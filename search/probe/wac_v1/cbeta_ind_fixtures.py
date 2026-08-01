# C-beta-IND repair: generalised model-side datum (n, r0, rinf) and admissibility predicate.
#
# Purpose: produce PRE-REGISTERED expected values for the corrected dummy fixtures
# demanded by Sol W94-2.1 / P94-2.1.  Single-system (python) PREDICTION only --
# the implementer must reproduce independently (GAP).  Not a cross-check by itself.
#
# Model datum  D = (n; r0, rinf):
#     h(k) = (k-i)^{r0} (k+i)^{-r0} (k-1)^{rinf} (k+1)^{-rinf},   g(k) = (k+1)/(k-1)
#     V4 = {1, sigma: k->-k, theta: k->1/k, sigma*theta}
#     h^sigma = h^{-1},  g^sigma = g^{-1},
#     h^theta = (-1)^{r0+rinf} h^{-1} g^{-2 rinf},  g^theta = -g       [paper, general (r0,rinf)]
#   => on characters (c_h,c_g) of Abar = <[h],[g]>:
#     sigma.(ch,cg) = (-ch, -cg)
#     theta.(ch,cg) = (-ch - 2*rinf*cg, cg)
#   divisors:  div(h) = r0([i]-[-i]) + rinf([1]-[-1]),   div(g) = [-1]-[1]
#   local characters: chi_0 = (r0,0) at k=i (V4-inertia sigma*theta, over lambda=0)
#                     chi_inf = (rinf,-1) at k=1 (theta, over lambda=infinity)
#                     chi_1 = (0,0) at k=0 (sigma, over lambda=1)
#   The h_alpha family used so far is exactly (r0,rinf) = (1,-alpha).
import sys, math
from itertools import product

# ---------------- admissibility (A1)-(A6): to be checked BEFORE enumeration -------------
def kummer_rank_order(n, r0, rinf):
    """|Abar| where Abar = image of Z^2 -> (Z/n)^4 spanned by div(h), div(g)."""
    # kernel = {(a,b): a*r0 = 0 mod n, b = a*rinf mod n}  => |kernel| = gcd(r0,n)
    ker = math.gcd(r0 % n if r0 % n else n, n)
    return (n * n) // ker, ker

def admissibility(n, r0, rinf):
    """Return (ok, reason). Fail-closed checks in the order a checker must run them."""
    if n < 3:            return False, "N_TOO_SMALL"
    if n % 2 == 0:       return False, "N_NOT_ODD"          # -1 must be an n-th power
    order, ker = kummer_rank_order(n, r0, rinf)
    if order != n * n:   return False, f"KUMMER_RANK_DEFICIENT(|Abar|={order}, expected {n*n})"
    return True, "OK"

# ---------------- model-side group, purely from (n, r0, rinf) --------------------------
VT = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]   # 0=1, 1=sigma, 2=theta, 3=sigma*theta

def model_group(n, r0, rinf):
    def vact(v, c):
        ch, cg = c
        if v == 0: return (ch % n, cg % n)
        if v == 1: return ((-ch) % n, (-cg) % n)
        if v == 2: return ((-ch - 2*rinf*cg) % n, cg % n)
        return vact(1, vact(2, c))
    for v in range(4):
        for w in range(4):
            for c in ((1,0),(0,1)):
                assert vact(VT[v][w], c) == vact(v, vact(w, c)), "not a V4 action"
    els = [((ch,cg), v) for ch in range(n) for cg in range(n) for v in range(4)]
    def mul(x, y):
        (c1,v1),(c2,v2) = x, y
        c = vact(v1, c2)
        return (((c1[0]+c[0]) % n, (c1[1]+c[1]) % n), VT[v1][v2])
    Hm = [((0,cg), 0) for cg in range(n)] + [((0,cg), 1) for cg in range(n)]
    Hs = set(Hm)
    for x in Hm:
        for y in Hm:
            assert mul(x,y) in Hs, "Hbar^mod not a subgroup"
    def coset(g): return min(mul(g,h) for h in Hm)
    cid = {}; reps = []; canon = {}
    for g in els:
        c = coset(g)
        if c not in cid: cid[c] = len(reps); reps.append(c)
        canon[g] = cid[c]
    L = len(reps)
    def perm(g): return tuple(canon[mul(g, reps[k])] for k in range(L))
    return els, mul, perm, L, Hm

def pmul(a,b): return tuple(a[b[i]] for i in range(len(a)))
def pinv(a):
    r = [0]*len(a)
    for i,v in enumerate(a): r[v] = i
    return tuple(r)
def ctype(p):
    m = len(p); seen = [False]*m; t = []
    for s in range(m):
        if seen[s]: continue
        c = 0; x = s
        while not seen[x]: seen[x] = True; x = p[x]; c += 1
        t.append(c)
    return tuple(sorted(t, reverse=True))

