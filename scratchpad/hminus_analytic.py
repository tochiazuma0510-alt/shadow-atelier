"""
h^- (relative class number) via analytic class number formula, exact arithmetic.

h^- = Q * w * prod_{chi odd} ( -B_{1,chi} / 2 )

B_{1,chi} = (1/f) * sum_{a=1}^{f} chi(a) * a   (chi = PRIMITIVE character mod f = conductor of chi)

Convention used (Washington, "Introduction to Cyclotomic Fields", Thm 4.17):
  w = number of roots of unity in Q(zeta_n)  ( = n if n even and 4|n gives w=n; more precisely
      w = n if n is even, w = 2n if n is odd -- but since we only ever feed EVEN n (28,20)
      or the odd prime case (23, where Q(zeta_23) has w = 2*23 = 46) we compute w directly
      from n's parity per Washington's remark: w = n * (2 if n odd else 1) is WRONG in general
      (true statement: mu(Q(zeta_n)) has order n if n even, order 2n if n odd, EXCEPT this is
      exactly the definition -- Q(zeta_n) always contains a primitive n-th root; it contains a
      primitive 2n-th root of unity iff n is odd, since zeta_{2n} = -zeta_n^{(n+1)/2} when n odd).
  Q = Hasse unit index, Q=1 unless n is a prime power in which case Q=2. (Washington Thm 4.12 /
      Cor 4.13 convention used here.) 28 = 2^2*7 is NOT a prime power => Q=1 (used below).
      23 is prime => Q=2. 20=2^2*5 not a prime power => Q=1.

All character-value arithmetic is done EXACTLY in the ring Q[x]/Phi_L(x) (L = exponent of the
character group of (Z/nZ)^*, Phi_L = L-th cyclotomic polynomial), i.e. Q(zeta_L), using sympy
Poly over QQ. No floating point / numerical approximation is used anywhere.
"""
import json
import sys
from fractions import Fraction
from itertools import product as iproduct

import sympy
from sympy import symbols, Poly, QQ, cyclotomic_poly, Rational, totient, primitive_root, isprime, factorint

x = symbols('x')


def cyc_ring(L):
    """Return the modulus polynomial Phi_L(x) as a sympy Poly over QQ."""
    return Poly(cyclotomic_poly(L, x), x, domain=QQ)


def poly_reduce(p, modulus):
    q, r = sympy.div(p, modulus, domain=QQ)
    return r


def const_poly(c, modulus):
    return poly_reduce(Poly(Rational(c), x, domain=QQ), modulus)


def mono_poly(exp_, coeff, L, modulus):
    """coeff * x^exp_ reduced mod Phi_L(x), with exp_ taken mod L first (x^L = ... not simply 1,
    but powers of x reduce automatically via poly division; still take exp_ mod L is safe since
    x^L - 1 is a multiple of Phi_L(x))."""
    e = exp_ % L
    p = Poly(Rational(coeff) * x**e, x, domain=QQ)
    return poly_reduce(p, modulus)


def poly_add(p, q, modulus):
    return poly_reduce(p + q, modulus)


def poly_mul(p, q, modulus):
    return poly_reduce(p * q, modulus)


def prime_power_factors(n):
    return [p**e for p, e in factorint(n).items()]


def build_component(q):
    """For prime power q (odd prime power, or 4), return (order, dlog_table) for the cyclic
    group (Z/qZ)^*. q must be an odd prime power or 4 (so that the group is cyclic)."""
    order = totint = int(totient(q))
    if q == 1:
        return 1, {}
    if q == 2:
        return 1, {1: 0}
    g = primitive_root(q)
    dlog = {}
    val = 1
    for i in range(order):
        dlog[val % q] = i
        val = (val * g) % q
    return order, dlog


