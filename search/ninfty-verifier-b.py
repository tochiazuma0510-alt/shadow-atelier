#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-verifier-b.py

N_infty stage-2 -- independent verifier B, per
mb/ninfty-verifier-contract/v13 (governing spec = mb/ninfty-stage2-predicate/v18).

**Repair history**:

  * **裁定 127** (2026-07-28, reverse-direction real-shape testing): this
    file (i) CRASHED on lane A's real certificate shapes in W-2/W-2'/W-3/W-4
    (blind `.get`/indexing assuming a specific shape), and (ii) had a
    **fail-open** defect in W-1/W-6: missing/misnamed keys silently
    defaulted to `[]` via `.get(key, [])`, and `[] == []` then satisfied
    PASS equality checks -- a vacuous PASS on structurally absent data.
    Fixed via: strict per-field type/key validation raising an internal
    `MalformedWitness`, a `@fail_closed` decorator that converts ANY
    exception into a clean FAIL (never a crash, never propagated), and
    explicit ABSENT-vs-FAIL-vs-PASS three-way handling everywhere so an
    empty/absent witness can never silently satisfy an equality check.

  * **裁定 128** (2026-07-28, docs/notes/cert_shape_interpretation_v1.md):
    spec sec.4.1 genuinely does NOT specify the internal JSON shape of the
    seven witness fields (component_bijection, exact_point_equality_witnesses,
    distinctness_witnesses, multiplicity_equalities, chart_overlap_witnesses,
    total_coverage_and_no_extra_component_witness,
    pushforward_compatibility_witness) -- the root cause of the lane A/B
    incompatibility 裁定127 found. Per the commander's interim interface
    note (Sol confirmation pending, status: interpretation/candidate, NOT
    a spec revision), this file now parses ALL SEVEN witness fields as
    **flat arrays whose entries carry a `divisor_object` tag** reusing
    spec's own literal native-object ref tokens
    (`ramification_divisor_on_C_ref` / `branch_divisor_on_P1_ref`) as tag
    VALUES, restoring the genuine "both native objects checked
    independently" requirement (contract sec.2: "両 native は各々 2 対象...
    W-1〜W-6 は2対象それぞれについて検査する") that this file previously
    only approximated by duplicating a single combined result across both
    object labels. See "CERTIFICATE SHAPE (裁定128 interim interface)"
    section below for the full derivation and the four Sol-confirmation
    points carried over unresolved.

Role (contract sec.1 V-0..V-3):
  * This is NOT a judgment lane. It cannot emit ACCEPT on its own.
  * It re-verifies a `divisor_equality_certificate` against the two
    supplied native artifacts, producing the canonical per-witness result
    vector R_B (contract sec.3.4) for BOTH objects independently, plus an
    overall verdict_B and its result_digest_B.
  * It does NOT compute the concordance comparison R_A vs R_B itself
    (contract C-7 -- belongs to the receiving side). This file has never
    read lane A's code or output, and was NOT adapted to look like lane
    A's real shape (裁定127: "B を A に合わせる案は棄却"). The 裁定128
    shape below is a COMMANDER-ISSUED INTERFACE NOTE binding both lanes
    equally (shared input/interface, not shared implementation -- per
    dependency-manifest v13's input/implementation separation rule), not
    something this implementer derived by peeking at lane A.
  * It replays certificate-declared arithmetic using its own from-scratch
    multivariate polynomial engine -- it never trusts the certificate's
    claims, and it never calls a shared canonicalizer.

Contact discipline: value-independent. Never hardcodes C, h, a5,
squareclasses, signs, branch values, concrete coefficients, or raw shard
naming patterns. All data comes from the certificate/native JSON supplied
by the caller.

Scope / EP status: EP has not run. This is a PARTIAL verifier. Declared
UNKNOWN / NOT IMPLEMENTED:
  * P-0.6 / P-1.4 (field_embedding_witness cross-presentation checks):
    only structural presence is checked, not the embedding map itself.
  * W-4 (chart_overlap_witnesses): checked for internal consistency of
    the declared data only; does not re-derive the chart atlas itself.
  * CR-11 (contract sec.9.1): the three-layer `implemented_checks`
    equality is UNKNOWN -- no executable inventory system exists yet.
  * **[裁定128, carried from cert_shape_interpretation_v1.md, Sol
    confirmation pending]**:
      (a) chart_ids element type (assumed: array of plain string ids)
      (b) whether the divisor_object-tagged-flat-array interpretation
          itself is accepted by Sol, or superseded by a v2 interface note
      (c) exact semantics of `_ref` fields (assumed: digest reference is
          authoritative; optional inline content only advisory, digest
          wins on conflict -- this file does NOT currently attempt a
          sub-digest recomputation against `_ref` beyond the whole-blob
          native_artifact_digest check in P-3.3; a genuine per-`_ref`
          digest cross-check is NOT implemented, flagged here as a gap)
      (d) whether "singular-noun witnesses must be exactly a 2-entry
          array" (component_bijection, total_coverage_and_no_extra_
          component_witness, pushforward_compatibility_witness) is
          consistent with contract sec.2's "2 対象それぞれについて検査"
          requirement, or whether >2 entries (extra/duplicate) for one
          object should be tolerated rather than FAILed -- this file
          FAILs a singular witness with more than 1 entry per object
          (see _check_singular_witness), which is a NEW implementer
          judgment call not literally covered by the interim note either.
  * **[裁定128, additional spec-silence points this implementer noticed
    while reshaping, forwarded to join the Sol confirmation queue]**:
      (e) the interim note does not say what should happen when an entry
          in a "plural" witness field (e.g. exact_point_equality_witnesses)
          carries NO divisor_object tag at all versus an UNRECOGNIZED one
          -- this file treats both as "unattributed" identically (FAILs
          both object channels rather than silently dropping the entry),
          which is this implementer's own fail-closed choice, not
          specified by the note.
      (f) the interim note does not say whether component_bijection's
          domain_components/codomain_components/mapping keys themselves
          are still the right per-entry sub-shape, or whether THEY are
          also supposed to be flattened/retagged under the new regime --
          this file keeps them as sub-keys of the (now singular, 2-entry)
          component_bijection array's per-object entry, unchanged from
          before 裁定128, since the interim note's rule 4 speaks only to
          "singular witnesses become a 2-entry array", not to further
          internal restructuring of what was already inside them.

