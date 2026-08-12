#!/usr/bin/env python3
"""
torsweep_t4_finalize_k13_gha.py -- TOR-DET finalize (steps 3-5) for K=13 specifically (裁定994).

Unlike torsweep_t4_finalize_gha.py (K=11/12, which loads B via torsweep_t4_step1_gha.load_inputs(K)
-- a SMALL, git-committed cert), K=13's EXACT H_basis is a 356MB local-only file (never committed,
per 裁定842(2) receipt convention) that must be transported onto the GHA runner via a GitHub
Release asset (裁定994) rather than git or cross-run artifact download. This script therefore takes
the EXACT B cert path directly (already downloaded + gunzipped + sha256-verified by the calling
workflow step) instead of going through load_inputs(13) (which is for step1's mod-q shortcut ONLY
-- see the warning comment in torsweep_t4_step1_gha.py's K13_B_MODQ_CERT section).

Logic (N_source assembly, independent-minor selection, Bareiss determinants, gcd, T5
factoring+QUAR-TOR-relevant prime listing) is duplicated from torsweep_t4_finalize_gha.py
UNCHANGED (not imported, to avoid any risk of altering the K=11/12 pipeline's behavior -- 847
discipline: this is a new, K=13-specific entry point, not a refactor of the working K=11/12 one).
"""
import argparse
import json
import os
import random
import sys
import time
from math import gcd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
sys.set_int_max_str_digits(0)

from torsweep_k12_run import det_bareiss, small_primes, sha256_of_file  # noqa: E402

