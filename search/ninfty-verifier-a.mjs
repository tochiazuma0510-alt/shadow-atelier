// search/ninfty-verifier-a.mjs
//
// N_infty stage-2 verifier A — lane A (decision lane / node runtime).
// Freeze: mb/ninfty-stage2-freeze/e2c9c701-e41d51db-df59b25f
//   governing spec    = mb/ninfty-stage2-predicate/v18
//   contract           = mb/ninfty-verifier-contract/v13
//   dependency manifest = mb/dependency-manifest/v13
//
// Implements contract Sec.3 (W-1..W-6 re-check procedure over a
// divisor_equality_certificate + both native artifacts), Sec.3.4 (canonical
// per-witness result vector R_A + result_digest_A), and the combination of
// R_A with an externally-supplied R_B into the FULL verdict state machine
// (governing spec Sec.5.3 + Sec.5.3.3 two-axis routing).
//
// INDEPENDENCE NOTE (contract G-3/G-4, Sec.7 C-1..C-9): this file is a
// SEPARATE, self-contained re-implementation of the Q[x] reduction / Bezout
// re-verification logic used by the generator in ninfty-searcher-v2.mjs. It
// does not import that file. Its own poly/ideal primitives below are
// deliberately written independently (different algorithm shape / variable
// naming) so that a bug specific to one implementation is not silently
// shared. This is still node/lane-A-internal reuse discipline, NOT the
// cross-lane (node vs python) independence the freeze receipt requires
// between verifier A and verifier B — that separation is by construction
// (this file never touches any python source).
//
// PARTIAL PREDICATE / UNKNOWN NOTICE: EP has not run. `combine()` below
// implements the full state-machine formula, but this lane alone cannot
// supply a genuine independent R_B (lane B/python is out of scope for this
// implementer task) — R_B must be supplied by the caller. All self-tests in
// search/ninfty-selftest-lanea.mjs that exercise concordance-axis codes
// ([26], and [24]+[26]) use an EXPLICITLY MOCKED R_B, clearly labeled as such,
// never presented as real lane-B output.

import { createHash } from 'node:crypto';

// --- independent Q[x] / Frac re-implementation (see INDEPENDENCE NOTE) ------

function gcdBig(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a === 0n ? 1n : a; }
class Q {
  constructor(n, d = 1n) {
    if (d === 0n) throw new Error('Q: zero denominator');
    if (d < 0n) { n = -n; d = -d; }
    const g = gcdBig(n, d);
    this.n = n / g; this.d = d / g;
  }
  static of(x) {
    if (x instanceof Q) return x;
    if (typeof x === 'bigint') return new Q(x, 1n);
    if (typeof x === 'string') {
      const parts = x.split('/');
      return parts.length === 2 ? new Q(BigInt(parts[0]), BigInt(parts[1])) : new Q(BigInt(parts[0]), 1n);
    }
    if (typeof x === 'number' && Number.isInteger(x)) return new Q(BigInt(x), 1n);
    throw new Error('Q.of: unsupported ' + x);
  }
  plus(o) { o = Q.of(o); return new Q(this.n * o.d + o.n * this.d, this.d * o.d); }
  minus(o) { o = Q.of(o); return new Q(this.n * o.d - o.n * this.d, this.d * o.d); }
  times(o) { o = Q.of(o); return new Q(this.n * o.n, this.d * o.d); }
  over(o) { o = Q.of(o); if (o.n === 0n) throw new Error('Q: /0'); return new Q(this.n * o.d, this.d * o.n); }
  zero() { return this.n === 0n; }
  same(o) { o = Q.of(o); return this.n === o.n && this.d === o.d; }
  str() { return this.d === 1n ? this.n.toString() : `${this.n}/${this.d}`; }
}
const ZERO = new Q(0n), ONE = new Q(1n);

