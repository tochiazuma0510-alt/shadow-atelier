#!/usr/bin/env python3
"""
search/fib_mult_2000_v1.py -- FIB-MULT-2000 (裁定823, follow-on to LINS-2000).
Extends search/fib_mult_v1.py's aggregation method (裁定803, hunting_chapter_v1_addendum_a.md
§4.2) from the index<=1000 census (search/certs/lins_twin_census_v1_20260806.json, 174 pairs)
to the index<=2000 census (search/certs/lins_census_2000_v1_20260811.json, 476 pairs, GHA run
31498009539). SAME method, NO new GAP run: nodes=distinct N (fingerprint=(index, sorted
canonical_id_words)), edges=twin_pairs entries, multiplicity=connected-component size.

Canary: the known 750-clique (id_group=[750,6]) must still reduce to exactly ONE component of
size 5 (multiplicity_nodes=5, pair_count_edges=10) -- reproduced from the LARGER 2000-index
inventory as a regression check against the already-established 1000-index result
(search/certs/fib_mult_v1_20260811.json). Also re-derives the Q8-FAM 8-pair-multiplicity-2
canary from addendum_a §1.2.

No verdict language. Raw multiplicity counts and booleans only.
"""
import json
import hashlib


CENSUS_PATH = "search/certs/lins_census_2000_v1_20260811.json"
PRIOR_1000_CERT = "search/certs/fib_mult_v1_20260811.json"


def node_key(index, member):
    return (index, tuple(sorted(member["canonical_id_words"])))


def group_key(member):
    """id_group when available; falls back to structure_description for the 16 members whose
    quotient order falls outside GAP's IdGroup coverage (e.g. order 1536, excluded per
    search/lins-census-2000-v1.g's IdGroupSafe) -- the SOURCE script's own twin-pairing already
    used this exact fallback (structDesc + IsomorphismGroups) for such members, per
    search/lins-census-2000-v1.g's QuotientsIso function, so re-using structure_description here
    for aggregation is consistent with how the twin_pairs were ACTUALLY formed, not a new
    assumption. Disclosed: structure_description is a WEAKER identity check than id_group in
    principle (two non-isomorphic groups could share a GAP StructureDescription string in rare
    cases) -- not observed as an issue here (only 16 affected members, all order 1536, a single
    dense band), but flagged as a fallback, not silently treated as equally strong."""
    if member["id_group"] is not None:
        return ("ID", tuple(member["id_group"]))
    return ("STRUCTDESC", member["structure_description"])


