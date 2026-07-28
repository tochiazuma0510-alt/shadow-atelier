// search/ninfty-selftest-lanea.mjs
//
// Lane A self-test harness: decision-lane predicate fixtures (E-1..E-6/T-1)
// + certificate/verifier-A fixtures (INTEGRITY_STOP codes + two-axis
// routing). Run via: node search/ninfty-selftest-lanea.mjs
//
// PARTIAL PREDICATE / UNKNOWN NOTICE: this exercises lane A only. Any R_B /
// checker_native used below is an EXPLICIT MOCK for unit-testing the state
// machine, never real lane-B (python) output.

import {
  evaluateDecisionLane, checkT1, buildSearcherNative, generateCertificate,
  loadFreezeReceiptDigests, DEFAULT_FREEZE_RECEIPT_PATH, digestOf,
} from './ninfty-searcher-v2.mjs';
import { runVerifierA, combine, vectorsEqual, verifyChartOverlap_forTest, classifyChartOverlapEntry_forTest } from './ninfty-verifier-a.mjs';

// Test-only ref-triple builder (裁定 139 item 3 shape: {artifact_id, digest,
// object_id, inline}), used only to construct SYNTHETIC fixture data below --
// not part of the frozen generator/verifier logic.
function makeTestRef(objectId, inlineData) {
  return { artifact_id: 'test-inline/' + objectId, digest: digestOf(inlineData), object_id: objectId, inline: inlineData };
}
import {
  decisionLaneFixtures, t1IsolatedTripleRoot, positive1,
} from './certs/fixtures-lanea.mjs';

let failures = 0;
let total = 0;

function check(label, cond, detail) {
  total++;
  if (cond) {
    console.log(`PASS  ${label}`);
  } else {
    failures++;
    console.log(`FAIL  ${label}${detail ? '  -- ' + detail : ''}`);
  }
}

console.log('=== decision-lane fixtures (evaluateDecisionLane) ===');
for (const fx of decisionLaneFixtures) {
  const result = evaluateDecisionLane(fx.candidate);
  const okVerdict = result.verdict === fx.expect.verdict;
  const okPrimary = result.primary_reason_code === fx.expect.primary_reason_code;
  check(
    `${fx.label}: verdict=${result.verdict} primary=${result.primary_reason_code}`,
    okVerdict && okPrimary,
    `expected verdict=${fx.expect.verdict} primary=${fx.expect.primary_reason_code}`,
  );
}

console.log('\n=== isolated T-1 fixture (checkT1) ===');
{
  const r = checkT1(t1IsolatedTripleRoot.aCoeffs);
  check(
    `${t1IsolatedTripleRoot.label}: ok=${r.ok} code=${r.code}`,
    r.ok === t1IsolatedTripleRoot.expect.ok && r.code === t1IsolatedTripleRoot.expect.code,
    `expected ok=${t1IsolatedTripleRoot.expect.ok} code=${t1IsolatedTripleRoot.expect.code} (dDeg=${r.dDeg}, dSquarefree=${r.dSquarefree}, tripleDeg=${r.tripleDeg})`,
  );
}

// ---------------------------------------------------------------------------
// Certificate / verifier-A fixtures
// ---------------------------------------------------------------------------

console.log('\n=== 裁定 115 item 1: certificate pin sourced from freeze receipt ===');
{
  const receipt = loadFreezeReceiptDigests();
  const native = buildSearcherNative(positive1.candidate);
  const cert = generateCertificate({
    candidateRef: 'lanea-cert-pin-check',
    searcherNative: native,
    checkerNative: native,
    // predicateSpecId/predicateSpecDigest DELIBERATELY OMITTED: defaults must
    // come from provenance/ninfty_freeze_receipt_sol75.md (machine-parsed),
    // never a hand-typed literal.
  });
  check(
    `cert.predicate_spec_id === receipt (${DEFAULT_FREEZE_RECEIPT_PATH})`,
    cert.predicate_spec_id === receipt.predicate_spec_id,
    `cert=${cert.predicate_spec_id} receipt=${receipt.predicate_spec_id}`,
  );
  check(
    'cert.predicate_spec_digest === receipt.predicate_spec_digest (exact 64-hex)',
    cert.predicate_spec_digest === receipt.predicate_spec_digest,
    `cert=${cert.predicate_spec_digest} receipt=${receipt.predicate_spec_digest}`,
  );
  check('cert.schema_digest === predicate_spec_digest (internal anchor, spec Sec.6)', cert.schema_digest === receipt.predicate_spec_digest);
  console.log('  sample cert pin: predicate_spec_id=' + cert.predicate_spec_id + ' predicate_spec_digest=' + cert.predicate_spec_digest);
}

console.log('\n=== certificate / verifier-A fixtures ===');

