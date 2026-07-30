# mine/collector/collect.py -- 採掘場(mine)の検収機械化・v0 最小版
# (裁定237・ideas/ideas_013_solver_platform.md §4.6)。
#
# 入力: --artifact-dir <CI が回収した artifact を展開したディレクトリ、
#         または dry-run なら repo の search/certs/ を artifact に見立てた
#         ディレクトリ> --plan <mine-job/v1 の plan JSON>
# 出力: mine/reports/<job_id>_report.md (機械生成)
#
# 機械読み規律(machine-piped):
#   - 判定は cert JSON の値のみから行う。run.log は探さない・grep しない
#     (このスクリプトは log ファイルを一切読まない -- §4.5 の
#     「collector に log reader を実装しない」を機構で守る)。
#   - 片系統しかない項目は candidate、両系統一致は "cross-checked 候補"
#     (最終昇格の裁定は人 -- このスクリプトは裁定しない)。
#
# usage:
#   python mine/collector/collect.py --artifact-dir <dir> --plan <plan.json>
#   python mine/collector/collect.py --artifact-dir search/certs --plan mine/jobs/queue/ladder-recal-20260730.json --dry-run

import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 比較から除外する volatile なキー(実行のたびに変わって当然の値 --
# 一致/不一致の判定対象にしない。情報としては表に出す)。
VOLATILE_KEY_SUBSTRINGS = ("elapsed_sec", "elapsed_ms", "date", "run_id", "timestamp")


def is_volatile_key(key):
    return any(s in key for s in VOLATILE_KEY_SUBSTRINGS)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def classify(obj):
    """cert JSON の中身だけから種別を判定する(ファイル名に依存しない)。"""
    if not isinstance(obj, dict):
        return "unknown"
    schema = obj.get("schema")
    if schema == "ladder-xi-recheck/v1":
        return "checker_window"
    if schema == "ladder-xi-recheck-manifest/v1":
        return "checker_manifest"
    if obj.get("generated_by") == "search/strike-a13-ladder.g":
        if "window_id" in obj:
            return "gap_window"
        if "windows" in obj:
            return "gap_manifest"
    return "unknown"


def discover_certs(dir_path):
    """dir_path 以下(再帰)の *.json を種別ごとに集める。
    SHA256SUMS.txt / result.txt は json ではないので自動的に除外される。"""
    buckets = {"gap_window": [], "gap_manifest": [], "checker_window": [], "checker_manifest": [], "unknown": []}
    for path in sorted(glob.glob(os.path.join(dir_path, "**", "*.json"), recursive=True)):
        try:
            obj = load_json(path)
        except Exception as e:
            buckets["unknown"].append((path, f"(parse error: {e})"))
            continue
        kind = classify(obj)
        buckets[kind].append((path, obj))
    return buckets


def field_diff_table(a, b, keys):
    """a, b (dict) の keys について値を突合する。volatile キーは
    参考列として出すが match 判定には数えない。"""
    rows = []
    all_match = True
    for k in keys:
        av = a.get(k, "(missing)")
        bv = b.get(k, "(missing)")
        volatile = is_volatile_key(k)
        match = (av == bv)
        if not volatile:
            all_match = all_match and match
        rows.append({"key": k, "a": av, "b": bv, "match": match, "volatile": volatile})
    return rows, all_match


# 較正再走の再現照合(§(a))で見る主要欄。両方の cert に存在するものだけ
# 実際には比較されるが、欠落自体も表に出す(missing はそのまま不一致扱い)。
REPRO_FIELDS = [
    "window_id", "n", "t", "canonical_id_sha256", "N_ord", "charming_count",
    "1_group_order", "2_ker_size", "3_ker_odd_part_order", "4_ker_2_part_order",
    "6_K_struct", "8_chi_image_order", "9_Q_struct_description",
    "11_xi_count_measured", "12_xi_count_bound", "17_H3_holds",
    "20_epsilon_zero", "24_gtsh_idgroup", "settled_fail_count",
    "26_naive_shadow_digest", "27_xi_shadow_digest", "26_eq_27", "shadow_total",
    "stage1_all_pass",
]

# GAP explorer cert のフィールド名 -> checker cert のフィールド名、の対付け
# (裁定216 の規約: 名前は違うが同じ量を測っている)。
PAIR_FIELD_MAP = [
    ("N_ord", "N_ord"),
    ("charming_count", "charming_count"),
    ("11_xi_count_measured", "scanned_count"),
    ("shadow_total", "accepted_count"),
    ("settled_fail_count", "settled_fail_count"),
    ("canonical_id_sha256", ("canonical_id_gate_v2", "recorded_sha256")),
]


def get_nested(obj, key):
    if isinstance(key, tuple):
        cur = obj
        for k in key:
            if not isinstance(cur, dict) or k not in cur:
                return "(missing)"
            cur = cur[k]
        return cur
    return obj.get(key, "(missing)")


def section_a_repro(gap_windows, out_dir_repo):
    """(a) artifact 側 GAP cert <-> repo 収蔵済み同名 GAP cert の再現照合。"""
    lines = []
    lines.append("## (a) 再現照合 -- artifact cert ⟷ repo 収蔵済み cert(同名ファイル)\n")
    lines.append("較正再走の合否: 主要欄が全一致すれば `REPRO_MATCH`、1つでも不一致があれば `REPRO_MISMATCH`。"
                  "volatile 欄(elapsed_sec 等)は参考列で判定には数えない。\n")
    if not gap_windows:
        lines.append("(artifact 内に GAP explorer window cert が見つからなかった)\n")
        return lines, []
    results = []
    for path, obj in gap_windows:
        basename = os.path.basename(path)
        repo_path = os.path.join(out_dir_repo, basename)
        lines.append(f"### {obj.get('window_id', basename)}\n")
        lines.append(f"- artifact: `{path}`")
        if not os.path.isfile(repo_path):
            lines.append(f"- repo baseline: `{repo_path}` -- **見つからない(新規窓 or パス不一致)**\n")
            results.append({"window_id": obj.get("window_id", basename), "verdict": "NO_BASELINE"})
            continue
        repo_obj = load_json(repo_path)
        lines.append(f"- repo baseline: `{repo_path}`\n")
        rows, all_match = field_diff_table(obj, repo_obj, REPRO_FIELDS)
        lines.append("| 欄 | artifact 値 | repo baseline 値 | 一致 |")
        lines.append("|---|---|---|---|")
        for r in rows:
            flag = "(参考)" if r["volatile"] else ("OK" if r["match"] else "**MISMATCH**")
            lines.append(f"| {r['key']} | {r['a']} | {r['b']} | {flag} |")
        verdict = "REPRO_MATCH" if all_match else "REPRO_MISMATCH"
        lines.append(f"\n判定: **{verdict}**\n")
        results.append({"window_id": obj.get("window_id", basename), "verdict": verdict})
    return lines, results


def section_b_pairing(gap_windows, checker_windows):
    """(b) GAP 側 cert ⟷ python checker 側 cert の窓単位対付け集計。"""
    lines = []
    lines.append("## (b) 対付け集計 -- GAP explorer cert ⟷ python checker cert\n")
    checker_by_id = {}
    for path, obj in checker_windows:
        wid = obj.get("window_id")
        if wid:
            checker_by_id[wid] = (path, obj)

    all_wids = sorted({obj.get("window_id") for _, obj in gap_windows if obj.get("window_id")}
                       | set(checker_by_id.keys()))

    if not all_wids:
        lines.append("(対付け対象の窓が見つからなかった)\n")
        return lines, {"agreement": "0/0", "pairs": []}

    lines.append("| 窓 | GAP cert | checker cert | 対付けフィールド一致 | ラベル |")
    lines.append("|---|---|---|---|---|")

    gap_by_id = {}
    for path, obj in gap_windows:
        wid = obj.get("window_id")
        if wid:
            gap_by_id[wid] = (path, obj)

    agree_count = 0
    pair_rows = []
    for wid in all_wids:
        gap_entry = gap_by_id.get(wid)
        chk_entry = checker_by_id.get(wid)
        if gap_entry and chk_entry:
            _, gobj = gap_entry
            _, cobj = chk_entry
            mismatches = []
            for gkey, ckey in PAIR_FIELD_MAP:
                gv = get_nested(gobj, gkey)
                cv = get_nested(cobj, ckey)
                if gv != cv:
                    mismatches.append(f"{gkey}={gv!r} vs {ckey}={cv!r}")
            if not mismatches:
                agree_count += 1
                label = "cross-checked候補(両系統一致)"
                flag = "PASS"
            else:
                label = "両系統に不一致あり(裁定要)"
                flag = "; ".join(mismatches)
            lines.append(f"| {wid} | 有 | 有 | {flag} | {label} |")
            pair_rows.append({"window_id": wid, "both_present": True, "agree": not mismatches, "mismatches": mismatches})
        else:
            which = "GAPのみ" if gap_entry else "checkerのみ"
            lines.append(f"| {wid} | {'有' if gap_entry else '無'} | {'有' if chk_entry else '無'} | -- | candidate({which}) |")
            pair_rows.append({"window_id": wid, "both_present": False, "agree": False, "mismatches": None})

    both = sum(1 for r in pair_rows if r["both_present"])
    lines.append(f"\n`agreement: {agree_count}/{both}`(両系統が揃った窓のうち一致した数。"
                  f"片系統のみの窓は分母に含めない)。全窓数 = {len(all_wids)}。\n")
    lines.append("昇格判断(candidate → cross-checked)は人が行う。本表は集計のみ。\n")

    return lines, {"agreement": f"{agree_count}/{both}", "total_windows": len(all_wids), "pairs": pair_rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact-dir", required=True, help="CI artifact を展開したディレクトリ(dry-run では search/certs で代用可)")
    ap.add_argument("--plan", required=True, help="mine-job/v1 plan JSON へのパス")
    ap.add_argument("--dry-run", action="store_true", help="レポート名に _dryrun を付ける(repo cert を artifact に見立てた自己検収用)")
    args = ap.parse_args()

    plan_path = args.plan
    plan = load_json(plan_path)
    job_id = plan.get("job_id", "unknown-job")
    out_dir_repo = plan.get("outputs", {}).get("out_dir", "search/certs")

    buckets = discover_certs(args.artifact_dir)

    lines = []
    lines.append(f"# mine 検収レポート -- {job_id}\n")
    lines.append(f"- 生成: {datetime.now(timezone.utc).isoformat()}(UTC)")
    lines.append(f"- plan: `{plan_path}`")
    lines.append(f"- artifact-dir: `{args.artifact_dir}`" + ("(dry-run: repo cert を artifact に見立てた自己検収)" if args.dry_run else ""))
    lines.append(f"- claim_class: `{plan.get('claim_class')}`")
    lines.append("")
    lines.append("machine-piped 規約: 本レポートは cert JSON の値のみから生成した。run.log は参照していない。\n")

    a_lines, a_results = section_a_repro(buckets["gap_window"], out_dir_repo)
    b_lines, b_summary = section_b_pairing(buckets["gap_window"], buckets["checker_window"])

    if buckets["unknown"]:
        lines.append(f"## 分類不能な json ({len(buckets['unknown'])} 件 -- artifact-dir 内の無関係な cert。"
                      f"内容は表示しない、パスのみ)\n")
        for item in buckets["unknown"]:
            path = item[0]
            note = item[1] if isinstance(item[1], str) else "(schema/generated_by が本ジョブの様式と一致しない)"
            lines.append(f"- `{path}` {note}")
        lines.append("")

    lines += a_lines
    lines.append("")
    lines += b_lines

    lines.append("## 集計まとめ\n")
    repro_match = sum(1 for r in a_results if r["verdict"] == "REPRO_MATCH")
    repro_total = len(a_results)
    lines.append(f"- 再現照合: {repro_match}/{repro_total} REPRO_MATCH")
    lines.append(f"- 対付け: agreement {b_summary['agreement']}(全窓数 {b_summary.get('total_windows', 0)})")
    lines.append("")
    lines.append("(この集計は候補表記であり、裁定・LEDGER 貼付・地図 delta の確定は人が行う。)")

    os.makedirs(os.path.join(ROOT, "mine", "reports"), exist_ok=True)
    suffix = "_dryrun" if args.dry_run else ""
    out_path = os.path.join(ROOT, "mine", "reports", f"{job_id}_report{suffix}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"WROTE: {out_path}")
    print(f"repro: {repro_match}/{repro_total} REPRO_MATCH; pairing agreement: {b_summary['agreement']}")


if __name__ == "__main__":
    main()