PIVOT_CERT_PRIME = 2147483647
NUM_MINORS_TARGET = 5
RNG_SEED = 20260807


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step1-artifact", required=True)
    ap.add_argument("--step2-a-artifact", required=True)
    ap.add_argument("--step2-b-artifact", required=True)
    ap.add_argument("--exact-b-cert", required=True,
                     help="Full torsweep_k13_hnf_construct_v1 cert (gunzipped, sha256-verified by "
                          "the caller), containing the EXACT H_basis matrix")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    random.seed(RNG_SEED)

    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    with open(args.step1_artifact, "r", encoding="utf-8") as f:
        step1 = json.load(f)
    with open(args.step2_a_artifact, "r", encoding="utf-8") as f:
        step2a = json.load(f)
    with open(args.step2_b_artifact, "r", encoding="utf-8") as f:
        step2b = json.load(f)
    assert step2a["modulus_label"] == "A" and step2b["modulus_label"] == "B"
    K = step1["k"]
    assert K == 13, f"this script is K=13-only, got K={K}"
    assert step2a["k"] == K and step2b["k"] == K
    r_prime = step1["r_prime"]
    H_rank = step1["H_rank"]
    record(f"K={K} H_rank={H_rank} r_prime={r_prime}")

    cols_a = step2a["cols"]
    cols_b = step2b["cols"]
    exact_moduli_agree = (cols_a == cols_b)
    record(f"exact_moduli_agree={exact_moduli_agree}")

    cert = {
        "schema": "tor_sweep_t4_finalize_k13_gha.1",
        "ruling_refs": ["裁定876", "裁定992", "裁定994"],
        "k": K,
        "H_rank": H_rank, "r_prime": r_prime,
        "pivot_cert_prime": step1["pivot_cert_prime"],
        "exact_modulus_A": step2a["exact_modulus"],
        "exact_modulus_B": step2b["exact_modulus"],
        "exact_moduli_agree": exact_moduli_agree,
        "exact_b_cert_path": args.exact_b_cert,
        "exact_b_cert_sha256": sha256_of_file(args.exact_b_cert),
        "stages": {}, "stop_rules": {},
    }
    if not exact_moduli_agree:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": "LATTICE_CANARY_FAIL (T4 exact-modulus disagreement)",
        }
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(cert, f, indent=2)
        record("STOP: exact moduli disagree")
        print("TORSWEEP_T4_FINALIZE_STOP", flush=True)
        sys.exit(1)

    record(f"loading exact B from {args.exact_b_cert} (this is the slow/large step)")
    with open(args.exact_b_cert, "r", encoding="utf-8") as f:
        bcert = json.load(f)
    B = bcert["H_basis"]
    H_rank_loaded = bcert["H_rank"]
    n_cols = bcert["dim_h"]
    assert H_rank_loaded == H_rank, (H_rank_loaded, H_rank)
    record(f"B loaded: shape=({H_rank_loaded},{n_cols})")

    N_source = [[sum(B[i][j] * cols_a[j][c] for j in range(n_cols))
                 for c in range(r_prime)]
                for i in range(H_rank)]
    record(f"N_source assembled, shape=({len(N_source)},{len(N_source[0])})")

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
        rows_sel = independent_rows_modp(N_source, PIVOT_CERT_PRIME, order)
        if len(rows_sel) != r_prime:
            continue
        key = tuple(sorted(rows_sel))
        if key in seen:
            continue
        seen.add(key)
        submat = [N_source[i] for i in rows_sel]
        d = det_bareiss(submat)
        if d == 0:
            continue
        minor_dets.append(d)
        minor_row_sets.append(rows_sel)
        if len(minor_dets) >= NUM_MINORS_TARGET:
            break
    record(f"computed {len(minor_dets)} minors, digit_counts={[len(str(d)) for d in minor_dets]}")

    if len(minor_dets) < 3:
        cert["stop_rules"]["S-TOR-1c"] = {
            "triggered": True,
            "reason": f"only {len(minor_dets)} independent minors found, need >=3",
        }
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(cert, f, indent=2)
        record("STOP: fewer than 3 independent minors")
        print("TORSWEEP_T4_FINALIZE_STOP", flush=True)
        sys.exit(1)

    gcd_abs = 0
    for d in minor_dets:
        gcd_abs = gcd(gcd_abs, abs(d))
    record(f"gcd_abs digits={len(str(gcd_abs))}")

    cert["stages"]["T4"] = {
        "N_source_shape": [len(N_source), len(N_source[0])],
        "N_source": N_source,
        "minor_determinants": [str(d) for d in minor_dets],
        "minor_determinant_digit_counts": [len(str(d)) for d in minor_dets],
        "minor_row_sets": minor_row_sets,
        "gcd_abs": str(gcd_abs),
        "gcd_abs_digits": len(str(gcd_abs)),
    }

    # T5 (only if gcd_abs != 1)
    if gcd_abs == 1:
        cert["stages"]["T5"] = {"triggered": False, "reason": "gcd_abs == 1"}
        record("T5: not triggered")
    else:
        record("T5: gcd_abs != 1, factoring")
        rem = gcd_abs
        trial_bound = 2_000_000
        factors = {}
        exhausted = True
        for p in small_primes(trial_bound):
            if p * p > rem:
                exhausted = False
                break
            while rem % p == 0:
                factors[p] = factors.get(p, 0) + 1
                rem //= p
        if rem > 1:
            if exhausted:
                factors[f"UNFACTORED_COFACTOR>{trial_bound}"] = str(rem)
            else:
                factors["UNRESOLVED_COMPOSITE"] = str(rem)
        torsion_primes = []
        for k_, v_ in factors.items():
            if isinstance(k_, int):
                torsion_primes.append(k_)
        cert["stages"]["T5"] = {
            "triggered": True,
            "gcd_abs_prime_factors": {str(k_): v_ for k_, v_ in factors.items()},
            "torsion_primes": torsion_primes,
        }
        record(f"T5: torsion_primes(raw)={torsion_primes}")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2)
    elapsed = time.time() - t_start
    cert["total_elapsed_seconds"] = elapsed
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2)
    record(f"finalize (K=13) done, elapsed={elapsed:.2f}s, artifact written: {args.out}")
    print(f"TORSWEEP_T4_FINALIZE_DONE k={K}", flush=True)


if __name__ == "__main__":
    main()
