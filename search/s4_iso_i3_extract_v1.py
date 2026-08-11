#!/usr/bin/env python3
"""
search/s4_iso_i3_extract_v1.py -- (I3) existing-cert re-read for N_S4's isolated status
(裁定886, docs/notes/ent_arith_type_gate_v2.md §4).

Task (verbatim, gate v2 §4 (I3)): "既存 cert の再読 -- ihnec 戦役が N'∈I を仮定していたか"
(表読み・最安・先に見る -- SPLIT-NULL の前件に N'∈I がある という gate v2 の読みの裏取り).

METHOD: direct textual re-reading of docs/notes/ihnec_v1.md (theorem SPLIT-NULL's literal
statement and its application to N_S4), docs/notes/surj_s4_v2.md (§3.5, the underlying cert
field), docs/notes/auto_settled_check_v1.md (a NEWER partial-closure route, VERBAL-ISO), and
provenance/LEDGER.md (for 裁定219/【SD-a】, the origin ruling of this open flag). This is a
"表読み" (table/text reading) task, not a computation -- there is no algorithm to run; the
result is a documentary finding, reported here as a structured cert per this project's
established discipline (matching search/u9bit_extract_v1.py's style for an analogous
document-reading task).

RESULT (raw, no verdict language):
(1) CONFIRMED: theorem SPLIT-NULL's literal statement (ihnec_v1.md line 374) includes "N'∈I"
    as an explicit stated hypothesis -- gate v2's (I3) hypothesis is textually correct.
(2) The campaign's APPLICATION of this theorem with N'=N_S4 (§6.5's predictions P-IHN-1..7,
    and the measurement sections that follow) does NOT independently establish N_S4∈I -- it is
    explicitly tracked as an OPEN precondition, tagged (S4-ISO), in ihnec_v1.md's own
    "前件表" (precondition table), lines 319 and 411.
(3) The underlying GAP certificate's own "isolated" field is a HARDCODED "UNKNOWN" placeholder
    (surj_s4_v2.md line 78, citing week3-psl-common.g L452) -- NOT a computed value.
(4) A SEPARATE document's isolated table claims "true" for N_S4, but this is explicitly labeled
    a HUMAN-DERIVED reading from the raw "settled 54/54" machine measurement, not itself a
    machine-verified or proof-based confirmation of Def 3.13's isolated predicate
    (surj_s4_v2.md lines 77-78, 259: "証明書自身は 'isolated: UNKNOWN' と書いている...
    week4-E2作戦_v1.md の isolated 表が true と記すのは...人が導いた読みである").
(5) A NEWER partial-closure mechanism exists (lemma VERBAL-ISO, docs/notes/
    auto_settled_check_v1.md) that lets isolated-ness be established WITHOUT machine
    computation for SOME windows (via N_F2 being verbal) -- but this document EXPLICITLY
    states it does NOT apply to N_S4/(S4-ISO): "ただし PSL(2,8) 窓 (S4-ISO) と W-5 には適用
    できない(N_{F_2} が verbal として構成されていないため)" (line 262).
(6) Origin: this whole open-item class is tracked as 【SD-a】, traced to 裁定219 (campaign-wide
    warning that wall-window isolated-ness was never independently verified).

No verdict language beyond the raw found/not-found status and direct quotation of the relevant
lines.
"""
import json


