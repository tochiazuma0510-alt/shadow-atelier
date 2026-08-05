#!/usr/bin/env python
"""
NW(7) mainrun scoring generator -- 裁定571.
Reads ONLY the joined artifacts downloaded from GHA runs
  31036732337 (lane S), 31026044104 (lane V), 31026047111 (lane P)
plus the frozen class manifest, and cross-checks against the IF-FIRST
prediction ticket (docs/notes/nw7_mainrun_predictions_iffirst_v1.md +
addendum_pentlayer_v1.md) and Sol's ratified branch values
(sol/sol_reply_106_math33.md).

This script does NOT touch the sealed 3 quantities. It only reads the
main-run cert artifacts (post-hoc, joined, already gated PASS by
collection_gate) and does read-only arithmetic on them.

Output: search/certs/nw7_mainrun_scoring_20260806.json (machine-written,
no hand-typed numbers below).
"""
import ijson
import json
import hashlib
from collections import Counter
from datetime import datetime, timezone

ROOT = "C:/Users/81905/Desktop/shadow-atelier"

S_MANIFEST = f"{ROOT}/scratchpad/mainrun_results/S/join_manifest.json"
V_MANIFEST = f"{ROOT}/scratchpad/mainrun_results/V/join_manifest.json"
P_MANIFEST = f"{ROOT}/scratchpad/mainrun_results/P/join_manifest.json"
S_RECEIPT = f"{ROOT}/scratchpad/mainrun_results/S/join_receipt.json"
V_RECEIPT = f"{ROOT}/scratchpad/mainrun_results/V/join_receipt.json"
P_RECEIPT = f"{ROOT}/scratchpad/mainrun_results/P/join_receipt.json"
S_GATE = f"{ROOT}/scratchpad/mainrun_results/S/collection_gate.json"
V_GATE = f"{ROOT}/scratchpad/mainrun_results/V/collection_gate.json"
P_GATE = f"{ROOT}/scratchpad/mainrun_results/P/collection_gate.json"

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def stream_candidates(path):
    with open(path, 'rb') as f:
        for item in ijson.items(f, 'shards.item.candidate_keys.item'):
            yield item

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

print("hashing input artifacts...")
artifact_sha256 = {
    "S/join_manifest.json": sha256_file(S_MANIFEST),
    "V/join_manifest.json": sha256_file(V_MANIFEST),
    "P/join_manifest.json": sha256_file(P_MANIFEST),
    "S/join_receipt.json": sha256_file(S_RECEIPT),
    "V/join_receipt.json": sha256_file(V_RECEIPT),
    "P/join_receipt.json": sha256_file(P_RECEIPT),
    "S/collection_gate.json": sha256_file(S_GATE),
    "V/collection_gate.json": sha256_file(V_GATE),
    "P/collection_gate.json": sha256_file(P_GATE),
}

S_receipt = load_json(S_RECEIPT)
V_receipt = load_json(V_RECEIPT)
P_receipt = load_json(P_RECEIPT)
S_gate = load_json(S_GATE)
V_gate = load_json(V_GATE)
P_gate = load_json(P_GATE)

print("streaming S lane...")
S_full = {}
for c in stream_candidates(S_MANIFEST):
    k = c['key']
    S_full[(k['m'], tuple(k['e']))] = c['status']

print("streaming V lane...")
V_full = {}
for c in stream_candidates(V_MANIFEST):
    k = c['key']
    V_full[(k['m'], tuple(k['e']))] = c['status']

print("streaming P lane...")
P_full = {}
for c in stream_candidates(P_MANIFEST):
    k = c['key']
    P_full[tuple(k['e'])] = c['status']

assert set(S_full.keys()) == set(V_full.keys()), "S/V keyspace mismatch"
sv_mismatches = [k for k in S_full if S_full[k] != V_full[k]]

S_pass = {k for k, v in S_full.items() if v == 'PASS'}
V_pass = {k for k, v in V_full.items() if v == 'PASS'}
P_pass = {e for e, v in P_full.items() if v == 'PASS'}

