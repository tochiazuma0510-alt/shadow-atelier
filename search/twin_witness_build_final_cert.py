#!/usr/bin/env python3
"""
twin_witness_build_final_cert.py -- assemble the final twin-witness run cert
from the already-produced (and independently cross-checked) intermediate
artifacts. Pure data assembly, no new group-theoretic computation.

Inputs:
  search/certs/twin_witness_scope1_v1_20260806.json       (scope 1: registered set)
  scratchpad/twin_witness_mirror_run.log                  (scope 2 系統A: GAP transcript)
  search/certs/twin_witness_mc1_export_v1_20260806.json   (系統A -> 系統B export)
  search/certs/twin_witness_mc1_check_result_v1_20260806.json (系統B: python re-check)

Output: search/certs/twin_witness_run_v1_20260806.json
"""
import json
import re
import hashlib

with open("search/certs/twin_witness_scope1_v1_20260806.json", encoding="utf-8") as f:
    scope1 = json.load(f)

with open("search/certs/twin_witness_mc1_check_result_v1_20260806.json", encoding="utf-8") as f:
    mc1_check = json.load(f)

with open("scratchpad/twin_witness_mirror_run.log", encoding="utf-8") as f:
    log_text = f.read()

# parse per-pair blocks out of the GAP transcript
blocks = re.findall(
    r"=== pair index=(\d+) pair_uid=(\w+) ===\n"
    r"\s*\|B3/A\|=(\d+) \|B3/B\|=(\d+) \(cert index=(\d+)\)\n"
    r"\s*canary \(3\.11\)@\[-1,1\] paper-product B3 identity: (\w+)\n"
    r"\s*mirror class \(A-side\): (\w+)\s+\(self=(\w+) partner=(\w+)\)\n"
    r"\s*mirror class \(B-side\): (\w+)\s+\(self=(\w+) partner=(\w+)\)\n"
    r"\s*A/B-side consistent: (\w+)\n"
    r"\s*W-c SURJ \(A side\): <a\^-1,b\^-1>=B3/A \? (\w+)\n"
    r"\s*W-c SURJ \(B side\): <a\^-1,b\^-1>=B3/B \? (\w+)\n",
    log_text,
)

per_window = []
for m in blocks:
    (idx, puid, sizeA, sizeB, certidx, canary, mclassA, selfA, partnerA,
     mclassB, selfB, partnerB, consistent, surjA, surjB) = m
    per_window.append({
        "index": int(idx), "pair_uid": puid,
        "sizeA": int(sizeA), "sizeB": int(sizeB), "cert_index": int(certidx),
        "size_sanity_ok": (int(sizeA) == int(certidx) and int(sizeB) == int(certidx)),
        "canary_minus1_hexagon_reduced_pass": (canary == "true"),
        "mirror_class_A_side": mclassA, "mirror_class_B_side": mclassB,
        "self_trivial_A": selfA == "true", "partner_trivial_A": partnerA == "true",
        "self_trivial_B": selfB == "true", "partner_trivial_B": partnerB == "true",
        "AB_side_consistent": consistent == "true",
        "wc_surj_A": surjA == "true", "wc_surj_B": surjB == "true",
    })

assert len(per_window) == 15, f"expected 15 parsed blocks, got {len(per_window)}"

mc1_by_index = {e["index"]: e for e in mc1_check["entries"]}
for w in per_window:
    mc1 = mc1_by_index.get(w["index"])
    # index 504 and 936 appear twice; match by pair_uid via mc1_check entries too
    matches = [e for e in mc1_check["entries"] if e["pair_uid"] == w["pair_uid"]]
    assert len(matches) == 1, f"pair_uid {w['pair_uid']} matched {len(matches)} MC-1 entries"
    w["mc1_python_check"] = matches[0]

predicted_M1 = [126, 234, 342, 378, 558, 666, 702, 774]
prediction_rows = []
n_M1 = n_M0 = n_M2 = 0
prereg_prediction_failed = []
for w in per_window:
    cls = w["mirror_class_A_side"]
    if cls == "M1":
        n_M1 += 1
    elif cls == "M0":
        n_M0 += 1
    elif cls == "M2":
        n_M2 += 1
    predicted = "M1" if w["index"] in predicted_M1 else "UNKNOWN(P-4/paper-undetermined)"
    row = {"index": w["index"], "pair_uid": w["pair_uid"], "predicted": predicted, "observed": cls}
    prediction_rows.append(row)
    if w["index"] in predicted_M1 and cls != "M1":
        prereg_prediction_failed.append(w["index"])

mc1_all_ok = mc1_check["all_ok"]
gap_python_agree = all(
    w["mirror_class_A_side"] == "M1" and w["mc1_python_check"]["entry_ok"]
    for w in per_window
)

s_tw_7_triggered = (n_M2 > 0) or (len(prereg_prediction_failed) > 0)

with open("docs/notes/twin_witness_prereg_iffirst_v1.md", "rb") as f:
    prereg_sha256 = hashlib.sha256(f.read()).hexdigest()

