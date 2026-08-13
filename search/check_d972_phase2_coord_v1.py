#!/usr/bin/env python3
"""Helper-disjoint arithmetic checker for d972_phase2_coord/v1."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def kap(m: int) -> int:
    return m + 1 if m & 1 else -m


def parameter_pairs(n: int) -> set[tuple[int, int]]:
    n_ord = math.lcm(n, 2)
    period = n // math.gcd(n, 2)
    result = set()
    for m in range(n_ord):
        if math.gcd(2 * m + 1, n_ord) != 1:
            continue
        for k in range(period):
            if n % 4 or (k - kap(m) // 2) % 2 == 0:
                result.add((m, k))
    return result


def reduced_pairs(n: int, target_n: int) -> set[tuple[int, int]]:
    target_ord = math.lcm(target_n, 2)
    return {(m % target_ord, k % target_n) for m, k in parameter_pairs(n)}


def roof_raw(n: int) -> int:
    image = set()
    for m, k in parameter_pairs(n):
        reduced = (m % 18, k % 9)
        u = (2 * reduced[0] + 1) % 18
        for translation in range(9):
            image.add((reduced, u, translation))
    return len(image)


def gn_order(n: int) -> int:
    return 4 * n**3 if n & 1 else 4 * (n // 2) ** 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="search/certs/d972_phase2_coord_v1_20260813.json")
    parser.add_argument("--output", default="search/certs/d972_phase2_coord_v1_check_20260813.json")
    args = parser.parse_args()
    source_path = ROOT / args.input
    output_path = ROOT / args.output
    source = json.loads(source_path.read_text(encoding="utf-8"))

    counts = {str(n): len(parameter_pairs(n)) for n in (9, 27, 36, 108)}
    reductions = {
        "27_to_9": len(reduced_pairs(27, 9)),
        "36_to_9": len(reduced_pairs(36, 9)),
        "108_to_27": len(reduced_pairs(108, 27)),
        "108_to_9": len(reduced_pairs(108, 9)),
    }
    raw = [roof_raw(27), roof_raw(108)]
    source_raw = [row["raw_image_size"] for row in source["depths"]]
    group_expected = {str(n): gn_order(n) for n in (9, 27, 36, 108)}
    roof_expected = {str(n): gn_order(n) * 504 for n in (9, 27, 36, 108)}

    checks = {
        "schema": source.get("schema") == "d972_phase2_coord/v1",
        "coordinate_rule_exact": source.get("coordinate_rule") == {
            "m_reduction": "m mod H_ord",
            "legacy_half_modulus_used": False,
        },
        "coordinate_counts": source.get("dihedral_coordinate_counts") == counts,
        "reduction_counts": reductions == {
            "27_to_9": 108,
            "36_to_9": 108,
            "108_to_27": 972,
            "108_to_9": 108,
        },
        "raw_depth_values": source_raw == raw,
        "base_roof_size": source.get("base_roof_size") == 972,
        "nonchain_raw": source.get("nonchain_probe", {}).get("raw_image_size") == roof_raw(36),
        "canonical_group_orders": source["group_order_receipts"]["canonical_gn_orders"] == group_expected,
        "roof_group_orders": source["group_order_receipts"]["roof_orders"] == roof_expected,
        "cumulative_meet_order": source["group_order_receipts"]["marked_product_g27_g36_order"] == gn_order(108),
        "factorization_flag": source["dihedral_reductions"]["factorization_108_27_9_all_coordinates"] is True,
        "noncontact_flags": all(
            source.get(key) is expected
            for key, expected in (
                ("u_touched", False),
                ("c_touched", False),
                ("sealed_k5_touched", False),
                ("prereg_quantities_untouched", True),
            )
        ),
    }
    result = {
        "schema": "d972_phase2_coord_check/v1",
        "source_run_id": source.get("run_id"),
        "checker": "search/check_d972_phase2_coord_v1.py",
        "helper_disjointness": "standard-library (m,k) enumeration; no SymPy permutations and no producer helpers imported",
        "recomputed": {
            "coordinate_counts": counts,
            "reduction_counts": reductions,
            "raw_depth_values": raw,
            "nonchain_raw": roof_raw(36),
            "group_order_formula": group_expected,
            "roof_order_formula": roof_expected,
        },
        "checks": checks,
        "all_checks_true": all(checks.values()),
        "source_sha256": digest(source_path),
        "producer_sha256": digest(ROOT / "search/d972_phase2_coord_v1.py"),
        "u_touched": False,
        "c_touched": False,
    }
    write_json(output_path, result)
    print(json.dumps({"all_checks_true": result["all_checks_true"], "raw": raw}))
    return 0 if result["all_checks_true"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
