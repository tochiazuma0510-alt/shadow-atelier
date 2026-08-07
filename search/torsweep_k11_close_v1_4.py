#!/usr/bin/env python3
"""
torsweep_k11_close_v1_4.py -- closes k=11 per 裁定737(3)/裁定739: full-column
adaptive-pivot Howell elimination modulo M over the FULL (not fixed-60-column)
N_11 = nu_11 o j |_H matrix, reconstructed exactly from cert v1.1's embedded
H_basis (裁定738 handoff note said N_11 itself was also embedded in v1.1 --
this is FALSE, cert v1.1 only has M (theta/tau) and H_basis; the discrepancy
was reported and corrected by 司令塔 in 裁定739, which approved proceeding
with reconstruction from H_basis alone).

裁定739 additional requirement (verbatim): record an empirical bound on the
absolute value of matrix entries, and either (a) scan with a prime exceeding
that bound (deterministic "0 mod p iff 0 over Z"), or (b) if no single
int64-safe prime exceeds the bound, fall back to two-independent-modulus
agreement (as already used throughout this repo for T1/T4's P_EXACT_A/B) and
say so explicitly. Individual N_source entries in cert v1.2 reach 14 digits
(~10^14), far beyond any int64-safe prime (~2^31 ~ 2.1e9, 10 digits), so (b)
applies here: this script uses TWO independent huge NON-PRIME moduli
(P_EXACT_A = 10**40, P_EXACT_B = 10**40+15), the same technique already
validated in torsweep_k11_run.py (T1) and torsweep_k11_t4t5_run.py (T4), and
requires byte-for-byte agreement of the two reconstructions as the exactness
witness (documented explicitly in the cert, per 裁定739).

"Full column" reinterpretation (also cleared by 裁定739): the design note's
"62x16,290" figure names dim(t_11) = Witt(3,11)+Witt(2,11), the INTRINSIC
free-Lie-algebra dimension. The actual production code (rank_nu_j_on_subspace_
ambient in edim_semidirect_v1.py) represents nu_11 o j in WORD-AMBIENT
coordinates (3**11 + 2**11 = 179,195 columns), not the intrinsic Lyndon
coordinatization of t_11 -- this is deliberate (PBW embedding is injective,
so elementary divisors of the restricted map are unchanged by composing with
the ambient inclusion; see torsweep_k11_t4t5_run.py's own module docstring).
"Full columns" is therefore read here as: every ambient word position that is
NONZERO in at least one of the 62 output rows (columns that are identically
zero across all 62 rows contribute nothing to rank or elementary divisors,
so dropping them is exact, not an approximation). Empirically (this run) that
support turns out to be nearly the entire 179,195-dimensional ambient space
(individual basis trees already touch ~85-99% of the 3**11=177,147-dim "n"
side alone), so in practice "full support columns" and "full ambient
columns" coincide almost exactly; this script uses the measured support set,
not a hardcoded guess.

Method (裁定737(3) + 裁定741 bugfix, corrected spec): at each of r_prime=60
(NOT H_rank=62 -- 裁定741 caught this: H_rank=62 is the SOURCE dimension,
r_prime=60=rank_Q(N_11) established by T2/T3 is the actual number of
linearly-independent pivots that can ever exist) elimination steps, search
ALL remaining live columns of the residual (not a fixed subset) for an
entry e with gcd(e, M) == 1 (a "unit pivot" mod M). Once r_prime pivots are
found, the H_rank-r_prime=2 remaining ("dependent") rows are checked for
being IDENTICALLY ZERO mod M across every live column. Outcomes:
  (i)   r_prime unit pivots found AND the 2 dependent rows are identically
        zero mod M everywhere -> every prime factor of M is innocent (rank
        stays r_prime=60 simultaneously mod every prime dividing M), proved
        WITHOUT factoring M.
  (ii)  a step finds no unit pivot anywhere, but some entry e in that
        step's residual (or, after r_prime pivots, a nonzero entry in a
        dependent row) has gcd(e, M) = g with 1 < g < M -> M splits for
        free into g and M/g (no trial division/ECM used); recurse on each
        piece.
  (iii) fewer than r_prime unit pivots found even using the COMPLETE live
        column set -> genuine rank drop mod (a divisor of) M -- STOP, raw
        values only, no judgement word, escalate per QUAR-TOR SS5.3.
"insufficient" (as seen in v1.3, from the FIXED 60-column N_source) is not a
possible outcome of this method when the FULL support is used (for reaching
the CORRECT target r_prime=60), because a genuine full-rank map has, by
definition, a nonsingular r'xr' minor somewhere among ALL its columns --
Howell elimination over the complete column set will always find it (mod
any prime not dividing that minor's determinant); it just might not be
among a pre-selected fixed 60.

***裁定741 self-correction record***: this script's FIRST version of this
method targeted H_rank=62 pivots (a bug), which is UNREACHABLE by
construction (rank_Q=60 < 62), producing "insufficient" at every batch
size up to and including the full 170,766-column set (10 consecutive
attempts, logged in the run history) purely as an artifact of the wrong
target -- not evidence of anything mathematical. 司令塔 caught this from
the reported attempt count (62) immediately upon seeing the speed-route
report. Confirmed independently via a small-modulus (M'=2*5*11393, all 3
factors already known-innocent) sanity check against the SAME reconstructed
matrix: it reproduced the exact predicted symptom (a degenerate "split" at
gcd(0,M')=M', triggered right after the 60th real pivot, i.e. exactly at
pivots_before_split=60 in 4/5 trials).

Target modulus M: the 71-digit unresolved residual named explicitly in cert
v1.3's own critical_limitation_found field as the next step
(53357876975946793169866005449844891373975644778775545810346141045350061 =
11393 x <67-digit UNRESOLVED_COMPOSITE from v1.2>). 11393 was ALREADY
confirmed innocent independently in v1.2 T5 via the full (not N_source-only)
rank_nu_j_on_subspace_ambient check, so including it in M here is redundant
but harmless -- it gives this new method a chance to re-derive an
already-known-true fact as a sanity check on the method itself (mirroring
what 裁定737's own retrospective did with primes 2 and 5).
"""
import hashlib
import json
import os
import pickle
import random
import sys
import time
from math import gcd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
import edim_semidirect_v1 as ed  # noqa: E402
from torsweep_k11_run import center_lift, ext_gcd, sha256_of_file, small_primes  # noqa: E402

