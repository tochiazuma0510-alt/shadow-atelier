"""
search/r_intersection_template_v1.py -- PARAMETRIZED TEMPLATE for r = |<[a]> cap <[b]>| in
Q^x/(Q^x)^9 (裁定974 【2】). Same discipline as search/compositum_degree_template_v1.py: sympy,
parametrized function + canary-only __main__, NO real a_9/b_{S4} data plugged in (r measurement's
own Sol-approved design has not yet been supplied by the mathematician -- per instruction, this
template stops at canaries).

Q^x/(Q^x)^9 is (for odd exponent 9) a direct sum of copies of Z/9Z, one per prime -- sign is
irrelevant since -1=(-1)^9 is already a 9th power (matches search/ds4_receipt_v1.py's sign_note).
Given a rational x = prod p^{e_p}, its class [x] corresponds to the vector (e_p mod 9)_p supported
on the (finite) set of primes dividing numerator or denominator. ord([x]) = lcm_p(9/gcd(9, e_p mod
9)). <[x]> = {k*[x] mod 9 : k=0..ord([x])-1}, a cyclic subgroup.

METHOD (direct enumeration, not a closed formula -- both cyclic subgroups have order <=9 so this
is at most 9x9 work): compute the vector for [a] and [b] on the union-of-primes support, enumerate
all multiples k*[a] (k=0..ord(a)-1) and k*[b] (k=0..ord(b)-1) as tuples, intersect the two sets.
r := |intersection|. This is exact (no approximation) since both <[a]> and <[b]> are finite exact
sets of vectors in (Z/9)^S for the finite prime-support set S.
"""
import json
import sys
from fractions import Fraction
from math import gcd

try:
    from sympy import factorint
except ImportError:
    factorint = None

N = 9


def prime_valuations(frac: Fraction):
    num = abs(frac.numerator)
    den = abs(frac.denominator)
    vals = {}
    if factorint is not None:
        for p, e in factorint(num).items():
            vals[p] = vals.get(p, 0) + e
        for p, e in factorint(den).items():
            vals[p] = vals.get(p, 0) - e
    else:
        for n, sign in ((num, 1), (den, -1)):
            x = n
            p = 2
            while p * p <= x:
                while x % p == 0:
                    vals[p] = vals.get(p, 0) + sign
                    x //= p
                p += 1
            if x > 1:
                vals[x] = vals.get(x, 0) + sign
    return {p: e for p, e in vals.items() if e % N != 0}  # drop primes with e==0 mod N (trivial)


def order_of_class(vals, n=N):
    order = 1
    for p, e in vals.items():
        vmod = e % n
        contrib = n // gcd(n, vmod) if vmod != 0 else 1
        order = order * contrib // gcd(order, contrib)
    return order


def r_intersection(a_expr, b_expr, verbose=True):
    """
    a_expr, b_expr: Fraction (or int/str convertible to Fraction). Returns a dict of raw data
    (no interpretation) -- ord(a), ord(b), r, and the explicit subgroup elements used.
    """
    a = Fraction(a_expr)
    b = Fraction(b_expr)
    a_vals_full = prime_valuations(a)
    b_vals_full = prime_valuations(b)
    support = sorted(set(a_vals_full) | set(b_vals_full))

    a_vec = tuple(a_vals_full.get(p, 0) % N for p in support)
    b_vec = tuple(b_vals_full.get(p, 0) % N for p in support)

    ord_a = order_of_class(a_vals_full)
    ord_b = order_of_class(b_vals_full)

    def multiples(vec, order):
        out = []
        for k in range(order):
            out.append(tuple((k * c) % N for c in vec))
        return out

    a_mults = multiples(a_vec, ord_a)
    b_mults = multiples(b_vec, ord_b)
    a_set = set(a_mults)
    b_set = set(b_mults)
    assert len(a_set) == ord_a, f"a subgroup enumeration degenerate: {len(a_set)} != {ord_a}"
    assert len(b_set) == ord_b, f"b subgroup enumeration degenerate: {len(b_set)} != {ord_b}"
    common = a_set & b_set
    r = len(common)

    if verbose:
        print(f"  a={a} b={b}  support={support}")
        print(f"  a_vec={a_vec} ord(a)={ord_a}   b_vec={b_vec} ord(b)={ord_b}")
        print(f"  <a> has {len(a_set)} elements, <b> has {len(b_set)} elements, "
              f"intersection r={r}")

    return {
        "a": str(a), "b": str(b),
        "support_primes": support,
        "a_vector_mod_9": list(a_vec), "b_vector_mod_9": list(b_vec),
        "ord_a": ord_a, "ord_b": ord_b,
        "subgroup_a_elements": [list(v) for v in sorted(a_set)],
        "subgroup_b_elements": [list(v) for v in sorted(b_set)],
        "intersection_elements": [list(v) for v in sorted(common)],
        "r": r,
    }


