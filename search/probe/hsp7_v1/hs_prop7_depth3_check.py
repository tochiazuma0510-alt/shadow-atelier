#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HS Prop 7 translation -- detection power of the rho-norm (= pentagon) test,
computed in the associated graded Lie algebra t_{0,5} = gr(K(0,5)) (x) Q.

Independent second implementation: everything is done inside the TENSOR algebra
T(V) (deg 2 = 25 dim, deg 3 = 125 dim), brackets = commutators.  This re-derives
the depth-2 result of hs_prop7_gr2_check.py (which used Lambda^2 directly) and
extends it to depth 3.

Quantities:
  nu_k(u) := sum_{i=0}^{4} rho^i(u)      (the "rho-norm" in degree k)
  depth 2:  nu_2([T1,T2]) = P (pentagon cycle)   -- expect 0 in t_2  => BLIND
  depth 3:  nu_3([[T1,T2],T1]), nu_3([[T1,T2],T2]) -- expect NONZERO => detector lives here
"""
from fractions import Fraction
from itertools import combinations, product

N = 5
pairs = [frozenset(p) for p in combinations(range(1, N + 1), 2)]

# ---- t_ij expressed in the basis T_k = t_{k,k+1} (from hs_prop7_gr2_check.py) ----
# recomputed here independently by solving the R3 system
def solve_coords():
    T = [frozenset((k, k % N + 1)) for k in range(1, N + 1)]
    Tset = set(T)
    diag = [p for p in pairs if p not in Tset]
    coord = {}
    for k, e in enumerate(T):
        coord[e] = [Fraction(1) if j == k else Fraction(0) for j in range(5)]
    # unknowns: coord[d] for d in diag ; equations R3_i
    n = len(diag)
    didx = {d: k for k, d in enumerate(diag)}
    for comp in range(5):
        A = []
        for i in range(1, N + 1):
            row = [Fraction(0)] * (n + 1)
            for p in pairs:
                if i not in p:
                    continue
                if p in Tset:
                    row[n] -= coord[p][comp]
                else:
                    row[didx[p]] += 1
            A.append(row)
        # gaussian elimination
        r = 0
        piv = []
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
        assert len(piv) == n, "R3 system singular"
        for d in diag:
            coord.setdefault(d, [Fraction(0)] * 5)
        for rr, c in enumerate(piv):
            coord[diag[c]][comp] = A[rr][n]
    return coord


coord = solve_coords()
for i in range(1, N + 1):
    s = [sum((coord[frozenset((i, j))][c] for j in range(1, N + 1) if j != i), Fraction(0))
         for c in range(5)]
    assert all(x == 0 for x in s)
print("R3 solved & re-checked (independent implementation).")

# ---------------- tensor algebra ----------------
D2 = [(a, b) for a in range(5) for b in range(5)]            # 25
D3 = [(a, b, c) for a in range(5) for b in range(5) for c in range(5)]  # 125
i2 = {k: n for n, k in enumerate(D2)}
i3 = {k: n for n, k in enumerate(D3)}


def t1(v):            # v : list of 5 Fractions
    return list(v)


def mul12(u, w):      # deg1 x deg1 -> deg2
    out = [Fraction(0)] * 25
    for a in range(5):
        if u[a] == 0:
            continue
        for b in range(5):
            if w[b] == 0:
                continue
            out[i2[(a, b)]] += u[a] * w[b]
    return out


def mul21(W, u):      # deg2 x deg1 -> deg3
    out = [Fraction(0)] * 125
    for k, (a, b) in enumerate(D2):
        if W[k] == 0:
            continue
        for c in range(5):
            if u[c] == 0:
                continue
            out[i3[(a, b, c)]] += W[k] * u[c]
    return out


def mul12b(u, W):     # deg1 x deg2 -> deg3
    out = [Fraction(0)] * 125
    for c in range(5):
        if u[c] == 0:
            continue
        for k, (a, b) in enumerate(D2):
            if W[k] == 0:
                continue
            out[i3[(c, a, b)]] += u[c] * W[k]
    return out


def br11(u, w):
    A, B = mul12(u, w), mul12(w, u)
    return [x - y for x, y in zip(A, B)]


def br21(W, u):
    A, B = mul21(W, u), mul12b(u, W)
    return [x - y for x, y in zip(A, B)]


def rref(rows, ncols):
    M = [r[:] for r in rows if any(x != 0 for x in r)]
    piv, r = [], 0
    for c in range(ncols):
        s = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if s is None:
            continue
        M[r], M[s] = M[s], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return [row for row in M if any(x != 0 for x in row)], piv


def rank(rows, ncols):
    return len(rref(rows, ncols)[0])


def in_span(rows, tgt, ncols):
    return rank(rows, ncols) == rank(rows + [tgt], ncols)


# ---------------- rho ----------------
# rho(x_{ij}) = x_{i+3,j+3} : on the T-basis  T1->T4->T2->T5->T3->T1
perm = {0: 3, 3: 1, 1: 4, 4: 2, 2: 0}   # index (T_{k+1}) -> index


def rho1(v):
    out = [Fraction(0)] * 5
    for a in range(5):
        out[perm[a]] += v[a]
    return out


# consistency: rho(t_13) must equal t_14
lhs = rho1(coord[frozenset((1, 3))])
rhs = coord[frozenset((1, 4))]
assert lhs == rhs, (lhs, rhs)
print("rho action check: rho(t_13) = t_14  OK")


def rho_deg(vec, deg):
    out = [Fraction(0)] * (5 ** deg)
    idx = D2 if deg == 2 else D3
    ii = i2 if deg == 2 else i3
    for k, key in enumerate(idx):
        if vec[k] == 0:
            continue
        out[ii[tuple(perm[a] for a in key)]] += vec[k]
    return out


def nu(vec, deg):
    tot = [Fraction(0)] * (5 ** deg)
    cur = vec[:]
    for _ in range(5):
        tot = [x + y for x, y in zip(tot, cur)]
        cur = rho_deg(cur, deg)
    assert cur == vec, "rho^5 != id"
    return tot


# ---------------- quadratic relations R of t_{0,5} ----------------
E = [[Fraction(1) if j == k else Fraction(0) for j in range(5)] for k in range(5)]
Rrel, Rlab = [], []
for p, q in combinations(pairs, 2):
    if p & q:
        continue
    Rrel.append(br11(coord[p], coord[q]))
    Rlab.append("R1 %s|%s" % (sorted(p), sorted(q)))
for trip in combinations(range(1, N + 1), 3):
    i, j, k = trip
    for (a, b, c) in [(i, j, k), (i, k, j), (j, k, i)]:
        u = coord[frozenset((a, b))]
        w = [x + y for x, y in zip(coord[frozenset((a, c))], coord[frozenset((b, c))])]
        Rrel.append(br11(u, w))
        Rlab.append("R2 %d%d|%d" % (a, b, c))

lie2 = [br11(E[a], E[b]) for a, b in combinations(range(5), 2)]
print("\ndim Lie_2(V) =", rank(lie2, 25), "(expect 10)")
rR = rref(Rrel, 25)[0]
print("dim R (quadratic relations) =", len(rR), "(expect 6)")
print("dim t_2 = gr_2(K(0,5)) x Q =", rank(lie2, 25) - len(rR), "(expect 4)")

# ---------------- DEPTH 2 : the pentagon cycle ----------------
P = nu(br11(E[0], E[1]), 2)      # nu_2([T1,T2])
print("\n=== depth 2 ===")
print("nu_2([T1,T2]) = P  is zero in t_2 ?  ->", in_span(Rrel, P, 25))
print("control: [T1,T2] itself zero in t_2 ? ->", in_span(Rrel, br11(E[0], E[1]), 25),
      "(expect False)")

# integral certificate for P = sum c_k * rel_k
A = [[Rrel[k][c] for k in range(len(Rrel))] for c in range(25)]
aug = [A[c] + [P[c]] for c in range(25)]
Ar, pv = rref(aug, len(Rrel) + 1)
if len(Rrel) not in pv:
    sol = [Fraction(0)] * len(Rrel)
    for r, c in enumerate(pv):
        sol[c] = Ar[r][len(Rrel)]
    dens = {s.denominator for s in sol}
    print("integral certificate: coefficients have denominators", sorted(dens),
          "=> P is an INTEGRAL combination of the relations" if dens == {1}
          else "=> NOT integral (torsion possible)")
    print("  nonzero coefficients:",
          {Rlab[k]: str(sol[k]) for k in range(len(Rrel)) if sol[k] != 0})

# ---------------- DEPTH 3 ----------------
print("\n=== depth 3 ===")
lie3 = []
for a, b in combinations(range(5), 2):
    for c in range(5):
        lie3.append(br21(br11(E[a], E[b]), E[c]))
print("dim Lie_3(V) =", rank(lie3, 125), "(expect 40)")

ideal3 = [br21(r, E[c]) for r in rR for c in range(5)]
d_id = rank(ideal3, 125)
print("dim [R,V] (degree-3 part of the ideal) =", d_id)
print("dim t_3 = gr_3(K(0,5)) x Q =", rank(lie3, 125) - d_id,
      "(expect 10 = Witt(3,3)+Witt(2,3) = 8+2)")

u1 = br21(br11(E[0], E[1]), E[0])     # [[T1,T2],T1]  = image of [[x,y],x]
u2 = br21(br11(E[0], E[1]), E[1])     # [[T1,T2],T2]  = image of [[x,y],y]
for name, u in (("nu_3([[x,y],x])", u1), ("nu_3([[x,y],y])", u2)):
    v = nu(u, 3)
    z = in_span(ideal3, v, 125)
    print("%-18s is zero in t_3 ? -> %s" % (name, z))

# is some combination nonzero?  compute rank of {nu_3(u1),nu_3(u2)} mod [R,V]
tot = rank(ideal3 + [nu(u1, 3), nu(u2, 3)], 125) - d_id
print("rank of nu_3 on gr_3(F2) (2-dim source), modulo [R,V]  =", tot,
      "  => detection dimension at depth 3")

# which combinations a*[[x,y],x] + b*[[x,y],y] are killed?
for (a, b) in [(1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2)]:
    v = nu([a * x + b * y for x, y in zip(u1, u2)], 3)
    print("   nu_3(%2d*[[x,y],x] + %2d*[[x,y],y]) = 0 ? -> %s"
          % (a, b, in_span(ideal3, v, 125)))
