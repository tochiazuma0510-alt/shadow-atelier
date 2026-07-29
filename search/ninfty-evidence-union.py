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

Sol 便84 P84-5.4 HARDENING (docs/notes/cert_shape_interpretation_addendum_o_v4.md,
sol/sol_reply_84_math11.md F84-5.4): the nominal gate that used to be open --
`coerce_to_route_result` checked `route_status` and status-specific fields
but NEVER `schema_id`/`route_id` -- is now closed:
  1. `schema_id` must equal SCHEMA_ID exactly (missing, or e.g. "evil/v9",
     is MALFORMED).
  2. the combinator's first argument slot must carry route_id="R1", the
     second must carry route_id="R2" (slot-bound, not just "any two
     distinct strings").
  3. `route_id` is enum-restricted to {"R1","R2"} at the CONSTRUCTOR level
     too (`_route_header` / VALID_ROUTE_IDS) -- `route_result_pass(
     "producer-choice", ...)` now refuses and falls back to MALFORMED.
  4. any field not part of the current status's own shape is rejected
     (subsumes the old cross-status co-presence check and additionally
     catches wholly invented field names).
  5. `route_from_verifier_b_w6` populates `claim_source_ref`/`evidence_refs`
     from the raw (status,detail) it was handed, recomputing the digest
     fresh each call, rather than leaving them at the constructors' `None`
     default.
  6. `evidence_union_fail_closed_v2` is the ONLY public combination entry
     point (used by both the CLI and any in-process caller) and it ALWAYS
     re-validates through the hardened `coerce_to_route_result` -- there is
     no path that accepts a raw producer JSON blob as an already-valid
     RouteResult.

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

# Sol 便84 P84-5.4 item 3: route_id is DISPATCH-FIXED (which slot/constructor
# call site is used), never a producer-chosen free string. R1 = the
# recomputation route, R2 = the witness-coverage route (追補(o) v3.1 "R1 =
# recomputation route, R2 = witness-coverage route"); the combinator's two
# argument slots are bound to exactly these two ids, in this fixed order
# (P84-5.4 item 2).
VALID_ROUTE_IDS = ("R1", "R2")


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
    if route_id not in VALID_ROUTE_IDS:
        raise RouteResultSchemaError(
            f"route_id must be one of {VALID_ROUTE_IDS!r} (dispatch-fixed by which constructor/slot was "
            f"used, never a producer-chosen free string -- Sol 便84 P84-5.4 item 3), got {route_id!r}"
        )
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
    try:
        result = _route_header(route_id, "FAIL")
    except RouteResultSchemaError as e:
        return route_result_malformed(route_id, [str(e)])
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
    try:
        result = _route_header(route_id, "ABSENT")
    except RouteResultSchemaError as e:
        return route_result_malformed(route_id, [str(e)])
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


def coerce_to_route_result(obj, expected_route_id=None):
    """
    Returns (route_status, claim_digest, detail). route_status in
    ROUTE_STATUSES; claim_digest is the route's own claim_digest when
    route_status in {PASS, FAIL}, else None. NEVER raises.

    `expected_route_id`, when supplied (Sol 便84 P84-5.4 item 2: the
    combinator's first argument slot MUST be route_id="R1", the second
    MUST be "R2"), additionally requires obj["route_id"] == expected_route_id
    -- a route result that is otherwise perfectly well-formed but sits in
    the WRONG slot (e.g. an "R2" route passed as the combinator's first
    argument) is MALFORMED, not silently accepted under a mismatched
    identity. `None` is left un-gated by this (see below): a route that is
    genuinely absent has no slot identity to check.

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

    Sol 便84 F84-5.4/P84-5 fixes, all enforced here (RouteResult nominal
    gate hardening -- a bare dict with a self-declared route_status alone
    is no longer sufficient to reach PASS/FAIL/ABSENT):
      1. `schema_id` MUST equal SCHEMA_ID exactly ("mb/ninfty-evidence-union
         /route-result/v1") -- a missing schema_id, or any other value
         (including a plausible-looking "evil/v9"), is MALFORMED. Closes
         Sol's literal probe: {schema_id missing, route_id missing,
         route_status="PASS"} used to reach PASS; it is MALFORMED now.
      2. `route_id` MUST be in the slot the caller expects (see
         `expected_route_id` above) -- P84-5.4 item 2.
      3. `route_id` MUST be one of VALID_ROUTE_IDS ("R1","R2") -- P84-5.4
         item 3, mirrors the same enum the constructors enforce (_route_header).
      4. ANY field on `obj` that is not part of {schema_id, route_id,
         route_status} plus this status's own shape fields (plus
         claim_digest/evidence_digest/claim_source_ref/evidence_refs for
         PASS/FAIL) is an unrecognized/foreign field -- MALFORMED. This
         SUBSUMES the pre-existing co-presence check below (a foreign
         status's shape field is, by construction, not in the current
         status's allowed set either) and additionally rejects a
         completely made-up field name like "evil_extra_field" that the
         old co-presence check alone would not have caught -- P84-5.4
         item 4.
    """
    if obj is None:
        return "ABSENT", None, {"reason": "route result is None -- receiver-derived ABSENT (no producer self-report trusted)"}
    if not isinstance(obj, dict):
        return "MALFORMED", None, {"schema_errors": [f"route result is not an object: {obj!r} (F83-2.2: non-object is MALFORMED, not ABSENT)"]}

    status = obj.get("route_status")
    if status not in ROUTE_STATUSES:
        return "MALFORMED", None, {"schema_errors": [f"route_status missing or unrecognized: {status!r}"]}

    schema_id = obj.get("schema_id")
    if schema_id != SCHEMA_ID:
        return "MALFORMED", None, {"schema_errors": [
            f"schema_id must be exactly {SCHEMA_ID!r}, got {schema_id!r} (Sol 便84 P84-5.4 item 1)",
        ]}

    route_id = obj.get("route_id")
    if route_id not in VALID_ROUTE_IDS:
        return "MALFORMED", None, {"schema_errors": [
            f"route_id must be one of {VALID_ROUTE_IDS!r} (dispatch-fixed, never producer-chosen), "
            f"got {route_id!r} (Sol 便84 P84-5.4 item 3)",
        ]}
    if expected_route_id is not None and route_id != expected_route_id:
        return "MALFORMED", None, {"schema_errors": [
            f"route_id={route_id!r} does not match the required slot {expected_route_id!r} -- the "
            "combinator's first argument must be route_id='R1', the second must be 'R2' (Sol 便84 "
            "P84-5.4 item 2)",
        ]}

    shape_fields = {"PASS": PASS_ONLY_FIELDS, "FAIL": FAIL_ONLY_FIELDS, "ABSENT": ABSENT_ONLY_FIELDS, "MALFORMED": MALFORMED_ONLY_FIELDS}
    allowed = set(HEADER_FIELDS) | set(shape_fields[status])
    if status in ("PASS", "FAIL"):
        allowed |= set(COMMON_PF_FIELDS)
    unrecognized = sorted(k for k in obj.keys() if k not in allowed)
    if unrecognized:
        return "MALFORMED", None, {
            "schema_errors": [
                f"route result declares route_status={status!r} but carries unrecognized/foreign field(s) "
                f"{unrecognized!r} not part of this status's own shape (Sol 便84 P84-5.4 item 4; this "
                "subsumes the prior F83-2.2 status-shape co-presence check -- e.g. a PASS-shaped result "
                "also carrying counterexample_loci is caught here too)",
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
    Top-level evidence-union/fail-closed-v2 composition (追補(o) v4,
    docs/notes/cert_shape_interpretation_addendum_o_v4.md, RouteResult
    two-layer per 裁定192 N83-2.3, hardened by Sol 便84 P84-5.4).
    `route1`/`route2` should be RouteResult dicts built via the
    route_result_* constructors, route1 with route_id="R1" (the
    recomputation route) and route2 with route_id="R2" (the
    witness-coverage route) -- this is the ONLY public entry point this
    module exposes for composing two routes (both the CLI `main()` reading
    raw producer JSON and any in-process caller go through this SAME
    function), and it ALWAYS re-validates both arguments via
    coerce_to_route_result with the slot bound (see `expected_route_id`
    there) -- there is no bypass path that trusts route1/route2 as
    already-valid just because they look like RouteResult dicts (Sol 便84
    P84-5.4 item 6: raw producer JSON is never accepted as a RouteResult
    directly -- it is held to the exact same schema_id/route_id/shape gate
    a freshly-constructed RouteResult would have to pass). Returns:
      {
        "route1_status": ..., "route1_detail": ...,
        "route2_status": ..., "route2_detail": ...,
        "overall_status": ...,
      }
    Never raises.
    """
    s1, d1, detail1 = coerce_to_route_result(route1, expected_route_id="R1")
    s2, d2, detail2 = coerce_to_route_result(route2, expected_route_id="R2")
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
    NOT a claim that W-6's real evidence has been migrated to the v3.1/v4
    RouteResult schema -- it exists solely so the composition function (the
    crisp, addendum-specified part) has a real, non-synthetic input to be
    exercised against in regression tests. Full EP v7 wiring (real
    claim_digest/evidence_digest/expected_domain_count bound to the actual
    native/map digests and per-side point/component counts) is explicitly
    deferred, per this round's task scope.

    Sol 便84 P84-5.4 item 5: `claim_source_ref`/`evidence_refs` are now
    populated FROM THE RAW w6_detail itself (never left as the constructors'
    None default) -- both the digest AND the refs are freshly recomputed
    from w6_detail on every call, so a stale/cached digest computed
    elsewhere can never be substituted here. This remains armature-level
    (the ref still names the (status,detail) pair this adapter was handed,
    not a genuine per-side native/map artifact identity), consistent with
    the SCOPE NOTE above.
    """
    if w6_status == "ABSENT":
        return route_result_absent(route_id, {"reason": (w6_detail or {}).get("reason", "W-6 ABSENT") if isinstance(w6_detail, dict) else "W-6 ABSENT"})
    if w6_status == "MALFORMED":
        errs = [str((w6_detail or {}).get("reason", w6_detail))] if isinstance(w6_detail, dict) else [str(w6_detail)]
        return route_result_malformed(route_id, errs)
    detail_digest = sha256_of(w6_detail if isinstance(w6_detail, dict) else {"detail": w6_detail})
    claim_source_ref = {"source": "ninfty-verifier-b.verify_W6_single", "raw_detail_digest": detail_digest}
    evidence_refs = [{"source": "ninfty-verifier-b.verify_W6_single.detail", "digest": detail_digest}]
    if w6_status == "FAIL":
        return route_result_fail(
            route_id, detail_digest, detail_digest,
            [w6_detail if w6_detail is not None else "W-6 FAIL (no detail supplied)"],
            claim_source_ref=claim_source_ref, evidence_refs=evidence_refs,
        )
    # w6_status == "PASS"
    return route_result_pass(
        route_id, detail_digest, detail_digest,
        expected_domain_count=1, checked_domain_count=1,  # PLACEHOLDER (armature only, see docstring)
        expected_domain_digest=detail_digest, coverage_digest=detail_digest,
        claim_source_ref=claim_source_ref, evidence_refs=evidence_refs,
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
