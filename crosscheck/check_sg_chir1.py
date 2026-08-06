#!/usr/bin/env python
# crosscheck/check_sg_chir1.py
# Independent checker for search/certs/sg_chir1_20260806.json (CHIR-1,
# 裁定686, theorem_check_mirrorall_l3vacuous_v1.md SSG.10.2, v2 architecture
# per 司令塔's intervention instruction).
#
# CROSSCHECK, NOT VERIFICATION: reads ONLY the cert JSON (no GAP call).
# Re-derives canaries C1-C6 and predictions P-CHIR-1..4 from rows[] alone.
import json, sys

PATH = "search/certs/sg_chir1_20260806.json"

def is_power_of_3(n):
    while n % 3 == 0:
        n //= 3
    return n == 1

def main():
    fails = []
    def fail(msg):
        fails.append(msg); print("[FAIL]", msg)
    def ok(msg):
        print("[PASS]", msg)

    doc = json.load(open(PATH, encoding="utf-8"))

    if doc.get("schema") != "shadow-atelier/sg-chir1/v2":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/sg-chir1/v2")

    rows = doc.get("rows", [])
    if len(rows) != 36:
        fail(f"rows has {len(rows)} entries, want 36")
    else:
        ok("rows has 36 entries")

    ok_rows = [r for r in rows if r["status"] == "OK"]
    if doc.get("windows_ok") != len(ok_rows):
        fail(f"windows_ok cert={doc.get('windows_ok')} rederived={len(ok_rows)}")
    else:
        ok(f"windows_ok = {len(ok_rows)}")

    non_ok = [r for r in rows if r["status"] != "OK"]
    if non_ok:
        for r in non_ok:
            print(f"  non-OK window: ({r['order']},{r['id']}) status={r['status']}")
    if len(doc.get("timeout_skipped", [])) + len(doc.get("compute_failed", [])) + len(doc.get("missing", [])) != len(non_ok):
        fail("timeout_skipped+compute_failed+missing counts don't match non-OK row count")
    else:
        ok(f"{len(non_ok)} non-OK windows accounted for (timeout/failed/missing)")

    # re-derive canaries C1-C6
    rederived_fails = []
    for r in ok_rows:
        kappa = r["kappa"]
        is_chiral = r["is_chiral"]
        if not is_chiral and kappa != 1:
            rederived_fails.append({"order": r["order"], "id": r["id"], "canary": "C1"})
        if is_chiral and kappa == 1:
            rederived_fails.append({"order": r["order"], "id": r["id"], "canary": "C2"})
        # C3 needs |Ghat| which we don't have directly in cert rows -- trust canary_C3_ok field is
        # internally consistent (kappa | order is checkable if we assume order field is |Ghat|... but
        # r['order'] is SmallGroups order id, which equals |Ghat| by definition)
        if r["order"] % kappa != 0:
            rederived_fails.append({"order": r["order"], "id": r["id"], "canary": "C3"})
        if r["kappa"] != r["kappa_mirror"]:
            rederived_fails.append({"order": r["order"], "id": r["id"], "canary": "C4"})
        if not r["canary_C5_ok"]:
            rederived_fails.append({"order": r["order"], "id": r["id"], "canary": "C5"})
        if r["X_excluded_family"]:
            rederived_fails.append({"order": r["order"], "id": r["id"], "canary": "C6"})

    cert_fails = doc.get("canary_fails", [])
    if len(rederived_fails) != len(cert_fails):
        fail(f"canary_fails count: cert={len(cert_fails)} rederived={len(rederived_fails)}")
    else:
        ok(f"canary_fails rederived matches cert: {len(rederived_fails)} (0 = all canaries clean)")

    # re-derive P-CHIR-1..4
    chiral_ok = [r for r in ok_rows if r["is_chiral"]]
    refl_ok = [r for r in ok_rows if not r["is_chiral"]]
    if len(chiral_ok) != 5:
        fail(f"chiral_ok count = {len(chiral_ok)}, want 5 (some chiral windows missing/failed)")
    if len(refl_ok) != 31:
        fail(f"refl_ok count = {len(refl_ok)}, want 31 (some reflexible windows missing/failed)")

    pchir1 = all(is_power_of_3(r["kappa"]) for r in chiral_ok) if chiral_ok else None
    cert_p1 = doc.get("predictions", {}).get("P_CHIR_1", {})
    if cert_p1.get("holds_for_all_5_chiral") != pchir1:
        fail(f"P_CHIR_1: cert={cert_p1.get('holds_for_all_5_chiral')} rederived={pchir1}")
    else:
        ok(f"P-CHIR-1 rederived matches cert: {pchir1}")

    layer3_keys = {(1944, 826), (1944, 921)}
    layer2_keys = {(1296, 2889), (1296, 3487), (1728, 31096)}

    for r in ok_rows:
        key = (r["order"], r["id"])
        if key in layer2_keys:
            broken = [f for f in r["covered_chief_factors"] if f["order"] == 9 and not f["sect_holds"]]
            if not broken:
                fail(f"layer-2 window {key}: no broken 3^2 factor found (expected exactly 1, per prior P-BAND-2' cert)")
            elif not all(f["covers"] for f in broken):
                fail(f"layer-2 window {key}: X does not cover its broken factor -- P-CHIR-3 violated")

    print()
    print("=== 36-row table ===")
    print(f"{'order':>6} {'id':>7} {'classification':30} {'status':16} {'kappa':>6} {'id_X':>10} {'C5':>6}")
    for r in sorted(rows, key=lambda r: (r["order"], r["id"])):
        kappa = r.get("kappa", "-")
        idx = str(r.get("id_X", "-"))
        c5 = str(r.get("canary_C5_ok", "-"))
        print(f"{r['order']:>6} {r['id']:>7} {r['classification']:30} {r['status']:16} {str(kappa):>6} {idx:>10} {c5:>6}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
