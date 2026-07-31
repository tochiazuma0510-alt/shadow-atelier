# u_meas_caseb_sieve19.py -- schema-v2 sieve on the p=19 non-degenerate candidates,
# followed by CRT + rational reconstruction of the x-scaling invariants over p = 7,13,19.
# Raw measurements only.
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'u_meas_caseb_search2.py')).read().split('if __name__')[0])

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
        g = polygcd(f, polysub(xq, [0, 1], p), p)
        if len(g) > 1:
            pat.extend([deg]*((len(g)-1)//deg)); f = polydivmod(f, g, p)[0]
    return tuple(sorted(pat, reverse=True))

def build(p, a, b, c, cc):
    half = pow(2, p-2, p); eighth = pow(8, p-2, p)
    f6 = [c % p, 0, b % p, 0, a % p, 0, 1]
    q = [0, (a*half) % p, 0, 1]; e = (b*half - a*a*eighth) % p
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
    return f6, polyadd(P1, [(3*half) % p], p), P2

def Nt(p, f6, A, B, t0):
    return polysub(polymul(polysub(A, [t0 % p], p), polysub(A, [t0 % p], p), p),
                   polymul(polymul(B, B, p), f6, p), p)

CANDS = [(19, 9, 6, 12, (0, 7, 1, 16)), (19, 12, 11, 12, (0, 0, 1, 4))]
surv = []
for (p, a, b, c, cc) in CANDS:
    print("=== p=%d (a,b,c)=(%d,%d,%d) c=(%d,%d,%d,%d) ===" % ((p, a, b, c)+cc))
    f6, A, B = build(p, a, b, c, cc)
    taus = [t for t in range(p) if (t*t-3*t+9) % p == 0]
    ok = all(cube_of_cubic(Nt(p, f6, A, B, t0), p) is not None for t0 in taus)
    pats = {}; bad = []
    for t0 in range(p):
        if t0 in taus: continue
        pat = factor_pattern(Nt(p, f6, A, B, t0), p)
        if pat is None: continue
        pats[t0] = pat
        if pat not in ALLOWED: bad.append((t0, pat))
    dec = (cc[1] == 0 and cc[2] == 0)
    print("   both-tau cubes: %s   decomposable-branch: %s" % (ok, dec))
    print("   Frobenius patterns: %s" % sorted(set(pats.values())))
    print("   outside PGammaL(2,8): %s" % (bad if bad else "none"))
    v = ok and not bad and not dec
    print("   VERDICT: %s" % ("SURVIVES" if v else "REJECTED"))
    if v: surv.append((p, a, b, c, cc))

DATA = [(7, 2, 1, 1, (1, 5, 1, 5)), (13, 3, 12, 8, (12, 5, 1, 11))] + surv
print("\n=== invariants ===")
inv_all = {}
for (p, a, b, c, cc) in DATA:
    ia = pow(a, p-2, p)
    d = {'I1': (b*pow(ia, 2, p)) % p, 'I2': (c*pow(ia, 3, p)) % p}
    for i, k in zip((3, 5, 7, 9), range(4)): d['J%d' % i] = (cc[k]**2*pow(a, i, p)) % p
    d['K35'] = (cc[0]*cc[1]*pow(a, 4, p)) % p; d['K37'] = (cc[0]*cc[2]*pow(a, 5, p)) % p
    d['K39'] = (cc[0]*cc[3]*pow(a, 6, p)) % p; d['K57'] = (cc[1]*cc[2]*pow(a, 6, p)) % p
    d['K59'] = (cc[1]*cc[3]*pow(a, 7, p)) % p; d['K79'] = (cc[2]*cc[3]*pow(a, 8, p)) % p
    inv_all[p] = d
    onloc = (b == (a*a*pow(4, p-2, p)) % p) and (c == (8*pow(a, 3, p)) % p)
    print(" p=%2d a=%2d : %s  on-locus=%s" % (p, a, d, onloc))

def crt(res):
    M = 1; X = 0
    for (r, m) in res:
        k = ((r-X)*pow(M % m, m-2, m)) % m; X += M*k; M *= m
    return X % M, M

def ratrec(x, M):
    bound = int(math.isqrt(M//2)); r0, r1 = M, x % M; s0, s1 = 0, 1
    while r1 > bound:
        q = r0//r1; r0, r1 = r1, r0-q*r1; s0, s1 = s1, s0-q*s1
    if s1 == 0 or abs(s1) > bound: return None
    n, d = r1, s1
    if d < 0: n, d = -n, -d
    g = math.gcd(abs(n), d) or 1
    return (n//g, d//g)

if len(inv_all) >= 3:
    print("\n=== CRT + rational reconstruction over p = %s ===" % sorted(inv_all))
    for k in ['I1', 'I2', 'J3', 'J5', 'J7', 'J9', 'K35', 'K37', 'K39', 'K57', 'K59', 'K79']:
        res = [(inv_all[p][k], p) for p in sorted(inv_all)]
        X, M = crt(res); rr = ratrec(X, M)
        print("  %-4s %s -> %s (mod %d)" % (k, [(p, inv_all[p][k]) for p in sorted(inv_all)],
              ("%d/%d" % rr if rr else "FAIL"), M))