runtime = python (stdlib only: fractions, hashlib, json, sys, argparse).
"""

from __future__ import annotations
from fractions import Fraction
import hashlib
import json
import sys
import argparse

# ============================================================================
# CERTIFICATE SHAPE (裁定128 interim interface, docs/notes/
# cert_shape_interpretation_v1.md) -- summary this file implements:
#
#   Top-level fields whose names/shape ARE literal per governing spec
#   sec.4.1 (unaffected by 裁定128): schema_id, schema_digest,
#   predicate_spec_id, predicate_spec_digest, candidate_ref,
#   curve_model_digest, chart_ids (array of string ids, per interim rule
#   2 / Sol-confirmation (a)), ambient_* / coefficient_field_* /
#   monomial_order_* / groebner_reduction_contract_* id+digest pairs,
#   searcher_native / checker_native = {ramification_divisor_on_C_ref,
#   branch_divisor_on_P1_ref, native_schema_id+digest, native_artifact_digest}.
#
#   The seven witness fields (spec-silent on internal shape -- root cause
#   of 裁定127's finding) are, per 裁定128 interim rules 1+4+5:
#
#   "Plural" fields (already array-shaped in spec's own naming) --
#   exact_point_equality_witnesses, distinctness_witnesses,
#   multiplicity_equalities, chart_overlap_witnesses -- remain flat
#   arrays; EACH ENTRY additionally carries a "divisor_object" key whose
#   value is one of the two literal tokens below.
#
#   "Singular" fields (grammatically singular in spec's own naming) --
#   component_bijection, total_coverage_and_no_extra_component_witness,
#   pushforward_compatibility_witness -- become themselves a flat array
#   of EXACTLY ONE entry per divisor_object token (2 entries total when
#   both objects are covered).
#
#   A container field that is missing, None, or not a list is coerced to
#   [] (rule 5) -- this routes to ABSENT, never an exception and never a
#   fail-open vacuous PASS (an empty container can never independently
#   satisfy a PASS -- see the per-witness checkers below).
# ============================================================================

DIVISOR_OBJECT_TOKENS = ("ramification_divisor_on_C_ref", "branch_divisor_on_P1_ref")


class MalformedWitness(Exception):
    """Raised internally when certificate data does not match this
    verifier's expected (spec-derived where literal, 裁定128-interim
    where spec is silent) nested shape. Always caught; never escapes to
    the caller (裁定127 fix (i): crash resistance)."""


def _require_dict(x, what):
    if not isinstance(x, dict):
        raise MalformedWitness(f"{what} must be an object/dict, got {type(x).__name__}: {x!r}")
    return x


def _require_list(x, what):
    if not isinstance(x, list):
        raise MalformedWitness(f"{what} must be an array/list, got {type(x).__name__}: {x!r}")
    return x


def _require_keys(d, keys, what):
    missing = [k for k in keys if k not in d]
    if missing:
        raise MalformedWitness(f"{what} missing required key(s) {missing} (present keys: {sorted(d.keys())})")
    return d


def _require_int(x, what):
    if isinstance(x, bool):
        raise MalformedWitness(f"{what} must be an integer, got bool: {x!r}")
    try:
        return int(x)
    except (TypeError, ValueError):
        raise MalformedWitness(f"{what} must be an integer, got {type(x).__name__}: {x!r}")


# --------------------------------------------------------------------------
# 裁定128 rule-5 machinery: coerce-to-empty-array-or-ABSENT, then split by
# divisor_object tag. Shared by all seven witness checkers.
# --------------------------------------------------------------------------


def _coerce_to_list(cert, field_name):
    """Missing/None/wrong-type -> ([], True). Present list -> (list, False)."""
    v = cert.get(field_name, None)
    if isinstance(v, list):
        return v, False
    return [], True


def _split_by_divisor_object(entries):
    """
    Groups entries by their 'divisor_object' tag. Entries that are not
    dicts, lack the tag, or carry an unrecognized value are collected as
    'unattributed' -- NEVER silently dropped (that would reopen a
    fail-open hole); callers FAIL the relevant object channel(s) instead.
    """
    groups = {tok: [] for tok in DIVISOR_OBJECT_TOKENS}
    unattributed = []
    for i, e in enumerate(entries):
        tag = e.get("divisor_object") if isinstance(e, dict) else None
        if tag in groups:
            groups[tag].append(e)
        else:
            unattributed.append((i, e))
    return groups, unattributed


def _absent_pair(reason):
    return {tok: ("ABSENT", {"reason": reason}) for tok in DIVISOR_OBJECT_TOKENS}


def _check_plural_witness(cert, field_name, validate_entry):
    """
    For W-2/W-2'/W-3/W-4 style fields: any number of entries per object,
    ALL must PASS for that object's channel to PASS. 0 entries for a
    given object (after a well-typed, nonempty container is split) ->
    ABSENT for that object specifically (still a legitimate "no claim").
    """
    raw, coerced = _coerce_to_list(cert, field_name)
    if len(raw) == 0:
        reason = f"{field_name} not supplied or empty"
        if coerced:
            reason += " (coerced from missing/wrong-typed container, cert_shape_interpretation_v1 rule 5)"
        return _absent_pair(reason)

    groups, unattributed = _split_by_divisor_object(raw)
    unattributed_reason = None
    if unattributed:
        unattributed_reason = (
            f"{len(unattributed)} entr{'y' if len(unattributed) == 1 else 'ies'} in {field_name} "
            f"lack a recognized 'divisor_object' tag and cannot be attributed to either native "
            f"object -- FAIL (not silently dropped, 裁定127 fail-open fix generalized to 裁定128 shape)"
        )

    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        entries = groups[tok]
        if not entries and not unattributed:
            out[tok] = ("ABSENT", {"reason": f"no {field_name} entries tagged divisor_object={tok!r}"})
            continue
        details = []
        all_ok = True
        for i, e in enumerate(entries):
            try:
                status, detail = validate_entry(e)
            except MalformedWitness as ex:
                status, detail = "FAIL", {"malformed": True, "reason": str(ex)}
            details.append({"index": i, "status": status, "detail": detail})
            if status != "PASS":
                all_ok = False
        if unattributed:
            all_ok = False
            details.append({"unattributed_entries": len(unattributed), "reason": unattributed_reason})
        if not entries and unattributed:
            out[tok] = ("FAIL", {"entries": details})
        else:
            out[tok] = ("PASS" if all_ok else "FAIL", {"entries": details})
    return out


def _check_singular_witness(cert, field_name, validate_entry):
    """
    For W-1/W-5/W-6 style fields (裁定128 rule 4: singular-noun witnesses
    become a 2-entry array, one per object). Exactly one entry per object
    is expected; 0 -> ABSENT for that object, >1 -> FAIL (ambiguous
    duplicate singular claim -- Sol-confirmation point (d), see docstring).
    """
    raw, coerced = _coerce_to_list(cert, field_name)
    if len(raw) == 0:
        reason = f"{field_name} not supplied or empty"
        if coerced:
            reason += " (coerced from missing/wrong-typed container, cert_shape_interpretation_v1 rule 5)"
        return _absent_pair(reason)

    groups, unattributed = _split_by_divisor_object(raw)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        entries = groups[tok]
        if len(entries) == 0:
            out[tok] = ("ABSENT", {"reason": f"no {field_name} entry tagged divisor_object={tok!r}"})
        elif len(entries) > 1:
            out[tok] = ("FAIL", {"reason": f"{field_name} has {len(entries)} entries tagged "
                                  f"divisor_object={tok!r}, expected exactly 1 (singular witness, "
                                  "cert_shape_interpretation_v1 rule 4)"})
        else:
            try:
                status, detail = validate_entry(entries[0])
            except MalformedWitness as ex:
                status, detail = "FAIL", {"malformed": True, "reason": str(ex)}
            out[tok] = (status, detail)
    if unattributed:
        reason = (f"{len(unattributed)} unattributed entries present in {field_name} "
                  "(missing/unrecognized divisor_object tag) -- FAIL, not silently dropped")
        for tok in DIVISOR_OBJECT_TOKENS:
            if out[tok][0] != "FAIL":
                out[tok] = ("FAIL", {"reason": reason})
    return out


def fail_closed_pairmap(fn):
    """
    Decorator for the top-level per-witness-type functions (which return
    a {token: (status, detail)} pair-map, not a single (status, detail)
    tuple). Any unexpected exception anywhere inside is converted into a
    FAIL pair-map rather than propagating (defense in depth on top of the
    per-entry @-free try/except already inside _check_plural_witness /
    _check_singular_witness).
    """
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:  # noqa: BLE001 -- deliberate blanket catch, fail-closed by design
            detail = {
                "crashed": True,
                "exception_type": type(e).__name__,
                "exception": str(e),
                "reason": "unexpected exception while checking this witness type -- "
                          "treated as FAIL for both object channels, never a crash or "
                          "silent PASS (裁定127 fix (i))",
            }
            return {tok: ("FAIL", detail) for tok in DIVISOR_OBJECT_TOKENS}
    wrapped.__name__ = fn.__name__
    wrapped.__doc__ = fn.__doc__
    return wrapped


# --------------------------------------------------------------------------
# Self-implemented multivariate polynomial engine over Q. Monomial = tuple
# of nonnegative ints. Poly = dict{monomial: Fraction}, zero coeffs
# removed. Used ONLY to replay certificate-declared arithmetic -- never
# trusts the certificate's claims, always recomputes from raw terms.
# --------------------------------------------------------------------------


def _F(x):
    if isinstance(x, Fraction):
        return x
    if isinstance(x, bool):
        raise MalformedWitness(f"coefficient must be a number, got bool: {x!r}")
    if isinstance(x, str):
        if "/" in x:
            parts = x.split("/")
            if len(parts) != 2:
                raise MalformedWitness(f"malformed rational coefficient string: {x!r}")
            try:
                return Fraction(int(parts[0]), int(parts[1]))
            except (TypeError, ValueError, ZeroDivisionError) as e:
                raise MalformedWitness(f"malformed rational coefficient string {x!r}: {e}")
        try:
            return Fraction(x)
        except (TypeError, ValueError) as e:
            raise MalformedWitness(f"malformed coefficient string {x!r}: {e}")
    if isinstance(x, (int, float, Fraction)):
        return Fraction(x)
    raise MalformedWitness(f"coefficient must be a number or numeric string, got {type(x).__name__}: {x!r}")


def _canon_mono(m):
    if not isinstance(m, list):
        raise MalformedWitness(f"mono must be an array of nonnegative ints, got {type(m).__name__}: {m!r}")
    for e in m:
        if isinstance(e, bool) or not isinstance(e, int) or e < 0:
            raise MalformedWitness(f"mono exponents must be nonnegative ints, got {m!r}")
    m = tuple(m)
    while m and m[-1] == 0:
        m = m[:-1]
    return m


def mv_from_json(terms):
    """
    terms: list of {"coeff": "n/d"|num, "mono": [e1,e2,...]}. RETAINED for
    backward compatibility only -- 裁定133 (h) retires the flat
    kind/tag-at-entry-level, sparse-multivariate-term shape this engine
    was built for ("kind/tag を entry 直下に平置きする形は採らない"). No
    current entry validator calls this; kept in case a future certificate
    genuinely needs multivariate (2-chart, x/y) generators, which the v2
    dense single-variable engine below (dp_*) cannot express.
    """
    _require_list(terms, "polynomial term list")
    out = {}
    for i, t in enumerate(terms):
        _require_dict(t, f"term[{i}]")
        _require_keys(t, ["coeff", "mono"], f"term[{i}]")
        m = _canon_mono(t["mono"])
        c = _F(t["coeff"])
        out[m] = out.get(m, Fraction(0)) + c
    return {m: c for m, c in out.items() if c != 0}


# --------------------------------------------------------------------------
# 裁定133 (h): dense single-variable Q[x] engine (low-degree-first list of
# Fraction). This is what the v2 nested witness shape actually carries
# (dividend / divisor_monic / quotient / remainder, generator_P /
# generator_Q / bezout_u / bezout_v -- all plain coefficient arrays, not
# sparse {coeff,mono} terms). Self-contained (no import of
# search/ninfty-checker.py or any other file) -- duplicated rather than
# shared, to keep this file's own dependency closure exactly as declared
# in search/certs/laneB_manifest.json.
# --------------------------------------------------------------------------


def dp_from_json(coeffs):
    _require_list(coeffs, "polynomial coefficient list")
    return _dp_trim([_F(c) for c in coeffs])


def _dp_trim(c):
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return c


def dp_add(a, b):
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, v in enumerate(a):
        out[i] += v
    for i, v in enumerate(b):
        out[i] += v
    return _dp_trim(out)


def dp_mul(a, b):
    a, b = _dp_trim(a), _dp_trim(b)
    if not a or not b:
        return []
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            out[i + j] += x * y
    return _dp_trim(out)


def dp_eq(a, b):
    return _dp_trim(a) == _dp_trim(b)


def dp_is_zero(a):
    return not _dp_trim(a)


DP_ONE = [Fraction(1)]


def dp_is_one(a):
    return dp_eq(a, DP_ONE)


def _dp_out(poly):
    return [str(c) for c in poly]


def _terms_out(poly):
    """Retained for mv_from_json backward-compat callers (none currently)."""
    return sorted(
        ({"mono": list(m), "coeff": str(c)} for m, c in poly.items()),
        key=lambda t: t["mono"],
    )


# --------------------------------------------------------------------------
# W-2 / W-2' / W-3 per-entry validators (裁定133 (h): nested `witness`
# object, dense single-variable polynomials; 裁定134 (j): W-3 field names
# renamed searcher_mult/checker_mult).
# --------------------------------------------------------------------------


def _validate_ideal_equality_direction(direction, label):
    """
    direction = {tag, dividend, divisor_monic, quotient, remainder}
    (裁定133 (h), literal field names). Re-derives
    quotient*divisor_monic + remainder from scratch and checks it equals
    dividend (never trusts the claimed quotient/remainder blindly), AND
    that the tag's own claim (remainder == 0 for reduction-to-zero,
    remainder == 1 for reduction-to-one) actually holds.
    """
    _require_dict(direction, f"{label} direction")
    _require_keys(direction, ["tag", "dividend", "divisor_monic", "quotient", "remainder"], f"{label} direction")
    if direction["tag"] not in ("reduction-to-zero", "reduction-to-one"):
        raise MalformedWitness(f"{label}: invalid/missing tag (P-1.5): {direction.get('tag')!r}")
    dividend = dp_from_json(direction["dividend"])
    divisor_monic = dp_from_json(direction["divisor_monic"])
    quotient = dp_from_json(direction["quotient"])
    remainder = dp_from_json(direction["remainder"])
    recomputed_dividend = dp_add(dp_mul(quotient, divisor_monic), remainder)
    identity_ok = dp_eq(recomputed_dividend, dividend)
    tag_ok = dp_is_zero(remainder) if direction["tag"] == "reduction-to-zero" else dp_is_one(remainder)
    ok = identity_ok and tag_ok
    return ok, {
        "identity_ok": identity_ok, "tag_ok": tag_ok,
        "recomputed_dividend": _dp_out(recomputed_dividend), "claimed_dividend": _dp_out(dividend),
    }


def _validate_w2_entry(e):
    """
    W-2 entry (裁定133 (h)): {locus_type, divisor_object, witness: {kind,
    forward: {...}, backward: {...}}}. `witness.ok` (if present) is a
    producer CLAIM and is never trusted -- only the recomputed
    forward/backward identities decide PASS/FAIL.
    """
    _require_dict(e, "W-2 entry")
    _require_keys(e, ["witness"], "W-2 entry")
    witness = _require_dict(e["witness"], "W-2 entry.witness")
    if witness.get("kind") != "ideal-equality":
        return "FAIL", {"reason": f"wrong kind for W-2 (must be ideal-equality, got {witness.get('kind')!r})"}
    _require_keys(witness, ["forward", "backward"], "W-2 entry.witness")
    fwd_ok, fwd_detail = _validate_ideal_equality_direction(witness["forward"], "forward")
    bwd_ok, bwd_detail = _validate_ideal_equality_direction(witness["backward"], "backward")
    ok = fwd_ok and bwd_ok
    return ("PASS" if ok else "FAIL"), {"forward": fwd_detail, "backward": bwd_detail}


def _validate_w2prime_entry(e):
    """
    W-2' entry (裁定133 (h) family, disjointness kind): {pair,
    divisor_object, witness: {kind: "disjointness", generator_P,
    generator_Q, bezout_u, bezout_v, reduction_tag}}. Recomputes
    bezout_u*generator_P + bezout_v*generator_Q from scratch and checks it
    equals the constant claimed by reduction_tag.
    """
    _require_dict(e, "W-2' entry")
    _require_keys(e, ["witness"], "W-2' entry")
    witness = _require_dict(e["witness"], "W-2' entry.witness")
    if witness.get("kind") != "disjointness":
        return "FAIL", {"reason": f"wrong kind for W-2' (must be disjointness, got {witness.get('kind')!r})"}
    _require_keys(witness, ["generator_P", "generator_Q", "bezout_u", "bezout_v", "reduction_tag"],
                   "W-2' entry.witness")
    if witness["reduction_tag"] not in ("reduction-to-zero", "reduction-to-one"):
        raise MalformedWitness(f"invalid/missing reduction_tag: {witness.get('reduction_tag')!r}")
    p = dp_from_json(witness["generator_P"])
    q = dp_from_json(witness["generator_Q"])
    u = dp_from_json(witness["bezout_u"])
    v = dp_from_json(witness["bezout_v"])
    acc = dp_add(dp_mul(u, p), dp_mul(v, q))
    ok = dp_is_one(acc) if witness["reduction_tag"] == "reduction-to-one" else dp_is_zero(acc)
    return ("PASS" if ok else "FAIL"), {"recomputed": _dp_out(acc)}


def _validate_w3_entry(e):
    """
    W-3 entry (裁定134 (j): searcher_mult/checker_mult -- mult_A/mult_B
    retired). `equal` (if present) is a producer claim and is never
    trusted; PASS/FAIL is decided solely by the independent int comparison.
    """
    _require_dict(e, "W-3 entry")
    _require_keys(e, ["searcher_mult", "checker_mult"], "W-3 entry")
    sm = _require_int(e["searcher_mult"], "W-3 entry.searcher_mult")
    cm = _require_int(e["checker_mult"], "W-3 entry.checker_mult")
    ok = sm == cm
    return ("PASS" if ok else "FAIL"), {"searcher_mult": sm, "checker_mult": cm}


def _validate_w4_entry(e):
    """
    W-4 entry (裁定133 (i)): {divisor_object, status, per_overlap_witnesses:
    [{chart_pair, component_in_chart_a, component_in_chart_b}, ...]}.
    `status` (if present) is a producer claim and is never trusted; PASS
    requires ALL per_overlap_witnesses entries to independently agree.
    """
    _require_dict(e, "W-4 entry")
    _require_keys(e, ["per_overlap_witnesses"], "W-4 entry")
    overlaps = _require_list(e["per_overlap_witnesses"], "W-4 entry.per_overlap_witnesses")
    if len(overlaps) == 0:
        return "FAIL", {"reason": "per_overlap_witnesses is present but empty -- no overlap claim to verify"}
    bad = []
    for i, o in enumerate(overlaps):
        if not isinstance(o, dict) or "component_in_chart_a" not in o or "component_in_chart_b" not in o:
            bad.append({"index": i, "reason": "malformed (need component_in_chart_a, component_in_chart_b)"})
            continue
        if o["component_in_chart_a"] != o["component_in_chart_b"]:
            bad.append({"index": i, "component_in_chart_a": o["component_in_chart_a"],
                        "component_in_chart_b": o["component_in_chart_b"]})
    ok = len(bad) == 0
    return ("PASS" if ok else "FAIL"), {"mismatches": bad, "checked": len(overlaps)}


@fail_closed_pairmap
def verify_W2(cert):
    """W-2: exact_point_equality_witnesses (裁定128 flat array + divisor_object tag, plural)."""
    return _check_plural_witness(cert, "exact_point_equality_witnesses", _validate_w2_entry)


@fail_closed_pairmap
def verify_W2prime(cert):
    """W-2': distinctness_witnesses (裁定128 flat array + divisor_object tag, plural)."""
    return _check_plural_witness(cert, "distinctness_witnesses", _validate_w2prime_entry)


