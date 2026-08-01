# -*- coding: utf-8 -*-
"""
DIV-LAW v1 検算スクリプト(整数演算のみ・単系統・証明ではない cross-check)
封印遵守: n=5 を全検査から除外している。
"""
import io, json, itertools, random
from math import gcd

FAIL = []
def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("  FAIL:", msg)
    return cond

# ---------------------------------------------------------------
# 0. Theta_n モデル: T = { (k,u,eps) } , (k1,u1,e1)*(k2,u2,e2) = (k1+u1k2, u1u2, e1+e2)
# ---------------------------------------------------------------
def units(n):
    return [u for u in range(n) if gcd(u, n) == 1]

def elements(n):
    return [(k, u, e) for k in range(n) for u in units(n) for e in (0, 1)]

def mul(n, a, b):
    return ((a[0] + a[1]*b[0]) % n, (a[1]*b[1]) % n, (a[2]+b[2]) % 2)

def inv(n, a):
    k, u, e = a
    ui = pow(u, -1, n)
    return ((-ui*k) % n, ui, (-e) % 2)

def chi(a):            # chi-tilde  -> (u, eps)  in (Z/n)^x x C2  ~ (Z/4n)^x
    return (a[1], a[2])

IOTA = lambda n: (0, (-1) % n, 1)     # pin  iota = [m=-1, f=1]

def subgroup(n, gens):
    S = {(0, 1, 0)}
    frontier = list(S)
    while frontier:
        new = []
        for a in frontier:
            for g in gens:
                for c in (mul(n, a, g), mul(n, g, a)):
                    if c not in S:
                        S.add(c); new.append(c)
        frontier = new
    return frozenset(S)

def H_std(n, d):       # H_d = { (k,u,e) : k = 0 mod n/d }
    e = n // d
    return frozenset((k, u, ep) for k in range(0, n, e) for u in units(n) for ep in (0, 1))

# ---------------------------------------------------------------
print("=== (A) Theta_n 群公理・chi-tilde・F0 ===")
for n in [3, 7, 9, 11, 15, 21, 25, 27, 33, 45]:
    T = elements(n); Ts = set(T)
    phi = len(units(n))
    check(len(T) == 2*n*phi, f"n={n}: |T|")
    # closure / inverse / identity  (associativity は構成上自動: 半直積)
    ok = all(mul(n, a, b) in Ts for a in T[:40] for b in T[:40])
    check(ok, f"n={n}: closure")
    check(all(mul(n, a, inv(n, a)) == (0, 1, 0) for a in T), f"n={n}: inverse")
    # chi-tilde が準同型・kernel = F0 ~ C_n
    check(all(chi(mul(n, a, b)) == ((a[1]*b[1]) % n, (a[2]+b[2]) % 2)
              for a in T[:60] for b in T[:60]), f"n={n}: chi hom")
    F0 = [a for a in T if chi(a) == (1, 0)]
    check(len(F0) == n and all(a[0] in range(n) for a in F0), f"n={n}: |F0|=n")
    # F0 は正規・共役作用は k -> u k
    check(all(mul(n, mul(n, g, (k, 1, 0)), inv(n, g)) == ((g[1]*k) % n, 1, 0)
              for g in T[:40] for k in range(n)), f"n={n}: F0 conj action = mult by u")
    # pin iota
    io_ = IOTA(n)
    check(mul(n, io_, io_) == (0, 1, 0), f"n={n}: iota^2=1")
    check(chi(io_) == ((-1) % n, 1), f"n={n}: chi(iota)")
print("  (A) done")

