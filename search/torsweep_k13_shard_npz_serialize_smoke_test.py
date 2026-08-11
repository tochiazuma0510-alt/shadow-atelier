#!/usr/bin/env python3
"""
torsweep_k13_shard_npz_serialize_smoke_test.py -- synthetic nnz~10^8
serialization smoke test for the 裁定867(2) npz fix, run LOCALLY before
any GHA re-dispatch (裁定867(4) explicit requirement: "合成nnz10^8級の
シリアライズ単体テストをローカルで1回通してから請求すること").

Does NOT run the real tree-evaluation (accumulate_nu_j_restricted_range)
-- that part of the pipeline was NOT what OOM'd run 31515932255 (its own
logs show "shard done, elapsed=...s" printing successfully before the
kill; the crash was in the POST-processing: np.nonzero extraction +
Python-list-of-int + json.dump(gzip) serialization). This script instead
builds a SYNTHETIC dense array with realistic shape (H_rank=210,
ambient_dim_total=3**13+2**13=1602515) and nnz density matched to the
90-tree-shard measurement from that run's own earlier successful smoke
test scaled up (5 trees -> nnz=6,716,452, i.e. ~1.343M/tree; 90 trees ->
~120.9M, density ~35.9% of the 210x1602515=336,528,150 cell space -- NOT
a sparse regime in the traditional <1% sense, which is exactly why the
old Python-object-per-entry format was so costly), then exercises the
EXACT extraction+serialization code path (search/torsweep_k13_shard_eval.
py's sparse_arrays_from_dense + np.savez_compressed) that crashed, with
RSS sampled at each stage boundary via psutil.

Usage: python search/torsweep_k13_shard_npz_serialize_smoke_test.py
"""
import gc
import os
import sys
import time

import numpy as np
import psutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
import torsweep_k13_shard_eval as shard_eval  # noqa: E402

H_RANK = 210
AMBIENT_DIM_TOTAL = 3 ** 13 + 2 ** 13  # 1,602,515
PRIME = 2147483647  # a commissioned modq prime, matches run 31515932255
TARGET_DENSITY = 120_896_100 / (H_RANK * AMBIENT_DIM_TOTAL)  # ~90-tree extrapolation
OUT_PATH = os.path.join(REPO_ROOT, "scratchpad", "torsweep", "smoke_test_shard.npz")

proc = psutil.Process(os.getpid())


def rss_mb():
    return proc.memory_info().rss / (1024 * 1024)


def main():
    t0 = time.time()
    print(f"[{time.time()-t0:6.1f}s] start, RSS={rss_mb():.0f}MB "
          f"target_density={TARGET_DENSITY:.4f} "
          f"(H_rank={H_RANK}, ambient_dim_total={AMBIENT_DIM_TOTAL}, "
          f"cells={H_RANK*AMBIENT_DIM_TOTAL:,})")

    rng = np.random.default_rng(20260812)
    dense = np.zeros((H_RANK, AMBIENT_DIM_TOTAL), dtype=np.int64)
    print(f"[{time.time()-t0:6.1f}s] dense array allocated, RSS={rss_mb():.0f}MB "
          f"(nbytes={dense.nbytes/1e9:.2f}GB)")

    mask = rng.random(dense.shape) < TARGET_DENSITY
    nnz_target = int(mask.sum())
    print(f"[{time.time()-t0:6.1f}s] mask built, RSS={rss_mb():.0f}MB "
          f"nnz_target={nnz_target:,}")

    dense[mask] = rng.integers(1, PRIME, size=nnz_target, dtype=np.int64)
    del mask
    gc.collect()
    print(f"[{time.time()-t0:6.1f}s] dense populated (mask freed), "
          f"RSS={rss_mb():.0f}MB")

    # ---- exact extraction path from torsweep_k13_shard_eval.py ----
    t_extract0 = time.time()
    rows, cols, vals = shard_eval.sparse_arrays_from_dense(dense, "modq", PRIME)
    nnz = len(vals)
    t_extract = time.time() - t_extract0
    print(f"[{time.time()-t0:6.1f}s] sparse_arrays_from_dense done "
          f"(elapsed={t_extract:.2f}s), RSS={rss_mb():.0f}MB nnz={nnz:,} "
          f"(target was {nnz_target:,})")
    assert nnz == nnz_target, (nnz, nnz_target)
    assert rows.dtype == np.int32 and cols.dtype == np.int32 and vals.dtype == np.int32

    del dense
    gc.collect()
    print(f"[{time.time()-t0:6.1f}s] dense array freed, RSS={rss_mb():.0f}MB "
          f"(peak RSS before this point is the number that matters -- "
          f"GHA runner had ~15GB total per 'free -h' in run 31515932255's logs)")

    # ---- exact write path ----
    t_write0 = time.time()
    meta = {"schema": "smoke-test", "nnz": nnz}
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    np.savez_compressed(OUT_PATH, rows=rows, cols=cols, vals=vals,
                         meta=np.array("smoke-test-meta"))
    t_write = time.time() - t_write0
    size_mb = os.path.getsize(OUT_PATH) / (1024 * 1024)
    print(f"[{time.time()-t0:6.1f}s] npz written (elapsed={t_write:.2f}s), "
          f"RSS={rss_mb():.0f}MB, file_size={size_mb:.1f}MB")

    # ---- reload + verify round-trip ----
    t_reload0 = time.time()
    with np.load(OUT_PATH, allow_pickle=True) as npz:
        rows2, cols2, vals2 = npz["rows"], npz["cols"], npz["vals"]
    t_reload = time.time() - t_reload0
    assert len(rows2) == nnz and len(cols2) == nnz and len(vals2) == nnz
    print(f"[{time.time()-t0:6.1f}s] reload+verify OK (elapsed={t_reload:.2f}s), "
          f"RSS={rss_mb():.0f}MB")

    os.remove(OUT_PATH)
    total = time.time() - t0
    print(f"[{time.time()-t0:6.1f}s] DONE. total_elapsed={total:.2f}s "
          f"nnz={nnz:,} extract_seconds={t_extract:.2f} "
          f"write_seconds={t_write:.2f} reload_seconds={t_reload:.2f} "
          f"final_file_size_MB={size_mb:.1f}")


if __name__ == "__main__":
    main()
