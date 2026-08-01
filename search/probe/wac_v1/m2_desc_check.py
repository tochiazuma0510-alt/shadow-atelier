"""m2_desc_check.py -- machine check for the (M2-DESC) field-of-moduli argument.

SPEC HEADER
  input      : none (self-contained; integer/permutation arithmetic only)
  n range    : ALLOWED_N = {3,7,9,11,13}.  n=5 FORBIDDEN (K^(5) blind / freeze U7-NO5).
  purpose    : the Branch Cycle Lemma says that for tau in G_Q the conjugate cover
               ^tau C has a description lying in the Nielsen class of the chi(tau)-power
               classes (C_0^m, C_1^m, C_inf^m), m = chi(tau) in (Z/2n)^x.
               This script verifies, WITHOUT using the normal form of the note, that for
               EVERY m in (Z/2n)^x:
                 (i)  Ni(C_0^m, C_1^m, C_inf^m) is a single Gamma_n-orbit of size 4n^2;
                 (ii) that orbit is Sym(2n)-simultaneously conjugate to the ORIGINAL
                      triple (Xbar,Ybar,Zbar)  --  i.e. ^tau C = C.
               (i)+(ii) => the G_Q-stabiliser of the cover is all of G_Q => FoM = Q.
  method     : conjugacy classes computed by brute force in Gamma_n; the comparison uses
               the BFS canonical form (complete invariant for simultaneous Sym-conjugacy
               of a transitive triple).  No appeal to eta/delta/rho.
  conventions_used (conventions_ledger_v1):
    perm_composition = paper_left ((p*q)(x)=p(q(x))) ; coset_side = left
    conjugation      = paper_inn_g_X_g_inv
    comparison_target= "the ORIGINAL cover C_alpha itself, for every m in (Z/2n)^x"
    separation_condition_included = n/a (this test is a stabiliser test, not a
                                   discrimination test; discrimination is m2_family_check.py)
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
def ppow(a, k):
    r = tuple(range(len(a)))
    for _ in range(k): r = pmul(r, a)
    return r
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


def abstract(n, a):
    """G_n = (Z/n)^3 |x| V_4 (ODD-H (1.1)) acting on G_n / H_{2,a,0} (ODD-H (1.2))."""
    def qact(q, v):
        if q == 0: return v
        return tuple(v[j] if (j + 1) == q else (-v[j]) % n for j in range(3))
    els = [(v, q) for v in product(range(n), repeat=3) for q in range(4)]
    def mul(x, y):
        (v, q), (w, r) = x, y
        aw = qact(q, w)
        return (tuple((v[j] + aw[j]) % n for j in range(3)), QTAB[q][r])
    U = [((a * t) % n, s % n, t % n) for s in range(n) for t in range(n)]
    H = set((v, q) for v in U for q in (0, 2))
    cid = {}; reps = []
    for g in els:
        c = min(mul(g, h) for h in H)
        if c not in cid: cid[c] = len(reps); reps.append(c)
    lab = {g: cid[min(mul(g, h) for h in H)] for g in els}
    L = len(reps)
    def perm(g): return tuple(lab[mul(g, reps[k])] for k in range(L))
    X = ((1, 0, 0), 1); Y = ((1, 1, 1), 2)
    XY = mul(X, Y)
    Zi = [g for g in els if mul(XY, g) == ((0, 0, 0), 0)][0]
    G = sorted({perm(g) for g in els})
    return perm(X), perm(Y), perm(Zi), L, G


def run(n):
    units = [u for u in range(1, n) if gcd(u, n) == 1]
    reps = []
    for u in units:
        if (n - u) % n not in reps: reps.append(u)
    ms = [m for m in range(1, 2 * n) if gcd(m, 2 * n) == 1]   # image of chi mod 2n
    print("=" * 74)
    print(f"n = {n}   alpha reps = {reps}   chi(tau) mod 2n ranges over {ms}")
    for a in reps:
        X, Y, Z, L, G = abstract(n, a)
        assert len(G) == 4 * n * n
        ID = tuple(range(L))
        Ginv = {g: pinv(g) for g in G}
        def cls(p): return {pmul(pmul(c, p), Ginv[c]) for c in G}
        cf0 = canon((X, Y, Z))
        assert cf0 is not None
        rows = []
        for m in ms:
            C0 = sorted(cls(ppow(X, m))); C1 = cls(ppow(Y, m)); CI = cls(ppow(Z, m))
            tri = []
            for g0 in C0:
                for g1 in C1:
                    gi = pinv(pmul(g0, g1))
                    if gi in CI: tri.append((g0, g1, gi))
            # STRONGER + CHEAPER than a separate generation test:
            # canon(t) is defined only for TRANSITIVE triples (else None) and is a complete
            # invariant for simultaneous Sym(2n)-conjugacy.  If canon(t) == cf0 for EVERY
            # triple in the Nielsen class, then every such triple is transitive (hence
            # generates the same group as (X,Y,Z), i.e. Gamma_n) AND lies in the single
            # Sym-class of the original cover.  That is exactly (i)+(ii).
            same = all(canon(t) == cf0 for t in tri)
            # single Gamma_n-orbit (size 4n^2) -- checked on the first triple only, then by count
            o = {tuple(pmul(pmul(c, x), Ginv[c]) for x in tri[0]) for c in G}
            orbs = [len(o)] if len(o) == len(tri) else ["MULTIPLE"]
            rows.append((m, len(C0), len(C1), len(CI), len(tri), orbs, same))
            assert orbs == [4 * n * n] and len(tri) == 4 * n * n, (n, a, m, orbs, len(tri))
            assert same, ("tau-conjugate cover differs!", n, a, m)
        print(f"  alpha={a}: for ALL m in (Z/2n)^x -> |C0^m|={rows[0][1]} |C1^m|={rows[0][2]} "
              f"|Cinf^m|={rows[0][3]}  triples={rows[0][4]}  orbits={rows[0][5]}  "
              f"tau-fixed={all(r[6] for r in rows)}  ({len(ms)} values of m)")
    print(f"  => G_Q stabilises every cover in the family  =>  field of moduli = Q")
    return True


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] or list(ALLOWED_N)
    for n in ns:
        assert n in ALLOWED_N, f"n={n} not allowed (n=5 is blind)"
        run(n)
    print("\nALL PASS")
