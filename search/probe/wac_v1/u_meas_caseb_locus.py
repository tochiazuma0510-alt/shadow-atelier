# u_meas_caseb_locus.py -- multi-prime confirmation on the conjectured locus + CRT reconstruction.
#
# From p=7,13 the unique surviving case-(b) candidate satisfies
#     b = a^2/4 ,  c = 8 a^3      (equivalently e = b/2 - a^2/8 = 0 and f6 = q^2 + c, q = x^3 + (a/2)x)
# Here we (i) rescan the LOCUS b=a^2/4, c=8a^3 for many primes with the full schema-v2 sieve,
# (ii) record the x-scaling invariants, (iii) CRT + rational-reconstruct them.
#
# scaling x -> al x :  a -> a/al^2 ,  c_i -> al^i c_i   (i = 3,5,7,9)
# invariants: J_i = c_i^2 a^i ;  K_35 = c_3 c_5 a^4 ; K_37 = c_3 c_7 a^5 ; K_39 = c_3 c_9 a^6
# Raw measurements only.

import sys, time
from math import gcd
exec(open(__file__.replace('locus', 'search2')).read().split('if __name__')[0])

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
        if 2*deg > len(f)-1:
            pat.append(len(f)-1); break
        xq = polypowmod([0, 1], p**deg, f, p)
        g = polygcd(f, polysub(xq, [0, 1], p), p)
        if len(g) > 1:
            pat.extend([deg]*((len(g)-1)//deg))
            f = polydivmod(f, g, p)[0]
    return tuple(sorted(pat, reverse=True))

def scan(p, log):
    half = pow(2, p-2, p); quarter = pow(4, p-2, p); eighth = pow(8, p-2, p)
    taus = [t for t in range(p) if (t*t-3*t+9) % p == 0]
    if not taus: log("p=%d skipped (tau not rational)" % p); return []
    cv = cvectors(p)
    out = []; t0 = time.time()
    for a in range(1, p):
        b = (a*a*quarter) % p; c = (8*a*a*a) % p
        f6 = [c, 0, b, 0, a, 0, 1]
        if len(polygcd(f6, polyder(f6, p), p)) != 1: continue
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
        for cc in cv:
            if cc[1] == 0 and cc[2] == 0: continue     # decomposable branch: t = cubic in theta
            P1 = []; P2 = []
            for k in range(4):
                if cc[k]:
                    P1 = polyadd(P1, polyscal(base[k][0], cc[k], p), p)
                    P2 = polyadd(P2, polyscal(base[k][1], cc[k], p), p)
            A = polyadd(P1, [(3*half) % p], p)
            good = True
            for tv in taus:
                N = polysub(polymul(polysub(A, [tv], p), polysub(A, [tv], p), p),
                            polymul(polymul(P2, P2, p), f6, p), p)
                if cube_of_cubic(N, p) is None: good = False; break
            if not good: continue
            bad = False
            for tv in range(p):
                if tv in taus: continue
                N = polysub(polymul(polysub(A, [tv], p), polysub(A, [tv], p), p),
                            polymul(polymul(P2, P2, p), f6, p), p)
                pat = factor_pattern(N, p)
                if pat is not None and pat not in ALLOWED: bad = True; break
            if bad: continue
            out.append((a, cc))
            log("  p=%d SURVIVOR a=%d c=(%d,%d,%d,%d)" % ((p, a)+cc))
    log("p=%d : %d survivors on the locus  (%.1fs)" % (p, len(out), time.time()-t0))
    return out

def crt(res):
    M = 1; X = 0
    for (r, m) in res:
        g, u = m, 0
        # solve X + M*k = r mod m
        k = ((r - X) * pow(M % m, m-2, m)) % m
        X += M*k; M *= m
    return X % M, M

def ratrec(x, M):
    """rational reconstruction with |num|,|den| <= sqrt(M/2)"""
    import math
    bound = int(math.isqrt(M // 2))
    r0, r1 = M, x % M; s0, s1 = 0, 1
    while r1 > bound:
        qq = r0 // r1
        r0, r1 = r1, r0 - qq*r1
        s0, s1 = s1, s0 - qq*s1
    if s1 == 0 or abs(s1) > bound: return None
    n, d = r1, s1
    if d < 0: n, d = -n, -d
    return (n, d)

if __name__ == "__main__":
    fh = open(sys.argv[1] if len(sys.argv) > 1 else "caseb_locus.log", "w")
    def log(s):
        print(s); fh.write(s+"\n"); fh.flush()
    primes = [int(v) for v in sys.argv[2:]] or [7, 13, 19, 31, 37, 43]
    data = {}
    for p in primes:
        log("=== p = %d ===" % p)
        s = scan(p, log)
        if len(s) == 1:
            a, cc = s[0]
            inv = {}
            inv['J3'] = (cc[0]**2 * pow(a, 3, p)) % p
            inv['J5'] = (cc[1]**2 * pow(a, 5, p)) % p
            inv['J7'] = (cc[2]**2 * pow(a, 7, p)) % p
            inv['J9'] = (cc[3]**2 * pow(a, 9, p)) % p
            inv['K35'] = (cc[0]*cc[1] * pow(a, 4, p)) % p
            inv['K37'] = (cc[0]*cc[2] * pow(a, 5, p)) % p
            inv['K39'] = (cc[0]*cc[3] * pow(a, 6, p)) % p
            data[p] = inv
            log("   invariants: %s" % inv)
        else:
            log("   !! %d survivors -- not usable for reconstruction" % len(s))
    if len(data) >= 2:
        log("\n=== CRT + rational reconstruction ===")
        for key in ['J3', 'J5', 'J7', 'J9', 'K35', 'K37', 'K39']:
            res = [(data[p][key], p) for p in sorted(data)]
            X, M = crt(res)
            rr = ratrec(X, M)
            log("  %-4s : residues %s   ->  %s   (mod %d)" %
                (key, [(p, data[p][key]) for p in sorted(data)],
                 ("%d/%d" % rr if rr else "no small reconstruction"), M))
    fh.close()
