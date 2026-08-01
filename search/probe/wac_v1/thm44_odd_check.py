#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thm44_odd_check.py -- 検算(cross-check, NOT a proof, single lane / python only)

目的:
  (A) 2405.11725 Prop 4.1 の「m 偶の場合は読者演習」分岐を、n 奇に限って
      悉皆計算で確認する(手計算 PROP41-EVEN の機械照合)。
      = 条件 (4.4)(4.5) を満たす charming GT-pair 全体を直接列挙し、
        Thm 4.3 (4.12) の記述と一致するかを見る。
  (B) THM44-odd(n,q 奇・n|q での R_{K^(q)},K^(n) の全射性)を、
      (4.12) の座標で直接列挙して確認する。

模型: F_2/K^{(n)}_{F_2} =~ G_n = <x,y> <= D_n^3   (2405 (3.6))
      x = (r, s, s), y = (rs, r, rs), z = (xy)^{-1} = (r^2 s, r^{-1} s, r)
      theta: x->y, y->x        (2405 の theta)
      tau:   x->y, y->z        (2405 の tau; tau(z)=x は xyz=1 から従う)
整数演算のみ。D_n の元は (a,e) = r^a s^e で表す。
"""

from math import gcd
from itertools import product


# ---------- D_n ----------
def dmul(n, p, q):
    a, e = p
    b, f = q
    return ((a + (b if e == 0 else -b)) % n, (e + f) % 2)


def dinv(n, p):
    a, e = p
    return ((-a) % n, 0) if e == 0 else (a % n, 1)


# ---------- G_n <= D_n^3 ----------
def tmul(n, P, Q):
    return tuple(dmul(n, P[i], Q[i]) for i in range(3))


def tinv(n, P):
    return tuple(dinv(n, P[i]) for i in range(3))


def gens(n):
    x = (((1 % n), 0), (0, 1), (0, 1))
    y = (((1 % n), 1), ((1 % n), 0), ((1 % n), 1))
    return x, y


def build_group(n):
    """BFS で G_n を列挙。各元に x,y の語(タプル: 0=x,1=y)を割り当てる。"""
    x, y = gens(n)
    one = ((0, 0), (0, 0), (0, 0))
    word = {one: ()}
    frontier = [one]
    while frontier:
        nxt = []
        for g in frontier:
            for idx, gen in ((0, x), (1, y)):
                h = tmul(n, g, gen)
                if h not in word:
                    word[h] = word[g] + (idx,)
                    nxt.append(h)
        frontier = nxt
    return word


def evaluate(n, w, imx, imy):
    """語 w を imx, imy に代入して評価。"""
    acc = ((0, 0), (0, 0), (0, 0))
    for i in w:
        acc = tmul(n, acc, imx if i == 0 else imy)
    return acc


def make_endo(n, word, imx, imy):
    return {g: evaluate(n, w, imx, imy) for g, w in word.items()}


def check_hom(n, word, phi):
    """phi が準同型であることを 2|G| 回の右乗法で検査(生成系での帰納)。"""
    x, y = gens(n)
    one = ((0, 0), (0, 0), (0, 0))
    if phi[one] != one:
        return False
    for g in word:
        for gen in (x, y):
            if phi[tmul(n, g, gen)] != tmul(n, phi[g], phi[gen]):
                return False
    return True


def commutator_subgroup(n, word):
    """[G,G] を生成元の共役類から BFS で。"""
    els = list(word.keys())
    x, y = gens(n)
    base = set()
    for g in els:
        c = tmul(n, tmul(n, g, tmul(n, x, tmul(n, tinv(n, g), tinv(n, x)))), ((0, 0), (0, 0), (0, 0)))
        base.add(c)
        c2 = tmul(n, g, tmul(n, y, tmul(n, tinv(n, g), tinv(n, y))))
        base.add(c2)
    # 閉包
    sub = {((0, 0), (0, 0), (0, 0))}
    frontier = [((0, 0), (0, 0), (0, 0))]
    base = list(base)
    while frontier:
        nxt = []
        for g in frontier:
            for b in base:
                h = tmul(n, g, b)
                if h not in sub:
                    sub.add(h)
                    nxt.append(h)
        frontier = nxt
    return sub


# ---------- (4.9) kappa, X_n ----------
def kappa(m):
    return m + 1 if m % 2 == 1 else -m


def Xn(n):
    ordK = n if n % 2 == 0 else 2 * n           # K^{(n)}_ord = lcm(n,2)
    return [m for m in range(ordK) if gcd(2 * m + 1, ordK) == 1], ordK


# ---------- 主検査 ----------
def run(n, verbose=True):
    assert n % 2 == 1 and n >= 3
    one = ((0, 0), (0, 0), (0, 0))
    word = build_group(n)
    x, y = gens(n)
    z = tinv(n, tmul(n, x, y))

    theta = make_endo(n, word, y, x)
    tau = make_endo(n, word, y, z)
    ok_hom = check_hom(n, word, theta) and check_hom(n, word, tau)
    ok_tau_z = (tau[z] == x)

    comm = commutator_subgroup(n, word)
    # n 奇 ⟹ [G,G] = <r>^3 (2405 Remark 3.7 (3.8))
    expect_comm = {tuple(((a[i], 0) for i in range(3))) for a in product(range(n), repeat=3)}
    expect_comm = {((a, 0), (b, 0), (c, 0)) for a in range(n) for b in range(n) for c in range(n)}
    ok_comm = (comm == expect_comm)

    xs, ordK = Xn(n)

    # --- 定義どおりの悉皆列挙: (4.4) g*theta(g)=1 かつ (4.5) tau^2(w) tau(w) w = 1, w = y^m g
    found = set()
    ypow = {}
    acc = one
    for m in range(ordK):
        ypow[m] = acc
        acc = tmul(n, acc, y)
    for m in xs:
        ym = ypow[m]
        for g in comm:
            if tmul(n, g, theta[g]) != one:
                continue
            w = tmul(n, ym, g)
            if tmul(n, tau[tau[w]], tmul(n, tau[w], w)) == one:
                found.add((m, g))

    # --- Thm 4.3 (4.12) の予測(4 nmid n 分岐)
    pred = set()
    for m in xs:
        for k in range(n):
            g = (((2 * k) % n, 0), ((-2 * k) % n, 0), (kappa(m) % n, 0))
            pred.add((m, g))

    ok_412 = (found == pred)
    # 偶 m 部分だけの照合(= 読者演習分岐)
    fe = {p for p in found if p[0] % 2 == 0}
    pe = {p for p in pred if p[0] % 2 == 0}
    ok_even = (fe == pe)
    fo = {p for p in found if p[0] % 2 == 1}
    po = {p for p in pred if p[0] % 2 == 1}
    ok_odd = (fo == po)

    if verbose:
        print(f"  n={n}: |G_n|={len(word)} (expect {4*n**3}) "
              f"|[G,G]|={len(comm)} (expect {n**3})  |X_n|={len(xs)} (expect {2*_phi(n)})")
        print(f"    hom(theta,tau)={ok_hom}  tau(z)=x:{ok_tau_z}  [G,G]=<r>^3:{ok_comm}")
        print(f"    |GT(K^(n))| enumerated={len(found)}  predicted={len(pred)} "
              f"(expect {2*n*_phi(n)})")
        print(f"    (4.12) all-m:{ok_412}  odd-m:{ok_odd}  EVEN-m:{ok_even}  <-- 読者演習分岐")
    return dict(n=n, ok_hom=ok_hom, ok_tau_z=ok_tau_z, ok_comm=ok_comm,
                ok_412=ok_412, ok_even=ok_even, ok_odd=ok_odd,
                size=len(found), expect=2 * n * _phi(n), gt=pred)


def _phi(n):
    return sum(1 for i in range(1, n + 1) if gcd(i, n) == 1)


# ---------- THM44-odd: R_{K^(q)},K^(n) の全射性 ----------
def reduction_surjectivity(q, n):
    """(4.12) 座標で R: GT(K^(q)) -> GT(K^(n)) を作り像を数える。n|q, 両者奇。"""
    assert q % 2 == 1 and n % 2 == 1 and q % n == 0
    xq, ordq = Xn(q)
    xn, ordn = Xn(n)
    src = [(m, k) for m in xq for k in range(q)]
    tgt = {(m, k) for m in xn for k in range(n)}
    img = set()
    for (m, k) in src:
        mm = m % ordn          # (3.60): m mod H_ord
        kk = k % n             # f の像: r^{2k} |-> r^{2k mod n}
        # 第3成分の整合(kappa(m) = kappa(mm) mod n)を独立に検査
        assert (kappa(m) - kappa(mm)) % n == 0, (q, n, m)
        img.add((mm, kk))
    return len(img), len(tgt), img == tgt


if __name__ == "__main__":
    print("=== (A) Prop 4.1 の偶 m 分岐(読者演習)の悉皆確認 / n 奇 ===")
    res = [run(n) for n in (3, 5, 7, 9)]
    failsA = [r for r in res if not (r["ok_hom"] and r["ok_tau_z"] and r["ok_comm"]
                                     and r["ok_412"] and r["ok_even"] and r["ok_odd"]
                                     and r["size"] == r["expect"])]
    print(f"  --> failures: {len(failsA)}")

    print()
    print("=== (B) THM44-odd: R_{K^(q)},K^(n) の全射性(n|q, 両者奇) ===")
    failsB = []
    for (q, n) in [(9, 3), (15, 5), (15, 3), (21, 7), (25, 5), (27, 9), (45, 15),
                   (45, 5), (45, 9), (33, 11), (35, 7), (105, 15)]:
        ni, nt, ok = reduction_surjectivity(q, n)
        print(f"  q={q:>3} -> n={n:>2}: |Im|={ni:>4} / |GT(K^(n))|={nt:>4}  surjective={ok}")
        if not ok:
            failsB.append((q, n))
    print(f"  --> failures: {len(failsB)}")

    print()
    print(f"TOTAL FAILURES: {len(failsA) + len(failsB)}")
