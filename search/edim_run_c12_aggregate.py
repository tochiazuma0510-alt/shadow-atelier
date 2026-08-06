#!/usr/bin/env python3
"""
edim_run_c12_aggregate.py -- E-DIM12/691 ceremony aggregate (裁定656/692/693).

Combines whichever per-prime certs from edim_run_c12_single_prime.py are
present (the two general primes 2147483647/998244353 always; 677 and 701
ONLY if a separate S-ED-7 dispatch produced them -- this script does not
require them and does not fail if they are absent).

★ THIS SCRIPT WRITES NO INTERPRETIVE VERDICT TEXT. No "SYN-0", "k*=12",
"段差", "不均衡", "calibration passed/failed as a claim about the math" --
only raw H/S values, per-prime match flags against the frozen calibration
value H12=112, two-large-prime agreement, and the RAW FACT of whether
prime=691's S12 numerically differs from the two general primes' S12 (a
plain equality/inequality check, not a claim about what that means).
Interpretation belongs to 司令塔/数学者/Sol, per instruction.

CALIBRATION_FAIL/STOP discipline: if H12 != 112 for ANY prime present, or
if any prime's own per-prime cert reports a k<=11 mismatch or its own
calibration_fail_h12=true, this aggregator marks calibration_fail=true and
does NOT populate a "raw_691_vs_general" comparison (S12 is not meaningful
if the calibration failed).
"""
import json
import os
import sys

GENERAL_PRIMES = [2147483647, 998244353]
SPECIAL_PRIME = 691
CONDITIONAL_PRIMES = [677, 701]  # only included if their certs exist (S-ED-7 follow-up)


def load_if_exists(p):
    path = f"search/certs/edim_c12_691_prime_{p}_v1_20260806.json"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def main():
    per_prime = {}
    missing = []
    for p in GENERAL_PRIMES + [SPECIAL_PRIME]:
        d = load_if_exists(p)
        if d is None:
            missing.append(p)
        else:
            per_prime[p] = d

    conditional_present = {}
    for p in CONDITIONAL_PRIMES:
        d = load_if_exists(p)
        if d is not None:
            conditional_present[p] = d

    if missing:
        out = {
            "schema": "edim-c12-691-aggregate/v1",
            "status": "INCOMPLETE",
            "missing_primes": missing,
            "primes_present": sorted(per_prime.keys()),
        }
        with open("search/certs/edim_c12_691_aggregate_v1_20260806.json", "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        print("*** INCOMPLETE -- not all required per-prime certs present ***")
        sys.exit(1)

    calibration_fail = False
    for p, d in per_prime.items():
        if d.get("mismatch_at_k_le_11") is not None or d.get("calibration_fail_h12"):
            calibration_fail = True

    raw = {}
    for p in GENERAL_PRIMES + [SPECIAL_PRIME]:
        row12 = per_prime[p]["results"].get("12") or per_prime[p]["results"].get(12)
        raw[p] = {
            "H12": row12["H_dim"] if row12 else None,
            "S12": row12["S_dim"] if row12 else None,
            "H12_eq_112": (row12["H_dim"] == 112) if row12 else None,
            "elapsed_sec": row12["elapsed_sec"] if row12 else None,
            "peak_rss_mb": row12["peak_rss_mb"] if row12 else None,
        }

    two_general_H12_agree = None
    two_general_S12_agree = None
    s12_691_differs_from_general = None
    if not calibration_fail:
        h_general = {raw[p]["H12"] for p in GENERAL_PRIMES}
        s_general = {raw[p]["S12"] for p in GENERAL_PRIMES}
        two_general_H12_agree = (len(h_general) == 1)
        two_general_S12_agree = (len(s_general) == 1)
        if two_general_S12_agree:
            general_s12_value = next(iter(s_general))
            s12_691_differs_from_general = (raw[SPECIAL_PRIME]["S12"] != general_s12_value)

    conditional_raw = {}
    for p, d in conditional_present.items():
        row12 = d["results"].get("12") or d["results"].get(12)
        conditional_raw[p] = {
            "H12": row12["H_dim"] if row12 else None,
            "S12": row12["S_dim"] if row12 else None,
            "H12_eq_112": (row12["H_dim"] == 112) if row12 else None,
        }

    out = {
        "schema": "edim-c12-691-aggregate/v1",
        "prereg_refs": {
            "656": "provenance/LEDGER.md 裁定656",
            "692": "provenance/LEDGER.md 裁定692",
            "693": "provenance/LEDGER.md 裁定693",
        },
        "status": "COMPLETE",
        "general_primes": GENERAL_PRIMES,
        "special_prime": SPECIAL_PRIME,
        "H12_calibration_target": 112,
        "calibration_fail": calibration_fail,
        "raw_values_by_prime": raw,
        "two_general_primes_H12_agree": two_general_H12_agree,
        "two_general_primes_S12_agree": two_general_S12_agree,
        "s12_691_differs_from_general_primes_RAW_FACT": s12_691_differs_from_general,
        "conditional_primes_677_701_present": sorted(conditional_present.keys()),
        "conditional_primes_raw_values": conditional_raw,
        "k13_not_run": True,
        "note": "No interpretive verdict is written by this script (no SYN-0/k*/段差 language). "
                "Raw values and plain equality facts only; interpretation is 司令塔/数学者/Sol's task, "
                "per 裁定656/692/693's frozen judgment table (provenance/LEDGER.md).",
    }
    with open("search/certs/edim_c12_691_aggregate_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(json.dumps(out, indent=2, ensure_ascii=False))

    if calibration_fail:
        print("*** CALIBRATION_FAIL present in at least one per-prime cert -- see calibration_fail=true ***")
        sys.exit(1)

    print("EDIM_C12_691_AGGREGATE_DONE")


if __name__ == "__main__":
    main()
