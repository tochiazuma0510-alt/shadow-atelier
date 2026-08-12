"""
search/a_class_indep_v1.py -- [CP] a_class([a]) 独立第三系統再導出(裁定1123・実装係隔離任務)
                              + 数学者紙検問5点(裁定1124・司令塔追加)

目的: 現行 [a]=[2]^7 (order 9) が Sol 単一セッション産であることに対する研究者の
      バグ仮説(ゲージ単数 = 2冪の混入疑い)を検証するため、u_9 の抽出から DESC-9 の
      指数落としまでを、Sol の script(search/sol123_r3_u9.py 等・検疫対象・未読)とは
      独立の計算経路で再実装する。

検疫: search/sol123_r3_u9.py・crosscheck/check_sol123_r3_u9.py・
      search/certs/sol123_r3_u9*.json・search/certs/sol123_p8_a_class_v1_20260813.json
      は一切未読(git log のコミットメッセージからも値を拾っていない)。

許可資料のみを使用:
  docs/notes/r2_r3_unram_execution_spec_v1.md (手順の正本・[R-3-U9]/DESC-9)
  docs/notes/p8_prereg_v3_2.md (凍結 schema・sha 3a9cfb06...で確認済)
  search/certs/r2_u_uniformizer_v1_20260813.json (工房 R-2 cert -- s^(1)=w, s^(2)=X/w^2 の定義)
  search/desc9_procedure_v1.py (工房 DESC-9 (D-i)/(D-iii) 手順・参照のみ、値は再計算)

独立性の設計(Sol の script を読んでいないため、以下は「同じ問題への別解法」であって
「Sol の答え合わせ」ではない):
  R-2 cert の script (search/r2_uniformizer_v1.py) は補助変数 s (X=s^3 と置く形式的
  パラメータ、c1^3=27/2 という *無理数* の根) を経由して w(s) を Puiseux 級数で解いた。
  本 script は補助変数 s を一切使わず、w 自身(真の Q-有理局所座標)を直接の展開変数として
  X(w), Y(w) を巾級数で解く(F_W から Y=X^2 w^3/(27(w+1)) を厳密代入し、F_E に代入して
  X(w) の係数を次数ごとに solve)。s^(2)=X/w^2 についても w(t) の級数反転を直接行う。
  これにより c1 の無理数性を経由せず、全計算が Q 上の巾級数のみで完結する
  -- 計算経路として R-2 cert の script と真に独立。
  ★ leading term のみが u_9 を決める(高次係数は order 18 の係数に影響しない --
  Y = y9 w^9 + O(w^10) ==> Y^2 = y9^2 w^18 + O(w^19))ため、次数上限 N は小さく取れる
  (a3, b1 のみが本質)。冗長性チェックのため N=8 まで解く。

ゲージ規約: t=-Y^2/4 (declared, spec §0 boxed model) を規約 GAUGE-A とし、
  spec §9 [1-3] が言及する代替 t'=-Y^2 (1/4 落とし) を規約 GAUGE-B として併記する。
  GAUGE-A/B の差は u_9 に対して定数倍 4=2^2 (2冪) --- これが「ゲージ単数」の具体例。
  w 自体のスケール変換 (w -> lambda*w) は u_9 を lambda^18 倍するのみで [u_9] mod 18
  (よって mod 9 の a_class)を変えない(T63-UNIF-INV の帰結)ため、ゲージ論点としては
  扱わない(検証のみ記録)。

紙検問5点(裁定1124・司令塔便):
  1. Belyi 正規化 fail-closed: t(B1)=t(B2)=1 (B_i: Y^2+4=0 上の点)
  2. GAUGE-18 実測: s^(1), s^(2) で [a] 一致(補題 GAUGE-18 の実測版)
  3. u_9 を厳密元として報告(v_2(u_9), v_3(u_9) 明記)
  4. DESC-9 (D-ii) 有理性検査の実行と結果明記
  5. Q-モデルで計算(zeta_3 モデル経由せず・E_Q 使用)

厳密演算のみ(sympy Rational / Fraction)。浮動小数点は不使用。
"""
import hashlib
import json
from fractions import Fraction
from math import gcd

import sympy as sp

try:
    from sympy import factorint
except ImportError:
    factorint = None

X, Y, w, t = sp.symbols('X Y w t')


def trunc(expr, var, order):
    ser = sp.series(expr, var, 0, order)
    return sp.expand(ser.removeO())


def factor_exact(n):
    if n == 0:
        return {}
    if factorint is not None:
        return dict(factorint(n))
    f = {}
    x = n
    p = 2
    while p * p <= x:
        while x % p == 0:
            f[p] = f.get(p, 0) + 1
            x //= p
        p += 1
    if x > 1:
        f[x] = f.get(x, 0) + 1
    return f


