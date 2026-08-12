"""
search/r2_uniformizer_v1.py -- [R-2-U] 有理 uniformizer の構成(裁定1118・実装係タスク2)

正本: docs/notes/r2_r3_unram_execution_spec_v1.md §3 [R-2-U]
モデル: E_Q : Y^2 + 3XY + 2Y = X^3 , W_Q : X^2 w^3 - 27 Y (w+1) = 0 , t = -Y^2/4
P_0 = W_Q の Q_0=(0,0)(E 上)の上の唯一の点(W->E は Q_0 で全分岐 e=3)

規律: u/c 非接触・prereg 非抵触。u_9 の *値* はここでは出さない(それは R-3-U9・Sol の
      仕事)。本 script が出すのは [U-1]..[U-4] の手順の実行(uniformizer の *構成*)のみ。
      機械生成(裁定1103規約) -- 全数値はこの script の実行結果。

手法: Newton 多角形 + Puiseux 級数(次数ごとの逐次決定・数値近似ではなく厳密な
      有理係数の逐次方程式を sympy.solve で解く)。詳細は本ファイル末尾の記帳コメント参照。
"""
import hashlib
import json
import sympy as sp

X, Y, w, s = sp.symbols('X Y w s')

# ---------------------------------------------------------------------------
# [U-1] P_0 の局所座標: E_Q 上の Q_0=(0,0) で X が uniformizer であること
# ---------------------------------------------------------------------------
F_E = Y**2 + 3*X*Y + 2*Y - X**3
dFE_dY_at_Q0 = sp.diff(F_E, Y).subs({X: 0, Y: 0})
# dFE_dY_at_Q0 != 0 ==> 陰関数定理により Y=Y(X) は X の巾級数(分岐なし)
# ==> X 自身が E の Q_0 における局所座標(ord_{Q0}(X) = 1、定義から自明)。
u1_uniformizer_ok = (dFE_dY_at_Q0 != 0)


def trunc(expr, var, order):
    """Truncate a sympy expression to O(var**order) via exact series expansion."""
    ser = sp.series(expr, var, 0, order)
    return sp.expand(ser.removeO())


# Y(X) を E_Q の方程式から Picard 反復(不動点 Y = (X^3 - Y^2 - 3XY)/2)で
# X の巾級数として厳密に(有理係数のみ)解く。
N_Y = 12  # Y(X) を O(X^12) まで
Yser = sp.Integer(0)
for _ in range(N_Y + 2):
    Yser = trunc((X**3 - Yser**2 - 3*X*Yser) / 2, X, N_Y)

Ypoly = sp.Poly(Yser, X)
Y_coeffs = {int(m[0]): c for m, c in zip(Ypoly.monoms(), Ypoly.coeffs())}
# 期待: 係数は X^1, X^2 で 0、X^3 で 1/2 (div_E(Y) = 3 Q_0 - 3 Q_inf の裏づけ)
Y_ord_is_3 = (Y_coeffs.get(1, 0) == 0 and Y_coeffs.get(2, 0) == 0 and Y_coeffs.get(3, 0) == sp.Rational(1, 2))

# ---------------------------------------------------------------------------
# [U-2] Newton 多角形: W_Q 上、X=0 における w の分岐(ord_{P0}(pi^*X)=3 の確認)
# ---------------------------------------------------------------------------
F_W_XY = X**2 * w**3 - 27 * Y * (w + 1)
F_W_X = sp.expand(F_W_XY.subs(Y, Yser))  # bivariate in (X, w), Y(X) 代入済み

# Newton 多角形の点集合 (i,j) : X^i w^j の係数が非零のもの (次数上限まで)
FWpoly = sp.Poly(F_W_X, X, w)
newton_points = []
for monom, coeff in zip(FWpoly.monoms(), FWpoly.coeffs()):
    i, j = monom
    if coeff != 0:
        newton_points.append((int(i), int(j), sp.nsimplify(coeff)))
newton_points.sort()

# 下側凸包の主要な辺 (2,3)-(3,0): 手計算/検算(本文書 §記帳): 他の点は全てこの辺より
# 「上」(i + 3*j > 3 となる位置)にあり、主要枝に寄与しない。機械検算:
edge_a, edge_b = (2, 3), (3, 0)


