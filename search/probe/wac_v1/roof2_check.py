#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""roof2_check.py -- M2 := K^(9) cap L (= K^(9) cap N0) の紙の主張の整数検算。
証明ではない cross-check。既存証明書(certificates/*.json)だけを入力とし、
GAP も探索器も走らせない。IF-FIRST 凍結の「実測」には当たらない
(GT(M2) の列挙は一切していない — 検算対象は指数・位数・集合の算術のみ)。
"""
import json, io, sys, os
from math import gcd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def chk(name, got, want):
    ok = (got == want)
    print(("PASS " if ok else "FAIL ") + name + ": got=" + repr(got) + " want=" + repr(want))
    if not ok:
        fails.append(name)

def load(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)

K3 = load("certificates/K3.v1.json")
K9 = load("certificates/K9.v1.json")
L01 = load("certificates/L01.v1.json")

# ---- 1. 証明書からの一次事実 -------------------------------------------------
chk("K3 |GT|", K3["counts"]["hexagon_pass"], 12)
chk("K9 |GT|", K9["counts"]["hexagon_pass"], 108)
chk("L01 |GT|", L01["counts"]["hexagon_pass"], 36)
chk("K3 [PB3:K3]", K3["target"]["invariants"]["index_PB3"], 108)
chk("K9 [PB3:K9]", K9["target"]["invariants"]["index_PB3"], 2916)
chk("K3 N_ord", K3["target"]["invariants"]["N_ord"], 6)
chk("K9 N_ord", K9["target"]["invariants"]["N_ord"], 18)
chk("K3 derived |[G3,G3]|", K3["target"]["invariants"]["derived_order"], 27)
chk("K9 derived |[G9,G9]|", K9["target"]["invariants"]["derived_order"], 729)

# G_n^ab = 4(補題 D0^n の機械側確認)
chk("|G3^ab|", 108 // 27, 4)
chk("|G9^ab|", 2916 // 729, 4)
chk("3 does not divide |G3^ab|", 4 % 3 != 0, True)
chk("3 does not divide |G9^ab|", 4 % 3 != 0, True)

# ---- 2. L subset K^(3) の機械確認(証明書由来) -------------------------------
red_L = [r for r in L01["reduction"] if r["to"] == "K3"]
chk("L01 has reduction->K3 entry (R_{L,K3} が定義されている = L<=K^(3))", len(red_L), 1)
imgL = red_L[0]["image"]
chk("L01 reduction image length = |GT(L)|", len(imgL), 36)
chk("L01 reduction image covers GT(K3) 12/12", sorted(set(imgL)), list(range(12)))
chk("L01 reduction surjective flag", red_L[0]["surjective"], True)
chk("L01 fibre sizes uniform 3", sorted({imgL.count(v) for v in range(12)}), [3])
# 指数の整合: [PB3:L] = |H3| * [PB3:K3]
chk("[PB3:L] = 27 * [PB3:K3]", 27 * 108, 2916)
chk("[B3:L] = 6*2916", 6 * 2916, 17496)

# ---- 3. R_{K9,K3} の全射性・繊維 --------------------------------------------
red_K9 = [r for r in K9["reduction"] if r["to"] == "K3"]
img9 = red_K9[0]["image"]
chk("K9 reduction image length", len(img9), 108)
chk("K9 reduction covers GT(K3) 12/12", sorted(set(img9)), list(range(12)))
chk("K9 fibre sizes uniform 9", sorted({img9.count(v) for v in range(12)}), [9])

# ---- 4. charming 集合 -------------------------------------------------------
def X(nord):
    return [m for m in range(nord) if gcd(2 * m + 1, nord) == 1]
X9, X3, X0 = X(18), X(6), X(3)
chk("X_9 (= X_{M2}, M2_ord=18)", X9, [0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17])
chk("|X_9|", len(X9), 12)
chk("X_3 (= X_L, L_ord=6)", X3, [0, 2, 3, 5])
chk("X_{N0} (N0_ord=3)", X0, [0, 2])
chk("X_9 mod 3 subset X_{N0}  [(MCOV) の前件]", sorted({m % 3 for m in X9}), [0, 2])
chk("X_3 mod 3 = X_{N0}", sorted({m % 3 for m in X3}), [0, 2])
chk("X_9 mod 6 = X_3", sorted({m % 6 for m in X9}), X3)
chk("m=1 mod 3 は charming が排除(補題 C.3)", [m for m in X9 if m % 3 == 1], [])

# ---- 5. M2 の位数の三通りの数え方 --------------------------------------------
# (a) 分裂表示 (K9, N0): |PB3/M2| = |G9| * |H3|
a = 2916 * 27
# (b) entangled 表示 (K9, L): |G9| * |PB3/L| / |E0|,  E0 = G3
b = 2916 * 2916 // 108
chk("|PB3/M2| 二表示一致", (a, b), (78732, 78732))
chk("|PB3/M2| = 4*3^9", 4 * 3 ** 9, 78732)
chk("[B3:M2]", 6 * 78732, 472392)
chk("|E0| = |G3|", 108, 2916 * 2916 // 78732)
chk("|E| = |B3/K^(3)|", 6 * 108, 648)

# |GT(M2)| = 324 を 4 通りで
g1 = 3 * 108                        # 中心持ち上げ(定理 M2(i))
g2 = len(X9) * (729 * 3)            # なし: raw ではなく 12 * |fibre|=27
g2 = len(X9) * 27
g3 = 27 * 12                        # |F_0(M2)| * |Im chi~| = (9*3) * phi(36)
def phi(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)
g4 = (9 * 3) * phi(36)
chk("|GT(M2)| 4 通り一致", (g1, g2, g3, g4), (324, 324, 324, 324))
chk("phi(36)", phi(36), 12)
chk("|F_0(M2)| = |F_0(K9)|*|Z(H3)| = 9*3", 9 * 3, 27)

# ---- 6. 走査規模 ------------------------------------------------------------
chk("raw candidates (M2) = |X_9| * |[Q,Q]|", len(X9) * (729 * 3), 26244)
chk("raw candidates (K9 単体) = cert と一致", len(X9) * 729, K9["counts"]["raw_candidates"])
chk("raw candidates (L 単体) = cert と一致", len(X3) * (27 * 3), L01["counts"]["raw_candidates"])
chk("raw candidates (N0 単体)", len(X0) * 3, 6)
chk("R4b(972 屋根)との規模比", 4408992 // 26244, 168)

# ---- 7. Q = C_2^2 の三指標(補題 D0 の作用表)と H^2 の不変量 ----------------
# a = diag(+1,-1,-1), b = diag(-1,+1,-1) on A = <r>^3
chi = {1: (+1, -1), 2: (-1, +1), 3: (-1, -1)}   # (chi(a), chi(b))
triv = (+1, +1)
chk("A の 3 座標はいずれも自明指標でない", [i for i in chi if chi[i] == triv], [])
wedge = {(i, j): (chi[i][0] * chi[j][0], chi[i][1] * chi[j][1]) for i in chi for j in chi if i < j}
chk("Lambda^2 A に自明指標なし", [k for k, v in wedge.items() if v == triv], [])
chk("Bockstein 部(=A^* と同型)に自明指標なし", [i for i in chi if chi[i] == triv], [])
# ==> H^2(G_n, Z/3)^{trivial coeff} = 0
chk("Lambda^2 の指標は 3 座標の指標の置換になっている",
    sorted(wedge.values()), sorted(chi.values()))

# ---- 8. Lambda = ker(GT(K9) -> GT(K3)) の構造(Theta_9 座標・追補 C.3 の積法則) --
# Theta_9([m,f]) = (k, u=2m+1 mod 9, eps=m mod 2),  (k1,u1,e1)*(k2,u2,e2)=(k1+u1k2, u1u2, e1+e2)
U9 = [u for u in range(9) if gcd(u, 9) == 1]
GT9 = [(k, u, e) for k in range(9) for u in U9 for e in range(2)]
chk("|GT(K9)| = 108 (Theta_9 座標)", len(GT9), 108)
def mul(g1, g2):
    return ((g1[0] + g1[1] * g2[0]) % 9, (g1[1] * g2[1]) % 9, (g1[2] + g2[2]) % 2)
def red3(g):
    return (g[0] % 3, g[1] % 3, g[2])
Lam = [g for g in GT9 if red3(g) == (0, 1, 0)]
chk("|Lambda| = |ker(GT(K9)->GT(K3))|", len(Lam), 9)
chk("Lambda は部分群", all(mul(a, b) in Lam for a in Lam for b in Lam), True)
chk("Lambda は可換", all(mul(a, b) == mul(b, a) for a in Lam for b in Lam), True)
def ordof(a, e):
    g, t = a, 1
    while g != e:
        g, t = mul(g, a), t + 1
    return t
chk("Lambda は exponent 3 (=> C3 x C3)",
    sorted({ordof(a, (0, 1, 0)) for a in Lam}), [1, 3])
chk("GT(K3) 水準の像は 12 元", len({red3(g) for g in GT9}), 12)
# K3(FV-SUB)が守るもの: Im*Lambda = GT(K9)  <=>  d | 9
chk("d は 9 を割らねばならない(K3 が守る範囲)", [d for d in [1, 2, 3, 4, 6, 9, 12] if 9 % d == 0],
    [1, 3, 9])
# SPLIT-NULL(m-fiber 合併)+ m(N0) subset {0,2} が許す d
mres = {0: [m for m in X9 if m % 3 == 0], 2: [m for m in X9 if m % 3 == 2]}
chk("X_9 の mod3 分割は 6+6", (len(mres[0]), len(mres[2])), (6, 6))
chk("SPLIT-NULL が許す d の候補(m(N0)=部分集合ごと)",
    sorted({12 // len(s) for s in ([X9, mres[0], mres[2]])}), [1, 2])
chk("K3 と SPLIT-NULL の共通解は d=1 のみ",
    [d for d in [1, 2] if 9 % d == 0], [1])

# ---- 9. GT(M2) の位数分布の予言(追補 C.3 の GT(K9) 分布 x C3) ----------------
dist9 = {1: 1, 2: 19, 3: 8, 6: 44, 9: 18, 18: 18}
chk("GT(K9) 位数分布の総和", sum(dist9.values()), 108)
def lcm(a, b):
    return a * b // gcd(a, b)
distM = {}
for d, c in dist9.items():
    distM[d] = distM.get(d, 0) + c            # z = 1
    e = lcm(d, 3)
    distM[e] = distM.get(e, 0) + 2 * c        # z の位数 3(2 個)
chk("GT(M2) 位数分布の予言", {k: distM[k] for k in sorted(distM)},
    {1: 1, 2: 19, 3: 26, 6: 170, 9: 54, 18: 54})
chk("GT(M2) 位数分布の総和", sum(distM.values()), 324)

print("")
print("failures = %d" % len(fails))
if fails:
    print("FAILED: " + ", ".join(fails))
    sys.exit(1)
print("ALL PASS")
