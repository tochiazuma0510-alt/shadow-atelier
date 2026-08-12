# -*- coding: utf-8 -*-
"""
[TRIAD-972 firing check]  Independent re-derivation of the raw values (adjudication 1122).
All numbers quoted in docs/notes/triad972_firing_adjudication_v1.md are produced here.

  [a] = 2^7      (support {2}, exponent 7, ord 9)
  [b] = 2^1 3^6  (support {2,3})
  basis (v_2, v_3) in (Z/9)^2 ;  r = |<[a]> cap <[b]>| ;  |X-A| = 972 - 12 d9 dS4 / r
"""
def gen(g):
    S, cur = set(), (0, 0)
    for _ in range(9):
        S.add(cur); cur = ((cur[0]+g[0]) % 9, (cur[1]+g[1]) % 9)
    return S

def span(*gs):
    S = {(0, 0)}
    for _ in range(4):
        S = {((x+k*g[0]) % 9, (y+k*g[1]) % 9) for (x, y) in S for g in gs for k in range(9)}
    return S

a, b = (7, 0), (1, 6)
Sa, Sb = gen(a), gen(b)
inter, joint = Sa & Sb, span(a, b)
d9, dS4, r = len(Sa), len(Sb), len(Sa & Sb)

print("=== r ===")
print("  <[a]>=<(7,0)> order %d (= d9)   <[b]>=<(1,6)> order %d (= dS4)" % (d9, dS4))
print("  intersection = %s   r = %d   matches cert: %s"
      % (sorted(inter), r, sorted(inter) == [(0, 0), (3, 0), (6, 0)]))
print()
print("=== Kummer compositum degree ===")
print("  |<[a],[b]>| = %d ;  d9*dS4/r = %d ;  equal: %s"
      % (len(joint), d9*dS4//r, len(joint) == d9*dS4//r))
print("  <[a],[b]> = {2^m 3^k : k = 0 mod 3} : %s"
      % (joint == {(m, k) for m in range(9) for k in (0, 3, 6)}))
print()
print("=== TRIAD-972 ===")
A = 12*d9*dS4//r
print("  |A| = 12*d9*dS4/r = %d ;  |X-A| = 972-%d = %d ;  matches 648: %s"
      % (A, A, 972-A, 972-A == 648))
print("  |A|/972 = 1/%d" % (972//A))
print("  r-dependence (cross-check vs ideas_surg_boost 648/864):")
for rr in (1, 3, 9):
    print("    r=%d : |A|=%4d  |X-A|=%4d" % (rr, 12*81//rr, 972-12*81//rr))
print()
print("=== d9 = 9 : valuation proof (independent of RES-INJ-9) ===")
print("  2 is unramified in K=Q(zeta_9) (disc is a power of 3), v(2^7)=7")
print("  9 | 7 : %s ;  9 | 21 : %s  ==> ord_K([a]) = 9" % (7 % 9 == 0, 21 % 9 == 0))
print("  second proof: [Q(2^(1/9)):Q]=9, [Q(zeta_9):Q]=6, cubic subfields differ")
print("                (Q(zeta_9)+ abelian vs Q(2^(1/3)) non-Galois) ==> degree 9")
print()
print("=== RES-INJ-9 on <[a],[b]> ===")
print("  elements 2^m 3^(3j); 9th power needs 9|m (2 unramified) ==> m=0,")
print("  and 3^(3j) a 9th power <=> 3^(1/3) or 9^(1/3) in Q(zeta_9): impossible (abelian)")
print("  ==> kernel trivial ==> [L9 LS4 : Q(zeta_9)] = 27")
print()
print("=== ramification of L_{9,Aff} ===")
print("  gcd(7,9)=1 ==> L_{9,Aff} = Q(zeta_9, 2^(1/9)); x^9-2 Eisenstein at 2")
print("  ==> totally ramified at 2 ==> 'unramified outside 3' is FALSE")

# ---------------------------------------------------------------------------
# [設問4] gauge sensitivity : how much does |X-A| depend on the class [a] ?
# ---------------------------------------------------------------------------
print()
print("=== sensitivity of the firing to [a] (adjudication 1123) ===")
b = (1, 6)
Sb = gen(b)
cases = [("observed  [a]=2^7", (7, 0)),
         ("P-K9U-1   [a]=3^1", (0, 1)),
         ("P-K9U-1   [a]=3^2", (0, 2)),
         ("P-K9U-1   [a]=3^4", (0, 4)),
         ("shift 2^k [a]=2^1", (1, 0)),
         ("shift 2^k [a]=2^4", (4, 0)),
         ("mixed     [a]=2^7*3^3", (7, 3)),
         ("mixed     [a]=2^1*3^6", (1, 6))]
for name, aa in cases:
    Sa = gen(aa); rr = len(Sa & Sb); d = len(Sa)
    if 12*d*9 % rr == 0:
        A = 12*d*9//rr; print("  %-22s ord=%d  r=%d  |A|=%4d  |X-A|=%4d" % (name, d, rr, A, 972-A))
    else:
        print("  %-22s ord=%d  r=%d  (non-integral)" % (name, d, rr))
print()
print("  ==> a PURE 2-power shift keeps the 3-part trivial, so it cannot turn 3^j into 2^7")
print("  ==> if [a] were 3^j (the prediction) then r = 1 and |X-A| = 0 : NO FIRING")
print("  ==> the firing and the prediction failure are THE SAME EVENT")
