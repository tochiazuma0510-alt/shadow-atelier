#!/usr/bin/env python
# crosscheck/check_s35_v2_1.py
# Independent checker for search/certs/w6_bu_s35_v2_1_20260806.json (S3.5
# v2.1 companion report, 裁定615 falsifier-review repair). Laid ALONGSIDE
# crosscheck/check_s35_v2.py (which still checks the frozen, unchanged v2
# cert) -- this checks v2.1 specifically, including the six repair items.
#
# CROSSCHECK, NOT VERIFICATION: reads ONLY the cert JSON, no GAP/driver
# import (search/crosscheck separation preserved).
import json, sys

PATH = "search/certs/w6_bu_s35_v2_1_20260806.json"
EXPECTED_ROWS = 17
EXPECTED_TOTAL_CLASSES = 449
EXPECTED_ACCEPTED = 73
EXPECTED_REJECTED = 376
EXPECTED_PAIRS = 1263
EXPECTED_L3 = 42          # v2.1 fix must NOT change the substantive measurement
EXPECTED_MARK_ISO = 21


def main():
    fails = []
    def fail(msg):
        fails.append(msg); print("[FAIL]", msg)
    def ok(msg):
        print("[PASS]", msg)

    doc = json.load(open(PATH, encoding="utf-8"))

    if doc.get("schema") != "w6-bu-s35-v2.1-cert/v1":
        fail("schema mismatch: " + str(doc.get("schema")))
    else:
        ok("schema = w6-bu-s35-v2.1-cert/v1")

    rows = doc.get("rows", [])
    if len(rows) != EXPECTED_ROWS:
        fail(f"row count {len(rows)} != {EXPECTED_ROWS}")
    else:
        ok(f"row count = {EXPECTED_ROWS}")

    rd_total = sum(r["num_classes"] for r in rows)
    rd_acc = sum(r["accepted_classes"] for r in rows)
    rd_rej = sum(r["rejected_classes"] for r in rows)
    rd_pairs = sum(r["affine_solution_pairs"] for r in rows)
    rd_l3 = sum(r["L3_surjective_lifts"] for r in rows)
    rd_mi = sum(r["MARK_ISO_orbits"] for r in rows)

    cv2 = doc.get("counts_v2", {})
    for name, got, want in [
        ("extension_classes", rd_total, cv2.get("extension_classes")),
        ("affine_solvable_classes", rd_acc, cv2.get("affine_solvable_classes")),
        ("affine_unsolvable_classes", rd_rej, cv2.get("affine_unsolvable_classes")),
        ("affine_solution_pairs", rd_pairs, cv2.get("affine_solution_pairs")),
        ("L3_surjective_lifts", rd_l3, cv2.get("L3_surjective_lifts")),
        ("MARK_ISO_orbits", rd_mi, cv2.get("MARK_ISO_orbits")),
    ]:
        (ok if got == want else fail)(f"{name}: rows-derived={got} top-level={want}")

    for name, got, want in [
        ("extension_classes == 449", rd_total, EXPECTED_TOTAL_CLASSES),
        ("affine_solvable_classes == 73", rd_acc, EXPECTED_ACCEPTED),
        ("affine_unsolvable_classes == 376", rd_rej, EXPECTED_REJECTED),
        ("affine_solution_pairs == 1263", rd_pairs, EXPECTED_PAIRS),
        ("L3_surjective_lifts == 42 (must be UNCHANGED from v2 -- v2.1 only fixes bookkeeping)", rd_l3, EXPECTED_L3),
        ("MARK_ISO_orbits == 21 (must be UNCHANGED from v2)", rd_mi, EXPECTED_MARK_ISO),
    ]:
        (ok if got == want else fail)(f"denominator {name}")

    # --- v2.1-specific repair items ---

    # item 2: shard_provenance must carry DISTINCT shard_output_sha256 per
    # shard (the v2 bug was all 3 identical -- the driver's own hash).
    sp = doc.get("shard_provenance", [])
    shas = [s.get("shard_output_sha256") for s in sp]
    if len(sp) != 3:
        fail(f"shard_provenance has {len(sp)} entries, want 3")
    elif len(set(shas)) != 3 or any(s is None for s in shas):
        fail(f"shard_output_sha256 values not all distinct/present (item 2 regression): {shas}")
    else:
        ok("shard_provenance.shard_output_sha256: 3 distinct real hashes (item 2 fixed)")
    driver_shas = [s.get("driver_self_sha256") for s in sp]
    if len(set(driver_shas)) != 1:
        fail(f"driver_self_sha256 should be identical across shards (same driver file): {driver_shas}")
    else:
        ok("driver_self_sha256 identical across shards (expected, same driver script)")

    # item 3: the 7 booleans must be actual booleans (not missing), and
    # PIE especially must be true only because it was really computed.
    pcc = doc.get("phat_construction", {}).get("sanity_checks_passed", {})
    ff = doc.get("f_fixtures", {})
    seven = {
        "phat_construction.sanity_checks_passed.size_Phat_eq_3000_times_V": pcc.get("size_Phat_eq_3000_times_V"),
        "phat_construction.sanity_checks_passed.piE_U0_eq_theta_and_piE_W0_eq_tau": pcc.get("piE_U0_eq_theta_and_piE_W0_eq_tau"),
        "phat_construction.sanity_checks_passed.order_...": pcc.get("order_Uhat0_times_What0_matches_or_doubles_Ghat5_reference"),
        "f_fixtures.F_1_all_pass": ff.get("F_1_all_pass"),
        "f_fixtures.F_2_1_sigma1sq_eq_x": ff.get("F_2_1_sigma1sq_eq_x"),
        "f_fixtures.F_2_2_sigma2sq_eq_y": ff.get("F_2_2_sigma2sq_eq_y"),
        "f_fixtures.F_3_5_negative_fixture_pass": ff.get("F_3_5_negative_fixture_pass"),
    }
    for name, v in seven.items():
        if v is not True:
            fail(f"item-3 boolean {name} is not True: {v!r}")
    if all(v is True for v in seven.values()):
        ok("all 7 item-3 booleans present and True")
    if "note" not in pcc or "AND-reduction of a REAL check" not in pcc.get("note", ""):
        fail("phat_construction.sanity_checks_passed.note missing the item-3 real-check disclosure")
    else:
        ok("item-3 disclosure note present")

    # item 4: check roster + denominator
    cs = doc.get("check_semantics", {})
    n_names = len(cs.get("checks_executed_names", []))
    n_total = cs.get("checks_executed_total")
    if n_total is None or n_names != n_total:
        fail(f"check_semantics roster/total mismatch: total={n_total} len(names)={n_names}")
    else:
        ok(f"check_semantics: checks_executed_total={n_total} matches roster length")
    if n_total is None or n_total <= 0:
        fail("checks_executed_total is missing or non-positive (item 4)")

    # item 5: fail-soft disclosure present
    if "fail-soft" not in cs.get("note", "") and "FAIL-SOFT" not in cs.get("note", ""):
        fail("check_semantics.note does not disclose Chk() fail-soft semantics (item 5)")
    else:
        ok("Chk() fail-soft semantics explicitly disclosed (item 5)")

    # item 6: naming map present
    fnm = ff.get("fixture_naming_map", {})
    required_map_keys = ["F-1.1", "F-2.1", "F-2.2", "F-2.5", "F-2.6", "F-3.5"]
    missing_map = [k for k in required_map_keys if k not in fnm]
    if missing_map:
        fail(f"fixture_naming_map missing keys: {missing_map} (item 6)")
    else:
        ok("fixture_naming_map covers F-1.1/F-2.1/F-2.2/F-2.5/F-2.6/F-3.5 (item 6)")

    # SM-1 disclosure
    l3z = doc.get("L3_zero_disclosure", {})
    if "SM_1" not in l3z or "blind" not in l3z.get("SM_1", "").lower():
        fail("L3_zero_disclosure.SM_1 missing or does not state the marking-blindness caveat")
    else:
        ok("SM-1 (L-3 is blind to marking window) disclosure present")

    # v2_1_repair_record present, names the predecessor
    rr = doc.get("v2_1_repair_record", {})
    if "w6_bu_s35_v2_20260806.json" not in str(rr.get("predecessor", "")):
        fail("v2_1_repair_record.predecessor does not reference the unchanged v2 cert")
    else:
        ok("v2_1_repair_record.predecessor correctly names the unchanged v2 cert")
    if len(rr.get("items_fixed", [])) < 6:
        fail(f"v2_1_repair_record.items_fixed has {len(rr.get('items_fixed', []))} entries, want >= 6")
    else:
        ok(f"v2_1_repair_record.items_fixed has {len(rr.get('items_fixed', []))} entries")

    # claims/non-contact discipline (same as v2)
    claims = doc.get("claims", {})
    if claims.get("kill_claim") is not False or claims.get("candidate_found") is not False or claims.get("empty_claim") is not False:
        fail("claims block contains a non-false kill/candidate/empty claim")
    else:
        ok("claims block: kill/candidate/empty all false")
    if claims.get("isolated_verdict") != "UNKNOWN":
        fail("isolated_verdict is not UNKNOWN")
    else:
        ok("isolated_verdict = UNKNOWN")

    if doc.get("fails_total") != 0:
        fail(f"cert's own fails_total = {doc.get('fails_total')} (GAP-side FAILS nonzero)")
    else:
        ok("cert's own fails_total = 0")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (cross-checked, NOT verified -- see CLAUDE.md Lean reservation)")
        sys.exit(0)


if __name__ == "__main__":
    main()
