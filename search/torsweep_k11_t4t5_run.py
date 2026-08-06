#!/usr/bin/env python3
"""
torsweep_k11_t4t5_run.py -- TOR-SWEEP stages T4/T5 at k=11 (literal
implementation of docs/notes/tor_sweep_design_v1.md SS3.2 "アルゴリズム
TOR-DET" + SS3.4 table rows T4/T5), 裁定734 発注①.

Loads T0-T3 results from the existing search/certs/torsweep_k11_v1_1_*.json
cert (M, H_basis) rather than recomputing them (裁定734: "v1.2...T0-T3の値を
引き継ぎ欄で参照"). Produces cert v1.2, superseding v1.1.

Scope: ONLY T4 (TOR-DET: s>=3 r'xr' Bareiss minors -> gcd) and, only if
gcd_abs>1, T5 (factor gcd -> per-candidate-prime rank_p confirmation, then
QUAR-TOR SS5.3 quarantine -- NOT published/judged). No judgement words
anywhere ("捩れ支持=∅" etc. are NEVER written); only raw gcd/factor/rank_p
values and booleans (S-TOR-4).

Mathematical fact used (not previously spelled out in torsweep_k11_run.py):
the free Lie algebra Lie_k(A,B,C) (resp. Lie_k(x,y)) is a Z-DIRECT SUMMAND
of the free associative (ambient word) algebra T_k(A,B,C) (resp. T_k(x,y))
-- definition LAT bullet 1 ("PBW splits over Z"). Consequently, for ANY map
f: H_k^Z -> t_k^Z, composing with the split inclusion t_k^Z -> T_k^Z(ambient)
does not change the elementary divisors of f (Smith normal form of [f;0] in
a complementary basis equals that of f). So r'xr' minors computed directly
in ambient-word coordinates (as already used for T2/T3's rank, per that
module's own docstring) give the CORRECT elementary divisors / torsion
primes of N_k: H_k^Z -> t_k^Z, without needing an explicit Lyndon-coordinate
reduction of the n-side (3-letter alphabet, which would be far more costly
at degree 11 -- avoided here for exactly this reason).

Exact (non-modular) arithmetic follows the same technique as T1's exact
theta/tau construction in torsweep_k11_run.py: all of eval_tree_in_t_ambient
/ t_bracket_ambient / delta_hexpr_on_nambient / word_add / word_bracket use
only +,-,* (no division), so evaluating them with an enormous non-prime
modulus p_exact and centre-lifting gives exact integers, cross-checked here
against a second independent modulus.
"""
import hashlib
import json
import os
import random
import sys
import time
from math import gcd

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
import edim_semidirect_v1 as ed  # noqa: E402
from torsweep_k11_run import (  # noqa: E402
    det_bareiss, small_primes, row_dependency_mod_p, center_lift,
    sha256_of_file,
)

K = 11
EXPECTED_H = 62
EXPECTED_S = 2
V1_1_CERT_PATH = os.path.join(REPO_ROOT, "search", "certs",
                               "torsweep_k11_v1_1_20260807.json")
PIVOT_CERT_PRIME = 2147483647  # reuses one of T2/T3's own RANK_PRIMES
P_EXACT_A = 10**40
P_EXACT_B = 10**40 + 15
NUM_MINORS_TARGET = 5  # design SS3.2 step 4: "あと2-4本" i.e. total s in [3,5]; upper end
WALLCLOCK_CAP_SECONDS = 3600
RNG_SEED = 20260807

random.seed(RNG_SEED)


def decode_word(idx, alphabet_size, degree):
    digits = []
    tmp = idx
    for _ in range(degree):
        digits.append(tmp % alphabet_size)
        tmp //= alphabet_size
    return tuple(reversed(digits))