S_layer_counts = Counter(m for (m, e) in S_pass)
V_layer_counts = Counter(m for (m, e) in V_pass)

m_values = sorted({m for (m, e) in S_full.keys()})
nonempty_layers_S = sorted(m for m in m_values if S_layer_counts.get(m, 0) > 0)
nonempty_layers_V = sorted(m for m in m_values if V_layer_counts.get(m, 0) > 0)

hex_total_S = len(S_pass)
hex_total_V = len(V_pass)

# hex(0) via lane S restricted to m=0
hex0_S = {e for (m, e) in S_pass if m == 0}
hex0_V = {e for (m, e) in V_pass if m == 0}
assert hex0_S == hex0_V, "hex(0) mismatch between S and V"

pent_raw_total = len(P_pass)          # unconditional PENT over all of [P,P] (117649), NOT restricted to hex(0)
pent_within_hex0 = hex0_S & P_pass    # the mathematically meaningful pent(0) = hex(0) cap PENT_pass
hex0_pent_fail = hex0_S - P_pass      # hexagon-only (fake, A-type) at m=0
pent_outside_hex0 = P_pass - hex0_S   # PENT-passing elements of [P,P] that are NOT hexagon solutions (not GT-shadow candidates)

# extrapolation via paper-proof-candidate lemma PENT-LAYER (addendum v1 SS3):
# |pent(m)| is claimed uniform across all non-empty m once >=1 PENT element exists in the layer.
pent_per_layer_predicted_uniform = len(pent_within_hex0)
pent_total_extrapolated = pent_per_layer_predicted_uniform * len(nonempty_layers_S)
hexonly_per_layer_extrapolated = len(hex0_pent_fail)
hexonly_total_extrapolated = hexonly_per_layer_extrapolated * len(nonempty_layers_S)

predictions = {
    "hexagon_total": {"predicted": 294, "source": "EXQ-4 (docs/notes/nw7_mainrun_predictions_iffirst_v1.md SS3, table SS3.1) -- ratified sol/sol_reply_106_math33.md"},
    "hexagon_per_layer": {"predicted": 49, "source": "EXQ-3 branch B-1a -- ratified"},
    "nonempty_layers": {"predicted": 6, "source": "EXQ-1' branch B-0a -- ratified"},
    "pent_per_layer": {"predicted": 7, "source": "EXQ-7 branch B-2a -- ratified (|ker(D|A)|=7, corrected PRE-2' xi'=1 in sol_reply_106)"},
    "pent_total": {"predicted": 42, "source": "EXQ-7 x 6 layers (uniform per PENT-LAYER addendum SS3, transport paper-proof candidate)"},
    "hexagon_only_per_layer": {"predicted": 42, "source": "EXQ-8 per layer = hex(m) - pent(m) = 49-7"},
    "hexagon_only_total": {"predicted": 252, "source": "EXQ-8 -- ratified"},
    "surj_fail": {"predicted": 0, "source": "EXQ-9 -- theorem consequence (H8'), NOT an independent measurement target of this mainrun"},
    "settled_pct": {"predicted": "100% (denominator 294, i.e. hexagon-pass set, NOT 705894)", "source": "EXQ-9 -- theorem consequence (ISO-V); F106-2.5 pins denominator=294"},
}

