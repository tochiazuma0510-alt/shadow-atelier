# u_meas_uloc_fire2.py -- minimal repair of the schema-v2 gate, then preregistration + U-LOC fire.
# Repairs (coordinator ruling, after the v1 gate stalled on high-level sympy APIs):
#   (a) cube test via gcd(N, N') degree  (the method that already worked)
#   (b) Frobenius patterns via the workshop's own F_p implementation (u_meas_caseb_sieve.py style)
# Lesson recorded: do not swap a verified in-house implementation for a high-level API.
import json, sys, os, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'u_meas_caseb_search2.py')).read().split('if __name__')[0])

LOG = open(sys.argv[1], "w")
def log(s):
    print(s); LOG.write(str(s)+"\n"); LOG.flush()
CERT = "search/certs/u_meas_uloc_v2_20260731.json"
rep = {"schema": "u-meas-uloc/v2", "sympy_version": sp.__version__,
       "authorisation": "coordinator ruling 268 (conditional) + minimal-repair ruling",
       "u_touched": False, "uniqueness_claimed": False,
       "repair_note": "v1 gate stalled: factor_list(extension=[sqrt(-3)]) and Poly(modulus=p) both misbehaved; "
                      "replaced by gcd-based cube test and the in-house F_p factor_pattern."}
def save(): json.dump(rep, open(CERT, "w"), indent=1, sort_keys=True)

x = sp.symbols('x')
c = sp.Rational(-512, 421875); q = x**3 - x/5; f6 = sp.expand(q**2 + c)
c3 = sp.Rational(3**4*5**3*19, 2**9); c5 = sp.Rational(3**6*5**5, 2**9)
c7 = sp.Rational(3**7*5**7, 2**10); c9 = sp.Rational(3**6*5**9, 2**11)
U = sp.expand((c3 + c5*x**2)*q + c7*x*(2*q**2 + c) + c9*(4*q**3 + 3*c*q))
B = sp.expand(c3 + c5*x**2 + 2*c7*x*q + c9*(4*q**2 + c))
A = sp.expand(U + sp.Rational(3, 2))
rep["model"] = {"curve": "y^2 = (x^3 - x/5)^2 - 512/421875", "c": str(c),
                "c3": str(c3), "c5": str(c5), "c7": str(c7), "c9": str(c9)}

# ---------- GATE 1a : cube test by gcd (exact) ----------
gate = {}
d3 = sp.sqrt(-3)
for nm, tau in (("N_tau1", sp.Rational(3,2)+sp.Rational(3,2)*d3), ("N_tau2", sp.Rational(3,2)-sp.Rational(3,2)*d3)):
    N = sp.Poly(sp.expand(sp.expand((A-tau)**2) - sp.expand(B**2*f6)), x)
    g = sp.gcd(N, N.diff(x)); r = sp.div(N, g)[0]
    iscube = sp.simplify(sp.expand(N.as_expr() - sp.LC(N)*(r.as_expr()/sp.LC(r))**3)) == 0
    gate[nm] = {"degree": int(N.degree()), "deg_gcd_with_derivative": int(g.degree()),
                "deg_radical": int(r.degree()), "equals_kappa_g_cubed": bool(iscube)}
    log("%s : deg=%d gcd=%d radical=%d cube=%s" % (nm, N.degree(), g.degree(), r.degree(), iscube))
L = sp.expand(sp.expand((sp.expand(U**2 - B**2*f6 - sp.Rational(27,4)))**2) + 27*U**2)
GL = sp.Poly(L, x); gl = sp.gcd(GL, GL.diff(x)); rl = sp.div(GL, gl)[0]
h = sp.expand(rl.as_expr()/sp.LC(rl))
gate["product_identity"] = {"deg_L": int(GL.degree()), "deg_gcd": int(gl.degree()),
    "L_equals_K_h_cubed": bool(sp.expand(L - sp.LC(GL)*h**3) == 0),
    "h": str(sp.factor(h)), "h_even": bool(sp.expand(h.subs(x, -x)-h) == 0)}
gate["f6"] = {"degree": int(sp.degree(f6, x)),
              "squarefree": bool(sp.gcd(sp.Poly(f6, x), sp.Poly(sp.diff(f6, x), x)).degree() == 0)}