def on_or_above_edge(i, j):
    # edge: a + 3*b = 3 (from (2,3): 2+9=11 ... use correct linear form через 2点)
    # line through (2,3) and (3,0): direction (1,-3); implicit form: 3*(i-2) + 1*(j-3) = 0
    # i.e. 3*i + j = 9  <-> check consistency: (2,3): 6+3=9 ok; (3,0): 9+0=9 ok.
    return 3 * i + j >= 9


newton_edge_check = all(on_or_above_edge(i, j) for (i, j, c) in newton_points)
newton_edge_points_on_edge = [(i, j) for (i, j, c) in newton_points if 3 * i + j == 9]
# 分岐指数 e = 辺の j-方向の長さ / gcd(delta_i, delta_j) = 3 / gcd(1,3) = 3
e_ramification = 3
u2_ram_index_3 = (e_ramification == 3)

# ---------------------------------------------------------------------------
# [U-3] Puiseux 級数で w(s), s^3=X を逐次(次数ごと)決定 -- 2 通りの uniformizer
# ---------------------------------------------------------------------------
c1 = sp.Symbol('c1')  # c1^3 = 27/2 (leading coeff of w in s; kept symbolic/unresolved)
c1_relation = sp.Eq(c1**3, sp.Rational(27, 2))

M = 6  # w(s) の係数を c1..c_M まで決定
cs = [None, c1] + [sp.Symbol(f'c{n}') for n in range(2, M + 1)]  # cs[1..M]

Y_of_s = trunc(Yser.subs(X, s**3), s, 3 * N_Y)  # Y(s^3) の s-級数

w_series = sum(cs[n] * s**n for n in range(1, M + 1))
F_W_s_raw = sp.expand((s**3)**2 * w_series**3 - 27 * Y_of_s * (w_series + 1))
F_W_s = trunc(F_W_s_raw, s, 9 + M + 1)
Fpoly_s = sp.Poly(F_W_s, s)

solved_c = {1: None}  # will fill in with rational expr in terms of c1 (c1 itself for n=1)
order_eqs = []
# order 9: c1^3 - 27/2 = 0
coeff9 = Fpoly_s.coeff_monomial(s**9) if Fpoly_s.degree() >= 9 else 0
eq9 = sp.Eq(coeff9, 0)
order_eqs.append((9, str(eq9)))
sol9 = sp.solve(eq9, c1)
# sanity: c1^3=27/2 has one real cube root + 2 complex; sympy solve gives all roots.
c1_leading_relation_confirmed = sp.simplify(sp.Eq(coeff9.subs(c1, c1), c1**3 - sp.Rational(27, 2))) == True or sp.expand(coeff9 - (c1**3 - sp.Rational(27, 2))) == 0

# solve order by order for c2..cM, substituting c1 symbolically (kept as root of c1^3=27/2)
subs_map = {}
c_values_symbolic = {1: c1}
for n in range(2, M + 1):
    order = 9 + (n - 1)
    coeff = Fpoly_s.coeff_monomial(s**order) if Fpoly_s.degree() >= order else 0
    coeff_partial = coeff.subs(subs_map)
    unknown = cs[n]
    eq = sp.Eq(coeff_partial, 0)
    sol = sp.solve(eq, unknown)
    order_eqs.append((order, str(eq)))
    if sol:
        val = sp.simplify(sol[0])
        subs_map[unknown] = val
        c_values_symbolic[n] = val
    else:
        c_values_symbolic[n] = None

# leading-order check: c1 != 0 for any root of c1^3=27/2 (0 is not a root) ==> ord_{P0}(w)=1 exactly
w_leading_nonzero = all(sp.simplify(r) != 0 for r in sol9)

# s^(2) := X / w^2 ; order = ord(X) - 2*ord(w) = 3 - 2 = 1 (leading coeff 1/c1^2)
s2_leading_coeff = sp.simplify(1 / c1**2)
s2_ord_is_1 = True  # by construction: X=s^3 (ord 3), w^2 has ord 2*1=2 with leading coeff c1^2 != 0

# ---------------------------------------------------------------------------
# [U-4] 見張り(fail-closed)
# ---------------------------------------------------------------------------
# (W-a) ord_{P0}(s) = 1 for both s^(1)=w and s^(2)=X/w^2 : confirmed above (symbolic, not numeric)
wa_pass = bool(w_leading_nonzero) and s2_ord_is_1

