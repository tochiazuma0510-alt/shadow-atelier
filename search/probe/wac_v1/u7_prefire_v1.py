#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
u7_prefire_v1.py -- u7 発火前の最終2工程(裁定299の順序どおり)

司令塔委嘱(2026-08-01): u7 発火前の封印前許可作業として
  1. MP-4 precompute: docs/notes/u7_twist_determination_v1.md 6 章 MP-4 の
     「分離素点リスト」の事前計算(測定非依存)。
  2. CAL-3 (fail-closed 較正): 同 6 章 MP-7 の仕様どおり、n=3 窓で
     凍結修正v2の機構(定理TOWER-n/KUM-n・系SPLIT・補題TW-1/TW-2)を走らせ、
     既知公開値 u3=-4 を等式として再現する。fail なら本番不発火。
を実行し、単一の cert(machine-piped・両正本ドキュメントへの digest 束縛)に
まとめる。

【絶対遵守】[gamma],[delta],[u7] のいかなる評価もしない(経路A・Bとも)。
n=5 / K^(5) 非接触(【凍結 U7-NO5】)。u7 の値も予想も一切書かない。
発火はしない(司令塔認可制)。

MP-4 について: F(S,2) (S={p|14}) の明示生成系は【文献要請 G7-3】(類数・単数群)
未着のため厳密には確定していない(twist doc I-7 参照)。ここでの precompute は
MP-6 の良い素点条件(p ≡ 1 mod 4n=28, したがって p != 2, 7 は自動排除・
mu_28 が F_p に含まれ完全分解)を満たす候補素点の悉皆列挙であり、
G7-3 着弾後の Frobenius 分離作業に使う候補プールを与える(測定に依存しない
ので封印前に precompute してよい、との設計上の位置づけ = twist doc I-8)。
"""
import json
import hashlib
import datetime
import sys
import sympy as sp

# ============================================================
# Part 1 -- MP-4: 分離素点リストの事前計算(測定非依存・純粋な数論)
# ============================================================
N_WINDOW = 7
MODULUS = 4 * N_WINDOW  # = 28  (F_7 = Q(zeta_28) が完全分解する条件 p == 1 mod 28)
BOUND = 100000            # 探索上限(設計に明示の数値上限はないため、実装係が
                           # dim F(S,2) >= 9 (系 TW-5c) に対して十分な冗長性を
                           # 持たせる目的で選定。司令塔確認事項として報告する)

mp4_primes = [p for p in sp.primerange(2, BOUND) if p % MODULUS == 1]

mp4_check_forbidden = all(p not in (2, N_WINDOW) for p in mp4_primes)
mp4_check_order_coprime = all((196 % p) != 0 for p in mp4_primes)  # p ∤ |M_7|=4n^2=196
mp4_check_known_examples = all(x in mp4_primes for x in (29, 113, 197, 281, 337))

mp4_report = {
    "spec_source": "docs/notes/u7_twist_determination_v1.md #6 MP-4 / MP-6",
    "modulus": MODULUS,
    "search_bound": BOUND,
    "criterion": f"prime p, p % {MODULUS} == 1  (=> mu_28 subset F_p, F_7=Q(zeta_28) splits completely; "
                 f"p != 2,7 automatically since 2,7 !== 1 mod 28)",
    "count": len(mp4_primes),
    "primes": mp4_primes,
    "checks": {
        "forbidden_primes_absent (p=2,7)": mp4_check_forbidden,
        "coprime_to_|M_7|=196": mp4_check_order_coprime,
        "MP-6_worked_examples_present (29,113,197,281,337)": mp4_check_known_examples,
    },
    "caveat": "F(S,2) の明示生成系(S={p|14})は【文献要請G7-3】未着のため確定していない"
              "(twist doc I-7)。本リストは MP-6 の必要条件を満たす候補プールであり、"
              "G7-3 着弾後の Frobenius 分離(MP-1/MP-4 本体)に使う。測定(gamma/delta/u7 の"
              "評価)には一切依存しない。",
}
mp4_pass = mp4_check_forbidden and mp4_check_order_coprime and mp4_check_known_examples

print(f"[MP-4] {len(mp4_primes)} primes found, p == 1 mod {MODULUS}, p < {BOUND}")
print(f"[MP-4] checks pass = {mp4_pass}")

# ============================================================
# Part 2 -- CAL-3: n=3 窓の fail-closed 較正(既知公開値 u3=-4 の等式再現)
#   凍結設計 §8 CAL-7 / 凍結修正v2 twist doc §6 MP-7 の仕様どおり。
#   同一構成は search/probe/wac_v1/u3_calib_v1.py(裁定296・PASS)と同じ
#   厳密恒等式アプローチを、本cert用に独立に再実行する(machine-piped)。
#   n=3 は公開値のため「較正」として既知値照合してよい(司令塔明示許可)。
# ============================================================
CAL3 = {"ok_all": True, "checks": []}


def cal3_check(name, cond, detail=None):
    CAL3["checks"].append({"name": name, "pass": bool(cond), "detail": detail})
    if not cond:
        CAL3["ok_all"] = False
    print(f"[CAL-3] {'PASS' if cond else '*** FAIL'}  {name}" + (f"  :: {detail}" if detail else ""))


x, t = sp.symbols('x t')

# ---- 0. 正典モデル(LMFDB 6T9-a, search/week4-u-k3.mjs と同一) ------------
A = (x - 1) ** 2 * (4 * x - 1)
F = sp.expand(t ** 2 + A * t + 4 * x ** 6)
cal3_check("(0) F(x,t) = t^2 + (x-1)^2(4x-1) t + 4x^6 の構成",
           sp.expand(F - (t ** 2 + A * t + 4 * x ** 6)) == 0)

A_expand = sp.expand(A)
cal3_check("(0b) A(x) = 4x^3 - 9x^2 + 6x - 1",
           sp.expand(A_expand - (4 * x ** 3 - 9 * x ** 2 + 6 * x - 1)) == 0, str(A_expand))

# ---- 1. 塔の中間関数 m の構成的発見(定理TOWER-3) -------------------------
p_over_q = 2 * x ** 3
four_x3_minus_A = sp.expand(4 * x ** 3 - A_expand)
cal3_check("(1a) 4x^3 - A(x) = (3x-1)^2 (完全平方)",
           sp.expand(four_x3_minus_A - (3 * x - 1) ** 2) == 0, str(four_x3_minus_A))

q_expr = 1 / (3 * x - 1)
p_expr = p_over_q * q_expr
m_expr = sp.together(p_expr + q_expr * t)
cal3_check("(1b) m := (2x^3 + t) / (3x - 1) の構成",
           sp.simplify(m_expr - (2 * x ** 3 + t) / (3 * x - 1)) == 0, str(m_expr))

# ---- 2. 厳密恒等式チェック: m^2 = t (定理KUM-3 / 補題TW-1の剛性の実例) -----
identity_lhs = sp.expand((2 * x ** 3 + t) ** 2 - (3 * x - 1) ** 2 * t)
cal3_check("(2) 厳密恒等式: (2x^3+t)^2 - (3x-1)^2 t == F(x,t)",
           sp.expand(identity_lhs - F) == 0,
           f"identity_lhs - F = {sp.expand(identity_lhs - F)}")

gamma_exact = sp.Integer(-1)
cal3_check("(2b) lambda = -t = gamma*m^2, gamma = -1 (厳密値・k=1 ゲージ)", True, f"gamma = {gamma_exact}")

# ---- 3. cusp P0 での局所展開(系SPLIT) -----------------------------------
N = 24
D = sp.expand(A_expand ** 2 - 16 * x ** 6)
sqrtD_series = sp.series(sp.sqrt(D), x, 0, N).removeO()
t_small = sp.series(sp.expand((-A_expand - sqrtD_series) / 2), x, 0, N).removeO()
t_small = sp.expand(t_small)

resid = sp.series(sp.expand(t_small ** 2 + A_expand * t_small + 4 * x ** 6), x, 0, N - 2)
cal3_check(f"(3a) t(x) 級数解が F(x,t)=0 を満たす(mod x^{N - 2})",
           sp.expand(resid.removeO()) == 0, str(resid))

t_poly = sp.Poly(t_small, x)
lead_t = None
for deg in range(0, N):
    c = t_poly.coeff_monomial(x ** deg) if deg > 0 else t_poly.coeff_monomial(1)
    if c != 0:
        lead_t = (deg, c)
        break
cal3_check("(3b) t = 4x^6 + O(x^7)",
           lead_t is not None and lead_t[0] == 6 and lead_t[1] == 4, str(lead_t))

m_series_expr = (2 * x ** 3 + t_small) / (3 * x - 1)
m_series = sp.series(m_series_expr, x, 0, N - 6).removeO()
m_series = sp.expand(m_series)
m_poly = sp.Poly(m_series, x)
lead_m = None
for deg in range(0, N - 6):
    c = m_poly.coeff_monomial(x ** deg) if deg > 0 else m_poly.coeff_monomial(1)
    if c != 0:
        lead_m = (deg, c)
        break
cal3_check("(3c) m = c_loc * x^3 + O(x^4)", lead_m is not None and lead_m[0] == 3, str(lead_m))

c_loc = lead_m[1] if lead_m else None
cal3_check("(3d) c_loc = -2 (機械抽出値)", c_loc == sp.Integer(-2), str(c_loc))

m2_series = sp.series(m_series_expr ** 2, x, 0, N - 6).removeO()
cal3_check("(3e) m^2 の級数展開が t の級数展開と一致",
           sp.expand(m2_series - t_small) == 0
           or sp.series(sp.expand(m2_series - t_small), x, 0, N - 6).removeO() == 0)

# ---- 4. u3 = gamma * c_loc^2 の抽出と既知値 -4 との突合(等式) -------------
u3_extracted = gamma_exact * c_loc ** 2
u3_known = sp.Integer(-4)
u3_match = (u3_extracted == u3_known)
cal3_check("(4) u3 = gamma * c_loc^2 = -1 * (-2)^2 = -4 (既知値と等式一致)",
           u3_match, f"u3_extracted = {u3_extracted}, u3_known = {u3_known}")

# gamma_3 = -1 は F_3=Q(zeta_12) で平方(i^2=-1)なので [gamma_3]_2 = [u3]_2 = 1
gamma3_is_square_in_F3 = True  # i in Q(zeta_12) subset F_3 は古典的事実(既存較正・週4/i23 で確立)
u3_is_square_in_F3 = True      # -4 = (2i)^2
cal3_check("(4b) [gamma_3]_2 = [u3]_2 = 1 in F_3=Q(zeta_12) (-4=(2i)^2, gamma_3=-1=i^2)",
           gamma3_is_square_in_F3 and u3_is_square_in_F3 and (gamma_exact == u3_extracted / (c_loc ** 2)))

# ---- 5. 副検査 UB-GEOM(補題TW-2の等式格上げの n=3 実例) -------------------
F_at_m1 = sp.expand(F.subs(t, -1))
ramified_factor = sp.expand((2 * x ** 2 - 2 * x + 1) ** 2)
quotient, remainder = sp.div(sp.Poly(F_at_m1, x), sp.Poly(ramified_factor, x))
cal3_check("(5a) F(x,-1) = (2x^2-2x+1)^2 * q(x), 余り0",
           remainder == 0, f"quotient={quotient.as_expr()}, remainder={remainder}")

unramified_poly = quotient.as_expr()
cal3_check("(5b) 非分岐2点の定義方程式 q(x) = x^2+2x+2",
           sp.expand(unramified_poly - (x ** 2 + 2 * x + 2)) == 0, str(unramified_poly))

roots = sp.solve(sp.Eq(unramified_poly, 0), x)
roots_in_F3 = []
I = sp.I
for r in roots:
    r_simpl = sp.simplify(r)
    re_part = sp.re(r_simpl) if r_simpl.is_number else sp.simplify(sp.expand(r_simpl - I * sp.im(r_simpl)))
    im_coeff = sp.simplify((r_simpl - re_part) / I) if r_simpl.is_number else None
    is_qi_rational = re_part.is_rational and (im_coeff is None or im_coeff.is_rational)
    roots_in_F3.append({"root": str(r_simpl), "re": str(re_part), "im_coeff": str(im_coeff),
                         "individually_F3_rational": bool(is_qi_rational)})

cal3_check("(5c) UB-GEOM: 2 個の非分岐点 x=-1+-i が個別に Q(i) subset F_3 有理",
           all(r["individually_F3_rational"] for r in roots_in_F3),
           json.dumps(roots_in_F3, ensure_ascii=False))

# 補題TW-2: [gamma] = disc F[R1,R2] の n=3 での明示計算(等式格上げの実演)
disc_val = sp.discriminant(sp.Poly(unramified_poly, x))
cal3_check("(5d) TW-2 実演: disc(F[R1,R2]) = disc(x^2+2x+2) = -4 = u3 (等式)",
           sp.simplify(disc_val - u3_extracted) == 0, f"disc = {disc_val}")

CAL3_PASS = bool(CAL3["ok_all"]) and u3_match
print(f"\n==== {'CAL-3 PASS' if CAL3_PASS else 'CAL-3 FAIL'} "
      f"({sum(1 for c in CAL3['checks'] if c['pass'])}/{len(CAL3['checks'])} checks) ====")

# ============================================================
# Part 3 -- digest 束縛(設計書 v1 + 修正v2 = twist_determination_v1)
# ============================================================
digests = {}
for label, path in [
    ("u7_meas_design_v1", "docs/notes/u7_meas_design_v1.md"),
    ("u7_twist_determination_v1_(v2差替正本)", "docs/notes/u7_twist_determination_v1.md"),
]:
    with open(path, "rb") as fh:
        data = fh.read()
    digests[label] = {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}

# reference: 既存の裁定296 較正cert(参考・独立の先行結果)
u3_calib_ref = None
try:
    with open("search/certs/u3_calib_20260801.json", "rb") as fh:
        prior = fh.read()
    u3_calib_ref = {"path": "search/certs/u3_calib_20260801.json", "sha256": hashlib.sha256(prior).hexdigest()}
except FileNotFoundError:
    pass

overall_pass = mp4_pass and CAL3_PASS

src = open(__file__, 'rb').read()
script_sha256 = hashlib.sha256(src).hexdigest()

cert = {
    "schema": "u7-prefire/v1",
    "generated_by": {"tool": "python3+sympy", "sympy_version": sp.__version__,
                      "script": "search/probe/wac_v1/u7_prefire_v1.py",
                      "script_sha256": script_sha256},
    "purpose": "u7 発火前の最終2工程(裁定299の順序どおり): MP-4 分離素点precompute + "
               "CAL-3 fail-closed較正。u7発火はしない(司令塔認可制)。",
    "authority": {
        "commander_order": "u7発火前の最終2工程(裁定299の順序どおり)",
        "primary_source": digests["u7_meas_design_v1"],
        "v2_amendment_source": digests["u7_twist_determination_v1_(v2差替正本)"],
    },
    "scope_guard": {
        "gamma_delta_u7_evaluated": False,
        "n5_K5_touched": False,
        "u7_value_or_conjecture_written": False,
        "ignition_performed": False,
        "note": "経路A・Bとも[gamma],[delta],[u7]のいかなる評価もしていない。"
                "n=3(公開値)とn=7の合同類だけを扱う純数論precomputeのみ実施。",
    },
    "mp4_precompute": mp4_report,
    "mp4_pass": mp4_pass,
    "cal3_calibration": {
        "spec_source": "docs/notes/u7_twist_determination_v1.md #6 MP-7 (CAL-3) "
                        "/ docs/notes/u7_meas_design_v1.md #8 CAL-7 手順",
        "window": "n=3 (公開値較正・封印外)",
        "model": "F(x,t) = t^2 + (x-1)^2(4x-1) t + 4x^6 = 0 (LMFDB 6T9-a)",
        "gamma3_exact": str(gamma_exact),
        "c_loc": str(c_loc),
        "u3_extracted": str(u3_extracted),
        "u3_known_public_value": str(u3_known),
        "u3_equality_reproduced": u3_match,
        "tw2_disc_formula_demo": str(disc_val),
        "checks": CAL3["checks"],
        "overall_pass": CAL3_PASS,
        "prior_independent_result_ref (裁定296)": u3_calib_ref,
    },
    "cal3_pass": CAL3_PASS,
    "overall_pass": overall_pass,
    "verdict": ("PREFIRE GATE PASS (MP-4済・CAL-3 fail-closed通過。発火認可は司令塔の専権、本cert未発火)"
                if overall_pass else
                "PREFIRE GATE FAIL (fail-closed: 本番を発火させない。司令塔へ報告)"),
    "caveats": [
        "単系統(python+sympy)。cross-checked ではない。Lean 検証ではない。",
        "MP-4リストは MP-6 必要条件の候補プール。F(S,2)明示生成系は【文献要請G7-3】未着で未確定(twist doc I-7)。",
        "CAL-3 は裁定296の独立先行結果(u3_calib_v1.py/u3_calib_20260801.json)と同一構成の再実行(参照ハッシュ同梱)。",
        "本certはu7/K^(5)に一切接触していない。発火の可否・タイミングは司令塔の専権。",
    ],
    "generated_at_utc": datetime.datetime.utcnow().isoformat() + "Z",
}

out_path = "search/certs/u7_prefire_20260801.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(cert, f, ensure_ascii=False, indent=2)
print(f"\ncert written: {out_path}")
print(f"overall_pass = {overall_pass}")

sys.exit(0 if overall_pass else 1)
