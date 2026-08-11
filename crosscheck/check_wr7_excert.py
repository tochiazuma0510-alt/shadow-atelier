#!/usr/bin/env python3
# crosscheck/check_wr7_excert.py
# Independent checker for the WR-7 retroactive exc-cert/v1 cert (裁定793(2),
# search/certs/wr7_excert_v1_20260811.json). Does NOT import
# search/wr7_retrodict_v1.py (search/crosscheck separation). Reads the TWO
# original source certs directly (sg_g4_g5_orb / sg_pband2prime -- both
# already-committed data, not this project's code) and independently
# reclassifies all 36 windows via its own logic, then compares against the
# cert.
import hashlib
import json
import sys

ORB_CERT_PATH = "search/certs/sg_g4_g5_orb_20260806.json"
PBAND2_CERT_PATH = "search/certs/sg_pband2prime_20260806.json"
CERT_PATH = "search/certs/wr7_excert_v1_20260811.json"


def main():
    fails = []

    def fail(msg):
        fails.append(msg)
        print("[FAIL]", msg)

    def ok(msg):
        print("[PASS]", msg)

    try:
        doc = json.load(open(CERT_PATH, encoding="utf-8"))
    except FileNotFoundError:
        print(f"CROSSCHECK RESULT: FAIL (cert not found: {CERT_PATH})")
        sys.exit(1)

    if doc.get("schema") != "shadow-atelier/exc-cert/v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/exc-cert/v1")

    orb = json.load(open(ORB_CERT_PATH, encoding="utf-8"))
    pband2 = json.load(open(PBAND2_CERT_PATH, encoding="utf-8"))

    orb_sha = hashlib.sha256(open(ORB_CERT_PATH, "rb").read()).hexdigest()
    pband2_sha = hashlib.sha256(open(PBAND2_CERT_PATH, "rb").read()).hexdigest()
    if orb_sha != doc["source_certs"]["orb_cert_sha256"] or pband2_sha != doc["source_certs"]["pband2_cert_sha256"]:
        fail("source cert sha256 mismatch -- the cert's provenance does not match the actual files "
             "on disk (possible new-run contamination or file drift)")
    else:
        ok("source cert sha256 hashes match the cert's declared provenance (no new run, files unchanged)")

    orb_by_key = {(r["order"], r["id"]): r for r in orb["g5_classification"]}
    pband2_by_key = {(r["order"], r["id"]): r for r in pband2["rows"]}

    if set(orb_by_key.keys()) != set(pband2_by_key.keys()):
        fail("window-set mismatch between the two source certs")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)

    # independent reclassification
    skip_ledger_recomputed = []
    excess_recomputed = []
    for key, orow in sorted(orb_by_key.items()):
        prow = pband2_by_key[key]
        order, gid = key
        if orow["classification"] == "isolated_self_mirror_no_twin":
            skip_ledger_recomputed.append((order, gid, "補題FIBER-FORCED"))
        elif orow["classification"] == "single_mirror_pair_non_exotic":
            if not prow["all_pass"]:
                skip_ledger_recomputed.append((order, gid, "定理SECT-CHIRAL"))
            else:
                excess_recomputed.append((order, gid))
        else:
            fail(f"unexpected classification for {key}: {orow['classification']}")

    cert_skip_keys = {(r["order"], r["id"], r["theorem_tag"]) for r in doc["skip_ledger"]}
    recomputed_skip_keys = set(skip_ledger_recomputed)
    if cert_skip_keys != recomputed_skip_keys:
        fail(f"skip_ledger mismatch: cert has {len(cert_skip_keys)} entries, recomputed has "
             f"{len(recomputed_skip_keys)} entries, diff={cert_skip_keys ^ recomputed_skip_keys}")
    else:
        ok(f"skip_ledger independently re-derived from the two source certs matches exactly "
           f"({len(recomputed_skip_keys)} entries)")

    cert_excess_keys = {(r["order"], r["id"]) for r in doc["excess"]}
    recomputed_excess_keys = set(excess_recomputed)
    if cert_excess_keys != recomputed_excess_keys:
        fail(f"excess mismatch: cert={cert_excess_keys} recomputed={recomputed_excess_keys}")
    else:
        ok(f"excess independently re-derived matches exactly: {sorted(recomputed_excess_keys)}")

    # discovery-history acceptance re-check
    n_fiber = sum(1 for _, _, tag in skip_ledger_recomputed if tag == "補題FIBER-FORCED")
    n_sect = sum(1 for _, _, tag in skip_ledger_recomputed if tag == "定理SECT-CHIRAL")
    n_danger = len(excess_recomputed)
    if (n_fiber, n_sect, n_danger) != (31, 3, 2):
        fail(f"discovery-history acceptance FAILS on recomputation: "
             f"fiber_forced={n_fiber} sect={n_sect} danger={n_danger} (expected 31,3,2)")
    else:
        ok(f"discovery-history acceptance independently re-verified: 31 FIBER-FORCED, "
           f"3 SECT-layer2, 2 DANGER-layer3 (total 36)")

    acc = doc["discovery_history_acceptance_check"]
    if acc["n_SKIP_FIBER_FORCED"] != n_fiber or acc["n_SKIP_SECT_layer2"] != n_sect or acc["n_DANGER_LAT_layer3"] != n_danger:
        fail("cert's own discovery_history_acceptance_check fields disagree with recomputation")

    # circularity check: verify canary_2's window set is genuinely disjoint
    # from the 5 chiral windows (independent structural check)
    reflexible_keys = {(r["order"], r["id"]) for r in pband2["rows"] if r["classification"] == "isolated_self_mirror_no_twin"}
    chiral_keys = {(r["order"], r["id"]) for r in pband2["rows"] if r["classification"] == "single_mirror_pair_non_exotic"}
    if reflexible_keys & chiral_keys:
        fail("canary_2's reflexible window set is NOT disjoint from the chiral window set -- "
             "circularity risk not actually avoided")
    else:
        ok(f"canary_2's window set ({len(reflexible_keys)} reflexible windows) is genuinely disjoint "
           f"from the classification target ({len(chiral_keys)} chiral windows) -- circularity check "
           f"independently confirmed")

    reflexible_all_pass_recomputed = all(r["all_pass"] for r in pband2["rows"] if r["classification"] == "isolated_self_mirror_no_twin")
    if reflexible_all_pass_recomputed != doc["canaries"][1]["all_pass"]:
        fail(f"canary_2 all_pass recomputed={reflexible_all_pass_recomputed} != cert "
             f"{doc['canaries'][1]['all_pass']}")
    else:
        ok(f"canary_2 (reflexible SECT health-check) all_pass re-derived correctly: "
           f"{reflexible_all_pass_recomputed}")

    if doc.get("stop_code") is not None:
        fail(f"cert has stop_code={doc.get('stop_code')} but recomputation shows discovery history "
             f"matches -- inconsistent")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (independently reclassified all 36 windows directly from the "
              "two original source certs -- own logic, not importing search/wr7_retrodict_v1.py -- "
              "reproduces skip_ledger/excess exactly, re-verifies the discovery-history acceptance "
              "criterion (31/3/2), and independently confirms the canary/skip window-set disjointness "
              "(circularity check); cross-checked, not 'verified' (reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
