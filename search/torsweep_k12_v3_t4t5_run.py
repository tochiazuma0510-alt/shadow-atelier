#!/usr/bin/env python3
"""
torsweep_k12_v3_t4t5_run.py -- TOR-SWEEP stages T4/T5 at k=12 (裁定794 go),
generalized from search/torsweep_k11_t4t5_run.py's k=11-standard method
(design docs/notes/tor_sweep_design_v1.md SS3.2 "アルゴリズム TOR-DET" +
SS3.4 table rows T4/T5, 裁定734発注①).

Loads:
  - M from search/certs/torsweep_k12_v1_20260807.json (T1a's exact ambient
    theta/tau constraint matrix, unaffected by 裁定754's H_basis fix).
  - B (H_basis), H_rank from search/certs/torsweep_k12_v3_hnf_kernel_
    20260807.json (裁定754 root-cause-fixed direct integer-kernel
    construction -- automatically saturated).
  - r_prime, dim_S_Q from the LATEST search/certs/torsweep_k12_v3_2_*.json
    (T2/T3 v2 cert, 裁定785 ritual-reuse variant) via glob.

裁定794(1): before starting, B_12's max |entry| was recorded (108 decimal
digits, from the v3_hnf_kernel cert's kernel_construction.max_abs_entry_
in_B field) -- far below k=13's >4300-digit scale, so the STOP condition
("もしk=13級に大きければSTOPして報告") does NOT apply; proceeding.

Same mathematical fact as k=11's script (LAT bullet 1, PBW splits over Z):
r'xr' minors computed directly in ambient-word coordinates give the
correct elementary divisors of N_12: H_12^Z -> t_12^Z without an explicit
Lyndon-coordinate reduction of the 3-letter side.

No judgement words emitted (S-TOR-4): raw values/booleans only.
"""
import glob
import json
import os
import random
import sys
import time
from math import gcd

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
sys.set_int_max_str_digits(0)  # defensive; k=12 entries are ~108 digits,
                                # nowhere near the 4300 default limit, but
                                # cost-free to set (see k=13 script's note).

import edim_semidirect_v1 as ed  # noqa: E402
from torsweep_k12_run import (  # noqa: E402
    det_bareiss, small_primes, center_lift, sha256_of_file,
)

K = 12
EXPECTED_H = 112
EXPECTED_S = 2
V1_CERT_PATH = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k12_v1_20260807.json")
HNF_CERT_PATH = os.path.join(REPO_ROOT, "search", "certs",
                              "torsweep_k12_v3_hnf_kernel_20260807.json")
PIVOT_CERT_PRIME = 2147483647  # reuses one of T2/T3's own RANK_PRIMES
P_EXACT_A = 10 ** 40
P_EXACT_B = 10 ** 40 + 15
NUM_MINORS_TARGET = 5  # design SS3.2 step 4: total s in [3,5], upper end
WALLCLOCK_CAP_SECONDS = 3600  # k<=12 design table cap
RNG_SEED = 20260807

# Checkpointing (added after two consecutive unexplained process deaths --
# no traceback/STOP, process simply vanished mid-computation, r1 at
# ~11154s during modulus B, r2 within minutes of starting -- suspected
# environment-level reaping per the incident record. step1 (~5700s) and
# each modulus's exact_restricted_columns (~5400s) are each expensive
# single computations with no internal progress persistence; checkpoint
# after each so a restart does not repeat already-finished expensive work.
# scratchpad only, per 拘束 (not part of the audited cert chain -- the
# final cert still records everything it always did, from these values).
CKPT_PATH = os.path.join(REPO_ROOT, "scratchpad", "torsweep", "k12_t4t5_checkpoint.json")


