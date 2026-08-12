#!/usr/bin/env python3
"""[D2-GATE] 次数18合成被覆 monodromy 測定(数値 path-tracking) -- 裁定1083/1086/1087・
docs/notes/p1d2_r1_canonicalization_v2.md §8.2 直結実装。

構成(v2 §7.3, 18枚の葉):
    t --y^2=-4t(2枚)--> y --x^3-3zeta3*y*x-(y^2+2y)=0(3枚)--> (x,y)
      --x^2 w^3-27*zeta3*y*(w+1)=0 (3枚)--> (x,y,w)
E : y^2 + 3*zeta3*x*y + 2*y = x^3   (Q0=(0,0), Q_inf=O)
W(P): w^3 + rho*A0(x,y)*w + rho*A0(x,y) = 0   (規約: z^3+Az+B, ゲージ z=(beta/alpha)w)
  A0(R) := X(R (-) P) - X_P ,  c := A0(B1)=A0(B2) ,  rho := -27/(4c)

分岐は t=0,1,inf のみ(v2 §7.3・独立検算済)。3分岐点 ⟹ sigma_0*sigma_1*sigma_inf=1
(loop 合成の位相的事実)⟹ sigma_inf は独立追跡せず derive のみ(正直に明記)。

エンジン: mpmath 高精度複素数 Newton 連続接続(predictor=前ステップの解・corrector=Newton)。
E の群法則(add/neg/A0_of)は search/p1_d2_scan_v2.py(裁定1080/1081・V4 PASS 済)と
同一導出を独立に再実装(コピーではなく同一の代数式を書き下し・数値は独立に再計算)。

出力: JSON(生値のみ)。GAP 後段(search/d2_gate_v1_group.g 相当・python 側が生成)で
Size/AllBlocks/IsTransitive と S18 共役判定を行う。
"""
import argparse
import json
import hashlib
import time
from pathlib import Path

import sympy as sp
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]

I = sp.I
zeta3 = sp.Rational(-1, 2) + sp.sqrt(3) / 2 * I
a1_t_sym, a3_t_sym = 3 * zeta3, sp.Integer(2)
zeta12 = sp.sqrt(3) / 2 + I / 2


def cs(e):
    return sp.simplify(sp.expand(e))


# ---- B1,B2 exact symbolic derivation (independent re-derivation, same target curve) ----
y_B1 = cs(-2 * (1 + I) / zeta12)
y_B2 = cs(-2 * (1 - I) / zeta12)


def w_of(s, yv):
    return cs(8 * I * s + (4 - 6 * zeta12 * yv))


w_B1 = w_of(1, y_B1)
w_B2 = w_of(-1, y_B2)

a_cov, b_cov = -16 * I, 36 * zeta12**2
c_cov, d_cov = -48 * zeta12, 16
X1_B1, W_B1 = cs(a_cov * y_B1), cs(a_cov * w_B1)
X1_B2, W_B2 = cs(a_cov * y_B2), cs(a_cov * w_B2)
X1d_B1 = cs(X1_B1 + b_cov / 3)
X1d_B2 = cs(X1_B2 + b_cov / 3)

u_val = 4 * I
s_val = cs(u_val * a1_t_sym / 2)
r_val = cs(s_val**2 / 3)
t_val_const = cs(u_val**3)
u2, u3 = cs(u_val**2), cs(u_val**3)


def to_target(X_S, Y_S):
    X_T = cs((X_S - r_val) / u2)
    Y_T = cs((Y_S - u2 * s_val * X_T - t_val_const) / u3)
    return X_T, Y_T


X_B1_sym, Y_B1_sym = to_target(X1d_B1, W_B1)
X_B2_sym, Y_B2_sym = to_target(X1d_B2, W_B2)


