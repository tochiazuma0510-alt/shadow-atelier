#!/usr/bin/env python3
# BH-BRIDGE independent check (integer arithmetic only; no window contact).
# Model: free group F2 = <x,y>.  Fox calculus into Z[F^ab] = Z[X^{+-1}, Y^{+-1}]
# (Laurent polynomials, monomial key = (i,j) meaning X^i Y^j).
# Facts checked:
#  (1) For w in F' the Fox pair is (d w/dx, d w/dy) = (-(Y-1)h, (X-1)h) with a
#      unique Laurent h  ==  the coordinate of the class of w in F'/F'' = Z[F^ab].theta'
#      (theta' = class of [x,y] = x y x^-1 y^-1, h(theta')=1).
#  (2) h([[x,y],x]) = -(X-1),   h([[x,y],y]) = -(Y-1).
#  (3) KEY IDENTITY:  for any f in F',  h([x, f^-1 y f]) = 1 + (X-1)(Y-1) h(f).
#  (4) theta(x<->y) acts on gr_3 by u1 -> -u2, u2 -> -u1  (D3-BLIND (b) input).
#  (5) the depth-3 hexagon locus {a=b} = Z.(u1+u2) is SATURATED in Z u1 + Z u2.

from itertools import product

# ---------- Laurent polynomials in X,Y over Z ----------
def lp(d):  return {k: v for k, v in d.items() if v != 0}
def add(a, b):
    r = dict(a)
    for k, v in b.items(): r[k] = r.get(k, 0) + v
    return lp(r)
def neg(a): return {k: -v for k, v in a.items()}
def mul(a, b):
    r = {}
    for (i, j), u in a.items():
        for (k, l), v in b.items():
            r[(i + k, j + l)] = r.get((i + k, j + l), 0) + u * v
    return lp(r)
ONE = {(0, 0): 1}
Xv  = {(1, 0): 1}
Yv  = {(0, 1): 1}
Xi  = {(1, 0): 1, (0, 0): -1}      # xi  = X - 1
Eta = {(0, 1): 1, (0, 0): -1}      # eta = Y - 1

def divide(a, b):
    """exact division of Laurent polys; returns None if not exact."""
    a = lp(dict(a)); b = lp(dict(b))
    if not b: raise ZeroDivisionError
    q = {}
    lead = max(b.keys())            # lexicographic leading term
    lc = b[lead]
    while a:
        t = max(a.keys()); tc = a[t]
        if tc % lc != 0: return None
        m = (t[0] - lead[0], t[1] - lead[1]); c = tc // lc
        q[m] = q.get(m, 0) + c
        a = add(a, neg(mul({m: c}, b)))
    return lp(q)

# ---------- free group words: list of (gen, exp) with gen in {'x','y'}, exp = +-1 ----------
def inv(w): return [(g, -e) for (g, e) in reversed(w)]
def cat(*ws):
    out = []
    for w in ws: out.extend(w)
    # free reduction
    r = []
    for t in out:
        if r and r[-1][0] == t[0] and r[-1][1] == -t[1]: r.pop()
        else: r.append(t)
    return r
def comm(a, b): return cat(a, b, inv(a), inv(b))     # [a,b] = a b a^-1 b^-1
X = [('x', 1)]; Y = [('y', 1)]

def ab(w):
    """image in F^ab as a monomial"""
    i = sum(e for (g, e) in w if g == 'x'); j = sum(e for (g, e) in w if g == 'y')
    return {(i, j): 1}

def fox(w, g):
    """Fox derivative d w / d g, abelianized, as Laurent poly."""
    res = {}; pref = ONE
    for (gen, e) in w:
        if e == 1:
            d = ONE if gen == g else {}
            res = add(res, mul(pref, d))
            pref = mul(pref, ab([(gen, 1)]))
        else:
            pref = mul(pref, ab([(gen, -1)]))
            d = neg(ab([(gen, -1)])) if gen == g else {}
            res = add(res, mul(mul(pref, mul(ab([(gen, 1)]), d)), ONE)) if False else add(res, mul(mul(pref, ab([(gen, 1)])), d))
    return lp(res)

