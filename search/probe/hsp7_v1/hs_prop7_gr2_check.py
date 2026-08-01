#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HS Prop 7 translation: depth-2 detection power check.

Question: in gr_2 of K(0,5) (= degree-2 part of the Drinfeld-Kohno Lie algebra t_{0,5}),
is the "pentagon cycle"

    P = T1^T2 + T2^T3 + T3^T4 + T4^T5 + T5^T1     (T_i := t_{i,i+1})

equal to zero?  P is the leading (depth-2) term of the rho-norm
N_rho(f) = rho^4(f) rho^3(f) rho^2(f) rho(f) f  for f in [F2,F2] with c2(f)=1.

If P = 0 then the rho-norm test (= HS condition (III) = pentagon) is
IDENTICALLY BLIND at depth 2, i.e. its first possible detection is at depth >= 3.

Everything is exact rational arithmetic (fractions).
"""
from fractions import Fraction
from itertools import combinations

N = 5
pairs = [frozenset(p) for p in combinations(range(1, N + 1), 2)]  # 10
pidx = {p: k for k, p in enumerate(pairs)}


def vec(d):
    v = [Fraction(0)] * len(pairs)
    for p, c in d.items():
        v[pidx[frozenset(p)]] += Fraction(c)
    return v


def rref(rows, ncols):
    """Return (rref_rows, pivot_cols)."""
    M = [r[:] for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        sel = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
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


def in_span(rows, target, ncols):
    R0, _ = rref(rows, ncols)
    R1, _ = rref(rows + [target], ncols)
    return len(R0) == len(R1)


# ---------- 1. V = span{t_ij} / (sum_{j!=i} t_ij = 0 for each i) ----------
R3 = []
for i in range(1, N + 1):
    R3.append(vec({(i, j): 1 for j in range(1, N + 1) if j != i}))
R3r, _ = rref(R3, len(pairs))
print("dim V =", len(pairs) - len(R3r), "(expect 5); rank of R3 relations =", len(R3r))

# express every t_ij in the basis T_k := t_{k,k+1}, k = 1..5 (indices mod 5)
T = [frozenset((k, k % N + 1)) for k in range(1, N + 1)]  # T[0]={1,2} ... T[4]={5,1}
Tset = set(T)
diag = [p for p in pairs if p not in Tset]
assert len(diag) == 5

# Solve: unknowns = coordinates of each t_ij in T-basis.
# Set up linear system from R3 relations, treating diagonals as unknowns.
# Unknown vector u_d in Q^5 (coords in T basis) for each diagonal d.
# R3 at i:  sum over edges at i of e_T  +  sum over diagonals at i of u_d = 0
rows = []
rhs = []
dvars = {d: k for k, d in enumerate(diag)}
for i in range(1, N + 1):
    edges_at_i = [p for p in pairs if i in p and p in Tset]
    diags_at_i = [p for p in pairs if i in p and p not in Tset]
    for comp in range(5):  # 5 independent components (T-basis coordinates)
        row = [Fraction(0)] * len(diag)
        for d in diags_at_i:
            row[dvars[d]] = Fraction(1)
        b = Fraction(0)
        for e in edges_at_i:
            if T.index(e) == comp:
                b -= 1
        rows.append(row)
        rhs.append(b)

# solve the 5x5 circulant system componentwise
aug = [rows[k] + [rhs[k]] for k in range(len(rows))]
Ar, pv = rref(aug, len(diag) + 1)
sol = {}
# rebuild: solve for each component separately (system is block-diagonal by component)
coord = {}
for comp in range(5):
    A = []
    b = []
    for i in range(1, N + 1):
        diags_at_i = [p for p in pairs if i in p and p not in Tset]
        edges_at_i = [p for p in pairs if i in p and p in Tset]
        row = [Fraction(0)] * len(diag)
        for d in diags_at_i:
            row[dvars[d]] = Fraction(1)
        rr = Fraction(0)
        for e in edges_at_i:
            if T.index(e) == comp:
                rr -= 1
        A.append(row + [rr])
        b.append(rr)
    Ar2, pv2 = rref(A, len(diag) + 1)
    assert len(pv2) == len(diag), ("singular", comp, pv2)
    x = [Fraction(0)] * len(diag)
    for r, c in enumerate(pv2):
        x[c] = Ar2[r][len(diag)]
    for d in diag:
        coord.setdefault(d, [Fraction(0)] * 5)[comp] = x[dvars[d]]

for k, e in enumerate(T):
    coord[e] = [Fraction(1) if j == k else Fraction(0) for j in range(5)]

print("\n-- t_ij in the T-basis --")
for p in pairs:
    print("  t_%s = %s" % ("".join(str(x) for x in sorted(p)),
                           " + ".join("%s*T%d" % (coord[p][j], j + 1)
                                      for j in range(5) if coord[p][j] != 0) or "0"))

# sanity: R3 must hold
for i in range(1, N + 1):
    s = [Fraction(0)] * 5
    for j in range(1, N + 1):
        if j == i:
            continue
        for c in range(5):
            s[c] += coord[frozenset((i, j))][c]
    assert all(x == 0 for x in s), ("R3 fails at", i, s)
print("R3 re-check: OK")

# ---------- 2. Lambda^2 V and the quadratic relations of t_{0,5} ----------
wpairs = list(combinations(range(5), 2))  # 10 basis elements T_a ^ T_b, a<b
widx = {w: k for k, w in enumerate(wpairs)}


def wedge(u, v):
    out = [Fraction(0)] * len(wpairs)
    for a in range(5):
        for b in range(5):
            if a == b or u[a] == 0 or v[b] == 0:
                continue
            if a < b:
                out[widx[(a, b)]] += u[a] * v[b]
            else:
                out[widx[(b, a)]] -= u[a] * v[b]
    return out


rels = []
labels = []
# (R1) disjoint pairs commute
for p, q in combinations(pairs, 2):
    if p & q:
        continue
    rels.append(wedge(coord[p], coord[q]))
    labels.append("R1 %s|%s" % (sorted(p), sorted(q)))
# (R2) [t_ij, t_ik + t_jk] = 0
for trip in combinations(range(1, N + 1), 3):
    i, j, k = trip
    for (a, b, c) in [(i, j, k), (i, k, j), (j, k, i)]:
        u = coord[frozenset((a, b))]
        v = [x + y for x, y in zip(coord[frozenset((a, c))], coord[frozenset((b, c))])]
        rels.append(wedge(u, v))
        labels.append("R2 %d%d|%d" % (a, b, c))

Rr, _ = rref(rels, len(wpairs))
print("\nrank of quadratic relation space in Lambda^2 V =", len(Rr),
      " => dim gr_2(K(0,5)) =", len(wpairs) - len(Rr), "(expect 4 = 3+1 from F3 x| F2)")

# ---------- 3. the pentagon cycle ----------
# careful: T5 ^ T1 has indices (a,b)=(4,0) -> -(T1^T5)
Pv = [Fraction(0)] * len(wpairs)
for k in range(5):
    a, b = k, (k + 1) % 5
    if a < b:
        Pv[widx[(a, b)]] += 1
    else:
        Pv[widx[(b, a)]] -= 1
print("\nP (pentagon cycle) coords in Lambda^2 V basis:",
      {("T%d^T%d" % (a + 1, b + 1)): str(Pv[widx[(a, b)]])
       for (a, b) in wpairs if Pv[widx[(a, b)]] != 0})

print("\n*** P lies in the relation space (i.e. P = 0 in gr_2)? ->",
      in_span(rels, Pv, len(wpairs)))

# control: a non-symmetric element should NOT be in the span (unless gr_2 is 0)
ctrl = [Fraction(0)] * len(wpairs)
ctrl[widx[(0, 1)]] = Fraction(1)  # T1 ^ T2 alone
print("control  T1^T2 in relation space? ->", in_span(rels, ctrl, len(wpairs)),
      "(expect False: c2 itself is NOT killed)")

# control 2: sum over the *diagonal* pentagon
Pv2 = [Fraction(0)] * len(wpairs)
for k in range(5):
    a, b = k, (k + 2) % 5
    if a < b:
        Pv2[widx[(a, b)]] += 1
    else:
        Pv2[widx[(b, a)]] -= 1
print("control  diagonal 5-cycle sum in relation space? ->",
      in_span(rels, Pv2, len(wpairs)))
