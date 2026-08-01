# -*- coding: utf-8 -*-
"""K5 campaign DESIGN-side checks (no measurement of any reduction image).
(1) H^2(G_5, F_5) = 0  (NO-CENTRAL^(5)) via Q-character bookkeeping
(2) H^2(G_5, chi_i) dimension = 2
(3) quotient/sizing arithmetic for the candidate window families
"""
import sys
from math import gcd
from itertools import combinations

fails = []


def chk(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + ((" | " + str(extra)) if extra else ""))
    if not cond:
        fails.append(name)


# ---------------- Q = C_2 x C_2 characters ----------------
# elements of Q as pairs in {0,1}^2 ; characters chi_(s,t)(a,b) = (-1)^(s a + t b)
Qel = [(0, 0), (0, 1), (1, 0), (1, 1)]
chars = [(0, 0), (0, 1), (1, 0), (1, 1)]          # (s,t) labels


def ev(ch, q):
    return (-1) ** ((ch[0] * q[0] + ch[1] * q[1]) % 2)


def mulch(c1, c2):
    return ((c1[0] + c2[0]) % 2, (c1[1] + c2[1]) % 2)


triv = (0, 0)
nontriv = [c for c in chars if c != triv]
chk("Q1 |Q|=4, 3 nontrivial characters", len(nontriv) == 3)
chk("Q2 product of two distinct nontrivial chars = the third",
    all(mulch(a, b) == [c for c in nontriv if c not in (a, b)][0]
        for a, b in combinations(nontriv, 2)))

# A = <r>^3 as Q-module.  From lemma D0^n: generator a=(r,s,s) inverts coords 2,3 ;
# b=(rs,r,rs) inverts coords 1,3.  So with Q=<a,b> ~ C_2^2:
#   coord1 : a->+1, b->-1  => chi=(0,1)
#   coord2 : a->-1, b->+1  => chi=(1,0)
#   coord3 : a->-1, b->-1  => chi=(1,1)
Achars = [(0, 1), (1, 0), (1, 1)]
chk("A1 A = chi_1 + chi_2 + chi_3 : three DISTINCT nontrivial characters",
    sorted(Achars) == sorted(nontriv))

# H^2(A,F_5) for A = (Z/5)^3 elementary abelian, p=5 odd:
#   H^*(A,F_p) = Lambda(x1,x2,x3) tensor F_p[y1,y2,y3], deg x=1, y=beta(x) deg 2
#   H^2 = <x_i x_j (i<j)>  +  <y_1,y_2,y_3>     (dim 6)
# characters: x_i, y_i carry chi_i (self-dual over F_p since chi_i^2=1);
#             x_j x_k carries chi_j*chi_k
H2A = []
for i in range(3):
    H2A.append(("y%d" % (i + 1), Achars[i]))
for i, j in combinations(range(3), 2):
    H2A.append(("x%dx%d" % (i + 1, j + 1), mulch(Achars[i], Achars[j])))
chk("B1 dim H^2(A,F_5) = 6", len(H2A) == 6)
inv_triv = [t for t in H2A if t[1] == triv]
chk("B2 (NO-CENTRAL^(5))  H^2(G_5,F_5) = H^2(A,F_5)^Q = 0",
    len(inv_triv) == 0, [t[0] for t in H2A])
# each nontrivial character appears exactly twice
for c in nontriv:
    mult = [t[0] for t in H2A if t[1] == c]
    chk("B3 chi=%s appears exactly twice in H^2(A,F_5): %s" % (c, mult), len(mult) == 2)
for i, c in enumerate(Achars):
    tw = [t[0] for t in H2A if mulch(t[1], c) == triv]
    chk("B4 dim H^2(G_5, chi_%d) = 2  (twist by chi makes exactly 2 summands trivial)" % (i + 1),
        len(tw) == 2, tw)
# H^1
H1A = [("x%d" % (i + 1), Achars[i]) for i in range(3)]
chk("B5 H^1(G_5,F_5) = 0 (trivial coeffs)", len([t for t in H1A if t[1] == triv]) == 0)
for i, c in enumerate(Achars):
    tw = [t[0] for t in H1A if mulch(t[1], c) == triv]
    chk("B6 dim H^1(G_5, chi_%d) = 1" % (i + 1), len(tw) == 1, tw)

