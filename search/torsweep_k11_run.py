#!/usr/bin/env python3
"""
torsweep_k11_run.py -- TOR-SWEEP stages T0-T3 at k=11 (literal implementation
of docs/notes/tor_sweep_design_v1.md SS3.4, table "実装指示書 TOR-1").

Scope (per instruction): ONLY T0-T3. T4 (TOR-DET torsion-prime confirmation)
and T5 (quarantine) are OUT OF SCOPE for this run -- no torsion-prime search
is performed, no judgement words are emitted (S-TOR-4).

Reuses search/edim_semidirect_v1.py (imported, NOT modified) for:
  - witt_dimension, all_lyndon_words          (T0)
  - GradedLie, build_theta_tau_matrix          (T1: exact theta/tau construction)
  - rank_modp_np                               (T1: mod-q rank cross-checks)
  - rank_nu_j_on_subspace_ambient              (T2/T3: nu_k o j restricted rank,
                                                 already the calibrated production
                                                 path used for the k=11 H=62,S=2
                                                 measurement in edim_run_c11.py)

NEW code in this file (not present anywhere else in the repo):
  - exact (non-modular) construction of theta/tau on Lambda_11 via a huge
    non-prime modulus p_exact, relying on the classical fact that the
    Lyndon-basis <-> ambient-word coordinate solve is UNIT triangular (pivot
    coefficient is always exactly 1 for the standard bracketing of a Lyndon
    word -- see edim_semidirect_v1.py build_sparse_solver docstring), so no
    genuine modular inverse (other than of 1) is ever taken and p_exact need
    not be prime;
  - exact-Q nullspace of the integer map M=[1+theta; 1+tau+tau^2] via sympy's
    DomainMatrix over QQ, denominators cleared per vector, together with an
    EXPLICIT saturation canary (T-b): saturation of a full-row-rank integer
    spanning matrix B (r x n) holds iff the gcd of several r x r maximal
    minors of B is +-1 (same principle as TOR-DET, S3.2 of the design note,
    applied here to the saturation question instead of to torsion primes).

Design's own definition LAT / (H-LAT) / structural argument used for T0:
Z^n/ker(M) for M an integer matrix embeds into Z^m (free, hence torsion-
free), so ker_Z(M) is AUTOMATICALLY a saturated submodule of Z^n whenever it
is computed exactly (not via a possibly-under-covering per-vector
denominator-clearing shortcut) -- the T-b canary below verifies this
concretely rather than merely asserting it.

Judgement words are NOT written anywhere in the cert (S-TOR-4): only raw
values and booleans. Regression comparison against the known k=11 measurement
(H_11=62, S_11=2, 662s/627MB, 裁定706 / search/certs/edim_c11_run_v1_20260806.json)
is S-TOR-2.
"""
import hashlib
import itertools
import json
import os
import random
import sys
import time

import numpy as np
from sympy import QQ
from sympy.polys.matrices import DomainMatrix

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
import edim_semidirect_v1 as ed  # noqa: E402

K = 11
EXPECTED_H = 62
EXPECTED_S = 2
# S-TOR-3 wall-clock cap for k<=12 is 3600s; recorded, not enforced mid-run
# (this is an interactive/instrumented run, not an unattended batch job).
WALLCLOCK_CAP_SECONDS = 3600

# T3's "3 large primes" (canary T-c). Two of these (2147483647, 998244353)
# are the repo's own established EDIM commissioned primes (S-ED-3 discipline,
# PRIMES in edim_semidirect_v1.py); a third independent large prime is added
# per the design's explicit "3 primes" requirement (design table SS3.4, T3).
RANK_PRIMES = [2147483647, 998244353, 1000000007]

# The T1 exact-arithmetic modulus. Need not be prime (see module docstring);
# only needs to exceed the true magnitude of any theta/tau coefficient at
# degree 11 (verified after the fact via the two-modulus agreement check
# below, matching this repo's own two-prime cross-check discipline, S-ED-3).
P_EXACT_A = 10**40
P_EXACT_B = 10**40 + 15  # independent second exact modulus for agreement check

RNG_SEED = 20260807

random.seed(RNG_SEED)


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def center_lift(x, p):
    x = x % p
    return x - p if x > p // 2 else x


def ext_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_r, old_s, (old_r - old_s * a) // b if b != 0 else 0


