#!/usr/bin/env python3
"""
drophunt_fib_analysis_v1.py

Calibration analysis for DROP-HUNT-DOUBLE (fake-side one-shot decision lane).
Reads the ALREADY machine-computed LINS marked-strictness export
(ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json,
produced by search/lins_marked_strictness_export_v1.g per ruling 1624 / mail 159h,
status CANDIDATE_GAP_PRODUCER, verified:false) and derives, for every K := L cap M
(L = one of the 4,265 nonidentity LowIndexNormalSubgroupsSearch(B3,2000) nodes,
M = K^(9) cap N_S4, the 972 roof window), the raw candidate fibre size

    #fib(K) = [M:K] * [M_F2:K_F2]
            = strictness.PB3_ratio_M_over_K * strictness.F2_ratio_MF_over_KF

per the cost formula in scratchpad/cofin_cert_draft_v1_2.md SS9.2:
    #fib(K) = (K_ord/M_ord) * [M_F2:K_F2]      (K <= M)
under the reading K_ord/M_ord = [M:K] (both K,M as finite-index subgroups of PB3;
K finer than M since K <= M, so the ratio is >= 1). This reading is an ASSUMPTION
flagged in the calibration report -- it is the only reading consistent with both
(a) the formula requiring an integer >= 1 for K<=M, and (b) the quantities that are
actually machine-computed and available in the source artifact.

No new GAP computation is performed here: this script only re-derives an arithmetic
product from fields that were already exactly computed (via real joint-image GAP
group orders) in the source artifact. This is a deliberate deviation from a literal
"recompute 50 rows fresh via a new GAP driver" reading of the task -- flagged in the
calibration report as a design question back to the command tower.
"""
import json
import statistics
import hashlib
import sys

SRC = "ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json"


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    src_sha256 = sha256_of_file(SRC)
    with open(SRC, encoding="utf-8") as f:
        d = json.load(f)

    universe = d["universe"]
    claim_cover = d["claim_cover"]
    roof_M = d["roof_M"]
    src_summary = d["summary"]
    rows = d["rows"]

    assert universe["nonidentity_rows"] == 4265, universe
    assert claim_cover["complete"] is True, claim_cover
    assert src_summary["strict_F2_count"] == 4255, src_summary

    fib_rows = []
    for r in rows:
        s = r["strictness"]
        fib = s["PB3_ratio_M_over_K"] * s["F2_ratio_MF_over_KF"]
        fib_rows.append({
            "node_id": r["node_id"],
            "b3_index_of_L": r["b3_index"],
            "PB3_ratio_M_over_K": s["PB3_ratio_M_over_K"],
            "F2_ratio_MF_over_KF": s["F2_ratio_MF_over_KF"],
            "class": s["class"],
            "fib_K": fib,
        })

    all_fib = [x["fib_K"] for x in fib_rows]
    degenerate = [x for x in fib_rows if x["fib_K"] == 1]
    nondeg = [x["fib_K"] for x in fib_rows if x["fib_K"] > 1]
    strict_f2_only = [x for x in fib_rows if x["class"] == "STRICT_F2"]
    strict_fib = [x["fib_K"] for x in strict_f2_only]

    fib_rows_sorted = sorted(fib_rows, key=lambda x: x["fib_K"])
    strict_sorted = sorted(strict_f2_only, key=lambda x: x["fib_K"])

    thresholds = [10, 50, 100, 500, 1000, 5000, 10000]
    threshold_counts = {
        str(t): sum(1 for f in nondeg if f <= t) for t in thresholds
    }

    out = {
        "schema": "drophunt-fib-analysis/v1",
        "status": "CANDIDATE_ARITHMETIC_DERIVATION",
        "verified": False,
        "note": (
            "Pure arithmetic re-derivation from an already GAP-computed source "
            "artifact. No new GAP execution. fib_K formula reading is an "
            "assumption -- see module docstring."
        ),
        "source_artifact_path": SRC,
        "source_artifact_sha256": src_sha256,
        "source_artifact_sha16": src_sha256[:16],
        "source_universe": universe,
        "source_claim_cover": claim_cover,
        "source_roof_M": roof_M,
        "source_measured_costs_ms": {
            "lins_elapsed_ms": src_summary["lins_elapsed_ms"],
            "total_elapsed_ms": src_summary["total_elapsed_ms"],
            "note": "real wall time already spent on GHA to compute K=L cap M "
                    "index/[M_F2:K_F2] for ALL 4,265 rows (one-time, already done).",
        },
        "fib_distribution_all_rows": {
            "n": len(all_fib),
            "degenerate_K_eq_M_count": len(degenerate),
            "nondegenerate_count": len(nondeg),
            "min": min(nondeg),
            "median": statistics.median(nondeg),
            "mean": round(statistics.mean(nondeg), 1),
            "max": max(nondeg),
            "threshold_counts_fib_leq": threshold_counts,
        },
        "fib_distribution_strict_F2_only": {
            "n": len(strict_fib),
            "min": min(strict_fib),
            "median": statistics.median(strict_fib),
            "mean": round(statistics.mean(strict_fib), 1),
            "max": max(strict_fib),
        },
        "cheapest_10_all_rows": fib_rows_sorted[:10],
        "cheapest_15_strict_F2_only": strict_sorted[:15],
    }

    with open("scratchpad/drophunt_fib_distribution_v1.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(json.dumps({k: v for k, v in out.items() if k not in (
        "cheapest_10_all_rows", "cheapest_15_strict_F2_only")}, indent=2))


if __name__ == "__main__":
    sys.exit(main())