// --- Fixture C1: certificate exactly as lane A's native scope actually
//     produces it (searcher_native == checker_native MOCK for the
//     concordance-agreement case). 裁定 115 item 2: W-4/W-6 are now
//     STRUCTURED ABSENT (this lane declares one chart and no explicit
//     points), so overall_verdict_A is honestly FAIL and combine() routes to
//     divisor-equality-failure [25] -- NOT a false ACCEPT. This is the
//     correct EP-pre posture: lane A alone cannot certify full witness
//     completeness yet.
{
  const native = buildSearcherNative(positive1.candidate);
  const cert = generateCertificate({
    candidateRef: 'lanea-cert-fixture-c1',
    searcherNative: native,
    checkerNative: native, // MOCK: stands in for an independent lane-B native artifact that happens to agree exactly
  });
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  const vB_mock = vA; // MOCK: identical R_B for the concordance-agreement case
  const combined = combine({ semanticS1S2Reasons: [], rejectReasons: [], R_A: vA.R_A, R_B: vB_mock.R_A });
  check('C1 W-4=ABSENT (structured, not PASS)', vA.R_A.ramification_divisor_on_C.find(([k]) => k === 'W-4')[1] === 'ABSENT', JSON.stringify(vA.R_A.ramification_divisor_on_C));
  check('C1 W-6=ABSENT (structured, not PASS)', vA.R_A.ramification_divisor_on_C.find(([k]) => k === 'W-6')[1] === 'ABSENT', JSON.stringify(vA.R_A.ramification_divisor_on_C));
  check('C1 honest-incomplete: overall_verdict_A=FAIL (W-4/W-6 ABSENT, not PASS)', vA.overall_verdict_A === 'FAIL', JSON.stringify(vA.R_A));
  check('C1 honest-incomplete: combine -> INTEGRITY_STOP/[25] (not a false ACCEPT)', combined.verdict === 'INTEGRITY_STOP' && combined.primary_reason_code === 'divisor-equality-failure', JSON.stringify(combined));
}

// --- Fixture C1b: SYNTHETIC/HYPOTHETICAL -- confirms the W-4/W-6 re-check
//     logic itself reaches PASS/ACCEPT when genuine (non-ABSENT) chart-overlap
//     and point-level data ARE supplied. This is NOT lane A's actual native
//     scope (this lane never produces a second chart or explicit points); it
//     is a regression test of runVerifierA's re-check code path only.
{
  const native = buildSearcherNative(positive1.candidate);
  const cert = generateCertificate({
    candidateRef: 'lanea-cert-fixture-c1b-synthetic',
    searcherNative: native,
    checkerNative: native,
  });
  // Inject SYNTHETIC genuine chart-overlap data: a second hypothetical chart
  // whose ideal generator for the a-pair-locus component is identical to the
  // first chart's (so mutual reduction-to-zero holds both ways).
  // 裁定 133: both fields are FLAT arrays with one entry per divisor_object
  // (docs/notes/cert_shape_interpretation_v2.md (i)); field renamed +
  // status vocabulary made strict by 裁定152 §3-1 / 追補(n) v2 (sharpened
  // 裁定177 F80-4.1): {status: "PRESENT", entries: [...]} is now the ONLY
  // shape verifyChartOverlap accepts for a genuine PASS/FAIL re-check --
  // the old `status: "PASS"` + `per_overlap_witnesses` shape is now
  // MALFORMED (retired).
  const ramGen = native.ramification_divisor_on_C_ref.components[0].ideal_generator;
  function syntheticChartOverlapEntry(tag) {
    return {
      divisor_object: tag,
      status: 'PRESENT',
      entries: [{ chart_pair: ['x-chart-single', 'x-chart-hypothetical-2'], agree: true, generator_chart_a: ramGen, generator_chart_b: ramGen }],
      reason: 'SYNTHETIC for regression testing only -- not lane A native scope',
    };
  }
  // 裁定 139 item 1: pushforward_compatibility_witness is now native_side-tagged
  // (searcher/checker), NOT divisor_object-tagged -- 2 entries total, each
  // {native_side, ramification_ref, branch_ref, map_ref, witness_ref} (all
  // _ref triples per item 3).
  function syntheticPushforwardEntry(side) {
    return {
      native_side: side,
      ramification_ref: makeTestRef(side + '-synthetic-ram', native.ramification_divisor_on_C_ref),
      branch_ref: makeTestRef(side + '-synthetic-branch', native.branch_divisor_on_P1_ref),
      map_ref: makeTestRef(side + '-synthetic-map', { description: 'SYNTHETIC identity map' }),
      witness_ref: makeTestRef(side + '-synthetic-witness', {
        points: [{ point_ref: 'synthetic-point-1', ram_multiplicity: 1, branch_multiplicity: 1, match: true }],
      }),
    };
  }
  cert.chart_overlap_witnesses = [
    syntheticChartOverlapEntry('ramification_divisor_on_C_ref'),
    syntheticChartOverlapEntry('branch_divisor_on_P1_ref'),
  ];
  cert.pushforward_compatibility_witness = [
    syntheticPushforwardEntry('searcher'),
    syntheticPushforwardEntry('checker'),
  ];
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  const combined = combine({ semanticS1S2Reasons: [], rejectReasons: [], R_A: vA.R_A, R_B: vA.R_A });
  check('C1b synthetic: W-4=PASS, W-6=PASS', vA.R_A.ramification_divisor_on_C.find(([k]) => k === 'W-4')[1] === 'PASS' && vA.R_A.ramification_divisor_on_C.find(([k]) => k === 'W-6')[1] === 'PASS', JSON.stringify(vA.R_A));
  check('C1b synthetic: overall_verdict_A=PASS', vA.overall_verdict_A === 'PASS', JSON.stringify(vA.R_A));
  check('C1b synthetic: combine -> ACCEPT', combined.verdict === 'ACCEPT' && combined.primary_reason_code === 'accepted', JSON.stringify(combined));
}

