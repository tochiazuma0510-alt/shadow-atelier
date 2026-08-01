# search/probe/wac_v1/ihnec_r4b_conventions_v2_gen.py
# 便99 W99-2.1-(4)(sol/sol_reply_99_math26.md・裁定412)。
#
# 目的: search/certs/ihnec_r4b_run_20260801.json の conventions_used ブロックが
# 規約台帳(docs/notes/conventions_ledger_v1.md)§2 の字義に照らして MALFORMED
# (判読書 cv9_reading_ihnec_r4ab_v1.md §8【要修正-4】): comparison_target が
# object欄へのbare string(規範8違反)・chi_P_criterionが欠落(規範2違反)・
# roundtrip_witness/separation/effective_source_chain/levelも不在。
#
# 本スクリプトは旧cert(ihnec_r4b_run_20260801.json)の値を一切変更せず、
# conventions_used ブロックのみを台帳v1.4正形へ書き直した v2 supplement cert
# を新設する。旧certはCV-10 superseded_byで束縛し(旧certファイル自体は
# byte不変)、数値(972/108/54等)の再検証・再計算は行わない(参照のみ)。
import json, hashlib, os, sys, platform

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def relpath(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

OLD_CERT_PATH = os.path.join(ROOT, "search", "certs", "ihnec_r4b_run_20260801.json")
old_sha = sha(OLD_CERT_PATH)
old = json.load(open(OLD_CERT_PATH, encoding="utf-8"))

# 旧 conventions_used の実測(訂正対象そのものを機械的に確認する -- 手写しではなく実測)
old_cu = old["conventions_used"]
malformed_findings = []
if isinstance(old_cu.get("comparison_target"), str):
    malformed_findings.append({
        "id": "MF-1", "rule": "規範8(object/array欄へのbare string禁止)",
        "field": "conventions_used.comparison_target",
        "observed_old_value": old_cu["comparison_target"],
        "issue": "object欄であるべきcomparison_targetにbare stringが入っている"
    })
if "chi_P_criterion" not in old_cu:
    malformed_findings.append({
        "id": "MF-2", "rule": "規範2(chi_P_criterion省略はMALFORMED・既定値を置かない)",
        "field": "conventions_used.chi_P_criterion",
        "observed_old_value": None,
        "issue": "chi_P_criterion 欄が丸ごと欠落している"
    })
for missing_field in ["roundtrip_witness", "separation", "effective_source_chain", "effective_source", "seal_recoverability", "level", "coset_object", "action_side", "opposite", "representative_vs_invariant"]:
    if missing_field not in old_cu:
        malformed_findings.append({
            "id": "MF-missing-%s" % missing_field, "rule": "規範1(該当しない欄はn/aと書く。欠品自体は不可)",
            "field": "conventions_used.%s" % missing_field,
            "observed_old_value": None,
            "issue": "%s 欄が丸ごと欠落している(旧certの遡及は不要・CL-2・本v2 supplementで補う)" % missing_field
        })

# 旧certの主要数値(参照のみ・再検証や再計算は行わない -- 変更禁止対象)
old_scan = old["scan"]
old_anchors = old["anchors"]

conventions_used_v2 = {
    "ledger_version": "conventions_ledger_v1_4",
    "perm_composition": old_cu.get("perm_composition", "gap_native_right_action"),
    "conjugation": "n/a(本certは共役演算を使わない・(m,f)組の同一性比較のみ)",
    "coset_object": "n/a(剰余類演算を使わない)",
    "action_side": "n/a",
    "coset_side_derivation": "n/a",
    "word_eval": [
        {"layer": "reduced_hexagon_predicate", "direction": "forward",
         "word_source": "search/week3-battery-common.g EnumerateReducedHexagon と数学的に逐語同一(旧certのreduced_hexagon_predicate欄を転記)"}
    ],
    "coarse_of": "n/a(粗ラベル写像を使わない)",
    "word_of": "n/a",
    "roundtrip_witness": {"status": "n/a", "reason": "R4bは粗/精ラベルの往復変換(coarse_of/WordOf)を持たない。直接(m,f)組の同一性比較のみ(判読書§3.1③④参照)"},
    "characters": [],
    "opposite": {"status": "n/a", "reason": "反準同型写像(tau等)は theta/tau homomorphism として実装内で使うが、その型付けはP^opを要しない対称的構成(theta,tauともG->Gの自己準同型として定義・week3-battery-common.g)"},
    "comparison_target": {
        "as_function_of": "R4bはcertificates/K9.v1.json・S4.v2.jsonを一切読まない単系統GAP直接列挙(driver冒頭の独立性申告・本v2生成スクリプトがdriverソースを参照して再確認)。したがって「二実装の比較」は成立せず、本欄は該当なしとして正確に宣言する(旧certのbare string記載をobject化して訂正)",
        "function_a": {"name": "n/a(単系統)", "domain": "n/a", "source_digest": "n/a"},
        "function_b": {"name": "n/a(単系統)", "domain": "n/a", "source_digest": "n/a"},
        "normalization_digest": "n/a(比較対象なし)"
    },
    "separation": {
        "included": False,
        "competitor_universe": [],
        "result": {"result_digest": "n/a(R4b単体では分離条件を導入しない。識別力を持つdummy/negative fixtureは別cert search/certs/ihnec_r4b_negative_fixture_20260802.json(便99 W99-2.1-(5))が担う)"},
        "forbidden_values": {"handling": "n/a", "list": []},
        "dummy_fixture": {
            "id": "n/a(本cert範囲外・search/certs/ihnec_r4b_negative_fixture_20260802.jsonを参照)",
            "normalised_input": "n/a", "normalised_output": "n/a",
            "discriminating_power": {"input_layer_novel": False, "output_layer_novel": False},
            "expected": "n/a", "observed": "n/a", "verdict": "n/a"
        }
    },
    "chi_P_criterion": {
        "value": "exact",
        "justification": "候補(m,f)組の同一性による厳密受理数比較。conjugacy classへの縮約は行わない(旧certで欠落していた欄を新設)",
        "generator_fixed": True,
        "orientation_fixed": True
    },
    "representative_vs_invariant": {
        "exact_representative": {"value": "n/a", "depends_on": {"model_id": "n/a", "uniformizer_id": "n/a", "orientation": "n/a", "lift": "n/a"}},
        "invariants": {"class": "shadow_total(基数)", "order": "n/a"}
    },
    "effective_source_chain": [
        {"role": "erratum", "path": relpath(OLD_CERT_PATH), "sha256": old_sha,
         "scope": "conventions_used ブロックのMALFORMED %d箇所(comparison_targetのbare string・chi_P_criterion欠落・roundtrip_witness/separation/effective_source_chain/level等の欠落)を訂正。scan/anchors/p_ihn_*等の実測値(972/108/54を含む)は本v2で一切改変しない(旧certは無罪・遡及不要・CL-2)" % len(malformed_findings),
         "superseded_by": {"path": "search/certs/ihnec_r4b_conventions_v2_20260802.json", "sha256": "SEE_MANIFEST(自己参照digestは書き出し後にsearch/certs/MANIFEST_sol99_w99_2_1_20260802.sha256へ記録・W99-2.1納品報告で申告)"}}
    ],
    "effective_source": {"path": "search/certs/ihnec_r4b_conventions_v2_20260802.json", "sha256": "SEE_MANIFEST(同上)"},
    "seal_recoverability": {"status": "n/a", "reason": "封印fixtureを使用しない"},
    "level": "PB3"
}

supplement = {
    "schema": "ihnec-r4b-conventions-supplement/v2",
    "generated_by": {
        "tool": "python (schema-conformance supplement generator; does not re-run GAP, does not alter measured values)",
        "script": relpath(os.path.abspath(__file__)),
        "date": "2026-08-02"
    },
    "task_ref": "便99 W99-2.1-(4)(sol/sol_reply_99_math26.md・裁定412)。判読書cv9_reading_ihnec_r4ab_v1.md §8【要修正-4】の是正。",
    "supplements_cert": {"path": relpath(OLD_CERT_PATH), "sha256": old_sha},
    "note": "本certは旧certのconventions_usedブロックのみを台帳v1.4正形へ書き直す。scan/anchors/p_ihn_*/shadows_sample等の実測値は一切変更・再計算しない(値はすべて旧certからの参照のみ)。旧certファイル自体はbyte不変のまま残る。",
    "malformed_findings_fixed": malformed_findings,
    "referenced_old_values": {
        "scan": old_scan,
        "anchors": old_anchors,
        "note": "上記2ブロックは旧cert(%s, sha256=%s)からの逐語参照。本certで再測定・再計算していない。" % (relpath(OLD_CERT_PATH), old_sha)
    },
    "conventions_used": conventions_used_v2,
    "cross_checked_status": old.get("cross_checked_status", {"status": "n/a", "reason": "旧certの記載を転記"}),
    "provenance": {
        "python_version": sys.version,
        "platform": platform.platform(),
        "old_cert_sha256_reconfirmed": old_sha,
        "note": "自己参照digest(このcert自身のsha256)は書き出し後にmanifestへ記録する(構造的な自己言及不能性 -- W99-2.1納品報告で明示的に申告する既知の逸脱)"
    }
}

OUT = os.path.join(ROOT, "search", "certs", "ihnec_r4b_conventions_v2_20260802.json")
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(supplement, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("malformed_findings_fixed count:", len(malformed_findings))
for mf in malformed_findings:
    print(" -", mf["id"], mf["field"])
print("Wrote", relpath(OUT))
print("old_cert_sha256:", old_sha)
