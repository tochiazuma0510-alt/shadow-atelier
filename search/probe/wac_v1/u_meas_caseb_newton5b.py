# u_meas_caseb_newton5b.py -- NEWTON-5 continued at higher 7-adic precision.
# c reconstructed cleanly as 512/3375 = (8/15)^3 at 7^96; the c_i needed more precision
# (their reconstructions sat exactly at the 10^40 bound = classic failure signature).
# Here we substitute the exact c and lift the 4 remaining unknowns to 7^512.
import sys, json, time, math
from itertools import combinations
import sympy as sp
LOG = open(sys.argv[1], "w")
def log(s):
    print(s); LOG.write(str(s)+"\n"); LOG.flush()
CERT = "search/certs/u_meas_caseb_newton5_20260731.json"
rep = json.load(open(CERT))

CVAL = sp.Rational(512, 3375)
log("c fixed to %s = (%s)^3 ; height %d" % (CVAL, sp.Rational(8, 15), max(abs(CVAL.p), CVAL.q)))
x = sp.symbols('x'); c3, c5, c7, c9 = sp.symbols('c3 c5 c7 c9'); h4, h2, h0 = sp.symbols('h4 h2 h0')
q = x**3 + x; f6 = sp.expand(q**2 + CVAL)
U = sp.expand((c3 + c5*x**2)*q + c7*x*(2*q**2 + CVAL) + c9*(4*q**3 + 3*CVAL*q))
B = sp.expand(c3 + c5*x**2 + 2*c7*x*q + c9*(4*q**2 + CVAL))
P = sp.expand(U**2 - B**2*f6 - sp.Rational(27, 4))
h = x**6 + h4*x**4 + h2*x**2 + h0
LHS = sp.expand(P**2 + 27*U**2); K = sp.expand(sp.LC(sp.Poly(LHS, x)))
pe = sp.Poly(sp.expand(LHS - K*h**3), x); DEG = pe.degree()
cf = {DEG-i: sp.expand(co) for i, co in enumerate(pe.all_coeffs())}
subs = {}; tops = sorted([d for d in cf if d % 2 == 0], reverse=True)[:3]
for deg, var in zip(tops, (h4, h2, h0)):
    subs[var] = sp.together(sp.solve(sp.Eq(sp.expand(cf[deg].subs(subs)), 0), var, dict=True)[0][var])
EQS = []
for deg in sorted([d for d in cf if d not in tops and d % 2 == 0], reverse=True):
    e = sp.expand(sp.numer(sp.cancel(sp.together(cf[deg].subs(subs)))))
    if e != 0: EQS.append(e)
