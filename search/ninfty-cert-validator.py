#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-cert-validator.py

Certificate-schema validator GATE (裁定127/128), same pattern as P76-3's
search/ninfty-manifest-compiler.py: a small, standalone receiving-side check
that runs BEFORE a divisor_equality_certificate is allowed to reach either
verifier. If the gate fails, the certificate is stopped with a
`digest-mismatch [12]`-equivalent verdict and MUST NOT be passed to
verifier A / verifier B.

Conformance target (task brief, verbatim):
  "準拠先 = spec v18 §4.1 の明文 + docs/notes/cert_shape_interpretation_v1.md
  (暫定解釈 v1)の界面。"

docs/notes/cert_shape_interpretation_v1.md (状態: interpretation/candidate,
Sol確認待ち, 裁定128) fixes 5 points for the 7 witness fields the frozen
spec v18 sec.4.1 is silent on:
  1. FLAT array + per-entry `divisor_object` tag (values are the spec's own
     literal tokens `ramification_divisor_on_C_ref` / `branch_divisor_on_P1_ref`).
     No object-keyed nesting.
  2. chart_ids = array of string ids.
  3. `_ref` fields: digest reference is the primary meaning; inline
     materialization is optional (may coexist; on conflict the digest wins).
  4. Singular-noun witnesses (`total_coverage_and_no_extra_component_witness`,
     `pushforward_compatibility_witness`) are ALSO 2-entry arrays (one per
     object), consistent with the other 5 fields -- NOT a special case.
  5. Missing/malformed witness fields are read, receiving-side, as an empty
     array -> the EXISTING "0 entries = ABSENT" branch (no exception raised,
     no fail-open promotion to PASS). ABSENT != FAIL != PASS is preserved.

This validator implements checks (task brief, verbatim):
  - 必須スカラー欄の実在と 64-hex (required scalar fields exist and are exact
    64-hex digests, except the one lane-A-documented exception:
    native_schema_digest, which is explicitly allowed to be null pending
    receipt-time pinning -- flagged UNKNOWN, not PASS, not a violation).
  - witness 7 field のフラット配列形状 と divisor_object タグの正当値
    (all 7 witness fields must be a flat list; every entry must carry
    divisor_object in {ramification_divisor_on_C_ref, branch_divisor_on_P1_ref}).
  - native object の形 (searcher_native / checker_native: native_artifact_digest
    present + 64-hex; the two *_ref fields present, either as an inline
    {components:[...]} object or a bare digest string per item 3).
  - 欠落キーの扱い (ABSENT は明示 status のみ・null 禁止): if a witness field
    is missing or not a list, this validator does NOT raise and does NOT
    treat it as PASS -- it records `fallback_to_empty_array` (item 5) as an
    observation, and separately checks that no field anywhere carries an
    explicit `null` where an ABSENT/status marker was structurally required
    (null is a bare falsy value, not a status -- forbidden by name).

