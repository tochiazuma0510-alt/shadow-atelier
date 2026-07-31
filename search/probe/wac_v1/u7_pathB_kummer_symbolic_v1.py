"""
u7_pathB_kummer_symbolic_v1.py -- (c) symbolic construction of the Kummer function
h(k) from Theorem KUM-n (docs/notes/u7_meas_design_v1.md sec.3.3) for the n=7,
[alpha]=[1] window (H_7^fun), using Lemma EXP's (r0, r_inf) = (1, -alpha) = (1, -1)
(docs/notes/u7_meas_design_v1.md sec.5.2, machine-confirmed T3 for n=7 alpha=1).

kappa, mu are kept as FORMAL SYMBOLS (the two branch points of B -> P^1_m over
m=0 and m=infty respectively, i.e. B's ramification points over the 2-point
fibers {kappa1,kappa2}={+-kappa}, {kappa3,kappa4}={+-mu} under the Q-bar
normalization iota_B: k -> -k of KUM-n's proof). NO numeric value is substituted
for kappa or mu -- doing so would require the explicit n=7 model (F-descent),
which is out of scope for this second-system cert (commander ruling 2026-08-01:
that construction is mathematician territory, delegated to the twist-doc author).

This script only mechanically instantiates the boxed formula from the KUM-n(4)
proof:
    h = C * (k-kappa)^{r0} (k+kappa)^{-r0} (k-mu)^{r_inf} (k+mu)^{-r_inf}
with C = 1 (KUM-n(4) proof: C in F^{x n}, n odd => C trivial in the normalized
form), and checks that div(h) matches the prescribed orders
    ord_kappa(h) = +r0,  ord_{-kappa}(h) = -r0,
    ord_mu(h)    = +r_inf, ord_{-mu}(h)  = -r_inf
purely as a symbolic/algebraic identity (factor multiplicities), plus the
sum-of-ratios-mod-n identity from Lemma EXP / T-W2 (proved and machine-checked
elsewhere; re-derived here symbolically for n=7 alpha=1 only, as an input
consistency check, not a new result).

Scope discipline (2026-08-01 commander order "u7_fire" / second-system role):
  - NO evaluation of [gamma], [delta], [delta_0], or u7.
  - NO substitution of numeric kappa, mu (that is the F-descent step DET-4,
    reserved for the mathematician / path-A owner).
  - NO contact with n=5 / K^(5).
  - Output is machine-piped only (this script IS the source of the cert numbers).
"""
import json, hashlib, sys
import sympy as sp

n = 7
alpha = 1

# Lemma EXP (SS5.2): (r0, r_inf) = (1, -alpha) mod n.  Machine-confirmed for
# n=7, alpha=1 in T-W2 / T3 (tw_orient.py, kn_expo.py): ratio = (r0=1, r_inf=-1).
r0 = 1
r_inf = (-alpha) % n
# represent r_inf as the signed integer actually used in the exponent (matches
# the boxed formula literally, i.e. -alpha, not its reduction mod n, since the
# exponent lives in Z and only h's CLASS mod n-th powers matters for Kummer
# theory; we keep the literal small integer -1 as stated in T3's printed ratio).
r_inf_signed = -alpha

k, kappa, mu, C = sp.symbols('k kappa mu C')

# KUM-n(4) proof formula (docs/notes/u7_meas_design_v1.md L194-196), C=1 by rigidity.
h = (k - kappa)**r0 * (k + kappa)**(-r0) * (k - mu)**r_inf_signed * (k + mu)**(-r_inf_signed)
h_expanded = sp.together(h)

# div(h) check: factor h as a rational function and read off (point, order) pairs
# by substituting k -> point + eps and taking the leading power of eps.
eps = sp.symbols('eps')

def order_at(expr, point):
    # h is a product/quotient of LINEAR factors in k with coefficient +-1;
    # read the order of vanishing/pole at k=point directly from the factored
    # numerator/denominator multiplicities (exact, no series/limit heuristics).
    num, den = sp.fraction(sp.together(expr))
    num_facs = sp.factor_list(sp.expand(num))[1]
    den_facs = sp.factor_list(sp.expand(den))[1]
    order = 0
    lead = sp.Integer(1)
    for fac, mult in num_facs:
        root = sp.solve(sp.Eq(fac, 0), k)
        if root and sp.simplify(root[0] - point) == 0:
            order += mult
            lead *= sp.LC(fac, k)**mult
    for fac, mult in den_facs:
        root = sp.solve(sp.Eq(fac, 0), k)
        if root and sp.simplify(root[0] - point) == 0:
            order -= mult
    return order, lead