def load_checkpoint():
    if os.path.exists(CKPT_PATH):
        with open(CKPT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_checkpoint(ckpt):
    os.makedirs(os.path.dirname(CKPT_PATH), exist_ok=True)
    tmp = CKPT_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(ckpt, f)
    os.replace(tmp, CKPT_PATH)  # atomic on POSIX and Windows (same volume)

random.seed(RNG_SEED)


def find_latest_t23_cert():
    candidates = sorted(glob.glob(os.path.join(
        REPO_ROOT, "search", "certs", "torsweep_k12_v3_2_*.json")))
    if not candidates:
        raise FileNotFoundError(
            "no torsweep_k12_v3_2_*.json (T2/T3 v2, 裁定785) cert found -- "
            "run torsweep_k12_v3_t0t3_run_v2.py first")
    return candidates[-1]


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

    t23_cert_path = find_latest_t23_cert()
    record(f"loading v1 cert (M), v3_hnf_kernel cert (B), {t23_cert_path} (r_prime)")
    with open(V1_CERT_PATH, "r", encoding="utf-8") as f:
        v1 = json.load(f)
    with open(HNF_CERT_PATH, "r", encoding="utf-8") as f:
        hnf = json.load(f)
    with open(t23_cert_path, "r", encoding="utf-8") as f:
        t23cert = json.load(f)

    M = v1["stages"]["T1"]["M"]
    n_cols = v1["stages"]["T1"]["M_shape"][1]
    B = hnf["H_basis"]
    H_rank = hnf["H_rank"]
    max_abs_entry_in_B = hnf["stages"]["kernel_construction"]["max_abs_entry_in_B"]
    assert hnf["stages"]["verification_battery_all_pass"] is True
    t23 = t23cert["stages"]["T2_T3"]
    r_prime = t23["r_prime"]
    assert H_rank == EXPECTED_H, (H_rank, EXPECTED_H)
    assert r_prime == EXPECTED_H - EXPECTED_S, r_prime
    assert t23cert["canaries"]["T-c"]["pass"] is True

    b_digits = len(str(abs(int(max_abs_entry_in_B))))
    record(f"loaded: H_rank={H_rank} r_prime={r_prime} n_cols={n_cols} "
           f"max_abs_entry_in_B_digits={b_digits} (裁定794(1) pre-check: "
           f"NOT k=13-scale [>4300 digits], proceeding)")

    cert = {
        "schema": "tor_sweep_k12_v3.4",
        "ruling_refs": ["裁定734", "裁定745", "裁定754", "裁定785", "裁定794"],
        "supersedes_note": "T0-T3 values carried forward by reference from "
                            "torsweep_k12_v3_hnf_kernel_20260807.json (B, "
                            "H_rank) and " + os.path.relpath(
                                t23_cert_path, REPO_ROOT).replace(os.sep, "/") +
                            " (r_prime, dim_S_Q) -- not recomputed. T4/T5 "
                            "only, per 裁定794(1) go.",
        "pre_check_794_1": {
            "max_abs_entry_in_B_digits": b_digits,
            "k13_scale_threshold_digits": 4300,
            "is_k13_scale": b_digits >= 4300,
            "note": "STOP condition per 裁定794(1) if is_k13_scale were "
                    "True; it is False, proceeding.",
        },
        "design_spec": "docs/notes/tor_sweep_design_v1.md",
        "scope": "T4-T5 only (T0-T3 loaded from prior certs, not recomputed)",
        "k": K,
        "generated_by": {
            "tool": "search/torsweep_k12_v3_t4t5_run.py",
            "python": sys.version,
            "numpy": np.__version__,
            "edim_semidirect_v1_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "edim_semidirect_v1.py")),
            "torsweep_k12_run_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "torsweep_k12_run.py")),
            "rng_seed": RNG_SEED,
        },
        "input_certs": {
            "v1": "search/certs/torsweep_k12_v1_20260807.json",
            "v3_hnf_kernel": "search/certs/torsweep_k12_v3_hnf_kernel_20260807.json",
            "t2_t3": os.path.relpath(t23_cert_path, REPO_ROOT).replace(os.sep, "/"),
        },
        "stages": {},
        "canaries": {},
        "stop_rules": {},
    }
    if b_digits >= 4300:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": f"裁定794(1) STOP condition: max_abs_entry_in_B has "
                      f"{b_digits} digits, k=13-scale, refusing to proceed "
                      f"without further instruction",
        }
        write_cert(cert, log)
        record("STOP: 裁定794(1) k13-scale B entries")
        return

    # =========================================================================
    # Step 1 (TOR-DET step 1-2): get r' pivot AMBIENT column positions from a
    # fresh rank certificate (reuses the already-calibrated production path).
    # =========================================================================
    t_piv_start = time.time()  # also used as the T4-stage elapsed-time
                                # origin below, whether step1 itself is
                                # recomputed or loaded from checkpoint
    ckpt = load_checkpoint()
    if "step1" in ckpt:
        record(f"T4 step1: loaded from checkpoint ({CKPT_PATH}), skipping recomputation")
        r_check = ckpt["step1"]["r_check"]
        pivot_positions = ckpt["step1"]["pivot_positions"]
        tag_boundary = ckpt["step1"]["tag_boundary"]
    else:
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
        pivot_positions = piv_cert["pivot_ambient_row_indices"]
        tag_boundary = piv_cert["row_encoding"]["tag_boundary"]
        ckpt["step1"] = {"r_check": r_check, "pivot_positions": pivot_positions,
                          "tag_boundary": tag_boundary}
        save_checkpoint(ckpt)
        record(f"T4 step1: checkpoint saved ({CKPT_PATH})")

    if r_check != r_prime:
        cert["stop_rules"]["S-TOR-2"] = {
            "triggered": True,
            "reason": f"pivot-certificate rank {r_check} != carried-forward "
                      f"r_prime {r_prime} (regression)",
        }
        write_cert(cert, log)
        record("STOP: S-TOR-2 (pivot rank regression)")
        return

    assert len(pivot_positions) == r_prime

    decoded = []
    for pos in pivot_positions:
        if pos < tag_boundary:
            decoded.append(("n", decode_word(pos, 3, K)))
        else:
            decoded.append(("h", decode_word(pos - tag_boundary, 2, K)))

    # =========================================================================
    # Step 2: EXACT (non-modular) ambient vectors of nu_12(j(y_i)) for each of
    # Lambda_12's 335 Lyndon basis trees y_i, restricted to just the r'=110
    # pivot word coordinates decoded above.
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
        return cols  # dim_h(335) x r_prime(110), exact ints

    if "cols_a" in ckpt:
        record(f"T4 step2: modulus A loaded from checkpoint, skipping recomputation")
        cols_a = ckpt["cols_a"]
    else:
        record("T4 step2: exact ambient columns, modulus A")
        t_exact_start = time.time()
        cols_a = exact_restricted_columns(P_EXACT_A)
        t_exact_a_elapsed = time.time() - t_exact_start
        record(f"T4 step2: modulus A done, elapsed={t_exact_a_elapsed:.2f}s")
        ckpt["cols_a"] = cols_a
        save_checkpoint(ckpt)
        record(f"T4 step2: checkpoint saved (modulus A, {CKPT_PATH})")

    if "cols_b" in ckpt:
        record(f"T4 step2: modulus B loaded from checkpoint, skipping recomputation")
        cols_b = ckpt["cols_b"]
    else:
        record("T4 step2: exact ambient columns, modulus B (independent cross-check)")
        t_exact_b_start = time.time()
        cols_b = exact_restricted_columns(P_EXACT_B)
        t_exact_b_elapsed = time.time() - t_exact_b_start
        record(f"T4 step2: modulus B done, elapsed={t_exact_b_elapsed:.2f}s")
        ckpt["cols_b"] = cols_b
        save_checkpoint(ckpt)
        record(f"T4 step2: checkpoint saved (modulus B, {CKPT_PATH})")

    exact_moduli_agree = (cols_a == cols_b)
    record(f"T4 step2: exact_moduli_agree={exact_moduli_agree}")
    if not exact_moduli_agree:
        cert["stop_rules"]["S-TOR-1b"] = {
            "triggered": True,
            "reason": "LATTICE_CANARY_FAIL (T4 exact-modulus disagreement, "
                      "suspect overflow of P_EXACT or a bug)",
        }
        write_cert(cert, log)
        record("STOP: exact moduli disagree")
        return
    n_source_cols = cols_a  # dim_h(335) x r'=110, exact, trusted

    N_source = [[sum(B[i][j] * n_source_cols[j][c] for j in range(n_cols))
                 for c in range(r_prime)]
                for i in range(H_rank)]  # H_rank(112) x r'(110)
    record(f"T4 step2: N_source assembled, shape=({len(N_source)},{len(N_source[0])})")

    # =========================================================================
    # Step 3-4 (TOR-DET): select s>=3 independent sets of r'=110 rows (out
    # of 112) to form s nonsingular r'xr' Bareiss minors of N_source.
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
        cert["stop_rules"]["S-TOR-1c"] = {
            "triggered": True,
            "reason": f"TOR-DET could only construct {len(minor_dets)} "
                      f"independent r'xr' minors, design requires s>=3",
        }
        write_cert(cert, log)
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
                        import sympy
                        if sympy.isprime(base):
                            factors[base] = factors.get(base, 0) + exp
                        else:
                            unresolved_cofactor = str(base)
                            factors["UNRESOLVED_COMPOSITE"] = str(base)
                    else:
                        factors[base] = factors.get(base, 0) + exp

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
    write_cert(cert, log)
    if os.path.exists(CKPT_PATH):
        os.remove(CKPT_PATH)
        record(f"checkpoint removed ({CKPT_PATH}) -- run completed successfully")
    record(f"DONE. total_elapsed={total_elapsed:.2f}s cert written")


def write_cert(cert, log_lines):
    cert["run_log"] = log_lines
    out_dir = os.path.join(REPO_ROOT, "search", "certs")
    date_str = time.strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"torsweep_k12_v3_4_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print(f"cert written: {out_path}", flush=True)


if __name__ == "__main__":
    main()
