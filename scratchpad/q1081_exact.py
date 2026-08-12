# 裁定1081 ★ 正準点 P1=(0,-2)=(-)Q0 での厳密モデル
# (1) A0(R) := X(R (-) P1) - X_{P1} == -a3*y/x^2  を恒等式として確認
# (2) c := A0(B1) = A0(B2) = zeta6/2 を厳密に確認
# (3) rho := -27/(4c) を厳密に、cert の alpha3_over_beta2_ratio と突合
import sympy as sp

I = sp.I
zeta3 = sp.Rational(-1, 2) + sp.sqrt(3) / 2 * I
zeta6 = sp.Rational(1, 2) + sp.sqrt(3) / 2 * I
a1, a3 = 3 * zeta3, sp.Integer(2)
x, y = sp.symbols('x y')

# --- (1) 恒等式 ---
P1 = (sp.Integer(0), sp.Integer(-2))
# check P1 on curve and (-)P1 = Q0, [2]P1 = Q0
def negp(P):
    X, Y = P
    return (X, -Y - a1 * X - a3)
print("P1 on curve:", sp.simplify(P1[1]**2 + a1*P1[0]*P1[1] + a3*P1[1] - P1[0]**3) == 0)
print("(-)P1 =", negp(P1), " (should be Q0=(0,0))")

# R (-) P1 = R (+) Q0 ; chord through R=(x,y) and Q0=(0,0): lam = y/x
lam = y / x
Xsum = sp.together(lam**2 + a1 * lam - x - 0)
A0_formula = sp.simplify(Xsum - P1[0])
# reduce modulo the curve relation y^2 = x^3 - a1*x*y - a3*y
num, den = sp.fraction(sp.together(A0_formula))
num = sp.expand(num)
# substitute y^2 -> x^3 - a1*x*y - a3*y repeatedly
target = sp.expand(-a3 * y / x**2)
diff = sp.together(A0_formula - target)
n2, d2 = sp.fraction(diff)
n2 = sp.expand(n2)
# reduce n2 modulo curve
curve = sp.expand(y**2 + a1*x*y + a3*y - x**3)
q, r = sp.div(sp.Poly(n2, y), sp.Poly(curve, y))
print("A0 - (-a3*y/x^2) reduces to (mod curve):", sp.simplify(r.as_expr()))
print("  => identity A0 = -2*y/x^2 :", sp.simplify(r.as_expr()) == 0)

# --- (2) c = A0(B1) = A0(B2) ---
XB1 = -1 + sp.sqrt(3) + I*(-sp.sqrt(3) - 1); YB1 = 2*I
XB2 = -sp.sqrt(3) - 1 + I*(1 - sp.sqrt(3)); YB2 = -2*I
def A0e(X, Y):
    return sp.simplify(sp.expand(-a3 * Y / X**2))
c1 = sp.nsimplify(sp.radsimp(sp.simplify(A0e(XB1, YB1))))
c2 = sp.nsimplify(sp.radsimp(sp.simplify(A0e(XB2, YB2))))
print("A0(B1) =", sp.simplify(c1), " = ", sp.nsimplify(sp.N(c1, 30)))
print("A0(B2) =", sp.simplify(c2))
print("A0(B1)-A0(B2) =", sp.simplify(c1 - c2))
print("c == zeta6/2 ? ", sp.simplify(c1 - zeta6/2) == 0)

# --- (3) rho ---
rho = sp.simplify(-27 / (4 * c1))
print("rho =", sp.expand(sp.radsimp(rho)), " numeric:", sp.N(rho, 25))
print("cert alpha3_over_beta2_ratio (P1) = -6.75 + 11.6913429510899217313102628052j")
print("rho == -27/(2*zeta6) == -27*zeta3^{-1}/2 ?",
      sp.simplify(rho + 27/(2*zeta6)) == 0)
# final model coefficient
coef = sp.simplify(rho * (-a3))   # rho*A0 = coef * y/x^2
print("rho*A0 = (", sp.expand(sp.radsimp(coef)), ") * y/x^2")
print("  compare -27*zeta3 =", sp.expand(-27*zeta3))
print("  equal?", sp.simplify(coef + 27*zeta3) == 0)
