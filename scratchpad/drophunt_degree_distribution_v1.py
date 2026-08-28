#!/usr/bin/env python3
"""
drophunt_degree_distribution_v1.py -- item 6 (裁定1763): degree guard
(degree <= 2000 assert, with K2 noted as out-of-checker-scope at
degree=23,340) + degree distribution over the 358-window fib<=100 set
(scratchpad/drophunt_fib_distribution_v1.json's window list), counting how
many windows would be excluded by the guard.

Degree of a window K:=M cap L = M's own degree (36) + L's own permutation
degree (b3_index, since LINS quotients B3/L act faithfully on b3_index
points in this census's construction, confirmed throughout this whole
repair line). No new GAP computation needed: b3_index is already recorded
per row in the existing LINS marked-strictness export artifact.
"""
import json
import sys

DEGREE_GUARD_MAX = 2000
M_DEGREE = 36

SRC_FIB358_LIST = "scratchpad/drophunt_fib_distribution_v1.json"
SRC_LINS_ARTIFACT = "ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json"


def main():
    # scratchpad/drophunt_fib_distribution_v1.json is the v1 (superseded-by-
    # v2-formula but still valid for node_id/b3_index bookkeeping) 358-window
    # list; we re-derive the CURRENT (v2-formula, fib<=100) 358-window set
    # directly from the LINS artifact to avoid depending on the superseded
    # v1 numeric values, using the SAME method as scratchpad/
    # drophunt_f6_distribution_v1.py (already cross-checked 0 mismatches
    # against stored c_eq_delta_sq).
    import re
    import math

    def perm_order_from_string(s):
        s = s.strip()
        if s in ("()", ""):
            return 1
        o = 1
        for c in re.findall(r"\(([^)]*)\)", s):
            n = len(c.split(","))
            if n > 1:
                o = o * n // math.gcd(o, n)
        return o

    with open(SRC_LINS_ARTIFACT, encoding="utf-8") as f:
        art = json.load(f)
    rows = art["rows"]
    assert len(rows) == 4265

    ORDER_MX = 18
    ORDER_MY = 18
    M_ORD = 18

    fib358 = []
    for r in rows:
        mqm = r["marked_quotient_map"]
        s = r["strictness"]
        ox = perm_order_from_string(mqm["x_eq_sigma1_sq"])
        oy = perm_order_from_string(mqm["y_eq_sigma2_sq"])
        jx = ox * ORDER_MX // math.gcd(ox, ORDER_MX)
        jy = oy * ORDER_MY // math.gcd(oy, ORDER_MY)
        k_ord = jx * jy // math.gcd(jx, jy)
        f2 = s["F2_ratio_MF_over_KF"]
        if k_ord % M_ORD != 0:
            continue
        f1 = k_ord // M_ORD
        fib = f1 * f2
        if 1 < fib <= 100:
            fib358.append({
                "node_id": r["node_id"],
                "b3_index": r["b3_index"],
                "K_ord": k_ord,
                "F2_ratio": f2,
                "fib_K": fib,
                "degree": M_DEGREE + r["b3_index"],
            })

    assert len(fib358) == 358, f"expected 358 windows, got {len(fib358)}"

    within_guard = [w for w in fib358 if w["degree"] <= DEGREE_GUARD_MAX]
    excluded = [w for w in fib358 if w["degree"] > DEGREE_GUARD_MAX]

    degrees = sorted(w["degree"] for w in fib358)
    n = len(degrees)

    def pct(p):
        idx = min(n - 1, int(p * n))
        return degrees[idx]

    out = {
        "schema": "drophunt-degree-distribution/v1",
        "status": "CANDIDATE_ARITHMETIC_DERIVATION",
        "verified": False,
        "degree_guard_max": DEGREE_GUARD_MAX,
        "K2_out_of_checker_scope_note": (
            "K2's own degree is 23,340 (23,328-point G36 right-regular representation "
            "+ 9-point PSL(2,8) block + 3-point L3 block), far exceeding this degree "
            "guard. K2 is NOT part of the 358-window fib<=100 sweep set (it is a "
            "separate, hand-built calibration window via K1=K^(36) cap N_S4, not a "
            "single LINS row against roof M) and its Python-checker round-trip is "
            "already known to be performance-limited at this scale (search/certs/"
            "drophunt_checker_v6_final_20260829.json). The degree guard formalizes "
            "this: any window with degree>2000 is out of the Python checker's "
            "practical scope and must be flagged, not silently attempted."
        ),
        "fib_leq_100_358_set": {
            "total": len(fib358),
            "within_guard_degree_leq_2000": len(within_guard),
            "excluded_degree_gt_2000": len(excluded),
            "excluded_windows": [{"node_id": w["node_id"], "b3_index": w["b3_index"], "degree": w["degree"], "fib_K": w["fib_K"]} for w in excluded],
        },
        "degree_distribution_all_358": {
            "min": degrees[0],
            "median": pct(0.5),
            "p90": pct(0.9),
            "p99": pct(0.99),
            "max": degrees[-1],
            "mean": round(sum(degrees) / n, 1),
        },
    }

    with open("scratchpad/drophunt_degree_distribution_v1.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    sys.exit(main())
