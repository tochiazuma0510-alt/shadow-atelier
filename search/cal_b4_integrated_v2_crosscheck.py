#!/usr/bin/env python3
"""
cal_b4_integrated_v2_crosscheck.py -- independent checker for
search/certs/cal_b4_integrated_v2_20260806.json.

Discipline (探索器と照合器の分離, CLAUDE.md): reads ONLY the committed cert
JSON. Does NOT import build_integrated_cert_v2.py, does NOT open the GAP
logs, does NOT re-run GAP. Recomputes self-evident arithmetic facts in pure
Python and verifies the cert's own PASS/FAIL/status flags and *_unit
annotations are internally consistent. Cross-checking, not verification
(Lean is reserved for "verified").

Exit code 0 iff no problems found.
"""
import json
import sys

CERT_PATH = "search/certs/cal_b4_integrated_v2_20260806.json"


def main():
    with open(CERT_PATH, encoding="utf-8") as f:
        cert = json.load(f)

    problems = []

    def check(cond, msg):
        if not cond:
            problems.append(msg)

    # --- schema / unit-declaration convention shape ---
    check(cert.get("schema") == "cal-b4-integrated/v2", "schema field mismatch")
    check("unit_declaration_convention" in cert, "missing unit_declaration_convention field (裁定674 requirement)")

    # --- every numeric leaf that has a sibling "<key>_expected" must also have a sibling "<key>_unit" ---
    def find_unit_gaps(node, path=""):
        if isinstance(node, dict):
            keys = set(node.keys())
            for k, v in node.items():
                if k.endswith("_expected") and not k.endswith("_unit_expected"):
                    base = k[: -len("_expected")]
                    if f"{base}_unit" not in keys and base not in ("pending_items",):
                        problems.append(f"unit-declaration gap: {path}.{k} has no sibling '{base}_unit' "
                                         f"(裁定674 requires every measured quantity to declare its unit)")
                if isinstance(v, dict):
                    find_unit_gaps(v, f"{path}.{k}" if path else k)

    find_unit_gaps(cert)

    for key in ["cal_b4_log", "p1_log"]:
        src = cert.get("sources", {}).get(key)
        check(src is not None, f"sources.{key} missing")
        if src is not None:
            check(isinstance(src.get("sha256"), str) and len(src["sha256"]) == 64,
                  f"sources.{key}.sha256 missing or malformed")
    check(cert["sources"]["cal_b4_log"]["gha_run_id"] == "31084038955",
          "cal_b4_log gha_run_id is not 31084038955 -- wrong source for v2")

    # --- C-1 ---
    c1 = cert["C1"]
    check(c1["idx_B4_PB4"] == c1["idx_B4_PB4_expected"] == 24, "C1: idx_B4_PB4 != 24")
    check(c1["convention_guard_bad_relators"] == 0, "C1: convention-guard reports nonzero bad relators")
    check(c1["image_psi_size"] == c1["idx_PB4fp_N19"] == 216, "C1: index values disagree or are not 216")
    check(c1["pass"] == (c1["image_psi_size"] == 216 and c1["idx_PB4fp_N19"] == 216),
          "C1: pass flag inconsistent")

    # --- C-2/C-3a/C-3b ---
    c2, c3a, c3b = cert["C2"], cert["C3a"], cert["C3b"]
    check(c2["pass"] == (c2["N_ord"] == c2["N_ord_expected"]), "C2: pass flag inconsistent")
    check(c3a["pass"] == (c3a["idx_F2_NF2"] == c3a["idx_F2_NF2_expected"]), "C3a: pass flag inconsistent")
    check(c3b["pass"] == (c3b["commutator_order"] == c3b["commutator_order_expected"]), "C3b: pass flag inconsistent")
    check(c3a["idx_F2_NF2"] % c3b["commutator_order"] == 0, "C3a/C3b: Lagrange violation")
    check(c3a["idx_F2_NF2"] // c3b["commutator_order"] == 36, "C3a/C3b: [P19:[P19,P19]] != 36")

    # --- C-4 ---
    c4 = cert["C4"]
    prim, cross = c4["primary_method"]["pentagon_pass_count"], c4["cross_method"]["pentagon_pass_count"]
    check(prim == cross == 216, "C4: methods disagree or not 216")

    # --- C-5 ---
    c5 = cert["C5"]
    check(c5["pair_count"] == 72 and c5["distinct_f"] == 36, "C5: not at expected values")
    check(c5["pair_count"] == 2 * c5["distinct_f"], "C5: pair_count != 2*distinct_f (uniform [[2,36]] distribution)")

    # --- C-6 first half ---
    c6a = cert["C6_first_half"]
    check(c6a["value"] == c5["pair_count"], "C6_first_half: value != C5.pair_count")
    check(c6a["pass"] == (c6a["value"] == c6a["expected"]), "C6_first_half: pass flag inconsistent")

    # --- C-6b (dual-unit, 裁定674's central fix) ---
    c6b = cert["C6b_second_half"]
    check(c6b["status"] == "COMPUTED", "C6b: status is not COMPUTED -- expected an actual result in v2")
    check(c6b["derived_subgroup_order"] == 216, "C6b: derived_subgroup_order != 216")
    check(c6b["f_count"] == 6, "C6b: f_count != 6")
    check(c6b["pair_count"] == 12, "C6b: pair_count != 12")
    check(c6b["pair_count"] == c6b["f_count"] * 2,
          "C6b: pair_count != f_count * 2 -- inconsistent with the uniform per-f good-m distribution "
          "[[2,36]] recorded in C5 (every f has exactly 2 good m, so a 6-f subset should give 12 pairs)")
    check(c6b["pass"] == (c6b["derived_subgroup_order"] == 216 and c6b["f_count"] == 6 and c6b["pair_count"] == 12),
          "C6b: pass flag inconsistent with its own recorded dual-unit values")

    # --- C-6c ---
    c6c = cert["C6c"]
    check(c6c["total_count"] == c6c["total_count_expected"] == 12, "C6c: total_count != 12")
    check(c6c["pass_count"] == c6c["total_count"], "C6c: pass_count != total_count despite pass=true possibility")
    check(c6c["pass"] == (c6c["pass_count"] == c6c["total_count"] == 12), "C6c: pass flag inconsistent")

    # --- C-6d ---
    c6d = cert["C6d"]
    check(c6d["total_count"] == c6d["total_count_expected"] == 6, "C6d: total_count != 6")
    check(c6d["pass"] == (c6d["pass_count"] == c6d["total_count"] == 6), "C6d: pass flag inconsistent")

    # --- C-6e (recommended) ---
    c6e = cert["C6e"]
    check(c6e["products_total"] == c6e["products_total_expected"] == 144,
          "C6e: products_total != 144 (should be 12*12 for a 12-element multiplication table)")
    check(c6e["closure_fail_count"] == 0, "C6e: closure_fail_count != 0 despite a claimed clean run")
    check(c6e["reconstructed_group_order"] == c6e["reconstructed_group_order_expected"] == 12,
          "C6e: reconstructed_group_order != 12")
    check(c6e["pass"] == (c6e["closure_fail_count"] == 0 and c6e["reconstructed_group_order"] == 12
                           and c6e["isomorphic_to_D6"] is True),
          "C6e: pass flag inconsistent with its own recorded closure/order/isomorphism fields")

    # --- P1 ---
    p1 = cert["P1"]
    seven_41 = 7 ** 41
    check(int(p1["R_size_decimal"]) == int(p1["R_size_expected_decimal"]) == seven_41,
          "P1: R_size does not match independently recomputed 7**41")
    check(p1["B4_EXQ1_pass"] == (int(p1["R_size_decimal"]) == seven_41), "P1: B4_EXQ1_pass flag inconsistent")
    check(p1["B4_EXQ2_status"] == "CRASHED_OOM_INCOMPLETE", "P1: B4_EXQ2_status narrative changed unexpectedly")

    # --- C-8 (must not claim adoption of the waiver) ---
    c8 = cert["C8"]
    check(c8["status"] == "SKIP", "C8: status is not SKIP")
    check("PASS" not in c8["status"], "C8: status field contains PASS -- forbidden for a SKIP job")
    check("弱い代替 gate は採用しない" in c8["waiver_ruling"] or "採用しない" in c8["waiver_ruling"],
          "C8: waiver_ruling does not record 裁定674's rejection of the weak waiver gate -- possible "
          "premature/incorrect adoption")
    check("便113" in c8["waiver_ruling"] or "113" in c8["waiver_ruling"],
          "C8: waiver_ruling does not defer the adoption question to Sol via 便113")

    # --- overall: recompute both aggregate flags independently ---
    overall = cert["overall"]
    required_flags = [c1["pass"], c2["pass"], c3a["pass"], c3b["pass"],
                       c4["primary_method"]["pass"], c4["cross_method"]["pass"],
                       c5["both_units_pass"], c6a["pass"], c6b["pass"], c6c["pass"], c6d["pass"],
                       p1["B4_EXQ1_pass"]]
    recomputed_required = all(required_flags)
    recomputed_including_recommended = recomputed_required and c6e["pass"]
    check(overall["all_required_checks_pass"] == recomputed_required,
          f"overall.all_required_checks_pass ({overall['all_required_checks_pass']}) does not match "
          f"independently recomputed conjunction ({recomputed_required})")
    check(overall["all_checks_including_recommended_pass"] == recomputed_including_recommended,
          f"overall.all_checks_including_recommended_pass ({overall['all_checks_including_recommended_pass']}) "
          f"does not match independently recomputed conjunction ({recomputed_including_recommended})")
    check("C6e" in overall.get("computed_checks", []), "overall.computed_checks does not list C6e")
    check(len(overall["pending_items"]) >= 2, "overall.pending_items has fewer than the 2 known-pending items (P1.B4_EXQ2, C8)")
    check(any("C8" in p for p in overall["pending_items"]), "overall.pending_items does not mention C8")
    check(any("B4_EXQ2" in p or "EXQ2" in p for p in overall["pending_items"]),
          "overall.pending_items does not mention P1.B4_EXQ2")

    result = {
        "schema": "cal-b4-integrated-v2-crosscheck/v1",
        "cert_checked": CERT_PATH,
        "problems": problems,
        "MATCH": len(problems) == 0,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    with open("search/certs/cal_b4_integrated_v2_crosscheck_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
