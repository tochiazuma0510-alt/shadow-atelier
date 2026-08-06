#!/usr/bin/env python3
"""
cal_b4_integrated_crosscheck.py -- independent checker for
search/certs/cal_b4_integrated_v1_20260806.json.

Discipline (探索器と照合器の分離, CLAUDE.md): this script reads ONLY the
committed cert JSON. It does NOT import build_integrated_cert.py, does NOT
open the GAP logs the cert was built from, and does NOT re-run GAP. Its job
is (a) to recompute the small set of self-evident arithmetic facts the cert
claims independently in pure Python, and (b) to verify the cert's own
PASS/FAIL/status flags are internally consistent with the numbers it reports
next to them. This is cross-checking, not verification (Lean is reserved
for "verified").

Exit code 0 iff no problems found; prints every problem found (fail-closed,
no silent pass).
"""
import json
import sys

CERT_PATH = "search/certs/cal_b4_integrated_v1_20260806.json"


def main():
    with open(CERT_PATH, encoding="utf-8") as f:
        cert = json.load(f)

    problems = []

    def check(cond, msg):
        if not cond:
            problems.append(msg)

    # --- schema / provenance shape ---
    check(cert.get("schema") == "cal-b4-integrated/v1", "schema field mismatch")
    for key in ["cal_b4_log", "p1_log"]:
        src = cert.get("sources", {}).get(key)
        check(src is not None, f"sources.{key} missing")
        if src is not None:
            check(isinstance(src.get("sha256"), str) and len(src["sha256"]) == 64,
                  f"sources.{key}.sha256 missing or malformed")

    # --- C-1: internal number consistency (independent arithmetic, not re-derivation of GAP) ---
    c1 = cert["C1"]
    check(c1["idx_B4_PB4"] == c1["idx_B4_PB4_expected"] == 24, "C1: idx_B4_PB4 != 24")
    check(c1["convention_guard_bad_relators"] == 0, "C1: convention-guard reports nonzero bad relators")
    check(c1["convention_guard_relator_count"] == c1["convention_guard_relators_total"],
          "C1: convention-guard relator-count fields disagree with each other")
    check(c1["image_psi_size"] == c1["idx_PB4fp_N19"] == 216,
          "C1: |Image(psi)| and |PB4fp:N19| disagree or are not 216 (Lagrange/orbit-stabilizer sanity)")
    check(c1["pass"] == (c1["image_psi_size"] == 216 and c1["idx_PB4fp_N19"] == 216),
          "C1: 'pass' flag inconsistent with the recorded index values")

    # --- C-2 ---
    c2 = cert["C2"]
    check(c2["pass"] == (c2["N_ord"] == c2["N_ord_expected"]), "C2: pass flag inconsistent with N_ord")

    # --- C-3a/C-3b: independent arithmetic fact, 216 must divide 7776 (Lagrange), and 7776/216=36 ---
    c3a = cert["C3a"]
    c3b = cert["C3b"]
    check(c3a["pass"] == (c3a["idx_F2_NF2"] == c3a["idx_F2_NF2_expected"]), "C3a: pass flag inconsistent")
    check(c3b["pass"] == (c3b["commutator_order"] == c3b["commutator_order_expected"]), "C3b: pass flag inconsistent")
    check(c3a["idx_F2_NF2"] % c3b["commutator_order"] == 0,
          "C3a/C3b: commutator_order does not divide idx_F2_NF2 (violates Lagrange -- structurally impossible "
          "for a subgroup order, independent arithmetic fact)")
    check(c3a["idx_F2_NF2"] // c3b["commutator_order"] == 36,
          "C3a/C3b: idx_F2_NF2 / commutator_order != 36 (expected quotient order [P19:[P19,P19]])")

    # --- C-4: both methods must agree with each other AND with 216 ---
    c4 = cert["C4"]
    prim = c4["primary_method"]["pentagon_pass_count"]
    cross = c4["cross_method"]["pentagon_pass_count"]
    check(prim == cross, f"C4: primary_method ({prim}) and cross_method ({cross}) pentagon counts disagree")
    check(prim == 216, "C4: primary_method pentagon count != 216")
    check(c4["primary_method"]["pass"] == (prim == 216), "C4: primary_method pass flag inconsistent")
    check(c4["cross_method"]["pass"] == (cross == 216), "C4: cross_method pass flag inconsistent")

    # --- C-5: pair count must be exactly 2x distinct_f (per-f distribution recorded as [[2,36]]) ---
    c5 = cert["C5"]
    check(c5["pair_count"] == 72 and c5["distinct_f"] == 36, "C5: pair_count/distinct_f not at expected values")
    check(c5["pair_count"] == 2 * c5["distinct_f"],
          "C5: pair_count != 2 * distinct_f -- inconsistent with the recorded per-f distribution "
          "[[2,36]] (every f has exactly 2 good m)")
    check("[ 2, 36 ]" in c5["per_f_good_m_distribution_raw"] or "[2, 36]" in c5["per_f_good_m_distribution_raw"]
          or "[[2, 36]]" in c5["per_f_good_m_distribution_raw"].replace(" ", "")
          or "[[2,36]]" in c5["per_f_good_m_distribution_raw"].replace(" ", ""),
          "C5: recorded per_f_good_m_distribution_raw does not literally contain the (2,36) pair "
          "the pair_count/distinct_f arithmetic above assumes")
    check(c5["both_units_pass"] == (c5["pair_count"] == 72 and c5["distinct_f"] == 36),
          "C5: both_units_pass flag inconsistent with recorded pair_count/distinct_f")

    # --- C-6 first half: must equal C5's pair_count (same quantity, cntC5) ---
    c6a = cert["C6_first_half"]
    check(c6a["value"] == c5["pair_count"],
          "C6_first_half: value does not equal C5.pair_count (both are cntC5 in the source script -- "
          "the cert's own note claims this identity)")
    check(c6a["pass"] == (c6a["value"] == c6a["expected"]), "C6_first_half: pass flag inconsistent")

    # --- C-6b: must NOT claim a computed numeric result while status=PENDING ---
    c6b = cert["C6b_second_half"]
    check(c6b["status"] == "PENDING", "C6b_second_half: status is not PENDING -- unexpected, re-audit")
    check("value" not in c6b, "C6b_second_half: cert carries a 'value' key while status=PENDING -- "
                               "this would mean a number was recorded without a supporting run (forbidden)")
    check(c6b.get("expected_if_computed") == 12, "C6b_second_half: expected_if_computed != 12 (2008 Table 1)")

    # --- P1: literal 7^41 check, and pass-flag consistency ---
    p1 = cert["P1"]
    seven_41 = 7 ** 41
    check(int(p1["R_size_expected_decimal"]) == seven_41,
          f"P1: R_size_expected_decimal != 7**41 computed independently ({seven_41})")
    check(int(p1["R_size_decimal"]) == int(p1["R_size_expected_decimal"]),
          "P1: R_size_decimal != R_size_expected_decimal despite B4_EXQ1_pass")
    check(p1["B4_EXQ1_pass"] == (int(p1["R_size_decimal"]) == seven_41),
          "P1: B4_EXQ1_pass flag inconsistent with the independently-recomputed 7**41 comparison")
    check(p1["B4_EXQ2_status"] == "CRASHED_OOM_INCOMPLETE",
          "P1: B4_EXQ2_status changed from the expected CRASHED_OOM_INCOMPLETE -- re-audit narrative")
    check(p1["reached_P1_PASS_marker"] is False,
          "P1: reached_P1_PASS_marker is not False, but B4_EXQ2 is recorded as crashed/incomplete -- "
          "inconsistent (a completed run should have hit the marker)")

    # --- C-8: must not claim PASS or 'waiver in effect' anywhere ---
    c8 = cert["C8"]
    check(c8["status"] == "SKIP", "C8: status is not SKIP -- if this changed, re-audit against the waiver prereg")
    check("PASS" not in c8["status"], "C8: status field contains the string PASS -- forbidden for a SKIP job")
    check(c8["waiver_status"].startswith("candidate"),
          "C8: waiver_status does not start with 'candidate' -- possible premature adoption of the waiver "
          "without 司令塔/Sol ruling (see docs/notes/cal_b4_c8_waiver_prereg_v1.md SS4)")

    # --- overall: recompute all_computed_checks_pass independently from the component flags ---
    overall = cert["overall"]
    recomputed_all_pass = all([
        c1["pass"], c2["pass"], c3a["pass"], c3b["pass"],
        c4["primary_method"]["pass"], c4["cross_method"]["pass"],
        c5["both_units_pass"], c6a["pass"], p1["B4_EXQ1_pass"],
    ])
    check(overall["all_computed_checks_pass"] == recomputed_all_pass,
          f"overall.all_computed_checks_pass ({overall['all_computed_checks_pass']}) does not match "
          f"independently recomputed conjunction of component pass flags ({recomputed_all_pass})")
    check(set(overall["pending_items"]) or True, "overall.pending_items sanity (non-empty expected)")
    check(len(overall["pending_items"]) >= 3,
          "overall.pending_items has fewer than the 3 known-pending items (C6b, P1.B4_EXQ2, C8) -- "
          "check for silent completion claims")

    result = {
        "schema": "cal-b4-integrated-crosscheck/v1",
        "cert_checked": CERT_PATH,
        "problems": problems,
        "MATCH": len(problems) == 0,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    with open("search/certs/cal_b4_integrated_crosscheck_v1_20260806.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
