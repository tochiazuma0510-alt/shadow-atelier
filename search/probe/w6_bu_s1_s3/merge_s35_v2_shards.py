#!/usr/bin/env python
# search/probe/w6_bu_s1_s3/merge_s35_v2_shards.py
# Merges the 3 shard outputs of w6_bu_s35_driver_v2.g (shardA/B/C, split to
# respect the ~600s wall-clock convention -- see gaplib_common.g) into the
# single S3.5 v2 companion report (裁定594 / Sol F110-2.5 minimal reclaim
# bundle 1-2). This is a MERGE utility only -- it does not recompute any
# group theory, it just concatenates the "rows" arrays and re-sums the
# already-computed per-row totals. The independent checker
# (check_s35_v2.py) re-derives totals from "rows" alone and cross-checks
# them against the merged top-level counts -- that is the crosscheck lane,
# kept separate from this merge step per the search/crosscheck separation
# rule (this script is part of the "search" side; it does not verify).
import json, hashlib, sys

SHARDS = [
    "search/certs/w6_bu_s35_v2_20260806_shardA.json",
    "search/certs/w6_bu_s35_v2_20260806_shardB.json",
    "search/certs/w6_bu_s35_v2_20260806_shardC.json",
]
OUT = "search/certs/w6_bu_s35_v2_20260806.json"

EXPECTED_ROW_ORDER = [
  "p2_d4_a0b0c2", "p2_d2_a0b0c1", "p2_d2_a0b1c0", "p2_d2_a2b0c0",
  "p2_d3_a1b0c1", "p2_d3_a1b1c0", "p2_d3_a3b0c0",
  "p2_d4_a0b1c1", "p2_d4_a0b2c0", "p2_d4_a2b0c1", "p2_d4_a2b1c0",
  "p2_d4_a4b0c0",
  "p3_d2_bruteforce_1", "p3_d2_bruteforce_2", "p3_d2_bruteforce_3",
  "p3_d2_bruteforce_4", "p3_d2_bruteforce_5",
]

def main():
    docs = [json.load(open(p, encoding="utf-8")) for p in SHARDS]

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

    # dpd (D+D lane A/B, lives entirely in shard A since p2_d4_a0b0c2 is
    # processed first in shard A's ProcessOrder)
    dpd_doc = None
    for d in docs:
        if d.get("lane_a_lane_b_dpd_only", {}).get("dpd_classes"):
            dpd_doc = d
            break
    dpd_block = dpd_doc["lane_a_lane_b_dpd_only"] if dpd_doc else None

    # take F-fixture / phat_construction / counts_v2.unit_definitions /
    # authorization boilerplate from shard A (identical across shards --
    # these are row-independent facts computed fresh in every shard as a
    # side effect, not shard-specific data)
    base = docs[0]

    merged = {
        "schema": "w6-bu-s35-v2-cert/v1",
        "note": base["note"] + " [MERGED from 3 shards: shardA(11 rows incl. D+D)+shardB(p2_d4_a4b0c0)+shardC(5 p3 rows) -- sharded per gaplib_common.g 600s wall-clock convention; merge is concatenation + re-sum only, see merge_s35_v2_shards.py]",
        "design_doc": base["design_doc"],
        "authorization": base["authorization"],
        "shard_provenance": [
            {"path": p, "self_sha256": d["self_sha256"], "fails_total": d["fails_total"]}
            for p, d in zip(SHARDS, docs)
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
        "phat_construction": base["phat_construction"],
        "f_fixtures": base["f_fixtures"],
        "lane_a_lane_b_dpd_only": dpd_block,
        "rows": ordered_rows,
        "L3_zero_disclosure": {
            "note": base["L3_zero_disclosure"]["note"],
            "needs_mathematical_review": (l3 == 0),
            "review_tag": "【要数学検分】",
            "candidate_theorem_note": base["L3_zero_disclosure"]["candidate_theorem_note"],
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
    }

    blob = json.dumps(merged, ensure_ascii=False, sort_keys=False, indent=None, separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(blob)
    print("Wrote", OUT)
    print("total_classes=", total_classes, "accepted=", accepted, "rejected=", rejected)
    print("affine_pairs=", affine_pairs, "L3_surjective=", l3, "MARK_ISO_orbits=", mark_iso)
    print("denominator_check=", merged["denominator_check"])
    print("fails_total=", fails_total)
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("sha256=", sha)

if __name__ == "__main__":
    main()
