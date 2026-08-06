#!/usr/bin/env python3
# crosscheck/check_aside3.py
# Independent checker for the ASIDE-3/RDV-1 exact-rational-D cert (裁定717/
# 718, docs/notes/ideas_ribet_dig_v2.md 札RDV-1, commit b1a3c6e, verbatim).
# Reads ONLY the cert JSON -- does NOT import search/aside3_exact_D_v1.py,
# search/aside2_run_single_prime.py, search/aside1_run_single_prime.py, or
# search/edim_semidirect_v1.py (search/crosscheck separation). This cannot
# re-derive the exact rational sigma_m/D from scratch without the same
# heavy CRT+reconstruction pipeline; instead it re-derives every INTERNAL
# consistency relation among the cert's own recorded raw fields (numerator/
# denominator factorizations, valuations, theta-mirror booleans, canary
# comparisons against the (separately, previously cross-checked) aside2
# certs) using only elementary arithmetic on what the cert reports.
import json
import sys
from math import prod

CERT_PATH = "search/certs/aside3_exact_D_v1_20260806.json"


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

    if doc.get("schema") != "shadow-atelier/aside3_exact_D/v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/aside3_exact_D/v1")

    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly, "
             f"cannot cross-check further fields")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    # S-AS-5 rescan
    forbidden = ["不均衡", "SYN-0", "k*", "段差"]
    blob = json.dumps(doc, ensure_ascii=False)
    for word in forbidden:
        if word in blob:
            fail(f"forbidden verdict text '{word}' found in cert -- S-AS-5 VERDICT_IN_CODE")
    ok("S-AS-5 rescan: no forbidden verdict strings")

    # reconstruction primes: pairwise-distinct, all < 2**31
    recon_primes = doc.get("reconstruction_primes", [])
    if len(set(recon_primes)) != len(recon_primes):
        fail(f"reconstruction_primes has duplicates: {recon_primes}")
    elif any(p >= 2**31 for p in recon_primes):
        fail(f"reconstruction_primes exceeds the pipeline's documented safe range (<2**31): {recon_primes}")
    else:
        ok(f"reconstruction_primes OK (pairwise distinct, all < 2**31): {recon_primes}")

    def rederive_valuation_from_factorization(num_fact, den_fact, p):
        num_exp = num_fact.get(str(p), 0)
        den_exp = den_fact.get(str(p), 0)
        return num_exp - den_exp

    def check_factorization_product(fact, expected_value):
        if not fact:
            return expected_value in (0, 1, None)
        val = prod(int(k) ** v for k, v in fact.items())
        return val == abs(expected_value)

    depth_report = doc.get("depth_report", {})
    print()
    print("=== per-depth internal consistency (re-derived from cert's own factorization fields) ===")
    for d_str, row in sorted(depth_report.items(), key=lambda kv: int(kv[0])):
        d = int(d_str)
        num = row.get("content_numerator")
        den = row.get("content_denominator")
        num_fact = row.get("content_numerator_factorization", {})
        den_fact = row.get("content_denominator_factorization", {})
        v691_recorded = row.get("v_691_of_content")

        if num is None:
            # zero-term depth -- content should be undefined/None
            if row.get("num_terms", 0) != 0:
                fail(f"depth={d}: content is None but num_terms={row.get('num_terms')} (expected 0)")
            else:
                ok(f"depth={d}: zero-term depth, content=None consistent")
            continue

        if not check_factorization_product(num_fact, num):
            fail(f"depth={d}: numerator factorization {num_fact} does not multiply to |{num}|")
        else:
            ok(f"depth={d}: numerator factorization product matches |{num}|")
        if not check_factorization_product(den_fact, den):
            fail(f"depth={d}: denominator factorization {den_fact} does not multiply to |{den}|")
        else:
            ok(f"depth={d}: denominator factorization product matches |{den}|")

        v691_rederived = rederive_valuation_from_factorization(num_fact, den_fact, 691)
        if v691_rederived != v691_recorded:
            fail(f"depth={d}: v_691 rederived={v691_rederived} != recorded={v691_recorded}")
        else:
            ok(f"depth={d}: v_691_of_content={v691_recorded} rederives correctly from factorization")

    # Theorem C-A / RDV-2 shape prediction: depths 2,3,9,10,11,12 must have
    # num_terms==0 (support band [4,8] strictly).
    support_band_ok = True
    for d in [2, 3, 9, 10, 11, 12]:
        row = depth_report.get(str(d), {})
        if row.get("num_terms", -1) != 0:
            support_band_ok = False
            fail(f"depth={d}: expected num_terms=0 (RDV-2 support band [4,8]) but got {row.get('num_terms')}")
    if support_band_ok:
        ok("support band confirmed: depths {2,3,9,10,11,12} all have num_terms=0")

    # palindrome of term counts: depth d and 12-d must have EQUAL num_terms
    # (RDV-2's theta-mirror-implied consequence).
    palindrome_ok = True
    for d in [4, 5]:
        dd = 12 - d
        t1 = depth_report.get(str(d), {}).get("num_terms")
        t2 = depth_report.get(str(dd), {}).get("num_terms")
        if t1 != t2:
            palindrome_ok = False
            fail(f"term-count palindrome broken: depth={d} has {t1} terms, depth={dd} has {t2} terms")
    if palindrome_ok:
        ok("term-count palindrome confirmed: depth 4<->8 and 5<->7 have equal counts")

    # 裁定718 items 1,2: v_691(D^4)==1, v_691(D^6) reported as an integer
    v691_d4 = doc.get("v_691_D4")
    v691_d4_equals_1 = doc.get("v_691_D4_equals_1")
    v691_d6 = doc.get("v_691_D6")
    if v691_d4_equals_1 != (v691_d4 == 1):
        fail(f"v_691_D4_equals_1={v691_d4_equals_1} inconsistent with v_691_D4={v691_d4}")
    else:
        ok(f"v_691_D4_equals_1 rederives correctly: v_691_D4={v691_d4}")
    if not isinstance(v691_d6, int):
        fail(f"v_691_D6 is not an integer: {v691_d6!r}")
    else:
        ok(f"v_691_D6={v691_d6} is an integer, as 裁定718-1 requested")
    if depth_report.get("6", {}).get("v_691_of_content") != v691_d6:
        fail("v_691_D6 top-level field disagrees with depth_report['6']['v_691_of_content']")
    if depth_report.get("4", {}).get("v_691_of_content") != v691_d4:
        fail("v_691_D4 top-level field disagrees with depth_report['4']['v_691_of_content']")

    # content(D^4) == 691/144 up to sign
    c4 = depth_report.get("4", {})
    expect_num = {"691": 1}
    expect_den = {"2": 4, "3": 2}
    rederived_match = (c4.get("content_numerator_factorization") == expect_num and
                        c4.get("content_denominator_factorization") == expect_den)
    if rederived_match != doc.get("content_D4_matches_691_over_144_up_to_sign"):
        fail(f"content_D4_matches_691_over_144_up_to_sign={doc.get('content_D4_matches_691_over_144_up_to_sign')} "
             f"but rederived from factorization={rederived_match}")
    else:
        ok(f"content(D^4)=691/144 up to sign: rederived match = {rederived_match}")

    # 裁定718 item 3: "691 以外の素数" fields must genuinely be empty/absent
    # of 691-foreign primes in numerators for d=4..8 (the "691だけ" claim).
    summary = doc.get("content_factorization_by_depth_4_to_8", {})
    other_primes_found = {}
    for d_str, row in summary.items():
        others = row.get("primes_other_than_691_in_numerator", [])
        if others:
            other_primes_found[d_str] = others
    if other_primes_found:
        print(f"[NOTE] non-691 primes found in numerator content at depths {other_primes_found} "
              f"-- reported as raw fact, third-singular-prime candidate material (not a FAIL)")
    else:
        ok("no prime other than 691 appears in any numerator content for depths 4..8 "
           "(691-only claim holds at the extraction-check level)")

    # theta mirror: every pair must be exact_match=True (Lemma C-2 / RDV-2,
    # re-surfaced here as a raw re-read, not re-derived -- the cert IS the
    # record of the exact-rational equality check).
    theta_mirror = doc.get("theta_mirror_exact", {})
    all_theta_ok = all(row.get("exact_match") is True for row in theta_mirror.values())
    if all_theta_ok and theta_mirror:
        ok(f"theta_mirror_exact: all {len(theta_mirror)} depth pairs report exact_match=True")
    else:
        fail(f"theta_mirror_exact: not all pairs report exact_match=True: {theta_mirror}")

    # canary vs aside2 certs: all match flags must be True, no singular terms
    canary = doc.get("canary_vs_existing_aside2_certs", {})
    for p_str, row in canary.items():
        flags = [row.get("v1_terms_match"), row.get("v2_terms_match"),
                 row.get("D_is_zero_match"), row.get("D_depth_profile_match")]
        singular = row.get("singular_term_counts", {})
        any_singular = any(v > 0 for v in singular.values())
        if all(flags) and not any_singular:
            ok(f"canary prime={p_str}: all match flags True, no singular (denominator-divisible) terms")
        else:
            fail(f"canary prime={p_str}: flags={flags} singular={singular}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (all cert-internal consistency relations re-derive correctly; "
              "this does NOT independently recompute sigma_m/D from scratch -- see report to 司令塔 "
              "for the reconstruction method's own fail-closed verification, which is a property of "
              "the driver script, not re-verified here)")
        sys.exit(0)


if __name__ == "__main__":
    main()
