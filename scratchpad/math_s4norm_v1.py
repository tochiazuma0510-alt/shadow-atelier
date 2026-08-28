from sympy import sqrt, simplify, expand, Rational, symbols
print("=== gate: the S4 3-point normalisation factor is a PERFECT CUBE ===")
l = sqrt(-3)
print("  lambda = sqrt(-3) ;  (-lambda)^3 =", simplify(expand((-l)**3)), "  ; 3*sqrt(-3) =", simplify(3*l))
print("  (-sqrt(-3))^3 == 3*sqrt(-3) ?", simplify(expand((-l)**3) - 3*l) == 0)
print("  tau1,tau2 = 3/2 +- (3/2)sqrt(-3) : sum =", simplify(Rational(3,2)+l*Rational(3,2)+Rational(3,2)-l*Rational(3,2)),
      " prod =", simplify((Rational(3,2)+l*Rational(3,2))*(Rational(3,2)-l*Rational(3,2))))
print("  tau2 - tau1 =", simplify((Rational(3,2)-l*Rational(3,2))-(Rational(3,2)+l*Rational(3,2))), " = -3*sqrt(-3)")
print()
print("=== gate: mod p verification, p = 1 mod 9 ===")
def cube(z,p): return pow(z % p, (p-1)//3, p)
def sqrtm(a,p):
    a%=p
    for x in range(1,p):
        if x*x%p==a: return x
    return None
u0inv = (-1423828125, 256)          # u0^{-1} = -1423828125/256
primes=[19,37,73,109,127,163,181,199,271,307,373,397]
def val(fr,p): return (fr[0]%p)*pow(fr[1]%p,p-2,p)%p
ok_cube=ok_cprime=0; rows=[]
for p in primes:
    if p in (2,3,5): continue
    s3=sqrtm(p-3,p)                  # sqrt(-3) mod p
    if s3 is None: rows.append((p,"no sqrt(-3)",)); continue
    fac=(3*s3)%p                     # the normalisation factor 3*sqrt(-3)
    c_fac=cube(fac,p)
    u0i=val(u0inv,p); u0=pow(u0i,p-2,p)
    udih=val((1,128),p)              # 2^-7
    S_u0   = cube(u0,p)
    S_norm = cube(fac*u0%p,p)        # normalised u_S4 = (tau_k-tau_j)/Lambda = +-3sqrt(-3)*u0  (up to -1=cube)
    S_anc  = cube(udih,p)
    if S_anc==1 or S_u0==1: rows.append((p,"degenerate")); continue
    cp_raw  = 1 if S_u0==S_anc else 2
    cp_norm = 1 if S_norm==S_anc else 2
    ok_cube += (c_fac==1); ok_cprime += (cp_raw==cp_norm)
    rows.append((p,c_fac==1,cp_raw,cp_norm,cp_raw==cp_norm))
for r in rows: print("  p=%-4s cube(3sqrt-3)==1:%-6s c'(u0)=%-2s c'(norm)=%-2s agree:%s"%r if len(r)==5 else "  p=%s %s"%r)
print(f"  => normalisation factor is a cube at ALL tested primes : {ok_cube}/{len([r for r in rows if len(r)==5])}")
print(f"  => c' UNCHANGED by the 3-point normalisation           : {ok_cprime}/{len([r for r in rows if len(r)==5])}")
print()
print("=== gate: falsifier's sensitivity check (u_dih = 2^-7 vs 2^-8) ===")
for p in primes[:6]:
    a=cube(val((1,128),p),p); b=cube(val((1,256),p),p); u0=pow(val(u0inv,p),p-2,p); S=cube(u0,p)
    if S==1 or a==1: continue
    print(f"  p={p:4d}  c'(u_dih=2^-7) = {1 if S==a else 2}   c'(u_dih=2^-8) = {1 if S==b else 2}   flipped: {(1 if S==a else 2)!=(1 if S==b else 2)}")
