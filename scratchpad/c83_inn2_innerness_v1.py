"""Task 1 (i): inner shadows of GT(N), identification with the fake-torus image, Q^ab, witnesses q.
Fast version: the action of Q=B3/N on 1152 points is REGULAR, so idx(A):=A[0] identifies Q with {0..1151}
and the Cayley table is just the list of permutation arrays: mul(i,j)=P[i][j]."""
import json, io, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CERT = r"C:\Users\81905\Desktop\shadow-atelier\search\certs\koubou83_tref_window_export_v1_20260822.json"
d = json.load(io.open(CERT, encoding='utf-8'))
N_ORD = 12
RES = {}

for wk, w in d['windows'].items():
    deg = w['degree']
    def to0(l): return [v-1 for v in l]
    s1a = to0(w['s1_perm_image_list']); s2a = to0(w['s2_perm_image_list'])
    ca  = to0(w['c_perm_image_list']);  Xa = to0(w['x12_perm_image_list']); Ya = to0(w['x23_perm_image_list'])
    ida = list(range(deg))
    def compa(A, B): return [A[B[i]] for i in range(deg)]
    def inva(A):
        r = [0]*deg
        for i, v in enumerate(A): r[v] = i
        return r
    # BFS on Q with full arrays, keyed by tuple
    Qset = {tuple(ida): ida}
    fr = [ida]
    gens = [s1a, s2a, inva(s1a), inva(s2a)]
    while fr:
        nf = []
        for A in fr:
            for g in gens:
                B = compa(A, g); tB = tuple(B)
                if tB not in Qset: Qset[tB] = B; nf.append(B)
        fr = nf
    assert len(Qset) == deg, (len(Qset), deg)
    bases = set(A[0] for A in Qset.values())
    assert len(bases) == deg, "action not regular"
    P = [None]*deg
    for A in Qset.values(): P[A[0]] = A
    assert P[0] == ida
    def mul(i, j): return P[i][j]
    INVT = [0]*deg
    for i in range(deg):
        for j in range(deg):
            if P[i][j] == 0: INVT[i] = j; break
    def iv(i): return INVT[i]
    def power(i, e):
        r = 0; b = i if e >= 0 else iv(i)
        for _ in range(abs(e)): r = mul(b, r)
        return r
    S1 = s1a[0]; S2 = s2a[0]; C = ca[0]; XI = Xa[0]; YI = Ya[0]
    print("="*80); print("WINDOW", wk, " |Q|=", deg)

    # G = <x,y> with words
    words = {0: ()}
    fr = [0]
    while fr:
        nf = []
        for a in fr:
            for gi, L in ((XI, 'x'), (YI, 'y')):
                for e in (1, -1):
                    b = mul(a, power(gi, e))
                    if b not in words: words[b] = words[a] + ((L, e),); nf.append(b)
        fr = nf
    G = sorted(words)
    # [G,G] = normal closure in G of [x,y]
    def comm(a, b): return mul(a, mul(b, mul(iv(a), iv(b))))
    seed = comm(XI, YI)
    DG = {0}; fr = [0]
    # normal closure: generate by all G-conjugates of seed
    congens = set(mul(g, mul(seed, iv(g))) for g in G)
    fr = [0]; DG = {0}
    while fr:
        nf = []
        for a in fr:
            for g in congens:
                b = mul(a, g)
                if b not in DG: DG.add(b); nf.append(b)
        fr = nf
    # [Q,Q] = normal closure in Q of [s1,s2]
    seedQ = comm(S1, S2)
    congensQ = set(mul(g, mul(seedQ, iv(g))) for g in range(deg))
    DQ = {0}; fr = [0]
    while fr:
        nf = []
        for a in fr:
            for g in congensQ:
                b = mul(a, g)
                if b not in DQ: DQ.add(b); nf.append(b)
        fr = nf
    Z = [q for q in range(deg) if mul(q, S1) == mul(S1, q) and mul(q, S2) == mul(S2, q)]
    ordc = min(e for e in range(1, 200) if power(C, e) == 0)
    print("  |G|=%d |[G,G]|=%d |[Q,Q]|=%d |Q^ab|=%d |Z(Q)|=%d ord(c)=%d"
          % (len(G), len(DG), len(DQ), deg//len(DQ), len(Z), ordc))

    def hexok(m, f):
        u = 2*m+1; fi = iv(f)
        L3 = mul(power(S1, u), mul(fi, mul(power(S2, u), f)))
        R3 = mul(fi, mul(mul(S1, S2), mul(power(XI, -m), power(C, m))))
        L4 = mul(fi, mul(power(S2, u), mul(f, power(S1, u))))
        R4 = mul(mul(S2, S1), mul(power(YI, -m), mul(power(C, m), f)))
        return L3 == R3 and L4 == R4
    shadows = [(m, f) for m in range(N_ORD) for f in G if hexok(m, f) and f in DG]
    print("  |GT(N)| =", len(shadows), " m-histogram:", sorted(Counter(m for m, _ in shadows).items()))

    # precompute conjugation data: for each q, (q s1 q^-1, q s2 q^-1)
    conj = {}
    for q in range(deg):
        qi = iv(q)
        conj.setdefault((mul(q, mul(S1, qi)), mul(q, mul(S2, qi))), []).append(q)

    def wstr(ww):
        s = ''
        for L, e in ww: s += L + ('' if e == 1 else '^%d' % e)
        return s or '1'

    inner = []; outer = []; witn = {}
    for (m, f) in shadows:
        u = 2*m+1; A = power(S1, u); Bm = mul(iv(f), mul(power(S2, u), f))
        qs = conj.get((A, Bm))
        if qs: inner.append((m, f)); witn[(m, f)] = qs
        else: outer.append((m, f))
    print("  INNER %d / %d ; non-inner m-hist: %s" % (len(inner), len(shadows),
          sorted(Counter(m for m, _ in outer).items())))
    # family
    def fam(nu): return mul(power(YI, nu), power(XI, -nu))
    ordfam = min(nu for nu in range(1, 60) if fam(nu) == 0)
    print("  family f_nu=y^nu x^-nu : smallest nu>0 with f_nu=1 in G is", ordfam)
    famimgs = {fam(nu): nu for nu in range(ordfam)}
    print("  inner elements:")
    for (m, f) in inner:
        qs = witn[(m, f)]
        nus = [nu for nu in range(ordfam) if fam(nu) == f]
        # try to name a witness q
        names = []
        for a in range(-6, 7):
            if power(XI, a) in qs: names.append('x^%d' % a)
            if power(YI, a) in qs: names.append('y^%d' % a)
            if mul(power(C, a), 0) in qs and a: names.append('c^%d' % a)
        for a in range(-4, 5):
            for b in range(-4, 5):
                q = mul(power(XI, a), power(YI, b))
                if q in qs and (a or b): names.append('x^%d y^%d' % (a, b))
        print("    m=%2d  f=%-20s  fam_nu=%s  #q=%d  q-names(sample)=%s"
              % (m, wstr(words[f]), nus, len(qs), names[:6]))
    print("  inner set == fake-torus image {[0,f_nu]}? ",
          set(inner) == set((0, fam(nu)) for nu in range(ordfam)))
    RES[wk] = dict(shadows=shadows, inner=inner, words=words, ordfam=ordfam,
                   G=G, DG=DG, deg=deg)
    # subgroup? check closure of inner under (3.53)
    def wsub(ww, ix, iy):
        o = []
        for L, e in ww:
            img = ix if L == 'x' else iy
            b = img if e >= 0 else tuple((LL, -ee) for LL, ee in reversed(img))
            o += list(b)*abs(e)
        return tuple(o)
    def ev(ww):
        R = 0
        for L, e in ww: R = mul(R, power(XI if L == 'x' else YI, e))
        return R
    def compsh(A, B):
        m1, f1 = A; m2, f2 = B
        u1 = 2*m1+1; wf1 = words[f1]
        imgx = (('x', u1),); imgy = tuple((LL, -ee) for LL, ee in reversed(wf1)) + (('y', u1),) + wf1
        res = wf1 + wsub(words[f2], imgx, imgy)
        return ((2*m1*m2+m1+m2) % N_ORD, ev(res))
    S = set(shadows); IS = set(inner)
    closed = all(compsh(a, b) in IS for a in inner for b in inner)
    print("  inner set closed under (3.53)? ", closed)
