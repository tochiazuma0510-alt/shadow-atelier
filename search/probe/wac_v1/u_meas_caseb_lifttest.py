# u_meas_caseb_lifttest.py -- do ANY F_7 points of the residual system lift to Z_7?
# Decisive between suspicion (i) (bad primes for t) and (ii) (I2 = -27/8 not exact).
import sys, json, math
from itertools import combinations, product
import sympy as sp
LOG=open(sys.argv[1],"w")
def log(s):
    print(s); LOG.write(str(s)+"\n"); LOG.flush()
x=sp.symbols('x'); c3,c5,c7,c9,h4,h2,h0=sp.symbols('c3 c5 c7 c9 h4 h2 h0')
CVAL = sp.Integer(sys.argv[2]) if len(sys.argv)>2 else sp.Integer(-27)
q=x**3+x; f6=sp.expand(q**2+CVAL)
U=sp.expand((c3+c5*x**2)*q+c7*x*(2*q**2+CVAL)+c9*(q**3+3*q*f6))
B=sp.expand(c3+c5*x**2+2*c7*x*q+c9*(3*q**2+f6))
P=sp.expand(U**2-B**2*f6-sp.Rational(27,4))
h=x**6+h4*x**4+h2*x**2+h0
LEAD=sp.expand(sp.LC(sp.Poly(sp.expand(P**2+27*U**2),x)))
pe=sp.Poly(sp.expand(sp.expand(P**2+27*U**2)-LEAD*h**3),x)
DEG=pe.degree(); cf={DEG-i:sp.expand(co) for i,co in enumerate(pe.all_coeffs())}
subs={}; tops=sorted([d for d in cf if d%2==0],reverse=True)[:3]
for deg,var in zip(tops,(h4,h2,h0)):
    subs[var]=sp.together(sp.solve(sp.Eq(sp.expand(cf[deg].subs(subs)),0),var,dict=True)[0][var])
EQS=[]
for deg in sorted([d for d in cf if d not in tops and d%2==0],reverse=True):
    e=sp.expand(sp.numer(sp.cancel(sp.together(cf[deg].subs(subs)))))
    if e!=0: EQS.append(e)
log("curve y^2=(x^3+x)^2%+d ; residual eqs: %s"%(CVAL,[int(sp.total_degree(e)) for e in EQS]))
VARS=(c3,c5,c7,c9); POLYS=[]
for e in EQS:
    pol=sp.Poly(e,*VARS); den=1
    for co in pol.coeffs(): den=sp.ilcm(den,sp.Rational(co).q)
    ip=sp.Poly(sp.expand(e*den),*VARS); ic=[int(v) for v in ip.coeffs()]
    v7=min((0 if v==0 else sp.multiplicity(7,abs(v))) for v in ic)
    POLYS.append({m:int(co)//7**v7 for m,co in zip(ip.monoms(),ic)})
def ev(d,c,M):
    s=0
    for m,co in d.items():
        tm=co%M
        for i,ei in enumerate(m):
            if ei: tm=tm*pow(c[i],ei,M)%M
        s=(s+tm)%M
    return s%M
def dev(d,c,M,j):
    s=0
    for m,co in d.items():
        if m[j]==0: continue
        tm=co*m[j]%M
        for i,ei in enumerate(m):
            e2=ei-1 if i==j else ei
            if e2: tm=tm*pow(c[i],e2,M)%M
        s=(s+tm)%M
    return s%M
def detmod(Mx,M):
    n=len(Mx); Mx=[r[:] for r in Mx]; det=1
    for i in range(n):
        piv=next((r for r in range(i,n) if Mx[r][i]%7!=0),None)
        if piv is None: return 0
        if piv!=i: Mx[i],Mx[piv]=Mx[piv],Mx[i]
        det=det*Mx[i][i]%M; inv=pow(Mx[i][i],-1,M)
        for r in range(i+1,n):
            f=Mx[r][i]*inv%M
            for cc in range(i,n): Mx[r][cc]=(Mx[r][cc]-f*Mx[i][cc])%M
    return det%M
def solve_lin(Mx,rhs,M):
    n=len(Mx); A=[row[:]+[rhs[i]] for i,row in enumerate(Mx)]
    for i in range(n):
        piv=next((r for r in range(i,n) if A[r][i]%7!=0),None)
        if piv is None: return None
        A[i],A[piv]=A[piv],A[i]; inv=pow(A[i][i],-1,M); A[i]=[v*inv%M for v in A[i]]
        for r in range(n):
            if r!=i and A[r][i]:
                f=A[r][i]; A[r]=[(A[r][cc]-f*A[i][cc])%M for cc in range(n+1)]
    return [A[i][n] for i in range(n)]
pts=[list(t) for t in product(range(7),repeat=4) if t[3]!=0 and all(ev(d,list(t),7)==0 for d in POLYS)]
log("F_7 points of the residual system with c9 != 0 : %d  -> %s"%(len(pts),pts[:20]))
lifted=[]
for c0 in pts:
    ch=None
    for combo in combinations(range(len(POLYS)),4):
        J=[[dev(POLYS[i],c0,7,j) for j in range(4)] for i in combo]
        if detmod(J,7)%7!=0: ch=combo; break
    if ch is None:
        log("  pt %s : Jacobian singular for every 4-subset (skip)"%c0); continue
    c=c0[:]; ok=True; kmax=1
    for k2 in (2,4,8,16):
        M=7**k2; c=[v%M for v in c]
        for _ in range(3):
            F=[ev(POLYS[i],c,M) for i in ch]
            J=[[dev(POLYS[i],c,M,j) for j in range(4)] for i in ch]
            dz=solve_lin(J,[(-f)%M for f in F],M)
            if dz is None: ok=False; break
            c=[(c[i]+dz[i])%M for i in range(4)]
        if not ok: break
        chk=[ev(POLYS[i],c,M) for i in range(len(POLYS)) if i not in ch]
        if any(v!=0 for v in chk): ok=False; break
        kmax=k2
    log("  pt %s driver=%s -> lifts to 7^%d %s"%(c0,list(ch),kmax,"OK" if ok else "(FAILS above)"))
    if ok: lifted.append((c0,c))
log("\n=== %d of %d F_7 points lift to 7^16 ==="%(len(lifted),len(pts)))
json.dump({"schema":"u-meas-caseb-lifttest/v1","sympy_version":sp.__version__,
  "curve":"y^2=(x^3+x)^2%+d"%CVAL,"n_F7_points":len(pts),"F7_points":[list(map(int,p)) for p in pts],
  "n_lifting_to_7^16":len(lifted),"u_touched":False,
  "verdict":"no F_7 point lifts -> the fixed curve carries no Z_7 solution" if not lifted else "at least one lifts"},
  open("search/certs/u_meas_caseb_lifttest_20260731.json","w"),indent=1,sort_keys=True)
LOG.close()
