# u_meas_uloc_fire.py -- 裁定 268 : (1) schema-v2 gate, (2) preregistration freeze, (3) U-LOC fire.
# Exact model (CB-30, addendum 6):
#   C : y^2 = f6 = q^2 + c ,  q = x^3 - x/5 ,  c = -512/421875 ,  Pbar = infty_+
#   t = 3/2 + c3*theta + c5*x^2*theta + c7*x*theta^2 + c9*theta^3 ,  theta = y + q
#   c3=3^4*5^3*19/2^9, c5=3^6*5^5/2^9, c7=3^7*5^7/2^10, c9=3^6*5^9/2^11
# The script writes the preregistration block to the cert and FLUSHES it BEFORE computing u.
import json, sys, math
from itertools import product
import sympy as sp

LOG = open(sys.argv[1], "w")
def log(s):
    print(s); LOG.write(str(s)+"\n"); LOG.flush()
CERT = "search/certs/u_meas_uloc_20260731.json"
rep = {"schema": "u-meas-uloc/v1", "sympy_version": sp.__version__,
       "authorisation": "coordinator ruling 268 (conditional)", "u_touched": False,
       "uniqueness_claimed": False}
def save(): json.dump(rep, open(CERT, "w"), indent=1, sort_keys=True)

x, y = sp.symbols('x y')
c = sp.Rational(-512, 421875); q = x**3 - x/5; f6 = sp.expand(q**2 + c)
c3 = sp.Rational(3**4*5**3*19, 2**9); c5 = sp.Rational(3**6*5**5, 2**9)
c7 = sp.Rational(3**7*5**7, 2**10); c9 = sp.Rational(3**6*5**9, 2**11)
U = sp.expand((c3 + c5*x**2)*q + c7*x*(2*q**2 + c) + c9*(4*q**3 + 3*c*q))
B = sp.expand(c3 + c5*x**2 + 2*c7*x*q + c9*(4*q**2 + c))
A = sp.expand(U + sp.Rational(3, 2))
rep["model"] = {"curve": "y^2 = (x^3 - x/5)^2 - 512/421875", "c": str(c),
                "c3": str(c3), "c5": str(c5), "c7": str(c7), "c9": str(c9),
                "A_of_x": str(sp.factor(A)), "B_of_x": str(sp.factor(B))}

# ---------------- (1) schema-v2 gate ----------------
log("=== GATE 1 : schema-v2 on the EXACT model ===")
gate = {}
d3 = sp.sqrt(-3); tau1 = sp.Rational(3, 2) + sp.Rational(3, 2)*d3; tau2 = sp.Rational(3, 2) - sp.Rational(3, 2)*d3
N1 = sp.expand(sp.expand((A - tau1)**2) - sp.expand(B**2*f6))
N2 = sp.expand(sp.expand((A - tau2)**2) - sp.expand(B**2*f6))
gate["deg_N_tau1"] = int(sp.degree(N1, x)); gate["deg_N_tau2"] = int(sp.degree(N2, x))
log("deg N_tau1 = %s ; deg N_tau2 = %s   (both must be 9)" % (gate["deg_N_tau1"], gate["deg_N_tau2"]))
for nm, NN in (("N_tau1", N1), ("N_tau2", N2)):
    fa = sp.factor_list(sp.Poly(NN, x).as_expr(), extension=[d3])
    mults = sorted([m for _, m in fa[1]], reverse=True)
    gate[nm + "_factor_multiplicities"] = mults
    log("  %s factor multiplicities = %s  (must be [3,3,3] or [3] of a cubic)" % (nm, mults))
gate["f6_squarefree"] = bool(sp.gcd(sp.Poly(f6, x), sp.Poly(sp.diff(f6, x), x)).degree() == 0)
gate["deg_f6"] = int(sp.degree(f6, x))
log("f6 squarefree = %s ; deg f6 = %s (genus 2 needs 6 and squarefree)" % (gate["f6_squarefree"], gate["deg_f6"]))

ALLOWED = {(1,)*9, (2,2,2,2,1), (3,3,3), (7,1,1), (9,), (3,3,1,1,1), (6,2,1)}
PSLTYPES = {(1,)*9, (2,2,2,2,1), (3,3,3), (7,1,1), (9,)}
seen = {}; bad = []
for p in (11, 17, 23, 29, 31, 37, 41, 43):
    try:
        Ap = sp.Poly(A, x, modulus=p); Bp = sp.Poly(B, x, modulus=p); Fp = sp.Poly(f6, x, modulus=p)
    except Exception as ex:
        continue
    if Fp.degree() != 6 or sp.gcd(Fp, Fp.diff(x)).degree() != 0: continue
    for t0 in range(p):
        NN = sp.Poly((Ap - t0)**2 - Bp**2*Fp, x, modulus=p)
        if NN.degree() != 9: continue
        if sp.gcd(NN, NN.diff(x)).degree() != 0: continue
        pat = tuple(sorted([f.degree() for f, m in sp.factor_list(NN)[1] for _ in range(m)], reverse=True))
        seen[pat] = seen.get(pat, 0) + 1
        if pat not in ALLOWED: bad.append((p, t0, pat))
gate["frobenius_patterns"] = {str(list(k)): v for k, v in sorted(seen.items())}
gate["patterns_outside_PGammaL"] = [[p, t, list(pt)] for p, t, pt in bad[:10]]
gate["saw_7_cycle"] = any(k == (7, 1, 1) for k in seen)
log("Frobenius patterns over p=11..43: %s" % gate["frobenius_patterns"])
log("outside PGammaL(2,8): %s" % (gate["patterns_outside_PGammaL"] or "none"))
log("saw a 7-cycle type (7,1,1) -> transitive+7-cycle on 9 pts is 2-transitive (Jordan) => PRIMITIVE, non-decomposable: %s" % gate["saw_7_cycle"])
gate["PASS"] = bool(gate["deg_N_tau1"] == 9 and gate["deg_N_tau2"] == 9 and not bad
                    and gate["f6_squarefree"] and gate["deg_f6"] == 6 and gate["saw_7_cycle"])