// --- Fixture C2: digest-mismatch [12] -- certificate declares a wrong
//     native_artifact_digest for searcher_native.
{
  const native = buildSearcherNative(positive1.candidate);
  const cert = generateCertificate({
    candidateRef: 'lanea-cert-fixture-c2',
    searcherNative: native,
    checkerNative: native,
  });
  cert.searcher_native.native_artifact_digest = '0'.repeat(64); // corrupt
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C2 digest-mismatch: p33_ok=false', vA.p33_ok === false, JSON.stringify(vA));
  // Caller-level routing: a P-3.3 failure feeds [12] into the semantic set externally.
  const combined = combine({ semanticS1S2Reasons: vA.p33_ok ? [] : ['digest-mismatch'], rejectReasons: [], R_A: vA.R_A, R_B: vA.R_A });
  check('C2 digest-mismatch: combine -> INTEGRITY_STOP/[digest-mismatch]', combined.verdict === 'INTEGRITY_STOP' && combined.primary_reason_code === 'digest-mismatch', JSON.stringify(combined));
}

// --- Fixture C3: divisor-equality-failure [25] -- one ideal-equality witness
//     is broken (wrong divisor claimed), R_A itself contains a FAIL, and
//     R_B is mocked identical (both verifiers "agree" it fails).
{
  const native = buildSearcherNative(positive1.candidate);
  const cert = generateCertificate({
    candidateRef: 'lanea-cert-fixture-c3',
    searcherNative: native,
    checkerNative: native,
  });
  // Corrupt the first ideal-equality witness's forward divisor so reduction fails.
  // (裁定 127: exact_point_equality_witnesses is now a FLAT array of entries
  // tagged by divisor_object, per spec Sec.4.1's literal schema -- find the
  // first ramification-divisor entry rather than indexing a nested object.)
  const w = cert.exact_point_equality_witnesses.find((e) => e.divisor_object === 'ramification_divisor_on_C_ref').witness;
  w.forward.divisor_monic = ['1', '1']; // wrong monic divisor (x+1) unrelated to the real ideal
  w.forward.remainder = ['1']; // also mark a nonzero remainder for consistency of the fixture data
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C3 divisor-equality-failure: W-2 recomputes FAIL', vA.R_A.ramification_divisor_on_C.find(([k]) => k === 'W-2')[1] === 'FAIL', JSON.stringify(vA.R_A.ramification_divisor_on_C));
  const R_B_mock = vA.R_A; // MOCK: lane B verifier agrees (both see the same broken witness)
  const combined = combine({ semanticS1S2Reasons: [], rejectReasons: [], R_A: vA.R_A, R_B: R_B_mock });
  check('C3 divisor-equality-failure: combine -> INTEGRITY_STOP/[25]', combined.verdict === 'INTEGRITY_STOP' && combined.primary_reason_code === 'divisor-equality-failure', JSON.stringify(combined));
}

// --- Fixture C4: verifier-result-mismatch [26] -- R_B (MOCK) differs from
//     R_A even though the certificate itself is clean.
{
  const native = buildSearcherNative(positive1.candidate);
  const cert = generateCertificate({
    candidateRef: 'lanea-cert-fixture-c4',
    searcherNative: native,
    checkerNative: native,
  });
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  const R_B_mock = JSON.parse(JSON.stringify(vA.R_A));
  // MOCK disagreement: flip W-3 result for the branch object.
  const idx = R_B_mock.branch_divisor_on_P1.findIndex(([k]) => k === 'W-3');
  R_B_mock.branch_divisor_on_P1[idx] = ['W-3', 'FAIL'];
  check('C4 setup: vectorsEqual(R_A, R_B_mock) is false', vectorsEqual(vA.R_A, R_B_mock) === false);
  const combined = combine({ semanticS1S2Reasons: [], rejectReasons: [], R_A: vA.R_A, R_B: R_B_mock });
  check('C4 verifier-result-mismatch: combine -> INTEGRITY_STOP/[26]', combined.verdict === 'INTEGRITY_STOP' && combined.primary_reason_code === 'verifier-result-mismatch', JSON.stringify(combined));
}

