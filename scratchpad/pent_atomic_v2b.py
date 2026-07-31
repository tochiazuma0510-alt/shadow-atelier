# ATOMIC CONFRONTATION: run OUR refined evaluator (faithful Python port of
# search/probe/wac_v1/pent_t2t3_v2_20260731.g) on the THIRD-PARTY (Package GT)
# charming witnesses, under the four possible word-transfer conventions.
import json, io
from math import gcd

N = 8
def perm(cycles):
    p = list(range(N))
    for cyc in cycles:
        for i in range(len(cyc)):
            p[cyc[i]-1] = cyc[(i+1) % len(cyc)] - 1
    return tuple(p)
def mul(p, q): return tuple(q[p[i]] for i in range(N))      # GAP: first p, then q
def inv(p):
    r = [0]*N
    for i, v in enumerate(p): r[v] = i
    return tuple(r)
def pw(p, k):
    if k < 0: p, k = inv(p), -k
    r = tuple(range(N))
    for _ in range(k): r = mul(r, p)
    return r
def cyc_str(p):
    seen = [False]*N; out = []
    for i in range(N):
        if not seen[i] and p[i] != i:
            c = []; j = i
            while not seen[j]: seen[j] = True; c.append(j+1); j = p[j]
            out.append(tuple(c))
    return "()" if not out else "".join("("+",".join(map(str,c))+")" for c in out)
ONE = tuple(range(N))

# ---------- window (probe lines 33-52) ----------
tt = perm([(1,2,3)]); aa = perm([(1,4,5)])
XX = mul(aa, inv(tt)); ss = mul(tt, pw(XX,3))
aE = mul(ss, perm([(6,8)])); bE = mul(tt, perm([(6,8,7)]))
s1 = mul(inv(bE), aE); s2 = mul(aE, pw(bE,2)); cc = pw(mul(s1,s2),3)
xb = pw(s1,2); yb = pw(s2,2)
X12v, X23v = xb, yb
X13v = mul(inv(yb), inv(xb))            # yb^-1*xb^-1
X34v = xb
X24v = mul(mul(inv(s1), yb), s1)        # s1^-1*yb*s1
X14v = mul(mul(inv(s1), X13v), s1)
cof = [[X12v, X23v, X13v],
       [X23v, X34v, X24v],
       [mul(X23v, X13v), X34v, mul(X24v, X14v)],
       [mul(X13v, X12v), mul(X34v, X24v), X14v],
       [X12v, mul(X24v, X23v), mul(X14v, X13v)]]
cofc = [mul(mul(c[1], c[2]), c[0]) for c in cof]     # cof[i][2]*cof[i][3]*cof[i][1]

# ---------- free words on x,y,c ----------
def red(w):
    out = []
    for l in w:
        if out and out[-1][0] == l[0] and out[-1][1] == -l[1]: out.pop()
        else: out.append(l)
    return out
def mw(*ws):
    r = []
    for w in ws: r = red(r + w)
    return r
def iw(w): return red([(n, -s) for n, s in reversed(w)])
def pwr(w, k):
    if k < 0: w, k = iw(w), -k
    r = []
    for _ in range(k): r = mw(r, w)
    return r
def rev(w): return list(reversed(w))          # GAP LetterRep reversal
X, Y, C = [('x',1)], [('y',1)], [('c',1)]
def subst(w, mp):
    r = []
    for n, s in w: r = mw(r, mp[n] if s > 0 else iw(mp[n]))
    return r
X13w = mw(iw(X), C, iw(Y))                    # gx^-1*gc*gy^-1
def Aut1(w): return subst(w, {'x': X, 'y': mw(iw(Y), X13w, Y), 'c': C})
def Aut2(w): return subst(w, {'x': X13w, 'y': Y, 'c': C})

def PsiAt(w, i):
    im = {'x': cof[i][0], 'y': cof[i][1], 'c': cofc[i]}
    r = ONE
    for n, s in rev(w): r = mul(r, im[n] if s > 0 else inv(im[n]))
    return r
def Psi(w): return tuple(PsiAt(w, i) for i in range(5))
ONE5 = tuple(ONE for _ in range(5))
def mul5(a, b): return tuple(mul(a[i], b[i]) for i in range(5))
def inv5(a): return tuple(inv(x) for x in a)

def closure5(gens):
    S = {ONE5}; fr = [ONE5]
    while fr:
        nf = []
        for a in fr:
            for g in gens:
                b = mul5(a, g)
                if b not in S: S.add(b); nf.append(b)
        fr = nf
    return S
QP = closure5([Psi(X), Psi(Y), Psi(C)])
QF = closure5([Psi(X), Psi(Y)])
print("|QP| =", len(QP), " |QF| =", len(QF), " ord(Psi(c)) =",
      next(k for k in range(1, 30) if all(pw(Psi(C)[i], k) == ONE for i in range(5))))