log("residual degrees: %s" % [int(sp.total_degree(e)) for e in EQS])
VARS = (c3, c5, c7, c9); POLYS = []
for e in EQS:
    pol = sp.Poly(e, *VARS); den = 1
    for co in pol.coeffs(): den = sp.ilcm(den, sp.Rational(co).q)
    ip = sp.Poly(sp.expand(e*den), *VARS); ic = [int(v) for v in ip.coeffs()]
    v7 = min((0 if v == 0 else sp.multiplicity(7, abs(v))) for v in ic)
    POLYS.append({m: int(co)//7**v7 for m, co in zip(ip.monoms(), ic)})
def ev(d, c, M):
    s = 0
    for m, co in d.items():
        tm = co % M
        for i, ei in enumerate(m):
            if ei: tm = tm*pow(c[i], ei, M) % M
        s = (s+tm) % M
    return s % M
def dev(d, c, M, j):
    s = 0
    for m, co in d.items():
        if m[j] == 0: continue
        tm = co*m[j] % M
        for i, ei in enumerate(m):
            e2 = ei-1 if i == j else ei
            if e2: tm = tm*pow(c[i], e2, M) % M
        s = (s+tm) % M
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
            for k2 in range(i, n): Mx[r][k2] = (Mx[r][k2]-f*Mx[i][k2]) % M
    return det % M
def solve_lin(Mx, rhs, M):
    n = len(Mx); A = [row[:]+[rhs[i]] for i, row in enumerate(Mx)]
    for i in range(n):
        piv = next((r for r in range(i, n) if A[r][i] % 7 != 0), None)
        if piv is None: return None
        A[i], A[piv] = A[piv], A[i]; inv = pow(A[i][i], -1, M); A[i] = [v*inv % M for v in A[i]]
        for r in range(n):
            if r != i and A[r][i]:
                f = A[r][i]; A[r] = [(A[r][k2]-f*A[i][k2]) % M for k2 in range(n+1)]
    return [A[i][n] for i in range(n)]
def ratrec(a, M):
    bd = math.isqrt(M//2); r0, r1 = M, a % M; s0, s1 = 0, 1
    while r1 > bd:
        qq = r0//r1; r0, r1 = r1, r0-qq*r1; s0, s1 = s1, s0-qq*s1
    if s1 == 0 or abs(s1) > bd: return None
    n, d = r1, s1
    if d < 0: n, d = -n, -d
    g = math.gcd(abs(n), d) or 1
    return sp.Rational(n//g, d//g)

seed = [1, 5, 1, 5]
log("seed residuals mod 7: %s" % [ev(d, seed, 7) for d in POLYS])
ch = None
for combo in combinations(range(len(POLYS)), 4):
    J = [[dev(POLYS[i], seed, 7, j) for j in range(4)] for i in combo]
    if detmod(J, 7) % 7 != 0: ch = combo; break
log("driver = %s" % list(ch))
c = seed[:]; k = 1; KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 512
t0 = time.time(); found = None
while k < KMAX:
    k2 = min(2*k, KMAX); M = 7**k2; c = [v % M for v in c]
    for _ in range(3):
        F = [ev(POLYS[i], c, M) for i in ch]
        J = [[dev(POLYS[i], c, M, j) for j in range(4)] for i in ch]
        dz = solve_lin(J, [(-f) % M for f in F], M)
        c = [(c[i]+dz[i]) % M for i in range(4)]
    drv = all(ev(POLYS[i], c, M) == 0 for i in ch)
    chk = [ev(POLYS[i], c, M) for i in range(len(POLYS)) if i not in ch]
    cv = [(0 if v == 0 else int(sp.multiplicity(7, v))) for v in chk]
    log("  k=%-4d driver_zero=%s checker_7val=%s (need >= %d)  [%.0fs]" % (k2, drv, cv, k2, time.time()-t0))
    if not drv or any(v != 0 for v in chk):
        log("FAIL-CLOSED at 7^%d" % k2); rep["stage2_status"] = "checker_fail_at_%d" % k2
        json.dump(rep, open(CERT, "w"), indent=1, sort_keys=True); LOG.close(); sys.exit(1)
    k = k2
    M2=7**k
    prods = {}
    for (i,j) in ((0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)):
        prods[(i,j)] = ratrec(c[i]*c[j] % M2, M2)
    if all(v is not None for v in prods.values()):
        log("    PRODUCT reconstruction at 7^%d : %s" % (k, {("c%d*c%d"%(3+2*i,3+2*j)): str(v) for (i,j),v in prods.items()}))
        found = prods; break
    rec = [ratrec(v, 7**k) for v in c]
    if all(r is not None for r in rec):
        sub = dict(zip(VARS, rec)); exact = [sp.simplify(e.subs(sub)) for e in EQS]
        hts = [int(max(abs(sp.Rational(r).p), sp.Rational(r).q)) for r in rec]
        log("    ratrec heights ~ %s ; exact all-zero: %s" % ([len(str(h)) for h in hts], all(v == 0 for v in exact)))
        if all(v == 0 for v in exact):
            found = rec; break
if found and isinstance(found, dict):
    rep["stage2_status"]="EXACT_PRODUCTS"
    rep["exact_products"]={("c%d*c%d"%(3+2*i,3+2*j)): str(v) for (i,j),v in found.items()}
    rep["exact_products"]["c"]=str(CVAL)
    log("PRODUCTS stored")
    import json as _j; _j.dump(rep, open(CERT,"w"), indent=1, sort_keys=True)
    log("cert updated"); LOG.close(); sys.exit(0)
if found:
    NAMES = ("c3", "c5", "c7", "c9")
    sol = {"c": str(CVAL), "I2_c_over_a3": str(CVAL/8),
           "values": {n: str(v) for n, v in zip(NAMES, found)},
           "denominator_factorisations": {n: {str(a1): int(b1) for a1, b1 in sp.factorint(sp.Rational(v).q).items()}
                                          for n, v in zip(NAMES, found)},
           "numerator_factorisations": {n: ({str(a1): int(b1) for a1, b1 in sp.factorint(abs(sp.Rational(v).p)).items()} if v != 0 else {})
                                        for n, v in zip(NAMES, found)},
           "c_denominator_factorisation": {str(a1): int(b1) for a1, b1 in sp.factorint(CVAL.q).items()},
           "exact_verification_all_zero": True, "reached_7_power": k,
           "residues": {str(pp): {n: int(sp.Rational(v).p*pow(int(sp.Rational(v).q), pp-2, pp) % pp)
                                  for n, v in zip(NAMES, found)} for pp in (13, 19)}}
    rep["stage2_status"] = "EXACT_SOLUTION"; rep["exact_solution"] = sol
    log("\n=== EXACT SOLUTION (7-adic branch of seed %s) ===" % seed)
    for kk, vv in sol.items(): log("  %s : %s" % (kk, vv))
else:
    rep["stage2_status"] = "no_reconstruction_up_to_7^%d" % KMAX
    log("no exact reconstruction up to 7^%d" % KMAX)
json.dump(rep, open(CERT, "w"), indent=1, sort_keys=True)
log("cert updated: %s" % CERT)
LOG.close()
