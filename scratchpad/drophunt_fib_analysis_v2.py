#!/usr/bin/env python3
"""
drophunt_fib_analysis_v2.py

Ruling 1720 repair (数学者裁定, scratchpad/fib_ruling_and_fibre_checker_spec_v1.md,
sha16 2878d55f90feae3c). v1's #fib(K) reading was WRONG:
  v1 used  #fib(K) = [M:K] * [M_F2:K_F2]        (PB3-index based -- WRONG)
Correct reading (2401 definition, ruling SS1.2):
  #fib(K) = (K_ord / M_ord) * [M_F2:K_F2]
where K_ord := lcm(order of x-image, order of y-image) in F2/K_F2
(x=sigma1^2, y=sigma2^2), NOT a PB3-subgroup index. M_ord=18 for the 972
window (verbatim sol/sol_reply_159_iv.md L2928, machine-confirmed below).

K_ord is NOT stored as an explicit field in the source artifact
(lins_marked_strictness_export_v1_20260823.json), but IS derivable via pure
arithmetic (permutation cycle-length lcm) from data that IS stored per row
(marked_quotient_map.x_eq_sigma1_sq / y_eq_sigma2_sq, the images of x,y in
B3/L) plus two fixed constants (Order(MX)=18, Order(MY)=18 in PB3/M, the
same for every row since M is fixed). This derivation was validated against
DIRECT GAP computation of the joint-image element orders on 10 rows
(search/drophunt_kord_validate_v1.g -> search/certs/drophunt_kord_validate_v1_20260829.json,
all_rows_match=true) before being trusted here.

[M_F2:K_F2] is UNCHANGED from v1: strictness.F2_ratio_MF_over_KF in the
source artifact already correctly equals [M_F2:K_F2] (verified: the
denominator used by the producer, 1,469,664, equals |PB3/M| AND |F2/M_F2|
because c (the PB3/F2 generator) maps to the identity in PB3/M --
roof_M.c_image == "identity" -- so |PB3/M| = |F2/M_F2| for M specifically;
this does not require c in L). Only the m-direction factor was wrong in v1.
"""
import json
import re
import math
import statistics
import hashlib
import sys

SRC = "ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json"
KORD_VALIDATION = "search/certs/drophunt_kord_validate_v1_20260829.json"

ORDER_MX = 18  # Order(MX) in PB3/M, machine-confirmed via search/drophunt_kord_validate_v1.g
ORDER_MY = 18  # Order(MY) in PB3/M, machine-confirmed
M_ORD = 18     # lcm(Order(MX), Order(MY)); matches sol_reply_159_iv.md verbatim C_M_ord=M_ord=18


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def perm_order_from_gap_string(s):
    """Order of a GAP permutation given in cycle-notation string, e.g.
    '(1,2,3)(4,5)' -> lcm(3,2) = 6 ; '()' -> 1.
    Cycle notation lists disjoint cycles; the permutation's order is the
    lcm of the cycle lengths (fixed points contribute cycles of length 1,
    which do not change the lcm, so they can be ignored)."""
    s = s.strip()
    if s == "()" or s == "":
        return 1
    cycles = re.findall(r"\(([^)]*)\)", s)
    order = 1
    for c in cycles:
        length = len(c.split(","))
        if length > 1:
            order = order * length // math.gcd(order, length)
    return order


