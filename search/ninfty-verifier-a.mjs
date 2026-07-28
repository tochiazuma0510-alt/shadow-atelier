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

// --- 裁定 139 item 3: _ref = {artifact_id, digest, object_id, inline?} ------
//
// Structural malformation (not a triple at all) is reported as `malformed`
// (裁定 139 item 4: MALFORMED != ABSENT -- fail-closed, never coerced).
// A present `inline` whose digest disagrees with the declared `digest` is a
// SEPARATE, pre-existing condition: existing code [12] digest-mismatch
// (v3 Sec.5: "digest/inline 不一致のみ既存 [12]" -- neither side is silently
// preferred).
//
// 裁定 142 fix: v3 条項 3 explicitly allows EITHER `object_id` OR
// `json_pointer` as the third triple component ("json_pointer または
// object_id") -- the prior implementation only accepted `object_id`,
// rejecting every legitimate json_pointer-form ref as malformed. That was the
// root cause of the reverse cross-check's 6/6 FAIL (lane B's _ref values all
// use json_pointer). Fixed: a json_pointer is resolved via the simple RFC 6901
// algorithm against the certificate's OWN root document ("payload 内 pointer
// の解決で足りる" -- no external artifact store is required or assumed for
// this lane's scope). If the pointer resolves, its digest is checked against
// `ref.digest` (this gives the pointer path the same identity guarantee an
// `inline` copy gives the object_id path) -- disagreement is the SAME
// existing-[12] digestMismatch condition, not malformed. If the pointer does
// not resolve within the payload at all, that IS a structural failure
// (malformed, reason 'json-pointer-unresolvable') -- distinct from a value
// that resolves but merely has the wrong digest.
export function resolveJsonPointer(root, pointer) {
  if (pointer === '') return { found: true, value: root };
  if (typeof pointer !== 'string' || pointer[0] !== '/') return { found: false };
  const parts = pointer.split('/').slice(1).map((p) => p.replace(/~1/g, '/').replace(/~0/g, '~'));
  let cur = root;
  for (const p of parts) {
    if (cur === undefined || cur === null || typeof cur !== 'object') return { found: false };
    if (!Object.prototype.hasOwnProperty.call(cur, p)) return { found: false };
    cur = cur[p];
  }
  return { found: true, value: cur };
}

// 裁定150 items 2/3 (sol/裁定_150_EPv6.md): a json_pointer that fails to
// resolve against `rootDoc` is NOT immediately malformed if the ref ALSO
// carries a digest-consistent `inline` -- it falls back to `inline` (item
// 2), exactly like the pre-existing inline-without-pointer path (a digest
// MISMATCH on that inline is still the established [12] digestMismatch
// condition, not malformed -- "digest 不一致は従来どおり [12]"). Only when
// the pointer is unresolvable AND no `inline` exists at all does this stay
// a fail-closed MALFORMED ('json-pointer-unresolvable', item 3 -- never
// silently coerced into a vacuous pass). When the pointer DOES resolve,
// the pre-existing priority is unchanged: `inline` (if present) is still
// preferred over the pointer-resolved value for the digest check (裁定142
// behavior, not altered by 裁定150).
export function resolveRef(ref, rootDoc) {
  if (!ref || typeof ref !== 'object' || typeof ref.artifact_id !== 'string' || typeof ref.digest !== 'string') {
    return { malformed: true, reason: 'ref-not-a-triple' };
  }
  const hasObjectId = typeof ref.object_id === 'string';
  const hasJsonPointer = typeof ref.json_pointer === 'string';
  if (!hasObjectId && !hasJsonPointer) {
    return { malformed: true, reason: 'ref-not-a-triple' }; // neither valid third component present
  }
  const hasInline = Object.prototype.hasOwnProperty.call(ref, 'inline');

  let pointerFound = false, pointerResolved;
  if (hasJsonPointer) {
    const res = resolveJsonPointer(rootDoc, ref.json_pointer);
    if (res.found) { pointerFound = true; pointerResolved = res.value; }
  }

  if (hasJsonPointer && !pointerFound) {
    // 裁定150 item 2: unresolvable pointer -> fall back to inline (if any).
    if (hasInline) {
      const recomputed = digestOf(ref.inline);
      if (recomputed !== ref.digest) return { malformed: false, digestMismatch: true, data: ref.inline };
      return { malformed: false, digestMismatch: false, data: ref.inline };
    }
    // 裁定150 item 3: neither the pointer nor a fallback inline resolves ->
    // fail-closed MALFORMED, never coerced into ABSENT/PASS.
    return { malformed: true, reason: 'json-pointer-unresolvable' };
  }

  if (hasInline) {
    const recomputed = digestOf(ref.inline);
    if (recomputed !== ref.digest) return { malformed: false, digestMismatch: true, data: ref.inline };
    return { malformed: false, digestMismatch: false, data: ref.inline };
  }
  if (hasJsonPointer) {
    const recomputed = digestOf(pointerResolved);
    if (recomputed !== ref.digest) return { malformed: false, digestMismatch: true, data: pointerResolved };
    return { malformed: false, digestMismatch: false, data: pointerResolved };
  }
  // object_id only, no inline: a pure external reference this lane's scope
  // cannot resolve (no artifact store) -- not malformed, just unresolvable data.
  return { malformed: false, digestMismatch: false, data: undefined };
}