function vecFromStrings(arr) { return arr.map((s) => Q.of(s)); }
function vTrim(v) { let d = v.length - 1; while (d >= 0 && v[d].zero()) d--; return v.slice(0, d + 1); }
function vDeg(v) { return vTrim(v).length - 1; }
function vAdd(v, w) { const n = Math.max(v.length, w.length); const r = []; for (let i = 0; i < n; i++) r.push((v[i] || ZERO).plus(w[i] || ZERO)); return vTrim(r); }
function vSub(v, w) { const n = Math.max(v.length, w.length); const r = []; for (let i = 0; i < n; i++) r.push((v[i] || ZERO).minus(w[i] || ZERO)); return vTrim(r); }
function vScale(v, s) { return vTrim(v.map((c) => c.times(s))); }
function vMul(v, w) {
  const dv = vDeg(v), dw = vDeg(w);
  if (dv < 0 || dw < 0) return [];
  const r = new Array(dv + dw + 1).fill(ZERO);
  for (let i = 0; i <= dv; i++) { if (v[i].zero()) continue; for (let j = 0; j <= dw; j++) { if (w[j].zero()) continue; r[i + j] = r[i + j].plus(v[i].times(w[j])); } }
  return vTrim(r);
}
function vDivMod(v, w) {
  const dw = vDeg(w);
  if (dw < 0) throw new Error('vDivMod: /0-poly');
  let rem = vTrim(v);
  const lc = w[dw];
  const qd = vDeg(rem) - dw;
  const quot = new Array(qd >= 0 ? qd + 1 : 0).fill(ZERO);
  while (true) {
    const dr = vDeg(rem);
    if (dr < dw) break;
    const f = rem[dr].over(lc);
    const sh = dr - dw;
    quot[sh] = f;
    const sub = new Array(dr + 1).fill(ZERO);
    for (let i = 0; i <= dw; i++) sub[i + sh] = w[i].times(f);
    rem = vSub(rem, sub);
  }
  return { quot: vTrim(quot), rem: vTrim(rem) };
}
function vMonic(v) { const d = vDeg(v); if (d < 0) return v; return vScale(v, ONE.over(v[d])); }
function vEq(v, w) { const a = vTrim(v), b = vTrim(w); if (a.length !== b.length) return false; for (let i = 0; i < a.length; i++) if (!a[i].same(b[i])) return false; return true; }
function vIsZero(v) { return vDeg(v) < 0; }
function toStrings(v) { return vTrim(v).map((c) => c.str()); }

function canonicalSerialize(obj) {
  function sort(x) {
    if (Array.isArray(x)) return x.map(sort);
    if (x && typeof x === 'object') { const out = {}; for (const k of Object.keys(x).sort()) out[k] = sort(x[k]); return out; }
    return x;
  }
  return JSON.stringify(sort(obj));
}
function sha256Hex(s) { return createHash('sha256').update(s, 'utf8').digest('hex'); }
function digestOf(obj) { return sha256Hex(canonicalSerialize(obj)); }
export { canonicalSerialize, sha256Hex, digestOf };

// --- W-2 / W-2' independent re-verification --------------------------------

// re-derive: does g reduce to 0 modulo monic(h)? (own implementation)
function reducesToZero(gStrs, hStrs) {
  const g = vecFromStrings(gStrs), h = vecFromStrings(hStrs);
  const hm = vMonic(h);
  if (vIsZero(hm)) return false;
  const { rem } = vDivMod(g, hm);
  return vIsZero(rem);
}

// Re-verify a claimed ideal-equality witness (kind must be 'ideal-equality',
// both forward/backward must carry a reduction-to-zero tag, and independently
// recomputing the reduction must agree with reduction to 0 in both
// directions). Per contract Sec.3.1: Bezout / untagged / digest-only /
// partition-only claims are REJECTED as evidence (return false).
function verifyIdealEqualityWitness(entry) {
  const w = entry.witness;
  if (!w || w.kind !== 'ideal-equality') return { pass: false, reason: 'wrong-kind-or-missing' };
  if (!w.forward || !w.backward) return { pass: false, reason: 'missing-direction' };
  if (w.forward.tag !== 'reduction-to-zero' || w.backward.tag !== 'reduction-to-zero') {
    return { pass: false, reason: 'untagged-reduction' };
  }
  const fwdOk = reducesToZero(w.forward.dividend, w.forward.divisor_monic);
  const bwdOk = reducesToZero(w.backward.dividend, w.backward.divisor_monic);
  if (!fwdOk || !bwdOk) return { pass: false, reason: 'reduction-nonzero' };
  return { pass: true };
}

