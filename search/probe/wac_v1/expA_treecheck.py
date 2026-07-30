#!/usr/bin/env python3
# search/probe/wac_v1/expA_treecheck.py
#   実験A 追補: T3 稿の閉形 (定理 T3-N0, 平面木 Catalan 計数) と
#   本稿の指標和 + 集合分割 Moebius による N_gen を突き合わせる。
#   N = Cat(m-1) * m! / (t! f2! f3!),  m = t + f2 + f3 - 1 = j - t + 1
#   (種数 0・lambda = (ell, 1^t)・(k,j) は Ree 等号で一意)
# 出力: 各 (ell,t) の N。search/probe/wac_v1/expA_scan.g の値と比較する。
from math import comb, factorial as F
from fractions import Fraction

def cat(k):
    return comb(2 * k, k) // (k + 1)

# (ell, t, 指標和で得た N_gen; None は未測定)
CASES = [(13, 3, 2), (17, 3, 10), (19, 5, 1), (29, 7, None)]

print("ell  t   n  (k,j)    (f2,f3)  m   N(tree)  N(character)  agree")
for ell, t, nchar in CASES:
    n = ell + t
    s = n + t - 1                      # k + 2j at genus 0
    k = min(n // 2, s - 2 * (n // 3))
    j = (s - k) // 2
    while (s - k) % 2 or j > n // 3 or k > n // 2:
        k -= 1
        j = (s - k) // 2
    f2, f3 = n - 2 * k, n - 3 * j
    m = t + f2 + f3 - 1
    assert m == j - t + 1, (ell, t, m, j - t + 1)
    val = Fraction(cat(m - 1) * F(m), F(t) * F(f2) * F(f3))
    ok = "-" if nchar is None else ("OK" if val == nchar else "MISMATCH")
    print("%3d %3d %3d  (%2d,%2d)  (%d,%d)    %d   %7s  %12s  %s"
          % (ell, t, n, k, j, f2, f3, m, val, nchar, ok))