rep["gate_schema_v2"] = gate; save()
log("GATE 1 PASS = %s" % gate["PASS"])
if not gate["PASS"]:
    rep["status"] = "gate_failed_no_fire"; save(); log("FAIL-CLOSED: not firing U-LOC"); LOG.close(); sys.exit(1)

# ---------------- (2) preregistration, FROZEN BEFORE any u computation ----------------
rep["preregistration"] = {
 "frozen_before_measurement": True,
 "a_quantity_measured": {
   "object": "u_0 = leading coefficient of lambda at P_0 in Prop U-LOC (u_meas_m3_design_v1.md 1.2)",
   "cusp": "P_0 in W over lambda=0 with e=9; its image Pbar = infty_+ on C (the unique pole of t, ord=9)",
   "local_parameter": "s := 1/x on C at infty_+ (Q-rational; W->C is unramified at P_0 so s is a parameter on W too)",
   "extraction_rule": "expand t = c_lead * s^-9 * (1+O(s)) at Pbar; then u_0 = -c_lead^{-1}, [u_0^{-1}]_9 = [c_lead]_9",
   "normalisation_bindings": ["integral model: y^2 = (x^3-x/5)^2-512/421875 as written (NOT minimalised)",
     "cusp section: Pbar = infty_+ = the branch of y with y/x^3 -> +1",
     "tame normalisation: s = 1/x exactly (no reparametrisation); any other s changes u by a 9th power (Lemma SL-2)",
     "Sol F91-5.4 note: good reduction does NOT make u a unit; valuations are reported for every prime in the support, no unit claim is made"],
   "sign_convention": "tau_1 = 3/2 + (3/2)sqrt(-3); the S3 involution sends t -> 3-t and swaps tau_1,tau_2"},
 "b_recorded_quantities": ["u_0 exact", "u_0^{-1} exact", "prime factorisation of numerator and denominator",
   "v_p(u_0) for every p in the support", "squarefree part of u_0^{-1} (the [u]_2 class)",
   "exponent vector of u_0^{-1} modulo 9 (the [u]_9 class datum)", "K = Q(zeta_9) is NOT used to reduce further here"],
 "c_C1prime": {"claim": "the u_0 measured here is the u of the S4-window bridge (intrinsic u of Thm SURJ-S4)",
   "status": "NOT PROVED HERE - separate line",
   "note": "measurement and theorem are kept apart (Sol F91-5.3). The identification requires: (i) Prop U-LOC's derivation chain W -> C -> P^1_t, (ii) the window binding of u-meas-cert schema (dessin class vector = diagonal), (iii) the bridge B_FC. Audit target for the mathematician / Sol."},
 "d_no_interpretation": "this cert records machine values only; no verdict on ord([u^{-1}]_9), surjectivity, or comparison with any prediction"}
rep["status"] = "preregistration_frozen"; save()
log("\n=== PREREGISTRATION FROZEN AND WRITTEN TO CERT (before any u computation) ===")

# ---------------- (3) FIRE ----------------
log("\n=== U-LOC FIRED ===")
s = sp.symbols('s', positive=True)
# at infty_+ : x = 1/s, y = +sqrt(f6) with y/x^3 -> +1
xs = 1/s
ys = sp.sqrt(sp.together(f6.subs(x, xs)))
th = sp.simplify(ys + q.subs(x, xs))
tt = sp.Rational(3, 2) + c3*th + c5*xs**2*th + c7*xs*th**2 + c9*th**3
lead = sp.limit(sp.simplify(tt*s**9), s, 0)
lead = sp.nsimplify(sp.simplify(lead))
log("c_lead = lim_{s->0} t*s^9 = %s = %s" % (lead, sp.factorint(sp.Rational(lead)) if lead.is_Rational else "non-rational"))
u0 = sp.nsimplify(-1/lead); u0i = sp.nsimplify(1/u0)
log("u_0 = %s" % u0); log("u_0^{-1} = %s" % u0i)
def fac(r):
    r = sp.Rational(r); d = {}
    for k_, v_ in sp.factorint(abs(r.p)).items(): d[str(k_)] = int(v_)
    for k_, v_ in sp.factorint(r.q).items(): d[str(k_)] = -int(v_)
    return d, (-1 if r < 0 else 1)
fu, su = fac(u0i)
sqfree = su
for pr, e in fu.items():
    if e % 2: sqfree *= int(pr)
rep["measurement"] = {
  "c_lead": str(lead), "c_lead_check_8c9": str(sp.simplify(lead - 8*c9)),
  "u_0": str(u0), "u_0_inverse": str(u0i),
  "u_0_inverse_sign": int(su),
  "u_0_inverse_valuations": fu,
  "u_0_valuations": {k_: -v_ for k_, v_ in fu.items()},
  "squarefree_part_of_u_0_inverse": int(sqfree),
  "exponent_vector_mod_9_of_u_0_inverse": {k_: int(v_ % 9) for k_, v_ in fu.items()},
  "sign_is_ninth_power": True,
  "note": "machine values only, no interpretation"}
rep["u_touched"] = True; rep["status"] = "measured"; save()
log("valuations of u_0^{-1}: %s ; sign %s ; squarefree part %s" % (fu, su, sqfree))
log("exponent vector mod 9: %s" % rep["measurement"]["exponent_vector_mod_9_of_u_0_inverse"])
log("cert: %s" % CERT)
LOG.close()
