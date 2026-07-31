# u_meas_caseb_newton5.py -- NEWTON-5 : a=2, b=1 kept (e=0), c returned to the unknowns.
#   C : y^2 = f6 = q^2 + c,  q = x^3 + x ;  Pbar = infty_+ ; theta = y+q ; theta*thetabar = c
#   t = 3/2 + c3*theta + c5*x^2*theta + c7*x*theta^2 + c9*theta^3
#   branch condition (rationalised, addendum 3): P^2 + 27 U^2 = K h^3, h monic EVEN degree 6
# 6 equations, 5 unknowns (c3,c5,c7,c9,c).  F_7 exhaustive -> 7-adic Newton -> rational reconstruction.
# No expected value is hard-coded.  U-LOC is NOT fired.  Uniqueness is NOT claimed.
import sys, json, time, math
from itertools import combinations, product
import sympy as sp

LOG = open(sys.argv[1], "w")
def log(s):
    print(s); LOG.write(str(s)+"\n"); LOG.flush()

CERT = "search/certs/u_meas_caseb_newton5_20260731.json"
rep = {"schema": "u-meas-caseb-newton5/v1", "sympy_version": sp.__version__, "prime": 7,
       "model": "y^2 = (x^3+x)^2 + c ; a=2,b=1 (e=0) kept from I1=1/4 ; c UNKNOWN",
       "unknowns": ["c3", "c5", "c7", "c9", "c"], "u_touched": False,
       "uniqueness_claimed": False, "branch_note": "solutions of the 7-adic branches only",
       "checkpoints": [], "status": "running"}
def save(): json.dump(rep, open(CERT, "w"), indent=1, sort_keys=True)

x = sp.symbols('x')
c3, c5, c7, c9, cc = sp.symbols('c3 c5 c7 c9 c')
h4, h2, h0 = sp.symbols('h4 h2 h0')
q = x**3 + x
f6 = sp.expand(q**2 + cc)
U = sp.expand((c3 + c5*x**2)*q + c7*x*(2*q**2 + cc) + c9*(4*q**3 + 3*cc*q))
B = sp.expand(c3 + c5*x**2 + 2*c7*x*q + c9*(4*q**2 + cc))
P = sp.expand(U**2 - B**2*f6 - sp.Rational(27, 4))
log("sympy %s ; deg U=%s deg B=%s deg P=%s" % (sp.__version__, sp.degree(U, x), sp.degree(B, x), sp.degree(P, x)))

h = x**6 + h4*x**4 + h2*x**2 + h0
LHS = sp.expand(P**2 + 27*U**2)
K = sp.expand(sp.LC(sp.Poly(LHS, x)))
log("leading coeff K = %s" % K)
pe = sp.Poly(sp.expand(LHS - K*h**3), x)
DEG = pe.degree()
cf = {DEG-i: sp.expand(co) for i, co in enumerate(pe.all_coeffs())}
log("deg E = %s ; odd-degree coeffs nonzero: %s" % (DEG, [d for d in cf if d % 2 and cf[d] != 0]))

subs = {}
tops = sorted([d for d in cf if d % 2 == 0], reverse=True)[:3]
for deg, var in zip(tops, (h4, h2, h0)):
    s = sp.solve(sp.Eq(sp.expand(cf[deg].subs(subs)), 0), var, dict=True)
    if len(s) != 1:
        log("stage-1 failure at x^%d" % deg); rep["status"] = "h_elim_fail"; save(); sys.exit(1)
    subs[var] = sp.together(s[0][var])
EQS = []
for deg in sorted([d for d in cf if d not in tops and d % 2 == 0], reverse=True):
    e = sp.expand(sp.numer(sp.cancel(sp.together(cf[deg].subs(subs)))))
    if e != 0: EQS.append(e)
log("residual equations: total degrees %s" % [int(sp.total_degree(e)) for e in EQS])
rep["residual_degrees"] = [int(sp.total_degree(e)) for e in EQS]; save()

