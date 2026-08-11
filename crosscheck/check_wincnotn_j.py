#!/usr/bin/env python
# crosscheck/check_wincnotn_j.py
# Independent checker for search/certs/wincnotn_j_v1_20260812.json (WIN-CNOTN-J, 裁定828).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT call GAP, does NOT import search/wincnotn_j_v1.g.
#
# DISCLOSED LIMITATION: AbelianInvariants(SmallGroup(id)) itself is a GAP-only primitive, not
# independently re-derived here (same convention as prior certs this session, e.g.
# crosscheck/check_hcen_ab.py).
#
# What IS independently checked:
#  (A) provenance: all 83 (index, id_group) entries match search/certs/wincnotn_v1_20260812.json's
#      win_cnotn_target_members list exactly (re-read independently, not copied from the search
#      script's hardcoded MEMBERS list).
#  (B) downstream arithmetic: j = e/2 (only when e_even), j_notin_1_3 = (j not in {1,3}) --
#      re-derived from the cert's own reported e/e_even/j fields using an INDEPENDENT cyclicity-
#      unaware check (since e_is_cyclic is itself a GAP-only fact, this checker verifies the
#      ARITHMETIC given e and e_even, not e_is_cyclic's correctness).
#  (C) odd_e_count / j_notin_1_3_count downstream re-derivation.
#  (D) AB-2J consistency: since all 83 members are window members (in_PB3=True per the source
#      wincnotn_v1 cert), AB-2J predicts e even for all -- checked that odd_e_count==0 is
#      consistent with ALL 83 reported e values being even (a direct re-scan of the results
#      list, not just trusting the reported summary field).
import json

WINCNOTN_PATH = "search/certs/wincnotn_v1_20260812.json"
CERT_PATH = "search/certs/wincnotn_j_v1_20260812.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def main():
    wincnotn = json.load(open(WINCNOTN_PATH, encoding="utf-8"))
    cert = json.load(open(CERT_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/wincnotn_j_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/wincnotn_j_v1")

    results = cert.get("results", [])
    if len(results) != 83:
        fail(f"results count = {len(results)}, want 83")
    else:
        ok("results count = 83")

    # (A) provenance: exact match against wincnotn_v1's own target member list (order-sensitive,
    # since both lists are naturally ordered the same way -- built from the same source scan)
    source_members = wincnotn["win_cnotn_target_members"]
    if len(source_members) != len(results):
        fail(f"source wincnotn_v1 has {len(source_members)} target members, cert has {len(results)}")
    else:
        ok(f"source/cert member counts match ({len(source_members)})")

    mismatch = []
    for i, (s, r) in enumerate(zip(source_members, results)):
        if s["index"] != r["index"] or list(s["id_group"]) != list(r["id_group"]):
            mismatch.append(f"position {i}: source={s['index']}/{s['id_group']} "
                             f"cert={r['index']}/{r['id_group']}")
    if mismatch:
        for m in mismatch[:10]:
            fail("provenance: " + m)
        if len(mismatch) > 10:
            fail(f"... and {len(mismatch)-10} more provenance mismatches")
    else:
        ok("all 83 (index, id_group) entries match search/certs/wincnotn_v1_20260812.json's "
           "win_cnotn_target_members exactly, in order (independently re-read, not copied)")

    # (B) downstream arithmetic re-derivation
    arith_bad = []
    odd_e = 0
    j_notin_13 = 0
    for r in results:
        e = r["e"]
        e_even = r["e_even"]
        expected_even = (e % 2 == 0)
        if e_even != expected_even:
            arith_bad.append(f"index={r['index']} id={r['id_group']}: e_even={e_even} "
                              f"but e={e} parity says {expected_even}")
            continue
        if not e_even:
            odd_e += 1
            if r["j"] is not None or r["j_notin_1_3"] is not None:
                arith_bad.append(f"index={r['index']}: e odd but j/j_notin_1_3 not null")
            continue
        expected_j = e // 2
        if r["j"] != expected_j:
            arith_bad.append(f"index={r['index']} id={r['id_group']}: j={r['j']} "
                              f"expected e/2={expected_j}")
            continue
        expected_flag = (expected_j not in (1, 3))
        if r["j_notin_1_3"] != expected_flag:
            arith_bad.append(f"index={r['index']} id={r['id_group']}: j_notin_1_3="
                              f"{r['j_notin_1_3']} expected {expected_flag} (j={expected_j})")
        if expected_flag:
            j_notin_13 += 1

    if arith_bad:
        for b in arith_bad[:15]:
            fail("arithmetic: " + b)
        if len(arith_bad) > 15:
            fail(f"... and {len(arith_bad)-15} more arithmetic mismatches")
    else:
        ok("j=e/2 and j_notin_1_3=(j not in {1,3}) correctly re-derived for all 83 entries "
           "from their own reported e/e_even values")

    # (C) summary counts
    if odd_e != cert.get("odd_e_count"):
        fail(f"odd_e_count rederived={odd_e} cert={cert.get('odd_e_count')}")
    else:
        ok(f"odd_e_count = {odd_e}")
    if j_notin_13 != cert.get("j_notin_1_3_count"):
        fail(f"j_notin_1_3_count rederived={j_notin_13} cert={cert.get('j_notin_1_3_count')}")
    else:
        ok(f"j_notin_1_3_count = {j_notin_13}")

    # (D) AB-2J consistency: window members (in_PB3=True) should have even e
    if odd_e != 0:
        print(f"[INFO] odd_e_count={odd_e} > 0 -- would be an AB-2J anomaly if any window "
              f"member has odd e (raw fact, not interpreted here)")
    else:
        ok("odd_e_count=0 -- consistent with AB-2J (N<=PB3 => e even) across all 83 window members")

    print()
    print(f"raw summary: 83 window+c_notin_N members; odd_e (AB-2J anomaly candidates)={odd_e}; "
          f"j_notin_{{1,3}} count={j_notin_13}/83")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有; AbelianInvariants "
              "itself not independently re-derived, see docstring)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