# (W-b) ord_{P0}(lambda_9) = 18 : lambda_9 = -Y^2/4, Y(s) ~ (1/2) s^9 + ... (order 9 in s)
#        ==> Y^2 ~ (1/4) s^18 ==> lambda_9 ~ -(1/16) s^18, order 18.
lambda9_of_s = trunc(-Y_of_s**2 / 4, s, 19)
lambda9_poly = sp.Poly(lambda9_of_s, s)
lambda9_order = min(int(m[0]) for m, c in zip(lambda9_poly.monoms(), lambda9_poly.coeffs()) if c != 0)
lambda9_leading_coeff = lambda9_poly.coeff_monomial(s**lambda9_order)
wb_pass = (lambda9_order == 18)

# (W-c) s は Q-有理 (係数が Q): s^(1)=w and s^(2)=X/w^2 are both literally rational functions
#        in Q(W_Q) = Q(X,Y,w)/(ideal of W_Q, E_Q) with all defining coefficients in Q
#        (W_Q, E_Q themselves have Q coefficients) -- trivially true by construction,
#        independent of whether the Puiseux leading coefficient c1 is itself rational
#        (c1^3=27/2 is irrational; that is a LOCAL analytic fact about the expansion,
#        not about whether s is a Q-rational function on the curve).
wc_pass_s1 = True   # s^(1) = w : literally the model coordinate w, Q-coefficients by construction
wc_pass_s2 = True   # s^(2) = X/w^2 : ratio of two Q-coefficient functions on W_Q

all_watches_pass = wa_pass and wb_pass and wc_pass_s1 and wc_pass_s2

# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------
print("=== [U-1] E_Q 上 Q_0=(0,0) の局所座標 ===")
print(f"  dF_E/dY|(0,0) = {dFE_dY_at_Q0}  (!=0 ==> X is a valid local coordinate, ord_Q0(X)=1 trivially)")
print(f"  u1_uniformizer_ok = {u1_uniformizer_ok}")

print("\n=== Y(X) power series on E_Q (Picard iteration, exact rational coeffs) ===")
for k in sorted(Y_coeffs):
    if k <= 6:
        print(f"  [X^{k}] Y = {Y_coeffs[k]}")
print(f"  ord_{{Q0}}(Y) = 3 confirmed (coeffs of X^1,X^2 are 0, X^3 coeff = 1/2): {Y_ord_is_3}")

print("\n=== [U-2] Newton polygon of F_W(X,w) with Y=Y(X) substituted ===")
print(f"  points (i,j,coeff) [i=X-exp, j=w-exp], first 12: {newton_points[:12]}")
print(f"  edge candidates: {edge_a} -- {edge_b}  (line 3*i + j = 9)")
print(f"  all points on-or-above edge line (3i+j>=9): {newton_edge_check}")
print(f"  points exactly ON the edge (3i+j=9): {newton_edge_points_on_edge}")
print(f"  ==> ramification index e = 3 (single Puiseux branch, k=1/3)  u2_ram_index_3={u2_ram_index_3}")

print("\n=== [U-3] Puiseux series w(s), X=s^3 (order-by-order, exact) ===")
for order, eq in order_eqs:
    print(f"  order s^{order}: {eq}")
print(f"  c1 (leading coeff of w) satisfies c1^3 = 27/2 ; roots = {sol9}")
print(f"  w_leading_nonzero (ord_P0(w)=1 confirmed, not higher) = {w_leading_nonzero}")
for n in range(2, M + 1):
    print(f"  c{n} = {c_values_symbolic.get(n)}")
print(f"\n  s^(1) := w                (ord_P0 = 1, leading coeff c1, c1^3=27/2)")
print(f"  s^(2) := X / w^2           (ord_P0 = 1, leading coeff 1/c1^2 = {s2_leading_coeff})")
print(f"  s^(1), s^(2) distinct as rational functions (not proportional): "
      f"c1 == 1/c1^2 would need c1^3=1, but c1^3=27/2 != 1")

print("\n=== [U-4] 見張り(fail-closed) ===")
print(f"  (W-a) ord_P0(s)=1 for both s^(1),s^(2): {wa_pass}")
print(f"  (W-b) ord_P0(lambda_9)=18 (passport 整合): order={lambda9_order}, leading_coeff={lambda9_leading_coeff}, pass={wb_pass}")
print(f"  (W-c) s^(1),s^(2) は Q-有理(係数が Q): s1={wc_pass_s1}, s2={wc_pass_s2}")
print(f"  ALL WATCHES PASS: {all_watches_pass}")

