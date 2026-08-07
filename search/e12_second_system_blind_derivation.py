#!/usr/bin/env python3
"""
search/e12_second_system_blind_derivation.py -- CR-1 second-system check
(裁定759(5), 司令塔), for docs/notes/cone_design_v1.md's P-CONE-2.

This script derives Brown's e-bar_12 (weight 12, depth 4, 118 terms,
arXiv 1301.3053v2 Definition 8.1/(8.4)(8.5)(8.6)(8.7) + Example 8.4's f_12)
INDEPENDENTLY of the existing first-system reconstruction
(docs/scout/brown_e12_reconstruct.py, embedded in
docs/scout/brown_e12_coefficients_verbatim_v1.md).

*** Provenance / independence protocol (important, read before trusting
this as a genuine second system) ***
This exact script was produced verbatim by a FRESH subagent (no memory of
this project's prior conversation) that was given ONLY the verbatim
primary-source paper text (transcribed from page images by an independent
reader task, itself pinned in the CR-1 note) as its prompt, with an
explicit instruction NOT to read docs/scout/brown_e12_coefficients_verbatim_v1.md,
docs/scout/brown_e12_reconstruct.py, or any file with "e12"/"brown_e12" in
its name. The orchestrating session (search/e12_second_system_v1.py's
author) HAD already read the full CR-1 note (including the first system's
derived 118-term JSON and its anchor table) before dispatching that
subagent -- this is disclosed, not hidden -- but the actual derivation
code below was written and executed by the blind subagent, which never
saw the first system's output. The post-hoc term-by-term comparison
against the first system happens ONLY in search/e12_second_system_v1.py,
after this script had already produced and written its own output.

Method: builds f0,f1 from f_12 per (8.4) (polynomial division, remainder
checked ==0), then computes e_bar_12 TWO independent ways from the
verbatim text -- ROUTE-A: the literal Z/5 cyclic sum (8.5) then reduce
y0=0,y_i=x_i; ROUTE-B: the already-reduced 10-term formula (8.6) -- and
cross-checks they agree exactly (an internal consistency check of the two
paper formulas, not a comparison to any external "known answer"). Also
checks identity (8.7) and the odd-symmetry property of f1 stated in the
paper text. Outputs the full 118-term polynomial as JSON.

No claim of primitivity/gcd is made here (that is search/e12_second_system_v1.py's
job, after the first/second-system term comparison PASSES) -- this script
emits only the raw derived polynomial and internal-consistency booleans.
"""
import sympy as sp
import json

x, y = sp.symbols('x y')
x1,x2,x3,x4 = sp.symbols('x1 x2 x3 x4')

# Step 1: define f12(x,y)
def bracket(a,b):
    return x**a*y**b - x**b*y**a

f12 = (bracket(8,2)) - 3*(bracket(6,4))
f12 = sp.expand(f12)

# factor out x*y*(x-y)
divisor = sp.expand(x*y*(x-y))
q, r = sp.div(sp.Poly(f12, x, y), sp.Poly(divisor, x, y))
remainder = sp.expand(r.as_expr())

f0 = sp.expand(q.as_expr())

f1 = sp.expand((x-y)*f0)

remainder_check = remainder

# Step 2: verify f1(-x,y) = f1(x,-y) = -f1(x,y)
f1_negx = sp.expand(f1.subs({x:-x, y:y}, simultaneous=True))
f1_negy = sp.expand(f1.subs({x:x, y:-y}, simultaneous=True))
neg_f1 = sp.expand(-f1)

check_negx = sp.simplify(f1_negx - neg_f1) == 0
check_negy = sp.simplify(f1_negy - neg_f1) == 0
f1_odd_identity_holds = bool(check_negx and check_negy)

# helper functions f0(a,b), f1(a,b) evaluated symbolically
def F0(a,b):
    return f0.subs({x:a, y:b}, simultaneous=True)

def F1(a,b):
    return f1.subs({x:a, y:b}, simultaneous=True)

# Step 3: ROUTE-A: literal cyclic sum in (8.5)
y0,y1,y2,y3,y4 = sp.symbols('y0 y1 y2 y3 y4')
Y = [y0,y1,y2,y3,y4]

def cyclic_shift(Y, j):
    # tau(y0,y1,y2,y3,y4) = (y1,y2,y3,y4,y0)
    # tau^j
    n = len(Y)
    return [Y[(i+j) % n] for i in range(n)]

