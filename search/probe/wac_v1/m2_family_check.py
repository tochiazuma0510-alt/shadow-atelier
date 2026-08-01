"""m2_family_check.py -- machine spot-check for the (M2) family identification note.

SPEC HEADER
  input      : none (self-contained; integer/permutation arithmetic only)
  n range    : ALLOWED_N = {3,7,9,11,13}.  n=5 is FORBIDDEN (K^(5) blind / freeze U7-NO5);
               the script asserts 5 not in the run list.
  alpha range: alpha in (Z/n)^x  (units only; gcd(alpha,n)>1 is out of scope by ODD-P)
  what it checks (fail-closed asserts + printed table):
    A. COORDINATE LEMMA (model): the map (c,v) |-> (eps,x), eps=0 iff v in {1,sigma},
       x = c_h (eps=0) resp. c_h - 2 alpha c_g (eps=1), is constant on left cosets of
       Hbar^mod and induces a bijection M^mod/Hbar^mod -> {0,1} x Z/n.
    A'. COORDINATE LEMMA (abstract): same with eps=0 iff q in {1,q_2},
       x = v_1 - alpha v_3 (eps=0) resp. v_1 + alpha v_3 (eps=1).
    B. NORMAL FORM: in those coordinates every group element acts as
         (0,x) -> (s,        eps*x + b')      (1,x) -> (1-s,      eps*x + b)
       with s in {0,1}, eps in {+1,-1}, b,b' in Z/n;  group order 4n^2, faithful.
    C. the model group and the abstract group are LITERALLY THE SAME subgroup
       Gamma_n <= Sym({0,1} x Z/n), independent of alpha.
    D. counts: |C0^exact|=|Cinf^exact|=n, |C0^class|=|Cinf^class|=2n, |C1|=n^2
    E. Nielsen: #triples(exact)=n^2, simply transitive under the translation subgroup;
                #triples(class)=4n^2, single M-orbit of size 4n^2 (trivial stabiliser);
                generation is automatic (never fails)
    F. invariants: model(alpha) triple has (eta0,delta)=(1,alpha);
                   abstract(alpha) triple has (eta0,delta)=(2,2 alpha); ratio = alpha
    G. cross table model(alpha) x abstract(alpha') over ALL unit reps mod +-1, by BFS
       canonical form (complete invariant for simultaneous Sym(2n)-conjugacy of a
       transitive triple).  expected: identity diagonal.
  conventions_used (conventions_ledger_v1):
    perm_composition = paper_left   ((p*q)(x) = p(q(x)))
    conjugation      = paper_inn_g_X_g_inv
    coset_side       = left  (left cosets gH, left action m.(gH)=(mg)H)
    chi_P_criterion  = "exact" AND "conjugacy_class" are both run ("line" NOT used)
    comparison_target= "every window H_{2,alpha',0}, alpha' ranging over (Z/n)^x/{+-1}"
    separation_condition_included = true (full cross table)
"""
import sys
from itertools import product

ALLOWED_N = (3, 7, 9, 11, 13)
assert 5 not in ALLOWED_N, "K^(5) is blind"
QTAB = [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]


def gcd(x, y):
    while y: x, y = y, x % y
    return x


def pmul(a, b): return tuple(a[b[i]] for i in range(len(a)))
def pinv(a):
    r = [0] * len(a)
    for i, v in enumerate(a): r[v] = i
    return tuple(r)
def ctype(p):
    n = len(p); seen = [False] * n; t = []
    for s in range(n):
        if seen[s]: continue
        c = 0; x = s
        while not seen[x]: seen[x] = True; x = p[x]; c += 1
        t.append(c)
    return tuple(sorted(t, reverse=True))
def canon(T):
    L = len(T[0]); best = None
    for s in range(L):
        lab = {s: 0}; order = [s]; i = 0
        while i < len(order):
            x = order[i]; i += 1
            for g in T[:2]:
                y = g[x]
                if y not in lab: lab[y] = len(order); order.append(y)
        if len(lab) != L: continue
        cf = tuple(tuple(lab[g[order[j]]] for j in range(L)) for g in T)
        if best is None or cf < best: best = cf
    return best


