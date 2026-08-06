#!/usr/bin/env python
# search/probe/w6_bu_s1_s3/merge_s35_v2_2_shards.py
# Merges the 3 shard outputs of w6_bu_s35_driver_v2_2.g (Sol 便112 F112-1/R-1
# minimal repair, 裁定637) into the single S3.5 v2.2 companion report.
# Concatenation + re-sum only -- no group theory recomputed here (search/
# crosscheck separation). v2.1 driver/cert are UNCHANGED (v2.2 laid
# alongside, per the recommended minimal repair).
import json, hashlib, sys

SHARDS = [
    "search/certs/w6_bu_s35_v2_2_20260806_shardA.json",
    "search/certs/w6_bu_s35_v2_2_20260806_shardB.json",
    "search/certs/w6_bu_s35_v2_2_20260806_shardC.json",
]
OUT = "search/certs/w6_bu_s35_v2_2_20260806.json"

EXPECTED_ROW_ORDER = [
  "p2_d4_a0b0c2", "p2_d2_a0b0c1", "p2_d2_a0b1c0", "p2_d2_a2b0c0",
  "p2_d3_a1b0c1", "p2_d3_a1b1c0", "p2_d3_a3b0c0",
  "p2_d4_a0b1c1", "p2_d4_a0b2c0", "p2_d4_a2b0c1", "p2_d4_a2b1c0",
  "p2_d4_a4b0c0",
  "p3_d2_bruteforce_1", "p3_d2_bruteforce_2", "p3_d2_bruteforce_3",
  "p3_d2_bruteforce_4", "p3_d2_bruteforce_5",
]

