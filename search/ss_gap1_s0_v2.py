#!/usr/bin/env python3
"""
search/ss_gap1_s0_v2.py
SS-GAP-1 Stage 0 [S0] main computation -- (c') canonical congruence model,
per docs/notes/ssg1_stage0_model_adjudication_v1.md (mathematician, commit
0492ece2, 裁定1098).

Model: H_p := PSL(2,Z/2p^2) = S3 x Q_p ,  Q_p := PSL(2,Z/p^2)
  i_2(Q_p) = 1 + (1/2)*#{tr=0   in SL(2,Z/p^2)}     (doc sec3.2/4)
  i_3(Q_p) = 1 + (1/2)*#{tr=+-1 in SL(2,Z/p^2)}      (doc sec4)
  i_2^T = 3*i_2(Q_p) ,  i_3^R = 2*i_3(Q_p) ,  |Z(H_p)| = 1 ,  |H_p| = 6|Q_p|
  U(p)  = 2 * i_2(Q_p) * i_3(Q_p) / |Q_p|             (doc sec5, [S0] patch)

closed form (a): trace/det histogram counting, O(n^2), n=p^2 -- exact
   because for p not in {2,3} lemma CH-REG (doc sec8.2) guarantees no
   p-congruence-kernel excess (target orders tested are 2,3; p|k only for
   p in {2,3}; here p in {5,7,11,13,17}, none divide 2 or 3).

full enumeration (b): only run for p=5 locally (n=25, full brute force
   n^4=390625 candidate matrices, feasible in seconds) -- classifies every
   SL(2,Z/25) matrix by its ACTUAL order-in-PSL (via literal matrix powers,
   checking A^k = +-I), independent of the trace/det shortcut. This is the
   "(b)" leg required by the spec patch to catch coding bugs (the math
   itself is already proven exact by the adjudication doc for p=5,7,11,13,17).

Excludes p=3 per doc sec5/sec8.5 (fit only over p=5,7,11,13,17); the p=3
PC-5b registration was already done in the prior Stage-0-partial run
(search/certs/ss_gap1_pc5_*_20260813.json) and matches the doc's prediction
Delta=26=3^3-1 exactly.
"""
import json
import math
from pathlib import Path

import numpy as np


def bc_histogram(n):
    hist = [0] * n
    for b in range(n):
        row = (b * np.arange(n)) % n
        for k in row:
            hist[int(k)] += 1
    return hist


def count_trace_det(t, e, n, hist):
    total = 0
    for a in range(n):
        d = (t - a) % n
        kappa = (a * d - e) % n
        total += hist[kappa]
    return total


def closed_form_Q(p):
    n = p * p
    hist = bc_histogram(n)
    count_tr0 = count_trace_det(0, 1, n, hist)
    count_tr1 = count_trace_det(1, 1, n, hist)
    count_trm1 = count_trace_det((-1) % n, 1, n, hist)
    i2 = 1 + count_tr0 // 2
    i3 = 1 + (count_tr1 + count_trm1) // 2
    assert count_tr0 % 2 == 0, f"count_tr0 not even at p={p}: {count_tr0}"
    assert (count_tr1 + count_trm1) % 2 == 0, f"count_tr1+count_trm1 not even at p={p}"
    Q_order_formula = p**4 * (p**2 - 1) // 2
    return {
        "p": p, "n": n,
        "count_tr0_SL": count_tr0,
        "count_tr1_SL": count_tr1,
        "count_trm1_SL": count_trm1,
        "i2_Qp": i2,
        "i3_Qp": i3,
        "Qp_order": Q_order_formula,
        "i2T": 3 * i2,
        "i3R": 2 * i3,
        "Z_Hp": 1,
        "Hp_order": 6 * Q_order_formula,
        "U": 2 * i2 * i3 / Q_order_formula,
    }


def full_enumeration_p5():
    """Ground-truth full enumeration for p=5 (n=25): brute-force ALL SL(2,Z/25)
    matrices via 4 nested loops, check det=1, dedupe by {A,-A}, compute the
    PSL order of each pair by literal matrix exponentiation (A^k =? +-I),
    classify i2 (order|2) and i3 (order|3). Independent of the trace/det
    shortcut used in closed_form_Q -- different algorithm entirely."""
    n = 25
    mats = []
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if (a * d - b * c) % n == 1:
                        mats.append((a, b, c, d))
    seen = set()
    def matmul(X, Y):
        a, b, c, d = X
        e, f, g, h = Y
        return ((a * e + b * g) % n, (a * f + b * h) % n,
                (c * e + d * g) % n, (c * f + d * h) % n)
    IDm = (1, 0, 0, 1)
    NEGIDm = (n - 1, 0, 0, n - 1)
    def is_id_or_neg(M):
        return M == IDm or M == NEGIDm
    i2_count = 0
    i3_count = 0
    total_classes = 0
    for M in mats:
        negM = ((n - M[0]) % n, (n - M[1]) % n, (n - M[2]) % n, (n - M[3]) % n)
        key = min(M, negM)
        if key in seen:
            continue
        seen.add(key)
        total_classes += 1
        # find PSL order: smallest k>=1 with M^k = +-I
        cur = M
        k = 1
        while not is_id_or_neg(cur):
            cur = matmul(cur, M)
            k += 1
            if k > 40:
                raise RuntimeError("order search exceeded bound, unexpected")
        if k in (1, 2):
            i2_count += 1
        if k in (1, 3):
            i3_count += 1
    return {
        "p": 5, "n": 25,
        "SL_matrix_count": len(mats),
        "PSL_class_count": total_classes,
        "i2_Qp_full_enum": i2_count,
        "i3_Qp_full_enum": i3_count,
    }


