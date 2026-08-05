#!/usr/bin/env python3
"""
search/probe/w6_bu_s0/conventions_diff_v2_1.py -- 裁定543【要修正B】の履行確認:
GAP cert (search/certs/w6_bu_s0_iso_gate_r3r4_v2_1_20260805.json) と Python
第二系統 output (search/probe/w6_bu_s0/r4_second_system_output_v2_1.json) の
conventions_used ブロックを実際に機械 diff し、司令塔指定の 5 項目
(perm_composition, abstract_prod_reversal, word_eval,
h10_fail_bookkeeping_unit, comparison_target) が一致することを確認する。

This is the CV-9-2 副検問 that v1/v2 could not perform (0/5 diffable per
falsifier's iso_r3r4_cv9_reading_v2.md sec.1(b)). Result is written to
search/probe/w6_bu_s0/conventions_diff_v2_1_result.json.
"""
import json

REQUIRED_KEYS = [
    "perm_composition",
    "abstract_prod_reversal",
    "word_eval",
    "h10_fail_bookkeeping_unit",
    "comparison_target",
]


def main():
    with open("search/certs/w6_bu_s0_iso_gate_r3r4_v2_1_20260805.json", encoding="utf-8") as f:
        gap_cert = json.load(f)
    with open("search/probe/w6_bu_s0/r4_second_system_output_v2_1.json", encoding="utf-8") as f:
        py_cert = json.load(f)

    gap_cu = gap_cert["conventions_used"]
    py_cu = py_cert["conventions_used"]

    results = {}
    all_match = True
    for key in REQUIRED_KEYS:
        gap_present = key in gap_cu
        py_present = key in py_cu
        if not (gap_present and py_present):
            results[key] = {"match": False, "reason": f"absent: gap={gap_present} python={py_present}"}
            all_match = False
            continue
        gap_val = gap_cu[key]
        py_val = py_cu[key]
        gap_type = type(gap_val).__name__
        py_type = type(py_val).__name__
        if gap_type != py_type:
            results[key] = {"match": False, "reason": f"type mismatch: gap={gap_type} python={py_type}"}
            all_match = False
            continue
        match = (gap_val == py_val)
        results[key] = {"match": match, "gap_value": gap_val, "python_value": py_val}
        if not match:
            all_match = False

    print("=== conventions_used machine diff (5 required keys) ===")
    for key in REQUIRED_KEYS:
        r = results[key]
        print(f"  {key}: {'MATCH' if r['match'] else 'MISMATCH'}"
              + ("" if r["match"] else f"  ({r.get('reason', '')})"))

    # also check grading_prohibitions (軽微F: same path, byte-identical text)
    gap_gp = gap_cu.get("grading_prohibitions")
    py_gp = py_cu.get("grading_prohibitions")
    grading_prohibitions_match = (gap_gp == py_gp)
    print(f"  grading_prohibitions (same path, both inside conventions_used): "
          f"{'MATCH' if grading_prohibitions_match else 'MISMATCH'}")

    out = {
        "schema": "gtsh-cert/iso-gate-r3r4-conventions-diff/v1",
        "purpose": "commander 裁定543 要修正B verification: machine-diff the 5 required conventions_used keys between the GAP cert v2.1 and the Python second-system output v2.1",
        "required_keys": REQUIRED_KEYS,
        "results": results,
        "all_5_keys_match": all_match,
        "grading_prohibitions_match": grading_prohibitions_match,
        "diffable_count": f"{sum(1 for r in results.values() if r['match'])}/5",
    }
    with open("search/probe/w6_bu_s0/conventions_diff_v2_1_result.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"\ndiffable_count = {out['diffable_count']}  all_5_keys_match = {all_match}  "
          f"grading_prohibitions_match = {grading_prohibitions_match}")
    print("wrote search/probe/w6_bu_s0/conventions_diff_v2_1_result.json")
    assert all_match, "NOT all 5 required conventions_used keys machine-diff as matching"
    assert grading_prohibitions_match, "grading_prohibitions text is not byte-identical"


if __name__ == "__main__":
    main()
