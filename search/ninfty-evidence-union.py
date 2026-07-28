#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-evidence-union.py

evidence-union/fail-closed-v2 (追補(o) v3.1,
docs/notes/cert_shape_interpretation_addendum_o_v3.md; Sol F81-3.2/F82-4.1,
sol/sol_reply_82_math9.md N82-4.1). A GENERAL two-route composition
function -- NOT W-6-specific (P80-D/P81-E: "複数証明経路の共通規則") --
for combining two independent evidence routes (e.g. R1 = recomputation
route, R2 = witness-coverage route) into ONE overall status, fail-closed
and TOTAL (defined on every input pair) and SWAP-SYMMETRIC.

SCOPE NOTE (read before extending): this is a NEW component, not a repair
of an existing bug. The addendum text specifies the COMPOSITION function
(`compose_route_statuses` below) precisely and completely: 4 ordered
rules, total over the 4x4 = 16 status-pair domain, swap-symmetric -- this
is implemented LITERALLY and is the part with a crisp, fully-specified
contract (table-driven-tested exhaustively, see
search/test_ninfty_evidence_union.py).

The route-BLOB shape and the blob -> route_status CLASSIFICATION function
(`classify_route` below) are NOT fully pinned by the addendum text (it
states required-field RULES -- "PASS/FAIL の共通必須欄は claim_digest +
evidence_digest", "PASS は checked_domain_count + coverage_digest の
receiver-derived expected domain digest との一致" -- but not a literal
JSON schema for the route blob itself, nor whether the raw blob carries
any self-declared "what kind of route is this" hint at all). This
implementer's `classify_route` is this file's OWN concretization of those
required-field rules, documented explicitly in its docstring, flagged as
interpretation/candidate exactly like the schema itself -- pending Sol
confirmation, same status as the addendum document it implements.

Per the coordinator's task scope for this round: the W-6 connection point
(`route_from_verifier_b_w6` below) is an ARMATURE ONLY -- it adapts
ninfty-verifier-b.py's verify_W6_single(...) output into a route blob this
module's classify_route can consume, but is NOT wired into the EP runner
in this round (EP v7 wiring is a separate, later step). It is a
placeholder bridge, not a claim that W-6's real R1/R2 evidence has been
fully migrated to this route-blob schema.

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


