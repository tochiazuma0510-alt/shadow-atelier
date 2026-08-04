# s3f_sixp_fam_check.py -- (6') 族版(定理 SIXP-fam)の紙証明の spot-check
# 格: python 単系統(cross-checked ではない・Lean 検証ではない)
# 宇宙(事前登録・値を見る前に固定):
#   n in {3,5,7,9,11,13,15,21}(奇数), j in {2,3}, alpha in (Z/n)\{0}(単元・非単元とも), beta in {0,1}
# 触れないもの: u 値・測定値・封印欄。本 script は G_n の純群論不変量のみを計算する。
import hashlib, sys

def mk(n):
    # D_n の元 = (a,e), a in Z/n, e in {0,1};  (a,e)*(b,f) = (a + (-1)^e b, e xor f)
    def dmul(p, q):
        a, e = p; b, f = q
        return ((a + (b if e == 0 else -b)) % n, e ^ f)
    def gmul(u, v):
        return (dmul(u[0], v[0]), dmul(u[1], v[1]), dmul(u[2], v[2]))
    def dinv(p):
        a, e = p
        return ((-a) % n, 0) if e == 0 else (a % n, 1)
    def ginv(u):
        return (dinv(u[0]), dinv(u[1]), dinv(u[2]))
    return gmul, ginv

def closure(gens, gmul, ident):
    S = {ident}
    frontier = [ident]
    while frontier:
        nf = []
        for x in frontier:
            for g in gens:
                y = gmul(x, g)
                if y not in S:
                    S.add(y); nf.append(y)
        frontier = nf
    return S

def run():
    fails = []
    rows = []
    UNIVERSE = [3, 5, 7, 9, 11, 13, 15, 21]
    for n in UNIVERSE:
        gmul, ginv = mk(n)
        e0 = ((0, 0), (0, 0), (0, 0))
        r = (1, 0); s = (0, 1); rs = (1, 1)
        X = (r, s, s); Y = (rs, r, rs)
        def pw(g, k):
            out = e0
            k = k % (4 * n * n)  # exponent reduced modulo a multiple of every element order
            for _ in range(k):
                out = gmul(out, g)
            return out
        a = {1: (r, (0, 0), (0, 0)), 2: ((0, 0), r, (0, 0)), 3: ((0, 0), (0, 0), r)}
        q = {1: ((0, 0), s, s), 2: (s, (0, 0), s), 3: (s, s, (0, 0))}
        G = closure([X, Y], gmul, e0)
        ok_G = (len(G) == 4 * n**3)
        # ord(X)
        t = X; o = 1
        while t != e0:
            t = gmul(t, X); o += 1
        ok_X = (o == 2 * n)
        if not ok_G: fails.append(("|G_n|", n, len(G)))
        if not ok_X: fails.append(("ord(X)", n, o))
        Xi = ginv(X)
        X2 = gmul(X, X)                      # = a_1^2
        ok_X2 = (X2 == (( (2 % n), 0), (0, 0), (0, 0)))
        if not ok_X2: fails.append(("X^2=a_1^2", n, X2))
        for j in (2, 3):
            jp = 5 - j
            for al in range(1, n):
                for be in (0, 1):
                    H = closure([a[j], gmul(pw(a[1], al), a[jp]), gmul(pw(a[1], be), q[j])], gmul, e0)
                    Hf = frozenset(H)
                    ok_H = (len(H) == 2 * n * n)
                    # Lambda = conjugacy orbit of H under <X,Y> = G_n  (BFS on generators)
                    def conj(Sf, g):
                        gi = ginv(g)
                        return frozenset(gmul(gmul(g, x), gi) for x in Sf)
                    Lam = {Hf}; fr = [Hf]
                    while fr:
                        nf = []
                        for S_ in fr:
                            for g in (X, Y, Xi, ginv(Y)):
                                T = conj(S_, g)
                                if T not in Lam:
                                    Lam.add(T); nf.append(T)
                        fr = nf
                    ok_L = (len(Lam) == 2 * n)          # <=> N_G(H) = H  (index count)
                    # <X> simply transitive on Lambda
                    orb = []; cur = Hf
                    for i in range(2 * n):
                        orb.append(cur); cur = conj(cur, X)
                    ok_st = (cur == Hf and len(set(orb)) == 2 * n and set(orb) == Lam)
                    # tau = conj by X as a permutation of Lambda (index it by orb order)
                    idx = {S_: i for i, S_ in enumerate(orb)}
                    tau = tuple(idx[conj(S_, X)] for S_ in orb)
                    ok_tau = (len(set(tau)) == 2 * n)
                    # Phi_{0,f_k} = inn_{X^{2k}} :  f_k^{-1} Y f_k == X^{-2k} Y X^{2k}
                    ok_phi = True; rho = []
                    for k in range(n):
                        fk = gmul(pw(a[1], 2 * k), pw(a[2], -2 * k))
                        lhs = gmul(gmul(ginv(fk), Y), fk)
                        c = pw(X, 2 * k)
                        rhs = gmul(gmul(ginv(c), Y), c)
                        if lhs != rhs: ok_phi = False
                        # rho_0(0,f_k) : H' -> Phi(H') = c^{-1} H' c
                        rho.append(tuple(idx[conj(S_, ginv(c))] for S_ in orb))
                    ok_faith = (len(set(rho)) == n)                     # rho_0 injective
                    tau2 = tuple(tau[tau[i]] for i in range(2 * n))
                    grp = set(); cur_p = tuple(range(2 * n))
                    for _ in range(n):
                        grp.add(cur_p); cur_p = tuple(tau2[cur_p[i]] for i in range(2 * n))
                    ok_img = (set(rho) == grp and len(grp) == n)        # rho_0(F_0) = tau(mu_{2n}[n])
                    # coordinate rule (ODD-H 11.2 cross-check): Phi_{0,f_k}(H_{j,al,be}) = H_{j,al,be-4k}
                    ok_coord = True
                    if j == 2:
                        lab = {}
                        for sg in (al, n - al):
                            for ga in range(n):
                                Hg = frozenset(closure([a[j], gmul(pw(a[1], sg), a[jp]),
                                                        gmul(pw(a[1], ga), q[j])], gmul, e0))
                                lab[Hg] = (sg % n, ga)
                        if set(lab.keys()) != Lam:
                            ok_coord = False
                        else:
                            for k in range(n):
                                c = pw(X, 2 * k)
                                img = conj(Hf, ginv(c))
                                if lab[img] != (al % n, (be - 4 * k) % n): ok_coord = False
                    for nm, okv in (("|H|", ok_H), ("|Lambda|", ok_L), ("simply-trans", ok_st),
                                    ("tau-inj", ok_tau), ("Phi=inn", ok_phi), ("rho0-faithful", ok_faith),
                                    ("rho0-image", ok_img), ("coord-rule", ok_coord)):
                        if not okv: fails.append((nm, n, j, al, be))
        rows.append((n, len(G), o, 2 * n, n))
    print("universe:", UNIVERSE)
    print("rows (n, |G_n|, ord(X), |Lambda_alpha|, |rho_0(F_0)|):")
    for row in rows: print("   ", row)
    print("checked windows:", sum(2 * (n - 1) * 2 for n in UNIVERSE))
    print("FAILS =", len(fails))
    if fails: print("FAIL detail:", fails[:20])
    print("RESULT:", "ALL PASS" if not fails else "FAILURES")

if __name__ == "__main__":
    h = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    run()
    print("script sha256 =", h)