def pt(eps, x, n): return eps * n + x % n


def nf(p, n):
    """decode a perm of {0,1}xZ/n (point eps*n+x) into (s,e,b,bp) or None"""
    s = 1 if p[0] >= n else 0
    bp = p[0] % n
    d = (p[1] % n - bp) % n
    e = 1 if d == 1 % n else (-1 if d == (n - 1) % n else None)
    if e is None: return None
    b = p[n] % n
    for x in range(n):
        if p[pt(0, x, n)] != pt(s, (e * x + bp) % n, n): return None
        if p[pt(1, x, n)] != pt(1 - s, (e * x + b) % n, n): return None
    return (s, e, b, bp)


def coset_group(els, mul, H, label):
    """verify `label` is constant on left cosets gH and a bijection onto {0,1}xZ/n,
       then return the induced left permutation action in those coordinates."""
    Hs = set(H)
    for x in H:
        for y in H: assert mul(x, y) in Hs, "H not a subgroup"
    lab = {}
    for g in els:
        L = label(g)
        for h in H:
            assert label(mul(g, h)) == L, ("label not coset-constant", g, h)
        lab[g] = L
    assert len(set(lab.values())) == len(els) // len(H), "label not injective on cosets"
    # find a representative for each label
    rep = {}
    for g in els:
        rep.setdefault(lab[g], g)
    order = sorted(rep)
    idx = {L: i for i, L in enumerate(order)}
    # coordinates: point index = eps*n + x  (order is lexicographic on (eps,x))
    def perm(g):
        return tuple(idx[lab[mul(g, rep[order[k]])]] for k in range(len(order)))
    return perm, len(order), order


def model(n, a):
    """M^mod = Abar^dual |x| V_4 built from div(h),div(g) only.
       V4 coded 0=1, 1=sigma, 2=theta, 3=sigma*theta."""
    def vact(v, c):
        ch, cg = c
        if v == 0: return (ch % n, cg % n)
        if v == 1: return ((-ch) % n, (-cg) % n)
        if v == 2: return ((-ch + 2 * a * cg) % n, cg % n)
        return vact(1, vact(2, c))
    for v in range(4):
        for w in range(4):
            for c in ((1, 0), (0, 1)):
                assert vact(QTAB[v][w], c) == vact(v, vact(w, c)), "not a V4 action"
    els = [((ch, cg), v) for ch in range(n) for cg in range(n) for v in range(4)]
    def mul(x, y):
        (c1, v1), (c2, v2) = x, y
        c = vact(v1, c2)
        return (((c1[0] + c[0]) % n, (c1[1] + c[1]) % n), QTAB[v1][v2])
    H = [((0, cg), 0) for cg in range(n)] + [((0, cg), 1) for cg in range(n)]
    def label(g):
        (ch, cg), v = g
        if v in (0, 1): return (0, ch % n)
        return (1, (ch - 2 * a * cg) % n)
    perm, L, order = coset_group(els, mul, H, label)
    return els, mul, perm, L, H


def abstract(n, a):
    """G_n = (Z/n)^3 |x| V_4 (ODD-H (1.1)), H = H_{2,alpha,0} (ODD-H (1.2))."""
    def qact(q, v):
        if q == 0: return v
        return tuple(v[j] if (j + 1) == q else (-v[j]) % n for j in range(3))
    els = [(v, q) for v in product(range(n), repeat=3) for q in range(4)]
    def mul(x, y):
        (v, q), (w, r) = x, y
        aw = qact(q, w)
        return (tuple((v[j] + aw[j]) % n for j in range(3)), QTAB[q][r])
    U = [((a * t) % n, s % n, t % n) for s in range(n) for t in range(n)]
    H = [(v, q) for v in U for q in (0, 2)]
    def label(g):
        v, q = g
        if q in (0, 2): return (0, (v[0] - a * v[2]) % n)
        return (1, (v[0] + a * v[2]) % n)
    perm, L, order = coset_group(els, mul, H, label)
    X = ((1, 0, 0), 1); Y = ((1, 1, 1), 2)
    XY = mul(X, Y)
    Zi = [g for g in els if mul(XY, g) == ((0, 0, 0), 0)][0]
    # <X,Y> = G_n ?  (load-bearing for S6-b)
    gen = {((0, 0, 0), 0)}; fr = [((0, 0, 0), 0)]
    Xi = [g for g in els if mul(X, g) == ((0, 0, 0), 0)][0]
    Yi = [g for g in els if mul(Y, g) == ((0, 0, 0), 0)][0]
    while fr:
        x = fr.pop()
        for s in (X, Y, Xi, Yi):
            y = mul(x, s)
            if y not in gen: gen.add(y); fr.append(y)
    assert len(gen) == len(els), "<X,Y> != G_n"
    return perm(X), perm(Y), perm(Zi), L, len(els), sorted({perm(g) for g in els})


