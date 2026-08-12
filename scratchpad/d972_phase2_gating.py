# -*- coding: utf-8 -*-
"""
[Phase 2 gating] canon formulas only (定義ノート §3 / 2405 Thm 4.3 / Thm 4.6).
  |G_n| = |PB_3/K^(n)| = 4n^3 (n odd) , 4(n/2)^3 (n even)
  |GT(K^(n))| = 2 n0 phi(n0)              (alpha <= 1)
              = n0 phi(n0) 2^(2 alpha - 2) (alpha >= 2)      n = 2^alpha n0
  K^(q) subset K^(n)  <=>  n | lcm(q,2)   [Prop 3.5]
  K^(n) = K^(2n) for n odd
測定済: |PB_3/N_S4| = 504 , |PB_3/M| = 1,469,664 = 2916*504 , |GT(M)| = 972 , |A| = 324
"""
from math import gcd
from sympy import totient, factorint

NS4 = 504
PB3_M = 1469664
GT_M, A = 972, 324

def Gn(n):
    return 4*n**3 if n % 2 else 4*(n//2)**3

def gt_kn(n):
    a = 0; m = n
    while m % 2 == 0: a += 1; m //= 2
    n0 = m
    return 2*n0*int(totient(n0)) if a <= 1 else n0*int(totient(n0))*2**(2*a-2)

print("=== index check : [GT(M):A] = r ? ===")
print(f"  |GT(M)|/|A| = {GT_M}//{A} = {GT_M//A}   r(measured) = 3   equal: {GT_M//A == 3}")
print(f"  |GT(M)| = 12*d9*dS4 = 12*9*9 = {12*81} : {12*81 == GT_M}")
print(f"  |A| = 12*d9*dS4/r = {12*81//3} : {12*81//3 == A}")
print("  ==> [GT(M):A] = r  (identity, not coincidence)")

print()
print("=== dihedral tower : is the reduction surjective? (Thm 4.3 cardinalities) ===")
for n in (9, 27, 81, 243):
    print(f"  n={n:3d}  |G_n| = {Gn(n):>10d}   |GT(K^(n))| = {gt_kn(n):>6d}")
print("  ratios: 108 -> 972 -> 8748 : factor 9 each  (X_n grows by 3, k-parameter by 3)")
print("  ==> R_{K^(3n),K^(n)} is surjective on both parameters (X_{3n}->X_n, Z/3n->Z/n)")

print()
print("=== Phase 2 candidates : K^(l) cap N_S4 with K^(l) subset K^(9)  (9 | lcm(l,2)) ===")
print(f"{'l':>5} {'9|lcm(l,2)':>11} {'|G_l|':>10} {'|GT(K^l)|':>10} {'gating bound':>14}  axis")
rows = []
for l in (18, 27, 36, 45, 54, 63, 72, 81, 90, 99, 108, 117, 126):
    ok = (9 % 2 == 0) or True
    cond = (( (l*2 if l%2 else l) ) % 9 == 0) if False else ( (l if l%2==0 else 2*l) % 9 == 0 )
    lcm2 = l if l % 2 == 0 else 2*l
    cond = (lcm2 % 9 == 0)
    if not cond: continue
    if l % 2 == 1 and l % 9 == 0 and l == 9: continue
    a = 0; m = l
    while m % 2 == 0: a += 1; m //= 2
    axis = "3-tower (i)" if m % 9 == 0 and a == 0 and l in (27,81,243) else \
           ("2-adic (iv-a)" if a >= 2 else "other prime (iv-b)")
    if l == 18: axis = "= K^(9) (nothing)"
    rows.append((l, Gn(l), gt_kn(l), Gn(l)*NS4, axis))
    print(f"{l:>5} {'yes':>11} {Gn(l):>10d} {gt_kn(l):>10d} {Gn(l)*NS4:>14d}  {axis}")

print()
print("=== free pre-filter : |GT(K)| < |GT(M)| = 972  =>  Im is forced to 324 (decided) ===")
print("  (since A <= Im <= GT(M), |Im| in {324,972}, and |Im| <= |GT(K)|)")
print("  [!] GT of a finer window generally GROWS, so this filter is cheap but unlikely to fire.")
print(f"  reference: |GT(K^(9))| = {gt_kn(9)} , |GT(M)| = {GT_M} (M finer than K^(9): 108 -> 972)")
