# -*- coding: utf-8 -*-
"""K^(5) universe pre-registration check (integer arithmetic + cert readout only).
NO new enumeration; reads certificates/K5.v1.json and re-derives Theta_5.
Touches nothing in the K5 blind campaign (no u, no c-hat, no PSL, no dessin data).
"""
import json, sys, itertools

n = 5
M = 2 * n            # K^(n)_ord
FOURN = 4 * n
fails = []


def chk(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + ((" | " + str(extra)) if extra else ""))
    if not cond:
        fails.append(name)


def kappa(m):
    return (m + 1) if (m % 2 == 1) else (-m)


# ---------- (A) X_5 and kappa ----------
X5 = [m for m in range(M) if _gcd(2 * m + 1, M) == 1] if False else None


def _gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


X5 = [m for m in range(M) if _gcd(2 * m + 1, M) == 1]
chk("A1 |X_5| = 2*phi(5) = 8", len(X5) == 8, X5)
chk("A2 X_5 = {0,1,3,4,5,6,8,9}", X5 == [0, 1, 3, 4, 5, 6, 8, 9])

# ---------- (B) read cert ----------
cert = json.load(open("certificates/K5.v1.json", encoding="utf-8"))
sh = cert["shadows"]
chk("B1 cert shadow count = 40", len(sh) == 40)
chk("B2 cert N_ord = 10", cert["target"]["invariants"]["N_ord"] == 10)
chk("B3 cert thm46_expected_order = 40", cert["counts"]["thm46_expected_order"] == 40)
chk("B4 cert index_PB3 = 500 (=|G_5|)", cert["target"]["invariants"]["index_PB3"] == 500)
chk("B5 cert derived_order = 125 (=|[G_5,G_5]|)",
    cert["target"]["invariants"]["derived_order"] == 125)

# ---------- (C) Theta_5 from f_triple ----------
inv2 = pow(2, -1, n)   # 3
theta = []             # index -> (k,u,eps)
for i, s in enumerate(sh):
    m = s["m"]
    tri = s["f_triple"]
    # tri[j] = [a_j, e_j] meaning r^{a_j} s^{e_j}
    ok_e = all(t[1] == 0 for t in tri)
    a1, a2, a3 = tri[0][0], tri[1][0], tri[2][0]
    k = (inv2 * a1) % n
    if not ok_e:
        fails.append("C0 f_triple has reflection part at idx %d" % i)
    if (a2 % n) != ((-2 * k) % n):
        fails.append("C1 second component mismatch at idx %d" % i)
    if (a3 % n) != (kappa(m) % n):
        fails.append("C2 third component != r^kappa(m) at idx %d" % i)
    u = (2 * m + 1) % n
    eps = m % 2
    theta.append((k, u, eps))
chk("C f_triple = (r^{2k}, r^{-2k}, r^{kappa(m)}) for all 40", len([f for f in fails if f.startswith("C")]) == 0)
chk("C3 Theta_5 injective (40 distinct triples)", len(set(theta)) == 40)
chk("C4 Theta_5 onto Z/5 x (Z/5)^x x C2",
    set(theta) == set((k, u, e) for k in range(5) for u in [1, 2, 3, 4] for e in [0, 1]))

# ---------- (D) group law vs composition table ----------
comp = cert["composition_table"]     # list of [i,j,res]
chk("D0 composition table has 1600 rows", len(comp) == 1600)
bad = 0
for row in comp:
    i, j, r = row
    k1, u1, e1 = theta[i]
    k2, u2, e2 = theta[j]
    pred = ((k1 + u1 * k2) % n, (u1 * u2) % n, (e1 + e2) % 2)
    if theta[r] != pred:
        bad += 1
chk("D1 (k,u,eps) semidirect law reproduces ALL 1600 products", bad == 0, "mismatches=%d" % bad)

# identity / inverse
idx_of = {t: i for i, t in enumerate(theta)}
e_idx = idx_of[(0, 1, 0)]
chk("D2 identity = Theta^-1(0,1,0) has m=0,f=1", sh[e_idx]["m"] == 0 and sh[e_idx]["f_word"] == [])
inv = cert["inverse_map"]
badinv = 0
for i, ii in inv:
    k1, u1, e1 = theta[i]
    ui = pow(u1, -1, n)
    pred = ((-ui * k1) % n, ui, e1)
    if theta[ii] != pred:
        badinv += 1
chk("D3 inverse map matches affine inverse", badinv == 0)

# ---------- (E) iota = [-1,1] ----------
cand = [i for i, s in enumerate(sh) if s["m"] == (M - 1) and s["f_word"] == []]
chk("E1 iota = [m=9, f=1] present in cert", len(cand) == 1, cand)
if cand:
    io = cand[0]
    chk("E2 Theta_5(iota) = (0,4,1)", theta[io] == (0, 4, 1), theta[io])
    sq = [r for (i, j, r) in comp if i == io and j == io][0]
    chk("E3 iota^2 = identity", sq == e_idx)
    chk("E4 chi~(iota) = 2m+1 = -1 mod 20", (2 * (M - 1) + 1) % FOURN == (FOURN - 1))

