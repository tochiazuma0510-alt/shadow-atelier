#!/usr/bin/env python3
"""
edim_run_c1c4.py -- runs calibration C-1..C-4 of docs/notes/
edim_semidirect_model_design_v1.md SS5.3, using search/edim_semidirect_v1.py.

STOPS AFTER C-4 (per instruction: "C-4 で必ず一旦停止して報告"). Does not
run k=7+ under any circumstance in this pass.

C-1: rho^5 = id at degree 1,2,3.
C-2: delta_X(A+B+C) = delta_Y(A+B+C) = 0.
C-3: dim t_k for k=1..6 = 5,4,10,21,54,125.
C-4 (lifeline): dim H_k, dim S_k for k=3,4,5,6, must match
    search/certs/edim56_20260806.json EXACTLY (H=1,1,2,3 / S=1,0,1,0).

Two independent primes (matching edim56's own convention); results are
cross-checked between them, not reported as single-prime "exact".
"""
import json
import sys

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed

KMAX = 6
PRIMES = ed.PRIMES

EXPECTED_T_DIM = {1: 5, 2: 4, 3: 10, 4: 21, 5: 54, 6: 125}
EXPECTED_H = {3: 1, 4: 1, 5: 2, 6: 3}
EXPECTED_S = {3: 1, 4: 0, 5: 1, 6: 0}


def run_for_prime(p):
    n_alg = ed.GradedLie(3, KMAX, p)
    h_alg = ed.GradedLie(2, KMAX, p)
    L_alg = ed.GradedLie(2, KMAX, p)  # L_k = Lie(x,y), separate instance from h (design: j is the canonical identification, but we keep them as distinct GradedLie objects instantiated identically -- same Lyndon word structure/order by construction, since both are Lie(2 letters))

    D = ed.build_delta_table(n_alg, h_alg, KMAX, p)

    result = {"prime": p}

    # ---- C-3: dim t_k = dim n_k + dim h_k ----
    t_dim = {k: n_alg.dim[k] + h_alg.dim[k] for k in range(1, KMAX + 1)}
    result["t_dim"] = t_dim
    result["C3_pass"] = all(t_dim[k] == EXPECTED_T_DIM[k] for k in range(1, KMAX + 1))

    # ---- C-2: delta_X(A+B+C) = delta_Y(A+B+C) = 0 ----
    abc_coord = [1 % p, 1 % p, 1 % p]  # A+B+C in n_1 basis coords [A,B,C]
    dX_abc = ed.delta_apply([1 % p, 0], 1, abc_coord, 1, D, n_alg, p)  # h_coord for X = [1,0]
    dY_abc = ed.delta_apply([0, 1 % p], 1, abc_coord, 1, D, n_alg, p)  # h_coord for Y = [0,1]
    result["C2_deltaX_ABC"] = dX_abc
    result["C2_deltaY_ABC"] = dY_abc
    result["C2_pass"] = all(x % p == 0 for x in dX_abc) and all(x % p == 0 for x in dY_abc)

    # ---- rho matrices for k=1..min(KMAX,3+2)=... build up to KMAX (needed for C-4's nu_k anyway) ----
    rho_mats = {}
    dim_n_of = {}
    dim_h_of = {}
    for k in range(1, KMAX + 1):
        M, dn, dh = ed.build_rho_matrix(k, n_alg, h_alg, D, p)
        rho_mats[k] = M
        dim_n_of[k] = dn
        dim_h_of[k] = dh

    # ---- C-1: rho^5 = id at degree 1,2,3 ----
    c1 = {}
    for k in (1, 2, 3):
        M5 = ed.mat_pow_modp(rho_mats[k], 5, p)
        I = ed.identity_modp(len(M5), p)
        c1[k] = (M5 == I)
    result["C1_rho5_is_id"] = c1
    result["C1_pass"] = all(c1.values())

    # ---- theta, tau matrices on L_k (reuse h_alg's Lyndon structure directly for L) ----
    theta_mats = {k: ed.build_theta_tau_matrix(k, h_alg, 'theta', p) for k in range(1, KMAX + 1)}
    tau_mats = {k: ed.build_theta_tau_matrix(k, h_alg, 'tau', p) for k in range(1, KMAX + 1)}

    # ---- H_k = ker(1+theta) cap ker(1+tau+tau^2), within L_k=h_alg basis ----
    H_dim = {}
    for k in range(1, KMAX + 1):
        dim_h = h_alg.dim[k]
        I = ed.identity_modp(dim_h, p)
        one_plus_theta = ed.mat_add_modp(I, theta_mats[k], p)
        tau2 = ed.mat_mul_modp(tau_mats[k], tau_mats[k], p)
        one_plus_tau_tau2 = ed.mat_add_modp(ed.mat_add_modp(I, tau_mats[k], p), tau2, p)
        stack = one_plus_theta + one_plus_tau_tau2  # row-stack (list of rows)
        rank = ed.rank_modp(stack, p) if dim_h > 0 else 0
        H_dim[k] = dim_h - rank
    result["H_dim"] = H_dim

    # ---- nu_k = sum_{i=0}^4 rho^i (on t_k), restricted to the h-block columns
    # (= j(L_k) subspace) for the S_k constraint ----
    S_dim = {}
    for k in range(1, KMAX + 1):
        dim_h = h_alg.dim[k]
        dim_t = rho_mats[k].__len__()
        nu = ed.identity_modp(dim_t, p)
        acc = ed.identity_modp(dim_t, p)
        cur = rho_mats[k]
        # nu = I + rho + rho^2 + rho^3 + rho^4
        nu = [row[:] for row in ed.identity_modp(dim_t, p)]
        power = ed.identity_modp(dim_t, p)
        for i in range(1, 5):
            power = ed.mat_mul_modp(power, rho_mats[k], p)
            nu = ed.mat_add_modp(nu, power, p)
        dim_n_k = dim_n_of[k]
        # nu restricted to h-block COLUMNS (j embeds L_k into the h-part,
        # n-component 0): columns dim_n_k .. dim_n_k+dim_h-1 of nu.
        nu_j_cols = [[nu[r][dim_n_k + c] for r in range(dim_t)] for c in range(dim_h)]
        # nu_j_cols[c] is a column vector (length dim_t); build matrix rows=dim_t, cols=dim_h
        nu_j_mat = [[nu_j_cols[c][r] for c in range(dim_h)] for r in range(dim_t)]

        # H_k basis (nullspace of stack) needed to intersect -- but we only
        # need dimensions, so build the FULL constraint stack: (1+theta),
        # (1+tau+tau^2), and nu_j_mat (dim_t rows), all acting on the SAME
        # dim_h-dimensional coordinate space (L_k = h_alg basis).
        I = ed.identity_modp(dim_h, p)
        one_plus_theta = ed.mat_add_modp(I, theta_mats[k], p)
        tau2 = ed.mat_mul_modp(tau_mats[k], tau_mats[k], p)
        one_plus_tau_tau2 = ed.mat_add_modp(ed.mat_add_modp(I, tau_mats[k], p), tau2, p)
        stack = one_plus_theta + one_plus_tau_tau2 + nu_j_mat
        rank = ed.rank_modp(stack, p) if dim_h > 0 else 0
        S_dim[k] = dim_h - rank
    result["S_dim"] = S_dim

    result["C4_pass"] = all(H_dim.get(k) == EXPECTED_H.get(k) for k in EXPECTED_H) and \
                         all(S_dim.get(k) == EXPECTED_S.get(k) for k in EXPECTED_S)

    return result