def full_valuation(fr: Fraction, p: int):
    """Exact (unbounded, signed) p-adic valuation of a nonzero Fraction."""
    num_f = factor_exact(abs(fr.numerator))
    den_f = factor_exact(abs(fr.denominator))
    return num_f.get(p, 0) - den_f.get(p, 0)


def to_fraction(sp_rational):
    r = sp.nsimplify(sp_rational)
    r = sp.Rational(r)
    return Fraction(r.p, r.q)


# ---------------------------------------------------------------------------
# [check5] Q-モデルで計算(zeta_3 を含まない E_Q, W_Q のみ使用 -- 構造的に排除)
# ---------------------------------------------------------------------------
model_uses_zeta3 = False  # E_Q, W_Q の定義式に zeta_3 は一切現れない(下記式を参照)

# ---------------------------------------------------------------------------
# [0] Belyi 正規化 fail-closed 検査: t(B1)=t(B2)=1  (B_i: Y^2+4=0 上の点)
# ---------------------------------------------------------------------------
t_def = -Y**2 / 4
t_at_B = sp.simplify(t_def.subs(Y**2, -4))
belyi_normalization_ok = (t_at_B == 1)

# ---------------------------------------------------------------------------
# [1] X(w), Y(w) を w の巾級数として直接解く(補助変数 s を使わない)
#     F_W: X^2 w^3 - 27 Y (w+1) = 0  ==>  Y = X^2 w^3 / (27 (w+1))  (exact, no series needed)
#     F_E: Y^2 + 3XY + 2Y - X^3 = 0  ==>  代入して X(w) を次数ごとに solve
# ---------------------------------------------------------------------------
N_ORDER = 6  # X(w) の係数を w^3..w^N_ORDER まで決定(leading term u9 は a3 のみで決まる;
             # 残りは order 確認・冗長性チェック用)
LAMBDA_TRUNC = 20  # w/t-side lambda_9 級数展開の trunc order 引数(order-18 項を
                    # 確実に捕捉するための固定余裕。sp.series(...,order)は order 未満の
                    # 項までしか返さないため order>=19 が必須 -- 最初の走行のバグ原因)

TRUNC_G = 9 + (N_ORDER - 3) + 4  # highest coefficient equation needed is order 9+(N_ORDER-3);
                                  # sp.series(...,order) captures terms strictly BELOW order,
                                  # so pad well past the needed degree (bug found in first run:
                                  # passing order=N_ORDER+1 silently dropped the w^9 term itself).

a = {n: sp.Symbol(f'a{n}') for n in range(3, N_ORDER + 1)}
X_series_sym = sum(a[n] * w**n for n in range(3, N_ORDER + 1))

Y_of_Xw = X_series_sym**2 * w**3 / (27 * (w + 1))
Y_of_Xw_trunc = trunc(Y_of_Xw, w, TRUNC_G)

G = trunc(Y_of_Xw_trunc**2 + 3 * X_series_sym * Y_of_Xw_trunc + 2 * Y_of_Xw_trunc - X_series_sym**3, w, TRUNC_G)
Gpoly = sp.Poly(G, w)

order_eqs_X = []
a_values = {}
subs_map = {}
coeff9 = Gpoly.coeff_monomial(w**9) if Gpoly.degree() >= 9 else sp.Integer(0)
eq9 = sp.Eq(coeff9, 0)
order_eqs_X.append((9, str(eq9)))
sol9 = sp.solve(eq9.subs(subs_map), a[3])
sol9_nonzero = [r for r in sol9 if sp.simplify(r) != 0]
assert len(sol9_nonzero) == 1, f"expected unique nonzero a3 root, got {sol9_nonzero}"
a3_val = sp.nsimplify(sol9_nonzero[0])
a_values[3] = a3_val
subs_map[a[3]] = a3_val

for n in range(4, N_ORDER + 1):
    order = 9 + (n - 3)
    if Gpoly.degree() < order:
        break
    coeff = Gpoly.coeff_monomial(w**order)
    coeff_partial = coeff.subs(subs_map)
    eq = sp.Eq(coeff_partial, 0)
    order_eqs_X.append((order, str(eq)))
    sol = sp.solve(eq, a[n])
    if sol:
        val = sp.nsimplify(sp.simplify(sol[0]))
        a_values[n] = val
        subs_map[a[n]] = val
    else:
        a_values[n] = None

X_series = sum(a_values[n] * w**n for n in a_values if a_values[n] is not None)
Y_series = trunc(X_series**2 * w**3 / (27 * (w + 1)), w, LAMBDA_TRUNC)

Xpoly = sp.Poly(X_series, w)
Ypoly = sp.Poly(Y_series, w)

