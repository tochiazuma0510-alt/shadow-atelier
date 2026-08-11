#!/usr/bin/env python3
"""
torsweep_t4_step1_gha.py -- TOR-DET step 1-2 (pivot AMBIENT column
selection), GHA job-splittable form (裁定876). Parametrized by K so the
SAME code can be run for K=11 as a regression anchor (裁定876(2): "(32,5)
系の回帰アンカー" -- reproduce an ALREADY-KNOWN value exactly before
trusting the new split-job code for K=12) and for K=12 as the actual
target (裁定867/869/870's repeated local-environment deaths of the serial
script motivate this GHA port).

Ported from search/torsweep_k12_v3_t4t5_run.py's step1 (itself ported
from search/torsweep_k11_t4t5_run.py) -- SAME algorithm, split out as its
own entry point so a GHA job can run just this piece (~1.5-1.6h at K=12,
per the local r1 run's own step1 timing of 5758.94s) and upload its
result as an artifact for the next jobs to consume, rather than needing
one long-lived serial process (repeatedly killed by this session's local
environment, 3 occurrences per LEDGER).

Inputs (all small, already-committed certs -- no huge-cert dependency
unlike k=13's HNF construction):
  K=11: search/certs/torsweep_k11_v1_1_20260807.json (T1: M, H_basis;
        T2_T3: r_prime)
  K=12: search/certs/torsweep_k12_v1_20260807.json (T1: M)
      + search/certs/torsweep_k12_v3_hnf_kernel_20260807.json (H_basis)
      + search/certs/torsweep_k12_v3_2_20260811.json (T2_T3: r_prime)

Output artifact: JSON (small -- pivot_positions is a length-r_prime list
of small ints, decoded is likewise small) with r_check, pivot_positions,
tag_boundary, decoded (n/h word tuples), H_rank, r_prime, dim_h -- exactly
what step2/finalize need, nothing large.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
sys.set_int_max_str_digits(0)

import edim_semidirect_v1 as ed  # noqa: E402

PIVOT_CERT_PRIME = 2147483647  # matches both k11/k12 T2/T3's own RANK_PRIMES

K11_CERT = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k11_v1_1_20260807.json")
K12_M_CERT = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k12_v1_20260807.json")
K12_B_CERT = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k12_v3_hnf_kernel_20260807.json")
K12_T23_CERT_GLOB = "torsweep_k12_v3_2_*.json"

EXPECTED = {
    11: {"H_rank": 62, "r_prime": 60, "dim_h": 186},
    12: {"H_rank": 112, "r_prime": 110, "dim_h": 335},
}


def decode_word(idx, alphabet_size, degree):
    digits = []
    tmp = idx
    for _ in range(degree):
        digits.append(tmp % alphabet_size)
        tmp //= alphabet_size
    return tuple(reversed(digits))


def load_inputs(k):
    if k == 11:
        with open(K11_CERT, "r", encoding="utf-8") as f:
            cert = json.load(f)
        M = cert["stages"]["T1"]["M"]
        B = cert["stages"]["T1"]["H_basis"]
        H_rank = cert["stages"]["T1"]["H_rank"]
        r_prime = cert["stages"]["T2_T3"]["r_prime"]
        n_cols = cert["stages"]["T1"]["M_shape"][1]
        return M, B, H_rank, r_prime, n_cols
    elif k == 12:
        with open(K12_M_CERT, "r", encoding="utf-8") as f:
            v1 = json.load(f)
        with open(K12_B_CERT, "r", encoding="utf-8") as f:
            hnf = json.load(f)
        import glob
        t23_candidates = sorted(glob.glob(os.path.join(
            REPO_ROOT, "search", "certs", K12_T23_CERT_GLOB)))
        if not t23_candidates:
            raise FileNotFoundError(K12_T23_CERT_GLOB + " not found")
        with open(t23_candidates[-1], "r", encoding="utf-8") as f:
            t23cert = json.load(f)
        M = v1["stages"]["T1"]["M"]
        n_cols = v1["stages"]["T1"]["M_shape"][1]
        B = hnf["H_basis"]
        H_rank = hnf["H_rank"]
        assert hnf["stages"]["verification_battery_all_pass"] is True
        r_prime = t23cert["stages"]["T2_T3"]["r_prime"]
        assert t23cert["canaries"]["T-c"]["pass"] is True
        return M, B, H_rank, r_prime, n_cols
    else:
        raise ValueError(f"unsupported k={k} (only 11 [regression anchor] "
                          f"and 12 [target] are wired up)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, required=True, choices=[11, 12])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    K = args.k

    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    M, B, H_rank, r_prime, n_cols = load_inputs(K)
    exp = EXPECTED[K]
    assert H_rank == exp["H_rank"] and r_prime == exp["r_prime"] and n_cols == exp["dim_h"], \
        (H_rank, r_prime, n_cols, exp)
    record(f"K={K}: loaded H_rank={H_rank} r_prime={r_prime} dim_h={n_cols}")

    record("step1: rank_nu_j_on_subspace_ambient (one prime) for pivot columns")
    h_alg2_piv = ed.GradedLie(2, K, PIVOT_CERT_PRIME)
    subspace_basis_modq = np.array(
        [[v % PIVOT_CERT_PRIME for v in row] for row in B], dtype=np.int64).T
    r_check = ed.rank_nu_j_on_subspace_ambient(
        K, h_alg2_piv, subspace_basis_modq, PIVOT_CERT_PRIME)
    piv_cert = h_alg2_piv._last_nu_rank_certificate
    elapsed = time.time() - t_start
    record(f"step1: r_check={r_check} (expect {r_prime}) elapsed={elapsed:.2f}s")

    payload = {
        "schema": "tor_sweep_t4_step1_gha.1",
        "ruling_refs": ["裁定876"],
        "k": K,
        "H_rank": H_rank, "r_prime": r_prime, "dim_h": n_cols,
        "pivot_cert_prime": PIVOT_CERT_PRIME,
        "r_check": int(r_check),
        "r_check_matches_r_prime": (r_check == r_prime),
        "elapsed_seconds": elapsed,
    }

    if r_check != r_prime:
        payload["stop"] = "S-TOR-2: pivot-certificate rank regression"
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        record("STOP: pivot rank regression -- see artifact")
        print("TORSWEEP_T4_STEP1_STOP", flush=True)
        sys.exit(1)

    pivot_positions = piv_cert["pivot_ambient_row_indices"]
    tag_boundary = piv_cert["row_encoding"]["tag_boundary"]
    assert len(pivot_positions) == r_prime

    decoded = []
    for pos in pivot_positions:
        if pos < tag_boundary:
            decoded.append(["n", list(decode_word(pos, 3, K))])
        else:
            decoded.append(["h", list(decode_word(pos - tag_boundary, 2, K))])

    payload["pivot_positions"] = pivot_positions
    payload["tag_boundary"] = tag_boundary
    payload["decoded"] = decoded

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    record(f"artifact written: {args.out} ({os.path.getsize(args.out)} bytes)")
    print(f"TORSWEEP_T4_STEP1_DONE k={K} r_check={r_check} elapsed={elapsed:.2f}", flush=True)


if __name__ == "__main__":
    main()
