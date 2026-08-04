# s3fam_check.py -- paper-side spot checks for (S3) family draft + K^(20) module addendum
# integer / GF(2) arithmetic only. single lane (python). NOT a cross-check, NOT verified.
from math import gcd
def phi(n):
    r=0
    for k in range(1,n+1):
        if gcd(k,n)==1: r+=1
    return r

fails=[]
def chk(name,cond,extra=""):
    if not cond: fails.append(name+" "+extra)

# ---- Part A: order bookkeeping for odd n (universe pre-registered: odd n in [3,201]) ----
UNIV=[n for n in range(3,202,2)]
rows=[]
for n in UNIV:
    GT=2*n*phi(n)                      # Thm 4.6 alpha=0 branch (n0=n)
    ph4=phi(4*n)                       # |(Z/4n)^x|
    lb=2*phi(n)                        # Thm 5.3 (5.4), alpha=0 branch: |GT_arith| >= 2 phi(n0)
    chk("A1 phi(4n)=2phi(n)",ph4==2*phi(n),f"n={n}")
    chk("A2 |GT|=n*phi(4n)",GT==n*ph4,f"n={n}")
    chk("A3 canonical lower bound = phi(4n)",lb==ph4,f"n={n}")
    chk("A4 gap factor = n",GT//lb==n and GT%lb==0,f"n={n}")
    # X_n = {m in [0,2n) : gcd(2m+1,2n)=1}; m -> 2m+1 bijection onto (Z/4n)^x
    X=[m for m in range(2*n) if gcd(2*m+1,2*n)==1]
    img=sorted({(2*m+1)%(4*n) for m in X})
    units=sorted([v for v in range(4*n) if gcd(v,4*n)==1])
    chk("A5 |X_n|=phi(4n)",len(X)==ph4,f"n={n}")
    chk("A6 m->2m+1 bijects X_n onto (Z/4n)^x",img==units,f"n={n}")
    rows.append((n,GT,ph4,lb,GT//lb))

# ---- Part B: GF(2) module V = ker(G_20 -> G_5), formulas (A)/(B)/(C) ----
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(3))%2 for j in range(3)] for i in range(3)]
I=[[1,0,0],[0,1,0],[0,0,1]]
def add(A,B): return [[(A[i][j]+B[i][j])%2 for j in range(3)] for i in range(3)]
def rank(M):
    M=[row[:] for row in M]; r=0
    for c in range(3):
        p=None
        for i in range(r,3):
            if M[i][c]: p=i;break
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        for i in range(3):
            if i!=r and M[i][c]:
                M[i]=[(M[i][j]+M[r][j])%2 for j in range(3)]
        r+=1
    return r
def nullity(M): return 3-rank(M)
def imgspace(M):   # set of images of all 8 vectors (as tuples), M acting on ROW vectors: v -> vM
    return {tuple(sum(v[i]*M[i][j] for i in range(3))%2 for j in range(3)) for v in
            [(a,b,c) for a in (0,1) for b in (0,1) for c in (0,1)]}
def kerspace(M):
    return {v for v in [(a,b,c) for a in (0,1) for b in (0,1) for c in (0,1)]
            if all(sum(v[i]*M[i][j] for i in range(3))%2==0 for j in range(3))}
def dim(S): # S a subspace given as a set of tuples
    import math; return int(round(math.log2(len(S))))

# cert matrices (search/certs/w6_coker_tool_20260804.json, part3_k20_module.module_data)
TH=[[0,1,0],[1,0,0],[0,0,1]]
TA=[[0,1,0],[0,0,1],[1,0,0]]
chk("B0 theta^2=I",mul(TH,TH)==I)
chk("B0 tau^3=I",mul(mul(TA,TA),TA)==I)
# row-vector convention v->vM must reproduce (4.7)(4.8) mod 2 : theta(b)=(b2,b1,b3), tau(b)=(b3,b1,b2)
def act(v,M): return tuple(sum(v[i]*M[i][j] for i in range(3))%2 for j in range(3))
for v in [(a,b,c) for a in (0,1) for b in (0,1) for c in (0,1)]:
    chk("B1 theta = (4.7) mod 2 (row conv)",act(v,TH)==(v[1],v[0],v[2]),str(v))
    chk("B1 tau   = (4.8) mod 2 (row conv)",act(v,TA)==(v[2],v[0],v[1]),str(v))

