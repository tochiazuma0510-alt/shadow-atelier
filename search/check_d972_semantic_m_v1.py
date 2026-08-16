#!/usr/bin/env python3
"""Independent checker for the finite semantic-M calibration receipt.

The receipt is emitted by the direct-BQ calibration script after GAP has
actually computed the finite orders and Artin/centrality checks. This Python
checker validates the lossless marker, source-script hash, and receipt hash;
it never constructs PB3 or an infinite quotient.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "search" / "d972_semantic_m_manifest_v1.json"
SCHEMA = "d972-semantic-m-bq-receipt/v2"
Q0_ORDER = 1_469_664
BQ_ORDER = 8_817_984


class SemanticMStop(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SemanticMStop("STATE_STOP semantic-M " + message)


def validate_receipt(
    receipt: dict[str, Any], calibration_receipt: dict[str, Any] | None = None,
) -> None:
    require(isinstance(receipt, dict) and receipt.get("schema") == SCHEMA and
            receipt.get("status") == "PASS", "schema/status")
    require(MANIFEST.is_file() and receipt.get("manifest_sha256") == file_sha(MANIFEST),
            "manifest binding")
    body = dict(receipt)
    claimed = body.pop("receipt_sha256", None)
    require(isinstance(claimed, str) and claimed == sha(body), "receipt self-hash")
    marker = receipt.get("raw_marker")
    require(isinstance(marker, list) and len(marker) == 18 and
            all(isinstance(item, str) for item in marker) and
            marker[:1] == ["D972_SEMANTIC_M"] and
            marker[1:7] == ["2916", "504", "1469664", "8817984", "1469664", "6"] and
            all(item == "true" for item in marker[7:]) and
            receipt.get("marker_sha256") == sha(marker),
            "lossless raw marker binding")
    require(receipt.get("source_group") == "PB3" and
            receipt.get("target_group") == "B3/M" and
            receipt.get("pure_target") == "PB3/M", "source/target typing")
    require(receipt.get("presentation") == {
        "generators": ["x12", "x13", "x23"],
        "relators": ["[c,x12]", "[c,x23]"],
        "center_word": "x12*x13*x23",
    }, "standard PB3 presentation")
    require(receipt.get("artin_bridge") == {
        "x12": "s1^2", "x13": "s2*s1^2*s2^-1", "x23": "s2^2",
        "c": "(s1*s2)^3", "replayed": True,
    }, "Artin bridge")
    require(receipt.get("c_word_identity_checked") is True,
            "Artin c-word identity")
    require(receipt.get("k9_pure_order") == 2916 and
            receipt.get("psl28_pure_order") == 504 and
            receipt.get("pure_joint_order") == Q0_ORDER and
            receipt.get("full_bq_order") == BQ_ORDER, "finite order marker")
    require(receipt.get("k9_projection_onto") is True and
            receipt.get("psl28_projection_onto") is True and
            receipt.get("pure_projection_onto") is True and
            receipt.get("s3_quotient_onto") is True, "projection-onto marker")
    require(receipt.get("epsilon_kernel_order") == Q0_ORDER and
            receipt.get("epsilon_index") == 6 and
            receipt.get("kernel_intersection_tautology") is True and
            receipt.get("M_normal_in_PB3") is True and
            receipt.get("M_B3_stable") is True, "kernel/intersection marker")
    for key in (
        "artin_bridge_checked", "center_x12_checked", "center_x23_checked",
        "component_relators_checked", "joint_image_order_checked",
        "epsilon_kernel_checked", "full_order_checked",
        "orientation_canary_checked",
    ):
        require(receipt.get(key) is True, key)
    require(isinstance(receipt.get("marker_sha256"), str) and
            len(receipt["marker_sha256"]) == 64 and
            isinstance(receipt.get("source_q_relators_sha256"), str) and
            len(receipt["source_q_relators_sha256"]) == 64 and
            isinstance(receipt.get("source_target_key_order_sha256"), str) and
            len(receipt["source_target_key_order_sha256"]) == 64 and
            isinstance(receipt.get("source_script_sha256"), str) and
            len(receipt["source_script_sha256"]) == 64 and
            isinstance(receipt.get("source_stdout_sha256"), str) and
            len(receipt["source_stdout_sha256"]) == 64,
            "raw marker/source digests")
    if calibration_receipt is not None:
        require(receipt["source_q_relators_sha256"] ==
                calibration_receipt.get("q_relators_sha256") and
                receipt["source_target_key_order_sha256"] ==
                calibration_receipt.get("target_key_order_sha256") and
                receipt["source_script_sha256"] ==
                calibration_receipt.get("script_sha256") and
                receipt["source_stdout_sha256"] ==
                calibration_receipt.get("stdout_sha256"),
                "source script/q-relator/target binding")
    require(receipt.get("infinite_pb3_api") == "forbidden" and
            receipt.get("order_authority") == "raw finite marker plus self-hashed receipt",
            "infinite API/order authority policy")


def self_test() -> int:
    pending = {"schema": SCHEMA, "status": "PENDING"}
    try:
        validate_receipt(pending)
    except SemanticMStop:
        pass
    else:
        raise AssertionError("pending semantic-M receipt unlocked")
    for key in (
        "artin_bridge", "pure_joint_order", "raw_marker", "k9_projection_onto",
        "orientation_canary_checked", "receipt_sha256",
    ):
        broken = {"schema": SCHEMA, "status": "PASS", key: None}
        try:
            validate_receipt(broken)
        except SemanticMStop:
            pass
        else:
            raise AssertionError(f"semantic-M tamper {key} accepted")
    print(json.dumps({
        "schema": "d972-semantic-m-checker-selftest/v2",
        "status": "PASS",
        "infinite_pb3_construction": "FORBIDDEN",
        "raw_finite_marker_required": True,
        "self_hash_required": True,
        "a_authority_without_receipt": False,
    }, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    require(args.receipt is not None and args.receipt.is_file(), "receipt absent")
    validate_receipt(json.loads(args.receipt.read_text(encoding="utf-8")))
    print("D972_SEMANTIC_M_RECEIPT_PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (SemanticMStop, OSError, json.JSONDecodeError) as exc:
        print(str(exc))
        raise SystemExit(2)
