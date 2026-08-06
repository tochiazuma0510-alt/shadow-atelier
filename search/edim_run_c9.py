#!/usr/bin/env python3
"""
edim_run_c9.py -- (1) regression check: k=7,8 rerun with the LARGE primes
(2147483647, 998244353) required by 裁定658, using the newly-added overflow-
safe matmul (mat_mul_modp_np_safe / mat_vec_modp_np_safe) -- confirms the
overflow fix reproduces the already-known S7=1,H7=6,S8=1,H8=10 (from
search/certs/edim_c78_scoring_v1_20260806.json, computed with SMALL primes)
before trusting the fix for k=9's real run. (2) k=9 real scoring run, dense-
matrix implementation, memory/time recorded.

裁定658 instruction order: regression on k=7/8 with large primes FIRST, THEN
k=9. This script does both, in that order, and stops (no k=10/11 -- those
need the sparse redesign, separate spec+implementation per instruction).
"""
import json
import sys
import time
import tracemalloc

import numpy as np

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed

LARGE_PRIMES = [2147483647, 998244353]

EXPECTED_H = {7: 6, 8: 10, 9: 19}
EXPECTED_S = {7: 1, 8: 1, 9: 1}


def compute_H_S_at_k_safe(k, n_alg, h_alg, D, p):
    """Same computation as edim_run_c78.py's compute_H_S_at_k, but using
    ONLY overflow-safe operations (mat_mul_modp_np_safe / mat_vec_modp_np_
    safe) throughout, and restricting the nu_k accumulation to the h-block
    COLUMNS only (dim_h wide, not the full dim_t) -- both changes needed for
    the large primes / larger k this script targets."""
    dim_n = n_alg.dim[k]
    dim_h = h_alg.dim[k]
    dim_t = dim_n + dim_h

    M_list, dn, dh = ed.build_rho_matrix(k, n_alg, h_alg, D, p)
    assert dn == dim_n and dh == dim_h
    rho = np.array(M_list, dtype=np.int64) % p

    # nu_k restricted to the h-block: start from the dim_t x dim_h matrix
    # [0; I_h] (j embeds L_k into the h-part, n-component 0), apply rho
    # iteratively 4 times, summing I + rho + rho^2 + rho^3 + rho^4 applied
    # to THIS restricted starting matrix only (not the full dim_t x dim_t
    # matrix) -- correctness: nu_k . j = (I+rho+..+rho^4) . j =
    # sum_i rho^i(j(basis)) which is exactly this iterative application.
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


def main():
    tracemalloc.start()
    t_start = time.time()

    print("=== PHASE 1: regression check, k=7,8 with LARGE primes (2147483647, 998244353) ===", flush=True)
    regression = {}
    for p in LARGE_PRIMES:
        print(f"--- prime {p} ---", flush=True)
        regression[p] = run_one_prime(8, p, kmin=7)

    regression_ok = True
    regression_report = {}
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
        print("*** REGRESSION FAILED -- overflow-safe fix does NOT reproduce known k=7,8 values. "
              "STOP, do not proceed to k=9. ***", flush=True)
        out = {"schema": "edim-c9-run/v1", "regression_report": regression_report,
               "regression_ok": False, "k9_result": None}
        with open("search/certs/edim_c9_run_v1_20260806.json", "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        sys.exit(1)

    print("=== regression PASSED -- proceeding to PHASE 2: k=9 real scoring run ===", flush=True)
    k9_results = {}
    for p in LARGE_PRIMES:
        print(f"--- prime {p}, k=9 ---", flush=True)
        r = run_one_prime(9, p, kmin=9)
        k9_results[p] = r[9]

    vals9 = {p: (k9_results[p]["H_dim"], k9_results[p]["S_dim"]) for p in LARGE_PRIMES}
    k9_agree = len(set(vals9.values())) == 1
    h9, s9 = next(iter(vals9.values()))

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    total_elapsed = time.time() - t_start

    calibration_fail = (h9 != EXPECTED_H[9])
    scoring = None
    if not calibration_fail:
        scoring = {"S_measured": s9, "S_predicted": EXPECTED_S[9], "S_match": (s9 == EXPECTED_S[9]),
                   "H_measured": h9, "H_predicted": EXPECTED_H[9], "H_match": True}

    out = {
        "schema": "edim-c9-run/v1",
        "authorization": "docs/notes/b_type_synthesis_design_v1_addendum_edim9_11_prediction.md "
                          "(commit 026dff8, frozen IF-FIRST prediction); 裁定658 (司令塔, this session)",
        "regression_report": regression_report,
        "regression_ok": True,
        "primes": LARGE_PRIMES,
        "k9_results_by_prime": {str(p): k9_results[p] for p in LARGE_PRIMES},
        "k9_two_prime_agree": k9_agree,
        "calibration_fail_H9_mismatch": calibration_fail,
        "scoring": scoring,
        "prediction": {"H": EXPECTED_H[9], "S": EXPECTED_S[9]},
        "total_elapsed_sec": round(total_elapsed, 2),
        "peak_memory_traced_mb": round(peak / (1024 * 1024), 2),
        "k10_k11_not_run": True,
        "note": "k=10,11 deferred pending sparse-representation redesign (dense ambient x basis "
                "matrix for the n-side coordinate solver is ~2.78GB at k=10 and ~22.8GB at k=11 -- "
                "exceeds the 8GB budget at k=11 with the current dense implementation). Design spec "
                "to follow separately per instruction before k=10/11/12 implementation.",
    }
    with open("search/certs/edim_c9_run_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    if calibration_fail:
        print(f"*** CALIBRATION_FAIL: H9 measured={h9} != predicted (derived) {EXPECTED_H[9]} -- "
              f"STOP, NOT reporting S9 ***", flush=True)
        sys.exit(1)

    print("k9 two_prime_agree:", k9_agree)
    print("scoring:", json.dumps(scoring, indent=2))
    print("total_elapsed_sec:", out["total_elapsed_sec"], "peak_memory_traced_mb:", out["peak_memory_traced_mb"])


if __name__ == "__main__":
    main()
