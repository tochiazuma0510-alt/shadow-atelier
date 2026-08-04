#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lane Sigma v2 driver -- HS 発火条件 4/5 の versioned summary(便102 F102-1.3 の4指定履行)。
入力: cert JSON のみ(4本)+ NW-P8 addendum(overlay, path+digest)。
driver コードは読まない(3レーン+p5control のいずれのdriverソースも本スクリプトはimportしていない -- JSON値のみ読む)。
出力: search/certs/hsp7_cond4_summary_v2_20260805.json への素材(JSON)。
"""
import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root (worktree root)

def sha256_of_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def load_json(relpath: str):
    p = ROOT / relpath
    return json.loads(p.read_text(encoding="utf-8")), sha256_of_file(p), str(relpath)

# ---- 1. pin inputs (path + machine-recomputed digest) ----
INPUTS = {}
for key, relpath in [
    ("laneS", "search/certs/hsp7_cond4_laneS_20260804.json"),
    ("laneV_v3", "search/certs/hsp7_cond4_laneV_v3_20260804.json"),
    ("laneP", "search/certs/hsp7_cond4_laneP_20260804.json"),
    ("laneP_p5control", "search/certs/hsp7_cond4_laneP_p5control_20260805.json"),
]:
    obj, digest, path = load_json(relpath)
    INPUTS[key] = {"obj": obj, "sha256": digest, "path": path}

# NW-P8 addendum overlay -- not a cert JSON (it is a note md), pin path+digest only, do not parse its prose as data.
ADDENDUM_PATH = "docs/notes/hs_prop7_translation_v1_addendum_nwp8_v1.md"
ADDENDUM_SHA256 = sha256_of_file(ROOT / ADDENDUM_PATH)

LANESPEC_PATH = "docs/notes/hsp7_cond4_lanespec_v1.md"
LANESPEC_SHA256 = sha256_of_file(ROOT / LANESPEC_PATH)

SOL102_PATH = "sol/sol_reply_102_math29.md"
SOL102_SHA256 = sha256_of_file(ROOT / SOL102_PATH)

# sanity: Sol reply F102-1.3 item1 quotes Lane V v3 digest as "c7a7...f68d"
assert INPUTS["laneV_v3"]["sha256"].startswith("c7a7") and INPUTS["laneV_v3"]["sha256"].endswith("f68d"), \
    "Lane V v3 digest does not match Sol reply F102-1.3 item1 pinned prefix/suffix"

laneS = INPUTS["laneS"]["obj"]
laneV = INPUTS["laneV_v3"]["obj"]
laneP = INPUTS["laneP"]["obj"]
laneP5 = INPUTS["laneP_p5control"]["obj"]

# ---- 2. B-1/B-2/B-4 re-evaluation from the aggregate predicate (F102-1.3 item2) ----
# B-1: execution_isolation physical evidence restored in the cert (not just a self-report boolean).
b1_fields = laneV.get("execution_isolation", {})
b1_present = all(k in b1_fields for k in ["worktree_created", "worktree_path", "stage_dir_deleted_before_run",
                                            "post_delete_listing", "post_delete_listing_sha256"])
b1_ok = bool(b1_present and b1_fields.get("worktree_created") is True and b1_fields.get("stage_dir_deleted_before_run") is True)

# B-2: N0 window evaluated for all 8 candidates (not just N window).
window_n0 = laneV.get("lane_specific_results", {}).get("window_N0", {})
n0_judgments = window_n0.get("hexagon_full_33_34_judgments", [])
b2_ok = len(n0_judgments) == 8

# B-4: rating correction -- cross_checked_status must not self-claim "cross-checked" pre-CV9.
ccs = laneV.get("cross_checked_status", {})
b4_ok = ccs.get("status") == "n/a"

b1_b2_b4_reeval = {
    "B-1_execution_isolation_physical_evidence": {
        "fields_present": b1_present,
        "worktree_created": b1_fields.get("worktree_created"),
        "stage_dir_deleted_before_run": b1_fields.get("stage_dir_deleted_before_run"),
        "post_delete_listing_sha256": b1_fields.get("post_delete_listing_sha256"),
        "verdict": "RESTORED" if b1_ok else "STILL_MISSING",
    },
    "B-2_N0_side_8_candidates": {
        "n0_candidate_count": len(n0_judgments),
        "expected_count": 8,
        "verdict": "COMPLETE" if b2_ok else "INCOMPLETE",
    },
    "B-4_rating_correction": {
        "cross_checked_status_in_laneV_v3": ccs,
        "self_claims_cross_checked": ccs.get("status") == "cross-checked",
        "verdict": "CORRECTED_TO_N/A" if b4_ok else "STILL_MISCLAIMED",
    },
    "note": "Lane Sigmaは新たな判定基準を作らない(lanespec v1.2 SS7 D-3(1))。ここではv3 certが自己申告する各欄の物理的な在/不在・値のみを機械確認し、CV-9副検問(hsp7_cond4_cv9_reading_v1.md)が課したB-1/B-2/B-4の修理要求に対する充足有無を転記する。",
}

# ---- 3. NW-P8 addendum overlay + S-8' application (F102-1.3 item3) ----
# S-8' (per addendum sec.3-1, sol_reply_102 F102-1.5 PASS): trigger = N/N0 judgment mismatch on >=1 item;
# verdict = IMPLEMENTATION_BUG_SUSPECTED / STOP.
window_n = laneV.get("lane_specific_results", {}).get("window_N", {})
n_judgments = window_n.get("hexagon_full_33_34_judgments", [])

def verdict_map(rows):
    return {r["key_id"]: r["verdict"] for r in rows}

n_map = verdict_map(n_judgments)
n0_map = verdict_map(n0_judgments)

s8prime_8candidates_rows = []
for kid in sorted(n_map.keys(), key=lambda x: (isinstance(x, str), x)):
    vn = n_map.get(kid)
    vn0 = n0_map.get(kid)
    s8prime_8candidates_rows.append({"key_id": kid, "verdictN": vn, "verdictN0": vn0, "agree": vn == vn0})

nw_p8 = laneV.get("nw_p8", {})
m_sweep_rows_raw = nw_p8.get("m_sweep_results", [])
s8prime_msweep_rows = [
    {"m": r["m"], "verdictN": r["verdictN"], "verdictN0": r["verdictN0"], "agree": r["agree"]}
    for r in m_sweep_rows_raw
]

all_s8prime_rows = s8prime_8candidates_rows + s8prime_msweep_rows
s8prime_mismatch_count = sum(1 for r in all_s8prime_rows if not r["agree"])
s8prime_fired = s8prime_mismatch_count >= 1  # S-8' trigger: >=1 mismatch

s8prime_applied = {
    "overlay": {
        "addendum_path": ADDENDUM_PATH,
        "addendum_sha256": ADDENDUM_SHA256,
        "note": "hs_prop7_translation_v1 追補(NW-P8 versioned撤回・S-8'再定義、candidate状態・sol_reply_102 F102-1.5でPASS=発効)。旧S-8(不一致0件でCALIBRATION_FAILED)は適用しない -- S-8'(1件でも不一致ならIMPLEMENTATION_BUG_SUSPECTED/STOP)を適用する。",
    },
    "predicate_source": "docs/notes/hs_prop7_translation_v1_addendum_nwp8_v1.md SS3 item1(S-8'定義, 逐語): trigger=「N と N0 の判定が1件でも食い違う」/ verdict=IMPLEMENTATION_BUG_SUSPECTED/STOP。sol_reply_102_math29.md F102-1.5でPASS(発効)。",
    "evaluated_scope": "Lane V v3のN/N0 8候補(dummy family 7件+h3負例1件) + NW-P8 m-sweep 5件 = 計13ペア。",
    "rows_8candidates": s8prime_8candidates_rows,
    "rows_msweep": s8prime_msweep_rows,
    "total_pairs_evaluated": len(all_s8prime_rows),
    "mismatch_count": s8prime_mismatch_count,
    "fired": s8prime_fired,
    "verdict": "not fired -- IMPLEMENTATION_BUG_SUSPECTED 未発火(不一致0件、13/13ペア一致)。" if not s8prime_fired
               else f"FIRED -- IMPLEMENTATION_BUG_SUSPECTED / STOP({s8prime_mismatch_count}件不一致)。",
    "arbitration_context_note": "仲裁(hsp7_hexagon_arbitration_v1.md, N∩F2=N0∩F2=V(F2))により、charming候補(f=1含む)ではN/N0のfull hexagon判定は理論上恒等に一致するはずと確定済み。ここでの不一致0件は、その定理の帰結としての一致を実測が再現した、という機械的事実の記録であり、Lane Sigma自身が新たに数学的解釈を追加するものではない。",
}

# ---- 4. NW-P7 cert (5 prechecks + 5/5 PASS) -> B-3 close, condition 4/5 -> cross-checked CANDIDATE ----
prechecks = laneP5.get("fail_closed_prechecks", {})
precheck_keys = ["precheck1_h4_order5_in_P5", "precheck2_jh4_order5_in_Q5", "precheck3_rho_bar_bijection_order5",
                  "precheck4_candidates_exactly_5", "precheck5_mutant_kill_source_map"]
precheck_verdicts = {}
for k in precheck_keys:
    block = prechecks.get(k, {})
    if k == "precheck5_mutant_kill_source_map":
        precheck_verdicts[k] = "PASS" if block.get("all_prechecks_pass") is not False else "SEE_NOTE"
    else:
        precheck_verdicts[k] = block.get("verdict")

all_prechecks_pass_flag = prechecks.get("all_prechecks_pass")
nwp7_results = laneP5.get("lane_specific_results", {}).get("pent_NW_P7", [])
nwp7_pass_count = sum(1 for r in nwp7_results if r.get("pent_verdict") == "PASS")
nwp7_total = len(nwp7_results)
s3_fired = laneP5.get("stop_rules", {}).get("S-3", {}).get("fired")

b3_close = {
    "input_cert": {"path": INPUTS["laneP_p5control"]["path"], "sha256": INPUTS["laneP_p5control"]["sha256"]},
    "prechecks_1_to_4_verdicts": {k: precheck_verdicts[k] for k in precheck_keys[:4]},
    "precheck5_mutant_kill_note": prechecks.get("precheck5_mutant_kill_source_map", {}).get("overall_note"),
    "all_prechecks_pass_declared": all_prechecks_pass_flag,
    "nwp7_pass_count": f"{nwp7_pass_count}/{nwp7_total}",
    "s3_fired": s3_fired,
    "verdict": "B-3 CLOSED" if (all_prechecks_pass_flag is True and nwp7_pass_count == 5 and nwp7_total == 5 and s3_fired is False) else "B-3 NOT CLOSED",
    "note": "sol_reply_102_math29.md F102-1.4は前検問5項の逐語履行を条件にNW-P7を限定認可した。laneP_p5control certはこの5項を走行前fail-closedに確認し(全PASS)、本走5/5 PASSを得た(S-3未発火)。lanespec v1.2の位置づけ(C-6順序ゲート・NW(5)は較正陽性を担う専用control)に照らし、B-3(=Lane P未較正)はこのcertの提出をもって閉じる。",
}

condition_4_5_status = {
    "b3_close": b3_close["verdict"],
    "rating": "cross-checked candidate" if b3_close["verdict"] == "B-3 CLOSED" else "UNCLOSED",
    "note": "★ candidate 語尾厳守(発注文どおり): 本certは条件4/5の全体を『cross-checked』の最終格へ昇格させるものではない。B-3が閉じたことにより cross-checked への昇格の**候補**へ上げる、まで。最終格付けはSol(便のゲート)の専権であり、Lane Sigmaはそれを僭称しない。",
}

# ---- 5. Sol NOTE: fix effective source chain by digest (not section-name only) ----
effective_source_chain = [
    {"path": INPUTS["laneS"]["path"], "sha256": INPUTS["laneS"]["sha256"], "role": "Lane S cert(候補鍵リスト+hexagon(3.10)(3.11)判定, window N)"},
    {"path": INPUTS["laneV_v3"]["path"], "sha256": INPUTS["laneV_v3"]["sha256"], "role": "Lane V cert v3(★正・B-1/B-2/B-4修理版, N/N0両窓hexagon(3.3)(3.4)判定, NW-P8 m-sweep)"},
    {"path": INPUTS["laneP"]["path"], "sha256": INPUTS["laneP"]["sha256"], "role": "Lane P cert(NW-P6/h3負例PENT/NW-P8 PENT側)"},
    {"path": INPUTS["laneP_p5control"]["path"], "sha256": INPUTS["laneP_p5control"]["sha256"], "role": "Lane P p=5 control cert(NW-P7、前検問5項+5/5 PASS、B-3閉じ手)"},
    {"path": ADDENDUM_PATH, "sha256": ADDENDUM_SHA256, "role": "NW-P8 versioned撤回・S-8'定義(overlay、sol_reply_102 F102-1.5でPASS=発効)"},
    {"path": LANESPEC_PATH, "sha256": LANESPEC_SHA256, "role": "発注設計書(v1.2)-- 述語の正本(S-9/S-8/S-8'適用先の定義)"},
    {"path": SOL102_PATH, "sha256": SOL102_SHA256, "role": "便102 F102-1.3(本certの発注根拠)・F102-1.4(NW-P7限定認可)・F102-1.5(S-8' PASS)"},
]

# ---- 6. S-9 (Lane S vs Lane V window N, unchanged predicate, using v3 now) ----
laneS_judgments = laneS.get("lane_specific_results", {}).get("hexagon_310_311_judgments", [])
laneS_map = {r["key_id"]: r["hexagon_verdict"] for r in laneS_judgments}
laneV_n_map = n_map  # window N verdicts from v3

s9_rows = []
for kid in sorted(laneS_map.keys()):
    vs = laneS_map.get(kid)
    vv = laneV_n_map.get(kid)
    s9_rows.append({"key_id": kid, "laneS": vs, "laneV_N": vv, "agree": vs == vv})
s9_mismatch_count = sum(1 for r in s9_rows if not r["agree"])
s9_fired = s9_mismatch_count >= 1

s9_applied = {
    "predicate_source": "lanespec v1.2 SS6 stop_rules.S-9(逐語, 不変): 「同一窓 N 上で Lane S と Lane V の項目別判定(候補ごとPASS/FAIL/UNKNOWN)が1件でも食い違う」 -> LANE_DISAGREEMENT / INTEGRITY_STOP。",
    "rows": s9_rows,
    "mismatch_count": s9_mismatch_count,
    "fired": s9_fired,
    "verdict": "not fired" if not s9_fired else "FIRED -- LANE_DISAGREEMENT / INTEGRITY_STOP",
}

# ---- 7. self-calibration: 2 fixtures (all-agree / 1-key-mismatch), v1と同型で再実施 ----
def s9_predicate(rows):
    """入力: [{key_id, laneS, laneV}] のリスト。出力: (fired, mismatch_count)"""
    mismatches = sum(1 for r in rows if r["laneS"] != r["laneV"])
    return (mismatches >= 1, mismatches)

fixture_1_all_agree = [
    {"key_id": i, "laneS": "PASS" if i < 8 else "FAIL", "laneV": "PASS" if i < 8 else "FAIL"}
    for i in range(1, 9)
]
fixture_1_fired, fixture_1_mismatch = s9_predicate(fixture_1_all_agree)

fixture_2_one_mismatch = [dict(r) for r in fixture_1_all_agree]
fixture_2_one_mismatch[3]["laneV"] = "FAIL" if fixture_2_one_mismatch[3]["laneV"] == "PASS" else "PASS"  # flip key_id=4
fixture_2_fired, fixture_2_mismatch = s9_predicate(fixture_2_one_mismatch)

def s8prime_predicate(rows):
    mismatches = sum(1 for r in rows if r["verdictN"] != r["verdictN0"])
    return (mismatches >= 1, mismatches)

s8prime_fixture_1_all_agree = [
    {"m_or_key": i, "verdictN": "PASS" if i % 3 == 0 else "FAIL", "verdictN0": "PASS" if i % 3 == 0 else "FAIL"}
    for i in range(1, 14)
]
s8f1_fired, s8f1_mismatch = s8prime_predicate(s8prime_fixture_1_all_agree)

s8prime_fixture_2_one_mismatch = [dict(r) for r in s8prime_fixture_1_all_agree]
s8prime_fixture_2_one_mismatch[6]["verdictN0"] = "PASS" if s8prime_fixture_2_one_mismatch[6]["verdictN0"] == "FAIL" else "FAIL"
s8f2_fired, s8f2_mismatch = s8prime_predicate(s8prime_fixture_2_one_mismatch)

self_calibration = {
    "note": "D-3(2)の要求(全一致/1鍵不一致の2組)をv1と同型で再実施。v2追加分: S-8'述語(N vs N0の1件以上不一致でfired)についても同型の2fixtureを追加(S-8'はv2で新設適用する述語のため)。",
    "s9_fixture_1_all_agree": {
        "description": "8件でLane S判定・Lane V判定が完全一致する合成fixture",
        "expected": "LANE_DISAGREEMENT(S-9)を発火しないこと",
        "observed_fired": fixture_1_fired, "observed_mismatch_count": fixture_1_mismatch,
        "pass": fixture_1_fired is False,
    },
    "s9_fixture_2_one_key_mismatch": {
        "description": "8件中key_id=4のみLane V側を反転させた合成fixture",
        "expected": "LANE_DISAGREEMENT(S-9)を発火すること",
        "observed_fired": fixture_2_fired, "observed_mismatch_count": fixture_2_mismatch,
        "pass": fixture_2_fired is True and fixture_2_mismatch == 1,
    },
    "s8prime_fixture_1_all_agree": {
        "description": "13ペア(8候補+m-sweep5)でN・N0判定が完全一致する合成fixture",
        "expected": "IMPLEMENTATION_BUG_SUSPECTED(S-8')を発火しないこと",
        "observed_fired": s8f1_fired, "observed_mismatch_count": s8f1_mismatch,
        "pass": s8f1_fired is False,
    },
    "s8prime_fixture_2_one_key_mismatch": {
        "description": "13ペア中1件のみN0側を反転させた合成fixture",
        "expected": "IMPLEMENTATION_BUG_SUSPECTED(S-8')を発火すること",
        "observed_fired": s8f2_fired, "observed_mismatch_count": s8f2_mismatch,
        "pass": s8f2_fired is True and s8f2_mismatch == 1,
    },
}
self_calibration["overall_pass"] = all([
    self_calibration["s9_fixture_1_all_agree"]["pass"],
    self_calibration["s9_fixture_2_one_key_mismatch"]["pass"],
    self_calibration["s8prime_fixture_1_all_agree"]["pass"],
    self_calibration["s8prime_fixture_2_one_key_mismatch"]["pass"],
])

# ---- assemble driver raw output ----
output = {
    "inputs_pinned": {k: {"path": v["path"], "sha256": v["sha256"]} for k, v in INPUTS.items()},
    "addendum_pinned": {"path": ADDENDUM_PATH, "sha256": ADDENDUM_SHA256},
    "lanespec_pinned": {"path": LANESPEC_PATH, "sha256": LANESPEC_SHA256},
    "sol102_pinned": {"path": SOL102_PATH, "sha256": SOL102_SHA256},
    "b1_b2_b4_reeval": b1_b2_b4_reeval,
    "s8prime_applied": s8prime_applied,
    "b3_close": b3_close,
    "condition_4_5_status": condition_4_5_status,
    "effective_source_chain": effective_source_chain,
    "s9_applied": s9_applied,
    "self_calibration": self_calibration,
}

if __name__ == "__main__":
    out_path = ROOT / "scratchpad" / "laneSigmaV2_driver_output.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "laneV_v3_sha256": INPUTS["laneV_v3"]["sha256"],
        "b1_ok": b1_ok, "b2_ok": b2_ok, "b4_ok": b4_ok,
        "s8prime_mismatch_count": s8prime_mismatch_count, "s8prime_fired": s8prime_fired,
        "s9_mismatch_count": s9_mismatch_count, "s9_fired": s9_fired,
        "b3_verdict": b3_close["verdict"],
        "condition_4_5_rating": condition_4_5_status["rating"],
        "self_calibration_overall_pass": self_calibration["overall_pass"],
    }, indent=2, ensure_ascii=False))
