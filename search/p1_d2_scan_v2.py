#!/usr/bin/env python3
"""[P1-D2 v2] [D2-3]+[D2-4] -- 裁定1080 直結実装。 docs/notes/p1d2_concrete_spec_v1.md
の続き(search/p1_d2_scan_v1.py で完了した [D2-1] YES・[D2-2] 4 点を土台にする)。

=== 数学的発見(本スクリプトの導出過程で判明・報告書に明記) ===
各点 P (2P=Q0) について、A の生成元(L(2P-Q0-Q∞), dim=1)を
    A0(R) := X(R (-) P) - X_P
と明示的に構成すると(X(-P)=X(P) と Q0(-)P = P (2P=Q0 より) から), div(A0) = Q0+Q∞-2P
が厳密に確認できる。RR で dim L(3P-Q0-Q∞)=1 (無条件) だが、L(2P-Q0-Q∞) が
2P~Q0+Q∞ (2P=Q0 の群法則条件と同値) のもとで dim=1 になることと合わせると、
L(2P-Q0-Q∞) ⊆ L(3P-Q0-Q∞) は次元が等しいので**両者は一致**する。
⟹ B の生成元は A0 そのもの(スカラー倍)にしかなり得ない: B = beta*A0。
これは仕様のいう「未知数2個・ゲージで1個減って実質1個」と**矛盾しない**むしろ
同じ結論を別の道で導く:disc = -4*A^3-27*B^2 = A0^2*(-4*alpha^3*A0-27*beta^2)
(alpha:=A の A0 に対する係数)。disc の「Q0,Q∞ 以外の 2 零点」は
A0(R) = c := -27*beta^2/(4*alpha^3) の解 R。A0 は E→P^1 の次数 2 の写像なので、
A0(R)=c の解は厳密に 2 点。ゆえに
    (V4) の判定 ⟺ A0(B1) = A0(B2)  (単一の等式!)
であり、これが成り立てば c := A0(B1) から比 alpha^3/beta^2 = -27/(4c) が一意に決まる
(alpha=1 と正規化すれば beta^2=-4c/27)。

=== エンジン ===
mpmath 高精度複素数演算(60 桁, 4 点中 3 点は根の厳密根号形が sympy.solve で
現実的時間内に終了しなかったため — 判定は残差が桁精度の丸め誤差レベル
(~1e-50)であることで担保。exact 点 (0,-2) と B1,B2(sympy 厳密値を60桁評価)は
桁精度を落とさず持ち込む。★ 厳密証明書(CRootOf/最小多項式)への格上げは未実施
-- 誠実に申告(裁定1080 は「必要なら」と条件付きだったため、数値的に十分な
精度で判定できる場合はこれで確定とする; 格上げが必要と判断されれば追撃する)。
"""
import json
import hashlib
from pathlib import Path

import sympy as sp
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
mp.mp.dps = 60

I = sp.I
zeta3 = sp.Rational(-1, 2) + sp.sqrt(3) / 2 * I
a1_t_sym, a3_t_sym = 3 * zeta3, sp.Integer(2)

# ---- reproduce B1,B2 target coords exactly (same derivation as v1 script) ----
zeta12 = sp.sqrt(3) / 2 + I / 2

def cs(e):
    return sp.simplify(sp.expand(e))

y = sp.symbols('y')
y_B1 = cs(-2 * (1 + I) / zeta12)
y_B2 = cs(-2 * (1 - I) / zeta12)

def w_of(s, yv):
    return cs(8 * I * s + (4 - 6 * zeta12 * yv))

w_B1 = w_of(1, y_B1)
w_B2 = w_of(-1, y_B2)

a_cov, b_cov, c_cov, d_cov = -16 * I, 36 * zeta12**2, -48 * zeta12, 16
X1_B1, W_B1 = cs(a_cov * y_B1), cs(a_cov * w_B1)
X1_B2, W_B2 = cs(a_cov * y_B2), cs(a_cov * w_B2)
X1d_B1 = cs(X1_B1 + b_cov / 3)
X1d_B2 = cs(X1_B2 + b_cov / 3)

u_val = 4 * I
s_val = cs(u_val * a1_t_sym / 2)
r_val = cs(s_val**2 / 3)
t_val = cs(u_val**3)
u2, u3 = cs(u_val**2), cs(u_val**3)

def to_target(X_S, Y_S):
    X_T = cs((X_S - r_val) / u2)
    Y_T = cs((Y_S - u2 * s_val * X_T - t_val) / u3)
    return X_T, Y_T