// --- 裁定 139 item 1: W-6 pushforward -- native_side-tagged (searcher/checker),
// NOT divisor_object-tagged (that duplication is now forbidden by
// docs/notes/cert_shape_interpretation_v3.md 条項 2). Each of the 2 entries
// carries its own ramification_ref/branch_ref/map_ref/witness_ref (all _ref
// triples, resolved via resolveRef). The witness_ref's inline `points` list
// (if genuinely populated) is checked the same way as before; per-side result
// is ABSENT when the side has no real point data, FAIL on any inconsistency,
// PASS only when real per-point data all agrees. The two sides are combined
// into ONE overall W-6 verdict (FAIL beats ABSENT beats PASS), which this
// lane's R_A vector places in BOTH the ramification and branch slots (the
// certificate-level data is no longer per-divisor-object, but contract
// Sec.3.4's canonical vector shape still has one W-6 slot per object -- see
// this file's docstring on that pre-existing, still-unresolved distinction).
export function verifyPushforwardV3(field, rootDoc) {
  if (!Array.isArray(field)) return { result: 'ABSENT', malformed: [] };
  const malformed = [];
  function sideResult(side) {
    const entries = field.filter((e) => e && e.native_side === side);
    if (entries.length !== 1) return 'ABSENT'; // 0 or >1 -- not a guess, not malformed (tag itself was valid)
    const e = entries[0];
    const refs = ['ramification_ref', 'branch_ref', 'map_ref', 'witness_ref'].map((k) => ({ k, r: resolveRef(e[k], rootDoc) }));
    for (const { k, r } of refs) {
      if (r.malformed) { malformed.push({ field: 'pushforward_compatibility_witness.' + side + '.' + k, reason: r.reason }); return 'MALFORMED'; }
    }
    const digestMismatch = refs.some(({ r }) => r.digestMismatch);
    if (digestMismatch) return 'FAIL'; // existing [12] territory, surfaced as FAIL at this per-side level
    const witnessData = refs.find(({ k }) => k === 'witness_ref').r.data;
    if (!witnessData || !Array.isArray(witnessData.points) || witnessData.points.length === 0) return 'ABSENT';
    const allOk = witnessData.points.every((p) => p.match === true && p.ram_multiplicity === p.branch_multiplicity);
    return allOk ? 'PASS' : 'FAIL';
  }
  const s = sideResult('searcher');
  const c = sideResult('checker');
  if (malformed.length > 0) return { result: 'MALFORMED', malformed };
  const rank = { FAIL: 0, ABSENT: 1, PASS: 2 };
  const combined = [s, c].reduce((worst, r) => (rank[r] < rank[worst] ? r : worst), 'PASS');
  return { result: combined, malformed: [] };
}

// --- W-1..W-6 for one object (ramification_divisor_on_C / branch_divisor_on_P1)

