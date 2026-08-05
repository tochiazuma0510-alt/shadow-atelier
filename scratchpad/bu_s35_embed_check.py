"""BU S3.5 embedding check -- paper-algebra verification (integer arithmetic only).

Model 1: Ghat5 = F5^3 : S4  (signed-permutation action, canon (4.7)(4.8))
Model 2: Ghat5 <= D5 wr S3 acting on 15 points (same rep as MakeGn(5))

No repo data read; no GAP; no sealed quantity touched.
"""
from itertools import product

# ---------------------------------------------------------------- Model 1
# A = F5^3 written as column vectors; matrices act on the LEFT (canon convention).
P = 5
def mv(M, v):                       # matrix * column vector, mod 5
    return tuple(sum(M[i][k]*v[k] for k in range(3)) % P for i in range(3))
def mm(M, N):                       # matrix * matrix
    return tuple(tuple(sum(M[i][k]*N[k][j] for k in range(3)) % P for j in range(3))
                 for i in range(3))
I3 = ((1,0,0),(0,1,0),(0,0,1))
# (4.7) theta(n1,n2,n3) = (n2,n1,-n3)   = Ad(Delta) on A
TH = ((0,1,0),(1,0,0),(0,0,-1 % P))
# (4.8) tau(n1,n2,n3)   = (n3,n1,n2)    = Ad(delta) on A
TA = ((0,0,1),(1,0,0),(0,1,0))

def matorder(M):
    k, X = 1, M
    while X != I3:
        X = mm(X, M); k += 1
    return k
assert matorder(TH) == 2 and matorder(TA) == 3
print("ord(theta|A)=%d ord(tau|A)=%d ord(theta*tau|A)=%d   [A-0 / GAMMA(a)]"
      % (matorder(TH), matorder(TA), matorder(mm(TH, TA))))

# enumerate Gamma|A = <TH,TA>
G = {I3}
frontier = [I3]
while frontier:
    nf = []
    for X in frontier:
        for M in (TH, TA):
            Y = mm(X, M)
            if Y not in G:
                G.add(Y); nf.append(Y)
    frontier = nf
print("|<theta|A, tau|A>| = %d   [GAMMA(b): expect 24]" % len(G))
assert len(G) == 24

# semidirect product elements (a; M), a in F5^3, M in G ; (a;M)(b;N) = (a + M b; MN)
def gmul(g, h):
    a, M = g; b, N = h
    return (tuple((a[i] + mv(M, b)[i]) % P for i in range(3)), mm(M, N))
def ginv(g):
    a, M = g
    Mi = M
    while mm(Mi, M) != I3: Mi = mm(Mi, M)   # M^(ord-1)
    return (tuple((-x) % P for x in mv(Mi, a)), Mi)
E = ((0,0,0), I3)
def gpow(g, n):
    r = E
    for _ in range(n): r = gmul(r, g)
    return r
def gorder(g):
    k, X = 1, g
    while X != E:
        X = gmul(X, g); k += 1
    return k
def closure(gens):
    S = {E}; frontier = [E]
    while frontier:
        nf = []
        for X in frontier:
            for t in gens:
                Y = gmul(X, t)
                if Y not in S:
                    S.add(Y); nf.append(Y)
        frontier = nf
    return S

# ---- H^1(C2*C3, A): pairs (alpha,beta) with (1+TH)alpha=0, (1+TA+TA^2)beta=0
Z1 = [(al, be) for al in product(range(P), repeat=3) for be in product(range(P), repeat=3)
      if all(v == 0 for v in [ (al[i]+mv(TH,al)[i]) % P for i in range(3) ])
      and all(v == 0 for v in [ (be[i]+mv(TA,be)[i]+mv(mm(TA,TA),be)[i]) % P for i in range(3) ])]
B1 = set()
for g in product(range(P), repeat=3):
    a = tuple((g[i] - mv(TH, g)[i]) % P for i in range(3))
    b = tuple((g[i] - mv(TA, g)[i]) % P for i in range(3))
    B1.add((a, b))
