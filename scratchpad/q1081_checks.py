# 裁定1081 数学者側の検算(紙の主張の機械確認)
# (A) V4 ⟺ [D2-1] のテスト: A0(R)=A0(R') ⟺ R (+) R' = [2]P  (任意の P で)
# (B) 4点の Galois 構造: x^3 - 6*zeta3*x - 8 の Q(zeta12) 上の既約性
# (C) rho-正規化: w^3 + rho*A0*(w+1)=0 が z^3+alpha*A0*z+beta*A0 と同型か(記号)
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
I = sp.I
zeta3 = sp.Rational(-1, 2) + sp.sqrt(3) / 2 * I
a1s, a3s = 3 * zeta3, sp.Integer(2)


def to_mp(e):
    n = sp.N(e, 50)
    return mp.mpc(str(sp.re(n)), str(sp.im(n)))


a1 = to_mp(a1s)
a3 = to_mp(a3s)


def neg(P):
    if P is None:
        return None
    x, y = P
    return (x, -y - a1 * x - a3)


def add(P1, P2):
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    x1, y1 = P1
    x2, y2 = P2
    if abs(x1 - x2) < mp.mpf(10) ** (-35):
        if abs(y1 + y2 + a1 * x1 + a3) < mp.mpf(10) ** (-35):
            return None
        lam = (3 * x1 ** 2 - a1 * y1) / (2 * y1 + a1 * x1 + a3)
    else:
        lam = (y2 - y1) / (x2 - x1)
    nu = y1 - lam * x1
    x3 = lam ** 2 + a1 * lam - x1 - x2
    y3 = -(lam + a1) * x3 - nu - a3
    return (x3, y3)


def oncurve_y(x, ybranch=0):
    # solve y^2 + (a1 x + a3) y - x^3 = 0
    b = a1 * x + a3
    disc = b ** 2 + 4 * x ** 3
    r = mp.sqrt(disc)
    return (-b + (r if ybranch == 0 else -r)) / 2


def A0(R, P):
    return add(R, neg(P))[0] - P[0]


print("=== (A) V4 <=> [D2-1] control ===")
mp.mp.dps = 50
for trial, xv in enumerate([mp.mpc(1.3, 0.7), mp.mpc(-0.4, 2.1), mp.mpc(3.0, -1.1)]):
    P = (xv, oncurve_y(xv))
    twoP = add(P, P)
    # R random on curve; R' := [2]P (-) R  => A0(R) should equal A0(R')
    for xr in [mp.mpc(0.9, -1.7), mp.mpc(-2.2, 0.3)]:
        R = (xr, oncurve_y(xr))
        Rp = add(twoP, neg(R))
        d_match = abs(A0(R, P) - A0(Rp, P))
        # a deliberately WRONG partner: R'' with R (+) R'' != [2]P
        Rpp = add(Rp, (mp.mpc(0), mp.mpc(0)))  # shift by Q0=(0,0)
        d_mismatch = abs(A0(R, P) - A0(Rpp, P))
        print(f"  P#{trial} R: |A0(R)-A0([2]P-R)| = {mp.nstr(d_match,5)}   "
              f"|A0(R)-A0(shifted)| = {mp.nstr(d_mismatch,5)}")

print()
print("=== (B) Galois structure of the 4 points ===")
x = sp.symbols('x')
cub = sp.expand(x ** 3 - 2 * a1s * x - 8)
print("  cubic =", sp.simplify(cub))
for ext_name, ext in [("Q(zeta3)=Q(sqrt(-3))", [sp.sqrt(-3)]),
                      ("Q(zeta12)=Q(i,sqrt3)", [sp.I, sp.sqrt(3)]),
                      ("Q(zeta36)", [sp.exp(2 * sp.pi * sp.I / 36)])]:
    try:
        f = sp.factor(cub, extension=ext)
        print(f"  over {ext_name}: {f}")
    except Exception as e:
        print(f"  over {ext_name}: ERROR {e}")

# rational root test over Q(zeta12) by brute: does cubic have a root in Q(i,sqrt3)?
print("  numeric roots:", [mp.nstr(r, 20) for r in
                           mp.polyroots([mp.mpc(1), mp.mpc(0), -2 * a1, mp.mpc(-8)],
                                        maxsteps=200, extraprec=300)])

print()
print("=== (C) rho normalization identity (symbolic) ===")
al, be, A0s, w, z = sp.symbols('alpha beta A0 w z')
lam = be / al
expr = sp.expand((lam * w) ** 3 + al * A0s * (lam * w) + be * A0s)
expr2 = sp.simplify(sp.expand(expr * al ** 3 / be ** 3))
print("  (beta/alpha*w)^3 + alpha*A0*(beta/alpha*w) + beta*A0, scaled by alpha^3/beta^3:")
print("   =", sp.factor(expr2))
rho = sp.symbols('rho')
print("  target w^3 + rho*A0*(w+1) with rho = alpha^3/beta^2 :",
      sp.simplify(expr2 - (w ** 3 + (al ** 3 / be ** 2) * A0s * (w + 1))))
