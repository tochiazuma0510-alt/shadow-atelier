#!/usr/bin/env python3
# crosscheck/check_aside3_contents.py
# Independent checker for search/certs/aside3_contents_v1_20260806.json
# (R-1, 裁定721). Reads ONLY the cert JSON -- does NOT import
# search/aside3_contents_v1.py or any aside* driver (search/crosscheck
# separation). Re-derives: each content's factorization-product consistency,
# and M_exceptional_primes/M_value as the union/product over the 6 reported
# contents' factorizations.
import json
import sys
from math import prod

CERT_PATH = "search/certs/aside3_contents_v1_20260806.json"


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

    if doc.get("schema") != "shadow-atelier/aside3_contents/v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/aside3_contents/v1")

    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    forbidden = ["不均衡", "SYN-0", "k*", "段差"]
    blob = json.dumps(doc, ensure_ascii=False)
    for word in forbidden:
        if word in blob:
            fail(f"forbidden verdict text '{word}' found -- S-AS-5 VERDICT_IN_CODE")
    ok("S-AS-5 rescan: no forbidden verdict strings")

    content_report = doc.get("content_report", {})
    all_primes_seen = set()
    for name, row in content_report.items():
        num = row.get("content_numerator")
        den = row.get("content_denominator")
        num_fact = row.get("content_numerator_factorization", {})
        den_fact = row.get("content_denominator_factorization", {})

        num_prod = prod(int(k) ** v for k, v in num_fact.items()) if num_fact else 1
        den_prod = prod(int(k) ** v for k, v in den_fact.items()) if den_fact else 1
        if num_prod != abs(num):
            fail(f"{name}: numerator factorization {num_fact} product {num_prod} != |{num}|")
        else:
            ok(f"{name}: numerator factorization consistent (|{num}|)")
        if den_prod != abs(den):
            fail(f"{name}: denominator factorization {den_fact} product {den_prod} != |{den}|")
        else:
            ok(f"{name}: denominator factorization consistent (|{den}|)")

        # numerator and denominator of a reduced Fraction must be coprime
        # (no shared prime) -- re-verify from the two factorization dicts.
        shared = set(num_fact.keys()) & set(den_fact.keys())
        if shared:
            fail(f"{name}: numerator and denominator factorizations share prime(s) {shared} "
                 f"-- content Fraction not in lowest terms?")
        else:
            ok(f"{name}: numerator/denominator factorizations share no prime (lowest terms OK)")

        all_primes_seen |= set(int(k) for k in num_fact.keys())
        all_primes_seen |= set(int(k) for k in den_fact.keys())

    rederived_M = sorted(all_primes_seen)
    rederived_M_value = 1
    for q in rederived_M:
        rederived_M_value *= q

    cert_M = doc.get("M_exceptional_primes")
    cert_M_value = doc.get("M_value")
    if rederived_M != cert_M:
        fail(f"M_exceptional_primes rederived={rederived_M} != cert={cert_M}")
    else:
        ok(f"M_exceptional_primes rederives correctly: {cert_M}")
    if rederived_M_value != cert_M_value:
        fail(f"M_value rederived={rederived_M_value} != cert={cert_M_value}")
    else:
        ok(f"M_value rederives correctly: {cert_M_value}")

    print()
    print("=== raw content table (re-read from cert only) ===")
    for name, row in content_report.items():
        print(f"  {name}: {row.get('content_numerator')}/{row.get('content_denominator')} "
              f"num_fact={row.get('content_numerator_factorization')} "
              f"den_fact={row.get('content_denominator_factorization')}")
    print(f"  M_exceptional_primes = {cert_M}, M_value = {cert_M_value}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (all cert-internal factorization/M-derivation relations "
              "re-derive correctly; this does NOT independently recompute sigma_m/v1/v2 from scratch)")
        sys.exit(0)


if __name__ == "__main__":
    main()
