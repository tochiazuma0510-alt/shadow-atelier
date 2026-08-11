#!/usr/bin/env python3
"""
torsweep_k13_hnf_construct_v1.py -- k=13 T0 + T1 (H_13^Z construction), the
LOCAL half of the k=13 pipeline per 裁定790/裁定789.

Scope (explicit): this script produces ONLY
  - T0: t_13^Z construction / freeness canary (T-a), same structural
    argument as k=11/k=12 (docs/notes/tor_sweep_design_v1.md SS1.2, LAT).
  - T1: M_13 = [1+theta; 1+tau+tau2] on Lambda_13^Z (exact, non-modular,
    two-independent-modulus cross-check -- unchanged method from
    torsweep_k12_run.py's build_exact_theta_tau, reused not modified in
    substance, only K generalized), THEN H_13^Z = ker_Z(M_13) via the
    裁定754 root-cause-fixed method: DIRECT INTEGER KERNEL construction
    (column-HNF / unimodular U tracking, integer_kernel_via_unimodular_
    columns, reused verbatim from torsweep_k12_v3_hnf_kernel.py) --
    NOT the old rational-nullspace + denominator-clearing + bounded
    prime-saturation path (裁定754 forbids that path for any new lattice
    construction, cone_design's LAT regulation extends the same rule).

T2/T3 (N_13 = nu_13 o j |_H13, GHA row-sharded) and T4/T5 (TOR-DET integer
proof) are OUT OF SCOPE here -- they are 裁定789's GHA workflow, which reads
this script's output cert (H_basis) as its input artifact (committed to the
repo per 裁定789(2c): "H13のHNF格子構成(先にローカルで作りBをrepo commit
→ workflowが読む)").

Frozen calibration values (裁定735⑥, NOT asserted/checked here since this
script does not compute N_13 -- recorded for the reader's reference only):
  rank H_13 = 210, rank nu_13 = 207, dim S_13(Q) = 3, torsion support = ∅
  (branch table: BOTH >3 and <3 are STOP, raw values, per 裁定735⑥).
This script DOES check H_rank == 210 (EXPECTED_H) as its own T1 regression
canary (S-TOR-2), since H_13 IS computed here.

No judgement words emitted (S-TOR-4): raw values/booleans only.
"""
import hashlib
import json
import os
import random
import sys
import time
from math import gcd

# B's entries can run to hundreds/thousands of digits (k=12 precedent:
# max_abs_entry_in_B had >100 digits; k=13 is larger). Python 3.11+'s
# default int<->str conversion limit (4300 digits, PEP 620-adjacent safety
# guard) would otherwise raise ValueError on str(huge_int) calls used only
# for reporting (digit counts, truncated display) -- lift it explicitly
# here (0 = no limit) since this script's own arithmetic never converts
# these ints through a string for computation, only for logging/cert size.
sys.set_int_max_str_digits(0)

import numpy as np
from sympy import QQ  # noqa: F401  (kept for parity/documentation; NOT used
# for T1 here -- 裁定754 forbids the old DomainMatrix/QQ nullspace +
# denominator-clearing path for lattice construction. Import kept only so a
# reader diffing against torsweep_k12_run.py sees explicitly what was
# dropped, not silently omitted.)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
import edim_semidirect_v1 as ed  # noqa: E402
from torsweep_k12_run import (  # noqa: E402
    sha256_of_file, center_lift, small_primes, row_dependency_mod_p,
    det_bareiss, mat_mul_exact, mat_add, identity,
)
from torsweep_k12_v3_hnf_kernel import (  # noqa: E402
    integer_kernel_via_unimodular_columns, independent_columns_modp,
    compute_sat_gcd,
)
from torsweep_k11_close_v1_4 import close_modulus_full  # noqa: E402

