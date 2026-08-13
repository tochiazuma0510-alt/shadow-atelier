#!/usr/bin/env python3
"""Helper-disjoint checker for d972_phase2_void/v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEVELS = (9, 27, 36, 45, 54, 63, 72, 81, 108, 126, 135, 162)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def kap(m: int) -> int:
    return m + 1 if m % 2 else -m


def pairs(level: int) -> set[tuple[int, int]]:
    order_modulus = math.lcm(level, 2)
    period = level // math.gcd(level, 2)
    result = set()
    for m in range(order_modulus):
        if math.gcd(2 * m + 1, order_modulus) != 1:
            continue
        for k in range(period):
            if level % 4 or (k - kap(m) // 2) % 2 == 0:
                result.add((m, k))
    return result


def reduced(level: int) -> set[tuple[int, int]]:
    return {(m % 18, k % 9) for m, k in pairs(level)}


def g_order(level: int) -> int:
    return 4 * level**3 if level % 2 else 4 * (level // 2) ** 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="search/certs/d972_phase2_void_v2_20260813.json")
    parser.add_argument(
        "--output", default="search/certs/d972_phase2_void_v2_check_20260813.json"
    )
    args = parser.parse_args()
    source_path = ROOT / args.input
    source = json.loads(source_path.read_text(encoding="utf-8"))

    recomputed = []
    for level in LEVELS:
        domain = pairs(level)
        image = reduced(level)
        recomputed.append({
            "level": level,
            "G_level_order": g_order(level),
            "dihedral_shadow_count": len(domain),
            "dihedral_reduction_image_count": len(image),
            "dihedral_reduction_onto_GT_K9": len(image) == 108,
            "roof_shadow_count": len(domain) * 9,
            "roof_reduction_raw_image_count": len(image) * 9,
        })

    checks = {
        "schema": source.get("schema") == "d972_phase2_void/v2",
        "input_hashes": all(
            digest(ROOT / path) == value for path, value in source["input_sha256"].items()
        ),
        "coordinate_table": source.get("coordinate_table") == recomputed,
        "all_raw_972": all(row["roof_reduction_raw_image_count"] == 972 for row in recomputed),
        "complete_product_logic_recorded": (
            source["complete_product_reason"]["G_l_solvable"]
            and source["complete_product_reason"]["PSL_2_8_nonabelian_simple"]
            and not source["complete_product_reason"]["nontrivial_common_quotient_exists"]
            and "F2/" in source["complete_product_reason"]["F2_corresponding_decomposition"]
        ),
        "model_semantics_disclosed": (
            source["old_phase2_annotation"][
                "producer_and_checker_semantics_same_fibre_product_model"
            ]
            and source["old_phase2_annotation"]["grade_ceiling"]
            == "cross-checked(model-only)"
        ),
        "old_rule_withdrawn": source["old_phase2_annotation"][
            "old_324_stop_branch_withdrawn_for_this_family"
        ],
        "unknown_boundary": (
            source["single_bit_scope"]["status"] == "UNKNOWN"
            and not source["single_bit_scope"]["product_family_can_reach_324"]
            and not source["single_bit_scope"]["finite_depth_B_type_recognition"]
        ),
        "noncontact": (
            not source["scope"]["u_touched"]
            and not source["scope"]["c_touched"]
            and not source["scope"]["sealed_k5_touched"]
            and not source["scope"]["preregistered_quantities_changed"]
        ),
    }
    result = {
        "schema": "d972_phase2_void_check/v2",
        "checker": "search/check_d972_phase2_void_v2.py",
        "helper_disjointness": (
            "stdlib (m,k) pairs; no producer import and no four-coordinate helper"
        ),
        "source_run_id": source.get("run_id"),
        "source_sha256": digest(source_path),
        "checks": checks,
        "all_checks_true": all(checks.values()),
        "recomputed": recomputed,
        "u_touched": False,
        "c_touched": False,
    }
    atomic_json(ROOT / args.output, result)
    print(json.dumps({
        "all_checks_true": result["all_checks_true"],
        "raw_values": sorted({row["roof_reduction_raw_image_count"] for row in recomputed}),
    }, sort_keys=True))
    return 0 if result["all_checks_true"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
