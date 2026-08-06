#!/usr/bin/env python3
"""
build_integrated_cert.py -- CAL-B4 integrated cert generator.

Machine-generates search/certs/cal_b4_integrated_v1_20260806.json by parsing
(regex, not hand-transcription) the committed GAP run logs:
  - search/probe/b4_cal_v1/logs/cal_b4_n19_run31078897925.log
      (C-1, C-2, C-3a, C-3b, C-4 (both methods), C-5, C-6 前半; GHA run
      31078897925, cal_b4_n19_pentagon.g BEFORE the C-6b addition made in
      this pass -- so C-6b is NOT in this log and is recorded as PENDING,
      not fabricated).
  - search/probe/b4_cal_v1/logs/p1_build_R_run31067255800.log
      (P1 / B4-EXQ-1, |R|=7^41; GHA run 31067255800. Saved from `gh run view
      31067255800 --log` output, trimmed to the p1_build_R step's raw GAP
      stdout -- see the file's own git history / this script for extraction
      method).

C-8's status is NOT parsed from any run log (there is none it could pass --
the job SKIPs cleanly on both local Windows (AUX collision) and GHA
ubuntu-latest (search/thirdparty/ is gitignored)). Its entry is populated
from the documented reasons in c8_packagegt_crosscheck.py's own docstring
and .github/workflows/b4-cal.yml's c8_packagegt job comments, plus a
pointer to the waiver prereg (docs/notes/cal_b4_c8_waiver_prereg_v1.md,
NOT yet ruled on -- candidate status only, this generator does not treat
the waiver as in effect).

Run: python search/probe/b4_cal_v1/build_integrated_cert.py
"""
import hashlib
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CAL_LOG = REPO_ROOT / "search/probe/b4_cal_v1/logs/cal_b4_n19_run31078897925.log"
P1_LOG = REPO_ROOT / "search/probe/b4_cal_v1/logs/p1_build_R_run31067255800.log"
OUT_CERT = REPO_ROOT / "search/certs/cal_b4_integrated_v1_20260806.json"


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

    # --- C-6b (NOT present in this log -- explicit PENDING, not fabricated) ---
    c6b_present = "C-6b PASS" in cal_text or "C-6b FAIL" in cal_text
    if c6b_present:
        raise RuntimeError("cert generation FAILED: cal_b4_n19_run31078897925.log unexpectedly "
                            "contains a C-6b marker -- this log predates the C-6b code addition. "
                            "Investigate before trusting this parse (wrong log file selected?).")

    # --- P1 ---
    m = must_search(r"\|R\| = (\d+)\s+\(B4-EXQ-1 predicts 7\^41 = (\d+)\)", p1_text, "P1 |R|")
    p1_r_size, p1_r_expected = int(m.group(1)), int(m.group(2))
    m = must_search(r"B4-EXQ-1: (true|false)", p1_text, "B4-EXQ-1 verdict")
    p1_b4exq1_pass = (m.group(1) == "true")
    m = must_search(r"\|Z\(R\)\| = (\d+)", p1_text, "|Z(R)|")
    p1_zR_size = int(m.group(1))
    p1_oom_crash = "Error, reached the pre-set memory limit" in p1_text
    p1_reached_p1_pass_marker = "P1_PASS" in p1_text
    p1_reached_all_done = "ALL_DONE" in p1_text

    cert = {
        "schema": "cal-b4-integrated/v1",
        "generated_by": {
            "tool": "search/probe/b4_cal_v1/build_integrated_cert.py",
            "method": "regex extraction from committed GAP/GHA run logs -- no hand-transcribed numeric values",
        },
        "sources": {
            "cal_b4_log": {
                "path": "search/probe/b4_cal_v1/logs/cal_b4_n19_run31078897925.log",
                "gha_run_id": "31078897925",
                "sha256": sha256_of(CAL_LOG),
                "note": "predates the C-6b code addition made in this pass (2026-08-06); does NOT "
                        "contain a C-6b result. See C6b_second_half.status below.",
            },
            "p1_log": {
                "path": "search/probe/b4_cal_v1/logs/p1_build_R_run31067255800.log",
                "gha_run_id": "31067255800",
                "sha256": sha256_of(P1_LOG),
                "note": "extracted from `gh run view 31067255800 --log`, p1_build_R step, trimmed to "
                        "the raw GAP stdout lines (shell echo/group lines stripped). Run crashed on a "
                        "GHA memory limit (-o 6g) partway through B4-EXQ-2's DirectFactorsOfGroup(R) "
                        "call, AFTER already printing and confirming B4-EXQ-1.",
            },
        },
        "C1": {
            "idx_B4_PB4": idx_b4_pb4, "idx_B4_PB4_expected": 24,
            "convention_guard_relator_count": n_relators,
            "convention_guard_bad_relators": n_bad_rel, "convention_guard_relators_total": n_rel_total,
            "image_psi_size": image_psi_size, "image_psi_size_expected": 216,
            "idx_PB4fp_N19": idx_pb4fp_n19, "idx_PB4fp_N19_expected": 216,
            "pass": c1_pass,
        },
        "C2": {"N_ord": n_ord, "N_ord_expected": 6, "pass": c2_pass},
        "C3a": {"idx_F2_NF2": idx_f2_nf2, "idx_F2_NF2_expected": 7776, "pass": c3a_pass},
        "C3b": {"commutator_order": commutator_order, "commutator_order_expected": 216, "pass": c3b_pass},
        "C4": {
            "primary_method": {
                "construction": "diagonal-Sym(45), 5 pentagon cofaces, full 7776-element enumeration",
                "pentagon_pass_count": c4_primary_count, "pentagon_pass_count_expected": 216,
                "elapsed_ms": c4_elapsed_ms,
                "pentagon_pass_set_closed_under_mult_diagnostic_only": c4_pentagon_pass_set_closed_under_mult,
                "pass": c4_pass,
            },
            "cross_method": {
                "construction": "c5.g-style independent reimplementation (separate variable names/functions, Av/Bv/Cv + compC5)",
                "pentagon_pass_count": c4_crossmethod_count, "pentagon_pass_count_expected": 216,
                "pass": (c4_crossmethod_count == 216),
            },
            "note": "Both methods run in the SAME GAP process / SAME session's implementation -- this "
                    "is an in-repo double-implementation agreement, NOT an independent third-party "
                    "cross-check. See docs/notes/cal_b4_c8_waiver_prereg_v1.md SS1.2 for the explicit "
                    "distinction (C-8/PackageGT would be the genuine third-party check).",
        },
        "C5": {
            "pair_count": c5_pair_count, "pair_count_expected": 72,
            "distinct_f": c5_distinct_f, "distinct_f_expected": 36,
            "elapsed_ms": c5_elapsed_ms,
            "per_f_good_m_distribution_raw": per_f_m_distribution_raw,
            "both_units_pass": c5_both_units_pass,
        },
        "C6_first_half": {
            "value": c6_first_half_value, "expected": 72,
            "note": "|GT(N19)| charming pair count, identical quantity to C5's pair_count (cntC5)",
            "pass": c6_first_half_pass,
        },
        "C6b_second_half": {
            "status": "PENDING",
            "reason": "C-6b (数学者#2 の 1 行レシピ: distinct hexagon-passing f のうち DerivedSubgroup(Gc5) "
                      "(位数216) に属する数を数える) was added to "
                      "search/probe/b4_cal_v1/cal_b4_n19_pentagon.g in this implementation pass "
                      "(2026-08-06). The only committed run log (GHA run 31078897925) predates this "
                      "code and contains no C-6b result. A fresh b4-cal.yml GHA dispatch is required "
                      "to produce that number; per the machine-piped-claims discipline this generator "
                      "refuses to hand-fill a value that has not actually been computed.",
            "expected_if_computed": 12,
            "script_section": "C-6b in search/probe/b4_cal_v1/cal_b4_n19_pentagon.g (after the existing "
                               "'C-6 後半: NOT COMPUTED this pass' block)",
        },
        "P1": {
            "gha_run_id": "31067255800",
            "R_size_decimal": str(p1_r_size),
            "R_size_expected_decimal": str(p1_r_expected),
            "R_size_expected_formula": "7^41",
            "B4_EXQ1_pass": p1_b4exq1_pass,
            "Z_R_size": p1_zR_size,
            "B4_EXQ2_status": "CRASHED_OOM_INCOMPLETE",
            "B4_EXQ2_note": "|Z(R)| was computed and printed (3909821048582988049), but the subsequent "
                            "DirectFactorsOfGroup(R) call hit GHA's -o 6g memory limit "
                            "('Error, reached the pre-set memory limit'). The script never reached its "
                            "P1_PASS/ALL_DONE markers because of this downstream OOM in the B4-EXQ-2 "
                            "block -- this is NOT a P1_FAIL of B4-EXQ-1 (which was already printed and "
                            "confirmed true before the crash). B4-EXQ-2 (R = C7 x Q direct-factor "
                            "confirmation) remains UNCONFIRMED, not FAIL.",
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
            "waiver_status": "candidate -- NOT yet ruled on by 司令塔/Sol; this cert does NOT treat the "
                              "waiver as in effect and records C-8 as plain SKIP, not as satisfied-via-waiver.",
        },
        "overall": {
            "computed_checks": ["C1", "C2", "C3a", "C3b", "C4.primary_method", "C4.cross_method",
                                 "C5", "C6_first_half", "P1.B4_EXQ1"],
            "all_computed_checks_pass": all([
                c1_pass, c2_pass, c3a_pass, c3b_pass, c4_pass, (c4_crossmethod_count == 216),
                c5_both_units_pass, c6_first_half_pass, p1_b4exq1_pass,
            ]),
            "pending_items": ["C6b_second_half (awaiting fresh GHA dispatch with the new code)",
                               "P1.B4_EXQ2 (R = C7 x Q direct-factor split -- OOM before confirmation)",
                               "C8 (environment blocker, waiver candidate not yet ruled on)"],
            "note": "'all_computed_checks_pass' covers ONLY the checks this cert could actually extract "
                    "from a real log. It does NOT imply CAL-B4/P0 as a whole is complete -- see "
                    "pending_items and docs/notes/cal_b4_c8_waiver_prereg_v1.md.",
        },
    }

    OUT_CERT.parent.mkdir(parents=True, exist_ok=True)
    OUT_CERT.write_text(json.dumps(cert, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_CERT}")
    print(json.dumps(cert["overall"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
