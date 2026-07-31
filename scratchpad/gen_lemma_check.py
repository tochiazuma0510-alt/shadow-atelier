# Machine check of Lemma GEN (erratum F91-1.2) and of GAP-S1.
#
#   window data: v in S_n with prescribed cycle type; all (2,3)-decompositions
#   g^2 = 1, h^3 = 1, g*h = v   (h := g*v, since g^{-1} = g)
#
#   surj  :  <v^2, (v^2)^g> >= A_n        (= shadow surjectivity <xbar, ybar^f> = P, conjugated by a_1)
#   gen   :  <g,h>          >= A_n        (decomposition generation; sign class fixes A_n vs S_n)
#
#   Lemma GEN says  surj => gen   (so "surj and not gen" must be EMPTY).
#   GAP-S1 claims   gen  => surj   (so "gen and not surj" nonempty would REFUTE it).
#   Corollary GEN-2 says gen => surj whenever ord(v) is odd.
from sympy.combinatorics import Permutation, PermutationGroup
from math import factorial
import sys

def involutions(n):
    def rec(free, cur):
        if not free:
            yield tuple(cur)
            return
        i = free[0]; rest = free[1:]
        cur[i] = i
        yield from rec(rest, cur)
        for idx, p in enumerate(rest):
            cur[i] = p; cur[p] = i
            yield from rec(rest[:idx] + rest[idx+1:], cur)
        cur[i] = i
    return rec(list(range(n)), [0]*n)

def comp(a, b):           # (a*b)(x) = a(b(x))
    return tuple(a[b[x]] for x in range(len(a)))

def sgn(p):
    n = len(p); seen = [False]*n; s = 0
    for i in range(n):
        if not seen[i]:
            L = 0; j = i
            while not seen[j]:
                seen[j] = True; j = p[j]; L += 1
            s += L-1
    return (-1)**s

def order_of(p):
    n = len(p); seen = [False]*n; o = 1
    from math import gcd
    for i in range(n):
        if not seen[i]:
            L = 0; j = i
            while not seen[j]:
                seen[j] = True; j = p[j]; L += 1
            o = o*L//gcd(o, L)
    return o

def contains_An(gens, n):
    G = PermutationGroup([Permutation(list(g)) for g in gens])
    return G.order() >= factorial(n)//2

def run(n, cycles, label):
    # v built from the given cycle lengths
    v = list(range(n)); base = 0
    for L in cycles:
        for i in range(L):
            v[base+i] = base + (i+1) % L
        base += L
    v = tuple(v)
    v2 = comp(v, v)
    ordv = order_of(v)
    stats = {}
    for g in involutions(n):
        h = comp(g, v)
        if any(h[h[h[x]]] != x for x in range(n)):
            continue
        gen = contains_An((g, h), n)
        v2g = comp(comp(g, v2), g)          # (v^2)^g = g v^2 g
        surj = contains_An((v2, v2g), n)
        key = sgn(g)
        d = stats.setdefault(key, [0, 0, 0, 0, 0])
        d[0] += 1
        d[1] += gen
        d[2] += surj
        d[3] += (gen and not surj)          # GAP-S1 counterexample
        d[4] += (surj and not gen)          # Lemma GEN counterexample (must stay 0)
    print(f"=== {label}: n={n} v-type={cycles} ord(v)={ordv} ({'odd' if ordv%2 else 'even'})")
    for key in sorted(stats):
        tot, gen, surj, s1, s2 = stats[key]
        print(f"   sgn(g)={key:+d}: decomp={tot}  gen={gen}  surj={surj}"
              f"  [gen&!surj]={s1} (GAP-S1 ce)  [surj&!gen]={s2} (Lemma GEN ce)")
    sys.stdout.flush()

if __name__ == "__main__":
    run(10, [9, 1], "W-E-A10-9t1")
    run(10, [10],   "W-E-A10-5x2t0")
    run(11, [9, 2], "W-E-A11-9t2")
    run(9,  [7, 2], "aux n=9")
    run(12, [9, 2, 1], "W-E-A12-9t3")
