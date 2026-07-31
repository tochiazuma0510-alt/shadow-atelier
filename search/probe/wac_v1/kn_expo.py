"""Rotation exponents of the D_n cover W->V, as a function of alpha."""
from kn_window import window
def comp(p,q): return tuple(p[q[i]] for i in range(len(q)))
def ctype(p):
    seen=set(); t=[]
    for i in range(len(p)):
        if i in seen: continue
        l=0;x=i
        while x not in seen: seen.add(x); x=p[x]; l+=1
        t.append(l)
    return tuple(sorted(t,reverse=True))

for n in (3,5,7,9,11):
    for alpha in range(1,(n-1)//2+1):
        w=window(n,alpha); pX,pY,pZ=w['perms']; d=2*n
        gens=[pY, comp(pX,pX)]
        orb={0}; fr=[0]
        while fr:
            nf=[]
            for x in fr:
                for g in gens:
                    if g[x] not in orb: orb.add(g[x]); nf.append(g[x])
            fr=nf
        B0=sorted(orb); B1=sorted(set(range(d))-orb)
        if len(B0)!=n: print(f"n={n} a={alpha}: no 2-block"); continue
        idx={v:i for i,v in enumerate(B0)}
        X2=comp(pX,pX); Z2=comp(pZ,pZ)
        rX2=tuple(idx[X2[v]] for v in B0); rZ2=tuple(idx[Z2[v]] for v in B0)
        if len(ctype(rX2))!=1:  # not an n-cycle
            print(f"n={n} a={alpha}: X^2|B0 type {ctype(rX2)}"); continue
        # relabel B0 by powers of rX2 from base point 0 -> rX2 becomes +1
        lab={}; x=0
        for i in range(n): lab[x]=i; x=rX2[x]
        # rZ2 in that labelling
        r0 = 1                              # exponent of X^2 (over m=0)
        rinf = (lab[rZ2[0]] - lab[0]) % n    # exponent of Z^2 (over m=inf)
        # consistency: rZ2 must be the same rotation everywhere
        ok = all((lab[rZ2[v]]-lab[v])%n == rinf for v in range(n))
        print(f"n={n} alpha={alpha}: exponents over (m=0, m=inf) = ({r0}, {rinf})  "
              f"rot-consistent={ok}   [check: rinf mod n vs -2/alpha? "
              f"alpha*rinf mod n = {(alpha*rinf)%n}]")