Nth=add(I,TH)                       # N_theta = 1+theta
Nta=add(add(I,TA),mul(TA,TA))       # N_tau   = 1+tau+tau^2
Vth=kerspace(add(TH,I))             # V^theta = ker(theta-1) = ker(theta+1) over F2
Vta=kerspace(add(TA,I))
dVth,dVta=dim(Vth),dim(Vta)
kNth,kNta=kerspace(Nth),kerspace(Nta)
both=kNth&kNta
dA=dVth+dVta-3+dim(both)                                   # formula (A)
d_direct=(dVth+dVta)-(3-dim(kerspace(Nth) & kerspace(Nta)))  # dim(V^th+V^ta) - dim im psi
im_psi=3-dim(both)
d_direct=dVth+dVta-im_psi
dB=dVta-dim({act(v,Nta) for v in kNth})                    # formula (B) -- requires p != 2
VG={v for v in [(a,b,c) for a in (0,1) for b in (0,1) for c in (0,1)]
    if act(v,TH)==v and act(v,TA)==v}
dC=dim(VG)                                                  # formula (C) -- requires p ł 6 (self-dual perm module)
chk("B2 dim V^theta=2",dVth==2,str(dVth))
chk("B3 dim V^tau=1",dVta==1,str(dVta))
chk("B4 dim(ker N_th & ker N_ta)=1",dim(both)==1,str(dim(both)))
chk("B5 formula (A) gives 1",dA==1,str(dA))
chk("B6 direct dim coker = 1",d_direct==1,str(d_direct))
chk("B7 cert coker_dim=1 agrees",dA==1)
chk("B8 formula (B) is WRONG at p=2 (gives 0)",dB==0,str(dB))
chk("B9 formula (C) numerically coincides (=1) though its hypothesis fails",dC==1,str(dC))
dBp=dVth-dim({act(v,Nth) for v in kNta})                   # formula (B') -- requires p != 3, so valid at p=2
chk("B9b formula (B') is valid at p=2 and gives 1",dBp==1,str(dBp))
# convention robustness: N_tau identical for tau and tau^{-1}
TAinv=mul(TA,TA)
chk("B10 N_tau(tau)=N_tau(tau^-1)",add(add(I,TAinv),mul(TAinv,TAinv))==Nta)

# ---- Part C: group orders for n=20 / n=5 (canonical |G_n| = 4n^3 odd, 4(n/2)^3 even) ----
chk("C1 |G_20|=4000",4*(20//2)**3==4000)
chk("C2 |G_5|=500",4*5**3==500)
chk("C3 |V|=8",4*(20//2)**3//(4*5**3)==8)
chk("C4 ker(Z/10 -> C_5, k->2k mod 5) has order 2",len([k for k in range(10) if (2*k)%5==0])==2)

print("universe: odd n in [3,201], |U| =",len(UNIV))
print("sample rows (n, |GT|=2n*phi(n), phi(4n), canonical LB 2phi(n), gap factor):")
for r in rows[:6]: print("  ",r)
print("dim V^theta,V^tau,ker&ker =",dVth,dVta,dim(both))
print("coker dims: (A)=",dA," direct=",d_direct," (Bprime)[valid at p=2]=",dBp," (B)[invalid at p=2]=",dB," (C)[invalid at p=2]=",dC)
print("FAILS =",len(fails))
for f in fails[:20]: print("  FAIL:",f)
print("RESULT:","ALL PASS" if not fails else "FAILURES")
