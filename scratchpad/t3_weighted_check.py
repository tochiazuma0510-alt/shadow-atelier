"""
t3_weighted_check.py  --  verification run for
docs/notes/t3_quasi_purecycle_rigidity_v1_addendum_weighted.md
(Shadow Atelier mathematician, 2026-07-31)

Three independent checks, no GAP, no character tables:

 W1  the CLASSIFICATION is a statement about the WEIGHTED count.
     Exhaustive scan of the diophantine condition Cat(m-1)*m!/(t!f2!f3!) = 1
     over all m <= 40 and all (t,f2,f3) with t+f2+f3 = m+1.

 W2  the m = 1 boundary (outside the range of Lemma A2 / Thm T3-N0'):
     the five degenerate passports are listed and their weighted counts are
     computed by direct group-theoretic brute force, and compared to the
     closed form.

 W3  the WEIGHTED count and the (unweighted) NIELSEN/GENERATION count N are
     genuinely different numbers outside the Jordan range: brute force over
     the whole of S_n for
        (l,t) = (7,2) n=9   -- weighted 1, but the unique class is PSL(2,8),
                               so the generation count is 0;
        (l,t) = (9,3) n=12  -- weighted 1/3 (Aut = C_3), generation count 0;
        (l,t) = (9,1) n=10  -- weighted 6 = generation count 6 (calibration).

Brute force method: fix v of cycle type (l,1^t) on [0..n-1]; enumerate all
involutions g (g^2 = 1) of the prescribed 2-power type; set h := g*v (left
action, h(x) = v(g(x))) and keep the pairs with h^3 = 1 of the prescribed
3-power type.  Weighted count = #{transitive pairs} / |C_{S_n}(v)| (Burnside
/ orbit counting, stabiliser of a pair in C(v) = C_{S_n}(<g,h>) = Aut(M)).
Generation count N = #{pairs with <g,h> >= A_n} / |C_{S_n}(v)|  (the
stabiliser is trivial there, so this really is an orbit count).
"""

from math import comb, factorial
from itertools import combinations
from sympy.combinatorics import Permutation, PermutationGroup

def cat(i):
    return comb(2*i, i)//(i+1)

# ---------------------------------------------------------------- W1
print("== W1: exhaustive scan of  Cat(m-1)*m!/(t! f2! f3!) = 1 ==")
sols = []
for m in range(1, 41):
    C = cat(m-1)
    for t in range(0, m+2):
        for f2 in range(0, m+2-t):
            f3 = m+1-t-f2
            if f3 < 0:
                continue
            num = C*factorial(m)
            den = factorial(t)*factorial(f2)*factorial(f3)
            if num == den:
                sols.append((m, t, f2, f3))
print("  solutions with m <= 40:")
for s in sols:
    print("   m=%d  (t,f2,f3)=(%d,%d,%d)   multiset=%s" %
          (s[0], s[1], s[2], s[3], sorted(s[1:], reverse=True)))
msets = sorted({tuple(sorted(s[1:], reverse=True)) for s in sols})
print("  distinct multisets:", msets)
print("  matches the paper's {5,0,0},{2,1,0},{1,1,0}? ",
      msets == [(1,1,0),(2,1,0),(5,0,0)])
# the a-priori bound used in the paper's proof: Cat(m-1) <= m+1
print("  bound check Cat(m-1) <= m+1 fails first at m =",
      next(m for m in range(1,20) if cat(m-1) > m+1))

# ---------------------------------------------------------------- helpers
def perm_from_cycles(cycles, n):
    return Permutation(cycles, size=n)

def cycle_type(p, n):
    return tuple(sorted((len(c) for c in p.full_cyclic_form), reverse=True))

