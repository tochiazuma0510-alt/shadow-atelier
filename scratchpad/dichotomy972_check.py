# -*- coding: utf-8 -*-
"""
[DICHOTOMY-972] the 648 split is all-or-nothing.  (adjudication 1125)

  A = a_M(G_Q)  subgroup of GT(M)   |A| = 324
  GT(M) group (M isolated)          |GT(M)| = 972
  PR_M(GTgen) : submonoid of a finite group => SUBGROUP, and A <= PR_M <= GT(M)
  [GT(M):A] = 3 is PRIME  =>  PR_M in {A, GT(M)}  =>  no intermediate case.
"""
from math import gcd

X, A = 972, 324
idx = X // A
print("=== index structure ===")
print("  |GT(M)| = %d = %s" % (X, "2^2 * 3^5"))
print("  |A|     = %d = %s   (= 12 * d9 * dS4 / r = 12*9*9/3)" % (A, "2^2 * 3^4"))
print("  [GT(M):A] = %d   prime: %s" % (idx, all(idx % p for p in range(2, idx)) and idx > 1))
print("  |X - A| = %d" % (X - A))
print()
print("=== dichotomy ===")
print("  PR_M is a subgroup with A <= PR_M <= GT(M) and [GT(M):A] prime")
print("  ==> PR_M = A            : #alpha(fake) = %d , #beta(genuine non-arith) = 0" % (X - A))
print("  ==> PR_M = GT(M)        : #alpha = 0 , #beta = %d" % (X - A))
print("  ==> NO intermediate case. The 648 are ALL fake or ALL genuine-non-arithmetic.")
print()
print("=== per-refinement measurement is a single bit ===")
print("  K isolated, K <= M  ==> R_{K,M} : GT(K) -> GT(M) is a group homomorphism")
print("  A = R_{K,M}(a_K(G_Q)) <= Im R_{K,M} <= GT(M)  ==> |Im| in {324, 972}")
print("  324 ==> all 648 FAKE (finite certificate, done)")
print("  972 ==> no information at this depth; go deeper")
print()
print("=== sensitivity: the dichotomy needs the index to be prime ===")
for r in (1, 3, 9):
    a = 12 * 9 * 9 // r
    i = X // a if X % a == 0 else None
    isp = i is not None and i > 1 and all(i % p for p in range(2, i))
    print("  r=%d : |A|=%4d  index=%s  prime: %s" % (r, a, i, isp))
print("  ==> the dichotomy is a feature of r = 3 (index 3). r = 9 gives index 9, NOT prime.")
print()
print("=== gating values for candidate refinements (from the canon, not guessed) ===")
print("  |G_n| = 4n^3 (n odd)  [definition note SS3]  =>  |B3/K^(n)| = 6 * 4n^3")
for n in (9, 27):
    print("    n=%2d : |G_n| = %6d , |B3/K^(n)| = %7d" % (n, 4*n**3, 6*4*n**3))
print("  K^(27) subset K^(9) since 9 | lcm(27,2) = 54   [Prop 3.5]")
print("  ==> candidate refinement K := K^(27) cap N_S4 ,  |B3/K| <= 472392 * |B3/N_S4|")
print("  |GT(K^(27))| = 2*n0*phi(n0) = 2*27*18 = %d   [Thm 4.3, n=27=3^3, alpha=0]" % (2*27*18))