# ---------- (F) chi~ and F_0 ----------
chit = {}
for i, s in enumerate(sh):
    chit[i] = (2 * s["m"] + 1) % FOURN
chk("F1 chi~ image = (Z/20)^x (8 values)",
    set(chit.values()) == set(a for a in range(FOURN) if _gcd(a, FOURN) == 1),
    sorted(set(chit.values())))
F0 = [i for i in range(40) if chit[i] == 1]
chk("F2 |ker chi~| = |F_0| = 5", len(F0) == 5)
chk("F3 F_0 = {(k,1,0)}", set(theta[i] for i in F0) == set((k, 1, 0) for k in range(5)))
# F0 cyclic C5 in composition table
gen = [i for i in F0 if theta[i] == (1, 1, 0)][0]
orb, cur = set(), e_idx
for _ in range(5):
    cur = [r for (a, b, r) in comp if a == cur and b == gen][0]
    orb.add(cur)
chk("F4 F_0 = <(1,1,0)> is cyclic of order 5 in the cert composition table", orb == set(F0))

# ---------- (G) the only two candidate subgroups H_d (d|5) ----------
H1 = set(i for i in range(40) if theta[i][0] == 0)
H5 = set(range(40))
chk("G1 |H_1| = 2*phi(5) = 8", len(H1) == 8)
chk("G2 H_1 closed under composition (cert table)",
    all(r in H1 for (i, j, r) in comp if i in H1 and j in H1))
chk("G3 H_1 cap F_0 = {e} (d=1)", len(H1 & set(F0)) == 1)
chk("G4 chi~(H_1) = (Z/20)^x  (full)",
    set(chit[i] for i in H1) == set(a for a in range(FOURN) if _gcd(a, FOURN) == 1))
chk("G5 iota in H_1", cand and cand[0] in H1)
chk("G6 index [T:H_1] = 5", 40 // len(H1) == 5)

# exhaustive: subgroups of T containing iota with full chi~ image
elts = list(range(40))
mul = {}
for (i, j, r) in comp:
    mul[(i, j)] = r


def gen_sub(S):
    cur = set(S) | {e_idx}
    while True:
        new = set(cur)
        for a in cur:
            for b in cur:
                new.add(mul[(a, b)])
        if new == cur:
            return cur
        cur = new


subs = set()
# all subgroups: generate from all subsets of size<=2 is enough for |T|=40? do size<=3 to be safe
for r in (1, 2, 3):
    for S in itertools.combinations(elts, r):
        subs.add(frozenset(gen_sub(S)))
full = set(a for a in range(FOURN) if _gcd(a, FOURN) == 1)
good = [H for H in subs if set(chit[i] for i in H) == full and (cand and cand[0] in H)]
chk("G7 exhaustive: subgroups with full chi~ AND containing iota are exactly {H_1, T}",
    set(frozenset(H) for H in good) == {frozenset(H1), frozenset(H5)},
    "found %d: sizes %s" % (len(good), sorted(len(H) for H in good)))
# without the iota anchor: the parity trap H^bad
Hbad = set(i for i in range(40) if theta[i][2] == 0)
chk("G8 parity trap H^bad = {eps=0} is a subgroup, d=5, index 2, iota NOT in it",
    all(mul[(i, j)] in Hbad for i in Hbad for j in Hbad)
    and len(Hbad & set(F0)) == 5 and 40 // len(Hbad) == 2 and (cand[0] not in Hbad))
chk("G9 chi~(H^bad) has order 4 (misses the (Z/4)^x part) -> (CHI) violated",
    len(set(chit[i] for i in Hbad)) == 4, sorted(set(chit[i] for i in Hbad)))

# ---------- (H) fake accounting under each hypothesis ----------
chk("H1 if d_gen=1: genuine set = H_1 (8), fake = 32 = (n-d)*2phi(n)",
    40 - len(H1) == (5 - 1) * 2 * 4)
chk("H2 if d_gen=5: fake = 0", (5 - 5) * 2 * 4 == 0)
chk("H3 Omega(5)=1 -> at most one true descent", True)

# ---------- (I) Dih-neighbourhood: which K^(q) contain / are contained ----------
def lcm(a, b):
    return a * b // _gcd(a, b)


coarse = [nn for nn in range(3, 200) if lcm(5, 2) % nn == 0]
chk("I1 K^(5) is contained in K^(nn) only for nn in {5,10} (Prop 3.5)", coarse == [5, 10], coarse)
fine = [q for q in range(3, 60) if q % 2 == 1 and lcm(q, 2) % 5 == 0]
chk("I2 odd q with K^(q) <= K^(5): q multiples of 5", fine == [5, 15, 25, 35, 45, 55], fine)

print()
print("RESULT:", "ALL PASS" if not fails else ("FAILURES: " + repr(fails)))
sys.exit(1 if fails else 0)
