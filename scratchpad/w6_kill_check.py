# w6_kill_check.py -- 紙の検算(整数演算のみ・群計算なし・証明書非読・Im R 非接触)
# 対象: docs/notes/w6_kill_theorems_v1.md の紙計算
#   Part A: 自由群 F_2 での語恒等式 (COBDY)   -- 自由簡約による厳密判定
#   Part B: K^(20) の座標計算 (ROOF-KILL の実物)  -- (Z/10)^3 の整数演算
#   Part C: theta-defect の公式と K^(20) での値
FAILS = 0
def chk(name, cond):
    global FAILS
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: FAILS += 1

# ---------- Part A: 自由群 F_2 = <x,y> の語演算 ----------
# 文字: ('x',+1) 等。z = (xy)^{-1}
def red(w):
    out = []
    for c in w:
        if out and out[-1][0] == c[0] and out[-1][1] == -c[1]:
            out.pop()
        else:
            out.append(c)
    return tuple(out)
def inv(w):  return red(tuple((c[0], -c[1]) for c in reversed(w)))
def mul(*ws):
    r = ()
    for w in ws: r = red(r + w)
    return r
X = (('x',1),); Y = (('y',1),)
def pw(w,n):
    return mul(*([w]*n)) if n>=0 else mul(*([inv(w)]*(-n)))
Z = inv(mul(X,Y))                       # z = (xy)^{-1}

# theta: x->y, y->x ;  tau: x->y, y->z, z->x
def apply(sub, w):
    return mul(*[ (sub[c[0]] if c[1]==1 else inv(sub[c[0]])) for c in w ]) if w else ()
TH = {'x':Y, 'y':X}
TA = {'x':Y, 'y':Z}
def theta(w): return apply(TH, w)
def tau(w):   return apply(TA, w)

chk("A0  theta^2 = id (x,y)",  theta(theta(X))==X and theta(theta(Y))==Y)
chk("A1  tau^3   = id (x,y)",  tau(tau(tau(X)))==X and tau(tau(tau(Y)))==Y)
chk("A2  tau(z)  = x",         tau(Z)==X)

w  = mul(pw(X,2), pw(Y,-2))     # w  = x^2 y^-2   (既出・札 1-D)
wp = mul(pw(Y,-2), pw(X,2))     # w' = y^-2 x^2   (本稿)

N_theta = lambda a: mul(a, theta(a))
N_tau   = lambda a: mul(tau(tau(a)), tau(a), a)

chk("A3  N_theta(w)  = 1  (既出)",          N_theta(w)  == ())
chk("A4  N_tau(w)   != 1  (既出の非自明語)", N_tau(w)    != ())
chk("A5  N_theta(w') = 1  ★本稿",           N_theta(wp) == ())
chk("A6  N_tau(w')   = 1  ★本稿",           N_tau(wp)   == ())
# 一般恒等式 (補題 COBDY): N_theta(u^-1 theta(u)) = 1, N_tau(tau(u) u^-1) = 1
import itertools, random
random.seed(0)
ok_th = ok_ta = True
for _ in range(200):
    n = random.randint(1,6)
    u = ()
    for _ in range(n):
        c = random.choice(['x','y']); e = random.choice([1,-1])
        u = mul(u, ((c,e),))
    if N_theta(mul(inv(u), theta(u))) != (): ok_th = False
    if N_tau(mul(tau(u), inv(u)))     != (): ok_ta = False
chk("A7  N_theta(u^-1 theta(u)) = 1 for 200 random u", ok_th)
chk("A8  N_tau(tau(u) u^-1)     = 1 for 200 random u", ok_ta)
chk("A9  w  = u^-1 theta(u), u = x^-2",  mul(pw(X,2), theta(pw(X,-2))) == w)
chk("A10 w' = tau(u) u^-1,   u = x^-2",  mul(tau(pw(X,-2)), pw(X,2))   == wp)
chk("A11 w' = u^-1 theta(u), u = y^2",   mul(pw(Y,-2), theta(pw(Y,2))) == wp)
chk("A12 w' = y^-2 w y^2 (共役)",        mul(pw(Y,-2), w, pw(Y,2))     == wp)

