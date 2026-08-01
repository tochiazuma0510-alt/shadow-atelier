# search/probe/wac_v1/ihnec_r4b_shards_manifest_gen.py
# 便99 W99-2.1-(6)(sol/sol_reply_99_math26.md・裁定412)。
#
# 目的: R4b の CI 12-shard cert(+ run.log)が scratchpad/ihnec_r4b/ (git 未追跡)
# にのみ存在し(判読書 cv9_reading_ihnec_r4ab_v1.md §8【軽微-5】)、GHA artifact
# は失効しうるため、永続位置 search/certs/ihnec_r4b_shards/ へ複写収蔵し、
# SHA256SUMS を添えて manifest 化する。
#
# 「二環境」の注記: 12 shard の provenance.gap_version はすべて 4.16.0 で
# あり(本スクリプトが機械確認)、二環境化は Windows(ローカル)/ Linux(CI ubuntu)
# という OS/toolchain 層の再現性であって、GAP 4.16.0 の実装独立性ではない
# (判読書§5「総評」・便99 F99-6.1のW98系での同種注記と同じ精神)。
import json, hashlib, os, sys, platform

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SHARDS_DIR = os.path.join(ROOT, "search", "certs", "ihnec_r4b_shards")

def relpath(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

M_VALUES = [0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17]

entries = []
gap_versions = set()
script_shas = set()
shadow_totals = {}
for m in M_VALUES:
    cert_dst = os.path.join(SHARDS_DIR, "ihnec_r4b_m%d_20260801.json" % m)
    log_dst = os.path.join(SHARDS_DIR, "ihnec_r4b_m%d_20260801.run.log" % m)
    cert_src = os.path.join(ROOT, "scratchpad", "ihnec_r4b",
                             "mine-run-ihnec-r4b-roof-20260801-m%d" % m,
                             "mine", "out", "ihnec-r4b-roof-20260801", "m%d" % m,
                             "ihnec_r4b_m%d_20260801.json" % m)
    log_src = os.path.join(ROOT, "scratchpad", "ihnec_r4b",
                            "mine-run-ihnec-r4b-roof-20260801-m%d" % m,
                            "ci", "out", "run.log")

    if not os.path.isfile(cert_dst):
        raise SystemExit("missing permanent copy: %s" % cert_dst)
    if not os.path.isfile(log_dst):
        raise SystemExit("missing permanent copy: %s" % log_dst)

    cert_dst_sha = sha(cert_dst)
    cert_src_sha = sha(cert_src) if os.path.isfile(cert_src) else None
    log_dst_sha = sha(log_dst)
    log_src_sha = sha(log_src) if os.path.isfile(log_src) else None

    byte_identical_to_scratchpad_cert = (cert_src_sha == cert_dst_sha) if cert_src_sha else None
    byte_identical_to_scratchpad_log = (log_src_sha == log_dst_sha) if log_src_sha else None

    d = json.load(open(cert_dst, encoding="utf-8"))
    gap_versions.add(d["provenance"]["gap_version"])
    script_shas.add(d["provenance"]["script_sha256"])
    shadow_totals[m] = d["scan"]["shadow_total"]

    entries.append({
        "m": m,
        "cert": {"path": relpath(cert_dst), "sha256": cert_dst_sha,
                 "byte_identical_to_scratchpad_origin": byte_identical_to_scratchpad_cert,
                 "scratchpad_origin_path": relpath(cert_src) if cert_src_sha else "n/a(scratchpad原本は本セッションで既に不在の可能性・複写時点のsha256のみ記録)"},
        "run_log": {"path": relpath(log_dst), "sha256": log_dst_sha,
                    "byte_identical_to_scratchpad_origin": byte_identical_to_scratchpad_log,
                    "scratchpad_origin_path": relpath(log_src) if log_src_sha else "n/a"},
        "gap_version": d["provenance"]["gap_version"],
        "script_sha256": d["provenance"]["script_sha256"],
        "shadow_total": d["scan"]["shadow_total"]
    })

sum_shadow_total = sum(shadow_totals.values())
live_driver_path = os.path.join(ROOT, "search", "probe", "wac_v1", "ihnec_r4b_run.g")
live_driver_sha = sha(live_driver_path)

manifest = {
    "schema": "ihnec-r4b-shards-manifest/v1",
    "generated_by": {
        "tool": "python (permanent-location copy + digest manifest generator; does not recompute shadow_total)",
        "script": relpath(os.path.abspath(__file__)),
        "date": "2026-08-02"
    },
    "task_ref": "便99 W99-2.1-(6)(sol/sol_reply_99_math26.md・裁定412)。判読書cv9_reading_ihnec_r4ab_v1.md §8【軽微-5】の是正。",
    "note": "R4bのCI 12-shard cert(+run.log)を scratchpad/ihnec_r4b/(git未追跡・GHA artifactは失効しうる)から search/certs/ihnec_r4b_shards/(git追跡・永続)へ複写収蔵した。数値の再計算は行わない(byte複写のみ・sha256で同一性を確認)。",
    "ci_run_reference": {
        "provider": "GitHub Actions",
        "run_id": "30697198947",
        "source_of_run_id": "mine/reports/ihnec-r4b-20260801_report.md (既存の検収レポート)",
        "jobs": "plan ジョブ + 12 gate-and-run shard ジョブ(m in {0,2,3,5,6,8,9,11,12,14,15,17})、全て conclusion=success(既存レポートに記載・本manifestは再確認していない)"
    },
    "two_environments_caveat": {
        "statement_ja": "「二環境」はWindows(ローカル)/Linux ubuntu(CI)というOS/toolchain層の再現性を指す。GAP自体は12 shard全てで4.16.0であることを本スクリプトが機械確認しており(gap_versions_observed参照)、GAP 4.16.0という単一実装に対する独立性の検証ではない(判読書cv9_reading_ihnec_r4ab_v1.md §5総評・【軽微-1】と同じ趣旨)。",
        "gap_versions_observed": sorted(gap_versions),
        "gap_implementation_independence_established": False
    },
    "script_sha256_consistency": {
        "distinct_script_sha256_values_across_12_shards": sorted(script_shas),
        "matches_live_driver": (script_shas == {live_driver_sha}),
        "live_driver_path": relpath(live_driver_path),
        "live_driver_sha256": live_driver_sha,
        "interpretation": "12 shard全てが単一のprovenance.script_sha256を報告し、それが現worktreeのihnec_r4b_run.gと一致する(driver不変性の確認)" if script_shas == {live_driver_sha} else "不一致あり -- 要調査"
    },
    "shard_accounting": {
        "m_values": M_VALUES,
        "shadow_total_per_m": shadow_totals,
        "sum_of_12_shard_shadow_totals": sum_shadow_total,
        "expected_972": sum_shadow_total == 972
    },
    "entries": entries,
    "conventions_used": {
        "ledger_version": "conventions_ledger_v1_4",
        "perm_composition": "n/a(manifest自体は置換演算を行わない)",
        "comparison_target": {
            "as_function_of": "n/a(本manifestは12 shard certの永続複写と digest 突合であり、二実装照合ではない)",
            "function_a": {"name": "n/a", "domain": "n/a", "source_digest": "n/a"},
            "function_b": {"name": "n/a", "domain": "n/a", "source_digest": "n/a"},
            "normalization_digest": "n/a"
        },
        "chi_P_criterion": {"value": "exact", "justification": "shadow_totalという厳密基数の12shard和のみを扱う", "generator_fixed": "n/a", "orientation_fixed": "n/a"},
        "separation": {
            "included": False, "competitor_universe": [],
            "result": {"result_digest": "n/a"},
            "forbidden_values": {"handling": "n/a", "list": []},
            "dummy_fixture": {"id": "n/a", "normalised_input": "n/a", "normalised_output": "n/a",
                              "discriminating_power": {"input_layer_novel": False, "output_layer_novel": False},
                              "expected": "n/a", "observed": "n/a", "verdict": "n/a"}
        },
        "roundtrip_witness": {"status": "n/a", "reason": "往復ラベル変換を持たない"},
        "effective_source_chain": {"status": "n/a", "reason": "本manifestは新規の永続化(初回複写)であり、既存certを訂正・supersedeしない。scratchpad原本は削除しない(複写のみ)"},
        "effective_source": {"status": "n/a", "reason": "同上"},
        "seal_recoverability": {"status": "n/a", "reason": "封印fixtureを使用しない"},
        "level": "PB3"
    },
    "provenance": {
        "python_version": sys.version,
        "platform": platform.platform()
    }
}

OUT_JSON = os.path.join(SHARDS_DIR, "MANIFEST_ihnec_r4b_shards_20260802.json")
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
    f.write("\n")

# SHA256SUMS-style plain text (sha256sum-compatible format: "<sha256>  <path>")
sums_lines = []
for e in entries:
    sums_lines.append("%s  %s" % (e["cert"]["sha256"], os.path.basename(e["cert"]["path"])))
    sums_lines.append("%s  %s" % (e["run_log"]["sha256"], os.path.basename(e["run_log"]["path"])))
sums_lines.sort()
OUT_SUMS = os.path.join(SHARDS_DIR, "SHA256SUMS")
with open(OUT_SUMS, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(sums_lines) + "\n")

print("Wrote", relpath(OUT_JSON))
print("Wrote", relpath(OUT_SUMS))
print("sum_of_12_shard_shadow_totals =", sum_shadow_total, "(expected 972)")
print("gap_versions_observed =", sorted(gap_versions))
print("script_sha256 matches live driver =", script_shas == {live_driver_sha})