// --- Fixture C5: [24]+[26] simultaneous -- MOCKED semantic S2 native
//     mismatch ('finite-partition-cross-mismatch', out of this lane's
//     computed scope, injected here purely to test invariant-2 secondary
//     code emission) co-occurring with a genuine R_A != R_B(mock).
{
  const native = buildSearcherNative(positive1.candidate);
  const cert = generateCertificate({
    candidateRef: 'lanea-cert-fixture-c5',
    searcherNative: native,
    checkerNative: native,
  });
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  const R_B_mock = JSON.parse(JSON.stringify(vA.R_A));
  const idx = R_B_mock.ramification_divisor_on_C.findIndex(([k]) => k === 'W-4');
  R_B_mock.ramification_divisor_on_C[idx] = ['W-4', 'FAIL'];
  const combined = combine({
    semanticS1S2Reasons: ['finite-partition-cross-mismatch'], // MOCK injection, see comment above
    rejectReasons: [], R_A: vA.R_A, R_B: R_B_mock,
  });
  check(
    'C5 [24]+[26]: primary=finite-partition-cross-mismatch, secondary=[verifier-result-mismatch]',
    combined.verdict === 'INTEGRITY_STOP'
      && combined.primary_reason_code === 'finite-partition-cross-mismatch'
      && JSON.stringify(combined.secondary_reason_codes) === JSON.stringify(['verifier-result-mismatch']),
    JSON.stringify(combined),
  );
}

// --- 裁定 139 item 4 (v3 条項 5): MALFORMED != ABSENT. Each fixture below
//     confirms a distinct malformation trigger yields runVerifierA's
//     fail-closed {malformed:true, ...} result, NEVER silently coerced to an
//     empty-array ABSENT reading.
console.log('\n=== 裁定 139 item 4: MALFORMED != ABSENT fixtures ===');

function freshCert() {
  const native = buildSearcherNative(positive1.candidate);
  return { native, cert: generateCertificate({ candidateRef: 'lanea-cert-malformed-fixture', searcherNative: native, checkerNative: native }) };
}

// C6: null field (not missing, not []) -> MALFORMED
{
  const { native, cert } = freshCert();
  cert.component_bijection = null;
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C6 null field -> malformed=true', vA.malformed === true && vA.malformed_fields.some((m) => m.field === 'component_bijection' && m.reason === 'null'), JSON.stringify(vA));
}

// C7: non-array field (an object instead of an array) -> MALFORMED
{
  const { native, cert } = freshCert();
  cert.exact_point_equality_witnesses = { oops: 'not an array' };
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C7 non-array field -> malformed=true', vA.malformed === true && vA.malformed_fields.some((m) => m.field === 'exact_point_equality_witnesses' && m.reason === 'not-an-array'), JSON.stringify(vA));
}

// C8: entry missing its tag key entirely -> MALFORMED
{
  const { native, cert } = freshCert();
  delete cert.multiplicity_equalities[0].divisor_object;
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C8 missing-tag entry -> malformed=true', vA.malformed === true && vA.malformed_fields.some((m) => m.field === 'multiplicity_equalities' && m.reason === 'missing-tag:divisor_object'), JSON.stringify(vA));
}

// C9: entry with an unknown tag VALUE -> MALFORMED
{
  const { native, cert } = freshCert();
  cert.distinctness_witnesses[0].divisor_object = 'some-made-up-object';
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C9 unknown-tag-value entry -> malformed=true', vA.malformed === true && vA.malformed_fields.some((m) => m.field === 'distinctness_witnesses' && m.reason.startsWith('unknown-tag-value')), JSON.stringify(vA));
}

// C10: pushforward_compatibility_witness entry with unknown native_side -> MALFORMED
{
  const { native, cert } = freshCert();
  cert.pushforward_compatibility_witness[0].native_side = 'nobody';
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C10 unknown native_side -> malformed=true', vA.malformed === true && vA.malformed_fields.some((m) => m.field === 'pushforward_compatibility_witness'), JSON.stringify(vA));
}

// C11 (control): explicit [] on a field is ABSENT-eligible, NOT malformed --
// confirms the empty-array case is still allowed through to normal scoring.
{
  const { native, cert } = freshCert();
  cert.distinctness_witnesses = [];
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C11 explicit [] -> malformed=false (ABSENT-eligible, not a schema violation)', vA.malformed === false, JSON.stringify(vA));
  check("C11 explicit [] -> W-2' reads ABSENT", vA.R_A.ramification_divisor_on_C.find(([k]) => k === "W-2'")[1] === 'ABSENT', JSON.stringify(vA.R_A));
}

// C12: native _ref not a triple at all (raw object, pre-裁定139 shape) -> MALFORMED
{
  const { native, cert } = freshCert();
  cert.searcher_native.ramification_divisor_on_C_ref = { components: [] }; // old-shape raw object, no artifact_id/digest/object_id
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C12 non-triple native _ref -> malformed=true', vA.malformed === true && vA.malformed_fields.some((m) => m.field === 'searcher_native.ramification_divisor_on_C_ref' && m.reason === 'ref-not-a-triple'), JSON.stringify(vA));
}

// C13: native _ref IS a well-formed triple, but inline disagrees with its own
// declared digest -> existing [12] digest-mismatch path (p33=false), NOT
// malformed (v3 Sec.5: "digest/inline 不一致のみ既存 [12]").
{
  const { native, cert } = freshCert();
  cert.searcher_native.ramification_divisor_on_C_ref.inline = { components: [{ locus_type: 'tampered', ideal_generator: ['1'], multiplicity: 1 }] };
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C13 ref inline/digest mismatch -> malformed=false, p33_ok=false (existing [12])', vA.malformed === false && vA.p33_ok === false, JSON.stringify(vA));
}

