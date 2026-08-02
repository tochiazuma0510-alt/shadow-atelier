# 便100修文 補題 DUM-HEX の検算(独立・整数演算のみ)
# 自由結合代数 Q<x,y> の中で Lie 元を計算し、theta_*, tau_* の作用を確かめる。
# 検査対象:
#   (1) v1=[[[x,y],x],x], v2=[[[x,y],x],y], v3=[[[x,y],y],y], Hall: [[[x,y],y],x] == v2
#   (2) theta_*: v1->-v3, v2->-v2, v3->-v1  ==> theta_*(h4) = -h4  (h4 = v1+4v2+v3)
#   (3) (1+tau_*+tau_*^2)(alpha v1 + beta v2 + gamma v3) == (4alpha-beta)(v1+v2+v3)
#       ==> h4 = (1,4,1) で 0
#   (4) theta_*(h3) = -h3   (h3 = u1+u2 = [[x,y],x]+[[x,y],y])
from collections import defaultdict
from itertools import product

def mul(A, B):
    C = defaultdict(int)
    for w1, c1 in A.items():
        for w2, c2 in B.items():
            C[w1 + w2] += c1 * c2
    return {w: c for w, c in C.items() if c}

def add(A, B, s=1):
    C = defaultdict(int, A)
    for w, c in B.items():
        C[w] += s * c
    return {w: c for w, c in C.items() if c}

def br(A, B):                      # [A,B] = AB - BA
    return add(mul(A, B), mul(B, A), -1)

def smul(s, A):
    return {w: s * c for w, c in A.items() if s * c}

X = {"x": 1}
Y = {"y": 1}

def gen_map(images):               # 生成元 -> 元 の対応を代数自己準同型へ延ばす
    def f(A):
        out = {}
        for w, c in A.items():
            t = {"": 1}
            for ch in w:
                t = mul(t, images[ch])
            out = add(out, smul(c, t))
        return out
    return f

theta = gen_map({"x": Y, "y": X})                       # x <-> y
tau   = gen_map({"x": Y, "y": add(smul(-1, X), smul(-1, Y))})  # x->y, y->-x-y

w   = br(X, Y)
u1  = br(w, X);  u2 = br(w, Y)
v1  = br(u1, X); v2 = br(u1, Y); v3 = br(u2, Y); v2b = br(u2, X)
h3  = add(u1, u2)
h4  = add(add(v1, smul(4, v2)), v3)

def coords(A):                     # deg-4 Lie 元を (v1,v2,v3) 座標へ(線型代数)
    basis = [v1, v2, v3]
    words = sorted({w for B in basis + [A] for w in B})
    import fractions
    M = [[fractions.Fraction(B.get(wd, 0)) for B in basis] + [fractions.Fraction(A.get(wd, 0))]
         for wd in words]
    # ガウス消去
    r = 0
    for c in range(3):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        piv = M[r][c]
        M[r] = [e / piv for e in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    for row in M[r:]:
        if row[3]: return None     # 張らない = v1,v2,v3 の一次結合でない
    sol = [0, 0, 0]
    r = 0
    for c in range(3):
        if r < len(M) and M[r][c] == 1:
            sol[c] = M[r][3]; r += 1
    return tuple(sol)

FAILS = []
def chk(name, cond):
    print(("PASS  " if cond else "FAIL  ") + name)
    if not cond: FAILS.append(name)

chk("tau^3 = id on x",       tau(tau(tau(X))) == X)
chk("theta^2 = id on x",     theta(theta(X)) == X)
chk("Hall [[[x,y],y],x]=v2", v2b == v2)
chk("dim: v1,v2,v3 独立",     coords(v1) == (1,0,0) and coords(v2) == (0,1,0) and coords(v3) == (0,0,1))
chk("theta(v1) = -v3",       coords(theta(v1)) == (0,0,-1))
chk("theta(v2) = -v2",       coords(theta(v2)) == (0,-1,0))
chk("theta(v3) = -v1",       coords(theta(v3)) == (-1,0,0))
chk("theta(h4) = -h4",       coords(theta(h4)) == (-1,-4,-1))
chk("theta(h3) = -h3",       add(theta(h3), h3) == {})
chk("(1+tau+tau^2)(h4) = 0", add(add(h4, tau(h4)), tau(tau(h4))) == {})

# (3) 一般形の真値: (1+tau+tau^2)(a v1 + b v2 + c v3) = (2a-b+2c)(v1+v2+v3)
ok = True
for a, b, c in product(range(-3, 4), repeat=3):
    F = add(add(smul(a, v1), smul(b, v2)), smul(c, v3))
    S = add(add(F, tau(F)), tau(tau(F)))
    k = 2*a - b + 2*c
    if coords(S) != (k, k, k): ok = False; print("   mismatch at", (a,b,c), coords(S))
chk("(1+tau+tau^2) の像 = (2a-b+2c)(v1+v2+v3)  [階数 1]", ok)

# (3') (3.10)-locus a=c 上では (2a-b+2c) = (4a-b) に還元される(設計ノート §2.3 の式)
ok3 = all((2*a - b + 2*a) == (4*a - b) for a, b in product(range(-3, 4), repeat=2))
chk("a=c 上で (2a-b+2c) = (4a-b)", ok3)

# (3'') hexagon deg4 解空間 = {a=c} ∩ {2a-b+2c=0} = span(1,4,1) = Q h4
sol = [(a,b,c) for a,b,c in product(range(-4,5), repeat=3)
       if a == c and 2*a - b + 2*c == 0]
chk("hexagon deg4 解 = t(1,4,1) のみ", all((a,b,c) == (t, 4*t, t) for (a,b,c) in sol
                                            for t in [a]) and (1,4,1) in sol)

# (3.10) の deg4 解空間: theta 条件 F+theta(F)=0  <=> a=c
ok2 = all((add(add(add(smul(a,v1),smul(b,v2)),smul(c,v3)),
               theta(add(add(smul(a,v1),smul(b,v2)),smul(c,v3)))) == {}) == (a == c)
          for a, b, c in product(range(-2, 3), repeat=3))
chk("(3.10) deg4 <=> a=c", ok2)

print("\nFAILS =", len(FAILS), FAILS)
