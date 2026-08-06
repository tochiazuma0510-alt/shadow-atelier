#!/usr/bin/env python3
"""
edim_run_c9_c10_v4_single_kp.py -- per-(k, PRIME) sparse run, one CLI pair,
for the 4-way GHA matrix (k in {9,10}, prime in {2147483647, 998244353}).

Split further from v3 (which was per-PRIME, running k=7..10 sequentially in
one job) because v3's own local timing showed k=10's bases+delta-table
build alone (~26.5min) plus k=10's H/S compute (~27.8min) already consumes
most of a 60-minute budget for JUST k=10 at one prime -- packing k=7..10
together per prime leaves little margin. Splitting by (k,prime) lets k=9
and k=10 jobs run at full parallelism too (4 jobs instead of 2), and each
gets its own 60-minute ceiling.

NOTE: this script rebuilds bases+delta-table UP TO degree k EVERY TIME
(k=9 and k=10 jobs both redo the up-to-9 work) -- this is deliberate
duplicated CPU spend traded for wall-clock parallelism (4 independent jobs,
no cross-job dependency), matching 司令塔's explicit 4-way matrix
instruction.

k=7,8 are NOT redone here (already confirmed via v2/v3's regression phase
against the known small-prime results, commit 70879b0/ca95afd) -- this
script assumes that regression is still valid (unchanged edim_semidirect_v1
public interface) and goes straight to the target k.

Usage: python search/edim_run_c9_c10_v4_single_kp.py <k> <prime>

Writes search/certs/edim_c9_c10_k{k}_prime_{prime}_v4_20260806.json.
"""
import json
import sys
import time
import tracemalloc

import numpy as np

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed

EXPECTED_H = {9: 19, 10: 33}
EXPECTED_S = {9: 1, 10: 1}


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
    if len(sys.argv) != 3:
        print("usage: edim_run_c9_c10_v4_single_kp.py <k> <prime>", file=sys.stderr)
        sys.exit(2)
    k = int(sys.argv[1])
    p = int(sys.argv[2])
    if k not in (9, 10):
        print(f"k={k} not in {{9,10}} -- this script is scoped to the k=9,10 4-way matrix only", file=sys.stderr)
        sys.exit(2)

    tracemalloc.start()
    t_start = time.time()

    t0 = time.time()
    n_alg = ed.GradedLie(3, k, p, sparse_degrees=set(range(1, k + 1)))
    h_alg = ed.GradedLie(2, k, p, sparse_degrees=set(range(1, k + 1)))
    bases_elapsed = time.time() - t0
    print(f"k={k} p={p}: bases built in {bases_elapsed:.1f}s", flush=True)

    t1 = time.time()
    D = ed.build_delta_table(n_alg, h_alg, k, p)
    delta_elapsed = time.time() - t1
    print(f"k={k} p={p}: delta table built in {delta_elapsed:.1f}s", flush=True)

    t2 = time.time()
    H_dim, S_dim, dim_n, dim_h, dim_t = compute_H_S_at_k_safe(k, n_alg, h_alg, D, p)
    compute_elapsed = time.time() - t2
    fillin_n = n_alg._sparse_solver_cache.get(k, {}).get("fillin_ratio")
    fillin_h = h_alg._sparse_solver_cache.get(k, {}).get("fillin_ratio")
    print(f"k={k} p={p}: H_dim={H_dim} S_dim={S_dim} dim_t={dim_t} compute_elapsed={compute_elapsed:.1f}s "
          f"fillin_n={fillin_n} fillin_h={fillin_h}", flush=True)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    total_elapsed = time.time() - t_start

    out = {
        "schema": "edim-c9-c10-kp-run/v4",
        "solver": "sparse (docs/notes/edim_sparse_solver_design_v1.md; possibly Sol-accelerated per "
                  "便112e/sol/112e-edim-speedup if that branch has been merged -- check edim_semidirect_v1.py "
                  "provenance if timing looks anomalously different from the v3 baseline)",
        "k": k, "prime": p,
        "bases_elapsed_sec": round(bases_elapsed, 2),
        "delta_table_elapsed_sec": round(delta_elapsed, 2),
        "compute_elapsed_sec": round(compute_elapsed, 2),
        "H_dim": H_dim, "S_dim": S_dim, "dim_n": dim_n, "dim_h": dim_h, "dim_t": dim_t,
        "H_predicted": EXPECTED_H[k], "S_predicted": EXPECTED_S[k],
        "H_match": (H_dim == EXPECTED_H[k]), "S_match": (S_dim == EXPECTED_S[k]),
        "fillin_ratio_n": fillin_n, "fillin_ratio_h": fillin_h,
        "total_elapsed_sec": round(total_elapsed, 2),
        "peak_memory_traced_mb": round(peak / (1024 * 1024), 2),
    }
    out_path = f"search/certs/edim_c9_c10_k{k}_prime_{p}_v4_20260806.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print("total_elapsed_sec:", out["total_elapsed_sec"], "peak_memory_traced_mb:", out["peak_memory_traced_mb"])
    print("EDIM_C9_C10_KP_DONE")


if __name__ == "__main__":
    main()
