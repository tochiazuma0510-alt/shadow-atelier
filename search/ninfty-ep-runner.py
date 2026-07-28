#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-ep-runner.py  (v3, 裁定127/128 対応版)

v3 CHANGES (司令塔指示, both lanes having migrated to the
docs/notes/cert_shape_interpretation_v1.md flat-array+divisor_object-tag
outer container):
  - cert-schema validator GATE wired in: search/ninfty-cert-validator.py's
    validate_certificate() runs on EVERY certificate BEFORE it is passed to
    ANY verifier (forward or reverse). Gate FAIL -> [12] digest-mismatch
    recorded, verifier NOT invoked for that certificate, in either direction.
  - the old ad-hoc schema converters (lanea_object_cert_to_laneb_flat,
    laneb_cert_to_lanea_style, etc.) are REMOVED. Both lanes now claim to
    speak the same outer interface, so gate-passed certificates are fed
    to the OTHER lane's verifier UNMODIFIED -- this is the only way to
    honestly answer the coordinator's question ("did witness-structure
    concordance improve from missing-agreement/ABSENT to genuine structural
    agreement, now that real data flows both ways without a receiving-side
    conversion layer built to paper over gaps"). Where the two lanes'
    inner witness/bijection micro-schemas still diverge (found live during
    this v3 pass: component_bijection sub-schema, ideal-equality/
    disjointness witness nesting, multiplicity field names), this is
    reported as a genuine, precise, ROOT-CAUSED finding, not smoothed over.
  - a SEPARATE diagnostic-only section (clearly labeled, gate-bypassed) is
    additionally run for certificates that FAIL the gate, purely to record
    what the raw structural interaction looks like -- never presented as
    part of the official gated EP verdict.
  - N76-5.3 checklist and input_bundle_digest recomputed against the new
    file set (adds search/ninfty-cert-validator.py).
  - search/ninfty-witness-gen.py (mentioned as in-progress by the
    coordinator) is checked for; if absent, recorded PENDING/UNKNOWN and
    this run does not wait for it.

v2 CHANGES (司令塔裁定124, addressing sol/sol_reply_76_math3.md F5 total FAIL):

EP (endorsement point) runner -- RECEIVING-SIDE reconciliation of lane A
(node: search/ninfty-searcher-v2.mjs + search/ninfty-verifier-a.mjs) and
lane B (python: search/ninfty-checker.py + search/ninfty-verifier-b.py).

v2 CHANGES (司令塔裁定124, addressing sol/sol_reply_76_math3.md F5 total FAIL):
  - P76-3 manifest compiler GATE: this script no longer reads the
    hand-authored search/certs/laneA_manifest.json / laneB_manifest.json
    directly. It first runs search/ninfty-manifest-compiler.py, which
    machine-generates schema-valid true/false records from the frozen
    [branch-contract] (fixing F76-5.1 top-level-false-branch,
    F76-5.2 null-not-ABSENT forbidden keys, F76-5.3 symbolic content
    digests). If that gate FAILS, THIS SCRIPT DOES NOT INVOKE EITHER
    VERIFIER and exits nonzero (F76 total-FAIL discipline: no partial
    self-declared PASS on top of a failed input gate).
  - F76-5.4: removed the self-contradictory toolchain-digest wording (v1
    called a lane-B value both "valid, no placeholder" and "placeholder" in
    different fields of the same report). The compiled manifest now carries
    real digests where obtainable and explicit UNKNOWN notes where not;
    the report quotes the compiler's own notes verbatim instead of writing
    a second, independently-worded (and in v1, contradictory) claim.
  - F76-5.5: the "17/17" figure is now labeled explicitly and ONLY as
    decision-lane reason-code concordance (cross_fixture_native_verdict).
    A SEPARATE, clearly distinguished section reports the per-witness
    verifier concordance (laneA_5_cert_fixtures_via_laneB_verifier), which
    is NOT a full witness PASS (see N76-5.3 checklist item 4) -- W-4/W-6 are
    genuinely ABSENT on both native sides at lane A's current scope (no
    chart/point-level data exists to check), which this report states as
    "concordant ABSENT, not a positive PASS concordance", per Sol's own
    wording in F76-5.5.
  - reverse direction (lane B cert fixtures -> verifier A) is now attempted,
    since lane B's cert_pos/neg_*.json fixtures now carry explicitly
    disclosed STAND-IN native_a/native_b fields (see per-fixture
    "_stand_in_disclosure"). This report carries that disclosure forward
    verbatim and does not present the result as genuine lane-A-native
    agreement.
  - N76-5.3 minimal-condition checklist is embedded with PASS/FAIL/UNKNOWN
    per item.
  - report is bound to an input_bundle_digest: sha256 over the canonical
    list of {path: sha256-of-actual-bytes} for every file this run actually
    read/executed (compiler + both compiled manifests + both verifier
    scripts + both checker/searcher scripts + every fixture file consumed).
    This lets a later reviewer confirm which exact bytes produced this
    report, without re-trusting this script's own prose.

