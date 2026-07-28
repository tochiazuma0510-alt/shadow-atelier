// search/ninfty-searcher-v2.mjs
//
// N_infty stage-2 searcher v2 — lane A (decision lane / node runtime).
// Freeze: mb/ninfty-stage2-freeze/e2c9c701-e41d51db-df59b25f
//   predicate_spec_id = mb/ninfty-stage2-predicate/v18
//   verifier_contract_id = mb/ninfty-verifier-contract/v13
//   dependency_manifest_schema_id = mb/dependency-manifest/v13
//
// Implements:
//   - decision-lane predicate (spec Sec.3 T-1 / Sec.5.3.1 reject_priority[1..8]
//     + the two [13]/[15] integrity identities that are checkable from (a,p,f6,C)
//     alone without curve-theoretic root-finding).
//   - the D-2 divisor_equality_certificate generator (spec Sec.4.1/4.2), producing
//     witnesses of BOTH kinds (ideal-equality / disjointness) per the v7-erratum
//     type separation.
//   - a native artifact builder ("searcher_native") for lane A's audit-lane
//     production (spec Sec.3 "audit lane A: local differential -> R on C -> mu_* R").
//
// SELF-CONTAINED: no imports from any other file in this repository. This is a
// deliberate choice for the freeze-scoped lane-A/lane-B independence discipline
// (governing spec Sec.4.4 / verifier contract Sec.7 / dependency manifest Sec.3-6):
// keeping this file's own transitive dependency closure trivial (Node builtins
// only) makes the "declared_untrusted_inputs vs implementation closure" and TCB
// bookkeeping unambiguous for the freeze receipt's four empty TCB columns.
//
// PARTIAL PREDICATE / UNKNOWN NOTICE (spec Sec.7, Sec.9): EP (external positive
// control) has not run. This module and its outputs are NOT a "calibrated
// detector" and NOT a "complete search". Every entry point below is scoped to
// the decision-lane + D-2 certificate machinery only; it does not attempt the
// full audit-lane B curve-theoretic identities ([13]-[24] beyond the two that
// are checkable here) — those require the checker (lane B, python, out of scope
// for this file) and the fuller ramification-divisor computation.
//
// E-5 (divisor orientation) — DERIVED, per 裁定 113 / docs/notes/e5_interpretation_v1.md
// (Prop E5-D): under E-1..E-4, div(mu) = 5(inf_-) - 5(inf_+) automatically,
// with orientation fixed by E-3's sign (a5 = +p2 => P0 = inf_-, P_inf = inf_+;
// this implementation only ever accepts the a5=+p2 branch, per E-3's literal
// equality, so the derived orientation is always the standard one whenever
// E-1..E-4 hold). The four checks V-E5.1..V-E5.4 are exactly the f6/degree/
// leading-coeff/Pell checks already computed for E-1..E-4 — no new algebra is
// needed. `candidate.orientation_declared_ok` is now an OPTIONAL cross-check
// input (spec Sec.3.2 of the note's minimal-repair form): absent -> derived
// value is used and REJECT[6] is never raised on that basis; present and
// disagreeing with the derived value -> REJECT[6]; if the V-E5.1..4 premises
// themselves are false, the corresponding precondition code ([1]-[5]) already
// fires and no separate orientation check is attempted.

import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

// ---------------------------------------------------------------------------
// Freeze-receipt digest loader (裁定 115 item 1): certificates must pin the
// EXACT digests recorded in provenance/ninfty_freeze_receipt_sol75.md, read
// and parsed by code -- never hand-transcribed into a literal string here.
// The receipt's own header states "以下の exact block は返信ファイル F8.4
// から機械転記(sed 抽出・手写しなし)"; this loader applies the same
// discipline on the lane-A consuming side.
// ---------------------------------------------------------------------------

const THIS_DIR = dirname(fileURLToPath(import.meta.url));
export const DEFAULT_FREEZE_RECEIPT_PATH = join(THIS_DIR, '..', 'provenance', 'ninfty_freeze_receipt_sol75.md');

// Extracts `key = value` or `key =\n  value` scalar assignments from the
// receipt's fenced ```text ... ``` block. Only scalar (non-array) fields are
// needed for certificate pinning; array fields (external_dependencies[],
// allowed_shared_*[]) are intentionally left to other consumers.
export function parseFreezeReceiptFields(text) {
  const fenceMatch = text.match(/```text\n([\s\S]*?)\n```/);
  if (!fenceMatch) throw new Error('parseFreezeReceiptFields: no ```text fenced block found in receipt');
  const body = fenceMatch[1];
  const lines = body.split('\n');
  const fields = {};
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const m = line.match(/^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)$/);
    if (!m) continue;
    const key = m[1];
    let rhs = m[2].trim();
    if (rhs === '' || rhs === '[') {
      // value lives on the next non-empty line (receipt's two-line style),
      // or this is an array opener we deliberately skip (rhs === '[').
      if (rhs === '[') continue;
      let j = i + 1;
      while (j < lines.length && lines[j].trim() === '') j++;
      rhs = (lines[j] || '').trim();
    }
    rhs = rhs.replace(/^"(.*)"$/, '$1'); // strip surrounding quotes if present
    if (/^[0-9a-fA-F]+$/.test(rhs) || /^[a-zA-Z0-9/_.\-]+$/.test(rhs)) {
      fields[key] = rhs;
    }
  }
  return fields;
}

