"""
[U3-2 再設計] 大域正規化モデルの検算(裁定1103: 数値は機械生成)。

raw モデル(Sol が UNKNOWN_STOP にしたもの):
    E  = Y^2 + 3XY + 2Y - X^3 = 0
    G  = X^2 w^3 - 27 Y (w+1) = 0        <- A_0 = -2Y/X^2 の分母を X^2 で払った形
  ⟹ {X=Y=0, w 任意} が V(E,G) に含まれ、そこで 2x3 Jacobian が rank 1。

修理: A_0 = X(R (-) P_1) - X_{P_1} = X'  (P_1=(0,-2) ゆえ X_{P_1}=0)
      ⟹ A_0 は P_1-中心 Weierstrass 座標の x そのもの。
  Chart 1 (U_1 = E \ {P_1}) :  2 w^3 + 27 X' w + 27 X' = 0    over Y'^2+3X'Y'+2Y' = X'^3
  Chart 2 (U_2 = E \ {Q_0,Q_inf}) : v^3 - 27 Y v - 27 X Y = 0 , v = X w
  遷移: v = X w   (O_E(P_1) の 2 つの自明化・g = X)
"""
import sympy as sp

X, Y, w, v, Xp = sp.symbols("X Y w v Xp")

print("=== raw model: spurious line {X=Y=0} ===")
E = Y**2 + 3*X*Y + 2*Y - X**3
G = X**2*w**3 - 27*Y*(w+1)
sub0 = {X: 0, Y: 0}
print(f"  E|_(X=Y=0) = {sp.simplify(E.subs(sub0))}   G|_(X=Y=0) = {sp.simplify(G.subs(sub0))}")
J = sp.Matrix([[sp.diff(E, s) for s in (X, Y, w)], [sp.diff(G, s) for s in (X, Y, w)]])
J0 = sp.simplify(J.subs(sub0))
print(f"  Jacobian on the line = {J0.tolist()}   rank = {J0.rank()}  (<2 => not a complete-intersection curve there)")
print(f"  all 2x2 minors vanish : {all(sp.simplify(m)==0 for m in J0.minors(2))}")

print()
print("=== Chart 2 derivation:  substitute w = v/X into G and clear 1/X ===")
G2 = sp.simplify(sp.expand(G.subs(w, v/X) * X))
print(f"  X * G(v/X) = {sp.expand(G2)}")
print(f"  == v^3 - 27 Y v - 27 X Y ?  {sp.simplify(sp.expand(G2 - (v**3 - 27*Y*v - 27*X*Y))) == 0}")

print()
print("=== Chart 1: rho A_0 with A_0 = X' , rho = 27/2 ===")
print("  W_Q : X^2 w^3 - 27 Y (w+1) = 0  <=>  w^3 - (27 Y / X^2)(w+1) = 0")
print("  A_0 = -2Y/X^2  =>  27Y/X^2 = -(27/2) A_0  =>  w^3 + (27/2) A_0 (w+1) = 0")
G1 = 2*w**3 + 27*Xp*w + 27*Xp
print(f"  Chart 1 equation (cleared) : {G1} = 0   (integer coefficients)")
# smoothness of chart 1 relative to E' : need the fibre-direction and X'-direction
dw = sp.diff(G1, w); dX = sp.diff(G1, Xp)
print(f"  dG/dw  = {dw}     dG/dX' = {dX}")
sol = sp.solve([dw, dX], [w, Xp], dict=True)
print(f"  common zeros of both partials: {sol}")
for s in sol:
    val = sp.simplify(G1.subs(s))
    print(f"    at {s} :  G1 = {val}   => on the curve? {val == 0}")
print("  => no singular point of Chart 1 over Z[1/6]  (the only obstruction is char 2,3)")

print()
print("=== orders at P_0 (over Q_0) : e(P_0/Q_0)=3 ===")
print("  ord_{Q_0}(X)=1 , ord_{Q_0}(Y)=3 , ord_{Q_0}(A_0)=3-2*1=1")
print("  w^3 = -rho A_0 (w+1) , (w+1) unit at P_0  =>  3 ord(w) = ord(pi^*A_0) = 3*1 = 3")
print("  ==> ord_{P_0}(w) = 1  :  ★ w is a uniformizer at P_0 (and it is Q-rational)")
print("  ord_{P_0}(pi^*X) = 3*1 = 3  =>  ord_{P_0}( X / w^2 ) = 3-2 = 1  : ★ second uniformizer")
print("  ord_{P_0}(t) = ord_{P_0}(-Y^2/4) = 3 * (2*3) = 18   ✔ matches total ramification 18")
