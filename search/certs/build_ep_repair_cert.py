#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/certs/build_ep_repair_cert.py

Generates search/certs/ep_repair_v19_20260801.json. EVERY machine value in
that cert -- suite counts, exit codes, file digests, union column statuses,
registry generation/freeze ids -- is produced by THIS script actually
running the thing it reports (手写し禁止, machine-piped-claims policy). The
prose fields are the author's; the numbers are not.

usage: python search/certs/build_ep_repair_cert.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEARCH = os.path.dirname(HERE)
REPO = os.path.dirname(SEARCH)
OUT = os.path.join(HERE, "ep_repair_v19_20260801.json")

PY_SUITES = [
    "test_ninfty_nf", "test_ninfty_checker_native", "test_ninfty_laneB",
    "test_ninfty_evidence_union", "test_ninfty_legacy_normalizer", "test_ninfty_r3nf",
]

DIGEST_FILES = [
    "docs/week4-NInfty_stage2_spec_v19.md",
    "docs/mb_ninfty_verifier_contract_v14.md",
    "docs/mb_dependency_manifest_v14.md",
    "search/bundle-selfaudit-v9.py",
    "search/repin_v19_bundle.py",
    "search/ninfty-verifier-w6-r3nf.py",
    "search/ninfty-evidence-union-full.py",
    "search/test_ninfty_r3nf.py",
    "search/test_ninfty_nf.py",
    "search/test_ninfty_evidence_union.py",
    "search/ninfty-native-registry.py",
    "search/ninfty-native-registry-provisioning.py",
    "search/ninfty-ep-genuine-provisioning.py",
    "search/ninfty-checker.py",
    "search/ninfty-searcher-v2.mjs",
    "search/certs/build_full_witness_evidence.py",
    "search/certs/ep_ci_full_witness_evidence_20260801.json",
    "search/fixtures/ninfty/neg_divisor_orientation_27.json",
    "search/fixtures/ninfty/neg_divisor_orientation_27_no_attestation.json",
    ".github/workflows/ep-union-check.yml",
]

FROZEN_FILES = [
    "docs/week4-NInfty_stage2_spec_v18.md",
    "docs/mb_ninfty_verifier_contract_v13.md",
    "docs/mb_dependency_manifest_v13.md",
    "search/ninfty-evidence-union.py",
    "search/ninfty-verifier-b.py",
    "search/ninfty-verifier-w6-r2.py",
    "search/bundle-selfaudit-v8.py",
]

SUMMARY_RE = re.compile(r"^\s*(\d+/\d+ checks passed\.|\d+ checks, \d+ FAIL|=== summary: \d+/\d+ passed ===)\s*$")