K = 11
EXPECTED_H = 62
EXPECTED_R_PRIME = 60
V1_1_CERT_PATH = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k11_v1_1_20260807.json")
V1_2_CERT_PATH = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k11_v1_2_20260807.json")
V1_3_CERT_PATH = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k11_v1_3_20260807.json")

P_EXACT_A = 10 ** 40
P_EXACT_B = 10 ** 40 + 15

TARGET_M = 53357876975946793169866005449844891373975644778775545810346141045350061

# 裁定742①: mandatory canary primes for the post-reconstruction rank gate,
# all already independently confirmed innocent (rank_p==60) via v1.2's T5
# (2,5,11393 directly; 3 indirectly -- it never appears as a factor of
# gcd_abs across ~20 sampled 60x60 minors, meaning at least one sampled
# minor is already nonsingular mod 3, which alone forces rank_3>=60=max).
CANARY_PRIMES = [2, 3, 5, 11393]

ROBUSTNESS_TRIALS = 8
RNG_SEED = 20260807
random.seed(RNG_SEED)

# Checkpoint (裁定740 aftermath: the first attempt was killed ~38 minutes in,
# right after the expensive FULL1/FULL2 stages succeeded, just as FULL3
# began -- to avoid repeating that ~2300s of work on a retry, the exact
# reconstruction result and its cert fragments are pickled here BEFORE the
# Howell elimination starts, and reloaded automatically if present.
# 裁定742 hygiene: this is scratch (not a work product), so it lives in the
# scratchpad, not search/certs/ -- certs is for committed output only.)
CHECKPOINT_PATH = os.path.join(
    r"C:\Users\81905\AppData\Local\Temp\claude\C--Users-81905-Desktop-shadow-atelier"
    r"\d2b80bbe-2be7-426c-9dbe-a39ba301883a\scratchpad",
    "_torsweep_k11_v1_4_checkpoint.pkl")


def record_factory():
    log = []
    t0 = time.time()

    def record(msg):
        line = f"[{time.time() - t0:8.2f}s] {msg}"
        print(line, flush=True)
        log.append(line)
    return record, log, t0


def exact_full_rows(K_, B, H_rank, dim_h, p_exact, record):
    """Returns H_rank sparse dict rows {(kind,word_tuple): int_value},
    keeping ONLY entries nonzero after summing the B-weighted contributions
    of ALL dim_h Lambda_11 Lyndon basis trees (not restricted to any
    pre-selected column subset). kind in {'n','h'}; word_tuple is the
    decoded ambient word (see torsweep_k11_t4t5_run.py's decode_word)."""
    h_alg2_exact = ed.GradedLie(2, K_, p_exact, sparse_degrees={K_})
    dim_h_check = h_alg2_exact.dim[K_]
    assert dim_h_check == dim_h, (dim_h_check, dim_h)
    state_leaf_images = ed._rho_power_h_leaf_images_ambient(p_exact)
    base_table = ed._delta_base_table(p_exact)
    tree_caches = [dict() for _ in range(5)]
    subtree_counts, cache_allowed = ed._subtree_cache_policy_for_roots(h_alg2_exact.trees[K_])

    rows = [dict() for _ in range(H_rank)]
    n_ambient_dim = 3 ** K_
    h_ambient_dim = 2 ** K_

    for basis_index, tree in enumerate(h_alg2_exact.trees[K_]):
        coeffs = [B[i][basis_index] for i in range(H_rank)]
        active_rows = [i for i, c in enumerate(coeffs) if c != 0]
        if not active_rows:
            continue
        nu_n = {}
        nu_h = {}
        for power in range(5):
            action_cache = {}
            n_part, h_part, h_expr, degree = ed.eval_tree_in_t_ambient(
                tree, state_leaf_images[power], p_exact,
                cache=tree_caches[power], base_table=base_table,
                action_cache=action_cache, cache_result=False,
                cache_allowed=cache_allowed)
            if degree != K_:
                raise ValueError("ambient rho evaluation returned wrong degree")
            nu_n = ed.word_add([nu_n, n_part], p_exact)
            nu_h = ed.word_add([nu_h, h_part], p_exact)

        for word, raw in nu_n.items():
            val = center_lift(raw, p_exact)
            if val == 0:
                continue
            key = ("n", word)
            for i in active_rows:
                c = coeffs[i]
                rows[i][key] = rows[i].get(key, 0) + c * val
        for word, raw in nu_h.items():
            val = center_lift(raw, p_exact)
            if val == 0:
                continue
            key = ("h", word)
            for i in active_rows:
                c = coeffs[i]
                rows[i][key] = rows[i].get(key, 0) + c * val

        if (basis_index + 1) % 20 == 0 or basis_index == dim_h - 1:
            nnz_now = sum(len(r) for r in rows)
            record(f"  exact_full_rows(p={str(p_exact)[:6]}...): "
                    f"{basis_index+1}/{dim_h} trees done, running total "
                    f"nnz across {H_rank} rows = {nnz_now}")

    # drop entries that cancelled to exactly 0 after full accumulation
    for i in range(H_rank):
        rows[i] = {k: v for k, v in rows[i].items() if v != 0}
    return rows, n_ambient_dim, h_ambient_dim


