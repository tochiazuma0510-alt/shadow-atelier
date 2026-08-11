#!/usr/bin/env python3
"""
search/jac_chk2_modq_v1.py -- JAC-CHK-2 mod-q rank/trace battery (裁定806/807).

Commander's ruling (裁定806): the exact-sympy-rational approach in search/jac_chk2_v1.py
is a tool-choice error for p=19 (Witt(2,19)=27,594-dim). dim R_p (rank) and the S3-isotypic
type (via character trace) are computed here mod q (two large primes, cross-checked) using
DENSE NUMPY int64 arrays -- a first pure-Python sparse-dict draft was measured to take 13.6s
for p=11 alone (n=10) and did not finish p=13 within 90s, an unacceptable scaling (Python-level
loop overhead per modular multiply/dict access, not the modulus size, was the bottleneck) --
replaced here with vectorized numpy row operations, which are orders of magnitude faster for
this shape of problem (few rows ~20, many columns ~10^4-10^5).

Method:
  - s_1..s_{p-1} (exact Fraction dicts) and theta(s_i)/tau(s_i) are built ONCE via the cheap
    exact bracket machinery (search/jac_chk_v1.py -- confirmed cheap even at p=17: 3.2s), then
    reduced mod q into a dense (n x N) int64 numpy matrix (N = |union of supports|, columns
    ordered canonically by sorted tensor-word tuples).
  - Gaussian elimination mod q on the dense matrix (vectorized row updates: row -= factor*pivot_row,
    all mod q, via numpy int64 arithmetic -- q ~ 10^9 so q^2 ~ 10^18 fits in int64 (max ~9.2*10^18)
    with margin for the subtraction, using Python's pow() for modular inverse (n is tiny, only
    called O(n) times, not a bottleneck) then numpy vectorized multiply+mod for the row update).
  - Trace via the RREF-pivot shortcut (once RREF is reached: basis vector e_i has 1 at its own
    pivot column and 0 at every other basis vector's pivot column, so theta(e_i)'s coordinate
    along e_i is theta(e_i) evaluated AT e_i's pivot column, directly, no linear solve). Applied
    to the mod-q reduced theta_s/tau_s matrices via the SAME row-combination coefficients tracked
    during elimination (an (n x n) matrix, cheap regardless of column count).
  - True integer character values recovered from mod-q1/mod-q2 residues via bounded-integer CRT
    (|chi(g)| <= dim <= p-1, primes ~10^9 >> dim, so residues determine the true integer exactly).

No verdict language. Raw dim/trace/multiplicity values only.
"""
import json
import sys
import time
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, "search")
from jac_chk_v1 import build_jacobson_s, theta_apply, tau_apply  # search-side reuse

Q1 = 999999937   # largest prime < 10^9
Q2 = 999999893   # another large prime < 10^9, distinct from Q1


def frac_mod(x: F, q: int, inv_cache: dict) -> int:
    """Reduce a Fraction mod q, using a cache of modular inverses keyed by denominator --
    denominators arising in this module are always small bounded integers (divisors of some
    i in 1..p-1, from build_jacobson_s's F(1,i) scaling), so this cache has at most ~p entries
    and avoids repeating an O(log q) modular exponentiation for every one of the (potentially
    thousands of) nonzero tensor-word coefficients -- this was the actual bottleneck in an
    earlier draft (measured: p=11 took 7-14s despite tiny n=10, because EVERY entry recomputed
    pow(denominator, q-2, q) from scratch)."""
    den = x.denominator
    inv = inv_cache.get(den)
    if inv is None:
        inv = pow(den % q, q - 2, q)
        inv_cache[den] = inv
    return (x.numerator % q) * inv % q


def build_dense_mod(vecs, support_index, q):
    n = len(vecs)
    N = len(support_index)
    M = np.zeros((n, N), dtype=np.int64)
    inv_cache = {}
    for i, v in enumerate(vecs):
        for w, c in v.items():
            j = support_index.get(w)
            if j is not None:
                M[i, j] = frac_mod(c, q, inv_cache)
    return M


def measure_modq(p: int, q: int, precomputed=None):
    """Returns (result_dict, precomputed) where precomputed caches the expensive exact
    bracket-construction step (s_list, theta(s_list), tau(s_list)) for reuse across the two
    primes Q1,Q2 (that part does NOT depend on q, no need to redo it)."""
    if precomputed is None:
        s_list, leftover = build_jacobson_s(p)
        theta_s = [theta_apply(s) for s in s_list]
        tau_s = [tau_apply(s) for s in s_list]
        precomputed = (s_list, leftover, theta_s, tau_s)
    else:
        s_list, leftover, theta_s, tau_s = precomputed
    leftover_is_zero = (len(leftover) == 0)
    n = len(s_list)

    support = sorted(set().union(*[set(s.keys()) for s in s_list]))
    support_index = {w: i for i, w in enumerate(support)}
    N = len(support)

    S = build_dense_mod(s_list, support_index, q)         # n x N
    THETA_S = build_dense_mod(theta_s, support_index, q)   # n x N
    TAU_S = build_dense_mod(tau_s, support_index, q)       # n x N

    # combo: n x n, tracks current row i as a linear combination (mod q) of ORIGINAL rows
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
            # vectorized: work[nzrows] -= outer(factors[nzrows], work[piv_idx]) mod q
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
    }
    if rank != p - 1:
        result["chi_theta_modq"] = None
        result["chi_tau_modq"] = None
        return result, precomputed

    chi_theta = 0
    chi_tau = 0
    for piv, pc in zip(pivots, pivot_combo_rows):
        # theta(e_i) = pc . THETA_S (row vector times matrix), coefficient at column piv
        tval = int((pc.astype(object) @ THETA_S[:, piv].astype(object)) % q)
        uval = int((pc.astype(object) @ TAU_S[:, piv].astype(object)) % q)
        chi_theta = (chi_theta + tval) % q
        chi_tau = (chi_tau + uval) % q

    result["chi_theta_modq"] = chi_theta
    result["chi_tau_modq"] = chi_tau
    return result, precomputed


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
    r1, pre = measure_modq(p, Q1)
    t1 = time.time()
    r2, pre = measure_modq(p, Q2, precomputed=pre)
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
              f"timing_q1={r['timing_sec']['q1']:.2f}s timing_q2={r['timing_sec']['q2']:.2f}s",
              flush=True)

    out = {
        "schema": "shadow-atelier/jac_chk2_modq_v1",
        "authority": "裁定806/807 (mod-q rank/trace battery, numpy dense implementation)",
        "method_note": "ALL linear algebra mod q throughout, dense numpy int64 arrays (n x N, "
                       "n~20 rows, N~10^4-10^5 columns) -- vectorized row operations. rank via "
                       "Gaussian elimination over F_q for two large primes Q1,Q2. S3-character "
                       "trace via RREF-pivot shortcut (no linear solve). True integer character "
                       "values recovered via bounded-integer CRT (|chi(g)|<=dim, primes >>dim).",
        "primes_used": {"Q1": Q1, "Q2": Q2},
        "per_p": {str(p): v for p, v in out_per_p.items()},
        "no_verdict_note": "raw ranks, characters, isotypic multiplicities, and booleans only.",
    }
    out_path = f"search/certs/jac_chk2_modq_v1_20260811_p{'_'.join(str(p) for p in targets)}.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