@fail_closed_pairmap
def verify_W3(cert):
    """W-3: multiplicity_equalities (裁定128 flat array + divisor_object tag, plural)."""
    return _check_plural_witness(cert, "multiplicity_equalities", _validate_w3_entry)


@fail_closed_pairmap
def verify_W4(cert):
    """W-4: chart_overlap_witnesses (裁定128 flat array + divisor_object tag, plural)."""
    return _check_plural_witness(cert, "chart_overlap_witnesses", _validate_w4_entry)


# --------------------------------------------------------------------------
# W-1 (裁定133 (g)): component_bijection is now itself a PLURAL field --
# one entry per matched (searcher, checker) pair, tagged divisor_object.
# The "exactly 1 entry per object" constraint is WITHDRAWN; instead
# injectivity is checked ACROSS the whole per-object group (cannot be
# decided entry-by-entry, unlike the other six witness types -- hence a
# bespoke function rather than _check_plural_witness/_check_singular_witness),
# and the total per-object entry count is cross-checked against W-5's
# `matched_count` for the same divisor_object.
#
# W-5 / W-6 remain "singular" (2-entry array, one per object, 裁定128 rule
# 4), but W-5's own entry shape now uses searcher_count/checker_count/
# matched_count/no_extra (this implementer's adopted shape -- 裁定133/134
# do not literally specify W-5's fields; flagged as a further spec-silence
# point in the module docstring UNKNOWN list, alongside (e)/(f)), and W-6
# now uses the 裁定133 (i) {status, points:[...]} shape.
# --------------------------------------------------------------------------


