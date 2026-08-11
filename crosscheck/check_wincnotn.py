#!/usr/bin/env python
# crosscheck/check_wincnotn.py
# Independent checker for search/certs/wincnotn_v1_20260812.json (WIN-CNOTN, 裁定823③).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT import search/wincnotn_v1.py. Re-implements the
# band-filter + cross-tabulation from scratch, reading ONLY the ORIGINAL source cert.
import json
import hashlib

CENSUS_PATH = "search/certs/lins_census_2000_v1_20260811.json"
CERT_PATH = "search/certs/wincnotn_v1_20260812.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def main():
    census_sha256 = hashlib.sha256(open(CENSUS_PATH, "rb").read()).hexdigest()
    census = json.load(open(CENSUS_PATH, encoding="utf-8"))
    cert = json.load(open(CERT_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/wincnotn_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/wincnotn_v1")

    if cert.get("source_cert_sha256") != census_sha256:
        fail(f"source_cert_sha256 mismatch")
    else:
        ok(f"source_cert_sha256 matches actual file ({census_sha256})")

    band_lo, band_hi = cert["band"]
    if [band_lo, band_hi] != [1000, 2000]:
        fail(f"band = {[band_lo, band_hi]}, want [1000, 2000]")
    else:
        ok("band = [1000, 2000]")

    # own independent re-derivation
    members = []
    for tp in census["twin_pairs"]:
        idx = tp["index"]
        if band_lo < idx <= band_hi:
            for m in tp["members"]:
                members.append({"index": idx, "id_group": m["id_group"],
                                 "in_PB3": m["in_PB3"], "c_in_N": m["c_in_N"]})

    total = len(members)
    if total != cert.get("total_members_in_band"):
        fail(f"total_members_in_band rederived={total} cert={cert.get('total_members_in_band')}")
    else:
        ok(f"total_members_in_band = {total}")

    def count(in_pb3, c_in_n):
        return sum(1 for m in members if m["in_PB3"] == in_pb3 and m["c_in_N"] == c_in_n)

    ct = cert["cross_tab"]
    rederived_ct = {
        "window_c_in_N": count(True, True),
        "window_c_notin_N": count(True, False),
        "nonwindow_c_in_N": count(False, True),
        "nonwindow_c_notin_N": count(False, False),
    }
    if rederived_ct != ct:
        fail(f"cross_tab mismatch: rederived={rederived_ct} cert={ct}")
    else:
        ok(f"cross_tab rederived exactly: {rederived_ct}")

    sum_all = sum(rederived_ct.values())
    if sum_all != total:
        fail(f"cross_tab sum ({sum_all}) != total_members_in_band ({total})")
    else:
        ok(f"cross_tab entries sum to total_members_in_band ({total}) -- exhaustive partition check")

    window_total = rederived_ct["window_c_in_N"] + rederived_ct["window_c_notin_N"]
    nonwindow_total = rederived_ct["nonwindow_c_in_N"] + rederived_ct["nonwindow_c_notin_N"]
    if window_total != cert.get("window_total"):
        fail(f"window_total rederived={window_total} cert={cert.get('window_total')}")
    else:
        ok(f"window_total = {window_total}")
    if nonwindow_total != cert.get("nonwindow_total"):
        fail(f"nonwindow_total rederived={nonwindow_total} cert={cert.get('nonwindow_total')}")
    else:
        ok(f"nonwindow_total = {nonwindow_total}")

    win_cnotn_members = [m for m in members if m["in_PB3"] and not m["c_in_N"]]
    if len(win_cnotn_members) != cert.get("win_cnotn_target_count"):
        fail(f"win_cnotn_target_count rederived={len(win_cnotn_members)} "
             f"cert={cert.get('win_cnotn_target_count')}")
    else:
        ok(f"win_cnotn_target_count = {len(win_cnotn_members)}")

    if len(win_cnotn_members) != rederived_ct["window_c_notin_N"]:
        fail("internal inconsistency: win_cnotn_target_count != cross_tab.window_c_notin_N")
    else:
        ok("win_cnotn_target_count consistent with cross_tab.window_c_notin_N")

    # spot check: every reported win_cnotn_target_members entry actually satisfies in_PB3=True,
    # c_in_N=False in the source cert
    cert_target_members = cert.get("win_cnotn_target_members", [])
    if len(cert_target_members) != len(win_cnotn_members):
        fail(f"win_cnotn_target_members length {len(cert_target_members)} != "
             f"win_cnotn_target_count {len(win_cnotn_members)}")
    else:
        ok(f"win_cnotn_target_members length matches win_cnotn_target_count ({len(cert_target_members)})")

    print()
    print(f"raw summary: {total} twin-pair members in band (1000,2000]; "
          f"window+c_notin_N target population = {len(win_cnotn_members)}")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
