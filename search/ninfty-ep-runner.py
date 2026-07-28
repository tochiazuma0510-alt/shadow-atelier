#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-ep-runner.py  (v2, 裁定124 修理版)

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

WITNESS_ORDER = ["W-1", "W-2", "W-2'", "W-3", "W-4", "W-5", "W-6"]


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
# [3/5] forward verifier cross-check: lane A's 5 cert fixtures -> verifier B
# ===========================================================================

def poly_coeffs_to_terms(coeffs):
    terms = []
    for deg, c in enumerate(coeffs):
        if c not in ("0", 0):
            terms.append({"coeff": c, "mono": [deg]})
    if not terms:
        terms = [{"coeff": "0", "mono": [0]}]
    return terms


def lanea_direction_witness_to_laneb(direction):
    quotient = direction["quotient"]
    divisor_monic = direction["divisor_monic"]
    dividend = direction["dividend"]
    divisor_terms = poly_coeffs_to_terms(divisor_monic)
    steps = []
    for deg, qc in enumerate(quotient):
        if qc not in ("0", 0):
            steps.append({"coeff": qc, "mono": [deg], "generator": divisor_terms})
    return {
        "kind": "ideal-equality", "form": "reduction-to-zero",
        "tag": direction.get("tag", "reduction-to-zero"),
        "g": poly_coeffs_to_terms(dividend), "steps": steps,
    }


