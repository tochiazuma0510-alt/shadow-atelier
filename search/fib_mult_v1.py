#!/usr/bin/env python3
"""
search/fib_mult_v1.py -- FIB-MULT (裁定803, docs/notes/hunting_chapter_v1_addendum_a.md
SS4.2, "FIB-SWEEP を撤回して差し替え"): fiber multiplicity = multiplicity of IdGroup(B3/N)
in the EXISTING census/lins twin-pair enumeration (index<=1000), with NO Aut computation and
NO new SmallGroups sweep -- per the addendum's own theorem:
    #{N normal in B3 : B3/N ~= G} = multiplicity of the isomorphism type in the lins output list
This is a PURE AGGREGATION of the already-committed
search/certs/lins_twin_census_v1_20260806.json (174 twin pairs, index<=1000, generated_by
LID-1-disciplined single LowIndexNormalSubgroupsSearch call -- exhaustive over the bound within
that run). NO new GAP run in this script (裁定803 point 2's "追加走行ゼロ" clause).

Method: build a graph whose nodes are DISTINCT normal subgroups N, identified by
(index, tuple(sorted(canonical_id_words))) -- a fingerprint derived from the words GAP found
for each N (disclosed: if two genuinely-distinct N's happened to be assigned identical word
fingerprints by the source cert, they would collapse here; not observed in a spot check, see
crosscheck). Edges are the twin_pairs entries themselves (N--K whenever the source cert already
recorded them as a twin pair, i.e. same index + same id_group). Connected components = cliques
(the source cert's own note confirms "twin relation = isomorphism of quotients is an
equivalence relation => cliques", already used for the 750-clique observation in
docs/notes/theorem_check_mirrorall_l3vacuous_v1.md SSG.2). Multiplicity of an id_group at a
given index = size of its connected component. Since twin_pairs only records pairs (multiplicity
>=2 relationships), multiplicity-1 (isolated, no twin) N's are invisible here BY CONSTRUCTION --
that is fine for this task's specific ask ("多重度>=3を全報告"), since any N with true
multiplicity>=3 necessarily appears in >=2 twin_pairs entries (a clique of size>=3 has >=3
edges), hence is fully visible in this data. This does NOT claim knowledge of the full
multiplicity-1/2 distribution beyond what set_ii_lt384/set_i_750/set_iii_L3 already established
elsewhere (that is out of scope for this aggregation).

Canary: the known 750-clique (id_group=[750,6], 10 pairs = C(5,2)) must reduce to exactly ONE
connected component of size 5 (multiplicity=5) -- this is the FIB-MULT target case named
explicitly in 裁定803/HA-GAP-5 ("指数750の10対...繊維多重度10の実例" -- NOTE: the addendum's own
HA-GAP-5 language says "多重度10" referring to the PAIR COUNT (10 = C(5,2)), whereas this
script's own multiplicity definition is the NODE COUNT (5, the clique size) -- both are reported
raw below, discrepancy disclosed explicitly, not silently resolved).
Also: the addendum's own SS1.2 Q8-FAM table (8 pairs, m=1..15 odd) must each reduce to
multiplicity=2 (twin pairs, not larger cliques) -- re-derivable from this same aggregation as a
second canary.

No verdict language. Raw multiplicity counts and booleans only.
"""
import json
import hashlib


CENSUS_PATH = "search/certs/lins_twin_census_v1_20260806.json"


def node_key(index, member):
    return (index, tuple(sorted(member["canonical_id_words"])))