// Re-verify a claimed disjointness (Bezout) witness: recompute u*P+v*Q and
// check it equals exactly 1 (own extended-gcd-free check: just recompute the
// linear combination from the claimed u,v — this is what "independently
// re-verify" means for a Bezout certificate; we do not need to reconstruct
// u,v ourselves, only confirm the claimed identity holds exactly).
function verifyDisjointnessWitness(entry) {
  const w = entry.witness;
  if (!w || w.kind !== 'disjointness') return { pass: false, reason: 'wrong-kind-or-missing' };
  if (!w.ok) return { pass: false, reason: 'generator-reported-not-unit' };
  if (w.reduction_tag !== 'reduction-to-one') return { pass: false, reason: 'untagged' };
  const P = vecFromStrings(w.generator_P), Qp = vecFromStrings(w.generator_Q);
  const u = vecFromStrings(w.bezout_u), v = vecFromStrings(w.bezout_v);
  const combo = vAdd(vMul(u, P), vMul(v, Qp));
  const ok = vDeg(combo) === 0 && combo[0].same(ONE);
  return { pass: ok, reason: ok ? null : 'bezout-identity-failed' };
}

// --- P-0.* ambient checks ----------------------------------------------------

function checkAmbient(cert) {
  const required = [
    'ambient_coordinate_ring_schema_id', 'ambient_coordinate_ring_schema_digest',
    'ambient_quotient_relations', 'coefficient_field_presentation_id', 'coefficient_field_presentation_digest',
    'monomial_order_id', 'monomial_order_digest', 'groebner_reduction_contract_id', 'groebner_reduction_contract_digest',
    'curve_model_digest', 'chart_ids', 'field_embedding_witness_schema_id', 'field_embedding_witness_schema_digest',
  ];
  const missing = required.filter((k) => cert[k] === undefined || cert[k] === null);
  return { pass: missing.length === 0, missing };
}

// --- W-4 / W-6 structured re-check (裁定 115 item 2) ------------------------
//
// Both witnesses are read as PASS/FAIL/ABSENT from their OWN declared
// `status` field plus (if present) independent re-verification of the
// per-overlap / per-point entries. A missing object, or status==='ABSENT',
// is read as ABSENT -- never silently promoted to PASS. This is what makes
// the certificate readable "without transformation" by verifier B: the shape
// (kind/status/entries) is the schema contract, not an implementation detail
// of lane A.

export function verifyChartOverlap_forTest(w) { return verifyChartOverlap(w); }
export function verifyPushforward_forTest(w) { return verifyPushforward(w); }

function verifyChartOverlap(w) {
  if (!w || typeof w !== 'object') return 'ABSENT';
  if (w.status === 'ABSENT') return 'ABSENT';
  if (!Array.isArray(w.per_overlap_witnesses) || w.per_overlap_witnesses.length === 0) return 'ABSENT';
  // Independent re-check: each declared overlap witness must claim agreement
  // AND (if it carries ideal generators for the two charts) must actually
  // reduce to the same monic ideal.
  const allOk = w.per_overlap_witnesses.every((ow) => {
    if (ow.agree !== true) return false;
    if (ow.generator_chart_a && ow.generator_chart_b) {
      return reducesToZero(ow.generator_chart_a, ow.generator_chart_b) && reducesToZero(ow.generator_chart_b, ow.generator_chart_a);
    }
    return true;
  });
  return allOk ? 'PASS' : 'FAIL';
}

function verifyPushforward(w) {
  if (!w || typeof w !== 'object') return 'ABSENT';
  if (w.status === 'ABSENT') return 'ABSENT';
  if (!Array.isArray(w.points) || w.points.length === 0) return 'ABSENT';
  const allOk = w.points.every((p) => p.match === true && p.ram_multiplicity === p.branch_multiplicity);
  return allOk ? 'PASS' : 'FAIL';
}

// --- W-1..W-6 for one object (ramification_divisor_on_C / branch_divisor_on_P1)

