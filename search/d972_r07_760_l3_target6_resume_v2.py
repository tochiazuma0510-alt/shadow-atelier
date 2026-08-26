#!/usr/bin/env python3
"""Checkpointed j>=9 continuation of the frozen g760 L3 target6 lane.

The inherited j=2,...,8 prefix is only a producer control-flow candidate.
This adapter authenticates the exact v1 resource-stop artifacts, rebuilds the
full v1 static input, and computes j=9,10,11,12 in order.  An interrupted j is
never checkpointed; without an optional relator-level state it is recomputed
from relator 1.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
V1_PATH = Path("search/d972_r07_760_l3_target6_v1.py")
TASK_PATH = Path("sol/luna_task_164_r07_760_l3_target6_resume_v2.md")
PRIOR_RECEIPT_PATH = Path(
    "search/certs/d972_r07_760_l3_target6_prior_"
    "run32901384400_v1_20260826.json")
PRIOR_LOG_PATH = Path(
    "search/certs/d972_r07_760_l3_target6_prior_"
    "run32901384400_producer_v1_20260826.log")

SCHEMA = "d972-r07-760-l3-target6-resume/v2"
CHECKPOINT_SCHEMA = "d972-r07-760-l3-target6-resume-checkpoint/v2"
PREFLIGHT_STATE = "R07_760_L3_TARGET6_RESUME_V2_PREFLIGHT_READY"
CHECKPOINT_STATE = "R07_760_L3_TARGET6_RESUME_V2_CHECKPOINT_READY"
FINAL_MARKER = "R07_760_L3_TARGET6_RESUME_V2_PRODUCER_PASS"
DEFAULT_PREFLIGHT = Path(
    "search/certs/d972_r07_760_l3_target6_resume_"
    "preflight_v2_20260826.json")
DEFAULT_FULL = Path("ci/out/d972_r07_760_l3_target6_resume_v2.json")
DEFAULT_CHECKPOINT_DIR = Path(
    "ci/out/d972_r07_760_l3_target6_resume_v2_checkpoints")

INHERITED_PREFIX = (2, 3, 4, 5, 6, 7, 8)
FRESH_J_ORDER = (9, 10, 11, 12)
START_J = 9
MAX_SECONDS = 21600.0
RECOMMENDED_SECONDS = 21000.0
MAX_RSS_MIB = 5600
BASE_SHA = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
PARENT_SHA = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"

PRIOR_RUN_ID = 32901384400
PRIOR_HEAD_SHA = "c1e7eb8fcd08676d5a6efad82add2c1c832a22c0"
PRIOR_RECEIPT_BYTES = 3239
PRIOR_RECEIPT_SHA = (
    "1c739559eee368ba676c694960be21db94d6bc2292a6136d89b97bedfef3e15b")
PRIOR_LOG_BYTES = 164
PRIOR_LOG_SHA = (
    "fc3901c29f958e216e17ba175be4857ee26cc140f3f809f0e29833b636ccd436")
V1_BYTES = 53284
V1_SHA = "7048e73a02e76df5d49fd359c52d5be70ae99d70aa95ebe74b28c4a18f130fde"
TASK_BYTES = 5292
TASK_SHA = "761359bda0fc14543ab9266ec61139006403525d828811bb2af5d27d34ccfc9d"

TERMINALS = {
    "R07_760_L3_TARGET6_NONMEMBER",
    "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
    "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
    "R07_760_L3_TARGET6_INPUT_STOP",
}

V2_PIN_SPECS: dict[str, tuple[Path, int, str]] = {
    "task_164": (TASK_PATH, TASK_BYTES, TASK_SHA),
    "v1_producer": (V1_PATH, V1_BYTES, V1_SHA),
    "prior_receipt": (
        PRIOR_RECEIPT_PATH, PRIOR_RECEIPT_BYTES, PRIOR_RECEIPT_SHA),
    "prior_producer_log": (PRIOR_LOG_PATH, PRIOR_LOG_BYTES, PRIOR_LOG_SHA),
}


class InputStop(RuntimeError):
    pass


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def resolve_repo_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def v2_pin_inputs() -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for label, (path, size, digest) in V2_PIN_SPECS.items():
        full = ROOT / path
        if not full.is_file() or full.stat().st_size != size or \
                digest_file(full) != digest:
            raise InputStop("v2 pin drift: " + path.as_posix())
        rows[label] = {"path": path.as_posix(), "bytes": size,
                       "sha256": digest}
    return rows


def load_v1() -> Any:
    spec = importlib.util.spec_from_file_location(
        "_d972_r07_760_l3_target6_frozen_v1", ROOT / V1_PATH)
    require(spec is not None and spec.loader is not None,
            "v1 producer module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    require(digest_file(ROOT / V1_PATH) == V1_SHA,
            "v1 producer post-import pin")
    return module


def claims() -> dict[str, bool]:
    return {
        "actual_A18_occurrence": False,
        "normalized_Brunnian_class": False,
        "compatible_cofinal_lift": False,
        "ihara_witness": False,
        "all_bases_obstruction": False,
    }


def verify_self_digest(data: dict[str, Any], label: str) -> None:
    require(type(data) is dict and type(data.get("self_digest_sha256")) is str,
            label + " self digest field")
    work = copy.deepcopy(data)
    claimed = work.pop("self_digest_sha256")
    require(claimed == digest_obj(work), label + " self digest")


def authenticate_prior() -> dict[str, Any]:
    receipt_path = ROOT / PRIOR_RECEIPT_PATH
    log_path = ROOT / PRIOR_LOG_PATH
    receipt_raw = receipt_path.read_bytes()
    log_raw = log_path.read_bytes()
    require(len(receipt_raw) == PRIOR_RECEIPT_BYTES and
            hashlib.sha256(receipt_raw).hexdigest() == PRIOR_RECEIPT_SHA,
            "prior receipt bytes")
    require(len(log_raw) == PRIOR_LOG_BYTES and
            hashlib.sha256(log_raw).hexdigest() == PRIOR_LOG_SHA,
            "prior producer log bytes")
    data = json.loads(receipt_raw.decode("ascii"))
    require(receipt_raw == canonical_bytes(data) + b"\n",
            "prior receipt canonical bytes")
    verify_self_digest(data, "prior receipt")
    require(data.get("schema") == "d972-r07-760-l3-target6/v1" and
            data.get("mode") == "full" and
            data.get("status") ==
                "R07_760_L3_TARGET6_UNKNOWN_RESOURCE" and
            data.get("terminal_token") ==
                "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
            "prior terminal envelope")
    result = data.get("result", {})
    require(result.get("state") ==
                "R07_760_L3_TARGET6_UNKNOWN_RESOURCE" and
            result.get("requested_seconds") == 10200.0 and
            result.get("stage") == "j=9:D2-relator-7" and
            result.get("mathematical_membership_claimed") is False and
            result.get("mathematical_nonmembership_claimed") is False,
            "prior exact stop fields")
    base = data.get("static", {}).get("base", {})
    require(base.get("base_kind") == "r07_760_commutator" and
            base.get("sha256") == BASE_SHA and
            base.get("parent_616_sha256") == PARENT_SHA and
            base.get("length") == 760 and
            base.get("free_exponent_sums") == [0, 0],
            "prior base fields")
    require(all(value is False for value in data.get("claims", {}).values())
            and len(data.get("claims", {})) == len(claims()),
            "prior false claims")
    expected_log = (
        "R07_760_L3_TARGET6_V1_PRODUCER_PASS "
        "terminal=R07_760_L3_TARGET6_UNKNOWN_RESOURCE "
        f"sha256={PRIOR_RECEIPT_SHA} bytes={PRIOR_RECEIPT_BYTES}\n"
    ).encode("ascii")
    require(log_raw == expected_log, "prior producer log exact marker")
    binding = {
        "run_id": PRIOR_RUN_ID,
        "head_sha": PRIOR_HEAD_SHA,
        "evidence_grade": "producer_control_flow_candidate_only",
        "inherited_candidate_prefix": list(INHERITED_PREFIX),
        "next_j": START_J,
        "unfinished_j_state_serialized": False,
        "prior_receipt": {
            "path": PRIOR_RECEIPT_PATH.as_posix(),
            "bytes": PRIOR_RECEIPT_BYTES,
            "sha256": PRIOR_RECEIPT_SHA,
            "self_digest_sha256": data["self_digest_sha256"],
            "terminal": data["terminal_token"],
            "stage": result["stage"],
            "requested_seconds": result["requested_seconds"],
        },
        "prior_producer_log": {
            "path": PRIOR_LOG_PATH.as_posix(),
            "bytes": PRIOR_LOG_BYTES,
            "sha256": PRIOR_LOG_SHA,
        },
        "v1_producer": {
            "path": V1_PATH.as_posix(), "bytes": V1_BYTES,
            "sha256": V1_SHA,
        },
    }
    binding["binding_sha256"] = digest_obj(binding)
    return binding


def summarize_static(v1_static: dict[str, Any],
                     v2_pins: dict[str, Any],
                     prior: dict[str, Any]) -> dict[str, Any]:
    require(type(v1_static.get("pins")) is dict and v1_static["pins"],
            "v1 static pins")
    without_pins = copy.deepcopy(v1_static)
    v1_pins = without_pins.pop("pins")
    base = v1_static["base"]
    target = v1_static["target6"]
    legal = v1_static["legal_overapproximation"]
    d2 = v1_static["PB4_D2"]
    jennings = v1_static["Jennings"]
    require(base["sha256"] == BASE_SHA and base["length"] == 760 and
            base["free_exponent_sums"] == [0, 0], "fresh static base")
    require(jennings["j_order"] == list(range(2, 13)) and
            jennings["first_terminal_rule"] is True,
            "fresh static Jennings order")
    summary = {
        "full_v1_static_rebuilt": True,
        "v1_static_without_pins_sha256": digest_obj(without_pins),
        "v1_pin_manifest_sha256": digest_obj(v1_pins),
        "v1_pin_manifest": v1_pins,
        "v2_pin_manifest_sha256": digest_obj(v2_pins),
        "v2_pin_manifest": v2_pins,
        "prior_binding_sha256": prior["binding_sha256"],
        "base": {
            "base_kind": base["base_kind"],
            "parent_616_sha256": base["parent_616_sha256"],
            "length": base["length"], "sha256": base["sha256"],
            "free_exponent_sums": base["free_exponent_sums"],
        },
        "target6": {
            key: target[key] for key in (
                "name", "formula", "word_length", "word_sha256",
                "raw_E4_gradient_sha256", "projected_L3_gradient_sha256",
                "value_identity_in_current_E4")
        },
        "prefix_action": {
            key: v1_static["prefix_action"][key] for key in (
                "formula", "value_sha256", "inverse_is_distinct",
                "fresh_from_g760")
        },
        "legal_overapproximation": {
            "row_count": legal["row_count"],
            "rows_sha256": legal["rows_sha256"],
            "overapproximation_safe_direction":
                legal["overapproximation_safe_direction"],
        },
        "PB4_D2": {
            "relation_count": d2["relation_count"],
            "relators_sha256": d2["relators_sha256"],
            "full_translate_count": d2["full_translate_count"],
        },
        "Jennings": {
            "weights": jennings["weights"],
            "full_j_order": jennings["j_order"],
            "fresh_j_order": list(FRESH_J_ORDER),
            "first_terminal_rule": jennings["first_terminal_rule"],
            "basis_manifest": [row for row in jennings["basis_manifest"]
                               if row["j"] in FRESH_J_ORDER],
        },
        "freshness_boundary": v1_static["freshness_boundary"],
    }
    summary["binding_sha256"] = digest_obj(summary)
    return summary


def build_context() -> tuple[Any, dict[str, Any], dict[str, Any],
                             dict[str, Any], dict[str, Any]]:
    v2_pins = v2_pin_inputs()
    prior = authenticate_prior()
    v1 = load_v1()
    v1_static, private = v1.build_static()
    summary = summarize_static(v1_static, v2_pins, prior)
    return v1, summary, private, prior, v2_pins


def checkpoint_filename(j: int) -> str:
    require(j in FRESH_J_ORDER, "checkpoint j")
    return f"d972_r07_760_l3_target6_resume_v2_j{j}.json"


def manifest_for(summary: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(row["j"]): row
            for row in summary["Jennings"]["basis_manifest"]}


def validate_public_row(row: dict[str, Any],
                        summary: dict[str, Any]) -> None:
    require(type(row) is dict and type(row.get("j")) is int and
            row["j"] in FRESH_J_ORDER, "checkpoint row j")
    expected = manifest_for(summary)[row["j"]]
    require(row.get("monomial_count") == expected["monomial_count"] and
            row.get("dim_Lambda_over_Ij") == expected["dim_Lambda_over_Ij"] and
            row.get("basis_sha256") == expected["basis_sha256"],
            "checkpoint row basis")
    dimension = int(row["dim_Lambda_over_Ij"])
    ranks = [row.get("rank_D2bar_alone"),
             row.get("rank_legal_overapproximation"),
             row.get("rank_combined")]
    require(all(type(value) is int and 0 <= value <= dimension
                for value in ranks) and
            ranks[0] <= ranks[2] and ranks[1] <= ranks[2],
            "checkpoint row ranks")
    require(type(row.get("target_projected_sha256")) is str and
            len(row["target_projected_sha256"]) == 64 and
            type(row.get("legal_projected_rows_sha256")) is str and
            len(row["legal_projected_rows_sha256"]) == 64 and
            row.get("PB4_translate_count") == 649539 and
            row.get("producer_D2_algorithm") ==
                "saturated (x_i-1) BFS, D2 first" and
            type(row.get("per_relator_closure_receipts")) is list and
            len(row["per_relator_closure_receipts"]) == 11,
            "checkpoint row algorithm")
    require(type(row.get("nonmember")) is bool, "checkpoint row decision")
    separator = row.get("separator")
    if row["nonmember"]:
        require(type(separator) is dict and
                separator.get("terms_sha256") ==
                    digest_obj(separator.get("terms")) and
                separator.get("support") == len(separator.get("terms", [])),
                "checkpoint separator serialization")
        replay = separator.get("pairing_replay")
        require(type(replay) is dict and
                replay.get("translated_boundary_rows_checked") == 649539 and
                replay.get("translated_boundary_nonzero_pairings") == 0 and
                replay.get("all_generated_rows_annihilated") is True and
                replay.get("target_pairing_nonzero") is True and
                replay.get("direct_all_59049_elements_x_11_relators") is True,
                "checkpoint separator direct replay")
    else:
        require(separator is None, "member row has no separator")


def checkpoint_payload(summary: dict[str, Any], prior: dict[str, Any],
                       progression: Sequence[dict[str, Any]],
                       prior_checkpoint: dict[str, Any] | None) \
        -> dict[str, Any]:
    require(progression, "nonempty checkpoint progression")
    completed = [int(row["j"]) for row in progression]
    require(completed == list(FRESH_J_ORDER[:len(completed)]),
            "checkpoint exact fresh prefix")
    for row in progression:
        validate_public_row(row, summary)
    nonmembers = [row["j"] for row in progression if row["nonmember"]]
    require(len(nonmembers) <= 1 and
            (not nonmembers or nonmembers == [completed[-1]]),
            "checkpoint first terminal")
    next_j = None if nonmembers or completed[-1] == FRESH_J_ORDER[-1] \
        else completed[-1] + 1
    expected_prior = None
    if completed[-1] != START_J:
        require(type(prior_checkpoint) is dict,
                "checkpoint previous binding required")
        expected_prior = prior_checkpoint
    else:
        require(prior_checkpoint is None, "j9 has no previous checkpoint")
    payload = {
        "schema": CHECKPOINT_SCHEMA,
        "mode": "checkpoint",
        "checkpoint_state": CHECKPOINT_STATE,
        "grade": "CANDIDATE",
        "inherited_candidate_prefix": list(INHERITED_PREFIX),
        "inherited_prefix_grade": "producer_control_flow_candidate_only",
        "start_j": START_J,
        "completed_j_prefix": completed,
        "next_j": next_j,
        "first_nonmember_j": nonmembers[0] if nonmembers else None,
        "fresh_j_progression": list(progression),
        "current_j_row_sha256": digest_obj(progression[-1]),
        "prior_checkpoint": expected_prior,
        "static_binding": summary,
        "prior_run_binding": prior,
        "unfinished_j_inferred": False,
        "relator_level_state_serialized": False,
        "claims": claims(),
    }
    payload["self_digest_sha256"] = digest_obj(payload)
    return payload


def validate_checkpoint_data(data: dict[str, Any],
                             summary: dict[str, Any],
                             prior: dict[str, Any]) -> None:
    verify_self_digest(data, "checkpoint")
    require(data.get("schema") == CHECKPOINT_SCHEMA and
            data.get("mode") == "checkpoint" and
            data.get("checkpoint_state") == CHECKPOINT_STATE and
            data.get("grade") == "CANDIDATE",
            "checkpoint envelope")
    require(data.get("inherited_candidate_prefix") ==
                list(INHERITED_PREFIX) and
            data.get("inherited_prefix_grade") ==
                "producer_control_flow_candidate_only" and
            data.get("start_j") == START_J and
            data.get("static_binding") == summary and
            data.get("prior_run_binding") == prior and
            data.get("unfinished_j_inferred") is False and
            data.get("relator_level_state_serialized") is False and
            data.get("claims") == claims(),
            "checkpoint fixed contract")
    progression = data.get("fresh_j_progression")
    require(type(progression) is list and progression,
            "checkpoint progression")
    completed = [row.get("j") for row in progression]
    require(completed == data.get("completed_j_prefix") and
            completed == list(FRESH_J_ORDER[:len(completed)]),
            "checkpoint completed prefix")
    for row in progression:
        validate_public_row(row, summary)
    nonmembers = [row["j"] for row in progression if row["nonmember"]]
    require(len(nonmembers) <= 1 and
            (not nonmembers or nonmembers == [completed[-1]]) and
            data.get("first_nonmember_j") ==
                (nonmembers[0] if nonmembers else None),
            "checkpoint first nonmember")
    expected_next = None if nonmembers or completed[-1] == FRESH_J_ORDER[-1] \
        else completed[-1] + 1
    require(data.get("next_j") == expected_next and
            data.get("current_j_row_sha256") == digest_obj(progression[-1]),
            "checkpoint next/current row")


def read_canonical(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    data = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(data) + b"\n", label + " canonical")
    return data, raw


def checkpoint_record(path: Path, raw: bytes, j: int) -> dict[str, Any]:
    resolved = path.resolve()
    try:
        public_path = resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        public_path = resolved.as_posix()
    return {
        "j": j, "path": public_path, "filename": path.name,
        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
    }


def validate_checkpoint_chain(path: Path,
                              summary: dict[str, Any],
                              prior: dict[str, Any],
                              seen: set[Path] | None = None) \
        -> tuple[dict[str, Any], list[dict[str, Any]]]:
    path = path.resolve()
    seen = set() if seen is None else seen
    require(path not in seen, "checkpoint chain cycle")
    seen.add(path)
    data, raw = read_canonical(path, "checkpoint")
    validate_checkpoint_data(data, summary, prior)
    current_j = data["completed_j_prefix"][-1]
    require(path.name == checkpoint_filename(current_j),
            "checkpoint filename/j")
    record = checkpoint_record(path, raw, current_j)
    previous = data.get("prior_checkpoint")
    if current_j == START_J:
        require(previous is None, "j9 prior checkpoint absent")
        return data, [record]
    require(type(previous) is dict and
            previous.get("j") == current_j - 1 and
            previous.get("filename") == checkpoint_filename(current_j - 1),
            "prior checkpoint adjacency")
    previous_path = path.parent / previous["filename"]
    require(previous_path.is_file() and
            previous_path.stat().st_size == previous.get("bytes") and
            digest_file(previous_path) == previous.get("sha256"),
            "prior checkpoint file binding")
    previous_data, records = validate_checkpoint_chain(
        previous_path, summary, prior, seen)
    require(previous_data["fresh_j_progression"] ==
            data["fresh_j_progression"][:-1],
            "checkpoint cumulative progression chain")
    return data, records + [record]


def validate_output(data: dict[str, Any]) -> None:
    verify_self_digest(data, "v2 output")
    require(data.get("schema") == SCHEMA and data.get("claims") == claims(),
            "v2 output envelope")
    if data.get("mode") == "preflight":
        require(data.get("preflight_state") == PREFLIGHT_STATE and
                "status" not in data and "terminal_token" not in data,
                "claim-free preflight")
        return
    require(data.get("mode") == "full" and
            data.get("terminal_token") in TERMINALS and
            data.get("status") == data.get("terminal_token") and
            data.get("grade") == "CANDIDATE",
            "full terminal envelope")
    result = data.get("result", {})
    require(result.get("state") == data["terminal_token"] and
            result.get("inherited_candidate_prefix") ==
                list(INHERITED_PREFIX) and
            result.get("inherited_prefix_grade") ==
                "producer_control_flow_candidate_only" and
            result.get("start_j") == START_J and
            result.get("unfinished_j_inferred") is False and
            result.get("mathematical_membership_claimed") is False and
            result.get("actual_A18_lift_claimed") is False,
            "full result boundary")


def checked_write(path: Path, data: dict[str, Any]) -> bytes:
    validate_output(data) if data.get("schema") == SCHEMA \
        else verify_self_digest(data, "checkpoint write")
    raw = canonical_bytes(data) + b"\n"
    full = resolve_repo_path(path)
    full.parent.mkdir(parents=True, exist_ok=True)
    if full.exists():
        require(full.read_bytes() == raw, "immutable output mismatch")
    else:
        full.write_bytes(raw)
    require(full.read_bytes() == raw, "checked immutable write")
    return raw


def common_result(progression: Sequence[dict[str, Any]],
                  manifest: Sequence[dict[str, Any]],
                  resume_record: dict[str, Any] | None) -> dict[str, Any]:
    nonmembers = [row["j"] for row in progression if row["nonmember"]]
    return {
        "inherited_candidate_prefix": list(INHERITED_PREFIX),
        "inherited_prefix_grade": "producer_control_flow_candidate_only",
        "start_j": START_J,
        "resume_from_checkpoint": resume_record,
        "fresh_j_order": list(FRESH_J_ORDER),
        "fresh_j_order_tested": [row["j"] for row in progression],
        "first_nonmember_j": nonmembers[0] if nonmembers else None,
        "j_progression": list(progression),
        "checkpoint_manifest": list(manifest),
        "unfinished_j_inferred": False,
        "relator_level_state_serialized": False,
        "mathematical_membership_claimed": False,
        "mathematical_nonmembership_claimed": False,
        "actual_A18_lift_claimed": False,
        "registered_108_family_used": False,
        "literal_A18_computed": False,
        "normalized_Brunnian_class_computed": False,
    }


def base_output(mode: str, summary: dict[str, Any],
                prior: dict[str, Any], v2_pins: dict[str, Any]) \
        -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "mode": mode,
        "grade": "CANDIDATE",
        "static_binding": summary,
        "prior_run_binding": prior,
        "v2_pins": v2_pins,
        "resume_contract": {
            "inherited_candidate_prefix": list(INHERITED_PREFIX),
            "inherited_prefix_grade": "producer_control_flow_candidate_only",
            "start_j": START_J,
            "fresh_j_order": list(FRESH_J_ORDER),
            "interrupted_j_recomputed_from_relator_1": True,
            "checkpoint_after_each_completed_j": True,
            "producer_only_grade": "CANDIDATE",
            "member_is_actual_A18_lift": False,
        },
        "sound_implication": {
            "nonmembership_direction_only": True,
            "membership_is_lift": False,
            "scope": "one explicit g760 prefix, first hexagon coordinate",
        },
        "claims": claims(),
    }


def build_preflight() -> dict[str, Any]:
    _, summary, private, prior, v2_pins = build_context()
    del private
    receipt = base_output("preflight", summary, prior, v2_pins)
    receipt["preflight_state"] = PREFLIGHT_STATE
    receipt["result"] = {"state": "UNBUILT_GHA_ONLY"}
    receipt["checkpoint_contract"] = {
        "schema": CHECKPOINT_SCHEMA,
        "checkpoint_state": CHECKPOINT_STATE,
        "filename_pattern":
            "d972_r07_760_l3_target6_resume_v2_j{j}.json",
        "j_values": list(FRESH_J_ORDER),
        "cumulative_public_rows": True,
        "prior_checkpoint_sha_and_bytes": True,
        "canonical_self_digest": True,
        "relator_level_state_serialized": False,
    }
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def checkpoint_path(directory: Path, j: int) -> Path:
    base = resolve_repo_path(directory)
    return base / checkpoint_filename(j)


def build_full(seconds: float, start_j: int, checkpoint_dir: Path,
               resume_checkpoint: Path | None) -> dict[str, Any]:
    require(start_j == START_J, "only start_j=9 is accepted")
    require(0 < seconds <= MAX_SECONDS, "seconds range")
    v1: Any | None = None
    summary: dict[str, Any] | None = None
    prior: dict[str, Any] | None = None
    v2_pins: dict[str, Any] | None = None
    progression: list[dict[str, Any]] = []
    manifest: list[dict[str, Any]] = []
    resume_record: dict[str, Any] | None = None
    stage = "input_authentication"
    try:
        v1, summary, private, prior, v2_pins = build_context()
        output_directory = resolve_repo_path(checkpoint_dir).resolve()
        output_directory.mkdir(parents=True, exist_ok=True)
        prior_checkpoint_record = None
        if resume_checkpoint is not None:
            resume_path = resolve_repo_path(resume_checkpoint).resolve()
            require(resume_path.parent == output_directory,
                    "resume/checkpoint directory mismatch")
            checkpoint, manifest = validate_checkpoint_chain(
                resume_path, summary, prior)
            require(checkpoint["next_j"] in FRESH_J_ORDER,
                    "terminal checkpoint cannot resume")
            progression = copy.deepcopy(checkpoint["fresh_j_progression"])
            prior_checkpoint_record = manifest[-1]
            resume_record = copy.deepcopy(prior_checkpoint_record)
            next_j = int(checkpoint["next_j"])
        else:
            next_j = START_J
        require(next_j == FRESH_J_ORDER[len(progression)],
                "resume exact next j")
        monitor = v1.Monitor(seconds)
        for j in FRESH_J_ORDER[len(progression):]:
            stage = f"j={j}:start"
            monitor.check(stage, force=True)
            row = v1.compute_j_bfs(private, j, monitor, pairing=True)
            progression.append(row)
            checkpoint_data = checkpoint_payload(
                summary, prior, progression, prior_checkpoint_record)
            path = checkpoint_path(checkpoint_dir, j)
            raw = checked_write(path, checkpoint_data)
            record = checkpoint_record(path, raw, j)
            manifest.append(record)
            prior_checkpoint_record = record
            if row["nonmember"]:
                stage = f"j={j}:fresh-no-state-replay"
                replay = v1.compute_j_bfs(private, j, monitor, pairing=False)
                keys = (
                    "rank_D2bar_alone", "rank_legal_overapproximation",
                    "rank_combined", "target_projected_sha256",
                    "legal_projected_rows_sha256", "nonmember")
                require(all(replay[key] == row[key] for key in keys),
                        "fresh no-state-leak BFS replay")
                break
        nonmembers = [row["j"] for row in progression if row["nonmember"]]
        terminal = ("R07_760_L3_TARGET6_NONMEMBER" if nonmembers else
                    "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE")
        receipt = base_output("full", summary, prior, v2_pins)
        receipt["status"] = terminal
        receipt["terminal_token"] = terminal
        result = common_result(progression, manifest, resume_record)
        result["state"] = terminal
        result["first_terminal_rule_applied"] = True
        receipt["result"] = result
    except BaseException as exc:
        is_resource = v1 is not None and isinstance(exc, v1.ResourceStop)
        terminal = ("R07_760_L3_TARGET6_UNKNOWN_RESOURCE" if is_resource else
                    "R07_760_L3_TARGET6_INPUT_STOP")
        if summary is None or prior is None or v2_pins is None:
            try:
                v2_pins = v2_pins or v2_pin_inputs()
                prior = prior or authenticate_prior()
            except BaseException:
                v2_pins = v2_pins or {}
                prior = prior or {
                    "run_id": PRIOR_RUN_ID,
                    "binding_authenticated": False,
                }
            summary = summary or {
                "full_v1_static_rebuilt": False,
                "base": {
                    "base_kind": "r07_760_commutator", "length": 760,
                    "sha256": BASE_SHA, "parent_616_sha256": PARENT_SHA,
                    "free_exponent_sums": [0, 0],
                },
            }
        receipt = base_output("full", summary, prior, v2_pins)
        receipt["status"] = terminal
        receipt["terminal_token"] = terminal
        result = common_result(progression, manifest, resume_record)
        result.update({
            "state": terminal,
            "stage": getattr(exc, "stage", stage),
            "reason": str(exc),
            "requested_seconds": seconds,
        })
        receipt["result"] = result
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def toy_checkpoint_tests() -> int:
    prior = {"binding_sha256": "a" * 64}
    summary = {
        "Jennings": {"basis_manifest": [{
            "j": 9, "monomial_count": 1,
            "dim_Lambda_over_Ij": 6, "basis_sha256": "b" * 64,
        }]},
    }
    row = {
        "j": 9, "monomial_count": 1, "dim_Lambda_over_Ij": 6,
        "basis_sha256": "b" * 64, "rank_D2bar_alone": 1,
        "rank_legal_overapproximation": 1, "rank_combined": 2,
        "target_projected_sha256": "c" * 64,
        "legal_projected_rows_sha256": "d" * 64,
        "PB4_translate_count": 649539,
        "producer_D2_algorithm": "saturated (x_i-1) BFS, D2 first",
        "per_relator_closure_receipts": [{} for _ in range(11)],
        "nonmember": False, "separator": None,
    }
    good = checkpoint_payload(summary, prior, [row], None)
    validate_checkpoint_data(good, summary, prior)
    mutations = []
    for label, mutate in (
        ("skip_prefix", lambda d: d.update({"completed_j_prefix": [10]})),
        ("wrong_next", lambda d: d.update({"next_j": 11})),
        ("row_basis", lambda d: d["fresh_j_progression"][0].update(
            {"basis_sha256": "0" * 64})),
        ("prior_binding", lambda d: d["prior_run_binding"].update(
            {"binding_sha256": "0" * 64})),
        ("claim_flip", lambda d: d["claims"].update(
            {"ihara_witness": True})),
        ("self_digest", lambda d: d.update(
            {"self_digest_sha256": "0" * 64})),
    ):
        bad = copy.deepcopy(good)
        mutate(bad)
        try:
            validate_checkpoint_data(bad, summary, prior)
        except RuntimeError:
            mutations.append(label)
            continue
        raise RuntimeError("checkpoint mutation survived: " + label)
    require(len(mutations) == 6, "checkpoint mutation count")
    return len(mutations)


def self_test() -> None:
    pins = v2_pin_inputs()
    prior = authenticate_prior()
    v1 = load_v1()
    _, base = v1.construct_base()
    v1.toy_tracker()
    mutations = toy_checkpoint_tests()
    require(len(base) == 760 and prior["next_j"] == START_J and
            len(pins) == len(V2_PIN_SPECS), "v2 selftest contract")
    print(
        "R07_760_L3_TARGET6_RESUME_V2_PRODUCER_SELFTEST_PASS "
        f"prior_artifacts=2 inherited_prefix=7 start_j=9 "
        f"checkpoint_mutations={mutations} relator_state=absent",
        flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seconds", type=float,
                        default=RECOMMENDED_SECONDS)
    parser.add_argument("--start-j", type=int, default=START_J)
    parser.add_argument("--checkpoint-dir", type=Path,
                        default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--resume-checkpoint", type=Path)
    args = parser.parse_args()
    require(sum((args.self_test, args.preflight, args.full)) == 1,
            "select exactly one mode")
    require(args.start_j == START_J, "only --start-j 9 is accepted")
    if args.self_test:
        require(args.resume_checkpoint is None, "selftest cannot resume")
        self_test()
        return 0
    if args.preflight:
        require(args.resume_checkpoint is None, "preflight cannot resume")
        receipt = build_preflight()
        output = args.output or DEFAULT_PREFLIGHT
    else:
        receipt = build_full(
            args.seconds, args.start_j, args.checkpoint_dir,
            args.resume_checkpoint)
        output = args.output or DEFAULT_FULL
    raw = checked_write(output, receipt)
    state_key = "preflight_state" if args.preflight else "terminal_token"
    state_label = "preflight_state" if args.preflight else "terminal"
    checkpoints = 0 if args.preflight else len(
        receipt["result"]["checkpoint_manifest"])
    print(
        FINAL_MARKER + f" {state_label}={receipt[state_key]} "
        f"grade=CANDIDATE checkpoints={checkpoints} "
        f"sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}",
        flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
