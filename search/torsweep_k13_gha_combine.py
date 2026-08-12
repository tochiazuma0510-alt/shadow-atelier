#!/usr/bin/env python3
"""
torsweep_k13_gha_combine.py -- combines the 3 small per-prime aggregate
JSONs (search/torsweep_k13_gha_aggregate_prime.py output) into the final
T2/T3-shaped cert (裁定808/897). Cheap -- these inputs are KB-scale, not
GB-scale -- runs fine either inside a GHA job or locally after a small
local download of the 3 per-prime aggregate artifacts (裁定897(2):
"local DL は小物のみ").

Checks (same discipline as search/torsweep_k13_shard_aggregate.py's
modq path, which this supersedes as the trusted route for k=13 T2/T3 --
that script's own load/sum path required the huge shard artifacts
locally, which is exactly what 裁定897 moved off of the local machine):
  - ranks_agree across all 3 primes (T-c canary)
  - r_prime == 207, dim_S_Q == H_rank - r_prime == 3 (裁定735(6) frozen
    values; BOTH >3 and <3 are STOP, not just one direction)
"""
import argparse
import json
import os
import sys
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPECTED_H = 210
EXPECTED_S = 3
EXPECTED_RANK_NU = 207


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aggregate", action="append", required=True,
                     help="path to a per-prime aggregate JSON; repeat for each of the 3 primes")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    per_prime = {}
    H_rank = None
    for path in args.aggregate:
        with open(path, "r", encoding="utf-8") as f:
            agg = json.load(f)
        q = str(agg["prime"])
        if H_rank is None:
            H_rank = agg["H_rank"]
        assert agg["H_rank"] == H_rank
        assert agg["k"] == 13
        per_prime[q] = {
            "rank": agg["rank"], "nnz_reconstructed": agg["nnz_reconstructed"],
            "shard_count": agg["shard_count"], "source_run_id": agg["source_run_id"],
            "shard_receipts_sha256": [r["sha256"] for r in agg["shard_receipts"]],
        }
        record(f"loaded {path}: prime={q} rank={agg['rank']} "
               f"shard_count={agg['shard_count']} source_run_id={agg['source_run_id']}")

    assert H_rank == EXPECTED_H, (H_rank, EXPECTED_H)
    if len(per_prime) != 3:
        record(f"WARNING: expected 3 primes, got {len(per_prime)}: {list(per_prime.keys())}")

    ranks = [v["rank"] for v in per_prime.values()]
    ranks_agree = len(ranks) == 3 and len(set(ranks)) == 1
    r_prime = ranks[0] if ranks_agree else None
    dim_S_Q = (H_rank - r_prime) if r_prime is not None else None
    rank_nu_matches = (r_prime == EXPECTED_RANK_NU) if r_prime is not None else False
    dim_S_matches = (dim_S_Q == EXPECTED_S) if dim_S_Q is not None else False

    cert = {
        "schema": "tor_sweep_k13_gha_combine.1",
        "ruling_refs": ["裁定735(6)", "裁定808", "裁定897"],
        "k": 13, "H_rank": H_rank,
        "stages": {
            "T2_T3": {
                "per_prime": per_prime,
                "ranks_agree": ranks_agree,
                "r_prime": r_prime,
                "dim_S_Q_byproduct": dim_S_Q,
                "rank_nu13_matches_expected_207": rank_nu_matches,
                "dim_S13_Q_matches_expected_3": dim_S_matches,
            },
        },
        "canaries": {
            "T-c": {"ranks_by_prime": {q: v["rank"] for q, v in per_prime.items()}, "pass": ranks_agree},
        },
        "stop_rules": {},
    }
    record(f"r_prime={r_prime} dim_S_Q={dim_S_Q} ranks_agree={ranks_agree} "
           f"rank_nu_matches={rank_nu_matches} dim_S_matches={dim_S_matches}")

    if not ranks_agree:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": "LATTICE_CANARY_FAIL (T-c, prime rank disagreement or "
                      "missing coverage for one or more primes)",
        }
    elif not (rank_nu_matches and dim_S_matches):
        cert["stop_rules"]["S-TOR-2"] = {
            "triggered": True,
            "reason": f"branch table (裁定735(6)): r_prime={r_prime} "
                      f"(expected {EXPECTED_RANK_NU}), dim_S_Q={dim_S_Q} "
                      f"(expected {EXPECTED_S}) -- BOTH directions of "
                      f"mismatch are STOP, raw values only",
        }

    cert["stop_rules"]["S-TOR-4"] = {"note": "no judgement words; raw values/booleans only"}
    cert["total_elapsed_seconds"] = time.time() - t_start
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    record(f"DONE. cert written: {args.out}")
    print(f"TORSWEEP_K13_GHA_COMBINE_DONE ranks_agree={ranks_agree} "
          f"r_prime={r_prime} dim_S_Q={dim_S_Q}", flush=True)


if __name__ == "__main__":
    main()