def build_cert(canary_name, result, expected_r=None):
    rec = {
        "schema": "r-intersection/v1-template",
        "generated_by": {"tool": "python/sympy", "script": "search/r_intersection_template_v1.py",
                          "task": "裁定974【2】r計算器の雛形(値は未差込)"},
        "canary": True,
        "canary_name": canary_name,
        "real_data_used": False,
        "result": result,
    }
    if expected_r is not None:
        rec["expected_r_hand_check"] = expected_r
        rec["agrees_with_hand_check"] = (result["r"] == expected_r)
    return rec


def main():
    certs = []

    print("Canary 1: (a,b) = (3, 5) -- disjoint prime support, expect r=1 (trivial intersection)")
    res1 = r_intersection(3, 5)
    c1 = build_cert("(3,5) disjoint primes", res1, expected_r=1)
    certs.append(c1)
    print("  ->", "PASS" if c1["agrees_with_hand_check"] else "FAIL", "r =", res1["r"], "\n")

    print("Canary 2: (a,b) = (3, 3^2=9) -- both generators of the SAME full Z/9 (gcd(1,9)=gcd(2,9)=1),")
    print("          expect r=9 (full intersection, positive-control per 裁定961: nontrivial max value)")
    res2 = r_intersection(3, 9)
    c2 = build_cert("(3, 3^2) both full generators", res2, expected_r=9)
    certs.append(c2)
    print("  ->", "PASS" if c2["agrees_with_hand_check"] else "FAIL", "r =", res2["r"], "\n")

    print("Canary 3: (a,b) = (3, 2*3^6=1458) -- overlapping prime support (3) but the extra factor")
    print("          of 2 in b forces v_2=0 as the only common point, expect r=1")
    res3 = r_intersection(3, 2 * 3**6)
    c3 = build_cert("(3, 2*3^6) overlapping support, still trivial", res3, expected_r=1)
    certs.append(c3)
    print("  ->", "PASS" if c3["agrees_with_hand_check"] else "FAIL", "r =", res3["r"], "\n")

    print("Canary 4: (a,b) = (3, 3^3=27) -- a generates all of Z/9 on the v_3 axis, b is the order-3")
    print("          subgroup {0,3,6} <= that same Z/9, expect r=3 (proper partial containment)")
    res4 = r_intersection(3, 27)
    c4 = build_cert("(3, 3^3) proper subgroup containment", res4, expected_r=3)
    certs.append(c4)
    print("  ->", "PASS" if c4["agrees_with_hand_check"] else "FAIL", "r =", res4["r"], "\n")

    out = {"schema": "r-intersection/v1-template-canary-batch", "canaries": certs,
           "all_pass": all(c["agrees_with_hand_check"] for c in certs)}
    with open("search/certs/r_intersection_template_canary_20260812.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("wrote search/certs/r_intersection_template_canary_20260812.json  all_pass =", out["all_pass"])
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
