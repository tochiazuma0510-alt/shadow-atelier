# u_meas_caseb_groebner2.py -- staged elimination version (h eliminated first, then Groebner in c).
# Same system as u_meas_caseb_groebner.py.  Writes directly to a log file (no pipe buffering).
import json, sys, time
import sympy as sp

LOG = open(sys.argv[1] if len(sys.argv) > 1 else "caseb_groebner.log", "w")
def log(s):
    print(s); LOG.write(str(s)+"\n"); LOG.flush()

x = sp.symbols('x')
c3, c5, c7, c9, h4, h2, h0 = sp.symbols('c3 c5 c7 c9 h4 h2 h0')
q  = x**3 + x
f6 = sp.expand(q**2 - 27)
U = sp.expand((c3 + c5*x**2)*q + c7*x*(2*q**2 - 27) + c9*(4*q**3 - 81*q))
B = sp.expand(c3 + c5*x**2 + 2*c7*x*q + c9*(4*q**2 - 27))
P = sp.expand(U**2 - B**2*f6 - sp.Rational(27, 4))

log("sympy %s" % sp.__version__)
log("deg U = %s, deg B = %s, deg P = %s  (deg P <= 8 required for deg N = 9)"
    % (sp.degree(U, x), sp.degree(B, x), sp.degree(P, x)))

h = x**6 + h4*x**4 + h2*x**2 + h0
E = sp.expand(sp.expand(P**2 + 27*U**2) - 432*c9**2*h**3)
pe = sp.Poly(E, x)
# coefficients by descending degree
DEG = pe.degree()
cf = {DEG-i: sp.expand(co) for i, co in enumerate(pe.all_coeffs())}
log('deg E = %s (leading terms of 27U^2 and 432 c9^2 h^3 cancel as designed)' % DEG)

odd_nonzero = [d for d in cf if d % 2 == 1 and cf[d] != 0]
log("odd-degree coefficients nonzero: %s" % odd_nonzero)

# stage 1 : solve x^16 for h4, x^14 for h2, x^12 for h0 (each linear in turn)
subs = {}
tops = sorted([d for d in cf if d % 2 == 0], reverse=True)[:3]
for deg, var in zip(tops, (h4, h2, h0)):
    eq = sp.expand(cf[deg].subs(subs))
    sol = sp.solve(sp.Eq(eq, 0), var, dict=True)
    if len(sol) != 1:
        log("stage-1 failure at x^%d for %s : %s" % (deg, var, sol)); sys.exit(1)
    subs[var] = sp.together(sol[0][var])
    log("  h from x^%d : %s = %s" % (deg, var, subs[var]))

rest = []
for deg in sorted([d for d in cf if d not in tops and d % 2 == 0], reverse=True):
    e = sp.simplify(sp.together(cf[deg].subs(subs)))
    e = sp.numer(sp.cancel(e))
    e = sp.expand(e)
    if e != 0: rest.append(e)
log("remaining equations in (c3,c5,c7,c9): %d  (degrees %s)"
    % (len(rest), [sp.total_degree(r) for r in rest]))

t0 = time.time()
G = sp.groebner(rest, c3, c5, c7, c9, order='lex')
log("groebner (lex) in %.1fs, %d generators" % (time.time()-t0, len(G.exprs)))
for g in G.exprs: log("   %s" % sp.factor(g))

t0 = time.time()
sols = sp.solve(rest, [c3, c5, c7, c9], dict=True)
log("solve in %.1fs : %d branches" % (time.time()-t0, len(sols)))
good = []
for s in sols:
    v = {k: sp.nsimplify(s.get(k, k)) for k in (c3, c5, c7, c9)}
    if not v[c9].free_symbols and v[c9] == 0:
        log("  reject (c9=0, pole order < 9): %s" % {str(k): v[k] for k in v}); continue
    free = [str(k) for k in v if v[k].free_symbols]
    dec = (v[c5] == 0 and v[c7] == 0)
    log("  branch %s  free=%s  decomposable=%s" % ({str(k): v[k] for k in v}, free, dec))
    if not dec and not free: good.append(v)

log("\n=== non-degenerate exact solutions: %d ===" % len(good))
report = {"schema": "u-meas-caseb-groebner/v1", "sympy_version": sp.__version__,
          "curve": "y^2 = (x^3+x)^2 - 27",
          "basis": ["theta", "x^2*theta", "x*theta^2", "theta^3"],
          "system": "P^2 + 27 U^2 = 432 c9^2 h^3 ; h monic even deg 6 ; h eliminated from x^16,x^14,x^12",
          "n_equations_after_elimination": len(rest),
          "groebner_lex_generators": [str(sp.factor(g)) for g in G.exprs],
          "solutions": []}
for v in good:
    d = {str(k): str(v[k]) for k in (c3, c5, c7, c9)}
    dens = set()
    for k in (c3, c5, c7, c9):
        val = v[k]
        if val.is_Rational and sp.Rational(val).q != 1:
            dens |= set(sp.factorint(sp.Rational(val).q).keys())
    d["denominator_primes"] = sorted(int(z) for z in dens)
    d["all_rational"] = all(v[k].is_Rational for k in (c3, c5, c7, c9))
    res = {}
    if d["all_rational"]:
        for p in (7, 13, 19):
            try:
                res[str(p)] = {str(k): int(sp.Rational(v[k]).p * pow(int(sp.Rational(v[k]).q), p-2, p) % p)
                               for k in (c3, c5, c7, c9)}
            except Exception as ex:
                res[str(p)] = "bad prime: %s" % ex
    d["residues"] = res
    report["solutions"].append(d)
    log("  %s" % d)

with open("search/certs/u_meas_caseb_groebner_20260731.json", "w") as fh:
    json.dump(report, fh, indent=1, sort_keys=True)
log("wrote search/certs/u_meas_caseb_groebner_20260731.json")
LOG.close()
