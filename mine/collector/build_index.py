# mine/collector/build_index.py -- certs メモ化索引の構築(v1 最小版・裁定237・
# ideas/ideas_013_solver_platform.md §4.7)。
#
# v1 配管での範囲: 完全な (UID x 述語 x 版 x impl_sha) 鍵は台帳の版管理が入る
# v1 後半に伸ばす(§4.7 本文どおり)。ここでは search/certs/ を走査し、cert
# から抽出できる範囲で (窓 ID または canonical sha, generated_by,
# script_sha256) を集めた索引 JSON を作るところまで。
#
# machine-piped: 索引の値は全て cert JSON の中身から抽出する(人手転記なし)。
# 抽出できなかった cert も欠落として記録する(黙って捨てない)。
#
# preflight/dispatch へのスキップ組込はまだしない(索引の存在と正確さが先、
# §4.7 の順序どおり)。
#
# usage: python mine/collector/build_index.py [--certs-dir search/certs]
#          [--out mine/index/certs_index.json]

import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def extract_generated_by(obj):
    """generated_by は文字列 (例: 'search/strike-r4.g') か
    {'tool':..., 'script':..., 'date':...} 形式のどちらか(cert 様式により
    異なる)。抽出できた素の script パスを 'script' に正規化する。"""
    gb = obj.get("generated_by")
    if isinstance(gb, str):
        return {"raw": gb, "script": gb}
    if isinstance(gb, dict):
        script = gb.get("script") or gb.get("tool")
        return {"raw": gb, "script": script}
    return None


def extract_window_id(obj):
    for key in ("window_id", "wid", "0_canonical_id"):
        v = obj.get(key)
        if isinstance(v, str) and v:
            return v
    return None


def extract_script_sha256(obj):
    v = obj.get("script_sha256")
    if isinstance(v, str) and v:
        return v
    return None


def extract_canonical_sha(obj):
    v = obj.get("canonical_id_sha256")
    if isinstance(v, str) and v:
        return v
    cg = obj.get("canonical_id_gate_v2")
    if isinstance(cg, dict):
        return cg.get("computed_sha256") or cg.get("recorded_sha256")
    return None


def entries_from_obj(obj):
    """1 cert JSON から (window_id/canonical_sha/generated_by/script_sha256)
    のエントリを 0 個以上作る。単一窓 cert は 1 エントリ、多窓 cert
    ('windows' 配列を持つもの -- 梯子/I10 系)は複数エントリ、抽出不能なら
    0 エントリ(呼び出し側が unresolved として数える)。"""
    if not isinstance(obj, dict):
        return []

    top_gb = extract_generated_by(obj)
    top_script_sha = extract_script_sha256(obj)

    wid = extract_window_id(obj)
    canon = extract_canonical_sha(obj)
    if wid or canon:
        return [{
            "window_id": wid,
            "canonical_id_sha256": canon,
            "generated_by": top_gb,
            "script_sha256": top_script_sha,
        }]

    windows = obj.get("windows")
    if isinstance(windows, list) and windows and all(isinstance(w, dict) for w in windows):
        out = []
        for w in windows:
            sub_wid = extract_window_id(w) or w.get("id")
            sub_canon = extract_canonical_sha(w)
            sub_gb = extract_generated_by(w) or top_gb
            sub_script_sha = extract_script_sha256(w) or w.get("cert_sha256") or top_script_sha
            if sub_wid or sub_canon:
                out.append({
                    "window_id": sub_wid,
                    "canonical_id_sha256": sub_canon,
                    "generated_by": sub_gb,
                    "script_sha256": sub_script_sha,
                })
        return out

    return []


def build_index(certs_dir):
    paths = sorted(glob.glob(os.path.join(certs_dir, "*.json")))
    index_entries = []
    unresolved = []
    parse_errors = []

    for path in paths:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        try:
            obj = load_json(path)
        except Exception as e:
            parse_errors.append({"cert_path": rel, "error": str(e)})
            continue
        entries = entries_from_obj(obj)
        if not entries:
            unresolved.append(rel)
            continue
        for e in entries:
            e["cert_path"] = rel
            index_entries.append(e)

    total_certs = len(paths)
    resolved_certs = total_certs - len(unresolved) - len(parse_errors)
    success_rate = (resolved_certs / total_certs) if total_certs else 0.0

    return {
        "schema": "mine-certs-index/v1",
        "note": "search/certs/ の走査索引(窓ID x generated_by の最小版)。preflight/dispatch へのスキップ組込は未実装(索引の正確さが先、§4.7)。",
        "certs_dir": os.path.relpath(certs_dir, ROOT).replace("\\", "/"),
        "total_certs_scanned": total_certs,
        "total_index_entries": len(index_entries),
        "certs_resolved": resolved_certs,
        "certs_unresolved": len(unresolved),
        "certs_parse_error": len(parse_errors),
        "extraction_success_rate": round(success_rate, 4),
        "entries": index_entries,
        "unresolved_certs": unresolved,
        "parse_errors": parse_errors,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certs-dir", default=os.path.join(ROOT, "search", "certs"))
    ap.add_argument("--out", default=os.path.join(ROOT, "mine", "index", "certs_index.json"))
    args = ap.parse_args()

    certs_dir = args.certs_dir if os.path.isabs(args.certs_dir) else os.path.join(ROOT, args.certs_dir)
    out_path = args.out if os.path.isabs(args.out) else os.path.join(ROOT, args.out)

    result = build_index(certs_dir)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"WROTE: {os.path.relpath(out_path, ROOT)}")
    print(f"total_certs_scanned={result['total_certs_scanned']} "
          f"total_index_entries={result['total_index_entries']} "
          f"resolved={result['certs_resolved']} unresolved={result['certs_unresolved']} "
          f"parse_error={result['certs_parse_error']} "
          f"extraction_success_rate={result['extraction_success_rate']}")


if __name__ == "__main__":
    main()
