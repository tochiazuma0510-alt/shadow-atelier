#!/usr/bin/env python3
"""
r6a_summarize.py -- pure reformatting of search/certs/r6a_word_iota_checker_v1_20260806.json
into the 3 output tables R-6a's task instruction asked for (k-value for the
750-clique B-members / mirror classification of the <384 pairs / mirror-or-
exotic classification of the L3 13 pairs). No new computation -- reads the
checker's own results field and regroups it. GT-shadow-predicate-free.
"""
import json

with open("search/certs/r6a_word_iota_checker_v1_20260806.json", encoding="utf-8") as f:
    d = json.load(f)
res = d["results"]

clique = [r for r in res if r["fiber"].startswith("clique750")]
lt384 = [r for r in res if r["fiber"].startswith("lt384")]
l3 = [r for r in res if r["fiber"].startswith("L3")]


def pair_table(rows):
    byfiber = {}
    for r in rows:
        byfiber.setdefault(r["fiber"], []).append(r)
    out = []
    for fib, ms in sorted(byfiber.items()):
        ms = sorted(ms, key=lambda r: r["uid"])
        if len(ms) != 2:
            out.append({"pair_fiber": fib, "classification": "NOT_A_SIMPLE_PAIR", "members": [m["uid"] for m in ms]})
            continue
        m0, m1 = ms
        if m0["iota_is_fixed"] and m1["iota_is_fixed"]:
            cls = "BOTH_FIXED (not mirror-related to each other -- twin explained by something other than iota)"
        elif m0["iota_matches"] == [m1["uid"]] and m1["iota_matches"] == [m0["uid"]]:
            cls = "MIRROR (iota swaps the two members of this pair)"
        else:
            cls = "OTHER (" + str([m["iota_matches"] for m in ms]) + ")"
        out.append({"pair_fiber": fib, "index": m0["index"], "classification": cls,
                    "m0_uid": m0["uid"], "m1_uid": m1["uid"]})
    return out


clique_table = [{"uid": r["uid"], "iota_matches": r["iota_matches"], "iota_is_fixed": r["iota_is_fixed"]}
                 for r in sorted(clique, key=lambda r: r["uid"])]
lt384_table = pair_table(lt384)
l3_table = pair_table(l3)

lt384_mirror = sum(1 for p in lt384_table if p["classification"].startswith("MIRROR"))
lt384_fixed = sum(1 for p in lt384_table if p["classification"].startswith("BOTH_FIXED"))
l3_mirror = sum(1 for p in l3_table if p["classification"].startswith("MIRROR"))
l3_fixed = sum(1 for p in l3_table if p["classification"].startswith("BOTH_FIXED"))

out = {
    "schema": "r6a-word-iota-summary/v1",
    "note": "Pure reformatting of search/certs/r6a_word_iota_checker_v1_20260806.json (系統B "
            "results). No new computation. No GT-shadow predicate (hexagon/charming/SURJ/kernel_"
            "multiplicity/settled/isolated/GTSh/arithmeticity) evaluated. 'MIRROR'/'BOTH_FIXED' "
            "here means ONLY the word-level iota(generator-inversion) automorphism relation "
            "between the two subgroups, not any GT-shadow-theoretic classification.",
    "source": "search/certs/r6a_word_iota_checker_v1_20260806.json",
    "set_i_750_clique_B_members": {
        "note": "All 5 members of the 750-clique (A + B1..B4), self-vs-fiber iota classification.",
        "detail": clique_table,
        "k_value": {
            "definition": "number of the 4 B-members that are individually iota-fixed",
            "value": sum(1 for r in clique_table if r["uid"].startswith("clique750:B") and r["iota_is_fixed"]),
            "of_4_B_members": 4,
        },
        "A_member_iota_fixed": next(r["iota_is_fixed"] for r in clique_table if r["uid"] == "clique750:A"),
        "mirror_pairs_among_all_5": 0,
        "consequence_for_exotic_count_per_LEDGER_formula_10_minus_k": "k(mirror pairs)=0 => exotic=10 (all 10 unordered pairs unexplained by iota)",
    },
    "set_ii_lt384_pairs": {
        "note": "45 registered twin pairs with index<384.",
        "detail": lt384_table,
        "summary": {"total_pairs": len(lt384_table), "mirror_pairs": lt384_mirror, "both_fixed_pairs": lt384_fixed},
    },
    "set_iii_L3_pairs": {
        "note": "13 registered L3 pairs (in_PB3=True, c_in_N=False, both members).",
        "detail": l3_table,
        "summary": {"total_pairs": len(l3_table), "mirror_pairs": l3_mirror, "both_fixed_pairs": l3_fixed},
    },
}

with open("search/certs/r6a_summary_v1_20260806.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("Wrote search/certs/r6a_summary_v1_20260806.json")
print("750-clique: k(B-members fixed)=", out["set_i_750_clique_B_members"]["k_value"]["value"], "of 4")
print("lt384: mirror=", lt384_mirror, "both_fixed=", lt384_fixed, "of", len(lt384_table), "pairs")
print("L3: mirror=", l3_mirror, "both_fixed=", l3_fixed, "of", len(l3_table), "pairs")