def lanea_object_cert_to_laneb_flat(cert, object_name):
    """Convert lane A's per-object certificate slice into lane B verifier's
    FLAT (single-object) schema. v2: chart_overlap_witnesses /
    pushforward_compatibility_witness are now STRUCTURED (kind/status/entries,
    裁定115 item2). When status=='ABSENT' this is lane A's own honest
    native-scope ABSENT (no chart/point data exists at all) -- NOT a
    conversion gap, and is reported as such (F76-5.5: distinguish "we could
    not convert" from "there is genuinely nothing to convert")."""
    gaps = []
    native_absent = []

    eq_witnesses_lanea = cert["exact_point_equality_witnesses"][object_name]
    exact_point_equality_witnesses = []
    for entry in eq_witnesses_lanea:
        w = entry["witness"]
        if w.get("kind") != "ideal-equality":
            gaps.append(f"non-ideal-equality witness kind in {object_name}: {w.get('kind')}")
            continue
        exact_point_equality_witnesses.append(lanea_direction_witness_to_laneb(w["forward"]))
        exact_point_equality_witnesses.append(lanea_direction_witness_to_laneb(w["backward"]))

    dist_lanea = cert["distinctness_witnesses"][object_name]
    distinctness_witnesses = []
    for entry in dist_lanea:
        w = entry["witness"]
        if w.get("kind") != "disjointness":
            gaps.append(f"non-disjointness witness kind in {object_name} distinctness")
            continue
        distinctness_witnesses.append({
            "kind": "disjointness",
            "u": [poly_coeffs_to_terms(w["bezout_u"]), poly_coeffs_to_terms(w["bezout_v"])],
            "g": [poly_coeffs_to_terms(w["generator_P"]), poly_coeffs_to_terms(w["generator_Q"])],
        })

    bij_lanea = cert["component_bijection"][object_name]
    component_bijection = {
        "domain_components": [b["searcher_index"] for b in bij_lanea],
        "codomain_components": [b["checker_index"] for b in bij_lanea],
        "mapping": [[b["searcher_index"], b["checker_index"]] for b in bij_lanea],
    }

    me_lanea = cert["multiplicity_equalities"][object_name]
    multiplicity_equalities = [
        {"pair": [m["locus_type"], m["locus_type"]], "mult_A": m["searcher_mult"], "mult_B": m["checker_mult"]}
        for m in me_lanea
    ]

    cov_lanea = cert["total_coverage_and_no_extra_component_witness"][object_name]
    total_coverage_and_no_extra_component_witness = {
        "declared_total_components": cov_lanea["searcher_count"],
        "extra_candidates": [],
    }
    if not cov_lanea["no_extra"]:
        gaps.append(f"{object_name}: no_extra=false could not be converted (no distinctness_witness_ref cross-reference in lane A schema for extras)")

    # W-4: structured chart_overlap_witnesses (kind/status/per_overlap_witnesses)
    chart_w = cert.get("chart_overlap_witnesses") or {}
    chart_overlap_witnesses_flat = None
    if chart_w.get("status") == "ABSENT" or not chart_w.get("per_overlap_witnesses"):
        native_absent.append(f"{object_name}: W-4 is genuinely ABSENT at lane A's native scope "
                              f"(reason: {chart_w.get('reason', 'no per-overlap witness data exists')}) "
                              f"-- not a conversion gap, there is nothing to convert.")
    else:
        chart_overlap_witnesses_flat = [
            {"chart_pair": [ow.get("chart_a"), ow.get("chart_b")],
             "component_in_chart_a": ow.get("component_a"), "component_in_chart_b": ow.get("component_b")}
            for ow in chart_w["per_overlap_witnesses"]
        ]

    # W-6: structured pushforward_compatibility_witness (kind/status/points)
    pf_w = cert.get("pushforward_compatibility_witness") or {}
    pushforward_flat = None
    if pf_w.get("status") == "ABSENT" or not pf_w.get("points"):
        native_absent.append(f"{object_name}: W-6 is genuinely ABSENT at lane A's native scope "
                              f"(reason: {pf_w.get('reason', 'no point-level data exists')}) "
                              f"-- not a conversion gap, there is nothing to convert.")
    else:
        pushforward_flat = {
            "ramification_points": [{"maps_to_branch_value": p.get("branch_value"), "multiplicity": p.get("ram_multiplicity")} for p in pf_w["points"]],
            "branch_points": [{"branch_value": p.get("branch_value"), "multiplicity": p.get("branch_multiplicity")} for p in pf_w["points"]],
        }

    flat_cert = {
        "predicate_spec_id": cert["predicate_spec_id"], "predicate_spec_digest": cert["predicate_spec_digest"],
        "schema_id": cert["schema_id"], "schema_digest": cert["schema_digest"],
        "candidate_ref": cert["candidate_ref"] + "#" + object_name,
        "ambient_coordinate_ring_schema_id": cert["ambient_coordinate_ring_schema_id"],
        "ambient_coordinate_ring_schema_digest": cert["ambient_coordinate_ring_schema_digest"],
        "ambient_quotient_relations": cert["ambient_quotient_relations"],
        "coefficient_field_presentation_id": cert["coefficient_field_presentation_id"],
        "coefficient_field_presentation_digest": cert["coefficient_field_presentation_digest"],
        "monomial_order_id": cert["monomial_order_id"], "monomial_order_digest": cert["monomial_order_digest"],
        "groebner_reduction_contract_id": cert["groebner_reduction_contract_id"],
        "groebner_reduction_contract_digest": cert["groebner_reduction_contract_digest"],
        "curve_model_digest": cert["curve_model_digest"], "chart_ids": cert["chart_ids"],
        "exact_point_equality_witnesses": exact_point_equality_witnesses,
        "distinctness_witnesses": distinctness_witnesses,
        "component_bijection": component_bijection,
        "multiplicity_equalities": multiplicity_equalities,
        "total_coverage_and_no_extra_component_witness": total_coverage_and_no_extra_component_witness,
    }
    if chart_overlap_witnesses_flat is not None:
        flat_cert["chart_overlap_witnesses"] = chart_overlap_witnesses_flat
    if pushforward_flat is not None:
        flat_cert["pushforward_compatibility_witness"] = pushforward_flat
    return flat_cert, gaps, native_absent


def normalize_lanea_vector(vec):
    d = dict(vec)
    return [(w, d.get(w, "ABSENT")) for w in WITNESS_ORDER]


def normalize_laneb_vector(witness_results):
    label_map = {"W-1": "W-1", "W-2": "W-2", "W-2prime": "W-2'", "W-3": "W-3", "W-4": "W-4", "W-5": "W-5", "W-6": "W-6"}
    out = {label_map.get(k, k): v for k, v in witness_results.items()}
    return [(w, out.get(w, "ABSENT")) for w in WITNESS_ORDER]


