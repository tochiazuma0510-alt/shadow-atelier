#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
asm_alpha_cal_v1.py

較正スイート ASM-α-CAL/v1(campaign v2 §5'.4.2 の発注仕様の実装)。

発注元: docs/notes/framework_promotion_campaign_v2.md §5'.4.2
移設元(参照のみ・両ファイルは現行リポジトリに現物が見当たらないため独立再実装):
    scratchpad/falsifier_passport_probe2.py (SHA-256 8b4d48c1398fb869052189b90913d175650a674ecb436fce0e13da980ed9e368 と申告)
    scratchpad/falsifier_discrimination.py  (SHA-256 d4c630fcb2780f6e5fc95f8aca786888dd1eaa7b23b82ff59b685cffbe85e30f と申告)
    → 群定義(G_n, H_{2,alpha,0}, X, Y)は search/probe/wac_v1/alpha_general_window_check.py と
      同一の模型(Sol P_n / ODD-H 補題A の加法座標)を独立に書き下したもの。ordered passport の
      閉形式は docs/notes/oddH_full_proof_v1.md §6 命題 ODD-P(紙上証明)を機械側で再現する。

格: python 単系統(cross-checked ではない・Lean 検証でもない)。tier = calibration。

宇宙(事前登録・変更しない):
    n in {3, 7, 9, 11, 13, 15, 21}   (奇数。n=5 は封印遵守で明示除外・非接触)
    alpha in Z/n                     (0 を含む全て)
    j=2, beta=0 に固定(H_{2,alpha,0}。campaign / falsifier 判読書と同一の窓族)

模型: G_n = (Z/n)^3 rtimes Q, Q = {1,q1,q2,q3} = C2 x C2 (ODD-H 補題A の加法座標)
      q_j は第 j 座標を固定し他の 2 座標を反転。
      a1=(1,0,0)標識, a2=(0,1,0), a3=(0,0,1)
      X = a1 q1 = ((1,0,0),1)
      Y = a1 a2 a3 q2 = ((1,1,1),2)
      Z = (X*Y)^{-1}
      U_alpha = {(alpha*v, u, v): u,v in Z/n}, H_{2,alpha,0} = U_alpha \\sqcup U_alpha*q2

必須検査 4 本(campaign v2 §5'.4.2 表):
    C-1  ordered passport の閉形式(命題 ODD-P)の機械側再現(79/79 一致)
    C-2  分離条件: gcd(alpha,n)=1 => K3/K5 型 / gcd(alpha,n)=d>1 => K3/K5 型でない(56/56, 0/16)
    C-3  陰性対照 2 本: (i) alpha=0 は N_G(H)!=H / (ii) 非単元 alpha は passport 不一致
    C-4  部分群性の直検査: H×H の全対で閉じている(H×Hgens だけではない)+ 生成集合からの生成が H に一致

fail-closed: C-2 が 1 件でも破れたら PREREGISTRATION_FALSIFIED で即停止。
封印非接触: n=5 は宇宙から明示除外(assert)。窓データ・Im R・封印量には一切触れない。
"""
import json
import math
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timezone

UNIVERSE_N = [3, 7, 9, 11, 13, 15, 21]
assert 5 not in UNIVERSE_N, "seal discipline: n=5 must not appear (excluded by preregistration)"
assert all(n % 2 == 1 for n in UNIVERSE_N), "universe must be odd n"

# ---------------------------------------------------------------------------
# 群の演算(G_n = (Z/n)^3 rtimes Q, Q = C2 x C2、ODD-H 補題A の加法座標)
# ---------------------------------------------------------------------------

QSIGNS = {
    0: (1, 1, 1),      # 1
    1: (1, -1, -1),    # q1
    2: (-1, 1, -1),    # q2
    3: (-1, -1, 1),    # q3
}

def qmul(i, j):
    s = tuple(QSIGNS[i][k] * QSIGNS[j][k] for k in range(3))
    for lab, v in QSIGNS.items():
        if v == s:
            return lab
    raise AssertionError("Q is not closed")

def act(q, a, n):
    s = QSIGNS[q]
    return tuple((s[k] * a[k]) % n for k in range(3))

def mul(g, h, n):
    a, q = g
    b, r = h
    return (tuple((a[k] + act(q, b, n)[k]) % n for k in range(3)), qmul(q, r))

def inv(g, n):
    a, q = g
    return (tuple((-x) % n for x in act(q, a, n)), q)  # Q has exponent 2

IDENTITY = ((0, 0, 0), 0)

def full_group(n):
    return [((a1, a2, a3), q)
            for a1 in range(n) for a2 in range(n) for a3 in range(n)
            for q in range(4)]

def window(n, alpha):
    """H_{2,alpha,0} を集合として返す(U_alpha と U_alpha*q2 の非交和)。"""
    U = set()
    for u in range(n):
        for v in range(n):
            U.add((((alpha * v) % n, u % n, v % n), 0))
    H = set(U)
    q2 = ((0, 0, 0), 2)
    for g in U:
        H.add(mul(g, q2, n))
    return H, U

def window_generators(n, alpha):
    # U_alpha = <a2, a1^alpha a3>、H = U_alpha 割 <q2>
    return [((0, 1, 0), 0), ((alpha % n, 0, 1), 0), ((0, 0, 0), 2)]

X_elt = lambda: ((1, 0, 0), 1)
Y_elt = lambda: ((1, 1, 1), 2)

# ---------------------------------------------------------------------------
# C-4: 部分群性の直検査(H の自己閉性・生成集合からの再生成)
# ---------------------------------------------------------------------------

def subgroup_direct_check(n, H):
    """closed(H,H) の全対検査 + 単位元・逆元の所属確認。"""
    Hlist = list(H)
    self_closed = all(mul(g, h, n) in H for g in Hlist for h in Hlist)
    has_identity = IDENTITY in H
    all_invertible = all(inv(g, n) in H for g in Hlist)
    return self_closed, has_identity, all_invertible

def generated_subgroup(gens, n, cap):
    """gens から積閉包を生成(BFS)。cap を超えたら異常終了。"""
    seen = set(gens) | {IDENTITY}
    changed = True
    while changed:
        changed = False
        new_elems = set()
        for g in seen:
            for gen in gens:
                for h in (mul(g, gen, n), mul(gen, g, n)):
                    if h not in seen and h not in new_elems:
                        new_elems.add(h)
        if new_elems:
            seen |= new_elems
            changed = True
        if len(seen) > cap:
            raise AssertionError("generated subgroup runaway")
    return seen

# ---------------------------------------------------------------------------
# ordered passport: G/H(左剰余類)上の左移動作用の巡回型
# ---------------------------------------------------------------------------

def coset_action_cycle_type(n, H, t):
    """G/H(左剰余類 gH の集合)上、g H -> (t g) H の左移動作用の置換の巡回型を返す
    (標準の coset 表現 pi: G -> Sym(G/H)、pi(t)(gH) = (t g) H)。
    <X> cap H = 1 かつ |<X>| = [G:H] のため、剰余類の代表元列挙に群全体を
    使わずとも良いが、ここでは素直に G を舐めて剰余類分割を作る(n<=21 で高速)。
    """
    G = full_group(n)
    visited = {}
    reps = []
    for g in G:
        if g in visited:
            continue
        cosetH = set(mul(g, h, n) for h in H)
        cid = len(reps)
        reps.append(g)
        for e in cosetH:
            visited[e] = cid
    num_cosets = len(reps)
    perm = [None] * num_cosets
    for cid, g0 in enumerate(reps):
        g1 = mul(t, g0, n)
        perm[cid] = visited[g1]
    # 巡回型
    seen = [False] * num_cosets
    cycle_lengths = []
    for i in range(num_cosets):
        if seen[i]:
            continue
        length = 0
        j = i
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            length += 1
        cycle_lengths.append(length)
    return num_cosets, tuple(sorted(cycle_lengths, reverse=True))

def cycle_type_str(lengths):
    """[2n] や [2,2,...,1,1] のような長さリストを '2n^1' 式の乗法表記へ。"""
    from collections import Counter
    c = Counter(lengths)
    parts = []
    for length in sorted(c.keys(), reverse=True):
        parts.append(f"{length}^{c[length]}")
    return " ".join(parts)

def closed_form_prediction(n, alpha):
    """命題 ODD-P(j=2)の閉形式予言: (X型, Y型, Z型)。d:=gcd(alpha,n)、gcd(0,n):=n。"""
    d = math.gcd(alpha, n) if alpha % n != 0 else n
    x_type = (2 * n,)
    y_type = tuple([2] * (n - 1) + [1, 1])
    z_type = tuple([2 * n // d] * d)
    return d, tuple(sorted(x_type, reverse=True)), tuple(sorted(y_type, reverse=True)), tuple(sorted(z_type, reverse=True))

def k3k5_target(n):
    x_type = tuple(sorted((2 * n,), reverse=True))
    y_type = tuple(sorted([2] * (n - 1) + [1, 1], reverse=True))
    z_type = tuple(sorted((2 * n,), reverse=True))
    return x_type, y_type, z_type

# ---------------------------------------------------------------------------
# 本体
# ---------------------------------------------------------------------------

def run():
    results = {
        "C1_rows": [],
        "C1_mismatches": [],
        "C2_unit_matches": [],
        "C2_unit_mismatches": [],
        "C2_nonunit_correctly_separated": [],
        "C2_nonunit_wrongly_matched": [],
        "C3_alpha0_control_pass": [],
        "C3_alpha0_control_fail": [],
        "C3_nonunit_control_pass": [],
        "C3_nonunit_control_fail": [],
        "C4_pass": [],
        "C4_fail": [],
    }

    cases_total = 0
    cases_zero = 0
    cases_unit = 0
    cases_nonunit = 0

    for n in UNIVERSE_N:
        for alpha in range(n):
            cases_total += 1
            is_zero = (alpha % n == 0)
            gcd_an = math.gcd(alpha, n) if not is_zero else n
            is_unit = (not is_zero) and gcd_an == 1
            is_nonunit_nonzero = (not is_zero) and gcd_an > 1
            if is_zero:
                cases_zero += 1
            elif is_unit:
                cases_unit += 1
            elif is_nonunit_nonzero:
                cases_nonunit += 1

            H, U = window(n, alpha)

            # --- C-4: 部分群性の直検査 ---
            self_closed, has_id, invertible = subgroup_direct_check(n, H)
            gens = window_generators(n, alpha)
            gen_closure = generated_subgroup(gens, n, cap=len(H) + 10)
            gens_generate_H = (gen_closure == H)
            c4_ok = self_closed and has_id and invertible and gens_generate_H
            tag4 = {"n": n, "alpha": alpha, "self_closed": self_closed,
                    "has_identity": has_id, "all_invertible": invertible,
                    "gens_generate_H": gens_generate_H, "abs_H": len(H)}
            (results["C4_pass"] if c4_ok else results["C4_fail"]).append(tag4)

            # --- ordered passport: 実測 ---
            num_cosets_x, xtype = coset_action_cycle_type(n, H, X_elt())
            XY = mul(X_elt(), Y_elt(), n)
            Z = inv(XY, n)
            num_cosets_y, ytype = coset_action_cycle_type(n, H, Y_elt())
            num_cosets_z, ztype = coset_action_cycle_type(n, H, Z)
            assert num_cosets_x == num_cosets_y == num_cosets_z == 2 * n, \
                ("index mismatch", n, alpha, num_cosets_x, num_cosets_y, num_cosets_z)

            # --- C-1: 閉形式(命題 ODD-P)との一致 ---
            d, pred_x, pred_y, pred_z = closed_form_prediction(n, alpha)
            c1_match = (xtype == pred_x and ytype == pred_y and ztype == pred_z)
            row = {
                "n": n, "alpha": alpha, "d": d,
                "observed": {"X": cycle_type_str(xtype), "Y": cycle_type_str(ytype), "Z": cycle_type_str(ztype)},
                "predicted": {"X": cycle_type_str(pred_x), "Y": cycle_type_str(pred_y), "Z": cycle_type_str(pred_z)},
                "match": c1_match,
            }
            results["C1_rows"].append(row)
            if not c1_match:
                results["C1_mismatches"].append(row)

            # --- N_G(H) = H (HF-3(a) の逆側 / (W3)) ---
            G = full_group(n)
            n_normalizer = 0
            for g in G:
                gi = inv(g, n)
                if all(mul(mul(g, h, n), gi, n) in H for h in gens):
                    n_normalizer += 1
            n_eq_h = (n_normalizer == len(H))

            # --- K3/K5 型判定 ---
            target_x, target_y, target_z = k3k5_target(n)
            is_k3k5 = (xtype == target_x and ytype == target_y and ztype == target_z)

            # --- C-2: 分離条件(alpha!=0 のみ) ---
            if is_unit:
                if is_k3k5:
                    results["C2_unit_matches"].append({"n": n, "alpha": alpha})
                else:
                    results["C2_unit_mismatches"].append({"n": n, "alpha": alpha, "row": row})
            elif is_nonunit_nonzero:
                if not is_k3k5:
                    results["C2_nonunit_correctly_separated"].append({"n": n, "alpha": alpha, "d": d})
                else:
                    results["C2_nonunit_wrongly_matched"].append({"n": n, "alpha": alpha, "row": row})

            # --- C-3: 陰性対照 ---
            if is_zero:
                # (i) alpha=0 では N_G(H) != H を期待
                if not n_eq_h:
                    results["C3_alpha0_control_pass"].append({"n": n, "alpha": alpha})
                else:
                    results["C3_alpha0_control_fail"].append({"n": n, "alpha": alpha, "N_size": n_normalizer, "abs_H": len(H)})
            elif is_nonunit_nonzero:
                # (ii) 非単元 alpha では K3/K5 型でないことを期待
                if not is_k3k5:
                    results["C3_nonunit_control_pass"].append({"n": n, "alpha": alpha})
                else:
                    results["C3_nonunit_control_fail"].append({"n": n, "alpha": alpha, "row": row})

    return results, cases_total, cases_zero, cases_unit, cases_nonunit


def main():
    results, cases_total, cases_zero, cases_unit, cases_nonunit = run()

    c1_pass = len(results["C1_mismatches"]) == 0
    c2_pass = (len(results["C2_unit_mismatches"]) == 0
               and len(results["C2_nonunit_wrongly_matched"]) == 0
               and len(results["C2_unit_matches"]) == cases_unit
               and len(results["C2_nonunit_correctly_separated"]) == cases_nonunit)
    c3_pass = (len(results["C3_alpha0_control_fail"]) == 0
               and len(results["C3_nonunit_control_fail"]) == 0
               and len(results["C3_alpha0_control_pass"]) == cases_zero
               and len(results["C3_nonunit_control_pass"]) == cases_nonunit)
    c4_pass = len(results["C4_fail"]) == 0

    # fail-closed: C-2 が破れたら即停止
    if not c2_pass:
        print(json.dumps({
            "RESULT": "PREREGISTRATION_FALSIFIED",
            "reason": "C-2 separation condition broke (ODD-P closed form and/or actual code disagree)",
            "C2_unit_mismatches": results["C2_unit_mismatches"][:10],
            "C2_nonunit_wrongly_matched": results["C2_nonunit_wrongly_matched"][:10],
        }, ensure_ascii=False, indent=2))
        sys.exit(2)

    summary = {
        "tier": "calibration",
        "id": "ASM-alpha-CAL/v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "conventions_used": {
            "n_universe": UNIVERSE_N,
            "n5_excluded": True,
            "window_family": "H_{j=2,alpha,beta=0}",
            "group_model": "G_n=(Z/n)^3 rtimes Q, Q=C2xC2 (ODD-H 補題A加法座標)",
            "X": "a1*q1", "Y": "a1*a2*a3*q2", "Z": "(X*Y)^-1",
            "closed_form_source": "docs/notes/oddH_full_proof_v1.md #6 命題ODD-P",
            "cases_total": cases_total,
            "cases_alpha_zero": cases_zero,
            "cases_alpha_unit": cases_unit,
            "cases_alpha_nonunit_nonzero": cases_nonunit,
        },
        "checks": {
            "C1_ODD_P_closed_form": {
                "pass": c1_pass,
                "cases_checked": cases_total,
                "mismatches": len(results["C1_mismatches"]),
            },
            "C2_unit_nonunit_separation": {
                "pass": c2_pass,
                "units_matching_K3K5": len(results["C2_unit_matches"]),
                "units_total": cases_unit,
                "nonunits_correctly_separated": len(results["C2_nonunit_correctly_separated"]),
                "nonunits_total": cases_nonunit,
            },
            "C3_negative_controls": {
                "pass": c3_pass,
                "alpha0_control_fired": len(results["C3_alpha0_control_pass"]),
                "alpha0_control_total": cases_zero,
                "nonunit_control_fired": len(results["C3_nonunit_control_pass"]),
                "nonunit_control_total": cases_nonunit,
            },
            "C4_subgroup_direct_check": {
                "pass": c4_pass,
                "cases_checked": cases_total,
                "failures": len(results["C4_fail"]),
            },
        },
        "RESULT": "ALL PASS" if (c1_pass and c2_pass and c3_pass and c4_pass) else "FAIL",
        "fail_closed": True,
        "seal_contact": "none",
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2))

    cert_path = Path(__file__).resolve().parents[2] / "certs" / "asm_alpha_cal_20260805.json"
    cert = dict(summary)
    cert["nonunit_examples"] = results["C2_nonunit_correctly_separated"]
    cert["c1_sample_rows"] = results["C1_rows"][:8]
    script_bytes = Path(__file__).read_bytes()
    cert["self_sha256"] = hashlib.sha256(script_bytes).hexdigest()
    cert_path.parent.mkdir(parents=True, exist_ok=True)
    cert_path.write_text(json.dumps(cert, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"cert written: {cert_path}")

    if not (c1_pass and c2_pass and c3_pass and c4_pass):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
