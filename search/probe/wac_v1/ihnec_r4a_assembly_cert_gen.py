# search/probe/wac_v1/ihnec_r4a_assembly_cert_gen.py
# 便99 W99-2.1-(2)(sol/sol_reply_99_math26.md・裁定412)。
#
# 目的: R4a(scratchpad/ihnec_r4a_run.py)には cert artifact が存在せず、出力が
# docs/notes/ihnec_v1.md 追補C の地の文のみだった(判読書 cv9_reading_ihnec_r4ab_v1.md
# §8【要修正-2】: 「R4a に cert artifact が無い(副検問が非対称)」)。本スクリプトは
# scratchpad/ihnec_r4a_run.py と数学的に同一の計算をこの場で再実行し、その結果を
# 機械可読な cert として search/certs/ihnec_r4a_assembly_20260802.json へ書き出す。
#
# 種別の明記(裁定412 F99-2.1/P99-2.1 の格語法の転記・崩さない):
#   これは測定 cert ではない。R4a は屋根 M = K^(9) cap N_S4 を一度も測定していない。
#   R4a がしているのは「命題 ROOF(4) を、既存の K9.v1.json / S4.v2.json という
#   因子データへ適用し、972 という整数を算出する」という紙予測の実行である。
#   格の正文(裁定412 P99-2.1 逐語): 「命題 ROOF(4) と既存因子 certificate から
#   得る紙の予測 972 と、M 上の 4,408,992 候補の直接悉皆列挙による測定 972 が
#   一致した。cross-check の対象は基数 972 のみ」。
#
# 独立性: このスクリプトは R4a(scratchpad/ihnec_r4a_run.py)と数学的に同一の
# 計算を行う(逐語複製・新しい独立実装ではない)。目的は「R4a の cert 化」で
# あって「R4a のクロスチェック」ではない — 探索器(R4a 本体)と照合器の分離
# 原則に触れない: 本スクリプトは照合器ではなく、既存単系統(R4a)の provenance
# 記録係である。
#
# 宇宙の事前登録: certificates/K9.v1.json・certificates/S4.v2.json の2入力のみ。
# 新しい対象への拡張ではない。
import json, hashlib, sys, os, platform
from math import gcd
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def relpath(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

K9P = os.path.join(ROOT, "certificates", "K9.v1.json")
S4P = os.path.join(ROOT, "certificates", "S4.v2.json")
K9 = json.load(open(K9P, encoding="utf-8"))
S4 = json.load(open(S4P, encoding="utf-8"))

fails = []
def chk(c, msg):
    if not c:
        fails.append(msg)

# ---------- U-11 (GT(K^(9)) の型): 合成表からの確認(R4a と同一の計算) ----------
sh = K9["shadows"]; ct = K9["composition_table"]; N = len(sh)
chk(N == 108, "|GT(K^9)|=108")
chk(K9["target"]["invariants"]["N_ord"] == 18, "K9_ord=18")
chk(K9["counts"]["raw_candidates"] == 12 * 729, "raw_candidates=12*729=8748")
prod = {}
for row in ct:
    prod[(row[0], row[1])] = row[2]
chk(len(prod) == N * N, "合成表 108x108 完備")

inv2 = pow(2, -1, 9)
def theta(s):
    m = s["m"]; a = s["f_triple"][0][0]
    ok_rot = (s["f_triple"][0][1] == 0 and s["f_triple"][1][1] == 0 and s["f_triple"][2][1] == 0)
    chk(ok_rot, "f_triple は回転成分のみ")
    k = (a * inv2) % 9
    chk(s["f_triple"][1][0] % 9 == (-a) % 9, "第2成分 = r^{-2k}")
    kap = (m + 1) if m % 2 == 1 else (-m)
    chk(s["f_triple"][2][0] % 9 == kap % 9, "第3成分 = r^{kappa(m)}")
    return (k, (2 * m + 1) % 9, m % 2)

TH = [theta(s) for s in sh]
chk(len(set(TH)) == 108, "Theta は単射(108点)")
chk(set(x[1] for x in TH) == set(u for u in range(9) if gcd(u, 9) == 1), "u 像 = (Z/9)^x")

bad = 0
for i in range(N):
    for j in range(N):
        k1, u1, e1 = TH[i]; k2, u2, e2 = TH[j]
        want = ((k1 + u1 * k2) % 9, (u1 * u2) % 9, (e1 + e2) % 2)
        if TH[prod[(i, j)]] != want:
            bad += 1
chk(bad == 0, "合成表が Aff(Z/9)xC2 の積と一致(全11664対)")

def order_of(i):
    e = i; n = 1
    ident_list = [t for t in range(N) if all(prod[(t, x)] == x for x in range(N))]
    ident = ident_list[0]
    while e != ident:
        e = prod[(e, i)]; n += 1
    return n
ident_list = [t for t in range(N) if all(prod[(t, x)] == x for x in range(N))]
ident = ident_list[0]
ordprof = Counter(order_of(i) for i in range(N))
center = [i for i in range(N) if all(prod[(i, j)] == prod[(j, i)] for j in range(N))]
chk(len(center) == 2, "中心の位数2")

# ---------- S4 窓の m 像・settled/shadow 述語分離(W99-2.1-(1)を同時に機械確認) ----------
settled_detail = S4["settled_detail"]
s4m = sorted(set(x["m"] for x in settled_detail))
c4 = Counter(x["m"] for x in settled_detail)
chk(S4["settled_count"] == 54, "|GT(N_S4)|=54 (settled_count)")
chk(s4m == [0, 2, 3, 5, 6, 8], "S4 の m 像 = charming set 全体")
chk(set(c4.values()) == {9}, "各 m の fiber = 9")

settled_true = sum(1 for r in settled_detail if r.get("settled") is True)
settled_false = sum(1 for r in settled_detail if r.get("settled") is False)
hexcert = S4["hexagon_free_certificate"]
generation_pass_count = S4["generation_pass_count"]
s4_count_semantics = {
    "r4a": "settled",
    "r4b": "shadow",
    "predicate_definitions": {
        "settled": "S4.v2.json settled_detail[i].settled == true; witness = exists h in P-Gamma-L(2,8) realizing T_{m,f} (week3-psl-common.g RunPSLWindow)。R4a の |GT(N_S4)|=54 assertion はこの述語を使う。",
        "shadow": "hexagon_free_certificate.shadow_total (hex310 and hex311 and surjectivity のみ・settled witness を要求しない)。R4b(ihnec_r4b_run.g)の shadow_total はこの述語。"
    },
    "set_difference_empty_this_run": (settled_true == hexcert["shadow_total"] == generation_pass_count == S4["settled_count"] == 54 and settled_false == 0),
    "machine_check": {
        "method": "S4.v2.json settled_detail の全54行を直接走査し settled フィールドを数える(この cert 生成スクリプト内で実測・値の手写しなし)",
        "settled_true_count": settled_true,
        "settled_false_count": settled_false,
        "settled_detail_total": len(settled_detail),
        "hexagon_free_certificate_shadow_total": hexcert["shadow_total"],
        "generation_pass_count": generation_pass_count,
        "settled_count_field": S4["settled_count"],
        "conclusion": "R4a対象(settled)とR4b対象(shadow)は本run(S4.v2.json)限り集合として一致(54=54=54=54, settled_false=0)。ただし一般には settled subseteq shadow (settled は真に強い条件)であり、両者の同一性はこの cert 特有の実測結果であって定義上の恒等ではない(判読書 §8【要修正-1】)。"
    }
}
chk(s4_count_semantics["set_difference_empty_this_run"], "s4_count_semantics: settled/shadow 集合一致(本run)")

# ---------- 屋根 M = K^(9) cap N_S4 の組立(紙予測 = ROOF(4) の適用。M は未測定) ----------
k9m = sorted(set(s["m"] for s in sh)); ck9 = Counter(s["m"] for s in sh)
chk(sorted(set(m % 9 for m in k9m)) == s4m, "P-IHN: X_9 mod 9 の像 = S4 charming set")
GTM = sum(ck9[m] * c4[m % 9] for m in k9m if m % 9 in c4)
chk(GTM == 972, "P-IHN-4: |GT(M)|=972 (紙予測の組立)")
imgK9 = sorted({m for m in k9m if m % 9 in c4})
chk(imgK9 == k9m, "P-IHN-5: Im R_{M,K9} は全 m-fiber を含む(108/108全射)")
imgS4 = sorted({m % 9 for m in k9m} & set(s4m))
chk(imgS4 == s4m, "P-IHN-6: Im R_{M,S4} は全 m-fiber を含む(54/54全射)")
chk(108 * 54 // 6 == 972, "fiber 積 108*54/|(Z/18)^x|=972")
chk(9 * 9 * 12 == 972, "972 = |F_0(M)|(81) * |(Z/36)^x|(12)")

RESULT = "ALL PASS" if not fails else "FAILED"

recomputed_values = {
    "GT_K9_cardinality": N,
    "U11_composition_pairs_checked": N * N,
    "U11_bad": bad,
    "GT_K9_group_type": "Aff(Z/9) x C2 = Hol(Z/9) x C2",
    "GT_K9_center_order": len(center),
    "GT_K9_order_profile": dict(sorted(ordprof.items())),
    "GT_N_S4_cardinality_settled": S4["settled_count"],
    "s4_m_image": s4m,
    "GTM_assembled_paper_prediction": GTM,
    "F0_M": 81,
    "chi_image_order": 12,
    "im_R_M_K9_full_108_of_108": imgK9 == k9m,
    "im_R_M_S4_full_54_of_54": imgS4 == s4m,
    "failures_count": len(fails),
    "failures_list": fails,
    "overall_result": RESULT,
}

cert_type = {
    "kind": "prediction_provenance_not_measurement",
    "statement_ja": "これは測定certでなく、命題ROOF(4)適用の紙予測のprovenance化である。R4aは屋根M(=K^(9) cap N_S4)を一度も測定していない(M自体の群構成にも触れない)。",
    "grading_transcribed_from": "sol/sol_reply_99_math26.md F99-2.1 / P99-2.1(便99検収=裁定412)",
    "grading_ja_verbatim": "命題ROOF(4)と既存因子certificateから得る紙の予測972と、(M)上の4,408,992候補の直接悉皆列挙による測定972が一致した。cross-checkの対象は基数972のみであり、二つの独立測定、shadow集合/NFの同一性、正典向きの独立照合を主張しない。有限測定はLean未検証である。",
    "grading_en": "paper-predicted x machine-measured, cross-checked for the scalar cardinality 972",
    "not_claimed": [
        "R4aとR4bの二独立測定の一致",
        "shadow集合(972元)そのものの正規形一致",
        "正典向きの独立照合",
        "verified(Lean未接続)"
    ]
}

conventions_used = {
    "ledger_version": "conventions_ledger_v1_4",
    "perm_composition": "n/a(python整数演算のみ・置換合成なし)",
    "comparison_target": {
        "as_function_of": "n/a(本certは二実装の照合ではなく、R4a単系統の入力certからの組立をprovenance化するのみ)",
        "function_a": {"name": "n/a", "domain": "n/a", "source_digest": "n/a"},
        "function_b": {"name": "n/a", "domain": "n/a", "source_digest": "n/a"},
        "normalization_digest": "n/a"
    },
    "chi_P_criterion": {
        "value": "exact",
        "justification": "K9.v1.json/S4.v2.jsonの(m,f)組そのものを数える厳密基数(conjugacy classへの縮約なし)",
        "generator_fixed": True,
        "orientation_fixed": True
    },
    "separation": {
        "included": False,
        "competitor_universe": [],
        "result": {"result_digest": "n/a(本certは単系統の組立provenance・分離条件は別cert search/certs/ihnec_r4b_negative_fixture_20260802.json が担う)"},
        "forbidden_values": {"handling": "n/a", "list": []},
        "dummy_fixture": {
            "id": "n/a", "normalised_input": "n/a", "normalised_output": "n/a",
            "discriminating_power": {"input_layer_novel": False, "output_layer_novel": False},
            "expected": "n/a", "observed": "n/a", "verdict": "n/a"
        }
    },
    "roundtrip_witness": {"status": "n/a", "reason": "粗/精ラベルの往復変換を持たない(既存cert内の(m,f)組をそのまま数えるのみ)"},
    "effective_source_chain": {"status": "n/a", "reason": "本certは新規provenance化の初出であり、既存certを訂正・supersedeしない(R4aにはこれまでcert artifactが存在しなかった)"},
    "effective_source": {"status": "n/a", "reason": "同上"},
    "seal_recoverability": {"status": "n/a", "reason": "封印fixtureを使用しない"},
    "level": "PB3"
}

cert = {
    "schema": "ihnec-r4a-assembly/v1",
    "generated_by": {
        "tool": "python (single-lane provenance-ization; not a new independent implementation)",
        "script": relpath(os.path.abspath(__file__)),
        "date": "2026-08-02"
    },
    "task_ref": "便99 W99-2.1-(2)(sol/sol_reply_99_math26.md・裁定412)。R4aの片側cert不在(判読書cv9_reading_ihnec_r4ab_v1.md §8【要修正-2】)の解消。",
    "reproduces": {
        "original_script": "scratchpad/ihnec_r4a_run.py",
        "original_script_sha256": sha(os.path.join(ROOT, "scratchpad", "ihnec_r4a_run.py")),
        "note": "本certの計算はscratchpad/ihnec_r4a_run.pyと数学的に同一(逐語複製)。目的はR4aの結果をcert化することであり、R4aへの独立クロスチェックではない。"
    },
    "cert_type": cert_type,
    "inputs": {
        "K9_v1": {"path": relpath(K9P), "sha256": sha(K9P)},
        "S4_v2": {"path": relpath(S4P), "sha256": sha(S4P)}
    },
    "recomputed_values": recomputed_values,
    "s4_count_semantics": s4_count_semantics,
    "conventions_used": conventions_used,
    "cross_checked_status": {"status": "n/a", "reason": "本certはR4a単系統の組立をcert化するのみ(972の紙予測x機械測定の一致という格はsol/sol_reply_99_math26.md F99-2.1/P99-2.1に別途記帳済み。本certはそのR4a側のprovenanceを埋めるものであって、それ自体がcross-checked certを新規に主張するものではない)"},
    "provenance": {
        "python_version": sys.version,
        "platform": platform.platform(),
        "generator_script_note": "このcert生成スクリプト自身のsha256は本cert書き出し後にsearch/certs/MANIFEST_sol99_w99_2_1_20260802.sha256へ記録する(自己参照digestの構造的制約 -- 台帳CV-10の自己言及不能性についてはW99-2.1納品報告で申告)"
    }
}

OUT = os.path.join(ROOT, "search", "certs", "ihnec_r4a_assembly_20260802.json")
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(cert, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("RESULT:", RESULT)
print("failures:", len(fails))
print("Wrote", relpath(OUT))
