#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-cert-validator.py  (v3, 裁定139対応)

Certificate-schema validator GATE (裁定127/128/139), same pattern as P76-3's
search/ninfty-manifest-compiler.py: a small, standalone receiving-side check
that runs BEFORE a divisor_equality_certificate is allowed to reach either
verifier. If the gate fails, the certificate is stopped with a
`digest-mismatch [12]`-equivalent verdict (or, for MALFORMED input, a
provisional schema-invalid gate-stop -- see below) and MUST NOT be passed to
verifier A / verifier B.

Conformance target (裁定139, verbatim): "docs/notes/cert_shape_interpretation_v3.md"
(supersedes v1/v2 as the LIVE interface; v1/v2 kept as historical record).
v3 conditions implemented here:
  1. chart_ids: array of non-empty opaque strings (full resolution against the
     curve_model_digest's chart registry is NOT independently checkable from
     the certificate alone -- recorded as UNKNOWN, not assumed satisfied).
  2/7. W-1..W-5 (component_bijection, exact_point_equality_witnesses,
     distinctness_witnesses, multiplicity_equalities, chart_overlap_witnesses)
     keep the flat array + per-entry `divisor_object` tag (v1/v2, W-4 multiplicity
     unchanged from v2(l): strict exactly-1-entry-per-divisor_object, checked
     structurally here as an observation, not enforced as a hard count).
  2. W-6 (pushforward_compatibility_witness) is EXEMPTED from divisor_object
     tagging (条項2: "divisor_object 複製禁止") -- it is tagged instead by
     `native_side` in {searcher, checker}, one entry per side, each entry
     shaped {native_side, ramification_ref, branch_ref, map_ref, witness_ref}.
  3. `_ref` triple: {artifact_id, digest, (json_pointer | object_id)}. `inline`
     coexistence is allowed but its canonical digest (same canonical_serialize
     scheme used project-wide: UTF-8/sorted-keys/no-whitespace) MUST match the
     declared `digest` -- mismatch is an INTEGRITY_STOP [12] digest-mismatch,
     neither value silently preferred.
  4. total_coverage_and_no_extra_component_witness stays a normal
     divisor_object-tagged field (2 entries naturally, one per object) --
     pushforward's old "singular 2-entry" treatment is WITHDRAWN (moved to
     native_side, condition 2).
  5. ABSENT != MALFORMED (条項5, NEW distinction from v1's leniency):
       missing key, OR present as an explicit `[]`           -> ABSENT (observation)
       explicit `null`                                        -> MALFORMED (violation)
       present but not an array                               -> MALFORMED (violation)
       entry missing its tag (divisor_object / native_side)   -> MALFORMED (violation)
       entry with an unrecognized tag value                   -> MALFORMED (violation)
     MALFORMED is a fail-closed PARSE/SCHEMA-layer stop, distinct from a
     content-level ABSENT (evidence-insufficiency, which routes to [25] at the
     verifier layer, not here). The dedicated `schema-invalid` reason-code
     enum is still pending Sol confirmation (v3's own "Sol へ残す諮問"); until
     then this validator reports MALFORMED findings with an explicit
     `[MALFORMED]` tag and STILL fails the gate (stop_before_verifier=True),
     but keeps the code distinguishable in `violations[]` from digest/schema
     violations so a future enum can be slotted in without re-deriving which
     findings belong to it.
       NOTE: this supersedes this validator's OWN v1 self-correction, which
       mirrored lane B verifier's `_coerce_to_list` leniency (any non-list ->
       silently ABSENT). v3 is a deliberate interface tightening over that
       lenient behavior; this validator now enforces the NEW rule regardless
       of whether either lane's verifier has caught up yet (that gap, if any,
       is an EP finding to surface separately, not something for the gate to
       paper over).
  6. component_bijection "edge" form: entries are NOT required (yet) to carry
     `searcher_native_digest`/`checker_native_digest` (the v3 target shape) --
     the still-common index-based v2(g) shape ({divisor_object, searcher_index,
     checker_index, locus_type}) is tolerated as an observation (structural
     upgrade pending). What IS checked and WARNED on: any entry (or the field
     as a whole) carrying a self-declared summary list (`domain_components`,
     `codomain_components`, or a top-level `mapping` array) -- the pre-v1
     "authority is the producer's own summary" anti-pattern condition 6
     explicitly disclaims ("自己申告の domain/codomain リストを authority に
     しない").
  8. multiplicity_equalities field names (searcher_mult/checker_mult) and
     total_coverage_and_no_extra_component_witness field names
     (searcher_count/checker_count/matched_count/no_extra) unchanged from
     v2(j)/(k) -- checked as before (structural presence only, not exact key
     names -- see NOTE in code).

Any violation -> `gate_passed=False`; verdict is `digest-mismatch [12]` for
digest/schema violations, or a provisional MALFORMED/schema-invalid gate-stop
for condition-5 findings (both set `stop_before_verifier=True`).

Usage:
  python search/ninfty-cert-validator.py <path-to-cert-json-or-export-sample>
  python search/ninfty-cert-validator.py -            (reads JSON from stdin)
  python search/ninfty-cert-validator.py --apply-samples   (applies to the
    known current export samples/fixtures and prints a summary table)

The input JSON may be either a bare `divisor_equality_certificate` object, or
a wrapper object with a `.certificate` key (as in laneA_ep_export_sample.json
or search/certs/full_witness_fixture_01.json) or a `{"certificate": {...}}`
payload (as in search/fixtures/ninfty/*.json).
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import sys
from pathlib import Path

if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SEARCH = ROOT / "search"
CERTS = SEARCH / "certs"
FIXTURES_NINFTY = SEARCH / "fixtures" / "ninfty"

HEX64 = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)

DIVISOR_OBJECT_VALUES = {"ramification_divisor_on_C_ref", "branch_divisor_on_P1_ref"}
NATIVE_SIDE_VALUES = {"searcher", "checker"}
PUSHFORWARD_REF_KEYS = ["ramification_ref", "branch_ref", "map_ref", "witness_ref"]
BIJECTION_SELF_DECLARED_KEYS = ("domain_components", "codomain_components", "mapping")

# --- required scalar fields (spec v18 sec.4.1 literal + governing pins) ----
REQUIRED_SCALAR_DIGESTS = [
    "predicate_spec_digest", "schema_digest", "curve_model_digest",
    "ambient_coordinate_ring_schema_digest", "coefficient_field_presentation_digest",
    "field_embedding_witness_schema_digest", "monomial_order_digest",
    "groebner_reduction_contract_digest", "certificate_digest",
]
REQUIRED_SCALAR_IDS = [
    "predicate_spec_id", "schema_id", "candidate_ref",
    "ambient_coordinate_ring_schema_id", "coefficient_field_presentation_id",
    "field_embedding_witness_schema_id", "monomial_order_id", "groebner_reduction_contract_id",
]

# the 6 divisor_object-tagged witness fields (v3 条項2: W-6 pushforward is
# EXEMPT from divisor_object tagging -- it uses native_side, checked separately)
DIVISOR_OBJECT_WITNESS_FIELDS = [
    "component_bijection",
    "exact_point_equality_witnesses",
    "distinctness_witnesses",
    "multiplicity_equalities",
    "chart_overlap_witnesses",
    "total_coverage_and_no_extra_component_witness",
]
NATIVE_SIDE_WITNESS_FIELD = "pushforward_compatibility_witness"


def canonical_serialize(obj):
    """Project-wide canonical form: UTF-8, sorted keys, explicit array order,
    no whitespace -- same convention used by search/ninfty-ep-runner.py and
    search/ninfty-manifest-compiler.py. Confirmed by direct computation
    against search/certs/full_witness_fixture_01.json's own inline/digest
    pairs (see task report) before being relied on here for [12] checks."""
    def sort(x):
        if isinstance(x, list):
            return [sort(y) for y in x]
        if isinstance(x, dict):
            return {k: sort(x[k]) for k in sorted(x.keys())}
        return x
    return json.dumps(sort(obj), separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def validate_ref_triple(ref, label):
    """v3 条項3: _ref = {artifact_id, digest, (json_pointer | object_id)},
    inline optional but its canonical digest MUST match `digest` if present.
    Returns a list of violation strings (empty if the ref is well-formed)."""
    violations = []
    if not isinstance(ref, dict):
        return [f"[MALFORMED] {label} is not an object (_ref must be "
                f"{{artifact_id, digest, json_pointer|object_id}}), got {type(ref).__name__}"]
    artifact_id = ref.get("artifact_id")
    if not (isinstance(artifact_id, str) and artifact_id):
        violations.append(f"[schema] {label}.artifact_id missing or not a non-empty string")
    digest = ref.get("digest")
    digest_ok = isinstance(digest, str) and HEX64.match(digest)
    if not digest_ok:
        violations.append(f"[64-hex] {label}.digest = {digest!r} is not an exact 64-hex digest")
    has_pointer = isinstance(ref.get("json_pointer"), str) and ref.get("json_pointer")
    has_object_id = isinstance(ref.get("object_id"), str) and ref.get("object_id")
    if not (has_pointer or has_object_id):
        violations.append(f"[schema] {label} has neither json_pointer nor object_id "
                           f"(_ref requires exactly one)")
    if "inline" in ref and digest_ok:
        recomputed = sha256_of(ref["inline"])
        if recomputed != digest:
            violations.append(f"[12/digest-mismatch] {label}.inline canonical digest "
                               f"{recomputed} != declared digest {digest} (interpretation v3 "
                               f"条項3: integrity stop, neither value silently preferred)")
    return violations


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
    for f in REQUIRED_SCALAR_DIGESTS:
        v = cert.get(f, "__MISSING__")
        if v == "__MISSING__":
            violations.append(f"[64-hex] required digest field {f!r} is missing")
        elif v is None:
            violations.append(f"[64-hex] required digest field {f!r} is explicit null (ABSENT must use a "
                               f"status marker, not null; and this field has no documented ABSENT-null exception)")
        elif not isinstance(v, str) or not HEX64.match(v):
            violations.append(f"[64-hex] required digest field {f!r} = {v!r} is not an exact 64-hex digest")

    # --- chart_ids: array of non-empty opaque strings (v3 条項1) -----------
    chart_ids = cert.get("chart_ids", "__MISSING__")
    if chart_ids == "__MISSING__":
        violations.append("[schema] chart_ids is missing")
    elif not isinstance(chart_ids, list) or not chart_ids or not all(isinstance(x, str) and x for x in chart_ids):
        violations.append(f"[interp-1] chart_ids must be a non-empty array of non-empty strings, got {chart_ids!r}")
    else:
        unknowns.append("chart_ids 条項1 full requirement (each id resolves into the curve_model_digest's own "
                         "chart registry / individual chart digest, uniquely pinning coordinate ring + open set + "
                         "transition map) is NOT independently checkable from the certificate alone -- this "
                         "validator only checks the string-array SHAPE, not registry resolution. UNKNOWN, not "
                         "assumed satisfied.")

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
        # *_ref fields: v3 条項3 -- either a bare 64-hex digest-reference
        # string, OR a full {artifact_id, digest, json_pointer|object_id,
        # inline?} triple (as lane A's now-migrated generateCertificate()
        # produces). Both forms accepted; a dict form is checked with the
        # SAME validate_ref_triple used for W-6's ref fields, plus a
        # native-specific requirement that inline (if present) carries a
        # 'components' array.
        for ref_name in ("ramification_divisor_on_C_ref", "branch_divisor_on_P1_ref"):
            refval = nat.get(ref_name, "__MISSING__")
            if refval == "__MISSING__":
                violations.append(f"[schema] {side}.{ref_name} is missing")
            elif refval is None:
                violations.append(f"[MALFORMED] {side}.{ref_name} is explicit null (must be either an inline "
                                   f"_ref triple or a digest-reference string, never null)")
            elif isinstance(refval, dict):
                violations.extend(validate_ref_triple(refval, f"{side}.{ref_name}"))
                inline = refval.get("inline")
                if inline is not None and (not isinstance(inline, dict) or "components" not in inline
                                           or not isinstance(inline.get("components"), list)):
                    violations.append(f"[schema] {side}.{ref_name}.inline missing a 'components' array "
                                       f"(native _ref inline must carry the component list)")
            elif isinstance(refval, str):
                if not HEX64.match(refval):
                    violations.append(f"[interp-3] {side}.{ref_name} is a bare string but not a 64-hex digest "
                                       f"reference: {refval!r}")
            else:
                violations.append(f"[schema] {side}.{ref_name} has an unrecognized type {type(refval).__name__}")

    # --- the 6 divisor_object-tagged witness fields (v3 条項2/4/6/7/8) ------
    #
    # v3 条項5 (NEW, supersedes this validator's own v1 self-correction):
    # ABSENT (missing key, or explicit []) is now DISTINCT from MALFORMED
    # (null / non-array / missing-tag / unknown-tag). MALFORMED is a
    # fail-closed parse/schema-layer stop -- it does NOT get coerced to
    # ABSENT/[] the way this validator previously tolerated (mirroring lane
    # B's old _coerce_to_list leniency). That leniency is deliberately
    # withdrawn here: v3 is a stricter interface than v1/v2 on this point,
    # and the gate must reflect the CURRENT interpretation, not whichever
    # lane's verifier happens to still be lenient.
    for field in DIVISOR_OBJECT_WITNESS_FIELDS:
        v = cert.get(field, "__MISSING__")
        if v == "__MISSING__":
            observations.append(f"[ABSENT] {field} key missing -- ABSENT per v3 条項5 "
                                 f"(evidence-insufficiency, not a schema violation)")
            continue
        if isinstance(v, list) and len(v) == 0:
            observations.append(f"[ABSENT] {field} is an explicit empty array -- ABSENT per v3 条項5")
            continue
        if v is None:
            violations.append(f"[MALFORMED] {field} is explicit null --条項5: null is MALFORMED, "
                               f"NOT ABSENT (ABSENT is missing-key or explicit [] only)")
            continue
        if not isinstance(v, list):
            violations.append(f"[MALFORMED] {field} is not an array (got {type(v).__name__}) -- 条項5: "
                               f"a non-array value is MALFORMED, NOT silently coerced to ABSENT/[]")
            continue
        # it IS a non-empty list: check flat shape and divisor_object tag validity
        for i, entry in enumerate(v):
            if not isinstance(entry, dict):
                violations.append(f"[MALFORMED] {field}[{i}] is not an object")
                continue
            tag = entry.get("divisor_object", "__MISSING__")
            if tag == "__MISSING__":
                violations.append(f"[MALFORMED] {field}[{i}] missing divisor_object tag (条項5: "
                                   f"missing tag is MALFORMED, not silently dropped/ABSENT)")
            elif tag not in DIVISOR_OBJECT_VALUES:
                violations.append(f"[MALFORMED] {field}[{i}].divisor_object = {tag!r} is not one of "
                                   f"{sorted(DIVISOR_OBJECT_VALUES)} (unrecognized tag = MALFORMED)")
            # v3 条項6: component_bijection entries must not carry a
            # self-declared domain/codomain summary (the pre-v1 anti-pattern
            # condition 6 explicitly disclaims as non-authoritative).
            if field == "component_bijection":
                declared_keys = [k for k in BIJECTION_SELF_DECLARED_KEYS if k in entry]
                if declared_keys:
                    violations.append(f"[WARN/interp-6] component_bijection[{i}] carries self-declared "
                                       f"summary key(s) {declared_keys} -- interpretation v3 条項6: "
                                       f"'自己申告の domain/codomain リストを authority にしない'; the "
                                       f"receiving side must reconstruct component sets from the native "
                                       f"artifacts, not trust this list.")
                if not ({"searcher_native_digest", "checker_native_digest"} <= entry.keys()):
                    observations.append(f"[interp-6-OPEN] component_bijection[{i}] uses the index-based "
                                         f"v2(g) shape (searcher_index/checker_index/locus_type) rather "
                                         f"than v3's target 'edge' shape with searcher_native_digest/"
                                         f"checker_native_digest -- tolerated for now (structural upgrade "
                                         f"pending), not a hard violation.")
    # --- W-6 pushforward_compatibility_witness: native_side tag (v3 条項2) --
    pf_field = NATIVE_SIDE_WITNESS_FIELD
    v = cert.get(pf_field, "__MISSING__")
    if v == "__MISSING__":
        observations.append(f"[ABSENT] {pf_field} key missing -- ABSENT per v3 条項5")
    elif isinstance(v, list) and len(v) == 0:
        observations.append(f"[ABSENT] {pf_field} is an explicit empty array -- ABSENT per v3 条項5")
    elif v is None:
        violations.append(f"[MALFORMED] {pf_field} is explicit null -- 条項5: null is MALFORMED, not ABSENT")
    elif not isinstance(v, list):
        violations.append(f"[MALFORMED] {pf_field} is not an array (got {type(v).__name__})")
    else:
        seen_sides = set()
        for i, entry in enumerate(v):
            if not isinstance(entry, dict):
                violations.append(f"[MALFORMED] {pf_field}[{i}] is not an object")
                continue
            side = entry.get("native_side", "__MISSING__")
            if side == "__MISSING__":
                violations.append(f"[MALFORMED] {pf_field}[{i}] missing native_side tag (条項2: W-6 uses "
                                   f"native_side, NOT divisor_object)")
                continue
            if side not in NATIVE_SIDE_VALUES:
                violations.append(f"[MALFORMED] {pf_field}[{i}].native_side = {side!r} is not one of "
                                   f"{sorted(NATIVE_SIDE_VALUES)}")
                continue
            if side in seen_sides:
                violations.append(f"[schema] {pf_field}[{i}]: duplicate native_side={side!r} entry "
                                   f"(exactly one entry per side)")
            seen_sides.add(side)
            for key in PUSHFORWARD_REF_KEYS:
                refval = entry.get(key, "__MISSING__")
                if refval == "__MISSING__":
                    violations.append(f"[schema] {pf_field}[{i}] ({side}) missing required ref key {key!r}")
                    continue
                violations.extend(validate_ref_triple(refval, f"{pf_field}[{i}]({side}).{key}"))
        missing_sides = NATIVE_SIDE_VALUES - seen_sides
        if missing_sides:
            observations.append(f"[ABSENT] {pf_field} has no entry for native_side(s) {sorted(missing_sides)} "
                                 f"-- ABSENT for that side specifically, not a violation for the whole field")

    gate_passed = len(violations) == 0
    return gate_passed, violations, unknowns, observations


def make_verdict(gate_passed, violations):
    if gate_passed:
        return {"verdict": "cert-schema-valid", "stop_before_verifier": False}
    malformed = [v for v in violations if v.startswith("[MALFORMED]") or v.startswith("[WARN/interp-6]")]
    digest_or_schema = [v for v in violations if v not in malformed]
    if malformed and not digest_or_schema:
        # v3 条項5: MALFORMED gets its own provisional gate-stop, distinct
        # from digest-mismatch [12] -- the dedicated `schema-invalid` enum
        # value is still pending Sol confirmation (v3's own "Sol へ残す諮問"),
        # so this is explicitly marked PROVISIONAL rather than silently
        # reusing [12]'s semantics for a different failure class.
        return {"verdict": "INTEGRITY_STOP", "primary_reason_code": "schema-invalid (PROVISIONAL, pending Sol enum)",
                "reason_code_number": None, "stop_before_verifier": True,
                "note": "certificate-schema validator gate FAILED with MALFORMED findings ONLY (v3 条項5: "
                        "null/non-array/missing-tag/unknown-tag) -- this certificate MUST NOT be passed to "
                        "verifier A or verifier B. A dedicated `schema-invalid` reason-code enum is still "
                        "pending Sol confirmation (cert_shape_interpretation_v3.md's own open referral); this "
                        "is a provisional gate-stop, NOT [12] digest-mismatch (that code is reserved for "
                        "genuine digest/pin mismatches, see [64-hex]/[12/digest-mismatch]-tagged findings)."}
    return {"verdict": "INTEGRITY_STOP", "primary_reason_code": "digest-mismatch",
            "reason_code_number": 12, "stop_before_verifier": True,
            "note": "certificate-schema validator gate FAILED (裁定127/128/139) -- this certificate MUST NOT be "
                    "passed to verifier A or verifier B. Treated as [12] digest-mismatch-equivalent per "
                    "contract sec.5.2 routing (a structurally invalid certificate cannot support a meaningful "
                    "P-3.* re-check). Contains MALFORMED findings alongside digest/schema violations if any "
                    "-- see violations[] for the full, tagged list."}


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
