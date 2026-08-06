#!/usr/bin/env python
# crosscheck/check_sg_pband2.py
# Independent checker for search/certs/sg_pband2_20260806.json (P-BAND-2
# test, 裁定677, theorem_check_mirrorall_l3vacuous_v1.md SSG.7.2).
#
# CROSSCHECK, NOT VERIFICATION: reads ONLY the cert JSON (no GAP call).
# Re-derives is_chiral/predicted_exists/matches_prediction from
# classification + pband2_exists alone, and re-derives the summary counts
# from rows[] -- catches bookkeeping bugs in the driver's own summary,
# though (as disclosed in the driver) it does NOT independently re-run
# CharacteristicSubgroups(Ghat) itself (single-lane/GAP-internal for that
# specific claim, same caveat structure as the G4/G5 pass).
import json, sys

PATH = "search/certs/sg_pband2_20260806.json"

def main():
    fails = []
    def fail(msg):
        fails.append(msg); print("[FAIL]", msg)
    def ok(msg):
        print("[PASS]", msg)

    doc = json.load(open(PATH, encoding="utf-8"))

    if doc.get("schema") != "shadow-atelier/sg-pband2/v1":
        fail("schema mismatch: " + str(doc.get("schema")))
    else:
        ok("schema = shadow-atelier/sg-pband2/v1")

    rows = doc.get("rows", [])
    if len(rows) != 36:
        fail(f"rows has {len(rows)} entries, want 36")
    else:
        ok("rows has 36 entries")

    if doc.get("windows_processed") != len(rows):
        fail(f"windows_processed={doc.get('windows_processed')} != len(rows)={len(rows)}")
    if len(doc.get("handoff_mismatches", [])) != 0:
        fail(f"handoff_mismatches nonzero: {doc.get('handoff_mismatches')}")
    else:
        ok("handoff_mismatches = 0")

    n_match = 0
    n_mismatch = 0
    chiral_count = 0
    reflexible_count = 0
    chiral_exists_count = 0
    reflexible_exists_count = 0
    mismatches = []

    for r in rows:
        is_chiral = (r["classification"] == "single_mirror_pair_non_exotic")
        if r["is_chiral"] != is_chiral:
            fail(f"({r['order']},{r['id']}): is_chiral={r['is_chiral']} but classification={r['classification']!r} implies {is_chiral}")
        predicted = is_chiral  # chiral -> predicted EXISTS; reflexible -> predicted NOT_EXISTS
        expected_match = (r["pband2_exists"] == predicted)
        if r["matches_prediction"] != expected_match:
            fail(f"({r['order']},{r['id']}): matches_prediction={r['matches_prediction']} rederived={expected_match}")
        if expected_match:
            n_match += 1
        else:
            n_mismatch += 1
            mismatches.append((r["order"], r["id"]))
        if is_chiral:
            chiral_count += 1
            if r["pband2_exists"]:
                chiral_exists_count += 1
        else:
            reflexible_count += 1
            if r["pband2_exists"]:
                reflexible_exists_count += 1

        # witness sanity: if pband2_exists, witness must be present and
        # structurally sane (Q_order>1, K_order<H_order<=|Ghat| implicitly)
        if r["pband2_exists"]:
            w = r.get("witness")
            if w is None:
                fail(f"({r['order']},{r['id']}): pband2_exists=true but witness is null")
            elif not (w["K_order"] < w["H_order"] and w["Q_order"] > 1 and w["H_order"] % w["K_order"] == 0
                      and w["H_order"] // w["K_order"] == w["Q_order"]):
                fail(f"({r['order']},{r['id']}): witness arithmetic inconsistent: {w}")
        else:
            if r.get("witness") is not None:
                fail(f"({r['order']},{r['id']}): pband2_exists=false but witness is non-null")

    if chiral_count != 5:
        fail(f"chiral_count={chiral_count}, expected 5")
    else:
        ok("chiral_count = 5")
    if reflexible_count != 31:
        fail(f"reflexible_count={reflexible_count}, expected 31")
    else:
        ok("reflexible_count = 31")

    ps = doc.get("prediction_summary", {})
    if ps.get("total_matches") != n_match or ps.get("total_mismatches") != n_mismatch:
        fail(f"prediction_summary: cert matches={ps.get('total_matches')} mismatches={ps.get('total_mismatches')} "
             f"rederived matches={n_match} mismatches={n_mismatch}")
    else:
        ok(f"prediction_summary rederived matches cert: {n_match} matches / {n_mismatch} mismatches")

    print()
    print("=== 36-row table ===")
    print(f"{'order':>6} {'id':>7} {'classification':30} {'pband2':10} {'predicted':10} {'match':6}")
    for r in sorted(rows, key=lambda r: (r["order"], r["id"])):
        pred = "EXISTS" if r["is_chiral"] else "NOT_EXISTS"
        act = "EXISTS" if r["pband2_exists"] else "NOT_EXISTS"
        print(f"{r['order']:>6} {r['id']:>7} {r['classification']:30} {act:10} {pred:10} {str(r['matches_prediction']):6}")

    print()
    print(f"chiral windows (n=5): pband2_exists=true count = {chiral_exists_count} (prediction: should be 5)")
    print(f"reflexible windows (n=31): pband2_exists=true count = {reflexible_exists_count} (prediction: should be 0)")
    if mismatches:
        print(f"MISMATCHES ({len(mismatches)}): {mismatches}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (cert bookkeeping cross-checked; CharacteristicSubgroups")
        print("completeness itself remains single-lane/GAP-internal, disclosed in the driver)")
        sys.exit(0)


if __name__ == "__main__":
    main()