K = 13
EXPECTED_H = 210  # 裁定735(6) frozen value (rank H_13)
# k=13's wallclock cap per design table SS3.4 (S-TOR-3): 14400s. This script
# is expected to finish in low minutes (M-build + integer kernel are both
# cheap, see k=12's 84s precedent for the analogous kernel stage); the cap
# is recorded, not enforced mid-run (interactive/instrumented run).
WALLCLOCK_CAP_SECONDS = 14400

# Same exact-arithmetic moduli as k=11/k=12 (need not be prime; only need to
# exceed the true magnitude of any theta/tau coefficient at degree 13 --
# verified after the fact via the two-modulus agreement check, same as
# k=12). 10**40 was sufficient through k=12; re-verified empirically below
# for k=13 via exact_moduli_agree (if it fails, that itself is the signal
# to raise the modulus -- not assumed correct in advance).
P_EXACT_A = 10 ** 40
P_EXACT_B = 10 ** 40 + 15

RNG_SEED = 20260807
random.seed(RNG_SEED)


def build_exact_theta_tau(h_alg2_exact, k, p_exact):
    theta_modp = ed.build_theta_tau_matrix(k, h_alg2_exact, 'theta', p_exact)
    tau_modp = ed.build_theta_tau_matrix(k, h_alg2_exact, 'tau', p_exact)
    theta = [[center_lift(v, p_exact) for v in row] for row in theta_modp]
    tau = [[center_lift(v, p_exact) for v in row] for row in tau_modp]
    return theta, tau