def _actual_bijection_counts_and_groups(cert):
    """Coerced-list-safe: returns (groups, unattributed) from the raw
    component_bijection container, never raises."""
    raw, coerced = _coerce_to_list(cert, "component_bijection")
    groups, unattributed = _split_by_divisor_object(raw)
    return groups, unattributed, coerced


def _validate_bijection_group(entries, matched_count_claim):
    """
    entries: raw dicts already filtered to one divisor_object token, each
    {searcher_index, checker_index, locus_type, divisor_object} (裁定133
    (g)). matched_count_claim: W-5's claimed matched_count for this same
    token (or None if unreadable) -- cross-checked here, NOT trusted
    blindly; genuine injectivity is what actually decides PASS/FAIL.
    """
    if len(entries) == 0:
        if matched_count_claim not in (0, None):
            return "FAIL", {"reason": "component_bijection has 0 entries for this divisor_object, but "
                             f"the matching W-5 entry claims matched_count={matched_count_claim!r} "
                             "(!= 0) -- refusing a vacuous empty PASS"}
        return "ABSENT", {"reason": "no component_bijection entries for this divisor_object"}
    bad = []
    searcher_idx, checker_idx = [], []
    for i, e in enumerate(entries):
        if not isinstance(e, dict) or "searcher_index" not in e or "checker_index" not in e:
            bad.append({"index": i, "reason": "malformed (need searcher_index, checker_index)"})
            continue
        try:
            si = _require_int(e["searcher_index"], f"component_bijection entry[{i}].searcher_index")
            ci = _require_int(e["checker_index"], f"component_bijection entry[{i}].checker_index")
        except MalformedWitness as ex:
            bad.append({"index": i, "reason": str(ex)})
            continue
        searcher_idx.append(si)
        checker_idx.append(ci)
    if bad:
        return "FAIL", {"malformed_entries": bad}
    injective_searcher = len(set(searcher_idx)) == len(searcher_idx)
    injective_checker = len(set(checker_idx)) == len(checker_idx)
    count_ok = matched_count_claim is None or len(entries) == matched_count_claim
    ok = injective_searcher and injective_checker and count_ok
    detail = {
        "entry_count": len(entries), "injective_searcher_index": injective_searcher,
        "injective_checker_index": injective_checker,
        "matched_count_claimed_by_W5": matched_count_claim, "count_matches_W5": count_ok,
    }
    return ("PASS" if ok else "FAIL"), detail


