#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
k5_w6_norm_obstruction_check.py
--------------------------------
K5 戦役 W-6 設計ノート (docs/notes/k5_w6_construction_v1.md) の検算。
【K5-GAP-1】の余核公式と、その帰結(elementary-5 核の検出力ゼロ)を確認する。

測るもの: 有限体 F_p 上の線型代数だけ。
  - theta, tau は 2405.11725 (4.7)(4.8) の A 上の作用
  - N_theta(b) = b + theta(b),  N_tau(b) = b + tau(b) + tau^2(b)
  - psi = (N_theta, N_tau) : V -> V^theta (+) V^tau
  - coker(psi) = (V^theta (+) V^tau) / im(psi)

Im R_{N,K^(5)} は一切測らない。証明書も読まない。封印量に触れない。
"""

# ---------------- F_p 線型代数(自前・整数のみ) ----------------

def rref(rows, p):
    """行既約化。rows は list of list。破壊的でない。(rref, rank, pivots) を返す。"""
    M = [r[:] for r in rows]
    if not M:
        return [], 0, []
    ncol = len(M[0])
    piv = []
    r = 0
    for c in range(ncol):
        pr = None
        for i in range(r, len(M)):
            if M[i][c] % p != 0:
                pr = i
                break
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p != 0:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % p for j in range(ncol)]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], r, piv


def rank(rows, p):
    return rref(rows, p)[1]


def matvec(A, v, p):
    return [sum(A[i][j] * v[j] for j in range(len(v))) % p for i in range(len(A))]


def matmul(A, B, p):
    n, m, k = len(A), len(B[0]), len(B)
    return [[sum(A[i][t] * B[t][j] for t in range(k)) % p for j in range(m)] for i in range(n)]


def eye(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def madd(A, B, p):
    return [[(A[i][j] + B[i][j]) % p for j in range(len(A[0]))] for i in range(len(A))]


def msub(A, B, p):
    return [[(A[i][j] - B[i][j]) % p for j in range(len(A[0]))] for i in range(len(A))]


def kernel_basis(A, p):
    """A: n x n(列ベクトルに作用)。ker A の基底(行ベクトルのリスト)。"""
    n = len(A[0])
    R, r, piv = rref(A, p)
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [0] * n
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-R[i][f]) % p
        basis.append(v)
    return basis


def image_basis(A, p):
    """A の像の基底(列空間)。転置の rref。"""
    n, m = len(A), len(A[0])
    cols = [[A[i][j] for i in range(n)] for j in range(m)]
    R, r, _ = rref(cols, p)
    return R


def span_dim(vs, p):
    if not vs:
        return 0
    return rank(vs, p)


def intersect_dim(B1, B2, p, n):
    """2 部分空間(基底 B1,B2)の交わりの次元 = dimB1+dimB2-dim(B1+B2)"""
    d1, d2 = span_dim(B1, p), span_dim(B2, p)
    return d1 + d2 - span_dim(B1 + B2, p)


# ---------------- 余核の計算 ----------------

def norms(th, ta, p):
    n = len(th)
    I = eye(n)
    Nth = madd(I, th, p)
    tau2 = matmul(ta, ta, p)
    Nta = madd(madd(I, ta, p), tau2, p)
    return Nth, Nta


def coker_dim_direct(th, ta, p):
    """
    psi : V -> V^theta (+) V^tau,  b |-> (N_theta b, N_tau b)
    coker = (V^theta (+) V^tau) / im psi   の次元を直接 rank で計算。
    """
    n = len(th)
    I = eye(n)
    Nth, Nta = norms(th, ta, p)
    Vth = kernel_basis(msub(th, I, p), p)      # V^theta
    Vta = kernel_basis(msub(ta, I, p), p)      # V^tau
    dth, dta = span_dim(Vth, p), span_dim(Vta, p)

    # im psi の次元 = rank of the 2n x n stacked map, then read inside V^th (+) V^ta
    # N_theta b は V^theta に、N_tau b は V^tau に入る(確認込み)。
    for b in eye(n):
        u = matvec(Nth, b, p)
        w = matvec(Nta, b, p)
        assert matvec(th, u, p) == u, "N_theta の像が V^theta に入らない"
        assert matvec(ta, w, p) == w, "N_tau の像が V^tau に入らない"

    stacked = [[*matvec(Nth, e, p), *matvec(Nta, e, p)] for e in eye(n)]  # 行 = psi(e_i)
    dim_im = span_dim(stacked, p)
    return dth + dta - dim_im, dth, dta, dim_im


def coker_dim_formula(th, ta, p):
    """master formula: dimV^th + dimV^ta - dimV + dim(ker N_th ∩ ker N_ta)"""
    n = len(th)
    I = eye(n)
    Nth, Nta = norms(th, ta, p)
    Vth = kernel_basis(msub(th, I, p), p)
    Vta = kernel_basis(msub(ta, I, p), p)
    Kth = kernel_basis(Nth, p)
    Kta = kernel_basis(Nta, p)
    return span_dim(Vth, p) + span_dim(Vta, p) - n + intersect_dim(Kth, Kta, p, n)


def coker_dim_short(th, ta, p):
    """short formula: dim V^tau - dim N_tau(ker N_theta)"""
    n = len(th)
    I = eye(n)
    Nth, Nta = norms(th, ta, p)
    Vta = kernel_basis(msub(ta, I, p), p)
    Kth = kernel_basis(Nth, p)
    img = [matvec(Nta, v, p) for v in Kth]
    return span_dim(Vta, p) - span_dim(img, p)


def dual_invariants_dim(th, ta, p):
    """dim (V^*)^Gamma = dim {lam : lam.th = lam, lam.ta = lam}  (転置の不変部分)"""
    n = len(th)
    I = eye(n)
    tht = [[th[j][i] for j in range(n)] for i in range(n)]
    tat = [[ta[j][i] for j in range(n)] for i in range(n)]
    A = msub(tht, I, p) + msub(tat, I, p)   # 行を縦に積む
    return n - rank(A, p)


def gamma_invariants_dim(th, ta, p):
    n = len(th)
    I = eye(n)
    A = msub(th, I, p) + msub(ta, I, p)
    return n - rank(A, p)


# ---------------- 群の生成(⟨theta,tau⟩ の位数) ----------------

def group_order(gens, p):
    n = len(gens[0])
    Id = tuple(tuple(r) for r in eye(n))
    seen = {Id}
    frontier = [eye(n)]
    while frontier:
        nxt = []
        for M in frontier:
            for g in gens:
                P = matmul(M, g, p)
                t = tuple(tuple(r) for r in P)
                if t not in seen:
                    seen.add(t)
                    nxt.append(P)
        frontier = nxt
        if len(seen) > 5000:
            return -1
    return len(seen)


# ---------------- モジュールの構成 ----------------

def A_module(p):
    """2405 (4.7)(4.8): A = <r>^3 の指数座標。theta:(n1,n2,n3)->(n2,n1,-n3), tau:->(n3,n1,n2)"""
    th = [[0, 1, 0], [1, 0, 0], [0, 0, p - 1]]
    ta = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
    return th, ta


def twist(th, ta, p, sth=1, sta=1):
    """1 次指標による捻り。theta -> sth*theta, tau -> sta*tau"""
    n = len(th)
    return ([[(sth * th[i][j]) % p for j in range(n)] for i in range(n)],
            [[(sta * ta[i][j]) % p for j in range(n)] for i in range(n)])


def perm_matrix(perm, n, p):
    """perm: 0-indexed の像リスト。e_i -> e_{perm[i]}"""
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        M[perm[i]][i] = 1
    return M


def std_module_S4(p, thperm, taperm):
    """{x in F_p^4 : sum x = 0} 上の標準 3 次元表現。基底 e1-e2, e2-e3, e3-e4。"""
    P4th = perm_matrix(thperm, 4, p)
    P4ta = perm_matrix(taperm, 4, p)
    basis = [[1, p - 1, 0, 0], [0, 1, p - 1, 0], [0, 0, 1, p - 1]]

    def restrict(P):
        cols = []
        for b in basis:
            img = matvec(P, b, p)
            # img を basis で展開: 座標 (c1,c2,c3) で img = c1*b1+c2*b2+c3*b3
            # b1=(1,-1,0,0), b2=(0,1,-1,0), b3=(0,0,1,-1)
            c1 = img[0] % p
            c2 = (c1 + img[1]) % p
            c3 = (c2 + img[2]) % p
            assert [(c1 * basis[0][k] + c2 * basis[1][k] + c3 * basis[2][k]) % p
                    for k in range(4)] == [x % p for x in img]
            cols.append([c1, c2, c3])
        return [[cols[j][i] for j in range(3)] for i in range(3)]
    return restrict(P4th), restrict(P4ta)


def two_dim_S3(p, sgn_th=1):
    """S3 の 2 次元既約: tau = 位数 3 回転, theta = 位数 2 の鏡映(det=-1)。
       {x in F_p^3 : sum=0} 上の座標置換の制限。"""
    P3ta = perm_matrix([1, 2, 0], 3, p)   # 3-cycle
    P3th = perm_matrix([1, 0, 2], 3, p)   # transposition
    basis = [[1, p - 1, 0], [0, 1, p - 1]]

    def restrict(P):
        cols = []
        for b in basis:
            img = matvec(P, b, p)
            c1 = img[0] % p
            c2 = (c1 + img[1]) % p
            assert [(c1 * basis[0][k] + c2 * basis[1][k]) % p for k in range(3)] == [x % p for x in img]
            cols.append([c1, c2])
        return [[cols[j][i] for j in range(2)] for i in range(2)]
    th, ta = restrict(P3th), restrict(P3ta)
    if sgn_th == -1:
        th = [[(-th[i][j]) % p for j in range(2)] for i in range(2)]
    return th, ta


# ---------------- 検査 ----------------

FAILS = []
def check(name, got, want):
    ok = (got == want)
    if not ok:
        FAILS.append((name, got, want))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got={got} want={want}")


print("=" * 72)
print("A) 2405 (4.7)(4.8) の作用の群論的事実")
print("=" * 72)
for p in (5, 3, 7, 11):
    th, ta = A_module(p)
    n = 3
    check(f"p={p}: theta^2 = I", matmul(th, th, p), eye(n))
    check(f"p={p}: tau^3 = I", matmul(matmul(ta, ta, p), ta, p), eye(n))
    thta = matmul(th, ta, p)
    o4 = matmul(matmul(thta, thta, p), matmul(thta, thta, p), p)
    check(f"p={p}: (theta.tau)^4 = I", o4, eye(n))
    check(f"p={p}: (theta.tau)^2 != I", matmul(thta, thta, p) == eye(n), False)
    check(f"p={p}: |<theta,tau>| = 24 (= S4)", group_order([th, ta], p), 24)

print()
print("=" * 72)
print("B) 余核の 3 通りの計算式が一致するか(全モジュールで)")
print("=" * 72)

cases = []
for p in (5, 3, 2, 7):
    th, ta = A_module(p)
    cases.append((f"A-module (4.7)(4.8)  p={p}", th, ta, p))
    th2, ta2 = twist(th, ta, p, sth=p - 1, sta=1)
    cases.append((f"A-module (x) sgn      p={p}", th2, ta2, p))
    cases.append((f"trivial 1-dim         p={p}", [[1]], [[1]], p))
    cases.append((f"sgn 1-dim (th=-1)     p={p}", [[p - 1]], [[1]], p))
    # S4 標準 3 次元: theta=(12), tau=(134) → (theta.tau) が 4-cycle
    thp = [1, 0, 2, 3]          # (12)
    tap = [2, 1, 3, 0]          # 1->3, 3->4, 4->1  (0-indexed: 0->2,2->3,3->0)
    s3th, s3ta = std_module_S4(p, thp, tap)
    cases.append((f"std3 (S4)             p={p}", s3th, s3ta, p))
    s3thn, s3tan = twist(s3th, s3ta, p, sth=p - 1, sta=1)
    cases.append((f"std3 (x) sgn          p={p}", s3thn, s3tan, p))
    d2th, d2ta = two_dim_S3(p)
    cases.append((f"2-dim (S3)            p={p}", d2th, d2ta, p))

print(f"{'module':<32}{'coker':>7}{'formula':>9}{'short':>7}{'dimV^G':>8}{'dim(V*)^G':>11}")
for name, th, ta, p in cases:
    d_direct, dth, dta, dim_im = coker_dim_direct(th, ta, p)
    d_form = coker_dim_formula(th, ta, p)
    dG = gamma_invariants_dim(th, ta, p)
    dGs = dual_invariants_dim(th, ta, p)
    # short formula は「2 が可逆」(ker N_theta = V^{theta=-1})を使う ⟹ p=2 では適用外
    d_short = coker_dim_short(th, ta, p) if p != 2 else None
    print(f"{name:<32}{d_direct:>7}{d_form:>9}{str(d_short):>7}{dG:>8}{dGs:>11}")
    if d_direct != d_form:
        FAILS.append((name + " master formula", d_form, d_direct))
    if d_short is not None and d_short != d_direct:
        FAILS.append((name + " short formula", d_short, d_direct))

print()
print("=" * 72)
print("C) 主張: 6 が可逆な係数では coker ~ ((V*)^Gamma)*")
print("=" * 72)
for name, th, ta, p in cases:
    if p in (2, 3):
        continue
    d_direct, *_ = coker_dim_direct(th, ta, p)
    dGs = dual_invariants_dim(th, ta, p)
    if d_direct != dGs:
        FAILS.append((name + " coker=dim(V*)^G", d_direct, dGs))
print("  (p=5,7 の全 case で coker = dim (V*)^Gamma を照合)")
check("6 可逆の case で coker = dim(V*)^Gamma がすべて一致",
      not any("coker=dim(V*)^G" in f[0] for f in FAILS), True)

print()
print("=" * 72)
print("D) 本命の帰結: elementary-5 核(次元 3 の両型)は coker = 0")
print("=" * 72)
th5, ta5 = A_module(5)
check("A (= K^(25) の型, std3(x)sgn) over F_5: coker = 0", coker_dim_direct(th5, ta5, 5)[0], 0)
th5t, ta5t = twist(th5, ta5, 5, sth=4, sta=1)
check("A (x) sgn (= rho(x)eps の型) over F_5: coker = 0", coker_dim_direct(th5t, ta5t, 5)[0], 0)
ths, tas = std_module_S4(5, [1, 0, 2, 3], [2, 1, 3, 0])
check("std3(S4) over F_5: coker = 0", coker_dim_direct(ths, tas, 5)[0], 0)
check("trivial over F_5: coker = 1 (⟹ 群は非零・ただし類は K5-MOD-v2(D) で消える)",
      coker_dim_direct([[1]], [[1]], 5)[0], 1)

print()
print("=" * 72)
print("E) WARN-13500 (p=3・S4 標準 3 次元 F_3-加群) の判定")
print("=" * 72)
th3, ta3 = std_module_S4(3, [1, 0, 2, 3], [2, 1, 3, 0])
check("std3(S4) over F_3: coker = 0", coker_dim_direct(th3, ta3, 3)[0], 0)
th3t, ta3t = twist(th3, ta3, 3, sth=2, sta=1)
check("std3(S4) (x) sgn over F_3: coker = 0", coker_dim_direct(th3t, ta3t, 3)[0], 0)
thA, taA = A_module(3)
check("A-model over F_3: coker = 0", coker_dim_direct(thA, taA, 3)[0], 0)

print()
print("=" * 72)
print("F) 検出力が生きる型の実在(p=3: tau が非自由な Jordan ブロック)")
print("=" * 72)
# tau が 2x2 unipotent、theta が対合として作用する 2 次元 F_3-加群
# tau = [[1,1],[0,1]] (order 3 in char 3), theta = [[1,0],[0,-1]]? 要 theta^2=I
th_u = [[1, 0], [0, 2]]
ta_u = [[1, 1], [0, 1]]
p = 3
check("char3 unipotent: theta^2=I", matmul(th_u, th_u, p), eye(2))
check("char3 unipotent: tau^3=I", matmul(matmul(ta_u, ta_u, p), ta_u, p), eye(2))
d, dth, dta, dim_im = coker_dim_direct(th_u, ta_u, p)
check("char3 unipotent 2-dim: coker != 0", d > 0, True)
print(f"    -> dim coker = {d}, dim V^theta = {dth}, dim V^tau = {dta}, dim im psi = {dim_im}")
# 自由 F_3[C_3](regular)は coker 0 を与えるはず(theta は座標反転)
ta_f = perm_matrix([1, 2, 0], 3, 3)
th_f = perm_matrix([1, 0, 2], 3, 3)
check("char3 regular C3 + transposition: tau^3=I", matmul(matmul(ta_f, ta_f, 3), ta_f, 3), eye(3))
d2 = coker_dim_direct(th_f, ta_f, 3)[0]
print(f"    -> F_3[C_3] 正則 + 座標転置: dim coker = {d2}")

print()
print("=" * 72)
print("G) char 2(theta 側の退化)")
print("=" * 72)
th_c2 = [[1, 1], [0, 1]]
ta_c2 = eye(2)
check("char2: theta^2=I", matmul(th_c2, th_c2, 2), eye(2))
d3 = coker_dim_direct(th_c2, ta_c2, 2)[0]
print(f"    -> char2 unipotent theta / tau=1: dim coker = {d3}")
check("char2 unipotent: coker != 0", d3 > 0, True)

print()
print("=" * 72)
print(f"FAILS = {len(FAILS)}")
for f in FAILS:
    print("   ", f)
print("=" * 72)
