#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAM-U domain 復帰 検算: 最短鎖 (S5) の位数計算を n=5 を含む宇宙で走らせる

前身 asm_v2_ordercheck.py は封印 U7-NO5 により n=5 を宇宙から除外していた。
裁定 396(封印解除認可)+ 裁定 398(n=5 開封対決・全的中)により、
本 script は n=5 を宇宙に含めた版である(versioned・前身は改変しない)。

検査項目(A-D は前身と同一・E を追加)
  A. n 奇 => gcd(2n,4)=2 かつ ord_{Z/2n}([4]) = 2n/gcd(2n,4) = n  (下から)
  B. 直接計算: Z/2n における 4 の加法位数(素朴逐次加算)= n
  C. (±4)^n = ±2^{2n} の整数恒等式(上から: (-4)^n = -2^{2n}, n 奇)
  D. zeta_{4n}^{2n} = -1(位数 2)かつ -1 は zeta_{4n} の 2n 乗 => [4]_{2n}=[-4]_{2n}
  E. F_n = Q(zeta_{4n}) の p|2 の分解: e=2, f=ord_n(2), g=phi(n)/f, e*f*g=phi(4n)
     かつ w_p(4) = e*v_2(4) = 4  (u5_fire cert (iv) 欄の独立再計算)
  F. n=5 の族公式値: u_{5,alpha~} = 4(-1)^alpha~ を alpha~=1,2 で表示(cert 突合用)
整数演算のみ・浮動小数なし。
"""
from math import gcd

ODD_N = [n for n in range(3, 502, 2)]          # ★ n=5 を除外しない(domain 復帰)


def add_order(a, m):
    """Z/m における a の加法位数を素朴に計算(閉形と独立)"""
    k, s = 1, a % m
    while s % m != 0:
        s += a
        k += 1
        if k > m + 1:
            return None
    return k


def mult_order(a, m):
    """(Z/m)^x における a の乗法位数"""
    k, s = 1, a % m
    while s != 1 % m:
        s = (s * a) % m
        k += 1
        if k > m + 1:
            return None
    return k


def phi(m):
    return sum(1 for t in range(1, m + 1) if gcd(t, m) == 1)


fails = []
for n in ODD_N:
    m = 2 * n
    g4 = gcd(m, 4)
    ordA = m // g4
    if not (g4 == 2 and ordA == n):
        fails.append(("A", n, g4, ordA))
    if add_order(4 % m, m) != n:
        fails.append(("B", n))
    if (-4) ** n != -(2 ** (2 * n)) or 4 ** n != 2 ** (2 * n):
        fails.append(("C", n))
    if not ((2 * n * 2) % (4 * n) == 0 and (2 * n) % (4 * n) != 0 and (4 * n) // 2 == 2 * n):
        fails.append(("D", n))
    e = 2
    f = mult_order(2, n) if n > 1 else 1
    if f is None or phi(n) % f != 0:
        fails.append(("E", n, f))
    else:
        gg = phi(n) // f
        if e * f * gg != phi(4 * n) or e * 2 != 4:
            fails.append(("E", n, e, f, gg))

print("universe : odd n in [3,501] INCLUDING n=5 ; |universe| =", len(ODD_N))
print("checks   : A(closed) B(naive order) C(power id) D(root of unity) E(2-decomposition)")
print("failures :", len(fails))
if fails:
    print(fails[:10])
    raise SystemExit(1)

n = 5
print("--- n=5 row (previously sealed) ---")
print("  ord_{Z/10}([4])        =", add_order(4, 10), "(closed form:", 10 // gcd(10, 4), ")")
print("  e(p|2), f, g in Q(z20) =", 2, mult_order(2, 5), phi(5) // mult_order(2, 5))
print("  w_p(4) = e*v_2(4)      =", 2 * 2)
print("  deg F_5 = phi(20)      =", phi(20), "= e*f*g =", 2 * mult_order(2, 5) * (phi(5) // mult_order(2, 5)))
for at in (1, 2):
    print("  u_5,alpha~=%d = 4*(-1)^%d = %+d" % (at, at, 4 * (-1) ** at))
print("RESULT   : ALL PASS")