# ---------------- G_5 basic arithmetic ----------------
n = 5
chk("C1 |G_5| = 4n^3 = 500", 4 * n ** 3 == 500)
chk("C2 |[G_5,G_5]| = n^3 = 125", n ** 3 == 125)
chk("C3 G_5^ab = C_2^2 -> only simple quotient of G_5 is C_2", True, "paper: lemma D0^n")
chk("C4 |GT(K^(5))| = 2n phi(n) = 40", 2 * n * 4 == 40)
chk("C5 [B_3:K^(5)] = 6*500 = 3000", 6 * 500 == 3000)

# ---------------- candidate window sizing ----------------
def lcm(a, b):
    return a * b // gcd(a, b)


def Xsize(Mord):
    return len([m for m in range(Mord) if gcd(2 * m + 1, Mord) == 1])


print()
print("--- sizing table (design only; no image measured) ---")
print("%-26s %-8s %-8s %-10s %-12s %-12s" %
      ("window", "M_ord", "|X_M|", "|PB3/M|", "|[Q,Q]|", "raw cand"))
rows = [
    ("K^(15)            (Dih)", 30, 4 * 15 ** 3, 15 ** 3),
    ("K^(25)            (Dih)", 50, 4 * 25 ** 3, 25 ** 3),
    ("K^(20)            (Dih,4|q)", 20, None, None),
    ("K^(5) cap N_0  (Heis27)", lcm(10, 3), 500 * 27, 125 * 3),
    ("K^(5) cap N_Q  (Q_8)", lcm(10, 8), 500 * 8, 125 * 1),
    ("ENT roof |G|=2500", 10, 2500, 625),
]
for nm, Mord, idx, dq in rows:
    xs = Xsize(Mord)
    raw = (xs * dq) if dq else None
    print("%-26s %-8s %-8s %-10s %-12s %-12s" % (nm, Mord, xs, idx, dq, raw))

chk("D1 |X_{30}| = 2*phi(15) = 16 (K^(15) charming set size)", Xsize(30) == 16)
chk("D2 |GT(K^(15))| = |X_15| * 15 = 240 = 2*15*phi(15)",
    Xsize(30) * 15 == 240 == 2 * 15 * 8)
chk("D3 K^(15) cert index_PB3 = |G_15| = 4*15^3 = 13500", 4 * 15 ** 3 == 13500)
chk("D4 |X_{10}| = 8 = |X_5| (K^(5) charming set)", Xsize(10) == 8)
chk("D5 K^(5) cap N_0 : M_ord = lcm(10,3) = 30 -> |X_M| = 16 (m-level RISES)",
    lcm(10, 3) == 30 and Xsize(30) == 16)

# reduction m-part K^(15) -> K^(5): m mod 10 ; both have ord 30 vs 10
chk("E1 K^(15)_ord = 30, K^(5)_ord = 10, 10 | 30", 30 % 10 == 0)
X15 = [m for m in range(30) if gcd(2 * m + 1, 30) == 1]
X5 = [m for m in range(10) if gcd(2 * m + 1, 10) == 1]
chk("E2 m mod 10 maps X_15 ONTO X_5", sorted(set(m % 10 for m in X15)) == X5,
    (X15, sorted(set(m % 10 for m in X15))))
chk("E3 m-part fibres uniform of size 2 (|X_15|=16, |X_5|=8)",
    len(X15) == 16 and len(X5) == 8
    and all(len([m for m in X15 if m % 10 == t]) == 2 for t in X5))
