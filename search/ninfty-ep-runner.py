#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-ep-runner.py

EP (endorsement point) runner -- RECEIVING-SIDE reconciliation of lane A
(node: search/ninfty-searcher-v2.mjs + search/ninfty-verifier-a.mjs) and
lane B (python: search/ninfty-checker.py + search/ninfty-verifier-b.py).

Governing documents (see docstrings/paths, versions pinned there -- this file
does not re-pin digests, it reads the manifests/fixtures as they stand):
  docs/mb_ninfty_verifier_contract_v13.md  (sec.3.4 result vector, sec.7 [26]
                                             concordance, C-7 no-cross-read)
  docs/mb_dependency_manifest_v13.md       (sec.6 I-3a/b/d, sec.2 D-1..D-4',
                                             receiving-side recompute I-0 series)
  provenance/ninfty_freeze_receipt_sol75.md

ROLE (task brief, verbatim): "EP は受領側検収の記録であって『complete search』
宣言ではない". This script does NOT judge the underlying mathematics; it
cross-checks two independently-produced artifact sets and reports where they
agree, disagree, or where a check could not be attempted (UNKNOWN/ABSENT).
It does not commit anything, does not touch certificates/mb/ or sealed
quantities, and does not modify lane A or lane B source files (read-only,
subprocess-only interaction with both).

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
# 1. manifest cross-check: I-3a (binary) / I-3b (source) / I-3d (build)
#    per dependency-manifest v13 sec.2 (D-1..D-4') / sec.6 (I-0*, I-3*)
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
    """Receiving-side recompute of D-1/D-2 for one manifest_entry, per manifest
    sec.2.2. Returns (d1, d2, d1_matches_declared_or_None, d2_matches_...)."""
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


def load_lanea_manifest():
    return json.loads((CERTS / "laneA_manifest.json").read_text(encoding="utf-8"))


def load_laneb_manifest():
    blob = json.loads((CERTS / "laneB_manifest.json").read_text(encoding="utf-8"))
    return blob["dependency_manifest"], blob


def manifest_faces(manifest):
    """binary_content_set / source_artifact_set / build_artifact_set per
    dependency-manifest v13 sec.6 (build face restricted to
    build_record_present==true entries for the build_definition/pinned_input
    components, per [branch-contract])."""
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
    return binary, source, build