def hcoord(w):
    """for w in F', return h with Fox pair = (-(Y-1)h, (X-1)h); verify both."""
    assert ab(w) == ONE, "word not in F' (abelianization nontrivial)"
    dy = fox(w, 'y'); dx = fox(w, 'x')
    h = divide(dy, Xi)
    assert h is not None, "d/dy not divisible by (X-1)"
    assert add(dx, mul(Eta, h)) == {}, "syzygy check failed"
    return h

# ---------- checks ----------
print("=== BH-BRIDGE independent check (exact integer/Laurent arithmetic) ===")

theta = comm(X, Y)
u1 = comm(theta, X)          # [[x,y],x]
u2 = comm(theta, Y)          # [[x,y],y]

h_theta = hcoord(theta)
h_u1 = hcoord(u1)
h_u2 = hcoord(u2)
print("(1) h([x,y])            =", h_theta, " expect {(0,0):1} :", h_theta == ONE)
print("(2) h([[x,y],x])        =", h_u1, " expect -(X-1)      :", h_u1 == neg(Xi))
print("    h([[x,y],y])        =", h_u2, " expect -(Y-1)      :", h_u2 == neg(Eta))

# (3) KEY IDENTITY, tested on several f in F' (including non-homogeneous ones)
tests = {
    "f=[[x,y],x]"          : u1,
    "f=[[x,y],y]"          : u2,
    "f=[[x,y],x]*[[x,y],y]": cat(u1, u2),
    "f=[x,y]"              : theta,
    "f=[[x,y],x]^-1"       : inv(u1),
    "f=[x,y]*[[x,y],y]^2"  : cat(theta, u2, u2),
    "f=[[[x,y],x],y]"      : comm(comm(theta, X), Y),
}
allok = True
for name, f in tests.items():
    w = comm(X, cat(inv(f), Y, f))                # [x, f^-1 y f]
    lhs = hcoord(w)
    rhs = add(ONE, mul(mul(Xi, Eta), hcoord(f)))
    ok = (lhs == rhs); allok &= ok
    print("(3) %-22s h([x,f^-1yf]) == 1+(X-1)(Y-1)h(f) : %s" % (name, ok))
print("(3) KEY IDENTITY all cases:", allok)

# (4) theta-involution (x<->y) on the two degree-3 basis words
def swap(w): return [('y' if g == 'x' else 'x', e) for (g, e) in w]
h_su1 = hcoord(swap(u1)); h_su2 = hcoord(swap(u2))
print("(4) h(theta(u1)) =", h_su1, " expect +(Y-1) (= class -u2):", h_su1 == Eta)
print("    h(theta(u2)) =", h_su2, " expect +(X-1) (= class -u1):", h_su2 == Xi)

# (5) saturation of the depth-3 hexagon locus {a=b} inside Z u1 + Z u2
#     locus = ker of (a,b) -> (a-b);  = Z.(1,1);  Z^2/Z(1,1) ~ Z is torsion free
#     => (1,1) is a primitive vector => the line is a direct summand (saturated).
from math import gcd
print("(5) gcd of coords of h_3=(1,1):", gcd(1, 1), "-> primitive:", gcd(1, 1) == 1)

# (6) unit checks at p=7 for the constants that appear in the bridge
p = 7
for name, c in [("2 (from (X+Y)^3-X^3-Y^3 = 3XY(X+Y), /3!)", 2),
                ("p^2-1 = 48 (Ihara kappa* normaliser)", p * p - 1),
                ("2*(p^2-1) = 96", 2 * (p * p - 1))]:
    print("(6) %-45s  mod %d = %d  unit: %s" % (name, p, c % p, c % p != 0))

# ---------- convert Laurent poly in X,Y to power series in xi,eta (X=1+xi) ----------
from math import comb
def to_xi(a, cut=6):
    """substitute X=1+xi, Y=1+eta ; negative powers expanded as (1+xi)^-n series."""
    out={}
    for (i,j),c in a.items():
        # (1+xi)^i  as series
        def pw(n,var):
            r={0:1}
            if n>=0:
                r={k:comb(n,k) for k in range(0,min(n,cut)+1)}
            else:
                m=-n
                r={k:((-1)**k)*comb(m+k-1,k) for k in range(0,cut+1)}
            return r
        A=pw(i,'xi'); B=pw(j,'eta')
        for k,ca in A.items():
            for l,cb in B.items():
                if k+l<=cut:
                    out[(k,l)]=out.get((k,l),0)+c*ca*cb
    return {k:v for k,v in out.items() if v!=0}