def howell_unit_pivot_mod_M_batch(cols_batch, M, col_order, row_priority, r_prime):
    """Full-column adaptive-pivot Howell elimination mod M (裁定737(3)),
    run over a SUBSET ("batch") of columns supplied by the caller.

    ***裁定741 bugfix***: the target pivot count is r_prime (the KNOWN
    Q-rank of the map, =60, established independently by T2/T3's 3-large-
    -prime rank cross-check, cert v1.1), NOT H_rank (=62, the number of
    ROWS/basis vectors of H_11, i.e. the SOURCE dimension). H_rank > r_prime
    here precisely because dim S_11(Q) = H_rank - r_prime = 2 (the byproduct
    that IS the whole point of T2/T3): there are only ever r_prime=60
    linearly-independent pivots to find, over ANY field/ring, because the
    map's rank over Q is 60. Requiring 62 unit pivots (this script's
    original, WRONG target, caught by 司令塔裁定741) is unreachable by
    construction, independent of any question of torsion -- every one of
    the 10 earlier "insufficient" results at every batch size including
    the full 170,766-column set was this bug, not evidence of anything
    mathematical (confirmed directly: a small-modulus M'=2*5*11393 sanity
    test against this same cols data hit the exact predicted symptom --
    "split" triggered at pivots_before_split=60 via the degenerate
    gcd(0, M')=M' artifact of the unreachable-62nd-pivot search).

    Once r_prime unit pivots are found, this function STOPS searching for
    more (there are none to find) and instead scans the reduced state of
    the H_rank - r_prime REMAINING (non-pivot) rows across every column in
    col_order that was actually visited, checking whether they are
    IDENTICALLY ZERO mod M. This is the correct positive criterion (裁定741):
    if the map is genuinely torsion-free at every prime dividing M, the
    r_prime=60 pivot rows' Z-span, when reduced against the OTHER 2 rows,
    forces those 2 rows to vanish EXACTLY mod M (not merely appear "stuck"
    with some ad hoc leftover value) -- because the 2 extra rows are, by
    the H-basis's own saturation (T-b canary, already independently
    confirmed), Z-linear (not just Q-linear) combinations of some spanning
    set once the correct unimodular row reduction is applied to the FULL
    rank-60 image; any residual nonzero entry surviving mod M in a
    "dependent" row after reduction is precisely a torsion witness.

    cols_batch: dict col_key -> list of length H_rank (dense per-column,
    values already reduced mod M). Mutates its OWN copy; does NOT mutate
    the caller's cols_batch dict's list objects -- this is DELIBERATE and
    load-bearing for correctness, not just caution: close_modulus_full's
    recursion on a 'split' calls this twice with the SAME `cols` for two
    DIFFERENT child moduli (g and M//g); if this function mutated the
    caller's dict in place, the second recursive call would see corrupted
    (already-reduced-for-a-different-modulus) data. (A memory-motivated
    in-place variant was tried and reverted during this run's own
    development for exactly this reason -- recorded here as the lesson,
    not repeated as a TODO.) Memory pressure instead addressed by deleting
    `rows` promptly once `cols` is built (see phase2_canary_and_howell)."""
    H_rank = len(row_priority)
    row_rank = {row: i for i, row in enumerate(row_priority)}
    A = {ck: v[:] for ck, v in cols_batch.items()}
    active = set(range(H_rank))
    pivots_found = []

    for col in col_order:
        if len(pivots_found) == r_prime:
            break
        colvec = A.get(col)
        if colvec is None:
            continue
        while True:
            nz = sorted((i for i in active if colvec[i] % M != 0),
                        key=lambda i: row_rank[i])
            if len(nz) <= 1:
                break
            i0, i1 = nz[0], nz[1]
            a, b = colvec[i0], colvec[i1]
            g, x, y = ext_gcd(a, b)
            ag, bg = a // g, b // g
            new_i0 = {}
            new_i1 = {}
            for ck, vec in A.items():
                v0, v1 = vec[i0], vec[i1]
                new_i0[ck] = (x * v0 + y * v1) % M
                new_i1[ck] = (ag * v1 - bg * v0) % M
            for ck in A:
                A[ck][i0] = new_i0[ck]
                A[ck][i1] = new_i1[ck]
            colvec = A[col]
        nz = sorted((i for i in active if colvec[i] % M != 0),
                    key=lambda i: row_rank[i])
        if not nz:
            continue
        piv_row = nz[0]
        pivot_val = colvec[piv_row]
        g = gcd(pivot_val, M)
        if g != 1:
            return {"status": "split", "factor": g, "pivot_col": col,
                    "pivots_before_split": len(pivots_found)}
        inv = pow(pivot_val, -1, M)
        piv_row_vals = {ck: (vec[piv_row] * inv) % M for ck, vec in A.items()}
        for ck, vec in A.items():
            vec[piv_row] = piv_row_vals[ck]
        for i in list(active):
            if i == piv_row:
                continue
            f = A[col][i]
            if f % M != 0:
                pv = piv_row_vals
                for ck, vec in A.items():
                    vec[i] = (vec[i] - f * pv[ck]) % M
        pivots_found.append((col, piv_row))
        active.discard(piv_row)

    if len(pivots_found) < r_prime:
        return {"status": "insufficient", "pivots_found": len(pivots_found),
                "target": r_prime}

    # r_prime pivots found. Now reduce EVERY remaining live column against
    # those r_prime pivots (not just the ones already visited in col_order
    # up to this point) and check whether the H_rank-r_prime dependent rows
    # go identically to zero mod M everywhere.
    remaining_rows = sorted(active)
    nonzero_witnesses = []
    for col in col_order:
        colvec = A.get(col)
        if colvec is None:
            continue
        for i in remaining_rows:
            v = colvec[i] % M
            if v != 0:
                nonzero_witnesses.append({"col": col, "row": i, "value_mod_M": v,
                                           "gcd_with_M": gcd(v, M)})
    if not nonzero_witnesses:
        return {"status": "success", "pivots": pivots_found,
                "remaining_rows": remaining_rows,
                "zero_check_columns": len(col_order)}
    return {"status": "residual_nonzero", "pivots": pivots_found,
            "remaining_rows": remaining_rows,
            "nonzero_witnesses": nonzero_witnesses[:50],
            "nonzero_witness_count": len(nonzero_witnesses)}


