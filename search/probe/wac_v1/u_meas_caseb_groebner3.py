# u_meas_caseb_groebner3.py -- stage 2: saturate by c9, then eliminate.
import json, sys, time
import sympy as sp
LOG = open(sys.argv[1], "w")
def log(s):
    print(s); LOG.write(str(s)+"\n"); LOG.flush()
x = sp.symbols('x'); c3,c5,c7,c9,h4,h2,h0 = sp.symbols('c3 c5 c7 c9 h4 h2 h0')
q = x**3+x; f6 = sp.expand(q**2-27)
U = sp.expand((c3+c5*x**2)*q + c7*x*(2*q**2-27) + c9*(4*q**3-81*q))
B = sp.expand(c3+c5*x**2+2*c7*x*q+c9*(4*q**2-27))
P = sp.expand(U**2-B**2*f6-sp.Rational(27,4))
h = x**6+h4*x**4+h2*x**2+h0
pe = sp.Poly(sp.expand(sp.expand(P**2+27*U**2)-432*c9**2*h**3), x)
DEG = pe.degree(); cf = {DEG-i: sp.expand(co) for i,co in enumerate(pe.all_coeffs())}
subs = {}; tops = sorted([d for d in cf if d%2==0], reverse=True)[:3]
for deg,var in zip(tops,(h4,h2,h0)):
    subs[var] = sp.together(sp.solve(sp.Eq(sp.expand(cf[deg].subs(subs)),0),var,dict=True)[0][var])
rest = []
for deg in sorted([d for d in cf if d not in tops and d%2==0], reverse=True):
    e = sp.expand(sp.numer(sp.cancel(sp.together(cf[deg].subs(subs)))))
    if e != 0:
        # strip c9^k (c9 != 0 : pole order exactly 9)
        pp = sp.Poly(e, c9); k = min(m[0] for m in pp.monoms())
        e = sp.expand(sp.cancel(e/c9**k))
        rest.append((deg, k, e))
log("sympy %s" % sp.__version__)
for (deg,k,e) in rest:
    log("  x^%-2d : c9^%d stripped -> total degree %d, %d terms" % (deg,k,sp.total_degree(e),len(sp.Poly(e,c3,c5,c7,c9).monoms())))
eqs = [e for (_,_,e) in rest]
t0=time.time()
try:
    G = sp.groebner(eqs, c3,c5,c7,c9, order='grevlex')
    log("grevlex groebner in %.1fs : %d gens; leading degrees %s" %
        (time.time()-t0, len(G.exprs), [sp.total_degree(g) for g in G.exprs]))
    for g in G.exprs[:12]: log("   %s" % sp.factor(g))
    json.dump({"schema":"u-meas-caseb-groebner/v1-partial","sympy_version":sp.__version__,
               "curve":"y^2 = (x^3+x)^2 - 27","status":"grevlex basis computed",
               "h_elimination":{str(k):str(v) for k,v in subs.items()},
               "grevlex_generators":[str(g) for g in G.exprs]},
              open("search/certs/u_meas_caseb_groebner_20260731.json","w"), indent=1, sort_keys=True)
    log("cert written")
except Exception as ex:
    log("grevlex failed: %s" % ex)
LOG.close()
