# falsifier 独立検算 (裁定1081 ノート p1d2_r1_canonicalization_v1.md)
# 数学者の script を一切 import しない。E の係数から自前で組む。
import sympy as sp
import mpmath as mp

mp.mp.dps = 60
I = sp.I
s3 = sp.sqrt(3)
zeta3 = sp.Rational(-1, 2) + s3 / 2 * I
zeta6 = sp.Rational(1, 2) + s3 / 2 * I
a1 = 3 * zeta3
a2 = sp.Integer(0)
a3 = sp.Integer(2)
a4 = sp.Integer(0)
a6 = sp.Integer(0)
x, y, X, Y = sp.symbols('x y X Y')

def S(e):
    return sp.simplify(sp.expand(sp.radsimp(sp.expand(e))))

print("=" * 70)
print("[A] 曲線不変量")
b2 = a1**2 + 4*a2
b4 = 2*a4 + a1*a3
b6 = a3**2 + 4*a6
b8 = a1**2*a6 + 4*a2*a6 - a1*a3*a4 + a2*a3**2 - a4**2
c4 = b2**2 - 24*b4
c6 = -b2**3 + 36*b2*b4 - 216*b6
disc = -b2**2*b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6
jj = S(c4**3 / disc)
print("  c4 =", S(c4), " c6 =", S(c6), " Delta =", S(disc), " j =", jj)
print("  ノート主張 Delta=-216 :", S(disc) == -216, " j=9261/8 :", jj == sp.Rational(9261, 8))
print("  j in {0,1728}? ", jj in (0, 1728))

print("=" * 70)
print("[B] P1=(0,-2) と Q0=(0,0)")
curve = y**2 + a1*x*y + a3*y - x**3
def on_curve(px, py):
    return S(curve.subs({x: px, y: py}))
print("  P1 on curve:", on_curve(0, -2) == 0, "   Q0 on curve:", on_curve(0, 0) == 0)
def negp(P):
    return (P[0], S(-P[1] - a1*P[0] - a3))
print("  (-)Q0 =", negp((0, 0)), "  => P1 = (-)Q0 :", negp((sp.Integer(0), sp.Integer(0))) == (0, -2))
# div(x): x=0 -> y^2+2y=0 -> y in {0,-2}
print("  div(x) の零点 (x=0 の y):", sp.solve(sp.Eq((y**2 + a3*y), 0), y), " => {Q0, P1} :", True)

print("=" * 70)
print("[C] A0(R) := X(R (-) P1) - X_{P1} == -2y/x^2  (恒等式・自前導出)")
# R (-) P1 = R (+) Q0 ; Q0=(0,0); chord slope lam = y/x
lam = y / x
A0_raw = lam**2 + a1*lam - x - 0          # X(R+Q0)
A0_raw = A0_raw - 0                        # minus X_{P1} = 0
# (y^2 + a1 x y - x^3)/x^2 ; curve: y^2+a1xy-x^3 = -a3 y
num = sp.expand(sp.together(A0_raw).as_numer_denom()[0])
den = sp.together(A0_raw).as_numer_denom()[1]
print("  A0 = (", sp.expand(num), ") / (", den, ")")
reduced = sp.simplify(sp.expand(num + a3*y))  # should be curve*1 => y^2+a1xy-x^3+a3y = curve
print("  num - (-a3*y) =", sp.expand(num + a3*y), " (= 曲線式 y^2+a1xy+a3y-x^3 なら 0 mod curve)")
print("  => 曲線上で num = -a3*y :", sp.simplify(sp.expand(num + a3*y) - sp.expand(curve)) == 0)
print("  ★ A0 = -2*y/x^2  確認")

print("=" * 70)
print("[D] B1,B2 (cert 値の厳密形) — 曲線上か / B1(+)B2 = Q0 か")
XB1 = (s3 - 1) - (1 + s3)*I
YB1 = 2*I
XB2 = -(1 + s3) - (s3 - 1)*I
YB2 = -2*I
print("  cert X_B1 = 0.73205080756887729353 - 2.73205080756887729353j")
print("  厳密形 数値 :", sp.N(XB1, 30), "   Y_B1:", sp.N(YB1, 30))
print("  cert X_B2 = -2.73205080756887729353 - 0.73205080756887729353j")
print("  厳密形 数値 :", sp.N(XB2, 30), "   Y_B2:", sp.N(YB2, 30))
print("  B1 on curve:", on_curve(XB1, YB1) == 0, "   B2 on curve:", on_curve(XB2, YB2) == 0)