# ---------- Part B: K^(20) の座標計算 ----------
# A_20 = <r^2>^3 ~ (Z/10)^3, 基底 (X^2, Y^2, (XY)^{-2}), 座標 n=(n1,n2,n3)
# theta(n) = (n2,n1,-n3) ; tau(n) = (n3,n1,n2)   [正典 (4.7)(4.8)]
M = 10
th_ = lambda n: ((n[1])%M, (n[0])%M, (-n[2])%M)
ta_ = lambda n: ((n[2])%M, (n[0])%M, (n[1])%M)
add = lambda *v: tuple(sum(t)%M for t in zip(*v))
# [G20,G20] = { n : n1=n2=n3 mod 2 }  (= I_Q A + <(-1,1,-1)>)
inD = lambda n: (n[0]%2)==(n[1]%2)==(n[2]%2)
DER = [n for n in itertools.product(range(M),repeat=3) if inD(n)]
chk("B1  |[G20,G20]| = 250", len(DER)==250)
chk("B2  |G20^ab| = 4000/250 = 16", 4000//len(DER)==16)
# I_Q A = 全偶 (125) と [X,Y]=(-1,1,-1) の生成で DER と一致
gen = set()
frontier = [(0,0,0)]
seen = {(0,0,0)}
basis = [(2,0,0),(0,2,0),(0,0,2),(M-1,1,M-1)]
while frontier:
    a = frontier.pop()
    for b in basis:
        c = add(a,b)
        if c not in seen: seen.add(c); frontier.append(c)
chk("B3  <2Z^3,(-1,1,-1)> = {同一パリティ}", seen==set(DER))
# V = ker(G20 -> G5) = {5b : b in F_2^3}
V = [tuple(5*bi for bi in b) for b in itertools.product(range(2),repeat=3)]
chk("B4  |V| = 8, V 初等アーベル 2 群", len(set(V))==8 and all(add(v,v)==(0,0,0) for v in V))
W = [v for v in V if inD(v)]
chk("B5  W = V cap [G,G] = <(5,5,5)>, |W| = 2", set(W)=={(0,0,0),(5,5,5)})
# f_1 = (1,-1,0) mod 5 ; w, w' の A_20 座標は X^2 Y^-2 = (1,-1,0) in (Z/10)^3
wbar = (1, M-1, 0)
chk("B6  wbar = (1,9,0) は f_1 を持ち上げる", tuple(c%5 for c in wbar)==(1,4,0))
chk("B7  ★ wbar not in [G20,G20]  (=> w,w' は K^(20) で使えない)", not inD(wbar))
# 屋根 witness (f_1, 1) : mod5 = (1,-1,0), mod2 = (0,0,0)  -> CRT
roof = (6,4,0)
chk("B8  (f1,1) = (6,4,0):  mod5 = f1", tuple(c%5 for c in roof)==(1,4,0))
chk("B9  (f1,1) = (6,4,0):  mod2 = 0 (G_4 成分自明)", tuple(c%2 for c in roof)==(0,0,0))
chk("B10 ★ (f1,1) in [G20,G20]  => delta_roof = 0", inD(roof))
chk("B11 ★ N_theta((6,4,0)) = 0", add(roof, th_(roof))==(0,0,0))
chk("B12 ★ N_tau((6,4,0))   = 0", add(ta_(ta_(roof)), ta_(roof), roof)==(0,0,0))
# 一意性の確認: [G,G] の中の f_1 の持上げはちょうど |W| = 2 個
lifts = [n for n in DER if tuple(c%5 for c in n)==(1,4,0)]
chk("B13 [G,G] 内の f_1 の持上げは 2 個 (= |W| torsor)", len(lifts)==2 and roof in lifts)
chk("B14 もう 1 個は (6,4,0)+(5,5,5) = (1,9,5)", set(lifts)=={(6,4,0),(1,9,5)})
# 両方が両ノルムを満たす (W 上 N_theta = 0, N_tau = id かつ beta_tau = 0 ゆえ)
o = lifts[1] if lifts[0]==roof else lifts[0]
chk("B15 ★ 第 2 の持上げも N_theta = 0  (N_theta|W = 0 ゆえ beta_theta は torsor 不変)",
    add(o, th_(o))==(0,0,0))
chk("B16 ★ 第 2 の持上げは N_tau = (5,5,5) != 0  (N_tau|W = id ゆえ beta_tau は W ぶん動く)",
    add(ta_(ta_(o)), ta_(o), o)==(5,5,5))
chk("B17 ★ よって [ (beta_theta,beta_tau) ] = 0 in coker psi_W は 2 個中 1 個の持上げが担う",
    sum(1 for L in lifts if add(L,th_(L))==(0,0,0)
                        and add(ta_(ta_(L)),ta_(L),L)==(0,0,0))==1)

# ---------- Part C: theta-defect の公式 ----------
# theta|_V (b) = (b2,b1,b3)  (p=2 で (4.7) の符号が消える)
# v_0 in V with wbar + v_0 in [G,G] ; theta-def = N_theta(v_0)
v0s = [v for v in V if inD(add(wbar,v))]
chk("C1  v_0 の候補はちょうど |W| = 2 個", len(v0s)==2)
defs = set(add(v, th_(v)) for v in v0s)
chk("C2  ★ theta-def は v_0 の取り方によらない", len(defs)==1)
chk("C3  ★ theta-def(K^(20)) = 0  (=> 障害類 0 ・prereg P-K20-4 と一致)", defs=={(0,0,0)})
chk("C4  theta-def in W", all(d in set(W) for d in defs))
# u = psi_4(w) の V 座標 = (1,1,0) ; [wbar] = [u] in V/W  (delta_roof = 0 の別経路)
u_coord = (5,5,0)      # b=(1,1,0) を V の座標 5b で
chk("C5  ★ [wbar] = [u] in V/W  (=> delta_roof = 0)", inD(add(wbar, u_coord)))
chk("C6  N_theta(u) = 0", add(u_coord, th_(u_coord))==(0,0,0))
# |V|=2 の一般論の健全性: dim_F2 W = 1 では N_theta = 0, N_tau = id
chk("C7  dim W = 1: N_theta|W = 0", all(add(w_,th_(w_))==(0,0,0) for w_ in W))
chk("C8  dim W = 1: N_tau|W  = id", all(add(ta_(ta_(w_)),ta_(w_),w_)==w_ for w_ in W))

print("\nFAILS =", FAILS)
print("RESULT:", "ALL PASS" if FAILS==0 else "FAILURES PRESENT")