function verifyObject(certObj, searcherComponents, checkerComponents) {
  const R = {}; // per-witness result: PASS / FAIL / ABSENT

  // W-1: recheck bijection independently from ideal-equality witnesses only
  // (contract Sec.3.2: "constructed independently from W-2's point identity").
  const bij = certObj.bijection || [];
  let w1 = bij.length > 0 ? 'PASS' : 'ABSENT';
  const seenS = new Set(), seenC = new Set();
  for (const b of bij) {
    if (seenS.has(b.searcher_index) || seenC.has(b.checker_index)) { w1 = 'FAIL'; break; }
    seenS.add(b.searcher_index); seenC.add(b.checker_index);
    if (searcherComponents[b.searcher_index]?.locus_type !== checkerComponents[b.checker_index]?.locus_type) { w1 = 'FAIL'; break; }
  }
  R['W-1'] = w1;

  // W-2: ideal-equality witnesses
  const eqW = certObj.exactWitnesses || [];
  if (eqW.length === 0) {
    R['W-2'] = 'ABSENT';
  } else {
    R['W-2'] = eqW.every((e) => verifyIdealEqualityWitness(e).pass) ? 'PASS' : 'FAIL';
  }

  // W-2': disjointness witnesses
  const disW = certObj.distinctness || [];
  if (disW.length === 0) {
    R["W-2'"] = 'ABSENT';
  } else {
    R["W-2'"] = disW.every((e) => verifyDisjointnessWitness(e).pass) ? 'PASS' : 'FAIL';
  }

  // W-3: multiplicity equalities
  const me = certObj.multiplicityEqualities || [];
  R['W-3'] = me.length === 0 ? 'ABSENT' : (me.every((m) => m.equal === true) ? 'PASS' : 'FAIL');

  // W-4 (裁定 115 item 2): structured chart-atlas / per-overlap re-check.
  // status='ABSENT' is read literally as ABSENT (not PASS) -- honest
  // reporting of "lane A has no genuine multi-chart overlap data" rather than
  // a vacuous-PASS reading of "single chart declared".
  R['W-4'] = verifyChartOverlap(certObj.chartOverlap);

  // W-5: coverage / no extra
  const cov = certObj.coverage;
  R['W-5'] = cov ? (cov.no_extra === true ? 'PASS' : 'FAIL') : 'ABSENT';

  // W-6 (裁定 115 item 2): structured point-level pushforward re-check.
  R['W-6'] = verifyPushforward(certObj.pushforward);

  return R;
}

// --- top-level contract Sec.3 procedure -------------------------------------

