# u_meas_caseb_search2.py -- case (b) mod-p exhaustive search, v2 (orbit-normalised).
#
# Same system as v1 (see docs/notes/u_meas_m3_caseb_v1.md §2):
#   C : y^2 = x^6 + a x^4 + b x^2 + c   (even sextic, monic), Pbar = infty_+
#   t = 3/2 + c3*th + c5*z5 + c7*z7 + c9*z9,  c9 != 0
#     th = y+q, q = x^3+(a/2)x ; z5 = x^2 th + e x, e = b/2 - a^2/8 ; z7 = x th^2 ; z9 = th^3
#   condition : N(x) = (A-tau)^2 - B^2 f6  =  kappa * g(x)^3 , g monic cubic  (deg N = 9)
#
# v2 changes:
#   * residual scaling x -> alpha x acts by (a,b,c) -> (a/al^2, b/al^4, c/al^6),
#     (c3,c5,c7,c9) -> (al^3 c3, al^5 c5, al^7 c7, al^9 c9).  Since (a,b,c) is scanned
#     exhaustively anyway, we normalise the c-vector: exactly one orbit rep has
#       c7 = 1                          (if c7 != 0 ; al -> al^7 is a bijection when gcd(7,p-1)=1)
#       c7 = 0, c5 = 1                  (if c5 != 0 ; gcd(5,p-1)=1)
#       c7 = c5 = 0, c9 in coset reps   (al^9 acts through the image of al -> al^9)
#   * unbuffered writing to a log file (v1's output was lost to pipe buffering).
# Raw measurements only.

import sys, time

def polymul(A, B, p):
    if not A or not B: return []
    R = [0]*(len(A)+len(B)-1)
    for i, ai in enumerate(A):
        if ai:
            for j, bj in enumerate(B):
                if bj: R[i+j] = (R[i+j] + ai*bj) % p
    while R and R[-1] == 0: R.pop()
    return R

def polyadd(A, B, p):
    n = max(len(A), len(B)); R = [0]*n
    for i in range(n):
        R[i] = ((A[i] if i < len(A) else 0) + (B[i] if i < len(B) else 0)) % p
    while R and R[-1] == 0: R.pop()
    return R

def polyscal(A, s, p):
    if s % p == 0: return []
    R = [(s*a) % p for a in A]
    while R and R[-1] == 0: R.pop()
    return R

def polysub(A, B, p): return polyadd(A, polyscal(B, p-1, p), p)

def polydivmod(A, B, p):
    A = A[:]; q = [0]*max(len(A)-len(B)+1, 0); inv = pow(B[-1], p-2, p)
    while len(A) >= len(B) and A:
        d = len(A)-len(B); co = (A[-1]*inv) % p; q[d] = co
        for i in range(len(B)): A[i+d] = (A[i+d] - co*B[i]) % p
        while A and A[-1] == 0: A.pop()
    while q and q[-1] == 0: q.pop()
    return q, A

def polygcd(A, B, p):
    A = A[:]; B = B[:]
    while B: A, B = B, polydivmod(A, B, p)[1]
    if A: A = polyscal(A, pow(A[-1], p-2, p), p)
    return A

def polyder(A, p):
    R = [(i*A[i]) % p for i in range(1, len(A))]
    while R and R[-1] == 0: R.pop()
    return R

def cube_of_cubic(N, p):
    """N == kappa*g^3 with g monic cubic ? return g or None"""
    if len(N) != 10: return None
    d = polyder(N, p)
    if not d: return None
    G = polygcd(N, d, p)
    if len(G) != 7: return None                 # gcd must be g^2, degree 6
    quo, rem = polydivmod(N, G, p)
    if rem or len(quo) != 4: return None        # radical must be cubic
    gm = polyscal(quo, pow(quo[-1], p-2, p), p)
    k = (N[-1] * pow(pow(gm[-1], 3, p), p-2, p)) % p
    if polysub(N, polyscal(polymul(polymul(gm, gm, p), gm, p), k, p), p): return None
    return gm

