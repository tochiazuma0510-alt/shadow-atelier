#!/usr/bin/env python3
# crosscheck/check_t2_split.py
# Independent checker for the T2-SPLIT cert (裁定778(1),
# search/certs/t2_split_v1_20260811.json). Does NOT import search/t2_split_v1.py
# (search/crosscheck separation). Reads the T2-HECKE cert directly (data,
# not code) for d_K values and independently recomputes every Legendre
# symbol via its own from-scratch Euler's-criterion implementation.
import json
import sys

CERT_PATH = "search/certs/t2_split_v1_20260811.json"
T2_HECKE_CERT_PATH = "search/certs/t2_hecke_v1_20260807.json"
ECHO_PRIME = {24: 103, 28: 7, 30: 5, 32: 37}


def legendre_symbol(a, p):
    a_mod = a % p
    if a_mod == 0:
        return 0
    ls = pow(a_mod, (p - 1) // 2, p)
    return 1 if ls == 1 else -1


def factorize(n):
    n = abs(n)
    if n <= 1:
        return {}
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


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

    if doc.get("schema") != "shadow-atelier/t2_split_v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/t2_split_v1")
    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    t2 = json.load(open(T2_HECKE_CERT_PATH, encoding="utf-8"))
    order_index = t2["H_g_order_index"]

    for k in [24, 28, 30, 32]:
        d_K_source = order_index[str(k)]["squarefree_part"]
        cert_row = doc["per_k"][str(k)]
        if d_K_source != cert_row["d_K"]:
            fail(f"k={k}: d_K in t2_split cert ({cert_row['d_K']}) != T2-HECKE cert's squarefree_part "
                 f"({d_K_source}) -- source mismatch")
            continue
        else:
            ok(f"k={k}: d_K={d_K_source} correctly sourced from the T2-HECKE cert")

        fact = factorize(d_K_source)
        fact_str = {str(p): e for p, e in fact.items()}
        if fact_str != cert_row["d_K_factorization"]:
            fail(f"k={k}: recomputed d_K factorization {fact_str} != cert {cert_row['d_K_factorization']}")
        else:
            ok(f"k={k}: independently recomputed d_K factorization matches: {fact_str}")

        p = ECHO_PRIME[k]
        if p != cert_row["echo_prime"]:
            fail(f"k={k}: echo_prime mismatch: expected {p}, cert has {cert_row['echo_prime']}")

        ls = legendre_symbol(d_K_source, p)
        if ls != cert_row["legendre_symbol_dK_over_p"]:
            fail(f"k={k}: independently recomputed Legendre symbol ({d_K_source}/{p})={ls} "
                 f"!= cert {cert_row['legendre_symbol_dK_over_p']}")
        else:
            ok(f"k={k}: independently recomputed Legendre symbol ({d_K_source}/{p}) = {ls} matches cert")

    if doc["k32_p37_is_the_open_target"]["legendre_symbol"] != doc["per_k"]["32"]["legendre_symbol_dK_over_p"]:
        fail("k32_p37_is_the_open_target.legendre_symbol does not match per_k['32'].legendre_symbol_dK_over_p")
    else:
        ok("k32_p37_is_the_open_target field consistent with per_k data")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (independently recomputed all 4 Legendre symbols from scratch "
              "via Euler's criterion, and independently verified d_K sourcing against the separately-"
              "loaded T2-HECKE cert; all match. cross-checked, not 'verified' (reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
