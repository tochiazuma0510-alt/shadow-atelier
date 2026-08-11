#!/usr/bin/env python3
"""
search/p2_strike_v1_1.py -- P2-STRIKE cert v1.1 (裁定778(2)/【P2-GAP-7】,
per docs/notes/p2_address_strike_design_v1_addendum_a.md §1.3, §4).

Formalizes algorithm B''s j* output (already computed in the v1 cert's
S_b_S_c_per_target[*].j_star field, from the blind subagent's independent
computation, search/certs/p2_strike_v1_20260807.json) as an explicit
deliverable, and performs the deep post-hoc cross-check against Kellner
2007 Table A.3's s1/s2 columns that addendum_a §1.3 requested
(【文献要請】: "Kellner Table A.3 の s1,s2 列...が l'=我々の j* を与えるか").

*** FINDING ***
For all 9 targets: s1 == k0 EXACTLY, and s2 == j* EXACTLY (all 9/9,
verified below by direct comparison of the already-committed j* values
against the already-committed Kellner Table A.3 transcription). This is
reported as a raw structural fact (does the table give a recoverable
formula, format-matching question per addendum_a §1.3) -- the
INTERPRETATION of what this means for CC-1* / GAMMA-EDGE-9 is explicitly
left to the mathematician (addendum_a's own instruction: "解釈は数学者").

No verdict language. Both j* and Kellner s1/s2 were independently
computed BEFORE this comparison was made (j* by the blind subagent per
裁定773's independence protocol, disclosed in search/p2_strike_v1.py;
Kellner's table by paper-scout in docs/scout/p2_literature_survey_v1.md,
independent of this project's own computation) -- this script performs
only the comparison, not a re-derivation of either side.
"""
import json

P2_STRIKE_V1_CERT_PATH = "search/certs/p2_strike_v1_20260807.json"

# Kellner 2007 (arXiv:math/0409223) Table A.3, p.39 -- same transcription
# already used in search/p2_strike_v1.py's S_f literature crosscheck,
# reused here unchanged (not re-derived).
KELLNER_TABLE_A3 = {
    (37, 32): {"delta": 21, "s1": 32, "s2": 7},
    (59, 44): {"delta": 26, "s1": 44, "s2": 15},
    (67, 58): {"delta": 21, "s1": 58, "s2": 49},
    (101, 68): {"delta": 42, "s1": 68, "s2": 57},
    (103, 24): {"delta": 54, "s1": 24, "s2": 2},
    (131, 22): {"delta": 25, "s1": 22, "s2": 93},
    (149, 130): {"delta": 79, "s1": 130, "s2": 74},
    (157, 62): {"delta": 48, "s1": 62, "s2": 40},
    (157, 110): {"delta": 51, "s1": 110, "s2": 73},
}


def main():
    v1 = json.load(open(P2_STRIKE_V1_CERT_PATH, encoding="utf-8"))
    rows = v1["S_b_S_c_per_target"]

    per_target = []
    all_s1_eq_k0 = True
    all_s2_eq_jstar = True
    for row in rows:
        p, k0, j_star = row["p"], row["k0"], row["j_star"]
        kv = KELLNER_TABLE_A3[(p, k0)]
        s1_eq_k0 = (kv["s1"] == k0)
        s2_eq_jstar = (kv["s2"] == j_star)
        all_s1_eq_k0 = all_s1_eq_k0 and s1_eq_k0
        all_s2_eq_jstar = all_s2_eq_jstar and s2_eq_jstar
        per_target.append({
            "p": p, "k0": k0, "k_star": row["k_star"],
            "j_star_algorithm_Bprime": j_star,
            "j_star_degenerate_case": row["degenerate_case"],
            "kellner_delta": kv["delta"], "kellner_s1": kv["s1"], "kellner_s2": kv["s2"],
            "s1_equals_k0": s1_eq_k0,
            "s2_equals_j_star": s2_eq_jstar,
        })
        print(f"p={p} k0={k0}: j*(alg B')={j_star} | Kellner s1={kv['s1']} (==k0: {s1_eq_k0}) "
              f"s2={kv['s2']} (==j*: {s2_eq_jstar})", flush=True)

    out = {
        "schema": "shadow-atelier/p2_strike_v1.1",
        "authority": "裁定778(2) (司令塔), docs/notes/p2_address_strike_design_v1_addendum_a.md "
                     "§1.3/§4 【P2-GAP-7】/【文献要請】 (verbatim)",
        "supersedes_note": "adds explicit algorithm-B' j* formalization and the deep Kellner s1/s2 "
                           "cross-check to the v1 cert (search/certs/p2_strike_v1_20260807.json, "
                           "b8d06d6) -- v1's own j_star field (already independently computed by the "
                           "blind subagent per 裁定773) is REUSED here unchanged, not recomputed.",
        "source_v1_cert": P2_STRIKE_V1_CERT_PATH,
        "kellner_source": "docs/scout/p2_literature_survey_v1.md Table A.3 (Kellner 2007, "
                          "arXiv:math/0409223 -> Math. Comp. 76 (2007) 405-441, p.39)",
        "per_target": per_target,
        "all_s1_equals_k0": all_s1_eq_k0,
        "all_s2_equals_j_star": all_s2_eq_jstar,
        "format_question_answer": {
            "question": "addendum_a §1.3's 【文献要請】: does Kellner Table A.3's (s1,s2) format give "
                       "l'=our j* directly?",
            "raw_finding": "YES, for all 9/9 targets: s1 == k0 exactly, and s2 == j* exactly "
                          "(algorithm B''s independently-computed value). This is reported as a raw "
                          "structural match between two independently-produced datasets (our own "
                          "algorithm-B' computation and Kellner's published table), not as a "
                          "re-derivation of either.",
            "interpretation_deferred_to_mathematician": "whether this confirms Kellner's (s1,s2) "
                          "literally encodes (k0, j*) in general (vs. a coincidence limited to these "
                          "9 targets), and what it implies for CC-1*/GAMMA-EDGE-9's literature "
                          "cross-reference, is left to the mathematician per addendum_a's own "
                          "instruction ('解釈は数学者').",
        },
        "no_verdict_note": "raw comparison values and booleans only. No claim of 'cross-checked' "
                           "(this is a literature comparison, not two independent internal "
                           "computations of the same quantity -- per addendum_a §2's own explicit "
                           "guidance: 文献の裏書きは「他人の計算を引用した」であって「二系統一致」ではない).",
        "stop_code": None,
    }
    out_path = "search/certs/p2_strike_v1_1_20260811.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"all_s1_equals_k0={all_s1_eq_k0} all_s2_equals_j_star={all_s2_eq_jstar}")


if __name__ == "__main__":
    main()