def canonical_serialize(obj):
    """Project-wide canonical form: UTF-8, sorted keys, no whitespace --
    same convention as ninfty-verifier-b.py / ninfty-cert-validator.py /
    ninfty-legacy-normalizer.py."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def _is_64hex(x):
    return isinstance(x, str) and bool(HEX64.match(x))


# ============================================================================
# Classification (受領側の義務): route blob -> (route_status, claim_digest,
# detail). route_status is ALWAYS a RECEIVER output, never trusted from a
# producer-supplied field (追補(o) v3.1 "分類": "route_status は producer
# 入力でなく受領 verifier の出力欄").
# ============================================================================


def classify_route(blob, expected_domain_digest=None):
    """
    Classifies ONE evidence route blob into (route_status, claim_digest,
    detail). route_status in {"ABSENT","MALFORMED","PASS","FAIL"}.
    claim_digest is the route's own claim_digest string when route_status
    in {"PASS","FAIL"}, else None.

    Adopted route blob shape (this file's interpretation, see module
    docstring SCOPE NOTE):
      {
        "evidence_kind": "PASS"|"FAIL"|"ABSENT"|None,  # producer's own
            # claim of what kind of route this is -- used ONLY to decide
            # which required-field set to structurally check against;
            # NEVER trusted as the final route_status. A blob with no
            # `evidence_kind` at all is classified purely from which
            # fields are structurally present (see below).
        "claim_digest": "<64-hex>",       # REQUIRED for PASS/FAIL (F82-4.1)
        "evidence_digest": "<64-hex>",    # REQUIRED for PASS/FAIL (v2, kept)
        "checked_domain_count": <int>,    # REQUIRED for PASS
        "coverage_digest": "<64-hex>",    # REQUIRED for PASS
        "counterexample_locus": <any, not None>,  # REQUIRED for FAIL
      }
    `expected_domain_digest` (a 64-hex string, or None if the caller has no
    independently-derived expected-domain digest to check against) is
    supplied BY THE CALLER (this module never derives it itself -- the
    real native-artifact-derived expected domain digest computation is out
    of this module's scope, matching v3.1's "expected domain は native
    divisor/map digest から受領側が導出する" -- that derivation belongs to
    whichever caller holds the native artifacts, e.g. lane B's verifier).
    If supplied and it disagrees with the route's own coverage_digest, the
    route's claimed full coverage is FALSIFIED by the receiver's own
    derivation -- this is scored as FAIL (a substantive/evidentiary
    disagreement), not MALFORMED (the blob's own shape is still
    well-formed; only its coverage CLAIM is contradicted).

    Never raises: any input this function cannot make sense of is
    classified MALFORMED or ABSENT, never an uncaught exception.
    """
    try:
        return _classify_route_inner(blob, expected_domain_digest)
    except Exception as e:  # noqa: BLE001 -- deliberate blanket catch, fail-closed by design
        return "MALFORMED", None, {
            "reason": "unexpected exception while classifying route -- treated as MALFORMED "
                      f"(schema/processing problem, never a crash or silent PASS): {type(e).__name__}: {e}",
        }


def _classify_route_inner(blob, expected_domain_digest):
    if blob is None or not isinstance(blob, dict):
        return "ABSENT", None, {
            "reason": "route blob is missing or not an object -- receiver-derived ABSENT "
                      "(no producer self-report trusted for this determination)",
        }

    kind = blob.get("evidence_kind")
    if kind not in ("PASS", "FAIL", "ABSENT", None):
        return "MALFORMED", None, {"reason": f"evidence_kind has an unrecognized value: {kind!r}"}

    evidence_field_names = (
        "claim_digest", "evidence_digest", "checked_domain_count",
        "coverage_digest", "counterexample_locus",
    )
    has_any_evidence_field = any(k in blob for k in evidence_field_names)

    # Structural absence: no self-declared non-ABSENT kind AND no evidence
    # fields present at all -- receiver-derived ABSENT (mirrors 追補(o) v2's
    # "route_absent は producer 自己申告を信じず受領側が入力欄から導出").
    if kind in (None, "ABSENT") and not has_any_evidence_field:
        return "ABSENT", None, {"reason": "no evidence fields present at all -- receiver-derived ABSENT"}

    # From here the blob claims (or structurally exhibits) non-ABSENT
    # evidence -- PASS/FAIL both share the F82-4.1 common required fields.
    claim_digest = blob.get("claim_digest")
    evidence_digest = blob.get("evidence_digest")
    if not _is_64hex(claim_digest):
        return "MALFORMED", None, {
            "reason": f"claim_digest missing or not exact 64-hex: {claim_digest!r} (F82-4.1 common "
                      "required field for any non-ABSENT evidence route)",
        }
    if not _is_64hex(evidence_digest):
        return "MALFORMED", None, {
            "reason": f"evidence_digest missing or not exact 64-hex: {evidence_digest!r} (v2 binding, "
                      "kept -- required for any non-ABSENT evidence route)",
        }

    is_fail_shaped = (kind == "FAIL") or (kind is None and blob.get("counterexample_locus") is not None)
    if is_fail_shaped:
        counterexample_locus = blob.get("counterexample_locus")
        if counterexample_locus is None:
            return "MALFORMED", None, {"reason": "FAIL-shaped route missing 'counterexample_locus'"}
        return "FAIL", claim_digest, {"counterexample_locus": counterexample_locus}

    # PASS-shaped path (kind == "PASS", or kind is None with PASS-only
    # evidence fields present).
    checked_domain_count = blob.get("checked_domain_count")
    if not isinstance(checked_domain_count, int) or isinstance(checked_domain_count, bool) or checked_domain_count < 0:
        return "MALFORMED", None, {
            "reason": f"checked_domain_count missing or not a non-negative int: {checked_domain_count!r} "
                      "(PASS requires a genuine domain-count claim, not just 'undefined==undefined')",
        }
    coverage_digest = blob.get("coverage_digest")
    if not _is_64hex(coverage_digest):
        return "MALFORMED", None, {"reason": f"coverage_digest missing or not exact 64-hex: {coverage_digest!r}"}

    if expected_domain_digest is not None:
        if not _is_64hex(expected_domain_digest):
            raise ValueError(f"expected_domain_digest supplied by caller is not exact 64-hex: {expected_domain_digest!r}")
        if coverage_digest != expected_domain_digest:
            # 追補(o) v3.1: "coverage_digest はその canonical domain の
            # digest と一致することを PASS 条件に含める" -- receiver's own
            # derivation disagrees, so the claimed full coverage is
            # falsified -- FAIL, not MALFORMED (schema is fine, substance
            # is wrong).
            return "FAIL", claim_digest, {
                "reason": "coverage_digest does not match the receiver-derived expected_domain_digest -- "
                          "the route's claimed full coverage is falsified",
                "counterexample_locus": "coverage-mismatch",
                "coverage_digest": coverage_digest,
                "expected_domain_digest": expected_domain_digest,
            }

    return "PASS", claim_digest, {"checked_domain_count": checked_domain_count, "coverage_digest": coverage_digest}


# ============================================================================
# Composition (追補(o) v3.1 "合成の全域関数"): TOTAL over the 4x4=16
# (route_status, route_status) domain, swap-symmetric, exactly the 4
# ordered rules below. This is the crisp, fully-specified part of the
# addendum -- implemented literally, table-driven-tested exhaustively.
# ============================================================================


def compose_route_statuses(status1, claim_digest1, status2, claim_digest2):
    """
    Composes two ALREADY-CLASSIFIED route statuses into ONE overall
    status. TOTAL (defined for every (status1, status2) in
    ROUTE_STATUSES x ROUTE_STATUSES) and SWAP-SYMMETRIC (compose(a,b) ==
    compose(b,a) with arguments swapped in pairs). Rules, IN ORDER
    (追補(o) v3.1 "合成の全域関数"):

      1. Either route MALFORMED -> INTEGRITY_STOP (regardless of
         direction/order).
      2. Both routes non-ABSENT (i.e. each in {PASS, FAIL}) -> compare
         claim_digest BEFORE composing status: mismatch -> CONFLICT
         (applies to PASS/PASS, FAIL/FAIL, AND FAIL/PASS alike -- not just
         the PASS/PASS case).
      3. Both non-ABSENT, claim_digest agrees, but the two statuses
         DISAGREE (one PASS, one FAIL) -> CONFLICT.
      4. Otherwise: any FAIL present -> FAIL; else any PASS present ->
         PASS; else (both ABSENT) -> ABSENT.

    Returns one of OVERALL_STATUSES: "INTEGRITY_STOP","CONFLICT","PASS",
    "FAIL","ABSENT".
    """
    for s in (status1, status2):
        if s not in ROUTE_STATUSES:
            raise ValueError(f"compose_route_statuses: not a valid route_status: {s!r}")

    # Rule 1.
    if status1 == "MALFORMED" or status2 == "MALFORMED":
        return "INTEGRITY_STOP"

    non_absent = [(s, d) for (s, d) in ((status1, claim_digest1), (status2, claim_digest2)) if s != "ABSENT"]

    if len(non_absent) == 2:
        (s_a, d_a), (s_b, d_b) = non_absent
        # Rule 2: claim_digest comparison BEFORE status composition,
        # regardless of which of PASS/FAIL combination this is.
        if d_a != d_b:
            return "CONFLICT"
        # Rule 3: same claim, but statuses disagree (PASS vs FAIL).
        if s_a != s_b:
            return "CONFLICT"
        # Same claim, same status -- PASS/PASS or FAIL/FAIL.
        return s_a

    if len(non_absent) == 1:
        # Rule 4 (one ABSENT, one non-ABSENT): the non-ABSENT status wins.
        return non_absent[0][0]

    # Rule 4 (both ABSENT).
    return "ABSENT"


# ============================================================================
# Top-level entry point: classify both routes, then compose.
# ============================================================================


def evidence_union_fail_closed_v2(route1_blob, route2_blob, expected_domain_digest=None):
    """
    Top-level evidence-union/fail-closed-v2 composition (追補(o) v3.1).
    Classifies BOTH route blobs independently (see classify_route), then
    composes their statuses (see compose_route_statuses). Returns a dict:
      {
        "route1_status": ..., "route1_detail": ...,
        "route2_status": ..., "route2_detail": ...,
        "overall_status": ...,
      }
    Never raises (classify_route is itself fail-closed/never-throwing;
    compose_route_statuses only raises on a status value classify_route
    could never actually produce, i.e. an internal-contract violation, not
    a possible external input).
    """
    s1, d1, detail1 = classify_route(route1_blob, expected_domain_digest)
    s2, d2, detail2 = classify_route(route2_blob, expected_domain_digest)
    overall = compose_route_statuses(s1, d1, s2, d2)
    return {
        "route1_status": s1, "route1_detail": detail1,
        "route2_status": s2, "route2_detail": detail2,
        "overall_status": overall,
    }


# ============================================================================
# W-6 connection point (ARMATURE ONLY this round -- see module docstring
# SCOPE NOTE; NOT wired into the EP runner here, EP v7 wiring is a later,
# separate step). Adapts ninfty-verifier-b.py's verify_W6_single(...)
# (status, detail) output into a route blob this module's classify_route
# can consume.
# ============================================================================


def route_from_verifier_b_w6(w6_status, w6_detail):
    """
    ARMATURE / PLACEHOLDER (not full EP wiring): adapts one
    ninfty-verifier-b.py verify_W6_single(cert, native_a, native_b) result
    -- a (status, detail) pair with status in
    {"ABSENT","MALFORMED","PASS","FAIL"} -- into a route blob this file's
    classify_route can consume as one of the two evidence routes (R1 or
    R2; the caller decides which slot this fills and supplies the OTHER
    route separately -- this function only builds ONE side).

    verify_W6_single predates this addendum's route-blob schema (it has no
    claim_digest/evidence_digest/checked_domain_count/coverage_digest
    fields of its own) -- this adapter DERIVES placeholder digests from
    the detail dict itself (sha256_of(detail)) so classify_route's
    required-field checks are satisfiable, but this is NOT a claim that
    W-6's real evidence has been migrated to the v3.1 route-blob schema;
    it exists solely so the composition function (the crisp, addendum-
    specified part) has a real, non-synthetic input to be exercised
    against in regression tests. Full EP v7 wiring (real
    claim_digest/evidence_digest bound to the actual native/map digests
    per v3.1's "evidence_digest は route の証拠を最終 record へ束縛する")
    is explicitly deferred, per this round's task scope.
    """
    if w6_status == "ABSENT":
        return {"evidence_kind": "ABSENT"}
    if w6_status == "MALFORMED":
        # A MALFORMED verify_W6_single result has no claim_digest/
        # evidence_digest either -- but classify_route's MALFORMED
        # detection for a PASS/FAIL-shaped blob already requires those
        # fields, so simply declaring evidence_kind=PASS with nothing else
        # naturally reaches MALFORMED via the missing-field check (never
        # needs a dedicated evidence_kind="MALFORMED" branch in the
        # adopted schema -- MALFORMED is always a receiver DERIVATION, per
        # the addendum, never a self-declared producer kind).
        return {"evidence_kind": "PASS"}  # deliberately incomplete -> classify_route -> MALFORMED
    detail_digest = sha256_of(w6_detail if isinstance(w6_detail, dict) else {"detail": w6_detail})
    if w6_status == "FAIL":
        return {
            "evidence_kind": "FAIL",
            "claim_digest": detail_digest,
            "evidence_digest": detail_digest,
            "counterexample_locus": w6_detail,
        }
    # w6_status == "PASS"
    return {
        "evidence_kind": "PASS",
        "claim_digest": detail_digest,
        "evidence_digest": detail_digest,
        "checked_domain_count": 1,  # PLACEHOLDER (armature only, see docstring) -- EP v7 must
                                    # bind this to the real per-side point/component count.
        "coverage_digest": detail_digest,
    }


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("payload_json", help="path to a JSON payload {route1, route2[, expected_domain_digest]}, or '-' for stdin")
    args = ap.parse_args(argv)
    if args.payload_json == "-":
        payload = json.load(sys.stdin)
    else:
        with open(args.payload_json, "r", encoding="utf-8") as f:
            payload = json.load(f)
    result = evidence_union_fail_closed_v2(
        payload.get("route1"), payload.get("route2"), payload.get("expected_domain_digest"),
    )
    print(canonical_serialize(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