def _sha256(rel):
    with open(os.path.join(REPO, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _run(cmd):
    p = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", cwd=REPO)
    lines = [ln.rstrip() for ln in (p.stdout or "").splitlines()]
    summary = next((ln.strip() for ln in reversed(lines) if SUMMARY_RE.match(ln)), None)
    return {"command": " ".join(os.path.basename(c) if c == sys.executable else c for c in cmd),
            "exit_code": p.returncode, "summary_line": summary}


def _count(summary):
    if not summary:
        return None
    m = re.search(r"(\d+)/(\d+) (?:checks passed|passed)", summary)
    if m:
        return int(m.group(2))
    m = re.search(r"(\d+) checks, (\d+) FAIL", summary)
    if m:
        return int(m.group(1))
    return None


def main():
    suites = {}
    for name in PY_SUITES:
        suites[name] = _run([sys.executable, os.path.join(SEARCH, f"{name}.py")])
    suites["ninfty-selftest-lanea.mjs"] = _run(["node", os.path.join(SEARCH, "ninfty-selftest-lanea.mjs")])

    total = 0
    incomplete = []
    for name, r in suites.items():
        c = _count(r["summary_line"])
        r["checks"] = c
        if c is None:
            incomplete.append(name)
        else:
            total += c

    selfaudit = {
        "v8_against_frozen_v18_v13_v13": _run([sys.executable, os.path.join(SEARCH, "bundle-selfaudit-v8.py")]),
        "v9_static_against_v19_v14_v14": _run([sys.executable, os.path.join(SEARCH, "bundle-selfaudit-v9.py")]),
        "v9_mutation_fixtures": _run([sys.executable, os.path.join(SEARCH, "bundle-selfaudit-v9.py"), "--mutate"]),
    }

    full_proc = subprocess.run(
        [sys.executable, os.path.join(SEARCH, "ninfty-evidence-union-full.py"),
         os.path.join(HERE, "ep_ci_full_witness_evidence_20260801.json")],
        capture_output=True, encoding="utf-8", cwd=REPO)
    full = json.loads(full_proc.stdout)
    four = full.get("four_role_registry_status", {})

    frozen_status = {}
    for rel in FROZEN_FILES:
        p = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=REPO, capture_output=True)
        frozen_status[rel] = {"byte_identical_to_HEAD": p.returncode == 0, "sha256": _sha256(rel)}

    cert = {
        "cert_id": "search/certs/ep_repair_v19_20260801.json",
        "generated_by": "search/certs/build_ep_repair_cert.py",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "role": ("Sol 便95 (sol_reply_95_math22.md §2) EP 再発効修理バンドル -- EP 専任係 (ep-keeper) による "
                 "引き継ぎ完遂記録。値はすべてこの script の実行出力(手写しなし)。"),
        "cross_checked_not_verified": True,
        "governing_docs": ["sol/sol_reply_95_math22.md §2 (P95-2.1 / F95-2.1 / W95-2.1-2.3 / F95-2.2-2.4 / P95-2.2)"],

        "ep_status": "uncalibrated/UNKNOWN",
        "calibrated_detector": False,
        "does_not_claim": [
            "EP 再発効 (re-activation)",
            "calibrated detector",
            "union 実 PASS (the full union's overall status is reported verbatim below and is NOT PASS)",
            "operational sentinel unlocked",
        ],

        "item_status": {
            "1_versioned_freeze_[27]": "DONE (spec v19 / contract v14 / manifest v14 + selfaudit v9 + 両縁 negative fixtures)",
            "2_ci_fail_closed": "DONE (fail-open in the previous draft's registry-smoke assert repaired -- see note)",
            "3_R3_NF_new_route": "DONE (new route + new suite; F95-2.2 の承認形どおり)",
            "4_full_witness_bearing_certificate": ("PARTIAL -- fixture built from the genuine fixtures and wired; "
                                                   "four-role registry + docs-era binding + R3-NF reach PASS; "
                                                   "R1/R2 reach MALFORMED for a STRUCTURAL reason that cannot be "
                                                   "fixed by a fixture (see r1_r2_blocker below). 司令塔検問案件。"),
            "5_terminology_diagnostic_vs_minted": "DONE (audit + explicit terminology in the new modules and lane files)",
            "6_positive_control": "NOT IMPLEMENTED, as instructed (諮問継続) -- EP stays uncalibrated/UNKNOWN",
        },

        "regression": {
            "suites": suites,
            "total_checks": total,
            "suites_without_a_parsed_summary_line": incomplete,
            "all_exit_zero": all(r["exit_code"] == 0 for r in suites.values()),
            "note": ("7 suites (was 6 -- test_ninfty_r3nf.py is new). The per-suite counts above are parsed "
                     "from each suite's own printed summary line, not restated by hand."),
        },
        "selfaudit": selfaudit,

        "freeze": {
            "new_freeze_id": four.get("freeze_id"),
            "new_generation_id": four.get("generation_id"),
            "supersedes_freeze_id": "ep-genuine-20260801",
            "supersede_not_overwrite": ("the previous generation directory is left in place on disk; only "
                                        "CURRENT.json was atomically re-pointed"),
            "receipt_schema_id": "mb/ninfty-ep-registry/gen-receipt/v2",
            "why_a_re_freeze_was_required": (
                "a gen-receipt/v1 records only the generation's own artifacts -- nothing in it says WHICH "
                "spec/contract/manifest era the generation was provisioned under. Bumping the docs trio to "
                "v19/v14/v14 therefore left the ep-genuine-20260801 generation unbindable to its own governing "
                "documents. gen-receipt/v2 adds a required governing_docs block pinning all three digests; "
                "R3-NF refuses a v1 receipt (an absent binding is not a satisfied binding)."),
            "governing_docs_pinned_in_the_receipt": (four.get("docs_era_binding") or {}).get("documents"),
            "artifacts": "3 genuine fixtures x 4 roles (native_a, native_b, nf_a, nf_b) = 12, one generation",
        },

        "full_union_machine_result": {
            "fixture": "search/certs/ep_ci_full_witness_evidence_20260801.json",
            "cli": "search/ninfty-evidence-union-full.py",
            "cli_exit_code": full_proc.returncode,
            "columns": {k: v.get("status") for k, v in full.get("columns", {}).items()},
            "overall_full": full.get("overall_full"),
            "four_role_registry_status": four.get("status"),
            "docs_era_binding_ok": (four.get("docs_era_binding") or {}).get("ok"),
            "R3_NF_reason": (full.get("columns", {}).get("R3-NF", {}).get("detail") or {}).get("reason"),
            "R1_detail": full.get("columns", {}).get("R1", {}).get("detail"),
            "calibrated_detector": full.get("calibrated_detector"),
        },

        "r1_r2_blocker": {
            "finding": (
                "R1/R2 CANNOT reach PASS against the genuine cross-lane native pair, and no fixture edit can "
                "change that. W-6 compares a {branch_value: multiplicity} map extracted from each lane's "
                "registry-pinned native artifact. Lane B's native carries exactly that "
                "(/branch_divisor_on_P1). Lane A's native represents the branch divisor by IDEAL GENERATORS "
                "per locus and contains no such array anywhere, so the searcher-side json_pointer either "
                "fails to resolve or resolves to component objects that carry no branch_value -- MALFORMED, "
                "as reported above. Lane A's own certificate generator sidesteps this by DERIVING a map "
                "(locus_type as the branch_value) and shipping it as an inline-only ref, which the registry "
                "gate correctly refuses (LEGACY_UNVERIFIED_REF: an inline ref never dereferences into the "
                "pinned artifact and so cannot certify native provenance)."),
            "consequence": (
                "the two lanes' native artifacts do not speak a common language at the W-6 layer. NF is "
                "precisely the common language introduced for this, and R3-NF -- which PASSES here on the "
                "genuine same-generation nf_a/nf_b pair -- is the real cross-lane agreement."),
            "what_would_be_required": (
                "either (a) lane A's native producer emits a pushforward map in the W-6 comparison shape, or "
                "(b) lane B's native producer emits a locus-typed map, or (c) W-6 is declared a same-lane "
                "historical route and cross-lane agreement is carried by R3-NF alone. ALL THREE are semantic "
                "changes to a lane or to a route's meaning, i.e. OUTSIDE this係's authority: 司令塔の検問 + "
                "Sol のゲート案件。Nothing was invented here to make a column green."),
        },

        "frozen_boundary": {
            "files_asserted_byte_identical_to_HEAD": frozen_status,
            "lane_files_touched_comment_only": {
                "search/ninfty-checker.py": "F95-2.3 terminology comment block only (no executable line changed)",
                "search/ninfty-searcher-v2.mjs": "F95-2.3 terminology comment block only (no executable line changed)",
            },
            "registry_modules_extended_additively": {
                "search/ninfty-native-registry.py": (
                    "gen-receipt/v2 accepted alongside v1; governing_docs validated fail-closed in BOTH "
                    "directions (a v2 without the block, and a v1 with it, both refuse to resolve); "
                    "receipt_schema_id/governing_docs passed through resolve_bundle uninterpreted. No "
                    "existing key changed meaning."),
                "search/ninfty-native-registry-provisioning.py": (
                    "commit_generation gained an optional governing_docs argument, validated with the "
                    "RESOLVER's own validator before any file is written, plus a read-back self-check."),
                "search/ninfty-ep-genuine-provisioning.py": (
                    "--governing-docs flag; each document's artifact_id is READ from the document's own "
                    "structural id declaration and its digest recomputed from the file bytes."),
            },
        },

        "negative_fixtures_both_edges": {
            "firing": "search/fixtures/ninfty/neg_divisor_orientation_27.json -- attested orientation "
                      "CONTRADICTS the derived value: both lanes INTEGRITY_STOP / [27], neither mints.",
            "non_firing": "search/fixtures/ninfty/neg_divisor_orientation_27_no_attestation.json -- the SAME "
                          "(a,p,f6) with the attestation keys deleted: both lanes MINT (PRESENT), N-1..N-5 "
                          "all pass, and the [27] reason string appears nowhere in either report.",
            "why_both": "an omitted attestation is not an error (the derived value is the authority). Only "
                        "the pair pins the predicate: the firing fixture alone would not catch a regression "
                        "that made [27] fire on ABSENCE, and the non-firing fixture alone would not catch "
                        "one that stopped it firing on contradiction.",
        },

        "file_sha256": {rel: _sha256(rel) for rel in DIGEST_FILES},

        "open_items_P95_2_2": {
            "1_new_exact_freeze_bundle_and_receipt": "CLOSED for the registry side (freeze above). The DOCS "
                                                     "trio is DRAFT/candidate -- Sol audit + 司令塔 freeze "
                                                     "receipt not yet sought.",
            "2_ci_fail_closed_receipt": "CLOSED in the workflow file; NOT YET EXERCISED -- workflow_dispatch "
                                        "firing is the 司令塔's action, so no run SHA/receipt is bound yet.",
            "3_full_witness_union": "PARTIAL -- see full_union_machine_result and r1_r2_blocker.",
            "4_positive_control": "OPEN (not implemented by instruction). EP stays uncalibrated/UNKNOWN.",
            "5_quarantine_and_four_role_invariant": "MAINTAINED -- _quarantine_synthetic/ untouched; the "
                                                    "four-role same-generation invariant is now machine-"
                                                    "asserted by the full union itself, not only by "
                                                    "provisioning.",
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    print(f"wrote {OUT}")
    print("total checks:", total, "| all suites exit 0:", cert["regression"]["all_exit_zero"])
    print("freeze:", cert["freeze"]["new_freeze_id"], cert["freeze"]["new_generation_id"])
    print("columns:", cert["full_union_machine_result"]["columns"],
          "overall:", cert["full_union_machine_result"]["overall_full"])
    frozen_bad = [k for k, v in frozen_status.items() if not v["byte_identical_to_HEAD"]]
    print("frozen files that differ from HEAD:", frozen_bad or "none")


if __name__ == "__main__":
    main()
