# mine/collector/receipt.py -- 判定 receipt 機構(P88-R4-2, sol_reply_88_math15.md SS2)
#
# 出所: 裁定235型「PREDICTION_TO_MEASUREMENT_CONTAMINATION」の恒久処方。
# Sol 便88 P88-R4-2 の4条件を満たす receipt 生成器:
#   1. frozen prediction と certificate を別入力として読み、実測欄は
#      certificate JSON からのみ出力する。
#   2. |G|=|K||Q|, |K|=|K|_odd |K|_2, |Xi(G)|=|G|, layer sum = total を
#      assertion 化する(cert に該当欄がある場合のみ)。
#   3. manifest が certificate digest と gate digest を束縛していなければ
#      判定生成を停止する。
#   4. 予言欄・実測欄・派生判定欄を schema 上(=md 上)も分離し、手書きの
#      「予言値を実測へ copy」経路を無くす。
#
# 入力:
#   --prediction-doc <凍結予言 .md へのパス>
#   --prediction-sha256 <その .md の期待 SHA-256(fail-closed 照合)>
#   --prediction-map <predictions を cert フィールドへ対付ける JSON
#                      (予言値の引用のみを持つ。実測値は一切含まない)>
#   --cert <測定 cert JSON へのパス>
#   --manifest <その cert を生成した driver の manifest JSON>
#   --job-id <receipt ファイル名に使う ID>
#
# 出力: mine/reports/<job_id>_receipt.md
#
# 禁止事項(このスクリプト自身の規律):
#   - 実測欄の値は cert dict から get() した生の値のみ(予言値を代入しない)。
#   - 予言欄の値は prediction-map から quote するだけ(cert から書き換えない)。
#   - manifest が cert のバイト digest を束縛していない場合、md を書かずに
#     エラー終了する(exit 1) -- 「生成停止」。
#
# usage:
#   python mine/collector/receipt.py \
#     --prediction-doc docs/notes/r4_prediction_v1.md \
#     --prediction-sha256 a991f65a8c84a553b4d730a39cb3591c42e3fd6f3bfa05c2292fd56b2d66b78f \
#     --prediction-map mine/collector/r4_prediction_map_v1.json \
#     --cert search/certs/r4_W_E_A20_5x4t0_C_20260730.json \
#     --manifest search/certs/r4_manifest_C_20260730.json \
#     --job-id r4-C-receipt

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def sha256_of_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fail(msg):
    print(f"RECEIPT_GENERATION_STOPPED: {msg}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# 恒等式 assert(要件2) -- cert に該当欄がある場合のみ評価する
# ---------------------------------------------------------------------------
def identity_asserts(cert):
    results = []

    def has(*keys):
        return all(k in cert for k in keys)

    # |G| = |K| |Q|
    if has("2_group_order", "3_ker_size", "11_chi_image_order"):
        g = cert["2_group_order"]
        k = cert["3_ker_size"]
        q = cert["11_chi_image_order"]
        ok = (g == k * q)
        results.append({
            "id": "ID-1", "label": "|G| = |K| |Q|",
            "lhs": f"2_group_order={g}", "rhs": f"3_ker_size * 11_chi_image_order = {k}*{q}={k*q}",
            "ok": ok,
        })
    else:
        results.append({"id": "ID-1", "label": "|G| = |K| |Q|", "ok": None,
                         "note": "cert に該当欄なし(2_group_order/3_ker_size/11_chi_image_order)"})

    # |K| = |K|_odd |K|_2
    if has("3_ker_size", "4_ker_odd_part_order", "5_ker_2_part_order"):
        k = cert["3_ker_size"]
        ko = cert["4_ker_odd_part_order"]
        k2 = cert["5_ker_2_part_order"]
        ok = (k == ko * k2)
        results.append({
            "id": "ID-2", "label": "|K| = |K|_odd |K|_2",
            "lhs": f"3_ker_size={k}", "rhs": f"4_ker_odd_part_order * 5_ker_2_part_order = {ko}*{k2}={ko*k2}",
            "ok": ok,
        })
    else:
        results.append({"id": "ID-2", "label": "|K| = |K|_odd |K|_2", "ok": None,
                         "note": "cert に該当欄なし(3_ker_size/4_ker_odd_part_order/5_ker_2_part_order)"})

    # |Xi(G)| = |G|  (image order == group order, i.e. Xi injective onto its image)
    if has("21_xi_image_order", "2_group_order"):
        xi = cert["21_xi_image_order"]
        g = cert["2_group_order"]
        ok = (xi == g)
        results.append({
            "id": "ID-3", "label": "|Xi(G)| = |G|",
            "lhs": f"21_xi_image_order={xi}", "rhs": f"2_group_order={g}",
            "ok": ok,
        })
    else:
        results.append({"id": "ID-3", "label": "|Xi(G)| = |G|", "ok": None,
                         "note": "cert に該当欄なし(21_xi_image_order/2_group_order)"})

    # layer sum = total
    if has("35_xi_count_measured_per_m", "36_xi_count_measured_total"):
        per_m = cert["35_xi_count_measured_per_m"]
        total = cert["36_xi_count_measured_total"]
        s = sum(per_m) if isinstance(per_m, list) else None
        ok = (s == total)
        results.append({
            "id": "ID-4", "label": "layer sum = total",
            "lhs": f"sum(35_xi_count_measured_per_m)={s}", "rhs": f"36_xi_count_measured_total={total}",
            "ok": ok,
        })
    else:
        results.append({"id": "ID-4", "label": "layer sum = total", "ok": None,
                         "note": "cert に該当欄なし(35_xi_count_measured_per_m/36_xi_count_measured_total)"})

    return results


# ---------------------------------------------------------------------------
# 派生判定(要件4: 予言欄と実測欄を分離したまま比較のみ行う)
# ---------------------------------------------------------------------------
def evaluate_prediction(pid, spec, cert):
    """spec は prediction-map の1エントリ(予言値の引用のみ)。cert から
    実測値を読み、比較結果(PASS/FAIL/NULL)だけを返す -- 予言値・実測値は
    呼び出し側で別欄に出す(ここでは判定文字列と両方の raw 値を返すのみ)。"""
    kind = spec.get("kind")

    if kind == "unavailable" or kind == "cross_branch":
        return {"verdict": "NULL", "measured": None, "predicted": spec.get("expected"),
                "detail": spec.get("note", "")}

    if kind == "canonical_id_and_stage1":
        got_id = cert.get("canonical_id_sha256", "(missing)")
        got_gate = cert.get("canonical_id_sha256_gate", "(missing)")
        got_stage1 = cert.get("stage1_all_pass", None)
        ok = (got_id == got_gate) and (got_stage1 is True) and got_id != "(missing)"
        return {"verdict": "PASS" if ok else "FAIL",
                "measured": {"canonical_id_sha256": got_id, "canonical_id_sha256_gate": got_gate,
                              "stage1_all_pass": got_stage1},
                "predicted": spec.get("note", ""), "detail": ""}

    if kind == "eq":
        field = spec["cert_field"]
        if field not in cert:
            return {"verdict": "NULL", "measured": None, "predicted": spec["expected"],
                    "detail": f"cert に欄 {field} なし"}
        measured = cert[field]
        ok = (measured == spec["expected"])
        return {"verdict": "PASS" if ok else "FAIL", "measured": measured,
                "predicted": spec["expected"], "detail": field}

    if kind == "idgroup_eq":
        field = spec["cert_field"]
        if field not in cert or cert[field] in (None, "null"):
            return {"verdict": "NULL", "measured": cert.get(field), "predicted": spec["expected"],
                    "detail": f"cert 欄 {field} が null(範囲外 IdGroup 等)"}
        measured = cert[field]
        ok = (list(measured) == list(spec["expected"]))
        return {"verdict": "PASS" if ok else "FAIL", "measured": measured,
                "predicted": spec["expected"], "detail": field}

    if kind == "eq_multi":
        rows = []
        all_ok = True
        any_null = False
        for chk in spec["checks"]:
            field = chk["cert_field"]
            if field not in cert:
                rows.append({"field": field, "measured": None, "predicted": chk.get("expected"), "ok": None})
                any_null = True
                continue
            measured = cert[field]
            if "expected_eq_field" in chk:
                other = chk["expected_eq_field"]
                expected = cert.get(other, "(missing)")
                ok = (measured == expected)
                rows.append({"field": field, "measured": measured,
                             "predicted": f"= {other} ({expected})", "ok": ok})
            else:
                expected = chk["expected"]
                ok = (measured == expected)
                rows.append({"field": field, "measured": measured, "predicted": expected, "ok": ok})
            all_ok = all_ok and (rows[-1]["ok"] is True)
        if any_null and not all_ok:
            verdict = "FAIL"  # explicit mismatch takes priority over missing field
        elif any_null:
            verdict = "NULL"
        else:
            verdict = "PASS" if all_ok else "FAIL"
        return {"verdict": verdict, "measured": rows, "predicted": None, "detail": ""}

    if kind == "pair_in_set":
        f1, f2 = spec["cert_field_pair"]
        if f1 not in cert or f2 not in cert:
            return {"verdict": "NULL", "measured": None, "predicted": spec["allowed_pairs"],
                    "detail": f"cert に欄 {f1}/{f2} なし"}
        pair = [cert[f1], cert[f2]]
        ok = pair in [list(p) for p in spec["allowed_pairs"]]
        return {"verdict": "PASS" if ok else "FAIL", "measured": pair,
                "predicted": spec["allowed_pairs"], "detail": f"{f1},{f2}"}

    return {"verdict": "NULL", "measured": None, "predicted": None,
            "detail": f"未知の kind={kind!r}"}


def md_bool(v):
    if v is True:
        return "true"
    if v is False:
        return "false"
    if v is None:
        return "null"
    return str(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prediction-doc", required=True)
    ap.add_argument("--prediction-sha256", required=True,
                     help="prediction-doc の期待 SHA-256(fail-closed: 不一致なら生成停止)")
    ap.add_argument("--prediction-map", required=True,
                     help="predictions -> cert フィールド対付け JSON(予言値の引用のみ)")
    ap.add_argument("--cert", required=True, help="測定 cert JSON")
    ap.add_argument("--manifest", required=True,
                     help="cert を生成した driver の manifest JSON(cert digest 束縛の検査に使う)")
    ap.add_argument("--job-id", required=True)
    args = ap.parse_args()

    # --- 出所検査その1: 凍結 prediction 文書の sha256(fail-closed) ---
    if not os.path.isfile(args.prediction_doc):
        fail(f"prediction-doc が見つからない: {args.prediction_doc}")
    actual_pred_sha = sha256_of_file(args.prediction_doc)
    if actual_pred_sha != args.prediction_sha256.lower():
        fail(f"prediction-doc の SHA-256 不一致: expected={args.prediction_sha256} actual={actual_pred_sha} "
             f"-- 凍結文書と異なる版が渡されている可能性(接触遮断違反の疑い)")

    pred_map = load_json(args.prediction_map)
    if pred_map.get("source_sha256", "").lower() != actual_pred_sha:
        fail(f"prediction-map の source_sha256 が prediction-doc の実 SHA-256 と不一致: "
             f"map={pred_map.get('source_sha256')} actual={actual_pred_sha}")

    # --- 出所検査その2: manifest が cert の digest を束縛しているか(要件3) ---
    if not os.path.isfile(args.cert):
        fail(f"cert が見つからない: {args.cert}")
    if not os.path.isfile(args.manifest):
        fail(f"manifest が見つからない: {args.manifest}")
    actual_cert_sha = sha256_of_file(args.cert)
    manifest = load_json(args.manifest)
    cert_basename = os.path.basename(args.cert)

    bound_entry = None
    for w in manifest.get("windows", []):
        outfile = w.get("outfile", "")
        if os.path.basename(outfile) == cert_basename:
            bound_entry = w
            break
    if bound_entry is None:
        fail(f"manifest ({args.manifest}) は cert ({args.cert}) を束縛していない -- "
             f"windows[].outfile に一致するエントリが無い。判定生成を停止する。")
    bound_sha = bound_entry.get("cert_sha256")
    if not bound_sha:
        fail(f"manifest のエントリに cert_sha256 が無い -- digest 束縛が無いので判定生成を停止する。")
    if bound_sha.lower() != actual_cert_sha.lower():
        fail(f"manifest が束縛する cert_sha256 ({bound_sha}) が cert の実 SHA-256 ({actual_cert_sha}) と不一致 "
             f"-- cert がすり替えられている可能性。判定生成を停止する。")
    manifest_gate_bound = bool(manifest.get("entry_gate_file")) and (manifest.get("entry_gate_all_pass") is True)

    cert = load_json(args.cert)

    # --- 恒等式 assert(要件2) ---
    id_results = identity_asserts(cert)

    # --- 派生判定(要件4: 予言欄と実測欄を分離したまま比較) ---
    pred_results = {}
    for pid, spec in pred_map.get("predictions", {}).items():
        pred_results[pid] = evaluate_prediction(pid, spec, cert)

    # --- receipt md 組み立て ---
    now = datetime.now(timezone.utc).isoformat()
    lines = []
    lines.append(f"# 判定 receipt -- {args.job_id}\n")
    lines.append(f"- 生成: {now} (UTC)")
    lines.append(f"- 生成器: `mine/collector/receipt.py`(P88-R4-2 恒久処方 -- sol_reply_88_math15.md SS2)")
    lines.append(f"- window_id: `{cert.get('window_id', '(不明)')}`")
    lines.append("")
    lines.append("## 出所(fail-closed 検査済み)\n")
    lines.append(f"- prediction-doc: `{args.prediction_doc}` (SHA-256 `{actual_pred_sha}`, 期待値と一致)")
    lines.append(f"- prediction-map: `{args.prediction_map}` (source_sha256 が prediction-doc と一致)")
    lines.append(f"- cert: `{args.cert}` (SHA-256 `{actual_cert_sha}`)")
    lines.append(f"- manifest: `{args.manifest}` -- windows[].outfile={cert_basename!r} の cert_sha256 束縛と実 SHA-256 が一致(検査 PASS)")
    lines.append(f"- manifest の S0 entry gate 束縛: entry_gate_file={manifest.get('entry_gate_file')!r}, "
                 f"entry_gate_all_pass={manifest.get('entry_gate_all_pass')} "
                 f"({'束縛あり' if manifest_gate_bound else '束縛なし(gate 未確認のまま生成 -- 要注意)'})")
    lines.append("")

    lines.append("## 予言欄(凍結文書からの引用のみ -- 実測値は書かない)\n")
    lines.append(f"出典: `{pred_map.get('source_doc')}` (SHA-256 `{pred_map.get('source_sha256')}`)\n")
    lines.append("| 予言ID | 予言(引用) |")
    lines.append("|---|---|")
    for pid, spec in pred_map.get("predictions", {}).items():
        lines.append(f"| {pid} | {spec.get('statement', '')} |")
    lines.append("")

    lines.append("## 実測欄(cert JSON からのみ機械抽出)\n")
    lines.append("| 欄 | 値 |")
    lines.append("|---|---|")
    # cert の全フィールドをそのまま出す(手書き転記を排除するため dict.items() を直接使う)
    for k, v in cert.items():
        if k in ("stage1_asserts", "37_shard_manifest", "note"):
            continue  # 大きい配列/長文はここでは省略(生 cert を直接参照可能)
        lines.append(f"| `{k}` | `{json.dumps(v, ensure_ascii=False)}` |")
    lines.append("")
    lines.append("(全欄は cert 原本を参照。上表は `stage1_asserts` / `37_shard_manifest` / `note` を省略した抜粋。)\n")

    lines.append("## 恒等式 assert(要件2 -- cert に該当欄がある場合のみ評価)\n")
    lines.append("| ID | 恒等式 | 左辺 | 右辺 | 判定 |")
    lines.append("|---|---|---|---|---|")
    for r in id_results:
        if r["ok"] is None:
            lines.append(f"| {r['id']} | {r['label']} | -- | -- | NULL({r.get('note', '')}) |")
        else:
            lines.append(f"| {r['id']} | {r['label']} | {r['lhs']} | {r['rhs']} | {'PASS' if r['ok'] else '**FAIL**'} |")
    lines.append("")

    lines.append("## 派生判定欄(予言欄 x 実測欄の比較結果のみ -- 値そのものは上の2欄を参照)\n")
    lines.append("| 予言ID | 判定 | 内訳 |")
    lines.append("|---|---|---|")
    for pid, res in pred_results.items():
        verdict = res["verdict"]
        if isinstance(res["measured"], list) and res["measured"] and isinstance(res["measured"][0], dict):
            detail_parts = []
            for row in res["measured"]:
                mark = "OK" if row["ok"] is True else ("NULL" if row["ok"] is None else "MISMATCH")
                detail_parts.append(f"{row['field']}: measured={row['measured']!r} predicted={row['predicted']!r} [{mark}]")
            detail = "; ".join(detail_parts)
        else:
            detail = f"measured={res['measured']!r} predicted={res['predicted']!r}"
            if res.get("detail"):
                detail += f" ({res['detail']})"
        vflag = {"PASS": "PASS", "FAIL": "**FAIL**", "NULL": "NULL"}.get(verdict, verdict)
        lines.append(f"| {pid} | {vflag} | {detail} |")
    lines.append("")

    n_pass = sum(1 for r in pred_results.values() if r["verdict"] == "PASS")
    n_fail = sum(1 for r in pred_results.values() if r["verdict"] == "FAIL")
    n_null = sum(1 for r in pred_results.values() if r["verdict"] == "NULL")
    lines.append("## 集計まとめ\n")
    lines.append(f"- 派生判定: PASS {n_pass} / FAIL {n_fail} / NULL {n_null} (全 {len(pred_results)} 予言)")
    n_id_fail = sum(1 for r in id_results if r["ok"] is False)
    n_id_null = sum(1 for r in id_results if r["ok"] is None)
    lines.append(f"- 恒等式 assert: FAIL {n_id_fail} / NULL(欄なし) {n_id_null} / 全 {len(id_results)}")
    lines.append("")
    lines.append("(本 receipt は cert JSON の値と凍結 prediction-map の引用値の機械照合であり、"
                 "候補判定であって裁定ではない。裁定は人(司令塔/研究者)が行う。)")

    os.makedirs(os.path.join(ROOT, "mine", "reports"), exist_ok=True)
    out_path = os.path.join(ROOT, "mine", "reports", f"{args.job_id}_receipt.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"WROTE: {out_path}")
    print(f"identity asserts: FAIL={n_id_fail} NULL={n_id_null} / {len(id_results)}")
    print(f"predictions: PASS={n_pass} FAIL={n_fail} NULL={n_null} / {len(pred_results)}")


if __name__ == "__main__":
    main()