def main():
    census = json.load(open(CENSUS_PATH, encoding="utf-8"))
    census_sha256 = hashlib.sha256(open(CENSUS_PATH, "rb").read()).hexdigest()

    twin_pairs = census["twin_pairs"]

    # union-find over node_key identities
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
    edge_count_per_pair_index_idgroup = {}  # (index, id_group_tuple) -> pair count (raw, for HA-GAP-5 cross-check)

    for tp in twin_pairs:
        idx = tp["index"]
        m0, m1 = tp["members"]
        idg0 = tuple(m0["id_group"])
        idg1 = tuple(m1["id_group"])
        if idg0 != idg1:
            raise ValueError(f"twin pair at index={idx} has mismatched id_group between members: {idg0} vs {idg1}")
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

    # connected components -> multiplicity
    components = {}
    for k in parent:
        r = find(k)
        components.setdefault(r, []).append(k)

    # aggregate by (index, id_group)
    mult_by_index_idgroup = {}
    for r, members in components.items():
        idx, idg = node_id_group[members[0]]
        # sanity: all members of this component must share the same (index,id_group)
        for m in members:
            assert node_id_group[m] == (idx, idg), "component has inconsistent (index,id_group)"
        key = (idx, idg)
        # a given (index,id_group) could in principle have MULTIPLE disjoint cliques (if the
        # twin relation were not fully transitive in the data, or if there are genuinely
        # separate clusters at the same index+id_group) -- track as a list, not overwrite
        mult_by_index_idgroup.setdefault(key, []).append(len(members))

    # flatten: report each connected component's multiplicity (node count = clique size)
    all_components_raw = []
    for (idx, idg), sizes in mult_by_index_idgroup.items():
        for sz in sizes:
            all_components_raw.append({"index": idx, "id_group": list(idg), "multiplicity_nodes": sz})

    all_components_raw.sort(key=lambda r: (-r["multiplicity_nodes"], r["index"]))

    mult_ge_3 = [r for r in all_components_raw if r["multiplicity_nodes"] >= 3]

    # HA-GAP-5 cross-reference: pair-count (edges) for the same (index,id_group) keys, reported
    # alongside node-count, to make the "10 vs 5" distinction explicit (not silently resolved)
    for r in all_components_raw:
        key2 = (r["index"], tuple(r["id_group"]))
        r["pair_count_edges"] = edge_count_per_pair_index_idgroup.get(key2, None)

    # canaries
    canary_750 = [r for r in all_components_raw if r["id_group"] == [750, 6]]
    canary_750_ok = (len(canary_750) == 1 and canary_750[0]["multiplicity_nodes"] == 5
                      and canary_750[0]["pair_count_edges"] == 10)

    q8fam_id_groups = [[24,3],[72,3],[120,15],[168,22],[216,3],[264,12],[312,25],[360,14]]
    canary_q8fam = []
    for idg in q8fam_id_groups:
        matches = [r for r in all_components_raw if r["id_group"] == idg]
        canary_q8fam.append({"id_group": idg, "matches": matches})
    canary_q8fam_all_mult_2 = all(
        len(c["matches"]) == 1 and c["matches"][0]["multiplicity_nodes"] == 2
        for c in canary_q8fam
    )

    total_nodes = len(parent)
    total_components = len(components)

    out = {
        "schema": "shadow-atelier/fib_mult_v1",
        "authority": "裁定803 (FIB-SWEEP撤回・置換), docs/notes/hunting_chapter_v1_addendum_a.md "
                     "§4.2 発注 FIB-MULT",
        "method_note": "pure aggregation of the ALREADY-COMMITTED search/certs/"
                       "lins_twin_census_v1_20260806.json (174 twin pairs, index<=1000, "
                       "single LowIndexNormalSubgroupsSearch call per LID-1 discipline). NO new "
                       "GAP run in this script. Nodes=distinct N (fingerprint=(index,sorted "
                       "canonical_id_words)), edges=twin_pairs entries, "
                       "multiplicity=connected-component size (clique size, per the source "
                       "cert's own documented twin-relation=equivalence-relation fact).",
        "source_cert": CENSUS_PATH,
        "source_cert_sha256": census_sha256,
        "scope_note": "index<=1000 only (the source cert's own scope). Multiplicity-1 "
                      "(isolated, no twin) N's are invisible in this aggregation by "
                      "construction (they never appear in twin_pairs) -- irrelevant for the "
                      "multiplicity>=3 ask, since any true multiplicity>=3 clique necessarily "
                      "has >=3 edges, all present in twin_pairs.",
        "total_distinct_N_nodes_with_a_twin": total_nodes,
        "total_connected_components": total_components,
        "all_components": all_components_raw,
        "multiplicity_ge_3": mult_ge_3,
        "multiplicity_ge_3_count": len(mult_ge_3),
        "canary_750_clique": {
            "note": "expected: exactly 1 component, multiplicity_nodes=5 (5 distinct N), "
                    "pair_count_edges=10 (=C(5,2), matching HA-GAP-5's own '10対' language for "
                    "the PAIR count, distinct from this script's node-count definition of "
                    "multiplicity -- both reported, discrepancy disclosed not resolved).",
            "found": canary_750,
            "pass": canary_750_ok,
        },
        "canary_q8fam_all_multiplicity_2": {
            "note": "addendum_a §1.2's 8 Q8-FAM pairs (m=1,3,5,7,9,11,13,15) should each reduce "
                    "to multiplicity_nodes=2 (ordinary twin pairs, not larger cliques).",
            "detail": canary_q8fam,
            "pass": canary_q8fam_all_mult_2,
        },
        "no_verdict_note": "raw multiplicity counts, component lists, and booleans only. No "
                           "judgment words -- 発効は司令塔専権.",
    }
    out_path = "search/certs/fib_mult_v1_20260811.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"total_nodes={total_nodes} total_components={total_components}")
    print(f"multiplicity_ge_3_count={len(mult_ge_3)}")
    for r in mult_ge_3:
        print(f"  index={r['index']} id_group={r['id_group']} multiplicity_nodes={r['multiplicity_nodes']} pair_count_edges={r['pair_count_edges']}")
    print(f"canary_750_clique.pass={canary_750_ok}")
    print(f"canary_q8fam_all_multiplicity_2.pass={canary_q8fam_all_mult_2}")


if __name__ == "__main__":
    main()
