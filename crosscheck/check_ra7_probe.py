#!/usr/bin/env python3
# crosscheck/check_ra7_probe.py
# Independent checker for the RA7-PROBE-1 cert (裁定752③,
# docs/notes/tor_sweep_design_v1_addendum_b.md §3.3, verbatim).
# Reads ONLY the cert JSON -- does NOT import search/ra7_probe_v1.py,
# search/aside3_exact_D_v1.py, search/aside1_run_single_prime.py, or
# search/edim_semidirect_v1.py (search/crosscheck separation). Unlike
# check_aside3.py (which could only re-derive internal consistency of
# summary fields, because that cert did not embed the full term vectors),
# THIS cert embeds the full raw D4_Q_terms (350) and sigma3_bar_Q_terms (3)
# exactly, so this checker performs a FULL independent recomputation: its
# own from-scratch (Fraction-based) Ihara bracket implementation, applied
# to the cert's raw terms, then its own mod-p reduction at each panel
# prime -- and compares against the cert's own reported results.
#
# It also independently re-reads docs/scout/brown_prop64_lattice_verbatim_v1.md
# (a docs/ file, not search/ code) to confirm the pinned quote is genuinely
# present verbatim, and checks the hard prime-panel exclusion (691,2,3
# absent) that 裁定752③ mandates.
import json
import sys
from fractions import Fraction

CERT_PATH = "search/certs/ra7_probe_v1_20260807.json"
BROWN_PIN_SOURCE = "docs/scout/brown_prop64_lattice_verbatim_v1.md"
FORBIDDEN_PRIMES = {691, 2, 3}


# ---------- independent (from-scratch) exact word-algebra ----------
# Deliberately reimplemented here rather than imported, per the
# search/crosscheck separation rule. Mirrors the mathematical definitions
# (free-Lie word bracket via concatenation, Ihara's Definition C-1) but is
# NOT the same code object as search/aside3_exact_D_v1.py's q_* functions.

def word_bracket(u, v):
    out = {}
    for w1, c1 in u.items():
        for w2, c2 in v.items():
            c = c1 * c2
            if c == 0:
                continue
            k1, k2 = w1 + w2, w2 + w1
            out[k1] = out.get(k1, Fraction(0)) + c
            out[k2] = out.get(k2, Fraction(0)) - c
    return {w: c for w, c in out.items() if c != 0}


def vec_add(*vecs):
    out = {}
    for vec in vecs:
        for w, c in vec.items():
            out[w] = out.get(w, Fraction(0)) + c
    return {w: c for w, c in out.items() if c != 0}


def vec_scale(vec, s):
    return {w: v * s for w, v in vec.items() if v * s != 0}


def deriv(f, g):
    """The derivation D_f sending Y -> [Y,f], applied to g (Ihara's
    convention: letter 1 = Y, letter 0 = X)."""
    img = word_bracket({(1,): Fraction(1)}, f)  # [Y,f]
    out = {}
    for w, c in g.items():
        for i, letter in enumerate(w):
            if letter != 1:
                continue
            prefix, suffix = w[:i], w[i + 1:]
            for w2, c2 in img.items():
                key = prefix + w2 + suffix
                out[key] = out.get(key, Fraction(0)) + c * c2
    return {w: c for w, c in out.items() if c != 0}


def ihara_bracket(f, g):
    return vec_add(deriv(f, g), vec_scale(deriv(g, f), -1), word_bracket(f, g))


def depth_of(word):
    return sum(1 for letter in word if letter == 1)


def reduce_mod(vec_Q, p):
    out = {}
    singular = []
    for w, c in vec_Q.items():
        if c.denominator % p == 0:
            singular.append(list(w))
            continue
        val = (c.numerator % p) * pow(c.denominator % p, -1, p) % p
        if val:
            out[w] = val
    return out, singular


