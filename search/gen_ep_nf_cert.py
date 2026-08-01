#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/gen_ep_nf_cert.py

Machine-piped generator for search/certs/ep_nf_20260801.json (司令塔指示
2026-08-01 item 6: NF 両 lane 実装+E-5 C-1..C-5 の全経路テストの cert).
Runs search/ninfty-nf-crosscheck.py over the 3 genuine fixtures + beta, and
assembles a cert with a conventions_used block (Sol 便94 CV-1..CV-9
direction, F94-5.1/F94-5.2) and an explicit comparison_target, per
memory "Machine-piped claims": no value in the cert is hand-typed, this
script is the sole producer.

Run: python search/gen_ep_nf_cert.py > search/certs/ep_nf_20260801.json
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.join(HERE, "fixtures", "ninfty")
EPDIR = os.path.join(HERE, "certs", "ep_first_run")

GENUINE_FIXTURES = ["checker_pos_01.json", "checker_pos_02.json", "checker_pos_03.json"]
BETA_FIXTURE = os.path.join(EPDIR, "beta_candidate.json")

SOURCE_FILES = [
    "search/ninfty-searcher-v2.mjs",
    "search/ninfty-nf-lanea-cli.mjs",
    "search/ninfty-checker.py",
    "search/ninfty-checker-native.py",
    "search/ninfty-nf-laneb.py",
    "search/ninfty-nf-crosscheck.py",
    "search/test_ninfty_nf.py",
]


