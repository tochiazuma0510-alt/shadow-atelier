#!/usr/bin/env python3
"""
edim_run_c9_c10_v4_aggregate.py -- combines the 4 per-(k,prime) certs from
edim_run_c9_c10_v4_single_kp.py (k in {9,10} x prime in {2147483647,
998244353}) into the final scoring cert.

Regression (k=7,8) is NOT re-run here (v4 dropped it per its own docstring
-- relies on v2/v3's already-recorded regression PASS, commit 70879b0/
ca95afd, since the public interface of edim_semidirect_v1.py used by v4 is
the same one v2/v3 regression-tested; a genuinely different Sol-accelerated
edim_semidirect_v1.py would need its OWN regression confirmation, done
locally per 司令塔's instruction #2 BEFORE this workflow is dispatched with
that version -- see the "Sol-branch regression battery" note in the
instruction this script was commissioned under).

CALIBRATION_FAIL/STOP discipline unchanged: if H9 or H10 (either prime)
don't match the derived values 19/33, STOP before reporting S.
"""
import json
import sys

LARGE_PRIMES = [2147483647, 998244353]
KS = [9, 10]
EXPECTED_H = {9: 19, 10: 33}
EXPECTED_S = {9: 1, 10: 1}


def main():
    per_kp = {}
    for k in KS:
        for p in LARGE_PRIMES:
            path = f"search/certs/edim_c9_c10_k{k}_prime_{p}_v4_20260806.json"
            with open(path, encoding="utf-8") as f:
                per_kp[(k, p)] = json.load(f)

    scoring = {}
    calibration_fail = None
    for k in KS:
        h_vals = {p: per_kp[(k, p)]["H_dim"] for p in LARGE_PRIMES}
        s_vals = {p: per_kp[(k, p)]["S_dim"] for p in LARGE_PRIMES}
        h_agree = len(set(h_vals.values())) == 1
        s_agree = len(set(s_vals.values())) == 1
        h0 = next(iter(h_vals.values()))

        if not h_agree:
            calibration_fail = k
            scoring[k] = {"STOP": "H_TWO_PRIME_DISAGREEMENT", "per_prime_H": {str(p): v for p, v in h_vals.items()}}
            break
        if h0 != EXPECTED_H[k]:
            calibration_fail = k
            scoring[k] = {"STOP": "CALIBRATION_FAIL", "H_measured": h0, "H_predicted": EXPECTED_H[k]}
            break

        if not s_agree:
            # H confirmed derived-correct and two-prime-agreed, but S
            # disagrees between primes -- S-ED-4: implementation-bug-first
            # suspicion, do not silently pick a winner.
            scoring[k] = {"two_prime_agree": False, "H_measured": h0, "H_predicted": EXPECTED_H[k], "H_match": True,
                          "per_prime_S": {str(p): v for p, v in s_vals.items()},
                          "S_UNRESOLVED_DISAGREEMENT": True}
            continue

        s0 = next(iter(s_vals.values()))
        scoring[k] = {"two_prime_agree": True, "H_measured": h0, "H_predicted": EXPECTED_H[k], "H_match": True,
                      "S_measured": s0, "S_predicted": EXPECTED_S[k], "S_match": (s0 == EXPECTED_S[k])}

    peak_mb = max(v["peak_memory_traced_mb"] for v in per_kp.values())
    total_wall_if_sequential = sum(v["total_elapsed_sec"] for v in per_kp.values())
    total_wall_actual_parallel = max(v["total_elapsed_sec"] for v in per_kp.values())

    out = {
        "schema": "edim-c9-c10-run/v4",
        "solver_provenance_note": "See each per-(k,prime) cert's own 'solver' field for whether a "
                                   "Sol-accelerated edim_semidirect_v1.py (便112e) was in effect for "
                                   "this specific run.",
        "authorization": "docs/notes/b_type_synthesis_design_v1_addendum_edim9_11_prediction.md "
                          "(commit 026dff8); 裁定658/660 (司令塔, this session); v4 = 4-way (k x prime) "
                          "GHA matrix, further split from v3 (per-prime only, k=7..10 sequential) after "
                          "v3's own local timing showed k=10 alone consuming most of a 60-min budget",
        "primes": LARGE_PRIMES, "ks": KS,
        "regression_k7_k8_status": "NOT RE-RUN in this aggregation -- relies on v2/v3's already-"
                                    "recorded PASS (commit 70879b0/ca95afd) against the same public "
                                    "interface. If edim_semidirect_v1.py changed (e.g. Sol speedup), "
                                    "that change must be regression-tested LOCALLY first per the "
                                    "commissioning instruction, before this workflow's cert can be "
                                    "trusted as more than 'per-(k,prime) raw numbers'.",
        "per_kp_full": {f"k{k}_p{p}": per_kp[(k, p)] for k in KS for p in LARGE_PRIMES},
        "scoring": scoring,
        "calibration_fail_at_k": calibration_fail,
        "peak_memory_traced_mb_max": peak_mb,
        "total_wall_sec_if_sequential": round(total_wall_if_sequential, 2),
        "total_wall_sec_actual_parallel": round(total_wall_actual_parallel, 2),
        "k11_k12_not_run": True,
    }

    with open("search/certs/edim_c9_c10_run_v4_20260806.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(json.dumps({k: v for k, v in out.items() if k != "per_kp_full"}, indent=2, ensure_ascii=False))

    if calibration_fail is not None:
        print(f"*** k={calibration_fail} STOP -- see scoring[{calibration_fail}] ***")
        sys.exit(1)

    print("EDIM_C9_C10_V4_AGGREGATE_DONE")


if __name__ == "__main__":
    main()
