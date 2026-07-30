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
  N83-2.1) is UNCHANGED in its rule structure (but is now private, see
  Sol 便86 below).

Sol 便86 P86-2 (docs/notes/cert_shape_interpretation_addendum_o_v6.md,
sol/sol_reply_86_math13.md F86-1.4 B86-o1..o3): three further blockers
found in 便85's v5 repair, three further fixes:

  B86-o1 (public-facade one-ification): EVERY combinator/adapter name that
    used to be public (no leading underscore) is now module-private:
    `compose_route_statuses` -> `_compose_route_statuses`,
    `coerce_to_route_result` -> `_coerce_to_route_result`,
    `evidence_union_fail_closed_v2` -> `_evidence_union_fail_closed_v2`,
    `route_from_verifier_b_w6` -> `_route_from_verifier_result` (also
    generalized to serve BOTH R1 and R2, see B86-o2 below). This module
    now declares `__all__ = ["evidence_union_from_raw_w6"]` -- the ONLY
    name a production caller is meant to import. A structural test
    (search/test_ninfty_evidence_union.py section 8) greps every other
    production file for references to these private names and asserts
    none exist; the suite's own white-box tests are explicitly exempted
    (calling a project's own private helpers directly from its own test
    file is the normal Python convention for testing internals, NOT a
    trust-boundary bypass -- what B86-o1 closes is a PRODUCTION caller
    reaching these names, not a test file).

  B86-o2 (R1/R2 were the same verifier called twice): `_build_R2` now
    calls `_run_w6_verifier_r2`, which dispatches to
    `search/ninfty-verifier-w6-r2.py`'s `verify_W6_single_r2` -- a SECOND,
    INDEPENDENTLY-WRITTEN implementation of the same W-6 predicate that
    shares no helper functions, no constants, and no code with
    `ninfty-verifier-b.py`. Both `_build_R1`/`_build_R2` now record their
    route's `implementation_id` (a fixed string naming the module/function
    that produced it) and `source_digest` (the SHA-256 of that verifier
    module's own file bytes, recomputed fresh every call, never cached
    from a prior claim) on the RouteResult itself (new PASS/FAIL-only
    fields, validated by the constructors and `_coerce_to_route_result`
    exactly like `claim_source_ref`/`evidence_refs`). `evidence_union_from_raw_w6`
    calls the new `_require_distinct_implementations(route1, route2)`
    BEFORE composing: if both routes reached PASS/FAIL and their
    `implementation_id` or `source_digest` AGREE, both are downgraded to
    MALFORMED (-> overall INTEGRITY_STOP) -- this is what makes route
    independence an ENFORCED structural invariant rather than only a
    documentation claim; a future regression that re-wires R2 back onto
    R1's own verifier is caught by this check, not merely documented as a
    known limitation the way 便85's v5 left it.

  B86-o3 (native dereference was never implemented): `ninfty-verifier-b.py`'s
    `_extract_w6_map` used to read ONLY the ref's self-carried `inline`
    copy for `map_ref`, never actually resolving `json_pointer`/`object_id`
    into the receiver's own pinned `native_a`/`native_b` artifact -- so an
    attacker who crafted a certificate, `native_a`, `native_b`, and two
    mutually-consistent (but native-UNBOUND) inline maps could reach PASS.
    FIX (new `_dereference_native_ref` in `ninfty-verifier-b.py`, mirroring
    `ninfty-verifier-a.mjs`'s existing `resolveJsonPointer`/`resolveRef`
    algorithm, ported independently): `map_ref`'s `json_pointer` is now
    resolved AGAINST THE ACTUAL NATIVE ARTIFACT the receiver holds
    (`native_a` for the searcher lane, `native_b` for the checker lane,
    per 裁定150 item 1's "json_pointer resolves within the artifact_id-named
    artifact" convention); the recomputed digest of the DEREFERENCED value
    must equal the ref's own declared `digest`, or this is the existing
    [12] `RefDigestMismatch` condition (-> MALFORMED), never a silent
    PASS. `inline` (if present) is now demoted to a CACHE: it is preferred
    only when the `json_pointer` does not resolve inside the native
    artifact at all (matching the existing fixtures, whose native payloads
    do not yet carry a `/pushforward_map` key -- unaffected, still uses
    `inline` there) -- when the pointer DOES resolve, the dereferenced
    native value is authoritative and inline is not consulted for `map_ref`
    at all. This closes both "matching forged inline maps" (the forged
    digest no longer matches what the pinned native artifact actually
    contains) and "swapped native refs" (the wrong native artifact
    dereferences to the WRONG map, so the digest disagrees with what the
    certificate's ref pinned).

Sol 便87 P87-1 (docs/notes/cert_shape_interpretation_addendum_o_v7.md,
sol/sol_reply_87_math14.md F87-1.2): 便86's B86-o3 fix left HALF of the
attack surface open -- both `ninfty-verifier-b._dereference_native_ref`
(R1) and `ninfty-verifier-w6-r2._load_ref_value` (R2) fell back to
`inline` whenever `json_pointer` was PRESENT but failed to resolve inside
the pinned native artifact, so a producer could hand a self-digest-
consistent FORGED inline map (with NO counterpart in native_a/native_b at
all) alongside `json_pointer="/definitely_missing"` and reach R1=R2=
overall=PASS (UNRESOLVED_POINTER_INLINE_ATTACK; the existing 481-negative
suite only ever exercised POINTERS THAT RESOLVE, never this unresolved-
pointer-plus-inline branch). Two fixes, both items P87-1 1/2:

  1. `_dereference_native_ref`/`_load_ref_value`: an unresolved
     `json_pointer` is now UNCONDITIONALLY a MalformedWitness/W6R2Error
     (-> MALFORMED) -- inline is consulted ONLY when `json_pointer` was
     never supplied in the first place (legacy/offline path, unchanged,
     裁定150 items 2/3). inline is a cache for cross-checking an ALREADY-
     resolved pointer value, never an independent fallback authority.
  2. `_native_provenance_status` (items 2-3): an honest, non-gating
     UNKNOWN annotation (`native_registry_status` on the return value)
     documenting that this codebase has no receiver-held native-artifact
     registry to confirm native_a/native_b provenance or check
     artifact_id against a pinned identity -- not fabricated.

New negatives (search/test_ninfty_evidence_union.py 12): Sol's exact
UNRESOLVED_POINTER_INLINE_ATTACK probe reproduced through R1 alone, R2
alone, and the end-to-end public facade -- all three now MALFORMED/
MALFORMED/INTEGRITY_STOP (were PASS/PASS/PASS pre-fix).

Sol 便88 P88-o (docs/notes/cert_shape_interpretation_addendum_o_v8.md,
sol/sol_reply_88_math15.md F88-3.2): 便87's v7 closed the unresolved-
pointer fallback, but left `native_registry_status` a NON-GATING, honest
"UNKNOWN" annotation -- this function still fed the RAW evidence's OWN
`native_a`/`native_b` straight into both verifiers as if they were
receiver-pinned content. Sol's F88-3.2 probe replaced certificate,
native_a, native_b, and the two refs' digests WHOLESALE with a
self-consistent forged world (including an `artifact_id` matching no
pinned identity) and reached R1=R2=overall=PASS, with
`native_registry_status={"status":"UNKNOWN"}` merely along for the ride.
P88-o's five conditions, all closed here:

  1. `_resolve_native_registry(raw)` (new): the receiver's native content
     is now resolved from `search/ninfty-native-registry.py`'s
     file-backed store (search/certs/ep_registry/) by `artifact_id`,
     NEVER from `raw["native_a"]`/`raw["native_b"]` -- `_run_w6_verifier_r1`/
     `_run_w6_verifier_r2` extract `cert` from `raw` as before but
     DISCARD `raw`'s own native_a/native_b immediately, feeding the
     verifiers ONLY the registry-resolved content (or `{}` when
     resolution fails, which the verifiers already treat as
     ABSENT/MALFORMED -- fail-closed by construction, not a new special
     case).
  2. the registry (search/ninfty-native-registry.py) pins artifact
     identity (`artifact_id`), a whole-artifact digest (freshly
     recomputed from the pinned `content` on every lookup, never trusted
     from a caller claim or even the registry file's own self-reported
     digest field), and a version/freeze id (`version_id`) per entry.
     `raw`'s new, REQUIRED-for-PASS `native_registry_refs` field is the
     caller's CLAIM about which artifact_id/digest/version it expects;
     `_resolve_native_registry` cross-checks that claim against the
     registry's actual pinned values (STALE on disagreement) and against
     the certificate's OWN `map_ref.artifact_id` for that lane
     (ARTIFACT_ID_MISMATCH on disagreement) and against the registry
     entry's own pinned `role` (ROLE_MISMATCH -- the A/B-swap guard).
  3. the pointer resolution itself is UNCHANGED (still
     `_dereference_native_ref`/`_load_ref_value` inside the two
     verifiers) -- it now simply resolves within the REGISTRY-pinned
     artifact instead of the raw-supplied one, and already re-checks the
     resolved value's digest (裁定139/Sol 便86 B86-o3, unaffected).
     `_resolve_native_registry` additionally requires the certificate's
     map_ref to actually CARRY a `json_pointer` at all for that lane
     (LEGACY_UNVERIFIED_REF otherwise, P88-o item 5(f)) -- the legacy
     object_id/inline path never touches the pinned registry artifact, so
     it cannot certify native provenance no matter how well-shaped the
     registry claim is.
  4. `native_registry_status.status == "PASS"` (both `native_a`/`native_b`
     lanes independently PASS in `_resolve_native_registry`) is now a
     GATING precondition for `overall_status == "PASS"`:
     `evidence_union_from_raw_w6` downgrades an otherwise-PASS
     `overall_status` to `"INTEGRITY_STOP"` whenever the registry status
     is not PASS (MISSING/UNKNOWN/STALE/REVOKED/ROLE_MISMATCH/
     ARTIFACT_ID_MISMATCH/LEGACY_UNVERIFIED_REF/MALFORMED, all non-PASS).
     A FAIL/CONFLICT/ABSENT overall_status is left as-is (already
     non-operative, not silently upgraded, not forced to INTEGRITY_STOP
     either -- an explicit FAIL/CONFLICT/ABSENT is itself the "明示的
     non-operative status" P88-o item 4 allows). `main()`'s existing
     fail-closed CLI (nonzero exit for anything but PASS) covers this
     automatically, no separate change needed there.
  5. search/test_ninfty_evidence_union.py section 13 adds all six P88-o
     item 5 negatives (a: full certificate+native_a/native_b replacement,
     b: unknown artifact_id, c: stale digest, d: A/B swap, e: registry
     store absent entirely, f: legacy object_id+inline bypass) plus a
     literal reproduction of Sol's F88-3.2 probe -- all confirmed
     overall_status != "PASS" post-fix. Section 10a's existing positive
     control is upgraded to provision a genuine registry entry and
     confirm overall PASS is still reachable for a properly-registered
     artifact (including a direct demonstration that `raw`'s own,
     deliberately-corrupted top-level `native_a`/`native_b` fields are
     never consulted at all once `native_registry_refs` resolves).

SCOPE NOTE: `search/ninfty-verifier-b.py` and `search/ninfty-verifier-w6-r2.py`
are UNCHANGED by this repair -- P88-o's gating is entirely a
FACADE-level concern (which native content is handed to an otherwise-
unmodified verifier), so their own direct callers (e.g.
search/test_ninfty_laneB.py, which exercises verify_W6_single directly
against fixture-supplied native content, never through the registry) are
unaffected by construction.

CLI NOTE (P86-2's "NOTE"): `main()` now returns a NONZERO exit code for
any `overall_status` other than "PASS" (previously always returned 0
regardless of status) -- a fail-closed CLI, not merely a fail-closed
Python return value.

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

# Sol 便86 P86-2 item 1 (B86-o1): the ONLY name a production caller is
# meant to import from this module. See module docstring's B86-o1 section
# and search/test_ninfty_evidence_union.py section 8 for the structural
# test that greps the rest of the repo for violations.
__all__ = ["evidence_union_from_raw_w6"]

HEX64 = re.compile(r'^[0-9a-f]{64}$', re.IGNORECASE)

ROUTE_STATUSES = ("ABSENT", "MALFORMED", "PASS", "FAIL")
OVERALL_STATUSES = ("ABSENT", "INTEGRITY_STOP", "CONFLICT", "PASS", "FAIL")

HEADER_FIELDS = ("schema_id", "route_id", "route_status")
PASS_ONLY_FIELDS = ("expected_domain_count", "checked_domain_count", "expected_domain_digest", "coverage_digest")
FAIL_ONLY_FIELDS = ("counterexample_loci", "expected_witness", "observed_witness")
ABSENT_ONLY_FIELDS = ("missing_mask",)
MALFORMED_ONLY_FIELDS = ("schema_errors",)
COMMON_PF_FIELDS = ("claim_digest", "evidence_digest", "claim_source_ref", "evidence_refs",
                    "implementation_id", "source_digest")
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

# Sol 便86 P86-2 item 2 (B86-o2): fixed, non-fabricated names identifying
# WHICH implementation produced a route -- R1 = ninfty-verifier-b.py's
# existing verify_W6_single, R2 = the NEW, independently-written
# search/ninfty-verifier-w6-r2.py's verify_W6_single_r2 (no shared helper
# code with R1's implementation). Recorded on every PASS/FAIL RouteResult
# (see COMMON_PF_FIELDS below) alongside a freshly-recomputed source_digest
# of that verifier module's own file bytes (_file_sha256), never a cached
# or self-reported value.
IMPLEMENTATION_ID_R1 = "ninfty-verifier-b.py::verify_W6_single"
IMPLEMENTATION_ID_R2 = "ninfty-verifier-w6-r2.py::verify_W6_single_r2"

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


def _is_nonempty_str(x):
    return isinstance(x, str) and len(x) > 0


def _file_sha256(path):
    """Sol 便86 P86-2 item 2/5: a freshly-recomputed SHA-256 of a verifier
    module's OWN file bytes -- never a value any caller supplies or a
    cached constant, so `_require_distinct_implementations` below is
    comparing genuinely independent, receiver-recomputed facts about which
    code ran, not two copies of a self-reported string."""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


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
                        expected_domain_digest, coverage_digest, *, claim_source_ref, evidence_refs,
                        implementation_id, source_digest):
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
      - implementation_id (non-empty str) and source_digest (exact 64-hex)
        are REQUIRED (Sol 便86 P86-2 item 2/5: every PASS/FAIL RouteResult
        must self-report which implementation produced it, so
        `_require_distinct_implementations` can enforce genuine route
        independence downstream).
    claim_source_ref/evidence_refs/implementation_id/source_digest are
    keyword-only (no positional default) -- every call site must name them
    explicitly.
    A caller that already knows these don't hold should NOT call this
    constructor at all -- see _route_result_fail's coverage-mismatch note.
    """
    try:
        result = _route_header(route_id, "PASS")
        for name, val in (("claim_digest", claim_digest), ("evidence_digest", evidence_digest),
                          ("expected_domain_digest", expected_domain_digest), ("coverage_digest", coverage_digest),
                          ("source_digest", source_digest)):
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
        if not _is_nonempty_str(implementation_id):
            raise RouteResultSchemaError(
                f"PASS RouteResult requires a non-empty string implementation_id, got {implementation_id!r} "
                "(Sol 便86 P86-2 item 2)"
            )
        result.update({
            "claim_digest": claim_digest, "evidence_digest": evidence_digest,
            "claim_source_ref": claim_source_ref, "evidence_refs": evidence_refs,
            "expected_domain_count": expected_domain_count, "checked_domain_count": checked_domain_count,
            "expected_domain_digest": expected_domain_digest, "coverage_digest": coverage_digest,
            "implementation_id": implementation_id, "source_digest": source_digest,
        })
        return result
    except RouteResultSchemaError as e:
        return _route_result_malformed(route_id, [str(e)])


def _route_result_fail(route_id, claim_digest, evidence_digest, counterexample_loci, *,
                        claim_source_ref, evidence_refs, implementation_id, source_digest,
                        expected_witness=None, observed_witness=None):
    """Builds a FAIL RouteResult. VALIDATES claim_digest/evidence_digest
    (64-hex), counterexample_loci (non-empty list, F83-2.1's structured
    requirement), claim_source_ref/evidence_refs (Sol 便85 B85-o2:
    required, non-null, structured, no default), and implementation_id/
    source_digest (Sol 便86 P86-2 item 2/5: required, non-empty str /
    64-hex) -- otherwise falls back to MALFORMED (never silently accepts a
    FAIL with no actual counterexample evidence or no genuine provenance).
    claim_source_ref/evidence_refs/implementation_id/source_digest are
    keyword-only."""
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
    if not _is_nonempty_str(implementation_id) or not _is_64hex(source_digest):
        return _route_result_malformed(route_id, [
            f"FAIL RouteResult requires a non-empty implementation_id and exact-64-hex source_digest, got "
            f"{implementation_id!r}/{source_digest!r} (Sol 便86 P86-2 item 2)",
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
        "implementation_id": implementation_id, "source_digest": source_digest,
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


def _coerce_to_route_result(obj, expected_route_id=None):
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

    # Sol 便86 P86-2 item 2: implementation_id/source_digest are now
    # REQUIRED on every PASS/FAIL route (non-empty str / exact 64-hex) --
    # shape only; `_require_distinct_implementations` (applied one layer
    # up, mirroring `_cross_check_refs_against_raw`) is what actually
    # enforces that R1 and R2 disagree on these values.
    implementation_id = obj.get("implementation_id")
    source_digest = obj.get("source_digest")
    if not _is_nonempty_str(implementation_id) or not _is_64hex(source_digest):
        return "MALFORMED", None, {"schema_errors": [
            f"{status} route result requires a non-empty implementation_id and exact-64-hex source_digest, "
            f"got {implementation_id!r}/{source_digest!r} (Sol 便86 P86-2 item 2)",
        ]}

    if status == "FAIL":
        loci = obj.get("counterexample_loci")
        if not isinstance(loci, list) or len(loci) == 0:
            return "MALFORMED", None, {"schema_errors": ["FAIL route result missing non-empty 'counterexample_loci'"]}
        return "FAIL", claim_digest, {
            "counterexample_loci": loci, "claim_source_ref": claim_source_ref, "evidence_refs": evidence_refs,
            "implementation_id": implementation_id, "source_digest": source_digest,
        }

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
        "implementation_id": implementation_id, "source_digest": source_digest,
    }


# ============================================================================
# Composition (追補(o) v3.1 "合成の全域関数", N83-2.1 confirmed PASS): TOTAL
# over the 4x4=16 (route_status, route_status) domain, swap-symmetric,
# exactly the 4 ordered rules below -- UNCHANGED in structure. 裁定192
# F83-2.2 adds ONE defensive layer: a PASS/FAIL status paired with a
# non-64-hex digest is ITSELF escalated to INTEGRITY_STOP even when this
# low-level function is called directly (bypassing coerce_to_route_result).
# ============================================================================


def _compose_route_statuses(status1, claim_digest1, status2, claim_digest2):
    """
    Composes two ALREADY-CLASSIFIED route statuses into ONE overall
    status. TOTAL (defined for every (status1, status2) in
    ROUTE_STATUSES x ROUTE_STATUSES) and SWAP-SYMMETRIC. Rules, IN ORDER:

      0. (裁定192 F83-2.2, defense in depth) a PASS/FAIL status paired with
         a digest that is not exact 64-hex -> INTEGRITY_STOP (this low-level
         API must not be more permissive than _coerce_to_route_result, even
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
            raise ValueError(f"_compose_route_statuses: not a valid route_status: {s!r}")

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


def _evidence_union_fail_closed_v2(route1, route2):
    """
    Top-level evidence-union/fail-closed-v2 composition (追補(o) v5,
    RouteResult two-layer per 裁定192 N83-2.3, hardened by Sol 便84
    P84-5.4 and 便85 P85-5; renamed module-private per Sol 便86 P86-2 item 1
    -- B86-o1). `route1`/`route2` should be RouteResult dicts
    built via the _route_result_* constructors, route1 with
    route_id="R1" (the recomputation route) and route2 with
    route_id="R2" (the witness-coverage route). It ALWAYS re-validates
    both arguments via _coerce_to_route_result with the slot bound (see
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
    s1, d1, detail1 = _coerce_to_route_result(route1, expected_route_id="R1")
    s2, d2, detail2 = _coerce_to_route_result(route2, expected_route_id="R2")
    overall = _compose_route_statuses(s1, d1, s2, d2)
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
_VERIFIER_R2_MODULE = None
_NATIVE_REGISTRY_MODULE = None


def _verifier_b():
    """Dynamically loads ninfty-verifier-b.py (hyphenated filename, so a
    plain `import` statement cannot name it -- same importlib.util
    technique search/test_ninfty_evidence_union.py already uses). Cached
    after first load. This is the RECEIVER-SIDE FIXED DISPATCH target for
    R1 (Sol 便85 B85-o1): the only code in this file that is allowed to
    decide R1's actual status/detail is a call to `verify_W6_single` on
    THIS module, never a caller-supplied (status, detail) pair."""
    global _VERIFIER_B_MODULE
    if _VERIFIER_B_MODULE is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "ninfty-verifier-b.py")
        spec = importlib.util.spec_from_file_location("ninfty_verifier_b_for_evidence_union", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _VERIFIER_B_MODULE = mod
    return _VERIFIER_B_MODULE


def _verifier_r2():
    """Sol 便86 P86-2 item 2 (B86-o2): dynamically loads the SECOND,
    independently-written search/ninfty-verifier-w6-r2.py (same importlib
    technique as _verifier_b -- but a wholly separate file, sharing no
    helper functions or constants with ninfty-verifier-b.py). This is the
    RECEIVER-SIDE FIXED DISPATCH target for R2 -- the only code in this
    file that decides R2's status/detail is a call to
    `verify_W6_single_r2` on THIS module, never anything derived from R1's
    call or R1's result."""
    global _VERIFIER_R2_MODULE
    if _VERIFIER_R2_MODULE is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "ninfty-verifier-w6-r2.py")
        spec = importlib.util.spec_from_file_location("ninfty_verifier_w6_r2_for_evidence_union", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _VERIFIER_R2_MODULE = mod
    return _VERIFIER_R2_MODULE


def _registry():
    """Sol 便88 P88-o item 1: dynamically loads the receiver-held native
    registry (search/ninfty-native-registry.py) -- same importlib
    technique as `_verifier_b`/`_verifier_r2`. This module calls ONLY
    `resolve(artifact_id)` on it, never `write_entry` -- provisioning the
    registry is an out-of-band receiver step this facade never performs
    while processing a caller-supplied `raw` evidence artifact."""
    global _NATIVE_REGISTRY_MODULE
    if _NATIVE_REGISTRY_MODULE is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "ninfty-native-registry.py")
        spec = importlib.util.spec_from_file_location("ninfty_native_registry_for_evidence_union", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _NATIVE_REGISTRY_MODULE = mod
    return _NATIVE_REGISTRY_MODULE


def _cert_side_artifact_ids(cert):
    """
    Sol 便88 P88-o item 2 support: reads, PURELY DESCRIPTIVELY (this
    function raises nothing and tolerates any shape), the certificate's
    OWN `pushforward_compatibility_witness` entries to learn, per lane
    ("searcher"/"checker"), (a) the `map_ref.artifact_id` the certificate
    itself declares and (b) whether that `map_ref` carries a `json_pointer`
    at all. `_resolve_native_registry` uses (a) to cross-check against the
    raw's `native_registry_refs` claim (ARTIFACT_ID_MISMATCH on
    disagreement) and (b) to detect the legacy object_id/inline bypass
    (LEGACY_UNVERIFIED_REF, P88-o item 5(f)) -- a lane whose map_ref never
    carries a json_pointer never actually dereferences against the pinned
    registry artifact, no matter how well the registry claim itself
    checks out.
    """
    ids, has_ptr = {}, {}
    if not isinstance(cert, dict):
        return ids, has_ptr
    entries = cert.get("pushforward_compatibility_witness")
    if not isinstance(entries, list):
        return ids, has_ptr
    for e in entries:
        if not isinstance(e, dict):
            continue
        side = e.get("native_side")
        if side not in ("searcher", "checker") or side in ids:
            continue
        map_ref = e.get("map_ref")
        if not isinstance(map_ref, dict):
            continue
        ids[side] = map_ref.get("artifact_id")
        has_ptr[side] = isinstance(map_ref.get("json_pointer"), str)
    return ids, has_ptr


# Sol 便88 P88-o item 4: the full set of non-PASS native_registry_status
# values this facade can report, in a fixed priority order used to pick
# ONE overall status when native_a/native_b disagree on their own status
# (e.g. one side PASS, one side STALE) -- earlier entries win. All of
# these are non-operative for gating purposes (see
# `evidence_union_from_raw_w6`): only "PASS" (both lanes PASS) permits an
# otherwise-PASS union to remain overall PASS.
_REGISTRY_STATUS_PRIORITY = (
    "MALFORMED", "MISSING", "UNKNOWN", "REVOKED", "ROLE_MISMATCH",
    "ARTIFACT_ID_MISMATCH", "STALE", "LEGACY_UNVERIFIED_REF",
)


def _resolve_native_registry(raw):
    """
    Sol 便88 P88-o items 1-3/5: resolves the ACTUAL native_a/native_b
    content this facade will hand to the two W-6 verifiers, from the
    receiver-held registry (`_registry().resolve`) -- `raw`'s own
    `native_a`/`native_b` fields are NEVER read here at all (P88-o item 1:
    "raw 内の native_a/native_b を authority として受け取らない" --
    literally, this function's body never once indexes into
    `raw["native_a"]`/`raw["native_b"]`).

    `raw["native_registry_refs"]` is the caller's CLAIM about which
    registry artifact backs each slot:
      {"native_a": {"artifact_id": <str>, "whole_artifact_digest": <64hex>,
                     "version_id": <str, optional>},
       "native_b": {...}}
    This claim is cross-checked, never trusted:
      - ref missing/ill-shaped                                -> MISSING
      - artifact_id not registered, registry store absent      -> MISSING
      - artifact_id not registered, registry store present     -> UNKNOWN
      - registry entry status != ACTIVE                        -> REVOKED
      - registry entry's pinned role != this slot (A/B swap)   -> ROLE_MISMATCH
      - claimed whole_artifact_digest != receiver's actual one -> STALE
      - claimed version_id (if given) != receiver's actual one -> STALE
      - certificate's own map_ref.artifact_id for this lane
        disagrees with the claimed artifact_id                 -> ARTIFACT_ID_MISMATCH
      - certificate's map_ref for this lane has no json_pointer
        (legacy object_id/inline path, never touches registry) -> LEGACY_UNVERIFIED_REF
      - otherwise                                               -> PASS

    Returns (overall_status, native_a_content, native_b_content, detail):
    overall_status is "PASS" iff BOTH lanes are "PASS"; otherwise the
    highest-priority non-PASS status across both lanes (`_REGISTRY_STATUS_PRIORITY`).
    native_a_content/native_b_content are the REGISTRY-pinned `content`
    for lanes that resolved PASS, else `{}` (the verifiers already treat
    a non-dict/empty native payload as ABSENT/MALFORMED, so this is not a
    new special case). `detail` is `{"native_a": {...}, "native_b": {...}}`,
    each with its own "status"/"reason".
    """
    if not isinstance(raw, dict):
        d = {"status": "MALFORMED", "reason": "raw evidence artifact is not an object"}
        return "MALFORMED", {}, {}, {"native_a": d, "native_b": d}

    refs = raw.get("native_registry_refs")
    cert_ids, cert_has_ptr = _cert_side_artifact_ids(raw.get("certificate"))
    reg = _registry()

    side_results = {}
    contents = {}
    for reg_side, cert_side in (("native_a", "searcher"), ("native_b", "checker")):
        ref = refs.get(reg_side) if isinstance(refs, dict) else None
        if not (
            isinstance(ref, dict)
            and _is_nonempty_str(ref.get("artifact_id"))
            and _is_64hex(ref.get("whole_artifact_digest"))
            and _is_nonempty_str(ref.get("version_id"))
        ):
            side_results[reg_side] = {
                "status": "MISSING",
                "reason": (
                    f"raw carries no well-shaped native_registry_refs[{reg_side!r}] "
                    "({'artifact_id': <str>, 'whole_artifact_digest': <64hex>, 'version_id': <non-empty str>}) "
                    "-- receiver-held registry lookup was never attempted; raw's own native_a/native_b fields "
                    "are never authority (Sol 便88 P88-o item 1). version_id is REQUIRED (Sol 便89 fix: an "
                    "omitted version_id used to silently skip the version check below and could still reach "
                    "PASS -- now it fails closed here instead, same bucket as an omitted artifact_id)"
                ),
            }
            continue
        entry = reg.resolve(ref["artifact_id"])
        if entry is None:
            if not reg.index_exists():
                side_results[reg_side] = {
                    "status": "MISSING",
                    "reason": "the receiver-held registry store itself is absent entirely (no index) -- P88-o item 5(e)",
                }
            else:
                side_results[reg_side] = {
                    "status": "UNKNOWN",
                    "reason": f"artifact_id {ref['artifact_id']!r} is not registered in the receiver-held registry -- P88-o item 5(b)",
                }
            continue
        if entry.get("status") != "ACTIVE":
            side_results[reg_side] = {
                "status": "REVOKED",
                "reason": f"artifact_id {ref['artifact_id']!r} has registry status {entry.get('status')!r}, not ACTIVE",
            }
            continue
        if entry.get("role") != reg_side:
            side_results[reg_side] = {
                "status": "ROLE_MISMATCH",
                "reason": (
                    f"artifact_id {ref['artifact_id']!r} is pinned in the registry with role "
                    f"{entry.get('role')!r}, but native_registry_refs used it for {reg_side!r} -- "
                    "A/B swap guard, P88-o item 5(d)"
                ),
            }
            continue
        if entry.get("whole_artifact_digest") != ref["whole_artifact_digest"]:
            side_results[reg_side] = {
                "status": "STALE",
                "reason": (
                    f"raw's claimed whole_artifact_digest for {reg_side!r} does not match the receiver's "
                    "currently-pinned artifact digest -- P88-o item 5(c)"
                ),
            }
            continue
        claimed_version = ref.get("version_id")
        # Sol 便89 fix: version_id is now REQUIRED-and-well-shaped by the
        # well-shaped-ref gate above (an omitted/empty version_id already
        # produced MISSING and `continue`d before reaching this line) --
        # so this comparison is now UNCONDITIONAL, no more "skip if
        # absent" branch that could bypass the version check entirely.
        if claimed_version != entry.get("version_id"):
            side_results[reg_side] = {
                "status": "STALE",
                "reason": f"raw's claimed version_id {claimed_version!r} does not match the pinned version {entry.get('version_id')!r}",
            }
            continue
        cert_artifact_id = cert_ids.get(cert_side)
        if cert_artifact_id != ref["artifact_id"]:
            side_results[reg_side] = {
                "status": "ARTIFACT_ID_MISMATCH",
                "reason": (
                    f"certificate's {cert_side} map_ref.artifact_id ({cert_artifact_id!r}) does not match "
                    f"native_registry_refs[{reg_side!r}].artifact_id ({ref['artifact_id']!r})"
                ),
            }
            continue
        if not cert_has_ptr.get(cert_side):
            side_results[reg_side] = {
                "status": "LEGACY_UNVERIFIED_REF",
                "reason": (
                    f"certificate's {cert_side} map_ref has no json_pointer -- the legacy object_id/inline "
                    "path never dereferences against the pinned registry artifact, so it cannot certify "
                    "native provenance -- P88-o item 5(f)"
                ),
            }
            continue
        side_results[reg_side] = {"status": "PASS", "reason": "resolved against the pinned registry artifact"}
        contents[reg_side] = entry["content"]

    statuses = {v["status"] for v in side_results.values()}
    overall = "PASS" if statuses == {"PASS"} else next(s for s in _REGISTRY_STATUS_PRIORITY if s in statuses)
    return overall, contents.get("native_a", {}), contents.get("native_b", {}), side_results


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


def _run_w6_verifier_r1(raw):
    """Receiver-side fixed dispatch for R1 (Sol 便85 B85-o1): independently
    invokes ninfty-verifier-b.verify_W6_single on the raw evidence.
    NEVER accepts a caller-supplied (status, detail) pair as a substitute
    -- if `raw` is not a genuine raw evidence artifact, this returns
    MALFORMED itself (schema violation), it does not delegate the
    decision to the caller.

    Sol 便88 P88-o item 1: `raw`'s OWN native_a/native_b (returned by
    `_validate_raw_w6_evidence` as `_raw_native_a`/`_raw_native_b` below)
    are intentionally DISCARDED -- never passed to the verifier. Instead,
    `_resolve_native_registry(raw)` resolves the receiver-held, registry-
    pinned content (or `{}` per lane when resolution fails, which the
    verifier already treats as ABSENT/MALFORMED)."""
    ok, cert, _raw_native_a, _raw_native_b, errors = _validate_raw_w6_evidence(raw)
    if not ok:
        return "MALFORMED", {"schema_errors": errors}
    _, native_a, native_b, _ = _resolve_native_registry(raw)
    return _verifier_b().verify_W6_single(cert, native_a, native_b)


def _run_w6_verifier_r2(raw):
    """Sol 便86 P86-2 item 2 (B86-o2): receiver-side fixed dispatch for R2
    -- independently invokes ninfty-verifier-w6-r2.verify_W6_single_r2 (a
    SEPARATE implementation from R1's verify_W6_single, sharing no helper
    code) on the SAME raw evidence. Same fail-closed non-raw-evidence
    handling as _run_w6_verifier_r1, and the SAME Sol 便88 P88-o item 1
    discard-and-resolve-from-registry treatment of native_a/native_b."""
    ok, cert, _raw_native_a, _raw_native_b, errors = _validate_raw_w6_evidence(raw)
    if not ok:
        return "MALFORMED", {"schema_errors": errors}
    _, native_a, native_b, _ = _resolve_native_registry(raw)
    return _verifier_r2().verify_W6_single_r2(cert, native_a, native_b)


def _route_from_verifier_result(w6_status, w6_detail, route_id, raw, implementation_id, source_digest):
    """
    ARMATURE / PLACEHOLDER (not full EP wiring): adapts one W-6 verifier's
    (status, detail) result -- status in
    {"ABSENT","MALFORMED","PASS","FAIL"} -- into a RouteResult built via
    the constructors above (route_id = "R1"/"R2", FIXED by the caller's
    dispatch, never inferred from the blob). Sol 便86 P86-2: this adapter
    is now shared by BOTH _build_R1 and _build_R2 -- it only formats a
    (status, detail) pair into a RouteResult shape and does not itself
    decide which verifier ran; `implementation_id`/`source_digest` (the
    caller-supplied facts about WHICH verifier produced w6_status/w6_detail)
    are threaded straight onto the PASS/FAIL RouteResult, never invented
    here.

    Sol 便85 B85-o3 fix: the four recognized statuses are matched by an
    EXHAUSTIVE if/elif chain; any value not in {"ABSENT","MALFORMED",
    "FAIL","PASS"} falls to an explicit final branch returning MALFORMED
    -- there is no longer an implicit "everything else is PASS" fall-
    through (the literal probe this closes:
    `_route_from_verifier_result("BOGUS", detail, "R2", raw, ...).route_status`
    used to be PASS, is now MALFORMED).

    Sol 便85 B85-o4 fix: the PASS branch's domain claim is grounded in the
    REAL two-lane W-6 contract (W6_DOMAIN_LANES) rather than a hardcoded
    placeholder "1" -- expected_domain_count=checked_domain_count=2,
    expected_domain_digest=coverage_digest=sha256_of(sorted(
    W6_DOMAIN_LANES)) (both lanes were actually resolved and compared
    equal by the verifier for this branch to be reached at all).

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
    claim_source_ref = {"source": implementation_id, "artifact": "raw_w6_evidence", "digest": raw_digest}
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
            implementation_id=implementation_id, source_digest=source_digest,
        )
    if w6_status == "PASS":
        domain_digest = sha256_of(sorted(W6_DOMAIN_LANES))
        return _route_result_pass(
            route_id, detail_digest, detail_digest,
            expected_domain_count=len(W6_DOMAIN_LANES), checked_domain_count=len(W6_DOMAIN_LANES),
            expected_domain_digest=domain_digest, coverage_digest=domain_digest,
            claim_source_ref=claim_source_ref, evidence_refs=evidence_refs,
            implementation_id=implementation_id, source_digest=source_digest,
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
    the slot (Sol 便85 P85-5 item 2). Independently invokes ninfty-verifier-b's
    verify_W6_single on `raw` itself (never a caller-supplied status/detail,
    B85-o1). Records `implementation_id`=IMPLEMENTATION_ID_R1 and a
    freshly-recomputed `source_digest` of ninfty-verifier-b.py's own file
    bytes (Sol 便86 P86-2 item 2)."""
    w6_status, w6_detail = _run_w6_verifier_r1(raw)
    here = os.path.dirname(os.path.abspath(__file__))
    src_digest = _file_sha256(os.path.join(here, "ninfty-verifier-b.py"))
    return _route_from_verifier_result(w6_status, w6_detail, "R1", raw, IMPLEMENTATION_ID_R1, src_digest)


def _build_R2(raw):
    """Witness-coverage route (R2). ALWAYS route_id='R2'; takes NO route_id
    parameter (item 2). Sol 便86 P86-2 item 2 (B86-o2 fix): R2 now
    independently invokes ninfty-verifier-w6-r2.verify_W6_single_r2 -- a
    SECOND, separately-written implementation of the same W-6 predicate,
    sharing no helper functions or constants with R1's ninfty-verifier-b.py
    (previously R2 called the SAME verify_W6_single as R1, an explicitly
    documented but unresolved limitation -- this closes it). Records
    `implementation_id`=IMPLEMENTATION_ID_R2 and a freshly-recomputed
    `source_digest` of ninfty-verifier-w6-r2.py's own file bytes."""
    w6_status, w6_detail = _run_w6_verifier_r2(raw)
    here = os.path.dirname(os.path.abspath(__file__))
    src_digest = _file_sha256(os.path.join(here, "ninfty-verifier-w6-r2.py"))
    return _route_from_verifier_result(w6_status, w6_detail, "R2", raw, IMPLEMENTATION_ID_R2, src_digest)


def _require_distinct_implementations(route1, route2):
    """
    Sol 便86 P86-2 item 5: an OPERATIVE union requires R1 and R2 to be
    built from genuinely DIFFERENT implementations, not merely different
    route_id labels wrapping the same underlying call (B86-o2's original
    defect). Enforced STRUCTURALLY, not just documented: if both routes
    reached PASS/FAIL and their self-reported `implementation_id` OR
    `source_digest` agree, that is exactly the "same verifier called
    twice" condition reappearing -- both routes are downgraded to
    MALFORMED here (-> overall INTEGRITY_STOP via composition), so a
    future regression that re-wires R2 back onto R1's own verifier is
    CAUGHT by this suite, not merely left as a documented limitation.
    Routes that are not both PASS/FAIL (e.g. one or both ABSENT) pass
    through unchanged -- there is no "same claim" being disputed yet.
    """
    if not isinstance(route1, dict) or not isinstance(route2, dict):
        return route1, route2
    if route1.get("route_status") not in ("PASS", "FAIL") or route2.get("route_status") not in ("PASS", "FAIL"):
        return route1, route2
    impl1, src1 = route1.get("implementation_id"), route1.get("source_digest")
    impl2, src2 = route2.get("implementation_id"), route2.get("source_digest")
    if impl1 == impl2 or src1 == src2:
        reason = (
            f"R1/R2 implementation independence violated: implementation_id {impl1!r}=={impl2!r} "
            f"or source_digest {src1!r}=={src2!r} -- an operative two-route union requires genuinely "
            "distinct implementations (Sol 便86 P86-2 item 5 / B86-o2)"
        )
        route_id1 = route1.get("route_id") if isinstance(route1.get("route_id"), str) else "R1"
        route_id2 = route2.get("route_id") if isinstance(route2.get("route_id"), str) else "R2"
        return _route_result_malformed(route_id1, [reason]), _route_result_malformed(route_id2, [reason])
    return route1, route2


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
    THE public trust-boundary entry point (Sol 便85 P85-5 items 1/6/7; the
    ONLY name this module exports, Sol 便86 P86-2 item 1/B86-o1, see
    __all__): accepts a RAW evidence artifact --
    {schema_id=RAW_W6_EVIDENCE_SCHEMA_ID, certificate, native_a, native_b,
    native_registry_refs (optional; Sol 便88 P88-o -- REQUIRED for
    overall_status to reach PASS, see step 5 below)} -- and NEVER a
    pre-built RouteResult (B85-o1: schema is not provenance; a valid-shape
    self-asserted RouteResult must not reach PASS just by looking right).
    `native_a`/`native_b` remain required KEYS for backward-compatible raw
    shape validation (`_validate_raw_w6_evidence`), but their VALUES are
    never used as native-content authority any more (P88-o item 1) -- see
    step 1. The receiver-side dispatch is FIXED end to end:

      1. `_build_R1(raw)` / `_build_R2(raw)` (item 2: no route_id
         parameter, so a caller cannot choose the slot) each independently
         invoke a SEPARATE verifier implementation on `raw` -- R1 calls
         ninfty-verifier-b.verify_W6_single, R2 calls the independently
         written ninfty-verifier-w6-r2.verify_W6_single_r2 (Sol 便86
         P86-2 item 2/B86-o2) -- there is no path from "caller claims a
         verifier already said X" to a route's status (B85-o1). Both, in
         turn, resolve every map_ref's json_pointer against the pinned
         native artifact ONLY -- an unresolved json_pointer is now an
         unconditional MALFORMED, never an inline fallback (Sol 便87
         P87-1 item 1, closing UNRESOLVED_POINTER_INLINE_ATTACK). Sol 便88
         P88-o item 1: "the pinned native artifact" here means the
         REGISTRY-resolved content from `_resolve_native_registry(raw)`,
         never `raw["native_a"]`/`raw["native_b"]` themselves (see
         `_run_w6_verifier_r1`/`_run_w6_verifier_r2`).
      2. `_cross_check_refs_against_raw` resolves each route's provenance
         refs against the SAME `raw` this function was actually called
         with, recomputing the digest rather than trusting the route's
         self-report (item 4/B85-o2).
      3. `_require_distinct_implementations` (Sol 便86 P86-2 item 5)
         downgrades BOTH routes to MALFORMED if their self-reported
         implementation_id/source_digest agree -- route independence is
         enforced here, not merely documented.
      4. `_evidence_union_fail_closed_v2` re-validates both routes through
         `_coerce_to_route_result` (shape/slot/enum, defense in depth) and
         composes via the unchanged 4-rule `_compose_route_statuses`.
      5. Sol 便88 P88-o: `_resolve_native_registry(raw)` is now a GATING
         check, not a non-gating annotation -- `native_a`/`native_b` fed
         to BOTH verifiers in step 1 already came exclusively from this
         same resolution (see `_run_w6_verifier_r1`/`_run_w6_verifier_r2`;
         `raw`'s own `native_a`/`native_b` fields are never consulted for
         W-6 native content at all). Here, if `overall_status` reached
         "PASS" from step 4 but `native_registry_status` is anything other
         than "PASS" (MISSING/UNKNOWN/STALE/REVOKED/ROLE_MISMATCH/
         ARTIFACT_ID_MISMATCH/LEGACY_UNVERIFIED_REF/MALFORMED),
         `overall_status` is downgraded to "INTEGRITY_STOP" -- P88-o item
         4's gating precondition, closing F88-3.2's full-replacement
         attack (which relied on `native_registry_status` being present
         but non-gating). A non-PASS `overall_status` (FAIL/CONFLICT/
         ABSENT/INTEGRITY_STOP) is left as-is: already non-operative, not
         silently upgraded, and itself an explicit "non-operative status"
         per P88-o item 4's own wording.

    Never raises.
    """
    route1 = _cross_check_refs_against_raw(_build_R1(raw), raw)
    route2 = _cross_check_refs_against_raw(_build_R2(raw), raw)
    route1, route2 = _require_distinct_implementations(route1, route2)
    result = _evidence_union_fail_closed_v2(route1, route2)
    registry_status, _, _, registry_detail = _resolve_native_registry(raw)
    if result.get("overall_status") == "PASS" and registry_status != "PASS":
        result["overall_status"] = "INTEGRITY_STOP"
    result["native_registry_status"] = {"status": registry_status, "detail": registry_detail}
    return result


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "raw_evidence_json",
        help=(
            "path to a JSON RAW evidence artifact "
            f"{{schema_id: {RAW_W6_EVIDENCE_SCHEMA_ID!r}, certificate, native_a, native_b}}, "
            "or '-' for stdin. This is NOT a pre-built RouteResult -- Sol 便85 B85-o1 closed the "
            "old path that accepted an already-built {route1, route2} pair directly; the "
            "route-specific W-6 verifiers are now always invoked by this tool itself."
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
    # Sol 便86 P86-2 NOTE: fail-closed CLI -- nonzero exit for anything
    # other than overall_status="PASS" (previously always returned 0).
    return 0 if result.get("overall_status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
