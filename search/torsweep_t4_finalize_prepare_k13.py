#!/usr/bin/env python3
"""Prepare and authenticate the shared exact K=13 N_source matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

from flint import fmpz_mat

sys.set_int_max_str_digits(0)

K = 13
H_RANK = 210
DIM_H = 630
R_PRIME = 207


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cols_digest(cols: list[list[int]]) -> str:
    encoded = json.dumps(cols, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def validate_step2(a: dict, b: dict) -> None:
    if (a.get("k"), a.get("dim_h"), a.get("r_prime")) != (
        K,
        DIM_H,
        R_PRIME,
    ):
        raise ValueError("step2 A dimensions mismatch")
    if (b.get("k"), b.get("dim_h"), b.get("r_prime")) != (
        K,
        DIM_H,
        R_PRIME,
    ):
        raise ValueError("step2 B dimensions mismatch")
    if a.get("modulus_label") != "A" or b.get("modulus_label") != "B":
        raise ValueError("step2 modulus labels mismatch")
    if a["cols"] != b["cols"]:
        raise ValueError("exact modulus A/B column matrices disagree")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step1-artifact", type=Path, required=True)
    parser.add_argument("--step2-a-artifact", type=Path, required=True)
    parser.add_argument("--step2-b-artifact", type=Path, required=True)
    parser.add_argument("--exact-b-cert", type=Path, required=True)
    parser.add_argument("--resume-checkpoint", type=Path)
    parser.add_argument("--resume-step2-a-artifact", type=Path)
    parser.add_argument("--resume-step2-b-artifact", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    step1 = load(args.step1_artifact)
    a = load(args.step2_a_artifact)
    b = load(args.step2_b_artifact)
    basis = load(args.exact_b_cert)
    if (step1.get("k"), step1.get("H_rank"), step1.get("dim_h"), step1.get("r_prime")) != (
        K,
        H_RANK,
        DIM_H,
        R_PRIME,
    ):
        raise ValueError("step1 dimensions mismatch")
    validate_step2(a, b)
    if (basis.get("H_rank"), basis.get("dim_h")) != (H_RANK, DIM_H):
        raise ValueError("exact B dimensions mismatch")

    current_identity = {
        "step1_sha256": sha256(args.step1_artifact),
        "step2_a_sha256": sha256(args.step2_a_artifact),
        "step2_b_sha256": sha256(args.step2_b_artifact),
        "exact_b_sha256": sha256(args.exact_b_cert),
    }
    current_cols_sha = cols_digest(a["cols"])
    n_source = None
    existing_determinants: list[str] = []
    existing_row_sets: list[list[int]] = []
    resume = {
        "requested": args.resume_checkpoint is not None,
        "accepted": False,
        "checkpoint_sha256": None,
        "checkpoint_stage": None,
        "checkpoint_identity": None,
    }

    if args.resume_checkpoint and args.resume_checkpoint.is_file():
        if not args.resume_step2_a_artifact or not args.resume_step2_b_artifact:
            raise ValueError("resume checkpoint requires its source step2 artifacts")
        checkpoint = load(args.resume_checkpoint)
        old_a = load(args.resume_step2_a_artifact)
        old_b = load(args.resume_step2_b_artifact)
        validate_step2(old_a, old_b)
        if old_a["cols"] != a["cols"]:
            raise ValueError("current and resume exact columns differ")
        old_identity = {
            "step1_sha256": current_identity["step1_sha256"],
            "step2_a_sha256": sha256(args.resume_step2_a_artifact),
            "step2_b_sha256": sha256(args.resume_step2_b_artifact),
            "exact_b_sha256": current_identity["exact_b_sha256"],
        }
        if checkpoint.get("schema") != "tor_sweep_t4_finalize_k13_checkpoint.2":
            raise ValueError("resume checkpoint schema mismatch")
        if checkpoint.get("identity") != old_identity:
            raise ValueError("resume checkpoint file identity mismatch")
        n_source = checkpoint.get("n_source")
        if not n_source:
            raise ValueError("resume checkpoint has no N_source")
        existing_determinants = checkpoint.get("minor_determinants", [])
        existing_row_sets = checkpoint.get("minor_row_sets", [])
        if len(existing_determinants) != len(existing_row_sets):
            raise ValueError("resume minor receipt lengths differ")
        resume.update(
            {
                "accepted": True,
                "checkpoint_sha256": sha256(args.resume_checkpoint),
                "checkpoint_stage": checkpoint.get("stage"),
                "checkpoint_identity": checkpoint.get("identity"),
            }
        )

    if n_source is None:
        print("FLINT fmpz_mat product B*cols", flush=True)
        product = fmpz_mat(basis["H_basis"]) * fmpz_mat(a["cols"])
        n_source = [
            [int(product[i, j]) for j in range(product.ncols())]
            for i in range(product.nrows())
        ]
    if len(n_source) != H_RANK or any(len(row) != R_PRIME for row in n_source):
        raise ValueError("N_source shape mismatch")

    payload = {
        "schema": "tor_sweep_t4_finalize_k13_prepare.1",
        "ruling_refs": ["task-114", "parallel-FLINT-minors"],
        "k": K,
        "H_rank": H_RANK,
        "dim_h": DIM_H,
        "r_prime": R_PRIME,
        "pivot_cert_prime": step1["pivot_cert_prime"],
        "exact_modulus_A": a["exact_modulus"],
        "exact_modulus_B": b["exact_modulus"],
        "exact_moduli_agree": True,
        "current_identity": current_identity,
        "exact_columns_sha256": current_cols_sha,
        "resume": resume,
        "existing_minor_determinants": existing_determinants,
        "existing_minor_row_sets": existing_row_sets,
        "n_source": n_source,
    }
    atomic_json(args.out, payload)
    print(
        "TORSWEEP_T4_FINALIZE_PREPARE_K13_DONE "
        f"resume_accepted={resume['accepted']} existing_minors={len(existing_determinants)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