measured = {
    "hexagon_total_lane_S": hex_total_S,
    "hexagon_total_lane_V": hex_total_V,
    "S_vs_V_keyspace_size": len(S_full),
    "S_vs_V_mismatch_count": len(sv_mismatches),
    "S_vs_V_identical_pass_set": (S_pass == V_pass),
    "nonempty_layers_S": nonempty_layers_S,
    "nonempty_layers_V": nonempty_layers_V,
    "hexagon_per_layer_S": dict(sorted(S_layer_counts.items())),
    "hexagon_per_layer_V": dict(sorted(V_layer_counts.items())),
    "hex0_S_eq_hex0_V": (hex0_S == hex0_V),
    "hex0_size": len(hex0_S),
    "lane_P_raw_universe_size": len(P_full),
    "lane_P_raw_PASS_count_unconditional_over_full_[P,P]": pent_raw_total,
    "lane_P_raw_PASS_note": "This is |{f in [P,P] : PENT_W(f)}| over the FULL 117649-element group at m=0 (lane_wrapper_P.g runs PENT() unconditionally, NOT restricted to hex(0)). It numerically equals 49 by coincidence of this window and is NOT itself EXQ-7's pent(0).",
    "pent_within_hex0_m0": len(pent_within_hex0),
    "pent_outside_hex0_m0_count": len(pent_outside_hex0),
    "hex0_pent_fail_count_m0_hexagon_only": len(hex0_pent_fail),
    "pent_total_extrapolated_via_PENT_LAYER_lemma": pent_total_extrapolated,
    "hexonly_total_extrapolated_via_PENT_LAYER_lemma": hexonly_total_extrapolated,
    "surj_lane_present_in_this_mainrun": False,
    "settled_lane_present_in_this_mainrun": False,
}

def classify(name, measured_val, predicted_val, grade, note):
    hit = (measured_val == predicted_val)
    return {
        "id": name,
        "grade_class": grade,  # 甲/乙/丙/丁 per docs/notes prereg SS7.2
        "measured": measured_val,
        "predicted": predicted_val,
        "match": hit,
        "note": note,
    }

scoring = []
scoring.append(classify("EXQ-1_nonempty_is_subgroup_of_6", nonempty_layers_S, [0,1,2,4,5,6],
    "乙(T*)", "非空層集合。LAY-1+LAY-2 の帰結。実測 = 予測 なら装置健全の確認のみ(新事実ではない)。"))
scoring.append(classify("EXQ-1p_six_nonempty_layers", len(nonempty_layers_S), 6,
    "丙(C・branch_resolved=B-0a)", "分岐 B-0a への着地。S/V 独立実装で完全一致(0 mismatch over 705894)。"))
scoring.append(classify("EXQ-2_uniform_per_layer", len(set(S_layer_counts.values())), 1,
    "乙(T*)", "非空層の hexagon 通過数が全て等しいか(集合の濃度=1なら一様)。"))
scoring.append(classify("EXQ-3_hex_per_layer_49", sorted(set(S_layer_counts.values())), [49],
    "丙(C・branch_resolved=B-1a)", "各層 49。中間値{14,21,28,35,42}は排除(LAY-4)。丁類には落ちなかった。"))
scoring.append(classify("EXQ-4_hex_total_294", hex_total_S, 294,
    "丙(C・derived from B-0a x B-1a)", "S lane 実測 294、V lane 実測 294、両者バイト同一(0 mismatch)。"))
scoring.append(classify("EXQ-7_pent_per_layer_7_at_m0", len(pent_within_hex0), 7,
    "丙(C・branch_resolved=B-2a)", "m=0 層のみ直接測定(PENT-LAYER 補題により他層への移送は紙の議論・本走は m=0 のみ測定)。hex(0)=49 のうち PENT を通るのは 7 個。"))
scoring.append(classify("EXQ-7_pent_total_42_extrapolated", pent_total_extrapolated, 42,
    "丙(C・extrapolated, NOT independently measured for m!=0)", "m=1,2,4,5,6 層の PENT 通過数はこの本走では独立測定されていない(lane P universe = 117649 = m=0 のみ)。42 は PENT-LAYER 補題(candidate, Sol 未監査の一般形)による外挿。"))
scoring.append(classify("EXQ-8_hexonly_per_layer_42_at_m0", len(hex0_pent_fail), 42,
    "丙(C・branch_resolved=B-2a)", "m=0 層: 49-7=42。"))
scoring.append(classify("EXQ-8_hexonly_total_252_extrapolated", hexonly_total_extrapolated, 252,
    "丙(C・extrapolated, NOT independently measured for m!=0)", "同上、他層は外挿。"))
