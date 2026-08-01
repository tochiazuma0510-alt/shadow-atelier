#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HS Prop 7 translation -- depth-4 obstruction of the rho-norm (= pentagon) test.

Setting: t = t_{0,5} = gr(K(0,5)) (x) Q, computed inside the tensor algebra T(V),
V = <T1..T5>, modulo the quadratic relations R of the Drinfeld-Kohno presentation.

For f = exp(F2+F3+F4+...) in the Malcev completion of F2 = <x,y> = <T1,T2>,
BCH for a product of five exponentials gives

  log N_rho(f) = sum_i rho^i(F)  +  1/2 sum_{k<l} [(L_k)_2,(L_l)_2] + (deg >= 5)

with L = (rho^4 f, rho^3 f, rho^2 f, rho f, f).  Hence

  deg 2 :  Omega_2 = c2 * P                       (P = pentagon cycle)
  deg 3 :  Omega_3 = nu_3(F3)
  deg 4 :  Omega_4 = nu_4(F4) + c2^2 * Theta,     Theta := 1/2 sum_{i>j}[rho^i w, rho^j w]

Arithmetic is done modulo two large primes for speed (10^9+7 and 2^31-1);
both avoid 2,3,5 so small torsion cannot cause a false "zero".
"""
from itertools import combinations
from fractions import Fraction

PRIMES = [10 ** 9 + 7, 2 ** 31 - 1]
Nn = 5
pairs = [frozenset(p) for p in combinations(range(1, Nn + 1), 2)]


# ---------- t_ij in the T-basis (exact, then reduced mod p) ----------
def solve_coords():
    T = [frozenset((k, k % Nn + 1)) for k in range(1, Nn + 1)]
    Tset = set(T)
    diag = [p for p in pairs if p not in Tset]
    coord = {e: [Fraction(1) if j == k else Fraction(0) for j in range(5)]
             for k, e in enumerate(T)}
    didx = {d: k for k, d in enumerate(diag)}
    n = len(diag)
    for d in diag:
        coord[d] = [Fraction(0)] * 5
    for comp in range(5):
        A = []
        for i in range(1, Nn + 1):
            row = [Fraction(0)] * (n + 1)
            for p in pairs:
                if i not in p:
                    continue
                if p in Tset:
                    row[n] -= coord[p][comp]
                else:
                    row[didx[p]] += 1
            A.append(row)
        r, piv = 0, []
        for c in range(n):
            s = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
            if s is None:
                continue
            A[r], A[s] = A[s], A[r]
            pv = A[r][c]
            A[r] = [x / pv for x in A[r]]
            for i in range(len(A)):
                if i != r and A[i][c] != 0:
                    fq = A[i][c]
                    A[i] = [a - fq * b for a, b in zip(A[i], A[r])]
            piv.append(c)
            r += 1
        assert len(piv) == n
        for rr, c in enumerate(piv):
            coord[diag[c]][comp] = A[rr][n]
    return coord


COORD = solve_coords()
perm = {0: 3, 3: 1, 1: 4, 4: 2, 2: 0}   # rho on T-indices: T1->T4->T2->T5->T3->T1
assert [x for x in COORD[frozenset((1, 4))]] == \
       [sum((COORD[frozenset((1, 3))][a] for a in range(5) if perm[a] == b), Fraction(0))
        for b in range(5)]


def run(p):
    def red(v):
        return [int(x.numerator % p) * pow(int(x.denominator % p), p - 2, p) % p for x in v]

    coord = {k: red(v) for k, v in COORD.items()}
    E = [[1 if j == k else 0 for j in range(5)] for k in range(5)]

    def mul(u, du, w, dw):
        """u : dict-free dense vector of length 5^du"""
        out = [0] * (5 ** (du + dw))
        m = 5 ** dw
        for i, a in enumerate(u):
            if a == 0:
                continue
            base = i * m
            for j, b in enumerate(w):
                if b:
                    out[base + j] = (out[base + j] + a * b) % p
        return out

    def br(u, du, w, dw):
        A = mul(u, du, w, dw)
        B = mul(w, dw, u, du)
        return [(x - y) % p for x, y in zip(A, B)]

    def rho_apply(v, d):
        out = [0] * (5 ** d)
        for i, a in enumerate(v):
            if a == 0:
                continue
            key = []
            t = i
            for _ in range(d):
                key.append(t % 5)
                t //= 5
            key.reverse()
            nk = [perm[c] for c in key]
            j = 0
            for c in nk:
                j = j * 5 + c
            out[j] = (out[j] + a) % p
        return out

    def rref(rows, nc):
        M = [r[:] for r in rows if any(r)]
        piv, r = [], 0
        for c in range(nc):
            s = next((i for i in range(r, len(M)) if M[i][c]), None)
            if s is None:
                continue
            M[r], M[s] = M[s], M[r]
            inv = pow(M[r][c], p - 2, p)
            M[r] = [x * inv % p for x in M[r]]
            Mr = M[r]
            for i in range(len(M)):
                if i != r and M[i][c]:
                    f = M[i][c]
                    Mi = M[i]
                    M[i] = [(a - f * b) % p for a, b in zip(Mi, Mr)]
            piv.append(c)
            r += 1
            if r == len(M):
                break
        return [row for row in M if any(row)]

    def rank(rows, nc):
        return len(rref(rows, nc))

    # ---- quadratic relations R ----
    R = []
    for a, b in combinations(pairs, 2):
        if a & b:
            continue
        R.append(br(coord[a], 1, coord[b], 1))
    for trip in combinations(range(1, Nn + 1), 3):
        i, j, k = trip
        for (a, b, c) in [(i, j, k), (i, k, j), (j, k, i)]:
            u = coord[frozenset((a, b))]
            w = [(x + y) % p for x, y in zip(coord[frozenset((a, c))],
                                             coord[frozenset((b, c))])]
            R.append(br(u, 1, w, 1))
    Rb = rref(R, 25)
    res = {"dim R": len(Rb)}

    # ---- degree 3 (reproduce the previous script, independent arithmetic) ----
    I3 = [br(r, 2, E[c], 1) for r in Rb for c in range(5)]
    lie3 = [br(br(E[a], 1, E[b], 1), 2, E[c], 1)
            for a, b in combinations(range(5), 2) for c in range(5)]
    d_lie3, d_I3 = rank(lie3, 125), rank(I3, 125)
    res["dim Lie3"], res["dim I3"], res["dim t3"] = d_lie3, d_I3, d_lie3 - d_I3

    w = br(E[0], 1, E[1], 1)             # [T1,T2] = [x,y]

    def nu(v, d):
        tot = [0] * (5 ** d)
        cur = v[:]
        for _ in range(5):
            tot = [(x + y) % p for x, y in zip(tot, cur)]
            cur = rho_apply(cur, d)
        assert cur == v
        return tot

    P = nu(w, 2)
    res["P=0 in t2"] = rank(Rb, 25) == rank(Rb + [P], 25)

    u1 = br(w, 2, E[0], 1)               # [[x,y],x]
    u2 = br(w, 2, E[1], 1)               # [[x,y],y]
    res["nu3 rank"] = rank(I3 + [nu(u1, 3), nu(u2, 3)], 125) - d_I3
    res["nu3(u1+u2)=0"] = rank(I3 + [nu([(x + y) % p for x, y in zip(u1, u2)], 3)],
                               125) == d_I3

    # ---- degree 4 ----
    I4 = [br(br(r, 2, E[c], 1), 3, E[d], 1) for r in Rb for c in range(5) for d in range(5)]
    I4b = rref(I4, 625)
    lie4 = []
    for a, b in combinations(range(5), 2):
        for c in range(5):
            x3 = br(br(E[a], 1, E[b], 1), 2, E[c], 1)
            for d in range(5):
                lie4.append(br(x3, 3, E[d], 1))
    d_lie4, d_I4 = rank(lie4, 625), len(I4b)
    res["dim Lie4"], res["dim I4"], res["dim t4"] = d_lie4, d_I4, d_lie4 - d_I4

    # gr_4(F2) basis  v1=[[[x,y],x],x], v2=[[[x,y],x],y], v3=[[[x,y],y],y]
    v1 = br(u1, 3, E[0], 1)
    v2 = br(u1, 3, E[1], 1)
    v3 = br(u2, 3, E[1], 1)
    nv = [nu(v, 4) for v in (v1, v2, v3)]
    res["nu4 rank on gr4(F2) (dim 3)"] = rank(I4b + nv, 625) - d_I4

    # (3.10) locus at depth 4 :  F4 + theta(F4) = 0  <=>  alpha = gamma
    #  i.e. F4 = alpha*(v1+v3) + beta*v2
    h1 = [(x + y) % p for x, y in zip(nv[0], nv[2])]       # nu4(v1+v3)
    h2 = nv[1]                                            # nu4(v2)
    res["nu4 rank on (3.10)-locus (dim 2)"] = rank(I4b + [h1, h2], 625) - d_I4

    # Theta = 1/2 * sum_{i>j} [rho^i w, rho^j w]
    rw = []
    cur = w[:]
    for i in range(5):
        rw.append(cur)
        cur = rho_apply(cur, 2)
    Th = [0] * 625
    for i in range(5):
        for j in range(5):
            if i > j:
                bb = br(rw[i], 2, rw[j], 2)
                Th = [(x + y) % p for x, y in zip(Th, bb)]
    inv2 = pow(2, p - 2, p)
    Th = [x * inv2 % p for x in Th]
    res["Theta = 0 in t4"] = rank(I4b + [Th], 625) == d_I4
    res["Theta in image(nu4|gr4(F2))"] = rank(I4b + nv + [Th], 625) == rank(I4b + nv, 625)
    res["Theta in image(nu4|(3.10)-locus)"] = \
        rank(I4b + [h1, h2, Th], 625) == rank(I4b + [h1, h2], 625)
    return res


for p in PRIMES:
    print("=== mod p = %d ===" % p)
    r = run(p)
    for k, v in r.items():
        print("   %-38s : %s" % (k, v))
