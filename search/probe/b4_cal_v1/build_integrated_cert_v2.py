#!/usr/bin/env python3
"""
build_integrated_cert_v2.py -- CAL-B4 integrated cert generator, v2.

Supersedes build_integrated_cert.py (v1, search/certs/cal_b4_integrated_v1_20260806.json)
for a fresh run (GHA run 31084038955, dispatched after 裁定674's driver additions:
C-6b dual-unit fix, C-6c mandatory SURJ check, C-6d cyclotomic bisection, C-6e
recommended composition-law/D6 isomorphism check). v1's script and cert are left
untouched (historical, reproducible from run 31078897925/31067255800).

新規則(裁定674「単位宣言規約の初適用」): every numeric field in this cert carries
an explicit sibling "*_unit" string describing what is being counted (index /
f-count / pair-count / group-order / etc.) -- this is the discipline that would
have caught the C-6b f-count-vs-pair-count mismatch (裁定674) before it needed a
コーディネーター-level correction.

Machine-generates search/certs/cal_b4_integrated_v2_20260806.json by parsing
(regex, not hand-transcription) the committed GAP/GHA run logs:
  - search/probe/b4_cal_v1/logs/cal_b4_n19_run31084038955.log
      (C-1, C-2, C-3a, C-3b, C-4 (both methods), C-5, C-6 前半, C-6b(両単位)/
      C-6c/C-6d/C-6e; GHA run 31084038955, collected by 司令塔 per 裁定675.
      This log postdates the 裁定674 driver additions -- ALL_DONE reached,
      no crash.)
  - search/probe/b4_cal_v1/logs/p1_build_R_run31067255800.log
      (unchanged from v1 -- P1/B4-EXQ-1, |R|=7^41; B4-EXQ-2 remains
      CRASHED_OOM_INCOMPLETE, no new P1 run in this pass.)

C-8's status is unchanged from v1 in substance, but the waiver ruling has moved:
裁定674 explicitly REJECTED the weak waiver gate proposed in
docs/notes/cal_b4_c8_waiver_prereg_v1.md ("弱い代替 gate は採用しない"). C-8
remains plain SKIP + recorded reason; adoption question is deferred to Sol via
便113 (not decided by this generator, not decided locally).

Run: python search/probe/b4_cal_v1/build_integrated_cert_v2.py
"""
import hashlib
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CAL_LOG = REPO_ROOT / "search/probe/b4_cal_v1/logs/cal_b4_n19_run31084038955.log"
P1_LOG = REPO_ROOT / "search/probe/b4_cal_v1/logs/p1_build_R_run31067255800.log"
OUT_CERT = REPO_ROOT / "search/certs/cal_b4_integrated_v2_20260806.json"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def must_search(pattern: str, text: str, label: str):
    m = re.search(pattern, text)
    if m is None:
        raise RuntimeError(f"cert generation FAILED: pattern for [{label}] not found in log -- "
                            f"pattern={pattern!r}. Refusing to hand-fill a value; report and fix the regex "
                            f"or the log instead.")
    return m


