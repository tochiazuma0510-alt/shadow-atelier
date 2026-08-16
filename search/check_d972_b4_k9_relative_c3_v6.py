#!/usr/bin/env python3
"""Independent receipt checker for the v6 explicit-BQ C9 bridge.

It does not import GAP and does not recompute permutation-group row bits.  It
does enforce the distinction that v5 missed: a full marked B3 quotient
``P -> BQ`` must be onto with kernel C9 before a relative pure cell can be
called a below-M candidate.  B4-normality, isolatedness, settledness, the
semantic M binding, and the outside-648 labels remain fail-closed UNKNOWN.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORD_ARTIFACT = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"
CANONICAL_CERT = ROOT / "search" / "certs" / "ihnec_r4b_run_20260801.json"
WORD_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
CANONICAL_SHA = "fdf5fd367cdd00e4aafde4d1ac4ef3708e6f3efd338f7b7945646879e0002fd2"
CANONICAL_ROW_SHA = "e9e1cb711dc700b3588902b7b05f83ae0ca1967983d70d46fc22825b96b0136c"
TARGET_DIGEST = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
TUPLE_DIGEST = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
ARTIFACT_CANONICAL = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
A18_NATIVE = (((1,), (2,), (4,)), ((4,), (5,), (6,)),
              ((2, 4), (3, 5), (6,)), ((1, 2), (3,), (5, 6)),
              ((1,), (2, 3), (4, 5)))
RADIX = [1, 2, 4, 5, 7, 8]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_pin(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(obj.get("rows"), list) and
            all(isinstance(row, list) and len(row) == 3 and
                isinstance(row[0], int) and isinstance(row[2], list)
                for row in obj["rows"]), "artifact row shape [m,key,word]")
    compact = json.dumps(obj["rows"], separators=(",", ":"), ensure_ascii=True)
    return {
        "schema": obj.get("schema"), "count": obj.get("count"),
        "sha256": sha256(path),
        "source_target_key_digest": obj.get("source_target_key_digest"),
        "frozen_tuple_sha256": obj.get("frozen_tuple_sha256"),
        "canonical_bytes_sha256": hashlib.sha256(compact.encode()).hexdigest(),
    }


def validate_cell(cell: dict[str, Any], *, artifact: Path = WORD_ARTIFACT,
                  canonical: Path = CANONICAL_CERT) -> dict[str, Any]:
    require(cell.get("status") == "FINITE_C9_BQ_CELL", "cell status")
    require(cell.get("radix") in RADIX and cell.get("pure_radix") ==
            (2 * cell["radix"]) % 9, "radix")
    require(cell.get("BQ_order") == 8_817_984 and
            cell.get("M_order") == 1_469_664, "finite BQ/M orders")
    require(cell.get("P_order") == 9 * 8_817_984 and
            cell.get("pure_P_order") == 9 * 1_469_664, "extension orders")
    require(cell.get("B3_braid_pass") is True and
            cell.get("marked_images_pass") is True and
            cell.get("P_to_BQ_onto") is True, "marked B3 bridge")
    require(cell.get("P_to_BQ_kernel_order") == 9, "P->BQ kernel is C9")
    require(cell.get("pure_to_M_onto") is True and
            cell.get("pure_to_M_kernel_order") == 9 and
            cell.get("N_le_M") is True, "pure relative kernel/N<=M")
    require(cell.get("N_le_M_proof") == "kernel composition B3_to_P_to_BQ",
            "N<=M proof label")

    require(cell.get("coface_count") == 5 and
            cell.get("coface_relation_pass") is True and
            cell.get("pb3_candidate_relation_pass") is True and
            cell.get("finite_factor_inverse_pass") is True and
            cell.get("coface_inverse_kernel_inclusion") is True and
            cell.get("N_PB3_intersection_exact") is True,
            "five-coface finite kernel equality")
    require(cell.get("center_order") == 3 and cell.get("center_central") is True,
            "C9 centre")

    # This lane must never silently upgrade a finite BQ/pure receipt into a
    # B4 theorem.  The string UNKNOWN is intentional and is checked here.
    for key in ("b4_normality", "isolated", "all_shadows_settled"):
        require(cell.get(key) == "UNKNOWN", f"{key} must remain UNKNOWN")
    require(cell.get("semantic_M_name") == "M=K^(9) intersect N_S4" and
            cell.get("semantic_M_binding_exact") is False,
            "semantic M binding")

    cp = cell.get("canonical_cert")
    require(isinstance(cp, dict) and cp.get("row_count") == 972 and
            cp.get("outside_648_identified") is False and
            cp.get("sha256") == CANONICAL_SHA and
            cp.get("rows_sha256") == CANONICAL_ROW_SHA, "canonical ledger")
    require(canonical.exists() and sha256(canonical) == CANONICAL_SHA,
            "canonical hash")
    src = cell.get("source_word_artifact")
    require(isinstance(src, dict) and src.get("row_count") == 972 and
            src.get("sha256") == WORD_SHA and
            src.get("row_shape") == "[m,key,word]", "word artifact binding")
    require(artifact.exists() and sha256(artifact) == WORD_SHA and
            artifact_pin(artifact) == {
                "schema": "d972-b4-word-key-artifact/v1", "count": 972,
                "sha256": WORD_SHA, "source_target_key_digest": TARGET_DIGEST,
                "frozen_tuple_sha256": TUPLE_DIGEST,
                "canonical_bytes_sha256": ARTIFACT_CANONICAL,
            }, "word artifact pin")

    bridge = cell.get("bridge")
    require(isinstance(bridge, dict) and bridge.get("explicit_BQ") is True and
            bridge.get("kernel_C9") is True and bridge.get("N_le_M") is True and
            bridge.get("terminal_allowed") is False and
            bridge.get("b4_normality") == "UNKNOWN" and
            bridge.get("arithmetic_label") == "UNAVAILABLE_TYPED_ARITHMETIC_BRIDGE" and
            bridge.get("outside_label") == "UNAVAILABLE_TYPED_OUTSIDE_LABEL",
            "bridge fail-closed fields")

    status = cell.get("row_status")
    bits = cell.get("row_bits")
    fails = cell.get("fail_indices")
    if status == "NOT_COMPUTED_BRIDGE_GATE":
        require(bits is None and fails is None and cell.get("zero_fiber_count") is None,
                "uncomputed row nullability")
        require(cell.get("finite_cell_gate") is False, "uncomputed gate")
        zero = 0
    else:
        require(status == "FINITE_C9_ROW_SCAN_NONTERMINAL" and
                cell.get("finite_cell_gate") is True, "row status")
        require(isinstance(bits, list) and len(bits) == 972 and
                all(isinstance(x, bool) for x in bits), "row bits")
        require(isinstance(fails, list) and
                fails == [i + 1 for i, bit in enumerate(bits) if not bit],
                "fail indices")
        require(cell.get("zero_fiber_count") == len(fails), "zero count")
        zero = len(fails)
    return {"zero": zero, "computed": status != "NOT_COMPUTED_BRIDGE_GATE"}


def validate(receipt: dict[str, Any], *, artifact: Path = WORD_ARTIFACT,
             canonical: Path = CANONICAL_CERT) -> dict[str, Any]:
    require(receipt.get("schema") == "d972-b4-k9-relative-c3/v6" and
            receipt.get("status") == "FINITE_C9_BQ_BRIDGE", "top schema/status")
    require(receipt.get("cell") == "d972-k3-c3-exponent-v6" and
            receipt.get("BQ_order") == 8_817_984 and
            receipt.get("M_order") == 1_469_664, "top orders")
    require(receipt.get("radix") == RADIX, "radix universe")
    results = receipt.get("results")
    require(isinstance(results, list) and len(results) == len(RADIX) and
            [r.get("radix") for r in results] == RADIX, "six result cells")
    require(receipt.get("semantic_M_name") == "M=K^(9) intersect N_S4" and
            receipt.get("semantic_M_binding_exact") is False, "top semantic gate")
    frozen = receipt.get("frozen_972")
    require(isinstance(frozen, dict) and frozen.get("row_count") == 972 and
            frozen.get("outside_648_identified") is False and
            frozen.get("canonical_sha256") == CANONICAL_SHA and
            frozen.get("canonical_rows_sha256") == CANONICAL_ROW_SHA and
            frozen.get("word_sha256") == WORD_SHA and
            frozen.get("row_shape") == "[m,key,word]", "top frozen ledger")
    bridge = receipt.get("bridge")
    require(isinstance(bridge, dict) and bridge.get("explicit_BQ") is True and
            bridge.get("kernel_C9_required") is True and
            bridge.get("N_le_M_required") is True and
            bridge.get("terminal_allowed") is False and
            bridge.get("b4_normality") == "UNKNOWN" and
            bridge.get("isolated") == "UNKNOWN" and
            bridge.get("settled") == "UNKNOWN", "top bridge")
    checked = [validate_cell(x, artifact=artifact, canonical=canonical) for x in results]
    zero = sum(x["zero"] for x in checked)
    computed = sum(x["computed"] for x in checked)
    require(receipt.get("zero_fiber_count_total") == zero and
            receipt.get("computed_cells") == computed, "top row totals")
    return {"cells": len(results), "computed_cells": computed,
            "zero_fiber_count_total": zero, "terminal_A_eligible": False,
            "terminal_B_eligible": False}


def fixture() -> dict[str, Any]:
    return {
        "status": "FINITE_C9_BQ_CELL", "radix": 1, "pure_radix": 2,
        "BQ_order": 8_817_984, "M_order": 1_469_664,
        "B3_braid_pass": True, "P_order": 9 * 8_817_984,
        "P_to_BQ_onto": True, "P_to_BQ_kernel_order": 9,
        "marked_images_pass": True, "pure_P_order": 9 * 1_469_664,
        "pure_to_M_onto": True, "pure_to_M_kernel_order": 9,
        "N_le_M": True, "N_le_M_proof": "kernel composition B3_to_P_to_BQ",
        "coface_count": 5, "coface_relation_pass": True,
        "pb3_candidate_relation_pass": True, "finite_factor_inverse_pass": True,
        "coface_inverse_kernel_inclusion": True, "N_PB3_intersection_exact": True,
        "center_order": 3, "center_central": True, "finite_cell_gate": True,
        "row_status": "FINITE_C9_ROW_SCAN_NONTERMINAL", "row_bits": [True] * 972,
        "fail_indices": [], "zero_fiber_count": 0,
        "b4_normality": "UNKNOWN", "isolated": "UNKNOWN",
        "all_shadows_settled": "UNKNOWN",
        "semantic_M_name": "M=K^(9) intersect N_S4", "semantic_M_binding_exact": False,
        "canonical_cert": {"row_count": 972, "outside_648_identified": False,
                            "sha256": CANONICAL_SHA, "rows_sha256": CANONICAL_ROW_SHA},
        "source_word_artifact": {"row_count": 972, "sha256": WORD_SHA,
                                  "row_shape": "[m,key,word]"},
        "bridge": {"explicit_BQ": True, "kernel_C9": True, "N_le_M": True,
                    "b4_normality": "UNKNOWN", "arithmetic_label":
                    "UNAVAILABLE_TYPED_ARITHMETIC_BRIDGE",
                    "outside_label": "UNAVAILABLE_TYPED_OUTSIDE_LABEL",
                    "terminal_allowed": False},
    }


def selftest() -> None:
    require(A18_NATIVE[0] == ((1,), (2,), (4,)), "A.18 canary")
    good = fixture()
    # Fixture uses real repository pins; this exercises all gates.
    validate_cell(good)
    bad = copy.deepcopy(good)
    bad["P_to_BQ_kernel_order"] = 3
    try:
        validate_cell(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError("C3 kernel accepted as C9")
    bad2 = copy.deepcopy(good)
    bad2["b4_normality"] = True
    try:
        validate_cell(bad2)
    except AssertionError:
        pass
    else:
        raise AssertionError("unsafe B4 promotion accepted")
    print("D972_B4_K9_RELATIVE_C3_V6_SELFTEST_PASS",
          {"BQ_order": 8_817_984, "kernel": 9, "rows": 972,
           "terminal": False})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", nargs="?", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return 0
    if args.receipt is None:
        parser.error("receipt path is required unless --selftest is used")
    print("D972_B4_K9_RELATIVE_C3_V6_CHECK_PASS",
          validate(json.loads(args.receipt.read_text(encoding="utf-8"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
