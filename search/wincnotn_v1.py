#!/usr/bin/env python3
"""
search/wincnotn_v1.py -- WIN-CNOTN (裁定823③, hunting_chapter_v1_addendum_a.md §3 "発注
WIN-CNOTN": "census/lins出力からN<=PB3(B3/N->>S3)かつc notin N を抽出し、e=2jのjを出力").
This pass covers the NEW band (1000,2000] only, per 裁定823's explicit scope ("新帯(1000,2000]
の窓層/c∉N分類数") -- the (0,1000] band's window layer was already fully classified elsewhere
(L2=15/L3=13, docs/notes/theorem_check_mirrorall_l3vacuous_v1.md §G.6.b).

Method: PURE AGGREGATION of the already-committed search/certs/lins_census_2000_v1_20260811.json
(twin_pairs, index<=2000, GHA run 31498009539). NO new GAP run. For every twin-pair MEMBER
(not just window ones) with index in (1000,2000], cross-tabulate by (in_PB3, c_in_N) -- both
fields already recorded per-member by the source cert (search/lins-census-2000-v1.g). Reports
RAW COUNTS ONLY (verbal_status is explicitly OUT OF SCOPE here, per the task's own "verbal_status
なし・数のみ" instruction -- matching this project's established discipline that verbal-
constructibility determination is a separate, not-yet-attempted judgment, per
lins-census-2000-v1.g's own "verbal_status: UNKNOWN for every row in this pass by design" note).

SCOPE CAVEAT (disclosed): this counts only TWIN-PAIR MEMBERS (i.e. N's that have at least one
other N at the same index with an isomorphic quotient) -- the source cert does not export
isolated (non-twinned) N's at all. This is NOT a full census of the (1000,2000] band's normal
subgroups; it is the window/c-notin-N classification restricted to the subset the source cert
actually recorded. Disclosed, not silently presented as exhaustive.

No verdict language. Raw counts and booleans only.
"""
import json
import hashlib

CENSUS_PATH = "search/certs/lins_census_2000_v1_20260811.json"


def main():
    census = json.load(open(CENSUS_PATH, encoding="utf-8"))
    census_sha256 = hashlib.sha256(open(CENSUS_PATH, "rb").read()).hexdigest()

    band_lo, band_hi = 1000, 2000
    members_in_band = []
    for tp in census["twin_pairs"]:
        idx = tp["index"]
        if band_lo < idx <= band_hi:
            for m in tp["members"]:
                members_in_band.append({
                    "index": idx,
                    "id_group": m["id_group"],
                    "in_PB3": m["in_PB3"],
                    "c_in_N": m["c_in_N"],
                })

    total = len(members_in_band)

    def count(in_pb3, c_in_n):
        return sum(1 for m in members_in_band
                   if m["in_PB3"] == in_pb3 and m["c_in_N"] == c_in_n)

    window_c_in_n = count(True, True)
    window_c_notin_n = count(True, False)
    nonwindow_c_in_n = count(False, True)
    nonwindow_c_notin_n = count(False, False)

    window_total = window_c_in_n + window_c_notin_n
    nonwindow_total = nonwindow_c_in_n + nonwindow_c_notin_n

    # the specific WIN-CNOTN target population: window AND c not in N
    win_cnotn_members = [m for m in members_in_band if m["in_PB3"] and not m["c_in_N"]]

    out = {
        "schema": "shadow-atelier/wincnotn_v1",
        "authority": "裁定823③ (WIN-CNOTN, hunting_chapter_v1_addendum_a.md §3 発注 WIN-CNOTN, "
                     "restricted to the NEW (1000,2000] band per 裁定823's explicit scope)",
        "method_note": "pure aggregation of the ALREADY-COMMITTED search/certs/"
                       "lins_census_2000_v1_20260811.json (twin_pairs, index<=2000, GHA run "
                       "31498009539). NO new GAP run. Cross-tabulates (in_PB3, c_in_N) for every "
                       "twin-pair member with index in (1000,2000]. verbal_status NOT reported "
                       "(out of scope per task instruction; counts only).",
        "source_cert": CENSUS_PATH,
        "source_cert_sha256": census_sha256,
        "scope_caveat": "counts ONLY twin-pair members (N's with at least one isomorphic-"
                        "quotient partner at the same index) -- the source cert does not export "
                        "isolated (non-twinned) N's, so this is NOT a full census of the "
                        "(1000,2000] band's normal subgroups, only the subset the source cert "
                        "actually recorded.",
        "band": [band_lo, band_hi],
        "total_members_in_band": total,
        "cross_tab": {
            "window_c_in_N": window_c_in_n,
            "window_c_notin_N": window_c_notin_n,
            "nonwindow_c_in_N": nonwindow_c_in_n,
            "nonwindow_c_notin_N": nonwindow_c_notin_n,
        },
        "window_total": window_total,
        "nonwindow_total": nonwindow_total,
        "win_cnotn_target_count": len(win_cnotn_members),
        "win_cnotn_target_members": win_cnotn_members,
        "no_verdict_note": "raw counts only. No judgment words, no verbal_status determination "
                           "-- 発効は司令塔専権.",
    }
    out_path = "search/certs/wincnotn_v1_20260812.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"total_members_in_band={total}")
    print(f"window_c_in_N={window_c_in_n} window_c_notin_N={window_c_notin_n} "
          f"nonwindow_c_in_N={nonwindow_c_in_n} nonwindow_c_notin_N={nonwindow_c_notin_n}")
    print(f"window_total={window_total} nonwindow_total={nonwindow_total}")
    print(f"win_cnotn_target_count={len(win_cnotn_members)}")
    for m in win_cnotn_members:
        print(f"  index={m['index']} id_group={m['id_group']}")


if __name__ == "__main__":
    main()
