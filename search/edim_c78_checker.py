#!/usr/bin/env python3
"""
edim_c78_checker.py -- independent (no edim_semidirect_v1 import) consistency
checker for search/certs/edim_c78_scoring_v1_20260806.json. Re-verifies the
cert's own internal bookkeeping and the frozen prediction doc's requirements
without recomputing the linear algebra (that recomputation is the THREE-PRIME
agreement already inside the cert itself -- this script's job is to catch
reporting/aggregation bugs, e.g. a scoring block that doesn't match the
underlying per-prime results, or S-ED-4 confirmation being claimed without
genuine three-way agreement).
"""
import hashlib
import json
import sys

CERT_PATH = "search/certs/edim_c78_scoring_v1_20260806.json"
PREREG_PATH = "docs/notes/b_type_synthesis_design_v1_addendum_edim78_prediction.md"

EXPECTED_H = {"7": 6, "8": 10}
EXPECTED_S = {"7": 1, "8": 1}


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    d = json.load(open(CERT_PATH, encoding="utf-8"))
    problems = []

    # S-ED-3: two primes present and small (<2^16)
    primes_small = d["primes_small"]
    if len(primes_small) != 2 or any(p >= 2**16 for p in primes_small):
        problems.append(f"primes_small not a valid S-ED-4 small-prime pair: {primes_small}")

    # S-ED-4: arbitration only claimed if small primes genuinely agreed, and
    # arbitration prime is >=2^16 ("large")
    if d["all_small_agree"]:
        if d["arbitration_prime"] is None or d["arbitration_prime"] < 2**16:
            problems.append("all_small_agree=True but no valid (>=2^16) arbitration_prime recorded")
        if d["arbitration_results"] is None:
            problems.append("all_small_agree=True but arbitration_results missing")
    else:
        if d["arbitration_prime"] is not None:
            problems.append("all_small_agree=False but an arbitration_prime was recorded (should be None)")

    # re-derive small_prime_agreement_per_k from results_by_prime directly
    rbp = d["results_by_prime"]
    p0, p1 = [str(p) for p in primes_small]
    for k in range(3, 9):
        ks = str(k)
        h0, h1 = rbp[p0][ks]["H_dim"], rbp[p1][ks]["H_dim"]
        s0, s1 = rbp[p0][ks]["S_dim"], rbp[p1][ks]["S_dim"]
        expected_agree = (h0 == h1 and s0 == s1)
        recorded_agree = d["small_prime_agreement_per_k"][ks]
        if expected_agree != recorded_agree:
            problems.append(f"k={k}: recomputed agreement={expected_agree} but cert says {recorded_agree}")

    # scoring block must match underlying prime-0 results and the FROZEN prediction doc values
    for k in ("7", "8"):
        sc = d["scoring"][k]
        h_meas = rbp[p0][k]["H_dim"]
        s_meas = rbp[p0][k]["S_dim"]
        if sc["H_measured"] != h_meas or sc["S_measured"] != s_meas:
            problems.append(f"k={k}: scoring block measured values don't match results_by_prime")
        if sc["H_predicted"] != EXPECTED_H[k] or sc["S_predicted"] != EXPECTED_S[k]:
            problems.append(f"k={k}: scoring predicted values don't match the frozen prediction doc "
                             f"(expected H={EXPECTED_H[k]} S={EXPECTED_S[k]})")
        if sc["H_match"] != (sc["H_measured"] == sc["H_predicted"]):
            problems.append(f"k={k}: H_match flag inconsistent with measured/predicted")
        if sc["S_match"] != (sc["S_measured"] == sc["S_predicted"]):
            problems.append(f"k={k}: S_match flag inconsistent with measured/predicted")
        # rank_confirmed must require BOTH all_small_agree AND arbitration match
        if d["all_small_agree"]:
            arb = d["S_ED_4_rank_confirmed"][k]
            expected_confirmed = arb["H_confirmed"] and arb["S_confirmed"]
            if sc["rank_confirmed"] != expected_confirmed:
                problems.append(f"k={k}: rank_confirmed={sc['rank_confirmed']} but S_ED_4 block implies {expected_confirmed}")
        else:
            if sc["rank_confirmed"] is not False:
                problems.append(f"k={k}: rank_confirmed should be False when small primes disagreed")

    # k=9+ not run (S-ED per instruction)
    if d.get("k9_plus_not_run") is not True:
        problems.append("k9_plus_not_run is not True")
    for p in primes_small + ([d["arbitration_prime"]] if d["arbitration_prime"] else []):
        pkey = str(p)
        source = rbp.get(pkey) or (d["arbitration_results"] if pkey == str(d["arbitration_prime"]) else None)
        if source and any(int(k) >= 9 for k in source if k.isdigit()):
            problems.append(f"prime {p}: results include k>=9, violating the k=9+ stop instruction")

    # prediction doc identity (informational -- not asserting a specific
    # historical commit hash match since we don't have git-blame tooling
    # here, just confirm the file exists and is referenced)
    try:
        _ = sha256_file(PREREG_PATH)
    except FileNotFoundError:
        problems.append(f"prediction doc not found at {PREREG_PATH}")

    result = {
        "schema": "edim-c78-checker/v1",
        "cert_checked": CERT_PATH,
        "problems": problems,
        "all_checks_pass": len(problems) == 0,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    with open("search/certs/edim_c78_checker_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