// --- 裁定 142: v3 条項 3 allows EITHER `object_id` OR `json_pointer` as the
//     _ref triple's third component -- lane B's refs all use json_pointer,
//     which the prior resolveRef rejected outright (root cause of the
//     reverse cross-check's 6/6 FAIL). These fixtures cover the json_pointer
//     path directly.
//
// 裁定150 (sol/裁定_150_EPv6.md item 1) UPDATE: a searcher_native/
// checker_native _ref's json_pointer resolves WITHIN THE NATIVE ARTIFACT
// (the caller-supplied searcherNativeBlob/checkerNativeBlob -- EP runner's
// native_a/native_b equivalent), NEVER within the certificate itself. C14/
// C16 below previously planted their pointer target on `cert._external_store`
// (the OLD, now-corrected rootDoc); they are updated here to plant it on
// `native` instead, matching the new (and, per 裁定150, the only ever
// correct) resolution root. C15/C17 are root-doc-independent and unchanged.
console.log('\n=== 裁定 142 / 裁定150: json_pointer _ref fixtures ===');

// C14 (positive): a json_pointer-only ref (no inline) resolving within the
// NATIVE ARTIFACT (searcherNativeBlob) to content whose digest matches the
// declared one (裁定150 item 1: root = native artifact, not certificate).
{
  const { native, cert } = freshCert();
  const content = { components: [{ locus_type: 'json-pointer-target', ideal_generator: ['1'], multiplicity: 1 }] };
  native._external_store = { searcherRam: content }; // native artifact location the pointer resolves against
  cert.searcher_native.ramification_divisor_on_C_ref = {
    artifact_id: 'test-json-pointer/searcher-ram',
    digest: digestOf(content),
    json_pointer: '/_external_store/searcherRam',
    // no `inline` key: resolution must come from the pointer alone
  };
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C14 json_pointer ref resolves (within native artifact) + digest matches -> malformed=false', vA.malformed === false, JSON.stringify(vA));
}

// C15 (negative, 裁定150 item 3 "両方不能"): json_pointer that does not
// resolve within the native artifact AND carries no `inline` to fall back
// on -> malformed ('json-pointer-unresolvable'), not silently ABSENT.
{
  const { native, cert } = freshCert();
  cert.searcher_native.ramification_divisor_on_C_ref = {
    artifact_id: 'test-json-pointer/dangling',
    digest: '0'.repeat(64),
    json_pointer: '/this/path/does/not/exist',
  };
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check(
    'C15 unresolvable json_pointer, no inline fallback -> malformed=true (json-pointer-unresolvable, 裁定150 item 3)',
    vA.malformed === true && vA.malformed_fields.some((m) => m.field === 'searcher_native.ramification_divisor_on_C_ref' && m.reason === 'json-pointer-unresolvable'),
    JSON.stringify(vA),
  );
}

// C16: json_pointer resolves (within the native artifact), but the resolved
// content's digest disagrees with the ref's declared digest -> existing
// [12] digest-mismatch path (p33=false), NOT malformed -- same discipline
// as the inline case (C13).
{
  const { native, cert } = freshCert();
  const content = { components: [{ locus_type: 'json-pointer-target-2', ideal_generator: ['1'], multiplicity: 1 }] };
  native._external_store = { searcherRam: content };
  cert.searcher_native.ramification_divisor_on_C_ref = {
    artifact_id: 'test-json-pointer/searcher-ram-mismatch',
    digest: '0'.repeat(64), // deliberately wrong
    json_pointer: '/_external_store/searcherRam',
  };
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C16 json_pointer resolves (within native artifact) but digest disagrees -> malformed=false, p33_ok=false (existing [12])', vA.malformed === false && vA.p33_ok === false, JSON.stringify(vA));
}

// C17 (control): a ref with NEITHER object_id NOR json_pointer is still
// correctly rejected as malformed (both-missing case unaffected by the fix).
{
  const { native, cert } = freshCert();
  cert.searcher_native.ramification_divisor_on_C_ref = { artifact_id: 'test/neither', digest: '0'.repeat(64) };
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('C17 ref with neither object_id nor json_pointer -> malformed=true', vA.malformed === true && vA.malformed_fields.some((m) => m.reason === 'ref-not-a-triple'), JSON.stringify(vA));
}

// --- 裁定150 items 2/3 new branches: pointer-unresolvable + inline fallback ---
console.log('\n=== 裁定150 items 2/3: json_pointer-unresolvable + inline fallback fixtures ===');

// C20 (裁定150 item 2, fallback success): json_pointer does NOT resolve
// (wrong path, or resolves outside the native artifact), but a
// digest-consistent `inline` IS also present -> falls back to inline,
// malformed=false, p33_ok=true (no [12] either -- the fallback data is
// genuinely correct).
{
  const { native, cert } = freshCert();
  const content = { components: [{ locus_type: 'fallback-target', ideal_generator: ['1'], multiplicity: 1 }] };
  cert.searcher_native.ramification_divisor_on_C_ref = {
    artifact_id: 'test-fallback/searcher-ram',
    digest: digestOf(content),
    json_pointer: '/this/path/does/not/exist/in/native', // deliberately unresolvable
    inline: content, // digest-consistent fallback
  };
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check(
    'C20 unresolvable json_pointer + digest-matching inline -> falls back to inline, malformed=false',
    vA.malformed === false,
    JSON.stringify(vA),
  );
  check(
    'C20 fallback data was genuinely used (p33_ok=true, no spurious [12])',
    vA.p33_ok === true,
    JSON.stringify(vA),
  );
}

