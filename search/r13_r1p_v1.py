"""
search/r13_r1p_v1.py -- [P1] 平面モデル本走(裁定983・指示書=docs/notes/branchP_and_r_spec_v1.md
第I部 §I.4 [P1])

★★ 正直申告(先に): 本スクリプトは [P1] の完全な F(t,w) 構成には**到達していない**。
以下の2点は R-0 の既走データから直接・厳密に導出できる「無料の」検算として完了しているが、
F(t,w)=0 の未定係数法+Gröbner による具体的構成は、構造的な設計判断(deg_t F の値、または
W_9 が特殊な形(超楕円的など)を持つか)が指示書に明記されておらず、これを実装係が独自に
仮定して大規模な数式計算(S4窓の CB-a5 系列が要した規模 = groebner*3+newton*3+search*2+
sieve*2+locus*2+lifttest、実質1日仕事)へ突入する前に、この1点をブロッカーとして報告する
判断をした(w=ord不能な仮定の下で誤った巨大計算に走ることを避ける、fail-closed の精神)。

完了: (a) dim L(18 P_inf) の Riemann-Roch 検算 (b) 18(P_0-P_inf)~0 の torsion 検算(R-0の
既走データから直接従う、新規計算なし)。
未完了: F(t,w) の具体的構成(未定係数の本数がまだ確定できない -- 下記「残項目」参照)。
"""
import json
from fractions import Fraction

R0_CERT = "search/certs/r13_r0_v1_1_20260812.json"
OUT_PATH = "search/certs/r13_r1p_v1_20260812.json"


