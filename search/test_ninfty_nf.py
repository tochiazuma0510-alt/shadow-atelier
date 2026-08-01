#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/test_ninfty_nf.py

Test suite for the two-lane NF calculators (search/ninfty-nf-lanea-cli.mjs
wrapping search/ninfty-searcher-v2.mjs's computeNormalFormLaneA,
search/ninfty-nf-laneb.py's compute_normal_form_lane_b) and the third-script
comparator (search/ninfty-nf-crosscheck.py), per docs/notes/
lanea_native_semantics_v1.md §4.1 (N-1..N-5) and Sol 便94 §4 / 裁定311.

Cases:
  * checker_pos_01/02/03.json (genuine positive fixtures, T-1/T-2/(Pell) all
    PASS): both lanes must mint status=PRESENT, N-1..N-5 must all pass,
    nf_digest must match exactly.
  * beta_candidate.json (real REJECT case, a-partition-mismatch): both lanes
    must report status=ABSENT (mint gate, 裁定309/P94-4.1 item1), with
    decision_lane_concordance=true and matching primary_reason_code.

Run: python search/test_ninfty_nf.py
Exits 0 iff all checks PASS.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.join(HERE, "fixtures", "ninfty")
EPDIR = os.path.join(HERE, "certs", "ep_first_run")

RESULTS = []


def check(name, cond, detail=None):
    RESULTS.append((name, bool(cond), detail))
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name}" + (f"  {detail}" if (detail and not cond) else ""))


def run_crosscheck(candidate_path):
    script = os.path.join(HERE, "ninfty-nf-crosscheck.py")
    out = subprocess.run([sys.executable, script, candidate_path], capture_output=True, encoding="utf-8", check=True)
    return json.loads(out.stdout)