def deck_and_centre(G, n):
    """G a transitive subgroup of Sym(2n) given as a set of tuples.
       returns (|Z(G)|, |C_{Sym}(G)|) -- the latter = deck group of the cover."""
    Gl = sorted(G)
    Z = [g for g in Gl if all(pmul(g, h) == pmul(h, g) for h in Gl)]
    # centraliser in Sym(2n): semiregular, so determined by the image of point 0
    L = 2 * n; C = 0
    for s in range(L):
        c = {0: s}; ok = True; stack = [0]
        while stack and ok:
            x = stack.pop()
            for g in Gl:
                y = g[x]; ty = g[c[x]]
                if y in c:
                    if c[y] != ty: ok = False; break
                else:
                    c[y] = ty; stack.append(y)
        if ok and len(c) == L and len(set(c.values())) == L: C += 1
    return len(Z), C


def model_triples(n, a, criterion):
    els, mul, perm, L, H = model(n, a)
    MM = sorted({perm(g) for g in els})
    ID = tuple(range(L))
    chi0 = (1 % n, 0); chiI = ((-a) % n, (-1) % n)
    def sq(g): return mul(g, g)[0]
    E0 = [g for g in els if g[1] == 3 and sq(g) == chi0]
    EI = [g for g in els if g[1] == 2 and sq(g) == chiI]
    if criterion == "exact":
        C0 = sorted({perm(g) for g in E0}); CI = {perm(g) for g in EI}
    else:
        inv = {}
        for g in els:
            for y in els:
                if mul(g, y) == ((0, 0), 0): inv[g] = y; break
        def cls(x): return {perm(mul(mul(c, x), inv[c])) for c in els}
        C0 = sorted(cls(E0[0])); CI = cls(EI[0])
    C1 = sorted({perm(g) for g in els if g[1] == 1})
    tri = []; gen_fail = 0
    CIs = set(CI)
    for g0 in C0:
        for g1 in C1:
            gi = pinv(pmul(g0, g1))
            if gi in CIs:
                gen = {ID}; fr = [ID]
                while fr:
                    x = fr.pop()
                    for t in (g0, g1, pinv(g0), pinv(g1)):
                        y = pmul(x, t)
                        if y not in gen: gen.add(y); fr.append(y)
                if len(gen) != len(MM): gen_fail += 1
                else: tri.append((g0, g1, gi))
    return C0, C1, CI, tri, MM, L, gen_fail


