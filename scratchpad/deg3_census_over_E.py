"""
[D2-GAP-4] fixture: degree-3 covers of a genus-1 curve E branched exactly at 4 marked
points Q0, Qinf (total ramification, local monodromy = 3-cycle) and B1, B2 (simple
branching, local monodromy = transposition).

pi_1(E \ {4 pts}) = < a, b, c1, c2, c3, c4 | [a,b] c1 c2 c3 c4 = 1 >

Count homomorphisms to S_3 with prescribed local classes and transitive (= surjective,
since transpositions are present) image, modulo S_3-conjugacy.

Prediction to test: 4  (= the number of points P with [2]P = Q_0 found by the algebraic
scan in p1_d2_scan_v2 / p1d2_r1_canonicalization_v1 SS1.5).
"""
from itertools import product

# S_3 as tuples: perm p means i -> p[i], on {0,1,2}
S3 = [
    (0, 1, 2),  # id
    (1, 2, 0),  # 3-cycle
    (2, 0, 1),  # 3-cycle
    (0, 2, 1),  # transposition
    (2, 1, 0),  # transposition
    (1, 0, 2),  # transposition
]
ID = (0, 1, 2)
THREE = [(1, 2, 0), (2, 0, 1)]
TRANSP = [(0, 2, 1), (2, 1, 0), (1, 0, 2)]


def mul(p, q):
    """(p*q)(i) = p(q(i))  -- left action convention"""
    return tuple(p[q[i]] for i in range(3))


def inv(p):
    r = [0, 0, 0]
    for i in range(3):
        r[p[i]] = i
    return tuple(r)


def comm(a, b):
    return mul(mul(a, b), mul(inv(a), inv(b)))


def gen_group(elts):
    cur = {ID}
    frontier = [ID]
    while frontier:
        nxt = []
        for g in frontier:
            for h in elts:
                x = mul(g, h)
                if x not in cur:
                    cur.add(x)
                    nxt.append(x)
        frontier = nxt
    return cur


def census(cls1, cls2, cls3, cls4, label):
    sols = []
    for a, b in product(S3, repeat=2):
        k = comm(a, b)  # [a,b]
        for c1, c2, c3, c4 in product(cls1, cls2, cls3, cls4):
            if mul(mul(mul(mul(k, c1), c2), c3), c4) == ID:
                grp = gen_group([a, b, c1, c2, c3, c4])
                if len(grp) == 6:      # transitive on 3 points AND non-cyclic => S_3
                    sols.append((a, b, c1, c2, c3, c4))
    # orbits under simultaneous S_3-conjugation
    seen = set()
    orbits = 0
    orbit_sizes = []
    for s in sols:
        if s in seen:
            continue
        orb = set()
        for g in S3:
            gi = inv(g)
            orb.add(tuple(mul(mul(g, x), gi) for x in s))
        seen |= orb
        orbits += 1
        orbit_sizes.append(len(orb))
    print(f"{label}: tuples = {len(sols)}, S3-orbits (= covers) = {orbits}, "
          f"orbit sizes = {sorted(set(orbit_sizes))}")
    return orbits, len(sols)


print("=== main census: (3-cyc, 3-cyc, transp, transp) at (Q0, Qinf, B1, B2) ===")
census(THREE, THREE, TRANSP, TRANSP, "  Q0,Qinf totally ramified; B1,B2 simple")

print()
print("=== controls (sanity: other local data) ===")
census(THREE, THREE, THREE, THREE, "  all four totally ramified")
census(TRANSP, TRANSP, TRANSP, TRANSP, "  all four simple")
census(THREE, TRANSP, TRANSP, TRANSP, "  one 3-cyc, three transp")

print()
print("=== genus check of the degree-3 cover W -> E (Riemann-Hurwitz) ===")
# 2g(W)-2 = 3*(2*1-2) + sum(e-1) = 0 + [2 + 2 + 1 + 1] = 6  => g(W) = 4
print("  2g-2 = 3*0 + (2+2+1+1) = 6  =>  g(W) = 4   (matches the required genus 4)")
