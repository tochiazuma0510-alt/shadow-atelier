# u_meas_caseb_sieve.py -- schema-v2 sieve on the case-(b) mod-p candidates.
# Order enforced (coordinator's directive):  tau2-consistency -> monodromy (9T27) ->
# primitivity/decomposability -> ONLY THEN u.
#
# Allowed Frobenius cycle types (GAP, _ct_tmp.g):
#   PSL(2,8)     : 1^9, 2^4 1, 3^3, 7 1 1, 9
#   PGammaL(2,8) : the above + 3^2 1^3, 6 2 1
# Any factorisation pattern of N_{t0}(x) outside the PGammaL list REJECTS the candidate.
# Raw measurements only.

import sys
from itertools import product
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
exec(open(__file__.replace('sieve', 'search2')).read().split('if __name__')[0])

ALLOWED = {(1,)*9, (2,2,2,2,1), (3,3,3), (7,1,1), (9,), (3,3,1,1,1), (6,2,1)}
PSL_ONLY = {(1,)*9, (2,2,2,2,1), (3,3,3), (7,1,1), (9,)}

def factor_pattern(N, p):
    """degrees of irreducible factors of squarefree-ish N over F_p, via distinct-degree"""
    if len(N) != 10: return None
    # squarefree check
    d = polyder(N, p)
    if not d or len(polygcd(N, d, p)) != 1: return None   # not squarefree -> skip this t0
    pat = []
    f = N[:]
    xq = [0, 1]
    deg = 0
    while len(f) > 1:
        deg += 1
        if 2*deg > len(f)-1:
            pat.append(len(f)-1); break
        # x^(p^deg) mod f
        xq = polydivmod(polypow(xq, p, f, p), f, p)[1] if deg > 1 else polydivmod(polypowmod([0,1], p, f, p), f, p)[1]
        g = polygcd(f, polysub(xq, [0,1], p), p)
        if len(g) > 1:
            k = (len(g)-1)//deg
            pat.extend([deg]*k)
            f = polydivmod(f, g, p)[0]
            xq = polydivmod(xq, f, p)[1] if len(f) > 1 else []
    return tuple(sorted(pat, reverse=True))

def polypowmod(base, e, mod, p):
    r = [1]; b = polydivmod(base, mod, p)[1]
    while e:
        if e & 1: r = polydivmod(polymul(r, b, p), mod, p)[1]
        b = polydivmod(polymul(b, b, p), mod, p)[1]; e >>= 1
    return r
def polypow(base, e, mod, p): return polypowmod(base, e, mod, p)

def build(p, a, b, c, cc):
    half = pow(2, p-2, p); eighth = pow(8, p-2, p)
    f6 = [c % p, 0, b % p, 0, a % p, 0, 1]
    q = [0, (a*half) % p, 0, 1]
    e = (b*half - a*a*eighth) % p
    th = (q, [1])
    def mul(u, v):
        return (polyadd(polymul(u[0], v[0], p), polymul(polymul(u[1], v[1], p), f6, p), p),
                polyadd(polymul(u[0], v[1], p), polymul(u[1], v[0], p), p))
    th2 = mul(th, th); th3 = mul(th2, th)
    x1 = [0, 1]; x2 = [0, 0, 1]
    z5 = (polyadd(polymul(x2, th[0], p), polyscal(x1, e, p), p), polymul(x2, th[1], p))
    z7 = (polymul(x1, th2[0], p), polymul(x1, th2[1], p))
    base = [th, z5, z7, th3]
    P1 = []; P2 = []
    for k in range(4):
        if cc[k]:
            P1 = polyadd(P1, polyscal(base[k][0], cc[k], p), p)
            P2 = polyadd(P2, polyscal(base[k][1], cc[k], p), p)
    A = polyadd(P1, [(3*half) % p], p)
    return f6, A, P2

def Nt(p, f6, A, B, t0):
    return polysub(polymul(polysub(A, [t0 % p], p), polysub(A, [t0 % p], p), p),
                   polymul(polymul(B, B, p), f6, p), p)

CANDS = [
    (7,  2, 1, 1, (1, 5, 1, 5)),
    (13, 3, 12, 8, (12, 5, 1, 11)),
    (13, 7, 12, 9, (0, 1, 1, 11)),
    (13, 9, 0, 4, (4, 4, 1, 7)),
    # one decomposable control from each prime (c5=c7=0) -- must be REJECTED
    (7,  0, 0, 1, (4, 0, 0, 2)),
    (13, 2, 1, 2, (7, 0, 0, 2)),
]

for (p, a, b, c, cc) in CANDS:
    print("=== p=%d  (a,b,c)=(%d,%d,%d)  c=(%d,%d,%d,%d) ===" % ((p, a, b, c)+cc))
    f6, A, B = build(p, a, b, c, cc)
    taus = [t for t in range(p) if (t*t-3*t+9) % p == 0]
    # (1) tau-consistency : BOTH tau's must give a perfect cube
    ok = True
    for t0 in taus:
        g = cube_of_cubic(Nt(p, f6, A, B, t0), p)
        print("    tau=%d : N = kappa*g^3 ? %s   g=%s" % (t0, g is not None, g))
        if g is None: ok = False
    # (2) decomposability quick flag
    print("    c5=c7=0 (t is a cubic in theta => decomposable) ? %s" % (cc[1] == 0 and cc[2] == 0))
    # (3) Frobenius cycle types over t0 in F_p \ {branch pts}
    pats = {}
    bad = []
    for t0 in range(p):
        if t0 in taus: continue
        pat = factor_pattern(Nt(p, f6, A, B, t0), p)
        if pat is None: continue
        pats[t0] = pat
        if pat not in ALLOWED: bad.append((t0, pat))
    print("    Frobenius patterns : %s" % sorted(set(pats.values())))
    print("    outside PGammaL(2,8) type list : %s" % (bad if bad else "none"))
    print("    VERDICT: %s" % ("SURVIVES" if (ok and not bad and not (cc[1] == 0 and cc[2] == 0)) else "REJECTED"))