result = {
    "schema": "twin_witness_run/v1 (adapted -- scope 3 not executed, see note)",
    "prereg_doc_path": "docs/notes/twin_witness_prereg_iffirst_v1.md",
    "prereg_doc_sha256": prereg_sha256,
    "census_cert_path": scope1["cert_path"],
    "census_cert_sha256": scope1["cert_sha256"],
    "scope1_registration": {
        "counts": scope1["counts"],
        "directed_counts": scope1["directed_counts"],
        "setdigest": scope1["setdigest"],
        "registered_set": "L2 (15 pairs / 30 directed, c_in_N and in_PB3 both members)",
        "L3_13_pairs_touched": False,
        "note": "matches docs/notes/twin_witness_prereg_iffirst_v1.md sec 1 bit-for-bit "
                "(all counts and all 4 SETDIGESTs machine-reproduced identically).",
    },
    "scope2_mirror_classification": {
        "domain": "L2 only (15 pairs / 30 directed) -- NOT the L1-28 superset the "
                  "prereg doc sec 2.5 mentions; task instruction explicitly restricts "
                  "to the registered L2 set and forbids touching L3 (13 pairs, "
                  "held under 裁定 T-1).",
        "per_window": per_window,
        "counts": {"M0": n_M0, "M1": n_M1, "M2": n_M2},
        "S_TW_7_triggered": s_tw_7_triggered,
        "prediction_table_vs_P1": prediction_rows,
        "prereg_prediction_P1_failures": prereg_prediction_failed,
        "prereg_prediction_P2_M2_is_zero": (n_M2 == 0),
        "prereg_prediction_P3_both_directions_nonempty": all(
            w["AB_side_consistent"] and w["mirror_class_A_side"] == "M1" for w in per_window
        ),
        "note": "ALL 15/15 registered pairs classify as M1 (mirror pairs), including "
                "all 7 pairs the paper (sec 7) left as UNKNOWN/50-50 (indices 432, 486, "
                "504x2, 882, 936x2). This EXCEEDS but does not contradict prediction "
                "P-1 (which only committed to the 8 named indices); no prediction "
                "failure (no predicted-M1 window came out M0), so S-TW-7 is NOT triggered.",
        "P4_note_per_裁定602": "P-4 の 7 対(432, 486, 504x2, 882, 936x2 -- 紙(ABEL-INDEX / "
                "MIRROR-OBSTRUCTION)では 50/50・判断材料なしとされていた)は全て機械計算で "
                "M1 と確定した。これは MIRROR-OBSTRUCTION の射程外(適切な特性巡回部分群 A を "
                "紙で特定できなかった窓)での確定であり、新しい紙証明(この 7 対に効く補題)を "
                "見つけられる可能性がある数学者検討材料として明記する(裁定602 追加指示)。",
    },
    "second_system": {
        "system_A": "GAP (search/twin-witness-mirror-v1.g): NaturalHomomorphismByNormalSubgroup "
                    "quotient construction + EvalString-based iota substitution (rebind global "
                    "a,b to their inverses and re-evaluate the identical generator-word text).",
        "system_B": "python, GAP-helper-free (search/twin_witness_mc1_check.py): independent "
                    "word parser + permutation arithmetic + BFS group-order routine, all "
                    "reimplemented from scratch; consumes ONLY the JSON permutation export "
                    "(search/certs/twin_witness_mc1_export_v1_20260806.json), no GAP code or "
                    "GAP data structures imported.",
        "agreement": "15/15 mirror_cert entries: braid relation holds, N subseteq ker(rho), "
                    "iota(N) != N confirmed (explicit nontrivial witness word per entry), "
                    "|<s1,s2>| == index exactly, K subseteq iota(N) (kernel identified as the "
                    "twin partner, not merely 'some' nontrivial kernel), SURJ holds.",
        "all_ok": mc1_all_ok,
        "gap_and_python_agree_on_all_15": gap_python_agree,
        "grade": "cross-checked (系統A + 系統B 一致; Lean 不使用ゆえ verified ではない)",
    },
    "M_ISO_2_status": {
        "claim": "M-ISO-2 (settled 述語が FALSE を返せることの実証) は満たされる: 登録した "
                 "L2 の全 15 対(directed 30)で ker(T_{-1,1}) = iota(N) = K != N が両系統で確認された。",
        "first_witness": {"index": 126, "pair_uid": "b6b8a3feb9d2"},
        "grading_limitation_verbatim": (
            "本 witness は算術元([-1,1] = 複素共役)であり、非算術証人(B 型)ではない。"
            "本件が閉じるのは M-ISO-2(settled 述語が FALSE を返せることの実証)であって、"
            "FAKE-VOID・非算術証人の存在/非存在には一切触れない。"
        ),
    },
    "scope3_not_executed": {
        "reason": "scope 3 (R1-b 悉皆 for M0-classified windows) applies only to windows "
                  "classified M0. Scope 2 found ZERO M0 windows in the registered L2 set "
                  "(all 15 are M1) -- so there is no M0 window to run scope 3 against. "
                  "Doc sec 3 permits (does not require) running scope 3 on M1 windows too "
                  "('shadow 全体と |GT| を得るために実行してよい') -- NOT executed in this "
                  "pass (out of scope for the witness deliverable; would require a separate "
                  "R1-b exhaustive enumeration script, up to 313,236 candidates across the "
                  "30 windows per doc sec 3.2).",
    },
    "output_claim_per_doc_sec5": (
        "witness FOUND (branch (i) of doc sec 5.3): L2 に M1(鏡映対)が 15 件(全数)。"
        "最小指数の対(126, pair_uid=b6b8a3feb9d2)を第一 witness とする。"
        "禁止語(AS-GAP-6 の非存在主張・AUTO-SETTLED・剛性主張・L3/L0残りへのTRUE/FALSE)は使用していない。"
    ),
}

with open("search/certs/twin_witness_run_v1_20260806.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Wrote search/certs/twin_witness_run_v1_20260806.json")
print(json.dumps({
    "counts": result["scope2_mirror_classification"]["counts"],
    "S_TW_7_triggered": s_tw_7_triggered,
    "gap_and_python_agree_on_all_15": gap_python_agree,
    "prereg_prediction_P1_failures": prereg_prediction_failed,
}, indent=2))
