# u_meas_caseb_search.py -- case (b) system for the window-B quotient dessin, mod-p search.
#
# Model (derived in docs/notes/u_meas_m3_caseb_v1.md):
#   psibar has 2 fixed points (probe7) => Pbar non-Weierstrass, psibar != iota.
#   Fix(psibar) = {Pbar, iota Pbar} => C : y^2 = f6(x) = x^6 + a x^4 + b x^2 + c   (EVEN sextic)
#   Pbar = infty_+ , psibar(x,y) = (-x,-y) , iota(x,y) = (x,-y) , t(infty_-) = 3/2.
#   t - 3/2 is psibar-ANTI-invariant with polar divisor 9*infty_+ ; the anti-invariant part of
#   L(9 infty_+) has dim 4 with pole orders 3,5,7,9 and basis
#       th   = y + q,        q = x^3 + (a/2) x        (order 3)
#       z5   = x^2 th + e x, e = b/2 - a^2/8          (order 5)
#       z7   = x th^2                                  (order 7)
#       z9   = th^3                                    (order 9)
#   t = 3/2 + c3*th + c5*z5 + c7*z7 + c9*z9  =  A(x) + B(x) y ,  c9 != 0.
#   Branch condition (one suffices; psibar swaps tau1<->tau2):
#       N(x) = (A - tau)^2 - B^2 f6   must be  kappa * g(x)^3  with g cubic,  deg N = 9.
#
# Search: brute force over F_p (p = 1 mod 3 so that tau^2-3tau+9 splits).
# Raw measurements only.

import sys
from itertools import product

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
        v = (A[i] if i < len(A) else 0) + (B[i] if i < len(B) else 0)
        R[i] = v % p
    while R and R[-1] == 0: R.pop()
    return R

def polyscal(A, s, p):
    R = [(s*a) % p for a in A]
    while R and R[-1] == 0: R.pop()
    return R

def polysub(A, B, p): return polyadd(A, polyscal(B, p-1, p), p)

def polydiv(A, B, p):
    A = A[:]; q = [0]*(max(len(A)-len(B)+1, 0))
    inv = pow(B[-1], p-2, p)
    while len(A) >= len(B) and A:
        d = len(A)-len(B); co = (A[-1]*inv) % p; q[d] = co
        for i in range(len(B)):
            A[i+d] = (A[i+d] - co*B[i]) % p
        while A and A[-1] == 0: A.pop()
    while q and q[-1] == 0: q.pop()
    return q, A

def polygcd(A, B, p):
    A = A[:]; B = B[:]
    while B:
        A, B = B, polydiv(A, B, p)[1]
    if A: A = polyscal(A, pow(A[-1], p-2, p), p)
    return A

def polyder(A, p):
    R = [(i*A[i]) % p for i in range(1, len(A))]
    while R and R[-1] == 0: R.pop()
    return R

def is_cube_of_cubic(N, p):
    """N == kappa * g^3 with g monic cubic?  returns g or None"""
    if len(N) != 10: return None            # degree 9
    d = polyder(N, p)
    if not d: return None
    g = polygcd(N, d, p)                    # should be g^2 (deg 6) if g squarefree
    # radical route: rad = N / gcd(N, N')
    quo, rem = polydiv(N, g, p)
    if rem: return None
    if len(quo) != 4: return None           # radical must be the cubic g
    gm = polyscal(quo, pow(quo[-1], p-2, p), p)
    k = (N[-1] * pow(pow(gm[-1], 3, p), p-2, p)) % p
    if polysub(N, polyscal(polymul(polymul(gm, gm, p), gm, p), k, p), p): return None
    return gm

def run(p, verbose=False):
    half = pow(2, p-2, p); quarter = pow(4, p-2, p); eighth = pow(8, p-2, p)
    # tau^2 - 3 tau + 9 = 0
    taus = [t for t in range(p) if (t*t - 3*t + 9) % p == 0]
    if not taus:
        print("p=%d : tau not in F_p, skip" % p); return []
    tau = taus[0]
    hits = []
    for a, b, c in product(range(p), repeat=3):
        f6 = [c % p, 0, b % p, 0, a % p, 0, 1]
        if len(polygcd(f6, polyder(f6, p), p)) != 1: continue   # need squarefree => genus 2
        q  = [0, (a*half) % p, 0, 1]
        e  = (b*half - a*a*eighth) % p
        # theta = y + q ; represent elements as (P1, P2) meaning P1 + P2*y
        th   = (q, [1])
        def mul(u, v):
            P = polyadd(polymul(u[0], v[0], p), polymul(polymul(u[1], v[1], p), f6, p), p)
            Q = polyadd(polymul(u[0], v[1], p), polymul(u[1], v[0], p), p)
            return (P, Q)
        th2 = mul(th, th); th3 = mul(th2, th)
        x   = [0, 1]; x2 = [0, 0, 1]
        z5  = (polyadd(polymul(x2, th[0], p), polyscal(x, e, p), p), polymul(x2, th[1], p))
        z7  = (polymul(x, th2[0], p), polymul(x, th2[1], p))
        z9  = th3
        for c9 in range(1, p):
            for c7, c5, c3 in product(range(p), repeat=3):
                P1 = polyadd(polyadd(polyscal(th[0], c3, p), polyscal(z5[0], c5, p), p),
                             polyadd(polyscal(z7[0], c7, p), polyscal(z9[0], c9, p), p), p)
                P2 = polyadd(polyadd(polyscal(th[1], c3, p), polyscal(z5[1], c5, p), p),
                             polyadd(polyscal(z7[1], c7, p), polyscal(z9[1], c9, p), p), p)
                A = polyadd(P1, [(3*half) % p], p)
                B = P2
                if len(B) != 7: continue                     # deg B must be 6
                N = polysub(polymul(polysub(A, [tau], p), polysub(A, [tau], p), p),
                            polymul(polymul(B, B, p), f6, p), p)
                g = is_cube_of_cubic(N, p)
                if g is not None:
                    hits.append((a, b, c, c3, c5, c7, c9, tuple(g)))
                    if verbose:
                        print("  HIT a,b,c=%s  c3,c5,c7,c9=%s  g=%s" % ((a,b,c),(c3,c5,c7,c9),g))
    return hits

if __name__ == "__main__":
    for p in [7, 13]:
        print("=== p = %d ===" % p)
        h = run(p, verbose=(p == 7))
        print("p=%d : %d hits" % (p, len(h)))
        if p == 13 and h:
            for r in h[:20]: print("   ", r)