def main():
    census = json.load(open(CENSUS_PATH, encoding="utf-8"))
    census_sha256 = hashlib.sha256(open(CENSUS_PATH, "rb").read()).hexdigest()
    prior = json.load(open(PRIOR_1000_CERT, encoding="utf-8"))

    twin_pairs = census["twin_pairs"]

    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    node_id_group = {}
    edge_count_per_pair_index_idgroup = {}

    for tp in twin_pairs:
        idx = tp["index"]
        m0, m1 = tp["members"]
        idg0 = group_key(m0)
        idg1 = group_key(m1)
        if idg0 != idg1:
            raise ValueError(f"twin pair at index={idx} has mismatched group_key between members: {idg0} vs {idg1}")
        k0 = node_key(idx, m0)
        k1 = node_key(idx, m1)
        for k, idg in ((k0, idg0), (k1, idg1)):
            if k not in parent:
                parent[k] = k
                node_id_group[k] = (idx, idg)
            else:
                if node_id_group[k] != (idx, idg):
                    raise ValueError(f"node {k} seen with inconsistent (index,id_group): "
                                      f"{node_id_group[k]} vs {(idx, idg)}")
        union(k0, k1)
        key2 = (idx, idg0)
        edge_count_per_pair_index_idgroup[key2] = edge_count_per_pair_index_idgroup.get(key2, 0) + 1

    components = {}
    for k in parent:
        r = find(k)
        components.setdefault(r, []).append(k)

    mult_by_index_idgroup = {}
    for r, mem in components.items():
        idx, idg = node_id_group[mem[0]]
        for m in mem:
            assert node_id_group[m] == (idx, idg), "component has inconsistent (index,id_group)"
        key = (idx, idg)
        mult_by_index_idgroup.setdefault(key, []).append(len(mem))

    all_components_raw = []
    for (idx, idg), sizes in mult_by_index_idgroup.items():
        tag, val = idg
        if tag == "ID":
            entry_idg, entry_struct = list(val), None
        else:
            entry_idg, entry_struct = None, val
        for sz in sizes:
            all_components_raw.append({"index": idx, "id_group": entry_idg,
                                        "structure_description_fallback": entry_struct,
                                        "multiplicity_nodes": sz, "_key": idg})
    all_components_raw.sort(key=lambda r: (-r["multiplicity_nodes"], r["index"]))

    mult_ge_3 = [r for r in all_components_raw if r["multiplicity_nodes"] >= 3]
    for r in all_components_raw:
        key2 = (r["index"], r["_key"])
        r["pair_count_edges"] = edge_count_per_pair_index_idgroup.get(key2, None)
    for r in all_components_raw:
        del r["_key"]

    canary_750 = [r for r in all_components_raw if r["id_group"] == [750, 6]]
    canary_750_ok = (len(canary_750) == 1 and canary_750[0]["multiplicity_nodes"] == 5
                      and canary_750[0]["pair_count_edges"] == 10)

    q8fam_id_groups = [[24, 3], [72, 3], [120, 15], [168, 22], [216, 3], [264, 12], [312, 25], [360, 14]]
    canary_q8fam = []
    for idg in q8fam_id_groups:
        matches = [r for r in all_components_raw if r["id_group"] == idg]
        canary_q8fam.append({"id_group": idg, "matches": matches})
    canary_q8fam_all_mult_2 = all(
        len(c["matches"]) == 1 and c["matches"][0]["multiplicity_nodes"] == 2
        for c in canary_q8fam
    )

    # regression check against the prior 1000-index result: every multiplicity>=3 component
    # already found at index<=1000 must STILL appear here (superset regression)
    prior_mult_ge_3 = prior["multiplicity_ge_3"]
    regression_ok = all(
        any(r["index"] == pr["index"] and r["id_group"] == pr["id_group"]
            and r["multiplicity_nodes"] == pr["multiplicity_nodes"] for r in mult_ge_3)
        for pr in prior_mult_ge_3
    )

    total_nodes = len(parent)
    total_components = len(components)

    out = {
        "schema": "shadow-atelier/fib_mult_2000_v1",
        "authority": "裁定823 (LINS-2000 follow-on aggregation), extends 裁定803/"
                     "hunting_chapter_v1_addendum_a.md §4.2 FIB-MULT to index<=2000",
        "method_note": "IDENTICAL method to search/fib_mult_v1.py, applied to the LARGER "
                       "index<=2000 census (search/certs/lins_census_2000_v1_20260811.json, "
                       "476 twin pairs, GHA run 31498009539). NO new GAP run in this script.",
        "source_cert": CENSUS_PATH,
        "source_cert_sha256": census_sha256,
        "prior_1000_cert_sha256_note": "regression-checked against search/certs/fib_mult_v1_20260811.json (index<=1000 result)",
        "scope_note": "index<=2000 (the source cert's own scope). Multiplicity-1 N's invisible "
                      "by construction (same as the 1000-index version) -- irrelevant for the "
                      "multiplicity>=3 ask.",
        "total_distinct_N_nodes_with_a_twin": total_nodes,
        "total_connected_components": total_components,
        "all_components": all_components_raw,
        "multiplicity_ge_3": mult_ge_3,
        "multiplicity_ge_3_count": len(mult_ge_3),
        "regression_vs_1000_index_ok": regression_ok,
        "canary_750_clique": {
            "note": "expected: exactly 1 component, multiplicity_nodes=5, pair_count_edges=10 "
                    "(reproduced from the LARGER 2000-index inventory).",
            "found": canary_750,
            "pass": canary_750_ok,
        },
        "canary_q8fam_all_multiplicity_2": {
            "detail": canary_q8fam,
            "pass": canary_q8fam_all_mult_2,
        },
        "no_verdict_note": "raw multiplicity counts, component lists, and booleans only.",
    }
    out_path = "search/certs/fib_mult_2000_v1_20260812.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"total_nodes={total_nodes} total_components={total_components}")
    print(f"multiplicity_ge_3_count={len(mult_ge_3)}")
    for r in mult_ge_3:
        print(f"  index={r['index']} id_group={r['id_group']} multiplicity_nodes={r['multiplicity_nodes']} pair_count_edges={r['pair_count_edges']}")
    print(f"canary_750_clique.pass={canary_750_ok}")
    print(f"canary_q8fam_all_multiplicity_2.pass={canary_q8fam_all_mult_2}")
    print(f"regression_vs_1000_index_ok={regression_ok}")


if __name__ == "__main__":
    main()