def main():
    findings = [
        {
            "id": "F1",
            "finding": "theorem SPLIT-NULL's literal statement includes 'N'∈I' as an "
                       "explicit hypothesis -- confirms gate v2's (I3) reading is textually "
                       "correct.",
            "source": "docs/notes/ihnec_v1.md line 374",
            "quote": "n 奇 ≥3、N'∈I、M:=K^{(n)}∩N' とし、"
                     "G_n=PB_3/K^{(n)} と PB_3/N' に共通の非自明"
                     "な商が無いと仮定する。",
        },
        {
            "id": "F2",
            "finding": "the campaign's APPLICATION of SPLIT-NULL with N'=N_S4 (predictions "
                       "P-IHN-1..7, §6.5) does NOT independently establish N_S4∈I -- "
                       "it is explicitly tracked as an OPEN precondition (S4-ISO) in the "
                       "document's own precondition table.",
            "source": "docs/notes/ihnec_v1.md lines 319, 411",
            "quote": "前件の明示: (S4-ISO) N_S4 が isolated であ"
                     "ること。状態: 機械測定(settled "
                     "54/54)のみ・証明書は 'isolated:UNKNOWN'"
                     "。→ 報告は「(S4-ISO)条件つき」"
                     "と明記すること。",
        },
        {
            "id": "F3",
            "finding": "the underlying GAP certificate's own 'isolated' field is a HARDCODED "
                       "'UNKNOWN' placeholder, not a computed value.",
            "source": "docs/notes/surj_s4_v2.md line 78 (citing week3-psl-common.g L452)",
            "quote": "証明書自身は 'isolated: UNKNOWN' と書い"
                     "ている(week3-psl-common.g L452 のハードコ"
                     "ード)。",
        },
        {
            "id": "F4",
            "finding": "a SEPARATE document's isolated table claims 'true' for N_S4, but this "
                       "is explicitly labeled a HUMAN-DERIVED reading from raw 'settled 54/54' "
                       "measurement data, not a machine-verified or proof-based confirmation.",
            "source": "docs/notes/surj_s4_v2.md lines 77-78, 259",
            "quote": "week4-E2作戦_v1.md の isolated 表が true と記"
                     "すのは、その 54/54 settled から人が"
                     "導いた読みである。証明書の"
                     "欄と文書の表が食い違って"
                     "いる。",
        },
        {
            "id": "F5",
            "finding": "a NEWER partial-closure mechanism (lemma VERBAL-ISO) EXPLICITLY does "
                       "NOT apply to N_S4/(S4-ISO) -- confirmed still open as of the most "
                       "recent related document found.",
            "source": "docs/notes/auto_settled_check_v1.md line 262",
            "quote": "ただし PSL(2,8) 窓 (S4-ISO) と W-5 には適用"
                     "できない(N_{F_2} が verbal として構成"
                     "されていないため)。",
        },
        {
            "id": "F6",
            "finding": "origin: this open-item class is tracked as 【SD-a】, traced to "
                       "裁定219 (campaign-wide warning that wall-window isolated-ness "
                       "was never independently verified).",
            "source": "docs/notes/e1_canonical_v1.md lines 182, 199; "
                      "docs/notes/ihnec_v1.md line 319/411",
            "quote": "壁窓の isolated (W1) 未検証。裁定219。",
        },
    ]

    established = False  # per findings F2-F5: explicitly tracked as OPEN, not established

    missing_for_i1_handoff = [
        "a genuine machine-verified or proof-based confirmation that N_S4 satisfies the "
        "canonical isolated definition (Def 3.13: 'N is isolated if every GT-shadow in GT(N) "
        "is settled') -- the cert's own field is a hardcoded placeholder, not a real "
        "computation over the 54 elements of GT(N_S4) checking ker(T_{m,f})=N_S4 for each.",
        "OR a paper-proof route analogous to VERBAL-ISO, but VERBAL-ISO itself is documented "
        "as NOT applicable to N_S4 (N_F2 for this window is not constructed as verbal) -- gate "
        "v2's own suggested route is different: PSL(2,8)'s SIMPLICITY (no proper nontrivial "
        "normal subgroups => no intermediate window can be built), which has NOT been checked "
        "against this specific isolated-predicate application in any found document.",
    ]

    out = {
        "schema": "shadow-atelier/s4_iso_i3_extract_v1",
        "authority": "裁定886 -- docs/notes/ent_arith_type_gate_v2.md §4 (I3) 既存cert再読",
        "method_note": "documentary re-reading task (表読み), not a computation. Direct textual "
                       "search of docs/notes/ihnec_v1.md, docs/notes/surj_s4_v2.md, "
                       "docs/notes/auto_settled_check_v1.md, docs/notes/e1_canonical_v1.md, and "
                       "provenance/LEDGER.md for N_S4's isolated-status determination and "
                       "SPLIT-NULL's stated precondition.",
        "gate_v2_i3_hypothesis": "SPLIT-NULL's precondition includes N'∈I "
                                  "(docs/notes/ent_arith_type_gate_v2.md §4, quoted verbatim: "
                                  "'SPLIT-NULLの前件にN'∈Iがある')",
        "gate_v2_i3_hypothesis_confirmed": True,
        "findings": findings,
        "n_s4_isolated_established": established,
        "missing_for_i1_handoff": missing_for_i1_handoff,
        "no_verdict_note": "raw documentary findings (direct quotes + line-number citations) "
                           "only. No judgment on WHAT THIS MEANS for the gate's overall "
                           "readiness (that is the commander's/mathematician's determination) "
                           "-- only whether N_S4∈I was found to be established.",
    }
    out_path = "search/certs/s4_iso_i3_extract_v1_20260812.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"gate_v2_i3_hypothesis_confirmed={out['gate_v2_i3_hypothesis_confirmed']}")
    print(f"n_s4_isolated_established={established}")
    for f in findings:
        print(f"  {f['id']}: {f['source']}")


if __name__ == "__main__":
    main()