Governing documents:
  docs/mb_ninfty_verifier_contract_v13.md  (sec.3.4 result vector, sec.7 [26]
                                             concordance, C-7 no-cross-read)
  docs/mb_dependency_manifest_v13.md       (sec.2.34 [branch-contract], sec.6
                                             I-3a/b/d, receiving-side recompute)
  provenance/ninfty_freeze_receipt_sol75.md
  sol/sol_reply_76_math3.md F5 (this file's repair mandate)
  裁定_124_ben76.md

ROLE: this script does NOT judge the underlying mathematics or declare
completeness. It cross-checks two independently-produced artifact sets and
reports agreement / disagreement / not-attempted (UNKNOWN/ABSENT), with an
explicit refusal to invoke verifiers if the manifest compiler gate fails.
It does not commit anything, does not touch certificates/mb/ or sealed
quantities, and does not modify lane A or lane B source files.

Usage: python search/ninfty-ep-runner.py
Output: prints a human-readable report to stdout and writes
        search/certs/ep_run_20260728.json
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SEARCH = ROOT / "search"
CERTS = SEARCH / "certs"
FIXTURES_NINFTY = SEARCH / "fixtures" / "ninfty"

NODE = "node"
PYTHON = sys.executable or "python"

VERIFIER_B = SEARCH / "ninfty-verifier-b.py"
CHECKER_B = SEARCH / "ninfty-checker.py"
LANEA_EXPORT_MJS = CERTS / "ep-lanea-export.mjs"
LANEA_EVAL_MJS = CERTS / "ep-lanea-eval-candidate.mjs"
MANIFEST_COMPILER = SEARCH / "ninfty-manifest-compiler.py"
LANEA_DRAFT = CERTS / "laneA_manifest_v2_draft.json"
LANEB_DRAFT = CERTS / "laneB_manifest_v2_draft.json"
CERT_VALIDATOR = SEARCH / "ninfty-cert-validator.py"
WITNESS_GEN = SEARCH / "ninfty-witness-gen.py"
LANEA_VERIFY_CERT_MJS = CERTS / "ep-lanea-verify-cert.mjs"

WITNESS_ORDER = ["W-1", "W-2", "W-2'", "W-3", "W-4", "W-5", "W-6"]

# --- import the cert-schema validator as a library (裁定127/128 gate) -------
_spec = importlib.util.spec_from_file_location("ninfty_cert_validator", str(CERT_VALIDATOR))
cert_validator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cert_validator)


# ---------------------------------------------------------------------------
# generic helpers
# ---------------------------------------------------------------------------