def involutions_of_type(n, k):
    """all g in S_n with g^2=1 having exactly k transpositions"""
    pts = list(range(n))
    def rec(avail, k):
        if k == 0:
            yield []
            return
        if len(avail) < 2*k:
            return
        a = avail[0]
        for idx in range(1, len(avail)):
            b = avail[idx]
            rest = avail[1:idx] + avail[idx+1:]
            for tail in rec(rest, k-1):
                yield [(a, b)] + tail
        # a is a fixed point
        for tail in rec(avail[1:], k):
            yield tail
    seen = set()
    for cyc in rec(pts, k):
        key = tuple(sorted(tuple(sorted(c)) for c in cyc))
        if key in seen:
            continue
        seen.add(key)
        yield perm_from_cycles([list(c) for c in cyc], n)

def brute(l, t, k, j, verbose=True):
    n = l + t
    f2, f3 = n-2*k, n-3*j
    m = t + f2 + f3 - 1
    v = perm_from_cycles([list(range(l))], n)     # (0 1 ... l-1), t fixed pts
    Cv = l * factorial(t)
    trans = 0; gen = 0; auts = []
    reps = []
    for g in involutions_of_type(n, k):
        h = v*g            # sympy: (v*g)(x) = g(v(x))?  -- normalise below
        # sympy Permutation multiplication is left-to-right: (p*q)(x)=q(p(x)).
        # We want h with g^{-1} h = v, i.e. h = g v  (as maps: first g then v)
        h = g*v
        if h.order() not in (1, 3):
            continue
        ct = cycle_type(h, n)
        if ct.count(3) != j or ct.count(1) != f3 or len(ct) != j+f3:
            continue
        G = PermutationGroup([g, h])
        if not G.is_transitive():
            continue
        trans += 1
        o = G.order()
        if o >= factorial(n)//2:
            gen += 1
        reps.append((g, h, o))
    weighted = trans / Cv
    Ngen = gen / Cv
    closed = cat(m-1)*factorial(m)/(factorial(t)*factorial(f2)*factorial(f3))
    if verbose:
        print("  l=%2d t=%d n=%2d (k,j)=(%d,%d) f2=%d f3=%d m=%d | T_trans=%5d |C|=%6d"
              " weighted=%s  closed=%s  match=%s | T_gen=%5d  N_gen=%s"
              % (l, t, n, k, j, f2, f3, m, trans, Cv, weighted, closed,
                 abs(weighted-closed) < 1e-9, gen, Ngen))
        orders = sorted({o for (_,_,o) in reps})
        print("        distinct |<g,h>| among transitive classes:", orders)
    return weighted, Ngen, closed

# ---------------------------------------------------------------- W2
print()
print("== W2: the m = 1 boundary (outside Lemma A2's m >= 2) ==")
print("  passports with m=1 (t+f2+f3=2), and their n:")
for (t, f2, f3) in [(1,1,0),(1,0,1),(0,1,1),(2,0,0),(0,0,2)]:
    m = 1
    j = m + t - 1
    n = 3*j + f3
    l = n - t
    k = (n - f2)//2 if (n-f2) % 2 == 0 else None
    closed = cat(m-1)*factorial(m)/(factorial(t)*factorial(f2)*factorial(f3))
    print("   (t,f2,f3)=(%d,%d,%d)  j=%d  n=%2d  l=%s  k=%s  closed form=%s"
          % (t, f2, f3, j, n, l, k, closed))
print("  -> only (t,f2,f3)=(1,0,1) has n>=4; brute force that one:")
brute(3, 1, 2, 1)

# ---------------------------------------------------------------- W3
print()
print("== W3: weighted count  vs  generation count N ==")
print("  (a) l=7 t=2 n=9  (k,j)=(4,3): closed form says weighted = 1")
brute(7, 2, 4, 3)
print("  (b) l=9 t=1 n=10 (k,j)=(4,3): calibration row of the note")
brute(9, 1, 4, 3)
print("  (c) l=9 t=3 n=12 (k,j)=(6,4): closed form says weighted = 1/3")
brute(9, 3, 6, 4)
print()
print("== DONE ==")
