#!/usr/bin/env python3
# crosscheck/check_e12_second_system.py
# Independent checker for the CR-1 second-system / P-CONE-2 cert
# (裁定759(5), search/certs/e12_second_system_v1_20260807.json). Does NOT
# import search/e12_second_system_v1.py or search/e12_second_system_blind_derivation.py
# (search/crosscheck separation). Reads three DATA sources directly (not
# search/ code): the primary-source note (docs/scout/...verbatim_v1.md,
# to extract the first-system's embedded JSON exactly as the cert claims
# to have done), the second system's raw output JSON
# (search/certs/e12_blind_derivation_raw_20260807.json, a data artifact,
# not code), and the cert itself -- then independently re-derives every
# comparison, gcd, and boolean the cert reports.
import hashlib
import json
import re
import sys
from math import gcd

CERT_PATH = "search/certs/e12_second_system_v1_20260807.json"
NOTE_PATH = "docs/scout/brown_e12_coefficients_verbatim_v1.md"
BLIND_JSON_PATH = "search/certs/e12_blind_derivation_raw_20260807.json"
NOTE_STATED_SHA256 = "baaa7580a6f6d45ee1a40dc2472ae92d49b7636a1dc33912667ce799d62acc1f"


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

    if doc.get("schema") != "shadow-atelier/e12_second_system_v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/e12_second_system_v1")

    # ---- re-extract first-system JSON from the note directly, verify sha256 ----
    note_text = open(NOTE_PATH, encoding="utf-8").read()
    m = re.search(r"```json\n(.*?)\n```", note_text, re.DOTALL)
    if not m:
        fail("could not locate ```json block in note")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    blob = m.group(1)
    blob_sha256 = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    if blob_sha256 != NOTE_STATED_SHA256:
        fail(f"recomputed sha256={blob_sha256} != note-stated {NOTE_STATED_SHA256}")
    else:
        ok(f"independently recomputed sha256 of note's embedded JSON matches note's own claim: {blob_sha256}")
    if blob_sha256 != doc.get("first_system_json_sha256_recomputed"):
        fail(f"cert's first_system_json_sha256_recomputed={doc.get('first_system_json_sha256_recomputed')} "
             f"!= independently recomputed {blob_sha256}")
    else:
        ok("cert's recomputed sha256 matches independent recomputation")

    first_system = json.loads(blob)
    blind = json.load(open(BLIND_JSON_PATH, encoding="utf-8"))

    first_terms = {tuple(w): c for w, c in first_system["terms"]}
    second_terms = {tuple(w): c for w, c in blind["terms"]}

    only_first = sorted(set(first_terms) - set(second_terms))
    only_second = sorted(set(second_terms) - set(first_terms))
    common = set(first_terms) & set(second_terms)
    coeff_mismatches = [{"monomial": list(k), "first_system": first_terms[k], "second_system": second_terms[k]}
                         for k in sorted(common) if first_terms[k] != second_terms[k]]
    full_match = (len(first_terms) == len(second_terms) == 118 and
                  not only_first and not only_second and not coeff_mismatches)

    tc = doc.get("term_comparison", {})
    if tc.get("n_terms_first_system") != len(first_terms) or tc.get("n_terms_second_system") != len(second_terms):
        fail(f"cert term counts {tc.get('n_terms_first_system')}/{tc.get('n_terms_second_system')} "
             f"!= recomputed {len(first_terms)}/{len(second_terms)}")
    else:
        ok(f"cert term counts match recomputation: first={len(first_terms)} second={len(second_terms)}")
    if [list(w) for w in only_first] != tc.get("only_in_first_system"):
        fail(f"only_in_first_system mismatch: recomputed {only_first} vs cert {tc.get('only_in_first_system')}")
    if [list(w) for w in only_second] != tc.get("only_in_second_system"):
        fail(f"only_in_second_system mismatch: recomputed {only_second} vs cert {tc.get('only_in_second_system')}")
    if coeff_mismatches != tc.get("coefficient_mismatches_on_common_monomials"):
        fail(f"coefficient_mismatches mismatch: recomputed {coeff_mismatches} "
             f"vs cert {tc.get('coefficient_mismatches_on_common_monomials')}")
    if full_match != tc.get("full_term_by_term_match"):
        fail(f"full_term_by_term_match recomputed={full_match} != cert {tc.get('full_term_by_term_match')}")
    else:
        ok(f"full_term_by_term_match independently recomputed and confirmed: {full_match} "
           f"(118/118 monomials, all coefficients identical between the two systems)")

    if not full_match:
        if doc.get("stop_code") != "TERM_MISMATCH":
            fail(f"term mismatch found but cert stop_code={doc.get('stop_code')} != TERM_MISMATCH")
        print()
        print(f"CROSSCHECK RESULT: {'FAIL' if fails else 'PASS (STOP state correctly recorded)'} ({len(fails)} issues)")
        sys.exit(1 if fails else 0)

    if doc.get("stop_code") is not None:
        fail(f"terms fully matched but cert stop_code={doc.get('stop_code')} != None")

    # ---- anchor 11 (antisymmetry), recomputed purely from second-system data ----
    antisym_mismatches = []
    for w, c in second_terms.items():
        rev = (w[3], w[2], w[1], w[0])
        if second_terms.get(rev) != -c:
            antisym_mismatches.append({"monomial": list(w), "coeff": c, "reverse_monomial": list(rev),
                                        "reverse_coeff": second_terms.get(rev)})
    if antisym_mismatches != doc.get("anchor_11_antisymmetry_mismatches"):
        fail(f"anchor_11 mismatches list differs: recomputed {antisym_mismatches} "
             f"vs cert {doc.get('anchor_11_antisymmetry_mismatches')}")
    else:
        ok(f"anchor 11 (antisymmetry) independently recomputed: {len(antisym_mismatches)} mismatches "
           f"(matches cert)")

    # ---- anchor 1,2,3,4 values, recomputed straight from second_terms ----
    def coeff(w):
        return second_terms.get(w, 0)

    anchors_recomputed = {
        "1": coeff((0, 0, 7, 1)),
        "2": coeff((3, 2, 2, 1)),
        "3": coeff((2, 5, 0, 1)),
        "4": len(second_terms),
    }
    expected = {"1": 1, "2": -116, "3": -57, "4": 118}
    if anchors_recomputed != expected:
        fail(f"anchor values recomputed {anchors_recomputed} != paper-stated {expected}")
    else:
        ok(f"anchors 1-4 independently recomputed straight from second-system terms: {anchors_recomputed} "
           f"(matches paper-printed values)")
    cert_anchors = doc.get("anchors_in_scope_reproduced", {})
    for k, expect_val in expected.items():
        cert_second_val = cert_anchors.get(k, {}).get("value_second_system")
        if cert_second_val != expect_val:
            fail(f"cert anchors_in_scope_reproduced['{k}'].value_second_system={cert_second_val} "
                 f"!= expected {expect_val}")
    else:
        ok("cert's anchors_in_scope_reproduced second-system values match expected paper anchors")

    # ---- P-CONE-2 gcd, recomputed independently on BOTH systems ----
    def gcd_all(coeffs):
        g = 0
        for c in coeffs:
            g = gcd(g, abs(c))
        return g

    gcd_first = gcd_all(first_terms.values())
    gcd_second = gcd_all(second_terms.values())
    pc = doc.get("P_CONE_2", {})
    if gcd_first != pc.get("gcd_all_118_coefficients_first_system"):
        fail(f"recomputed gcd_first={gcd_first} != cert {pc.get('gcd_all_118_coefficients_first_system')}")
    else:
        ok(f"gcd of first-system's 118 coefficients independently recomputed: {gcd_first}")
    if gcd_second != pc.get("gcd_all_118_coefficients_second_system"):
        fail(f"recomputed gcd_second={gcd_second} != cert {pc.get('gcd_all_118_coefficients_second_system')}")
    else:
        ok(f"gcd of second-system's 118 coefficients independently recomputed: {gcd_second}")
    agree = (gcd_first == gcd_second)
    if agree != pc.get("gcd_agrees_across_both_systems"):
        fail(f"gcd_agrees_across_both_systems recomputed={agree} != cert {pc.get('gcd_agrees_across_both_systems')}")
    else:
        ok(f"gcd_agrees_across_both_systems re-derives correctly: {agree}")
    gcd_is_1 = (gcd_second == 1)
    if gcd_is_1 != pc.get("gcd_equals_1"):
        fail(f"gcd_equals_1 recomputed={gcd_is_1} != cert {pc.get('gcd_equals_1')}")
    else:
        ok(f"P-CONE-2 raw gcd_equals_1 re-derives correctly: {gcd_is_1}")

    expect_fact = {str(p): e for p, e in factorize(gcd_second).items()}
    if expect_fact != pc.get("gcd_factorization"):
        fail(f"gcd_factorization recomputed {expect_fact} != cert {pc.get('gcd_factorization')}")

    if "CR2" not in "".join(doc.get("scope_limitation_CR2", "")).upper().replace("CR-2", "CR2") and \
       "CR-2" not in doc.get("scope_limitation_CR2", ""):
        fail("scope_limitation_CR2 field does not reference CR-2")
    else:
        ok("scope_limitation_CR2 field present and references CR-2 (LAT-ls lattice-definition caveat)")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (independently re-extracted the first-system JSON from the note "
              "and sha256-verified it, independently recomputed the full 118-term comparison against the "
              "second system's raw data, independently recomputed anchors 1-4 and 11, and independently "
              "recomputed gcd(coefficients) on both systems -- all match the cert exactly; "
              "cross-checked, not 'verified' (reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
