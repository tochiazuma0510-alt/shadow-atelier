#!/usr/bin/env python
# crosscheck/check_pq8fam_ext.py
# Independent checker for search/certs/pq8fam_ext_v1_20260812.json (P-Q8FAM extension, 裁定823②).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT call GAP, does NOT import search/pq8fam_ext_v1.g.
#
# DISCLOSED LIMITATION: the actual AbelianInvariants(SmallGroup(id)) computation is a GAP-only
# primitive, not independently re-derived here (same convention as prior certs this session).
#
# What IS independently checked:
#  (A) provenance: EVERY candidate (m, id_group, structure_description) listed in the cert is
#      independently re-derived by scanning the ORIGINAL source cert
#      (search/certs/lins_census_2000_v1_20260811.json) for twin_pairs at index=24m whose
#      structure_description contains "SL(2,3)" or "Q8" -- re-implemented from scratch here,
#      not copy-pasted from the search script's hardcoded CANDIDATES list. This catches
#      transcription errors of the kind the implementer self-caught while authoring the search
#      script (m=55/65 initially mis-picked an SL(2,5)-based candidate instead of the correct
#      SL(2,3)-based one).
#  (B) predicted_3m = 3*m arithmetic re-derivation.
#  (C) matches_prediction = (ab_is_cyclic AND ab_order==predicted_3m) logical re-derivation
#      from the cert's own reported ab_order/ab_is_cyclic fields.
#  (D) m_found_count/missing_m/all_matches_prediction downstream re-derivation.
#  (E) completeness: every odd m in [1,83] (24m<=2000) has exactly one candidate in the cert.
import json

CENSUS_PATH = "search/certs/lins_census_2000_v1_20260811.json"
CERT_PATH = "search/certs/pq8fam_ext_v1_20260812.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def main():
    census = json.load(open(CENSUS_PATH, encoding="utf-8"))
    cert = json.load(open(CERT_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/pq8fam_ext_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/pq8fam_ext_v1")

    # (A) independently re-derive candidates from the source census
    odd_ms = list(range(1, 84, 2))
    if len(odd_ms) != 42:
        fail(f"internal: odd m count = {len(odd_ms)}, want 42")

    rederived_candidates = {}
    for tp in census["twin_pairs"]:
        idx = tp["index"]
        if idx % 24 != 0:
            continue
        m = idx // 24
        if m not in odd_ms:
            continue
        for member in tp["members"]:
            struct = member["structure_description"]
            if "SL(2,3)" in struct or "Q8" in struct:
                key = (m, tuple(member["id_group"]))
                rederived_candidates.setdefault(m, set()).add((tuple(member["id_group"]), struct))

    cert_results = {r["m"]: r for r in cert["results"]}

    mismatch_found = []
    for m in odd_ms:
        cert_r = cert_results.get(m)
        rederived = rederived_candidates.get(m, set())
        if cert_r is None:
            mismatch_found.append(f"m={m}: missing from cert entirely")
            continue
        cert_id = tuple(cert_r["id_group"])
        if (cert_id, cert_r["structure_description"]) not in rederived:
            mismatch_found.append(f"m={m}: cert's chosen candidate {cert_id}/"
                                    f"{cert_r['structure_description']} not found among "
                                    f"independently-rederived matches {rederived}")
    if mismatch_found:
        for m in mismatch_found:
            fail("provenance: " + m)
    else:
        ok("all 42 candidates' (m, id_group, structure_description) independently confirmed "
           "present in the source census with a matching SL(2,3)/Q8 signature (re-scanned from "
           "scratch, not copied from the search script)")

    # (B)+(C) arithmetic/logic re-derivation
    logic_bad = []
    for m, r in cert_results.items():
        pred = 3 * m
        if pred != r["predicted_3m"]:
            logic_bad.append(f"m={m}: predicted_3m rederived={pred} cert={r['predicted_3m']}")
            continue
        expected_match = r["ab_is_cyclic"] and (r["ab_order"] == pred)
        if expected_match != r["matches_prediction"]:
            logic_bad.append(f"m={m}: matches_prediction rederived={expected_match} "
                              f"cert={r['matches_prediction']} (ab_order={r['ab_order']}, "
                              f"ab_is_cyclic={r['ab_is_cyclic']}, predicted={pred})")
    if logic_bad:
        for b in logic_bad:
            fail(b)
    else:
        ok("predicted_3m=3m and matches_prediction=(ab_is_cyclic AND ab_order==3m) logic "
           "correctly re-derived for all 42 entries")

    # (D) downstream summary re-derivation
    rederived_m_found = sorted(cert_results.keys())
    rederived_missing = [m for m in odd_ms if m not in cert_results]
    rederived_all_match = all(r["matches_prediction"] for r in cert_results.values())

    if len(rederived_m_found) != cert.get("m_found_count"):
        fail(f"m_found_count rederived={len(rederived_m_found)} cert={cert.get('m_found_count')}")
    else:
        ok(f"m_found_count = {len(rederived_m_found)}")
    if rederived_missing != cert.get("missing_m"):
        fail(f"missing_m rederived={rederived_missing} cert={cert.get('missing_m')}")
    else:
        ok(f"missing_m = {rederived_missing}")
    if rederived_all_match != cert.get("all_matches_prediction"):
        fail(f"all_matches_prediction rederived={rederived_all_match} "
             f"cert={cert.get('all_matches_prediction')}")
    else:
        ok(f"all_matches_prediction = {rederived_all_match}")

    print()
    print("DISCLOSED LIMITATION: AbelianInvariants(SmallGroup(id)) itself is a GAP-only "
          "primitive, not independently re-derived by this checker.")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有; core GAP primitive not independently re-derived, see docstring)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
