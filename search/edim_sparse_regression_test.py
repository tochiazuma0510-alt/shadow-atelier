#!/usr/bin/env python3
"""
edim_sparse_regression_test.py -- regression gate per docs/notes/
edim_sparse_solver_design_v1.md SS5 step 2: confirm the sparse solver
(build_sparse_solver/sparse_solve_coords, GradedLie(sparse_degrees=...))
reproduces the DENSE solver's H_dim/S_dim exactly at k=3..6 (the dense path
is the trusted baseline, already cross-checked against search/certs/
edim56_20260806.json in commit e232aa2).

Also confirms basis-vector self-consistency (each basis vector's own
coordinate solve recovers the standard unit vector) at k=1..6, and reports
the fill-in ratio trend.
"""
import json
import sys

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed

P = 2147483647
KMAX = 6
EXPECTED_H = {3: 1, 4: 1, 5: 2, 6: 3}
EXPECTED_S = {3: 1, 4: 0, 5: 1, 6: 0}


def compute_H_S_at_k(k, n_alg, h_alg, D, p):
    import numpy as np
    dim_n = n_alg.dim[k]
    dim_h = h_alg.dim[k]
    dim_t = dim_n + dim_h
    M_list, dn, dh = ed.build_rho_matrix(k, n_alg, h_alg, D, p)
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
    return H_dim, S_dim


def main():
    problems = []

    # basis self-consistency, sparse solver, k=1..6, both alphabets
    n_alg_sparse = ed.GradedLie(3, KMAX, P, sparse_degrees=set(range(1, KMAX + 1)))
    h_alg_sparse = ed.GradedLie(2, KMAX, P, sparse_degrees=set(range(1, KMAX + 1)))
    fillin_trend = {"n": {}, "h": {}}
    for alg, tag in ((n_alg_sparse, "n"), (h_alg_sparse, "h")):
        for k in range(1, KMAX + 1):
            basis = alg.ambient[k]
            for i, bvec in enumerate(basis):
                coord = alg.coords_of_ambient(k, bvec)
                expected = [1 if j == i else 0 for j in range(len(basis))]
                if coord != expected:
                    problems.append(f"{tag}-side k={k} basis[{i}] self-consistency FAILED")
            solver = alg._sparse_solver_cache.get(k, {})
            fillin_trend[tag][k] = solver.get("fillin_ratio")

    # H/S dims: sparse vs known-good dense values (edim_semidirect_c1c4_v1_20260806.json)
    D_sparse = ed.build_delta_table(n_alg_sparse, h_alg_sparse, KMAX, P)
    sparse_HS = {}
    for k in range(3, KMAX + 1):
        H, S = compute_H_S_at_k(k, n_alg_sparse, h_alg_sparse, D_sparse, P)
        sparse_HS[k] = {"H": H, "S": S}
        if H != EXPECTED_H[k] or S != EXPECTED_S[k]:
            problems.append(f"k={k}: sparse H={H},S={S} != known-good H={EXPECTED_H[k]},S={EXPECTED_S[k]}")

    result = {
        "schema": "edim-sparse-regression-test/v1",
        "prime": P,
        "kmax": KMAX,
        "sparse_HS": sparse_HS,
        "expected_HS": {k: {"H": EXPECTED_H[k], "S": EXPECTED_S[k]} for k in range(3, KMAX + 1)},
        "fillin_ratio_trend": fillin_trend,
        "problems": problems,
        "all_checks_pass": len(problems) == 0,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    with open("search/certs/edim_sparse_regression_test_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
