#!/usr/bin/env python
# crosscheck/check_sg_g9_characteristic.py
# Independent checker for search/certs/sg_g9_characteristic_20260806.json
# (GAP-G9-1, 裁定683, theorem_check_mirrorall_l3vacuous_v1.md SSG.9.1).
#
# CROSSCHECK, NOT VERIFICATION: reads ONLY the cert JSON (no GAP call).
# Re-derives characteristic_confirmed and grade from M_check/L_check alone,
# and checks the logical structure (both_confirmed = M.characteristic AND
# L.characteristic; characteristic_confirmed = unique_normal OR std_match).
import json, sys

PATH = "search/certs/sg_g9_characteristic_20260806.json"
EXPECTED_TARGETS = {(1296, 2889), (1296, 3487), (1728, 31096)}

def main():
    fails = []
    def fail(msg):
        fails.append(msg); print("[FAIL]", msg)
    def ok(msg):
        print("[PASS]", msg)

    doc = json.load(open(PATH, encoding="utf-8"))

    if doc.get("schema") != "shadow-atelier/sg-g9-characteristic/v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/sg-g9-characteristic/v1")

    rows = doc.get("rows", [])
    keys = {(r["order"], r["id"]) for r in rows}
    if keys != EXPECTED_TARGETS:
        fail(f"rows cover {keys}, expected {EXPECTED_TARGETS}")
    else:
        ok("rows cover exactly the 3 target windows")

    for r in rows:
        for side, chk in [("M", r["M_check"]), ("L", r["L_check"])]:
            if chk is None:
                fail(f"({r['order']},{r['id']}) {side}_check is null (RESCAN_MISMATCH?)")
                continue
            rederived = chk["unique_normal_of_order"] or (chk["matches_standard_characteristic_term"] is not None)
            if rederived != chk["characteristic_confirmed"]:
                fail(f"({r['order']},{r['id']}) {side}: characteristic_confirmed cert={chk['characteristic_confirmed']} rederived={rederived}")
            if not chk["is_normal"]:
                fail(f"({r['order']},{r['id']}) {side}: is_normal=false -- chief series term should always be normal")

        if r["M_check"] is not None and r["L_check"] is not None:
            rederived_both = r["M_check"]["characteristic_confirmed"] and r["L_check"]["characteristic_confirmed"]
            if rederived_both != r["both_confirmed"]:
                fail(f"({r['order']},{r['id']}): both_confirmed cert={r['both_confirmed']} rederived={rederived_both}")
            expected_grade = "紙定理+機械入力" if rederived_both else "機械のみ"
            if r["grade"] != expected_grade:
                fail(f"({r['order']},{r['id']}): grade cert={r['grade']!r} rederived={expected_grade!r}")

    ok_count = sum(1 for r in rows if r.get("both_confirmed") is True)
    print()
    print("=== summary table ===")
    for r in sorted(rows, key=lambda r: (r["order"], r["id"])):
        print(f"  ({r['order']},{r['id']}): M_order={r['M_order']} L_order={r['L_order']} "
              f"both_confirmed={r['both_confirmed']} grade={r['grade']!r}")
    print()
    print(f"windows with characteristic premise confirmed: {ok_count}/3")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
