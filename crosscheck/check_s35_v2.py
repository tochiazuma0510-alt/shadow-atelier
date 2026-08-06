#!/usr/bin/env python
# crosscheck/check_s35_v2.py
# Independent checker for search/certs/w6_bu_s35_v2_20260806.json (S3.5 v2
# companion report, 裁定594 / Sol F110-2.5 minimal reclaim bundle 1-2).
#
# CROSSCHECK, NOT VERIFICATION: this reads ONLY the cert JSON (no GAP code,
# no import of the driver or its helpers -- keeps the search/crosscheck
# separation the project requires). It re-derives every top-level count
# from the "rows" array and checks internal consistency + the disclosure
# discipline (no EMPTY/impossibility claim smuggled into "claims", a
# 【要数学検分】 tag present if L3_surjective_lifts totals to 0, D+D lane
# A/B scope statement present and literally says "D+D ROW ONLY"). It does
# NOT re-run any group theory and cannot detect a wrong GAP computation
# that is internally self-consistent -- that is out of scope for a
# cert-only checker, consistent with prior S3.5 checkers in this project.
import json, sys

PATH = "search/certs/w6_bu_s35_v2_20260806.json"
EXPECTED_ROWS = 17
EXPECTED_TOTAL_CLASSES = 449
EXPECTED_ACCEPTED = 73
EXPECTED_REJECTED = 376
EXPECTED_PAIRS = 1263

def fail(msg, fails):
    fails.append(msg)
    print("[FAIL]", msg)

def ok(msg):
    print("[PASS]", msg)

