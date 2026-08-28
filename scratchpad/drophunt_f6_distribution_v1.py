#!/usr/bin/env python3
"""
drophunt_f6_distribution_v1.py -- F6 (c in K) distribution across the 358
fib<=100 windows (and, for reference, all 4265 LINS rows), computed PURELY
FROM the already-existing full LINS marked-strictness export artifact
(ci/lins_marked_artifacts_32626064970/lins_marked_export/
lins_marked_strictness_export_v1_20260823.json), which stores sigma1,sigma2
(NOT just x,y) per row as GAP permutation-cycle strings. No new GAP run is
needed: F6 := c in K = M cap L  <=>  c in L (since c is ALWAYS in M by
construction of the K^(9)-type roof, a documented structural fact, not
window-specific data), and c's image in B3/L is computable directly as
Cp := (S1 * S2 * S1)^2 from the stored sigma1/sigma2 permutations, checked
for identity.

F7 (tau descends) is set conservatively equal to F6 per spec v2 SS10 point 4
("GAP-3's <= direction is unproven; treat non-descent as dangerous"):
F6=true is trusted safe (F7:=true), F6=false is treated as unsafe/blocked
(F7:=false), matching exactly how search/drophunt_checker_producer_v2.g
already gates the predicate.
"""
import json
import re
import math
import hashlib
import sys

SRC = "ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json"

ORDER_MX = 18
ORDER_MY = 18
M_ORD = 18


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def parse_perm(cycle_str, degree):
    """GAP permutation cycle notation -> 0-indexed image tuple of length degree."""
    img = list(range(degree))
    s = cycle_str.strip()
    if s in ("()", ""):
        return tuple(img)
    for cyc in re.findall(r"\(([^)]*)\)", s):
        pts = [int(x) - 1 for x in cyc.split(",")]
        n = len(pts)
        if n < 2:
            continue
        for i in range(n):
            img[pts[i]] = pts[(i + 1) % n]
    return tuple(img)


def pmul(a, b):
    return tuple(b[a[i]] for i in range(len(a)))


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
    src_sha256 = sha256_of_file(SRC)
    with open(SRC, encoding="utf-8") as f:
        d = json.load(f)
    rows = d["rows"]
    assert len(rows) == 4265

    results = []
    for r in rows:
        mqm = r["marked_quotient_map"]
        s = r["strictness"]
        deg = mqm["permutation_degree"]
        S1 = parse_perm(mqm["sigma1"], deg)
        S2 = parse_perm(mqm["sigma2"], deg)
        Delta = pmul(pmul(S1, S2), S1)   # s1 s2 s1  (word order; see note below)
        Cp = pmul(Delta, Delta)          # (s1 s2 s1)^2
        identity = tuple(range(deg))
        c_in_L = (Cp == identity)

        # also cross-check against the row's own stored c_eq_delta_sq field
        # (independently computed by the census producer via the SAME
        # formula) as an internal consistency check on our own parse.
        stored_c = mqm.get("c_eq_delta_sq")
        stored_c_is_identity = (stored_c is not None and stored_c.strip() == "()")

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

        results.append({
            "node_id": r["node_id"],
            "b3_index": r["b3_index"],
            "K_ord": k_ord,
            "F2_ratio": f2,
            "fib_K": fib,
            "c_in_K_F6": c_in_L,
            "c_in_K_F6_cross_check_matches_stored": (c_in_L == stored_c_is_identity),
            "F7_tau_descends_conservative": c_in_L,
        })

    mismatches = [x for x in results if not x["c_in_K_F6_cross_check_matches_stored"]]
    if mismatches:
        print(f"WARNING: {len(mismatches)} rows where independently-computed c_in_K "
              f"disagrees with the row's own stored c_eq_delta_sq field", file=sys.stderr)

    all_rows = results
    fib100 = [x for x in results if 1 < x["fib_K"] <= 100]

    def summarize(subset, label):
        f6_true = [x for x in subset if x["c_in_K_F6"]]
        f6_false = [x for x in subset if not x["c_in_K_F6"]]
        return {
            "label": label,
            "total": len(subset),
            "F6_true_count": len(f6_true),
            "F6_false_count": len(f6_false),
        }

    summary_all = summarize(all_rows, "all_4265_nondegenerate")
    summary_358 = summarize(fib100, "fib_leq_100_358_set")

    f6_true_358_list = [x for x in fib100 if x["c_in_K_F6"]]
    f6_false_358_list = [x for x in fib100 if not x["c_in_K_F6"]]

    out = {
        "schema": "drophunt-f6-distribution/v1",
        "status": "CANDIDATE_ARITHMETIC_DERIVATION",
        "verified": False,
        "method": "pure Python, parsed from stored sigma1/sigma2 permutation-cycle strings in the already-existing full LINS marked-strictness export artifact -- NO new GAP execution (no LowIndexNormalSubgroupsSearch re-run needed).",
        "source_artifact_path": SRC,
        "source_artifact_sha256": src_sha256,
        "cross_check_against_stored_c_eq_delta_sq": {
            "total_rows_checked": len(results),
            "mismatches": len(mismatches),
            "note": "Each row's stored c_eq_delta_sq field (independently computed by the original census producer via the same (s1 s2 s1)^2 formula) is compared against this script's own from-scratch parse+multiply of sigma1/sigma2. 0 mismatches confirms the parser/multiplication convention is correct.",
        },
        "summary_all_4265": summary_all,
        "summary_fib_leq_100_358_set": summary_358,
        "F6_true_358_subset_node_ids": [x["node_id"] for x in f6_true_358_list],
        "F6_true_358_subset_detail": f6_true_358_list,
        "F6_false_358_subset_node_ids": [x["node_id"] for x in f6_false_358_list],
        "F6_false_358_subset_detail_count_only": len(f6_false_358_list),
    }

    with open("scratchpad/drophunt_f6_distribution_v1.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(json.dumps({k: v for k, v in out.items() if k not in (
        "F6_true_358_subset_node_ids", "F6_true_358_subset_detail",
        "F6_false_358_subset_node_ids")}, indent=2))


if __name__ == "__main__":
    sys.exit(main())