def model_run(n, r0, rinf):
    els, mul, perm, L, Hm = model_group(n, r0, rinf)
    M = sorted({perm(g) for g in els}); ID = tuple(range(L))
    chi0 = (r0 % n, 0)
    chiI = (rinf % n, (-1) % n)
    def sq(el): return mul(el, el)[0]
    C0 = [perm(g) for g in els if g[1] == 3 and sq(g) == chi0]
    CI = set(perm(g) for g in els if g[1] == 2 and sq(g) == chiI)
    C1 = [perm(g) for g in els if g[1] == 1]
    tri = []
    for g0 in C0:
        for g1 in C1:
            gi = pinv(pmul(g0, g1))
            if gi in CI:
                gen = {ID}; fr = [ID]
                while fr:
                    x = fr.pop()
                    for s in (g0, g1, pinv(g0), pinv(g1)):
                        y = pmul(x, s)
                        if y not in gen: gen.add(y); fr.append(y)
                if len(gen) == len(M): tri.append((g0, g1, gi))
    seen = set(); orbits = []
    for t in tri:
        if t in seen: continue
        orb = {tuple(pmul(pmul(c,x),pinv(c)) for x in t) for c in M}
        seen |= orb; orbits.append(orb)
    types = (ctype(tri[0][0]), ctype(tri[0][1]), ctype(tri[0][2])) if tri else None
    return dict(group_order=len(M), degree=L, Hbar=len(Hm), nC0=len(C0), nC1=len(C1),
                nCinf=len(CI), triples=len(tri), orbits=len(orbits),
                orbit_sizes=sorted(len(o) for o in orbits), cycle_types=types), tri, L

# ---------------- abstract side: window H_{2,alpha,0} in M_n on 2n points ---------------
QTAB = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]
def abstract_build(n, alpha):
    def enc(v,q): return ((v[0]*n+v[1])*n+v[2])*4+q
    def dec(x):
        q = x % 4; x //= 4; c = x % n; x //= n; return (x//n, x % n, c), q
    def act(q,v):
        if q == 0: return v
        return tuple(v[j] if (j+1) == q else (-v[j]) % n for j in range(3))
    def mul(x,y):
        v,q = dec(x); w,r = dec(y); aw = act(q,w)
        return enc(tuple((v[j]+aw[j]) % n for j in range(3)), QTAB[q][r])
    def inv(x):
        v,q = dec(x); return enc(act(q, tuple((-t) % n for t in v)), q)
    G = list(range(4*n**3))
    U = [((alpha*t) % n, s % n, t % n) for s in range(n) for t in range(n)]
    H = [enc(v,q) for v in U for q in (0,2)]
    def coset(g): return min(mul(g,h) for h in H)
    cid = {}; reps = []; canon = {}
    for g in G:
        c = coset(g)
        if c not in cid: cid[c] = len(reps); reps.append(c)
        canon[g] = cid[c]
    L = len(reps)
    def perm(g): return tuple(canon[mul(g,reps[k])] for k in range(L))
    X = enc((1,0,0),1); Y = enc((1,1,1),2); Z = inv(mul(X,Y))
    return L, perm(X), perm(Y), perm(Z)

def canon_form(g0, g1, start):
    L = len(g0); lab = {start:0}; order = [start]; i = 0
    while i < len(order):
        x = order[i]; i += 1
        for gg in (g0, g1):
            y = gg[x]
            if y not in lab: lab[y] = len(order); order.append(y)
    if len(lab) != L: return None
    def rl(p): return tuple(lab[p[order[j]]] for j in range(L))
    return (rl(g0), rl(g1))

def s6_row(n, tri, L, windows):
    """for each alpha' in windows: is some model triple simultaneously conjugate to abstract?"""
    out = {}
    for ap in windows:
        La, X, Y, Z = abstract_build(n, ap)
        if La != L: out[ap] = "DEGREE_MISMATCH"; continue
        cf = canon_form(X, Y, 0)
        hit = False
        for (g0,g1,gi) in tri:
            if any(canon_form(g0,g1,s) == cf for s in range(L)): hit = True; break
        out[ap] = hit
    return out

def windows_of(n):
    """(Z/n)^x / {+-1} representatives"""
    seen = set(); reps = []
    for a in range(1, n):
        if math.gcd(a,n) != 1: continue
        if a in seen: continue
        seen.add(a); seen.add((-a) % n); reps.append(a)
    return reps

def report(tag, n, r0, rinf, do_s6=True):
    ok, reason = admissibility(n, r0, rinf)
    print(f"--- {tag}: n={n} r0={r0} rinf={rinf}  alpha_norm={norm_alpha(n,r0,rinf)}")
    print(f"    admissibility: {ok}  reason={reason}")
    if not ok:
        print("    => CONTROLLED_REJECT (no enumeration)"); return
    res, tri, L = model_run(n, r0, rinf)
    print("    ", res)
    if do_s6:
        print("     S6 row:", s6_row(n, tri, L, windows_of(n)))

def norm_alpha(n, r0, rinf):
    """normalised window label [alpha] = [-rinf * r0^{-1}] in (Z/n)^x/{+-1}, or None."""
    if math.gcd(r0 % n, n) != 1: return None
    a = (-rinf) * pow(r0 % n, -1, n) % n
    if math.gcd(a, n) != 1: return f"non-unit {a}"
    return min(a, (-a) % n)

if __name__ == "__main__":
    print("=== control: registered fixtures (r0=1, rinf=-alpha) ===")
    for a in (1,2,3):
        report(f"CTRL n=7 alpha={a}", 7, 1, -a)
    print("=== DUM-1: different rational function h, same n (r0=2) ===")
    report("DUM-1", 7, 2, -1)
    print("=== DUM-2: different n, out of registered universe ===")
    report("DUM-2", 11, 1, -4)
    print("=== DUM-3: non-admissible (rank-deficient Kummer datum) ===")
    report("DUM-3", 9, 3, -1)
    print("=== DUM-4: admissible but gcd(alpha,n)>1 (FAM-U out of scope) ===")
    report("DUM-4", 9, 1, -3)
    print("=== DUM-5: n even (must reject) ===")
    report("DUM-5", 6, 1, -1)
    print("=== reference: what the OLD dummies actually were ===")
    for lab in (99, 5):
        print(f"    old dummy alphaLabel={lab}: residue mod 7 = {lab%7}, "
              f"window class = {min(lab%7, (-lab)%7)}")
