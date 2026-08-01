# C-beta stage 3a/3b/3c: build the MODEL-SIDE monodromy group purely from the equations
# (Kummer theory over the V_4-Galois base C(k)/C(lambda)), then compare with the abstract
# window triple on 14 points.  No analytic continuation, no TOWER-n / KUM-n / TW-1 / SPLIT.
#
#   C(k)/C(lambda) is V_4-Galois:  sigma: k -> -k ,  theta: k -> 1/k    [verified algebraically]
#   h = (k-i)(k+1)^a / ((k+i)(k-1)^a) ,  g = (k+1)/(k-1)
#   h^sigma = h^{-1} ,  g^sigma = g^{-1} ,  h^theta = (-1)^{a+1} h^{-1} g^{2a} ,  g^theta = -g
#   => Abar = <[h],[g]> = F_7^2 ; Gal(L/C(k)) = Abar^dual ; M^mod = Abar^dual x| V_4 (split)
#   Action on characters (c_h, c_g):
#       sigma : (c_h, c_g) -> (-c_h, -c_g)
#       theta : (c_h, c_g) -> (-c_h + 2a c_g, c_g)
#   Hbar^mod = {(0,c_g)} u {(0,c_g)*sigma}   (order 14; stabiliser of C(W_0)=C(k,y)^iota)
import itertools, sys
sys.path.insert(0, ".")
from cbeta_nielsen import build as abstract_build, pmul, pinv, ctype

N = 7

def model_group(n, a):
    # V_4 elements coded 0=1, 1=sigma, 2=theta, 3=sigma*theta
    def vact(v, c):
        ch, cg = c
        if v == 0: return (ch % n, cg % n)
        if v == 1: return ((-ch) % n, (-cg) % n)
        if v == 2: return ((-ch + 2*a*cg) % n, cg % n)
        # sigma*theta
        return vact(1, vact(2, c))
    VT = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]
    # check the action is a V_4-action
    for v in range(4):
        for w in range(4):
            for c in [(1,0),(0,1)]:
                assert vact(VT[v][w], c) == vact(v, vact(w, c)), "not a V4 action"
    els = [((ch,cg), v) for ch in range(n) for cg in range(n) for v in range(4)]
    def mul(x, y):
        (c1,v1),(c2,v2) = x, y
        c = vact(v1, c2)
        return (((c1[0]+c[0]) % n, (c1[1]+c[1]) % n), VT[v1][v2])
    def inv(x):
        (c,v) = x
        ci = vact(v, ((-c[0]) % n, (-c[1]) % n))   # v^{-1} = v
        return (ci, v)
    # Hbar^mod
    Hm = [((0,cg), 0) for cg in range(n)] + [((0,cg), 1) for cg in range(n)]
    Hs = set(Hm)
    for x in Hm:
        for y in Hm:
            assert mul(x,y) in Hs, "Hbar^mod not a subgroup"
    # coset action
    def coset(g): return min(mul(g,h) for h in Hm)
    cid={}; reps=[]; canon={}
    for g in els:
        c = coset(g)
        if c not in cid: cid[c]=len(reps); reps.append(c)
        canon[g]=cid[c]
    L=len(reps)
    def perm(g): return tuple(canon[mul(g, reps[k])] for k in range(L))
    return els, mul, inv, perm, L, Hm

def canon_form(g0, g1, start):
    """BFS-canonical relabelling of a transitive 2-generated permutation triple."""
    L=len(g0); lab={start:0}; order=[start]; i=0
    while i < len(order):
        x=order[i]; i+=1
        for gg in (g0, g1):
            y=gg[x]
            if y not in lab: lab[y]=len(order); order.append(y)
    if len(lab)!=L: return None
    def rl(p): return tuple(lab[p[order[j]]] for j in range(L))
    return (rl(g0), rl(g1))

def run(a):
    els, mul, inv, perm, L, Hm = model_group(N, a)
    M = sorted({perm(g) for g in els})
    ID = tuple(range(L))
    # ---- 3b: local inertia data straight from the divisors ----
    # v_P(h), v_P(g) at the four ramification-relevant points of B_0 (k-coordinates)
    div = {"i": (1, 0), "-i": (-1, 0), "1": (-a, -1), "-1": (a, 1)}
    # V_4 inertia at each: which v in V_4 fixes the k-point
    #   k=i  fixed by sigma*theta (k -> -1/k)      -> over lambda = 0
    #   k=1  fixed by theta       (k -> 1/k)       -> over lambda = infinity
    #   k=0  fixed by sigma       (k -> -k)        -> over lambda = 1   (v_0(h)=v_0(g)=0)
    def inertia_elems(cvec, v):
        """all elements of M^mod projecting to v whose 'A-part direction' is <cvec>"""
        out=[]
        for t in range(N):
            for cg in range(N):     # free part along the unramified direction is NOT free:
                pass
        return out
    # Rather than derive the inertia generator by hand, use the intrinsic characterisation:
    # g_0 is an element of order 14 lying over v=3 (sigma*theta) whose 14th power is 1 and
    # which acts on the 14 cosets as a 14-cycle; g_inf likewise over v=2 (theta);
    # g_1 is an involution over v=1 (sigma) acting with type 2^6 1^2.
    def over(v): return [perm(g) for g in els if g[1]==v]
    C0 = [p for p in over(3) if ctype(p)==(2*N,)]
    Ci = [p for p in over(2) if ctype(p)==(2*N,)]
    C1 = [p for p in over(1) if ctype(p)==tuple([2]*(N-1)+[1,1])]
    triples=[]
    for g0 in C0:
        for g1 in C1:
            gi=pinv(pmul(g0,g1))
            if gi in Ci:
                gen={ID}; fr=[ID]
                while fr:
                    x=fr.pop()
                    for s in (g0,g1,pinv(g0),pinv(g1)):
                        y=pmul(x,s)
                        if y not in gen: gen.add(y); fr.append(y)
                if len(gen)==len(M): triples.append((g0,g1,gi))
    # M-conjugation orbits
    seen=set(); orbits=[]
    for t in triples:
        if t in seen: continue
        orb={tuple(pmul(pmul(c,x),pinv(c)) for x in t) for c in M}
        seen|=orb; orbits.append(orb)
    # ---- 5: compare with the abstract window triple on 14 points ----
    La, X, Y, Z, Mabs = abstract_build(N, a)
    cf_abs = canon_form(X, Y, 0)
    match = False
    for (g0,g1,gi) in triples:
        for s in range(L):
            if canon_form(g0,g1,s) == cf_abs:
                match = True; break
        if match: break
    print(dict(alpha=a, model_group_order=len(M), degree=L,
               model_Hbar_order=len(Hm),
               n_triples=len(triples), n_orbits=len(orbits),
               orbit_sizes=sorted(len(o) for o in orbits),
               abstract_group_order=len(Mabs), abstract_degree=La,
               MODEL_TRIPLE_MATCHES_ABSTRACT=match), flush=True)

if __name__=="__main__":
    for a in (1,2,3):
        run(a)
