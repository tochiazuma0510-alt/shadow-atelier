# u_meas_caseb_groebner.py -- exact solution of the case-(b) branch system on the fixed curve
#   C : y^2 = f6(x) = (x^3+x)^2 - 27      (a=2, b=1, c=-27 ; e=0 ; theta*thetabar = -27)
#   t  = 3/2 + c3*theta + c5*x^2*theta + c7*x*theta^2 + c9*theta^3 = A(x) + B(x) y
#
# RATIONALISATION (removes delta = tau - 3/2, delta^2 = -27/4):
#   U := A - 3/2 is ODD, B is EVEN  (because t o psibar = 3 - t, psibar : (x,y)->(-x,-y))
#   N_tau = (U - delta)^2 - B^2 f6 = P - 2 delta U,   P := U^2 - B^2 f6 - 27/4   (EVEN, deg <= 8)
#   N_tau1 * N_tau2 = P^2 + 27 U^2                                        (deg 18, EVEN)
#   branch condition  N_tau = kappa g^3  (g monic cubic)  =>  P^2 + 27 U^2 = K * h(x)^3
#   with h monic of degree 6 and EVEN (since the LHS is even and h^3 even => h even over Q),
#   K = 432 c9^2 (leading coefficients).
# Unknowns: c3,c5,c7,c9,h4,h2,h0   (7)      Equations: coefficients of x^16,...,x^0 (9)
#
# No expected values are hard-coded (contact isolation).  Exact rational arithmetic only.

import json, hashlib, sys, time
import sympy as sp

x = sp.symbols('x')
c3, c5, c7, c9, h4, h2, h0 = sp.symbols('c3 c5 c7 c9 h4 h2 h0')

q  = x**3 + x
f6 = sp.expand(q**2 - 27)

U = sp.expand((c3 + c5*x**2)*q + c7*x*(2*q**2 - 27) + c9*(4*q**3 - 81*q))
B = sp.expand(c3 + c5*x**2 + 2*c7*x*q + c9*(4*q**2 - 27))
P = sp.expand(U**2 - B**2*f6 - sp.Rational(27, 4))

print("sympy", sp.__version__)
print("deg U =", sp.degree(U, x), " (odd?)", all(sp.Poly(U, x).all_coeffs()[::-1][i] == 0 for i in range(0, 10, 2)))
print("deg B =", sp.degree(B, x))
print("deg P =", sp.degree(P, x), "  (must be <= 8 for deg N = 9)")

h = x**6 + h4*x**4 + h2*x**2 + h0
LHS = sp.expand(P**2 + 27*U**2)
K = 432*c9**2
E = sp.expand(LHS - K*h**3)
pe = sp.Poly(E, x)
eqs = [sp.expand(co) for co in pe.all_coeffs() if sp.expand(co) != 0]
print("deg LHS =", sp.degree(LHS, x), "  #nonzero coefficient equations =", len(eqs))

t0 = time.time()
sols = sp.solve(eqs, [c3, c5, c7, c9, h4, h2, h0], dict=True)
print("solve took %.1fs ; %d raw solution branches" % (time.time()-t0, len(sols)))

good = []
for s in sols:
    v = {k: sp.nsimplify(s.get(k, k)) for k in (c3, c5, c7, c9, h4, h2, h0)}
    free = [k for k in (c3, c5, c7, c9) if v[k].free_symbols]
    c9v = v[c9]
    if (not c9v.free_symbols) and c9v == 0:
        print("  branch rejected (c9 = 0, pole order < 9):", {str(k): v[k] for k in (c3, c5, c7, c9)})
        continue
    dec = (v[c5] == 0 and v[c7] == 0)
    tag = "DECOMPOSABLE (t = cubic in theta)" if dec else ("FREE PARAMS " + str(free) if free else "CANDIDATE")
    print("  branch:", {str(k): v[k] for k in (c3, c5, c7, c9)}, "->", tag)
    if (not dec) and (not free):
        good.append(v)

print("\n=== non-degenerate exact solutions: %d ===" % len(good))
report = {"schema": "u-meas-caseb-groebner/v1",
          "sympy_version": sp.__version__,
          "curve": "y^2 = (x^3+x)^2 - 27",
          "basis": ["theta", "x^2*theta", "x*theta^2", "theta^3"],
          "system": "P^2 + 27 U^2 = 432 c9^2 h^3, h monic even of degree 6",
          "n_equations": len(eqs),
          "solutions": []}
for v in good:
    d = {str(k): str(v[k]) for k in (c3, c5, c7, c9, h4, h2, h0)}
    dens = set()
    for k in (c3, c5, c7, c9):
        val = sp.nsimplify(v[k])
        for e2 in sp.preorder_traversal(val):
            pass
        rr = sp.Rational(val) if val.is_Rational else None
        if rr is not None and rr.q != 1: dens |= set(sp.factorint(rr.q).keys())
    d["denominator_primes"] = sorted(int(z) for z in dens)
    # residues mod 7,13,19 for cross-check with the mod-p survivors
    res = {}
    for p in (7, 13, 19):
        try:
            res[str(p)] = {str(k): int(sp.Rational(v[k]).p * pow(int(sp.Rational(v[k]).q), p-2, p) % p)
                           for k in (c3, c5, c7, c9)}
        except Exception as ex:
            res[str(p)] = "not rational: %s" % ex
    d["residues"] = res
    report["solutions"].append(d)
    print(" ", d)

with open("search/certs/u_meas_caseb_groebner_20260731.json", "w") as fh:
    json.dump(report, fh, indent=1, sort_keys=True)
print("\nwrote search/certs/u_meas_caseb_groebner_20260731.json")
