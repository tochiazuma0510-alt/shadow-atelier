#!/usr/bin/env python3
"""
edim_c9_c10_v3_checker.py -- independent (no edim_semidirect_v1/
edim_run_c9_c10_v3_* import) consistency checker for search/certs/
edim_c9_c10_run_v3_20260806.json (the final k=9,10 scoring cert produced by
edim_run_c9_c10_v3_aggregate.py from the two per-prime certs). Re-verifies
the cert's own bookkeeping, the frozen prediction doc's values, and the
S-ED-4/regression-gate/CALIBRATION_FAIL discipline, WITHOUT recomputing the
underlying linear algebra (that independent recomputation is the two-large-
prime + three-total-prime -- including 65521 -- agreement already recorded
in the per-prime certs themselves).
"""
import json
import sys

CERT_PATH = "search/certs/edim_c9_c10_run_v3_20260806.json"
PER_PRIME_PATHS = {
    2147483647: "search/certs/edim_c9_c10_prime_2147483647_v3_20260806.json",
    998244353: "search/certs/edim_c9_c10_prime_998244353_v3_20260806.json",
}
CANARY_PRIME_PATH = "search/certs/edim_c9_c10_prime_65521_v3_20260806.json"

EXPECTED_H = {"3": 1, "4": 1, "5": 2, "6": 3, "7": 6, "8": 10, "9": 19, "10": 33}
EXPECTED_S = {"3": 1, "4": 0, "5": 1, "6": 0, "7": 1, "8": 1, "9": 1, "10": 1}
LARGE_PRIMES = [2147483647, 998244353]


def main():
    d = json.load(open(CERT_PATH, encoding="utf-8"))
    problems = []

    if d.get("primes") != LARGE_PRIMES:
        problems.append(f"primes != required scoring pair: {d.get('primes')}")

    # re-verify against the ORIGINAL per-prime cert files directly (not
    # trusting the aggregate cert's own copies)
    per_prime_raw = {}
    for p, path in PER_PRIME_PATHS.items():
        try:
            per_prime_raw[p] = json.load(open(path, encoding="utf-8"))
        except FileNotFoundError:
            problems.append(f"per-prime cert missing: {path}")
            continue
        if not per_prime_raw[p].get("regression_ok"):
            problems.append(f"prime {p}: source per-prime cert has regression_ok != True")
        for k in EXPECTED_H:
            row = per_prime_raw[p]["results"].get(k)
            if row is None:
                problems.append(f"prime {p}: missing k={k} in per-prime results")
                continue
            if row["H_dim"] != EXPECTED_H[k] or row["S_dim"] != EXPECTED_S[k]:
                problems.append(f"prime {p} k={k}: H={row['H_dim']},S={row['S_dim']} != "
                                 f"expected H={EXPECTED_H[k]},S={EXPECTED_S[k]}")

    # regression_report (k=7,8) cross-check against the raw per-prime data
    rr = d.get("regression_report", {})
    for k in ("7", "8"):
        entry = rr.get(k)
        if entry is None:
            problems.append(f"regression_report missing k={k}")
            continue
        for p in LARGE_PRIMES:
            if p not in per_prime_raw:
                continue
            raw_row = per_prime_raw[p]["results"][k]
            agg_row = entry["per_prime"].get(str(p))
            if agg_row is None or list(agg_row) != [raw_row["H_dim"], raw_row["S_dim"]]:
                problems.append(f"k={k} prime={p}: aggregate regression_report doesn't match "
                                 f"source per-prime cert ({agg_row} vs {[raw_row['H_dim'], raw_row['S_dim']]})")

    if not d.get("regression_ok"):
        problems.append("regression_ok is not True in the aggregate cert (source certs above show it "
                         "should be, per the re-derivation) -- OR this is an expected STOP cert, "
                         "check stop_reason")

    # scoring k=9,10
    for k in (9, 10):
        sc = d.get("scoring", {}).get(str(k)) or d.get("scoring", {}).get(k)
        if sc is None:
            if d.get("calibration_fail_at_k") == k:
                continue  # expected: scoring suppressed after CALIBRATION_FAIL
            problems.append(f"k={k}: no scoring entry and no calibration_fail_at_k={k}")
            continue
        if "S_UNRESOLVED_DISAGREEMENT" in sc:
            continue  # legitimate S-ED-4 disagreement report, not an error
        if sc.get("H_measured") != EXPECTED_H[str(k)]:
            problems.append(f"k={k}: scoring H_measured={sc.get('H_measured')} != {EXPECTED_H[str(k)]}")
        if sc.get("S_measured") is not None and sc.get("S_predicted") != EXPECTED_S[str(k)]:
            problems.append(f"k={k}: scoring S_predicted={sc.get('S_predicted')} != {EXPECTED_S[str(k)]}")
        if sc.get("S_match") != (sc.get("S_measured") == sc.get("S_predicted")):
            problems.append(f"k={k}: S_match flag inconsistent with measured/predicted")

    if d.get("k11_k12_not_run") is not True:
        problems.append("k11_k12_not_run is not True")

    # informational: canary prime (65521) status, not required for the
    # official scoring pair but part of the commissioned local battery
    canary_ok = None
    try:
        canary = json.load(open(CANARY_PRIME_PATH, encoding="utf-8"))
        canary_ok = canary.get("regression_ok")
    except FileNotFoundError:
        pass

    result = {"schema": "edim-c9-c10-v3-checker/v1", "cert_checked": CERT_PATH,
              "canary_prime_65521_regression_ok": canary_ok,
              "problems": problems, "all_checks_pass": len(problems) == 0}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    with open("search/certs/edim_c9_c10_v3_checker_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
