from itertools import product
N=5
def pmul(a,b): return tuple(b[a[i]] for i in range(len(a)))
def pinv(a):
    r=[0]*len(a)
    for i,j in enumerate(a): r[j]=i
    return tuple(r)
ID=tuple(range(15))
r5=tuple((j+1)%N for j in range(N)); s5=tuple((N-j)%N for j in range(N))
def tr(p,i):
    l=list(range(15))
    for j in range(N): l[j+(i-1)*N]=p[j]+(i-1)*N
    return tuple(l)
def blockperm(pi):
    l=[0]*15
    for i in (1,2,3):
        for j in range(N): l[j+(i-1)*N]=j+(pi[i]-1)*N
    return tuple(l)
# F20 = AGL(1,5) on {0..4}: j -> a*j+b, a in {1,2,3,4}, b in {0..4}
F20=[tuple((a*j+b)%N for j in range(N)) for a in (1,2,3,4) for b in range(N)]
assert len(set(F20))==20
S3=[{1:a,2:b,3:c} for a,b,c in product((1,2,3),repeat=3) if len({a,b,c})==3]
x=pmul(pmul(tr(r5,1),tr(s5,2)),tr(s5,3))
y=pmul(pmul(tr(pmul(s5,r5),1),tr(r5,2)),tr(pmul(s5,r5),3))
# search space: N_{S15}(G5) <= F20 wr S3  (G5 orbits = the 3 blocks; N_{S5}(D5)=F20)
Wbig=[]
for d in product(F20,repeat=3):
    base=pmul(pmul(tr(d[0],1),tr(d[1],2)),tr(d[2],3))
    for pi in S3: Wbig.append(pmul(base,blockperm(pi)))
Wbig=list(set(Wbig))
print("|F20 wr S3| =",len(Wbig),"  (contains N_{S15}(G5))")
c1=[g for g in Wbig if pmul(g,g)==x]; c2=[g for g in Wbig if pmul(g,g)==y]
print("g^2 = x :",len(c1),"   g^2 = y :",len(c2))
def gen(gs):
    S={ID}; fr=[ID]
    while fr:
        nf=[]
        for X in fr:
            for t in gs:
                Y=pmul(X,t)
                if Y not in S: S.add(Y); nf.append(Y)
        fr=nf
    return S
def cyc(p):
    seen,out=set(),[]
    for st in range(15):
        if st in seen: continue
        c,cur=[],st
        while cur not in seen: seen.add(cur); c.append(cur+1); cur=p[cur]
        if len(c)>1: out.append("("+",".join(map(str,c))+")")
    return "".join(out) or "()"
sols=[]
for g1 in c1:
    for g2 in c2:
        if pmul(pmul(g1,g2),g1)!=pmul(pmul(g2,g1),g2): continue
        D=pmul(pmul(g1,g2),g1)
        if pmul(D,D)!=ID: continue
        sols.append((g1,g2,len(gen([g1,g2,pinv(g1),pinv(g2)]))))
print("\npairs with braid + c->1 in F20 wr S3 :",len(sols))
for g1,g2,n in sols:
    print("   s1=%s  s2=%s  |<s1,s2>|=%d"%(cyc(g1),cyc(g2),n))
