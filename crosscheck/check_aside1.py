#!/usr/bin/env python3
# crosscheck/check_aside1.py
# Independent checker for the ASIDE-1 per-prime certs (裁定699 part2,
# docs/notes/aside_measurement_design_v1.md SS5/SS7 verbatim). Reads ONLY
# the cert JSON files -- does NOT import search/aside1_run_single_prime.py
# or search/edim_semidirect_v1.py (search/crosscheck separation). Re-derives
# every stop-rule/canary predicate from the raw per-prime fields in the
# cert and compares against what the cert itself recorded.
import json
import sys
import glob

CERT_GLOB = "search/certs/aside1_prime_*_v1_20260806.json"
GENERAL_PRIMES = {2147483647, 998244353}
SPECIAL_PRIME = 691


def main():
    fails = []

    def fail(msg):
        fails.append(msg)
        print("[FAIL]", msg)

    def ok(msg):
        print("[PASS]", msg)

    paths = sorted(glob.glob(CERT_GLOB))
    if not paths:
        fail("no aside1 cert files found")
        print("CROSSCHECK RESULT: FAIL (0 issues would be wrong -- no input)")
        sys.exit(1)

    certs = {}
    for path in paths:
        doc = json.load(open(path, encoding="utf-8"))
        certs[doc["prime"]] = doc
        if doc.get("schema") != "shadow-atelier/aside1/v1":
            fail(f"{path}: schema mismatch")
        else:
            ok(f"{path}: schema = shadow-atelier/aside1/v1")

    print()
    print(f"=== primes present: {sorted(certs.keys())} ===")

    # S-AS-5: no verdict language anywhere in the cert text (scan raw JSON
    # text for the 4 forbidden strings, independent re-scan).
    forbidden = ["不均衡", "SYN-0", "k*", "段差"]
    for prime, doc in certs.items():
        blob = json.dumps(doc, ensure_ascii=False)
        for word in forbidden:
            if word in blob:
                fail(f"prime={prime}: forbidden verdict text '{word}' found in cert -- S-AS-5 VERDICT_IN_CODE")
    ok("S-AS-5 rescan: no forbidden verdict strings in any cert")

    # Per-prime re-derivation of canaries/stop rules from raw fields only.
    for prime, doc in sorted(certs.items()):
        stage_a = doc.get("stage_A_sigma", {})
        # S-AS-1: dim S_m == 1 for all m in {3,5,7,9}
        sigma_ok_all = all(stage_a.get(str(m), stage_a.get(m, {})).get("S_dim") == 1
                            for m in (3, 5, 7, 9)) if stage_a else None
        rederived_stop = None
        if sigma_ok_all is False:
            rederived_stop = "SIGMA_NONUNIQUE"

        stage_b = doc.get("stage_B_model_weight_graded")
        stage_c = doc.get("stage_C_free_lie_depth_graded")

        if rederived_stop is None and stage_b is not None and stage_c is not None:
            A12 = stage_b.get("A12")
            A12_depth2 = stage_c.get("A12_depth2")
            is_general = prime in GENERAL_PRIMES
            if is_general:
                if not (A12 == 2 and A12_depth2 == 2):
                    rederived_stop = "CALIBRATION_FAIL"
            elif prime == SPECIAL_PRIME:
                if A12_depth2 != 1:
                    rederived_stop = "CONGRUENCE_NOT_REPRODUCED"
            if rederived_stop is None and A12 is not None:
                # S-AS-4 requires comparing against S_12, which this
                # measurement never computes (out of ASIDE-1 scope) -- so
                # only the crude A12<=2 sanity bound (span of 2 vectors) is
                # checkable here, matching the driver's own bound check.
                if A12 > 2:
                    rederived_stop = "IMPOSSIBLE_CELL"

        cert_stop = doc.get("stop_code")
        if cert_stop != rederived_stop:
            fail(f"prime={prime}: stop_code cert={cert_stop!r} rederived={rederived_stop!r}")
        else:
            ok(f"prime={prime}: stop_code={cert_stop!r} rederived matches")

    print()
    print("=== raw per-prime table (re-read from cert only) ===")
    for prime, doc in sorted(certs.items()):
        b = doc.get("stage_B_model_weight_graded", {})
        c = doc.get("stage_C_free_lie_depth_graded", {})
        print(f"  prime={prime}: A12={b.get('A12')} A12_depth2={c.get('A12_depth2')} "
              f"stop_code={doc.get('stop_code')} elapsed_sec={doc.get('total_elapsed_sec')}")

    # cross-prime consistency the design doc itself asks for (S-ED-7-style,
    # but only for the primes actually present in this dispatch: canary
    # (b) needs BOTH general primes to agree with each other, independent
    # of whether 691 passed its own canary).
    general_present = {p: certs[p] for p in GENERAL_PRIMES if p in certs}
    if len(general_present) == 2:
        a12_vals = {p: d.get("stage_B_model_weight_graded", {}).get("A12") for p, d in general_present.items()}
        a12d2_vals = {p: d.get("stage_C_free_lie_depth_graded", {}).get("A12_depth2") for p, d in general_present.items()}
        if len(set(a12_vals.values())) == 1 and len(set(a12d2_vals.values())) == 1:
            ok(f"the 2 general primes AGREE with each other: A12={list(a12_vals.values())[0]} "
               f"A12_depth2={list(a12d2_vals.values())[0]}")
        else:
            fail(f"the 2 general primes DISAGREE: A12={a12_vals} A12_depth2={a12d2_vals}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (all cert-internal stop_code/canary predicates re-derive correctly "
              "from raw fields; this is a self-consistency check of the cert, NOT a mathematical validation "
              "of the disputed Ihara-bracket construction in stage C -- see report to 司令塔)")
        sys.exit(0)


if __name__ == "__main__":
    main()
