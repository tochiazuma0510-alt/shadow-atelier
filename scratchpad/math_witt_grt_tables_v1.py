from fractions import Fraction as F
import math
def divisors(n): return [d for d in range(1,n+1) if n%d==0]
def mobius(n):
    r=1; m=n; p=2
    while p*p<=m:
        if m%p==0:
            m//=p
            if m%p==0: return 0
            r=-r
        p+=1
    if m>1: r=-r
    return r
def witt(n,d):
    s=sum(mobius(e)*d**(n//e) for e in divisors(n)); assert s%n==0; return s//n
print("Witt(free Lie, 2 gens) n=1..10:", [witt(n,2) for n in range(1,11)])

NMAX=30
c=[0]*(NMAX+1)
for w in range(3,NMAX+1,2): c[w]=1
H=[F(0)]*(NMAX+1); H[0]=F(1)
for n in range(1,NMAX+1): H[n]=sum(c[k]*H[n-k] for k in range(1,n+1))
# log H
LH=[F(0)]*(NMAX+1)
# log(1+u) with u = H-1
u=[H[i] for i in range(NMAX+1)]; u[0]=F(0)
pw=[F(0)]*(NMAX+1); pw[0]=F(1)   # u^0
term=[F(1)]+[F(0)]*NMAX
cur=[F(1)]+[F(0)]*NMAX
for k in range(1,NMAX+1):
    new=[F(0)]*(NMAX+1)
    for i in range(NMAX+1):
        if cur[i]==0: continue
        for j in range(1,NMAX+1-i):
            if u[j]==0: continue
            new[i+j]+=cur[i]*u[j]
    cur=new
    for i in range(NMAX+1): LH[i]+= F((-1)**(k+1),k)*cur[i]
a=[0]*(NMAX+1)
for n in range(1,NMAX+1):
    s=sum(mobius(n//d)*d*LH[d] for d in divisors(n))
    assert s.denominator==1 and s.numerator%n==0, (n,s)
    a[n]=s.numerator//n
print("dim A_w (free Lie on one gen each odd wt>=3), w=1..29:", a[1:30])
def zass(n,d,p):
    t=0;k=0
    while p**k<=n:
        if n%(p**k)==0: t+=witt(n//p**k,d)
        k+=1
    return t
print("Zassenhaus dims d=2,p=7,n=1..9:", [zass(n,2,7) for n in range(1,10)])
print("Zassenhaus dims d=2,p=3,n=1..9:", [zass(n,2,3) for n in range(1,10)])
print("sum witt n=1..4 (=log_7|P| for NW(7)):", sum(witt(n,2) for n in range(1,5)))
