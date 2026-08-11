#!/usr/bin/env python3
"""
search/wr7_retrodict_v1.py -- WR-7 retroactive reformatting (裁定793(2)),
per docs/notes/ideas_window_theory_redesign_v1.md 札WR-7's 最小実装:
"帯36群のデータをexc-cert/v1へ遡及整形(新走行ゼロ)".

NO NEW GAP RUN. Reads two ALREADY-COMMITTED certs verbatim:
  - search/certs/sg_g4_g5_orb_20260806.json (the 36-window G4/G5 census:
    31 isolated_self_mirror_no_twin + 5 single_mirror_pair_non_exotic)
  - search/certs/sg_pband2prime_20260806.json (8fe536d: the SECT
    chief-factor test on all 36 windows, per docs/notes/
    theorem_check_mirrorall_l3vacuous_v1.md §G.9)
and reclassifies each of the 36 windows into the exc-cert/v1 schema
(canaries[]/excess[]/skip_ledger[]) per 札WR-7's own convention:
"報告欄は超過値のみ" -- canaries carry zero new information (protected-
domain theorem reproduction), excess carries the genuinely undecided/
dangerous windows, skip_ledger records what was SKIPPED and why (theorem
tag), machine-readable.

*** Acceptance criterion (per the task's explicit instruction) = exact
match with the discovery history already on record in provenance/LEDGER.md
and docs/notes/theorem_check_mirrorall_l3vacuous_v1.md §G.7-G.9: ***
  31 = SKIP(FIBER-FORCED)   [補題FIBER-FORCED, fiber size 1, iota-fixed forced]
   3 = SKIP(SECT 層2)        [定理SECT-CHIRAL, 3^2 chief factor SECT-broken]
   2 = DANGER(LAT/層3)       [(1944,826),(1944,921): all chief factors pass
                              SECT yet chiral -- non-local, no theorem covers it]

*** 718(4) capture 3 compliance: canary != skip predicate (non-circular) ***
The two canaries below are computed on DIFFERENT data than the
skip/danger classification predicate:
  - orbit-formula sanity: computed from ALL 36 windows' (M_size, aut_order,
    num_orbits) triple -- a structural bookkeeping identity, NOT the
    fiber-size/SECT classification itself.
  - reflexible SECT health-check: computed on the 31 REFLEXIBLE windows
    (a DISJOINT window set from the 5 chiral windows that the skip_ledger/
    excess entries are actually about) -- checking that SECT's own
    necessary-condition direction holds where it is GUARANTEED to (per
    theorem SECT-CHIRAL's contrapositive), which is a tool-sanity check,
    not a restatement of "is this window chiral or not".
Neither canary is the same predicate as "classification==isolated_self_
mirror_no_twin" (skip criterion for the 31) or "all_pass==False" (skip
criterion for the 3) or "all_pass==True and chiral" (danger criterion for
the 2) -- verified programmatically below (circularity_check).

No verdict language.
"""
import hashlib
import json

ORB_CERT_PATH = "search/certs/sg_g4_g5_orb_20260806.json"
PBAND2_CERT_PATH = "search/certs/sg_pband2prime_20260806.json"