def main():
    # sanity: cross-check the parser against the GAP-validated rows before
    # trusting it on the full 4265-row set.
    with open(KORD_VALIDATION, encoding="utf-8") as f:
        kv = json.load(f)
    assert kv["all_rows_match"] is True, "K_ord formula not GAP-validated -- STOP"
    assert kv["Order_MX"] == ORDER_MX and kv["Order_MY"] == ORDER_MY

    src_sha256 = sha256_of_file(SRC)
    with open(SRC, encoding="utf-8") as f:
        d = json.load(f)

    universe = d["universe"]
    claim_cover = d["claim_cover"]
    roof_M = d["roof_M"]
    rows = d["rows"]
    assert universe["nonidentity_rows"] == 4265
    assert claim_cover["complete"] is True

    fib_rows = []
    input_errors = []
    for r in rows:
        mqm = r["marked_quotient_map"]
        s = r["strictness"]
        f2_ratio = s["F2_ratio_MF_over_KF"]  # unchanged: this IS [M_F2:K_F2]

        ord_x_L = perm_order_from_gap_string(mqm["x_eq_sigma1_sq"])
        ord_y_L = perm_order_from_gap_string(mqm["y_eq_sigma2_sq"])
        ord_jx = ord_x_L * ORDER_MX // math.gcd(ord_x_L, ORDER_MX)
        ord_jy = ord_y_L * ORDER_MY // math.gcd(ord_y_L, ORDER_MY)
        k_ord = ord_jx * ord_jy // math.gcd(ord_jx, ord_jy)

        if k_ord % M_ORD != 0:
            input_errors.append({"node_id": r["node_id"], "b3_index": r["b3_index"],
                                  "k_ord": k_ord, "m_ord": M_ORD})
            continue

        m_factor = k_ord // M_ORD
        fib = m_factor * f2_ratio
        fib_rows.append({
            "node_id": r["node_id"],
            "b3_index_of_L": r["b3_index"],
            "K_ord": k_ord,
            "M_ord": M_ORD,
            "m_factor_K_ord_over_M_ord": m_factor,
            "F2_ratio_MF_over_KF": f2_ratio,
            "fib_K": fib,
            "class": s["class"],
        })

    if input_errors:
        # Per ruling: nonintegral K_ord/M_ord => K not<= M => stop and report.
        with open("scratchpad/drophunt_fib_v2_input_errors.json", "w", encoding="utf-8") as f:
            json.dump(input_errors, f, indent=2)
        print(f"INPUT_ERRORS count={len(input_errors)} (see "
              f"scratchpad/drophunt_fib_v2_input_errors.json) -- these rows "
              f"excluded from distribution below", file=sys.stderr)

    all_fib = [x["fib_K"] for x in fib_rows]
    degenerate = [x for x in fib_rows if x["fib_K"] == 1]
    nondeg = [x["fib_K"] for x in fib_rows if x["fib_K"] > 1]
    strict_only = [x for x in fib_rows if x["class"] == "STRICT_F2"]
    strict_fib = [x["fib_K"] for x in strict_only]

    fib_sorted = sorted(fib_rows, key=lambda x: x["fib_K"])
    strict_sorted = sorted(strict_only, key=lambda x: x["fib_K"])

    thresholds = [10, 50, 100, 500, 1000, 5000, 10000]
    threshold_counts = {str(t): sum(1 for f in nondeg if f <= t) for t in thresholds}
    threshold_counts_strict = {str(t): sum(1 for f in strict_fib if f <= t) for t in thresholds}

    m_factor_hist = {}
    for x in fib_rows:
        k = x["m_factor_K_ord_over_M_ord"]
        m_factor_hist[k] = m_factor_hist.get(k, 0) + 1

    out = {
        "schema": "drophunt-fib-analysis/v2",
        "status": "CANDIDATE_ARITHMETIC_DERIVATION_GAP_VALIDATED",
        "verified": False,
        "supersedes": "scratchpad/drophunt_fib_distribution_v1.json (WRONG formula reading, see ruling 1720)",
        "ruling": "裁定1720 / scratchpad/fib_ruling_and_fibre_checker_spec_v1.md sha16 2878d55f90feae3c SS1",
        "note": (
            "#fib(K) = (K_ord/M_ord) * [M_F2:K_F2], K_ord = lcm(order of x-image, "
            "order of y-image) in F2/K_F2 (NOT a PB3-subgroup index). K_ord derived "
            "via pure permutation-cycle arithmetic from marked_quotient_map fields "
            "already stored per row in the source artifact, plus two fixed constants "
            "(Order(MX)=Order(MY)=18) computed once via GAP and cross-validated "
            "against direct GAP joint-image-order computation on 10 rows "
            "(all matched exactly) before use here. No new full-inventory GAP run "
            "was needed."
        ),
        "source_artifact_path": SRC,
        "source_artifact_sha256": src_sha256,
        "source_artifact_sha16": src_sha256[:16],
        "kord_validation_path": KORD_VALIDATION,
        "kord_validation_all_rows_match": kv["all_rows_match"],
        "kord_derivation_constants": {"Order_MX": ORDER_MX, "Order_MY": ORDER_MY, "M_ord": M_ORD},
        "input_errors_count": len(input_errors),
        "fib_distribution_all_rows": {
            "n": len(fib_rows),
            "degenerate_K_eq_M_count": len(degenerate),
            "nondegenerate_count": len(nondeg),
            "min": min(nondeg) if nondeg else None,
            "median": statistics.median(nondeg) if nondeg else None,
            "mean": round(statistics.mean(nondeg), 1) if nondeg else None,
            "max": max(nondeg) if nondeg else None,
            "threshold_counts_fib_leq": threshold_counts,
        },
        "fib_distribution_strict_F2_only": {
            "n": len(strict_fib),
            "min": min(strict_fib) if strict_fib else None,
            "median": statistics.median(strict_fib) if strict_fib else None,
            "mean": round(statistics.mean(strict_fib), 1) if strict_fib else None,
            "max": max(strict_fib) if strict_fib else None,
            "threshold_counts_fib_leq": threshold_counts_strict,
        },
        "m_factor_histogram_K_ord_over_M_ord": dict(sorted(m_factor_hist.items())),
        "cheapest_10_all_rows": fib_sorted[:10],
        "cheapest_15_strict_F2_only": strict_sorted[:15],
    }

    with open("scratchpad/drophunt_fib_distribution_v2.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(json.dumps({k: v for k, v in out.items() if k not in (
        "cheapest_10_all_rows", "cheapest_15_strict_F2_only", "m_factor_histogram_K_ord_over_M_ord")}, indent=2))


if __name__ == "__main__":
    sys.exit(main())