def main():
    log = []
    t_script_start = time.time()

    def record(msg):
        line = f"[{time.time() - t_script_start:8.2f}s] {msg}"
        print(line, flush=True)
        log.append(line)

    record("loading v1.1 cert (T0-T3 values, not recomputed)")
    with open(V1_1_CERT_PATH, "r", encoding="utf-8") as f:
        v1_1 = json.load(f)
    t1 = v1_1["stages"]["T1"]
    t23 = v1_1["stages"]["T2_T3"]
    M = t1["M"]
    B = t1["H_basis"]
    H_rank = t1["H_rank"]
    r_prime = t23["r_prime"]
    assert H_rank == EXPECTED_H, (H_rank, EXPECTED_H)
    assert r_prime == EXPECTED_H - EXPECTED_S, r_prime
    n_cols = t1["M_shape"][1]
    record(f"loaded: H_rank={H_rank} r_prime={r_prime} n_cols={n_cols}")

    cert = {
        "schema": "tor_sweep_k11_v1.2",
        "supersedes": "search/certs/torsweep_k11_v1_1_20260807.json",
        "supersedes_note": "T0-T3 values are carried forward by reference "
                            "(see t0_t3_summary below) from the v1.1 cert, "
                            "not recomputed. v1.1 in turn supersedes v1 "
                            "(the original T0-STOP cert).",
        "t0_t3_summary": {
            "witt2": v1_1["stages"]["T0"]["witt2"],
            "witt3": v1_1["stages"]["T0"]["witt3"],
            "t_rank": v1_1["stages"]["T0"]["t_rank"],
            "H_rank": H_rank,
            "r_prime": r_prime,
            "dim_S_Q_byproduct": t23["dim_S_Q_byproduct"],
            "canaries_T_a_T_b_T_c_all_pass": all(
                v1_1["canaries"][c]["pass"] for c in ("T-a", "T-b", "T-c")),
        },
        "design_spec": "docs/notes/tor_sweep_design_v1.md",
        "scope": "T4-T5 only (T0-T3 loaded from v1.1, not recomputed)",
        "k": K,
        "generated_by": {
            "tool": "search/torsweep_k11_t4t5_run.py",
            "python": sys.version,
            "numpy": np.__version__,
            "edim_semidirect_v1_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "edim_semidirect_v1.py")),
            "torsweep_k11_run_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "torsweep_k11_run.py")),
            "rng_seed": RNG_SEED,
        },
        "stages": {},
        "canaries": {},
        "stop_rules": {},
    }

    # =========================================================================
    # Step 1 (TOR-DET step 1-2): get r' pivot AMBIENT column positions from a
    # fresh rank certificate (reuses the already-calibrated production path).
    # =========================================================================
    record("T4 step1: rank_nu_j_on_subspace_ambient (one prime) for pivot columns")
    t_piv_start = time.time()
    h_alg2_piv = ed.GradedLie(2, K, PIVOT_CERT_PRIME)
    subspace_basis_modq = np.array(
        [[v % PIVOT_CERT_PRIME for v in row] for row in B], dtype=np.int64).T
    r_check = ed.rank_nu_j_on_subspace_ambient(
        K, h_alg2_piv, subspace_basis_modq, PIVOT_CERT_PRIME)
    piv_cert = h_alg2_piv._last_nu_rank_certificate
    t_piv_elapsed = time.time() - t_piv_start
    record(f"T4 step1: r_check={r_check} (expect {r_prime}) elapsed={t_piv_elapsed:.2f}s")
    if r_check != r_prime:
        cert["stop_rules"]["S-TOR-2"] = {
            "triggered": True,
            "reason": f"pivot-certificate rank {r_check} != carried-forward "
                      f"r_prime {r_prime} (regression)",
        }
        write_cert(cert)
        record("STOP: S-TOR-2 (pivot rank regression)")
        return

    pivot_positions = piv_cert["pivot_ambient_row_indices"]
    tag_boundary = piv_cert["row_encoding"]["tag_boundary"]
    assert len(pivot_positions) == r_prime
    n_ambient_dim = 3 ** K
    h_ambient_dim = 2 ** K

    decoded = []
    for pos in pivot_positions:
        if pos < tag_boundary:
            decoded.append(("n", decode_word(pos, 3, K)))
        else:
            decoded.append(("h", decode_word(pos - tag_boundary, 2, K)))

    # =========================================================================
    # Step 2: EXACT (non-modular) ambient vectors of nu_11(j(y_i)) for each of
    # Lambda_11's 186 Lyndon basis trees y_i, restricted to just the r'=60
    # pivot word coordinates decoded above (everything else discarded
    # immediately to keep memory bounded).
    # =========================================================================
    def exact_restricted_columns(p_exact):
        h_alg2_exact = ed.GradedLie(2, K, p_exact, sparse_degrees={K})
        dim_h = h_alg2_exact.dim[K]
        assert dim_h == n_cols
        state_leaf_images = ed._rho_power_h_leaf_images_ambient(p_exact)
        base_table = ed._delta_base_table(p_exact)
        tree_caches = [dict() for _ in range(5)]
        subtree_counts, cache_allowed = ed._subtree_cache_policy_for_roots(
            h_alg2_exact.trees[K])
        cols = [[0] * r_prime for _ in range(dim_h)]
        for basis_index, tree in enumerate(h_alg2_exact.trees[K]):
            nu_n = {}
            nu_h = {}
            for power in range(5):
                action_cache = {}
                n_part, h_part, h_expr, degree = ed.eval_tree_in_t_ambient(
                    tree, state_leaf_images[power], p_exact,
                    cache=tree_caches[power], base_table=base_table,
                    action_cache=action_cache, cache_result=False,
                    cache_allowed=cache_allowed)
                assert degree == K
                nu_n = ed.word_add([nu_n, n_part], p_exact)
                nu_h = ed.word_add([nu_h, h_part], p_exact)
            row = []
            for kind, word in decoded:
                raw = (nu_n if kind == "n" else nu_h).get(word, 0)
                row.append(center_lift(raw, p_exact))
            cols[basis_index] = row
        return cols  # dim_h(186) x r_prime(60), exact ints

    record("T4 step2: exact ambient columns, modulus A")
    t_exact_start = time.time()
    cols_a = exact_restricted_columns(P_EXACT_A)
    t_exact_a_elapsed = time.time() - t_exact_start
    record(f"T4 step2: modulus A done, elapsed={t_exact_a_elapsed:.2f}s")

    record("T4 step2: exact ambient columns, modulus B (independent cross-check)")
    t_exact_b_start = time.time()
    cols_b = exact_restricted_columns(P_EXACT_B)
    t_exact_b_elapsed = time.time() - t_exact_b_start
    record(f"T4 step2: modulus B done, elapsed={t_exact_b_elapsed:.2f}s")

    exact_moduli_agree = (cols_a == cols_b)
    record(f"T4 step2: exact_moduli_agree={exact_moduli_agree}")
    if not exact_moduli_agree:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": "LATTICE_CANARY_FAIL (T4 exact-modulus disagreement, "
                      "suspect overflow of P_EXACT or a bug)",
        }
        write_cert(cert)
        record("STOP: exact moduli disagree")
        return
    n_source_cols = cols_a  # dim_h(186) x r_prime(60), exact, trusted

    # N_source = B (H_rank=62 x 186) @ n_source_cols (186 x r'=60), exact
    N_source = [[sum(B[i][j] * n_source_cols[j][c] for j in range(n_cols))
                 for c in range(r_prime)]
                for i in range(H_rank)]  # H_rank(62) x r'(60)
    record(f"T4 step2: N_source assembled, shape=({len(N_source)},{len(N_source[0])})")

    # =========================================================================
    # Step 3-4 (TOR-DET): select s>=3 independent sets of r'=60 rows (out of
    # 62) to form s nonsingular r'xr' Bareiss minors of N_source.
    # =========================================================================
    def independent_rows_modp(rows_as_matrix, p, order):
        pivots = {}
        selected = []
        for r in order:
            row = rows_as_matrix[r]
            vec = {c: row[c] % p for c in range(len(row)) if row[c] % p}
            while vec:
                piv = min(vec)
                old = pivots.get(piv)
                if old is None:
                    inv = pow(vec[piv], p - 2, p)
                    vec = {c: (v * inv) % p for c, v in vec.items() if v % p}
                    pivots[piv] = vec
                    selected.append(r)
                    break
                factor = vec[piv]
                for c, v in old.items():
                    nv = (vec.get(c, 0) - factor * v) % p
                    if nv:
                        vec[c] = nv
                    else:
                        vec.pop(c, None)
            if len(selected) == len(rows_as_matrix[0]):
                break
        return selected

    big_prime = PIVOT_CERT_PRIME
    orders = [list(range(H_rank))]
    for _ in range(NUM_MINORS_TARGET + 2):
        o = list(range(H_rank))
        random.shuffle(o)
        orders.append(o)
    orders.append(list(reversed(range(H_rank))))

    minor_dets = []
    minor_row_sets = []
    seen = set()
    for order in orders:
        rows_sel = independent_rows_modp(N_source, big_prime, order)
        if len(rows_sel) != r_prime:
            continue
        key = tuple(sorted(rows_sel))
        if key in seen:
            continue
        seen.add(key)
        submat = [N_source[i] for i in rows_sel]
        d = det_bareiss(submat)
        if d == 0:
            continue  # shouldn't happen if truly independent mod big_prime
        minor_dets.append(d)
        minor_row_sets.append(rows_sel)
        if len(minor_dets) >= NUM_MINORS_TARGET:
            break
    record(f"T4: computed {len(minor_dets)} minors, "
           f"digit_counts={[len(str(d)) for d in minor_dets]}")

    if len(minor_dets) < 3:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": f"TOR-DET could only construct {len(minor_dets)} "
                      f"independent r'xr' minors, design requires s>=3",
        }
        write_cert(cert)
        record("STOP: fewer than 3 independent minors found")
        return

    gcd_abs = 0
    for d in minor_dets:
        gcd_abs = gcd(gcd_abs, abs(d))
    record(f"T4: gcd_abs digits={len(str(gcd_abs))} value_leading={str(gcd_abs)[:20]}")

    cert["stages"]["T4"] = {
        "pivot_cert_prime": PIVOT_CERT_PRIME,
        "pivot_ambient_positions_count": len(pivot_positions),
        "exact_modulus_A": str(P_EXACT_A),
        "exact_modulus_B": str(P_EXACT_B),
        "exact_moduli_agree": exact_moduli_agree,
        "N_source_shape": [len(N_source), len(N_source[0])],
        # N_source itself is recorded (small: H_rank x r' = 62x60 exact
        # ints) so the independent checker can recompute minor determinants
        # from scratch, and so a future run can add MORE minors without
        # repeating the ~40-minute exact two-modulus construction above.
        "N_source": N_source,
        "decoded_pivot_positions": [[kind, list(word)] for kind, word in decoded],
        "minor_determinants": [str(d) for d in minor_dets],
        "minor_determinant_digit_counts": [len(str(d)) for d in minor_dets],
        "minor_row_sets": minor_row_sets,
        "gcd_abs": str(gcd_abs),
        "gcd_abs_digits": len(str(gcd_abs)),
        "elapsed_seconds": time.time() - t_piv_start,
    }
    cert["canaries"]["T-P-T-1"] = {
        "note": "P-T-1 prediction check (raw value only, no judgement word): "
                "gcd_abs == 1 iff the prediction holds for this run",
        "gcd_abs_equals_1": (gcd_abs == 1),
    }

    # =========================================================================
    # T5: only if gcd_abs > 1 -- factor, then per-candidate-prime rank check.
    # =========================================================================
    if gcd_abs == 1:
        cert["stages"]["T5"] = {"triggered": False,
                                 "reason": "gcd_abs == 1, TOR-DET SS3.2 step 5 "
                                           "first bullet applies, T5 not run"}
        record("T5: not triggered (gcd_abs == 1)")
    else:
        record("T5: gcd_abs != 1, factoring and per-candidate rank_p checks "
               "(QUAR-TOR SS5.3 -- not a judgement, raw values only)")
        rem = gcd_abs
        trial_bound = 2_000_000
        factors = {}
        exhausted_without_full_factorization = True
        for p in small_primes(trial_bound):
            if p * p > rem:
                exhausted_without_full_factorization = False
                break
            while rem % p == 0:
                factors[p] = factors.get(p, 0) + 1
                rem //= p
        if rem > 1:
            if exhausted_without_full_factorization:
                factors[f"UNFACTORED_COFACTOR>{trial_bound}"] = str(rem)
            else:
                factors[rem] = factors.get(rem, 0) + 1
                rem = 1

        # If trial division left a residual composite cofactor, make a
        # best-effort attempt with sympy's factorint (Pollard rho / p-1 /
        # ECM as available) before giving up -- but do NOT silently accept
        # an unresolved cofactor as "innocent"; record its status honestly.
        unresolved_cofactor = None
        for key in list(factors):
            if isinstance(key, str) and key.startswith("UNFACTORED_COFACTOR"):
                cof = int(factors.pop(key))
                record(f"T5: attempting sympy.factorint on the {len(str(cof))}-digit "
                       f"residual cofactor (best effort, bounded)")
                t_fact_start = time.time()
                try:
                    import sympy
                    sub_factors = sympy.factorint(cof, limit=10_000_000)
                except Exception as exc:
                    sub_factors = {cof: 1}
                    record(f"T5: factorint raised {exc!r}, treating cofactor as unresolved")
                record(f"T5: factorint attempt took {time.time()-t_fact_start:.1f}s, "
                       f"found {dict(sub_factors)}")
                for base, exp in sub_factors.items():
                    base = int(base)
                    if base > 10_000_000:
                        # factorint couldn't further reduce it below the
                        # limit -- could be prime or a product of primes
                        # each > limit; check primality explicitly.
                        import sympy
                        if sympy.isprime(base):
                            factors[base] = factors.get(base, 0) + exp
                        else:
                            unresolved_cofactor = str(base)
                            factors[f"UNRESOLVED_COMPOSITE"] = str(base)
                    else:
                        factors[base] = factors.get(base, 0) + exp

        # Two-tier check per candidate prime p (mirrors the T-b saturation
        # fix): a CHEAP test first -- rank_p(N_source) using the already-
        # computed exact 62x60 minor-source matrix (independent_rows_modp,
        # instant). If N_source already has full rank r' mod p, that alone
        # PROVES p cannot divide d_{r'} (the true elementary divisor) --
        # because r'=rank_Q(N_k) is the maximum possible rank at any prime,
        # so witnessing rank_p(N_source)=r' via THIS SPECIFIC r'xr' column
        # selection already exhibits a nonsingular r'xr' minor mod p, which
        # is exactly what "p does not divide d_{r'}" means. Only if
        # N_source itself is singular mod p (inconclusive -- could be an
        # artifact of this one column choice, exactly as the T-b sat_gcd
        # false positives were) does this escalate to the EXPENSIVE full
        # rank_nu_j_on_subspace_ambient call (which was the sole tool used
        # in the first draft of this stage and made T5 impractically slow
        # when gcd_abs had ~dozens of small-prime factors, per this run's
        # own development history).
        torsion_primes = []
        jump_at_p = {}
        for p in factors:
            if not isinstance(p, int):
                continue
            cheap_rank = len(independent_rows_modp(N_source, p, list(range(H_rank))))
            if cheap_rank == r_prime:
                jump_at_p[str(p)] = {"rank_p": int(cheap_rank), "r_prime": r_prime,
                                      "jumps": False, "method": "cheap_N_source_rank"}
                continue
            record(f"T5: prime {p} inconclusive via N_source (cheap rank "
                   f"{cheap_rank} < {r_prime}) -- escalating to full "
                   f"rank_nu_j_on_subspace_ambient check")
            h_alg2_p = ed.GradedLie(2, K, p)
            subspace_basis_p = np.array(
                [[v % p for v in row] for row in B], dtype=np.int64).T
            rank_p = ed.rank_nu_j_on_subspace_ambient(K, h_alg2_p, subspace_basis_p, p)
            jump_at_p[str(p)] = {"rank_p": int(rank_p), "r_prime": r_prime,
                                  "jumps": (rank_p < r_prime),
                                  "method": "full_rank_nu_j_on_subspace_ambient",
                                  "cheap_N_source_rank": int(cheap_rank)}
            if rank_p < r_prime:
                torsion_primes.append(p)
        cert["stages"]["T5"] = {
            "triggered": True,
            "gcd_abs_prime_factors": {str(k): v for k, v in factors.items()},
            "torsion_primes": torsion_primes,
            "jump_at_p": jump_at_p,
            "unresolved_cofactor": unresolved_cofactor,
            "factorization_fully_resolved": (unresolved_cofactor is None),
        }
        record(f"T5: torsion_primes(raw)={torsion_primes} "
               f"factorization_fully_resolved={unresolved_cofactor is None}")
        if unresolved_cofactor is not None:
            record(f"T5: WARNING -- residual cofactor NOT fully factored "
                   f"({len(unresolved_cofactor)} digits), its status as a "
                   f"torsion candidate is UNDETERMINED, not 'confirmed "
                   f"innocent' -- must not be silently dropped")
        if torsion_primes:
            record("QUAR-TOR SS5.3 step1: quarantine -- recorded in cert only, "
                   "not published as a finding, no judgement word emitted, "
                   "awaiting 司令塔 review before any further step")
            cert["stop_rules"]["QUAR-TOR"] = {
                "triggered": True,
                "quarantined_primes": torsion_primes,
                "note": "recorded per QUAR-TOR SS5.3 -- judgement word "
                        "deliberately withheld; 司令塔 disposition required "
                        "before this is treated as a finding",
            }

    total_elapsed = time.time() - t_script_start
    cert["stop_rules"]["S-TOR-3"] = {
        "wallclock_cap_seconds": WALLCLOCK_CAP_SECONDS,
        "total_elapsed_seconds": total_elapsed,
        "within_cap": total_elapsed <= WALLCLOCK_CAP_SECONDS,
    }
    cert["stop_rules"]["S-TOR-4"] = {
        "note": "no judgement words emitted anywhere in this cert; raw "
                "values and booleans only",
    }
    cert["total_elapsed_seconds"] = total_elapsed
    cert["run_log"] = log
    write_cert(cert)
    record(f"DONE. total_elapsed={total_elapsed:.2f}s cert written")


def write_cert(cert):
    out_dir = os.path.join(REPO_ROOT, "search", "certs")
    os.makedirs(out_dir, exist_ok=True)
    date_str = time.strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"torsweep_k11_v1_2_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print(f"cert written: {out_path}", flush=True)


if __name__ == "__main__":
    main()