def close_modulus_full(cols, M, H_rank, r_prime, record, depth=0):
    """裁定741: single DETERMINISTIC pass over the COMPLETE live column set
    (no batching/escalation, no 8x robustness retries -- 司令塔's point:
    "適応全列探索は決定的" -- once every column is available, the outcome
    of this deterministic algorithm does not depend on search order in any
    way that changes the underlying yes/no answer, only possibly which
    SPECIFIC columns end up as the r_prime pivots)."""
    indent = "  " * depth
    record(f"{indent}close_modulus_full: M has {len(str(M))} digits, "
           f"{len(cols)} live columns, target r_prime={r_prime}")
    if M == 1:
        return [{"modulus": "1", "status": "trivial"}]
    col_order = sorted(cols.keys())
    row_priority = list(range(H_rank))
    result = howell_unit_pivot_mod_M_batch(cols, M, col_order, row_priority, r_prime)
    record(f"{indent}close_modulus_full: result status={result['status']}")

    if result["status"] == "success":
        record(f"{indent}close_modulus_full: SUCCESS -- {r_prime} unit pivots "
               f"found AND the remaining {H_rank - r_prime} dependent row(s) "
               f"are IDENTICALLY ZERO mod M across all {result['zero_check_columns']} "
               f"live columns checked -- every prime factor of this M is "
               f"confirmed innocent (rank stays r_prime=={r_prime} "
               f"simultaneously mod every prime dividing M)")
        return [{"modulus": str(M), "status": "success",
                 "pivot_count": len(result["pivots"]),
                 "zero_check_columns": result["zero_check_columns"]}]

    if result["status"] == "split":
        g = result["factor"]
        other = M // g
        record(f"{indent}close_modulus_full: SPLIT at pivot_col={result['pivot_col']} "
               f"(pivots_before_split={result['pivots_before_split']}) "
               f"-- free factor g={g} ({len(str(g))} digits), M//g has "
               f"{len(str(other))} digits -- recursing on both")
        return (close_modulus_full(cols, g, H_rank, r_prime, record, depth + 1)
                + close_modulus_full(cols, other, H_rank, r_prime, record, depth + 1))

    if result["status"] == "residual_nonzero":
        record(f"{indent}close_modulus_full: {r_prime} unit pivots found, but "
               f"{result['nonzero_witness_count']} nonzero residual entries "
               f"remain in the {H_rank - r_prime} dependent row(s) mod M -- "
               f"this is raw torsion-candidate evidence. Recursing on the "
               f"gcd(value,M) of each distinct witnessed factor (excluding "
               f"1) exactly like a TOR-DET split, since these ARE free "
               f"factors of M revealed without trial division.")
        distinct_gcds = sorted({w["gcd_with_M"] for w in result["nonzero_witnesses"]
                                 if w["gcd_with_M"] != 1})
        if not distinct_gcds:
            # every witnessed value is literally coprime to M (gcd==1) --
            # contradicts len(pivots_found)==r_prime being the MAXIMUM
            # possible rank; this would mean rank > r_prime was achievable,
            # a genuine anomaly against the independently-established
            # rank_Q=r_prime fact. STOP, do not guess further.
            record(f"{indent}close_modulus_full: ANOMALY -- nonzero "
                   f"witnesses all have gcd(value,M)==1 despite "
                   f"{r_prime} pivots already being the maximum possible "
                   f"rank (rank_Q={r_prime}, cert v1.1 T2/T3) -- this "
                   f"contradicts the independently established rank. STOP, "
                   f"no judgement word, raw evidence only.")
            return [{"modulus": str(M), "status": "anomaly_unit_witness_beyond_rank",
                     "nonzero_witnesses_sample": result["nonzero_witnesses"]}]
        g = distinct_gcds[0]
        other = M // g
        record(f"{indent}close_modulus_full: treating smallest witnessed "
               f"gcd={g} ({len(str(g))} digits) as a free factor of M -- "
               f"M//g has {len(str(other))} digits -- recursing on both")
        return (close_modulus_full(cols, g, H_rank, r_prime, record, depth + 1)
                + close_modulus_full(cols, other, H_rank, r_prime, record, depth + 1))

    record(f"{indent}close_modulus_full: INSUFFICIENT -- fewer than {r_prime} "
           f"unit pivots ({result['pivots_found']}) found even using the "
           f"COMPLETE live column set -- genuine rank drop mod (a divisor "
           f"of) this M. STOP. No judgement word. Raw evidence only; "
           f"escalate per QUAR-TOR SS5.3.")
    return [{"modulus": str(M), "status": "insufficient_FULL_COLUMNS",
             "pivots_found": result["pivots_found"], "target": r_prime}]


