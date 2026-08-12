#!/usr/bin/env python3
"""Build the K=13 T4 pivot artifact from the completed T2/T3 pivot lane.

The source aggregate is the exact same 210 x (3^13+2^13) restricted matrix
over 2147483647 that the cancelled monolithic T4 step1 attempted to rebuild.
The T2/T3 lane already covered all 630 generator-tree shards and retained the
207 pivot ambient positions.  This adapter validates that provenance and only
performs the word-index decoding required by T4 step2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


K = 13
PRIME = 2_147_483_647
H_RANK = 210
DIM_H = 630
R_PRIME = 207
TAG_BOUNDARY = 3**K
AMBIENT_DIM = TAG_BOUNDARY + 2**K


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_word(index: int, alphabet_size: int, degree: int) -> list[int]:
    digits = []
    for _ in range(degree):
        digits.append(index % alphabet_size)
        index //= alphabet_size
    if index:
        raise ValueError("ambient word index exceeds requested degree")
    return list(reversed(digits))


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aggregate-prime", type=Path, required=True)
    parser.add_argument("--aggregate-workflow-run", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    args = parser.parse_args()

    source = json.loads(args.aggregate_prime.read_text(encoding="utf-8"))
    expected = {
        "schema": "tor_sweep_k13_gha_aggregate_prime.1",
        "k": K,
        "prime": PRIME,
        "source_run_id": "31527005518",
        "H_rank": H_RANK,
        "dim_h": DIM_H,
        "rank": R_PRIME,
        "shard_count": 7,
        "n_ambient_dim": TAG_BOUNDARY,
        "ambient_dim_total": AMBIENT_DIM,
    }
    observed = {key: source.get(key) for key in expected}
    if observed != expected:
        raise ValueError(f"aggregate metadata mismatch: {observed!r} != {expected!r}")

    coverage = [tuple(row) for row in source["coverage_ranges"]]
    if coverage != [
        (0, 90),
        (90, 180),
        (180, 270),
        (270, 360),
        (360, 450),
        (450, 540),
        (540, 630),
    ]:
        raise ValueError(f"unexpected tree coverage: {coverage!r}")
    pivots = source["pivot_ambient_row_indices"]
    if len(pivots) != R_PRIME or len(set(pivots)) != R_PRIME:
        raise ValueError("pivot list does not contain 207 distinct positions")
    if not all(0 <= p < AMBIENT_DIM for p in pivots):
        raise ValueError("pivot position outside ambient range")

    decoded = []
    for pos in pivots:
        if pos < TAG_BOUNDARY:
            decoded.append(["n", decode_word(pos, 3, K)])
        else:
            decoded.append(["h", decode_word(pos - TAG_BOUNDARY, 2, K)])

    payload = {
        "schema": "tor_sweep_t4_step1_gha.2",
        "ruling_refs": ["task-114", "T2/T3-shard-reuse"],
        "k": K,
        "H_rank": H_RANK,
        "r_prime": R_PRIME,
        "dim_h": DIM_H,
        "pivot_cert_prime": PRIME,
        "r_check": source["rank"],
        "r_check_matches_r_prime": source["rank"] == R_PRIME,
        "pivot_positions": pivots,
        "tag_boundary": TAG_BOUNDARY,
        "decoded": decoded,
        "reuse_provenance": {
            "aggregate_workflow_run_id": str(args.aggregate_workflow_run),
            "aggregate_source_shard_run_id": source["source_run_id"],
            "aggregate_prime_artifact_sha256": sha256(args.aggregate_prime),
            "shard_receipts": source["shard_receipts"],
            "coverage_ranges": source["coverage_ranges"],
            "identity_note": "same prime, basis, 630-tree sum, restricted matrix, rank routine, and pivot certificate as cancelled T4 step1",
        },
    }
    atomic_json(args.checkpoint, {**payload, "state": "COMPLETE"})
    atomic_json(args.out, payload)
    print(
        "TORSWEEP_T4_STEP1_REUSED_DONE "
        f"k={K} rank={R_PRIME} pivots={len(pivots)}"
    )


if __name__ == "__main__":
    main()