def _matched_count_claimed_by_w5(cert):
    """Best-effort {token: claimed matched_count or None} from the raw W-5 container."""
    raw, _coerced = _coerce_to_list(cert, "total_coverage_and_no_extra_component_witness")
    groups, _unattributed = _split_by_divisor_object(raw)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        entries = groups[tok]
        val = None
        if len(entries) == 1 and isinstance(entries[0], dict):
            v = entries[0].get("matched_count")
            if isinstance(v, int) and not isinstance(v, bool):
                val = v
        out[tok] = val
    return out


@fail_closed_pairmap
def verify_W1(cert):
    """W-1: component_bijection (裁定133 (g): plural, per-pair entries;
    injectivity checked across each per-object group; count cross-checked
    against W-5's claimed matched_count)."""
    groups, unattributed, coerced = _actual_bijection_counts_and_groups(cert)
    if coerced:
        reason = "component_bijection not supplied or not a list (coerced to [])"
        return _absent_pair(reason)
    matched_claims = _matched_count_claimed_by_w5(cert)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        status, detail = _validate_bijection_group(groups[tok], matched_claims[tok])
        if unattributed and status != "FAIL":
            status, detail = "FAIL", {"reason": f"{len(unattributed)} unattributed component_bijection "
                                       "entries present (missing/unrecognized divisor_object tag)"}
        out[tok] = (status, detail)
    return out


