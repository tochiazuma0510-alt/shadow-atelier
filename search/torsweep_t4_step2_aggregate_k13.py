#!/usr/bin/env python3
"""Assemble checkpointed K=13 exact-column shards into canonical A/B files."""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
from pathlib import Path


K = 13
DIM_H = 630
R_PRIME = 207
MODULI = {"A": 10**40, "B": 10**40 + 15}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-glob", required=True)
    parser.add_argument("--modulus-label", choices=("A", "B"), required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    paths = [Path(path) for path in sorted(glob.glob(args.shard_glob, recursive=True))]
    if not paths:
        raise FileNotFoundError(args.shard_glob)
    by_index: dict[int, list[int]] = {}
    receipts = []
    ranges = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema") != "tor_sweep_t4_step2_shard_k13_gha.1":
            continue
        identity = payload["identity"]
        if identity["modulus_label"] != args.modulus_label:
            continue
        ranges.append((identity["tree_start"], identity["tree_end"]))
        for index, row in payload["rows"]:
            if index in by_index:
                raise ValueError(f"duplicate tree row {index}")
            if len(row) != R_PRIME:
                raise ValueError(f"tree row {index} has wrong width")
            by_index[index] = row
        receipts.append(
            {
                "path": path.as_posix(),
                "sha256": sha256(path),
                "tree_start": identity["tree_start"],
                "tree_end": identity["tree_end"],
            }
        )
    if sorted(by_index) != list(range(DIM_H)):
        missing = sorted(set(range(DIM_H)) - set(by_index))
        raise ValueError(f"incomplete tree coverage; missing={missing[:20]}")
    ranges.sort()
    cursor = 0
    for start, end in ranges:
        if start != cursor:
            raise ValueError(f"range gap/overlap at {cursor}: {(start, end)}")
        cursor = end
    if cursor != DIM_H:
        raise ValueError(f"range coverage ended at {cursor}")

    payload = {
        "schema": "tor_sweep_t4_step2_gha.2",
        "k": K,
        "modulus_label": args.modulus_label,
        "exact_modulus": str(MODULI[args.modulus_label]),
        "dim_h": DIM_H,
        "r_prime": R_PRIME,
        "cols": [by_index[index] for index in range(DIM_H)],
        "shard_receipts": receipts,
        "coverage_ranges": ranges,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload) + "\n", encoding="utf-8")
    print(
        "TORSWEEP_T4_STEP2_AGGREGATE_DONE "
        f"label={args.modulus_label} shards={len(receipts)} rows={DIM_H}"
    )


if __name__ == "__main__":
    main()
