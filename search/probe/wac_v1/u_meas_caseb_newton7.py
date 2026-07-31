# u_meas_caseb_newton7.py -- 7-adic Newton lift of the p=7 branch of the case-(b) residual system.
#
# System: curve C : y^2 = (x^3+x)^2 - 27 fixed; t = 3/2 + c3*th + c5*x^2*th + c7*x*th^2 + c9*th^3.
# Branch condition rationalised (addendum 3):  P^2 + 27 U^2 = 432 c9^2 h(x)^3, h monic even deg 6;
# h4,h2,h0 eliminated in closed form from the x^16,x^14,x^12 coefficients; 6 residual equations
# in (c3,c5,c7,c9) of total degrees 12,15,18,21,24,27.
#
# Seed: the p=7 sieve survivor (c3,c5,c7,c9) = (1,5,1,5) mod 7  (u_meas_caseb_search2.py / _sieve.py).
# 4 equations with invertible Jacobian at the seed drive Newton; the other 2 are checked at every
# precision level (fail-closed).  Then rational reconstruction + exact sympy verification.
#
# No expected value of u appears anywhere.  U-LOC is NOT fired here.

import json, sys, time, math
from itertools import combinations
import sympy as sp

LOG = open(sys.argv[1] if len(sys.argv) > 1 else "newton7.log", "w")
def log(s):
    print(s); LOG.write(str(s)+"\n"); LOG.flush()

CERT = "search/certs/u_meas_caseb_newton7_20260731.json"
rep = {"schema": "u-meas-caseb-newton7/v1", "sympy_version": sp.__version__,
       "curve": "y^2 = (x^3+x)^2 - 27", "prime": 7,
       "seed_mod_7": {"c3": 1, "c5": 5, "c7": 1, "c9": 5},
       "seed_source": "p=7 survivor of the schema-v2 sieve (monodromy 9T27-compatible, non-decomposable)",
       "branch_note": "This is the solution of the p=7 BRANCH; uniqueness over Q is NOT claimed here.",
       "u_touched": False, "checkpoints": [], "status": "running"}
def save():
    json.dump(rep, open(CERT, "w"), indent=1, sort_keys=True)

# ---------- build the residual system ----------
x = sp.symbols('x'); c3, c5, c7, c9, h4, h2, h0 = sp.symbols('c3 c5 c7 c9 h4 h2 h0')
q = x**3 + x; f6 = sp.expand(q**2 - 27)
U = sp.expand((c3 + c5*x**2)*q + c7*x*(2*q**2 - 27) + c9*(4*q**3 - 81*q))
B = sp.expand(c3 + c5*x**2 + 2*c7*x*q + c9*(4*q**2 - 27))
P = sp.expand(U**2 - B**2*f6 - sp.Rational(27, 4))
h = x**6 + h4*x**4 + h2*x**2 + h0
pe = sp.Poly(sp.expand(sp.expand(P**2 + 27*U**2) - 432*c9**2*h**3), x)
DEG = pe.degree(); cf = {DEG-i: sp.expand(co) for i, co in enumerate(pe.all_coeffs())}
subs = {}; tops = sorted([d for d in cf if d % 2 == 0], reverse=True)[:3]
for deg, var in zip(tops, (h4, h2, h0)):
    subs[var] = sp.together(sp.solve(sp.Eq(sp.expand(cf[deg].subs(subs)), 0), var, dict=True)[0][var])
EQS = []
for deg in sorted([d for d in cf if d not in tops and d % 2 == 0], reverse=True):
    e = sp.expand(sp.numer(sp.cancel(sp.together(cf[deg].subs(subs)))))
    if e != 0: EQS.append((deg, e))
log("sympy %s ; residual equations: %s" % (sp.__version__, [(d, int(sp.total_degree(e))) for d, e in EQS]))
rep["residual_degrees"] = [int(sp.total_degree(e)) for _, e in EQS]