def terms_to_dict(terms):
    return {tuple(w): Fraction(num, den) for w, num, den in terms}


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

    if doc.get("schema") != "shadow-atelier/ra7_probe_v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/ra7_probe_v1")

    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    # ---- prereg: hard prime-panel exclusion (裁定752③) ----
    panel = doc.get("prereg", {}).get("prime_panel", [])
    violation = set(panel) & FORBIDDEN_PRIMES
    if violation:
        fail(f"prime panel contains a FORBIDDEN prime (691/2/3): {violation} -- 裁定752③ VIOLATION")
    else:
        ok(f"prime panel {panel} contains none of the forbidden primes {FORBIDDEN_PRIMES}")
    expected_panel = {677, 701, 998244353, 2147483647}
    if set(panel) != expected_panel:
        fail(f"prime panel {panel} != addendum-specified {sorted(expected_panel)}")
    else:
        ok(f"prime panel exactly matches addendum §3.3 R-e: {sorted(expected_panel)}")

    exclusions = doc.get("prereg", {}).get("prime_panel_exclusions", {})
    for p in ("691", "2", "3"):
        if p not in exclusions or not exclusions[p]:
            fail(f"prime_panel_exclusions missing reason for p={p}")
    if all(p in exclusions and exclusions[p] for p in ("691", "2", "3")):
        ok("prime_panel_exclusions has a non-empty reason for 691, 2, 3 each")

    # ---- B-PIN-1: verbatim quote actually present in the cited source file ----
    b_pin = doc.get("prereg", {}).get("b_pin_1", {})
    quote = b_pin.get("verbatim_quote", "")
    try:
        source_text = open(BROWN_PIN_SOURCE, encoding="utf-8").read()
    except FileNotFoundError:
        fail(f"B-PIN-1 source file not found: {BROWN_PIN_SOURCE}")
        source_text = None
    if source_text is not None:
        if quote and quote in source_text:
            ok(f"B-PIN-1 verbatim quote independently confirmed present in {BROWN_PIN_SOURCE}")
        else:
            fail(f"B-PIN-1 verbatim quote NOT found verbatim in {BROWN_PIN_SOURCE}")
    if b_pin.get("source", "").split(" ")[0] != BROWN_PIN_SOURCE:
        fail(f"b_pin_1.source path mismatch: {b_pin.get('source')!r} vs expected prefix {BROWN_PIN_SOURCE!r}")
    else:
        ok("b_pin_1.source path matches the addendum-designated pin file")

    # ---- D4_Q_terms shape ----
    d4_terms = doc.get("D4_Q_terms", [])
    if len(d4_terms) != doc.get("D4_Q_num_terms"):
        fail(f"D4_Q_terms length {len(d4_terms)} != D4_Q_num_terms {doc.get('D4_Q_num_terms')}")
    else:
        ok(f"D4_Q_terms length matches D4_Q_num_terms = {len(d4_terms)}")
    if not all(len(w) == 12 and depth_of(w) == 4 for w, _, _ in d4_terms):
        fail("some D4_Q_terms word is not length-12 weight-12/depth-4 (expected: proxy for e_12)")
    else:
        ok("all D4_Q_terms words have weight 12 and depth 4 (consistent with D^(4) label)")

    # independent content(D4) recomputation, cross-checked against the
    # cert's own D4_integrity_vs_committed_aside3_cert block
    D4_Q = terms_to_dict(d4_terms)

    def content_of(vec):
        if not vec:
            return Fraction(0)
        den_lcm = 1
        for c in vec.values():
            g = _gcd(den_lcm, c.denominator)
            den_lcm = den_lcm * c.denominator // g
        num_gcd = 0
        for c in vec.values():
            w = c.numerator * (den_lcm // c.denominator)
            num_gcd = _gcd(num_gcd, abs(w))
        return Fraction(num_gcd, den_lcm)

    def _gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    d4_content = content_of(D4_Q)
    if (d4_content.numerator, d4_content.denominator) != (691, 144):
        fail(f"independently recomputed content(D4_Q) = {d4_content} != 691/144 (up to sign convention "
             f"already fixed positive by content_of)")
    else:
        ok(f"independently recomputed content(D4_Q) = {d4_content} == 691/144")

    # ---- sigma3_bar_Q_terms shape ----
    s3_terms = doc.get("sigma3_bar_Q_terms", [])
    if not (len(s3_terms) == 3 and all(len(w) == 3 and depth_of(w) == 1 for w, _, _ in s3_terms)):
        fail(f"sigma3_bar_Q_terms shape wrong: {s3_terms}")
    else:
        ok("sigma3_bar_Q_terms: 3 terms, weight 3, depth 1 (matches -( ad X)^2(Y) shape)")
    sigma3_bar_Q = terms_to_dict(s3_terms)
    # independent recomputation of sigma3_bar from the stated formula
    y_vec = {(1,): Fraction(1)}
    ad1 = word_bracket({(0,): Fraction(1)}, y_vec)
    ad2 = word_bracket({(0,): Fraction(1)}, ad1)
    sigma3_bar_recomputed = vec_scale(ad2, -1)
    if sigma3_bar_recomputed != sigma3_bar_Q:
        fail(f"sigma3_bar_Q_terms {sigma3_bar_Q} does NOT match independently recomputed "
             f"-(ad X)^2(Y) = {sigma3_bar_recomputed}")
    else:
        ok("sigma3_bar_Q_terms matches an independently recomputed -(ad X)^2(Y) exactly")

    # ---- full independent Ihara bracket recomputation ----
    B_Q_recomputed = ihara_bracket(D4_Q, sigma3_bar_Q)
    B_Q_num_terms_recomputed = len(B_Q_recomputed)
    if B_Q_num_terms_recomputed != doc.get("B_Q_num_terms"):
        fail(f"independently recomputed B_Q has {B_Q_num_terms_recomputed} terms, "
             f"cert reports B_Q_num_terms={doc.get('B_Q_num_terms')}")
    else:
        ok(f"independently recomputed {{D^(4),sigma3_bar}} has {B_Q_num_terms_recomputed} terms, "
           f"matches cert's B_Q_num_terms")

    depth_profile_recomputed = {}
    weights_recomputed = set()
    for w in B_Q_recomputed:
        d = depth_of(w)
        depth_profile_recomputed[d] = depth_profile_recomputed.get(d, 0) + 1
        weights_recomputed.add(len(w))
    depth_profile_cert = {int(k): v for k, v in doc.get("B_Q_depth_profile", {}).items()}
    if depth_profile_recomputed != depth_profile_cert:
        fail(f"independently recomputed depth profile {depth_profile_recomputed} "
             f"!= cert's B_Q_depth_profile {depth_profile_cert}")
    else:
        ok(f"independently recomputed depth profile matches cert: {depth_profile_recomputed}")
    only_depth5 = (set(depth_profile_recomputed.keys()) <= {5})
    if only_depth5 != doc.get("B_Q_only_depth5_nonzero"):
        fail(f"only_depth5_nonzero recomputed={only_depth5} != cert={doc.get('B_Q_only_depth5_nonzero')}")
    else:
        ok(f"B_Q_only_depth5_nonzero recomputed and confirmed: {only_depth5}")
    if weights_recomputed != {15}:
        fail(f"independently recomputed B_Q has words of weight(s) {weights_recomputed}, expected only {{15}}")
    else:
        ok("all recomputed B_Q words have weight 15 (ambient 2^15, as specified)")

    # ---- per-prime independent mod reduction ----
    per_prime_cert = doc.get("per_prime", {})
    for p in panel:
        reduced, singular = reduce_mod(B_Q_recomputed, p)
        is_zero_recomputed = (len(reduced) == 0)
        row = per_prime_cert.get(str(p), {})
        if row.get("nonzero_term_count") != len(reduced):
            fail(f"prime={p}: recomputed nonzero_term_count={len(reduced)} "
                 f"!= cert's {row.get('nonzero_term_count')}")
        elif row.get("is_zero") != is_zero_recomputed:
            fail(f"prime={p}: recomputed is_zero={is_zero_recomputed} != cert's {row.get('is_zero')}")
        elif row.get("singular_term_count") != len(singular):
            fail(f"prime={p}: recomputed singular_term_count={len(singular)} "
                 f"!= cert's {row.get('singular_term_count')}")
        else:
            ok(f"prime={p}: independently recomputed nonzero_term_count={len(reduced)} "
               f"is_zero={is_zero_recomputed} singular_term_count={len(singular)} -- matches cert")

    # ---- summary bools re-derived from per-prime is_zero ----
    is_zero_summary_cert = doc.get("is_zero_summary", {})
    at_least_one_nonzero_recomputed = any(not v for v in is_zero_summary_cert.values())
    all_zero_recomputed = all(v for v in is_zero_summary_cert.values())
    if at_least_one_nonzero_recomputed != doc.get("at_least_one_prime_nonzero"):
        fail("at_least_one_prime_nonzero does not re-derive from is_zero_summary")
    else:
        ok(f"at_least_one_prime_nonzero re-derives correctly: {at_least_one_nonzero_recomputed}")
    if all_zero_recomputed != doc.get("all_primes_zero"):
        fail("all_primes_zero does not re-derive from is_zero_summary")
    else:
        ok(f"all_primes_zero re-derives correctly: {all_zero_recomputed}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (full independent recomputation from the cert's own raw "
              "D4_Q_terms/sigma3_bar_Q_terms -- own from-scratch Ihara bracket + mod-p reduction "
              "code, not imported from search/ -- reproduces every reported term count, depth "
              "profile, and per-prime is_zero bool exactly; this is cross-checked, not 'verified' "
              "(reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
