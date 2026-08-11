#!/usr/bin/env python
# crosscheck/check_fib_mult.py
# Independent checker for search/certs/fib_mult_v1_20260811.json (FIB-MULT, 裁定803,
# docs/notes/hunting_chapter_v1_addendum_a.md §4.2).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT import search/fib_mult_v1.py. Re-implements the
# union-find/clique-aggregation logic FROM SCRATCH, reading ONLY the ORIGINAL source cert
# (search/certs/lins_twin_census_v1_20260806.json), not the cert-under-test's own
# "all_components" field (which is treated as the thing being checked, not an input).
import json
import hashlib

CENSUS_PATH = "search/certs/lins_twin_census_v1_20260806.json"
CERT_PATH = "search/certs/fib_mult_v1_20260811.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry


def main():
    census_sha256 = hashlib.sha256(open(CENSUS_PATH, "rb").read()).hexdigest()
    census = json.load(open(CENSUS_PATH, encoding="utf-8"))
    cert = json.load(open(CERT_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/fib_mult_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/fib_mult_v1")

    if cert.get("source_cert_sha256") != census_sha256:
        fail(f"source_cert_sha256 mismatch: cert claims {cert.get('source_cert_sha256')}, "
             f"actual file hash {census_sha256}")
    else:
        ok(f"source_cert_sha256 matches actual file ({census_sha256})")

    # --- own independent aggregation (own key/edge logic, not copied from search script) ---
    uf = UnionFind()
    node_idg = {}
    edge_counts = {}

    def key_of(idx, member):
        return (idx, tuple(sorted(member["canonical_id_words"])))

    for tp in census["twin_pairs"]:
        idx = tp["index"]
        m0, m1 = tp["members"]
        idg0, idg1 = tuple(m0["id_group"]), tuple(m1["id_group"])
        if idg0 != idg1:
            fail(f"twin pair at index={idx}: member id_group mismatch {idg0} vs {idg1}")
            continue
        k0, k1 = key_of(idx, m0), key_of(idx, m1)
        node_idg[k0] = (idx, idg0)
        node_idg[k1] = (idx, idg1)
        uf.union(k0, k1)
        edge_counts[(idx, idg0)] = edge_counts.get((idx, idg0), 0) + 1

    comps = {}
    for k in node_idg:
        r = uf.find(k)
        comps.setdefault(r, []).append(k)

    rederived_components = []
    for r, members in comps.items():
        idx, idg = node_idg[members[0]]
        rederived_components.append({
            "index": idx, "id_group": list(idg), "multiplicity_nodes": len(members),
            "pair_count_edges": edge_counts.get((idx, idg)),
        })

    rederived_total_nodes = len(node_idg)
    rederived_total_components = len(comps)

    if rederived_total_nodes != cert.get("total_distinct_N_nodes_with_a_twin"):
        fail(f"total_distinct_N_nodes_with_a_twin rederived={rederived_total_nodes} "
             f"cert={cert.get('total_distinct_N_nodes_with_a_twin')}")
    else:
        ok(f"total_distinct_N_nodes_with_a_twin = {rederived_total_nodes}")

    if rederived_total_components != cert.get("total_connected_components"):
        fail(f"total_connected_components rederived={rederived_total_components} "
             f"cert={cert.get('total_connected_components')}")
    else:
        ok(f"total_connected_components = {rederived_total_components}")

    rederived_mult_ge_3 = sorted(
        [c for c in rederived_components if c["multiplicity_nodes"] >= 3],
        key=lambda r: (-r["multiplicity_nodes"], r["index"])
    )
    cert_mult_ge_3 = cert.get("multiplicity_ge_3", [])
    # compare as sets of (index, tuple(id_group), multiplicity_nodes, pair_count_edges)
    def norm(lst):
        return sorted((r["index"], tuple(r["id_group"]), r["multiplicity_nodes"], r["pair_count_edges"]) for r in lst)
    if norm(rederived_mult_ge_3) != norm(cert_mult_ge_3):
        fail(f"multiplicity_ge_3 mismatch: rederived={norm(rederived_mult_ge_3)} cert={norm(cert_mult_ge_3)}")
    else:
        ok(f"multiplicity_ge_3 rederived exactly: {norm(rederived_mult_ge_3)}")

    if cert.get("multiplicity_ge_3_count") != len(rederived_mult_ge_3):
        fail(f"multiplicity_ge_3_count cert={cert.get('multiplicity_ge_3_count')} rederived={len(rederived_mult_ge_3)}")
    else:
        ok(f"multiplicity_ge_3_count = {len(rederived_mult_ge_3)}")

    # canary re-derivations
    c750 = [c for c in rederived_components if c["id_group"] == [750, 6]]
    c750_ok = (len(c750) == 1 and c750[0]["multiplicity_nodes"] == 5 and c750[0]["pair_count_edges"] == 10)
    if c750_ok != cert["canary_750_clique"]["pass"]:
        fail(f"canary_750_clique.pass rederived={c750_ok} cert={cert['canary_750_clique']['pass']}")
    else:
        ok(f"canary_750_clique.pass = {c750_ok} (found={c750})")

    q8fam_id_groups = [[24,3],[72,3],[120,15],[168,22],[216,3],[264,12],[312,25],[360,14]]
    q8fam_ok = all(
        len([c for c in rederived_components if c["id_group"] == idg]) == 1 and
        [c for c in rederived_components if c["id_group"] == idg][0]["multiplicity_nodes"] == 2
        for idg in q8fam_id_groups
    )
    if q8fam_ok != cert["canary_q8fam_all_multiplicity_2"]["pass"]:
        fail(f"canary_q8fam_all_multiplicity_2.pass rederived={q8fam_ok} cert={cert['canary_q8fam_all_multiplicity_2']['pass']}")
    else:
        ok(f"canary_q8fam_all_multiplicity_2.pass = {q8fam_ok}")

    print()
    print(f"raw summary: {len(rederived_mult_ge_3)} component(s) with multiplicity>=3 found "
          f"(independently rederived from {CENSUS_PATH} alone): {norm(rederived_mult_ge_3)}")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
