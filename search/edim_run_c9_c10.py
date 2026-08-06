#!/usr/bin/env python3
"""
edim_run_c9_c10.py -- GHA-hosted run (16GB standard runner, per 司令塔裁定
this session: local 8GB machine is being kept clear of EDIM's GAP-adjacent
congestion; this workload is pure python/numpy, no GAP). Order (per 裁定658,
reiterated for GHA):

  PHASE 1: regression check -- k=7,8 rerun with the LARGE primes
    (2147483647, 998244353) required by 裁定658, using the overflow-safe
    matmul fix, confirming reproduction of the already-known S7=1,H7=6,
    S8=1,H8=10 (from search/certs/edim_c78_scoring_v1_20260806.json, which
    used small primes). STOP if this fails -- do not trust the fix for k=9/10.

  PHASE 2: k=9 real scoring run (dense-matrix implementation; measured
    ~0.34GB for the n-side coordinate solver locally, well within a 16GB
    runner).

  PHASE 3: k=10 real scoring run (dense-matrix implementation; measured
    ~2.78GB for the n-side coordinate solver -- comfortable on a 16GB
    runner, would have been risky on the 8GB local machine, hence the GHA
    move).

k=11 is NOT run here (dense n-side solver ~22.8GB, exceeds even a 16GB
runner -- needs the sparse redesign, tracked separately). k=12 likewise not
run (separate 691 workstream, also needs the sparse redesign on a 16GB
runner: dim t_12=44,555, 3^12=531,441 ambient words on the n-side).

Frozen predictions (verbatim authority, commit 026dff8): docs/notes/
b_type_synthesis_design_v1_addendum_edim9_11_prediction.md --
  H9=19 (derived, CALIBRATION_FAIL/STOP if wrong), S9=1 (scored)
  H10=33 (derived, CALIBRATION_FAIL/STOP if wrong), S10=1 (scored)
"""
import json
import sys
import time
import tracemalloc

import numpy as np

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed

LARGE_PRIMES = [2147483647, 998244353]

EXPECTED_H = {7: 6, 8: 10, 9: 19, 10: 33}
EXPECTED_S = {7: 1, 8: 1, 9: 1, 10: 1}


def compute_H_S_at_k_safe(k, n_alg, h_alg, D, p):
    dim_n = n_alg.dim[k]
    dim_h = h_alg.dim[k]
    dim_t = dim_n + dim_h

    M_list, dn, dh = ed.build_rho_matrix(k, n_alg, h_alg, D, p)
    assert dn == dim_n and dh == dim_h
    rho = np.array(M_list, dtype=np.int64) % p

    j_embed = np.zeros((dim_t, dim_h), dtype=np.int64)
    j_embed[dim_n:dim_n + dim_h, :] = np.eye(dim_h, dtype=np.int64)
    nu_j = j_embed.copy()
    cur = j_embed.copy()
    for i in range(1, 5):
        cur = ed.mat_mul_modp_np_safe(rho, cur, p)
        nu_j = (nu_j + cur) % p

    theta = np.array(ed.build_theta_tau_matrix(k, h_alg, 'theta', p), dtype=np.int64) % p
    tau = np.array(ed.build_theta_tau_matrix(k, h_alg, 'tau', p), dtype=np.int64) % p
    I_h = np.eye(dim_h, dtype=np.int64)
    one_plus_theta = (I_h + theta) % p
    tau2 = ed.mat_mul_modp_np_safe(tau, tau, p)
    one_plus_tau_tau2 = (I_h + tau + tau2) % p

    H_stack = np.concatenate([one_plus_theta, one_plus_tau_tau2], axis=0)
    H_dim = dim_h - ed.rank_modp_np(H_stack, p)

    S_stack = np.concatenate([one_plus_theta, one_plus_tau_tau2, nu_j], axis=0)
    S_dim = dim_h - ed.rank_modp_np(S_stack, p)

    return H_dim, S_dim, dim_n, dim_h, dim_t


def run_one_prime(kmax, p, kmin=3):
    t0 = time.time()
    n_alg = ed.GradedLie(3, kmax, p)
    h_alg = ed.GradedLie(2, kmax, p)
    D = ed.build_delta_table(n_alg, h_alg, kmax, p)
    t_build = time.time() - t0
    out = {"_build_elapsed_sec": round(t_build, 3)}
    for k in range(kmin, kmax + 1):
        tk0 = time.time()
        H_dim, S_dim, dim_n, dim_h, dim_t = compute_H_S_at_k_safe(k, n_alg, h_alg, D, p)
        out[k] = {"H_dim": H_dim, "S_dim": S_dim, "dim_n": dim_n, "dim_h": dim_h,
                   "dim_t": dim_t, "elapsed_sec": round(time.time() - tk0, 3)}
        print(f"  p={p} k={k}: H_dim={H_dim} S_dim={S_dim} dim_t={dim_t} "
              f"elapsed={out[k]['elapsed_sec']}s", flush=True)
    return out