// C21 (裁定150 item 2, fallback + existing [12]): json_pointer unresolvable,
// inline present but its OWN digest disagrees with the ref's declared
// digest -- still falls back to inline as the data source (not malformed),
// but surfaces as the pre-existing [12] digest-mismatch condition, exactly
// as an inline-only ref with a bad digest would (C13/C16 symmetry).
{
  const { native, cert } = freshCert();
  const content = { components: [{ locus_type: 'fallback-mismatch-target', ideal_generator: ['1'], multiplicity: 1 }] };
  cert.searcher_native.ramification_divisor_on_C_ref = {
    artifact_id: 'test-fallback/searcher-ram-mismatch',
    digest: '0'.repeat(64), // deliberately wrong vs. content's real digest
    json_pointer: '/this/path/does/not/exist/in/native',
    inline: content,
  };
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check(
    'C21 unresolvable json_pointer + digest-mismatched inline fallback -> malformed=false, p33_ok=false (existing [12], not malformed)',
    vA.malformed === false && vA.p33_ok === false,
    JSON.stringify(vA),
  );
}

// --- 裁定145 残差2: generateCertificate's OWN W-6 map_ref.inline placeholder
//     must be the ARRAY-of-{branch_value, multiplicity} shape (interp v3
//     条項2's W-6 entry shape; the shape lane B's verifier
//     search/ninfty-verifier-b.py _extract_w6_map parses, and the shape
//     the witness-gen-merged full-witness fixture already carries) -- NOT
//     a single descriptive dict ({description: ...}), which was a schema
//     mismatch, not a genuine alternate interpretation.
console.log('\n=== 裁定145 残差2: W-6 map_ref.inline is array-shaped ===');

// C18: both native_side entries' map_ref.inline are arrays (not a bare
// object), and every element carries branch_value + an integer multiplicity.
{
  const { cert } = freshCert();
  for (const entry of cert.pushforward_compatibility_witness) {
    const inline = entry.map_ref.inline;
    const isArray = Array.isArray(inline);
    check(
      `C18 map_ref.inline is an array (native_side=${entry.native_side})`,
      isArray,
      JSON.stringify(inline),
    );
    if (isArray) {
      const allShaped = inline.every((e) => e && typeof e === 'object' && 'branch_value' in e && Number.isInteger(e.multiplicity));
      check(
        `C18 every map_ref.inline entry has {branch_value, multiplicity:int} (native_side=${entry.native_side})`,
        allShaped,
        JSON.stringify(inline),
      );
    }
  }
}

// C19: the map_ref.inline entries agree (branch_value + multiplicity) with
// the corresponding native branch_divisor_on_P1_ref.components -- the array
// is genuinely derived from native data, not an arbitrary/hardcoded literal.
{
  const { native, cert } = freshCert();
  const searcherEntry = cert.pushforward_compatibility_witness.find((e) => e.native_side === 'searcher');
  const expected = native.branch_divisor_on_P1_ref.components.map((c) => ({ branch_value: c.locus_type, multiplicity: c.multiplicity }));
  check(
    'C19 searcher map_ref.inline matches native branch_divisor_on_P1_ref.components (locus_type/multiplicity)',
    JSON.stringify(searcherEntry.map_ref.inline) === JSON.stringify(expected),
    `got=${JSON.stringify(searcherEntry.map_ref.inline)} expected=${JSON.stringify(expected)}`,
  );
}

// --- 裁定177 F80-4.1: Sol's five adversarial W-4 (chart_overlap_witnesses)
//     probes against verifyChartOverlap. Direct probe found ALL FIVE
//     returning 'ABSENT' before this fix -- the first three (and the fifth)
//     should be MALFORMED, and the fourth (status=PRESENT + genuinely
//     non-empty, agreeing entries) should re-verify to PASS. Tested both
//     as isolated-function calls (verifyChartOverlap_forTest, matching
//     Sol's own direct-probe style) AND, for the MALFORMED cases,
//     end-to-end through runVerifierA to confirm the top-level
//     {malformed:true, ...} escalation actually fires.
console.log("\n=== 裁定177 F80-4.1: Sol's five adversarial W-4 probes ===");

const RAM_TAG = 'ramification_divisor_on_C_ref';
const BRANCH_TAG = 'branch_divisor_on_P1_ref';