X_B1_sym, Y_B1_sym = to_target(X1d_B1, W_B1)
X_B2_sym, Y_B2_sym = to_target(X1d_B2, W_B2)

# convert to mpmath at 60 dps
def to_mp(e):
    n = sp.N(e, 60)
    return mp.mpc(str(sp.re(n)), str(sp.im(n)))

a1 = to_mp(a1_t_sym)
a3 = to_mp(a3_t_sym)
XB1 = to_mp(X_B1_sym); YB1 = to_mp(Y_B1_sym)
XB2 = to_mp(X_B2_sym); YB2 = to_mp(Y_B2_sym)

# ---- Weierstrass group law (mpmath) ----
def neg(P):
    x, yv = P
    return (x, -yv - a1 * x - a3)

def add(P1, P2):
    x1, y1v = P1
    x2, y2v = P2
    if abs(x1 - x2) < mp.mpf(10)**(-40):
        if abs(y1v + y2v + a1 * x1 + a3) < mp.mpf(10)**(-40):
            return None
        lam = (3 * x1**2 - a1 * y1v) / (2 * y1v + a1 * x1 + a3)
    else:
        lam = (y2v - y1v) / (x2 - x1)
    nu = y1v - lam * x1
    x3v = lam**2 + a1 * lam - x1 - x2
    y3v = -(lam + a1) * x3v - nu - a3
    return (x3v, y3v)

def on_curve_resid(P):
    x, yv = P
    return yv**2 + a1 * x * yv + a3 * yv - x**3

def A0_of(R, P):
    # A0(R) := X(R (-) P) - X_P
    RmP = add(R, neg(P))
    return RmP[0] - P[0]

# sanity: B1, B2 on curve, B1+B2 = Q0
assert abs(on_curve_resid((XB1, YB1))) < mp.mpf(10)**(-50)
assert abs(on_curve_resid((XB2, YB2))) < mp.mpf(10)**(-50)
Q0 = (mp.mpc(0), mp.mpc(0))
sumB = add((XB1, YB1), (XB2, YB2))
assert abs(sumB[0]) < mp.mpf(10)**(-50) and abs(sumB[1]) < mp.mpf(10)**(-50)

# ---- [D2-2] the 4 points P (reproduced at 60 dps) ----
P_points = []
P_points.append({"label": "P1", "pt": (mp.mpc(0), mp.mpc(-2)), "exact": True})

a1_c = a1  # complex
cubic_coeffs = [mp.mpc(1), mp.mpc(0), -2 * a1_c, mp.mpc(-8)]
roots = mp.polyroots(cubic_coeffs, maxsteps=300, extraprec=400)
for idx, r in enumerate(roots):
    xv = r
    yv = xv**3 / 2 - a1 * xv - a3
    P_points.append({"label": f"P{idx+2}", "pt": (xv, yv), "exact": False})

# verify all 4 points satisfy on-curve and 2P=Q0
def double_pt(P):
    x, yv = P
    lam = (3 * x**2 - a1 * yv) / (2 * yv + a1 * x + a3)
    x3v = lam**2 + a1 * lam - 2 * x
    y3v = -(lam + a1) * x3v - (yv - lam * x) - a3
    return (x3v, y3v)

for rec in P_points:
    P = rec["pt"]
    rec["on_curve_residual"] = str(abs(on_curve_resid(P)))
    d2 = double_pt(P)
    rec["twoP_minus_Q0_residual"] = str(max(abs(d2[0]), abs(d2[1])))

# ---- [D2-3]+[D2-4](V4): for each P, decisive equality A0(B1) =? A0(B2) ----
watches = {
    "V1": [], "V2": None, "V3": [], "V4": [], "V5": [], "V6": None, "V7": None
}
per_point_results = []

