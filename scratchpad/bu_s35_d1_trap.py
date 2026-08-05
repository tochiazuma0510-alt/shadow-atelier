from itertools import product
P=5
def mv(M,v): return tuple(sum(M[i][k]*v[k] for k in range(3))%P for i in range(3))
def mm(M,N): return tuple(tuple(sum(M[i][k]*N[k][j] for k in range(3))%P for j in range(3)) for i in range(3))
I3=((1,0,0),(0,1,0),(0,0,1))
TH=((0,1,0),(1,0,0),(0,0,4))
TA=((0,0,1),(1,0,0),(0,1,0))          # canon (4.8)
TAbad=mm(TA,TA)                       # tau^{-1}: the row-vector / GAP-transpose slip
def gmul(g,h):
    a,M=g; b,N=h
    return (tuple((a[i]+mv(M,b)[i])%P for i in range(3)), mm(M,N))
def ginv(g):
    a,M=g; Mi=M
    while mm(Mi,M)!=I3: Mi=mm(Mi,M)
    return (tuple((-x)%P for x in mv(Mi,a)),Mi)
E=((0,0,0),I3)
def gpow(g,n):
    r=E
    for _ in range(n): r=gmul(r,g)
    return r
def closure(gens):
    S={E}; fr=[E]
    while fr:
        nf=[]
        for X in fr:
            for t in gens:
                Y=gmul(X,t)
                if Y not in S: S.add(Y); nf.append(Y)
        fr=nf
    return S
for name,T in (("CANON  tau=(n3,n1,n2)",TA),("TRAP   tau=(n2,n3,n1)",TAbad)):
    u=((0,0,0),TH); v=((1,4,0),T)
    if gpow(v,3)!=E: v=((1,0,4),T)
    s1=gmul(ginv(v),u); s2=gmul(ginv(u),gpow(v,2))
    braid = gmul(gmul(s1,s2),s1)==gmul(gmul(s2,s1),s2)
    chat  = gpow(gmul(gmul(s1,s2),s1),2)==E
    n     = len(closure([s1,s2,ginv(s1),ginv(s2)]))
    print("%s :" % name)
    print("   L-1 braid=%s  L-2 c->1=%s  L-3 |<s1,s2>|=%d   <-- ALL BLIND to the slip"%(braid,chat,n))
    print("   Ad(sigma1^2)|A diag = %s   (MakeGn x=(r,s,s) demands (1,-1,-1))"
          % (tuple(mm(s1[1],s1[1])[i][i] for i in range(3)),))
    print("   Ad(sigma2^2)|A diag = %s   (MakeGn y=(sr,r,sr) demands (-1,1,-1))"
          % (tuple(mm(s2[1],s2[1])[i][i] for i in range(3)),))
