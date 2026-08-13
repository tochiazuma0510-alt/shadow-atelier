#!/usr/bin/env python3
"""Independent text-and-integer checker for the Phase-2b preflight."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="search/certs/d972_phase2b_gate_v1_20260813.json")
    parser.add_argument(
        "--output", default="search/certs/d972_phase2b_gate_v1_check_20260813.json"
    )
    args = parser.parse_args()
    source_path = ROOT / args.input
    source = json.loads(source_path.read_text(encoding="utf-8"))
    library = Path(source["candidate"]["library_path"])
    text = library.read_text(encoding="utf-8")
    marker = text[text.index("# 32256.2"):text.index("PERFGRP[73]", text.index("# 32256.2"))]
    checks = {
        "schema": source.get("schema") == "d972_phase2b_gate/v1",
        "library_digest": digest(library) == source["candidate"]["library_sha256"],
        "library_entry": all(token in marker for token in (
            '"L2(8) N 2^6"', '[[a*v*w,c,x]]', '[16,6,2]', '4,72'
        )),
        "orders": (
            source["candidate"]["order"] == 64 * 504 == 32256
            and source["scale"]["source_pure_roof_quotient_order"] == 2916 * 32256
            and source["scale"]["source_full_roof_quotient_order"] == 6 * 2916 * 32256
            and source["scale"]["target_pure_roof_quotient_order"] == 2916 * 504
        ),
        "bounds": (
            source["scale"]["candidate_hexagon_scan_upper_bound"] == 6 * 32256
            and source["scale"]["fixed_quotient_lift_pair_upper_bound"] == 8 * 64
        ),
        "sequence_boundary": (
            not source["measurement_performed"]
            and not source["reduction_image_formed"]
            and source["premeasurement_gates"]["isolatedness_must_be_settled_before_measurement"]
            and source["premeasurement_gates"]["source_shadow_count_must_be_positive_before_measurement"]
        ),
        "noncontact": (
            not source["u_touched"]
            and not source["c_touched"]
            and not source["sealed_k5_touched"]
        ),
    }
    result = {
        "schema": "d972_phase2b_gate_check/v1",
        "checker": "search/check_d972_phase2b_gate_v1.py",
        "helper_disjointness": "independent library slice and integer products; no producer import",
        "source_run_id": source["run_id"],
        "source_sha256": digest(source_path),
        "checks": checks,
        "all_checks_true": all(checks.values()),
    }
    write_json(ROOT / args.output, result)
    print(json.dumps({"all_checks_true": result["all_checks_true"]}, sort_keys=True))
    return 0 if result["all_checks_true"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
