#!/usr/bin/env python3
"""
edim_run_c9_c10_v3_single_prime.py -- per-PRIME sparse run for k=7,8,9,10,
runnable standalone with one CLI arg (the prime). Split out of
edim_run_c9_c10_v2.py so GHA can run the two required large primes as
PARALLEL matrix jobs (each prime independently took ~56 minutes locally --
sequential-in-one-job would need ~110+ minutes, closer to timing out even
with a generous ceiling; parallel jobs cut wall time roughly in half).

Usage: python search/edim_run_c9_c10_v3_single_prime.py <prime>

Writes search/certs/edim_c9_c10_prime_<prime>_v3_20260806.json (per-prime
raw results only -- NO regression/scoring verdict, NO cross-prime
agreement check; that aggregation happens in
edim_run_c9_c10_v3_aggregate.py after BOTH primes' certs exist).
"""
import json
import sys
import time
import tracemalloc

import numpy as np

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed

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


def main():
    if len(sys.argv) != 2:
        print("usage: edim_run_c9_c10_v3_single_prime.py <prime>", file=sys.stderr)
        sys.exit(2)
    p = int(sys.argv[1])

    tracemalloc.start()
    t_start = time.time()

    t0 = time.time()
    n_alg = ed.GradedLie(3, KMAX, p, sparse_degrees=set(range(1, KMAX + 1)))
    h_alg = ed.GradedLie(2, KMAX, p, sparse_degrees=set(range(1, KMAX + 1)))
    print(f"p={p}: bases built in {time.time()-t0:.1f}s", flush=True)
    t1 = time.time()
    D = ed.build_delta_table(n_alg, h_alg, KMAX, p)
    build_elapsed = time.time() - t1
    print(f"p={p}: delta table built in {build_elapsed:.1f}s", flush=True)

    results = {}
    for k in range(7, KMAX + 1):
        tk0 = time.time()
        H_dim, S_dim, dim_n, dim_h, dim_t = compute_H_S_at_k_safe(k, n_alg, h_alg, D, p)
        fillin_n = n_alg._sparse_solver_cache.get(k, {}).get("fillin_ratio")
        fillin_h = h_alg._sparse_solver_cache.get(k, {}).get("fillin_ratio")
        elapsed = round(time.time() - tk0, 3)
        results[k] = {"H_dim": H_dim, "S_dim": S_dim, "dim_n": dim_n, "dim_h": dim_h,
                     "dim_t": dim_t, "elapsed_sec": elapsed,
                     "fillin_ratio_n": fillin_n, "fillin_ratio_h": fillin_h,
                     "H_predicted": EXPECTED_H[k], "S_predicted": EXPECTED_S[k],
                     "H_match": (H_dim == EXPECTED_H[k]), "S_match": (S_dim == EXPECTED_S[k])}
        print(f"p={p} k={k}: H_dim={H_dim} S_dim={S_dim} dim_t={dim_t} elapsed={elapsed}s "
              f"fillin_n={fillin_n} fillin_h={fillin_h}", flush=True)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    total_elapsed = time.time() - t_start

    out = {
        "schema": "edim-c9-c10-prime-run/v3",
        "solver": "sparse (docs/notes/edim_sparse_solver_design_v1.md, 裁定660 approved)",
        "prime": p,
        "kmax": KMAX,
        "bases_and_delta_table_elapsed_sec": round(build_elapsed, 2),
        "results": results,
        "total_elapsed_sec": round(total_elapsed, 2),
        "peak_memory_traced_mb": round(peak / (1024 * 1024), 2),
        "note": "Per-PRIME raw results only. Cross-prime agreement / regression verdict / final "
                "scoring is computed by edim_run_c9_c10_v3_aggregate.py after both primes complete.",
    }
    out_path = f"search/certs/edim_c9_c10_prime_{p}_v3_20260806.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print("total_elapsed_sec:", out["total_elapsed_sec"], "peak_memory_traced_mb:", out["peak_memory_traced_mb"])
    print("EDIM_C9_C10_SINGLE_PRIME_DONE")


if __name__ == "__main__":
    main()
