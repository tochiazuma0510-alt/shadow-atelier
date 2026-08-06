#!/usr/bin/env python3
# crosscheck/check_aside2.py
# Independent checker for the ASIDE-2 per-prime certs (裁定708,
# docs/notes/aside_measurement_design_v1_addendum_c.md, commit 85827ca,
# verbatim). Reads ONLY the cert JSON files -- does NOT import
# search/aside2_run_single_prime.py, search/aside1_run_single_prime.py, or
# search/edim_semidirect_v1.py (search/crosscheck separation). Re-derives
# every stop-rule/canary predicate from the raw per-prime fields recorded
# in the cert.
#
# ASIDE-1's v1 certs (search/certs/aside1_prime_*_v1_20260806.json) are
# EXPLICITLY NOT adopted by this checker -- per 裁定708 point 4, they are
# superseded by ASIDE-2's stage B'/C' (Ihara bracket, addendum-fixed
# convention) because ASIDE-1's stage B/C used a plain free-Lie commutator
# that the addendum diagnosed as BRACKET_IMPL_FAIL. This checker does not
# read those files at all; they remain on disk only as an audit trail.
import json
import sys
import glob

CERT_GLOB = "search/certs/aside2_prime_*_v2_20260806.json"
AUTHORIZED_GENERAL_PRIMES = {2147483647, 998244353, 677, 701}  # 裁定711: 677/701
# authorized as the S-ED-7 mid-size control pair (addendum SS4.3), expected
# to behave like the 2 large "general" primes -- same S-AS-2' gate applies.
SPECIAL_PRIME = 691
AUTHORIZED_PRIMES_THIS_DISPATCH = {691, 998244353, 2147483647, 677, 701}  # 裁定708
# point 3 (691,998244353,2147483647) + 裁定711 (677,701 S-ED-7 control pair).