def write_stop_cert(payload):
    with open("search/certs/edim_c9_c10_run_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def main():
    tracemalloc.start()
    t_start = time.time()

    print("=== PHASE 1: regression check, k=7,8 with LARGE primes ===", flush=True)
    regression = {}
    for p in LARGE_PRIMES:
        print(f"--- prime {p} ---", flush=True)
        regression[p] = run_one_prime(8, p, kmin=7)

    regression_report = {}
    regression_ok = True
    for k in (7, 8):
        vals = {p: (regression[p][k]["H_dim"], regression[p][k]["S_dim"]) for p in LARGE_PRIMES}
        agree = len(set(vals.values())) == 1
        h0, s0 = next(iter(vals.values()))
        matches_known = (h0 == EXPECTED_H[k] and s0 == EXPECTED_S[k])
        regression_report[k] = {"per_prime": {str(p): vals[p] for p in LARGE_PRIMES},
                                 "two_prime_agree": agree, "matches_prior_small_prime_result": matches_known}
        if not (agree and matches_known):
            regression_ok = False

    print("regression_report:", json.dumps(regression_report, indent=2), flush=True)
    if not regression_ok:
        print("*** REGRESSION FAILED -- STOP, do not proceed to k=9/10 ***", flush=True)
        write_stop_cert({"schema": "edim-c9-c10-run/v1", "regression_report": regression_report,
                         "regression_ok": False, "k9_result": None, "k10_result": None})
        sys.exit(1)

    print("=== regression PASSED -- PHASE 2: k=9 ===", flush=True)
    k9_results = {}
    for p in LARGE_PRIMES:
        r = run_one_prime(9, p, kmin=9)
        k9_results[p] = r[9]
    vals9 = {p: (k9_results[p]["H_dim"], k9_results[p]["S_dim"]) for p in LARGE_PRIMES}
    k9_agree = len(set(vals9.values())) == 1
    h9, s9 = next(iter(vals9.values()))
    k9_calibration_fail = (h9 != EXPECTED_H[9])

    if k9_calibration_fail:
        print(f"*** k=9 CALIBRATION_FAIL: H9={h9} != predicted {EXPECTED_H[9]} -- STOP before k=10 ***", flush=True)
        write_stop_cert({
            "schema": "edim-c9-c10-run/v1", "regression_report": regression_report, "regression_ok": True,
            "k9_results_by_prime": {str(p): k9_results[p] for p in LARGE_PRIMES},
            "k9_two_prime_agree": k9_agree, "k9_calibration_fail_H9_mismatch": True,
            "k9_scoring": None, "k10_result": None,
        })
        sys.exit(1)

    k9_scoring = {"S_measured": s9, "S_predicted": EXPECTED_S[9], "S_match": (s9 == EXPECTED_S[9]),
                  "H_measured": h9, "H_predicted": EXPECTED_H[9], "H_match": True}
    print("k9_scoring:", json.dumps(k9_scoring, indent=2), flush=True)

    print("=== PHASE 3: k=10 ===", flush=True)
    k10_results = {}
    for p in LARGE_PRIMES:
        r = run_one_prime(10, p, kmin=10)
        k10_results[p] = r[10]
    vals10 = {p: (k10_results[p]["H_dim"], k10_results[p]["S_dim"]) for p in LARGE_PRIMES}
    k10_agree = len(set(vals10.values())) == 1
    h10, s10 = next(iter(vals10.values()))
    k10_calibration_fail = (h10 != EXPECTED_H[10])

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    total_elapsed = time.time() - t_start

    k10_scoring = None
    if not k10_calibration_fail:
        k10_scoring = {"S_measured": s10, "S_predicted": EXPECTED_S[10], "S_match": (s10 == EXPECTED_S[10]),
                       "H_measured": h10, "H_predicted": EXPECTED_H[10], "H_match": True}

    out = {
        "schema": "edim-c9-c10-run/v1",
        "authorization": "docs/notes/b_type_synthesis_design_v1_addendum_edim9_11_prediction.md "
                          "(commit 026dff8, frozen IF-FIRST prediction); 裁定658 (司令塔, this session), "
                          "GHA relocation per 司令塔裁定 (16GB runner, EDIM moved off local 8GB machine)",
        "environment": "GitHub Actions ubuntu-latest (16GB RAM per 司令塔裁定; pure python/numpy, no GAP)",
        "regression_report": regression_report,
        "regression_ok": True,
        "primes": LARGE_PRIMES,
        "k9_results_by_prime": {str(p): k9_results[p] for p in LARGE_PRIMES},
        "k9_two_prime_agree": k9_agree,
        "k9_calibration_fail_H9_mismatch": False,
        "k9_scoring": k9_scoring,
        "k10_results_by_prime": {str(p): k10_results[p] for p in LARGE_PRIMES},
        "k10_two_prime_agree": k10_agree,
        "k10_calibration_fail_H10_mismatch": k10_calibration_fail,
        "k10_scoring": k10_scoring,
        "total_elapsed_sec": round(total_elapsed, 2),
        "peak_memory_traced_mb": round(peak / (1024 * 1024), 2),
        "k11_k12_not_run": True,
        "note": "k=11,12 deferred pending sparse-representation redesign (dense ambient x basis "
                "matrix for the n-side coordinate solver is ~22.8GB at k=11, exceeding even a 16GB "
                "runner; k=12 is larger still, 3^12=531441 ambient words). Design spec to follow "
                "separately per instruction.",
    }
    write_stop_cert(out)

    if k10_calibration_fail:
        print(f"*** k=10 CALIBRATION_FAIL: H10={h10} != predicted {EXPECTED_H[10]} -- "
              f"STOP, NOT reporting S10 ***", flush=True)
        sys.exit(1)

    print("k10_scoring:", json.dumps(k10_scoring, indent=2))
    print("total_elapsed_sec:", out["total_elapsed_sec"], "peak_memory_traced_mb:", out["peak_memory_traced_mb"])
    print("EDIM_C9_C10_RUN_DONE")


if __name__ == "__main__":
    main()
