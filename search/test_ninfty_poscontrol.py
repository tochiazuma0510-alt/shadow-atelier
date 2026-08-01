#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/test_ninfty_poscontrol.py

NON-BLIND unit fixtures for the positive-control harness
(search/ninfty-ep-poscontrol-harness.py), which is the only kind of trial
Sol 便97 P97-4.1 authorises. There is no secret trial here, no blind
campaign, no calibration claim and no EP status change: every fixture below
runs with the "secrets" in plain sight, which is precisely why it is a unit
fixture and not a positive control.

Sections map 1:1 onto 便97 W97-4.1 items 1--10.

Run: python search/test_ninfty_poscontrol.py    (exit 0 iff all checks PASS)
"""
from __future__ import annotations

import copy
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DRAFT_V1 = os.path.join(REPO, "docs", "ep_positive_control_design_draft_v1.md")
DRAFT_V2 = os.path.join(REPO, "docs", "ep_positive_control_design_draft_v2.md")

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if not ok else ""))


def _load(alias, filename):
    path = os.path.join(HERE, filename)
    spec = importlib.util.spec_from_file_location(alias, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


H = _load("poscontrol_harness", "ninfty-ep-poscontrol-harness.py")

with open(os.path.join(HERE, "ninfty-ep-poscontrol-harness.py"), encoding="utf-8") as f:
    HARNESS_SRC = f.read()
with open(DRAFT_V2, encoding="utf-8") as f:
    DRAFT_V2_TEXT = f.read()

BASE = {"schema_id": "mb/ninfty-evidence-union/raw-w6-evidence/v1",
        "certificate": {"predicate_spec_id": "mb/ninfty-stage2-predicate/v18",
                        "searcher_native": {"native_schema_id": "x#cert-schema"},
                        "checker_native": {"native_schema_id": "x#cert-schema"}},
        "components": [{"branch_value": "b0", "multiplicity": 1},
                       {"branch_value": "b1", "multiplicity": 2}]}

EXACT_VECTOR = {"expected_stage": "T1", "expected_primary_reason_code": "[24]",
                "expected_sealed_reason_vector": ["[24]", "[27]"],
                "expected_public_reason_vector": ["[24]"], "expected_exit_code": 1}

# ============================================================================
# §1 item 1 -- THREE roles
# ============================================================================

check("§1 the harness declares THREE roles (injector / detector / adjudicator), repairing the draft's "
      "'two-role separation' wording (W97-4.1 item 1)",
      H.ROLES == ("injector", "detector", "adjudicator"), H.ROLES)
_v2_body = DRAFT_V2_TEXT.split("\n## 1.", 1)[-1]
check("§1 the design draft v2 says 三役分離 in its NORMATIVE body, the old 二役分離 wording survives only "
      "inside the version-difference table as a quotation of v1, and v1 itself still exists unedited "
      "(versioned supersede, not an in-place fix)",
      "三役分離" in DRAFT_V2_TEXT and "二役分離" not in _v2_body and "二役分離" in DRAFT_V2_TEXT
      and os.path.exists(DRAFT_V1),
      ("三役分離" in DRAFT_V2_TEXT, "二役分離" in _v2_body))

# ============================================================================
# §2 item 2 -- blind injection is settled, not an open choice
# ============================================================================

check("§2 the harness states that a `calibrated detector` claim REQUIRES blind injection and that an "
      "absence argument is not a substitute (W97-4.1 item 2 closes draft v1 section 5 item 1)",
      "absence argument" in H.BLIND_INJECTION_REQUIRED_NOTE
      and "NOT a substitute" in H.BLIND_INJECTION_REQUIRED_NOTE)
check("§2 the draft v2 no longer lists 盲検注入 vs 不在論証 as an undecided choice",
      "継続諮問中" not in DRAFT_V2_TEXT.split("## 5")[-1] if "## 5" in DRAFT_V2_TEXT else True)

# ============================================================================
# §3 item 3 -- high-entropy commitment, not a dictionary-attackable digest
# ============================================================================

KEY = H.new_key()
NONCE = H.new_nonce()
PAYLOAD = {"campaign_id": "pc-draft", "trial_id": "t01", "catalog_digest": "0" * 64,
           "base_artifact_digest": H.sha256_of(BASE), "mutation_id": "m-swap",
           "mutation_parameters": {"op": "set", "json_pointer": "/components/0/multiplicity", "value": 2},
           "mutated_artifact_digest": "", "exact_expected_vector": EXACT_VECTOR,
           "null_or_injected": "injected", "nonce": NONCE}
PAYLOAD["mutated_artifact_digest"] = H.sha256_of(
    H.apply_mutation(BASE, PAYLOAD["mutation_parameters"]))

check("§3 the nonce is high-entropy (>= 32 hex chars from a CSPRNG), so the commitment cannot be "
      "inverted by enumerating the small option set (W97-4.1 item 3)",
      len(NONCE) >= 64 and NONCE != H.new_nonce())
check("§3 the harness uses an HMAC over the sealed payload, not a bare sha256 of the options",
      "hmac.new" in HARNESS_SRC and "hmac.compare_digest" in HARNESS_SRC)
SEALED = H.seal_commitment(PAYLOAD, KEY)
check("§3 the commitment binds EXACTLY the P97-4.1 field list",
      tuple(SEALED["bound_fields"]) == H.COMMITMENT_FIELDS
      and set(H.COMMITMENT_FIELDS) == {"campaign_id", "trial_id", "catalog_digest",
                                       "base_artifact_digest", "mutation_id", "mutation_parameters",
                                       "mutated_artifact_digest", "exact_expected_vector",
                                       "null_or_injected", "nonce"},
      SEALED["bound_fields"])
check("§3 the sealed values themselves never appear in the commitment object",
      not any(str(PAYLOAD[f]) in H.canonical(SEALED) for f in ("mutation_id", "nonce")))
for _field in H.COMMITMENT_FIELDS:
    _tampered = copy.deepcopy(PAYLOAD)
    _tampered[_field] = ("null" if _field == "null_or_injected" else
                         ("z" * 64 if isinstance(_tampered[_field], str) else {"changed": True}))
    if _field == "exact_expected_vector":
        _tampered[_field] = dict(EXACT_VECTOR, expected_primary_reason_code="[25]")
    try:
        _ok = H.verify_commitment(_tampered, KEY, SEALED)
    except ValueError:
        _ok = False
    check(f"§3 changing the bound field {_field!r} breaks the commitment (nothing is bound loosely)",
          _ok is False)
_refused_when_missing = []
for _field in H.COMMITMENT_FIELDS:
    _short = {k: v for k, v in PAYLOAD.items() if k != _field}
    try:
        H.seal_commitment(_short, KEY)
        _refused_when_missing.append((_field, "SEALED ANYWAY"))
    except ValueError:
        pass
check("§3 a commitment missing ANY required field is refused outright -- a commitment that omits a "
      "field binds less than it claims to",
      _refused_when_missing == [], _refused_when_missing)

# ============================================================================
# §4 item 4 -- the injector's self-report is replayed, not believed
# ============================================================================

_ok, _digest, _reason = H.replay_and_verify(BASE, PAYLOAD["mutation_parameters"],
                                            PAYLOAD["mutated_artifact_digest"])
check("§4 positive control: the adjudicator replays the declared mutation from the clean base and "
      "reproduces the committed mutated digest (W97-4.1 item 4)", _ok, (_digest, _reason))
_ok, _digest, _reason = H.replay_and_verify(BASE, PAYLOAD["mutation_parameters"], "0" * 64)
check("§4 a LYING injector is caught: the replayed digest contradicts the committed one",
      _ok is False and "contradicted" in _reason, _reason)
_ok, _digest, _reason = H.replay_and_verify(
    BASE, {"op": "set", "json_pointer": "/components/0/multiplicity", "value": 1}, H.sha256_of(BASE))
check("§4 a NO-OP 'mutation' is caught: nothing was actually injected",
      _ok is False and "unchanged" in _reason, _reason)
_ok, _digest, _reason = H.replay_and_verify(
    BASE, {"op": "set", "json_pointer": "/no/such/path", "value": 1}, "0" * 64)
check("§4 a mutation that does not replay against the clean base is a failure, not a skip",
      _ok is False and "does not replay" in _reason, _reason)

# ============================================================================
# §5 item 5 -- exact expected vectors; ranges rejected
# ============================================================================

check("§5 an exact per-trial vector (stage, primary, sealed vector, public vector, exit code) validates",
      H.validate_expected_vector(EXACT_VECTOR)[0] is True, H.validate_expected_vector(EXACT_VECTOR))
for _bad, _label in (
        ({**EXACT_VECTOR, "expected_public_reason_vector": ["[1]--[5]"]}, "a RANGE '[1]--[5]'"),
        ({k: v for k, v in EXACT_VECTOR.items() if k != "expected_stage"}, "an ABSENT stage"),
        ({**EXACT_VECTOR, "expected_primary_reason_code": ["[24]", "[25]"]}, "a SET of primaries"),
        ({**EXACT_VECTOR, "expected_exit_code": "1"}, "a non-integer exit code")):
    _ok, _errs = H.validate_expected_vector(_bad)
    check(f"§5 {_label} is rejected -- 'somewhere in this range' is not an expectation (W97-4.1 item 5)",
          _ok is False, _errs)
try:
    H.seal_commitment({**PAYLOAD, "exact_expected_vector": {"expected_stage": "T1"}}, KEY)
    _sealed_loose = True
except ValueError:
    _sealed_loose = False
check("§5 an injected trial cannot even be SEALED with a loose expectation",
      _sealed_loose is False)

# ============================================================================
# §6 item 6 -- null trials, hidden injection bit, false positives measurable
# ============================================================================

_null_payload = {**PAYLOAD, "trial_id": "t02", "null_or_injected": "null",
                 "mutation_id": None, "mutation_parameters": None,
                 "mutated_artifact_digest": PAYLOAD["base_artifact_digest"],
                 "exact_expected_vector": None, "nonce": H.new_nonce()}
check("§6 a NULL (no-injection) trial is a first-class sealed trial, so false positives are measured "
      "too (W97-4.1 item 6)",
      H.seal_commitment(_null_payload, KEY)["commitment"] != SEALED["commitment"])
_trial = {"trial_id": "t01", "artifact": BASE, "null_or_injected": "injected",
          "exact_expected_vector": EXACT_VECTOR, "mutation_id": "m-swap",
          "mutation_parameters": {}, "base_artifact_digest": "x", "nonce": NONCE, "order_index": 3}
_view = H.detector_view(_trial)
check("§6 the detector's view withholds the injection bit, the expected vector, the mutation, the "
      "base digest, the nonce AND the trial's position in the order",
      set(_view) == {"trial_id", "artifact"}, sorted(_view))
check("§6 the withheld fields are genuinely absent, not merely blanked",
      all(k not in H.canonical(_view) for k in ("null_or_injected", "expected_stage", "m-swap")))

# ============================================================================
# §7 item 7 -- full path means public ingress .. public receipt
# ============================================================================

check("§7 the full path is declared as the eight public-ingress..public-receipt stages",
      H.FULL_PATH_STAGES == ("public_ingress", "schema_and_digest", "registry_resolution", "lane_a",
                             "lane_b", "w6", "composition", "public_receipt"), H.FULL_PATH_STAGES)
check("§7 a trial traversing every stage is a full-path trial",
      H.is_full_path(list(H.FULL_PATH_STAGES))[0] is True)
_ok, _missing = H.is_full_path(["lane_a"])
check("§7 a mutation applied to an internal function is a UNIT test and is NOT counted as full-path "
      "(W97-4.1 item 7)", _ok is False and "public_ingress" in _missing, _missing)
check("§7 an unrecorded path is not a full path (fail-closed, not 'assume it went through')",
      H.is_full_path(None)[0] is False)

# ============================================================================
# §8 item 8 -- data plane and code plane are separate families
# ============================================================================

check("§8 F-con is SPLIT into a data-plane one-lane fault and a code-plane tamper, with different "
      "planes (W97-4.1 item 8: otherwise F-con only measures the code-digest gate [12])",
      H.FAULT_FAMILIES["F-con-data"]["plane"] == "data_plane"
      and H.FAULT_FAMILIES["F-con-code"]["plane"] == "code_plane",
      {k: v["plane"] for k, v in H.FAULT_FAMILIES.items()})
check("§8 every family declares exactly one plane from the fixed set",
      all(v["plane"] in H.PLANES for v in H.FAULT_FAMILIES.values()))
_catalog = H.build_catalog([{"mutation_id": "m-swap", "family": "F-w6", "op": "set",
                             "json_pointer": "/components/0/multiplicity", "value": 2}])
check("§8 the catalog is digested over its own content, so a claim can be scoped to it",
      len(_catalog["catalog_digest"]) == 64 and _catalog["errors"] == [], _catalog["errors"])
_bad_catalog = H.build_catalog([{"mutation_id": "x", "family": "F-nonexistent"}])
check("§8 an unknown fault family is an error, not a silently accepted entry",
      _bad_catalog["errors"], _bad_catalog["errors"])

# ============================================================================
# §9 item 9 -- catalog coverage is not a false-negative rate
# ============================================================================

_scope = H.calibration_scope(_catalog["catalog_digest"])
check("§9 the claim is scoped to `catalog-calibrated under <catalog_digest>` and explicitly denies "
      "being a general false-negative rate (W97-4.1 item 9)",
      _scope.startswith("catalog-calibrated under " + _catalog["catalog_digest"])
      and "not a general" in _scope, _scope)

# ============================================================================
# §10 item 10 -- the dry-run receipt is a different artifact class
# ============================================================================

_dry = H.dry_run_receipt(_catalog["catalog_digest"], [], ["F-w6"])
check("§10 the pre-W-6 dry-run receipt has its OWN schema id, distinct from the calibration receipt",
      _dry["schema_id"] == H.DRY_RUN_RECEIPT_SCHEMA_ID
      and _dry["schema_id"] != H.CALIBRATION_RECEIPT_SCHEMA_ID)
check("§10 it records F-w6 as undetectable_by_construction and forbids being merged into or reported "
      "as a calibration receipt (W97-4.1 item 10)",
      _dry["undetectable_by_construction"] == ["F-w6"] and _dry["is_calibration"] is False
      and "may NOT be merged" in _dry["merge_rule"])
check("§10 the dry-run receipt still carries calibrated_detector=false and ep_status=uncalibrated/UNKNOWN",
      _dry["calibrated_detector"] is False and _dry["ep_status"] == "uncalibrated/UNKNOWN")

# ============================================================================
# §11 the authorisation boundary itself (P97-4.1) -- asserted in code
# ============================================================================

try:
    H.run_blind_campaign()
    _refused = False
except H.NotAuthorised as exc:
    _refused = "NOT authorised" in str(exc)
check("§11 a blind campaign run is REFUSED by the code, so the absence of a blind run is a property of "
      "the harness rather than of anyone's restraint (P97-4.1 不認可)", _refused)
check("§11 there is no code path that can emit calibrated_detector=true",
      "calibrated_detector" in HARNESS_SRC
      and all(frag not in HARNESS_SRC for frag in ("calibrated_detector\": True",
                                                   "calibrated_detector': True",
                                                   "calibrated_detector = True")))
_status = H.harness_status()
check("§11 the harness's own status keeps EP at uncalibrated/UNKNOWN and denies that the instrument's "
      "existence is a positive control",
      _status["calibrated_detector"] is False and _status["ep_status"] == "uncalibrated/UNKNOWN"
      and _status["blind_campaign_authorised"] is False
      and "not the existence of a positive control" in _status["note"], _status)
check("§11 the harness performs no ingress into the real pipeline: it imports no lane, no registry and "
      "no union module, and starts no subprocess",
      all(tok not in HARNESS_SRC for tok in ("subprocess", "importlib", "ninfty-native-registry",
                                             "ninfty-evidence-union", "ninfty-checker")))

n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS)} checks, {n_fail} FAIL")
raise SystemExit(1 if n_fail else 0)
