#!/usr/bin/env python3
# crosscheck/check_dig_r0_1.py
# Independent checker for search/certs/dig_r0_1_v1_20260806.json (DIG-R0-1,
# 裁定720, docs/notes/ribet_dig_campaign_v1_addendum_a.md SS2.7). Reads
# ONLY the cert JSON -- does NOT import/execute the GAP driver
# (search/probe/dig_r0_1/dig_r0_1.g) or any GAP process (search/crosscheck
# separation: this is a from-scratch, GAP-independent re-derivation in pure
# Python of every closed-form prediction the addendum froze in advance, plus
# internal consistency checks on the cert's own recorded match flags).
#
# What this crosscheck CAN independently re-derive (pure number theory, no
# group theory library needed): all the closed-form predicted VALUES
# (6p^2, 2p, (-2,1) mod p, (1,-2) mod p, p-1, etc.) and the cert's own
# "_match"/"_is_1"/"_is_C2" boolean flags against those values. It does NOT
# re-run the GAP linear algebra itself (that would require reimplementing
# the same matrix computations -- this checker instead verifies the
# ARITHMETIC of the predictions and the INTERNAL CONSISTENCY of what the
# cert reports, which is the standard cross-check pattern used throughout
# this project's aside*/checker pairs).
import json
import sys
from math import gcd