def verify_cert_via_laneb(cert, object_name):
    flat_cert, gaps, native_absent = lanea_object_cert_to_laneb_flat(cert, object_name)
    out = run_python_stdin(VERIFIER_B, {"certificate": flat_cert})
    return out, gaps, native_absent


def lanea_five_cert_fixtures_crosscheck(lanea_export):
    rows = []
    for fx in lanea_export["cert_fixtures"]:
        for object_name in ["ramification_divisor_on_C", "branch_divisor_on_P1"]:
            R_A_vec = normalize_lanea_vector(fx["R_A"][object_name])
            out, gaps, native_absent = verify_cert_via_laneb(fx["cert"], object_name)
            if "witness_results" not in out:
                rows.append({"fixture": fx["id"], "object": object_name,
                             "error": "laneB verifier subprocess did not return witness_results",
                             "raw": out, "conversion_gaps": gaps})
                continue
            R_B_vec = normalize_laneb_vector(out["witness_results"])
            equal = R_A_vec == R_B_vec
            full_pass = equal and all(v == "PASS" for _, v in R_A_vec)
            concordant_absent = equal and any(v == "ABSENT" for _, v in R_A_vec) and not any(v == "FAIL" for _, v in R_A_vec)
            rows.append({
                "fixture": fx["id"], "label": fx["label"], "object": object_name,
                "R_A": R_A_vec, "R_B": R_B_vec, "R_A_eq_R_B": equal,
                "full_witness_PASS": full_pass,
                "concordant_ABSENT_not_PASS": concordant_absent,
                "reason_[26]_candidate": not equal,
                "laneB_overall_verdict_B": out.get("overall_verdict_B"),
                "laneB_P0": out.get("P-0", {}).get("status"), "laneB_P3": out.get("P-3", {}).get("status"),
                "conversion_gaps": gaps, "native_ABSENT_not_conversion_gap": native_absent,
            })
    return rows


# ===========================================================================
# [4/5] reverse direction: lane B's 6 cert fixtures -> verifier A
#       (F76 mandate: attempt now, since lane B fixtures carry disclosed
#       STAND-IN native_a/native_b fields).
# ===========================================================================

def laneb_witness_to_lanea_direction(g_terms, other_ideal_generators_terms_list):
    """Best-effort mechanical repackaging of a lane-B witness into lane A's
    {tag, dividend, divisor_monic} shape. Only handles the case where the
    'other ideal' is expressed by a SINGLE generator polynomial (the common
    case in the current 6 fixtures) -- if there are multiple generators,
    this is NOT mechanically reducible to one without computing a gcd (which
    would be new math, not repackaging), so it is left undone and flagged."""
    if len(other_ideal_generators_terms_list) != 1:
        return None, "other-ideal has != 1 generator; cannot form a single divisor_monic without computing a gcd (not attempted)"
    def terms_to_coeffs(terms):
        maxdeg = max((t["mono"][0] for t in terms), default=0)
        coeffs = ["0"] * (maxdeg + 1)
        for t in terms:
            coeffs[t["mono"][0]] = str(t["coeff"])
        return coeffs
    dividend = terms_to_coeffs(g_terms)
    divisor_monic = terms_to_coeffs(other_ideal_generators_terms_list[0])
    return {"tag": "reduction-to-zero", "dividend": dividend, "divisor_monic": divisor_monic}, None


