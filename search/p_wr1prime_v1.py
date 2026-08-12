"""
search/p_wr1prime_v1.py -- P-WR-1' 前哨(裁定953・仕様=docs/notes/retarget_F_audit_v1.md §4.3)

既走 cert の det フィールド読み出し(新規探索なし)。retarget (F) = H_F = SL^pm(2,691) x_{C2} S3 の
C2 判定: braid 対 (a,b) が H_F を生成するなら braid 関係 aba=bab から det(a)=det(b) が強制される
(§4.1)。det(a)=det(b)=-1 なら Goursat の懸念が消えて C2 は即 PASS(§4.2)。

入力(§4.3 の指定どおり):
  search/certs/w691_gen23_witness_v1_20260812.json  (H_2 の目撃者 -- ただし下記の raw finding 参照)
  search/certs/w691_gen23_braid_backconv_v1_20260812.json (逆変換, all_ok=true)

★ raw finding(判定ではなく事実確認): witness_v1 cert の "witness":{"a":...,"b":...} は
  (2,3)-生成対 (u,v)(u が位数2・v が位数3、a=u,b=v)であって、braid 関係 aba=bab を満たす braid 対
  ではない -- 実際に det(a),det(b) を計算すると H_2 で det(a)=690,det(b)=1(不一致)であり、
  §4.1 が要求する fail-closed 検査「期待: det(a)=det(b)」を witness_v1 の raw pair は満たさない。
  真の braid 対(aba=bab を満たす)は w691_gen23_braid_backconv_v1 の (x,y) であり(cert 内
  "braid_relation_ok":true で確認済み)、本前哨はそちらから det を読む(§4.3 の
  「必要なら braid_backconv」を発動する側になった)。

det は cert に直接のフィールドとして格納されていないため、格納済みの 2x2 整数行列から
det(M) = M[0][0]*M[1][1] - M[0][1]*M[1][0] mod 691 を独立に計算する(cert の生データの読み出しの
範囲内 -- 新規探索・新規行列生成は一切行わない)。
"""
import json

P = 691
WITNESS_PATH = "search/certs/w691_gen23_witness_v1_20260812.json"
BACKCONV_PATH = "search/certs/w691_gen23_braid_backconv_v1_20260812.json"
OUT_PATH = "search/certs/p_wr1prime_v1_20260812.json"


def det2(M, p=P):
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % p


def main():
    with open(WITNESS_PATH, encoding="utf-8") as fh:
        witness_cert = json.load(fh)
    with open(BACKCONV_PATH, encoding="utf-8") as fh:
        backconv_cert = json.load(fh)

    witness_h2 = next(r for r in witness_cert["results"] if r["label"] == "H_2")
    backconv_h2 = next(r for r in backconv_cert["results"] if r["label"] == "H_2")
    backconv_h6 = next(r for r in backconv_cert["results"] if r["label"] == "H_6")

    # raw pair from witness_v1 (the (2,3)-generators u,v -- NOT a braid pair, see docstring)
    wit_a, wit_b = witness_h2["witness"]["a"], witness_h2["witness"]["b"]
    wit_det_a, wit_det_b = det2(wit_a), det2(wit_b)
    wit_det_equal = (wit_det_a == wit_det_b)

    # true braid pair from braid_backconv (aba=bab confirmed via braid_relation_ok in that cert)
    bc_x, bc_y = backconv_h2["x"], backconv_h2["y"]
    bc_det_x, bc_det_y = det2(bc_x), det2(bc_y)
    bc_det_equal = (bc_det_x == bc_det_y)
    bc_both_minus1 = (bc_det_x == P - 1) and (bc_det_y == P - 1)
    bc_braid_relation_ok = backconv_h2["braid_relation_ok"]

    # H_6 supplementary (not the target of this outpost -- H_F=SL^pm concerns H_2 only -- but
    # computed for transparency since braid_backconv contains it too)
    h6_x, h6_y = backconv_h6["x"], backconv_h6["y"]
    h6_det_x, h6_det_y = det2(h6_x), det2(h6_y)

    print("[RAW] witness_v1 H_2 raw pair (a,b) -- these are (2,3)-generators, NOT the braid pair:")
    print(f"      det(a)={wit_det_a} det(b)={wit_det_b} equal={wit_det_equal}")
    print("[RAW] braid_backconv H_2 true braid pair (x,y), braid_relation_ok=", bc_braid_relation_ok)
    print(f"      det(x)={bc_det_x} det(y)={bc_det_y} equal={bc_det_equal} both=-1(={P-1})={bc_both_minus1}")
    print(f"[RAW] braid_backconv H_6 (supplementary, not this outpost's target): "
          f"det(x)={h6_det_x} det(y)={h6_det_y} equal={h6_det_x == h6_det_y}")

    # [2] judgement per §4.3 step [2] -- boolean only, no verdict language
    c2_pass = bc_det_equal and bc_both_minus1 and bc_braid_relation_ok

    out = {
        "schema": "wr1prime/v1",
        "generated_by": {"tool": "python", "script": "search/p_wr1prime_v1.py",
                          "order": "裁定953 / docs/notes/retarget_F_audit_v1.md §4.3"},
        "inputs": {"witness_cert": WITNESS_PATH, "braid_backconv_cert": BACKCONV_PATH},
        "raw_finding": {
            "note": "witness_v1 の H_2 raw (a,b) は (2,3)-生成対であり braid 対ではない -- "
                    "det(a)=det(b) が成り立たない(690 vs 1)。真の braid 対は braid_backconv の (x,y)。",
            "witness_v1_raw_pair_det_a": wit_det_a, "witness_v1_raw_pair_det_b": wit_det_b,
            "witness_v1_raw_pair_det_equal": wit_det_equal,
        },
        "step1_true_braid_pair_det": {
            "source": "w691_gen23_braid_backconv_v1_20260812.json (H_2, braid_relation_ok=true)",
            "det_x": bc_det_x, "det_y": bc_det_y, "det_equal": bc_det_equal,
        },
        "step2_judgement": {
            "det_equal": bc_det_equal,
            "det_both_minus1": bc_both_minus1,
            "braid_relation_ok": bc_braid_relation_ok,
            "c2_pass": c2_pass,
        },
        "supplementary_h6_not_this_outposts_target": {
            "det_x": h6_det_x, "det_y": h6_det_y, "det_equal": (h6_det_x == h6_det_y),
        },
        "p": P,
        "u_touched": False,
        "d_no_interpretation": "boolean/raw values only; verdict は司令塔",
    }
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"\nwrote {OUT_PATH}")
    print(f"[RAW] c2_pass = {c2_pass}")


if __name__ == "__main__":
    main()