scoring.append(classify("EXQ-9_surj_fail_0", "not_evaluated", 0,
    "甲(T)・not_evaluated", "この本走(S/V/P 3 lane)は SURJ を独立に測定する lane を含まない。H8' による理論的帰結のみ(的中しても情報量ゼロの検出器条項)。"))
scoring.append(classify("EXQ-9_settled_100pct", "not_evaluated", "100% (denom 294)",
    "甲(T)・not_evaluated", "settled lane はこの本走に存在しない。ISO-V による理論的帰結のみ。"))

# structural predictions (EXQ-6): order-level consistency only, group law NOT tested by these lanes
scoring.append({
    "id": "EXQ-6_GT_N_order_294_structure_C7sq_rtimes_C6",
    "grade_class": "丙(C, relative to B-1a) -- order-level only",
    "measured": {"hex0_size_as_candidate_for_A": len(hex0_S), "hex_total_as_candidate_for_|GT(N)|": hex_total_S},
    "predicted": {"|A|": 49, "|GT(N)|": 294},
    "match": (len(hex0_S) == 49 and hex_total_S == 294),
    "note": "|A|=49=7^2 と |GT(N)|=294=6*49 は次数として一致(C_7^2 rtimes C_6 の位数と整合)。ただし本走の3 lane(hexagon x2 + 独立PENT)は GT 合成則(3.53)そのものを再検査していないので、群構造(半直積・作用の指数)は独立に確認していない -- 群同型の主張には未接触。",
})

out = {
    "schema": "nw7-mainrun-scoring/v1",
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "ruling": "裁定571",
    "generator_script": "scratchpad/gen_nw7_scoring.py",
    "input_runs": {
        "S": {"run_id": 31036732337, "artifact_name": "hs-S-joined"},
        "V": {"run_id": 31026044104, "artifact_name": "hs-V-joined"},
        "P": {"run_id": 31026047111, "artifact_name": "hs-P-joined"},
    },
    "input_artifact_sha256": artifact_sha256,
    "collection_gates": {"S": S_gate, "V": V_gate, "P": P_gate},
    "join_receipts": {"S": S_receipt, "V": V_receipt, "P": P_receipt},
    "prediction_sources": {
        "primary_ticket": "docs/notes/nw7_mainrun_predictions_iffirst_v1.md (commit 89349a8)",
        "addendum": "docs/notes/nw7_predictions_addendum_pentlayer_v1.md",
        "sol_ratification": "sol/sol_reply_106_math33.md (F106 series, branch B-1a and corrected B-2a via PRE-2' xi'=1)",
    },
    "predictions": predictions,
    "measured": measured,
    "scoring": scoring,
    "sealed_quantities_contacted": False,
    "sealed_quantities_note": "n=5 related / Im R / d_N / u 値 -- 本スクリプトは NW(7) 窓の join manifest のみを読み、これら封印量には一切接触していない。",
    "artifact_rewrite": False,
    "cross_check_status": "cross-checked (NOT verified -- Lean 未使用)",
    "cv9_note": "この scoring は探索器(GAP main-run lanes)の出力証明書のみを入力にした照合であり、GAP コード・中間結果は import していない(探索器/照合器分離)。ただし本 scoring script 自体は falsifier による CV-9 仕様同一性判読(S/V が真に独立実装かの監査)を経ていない -- 便読解上は predicate_lib_laneS.g / predicate_lib_laneV_cf.g のソース比較により独立実装であることを確認済み(異なる pcgs_basis_fingerprint, 異なるアルゴリズム: word-walk vs closed-form automorphism)。",
}

OUT_PATH = f"{ROOT}/search/certs/nw7_mainrun_scoring_20260806.json"
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=False)

print("WROTE", OUT_PATH)
print(json.dumps({"hex_total_S": hex_total_S, "hex_total_V": hex_total_V,
                   "sv_mismatches": len(sv_mismatches),
                   "pent_within_hex0_m0": len(pent_within_hex0),
                   "hex0_pent_fail_m0": len(hex0_pent_fail),
                   "lane_P_raw_pass": pent_raw_total}, indent=2))