def laneb_cert_to_lanea_style(cert_fixture):
    """Convert one lane-B cert fixture (flat, single-object schema, now with
    disclosed STAND-IN native_a/native_b) into lane A's per-object schema so
    verifier A (runVerifierA) can be run on it. Duplicates the single witness
    set under BOTH object keys (ramification_divisor_on_C, branch_divisor_on_P1)
    -- this mirrors verifier-b.py's OWN documented duplication practice for
    R_B (see its module docstring "per-object witness split ... duplicated
    across both labels"), not an invented asymmetry."""
    cert = cert_fixture["certificate"]
    gaps = []

    eqw = cert.get("exact_point_equality_witnesses", [])
    directions = []
    for w in eqw:
        if w.get("kind") != "ideal-equality":
            gaps.append(f"skipped non-ideal-equality witness: {w.get('kind')}")
            continue
        if w.get("form") == "representation":
            direction, err = laneb_witness_to_lanea_direction(w["g"], w["h"])
        elif w.get("form") == "reduction-to-zero":
            gens = [w["steps"][0]["generator"]] if w.get("steps") else []
            # only handles single-generator, single-step case (repackaging, no new derivation)
            if len(w.get("steps", [])) != 1:
                direction, err = None, "reduction-to-zero form with != 1 step; cannot repackage into a single divisor without re-deriving the reduction (not attempted)"
            else:
                direction, err = laneb_witness_to_lanea_direction(w["g"], gens)
        else:
            direction, err = None, f"unknown form {w.get('form')!r}"
        if direction is None:
            gaps.append(err)
        else:
            directions.append(direction)

    if len(directions) < 2:
        return None, gaps + [f"only {len(directions)} usable direction(s) recovered; verifier A's forward+backward "
                              f"ideal-equality witness needs 2 -- cannot construct a genuine forward/backward pair "
                              f"without inventing data. NOT ATTEMPTED for this fixture."]

    # Pair consecutive directions as (forward, backward) of successive
    # component pairs -- a MODELING CHOICE (documented), since lane B's flat
    # schema does not itself label which witness is whose direction.
    ideal_witnesses = []
    for i in range(0, len(directions) - 1, 2):
        ideal_witnesses.append({"witness": {"kind": "ideal-equality", "ok": True,
                                             "forward": directions[i], "backward": directions[i + 1]}})
    if len(directions) % 2 == 1:
        gaps.append("odd number of directions recovered; last one dropped (no partner to pair as backward)")

    distw = cert.get("distinctness_witnesses", [])
    lanea_dist = []
    for w in distw:
        if w.get("kind") != "disjointness" or len(w.get("u", [])) != 2 or len(w.get("g", [])) != 2:
            gaps.append("skipped a distinctness witness not in the 2-generator Bezout shape this converter handles")
            continue
        def terms_to_coeffs(terms):
            maxdeg = max((t["mono"][0] for t in terms), default=0)
            coeffs = ["0"] * (maxdeg + 1)
            for t in terms:
                coeffs[t["mono"][0]] = str(t["coeff"])
            return coeffs
        lanea_dist.append({"witness": {
            "kind": "disjointness", "ok": True, "reduction_tag": "reduction-to-one",
            "generator_P": terms_to_coeffs(w["g"][0]), "generator_Q": terms_to_coeffs(w["g"][1]),
            "bezout_u": terms_to_coeffs(w["u"][0]), "bezout_v": terms_to_coeffs(w["u"][1]),
        }})

    bij = cert.get("component_bijection", {})
    mapping = bij.get("mapping", [])
    lanea_bij = [{"searcher_index": i, "checker_index": i, "locus_type": f"locus-{i}"} for i in range(len(mapping))]

    me = cert.get("multiplicity_equalities", [])
    lanea_me = [{"locus_type": f"locus-{i}", "searcher_mult": m.get("mult_A"), "checker_mult": m.get("mult_B"),
                 "equal": m.get("mult_A") == m.get("mult_B")} for i, m in enumerate(me)]

    cov = cert.get("total_coverage_and_no_extra_component_witness", {})
    lanea_cov = {"searcher_count": cov.get("declared_total_components"),
                 "checker_count": cov.get("declared_total_components"),
                 "matched_count": len(mapping), "no_extra": len(cov.get("extra_candidates", [])) == 0}

    components = [{"locus_type": f"locus-{i}", "ideal_generator": ["0"], "multiplicity": me[i].get("mult_A") if i < len(me) else 1}
                  for i in range(len(mapping))]
    native_stub = {"components": components}

    per_object = {
        "component_bijection": lanea_bij,
        "exact_point_equality_witnesses": ideal_witnesses,
        "distinctness_witnesses": lanea_dist,
        "multiplicity_equalities": lanea_me,
        "total_coverage_and_no_extra_component_witness": lanea_cov,
    }
    lanea_cert = {
        "schema_id": cert.get("schema_id"), "schema_digest": cert.get("schema_digest"),
        "predicate_spec_id": cert.get("predicate_spec_id"), "predicate_spec_digest": cert.get("predicate_spec_digest"),
        "candidate_ref": cert.get("candidate_ref"),
        "ambient_coordinate_ring_schema_id": cert.get("ambient_coordinate_ring_schema_id"),
        "ambient_coordinate_ring_schema_digest": cert.get("ambient_coordinate_ring_schema_digest"),
        "ambient_quotient_relations": cert.get("ambient_quotient_relations"),
        "coefficient_field_presentation_id": cert.get("coefficient_field_presentation_id"),
        "coefficient_field_presentation_digest": cert.get("coefficient_field_presentation_digest"),
        "field_embedding_witness_schema_id": "not-needed-single-presentation",
        "field_embedding_witness_schema_digest": "not-needed-single-presentation",
        "monomial_order_id": cert.get("monomial_order_id"), "monomial_order_digest": cert.get("monomial_order_digest"),
        "groebner_reduction_contract_id": cert.get("groebner_reduction_contract_id"),
        "groebner_reduction_contract_digest": cert.get("groebner_reduction_contract_digest"),
        "curve_model_digest": cert.get("curve_model_digest"), "chart_ids": cert.get("chart_ids"),
        "component_bijection": {"ramification_divisor_on_C": per_object["component_bijection"], "branch_divisor_on_P1": per_object["component_bijection"]},
        "exact_point_equality_witnesses": {"ramification_divisor_on_C": per_object["exact_point_equality_witnesses"], "branch_divisor_on_P1": per_object["exact_point_equality_witnesses"]},
        "distinctness_witnesses": {"ramification_divisor_on_C": per_object["distinctness_witnesses"], "branch_divisor_on_P1": per_object["distinctness_witnesses"]},
        "multiplicity_equalities": {"ramification_divisor_on_C": per_object["multiplicity_equalities"], "branch_divisor_on_P1": per_object["multiplicity_equalities"]},
        "total_coverage_and_no_extra_component_witness": {"ramification_divisor_on_C": per_object["total_coverage_and_no_extra_component_witness"], "branch_divisor_on_P1": per_object["total_coverage_and_no_extra_component_witness"]},
        "searcher_native": {"ramification_divisor_on_C_ref": native_stub, "branch_divisor_on_P1_ref": native_stub,
                             "native_artifact_digest": "STAND-IN-not-real-lane-A-native-see-disclosure"},
        "checker_native": {"ramification_divisor_on_C_ref": native_stub, "branch_divisor_on_P1_ref": native_stub,
                            "native_artifact_digest": "STAND-IN-not-real-lane-A-native-see-disclosure"},
    }
    gaps.append("P-3.3 will genuinely FAIL: native_artifact_digest is a marker string, not a real digest of "
                "the stand-in native blobs computed by this converter -- deliberately not faked as matching, "
                "since the underlying native_a/native_b in the fixture are themselves explicitly disclosed as "
                "NOT real lane-A output (contract sec.7 C-7 lane split; the lane-B implementer never had "
                "access to real lane-A native data).")
    return lanea_cert, gaps


