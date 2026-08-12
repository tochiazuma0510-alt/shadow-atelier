#!/usr/bin/env python3
"""
Independent (crosscheck-side) recomputation of disc_w(R1) for the [P1]/Tier2 branch_I check.
Reuses ONLY my own committed script's math (search/r13_p1_tier2_gha.py @ commit 959a1ac9,
inlined below as build_P_and_gamma(), independently re-typed rather than imported) to
reconstruct discR1(a,b) -- this is NOT a re-use of Sol's script; only Sol's OUTPUT cert (the factorization JSON) is read
below, as machine data, per search/crosscheck separation.

Goal (裁定1017補記 items 2): degree agreement + rational-point value agreement between
  - my discR1(a,b) (bivariate, from my own v2 GHA script's exact computation), and
  - Sol's branch_I factorization (ci/sol_tier2_artifacts_31584810985/.../r13_p1_tier2_math_checkpoint.json),
    which is expressed as a product of factors in a single normalized variable (presumed r=b/a).

Method: homogenize/dehomogenize -- if discR1(a,b) is homogeneous of degree D in (a,b), then
discR1(a,b) = a^D * f(r) with r=b/a. Compare degree(f) to Sol's reported total degree (196,
=28*1+56*1+56*2 from the factor list), and compare f(r) to Sol's reconstructed g(r) = product of
factors (each raised to its exponent) at several rational r-values, up to a possible overall
nonzero scalar (checked by verifying the ratio f(r)/g(r) is the SAME constant across multiple
independent points -- not just equal at one point).
"""
import json
import sys
from pathlib import Path

import sympy as sp

def build_P_and_gamma():
    """Reconstruct P(w;a,b) and gamma(a,b) (the step1 curve, c9(a,b)-2=0). Inlined here
    (not imported from search/r13_p1_tier2_gha.py) so this crosscheck script is self-contained,
    per search/crosscheck separation -- the derivation itself is elementary algebra (defining
    P as the resultant-elimination target of (w-a)(w-b)*gpoly^2 matching w^9..w^17 coefficients
    to 0), independently re-typed here rather than imported."""
    w = sp.symbols("w")
    a, b = sp.symbols("a b")
    gsyms = sp.symbols("g0 g1 g2 g3 g4 g5 g6 g7")

    gpoly = w ** 8 + sum(gsyms[i] * w ** i for i in range(8))
    target = sp.expand((w - a) * (w - b) * gpoly ** 2)
    target_poly = sp.Poly(target, w)
    coeffs = target_poly.all_coeffs()

    order = [gsyms[7], gsyms[6], gsyms[5], gsyms[4], gsyms[3], gsyms[2], gsyms[1], gsyms[0]]
    subs = {}
    for i in range(8):
        idx = 18 - (17 - i)
        eq = coeffs[idx].subs(subs)
        var = order[i]
        sol = sp.solve(sp.Eq(eq, 0), var)
        subs[var] = sp.simplify(sol[0])

    target_sub = sp.expand(target_poly.as_expr().subs(subs))
    target_sub_poly = sp.Poly(target_sub, w)
    tcoeffs = target_sub_poly.all_coeffs()

    c = {}
    for j in range(0, 10):
        idx = 18 - j
        c[j] = sp.simplify(tcoeffs[idx])

    gamma = sp.expand(c[9] - 2)
    P_generic = sum(c[j] * w ** j for j in range(0, 10))
    return w, a, b, P_generic, gamma, c



SOL_CHECKPOINT = Path("ci/sol_tier2_artifacts_31584810985/w9-p1-tier2-v2-31584810985/"
                       "r13_p1_tier2_math_checkpoint.json")

print("== step 1: rebuild P(w;a,b), gamma(a,b) via MY OWN committed script (959a1ac9) ==")
w, a, b, P_generic, gamma, c = build_P_and_gamma()

P_on_curve = sum(c[j] * w**j for j in range(0, 9)) + 2 * w**9
R1 = sp.expand(P_on_curve - 2 * w**9)
deg_w_R1 = sp.degree(R1, w) if R1 != 0 else 0
print(f"deg_w(R1) = {deg_w_R1} (expect <=8, matches my run's R1_degree_w=8)")

print("== step 2: disc_w(R1) (bivariate in a,b) -- this is my run's exact computation ==")
discR1 = sp.expand(sp.discriminant(sp.Poly(R1, w)))
num_terms = len(sp.Add.make_args(discR1))
print(f"discR1 term_count = {num_terms} (my cert recorded discR1_num_terms=197)")

print("== step 3: homogeneity check + degree ==")
discR1_poly = sp.Poly(discR1, a, b)
degs = set()
is_homog = True
for monom, coeff in discR1_poly.terms():
    degs.add(sum(monom))
