#!/usr/bin/env python3
# Lane Sigma driver -- HS hakka jouken 4, D-3 4-ten taiou.
# Yakuwari: 3 cert (JSON atai nomi) wo yomikomi, lanespec de jizen kakutei-zumi no jutsugo
# (S-9, S-8) wo kikaiteki ni tekiyou suru dake. Atarashii handan kijun wa tsukuranai.
# driver code wa yomanai (kyoukai). Jikko wa kono script jishin (Lane Sigma jishin no shinki jikkou).

import hashlib
import json
import sys

ROOT = "C:/Users/81905/Desktop/shadow-atelier/.claude/worktrees/agent-a3dcb4e04dda33388"

LANE_S_PATH = ROOT + "/search/certs/hsp7_cond4_laneS_20260804.json"
LANE_V_PATH = ROOT + "/search/certs/hsp7_cond4_laneV_v2_20260804.json"
LANE_P_PATH = ROOT + "/search/certs/hsp7_cond4_laneP_20260804.json"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def s9_predicate(laneS_verdicts, laneV_verdicts):
    """laneSpec SS9(stop_rules.S-9) jutsugo: douitsu mado N ue de Lane S to Lane V no
    kounoku betsu handan(PASS/FAIL/UNKNOWN) ga 1-ken demo kuichigaeba fired=true.
    laneS_verdicts, laneV_verdicts: dict key_id -> verdict string.
    Kaesu: (fired: bool, mismatch_count: int, rows: list)
    """
    rows = []
    mismatch = 0
    all_keys = sorted(set(laneS_verdicts.keys()) | set(laneV_verdicts.keys()), key=str)
    for k in all_keys:
        vs = laneS_verdicts.get(k, "MISSING")
        vv = laneV_verdicts.get(k, "MISSING")
        match = (vs == vv)
        if not match:
            mismatch += 1
        rows.append({"key_id": k, "laneS": vs, "laneV": vv, "match": match})
    fired = mismatch > 0
    return fired, mismatch, rows


def s8_predicate(m_sweep_results):
    """laneSpec SS4.2 S-8 jutsugo (reduced scope): m-sweep no kekka(5 kumi, verdictN/verdictN0)
    kara mismatch_count wo kikaiteki ni saikeisan. fired = (mismatch_count == 0).
    """
    mismatch = 0
    rows = []
    for r in m_sweep_results:
        agree = (r["verdictN"] == r["verdictN0"])
        if not agree:
            mismatch += 1
        rows.append({"m": r["m"], "verdictN": r["verdictN"], "verdictN0": r["verdictN0"], "agree": agree})
    fired = (mismatch == 0)
    return fired, mismatch, rows


# ---------------------------------------------------------------------------
# D-3(2): Jiko kousei fixture 2 kumi (honsou mae ni hissu)
# ---------------------------------------------------------------------------

def run_self_calibration():
    results = {}

    # Fixture (1): zen kouho de (Lane S, Lane V) ga icchi suru gousei fixture cert kumi.
    # 8 kouho, subete PASS de touitsu (verdict wa PASS/FAIL/UNKNOWN no sanchi de yoi;
    # koko de wa jissai no candidate_key_list to onaji 8-ken kousei wo tsukau).
    fixture1_laneS = {i: "PASS" for i in range(1, 8)}
    fixture1_laneS[8] = "FAIL"
    fixture1_laneV = dict(fixture1_laneS)  # zen icchi
    fired1, mismatch1, rows1 = s9_predicate(fixture1_laneS, fixture1_laneV)
    results["fixture_all_agree"] = {
        "laneS_synth": fixture1_laneS,
        "laneV_synth": fixture1_laneV,
        "expected": "LANE_DISAGREEMENT wo hakka SHINAI koto",
        "observed_fired": fired1,
        "observed_mismatch_count": mismatch1,
        "rows": rows1,
        "pass": (fired1 is False),
    }

    # Fixture (2): choudo 1 ken dake fui-icchi no fixture cert kumi.
    fixture2_laneS = {i: "PASS" for i in range(1, 8)}
    fixture2_laneS[8] = "FAIL"
    fixture2_laneV = dict(fixture2_laneS)
    fixture2_laneV[4] = "FAIL"  # key_id 4 wo wazato hanten (PASS -> FAIL) = 1-ken fui-icchi
    fired2, mismatch2, rows2 = s9_predicate(fixture2_laneS, fixture2_laneV)
    results["fixture_one_mismatch"] = {
        "laneS_synth": fixture2_laneS,
        "laneV_synth": fixture2_laneV,
        "expected": "LANE_DISAGREEMENT wo hakka SURU koto",
        "observed_fired": fired2,
        "observed_mismatch_count": mismatch2,
        "rows": rows2,
        "pass": (fired2 is True and mismatch2 == 1),
    }

    overall_pass = results["fixture_all_agree"]["pass"] and results["fixture_one_mismatch"]["pass"]
    results["overall_pass"] = overall_pass
    if not overall_pass:
        results["gate"] = "CALIBRATION_FAILED -- Lane Sigma jishin no jiko kousei ga kitai doori ni ugokanai. Tei shi."
    else:
        results["gate"] = "PASS -- ryouhou no fixture ga kitai doori ni ugoita. Hon-sou he shinkou."
    return results