print("|Z^1| = %d  |B^1| = %d  |H^1(C2*C3,A)| = %d" % (len(Z1), len(B1), len(Z1)//len(B1)))

gen_ok, gen_bad = [], []
for (al, be) in Z1:
    u = (al, TH); v = (be, TA)
    n = len(closure([u, v, ginv(u), ginv(v)]))
    (gen_ok if n == 3000 else gen_bad).append(((al, be), n))
print("pairs (alpha,beta) in Z^1: %d total ; %d generate Ghat5 (order 3000) ; %d do not"
      % (len(Z1), len(gen_ok), len(gen_bad)))
print("   non-generating orders seen: %s" % sorted({n for _, n in gen_bad}))

# ---- the normalised choice: alpha = 0, beta = (1,-1,0) = f1 coordinates
u = ((0,0,0), TH)                      # Delta-hat
v = ((1, P-1, 0), TA)                  # delta-hat
assert gpow(u, 2) == E, "Delta^2 != 1"
assert gpow(v, 3) == E, "delta^3 != 1"
s1 = gmul(ginv(v), u)                  # sigma1 = delta^{-1} Delta
s2 = gmul(ginv(u), gpow(v, 2))         # sigma2 = Delta^{-1} delta^2
print("\n--- Model 1 (F5^3 : S4) ---")
print("sigma1-hat = (%s ; matrix %s)" % (s1[0], s1[1]))
print("sigma2-hat = (%s ; matrix %s)" % (s2[0], s2[1]))
lhs = gmul(gmul(s1, s2), s1); rhs = gmul(gmul(s2, s1), s2)
print("braid  s1 s2 s1 == s2 s1 s2 :", lhs == rhs, " and == Delta-hat :", lhs == u)
print("c-hat = (s1 s2 s1)^2 == 1 :", gpow(lhs, 2) == E)
print("s1 s2 == delta-hat :", gmul(s1, s2) == v)
full = closure([s1, s2, ginv(s1), ginv(s2)])
print("|<sigma1-hat, sigma2-hat>| =", len(full), "  [expect 3000]")
print("ord(sigma1-hat)=%d ord(sigma2-hat)=%d ord(x-hat)=%d ord(y-hat)=%d"
      % (gorder(s1), gorder(s2), gorder(gpow(s1, 2)), gorder(gpow(s2, 2))))
print("x-hat = sigma1^2 = (%s ; %s)" % (gpow(s1,2)[0], gpow(s1,2)[1]))
print("y-hat = sigma2^2 = (%s ; %s)" % (gpow(s2,2)[0], gpow(s2,2)[1]))

# ---- S4 labels via the four cube diagonals
diag = {1: (1,1,-1), 2: (1,1,1), 3: (-1,1,1), 4: (1,-1,1)}
def norm(vv):
    vv = tuple(((x + P) % P) for x in vv)
    # represent +-class canonically
    alt = tuple((-x) % P for x in vv)
    return min(vv, alt)
lab = {norm(d): k for k, d in diag.items()}
def perm_of(M):
    return tuple(lab[norm(mv(M, tuple(x % P for x in diag[k])))] for k in (1,2,3,4))
def cyc(p):                            # p is image tuple for 1..4
    seen, out = set(), []
    for st in range(1, 5):
        if st in seen: continue
        c, cur = [], st
        while cur not in seen:
            seen.add(cur); c.append(cur); cur = p[cur-1]
        if len(c) > 1: out.append(tuple(c))
    return out
print("\nS4 labels under diagonal labelling l(1)=[1:1:-1] l(2)=[1:1:1] l(3)=[-1:1:1] l(4)=[1:-1:1]")
for nm, M in (("Delta (theta)", TH), ("delta (tau)", TA),
              ("sigma1", s1[1]), ("sigma2", s2[1]), ("theta*tau", mm(TH, TA))):
    print("   %-14s -> %s" % (nm, cyc(perm_of(M)) or "id"))

# ---------------------------------------------------------------- Model 2
# D5 wr S3 on 15 points, identical layout to MakeGn(5): block i = points 5(i-1)+1..5i
print("\n--- Model 2 (D5 wr S3 on 15 points, MakeGn(5) layout) ---")
N = 5
def pmul(a, b):                        # (a*b)(i) = b(a(i))  -- GAP right-action convention
    return tuple(b[a[i]] for i in range(len(a)))
def pinv(a):
    r = [0]*len(a)
    for i, j in enumerate(a): r[j] = i
    return tuple(r)
ID15 = tuple(range(15))
r5 = tuple((j + 1) % N for j in range(N))                 # (1,2,3,4,5)
s5 = tuple(((N - j) % N) for j in range(N))               # fixes 1, = (2,5)(3,4)
assert pmul(pmul(s5, r5), pinv(s5)) == pinv(r5)
def tr(p, i):                                             # p on block i (1-based)
    l = list(range(15))
    for j in range(N): l[j + (i-1)*N] = p[j] + (i-1)*N
    return tuple(l)
def blockperm(pi):                                        # pi: dict on {1,2,3}
    l = [0]*15
    for i in (1,2,3):
        for j in range(N): l[j + (i-1)*N] = j + (pi[i]-1)*N
    return tuple(l)
D5 = []
for k in range(N):
    rk = ID15
    rr = tuple((j + k) % N for j in range(N))
    D5.append(rr)
    D5.append(pmul(s5, rr))
D5 = [tuple(d) for d in D5]
assert len(set(D5)) == 10
S3 = [{1:a,2:b,3:c} for a,b,c in product((1,2,3),repeat=3) if len({a,b,c}) == 3]

x = pmul(pmul(tr(r5,1), tr(s5,2)), tr(s5,3))              # MakeGn: x = sigma1^2
y = pmul(pmul(tr(pmul(s5,r5),1), tr(r5,2)), tr(pmul(s5,r5),3))   # y = sigma2^2
W = []
for d1, d2, d3 in product(D5, repeat=3):
    base = pmul(pmul(tr(d1,1), tr(d2,2)), tr(d3,3))
    for pi in S3:
        W.append(pmul(base, blockperm(pi)))
W = list(set(W))
print("|D5 wr S3| =", len(W))
def pgen(gens):
    S = {ID15}; fr = [ID15]
    while fr:
        nf = []
        for X in fr:
            for t in gens:
                Y = pmul(X, t)
                if Y not in S: S.add(Y); nf.append(Y)
        fr = nf
    return S
cand1 = [g for g in W if pmul(g, g) == x]
cand2 = [g for g in W if pmul(g, g) == y]
print("solutions of g^2 = x : %d ;  g^2 = y : %d" % (len(cand1), len(cand2)))
sols = []
for g1 in cand1:
    for g2 in cand2:
        if pmul(pmul(g1,g2),g1) != pmul(pmul(g2,g1),g2): continue
        D = pmul(pmul(g1,g2),g1)
        if pmul(D,D) != ID15: continue
        n = len(pgen([g1,g2,pinv(g1),pinv(g2)]))
        sols.append((g1,g2,n))
print("pairs with braid + c->1 : %d   orders: %s" % (len(sols), sorted({n for *_ , n in sols})))
def cycles(p):
    seen, out = set(), []
    for st in range(15):
        if st in seen: continue
        c, cur = [], st
        while cur not in seen:
            seen.add(cur); c.append(cur+1); cur = p[cur]
        if len(c) > 1: out.append(tuple(c))
    return out
def porder(p):
    k, X = 1, p
    while X != ID15: X = pmul(X, p); k += 1
    return k
for (g1, g2, n) in sols:
    if n != 3000: continue
    D = pmul(pmul(g1,g2),g1); dl = pmul(g1,g2)
    print("  sigma1 = %s   ord=%d" % (cycles(g1), porder(g1)))
    print("  sigma2 = %s   ord=%d" % (cycles(g2), porder(g2)))
    print("  Delta  = %s   ord=%d" % (cycles(D), porder(D)))
    print("  delta  = %s   ord=%d" % (cycles(dl), porder(dl)))
    print("  |<s1,s2>| = %d ; s1^2 == x : %s ; s2^2 == y : %s"
          % (n, pmul(g1,g1) == x, pmul(g2,g2) == y))
    print()

# ---- cross-model check: Ad(sigma1)|A pattern from MakeGn's x
# conjugation of A = <r>^3 by x = (r,s,s) is diag(+1,-1,-1)
print("cross-check  Ad(x)|A from MakeGn (r,s,s) = diag(1,-1,-1) ; "
      "from (4.7)(4.8): Ad(sigma1^2) = %s" % (mm(s1[1], s1[1]),))