def rank_streaming_modp_from_rows(rows, H_rank, p):
    """裁定742①/self-correction: MANDATORY canary -- independent (from the
    Howell/ext_gcd machinery above) simple Fp Gaussian elimination, run
    DIRECTLY on the TRUE EXACT reconstructed `rows` (list of H_rank dicts,
    col_key -> exact signed integer, BEFORE any reduction mod the target
    M), immediately after FULL1/FULL2 succeed and BEFORE any Howell
    elimination is attempted.

    ***Self-caught methodology bug, corrected here***: the first version of
    this canary was accidentally run against `cols` (values already
    reduced mod the 71-digit ODD target M) instead of the true exact
    `rows`. Since M is odd, (value mod M) mod 2 != value mod 2 in general
    (mod-M reduction can flip parity) -- this produced a bogus rank-mod-2
    result of 62 (impossible, since rank_p <= rank_Q=60 always), which was
    INITIALLY (wrongly) reported as a reconstruction bug. Verified directly:
    an independent fresh recomputation of 30 random sample columns matched
    exact_full_rows's true values EXACTLY (mine == fresh % M for all of
    them) -- the reconstruction itself was correct all along; only the
    diagnostic's input was wrong. This function takes `rows` (pre-mod-M,
    true exact) specifically to avoid repeating that mistake."""
    fp_rows = [dict() for _ in range(H_rank)]
    for i in range(H_rank):
        for ck, v in rows[i].items():
            vp = v % p
            if vp:
                fp_rows[i][ck] = vp
    rank = 0
    used = [False] * H_rank
    for _ in range(H_rank):
        piv_i = None
        piv_col = None
        for i in range(H_rank):
            if used[i]:
                continue
            if fp_rows[i]:
                piv_i = i
                piv_col = next(iter(fp_rows[i]))
                break
        if piv_i is None:
            continue
        used[piv_i] = True
        pivval = fp_rows[piv_i][piv_col]
        inv = pow(pivval, p - 2, p)
        fp_rows[piv_i] = {c: (v * inv) % p for c, v in fp_rows[piv_i].items()}
        for i in range(H_rank):
            if used[i] or i == piv_i:
                continue
            if piv_col in fp_rows[i]:
                f = fp_rows[i][piv_col]
                pr = fp_rows[piv_i]
                newrow = dict(fp_rows[i])
                for c, v in pr.items():
                    nv = (newrow.get(c, 0) - f * v) % p
                    if nv:
                        newrow[c] = nv
                    else:
                        newrow.pop(c, None)
                fp_rows[i] = newrow
        rank += 1
    return rank


def run_reconstruction_canary(rows, H_rank, r_prime, record):
    """裁定742①: run the rank_streaming_modp_from_rows gate over
    CANARY_PRIMES against the TRUE EXACT rows (not mod-M-reduced),
    return (passed: bool, results: dict[str(p) -> rank])."""
    results = {}
    passed = True
    for p in CANARY_PRIMES:
        t0 = time.time()
        r = rank_streaming_modp_from_rows(rows, H_rank, p)
        elapsed = time.time() - t0
        ok = (r == r_prime)
        results[str(p)] = {"rank": r, "expected": r_prime, "pass": ok,
                            "elapsed_seconds": elapsed}
        record(f"CANARY rank mod {p}: got {r}, expected {r_prime}, "
               f"pass={ok} ({elapsed:.2f}s)")
        if not ok:
            passed = False
            record(f"CANARY FAILED at p={p} -- rank {r} != r_prime={r_prime}. "
                   f"Since rank_p <= rank_Q for EVERY prime, r > r_prime is "
                   f"mathematically IMPOSSIBLE for a correct reconstruction "
                   f"of the SAME map that gave rank_Q={r_prime} (cert v1.1 "
                   f"T2/T3) -- this indicates a RECONSTRUCTION BUG, not a "
                   f"torsion finding (p={p} is already independently "
                   f"confirmed innocent via v1.2 T5/T4). r < r_prime would "
                   f"be almost as surprising (contradicts v1.2's direct "
                   f"confirmation of p={p}). STOPPING before any Howell "
                   f"elimination is attempted.")
            # do not break -- collect all canary primes' results for the record
    return passed, results


