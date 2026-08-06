from fractions import Fraction
# LCS ranks phi_k from prod_k (1-t^k)^{phi_k} = prod_{i=1}^{n-1} (1 - i t)
def series_mul(a,b,n):
    c=[0]*(n+1)
    for i,x in enumerate(a):
        if i>n: break
        for j,y in enumerate(b):
            if i+j>n: break
            c[i+j]+=x*y
    return c
def pow_series(base,e,n):
    r=[1]+[0]*n
    for _ in range(abs(e)):
        r=series_mul(r,base,n)
    if e<0:
        # invert
        inv=[0]*(n+1); inv[0]=Fraction(1,1)
        for k in range(1,n+1):
            s=0
            for j in range(1,k+1):
                s+=r[j]*inv[k-j]
            inv[k]=-s/r[0]
        r=[Fraction(x) for x in inv]
    return r
def lcs_ranks(n, deg):
    # target = prod_{i=1}^{n-1}(1 - i t)
    tgt=[Fraction(1)]+[Fraction(0)]*deg
    for i in range(1,n):
        tgt=series_mul(tgt,[Fraction(1),Fraction(-i)]+[Fraction(0)]*deg,deg)
    phi=[]
    cur=tgt
    for k in range(1,deg+1):
        pk=-cur[k]
        phi.append(pk)
        # divide by (1-t^k)^{pk}
        f=[Fraction(0)]*(deg+1); f[0]=Fraction(1); f[k]=Fraction(-1)
        cur=series_mul(cur,pow_series(f,-int(pk),deg),deg)
    return phi
print("PB_4 LCS ranks (deg1..6):",[int(x) for x in lcs_ranks(4,6)])
print("PB_3 LCS ranks (deg1..6):",[int(x) for x in lcs_ranks(3,6)])
p4=[int(x) for x in lcs_ranks(4,4)]
print("sum deg<=4 for PB4:",sum(p4), "=> |PB4 : gamma5 PB4^7| = 7^%d"%sum(p4))
print("K(0,5) = PB4/Z  => ranks", [p4[0]-1]+p4[1:], "sum", sum([p4[0]-1]+p4[1:]))
# free 2-generator (F2) ranks (Witt numbers) for comparison
def witt(r,k):
    from sympy import mobius, divisors
    return sum(mobius(d)*r**(k//d) for d in divisors(k))//k
try:
    print("Witt(2,k) k=1..5:",[witt(2,k) for k in range(1,6)])
except Exception as e:
    print("witt skipped",e)