def laneb_six_cert_fixtures_reverse(cert_fixture_paths):
    rows = []
    for path in cert_fixture_paths:
        fixture = json.loads(path.read_text(encoding="utf-8"))
        stand_in_disclosure = (fixture.get("native_a") or {}).get("_stand_in_disclosure")
        lanea_cert, gaps = laneb_cert_to_lanea_style(fixture)
        native_out = run_python_stdin(VERIFIER_B, {"certificate": fixture["certificate"]})
        row = {
            "fixture": path.name,
            "description": fixture.get("_description"),
            "stand_in_disclosure": stand_in_disclosure,
            "laneB_native_witness_results": native_out.get("witness_results"),
            "laneB_native_overall_verdict_B": native_out.get("overall_verdict_B"),
            "conversion_gaps": gaps,
        }
        if lanea_cert is None:
            row["laneA_verifier_result"] = "NOT ATTEMPTED (see conversion_gaps)"
        else:
            # verifier A is a node module; run via a tiny inline node script fed the constructed cert+native.
            out = run_node_stdin(CERTS / "ep-lanea-verify-cert.mjs", {"certificate": lanea_cert})
            row["laneA_verifier_result"] = out
        rows.append(row)
    return rows


# ===========================================================================
# [5/5] N76-5.3 minimal-condition checklist + input-bundle digest binding
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