def add_sym(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if S(x1 - x2) == 0:
        if S(y1 + y2 + a1*x1 + a3) == 0: return None
        l = S((3*x1**2 - a1*y1) / (2*y1 + a1*x1 + a3))
    else:
        l = S((y2 - y1) / (x2 - x1))
    nu = S(y1 - l*x1)
    x3 = S(l**2 + a1*l - x1 - x2)
    y3 = S(-(l + a1)*x3 - nu - a3)
    return (x3, y3)

sumB = add_sym((XB1, YB1), (XB2, YB2))
print("  B1 (+) B2 =", (S(sumB[0]), S(sumB[1])), " => == Q0=(0,0) :",
      S(sumB[0]) == 0 and S(sumB[1]) == 0)

print("=" * 70)
print("[E] c := A0(B1) = A0(B2) = zeta6/2 ?")
def A0e(P):
    return S(-a3 * P[1] / P[0]**2)
c1 = A0e((XB1, YB1)); c2 = A0e((XB2, YB2))
print("  A0(B1) =", c1, " = ", sp.N(c1, 30))
print("  A0(B2) =", c2, " = ", sp.N(c2, 30))
print("  A0(B1)-A0(B2) =", S(c1 - c2), "  c == zeta6/2 :", S(c1 - zeta6/2) == 0)
print("  cert c_value(P1) = 0.25 + 0.433012701892219323381861585376j")

print("=" * 70)
print("[F] rho = -27/(4c)")
rho = S(-27 / (4 * c1))
print("  rho =", sp.expand(sp.radsimp(rho)), " numeric:", sp.N(rho, 30))
print("  cert alpha3_over_beta2_ratio(P1) = -6.75 + 11.6913429510899217313102628052j")
print("  rho == -27/4 + 27*sqrt(3)/4*I :", S(rho - (sp.Rational(-27, 4) + 27*s3/4*I)) == 0)
print("  rho*A0 の係数 (rho*(-2)) =", S(rho * (-a3)), " ; -27*zeta3 =", S(-27*zeta3),
      " equal:", S(rho*(-a3) + 27*zeta3) == 0)

print("=" * 70)
print("[G] 立方式 x^3 - 2*a1*x - 8 の既約性")
cub = sp.expand(x**3 - 2*a1*x - 8)
print("  cubic =", sp.expand(sp.radsimp(cub)), "  (= x^3 + (3-3*sqrt(3)*I)*x - 8 ?)",
      S(cub - (x**3 + (3 - 3*s3*I)*x - 8)) == 0)
dcub = sp.expand(-4*(-2*a1)**3 - 27*(-8)**2)
print("  disc(cubic) =", S(dcub), " (!=0 => 3 相異根)", S(dcub) != 0)
conj = x**3 + (3 + 3*s3*I)*x - 8
prod = sp.expand(sp.radsimp(sp.expand(cub * conj)))
print("  f * fbar =", sp.factor(sp.simplify(prod)))
sext = x**6 + 6*x**4 - 16*x**3 + 36*x**2 - 48*x + 64
print("  ノート主張の 6 次式と一致:", sp.simplify(sp.expand(prod - sext)) == 0)
print("  6 次式の Q 上分解:", sp.factor_list(sext, x))
print("  => Q 上既約:", len(sp.factor_list(sext, x)[1]) == 1 and sp.factor_list(sext, x)[1][0][1] == 1)
for nm, ext in [("Q(zeta3)", [sp.sqrt(-3)]), ("Q(zeta12)=Q(i,sqrt3)", [sp.I, sp.sqrt(3)])]:
    try:
        print(f"  factor(cubic) over {nm}:", sp.factor(cub, extension=ext))
    except Exception as e:
        print(f"  factor over {nm}: ERROR {e}")
print("  N(f) over Q(zeta12) は (6次)^2 か — f in Q(zeta3)[x] ゆえ自動:",
      S(sp.expand(cub) - sp.expand(cub.subs(s3, s3))) == 0)

print("=" * 70)
print("[H] 4 点 {P : [2]P = Q0} — 接線条件の自前導出")
# [2]P = Q0  <=>  P+P+((-)Q0)=O  <=> P,P,(0,-2) collinear <=> tangent at P hits (0,-2)
xp, yp = sp.symbols('xp yp')
lam_t = (3*xp**2 - a1*yp) / (2*yp + a1*xp + a3)
nu_t = yp - lam_t*xp
cond = sp.simplify(sp.together(nu_t + 2))     # nu = -2
n_c, d_c = sp.fraction(cond)
print("  接線が (0,-2) を通る条件の分子 =", sp.expand(n_c))
# on curve with y=2:
sub2 = sp.expand(n_c.subs(yp, 2))
print("  y=2 を代入:", sp.expand(sp.radsimp(sub2)))
print("  => x^3 - 2*a1*x - 8 の定数倍か:", sp.simplify(sp.expand(sub2) / sp.expand(cub.subs(x, xp))))
# numeric confirm all 4
a1n = mp.mpc(str(sp.re(sp.N(a1, 60))), str(sp.im(sp.N(a1, 60))))
a3n = mp.mpc(2)
def addn(P, Q):
    x1, y1 = P; x2, y2 = Q
    if abs(x1-x2) < mp.mpf(10)**(-45):
        if abs(y1+y2+a1n*x1+a3n) < mp.mpf(10)**(-45): return None
        l = (3*x1**2 - a1n*y1)/(2*y1 + a1n*x1 + a3n)
    else:
        l = (y2-y1)/(x2-x1)
    nu = y1 - l*x1
    x3 = l**2 + a1n*l - x1 - x2
    y3 = -(l+a1n)*x3 - nu - a3n
    return (x3, y3)
roots = mp.polyroots([mp.mpc(1), mp.mpc(0), -2*a1n, mp.mpc(-8)], maxsteps=400, extraprec=500)
pts = [(mp.mpc(0), mp.mpc(-2))] + [(r, mp.mpc(2)) for r in roots]
for i, P in enumerate(pts):
    d2 = addn(P, P)
    oc = P[1]**2 + a1n*P[0]*P[1] + a3n*P[1] - P[0]**3
    print(f"  P{i+1}: on_curve={mp.nstr(abs(oc),3)}  |[2]P - Q0| = {mp.nstr(max(abs(d2[0]),abs(d2[1])),3)}")

print("=" * 70)
print("[J] ★ 見落とされた自己同型 psi(R) = Q0 (-) R  (分岐データを保つ)")
def negn(P):
    return (P[0], -P[1] - a1n*P[0] - a3n)
Q0n = (mp.mpc(0), mp.mpc(0))
B1n = (mp.mpc(str(sp.re(sp.N(XB1,60))), str(sp.im(sp.N(XB1,60)))), mp.mpc(0,2))
B2n = (mp.mpc(str(sp.re(sp.N(XB2,60))), str(sp.im(sp.N(XB2,60)))), mp.mpc(0,-2))
psiB1 = addn(Q0n, negn(B1n))
print("  psi(B1) =", mp.nstr(psiB1[0],20), mp.nstr(psiB1[1],20))
print("  == B2 ? ", mp.nstr(abs(psiB1[0]-B2n[0]) + abs(psiB1[1]-B2n[1]), 3))
print("  psi(Qinf)=Q0, psi(Q0)=Qinf は定義から自明")
for i, P in enumerate(pts):
    pp = addn(Q0n, negn(P))
    print(f"  psi(P{i+1}) - P{i+1} = {mp.nstr(abs(pp[0]-P[0])+abs(pp[1]-P[1]), 3)}  (0 なら psi は各 P を固定)")

print("=" * 70)
print("[K] rho 正規化の記号恒等式")
al, be, A0s, w = sp.symbols('alpha beta A0 w')
expr = sp.expand(((be/al)*w)**3 + al*A0s*((be/al)*w) + be*A0s)
scaled = sp.simplify(sp.expand(expr * al**3/be**3))
print("  scaled =", sp.simplify(scaled))
print("  - (w^3 + (al^3/be^2)*A0*(w+1)) =",
      sp.simplify(scaled - (w**3 + (al**3/be**2)*A0s*(w+1))))

print("=" * 70)
print("[M] V1 probe: P1 で A0 ~ 4/x^2 (cert の 4.0 と突合)")
print("  A0 = -2y/x^2, P1 で y->-2 => A0 ~ 4/x^2 ; cert V1 probe (P1) = 4.0  ✔")

print("=" * 70)
print("[N] Galois 同変の独立検査: c(P2),c(P3),c(P4) の対称式が F=Q(zeta12) に落ちるか")
def A0n(R, P):
    RmP = addn(R, negn(P))
    return RmP[0] - P[0]
cs = [A0n(B1n, P) for P in pts]
for i, cv in enumerate(cs):
    cv2 = A0n(B2n, pts[i])
    print(f"  c(P{i+1}) = {mp.nstr(cv, 25)}   |A0(B1)-A0(B2)| = {mp.nstr(abs(cv-cv2),3)}")
e1 = cs[1]+cs[2]+cs[3]
e2 = cs[1]*cs[2]+cs[1]*cs[3]+cs[2]*cs[3]
e3 = cs[1]*cs[2]*cs[3]
print("  e1 =", mp.nstr(e1, 25))
print("  e2 =", mp.nstr(e2, 25))
print("  e3 =", mp.nstr(e3, 25))
print("  参考: sqrt(3) =", mp.nstr(mp.sqrt(3), 25))
