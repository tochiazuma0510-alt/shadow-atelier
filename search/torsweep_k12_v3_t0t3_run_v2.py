#!/usr/bin/env python3
"""
torsweep_k12_v3_t0t3_run_v2.py -- TOR-SWEEP stages T0-T3 at k=12, v2 per
裁定785 (efficiency ruling).

裁定785 point 1 (T2/T3 半冗長性の解消): rank(N_12 mod p) is intrinsic to the
abstract subspace H_12 (basis-independent), and for p>=5 theorem TOR-S3
gives H_12 (x) F_p = ker(1+theta, 1+tau+tau2) mod p regardless of which
Z-lattice/basis was used to construct H_12 -- so a mod-p rank measured by
an entirely different construction (the E-DIM "ritual" single-prime
measurement, edim_run_c12_single_prime.py via compute_H_S_at_k_safe) of
the SAME mathematical map nu_12 o j |_{H_12} is a legitimate independent
second system for the two primes it already covers. This script:
  - REUSES the ritual certs' k=12 raw values for primes 2147483647 and
    998244353 (search/certs/edim_c12_691_prime_{p}_v1_20260806.json,
    results["12"]: S_dim, H_dim) instead of recomputing rank_nu_j_on_
    subspace_ambient for those two primes on the reconstructed HNF basis B.
  - COMPUTES FRESH only the non-duplicate prime 1000000007 on B (the only
    prime T-c needs that the ritual certs do not already cover).
T4/T5 (the integer TOR-DET certificate) remain entirely self-computed, as
before -- 裁定785 point 1 only trims T2/T3's redundant mod-p rank work.

裁定785 point 2 (k=13 efficiency gate): this script does NOT proceed to
k=13. It prints a single FG-H instrumentation line (nnz(restricted),
|all_keys| for k=12, read off the one fresh-computed prime's certificate
via edim_semidirect_v1.rank_nu_j_on_subspace_ambient's new fg_h_* fields --
no separate/new computation) for the coordinator to use in the k=13 routing
decision (Sol slim-down WFS-ENG-1 / GHA offload / old-path). k=13 is
explicitly out of scope for this script.

Base: torsweep_k12_v3_t0t3_run.py (unmodified, kept as-is for provenance).
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

# The two primes already measured independently by the E-DIM "ritual" run
# (edim_run_c12_single_prime.py) -- reused per 裁定785(1), not recomputed.
REUSED_RITUAL_PRIMES = [2147483647, 998244353]
RITUAL_CERT_PATHS = {
    2147483647: os.path.join(REPO_ROOT, "search", "certs",
                              "edim_c12_691_prime_2147483647_v1_20260806.json"),
    998244353: os.path.join(REPO_ROOT, "search", "certs",
                             "edim_c12_691_prime_998244353_v1_20260806.json"),
}
# The one prime NOT covered by the ritual certs -- computed fresh on the
# reconstructed HNF basis B, per 裁定785(1) "非重複分のみ自前計算".
FRESH_PRIME = 1000000007
RANK_PRIMES = REUSED_RITUAL_PRIMES + [FRESH_PRIME]


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
        "schema": "tor_sweep_k12_v3.2",
        "ruling_refs": ["裁定745", "裁定754", "裁定785"],
        "v2_change_note": "裁定785(1): T2/T3 reuses ritual-cert mod-p rank "
                           "at 2 primes (basis-independence, theorem "
                           "TOR-S3, p>=5) as second-system cross-check; "
                           "only the non-duplicate prime is self-computed. "
                           "裁定785(2): k=13 explicitly out of scope here, "
                           "FG-H nnz/all_keys reported as byproduct of the "
                           "one required fresh computation.",
        "input_certs": {
            "v1": "search/certs/torsweep_k12_v1_20260807.json",
            "v3_hnf_kernel": "search/certs/torsweep_k12_v3_hnf_kernel_20260807.json",
            "ritual_2147483647": "search/certs/edim_c12_691_prime_2147483647_v1_20260806.json",
            "ritual_998244353": "search/certs/edim_c12_691_prime_998244353_v1_20260806.json",
        },
        "design_spec": "docs/notes/tor_sweep_design_v1.md",
        "k": K,
        "generated_by": {
            "tool": "search/torsweep_k12_v3_t0t3_run_v2.py",
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

    # T1 -- thin re-record of the v3_hnf_kernel cert's own verification
    # battery (unchanged from v1 script).
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
    # T2/T3 v2 (裁定785(1)): 2 primes reused from the ritual cert (second
    # system, basis-independent by TOR-S3), 1 prime self-computed fresh on
    # the reconstructed B.
    # =========================================================================
    record("T2/T3 v2: reusing ritual-cert mod-p rank at "
           f"{REUSED_RITUAL_PRIMES}, self-computing only {FRESH_PRIME}")
    per_prime = {}

    for q in REUSED_RITUAL_PRIMES:
        path = RITUAL_CERT_PATHS[q]
        with open(path, "r", encoding="utf-8") as f:
            ritual = json.load(f)
        ritual_sha = sha256_of_file(path)
        r12 = ritual["results"]["12"]
        H_dim_ritual = r12["H_dim"]
        S_dim_ritual = r12["S_dim"]
        rank_reused = H_dim_ritual - S_dim_ritual
        per_prime[str(q)] = {
            "rank": int(rank_reused),
            "source": "reused_from_ritual_cert",
            "ritual_cert_path": os.path.relpath(path, REPO_ROOT).replace(os.sep, "/"),
            "ritual_cert_sha256": ritual_sha,
            "ritual_raw": {"H_dim": H_dim_ritual, "S_dim": S_dim_ritual,
                            "elapsed_sec": r12.get("elapsed_sec"),
                            "peak_rss_mb": r12.get("peak_rss_mb")},
            "cross_check_rationale": "rank(nu_12 o j |_H12) mod p is "
                "intrinsic to the abstract map on the abstract subspace "
                "H_12 (basis-independent). For p>=5, theorem TOR-S3 "
                "(Maschke) gives H_12 (x) F_p = ker(1+theta,1+tau+tau2) "
                "mod p regardless of which Z-construction of H_12 is "
                "used -- so the ritual cert's independently-constructed "
                "H_12@p (via edim_run_c12_single_prime.py / "
                "compute_H_S_at_k_safe, NOT derived from our HNF basis B) "
                "measures the same map. rank_reused = H_dim - S_dim from "
                "the ritual cert's own k=12 entry.",
        }
        record(f"T2/T3: q={q} rank={rank_reused} (reused from ritual cert "
               f"{path}, H_dim={H_dim_ritual} S_dim={S_dim_ritual})")

    t23_start = time.time()
    subspace_basis_modq = np.array(
        [[v % FRESH_PRIME for v in row] for row in B], dtype=np.int64).T
    assert subspace_basis_modq.shape == (dim_h, H_rank)
    h_alg2_q = ed.GradedLie(2, K, FRESH_PRIME)
    t_q0 = time.time()
    r_q = ed.rank_nu_j_on_subspace_ambient(K, h_alg2_q, subspace_basis_modq, FRESH_PRIME)
    t_q_elapsed = time.time() - t_q0
    nu_cert = getattr(h_alg2_q, "_last_nu_rank_certificate", {})
    per_prime[str(FRESH_PRIME)] = {
        "rank": int(r_q),
        "source": "self_computed_fresh",
        "elapsed_seconds": t_q_elapsed,
        "restricted_dense_bytes": nu_cert.get("restricted_dense_bytes"),
        "ambient_dim": nu_cert.get("ambient_dim"),
        "domain_dim": nu_cert.get("domain_dim"),
        "fg_h_nnz_restricted": nu_cert.get("fg_h_nnz_restricted"),
        "fg_h_all_keys_count": nu_cert.get("fg_h_all_keys_count"),
    }
    record(f"T2/T3: q={FRESH_PRIME} rank={r_q} elapsed={t_q_elapsed:.2f}s "
           f"(self-computed, fresh) "
           f"fg_h_nnz_restricted={nu_cert.get('fg_h_nnz_restricted')} "
           f"fg_h_all_keys_count={nu_cert.get('fg_h_all_keys_count')}")

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
        "elapsed_seconds_self_computed_portion_only": t23_elapsed,
    }
    cert["canaries"]["T-c"] = {
        "ranks_by_prime": {str(q): per_prime[str(q)]["rank"] for q in RANK_PRIMES},
        "sources_by_prime": {str(q): per_prime[str(q)]["source"] for q in RANK_PRIMES},
        "pass": canary_Tc_pass,
        "note": "2/3 primes reused from an independently-constructed "
                "second system (ritual cert) per 裁定785(1); 1/3 primes "
                "self-computed fresh on the reconstructed HNF basis B.",
    }
    record(f"T2/T3: r_prime={r_prime} dim_S_Q={dim_S_Q} "
           f"(expected {EXPECTED_S}, match={S_regression_match}) "
           f"canary_Tc_pass={canary_Tc_pass} "
           f"elapsed(self-computed portion)={t23_elapsed:.2f}s")

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
    cert["stop_rules"]["k13-gate-裁定785(2)"] = {
        "note": "this script stops after k=12 T2/T3; k=13 is explicitly "
                "out of scope here and is NOT auto-started. See the "
                "printed FG-H one-line report (nnz(restricted), "
                "|all_keys| for k=12) for the coordinator's routing "
                "decision (Sol slim-down WFS-ENG-1 / GHA offload / old "
                "path) before any k=13 work begins.",
    }
    cert["total_elapsed_seconds"] = total_elapsed
    write_cert(cert, log)
    record(f"DONE. total_elapsed={total_elapsed:.2f}s")

    # 裁定785(2): FG-H one-line report, byproduct of the one required
    # fresh computation above -- no separate/new run.
    fg_nnz = per_prime[str(FRESH_PRIME)]["fg_h_nnz_restricted"]
    fg_keys = per_prime[str(FRESH_PRIME)]["fg_h_all_keys_count"]
    print(f"FG-H k=12 (prime={FRESH_PRIME}): nnz(restricted)={fg_nnz} "
          f"|all_keys|(nonzero ambient columns)={fg_keys} "
          f"restricted_shape=({H_rank},{nu_cert.get('ambient_dim')}) "
          "-- k=13 NOT auto-started (裁定785(2) gate); awaiting routing "
          "decision.", flush=True)
    log.append(f"FG-H k=12 (prime={FRESH_PRIME}): nnz(restricted)={fg_nnz} "
               f"|all_keys|(nonzero ambient columns)={fg_keys}")


def write_cert(cert, log_lines):
    cert["run_log"] = log_lines
    out_dir = os.path.join(REPO_ROOT, "search", "certs")
    date_str = time.strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"torsweep_k12_v3_2_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print(f"cert written: {out_path}", flush=True)


if __name__ == "__main__":
    main()
