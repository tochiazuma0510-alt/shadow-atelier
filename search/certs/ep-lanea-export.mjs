// search/certs/ep-lanea-export.mjs
//
// EP (endorsement point) receiving-side export helper for lane A.
//
// ROLE: this file is part of the EP runner's RECEIVING side (search/ninfty-ep-runner.py),
// NOT a third lane. It imports lane A's own two frozen artifacts
// (search/ninfty-searcher-v2.mjs, search/ninfty-verifier-a.mjs) exactly as lane A's own
// selftest (search/ninfty-selftest-lanea.mjs) does, and dumps to stdout (JSON):
//
//   1. decision_fixture_results[]  -- evaluateDecisionLane() run over lane A's own
//      decisionLaneFixtures (9 fixtures from search/certs/fixtures-lanea.mjs), with the
//      candidate + lane A's own verdict/primary_reason_code (native verdict, lane A side).
//   2. cert_fixtures[]              -- the 5 certificate fixtures C1..C5 EXACTLY as
//      constructed inline in ninfty-selftest-lanea.mjs (same corruptions applied), but
//      WITHOUT that file's own MOCKED R_B (the mock is lane-A-internal state-machine
//      unit testing; the EP runner instead computes a genuine, independently-derived
//      R_B via lane B's verifier over a schema-converted certificate -- see
//      ninfty-ep-runner.py). For each: cert, native (single blob, since C1-C5 all use
//      searcherNative===checkerNative), R_A (genuine, from runVerifierA), overall_verdict_A.
//
// This script does NOT modify lane A's files and does NOT read any lane B (python)
// source. It is read-only w.r.t. both lanes -- consistent with the EP runner's
// receiving-side role (task brief: "受領側は両 lane を見てよい(lane 同士は相互不可視
// のまま -- コードを混ぜない・突合のみ)").

import {
  evaluateDecisionLane, buildSearcherNative, generateCertificate,
} from '../ninfty-searcher-v2.mjs';
import { runVerifierA } from '../ninfty-verifier-a.mjs';
import { decisionLaneFixtures, positive1 } from './fixtures-lanea.mjs';

// 裁定124 (便76 F76-5.4/5.5 修理): use the REAL freeze-receipt digests, not a
// placeholder string, so P-3.1 is a genuine cross-lane pin check rather than
// a guaranteed-mismatch artifact of this export script's own choice. Values
// read verbatim from provenance/ninfty_freeze_receipt_sol75.md (receipt_id
// mb/ninfty-stage2-freeze-receipt/sol75/e2c9c701-e41d51db-df59b25f).
const PREDICATE_SPEC_ID = 'mb/ninfty-stage2-predicate/v18';
const PREDICATE_SPEC_DIGEST_PLACEHOLDER = 'e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56';

// --- 1. decision-lane fixtures (native verdict, lane A) --------------------

const decision_fixture_results = decisionLaneFixtures.map((fx) => {
  const result = evaluateDecisionLane(fx.candidate);
  return {
    label: fx.label,
    candidate: fx.candidate,
    expect: fx.expect,
    laneA_native: { verdict: result.verdict, primary_reason_code: result.primary_reason_code },
  };
});

// --- 2. cert fixtures C1..C5 (verbatim reconstruction of the selftest's own
//        construction, minus the MOCKED R_B) ---------------------------------

function makeBaseCert(candidateRef) {
  const native = buildSearcherNative(positive1.candidate);
  const cert = generateCertificate({
    candidateRef,
    searcherNative: native,
    checkerNative: native,
    predicateSpecId: PREDICATE_SPEC_ID,
    predicateSpecDigest: PREDICATE_SPEC_DIGEST_PLACEHOLDER,
  });
  return { native, cert };
}

const cert_fixtures = [];

// C1: clean PASS
{
  const { native, cert } = makeBaseCert('lanea-cert-fixture-c1');
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  cert_fixtures.push({ id: 'C1', label: 'clean-PASS', corruption: 'none', cert, native, R_A: vA.R_A, overall_verdict_A: vA.overall_verdict_A, p33_ok: vA.p33_ok });
}

// C2: digest-mismatch [12] -- corrupt searcher_native.native_artifact_digest
{
  const { native, cert } = makeBaseCert('lanea-cert-fixture-c2');
  cert.searcher_native.native_artifact_digest = '0'.repeat(64);
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  cert_fixtures.push({ id: 'C2', label: 'digest-mismatch-[12]', corruption: 'searcher_native.native_artifact_digest corrupted', cert, native, R_A: vA.R_A, overall_verdict_A: vA.overall_verdict_A, p33_ok: vA.p33_ok });
}

// C3: divisor-equality-failure [25] -- corrupt first ideal-equality witness's forward divisor
{
  const { native, cert } = makeBaseCert('lanea-cert-fixture-c3');
  const w = cert.exact_point_equality_witnesses.ramification_divisor_on_C[0].witness;
  w.forward.divisor_monic = ['1', '1'];
  w.forward.remainder = ['1'];
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  cert_fixtures.push({ id: 'C3', label: 'divisor-equality-failure-[25]', corruption: 'ramification W-2 first witness forward.divisor_monic corrupted', cert, native, R_A: vA.R_A, overall_verdict_A: vA.overall_verdict_A, p33_ok: vA.p33_ok });
}

// C4: clean cert (verifier-result-mismatch [26] is tested by the EP runner
// itself, comparing this genuine R_A against a genuinely independent R_B --
// no artificial R_B flip needed here, unlike the selftest's own unit test).
{
  const { native, cert } = makeBaseCert('lanea-cert-fixture-c4');
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  cert_fixtures.push({ id: 'C4', label: 'clean-for-concordance-check', corruption: 'none (selftest applies a MOCK R_B flip here; EP runner instead compares against a genuinely independent verifier-B run)', cert, native, R_A: vA.R_A, overall_verdict_A: vA.overall_verdict_A, p33_ok: vA.p33_ok });
}

// C5: clean cert (selftest injects a MOCK semantic S2 code + MOCK R_B flip
// purely to test invariant-2 secondary-code emission in combine(); EP runner
// omits both mocks and only carries the genuine cert through for R_A vs
// genuine R_B concordance).
{
  const { native, cert } = makeBaseCert('lanea-cert-fixture-c5');
  const vA = runVerifierA({ certificate: cert, searcherNativeBlob: native, checkerNativeBlob: native });
  cert_fixtures.push({ id: 'C5', label: 'clean-for-concordance-check-2', corruption: 'none (selftest applies MOCK S2 code + MOCK R_B flip here; EP runner omits both mocks)', cert, native, R_A: vA.R_A, overall_verdict_A: vA.overall_verdict_A, p33_ok: vA.p33_ok });
}

process.stdout.write(JSON.stringify({ decision_fixture_results, cert_fixtures }));
