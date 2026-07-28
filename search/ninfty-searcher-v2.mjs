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
// KNOWN GAP (flagged for commander/mathematician review, not silently decided):
// precondition E-5 ("divisor orientation", spec Sec.2, sourced from external
// dependency S5/prop-S5-1) is NOT algebraically derivable from (a,p,f6) alone
// without the external S5 curve/dessin data, which is outside this lane's
// literature-gate scope. This implementation therefore treats E-5 as an
// EXPLICIT DECLARED INPUT FLAG (`candidate.orientation_declared_ok`, boolean,
// required) rather than a computed predicate. Absence of the flag is
// fail-closed (treated as E-5 violation, code [6]). This is a design
// simplification, not a claim that E-5 has been derived.

import { createHash } from 'node:crypto';

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

  // E-5: divisor orientation — DECLARED INPUT FLAG (see file header KNOWN GAP).
  const orientationOk = candidate.orientation_declared_ok === true;
  if (!orientationOk) R.add('precondition/divisor-orientation');

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

  const ramComponents = [
    { locus_type: 'a-pair-locus', ideal_generator: polyToCoeffStrings(d), multiplicity: 1 },
    { locus_type: 'p-locus', ideal_generator: polyToCoeffStrings(polyMonic(p)), multiplicity: 1 },
    { locus_type: 'weierstrass-locus', ideal_generator: polyToCoeffStrings(polyMonic(f6)), multiplicity: 1 },
  ];
  // branch divisor on P1: for this scope (x-only ideal data), the pushforward
  // of each locus is itself (identity map on the x-coordinate ideal); we tag
  // it distinctly to keep the two "native objects" of the certificate schema
  // (spec Sec.4.1) structurally separate even though the underlying ideals
  // coincide in this restricted scope.
  const branchComponents = ramComponents.map((c) => ({ ...c, pushforward_of: c.locus_type }));

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
    const bijection = matched.map(([i, j]) => ({ searcher_index: i, checker_index: j, locus_type: sc[i].locus_type }));
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
    searcher_native: {
      ramification_divisor_on_C_ref: searcherNative.ramification_divisor_on_C_ref,
      branch_divisor_on_P1_ref: searcherNative.branch_divisor_on_P1_ref,
      native_schema_id: searcherNative.native_schema_id,
      native_schema_digest: searcherNative.native_schema_digest,
      native_artifact_digest: searcherNative.native_artifact_digest,
    },
    checker_native: {
      ramification_divisor_on_C_ref: checkerNative.ramification_divisor_on_C_ref,
      branch_divisor_on_P1_ref: checkerNative.branch_divisor_on_P1_ref,
      native_schema_id: checkerNative.native_schema_id,
      native_schema_digest: checkerNative.native_schema_digest,
      native_artifact_digest: checkerNative.native_artifact_digest,
    },
    component_bijection: { ramification_divisor_on_C: ram.component_bijection, branch_divisor_on_P1: branch.component_bijection },
    exact_point_equality_witnesses: { ramification_divisor_on_C: ram.exact_point_equality_witnesses, branch_divisor_on_P1: branch.exact_point_equality_witnesses },
    distinctness_witnesses: { ramification_divisor_on_C: ram.distinctness_witnesses, branch_divisor_on_P1: branch.distinctness_witnesses },
    multiplicity_equalities: { ramification_divisor_on_C: ram.multiplicity_equalities, branch_divisor_on_P1: branch.multiplicity_equalities },
    chart_overlap_witnesses: { note: 'single chart declared (chart_ids has one entry); no overlap to witness', charts: 1 },
    total_coverage_and_no_extra_component_witness: { ramification_divisor_on_C: ram.total_coverage_and_no_extra_component_witness, branch_divisor_on_P1: branch.total_coverage_and_no_extra_component_witness },
    pushforward_compatibility_witness: {
      note: 'x-only scope: pushforward is the identity on x-coordinate ideals in this lane',
      ok: true,
    },
  };
  cert.certificate_digest = digestOf(cert);
  return cert;
}