print(f"total-degree set of discR1 monomials (a,b): {sorted(degs)}")
if len(degs) == 1:
    D = degs.pop()
    print(f"discR1 IS homogeneous, total degree D = {D}")
else:
    D = max(degs)
    is_homog = False
    print(f"discR1 is NOT homogeneous (degree spread {sorted(degs)}) -- will use max degree D={D} "
          f"for a-power normalization, results may show a residual a-dependence")

r = sp.symbols("r")
f_num = sp.expand(discR1.subs({b: r * a}))
# factor out a^D (should divide out cleanly if homogeneous)
f_r = sp.simplify(f_num / a**D)
f_r_poly = sp.Poly(sp.expand(f_r), r) if f_r.free_symbols <= {r} else None
if f_r_poly is not None:
    print(f"f(r) = discR1(a,b)/a^D at b=r*a: degree_r = {f_r_poly.degree()}")
else:
    print(f"WARNING: f(r) still has free symbols other than r: {sp.expand(f_r).free_symbols}")

print()
print("== step 4: load Sol's branch_I factorization (OUTPUT DATA ONLY, not Sol's code) ==")
sol = json.loads(SOL_CHECKPOINT.read_text(encoding="utf-8"))
branchI = sol["branch_I"]
print(f"Sol branch_I degree = {branchI['degree']}, term_count = {branchI['term_count']}")

g_r = sp.Integer(1)
total_deg_check = 0
for fac in branchI["factors"]:
    coeffs_hi_lo = fac["primitive_integer_coefficients_high_to_low"]
    deg = fac["degree"]
    exponent = fac["exponent"]
    total_deg_check += deg * exponent
    poly_expr = sum(sp.Integer(coeffs_hi_lo[i]) * r**(deg - i) for i in range(len(coeffs_hi_lo)))
    g_r = sp.expand(g_r * poly_expr**exponent)
print(f"reconstructed g(r) from Sol's factors: degree_r = {sp.degree(g_r, r)}, "
      f"expected total (sum deg*exp) = {total_deg_check}")

print()
print("== step 5: degree agreement ==")
my_deg = f_r_poly.degree() if f_r_poly is not None else None
print(f"my f(r) degree = {my_deg}, Sol g(r) degree = {sp.degree(g_r, r)}, "
      f"MATCH = {my_deg == sp.degree(g_r, r)}")

print()
print("== step 6: rational-point value agreement (ratio constancy check) ==")
test_points = [sp.Rational(3, 2), sp.Rational(7, 5), sp.Rational(11, 4), sp.Rational(-2, 3)]
ratios = []
for rv in test_points:
    fv = sp.Rational(f_r_poly.eval(rv)) if f_r_poly is not None else sp.Rational(sp.expand(f_r).subs(r, rv))
    gv = sp.Rational(g_r.subs(r, rv))
    ratio = sp.Rational(fv, gv) if gv != 0 else None
    ratios.append(ratio)
    print(f"  r={rv}: f(r) has {len(str(fv))} digits, g(r) has {len(str(gv))} digits, exact ratio f/g={ratio}")

ratio_set = set(ratios)
print(f"\nratio SET across all test points: {ratio_set}")
print(f"ratio CONSTANT across all points (same nonzero scalar) = {len(ratio_set) == 1 and None not in ratio_set}")

result = {
    "schema": "crosscheck/tier2_branchI_discR1/v1",
    "d_no_interpretation": "machine values only; verdict は司令塔",
    "my_side": {
        "source": "search/r13_p1_tier2_gha.py @ 959a1ac9 (own committed script, re-executed locally)",
        "deg_w_R1": int(deg_w_R1),
        "discR1_term_count": int(num_terms),
        "discR1_homogeneous_in_ab": bool(is_homog),
        "discR1_total_degree_ab": int(D),
        "f_r_degree": int(my_deg),
    },
    "sol_side": {
        "source": str(SOL_CHECKPOINT),
        "branch_I_degree_reported": int(branchI["degree"]),
        "branch_I_term_count_reported": int(branchI["term_count"]),
        "g_r_reconstructed_degree": int(sp.degree(g_r, r)),
    },
    "degree_match": bool(my_deg == sp.degree(g_r, r)),
    "test_points": [str(x) for x in test_points],
    "ratios_f_over_g": [str(x) for x in ratios],
    "ratio_constant_across_points": bool(len(ratio_set) == 1 and None not in ratio_set),
    "ratio_value_if_constant": str(next(iter(ratio_set))) if len(ratio_set) == 1 else None,
}
out_path = Path("scratchpad/crosscheck_tier2/independent_discR1_crosscheck_result.json")
out_path.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"\nwrote {out_path}")
