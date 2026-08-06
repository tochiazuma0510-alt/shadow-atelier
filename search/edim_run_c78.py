#!/usr/bin/env python3
"""
edim_run_c78.py -- E-DIM7/8 scoring run per 裁定652/裁定646 follow-up.

Frozen prediction (verbatim authority, commit 346c264): docs/notes/
b_type_synthesis_design_v1_addendum_edim78_prediction.md --
  dim S_7 = 1, dim S_8 = 1 (scored); dim H_7 = 6, dim H_8 = 10 (reference).

Uses search/edim_semidirect_v1.py (semidirect model, NOT the ideal-quotient
method the prediction doc's own SS2 feasibility table was estimating cost
for -- this model's native dim t_7=330, t_8=840, per design doc SS4).

S-ED-3/S-ED-4 discipline: TWO independent SMALL primes (<2^16) run first
(fast, numpy-int64-exact matmul: p^2*840 well under int64 range) --
PRIMES_SMALL = [65521, 65519]. If they agree, run ONE arbitration prime
(ARBITRATION_PRIME = 29999999, still int64-matmul-safe: p^2*840 ~7.6e17,
comfortably under int64max~9.2e18) to confirm the rank is not a small-prime
artefact, per S-ED-4 ("小素数使用時は大素数仲裁まで階数未確定"). Rank is only
reported as CONFIRMED if all three primes agree.

k=9+ is explicitly NOT run (裁定652/reiteration: "k=9以降は走らせず停止報告").

Memory: peak RSS is recorded (S-ED-6-adjacent discipline -- if this exceeds
budget mid-run for k=8, the run is expected to fail loudly, not report a
partial result).
"""
import gc
import json
import sys
import time
import tracemalloc

import numpy as np

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed

PRIMES_SMALL = [65521, 65519]
ARBITRATION_PRIME = 29999999
for p in PRIMES_SMALL + [ARBITRATION_PRIME]:
    import sympy
    assert sympy.isprime(p), f"{p} is not prime"
assert PRIMES_SMALL[0] < 2**16 and PRIMES_SMALL[1] < 2**16, "PRIMES_SMALL must be S-ED-4 'small' (<2^16)"
assert ARBITRATION_PRIME >= 2**16, "arbitration prime must be S-ED-4 'large' (>=2^16)"
for p in PRIMES_SMALL + [ARBITRATION_PRIME]:
    assert p * p * 840 < (2**63 - 1) // 4, f"prime {p} not safe for int64 matmul at max dim 840"

EXPECTED_H = {7: 6, 8: 10}
EXPECTED_S = {7: 1, 8: 1}


def build_for_kmax(kmax, p):
    n_alg = ed.GradedLie(3, kmax, p)
    h_alg = ed.GradedLie(2, kmax, p)
    D = ed.build_delta_table(n_alg, h_alg, kmax, p)
    return n_alg, h_alg, D


def compute_H_S_at_k(k, n_alg, h_alg, D, p):
    dim_n = n_alg.dim[k]
    dim_h = h_alg.dim[k]
    dim_t = dim_n + dim_h

    # rho matrix (built via the existing pure-python tree-substitution code
    # -- this part is combinatorial/tree-recursive, not a big matmul, and is
    # only O(dim_t) calls each doing O(k) bracket steps, so it stays fast)
    M_list, dn, dh = ed.build_rho_matrix(k, n_alg, h_alg, D, p)
    assert dn == dim_n and dh == dim_h
    rho = np.array(M_list, dtype=np.int64) % p

    # nu_k = I + rho + rho^2 + rho^3 + rho^4 (numpy matmul, safe primes)
    nu = np.eye(dim_t, dtype=np.int64)
    power = np.eye(dim_t, dtype=np.int64)
    for i in range(1, 5):
        power = ed.mat_mul_modp_np(power, rho, p)
        nu = (nu + power) % p

    # theta, tau on L_k = h_alg's own Lyndon structure (small: dim_h<=30)
    theta = np.array(ed.build_theta_tau_matrix(k, h_alg, 'theta', p), dtype=np.int64) % p
    tau = np.array(ed.build_theta_tau_matrix(k, h_alg, 'tau', p), dtype=np.int64) % p
    I_h = np.eye(dim_h, dtype=np.int64)
    one_plus_theta = (I_h + theta) % p
    tau2 = ed.mat_mul_modp_np(tau, tau, p)
    one_plus_tau_tau2 = (I_h + tau + tau2) % p

    H_stack = np.concatenate([one_plus_theta, one_plus_tau_tau2], axis=0)
    H_dim = dim_h - ed.rank_modp_np(H_stack, p)

    nu_j_mat = nu[:, dim_n:dim_n + dim_h]  # dim_t x dim_h
    S_stack = np.concatenate([one_plus_theta, one_plus_tau_tau2, nu_j_mat], axis=0)
    S_dim = dim_h - ed.rank_modp_np(S_stack, p)

    return H_dim, S_dim, dim_n, dim_h, dim_t


