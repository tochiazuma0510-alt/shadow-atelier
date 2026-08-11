#!/usr/bin/env python3
"""
search/jac_construct_modq_regression_test.py -- regression anchor (裁定843 requirement ①).

Before the new mod-q construction pipeline (search/jac_construct_modq_v1.py,
search/jac_chk2_modq_v1.py v2) is trusted for p=17,19,23, it MUST reproduce the ALREADY-KNOWN
exact values for p=5,7,11 (and, as an extra check beyond the explicit requirement, p=13) from
search/certs/jac_chk_v1_20260811.json (the original exact-Fraction computation, committed and
cross-checked earlier this session): dim R_p and the S3-isotypic type (m_triv, m_sgn, m_std).

This script is the regression check itself (not a crosscheck in the search/crosscheck sense --
it compares the NEW mod-q construction against the OLD exact-Fraction construction's OWN
already-committed cert, both being search-side artifacts; this is a self-consistency/regression
gate, not an independent-implementation crosscheck).

Raw pass/fail per anchor point, no verdict language beyond the boolean match itself.
"""
import json
import sys

sys.path.insert(0, "search")
from jac_chk2_modq_v1 import measure_both_q

EXACT_CERT_PATH = "search/certs/jac_chk_v1_20260811.json"
ANCHOR_PRIMES = [5, 7, 11, 13]


def main():
    exact = json.load(open(EXACT_CERT_PATH, encoding="utf-8"))

    results = []
    all_pass = True
    for p in ANCHOR_PRIMES:
        exact_r = exact["per_p"][str(p)]
        exact_dim = exact_r["rank_span_s_i"]
        exact_iso = exact_r["isotypic"]

        modq_r = measure_both_q(p)
        modq_dim = modq_r["dim_R_p"]
        modq_iso = modq_r.get("isotypic")

        dim_match = (modq_dim == exact_dim)
        iso_match = (modq_iso == exact_iso)
        point_pass = dim_match and iso_match
        if not point_pass:
            all_pass = False

        results.append({
            "p": p,
            "exact_dim": exact_dim, "modq_dim": modq_dim, "dim_match": dim_match,
            "exact_isotypic": exact_iso, "modq_isotypic": modq_iso, "isotypic_match": iso_match,
            "point_pass": point_pass,
            "timing_sec": modq_r["timing_sec"],
        })
        print(f"p={p}: exact_dim={exact_dim} modq_dim={modq_dim} match={dim_match} | "
              f"exact_iso={exact_iso} modq_iso={modq_iso} match={iso_match} | "
              f"PASS={point_pass} | timing={modq_r['timing_sec']}", flush=True)

    out = {
        "schema": "shadow-atelier/jac_construct_modq_regression_test_v1",
        "authority": "裁定843 requirement ① -- regression anchor for the mod-q construction rewrite",
        "source_exact_cert": EXACT_CERT_PATH,
        "anchor_primes": ANCHOR_PRIMES,
        "results": results,
        "all_anchors_pass": all_pass,
        "no_verdict_note": "raw dim/isotypic comparison and booleans only.",
    }
    out_path = "search/certs/jac_construct_modq_regression_test_v1_20260812.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"all_anchors_pass={all_pass}")


if __name__ == "__main__":
    main()
