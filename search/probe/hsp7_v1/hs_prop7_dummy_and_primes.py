#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(1) verify that the depth-4 hexagon generator  psi4 = v1 + 4*v2 + v3  FAILS the
    pentagon (rho-norm), i.e. nu_4(psi4) != 0 in t_4 = gr_4(K(0,5));
(2) modular profile: for which residue characteristics p does the detector die?
(3) is Theta in nu_4(Q*psi4)?
"""
from itertools import combinations
from fractions import Fraction
import sys

sys.setrecursionlimit(10000)
Nn = 5
pairs = [frozenset(p) for p in combinations(range(1, Nn + 1), 2)]
perm = {0: 3, 3: 1, 1: 4, 4: 2, 2: 0}


def solve_coords():
    T = [frozenset((k, k % Nn + 1)) for k in range(1, Nn + 1)]
    Tset = set(T)
    diag = [p for p in pairs if p not in Tset]
    coord = {e: [Fraction(1) if j == k else Fraction(0) for j in range(5)]
             for k, e in enumerate(T)}
    for d in diag:
        coord[d] = [Fraction(0)] * 5
    didx = {d: k for k, d in enumerate(diag)}
    n = len(diag)
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
            A[r] = [q / pv for q in A[r]]
            for i in range(len(A)):
                if i != r and A[i][c] != 0:
                    fq = A[i][c]
                    A[i] = [a - fq * b for a, b in zip(A[i], A[r])]
            piv.append(c); r += 1
        for rr, c in enumerate(piv):
            coord[diag[c]][comp] = A[rr][n]
    return coord


COORD = solve_coords()


def run(p):
    def red(v):
        return [int(x.numerator) % p * pow(int(x.denominator) % p, p - 2, p) % p for x in v]

    coord = {k: red(v) for k, v in COORD.items()}
    E = [[1 if j == k else 0 for j in range(5)] for k in range(5)]

    def mul(u, du, w, dw):
        out = [0] * (5 ** (du + dw))
        m = 5 ** dw
        for i, a in enumerate(u):
            if a:
                base = i * m
                for j, b in enumerate(w):
                    if b:
                        out[base + j] = (out[base + j] + a * b) % p
        return out

    def br(u, du, w, dw):
        return [(x - y) % p for x, y in zip(mul(u, du, w, dw), mul(w, dw, u, du))]

    def rho_apply(v, d):
        out = [0] * (5 ** d)
        for i, a in enumerate(v):
            if not a:
                continue
            key, t = [], i
            for _ in range(d):
                key.append(t % 5); t //= 5
            key.reverse()
            j = 0
            for c in key:
                j = j * 5 + perm[c]
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
            iv = pow(M[r][c], p - 2, p)
            M[r] = [x * iv % p for x in M[r]]
            Mr = M[r]
            for i in range(len(M)):
                if i != r and M[i][c]:
                    f = M[i][c]
                    M[i] = [(a - f * b) % p for a, b in zip(M[i], Mr)]
                piv_ok = True
            piv.append(c); r += 1
            if r == len(M):
                break
        return [row for row in M if any(row)]

    rank = lambda rows, nc: len(rref(rows, nc))

    R = []
    for a, b in combinations(pairs, 2):
        if not (a & b):
            R.append(br(coord[a], 1, coord[b], 1))
    for i, j, k in combinations(range(1, Nn + 1), 3):
        for (a, b, c) in [(i, j, k), (i, k, j), (j, k, i)]:
            u = coord[frozenset((a, b))]
            w = [(x + y) % p for x, y in zip(coord[frozenset((a, c))],
                                             coord[frozenset((b, c))])]
            R.append(br(u, 1, w, 1))
    Rb = rref(R, 25)

    w = br(E[0], 1, E[1], 1)
    u1, u2 = br(w, 2, E[0], 1), br(w, 2, E[1], 1)
    v1, v2, v3 = br(u1, 3, E[0], 1), br(u1, 3, E[1], 1), br(u2, 3, E[1], 1)

    def nu(v, d):
        tot = [0] * (5 ** d); cur = v[:]
        for _ in range(5):
            tot = [(x + y) % p for x, y in zip(tot, cur)]
            cur = rho_apply(cur, d)
        return tot

    I4 = rref([br(br(r, 2, E[c], 1), 3, E[d], 1) for r in Rb
               for c in range(5) for d in range(5)], 625)
    d_I4 = len(I4)
    lie4 = []
    for a, b in combinations(range(5), 2):
        for c in range(5):
            x3 = br(br(E[a], 1, E[b], 1), 2, E[c], 1)
            for d in range(5):
                lie4.append(br(x3, 3, E[d], 1))
    d_lie4 = rank(lie4, 625)

    psi4 = [(x + 4 * y + z) % p for x, y, z in zip(v1, v2, v3)]
    npsi = nu(psi4, 4)
    dead = rank(I4 + [npsi], 625) == d_I4

    # sigma3 = u1 + u2 : must PASS at depth 3
    I3 = rref([br(r, 2, E[c], 1) for r in Rb for c in range(5)], 125)
    s3 = nu([(x + y) % p for x, y in zip(u1, u2)], 3)
    s3_pass = rank(I3 + [s3], 125) == len(I3)

    # Theta
    rw, cur = [], w[:]
    for _ in range(5):
        rw.append(cur); cur = rho_apply(cur, 2)
    Th = [0] * 625
    for i in range(5):
        for j in range(i):
            Th = [(x + y) % p for x, y in zip(Th, br(rw[i], 2, rw[j], 2))]
    if p != 2:
        Th = [x * pow(2, p - 2, p) % p for x in Th]
    th_in_line = rank(I4 + [npsi, Th], 625) == rank(I4 + [npsi], 625)
    th_zero = rank(I4 + [Th], 625) == d_I4
    return dict(dim_R=len(Rb), dim_lie4=d_lie4, dim_I4=d_I4, dim_t4=d_lie4 - d_I4,
                nu4_psi4_is_ZERO=dead, sigma3_passes_pentagon=s3_pass,
                Theta_is_ZERO=th_zero, Theta_in_line_of_nu4_psi4=th_in_line)


for p in [2, 3, 5, 7, 11, 13, 10 ** 9 + 7]:
    print("p = %-12d %s" % (p, run(p)))