def cvectors(p):
    """orbit representatives of (c3,c5,c7,c9), c9 != 0, under (al^3,al^5,al^7,al^9)"""
    out = []
    if (7 % (p-1)) and True:
        pass
    # c7 != 0 branch: normalise c7 = 1 iff al -> al^7 is onto F_p^*  <=> gcd(7,p-1)=1
    import math
    if math.gcd(7, p-1) == 1:
        for c3 in range(p):
            for c5 in range(p):
                for c9 in range(1, p): out.append((c3, c5, 1, c9))
    else:
        for c3 in range(p):
            for c5 in range(p):
                for c7 in range(1, p):
                    for c9 in range(1, p): out.append((c3, c5, c7, c9))
    # c7 = 0
    if math.gcd(5, p-1) == 1:
        for c3 in range(p):
            for c9 in range(1, p): out.append((c3, 1, 0, c9))
    else:
        for c3 in range(p):
            for c5 in range(1, p):
                for c9 in range(1, p): out.append((c3, c5, 0, c9))
    # c7 = c5 = 0 : scale by al^3 and al^9 ; both are al^(3) up to the image subgroup
    img = sorted({pow(al, 9, p) for al in range(1, p)})
    reps = []
    seen = set()
    for c9 in range(1, p):
        if c9 in seen: continue
        orb = {(c9*i) % p for i in img}
        seen |= orb; reps.append(c9)
    for c3 in range(p):
        for c9 in reps: out.append((c3, 0, 0, c9))
    return out

def run(p, log):
    import math
    half = pow(2, p-2, p); eighth = pow(8, p-2, p)
    taus = [t for t in range(p) if (t*t - 3*t + 9) % p == 0]
    if not taus:
        log("p=%d : tau^2-3tau+9 has no root in F_p -- skipped" % p); return []
    tau = taus[0]
    cv = cvectors(p)
    log("p=%d  tau=%s  #c-vectors=%d  total candidates ~ %d" % (p, taus, len(cv), p**3*len(cv)))
    hits = []; t0 = time.time(); ndeg = 0
    for a in range(p):
        for b in range(p):
            for c in range(p):
                f6 = [c, 0, b, 0, a, 0, 1]
                if len(polygcd(f6, polyder(f6, p), p)) != 1: continue
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
                z9 = th3
                base = [th, z5, z7, z9]
                for (c3, c5, c7, c9) in cv:
                    co = (c3, c5, c7, c9)
                    P1 = []; P2 = []
                    for k in range(4):
                        if co[k]:
                            P1 = polyadd(P1, polyscal(base[k][0], co[k], p), p)
                            P2 = polyadd(P2, polyscal(base[k][1], co[k], p), p)
                    A = polyadd(P1, [(3*half) % p], p)
                    N = polysub(polymul(polysub(A, [tau], p), polysub(A, [tau], p), p),
                                polymul(polymul(P2, P2, p), f6, p), p)
                    if len(N) != 10: ndeg += 1; continue
                    g = cube_of_cubic(N, p)
                    if g is not None:
                        hits.append((a, b, c, c3, c5, c7, c9, tuple(g)))
                        log("  HIT (a,b,c)=(%d,%d,%d) (c3,c5,c7,c9)=(%d,%d,%d,%d) g=%s" %
                            (a, b, c, c3, c5, c7, c9, g))
    log("p=%d done in %.1fs : %d hits ; %d candidates had deg N != 9" % (p, time.time()-t0, len(hits), ndeg))
    return hits

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "caseb_search2.log"
    ps = [int(v) for v in sys.argv[2:]] or [7]
    fh = open(path, "w")
    def log(s):
        print(s); fh.write(s+"\n"); fh.flush()
    for p in ps:
        log("=== p = %d ===" % p)
        run(p, log)
    fh.close()
