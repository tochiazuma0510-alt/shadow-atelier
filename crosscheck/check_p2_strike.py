#!/usr/bin/env python3
# crosscheck/check_p2_strike.py
# Independent checker for the P2-STRIKE cert (裁定772/773,
# search/certs/p2_strike_v1_20260807.json). Does NOT import
# search/p2_strike_v1.py or search/p2_strike_blind.py (search/crosscheck
# separation). Independently reimplements Bernoulli-number computation
# (own Akiyama-Tanigawa code) and re-derives v_p(num(B_k*)), v_p(k*!),
# and algorithm B''s alpha/beta/j_star for all 9 targets directly from
# the design doc's frozen target list -- not by reading the blind JSON's
# claimed values and merely checking internal consistency, but by
# RECOMPUTING Bernoulli numbers from scratch for all 9 targets.
import json
import sys
from fractions import Fraction as F
from math import gcd

CERT_PATH = "search/certs/p2_strike_v1_20260807.json"
TARGETS = [(37, 32), (59, 44), (67, 58), (101, 68), (103, 24), (131, 22), (149, 130), (157, 62), (157, 110)]


def bernoulli(n):
    A = [F(0)] * (n + 1)
    for m in range(n + 1):
        A[m] = F(1, m + 1)
        for j in range(m, 0, -1):
            A[j - 1] = j * (A[j - 1] - A[j])
    return A[0]


def val_mod_p2(k, p, cache):
    if k in cache:
        Bk = cache[k]
    else:
        Bk = bernoulli(k)
        cache[k] = Bk
    frac = Bk / k
    num, den = frac.numerator, frac.denominator
    modulus = p * p
    if gcd(den, modulus) != 1:
        return None
    inv_den = pow(den % modulus, -1, modulus)
    return (num * inv_den) % modulus


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

    if doc.get("schema") != "shadow-atelier/p2_strike_v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/p2_strike_v1")
    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    cert_targets = doc.get("S_b_S_c_per_target", [])
    cert_by_pk0 = {(row["p"], row["k0"]): row for row in cert_targets}

    if set(cert_by_pk0.keys()) != set(TARGETS):
        fail(f"target universe mismatch: cert has {sorted(cert_by_pk0.keys())}, expected {sorted(TARGETS)}")
    else:
        ok(f"target universe matches the frozen 9-target list exactly")

    cache = {}
    exceptions_recomputed = []
    for (p, k0) in TARGETS:
        kstar = k0 + p - 1
        B = bernoulli(kstar)
        cache[kstar] = B
        num = abs(B.numerator)
        v = 0
        n = num
        while n % p == 0:
            n //= p
            v += 1
        vk = 0
        q = p
        while q <= kstar:
            vk += kstar // q
            q *= p
        vzeta = v - vk

        cert_row = cert_by_pk0[(p, k0)]
        if (kstar != cert_row["k_star"] or v != cert_row["v_p_num_B"] or
                vk != cert_row["v_p_kfact"] or vzeta != cert_row["v_p_zeta"]):
            fail(f"(p={p},k0={k0}): recomputed k_star={kstar} v_p_num_B={v} v_p_kfact={vk} v_p_zeta={vzeta} "
                 f"!= cert k_star={cert_row['k_star']} v_p_num_B={cert_row['v_p_num_B']} "
                 f"v_p_kfact={cert_row['v_p_kfact']} v_p_zeta={cert_row['v_p_zeta']}")
        else:
            ok(f"(p={p},k0={k0}): independently recomputed k*={kstar} v_p_num_B={v} v_p_kfact={vk} "
               f"v_p_zeta={vzeta} matches cert")
        if v >= 2:
            exceptions_recomputed.append({"p": p, "k0": k0, "k_star": kstar, "v_p_num_B": v})

        # algorithm B'
        val0 = val_mod_p2(k0, p, cache)
        val1 = val_mod_p2(kstar, p, cache)
        if val0 is None or val1 is None:
            fail(f"(p={p},k0={k0}): denominator anomaly in val_mod_p2 recomputation")
            continue
        if val0 % p != 0 or val1 % p != 0:
            fail(f"(p={p},k0={k0}): val_mod_p2 not divisible by p as expected (val0={val0} val1={val1})")
            continue
        alpha_raw = (val0 // p) % p
        ab_raw = (val1 // p) % p
        beta = (ab_raw - alpha_raw) % p
        if beta != 0:
            j_star = (-alpha_raw * pow(beta, p - 2, p)) % p
            degenerate = "unique"
        elif alpha_raw != 0:
            j_star = None
            degenerate = "no_j_star"
        else:
            j_star = None
            degenerate = "all_j_degenerate"

        cert_alpha = cert_row.get("alpha_raw")
        cert_beta = cert_row.get("beta")
        cert_j = cert_row.get("j_star")
        cert_deg = cert_row.get("degenerate_case")
        if alpha_raw != cert_alpha or beta != cert_beta or j_star != cert_j or degenerate != cert_deg:
            fail(f"(p={p},k0={k0}): algorithm B' recomputed alpha={alpha_raw} beta={beta} j*={j_star} "
                 f"class={degenerate} != cert alpha={cert_alpha} beta={cert_beta} j*={cert_j} class={cert_deg}")
        else:
            ok(f"(p={p},k0={k0}): algorithm B' independently recomputed alpha={alpha_raw} beta={beta} "
               f"j*={j_star} class={degenerate} matches cert")

    if exceptions_recomputed != doc.get("exceptions_found_v_ge_2"):
        fail(f"exceptions_found_v_ge_2 recomputed={exceptions_recomputed} != cert {doc.get('exceptions_found_v_ge_2')}")
    else:
        ok(f"exceptions_found_v_ge_2 re-derives correctly: {exceptions_recomputed}")

    canary = all(cert_by_pk0[t]["v_p_num_B"] >= 1 for t in TARGETS)
    if canary != doc["S_a_canary"]["all_v_ge_1"]:
        fail(f"S_a_canary.all_v_ge_1 recomputed={canary} != cert {doc['S_a_canary']['all_v_ge_1']}")
    else:
        ok(f"S_a_canary.all_v_ge_1 re-derives correctly: {canary}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (independent from-scratch Bernoulli-number computation -- own "
              "Akiyama-Tanigawa code, not imported from search/ -- recomputes v_p(num(B_k*)), v_p(k*!), "
              "and algorithm B''s alpha/beta/j_star for all 9 targets directly from the frozen target "
              "list, matching the cert exactly; cross-checked, not 'verified' (reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