def main():
    per_prime = [run_for_prime(p) for p in PRIMES]

    agree = True
    for field in ("t_dim", "H_dim", "S_dim", "C1_pass", "C2_pass", "C3_pass", "C4_pass"):
        vals = [r[field] for r in per_prime]
        if vals[0] != vals[1]:
            agree = False

    out = {
        "schema": "edim-semidirect-c1c4/v1",
        "authorization": "docs/notes/edim_semidirect_model_design_v1.md SS5.3 (裁定646, 司令塔 this session)",
        "primes": PRIMES,
        "two_prime_agreement": agree,
        "per_prime": per_prime,
        "C1_pass": per_prime[0]["C1_pass"] and agree,
        "C2_pass": per_prime[0]["C2_pass"] and agree,
        "C3_pass": per_prime[0]["C3_pass"] and agree,
        "C4_pass": per_prime[0]["C4_pass"] and agree,
        "expected": {"t_dim": EXPECTED_T_DIM, "H": EXPECTED_H, "S": EXPECTED_S},
        "note": "STOPPED after C-4 per instruction (k=7+ not run in this pass). C-4 is the lifeline: "
                "must match search/certs/edim56_20260806.json's H_dim/S_dim exactly (independent second "
                "implementation of the same quantity via a different method -- ideal-quotient vs "
                "semidirect-model).",
    }
    with open("search/certs/edim_semidirect_c1c4_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print("two_prime_agreement:", agree)
    print("C1_pass:", out["C1_pass"])
    print("C2_pass:", out["C2_pass"])
    print("C3_pass:", out["C3_pass"], "t_dim:", per_prime[0]["t_dim"])
    print("C4_pass:", out["C4_pass"])
    print("  H_dim:", per_prime[0]["H_dim"], "expected:", EXPECTED_H)
    print("  S_dim:", per_prime[0]["S_dim"], "expected:", EXPECTED_S)
    if not out["C4_pass"]:
        print("*** C-4 LIFELINE FAILED -- STOP, do not report k=7+ (there is none in this pass anyway) ***")
        sys.exit(1)


if __name__ == "__main__":
    main()
