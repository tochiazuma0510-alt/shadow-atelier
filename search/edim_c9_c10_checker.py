#!/usr/bin/env python3
"""
edim_c9_c10_checker.py -- independent (no edim_semidirect_v1/edim_run_c9_c10
import) consistency checker for search/certs/edim_c9_c10_run_v1_20260806.json.
Re-verifies the cert's own bookkeeping, the frozen prediction doc's DERIVED H
values, S-ED-4/regression-gate discipline, and the "k=11,12 not run" claim,
without recomputing the underlying linear algebra.
"""
import json
import sys

CERT_PATH = "search/certs/edim_c9_c10_run_v1_20260806.json"

EXPECTED_H = {"7": 6, "8": 10, "9": 19, "10": 33}
EXPECTED_S = {"7": 1, "8": 1, "9": 1, "10": 1}
LARGE_PRIMES = [2147483647, 998244353]


def main():
    d = json.load(open(CERT_PATH, encoding="utf-8"))
    problems = []

    if d.get("primes") != LARGE_PRIMES and "primes" in d:
        problems.append(f"primes != required large-prime pair: {d.get('primes')}")

    # regression gate: must have run and passed BEFORE any k9/k10 content exists
    if not d.get("regression_ok"):
        if "k9_results_by_prime" in d and d["k9_results_by_prime"]:
            problems.append("regression_ok=False but k9_results_by_prime is populated -- "
                             "gate should have stopped the run before k=9")
        # nothing else to check in this branch; a failed-regression cert is
        # expected to be minimal
        print(json.dumps({"schema": "edim-c9-c10-checker/v1", "problems": problems,
                          "all_checks_pass": len(problems) == 0,
                          "note": "cert reports regression_ok=False -- checked only the stop-gate "
                                  "invariant, no scoring to verify"}, indent=2, ensure_ascii=False))
        sys.exit(0 if not problems else 1)

    rr = d["regression_report"]
    for k in ("7", "8"):
        entry = rr.get(k) or rr.get(int(k))
        if entry is None:
            problems.append(f"regression_report missing k={k}")
            continue
        per_prime = entry["per_prime"]
        vals = list(per_prime.values())
        if len(set(tuple(v) for v in vals)) != 1:
            problems.append(f"k={k}: regression per_prime values don't actually agree: {per_prime}")
        if not entry["two_prime_agree"]:
            problems.append(f"k={k}: two_prime_agree=False but regression_ok=True overall")
        h, s = vals[0]
        if h != EXPECTED_H[k] or s != EXPECTED_S[k]:
            problems.append(f"k={k}: regression values {h},{s} don't match known prior "
                             f"H={EXPECTED_H[k]},S={EXPECTED_S[k]}")
        if not entry["matches_prior_small_prime_result"]:
            problems.append(f"k={k}: matches_prior_small_prime_result=False but values match by "
                             f"direct comparison -- flag inconsistency")

    # k=9
    if d.get("k9_calibration_fail_H9_mismatch"):
        if d.get("k9_scoring") is not None:
            problems.append("k9_calibration_fail_H9_mismatch=True but k9_scoring is not None "
                             "-- CALIBRATION_FAIL should suppress S reporting")
    else:
        k9r = d.get("k9_results_by_prime", {})
        if len(k9r) != 2:
            problems.append(f"k9_results_by_prime should have 2 entries, has {len(k9r)}")
        else:
            vals9 = [(v["H_dim"], v["S_dim"]) for v in k9r.values()]
            if len(set(vals9)) != 1:
                problems.append(f"k=9: per-prime results don't agree: {k9r}")
            h9, s9 = vals9[0]
            if h9 != EXPECTED_H["9"]:
                problems.append(f"k=9: H_dim={h9} != derived-expected {EXPECTED_H['9']} but "
                                 f"k9_calibration_fail_H9_mismatch is not True")
            sc = d.get("k9_scoring")
            if sc is None:
                problems.append("k=9: not a calibration fail but k9_scoring is None")
            else:
                if sc["S_measured"] != s9 or sc["H_measured"] != h9:
                    problems.append("k=9: k9_scoring doesn't match k9_results_by_prime")
                if sc["S_match"] != (sc["S_measured"] == EXPECTED_S["9"]):
                    problems.append("k=9: S_match flag inconsistent")

        # k=10 only checked if k9 didn't fail calibration
        if d.get("k10_calibration_fail_H10_mismatch"):
            if d.get("k10_scoring") is not None:
                problems.append("k10_calibration_fail_H10_mismatch=True but k10_scoring is not None")
        elif "k10_results_by_prime" in d and d["k10_results_by_prime"]:
            k10r = d["k10_results_by_prime"]
            if len(k10r) != 2:
                problems.append(f"k10_results_by_prime should have 2 entries, has {len(k10r)}")
            else:
                vals10 = [(v["H_dim"], v["S_dim"]) for v in k10r.values()]
                if len(set(vals10)) != 1:
                    problems.append(f"k=10: per-prime results don't agree: {k10r}")
                h10, s10 = vals10[0]
                if h10 != EXPECTED_H["10"]:
                    problems.append(f"k=10: H_dim={h10} != derived-expected {EXPECTED_H['10']} but "
                                     f"k10_calibration_fail_H10_mismatch is not True")
                sc10 = d.get("k10_scoring")
                if sc10 is None:
                    problems.append("k=10: not a calibration fail but k10_scoring is None")
                else:
                    if sc10["S_measured"] != s10 or sc10["H_measured"] != h10:
                        problems.append("k=10: k10_scoring doesn't match k10_results_by_prime")
                    if sc10["S_match"] != (sc10["S_measured"] == EXPECTED_S["10"]):
                        problems.append("k=10: S_match flag inconsistent")

    if d.get("k11_k12_not_run") is not True:
        problems.append("k11_k12_not_run is not True")
    for blob_key in ("k9_results_by_prime", "k10_results_by_prime", "regression_report"):
        blob = d.get(blob_key)
        if not blob:
            continue
        keys = blob.keys() if isinstance(blob, dict) else []
        for k in keys:
            if k.isdigit() and int(k) >= 11:
                problems.append(f"{blob_key} contains k={k}, violating the k=11+ stop instruction")

    result = {"schema": "edim-c9-c10-checker/v1", "cert_checked": CERT_PATH,
              "problems": problems, "all_checks_pass": len(problems) == 0}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    with open("search/certs/edim_c9_c10_checker_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
