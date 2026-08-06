#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""falsifier independent re-derivation for BIT-252.
Free Lie algebra L_n on {x,y} over F_7, with the graded S3-action
  theta: x<->y            (graded, exact)
  tau  : x->y, y->-x-y    (degree-1 part of tau: x->y, y->z=(xy)^-1)
Computes, with NO GAP and no reuse of the driver:
  - dim L_4, dim L_5
  - the hexagon solution space at m=0 in each graded layer:
        (3.10)_gr : (1+theta_*)w = 0
        (3.11)_gr : (1+tau_*+tau_*^2)w = 0
  - checks that the gr_4 solution space is the LINE spanned by v1+4v2+v3
  - S3-isotypic decomposition of gr_4, gr_5
"""
P = 7

def wadd(A, B):
    C = dict(A)
    for k, v in B.items():
        n = (C.get(k, 0) + v) % P
        if n: C[k] = n
        else: C.pop(k, None)
    return C

def wscale(A, s):
    s %= P
    if s == 0: return {}
    return {k: (v * s) % P for k, v in A.items()}

def wmul(A, B):
    C = {}
    for k1, v1 in A.items():
        for k2, v2 in B.items():
            k = k1 + k2
            n = (C.get(k, 0) + v1 * v2) % P
            if n: C[k] = n
            else: C.pop(k, None)
    return C

def bracket(A, B):
    return wadd(wmul(A, B), wscale(wmul(B, A), -1))

X = {"x": 1}
Y = {"y": 1}

# ---- substitution endomorphisms of the free associative algebra -------------
def apply_sub(A, imx, imy):
    out = {}
    for w, c in A.items():
        term = {"": 1}
        for ch in w:
            term = wmul(term, imx if ch == "x" else imy)
        out = wadd(out, wscale(term, c))
    return out

TH_X, TH_Y = Y, X                                   # theta
TA_X, TA_Y = Y, wadd(wscale(X, -1), wscale(Y, -1))  # tau : y -> -x-y

def theta(A): return apply_sub(A, TH_X, TH_Y)
def tau(A):   return apply_sub(A, TA_X, TA_Y)

# ---- build L_n --------------------------------------------------------------
def basis_of(vectors, words):
    """row-reduce; return (rank, list of independent vectors, pivot info)"""
    idx = {w: i for i, w in enumerate(words)}
    rows = []
    for v in vectors:
        r = [0] * len(words)
        for w, c in v.items(): r[idx[w]] = c % P
        rows.append(r)
    # gaussian elimination over F_P
    mat = [r[:] for r in rows]
    piv = []
    rr = 0
    for col in range(len(words)):
        sel = None
        for i in range(rr, len(mat)):
            if mat[i][col] % P: sel = i; break
        if sel is None: continue
        mat[rr], mat[sel] = mat[sel], mat[rr]
        inv = pow(mat[rr][col], P - 2, P)
        mat[rr] = [(a * inv) % P for a in mat[rr]]
        for i in range(len(mat)):
            if i != rr and mat[i][col] % P:
                f = mat[i][col]
                mat[i] = [(a - f * b) % P for a, b in zip(mat[i], mat[rr])]
        piv.append(col); rr += 1
        if rr == len(mat): break
    return rr, mat[:rr], piv

def words_of_len(n):
    out = [""]
    for _ in range(n):
        out = [w + c for w in out for c in "xy"]
    return out

L = {1: [X, Y]}
for n in range(2, 6):
    gen = []
    for a in L[n - 1]:
        for g in (X, Y):
            gen.append(bracket(a, g))
    W = words_of_len(n)
    rk, rows, piv = basis_of(gen, W)
    # turn reduced rows back into dicts
    L[n] = [{W[i]: r[i] for i in range(len(W)) if r[i]} for r in rows]
    print(f"dim L_{n} = {rk}")

# ---- v1,v2,v3 in L_4 --------------------------------------------------------
c_xy = bracket(X, Y)
v1 = bracket(bracket(c_xy, X), X)
v2 = bracket(bracket(c_xy, X), Y)
v3 = bracket(bracket(c_xy, Y), Y)
h4 = wadd(wadd(v1, wscale(v2, 4)), v3)

def coords(vec, basis, words):
    """express vec in terms of `basis` (list of dicts) over F_P; returns list or None"""
    idx = {w: i for i, w in enumerate(words)}
    m = len(basis)
    aug = []
    for w in words:
        row = [b.get(w, 0) % P for b in basis] + [vec.get(w, 0) % P]
        aug.append(row)
    # solve
    rr = 0; piv = []
    for col in range(m):
        sel = None
        for i in range(rr, len(aug)):
            if aug[i][col] % P: sel = i; break
        if sel is None: continue
        aug[rr], aug[sel] = aug[sel], aug[rr]
        inv = pow(aug[rr][col], P - 2, P)
        aug[rr] = [(a * inv) % P for a in aug[rr]]
        for i in range(len(aug)):
            if i != rr and aug[i][col] % P:
                f = aug[i][col]
                aug[i] = [(a - f * b) % P for a, b in zip(aug[i], aug[rr])]
        piv.append(col); rr += 1
    for i in range(rr, len(aug)):
        if aug[i][m] % P: return None
    sol = [0] * m
    for i, col in enumerate(piv): sol[col] = aug[i][m]
    return sol

# ---- per-layer hexagon solution space ---------------------------------------
def analyze(n):
    W = words_of_len(n)
    B = L[n]
    d = len(B)
    # matrices of theta and tau on L_n in basis B
    def mat_of(f):
        cols = []
        for b in B:
            im = f(b)
            c = coords(im, B, W)
            assert c is not None, "image left L_n -- bug"
            cols.append(c)
        return cols  # cols[j][i] = coefficient of B[i] in f(B[j])
    Mth = mat_of(theta); Mta = mat_of(tau)
    def apply_mat(M, v):
        out = [0] * d
        for j in range(d):
            if v[j] % P:
                for i in range(d): out[i] = (out[i] + v[j] * M[j][i]) % P
        return out
    # build the combined condition matrix rows: (1+theta) and (1+tau+tau^2)
    def op_1p_theta(v):
        return [(a + b) % P for a, b in zip(v, apply_mat(Mth, v))]
    def op_N(v):
        t1 = apply_mat(Mta, v); t2 = apply_mat(Mta, t1)
        return [(a + b + c) % P for a, b, c in zip(v, t1, t2)]
    # nullspace of the stacked system
    rowsM = []
    for j in range(d):
        e = [0] * d; e[j] = 1
        rowsM.append(op_1p_theta(e) + op_N(e))   # column j of stacked op
    # rowsM[j] is the image of e_j -> we need nullspace of the map, so build matrix
    # A[i][j] = component i of image of e_j
    A = [[rowsM[j][i] for j in range(d)] for i in range(2 * d)]
    # gaussian elimination to get nullspace dim
    mat = [r[:] for r in A]; rr = 0; piv = []
    for col in range(d):
        sel = None
        for i in range(rr, len(mat)):
            if mat[i][col] % P: sel = i; break
        if sel is None: continue
        mat[rr], mat[sel] = mat[sel], mat[rr]
        inv = pow(mat[rr][col], P - 2, P)
        mat[rr] = [(a * inv) % P for a in mat[rr]]
        for i in range(len(mat)):
            if i != rr and mat[i][col] % P:
                f = mat[i][col]
                mat[i] = [(a - f * b) % P for a, b in zip(mat[i], mat[rr])]
        piv.append(col); rr += 1
    nullity = d - rr
    # also: dim ker(1+theta), dim ker N separately
    def nulldim(op):
        AA = []
        cols = []
        for j in range(d):
            e = [0] * d; e[j] = 1
            cols.append(op(e))
        AA = [[cols[j][i] for j in range(d)] for i in range(d)]
        m2 = [r[:] for r in AA]; r2 = 0
        for col in range(d):
            sel = None
            for i in range(r2, len(m2)):
                if m2[i][col] % P: sel = i; break
            if sel is None: continue
            m2[r2], m2[sel] = m2[sel], m2[r2]
            inv = pow(m2[r2][col], P - 2, P)
            m2[r2] = [(a * inv) % P for a in m2[r2]]
            for i in range(len(m2)):
                if i != r2 and m2[i][col] % P:
                    f = m2[i][col]
                    m2[i] = [(a - f * b) % P for a, b in zip(m2[i], m2[r2])]
            r2 += 1
        return d - r2
    # S3 character -> isotypic multiplicities
    tr_e = d
    tr_th = sum(Mth[j][j] for j in range(d)) % P
    tr_ta = sum(Mta[j][j] for j in range(d)) % P
    # lift traces to integers in (-P/2, P/2] for character arithmetic
    def lift(t): return t - P if t > P // 2 else t
    te, tt, tu = tr_e, lift(tr_th), lift(tr_ta)
    m_triv = (te + 3 * tt + 2 * tu) // 6
    m_sgn = (te - 3 * tt + 2 * tu) // 6
    m_std = (2 * te - 2 * tu) // 6
    return dict(dim=d, nullity_both=nullity, ker_1ptheta=nulldim(op_1p_theta),
                ker_N=nulldim(op_N), tr=(te, tt, tu),
                iso=(m_triv, m_sgn, m_std), Mth=Mth, Mta=Mta, B=B, W=W)

print()
for n in (4, 5):
    r = analyze(n)
    print(f"--- gr_{n} (dim {r['dim']}) ---")
    print(f"  S3 character (e,transposition,3-cycle) = {r['tr']}")
    print(f"  isotypic  trivial:{r['iso'][0]}  sign:{r['iso'][1]}  standard:{r['iso'][2]}")
    print(f"  dim ker(1+theta_*)      = {r['ker_1ptheta']}")
    print(f"  dim ker(1+tau+tau^2)    = {r['ker_N']}")
    print(f"  dim of joint solution space (graded hexagon at m=0) = {r['nullity_both']}"
          f"   => {P}^{r['nullity_both']} = {P**r['nullity_both']} solutions")

# ---- confirm h4 spans the gr_4 solution line --------------------------------
print()
W4 = words_of_len(4); B4 = L[4]
r4 = analyze(4)
def op1(v, M):
    d = len(v); out = [0]*d
    for j in range(d):
        if v[j] % P:
            for i in range(d): out[i] = (out[i] + v[j]*M[j][i]) % P
    return out
h4c = coords(h4, B4, W4)
th_h4 = op1(h4c, r4['Mth'])
t1 = op1(h4c, r4['Mta']); t2 = op1(t1, r4['Mta'])
chk310 = all((a+b) % P == 0 for a, b in zip(h4c, th_h4))
chkN = all((a+b+c) % P == 0 for a, b, c in zip(h4c, t1, t2))
print("h4 = v1 + 4*v2 + v3 :")
print("   (1+theta_*)h4 = 0 ?", chk310, "   (theta_* h4 = -h4 ?)",
      all((a+b) % P == 0 for a, b in zip(h4c, th_h4)))
print("   (1+tau+tau^2)h4 = 0 ?", chkN)
print("   => h4 satisfies the graded hexagon in gr_4  [independent re-derivation of DUM-HEX]")
# enumerate the full gr_4 solution set in the (v1,v2,v3) coordinates
sols = []
for a in range(P):
    for b in range(P):
        for c in range(P):
            w = wadd(wadd(wscale(v1, a), wscale(v2, b)), wscale(v3, c))
            wc = coords(w, B4, W4)
            thw = op1(wc, r4['Mth'])
            u1 = op1(wc, r4['Mta']); u2 = op1(u1, r4['Mta'])
            if all((p+q) % P == 0 for p, q in zip(wc, thw)) and \
               all((p+q+r) % P == 0 for p, q, r in zip(wc, u1, u2)):
                sols.append((a, b, c))
print(f"   gr_4 hexagon solutions in (a,b,c) coords: {len(sols)} -> {sorted(sols)}")
expected = sorted([(t, (4*t) % P, t % P) for t in range(P)])
print(f"   equals the line F7*(1,4,1)? {sorted(sols) == expected}")
print("   [this is the driver's F-7, re-derived with no GAP and no driver code]")