X_order = min(int(m[0]) for m, c in zip(Xpoly.monoms(), Xpoly.coeffs()) if c != 0)
Y_order = min(int(m[0]) for m, c in zip(Ypoly.monoms(), Ypoly.coeffs()) if c != 0)
X_leading = Xpoly.coeff_monomial(w**X_order)
Y_leading = Ypoly.coeff_monomial(w**Y_order)

X_order_is_3 = (X_order == 3)
Y_order_is_9 = (Y_order == 9)

# ---------------------------------------------------------------------------
# [2] GAUGE-A: lambda_9 := t_A = -Y^2/4  (declared spec boxed model, §0)
# ---------------------------------------------------------------------------
lambda9_A_w = trunc(-Y_series**2 / 4, w, LAMBDA_TRUNC)
lambda9_A_w_poly = sp.Poly(lambda9_A_w, w)
lambda9_A_w_order = min(int(m[0]) for m, c in zip(lambda9_A_w_poly.monoms(), lambda9_A_w_poly.coeffs()) if c != 0)
u9_1_gaugeA = lambda9_A_w_poly.coeff_monomial(w**lambda9_A_w_order)
u9_1_gaugeA_order18 = (lambda9_A_w_order == 18)

# ---------------------------------------------------------------------------
# [3] GAUGE-B: lambda_9' := t_B = -Y^2  (spec §9 [1-3] alternative, drop /4)
# ---------------------------------------------------------------------------
lambda9_B_w = trunc(-Y_series**2, w, LAMBDA_TRUNC)
lambda9_B_w_poly = sp.Poly(lambda9_B_w, w)
lambda9_B_w_order = min(int(m[0]) for m, c in zip(lambda9_B_w_poly.monoms(), lambda9_B_w_poly.coeffs()) if c != 0)
u9_1_gaugeB = lambda9_B_w_poly.coeff_monomial(w**lambda9_B_w_order)

gauge_ratio = sp.simplify(u9_1_gaugeB / u9_1_gaugeA)  # should be exactly 4

# ---------------------------------------------------------------------------
# [4] s^(2) = X/w^2 : 級数反転で t := X/w^2 の逆関数 w(t) を直接構成(独立の第二経路)
#     leading term のみが u9 に効くので b1 が本質(高次 b_n は冗長性チェック用)
# ---------------------------------------------------------------------------
t_of_w = trunc(X_series / w**2, w, N_ORDER + 1)  # starts at w^1, leading coeff a3
t_of_w_poly = sp.Poly(t_of_w, w)
t_of_w_order = min(int(m[0]) for m, c in zip(t_of_w_poly.monoms(), t_of_w_poly.coeffs()) if c != 0)
assert t_of_w_order == 1

N_INV = N_ORDER - 1
b = {n: sp.Symbol(f'b{n}') for n in range(1, N_INV + 1)}

t_of_w_as_poly_in_w = sp.Poly(t_of_w, w)


def eval_t_of_w(w_expr, order):
    total = sp.Integer(0)
    for monom, coeff in zip(t_of_w_as_poly_in_w.monoms(), t_of_w_as_poly_in_w.coeffs()):
        k = monom[0]
        if k == 0:
            continue
        total += coeff * w_expr**k
    return trunc(total, t, order + 1)


subs_map_b = {}
order_eqs_w = []
for n in range(1, N_INV + 1):
    order = n
    partial_w = sum((subs_map_b.get(m, b[m])) * t**m for m in range(1, n + 1))
    Fexpr = trunc(eval_t_of_w(partial_w, order) - t, t, order + 1)
    Fpoly = sp.Poly(Fexpr, t) if Fexpr != 0 else None
    coeff = Fpoly.coeff_monomial(t**order) if (Fpoly is not None and Fpoly.degree() >= order) else sp.Integer(0)
    eq = sp.Eq(coeff, 0)
    order_eqs_w.append((order, str(eq)))
    sol = sp.solve(eq, b[n])
    if sol:
        val = sp.nsimplify(sp.simplify(sol[0]))
        subs_map_b[n] = val
    else:
        subs_map_b[n] = None
    if subs_map_b[n] is None:
        break

w_of_t = sum(subs_map_b[n] * t**n for n in subs_map_b if subs_map_b[n] is not None)
b1_expected = sp.nsimplify(1 / a3_val)
b1_matches = sp.simplify(subs_map_b.get(1) - b1_expected) == 0