def _actual_bijection_entry_counts(cert):
    """{token: actual number of component_bijection entries for that token}, never raises."""
    groups, _unattributed, _coerced = _actual_bijection_counts_and_groups(cert)
    return {tok: len(groups[tok]) for tok in DIVISOR_OBJECT_TOKENS}


def _validate_coverage_entry_factory(actual_matched_count):
    """
    actual_matched_count: the ACTUAL (recomputed, not claimed) number of
    component_bijection entries for this divisor_object -- cross-checked
    here so W-5's PASS genuinely requires the claimed matched_count to
    match reality, no_extra to be independently recomputed (not trusted),
    and every extra candidate to carry a distinctness_witness_ref.
    W-5's own entry shape (searcher_count/checker_count/matched_count/
    no_extra/extra_candidates) is this implementer's adopted choice --
    裁定133/134 do not literally specify W-5's fields (see module
    docstring UNKNOWN list).
    """
    def _validate(w):
        _require_dict(w, "total_coverage entry")
        _require_keys(w, ["searcher_count", "checker_count", "matched_count"], "total_coverage entry")
        sc = _require_int(w["searcher_count"], "total_coverage entry.searcher_count")
        cc = _require_int(w["checker_count"], "total_coverage entry.checker_count")
        mc = _require_int(w["matched_count"], "total_coverage entry.matched_count")
        extras = w.get("extra_candidates", [])
        if not isinstance(extras, list):
            return "FAIL", {"reason": f"extra_candidates must be an array, got {type(extras).__name__}"}
        extras_have_distinctness = True
        for e in extras:
            ref = e.get("distinctness_witness_ref") if isinstance(e, dict) else None
            if not ref:
                extras_have_distinctness = False
        no_extra_recomputed = (mc == sc == cc)
        matched_ok = actual_matched_count is None or mc == actual_matched_count
        ok = matched_ok and no_extra_recomputed and (len(extras) == 0 or extras_have_distinctness)
        detail = {
            "searcher_count": sc, "checker_count": cc, "matched_count_claimed": mc,
            "matched_count_actual_from_W1": actual_matched_count, "matched_ok": matched_ok,
            "no_extra_recomputed": no_extra_recomputed,
            "extras": len(extras), "extras_have_distinctness_ref": extras_have_distinctness,
        }
        return ("PASS" if ok else "FAIL"), detail
    return _validate


@fail_closed_pairmap
def verify_W5(cert):
    """W-5: total_coverage_and_no_extra_component_witness (singular, 2-entry
    array), cross-checked against W-1's ACTUAL (recomputed) matched count."""
    actual = _actual_bijection_entry_counts(cert)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        result_pair = _check_singular_witness(
            {"total_coverage_and_no_extra_component_witness":
                cert.get("total_coverage_and_no_extra_component_witness")},
            "total_coverage_and_no_extra_component_witness",
            _validate_coverage_entry_factory(actual[tok]),
        )
        out[tok] = result_pair[tok]
    return out


def _validate_w6_entry_factory(actual_matched_count):
    """
    W-6 entry (裁定133 (i)): {divisor_object, status, points: [...]}.
    `status` (if present) is a producer claim and is never trusted. Each
    point is {role: "ramification"|"branch", multiplicity, and either
    maps_to_branch_value (ramification) or branch_value (branch)} -- this
    implementer's own reasonable reading of "points" (not literally
    specified beyond the key name; flagged in module docstring UNKNOWN
    list). PASS requires the pushforward sum recomputed from role=
    "ramification" points to equal the declared role="branch" points,
    AND (closing the exact empty-vs-empty vacuous-PASS hole 裁定127
    identified in this function specifically) an entirely empty `points`
    list is only accepted when W-1's actual matched count for this object
    is also 0.
    """
    def _validate(w):
        _require_dict(w, "W-6 entry")
        _require_keys(w, ["points"], "W-6 entry")
        points = _require_list(w["points"], "W-6 entry.points")
        if len(points) == 0:
            if actual_matched_count not in (0, None):
                return "FAIL", {"reason": "points is empty, but W-1 shows "
                                 f"matched_count={actual_matched_count!r} (!= 0) for this object -- "
                                 "refusing a vacuous empty PASS"}
        push, declared = {}, {}
        for i, p in enumerate(points):
            if not isinstance(p, dict) or "role" not in p or "multiplicity" not in p:
                raise MalformedWitness(f"points[{i}] malformed (need role, multiplicity): {p!r}")
            mult = _require_int(p["multiplicity"], f"points[{i}].multiplicity")
            role = p["role"]
            if role == "ramification":
                if "maps_to_branch_value" not in p:
                    raise MalformedWitness(f"points[{i}] role=ramification missing maps_to_branch_value")
                bv = p["maps_to_branch_value"]
                push[bv] = push.get(bv, 0) + mult
            elif role == "branch":
                if "branch_value" not in p:
                    raise MalformedWitness(f"points[{i}] role=branch missing branch_value")
                bv = p["branch_value"]
                declared[bv] = mult
            else:
                raise MalformedWitness(f"points[{i}].role must be 'ramification' or 'branch', got {role!r}")
        ok = set(push.keys()) == set(declared.keys()) and all(push[k] == declared[k] for k in push)
        return ("PASS" if ok else "FAIL"), {"recomputed_pushforward": push, "declared_branch": declared}
    return _validate


