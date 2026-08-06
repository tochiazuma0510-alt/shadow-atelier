#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FULLY INDEPENDENT re-derivation of the BIT-252 experiment. No GAP, no ANUPQ,
no reuse of bit252_oneway_main.g or bit252_independent_check.py.

Construction (different from the driver's): the truncated Magnus embedding.
  F2 -> (F_7<X,Y> / deg>=n)^x ,  x |-> 1+X ,  y |-> 1+Y
Its kernel is the n-th Jennings/Zassenhaus dimension subgroup mod 7,
  D_n = gamma_n * gamma_1^7      (since 7*1 = 7 >= n for n <= 7),
so
  n = 5  gives  P  = F2/(gamma_5 F2^7)   (|P|  = 7^8)
  n = 6  gives  P' = F2/(gamma_6 F2^7)   (|P'| = 7^14)
exactly the driver's two windows, built by a completely different route
(ANUPQ p-quotient there, associative truncation here).

theta : x<->y                       -> variable map X|->Y, Y|->X
tau   : x|->y, y|->z=(xy)^-1        -> X|->Y, Y|->((1+X)(1+Y))^-1 - 1
"""
P = 7

def mk(deg_cap):
    cap = deg_cap
    def mul(A, B):
        C = {}
        for w1, c1 in A.items():
            l1 = len(w1)
            for w2, c2 in B.items():
                if l1 + len(w2) > cap:
                    continue
                w = w1 + w2
                v = (C.get(w, 0) + c1 * c2) % P
                if v: C[w] = v
                else: C.pop(w, None)

        return C
    return mul

def add(A, B):
    C = dict(A)
    for k, v in B.items():
        n = (C.get(k, 0) + v) % P
        if n: C[k] = n
        else: C.pop(k, None)
    return C

def scale(A, s):
    s %= P
    if s == 0: return {}
    return {k: (v * s) % P for k, v in A.items()}

def sub(A, B): return add(A, scale(B, -1))

class Alg:
    def __init__(self, cap):
        self.cap = cap
        self.mul = mk(cap)
    def one(self): return {"": 1}
    def prod(self, *els):
        r = self.one()
        for e in els: r = self.mul(r, e)
        return r
    def inv(self, g):
        # g = 1 + u  ->  1 - u + u^2 - ... up to cap
        u = dict(g); u.pop("", None)
        assert g.get("", 0) % P == 1, "not a 1-unit"
        r = self.one(); term = self.one()
        for k in range(1, self.cap + 1):
            term = self.mul(term, u)
            if not term: break
            r = add(r, scale(term, (-1) ** k))
        return r
    def pw(self, g, k):
        if k < 0: return self.pw(self.inv(g), -k)
        r = self.one()
        for _ in range(k): r = self.mul(r, g)
        return r
    def comm(self, a, b):
        # GAP Comm(a,b) = a^-1 b^-1 a b
        return self.prod(self.inv(a), self.inv(b), a, b)
    def subst(self, A, imX, imY):
        out = {}
        for w, c in A.items():
            t = self.one()
            for ch in w:
                t = self.mul(t, imX if ch == "X" else imY)
            out = add(out, scale(t, c))
        return out

def build(cap, label):
    G = Alg(cap)
    x = {"": 1, "X": 1}
    y = {"": 1, "Y": 1}
    imTh_X, imTh_Y = {"Y": 1}, {"X": 1}
    z = G.inv(G.mul(x, y))                 # z = (xy)^-1
    imTa_X = {"Y": 1}                      # X -> Y
    imTa_Y = sub(z, G.one())               # Y -> z - 1
    theta = lambda A: G.subst(A, imTh_X, imTh_Y)
    tau = lambda A: G.subst(A, imTa_X, imTa_Y)
    # sanity
    assert theta(x) == y and theta(y) == x, "theta wrong"
    assert tau(x) == y and tau(y) == z, "tau wrong"
    t3x = tau(tau(tau(x))); t3y = tau(tau(tau(y)))
    print(f"[{label}] cap={cap}  tau^3=id on x,y ? {t3x == x and t3y == y}"
          f"   theta^2=id ? {theta(theta(x)) == x and theta(theta(y)) == y}")
    return G, x, y, theta, tau

# ---------------------------------------------------------------- P  (7^8)
print("=== building P = F2/(gamma_5 F2^7) via truncation deg<=4 ===")
GP, xP, yP, thP, taP = build(4, "P")
# ---------------------------------------------------------------- P' (7^14)
print("=== building P' = F2/(gamma_6 F2^7) via truncation deg<=5 ===")
GQ, xQ, yQ, thQ, taQ = build(5, "P'")

def hexpass(G, theta, tau, ygen, m, f):
    """driver's predicate, re-implemented: (3.10) f*theta(f)=1 and
       (3.11) tau^2(w) tau(w) w = 1 with w = y^m f."""
    if G.mul(f, theta(f)) != G.one(): return False
    w = G.mul(G.pw(ygen, m), f)
    t1 = tau(w); t2 = tau(t1)
    return G.prod(t2, t1, w) == G.one()

def hexpass_rev(G, theta, tau, ygen, m, f):
    if G.mul(f, theta(f)) != G.one(): return False
    w = G.mul(G.pw(ygen, m), f)
    t1 = tau(w); t2 = tau(t1)
    return G.prod(w, t1, t2) == G.one()

def vs(G, x, y):
    c = G.comm(x, y)
    v1 = G.comm(G.comm(c, x), x)
    v2 = G.comm(G.comm(c, x), y)
    v3 = G.comm(G.comm(c, y), y)
    return v1, v2, v3, G.prod(v1, G.pw(v2, 4), v3)

v1P, v2P, v3P, h4P = vs(GP, xP, yP)
v1Q, v2Q, v3Q, h4Q = vs(GQ, xQ, yQ)

print("\n=== R0 calibration, re-derived independently (window P) ===")
res = {}
res["F1"] = hexpass(GP, thP, taP, yP, 0, GP.one())
res["F2"] = hexpass(GP, thP, taP, yP, 6, GP.one())
res["F3"] = sum(hexpass(GP, thP, taP, yP, 0, GP.pw(h4P, t)) for t in range(7))
rP = GP.mul(GP.comm(GP.comm(xP, yP), xP), GP.comm(GP.comm(xP, yP), yP))
res["F4_fails"] = not hexpass(GP, thP, taP, yP, 0, rP)
sP = GP.prod(v1P, v2P, v3P)
res["F5"] = hexpass(GP, thP, taP, yP, 0, GP.mul(rP, GP.inv(sP)))
f7 = [(a, b, c) for a in range(7) for b in range(7) for c in range(7)
      if hexpass(GP, thP, taP, yP, 0,
                 GP.prod(GP.pw(v1P, a), GP.pw(v2P, b), GP.pw(v3P, c)))]
res["F7_count"] = len(f7)
res["F7_line"] = sorted(f7) == sorted([(t, (4 * t) % 7, t) for t in range(7)])
for k, v in res.items(): print(f"  {k:12s} = {v}")
print(f"  F7 solutions = {sorted(f7)}")

print("\n=== SEPARATION: does the calibration detect a W-4 product-order slip? ===")
for name, m, f in [("F1 (m=0,f=1)", 0, GP.one()), ("F2 (m=6,f=1)", 6, GP.one()),
                   ("F3 (m=0,f=h4)", 0, h4P), ("F5 (m=0,f=g1)", 0, GP.mul(rP, GP.inv(sP)))]:
    a = hexpass(GP, thP, taP, yP, m, f); b = hexpass_rev(GP, thP, taP, yP, m, f)
    print(f"  {name:16s} correct-order={a!s:5s} reversed-order={b!s:5s}"
          f"  -> {'DETECTS the slip' if a != b else 'blind to the slip'}")
n_line_rev = len([(a, b, c) for a in range(7) for b in range(7) for c in range(7)
                  if hexpass_rev(GP, thP, taP, yP, 0,
                                 GP.prod(GP.pw(v1P, a), GP.pw(v2P, b), GP.pw(v3P, c)))])
print(f"  F7 sweep         correct-order=7     reversed-order={n_line_rev}"
      f"  -> {'DETECTS' if n_line_rev != 7 else 'BLIND to the slip'}")

print("\n=== POSITIVE CONTROL IN P' (the fixture the run never evaluated) ===")
pc1 = hexpass(GQ, thQ, taQ, yQ, 0, GQ.one())
pc2 = hexpass(GQ, thQ, taQ, yQ, 6, GQ.one())
pc2r = hexpass_rev(GQ, thQ, taQ, yQ, 6, GQ.one())
print(f"  P'-F1 (m=0,f=1) [vacuous]                      : {pc1}")
print(f"  P'-F2 (m=6,f=1) MUST be True (PIN-A identity)  : {pc2}")
print(f"  P'-F2 reversed order [must be False]           : {pc2r}")
print(f"  => the P'-side predicate is alive and order-correct: {pc2 and not pc2r}")

print("\n=== R3: FULL independent fiber sweep (117,649 elements) ===")
# fiber = {h4' * (1+zeta) : zeta in L_5}. degree-5 elements are central and
# (1+z)(1+z')=1+z+z', so f' = h4' + zeta as algebra elements.
# Build a basis of L_5 (free Lie algebra degree 5) from iterated brackets.
def lie_basis():
    def br(a, b): return sub(GQ.mul(a, b), GQ.mul(b, a))
    X = {"X": 1}; Y = {"Y": 1}
    cur = [X, Y]
    for _ in range(4):
        cur = [br(a, g) for a in cur for g in (X, Y)]
    words = []
    def gen(n):
        out = [""]
        for _ in range(n): out = [w + c for w in out for c in "XY"]
        return out
    W = gen(5); idx = {w: i for i, w in enumerate(W)}
    rows = []
    for v in cur:
        r = [0] * len(W)
        for w, c in v.items():
            if len(w) == 5: r[idx[w]] = c % P
        rows.append(r)
    mat = [r[:] for r in rows]; rr = 0; piv = []
    for col in range(len(W)):
        sel = next((i for i in range(rr, len(mat)) if mat[i][col] % P), None)
        if sel is None: continue
        mat[rr], mat[sel] = mat[sel], mat[rr]
        inv = pow(mat[rr][col], P - 2, P)
        mat[rr] = [(a * inv) % P for a in mat[rr]]
        for i in range(len(mat)):
            if i != rr and mat[i][col] % P:
                f = mat[i][col]
                mat[i] = [(a - f * b) % P for a, b in zip(mat[i], mat[rr])]
        piv.append(col); rr += 1
    return [{W[i]: r[i] for i in range(len(W)) if r[i]} for r in mat[:rr]]

B5 = lie_basis()
print(f"  dim L_5 (fiber rank) = {len(B5)}  -> fiber size = 7^{len(B5)} = {7**len(B5)}")
assert len(B5) == 6 and 7 ** len(B5) == 117649

import itertools
survival = 0
survivors = []
for coeffs in itertools.product(range(7), repeat=6):
    zeta = {}
    for c, b in zip(coeffs, B5):
        if c: zeta = add(zeta, scale(b, c))
    fq = add(h4Q, zeta)              # h4' * (1+zeta) = h4' + zeta
    if hexpass(GQ, thQ, taQ, yQ, 0, fq):
        survival += 1
        if len(survivors) < 3: survivors.append(coeffs)
print(f"  SURVIVAL COUNT = {survival} / 117649")
print(f"  cert reports   = 0 / 117649   -> agreement: {survival == 0}")
if survivors: print(f"  survivors (first few, in L_5 coords) = {survivors}")

print("\n=== theory: which counts are even possible? ===")
# linear part: (1+theta) and N=1+tau+tau^2 acting on L_5
def mat_on_L5(f):
    cols = []
    for b in B5:
        im = f(b)
        # express in B5
        W = sorted({w for bb in B5 for w in bb} | set(im))
        aug = []
        for w in W:
            aug.append([bb.get(w, 0) % P for bb in B5] + [im.get(w, 0) % P])
        m = len(B5); rr = 0; piv = []
        for col in range(m):
            sel = next((i for i in range(rr, len(aug)) if aug[i][col] % P), None)
            if sel is None: continue
            aug[rr], aug[sel] = aug[sel], aug[rr]
            inv = pow(aug[rr][col], P - 2, P)
            aug[rr] = [(a * inv) % P for a in aug[rr]]
            for i in range(len(aug)):
                if i != rr and aug[i][col] % P:
                    ff = aug[i][col]
                    aug[i] = [(a - ff * b) % P for a, b in zip(aug[i], aug[rr])]
            piv.append(col); rr += 1
        sol = [0] * m
        for i, col in enumerate(piv): sol[col] = aug[i][m]
        cols.append(sol)
    return cols
Mth5 = mat_on_L5(thQ); Mta5 = mat_on_L5(taQ)
def ap(M, v):
    o = [0] * len(v)
    for j in range(len(v)):
        if v[j] % P:
            for i in range(len(v)): o[i] = (o[i] + v[j] * M[j][i]) % P
    return o
def nullity(op, d=6):
    cols = []
    for j in range(d):
        e = [0] * d; e[j] = 1; cols.append(op(e))
    A = [[cols[j][i] for j in range(d)] for i in range(len(cols[0]))]
    rr = 0
    for col in range(d):
        sel = next((i for i in range(rr, len(A)) if A[i][col] % P), None)
        if sel is None: continue
        A[rr], A[sel] = A[sel], A[rr]
        inv = pow(A[rr][col], P - 2, P)
        A[rr] = [(a * inv) % P for a in A[rr]]
        for i in range(len(A)):
            if i != rr and A[i][col] % P:
                f = A[i][col]
                A[i] = [(a - f * b) % P for a, b in zip(A[i], A[rr])]
        rr += 1
    return d - rr
op_th = lambda v: [(a + b) % P for a, b in zip(v, ap(Mth5, v))]
def op_N(v):
    t1 = ap(Mta5, v); t2 = ap(Mta5, t1)
    return [(a + b + c) % P for a, b, c in zip(v, t1, t2)]
op_both = lambda v: op_th(v) + op_N(v)
d5 = nullity(op_both)
print(f"  d_5 = dim(ker(1+theta_*) cap ker(1+tau+tau^2)) on gr_5 = {d5}")
print(f"  => the ONLY possible outcomes are 0 or 7^{d5} = {7**d5}.")
print(f"  prereg BIT1-P3 registered the allowed set as {{0}} U {{7^k, 0<=k<=6}}"
      f" = {[0] + [7**k for k in range(7)]}")
print(f"  -> BIT1-P3 would have ACCEPTED "
      f"{sorted(set([7**k for k in range(7)]) - {7**d5})} , all theoretically impossible.")
