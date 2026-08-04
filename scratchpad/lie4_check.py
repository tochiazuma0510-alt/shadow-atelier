# Independent machine check of the paper-side (H-a)/(H-b') claim for h4.
# Work inside the free ASSOCIATIVE algebra Z<X,Y> (= universal envelope of the free
# Lie algebra), degree 4 component: 16 monomials.  Lie brackets expand to
# [u,v] = uv - vu.  theta and tau are Lie-algebra automorphisms determined by their
# degree-1 action, hence extend to ALGEBRA automorphisms of Z<X,Y>:
#     theta: x -> y,  y -> x
#     tau  : x -> y,  y -> -x-y     (from tau(y) = y^-1 x^-1, image in gr_1)
from itertools import product

def mul(p, q):
    r = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = m1 + m2
            r[m] = r.get(m, 0) + c1 * c2
    return {m: c for m, c in r.items() if c}

def add(*ps):
    r = {}
    for p in ps:
        for m, c in p.items():
            r[m] = r.get(m, 0) + c
    return {m: c for m, c in r.items() if c}

def smul(s, p):
    return {m: s * c for m, c in p.items() if s * c}

def br(p, q):
    return add(mul(p, q), smul(-1, mul(q, p)))

X = {"x": 1}
Y = {"y": 1}

def alg_map(p, imx, imy):
    """apply the algebra homomorphism determined by x->imx, y->imy"""
    out = {}
    for mon, c in p.items():
        acc = {"": 1}
        for ch in mon:
            acc = mul(acc, imx if ch == "x" else imy)
        out = add(out, smul(c, acc))
    return out

theta = lambda p: alg_map(p, Y, X)
tau   = lambda p: alg_map(p, Y, add(smul(-1, X), smul(-1, Y)))

a  = br(X, Y)                 # a = [x,y]
e1 = br(br(a, X), X)          # v1 = [[[x,y],x],x]
e2 = br(br(a, X), Y)          # v2 = [[[x,y],x],y]
e3 = br(br(a, Y), Y)          # v3 = [[[x,y],y],y]
e2alt = br(br(a, Y), X)       # [[[x,y],y],x]  -- Hall: must equal v2

print("Hall identity [[a,y],x] == [[a,x],y] :", e2alt == e2)
print("tau(a) == a                          :", tau(a) == a)
print("theta(a) == -a                       :", theta(a) == smul(-1, a))

h4 = add(e1, smul(4, e2), e3)
print("theta(h4) == -h4   [(H-a)]           :", theta(h4) == smul(-1, h4))
print("h4 + tau(h4) + tau^2(h4) == 0  [(H-b')]:",
      add(h4, tau(h4), tau(tau(h4))) == {})

# general form:  (1 + tau + tau^2)(alpha*v1 + beta*v2 + gamma*v3) = ? * (v1+v2+v3)
sumv = add(e1, e2, e3)
print("\ngeneral (alpha,beta,gamma) -> coefficient of (v1+v2+v3):")
ok_general = True
for al, be, ga in product(range(-3, 4), repeat=3):
    g = add(smul(al, e1), smul(be, e2), smul(ga, e3))
    s = add(g, tau(g), tau(tau(g)))
    pred = smul(2 * al - be + 2 * ga, sumv)
    if s != pred:
        ok_general = False
        print("   MISMATCH at", (al, be, ga))
print("   (1+tau+tau^2)(a*v1+b*v2+c*v3) == (2a-b+2c)(v1+v2+v3) for all 343 triples:", ok_general)

# theta-locus
print("\ntheta(g) == -g  <=>  alpha == gamma :", all(
    (theta(add(smul(al, e1), smul(be, e2), smul(ga, e3)))
     == smul(-1, add(smul(al, e1), smul(be, e2), smul(ga, e3)))) == (al == ga)
    for al, be, ga in product(range(-3, 4), repeat=3)))
print("joint solution locus {alpha=gamma} & {2a-b+2c=0}  ->  (1,4,1)*Q :",
      sorted((al, be, ga) for al, be, ga in product(range(-4, 5), repeat=3)
             if al == ga and 2 * al - be + 2 * ga == 0 and (al, be, ga) != (0, 0, 0)))