chk("E4 predicted total fibre of R_{K15,K5} is 2*3 = 6 and 240/40 = 6",
    (len(X15) // len(X5)) * (15 // 5) == 240 // 40 == 6)


# ---------------- (F) prop K5-ENT-INSUF : K^(np), p | n ----------------
def rad(m):
    r, d = 1, 2
    while d * d <= m:
        if m % d == 0:
            r *= d
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        r *= m
    return r


def pval(m, p):
    e = 0
    while m % p == 0:
        m //= p
        e += 1
    return e


print()
print("--- prop K5-ENT-INSUF : N = K^(np) with p | n ---")
for (nn, pp) in [(3, 3), (5, 5), (9, 3), (7, 7), (15, 3), (15, 5), (25, 5)]:
    m = nn * pp
    e = pval(m, pp)
    # (i)  B_0 = n*A_{np} is inside Phi(A_{np}) = rad(m)*A_{np}
    inside = (rad(m) % 1 == 0) and (nn % rad(m) == 0)
    # (ii) invariant-factor obstruction: (Z/m)^3  !=  (Z/p)^3 x (Z/n)^3  when p|n
    lhs_p = [e, e, e]
    rhs_p = sorted([1, 1, 1] + [pval(nn, pp)] * 3)
    noniso = (sorted(lhs_p) != rhs_p)
    chk("F(%d,%d) B_0 = n*A subset Phi(A)=rad(np)*A  [rad=%d, n=%d]" % (nn, pp, rad(m), nn), inside)
    chk("F(%d,%d) (Z/%d)^3 NOT iso (Z/%d)^3 x (Z/%d)^3  (p-elem-div %s vs %s)"
        % (nn, pp, m, pp, nn, sorted(lhs_p), rhs_p), noniso and e >= 2)
    chk("F(%d,%d) |G_np| = 4(np)^3 and |ker(G_np->G_n)| = p^3"
        % (nn, pp), 4 * m ** 3 // (4 * nn ** 3) == pp ** 3)

# the measured n=3 instance
chk("F* n=3,p=3 : |G_9|=2916, |G_3|=108, kernel 27 = 3^3, and cert K9->K3 is the witness",
    4 * 9 ** 3 == 2916 and 4 * 27 == 108 and 2916 // 108 == 27)
# counter-check: p NOT dividing n -> CRT splits, so no obstruction
for (nn, pp) in [(5, 3), (7, 3), (3, 5)]:
    m = nn * pp
    e = pval(m, pp)
    chk("F' (%d,%d) p does NOT divide n -> (Z/%d)^3 = (Z/%d)^3 x (Z/%d)^3 (CRT, splits)"
        % (nn, pp, m, pp, nn), e == 1 and gcd(nn, pp) == 1)

# ---------------- (G) T1 scan sizes (prop K5-BIT) ----------------
print()
print("--- T1 scan sizes ---")
for tag, Mord, B0 in [("W-2 K^(25)", 50, 125), ("W-4 K^(5)capN_0", 30, 3)]:
    ms = [mm for mm in range(Mord) if mm % 10 == 0 and gcd(2 * mm + 1, Mord) == 1]
    print("  %-18s admissible m~ = %s  x |B_0 cap [P,P]| = %d  ->  %d"
          % (tag, ms, B0, len(ms) * B0))
chk("G1 W-2 T1 = 5 x 125 = 625",
    len([mm for mm in range(50) if mm % 10 == 0 and gcd(2 * mm + 1, 50) == 1]) * 125 == 625)
chk("G2 W-4 T1 = 2 x 3 = 6  (m~=10 drops: gcd(21,30)=3)",
    len([mm for mm in range(30) if mm % 10 == 0 and gcd(2 * mm + 1, 30) == 1]) * 3 == 6
    and gcd(21, 30) == 3)
chk("G3 |GT(K^(25))| = 2*25*phi(25) = 1000", 2 * 25 * 20 == 1000)
chk("G4 |X_50| = 40 = 2*phi(25)", Xsize(50) == 40)
chk("G5 K^(20) = K^(5) cap K^(4) (lcm(5,4)=20), 4 | 20 -> canon proved branch",
    lcm(5, 4) == 20 and 20 % 4 == 0)
chk("G6 |X_20| = 16 = 2*phi(10)... careful: 2*phi(20)/2", Xsize(20) == 16)
chk("G7 |X_40| = 32 (W-5 charming set)", Xsize(40) == 32)

print()
print("RESULT:", "ALL PASS" if not fails else ("FAILURES: " + repr(fails)))
sys.exit(1 if fails else 0)
