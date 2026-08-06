#!/usr/bin/env python3
"""
edim_run_c9_c10_v2.py -- v2 driver using the SPARSE solver (docs/notes/
edim_sparse_solver_design_v1.md, approved 裁定660) after the dense v1 driver
(edim_run_c9_c10.py) timed out on GHA at k=9/10 (both runs 31074225133 /
31074224863 hit the 60-minute job ceiling with NO cert produced -- the dense
ambient x basis_dim inversion at k=10 (basis_dim=5880) combined with the
large-prime-safe matvec was too slow).

Local validation before this driver was written (regression discipline,
same spirit as v1's own internal regression phase):
  - k<=6: sparse solver reproduces the dense solver's H/S dims EXACTLY
    (H=1,1,2,3 / S=1,0,1,0 for k=3..6) -- see search/edim_sparse_regression_
    test.py.
  - k=9 (single prime, p=2147483647): sparse gives H=19, S=1 (MATCHES the
    frozen prediction) in 98.7s (setup: bases+delta table up to k=9) + 115.7s
    (H/S compute for k=9 itself) = ~214s total for one prime at kmax=9.

v2 CHANGES from v1 (edim_run_c9_c10.py):
  1. sparse_degrees enabled for ALL degrees (GradedLie(..., sparse_degrees=
     set(range(1,kmax+1)))) -- fixes the GHA timeout.
  2. Builds n_alg/h_alg/delta-table ONCE per prime at kmax=10 (not
     separately for kmax=8, then 9, then 10 as v1 did) -- avoids redundant
     rebuild work, since H/S at any k<=kmax only needs data already present
     in a kmax=10 build.
  3. Fill-in ratio and per-degree sparse-solver stats are recorded in the
     cert (docs/notes/edim_sparse_solver_design_v1.md SS2.2 fail-closed
     discipline: SparseFillinExceeded aborts the run with no cert claiming
     success, rather than silently falling back to dense).

Order (unchanged from v1, per 裁定658): regression (k=7,8, large primes) ->
k=9 -> k=10. k=11,12 NOT run here (design spec's own plan: validate k=9,10
sparse-vs-dense agreement first, THEN attempt k=11 as a SEPARATE follow-up
once this run is confirmed feasible).
"""
import json
import sys
import time
import tracemalloc

import numpy as np

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed

LARGE_PRIMES = [2147483647, 998244353]
KMAX = 10

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


def build_and_run(p, kmax=KMAX, kmin=7):
    t0 = time.time()
    n_alg = ed.GradedLie(3, kmax, p, sparse_degrees=set(range(1, kmax + 1)))
    h_alg = ed.GradedLie(2, kmax, p, sparse_degrees=set(range(1, kmax + 1)))
    print(f"  p={p}: bases built in {time.time()-t0:.1f}s", flush=True)
    t1 = time.time()
    D = ed.build_delta_table(n_alg, h_alg, kmax, p)
    print(f"  p={p}: delta table built in {time.time()-t1:.1f}s", flush=True)
    t_build = time.time() - t0

    out = {"_build_elapsed_sec": round(t_build, 3)}
    for k in range(kmin, kmax + 1):
        tk0 = time.time()
        H_dim, S_dim, dim_n, dim_h, dim_t = compute_H_S_at_k_safe(k, n_alg, h_alg, D, p)
        fillin_n = n_alg._sparse_solver_cache.get(k, {}).get("fillin_ratio")
        fillin_h = h_alg._sparse_solver_cache.get(k, {}).get("fillin_ratio")
        out[k] = {"H_dim": H_dim, "S_dim": S_dim, "dim_n": dim_n, "dim_h": dim_h,
                   "dim_t": dim_t, "elapsed_sec": round(time.time() - tk0, 3),
                   "fillin_ratio_n": fillin_n, "fillin_ratio_h": fillin_h}
        print(f"  p={p} k={k}: H_dim={H_dim} S_dim={S_dim} dim_t={dim_t} "
              f"elapsed={out[k]['elapsed_sec']}s fillin_n={fillin_n} fillin_h={fillin_h}", flush=True)
    return out