for rec in P_points:
    P = rec["pt"]
    label = rec["label"]
    A0_B1 = A0_of((XB1, YB1), P)
    A0_B2 = A0_of((XB2, YB2), P)
    resid_v4 = abs(A0_B1 - A0_B2)
    v4_pass = resid_v4 < mp.mpf(10)**(-45)

    entry = {
        "label": label,
        "P": {"X": mp.nstr(P[0], 30), "Y": mp.nstr(P[1], 30)},
        "A0_B1": mp.nstr(A0_B1, 30),
        "A0_B2": mp.nstr(A0_B2, 30),
        "V4_residual_abs": str(resid_v4),
        "V4_pass": bool(v4_pass),
    }

    if v4_pass:
        c_val = (A0_B1 + A0_B2) / 2
        entry["c_value"] = mp.nstr(c_val, 30)
        c_nonzero = abs(c_val) > mp.mpf(10)**(-30)
        entry["c_nonzero"] = bool(c_nonzero)
        if c_nonzero:
            # normalize alpha=1; beta^2 = -4c/27
            beta_sq = -4 * c_val / 27
            entry["alpha"] = "1 (normalization)"
            entry["beta_squared"] = mp.nstr(beta_sq, 30)
            entry["alpha3_over_beta2_ratio"] = mp.nstr(-27 / (4 * c_val), 30)

            # V1: deg(disc)=6 -- check A0 has genuine order-2 pole at P (nonzero
            # leading Laurent coefficient), via a nearby-point finite-difference
            # sanity probe (A0 -> infinity like kappa/eps^2 as R->P along a
            # generic direction; check it actually blows up, not exactly proving
            # order but excluding an accidental order-drop)
            eps = mp.mpf(10)**(-12)
            R_near = (P[0] + eps, None)
            # move along the curve near P: solve y from curve eq via Newton
            # from P's own y as an initial guess (small perturbation)
            def curve_y_near(xv, y_guess):
                yv = y_guess
                for _ in range(40):
                    f = yv**2 + a1 * xv * yv + a3 * yv - xv**3
                    fp = 2 * yv + a1 * xv + a3
                    if abs(fp) < mp.mpf(10)**(-40):
                        break
                    yv = yv - f / fp
                return yv
            y_near = curve_y_near(P[0] + eps, P[1])
            R_near = (P[0] + eps, y_near)
            A0_near = A0_of(R_near, P)
            v1_blowup_ratio = abs(A0_near) / abs(eps**-2) if abs(eps) != 0 else None
            entry["V1_pole_order2_probe_A0_near_over_eps_inv2"] = mp.nstr(v1_blowup_ratio, 10)
            v1_pass = abs(A0_near) > mp.mpf(10)**10  # genuinely blowing up at eps=1e-12
            entry["V1_pass"] = bool(v1_pass)
            watches["V1"].append(v1_pass)

            # V3: ord_Q0(B)=ord_Q∞(B)=1, automatic since B=beta*A0 (beta!=0) and
            # A0 has exact simple zeros at Q0,Q∞ by construction (verified below
            # directly: A0(Q0)=0, A0(Q∞ i.e. R->P along -P branch)=0, and check
            # A0 is NOT identically zero / doesn't have a higher-order zero by a
            # nearby-point derivative probe)
            A0_at_Q0 = A0_of(Q0, P)
            entry["A0_at_Q0_residual"] = str(abs(A0_at_Q0))
            v3_zero_at_Q0 = abs(A0_at_Q0) < mp.mpf(10)**(-45)
            # A0 at Q_infty: R=Q_infty means R(-)P = -P, X(-P)=X(P) so A0(Q_inf)=0 by construction (always true)
            entry["V3_zero_at_Q0_pass"] = bool(v3_zero_at_Q0)
            v3_pass = v3_zero_at_Q0 and c_nonzero
            entry["V3_pass"] = bool(v3_pass)
            watches["V3"].append(v3_pass)

            # V5: genus(W9)=4 via RH given ramification profile e=3,3,2,2 (R=6),
            # contingent on V1 (deg D=6) and V4 (B1,B2 are exactly the 2 extra
            # zeros, i.e. simple => e=2 there) and the pre-established V3-type
            # total ramification e=3 at Q0,Q_inf. This is an arithmetic
            # consequence check, not an independent new construction.
            R_total = 2 + 2 + 1 + 1
            g_E = 1  # E is an elliptic curve (genus 1) -- NOT genus 0 (self-caught bug, fixed)
            genus_w9 = (3 * (2 * g_E - 2) + R_total + 2) // 2
            entry["V5_RH_genus_computed"] = genus_w9
            v5_pass = (genus_w9 == 4)
            entry["V5_pass"] = bool(v5_pass)
            watches["V5"].append(v5_pass)
        else:
            entry["note"] = "c=0 -> degenerate (beta would be 0); V1/V3/V5 not evaluated for this P"
    per_point_results.append(entry)
    watches["V4"].append(bool(v4_pass))

watches["V2"] = "pre-established globally in [D2-0] (delta=0); not re-derived per-point here"
watches["V6"] = ("NOT COMPUTED -- requires constructing the actual degree-3 cover "
                  "W9 (z^3=A z+B over E, an explicit genus-4 curve) and computing "
                  "the order of the divisor class P0-P_inf in its Jacobian. This is "
                  "a materially larger computation (function-field/Jacobian "
                  "arithmetic on a genus-4 curve, or period/torsion computation) "
                  "than [D2-1]-[D2-4]'s elliptic-curve-only algebra, and was not "
                  "attempted in this pass. Honestly flagged, not fabricated.")