def sha256_of_file(rel_path):
    with open(os.path.join(HERE, "..", rel_path), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def sha256_of_file_abs(abs_path):
    with open(abs_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run_crosscheck(candidate_path):
    script = os.path.join(HERE, "ninfty-nf-crosscheck.py")
    out = subprocess.run([sys.executable, script, candidate_path], capture_output=True, encoding="utf-8", check=True)
    return json.loads(out.stdout)


def run_pytest_like(script_name):
    path = os.path.join(HERE, script_name)
    out = subprocess.run([sys.executable, path], capture_output=True, encoding="utf-8", errors="replace")
    tail = ""
    if out.stdout and out.stdout.strip():
        tail = out.stdout.strip().splitlines()[-1]
    return {"script": script_name, "exit_code": out.returncode, "stdout_tail": tail}


def main():
    genuine_reports = {}
    for name in GENUINE_FIXTURES:
        path = os.path.join(FIXDIR, name)
        report = run_crosscheck(path)
        genuine_reports[name] = {
            "candidate_sha256": sha256_of_file_abs(path),
            "lane_a_status": report["lane_a_status"],
            "lane_b_status": report["lane_b_status"],
            "digest_match": report.get("digest_match"),
            "n1_n5_all_pass": report.get("all_pass"),
            "n1_n5_detail": report.get("n1_n5"),
            "lane_a_nf_digest": report["lane_a_full"]["nf_digest"] if "lane_a_full" in report else None,
        }
        # also stash full lane digests directly from the underlying reports
        genuine_reports[name]["nf_digest_lane_a"] = None
        genuine_reports[name]["nf_digest_lane_b"] = None

    # re-run once more directly to capture both nf_digests explicitly (report
    # above only keeps them when status != PRESENT; re-derive here honestly)
    for name in GENUINE_FIXTURES:
        path = os.path.join(FIXDIR, name)
        lanea = subprocess.run(["node", os.path.join(HERE, "ninfty-nf-lanea-cli.mjs"), path],
                                capture_output=True, encoding="utf-8", check=True)
        laneb = subprocess.run([sys.executable, os.path.join(HERE, "ninfty-nf-laneb.py"), path],
                                capture_output=True, encoding="utf-8", check=True)
        a_json = json.loads(lanea.stdout)
        b_json = json.loads(laneb.stdout)
        genuine_reports[name]["nf_digest_lane_a"] = a_json["nf_digest"]
        genuine_reports[name]["nf_digest_lane_b"] = b_json["nf_digest"]

    beta_report = run_crosscheck(BETA_FIXTURE)
    beta_record = {
        "candidate_sha256": sha256_of_file_abs(BETA_FIXTURE),
        "lane_a_status": beta_report["lane_a_status"],
        "lane_b_status": beta_report["lane_b_status"],
        "decision_lane_concordance": beta_report.get("decision_lane_concordance"),
        "lane_a_primary_reason_code": beta_report["lane_a_full"]["primary_reason_code"],
        "lane_b_primary_reason_code": beta_report["lane_b_full"]["primary_reason_code"],
        "n1_n5": beta_report.get("n1_n5"),
    }

    regression_scripts = [
        "test_ninfty_nf.py",
        "test_ninfty_checker_native.py",
        "test_ninfty_laneB.py",
        "test_ninfty_evidence_union.py",
        "test_ninfty_legacy_normalizer.py",
    ]
    regression_results = [run_pytest_like(s) for s in regression_scripts]

    source_digests = {f: sha256_of_file(f) for f in SOURCE_FILES}

    cert = {
        "cert_id": "search/certs/ep_nf_20260801.json",
        "role": "EP re-activation batch: two-lane independent NF calculators + N-1..N-5 crosscheck + mint gate + E-5 C-1..C-5, per 司令塔指示 2026-08-01 (裁定311 / Sol 便94 §4 P94-1/P94-4.1/F94-4.2).",
        "governing_docs": [
            "docs/notes/lanea_native_semantics_v1.md (Theorem A/B, NF §4.1, N-1..N-5)",
            "sol/sol_reply_94_math21.md §4 (F94-4.1, F94-4.2, W94-4.1, P94-4.1, F94-4.3, F94-4.4, P94-4.2)",
        ],
        "conventions_used": {
            "chi_level": [
                {"layer": "candidate-instance", "purpose": "mint-gate verdict per (a,p,f6) triple", "modulus": None, "source": "evaluateDecisionLane (lane A) / run_checker (lane B)"},
            ],
            "comparison_target": {
                "function_compared": "NF (normal form, spec §4.1): (ram_finite, ram_infinite, branch, non_ramification_certificates)",
                "domain": "candidates satisfying E-1..E-4, T-1, T-2, (Pell) (mint-gate PRESENT only; ABSENT/INTEGRITY_STOP candidates compared on decision-lane concordance only, not NF)",
                "source_digests": None,  # filled below
                "normalization_digest": None,  # filled below (sha256 of this cert's own N-1..N-5 comparator source)
            },
            "separation_condition": {
                "included": True,
                "competitor_universe": "lane A (mjs/node) vs lane B (python/sympy) NF calculators; the crosscheck script (search/ninfty-nf-crosscheck.py) imports neither",
                "comparison_basis": "each lane's CLI is invoked as a SEPARATE OS subprocess; only stdout JSON is compared -- no shared in-process helper",
                "forbidden_value_handling": "ABSENT/INTEGRITY_STOP candidates never enter N-1..N-5; reported as decision_lane_concordance instead",
            },
            "round_trip_witness": "not applicable (NF construction is one-directional: candidate -> NF; no inverse claimed)",
            "coset_action_type": "not applicable (this cert concerns divisor/ideal data, not group actions)",
            "cv8_representative_vs_invariant": "not applicable (no group element representative involved)",
            "effective_source_chain": {
                "original": "docs/week4-NInfty_stage2_spec_v18.md §4.1 (native_artifact schema)",
                "supersedes": "lanea_native_semantics_v1.md §3 (rejects branch_divisor_on_P1_ref mislabel, defines NF)",
                "errata": [],
            },
            "seal_recoverability": "not applicable (no sealed value touched by this cert -- C is candidate-derived and already exposed in existing native artifacts per §4.3 要点3 of the governing note)",
            "IF_FIRST": True,
        },
        "if_first_note": "conventions_used block adopted FIRST (before result fields below), per Sol 便94 F94-5.1/CV block direction.",
        "mint_gate": {
            "rule": "REJECT -> ABSENT (no NF minted); INTEGRITY_STOP -> INTEGRITY_STOP (no NF minted, theorem-forced identity broke); ACCEPT (all prerequisites + (60.5)/E-6/E-5-derivation PASS) -> PRESENT (NF minted)",
            "applies_to": ["lane A (search/ninfty-searcher-v2.mjs computeNormalFormLaneA)", "lane B (search/ninfty-nf-laneb.py compute_normal_form_lane_b)"],
        },
        "e5_c1_c5": {
            "applied_to": ["lane A (search/ninfty-searcher-v2.mjs)", "lane B (search/ninfty-checker.py)"],
            "c1_derived": "E-5 treated as DERIVED (not caller-attested-only) once E-1..E-4 hold, both lanes",
            "c2_unknown_removed": "E-5 removed from lane B's result['unknown'] list",
            "c3_reject_to_integrity_stop": "attested orientation contradicting the derived value now raises INTEGRITY code 'divisor-orientation-attestation-mismatch' [27] instead of REJECT[6], both lanes",
            "c4_absent_attestation_not_rejected": "attestation absent is never REJECTed on either lane (unchanged behavior, now documented as C-4 compliance)",
            "c5_simultaneous": "both lanes edited in this same batch, per §5.2 C-5's independence-preserving instruction",
        },
        "genuine_fixtures": genuine_reports,
        "beta_fixture_absent_control": beta_record,
        "regression_suites": regression_results,
        "source_file_sha256": source_digests,
        "scope_note": (
            "This cert covers ONLY the NF calculators + crosscheck + mint gate + E-5 C-1..C-5, per 司令塔 item 1-4/6. "
            "It does NOT cover: bundle/commit_generation wiring to NF, registry mint reflection, or CI (司令塔 item 6, "
            "explicitly deferred to the next batch; see lanea_native_semantics_v1.md §8's 'unimplemented' list)."
        ),
        "cross_checked_not_verified": True,
    }
    cert["conventions_used"]["comparison_target"]["source_digests"] = source_digests
    cert["conventions_used"]["comparison_target"]["normalization_digest"] = source_digests["search/ninfty-nf-crosscheck.py"]

    print(json.dumps(cert, indent=2, sort_keys=True, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