const ADVERSARIAL_W4 = [
  { label: 'adversarial 1: status missing entirely + entries=[]', entry: { divisor_object: RAM_TAG, entries: [] }, expect: 'MALFORMED' },
  { label: 'adversarial 2: status=ABSENT + entries non-empty', entry: { divisor_object: RAM_TAG, status: 'ABSENT', entries: [{ chart_pair: ['a', 'b'], agree: true }] }, expect: 'MALFORMED' },
  { label: 'adversarial 3: status=PRESENT + entries=[]', entry: { divisor_object: RAM_TAG, status: 'PRESENT', entries: [] }, expect: 'MALFORMED' },
  { label: 'adversarial 5: unknown status + entries=[]', entry: { divisor_object: RAM_TAG, status: 'not-a-real-status', entries: [] }, expect: 'MALFORMED' },
];
for (const { label, entry, expect } of ADVERSARIAL_W4) {
  const got = verifyChartOverlap_forTest(entry);
  check(`裁定177 ${label} -> ${expect} (isolated verifyChartOverlap_forTest)`, got === expect, `got ${got}`);
}

// adversarial 4 (POSITIVE regression): status=PRESENT + genuinely correct,
// non-empty entries -> PASS (not ABSENT). Reuses the same synthetic
// agreeing-generator construction as fixture C1b.
{
  const native4 = buildSearcherNative(positive1.candidate);
  const ramGen4 = native4.ramification_divisor_on_C_ref.components[0].ideal_generator;
  const goodEntry = {
    divisor_object: RAM_TAG, status: 'PRESENT',
    entries: [{ chart_pair: ['x-chart-single', 'x-chart-hypothetical-2'], agree: true, generator_chart_a: ramGen4, generator_chart_b: ramGen4 }],
  };
  const got4 = verifyChartOverlap_forTest(goodEntry);
  check('裁定177 adversarial 4: status=PRESENT + correct non-empty entries -> PASS (isolated)', got4 === 'PASS', `got ${got4}`);
}

// End-to-end: each MALFORMED adversarial shape, wired into BOTH
// divisor_object slots of a real certificate, must escalate runVerifierA's
// TOP-LEVEL result to {malformed:true, ...} (not just a buried non-PASS
// inside R_A, which C1b/objVerify alone would not distinguish from an
// ordinary FAIL).
for (const { label, entry } of ADVERSARIAL_W4) {
  const { native, cert } = freshCert();
  cert.chart_overlap_witnesses = [
    { ...entry, divisor_object: RAM_TAG },
    { ...entry, divisor_object: BRANCH_TAG },
  ];
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check(`裁定177 end-to-end ${label} -> runVerifierA escalates malformed=true`,
        vA.malformed === true && Array.isArray(vA.malformed_fields) && vA.malformed_fields.length > 0,
        JSON.stringify(vA));
}

// --- 裁定185 F81-3.1: three remaining fail-closed gaps Sol found even
//     after the F80-4.1 six-branch fix (all reproduced directly against
//     classifyChartOverlapEntry_forTest / verifyChartOverlap_forTest
//     before this repair): (1) duplicate divisor_object-tagged W-4 entries
//     read as ABSENT instead of MALFORMED (v3 条項7: exactly 1 entry);
//     (2) a RETIRED per_overlap_witnesses key coexisting with a valid
//     canonical shape was not checked at all; (3) a PRESENT entry's inner
//     entries[] items were never schema-checked (entries:[null] crashed
//     with a TypeError, entries:[{}] was silently scored as an ordinary
//     arithmetic FAIL). Sol's four cases, end-to-end via runVerifierA.
console.log('\n=== 裁定185 F81-3.1: duplicate entry / retired-key coexistence / inner schema ===');

// case 1: duplicate entries for the SAME divisor_object -- MALFORMED, not ABSENT.
{
  const { native, cert } = freshCert();
  cert.chart_overlap_witnesses = [
    { divisor_object: RAM_TAG, status: 'ABSENT', entries: [] },
    { divisor_object: RAM_TAG, status: 'ABSENT', entries: [] }, // duplicate tag
    { divisor_object: BRANCH_TAG, status: 'ABSENT', entries: [] },
  ];
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('裁定185 case 1: duplicate divisor_object-tagged W-4 entries -> runVerifierA escalates malformed=true (v3 条項7)',
        vA.malformed === true && Array.isArray(vA.malformed_fields) && vA.malformed_fields.length > 0,
        JSON.stringify(vA));
}

