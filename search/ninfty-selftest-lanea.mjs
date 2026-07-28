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
  loadFreezeReceiptDigests, DEFAULT_FREEZE_RECEIPT_PATH,
} from './ninfty-searcher-v2.mjs';
import { runVerifierA, combine, vectorsEqual } from './ninfty-verifier-a.mjs';
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
  const ramGen = native.ramification_divisor_on_C_ref.components[0].ideal_generator;
  cert.chart_overlap_witnesses = {
    kind: 'chart-overlap',
    chart_atlas: [{ chart_id: 'x-chart-single', coordinate: 'x' }, { chart_id: 'x-chart-hypothetical-2', coordinate: 'x' }],
    per_overlap_witnesses: [{ chart_pair: ['x-chart-single', 'x-chart-hypothetical-2'], agree: true, generator_chart_a: ramGen, generator_chart_b: ramGen }],
    status: 'PASS',
    reason: 'SYNTHETIC for regression testing only -- not lane A native scope',
  };
  cert.pushforward_compatibility_witness = {
    kind: 'pushforward-compatibility',
    points: [{ point_ref: 'synthetic-point-1', ram_multiplicity: 1, branch_multiplicity: 1, match: true }],
    status: 'PASS',
    reason: 'SYNTHETIC for regression testing only -- not lane A native scope',
  };
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
  const w = cert.exact_point_equality_witnesses.ramification_divisor_on_C[0].witness;
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