// 裁定 139 item 2: component_bijection entries are EDGES naming both native
// digests + component_ids explicitly. The verifier does NOT trust this list
// as a self-declared domain/codomain -- it reconstructs the two REAL
// component-id sets from the native artifacts (searcherComponents /
// checkerComponents, already carrying component_id per ninfty-searcher-v2.mjs)
// and checks: (a) every edge's declared native digests match the ACTUAL
// native digests this verifier is holding, (b) every edge's component_id
// exists in the corresponding real set, (c) no component_id is used twice on
// either side (in-degree = out-degree = 1 for every vertex the edge list
// touches). This is exactly "受領側が native artifact から両成分集合を再構成し、
// 各頂点の入次数・出次数 = 1 を検査する" (v3 条項 6).
function verifyComponentBijectionEdges(edges, searcherComponents, checkerComponents, expectedSearcherDigest, expectedCheckerDigest) {
  if (!edges || edges.length === 0) return 'ABSENT';
  const sIds = new Set(searcherComponents.map((c) => c.component_id));
  const cIds = new Set(checkerComponents.map((c) => c.component_id));
  const seenS = new Map(), seenC = new Map();
  for (const e of edges) {
    if (e.searcher_native_digest !== expectedSearcherDigest || e.checker_native_digest !== expectedCheckerDigest) return 'FAIL';
    if (!sIds.has(e.searcher_component_id) || !cIds.has(e.checker_component_id)) return 'FAIL';
    seenS.set(e.searcher_component_id, (seenS.get(e.searcher_component_id) || 0) + 1);
    seenC.set(e.checker_component_id, (seenC.get(e.checker_component_id) || 0) + 1);
  }
  for (const v of seenS.values()) if (v !== 1) return 'FAIL';
  for (const v of seenC.values()) if (v !== 1) return 'FAIL';
  return 'PASS';
}

function verifyObject(certObj, searcherComponents, checkerComponents) {
  const R = {}; // per-witness result: PASS / FAIL / ABSENT

  // W-1: edge-form bijection re-check (裁定 139 item 2, see function above).
  R['W-1'] = verifyComponentBijectionEdges(certObj.bijection, searcherComponents, checkerComponents, certObj.expectedSearcherDigest, certObj.expectedCheckerDigest);

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

  // W-4 (裁定 115 item 2, v3 条項 7 -- unchanged): structured chart-atlas /
  // per-overlap re-check, divisor_object-keyed 1 entry, per_overlap_witnesses[]
  // carries the layering. status='ABSENT' is read literally as ABSENT.
  R['W-4'] = verifyChartOverlap(certObj.chartOverlap);

  // W-5: coverage / no extra
  const cov = certObj.coverage;
  R['W-5'] = cov ? (cov.no_extra === true ? 'PASS' : 'FAIL') : 'ABSENT';

  // W-6 (裁定 139 item 1): no longer computed per divisor_object -- caller
  // passes in the single, already-combined native_side-based verdict
  // (verifyPushforwardV3), duplicated into both R vectors' W-6 slot.
  R['W-6'] = certObj.pushforwardResult;

  return R;
}

// --- 裁定 139 item 4: MALFORMED != ABSENT (v3 条項 5) ------------------------
//
// A field that is `undefined` (missing) or explicit `[]` is ABSENT-eligible
// (evidence simply not present). A field that is `null`, not an array, or an
// array containing an entry with a missing/unknown tag is MALFORMED -- a
// schema/contract violation, reported as a fail-closed STOP (provisional
// reason code `schema-invalid`, per v3 Sec.5 pending a dedicated enum from
// Sol), never silently coerced into an empty array.
const VALID_DIVISOR_OBJECTS = ['ramification_divisor_on_C_ref', 'branch_divisor_on_P1_ref'];
const VALID_NATIVE_SIDES = ['searcher', 'checker'];

function classifyTaggedArrayField(field, tagKey, validTags) {
  if (field === undefined) return { status: 'empty' };
  if (field === null) return { status: 'malformed', reason: 'null' };
  if (!Array.isArray(field)) return { status: 'malformed', reason: 'not-an-array' };
  if (field.length === 0) return { status: 'empty' };
  for (const e of field) {
    if (!e || typeof e !== 'object') return { status: 'malformed', reason: 'entry-not-an-object' };
    if (!Object.prototype.hasOwnProperty.call(e, tagKey)) return { status: 'malformed', reason: 'missing-tag:' + tagKey };
    if (!validTags.includes(e[tagKey])) return { status: 'malformed', reason: 'unknown-tag-value:' + String(e[tagKey]) };
  }
  return { status: 'ok' };
}