def build_state(dps):
    mp.mp.dps = dps

    def to_mp(e):
        n = sp.N(e, dps + 15)
        return mp.mpc(str(sp.re(n)), str(sp.im(n)))

    a1 = to_mp(a1_t_sym)
    a3 = to_mp(a3_t_sym)
    XB1, YB1 = to_mp(X_B1_sym), to_mp(Y_B1_sym)
    XB2, YB2 = to_mp(X_B2_sym), to_mp(Y_B2_sym)

    def neg(P):
        x, yv = P
        return (x, -yv - a1 * x - a3)

    def add(P1, P2):
        x1, y1v = P1
        x2, y2v = P2
        if abs(x1 - x2) < mp.mpf(10) ** (-(dps - 10)):
            if abs(y1v + y2v + a1 * x1 + a3) < mp.mpf(10) ** (-(dps - 10)):
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
        RmP = add(R, neg(P))
        return RmP[0] - P[0]

    assert abs(on_curve_resid((XB1, YB1))) < mp.mpf(10) ** (-(dps - 10))
    assert abs(on_curve_resid((XB2, YB2))) < mp.mpf(10) ** (-(dps - 10))
    Q0 = (mp.mpc(0), mp.mpc(0))
    sumB = add((XB1, YB1), (XB2, YB2))
    assert abs(sumB[0]) < mp.mpf(10) ** (-(dps - 10))
    assert abs(sumB[1]) < mp.mpf(10) ** (-(dps - 10))

    # ---- [D2-2] 4 points P (independent re-derivation) ----
    cubic_coeffs = [mp.mpc(1), mp.mpc(0), -2 * a1, mp.mpc(-8)]
    roots = mp.polyroots(cubic_coeffs, maxsteps=400, extraprec=dps * 8)
    cand = []
    for r in roots:
        xv = r
        yv = xv**3 / 2 - a1 * xv - a3
        cand.append((xv, yv))

    P1 = (mp.mpc(0), mp.mpc(-2))
    # identify P2 = the root nearest the cert p1_d2_scan_v2 recorded P2 value
    # (search/certs/p1_d2_scan_v2_20260813.json, d2_2_points_reproduced[1])
    p2_cert_re = mp.mpf("1.37007270483432961175101010064")
    p2_cert_im = mp.mpf("0.912964171632262767821564487482")
    p2_target = mp.mpc(p2_cert_re, p2_cert_im)
    best = min(cand, key=lambda pt: abs(pt[0] - p2_target))
    P2 = best

    for P in (P1, P2):
        assert abs(on_curve_resid(P)) < mp.mpf(10) ** (-(dps - 10)), "P off curve"

    return dict(
        dps=dps, a1=a1, a3=a3, XB1=XB1, YB1=YB1, XB2=XB2, YB2=YB2,
        neg=neg, add=add, on_curve_resid=on_curve_resid, A0_of=A0_of,
        Q0=Q0, P1=P1, P2=P2,
    )


def get_c_rho(state, P):
    A0_of = state["A0_of"]
    XB1, YB1, XB2, YB2 = state["XB1"], state["YB1"], state["XB2"], state["YB2"]
    dps = state["dps"]
    A0B1 = A0_of((XB1, YB1), P)
    A0B2 = A0_of((XB2, YB2), P)
    resid = abs(A0B1 - A0B2)
    c = (A0B1 + A0B2) / 2
    rho = -27 / (4 * c)
    return c, rho, str(resid)


# ---------------------------------------------------------------------------
# path-tracking primitives
# ---------------------------------------------------------------------------

def newton_continue(f, fp, x_prev, args, maxiter=25, tol=None):
    x = x_prev
    for _ in range(maxiter):
        fx = f(x, *args)
        fpx = fp(x, *args)
        if fpx == 0:
            break
        dx = fx / fpx
        x = x - dx
        if tol is not None and abs(dx) < tol:
            break
    return x


def make_loop_path(t0, b, radius, n_line, n_circle):
    d = (t0 - b)
    d = d / abs(d)
    p_b = b + radius * d
    seg1 = [t0 + (p_b - t0) * mp.mpf(k) / n_line for k in range(n_line + 1)]
    theta0 = mp.arg(d)
    circle = [b + radius * mp.exp(mp.mpc(0, 1) * (theta0 + 2 * mp.pi * mp.mpf(k) / n_circle))
              for k in range(n_circle + 1)]
    seg2 = list(reversed(seg1))
    return seg1 + circle[1:] + seg2[1:]