def main():
    with open(R0_CERT, encoding="utf-8") as fh:
        r0 = json.load(fh)

    g = r0["r0c_genus"]["g"]
    D = r0["a_enumeration_completeness"]["g_size"] if False else None  # not the right field; use below
    D = 18  # R-0-a: D=[P_9:H_9^fun]=18 (search/certs/r13_r0_v1_1_20260812.json r0a_D.D)
    D_from_cert = r0["r0a_D"]["D"]
    assert D_from_cert == D, f"D mismatch: cert says {D_from_cert}, expected {D}"
    assert g == 4, f"genus mismatch: cert says {g}, expected 4"

    passport_X = r0["r0b_ramification"]["passport_X_at_0"]
    passport_Z = r0["r0b_ramification"]["passport_Z_at_infty"]
    print(f"[input] from {R0_CERT}: g={g}, D={D}, passport(0)={passport_X}, passport(infty)={passport_Z}")

    # ---- (a) Riemann-Roch check: dim L(18 P_inf) = 18 - g + 1, valid since 18 >= 2g-1 ----
    k = 18
    rr_valid_range = (k >= 2 * g - 1)
    dim_L = k - g + 1
    print(f"[a] Riemann-Roch: dim L({k} P_inf) = {k}-{g}+1 = {dim_L}  "
          f"(valid range check: {k} >= 2*{g}-1={2*g-1}: {rr_valid_range})")
    expected_dim = 15
    dim_matches_design_doc = (dim_L == expected_dim)
    print(f"    matches design doc's stated value 15: {dim_matches_design_doc}")

    # ---- (b) torsion check: div(lambda_9) = D*P0 - D*P_inf (single point, full ramification at
    #      both 0 and infty per R-0's own passport data) => D*(P0-P_inf) ~ 0 (principal divisor) ----
    single_point_at_0 = (len(passport_X) == 1 and passport_X[0][1] == 1)
    single_point_at_inf = (len(passport_Z) == 1 and passport_Z[0][1] == 1)
    ram_at_0 = passport_X[0][0] if passport_X else None
    ram_at_inf = passport_Z[0][0] if passport_Z else None
    torsion_order_divides = (single_point_at_0 and single_point_at_inf and
                              ram_at_0 == D and ram_at_inf == D)
    print(f"[b] torsion: single point at 0 (mult={ram_at_0}), single point at infty (mult={ram_at_inf}) "
          f"=> div(lambda_9) = {D}*P0 - {D}*P_inf => {D}*(P0-P_inf) ~ 0: {torsion_order_divides}")

    # ---- F(t,w) construction status: NOT COMPLETED ----
    blocker = {
        "claim": "F(t,w) の未定係数法+Gröbner による具体的構成には到達していない",
        "known_from_design_doc": {
            "deg_w_F": 18,
            "F_at_t0": "c_0 * w^18 (single root mult 18, from full ramification passport(0)=[[18,1]])",
            "F_at_t1": "c_1*(w-a1)*(w-a2)*prod_{j=1}^{8}(w-bj)^2 "
                        "(passport(1)=[[1,2],[2,8]]: 2 simple roots + 8 double roots)",
            "F_at_tinf": "w=infty corresponds to P_inf; leading term in t is a monomial (stated, "
                          "not made fully explicit in degree)",
        },
        "missing_structural_input": [
            "deg_t F (次数) -- 指示書のどこにも数値が明記されていない。S4窓のu_meas_m3_design_v1.md"
            " §1.4は超楕円(genus 2はほぼ自動的に超楕円)という**別の窓固有の事実**を仮定して"
            " y^2=f(x)型のansatzを取っていたが、genus 4のW_9が同様の特殊構造(例えば超楕円/"
            " trigonal等)を持つかはこのセッションで未検証。W-48(他窓の構造の無断流用禁止)に"
            " 照らし、S4のhyperelliptic ansatzをそのまま転用することはできない。",
            "未定係数の本数を具体的に数えるには deg_t F が要る(dim L(18 P_inf)=15 は「上限の"
            " sanity check」としてのみ使えると指示書に明記されており、それ単独ではansatzの"
            " 次数を決定できない)。",
            "W_9 の特殊構造(超楕円か・trigonal か・一般平面モデルか)を判定する追加情報 "
            "(例えば H_9^fun の置換表現からモノドロミー経由でカバーの型を判定する計算、または "
            "既存文献での類似次数・種数の Belyi 写像の型の参照)が必要。これは W-48 の射程外 "
            "(K^(9) 固有の判定であって他窓の値の流用ではない) だが、このセッションでは未実施。",
        ],
        "why_stopped_here": "deg_t Fを当てずっぽうで固定して大規模Gröbner計算に入ると、S4窓のCB-a5"
                             "系列(groebner*3・newton*3・search*2・sieve*2・locus*2・lifttest、"
                             "実質1日規模)に匹敵する計算コストがかかる可能性が高く、仮定が誤って"
                             "いた場合は全て無駄になる。fail-closedの精神(裁定828等)に基づき、"
                             "ここで一度停止し構造的な設計判断を仰ぐのが適切と判断した。",
    }
    print("\n[BLOCKER] F(t,w) construction NOT completed -- see cert for details.")

    out = {
        "schema": "r13-r1p/v1",
        "generated_by": {"tool": "python", "script": "search/r13_r1p_v1.py",
                          "order": "裁定983 / docs/notes/branchP_and_r_spec_v1.md 第I部 §I.4 [P1]"},
        "status": "PARTIAL -- (a)(b) の無料検算は完了・F(t,w)本体の構成は未完了(下記blocker参照)",
        "input_from_R0": {"cert": R0_CERT, "g": g, "D": D,
                           "passport_0": passport_X, "passport_1": r0["r0b_ramification"]["passport_Y_at_1"],
                           "passport_infty": passport_Z},
        "check_a_riemann_roch": {
            "k": k, "g": g, "dim_L_kPinf": dim_L,
            "valid_range_check": rr_valid_range,
            "matches_design_doc_stated_value_15": dim_matches_design_doc,
        },
        "check_b_torsion": {
            "single_point_at_0": single_point_at_0, "single_point_at_infty": single_point_at_inf,
            "ramification_at_0": ram_at_0, "ramification_at_infty": ram_at_inf,
            "div_lambda9_eq_D_P0_minus_D_Pinf": torsion_order_divides,
            "conclusion": f"{D}*(P0-P_inf) ~ 0 (principal divisor, follows directly from R-0's own "
                          f"passport data, no new computation)",
        },
        "f_tw_construction": {"completed": False, "blocker": blocker},
        "u_touched": False,
        "d_no_interpretation": "machine values only; verdict は司令塔",
    }
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"\nwrote {OUT_PATH}")


if __name__ == "__main__":
    main()