def main():
    record, log, t_start = record_factory()

    record("loading v1.1 (H_basis), v1.2 (N_source ground truth + pivot cols), "
           "v1.3 (residual M)")
    with open(V1_1_CERT_PATH, "r", encoding="utf-8") as f:
        v1_1 = json.load(f)
    with open(V1_2_CERT_PATH, "r", encoding="utf-8") as f:
        v1_2 = json.load(f)
    with open(V1_3_CERT_PATH, "r", encoding="utf-8") as f:
        v1_3 = json.load(f)

    B = v1_1["stages"]["T1"]["H_basis"]
    H_rank = v1_1["stages"]["T1"]["H_rank"]
    dim_h = v1_1["stages"]["T1"]["M_shape"][1]
    assert H_rank == EXPECTED_H

    t4 = v1_2["stages"]["T4"]
    N_source_ground_truth = t4["N_source"]
    decoded_pivots = t4["decoded_pivot_positions"]  # [[kind, [word...]], ...]
    r_prime = t4["N_source_shape"][1]
    assert r_prime == EXPECTED_R_PRIME

    M = TARGET_M
    record(f"target M = {M} ({len(str(M))} digits) -- the 71-digit residual "
           f"named in v1.3's critical_limitation_found as the next step "
           f"(includes already-confirmed-innocent 11393 as a redundant "
           f"safety margin, per 司令塔裁定739)")

    if os.path.exists(CHECKPOINT_PATH):
        record(f"CHECKPOINT FOUND at {CHECKPOINT_PATH} -- loading TRUE EXACT "
               f"rows instead of redoing FULL1/FULL2 (裁定743: checkpoints "
               f"now store pre-mod-M rows, not mod-M cols, so the "
               f"reconstruction canary can always be (re)run on resume)")
        with open(CHECKPOINT_PATH, "rb") as f:
            ckpt = pickle.load(f)
        if ckpt["M"] != M:
            raise ValueError("checkpoint M does not match TARGET_M -- stale checkpoint")
        rows = ckpt["rows"]
        n_ambient_dim = ckpt["n_ambient_dim"]
        h_ambient_dim = ckpt["h_ambient_dim"]
        cert = ckpt["cert_prefix"]
        cert["generated_by"]["resumed_from_checkpoint"] = True
        record(f"CHECKPOINT LOADED: {sum(len(r) for r in rows)} nonzero entries "
               f"across {H_rank} rows")
        phase2_canary_and_howell(cert, rows, H_rank, r_prime, M, n_ambient_dim,
                                  h_ambient_dim, record, log, t_start)
        return

    cert = {
        "schema": "tor_sweep_k11_v1.4",
        "supersedes": "search/certs/torsweep_k11_v1_3_20260807.json",
        "supersedes_note": "closes the 71-digit residual left open in v1.3 "
                            "(critical_limitation_found) using the FULL "
                            "(not fixed-60-column) N_11 matrix, per "
                            "裁定737(3)/裁定739. v1.1-v1.3 remain on disk as "
                            "the historical record; not modified.",
        "design_spec": "docs/notes/tor_sweep_design_v1.md",
        "ruling_refs": ["裁定736", "裁定737", "裁定738", "裁定739"],
        "k": K,
        "generated_by": {
            "tool": "search/torsweep_k11_close_v1_4.py",
            "python": sys.version,
            "edim_semidirect_v1_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "edim_semidirect_v1.py")),
            "torsweep_k11_run_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "torsweep_k11_run.py")),
            "rng_seed": RNG_SEED,
        },
        "target_M": str(M),
        "target_M_digits": len(str(M)),
        "target_M_provenance": "v1.3 stages.step2_howell_mod_M.closures "
                                "final piece (critical_limitation_found); "
                                "= 11393 * <67-digit UNRESOLVED_COMPOSITE "
                                "from v1.2 stages.T5.gcd_abs_prime_factors>",
        "stages": {},
    }

    # =========================================================================
    # Stage FULL-1: exact full-column reconstruction, TWO independent huge
    # non-prime moduli, entrywise agreement required (裁定739's fallback (b):
    # no int64-safe prime exceeds the observed 14-digit entry magnitude, so a
    # single-prime "0 mod p iff 0 over Z" argument is not available here).
    # =========================================================================
    record("STAGE FULL-1: exact full-column N_11 reconstruction, modulus A")
    t_a_start = time.time()
    rows_a, n_ambient_dim, h_ambient_dim = exact_full_rows(K, B, H_rank, dim_h, P_EXACT_A, record)
    t_a_elapsed = time.time() - t_a_start
    nnz_a = sum(len(r) for r in rows_a)
    record(f"STAGE FULL-1: modulus A done in {t_a_elapsed:.2f}s, total nnz={nnz_a} "
           f"out of theoretical max {H_rank}*{n_ambient_dim + h_ambient_dim}")

    record("STAGE FULL-1: exact full-column N_11 reconstruction, modulus B "
           "(independent cross-check, per 裁定739 2-modulus fallback)")
    t_b_start = time.time()
    rows_b, _, _ = exact_full_rows(K, B, H_rank, dim_h, P_EXACT_B, record)
    t_b_elapsed = time.time() - t_b_start
    nnz_b = sum(len(r) for r in rows_b)
    record(f"STAGE FULL-1: modulus B done in {t_b_elapsed:.2f}s, total nnz={nnz_b}")

    exact_moduli_agree = (rows_a == rows_b)
    record(f"STAGE FULL-1: exact_moduli_agree={exact_moduli_agree}")

    max_abs_entry_measured = 0
    for r in rows_a:
        for v in r.values():
            av = abs(v)
            if av > max_abs_entry_measured:
                max_abs_entry_measured = av

    bound_note = (
        f"measured max|entry| over the FULL reconstructed N_11 = "
        f"{max_abs_entry_measured} ({len(str(max_abs_entry_measured))} digits). "
        f"No int64-safe prime (max ~2**31-1, ~10 digits, per "
        f"edim_semidirect_v1._check_scalar_dense_int64_bound) exceeds this "
        f"bound, so the deterministic single-prime argument of 裁定739's "
        f"primary clause is NOT available; per 裁定739's explicit fallback, "
        f"this run uses the two-independent-huge-modulus agreement instead "
        f"(P_EXACT_A=10**40, P_EXACT_B=10**40+15, both >> "
        f"{max_abs_entry_measured}, i.e. >> 2*max|entry|, so EACH modulus "
        f"individually already center-lifts to the exact value "
        f"deterministically; the cross-modulus agreement additionally rules "
        f"out an implementation bug, matching this repo's existing T1/T4 "
        f"precedent for the same technique)."
    )
    record(f"STAGE FULL-1: {bound_note}")

    cert["stages"]["FULL1_exact_reconstruction"] = {
        "modulus_A": str(P_EXACT_A),
        "modulus_B": str(P_EXACT_B),
        "exact_moduli_agree": exact_moduli_agree,
        "nnz_modulus_A": nnz_a,
        "nnz_modulus_B": nnz_b,
        "n_ambient_dim": n_ambient_dim,
        "h_ambient_dim": h_ambient_dim,
        "full_word_ambient_dim": n_ambient_dim + h_ambient_dim,
        "measured_max_abs_entry": str(max_abs_entry_measured),
        "measured_max_abs_entry_digits": len(str(max_abs_entry_measured)),
        "bound_argument": bound_note,
        "elapsed_seconds_modulus_A": t_a_elapsed,
        "elapsed_seconds_modulus_B": t_b_elapsed,
    }

    if not exact_moduli_agree:
        cert["stop_rules"] = {"S-TOR-1": {
            "triggered": True,
            "reason": "LATTICE_CANARY_FAIL (FULL1, exact-modulus disagreement, "
                      "suspect overflow of P_EXACT or a bug)"}}
        write_cert(cert, log)
        record("STOP: exact moduli disagree at FULL1")
        return

    rows = rows_a  # trusted, exact
    del rows_b  # rows_a/rows_b already compared equal; free the duplicate ~700MB

    # =========================================================================
    # Stage FULL-2: cross-check against v1.2's already-verified N_source
    # ground truth at the 60 recorded pivot columns (independent bug check,
    # reuses previously cross-checked data rather than trusting this new
    # code blind).
    # =========================================================================
    record("STAGE FULL-2: cross-check against v1.2 N_source ground truth "
           "at the 60 recorded pivot columns")
    mismatches = 0
    for j, (kind, word_list) in enumerate(decoded_pivots):
        key = (kind, tuple(word_list))
        for i in range(H_rank):
            got = rows[i].get(key, 0)
            expected = N_source_ground_truth[i][j]
            if got != expected:
                mismatches += 1
    ground_truth_match = (mismatches == 0)
    record(f"STAGE FULL-2: mismatches={mismatches} against v1.2 N_source "
           f"(ground_truth_match={ground_truth_match})")
    cert["stages"]["FULL2_ground_truth_crosscheck"] = {
        "pivot_columns_checked": len(decoded_pivots),
        "mismatches": mismatches,
        "ground_truth_match": ground_truth_match,
    }
    if not ground_truth_match:
        cert["stop_rules"] = {"S-TOR-1": {
            "triggered": True,
            "reason": "FULL2 ground-truth cross-check against v1.2 N_source "
                      "FAILED -- the new full-column reconstruction disagrees "
                      "with already cross-checked data, suspect a bug in "
                      "this script"}}
        write_cert(cert, log)
        record("STOP: FULL2 ground-truth mismatch")
        return

    # CHECKPOINT here (裁定743: store the TRUE EXACT rows, pre-mod-M, not
    # the mod-M-reduced cols -- so a resume can always (re)run the
    # reconstruction canary correctly, unlike the first checkpoint design).
    record(f"checkpointing TRUE EXACT rows to {CHECKPOINT_PATH} "
           f"(FULL1/FULL2 done, before canary/Howell)")
    with open(CHECKPOINT_PATH, "wb") as f:
        pickle.dump({"M": M, "rows": rows, "n_ambient_dim": n_ambient_dim,
                     "h_ambient_dim": h_ambient_dim, "cert_prefix": cert}, f,
                    protocol=pickle.HIGHEST_PROTOCOL)
    record("checkpoint written")

    phase2_canary_and_howell(cert, rows, H_rank, r_prime, M, n_ambient_dim,
                              h_ambient_dim, record, log, t_start)


