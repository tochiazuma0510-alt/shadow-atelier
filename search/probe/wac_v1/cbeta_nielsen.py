# C-beta stage 3' validation: is the Nielsen class in M_7 (degree-14 action) a single orbit?
# If yes, the model's monodromy triple is pinned by ALGEBRAIC local data alone
# (no analytic continuation, no path tracking).
import itertools, sys
QTAB = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]

def build(n, alpha):
    def enc(v,q): return ((v[0]*n+v[1])*n+v[2])*4+q
    def dec(x):
        q=x%4; x//=4; c=x%n; x//=n; return (x//n, x%n, c), q
    def act(q,v):
        if q==0: return v
        return tuple(v[j] if (j+1)==q else (-v[j])%n for j in range(3))
    def mul(x,y):
        v,q=dec(x); w,r=dec(y); aw=act(q,w)
        return enc(tuple((v[j]+aw[j])%n for j in range(3)), QTAB[q][r])
    def inv(x):
        v,q=dec(x); return enc(act(q,tuple((-t)%n for t in v)), q)
    G=list(range(4*n**3))
    U=[((alpha*t)%n, s%n, t%n) for s in range(n) for t in range(n)]
    H=[enc(v,q) for v in U for q in (0,2)]
    def coset(g): return min(mul(g,h) for h in H)
    cid={}; reps=[]; canon={}
    for g in G:
        c=coset(g)
        if c not in cid: cid[c]=len(reps); reps.append(c)
        canon[g]=cid[c]
    L=len(reps)
    def perm(g): return tuple(canon[mul(g,reps[k])] for k in range(L))
    X=enc((1,0,0),1); Y=enc((1,1,1),2); Z=inv(mul(X,Y))
    M=set()                                # monodromy group = image in Sym(L)
    for g in G: M.add(perm(g))
    return L, perm(X), perm(Y), perm(Z), sorted(M)

def pmul(a,b): return tuple(a[b[i]] for i in range(len(a)))   # (a*b)(i) = a(b(i))
def pinv(a):
    r=[0]*len(a)
    for i,v in enumerate(a): r[v]=i
    return tuple(r)
def ctype(p):
    n=len(p); seen=[False]*n; t=[]
    for s in range(n):
        if seen[s]: continue
        c=0; x=s
        while not seen[x]: seen[x]=True; x=p[x]; c+=1
        t.append(c)
    return tuple(sorted(t, reverse=True))

def run(n, alpha, verbose=True):
    L, X, Y, Z, M = build(n, alpha)
    Mset=set(M)
    def cls(g): return frozenset(pmul(pmul(c,g),pinv(c)) for c in M)
    C0, C1, Ci = cls(X), cls(Y), cls(Z)
    ID=tuple(range(L))
    # enumerate Nielsen class
    triples=[]
    for g0 in C0:
        for g1 in C1:
            gi=pinv(pmul(g0,g1))
            if gi in Ci:
                # generation check
                gen={ID}; frontier=[ID]
                while frontier:
                    x=frontier.pop()
                    for s in (g0,g1,pinv(g0),pinv(g1)):
                        y=pmul(x,s)
                        if y not in gen: gen.add(y); frontier.append(y)
                if len(gen)==len(M):
                    triples.append((g0,g1,gi))
    # orbits under simultaneous M-conjugation
    seen=set(); orbits=[]
    for t in triples:
        if t in seen: continue
        orb=set()
        for c in M:
            ci=pinv(c)
            orb.add(tuple(pmul(pmul(c,g),ci) for g in t))
        seen |= orb; orbits.append(orb)
    # orbits under N_{Sym(L)}(M) : approximate by conjugating by all elements of Sym(L)
    # that normalise M -- computed as the setwise stabiliser via a generating search is
    # expensive; instead report whether (X,Y,Z) is in one of the orbits.
    inXYZ = any((X,Y,Z) in o for o in orbits)
    if verbose:
        print(dict(n=n, alpha=alpha, deg=L, Morder=len(M),
                   type_X=ctype(X), type_Y=ctype(Y), type_Z=ctype(Z),
                   classes=(len(C0),len(C1),len(Ci)),
                   nielsen_triples=len(triples),
                   M_conj_orbits=len(orbits),
                   orbit_sizes=sorted(len(o) for o in orbits),
                   XYZ_in_class=inXYZ), flush=True)
    return len(orbits)

if __name__=="__main__":
    for (n,a) in ((3,1),(7,1),(7,2),(7,3)):
        run(n,a)