@fail_closed_pairmap
def verify_W6(cert):
    """W-6: pushforward_compatibility_witness (裁定133 (i): {status, points}
    shape), cross-checked against W-1's actual matched count."""
    actual = _actual_bijection_entry_counts(cert)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        result_pair = _check_singular_witness(
            {"pushforward_compatibility_witness": cert.get("pushforward_compatibility_witness")},
            "pushforward_compatibility_witness",
            _validate_w6_entry_factory(actual[tok]),
        )
        out[tok] = result_pair[tok]
    return out


# --------------------------------------------------------------------------
# P-0.* / P-3.* input binding checks (contract sec.3.0 / sec.3.3).
# --------------------------------------------------------------------------


def _fail_closed_pair(fn):
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:  # noqa: BLE001
            return "FAIL", {"crashed": True, "exception_type": type(e).__name__, "exception": str(e)}
    wrapped.__name__ = fn.__name__
    return wrapped


@_fail_closed_pair
def verify_P0(cert, expected):
    """
    P-0.1..P-0.8: ambient fixation re-check. These field names ARE literal
    per governing spec sec.4.1 (unaffected by 裁定128, which concerns only
    the seven witness fields).
    """
    _require_dict(cert, "certificate")
    checks = {}
    required_fields = [
        "ambient_coordinate_ring_schema_id",
        "ambient_coordinate_ring_schema_digest",
        "ambient_quotient_relations",
        "coefficient_field_presentation_id",
        "coefficient_field_presentation_digest",
        "monomial_order_id",
        "monomial_order_digest",
        "groebner_reduction_contract_id",
        "groebner_reduction_contract_digest",
        "curve_model_digest",
        "chart_ids",
    ]
    for f in required_fields:
        checks[f] = f in cert and cert[f] not in (None, "", [])
    p_0_1 = checks["ambient_coordinate_ring_schema_id"] and checks["ambient_coordinate_ring_schema_digest"]
    p_0_2 = checks["ambient_quotient_relations"]
    p_0_3 = checks["coefficient_field_presentation_id"] and checks["coefficient_field_presentation_digest"]
    p_0_4 = checks["monomial_order_id"] and checks["monomial_order_digest"]
    p_0_5 = checks["groebner_reduction_contract_id"] and checks["groebner_reduction_contract_digest"]
    p_0_7 = checks["curve_model_digest"] and checks["chart_ids"]

    field_embedding_present = "field_embedding_witness_schema_id" in cert
    p_0_6 = True
    if cert.get("_requires_field_embedding_witness"):
        p_0_6 = field_embedding_present
    p_0_8 = (not field_embedding_present) or ("field_embedding_witness_schema_digest" in cert)

    all_ok = all([p_0_1, p_0_2, p_0_3, p_0_4, p_0_5, p_0_7, p_0_6, p_0_8])
    return ("PASS" if all_ok else "FAIL"), {
        "P-0.1": p_0_1, "P-0.2": p_0_2, "P-0.3": p_0_3, "P-0.4": p_0_4,
        "P-0.5": p_0_5, "P-0.6": p_0_6, "P-0.7": p_0_7, "P-0.8": p_0_8,
        "field_embedding_witness_present": field_embedding_present,
    }