def main():
    primes = [5, 7, 11, 13, 17]
    results = [closed_form_Q(p) for p in primes]

    fe5 = full_enumeration_p5()
    cf5 = next(r for r in results if r["p"] == 5)
    match_i2_p5 = (fe5["i2_Qp_full_enum"] == cf5["i2_Qp"])
    match_i3_p5 = (fe5["i3_Qp_full_enum"] == cf5["i3_Qp"])

    # PRED-S0-2 check: doc predicts U(5) in [48,50], hand-estimate i2~301,i3~601
    pred_s0_2_U5 = cf5["U"]

    # fit: log(U) = log(const) + e*log(p)
    logp = np.log(np.array(primes, dtype=float))
    logU = np.log(np.array([r["U"] for r in results], dtype=float))
    e_fit_np, logc_fit_np = np.polyfit(logp, logU, 1)
    e_fit = float(e_fit_np)
    logc_fit = float(logc_fit_np)
    const_fit = math.exp(logc_fit)

    U_691_fit = const_fit * (691 ** e_fit)
    U_691_e2_2p2 = 2 * 691 ** 2  # doc's PRED-S0-3 naive formula 2p^2

    CPD_bound = 15180
    cpd_pass_fit = (U_691_fit >= CPD_bound)
    cpd_pass_2p2 = (U_691_e2_2p2 >= CPD_bound)

    out = {
        "schema": "ssg1_count/v2_stage0_main",
        "generated_by": {
            "tool": "python3 (numpy for histogram/fit only, no group-theory library)",
            "script": "search/ss_gap1_s0_v2.py",
            "order": "裁定1098 / docs/notes/ssg1_stage0_model_adjudication_v1.md",
        },
        "model": "(c') H_p := PSL(2,Z/2p^2) = S3 x Q_p, Q_p := PSL(2,Z/p^2)",
        "u_touched": False,
        "c_touched": False,
        "prereg_quantities_touched": False,
        "d_no_interpretation": "machine values only; verdict は司令塔",

        "model_eligibility_argument": {
            "claim": "#Epi^mk(Z/2*Z/3, H_p) > 0 は構成により自動的に成立する(計算不要な論理的事実)",
            "reasoning": "PSL(2,Z) = Z/2*Z/3 = <a,b | a^2=b^3=1> であり、標準生成元 a=S, b=ST "
                "(S=[[0,-1],[1,0]], T=[[1,1],[0,1]]) は PSL(2,Z) を生成する(古典的事実)。"
                "H_p := PSL(2,Z)/Gamma(2p^2) は PSL(2,Z) の商であるから、任意の全射準同型の下で"
                "生成元の像は像群を生成する(群論の初等的事実: phi:G->>Q 全射, G=<S> ならば Q=<phi(S)>)。"
                "よって a,b の H_p での像は自動的に H_p を生成し、a^2=1,b^3=1 は完全に厳密に保たれる"
                "(近似ではない、Gamma(2p^2) による商でも a^2,b^3 の関係式自体は変わらない)。"
                "ゆえに #Epi^mk > 0 は p に依らず保証される -- これは計算ではなく構成の帰結。",
            "numeric_corroboration": "i2^T, i3^R は下記 raw_values で全 p について正の値(実際 i2_Qp,i3_Qp >= 1 "
                "は closed_form の '1 + ...' 形から自明に成立し、かつ p>=5 では非自明元も豊富(count_tr0等 > 0))。",
        },

        "raw_values": results,

        "full_enumeration_crosscheck_p5": {
            "method": "brute force ALL SL(2,Z/25) matrices (n^4=390625), dedupe by {A,-A}, "
                      "literal matrix exponentiation to find PSL order (A^k =? +-I). "
                      "Independent of the trace/det histogram shortcut.",
            "data": fe5,
            "match_i2": match_i2_p5,
            "match_i3": match_i3_p5,
        },

        "PRED_S0_checks": {
            "PRED-S0-2_doc_predicted_range": [48, 50],
            "PRED-S0-2_measured_U5": pred_s0_2_U5,
            "PRED-S0-2_in_range": (48 <= pred_s0_2_U5 <= 50),
        },

        "fit": {
            "primes_used": primes,
            "note": "p=3 excluded per doc sec5/sec8.5 (known artifact positive control, "
                    "registered separately in ss_gap1_pc5_*)",
            "e_fit": float(e_fit),
            "const_fit": float(const_fit),
            "U_values_used": [r["U"] for r in results],
            "PRED-S0-1_doc_predicted_e": 2,
            "e_fit_minus_2": float(e_fit - 2),
        },

        "extrapolation_p691": {
            "U_691_via_fit_const_times_p_pow_e": U_691_fit,
            "U_691_via_doc_naive_formula_2p2": U_691_e2_2p2,
            "PRED-S0-3_doc_predicted": 9.55e5,
            "extrapolation_label": "★外挿 -- p=691 は本セッションで一切計算していない(触らない方針を厳守)。"
                "上記2値はいずれも p=5..17 の実測からの外挿/解析的概算であり、p=691 の直接計算値ではない。",
        },

        "CPD_comparison": {
            "CPD_bound_from_cyclotomic_lower_bound": CPD_bound,
            "U_691_fit_ge_bound": cpd_pass_fit,
            "U_691_2p2_ge_bound": cpd_pass_2p2,
            "note": "U(p) >= 15180 <=> p >= 87 なる doc の解析(2p^2 モデルで)と、"
                    "上記 fit ベースの値を突合。判定語は付さず、生の比較結果のみ記帳。",
        },
    }

    out_path = Path("search/certs/ss_gap1_s0_v2_python_20260813.json")
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=None), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("\nwrote", out_path)


if __name__ == "__main__":
    main()