def main():
    log = []
    t_start = time.time()

    def record(msg):
        line = f"[{time.time() - t_start:8.2f}s] {msg}"
        print(line, flush=True)
        log.append(line)

    cert = {
        "schema": "tor_sweep_k13_hnf_construct.1",
        "design_spec": "docs/notes/tor_sweep_design_v1.md",
        "ruling_refs": ["裁定735(6)", "裁定745", "裁定754", "裁定789", "裁定790"],
        "scope": "T0 + T1 (H_13^Z construction) ONLY. T2/T3/T4/T5 are the "
                 "GHA row-sharded workflow (裁定789), out of scope here.",
        "frozen_calibration_reference_not_checked_here": {
            "rank_H13": 210, "rank_nu13": 207, "dim_S13_Q": 3,
            "torsion_support": [],
            "note": "裁定735(6). Only rank_H13 is actually computed/checked "
                    "by this script (H_rank == EXPECTED_H below); the other "
                    "three require N_13 = nu_13 o j |_H13, which is the GHA "
                    "workflow's job.",
        },
        "k": K,
        "generated_by": {
            "tool": "search/torsweep_k13_hnf_construct_v1.py",
            "python": sys.version,
            "numpy": np.__version__,
            "edim_semidirect_v1_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "edim_semidirect_v1.py")),
            "torsweep_k12_run_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "torsweep_k12_run.py")),
            "torsweep_k12_v3_hnf_kernel_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "torsweep_k12_v3_hnf_kernel.py")),
            "rng_seed": RNG_SEED,
        },
        "stages": {},
        "canaries": {},
        "stop_rules": {},
    }

    # =========================================================================
    # T0: t_13^Z construction / freeness canary (T-a)
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
    # design table SS1.1 (裁定732-corrected row): k=13 -> witt2=630,
    # witt3=122640, t_rank=123270.
    canary_Ta_table_match = (witt2 == 630 and witt3 == 122640 and t_rank == 123270)
    canary_Ta_pass = canary_Ta_witt2_match and canary_Ta_witt3_match and canary_Ta_table_match

    cert["stages"]["T0"] = {
        "witt2": witt2, "witt3": witt3,
        "lyndon2_count": lyndon2_count, "lyndon3_count": lyndon3_count,
        "t_rank": t_rank,
        "t_hnf_diag_all_units": True,
        "t_hnf_diag_all_units_basis": "structural (same argument as k=11/"
                                       "k=12, see those certs' "
                                       "t_hnf_diag_all_units_justification "
                                       "field; unaffected by k)",
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
            "triggered": True, "reason": "LATTICE_CANARY_FAIL (T-a)",
        }
        write_cert(cert, log)
        record("STOP: S-TOR-1 (T-a failed)")
        return

    # =========================================================================
    # T1a: M_13 = [1+theta; 1+tau+tau^2] exact (two-modulus cross-check)
    # =========================================================================
    record("T1a: building h_alg2 (2-letter GradedLie, exact modulus A)")
    t1_start = time.time()

    h_alg2_exact_a = ed.GradedLie(2, K, P_EXACT_A, sparse_degrees={K})
    dim_h = h_alg2_exact_a.dim[K]
    assert dim_h == witt2

    record("T1a: building exact theta/tau (modulus A)")
    theta_a, tau_a = build_exact_theta_tau(h_alg2_exact_a, K, P_EXACT_A)

    record("T1a: building exact theta/tau (modulus B, independent cross-check)")
    h_alg2_exact_b = ed.GradedLie(2, K, P_EXACT_B, sparse_degrees={K})
    theta_b, tau_b = build_exact_theta_tau(h_alg2_exact_b, K, P_EXACT_B)

    exact_moduli_agree = (theta_a == theta_b) and (tau_a == tau_b)
    max_abs_theta = max(abs(v) for row in theta_a for v in row) if dim_h else 0
    max_abs_tau = max(abs(v) for row in tau_a for v in row) if dim_h else 0
    record(f"T1a: exact_moduli_agree={exact_moduli_agree} "
           f"max_abs_theta={max_abs_theta} max_abs_tau={max_abs_tau}")

    if not exact_moduli_agree:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": "exact_moduli_agree=False -- P_EXACT_A/B insufficient "
                      "or overflowed at degree 13, STOP before trusting M",
        }
        cert["stages"]["T1a_partial"] = {
            "dim_h": dim_h, "max_abs_theta": max_abs_theta,
            "max_abs_tau": max_abs_tau, "exact_moduli_agree": False,
        }
        write_cert(cert, log)
        record("STOP: S-TOR-1 (T1a exact-modulus agreement failed)")
        return

    theta, tau = theta_a, tau_a
    I_h = identity(dim_h)
    N_theta = mat_add(I_h, theta)
    record("T1a: computing tau^2 (exact integer matmul)")
    tau2 = mat_mul_exact(tau, tau)
    N_tau = mat_add(mat_add(I_h, tau), tau2)
    M = N_theta + N_tau  # vertical stack, list-of-rows concatenation
    m_rows, n_cols = len(M), dim_h
    record(f"T1a: M assembled, shape=({m_rows},{n_cols})")

    RANK_PRIMES_T0CHECK = [2147483647, 998244353, 1000000007]
    H_rank_modq = {}
    for q in RANK_PRIMES_T0CHECK:
        Mq = np.array([[v % q for v in row] for row in M], dtype=np.int64)
        rk = ed.rank_modp_np(Mq, q)
        H_rank_modq[str(q)] = n_cols - rk
    H_rank_modq_agree = len(set(H_rank_modq.values())) == 1
    record(f"T1a: H_rank via mod-q rank cross-check = {H_rank_modq} "
           f"agree={H_rank_modq_agree}")

    cert["stages"]["T1a"] = {
        "dim_h_ambient_lambda13": dim_h,
        "exact_modulus_A": str(P_EXACT_A), "exact_modulus_B": str(P_EXACT_B),
        "exact_moduli_agree": exact_moduli_agree,
        "max_abs_theta_entry": max_abs_theta, "max_abs_tau_entry": max_abs_tau,
        "M_shape": [m_rows, n_cols],
        "M": M,
        "H_rank_via_modq_rank": H_rank_modq,
        "H_rank_via_modq_rank_agree": H_rank_modq_agree,
        "elapsed_seconds": time.time() - t1_start,
    }
    record(f"T1a: done, elapsed={time.time()-t1_start:.2f}s")

    # =========================================================================
    # T1b: H_13^Z = ker_Z(M) via DIRECT INTEGER KERNEL construction
    # (裁定754 root-cause fix -- no rational nullspace, no denominator
    # clearing, no bounded-prime-list saturation search; automatically
    # saturated by construction).
    # =========================================================================
    record("T1b: integer_kernel_via_unimodular_columns(M) -- exact, no "
           "primes, no fractions (裁定754 method, reused from "
           "torsweep_k12_v3_hnf_kernel.py)")
    t1b_start = time.time()
    B, U_full, active, kstats = integer_kernel_via_unimodular_columns(M, record)
    H_rank = len(B)
    t1b_elapsed = time.time() - t1b_start
    record(f"T1b: kernel dimension = {H_rank} (expected {EXPECTED_H}) "
           f"elapsed={t1b_elapsed:.2f}s")
    cert["stages"]["T1b_kernel_construction"] = {
        "H_rank": H_rank,
        "H_rank_matches_expected_210": (H_rank == EXPECTED_H),
        "pivots_found": kstats["pivots_found"],
        "combine_ops": kstats["combine_ops"],
        "elapsed_seconds": kstats["elapsed_seconds"],
        "max_abs_entry_in_B_digit_count": max(
            (len(str(abs(v))) for row in B for v in row), default=0),
    }
    if H_rank != EXPECTED_H:
        cert.setdefault("stop_rules", {})["S-TOR-2"] = {
            "triggered": True,
            "reason": f"kernel dimension {H_rank} != EXPECTED_H {EXPECTED_H}",
        }
        write_cert(cert, log)
        record("STOP: kernel dimension regression")
        return

    # ---- exact M @ B^T == 0 ----
    record("T1b: exact M@B^T residual check")
    residual_nonzero = 0
    for brow in B:
        for mrow in M:
            s = sum(mrow[j] * brow[j] for j in range(dim_h))
            if s != 0:
                residual_nonzero += 1
    record(f"T1b: M@B^T residual_nonzero_entries={residual_nonzero} (expect 0)")
    cert["stages"]["MBt_check"] = {"residual_nonzero_entries": residual_nonzero}
    if residual_nonzero != 0:
        cert.setdefault("stop_rules", {})["S-TOR-1"] = {
            "triggered": True,
            "reason": "M@B^T != 0 -- STOP, no judgement word (should be "
                      "impossible by construction; indicates a bug)",
        }
        write_cert(cert, log)
        record("STOP: kernel check failed")
        return

    # ---- rank(B mod p) == H_rank for a fresh prime sieve (no k=12-specific
    # historical defect primes reused -- those were k=12 construction
    # artifacts, not k=13-relevant; SAT-JOIN (裁定766) requires this battery
    # regardless) ----
    record("T1b: rank(B mod p) == H_rank for the 303-prime sieve (SAT-JOIN)")
    test_primes = small_primes(2000)
    rank_results = {}
    all_rank_pass = True
    for p in test_primes:
        dep = row_dependency_mod_p(B, p)
        ok = (dep is None)
        rank_results[str(p)] = ok
        if not ok:
            all_rank_pass = False
            record(f"T1b: FAIL at p={p}: row_dependency_mod_p found a "
                   f"dependency (rank < {H_rank})")
    record(f"T1b: tested {len(test_primes)} primes, all_pass={all_rank_pass}")
    cert["stages"]["rank_battery"] = {
        "primes_tested_count": len(test_primes),
        "all_pass": all_rank_pass,
        "failures": [p for p, ok in rank_results.items() if not ok],
    }
    if not all_rank_pass:
        cert.setdefault("stop_rules", {})["S-TOR-1"] = {
            "triggered": True,
            "reason": "rank battery failed at one or more primes -- STOP, "
                      "no judgement word",
            "failed_primes": [p for p, ok in rank_results.items() if not ok],
        }
        write_cert(cert, log)
        record("STOP: rank battery failed")
        return

    # ---- sat_gcd recompute; if !=1, close via ONE direct Howell run, no
    # factoring (裁定754 lesson, SAT-JOIN 裁定766) ----
    record("T1b: sat_gcd recompute (fresh minors on B)")
    big_prime = RANK_PRIMES_T0CHECK[0]
    sat_gcd, minor_dets, minor_col_sets = compute_sat_gcd(
        B, H_rank, dim_h, big_prime, record)
    cert["stages"]["sat_gcd_check"] = {
        "sat_gcd_digits": len(str(sat_gcd)),
        "sat_gcd": str(sat_gcd) if len(str(sat_gcd)) < 300 else
                   f"{str(sat_gcd)[:50]}...({len(str(sat_gcd))} digits)",
    }
    if sat_gcd == 1:
        record("T1b: sat_gcd == 1 -- fully saturated, no closure needed")
        cert["stages"]["sat_gcd_check"]["closure_needed"] = False
        battery_pass = True
    else:
        record(f"T1b: sat_gcd != 1 ({len(str(sat_gcd))} digits) -- closing "
               f"via ONE direct Howell run (no factoring attempted)")
        cols = {j: [B[i][j] % sat_gcd for i in range(H_rank)] for j in range(dim_h)}
        closures = close_modulus_full(cols, sat_gcd, H_rank, H_rank, record)
        all_success = all(c["status"] == "success" for c in closures)
        cert["stages"]["sat_gcd_check"]["closure_needed"] = True
        cert["stages"]["sat_gcd_check"]["closures_summary"] = [
            {"modulus_digits": len(c["modulus"]), "status": c["status"]}
            for c in closures
        ]
        cert["stages"]["sat_gcd_check"]["all_pieces_success"] = all_success
        battery_pass = all_success
        if not all_success:
            cert.setdefault("stop_rules", {})["S-TOR-1"] = {
                "triggered": True,
                "reason": "sat_gcd closure did not succeed on all pieces "
                          "-- STOP, no judgement word (genuine finding, "
                          "not scaffolding noise -- this construction has "
                          "no denominator-clearing step to blame)",
            }

    cert["stages"]["verification_battery_all_pass"] = (
        all_rank_pass and residual_nonzero == 0 and (H_rank == EXPECTED_H)
        and battery_pass and exact_moduli_agree
    )
    record(f"verification_battery_all_pass="
           f"{cert['stages']['verification_battery_all_pass']}")

    if not battery_pass:
        write_cert(cert, log)
        record("STOP: sat_gcd closure failed")
        return

    total_elapsed = time.time() - t_start
    cert["stop_rules"]["S-TOR-3"] = {
        "wallclock_cap_seconds": WALLCLOCK_CAP_SECONDS,
        "total_elapsed_seconds": total_elapsed,
        "within_cap": total_elapsed <= WALLCLOCK_CAP_SECONDS,
    }
    cert["stop_rules"]["S-TOR-4"] = {
        "note": "no judgement words emitted anywhere in this cert; raw "
                "values and booleans only",
    }
    cert["H_basis"] = B
    cert["H_rank"] = H_rank
    cert["dim_h"] = dim_h
    cert["M_shape"] = [m_rows, n_cols]
    cert["total_elapsed_seconds"] = total_elapsed
    write_cert(cert, log)
    record(f"DONE. verification_battery_all_pass=True total_elapsed="
           f"{total_elapsed:.2f}s cert written -- ready for GHA T2/T3/T4/T5 "
           f"(裁定789) to read this cert's H_basis as input artifact")


def write_cert(cert, log_lines):
    cert["run_log"] = log_lines
    out_dir = os.path.join(REPO_ROOT, "search", "certs")
    date_str = time.strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"torsweep_k13_hnf_construct_v1_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print(f"cert written: {out_path}", flush=True)


if __name__ == "__main__":
    main()