def build_fiber(state, P, rho, t0):
    a1, a3 = state["a1"], state["a3"]
    A0_of = state["A0_of"]
    dps = state["dps"]

    y0 = mp.sqrt(-4 * t0)
    y0s = [y0, -y0]

    x0 = [[], []]
    for iy in range(2):
        yv = y0s[iy]
        coeffs = [mp.mpc(1), mp.mpc(0), -a1 * yv, -(yv**2 + a3 * yv)]
        roots = mp.polyroots(coeffs, maxsteps=400, extraprec=dps * 8)
        x0[iy] = list(roots)

    w0 = [[None, None, None], [None, None, None]]
    for iy in range(2):
        yv = y0s[iy]
        for ix in range(3):
            xv = x0[iy][ix]
            a0v = A0_of((xv, yv), P)
            c1 = rho * a0v
            coeffs = [mp.mpc(1), mp.mpc(0), c1, c1]
            roots = mp.polyroots(coeffs, maxsteps=400, extraprec=dps * 8)
            w0[iy][ix] = list(roots)

    return y0s, x0, w0


def track_loop(state, P, rho, t0, branch_point, radius, n_line, n_circle):
    a1, a3 = state["a1"], state["a3"]
    A0_of = state["A0_of"]

    y0s, x0, w0 = build_fiber(state, P, rho, t0)
    path = make_loop_path(t0, branch_point, radius, n_line, n_circle)

    def f_y(y, t):
        return y**2 + 4 * t

    def fp_y(y, t):
        return 2 * y

    def f_x(x, y):
        return x**3 - a1 * y * x - (y**2 + a3 * y)

    def fp_x(x, y):
        return 3 * x**2 - a1 * y

    def f_w(w, c1):
        return w**3 + c1 * w + c1

    def fp_w(w, c1):
        return 3 * w**2 + c1

    y_seq = [[y0s[iy]] for iy in range(2)]
    for t_new in path[1:]:
        for iy in range(2):
            y_prev = y_seq[iy][-1]
            y_seq[iy].append(newton_continue(f_y, fp_y, y_prev, (t_new,)))

    x_seq = [[[x0[iy][ix]] for ix in range(3)] for iy in range(2)]
    for step in range(1, len(path)):
        for iy in range(2):
            y_new = y_seq[iy][step]
            for ix in range(3):
                x_prev = x_seq[iy][ix][-1]
                x_seq[iy][ix].append(newton_continue(f_x, fp_x, x_prev, (y_new,)))

    w_seq = [[[[w0[iy][ix][iw]] for iw in range(3)] for ix in range(3)] for iy in range(2)]
    for step in range(1, len(path)):
        for iy in range(2):
            y_new = y_seq[iy][step]
            for ix in range(3):
                x_new = x_seq[iy][ix][step]
                a0v = A0_of((x_new, y_new), P)
                c1 = rho * a0v
                for iw in range(3):
                    w_prev = w_seq[iy][ix][iw][-1]
                    w_seq[iy][ix][iw].append(newton_continue(f_w, fp_w, w_prev, (c1,)))

    # ---- match final values back to the initial fiber ----
    diagnostics = {"max_match_dist": 0.0}

    y_final = [y_seq[iy][-1] for iy in range(2)]
    y_perm = []
    for iy in range(2):
        dists = [abs(y_final[iy] - y0s[j]) for j in range(2)]
        j = dists.index(min(dists))
        diagnostics["max_match_dist"] = max(diagnostics["max_match_dist"], float(min(dists)))
        y_perm.append(j)

    x_perm = [[None, None, None], [None, None, None]]
    for iy in range(2):
        jy = y_perm[iy]
        for ix in range(3):
            xf = x_seq[iy][ix][-1]
            dists = [abs(xf - x0[jy][k]) for k in range(3)]
            k = dists.index(min(dists))
            diagnostics["max_match_dist"] = max(diagnostics["max_match_dist"], float(min(dists)))
            x_perm[iy][ix] = k

    w_perm = [[[None, None, None] for _ in range(3)] for _ in range(2)]
    for iy in range(2):
        jy = y_perm[iy]
        for ix in range(3):
            jx = x_perm[iy][ix]
            for iw in range(3):
                wf = w_seq[iy][ix][iw][-1]
                dists = [abs(wf - w0[jy][jx][k]) for k in range(3)]
                k = dists.index(min(dists))
                diagnostics["max_match_dist"] = max(diagnostics["max_match_dist"], float(min(dists)))
                w_perm[iy][ix][iw] = k

    def idx(iy, ix, iw):
        return iy * 9 + ix * 3 + iw

    sigma = [None] * 18
    for iy in range(2):
        jy = y_perm[iy]
        for ix in range(3):
            jx = x_perm[iy][ix]
            for iw in range(3):
                jw = w_perm[iy][ix][iw]
                sigma[idx(iy, ix, iw)] = idx(jy, jx, jw)

    q = [None] * 6

    def qidx(iy, ix):
        return iy * 3 + ix

    for iy in range(2):
        jy = y_perm[iy]
        for ix in range(3):
            jx = x_perm[iy][ix]
            q[qidx(iy, ix)] = qidx(jy, jx)

    return dict(sigma=sigma, q=q, diagnostics=diagnostics, n_steps=len(path))