def main():
    genuine = ["checker_pos_01.json", "checker_pos_02.json", "checker_pos_03.json"]
    for name in genuine:
        path = os.path.join(FIXDIR, name)
        report = run_crosscheck(path)
        check(f"{name}: lane A status PRESENT", report["lane_a_status"] == "PRESENT", report.get("lane_a_status"))
        check(f"{name}: lane B status PRESENT", report["lane_b_status"] == "PRESENT", report.get("lane_b_status"))
        check(f"{name}: nf_digest exact match across lanes", report.get("digest_match") is True, report)
        if isinstance(report.get("n1_n5"), dict):
            for k in ["N-1", "N-2", "N-3", "N-4", "N-5"]:
                check(f"{name}: {k}", report["n1_n5"][k]["pass"], report["n1_n5"][k])
        else:
            check(f"{name}: N-1..N-5 ran (not ABSENT)", False, report.get("n1_n5"))
        check(f"{name}: all_pass true", report.get("all_pass") is True, report.get("all_pass"))

    beta_path = os.path.join(EPDIR, "beta_candidate.json")
    beta_report = run_crosscheck(beta_path)
    check("beta: lane A status ABSENT (mint gate, REJECT case)", beta_report["lane_a_status"] == "ABSENT", beta_report.get("lane_a_status"))
    check("beta: lane B status ABSENT (mint gate, REJECT case)", beta_report["lane_b_status"] == "ABSENT", beta_report.get("lane_b_status"))
    check("beta: decision_lane_concordance true", beta_report.get("decision_lane_concordance") is True, beta_report)
    check("beta: primary_reason_code matches across lanes",
          beta_report["lane_a_full"]["primary_reason_code"] == beta_report["lane_b_full"]["primary_reason_code"]
          == "a-partition-mismatch",
          (beta_report["lane_a_full"]["primary_reason_code"], beta_report["lane_b_full"]["primary_reason_code"]))
    check("beta: N-1..N-5 reported ABSENT, not silently PASS", beta_report["n1_n5"] != True and not isinstance(beta_report["n1_n5"], dict), beta_report.get("n1_n5"))

    # --- Sol 便95 P95-2.2 item 1 point 4: negative fixture for [27] --------
    # divisor-orientation-attestation-mismatch must fire on BOTH lanes (not
    # the pre-2026-08-01 REJECT/'precondition/divisor-orientation' [6]
    # routing), and neither lane may mint an NF for it (status must be
    # INTEGRITY_STOP on both sides, never PRESENT -- same mint-gate
    # discipline as the beta/REJECT case above, but for the INTEGRITY_STOP
    # class instead of REJECT).
    orient_path = os.path.join(FIXDIR, "neg_divisor_orientation_27.json")
    orient_report = run_crosscheck(orient_path)
    check("neg-orientation[27]: lane A status INTEGRITY_STOP (not PRESENT -- mint gate)",
          orient_report["lane_a_status"] == "INTEGRITY_STOP", orient_report.get("lane_a_status"))
    check("neg-orientation[27]: lane B status INTEGRITY_STOP (not PRESENT -- mint gate)",
          orient_report["lane_b_status"] == "INTEGRITY_STOP", orient_report.get("lane_b_status"))
    check("neg-orientation[27]: decision_lane_concordance true", orient_report.get("decision_lane_concordance") is True, orient_report)
    check("neg-orientation[27]: primary_reason_code == 'divisor-orientation-attestation-mismatch' on BOTH lanes (not the old REJECT[6] 'precondition/divisor-orientation')",
          orient_report["lane_a_full"]["primary_reason_code"] == orient_report["lane_b_full"]["primary_reason_code"]
          == "divisor-orientation-attestation-mismatch",
          (orient_report["lane_a_full"]["primary_reason_code"], orient_report["lane_b_full"]["primary_reason_code"]))
    check("neg-orientation[27]: neither lane's decision verdict/stage is REJECT",
          orient_report["lane_a_full"]["decision_verdict"] != "REJECT" and orient_report["lane_b_full"]["decision_stage"] != "REJECT",
          (orient_report["lane_a_full"]["decision_verdict"], orient_report["lane_b_full"]["decision_stage"]))
    check("neg-orientation[27]: N-1..N-5 reported ABSENT (no NF minted on either lane to compare)",
          orient_report["n1_n5"] != True and not isinstance(orient_report["n1_n5"], dict), orient_report.get("n1_n5"))

    # --- 束縛条項(b): the NON-FIRING edge of the SAME predicate -----------
    # [27] fires ONLY on an attested value that CONTRADICTS the derived one.
    # An OMITTED attestation is not an error (the derived value is the
    # authority) -- so the identical (a,p,f6) with the two attestation keys
    # deleted must take the ORDINARY route and MINT on both lanes. Testing
    # only the firing side would leave an "undefined read as failure"
    # regression (or its mirror) invisible; this pair pins both edges.
    noattest_path = os.path.join(FIXDIR, "neg_divisor_orientation_27_no_attestation.json")
    noattest_report = run_crosscheck(noattest_path)
    check("no-attestation edge: same (a,p,f6) as the [27] fixture, attestation OMITTED -> lane A MINTS (status PRESENT, not INTEGRITY_STOP)",
          noattest_report["lane_a_status"] == "PRESENT", noattest_report.get("lane_a_status"))
    check("no-attestation edge: lane B MINTS (status PRESENT, not INTEGRITY_STOP)",
          noattest_report["lane_b_status"] == "PRESENT", noattest_report.get("lane_b_status"))
    check("no-attestation edge: N-1..N-5 all pass (ordinary route, real cross-lane NF agreement)",
          noattest_report.get("all_pass") is True and isinstance(noattest_report.get("n1_n5"), dict),
          noattest_report.get("all_pass"))
    check("no-attestation edge: nf_digest agrees across lanes",
          noattest_report.get("digest_match") is True, noattest_report.get("digest_match"))
    check("no-attestation edge: [27] does NOT appear anywhere in either lane's report (non-firing side of the predicate)",
          "divisor-orientation-attestation-mismatch" not in json.dumps(noattest_report),
          "searched the whole report text for the [27] reason string")
    check("両縁 contrast is real: the ONLY difference between the two fixtures is the attestation keys",
          {k: v for k, v in json.load(open(orient_path, encoding="utf-8")).items()
           if k in ("a", "p", "f6")}
          == {k: v for k, v in json.load(open(noattest_path, encoding="utf-8")).items()
              if k in ("a", "p", "f6")},
          "(a,p,f6) identical across the firing and non-firing fixtures")

    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print(f"\n{len(RESULTS)} checks, {n_fail} FAIL")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