def order(a): return min(k+l for (k,l) in a) if a else 99

print("--- xi,eta coordinates ---")
print("(7) pr h(u1) =", to_xi(h_u1), " expect -xi  :", to_xi(h_u1)=={(1,0):-1})
print("    pr h(u2) =", to_xi(h_u2), " expect -eta :", to_xi(h_u2)=={(0,1):-1})
v1 = comm(comm(theta, X), X); v2 = comm(comm(theta, X), Y); v3 = comm(comm(theta, Y), Y)
print("(8) gamma_4 words: xi-order of pr h(v_i) =", [order(to_xi(hcoord(w))) for w in (v1,v2,v3)],
      " all >=2 :", all(order(to_xi(hcoord(w)))>=2 for w in (v1,v2,v3)))
print("(9) Hall  h([[[x,y],y],x]) == h([[[x,y],x],y]) :", hcoord(comm(comm(theta,Y),X))==hcoord(v2))

# (10) END-TO-END: for f = u1^a u2^b (mod gamma_4), pr(B'_sigma)=1+xi*eta*pr(h_f)
#      must have degree-3 part  -a xi^2 eta - b xi eta^2 .
print("--- end-to-end degree-3 coefficient ---")
ok=True
for a,b in [(1,0),(0,1),(1,1),(2,3),(-1,4)]:
    f=[]
    for _ in range(abs(a)): f=cat(f, u1 if a>0 else inv(u1))
    for _ in range(abs(b)): f=cat(f, u2 if b>0 else inv(u2))
    if not f: continue
    w  = comm(X, cat(inv(f), Y, f))
    Bp = to_xi(hcoord(w))                       # = pr(B'_sigma) written as 1 + ...
    deg3 = {k:v for k,v in Bp.items() if sum(k)==3}
    want = {kk:vv for kk,vv in {(2,1):-a,(1,2):-b}.items() if vv!=0}
    deg2 = {k:v for k,v in Bp.items() if sum(k)==2}
    good = (deg3==want and deg2=={} and Bp.get((0,0),0)==1)
    ok &= good
    print("(10) f=u1^%d u2^%d : deg2=%s deg3=%s expect %s : %s"%(a,b,deg2,deg3,want,good))
print("(10) END-TO-END all cases:", ok)
print("(11) => matching 1+xi*eta*pr(h_f) with psi^ab = 1 + (k*_3/2)(xi^2 eta + xi eta^2)")
print("     gives  a = b = -k*_3(sigma)/2 .  (a=b falls out, independent re-derivation of D3-BLIND(b))")

# (12) cross-check against the ALREADY-MEASURED Phi-action on L
#      (cert search/certs/bhunt_j0j2_20260806.json : m0=1 -> u0=3 ; Phi|_L = multiplication by -1)
#      SUP-4 predicts Phi acts by u^3 on the gr_3 line L_3 and by u^4 on the gr_4 line L_4.
u0 = 3
c3 = pow(u0, 3, 7); c4 = pow(u0, 4, 7); m1 = (-1) % 7
print("--- consistency with measured Phi|_L = -1 (cert bhunt_j0j2_20260806) ---")
print("(12) u0=%d : u0^3 mod 7 = %d , u0^4 mod 7 = %d , -1 mod 7 = %d" % (u0, c3, c4, m1))
print("     measured -1 equals u0^3 (gr_3 line) :", c3 == m1)
print("     measured -1 differs from u0^4 (gr_4 line) :", c4 != m1)
print("     => L = L_3 ; the Galois gr_3 line carries Tate twist 3, matching KUR Rem 4.3 (Phi(3)/Phi(4) = Z_p(3)) :", (c3 == m1) and (c4 != m1))