def phase2_canary_and_howell(cert, rows, H_rank, r_prime, M, n_ambient_dim,
                              h_ambient_dim, record, log, t_start):
    """Shared tail for both the fresh-build and checkpoint-resume paths
    (裁定743): mandatory reconstruction canary on the TRUE EXACT rows,
    then build the mod-M column structure and run the Howell elimination."""
    # =========================================================================
    # Stage FULL-2b: MANDATORY reconstruction canary (裁定742(1)), run on the
    # TRUE EXACT `rows` (pre-mod-M) BEFORE any Howell elimination is
    # attempted. Lesson recorded here per 裁定743: a canary fed DERIVED data
    # sees a phantom -- the first version of this gate was accidentally run
    # against mod-M-reduced values (M odd), which flips parity vs the true
    # integers and produced a bogus rank-mod-2=62. Fixed by feeding it the
    # raw exact integers directly, as below.
    # =========================================================================
    record("STAGE FULL-2b: mandatory reconstruction canary (rank mod "
           f"{CANARY_PRIMES} must equal r_prime={r_prime}), on TRUE EXACT rows")
    t_canary_start = time.time()
    canary_passed, canary_results = run_reconstruction_canary(rows, H_rank, r_prime, record)
    t_canary_elapsed = time.time() - t_canary_start
    cert["stages"]["FULL2b_reconstruction_canary"] = {
        "canary_primes": CANARY_PRIMES,
        "r_prime_target": r_prime,
        "input": "true exact rows (pre-mod-M) -- NOT the mod-M-reduced "
                 "cols structure (裁定743 lesson: a canary fed derived "
                 "data sees a phantom; mod-M reduction with odd M flips "
                 "parity vs the true integers)",
        "results_by_prime": canary_results,
        "all_pass": canary_passed,
        "elapsed_seconds": t_canary_elapsed,
    }
    record(f"STAGE FULL-2b: all_pass={canary_passed} elapsed={t_canary_elapsed:.2f}s")
    if not canary_passed:
        cert["stop_rules"] = {"S-TOR-1": {
            "triggered": True,
            "reason": "RECONSTRUCTION_CANARY_FAIL (裁定742) -- rank mod at "
                      "least one already-confirmed-innocent prime does not "
                      "equal r_prime, computed from the TRUE EXACT rows. "
                      "See stages.FULL2b_reconstruction_canary."}}
        cert["total_elapsed_seconds"] = time.time() - t_start
        write_cert(cert, log)
        record("STOP: S-TOR-1 (reconstruction canary failed on true exact "
               "rows) -- Howell elimination NOT attempted")
        return

    # =========================================================================
    # Stage FULL-3: build the dense-per-column working structure and run the
    # full-column adaptive-pivot Howell elimination mod M (裁定737(3)).
    # =========================================================================
    record("STAGE FULL-3: assembling column-indexed structure for Howell elimination")
    col_union = set()
    for r in rows:
        col_union.update(r.keys())
    col_union = sorted(col_union)
    record(f"STAGE FULL-3: {len(col_union)} live columns (out of "
           f"{n_ambient_dim + h_ambient_dim} full word-ambient)")
    cols = {}
    for ck in col_union:
        cols[ck] = [rows[i].get(ck, 0) % M for i in range(H_rank)]

    # Memory fix (this run, 裁定 aftermath): the first attempt at this
    # single-shot 170,766-column Howell call drove free system memory from
    # ~2.8GB down past 450MB while running (observed directly via wmic),
    # dangerously close to the OOM kills that hit two earlier attempts.
    # `rows` (~700MB, list of H_rank dicts) is no longer needed once `cols`
    # is built -- delete it and force a collection before the expensive
    # step, rather than let it linger for the rest of this function's scope.
    del rows, col_union
    import gc
    gc.collect()
    record("STAGE FULL-3: freed `rows` (no longer needed) and ran gc.collect() "
           "before the Howell elimination, to reduce OOM risk")

    run_full3_and_finish(cert, cols, M, H_rank, r_prime, n_ambient_dim,
                          h_ambient_dim, record, log, t_start)


