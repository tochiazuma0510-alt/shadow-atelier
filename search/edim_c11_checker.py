#!/usr/bin/env python3
"""
edim_c11_checker.py -- independent (no edim_semidirect_v1/edim_run_c11
import) consistency checker for search/certs/edim_c11_run_v1_20260806.json.
Re-verifies the cert's own bookkeeping, the frozen prediction doc's DERIVED
H11=62 and scored S11=2, the CALIBRATION_FAIL/STOP discipline, the S-ED-4
arbitration-only-on-disagreement rule, and the "k=12 not run" claim --
WITHOUT recomputing the underlying linear algebra (that independent
recomputation is the two-large-prime agreement already recorded per-prime
in the cert, k=3..11 each).
"""
import json
import sys

CERT_PATH = "search/certs/edim_c11_run_v1_20260806.json"
LARGE_PRIMES = [2147483647, 998244353]
EXPECTED_H = {"3": 1, "4": 1, "5": 2, "6": 3, "7": 6, "8": 10, "9": 19, "10": 33, "11": 62}
EXPECTED_S = {"3": 1, "4": 0, "5": 1, "6": 0, "7": 1, "8": 1, "9": 1, "10": 1, "11": 2}


def main():
    d = json.load(open(CERT_PATH, encoding="utf-8"))
    problems = []

    if d.get("primes") != LARGE_PRIMES:
        problems.append(f"primes != required scoring pair: {d.get('primes')}")
    if d.get("dim_t_11") != 16290:
        problems.append(f"dim_t_11 != 16290 (Witt(3,11)+Witt(2,11)): {d.get('dim_t_11')}")
    if d.get("k12_not_run") is not True:
        problems.append("k12_not_run is not True")

    per_prime = d.get("per_prime", {})
    if set(per_prime.keys()) != {str(p) for p in LARGE_PRIMES}:
        problems.append(f"per_prime keys unexpected: {list(per_prime.keys())}")

    mismatches = []
    for p_str, row in per_prime.items():
        if row.get("mismatch_at_k") is not None:
            mismatches.append((p_str, row["mismatch_at_k"]))
            continue
        results = row.get("results", {})
        # keys may be int or str depending on json round-trip; normalize
        results = {str(k): v for k, v in results.items()}
        for k in EXPECTED_H:
            if k not in results:
                if int(k) > 11:
                    continue
                problems.append(f"prime {p_str}: missing k={k} in results (no mismatch recorded either)")
                continue
            row_k = results[k]
            if row_k["H_dim"] != EXPECTED_H[k] or row_k["S_dim"] != EXPECTED_S[k]:
                problems.append(f"prime {p_str} k={k}: H={row_k['H_dim']},S={row_k['S_dim']} != "
                                 f"expected H={EXPECTED_H[k]},S={EXPECTED_S[k]}")

    if mismatches and d.get("calibration_fail_at_k") is None:
        problems.append(f"per-prime mismatch(es) recorded {mismatches} but calibration_fail_at_k is None")

    if d.get("calibration_fail_at_k") is not None:
        if d.get("scoring") is not None:
            problems.append("calibration_fail_at_k is set but scoring is not None -- "
                             "CALIBRATION_FAIL should suppress S reporting")
    else:
        # no calibration fail -- both primes should agree at k=11 (possibly via arbitration)
        h11_vals = set()
        s11_vals = set()
        for p_str, row in per_prime.items():
            results = {str(k): v for k, v in row.get("results", {}).items()}
            if "11" in results:
                h11_vals.add(results["11"]["H_dim"])
                s11_vals.add(results["11"]["S_dim"])
        h11_agree = len(h11_vals) == 1
        s11_agree = len(s11_vals) == 1

        arb = d.get("k11_arbitration")
        if not s11_agree and arb is None:
            problems.append(f"k=11 S disagreement between primes {s11_vals} but no arbitration record present")
        if arb is not None and s11_agree:
            problems.append("arbitration record present but the two designated primes already agreed on S11 "
                             "-- arbitration should only fire on disagreement")

        sc = d.get("scoring")
        if sc is None:
            problems.append("no calibration_fail_at_k but scoring is None")
        else:
            if sc.get("H_measured") != 62 or sc.get("H_predicted") != 62 or not sc.get("H_match"):
                problems.append(f"scoring H fields wrong: {sc}")
            if sc.get("S_predicted") != 2:
                problems.append(f"scoring S_predicted != 2: {sc}")
            if sc.get("S_match") != (sc.get("S_measured") == sc.get("S_predicted")):
                problems.append("S_match flag inconsistent with measured/predicted")
            if h11_agree and list(h11_vals)[0] != 62:
                problems.append(f"both primes agree on H11 but it isn't 62: {h11_vals}")

    result = {"schema": "edim-c11-checker/v1", "cert_checked": CERT_PATH,
              "problems": problems, "all_checks_pass": len(problems) == 0}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    with open("search/certs/edim_c11_checker_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
