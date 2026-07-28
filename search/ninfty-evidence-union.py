#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-evidence-union.py

evidence-union/fail-closed-v2 (追補(o) v3.1,
docs/notes/cert_shape_interpretation_addendum_o_v3.md; sharpened by Sol
F83-2.1/2.2/2.3 -> N83-2.3 -> sol/裁定_192_便83検収.md, sol/sol_reply_83_math10.md).
A GENERAL two-route composition function -- NOT W-6-specific (P80-D/P81-E:
"複数証明経路の共通規則") -- for combining two independent evidence routes
(R1 = recomputation route, R2 = witness-coverage route) into ONE overall
status, fail-closed and TOTAL (defined on every input pair) and
SWAP-SYMMETRIC.

裁定192 REDESIGN (N83-2.3 "二層化", replacing the prior single-layer
`classify_route(blob)`): Sol's F83-2.2 finding was that a generic
"classify an ambiguous raw blob by reading its self-declared `evidence_kind`
field" function is inherently a VERDICT-SELECTOR vulnerability -- a
producer can plant PASS-shaped fields alongside a FAIL-shaped
`counterexample_locus` and the presence/absence of `evidence_kind` alone
flips the outcome. The fix is architectural, not a patch: DISPATCH (which
Python object/constructor was actually invoked) fixes route_id and
route_status, never a self-declared field inside the evidence blob.

  - A `RouteResult` is a dict built ONLY via the four constructors below
    (route_result_pass/fail/absent/malformed), each of which independently
    validates ITS OWN required fields and raises internally (never
    silently accepting a bad shape) if the invariants are not met -- there
    is no path from "arbitrary producer blob" directly to a route_status
    without going through code that ALREADY decided which status applies.
  - `coerce_to_route_result(obj)` re-validates an ALREADY-BUILT (or
    foreign/untrusted) RouteResult-shaped value at the combinator's own
    entry point (defense in depth, per N83-2.3: "combinator は
    RouteResult の constructor/private validation を通った値だけを受ける
    か、入口で同じ invariant を再検査する") -- a non-object, a missing/
    unrecognized route_status, or CO-PRESENT fields belonging to a
    DIFFERENT status's shape (F83-2.2: "status-specific shape の併存") are
    ALL MALFORMED, never silently resolved to ABSENT (F83-2.2's "非 object
    blob が ABSENT" bug is closed here: only `None` is ABSENT; any other
    non-RouteResult-shaped value is MALFORMED).
  - `compose_route_statuses` (the crisp, Sol-confirmed-PASS 4-rule core,
    N83-2.1) is UNCHANGED in its rule structure, but now ALSO defends
    itself at the low level (F83-2.2's "低水準 API でも
    compose_route_statuses(PASS, None, PASS, None) -> PASS" gap): a
    PASS/FAIL status paired with a digest that is not exact 64-hex is
    ITSELF escalated to INTEGRITY_STOP, even when this function is called
    directly (bypassing coerce_to_route_result).
  - PASS now REQUIRES `expected_domain_count`/`expected_domain_digest` as
    part of the RouteResult's OWN shape (not optional caller arguments
    threaded in after the fact, F83-2.1's core finding) -- the PASS
    constructor validates `expected_domain_count == checked_domain_count`
    and `expected_domain_digest == coverage_digest` ITSELF; a route-
    specific verifier that cannot establish these equalities must call
    route_result_fail(...) (if it has genuine counterexample evidence) or
    route_result_absent(...)/route_result_malformed(...) instead -- it must
    never call route_result_pass(...) with mismatched counts/digests
    hoping the constructor will paper over it (it will raise instead,
    surfacing as a MALFORMED-shaped result via the fail-closed wrapper).

SCOPE NOTE -- W-6 armature (unchanged from v3.1's task boundary):
`route_from_verifier_b_w6` adapts ninfty-verifier-b.py's
verify_W6_single(...) output into a RouteResult via the constructors
above, but remains an ARMATURE/PLACEHOLDER (per F83-2.3: this is NOT
"proof of real EP wiring") -- claim_digest/evidence_digest/
expected_domain_count are still derived from the detail dict itself
(sha256_of(detail)) or a hardcoded placeholder count, not from the actual
native/map digests. Full EP v7 wiring (binding these to genuine per-side
point/component data) is explicitly deferred to a later, separate step.

runtime = python (stdlib only: hashlib, json, re, sys, argparse).
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys

HEX64 = re.compile(r'^[0-9a-f]{64}$', re.IGNORECASE)

ROUTE_STATUSES = ("ABSENT", "MALFORMED", "PASS", "FAIL")
OVERALL_STATUSES = ("ABSENT", "INTEGRITY_STOP", "CONFLICT", "PASS", "FAIL")

HEADER_FIELDS = ("schema_id", "route_id", "route_status")
PASS_ONLY_FIELDS = ("expected_domain_count", "checked_domain_count", "expected_domain_digest", "coverage_digest")
FAIL_ONLY_FIELDS = ("counterexample_loci", "expected_witness", "observed_witness")
ABSENT_ONLY_FIELDS = ("missing_mask",)
MALFORMED_ONLY_FIELDS = ("schema_errors",)
COMMON_PF_FIELDS = ("claim_digest", "evidence_digest", "claim_source_ref", "evidence_refs")
SCHEMA_ID = "mb/ninfty-evidence-union/route-result/v1"


def canonical_serialize(obj):
    """Project-wide canonical form: UTF-8, sorted keys, no whitespace --
    same convention as ninfty-verifier-b.py / ninfty-cert-validator.py /
    ninfty-legacy-normalizer.py."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def _is_64hex(x):
    return isinstance(x, str) and bool(HEX64.match(x))


class RouteResultSchemaError(Exception):
    """Raised internally by the route_result_* constructors when their own
    REQUIRED invariants are not met (e.g. route_result_pass called with
    expected_domain_count != checked_domain_count). Always caught by the
    public constructor wrappers, which return a MALFORMED RouteResult
    instead of propagating -- a caller can never accidentally construct an
    internally-inconsistent "PASS" RouteResult."""


# ============================================================================
# RouteResult constructors (裁定192 N83-2.3 "二層化"): the ONLY way to build
# a RouteResult. Dispatch (which constructor got called) fixes route_status
# -- no self-declared producer field ever selects the branch.
# ============================================================================


def _route_header(route_id, route_status):
    if not isinstance(route_id, str) or not route_id:
        raise RouteResultSchemaError(f"route_id must be a non-empty string, got {route_id!r}")
    return {"schema_id": SCHEMA_ID, "route_id": route_id, "route_status": route_status}


def route_result_pass(route_id, claim_digest, evidence_digest, expected_domain_count, checked_domain_count,
                       expected_domain_digest, coverage_digest, claim_source_ref=None, evidence_refs=None):
    """
    Builds a PASS RouteResult. VALIDATES (raises RouteResultSchemaError,
    caught by the wrapper below, on failure) that:
      - claim_digest/evidence_digest/expected_domain_digest/coverage_digest
        are all exact 64-hex (F82-4.1/F83-2.1 common + PASS-specific
        required fields).
      - expected_domain_count/checked_domain_count are non-negative ints
        AND EQUAL (F83-2.1: PASS requires this equality to ALREADY hold --
        a route-specific verifier that cannot establish it must call
        route_result_fail/_absent/_malformed instead, never this
        constructor with mismatched values).
      - expected_domain_digest == coverage_digest (F83-2.1/N82-4.1: the
        receiver-derived canonical domain digest must equal the route's
        own coverage_digest).
    A caller that already knows these don't hold should NOT call this
    constructor at all -- see route_result_fail's coverage-mismatch note.
    """
    try:
        result = _route_header(route_id, "PASS")
        for name, val in (("claim_digest", claim_digest), ("evidence_digest", evidence_digest),
                          ("expected_domain_digest", expected_domain_digest), ("coverage_digest", coverage_digest)):
            if not _is_64hex(val):
                raise RouteResultSchemaError(f"PASS RouteResult.{name} must be exact 64-hex, got {val!r}")
        for name, val in (("expected_domain_count", expected_domain_count), ("checked_domain_count", checked_domain_count)):
            if not isinstance(val, int) or isinstance(val, bool) or val < 0:
                raise RouteResultSchemaError(f"PASS RouteResult.{name} must be a non-negative int, got {val!r}")
        if expected_domain_count != checked_domain_count:
            raise RouteResultSchemaError(
                f"PASS RouteResult requires expected_domain_count == checked_domain_count "
                f"(got {expected_domain_count!r} != {checked_domain_count!r}) -- the caller must not claim "
                "PASS when this equality does not already hold (F83-2.1)"
            )
        if expected_domain_digest != coverage_digest:
            raise RouteResultSchemaError(
                "PASS RouteResult requires expected_domain_digest == coverage_digest -- the caller must "
                "not claim PASS when the receiver-derived expected domain digest disagrees with the "
                "route's own coverage_digest (F83-2.1/N82-4.1)"
            )
        result.update({
            "claim_digest": claim_digest, "evidence_digest": evidence_digest,
            "claim_source_ref": claim_source_ref, "evidence_refs": evidence_refs,
            "expected_domain_count": expected_domain_count, "checked_domain_count": checked_domain_count,
            "expected_domain_digest": expected_domain_digest, "coverage_digest": coverage_digest,
        })
        return result
    except RouteResultSchemaError as e:
        return route_result_malformed(route_id, [str(e)])


def route_result_fail(route_id, claim_digest, evidence_digest, counterexample_loci,
                       claim_source_ref=None, evidence_refs=None, expected_witness=None, observed_witness=None):
    """Builds a FAIL RouteResult. VALIDATES claim_digest/evidence_digest
    (64-hex) and counterexample_loci (non-empty list, F83-2.1's structured
    requirement) -- otherwise falls back to MALFORMED (never silently
    accepts a FAIL with no actual counterexample evidence)."""
    if not _is_64hex(claim_digest) or not _is_64hex(evidence_digest):
        return route_result_malformed(route_id, [
            f"FAIL RouteResult requires claim_digest/evidence_digest as exact 64-hex, got "
            f"{claim_digest!r}/{evidence_digest!r}",
        ])
    if not isinstance(counterexample_loci, list) or len(counterexample_loci) == 0:
        return route_result_malformed(route_id, [
            f"FAIL RouteResult requires a non-empty 'counterexample_loci' array, got {counterexample_loci!r}",
        ])
    result = _route_header(route_id, "FAIL")
    result.update({
        "claim_digest": claim_digest, "evidence_digest": evidence_digest,
        "claim_source_ref": claim_source_ref, "evidence_refs": evidence_refs,
        "counterexample_loci": counterexample_loci,
        "expected_witness": expected_witness, "observed_witness": observed_witness,
    })
    return result


def route_result_absent(route_id, missing_mask):
    """Builds an ABSENT RouteResult. `missing_mask` is RECEIVER-DERIVED
    (never a producer self-report) and REQUIRED (non-None) -- an ABSENT
    result with no missing_mask at all is itself a schema violation
    (MALFORMED), not a silently-accepted ABSENT."""
    if missing_mask is None:
        return route_result_malformed(route_id, ["ABSENT RouteResult requires a non-None 'missing_mask' (receiver-derived)"])
    result = _route_header(route_id, "ABSENT")
    result["missing_mask"] = missing_mask
    return result


def route_result_malformed(route_id, schema_errors):
    """Builds a MALFORMED RouteResult. `schema_errors` must be a non-empty
    list (if the caller somehow supplies an empty/invalid one, a generic
    fallback error is substituted -- MALFORMED can never end up with an
    empty error list, since that would itself be a schema violation with
    nothing to show for it)."""
    if not isinstance(schema_errors, list) or len(schema_errors) == 0:
        schema_errors = ["MALFORMED RouteResult constructed with no schema_errors -- generic fallback recorded"]
    try:
        result = _route_header(route_id, "MALFORMED")
    except RouteResultSchemaError:
        result = {"schema_id": SCHEMA_ID, "route_id": route_id if isinstance(route_id, str) else "unknown", "route_status": "MALFORMED"}
    result["schema_errors"] = schema_errors
    return result


# ============================================================================
# Re-validation entry point (裁定192 N83-2.3): the combinator calls THIS,
# not any raw producer field, to determine (route_status, claim_digest,
# detail) for an already-built-or-foreign RouteResult-shaped value. This is
# the SAME invariant the constructors above enforce, re-checked at the
# combinator's own boundary (defense in depth) -- a value that never went
# through the constructors (e.g. deserialized from disk, or maliciously
# hand-crafted) is held to the identical standard.
# ============================================================================


def coerce_to_route_result(obj):
    """
    Returns (route_status, claim_digest, detail). route_status in
    ROUTE_STATUSES; claim_digest is the route's own claim_digest when
    route_status in {PASS, FAIL}, else None. NEVER raises.

    裁定192 F83-2.2 fixes, all enforced here:
      - a non-dict value (INCLUDING an explicit non-None "garbage"/list/
        string) is MALFORMED, NOT ABSENT -- only `None` (or a dict that
        structurally declares route_status="ABSENT" with a missing_mask)
        is ABSENT. "Existence of *something* that isn't a valid RouteResult
        shape" is a schema problem, not evidence-absence.
      - route_status is read from the RouteResult's OWN header field, never
        inferred from `evidence_kind` or any other producer hint -- there
        is no `evidence_kind` field in this schema at all anymore.
      - co-presence of ANOTHER status's shape-specific fields (e.g. a
        route declaring route_status="PASS" while ALSO carrying
        `counterexample_loci`) is MALFORMED, regardless of which status
        "wins" -- never silently resolved by preferring one field set.
    """
    if obj is None:
        return "ABSENT", None, {"reason": "route result is None -- receiver-derived ABSENT (no producer self-report trusted)"}
    if not isinstance(obj, dict):
        return "MALFORMED", None, {"schema_errors": [f"route result is not an object: {obj!r} (F83-2.2: non-object is MALFORMED, not ABSENT)"]}

    status = obj.get("route_status")
    if status not in ROUTE_STATUSES:
        return "MALFORMED", None, {"schema_errors": [f"route_status missing or unrecognized: {status!r}"]}

    shape_fields = {"PASS": PASS_ONLY_FIELDS, "FAIL": FAIL_ONLY_FIELDS, "ABSENT": ABSENT_ONLY_FIELDS, "MALFORMED": MALFORMED_ONLY_FIELDS}
    foreign = []
    for other_status, fields in shape_fields.items():
        if other_status == status:
            continue
        for f in fields:
            if f in obj:
                foreign.append(f)
    if foreign:
        return "MALFORMED", None, {
            "schema_errors": [
                f"route result declares route_status={status!r} but ALSO carries foreign status-shape "
                f"field(s) {foreign!r} (F83-2.2: status-specific shape co-presence is MALFORMED, never "
                "silently resolved by preferring one)",
            ],
        }

    if status == "ABSENT":
        if obj.get("missing_mask") is None:
            return "MALFORMED", None, {"schema_errors": ["ABSENT route result missing non-None 'missing_mask'"]}
        return "ABSENT", None, {"missing_mask": obj["missing_mask"]}

    if status == "MALFORMED":
        errs = obj.get("schema_errors")
        if not isinstance(errs, list) or len(errs) == 0:
            return "MALFORMED", None, {"schema_errors": ["MALFORMED route result missing non-empty 'schema_errors'"]}
        return "MALFORMED", None, {"schema_errors": errs}

    # PASS or FAIL: common digest fields required (F82-4.1/F83-2.1).
    claim_digest = obj.get("claim_digest")
    evidence_digest = obj.get("evidence_digest")
    if not _is_64hex(claim_digest) or not _is_64hex(evidence_digest):
        return "MALFORMED", None, {"schema_errors": [
            f"{status} route result missing/ill-typed claim_digest ({claim_digest!r}) or evidence_digest "
            f"({evidence_digest!r})",
        ]}

    if status == "FAIL":
        loci = obj.get("counterexample_loci")
        if not isinstance(loci, list) or len(loci) == 0:
            return "MALFORMED", None, {"schema_errors": ["FAIL route result missing non-empty 'counterexample_loci'"]}
        return "FAIL", claim_digest, {"counterexample_loci": loci}

    # PASS
    edc = obj.get("expected_domain_count")
    cdc = obj.get("checked_domain_count")
    edd = obj.get("expected_domain_digest")
    cvd = obj.get("coverage_digest")
    for name, val in (("expected_domain_count", edc), ("checked_domain_count", cdc)):
        if not isinstance(val, int) or isinstance(val, bool) or val < 0:
            return "MALFORMED", None, {"schema_errors": [f"PASS route result.{name} must be a non-negative int, got {val!r}"]}
    if not _is_64hex(edd) or not _is_64hex(cvd):
        return "MALFORMED", None, {"schema_errors": [f"PASS route result expected_domain_digest/coverage_digest must be exact 64-hex, got {edd!r}/{cvd!r}"]}
    if edc != cdc:
        return "MALFORMED", None, {"schema_errors": [f"PASS route result expected_domain_count != checked_domain_count ({edc!r} != {cdc!r}) -- F83-2.1"]}
    if edd != cvd:
        return "MALFORMED", None, {"schema_errors": [f"PASS route result expected_domain_digest != coverage_digest -- F83-2.1/N82-4.1"]}
    return "PASS", claim_digest, {"expected_domain_count": edc, "checked_domain_count": cdc, "expected_domain_digest": edd, "coverage_digest": cvd}


# ============================================================================
# Composition (追補(o) v3.1 "合成の全域関数", N83-2.1 confirmed PASS): TOTAL
# over the 4x4=16 (route_status, route_status) domain, swap-symmetric,
# exactly the 4 ordered rules below -- UNCHANGED in structure. 裁定192
# F83-2.2 adds ONE defensive layer: a PASS/FAIL status paired with a
# non-64-hex digest is ITSELF escalated to INTEGRITY_STOP even when this
# low-level function is called directly (bypassing coerce_to_route_result).
# ============================================================================


def compose_route_statuses(status1, claim_digest1, status2, claim_digest2):
    """
    Composes two ALREADY-CLASSIFIED route statuses into ONE overall
    status. TOTAL (defined for every (status1, status2) in
    ROUTE_STATUSES x ROUTE_STATUSES) and SWAP-SYMMETRIC. Rules, IN ORDER:

      0. (裁定192 F83-2.2, defense in depth) a PASS/FAIL status paired with
         a digest that is not exact 64-hex -> INTEGRITY_STOP (this low-level
         API must not be more permissive than coerce_to_route_result, even
         when called directly).
      1. Either route MALFORMED -> INTEGRITY_STOP (regardless of
         direction/order).
      2. Both routes non-ABSENT (i.e. each in {PASS, FAIL}) -> compare
         claim_digest BEFORE composing status: mismatch -> CONFLICT
         (applies to PASS/PASS, FAIL/FAIL, AND FAIL/PASS alike).
      3. Both non-ABSENT, claim_digest agrees, but the two statuses
         DISAGREE (one PASS, one FAIL) -> CONFLICT.
      4. Otherwise: any FAIL present -> FAIL; else any PASS present ->
         PASS; else (both ABSENT) -> ABSENT.

    Returns one of OVERALL_STATUSES.
    """
    for s in (status1, status2):
        if s not in ROUTE_STATUSES:
            raise ValueError(f"compose_route_statuses: not a valid route_status: {s!r}")

    # Rule 0 (defense in depth).
    for s, d in ((status1, claim_digest1), (status2, claim_digest2)):
        if s in ("PASS", "FAIL") and not _is_64hex(d):
            return "INTEGRITY_STOP"

    # Rule 1.
    if status1 == "MALFORMED" or status2 == "MALFORMED":
        return "INTEGRITY_STOP"

    non_absent = [(s, d) for (s, d) in ((status1, claim_digest1), (status2, claim_digest2)) if s != "ABSENT"]

    if len(non_absent) == 2:
        (s_a, d_a), (s_b, d_b) = non_absent
        if d_a != d_b:
            return "CONFLICT"
        if s_a != s_b:
            return "CONFLICT"
        return s_a

    if len(non_absent) == 1:
        return non_absent[0][0]

    return "ABSENT"


# ============================================================================
# Top-level entry point: coerce/re-validate both RouteResults, then compose.
# ============================================================================


def evidence_union_fail_closed_v2(route1, route2):
    """
    Top-level evidence-union/fail-closed-v2 composition (追補(o) v3.1,
    RouteResult two-layer per 裁定192 N83-2.3). `route1`/`route2` should be
    RouteResult dicts built via the route_result_* constructors (R1/R2, per
    dispatch); this function re-validates them regardless (see
    coerce_to_route_result) so a foreign/hand-crafted value is held to the
    same invariant, never trusted blindly. Returns:
      {
        "route1_status": ..., "route1_detail": ...,
        "route2_status": ..., "route2_detail": ...,
        "overall_status": ...,
      }
    Never raises.
    """
    s1, d1, detail1 = coerce_to_route_result(route1)
    s2, d2, detail2 = coerce_to_route_result(route2)
    overall = compose_route_statuses(s1, d1, s2, d2)
    return {
        "route1_status": s1, "route1_detail": detail1,
        "route2_status": s2, "route2_detail": detail2,
        "overall_status": overall,
    }


# ============================================================================
# W-6 connection point (ARMATURE ONLY -- see module docstring SCOPE NOTE;
# NOT wired into the EP runner here, EP v7 wiring is a later, separate
# step). Adapts ninfty-verifier-b.py's verify_W6_single(...) (status,
# detail) output into a RouteResult via the constructors above (never a
# raw ad hoc blob).
# ============================================================================


def route_from_verifier_b_w6(w6_status, w6_detail, route_id):
    """
    ARMATURE / PLACEHOLDER (not full EP wiring): adapts one
    ninfty-verifier-b.py verify_W6_single(cert, native_a, native_b) result
    -- a (status, detail) pair with status in
    {"ABSENT","MALFORMED","PASS","FAIL"} -- into a RouteResult built via
    the constructors above (route_id = "R1"/"R2", FIXED by the caller's
    dispatch, never inferred from the blob).

    verify_W6_single predates this addendum's RouteResult schema (it has no
    claim_digest/evidence_digest/expected_domain_count/expected_domain_digest
    fields of its own) -- this adapter DERIVES placeholder digests from the
    detail dict itself (sha256_of(detail)) and a hardcoded
    expected_domain_count=checked_domain_count=1 so the PASS constructor's
    OWN invariants (which it always checks) are satisfiable, but this is
    NOT a claim that W-6's real evidence has been migrated to the v3.1
    RouteResult schema -- it exists solely so the composition function (the
    crisp, addendum-specified part) has a real, non-synthetic input to be
    exercised against in regression tests. Full EP v7 wiring (real
    claim_digest/evidence_digest/expected_domain_count bound to the actual
    native/map digests and per-side point/component counts) is explicitly
    deferred, per this round's task scope.
    """
    if w6_status == "ABSENT":
        return route_result_absent(route_id, {"reason": (w6_detail or {}).get("reason", "W-6 ABSENT") if isinstance(w6_detail, dict) else "W-6 ABSENT"})
    if w6_status == "MALFORMED":
        errs = [str((w6_detail or {}).get("reason", w6_detail))] if isinstance(w6_detail, dict) else [str(w6_detail)]
        return route_result_malformed(route_id, errs)
    detail_digest = sha256_of(w6_detail if isinstance(w6_detail, dict) else {"detail": w6_detail})
    if w6_status == "FAIL":
        return route_result_fail(route_id, detail_digest, detail_digest, [w6_detail if w6_detail is not None else "W-6 FAIL (no detail supplied)"])
    # w6_status == "PASS"
    return route_result_pass(
        route_id, detail_digest, detail_digest,
        expected_domain_count=1, checked_domain_count=1,  # PLACEHOLDER (armature only, see docstring)
        expected_domain_digest=detail_digest, coverage_digest=detail_digest,
    )


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("payload_json", help="path to a JSON payload {route1, route2} (already-built RouteResult dicts), or '-' for stdin")
    args = ap.parse_args(argv)
    if args.payload_json == "-":
        payload = json.load(sys.stdin)
    else:
        with open(args.payload_json, "r", encoding="utf-8") as f:
            payload = json.load(f)
    result = evidence_union_fail_closed_v2(payload.get("route1"), payload.get("route2"))
    print(canonical_serialize(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