// input: { certificate, searcherNativeBlob, checkerNativeBlob }
// searcherNativeBlob/checkerNativeBlob are the ACTUAL blobs verifier A read
// (for P-3.3 digest re-check against the certificate's declared digests).
export function runVerifierA({ certificate, searcherNativeBlob, checkerNativeBlob }) {
  const ambient = checkAmbient(certificate);

  // P-3.1 / P-3.2: predicate_spec_id/digest, schema_id/digest present & self-consistent.
  const p31 = certificate.predicate_spec_id === certificate.schema_id.split('#')[0] &&
              certificate.predicate_spec_digest === certificate.schema_digest;
  // P-3.3: native_artifact_digest matches what verifier A actually read.
  const searcherDigestOk = digestOf({
    ramification_divisor_on_C_ref: searcherNativeBlob.ramification_divisor_on_C_ref,
    branch_divisor_on_P1_ref: searcherNativeBlob.branch_divisor_on_P1_ref,
  }) === certificate.searcher_native.native_artifact_digest;
  const checkerDigestOk = digestOf({
    ramification_divisor_on_C_ref: checkerNativeBlob.ramification_divisor_on_C_ref,
    branch_divisor_on_P1_ref: checkerNativeBlob.branch_divisor_on_P1_ref,
  }) === certificate.checker_native.native_artifact_digest;
  const p33 = searcherDigestOk && checkerDigestOk;

  // 裁定 127: spec Sec.4.1's literal schema has NO object-keyed nesting for
  // the witness-group fields -- they are single flat fields. This verifier
  // therefore reads them as FLAT ARRAYS and filters by each entry's own
  // `divisor_object` tag (using the exact literal tokens spec Sec.4.1 already
  // uses for the native sub-schema: `ramification_divisor_on_C_ref` /
  // `branch_divisor_on_P1_ref`), instead of indexing into an invented
  // per-locus sub-object. A field that is missing or not an array is treated
  // as an EMPTY array (never crashes, never silently matches some other
  // default) -- which resolves to ABSENT downstream, never a vacuous PASS
  // (裁定 127 item 3: fail-open removal).
  function filterByObject(field, tag) {
    if (!Array.isArray(field)) return [];
    return field.filter((e) => e && e.divisor_object === tag);
  }

  function objVerify(tag) {
    const coverageEntries = filterByObject(certificate.total_coverage_and_no_extra_component_witness, tag);
    return verifyObject({
      bijection: filterByObject(certificate.component_bijection, tag),
      exactWitnesses: filterByObject(certificate.exact_point_equality_witnesses, tag),
      distinctness: filterByObject(certificate.distinctness_witnesses, tag),
      multiplicityEqualities: filterByObject(certificate.multiplicity_equalities, tag),
      chartOverlap: certificate.chart_overlap_witnesses, // single declared object, not per-tag (see file header note)
      coverage: coverageEntries.length === 1 ? coverageEntries[0] : undefined, // 0 or >1 entries -> ABSENT, not a guess
      pushforward: certificate.pushforward_compatibility_witness,
    }, (searcherNativeBlob[tag] && searcherNativeBlob[tag].components) || [], (checkerNativeBlob[tag] && checkerNativeBlob[tag].components) || []);
  }

  const DIVISOR_OBJECT_RAM = 'ramification_divisor_on_C_ref';
  const DIVISOR_OBJECT_BRANCH = 'branch_divisor_on_P1_ref';
  const R_ram = objVerify(DIVISOR_OBJECT_RAM);
  const R_branch = objVerify(DIVISOR_OBJECT_BRANCH);

  // canonical per-witness result vector (contract Sec.3.4)
  const WITNESS_ORDER = ['W-1', 'W-2', "W-2'", 'W-3', 'W-4', 'W-5', 'W-6'];
  function vectorFor(R) { return WITNESS_ORDER.map((k) => [k, R[k]]); }
  const R_A = { ramification_divisor_on_C: vectorFor(R_ram), branch_divisor_on_P1: vectorFor(R_branch) };

  const allPass = (R) => WITNESS_ORDER.every((k) => R[k] === 'PASS');
  const p0p1Ok = ambient.pass; // P-0.* bundled; P-1.* folded into W-2 recheck above
  const overall_verdict_A = (p0p1Ok && p31 && p33 && allPass(R_ram) && allPass(R_branch)) ? 'PASS' : 'FAIL';

  const result_digest_A = digestOf({
    contract_id: 'mb/ninfty-verifier-contract/v13',
    contract_digest: 'e41d51dbdbdcf66efaff2ccd073bbfba9bff12bbfff435ca290a4248abcf5022',
    certificate_digest: certificate.certificate_digest,
    searcher_native_artifact_digest: certificate.searcher_native.native_artifact_digest,
    checker_native_artifact_digest: certificate.checker_native.native_artifact_digest,
    R_A, overall_verdict_A,
  });

  return {
    ambient_ok: ambient.pass, ambient_missing: ambient.missing,
    p31_ok: p31, p33_ok: p33,
    R_A, overall_verdict_A, result_digest_A,
  };
}

// --- verdict state machine: two-axis routing + combination (governing spec
// Sec.5.3 / Sec.5.3.3, contract Sec.5.1) ------------------------------------

// R_A/R_B: { ramification_divisor_on_C: [[witness,result],...], branch_divisor_on_P1: [...] }
export function vectorsEqual(R_A, R_B) {
  function eqList(a, b) {
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) if (a[i][0] !== b[i][0] || a[i][1] !== b[i][1]) return false;
    return true;
  }
  return eqList(R_A.ramification_divisor_on_C, R_B.ramification_divisor_on_C) &&
         eqList(R_A.branch_divisor_on_P1, R_B.branch_divisor_on_P1);
}

function vectorHasFailure(R) {
  const flat = [...R.ramification_divisor_on_C, ...R.branch_divisor_on_P1];
  return flat.some(([, v]) => v === 'FAIL' || v === 'ABSENT');
}