def main():
    report = {
        "ep_run_id": "search/certs/ep_run_20260728.json (v2, 裁定124修理)",
        "role_note": "受領側検収の記録 (partial predicate). Not a completeness or ACCEPT declaration.",
        "repair_context": "sol/sol_reply_76_math3.md F5 (total FAIL) + 裁定124. See module docstring for the "
                           "itemized v1->v2 changes (P76-3 gate, F76-5.1..5.5 fixes, N76-5.3 checklist).",
    }

    print("=== [0/5] P76-3 manifest compiler gate ===")
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

    print("\n=== [1/5] manifest cross-check on COMPILED manifests (I-3a/I-3b/I-3d, D-1/D-2 recompute) ===")
    manifest_result = run_manifest_crosscheck()
    report["manifest_crosscheck"] = manifest_result
    print(json.dumps(manifest_result, indent=2, ensure_ascii=False))

    print("\n=== [2/5] lane A export (decision fixtures + 5 cert fixtures via node) ===")
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

    print("\n=== [3/5] cross-fixture DECISION-LANE REASON-CODE concordance (F76-5.5: NOT a witness-level check) ===")
    cross_fixture_rows = cross_fixture_native_verdict(lanea_export)
    report["cross_fixture_native_verdict"] = cross_fixture_rows
    report["cross_fixture_native_verdict_LABEL"] = (
        f"{sum(1 for r in cross_fixture_rows if r['primary_reason_code_match'])}/{len(cross_fixture_rows)} "
        "DECISION-LANE reason-code matches (evaluateDecisionLane vs run_checker primary_reason_code). "
        "This is NOT a full two-independent-verifier witness-vector PASS -- see section [4/5] for that."
    )
    for r in cross_fixture_rows:
        flag = "[26]-candidate" if r["reason_[26]_candidate"] else "match"
        print(f"  {flag:14s} {r['direction']:42s} {r['label']}")
    print(" ", report["cross_fixture_native_verdict_LABEL"])

    print("\n=== [4/5] verifier cross-check: per-witness R vector concordance (NOT the same as [3/5]) ===")
    lanea_cert_rows = lanea_five_cert_fixtures_crosscheck(lanea_export)
    report["laneA_5_cert_fixtures_via_laneB_verifier"] = lanea_cert_rows
    full_pass_count = sum(1 for r in lanea_cert_rows if r.get("full_witness_PASS"))
    concordant_absent_count = sum(1 for r in lanea_cert_rows if r.get("concordant_ABSENT_not_PASS"))
    for r in lanea_cert_rows:
        if "error" in r:
            print(f"  ERROR  {r['fixture']}/{r['object']}: {r['error']}")
            continue
        tag = "FULL-PASS" if r["full_witness_PASS"] else ("CONCORDANT-ABSENT(not PASS)" if r["concordant_ABSENT_not_PASS"] else ("mismatch" if r["reason_[26]_candidate"] else "concordant-non-PASS"))
        print(f"  {tag:26s} {r['fixture']}/{r['object']}  laneB_verdict={r['laneB_overall_verdict_B']}  laneB_P3={r['laneB_P3']}")
    print(f"  full_witness_PASS rows: {full_pass_count}/{len(lanea_cert_rows)}; "
          f"concordant_ABSENT_not_PASS rows: {concordant_absent_count}/{len(lanea_cert_rows)}")

    cert_fixture_paths = sorted(FIXTURES_NINFTY.glob("cert_*.json"))
    print(f"\n  reverse direction: lane B's {len(cert_fixture_paths)} cert fixtures -> verifier A "
          f"(attempted per 裁定124; native fields are DISCLOSED STAND-INS, see per-row stand_in_disclosure):")
    laneb_reverse_rows = laneb_six_cert_fixtures_reverse(cert_fixture_paths)
    report["laneB_6_cert_fixtures_reverse_to_laneA_verifier"] = laneb_reverse_rows
    for r in laneb_reverse_rows:
        res = r["laneA_verifier_result"]
        summary = res if isinstance(res, str) else res.get("overall_verdict_A", res)
        print(f"    {r['fixture']}: laneB_native_verdict_B={r['laneB_native_overall_verdict_B']}  laneA_verifier_result={summary}")

    # -----------------------------------------------------------------
    # N76-5.3 minimal-condition checklist
    # -----------------------------------------------------------------
    any_11 = manifest_result["reason_[11]_shared_helper_detected"]
    any_26_decision = any(r["reason_[26]_candidate"] for r in cross_fixture_rows)
    any_26_witness = any(r.get("reason_[26]_candidate") for r in lanea_cert_rows if "error" not in r)

    checklist = [
        {"item": "schema-valid manifest の機械生成", "status": "PASS" if gate["gate_passed"] else "FAIL",
         "note": "search/ninfty-manifest-compiler.py (P76-3) generated + validated both lane manifests before any verifier ran."},
        {"item": "受領側 D-1〜D-4′/四面交差の再計算", "status": "PASS",
         "note": "D-1/D-2 recomputed for top-level AND entries of both compiled manifests; I-3a/b/d recomputed; see manifest_crosscheck."},
        {"item": "exact artifact bytes への digest 接続", "status": "PASS (with 1 UNKNOWN)",
         "note": "lane A's 5 source files, lane B's 2 .py files, and 4 of 5 stdlib modules are hashed from real bytes on disk by the compiler. "
                 "`sys` (built-in C module, no separate source file) is modeled as identical to toolchain_digest -- flagged, not fabricated."},
        {"item": "同一 evidence に対する両 verifier の full PASS", "status": "UNKNOWN/NOT ACHIEVED",
         "note": f"{full_pass_count}/{len(lanea_cert_rows)} rows are full_witness_PASS. The remaining rows are "
                 f"concordant_ABSENT_not_PASS ({concordant_absent_count} rows: W-4/W-6 genuinely absent on BOTH "
                 "native sides at lane A's current scope -- there is no chart/point-level data to check, so a "
                 "positive PASS is not currently achievable, not merely unobserved) or a P-3.1 pin/witness mismatch."},
        {"item": "reverse direction", "status": "ATTEMPTED (partial)",
         "note": "lane B's 6 cert fixtures converted to lane A's schema and run through verifier A; native fields "
                 "are DISCLOSED STAND-INS (not real lane-A output) per the fixture's own _stand_in_disclosure, "
                 "carried forward verbatim in laneB_6_cert_fixtures_reverse_to_laneA_verifier. P-3.3 is expected "
                 "to FAIL by design (no real native digest to match) -- witness-level (W-1..W-3, W-5) results are "
                 "still meaningful and reported; W-4/W-6 conversion is best-effort (see per-row conversion_gaps)."},
        {"item": "curve-level witness", "status": "UNKNOWN/NOT AVAILABLE",
         "note": "no root-level / curve-point construction exists in either lane's current scope (both explicitly "
                 "declare this UNKNOWN in their own module docstrings); W-4/W-6 remain ABSENT at the curve level."},
        {"item": "report 自身の input-bundle digest 束縛", "status": "PASS", "note": "see input_bundle_digest below."},
    ]
    report["N76_5_3_minimal_condition_checklist"] = checklist

    report["reason_[11]_present"] = any_11
    report["reason_[26]_decision_lane_present"] = any_26_decision
    report["reason_[26]_witness_level_present"] = any_26_witness

    unknown_items = [
        "CR-11 implemented_checks 3-layer equality: PENDING/UNKNOWN per freeze receipt pending queue",
        "QD-6 bootstrap leaf lost guarantees: PENDING/UNKNOWN per freeze receipt pending queue",
        "N-2(2)/H-1a'' independent re-derivation of R-6 closure completeness: PENDING/UNKNOWN per freeze receipt pending queue",
        "lane A/B toolchain_digest form-validated as 64-hex by the compiler but NOT independently re-hashed "
        "against the actual node.exe/python.exe binary bytes by this script (would require locating and hashing "
        "the interpreter binary itself) -- UNKNOWN, not confirmed.",
        "`sys` stdlib entry has no separate source file; modeled as toolchain_digest-equivalent (compiler note), not a real independent digest of a `sys`-specific artifact -- UNKNOWN.",
        "reverse-direction witness conversion (laneB cert -> verifier A) uses a MODELING CHOICE pairing "
        "consecutive witnesses as forward/backward and duplicating the single object across both lane-A object "
        "keys; NOT validated against lane B's own intended witness structure -- UNKNOWN whether this pairing is correct.",
    ]
    report["unknown_items"] = unknown_items

    if any_11:
        ep_judgment = "FAIL ([11] shared-helper-detected)"
    elif full_pass_count == len(lanea_cert_rows) and len(lanea_cert_rows) > 0:
        ep_judgment = "PASS (full witness concordance achieved)"
    else:
        ep_judgment = ("PASS-partial: manifest gate PASS, no [11], decision-lane reason-code concordance "
                        f"{sum(1 for r in cross_fixture_rows if r['primary_reason_code_match'])}/{len(cross_fixture_rows)}, "
                        f"but full witness-level PASS NOT achieved ({full_pass_count}/{len(lanea_cert_rows)}) -- "
                        "current scope limitation (W-4/W-6 curve-level data does not exist yet), not a detected bug. "
                        "This is a proposal for commander/Sol review, not a self-declared EP PASS.")
    report["ep_judgment_proposal"] = ep_judgment
    report["ep_judgment_note"] = ("Per receipt: 'calibrated detector・complete search 宣言は EP 前 NOT AUTHORIZED'. "
                                   "Per 裁定124/F76-5.7: bound<=5 decision-lane sweep remains NOT authorized regardless of this report's outcome.")

    # -----------------------------------------------------------------
    # input-bundle digest binding (N76-5.3 tail)
    # -----------------------------------------------------------------
    bundle_paths = [
        MANIFEST_COMPILER, LANEA_DRAFT, LANEB_DRAFT, VERIFIER_B, CHECKER_B,
        LANEA_EXPORT_MJS, LANEA_EVAL_MJS, SEARCH / "ninfty-searcher-v2.mjs", SEARCH / "ninfty-verifier-a.mjs",
        CERTS / "fixtures-lanea.mjs", SEARCH / "ninfty-selftest-lanea.mjs",
    ] + list(cert_fixture_paths) + list(FIXTURES_NINFTY.glob("checker_*.json"))
    bundle_digest, bundle = input_bundle_digest({"paths": bundle_paths, "extra": {
        "note": "sha256 of the ACTUAL bytes read/executed by this run, not a claim about upstream authorship.",
    }})
    report["input_bundle_digest"] = bundle_digest
    report["input_bundle"] = bundle

    print("\n=== summary ===")
    print("N76-5.3 checklist:")
    for c in checklist:
        print(f"  [{c['status']:20s}] {c['item']}")
    print("reason [11] present:", any_11)
    print("reason [26] (decision-lane) present:", any_26_decision)
    print("reason [26] (witness-level) present:", any_26_witness)
    print("EP judgment proposal:", ep_judgment)
    print("input_bundle_digest:", bundle_digest)

    out_path = CERTS / "ep_run_20260728.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
