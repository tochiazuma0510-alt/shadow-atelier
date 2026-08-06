#!/usr/bin/env python3
"""
edim_run_c11.py -- E-DIM11 scoring run per 裁定691.

Frozen prediction (verbatim authority, commit 026dff8): docs/notes/
b_type_synthesis_design_v1_addendum_edim9_11_prediction.md --
  H11=62 (derived, CALIBRATION_FAIL/STOP if wrong), S11=2 (scored).

Reuses compute_H_S_at_k_safe from search/edim_run_c9_c10_v3_single_prime.py
(Sol's 112e H-first ambient rank accelerator) UNCHANGED -- does not
duplicate or modify that logic. Extends the sweep to k=11 (KMAX=11,
dim t_11=16,290 -- the first 5-digit-plus degree this accelerated solver
has been run at; memory is explicitly observed and recorded per
instruction, not just timing).

Runs the FULL k=3..11 stepwise sweep (same discipline as v3_single_prime:
stop at the FIRST k where H or S mismatches the frozen/derived value,
never report a later k's S after an earlier miss) for TWO large primes
(2147483647, 998244353), per 裁定658's designated pair ("k=9,10,11には
特異素数を加えない"). S-ED-4: if the two primes disagree at k=11 (H match
but S differs), a THIRD prime is used to arbitrate (chosen safe for the
accelerated solver's int64 arithmetic, matching the existing large-prime
safety margin already used elsewhere in this module).

k=12 is explicitly NOT run here (separate ceremony, 691-series primes,
裁定656 -- out of scope for this script).
"""
import json
import sys
import time

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed
from edim_run_c9_c10_v3_single_prime import compute_H_S_at_k_safe, peak_rss_mb

KMAX = 11
EXPECTED_H = {3: 1, 4: 1, 5: 2, 6: 3, 7: 6, 8: 10, 9: 19, 10: 33, 11: 62}
EXPECTED_S = {3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 1, 9: 1, 10: 1, 11: 2}
LARGE_PRIMES = [2147483647, 998244353]
ARBITRATION_PRIME = 998244353 + 0  # placeholder, replaced below if needed at runtime
# A genuine THIRD prime, distinct from both designated primes, kept in the
# same "safe for int64 accelerated arithmetic" family used throughout this
# module (large, but chosen with the same margin discipline as
# edim_run_c78.py's ARBITRATION_PRIME=29999999 precedent -- here we can
# safely use another prime of the same magnitude as the two designated ones
# since compute_H_S_at_k_safe's own internals already handle p up to ~2^31
# safely, per the overflow fixes earlier this session).
THIRD_ARBITRATION_PRIME = 1000000007


def run_one_prime(p, kmax=KMAX):
    t0 = time.time()
    h_alg = ed.GradedLie(2, kmax, p, sparse_degrees=set(range(1, kmax + 1)))
    build_elapsed = time.time() - t0
    print(f"p={p}: bases built in {build_elapsed:.1f}s", flush=True)

    results = {}
    mismatch_at_k = None
    for k in range(3, kmax + 1):
        tk0 = time.time()
        H_dim, S_dim, dim_n, dim_h, dim_t = compute_H_S_at_k_safe(k, None, h_alg, None, p)
        elapsed = round(time.time() - tk0, 3)
        h_match = (H_dim == EXPECTED_H[k])
        s_match = (S_dim == EXPECTED_S[k])
        results[k] = {"H_dim": H_dim, "S_dim": S_dim, "dim_n": dim_n, "dim_h": dim_h,
                     "dim_t": dim_t, "elapsed_sec": elapsed,
                     "H_predicted": EXPECTED_H[k], "S_predicted": EXPECTED_S[k],
                     "H_match": h_match, "S_match": s_match}
        rss_mb, rss_metric = peak_rss_mb()
        print(f"p={p} k={k}: H_dim={H_dim} S_dim={S_dim} dim_t={dim_t} elapsed={elapsed}s "
              f"peak_rss_mb={rss_mb:.1f}", flush=True)
        if not (h_match and s_match):
            mismatch_at_k = k
            print(f"*** p={p} k={k} MISMATCH -- STOP (no further k reported for this prime) ***", flush=True)
            break

    rss_peak_mb, rss_metric = peak_rss_mb()
    total_elapsed = time.time() - t0
    return {
        "prime": p, "build_elapsed_sec": round(build_elapsed, 2),
        "results": results, "mismatch_at_k": mismatch_at_k,
        "total_elapsed_sec": round(total_elapsed, 2),
        "peak_memory_mb": round(rss_peak_mb, 2), "memory_metric": rss_metric,
    }


