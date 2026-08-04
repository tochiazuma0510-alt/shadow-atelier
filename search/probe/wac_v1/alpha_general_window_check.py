#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
alpha_general_window_check.py

目的: 命題 HF-1(a)(b)(c) と HF-3(a) を *一般 alpha* へ広げた紙の主張
      「窓 H_{2,alpha,0} は alpha != 0 なる全ての alpha で
         |H| = 2n^2 / [G_n:H] = 2n / ord(X) = 2n / <X> cap H = 1 / N_G(H) = H
       を満たす(すなわち (W3)(W4) が alpha 非依存)」
      の *予言* を有限 spot-check する。

格: python 単系統(cross-checked ではない・Lean 検証でもない)。
    紙の証明の根拠ではなく、その予言の spot-check。

宇宙(事前登録・後から変えない):
    n in {3, 7, 9, 11, 13, 15, 21}   (奇数・n=5 は封印遵守で明示除外・非接触)
    alpha in (Z/n) \ {0}             (全て)
    追加で alpha = 0 も走らせ、「N_G(H) != H」(good が壊れる)を確認する
    = 陰性対照(HF-3(a) の逆側)。

模型: G_n = (Z/n)^3 rtimes Q,  Q = {1, q1, q2, q3} = C2 x C2
      q_j は第 j 座標を固定し他の 2 座標を反転(q1 q2 = q3)。
      X = a_1 q_1 = ((1,0,0), q1)
      U_alpha = {(alpha*v, u, v) : u,v in Z/n},  H_{2,alpha,0} = U tsqcup U*q2
"""
import itertools
import json
import sys

# Q の元を符号ベクトルで表す: q_j -> 第 j 座標のみ +1
QSIGNS = {
    0: (1, 1, 1),      # 1
    1: (1, -1, -1),    # q1
    2: (-1, 1, -1),    # q2
    3: (-1, -1, 1),    # q3
}
# Q = C2 x C2 の乗法(符号ベクトルの成分積 -> ラベル)
def qmul(i, j):
    s = tuple(QSIGNS[i][k] * QSIGNS[j][k] for k in range(3))
    for lab, v in QSIGNS.items():
        if v == s:
            return lab
    raise AssertionError("Q is not closed")

def act(q, a, n):
    """q が A = (Z/n)^3 に作用"""
    s = QSIGNS[q]
    return tuple((s[k] * a[k]) % n for k in range(3))

def mul(g, h, n):
    """(a, q) * (b, r) = (a + q.b, q r)"""
    a, q = g
    b, r = h
    return (tuple((a[k] + act(q, b, n)[k]) % n for k in range(3)), qmul(q, r))

def inv(g, n):
    a, q = g
    qi = q  # Q は指数 2 なので自己逆元
    return (tuple((-x) % n for x in act(qi, a, n)), qi)

def window(n, alpha):
    """H_{2,alpha,0} を集合として返す"""
    U = set()
    for u in range(n):
        for v in range(n):
            U.add((((alpha * v) % n, u % n, v % n), 0))
    H = set(U)
    q2 = ((0, 0, 0), 2)
    for g in U:
        H.add(mul(g, q2, n))
    return H, U

def check(n, alpha):
    G = [((a1, a2, a3), q)
         for a1 in range(n) for a2 in range(n) for a3 in range(n)
         for q in range(4)]
    assert len(G) == 4 * n ** 3
    H, U = window(n, alpha)
    # H が部分群であることの確認(閉性・単位元)
    Hgens = [((alpha % n, 0, 1), 0), ((0, 1, 0), 0), ((0, 0, 0), 2)]
    for g in Hgens:
        assert g in H, ("generator not in H", n, alpha, g)
    closed = all(mul(g, h, n) in H for g in Hgens for h in H)
    # X = a_1 q_1
    X = ((1, 0, 0), 1)
    ordX, p = 0, ((0, 0, 0), 0)
    while True:
        p = mul(p, X, n)
        ordX += 1
        if p == ((0, 0, 0), 0):
            break
        if ordX > 8 * n:
            raise AssertionError("ord(X) runaway")
    # <X> cap H
    cyc, p = set(), ((0, 0, 0), 0)
    for _ in range(ordX):
        cyc.add(p)
        p = mul(p, X, n)
    cap = len(cyc & H)
    # N_G(H)  (生成元での判定)
    Nsize = 0
    for g in G:
        gi = inv(g, n)
        if all(mul(mul(g, h, n), gi, n) in H for h in Hgens):
            Nsize += 1
    return {
        "n": n, "alpha": alpha,
        "unit": (pow(alpha, -1, n) is not None) if alpha % n != 0 and __import__("math").gcd(alpha, n) == 1 else False,
        "gcd_alpha_n": __import__("math").gcd(alpha, n) if alpha % n != 0 else n,
        "H_is_subgroup": bool(closed),
        "abs_H": len(H), "exp_abs_H": 2 * n * n,
        "index": (4 * n ** 3) // len(H), "exp_index": 2 * n,
        "ord_X": ordX, "exp_ord_X": 2 * n,
        "cyc_cap_H": cap, "exp_cyc_cap_H": 1,
        "N_eq_H": Nsize == len(H), "N_size": Nsize,
    }

def main():
    UNIVERSE = [3, 7, 9, 11, 13, 15, 21]  # n=5 は封印遵守で除外(非接触)
    assert 5 not in UNIVERSE, "seal discipline: n=5 must not appear"
    rows, fails = [], []
    for n in UNIVERSE:
        for alpha in range(n):
            r = check(n, alpha)
            rows.append(r)
            if alpha % n == 0:
                # 陰性対照: alpha=0 では good が壊れる(N != H)ことを期待
                ok = (r["abs_H"] == r["exp_abs_H"] and r["index"] == r["exp_index"]
                      and r["ord_X"] == r["exp_ord_X"] and r["H_is_subgroup"]
                      and (not r["N_eq_H"]))
                if not ok:
                    fails.append(("alpha0-control", r))
            else:
                ok = (r["H_is_subgroup"] and r["abs_H"] == r["exp_abs_H"]
                      and r["index"] == r["exp_index"] and r["ord_X"] == r["exp_ord_X"]
                      and r["cyc_cap_H"] == 1 and r["N_eq_H"])
                if not ok:
                    fails.append(("alpha-nonzero", r))
    n_nonzero = sum(1 for r in rows if r["alpha"] % r["n"] != 0)
    n_units = sum(1 for r in rows if r["gcd_alpha_n"] == 1)
    print(json.dumps({
        "universe_n": UNIVERSE,
        "cases_total": len(rows),
        "cases_alpha_nonzero": n_nonzero,
        "cases_alpha_unit": n_units,
        "cases_alpha_nonzero_nonunit": n_nonzero - n_units,
        "failures": len(fails),
        "RESULT": "ALL PASS" if not fails else "FAIL",
    }, ensure_ascii=False, indent=2))
    if fails:
        for tag, r in fails[:10]:
            print(tag, r, file=sys.stderr)
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