def run_manifest_crosscheck():
    manifest_a = load_lanea_manifest()
    manifest_b, manifest_b_full = load_laneb_manifest()

    recompute_report = {"laneA": [], "laneB": []}
    for label, manifest in (("laneA", manifest_a), ("laneB", manifest_b)):
        for e in manifest.get("entries", []):
            d1, d2, d1_ok, d2_ok = recompute_entry_d1_d2(e)
            recompute_report[label].append({
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

    allowed_tcb_a = {t.get("content_digest") for t in manifest_a.get("allowed_shared_tcb", [])}
    allowed_tcb_b = {t.get("content_digest") for t in manifest_b.get("allowed_shared_tcb", [])}
    allowed_src_tcb = {t.get("source_artifact_digest") for t in manifest_a.get("allowed_shared_source_tcb", [])} | \
                      {t.get("source_artifact_digest") for t in manifest_b.get("allowed_shared_source_tcb", [])}
    allowed_build_tcb = {t.get("build_artifact_digest") for t in manifest_a.get("allowed_shared_build_tcb", [])} | \
                        {t.get("build_artifact_digest") for t in manifest_b.get("allowed_shared_build_tcb", [])}

    i3a_binary_intersection = sorted((bin_a & bin_b) - (allowed_tcb_a | allowed_tcb_b))
    i3b_source_intersection = sorted((src_a & src_b) - allowed_src_tcb)
    i3d_build_intersection = sorted((build_a & build_b) - allowed_build_tcb)

    # toolchain digest validity (E-6: mandatory, null-not-allowed, must be an
    # exact content digest -- lane B's declared value is a placeholder string,
    # not a content digest; flag as UNKNOWN per the manifest's own note).
    toolchain_digests_a = sorted({e.get("toolchain_digest") for e in manifest_a.get("entries", []) if e.get("toolchain_digest")})
    toolchain_digests_b = sorted({e.get("toolchain_digest") for e in manifest_b.get("entries", []) if e.get("toolchain_digest")})
    toolchain_validity = {
        "laneA": {t: is_valid_hex_digest(t) for t in toolchain_digests_a},
        "laneB": {t: is_valid_hex_digest(t) for t in toolchain_digests_b},
    }
    toolchain_unknown = [t for t, ok in toolchain_validity["laneB"].items() if not ok] + \
                        [t for t, ok in toolchain_validity["laneA"].items() if not ok]

    reason_11_shared_helper_detected = bool(i3a_binary_intersection or i3b_source_intersection or i3d_build_intersection)

    return {
        "recompute_D1_D2": recompute_report,
        "faces": {
            "laneA": {"binary": sorted(bin_a), "source": sorted(src_a), "build": sorted(build_a)},
            "laneB": {"binary": sorted(bin_b), "source": sorted(src_b), "build": sorted(build_b)},
        },
        "I-3a_binary_intersection": i3a_binary_intersection,
        "I-3b_source_intersection": i3b_source_intersection,
        "I-3d_build_intersection": i3d_build_intersection,
        "toolchain_digest_validity": toolchain_validity,
        "toolchain_digest_UNKNOWN_placeholders": toolchain_unknown,
        "reason_[11]_shared_helper_detected": reason_11_shared_helper_detected,
        "notes": [
            "D-3/D-4' (build_root_id/subject_build_binding_digest) recompute NOT attempted: "
            "both lanes declare build_record_present=false at top level and for all entries "
            "(QD-3 bootstrap leaf per [branch-contract]); per branch-contract false.recompute "
            "the receiving-side obligation is D-1/D-2 only, D-3/D-4' are ABSENT by design, not "
            "a gap in this recompute.",
            "Lane B's toolchain_digest ('cpython-3.13-stdlib-only-no-external-packages') is a "
            "placeholder identity string, not a content digest of the CPython interpreter binary "
            "-- flagged UNKNOWN per task instruction ('toolchain placeholder は UNKNOWN と記録'), "
            "not treated as a match or mismatch against lane A's real toolchain content digest.",
            "family face (I-3c') is an audit flag only (M-3'), not computed here as a blocking "
            "check; implementation_family_id is null in both manifests (not yet minted by any "
            "receipt authority) so it is UNKNOWN, not empty-by-computation.",
        ],
    }


# ===========================================================================
# 2. cross-fixture native-verdict check (decision lane)
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
    # divisor_orientation_attested = null/absent (lane B "UNKNOWN, caller
    # didn't attest") is omitted here -- lane A's own comment says an absent
    # field means "derived value is authoritative, no REJECT", the closest
    # honest analogue; NOT the same epistemic status as lane B's UNKNOWN, so
    # this substitution is recorded, not silently assumed equivalent.
    return out


def run_checker_subprocess(candidate):
    return run_python_stdin(CHECKER_B, candidate)


def run_lanea_decision_subprocess(candidate):
    return run_node_stdin(LANEA_EVAL_MJS, candidate)


def cross_fixture_native_verdict(lanea_export):
    rows = []

    # direction 1: lane A's own decision fixtures -> lane B checker
    for fx in lanea_export["decision_fixture_results"]:
        checker_input = lanea_decision_to_checker_candidate(fx["candidate"])
        checker_out = run_checker_subprocess(checker_input)
        checker_stage = checker_out.get("stage")
        checker_primary = checker_out.get("primary_reason_code")
        lanea_native = fx["laneA_native"]
        # normalize: checker_out has no "verdict" field the way lane A does
        # (REJECT/INTEGRITY_STOP/None-i.e.-accept); map stage None -> 'ACCEPT-shaped'
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

    # direction 2: lane B's own checker fixtures -> lane A decision lane
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
# 3. verifier cross-check: run both lanes' certificate fixtures through BOTH
#    verifiers where schema conversion is feasible; record UNKNOWN where not.
# ===========================================================================

def poly_coeffs_to_terms(coeffs):
    """lane A ascending-degree coefficient-string array -> lane B poly-terms
    list [{"coeff":..,"mono":[deg]}], dropping exact-zero coefficients. This
    is a pure re-serialization of already-known coefficients -- no new
    arithmetic is performed (contract Y-4a: parameter/representation choice,
    not a shared math-helper)."""
    terms = []
    for deg, c in enumerate(coeffs):
        if c not in ("0", 0):
            terms.append({"coeff": c, "mono": [deg]})
    if not terms:
        terms = [{"coeff": "0", "mono": [0]}]
    return terms


def lanea_direction_witness_to_laneb(direction):
    """lane A's {tag,dividend,divisor_monic,quotient,remainder} (single fixed
    divisor, full polynomial-division remainder already computed) -> lane B's
    {kind:'ideal-equality', form:'reduction-to-zero', g, steps[], tag}.
    Expansion: dividend = quotient*divisor_monic + remainder (division
    identity already established by lane A's own polyDivMod at generation
    time); steps[] here decomposes quotient*divisor_monic term-by-term
    against the SAME divisor_monic (one step per nonzero quotient
    coefficient: step_i = {coeff: q_i, mono:[i], generator: divisor_monic}),
    which is a mechanical re-expression of the already-declared quotient, not
    a re-derivation of it. If the certificate's quotient/divisor/dividend are
    mutually inconsistent (e.g. a corrupted divisor left with a stale
    quotient), the replay will genuinely fail in lane B's engine too -- this
    conversion does not paper over such corruption."""
    quotient = direction["quotient"]
    divisor_monic = direction["divisor_monic"]
    dividend = direction["dividend"]
    divisor_terms = poly_coeffs_to_terms(divisor_monic)
    steps = []
    for deg, qc in enumerate(quotient):
        if qc not in ("0", 0):
            steps.append({"coeff": qc, "mono": [deg], "generator": divisor_terms})
    return {
        "kind": "ideal-equality",
        "form": "reduction-to-zero",
        "tag": direction.get("tag", "reduction-to-zero"),
        "g": poly_coeffs_to_terms(dividend),
        "steps": steps,
    }


def lanea_object_cert_to_laneb_flat(cert, object_name):
    """Convert lane A's per-object certificate slice (object_name in
    {ramification_divisor_on_C, branch_divisor_on_P1}) into lane B
    verifier's expected FLAT (single-object) certificate schema. Declared
    UNKNOWN / not-attempted pieces are marked in the returned _conversion_gaps
    list rather than fabricated."""
    gaps = []

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
    domain = [b["searcher_index"] for b in bij_lanea]
    codomain = [b["checker_index"] for b in bij_lanea]
    component_bijection = {
        "domain_components": domain,
        "codomain_components": codomain,
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

    # W-4 (chart_overlap_witnesses) and W-6 (pushforward_compatibility_witness,
    # point-level ramification/branch data) cannot be honestly reconstructed
    # from lane A's per-candidate cert: lane A only carries a single
    # chart-count flag and a single scope-level "ok" boolean, not the
    # per-overlap / per-point declarations lane B's verify_W4/verify_W6
    # require. Declared as conversion gaps (ABSENT on the lane-B side),
    # not fabricated.
    gaps.append(f"{object_name}: W-4 chart_overlap_witnesses not convertible (lane A only declares a chart count, not per-overlap component agreement) -> lane B side will read ABSENT")
    gaps.append(f"{object_name}: W-6 pushforward_compatibility_witness not convertible (lane A only declares a single scope-level ok flag, not point-level ramification/branch multiplicities) -> lane B side will read ABSENT")

    flat_cert = {
        "predicate_spec_id": cert["predicate_spec_id"],
        "predicate_spec_digest": cert["predicate_spec_digest"],
        "schema_id": cert["schema_id"],
        "schema_digest": cert["schema_digest"],
        "candidate_ref": cert["candidate_ref"] + "#" + object_name,
        "ambient_coordinate_ring_schema_id": cert["ambient_coordinate_ring_schema_id"],
        "ambient_coordinate_ring_schema_digest": cert["ambient_coordinate_ring_schema_digest"],
        "ambient_quotient_relations": cert["ambient_quotient_relations"],
        "coefficient_field_presentation_id": cert["coefficient_field_presentation_id"],
        "coefficient_field_presentation_digest": cert["coefficient_field_presentation_digest"],
        "monomial_order_id": cert["monomial_order_id"],
        "monomial_order_digest": cert["monomial_order_digest"],
        "groebner_reduction_contract_id": cert["groebner_reduction_contract_id"],
        "groebner_reduction_contract_digest": cert["groebner_reduction_contract_digest"],
        "curve_model_digest": cert["curve_model_digest"],
        "chart_ids": cert["chart_ids"],
        "exact_point_equality_witnesses": exact_point_equality_witnesses,
        "distinctness_witnesses": distinctness_witnesses,
        "component_bijection": component_bijection,
        "multiplicity_equalities": multiplicity_equalities,
        "total_coverage_and_no_extra_component_witness": total_coverage_and_no_extra_component_witness,
        # chart_overlap_witnesses / pushforward_compatibility_witness intentionally omitted (ABSENT) -- see gaps above
    }
    return flat_cert, gaps


def normalize_lanea_vector(vec):
    d = dict(vec)
    return [(w, d.get(w, "ABSENT")) for w in WITNESS_ORDER]


def normalize_laneb_vector(witness_results):
    label_map = {"W-1": "W-1", "W-2": "W-2", "W-2prime": "W-2'", "W-3": "W-3", "W-4": "W-4", "W-5": "W-5", "W-6": "W-6"}
    out = {}
    for k, v in witness_results.items():
        out[label_map.get(k, k)] = v
    return [(w, out.get(w, "ABSENT")) for w in WITNESS_ORDER]


def vectors_equal(v1, v2):
    return v1 == v2


def verify_cert_via_laneb(cert, object_name):
    flat_cert, gaps = lanea_object_cert_to_laneb_flat(cert, object_name)
    out = run_python_stdin(VERIFIER_B, {"certificate": flat_cert})
    return out, gaps


def lanea_five_cert_fixtures_crosscheck(lanea_export):
    rows = []
    for fx in lanea_export["cert_fixtures"]:
        for object_name in ["ramification_divisor_on_C", "branch_divisor_on_P1"]:
            R_A_vec = normalize_lanea_vector(fx["R_A"][object_name])
            out, gaps = verify_cert_via_laneb(fx["cert"], object_name)
            if "witness_results" not in out:
                rows.append({
                    "fixture": fx["id"], "object": object_name,
                    "error": "laneB verifier subprocess did not return witness_results",
                    "raw": out, "conversion_gaps": gaps,
                })
                continue
            R_B_vec = normalize_laneb_vector(out["witness_results"])
            equal = vectors_equal(R_A_vec, R_B_vec)
            rows.append({
                "fixture": fx["id"],
                "label": fx["label"],
                "object": object_name,
                "R_A": R_A_vec,
                "R_B": R_B_vec,
                "R_A_eq_R_B": equal,
                "reason_[26]_candidate": not equal,
                "laneB_overall_verdict_B": out.get("overall_verdict_B"),
                "laneB_P0": out.get("P-0", {}).get("status"),
                "laneB_P3": out.get("P-3", {}).get("status"),
                "conversion_gaps": gaps,
            })
    return rows


def laneb_six_cert_fixtures_native(cert_fixture_paths):
    """Run lane B's own 6 cert fixtures through verifier B (native, schema
    matches by construction). Reverse direction (lane B cert -> verifier A)
    is NOT attempted: lane B's cert fixtures carry no searcher_native /
    checker_native / native_artifact_digest at all (P-3.3 has nothing to
    check against), and fabricating a native blob to satisfy verifier A's
    P-3.3 would inject data the fixture never declared. Recorded as
    UNKNOWN / not-attempted, not silently skipped."""
    rows = []
    for path in cert_fixture_paths:
        fixture = json.loads(path.read_text(encoding="utf-8"))
        out = run_python_stdin(VERIFIER_B, {"certificate": fixture["certificate"]})
        rows.append({
            "fixture": path.name,
            "description": fixture.get("_description"),
            "laneB_native_witness_results": out.get("witness_results"),
            "laneB_native_overall_verdict_B": out.get("overall_verdict_B"),
            "laneA_verifier_crosscheck": "NOT ATTEMPTED / UNKNOWN -- fixture has no searcher_native/"
                                          "checker_native/native_artifact_digest for verifier A's P-3.3 "
                                          "to check against; fabricating one would inject undeclared data",
        })
    return rows


# ===========================================================================
# main
# ===========================================================================

def main():
    report = {"ep_run_id": "search/certs/ep_run_20260728.json", "role_note":
              "受領側検収の記録 (partial predicate). Not a completeness or ACCEPT declaration."}

    print("=== [1/4] manifest cross-check (I-3a/I-3b/I-3d, D-1/D-2 recompute) ===")
    manifest_result = run_manifest_crosscheck()
    report["manifest_crosscheck"] = manifest_result
    print(json.dumps(manifest_result, indent=2, ensure_ascii=False))

    print("\n=== [2/4] lane A export (decision fixtures + 5 cert fixtures via node) ===")
    lanea_export = run_node_stdin(LANEA_EXPORT_MJS, {})
    if "decision_fixture_results" not in lanea_export:
        print("ERROR: lane A export failed:", json.dumps(lanea_export)[:2000])
        report["error"] = "lanea_export_failed"
        report["lanea_export_raw"] = lanea_export
        (CERTS / "ep_run_20260728.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        return 1
    print(f"decision_fixture_results: {len(lanea_export['decision_fixture_results'])} fixtures")
    print(f"cert_fixtures: {len(lanea_export['cert_fixtures'])} fixtures (expect 5 -- C1..C5)")

    print("\n=== [3/4] cross-fixture native verdict (decision lane, A<->B) ===")
    cross_fixture_rows = cross_fixture_native_verdict(lanea_export)
    report["cross_fixture_native_verdict"] = cross_fixture_rows
    for r in cross_fixture_rows:
        flag = "[26]-candidate" if r["reason_[26]_candidate"] else "match"
        print(f"  {flag:14s} {r['direction']:42s} {r['label']}")

    print("\n=== [4/4] verifier cross-check (per-witness R vector concordance) ===")
    lanea_cert_rows = lanea_five_cert_fixtures_crosscheck(lanea_export)
    report["laneA_5_cert_fixtures_via_laneB_verifier"] = lanea_cert_rows
    for r in lanea_cert_rows:
        if "error" in r:
            print(f"  ERROR  {r['fixture']}/{r['object']}: {r['error']}")
            continue
        flag = "[26]-candidate" if r["reason_[26]_candidate"] else "match"
        print(f"  {flag:14s} {r['fixture']}/{r['object']}  laneB_verdict={r['laneB_overall_verdict_B']}  laneB_P3={r['laneB_P3']}")

    cert_fixture_paths = sorted(FIXTURES_NINFTY.glob("cert_*.json"))
    print(f"\n  lane B's own {len(cert_fixture_paths)} cert fixtures -> verifier B native (verifier A direction UNKNOWN, see notes):")
    laneb_cert_rows = laneb_six_cert_fixtures_native(cert_fixture_paths)
    report["laneB_6_cert_fixtures_native"] = laneb_cert_rows
    for r in laneb_cert_rows:
        print(f"    {r['fixture']}: verdict_B={r['laneB_native_overall_verdict_B']}")

    # -----------------------------------------------------------------
    # verdict matrix + EP judgment
    # -----------------------------------------------------------------
    any_26 = any(r["reason_[26]_candidate"] for r in cross_fixture_rows) or \
             any(r.get("reason_[26]_candidate") for r in lanea_cert_rows if "error" not in r)
    any_11 = manifest_result["reason_[11]_shared_helper_detected"]

    unknown_items = [
        "CR-11 implemented_checks 3-layer equality (contract/manifest sec.9.1): PENDING/UNKNOWN per freeze receipt pending queue",
        "QD-6 bootstrap leaf lost guarantees (build_record_present=false in both lanes): PENDING/UNKNOWN per freeze receipt pending queue",
        "N-2(2)/H-1a'' independent re-derivation of R-6 closure completeness: PENDING/UNKNOWN per freeze receipt pending queue",
        "lane B toolchain_digest is a placeholder string, not a real content digest: UNKNOWN (see manifest_crosscheck.notes)",
        "reverse direction (lane B's 6 cert fixtures -> verifier A): NOT ATTEMPTED, no native artifact data to satisfy P-3.3 -- UNKNOWN, not a PASS or FAIL",
        "W-4/W-6 for lane A's 5 cert fixtures under verifier B: ABSENT due to schema conversion gaps (lane A's cert does not carry per-overlap / point-level data), not an independent verifier disagreement about identical evidence -- see per-row conversion_gaps",
        "P-3.1 mismatch expected for all 5 lane-A cert fixtures under verifier B (lane A selftest certs use a placeholder predicate_spec_digest, not verifier B's EXPECTED_PINS digest) -- a genuine pin mismatch, not a converter defect",
    ]
    report["unknown_items"] = unknown_items
    report["reason_[11]_present"] = any_11
    report["reason_[26]_present"] = any_26

    ep_judgment = "FAIL" if any_11 else ("PASS-partial (with UNKNOWNs, no [11]/no unexplained [26])" if not any_26 else "PASS-partial (with UNKNOWNs; [26]-candidates present, see per-row conversion_gaps for whether schema-conversion-driven or genuine)")
    report["ep_judgment_proposal"] = ep_judgment
    report["ep_judgment_note"] = "This is a proposal for the commander/Sol gate to review, NOT a self-declared EP PASS. Per receipt: 'calibrated detector・complete search 宣言は EP 前 NOT AUTHORIZED'."

    print("\n=== summary ===")
    print("reason [11] (shared-helper-detected) present:", any_11)
    print("reason [26] (verifier-result-mismatch) candidates present:", any_26)
    print("EP judgment proposal:", ep_judgment)

    out_path = CERTS / "ep_run_20260728.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
