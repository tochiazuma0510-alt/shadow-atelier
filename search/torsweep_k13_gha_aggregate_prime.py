#!/usr/bin/env python3
"""
torsweep_k13_gha_aggregate_prime.py -- per-prime k=13 T2/T3 shard
aggregation, RUNS INSIDE A GHA JOB (裁定808/897). Downloads that prime's
modq shard artifacts from a (possibly different) source workflow run ONE
AT A TIME via `gh run download --name`, folds each into a running dense
(H_rank x ambient_dim_total) array, then DELETES the downloaded file
before fetching the next -- peak local (runner) disk usage is bounded by
a small constant number of shard files (~1-1.2GB each, per the real
artifact sizes measured in run 31527005518/31537900578), never the whole
~7.7GB/prime pile at once. This is the direct fix for local bulk download
failing with repeated `wsarecv: An existing connection was forcibly
closed by the remote host` resets (裁定897(4)'s diagnosis: same machine/
connection would fail identically for the coordinator too -- the runner's
GitHub-internal network path is the actual fix, not a different puller).

Output: a SMALL (KB-scale, not GB-scale) per-prime aggregate JSON --
just the rank certificate result and shard receipts (name/sha256/size/
tree-range), NOT the reconstructed dense/sparse matrix itself. This is
what makes "artifact 化するのは小型成果物のみ" (裁定897 requirement 2)
possible: the big pile stays in GHA artifact storage, never leaves it.

Usage (inside a GHA job, GH_TOKEN/GITHUB_TOKEN must be set in env for
`gh` to authenticate against this repo):
  python search/torsweep_k13_gha_aggregate_prime.py \
      --run-id 31527005518 --prime 2147483647 \
      --out ci/out/aggregate_prime_2147483647.json
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
sys.set_int_max_str_digits(0)

import edim_semidirect_v1 as ed  # noqa: E402

K = 13
H_RANK = 210
DIM_H = 630
N_AMBIENT_DIM = 3 ** K
H_AMBIENT_DIM = 2 ** K
AMBIENT_DIM_TOTAL = N_AMBIENT_DIM + H_AMBIENT_DIM


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def gh(*args, cwd=None):
    result = subprocess.run(["gh", *args], cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {result.stderr}")
    return result.stdout


def list_shard_artifact_names(run_id, prime):
    out = gh("api", f"repos/{{owner}}/{{repo}}/actions/runs/{run_id}/artifacts",
              "--paginate", "--jq", ".artifacts[].name")
    names = [n for n in out.splitlines() if n]
    pattern_suffix = f"_p{prime}-artifact"
    matched = [n for n in names if n.startswith("torsweep-k13-modq-") and n.endswith(pattern_suffix)]
    return sorted(matched)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True, help="source workflow run id holding this prime's shard artifacts")
    ap.add_argument("--prime", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tmp-dir", default=None, help="scratch dir for sequential per-shard download (deleted after each shard)")
    args = ap.parse_args()
    p = args.prime

    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    tmp_dir = args.tmp_dir or os.path.join(REPO_ROOT, "ci", "tmp_shard_dl")
    os.makedirs(tmp_dir, exist_ok=True)

    record(f"listing shard artifacts for run {args.run_id}, prime {p}")
    artifact_names = list_shard_artifact_names(args.run_id, p)
    if not artifact_names:
        raise RuntimeError(f"no torsweep-k13-modq-*_p{p}-artifact artifacts found in run {args.run_id}")
    record(f"found {len(artifact_names)} shard artifacts: {artifact_names}")

    dense = np.zeros((H_RANK, AMBIENT_DIM_TOTAL), dtype=np.int64)
    receipts = []
    coverage = []
    for name in artifact_names:
        t_shard0 = time.time()
        record(f"downloading {name}")
        # sequential, ONE artifact at a time -- runner disk stays bounded
        gh("run", "download", args.run_id, "--name", name, "--dir", tmp_dir)
        downloaded = [f for f in os.listdir(tmp_dir) if f.endswith(".npz")]
        if len(downloaded) != 1:
            raise RuntimeError(f"expected exactly 1 .npz in {tmp_dir} after downloading "
                                f"{name}, found {downloaded}")
        npz_path = os.path.join(tmp_dir, downloaded[0])
        digest = sha256_of_file(npz_path)
        size = os.path.getsize(npz_path)
        record(f"  downloaded {downloaded[0]} ({size} bytes), sha256={digest}")

        with np.load(npz_path, allow_pickle=True) as npz:
            meta = json.loads(str(npz["meta"]))
            assert meta["k"] == K and meta["mode"] == "modq" and int(meta["modulus"]) == p
            rows = npz["rows"].astype(np.int64)
            cols = npz["cols"].astype(np.int64)
            vals = npz["vals"].astype(np.int64)
        np.add.at(dense, (rows, cols), vals)
        coverage.append((meta["tree_start"], meta["tree_end"]))
        receipts.append({
            "artifact_name": name, "file_name": downloaded[0],
            "sha256": digest, "size_bytes": size,
            "tree_start": meta["tree_start"], "tree_end": meta["tree_end"],
            "nnz": meta["nnz"],
        })

        # delete BEFORE fetching the next shard -- keeps peak disk usage
        # to ~1 shard, not the whole per-prime pile (裁定897(1))
        shutil.rmtree(tmp_dir)
        os.makedirs(tmp_dir, exist_ok=True)
        record(f"  folded and deleted, elapsed_this_shard={time.time()-t_shard0:.2f}s")

    dense %= p

    # coverage check: union of [tree_start,tree_end) ranges == [0,630) exactly
    coverage.sort()
    cursor = 0
    for a, b in coverage:
        if a != cursor:
            raise ValueError(f"coverage gap/overlap: expected next tree_start={cursor}, got {a}")
        cursor = b
    if cursor != DIM_H:
        raise ValueError(f"coverage incomplete: covered up to {cursor}, need {DIM_H}")
    record(f"coverage OK: {len(coverage)} shards cover [0,{DIM_H})")

    nnz_reconstructed = int(np.count_nonzero(dense))
    rank, rank_cert = ed.rank_dense_restricted_ambient_modp(
        dense, p, tag_boundary=N_AMBIENT_DIM)
    record(f"rank={rank} nnz_reconstructed={nnz_reconstructed}")

    payload = {
        "schema": "tor_sweep_k13_gha_aggregate_prime.1",
        "ruling_refs": ["裁定808", "裁定897"],
        "k": K, "prime": p, "source_run_id": args.run_id,
        "H_rank": H_RANK, "dim_h": DIM_H,
        "n_ambient_dim": N_AMBIENT_DIM, "ambient_dim_total": AMBIENT_DIM_TOTAL,
        "rank": int(rank),
        "nnz_reconstructed": nnz_reconstructed,
        "shard_count": len(artifact_names),
        "shard_receipts": receipts,
        "coverage_ranges": coverage,
        "pivot_ambient_row_indices": rank_cert.get("pivot_ambient_row_indices"),
        "elapsed_seconds": time.time() - t_start,
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    size_out = os.path.getsize(args.out)
    record(f"aggregate written: {args.out} ({size_out} bytes)")
    print(f"TORSWEEP_K13_GHA_AGGREGATE_PRIME_DONE prime={p} rank={rank} "
          f"shard_count={len(artifact_names)} out_bytes={size_out}", flush=True)


if __name__ == "__main__":
    main()