log("L: deg=%d cube=%s h_even=%s ; f6 deg=%d squarefree=%s" %
    (gate["product_identity"]["deg_L"], gate["product_identity"]["L_equals_K_h_cubed"],
     gate["product_identity"]["h_even"], gate["f6"]["degree"], gate["f6"]["squarefree"]))

# ---------- GATE 1b : Frobenius patterns with the in-house F_p code ----------
ALLOWED = {(1,)*9, (2,2,2,2,1), (3,3,3), (7,1,1), (9,), (3,3,1,1,1), (6,2,1)}
def polypowmod(base, e, mod, p):
    r = [1]; b = polydivmod(base, mod, p)[1]
    while e:
        if e & 1: r = polydivmod(polymul(r, b, p), mod, p)[1]
        b = polydivmod(polymul(b, b, p), mod, p)[1]; e >>= 1
    return r
def factor_pattern(N, p):
    if len(N) != 10: return None
    d = polyder(N, p)
    if not d or len(polygcd(N, d, p)) != 1: return None
    pat = []; f = N[:]; deg = 0
    while len(f) > 1:
        deg += 1
        if 2*deg > len(f)-1: pat.append(len(f)-1); break
        xq = polypowmod([0, 1], p**deg, f, p)
        g2 = polygcd(f, polysub(xq, [0, 1], p), p)
        if len(g2) > 1:
            pat.extend([deg]*((len(g2)-1)//deg)); f = polydivmod(f, g2, p)[0]
    return tuple(sorted(pat, reverse=True))
def redp(expr, p):
    pol = sp.Poly(expr, x); n = pol.degree()
    out = [0]*(n+1)
    for m, co in zip(pol.monoms(), pol.coeffs()):
        r = sp.Rational(co)
        if r.q % p == 0: return None
        out[m[0]] = (int(r.p) % p) * pow(int(r.q) % p, p-2, p) % p
    while out and out[-1] == 0: out.pop()
    return out
seen = {}; bad = []; sevens = []
for p in (11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
    Ap = redp(A, p); Bp = redp(B, p); Fp = redp(f6, p)
    if Ap is None or Bp is None or Fp is None or len(Fp) != 7: continue
    if len(polygcd(Fp, polyder(Fp, p), p)) != 1: continue
    for t0 in range(p):
        N = polysub(polymul(polysub(Ap, [t0], p), polysub(Ap, [t0], p), p),
                    polymul(polymul(Bp, Bp, p), Fp, p), p)
        pat = factor_pattern(N, p)
        if pat is None: continue
        seen[pat] = seen.get(pat, 0) + 1
        if pat not in ALLOWED: bad.append([p, t0, list(pat)])
        if pat == (7, 1, 1): sevens.append([p, t0])
gate["frobenius"] = {"patterns": {str(list(k)): v for k, v in sorted(seen.items())},
                     "outside_PGammaL_2_8": bad[:10], "n_samples": sum(seen.values()),
                     "seven_cycle_witnesses_p_t0": sevens[:10],
                     "primitivity_argument": "a transitive group on 9 points containing a 7-cycle is 2-transitive (Jordan) "
                        "=> primitive => the cover is non-decomposable (no intermediate field)"}
log("Frobenius patterns: %s" % gate["frobenius"]["patterns"])
log("samples=%d  outside PGammaL: %s  (7,1,1) witnesses: %s" %
    (gate["frobenius"]["n_samples"], bad[:5] or "none", sevens[:5]))
gate["PASS"] = bool(all(gate[n]["degree"] == 9 and gate[n]["equals_kappa_g_cubed"] for n in ("N_tau1", "N_tau2"))
                    and gate["f6"]["squarefree"] and gate["f6"]["degree"] == 6
                    and gate["product_identity"]["L_equals_K_h_cubed"]
                    and seen and not bad and sevens)
rep["gate_schema_v2"] = gate; save()
log("GATE PASS = %s" % gate["PASS"])
if not gate["PASS"]:
    rep["status"] = "gate_failed_no_fire"; save(); log("FAIL-CLOSED: not firing"); LOG.close(); sys.exit(1)

# ---------- (2) PREREGISTRATION, frozen before any u computation ----------
rep["preregistration"] = {
 "frozen_before_measurement": True,
 "a_quantity": {"object": "u_0 of Prop U-LOC (u_meas_m3_design_v1.md 1.2)",
   "cusp": "P_0 over lambda=0 (e=9); image Pbar = infty_+ on C = the unique pole of t (ord 9)",
   "local_parameter": "s := 1/x at infty_+ (Q-rational); W->C unramified at P_0 so s is a parameter upstairs",
   "extraction": "t = c_lead*s^-9*(1+O(s)) at Pbar ; u_0 := -c_lead^{-1} ; [u_0^{-1}]_9 = [c_lead]_9",
   "bindings": ["integral model exactly as written (NOT minimalised)",
     "cusp section: the branch with y/x^3 -> +1",
     "tame normalisation: s = 1/x exactly; another s changes u_0 by a 9th power (Lemma SL-2)",
     "Sol F91-5.4: good reduction does NOT make u a unit; valuations reported for every prime in the support, no unit claim"],
   "sign_convention": "tau_1 = 3/2 + (3/2)sqrt(-3); the S3 involution sends t -> 3-t and swaps tau_1,tau_2"},
 "b_recorded": ["u_0 exact", "u_0^{-1} exact", "prime factorisations", "v_p for all p in the support",
   "squarefree part of u_0^{-1}", "exponent vector of u_0^{-1} mod 9"],
 "c_C1prime": {"claim": "this u_0 is the u of the S4-window bridge (Thm SURJ-S4)",
   "status": "NOT PROVED HERE - separate line; audit target for the mathematician / Sol (Sol F91-5.3 separation)"},
 "d_no_interpretation": "machine values only; no verdict on ord([u^{-1}]_9), on surjectivity, or against any prediction"}
rep["status"] = "preregistration_frozen"; save()
log("\n=== PREREGISTRATION FROZEN (written to cert before any u computation) ===")

# ---------- (3) FIRE ----------
s = sp.symbols('s', positive=True)
xs = 1/s
ys = sp.sqrt(sp.together(f6.subs(x, xs)))
th = ys + q.subs(x, xs)
tt = sp.Rational(3, 2) + c3*th + c5*xs**2*th + c7*xs*th**2 + c9*th**3
lead = sp.nsimplify(sp.simplify(sp.limit(sp.simplify(sp.expand(tt)*s**9), s, 0)))
log("\n=== U-LOC FIRED ===")
log("c_lead = %s   (identity check c_lead - 8*c9 = %s)" % (lead, sp.simplify(lead - 8*c9)))
u0 = sp.nsimplify(-1/lead); u0i = sp.nsimplify(1/u0)
def fac(r):
    r = sp.Rational(r); d = {}
    for k_, v_ in sp.factorint(abs(r.p)).items(): d[str(k_)] = int(v_)
    for k_, v_ in sp.factorint(r.q).items(): d[str(k_)] = -int(v_)
    return d, (-1 if r < 0 else 1)
fu, su = fac(u0i); sqf = su
for pr, e in fu.items():
    if e % 2: sqf *= int(pr)
rep["measurement"] = {"c_lead": str(lead), "u_0": str(u0), "u_0_inverse": str(u0i),
  "u_0_inverse_sign": int(su), "u_0_inverse_valuations": fu,
  "u_0_valuations": {k_: -v_ for k_, v_ in fu.items()},
  "squarefree_part_of_u_0_inverse": int(sqf),
  "exponent_vector_mod_9_of_u_0_inverse": {k_: int(v_ % 9) for k_, v_ in fu.items()},
  "note": "machine values only, no interpretation"}
rep["u_touched"] = True; rep["status"] = "measured"; save()
log("u_0 = %s" % u0); log("u_0^{-1} = %s" % u0i)
log("valuations(u_0^{-1}) = %s ; sign = %s ; squarefree part = %s" % (fu, su, sqf))
log("exponent vector mod 9 = %s" % rep["measurement"]["exponent_vector_mod_9_of_u_0_inverse"])
log("cert: %s" % CERT)
LOG.close()
