"""Independent decode of the K3 witness export: linking-number abelianization (a,b,gamma),
evaluation in Q, hexagon-at-N check, reduction check f'' = f mod N_F2."""
import json, io, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
EXP = r"C:\Users\81905\Desktop\shadow-atelier\search\certs\koubou83_k3_witness_export_v1_20260822.json"
CERT = r"C:\Users\81905\Desktop\shadow-atelier\search\certs\koubou83_tref_window_export_v1_20260822.json"
d = json.load(io.open(CERT, encoding='utf-8'))
E = json.load(io.open(EXP, encoding='utf-8'))
N_ORD = 12

def linking(word):
    """word: list of +-1,+-2 (sigma_i^{+-1}). Returns (l12,l13,l23) or None if not pure."""
    pos = [1, 2, 3]          # pos[k] = strand occupying position k+1
    L = {(1,2):0, (1,3):0, (2,3):0}
    for a in word:
        i = abs(a); s = 1 if a > 0 else -1
        j, k = pos[i-1], pos[i]
        key = (min(j,k), max(j,k))
        L[key] += s
        pos[i-1], pos[i] = k, j
    if pos != [1,2,3]: return None
    for v in L.values():
        if v % 2: return None
    return (L[(1,2)]//2, L[(1,3)]//2, L[(2,3)]//2)

def abg(word):
    lk = linking(word)
    if lk is None: return None
    l12, l13, l23 = lk
    return (l12-l13, l23-l13, l13)      # (a,b,gamma) : elt = x^a y^b ... c^gamma  in PB3^ab

for wk, w in d['windows'].items():
    deg = w['degree']
    def to0(l): return [v-1 for v in l]
    s1a = to0(w['s1_perm_image_list']); s2a = to0(w['s2_perm_image_list'])
    ca = to0(w['c_perm_image_list']); Xa = to0(w['x12_perm_image_list']); Ya = to0(w['x23_perm_image_list'])
    ida = list(range(deg))
    def compa(A, B): return [A[B[i]] for i in range(deg)]
    def inva(A):
        r = [0]*deg
        for i, v in enumerate(A): r[v] = i
        return r
    Qs = {tuple(ida): ida}; fr = [ida]
    for g in ():
        pass
    gens = [s1a, s2a, inva(s1a), inva(s2a)]
    while fr:
        nf = []
        for A in fr:
            for g in gens:
                B = compa(A, g); t = tuple(B)
                if t not in Qs: Qs[t] = B; nf.append(B)
        fr = nf
    P = [None]*deg
    for A in Qs.values(): P[A[0]] = A
    def mul(i, j): return P[i][j]
    INVT = [0]*deg
    for i in range(deg):
        row = P[i]
        for j in range(deg):
            if row[j] == 0: INVT[i] = j; break
    def iv(i): return INVT[i]
    def power(i, e):
        r = 0; b = i if e >= 0 else iv(i)
        for _ in range(abs(e)): r = mul(b, r)
        return r
    S1 = s1a[0]; S2 = s2a[0]; C = ca[0]; XI = Xa[0]; YI = Ya[0]
    def evalw(word):
        """sigma-word (paper order, left-to-right = product w1 w2 ... ) -> element index"""
        r = 0
        for a in word:
            g = S1 if abs(a) == 1 else S2
            r = mul(r, power(g, 1 if a > 0 else -1))
        return r
    def hexok(m, f):
        u = 2*m+1; fi = iv(f)
        L3 = mul(power(S1, u), mul(fi, mul(power(S2, u), f)))
        R3 = mul(fi, mul(mul(S1, S2), mul(power(XI, -m), power(C, m))))
        L4 = mul(fi, mul(power(S2, u), mul(f, power(S1, u))))
        R4 = mul(mul(S2, S1), mul(power(YI, -m), mul(power(C, m), f)))
        return L3 == R3 and L4 == R4
    # subgroup G=<x,y> and [G,G]
    G = {0}; fr = [0]
    while fr:
        nf = []
        for a in fr:
            for g in (XI, YI, iv(XI), iv(YI)):
                b = mul(a, g)
                if b not in G: G.add(b); nf.append(b)
        fr = nf
    def comm(a, b): return mul(a, mul(b, mul(iv(a), iv(b))))
    cg = set(mul(g, mul(comm(XI, YI), iv(g))) for g in G)
    DG = {0}; fr = [0]
    while fr:
        nf = []
        for a in fr:
            for g in cg:
                b = mul(a, g)
                if b not in DG: DG.add(b); nf.append(b)
        fr = nf
    ordx = min(e for e in range(1, 200) if power(XI, e) == 0)
    ordy = min(e for e in range(1, 200) if power(YI, e) == 0)
    ordc = min(e for e in range(1, 200) if power(C, e) == 0)
    print("="*84)
    print("WINDOW", wk, " ord(x)=%d ord(y)=%d ord(c)=%d  |G|=%d |[G,G]|=%d  G^ab order=%d"
          % (ordx, ordy, ordc, len(G), len(DG), len(G)//len(DG)))
    # Lambda_N : kernel of Z^2 -> G^ab.  compute image of (a,b) -> x^a y^b mod [G,G]
    cos = {}
    for a in range(ordx):
        for b in range(ordy):
            e = mul(power(XI, a), power(YI, b))
            # coset of [G,G]
            key = frozenset(mul(e, t) for t in DG)
            cos.setdefault(key, []).append((a, b))
    print("  #cosets of [G,G] hit by x^a y^b =", len(cos))
    zero = None
    for k, v in cos.items():
        if (0, 0) in v: zero = v
    print("  Lambda_N (mod (ord x,ord y)) sample of (a,b) with x^a y^b in [G,G]:", sorted(zero)[:14])

    rows = E['windows'][wk]['rows']
    for name in ['PC-fam-n4', 'C6-elt2', 'C6-elt3', 'C6-elt4', 'C6-elt5', 'C6-elt6',
                 'm6-elt1', 'm6-elt2', 'm6-elt3', 'm6-elt4', 'm6-elt5', 'm6-elt6']:
        r = rows[name]
        fw = r['f_sigma']; ww = r['w']; kk = r['k']; fpp = r['fpp']; wm = r['witness_m']
        F = evalw(fw); FPP = evalw(fpp)
        red_ok = (F == FPP)
        print("  %-10s m=%d |f|=%d |w|=%d |k|=%d |f''|=%d  abg(f)=%s abg(w)=%s abg(k)=%s abg(f'')=%s"
              % (name, wm, len(fw), len(ww), len(kk), len(fpp),
                 abg(fw), abg(ww), abg(kk), abg(fpp)))
        print("      f in G? %s  f in [G,G]? %s  hexagon-at-N(m=%d,f)? %s  f''==f in Q? %s  f'' in [G,G]? %s"
              % (F in G, F in DG, wm, hexok(wm, F), red_ok, FPP in DG))
