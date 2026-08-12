"""
search/compositum_degree_template_v1.py -- PARAMETRIZED TEMPLATE for compositum-degree computation
(準備 2, 司令塔指示: ISO-S4 が Sol 監査を通れば発火する |A| = [L9 L_S4 : Q] = COMPOSITUM-rho の計算)。

⚠ この段階では L9/L_S4 の実データは一切差し込まない(体の確定は Sol 批准後)。
本ファイルは 2 つの数体(定義多項式で与える)の合成体次数を計算する汎用関数 + canary(既知の
小例)のみを含む。__main__ は canary のみを実行する(実発火は別スクリプトから compositum_degree()
を import して行う想定 -- そのスクリプトは今回作らない)。

METHOD (標準の「終結式 + 原始元」法):
  f(x) = alpha の最小多項式 (次数 m), g(y) = beta の最小多項式 (次数 n)。
  整数 c=1,2,3,... を順に試し, h(z) := Resultant_x( f(x), g(z - c*x) ) を計算。
  alpha,beta の複素根を1つずつ選び theta0 := alpha0 + c*beta0 を数値評価。
  h(z) を QQ 上で因数分解し, theta0 に(数値的に)最も近い根を持つ既約因子を選ぶ
  -- その次数が [Q(alpha,beta):Q] = 合成体次数 (原始元定理: 分離拡大なら一般の c で
  theta=alpha+c*beta が合成体を生成する)。
  collapse_factor := (m*n) / compositum_degree -- 1 なら線形独立(linearly disjoint)、
  >1 ならオーバーラップ(共通部分体がある)の兆候 -- どの部分体かは本テンプレートでは同定しない
  (COMPOSITUM-rho の前件2・3 の判定はこの先, 実データ差し込み後の別作業)。

依拠: sympy (resultant, factor_list, nroots) -- 本キャンペーンの u_meas_caseb_* 系列と同じ道具立て
(search/probe/wac_v1/u_meas_caseb_*.py)。GAP でなく Python/sympy を選んだ理由: 数体の合成次数計算は
終結式+多項式因数分解が本体で、GAP 側に軽量な同等機能がない(本テンプレートは GAP 非使用)。
"""
import json
import sys
from sympy import (symbols, Poly, resultant, factor_list, QQ, nroots, Rational, degree)

x, z = symbols("x z")


def _numeric_roots(poly_expr, var):
    p = Poly(poly_expr, var, domain="QQ")
    return nroots(p.as_expr(), n=40)


def compositum_degree(f_expr, g_expr, var_f=x, var_g=None, c_max=12, verbose=True):
    """
    f_expr: minimal polynomial of alpha, expression in var_f (over QQ).
    g_expr: minimal polynomial of beta, expression in a DIFFERENT symbol than var_f
            (pass as expression in its own symbol; internally renamed).
    Returns a dict (raw data, no interpretation) suitable for JSON serialization.
    """
    y = symbols("y__internal")
    if var_g is None:
        # g_expr is expected to already be in a symbol distinct from var_f; substitute to y
        free = list(g_expr.free_symbols)
        assert len(free) == 1, f"g_expr must be univariate, got {free}"
        var_g = free[0]
    g_expr_y = g_expr.subs(var_g, y)

    f_poly = Poly(f_expr, var_f, domain="QQ")
    g_poly = Poly(g_expr_y, y, domain="QQ")
    m = f_poly.degree()
    n = g_poly.degree()

    alpha_roots = _numeric_roots(f_expr, var_f)
    beta_roots = _numeric_roots(g_expr_y, y)
    alpha0 = alpha_roots[0]
    beta0 = beta_roots[0]

    chosen_c = None
    h_poly_expr = None
    factors = None
    matched_factor_expr = None
    matched_factor_degree = None

    for c in range(1, c_max + 1):
        h = resultant(f_poly.as_expr(), g_expr_y.subs(y, z - c * var_f), var_f)
        h_poly = Poly(h, z, domain="QQ")
        if h_poly.degree() == 0:
            continue
        # squarefree check (generic c should give squarefree h for separable f,g)
        g_h = h_poly.gcd(h_poly.diff())
        disc_sqfree = (g_h.degree() == 0)
        if not disc_sqfree:
            if verbose:
                print(f"[skip] c={c}: h(z) not squarefree, trying next c")
            continue
        theta0 = alpha0 + c * beta0
        content, flist = factor_list(h_poly.as_expr(), z)
        best = None
        best_dist = None
        for fac, mult in flist:
            fac_poly = Poly(fac, z, domain="QQ")
            for r in nroots(fac_poly.as_expr(), n=40):
                dist = abs(complex(r) - complex(theta0))
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    best = fac_poly
        if best is None:
            continue
        chosen_c = c
        h_poly_expr = h_poly.as_expr()
        factors = [(str(fac), mult, Poly(fac, z, domain="QQ").degree()) for fac, mult in flist]
        matched_factor_expr = best.as_expr()
        matched_factor_degree = best.degree()
        if verbose:
            print(f"[c={c}] h(z) degree={h_poly.degree()} squarefree=True "
                  f"matched_factor_degree={matched_factor_degree} (closest root dist={best_dist:.2e})")
        break

    if chosen_c is None:
        raise RuntimeError(f"no working c found in range 1..{c_max} (all gave non-squarefree resultants)")

    compositum_deg = matched_factor_degree
    product_mn = m * n
    collapse_factor = Rational(product_mn, compositum_deg)

    return {
        "input": {
            "field1_min_poly": str(f_expr), "field1_degree": m,
            "field2_min_poly": str(g_expr_y.subs(y, var_g)), "field2_degree": n,
        },
        "method": "resultant_primitive_element",
        "primitive_element_c": chosen_c,
        "resultant_poly_degree": m * n,
        "resultant_factorization": factors,
        "matched_factor_min_poly": str(matched_factor_expr),
        "compositum_degree": compositum_deg,
        "product_of_degrees": product_mn,
        "collapse_factor": str(collapse_factor),
        "linearly_disjoint": (collapse_factor == 1),
    }