let _freezeReceiptCache = null;
export function loadFreezeReceiptDigests(path = DEFAULT_FREEZE_RECEIPT_PATH) {
  if (_freezeReceiptCache && _freezeReceiptCache.path === path) return _freezeReceiptCache.fields;
  const text = readFileSync(path, 'utf8');
  const fields = parseFreezeReceiptFields(text);
  const required = [
    'predicate_spec_id', 'predicate_spec_digest',
    'verifier_contract_id', 'verifier_contract_digest',
    'dependency_manifest_schema_id', 'dependency_manifest_schema_digest',
  ];
  const missing = required.filter((k) => !fields[k]);
  if (missing.length > 0) throw new Error('loadFreezeReceiptDigests: missing required fields: ' + missing.join(', '));
  _freezeReceiptCache = { path, fields };
  return fields;
}

// ---------------------------------------------------------------------------
// Exact rational arithmetic (BigInt numerator/denominator, always reduced).
// ---------------------------------------------------------------------------

function bigAbs(x) { return x < 0n ? -x : x; }
function bigGcd(a, b) {
  a = bigAbs(a); b = bigAbs(b);
  while (b) { [a, b] = [b, a % b]; }
  return a === 0n ? 1n : a;
}

export class Frac {
  constructor(n, d = 1n) {
    if (d === 0n) throw new Error('Frac: zero denominator');
    if (d < 0n) { n = -n; d = -d; }
    const g = bigGcd(n, d);
    this.n = n / g;
    this.d = d / g;
  }
  static from(x) {
    if (x instanceof Frac) return x;
    if (typeof x === 'bigint') return new Frac(x, 1n);
    if (typeof x === 'number') {
      if (!Number.isInteger(x)) throw new Error('Frac.from: non-integer number not supported, pass a string/BigInt ratio');
      return new Frac(BigInt(x), 1n);
    }
    if (typeof x === 'string') {
      const parts = x.split('/');
      if (parts.length === 1) return new Frac(BigInt(parts[0]), 1n);
      if (parts.length === 2) return new Frac(BigInt(parts[0]), BigInt(parts[1]));
      throw new Error('Frac.from: bad string ' + x);
    }
    throw new Error('Frac.from: unsupported type');
  }
  add(o) { o = Frac.from(o); return new Frac(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { o = Frac.from(o); return new Frac(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { o = Frac.from(o); return new Frac(this.n * o.n, this.d * o.d); }
  div(o) { o = Frac.from(o); if (o.n === 0n) throw new Error('Frac: division by zero'); return new Frac(this.n * o.d, this.d * o.n); }
  neg() { return new Frac(-this.n, this.d); }
  isZero() { return this.n === 0n; }
  eq(o) { o = Frac.from(o); return this.n === o.n && this.d === o.d; }
  toString() { return this.d === 1n ? this.n.toString() : `${this.n}/${this.d}`; }
  toJSON() { return this.toString(); }
}
export const F0 = new Frac(0n);
export const F1 = new Frac(1n);
function fr(x) { return Frac.from(x); }

// ---------------------------------------------------------------------------
// Polynomials over Q, ascending-coefficient arrays of Frac. deg(-infinity) := [].
// ---------------------------------------------------------------------------

export function polyFromInts(arr) { return arr.map((x) => fr(typeof x === 'bigint' ? x : (typeof x === 'string' ? x : BigInt(x)))); }
export function polyTrim(p) {
  let d = p.length - 1;
  while (d >= 0 && p[d].isZero()) d--;
  return p.slice(0, d + 1);
}
export function polyDeg(p) { return polyTrim(p).length - 1; }
export function polyIsZero(p) { return polyDeg(p) < 0; }

export function polyAdd(p, q) {
  const n = Math.max(p.length, q.length);
  const r = new Array(n).fill(F0);
  for (let i = 0; i < n; i++) r[i] = (p[i] || F0).add(q[i] || F0);
  return polyTrim(r);
}
export function polySub(p, q) {
  const n = Math.max(p.length, q.length);
  const r = new Array(n).fill(F0);
  for (let i = 0; i < n; i++) r[i] = (p[i] || F0).sub(q[i] || F0);
  return polyTrim(r);
}
export function polyScale(p, s) { s = fr(s); return polyTrim(p.map((c) => c.mul(s))); }
export function polyMul(p, q) {
  const dp = polyDeg(p), dq = polyDeg(q);
  if (dp < 0 || dq < 0) return [];
  const r = new Array(dp + dq + 1).fill(F0);
  for (let i = 0; i <= dp; i++) {
    if (p[i].isZero()) continue;
    for (let j = 0; j <= dq; j++) {
      if (q[j].isZero()) continue;
      r[i + j] = r[i + j].add(p[i].mul(q[j]));
    }
  }
  return polyTrim(r);
}
export function polyDerivative(p) {
  const d = polyDeg(p);
  if (d <= 0) return [];
  const r = new Array(d).fill(F0);
  for (let i = 1; i <= d; i++) r[i - 1] = p[i].mul(fr(BigInt(i)));
  return polyTrim(r);
}
export function polyDivMod(p, q) {
  const dq = polyDeg(q);
  if (dq < 0) throw new Error('polyDivMod: division by zero polynomial');
  let rem = polyTrim(p);
  const lcQ = q[dq];
  const quotDeg = polyDeg(rem) - dq;
  const quot = new Array(quotDeg >= 0 ? quotDeg + 1 : 0).fill(F0);
  while (true) {
    const dr = polyDeg(rem);
    if (dr < dq) break;
    const factor = rem[dr].div(lcQ);
    const shift = dr - dq;
    quot[shift] = factor;
    const sub = new Array(dr + 1).fill(F0);
    for (let i = 0; i <= dq; i++) sub[i + shift] = q[i].mul(factor);
    rem = polySub(rem, sub);
  }
  return { quot: polyTrim(quot), rem: polyTrim(rem) };
}
export function polyGCD(p, q) {
  let a = polyTrim(p), b = polyTrim(q);
  if (polyIsZero(a)) return b;
  if (polyIsZero(b)) return a;
  while (!polyIsZero(b)) {
    const { rem } = polyDivMod(a, b);
    a = b; b = rem;
  }
  return a;
}
export function polyMonic(p) {
  const d = polyDeg(p);
  if (d < 0) return p;
  return polyScale(p, F1.div(p[d]));
}
export function polyEqual(p, q) {
  const pt = polyTrim(p), qt = polyTrim(q);
  if (pt.length !== qt.length) return false;
  for (let i = 0; i < pt.length; i++) if (!pt[i].eq(qt[i])) return false;
  return true;
}
export function polyToCoeffStrings(p) { return polyTrim(p).map((c) => c.toString()); }
export function polyLeading(p) { const d = polyDeg(p); return d < 0 ? F0 : p[d]; }

// ---------------------------------------------------------------------------
// Canonical serialization + digest (Node builtin crypto — runtime/hash-primitive
// role, not a math-helper per dependency manifest v13 Sec.5.1 H-3/H-3a).
// ---------------------------------------------------------------------------

export function canonicalSerialize(obj) {
  function sort(x) {
    if (Array.isArray(x)) return x.map(sort);
    if (x && typeof x === 'object') {
      const out = {};
      for (const k of Object.keys(x).sort()) out[k] = sort(x[k]);
      return out;
    }
    return x;
  }
  return JSON.stringify(sort(obj));
}
export function sha256Hex(s) { return createHash('sha256').update(s, 'utf8').digest('hex'); }
export function digestOf(obj) { return sha256Hex(canonicalSerialize(obj)); }

// ---------------------------------------------------------------------------
// Decision-lane predicate: E-1..E-6 + T-1, plus the two purely-algebraic
// integrity identities [13] (pell-implies-coprime) and [15] (pell-derivative,
// eqn (60.5) a' =. p*d) that are checkable from (a,p,f6,C) without further
// curve data. All OTHER integrity codes ([9]-[12],[14],[16]-[26]) belong to
// the certificate/verifier layer (see checkStage2Candidate's `certificateAware`
// param) or to audit-lane-B curve data this file does not compute.
// ---------------------------------------------------------------------------

const REJECT_PRIORITY = [
  'precondition/degree-mismatch',            // [1]
  'precondition/f6-not-monic',               // [2]
  'precondition/curve-not-squarefree',       // [3]
  'precondition/leading-coeff-mismatch',     // [4]
  'precondition/pell-violation',             // [5]
  'precondition/divisor-orientation',        // [6]
  'triple-root-of-a',                        // [7]
  'a-partition-mismatch',                    // [8]
];

// spec Sec.5.3.2 numeric codes, for cross-reference / result vectors elsewhere.
export const REASON_CODE_NUMBER = {
  'precondition/degree-mismatch': 1,
  'precondition/f6-not-monic': 2,
  'precondition/curve-not-squarefree': 3,
  'precondition/leading-coeff-mismatch': 4,
  'precondition/pell-violation': 5,
  'precondition/divisor-orientation': 6,
  'triple-root-of-a': 7,
  'a-partition-mismatch': 8,
  'sealed-field-leak': 9,
  'deterministic-digest-exposed': 10,
  'shared-helper-detected': 11,
  'digest-mismatch': 12,
  'pell-implies-coprime-mismatch': 13,
  'divisor-identity': 14,
  'pell-derivative-mismatch': 15,
  'chart-degree-mismatch': 16,
  'p-locus-unhandled': 17,
  'weierstrass-unhandled': 18,
  'infinity-unhandled': 19,
  'rh-mismatch': 20,
  'extra-branch-value': 21,
  'finite-branch-count-mismatch': 22,
  'branch-pair-not-harmonic': 23,
  'finite-partition-cross-mismatch': 24,
  'divisor-equality-failure': 25,
  'verifier-result-mismatch': 26,
  accepted: 'accepted',
};

// T-1 sub-check, exported standalone so it can be unit-tested in isolation
// (used by the code[7]-vs-code[8] negative fixture that is NOT accompanied by
// a Pell-consistent (p,f6,C) triple — see search/certs/fixtures-lanea.mjs for
// the documented reason).
export function checkT1(aCoeffs) {
  const a = polyFromInts(aCoeffs);
  const ad = polyDerivative(a);
  const add = polyDerivative(ad);
  const d = polyMonic(polyGCD(a, ad));
  const dDeg = polyDeg(d);
  const dSquarefree = polyDeg(polyGCD(d, polyDerivative(d))) === 0;
  const tripleDeg = polyDeg(polyGCD(d, add)); // deg gcd(a,a',a'')
  if (tripleDeg > 0 || (dDeg === 2 && !dSquarefree) || dDeg > 2) {
    return { ok: false, code: 'triple-root-of-a', dDeg, dSquarefree, tripleDeg };
  }
  if (dDeg !== 2 || !dSquarefree) {
    return { ok: false, code: 'a-partition-mismatch', dDeg, dSquarefree, tripleDeg };
  }
  return { ok: true, code: null, dDeg, dSquarefree, tripleDeg, d: polyToCoeffStrings(d) };
}

// candidate = { a: [c0..c5], p: [c0..c2], f6: [c0..c6], orientation_declared_ok: bool }
// All coefficient arrays are ascending-degree, elements coercible via Frac.from
// (integer, BigInt, or "num/den" string).
export function evaluateDecisionLane(candidate) {
  const R = new Set(); // detected reject reasons (spec Sec.5.3.1, evaluated collectively)
  const I = new Set(); // detected integrity reasons among those computable here

  const a = polyFromInts(candidate.a);
  const p = polyFromInts(candidate.p);
  const f6 = polyFromInts(candidate.f6);

  const degA = polyDeg(a), degP = polyDeg(p), degF6 = polyDeg(f6);
  if (degA !== 5 || degP !== 2 || degF6 !== 6) R.add('precondition/degree-mismatch');

  // Only proceed with the rest of the pure-algebra checks if degrees are usable
  // (spec Sec.5.3: checks are evaluated collectively, not short-circuited; but
  // a-priori-wrong-degree data cannot feed later checks meaningfully, so we
  // still attempt them defensively where BigInt indexing is safe).
  let f6Monic = false, f6Squarefree = false;
  if (degF6 === 6) {
    f6Monic = polyLeading(f6).eq(F1);
    f6Squarefree = polyDeg(polyGCD(f6, polyDerivative(f6))) === 0;
    if (!f6Monic) R.add('precondition/f6-not-monic');
    if (!f6Squarefree) R.add('precondition/curve-not-squarefree');
  }

  let leadingMatch = false;
  if (degA === 5 && degP === 2) {
    leadingMatch = a[5].eq(p[2]) && !a[5].isZero();
    if (!leadingMatch) R.add('precondition/leading-coeff-mismatch');
  }

  // Pell: a^2 - f6*p^2 = C, a nonzero constant.
  let pellC = null, pellOk = false;
  if (degA === 5 && degP === 2 && degF6 === 6) {
    const lhs = polySub(polyMul(a, a), polyMul(f6, polyMul(p, p)));
    const lhsDeg = polyDeg(lhs);
    if (lhsDeg === 0 && !lhs[0].isZero()) {
      pellOk = true;
      pellC = lhs[0];
    } else if (lhsDeg < 0) {
      pellOk = false; // C would be 0, forbidden
    } else {
      pellOk = false;
    }
    if (!pellOk) R.add('precondition/pell-violation');
  }

  // E-5: divisor orientation — DERIVED (Prop E5-D, 裁定 113 / e5_interpretation_v1.md).
  // V-E5.1..V-E5.4 are exactly the f6/degree/leading-coeff/Pell checks above.
  const e5PremisesHold = degF6 === 6 && f6Monic && f6Squarefree && degA === 5 && degP === 2 && leadingMatch && pellOk;
  let orientationOk = null; // null = premises not decidable here (some earlier code already fired)
  if (e5PremisesHold) {
    // derived orientation is always the standard one (P0=inf_-, P_inf=inf_+),
    // since leadingMatch as checked above only accepts a5=+p2 (E-3 literal equality).
    const derivedOrientationOk = true;
    orientationOk = derivedOrientationOk;
    if (typeof candidate.orientation_declared_ok === 'boolean' && candidate.orientation_declared_ok !== derivedOrientationOk) {
      R.add('precondition/divisor-orientation'); // declared cross-check disagrees with the derivation
      orientationOk = false;
    }
    // orientation_declared_ok absent (undefined): derived value is authoritative, no REJECT.
  }
  // If e5PremisesHold is false, V-E5.1..4 already surfaced their own codes
  // ([1]/[2]/[3]/[4]/[5] as applicable) above; E-5 is not separately checked.

  // E-6: gcd(a,p)=1 is automatic from E-4 + C != 0 (spec Sec.2). If Pell passed
  // but gcd(a,p) != 1 anyway, that is a theorem-forced-identity break =>
  // INTEGRITY_STOP, not REJECT (spec Sec.2, code [13]).
  if (pellOk && degA === 5 && degP === 2) {
    const gcdAP = polyDeg(polyGCD(a, p));
    if (gcdAP !== 0) I.add('pell-implies-coprime-mismatch');
  }

  // T-1
  let t1 = null;
  if (degA === 5) {
    t1 = checkT1(candidate.a);
    if (!t1.ok) R.add(t1.code);
  }

  // (60.5) a' =. p*d  (code [15]) — only meaningful once T-1 passed with a
  // genuine degree-2 squarefree d, and preconditions hold.
  if (t1 && t1.ok && pellOk && leadingMatch) {
    const ad = polyDerivative(a);
    const d = polyFromInts(t1.d);
    const rhs = polyMonic(polyMul(p, d));
    const lhs = polyMonic(ad);
    if (!polyEqual(lhs, rhs)) I.add('pell-derivative-mismatch');
  }

  const reasonCodesR = canonicalSortByPriority([...R], REJECT_PRIORITY);
  const reasonCodesI = canonicalSortByIntegrity([...I]);

  let verdict, primary, allReasonCodes;
  if (I.size > 0) {
    verdict = 'INTEGRITY_STOP';
    primary = reasonCodesI[0];
    allReasonCodes = canonicalSortByIntegrity([...I, ...R]);
  } else if (R.size > 0) {
    verdict = 'REJECT';
    primary = reasonCodesR[0];
    allReasonCodes = reasonCodesR;
  } else {
    verdict = 'ACCEPT';
    primary = 'accepted';
    allReasonCodes = ['accepted'];
  }

  return {
    verdict,
    primary_reason_code: primary,
    all_reason_codes: allReasonCodes,
    a_root_partition: t1 && t1.ok ? [2, 2, 1] : null,
    finite_branch_pair_candidate_C: pellOk ? pellC.toString() : null,
    diagnostics: {
      degA, degP, degF6, f6Monic, f6Squarefree, leadingMatch, pellOk,
      t1: t1 ? { dDeg: t1.dDeg, dSquarefree: t1.dSquarefree, tripleDeg: t1.tripleDeg } : null,
      orientationOk,
    },
  };
}

function canonicalSortByPriority(codes, priorityList) {
  return [...codes].sort((x, y) => priorityList.indexOf(x) - priorityList.indexOf(y));
}
const INTEGRITY_PRIORITY = [
  'sealed-field-leak', 'deterministic-digest-exposed', 'shared-helper-detected',
  'digest-mismatch', 'pell-implies-coprime-mismatch', 'divisor-identity',
  'pell-derivative-mismatch', 'chart-degree-mismatch', 'p-locus-unhandled',
  'weierstrass-unhandled', 'infinity-unhandled', 'rh-mismatch', 'extra-branch-value',
  'finite-branch-count-mismatch', 'branch-pair-not-harmonic', 'finite-partition-cross-mismatch',
  'divisor-equality-failure', 'verifier-result-mismatch',
];
export function canonicalSortByIntegrity(codes) {
  const uniq = [...new Set(codes)];
  return uniq.sort((x, y) => {
    const ix = INTEGRITY_PRIORITY.indexOf(x), iy = INTEGRITY_PRIORITY.indexOf(y);
    if (ix === -1 && iy === -1) return x < y ? -1 : x > y ? 1 : 0;
    if (ix === -1) return 1;
    if (iy === -1) return -1;
    return ix - iy;
  });
}
export { INTEGRITY_PRIORITY, REJECT_PRIORITY };

// ---------------------------------------------------------------------------
// Native artifact ("searcher_native"): ramification-divisor-on-C and
// branch-divisor-on-P1 components, represented as PRINCIPAL IDEALS of Q[x]
// (monic generator polynomials), NOT as explicit root values. This is how the
// implementation honors "searcher は resultant を使わない" and "純 ℚ 有理数算術":
// components are given by the gcd-derived locus polynomials themselves
// (spec Sec.1.7-1.8's d = gcd(a,a'), p(x), f6(x)), never by factoring over
// Qbar. component identity/comparison is by exact polynomial (ideal) equality,
// which is exactly what the witness machinery in Sec.4.2 requires.
//
// SCOPE NOTE: this builds only the components derivable from T-1/T-2/T-3/T-4
// (the finite non-fixed pair locus `d`, the p-locus, the Weierstrass locus).
// The two-infinity component (T-5) and the RH/harmonicity/branch-count global
// checks (T-7) are NOT computed here (would require the fuller curve
// machinery out of this lane's implemented scope) — codes [16]-[24] beyond
// what evaluateDecisionLane already covers are therefore always left ABSENT
// (not PASS) in the result vector, per contract Sec.3.4 R-2's ABSENT/FAIL
// distinction, and are reported as UNKNOWN, never asserted PASS.
// ---------------------------------------------------------------------------

export function buildSearcherNative(candidate) {
  const a = polyFromInts(candidate.a);
  const p = polyFromInts(candidate.p);
  const f6 = polyFromInts(candidate.f6);
  const ad = polyDerivative(a);
  const d = polyMonic(polyGCD(a, ad)); // finite non-fixed branch-pair locus (T-1/T-2)

  // 裁定 139 item 2: each component carries an explicit component_id, minted
  // by the generator, so the verifier can reconstruct the two native
  // component sets from the native artifacts themselves rather than trusting
  // a certificate-declared domain/codomain list. IDs are scoped per native
  // object (ram vs branch) since a bijection edge always names both sides
  // explicitly.
  const ramComponents = [
    { component_id: 'ramification_divisor_on_C_ref:a-pair-locus', locus_type: 'a-pair-locus', ideal_generator: polyToCoeffStrings(d), multiplicity: 1 },
    { component_id: 'ramification_divisor_on_C_ref:p-locus', locus_type: 'p-locus', ideal_generator: polyToCoeffStrings(polyMonic(p)), multiplicity: 1 },
    { component_id: 'ramification_divisor_on_C_ref:weierstrass-locus', locus_type: 'weierstrass-locus', ideal_generator: polyToCoeffStrings(polyMonic(f6)), multiplicity: 1 },
  ];
  // branch divisor on P1: for this scope (x-only ideal data), the pushforward
  // of each locus is itself (identity map on the x-coordinate ideal); we tag
  // it distinctly to keep the two "native objects" of the certificate schema
  // (spec Sec.4.1) structurally separate even though the underlying ideals
  // coincide in this restricted scope.
  const branchComponents = ramComponents.map((c) => ({
    ...c,
    component_id: 'branch_divisor_on_P1_ref:' + c.locus_type,
    pushforward_of: c.locus_type,
  }));

  const native = {
    ramification_divisor_on_C_ref: { components: ramComponents },
    branch_divisor_on_P1_ref: { components: branchComponents },
  };
  const native_artifact_digest = digestOf(native);
  return {
    native_schema_id: 'mb/ninfty-stage2-predicate/v18#cert-schema',
    native_schema_digest: null, // filled by caller once schema digest is pinned by receipt
    ramification_divisor_on_C_ref: native.ramification_divisor_on_C_ref,
    branch_divisor_on_P1_ref: native.branch_divisor_on_P1_ref,
    native_artifact_digest,
  };
}

// ---------------------------------------------------------------------------
// Witness generation (spec Sec.4.2): kind = ideal-equality (point identity,
// via reduction-to-zero of each generator against the OTHER ideal's monic
// form — valid because Q[x] is a PID so "reduced Groebner basis" collapses to
// "the monic generator") and kind = disjointness (Bezout 1 = u*g1 + v*g2,
// used ONLY for injectivity / no-extra-component, never for point identity —
// this is the exact type separation erratum E1 of spec v7 requires).
// ---------------------------------------------------------------------------

// Extended Euclidean algorithm over Q[x]: returns {g, u, v} with u*a+v*b=g.
function polyExtGCD(a, b) {
  let old_r = polyTrim(a), r = polyTrim(b);
  let old_s = [F1], s = [];
  let old_t = [], t = [F1];
  while (!polyIsZero(r)) {
    const { quot } = polyDivMod(old_r, r);
    const newR = polySub(old_r, polyMul(quot, r));
    old_r = r; r = newR;
    const newS = polySub(old_s, polyMul(quot, s));
    old_s = s; s = newS;
    const newT = polySub(old_t, polyMul(quot, t));
    old_t = t; t = newT;
  }
  return { g: old_r, u: old_s, v: old_t };
}

// reduction-to-zero certificate: reduce generator g by the reduced (monic)
// form of ideal J = (h); returns the quotient sequence needed to witness
// g mod h == 0, or null if g mod h != 0.
function reductionToZeroWitness(g, h) {
  const hm = polyMonic(h);
  if (polyIsZero(hm)) return null;
  const { quot, rem } = polyDivMod(polyTrim(g), hm);
  if (!polyIsZero(rem)) return null;
  return {
    tag: 'reduction-to-zero',
    dividend: polyToCoeffStrings(g),
    divisor_monic: polyToCoeffStrings(hm),
    quotient: polyToCoeffStrings(quot),
    remainder: polyToCoeffStrings(rem),
  };
}

// Builds an ideal-equality witness for a pair of matched components whose
// ideal_generator polynomials are claimed equal, by mutually reducing each
// generator against the other's monic form (both directions must reduce to
// zero for I_1 = I_2 in the PID Q[x]).
export function buildIdealEqualityWitness(genA, genB) {
  const a = polyFromInts(genA), b = polyFromInts(genB);
  const fwd = reductionToZeroWitness(a, b);
  const bwd = reductionToZeroWitness(b, a);
  if (!fwd || !bwd) return { kind: 'ideal-equality', ok: false, forward: fwd, backward: bwd };
  return { kind: 'ideal-equality', ok: true, forward: fwd, backward: bwd };
}

// Builds a disjointness (Bezout) witness for two DIFFERENT components, used
// only for W-1 injectivity / W-5 no-extra-component, never for point identity.
export function buildDisjointnessWitness(genP, genQ) {
  const p = polyMonic(polyFromInts(genP)), q = polyMonic(polyFromInts(genQ));
  const { g, u, v } = polyExtGCD(p, q);
  const gm = polyMonic(g);
  const isUnit = polyDeg(gm) === 0 && !gm[0] ? false : polyDeg(gm) === 0;
  // 1 = (u/lc(g)) * p + (v/lc(g)) * q  when gcd is a nonzero constant.
  if (!isUnit) return { kind: 'disjointness', ok: false, reason: 'gcd-not-unit', gcd_degree: polyDeg(gm) };
  const lc = polyDeg(g) >= 0 ? g[polyDeg(g)] : F0;
  const uu = polyScale(u, F1.div(lc));
  const vv = polyScale(v, F1.div(lc));
  // sanity re-check: uu*p+vv*q == 1
  const check = polyAdd(polyMul(uu, p), polyMul(vv, q));
  const ok = polyDeg(check) === 0 && check[0].eq(F1);
  return {
    kind: 'disjointness', ok,
    generator_P: polyToCoeffStrings(p), generator_Q: polyToCoeffStrings(q),
    bezout_u: polyToCoeffStrings(uu), bezout_v: polyToCoeffStrings(vv),
    reduction_tag: 'reduction-to-one',
  };
}

// ---------------------------------------------------------------------------
// D-2 divisor_equality_certificate generator (spec Sec.4.1). This is the
// GENERATOR only (spec G-1: "not a third decision lane; cannot output ACCEPT
// on its own"). It builds witnesses from BOTH native artifacts by component
// locus_type matching (component_bijection), producing ideal-equality
// witnesses for matched pairs and disjointness witnesses for cross-checking
// distinctness of unmatched/extra components.
// ---------------------------------------------------------------------------

export function generateCertificate({ candidateRef, searcherNative, checkerNative, predicateSpecId, predicateSpecDigest }) {
  // 裁定 115 item 1: pin from the freeze receipt (machine-parsed), never a
  // hand-typed placeholder. Caller may still override explicitly (e.g. for
  // negative/digest-mismatch fixtures that deliberately corrupt the pin), but
  // the DEFAULT is always the receipt's own recorded values.
  if (predicateSpecId === undefined || predicateSpecDigest === undefined) {
    const receipt = loadFreezeReceiptDigests();
    if (predicateSpecId === undefined) predicateSpecId = receipt.predicate_spec_id;
    if (predicateSpecDigest === undefined) predicateSpecDigest = receipt.predicate_spec_digest;
  }
  const ambient = {
    ambient_coordinate_ring_schema_id: 'mb/ninfty-lanea/ambient-ring/v1',
    ambient_coordinate_ring_schema_digest: sha256Hex('Q[x] (single chart, x-coordinate ideals only; y determined by locus type)'),
    ambient_quotient_relations: 'y^2 - f6(x) = 0 (curve model); component ideals below are pulled back to Q[x] via the x-coordinate projection',
    coefficient_field_presentation_id: 'Q/standard',
    coefficient_field_presentation_digest: sha256Hex('Q/standard'),
    field_embedding_witness_schema_id: 'mb/ninfty-lanea/no-embedding-needed/v1',
    field_embedding_witness_schema_digest: sha256Hex('no-embedding-needed: all components rational-coefficient ideals in Q[x]'),
    monomial_order_id: 'lex-single-variable',
    monomial_order_digest: sha256Hex('lex-single-variable'),
    groebner_reduction_contract_id: 'mb/ninfty-lanea/pid-monic-reduction/v1',
    groebner_reduction_contract_digest: sha256Hex('Q[x] is a PID: reduced Groebner basis of a principal ideal is {monic(generator)}'),
  };

  // 裁定 139 item 3 / 裁定 142 item 3 (confirmed policy, self-contained by
  // construction): a _ref is a triple {artifact_id, digest, object_id OR
  // json_pointer}, with an OPTIONAL inline copy whose digest must match
  // exactly (mismatch -> existing [12] digest-mismatch, never silently
  // preferring one side). THIS LANE'S POLICY: every _ref this generator
  // produces uses the `object_id` variant AND ALWAYS carries `inline` --
  // never a bare external reference. This means every certificate lane A
  // emits is self-contained: a receiving verifier (verifier B included) can
  // resolve every _ref's data from the certificate blob alone, with no
  // external artifact store, no json_pointer lookup, and no round-trip back
  // to lane A. (lane A's OWN verifier A additionally accepts the
  // json_pointer variant when READING a certificate -- see
  // ninfty-verifier-a.mjs resolveRef -- for cross-lane/EP certificates that
  // legitimately choose that form; this generator itself just never emits it.)
  function makeRef(objectId, inlineData) {
    return { artifact_id: 'mb/ninfty-lanea/inline-artifact/' + objectId, digest: digestOf(inlineData), object_id: objectId, inline: inlineData };
  }

  function objectsOf(native) {
    return {
      ramification_divisor_on_C: native.ramification_divisor_on_C_ref.components,
      branch_divisor_on_P1: native.branch_divisor_on_P1_ref.components,
    };
  }
  const sObj = objectsOf(searcherNative);
  const cObj = objectsOf(checkerNative);

  function buildForObject(name) {
    const sc = sObj[name], cc = cObj[name];
    const matched = [];
    const usedC = new Set();
    for (let i = 0; i < sc.length; i++) {
      const j = cc.findIndex((x, idx) => !usedC.has(idx) && x.locus_type === sc[i].locus_type);
      if (j >= 0) { matched.push([i, j]); usedC.add(j); }
    }
    // 裁定 139 item 2: component_bijection entries are EDGES naming both
    // sides' native digest + component_id explicitly, so the verifier can
    // reconstruct the vertex sets from the native artifacts and check
    // in/out-degree = 1 WITHOUT trusting this list as authority.
    const bijection = matched.map(([i, j]) => ({
      searcher_native_digest: searcherNative.native_artifact_digest,
      searcher_component_id: sc[i].component_id,
      checker_native_digest: checkerNative.native_artifact_digest,
      checker_component_id: cc[j].component_id,
    }));
    const exactWitnesses = matched.map(([i, j]) => ({
      locus_type: sc[i].locus_type,
      witness: buildIdealEqualityWitness(sc[i].ideal_generator, cc[j].ideal_generator),
    }));
    const multiplicityEqualities = matched.map(([i, j]) => ({
      locus_type: sc[i].locus_type, searcher_mult: sc[i].multiplicity, checker_mult: cc[j].multiplicity,
      equal: sc[i].multiplicity === cc[j].multiplicity,
    }));
    // distinctness witnesses: pairwise Bezout among the matched components'
    // generators (injectivity of the bijection) + coverage (no extras).
    const distinctness = [];
    for (let x = 0; x < matched.length; x++) {
      for (let y = x + 1; y < matched.length; y++) {
        const gi = sc[matched[x][0]].ideal_generator;
        const gj = sc[matched[y][0]].ideal_generator;
        distinctness.push({ pair: [matched[x][0], matched[y][0]], witness: buildDisjointnessWitness(gi, gj) });
      }
    }
    const noExtra = sc.length === matched.length && cc.length === matched.length;
    return {
      component_bijection: bijection,
      exact_point_equality_witnesses: exactWitnesses,
      distinctness_witnesses: distinctness,
      multiplicity_equalities: multiplicityEqualities,
      total_coverage_and_no_extra_component_witness: { searcher_count: sc.length, checker_count: cc.length, matched_count: matched.length, no_extra: noExtra },
    };
  }

  // 裁定 127: spec Sec.4.1's literal schema lists component_bijection /
  // exact_point_equality_witnesses / distinctness_witnesses /
  // multiplicity_equalities / total_coverage_and_no_extra_component_witness
  // as SINGLE flat fields -- there is no object-keyed (per-locus) nesting
  // anywhere in that literal text. The earlier lane-A shape
  // ({ramification_divisor_on_C: [...], branch_divisor_on_P1: [...]}) added
  // a nesting layer the schema does not specify, which is exactly the kind
  // of unlicensed shape the coordinator's dispatch flags. Contract Sec.2
  // separately requires "both of the two native objects" to be checked by
  // W-1..W-6, without specifying HOW a flat field distinguishes the two --
  // this is UNKNOWN and is not silently resolved by adding a nesting layer;
  // instead each entry in each flat array carries an explicit
  // `divisor_object` tag using the EXACT literal token names spec/contract
  // already use (`ramification_divisor_on_C_ref` / `branch_divisor_on_P1_ref`
  // from spec Sec.4.1's own searcher_native/checker_native sub-schema),
  // rather than inventing new vocabulary.
  const DIVISOR_OBJECT_RAM = 'ramification_divisor_on_C_ref';
  const DIVISOR_OBJECT_BRANCH = 'branch_divisor_on_P1_ref';

  function tagAll(arr, tag) { return arr.map((e) => ({ divisor_object: tag, ...e })); }

  const ram = buildForObject('ramification_divisor_on_C');
  const branch = buildForObject('branch_divisor_on_P1');

  const cert = {
    schema_id: predicateSpecId + '#cert-schema',
    schema_digest: predicateSpecDigest,
    predicate_spec_id: predicateSpecId,
    predicate_spec_digest: predicateSpecDigest,
    candidate_ref: candidateRef,
    curve_model_digest: sha256Hex('y^2 = f6(x), mu = a(x)+p(x)y (lane A candidate-scoped model)'),
    chart_ids: ['x-chart-single'],
    ...ambient,
    // 裁定 139 item 3: _ref fields are now {artifact_id, digest, object_id, inline}
    // triples (inline included since this lane has no external artifact store).
    searcher_native: {
      ramification_divisor_on_C_ref: makeRef('searcher-ramification_divisor_on_C_ref', searcherNative.ramification_divisor_on_C_ref),
      branch_divisor_on_P1_ref: makeRef('searcher-branch_divisor_on_P1_ref', searcherNative.branch_divisor_on_P1_ref),
      native_schema_id: searcherNative.native_schema_id,
      native_schema_digest: searcherNative.native_schema_digest,
      native_artifact_digest: searcherNative.native_artifact_digest,
    },
    checker_native: {
      ramification_divisor_on_C_ref: makeRef('checker-ramification_divisor_on_C_ref', checkerNative.ramification_divisor_on_C_ref),
      branch_divisor_on_P1_ref: makeRef('checker-branch_divisor_on_P1_ref', checkerNative.branch_divisor_on_P1_ref),
      native_schema_id: checkerNative.native_schema_id,
      native_schema_digest: checkerNative.native_schema_digest,
      native_artifact_digest: checkerNative.native_artifact_digest,
    },
    // FLAT per spec Sec.4.1 literal schema (裁定 127); per-entry divisor_object tag.
    component_bijection: [...tagAll(ram.component_bijection, DIVISOR_OBJECT_RAM), ...tagAll(branch.component_bijection, DIVISOR_OBJECT_BRANCH)],
    exact_point_equality_witnesses: [...tagAll(ram.exact_point_equality_witnesses, DIVISOR_OBJECT_RAM), ...tagAll(branch.exact_point_equality_witnesses, DIVISOR_OBJECT_BRANCH)],
    distinctness_witnesses: [...tagAll(ram.distinctness_witnesses, DIVISOR_OBJECT_RAM), ...tagAll(branch.distinctness_witnesses, DIVISOR_OBJECT_BRANCH)],
    multiplicity_equalities: [...tagAll(ram.multiplicity_equalities, DIVISOR_OBJECT_RAM), ...tagAll(branch.multiplicity_equalities, DIVISOR_OBJECT_BRANCH)],
    // W-4 (裁定 133: docs/notes/cert_shape_interpretation_v2.md (i)) --
    // FLAT array of 2 entries (one per divisor_object, same outer shape as
    // the other 6 fields), each entry = {divisor_object, status,
    // per_overlap_witnesses:[...]}. This lane's native scope declares only
    // ONE chart (x-chart-single), so there is no second chart to produce a
    // genuine per-overlap witness against -- STRUCTURED ABSENT per entry,
    // not an implied PASS.
    chart_overlap_witnesses: [
      {
        divisor_object: DIVISOR_OBJECT_RAM,
        status: 'ABSENT',
        per_overlap_witnesses: [], // would list {chart_pair, agree, generator_chart_a, generator_chart_b, ...} entries if >=2 charts existed
        reason: 'lane A native declares a single chart; no second chart exists to produce a genuine per-overlap witness. Structured ABSENT, not PASS.',
      },
      {
        divisor_object: DIVISOR_OBJECT_BRANCH,
        status: 'ABSENT',
        per_overlap_witnesses: [],
        reason: 'lane A native declares a single chart; no second chart exists to produce a genuine per-overlap witness. Structured ABSENT, not PASS.',
      },
    ],
    // FLAT: array of 2 entries, one per divisor object, each tagged.
    total_coverage_and_no_extra_component_witness: [
      { divisor_object: DIVISOR_OBJECT_RAM, ...ram.total_coverage_and_no_extra_component_witness },
      { divisor_object: DIVISOR_OBJECT_BRANCH, ...branch.total_coverage_and_no_extra_component_witness },
    ],
    // W-6 (裁定 139 item 1, docs/notes/cert_shape_interpretation_v3.md 条項 2/9):
    // divisor_object duplication is FORBIDDEN for pushforward (it relates the
    // TWO divisors + a map on ONE side, not a per-divisor-object fact) --
    // native_side-tagged 2 entries (searcher / checker), each
    // {native_side, ramification_ref, branch_ref, map_ref, witness_ref}
    // (all four are _ref triples per item 3). This lane represents components
    // by IDEALS (locus polynomials), never explicit root/point enumeration
    // over Qbar, so witness_ref.inline.points is honestly empty (STRUCTURED
    // ABSENT), while ramification_ref/branch_ref/map_ref carry real inline
    // data (the native divisors themselves + the identity pushforward map
    // description for this lane's single-chart scope).
    pushforward_compatibility_witness: [
      {
        native_side: 'searcher',
        ramification_ref: makeRef('searcher-pushforward-ramification', searcherNative.ramification_divisor_on_C_ref),
        branch_ref: makeRef('searcher-pushforward-branch', searcherNative.branch_divisor_on_P1_ref),
        map_ref: makeRef('searcher-pushforward-map', { description: 'x-coordinate identity pushforward (single-chart scope, no root-level map computed)' }),
        witness_ref: makeRef('searcher-pushforward-witness', { points: [], status: 'ABSENT', reason: 'lane A represents components by ideals, not explicit points; no point-level pushforward witness computed yet.' }),
      },
      {
        native_side: 'checker',
        ramification_ref: makeRef('checker-pushforward-ramification', checkerNative.ramification_divisor_on_C_ref),
        branch_ref: makeRef('checker-pushforward-branch', checkerNative.branch_divisor_on_P1_ref),
        map_ref: makeRef('checker-pushforward-map', { description: 'x-coordinate identity pushforward (single-chart scope, no root-level map computed)' }),
        witness_ref: makeRef('checker-pushforward-witness', { points: [], status: 'ABSENT', reason: 'lane A represents components by ideals, not explicit points; no point-level pushforward witness computed yet.' }),
      },
    ],
  };
  cert.certificate_digest = digestOf(cert);
  return cert;
}