def sha256_of_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def main():
    docs = [json.load(open(p, encoding="utf-8")) for p in SHARDS]
    shard_file_shas = [sha256_of_file(p) for p in SHARDS]

    all_rows = []
    for d in docs:
        all_rows.extend(d["rows"])
    by_id = {r["module_id"]: r for r in all_rows}
    missing = [m for m in EXPECTED_ROW_ORDER if m not in by_id]
    extra = [m for m in by_id if m not in EXPECTED_ROW_ORDER]
    if missing:
        print("MERGE_FAIL: missing rows:", missing); sys.exit(1)
    if extra:
        print("MERGE_FAIL: unexpected extra rows:", extra); sys.exit(1)
    ordered_rows = [by_id[m] for m in EXPECTED_ROW_ORDER]

    total_classes = sum(r["num_classes"] for r in ordered_rows)
    accepted = sum(r["accepted_classes"] for r in ordered_rows)
    rejected = sum(r["rejected_classes"] for r in ordered_rows)
    affine_pairs = sum(r["affine_solution_pairs"] for r in ordered_rows)
    l3 = sum(r["L3_surjective_lifts"] for r in ordered_rows)
    mark_iso = sum(r["MARK_ISO_orbits"] for r in ordered_rows)

    fails_total = sum(d["fails_total"] for d in docs)
    all_fails = []
    for d in docs:
        all_fails.extend(d["fails"])

    def and_across(key_path):
        vals = []
        for d in docs:
            node = d
            for k in key_path:
                node = node[k]
            vals.append(bool(node))
        return all(vals)

    size_phat_ok = and_across(["phat_construction", "sanity_checks_passed", "size_Phat_eq_3000_times_V"])
    pie_ok = and_across(["phat_construction", "sanity_checks_passed", "piE_U0_eq_theta_and_piE_W0_eq_tau"])
    order_ok = and_across(["phat_construction", "sanity_checks_passed", "order_Uhat0_times_What0_matches_or_doubles_Ghat5_reference"])
    f1_ok = and_across(["f_fixtures", "F_1_all_pass"])
    f21_ok = and_across(["f_fixtures", "F_2_1_sigma1sq_eq_x"])
    f22_ok = and_across(["f_fixtures", "F_2_2_sigma2sq_eq_y"])
    f25_makegn_ok = and_across(["f_fixtures", "F_2_5_makegn_basis_pass"])
    f26_makegn_ok = and_across(["f_fixtures", "F_2_6_makegn_basis_pass"])
    f25_canon_ok = and_across(["f_fixtures", "F_2_5_canon_basis_pass"])
    f26_canon_ok = and_across(["f_fixtures", "F_2_6_canon_basis_pass"])
    f25_ok = and_across(["f_fixtures", "F_2_5_pass"])
    f26_ok = and_across(["f_fixtures", "F_2_6_pass"])
    f35_ok = and_across(["f_fixtures", "F_3_5_negative_fixture_pass"])
    block_basis_eq_amod_ok = and_across(["f_fixtures", "v2_2_block_basis_eq_Amod"])

    merged_check_names = []
    seen_global = set()
    GLOBAL_PREFIXES = ("F-1.", "F-2.", "F-3.5", "A:", "v2.2:")
    for d in docs:
        for name in d["check_semantics"]["checks_executed_names"]:
            if any(name.startswith(p) for p in GLOBAL_PREFIXES):
                if name in seen_global:
                    continue
                seen_global.add(name)
            merged_check_names.append(name)
    checks_total = len(merged_check_names)

    dpd_doc = None
    for d in docs:
        if d.get("lane_a_lane_b_dpd_only", {}).get("dpd_classes"):
            dpd_doc = d
            break
    dpd_block = dpd_doc["lane_a_lane_b_dpd_only"] if dpd_doc else None

    base = docs[0]

    merged = {
        "schema": "w6-bu-s35-v2.2-cert/v1",
        "note": base["note"] + " [MERGED from 3 shards: shardA(11 rows incl. D+D)+shardB(p2_d4_a4b0c0)+shardC(5 p3 rows) -- sharded per gaplib_common.g 600s wall-clock convention; merge is concatenation + re-sum + AND-reduce only, see merge_s35_v2_2_shards.py. v2.1 driver/cert are UNCHANGED (predecessor, laid alongside).]",
        "design_doc": base["design_doc"],
        "authorization": base["authorization"],
        "predecessor_unchanged": "search/certs/w6_bu_s35_v2_1_20260806.json",
        "shard_provenance": [
            {"path": p, "shard_output_sha256": sha, "driver_self_sha256": d["driver_self_sha256"], "fails_total": d["fails_total"]}
            for p, sha, d in zip(SHARDS, shard_file_shas, docs)
        ],
        "counts_v2": {
            "extension_classes": total_classes,
            "affine_solvable_classes": accepted,
            "affine_unsolvable_classes": rejected,
            "affine_solution_pairs": affine_pairs,
            "L3_surjective_lifts": l3,
            "MARK_ISO_orbits": mark_iso,
            "full_v_squared_pair_domain": 91809,
            "unit_definitions": base["counts_v2"]["unit_definitions"],
        },
        "phat_construction": {
            "method": base["phat_construction"]["method"],
            "sanity_checks_passed": {
                "size_Phat_eq_3000_times_V": size_phat_ok,
                "piE_U0_eq_theta_and_piE_W0_eq_tau": pie_ok,
                "order_Uhat0_times_What0_matches_or_doubles_Ghat5_reference": order_ok,
                "note": base["phat_construction"]["sanity_checks_passed"]["note"] + " [AND-reduced across all 3 shards by this merge step]",
            },
            "known_slow_step_avoided": base["phat_construction"]["known_slow_step_avoided"],
        },
        "f_fixtures": {
            "F_1_all_pass": f1_ok,
            "F_2_1_sigma1sq_eq_x": f21_ok,
            "F_2_2_sigma2sq_eq_y": f22_ok,
            "F_2_5_F_2_6_v2_2_method": base["f_fixtures"]["F_2_5_F_2_6_v2_2_method"],
            "v2_2_block_basis_eq_Amod": block_basis_eq_amod_ok,
            "v2_2_declared_basis_native": base["f_fixtures"]["v2_2_declared_basis_native"],
            "v2_2_Ad_Delta_MakeGn_basis": base["f_fixtures"]["v2_2_Ad_Delta_MakeGn_basis"],
            "v2_2_Ad_delta_MakeGn_basis": base["f_fixtures"]["v2_2_Ad_delta_MakeGn_basis"],
            "v2_2_Theta_canon": base["f_fixtures"]["v2_2_Theta_canon"],
            "v2_2_T_canon": base["f_fixtures"]["v2_2_T_canon"],
            "v2_2_d_basis_change": base["f_fixtures"]["v2_2_d_basis_change"],
            "v2_2_dTd_MakeGn_expected": base["f_fixtures"]["v2_2_dTd_MakeGn_expected"],
            "v2_2_Ad_Delta_canon_basis_via_simultaneous_d": base["f_fixtures"]["v2_2_Ad_Delta_canon_basis_via_simultaneous_d"],
            "v2_2_Ad_delta_canon_basis_via_simultaneous_d": base["f_fixtures"]["v2_2_Ad_delta_canon_basis_via_simultaneous_d"],
            "F_2_5_makegn_basis_pass": f25_makegn_ok, "F_2_6_makegn_basis_pass": f26_makegn_ok,
            "F_2_5_canon_basis_pass": f25_canon_ok, "F_2_6_canon_basis_pass": f26_canon_ok,
            "F_2_5_ad_Delta_basis_match": base["f_fixtures"]["F_2_5_ad_Delta_basis_match"],
            "F_2_6_ad_delta_basis_match": base["f_fixtures"]["F_2_6_ad_delta_basis_match"],
            "F_2_5_pass": f25_ok, "F_2_6_pass": f26_ok,
            "F_3_5_negative_fixture_pass": f35_ok,
            "F_3_5_v2_2_note": base["f_fixtures"]["F_3_5_v2_2_note"],
            "fixture_naming_map": base["f_fixtures"]["fixture_naming_map"],
        },
        "check_semantics": {
            "note": base["check_semantics"]["note"],
            "checks_executed_total": checks_total,
            "checks_executed_names": merged_check_names,
            "fails_total_denominator": base["check_semantics"]["fails_total_denominator"],
        },
        "lane_a_lane_b_dpd_only": dpd_block,
        "rows": ordered_rows,
        "L3_zero_disclosure": {
            "note": base["L3_zero_disclosure"]["note"],
            "needs_mathematical_review": (l3 == 0),
            "review_tag": "【要数学検分】",
            "candidate_theorem_note": base["L3_zero_disclosure"]["candidate_theorem_note"],
            "SM_1": base["L3_zero_disclosure"]["SM_1"],
            "per_row_L3_surjective_lifts": {r["module_id"]: r["L3_surjective_lifts"] for r in ordered_rows},
            "rows_with_nonzero_L3": [r["module_id"] for r in ordered_rows if r["L3_surjective_lifts"] > 0],
            "rows_with_zero_L3": [r["module_id"] for r in ordered_rows if r["L3_surjective_lifts"] == 0],
        },
        "claims": {"isolated_verdict": "UNKNOWN", "kill_claim": False, "candidate_found": False, "empty_claim": False},
        "non_contact_declaration": {"exploration": False, "candidate_generation": False, "kill": False,
                                     "empty_theorem": False, "im_R": False, "d_N": False,
                                     "sealed_quantities": False, "S9": False},
        "fails_total": fails_total,
        "fails": all_fails,
        "denominator_check": {
            "extension_classes_449": total_classes == 449,
            "affine_solvable_73": accepted == 73,
            "affine_unsolvable_376": rejected == 376,
            "affine_solution_pairs_1263": affine_pairs == 1263,
        },
        "v2_2_repair_record": {
            "authority": "裁定637 (司令塔), sol/sol_reply_112_math38.md F112-1/R-1 推奨する小修理",
            "predecessor": "search/certs/w6_bu_s35_v2_1_20260806.json (UNCHANGED, laid alongside)",
            "items_fixed": [
                "(1) F-2.5/F-2.6: replaced charpoly-similarity check with DIRECT MATRIX EQUALITY over GF(5) in the explicit MakeGn block basis A=<tr(r,1),tr(r,2),tr(r,3)> (verified = Amod exactly), PLUS an explicit SIMULTANEOUS change-of-basis d=diag(1,1,-1) applied to both Ad(Delta) and Ad(delta) together, confirming the canon-basis equalities too. Both bases' equalities checked entrywise, not via characteristic polynomial.",
                "(2) F-3.5: added lane B (|V|^2=16 exhaustive pair enumeration, direct matrix test, no SolveAffine) alongside lane A on the negative fixture, confirming n_A=n_B=0 on BOTH lanes as bu_s35_embedding_v1.md SS8 F-3.5 requires (v2.1 only ran lane A).",
            ],
        },
    }

    blob = json.dumps(merged, ensure_ascii=False, sort_keys=False, indent=None, separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(blob)
    print("Wrote", OUT)
    print("total_classes=", total_classes, "accepted=", accepted, "rejected=", rejected)
    print("affine_pairs=", affine_pairs, "L3_surjective=", l3, "MARK_ISO_orbits=", mark_iso)
    print("denominator_check=", merged["denominator_check"])
    print("phat sanity AND-reduced:", size_phat_ok, pie_ok, order_ok)
    print("f_fixtures AND-reduced:", f1_ok, f21_ok, f22_ok, f25_ok, f26_ok, f35_ok,
          "makegn:", f25_makegn_ok, f26_makegn_ok, "canon:", f25_canon_ok, f26_canon_ok,
          "block_basis_eq_Amod:", block_basis_eq_amod_ok)
    print("checks_executed_total=", checks_total)
    print("fails_total=", fails_total)
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("sha256=", sha)

if __name__ == "__main__":
    main()