const SHAPE_CHECKS = [
  ['component_bijection', 'divisor_object', VALID_DIVISOR_OBJECTS],
  ['exact_point_equality_witnesses', 'divisor_object', VALID_DIVISOR_OBJECTS],
  ['distinctness_witnesses', 'divisor_object', VALID_DIVISOR_OBJECTS],
  ['multiplicity_equalities', 'divisor_object', VALID_DIVISOR_OBJECTS],
  ['chart_overlap_witnesses', 'divisor_object', VALID_DIVISOR_OBJECTS],
  ['total_coverage_and_no_extra_component_witness', 'divisor_object', VALID_DIVISOR_OBJECTS],
  ['pushforward_compatibility_witness', 'native_side', VALID_NATIVE_SIDES],
];

// 裁定150 item 1 (sol/裁定_150_EPv6.md): a _ref triple's `json_pointer`
// resolves WITHIN THE ARTIFACT `artifact_id` NAMES, never within the
// certificate itself -- for searcher_native/checker_native's
// ramification_divisor_on_C_ref / branch_divisor_on_P1_ref, that artifact
// is the caller-supplied native artifact (EP runner's native_a/native_b,
// or this file's own searcherNativeBlob/checkerNativeBlob params -- same
// role). Using `certificate` as rootDoc here was the root cause of the
// reverse cross-check's spurious json-pointer-unresolvable MALFORMED (a
// pointer like "/ramification_divisor_on_C_ref" simply does not exist at
// the certificate's own top level). Backward-compatible: the two new
// params default to `certificate` (the old rootDoc) so any caller that
// still only supplies one argument keeps its previous behavior exactly.
export function validateCertificateShapeV3(certificate, searcherNativeArtifact = certificate, checkerNativeArtifact = certificate) {
  const malformed = [];
  for (const [fieldName, tagKey, validTags] of SHAPE_CHECKS) {
    const c = classifyTaggedArrayField(certificate[fieldName], tagKey, validTags);
    if (c.status === 'malformed') malformed.push({ field: fieldName, reason: c.reason });
  }
  const NATIVE_ROOT_DOC = { searcher_native: searcherNativeArtifact, checker_native: checkerNativeArtifact };
  for (const nativeField of ['searcher_native', 'checker_native']) {
    for (const refField of ['ramification_divisor_on_C_ref', 'branch_divisor_on_P1_ref']) {
      const r = resolveRef(certificate[nativeField] && certificate[nativeField][refField], NATIVE_ROOT_DOC[nativeField]);
      if (r.malformed) malformed.push({ field: nativeField + '.' + refField, reason: r.reason });
    }
  }
  return malformed;
}

// --- top-level contract Sec.3 procedure -------------------------------------

