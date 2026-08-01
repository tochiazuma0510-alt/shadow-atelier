#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detection power of the pentagon (= rho-norm) OVER the hexagon, degree by degree,
in the Malcev/graded setting with lambda = 1 (m = 0).

F2 side: truncated tensor algebra on {x,y}, degrees <= 4.
  (3.10)  f * theta(f) = 1            theta : x<->y            (graded)
  (3.11)  tau^2(f) tau(f) f = 1       tau : x->y->z->x, z=(xy)^-1  (filtered)

Output: for each degree d = 2,3,4, the dimension of
  - Hex(d)  : solutions of (3.10)+(3.11) in gr_d(F2)  (with the lower degrees set to 0)
  - and the explicit generator at d = 4  ->  the DUMMY for the pentagon test.
"""
from fractions import Fraction
from itertools import product

DEG = 4
LET = 2
words = [()]
for d in range(1, DEG + 1):
    words += [w for w in product(range(LET), repeat=d)]
widx = {w: i for i, w in enumerate(words)}
NW = len(words)
Z = lambda: [Fraction(0)] * NW


def mul(A, B):
    C = Z()
    for i, a in enumerate(A):
        if a == 0:
            continue
        wa = words[i]
        for j, b in enumerate(B):
            if b == 0:
                continue
            w = wa + words[j]
            if len(w) <= DEG:
                C[widx[w]] += a * b
    return C


def add(*Xs):
    C = Z()
    for X in Xs:
        for i, a in enumerate(X):
            C[i] += a
    return C


def smul(c, A):
    return [Fraction(c) * a for a in A]


def brk(A, B):
    return add(mul(A, B), smul(-1, mul(B, A)))


ONE = Z(); ONE[widx[()]] = Fraction(1)
X = Z(); X[widx[(0,)]] = Fraction(1)
Y = Z(); Y[widx[(1,)]] = Fraction(1)


def expo(A):                       # A has no constant term
    out, term = ONE[:], ONE[:]
    for k in range(1, DEG + 1):
        term = smul(Fraction(1, k), mul(term, A))
        out = add(out, term)
    return out


def loga(A):                       # A = 1 + (higher)
    U = add(A, smul(-1, ONE))
    out, term = Z(), ONE[:]
    for k in range(1, DEG + 1):
        term = mul(term, U)
        out = add(out, smul(Fraction((-1) ** (k + 1), k), term))
    return out


def inv(A):
    U = add(A, smul(-1, ONE))
    out, term = ONE[:], ONE[:]
    for k in range(1, DEG + 1):
        term = mul(term, U)
        out = add(out, smul(Fraction((-1) ** k), term))
    return out


def subst(A, ix, iy):              # algebra map x->ix, y->iy
    C = Z()
    for i, a in enumerate(A):
        if a == 0:
            continue
        t = ONE[:]
        for l in words[i]:
            t = mul(t, ix if l == 0 else iy)
        C = add(C, smul(a, t))
    return C


ZED = loga(inv(mul(expo(X), expo(Y))))          # z = log((xy)^-1)
theta = lambda A: subst(A, Y, X)
tau = lambda A: subst(A, Y, ZED)

# sanity: tau^3 = id, theta^2 = id, x y z = 1
assert theta(theta(X)) == X and theta(theta(Y)) == Y
assert tau(tau(tau(X))) == X, "tau^3 != id on x"
assert tau(tau(tau(Y))) == Y, "tau^3 != id on y"
prod_xyz = mul(mul(expo(X), expo(Y)), expo(ZED))
assert prod_xyz == ONE, "xyz != 1"
print("setup checks: theta^2=id, tau^3=id, x*y*z=1  -> OK")

A = brk(X, Y)                                    # [x,y]
u1, u2 = brk(A, X), brk(A, Y)                    # gr_3(F2) basis
v1, v2, v3 = brk(u1, X), brk(u1, Y), brk(u2, Y)  # gr_4(F2) basis
# check the Hall relation [[[x,y],y],x] = [[[x,y],x],y]
assert brk(u2, X) == v2, "Hall relation fails"
print("gr_3(F2) rank 2, gr_4(F2) rank 3 basis fixed; Hall relation OK")


def hexagon_defect(F):
    f = expo(F)
    d10 = mul(f, theta(f))
    d11 = mul(mul(tau(tau(f)), tau(f)), f)
    return add(d10, smul(-1, ONE)), add(d11, smul(-1, ONE))


def degpart(V, d):
    return [V[widx[w]] for w in words if len(w) == d]


def solve(basis, deg, offset=None):
    """which combos of `basis` kill both hexagon defects in degree `deg`"""
    rows = []
    n = len(basis)
    cols = []
    for k, B in enumerate(basis):
        a, b = hexagon_defect(B)
        cols.append(degpart(a, deg) + degpart(b, deg))
    off = [Fraction(0)] * len(cols[0])
    if offset is not None:
        a, b = hexagon_defect(offset)
        off = degpart(a, deg) + degpart(b, deg)
    # solve  sum_k c_k * cols[k] + off = 0
    M = [[cols[k][r] for k in range(n)] + [-off[r]] for r in range(len(off))]
    # rref
    piv, r = [], 0
    for c in range(n):
        s = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if s is None:
            continue
        M[r], M[s] = M[s], M[r]
        pv = M[r][c]
        M[r] = [q / pv for q in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                fq = M[i][c]
                M[i] = [p - fq * q for p, q in zip(M[i], M[r])]
        piv.append(c); r += 1
    for row in M[len(piv):]:
        if row[n] != 0:
            return None, None       # inconsistent
    free = [c for c in range(n) if c not in piv]
    part = [Fraction(0)] * n
    for rr, c in enumerate(piv):
        part[c] = M[rr][n]
    kern = []
    for fcol in free:
        v = [Fraction(0)] * n
        v[fcol] = Fraction(1)
        for rr, c in enumerate(piv):
            v[c] = -M[rr][fcol]
        kern.append(v)
    return part, kern


print("\n=== hexagon (lambda = 1, i.e. m = 0), degree by degree ===")
p2, k2 = solve([A], 2)
print("deg 2:  solution space of hexagon in gr_2(F2) (dim 1) -> dim", len(k2),
      "  => c2 = 0 is forced" if len(k2) == 0 else "")
p3, k3 = solve([u1, u2], 3)
print("deg 3:  dim", len(k3), " kernel basis (coeffs of [[x,y],x],[[x,y],y]):",
      [[str(t) for t in v] for v in k3])
p4, k4 = solve([v1, v2, v3], 4)
print("deg 4:  dim", len(k4), " kernel basis (coeffs of v1,v2,v3):",
      [[str(t) for t in v] for v in k4])

print("""
  => DUMMY candidate at depth 4 (satisfies hexagon, to be tested against pentagon):
     psi4 = %s""" % (" + ".join("%s*v%d" % (k4[0][i], i + 1) for i in range(3)) if k4 else "none"))