const INTEGRITY_PRIORITY = [
  'sealed-field-leak', 'deterministic-digest-exposed', 'shared-helper-detected',
  'digest-mismatch', 'pell-implies-coprime-mismatch', 'divisor-identity',
  'pell-derivative-mismatch', 'chart-degree-mismatch', 'p-locus-unhandled',
  'weierstrass-unhandled', 'infinity-unhandled', 'rh-mismatch', 'extra-branch-value',
  'finite-branch-count-mismatch', 'branch-pair-not-harmonic', 'finite-partition-cross-mismatch',
  'divisor-equality-failure', 'verifier-result-mismatch',
];
function sortIntegrity(codes) {
  const uniq = [...new Set(codes)];
  return uniq.sort((x, y) => INTEGRITY_PRIORITY.indexOf(x) - INTEGRITY_PRIORITY.indexOf(y));
}

// combine(): implements governing spec Sec.5.3 + Sec.5.3.3 exactly.
//  - S1 (envelope) and S2 (native cross-check) reasons are supplied by the
//    caller as `semanticS1S2Reasons` (this lane's evaluateDecisionLane's
//    integrity codes belong here for [13]/[15]; codes [9]-[12]/[14]/[16]-[24]
//    beyond that are UNKNOWN in this lane's scope and must be supplied
//    externally if computed, else omitted -- omission is NOT the same as
//    "checked and passed").
//  - R_A, R_B are canonical per-witness result vectors from the two verifiers.
//  - rejectReasons (R, the 8-code reject set) is supplied by the decision lane.
export function combine({ semanticS1S2Reasons = [], rejectReasons = [], R_A, R_B, inputDigestsMatch = true }) {
  const semantic = new Set(semanticS1S2Reasons);
  const concordance = new Set();

  if (!inputDigestsMatch) {
    // R-3 / Y-3: RA vs RB comparison is only meaningful when input digests match.
    semantic.add('digest-mismatch');
  } else if (R_A && R_B) {
    if (!vectorsEqual(R_A, R_B)) {
      concordance.add('verifier-result-mismatch'); // [26]
    } else {
      // X-2: [25] only once S2 native reasons are empty AND R_A=R_B has a failure.
      const s2NativeEmpty = ![...semantic].some((c) => INTEGRITY_PRIORITY.indexOf(c) >= INTEGRITY_PRIORITY.indexOf('divisor-identity') && INTEGRITY_PRIORITY.indexOf(c) <= INTEGRITY_PRIORITY.indexOf('finite-partition-cross-mismatch'));
      if (s2NativeEmpty && vectorHasFailure(R_A)) {
        semantic.add('divisor-equality-failure'); // [25]
      }
    }
  }

  const I = new Set([...semantic, ...concordance]);
  const R = new Set(rejectReasons);

  let verdict, primary, all_reason_codes, secondary_reason_codes;
  if (I.size > 0) {
    verdict = 'INTEGRITY_STOP';
    const sorted = sortIntegrity([...I]);
    primary = sorted[0];
    all_reason_codes = sortIntegrity([...I, ...R]);
    // invariant 2: public secondary = canonical_sort( ({[26]} ∩ I) - {primary} )
    secondary_reason_codes = sortIntegrity([...I].filter((c) => c === 'verifier-result-mismatch' && c !== primary));
  } else if (R.size > 0) {
    const REJECT_PRIORITY_LOCAL = [
      'precondition/degree-mismatch', 'precondition/f6-not-monic', 'precondition/curve-not-squarefree',
      'precondition/leading-coeff-mismatch', 'precondition/pell-violation', 'precondition/divisor-orientation',
      'triple-root-of-a', 'a-partition-mismatch',
    ];
    verdict = 'REJECT';
    primary = [...R].sort((x, y) => REJECT_PRIORITY_LOCAL.indexOf(x) - REJECT_PRIORITY_LOCAL.indexOf(y))[0];
    all_reason_codes = [...R].sort((x, y) => REJECT_PRIORITY_LOCAL.indexOf(x) - REJECT_PRIORITY_LOCAL.indexOf(y));
    secondary_reason_codes = [];
  } else {
    verdict = 'ACCEPT';
    primary = 'accepted';
    all_reason_codes = ['accepted'];
    secondary_reason_codes = [];
  }

  return { verdict, primary_reason_code: primary, secondary_reason_codes, all_reason_codes };
}
