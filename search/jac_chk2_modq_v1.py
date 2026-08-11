#!/usr/bin/env python3
"""
search/jac_chk2_modq_v1.py -- JAC-CHK-2 mod-q rank/trace battery (裁定806/807/832/843).

*** v2 REWRITE (裁定843) *** -- 裁定832's bounded profiling (scratchpad/profile_jac17.py,
cProfile on p=17, 15-min cap) found the ACTUAL bottleneck was NOT the linear algebra (already
mod-q since 裁定806) but the CONSTRUCTION step itself: this module previously imported
search/jac_chk_v1.py's build_jacobson_s/theta_apply/tau_apply, which use exact Python Fraction
arithmetic and were measured to have SEVERE super-linear blowup (theta_apply calls 1-5 took
50.8s combined; call #6 alone did not finish within the remaining ~850s of the 15-minute cap).
Fixed here per 裁定843's approved fix: the ENTIRE construction pipeline is now mod-q throughout
(search/jac_construct_modq_v1.py's build_jacobson_s_modq/theta_apply_modq/tau_apply_modq,
bounded-integer arithmetic, no Fractions at all), run TWICE (once per prime Q1,Q2) since there
is no longer a shared "exact" intermediate to cache across primes.

Regression anchor (裁定843 requirement ①): p=5,7,11's known exact values (from
search/certs/jac_chk_v1_20260811.json: dim R_p=4,6,10 and isotypic type (1,1,1)/(1,1,2)/(2,2,3))
are checked by scratchpad/jac_construct_modq_regression_test.py before this module is trusted
for p=17,19,23.

Method (linear algebra part UNCHANGED from the v1 numpy-dense design, still valid):
  - Gaussian elimination mod q on a dense (n x N) int64 numpy matrix (vectorized row updates).
  - Trace via the RREF-pivot shortcut (no linear solve).
  - True integer character values recovered from mod-q1/mod-q2 residues via bounded-integer CRT.

No verdict language. Raw dim/trace/multiplicity values only.
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, "search")
from jac_construct_modq_v1 import build_jacobson_s_modq, theta_apply_modq, tau_apply_modq

Q1 = 999999937   # largest prime < 10^9
Q2 = 999999893   # another large prime < 10^9, distinct from Q1


def build_dense_modq(vecs, support_index, q):
    """vecs are ALREADY int-mod-q dicts (no Fraction reduction needed, unlike v1)."""
    n = len(vecs)
    N = len(support_index)
    M = np.zeros((n, N), dtype=np.int64)
    for i, v in enumerate(vecs):
        for w, c in v.items():
            j = support_index.get(w)
            if j is not None:
                M[i, j] = c % q
    return M


def measure_modq(p: int, q: int):
    """Construction is run FRESH for this q (no cross-prime caching -- the construction itself
    is now cheap mod q, per 裁定843's diagnosis/fix; the OLD v1 cached construction across
    primes specifically because it was expensive there, which is no longer the bottleneck)."""
    t_construct_0 = time.time()
    s_list, leftover = build_jacobson_s_modq(p, q)
    theta_s = [theta_apply_modq(s, q) for s in s_list]
    tau_s = [tau_apply_modq(s, q) for s in s_list]
    t_construct = time.time() - t_construct_0

    leftover_is_zero = (len(leftover) == 0)
    n = len(s_list)

    support = sorted(set().union(*[set(s.keys()) for s in s_list]))
    support_index = {w: i for i, w in enumerate(support)}
    N = len(support)

    S = build_dense_modq(s_list, support_index, q)
    THETA_S = build_dense_modq(theta_s, support_index, q)
    TAU_S = build_dense_modq(tau_s, support_index, q)

    combo = np.eye(n, dtype=np.int64)
    work = S.copy()

    used = np.zeros(n, dtype=bool)
    pivots = []
    pivot_combo_rows = []

    for col in range(N):
        nz = np.nonzero(work[:, col] % q)[0]
        piv_idx = None
        for i in nz:
            if not used[i]:
                piv_idx = int(i)
                break
        if piv_idx is None:
            continue
        used[piv_idx] = True
        pivval = int(work[piv_idx, col]) % q
        inv = pow(pivval, q - 2, q)
        work[piv_idx] = (work[piv_idx] * inv) % q
        combo[piv_idx] = (combo[piv_idx] * inv) % q

        factors = work[:, col].copy() % q
        factors[piv_idx] = 0
        nzrows = np.nonzero(factors)[0]
        if len(nzrows) > 0:
            upd = np.outer(factors[nzrows], work[piv_idx]) % q
            work[nzrows] = (work[nzrows] - upd) % q
            updc = np.outer(factors[nzrows], combo[piv_idx]) % q
            combo[nzrows] = (combo[nzrows] - updc) % q

        pivots.append(col)
        pivot_combo_rows.append(combo[piv_idx].copy())
        if len(pivots) == n:
            break

    rank = len(pivots)
    result = {
        "p": p, "q": q, "rank": rank, "expected_p_minus_1": p - 1,
        "linearly_independent": (rank == p - 1),
        "leftover_t_p_minus_1_is_zero": leftover_is_zero,
        "construction_time_sec": t_construct,
        "support_size": N,
    }
    if rank != p - 1:
        result["chi_theta_modq"] = None
        result["chi_tau_modq"] = None
        return result

    chi_theta = 0
    chi_tau = 0
    for piv, pc in zip(pivots, pivot_combo_rows):
        tval = int((pc.astype(object) @ THETA_S[:, piv].astype(object)) % q)
        uval = int((pc.astype(object) @ TAU_S[:, piv].astype(object)) % q)
        chi_theta = (chi_theta + tval) % q
        chi_tau = (chi_tau + uval) % q

    result["chi_theta_modq"] = chi_theta
    result["chi_tau_modq"] = chi_tau
    return result


def recover_signed_int(r1, r2, q1: int, q2: int, bound: int):
    from math import gcd
    if r1 is None or r2 is None:
        return None
    if gcd(q1, q2) != 1:
        return None
    inv_q1_mod_q2 = pow(q1, -1, q2)
    k = ((r2 - r1) * inv_q1_mod_q2) % q2
    x = r1 + q1 * k
    modulus = q1 * q2
    if x > modulus // 2:
        x -= modulus
    if abs(x) > bound:
        return None
    return x


def measure_both_q(p: int):
    t0 = time.time()
    r1 = measure_modq(p, Q1)
    t1 = time.time()
    r2 = measure_modq(p, Q2)
    t2 = time.time()
    agree_rank = (r1["rank"] == r2["rank"])
    out = {
        "p": p, "q1": Q1, "q2": Q2, "modq1": r1, "modq2": r2,
        "rank_agrees_across_q": agree_rank,
        "dim_R_p": r1["rank"] if agree_rank else None,
        "linearly_independent": r1["linearly_independent"] if agree_rank else None,
        "timing_sec": {"q1": t1 - t0, "q2": t2 - t1},
    }
    if agree_rank and r1["linearly_independent"]:
        dim = r1["rank"]
        bound = dim
        chi_theta = recover_signed_int(r1["chi_theta_modq"], r2["chi_theta_modq"], Q1, Q2, bound)
        chi_tau = recover_signed_int(r1["chi_tau_modq"], r2["chi_tau_modq"], Q1, Q2, bound)
        out["chi_theta"] = chi_theta
        out["chi_tau"] = chi_tau
        if chi_theta is not None and chi_tau is not None:
            num_triv = dim + 3 * chi_theta + 2 * chi_tau
            num_sgn = dim - 3 * chi_theta + 2 * chi_tau
            num_std = dim - chi_tau
            m_triv = num_triv // 6 if num_triv % 6 == 0 else None
            m_sgn = num_sgn // 6 if num_sgn % 6 == 0 else None
            m_std = num_std // 3 if num_std % 3 == 0 else None
            out["isotypic"] = {"m_triv": m_triv, "m_sgn": m_sgn, "m_std": m_std}
            out["isotypic_exact_division_ok"] = (num_triv % 6 == 0 and num_sgn % 6 == 0 and num_std % 3 == 0)
            if None not in (m_triv, m_sgn, m_std):
                out["dim_from_isotypic_sum"] = m_triv + m_sgn + 2 * m_std
                out["dim_matches_isotypic_sum"] = (out["dim_from_isotypic_sum"] == dim)
    return out


def main():
    targets = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [17]
    out_per_p = {}
    for p in targets:
        r = measure_both_q(p)
        out_per_p[p] = r
        print(f"p={p}: q1_rank={r['modq1']['rank']} q2_rank={r['modq2']['rank']} "
              f"agree={r['rank_agrees_across_q']} chi_theta={r.get('chi_theta')} "
              f"chi_tau={r.get('chi_tau')} isotypic={r.get('isotypic')} "
              f"construct_q1={r['modq1'].get('construction_time_sec'):.2f}s "
              f"construct_q2={r['modq2'].get('construction_time_sec'):.2f}s "
              f"timing_q1={r['timing_sec']['q1']:.2f}s timing_q2={r['timing_sec']['q2']:.2f}s",
              flush=True)

    out = {
        "schema": "shadow-atelier/jac_chk2_modq_v1",
        "authority": "裁定806/807/832/843 (mod-q rank/trace battery, v2: FULL mod-q construction, "
                     "fixing the theta_apply/tau_apply exact-Fraction super-linear blowup "
                     "diagnosed via scratchpad/profile_jac17.py)",
        "method_note": "construction (build_jacobson_s/theta_apply/tau_apply) is NOW mod-q "
                       "throughout (search/jac_construct_modq_v1.py), run once per prime (no "
                       "cross-prime caching, since construction is no longer the expensive "
                       "part). Linear algebra unchanged from v1: dense numpy int64 Gaussian "
                       "elimination + RREF-pivot-shortcut trace + bounded-integer CRT.",
        "primes_used": {"Q1": Q1, "Q2": Q2},
        "per_p": {str(p): v for p, v in out_per_p.items()},
        "no_verdict_note": "raw ranks, characters, isotypic multiplicities, and booleans only.",
    }
    out_path = f"search/certs/jac_chk2_modq_v1_20260811_p{'_'.join(str(p) for p in targets)}.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