def main():
    fails = []

    def fail(msg):
        fails.append(msg)
        print("[FAIL]", msg)

    def ok(msg):
        print("[PASS]", msg)

    paths = sorted(glob.glob(CERT_GLOB))
    if not paths:
        fail("no aside2 cert files found")
        print("CROSSCHECK RESULT: FAIL")
        sys.exit(1)

    certs = {}
    for path in paths:
        doc = json.load(open(path, encoding="utf-8"))
        certs[doc["prime"]] = doc
        if doc.get("schema") != "shadow-atelier/aside2/v1":
            fail(f"{path}: schema mismatch")
        else:
            ok(f"{path}: schema = shadow-atelier/aside2/v1")

    print()
    print(f"=== primes present: {sorted(certs.keys())} ===")
    unexpected = set(certs.keys()) - AUTHORIZED_PRIMES_THIS_DISPATCH
    if unexpected:
        fail(f"unauthorized primes present in this dispatch: {unexpected} "
             f"(only {AUTHORIZED_PRIMES_THIS_DISPATCH} were authorized by 裁定708 point 3)")
    else:
        ok(f"only authorized primes present: {sorted(certs.keys())}")

    # S-AS-5 rescan: no forbidden verdict language anywhere in the cert text.
    forbidden = ["不均衡", "SYN-0", "k*", "段差"]
    for prime, doc in certs.items():
        blob = json.dumps(doc, ensure_ascii=False)
        for word in forbidden:
            if word in blob:
                fail(f"prime={prime}: forbidden verdict text '{word}' found in cert -- S-AS-5 VERDICT_IN_CODE")
    ok("S-AS-5 rescan: no forbidden verdict strings in any cert")

    # fixture_ok / S-AS-7 must be True in every cert (checked fresh each
    # dispatch, per the driver's own design) -- re-verify presence and value.
    for prime, doc in sorted(certs.items()):
        fc = doc.get("fixture_check", {})
        fixture_ok_recorded = doc.get("fixture_ok_this_run")
        subchecks = ["word_table_ok", "term_counts_ok", "recon_ok", "theorem_ca_ok"]
        rederived_fixture_ok = all(fc.get(s) is True for s in subchecks) if fc else None
        if rederived_fixture_ok != fixture_ok_recorded:
            fail(f"prime={prime}: fixture_ok_this_run={fixture_ok_recorded} but rederived from "
                 f"sub-checks={rederived_fixture_ok}")
        else:
            ok(f"prime={prime}: fixture_ok_this_run={fixture_ok_recorded} matches sub-checks "
               f"({subchecks})")
        if not fixture_ok_recorded:
            fail(f"prime={prime}: fixture_ok_this_run=False -- S-AS-7 FIXTURE_MISMATCH should have stopped")

    # Per-prime stop_code re-derivation from raw fields only.
    for prime, doc in sorted(certs.items()):
        if not doc.get("fixture_ok_this_run"):
            rederived_stop = "FIXTURE_MISMATCH"
        else:
            stage_a = doc.get("stage_A_sigma", {})
            sigma_ok_all = all(stage_a.get(str(m), stage_a.get(m, {})).get("S_dim") == 1
                                for m in (3, 5, 7, 9)) if stage_a else None
            rederived_stop = None
            if sigma_ok_all is False:
                rederived_stop = "SIGMA_NONUNIQUE"

            stage_b = doc.get("stage_B_prime_ihara_weight_graded")
            stage_c = doc.get("stage_C_prime_ihara_depth2")
            if rederived_stop is None and stage_b is not None:
                A12_ihara = stage_b.get("A12_ihara")
                is_general = prime in AUTHORIZED_GENERAL_PRIMES
                if is_general and A12_ihara != 2:
                    rederived_stop = "CALIBRATION_FAIL"
            if rederived_stop is None and stage_c is not None:
                A12_depth2_ihara = stage_c.get("A12_depth2_ihara")
                if A12_depth2_ihara != 1:
                    rederived_stop = "BRACKET_IMPL_FAIL"
            if rederived_stop is None:
                theta_ok = doc.get("theta_ok")
                if theta_ok is False:
                    rederived_stop = "BRACKET_NOT_GRT"

        cert_stop = doc.get("stop_code")
        if cert_stop != rederived_stop:
            fail(f"prime={prime}: stop_code cert={cert_stop!r} rederived={rederived_stop!r}")
        else:
            ok(f"prime={prime}: stop_code={cert_stop!r} rederived matches")

    # Theorem C-A canary: A12_depth2_ihara must be EXACTLY 1 at every prime
    # present (not just general primes) -- re-derive directly.
    for prime, doc in sorted(certs.items()):
        stage_c = doc.get("stage_C_prime_ihara_depth2", {})
        val = stage_c.get("A12_depth2_ihara")
        if val != 1:
            fail(f"prime={prime}: Theorem C-A canary violated -- A12_depth2_ihara={val} != 1")
        else:
            ok(f"prime={prime}: Theorem C-A canary holds (A12_depth2_ihara=1)")

    # Stage E self-consistency: D_is_zero should be consistent with the
    # depth profile (all-zero depth profile <=> D_is_zero=True), and with
    # A12_ihara (D_is_zero=True implies v1=3*v2 implies A12_ihara<=1, i.e.
    # A12_ihara should be 1 whenever D_is_zero=True and v1,v2 not both zero).
    for prime, doc in sorted(certs.items()):
        stage_e = doc.get("stage_E_D_ihara_takao_difference", {})
        stage_b = doc.get("stage_B_prime_ihara_weight_graded", {})
        D_is_zero = stage_e.get("D_is_zero")
        depth_profile = stage_e.get("D_depth_profile", {})
        profile_all_zero = all(v == 0 for v in depth_profile.values()) if depth_profile else None
        if D_is_zero != profile_all_zero:
            fail(f"prime={prime}: D_is_zero={D_is_zero} but depth_profile_all_zero={profile_all_zero}")
        else:
            ok(f"prime={prime}: D_is_zero={D_is_zero} consistent with depth profile")
        A12_ihara = stage_b.get("A12_ihara")
        if D_is_zero is True and A12_ihara not in (0, 1):
            fail(f"prime={prime}: D_is_zero=True but A12_ihara={A12_ihara} (expected <=1)")
        if D_is_zero is False and A12_ihara == 1:
            # not a contradiction per se (D!=0 doesn't strictly forbid rank 1
            # if v1,v2 have a different non-3x relation), but flag for visibility
            print(f"[NOTE] prime={prime}: D_is_zero=False yet A12_ihara=1 -- worth a second look "
                  f"(not flagged as FAIL, just noted)")

    print()
    print("=== raw per-prime table (re-read from cert only) ===")
    for prime, doc in sorted(certs.items()):
        b = doc.get("stage_B_prime_ihara_weight_graded", {})
        c = doc.get("stage_C_prime_ihara_depth2", {})
        e = doc.get("stage_E_D_ihara_takao_difference", {})
        print(f"  prime={prime}: A12_ihara={b.get('A12_ihara')} A12_depth2_ihara={c.get('A12_depth2_ihara')} "
              f"theta_ok={doc.get('theta_ok')} D_is_zero={e.get('D_is_zero')} "
              f"D_depth_profile={e.get('D_depth_profile')} stop_code={doc.get('stop_code')}")

    # cross-prime agreement of ALL general/S-ED-7-control primes present
    # (large primes 2147483647/998244353 + mid-size control pair 677/701,
    # 裁定711 -- all are expected to show the SAME (A12_ihara, D_depth_
    # profile), since none of them is the special prime 691).
    general_present = {p: certs[p] for p in AUTHORIZED_GENERAL_PRIMES if p in certs}
    if len(general_present) >= 2:
        a12_vals = {p: d.get("stage_B_prime_ihara_weight_graded", {}).get("A12_ihara") for p, d in general_present.items()}
        profiles = {p: d.get("stage_E_D_ihara_takao_difference", {}).get("D_depth_profile") for p, d in general_present.items()}
        if len(set(a12_vals.values())) == 1 and len(set(json.dumps(v, sort_keys=True) for v in profiles.values())) == 1:
            ok(f"all {len(general_present)} general/control primes {sorted(general_present.keys())} AGREE "
               f"with each other: A12_ihara={list(a12_vals.values())[0]}, D_depth_profile identical")
        else:
            fail(f"the general/control primes DISAGREE: A12_ihara={a12_vals} profiles={profiles}")

    # S-ED-7 specific check (裁定711): 677/701 must each individually match
    # the large-prime pattern (this is the literal point of the control
    # pair -- "691 だけが特異" confirmed only if 677/701 pattern with the
    # large primes, not with 691).
    sed7_pair = {p: certs[p] for p in (677, 701) if p in certs}
    if sed7_pair:
        for p, d in sed7_pair.items():
            a12 = d.get("stage_B_prime_ihara_weight_graded", {}).get("A12_ihara")
            d_is_zero = d.get("stage_E_D_ihara_takao_difference", {}).get("D_is_zero")
            if a12 == 2 and d_is_zero is False:
                ok(f"S-ED-7 control prime={p}: matches the general-prime pattern (A12_ihara=2, D_is_zero=False) "
                   f"-- 691's difference is NOT shared by this nearby mid-size prime")
            else:
                fail(f"S-ED-7 control prime={p}: does NOT match the general-prime pattern "
                     f"(A12_ihara={a12}, D_is_zero={d_is_zero}) -- raw fact, needs 司令塔/数学者 attention")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (all cert-internal stop_code/canary/fixture predicates "
              "re-derive correctly from raw fields; this is a self-consistency check of the cert, "
              "NOT a mathematical validation of Definition C-1 itself -- see report to 司令塔)")
        sys.exit(0)


if __name__ == "__main__":
    main()