def run_one_prime(kmax, p):
    t0 = time.time()
    n_alg, h_alg, D = build_for_kmax(kmax, p)
    t_build = time.time() - t0
    out = {}
    for k in range(3, kmax + 1):
        tk0 = time.time()
        H_dim, S_dim, dim_n, dim_h, dim_t = compute_H_S_at_k(k, n_alg, h_alg, D, p)
        out[k] = {"H_dim": H_dim, "S_dim": S_dim, "dim_n": dim_n, "dim_h": dim_h,
                   "dim_t": dim_t, "elapsed_sec": round(time.time() - tk0, 3)}
        print(f"  p={p} k={k}: H_dim={H_dim} S_dim={S_dim} dim_t={dim_t} "
              f"elapsed={out[k]['elapsed_sec']}s")
    out["_build_elapsed_sec"] = round(t_build, 3)
    return out


def main():
    KMAX = 8
    tracemalloc.start()
    t_start = time.time()

    results_by_prime = {}
    for p in PRIMES_SMALL:
        print(f"=== running prime {p} (small, S-ED-4) up to k={KMAX} ===")
        results_by_prime[p] = run_one_prime(KMAX, p)
        gc.collect()

    small_agree = {}
    for k in range(3, KMAX + 1):
        h_vals = {p: results_by_prime[p][k]["H_dim"] for p in PRIMES_SMALL}
        s_vals = {p: results_by_prime[p][k]["S_dim"] for p in PRIMES_SMALL}
        small_agree[k] = (len(set(h_vals.values())) == 1 and len(set(s_vals.values())) == 1)

    all_small_agree = all(small_agree.values())
    print("small-prime agreement per k:", small_agree)

    arb_results = None
    confirmed = {}
    if all_small_agree:
        print(f"=== small primes agree -- running arbitration prime {ARBITRATION_PRIME} (S-ED-4) ===")
        arb_results = run_one_prime(KMAX, ARBITRATION_PRIME)
        for k in range(3, KMAX + 1):
            h_small = results_by_prime[PRIMES_SMALL[0]][k]["H_dim"]
            s_small = results_by_prime[PRIMES_SMALL[0]][k]["S_dim"]
            h_arb = arb_results[k]["H_dim"]
            s_arb = arb_results[k]["S_dim"]
            confirmed[k] = {"H_confirmed": (h_small == h_arb), "S_confirmed": (s_small == s_arb),
                             "H_small": h_small, "H_arbitration": h_arb,
                             "S_small": s_small, "S_arbitration": s_arb}
    else:
        print("*** SMALL PRIMES DISAGREE -- rank is UNCONFIRMED per S-ED-4; "
              "reporting disagreement, not picking a winner ***")

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    total_elapsed = time.time() - t_start

    out = {
        "schema": "edim-c78-scoring/v1",
        "authorization": "docs/notes/b_type_synthesis_design_v1_addendum_edim78_prediction.md "
                          "(commit 346c264, frozen IF-FIRST prediction); 裁定652/reiteration (司令塔, this session)",
        "model": "semidirect (search/edim_semidirect_v1.py), NOT the ideal-quotient method the "
                 "prediction doc's SS2 feasibility table was estimating cost for",
        "primes_small": PRIMES_SMALL,
        "arbitration_prime": ARBITRATION_PRIME if all_small_agree else None,
        "small_prime_agreement_per_k": small_agree,
        "all_small_agree": all_small_agree,
        "S_ED_4_rank_confirmed": confirmed if all_small_agree else "NOT_CONFIRMED (small primes disagreed)",
        "results_by_prime": {str(p): results_by_prime[p] for p in PRIMES_SMALL},
        "arbitration_results": arb_results,
        "prediction": {"H": EXPECTED_H, "S_scored": EXPECTED_S},
        "scoring": {},
        "total_elapsed_sec": round(total_elapsed, 2),
        "peak_memory_traced_mb": round(peak / (1024 * 1024), 2),
        "note_memory": "tracemalloc traces PYTHON-level allocations only (not numpy's underlying "
                        "C buffers in full detail depending on allocator, and not GAP -- this is a "
                        "pure-python/numpy process, no GAP involved). Reported as a lower-bound signal, "
                        "not an authoritative RSS peak; see stdout for wall-clock timing per k as the "
                        "primary feasibility evidence.",
        "k9_plus_not_run": True,
    }
    for k in (7, 8):
        if k in results_by_prime[PRIMES_SMALL[0]]:
            s_val = results_by_prime[PRIMES_SMALL[0]][k]["S_dim"]
            h_val = results_by_prime[PRIMES_SMALL[0]][k]["H_dim"]
            out["scoring"][k] = {
                "S_measured": s_val, "S_predicted": EXPECTED_S[k], "S_match": (s_val == EXPECTED_S[k]),
                "H_measured": h_val, "H_predicted": EXPECTED_H[k], "H_match": (h_val == EXPECTED_H[k]),
                "rank_confirmed": confirmed.get(k, {}).get("S_confirmed", False) and
                                   confirmed.get(k, {}).get("H_confirmed", False) if all_small_agree else False,
            }

    with open("search/certs/edim_c78_scoring_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(json.dumps(out["scoring"], indent=2, ensure_ascii=False))
    print("total_elapsed_sec:", out["total_elapsed_sec"], "peak_memory_traced_mb:", out["peak_memory_traced_mb"])


if __name__ == "__main__":
    main()