def main():
    cal_text = CAL_LOG.read_text(encoding="utf-8")
    p1_text = P1_LOG.read_text(encoding="utf-8")

    if "ALL_DONE" not in cal_text:
        raise RuntimeError("cert generation FAILED: cal_b4_n19_run31084038955.log does not contain "
                            "ALL_DONE -- run did not complete cleanly, refusing to build a cert from a "
                            "partial log.")

    # --- C-1 ---
    m = must_search(r"\[B4:PB4\] = (\d+) \(expect 24\)", cal_text, "B4:PB4 index")
    idx_b4_pb4 = int(m.group(1))
    m = must_search(r"Convention-guard: \|RelatorsOfFpGroup\(PB4fp\)\| = (\d+)", cal_text, "convention-guard relator count")
    n_relators = int(m.group(1))
    m = must_search(r"Convention-guard: relators failing to map to identity = (\d+) / (\d+)", cal_text, "convention-guard failures")
    n_bad_rel, n_rel_total = int(m.group(1)), int(m.group(2))
    m = must_search(r"\|Image\(psi\)\| = (\d+) \(expect 216", cal_text, "|Image(psi)|")
    image_psi_size = int(m.group(1))
    m = must_search(r"\|PB4fp : N19\| = (\d+) \(expect 216", cal_text, "|PB4fp:N19|")
    idx_pb4fp_n19 = int(m.group(1))
    c1_pass = "C-1 PASS: |PB4:N19| = 216" in cal_text

    # --- C-3a ---
    m = must_search(r"\|P19\| = \|F2:N_F2\| = (\d+)\s+\(expect 7776, C-3a\)", cal_text, "|F2:N_F2|")
    idx_f2_nf2 = int(m.group(1))
    c3a_pass = "C-3a PASS: |F2:N_F2| = 7776" in cal_text

    # --- C-2 ---
    m = must_search(r"C-2: N_ord = lcm\(ord\(x\),ord\(y\)\) = (\d+) \(expect 6\)", cal_text, "N_ord")
    n_ord = int(m.group(1))
    c2_pass = "C-2 PASS: N_ord = 6" in cal_text

    # --- C-3b ---
    m = must_search(r"C-3b: \|\[F2/N_F2,F2/N_F2\]\| = (\d+) \(expect 216\)", cal_text, "commutator order")
    commutator_order = int(m.group(1))
    c3b_pass = "C-3b PASS: commutator subgroup order = 216" in cal_text

    # --- C-4 (primary + c5.g cross-method) ---
    m = must_search(r"pentagon-pass count = (\d+)\s+\(expect 216, C-4\)\s+elapsed_ms=(\d+)", cal_text, "C-4 primary count")
    c4_primary_count, c4_elapsed_ms = int(m.group(1)), int(m.group(2))
    c4_pass = "C-4 PASS: pentagon count = 216" in cal_text
    m = must_search(r"pentagon-pass set closed under \*\? (true|false)", cal_text, "pentagon-pass closure diagnostic")
    c4_pentagon_pass_set_closed_under_mult = (m.group(1) == "true")
    m = must_search(r"C-4 \(c5\.g method, cross-check\) pentagon solutions = (\d+) \(expect 216\)", cal_text, "C-4 cross-method count")
    c4_crossmethod_count = int(m.group(1))

    # --- C-5 ---
    m = must_search(r"C-5 \(full hexagon\) pair count \(m,f\) = (\d+)\s+\(target: pair=72\)\s+elapsed_ms=(\d+)", cal_text, "C-5 pair count")
    c5_pair_count, c5_elapsed_ms = int(m.group(1)), int(m.group(2))
    m = must_search(r"C-5 \(full hexagon\) distinct f = (\d+)\s+\(target: distinct-f=36\)", cal_text, "C-5 distinct-f")
    c5_distinct_f = int(m.group(1))
    c5_both_units_pass = "C-5 PASS: BOTH units match (pair=72 AND distinct-f=36)" in cal_text
    m = must_search(r"per-f good-m distribution \(value,count pairs\) = (\[.*\])", cal_text, "per-f m distribution")
    per_f_m_distribution_raw = m.group(1)

    # --- C-6 前半 ---
    m = must_search(r"C-6 \(前半\): \|GT\(N19\)\| \(charming pair count\) = (\d+) \(expect 72, Table 1\)", cal_text, "C-6 first-half value")
    c6_first_half_value = int(m.group(1))
    c6_first_half_pass = (c6_first_half_value == 72)

    # --- C-6b (dual-unit, 裁定674) ---
    m = must_search(r"C-6b: \|DerivedSubgroup\(Gc5\)\| = (\d+) \(expect 216\)", cal_text, "C-6b DerivedSubgroup order")
    c6b_derived_order = int(m.group(1))
    m = must_search(r"C-6b: \|GT-heart\(N19\)\| \[f unit\] = (\d+) \(expect 6\)", cal_text, "C-6b f-unit count")
    c6b_f_count = int(m.group(1))
    m = must_search(r"C-6b: \|GT-heart\(N19\)\| \[pair unit\] = (\d+) \(expect 12, 2008 Table 1\)", cal_text, "C-6b pair-unit count")
    c6b_pair_count = int(m.group(1))
    c6b_pass = "C-6b PASS (dual-unit): f-count=6 AND pair-count=12" in cal_text

    # --- C-6c (必須, SURJ) ---
    m = must_search(r"C-6c: SURJ \(2\.61\) 検査 = (\d+) / (\d+) pass", cal_text, "C-6c SURJ tally")
    c6c_pass_count, c6c_total_count = int(m.group(1)), int(m.group(2))
    c6c_pass = "C-6c PASS: 全 12 heart shadows が charming 条件 (2) を満たす" in cal_text

    # --- C-6d (円分指標二等分) ---
    m = must_search(r"C-6d: 円分指標二等分 = (\d+) / (\d+) heart-f で成立", cal_text, "C-6d bisection tally")
    c6d_pass_count, c6d_total_count = int(m.group(1)), int(m.group(2))
    c6d_pass = "C-6d PASS: 全 6 heart-f で円分指標二等分を確認" in cal_text

    # --- C-6e (推奨, 合成則/D6同型) ---
    m = must_search(r"C-6e: 合成閉包の失敗数 = (\d+) / (\d+) 積", cal_text, "C-6e closure tally")
    c6e_closure_fail, c6e_products_total = int(m.group(1)), int(m.group(2))
    m = must_search(r"C-6e: GroupByMultiplicationTable の位数 = (\d+) \(expect 12\)", cal_text, "C-6e reconstructed group order")
    c6e_group_order = int(m.group(1))
    m = must_search(r"C-6e: GT-heart\(N19\) =~= D6\(位数12・r\^6=s\^2=\(rs\)\^2=1\)\? (true|false)", cal_text, "C-6e D6 isomorphism verdict")
    c6e_isD6 = (m.group(1) == "true")
    c6e_pass = "C-6e PASS: GT-heart(N19) の乗積表は 12 元で閉じ、D6 と同型" in cal_text

    # --- P1 (unchanged from v1 -- same log, same run) ---
    m = must_search(r"\|R\| = (\d+)\s+\(B4-EXQ-1 predicts 7\^41 = (\d+)\)", p1_text, "P1 |R|")
    p1_r_size, p1_r_expected = int(m.group(1)), int(m.group(2))
    m = must_search(r"B4-EXQ-1: (true|false)", p1_text, "B4-EXQ-1 verdict")
    p1_b4exq1_pass = (m.group(1) == "true")
    m = must_search(r"\|Z\(R\)\| = (\d+)", p1_text, "|Z(R)|")
    p1_zR_size = int(m.group(1))
    p1_reached_p1_pass_marker = "P1_PASS" in p1_text
    p1_reached_all_done = "ALL_DONE" in p1_text

    cert = {
        "schema": "cal-b4-integrated/v2",
        "supersedes": "search/certs/cal_b4_integrated_v1_20260806.json (v1 left untouched, historical)",
        "unit_declaration_convention": "初適用(裁定674): every numeric field below has a sibling "
                                        "'*_unit' string naming what is counted. This convention exists "
                                        "because C-6b's first pass (run 31080320082) reported '6' and "
                                        "was scored FAIL against an expected '12' that was actually a "
                                        "DIFFERENT unit (pair-count, not f-count) -- see C6b below.",
        "generated_by": {
            "tool": "search/probe/b4_cal_v1/build_integrated_cert_v2.py",
            "method": "regex extraction from committed GAP/GHA run logs -- no hand-transcribed numeric values",
        },
        "sources": {
            "cal_b4_log": {
                "path": "search/probe/b4_cal_v1/logs/cal_b4_n19_run31084038955.log",
                "gha_run_id": "31084038955",
                "sha256": sha256_of(CAL_LOG),
                "note": "Collected by 司令塔 (裁定675) after the 裁定674 driver additions (C-6b dual-unit "
                        "fix, C-6c/C-6d mandatory, C-6e recommended) were pushed+dispatched. Reaches "
                        "ALL_DONE cleanly, no crash.",
            },
            "p1_log": {
                "path": "search/probe/b4_cal_v1/logs/p1_build_R_run31067255800.log",
                "gha_run_id": "31067255800",
                "sha256": sha256_of(P1_LOG),
                "note": "Unchanged from v1 -- no new P1 run in this pass. Run crashed on a GHA memory "
                        "limit (-o 6g) partway through B4-EXQ-2's DirectFactorsOfGroup(R) call, AFTER "
                        "already printing and confirming B4-EXQ-1.",
            },
        },
        "C1": {
            "idx_B4_PB4": idx_b4_pb4, "idx_B4_PB4_unit": "subgroup index [B4:PB4]", "idx_B4_PB4_expected": 24,
            "convention_guard_relator_count": n_relators, "convention_guard_relator_count_unit": "relator count in RelatorsOfFpGroup(PB4fp)",
            "convention_guard_bad_relators": n_bad_rel, "convention_guard_bad_relators_unit": "relator count failing to map to identity under psiImages",
            "convention_guard_relators_total": n_rel_total,
            "image_psi_size": image_psi_size, "image_psi_size_unit": "group order |Image(psi)| in S9", "image_psi_size_expected": 216,
            "idx_PB4fp_N19": idx_pb4fp_n19, "idx_PB4fp_N19_unit": "subgroup index [PB4fp:N19]", "idx_PB4fp_N19_expected": 216,
            "pass": c1_pass,
        },
        "C2": {"N_ord": n_ord, "N_ord_unit": "lcm(ord(x-bar),ord(y-bar)) in P19 -- cyclotomic character modulus", "N_ord_expected": 6, "pass": c2_pass},
        "C3a": {"idx_F2_NF2": idx_f2_nf2, "idx_F2_NF2_unit": "subgroup index [F2:N_F2] = |P19|", "idx_F2_NF2_expected": 7776, "pass": c3a_pass},
        "C3b": {"commutator_order": commutator_order, "commutator_order_unit": "group order |[P19,P19]| (DerivedSubgroup)", "commutator_order_expected": 216, "pass": c3b_pass},
        "C4": {
            "primary_method": {
                "construction": "diagonal-Sym(45), 5 pentagon cofaces, full 7776-element enumeration",
                "pentagon_pass_count": c4_primary_count,
                "pentagon_pass_count_unit": "f-count over the full 7776-element universe P19 (NOT pair-count, NOT restricted to [P19,P19])",
                "pentagon_pass_count_expected": 216,
                "elapsed_ms": c4_elapsed_ms,
                "pentagon_pass_set_closed_under_mult_diagnostic_only": c4_pentagon_pass_set_closed_under_mult,
                "pass": c4_pass,
            },
            "cross_method": {
                "construction": "c5.g-style independent reimplementation (separate variable names/functions, Av/Bv/Cv + compC5)",
                "pentagon_pass_count": c4_crossmethod_count,
                "pentagon_pass_count_unit": "f-count over the 7776-element universe Gc5 (same unit as primary_method, independently re-derived)",
                "pentagon_pass_count_expected": 216,
                "pass": (c4_crossmethod_count == 216),
            },
            "note": "Both methods run in the SAME GAP process / SAME session's implementation -- this "
                    "is an in-repo double-implementation agreement, NOT an independent third-party "
                    "cross-check. See docs/notes/cal_b4_c8_waiver_prereg_v1.md SS1.2 for the explicit "
                    "distinction (C-8/PackageGT would be the genuine third-party check).",
        },
        "C5": {
            "pair_count": c5_pair_count, "pair_count_unit": "shadow (m,f) pair-count over the 216 pentagon-passing f's x 4 candidate m's", "pair_count_expected": 72,
            "distinct_f": c5_distinct_f, "distinct_f_unit": "f-count (distinct f among the 216 pentagon-passing elements that hexagon-pass for AT LEAST ONE m)", "distinct_f_expected": 36,
            "elapsed_ms": c5_elapsed_ms,
            "per_f_good_m_distribution_raw": per_f_m_distribution_raw,
            "per_f_good_m_distribution_unit": "(good-m-count, number-of-f-with-that-count) pairs -- uniform [[2,36]] means every one of the 36 distinct f's has exactly 2 good m's",
            "both_units_pass": c5_both_units_pass,
        },
        "C6_first_half": {
            "value": c6_first_half_value, "value_unit": "shadow (m,f) pair-count, identical quantity to C5.pair_count (cntC5)", "expected": 72,
            "note": "|GT(N19)| charming pair count",
            "pass": c6_first_half_pass,
        },
        "C6b_second_half": {
            "status": "COMPUTED",
            "note": "★ 単位訂正(裁定674): run 31080320082 の初回実測(f_count=6)は FAIL と誤判定された -- "
                    "比較先の '12'(2008 Table 1)が実は pair-count 単位だったため。両単位を独立に検査する "
                    "よう driver を修正(裁定674)し、run 31084038955 で両方 PASS を確認した。",
            "derived_subgroup_order": c6b_derived_order,
            "derived_subgroup_order_unit": "group order |DerivedSubgroup(Gc5)|",
            "derived_subgroup_order_expected": 216,
            "f_count": c6b_f_count,
            "f_count_unit": "f-count -- distinct f (of the 36 hexagon-passing f's) whose Gc5-image lies in DerivedSubgroup(Gc5)",
            "f_count_expected": 6,
            "pair_count": c6b_pair_count,
            "pair_count_unit": "shadow (m,f) pair-count -- hexpassC5 pairs whose f-index is one of the f_count=6 (2008 Table 1's GT-heart(N19)=12)",
            "pair_count_expected": 12,
            "pass": c6b_pass,
        },
        "C6c": {
            "status": "COMPUTED",
            "note": "必須(裁定674)。charming 条件 (2)(2.61): T^F2_{m,f} = T^PB3_{m,f}|_F2 が F2 -> F2/N_F2 "
                    "全射であることを、C-6b の 12 個の heart shadow (pair-count 単位) すべてで直接検査。",
            "pass_count": c6c_pass_count,
            "pass_count_unit": "shadow-count (of the 12 heart pair-count shadows) satisfying Group(gX^(2m+1), F^-1 gY^(2m+1) F) = Gc5",
            "total_count": c6c_total_count,
            "total_count_unit": "shadow-count (of the 12 heart pair-count shadows) attempted",
            "total_count_expected": 12,
            "pass": c6c_pass,
        },
        "C6d": {
            "status": "COMPUTED",
            "note": "円分指標二等分(裁定674)。各 heart-f(f_count=6 単位)の good-m 2 個が {0,3} から 1 個・"
                    "{2,5} から 1 個であることを実測(仮定せず悉皆)。",
            "pass_count": c6d_pass_count,
            "pass_count_unit": "f-count (of the 6 heart-f's) whose good-m pair bisects {0,3}/{2,5}",
            "total_count": c6d_total_count,
            "total_count_unit": "f-count (of the 6 heart-f's) attempted",
            "total_count_expected": 6,
            "pass": c6d_pass,
        },
        "C6e": {
            "status": "COMPUTED (推奨, not part of the required P0 gate)",
            "note": "合成則 (2.52)/(2.55) を12個の heart shadow(pair-count単位)に適用し乗積表を構築、"
                    "閉じれば GroupByMultiplicationTable で群を再構成し DihedralGroup(12) と IdGroup で比較。",
            "closure_fail_count": c6e_closure_fail,
            "closure_fail_count_unit": "ordered-product-count failing to land back in the 12-element heart set",
            "products_total": c6e_products_total,
            "products_total_unit": "ordered-product-count attempted (12 x 12 multiplication-table entries)",
            "products_total_expected": 144,
            "reconstructed_group_order": c6e_group_order,
            "reconstructed_group_order_unit": "group order |GroupByMultiplicationTable(mulTable)|",
            "reconstructed_group_order_expected": 12,
            "isomorphic_to_D6": c6e_isD6,
            "isomorphic_to_D6_note": "D6 = DihedralGroup(12) in GAP convention (order-12 dihedral group, r^6=s^2=(rs)^2=1)",
            "pass": c6e_pass,
        },
        "P1": {
            "gha_run_id": "31067255800",
            "R_size_decimal": str(p1_r_size),
            "R_size_decimal_unit": "group order |R| where R = PB4fp / V(PB4fp)",
            "R_size_expected_decimal": str(p1_r_expected),
            "R_size_expected_formula": "7^41",
            "B4_EXQ1_pass": p1_b4exq1_pass,
            "Z_R_size": p1_zR_size,
            "Z_R_size_unit": "group order |Z(R)|",
            "B4_EXQ2_status": "CRASHED_OOM_INCOMPLETE",
            "B4_EXQ2_note": "|Z(R)| was computed and printed (3909821048582988049), but the subsequent "
                            "DirectFactorsOfGroup(R) call hit GHA's -o 6g memory limit "
                            "('Error, reached the pre-set memory limit'). The script never reached its "
                            "P1_PASS/ALL_DONE markers because of this downstream OOM in the B4-EXQ-2 "
                            "block -- this is NOT a P1_FAIL of B4-EXQ-1 (which was already printed and "
                            "confirmed true before the crash). B4-EXQ-2 (R = C7 x Q direct-factor "
                            "confirmation) remains UNCONFIRMED, not FAIL. No new P1 run in this pass "
                            "(v2 cert reuses the same v1 P1 log/values).",
            "reached_P1_PASS_marker": p1_reached_p1_pass_marker,
            "reached_ALL_DONE_marker": p1_reached_all_done,
            "run_gap_exit_code": 1,
            "run_gap_exit_note": "nonzero because of the B4-EXQ-2 OOM crash, not because B4-EXQ-1 failed",
        },
        "C8": {
            "status": "SKIP",
            "reason": "Genuine environment blocker on BOTH available environments: local Windows/"
                      "Git-Bash import fails because search/thirdparty/PackageGT/Aux.py collides with "
                      "the Windows-reserved device name AUX; GHA ubuntu-latest's checkout does not "
                      "include search/thirdparty/ (gitignored by design, provenance/LEDGER.md "
                      "2026-07-26 copyright/future-public-release decision). SKIP is not PASS.",
            "workflow_job": ".github/workflows/b4-cal.yml c8_packagegt (reports clean SKIP when "
                             "search/thirdparty/PackageGT is absent)",
            "waiver_prereg": "docs/notes/cal_b4_c8_waiver_prereg_v1.md",
            "waiver_ruling": "裁定674(2026-08-06): 弱い代替 gate は採用しない -- C-8 は SKIP+記録のまま。"
                              "採否(waiver prereg §1.2の弱い代替根拠を暫定 gate として認めるか)は "
                              "便113で Sol に諮る。この cert は waiver を発効済みとして扱わない。",
        },
        "overall": {
            "computed_checks": ["C1", "C2", "C3a", "C3b", "C4.primary_method", "C4.cross_method",
                                 "C5", "C6_first_half", "C6b_second_half", "C6c", "C6d", "C6e",
                                 "P1.B4_EXQ1"],
            "all_required_checks_pass": all([
                c1_pass, c2_pass, c3a_pass, c3b_pass, c4_pass, (c4_crossmethod_count == 216),
                c5_both_units_pass, c6_first_half_pass, c6b_pass, c6c_pass, c6d_pass, p1_b4exq1_pass,
            ]),
            "all_required_checks_pass_note": "C6e is 推奨 (recommended), not required -- excluded from "
                                              "this flag by design (裁定674). See all_checks_including_recommended_pass.",
            "all_checks_including_recommended_pass": all([
                c1_pass, c2_pass, c3a_pass, c3b_pass, c4_pass, (c4_crossmethod_count == 216),
                c5_both_units_pass, c6_first_half_pass, c6b_pass, c6c_pass, c6d_pass, c6e_pass, p1_b4exq1_pass,
            ]),
            "pending_items": ["P1.B4_EXQ2 (R = C7 x Q direct-factor split -- OOM before confirmation, no new run this pass)",
                               "C8 (environment blocker, waiver adoption question deferred to Sol via 便113, 裁定674)"],
            "note": "'all_required_checks_pass' covers C-1 through C-6d + P1.B4-EXQ-1 (excludes the "
                    "recommended-only C-6e and the environment-blocked C-8). It does NOT imply CAL-B4/P0 "
                    "as a whole (which per sol_reply_112_math38.md SS197 requires C-1..C-6/C-8) is "
                    "complete -- see pending_items.",
        },
    }

    OUT_CERT.parent.mkdir(parents=True, exist_ok=True)
    OUT_CERT.write_text(json.dumps(cert, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_CERT}")
    print(json.dumps(cert["overall"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
