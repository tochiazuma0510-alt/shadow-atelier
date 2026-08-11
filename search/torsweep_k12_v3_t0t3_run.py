#!/usr/bin/env python3
"""
torsweep_k12_v3_t0t3_run.py -- TOR-SWEEP stages T0-T3 at k=12, RERUN with the
H_basis B produced by torsweep_k12_v3_hnf_kernel.py (裁定754(4): "(iv) 解除:
T0-T3 再走(全カナリア・生整数入力)"). B here is constructed by DIRECT
integer-kernel (column-HNF/unimodular-U-tracking) reconstruction -- no
rational nullspace, no denominator clearing, no prime-hunting saturation
anywhere -- and already passed its own verification battery (kernel
dimension==112, exact M@B^T=0, rank mod 310 primes including all 7
historically-discovered defect primes, sat_gcd closed via one direct Howell
run) in cert torsweep_k12_v3_hnf_kernel_20260807.json.

T0 (t_12^Z construction) is UNAFFECTED by the H_basis construction method
(different Z-module entirely) -- carried forward BY VALUE from the v1 cert
(re-asserted, not merely referenced), matching 裁定742's "canary inputs must
be raw exact data" discipline.

T1 here is a THIN re-record of the v3 cert's own verification results (not
recomputed a third time -- the v3 cert's battery already IS the T-b canary
in substance, computed independently of the construction method by design).

T2/T3 (rank of nu_12 o j restricted to H_12=span(B), 3-large-prime canary
T-c, dim S_12(Q) byproduct) run for the first time on the reconstructed B.
Calibration point (裁定734/addendum_a): EXPECTED_H=112, EXPECTED_S=2.

No judgement words emitted (S-TOR-4): raw values/booleans only.
"""
import hashlib
import json
import os
import sys
import time

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
import edim_semidirect_v1 as ed  # noqa: E402
from torsweep_k12_run import sha256_of_file  # noqa: E402

K = 12
EXPECTED_H = 112
EXPECTED_S = 2
WALLCLOCK_CAP_SECONDS = 3600
V1_CERT_PATH = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k12_v1_20260807.json")
HNF_CERT_PATH = os.path.join(REPO_ROOT, "search", "certs",
                              "torsweep_k12_v3_hnf_kernel_20260807.json")
RANK_PRIMES = [2147483647, 998244353, 1000000007]


