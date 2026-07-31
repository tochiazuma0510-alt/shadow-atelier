#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
u3_calib_v1.py -- u 測定装置(n=3 較正走)
司令塔委嘱(2026-08-01): docs/notes/u7_meas_design_v1.md 較正節(§8 CAL-7)の
仕様どおりに n=3 窓の厳密モデル構成 -> cusp/parameter 規約 -> u3 抽出を実走し、
既知値 u3 = -4 (公開・manifest_k5_appendixA_v1.md SS2) を再現するかを機械判定する。

正典の出発点: search/week4-u-k3.mjs の LMFDB 6T9-a 平面モデル
  F(x,t) = t^2 + (x-1)^2(4x-1) t + 4x^6 = 0,  lambda := -t
  (0,1,infty) 上で型 (6, 2^2 1^2, 6)。P0 = (x,t)=(0,0) は lambda=0 上の唯一の点(全分岐 e=6)。

本スクリプトが新規に実行するのは、この正典モデル上で
 定理 TOWER-3 (塔 W_3 -deg3-> V=P^1_m -deg2-> P^1_lambda, lambda=gamma*m^2) が
 具体的に実現するかどうかの構成的検証、および
 系 SPLIT (u_n = gamma * c^2, m = c*tau^n + ... at P0, tau=x) による u_3 の抽出。

方針(§8.2 の手続きに対応):
 1. 厳密モデル構成: F(x,t)=0 の関数体 Q(x)[t]/(F) の中に、次数3の元 m を
    m^2 = c0 * t (c0 は有理定数) という代数的識別式で探す(ansatz m=p(x)+q(x)t、
    p=2x^3 q の形を要求すると q^2*(4x^3 - A(x)) = c0 が出て、
    4x^3-A(x) が完全平方 (3x-1)^2 になることを利用)。
    見つかった m が実際に厳密恒等式 m^2 = t (gamma=-1 の代表元) を満たすかを
    多項式展開で機械確認する(mod F ではなく整式として一致するかを見る = 剛性)。
 2. cusp/parameter 規約: tau = x (P0 での正準・有理一意化変数、既存の週4 較正で
    確立済みの規約をそのまま流用)。m の x 級数展開の先頭項 m = c_loc * x^3 + ... を抽出。
 3. u3 抽出: gamma (m^2=t の比例定数の逆符号) と c_loc から u3 = gamma * c_loc^2 を計算し、
    既知値 -4 と一致するかを bool 判定。
 4. 副検査 UB-GEOM (§4.2 / §8.2 手順3): lambda=1 (t=-1) 上の非分岐 2 点(1,1 型)が
    個別に F_3 = Q(zeta_12) 有理であるかを確認する( [gamma]_2=1 の幾何側 cross-check、
    helper 非共有)。