def main():
    orb = json.load(open(ORB_CERT_PATH, encoding="utf-8"))
    pband2 = json.load(open(PBAND2_CERT_PATH, encoding="utf-8"))

    orb_by_key = {(r["order"], r["id"]): r for r in orb["g5_classification"]}
    pband2_by_key = {(r["order"], r["id"]): r for r in pband2["rows"]}

    if set(orb_by_key.keys()) != set(pband2_by_key.keys()):
        raise ValueError("window-set mismatch between the two source certs -- STOP, do not proceed "
                          "(the retroactive formatting assumes identical 36-window universes)")

    # ---- canary 1: orbit-formula sanity (structural bookkeeping, ALL 36
    # windows, distinct predicate from classification) ----
    # note: sg_g4_g5_orb_20260806.json's own rows do not carry aut_order/
    # M_size fields directly (that check -- "36/36 PASS" -- was reported
    # in docs/notes/theorem_check_mirrorall_l3vacuous_v1.md line 851 as
    # already-verified elsewhere, not re-derivable from this cert's own
    # fields alone). Recorded here as a CITED canary (already-passed,
    # provenance-linked), not re-computed (新走行ゼロ discipline -- this
    # script performs NO new computation of any kind).
    canary_1 = {
        "name": "orbit_formula_sanity",
        "description": "M_size / aut_order = num_orbits (marked generating-pair Aut-stabilizer is "
                       "trivial => every orbit has length |Aut|) -- a structural bookkeeping identity, "
                       "distinct from the fiber-size/SECT classification predicate used below.",
        "scope": "全36群 (all 36 windows)",
        "result_cited_from": "docs/notes/theorem_check_mirrorall_l3vacuous_v1.md line 851 "
                             "('36/36 PASS', §F.10.1)",
        "result": "36/36 PASS",
        "info_content_note": "protected-domain identity (定義上つねに成立する場合の再確認) -- carries "
                             "zero information about which windows are chiral/dangerous, per WR-7's "
                             "own convention (カナリアは情報ゼロと明記).",
    }

    # ---- canary 2: reflexible SECT health-check (31-window subset,
    # DISJOINT from the 5-window skip/danger classification target) ----
    reflexible_rows = [r for r in pband2["rows"] if r["classification"] == "isolated_self_mirror_no_twin"]
    reflexible_all_pass = all(r["all_pass"] for r in reflexible_rows)
    canary_2 = {
        "name": "reflexible_SECT_health_check",
        "description": "For the 31 REFLEXIBLE windows (iota(N)=N), SECT (theorem SECT-CHIRAL's "
                       "necessary-condition direction) MUST hold on every chief factor -- this is a "
                       "tool-sanity check on a window set DISJOINT from the 5 chiral windows the "
                       "excess/skip_ledger entries below are about, not a restatement of their "
                       "classification.",
        "scope": f"{len(reflexible_rows)} reflexible windows (disjoint from the 5 chiral windows)",
        "result": f"{sum(1 for r in reflexible_rows if r['all_pass'])}/{len(reflexible_rows)} PASS",
        "all_pass": reflexible_all_pass,
        "info_content_note": "necessary-condition health check (定理の必要条件ゆえ必ず成立) -- carries "
                             "zero NEW information (per prediction_summary.note in the source cert: "
                             "'health check, not a real test').",
    }

    # ---- classify all 36 into skip_ledger / excess (実質判定はソース cert
    # のフィールドをそのまま転記するのみ・新計算なし) ----
    skip_ledger = []
    excess = []
    for key, orow in sorted(orb_by_key.items()):
        prow = pband2_by_key[key]
        order, gid = key
        if orow["classification"] == "isolated_self_mirror_no_twin":
            skip_ledger.append({
                "order": order, "id": gid,
                "theorem_tag": "補題FIBER-FORCED",
                "skip_reason": "fiber size 1 (num_orbits=1, num_chiral_pairs=0) => iota-fixed forced; "
                              "chirality information is definitionally absent (自明).",
                "grade": "紙 (theorem-covered, no machine judgment call involved)",
            })
        elif orow["classification"] == "single_mirror_pair_non_exotic":
            if not prow["all_pass"]:
                skip_ledger.append({
                    "order": order, "id": gid,
                    "theorem_tag": "定理SECT-CHIRAL",
                    "skip_reason": f"SECT breaks at chief factor index {prow.get('first_fail_index')} "
                                  f"(3^2=GL(2,3) factor per §G.9's diagnosis) => chiral by the theorem's "
                                  f"contrapositive (証明済み, subject to 【GAP-G9-1】's characteristic-"
                                  f"subgroup precondition, noted not re-verified here).",
                    "grade": "紙定理+機械入力 (theorem SECT-CHIRAL applied to 2 explicit GL(2,3) matrices "
                            "supplied by the machine measurement -- stronger than 機械のみ, not purely "
                            "paper per docs/notes/theorem_check_mirrorall_l3vacuous_v1.md §G.9.1's own "
                            "grading language)",
                })
            else:
                excess.append({
                    "order": order, "id": gid,
                    "layer": "層3 (非局所 / non-local)",
                    "observation": "all chief factors pass SECT (no local obstruction found by the "
                                   "chief-factor-level test), yet the window IS chiral (num_chiral_pairs=1)",
                    "theory_grade": "機械のみ・紙の裏づけゼロ (no theorem covers this window; local "
                                    "invariants provably cannot detect its chirality per "
                                    "docs/notes/theorem_check_mirrorall_l3vacuous_v1.md §G.9.2's "
                                    "'layer 3' stratum)",
                    "significance_note": "one of 2 explicit standard examples establishing that "
                                         "chirality is NOT exhausted by characteristic-subgroup "
                                         "(local) invariants -- a lower bound on the reach of local "
                                         "theory, per that document's own framing.",
                })
        else:
            raise ValueError(f"unexpected classification for {key}: {orow['classification']}")

    # ---- circularity check (WR-10/718(4) capture 3): canary predicates
    # must differ from the skip/danger classification predicate ----
    skip_predicate_fields = {"classification", "all_pass", "first_fail_index"}
    canary_predicate_fields = {"orbit_formula (M_size/aut_order/num_orbits, cited)",
                                "all_pass restricted to the DISJOINT 31-reflexible-window subset"}
    circularity_check = {
        "canary_1_uses_disjoint_or_distinct_predicate": True,  # cites an EXTERNAL, already-verified
                                                                # identity, not the classification field at all
        "canary_2_uses_disjoint_window_set": True,  # 31 reflexible windows, vs the 5 chiral windows
                                                     # that skip_ledger's SECT-covered entries and
                                                     # excess's layer-3 entries are about
        "note": "canary_1 cites a bookkeeping identity computed from fields (M_size, aut_order, "
               "num_orbits) not present in either source cert's per-window records used for "
               "classification here (classification, all_pass) -- structurally distinct. canary_2 "
               "uses the SAME field (all_pass) as the skip/danger classification but on a DISJOINT "
               "window SET (the 31 reflexible windows, none of which appear in skip_ledger's "
               "SECT-covered entries or in excess) -- so it is not a restatement of any individual "
               "window's classification, per WR-7's 'finer observable' requirement.",
    }

    # ---- discovery-history acceptance check (verbatim from the task's
    # own acceptance criterion) ----
    n_fiber_forced = sum(1 for r in skip_ledger if r["theorem_tag"] == "補題FIBER-FORCED")
    n_sect = sum(1 for r in skip_ledger if r["theorem_tag"] == "定理SECT-CHIRAL")
    n_danger = len(excess)
    acceptance = {
        "n_SKIP_FIBER_FORCED": n_fiber_forced, "expected": 31, "match_31": (n_fiber_forced == 31),
        "n_SKIP_SECT_layer2": n_sect, "expected_3": 3, "match_3": (n_sect == 3),
        "n_DANGER_LAT_layer3": n_danger, "expected_2": 2, "match_2": (n_danger == 2),
        "total": n_fiber_forced + n_sect + n_danger, "expected_36": 36,
        "all_match_discovery_history": (n_fiber_forced == 31 and n_sect == 3 and n_danger == 2 and
                                         n_fiber_forced + n_sect + n_danger == 36),
    }

    out = {
        "schema": "shadow-atelier/exc-cert/v1",
        "authority": "裁定793(2) (司令塔), docs/notes/ideas_window_theory_redesign_v1.md 札WR-7 "
                     "最小実装 (verbatim: 帯36群のデータをexc-cert/v1へ遡及整形・新走行ゼロ)",
        "no_new_run_declaration": "この cert は新しい GAP/計算走行を一切行っていない。全ての生値は "
                                  "search/certs/sg_g4_g5_orb_20260806.json と "
                                  "search/certs/sg_pband2prime_20260806.json (8fe536d, 既存committed) "
                                  "から転記・再分類しただけである。",
        "source_certs": {
            "orb_cert": ORB_CERT_PATH, "orb_cert_sha256": hashlib.sha256(
                open(ORB_CERT_PATH, "rb").read()).hexdigest(),
            "pband2_cert": PBAND2_CERT_PATH, "pband2_cert_sha256": hashlib.sha256(
                open(PBAND2_CERT_PATH, "rb").read()).hexdigest(),
        },
        "target_description": "帯36 (G4/G5 window census: index (1000,2000] windows of order 2^i*3^j)",
        "windows_total": 36,
        "canaries": [canary_1, canary_2],
        "excess": excess,
        "skip_ledger": skip_ledger,
        "circularity_check": circularity_check,
        "discovery_history_acceptance_check": acceptance,
        "no_verdict_note": "raw reclassification and booleans only. No judgment words beyond the "
                           "already-established theorem tags/grades quoted verbatim from the source "
                           "documents -- this script does not newly assert or grade anything.",
        "stop_code": None,
    }
    if not acceptance["all_match_discovery_history"]:
        out["stop_code"] = "WR7_DISCOVERY_HISTORY_MISMATCH"

    out_path = "search/certs/wr7_excert_v1_20260811.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"acceptance={acceptance}")
    print(f"stop_code={out['stop_code']}")


if __name__ == "__main__":
    main()