def perm_to_1indexed(sigma0idx):
    return [x + 1 for x in sigma0idx]


def compose(sigma_a, sigma_b):
    # (a then b): result[i] = b[a[i]]
    return [sigma_b[sigma_a[i]] for i in range(len(sigma_a))]


def inverse(sigma):
    inv = [None] * len(sigma)
    for i, j in enumerate(sigma):
        inv[j] = i
    return inv


def cycle_type(sigma):
    n = len(sigma)
    seen = [False] * n
    cycles = []
    for i in range(n):
        if seen[i]:
            continue
        c = []
        j = i
        while not seen[j]:
            seen[j] = True
            c.append(j)
            j = sigma[j]
        cycles.append(len(c))
    return sorted(cycles, reverse=True)


def perm_as_cycles_1indexed(sigma0idx):
    n = len(sigma0idx)
    seen = [False] * n
    cycles = []
    for i in range(n):
        if seen[i]:
            continue
        c = []
        j = i
        while not seen[j]:
            seen[j] = True
            c.append(j + 1)
            j = sigma0idx[j]
        if len(c) > 1:
            cycles.append(c)
    return cycles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dps", type=int, default=50)
    ap.add_argument("--n_line", type=int, default=300)
    ap.add_argument("--n_circle", type=int, default=720)
    ap.add_argument("--radius", type=float, default=0.15)
    ap.add_argument("--smoke", action="store_true", help="P1 only, reduced density")
    ap.add_argument("--out", type=str, default="search/certs/d2_gate_v1_track_20260813.json")
    args = ap.parse_args()

    dps = args.dps
    n_line, n_circle, radius = args.n_line, args.n_circle, args.radius
    if args.smoke:
        dps = min(dps, 20)
        n_line = min(n_line, 50)
        n_circle = min(n_circle, 100)

    t_start = time.time()
    state = build_state(dps)
    mp.mp.dps = dps
    t0 = mp.mpc("0.55", "0.35")

    targets = ["P1"] if args.smoke else ["P1", "P2"]

    out = {
        "schema": "d2_gate_v1_track/v1",
        "params": {"dps": dps, "n_line": n_line, "n_circle": n_circle, "radius": radius,
                    "t0": mp.nstr(t0, 20), "smoke": bool(args.smoke)},
        "per_point": {},
    }

    for label in targets:
        P = state[label]
        c, rho, resid_c = get_c_rho(state, P)
        out["per_point"][label] = {
            "P": {"X": mp.nstr(P[0], 30), "Y": mp.nstr(P[1], 30)},
            "c_value": mp.nstr(c, 30),
            "rho": mp.nstr(rho, 30),
            "c_v4_residual": resid_c,
        }
        res_loops = {}
        for bname, bpt in (("branch0", mp.mpc(0)), ("branch1", mp.mpc(1))):
            t_loop_start = time.time()
            res = track_loop(state, P, rho, t0, bpt, radius, n_line, n_circle)
            res_loops[bname] = res
            res["seconds"] = time.time() - t_loop_start

        sigma0 = res_loops["branch0"]["sigma"]
        sigma1 = res_loops["branch1"]["sigma"]
        q0 = res_loops["branch0"]["q"]
        q1 = res_loops["branch1"]["q"]
        sigma_inf = inverse(compose(sigma0, sigma1))
        q_inf = inverse(compose(q0, q1))

        out["per_point"][label]["sigma0"] = perm_to_1indexed(sigma0)
        out["per_point"][label]["sigma1"] = perm_to_1indexed(sigma1)
        out["per_point"][label]["sigma_inf_derived"] = perm_to_1indexed(sigma_inf)
        out["per_point"][label]["sigma_inf_note"] = (
            "derived via sigma_inf = (sigma0*sigma1)^-1 (topological loop-composition "
            "identity for a 3-branch-point cover) -- NOT independently path-tracked."
        )
        out["per_point"][label]["cycle_type_sigma0"] = cycle_type(sigma0)
        out["per_point"][label]["cycle_type_sigma1"] = cycle_type(sigma1)
        out["per_point"][label]["cycle_type_sigma_inf_derived"] = cycle_type(sigma_inf)
        out["per_point"][label]["q0_degree6"] = [x + 1 for x in q0]
        out["per_point"][label]["q1_degree6"] = [x + 1 for x in q1]
        out["per_point"][label]["q_inf_degree6_derived"] = [x + 1 for x in q_inf]
        out["per_point"][label]["max_match_dist_branch0"] = res_loops["branch0"]["diagnostics"]["max_match_dist"]
        out["per_point"][label]["max_match_dist_branch1"] = res_loops["branch1"]["diagnostics"]["max_match_dist"]
        out["per_point"][label]["n_steps_per_loop"] = res_loops["branch0"]["n_steps"]
        out["per_point"][label]["seconds_branch0"] = res_loops["branch0"]["seconds"]
        out["per_point"][label]["seconds_branch1"] = res_loops["branch1"]["seconds"]

    out["total_seconds"] = time.time() - t_start
    out["u_touched"] = False
    out["c_touched"] = False
    out["prereg_touched"] = False
    out["d_no_interpretation"] = "machine values only; verdict は司令塔"

    script_bytes = Path(__file__).read_bytes()
    out["provenance"] = {"script_sha256": hashlib.sha256(script_bytes).hexdigest()}

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out_path)

    # ---- emit GAP-syntax generator file (machine-generated, not hand-typed) ----
    gap_path = out_path.with_suffix(".gens.g")
    gap_lines = [
        "# AUTO-GENERATED by search/d2_gate_v1_track.py -- do not hand-edit.",
        "# permutations from numeric path-tracking (dps=%d, n_line=%d, n_circle=%d)" % (dps, n_line, n_circle),
    ]
    for label in targets:
        p = out["per_point"][label]
        gap_lines.append("sigma0_%s := PermList(%s);;" % (label, p["sigma0"]))
        gap_lines.append("sigma1_%s := PermList(%s);;" % (label, p["sigma1"]))
        gap_lines.append("sigmaInf_%s := PermList(%s);;" % (label, p["sigma_inf_derived"]))
    gap_path.write_text("\n".join(gap_lines) + "\n", encoding="ascii")
    print("wrote", gap_path)
    print("total_seconds =", out["total_seconds"])
    for label in targets:
        print(label, "cycle_type_sigma0 =", out["per_point"][label]["cycle_type_sigma0"],
              "cycle_type_sigma1 =", out["per_point"][label]["cycle_type_sigma1"],
              "cycle_type_sigma_inf =", out["per_point"][label]["cycle_type_sigma_inf_derived"],
              "max_match_dist =", max(out["per_point"][label]["max_match_dist_branch0"],
                                       out["per_point"][label]["max_match_dist_branch1"]))


if __name__ == "__main__":
    main()
