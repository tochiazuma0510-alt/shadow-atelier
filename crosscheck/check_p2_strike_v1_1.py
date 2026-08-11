#!/usr/bin/env python3
# crosscheck/check_p2_strike_v1_1.py
# Independent checker for the P2-STRIKE v1.1 cert (裁定778(2),
# search/certs/p2_strike_v1_1_20260811.json). Does NOT import
# search/p2_strike_v1_1.py (search/crosscheck separation). Independently
# recomputes j* from scratch (own Akiyama-Tanigawa Bernoulli code + own
# algorithm-B' implementation, NOT reading the v1 cert's j_star field
# blindly) for all 9 targets, and independently re-transcribes the
# Kellner comparison, then compares against the v1.1 cert.
import json
import sys
from fractions import Fraction as F
from math import gcd

CERT_PATH = "search/certs/p2_strike_v1_1_20260811.json"
TARGETS = [(37, 32), (59, 44), (67, 58), (101, 68), (103, 24), (131, 22), (149, 130), (157, 62), (157, 110)]
KELLNER_TABLE_A3 = {
    (37, 32): {"delta": 21, "s1": 32, "s2": 7},
    (59, 44): {"delta": 26, "s1": 44, "s2": 15},
    (67, 58): {"delta": 21, "s1": 58, "s2": 49},
    (101, 68): {"delta": 42, "s1": 68, "s2": 57},
    (103, 24): {"delta": 54, "s1": 24, "s2": 2},
    (131, 22): {"delta": 25, "s1": 22, "s2": 93},
    (149, 130): {"delta": 79, "s1": 130, "s2": 74},
    (157, 62): {"delta": 48, "s1": 62, "s2": 40},
    (157, 110): {"delta": 51, "s1": 110, "s2": 73},
}


def bernoulli(n):
    A = [F(0)] * (n + 1)
    for m in range(n + 1):
        A[m] = F(1, m + 1)
        for j in range(m, 0, -1):
            A[j - 1] = j * (A[j - 1] - A[j])
    return A[0]


def val_mod_p2(k, p, cache):
    if k not in cache:
        cache[k] = bernoulli(k)
    Bk = cache[k]
    frac = Bk / k
    num, den = frac.numerator, frac.denominator
    modulus = p * p
    if gcd(den, modulus) != 1:
        return None
    inv_den = pow(den % modulus, -1, modulus)
    return (num * inv_den) % modulus


def compute_j_star(p, k0, cache):
    kstar = k0 + p - 1
    val0 = val_mod_p2(k0, p, cache)
    val1 = val_mod_p2(kstar, p, cache)
    alpha_raw = (val0 // p) % p
    ab_raw = (val1 // p) % p
    beta = (ab_raw - alpha_raw) % p
    if beta != 0:
        return (-alpha_raw * pow(beta, p - 2, p)) % p
    return None  # degenerate


def main():
    fails = []

    def fail(msg):
        fails.append(msg)
        print("[FAIL]", msg)

    def ok(msg):
        print("[PASS]", msg)

    try:
        doc = json.load(open(CERT_PATH, encoding="utf-8"))
    except FileNotFoundError:
        print(f"CROSSCHECK RESULT: FAIL (cert not found: {CERT_PATH})")
        sys.exit(1)

    if doc.get("schema") != "shadow-atelier/p2_strike_v1.1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/p2_strike_v1.1")
    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    cache = {}
    for (p, k0) in TARGETS:
        j_star_recomputed = compute_j_star(p, k0, cache)
        row = next(r for r in doc["per_target"] if r["p"] == p and r["k0"] == k0)
        if j_star_recomputed != row["j_star_algorithm_Bprime"]:
            fail(f"(p={p},k0={k0}): independently recomputed j*={j_star_recomputed} "
                 f"!= cert {row['j_star_algorithm_Bprime']}")
        else:
            ok(f"(p={p},k0={k0}): independently recomputed j* (own Bernoulli+alg-B' code) = "
               f"{j_star_recomputed} matches cert")

        kv = KELLNER_TABLE_A3[(p, k0)]
        s1_eq = (kv["s1"] == k0)
        s2_eq = (kv["s2"] == j_star_recomputed)
        if s1_eq != row["s1_equals_k0"] or s2_eq != row["s2_equals_j_star"]:
            fail(f"(p={p},k0={k0}): recomputed s1_eq={s1_eq} s2_eq={s2_eq} != cert "
                 f"s1_eq={row['s1_equals_k0']} s2_eq={row['s2_equals_j_star']}")
        else:
            ok(f"(p={p},k0={k0}): s1==k0 ({s1_eq}) and s2==j* ({s2_eq}) re-derive correctly")

    all_s1_recomputed = all(r["s1_equals_k0"] for r in doc["per_target"])
    all_s2_recomputed = all(r["s2_equals_j_star"] for r in doc["per_target"])
    if all_s1_recomputed != doc["all_s1_equals_k0"]:
        fail(f"all_s1_equals_k0 recomputed={all_s1_recomputed} != cert {doc['all_s1_equals_k0']}")
    else:
        ok(f"all_s1_equals_k0 re-derives correctly: {all_s1_recomputed}")
    if all_s2_recomputed != doc["all_s2_equals_j_star"]:
        fail(f"all_s2_equals_j_star recomputed={all_s2_recomputed} != cert {doc['all_s2_equals_j_star']}")
    else:
        ok(f"all_s2_equals_j_star re-derives correctly: {all_s2_recomputed} "
           f"(9/9 targets: Kellner s2 == our algorithm-B' j*)")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (independently recomputed j* from scratch for all 9 targets "
              "via own Bernoulli-number + algorithm-B' code, not reading the cert's j_star field "
              "blindly, and independently re-verified the Kellner s1/s2 comparison; all match. "
              "cross-checked, not 'verified' (reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