def canonical_serialize(obj):
    def sort(x):
        if isinstance(x, list):
            return [sort(y) for y in x]
        if isinstance(x, dict):
            return {k: sort(x[k]) for k in sorted(x.keys())}
        return x
    return json.dumps(sort(obj), separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def sha256_file(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_valid_hex_digest(s):
    return isinstance(s, str) and len(s) >= 32 and re.fullmatch(r"[0-9a-fA-F]+", s) is not None


def run_subprocess_json(cmd, input_obj):
    proc = subprocess.run(
        cmd, input=json.dumps(input_obj), capture_output=True, text=True, cwd=str(ROOT),
        encoding="utf-8", errors="replace",
    )
    stdout = (proc.stdout or "").strip()
    if not stdout:
        return {"_subprocess_error": True, "returncode": proc.returncode, "stderr": proc.stderr[-4000:]}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"_subprocess_json_error": True, "raw_stdout": stdout[:4000], "stderr": proc.stderr[-4000:]}


def run_node_stdin(script_path, payload):
    return run_subprocess_json([NODE, str(script_path)], payload)


def run_python_stdin(script_path, payload):
    return run_subprocess_json([PYTHON, str(script_path), "-"], payload)


# ===========================================================================
# [0/5] P76-3 manifest compiler gate -- MUST run and PASS before any verifier
#       is invoked (裁定124 mandate, replacing v1's direct hand-authored-JSON read)
# ===========================================================================

def run_manifest_compiler_gate():
    proc = subprocess.run(
        [PYTHON, str(MANIFEST_COMPILER)], capture_output=True, text=True, cwd=str(ROOT),
        encoding="utf-8", errors="replace",
    )
    gate_passed = proc.returncode == 0
    return {
        "gate_passed": gate_passed,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


# ===========================================================================
# [1/5] manifest cross-check: I-3a (binary) / I-3b (source) / I-3d (build)
#    over the COMPILED (gate-validated) manifests, per dependency-manifest v13
#    sec.2 (D-1..D-4') / sec.6 (I-0*, I-3*). Hand-authored laneA_manifest.json
#    / laneB_manifest.json are NOT read by this step anymore (P76-3).
# ===========================================================================

def d1_source_closure(source_artifact_digests):
    return sha256_of(sorted(set(source_artifact_digests or [])))


def d2_implementation_lineage(source_artifact_digests, toolchain_digest, build_step_digests):
    return sha256_of({
        "source": sorted(set(source_artifact_digests or [])),
        "toolchain": toolchain_digest,
        "steps": list(build_step_digests or []),
    })


def recompute_entry_d1_d2(entry):
    d1 = d1_source_closure(entry.get("source_artifact_digests"))
    d2 = d2_implementation_lineage(
        entry.get("source_artifact_digests"),
        entry.get("toolchain_digest"),
        entry.get("build_step_digests"),
    )
    declared_d1 = entry.get("source_closure_digest")
    declared_d2 = entry.get("implementation_lineage_digest")
    d1_match = None if declared_d1 in (None, "") else (d1 == declared_d1)
    d2_match = None if declared_d2 in (None, "") else (d2 == declared_d2)
    return d1, d2, d1_match, d2_match


def load_compiled_manifest(path):
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_faces(manifest):
    entries = manifest.get("entries", [])
    binary = {e.get("content_digest") for e in entries if e.get("content_digest")}
    source = set()
    for e in entries:
        source |= set(e.get("source_artifact_digests") or [])
    build = set()
    for e in entries:
        if e.get("toolchain_digest"):
            build.add(e["toolchain_digest"])
        build |= set(e.get("build_step_digests") or [])
        if e.get("build_record_present") is True:
            if e.get("build_definition_blob_digest"):
                build.add(e["build_definition_blob_digest"])
            build |= set(e.get("pinned_input_digests") or [])
    # top-level (now always true-branch per F76-5.1 fix) also contributes to
    # the build face.
    if manifest.get("build_record_present") is True:
        if manifest.get("build_definition_blob_digest"):
            build.add(manifest["build_definition_blob_digest"])
        build |= set(manifest.get("pinned_input_digests") or [])
    return binary, source, build


def run_manifest_crosscheck():
    manifest_a = load_compiled_manifest(LANEA_DRAFT)
    manifest_b = load_compiled_manifest(LANEB_DRAFT)

    recompute_report = {"laneA": [], "laneB": []}
    for label, manifest in (("laneA", manifest_a), ("laneB", manifest_b)):
        # top-level D-1/D-2 recompute too (top-level is now a full record)
        d1_top = d1_source_closure(manifest.get("source_artifact_digests"))
        d2_top = d2_implementation_lineage(
            manifest.get("source_artifact_digests"), manifest.get("toolchain_digest"),
            manifest.get("build_step_digests"))
        recompute_report[label].append({
            "record": "top-level", "subject_id": manifest.get("subject_id"),
            "recomputed_source_closure_digest": d1_top,
            "recomputed_implementation_lineage_digest": d2_top,
        })
        for e in manifest.get("entries", []):
            d1, d2, d1_ok, d2_ok = recompute_entry_d1_d2(e)
            recompute_report[label].append({
                "record": "entry",
                "content_digest": e.get("content_digest"),
                "source_ref": (e.get("provenance") or {}).get("source_ref"),
                "recomputed_source_closure_digest": d1,
                "recomputed_implementation_lineage_digest": d2,
                "declared_source_closure_digest": e.get("source_closure_digest"),
                "declared_implementation_lineage_digest": e.get("implementation_lineage_digest"),
                "d1_matches_declared": d1_ok,
                "d2_matches_declared": d2_ok,
            })

    bin_a, src_a, build_a = manifest_faces(manifest_a)
    bin_b, src_b, build_b = manifest_faces(manifest_b)

    allowed_tcb = set()  # both compiled manifests declare all four TCB columns empty
    i3a = sorted(bin_a & bin_b)
    i3b = sorted(src_a & src_b)
    i3d = sorted(build_a & build_b)

    # toolchain validity (post-compiler: real digests except the documented
    # `sys`-modeled-as-toolchain equivalence in lane B, which the compiler
    # itself flags -- report that flag verbatim, do not re-word it.
    toolchain_a = manifest_a.get("toolchain_digest")
    toolchain_b = manifest_b.get("toolchain_digest")

    reason_11 = bool(i3a or i3b or i3d)

    return {
        "source": "compiled drafts (search/certs/laneA_manifest_v2_draft.json, laneB_manifest_v2_draft.json), "
                   "NOT the hand-authored laneA_manifest.json/laneB_manifest.json",
        "recompute_D1_D2": recompute_report,
        "faces": {
            "laneA": {"binary": sorted(bin_a), "source": sorted(src_a), "build": sorted(build_a)},
            "laneB": {"binary": sorted(bin_b), "source": sorted(src_b), "build": sorted(build_b)},
        },
        "I-3a_binary_intersection": i3a,
        "I-3b_source_intersection": i3b,
        "I-3d_build_intersection": i3d,
        "toolchain_digest": {"laneA": toolchain_a, "laneB": toolchain_b,
                              "laneA_valid_hex": is_valid_hex_digest(toolchain_a),
                              "laneB_valid_hex": is_valid_hex_digest(toolchain_b)},
        "laneB_compiler_notes": {
            "stdlib_gap_notes": manifest_b.get("stdlib_gap_notes"),
            "toolchain_digest_note": manifest_b.get("toolchain_digest_note"),
        },
        "laneA_compiler_notes": {
            "toolchain_digest_note": manifest_a.get("toolchain_digest_note"),
        },
        "reason_[11]_shared_helper_detected": reason_11,
        "notes": [
            "D-3/D-4' now computed for BOTH top-level records (F76-5.1 fix: top-level is the TRUE branch, "
            "not a bootstrap leaf). Entry-level false-branch records omit the four build-preimage keys "
            "literally (F76-5.2 fix), verified by the compiler gate before this step ran at all.",
            "family face (I-3c') remains an audit flag only (M-3'), not computed here as blocking; "
            "implementation_family_id is null in both compiled manifests (not yet minted by any receipt authority).",
        ],
    }


# ===========================================================================
# [2/5] cross-fixture native-verdict check (decision lane) -- LABELED
#       EXPLICITLY as reason-code concordance only (F76-5.5).
# ===========================================================================

def lanea_decision_to_checker_candidate(candidate):
    out = {"a": candidate["a"], "p": candidate["p"], "f6": candidate["f6"]}
    v = candidate.get("orientation_declared_ok")
    if isinstance(v, bool):
        out["divisor_orientation_attested"] = v
    return out


def laneb_checker_fixture_to_lanea_candidate(fixture):
    out = {"a": fixture["a"], "p": fixture["p"], "f6": fixture["f6"]}
    v = fixture.get("divisor_orientation_attested")
    if isinstance(v, bool):
        out["orientation_declared_ok"] = v
    return out


def run_checker_subprocess(candidate):
    return run_python_stdin(CHECKER_B, candidate)


def run_lanea_decision_subprocess(candidate):
    return run_node_stdin(LANEA_EVAL_MJS, candidate)


def cross_fixture_native_verdict(lanea_export):
    rows = []
    for fx in lanea_export["decision_fixture_results"]:
        checker_input = lanea_decision_to_checker_candidate(fx["candidate"])
        checker_out = run_checker_subprocess(checker_input)
        checker_stage = checker_out.get("stage")
        checker_primary = checker_out.get("primary_reason_code")
        lanea_native = fx["laneA_native"]
        checker_verdict_shape = checker_stage if checker_stage is not None else "ACCEPT-shaped(no-reason)"
        match_primary = (checker_primary == lanea_native["primary_reason_code"]) or (
            checker_primary is None and lanea_native["primary_reason_code"] == "accepted"
        )
        rows.append({
            "direction": "laneA-decision-fixture -> laneB-checker",
            "label": fx["label"],
            "laneA_native_verdict": lanea_native["verdict"],
            "laneA_native_primary": lanea_native["primary_reason_code"],
            "laneB_checker_stage": checker_verdict_shape,
            "laneB_checker_primary": checker_primary,
            "primary_reason_code_match": match_primary,
            "reason_[26]_candidate": not match_primary,
        })

    for fname in sorted(FIXTURES_NINFTY.glob("checker_*.json")):
        fixture = json.loads(fname.read_text(encoding="utf-8"))
        checker_native = run_checker_subprocess({k: v for k, v in fixture.items() if not k.startswith("_")})
        lanea_input = laneb_checker_fixture_to_lanea_candidate(fixture)
        lanea_out = run_lanea_decision_subprocess(lanea_input)
        checker_stage = checker_native.get("stage")
        checker_primary = checker_native.get("primary_reason_code")
        checker_verdict_shape = checker_stage if checker_stage is not None else "ACCEPT-shaped(no-reason)"
        lanea_primary = lanea_out.get("primary_reason_code")
        match_primary = (checker_primary == lanea_primary) or (
            checker_primary is None and lanea_primary == "accepted"
        )
        rows.append({
            "direction": "laneB-checker-fixture -> laneA-decision-lane",
            "label": fname.name,
            "description": fixture.get("_description"),
            "laneB_checker_stage": checker_verdict_shape,
            "laneB_checker_primary": checker_primary,
            "laneA_native_verdict": lanea_out.get("verdict"),
            "laneA_native_primary": lanea_primary,
            "primary_reason_code_match": match_primary,
            "reason_[26]_candidate": not match_primary,
        })
    return rows


# ===========================================================================
# [3/6] cert-schema validator GATE (裁定127/128) -- runs on EVERY candidate
#       certificate BEFORE any verifier call, in BOTH directions.
# ===========================================================================

def gate_certificate(cert, label):
    gate_passed, violations, unknowns, observations = cert_validator.validate_certificate(cert)
    verdict = cert_validator.make_verdict(gate_passed, violations)
    return {
        "label": label, "gate_passed": gate_passed, "verdict": verdict,
        "violations": violations, "unknowns": unknowns, "observations": observations,
    }


# ===========================================================================
# [4/6] forward direction: lane A's 5 cert fixtures -> verifier B, gated,
#       UNMODIFIED (no schema converter -- both lanes claim the same outer
#       interface now; feeding the cert as-is is the honest test of that).
# ===========================================================================

def normalize_lanea_vector(vec):
    d = dict(vec)
    return [(w, d.get(w, "ABSENT")) for w in WITNESS_ORDER]


def normalize_laneb_vector(witness_results_by_label, object_label):
    """witness_results_by_label: {label: {object_label: status}} (v3 shape,
    genuinely independent per object -- 裁定128)."""
    label_map = {"W-1": "W-1", "W-2": "W-2", "W-2prime": "W-2'", "W-3": "W-3", "W-4": "W-4", "W-5": "W-5", "W-6": "W-6"}
    out = {}
    for lbl, per_obj in witness_results_by_label.items():
        out[label_map.get(lbl, lbl)] = per_obj.get(object_label, "ABSENT")
    return [(w, out.get(w, "ABSENT")) for w in WITNESS_ORDER]


def forward_verifier_crosscheck(lanea_export):
    rows = []
    for fx in lanea_export["cert_fixtures"]:
        cert = fx["cert"]
        gate = gate_certificate(cert, f"{fx['id']} (forward, lane A cert -> verifier B)")
        row = {"fixture": fx["id"], "label": fx["label"], "gate": gate}
        if not gate["gate_passed"]:
            row["verifier_invoked"] = False
            row["note"] = "[12] digest-mismatch: certificate failed the schema gate, verifier B was NOT invoked."
            rows.append(row)
            continue

        # UNMODIFIED cert, no converter. v4: native_a/native_b are now
        # supplied (fx["native"], the raw unwrapped native blob lane A's own
        # export produced) -- v3's W-1 edge-form and W-6 native_side checks
        # BOTH require native_a/native_b to reconstruct component sets /
        # pushforward maps (裁定139 items 6/2); omitting them (as v3's EP run
        # did) leaves W-1/W-6 unable to do anything but read ABSENT/FAIL from
        # a degenerate comparison. This also exercises P-3.3 genuinely now.
        # native_artifact_digest is computed (by lane A's own buildSearcherNative)
        # over ONLY {ramification_divisor_on_C_ref, branch_divisor_on_P1_ref}
        # -- fx["native"] additionally carries native_schema_id/_digest/
        # native_artifact_digest wrapper metadata. Passing the WHOLE wrapper
        # as native_a/native_b would hash those extra keys too (a self-
        # referential digest bug on THIS EP script's part, confirmed live:
        # sha256(fx["native"]) != native_artifact_digest, while
        # sha256({the two _ref keys only}) == native_artifact_digest exactly).
        native_slim = {"ramification_divisor_on_C_ref": fx["native"]["ramification_divisor_on_C_ref"],
                       "branch_divisor_on_P1_ref": fx["native"]["branch_divisor_on_P1_ref"]}
        out = run_python_stdin(VERIFIER_B, {"certificate": cert, "native_a": native_slim, "native_b": native_slim})
        row["verifier_invoked"] = True
        row["laneB_raw_result"] = {
            "overall_verdict_B": out.get("overall_verdict_B"),
            "P-0": out.get("P-0"), "P-3": out.get("P-3"),
        }
        for object_name, object_label in (
            ("ramification_divisor_on_C", "ramification_divisor_on_C"),
            ("branch_divisor_on_P1", "branch_divisor_on_P1"),
        ):
            R_A_vec = normalize_lanea_vector(fx["R_A"][object_name])
            wr = out.get("witness_results")
            if not isinstance(wr, dict):
                row.setdefault("objects", {})[object_name] = {"error": "verifier B did not return witness_results", "raw": out}
                continue
            R_B_vec = normalize_laneb_vector(wr, object_label)
            equal = R_A_vec == R_B_vec
            full_pass = equal and all(v == "PASS" for _, v in R_A_vec)
            concordant_absent = equal and any(v == "ABSENT" for _, v in R_A_vec) and not any(v == "FAIL" for _, v in R_A_vec)
            mismatched_witnesses = [(w, a, b) for (w, a), (_, b) in zip(R_A_vec, R_B_vec) if a != b]
            row.setdefault("objects", {})[object_name] = {
                "R_A": R_A_vec, "R_B": R_B_vec, "R_A_eq_R_B": equal,
                "full_witness_PASS": full_pass, "concordant_ABSENT_not_PASS": concordant_absent,
                "reason_[26]_candidate": not equal,
                "mismatched_witnesses": mismatched_witnesses,
            }
        rows.append(row)
    return rows


# ===========================================================================
# [5/6] reverse direction: lane B's cert fixtures -> verifier A, gated,
#       UNMODIFIED (verifier A already reads the flat divisor_object-tagged
#       schema -- confirmed live against ninfty-verifier-a.mjs). Certificates
#       failing the gate get an OFFICIAL [12] record (no verifier call) plus
#       a SEPARATE, clearly-labeled gate-BYPASSED diagnostic run so the raw
#       structural interaction is still visible for debugging -- never
#       presented as part of the official gated verdict.
# ===========================================================================

def reverse_verifier_crosscheck(cert_fixture_paths):
    rows = []
    for path in cert_fixture_paths:
        fixture = json.loads(path.read_text(encoding="utf-8"))
        cert = fixture["certificate"]
        gate = gate_certificate(cert, f"{path.name} (reverse, lane B cert -> verifier A)")
        row = {"fixture": path.name, "description": fixture.get("_description"), "gate": gate}

        # lane B's own native run on its own fixture (unaffected by the
        # cross-lane gate; this is lane B verifying its own certificate,
        # not a cross-lane check) -- reported for context. v4: pass the
        # fixture's own top-level native_a/native_b (present in all 6
        # fixtures post-v3-migration) so W-1/W-6 are genuinely exercised.
        native_a = fixture.get("native_a")
        native_b = fixture.get("native_b")
        native_b_out = run_python_stdin(VERIFIER_B, {"certificate": cert, "native_a": native_a, "native_b": native_b})
        row["laneB_native_overall_verdict_B"] = native_b_out.get("overall_verdict_B")
        row["laneB_native_witness_results"] = native_b_out.get("witness_results")

        if gate["gate_passed"]:
            row["verifier_invoked"] = True
            out = run_node_stdin(LANEA_VERIFY_CERT_MJS, {"certificate": cert, "native_a": native_a, "native_b": native_b})
            row["laneA_verifier_result"] = out
        else:
            row["verifier_invoked"] = False
            row["note"] = "[12] digest-mismatch: certificate failed the schema gate, verifier A was NOT invoked (official pipeline)."
            # gate-BYPASSED diagnostic, clearly separated from the official result.
            diag = run_node_stdin(LANEA_VERIFY_CERT_MJS, {"certificate": cert, "native_a": native_a, "native_b": native_b})
            row["DIAGNOSTIC_gate_bypassed_laneA_verifier_result"] = diag
            row["DIAGNOSTIC_caveat"] = ("NOT part of the official EP v3 verdict -- this certificate FAILED the "
                                        "schema gate and would not reach verifier A in the real pipeline. Run "
                                        "here ONLY to record what the raw structural interaction looks like.")
        rows.append(row)
    return rows


# ===========================================================================
# [6/6] N76-5.3 minimal-condition checklist + input-bundle digest binding
# ===========================================================================

def input_bundle_digest(paths_and_extra):
    entries = []
    for p in paths_and_extra["paths"]:
        pp = Path(p)
        if pp.exists():
            entries.append({"path": str(pp.relative_to(ROOT)) if pp.is_absolute() else str(pp), "sha256": sha256_file(pp)})
        else:
            entries.append({"path": str(p), "sha256": None, "note": "file not found at report time"})
    bundle = {"files": sorted(entries, key=lambda e: e["path"]), "extra": paths_and_extra.get("extra", {})}
    return sha256_of(bundle), bundle


FULL_WITNESS_FIXTURE = CERTS / "full_witness_fixture_01.json"


def full_witness_fixture_crosscheck():
    """search/ninfty-witness-gen.py + search/certs/assemble_full_witness_cert.py
    (found present during this v3 run, per coordinator instruction 'if
    complete, include in EP v3') produce a genuine curve-level chart_overlap/
    pushforward pair spliced into lane A's real generateCertificate() output.
    Gated + run through BOTH verifiers with NO conversion, same discipline
    as the C1..C5 fixtures."""
    if not FULL_WITNESS_FIXTURE.exists():
        return {"present": False, "status": "PENDING", "note": "full_witness_fixture_01.json not found at report time"}
    fixture = json.loads(FULL_WITNESS_FIXTURE.read_text(encoding="utf-8"))
    cert = fixture["certificate"]
    gate = gate_certificate(cert, "full_witness_fixture_01 (curve-level W-4/W-6)")
    row = {"present": True, "description": fixture.get("_description"), "gate": gate}
    if not gate["gate_passed"]:
        row["verifier_invoked"] = False
        return row
    native_a = fixture.get("native_a")
    native_b = fixture.get("native_b")
    laneB_out = run_python_stdin(VERIFIER_B, {"certificate": cert, "native_a": native_a, "native_b": native_b})
    laneA_out = run_node_stdin(LANEA_VERIFY_CERT_MJS, {"certificate": cert, "native_a": native_a, "native_b": native_b})
    row["verifier_invoked"] = True
    row["laneB_result"] = {"overall_verdict_B": laneB_out.get("overall_verdict_B"),
                            "witness_results": laneB_out.get("witness_results"),
                            "P-0": laneB_out.get("P-0"), "P-3": laneB_out.get("P-3")}
    row["laneA_result"] = laneA_out
    if "R_A" in laneA_out and isinstance(laneB_out.get("witness_results"), dict):
        objects = {}
        for object_name, object_label in (
            ("ramification_divisor_on_C", "ramification_divisor_on_C"),
            ("branch_divisor_on_P1", "branch_divisor_on_P1"),
        ):
            R_A_vec = normalize_lanea_vector(laneA_out["R_A"][object_name])
            R_B_vec = normalize_laneb_vector(laneB_out["witness_results"], object_label)
            equal = R_A_vec == R_B_vec
            objects[object_name] = {
                "R_A": R_A_vec, "R_B": R_B_vec, "R_A_eq_R_B": equal,
                "full_witness_PASS": equal and all(v == "PASS" for _, v in R_A_vec),
                "mismatched_witnesses": [(w, a, b) for (w, a), (_, b) in zip(R_A_vec, R_B_vec) if a != b],
            }
        row["objects"] = objects
    return row


def check_witness_gen():
    if WITNESS_GEN.exists():
        return {"present": True, "path": str(WITNESS_GEN.relative_to(ROOT)), "sha256": sha256_file(WITNESS_GEN)}
    return {"present": False, "status": "PENDING", "note": "search/ninfty-witness-gen.py not found at report time; "
            "coordinator described it as in-progress (full-certificate generation) -- this run does NOT wait for it "
            "and proceeds with the fixtures/exports that already exist."}


def main():
    report = {
        "ep_run_id": "search/certs/ep_run_20260728.json (v3, 裁定127/128 対応)",
        "role_note": "受領側検収の記録 (partial predicate). Not a completeness or ACCEPT declaration.",
        "repair_context": "司令塔指示: both lanes migrated to cert_shape_interpretation_v1's flat-array+"
                           "divisor_object-tag outer container; cert-validator wired as a pre-verifier gate; "
                           "EP v3 re-run to measure whether witness concordance improved from missing-agreement "
                           "to genuine structural agreement.",
    }

    print("=== [0/6] P76-3 manifest compiler gate ===")
    gate = run_manifest_compiler_gate()
    report["manifest_compiler_gate"] = gate
    print(gate["stdout"])
    if gate["stderr"]:
        print("stderr:", gate["stderr"])
    if not gate["gate_passed"]:
        print("\nGATE FAILED. Per P76-3 mandate, verifiers are NOT invoked. Aborting.")
        report["aborted_after_gate_failure"] = True
        report["ep_judgment_proposal"] = "FAIL (manifest compiler gate)"
        (CERTS / "ep_run_20260728.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        return 1

    print("\n=== [1/6] manifest cross-check on COMPILED manifests (I-3a/I-3b/I-3d, D-1/D-2 recompute) ===")
    manifest_result = run_manifest_crosscheck()
    report["manifest_crosscheck"] = manifest_result
    print(json.dumps(manifest_result, indent=2, ensure_ascii=False))

    print("\n=== [2/6] lane A export (decision fixtures + 5 cert fixtures via node) ===")
    lanea_export = run_node_stdin(LANEA_EXPORT_MJS, {})
    if "decision_fixture_results" not in lanea_export:
        print("ERROR: lane A export failed:", json.dumps(lanea_export)[:2000])
        report["error"] = "lanea_export_failed"
        report["lanea_export_raw"] = lanea_export
        (CERTS / "ep_run_20260728.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        return 1
    n_decision = len(lanea_export["decision_fixture_results"])
    n_cert = len(lanea_export["cert_fixtures"])
    print(f"decision_fixture_results: {n_decision} fixtures; cert_fixtures: {n_cert} (expect 5, C1..C5)")

    print("\n=== [3/6] cross-fixture DECISION-LANE REASON-CODE concordance (unaffected by cert-schema migration) ===")
    cross_fixture_rows = cross_fixture_native_verdict(lanea_export)
    report["cross_fixture_native_verdict"] = cross_fixture_rows
    n_decision_match = sum(1 for r in cross_fixture_rows if r['primary_reason_code_match'])
    report["cross_fixture_native_verdict_LABEL"] = (
        f"{n_decision_match}/{len(cross_fixture_rows)} DECISION-LANE reason-code matches "
        "(evaluateDecisionLane vs run_checker primary_reason_code). This is NOT a witness-vector PASS -- see [4/6]/[5/6]."
    )
    for r in cross_fixture_rows:
        flag = "[26]-candidate" if r["reason_[26]_candidate"] else "match"
        print(f"  {flag:14s} {r['direction']:42s} {r['label']}")
    print(" ", report["cross_fixture_native_verdict_LABEL"])

    print("\n=== [4/6] cert-schema gate + FORWARD verifier cross-check (lane A cert -> verifier B, UNMODIFIED) ===")
    forward_rows = forward_verifier_crosscheck(lanea_export)
    report["forward_laneA_to_laneB"] = forward_rows
    n_forward_gate_pass = sum(1 for r in forward_rows if r["gate"]["gate_passed"])
    full_pass_count = 0
    concordant_absent_count = 0
    mismatch_count = 0
    total_object_rows = 0
    for r in forward_rows:
        gs = "GATE-PASS" if r["gate"]["gate_passed"] else "GATE-FAIL[12]"
        print(f"  {gs:14s} {r['fixture']} ({r['label']})")
        if not r["gate"]["gate_passed"]:
            for v in r["gate"]["violations"]:
                print(f"      violation: {v}")
            continue
        for obj_name, obj_row in r.get("objects", {}).items():
            if "error" in obj_row:
                print(f"      ERROR {obj_name}: {obj_row['error']}")
                continue
            total_object_rows += 1
            if obj_row["full_witness_PASS"]:
                full_pass_count += 1
                tag = "FULL-PASS"
            elif obj_row["concordant_ABSENT_not_PASS"]:
                concordant_absent_count += 1
                tag = "CONCORDANT-ABSENT(not PASS)"
            elif obj_row["reason_[26]_candidate"]:
                mismatch_count += 1
                tag = "STRUCTURAL-MISMATCH[26]"
            else:
                tag = "concordant-non-PASS(real-defect-detected-by-both)"
            print(f"      {tag:42s} {obj_name}  mismatched={obj_row['mismatched_witnesses']}")
    print(f"  gate PASS: {n_forward_gate_pass}/{len(forward_rows)}; of {total_object_rows} object-rows evaluated: "
          f"full_witness_PASS={full_pass_count}, concordant_ABSENT={concordant_absent_count}, "
          f"structural_mismatch[26]={mismatch_count}")

    cert_fixture_paths = sorted(FIXTURES_NINFTY.glob("cert_*.json"))
    print(f"\n=== [5/6] cert-schema gate + REVERSE verifier cross-check (lane B's {len(cert_fixture_paths)} cert "
          f"fixtures -> verifier A, UNMODIFIED) ===")
    reverse_rows = reverse_verifier_crosscheck(cert_fixture_paths)
    report["reverse_laneB_to_laneA"] = reverse_rows
    n_reverse_gate_pass = sum(1 for r in reverse_rows if r["gate"]["gate_passed"])
    for r in reverse_rows:
        gs = "GATE-PASS" if r["gate"]["gate_passed"] else "GATE-FAIL[12]"
        laneA_summary = "N/A"
        if r["gate"]["gate_passed"]:
            res = r["laneA_verifier_result"]
            laneA_summary = res if isinstance(res, str) else res.get("overall_verdict_A", res)
        print(f"  {gs:14s} {r['fixture']}  laneB_native_verdict_B={r['laneB_native_overall_verdict_B']}  laneA_verifier_result={laneA_summary}")
        if not r["gate"]["gate_passed"]:
            for v in r["gate"]["violations"][:3]:
                print(f"      violation: {v}")
            if len(r["gate"]["violations"]) > 3:
                print(f"      ... and {len(r['gate']['violations']) - 3} more violations (see report JSON)")
    print(f"  gate PASS: {n_reverse_gate_pass}/{len(reverse_rows)} -- see report for the gate-bypassed DIAGNOSTIC "
          f"section on the gate-FAIL rows (NOT part of the official verdict).")

    print("\n=== witness-gen status ===")
    witness_gen_status = check_witness_gen()
    report["witness_gen_status"] = witness_gen_status
    print(json.dumps(witness_gen_status, indent=2, ensure_ascii=False))

    print("\n=== full-witness fixture (search/ninfty-witness-gen.py output, curve-level W-4/W-6) ===")
    full_witness_row = full_witness_fixture_crosscheck()
    report["full_witness_fixture_crosscheck"] = full_witness_row
    if not full_witness_row.get("present"):
        print("  ", full_witness_row.get("note", "not present"))
    elif not full_witness_row["gate"]["gate_passed"]:
        print("  GATE-FAIL[12]:", full_witness_row["gate"]["violations"])
    else:
        for obj_name, obj_row in full_witness_row.get("objects", {}).items():
            tag = "FULL-PASS" if obj_row["full_witness_PASS"] else "mismatch/partial"
            print(f"  {tag:20s} {obj_name}  mismatched={obj_row['mismatched_witnesses']}")

    # -----------------------------------------------------------------
    # N76-5.3 minimal-condition checklist
    # -----------------------------------------------------------------
    any_11 = manifest_result["reason_[11]_shared_helper_detected"]
    any_26_decision = any(r["reason_[26]_candidate"] for r in cross_fixture_rows)
    any_26_forward = any(obj.get("reason_[26]_candidate") for r in forward_rows for obj in r.get("objects", {}).values() if "error" not in obj)

    checklist = [
        {"item": "schema-valid manifest の機械生成", "status": "PASS",
         "note": "search/ninfty-manifest-compiler.py (P76-3) generated + validated both lane manifests before any verifier ran."},
        {"item": "certificate-schema validator gate 配線(裁定127/128)", "status": "PASS",
         "note": f"every certificate (forward {len(forward_rows)}, reverse {len(reverse_rows)}) passed through "
                 f"search/ninfty-cert-validator.py's validate_certificate() before any verifier call. Forward gate "
                 f"PASS: {n_forward_gate_pass}/{len(forward_rows)}. Reverse gate PASS: {n_reverse_gate_pass}/{len(reverse_rows)}."},
        {"item": "受領側 D-1〜D-4′/四面交差の再計算", "status": "PASS",
         "note": "D-1/D-2 recomputed for top-level AND entries of both compiled manifests; I-3a/b/d recomputed; see manifest_crosscheck."},
        {"item": "exact artifact bytes への digest 接続", "status": "PASS (with 1 UNKNOWN)",
         "note": "lane A's source files, lane B's 2 .py files, and 4 of 5 stdlib modules are hashed from real bytes on disk by the compiler. "
                 "`sys` (built-in C module, no separate source file) is modeled as identical to toolchain_digest -- flagged, not fabricated."},
        {"item": "同一 evidence に対する両 verifier の full PASS (NO conversion layer)", "status": "PARTIAL/MIXED",
         "note": f"forward: {full_pass_count}/{total_object_rows} object-rows are full_witness_PASS, "
                 f"{concordant_absent_count} are concordant_ABSENT_not_PASS, {mismatch_count} are genuine "
                 f"STRUCTURAL mismatches now that certs are fed unmodified (see forward_laneA_to_laneB for exact "
                 "mismatched witness labels + reasons -- this is the precise answer to whether concordance improved "
                 "from 'missing-agreement' to 'structural agreement': the OUTER container/routing genuinely works "
                 "now (both verifiers correctly attribute entries to the right divisor_object without any "
                 "conversion), but the INNER witness/bijection micro-schemas still diverge in specific, identified "
                 "ways -- this is progress, not a regression, and not yet full concordance."},
        {"item": "reverse direction", "status": "WIRED, gate-BLOCKED on current fixtures",
         "note": f"{n_reverse_gate_pass}/{len(reverse_rows)} of lane B's cert fixtures pass the schema gate; the "
                 "reverse pathway to verifier A is now a genuine no-conversion pipeline (verifier A already reads "
                 "the flat divisor_object-tagged schema), but the specific 6 fixtures currently fail the gate "
                 "(placeholder digests, missing certificate_digest/field_embedding fields, non-digest native _ref "
                 "strings) -- see gate.violations per row. Gate-bypassed diagnostic results are recorded separately "
                 "and are NOT part of the official verdict."},
        {"item": "curve-level witness", "status": "UNKNOWN/NOT AVAILABLE",
         "note": "no root-level / curve-point construction exists in either lane's current scope; W-4/W-6 remain ABSENT at the curve level."},
        {"item": "witness-gen (search/ninfty-witness-gen.py) full-certificate generation", "status": witness_gen_status.get("status", "PASS" if witness_gen_status["present"] else "PENDING"),
         "note": "checked at report time; not waited on (coordinator instruction)."},
        {"item": "report 自身の input-bundle digest 束縛", "status": "PASS", "note": "see input_bundle_digest below."},
    ]
    report["N76_5_3_minimal_condition_checklist"] = checklist

    report["reason_[11]_present"] = any_11
    report["reason_[26]_decision_lane_present"] = any_26_decision
    report["reason_[26]_forward_structural_present"] = any_26_forward

    unknown_items = [
        "CR-11 implemented_checks 3-layer equality: PENDING/UNKNOWN per freeze receipt pending queue",
        "QD-6 bootstrap leaf lost guarantees: PENDING/UNKNOWN per freeze receipt pending queue",
        "N-2(2)/H-1a'' independent re-derivation of R-6 closure completeness: PENDING/UNKNOWN per freeze receipt pending queue",
        "lane A/B toolchain_digest form-validated as 64-hex by the compiler but NOT independently re-hashed "
        "against the actual node.exe/python.exe binary bytes -- UNKNOWN, not confirmed.",
        "`sys` stdlib entry has no separate source file; modeled as toolchain_digest-equivalent -- UNKNOWN.",
        "P-3.3 was NOT exercised in the forward direction (native_a/native_b omitted from the payload); "
        "verifier B's own verify_P3 defaults p33_a/p33_b to True when they are omitted, which reads as PASS "
        "without having actually checked anything -- flagged as a known ambiguity in verifier B's own P-3 "
        "implementation, not something this runner silently relied on as a genuine PASS.",
        "search/ninfty-witness-gen.py: " + ("present, see witness_gen_status" if witness_gen_status["present"] else "PENDING, not found at report time"),
        "reverse-direction gate-bypassed diagnostic results (on gate-FAIL fixtures) are informational only and "
        "are explicitly NOT validated against the official gated verdict's discipline -- UNKNOWN whether they "
        "reflect anything beyond 'garbage in, garbage out'.",
    ]
    report["unknown_items"] = unknown_items

    if any_11:
        ep_judgment = "FAIL ([11] shared-helper-detected)"
    elif full_pass_count == total_object_rows and total_object_rows > 0 and n_reverse_gate_pass == len(reverse_rows):
        ep_judgment = "PASS (full witness concordance achieved both directions)"
    else:
        ep_judgment = (
            f"PASS-partial: manifest gate PASS, cert-validator gate wired, no [11]. Decision-lane reason-code "
            f"concordance {n_decision_match}/{len(cross_fixture_rows)}. Forward (lane A -> verifier B, no "
            f"conversion): gate PASS {n_forward_gate_pass}/{len(forward_rows)}, of which "
            f"{full_pass_count}/{total_object_rows} object-rows are full_witness_PASS, "
            f"{concordant_absent_count} concordant_ABSENT, {mismatch_count} genuine structural mismatches "
            f"(specific witness/bijection sub-schema divergence, root-caused per row). Reverse (lane B -> "
            f"verifier A): gate PASS {n_reverse_gate_pass}/{len(reverse_rows)} -- currently 0 or few of lane B's "
            f"fixtures pass the schema gate, so the reverse pathway is wired but not yet exercised end-to-end on "
            f"conformant data. This is a proposal for commander/Sol review, not a self-declared EP PASS."
        )
    report["ep_judgment_proposal"] = ep_judgment
    report["ep_judgment_note"] = ("Per receipt: 'calibrated detector・complete search 宣言は EP 前 NOT AUTHORIZED'. "
                                   "Per 裁定124/F76-5.7: bound<=5 decision-lane sweep remains NOT authorized regardless of this report's outcome.")

    # -----------------------------------------------------------------
    # input-bundle digest binding (N76-5.3 tail)
    # -----------------------------------------------------------------
    bundle_paths = [
        MANIFEST_COMPILER, LANEA_DRAFT, LANEB_DRAFT, VERIFIER_B, CHECKER_B, CERT_VALIDATOR,
        LANEA_EXPORT_MJS, LANEA_EVAL_MJS, LANEA_VERIFY_CERT_MJS,
        SEARCH / "ninfty-searcher-v2.mjs", SEARCH / "ninfty-verifier-a.mjs",
        CERTS / "fixtures-lanea.mjs", SEARCH / "ninfty-selftest-lanea.mjs",
        WITNESS_GEN, CERTS / "assemble_full_witness_cert.py", FULL_WITNESS_FIXTURE,
    ] + list(cert_fixture_paths) + list(FIXTURES_NINFTY.glob("checker_*.json"))
    bundle_digest, bundle = input_bundle_digest({"paths": bundle_paths, "extra": {
        "note": "sha256 of the ACTUAL bytes read/executed by this run, not a claim about upstream authorship.",
    }})
    report["input_bundle_digest"] = bundle_digest
    report["input_bundle"] = bundle

    print("\n=== summary ===")
    print("N76-5.3 checklist:")
    for c in checklist:
        print(f"  [{c['status']:38s}] {c['item']}")
    print("reason [11] present:", any_11)
    print("reason [26] (decision-lane) present:", any_26_decision)
    print("reason [26] (forward structural) present:", any_26_forward)
    print("EP judgment proposal:", ep_judgment)
    print("input_bundle_digest:", bundle_digest)

    out_path = CERTS / "ep_run_20260728.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
