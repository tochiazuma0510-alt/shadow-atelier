#!/usr/bin/env python3
"""Versioned PH2-VOID receipt for the dihedral x PSL(2,8) family.

Only exact integer coordinates from Thm. 4.3 are enumerated.  The old
Phase-2 certificate is bound as history, not used as a mathematical input.
No local Kummer payload is read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEVELS = (9, 27, 36, 45, 54, 63, 72, 81, 108, 126, 135, 162)


def sha256(path: Path) -> str:
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


def kappa(m: int) -> int:
    return m + 1 if m & 1 else -m


def gt_dih(level: int) -> set[tuple[int, int, int, int]]:
    order_modulus = math.lcm(level, 2)
    k_period = level // math.gcd(level, 2)
    rows: set[tuple[int, int, int, int]] = set()
    for m in range(order_modulus):
        if math.gcd(2 * m + 1, order_modulus) != 1:
            continue
        kap = kappa(m)
        for k in range(k_period):
            if level % 4 == 0 and (k - kap // 2) % 2:
                continue
            rows.add((m, 2 * k % level, -2 * k % level, kap % level))
    return rows


def reduce_to_9(row: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    m, a, b, c = row
    return (m % 18, a % 9, b % 9, c % 9)


def group_order(level: int) -> int:
    return 4 * level**3 if level & 1 else 4 * (level // 2) ** 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="search/certs/d972_phase2_void_v2_20260813.json")
    parser.add_argument(
        "--checkpoint", default="search/certs/d972_phase2_void_v2_checkpoint.json"
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "d972_phase2_void_checkpoint/v2",
        "stage": "start",
        "complete": False,
    }
    atomic_json(checkpoint, state)

    def watchdog() -> None:
        time.sleep(args.hard_timeout_seconds)
        if not state.get("complete"):
            state.update(stage="hard_timeout", elapsed_ms=int(1000 * (time.monotonic() - started)))
            atomic_json(checkpoint, state)
            os._exit(124)

    threading.Thread(target=watchdog, daemon=True).start()
    try:
        target = gt_dih(9)
        table: list[dict[str, object]] = []
        for level in LEVELS:
            source = gt_dih(level)
            image = {reduce_to_9(row) for row in source}
            table.append({
                "level": level,
                "G_level_order": group_order(level),
                "dihedral_shadow_count": len(source),
                "dihedral_reduction_image_count": len(image),
                "dihedral_reduction_onto_GT_K9": image == target,
                "roof_shadow_count": len(source) * 9,
                "roof_reduction_raw_image_count": len(image) * 9,
            })
        state.update(stage="coordinate_table", rows=len(table))
        atomic_json(checkpoint, state)

        old_cert = ROOT / "search/certs/d972_phase2_coord_v1_20260813.json"
        old_check = ROOT / "search/certs/d972_phase2_coord_v1_check_20260813.json"
        paths = (
            ROOT / "docs/notes/c1p5_closure_review_v1.md",
            old_cert,
            old_check,
            ROOT / "search/d972_phase2_coord_v1.py",
            ROOT / "search/check_d972_phase2_coord_v1.py",
        )
        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        cert = {
            "schema": "d972_phase2_void/v2",
            "run_id": f"d972-phase2-void-v2-{now}",
            "generated_by": {
                "script": "search/d972_phase2_void_v2.py",
                "tool": "Python 3.13 standard library",
            },
            "scope": {
                "family": "K^(l) intersection N_S4 with 9 dividing l",
                "u_touched": False,
                "c_touched": False,
                "sealed_k5_touched": False,
                "preregistered_quantities_changed": False,
            },
            "PH2_VOID": {
                "statement": (
                    "for every admissible l, raw image size equals the dihedral reduction "
                    "image size times the constant S4 fibre size 9"
                ),
                "constant_S4_fibre_size": 9,
                "target_dihedral_shadow_count": len(target),
                "all_enumerated_reductions_onto": all(
                    row["dihedral_reduction_onto_GT_K9"] for row in table
                ),
                "all_enumerated_raw_images_972": all(
                    row["roof_reduction_raw_image_count"] == 972 for row in table
                ),
                "paper_extension_to_all_admissible_levels": (
                    "Thm. 4.3 gives surjectivity of the dihedral reduction; the fibre count "
                    "then gives 108*9"
                ),
            },
            "complete_product_reason": {
                "G_l_solvable": True,
                "PSL_2_8_nonabelian_simple": True,
                "nontrivial_common_quotient_exists": False,
                "goursat_conclusion": (
                    "PB3/(K^(l) intersection N_S4) is G_l direct-product PSL(2,8)"
                ),
                "F2_corresponding_decomposition": (
                    "F2/((F2 intersection K^(l)) intersection (F2 intersection N_S4)) "
                    "is the direct product of its two factor quotients; the central factor "
                    "of PB3=F2 x <c> is killed by both kernels"
                ),
            },
            "coordinate_table": table,
            "old_phase2_annotation": {
                "producer_and_checker_helpers_shared": False,
                "producer_and_checker_semantics_same_fibre_product_model": True,
                "grade_ceiling": "cross-checked(model-only)",
                "old_324_stop_branch_withdrawn_for_this_family": True,
                "old_972_values_role": "theorem rederivation",
                "P_PH2_1_level_81_role": "theorem rederivation, not a predictive datum",
                "old_phase1_cert_bound_as_history_not_as_support": True,
            },
            "single_bit_scope": {
                "product_family_can_reach_324": False,
                "product_family_decides_A_or_B": False,
                "status": "UNKNOWN",
                "finite_depth_B_type_recognition": False,
            },
            "input_sha256": {
                str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path) for path in paths
            },
            "elapsed_ms": int(1000 * (time.monotonic() - started)),
        }
        atomic_json(output, cert)
        state.update(
            stage="complete",
            complete=True,
            output=str(output.relative_to(ROOT)).replace("\\", "/"),
            run_id=cert["run_id"],
            elapsed_ms=cert["elapsed_ms"],
        )
        atomic_json(checkpoint, state)
        print(json.dumps({
            "run_id": cert["run_id"],
            "levels": len(table),
            "raw_values": sorted({row["roof_reduction_raw_image_count"] for row in table}),
        }, sort_keys=True))
        return 0
    except Exception as exc:
        state.update(
            stage="error", error=repr(exc), elapsed_ms=int(1000 * (time.monotonic() - started))
        )
        atomic_json(checkpoint, state)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