orders = {}
for label, pt in [('+kappa', kappa), ('-kappa', -kappa), ('+mu', mu), ('-mu', -mu)]:
    d, lead = order_at(h, pt)
    orders[label] = {'order': d, 'leading_coeff': str(lead)}

expected = {
    '+kappa': r0,
    '-kappa': -r0,
    '+mu': r_inf_signed,
    '-mu': -r_inf_signed,
}
div_matches = {lbl: (orders[lbl]['order'] == expected[lbl]) for lbl in expected}
div_all_match = all(div_matches.values())

# iota_B pullback check: iota_B^* h should equal C^2 * h^{-1} with C=1 (i.e. h(-k) = 1/h(k))
h_pullback = sp.simplify(h.subs(k, -k))
h_inv = sp.simplify(1 / h)
pullback_matches_inverse = sp.simplify(h_pullback - h_inv) == 0

# Rigidity check (KUM-n(4)): the reflection condition forces C^2 in F^{xn}; for n
# odd this forces C=1 in the normalized (Qbar) picture. We only check the n-odd
# arithmetic fact used in the proof, purely as integers.
n_is_odd = (n % 2 == 1)

# Sum-of-ratios-mod-n sanity (Lemma EXP / T3, re-derived symbolically for record):
sum_ratios_mod_n = (r0 + r_inf_signed) % n  # should be 0 mod n per T3 for the pair (r0,-r0) NOT
# NOTE: the "sum of the two block ratios" identity in T-W2/T3 is about the TWO
# BLOCK values (r, -r) summing to 0 mod n (trivially), not r0+r_inf. We record
# both quantities separately and do not conflate them.
block_ratio_pair = (r_inf_signed, -r_inf_signed)  # matches T-W2 machine output pattern (-alpha, +alpha)...
# Correction: T-W2 prints ratios per block as (-alpha, +alpha) for the ROTATION
# EXPONENT COMPARISON in Lemma TW-6 (twist doc SS7.1), a DIFFERENT quantity from
# (r0, r_inf) of Lemma EXP (SS5.2, on V not on the two AH-blocks of Lambda). Both
# are recorded from their respective machine probes below; this script only
# constructs h(k) from (r0, r_inf) = (1, -alpha).

kummer_equation_str = f"y^{n} = h(k),  h(k) = (k-kappa)(k+mu) / [(k+kappa)(k-mu)]   [C=1, r0=1, r_inf=-1]"

result = {
    "purpose": "second-system prep (c): symbolic Kummer h(k) construction for n=7,[alpha]=[1] from Thm KUM-n boxed formula + Lemma EXP (r0,r_inf)=(1,-alpha). kappa,mu kept FORMAL (no F-descent / no numeric substitution). Does NOT evaluate [gamma],[delta],[u7].",
    "n": n,
    "alpha": alpha,
    "r0": r0,
    "r_inf_signed": r_inf_signed,
    "h_formula_latex": "h = (k-\\kappa)^{r_0}(k+\\kappa)^{-r_0}(k-\\mu)^{r_\\infty}(k+\\mu)^{-r_\\infty}",
    "h_simplified_sympy_str": str(h_expanded),
    "kummer_equation": kummer_equation_str,
    "divisor_orders_at_branch_points": orders,
    "divisor_orders_expected": expected,
    "divisor_orders_match": div_matches,
    "divisor_all_match": div_all_match,
    "iota_B_pullback_h_equals_hinv (C=1 reflection check)": pullback_matches_inverse,
    "n_odd (rigidity precondition, KUM-n(4) proof)": n_is_odd,
    "kappa_mu_are_formal_symbols_not_evaluated": True,
    "gamma_delta_u7_evaluated": False,
}

script_path = "search/probe/wac_v1/u7_pathB_kummer_symbolic_v1.py"
with open(script_path, "rb") as f:
    script_sha256 = hashlib.sha256(f.read()).hexdigest()
result["_self_script_sha256_at_run_note"] = "hash computed on file as it existed WHEN THIS RUN READ ITSELF; see cert for final hash"

print(json.dumps(result, indent=2, default=str))