@_fail_closed_pair
def verify_P3(cert, native_a, native_b, expected):
    """
    P-3.1..P-3.3: input/output binding. [裁定128 Sol-confirmation (c)]:
    `_ref` fields are interpreted as digest references (authoritative);
    this function checks the whole-blob native_artifact_digest, which is
    consistent with "digest is authoritative", but does NOT yet perform a
    finer-grained per-`_ref` sub-digest recomputation -- flagged as a gap
    in the module docstring, not silently assumed complete.
    """
    _require_dict(cert, "certificate")
    p31 = (
        cert.get("predicate_spec_id") == expected.get("predicate_spec_id")
        and cert.get("predicate_spec_digest") == expected.get("predicate_spec_digest")
    )
    p32 = cert.get("schema_id") is not None and cert.get("schema_digest") is not None

    def recomputed_digest(native_obj):
        if native_obj is None:
            return None
        return hashlib.sha256(
            json.dumps(native_obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    searcher_native = cert.get("searcher_native")
    checker_native = cert.get("checker_native")
    if not isinstance(searcher_native, dict):
        searcher_native = {}
    if not isinstance(checker_native, dict):
        checker_native = {}

    p33_a = True
    p33_b = True
    detail = {}
    if native_a is not None:
        recomputed = recomputed_digest(native_a)
        declared = searcher_native.get("native_artifact_digest")
        p33_a = declared is None or recomputed == declared
        detail["searcher_native_recomputed_digest"] = recomputed
        detail["searcher_native_declared_digest"] = declared
    if native_b is not None:
        recomputed = recomputed_digest(native_b)
        declared = checker_native.get("native_artifact_digest")
        p33_b = declared is None or recomputed == declared
        detail["checker_native_recomputed_digest"] = recomputed
        detail["checker_native_declared_digest"] = declared

    ok = p31 and p32 and p33_a and p33_b
    detail.update({"P-3.1": p31, "P-3.2": p32, "P-3.3_searcher": p33_a, "P-3.3_checker": p33_b})
    return ("PASS" if ok else "FAIL"), detail


# --------------------------------------------------------------------------
# contract sec.3.4: canonical per-witness result vector R_B, now genuinely
# independent for the two native objects (裁定128 closes the "duplicated
# combined result" approximation this file previously used).
# --------------------------------------------------------------------------

WITNESS_LABELS = ["W-1", "W-2", "W-2prime", "W-3", "W-4", "W-5", "W-6"]
OBJECT_LABELS = {
    "ramification_divisor_on_C_ref": "ramification_divisor_on_C",
    "branch_divisor_on_P1_ref": "branch_divisor_on_P1",
}

VERIFIER_ID = "search/ninfty-verifier-b.py"

EXPECTED_PINS = {
    "predicate_spec_id": "mb/ninfty-stage2-predicate/v18",
    "predicate_spec_digest": "e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56",
    "verifier_contract_id": "mb/ninfty-verifier-contract/v13",
    "verifier_contract_digest": "e41d51dbdbdcf66efaff2ccd073bbfba9bff12bbfff435ca290a4248abcf5022",
    "dependency_manifest_schema_id": "mb/dependency-manifest/v13",
    "dependency_manifest_schema_digest": "df59b25f75e8e48a4607ed39177e5aa15be5a3fd4c738391aec347d8f7c1cb3e",
}


def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def run_verifier_b(payload):
    """
    payload = {
      "certificate": {...divisor_equality_certificate...},
      "native_a": {...searcher native raw content, optional...},
      "native_b": {...checker native raw content, optional...}
    }
    **Never raises**: the outermost gate rejects a non-dict payload/
    certificate as a clean FAIL/INTEGRITY_STOP-style result before any
    witness processing; every per-witness-type function is additionally
    wrapped by @fail_closed_pairmap as defense in depth.
    """
    if not isinstance(payload, dict) or not isinstance(payload.get("certificate"), dict):
        return {
            "verifier_id": VERIFIER_ID,
            "overall_verdict_B": "INTEGRITY_STOP",
            "primary_reason_code_hint": "digest-mismatch",
            "reason": "payload is not an object, or payload['certificate'] is missing/not "
                      "an object -- fail-closed rejection before any witness processing",
            "witness_results": {label: {tok: "ABSENT" for tok in OBJECT_LABELS.values()}
                                 for label in WITNESS_LABELS},
            "unknown": ["entire certificate was structurally unusable; no further checks were attempted"],
        }

    cert = payload["certificate"]
    native_a = payload.get("native_a")
    native_b = payload.get("native_b")

    p0_status, p0_detail = verify_P0(cert, EXPECTED_PINS)
    p3_status, p3_detail = verify_P3(cert, native_a, native_b, EXPECTED_PINS)

    per_witness_pairmaps = {
        "W-1": verify_W1(cert),
        "W-2": verify_W2(cert),
        "W-2prime": verify_W2prime(cert),
        "W-3": verify_W3(cert),
        "W-4": verify_W4(cert),
        "W-5": verify_W5(cert),
        "W-6": verify_W6(cert),
    }

    # witness_results[label][object_label] = status ; kept both in this
    # nested (per-object, genuinely independent) form AND flattened into
    # R_B per contract sec.3.4's per-object vector shape.
    witness_results = {
        label: {OBJECT_LABELS[tok]: pairmap[tok][0] for tok in DIVISOR_OBJECT_TOKENS}
        for label, pairmap in per_witness_pairmaps.items()
    }
    witness_detail = {
        label: {OBJECT_LABELS[tok]: pairmap[tok][1] for tok in DIVISOR_OBJECT_TOKENS}
        for label, pairmap in per_witness_pairmaps.items()
    }

    R_B = {}
    for tok, obj_label in OBJECT_LABELS.items():
        R_B[obj_label] = [(label, per_witness_pairmaps[label][tok][0]) for label in WITNESS_LABELS]

    all_pass_ram = all(witness_results[label]["ramification_divisor_on_C"] == "PASS" for label in WITNESS_LABELS)
    all_pass_branch = all(witness_results[label]["branch_divisor_on_P1"] == "PASS" for label in WITNESS_LABELS)
    ambient_ok = p0_status == "PASS" and p3_status == "PASS"

    verdict_B = "PASS" if (ambient_ok and all_pass_ram and all_pass_branch) else "FAIL"

    result = {
        "verifier_id": VERIFIER_ID,
        "P-0": {"status": p0_status, "detail": p0_detail},
        "P-3": {"status": p3_status, "detail": p3_detail},
        "witness_results": witness_results,
        "witness_detail": witness_detail,
        "R_B": R_B,
        "overall_verdict_B": verdict_B,
    }
    result["result_digest_B"] = sha256_of(
        {
            "verifier_contract_id": EXPECTED_PINS["verifier_contract_id"],
            "verifier_contract_digest": EXPECTED_PINS["verifier_contract_digest"],
            "certificate_digest": cert.get("candidate_ref"),
            "R_B": R_B,
            "overall_verdict_B": verdict_B,
        }
    )

    result["unknown"] = [
        "[裁定128, Sol confirmation pending] certificate shape follows "
        "docs/notes/cert_shape_interpretation_v1.md (interim interface, "
        "NOT a spec revision) -- see this module's docstring for the four "
        "carried-over Sol-confirmation points (a)-(d) plus two additional "
        "spec-silence points (e)-(f) this implementer noticed while "
        "reshaping.",
        "P-0.6/P-1.4 field embedding: only presence is checked, not the "
        "embedding map itself (out of scope for this partial verifier)",
        "W-4 chart atlas: only internal consistency of declared overlaps "
        "is checked, not full re-derivation of the chart atlas",
        "CR-11 (contract sec.9.1): implemented_checks 3-layer equality is "
        "UNKNOWN -- no executable-inventory system exists yet",
        "R_A vs R_B concordance ([26]): NOT computed by this file (contract "
        "C-7: belongs to the receiving side that holds both R_A and R_B "
        "independently)",
        "P-3.3 `_ref` semantics (裁定128 rule 3): only the whole-blob "
        "native_artifact_digest is checked; a finer per-_ref sub-digest "
        "recomputation is NOT implemented (see verify_P3 docstring)",
    ]
    return result


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("payload_json", help="path to payload JSON (certificate [+native_a/native_b]), or '-' for stdin")
    args = ap.parse_args(argv)

    if args.payload_json == "-":
        payload = json.load(sys.stdin)
    else:
        with open(args.payload_json, "r", encoding="utf-8") as f:
            payload = json.load(f)

    result = run_verifier_b(payload)
    print(canonical_serialize(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
