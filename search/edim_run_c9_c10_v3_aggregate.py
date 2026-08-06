#!/usr/bin/env python3
"""
edim_run_c9_c10_v3_aggregate.py -- combines the two per-prime certs written
by edim_run_c9_c10_v3_single_prime.py (one per LARGE_PRIME, run as parallel
GHA matrix jobs) into the final regression+scoring cert, applying the SAME
gating discipline as the single-process v2 driver would have: regression
(k=7,8) must two-prime-agree AND match the already-known values before k=9
is trusted; k=9 must not CALIBRATION_FAIL (H9!=19) before k=10 is reported;
k=10 must not CALIBRATION_FAIL (H10!=33) before S10 is reported.
"""
import json
import sys

LARGE_PRIMES = [2147483647, 998244353]
EXPECTED_H = {7: 6, 8: 10, 9: 19, 10: 33}
EXPECTED_S = {7: 1, 8: 1, 9: 1, 10: 1}


def main():
    per_prime = {}
    for p in LARGE_PRIMES:
        path = f"search/certs/edim_c9_c10_prime_{p}_v3_20260806.json"
        with open(path, encoding="utf-8") as f:
            per_prime[p] = json.load(f)

    regression_report = {}
    regression_ok = True
    for k in (7, 8):
        vals = {p: (per_prime[p]["results"][str(k)]["H_dim"], per_prime[p]["results"][str(k)]["S_dim"])
                for p in LARGE_PRIMES}
        agree = len(set(vals.values())) == 1
        h0, s0 = next(iter(vals.values()))
        matches_known = (h0 == EXPECTED_H[k] and s0 == EXPECTED_S[k])
        regression_report[k] = {"per_prime": {str(p): vals[p] for p in LARGE_PRIMES},
                                 "two_prime_agree": agree, "matches_prior_small_prime_result": matches_known}
        if not (agree and matches_known):
            regression_ok = False

    out = {
        "schema": "edim-c9-c10-run/v3",
        "solver": "sparse (docs/notes/edim_sparse_solver_design_v1.md, 裁定660 approved)",
        "authorization": "docs/notes/b_type_synthesis_design_v1_addendum_edim9_11_prediction.md "
                          "(commit 026dff8); 裁定658/660 (司令塔, this session); v3 = per-prime "
                          "PARALLEL GHA matrix jobs (v2's single-job sequential 2-prime run measured "
                          "~56min/prime locally -> ~110min+ sequential, too close to GHA timeout "
                          "margins; v3 halves wall time via parallelism)",
        "primes": LARGE_PRIMES,
        "regression_report": regression_report,
        "regression_ok": regression_ok,
    }

    if not regression_ok:
        out["scoring"] = {}
        out["calibration_fail_at_k"] = None
        out["stop_reason"] = "REGRESSION_FAILED"
        with open("search/certs/edim_c9_c10_run_v3_20260806.json", "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        print("*** REGRESSION FAILED -- STOP ***")
        sys.exit(1)

    scoring = {}
    calibration_fail = None
    for k in (9, 10):
        vals = {p: (per_prime[p]["results"][str(k)]["H_dim"], per_prime[p]["results"][str(k)]["S_dim"])
                for p in LARGE_PRIMES}
        agree = len(set(vals.values())) == 1
        h, s = next(iter(vals.values()))
        if h != EXPECTED_H[k]:
            calibration_fail = k
            break
        if not agree:
            # two primes disagree on S even though H matched -- S-ED-4:
            # implementation-bug-first suspicion, do not silently pick one
            scoring[k] = {"two_prime_agree": False, "per_prime": {str(p): vals[p] for p in LARGE_PRIMES},
                          "H_measured": h, "H_predicted": EXPECTED_H[k], "H_match": True,
                          "S_UNRESOLVED_DISAGREEMENT": True}
            continue
        scoring[k] = {"two_prime_agree": True, "H_measured": h, "H_predicted": EXPECTED_H[k], "H_match": True,
                      "S_measured": s, "S_predicted": EXPECTED_S[k], "S_match": (s == EXPECTED_S[k])}

    peak_mb = max(per_prime[p]["peak_memory_traced_mb"] for p in LARGE_PRIMES)
    total_wall_sec_if_sequential = sum(per_prime[p]["total_elapsed_sec"] for p in LARGE_PRIMES)
    total_wall_sec_parallel_actual = max(per_prime[p]["total_elapsed_sec"] for p in LARGE_PRIMES)

    out.update({
        "per_prime_full": per_prime,
        "scoring": scoring,
        "calibration_fail_at_k": calibration_fail,
        "peak_memory_traced_mb_max_across_primes": peak_mb,
        "total_wall_sec_if_run_sequentially": round(total_wall_sec_if_sequential, 2),
        "total_wall_sec_actual_parallel": round(total_wall_sec_parallel_actual, 2),
        "k11_k12_not_run": True,
        "note": "k=11,12 deferred: this run validates k=9,10 sparse-solver correctness+feasibility "
                "first; k=11 is a separate follow-up once this is confirmed.",
    })

    with open("search/certs/edim_c9_c10_run_v3_20260806.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(json.dumps({k: v for k, v in out.items() if k != "per_prime_full"}, indent=2, ensure_ascii=False))

    if calibration_fail is not None:
        print(f"*** k={calibration_fail} CALIBRATION_FAIL -- STOP ***")
        sys.exit(1)

    print("EDIM_C9_C10_V3_AGGREGATE_DONE")


if __name__ == "__main__":
    main()