CERT_PATH = "search/certs/dig_r0_1_v1_20260806.json"
EXPECTED_PRIMES = [5, 7, 13, 691]
CALIBRATION_PRIMES = {5, 7, 13}


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

    if doc.get("schema") != "shadow-atelier/dig_r0_1/v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/dig_r0_1/v1")

    if doc.get("universe_primes") != EXPECTED_PRIMES:
        fail(f"universe_primes={doc.get('universe_primes')} != prereg'd {EXPECTED_PRIMES}")
    else:
        ok(f"universe_primes matches prereg: {EXPECTED_PRIMES}")

    forbidden = ["不均衡", "SYN-0", "k*", "段差"]
    blob = json.dumps(doc, ensure_ascii=False)
    for word in forbidden:
        if word in blob:
            fail(f"forbidden verdict text '{word}' found -- S-AS-5-style VERDICT_IN_CODE")
    ok("no forbidden verdict strings found in cert")

    results = doc.get("results", [])
    primes_present = [r["prime"] for r in results]
    if primes_present != EXPECTED_PRIMES:
        fail(f"primes present {primes_present} != expected {EXPECTED_PRIMES}")
    else:
        ok(f"all 4 primes present in order: {primes_present}")

    all_pass_flags = []

    for r in results:
        p = r["prime"]
        is_calib = p in CALIBRATION_PRIMES
        print(f"\n--- prime={p} (calibration={is_calib}) ---")

        # R0-a
        a = r["R0a"]
        pred_size = 6 * p * p
        if a["size_predicted"] != pred_size:
            fail(f"p={p}: R0a.size_predicted={a['size_predicted']} != 6p^2={pred_size}")
        rederived_size_match = (a["size_R0_full_generators"] == pred_size)
        if rederived_size_match != a["size_match"]:
            fail(f"p={p}: R0a.size_match={a['size_match']} but rederived={rederived_size_match}")
        else:
            ok(f"p={p}: R0a |R0(p)|={a['size_R0_full_generators']} == 6p^2={pred_size}")
        if a["R0ab_is_C2"] != (a["R0ab_invariants"] == [2]):
            fail(f"p={p}: R0a.R0ab_is_C2 inconsistent with R0ab_invariants={a['R0ab_invariants']}")
        if a["Z_size_is_1"] != (a["Z_size"] == 1):
            fail(f"p={p}: R0a.Z_size_is_1 inconsistent with Z_size={a['Z_size']}")
        if a["Phi_size_is_1"] != (a["Phi_size"] == 1):
            fail(f"p={p}: R0a.Phi_size_is_1 inconsistent with Phi_size={a['Phi_size']}")
        if not (a["R0ab_is_C2"] and a["Z_size_is_1"] and a["Phi_size_is_1"]):
            fail(f"p={p}: R0a structural predictions (R0ab=C2, |Z|=1, |Phi|=1) not all confirmed")
        else:
            ok(f"p={p}: R0a structural predictions (R0ab=C2, |Z|=1, |Phi|=1) all confirmed")
        if not is_calib and "direct_linear_algebra" not in a["method"]:
            fail(f"p={p}: expected direct_linear_algebra method at non-calibration prime, "
                 f"got method={a['method']!r} -- heavy generic GAP method may have been used at scale")
        if is_calib and "gap_native" not in a["method"]:
            fail(f"p={p}: expected gap_native method at calibration prime, got {a['method']!r}")
        if not is_calib:
            ok(f"p={p}: R0a used direct_linear_algebra method (heavy generic GAP methods avoided at scale)")

        # R0-b
        b = r["R0b"]
        if b["size_predicted"] != pred_size:
            fail(f"p={p}: R0b.size_predicted={b['size_predicted']} != 6p^2={pred_size}")
        if (b["size_UW"] == pred_size) != b["generates"]:
            fail(f"p={p}: R0b.generates inconsistent with size_UW vs predicted")
        elif not b["generates"]:
            fail(f"p={p}: R0b (2,3)-generation by (U,W) FAILED")
        else:
            ok(f"p={p}: R0b (U,W) generates R0(p), Size=<U,W>={b['size_UW']}")

        # R0-c
        c = r["R0c"]
        pred_n = 2 * p
        if c["predicted"] != pred_n:
            fail(f"p={p}: R0c.predicted={c['predicted']} != 2p={pred_n}")
        if (c["n"] == pred_n) != c["match"]:
            fail(f"p={p}: R0c.match inconsistent")
        elif not c["match"]:
            fail(f"p={p}: R0c n={c['n']} != predicted 2p={pred_n}")
        else:
            ok(f"p={p}: R0c n=ord(s1)={c['n']} == 2p")

        # R0-d
        d = r["R0d"]
        pred_xbar = [(p - 2) % p, 1]
        pred_ybar = [1, (p - 2) % p]
        if d["xbar_predicted"] != pred_xbar:
            fail(f"p={p}: R0d.xbar_predicted={d['xbar_predicted']} != rederived {pred_xbar}")
        if d["ybar_predicted"] != pred_ybar:
            fail(f"p={p}: R0d.ybar_predicted={d['ybar_predicted']} != rederived {pred_ybar}")
        if not (d["xbar_match"] and d["ybar_match"]):
            fail(f"p={p}: R0d xbar/ybar coordinates do not match prediction")
        else:
            ok(f"p={p}: R0d xbar={d['xbar']}==(-2,1 mod p), ybar={d['ybar']}==(1,-2 mod p)")
        # independence: rederive det from xbar,ybar directly
        xb, yb = d["xbar"], d["ybar"]
        rederived_det = (xb[0] * yb[1] - xb[1] * yb[0]) % p
        if rederived_det != d["independence_det_mod_p"]:
            fail(f"p={p}: R0d det rederived={rederived_det} != cert={d['independence_det_mod_p']}")
        if (rederived_det != 0) != d["independent"]:
            fail(f"p={p}: R0d.independent inconsistent with det")
        elif not d["independent"]:
            fail(f"p={p}: R0d xbar,ybar NOT independent (det=0)")
        else:
            ok(f"p={p}: R0d xbar,ybar independent (det={rederived_det} mod {p})")
        if not (d["xbar_lin_part_is_identity"] and d["ybar_lin_part_is_identity"]):
            fail(f"p={p}: R0d xbar/ybar linear part not identity (s1^2/s2^2 not pure translations)")

        # R0-e
        e = r["R0e"]
        if e["m_range"] != [0, p - 1]:
            fail(f"p={p}: R0e.m_range={e['m_range']} != [0,p-1]=[0,{p-1}]")
        if e["num_m_tested"] != p:
            fail(f"p={p}: R0e.num_m_tested={e['num_m_tested']} != p={p}")
        if not e["m_zero_included"]:
            fail(f"p={p}: R0e canary (b) violated -- m=0 must be included")
        if not e["all_m_pass"] or e["num_fail"] != 0:
            fail(f"p={p}: R0e braid relation FAILED for {e['num_fail']} value(s) of m: "
                 f"{e.get('fail_list_head')}")
        else:
            ok(f"p={p}: R0e braid relation ABA=BAB holds for all {p} values of m (incl. m=0)")

        # R0-f
        f = r["R0f"]
        if f["N_ord"] != p:
            fail(f"p={p}: R0f.N_ord={f['N_ord']} != p")
        rederived_GT = sum(1 for mm in range(p) if gcd(2 * mm + 1, p) == 1)
        if rederived_GT != p - 1:
            fail(f"p={p}: rederived GT_count={rederived_GT} != p-1={p-1} (arithmetic sanity failure)")
        if f["GT_count"] != rederived_GT:
            fail(f"p={p}: R0f.GT_count={f['GT_count']} != independently rederived {rederived_GT}")
        elif not f["GT_count_match"]:
            fail(f"p={p}: R0f GT_count_match=False")
        else:
            ok(f"p={p}: R0f |GT(N)|={f['GT_count']} == p-1={p-1} (independently rederived via gcd count)")

        # R0-g
        g = r["R0g"]
        if not (g["beta_U_eq_U"] and g["beta_W_eq_Winv"]):
            fail(f"p={p}: R0g beta(U)=U or beta(W)=W^-1 FAILED")
        else:
            ok(f"p={p}: R0g beta(U)=U and beta(W)=W^-1 confirmed")
        if not g["homomorphism_spot_check_all_pass"]:
            fail(f"p={p}: R0g homomorphism spot-check FAILED")
        if is_calib and not g["homomorphism_spot_check_exhaustive_small_group"]:
            fail(f"p={p}: expected exhaustive homomorphism check at calibration prime")
        if not is_calib and g["homomorphism_spot_check_random_samples"] < 1:
            fail(f"p={p}: expected >=1 random homomorphism spot-check at non-calibration prime")

        # R0-h
        h = r["R0h"]
        if p in (5, 7):
            if not h.get("ran"):
                fail(f"p={p}: R0h should have run (p in {{5,7}}) but ran=False")
            elif h.get("num_aut_orbits") != 1 or not h.get("match"):
                fail(f"p={p}: R0h num_aut_orbits={h.get('num_aut_orbits')} != predicted 1")
            else:
                ok(f"p={p}: R0h Aut-orbit count of generating (2,3)-pairs = 1 "
                   f"(over {h.get('num_generating_pairs')} generating pairs)")
        else:
            if h.get("ran"):
                fail(f"p={p}: R0h should NOT have run (spec restricts to p in {{5,7}}) but ran=True")
            else:
                ok(f"p={p}: R0h correctly skipped (spec restricts to p in {{5,7}})")

        p_all_pass = (a["size_match"] and a["R0ab_is_C2"] and a["Z_size_is_1"] and a["Phi_size_is_1"] and
                      b["generates"] and c["match"] and d["xbar_match"] and d["ybar_match"] and
                      d["independent"] and e["all_m_pass"] and f["GT_count_match"] and
                      g["beta_U_eq_U"] and g["beta_W_eq_Winv"] and g["homomorphism_spot_check_all_pass"])
        all_pass_flags.append((p, p_all_pass))

    print()
    print("=== summary (re-read + rederived from cert only) ===")
    for p, ok_flag in all_pass_flags:
        print(f"  p={p}: all_predictions_confirmed={ok_flag}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (all closed-form predictions independently rederived in pure "
              "Python and confirmed against the cert's raw values; this does NOT re-run the GAP linear "
              "algebra itself -- see report to 司令塔)")
        sys.exit(0)


if __name__ == "__main__":
    main()
