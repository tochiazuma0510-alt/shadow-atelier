#!/usr/bin/env python3
"""Compute one deterministic K=13 exact minor in a parallel FLINT job."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
from pathlib import Path

from flint import fmpz_mat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
sys.set_int_max_str_digits(0)

from torsweep_t4_finalize_k13_gha import independent_rows_modp  # noqa: E402

H_RANK = 210
R_PRIME = 207
PIVOT_PRIME = 2_147_483_647
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


def candidate_order(index: int) -> list[int]:
    if index == 0:
        return list(range(H_RANK))
    rng = random.Random(RNG_SEED)
    order = None
    for _ in range(index):
        order = list(range(H_RANK))
        rng.shuffle(order)
    assert order is not None
    return order


def determinant_mod_prime(rows: list[list[int]], prime: int) -> int:
    matrix = [[value % prime for value in row] for row in rows]
    determinant = 1
    for column in range(len(matrix)):
        pivot = next(
            (row for row in range(column, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            determinant = -determinant
        value = matrix[column][column]
        determinant = determinant * value % prime
        inverse = pow(value, -1, prime)
        for row in range(column + 1, len(matrix)):
            factor = matrix[row][column] * inverse % prime
            if not factor:
                continue
            matrix[row][column:] = [
                (a - factor * b) % prime
                for a, b in zip(matrix[row][column:], matrix[column][column:])
            ]
    return determinant % prime


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", type=Path, required=True)
    parser.add_argument("--candidate-index", type=int, choices=range(5), required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    prepare = json.loads(args.prepare.read_text(encoding="utf-8"))
    if prepare.get("schema") != "tor_sweep_t4_finalize_k13_prepare.1":
        raise ValueError("prepare schema mismatch")
    n_source = prepare["n_source"]
    selected = independent_rows_modp(
        n_source, PIVOT_PRIME, candidate_order(args.candidate_index)
    )
    if len(selected) != R_PRIME:
        raise ValueError("candidate row set is not full rank at pivot prime")
    key = tuple(sorted(selected))
    determinant = None
    reused = False
    for rows, value in zip(
        prepare.get("existing_minor_row_sets", []),
        prepare.get("existing_minor_determinants", []),
    ):
        if tuple(sorted(rows)) == key:
            determinant = int(value)
            reused = True
            break
    matrix = [n_source[index] for index in selected]
    modular = determinant_mod_prime(matrix, PIVOT_PRIME)
    if modular == 0:
        raise ValueError("selected minor vanished at the pivot prime")
    if determinant is None:
        print(f"FLINT determinant candidate={args.candidate_index}", flush=True)
        determinant = int(fmpz_mat(matrix).det())
    if determinant % PIVOT_PRIME != modular:
        raise ValueError("exact determinant disagrees with independent modular elimination")

    payload = {
        "schema": "tor_sweep_t4_finalize_k13_minor.1",
        "candidate_index": args.candidate_index,
        "prepare_sha256": sha256(args.prepare),
        "row_set": selected,
        "determinant": str(determinant),
        "determinant_digits": len(str(abs(determinant))),
        "pivot_prime": PIVOT_PRIME,
        "determinant_mod_pivot_prime": modular,
        "reused_from_authenticated_checkpoint": reused,
    }
    atomic_json(args.out, payload)
    print(
        "TORSWEEP_T4_FINALIZE_MINOR_K13_DONE "
        f"candidate={args.candidate_index} reused={reused} digits={payload['determinant_digits']}",
        flush=True,
    )


if __name__ == "__main__":
    main()
