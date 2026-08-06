# Delta_4^2 product presentation, verified in the FAITHFUL Artin representation B_n -> Aut(F_n).
# Free group F_4 on t1..t4; word = tuple of (i,e) with i in 1..4, e = +-1 ; free reduction.
def red(w):
    out=[]
    for g in w:
        if out and out[-1][0]==g[0] and out[-1][1]==-g[1]: out.pop()
        else: out.append(g)
    return tuple(out)
def mul(*ws):
    r=[]
    for w in ws: r+=list(w)
    prev=None; cur=tuple(r)
    while prev!=cur: prev=cur; cur=red(cur)
    return cur
def inv(w): return tuple((i,-e) for i,e in reversed(w))
T=lambda i:((i,1),)
N=4
ID=tuple(T(i) for i in range(1,N+1))              # automorphism = tuple of images of t1..tN
def apply(phi,w):                                  # phi applied to a word
    parts=[]
    for i,e in w:
        u=phi[i-1]
        parts.append(u if e==1 else inv(u))
    return mul(*parts)
def comp(phi,psi):  return tuple(apply(phi,psi[k]) for k in range(N))   # (phi o psi)(t)=phi(psi(t))
def sigma(i,sign=1):
    img=list(ID)
    if sign==1:
        img[i-1]=mul(T(i),T(i+1),inv(T(i)));  img[i]=T(i)
    else:
        img[i-1]=T(i+1);                      img[i]=mul(inv(T(i+1)),T(i),T(i+1))
    return tuple(img)
def word(*gens):
    r=ID
    for g in gens: r=comp(r,g)
    return r
s=lambda i: sigma(i,1); si=lambda i: sigma(i,-1)
# sanity: braid relations
assert word(s(1),s(2),s(1))==word(s(2),s(1),s(2))
assert word(s(1),s(3))==word(s(3),s(1))
assert word(s(1),si(1))==ID
print("braid relations in Aut(F4): OK  (Artin rep is faithful - Artin 1947)")
# x_ij  (A.2)
x12=word(s(1),s(1)); x23=word(s(2),s(2)); x34=word(s(3),s(3))
x13=word(s(2),s(1),s(1),si(2)); x24=word(s(3),s(2),s(2),si(3))
x14=word(s(3),s(2),s(1),s(1),si(2),si(3))
D2 =word(*([s(1),s(2),s(3)]*4))                    # Delta_4^2 = (s1 s2 s3)^4
c  =word(s(1),s(2),s(1),s(2),s(1),s(2))            # (s1 s2)^3
print("c = (s1s2)^3 == x12*x13*x23 :", c==word(x12,x13,x23), "   == x23*x12*x13 :", c==word(x23,x12,x13))
print("[x14,x23]=1 (nested pair, A.3)      :", word(x14,x23)==word(x23,x14))
print("Delta^2 == x12*(x13 x23)*(x14 x24 x34) = c*(x14x24x34) :", D2==word(c,x14,x24,x34))
print("Delta^2 == (x12 x13 x14)(x23 x24)(x34)                 :", D2==word(x12,x13,x14,x23,x24,x34))
print("Delta^2 central in PB4 (checked vs all 6 x_ij)         :",
      all(word(D2,g)==word(g,D2) for g in [x12,x13,x14,x23,x24,x34]))
