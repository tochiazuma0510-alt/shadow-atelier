# u_meas_cal_a5.py -- CAL-M3: end-to-end calibration of the quotient route on the A5 window,
# plus the window-B case-(a) determination.  Exact symbolic arithmetic (sympy, no floats in decisions).
#
# A5 window : M = e = 5, Lambda = A5/A4 (5 points), lambda-cover genus 2, passport (5,5,5).
#             quotient C = W/phi -> P^1_t : genus 0, degree 5, passport ((3,1,1),(3,1,1),(5)).
#             Known published value (W3-8): u^{-1} = -2, fixed field Q(zeta_5, 2^{1/5}).
# Window B  : quotient genus 2, degree 9, passport (3^3, 3^3, (9)).  Case (a) = Pbar Weierstrass.

import sympy as sp

x, Z, T, t = sp.symbols('x Z T t')
s3 = sp.sqrt(-3)

print("=== CAL-M3 : A5 window, quotient route ===")

# branch points of P^1_lambda -> P^1_t : roots of t^2 - 3t + 9
taus = sp.solve(sp.Eq(t**2 - 3*t + 9, 0), t)
print("tau_1, tau_2 =", taus, "  sum =", sp.simplify(taus[0]+taus[1]), " prod =", sp.simplify(taus[0]*taus[1]))

# Shanks base change identity: lambda, mu(lambda), mu^2(lambda) are roots of
#   L^3 - t L^2 + (t-3) L + 1,  with t = e1(lambda)
lam = sp.symbols('lam')
t_of_lam = sp.together(lam + 1/(1-lam) + (lam-1)/lam)
poly_check = sp.simplify(sp.expand(lam**3 - t_of_lam*lam**2 + (t_of_lam-3)*lam + 1))
print("Shanks cubic satisfied by lambda :", poly_check == 0)
# and the S3 swap:  t(1-lambda) = 3 - t(lambda)
print("t(1-lambda) = 3 - t(lambda)     :",
      sp.simplify(t_of_lam.subs(lam, 1-lam) - (3 - t_of_lam)) == 0)

# --- construct the genus-0 quotient dessin of the A5 window ---
# t5' = 5c (Z^2+3)^2  (two triple points at Z = +- sqrt(-3), conjugate over Q(sqrt(-3)))
c = sp.Rational(1,16)
t5 = c*(Z**5 + 10*Z**3 + 45*Z) + sp.Rational(3,2)
print("\n t5(Z) =", t5)
print(" t5'(Z) = 5c (Z^2+3)^2 :", sp.simplify(sp.diff(t5,Z) - 5*c*(Z**2+3)**2) == 0)
v1 = sp.simplify(t5.subs(Z, s3)); v2 = sp.simplify(t5.subs(Z, -s3))
print(" t5(+sqrt(-3)) =", sp.simplify(sp.expand(v1)), "  is a tau ? ", sp.simplify(v1**2-3*v1+9) == 0)
print(" t5(-sqrt(-3)) =", sp.simplify(sp.expand(v2)), "  is a tau ? ", sp.simplify(v2**2-3*v2+9) == 0)
for name, v, r in (("tau_a", v1, s3), ("tau_b", v2, -s3)):
    q = sp.Poly(sp.expand(16*(t5 - v)), Z)
    fac = sp.factor(q.as_expr())
    print("  16*(t5 - %s) factors as: %s" % (name, fac))

# passport check: multiplicity of the root at Z=+-sqrt(-3)
for r in (s3, -s3):
    q = sp.Poly(sp.expand(16*(t5 - t5.subs(Z, r))), Z)
    m = 0
    rem = q.as_expr()
    while sp.simplify(sp.expand(sp.div(rem, (Z-r), Z)[1])) == 0:
        rem = sp.div(rem, (Z-r), Z)[0]; m += 1
    print("  multiplicity of Z=%s : %d  (want 3)" % (r, m))

# --- u_0 via Prop U-LOC : t5 = c * s^{-5} (1+O(s)), s = 1/Z ; u_0 = -1/c
u0 = -1/c
print("\n leading coeff c =", c, "   u_0 = -c^{-1} =", u0, "   u_0^{-1} =", sp.nsimplify(1/u0))
print(" published A5 value  u^{-1} = -2")
ratio = sp.nsimplify((1/u0) / sp.Integer(-2))
print(" (u_0^{-1}) / (-2) =", ratio, "  is a 5th power in Q ? ", sp.nsimplify(ratio) == sp.Rational(1,32), " (=2^-5)")

# exact match after the rational rescaling Z -> Z/2  (s -> 2s, u_0^{-1} -> u_0^{-1} * 2^5)
Zn = sp.symbols('Zn')
t5n = sp.expand(t5.subs(Z, 2*Zn))
print("\n rescaled t5(2*Zn) =", t5n, "  leading coeff =", sp.Poly(t5n, Zn).all_coeffs()[0])
c_new = sp.Poly(t5n, Zn).all_coeffs()[0]
print(" u_0(new) = -1/c_new =", -1/c_new, "   u_0^{-1}(new) =", -c_new)
print(" ===> EXACT MATCH with published u^{-1} = -2 :", sp.simplify(-c_new + 2) == 0)

print("\n=== window B : case (a)  (Pbar a Weierstrass point) ===")
G = x**3 + 9*x - 6
Phi = sp.expand(G**3 - 1728)
print(" Phi = G^3 - 1728, G =", G)
target = sp.expand((x**2+3)**2 * (x**3+9*x-18) * (x**2+12))
print(" Phi == (x^2+3)^2 (x^3+9x-18)(x^2+12) :", sp.expand(Phi - target) == 0)
f5 = sp.expand((x**3+9*x-18)*(x**2+12))
print(" f5 =", f5)
print(" f5 squarefree ? ", sp.gcd(f5, sp.diff(f5,x)) == 1, "   deg =", sp.degree(f5,x), " => genus 2")
print(" B(x) = (x^2+3)/16 ;  t = 3/2 + B(x) y ;  N_tau = -27/4 - B^2 f5 = -(1/256) Phi :",
      sp.expand(sp.Rational(-27,4) - ((x**2+3)/16)**2 * f5 + sp.Rational(1,256)*Phi) == 0)
print(" leading coeff of t at Pbar: 1/16  =>  u_0^{-1} = -1/16 == [2^-4]")
print("\n *** BUT: Phi = Psi o G with Psi(u)=u^3-1728  =>  Phi is DECOMPOSABLE")
print(" *** => Mon(Phi) is imprimitive (preserves the fibres of G, blocks of size 3)")
print(" *** => Mon(C/P^1_t) <= Mon(Phi) is imprimitive, but PSL(2,8) on 9 points is PRIMITIVE")
print(" *** => case (a) is NOT the window-B dessin.  Pbar is NOT a Weierstrass point.")

# rationality of case (a): 4p^3 = 81 q^2 has only p=9z^2, q=+-6z^3
p_, q_, z_ = sp.symbols('p q z')
sol = sp.solve([sp.Eq(4*p_**3, 81*q_**2)], [p_], dict=True)
print("\n case-(a) rationality condition 4p^3 = 81 q^2 ; parametrisation p=9z^2, q=-6z^3 :",
      sp.simplify(4*(9*z_**2)**3 - 81*(-6*z_**3)**2) == 0)
print("=== done ===")