# derived subgroup of QP (for c4)
gensQ = [Psi(X), Psi(Y), Psi(C)]
comms = [mul5(mul5(inv5(a), inv5(b)), mul5(a, b)) for a in gensQ for b in gensQ]
D = closure5([c for c in comms if c != ONE5])
# normal closure
changed = True
while changed:
    changed = False
    for g in gensQ:
        for d in list(D):
            e = mul5(mul5(inv5(g), d), g)
            if e not in D:
                D = closure5(list(D) + [e]); changed = True; break
        if changed: break
print("|[QP,QP]| =", len(D))

# ---------- our six conditions (Chk6 of the probe) ----------
def chk(m, w):
    u = 2*m + 1
    P0 = mw(pwr(X, m), iw(w), Aut2(mw(pwr(Y, m), w)))
    R0 = pwr(mw(X13w, Y), m)
    D1 = mw(Aut1(P0), iw(Aut1(Aut2(R0))), w)
    S0 = pwr(mw(X, X13w), m)
    D2 = mw(iw(w), Aut2(mw(pwr(Y, m), w)), Aut2(Aut1(pwr(X, m))),
            iw(mw(Aut2(Aut1(S0)), Aut2(Aut1(w)))))
    c1 = Psi(D1) == ONE5
    c2 = Psi(D2) == ONE5
    v = [PsiAt(w, i) for i in range(5)]
    c3 = mul(mul(v[0], v[3]), v[1]) == mul(v[2], v[4])
    q = Psi(w)
    c4 = q in D
    sb = closure5([Psi(pwr(X, u)), Psi(mw(iw(w), pwr(Y, u), w))])
    c5 = (len(sb) == len(QF))
    return c1, c2, c3, c4, c5, (c1 and c2 and c3 and c4 and c5)

# smoke test: our own identity witness (m=0 and m=4) must pass
for m in (0, 4):
    print(f"  self-test identity witness m={m}: {chk(m, [])}")

# ---------- third-party witnesses ----------
d = json.load(io.open('search/certs/pent_thirdparty_gt_20260731.json', encoding='utf-8'))
rows = d['coarse_reduction']['charming']['per_entry_rows']
lets = {0: ('x', 1), 1: ('y', 1), 2: ('c', 1)}   # package t = (x12,x23,x13,...)
def word_of(idxs): return red([lets[i] for i in idxs])

print("\n--- our evaluator on the 20 third-party charming witnesses ---")
tot = {k: 0 for k in ('w', 'rev', 'inv', 'revinv')}
for r in rows:
    w0 = word_of(r['word']); m = r['m']
    cands = {'w': w0, 'rev': rev(w0), 'inv': iw(w0), 'revinv': iw(rev(w0))}
    res = {k: chk(m, v) for k, v in cands.items()}
    for k, v in res.items(): tot[k] += 1 if v[5] else 0
    coarse = {k: cyc_str(PsiAt(v, 0)) for k, v in cands.items()}
    print(f"  m={m} len={len(r['word']):2d} | " +
          " | ".join(f"{k}: {''.join('1' if b else '0' for b in res[k][:5])}"
                     f"{'*' if res[k][5] else ' '} f1={coarse[k]}" for k in ('w','rev')))
print("\nfull-pass totals by transfer convention:", tot)

# ---------- fault-line confirmation: coarse enumerator in the REVERSED convention ----------
def closureP(gens):
    S={ONE}; fr=[ONE]
    while fr:
        nf=[]
        for a in fr:
            for g in gens:
                b=mul(a,g)
                if b not in S: S.add(b); nf.append(b)
        fr=nf
    return S
P = closureP([xb,yb])
def evalrev(seq):            # evaluate a list of (perm,exp) with REVERSED order
    r=ONE
    for p,e in reversed(seq): r=mul(r,pw(p,e))
    return r
def evalfwd(seq):
    r=ONE
    for p,e in seq: r=mul(r,pw(p,e))
    return r
def hex_conv(m,f,ev):
    u=2*m+1
    L1=ev([(s1,u),(f,-1),(s2,u),(f,1)]);  R1=ev([(f,-1),(s1,1),(s2,1),(xb,-m),(cc,m)])
    L2=ev([(f,-1),(s2,u),(f,1),(s1,u)]);  R2=ev([(s2,1),(s1,1),(yb,-m),(cc,m),(f,1)])
    return L1==R1 and L2==R2
for name,ev in (("fwd(GAP order, = probe's Hex)",evalfwd),("rev(paper order reversed)",evalrev)):
    sol=[(m,cyc_str(f)) for m in (0,1,3,4) for f in sorted(P)
         if hex_conv(m,f,ev) and closureP([xb,mul(mul(inv(f),yb),f)])==P]
    print(f"\ncoarse solutions [{name}]: n={len(sol)}")
    for m in (0,1,3,4): print("   m=%d:"%m, sorted(s for mm,s in sol if mm==m))