VARS = (c3, c5, c7, c9)
# integer models with the 7-content stripped
POLYS = []
for deg, e in EQS:
    pol = sp.Poly(e, *VARS)
    den = 1
    for co in pol.coeffs(): den = sp.ilcm(den, sp.Rational(co).q)
    ip = sp.Poly(sp.expand(e*den), *VARS)
    ic = [int(v) for v in ip.coeffs()]
    v7 = min((0 if v == 0 else sp.multiplicity(7, abs(v))) for v in ic) if ic else 0
    d = {m: int(co)//7**v7 for m, co in zip(ip.monoms(), ic)}
    POLYS.append(d)
    log("  eq(x^%d): denom-lcm 7-adic val=%s, stripped 7^%d, %d monomials"
        % (deg, sp.multiplicity(7, den) if den % 7 == 0 else 0, v7, len(d)))

def ev(d, c, M):
    s = 0
    for m, co in d.items():
        tm = co % M
        for i, ei in enumerate(m):
            if ei: tm = tm * pow(c[i], ei, M) % M
        s = (s + tm) % M
    return s % M

def dev(d, c, M, j):
    s = 0
    for m, co in d.items():
        if m[j] == 0: continue
        tm = co*m[j] % M
        for i, ei in enumerate(m):
            e2 = ei-1 if i == j else ei
            if e2: tm = tm * pow(c[i], e2, M) % M
        s = (s + tm) % M
    return s % M

seed = [1, 5, 1, 5]
vals7 = [ev(d, seed, 7) for d in POLYS]
log("seed residuals mod 7: %s" % vals7)
if any(vals7):
    log("FAIL-CLOSED: seed does not satisfy the residual system mod 7"); rep["status"] = "seed_fail"; save(); sys.exit(1)

def detmod(Mx, M):
    n = len(Mx); Mx = [row[:] for row in Mx]; det = 1
    for i in range(n):
        piv = next((r for r in range(i, n) if Mx[r][i] % 7 != 0), None)
        if piv is None: return 0
        if piv != i: Mx[i], Mx[piv] = Mx[piv], Mx[i]; det = -det
        det = det*Mx[i][i] % M
        inv = pow(Mx[i][i], -1, M)
        for r in range(i+1, n):
            f = Mx[r][i]*inv % M
            for cc in range(i, n): Mx[r][cc] = (Mx[r][cc] - f*Mx[i][cc]) % M
    return det % M

def solve_lin(Mx, rhs, M):
    n = len(Mx); A = [row[:] + [rhs[i]] for i, row in enumerate(Mx)]
    for i in range(n):
        piv = next((r for r in range(i, n) if A[r][i] % 7 != 0), None)
        A[i], A[piv] = A[piv], A[i]
        inv = pow(A[i][i], -1, M)
        A[i] = [v*inv % M for v in A[i]]
        for r in range(n):
            if r != i and A[r][i]:
                f = A[r][i]
                A[r] = [(A[r][cc] - f*A[i][cc]) % M for cc in range(n+1)]
    return [A[i][n] for i in range(n)]

# choose 4 equations with invertible Jacobian mod 7
chosen = None
for combo in combinations(range(len(POLYS)), 4):
    J = [[dev(POLYS[i], seed, 7, j) for j in range(4)] for i in combo]
    if detmod(J, 7) % 7 != 0: chosen = combo; break
if chosen is None:
    log("FAIL: no 4-subset has invertible Jacobian mod 7"); rep["status"] = "jacobian_singular"; save(); sys.exit(1)
log("Newton driver equations (indices into the residual list): %s ; checkers: %s"
    % (list(chosen), [i for i in range(len(POLYS)) if i not in chosen]))
rep["newton_driver_eq_indices"] = list(chosen)
rep["checker_eq_indices"] = [i for i in range(len(POLYS)) if i not in chosen]

c = seed[:]; k = 1; t0 = time.time()
while k < 96:
    k2 = min(2*k, 96); M = 7**k2
    c = [v % M for v in c]
    for _ in range(3):
        F = [ev(POLYS[i], c, M) for i in chosen]
        J = [[dev(POLYS[i], c, M, j) for j in range(4)] for i in chosen]
        dz = solve_lin(J, [(-f) % M for f in F], M)
        c = [(c[i] + dz[i]) % M for i in range(4)]
    F = [ev(POLYS[i], c, M) for i in chosen]
    chk = [ev(POLYS[i], c, M) for i in range(len(POLYS)) if i not in chosen]
    ok = all(f == 0 for f in F)
    chk_v = [(0 if v == 0 else int(sp.multiplicity(7, v))) for v in chk]
    log("  k=%-3d driver residuals zero: %s ; checker 7-valuations: %s (>= k2=%d required)" % (k2, ok, chk_v, k2))
    rep["checkpoints"].append({"k": k2, "driver_zero": bool(ok), "checker_7valuations": chk_v,
                               "c_mod_7k": [int(v) for v in c]})
    save()
    if not ok:
        log("FAIL-CLOSED: Newton did not converge at k=%d" % k2); rep["status"] = "newton_fail"; save(); sys.exit(1)
    if any(v < k2 for v in chk_v):
        log("FAIL-CLOSED: a checker equation is not 0 mod 7^%d" % k2); rep["status"] = "checker_fail"; save(); sys.exit(1)
    k = k2
    if k >= 96: break
log("Newton finished to 7^%d in %.1fs" % (k, time.time()-t0))

def ratrec(a, M):
    bound = math.isqrt(M//2); r0, r1 = M, a % M; s0, s1 = 0, 1
    while r1 > bound:
        qq = r0//r1; r0, r1 = r1, r0-qq*r1; s0, s1 = s1, s0-qq*s1
    if s1 == 0 or abs(s1) > bound: return None
    n, d = r1, s1
    if d < 0: n, d = -n, -d
    g = math.gcd(abs(n), d) or 1
    return sp.Rational(n//g, d//g)

M = 7**k
rec = [ratrec(v, M) for v in c]
log("rational reconstruction: %s" % rec)
rep["reconstruction"] = {n: (str(v) if v is not None else None) for n, v in zip(("c3", "c5", "c7", "c9"), rec)}
if any(v is None for v in rec):
    log("reconstruction failed at 7^%d" % k); rep["status"] = "ratrec_fail"; save(); sys.exit(1)

dens = {}
for n, v in zip(("c3", "c5", "c7", "c9"), rec):
    dens[n] = {"numer": str(sp.Rational(v).p), "denom": str(sp.Rational(v).q),
               "denom_factorisation": {str(kk): int(vv) for kk, vv in sp.factorint(sp.Rational(v).q).items()},
               "numer_factorisation": {str(kk): int(vv) for kk, vv in sp.factorint(abs(sp.Rational(v).p)).items()} if v != 0 else {}}
rep["denominators"] = dens
log("denominator factorisations: %s" % {n: dens[n]["denom_factorisation"] for n in dens})

sub = dict(zip(VARS, rec))
exact = [sp.simplify(e.subs(sub)) for _, e in EQS]
log("EXACT verification (all 6 residual equations): %s" % exact)
rep["exact_verification"] = {"values": [str(v) for v in exact], "all_zero": all(v == 0 for v in exact)}
res_chk = {}
for p in (13, 19):
    try:
        res_chk[str(p)] = {n: int(sp.Rational(v).p * pow(int(sp.Rational(v).q), p-2, p) % p)
                           for n, v in zip(("c3", "c5", "c7", "c9"), rec)}
    except Exception as ex:
        res_chk[str(p)] = "bad prime: %s" % ex
rep["residues_for_crosscheck"] = res_chk
log("residues mod 13,19 (to be compared with the sieve survivors up to the alpha-twist): %s" % res_chk)
rep["status"] = "verified" if all(v == 0 for v in exact) else "exact_verification_failed"
save()
log("cert written: %s   status=%s" % (CERT, rep["status"]))
LOG.close()