def small_primes(bound):
    sieve = [True] * (bound + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(bound ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, bound + 1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]


def row_dependency_mod_p(B, p):
    """B: r x n int matrix. Returns None if rows are independent mod p,
    else a length-r vector (not all 0 mod p) w with sum_i w[i]*B[i] = 0
    (mod p), found via augmented [B|I_r] row reduction over F_p."""
    r = len(B)
    n = len(B[0]) if r else 0
    aug = [[B[i][j] % p for j in range(n)] + [1 if i == k else 0 for k in range(r)]
           for i in range(r)]
    row = 0
    for col in range(n):
        if row >= r:
            break
        piv = None
        for rr in range(row, r):
            if aug[rr][col] % p != 0:
                piv = rr
                break
        if piv is None:
            continue
        aug[row], aug[piv] = aug[piv], aug[row]
        inv = pow(aug[row][col], p - 2, p)
        aug[row] = [(x * inv) % p for x in aug[row]]
        for rr in range(r):
            if rr != row and aug[rr][col] % p != 0:
                f = aug[rr][col]
                aug[rr] = [(aug[rr][c] - f * aug[row][c]) % p for c in range(n + r)]
        row += 1
    if row == r:
        return None
    for rr in range(row, r):
        if all(aug[rr][c] % p == 0 for c in range(n)):
            combo = [aug[rr][n + k] % p for k in range(r)]
            if any(c != 0 for c in combo):
                return combo
    return None


def saturate_spanning_set(B, max_prime_bound=2000, max_rounds=20000):
    """p-saturation refinement (NEW code, not present elsewhere in the repo):
    given an integer matrix B (r x n, full row rank r) that spans the
    correct Q-subspace but may be an index>1 sublattice of its saturation
    Z^n cap span_Q(B) (per-vector denominator-clearing from a rational
    nullspace basis does NOT in general give a saturated set -- verified
    empirically at k=6 during this run's development, see report), refine
    it by finding & dividing out row-dependencies mod each small prime in
    turn. Only ever does mod-p linear algebra on the SMALL r x n matrix, not
    the original big map, so this is fast regardless of the ambient
    dimension n. The definitive saturation check remains the T-b minor-gcd
    canary computed AFTER this refinement -- this function is a best-effort
    accelerant, not itself trusted as proof."""
    B = [row[:] for row in B]
    r = len(B)
    n = len(B[0]) if r else 0
    primes = small_primes(max_prime_bound)
    rounds = 0
    rounds_by_prime = {}
    for ell in primes:
        while True:
            combo = row_dependency_mod_p(B, ell)
            if combo is None:
                break
            newrow = [sum(combo[i] * B[i][j] for i in range(r)) for j in range(n)]
            if any(v % ell != 0 for v in newrow):
                raise ValueError("saturate_spanning_set: internal error, "
                                  "combo did not annihilate mod ell")
            newrow = [v // ell for v in newrow]
            piv = next(i for i in range(r) if combo[i] % ell != 0)
            B[piv] = newrow
            rounds += 1
            rounds_by_prime[ell] = rounds_by_prime.get(ell, 0) + 1
            if rounds > max_rounds:
                raise RuntimeError("saturate_spanning_set: exceeded max_rounds "
                                    "-- suspect index has a prime factor beyond "
                                    "max_prime_bound, or a bug")
    return B, rounds, rounds_by_prime


def det_bareiss(mat):
    """Exact integer determinant, fraction-free Bareiss elimination."""
    n = len(mat)
    if n == 0:
        return 1
    M = [row[:] for row in mat]
    prev = 1
    sign = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            swap_row = None
            for i in range(k + 1, n):
                if M[i][k] != 0:
                    swap_row = i
                    break
            if swap_row is None:
                return 0
            M[k], M[swap_row] = M[swap_row], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


def build_exact_theta_tau(h_alg2_exact, k, p_exact):
    theta_modp = ed.build_theta_tau_matrix(k, h_alg2_exact, 'theta', p_exact)
    tau_modp = ed.build_theta_tau_matrix(k, h_alg2_exact, 'tau', p_exact)
    theta = [[center_lift(v, p_exact) for v in row] for row in theta_modp]
    tau = [[center_lift(v, p_exact) for v in row] for row in tau_modp]
    return theta, tau


def mat_mul_exact(A, B):
    n = len(A)
    m = len(B[0])
    kk = len(B)
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for l in range(kk):
            a = Ai[l]
            if a == 0:
                continue
            Bl = B[l]
            for j in range(m):
                Ci[j] += a * Bl[j]
    return C


def mat_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def main():
    log = []

    def record(msg):
        t = time.time()
        line = f"[{t - t_script_start:8.2f}s] {msg}"
        print(line, flush=True)
        log.append(line)

    t_script_start = time.time()
    cert = {
        "schema": "tor_sweep_k11_v1",
        "design_spec": "docs/notes/tor_sweep_design_v1.md",
        "scope": "T0-T3 only (T4/T5 out of scope, no torsion-prime search performed)",
        "k": K,
        "generated_by": {
            "tool": "search/torsweep_k11_run.py",
            "python": sys.version,
            "numpy": np.__version__,
            "sympy": __import__("sympy").__version__,
            "edim_semidirect_v1_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "edim_semidirect_v1.py")),
            "rng_seed": RNG_SEED,
        },
        "stages": {},
        "canaries": {},
        "stop_rules": {},
    }

    # =========================================================================
    # T0: t_11^Z construction / freeness canary (T-a)
    # =========================================================================
    record("T0: start")
    t0_start = time.time()
    witt2 = ed.witt_dimension(2, K)
    witt3 = ed.witt_dimension(3, K)
    lyndon2_words = ed.all_lyndon_words(2, K)
    lyndon3_words = ed.all_lyndon_words(3, K)
    lyndon2_count = len(lyndon2_words)
    lyndon3_count = len(lyndon3_words)
    t_rank = witt2 + witt3
    t0_elapsed = time.time() - t0_start

    canary_Ta_witt2_match = (lyndon2_count == witt2)
    canary_Ta_witt3_match = (lyndon3_count == witt3)
    # design table SS1.1 expected values at k=11
    canary_Ta_table_match = (witt2 == 186 and witt3 == 14880 and t_rank == 15066)
    canary_Ta_pass = canary_Ta_witt2_match and canary_Ta_witt3_match and canary_Ta_table_match

    t_hnf_diag_all_units_justification = (
        "t_11^Z is realized (per definition LAT and the semidirect-model "
        "calibration, docs/notes/edim_semidirect_model_design_v1.md) as the "
        "underlying Z-module direct sum Lie_Z(A,B,C)_11 (+) Lie_Z(x,y)_11 "
        "(bracket twisting in the semidirect product does not alter the "
        "additive/Z-module structure). Each summand's standard Lyndon basis "
        "is a Z-basis of a free Lie ring's degree-k piece (classical fact, "
        "PBW splits over Z) -- the union of the two Lyndon bases is "
        "therefore literally a Z-basis of t_11^Z by construction, i.e. the "
        "HNF of the identity embedding is the identity (all diagonal +-1). "
        "This is NOT an independent computation; it is a structural "
        "consequence of using the semidirect-model realization as t_k^Z. "
        "The genuinely open gap is (H-LAT) itself: whether this semidirect "
        "model IS gr(K(0,5)) as a Z-form beyond the degree<=6 calibration "
        "(【T-GAP-1】, design SS6.1) -- unaffected by this canary."
    )

    cert["stages"]["T0"] = {
        "witt2": witt2,
        "witt3": witt3,
        "lyndon2_count": lyndon2_count,
        "lyndon3_count": lyndon3_count,
        "t_rank": t_rank,
        "t_hnf_diag_all_units": True,
        "t_hnf_diag_all_units_basis": "structural (see justification field)",
        "t_hnf_diag_all_units_justification": t_hnf_diag_all_units_justification,
        "elapsed_seconds": t0_elapsed,
    }
    cert["canaries"]["T-a"] = {
        "witt2_matches_lyndon_count": canary_Ta_witt2_match,
        "witt3_matches_lyndon_count": canary_Ta_witt3_match,
        "matches_design_table_SS1_1": canary_Ta_table_match,
        "pass": canary_Ta_pass,
    }
    record(f"T0: witt2={witt2} witt3={witt3} t_rank={t_rank} "
           f"canary_Ta_pass={canary_Ta_pass} ({t0_elapsed:.2f}s)")

    if not canary_Ta_pass:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": "LATTICE_CANARY_FAIL (T-a)",
        }
        write_cert(cert)
        record("STOP: S-TOR-1 (T-a failed) -- see cert, no further stages run")
        return

    # =========================================================================
    # T1: H_11^Z = Lambda_11^Z cap ker(1+theta) cap ker(1+tau+tau^2), saturated
    # =========================================================================
    record("T1: building h_alg2 (2-letter GradedLie, exact modulus A)")
    t1_start = time.time()

    h_alg2_exact_a = ed.GradedLie(2, K, P_EXACT_A, sparse_degrees={K})
    dim_h = h_alg2_exact_a.dim[K]
    assert dim_h == witt2

    record("T1: building exact theta/tau (modulus A)")
    theta_a, tau_a = build_exact_theta_tau(h_alg2_exact_a, K, P_EXACT_A)

    record("T1: building exact theta/tau (modulus B, independent cross-check)")
    h_alg2_exact_b = ed.GradedLie(2, K, P_EXACT_B, sparse_degrees={K})
    theta_b, tau_b = build_exact_theta_tau(h_alg2_exact_b, K, P_EXACT_B)

    exact_moduli_agree = (theta_a == theta_b) and (tau_a == tau_b)
    max_abs_theta = max(abs(v) for row in theta_a for v in row) if dim_h else 0
    max_abs_tau = max(abs(v) for row in tau_a for v in row) if dim_h else 0
    record(f"T1: exact_moduli_agree={exact_moduli_agree} "
           f"max_abs_theta={max_abs_theta} max_abs_tau={max_abs_tau}")

    theta, tau = theta_a, tau_a
    I_h = identity(dim_h)
    N_theta = mat_add(I_h, theta)
    record("T1: computing tau^2 (exact integer matmul)")
    tau2 = mat_mul_exact(tau, tau)
    N_tau = mat_add(mat_add(I_h, tau), tau2)
    M = N_theta + N_tau  # vertical stack, list-of-rows concatenation
    m_rows, n_cols = len(M), dim_h
    record(f"T1: M assembled, shape=({m_rows},{n_cols})")

    # mod-q rank cross-check of nullity (cheap, independent of the exact
    # Q-nullspace computation below)
    H_rank_modq = {}
    for q in RANK_PRIMES:
        Mq = np.array([[v % q for v in row] for row in M], dtype=np.int64)
        rk = ed.rank_modp_np(Mq, q)
        H_rank_modq[str(q)] = n_cols - rk
    H_rank_modq_agree = len(set(H_rank_modq.values())) == 1
    record(f"T1: H_rank via mod-q rank cross-check = {H_rank_modq} "
           f"agree={H_rank_modq_agree}")

    record("T1: exact Q-nullspace of M via sympy DomainMatrix/QQ")
    dm = DomainMatrix(M, (m_rows, n_cols), QQ)
    ns = dm.nullspace()
    ns_matrix = ns.to_Matrix()
    H_rank_exact = ns_matrix.rows
    record(f"T1: exact nullspace dim = {H_rank_exact} "
           f"(elapsed so far {time.time()-t1_start:.2f}s)")

    # clear denominators per row -> integer spanning matrix B_raw (H_rank x n_cols)
    # NOTE: per-vector denominator clearing spans the correct Q-subspace but
    # is NOT in general a saturated Z-basis (confirmed empirically at k=6
    # during development: gcd of maximal minors came out 3, not 1). The
    # p-saturation refinement below (saturate_spanning_set, new code) fixes
    # this; the T-b canary further down is the definitive, independent check
    # of the RESULT, not a trust-the-refinement-step assumption.
    from sympy import lcm as sympy_lcm
    B_raw = []
    for i in range(H_rank_exact):
        row = ns_matrix.row(i)
        dens = [r.q for r in row]
        L = 1
        for d in dens:
            L = sympy_lcm(L, d)
        int_row = [int(r * L) for r in row]
        B_raw.append(int_row)

    record("T1: p-saturation refinement of the denominator-cleared spanning set")
    t_sat_start = time.time()
    B, saturation_rounds, saturation_rounds_by_prime = saturate_spanning_set(B_raw)
    t_sat_elapsed = time.time() - t_sat_start
    record(f"T1: saturation refinement done in {t_sat_elapsed:.2f}s, "
           f"{saturation_rounds} rounds, primes touched="
           f"{sorted(saturation_rounds_by_prime.keys())}")

    # exact verification: M @ B^T == 0
    residual_nonzero = 0
    for brow in B:
        for mrow in M:
            s = sum(mrow[j] * brow[j] for j in range(n_cols))
            if s != 0:
                residual_nonzero += 1
    record(f"T1: exact M@B^T residual_nonzero_entries={residual_nonzero} "
           f"(expect 0)")

    # ---- T-b saturation canary: gcd of several H_rank x H_rank minors of B ----
    def independent_columns_modp(rows_as_matrix, p, order):
        """Pick a full-rank set of len(rows_as_matrix) columns, scanning
        columns in the given order, via mod-p pivoting."""
        pivots = {}
        selected = []
        for col in order:
            vec = {i: rows_as_matrix[i][col] % p for i in range(len(rows_as_matrix))
                   if rows_as_matrix[i][col] % p}
            while vec:
                piv = min(vec)
                old = pivots.get(piv)
                if old is None:
                    inv = pow(vec[piv], p - 2, p)
                    vec = {i: (v * inv) % p for i, v in vec.items() if v % p}
                    pivots[piv] = vec
                    selected.append(col)
                    break
                factor = vec[piv]
                for i, v in old.items():
                    nv = (vec.get(i, 0) - factor * v) % p
                    if nv:
                        vec[i] = nv
                    else:
                        vec.pop(i, None)
            if len(selected) == len(rows_as_matrix):
                break
        return selected

    minor_dets = []
    minor_col_sets = []
    if H_rank_exact > 0:
        big_prime_for_pivoting = RANK_PRIMES[0]
        orders = []
        base_order = list(range(n_cols))
        orders.append(base_order)
        rnd1 = base_order[:]
        random.shuffle(rnd1)
        orders.append(rnd1)
        rnd2 = base_order[:]
        random.shuffle(rnd2)
        orders.append(rnd2)
        orders.append(list(reversed(base_order)))
        seen_col_sets = set()
        for order in orders:
            cols = independent_columns_modp(B, big_prime_for_pivoting, order)
            if len(cols) != H_rank_exact:
                continue
            key = tuple(sorted(cols))
            if key in seen_col_sets:
                continue
            seen_col_sets.add(key)
            submat = [[B[i][c] for c in cols] for i in range(H_rank_exact)]
            d = det_bareiss(submat)
            minor_dets.append(d)
            minor_col_sets.append(cols)
            if len(minor_dets) >= 4:
                break
        from math import gcd
        sat_gcd = 0
        for d in minor_dets:
            sat_gcd = gcd(sat_gcd, abs(d))
    else:
        sat_gcd = 1  # trivial (0-dim) lattice is vacuously saturated

    canary_Tb_pass = (sat_gcd == 1)
    record(f"T1: saturation minors dets={minor_dets} sat_gcd={sat_gcd} "
           f"canary_Tb_pass={canary_Tb_pass}")

    H_rank = H_rank_exact
    H_rank_regression_match = (H_rank == EXPECTED_H)

    t1_elapsed = time.time() - t1_start
    cert["stages"]["T1"] = {
        "dim_h_ambient_lambda11": dim_h,
        "exact_modulus_A": str(P_EXACT_A),
        "exact_modulus_B": str(P_EXACT_B),
        "exact_moduli_agree": exact_moduli_agree,
        "max_abs_theta_entry": max_abs_theta,
        "max_abs_tau_entry": max_abs_tau,
        "M_shape": [m_rows, n_cols],
        "H_rank_via_modq_rank": H_rank_modq,
        "H_rank_via_modq_rank_agree": H_rank_modq_agree,
        "H_rank_exact_Q_nullspace": H_rank_exact,
        "saturation_refinement_rounds": saturation_rounds,
        "saturation_refinement_primes_touched": sorted(saturation_rounds_by_prime.keys()),
        "saturation_refinement_elapsed_seconds": t_sat_elapsed,
        "H_rank": H_rank,
        "H_rank_matches_edim_c11_measurement_62": H_rank_regression_match,
        "exact_kernel_residual_nonzero_entries": residual_nonzero,
        "saturation_minor_determinants": [str(d) for d in minor_dets],
        "saturation_minor_column_sets_sample": minor_col_sets,
        "saturation_gcd_of_minors": str(sat_gcd),
        "elapsed_seconds": t1_elapsed,
    }
    cert["canaries"]["T-b"] = {
        "method": "gcd of several H_rank x H_rank Bareiss minors of the "
                  "exact-Q-nullspace integer spanning matrix B; gcd==1 "
                  "implies Z-rowspan(B) is already saturated (same "
                  "principle as TOR-DET SS3.2, applied to the saturation "
                  "question rather than to a torsion-prime search)",
        "sat_gcd": str(sat_gcd),
        "pass": canary_Tb_pass,
    }
    record(f"T1: H_rank={H_rank} (expected {EXPECTED_H}, match="
           f"{H_rank_regression_match}) elapsed={t1_elapsed:.2f}s")

    if not canary_Tb_pass:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": "LATTICE_CANARY_FAIL (T-b, saturation)",
        }
        write_cert(cert)
        record("STOP: S-TOR-1 (T-b failed) -- see cert, no further stages run")
        return

    if not H_rank_regression_match:
        cert["stop_rules"]["S-TOR-2"] = {
            "triggered": True,
            "reason": f"H_rank={H_rank} != EXPECTED_H={EXPECTED_H}",
        }
        write_cert(cert)
        record("STOP: S-TOR-2 (H_rank regression mismatch) -- see cert, "
               "no further stages run")
        return

    # =========================================================================
    # T2/T3: N_11 = nu_11 o j |_H, rank via 3 large primes (canary T-c),
    # dim S_11(Q) byproduct
    # =========================================================================
    record("T2/T3: start (rank_nu_j_on_subspace_ambient x 3 primes)")
    t23_start = time.time()

    per_prime = {}
    for q in RANK_PRIMES:
        subspace_basis_modq = np.array(
            [[v % q for v in row] for row in B], dtype=np.int64).T
        assert subspace_basis_modq.shape == (dim_h, H_rank)
        h_alg2_q = ed.GradedLie(2, K, q)
        t_q0 = time.time()
        r_q = ed.rank_nu_j_on_subspace_ambient(K, h_alg2_q, subspace_basis_modq, q)
        t_q_elapsed = time.time() - t_q0
        nu_cert = getattr(h_alg2_q, "_last_nu_rank_certificate", {})
        per_prime[str(q)] = {
            "rank": int(r_q),
            "elapsed_seconds": t_q_elapsed,
            "restricted_dense_bytes": nu_cert.get("restricted_dense_bytes"),
            "ambient_dim": nu_cert.get("ambient_dim"),
            "domain_dim": nu_cert.get("domain_dim"),
        }
        record(f"T2/T3: q={q} rank={r_q} elapsed={t_q_elapsed:.2f}s "
               f"restricted_bytes={nu_cert.get('restricted_dense_bytes')}")

    ranks = [per_prime[str(q)]["rank"] for q in RANK_PRIMES]
    canary_Tc_pass = (len(set(ranks)) == 1)
    r_prime = ranks[0] if canary_Tc_pass else None
    dim_S_Q = (H_rank - r_prime) if r_prime is not None else None
    S_regression_match = (dim_S_Q == EXPECTED_S) if dim_S_Q is not None else False

    t23_elapsed = time.time() - t23_start
    cert["stages"]["T2_T3"] = {
        "per_prime": per_prime,
        "ranks_agree": canary_Tc_pass,
        "r_prime": r_prime,
        "dim_S_Q_byproduct": dim_S_Q,
        "dim_S_Q_matches_edim_c11_measurement_2": S_regression_match,
        "elapsed_seconds": t23_elapsed,
    }
    cert["canaries"]["T-c"] = {
        "ranks_by_prime": {str(q): per_prime[str(q)]["rank"] for q in RANK_PRIMES},
        "pass": canary_Tc_pass,
    }
    record(f"T2/T3: r_prime={r_prime} dim_S_Q={dim_S_Q} "
           f"(expected {EXPECTED_S}, match={S_regression_match}) "
           f"canary_Tc_pass={canary_Tc_pass} elapsed={t23_elapsed:.2f}s")

    if not canary_Tc_pass:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": "LATTICE_CANARY_FAIL (T-c, 3-prime rank disagreement)",
        }
        write_cert(cert)
        record("STOP: S-TOR-1 (T-c failed) -- see cert")
        return

    if not S_regression_match:
        cert["stop_rules"]["S-TOR-2"] = {
            "triggered": True,
            "reason": f"dim_S_Q={dim_S_Q} != EXPECTED_S={EXPECTED_S}",
        }
        write_cert(cert)
        record("STOP: S-TOR-2 (dim_S_Q regression mismatch) -- see cert")
        return

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
    out_path = os.path.join(out_dir, f"torsweep_k11_v1_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print(f"cert written: {out_path}", flush=True)


if __name__ == "__main__":
    main()