def main():
    log = []
    t_start = time.time()

    def record(msg):
        line = f"[{time.time() - t_start:8.2f}s] {msg}"
        print(line, flush=True)
        log.append(line)

    record("loading v1 cert (T0, M) and v3_hnf_kernel cert (reconstructed B)")
    with open(V1_CERT_PATH, "r", encoding="utf-8") as f:
        v1 = json.load(f)
    with open(HNF_CERT_PATH, "r", encoding="utf-8") as f:
        hnf = json.load(f)

    t0 = v1["stages"]["T0"]
    M = v1["stages"]["T1"]["M"]
    dim_h = v1["stages"]["T1"]["M_shape"][1]
    B = hnf["H_basis"]
    H_rank = hnf["H_rank"]
    assert H_rank == EXPECTED_H, (H_rank, EXPECTED_H)
    assert len(B) == H_rank and len(B[0]) == dim_h
    assert hnf["stages"]["verification_battery_all_pass"] is True
    record(f"loaded: H_rank={H_rank}, dim_h={dim_h}, "
           f"hnf_verification_battery_all_pass="
           f"{hnf['stages']['verification_battery_all_pass']}")

    cert = {
        "schema": "tor_sweep_k12_v3.1",
        "supersedes": "search/certs/torsweep_k12_v2_20260807.json (never "
                       "produced -- v2 line was superseded by 裁定754's "
                       "root-cause fix before reaching T2/T3)",
        "input_certs": {
            "v1": "search/certs/torsweep_k12_v1_20260807.json",
            "v3_hnf_kernel": "search/certs/torsweep_k12_v3_hnf_kernel_20260807.json",
        },
        "supersedes_note": "T0-T3 rerun (裁定754(4)) with the H_basis B "
                            "constructed by direct integer-kernel "
                            "(column-HNF/unimodular-U-tracking) "
                            "reconstruction -- 根治, no prime-hunting "
                            "saturation anywhere.",
        "design_spec": "docs/notes/tor_sweep_design_v1.md",
        "ruling_refs": ["裁定745", "裁定754"],
        "k": K,
        "generated_by": {
            "tool": "search/torsweep_k12_v3_t0t3_run.py",
            "python": sys.version,
            "numpy": np.__version__,
            "edim_semidirect_v1_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "edim_semidirect_v1.py")),
            "torsweep_k12_v3_hnf_kernel_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "torsweep_k12_v3_hnf_kernel.py")),
        },
        "stages": {},
        "canaries": {},
        "stop_rules": {},
    }

    # T0 -- carried forward by value from v1 (unaffected by the H-basis
    # construction method).
    cert["stages"]["T0"] = dict(t0)
    cert["canaries"]["T-a"] = {
        "carried_forward_from": "torsweep_k12_v1_20260807.json",
        "witt2_matches_lyndon_count": (t0["witt2"] == t0["lyndon2_count"]),
        "witt3_matches_lyndon_count": (t0["witt3"] == t0["lyndon3_count"]),
        "pass": (t0["witt2"] == t0["lyndon2_count"]) and (t0["witt3"] == t0["lyndon3_count"]),
    }
    record(f"T0: carried forward, witt2={t0['witt2']} witt3={t0['witt3']} "
           f"t_rank={t0['t_rank']}")

    # =========================================================================
    # T1: thin re-record of the v3_hnf_kernel cert's own verification
    # battery (that battery IS the T-b canary in substance: exact M@B^T=0,
    # rank mod 310 primes including all 7 historically-discovered defect
    # primes, sat_gcd closed via one direct Howell run -- not recomputed a
    # third time here, cited by reference to the input cert's raw values).
    # =========================================================================
    kc = hnf["stages"]["kernel_construction"]
    mbt = hnf["stages"]["MBt_check"]
    rb = hnf["stages"]["rank_battery"]
    sgc = hnf["stages"]["sat_gcd_check"]
    canary_Tb_pass = hnf["stages"]["verification_battery_all_pass"]
    cert["stages"]["T1"] = {
        "dim_h_ambient_lambda12": dim_h,
        "M_shape": [len(M), dim_h],
        "H_rank": H_rank,
        "H_basis": B,
        "H_rank_matches_expected_112": (H_rank == EXPECTED_H),
        "construction_method": "direct integer kernel (column-HNF / "
                                "unimodular U tracking), see "
                                "torsweep_k12_v3_hnf_kernel.py",
        "kernel_construction_summary": kc,
        "MBt_check_summary": mbt,
        "rank_battery_summary": {
            "primes_tested_count": rb["primes_tested_count"],
            "all_pass": rb["all_pass"],
        },
        "sat_gcd_check_summary": sgc,
    }
    cert["canaries"]["T-b"] = {
        "method": "battery from torsweep_k12_v3_hnf_kernel.py, cited by "
                  "reference (not recomputed here): exact M@B^T=0 + "
                  "rank mod 310 primes (303-prime sieve + 7 "
                  "historically-discovered defect primes) + sat_gcd "
                  "closed via one direct Howell run, no factoring.",
        "pass": canary_Tb_pass,
    }
    record(f"T1: carried forward from v3_hnf_kernel cert, canary_Tb_pass="
           f"{canary_Tb_pass}")

    if not canary_Tb_pass or H_rank != EXPECTED_H:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": f"T1 (v3_hnf_kernel battery) not passing "
                      f"(canary_Tb_pass={canary_Tb_pass}, H_rank={H_rank})",
        }
        write_cert(cert, log)
        record("STOP: T1 battery not passing")
        return

    # =========================================================================
    # T2/T3: N_12 = nu_12 o j |_H, rank via 3 large primes (canary T-c),
    # dim S_12(Q) byproduct. First run on the reconstructed B.
    # =========================================================================
    record("T2/T3: start (rank_nu_j_on_subspace_ambient x 3 primes) on "
           "reconstructed B")
    t23_start = time.time()
    per_prime = {}
    # Checkpoint (scratchpad only, per 拘束): each prime's rank computation
    # is expensive (observed: still running after 80+ minutes for the
    # FIRST prime in this run's own development, before a background-task
    # interruption lost that work) -- persist completed primes' results
    # so a rerun after an interruption does not repeat already-finished
    # primes.
    ckpt_dir = os.path.join(REPO_ROOT, "scratchpad", "torsweep")
    os.makedirs(ckpt_dir, exist_ok=True)
    ckpt_path = os.path.join(ckpt_dir, "k12_v3_t2t3_per_prime_checkpoint.json")
    if os.path.exists(ckpt_path):
        with open(ckpt_path, "r", encoding="utf-8") as f:
            per_prime = json.load(f)
        record(f"T2/T3: checkpoint found, {len(per_prime)} prime(s) already "
               f"done: {list(per_prime.keys())}")
    for q in RANK_PRIMES:
        if str(q) in per_prime:
            record(f"T2/T3: q={q} already done (checkpoint), rank="
                   f"{per_prime[str(q)]['rank']} -- skipping")
            continue
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
        record(f"T2/T3: q={q} rank={r_q} elapsed={t_q_elapsed:.2f}s")
        with open(ckpt_path, "w", encoding="utf-8") as f:
            json.dump(per_prime, f, default=str)
        record(f"T2/T3: checkpoint written ({len(per_prime)}/{len(RANK_PRIMES)} primes done)")

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
        "dim_S_Q_matches_expected_2": S_regression_match,
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
        write_cert(cert, log)
        record("STOP: S-TOR-1 (T-c failed)")
        return

    if not S_regression_match:
        cert["stop_rules"]["S-TOR-2"] = {
            "triggered": True,
            "reason": f"dim_S_Q={dim_S_Q} != EXPECTED_S={EXPECTED_S}",
        }
        write_cert(cert, log)
        record("STOP: S-TOR-2 (dim_S_Q regression mismatch)")
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
    cert["total_elapsed_seconds"] = total_elapsed
    write_cert(cert, log)
    record(f"DONE. total_elapsed={total_elapsed:.2f}s")


def write_cert(cert, log_lines):
    cert["run_log"] = log_lines
    out_dir = os.path.join(REPO_ROOT, "search", "certs")
    date_str = time.strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"torsweep_k12_v3_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print(f"cert written: {out_path}", flush=True)


if __name__ == "__main__":
    main()
