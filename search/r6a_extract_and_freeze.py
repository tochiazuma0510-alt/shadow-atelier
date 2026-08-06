#!/usr/bin/env python3
"""
r6a_extract_and_freeze.py -- R-6a scope freeze (sol/sol_reply_112_math38.md
F112-5/R-6a; 裁定637). Reads ONLY search/certs/lins_twin_census_v1_20260806.json
(the existing B3 twin census cert; not re-run, not modified) and extracts the
three target sets verbatim, per R-6a's exact scope:

  (i)   The 750-clique's 4 "B-members" (c_in_N=False; the 5th member "A" has
        c_in_N=True and is out of scope for this task -- included here only
        as a same-fiber CANDIDATE for the iota match, never as a target).
  (ii)  All registered census pairs with index < 384.
  (iii) The L3 layer: 13 registered pairs with in_PB3=True (both members) and
        c_in_N=False (both members) -- 裁定637/便112 R-4's "L3 13対".

Writes a FROZEN cert (member UID / canonical_id_words / set digest) BEFORE
any iota computation is performed, per task instruction ("走行前にmember
UID・canonical word list・集合digestを凍結certに記録"). This script does
ZERO group theory -- it is a pure extraction+hash step over already-computed,
already-committed census data.

UID scheme: "{layer}:{index}:{ordinal within that index's member list as it
appears in the census JSON, 0-based}" -- deterministic and reproducible from
the census file alone (no re-derivation, no renumbering across runs).

Output: search/certs/r6a_scope_freeze_v1_20260806.json
"""
import json
import hashlib

CENSUS_PATH = "search/certs/lins_twin_census_v1_20260806.json"
OUT_PATH = "search/certs/r6a_scope_freeze_v1_20260806.json"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    census_sha = sha256_file(CENSUS_PATH)
    with open(CENSUS_PATH, encoding="utf-8") as f:
        d = json.load(f)
    tp = d["twin_pairs"]
    assert d["census_index_hi"] == 1000, "census bound changed -- STOP, re-freeze required"

    # ---- (i) 750-clique: dedupe members by canonical_id_words tuple ----
    idx750_pairs = [p for p in tp if p["index"] == 750]
    members750 = {}
    for p in idx750_pairs:
        for m in p["members"]:
            key = tuple(m["canonical_id_words"])
            members750[key] = m
    assert len(members750) == 5, f"expected 5-member 750-clique, got {len(members750)}"
    clique_A = [(k, m) for k, m in members750.items() if m["c_in_N"]]
    clique_B = [(k, m) for k, m in members750.items() if not m["c_in_N"]]
    assert len(clique_A) == 1 and len(clique_B) == 4, (
        f"750-clique c_in_N split expected 1 True + 4 False, got "
        f"{len(clique_A)} True + {len(clique_B)} False")

    set_i = []
    set_i.append({"uid": "clique750:A", "role": "candidate_only (c_in_N=True, NOT a B-member target; "
                  "included only as a same-fiber iota-image candidate)",
                  "c_in_N": True, "in_PB3": clique_A[0][1]["in_PB3"],
                  "id_group": clique_A[0][1]["id_group"],
                  "canonical_id_words": list(clique_A[0][0])})
    for i, (k, m) in enumerate(clique_B):
        set_i.append({"uid": f"clique750:B{i+1}", "role": "target (B-member)",
                      "c_in_N": False, "in_PB3": m["in_PB3"],
                      "id_group": m["id_group"],
                      "canonical_id_words": list(k)})

    # ---- (ii) index < 384, all registered pairs ----
    idx_lt_384_pairs = [p for p in tp if p["index"] < 384]
    set_ii = []
    for pidx, p in enumerate(idx_lt_384_pairs):
        pair_uid = f"lt384:idx{p['index']}:pair{pidx}"
        for midx, m in enumerate(p["members"]):
            set_ii.append({"uid": f"{pair_uid}:m{midx}", "pair_uid": pair_uid,
                          "index": p["index"], "c_in_N": m["c_in_N"], "in_PB3": m["in_PB3"],
                          "id_group": m["id_group"],
                          "canonical_id_words": m["canonical_id_words"]})

    # ---- (iii) L3 layer: in_PB3=True (both) and c_in_N=False (both) ----
    def is_l3(p):
        ms = p["members"]
        return all(m["in_PB3"] for m in ms) and all(not m["c_in_N"] for m in ms)
    l3_pairs = [p for p in tp if is_l3(p)]
    assert len(l3_pairs) == 13, f"expected 13 L3 pairs, got {len(l3_pairs)}"
    set_iii = []
    for pidx, p in enumerate(l3_pairs):
        pair_uid = f"L3:idx{p['index']}:pair{pidx}"
        for midx, m in enumerate(p["members"]):
            set_iii.append({"uid": f"{pair_uid}:m{midx}", "pair_uid": pair_uid,
                           "index": p["index"], "c_in_N": m["c_in_N"], "in_PB3": m["in_PB3"],
                           "id_group": m["id_group"],
                           "canonical_id_words": m["canonical_id_words"]})

    # ---- digest over the frozen selection (deterministic JSON dump) ----
    frozen_payload = {"set_i_750_clique": set_i, "set_ii_lt384": set_ii, "set_iii_L3": set_iii}
    frozen_bytes = json.dumps(frozen_payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    frozen_digest = hashlib.sha256(frozen_bytes).hexdigest()

    out = {
        "schema": "r6a-scope-freeze-cert/v1",
        "authorization": "sol/sol_reply_112_math38.md F112-5/R-6a; 裁定637 task 2",
        "source_cert": CENSUS_PATH,
        "source_cert_sha256": census_sha,
        "note": "PURE EXTRACTION -- no group theory performed in this script. Frozen BEFORE any "
                "iota computation, per R-6a scope instruction. Target sets: (i) 750-clique 4 "
                "B-members (c_in_N=False) + the 1 A-member (c_in_N=True, candidate-only, not a "
                "target); (ii) all 45 registered twin pairs with index<384 (90 members); (iii) "
                "the 13 registered L3 pairs (in_PB3=True & c_in_N=False both members, 26 members).",
        "counts": {"set_i_750_clique_members": len(set_i), "set_i_B_member_targets": len(clique_B),
                   "set_ii_lt384_pairs": len(idx_lt_384_pairs), "set_ii_lt384_members": len(set_ii),
                   "set_iii_L3_pairs": len(l3_pairs), "set_iii_L3_members": len(set_iii)},
        "frozen_selection_sha256": frozen_digest,
        "set_i_750_clique": set_i,
        "set_ii_lt384": set_ii,
        "set_iii_L3": set_iii,
        "scope_prohibitions": {
            "hexagon": False, "charming": False, "SURJ": False, "kernel_multiplicity": False,
            "settled": False, "isolated": False, "GTSh": False, "arithmeticity": False,
            "window_label_on_in_PB3_false": False, "checker_TRUE_FALSE_verdict": False,
            "other_stage_unlock": False,
            "note": "This freeze cert records ZERO evaluation of any of the above -- word-level "
                    "iota identification only, per R-6a."}
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {OUT_PATH}")
    print(f"  set_i (750-clique): {len(set_i)} members ({len(clique_B)} B-member targets)")
    print(f"  set_ii (index<384): {len(idx_lt_384_pairs)} pairs, {len(set_ii)} members")
    print(f"  set_iii (L3): {len(l3_pairs)} pairs, {len(set_iii)} members")
    print(f"  frozen_selection_sha256: {frozen_digest}")


if __name__ == "__main__":
    main()
