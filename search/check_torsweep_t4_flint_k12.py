#!/usr/bin/env python3
"""Regression anchor: replay completed K=12 T4 determinants with FLINT."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from math import gcd
from pathlib import Path

from flint import fmpz_mat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
sys.set_int_max_str_digits(0)

from torsweep_t4_finalize_k13_gha import independent_rows_modp  # noqa: E402
from torsweep_t4_step1_gha import load_inputs  # noqa: E402


PIVOT_PRIME = 2_147_483_647
RNG_SEED = 20260807
NUM_MINORS = 5


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step1", type=Path, required=True)
    parser.add_argument("--step2-a", type=Path, required=True)
    parser.add_argument("--step2-b", type=Path, required=True)
    parser.add_argument("--reference-final", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    step1 = json.loads(args.step1.read_text(encoding="utf-8"))
    step2a = json.loads(args.step2_a.read_text(encoding="utf-8"))
    step2b = json.loads(args.step2_b.read_text(encoding="utf-8"))
    reference = json.loads(args.reference_final.read_text(encoding="utf-8"))
    if step2a["cols"] != step2b["cols"]:
        raise ValueError("K12 exact moduli disagree")
    _, basis, h_rank, r_prime, dim_h = load_inputs(12)
    if (h_rank, r_prime, dim_h) != (112, 110, 335):
        raise ValueError("K12 committed input dimensions mismatch")

    product = fmpz_mat(basis) * fmpz_mat(step2a["cols"])
    n_source = [
        [int(product[i, j]) for j in range(product.ncols())]
        for i in range(product.nrows())
    ]
    rng = random.Random(RNG_SEED)
    orders = [list(range(h_rank))]
    for _ in range(NUM_MINORS + 2):
        order = list(range(h_rank))
        rng.shuffle(order)
        orders.append(order)
    orders.append(list(reversed(range(h_rank))))
    determinants = []
    row_sets = []
    seen = set()
    for order in orders:
        selected = independent_rows_modp(n_source, PIVOT_PRIME, order)
        if len(selected) != r_prime:
            continue
        key = tuple(sorted(selected))
        if key in seen:
            continue
        seen.add(key)
        determinant = int(fmpz_mat([n_source[index] for index in selected]).det())
        if determinant:
            determinants.append(str(determinant))
            row_sets.append(selected)
        if len(determinants) >= NUM_MINORS:
            break
    gcd_abs = 0
    for determinant in determinants:
        gcd_abs = gcd(gcd_abs, abs(int(determinant)))

    ref_t4 = reference["stages"]["T4"]
    checks = {
        "step1_dimensions": (
            step1["k"], step1["H_rank"], step1["r_prime"], step1["dim_h"]
        )
        == (12, 112, 110, 335),
        "exact_moduli_agree": step2a["cols"] == step2b["cols"],
        "n_source_equal": n_source == ref_t4["N_source"],
        "minor_row_sets_equal": row_sets == ref_t4["minor_row_sets"],
        "minor_determinants_equal": determinants == ref_t4["minor_determinants"],
        "gcd_abs_equal": str(gcd_abs) == ref_t4["gcd_abs"],
        "quar_tor_present_in_reference": "QUAR-TOR" in reference["stop_rules"],
    }
    output = {
        "schema": "torsweep-t4-flint-k12-check/v1",
        "generated_by": "search/check_torsweep_t4_flint_k12.py",
        "source_run_id": "31565199573",
        "source_sha256": {
            "step1": sha256(args.step1),
            "step2_a": sha256(args.step2_a),
            "step2_b": sha256(args.step2_b),
            "reference_final": sha256(args.reference_final),
        },
        "engine": "python-flint fmpz_mat product and determinant",
        "checks": checks,
        "all_checks_true": all(checks.values()),
        "raw": {
            "minor_determinant_digit_counts": [
                len(value.lstrip("-")) for value in determinants
            ],
            "gcd_abs": str(gcd_abs),
            "reference_quarantined_primes": reference["stop_rules"]["QUAR-TOR"][
                "quarantined_primes"
            ],
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"TORSWEEP_T4_FLINT_K12_CHECK_DONE all_checks_true={all(checks.values())}")
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