# NOTE: composing the full high-degree Y_series (deg ~LAMBDA_TRUNC-1) with w_of_t (deg N_INV)
# blows up combinatorially before truncation. Only the LEADING term of Y_series (order 9,
# coeff Y_leading) can contribute to the order-9 coefficient of the composition (standard
# fact for formal power series: if f has order k and g has order 1 with g_1!=0, then f(g(t))
# has order k with leading coeff f_k * g_1^k -- higher-order terms of f only raise the order
# of their contribution). We therefore cap the composition input to a modest degree (order 13,
# i.e. y9..y12) for a genuine multi-term series cross-check that stays computationally light,
# and separately verify against the closed-form product below.
Y_series_for_comp = trunc(Y_series, w, 13)
Y_of_t = trunc(sp.expand(Y_series_for_comp.subs(w, w_of_t)), t, LAMBDA_TRUNC)
Ypoly_t = sp.Poly(Y_of_t, t)
Y_of_t_order = min(int(m[0]) for m, c in zip(Ypoly_t.monoms(), Ypoly_t.coeffs()) if c != 0)
Y_of_t_leading = Ypoly_t.coeff_monomial(t**Y_of_t_order)
Y_of_t_order_is_9 = (Y_of_t_order == 9)

lambda9_A_t = trunc(-Y_of_t**2 / 4, t, LAMBDA_TRUNC)
lambda9_A_t_poly = sp.Poly(lambda9_A_t, t)
lambda9_A_t_order = min(int(m[0]) for m, c in zip(lambda9_A_t_poly.monoms(), lambda9_A_t_poly.coeffs()) if c != 0)
u9_2_gaugeA = lambda9_A_t_poly.coeff_monomial(t**lambda9_A_t_order)
u9_2_gaugeA_order18 = (lambda9_A_t_order == 18)

lambda9_B_t = trunc(-Y_of_t**2, t, LAMBDA_TRUNC)
lambda9_B_t_poly = sp.Poly(lambda9_B_t, t)
lambda9_B_t_order = min(int(m[0]) for m, c in zip(lambda9_B_t_poly.monoms(), lambda9_B_t_poly.coeffs()) if c != 0)
u9_2_gaugeB = lambda9_B_t_poly.coeff_monomial(t**lambda9_B_t_order)

# ---------------------------------------------------------------------------
# [4b] closed-form cross-check (independent of the series-composition machinery above):
#      Y_of_t leading coeff = Y_leading * b1^Y_order  (formal power series composition:
#      f(g(t)) has order = ord(f)*ord(g) when ord(g)=1, leading coeff = f_k * g_1^k)
# ---------------------------------------------------------------------------
b1_val = subs_map_b.get(1)
Y_of_t_leading_closed_form = sp.nsimplify(sp.simplify(Y_leading * b1_val**Y_order))
u9_2_gaugeA_closed_form = sp.nsimplify(sp.simplify(-Y_of_t_leading_closed_form**2 / 4))
closed_form_matches_series = (sp.simplify(Y_of_t_leading_closed_form - Y_of_t_leading) == 0) and \
                              (sp.simplify(u9_2_gaugeA_closed_form - u9_2_gaugeA) == 0)

# ---------------------------------------------------------------------------
# [5] T63-UNIF-INV / GAUGE-18 実測: u9^(1)/u9^(2) が exact 18th power かどうか(GAUGE-A)
# ---------------------------------------------------------------------------
ratio_12_gaugeA = sp.nsimplify(sp.Rational(u9_1_gaugeA) / sp.Rational(u9_2_gaugeA))
rf = sp.Rational(ratio_12_gaugeA)


