#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAM-U-ASM v2 検算: 最短鎖 (S5) の位数計算(整数演算のみ・n=5 非接触)

検査項目
  A. n 奇 => gcd(2n,4)=2 かつ ord_{Z/2n}([4]) = 2n/gcd(2n,4) = n  (下から)
  B. 直接計算: Z/2n における 4 の加法位数(4 を k 回足して 0 になる最小 k)= n
  C. (±4)^n = ±2^{2n} の整数恒等式 (上から: (-4)^n = -2^{2n}, n 奇)
  D. zeta_{4n}^{2n} = -1 の指数計算 (2n mod 4n の半分 => 位数 2 の元)
出力は PASS/FAIL のみ。K^{(5)} は検査宇宙から除外(封印遵守)。
"""
from math import gcd

ODD_N = [n for n in range(3, 502, 2) if n != 5]   # n=5 は封印により除外

fails = []

def add_order(a, m):
    """Z/m における a の加法位数を素朴に計算(素朴 = 独立実装)"""
    k, s = 1, a % m
    while s % m != 0:
        s += a
        k += 1
        if k > m + 1:
            return None
    return k

for n in ODD_N:
    m = 2 * n
    # A: 閉形
    g = gcd(m, 4)
    ordA = m // g
    if not (g == 2 and ordA == n):
        fails.append(("A", n, g, ordA))
    # B: 素朴な直接計算(閉形と独立)
    ordB = add_order(4 % m, m)
    if ordB != n:
        fails.append(("B", n, ordB))
    # C: (-4)^n == -2^(2n) , 4^n == 2^(2n)
    if (-4) ** n != -(2 ** (2 * n)) or 4 ** n != 2 ** (2 * n):
        fails.append(("C", n))
    # D: zeta_{4n}^{2n} は位数 2 (=> = -1) : 4n | 2n*2 かつ 4n ∤ 2n
    if not ((2 * n * 2) % (4 * n) == 0 and (2 * n) % (4 * n) != 0):
        fails.append(("D", n))

print("universe: odd n in [3,501], n != 5 (sealed) ; |universe| =", len(ODD_N))
print("checks   : A(closed form) B(naive order) C(power identity) D(root of unity)")
print("failures :", len(fails))
if fails:
    print(fails[:10])
    raise SystemExit(1)
print("RESULT   : ALL PASS")
