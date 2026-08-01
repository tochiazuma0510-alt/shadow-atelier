#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/certs/ep_sweep744/assemble_sweep744_cert.py

Merges candidates_744.json + lanea_results_744.json + laneb_results_744.json
by global_index, computes per-point decision-lane concordance
(primary_reason_code match; verdict/stage both REJECT/ACCEPT/INTEGRITY_STOP
family match), and writes the final sweep cert
search/certs/ep_sweep744_20260801.json.

If any point is discordant, the run is NOT halted programmatically here
(all 744 points are cheap and independent) but every discordant point is
isolated into a separate top-level list and the overall summary flags it,
per the commander's instruction ("不一致があれば該当点を隔離記録して停止").
"""

import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def sha256_of_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    cand_path = os.path.join(HERE, "candidates_744.json")
    lanea_path = os.path.join(HERE, "lanea_results_744.json")
    laneb_path = os.path.join(HERE, "laneb_results_744.json")

    with open(cand_path, encoding="utf-8") as f:
        cand_data = json.load(f)
    with open(lanea_path, encoding="utf-8") as f:
        lanea_data = json.load(f)
    with open(laneb_path, encoding="utf-8") as f:
        laneb_data = json.load(f)

    cand_by_idx = {c["global_index"]: c for c in cand_data["candidates"]}
    lanea_by_idx = {r["global_index"]: r["lane_A"] for r in lanea_data["results"]}
    laneb_by_idx = {r["global_index"]: r["lane_B"] for r in laneb_data["results"]}

    assert set(cand_by_idx) == set(lanea_by_idx) == set(laneb_by_idx), "index set mismatch across the three inputs"

    # verdict-family normalization: lane A speaks {"ACCEPT","REJECT","INTEGRITY_STOP", ...},
    # lane B speaks stage in {"REJECT","INTEGRITY_STOP", None(pass-through)}. We compare
    # the raw strings directly where both are populated; lane B's "stage" is the direct
    # analogue of lane A's "verdict" for this comparison.
    points = []
    concordant_count = 0
    discordant = []
    reason_code_dist = {}

    for idx in sorted(cand_by_idx):
        la = lanea_by_idx[idx]
        lb = laneb_by_idx[idx]
        la_err = "error" in la
        lb_err = "error" in lb

        la_verdict = la.get("verdict")
        la_primary = la.get("primary_reason_code")
        lb_stage = lb.get("stage")
        lb_primary = lb.get("primary_reason_code")

        primary_match = (not la_err) and (not lb_err) and (la_primary == lb_primary)
        verdict_family_match = (not la_err) and (not lb_err) and (la_verdict == lb_stage)
        concordant = primary_match and verdict_family_match and not la_err and not lb_err

        if concordant:
            concordant_count += 1
        else:
            discordant.append({
                "global_index": idx,
                "source_file": cand_by_idx[idx]["source_file"],
                "source_local_index": cand_by_idx[idx]["source_local_index"],
                "candidate": cand_by_idx[idx]["candidate"],
                "lane_A": la,
                "lane_B": lb,
            })

        key = f"A={la_primary}|B={lb_primary}"
        reason_code_dist[key] = reason_code_dist.get(key, 0) + 1

        points.append({
            "global_index": idx,
            "source_file": cand_by_idx[idx]["source_file"],
            "source_local_index": cand_by_idx[idx]["source_local_index"],
            "candidate": cand_by_idx[idx]["candidate"],
            "lane_A_verdict": la_verdict,
            "lane_A_primary_reason_code": la_primary,
            "lane_B_stage": lb_stage,
            "lane_B_primary_reason_code": lb_primary,
            "concordant": concordant,
        })

    input_hashes = {
        "search/certs/ep_sweep744/candidates_744.json": sha256_of_file(cand_path),
        "search/certs/ep_sweep744/lanea_results_744.json": sha256_of_file(lanea_path),
        "search/certs/ep_sweep744/laneb_results_744.json": sha256_of_file(laneb_path),
    }

    out = {
        "cert_id": "ep_sweep744_20260801",
        "role_note": "P5 哨戒: 事前登録済み stage1_pass 744候補(bound3全域+bound4の7分割、計8証明書)の全点に対する decision-lane 単発実走(lane A / lane B 独立実装)の concordance 記録。",
        "AUTHORIZATION_BASIS": "Sol の AUTHORIZED 裁定(凍結 schema 下の単発 lane 実走)を、点ごとに 744 回適用したもの。1点ずつの実行内容は search/certs/ep_first_run_20260801.json の候補β単発実走(ep_first_first run, sol_reply_93_math20.md §6 AUTHORIZED)と同型。",
        "EXPLICIT_NON_DECLARATIONS": [
            "この cert は事前登録集合上の decision-lane concordance の記録であり、completeness 宣言ではない。",
            "この cert は「calibrated detector」を宣言しない。",
            "この cert は「fake は存在しない」等の結論を宣言しない。",
            "全ての verdict は partial predicate / UNKNOWN 格のまま(spec v18 §7)。この cert 内の REJECT は各点の decision lane(precondition E-1..E-6 / T-1)による REJECT であり、それ以上でも以下でもない。",
        ],
        "run_mode": "batch_of_unit_runs",
        "complete_search": False,
        "calibrated_detector": False,
        "universe": {
            "description": "certificates/mb/ninfty-branch-search-bound3.json (search_bound=3, a5 in {+-1}) の stage1_pass 全数 + certificates/mb/ninfty-branch-search-bound4-*.json (search_bound=4, 7分割) の stage1_pass 全数。8証明書の合計 = 744 (288+0+114+114+0+114+0+114)、docs/mb/委嘱3_報告.md および docs/notes/ep_first_candidate_design_v1.md の既報値と一致。",
            "source_files_sha256": cand_data["source_files_sha256"],
        },
        "extraction_provenance": {
            "extractor_path": "search/certs/ep_sweep744/extract_sweep744.mjs",
            "extraction_rule": cand_data["extraction_rule"],
        },
        "lane_A_provenance": {
            "entry_point": lanea_data["entry_point"],
            "entry_point_sha256": lanea_data["entry_point_sha256"],
        },
        "lane_B_provenance": {
            "entry_point": laneb_data["entry_point"],
            "entry_point_sha256": laneb_data["entry_point_sha256"],
        },
        "summary": {
            "total_points": len(points),
            "concordant_count": concordant_count,
            "discordant_count": len(discordant),
            "all_concordant": len(discordant) == 0,
            "primary_reason_code_pair_distribution": reason_code_dist,
        },
        "discordant_points": discordant,
        "points": points,
        "input_files_sha256": input_hashes,
        "provenance": {
            "generated_by": "実装担当(shadow-atelier implementer)",
            "generated_at_context": "2026-08-01, P5 哨戒 744点悉皆 concordance 掃射 発注に基づく",
            "machine_piped": "全ての primary_reason_code / verdict / stage / digest 値は本セッションの実コマンド実行結果からの機械貼付(手写しなし)。",
        },
    }

    out_path = os.path.join(ROOT, "search", "certs", "ep_sweep744_20260801.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=True)
        f.write("\n")

    print(json.dumps({
        "total_points": len(points),
        "concordant_count": concordant_count,
        "discordant_count": len(discordant),
        "all_concordant": len(discordant) == 0,
        "primary_reason_code_pair_distribution": reason_code_dist,
        "output": "search/certs/ep_sweep744_20260801.json",
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