# ---------------------------------------------------------------
print("=== (B) H_d は部分群・位数・交叉・左剰余類 = k mod (n/d) の fiber ===")
for n in [3, 7, 9, 15, 21, 25, 27, 45]:
    phi = len(units(n))
    divs = [d for d in range(1, n+1) if n % d == 0]
    for d in divs:
        H = H_std(n, d)
        check(all(mul(n, a, b) in H for a in H for b in H) if len(H) <= 400 else True,
              f"n={n},d={d}: H_d closed")
        check(len(H) == 2*d*phi, f"n={n},d={d}: |H_d|=2 d phi(n)")
        check(IOTA(n) in H, f"n={n},d={d}: iota in H_d")
        check(set(chi(a) for a in H) == set((u, e) for u in units(n) for e in (0, 1)),
              f"n={n},d={d}: chi(H_d) full")
        check(frozenset(a for a in H if chi(a) == (1, 0)) ==
              frozenset((k, 1, 0) for k in range(0, n, n//d)), f"n={n},d={d}: H_d cap F0 = C_d")
    for d1 in divs:
        for d2 in divs:
            check(H_std(n, d1) & H_std(n, d2) == H_std(n, gcd(d1, d2)),
                  f"n={n}: H_{d1} cap H_{d2} = H_gcd")
    # 左剰余類 = { k = k0 mod e }
    for d in divs:
        e = n//d
        H = H_std(n, d)
        for k0 in range(n):
            g = (k0, 1, 0)
            coset = frozenset(mul(n, g, h) for h in H)
            check(coset == frozenset(a for a in elements(n) if a[0] % e == k0 % e),
                  f"n={n},d={d},k0={k0}: 左剰余類 = k mod e の fiber")
print("  (B) done")

# ---------------------------------------------------------------
print("=== (C) 分類定理: chi 全像の部分群 = H_d の F0-共役 (完全列挙) ===")
# 完全性: H が chi 全像なら H = < H cap F0 , (Q の生成系の持上げ) >
def all_full_chi_subgroups(n):
    U = units(n)
    # Q = (Z/n)^x x C2 の生成系
    qgens = []
    # (Z/n)^x の生成系を貪欲に
    cur = {1}
    for u in U:
        if u not in cur:
            qgens.append((u, 0))
            new = set()
            for a in cur:
                v = a
                for _ in range(n):
                    v = (v*u) % n
                    new.add((a*v) % n)
            cur |= new
            cur = {(a*b) % n for a in cur for b in cur} | cur
            # 閉包
            changed = True
            while changed:
                changed = False
                for a in list(cur):
                    for b in list(cur):
                        c = (a*b) % n
                        if c not in cur:
                            cur.add(c); changed = True
        if len(cur) == len(U):
            break
    qgens.append((1, 1))     # C2 成分
    r = len(qgens)
    out = {}
    for d in [d for d in range(1, n+1) if n % d == 0]:
        Cd = [(k, 1, 0) for k in range(0, n, n//d)]
        for lifts in itertools.product(range(n), repeat=r):
            gens = Cd + [(lifts[i], qgens[i][0], qgens[i][1]) for i in range(r)]
            H = subgroup(n, gens)
            F = frozenset(a for a in H if chi(a) == (1, 0))
            if len(set(chi(a) for a in H)) == 2*len(U) and len(F) == d:
                out.setdefault(H, d)
    return out, r

for n in [3, 7, 9, 15, 21]:
    subs, r = all_full_chi_subgroups(n)
    divs = [d for d in range(1, n+1) if n % d == 0]
    # (1) 個数 = sigma(n)
    check(len(subs) == sum(n//d for d in divs), f"n={n}: chi 全像部分群の個数 = sigma(n)={sum(n//d for d in divs)} (実測 {len(subs)})")
    # (2) それぞれ H_d の F0-共役
    for H, d in subs.items():
        conjs = set()
        for k0 in range(n):
            g = (k0, 1, 0)
            conjs.add(frozenset(mul(n, mul(n, g, h), inv(n, g)) for h in H_std(n, d)))
        check(H in conjs, f"n={n},d={d}: H は H_d の F0-共役")
    # (3) iota を含むものはちょうど H_d
    withiota = {H: d for H, d in subs.items() if IOTA(n) in H}
    check(set(withiota.keys()) == set(H_std(n, d) for d in divs),
          f"n={n}: iota を含む chi 全像部分群 = {{H_d}} (各 d にちょうど 1 個)")
    check(len(withiota) == len(divs), f"n={n}: その個数 = 約数個数")
    print(f"  n={n}: chi 全像部分群 {len(subs)} 個 / iota 込 {len(withiota)} 個 / 約数 {len(divs)} 個  OK")

# 独立確認: n=3,9 は全部分群を総当たりして (C) の列挙が漏れていないことを検査
def all_subgroups(n):
    T = elements(n)
    subs = {frozenset({(0, 1, 0)})}
    frontier = list(subs)
    while frontier:
        new = []
        for S in frontier:
            for g in T:
                if g in S:
                    continue
                H = subgroup(n, list(S) + [g])
                if H not in subs:
                    subs.add(H); new.append(H)
        frontier = new
    return subs

for n in [3, 9]:
    allS = all_subgroups(n)
    full = {H for H in allS if len(set(chi(a) for a in H)) == 2*len(units(n))}
    subs, _ = all_full_chi_subgroups(n)
    check(full == set(subs.keys()), f"n={n}: 総当たり列挙と一致 ({len(allS)} 部分群中 {len(full)} 個)")
    print(f"  n={n}: 全部分群 {len(allS)} 個・うち chi 全像 {len(full)} 個 — 一致 OK")
print("  (C) done")

# ---------------------------------------------------------------
print("=== (D) パリティ罠: eps 成分を落とすと d=n から H=T が出ない ===")
for n in [3, 7, 9, 15, 21]:
    Hbad = frozenset((k, u, 0) for k in range(n) for u in units(n))   # Aff(Z/n) x {0}
    check(all(mul(n, a, b) in Hbad for a in Hbad for b in Hbad), f"n={n}: Hbad は部分群")
    F = frozenset(a for a in Hbad if chi(a) == (1, 0))
    check(len(F) == n, f"n={n}: Hbad cap F0 = F0 全体 (d=n)")
    check(len(Hbad) == n*len(units(n)) and len(Hbad)*2 == len(elements(n)),
          f"n={n}: |Hbad| = |T|/2 — d=n でも H != T")
    check(IOTA(n) not in Hbad, f"n={n}: iota not in Hbad (pin がこの罠を殺す)")
    # (Z/2n)^x と (Z/4n)^x の位数差 = 罠の正体
    phi2n = len([u for u in range(2*n) if gcd(u, 2*n) == 1])
    phi4n = len([u for u in range(4*n) if gcd(u, 4*n) == 1])
    check(phi2n == len(units(n)) and phi4n == 2*len(units(n)),
          f"n={n}: phi(2n)=phi(n)={phi2n}, phi(4n)=2phi(n)={phi4n}")
print("  (D) done")

# ---------------------------------------------------------------
print("=== (E) H^1(Q, C_n/C_d) = 0 (直接検算: 全 cocycle が coboundary) ===")
# Q = (Z/n)^x x C2 (C2 は自明作用), A = Z/e.  cocycle は生成元での値で決まる。
def H1_is_zero(n, e):
    U = units(n)
    # Q の全元 (u,eps) を走査、cocycle 条件を満たす関数を全部作るのは高価
    # ⇒ 命題の証明どおり kappa(q) = (1-q) b の形しかないことを、
    #    「2 kappa(q) = (1-q) kappa(z)」(z = 作用 -1 の元)から直接確認する。
    # ここでは Z^1 を線型方程式として全解を求める(A は Z/e 上の加群)。
    Q = [(u, ep) for u in U for ep in (0, 1)]
    idx = {q: i for i, q in enumerate(Q)}
    # 未知数 kappa(q) in Z/e。条件 kappa(q1 q2) = kappa(q1) + u1 kappa(q2)
    # 総当たりは e^|Q| なので、生成元から決まることを使い、全 Z^1 を構成的に列挙:
    sols = []
    # kappa は Q の全元での値。Q は有限アーベル群。全解を Gauss 消去せずに、
    # 「kappa(q)=(1-q)b」型の解 (coboundary) を作り、Z^1 の位数と比較する。
    cob = set()
    for b in range(e):
        cob.add(tuple(((1-u) * b) % e for (u, ep) in Q))
    # Z^1 の位数を数える: kappa は Q の生成元での値で一意に決まる ⇒ 候補を全列挙し
    # cocycle 条件を全対で検査する。
    gens = []
    cur = {(1, 0)}
    for q in Q:
        if q not in cur:
            gens.append(q)
            # 閉包
            changed = True
            cur.add(q)
            while changed:
                changed = False
                for a in list(cur):
                    for b_ in list(cur):
                        c = ((a[0]*b_[0]) % n, (a[1]+b_[1]) % 2)
                        if c not in cur:
                            cur.add(c); changed = True
        if len(cur) == len(Q):
            break
    Z1 = set()
    for vals in itertools.product(range(e), repeat=len(gens)):
        kap = {(1, 0): 0}
        # 生成元から拡張(BFS)
        assign = dict(zip(gens, vals))
        frontier = [(1, 0)]
        ok = True
        while frontier and ok:
            nf = []
            for q in frontier:
                for g in gens:
                    q2 = ((q[0]*g[0]) % n, (q[1]+g[1]) % 2)
                    v = (kap[q] + q[0]*assign[g]) % e
                    if q2 in kap:
                        if kap[q2] != v:
                            ok = False; break
                    else:
                        kap[q2] = v; nf.append(q2)
                if not ok:
                    break
            frontier = nf
        if ok and len(kap) == len(Q):
            # 全対で cocycle 条件を検査
            good = all((kap[((q1[0]*q2[0]) % n, (q1[1]+q2[1]) % 2)] ==
                        (kap[q1] + q1[0]*kap[q2]) % e) for q1 in Q for q2 in Q)
            if good:
                Z1.add(tuple(kap[q] for q in Q))
    return Z1, cob

for n in [3, 7, 9, 15]:
    for d in [d for d in range(1, n+1) if n % d == 0]:
        e = n // d
        if e == 1:
            continue
        Z1, cob = H1_is_zero(n, e)
        check(Z1 == cob, f"n={n},e={e}: Z^1 = B^1 (H^1=0) — |Z1|={len(Z1)}, |B1|={len(cob)}")
        check(len(cob) == e, f"n={n},e={e}: |B^1| = e (A^Q = 0)")
print("  (E) done")

# ---------------------------------------------------------------
print("=== (F) 降下回数の上界 Omega(n) ===")
def Omega(n):
    c, m, p = 0, n, 2
    while m > 1:
        while m % p == 0:
            m //= p; c += 1
        p += 1
    return c
for n in [3, 7, 9, 15, 21, 27, 45, 225, 1155]:
    divs = [d for d in range(1, n+1) if n % d == 0]
    # 真に減少する H_d の鎖の最大長 = 約数鎖の最大長 = Omega(n)
    best = {1: 0}
    for d in sorted(divs):
        best[d] = max([best[dd]+1 for dd in divs if dd < d and d % dd == 0] or [0])
    check(best[n] == Omega(n), f"n={n}: 最長真減少鎖 {best[n]} = Omega(n) {Omega(n)}")
print("  (F) done")

# ---------------------------------------------------------------
print("=== (G) 証明書 K9.v1.json による iota と H_d の実物確認 ===")
d9 = json.load(io.open('C:/Users/81905/Desktop/shadow-atelier/certificates/K9.v1.json', encoding='utf-8'))
sh = d9['shadows']
check(len(sh) == 108, "K9: 108 shadow")
# Theta_9 座標(追補 C.3 と同じ規約: k = f_triple[0][0] / 2 mod 9)
def theta9(s):
    a = s['f_triple'][0]        # [a,e] = r^a s^e ; 期待 e=0, a = 2k
    assert a[1] == 0
    k = (a[0] * pow(2, -1, 9)) % 9
    m = s['m']
    return (k, (2*m+1) % 9, m % 2)
TH = [theta9(s) for s in sh]
check(len(set(TH)) == 108, "K9: Theta_9 単射")
# iota = [m=17, f=1]
iot = [i for i, s in enumerate(sh) if s['m'] == 17 and s['f_word'] == []]
check(len(iot) == 1, "K9: iota = [m=17,f=1] が証明書にちょうど 1 個")
check(TH[iot[0]] == (0, 8, 1), f"K9: Theta_9(iota) = (0,8,1) — 実測 {TH[iot[0]]}")
# 合成表で iota^2 = 1
comp = {(a, b): c for a, b, c in d9['composition_table']}
i0 = iot[0]
check(comp[(i0, i0)] == 0, "K9: 合成表で iota^2 = 単位元 (index 0)")
check(sh[0]['m'] == 0 and sh[0]['f_word'] == [], "K9: index 0 は単位元 [0,1]")
# H_d (d=1,3,9) が証明書の合成表で部分群になっている
for d in [1, 3, 9]:
    e = 9 // d
    idxs = frozenset(i for i in range(108) if TH[i][0] % e == 0)
    check(len(idxs) == 2*d*6, f"K9: |H_{d}| = {2*d*6} (実測 {len(idxs)})")
    check(all(comp[(i, j)] in idxs for i in idxs for j in idxs),
          f"K9: H_{d} は合成表上で閉じている")
    check(i0 in idxs, f"K9: iota in H_{d}")
    check(set((TH[i][1], TH[i][2]) for i in idxs) ==
          set((u, ep) for u in units(9) for ep in (0, 1)), f"K9: chi(H_{d}) 全像")
print("  (G) done")

# ---------------------------------------------------------------
print("=== (H) 補題 PIN の braid 恒等式 (Burau 忠実表現・乱択 t で cross-check) ===")
# 被約 Burau (n=3): sigma1 -> [[-t,1],[0,1]], sigma2 -> [[1,0],[t,-t]]
def mm(A, B, p):
    return [[(A[0][0]*B[0][0]+A[0][1]*B[1][0]) % p, (A[0][0]*B[0][1]+A[0][1]*B[1][1]) % p],
            [(A[1][0]*B[0][0]+A[1][1]*B[1][0]) % p, (A[1][0]*B[0][1]+A[1][1]*B[1][1]) % p]]
def minv(A, p):
    det = (A[0][0]*A[1][1]-A[0][1]*A[1][0]) % p
    di = pow(det, -1, p)
    return [[(A[1][1]*di) % p, (-A[0][1]*di) % p], [(-A[1][0]*di) % p, (A[0][0]*di) % p]]
def word(ws, s1, s2, p):
    R = [[1, 0], [0, 1]]
    for g, k in ws:
        M = s1 if g == 1 else s2
        M = M if k > 0 else minv(M, p)
        for _ in range(abs(k)):
            R = mm(R, M, p)
    return R
p = 1000003
random.seed(20260801)
for _ in range(8):
    t = random.randrange(2, p-1)
    s1 = [[(-t) % p, 1], [0, 1]]
    s2 = [[1, 0], [t % p, (-t) % p]]
    # braid 関係の確認
    check(word([(1,1),(2,1),(1,1)], s1, s2, p) == word([(2,1),(1,1),(2,1)], s1, s2, p),
          f"t={t}: braid 関係")
    D = word([(1,1),(2,1),(1,1)], s1, s2, p)          # Delta
    c = mm(D, D, p)                                    # c = Delta^2
    check(c != [[1,0],[0,1]], f"t={t}: c != 1 (中心だが自明でない)")
    x = word([(1,2)], s1, s2, p); y = word([(2,2)], s1, s2, p)
    # (3.3) m=-1,f=1:  s1^{-1} s2^{-1} = s1 s2 x^{1} c^{-1}
    L = word([(1,-1),(2,-1)], s1, s2, p)
    R = mm(mm(word([(1,1),(2,1)], s1, s2, p), x, p), minv(c, p), p)
    check(L == R, f"t={t}: (3.3) at [m=-1,f=1]")
    # (3.4) m=-1,f=1:  s2^{-1} s1^{-1} = s2 s1 y^{1} c^{-1}
    L2 = word([(2,-1),(1,-1)], s1, s2, p)
    R2 = mm(mm(word([(2,1),(1,1)], s1, s2, p), y, p), minv(c, p), p)
    check(L2 == R2, f"t={t}: (3.4) at [m=-1,f=1]")
print("  (H) done")

# ---------------------------------------------------------------
print("=== (I) N5 control (c != 1 の窓) で iota を確認 ===")
# B3 -> S3 x C5 : s1 -> ((12),t), s2 -> ((23),t)
S3 = list(itertools.permutations(range(3)))
def pmul(a, b): return tuple(a[b[i]] for i in range(3))
def pinv(a):
    r = [0]*3
    for i, v in enumerate(a): r[v] = i
    return tuple(r)
s1p = (1, 0, 2); s2p = (0, 2, 1)
def gmul(a, b): return (pmul(a[0], b[0]), (a[1]+b[1]) % 5)
def ginv(a): return (pinv(a[0]), (-a[1]) % 5)
def gpow(a, k):
    r = ((0,1,2), 0)
    b = a if k >= 0 else ginv(a)
    for _ in range(abs(k)): r = gmul(r, b)
    return r
S1 = (s1p, 1); S2 = (s2p, 1)
X = gpow(S1, 2); Y = gpow(S2, 2)
C = gpow(gmul(gmul(S1, S2), S1), 2)
check(C == (((0,1,2)), 1) or C[0] == (0,1,2), f"N5: c は中心・c={C}")
check(C[1] % 5 != 0, f"N5: ord(c)=5 (c={C})")
# f = 1 の GT-pair 検査: (3.3) s1^{2m+1} s2^{2m+1} = s1 s2 x^{-m} c^m ; (3.4) 同様
good_m = []
for m in range(5):
    u = 2*m+1
    L = gmul(gpow(S1, u), gpow(S2, u))
    R = gmul(gmul(gmul(S1, S2), gpow(X, -m)), gpow(C, m))
    L2 = gmul(gpow(S2, u), gpow(S1, u))
    R2 = gmul(gmul(gmul(S2, S1), gpow(Y, -m)), gpow(C, m))
    if L == R and L2 == R2 and gcd(u, 5) == 1:     # charming: gcd(2m+1, N_ord)=1
        good_m.append(m)
check(good_m == [0, 1, 3, 4], f"N5: f=1 の charming GT-pair の m = {good_m} (定義ノート §4-7 の期待 {{0,1,3,4}})")
check(4 in good_m, "N5: m = -1 (=4 mod 5) が通過 = 補題 PIN の c!=1 窓での確認")
print("  (I) done")

# ---------------------------------------------------------------
print()
print("=" * 60)
print("failures:", len(FAIL))
for f in FAIL:
    print("  -", f)
print("ALL PASS" if not FAIL else "SOME FAILED")