VARS = (c3, c5, c7, c9, cc)
POLYS = []
for e in EQS:
    pol = sp.Poly(e, *VARS); den = 1
    for co in pol.coeffs(): den = sp.ilcm(den, sp.Rational(co).q)
    ip = sp.Poly(sp.expand(e*den), *VARS); ic = [int(v) for v in ip.coeffs()]
    v7 = min((0 if v == 0 else sp.multiplicity(7, abs(v))) for v in ic)
    POLYS.append({m: int(co)//7**v7 for m, co in zip(ip.monoms(), ic)})
log("monomial counts: %s" % [len(d) for d in POLYS])

def ev(d, c, M):
    s = 0
    for m, co in d.items():
        tm = co % M
        for i, ei in enumerate(m):
            if ei: tm = tm*pow(c[i], ei, M) % M
        s = (s + tm) % M
    return s % M

def dev(d, c, M, j):
    s = 0
    for m, co in d.items():
        if m[j] == 0: continue
        tm = co*m[j] % M
        for i, ei in enumerate(m):
            e2 = ei-1 if i == j else ei
            if e2: tm = tm*pow(c[i], e2, M) % M
        s = (s + tm) % M
    return s % M

def detmod(Mx, M):
    n = len(Mx); Mx = [r[:] for r in Mx]; det = 1
    for i in range(n):
        piv = next((r for r in range(i, n) if Mx[r][i] % 7 != 0), None)
        if piv is None: return 0
        if piv != i: Mx[i], Mx[piv] = Mx[piv], Mx[i]
        det = det*Mx[i][i] % M; inv = pow(Mx[i][i], -1, M)
        for r in range(i+1, n):
            f = Mx[r][i]*inv % M
            for k2 in range(i, n): Mx[r][k2] = (Mx[r][k2] - f*Mx[i][k2]) % M
    return det % M

def solve_lin(Mx, rhs, M):
    n = len(Mx); A = [row[:] + [rhs[i]] for i, row in enumerate(Mx)]
    for i in range(n):
        piv = next((r for r in range(i, n) if A[r][i] % 7 != 0), None)
        if piv is None: return None
        A[i], A[piv] = A[piv], A[i]; inv = pow(A[i][i], -1, M)
        A[i] = [v*inv % M for v in A[i]]
        for r in range(n):
            if r != i and A[r][i]:
                f = A[r][i]; A[r] = [(A[r][k2] - f*A[i][k2]) % M for k2 in range(n+1)]
    return [A[i][n] for i in range(n)]

def sqfree7(cv):
    f = sp.Poly(sp.expand((x**3+x)**2 + cv), x, modulus=7)
    return sp.Poly(sp.gcd(f, f.diff(x)), x, modulus=7).degree() == 0

t0 = time.time(); pts = []
for tup in product(range(7), repeat=5):
    if tup[3] == 0 or tup[4] == 0: continue
    if all(ev(d, list(tup), 7) == 0 for d in POLYS): pts.append(list(tup))
log("F_7 points (c9!=0, c!=0) satisfying all 6 eqs: %d  (%.1fs)" % (len(pts), time.time()-t0))
pts = [p for p in pts if sqfree7(p[4])]
log("  after f6-squarefree filter: %d -> %s" % (len(pts), pts[:30]))
rep["n_F7_points"] = len(pts); rep["F7_points"] = [list(map(int, p)) for p in pts]; save()

def ratrec(a, M):
    bd = math.isqrt(M//2); r0, r1 = M, a % M; s0, s1 = 0, 1
    while r1 > bd:
        qq = r0//r1; r0, r1 = r1, r0-qq*r1; s0, s1 = s1, s0-qq*s1
    if s1 == 0 or abs(s1) > bd: return None
    n, d = r1, s1
    if d < 0: n, d = -n, -d
    g = math.gcd(abs(n), d) or 1
    return sp.Rational(n//g, d//g)

NAMES = ("c3", "c5", "c7", "c9", "c")
survivors = []
for p0 in pts:
    ch = None
    for combo in combinations(range(len(POLYS)), 5):
        J = [[dev(POLYS[i], p0, 7, j) for j in range(5)] for i in combo]
        if detmod(J, 7) % 7 != 0: ch = combo; break
    if ch is None:
        log("  pt %s : Jacobian singular for every 5-subset" % p0); continue
    c = p0[:]; k = 1; ok = True; cps = []
    while k < 96:
        k2 = min(2*k, 96); M = 7**k2; c = [v % M for v in c]
        for _ in range(3):
            F = [ev(POLYS[i], c, M) for i in ch]
            J = [[dev(POLYS[i], c, M, j) for j in range(5)] for i in ch]
            dz = solve_lin(J, [(-f) % M for f in F], M)
            if dz is None: ok = False; break
            c = [(c[i] + dz[i]) % M for i in range(5)]
        if not ok: break
        drv = all(ev(POLYS[i], c, M) == 0 for i in ch)
        chk = [ev(POLYS[i], c, M) for i in range(len(POLYS)) if i not in ch]
        cps.append({"k": k2, "driver_zero": bool(drv),
                    "checker_7val": [(0 if v == 0 else int(sp.multiplicity(7, v))) for v in chk]})
        if not drv or any(v != 0 for v in chk): ok = False; break
        k = k2
    log("  pt %s driver=%s -> %s at 7^%d" % (p0, list(ch), "OK" if ok else "DIED", k))
    rep["checkpoints"].append({"seed": list(map(int, p0)), "driver": list(ch),
                               "reached_k": k, "ok": bool(ok), "levels": cps}); save()
    if ok and k >= 96:
        M = 7**96; rec = [ratrec(v, M) for v in c]
        log("    reconstruction: %s" % rec)
        if any(v is None for v in rec): continue
        sub = dict(zip(VARS, rec)); exact = [sp.simplify(e.subs(sub)) for e in EQS]
        allz = all(v == 0 for v in exact)
        log("    EXACT check (6 eqs): %s -> all zero: %s" % (exact, allz))
        I2 = sp.Rational(rec[4], 8)
        d = {"seed": list(map(int, p0)),
             "values": {n: str(v) for n, v in zip(NAMES, rec)},
             "denominator_factorisations": {n: {str(a1): int(b1) for a1, b1 in sp.factorint(sp.Rational(v).q).items()}
                                            for n, v in zip(NAMES, rec)},
             "numerator_factorisations": {n: ({str(a1): int(b1) for a1, b1 in sp.factorint(abs(sp.Rational(v).p)).items()} if v != 0 else {})
                                          for n, v in zip(NAMES, rec)},
             "I2_c_over_a3": str(I2), "I2_height": int(max(abs(I2.p), I2.q)),
             "I2_vs_minus27over8": str(sp.Rational(I2) - sp.Rational(-27, 8)),
             "exact_verification_all_zero": bool(allz),
             "residues": {str(pp): {n: int(sp.Rational(v).p*pow(int(sp.Rational(v).q), pp-2, pp) % pp)
                                    for n, v in zip(NAMES, rec)} for pp in (13, 19)}}
        survivors.append(d); rep.setdefault("solutions", []).append(d); save()

rep["status"] = "solutions_found" if survivors else "all_branches_died"
save()
log("")
log("=== %d 7-adic branch solutions ===" % len(survivors))
log("cert: %s  status=%s" % (CERT, rep["status"]))
LOG.close()