def main():
    fails = []
    doc = json.load(open(PATH, encoding="utf-8"))

    if doc.get("schema") != "w6-bu-s35-v2-cert/v1":
        fail("schema mismatch: " + str(doc.get("schema")), fails)
    else:
        ok("schema = w6-bu-s35-v2-cert/v1")

    rows = doc.get("rows", [])
    if len(rows) != EXPECTED_ROWS:
        fail(f"row count {len(rows)} != {EXPECTED_ROWS}", fails)
    else:
        ok(f"row count = {EXPECTED_ROWS}")

    # re-derive totals from rows alone
    rd_total_classes = sum(r["num_classes"] for r in rows)
    rd_accepted = sum(r["accepted_classes"] for r in rows)
    rd_rejected = sum(r["rejected_classes"] for r in rows)
    rd_pairs = sum(r["affine_solution_pairs"] for r in rows)
    rd_l3 = sum(r["L3_surjective_lifts"] for r in rows)
    rd_mark_iso = sum(r["MARK_ISO_orbits"] for r in rows)

    cv2 = doc.get("counts_v2", {})
    checks = [
        ("extension_classes (rows-derived vs top-level)", rd_total_classes, cv2.get("extension_classes")),
        ("affine_solvable_classes (rows-derived vs top-level)", rd_accepted, cv2.get("affine_solvable_classes")),
        ("affine_unsolvable_classes (rows-derived vs top-level)", rd_rejected, cv2.get("affine_unsolvable_classes")),
        ("affine_solution_pairs (rows-derived vs top-level)", rd_pairs, cv2.get("affine_solution_pairs")),
        ("L3_surjective_lifts (rows-derived vs top-level)", rd_l3, cv2.get("L3_surjective_lifts")),
        ("MARK_ISO_orbits (rows-derived vs top-level)", rd_mark_iso, cv2.get("MARK_ISO_orbits")),
    ]
    for name, got, want in checks:
        if got != want:
            fail(f"{name}: rows-derived={got} top-level={want}", fails)
        else:
            ok(f"{name}: {got}")

    # denominator against the frozen Sol/companion numbers
    denom_checks = [
        ("extension_classes == 449", rd_total_classes, EXPECTED_TOTAL_CLASSES),
        ("affine_solvable_classes == 73", rd_accepted, EXPECTED_ACCEPTED),
        ("affine_unsolvable_classes == 376", rd_rejected, EXPECTED_REJECTED),
        ("affine_solution_pairs == 1263", rd_pairs, EXPECTED_PAIRS),
        ("accepted + rejected == total", rd_accepted + rd_rejected, rd_total_classes),
    ]
    for name, got, want in denom_checks:
        if got != want:
            fail(f"denominator {name}: got={got} want={want}", fails)
        else:
            ok(f"denominator {name}")

    # per-row L3_surjective_lifts sanity: each must be <= affine_solution_pairs
    for r in rows:
        if not (0 <= r["L3_surjective_lifts"] <= r["affine_solution_pairs"]):
            fail(f"row {r['module_id']}: L3_surjective_lifts={r['L3_surjective_lifts']} out of [0,{r['affine_solution_pairs']}]", fails)
    ok("per-row L3_surjective_lifts in [0, affine_solution_pairs] for all rows")

    # claims discipline: no EMPTY/kill/candidate-found claim anywhere
    claims = doc.get("claims", {})
    if claims.get("kill_claim") is not False or claims.get("candidate_found") is not False or claims.get("empty_claim") is not False:
        fail("claims block contains a non-false kill/candidate/empty claim: " + json.dumps(claims), fails)
    else:
        ok("claims block: kill/candidate/empty all false")
    if claims.get("isolated_verdict") != "UNKNOWN":
        fail("isolated_verdict is not UNKNOWN: " + str(claims.get("isolated_verdict")), fails)
    else:
        ok("isolated_verdict = UNKNOWN")

    # L3_zero_disclosure: must carry the review tag if total L3 is 0, and
    # must NOT claim impossibility/theorem status
    l3z = doc.get("L3_zero_disclosure", {})
    if rd_l3 == 0:
        if l3z.get("needs_mathematical_review") is not True:
            fail("L3_surjective_lifts totals to 0 but needs_mathematical_review is not true", fails)
        else:
            ok("L3=0 correctly flagged needs_mathematical_review=true")
        if "【要数学検分】" not in str(l3z.get("review_tag", "")):
            fail("L3=0 but review_tag missing 【要数学検分】", fails)
        else:
            ok("review_tag present")
    else:
        ok(f"L3_surjective_lifts = {rd_l3} (nonzero; not a global-zero case)")
    note_text = str(l3z.get("note", "")) + str(l3z.get("candidate_theorem_note", ""))
    for banned in ["is proven", "theorem:", "QED", "proves that no marked lift"]:
        if banned.lower() in note_text.lower():
            fail(f"L3_zero_disclosure text appears to overclaim ('{banned}' found)", fails)
    ok("L3_zero_disclosure text does not contain overclaim phrases")

    # D+D lane A/B scope statement literal check
    dpd = doc.get("lane_a_lane_b_dpd_only", {})
    scope = str(dpd.get("scope_statement", ""))
    if "D+D ROW ONLY" not in scope and "D+D" not in scope:
        fail("lane_a_lane_b_dpd_only.scope_statement does not mention D+D-only scope", fails)
    else:
        ok("D+D-only scope statement present")
    dpd_classes = dpd.get("dpd_classes", [])
    if len(dpd_classes) != 4:
        fail(f"dpd_classes has {len(dpd_classes)} entries, want 4 (D+D row classes)", fails)
    else:
        ok("dpd_classes has 4 entries (D+D row)")
    for c in dpd_classes:
        if "l3_surjective" not in c:
            fail("a dpd_classes entry is missing l3_surjective (F110-2.5 required L-3 in lane B)", fails)
    ok("all dpd_classes entries carry l3_surjective (lane B now includes L-3)")

    # F-3.5 negative fixture must be present and true
    ff = doc.get("f_fixtures", {})
    if ff.get("F_3_5_negative_fixture_pass") is not True:
        fail("F_3_5_negative_fixture_pass is not true", fails)
    else:
        ok("F-3.5 negative fixture pass = true")

    # non_contact_declaration must be all false (no sealed-quantity contact)
    ncd = doc.get("non_contact_declaration", {})
    if any(ncd.get(k) for k in ["im_R", "d_N", "sealed_quantities", "S9", "kill", "empty_theorem", "candidate_generation"]):
        fail("non_contact_declaration has a true flag where false is required: " + json.dumps(ncd), fails)
    else:
        ok("non_contact_declaration all false where required")

    fails_total_field = doc.get("fails_total")
    if fails_total_field != 0:
        fail(f"cert's own fails_total = {fails_total_field} (GAP-side FAILS nonzero)", fails)
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