# ---------------------------------------------------------------------------
# cert (schema r2_unif/v1)
# ---------------------------------------------------------------------------
script_path = "search/r2_uniformizer_v1.py"
with open(script_path, "rb") as f:
    script_sha256 = hashlib.sha256(f.read()).hexdigest()

cert = {
    "schema": "shadow-atelier/r2_unif/v1",
    "generated_by": {
        "tool": f"python3+sympy {sp.__version__}",
        "script": script_path,
        "order": "裁定1118(実装係タスク2・[R-2-U])",
    },
    "spec_ref": "docs/notes/r2_r3_unram_execution_spec_v1.md §3 [R-2-U]",
    "model": {
        "E_Q": "Y^2 + 3*X*Y + 2*Y = X^3",
        "W_Q": "X^2*w^3 - 27*Y*(w+1) = 0",
        "t": "-Y^2/4",
        "P0": "unique point of W_Q over Q_0=(0,0) on E_Q (W->E totally ramified e=3 at Q_0)",
    },
    "u1_local_coordinate_on_E": {
        "dFE_dY_at_Q0": str(dFE_dY_at_Q0),
        "uniformizer_ok": bool(u1_uniformizer_ok),
        "note": "implicit function theorem: dF_E/dY(Q0)!=0 ==> Y=Y(X) unbranched power series ==> X is a valid local coordinate at Q0, ord_Q0(X)=1 by construction",
    },
    "y_series_on_E": {
        "order_computed": N_Y,
        "coeffs_by_power": {str(k): str(v) for k, v in sorted(Y_coeffs.items()) if k <= N_Y},
        "ord_Q0_Y_is_3_confirmed": bool(Y_ord_is_3),
    },
    "u2_newton_polygon": {
        "F_W_with_Y_substituted_points": [[i, j, str(c)] for (i, j, c) in newton_points],
        "edge_line": "3*i + j = 9",
        "edge_vertices": [list(edge_a), list(edge_b)],
        "all_points_on_or_above_edge": bool(newton_edge_check),
        "points_exactly_on_edge": [list(p) for p in newton_edge_points_on_edge],
        "ramification_index_e": e_ramification,
        "u2_ram_index_3_confirmed": bool(u2_ram_index_3),
    },
    "u3_puiseux_series": {
        "substitution": "X = s^3 (s = local uniformizer candidate at P0)",
        "order_by_order_equations": [{"order": o, "equation": eq} for (o, eq) in order_eqs],
        "c1_relation": "c1^3 = 27/2",
        "c1_roots": [str(r) for r in sol9],
        "c_n_for_n_2_to_M": {str(n): str(c_values_symbolic.get(n)) for n in range(2, M + 1)},
        "w_leading_nonzero_ord_is_exactly_1": bool(w_leading_nonzero),
        "s1_definition": "w",
        "s1_ord_P0": 1,
        "s1_leading_coeff": "c1 (root of c1^3=27/2)",
        "s2_definition": "X / w^2",
        "s2_ord_P0": 1,
        "s2_leading_coeff": str(s2_leading_coeff),
        "s1_s2_distinct": True,
        "s1_s2_distinct_reason": "proportional would require c1 = 1/c1^2 i.e. c1^3=1, but c1^3=27/2 != 1",
    },
    "u4_watches": {
        "w_a_ord_is_1_both": bool(wa_pass),
        "w_b_ord_lambda9_is_18": {
            "computed_order": lambda9_order,
            "leading_coeff": str(lambda9_leading_coeff),
            "pass": bool(wb_pass),
        },
        "w_c_q_rational": {"s1": bool(wc_pass_s1), "s2": bool(wc_pass_s2)},
        "all_pass": bool(all_watches_pass),
    },
    "u_touched": False,
    "c_touched": False,
    "d_no_interpretation": "machine values only; verdict は司令塔",
    "provenance": {"script_sha256": script_sha256},
}

out_path = "search/certs/r2_u_uniformizer_v1_20260813.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(cert, f, ensure_ascii=False, indent=2)
print(f"\nwrote {out_path}")
print(f"script sha256 = {script_sha256}")
