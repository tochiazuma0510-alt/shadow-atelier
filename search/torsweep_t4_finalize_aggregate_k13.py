#!/usr/bin/env python3
"""Aggregate five parallel exact K=13 FLINT minors into the T4/T5 cert."""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
sys.set_int_max_str_digits(0)

from torsweep_t4_finalize_k13_v2_gha import factor_and_rank  # noqa: E402

K = 13
H_RANK = 210
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
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", type=Path, required=True)
    parser.add_argument("--minor-glob", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    prepare = json.loads(args.prepare.read_text(encoding="utf-8"))
    if prepare.get("schema") != "tor_sweep_t4_finalize_k13_prepare.1":
        raise ValueError("prepare schema mismatch")
    prepare_sha = sha256(args.prepare)
    receipts = []
    for name in glob.glob(args.minor_glob, recursive=True):
        payload = json.loads(Path(name).read_text(encoding="utf-8"))
        if payload.get("schema") == "tor_sweep_t4_finalize_k13_minor.1":
            receipts.append(payload)
    receipts.sort(key=lambda row: row["candidate_index"])
    if [row["candidate_index"] for row in receipts] != list(range(5)):
        raise ValueError("minor candidate coverage is not exactly 0..4")
    if any(row["prepare_sha256"] != prepare_sha for row in receipts):
        raise ValueError("minor prepare SHA mismatch")
    row_keys = [tuple(sorted(row["row_set"])) for row in receipts]
    if len(set(row_keys)) != 5:
        raise ValueError("minor row sets are not distinct")
    determinants = [int(row["determinant"]) for row in receipts]
    if any(value == 0 for value in determinants):
        raise ValueError("zero determinant receipt")
    for row, determinant in zip(receipts, determinants):
        if determinant % row["pivot_prime"] != row["determinant_mod_pivot_prime"]:
            raise ValueError("minor modular residue mismatch")

    gcd_abs = 0
    for determinant in determinants:
        gcd_abs = gcd(gcd_abs, abs(determinant))
    n_source = prepare["n_source"]
    t5 = (
        {"triggered": False, "reason": "gcd_abs == 1"}
        if gcd_abs == 1
        else factor_and_rank(gcd_abs, n_source)
    )
    cert = {
        "schema": "tor_sweep_t4_finalize_k13_gha.2",
        "ruling_refs": ["task-114", "k12-schema", "QUAR-TOR"],
        "k": K,
        "H_rank": H_RANK,
        "r_prime": R_PRIME,
        "pivot_cert_prime": prepare["pivot_cert_prime"],
        "exact_modulus_A": prepare["exact_modulus_A"],
        "exact_modulus_B": prepare["exact_modulus_B"],
        "exact_moduli_agree": prepare["exact_moduli_agree"],
        "exact_b_cert_sha256": prepare["current_identity"]["exact_b_sha256"],
        "engine": "five parallel python-flint fmpz_mat determinants",
        "prepare_sha256": prepare_sha,
        "resume": prepare["resume"],
        "stages": {
            "T4": {
                "N_source_shape": [H_RANK, R_PRIME],
                "N_source": n_source,
                "minor_determinants": [str(value) for value in determinants],
                "minor_determinant_digit_counts": [
                    len(str(abs(value))) for value in determinants
                ],
                "minor_row_sets": [row["row_set"] for row in receipts],
                "minor_reused_from_checkpoint": [
                    row["reused_from_authenticated_checkpoint"] for row in receipts
                ],
                "minor_modular_residues": [
                    row["determinant_mod_pivot_prime"] for row in receipts
                ],
                "gcd_abs": str(gcd_abs),
                "gcd_abs_digits": len(str(gcd_abs)),
            },
            "T5": t5,
        },
        "stop_rules": {
            "S-TOR-4": {"note": "no judgement words; raw values/booleans only"}
        },
    }
    if t5.get("torsion_primes"):
        cert["stop_rules"]["QUAR-TOR"] = {
            "triggered": True,
            "quarantined_primes": t5["torsion_primes"],
            "note": "QUAR-TOR section 5.3 -- commander disposition required",
        }
    atomic_json(args.out, cert)
    print(
        "TORSWEEP_T4_FINALIZE_K13_PARALLEL_DONE "
        f"gcd_abs_digits={len(str(gcd_abs))}",
        flush=True,
    )


if __name__ == "__main__":
    main()
