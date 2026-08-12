#!/usr/bin/env python3
"""FLINT-backed, checkpointed K=13 TOR-DET finalize with QUAR-TOR."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
import time
from math import gcd
from pathlib import Path

from flint import fmpz_mat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
sys.set_int_max_str_digits(0)

from torsweep_k12_run import small_primes  # noqa: E402
from torsweep_t4_finalize_k13_gha import independent_rows_modp  # noqa: E402


K = 13
H_RANK = 210
DIM_H = 630
R_PRIME = 207
PIVOT_PRIME = 2_147_483_647
NUM_MINORS = 5
RNG_SEED = 20260807


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def flint_product(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    product = fmpz_mat(left) * fmpz_mat(right)
    return [
        [int(product[i, j]) for j in range(product.ncols())]
        for i in range(product.nrows())
    ]


def flint_det(rows: list[list[int]]) -> int:
    return int(fmpz_mat(rows).det())


def factor_and_rank(gcd_abs: int, n_source: list[list[int]]) -> dict:
    rem = gcd_abs
    trial_bound = 2_000_000
    factors: dict[int | str, int | str] = {}
    exhausted = True
    for prime in small_primes(trial_bound):
        if prime * prime > rem:
            exhausted = False
            break
        while rem % prime == 0:
            factors[prime] = int(factors.get(prime, 0)) + 1
            rem //= prime
    unresolved = None
    if rem > 1:
        if exhausted:
            import sympy

            sub = sympy.factorint(rem, limit=10_000_000)
            for base, exponent in sub.items():
                base = int(base)
                if base > 10_000_000 and not sympy.isprime(base):
                    unresolved = str(base)
                    factors["UNRESOLVED_COMPOSITE"] = unresolved
                else:
                    factors[base] = int(factors.get(base, 0)) + int(exponent)
        else:
            factors[int(rem)] = int(factors.get(int(rem), 0)) + 1

    jumps = {}
    torsion_primes = []
    for prime in factors:
        if not isinstance(prime, int):
            continue
        rank = len(independent_rows_modp(n_source, prime, list(range(H_RANK))))
        has_jump = rank != R_PRIME
        jumps[str(prime)] = {
            "rank_p": rank,
            "r_prime": R_PRIME,
            "jumps": has_jump,
            "method": "cheap_N_source_rank",
        }
        if has_jump:
            torsion_primes.append(prime)
    return {
        "triggered": True,
        "gcd_abs_prime_factors": {str(key): value for key, value in factors.items()},
        "torsion_primes": torsion_primes,
        "jump_at_p": jumps,
        "unresolved_cofactor": unresolved,
        "factorization_fully_resolved": unresolved is None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step1-artifact", type=Path, required=True)
    parser.add_argument("--step2-a-artifact", type=Path, required=True)
    parser.add_argument("--step2-b-artifact", type=Path, required=True)
    parser.add_argument("--exact-b-cert", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--resume-checkpoint", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    started = time.time()

    paths = {
        "step1": args.step1_artifact,
        "step2_a": args.step2_a_artifact,
        "step2_b": args.step2_b_artifact,
        "exact_b": args.exact_b_cert,
    }
    identity = {name + "_sha256": sha256(path) for name, path in paths.items()}
    state = {
        "schema": "tor_sweep_t4_finalize_k13_checkpoint.2",
        "identity": identity,
        "stage": "INPUTS",
        "n_source": None,
        "minor_determinants": [],
        "minor_row_sets": [],
    }
    if args.resume_checkpoint and args.resume_checkpoint.is_file():
        candidate = json.loads(args.resume_checkpoint.read_text(encoding="utf-8"))
        if candidate.get("schema") != state["schema"] or candidate.get("identity") != identity:
            raise ValueError("finalize resume checkpoint identity mismatch")
        state = candidate
        print(f"resume_stage={state['stage']}", flush=True)

    def checkpoint(stage: str) -> None:
        state["stage"] = stage
        state["elapsed_seconds_this_attempt"] = time.time() - started
        atomic_json(args.checkpoint, state)

    step1 = json.loads(args.step1_artifact.read_text(encoding="utf-8"))
    step2a = json.loads(args.step2_a_artifact.read_text(encoding="utf-8"))
    step2b = json.loads(args.step2_b_artifact.read_text(encoding="utf-8"))
    if (step1["k"], step1["H_rank"], step1["dim_h"], step1["r_prime"]) != (
        K,
        H_RANK,
        DIM_H,
        R_PRIME,
    ):
        raise ValueError("step1 dimensions mismatch")
    if step2a["modulus_label"] != "A" or step2b["modulus_label"] != "B":
        raise ValueError("step2 modulus labels mismatch")
    cols_a = step2a["cols"]
    cols_b = step2b["cols"]
    exact_moduli_agree = cols_a == cols_b
    if not exact_moduli_agree:
        checkpoint("EXACT_MODULI_DISAGREE")
        raise ValueError("exact modulus A/B column matrices disagree")
    checkpoint("EXACT_MODULI_AGREE")

    if state.get("n_source") is None:
        print("loading exact B", flush=True)
        bcert = json.loads(args.exact_b_cert.read_text(encoding="utf-8"))
        if (bcert["H_rank"], bcert["dim_h"]) != (H_RANK, DIM_H):
            raise ValueError("exact B dimensions mismatch")
        print("FLINT fmpz_mat product B*cols", flush=True)
        state["n_source"] = flint_product(bcert["H_basis"], cols_a)
        checkpoint("N_SOURCE_COMPLETE")
    n_source = state["n_source"]

    rng = random.Random(RNG_SEED)
    orders = [list(range(H_RANK))]
    for _ in range(NUM_MINORS + 2):
        order = list(range(H_RANK))
        rng.shuffle(order)
        orders.append(order)
    orders.append(list(reversed(range(H_RANK))))

    seen = {tuple(sorted(row)) for row in state["minor_row_sets"]}
    for order in orders:
        if len(state["minor_determinants"]) >= NUM_MINORS:
            break
        selected = independent_rows_modp(n_source, PIVOT_PRIME, order)
        if len(selected) != R_PRIME:
            continue
        key = tuple(sorted(selected))
        if key in seen:
            continue
        seen.add(key)
        print(
            f"FLINT determinant {len(state['minor_determinants'])+1}/{NUM_MINORS}",
            flush=True,
        )
        determinant = flint_det([n_source[index] for index in selected])
        if determinant == 0:
            continue
        state["minor_determinants"].append(str(determinant))
        state["minor_row_sets"].append(selected)
        checkpoint(f"MINOR_{len(state['minor_determinants'])}_COMPLETE")
    if len(state["minor_determinants"]) < 3:
        raise ValueError("fewer than three nonzero independent minors")

    gcd_abs = 0
    for determinant in state["minor_determinants"]:
        gcd_abs = gcd(gcd_abs, abs(int(determinant)))
    t5 = (
        {"triggered": False, "reason": "gcd_abs == 1"}
        if gcd_abs == 1
        else factor_and_rank(gcd_abs, n_source)
    )
    checkpoint("T5_COMPLETE")

    cert = {
        "schema": "tor_sweep_t4_finalize_k13_gha.2",
        "ruling_refs": ["task-114", "k12-schema", "QUAR-TOR"],
        "k": K,
        "H_rank": H_RANK,
        "r_prime": R_PRIME,
        "pivot_cert_prime": step1["pivot_cert_prime"],
        "exact_modulus_A": step2a["exact_modulus"],
        "exact_modulus_B": step2b["exact_modulus"],
        "exact_moduli_agree": exact_moduli_agree,
        "exact_b_cert_path": str(args.exact_b_cert),
        "exact_b_cert_sha256": identity["exact_b_sha256"],
        "engine": "python-flint fmpz_mat product and determinant",
        "stages": {
            "T4": {
                "N_source_shape": [H_RANK, R_PRIME],
                "N_source": n_source,
                "minor_determinants": state["minor_determinants"],
                "minor_determinant_digit_counts": [
                    len(value.lstrip("-")) for value in state["minor_determinants"]
                ],
                "minor_row_sets": state["minor_row_sets"],
                "gcd_abs": str(gcd_abs),
                "gcd_abs_digits": len(str(gcd_abs)),
            },
            "T5": t5,
        },
        "stop_rules": {
            "S-TOR-4": {"note": "no judgement words; raw values/booleans only"}
        },
        "total_elapsed_seconds_this_attempt": time.time() - started,
    }
    if t5.get("torsion_primes"):
        cert["stop_rules"]["QUAR-TOR"] = {
            "triggered": True,
            "quarantined_primes": t5["torsion_primes"],
            "note": "QUAR-TOR section 5.3 -- commander disposition required",
        }
    atomic_json(args.out, cert)
    state["cert_sha256"] = sha256(args.out)
    checkpoint("COMPLETE")
    print(
        "TORSWEEP_T4_FINALIZE_K13_V2_DONE "
        f"gcd_abs_digits={len(str(gcd_abs))}",
        flush=True,
    )


if __name__ == "__main__":
    main()