def build_cert(canary_name, result, expected_degree=None):
    rec = {
        "schema": "compositum-degree/v1-template",
        "generated_by": {"tool": "python/sympy", "script": "search/compositum_degree_template_v1.py",
                          "task": "準備2(司令塔指示・待機解除メッセージ)ISO-S4 COMPOSITUM-rho 発火用の雛形"},
        "canary": True,
        "canary_name": canary_name,
        "real_data_used": False,
        "result": result,
    }
    if expected_degree is not None:
        rec["expected_degree_hand_check"] = expected_degree
        rec["agrees_with_hand_check"] = (result["compositum_degree"] == expected_degree)
    return rec


def main():
    certs = []

    # ---- Canary A: Q(zeta_12) x Q(2^(1/3)) -- coprime degrees (4,3), expect linearly disjoint, deg 12
    zeta12_poly = x**4 - x**2 + 1          # min poly of a primitive 12th root of unity, degree phi(12)=4
    cbrt2_var = symbols("w")
    cbrt2_poly = cbrt2_var**3 - 2           # degree 3
    resA = compositum_degree(zeta12_poly, cbrt2_poly, var_f=x, var_g=cbrt2_var)
    certA = build_cert("Q(zeta_12) x Q(cbrt(2))", resA, expected_degree=12)
    certs.append(certA)
    print("Canary A:", "PASS" if certA["agrees_with_hand_check"] else "FAIL",
          "compositum_degree =", resA["compositum_degree"], "(expect 12)")

    # ---- Canary B: [Q(zeta_12,cbrt2)] x Q(i) -- Q(i) subset Q(zeta_12) already, expect COLLAPSE to 12
    deg12_min_poly_expr = zeta12_poly if False else None
    # use canary A's matched primitive-element minimal polynomial as field1 for canary B
    from sympy import sympify
    deg12_min_poly = sympify(resA["matched_factor_min_poly"])
    # matched_factor_min_poly is in variable z (from the resultant construction) -- rename to x
    deg12_min_poly = deg12_min_poly.subs(z, x)
    i_var = symbols("v")
    i_poly = i_var**2 + 1                   # min poly of i, degree 2
    resB = compositum_degree(deg12_min_poly, i_poly, var_f=x, var_g=i_var)
    certB = build_cert("Q(zeta_12,cbrt2) x Q(i) [Q(i) subset Q(zeta_12) already]", resB, expected_degree=12)
    certs.append(certB)
    print("Canary B:", "PASS" if certB["agrees_with_hand_check"] else "FAIL",
          "compositum_degree =", resB["compositum_degree"], "(expect 12, collapse_factor=2)")

    # ---- Canary C: Q(sqrt2) x Q(sqrt3) -- independent quadratics, expect deg 4
    s2_var = symbols("p")
    s3_var = symbols("q")
    s2_poly = s2_var**2 - 2
    s3_poly = s3_var**2 - 3
    resC = compositum_degree(s2_poly, s3_poly, var_f=s2_var, var_g=s3_var)
    certC = build_cert("Q(sqrt2) x Q(sqrt3)", resC, expected_degree=4)
    certs.append(certC)
    print("Canary C:", "PASS" if certC["agrees_with_hand_check"] else "FAIL",
          "compositum_degree =", resC["compositum_degree"], "(expect 4)")

    out = {"schema": "compositum-degree/v1-template-canary-batch", "canaries": certs,
           "all_pass": all(c["agrees_with_hand_check"] for c in certs)}
    with open("search/certs/compositum_degree_template_canary_20260812.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("\nwrote search/certs/compositum_degree_template_canary_20260812.json  all_pass =", out["all_pass"])
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
