#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-evidence-union.py

evidence-union/fail-closed-v2 (追補(o) v5,
docs/notes/cert_shape_interpretation_addendum_o_v5.md; trust-boundary
repair per Sol F85-6.3 B85-o1..o4 / P85-5 -> sol/sol_reply_85_math12.md).
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

Sol 便84 P84-5.4 HARDENING (docs/notes/cert_shape_interpretation_addendum_o_v4.md,
sol/sol_reply_84_math11.md F84-5.4): closed the RouteResult NOMINAL gate
(schema_id/route_id/slot binding/unknown fields), summarized in the
RouteResult constructors and `coerce_to_route_result` below.

Sol 便85 P85-5 TRUST-BOUNDARY REPAIR (docs/notes/
cert_shape_interpretation_addendum_o_v5.md, sol/sol_reply_85_math12.md
F85-6.3 -- B85-o1..o4): 便84's nominal-gate hardening made a RouteResult's
SHAPE strict, but Sol's F85-6.3 probe showed that **shape is not
provenance**: a producer who knows the (now-strict) shape can still hand
the combinator a self-asserted, valid-shape "PASS" that was never actually
produced by a route-specific verifier. Four blockers, four fixes, all
below:

  B85-o1 (raw producer self-asserted PASS reaches PASS): the OLD `main()`
    read an already-built `{route1, route2}` RouteResult pair straight
    from JSON and fed it to the combinator -- there was NO code path that
    forced a route-specific verifier to actually run. FIX: the public
    entry point (`evidence_union_from_raw_w6`, and the CLI `main()` that
    calls it) now accepts ONLY a RAW evidence artifact
    (`{schema_id=RAW_W6_EVIDENCE_SCHEMA_ID, certificate, native_a,
    native_b}`) -- never a pre-built RouteResult. The receiver-side
    dispatch inside `_build_R1`/`_build_R2` is FIXED: it ALWAYS calls
    `ninfty-verifier-b.verify_W6_single` itself, on this raw evidence,
    independently of anything a caller might separately claim the
    verifier already said.

  B85-o2 (provenance refs not required/re-verified): `claim_source_ref`/
    `evidence_refs` used to be optional (constructor default `None`) and
    were never checked by `coerce_to_route_result` beyond "is this key
    present at all". FIX: both fields are now REQUIRED, non-null,
    STRUCTURED ({"source": <str>, "digest": <64-hex>}, evidence_refs a
    non-empty list of such objects) at the constructor AND at
    `coerce_to_route_result` (missing/None/ill-shaped -> MALFORMED). And,
    critically, self-reported shape is still not provenance BY ITSELF:
    `evidence_union_from_raw_w6` independently recomputes the digest of
    the raw evidence it was actually given and requires every ref's
    `digest` to equal that RECEIVER-recomputed value
    (`_cross_check_refs_against_raw`) -- a route whose refs merely LOOK
    well-shaped but do not resolve to the raw evidence in hand is
    downgraded to MALFORMED, never accepted on self-report alone.

  B85-o3 (status enum fall-through in the W-6 adapter): the OLD
    `route_from_verifier_b_w6` checked ABSENT and MALFORMED explicitly,
    then FAIL, then fell through an unconditional `else` treated as PASS
    -- so `route_from_verifier_b_w6("BOGUS", ..., "R2").route_status` was
    PASS. FIX: the four recognized statuses (ABSENT/MALFORMED/FAIL/PASS)
    are now an EXHAUSTIVE if/elif chain, and anything else (any
    unrecognized string) falls to an explicit final branch that returns
    MALFORMED -- there is no implicit "everything else is PASS" branch
    left anywhere in this file.

  B85-o4 (connector is armature/placeholder -- placeholder counts):
    `route_from_verifier_b_w6`'s PASS branch used to hardcode
    `expected_domain_count=checked_domain_count=1` and reuse
    `sha256_of(detail)` for every digest field, none of which reflected a
    real domain. FIX: the PASS domain claim is now grounded in a REAL
    structural fact this file can actually establish without inventing
    anything -- W-6's own two-lane contract (`W6_DOMAIN_LANES = ("checker",
    "searcher")`, mirroring ninfty-verifier-b.py's NATIVE_SIDE_VALUES):
    `expected_domain_count=2` (both lanes MUST be checked per the W-6
    contract), `checked_domain_count=2` only when `verify_W6_single`
    actually resolved and compared BOTH lanes (i.e. reached a genuine
    PASS/FAIL verdict, not an ABSENT/MALFORMED short-circuit for either
    lane), `expected_domain_digest=coverage_digest=sha256_of(sorted(
    W6_DOMAIN_LANES))`. This remains an ARMATURE for genuine
    route-INDEPENDENCE (see `_build_R2`'s docstring): this codebase wires
    only ONE actual W-6 verifier (`verify_W6_single`), so R2 is still
    derived from the SAME receiver-invoked recomputation as R1, not a
    second, differently-implemented coverage check -- that second
    verifier does not exist yet and is UNKNOWN/not fabricated here (Sol
    便85 P85-5 item 5's "できない部分は UNKNOWN 申告で残し「発効対象外」
    と明記 -- 発明しない"). Full EP v7 wiring (binding these to genuine
    per-side point/component data beyond the two-lane structural fact) is
    still explicitly deferred.

  P85-5 item 7 (module-private constructors): the four
    `route_result_*` constructors are renamed `_route_result_*`
    (leading underscore, Python's "not part of the public API"
    convention) -- the only PUBLIC trust-boundary entry point this module
    exposes for untrusted input (CLI or in-process) is
    `evidence_union_from_raw_w6(raw)`, which never accepts an
    already-built RouteResult as its top-level argument.

  `compose_route_statuses` (the crisp, Sol-confirmed-PASS 4-rule core,
  N83-2.1) is UNCHANGED in its rule structure.

SCOPE NOTE -- W-6 armature (unchanged from v3.1/v4's task boundary):
`_build_R1`/`_build_R2` adapt ninfty-verifier-b.py's verify_W6_single(...)
output into a RouteResult -- but remain an ARMATURE/PLACEHOLDER (per
F83-2.3: this is NOT "proof of real EP wiring") in the sense that both
routes still recompute the SAME underlying pushforward-equality check;
genuine two-implementation independence for W-6 specifically is UNKNOWN
(not implemented). Full EP v7 wiring (binding these to genuine per-side
point/component data) is explicitly deferred to a later, separate step.

runtime = python (stdlib only: hashlib, importlib, json, os, re, sys,
argparse -- the dynamic import of ninfty-verifier-b.py uses
importlib.util, same technique search/test_ninfty_evidence_union.py
already used to load hyphenated-filename modules).
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
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

# Sol 便85 B85-o1 fix: the schema_id of a RAW evidence artifact (the ONLY
# shape the public trust boundary accepts) -- deliberately DISTINCT from
# SCHEMA_ID above (a RouteResult's own schema_id), so a producer cannot
# hand a pre-built RouteResult to the raw-evidence entry point and have it
# silently accepted as if it were raw evidence (or vice versa): the two
# schemas are different strings, checked at different, non-overlapping
# entry points.
RAW_W6_EVIDENCE_SCHEMA_ID = "mb/ninfty-evidence-union/raw-w6-evidence/v1"

# Sol 便85 B85-o4 fix: the REAL two-lane structural domain W-6 must check
# (mirrors ninfty-verifier-b.py's NATIVE_SIDE_VALUES = ("searcher",
# "checker")) -- used to ground expected_domain_count/expected_domain_digest
# in an actual fact about the W-6 contract, replacing the old hardcoded
# placeholder "1".
W6_DOMAIN_LANES = ("checker", "searcher")

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


def _is_valid_source_ref(ref):
    """Sol 便85 B85-o2: a well-shaped provenance ref = {"source": <non-empty
    str>, "digest": <exact 64-hex>} (extra keys tolerated on the ref object
    itself -- only claim_source_ref/evidence_refs presence+shape on the
    RouteResult is schema-gated elsewhere; this checks the ref's OWN two
    required sub-fields)."""
    return (
        isinstance(ref, dict)
        and isinstance(ref.get("source"), str) and len(ref["source"]) > 0
        and _is_64hex(ref.get("digest"))
    )


def _is_valid_evidence_refs(refs):
    return isinstance(refs, list) and len(refs) > 0 and all(_is_valid_source_ref(r) for r in refs)


class RouteResultSchemaError(Exception):
    """Raised internally by the _route_result_* constructors when their own
    REQUIRED invariants are not met (e.g. _route_result_pass called with
    expected_domain_count != checked_domain_count). Always caught by the
    public constructor wrappers, which return a MALFORMED RouteResult
    instead of propagating -- a caller can never accidentally construct an
    internally-inconsistent "PASS" RouteResult."""


# ============================================================================
# RouteResult constructors (裁定192 N83-2.3 "二層化"; renamed module-PRIVATE
# per Sol 便85 P85-5 item 7 -- these are internal building blocks, never
# the public trust boundary): the ONLY way to build a RouteResult. Dispatch
# (which constructor got called) fixes route_status -- no self-declared
# producer field ever selects the branch.
# ============================================================================


def _route_header(route_id, route_status):
    if route_id not in VALID_ROUTE_IDS:
        raise RouteResultSchemaError(
            f"route_id must be one of {VALID_ROUTE_IDS!r} (dispatch-fixed by which constructor/slot was "
            f"used, never a producer-chosen free string -- Sol 便84 P84-5.4 item 3), got {route_id!r}"
        )
    return {"schema_id": SCHEMA_ID, "route_id": route_id, "route_status": route_status}


def _route_result_pass(route_id, claim_digest, evidence_digest, expected_domain_count, checked_domain_count,
                        expected_domain_digest, coverage_digest, claim_source_ref, evidence_refs):
    """
    Builds a PASS RouteResult. VALIDATES (raises RouteResultSchemaError,
    caught by the wrapper below, on failure) that:
      - claim_digest/evidence_digest/expected_domain_digest/coverage_digest
        are all exact 64-hex (F82-4.1/F83-2.1 common + PASS-specific
        required fields).
      - expected_domain_count/checked_domain_count are non-negative ints
        AND EQUAL (F83-2.1: PASS requires this equality to ALREADY hold --
        a route-specific verifier that cannot establish it must call
        _route_result_fail/_absent/_malformed instead, never this
        constructor with mismatched values).
      - expected_domain_digest == coverage_digest (F83-2.1/N82-4.1: the
        receiver-derived canonical domain digest must equal the route's
        own coverage_digest).
      - claim_source_ref/evidence_refs are REQUIRED, non-null, structured
        (Sol 便85 B85-o2: no default `None` anymore -- a route-specific
        verifier that cannot produce genuine provenance refs must not
        call this constructor at all).
    A caller that already knows these don't hold should NOT call this
    constructor at all -- see _route_result_fail's coverage-mismatch note.
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
        if not _is_valid_source_ref(claim_source_ref):
            raise RouteResultSchemaError(
                f"PASS RouteResult requires a structured non-null claim_source_ref "
                f"({{'source': <str>, 'digest': <64-hex>}}), got {claim_source_ref!r} (Sol 便85 B85-o2)"
            )
        if not _is_valid_evidence_refs(evidence_refs):
            raise RouteResultSchemaError(
                f"PASS RouteResult requires a non-empty list of structured evidence_refs, got "
                f"{evidence_refs!r} (Sol 便85 B85-o2)"
            )
        result.update({
            "claim_digest": claim_digest, "evidence_digest": evidence_digest,
            "claim_source_ref": claim_source_ref, "evidence_refs": evidence_refs,
            "expected_domain_count": expected_domain_count, "checked_domain_count": checked_domain_count,
            "expected_domain_digest": expected_domain_digest, "coverage_digest": coverage_digest,
        })
        return result
    except RouteResultSchemaError as e:
        return _route_result_malformed(route_id, [str(e)])


def _route_result_fail(route_id, claim_digest, evidence_digest, counterexample_loci,
                        claim_source_ref, evidence_refs, expected_witness=None, observed_witness=None):
    """Builds a FAIL RouteResult. VALIDATES claim_digest/evidence_digest
    (64-hex), counterexample_loci (non-empty list, F83-2.1's structured
    requirement), and claim_source_ref/evidence_refs (Sol 便85 B85-o2:
    required, non-null, structured, no default) -- otherwise falls back to
    MALFORMED (never silently accepts a FAIL with no actual counterexample
    evidence or no genuine provenance)."""
    if not _is_64hex(claim_digest) or not _is_64hex(evidence_digest):
        return _route_result_malformed(route_id, [
            f"FAIL RouteResult requires claim_digest/evidence_digest as exact 64-hex, got "
            f"{claim_digest!r}/{evidence_digest!r}",
        ])
    if not isinstance(counterexample_loci, list) or len(counterexample_loci) == 0:
        return _route_result_malformed(route_id, [
            f"FAIL RouteResult requires a non-empty 'counterexample_loci' array, got {counterexample_loci!r}",
        ])
    if not _is_valid_source_ref(claim_source_ref):
        return _route_result_malformed(route_id, [
            f"FAIL RouteResult requires a structured non-null claim_source_ref, got {claim_source_ref!r} (Sol 便85 B85-o2)",
        ])
    if not _is_valid_evidence_refs(evidence_refs):
        return _route_result_malformed(route_id, [
            f"FAIL RouteResult requires a non-empty list of structured evidence_refs, got {evidence_refs!r} (Sol 便85 B85-o2)",
        ])
    try:
        result = _route_header(route_id, "FAIL")
    except RouteResultSchemaError as e:
        return _route_result_malformed(route_id, [str(e)])
    result.update({
        "claim_digest": claim_digest, "evidence_digest": evidence_digest,
        "claim_source_ref": claim_source_ref, "evidence_refs": evidence_refs,
        "counterexample_loci": counterexample_loci,
        "expected_witness": expected_witness, "observed_witness": observed_witness,
    })
    return result


def _route_result_absent(route_id, missing_mask):
    """Builds an ABSENT RouteResult. `missing_mask` is RECEIVER-DERIVED
    (never a producer self-report) and REQUIRED (non-None) -- an ABSENT
    result with no missing_mask at all is itself a schema violation
    (MALFORMED), not a silently-accepted ABSENT."""
    if missing_mask is None:
        return _route_result_malformed(route_id, ["ABSENT RouteResult requires a non-None 'missing_mask' (receiver-derived)"])
    try:
        result = _route_header(route_id, "ABSENT")
    except RouteResultSchemaError as e:
        return _route_result_malformed(route_id, [str(e)])
    result["missing_mask"] = missing_mask
    return result


def _route_result_malformed(route_id, schema_errors):
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
         (including a plausible-looking "evil/v9"), is MALFORMED.
      2. `route_id` MUST be in the slot the caller expects.
      3. `route_id` MUST be one of VALID_ROUTE_IDS ("R1","R2").
      4. ANY field on `obj` that is not part of {schema_id, route_id,
         route_status} plus this status's own shape fields (plus
         claim_digest/evidence_digest/claim_source_ref/evidence_refs for
         PASS/FAIL) is an unrecognized/foreign field -- MALFORMED.

    Sol 便85 F85-6.3/P85-5 fix, enforced here (item 4: provenance refs are
    REQUIRED, not merely allowed):
      5. for PASS/FAIL, `claim_source_ref` MUST be a well-shaped
         {"source": <str>, "digest": <64-hex>} object, and `evidence_refs`
         MUST be a non-empty list of such objects -- missing, None, or
         ill-shaped is MALFORMED. (This checks SHAPE only; RESOLVING the
         refs against the actual raw evidence and recomputing the digest
         is a receiver-side step this function cannot perform on its own
         -- see `_cross_check_refs_against_raw`, which the public entry
         point always applies afterward.)
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
                f"{unrecognized!r} not part of this status's own shape (Sol 便84 P84-5.4 item 4)",
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

    # Sol 便85 B85-o2: claim_source_ref/evidence_refs are now REQUIRED,
    # non-null, structured -- shape only (resolution against raw evidence
    # happens one layer up, see _cross_check_refs_against_raw).
    claim_source_ref = obj.get("claim_source_ref")
    evidence_refs = obj.get("evidence_refs")
    if not _is_valid_source_ref(claim_source_ref):
        return "MALFORMED", None, {"schema_errors": [
            f"{status} route result requires a structured non-null claim_source_ref "
            f"({{'source': <str>, 'digest': <64-hex>}}), got {claim_source_ref!r} (Sol 便85 B85-o2)",
        ]}
    if not _is_valid_evidence_refs(evidence_refs):
        return "MALFORMED", None, {"schema_errors": [
            f"{status} route result requires a non-empty list of structured evidence_refs, got "
            f"{evidence_refs!r} (Sol 便85 B85-o2)",
        ]}

    if status == "FAIL":
        loci = obj.get("counterexample_loci")
        if not isinstance(loci, list) or len(loci) == 0:
            return "MALFORMED", None, {"schema_errors": ["FAIL route result missing non-empty 'counterexample_loci'"]}
        return "FAIL", claim_digest, {"counterexample_loci": loci, "claim_source_ref": claim_source_ref, "evidence_refs": evidence_refs}

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
    return "PASS", claim_digest, {
        "expected_domain_count": edc, "checked_domain_count": cdc,
        "expected_domain_digest": edd, "coverage_digest": cvd,
        "claim_source_ref": claim_source_ref, "evidence_refs": evidence_refs,
    }


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
# Top-level composition (internal): coerce/re-validate both RouteResults,
# then compose. NOT the untrusted-input trust boundary by itself (Sol 便85
# B85-o1: coerce_to_route_result checks SHAPE, not provenance) -- the
# public entry point below (`evidence_union_from_raw_w6`) is what untrusted
# JSON must go through; this function remains available for white-box
# testing of the composition plumbing on already-constructed RouteResults.
# ============================================================================


def evidence_union_fail_closed_v2(route1, route2):
    """
    Top-level evidence-union/fail-closed-v2 composition (追補(o) v5,
    RouteResult two-layer per 裁定192 N83-2.3, hardened by Sol 便84
    P84-5.4 and 便85 P85-5). `route1`/`route2` should be RouteResult dicts
    built via the _route_result_* constructors, route1 with
    route_id="R1" (the recomputation route) and route2 with
    route_id="R2" (the witness-coverage route). It ALWAYS re-validates
    both arguments via coerce_to_route_result with the slot bound (see
    `expected_route_id` there) -- there is no bypass path that trusts
    route1/route2 as already-valid just because they look like RouteResult
    dicts. Returns:
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

_VERIFIER_B_MODULE = None


def _verifier_b():
    """Dynamically loads ninfty-verifier-b.py (hyphenated filename, so a
    plain `import` statement cannot name it -- same importlib.util
    technique search/test_ninfty_evidence_union.py already uses). Cached
    after first load. This is the RECEIVER-SIDE FIXED DISPATCH target
    (Sol 便85 B85-o1): the only code in this file that is allowed to
    decide a W-6 route's actual status/detail is a call to
    `verify_W6_single` on THIS module, never a caller-supplied
    (status, detail) pair."""
    global _VERIFIER_B_MODULE
    if _VERIFIER_B_MODULE is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "ninfty-verifier-b.py")
        spec = importlib.util.spec_from_file_location("ninfty_verifier_b_for_evidence_union", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _VERIFIER_B_MODULE = mod
    return _VERIFIER_B_MODULE


def _validate_raw_w6_evidence(raw):
    """
    Sol 便85 B85-o1: validates that `raw` is a genuine RAW evidence
    artifact -- {schema_id=RAW_W6_EVIDENCE_SCHEMA_ID, certificate,
    native_a, native_b} -- and NOT a RouteResult or any other shape.
    Returns (ok, certificate, native_a, native_b, errors).
    """
    if not isinstance(raw, dict):
        return False, None, None, None, [f"raw evidence artifact must be an object, got {type(raw).__name__}: {raw!r}"]
    errors = []
    schema_id = raw.get("schema_id")
    if schema_id != RAW_W6_EVIDENCE_SCHEMA_ID:
        errors.append(f"raw evidence artifact schema_id must be exactly {RAW_W6_EVIDENCE_SCHEMA_ID!r}, got {schema_id!r}")
    for key in ("certificate", "native_a", "native_b"):
        if key not in raw:
            errors.append(f"raw evidence artifact missing required key {key!r}")
    if errors:
        return False, None, None, None, errors
    return True, raw["certificate"], raw["native_a"], raw["native_b"], []


def _run_w6_verifier(raw):
    """Receiver-side fixed dispatch (Sol 便85 B85-o1): independently
    invokes ninfty-verifier-b.verify_W6_single on the raw evidence.
    NEVER accepts a caller-supplied (status, detail) pair as a substitute
    -- if `raw` is not a genuine raw evidence artifact, this returns
    MALFORMED itself (schema violation), it does not delegate the
    decision to the caller."""
    ok, cert, native_a, native_b, errors = _validate_raw_w6_evidence(raw)
    if not ok:
        return "MALFORMED", {"schema_errors": errors}
    return _verifier_b().verify_W6_single(cert, native_a, native_b)


def route_from_verifier_b_w6(w6_status, w6_detail, route_id, raw):
    """
    ARMATURE / PLACEHOLDER (not full EP wiring): adapts one
    ninfty-verifier-b.py verify_W6_single(cert, native_a, native_b) result
    -- a (status, detail) pair with status in
    {"ABSENT","MALFORMED","PASS","FAIL"} -- into a RouteResult built via
    the constructors above (route_id = "R1"/"R2", FIXED by the caller's
    dispatch, never inferred from the blob).

    Sol 便85 B85-o3 fix: the four recognized statuses are matched by an
    EXHAUSTIVE if/elif chain; any value not in {"ABSENT","MALFORMED",
    "FAIL","PASS"} falls to an explicit final branch returning MALFORMED
    -- there is no longer an implicit "everything else is PASS" fall-
    through (the literal probe this closes:
    `route_from_verifier_b_w6("BOGUS", detail, "R2", raw).route_status`
    used to be PASS, is now MALFORMED).

    Sol 便85 B85-o4 fix: the PASS branch's domain claim is grounded in the
    REAL two-lane W-6 contract (W6_DOMAIN_LANES) rather than a hardcoded
    placeholder "1" -- expected_domain_count=checked_domain_count=2,
    expected_domain_digest=coverage_digest=sha256_of(sorted(
    W6_DOMAIN_LANES)) (both lanes were actually resolved and compared
    equal by verify_W6_single for this branch to be reached at all).

    `raw` (the raw evidence artifact this adapter was built FROM) is used
    to compute evidence_refs/claim_source_ref's digest as a reference to
    the ACTUAL input, not to the detail dict alone -- Sol 便85 B85-o2:
    `claim_source_ref`/`evidence_refs` are now REQUIRED (no default
    `None`), and the receiver-side `_cross_check_refs_against_raw`
    (applied by the public entry point) independently recomputes this
    same digest from its OWN copy of `raw` and requires equality, closing
    the "self-reported digest comparison only" gap.
    """
    detail_digest = sha256_of(w6_detail if isinstance(w6_detail, dict) else {"detail": w6_detail})
    raw_digest = sha256_of(raw) if isinstance(raw, dict) else sha256_of({"raw": raw})
    claim_source_ref = {"source": "ninfty-verifier-b.verify_W6_single", "artifact": "raw_w6_evidence", "digest": raw_digest}
    evidence_refs = [{"source": "raw_w6_evidence", "digest": raw_digest}]

    if w6_status == "ABSENT":
        reason = (w6_detail or {}).get("reason", "W-6 ABSENT") if isinstance(w6_detail, dict) else "W-6 ABSENT"
        return _route_result_absent(route_id, {"reason": reason})
    if w6_status == "MALFORMED":
        errs = [str((w6_detail or {}).get("reason", w6_detail))] if isinstance(w6_detail, dict) else [str(w6_detail)]
        return _route_result_malformed(route_id, errs)
    if w6_status == "FAIL":
        return _route_result_fail(
            route_id, detail_digest, detail_digest,
            [w6_detail if w6_detail is not None else "W-6 FAIL (no detail supplied)"],
            claim_source_ref=claim_source_ref, evidence_refs=evidence_refs,
        )
    if w6_status == "PASS":
        domain_digest = sha256_of(sorted(W6_DOMAIN_LANES))
        return _route_result_pass(
            route_id, detail_digest, detail_digest,
            expected_domain_count=len(W6_DOMAIN_LANES), checked_domain_count=len(W6_DOMAIN_LANES),
            expected_domain_digest=domain_digest, coverage_digest=domain_digest,
            claim_source_ref=claim_source_ref, evidence_refs=evidence_refs,
        )
    # Sol 便85 B85-o3: exhaustive enum match -- any OTHER value (e.g. the
    # literal probe "BOGUS") is a schema violation, never silently PASS.
    return _route_result_malformed(route_id, [
        f"unrecognized w6_status {w6_status!r} -- exhaustive enum match over "
        "{{'ABSENT','MALFORMED','FAIL','PASS'}}, no implicit fall-through (Sol 便85 B85-o3)",
    ])


def _build_R1(raw):
    """Recomputation route (R1). ALWAYS route_id='R1', fixed by dispatch --
    this function takes NO route_id parameter, so a caller cannot select
    the slot (Sol 便85 P85-5 item 2). Independently invokes the W-6
    verifier on `raw` itself (never a caller-supplied status/detail,
    B85-o1)."""
    w6_status, w6_detail = _run_w6_verifier(raw)
    return route_from_verifier_b_w6(w6_status, w6_detail, "R1", raw)


def _build_R2(raw):
    """Witness-coverage route (R2). ALWAYS route_id='R2'; takes NO route_id
    parameter (item 2). ARMATURE NOTE (Sol 便85 P85-5 item 5, "できない
    部分は UNKNOWN 申告で残し「発効対象外」と明記 -- 発明しない"): this
    codebase currently wires only ONE actual W-6 verifier
    (`verify_W6_single`) -- a second, differently-implemented
    witness-coverage-specific check does NOT exist yet, and this function
    does not fabricate one. R2 therefore derives from the SAME
    receiver-invoked recomputation as R1 (both independently invoked from
    `raw`, never from a caller-supplied status/detail -- so B85-o1 is
    still closed for R2 too), rather than from genuinely independent
    second-implementation evidence. This is an explicit, documented
    limitation, not a silent one."""
    w6_status, w6_detail = _run_w6_verifier(raw)
    return route_from_verifier_b_w6(w6_status, w6_detail, "R2", raw)


def _cross_check_refs_against_raw(route, raw):
    """
    Sol 便85 B85-o2 fix: RESOLVES claim_source_ref/evidence_refs against
    the raw evidence the RECEIVER independently holds (not the route's own
    self-report) and RECOMPUTES the digest -- a route whose refs are
    missing/ill-shaped, or whose declared digest does not match the
    receiver's own sha256_of(raw), is downgraded to MALFORMED here, before
    composition. This is the step `coerce_to_route_result` alone cannot
    perform (it only sees the RouteResult, never the raw evidence) --
    closing the "self-reported digest comparison only" gap Sol's probe
    demonstrated (a route with refs=None used to reach PASS unchallenged).
    Non-PASS/FAIL routes (ABSENT/MALFORMED) pass through unchanged -- they
    carry no claim_source_ref/evidence_refs to check.
    """
    if not isinstance(route, dict) or route.get("route_status") not in ("PASS", "FAIL"):
        return route
    raw_digest = sha256_of(raw) if isinstance(raw, dict) else sha256_of({"raw": raw})
    refs = route.get("evidence_refs")
    src = route.get("claim_source_ref")
    route_id = route.get("route_id") if isinstance(route.get("route_id"), str) else "unknown"
    if not _is_valid_source_ref(src) or not _is_valid_evidence_refs(refs):
        return _route_result_malformed(route_id, [
            f"claim_source_ref/evidence_refs missing or ill-shaped on a {route.get('route_status')} route -- "
            "required, non-null, structured (Sol 便85 P85-5 item 4)",
        ])
    if src.get("digest") != raw_digest or any(r.get("digest") != raw_digest for r in refs):
        return _route_result_malformed(route_id, [
            f"claim_source_ref/evidence_refs digest does not match the receiver's own recomputed raw "
            f"evidence digest {raw_digest!r} -- self-reported digest agreement alone is never sufficient "
            "(Sol 便85 P85-5 item 4/B85-o2)",
        ])
    return route


def evidence_union_from_raw_w6(raw):
    """
    THE public trust-boundary entry point (Sol 便85 P85-5 items 1/6/7):
    accepts a RAW evidence artifact -- {schema_id=RAW_W6_EVIDENCE_SCHEMA_ID,
    certificate, native_a, native_b} -- and NEVER a pre-built RouteResult
    (B85-o1: schema is not provenance; a valid-shape self-asserted
    RouteResult must not reach PASS just by looking right). The
    receiver-side dispatch is FIXED end to end:

      1. `_build_R1(raw)` / `_build_R2(raw)` (item 2: no route_id
         parameter, so a caller cannot choose the slot) each independently
         call `_run_w6_verifier(raw)`, which ALWAYS invokes
         ninfty-verifier-b.verify_W6_single itself on `raw` -- there is no
         path from "caller claims the verifier already said X" to a
         route's status (B85-o1).
      2. `_cross_check_refs_against_raw` resolves each route's provenance
         refs against the SAME `raw` this function was actually called
         with, recomputing the digest rather than trusting the route's
         self-report (item 4/B85-o2).
      3. `evidence_union_fail_closed_v2` re-validates both routes through
         `coerce_to_route_result` (shape/slot/enum, defense in depth) and
         composes via the unchanged 4-rule `compose_route_statuses`.

    Never raises.
    """
    route1 = _cross_check_refs_against_raw(_build_R1(raw), raw)
    route2 = _cross_check_refs_against_raw(_build_R2(raw), raw)
    return evidence_union_fail_closed_v2(route1, route2)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "raw_evidence_json",
        help=(
            "path to a JSON RAW evidence artifact "
            f"{{schema_id: {RAW_W6_EVIDENCE_SCHEMA_ID!r}, certificate, native_a, native_b}}, "
            "or '-' for stdin. This is NOT a pre-built RouteResult -- Sol 便85 B85-o1 closed the "
            "old path that accepted an already-built {route1, route2} pair directly; the "
            "route-specific W-6 verifier is now always invoked by this tool itself."
        ),
    )
    args = ap.parse_args(argv)
    if args.raw_evidence_json == "-":
        raw = json.load(sys.stdin)
    else:
        with open(args.raw_evidence_json, "r", encoding="utf-8") as f:
            raw = json.load(f)
    result = evidence_union_from_raw_w6(raw)
    print(canonical_serialize(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
