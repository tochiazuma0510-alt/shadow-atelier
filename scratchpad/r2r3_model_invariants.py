"""
[R-2/R-3/UNRAM spec] 宣言済みモデル W(P_1) の *既公開* 不変量の再現(裁定1103: 数値は機械生成)。

  E : y^2 + 3*z3*x*y + 2*y = x^3       (z3 = primitive cube root of 1)
  W : x^2 w^3 - 27*z3*y*(w+1) = 0
  t = -y^2/4

⚠ prereg 検問: 本 script は d_9 / r / a_class / S(悪い素点集合)を *計算しない*。
   出すのは E の標準不変量(Delta, c4, j)と、次数・種数の帳簿のみ。
   これらは既に fals_p1d2_r1_audit_v1.md §5 と宣言 v4 に公開済みの値である。
"""
import sympy as sp

z3 = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2          # primitive cube root of unity
a1, a2, a3, a4, a6 = 3 * z3, 0, 2, 0, 0

b2 = sp.expand(a1**2 + 4 * a2)
b4 = sp.expand(2 * a4 + a1 * a3)
b6 = sp.expand(a3**2 + 4 * a6)
b8 = sp.expand(a1**2 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3**2 - a4**2)
Delta = sp.simplify(sp.expand(-b2**2 * b8 - 8 * b4**3 - 27 * b6**2 + 9 * b2 * b4 * b6))
c4 = sp.simplify(sp.expand(b2**2 - 24 * b4))
j = sp.simplify(c4**3 / Delta)

print("=== E : y^2 + 3*zeta3*x*y + 2*y = x^3 ===")
print(f"  b2 = {sp.simplify(b2)}   b4 = {sp.simplify(b4)}   b6 = {b6}   b8 = {b8}")
print(f"  c4 = {c4}")
print(f"  Delta = {Delta}          rational: {Delta.is_rational}")
print(f"  j     = {j} = {sp.nsimplify(j)}   rational: {sp.simplify(j).is_rational}")
print(f"  Delta factored = {sp.factorint(int(sp.simplify(Delta)))}")
num, den = sp.fraction(sp.nsimplify(j))
print(f"  j = {num}/{den}   num factored = {sp.factorint(int(num))}   den factored = {sp.factorint(int(den))}")
print(f"  v_2(j) = {-sp.Integer(den).as_coeff_exponent(2)[1] if False else 'see den'}   "
      f"=> j has 2 in the DENOMINATOR: {int(den) % 2 == 0}  (potentially multiplicative at 2)")
print(f"  3 | Delta and 3 does NOT divide den(j): {int(sp.simplify(Delta)) % 3 == 0 and int(den) % 3 != 0}"
      "  (potentially good reduction at 3)")

print()
print("=== degree / genus bookkeeping (all from the declared passport) ===")
D = 18
prof = {"t=0": [18], "t=1": [2]*8 + [1]*2, "t=inf": [18]}
tot = 0
for k, v in prof.items():
    assert sum(v) == D
    tot += sum(e - 1 for e in v)
    print(f"  {k:6s} profile {v}  sum(e-1) = {sum(e-1 for e in v)}")
g = (tot - 2 * D + 2) // 2
print(f"  total sum(e-1) = {tot}   2g-2 = {-2*D + tot}   g = {g}")
print(f"  deg L(18 P_inf) = 18 - g + 1 = {18 - g + 1}   (Riemann-Roch, 18 > 2g-2 = {2*g-2})")
print(f"  div(lambda_9) = 18(P_0 - P_inf)  => 18(P_0-P_inf) ~ 0 : automatic (principal)")
print(f"  ord(P_0 - P_inf) = 9 by Lemma ORD9 (p1d2_r1_canonicalization_v2 SS6.2); 9 | 18 : {18 % 9 == 0}")

print()
print("=== tower layers (declared) ===")
print("  W --3--> E --3--> P^1_s --2--> P^1_t     3*3*2 = 18")
print("  s = y/(2i) ,  t = s^2 = -y^2/4 ;  coefficients of E, W, t all in Q(zeta_3)")


# ---------------------------------------------------------------------------
# [U3-1 / Z 係数化] 宣言モデルは Q 上に降りるか — 置換 x = zeta_3^2 * X の検算
# ---------------------------------------------------------------------------
def descent_check():
    X, Y, w = sp.symbols('X Y w')
    z = sp.symbols('z')                      # z stands for zeta_3, with z^3 = 1
    def red(e):                              # reduce modulo z^3 - 1
        return sp.simplify(sp.rem(sp.expand(e), z**3 - 1, z))
    # E : y^2 + 3 z x y + 2 y - x^3 = 0   with   x = z^2 X , y = Y
    E_sub = red((Y**2 + 3*z*(z**2*X)*Y + 2*Y - (z**2*X)**3))
    # W : x^2 w^3 - 27 z y (w+1) = 0      with the same substitution
    W_sub = red(((z**2*X)**2 * w**3 - 27*z*Y*(w+1)))
    print("\n=== [U3-1] descent to Q via x = zeta_3^2 * X  (z^3 = 1) ===")
    print(f"  E  ->  {sp.factor(E_sub)}")
    print(f"     coefficients free of zeta_3 : {E_sub.free_symbols.isdisjoint({z})}")
    W_over_z = sp.simplify(sp.cancel(W_sub / z))
    print(f"  W  ->  {sp.expand(W_sub)}")
    print(f"     = zeta_3 * ( {sp.expand(W_over_z)} )")
    print(f"     after dividing by the unit zeta_3, coefficients free of zeta_3 : "
          f"{sp.expand(W_over_z).free_symbols.isdisjoint({z})}")
    print("  t  ->  -Y^2/4   (unchanged, already rational)")
    # marked points
    print("  marked points:  Q_0 = (0,0) -> (0,0) ;  Q_inf = O -> O ;  P_1 = (0,-2) -> (0,-2)")
    print("  B_1,B_2 : Y = +-2i  -> rational as the DIVISOR (Y^2 + 4 = 0)")
    # discriminant of the Q-model
    b2, b4, b6, b8 = 9, 6, 4, 0
    D = -b2**2*b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6
    c4 = b2**2 - 24*b4
    print(f"\n  Q-model E_Q : Y^2 + 3XY + 2Y = X^3   Delta = {D} = {sp.factorint(D)}   "
          f"c4 = {c4}   j = {sp.Rational(c4**3, D)}")

descent_check()