def analytic_hminus(n, L_override=None, verbose_label=""):
    """Compute h^-(Q(zeta_n)) exactly. Returns dict with all intermediate exact data."""
    factors = prime_power_factors(n)
    # component data: list of (q, order_q, dlog_q)
    comps = []
    for q in factors:
        order_q, dlog_q = build_component(q)
        comps.append((q, order_q, dlog_q))

    L = 1
    for (_, order_q, _) in comps:
        L = sympy.ilcm(L, order_q)
    if L_override is not None:
        assert L_override == L
    modulus = cyc_ring(L)

    def chi_value_poly(ks, a):
        """chi(a) as element of Q[x]/Phi_L(x), chi given by exponent tuple ks (one per comp)."""
        val = const_poly(1, modulus)
        for (q, order_q, dlog_q), k in zip(comps, ks):
            r = a % q
            if r not in dlog_q:  # gcd(a,q) > 1 => character (and hence chi) is 0 at a
                return None
            dl = dlog_q[r]
            if k == 0:
                continue
            e = (k * dl) % order_q
            # embed order_q-th root as L-th root: zeta_L^{ (L/order_q) * e }
            step = L // order_q
            val = poly_mul(val, mono_poly(step * e, 1, L, modulus), modulus)
        return val

    # enumerate all characters
    ranges = [range(order_q) for (_, order_q, _) in comps]
    all_chars = list(iproduct(*ranges)) if ranges else [()]

    neg_one = n - 1  # representative of -1 mod n

    odd_chars = []
    for ks in all_chars:
        if all(k == 0 for k in ks):
            continue  # trivial character excluded (even, and also not part of odd product)
        val_at_neg1 = chi_value_poly(ks, neg_one)
        assert val_at_neg1 is not None
        if val_at_neg1 == const_poly(-1, modulus):
            odd_chars.append(ks)
        elif val_at_neg1 == const_poly(1, modulus):
            pass
        else:
            raise RuntimeError(f"chi(-1) not +-1: {val_at_neg1} for ks={ks}, n={n}")

    # for each odd character, determine conductor = product of q where k_q != 0
    char_records = []
    for ks in odd_chars:
        cond = 1
        for (q, order_q, dlog_q), k in zip(comps, ks):
            if k != 0:
                cond *= q
        # B_{1,chi} = (1/cond) * sum_{a=1}^{cond} chi(a)*a   (chi evaluated via full ks tuple;
        # since components with k_q=0 are trivial characters mod that prime power and don't
        # affect the value as function of a mod cond, this correctly computes the PRIMITIVE
        # character's Bernoulli number as long as cond is indeed the conductor, i.e. no
        # sub-prime-power reduction is possible -- true here since every q in our factorizations
        # is prime or 4, and the unique nontrivial character mod 4 already has conductor 4.)
        acc = const_poly(0, modulus)
        for a in range(1, cond + 1):
            if sympy.gcd(a, cond) != 1:
                continue
            cv = chi_value_poly(ks, a)
            if cv is None:
                continue
            acc = poly_add(acc, mono_poly(0, 0, L, modulus), modulus)  # no-op keep type
            acc = poly_add(acc, poly_mul(cv, const_poly(a, modulus), modulus), modulus)
        # divide by cond
        B1 = poly_reduce(Poly([c / cond for c in acc.all_coeffs()], x, domain=QQ) if acc.all_coeffs() else const_poly(0, modulus), modulus) if False else None
        # simpler: scale coefficients directly
        coeffs = acc.all_coeffs()
        if coeffs:
            scaled = [Rational(c) / cond for c in coeffs]
            B1 = Poly(scaled, x, domain=QQ)
        else:
            B1 = const_poly(0, modulus)
        char_records.append({"ks": ks, "conductor": cond, "B1": B1})

    # product of (-B1/2) over all odd chars
    prod = const_poly(1, modulus)
    for rec in char_records:
        term = poly_mul(const_poly(-1, modulus), rec["B1"], modulus)
        term = Poly([Rational(c) / 2 for c in term.all_coeffs()], x, domain=QQ) if term.all_coeffs() else const_poly(0, modulus)
        prod = poly_mul(prod, term, modulus)

    # prod should reduce to a rational constant
    prod_coeffs = prod.all_coeffs()
    is_const = (prod.degree() <= 0)
    const_val = prod_coeffs[-1] if prod_coeffs else Rational(0)

    return {
        "n": n,
        "L_exponent": L,
        "num_odd_characters": len(odd_chars),
        "char_records": [
            {"ks": rec["ks"], "conductor": rec["conductor"], "B1_poly": str(rec["B1"].as_expr())}
            for rec in char_records
        ],
        "product_poly": str(prod.as_expr()),
        "product_is_rational_constant": is_const,
        "product_value": str(const_val) if is_const else None,
    }


def known_w(n):
    # order of the full group of roots of unity in Q(zeta_n)
    if n % 2 == 0:
        return n
    else:
        return 2 * n


def known_Q(n):
    # Hasse unit index convention (Washington, Thm 4.12 / Cor 4.13): Q=1 iff n is a prime power
    # (including n = p^k, k>=1), Q=2 otherwise (n has >= 2 distinct prime factors).
    f = factorint(n)
    is_prime_power = (len(f) == 1)
    return 1 if is_prime_power else 2


def full_hminus(n):
    data = analytic_hminus(n)
    if not data["product_is_rational_constant"]:
        raise RuntimeError(f"product not rational for n={n}: {data['product_poly']}")
    prod_val = Rational(data["product_value"])
    w = known_w(n)
    Q = known_Q(n)
    hminus = Q * w * prod_val
    data["w"] = w
    data["Q"] = Q
    data["hminus_raw"] = str(Q * w * prod_val)
    data["hminus"] = str(hminus)
    data["hminus_is_integer"] = (hminus.q == 1)
    return data


if __name__ == "__main__":
    results = {}
    for n in [23, 20, 28]:
        print(f"=== n={n} ===")
        d = full_hminus(n)
        print(json.dumps(d, indent=2, default=str))
        results[str(n)] = d

    out = {
        "task": "hminus_zeta28_analytic",
        "sympy_version": sympy.__version__,
        "convention": {
            "formula": "h^- = Q * w * prod_{chi odd} ( -B_{1,chi} / 2 )",
            "B1_definition": "B_{1,chi} = (1/f) sum_{a=1}^{f} chi(a) a, chi primitive mod f=conductor(chi)",
            "w_rule": "w = n if n even, w = 2n if n odd  (order of mu(Q(zeta_n)))",
            "Q_rule": "Q = 1 if n is a prime power, else Q = 2  (Hasse unit index convention, Washington Thm 4.12/Cor 4.13)",
            "arithmetic": "exact, done in Q[x]/Phi_L(x) (L = exponent of (Z/nZ)^*), no floating point",
        },
        "calibration": {
            "n=23": {"expected_hminus": 3, "computed_hminus": results["23"]["hminus"],
                     "match": results["23"]["hminus"] == "3"},
            "n=20": {"expected_hminus": 1, "computed_hminus": results["20"]["hminus"],
                     "match": results["20"]["hminus"] == "1"},
        },
        "results": results,
    }
    with open(sys.argv[1] if len(sys.argv) > 1 else "hminus_out.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("=== calibration ===")
    print(json.dumps(out["calibration"], indent=2))