def write_cert(payload):
    with open("search/certs/edim_c9_c10_run_v2_20260806.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def main():
    tracemalloc.start()
    t_start = time.time()

    print("=== v2 (sparse solver) run: k=7,8,9,10, single build per prime, kmax=10 ===", flush=True)
    per_prime = {}
    for p in LARGE_PRIMES:
        print(f"--- prime {p} ---", flush=True)
        per_prime[p] = build_and_run(p, kmax=KMAX, kmin=7)

    regression_report = {}
    regression_ok = True
    for k in (7, 8):
        vals = {p: (per_prime[p][k]["H_dim"], per_prime[p][k]["S_dim"]) for p in LARGE_PRIMES}
        agree = len(set(vals.values())) == 1
        h0, s0 = next(iter(vals.values()))
        matches_known = (h0 == EXPECTED_H[k] and s0 == EXPECTED_S[k])
        regression_report[k] = {"per_prime": {str(p): vals[p] for p in LARGE_PRIMES},
                                 "two_prime_agree": agree, "matches_prior_small_prime_result": matches_known}
        if not (agree and matches_known):
            regression_ok = False

    print("regression_report:", json.dumps(regression_report, indent=2), flush=True)
    if not regression_ok:
        print("*** REGRESSION FAILED (sparse vs known k=7,8) -- STOP ***", flush=True)
        write_cert({"schema": "edim-c9-c10-run/v2", "solver": "sparse", "regression_report": regression_report,
                    "regression_ok": False, "k9_scoring": None, "k10_scoring": None})
        sys.exit(1)

    scoring = {}
    calibration_fail = None
    for k in (9, 10):
        vals = {p: (per_prime[p][k]["H_dim"], per_prime[p][k]["S_dim"]) for p in LARGE_PRIMES}
        agree = len(set(vals.values())) == 1
        h, s = next(iter(vals.values()))
        if h != EXPECTED_H[k]:
            calibration_fail = k
            print(f"*** k={k} CALIBRATION_FAIL: H={h} != predicted {EXPECTED_H[k]} -- STOP ***", flush=True)
            break
        scoring[k] = {"two_prime_agree": agree, "H_measured": h, "H_predicted": EXPECTED_H[k], "H_match": True,
                      "S_measured": s, "S_predicted": EXPECTED_S[k], "S_match": (s == EXPECTED_S[k])}
        print(f"k={k} scoring:", json.dumps(scoring[k], indent=2), flush=True)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    total_elapsed = time.time() - t_start

    out = {
        "schema": "edim-c9-c10-run/v2",
        "solver": "sparse (docs/notes/edim_sparse_solver_design_v1.md, 裁定660 approved)",
        "authorization": "docs/notes/b_type_synthesis_design_v1_addendum_edim9_11_prediction.md "
                          "(commit 026dff8); 裁定658/660 (司令塔, this session); v2 supersedes the "
                          "dense v1 driver (edim_run_c9_c10.py) which timed out on GHA (runs "
                          "31074225133/31074224863, both hit the 60-min job ceiling, no cert produced)",
        "environment": "GitHub Actions ubuntu-latest (per 司令塔裁定; pure python/numpy, no GAP)",
        "primes": LARGE_PRIMES,
        "regression_report": regression_report,
        "regression_ok": True,
        "per_prime_full": {str(p): per_prime[p] for p in LARGE_PRIMES},
        "scoring": scoring,
        "calibration_fail_at_k": calibration_fail,
        "total_elapsed_sec": round(total_elapsed, 2),
        "peak_memory_traced_mb": round(peak / (1024 * 1024), 2),
        "k11_k12_not_run": True,
        "note": "k=11,12 deferred: this run validates k=9,10 sparse-solver correctness+feasibility "
                "first (per docs/notes/edim_sparse_solver_design_v1.md SS5 step 2); k=11 is a "
                "separate follow-up once this is confirmed.",
    }
    write_cert(out)

    if calibration_fail is not None:
        sys.exit(1)

    print("total_elapsed_sec:", out["total_elapsed_sec"], "peak_memory_traced_mb:", out["peak_memory_traced_mb"])
    print("EDIM_C9_C10_V2_RUN_DONE")


if __name__ == "__main__":
    main()