Any violation -> `gate_passed=False`, verdict `digest-mismatch [12]`
(mirrors contract sec.5.2's routing table entry for digest-mismatch), and
the caller must not invoke a verifier on this certificate.

Usage:
  python search/ninfty-cert-validator.py <path-to-cert-json-or-export-sample>
  python search/ninfty-cert-validator.py -            (reads JSON from stdin)
  python search/ninfty-cert-validator.py --apply-samples   (applies to the
    known current export samples/fixtures and prints a summary table)

The input JSON may be either a bare `divisor_equality_certificate` object, or
a wrapper object with a `.certificate` key (as in laneA_ep_export_sample.json)
or a `{"certificate": {...}}` payload (as in search/fixtures/ninfty/*.json).
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SEARCH = ROOT / "search"
CERTS = SEARCH / "certs"
FIXTURES_NINFTY = SEARCH / "fixtures" / "ninfty"

HEX64 = None
import re
HEX64 = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)

DIVISOR_OBJECT_VALUES = {"ramification_divisor_on_C_ref", "branch_divisor_on_P1_ref"}

# --- required scalar fields (spec v18 sec.4.1 literal + governing pins) ----
# name -> (nullable_documented_exception: bool)
REQUIRED_SCALAR_DIGESTS = {
    "predicate_spec_digest": False,
    "schema_digest": False,
    "curve_model_digest": False,
    "ambient_coordinate_ring_schema_digest": False,
    "coefficient_field_presentation_digest": False,
    "field_embedding_witness_schema_digest": False,
    "monomial_order_digest": False,
    "groebner_reduction_contract_digest": False,
    "certificate_digest": False,
}
REQUIRED_SCALAR_IDS = [
    "predicate_spec_id", "schema_id", "candidate_ref",
    "ambient_coordinate_ring_schema_id", "coefficient_field_presentation_id",
    "field_embedding_witness_schema_id", "monomial_order_id", "groebner_reduction_contract_id",
]

# the 7 witness fields spec v18 sec.4.1 leaves silent (interpretation v1 sec."裁定した形状")
SEVEN_WITNESS_FIELDS = [
    "component_bijection",
    "exact_point_equality_witnesses",
    "distinctness_witnesses",
    "multiplicity_equalities",
    "chart_overlap_witnesses",
    "total_coverage_and_no_extra_component_witness",
    "pushforward_compatibility_witness",
]


def unwrap_certificate(payload):
    """Accept a bare certificate, or a wrapper with .certificate, or the
    laneA_ep_export_sample.json shape."""
    if isinstance(payload, dict) and "certificate" in payload and isinstance(payload["certificate"], dict):
        return payload["certificate"]
    return payload


def validate_certificate(cert):
    """Returns (gate_passed, violations[], unknowns[], observations[])."""
    violations = []
    unknowns = []
    observations = []

    if not isinstance(cert, dict):
        return False, ["certificate payload is not a JSON object"], [], []

    # --- required scalar id fields: must exist and be non-empty strings ---
    for f in REQUIRED_SCALAR_IDS:
        v = cert.get(f, "__MISSING__")
        if v == "__MISSING__":
            violations.append(f"[schema] required id field {f!r} is missing")
        elif not isinstance(v, str) or v == "":
            violations.append(f"[schema] required id field {f!r} is not a non-empty string (got {v!r})")

    # --- required scalar digest fields: must exist, non-null, exact 64-hex ---
    for f, _ in REQUIRED_SCALAR_DIGESTS.items():
        v = cert.get(f, "__MISSING__")
        if v == "__MISSING__":
            violations.append(f"[64-hex] required digest field {f!r} is missing")
        elif v is None:
            violations.append(f"[64-hex] required digest field {f!r} is explicit null (ABSENT must use a "
                               f"status marker, not null; and this field has no documented ABSENT-null exception)")
        elif not isinstance(v, str) or not HEX64.match(v):
            violations.append(f"[64-hex] required digest field {f!r} = {v!r} is not an exact 64-hex digest")

    # --- chart_ids: array of string ids (interpretation item 2) -----------
    chart_ids = cert.get("chart_ids", "__MISSING__")
    if chart_ids == "__MISSING__":
        violations.append("[schema] chart_ids is missing")
    elif not isinstance(chart_ids, list) or not all(isinstance(x, str) and x for x in chart_ids):
        violations.append(f"[interp-2] chart_ids must be an array of non-empty strings, got {chart_ids!r}")

    # --- native objects: searcher_native / checker_native ------------------
    for side in ("searcher_native", "checker_native"):
        nat = cert.get(side, "__MISSING__")
        if nat == "__MISSING__" or not isinstance(nat, dict):
            violations.append(f"[schema] {side} is missing or not an object")
            continue
        nad = nat.get("native_artifact_digest", "__MISSING__")
        if nad == "__MISSING__" or nad is None:
            violations.append(f"[64-hex] {side}.native_artifact_digest is missing/null")
        elif not isinstance(nad, str) or not HEX64.match(nad):
            violations.append(f"[64-hex] {side}.native_artifact_digest = {nad!r} is not exact 64-hex")
        # native_schema_digest: DOCUMENTED exception -- null allowed pending
        # receipt-time pinning (lane A's own comment); flagged UNKNOWN, not FAIL.
        nsd = nat.get("native_schema_digest", "__MISSING__")
        if nsd == "__MISSING__":
            violations.append(f"[schema] {side}.native_schema_digest key is missing entirely "
                               f"(must be present, even if null pending receipt pin)")
        elif nsd is None:
            unknowns.append(f"{side}.native_schema_digest is null -- documented exception (pending receipt-time "
                             f"pinning), recorded as UNKNOWN, not a violation and not a PASS.")
        elif not (isinstance(nsd, str) and HEX64.match(nsd)):
            violations.append(f"[64-hex] {side}.native_schema_digest = {nsd!r} present but not exact 64-hex")
        # *_ref fields: item 3, digest-reference primary, inline optional.
        for ref_name in ("ramification_divisor_on_C_ref", "branch_divisor_on_P1_ref"):
            refval = nat.get(ref_name, "__MISSING__")
            if refval == "__MISSING__":
                violations.append(f"[schema] {side}.{ref_name} is missing")
            elif refval is None:
                violations.append(f"[interp-3] {side}.{ref_name} is explicit null (must be either an inline "
                                   f"object or a digest-reference string, never null)")
            elif isinstance(refval, dict):
                if "components" not in refval or not isinstance(refval.get("components"), list):
                    violations.append(f"[schema] {side}.{ref_name} inline object missing a 'components' array")
            elif isinstance(refval, str):
                if not HEX64.match(refval):
                    violations.append(f"[interp-3] {side}.{ref_name} is a bare string but not a 64-hex digest "
                                       f"reference: {refval!r}")
            else:
                violations.append(f"[schema] {side}.{ref_name} has an unrecognized type {type(refval).__name__}")

    # --- the 7 witness fields: flat array + divisor_object tag -------------
    #
    # CORRECTED (this validator's own self-audit against lane B's now-live
    # verifier-b.py, which is the actual second implementation of this same
    # interface): interpretation item 4 names ONLY
    # total_coverage_and_no_extra_component_witness and
    # pushforward_compatibility_witness as "also 2-entry array" -- NOT
    # chart_overlap_witnesses (a PLURAL name, validated as a many-tagged-
    # entries field by lane B's own verify_W4/_check_plural_witness). An
    # earlier version of this validator incorrectly grouped chart_overlap
    # with the two singular-noun fields and FAILED lane A's genuinely
    # conformant certificates on that basis -- self-corrected here.
    for field in SEVEN_WITNESS_FIELDS:
        v = cert.get(field, "__MISSING__")
        if v == "__MISSING__":
            observations.append(f"[interp-5] {field} key missing -- receiving side treats as ABSENT/[] "
                                 f"(fallback_to_empty_array), not a hard violation, not promoted to PASS")
            continue
        if v is None:
            violations.append(f"[interp-5] {field} is explicit null (ABSENT must be an empty array or a "
                               f"structured status marker, never a bare null)")
            continue
        if not isinstance(v, list):
            # MIRRORS lane B's own _coerce_to_list (search/ninfty-verifier-b.py):
            # ANY non-list value for one of these 7 fields is coerced to []
            # (-> ABSENT for both objects) by the second live implementation
            # of this same interface -- not a hard verifier-side rejection.
            # This validator follows that same tolerance rather than failing
            # a shape lane B itself accepts. A structured {status:...} object
            # (lane A's current pre-2-entry-array form for
            # chart_overlap_witnesses/pushforward_compatibility_witness) is
            # recorded as an observation (migration-in-progress marker, not
            # yet item 4's 2-entry array -- itself one of the 4 points
            # cert_shape_interpretation_v1.md defers to Sol confirmation).
            # The ONLY hard violation here is a fake ABSENT marker: a dict
            # that names a 'status' key but sets it to null.
            if isinstance(v, dict) and "status" in v:
                if v.get("status") is None:
                    violations.append(f"[abs-null] {field}.status is explicit null (ABSENT must be the string "
                                       f"'ABSENT', never null)")
                else:
                    observations.append(f"[interp-4-OPEN/coerced] {field} is a single structured-status object "
                                         f"(status={v.get('status')!r}), coerced to ABSENT by lane B's own "
                                         f"_coerce_to_list (not a FAIL there); not yet item 4's 2-entry array form "
                                         f"(open Sol-confirmation point d) -- observation, not a violation.")
            else:
                observations.append(f"[interp-5/coerced] {field} is not a list (got {type(v).__name__}); lane B's "
                                     f"own _coerce_to_list treats any non-list as [] (-> ABSENT), so this validator "
                                     f"does the same rather than being stricter than the live verifier -- recorded "
                                     f"as an observation.")
            continue
        # it IS a list: check flat shape (no nested dict-keyed-by-object) and tag validity
        for i, entry in enumerate(v):
            if not isinstance(entry, dict):
                violations.append(f"[schema] {field}[{i}] is not an object")
                continue
            tag = entry.get("divisor_object", "__MISSING__")
            if tag == "__MISSING__":
                violations.append(f"[interp-1] {field}[{i}] missing divisor_object tag")
            elif tag not in DIVISOR_OBJECT_VALUES:
                violations.append(f"[interp-1] {field}[{i}].divisor_object = {tag!r} is not one of "
                                   f"{sorted(DIVISOR_OBJECT_VALUES)}")
        if field == "total_coverage_and_no_extra_component_witness" and len(v) not in (0, 2):
            observations.append(f"[interp-4] {field} has {len(v)} entries, not the expected 2 (one per object) "
                                 f"-- not necessarily a violation (0 is ABSENT-equivalent per item 5) but flagged")

    gate_passed = len(violations) == 0
    return gate_passed, violations, unknowns, observations


def make_verdict(gate_passed, violations):
    if gate_passed:
        return {"verdict": "cert-schema-valid", "stop_before_verifier": False}
    return {"verdict": "INTEGRITY_STOP", "primary_reason_code": "digest-mismatch",
            "reason_code_number": 12, "stop_before_verifier": True,
            "note": "certificate-schema validator gate FAILED (裁定127/128) -- this certificate MUST NOT be "
                    "passed to verifier A or verifier B. Treated as [12] digest-mismatch-equivalent per "
                    "contract sec.5.2 routing (a structurally invalid certificate cannot support a meaningful "
                    "P-3.* re-check)."}


def apply_to_sample(label, payload):
    cert = unwrap_certificate(payload)
    gate_passed, violations, unknowns, observations = validate_certificate(cert)
    verdict = make_verdict(gate_passed, violations)
    return {
        "label": label, "gate_passed": gate_passed, "verdict": verdict,
        "violations": violations, "unknowns": unknowns, "observations": observations,
    }


def apply_samples():
    results = []

    p = CERTS / "laneA_ep_export_sample.json"
    if p.exists():
        results.append(apply_to_sample(str(p.relative_to(ROOT)), json.loads(p.read_text(encoding="utf-8"))))

    for p in sorted(FIXTURES_NINFTY.glob("cert_*.json")):
        results.append(apply_to_sample(str(p.relative_to(ROOT)), json.loads(p.read_text(encoding="utf-8"))))

    # live lane-A export (C1..C5), generated fresh via node -- exercises the
    # CURRENT generateCertificate() output, not a possibly-stale sample file.
    export_mjs = CERTS / "ep-lanea-export.mjs"
    if export_mjs.exists():
        import subprocess
        proc = subprocess.run(["node", str(export_mjs)], capture_output=True, text=True, cwd=str(ROOT),
                               encoding="utf-8", errors="replace")
        try:
            export = json.loads(proc.stdout.strip())
            for fx in export.get("cert_fixtures", []):
                results.append(apply_to_sample(f"live-export:{fx['id']}", {"certificate": fx["cert"]}))
        except json.JSONDecodeError:
            results.append({"label": "live-export", "gate_passed": False,
                             "violations": ["node export script did not return valid JSON"],
                             "raw_stdout": proc.stdout[:2000], "raw_stderr": proc.stderr[:2000]})

    return results


def main(argv):
    if argv and argv[0] == "--apply-samples":
        results = apply_samples()
        print(json.dumps(results, indent=2, ensure_ascii=False))
        print("\n=== summary ===")
        for r in results:
            status = "PASS" if r["gate_passed"] else f"FAIL ({len(r['violations'])} violations)"
            print(f"  {r['label']:40s} {status}")
        (CERTS / "cert_validator_sample_report.json").write_text(
            json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {CERTS / 'cert_validator_sample_report.json'}")
        return 0 if all(r["gate_passed"] for r in results) else 1

    if not argv:
        print("usage: python search/ninfty-cert-validator.py <path-or--> | --apply-samples", file=sys.stderr)
        return 2

    if argv[0] == "-":
        payload = json.load(sys.stdin)
    else:
        payload = json.loads(Path(argv[0]).read_text(encoding="utf-8"))

    cert = unwrap_certificate(payload)
    gate_passed, violations, unknowns, observations = validate_certificate(cert)
    verdict = make_verdict(gate_passed, violations)
    print(json.dumps({
        "gate_passed": gate_passed, "verdict": verdict,
        "violations": violations, "unknowns": unknowns, "observations": observations,
    }, indent=2, ensure_ascii=False))
    return 0 if gate_passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
