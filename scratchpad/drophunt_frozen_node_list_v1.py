#!/usr/bin/env python3
"""
drophunt_frozen_node_list_v1.py -- item 7 (裁定1763): generate the FROZEN
358-window node_id list (fib<=100 set, current v2-formula derivation) for
runtime cross-check by the sweep driver (mismatch = stop). Re-derives the
list directly and deterministically from the LINS marked-strictness export
artifact (same method as scratchpad/drophunt_degree_distribution_v1.py /
drophunt_f6_distribution_v1.py, both already cross-checked 0 mismatches
against the artifact's own stored c_eq_delta_sq field).
"""
import hashlib
import json
import math
import re
import sys

SRC_LINS_ARTIFACT = "ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json"


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


def main():
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
                "degree": 36 + r["b3_index"],
            })

    assert len(fib358) == 358

    fib358_sorted = sorted(fib358, key=lambda w: (w["fib_K"], w["b3_index"], w["node_id"]))

    node_id_list = [w["node_id"] for w in fib358_sorted]
    list_digest = hashlib.sha256(json.dumps(node_id_list, sort_keys=False, separators=(",", ":")).encode("ascii")).hexdigest()

    out = {
        "schema": "drophunt-frozen-node-list/v1",
        "status": "FROZEN",
        "verified": False,
        "source_artifact_path": SRC_LINS_ARTIFACT,
        "count": len(fib358_sorted),
        "order": "sorted by (fib_K asc, b3_index asc, node_id asc) -- cheap-first, deterministic tie-break",
        "list_sha256": list_digest,
        "windows": fib358_sorted,
    }
    with open("search/certs/drophunt_frozen_node_list_v1_20260829.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != "windows"}, indent=2))


if __name__ == "__main__":
    sys.exit(main())
