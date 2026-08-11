#!/usr/bin/env python3
"""
torsweep_k13_materialize_modq_basis.py -- reduce H_13's basis B (from the
LOCAL-ONLY full HNF construction cert, ~356MB, entries to ~9720 digits,
NOT committed to git per 裁定842(2)) mod each of the T2/T3 modq primes,
producing SMALL, COMMITTABLE per-prime files (裁定842(5)).

WHY THIS IS NEEDED (architecture gap this script closes): torsweep-k13.yml
originally had modq_shard jobs read --hnf-cert directly from the checked-
out repo -- but the full HNF cert is git-ignored (裁定842(2), GitHub's
100MB/file push limit), so a GHA runner's actions/checkout would NOT have
that file available. Materializing small mod-q-reduced basis files here
(entries bounded < q, ~10 digits each for the commissioned primes -- 210x
630 matrix, ~1-2MB per prime) lets those files be committed and read
directly by GHA runners without ever needing the huge source cert there.

Output: search/certs/torsweep_k13_basis_modq/torsweep_k13_B_modq_<prime>_
<date>.json, one per prime in MODQ_PRIMES (matches torsweep-k13.yml's
default modq_primes input, 裁定789(2a): all 3 self-computed at k=13, no
ritual reuse).

Usage: python search/torsweep_k13_materialize_modq_basis.py [--hnf-cert PATH]
"""
import argparse
import glob
import hashlib
import json
import os
import sys
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)

K = 13
EXPECTED_H = 210
EXPECTED_DIM_H = 630
MODQ_PRIMES = [2147483647, 998244353, 1000000007]  # matches torsweep-k13.yml default modq_primes
OUT_DIR = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k13_basis_modq")


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def find_latest_hnf_cert():
    candidates = sorted(glob.glob(os.path.join(
        REPO_ROOT, "search", "certs", "torsweep_k13_hnf_construct_v1_*.json")))
    candidates = [c for c in candidates if not c.endswith("_RECEIPT.json")]
    if not candidates:
        raise FileNotFoundError(
            "no torsweep_k13_hnf_construct_v1_*.json (non-receipt) cert "
            "found locally -- this script needs the LOCAL full cert (not "
            "committed, 裁定842(2)) to materialize mod-q reductions from")
    return candidates[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hnf-cert", default=None)
    args = ap.parse_args()

    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    hnf_cert_path = args.hnf_cert or find_latest_hnf_cert()
    record(f"loading {hnf_cert_path}")
    with open(hnf_cert_path, "r", encoding="utf-8") as f:
        hnf = json.load(f)

    assert hnf["stages"]["verification_battery_all_pass"] is True, \
        "refusing to materialize mod-q basis from an HNF cert that did not pass its own battery"
    B = hnf["H_basis"]
    H_rank = hnf["H_rank"]
    dim_h = hnf["dim_h"]
    assert H_rank == EXPECTED_H and dim_h == EXPECTED_DIM_H, (H_rank, dim_h)
    assert len(B) == H_rank and len(B[0]) == dim_h
    record(f"loaded H_rank={H_rank} dim_h={dim_h}")

    src_sha256 = sha256_of_file(hnf_cert_path)
    record(f"source cert sha256={src_sha256}")

    os.makedirs(OUT_DIR, exist_ok=True)
    date_str = time.strftime("%Y%m%d")
    written = []
    for q in MODQ_PRIMES:
        record(f"reducing B mod {q}")
        B_modq = [[v % q for v in row] for row in B]
        max_entry_digits = max(len(str(v)) for row in B_modq for v in row)
        payload = {
            "schema": "tor_sweep_k13_basis_modq.1",
            "ruling_refs": ["裁定789", "裁定790", "裁定792", "裁定842(5)"],
            "k": K,
            "prime": q,
            "H_rank": H_rank,
            "dim_h": dim_h,
            "B_modq": B_modq,
            "source_hnf_cert_path": os.path.relpath(hnf_cert_path, REPO_ROOT).replace(os.sep, "/"),
            "source_hnf_cert_sha256": src_sha256,
            "note": "B_modq[i][j] = H_basis[i][j] mod prime, entries in "
                    "[0,prime) -- small/committable, generated so GHA "
                    "modq_shard jobs do not need the full (git-ignored, "
                    "356MB, 裁定842(2)) HNF cert checked out on the runner.",
            "max_entry_digit_count": max_entry_digits,
        }
        out_path = os.path.join(OUT_DIR, f"torsweep_k13_B_modq_{q}_{date_str}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)
        size = os.path.getsize(out_path)
        record(f"wrote {out_path} ({size} bytes, max_entry_digits={max_entry_digits})")
        written.append((out_path, size))

    record("DONE")
    for path, size in written:
        print(f"TORSWEEP_K13_MODQ_BASIS_WRITTEN path={path} bytes={size}")


if __name__ == "__main__":
    main()