def run(n):
    units = [u for u in range(1, n) if gcd(u, n) == 1]
    reps = []
    for u in units:
        if (n - u) % n not in reps: reps.append(u)
    print("=" * 74)
    print(f"n = {n}   units = {units}   alpha reps mod +-1 = {reps}")
    # --- A/B/C ---
    groups = {}
    for a in units:
        els, mul, perm, L, H = model(n, a)
        assert L == 2 * n and len(H) == 2 * n
        G = {perm(g) for g in els}
        assert len(G) == 4 * n * n, (n, a, len(G))          # faithful, order 4n^2
        for p in G: assert nf(p, n) is not None, ("model NF fails", n, a, p)
        groups[("model", a)] = G
    for a in units:
        X, Y, Z, L, ordG, G = abstract(n, a)
        assert L == 2 * n and ordG == 4 * n ** 3
        assert len(G) == 4 * n * n
        for p in G: assert nf(p, n) is not None, ("abstract NF fails", n, a, p)
        groups[("abs", a)] = set(G)
    allsame = len({frozenset(v) for v in groups.values()}) == 1
    print(f"  [A,A',B] coordinate lemma + normal form: PASS   (order 4n^2 = {4*n*n}, deg 2n = {2*n})")
    print(f"  [C] model group == abstract group == Gamma_n for ALL alpha: {allsame}")
    assert allsame
    zc, cc = deck_and_centre(groups[("model", units[0])], n)
    print(f"  [C'] |Z(Gamma_n)| = {zc}   |C_Sym(Gamma_n)| = deck group = {cc}   (<X,Y>=G_n asserted)")
    assert (zc, cc) == (1, 1)
    # --- D/E/F ---
    for a in reps:
        C0, C1, CI, T, MM, L, gf = model_triples(n, a, "exact")
        C0c, C1c, CIc, Tc, _, _, gfc = model_triples(n, a, "conjugacy_class")
        trans = [m for m in MM if nf(m, n)[0] == 0 and nf(m, n)[1] == 1]
        assert len(trans) == n * n
        # orbits of exact triples under translations
        seen = set(); orbs = []
        for t in T:
            if t in seen: continue
            o = {tuple(pmul(pmul(m, x), pinv(m)) for x in t) for m in trans}
            seen |= o; orbs.append(len(o))
        # orbits of class triples under full M
        seen2 = set(); orbs2 = []
        for t in Tc:
            if t in seen2: continue
            o = {tuple(pmul(pmul(m, x), pinv(m)) for x in t) for m in MM}
            seen2 |= o; orbs2.append(len(o))
        s, e, b, bp = nf(T[0][0], n); eta0 = (b + bp) % n
        _, _, b2, bp2 = nf(T[0][2], n); delta = (bp2 - b2) % n
        print(f"   MODEL a={a}: |C0|={len(C0)} |C1|={len(C1)} |Cinf|={len(CI)} "
              f"tri={len(T)} orb/transl={orbs} genfail={gf} | "
              f"class: |C0|={len(C0c)} tri={len(Tc)} orb/M={orbs2} genfail={gfc} | "
              f"(eta0,delta)=({eta0},{delta})  types={ctype(T[0][0])},{ctype(T[0][1])},{ctype(T[0][2])}")
        assert (len(C0), len(CI), len(C1), len(T), orbs, gf) == (n, n, n * n, n * n, [n * n], 0)
        assert (len(C0c), len(CIc), len(Tc), orbs2, gfc) == (2 * n, 2 * n, 4 * n * n, [4 * n * n], 0)
        assert (eta0, delta) == (1 % n, a % n)
    for a in reps:
        X, Y, Z, L, _, _ = abstract(n, a)
        s, e, b, bp = nf(X, n); eta0 = (b + bp) % n
        _, _, b2, bp2 = nf(Z, n); delta = (bp2 - b2) % n
        ratio = (delta * pow(eta0, -1, n)) % n
        print(f"   ABS   a={a}: types={ctype(X)},{ctype(Y)},{ctype(Z)}  "
              f"(eta0,delta)=({eta0},{delta})  ratio={ratio}")
        assert (eta0, delta, ratio) == (2 % n, (2 * a) % n, a % n)
    # --- G cross table ---
    mc = {}
    for a in reps:
        _, _, _, T, _, _, _ = model_triples(n, a, "exact")
        mc[a] = {canon(t) for t in T}
    ok = True; tbl = []
    for a in reps:
        row = []
        for ap in reps:
            X, Y, Z, L, _, _ = abstract(n, ap)
            v = canon((X, Y, Z)) in mc[a]
            row.append(1 if v else 0)
            if v != (a == ap): ok = False
        tbl.append(row)
    print(f"   CROSSTABLE (rows=model alpha, cols=abstract alpha') = {tbl}")
    print(f"   identity diagonal (S6-a AND S6-b): {ok}")
    assert ok
    return ok


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] or list(ALLOWED_N)
    for n in ns:
        assert n in ALLOWED_N, f"n={n} not allowed (n=5 is blind)"
        run(n)
    print("\nALL PASS")