e_f_terms = []
for j in range(5):
    Yp = cyclic_shift(Y, j)
    y0p,y1p,y2p,y3p,y4p = Yp
    term = F1(y4p - y3p, y2p - y1p) + (y0p - y1p)*F0(y2p - y3p, y4p - y3p)
    e_f_terms.append(term)

e_f = sp.expand(sum(e_f_terms))

# reduce: y0=0, y1..y4 = x1..x4
ebar_A = sp.expand(e_f.subs({y0:0, y1:x1, y2:x2, y3:x3, y4:x4}, simultaneous=True))

# Step 4: ROUTE-B: formula (8.6) directly
term1 = F1(x4-x3, x2-x1)
term2 = F1(-x4, x3-x2)
term3 = F1(x1, x4-x3)
term4 = F1(x2-x1, -x4)
term5 = F1(x3-x2, x1)
term6 = -x1*F0(x2-x3, x4-x3)
term7 = (x1-x2)*F0(x3-x4, -x4)
term8 = (x2-x3)*F0(x4, x1)
term9 = (x3-x4)*F0(-x1, x2-x1)
term10 = x4*F0(x1-x2, x3-x2)

ebar_B = sp.expand(term1+term2+term3+term4+term5+term6+term7+term8+term9+term10)

# Step 5: compare
diff_AB = sp.expand(ebar_A - ebar_B)
route_a_route_b_match = (diff_AB == 0)

# Step 6: verify (8.7)
ebar = ebar_A  # use route A (should match B)
lhs_87 = sp.expand(ebar.subs({x3:0, x4:0}, simultaneous=True))
rhs_87a = sp.expand(F1(x1,x2))
rhs_87b = sp.expand(F1(-x2, x1))
eq_8_7_holds = bool(sp.expand(lhs_87 - rhs_87a) == 0 and sp.expand(lhs_87 - rhs_87b) == 0)

# Step 7: collect terms
poly = sp.Poly(ebar, x1, x2, x3, x4)
terms_dict = poly.as_dict()  # {(a1,a2,a3,a4): coeff}

nonzero_terms = [(list(monom), int(coeff)) for monom, coeff in terms_dict.items() if coeff != 0]

# sort by descending lex order on (a1,a2,a3,a4)
nonzero_terms.sort(key=lambda t: tuple(t[0]), reverse=True)

n_terms = len(nonzero_terms)

def get_coeff(a1,a2,a3,a4):
    key = (a1,a2,a3,a4)
    if key in terms_dict:
        return int(terms_dict[key])
    else:
        return 0

coeff_x3_7_x4 = get_coeff(0,0,7,1)
coeff_x1_3_x2_2_x3_2_x4 = get_coeff(3,2,2,1)
coeff_x1_2_x2_5_x4 = get_coeff(2,5,0,1)

result = {
    "element": "e12_bar",
    "vars": ["x1","x2","x3","x4"],
    "term_format": "[[a1,a2,a3,a4],coeff] = coeff*x1^a1*x2^a2*x3^a3*x4^a4",
    "route_a_route_b_match": route_a_route_b_match,
    "n_terms": n_terms,
    "anchor_check": {
        "coeff_x3^7_x4": coeff_x3_7_x4,
        "coeff_x1^3_x2^2_x3^2_x4": coeff_x1_3_x2_2_x3_2_x4,
        "coeff_x1^2_x2^5_x4": coeff_x1_2_x2_5_x4,
        "eq_8_7_holds": eq_8_7_holds,
        "f1_odd_identity_holds": f1_odd_identity_holds
    },
    "terms": [[m, c] for m,c in nonzero_terms]
}

with open("search/certs/e12_blind_derivation_raw_20260807.json", "w") as fp:
    json.dump(result, fp, indent=1)

print("f12 =", f12)
print("divisor =", divisor)
print("remainder (should be 0) =", remainder_check)
print("f0 =", f0)
print("f1 =", f1)
print("f1_odd_identity_holds:", f1_odd_identity_holds)
print("route_a_route_b_match:", route_a_route_b_match)
print("diff_AB:", diff_AB)
print("eq_8_7_holds:", eq_8_7_holds)
print("lhs_87:", lhs_87)
print("rhs_87a:", rhs_87a)
print("rhs_87b:", rhs_87b)
print("n_terms:", n_terms)
print("coeff_x3^7_x4:", coeff_x3_7_x4, "(expect 1)")
print("coeff_x1^3_x2^2_x3^2_x4:", coeff_x1_3_x2_2_x3_2_x4, "(expect -116)")
print("coeff_x1^2_x2^5_x4:", coeff_x1_2_x2_5_x4, "(expect -57)")
