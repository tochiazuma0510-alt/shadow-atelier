#!/usr/bin/env python3
"""
torsweep_t4_finalize_gha.py -- TOR-DET steps 3-5 (assemble N_source from
B + the two independent-modulus column artifacts, verify agreement,
extract s>=3 Bareiss minors, gcd, T5 factoring+QUAR-TOR if gcd!=1),
GHA job-splittable form (裁定876). Runs LOCALLY too (this is exactly
where the K=11 regression-anchor comparison happens, and where the K=12
GHA run's final cert gets written) -- cheap (small B, small cols, only a
few r'xr' Bareiss determinants), so no reason to keep this on a GHA
runner beyond convenience of a single workflow.

For K=11 (regression anchor, 裁定876(2)): compares gcd_abs against the
ALREADY-KNOWN value from search/certs/torsweep_k11_v1_2_20260807.json
(73 digits, leading "10671575395189358633973201089968978274795128955755"
-- read from that cert at runtime, not hardcoded, so a stale copy here
can never silently diverge from the source of truth) -- must match
EXACTLY (same RNG_SEED=20260807, same PIVOT_CERT_PRIME, same B/M source
cert, same minor-selection algorithm) before this ported code is trusted
for K=12.
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
from torsweep_t4_step1_gha import load_inputs  # noqa: E402 (reuses the SAME B loader as step1 -- single source)

PIVOT_CERT_PRIME = 2147483647
NUM_MINORS_TARGET = 5
RNG_SEED = 20260807

K11_ANCHOR_CERT = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k11_v1_2_20260807.json")


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
    assert step2a["k"] == K and step2b["k"] == K
    r_prime = step1["r_prime"]
    H_rank = step1["H_rank"]
    record(f"K={K} H_rank={H_rank} r_prime={r_prime}")

    cols_a = step2a["cols"]
    cols_b = step2b["cols"]
    exact_moduli_agree = (cols_a == cols_b)
    record(f"exact_moduli_agree={exact_moduli_agree}")

    cert = {
        "schema": "tor_sweep_t4_finalize_gha.1",
        "ruling_refs": ["裁定876"],
        "k": K,
        "H_rank": H_rank, "r_prime": r_prime,
        "pivot_cert_prime": step1["pivot_cert_prime"],
        "exact_modulus_A": step2a["exact_modulus"],
        "exact_modulus_B": step2b["exact_modulus"],
        "exact_moduli_agree": exact_moduli_agree,
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

    _, B, H_rank_loaded, r_prime_loaded, n_cols = load_inputs(K)
    assert H_rank_loaded == H_rank and r_prime_loaded == r_prime

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

    # ---- K=11 regression anchor (裁定876(2)) ----
    if K == 11:
        with open(K11_ANCHOR_CERT, "r", encoding="utf-8") as f:
            anchor = json.load(f)
        anchor_gcd = anchor["stages"]["T4"]["gcd_abs"]
        match = (str(gcd_abs) == anchor_gcd)
        cert["k11_regression_anchor"] = {
            "anchor_cert": "search/certs/torsweep_k11_v1_2_20260807.json",
            "anchor_gcd_abs_digits": len(anchor_gcd),
            "computed_gcd_abs_digits": len(str(gcd_abs)),
            "exact_match": match,
        }
        record(f"K=11 regression anchor: exact_match={match} "
               f"(anchor {len(anchor_gcd)} digits vs computed {len(str(gcd_abs))} digits)")
        if not match:
            cert["stop_rules"]["S-TOR-2-ANCHOR"] = {
                "triggered": True,
                "reason": "K=11 regression anchor MISMATCH -- ported GHA-split "
                          "code does not reproduce the known torsweep_k11_v1_2 "
                          "gcd_abs; DO NOT trust this pipeline for K=12 until "
                          "resolved",
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
                factors[rem] = factors.get(rem, 0) + 1
        unresolved_cofactor = None
        for key in list(factors):
            if isinstance(key, str) and key.startswith("UNFACTORED_COFACTOR"):
                cof = int(factors.pop(key))
                record(f"T5: attempting sympy.factorint on {len(str(cof))}-digit cofactor")
                try:
                    import sympy
                    sub = sympy.factorint(cof, limit=10_000_000)
                except Exception as exc:
                    sub = {cof: 1}
                    record(f"T5: factorint raised {exc!r}")
                for base, exp in sub.items():
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
            jumps = cheap_rank != r_prime
            jump_at_p[str(p)] = {"rank_p": int(cheap_rank), "r_prime": r_prime,
                                  "jumps": jumps, "method": "cheap_N_source_rank"}
            if jumps:
                torsion_primes.append(p)
        cert["stages"]["T5"] = {
            "triggered": True,
            "gcd_abs_prime_factors": {str(k): v for k, v in factors.items()},
            "torsion_primes": torsion_primes,
            "jump_at_p": jump_at_p,
            "unresolved_cofactor": unresolved_cofactor,
            "factorization_fully_resolved": unresolved_cofactor is None,
        }
        record(f"T5: torsion_primes(raw)={torsion_primes}")
        if torsion_primes:
            cert["stop_rules"]["QUAR-TOR"] = {
                "triggered": True, "quarantined_primes": torsion_primes,
                "note": "QUAR-TOR SS5.3 -- 司令塔 disposition required",
            }

    cert["stop_rules"]["S-TOR-4"] = {"note": "no judgement words; raw values/booleans only"}
    cert["total_elapsed_seconds"] = time.time() - t_start
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    record(f"DONE. cert written: {args.out}")
    print(f"TORSWEEP_T4_FINALIZE_DONE k={K} gcd_abs_digits={len(str(gcd_abs))}", flush=True)


if __name__ == "__main__":
    main()