def main():
    print("=== E-DIM11 scoring run (裁定691), full k=3..11 sweep, two designated primes ===", flush=True)
    per_prime = {}
    for p in LARGE_PRIMES:
        print(f"--- prime {p} ---", flush=True)
        per_prime[p] = run_one_prime(p)

    # per-k, per-prime comparison up through k=11 (or wherever a mismatch stopped a prime early)
    max_k_common = min(
        (max(per_prime[p]["results"].keys()) for p in LARGE_PRIMES), default=0)
    k11_agree = None
    h11 = s11 = None
    calibration_fail_at_k = None
    arbitration = None

    for p in LARGE_PRIMES:
        if per_prime[p]["mismatch_at_k"] is not None:
            calibration_fail_at_k = per_prime[p]["mismatch_at_k"]

    if calibration_fail_at_k is None:
        # both primes completed k=3..11 cleanly; compare k=11 specifically
        h_vals = {p: per_prime[p]["results"][11]["H_dim"] for p in LARGE_PRIMES}
        s_vals = {p: per_prime[p]["results"][11]["S_dim"] for p in LARGE_PRIMES}
        h_agree = len(set(h_vals.values())) == 1
        s_agree = len(set(s_vals.values())) == 1
        h11 = next(iter(h_vals.values()))

        if not h_agree:
            calibration_fail_at_k = 11
        elif h11 != EXPECTED_H[11]:
            calibration_fail_at_k = 11
        elif not s_agree:
            print(f"*** k=11 S DISAGREEMENT between designated primes ({s_vals}) -- "
                  f"S-ED-4 arbitration with prime {THIRD_ARBITRATION_PRIME} ***", flush=True)
            arb_result = run_one_prime(THIRD_ARBITRATION_PRIME, kmax=11)
            arb_h = arb_result["results"].get(11, {}).get("H_dim")
            arb_s = arb_result["results"].get(11, {}).get("S_dim")
            arbitration = {"prime": THIRD_ARBITRATION_PRIME, "H_dim": arb_h, "S_dim": arb_s,
                           "elapsed_sec": arb_result["total_elapsed_sec"],
                           "resolved": arb_s in s_vals.values()}
            if arb_h != EXPECTED_H[11]:
                calibration_fail_at_k = 11
            elif arb_s in s_vals.values():
                s11 = arb_s
                k11_agree = "resolved_by_arbitration"
            else:
                # arbitration disagrees with BOTH designated primes -- do
                # not pick a winner, report as unresolved for 司令塔/Sol
                k11_agree = "UNRESOLVED_EVEN_WITH_ARBITRATION"
        else:
            s11 = next(iter(s_vals.values()))
            k11_agree = True

    scoring = None
    if calibration_fail_at_k is None and s11 is not None:
        scoring = {"H_measured": h11, "H_predicted": EXPECTED_H[11], "H_match": (h11 == EXPECTED_H[11]),
                  "S_measured": s11, "S_predicted": EXPECTED_S[11], "S_match": (s11 == EXPECTED_S[11]),
                  "two_prime_agree_or_arbitrated": k11_agree}

    out = {
        "schema": "edim-c11-run/v1",
        "authorization": "docs/notes/b_type_synthesis_design_v1_addendum_edim9_11_prediction.md "
                          "(commit 026dff8, frozen IF-FIRST prediction); 裁定691 (司令塔, this session)",
        "solver": "Sol H-first ambient sparse rank accelerator (便112e), reused unchanged from "
                  "search/edim_run_c9_c10_v3_single_prime.py's compute_H_S_at_k_safe",
        "primes": LARGE_PRIMES,
        "dim_t_11": 16290,
        "dim_t_11_note": "first 5-digit-plus degree run with the accelerated solver -- memory "
                         "explicitly observed per instruction",
        "per_prime": {str(p): per_prime[p] for p in LARGE_PRIMES},
        "calibration_fail_at_k": calibration_fail_at_k,
        "k11_arbitration": arbitration,
        "scoring": scoring,
        "k12_not_run": True,
        "note": "k=12 explicitly NOT run (separate ceremony, 691-series primes, 裁定656).",
    }
    with open("search/certs/edim_c11_run_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(json.dumps({k: v for k, v in out.items() if k != "per_prime"}, indent=2, ensure_ascii=False))

    if calibration_fail_at_k is not None:
        print(f"*** k={calibration_fail_at_k} CALIBRATION_FAIL -- STOP, S NOT reported ***", flush=True)
        sys.exit(1)
    if scoring is None:
        print("*** k=11 UNRESOLVED (arbitration did not resolve) -- STOP ***", flush=True)
        sys.exit(1)

    print("EDIM_C11_RUN_DONE")


if __name__ == "__main__":
    main()