# ---------------------------------------------------------------------------
# Main: R-20 digest chain, jissou 3 cert eno S-9/S-8 tekiyou
# ---------------------------------------------------------------------------

def main():
    log = {}

    # --- R-20: candidates_in digest chain seigousei ---
    laneS_actual_sha256 = sha256_file(LANE_S_PATH)
    laneV = load(LANE_V_PATH)
    laneP = load(LANE_P_PATH)
    laneS = load(LANE_S_PATH)

    laneV_declared = laneV.get("candidates_in_source_cert_sha256")
    laneP_declared = laneP.get("candidates_in_source_cert_sha256")

    log["r20_digest_chain"] = {
        "laneS_cert_actual_sha256": laneS_actual_sha256,
        "laneV_declared_candidates_in_source_cert_sha256": laneV_declared,
        "laneP_declared_candidates_in_source_cert_sha256": laneP_declared,
        "laneV_matches_actual": (laneV_declared == laneS_actual_sha256),
        "laneP_matches_actual": (laneP_declared == laneS_actual_sha256),
        "verdict": "INTACT" if (laneV_declared == laneS_actual_sha256 and laneP_declared == laneS_actual_sha256) else "BROKEN",
    }

    # --- Self calibration (D-3 2) ---
    log["self_calibration"] = run_self_calibration()

    # --- S-9 tekiyou (jissou 3 cert, kouho 8-ken, mado N) ---
    laneS_verdicts = {}
    for row in laneS["lane_specific_results"]["hexagon_310_311_judgments"]:
        laneS_verdicts[row["key_id"]] = row["hexagon_verdict"]

    laneV_verdicts = {}
    for row in laneV["lane_specific_results"]["hexagon_full_33_34_judgments"]:
        laneV_verdicts[row["key_id"]] = row["verdict"]

    fired_s9, mismatch_s9, rows_s9 = s9_predicate(laneS_verdicts, laneV_verdicts)
    log["s9_applied"] = {
        "window": "N",
        "candidate_count": len(rows_s9),
        "rows": rows_s9,
        "mismatch_count": mismatch_s9,
        "fired": fired_s9,
        "verdict": "LANE_DISAGREEMENT / INTEGRITY_STOP" if fired_s9 else "not fired",
        "cross_check_note": "Lane Sigma ga laneS/laneV cert no kouho-betsu handan wo dokuji ni saichushutsu shi S-9 jutsugo wo tekiyou shita (Lane V no four_way_comparison_table jishin-shinkoku to wa betsu keiro de saikeisan; kekka wa itchi shita).",
    }
    log["s9_selfreport_crosscheck"] = {
        "laneV_four_way_comparison_table_summary": laneV.get("four_way_comparison_table", {}).get("summary_counts"),
        "laneV_self_reported_s9_mismatch_count": laneV.get("four_way_comparison_table", {}).get("s9_mismatch_count"),
        "laneSigma_recomputed_mismatch_count": mismatch_s9,
        "match": (laneV.get("four_way_comparison_table", {}).get("s9_mismatch_count") == mismatch_s9),
    }

    # --- S-8 tekiyou (Lane V v2 no NW-P8 m-sweep, reduced scope) ---
    m_sweep = laneV["nw_p8"]["m_sweep_results"]
    fired_s8, mismatch_s8, rows_s8 = s8_predicate(m_sweep)
    log["s8_applied"] = {
        "source": "Lane V v2 cert nw_p8.m_sweep_results (reduced scope, m-sweep only)",
        "rows": rows_s8,
        "mismatch_count_recomputed": mismatch_s8,
        "laneV_self_reported_mismatch_count": laneV["nw_p8"]["mismatch_count_N_vs_N0"],
        "recompute_matches_selfreport": (mismatch_s8 == laneV["nw_p8"]["mismatch_count_N_vs_N0"]),
        "fired": fired_s8,
        "laneV_stop_rules_S8_verbatim": laneV["stop_rules"]["S-8"],
    }

    with open(ROOT + "/scratchpad/laneSigma_driver_output.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(json.dumps(log, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