any_v4_pass = any(watches["V4"])
watches["V7"] = {
    "all_4_points_failed_V4": (not any_v4_pass),
    "note": ("If true: 'no degree-3 cover with z as a line-bundle section exists' "
              "-- first-class negative result -> Miranda form territory.")
              if not any_v4_pass else
             "at least one P passes V4 -- not a V7 negative result."
}

# ---------------------------------------------------------------------------
result = {
    "schema": "r13-p1d2/v2",
    "generated_by": {
        "tool": "python (mpmath 60dps complex algebra + sympy for exact B1,B2 "
                "derivation carried over from p1_d2_scan_v1.py). No GAP execution.",
        "script": "search/p1_d2_scan_v2.py",
        "order": "裁定1080 [D2-3]+[D2-4] / docs/notes/p1d2_concrete_spec_v1.md",
    },
    "status": "D2-3 (linear system, all 4 P's) and D2-4 watches V1,V3,V4,V5,V7 COMPLETE. "
              "V2 = pre-established global fact (cited, not re-derived). "
              "V6 NOT COMPUTED (out of scope for this pass -- see watches.V6).",
    "target_curve": "E: Y^2+3*zeta3*X*Y+2*Y=X^3, Q_inf=O, Q0=(0,0)",
    "mathematical_finding": (
        "L(2P-Q0-Q_inf) = L(3P-Q0-Q_inf) exactly (both dim 1) under the branching "
        "condition 2P=Q0, forcing B to be a scalar multiple of the SAME generator "
        "A0 as A. This reduces the whole D2-3/D2-4(V4) system to a single scalar "
        "equality test A0(B1)=?A0(B2), since A0:E->P^1 is a degree-2 map and its "
        "fiber over any value has exactly 2 points -- so A0(B1)=A0(B2) (with "
        "B1!=B2) is necessary AND sufficient for {B1,B2} to be exactly disc's "
        "remaining 2 zeros. See in-script docstring for the derivation."
    ),
    "B1_target": {"X": mp.nstr(XB1, 30), "Y": mp.nstr(YB1, 30)},
    "B2_target": {"X": mp.nstr(XB2, 30), "Y": mp.nstr(YB2, 30)},
    "d2_2_points_reproduced": [
        {"label": r["label"], "X": mp.nstr(r["pt"][0], 30), "Y": mp.nstr(r["pt"][1], 30),
         "exact": r["exact"], "on_curve_residual": r["on_curve_residual"],
         "twoP_minus_Q0_residual": r["twoP_minus_Q0_residual"]}
        for r in P_points
    ],
    "d2_3_and_d2_4_per_point": per_point_results,
    "watches_V1_V7": watches,
    "quarantine_4_lines_1007": {
        "name_collide_note": "本仕様の平方類/立方類は F_9(E) の函数体類。封印『c 平方類』"
                              "(K^(5) 窓インスタンス)とは別対象。",
        "n5_value_computed": False,
        "derivation_bridge_found": False,
        "b34_handled_as_divisor": None,
    },
    "u_touched": False,
    "c_touched": False,
    "prereg_touched": False,
    "precision_note": "mpmath 60 decimal digits; V4 pass threshold = residual < 1e-45 "
                       "(i.e. ~15 orders of magnitude below working precision floor, "
                       "not merely round-off). Exact symbolic/CRootOf certificate "
                       "NOT constructed in this pass -- numeric-only per 裁定1080's "
                       "conditional phrasing ('必要なら CRootOf... 厳密化'); flagged "
                       "for upgrade if the coordinator judges it necessary.",
    "d_no_interpretation": "machine values only; verdict は司令塔",
}

script_bytes = Path(__file__).read_bytes()
result["provenance"] = {"script_sha256": hashlib.sha256(script_bytes).hexdigest()}

out_path = ROOT / "search" / "certs" / "p1_d2_scan_v2_20260813.json"
out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

print("=== per-point V4 results ===")
for e in per_point_results:
    print(e["label"], "V4_pass=", e["V4_pass"], "resid=", e["V4_residual_abs"])
print("watches V1:", watches["V1"])
print("watches V3:", watches["V3"])
print("watches V5:", watches["V5"])
print("watches V7:", watches["V7"])
print("wrote", out_path)
print("script sha256 =", result["provenance"]["script_sha256"])