// input: { certificate, searcherNativeBlob, checkerNativeBlob }
// searcherNativeBlob/checkerNativeBlob are the ACTUAL blobs verifier A read
// (for P-3.3 digest re-check against the certificate's declared digests).
export function runVerifierA({ certificate, searcherNativeBlob, checkerNativeBlob }) {
  // 裁定 139 item 4: fail-closed schema/shape validation FIRST, before any
  // witness logic runs. A malformed certificate never reaches PASS/FAIL/ABSENT
  // scoring -- it stops here with a distinct result shape.
  const shapeMalformed = validateCertificateShapeV3(certificate, searcherNativeBlob, checkerNativeBlob);
  if (shapeMalformed.length > 0) {
    return {
      malformed: true,
      malformed_fields: shapeMalformed,
      provisional_reason_code: 'schema-invalid', // v3 Sec.5: dedicated enum pending Sol
      overall_verdict_A: 'FAIL',
    };
  }

  const ambient = checkAmbient(certificate);

  // P-3.1 / P-3.2: predicate_spec_id/digest, schema_id/digest present & self-consistent.
  const p31 = certificate.predicate_spec_id === certificate.schema_id.split('#')[0] &&
              certificate.predicate_spec_digest === certificate.schema_digest;

  // P-3.3 (裁定 139 item 3): _ref triples resolved via resolveRef (shape
  // already validated above, so these calls cannot return malformed here).
  // An inline/digest mismatch is the EXISTING [12] condition, folded into p33.
  // 裁定150 item 1: rootDoc = the caller-supplied native artifact
  // (searcherNativeBlob/checkerNativeBlob), NOT `certificate` -- a
  // json_pointer inside searcher_native/checker_native resolves within the
  // artifact_id-named native artifact, never within the certificate itself.
  const searcherRam = resolveRef(certificate.searcher_native.ramification_divisor_on_C_ref, searcherNativeBlob);
  const searcherBranch = resolveRef(certificate.searcher_native.branch_divisor_on_P1_ref, searcherNativeBlob);
  const checkerRam = resolveRef(certificate.checker_native.ramification_divisor_on_C_ref, checkerNativeBlob);
  const checkerBranch = resolveRef(certificate.checker_native.branch_divisor_on_P1_ref, checkerNativeBlob);
  const refInlineDigestOk = ![searcherRam, searcherBranch, checkerRam, checkerBranch].some((r) => r.digestMismatch);

  const searcherDigestOk = digestOf({
    ramification_divisor_on_C_ref: searcherNativeBlob.ramification_divisor_on_C_ref,
    branch_divisor_on_P1_ref: searcherNativeBlob.branch_divisor_on_P1_ref,
  }) === certificate.searcher_native.native_artifact_digest;
  const checkerDigestOk = digestOf({
    ramification_divisor_on_C_ref: checkerNativeBlob.ramification_divisor_on_C_ref,
    branch_divisor_on_P1_ref: checkerNativeBlob.branch_divisor_on_P1_ref,
  }) === certificate.checker_native.native_artifact_digest;
  const p33 = searcherDigestOk && checkerDigestOk && refInlineDigestOk;

  // 裁定 127 (fields other than W-6): spec Sec.4.1's literal schema has no
  // object-keyed nesting for the witness-group fields -- flat arrays, filtered
  // by each entry's own `divisor_object` tag. A field that is missing or not
  // an array is treated as empty (shape-validated above; this is now only a
  // defensive fallback) -- resolves to ABSENT downstream, never a vacuous PASS.
  function filterByObject(field, tag) {
    if (!Array.isArray(field)) return [];
    return field.filter((e) => e && e.divisor_object === tag);
  }

  // 裁定 139 item 1: W-6 is native_side-tagged, NOT divisor_object-tagged --
  // computed ONCE (not per divisor object) and duplicated into both R vectors.
  const pushforward = verifyPushforwardV3(certificate.pushforward_compatibility_witness, certificate);
  if (pushforward.result === 'MALFORMED') {
    return {
      malformed: true,
      malformed_fields: pushforward.malformed,
      provisional_reason_code: 'schema-invalid',
      overall_verdict_A: 'FAIL',
    };
  }

  function objVerify(tag, expectedSearcherDigest, expectedCheckerDigest) {
    const coverageEntries = filterByObject(certificate.total_coverage_and_no_extra_component_witness, tag);
    return verifyObject({
      bijection: filterByObject(certificate.component_bijection, tag),
      expectedSearcherDigest, expectedCheckerDigest,
      exactWitnesses: filterByObject(certificate.exact_point_equality_witnesses, tag),
      distinctness: filterByObject(certificate.distinctness_witnesses, tag),
      multiplicityEqualities: filterByObject(certificate.multiplicity_equalities, tag),
      // W-4 (v3 条項 7, unchanged from 裁定 133): divisor_object-keyed 1 entry.
      chartOverlap: (() => { const e = filterByObject(certificate.chart_overlap_witnesses, tag); return e.length === 1 ? e[0] : undefined; })(),
      coverage: coverageEntries.length === 1 ? coverageEntries[0] : undefined, // 0 or >1 entries -> ABSENT, not a guess
      pushforwardResult: pushforward.result, // shared W-6 verdict (裁定 139 item 1)
    }, (searcherNativeBlob[tag] && searcherNativeBlob[tag].components) || [], (checkerNativeBlob[tag] && checkerNativeBlob[tag].components) || []);
  }

  const DIVISOR_OBJECT_RAM = 'ramification_divisor_on_C_ref';
  const DIVISOR_OBJECT_BRANCH = 'branch_divisor_on_P1_ref';
  const R_ram = objVerify(DIVISOR_OBJECT_RAM, certificate.searcher_native.native_artifact_digest, certificate.checker_native.native_artifact_digest);
  const R_branch = objVerify(DIVISOR_OBJECT_BRANCH, certificate.searcher_native.native_artifact_digest, certificate.checker_native.native_artifact_digest);

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
    malformed: false,
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