// case 2: retired per_overlap_witnesses key coexisting with a canonical
// shape -- isolated probe of BOTH the "canonical ABSENT + retired key"
// and "canonical PRESENT + CONTRADICTING retired key" shapes Sol used,
// confirming they are no longer ABSENT/PASS respectively.
{
  const ramGenR185 = buildSearcherNative(positive1.candidate).ramification_divisor_on_C_ref.components[0].ideal_generator;
  const absentPlusRetired = { divisor_object: RAM_TAG, status: 'ABSENT', entries: [], per_overlap_witnesses: [] };
  const gotAbsentPlusRetired = classifyChartOverlapEntry_forTest(absentPlusRetired);
  check('裁定185 case 2a: canonical ABSENT + retired per_overlap_witnesses=[] -> MALFORMED (was ABSENT)',
        gotAbsentPlusRetired.status === 'MALFORMED', JSON.stringify(gotAbsentPlusRetired));

  const presentPlusContradictingRetired = {
    divisor_object: RAM_TAG, status: 'PRESENT',
    entries: [{ chart_pair: ['x-chart-single', 'x-chart-hypothetical-2'], agree: true, generator_chart_a: ramGenR185, generator_chart_b: ramGenR185 }],
    per_overlap_witnesses: [], // contradicts (empty) -- previously ignored, PASS leaked through
  };
  const gotPresentPlusRetired = classifyChartOverlapEntry_forTest(presentPlusContradictingRetired);
  check('裁定185 case 2b: canonical PRESENT + CONTRADICTING retired per_overlap_witnesses -> MALFORMED (was PASS)',
        gotPresentPlusRetired.status === 'MALFORMED', JSON.stringify(gotPresentPlusRetired));
}
// same case 2 (PRESENT + contradicting retired key), end-to-end.
{
  const { native, cert } = freshCert();
  const ramGen2 = native.ramification_divisor_on_C_ref.components[0].ideal_generator;
  const entry = {
    status: 'PRESENT',
    entries: [{ chart_pair: ['x-chart-single', 'x-chart-hypothetical-2'], agree: true, generator_chart_a: ramGen2, generator_chart_b: ramGen2 }],
    per_overlap_witnesses: [],
  };
  cert.chart_overlap_witnesses = [{ ...entry, divisor_object: RAM_TAG }, { ...entry, divisor_object: BRANCH_TAG }];
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check('裁定185 case 2: retired-key coexistence -> runVerifierA escalates malformed=true (end-to-end)',
        vA.malformed === true && Array.isArray(vA.malformed_fields) && vA.malformed_fields.length > 0,
        JSON.stringify(vA));
}

// case 3: inner entries[] item is null -- must NOT crash (TypeError), must
// resolve to MALFORMED end-to-end.
{
  const { native, cert } = freshCert();
  cert.chart_overlap_witnesses = [
    { divisor_object: RAM_TAG, status: 'PRESENT', entries: [null] },
    { divisor_object: BRANCH_TAG, status: 'PRESENT', entries: [null] },
  ];
  let threw = false;
  let vA;
  try {
    vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  } catch (e) {
    threw = true;
  }
  check('裁定185 case 3: entries=[null] does NOT crash (no TypeError)', threw === false, threw ? 'threw' : 'no throw');
  check('裁定185 case 3: entries=[null] -> runVerifierA escalates malformed=true (not a crash, not FAIL)',
        !threw && vA.malformed === true && Array.isArray(vA.malformed_fields) && vA.malformed_fields.length > 0,
        threw ? 'crashed' : JSON.stringify(vA));
}

// case 4: inner entries[] item is {} (missing required 'agree' field) --
// must be MALFORMED, not a silently-scored arithmetic FAIL.
{
  const { native, cert } = freshCert();
  cert.chart_overlap_witnesses = [
    { divisor_object: RAM_TAG, status: 'PRESENT', entries: [{}] },
    { divisor_object: BRANCH_TAG, status: 'PRESENT', entries: [{}] },
  ];
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  check("裁定185 case 4: entries=[{}] (missing 'agree') -> runVerifierA escalates malformed=true (was silently scored FAIL)",
        vA.malformed === true && Array.isArray(vA.malformed_fields) && vA.malformed_fields.length > 0,
        JSON.stringify(vA));
}

// isolated-function corroboration of cases 3/4 (matching Sol's own
// direct-probe style).
check('裁定185 case 3 (isolated): classifyChartOverlapEntry_forTest({status:PRESENT, entries:[null]}) -> MALFORMED (no throw)',
      (() => {
        try {
          return classifyChartOverlapEntry_forTest({ status: 'PRESENT', entries: [null] }).status === 'MALFORMED';
        } catch (e) {
          return false;
        }
      })());
check("裁定185 case 4 (isolated): classifyChartOverlapEntry_forTest({status:PRESENT, entries:[{}]}) -> MALFORMED (not FAIL)",
      classifyChartOverlapEntry_forTest({ status: 'PRESENT', entries: [{}] }).status === 'MALFORMED');

// --- Worked examples from the spec text itself (Sec.5.3.2 line 508 and
//     contract Sec.5.1 F4.1/F4.2), tested directly against combine()'s
//     priority ordering (sanity-check of INTEGRITY_PRIORITY table, not a
//     certificate scenario).
console.log('\n=== spec worked-example priority checks ===');
{
  const c = combine({ semanticS1S2Reasons: ['sealed-field-leak'], rejectReasons: ['precondition/degree-mismatch'], R_A: undefined, R_B: undefined });
  check('worked example: [1]+[9] -> primary=[9]', c.primary_reason_code === 'sealed-field-leak', JSON.stringify(c));
}
{
  const c = combine({ semanticS1S2Reasons: ['pell-derivative-mismatch', 'divisor-equality-failure'], rejectReasons: [], R_A: undefined, R_B: undefined });
  check('worked example: [15]+[25] -> primary=[15]', c.primary_reason_code === 'pell-derivative-mismatch', JSON.stringify(c));
}

console.log(`\n=== summary: ${total - failures}/${total} passed ===`);
if (failures > 0) process.exit(1);