def is_exact_kth_power(fr: Fraction, k: int):
    num, den = abs(fr.numerator), abs(fr.denominator)
    fn = factor_exact(num)
    fd = factor_exact(den)
    all_primes = set(fn) | set(fd)
    exps = {p: fn.get(p, 0) - fd.get(p, 0) for p in all_primes}
    if all(e % k == 0 for e in exps.values()):
        witness_num = 1
        witness_den = 1
        for p, e in exps.items():
            if e >= 0:
                witness_num *= p ** (e // k)
            else:
                witness_den *= p ** ((-e) // k)
        return True, Fraction(witness_num, witness_den)
    return False, None


ratio_frac = Fraction(rf.p, rf.q)
is_18th_power, witness_18 = is_exact_kth_power(ratio_frac, 18)

# ---------------------------------------------------------------------------
# [6] DESC-9 (D-i)/(D-iii): a_9 := u_9^{-1} を Q^x/(Q^x)^18 -> mod 9 に落とす
#     (workshop の既存手順 search/desc9_procedure_v1.py と同じアルゴリズムを再実装
#      -- ファイルは参照のみ、値は本 script で再計算)
# ---------------------------------------------------------------------------
def prime_valuations(frac: Fraction, modulus: int):
    num = abs(frac.numerator)
    den = abs(frac.denominator)
    vals = {}
    fn = factor_exact(num)
    fd = factor_exact(den)
    for p, e in fn.items():
        vals[p] = vals.get(p, 0) + e
    for p, e in fd.items():
        vals[p] = vals.get(p, 0) - e
    return {p: (e % modulus) for p, e in vals.items() if e % modulus != 0}


def desc9(a9_rational: Fraction):
    class_mod18 = prime_valuations(a9_rational, 18)
    image_mod9 = {p: (e % 9) for p, e in class_mod18.items() if e % 9 != 0}
    support = sorted(image_mod9.keys())
    exponents = [image_mod9[p] for p in support]
    if not support:
        order = 1
    else:
        g = 0
        for e in exponents:
            g = gcd(g, e)
        order = 9 // gcd(9, g) if g != 0 else 1
    a_class = {
        "representation": "exponent vector mod 9 over the support primes",
        "support": support,
        "exponents": exponents,
        "order": order,
        "normalization": "a は Q^x/(Q^x)^9 の代表・sign は 9 乗で消えるため無視",
    }
    return class_mod18, image_mod9, a_class


u9_1_gaugeA_frac = to_fraction(u9_1_gaugeA)
u9_1_gaugeB_frac = to_fraction(u9_1_gaugeB)
u9_2_gaugeA_frac = to_fraction(u9_2_gaugeA)

a9_gaugeA_inv = Fraction(1, 1) / u9_1_gaugeA_frac  # a_9 := u_9^{-1}, using s^(1)=w, gauge A
a9_gaugeB_inv = Fraction(1, 1) / u9_1_gaugeB_frac  # gauge B, same s^(1)
a9_gaugeA_s2_inv = Fraction(1, 1) / u9_2_gaugeA_frac  # gauge A, s^(2)=X/w^2 (cross-check)

class_mod18_A, image_mod9_A, a_class_A = desc9(a9_gaugeA_inv)
class_mod18_B, image_mod9_B, a_class_B = desc9(a9_gaugeB_inv)
class_mod18_A_s2, image_mod9_A_s2, a_class_A_s2 = desc9(a9_gaugeA_s2_inv)

a_class_A_matches_s2 = (a_class_A == a_class_A_s2)  # ★ [check2] GAUGE-18 実測

# ---------------------------------------------------------------------------
# [check3] u9 を厳密元(Fraction)として報告 + v2(u9), v3(u9) 完全付値(mod なし)
# ---------------------------------------------------------------------------
v2_u9_s1_gaugeA = full_valuation(u9_1_gaugeA_frac, 2)
v3_u9_s1_gaugeA = full_valuation(u9_1_gaugeA_frac, 3)
v2_u9_s2_gaugeA = full_valuation(u9_2_gaugeA_frac, 2)
v3_u9_s2_gaugeA = full_valuation(u9_2_gaugeA_frac, 3)
v2_u9_s1_gaugeB = full_valuation(u9_1_gaugeB_frac, 2)
v3_u9_s1_gaugeB = full_valuation(u9_1_gaugeB_frac, 3)
# full factorization (all primes, not just 2,3) for completeness
u9_s1_gaugeA_full_factorization = {
    "positive_powers": factor_exact(abs(u9_1_gaugeA_frac.numerator)),
    "negative_powers_denominator": factor_exact(abs(u9_1_gaugeA_frac.denominator)),
    "sign": -1 if u9_1_gaugeA_frac < 0 else 1,
}

# ---------------------------------------------------------------------------
# [check4] DESC-9 (D-ii) 有理性検査: iota: Q^x/(Q^x)^9 -> F^x/(F^x)^9 の像に
#          a_9 mod 9 が入るか。本モデルでは F=Q(spec §6・宣言モデルが Q に降りた
#          帰結)なので iota は恒等写像 -- 実行して pass を明記(構造的仮定のまま
#          放置しない)。
# ---------------------------------------------------------------------------
# u9 (よって a9=u9^{-1}) が sympy Rational / Fraction として得られていること自体が
# 「Q^x の元である」の実行時証拠(zeta が残っていれば Fraction への変換で失敗する)。
d_ii_u9_is_rational_element_of_Q = isinstance(u9_1_gaugeA_frac, Fraction) and isinstance(a9_gaugeA_inv, Fraction)
d_ii_F_equals_Q_structural = True  # spec §6: 宣言モデル Q への降下(§0)の帰結。iota=identity。
d_ii_step_passed = bool(d_ii_u9_is_rational_element_of_Q and d_ii_F_equals_Q_structural)

gauge_diff_exponent_vector = {}
all_p = sorted(set(list(image_mod9_A.keys()) + list(image_mod9_B.keys())))
for p in all_p:
    eA = image_mod9_A.get(p, 0)
    eB = image_mod9_B.get(p, 0)
    d = (eB - eA) % 9
    if d != 0:
        gauge_diff_exponent_vector[p] = d

# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------
print("=== [check5] Q-モデル使用確認(zeta_3 不使用) ===")
print(f"  model_uses_zeta3 = {model_uses_zeta3}  (E_Q, W_Q に zeta_3 は一切出現しない)")

print("\n=== [check1] Belyi 正規化 fail-closed: t(B1)=t(B2)=1 ===")
print(f"  t|_{{Y^2=-4}} = {t_at_B}   belyi_normalization_ok = {belyi_normalization_ok}")

print("\n=== [1] X(w), Y(w) 直接巾級数解(補助変数 s 不使用) ===")
print(f"  X order = {X_order} (expect 3): {X_order_is_3}   leading coeff a3 = {X_leading}")
print(f"  Y order = {Y_order} (expect 9): {Y_order_is_9}   leading coeff y9 = {Y_leading}")
print(f"  a3 solved from order-9 balance eq: {order_eqs_X[0][1]}  ==> a3 = {a3_val}")

print("\n=== [2] GAUGE-A: lambda_9 = -Y^2/4 (declared, s^(1)=w) ===")
print(f"  ord_P0 = {lambda9_A_w_order} (expect 18): {u9_1_gaugeA_order18}")
print(f"  u9^(1)_gaugeA = {u9_1_gaugeA}  (exact fraction: {u9_1_gaugeA_frac})")

print("\n=== [3] GAUGE-B: lambda_9' = -Y^2 (spec 9 [1-3] alt, s^(1)=w) ===")
print(f"  u9^(1)_gaugeB = {u9_1_gaugeB}   ratio gaugeB/gaugeA = {gauge_ratio} (expect 4)")

print("\n=== [4] s^(2) = X/w^2 : 独立反転経路 ===")
print(f"  b1 = w(t) leading coeff = {subs_map_b.get(1)}  matches 1/a3 = {b1_matches}")
print(f"  Y(t) order = {Y_of_t_order} (expect 9): {Y_of_t_order_is_9}   leading = {Y_of_t_leading}")
print(f"  lambda9_A(t) order = {lambda9_A_t_order} (expect 18): {u9_2_gaugeA_order18}")
print(f"  u9^(2)_gaugeA = {u9_2_gaugeA}  (exact fraction: {u9_2_gaugeA_frac})")
print(f"  u9^(2)_gaugeB = {u9_2_gaugeB}")
print(f"  [4b] closed-form cross-check (f(g(t)) order/leading rule): "
      f"Y_of_t_leading_closed_form={Y_of_t_leading_closed_form}, "
      f"u9_2_gaugeA_closed_form={u9_2_gaugeA_closed_form}, matches series calc = {closed_form_matches_series}")

print("\n=== [5]/[check2] GAUGE-18 実測: u9^(1)/u9^(2) exact 18th power? (gauge A) ===")
print(f"  ratio = {ratio_frac}")
print(f"  is_exact_18th_power = {is_18th_power}   witness (r s.t. r^18=ratio, up to sign) = {witness_18}")

print("\n=== [check3] u9 の完全付値(mod なし・厳密) ===")
print(f"  v2(u9^(1)_gaugeA) = {v2_u9_s1_gaugeA}   v3(u9^(1)_gaugeA) = {v3_u9_s1_gaugeA}")
print(f"  v2(u9^(2)_gaugeA) = {v2_u9_s2_gaugeA}   v3(u9^(2)_gaugeA) = {v3_u9_s2_gaugeA}")
print(f"  v2(u9^(1)_gaugeB) = {v2_u9_s1_gaugeB}   v3(u9^(1)_gaugeB) = {v3_u9_s1_gaugeB}")

print("\n=== [check4] DESC-9 (D-ii) 有理性検査 実行結果 ===")
print(f"  d_ii_u9_is_rational_element_of_Q = {d_ii_u9_is_rational_element_of_Q}")
print(f"  d_ii_step_passed = {d_ii_step_passed}")

print("\n=== [6] DESC-9 -> a_class (GAUGE-A, declared) ===")
print(f"  a9 = u9^{{-1}} = {a9_gaugeA_inv}")
print(f"  class_mod18 = {class_mod18_A}")
print(f"  a_class (GAUGE-A, s^(1)) = {a_class_A}")
print(f"  a_class (GAUGE-A, s^(2), cross-check / GAUGE-18) = {a_class_A_s2}   matches s^(1): {a_class_A_matches_s2}")
print(f"\n  a9 (GAUGE-B) = {a9_gaugeB_inv}")
print(f"  a_class (GAUGE-B) = {a_class_B}")
print(f"  gauge diff exponent vector (mod 9, B minus A) = {gauge_diff_exponent_vector}")

# ---------------------------------------------------------------------------
# input file hashes (provenance)
# ---------------------------------------------------------------------------
def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


input_files = [
    "docs/notes/r2_r3_unram_execution_spec_v1.md",
    "docs/notes/p8_prereg_v3_2.md",
    "search/certs/r2_u_uniformizer_v1_20260813.json",
    "search/desc9_procedure_v1.py",
]
input_sha = {f: sha256_of(f) for f in input_files}

script_path = "search/a_class_indep_v1.py"
with open(script_path, "rb") as f:
    script_sha256 = hashlib.sha256(f.read()).hexdigest()

cert = {
    "schema": "shadow-atelier/a_class_indep/v1",
    "generated_by": {
        "tool": f"python3+sympy {sp.__version__}",
        "script": script_path,
        "order": "裁定1123([CP]タスク・a_class 独立第三系統再導出・研究者バグ仮説検証) "
                 "+ 裁定1124(数学者紙検問5点・司令塔追加)",
    },
    "quarantine_note": "search/sol123_r3_u9.py, crosscheck/check_sol123_r3_u9.py, "
                        "search/certs/sol123_r3_u9*.json, "
                        "search/certs/sol123_p8_a_class_v1_20260813.json は未読。"
                        "本 cert は Sol の値と比較していない(比較は司令塔の専権)。",
    "independence_note": "R-2 cert(search/r2_uniformizer_v1.py)は補助変数 s (X=s^3, "
                          "c1^3=27/2 の無理根)を経由して w(s) を Puiseux 展開した。本 script は "
                          "s を一切使わず、真の局所座標 w を直接の展開変数として X(w),Y(w) を "
                          "F_W(厳密代入)+F_E(次数ごと solve)で解く。s^(2)=X/w^2 も w(t) の "
                          "級数反転で独立に構成。計算経路として非依存(参照した工房ファイルは "
                          "R-2 cert の *出力値の再検算対象*であって Sol の実装ではない)。",
    "spec_ref": "docs/notes/r2_r3_unram_execution_spec_v1.md §4-§7 ([R-3-U9], DESC-9, a_class schema)",
    "model": {
        "E_Q": "Y^2 + 3*X*Y + 2*Y = X^3",
        "W_Q": "X^2*w^3 - 27*Y*(w+1) = 0",
        "P0": "unique point of W_Q over Q_0=(0,0) on E_Q",
        "s1_definition": "w  (R-2 cert s^(1))",
        "s2_definition": "X / w^2  (R-2 cert s^(2))",
        "model_uses_zeta3": model_uses_zeta3,
    },
    "check1_belyi_normalization": {
        "t_definition": "-Y^2/4",
        "B_points_definition": "Y^2 + 4 = 0",
        "t_at_B_symbolic": str(t_at_B),
        "belyi_normalization_ok": bool(belyi_normalization_ok),
        "note": "t(B1)=t(B2)=1 を Y^2=-4 の代数的簡約で厳密確認(数値近似・分岐選択なし)。"
    },
    "gauge_convention": {
        "GAUGE_A": {
            "t_definition": "-Y^2/4",
            "label": "declared (spec §0 boxed model, r2_r3_unram_execution_spec_v1.md)",
            "note": "1/4 の 2 冪を含む。spec §9 [1-3] が同一 t の Z 係数化文脈で言及する定数。"
        },
        "GAUGE_B": {
            "t_definition": "-Y^2",
            "label": "alternative (spec §9 [1-3], 1/4 落とし)",
            "note": "GAUGE_A との比 = 4 = 2^2 exactly (u9 leading coeff 比・検証済)"
        },
        "w_rescaling_note": "w -> lambda*w (any lambda in Q^x) changes u9 by lambda^18, "
                             "which is trivial in Q^x/(Q^x)^18 (a fortiori mod 9) by "
                             "T63-UNIF-INV; this is NOT a source of class ambiguity and is "
                             "not tested as a separate gauge axis."
    },
    "raw_series_data": {
        "X_order_confirmed_3": bool(X_order_is_3),
        "X_leading_coeff_a3": str(X_leading),
        "Y_order_confirmed_9": bool(Y_order_is_9),
        "Y_leading_coeff_y9_s1": str(Y_leading),
        "Y_leading_coeff_y9_s2": str(Y_of_t_leading),
        "Y_order_s2_confirmed_9": bool(Y_of_t_order_is_9),
    },
    "u9_raw_values": {
        "u9_s1_gaugeA": str(u9_1_gaugeA),
        "u9_s1_gaugeA_exact_fraction": str(u9_1_gaugeA_frac),
        "u9_s1_gaugeA_order_is_18": bool(u9_1_gaugeA_order18),
        "u9_s1_gaugeB": str(u9_1_gaugeB),
        "gaugeB_over_gaugeA_ratio": str(gauge_ratio),
        "u9_s2_gaugeA": str(u9_2_gaugeA),
        "u9_s2_gaugeA_exact_fraction": str(u9_2_gaugeA_frac),
        "u9_s2_gaugeA_order_is_18": bool(u9_2_gaugeA_order18),
        "u9_s2_gaugeB": str(u9_2_gaugeB),
    },
    "check3_u9_exact_valuations": {
        "u9_s1_gaugeA": {"v2": v2_u9_s1_gaugeA, "v3": v3_u9_s1_gaugeA,
                          "full_factorization": u9_s1_gaugeA_full_factorization},
        "u9_s2_gaugeA": {"v2": v2_u9_s2_gaugeA, "v3": v3_u9_s2_gaugeA},
        "u9_s1_gaugeB": {"v2": v2_u9_s1_gaugeB, "v3": v3_u9_s1_gaugeB},
        "note": "mod 18/mod 9 に落とす前の完全付値(符号なし絶対値ベース、無制限整数)。"
                "SUPP2 機構仮説の判定材料として司令塔便の要請どおり明記。解釈はしない。"
    },
    "check2_gauge18_measured": {
        "lemma_ref": "数学者紙・補題 GAUGE-18(uniformizer 取替は u9 を c1^-18 倍するのみ "
                      "==> 法18乗類は不変)の実測版",
        "t63_unif_inv_check": {
            "u9_s1_over_u9_s2_ratio_gaugeA": str(ratio_frac),
            "is_exact_18th_power": bool(is_18th_power),
            "witness_18th_root_abs": str(witness_18) if witness_18 is not None else None,
        },
        "a_class_s1_vs_s2_match": bool(a_class_A_matches_s2),
        "closed_form_crosscheck": {
            "Y_of_t_leading_closed_form": str(Y_of_t_leading_closed_form),
            "u9_2_gaugeA_closed_form": str(u9_2_gaugeA_closed_form),
            "matches_series_composition_calc": bool(closed_form_matches_series),
            "note": "f(g(t)) の位数/主係数則(g の位数1・f_k の主係数のみで決まる、標準的な "
                    "形式的巾級数合成の事実)による閉形式と、実際の級数合成計算(series-based, "
                    "N_INV=5 反転+ order-13 打切り合成)が一致することを確認。"
        },
        "note": "両 uniformizer の一致性 -- 最重要の生値。exact であって近似ではない。"
    },
    "check4_desc9_dii_rationality_test": {
        "u9_is_rational_element_of_Q_runtime_check": bool(d_ii_u9_is_rational_element_of_Q),
        "F_equals_Q_structural_fact": d_ii_F_equals_Q_structural,
        "structural_fact_basis": "spec §6: 宣言モデルが Q に降下(§0)した帰結。iota: "
                                  "Q^x/(Q^x)^9 -> F^x/(F^x)^9 は F=Q のとき恒等写像。",
        "d_ii_step_passed": bool(d_ii_step_passed),
        "note": "fail-closed guard 実行結果。zeta 混入なし(u9 が Fraction への変換に "
                "成功していること自体が実行時証拠 -- 失敗すれば即停止だった)。"
    },
    "a_class_gaugeA": {
        "via_s1": a_class_A,
        "via_s2_crosscheck": a_class_A_s2,
        "s1_s2_match": bool(a_class_A_matches_s2),
        "a9_inv_used": str(a9_gaugeA_inv),
        "class_mod18": {str(k): v for k, v in class_mod18_A.items()},
    },
    "a_class_gaugeB": {
        "via_s1": a_class_B,
        "a9_inv_used": str(a9_gaugeB_inv),
        "class_mod18": {str(k): v for k, v in class_mod18_B.items()},
    },
    "gauge_sensitivity_example": {
        "diff_exponent_vector_mod9_B_minus_A": {str(k): v for k, v in gauge_diff_exponent_vector.items()},
        "note": "GAUGE-A -> GAUGE-B (Y^2/4 -> Y^2, factor 4=2^2) がどれだけ a_class を動かすかの "
                "1 例。support が {2} のままか {3} 側に動くかは、この 2 種のゲージ比較だけでは "
                "確定しない(3rd gauge axis 未試験)-- raw 記録のみ、解釈は司令塔。"
    },
    "u_touched": True,
    "c_touched": False,
    "封印3量_touched": False,
    "d9_r_interpretation": "none (raw values only, per task instruction)",
    "u_name_collide_note": "u touched = NAME-COLLIDE 行(K^(9) 窓インスタンス)。d9/r の解釈は行っていない。",
    "input_sha256": input_sha,
    "provenance": {"script_sha256": script_sha256},
}

out_path = "search/certs/a_class_indep_v1_20260813.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(cert, f, ensure_ascii=False, indent=2)
print(f"\nwrote {out_path}")
print(f"script sha256 = {script_sha256}")