宇宙: n=3 のみ。TOWER-n は n=3 でも成立するので使用(委嘱どおり)。u7 には一切触れない。
演算はすべて sympy の厳密有理・代数演算(浮動小数点不使用)。
"""
import json
import hashlib
import datetime
import sys
import sympy as sp

REPORT = {"ok_all": True, "checks": []}


def check(name, cond, detail=None):
    REPORT["checks"].append({"name": name, "pass": bool(cond), "detail": detail})
    if not cond:
        REPORT["ok_all"] = False
    print(f"{'PASS' if cond else '*** FAIL'}  {name}" + (f"  :: {detail}" if detail else ""))


x, t = sp.symbols('x t')

# ---- 0. 正典モデル -----------------------------------------------------
A = (x - 1)**2 * (4 * x - 1)
F = sp.expand(t**2 + A * t + 4 * x**6)
check("(0) F(x,t) = t^2 + (x-1)^2(4x-1) t + 4x^6 の構成",
      sp.expand(F - (t**2 + A * t + 4 * x**6)) == 0)

A_expand = sp.expand(A)
check("(0b) A(x) = 4x^3 - 9x^2 + 6x - 1", sp.expand(A_expand - (4*x**3 - 9*x**2 + 6*x - 1)) == 0,
      str(A_expand))

# ---- 1. 塔の中間関数 m の構成的発見 -------------------------------------
# ansatz: m = p(x) + q(x) t,  p = 2 x^3 q  (m^2 の t^0 成分を消すための唯一の比)
# m^2 = p^2 + 2pq t + q^2 t^2, かつ t^2 = -A t - 4x^6 (F=0 の関係式)
#   => m^2 = (p^2 - 4x^6 q^2) + (2pq - A q^2) t
# p^2 - 4x^6 q^2 = (2x^3 q)^2 - 4x^6 q^2 = 0  (恒等的に 0、任意の q で)
# 2pq - A q^2 = q^2 (4x^3 - A) = q^2 (3x-1)^2   [4x^3 - A = (3x-1)^2 を利用]
p_over_q = 2 * x**3
four_x3_minus_A = sp.expand(4 * x**3 - A_expand)
check("(1a) 4x^3 - A(x) = (3x-1)^2 (完全平方 -- q が有理関数になるための必要条件)",
      sp.expand(four_x3_minus_A - (3*x - 1)**2) == 0, str(four_x3_minus_A))

# k=1 (ゲージ固定): q = 1/(3x-1), p = 2x^3/(3x-1)
q_expr = 1 / (3 * x - 1)
p_expr = p_over_q * q_expr
m_expr = sp.together(p_expr + q_expr * t)  # m = (2x^3 + t) / (3x-1)
check("(1b) m := (2x^3 + t) / (3x - 1) の構成", sp.simplify(m_expr - (2*x**3 + t) / (3*x - 1)) == 0,
      str(m_expr))

# ---- 2. 厳密恒等式チェック: m^2 = t が F=0 と多項式として同値であること -------
# (2x^3+t)^2 - (3x-1)^2 t を展開すると F(x,t) にちょうど一致するはず(剛性 = ゲージ非依存の厳密等式)
identity_lhs = sp.expand((2 * x**3 + t)**2 - (3 * x - 1)**2 * t)
check("(2) 厳密恒等式: (2x^3+t)^2 - (3x-1)^2 t == F(x,t)  (多項式として完全一致、mod F ではない)",
      sp.expand(identity_lhs - F) == 0,
      f"identity_lhs - F = {sp.expand(identity_lhs - F)}")

# これは m^2 = t が曲線上で恒等的に成り立つことを意味する(gamma = -1 の代表元、
# lambda = -t = -m^2 = gamma * m^2 with gamma = -1 exactly)。
gamma_exact = sp.Integer(-1)
check("(2b) ゆえに m^2 = t (恒等的) ⇒ lambda = -t = gamma * m^2, gamma = -1 (厳密値・k=1 ゲージ)",
      True, f"gamma = {gamma_exact}")

# ---- 3. cusp P0 での局所展開(tau = x、既存較正で確立済みの正準一意化変数) -------
# t(x) を F(x,t)=0, t=O(x^6) の分岐で級数展開 (2次方程式を厳密に解いて sqrt を級数展開)
N = 24  # 級数次数(3 で割った後も十分な余裕を持たせる)
D = sp.expand(A_expand**2 - 16 * x**6)
sqrtD_series = sp.series(sp.sqrt(D), x, 0, N).removeO()
t_small = sp.series(sp.expand((-A_expand - sqrtD_series) / 2), x, 0, N).removeO()
t_small = sp.expand(t_small)

# 検算: F(x, t_small) が x^(N-2) の精度でゼロに一致するか(mod x^N)
resid = sp.series(sp.expand(t_small**2 + A_expand * t_small + 4 * x**6), x, 0, N - 2)
check("(3a) t(x) 級数解が F(x,t)=0 を満たす(mod x^{})".format(N - 2),
      sp.expand(resid.removeO()) == 0, str(resid))

t_poly = sp.Poly(t_small, x)
lead_t = None
for deg in range(0, N):
    c = t_poly.coeff_monomial(x**deg) if deg > 0 else t_poly.coeff_monomial(1)
    if c != 0:
        lead_t = (deg, c)
        break
check("(3b) t = 4x^6 + O(x^7) (P0 での正準一意化変数 x による既存較正 week4-u-k3.mjs と一致)",
      lead_t is not None and lead_t[0] == 6 and lead_t[1] == 4, str(lead_t))

# m の級数展開: m = (2x^3+t)/(3x-1)
m_series_expr = (2 * x**3 + t_small) / (3 * x - 1)
m_series = sp.series(m_series_expr, x, 0, N - 6).removeO()
m_series = sp.expand(m_series)
m_poly = sp.Poly(m_series, x)
lead_m = None
for deg in range(0, N - 6):
    c = m_poly.coeff_monomial(x**deg) if deg > 0 else m_poly.coeff_monomial(1)
    if c != 0:
        lead_m = (deg, c)
        break
check("(3c) m = c_loc * x^3 + O(x^4) (deg=3 の全分岐、定理 TOWER-3(3) の局所型 (n)=(3) と整合)",
      lead_m is not None and lead_m[0] == 3, str(lead_m))

c_loc = lead_m[1] if lead_m else None
check("(3d) c_loc = -2 (機械抽出値)", c_loc == sp.Integer(-2), str(c_loc))

# m^2 の級数が t の級数と厳密一致するか(局所展開レベルでも恒等式 m^2=t を再確認)
m2_series = sp.series(m_series_expr**2, x, 0, N - 6).removeO()
check("(3e) m^2 の級数展開が t の級数展開と一致(局所レベルでの恒等式再確認)",
      sp.expand(m2_series - t_small) == 0 or sp.series(sp.expand(m2_series - t_small), x, 0, N - 6).removeO() == 0)

# ---- 4. u3 = gamma * c_loc^2 の抽出 と 既知値 -4 との突合 --------------------
u3_extracted = gamma_exact * c_loc**2
u3_known = sp.Integer(-4)
u3_match = (u3_extracted == u3_known)
check("(4) ★★ u3 = gamma * c_loc^2 = -1 * (-2)^2 = -4  (既知値 u3=-4 と一致)",
      u3_match, f"u3_extracted = {u3_extracted}, u3_known = {u3_known}")

# ---- 5. 副検査 UB-GEOM: lambda=1 (t=-1) の非分岐 2 点の F_3-有理性 -----------
# F(x,-1) を因数分解し、(2x^2-2x+1)^2 * (残り次数2) の形になるはず(既知の分岐点 x=(1+-i)/2 由来)
F_at_m1 = sp.expand(F.subs(t, -1))
ramified_factor = sp.expand((2 * x**2 - 2 * x + 1)**2)
quotient, remainder = sp.div(sp.Poly(F_at_m1, x), sp.Poly(ramified_factor, x))
check("(5a) F(x,-1) = (2x^2-2x+1)^2 * q(x), 余り0 (分岐部分の分離)",
      remainder == 0, f"quotient={quotient.as_expr()}, remainder={remainder}")

unramified_poly = quotient.as_expr()
check("(5b) 非分岐 2 点の定義方程式 q(x) = x^2+2x+2", sp.expand(unramified_poly - (x**2 + 2*x + 2)) == 0,
      str(unramified_poly))

roots = sp.solve(sp.Eq(unramified_poly, 0), x)
roots_in_F3 = []
I = sp.I
for r in roots:
    r_simpl = sp.simplify(r)
    # F_3 = Q(zeta_12) = Q(i, sqrt(3)) 上の有理性: a + b*I の形 (a,b in Q) であれば
    # 個別に Q(i) subset F_3 上有理
    re_part = sp.re(r_simpl) if r_simpl.is_number else sp.simplify(sp.expand(r_simpl - I * sp.im(r_simpl)))
    im_coeff = sp.simplify((r_simpl - re_part) / I) if r_simpl.is_number else None
    is_qi_rational = re_part.is_rational and (im_coeff is None or im_coeff.is_rational)
    roots_in_F3.append({"root": str(r_simpl), "re": str(re_part), "im_coeff": str(im_coeff),
                         "individually_F3_rational": bool(is_qi_rational)})

check("(5c) UB-GEOM: 2 個の非分岐点 x=-1+-i が個別に Q(i) subset F_3 有理 (交換で入れ替わらない)",
      all(r["individually_F3_rational"] for r in roots_in_F3), json.dumps(roots_in_F3, ensure_ascii=False))

gamma_is_square_in_F3 = True  # gamma=-1=i^2, i in F_3=Q(zeta_12) は既知(週4/i23 等で確立済みの事実を援用)
check("(5d) [gamma]_2 = [-1]_2 = 1 in F_3 (i=zeta_12^3 in F_3 ゆえ -1=i^2) -- UB-GEOM の予測と整合",
      gamma_is_square_in_F3)

# ---- 6. 総合判定 --------------------------------------------------------
CAL7_PASS = bool(REPORT["ok_all"]) and u3_match
print(f"\n==== {'CAL-7 PASS' if CAL7_PASS else 'CAL-7 FAIL'} "
      f"({sum(1 for c in REPORT['checks'] if c['pass'])}/{len(REPORT['checks'])} checks) ====")

# ---- cert 出力 -----------------------------------------------------------
src = open(__file__, 'rb').read()
script_sha256 = hashlib.sha256(src).hexdigest()

cert = {
    "schema": "u3-calib/v1",
    "generated_by": {"tool": "python3+sympy", "sympy_version": sp.__version__,
                      "script": "search/probe/wac_v1/u3_calib_v1.py"},
    "purpose": "u7 測定装置(n=7 転用設計 docs/notes/u7_meas_design_v1.md)の CAL-7 較正走"
               "(n=3 窓・deg6・genus1・既知値 u3=-4 との突合・較正ゲート = 接触遮断の例外)",
    "universe": {"n": 3, "note": "u7 に一切接触していない。K^(5) 非接触。"},
    "model": {
        "plane_model": "F(x,t) = t^2 + (x-1)^2(4x-1) t + 4x^6 = 0  (LMFDB 6T9-a, "
                        "search/week4-u-k3.mjs と同一の正典モデル)",
        "lambda_assignment": "lambda := -t",
        "cusp_P0": "(x,t) = (0,0), lambda=0 上の唯一の全分岐点 (e=6)",
        "canonical_uniformizer_tau": "x",
    },
    "tower_construction": {
        "method": "ansatz m = p(x)+q(x)t with p=2x^3 q, solved via 4x^3-A(x)=(3x-1)^2",
        "m_formula": "m = (2x^3 + t) / (3x - 1)   (gauge k=1)",
        "exact_identity": "(2x^3+t)^2 - (3x-1)^2 t == F(x,t)  [polynomial identity, verified]",
        "consequence": "lambda = -t = -m^2 = gamma*m^2 with gamma = -1 EXACTLY (not just mod squares)",
        "gamma": "-1",
        "divisor_of_m": "3*P0 - 3*P_infty (deg 3, matches TOWER-3 local type (n)=(3) at P0,P_infty)",
    },
    "local_expansion_at_P0": {
        "t_series_leading": "t = 4*x^6 + O(x^7)",
        "m_series_leading": "m = c_loc * x^3 + O(x^4), c_loc = -2",
        "u3_extraction_formula": "u3 = gamma * c_loc^2  (系 SPLIT)",
    },
    "u3_extracted": str(u3_extracted),
    "u3_known_public_value": str(u3_known),
    "u3_reproduced": u3_match,
    "ub_geom_secondary_check": {
        "unramified_points_over_lambda1": roots_in_F3,
        "individually_F3_rational": all(r["individually_F3_rational"] for r in roots_in_F3),
        "predicted_by_design_doc": "[u3]_2=1 <=> 2 非分岐点が個別に F_3-有理 (docs/notes/u7_meas_design_v1.md L254-256)",
    },
    "checks": REPORT["checks"],
    "overall_pass": CAL7_PASS,
    "verdict": "CAL-7 PASS (装置較正成功・本番 gate 通過可)" if CAL7_PASS
               else "CAL-7 FAIL (fail-closed・修理は司令塔判断・本番を発火させない)",
    "caveats": [
        "単系統(sympy 厳密演算)。cross-checked ではない。Lean 検証ではない。",
        "本証明書は n=3 のみに関する較正結果。u7 の値・予想には一切触れていない。",
        "\\tilde W (Galois 閉包)/B の明示構成は経由していない -- m を直接 ansatz で発見し"
        "厳密恒等式で正当化する近道を取った(結果は KUM-3/系 SPLIT の予言と完全一致)。",
    ],
    "generated_at_utc": datetime.datetime.utcnow().isoformat() + "Z",
    "provenance": {"script_sha256": script_sha256},
}

out_path = "search/certs/u3_calib_20260801.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(cert, f, ensure_ascii=False, indent=2)
print(f"\ncert written: {out_path}")

sys.exit(0 if CAL7_PASS else 1)