def run_full3_and_finish(cert, cols, M, H_rank, r_prime, n_ambient_dim,
                          h_ambient_dim, record, log, t_start):
    # NOTE: the reconstruction canary (裁定742(1)) already ran, in
    # phase2_canary_and_howell, directly on the true exact `rows` BEFORE
    # they were reduced mod M into `cols` (裁定743 lesson -- a canary fed
    # derived/mod-M-reduced data can see a phantom, since odd-M reduction
    # flips parity vs the true integers). Its result is recorded in
    # cert["stages"]["FULL2b_reconstruction_canary"]. Nothing further to
    # gate here.
    record(f"STAGE FULL-3: running close_modulus_full over {len(cols)} columns "
           f"(target r_prime={r_prime}, per 裁定741 bugfix)")
    t_howell_start = time.time()
    closures = close_modulus_full(cols, M, H_rank, r_prime, record)
    t_howell_elapsed = time.time() - t_howell_start
    all_success = all(c["status"] == "success" for c in closures)
    STOP_STATUSES = {"insufficient_FULL_COLUMNS", "anomaly_unit_witness_beyond_rank"}
    any_stop = any(c["status"] in STOP_STATUSES for c in closures)

    cert["stages"]["FULL3_howell_full_columns"] = {
        "live_column_count": len(cols),
        "target_M_digits": len(str(M)),
        "r_prime_target": r_prime,
        "H_rank": H_rank,
        "closures": closures,
        "all_pieces_resolved_success": all_success,
        "any_stop_evidence": any_stop,
        "elapsed_seconds": t_howell_elapsed,
    }
    record(f"STAGE FULL-3: all_pieces_resolved_success={all_success} "
           f"any_stop_evidence={any_stop} elapsed={t_howell_elapsed:.2f}s")
    record(f"closures={closures}")

    if any_stop:
        cert.setdefault("stop_rules", {})["QUAR-TOR"] = {
            "triggered": True,
            "note": "FULL-COLUMN Howell elimination (target r_prime, 裁定741 "
                    "corrected criterion) gave stop-evidence on at least one "
                    "piece of M (insufficient pivots even using the complete "
                    "column set, or a unit-gcd witness anomalous against the "
                    "known rank) -- per QUAR-TOR SS5.3 this is raw evidence "
                    "only, no judgement word is written here; 司令塔 "
                    "disposition required.",
        }

    cert["total_elapsed_seconds"] = time.time() - t_start
    write_cert(cert, log)
    record(f"DONE. total_elapsed={cert['total_elapsed_seconds']:.2f}s cert written")
    if os.path.exists(CHECKPOINT_PATH):
        os.remove(CHECKPOINT_PATH)
        record("checkpoint removed (run completed successfully)")


def write_cert(cert, log_lines):
    cert["run_log"] = log_lines
    out_dir = os.path.join(REPO_ROOT, "search", "certs")
    date_str = time.strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"torsweep_k11_v1_4_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print(f"cert written: {out_path}", flush=True)


if __name__ == "__main__":
    main()
