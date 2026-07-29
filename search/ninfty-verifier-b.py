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
import math
import re
import sys
import argparse

# 裁定192 (sol/裁定_192_便83検収.md, F83-1.1/1.2 -> W-4 authority binding):
# a coefficient is accepted ONLY as a CANONICAL rational STRING (never a raw
# JSON/JS number at all -- this closes F83-1.2's unsafe-integer round-trip
# gap by construction, matching the rest of this codebase's own convention
# of always using string coefficients for native ideal_generator arrays).
# Canonical form: optional '-', then '0' or a no-leading-zero digit run
# (the integer part); OPTIONALLY '/' then a no-leading-zero positive digit
# run (the denominator) -- and if a denominator IS present, it must be > 1
# and the fraction must already be in lowest terms (gcd(|n|,d) == 1).
# Rejects (never canonicalizes) "+1", "01", "2/2", "1/01", "1/1" etc. --
# each distinct non-canonical byte string is refused, not silently rewritten,
# so canonical-form equality can be decided by plain string comparison.
# Sol 便84 F84-5.1/P84-4 fix (was: re.match with bare \d, both gaps found by
# Sol's adversarial probe): (1) re.ASCII forces \d/\w/\s to ASCII-only, and
# the character classes below are ALSO spelled out as [0-9] explicitly, so
# a Unicode digit (e.g. full-width or Arabic-indic) is rejected by
# construction, not merely by an easily-dropped flag; (2) fullmatch (not
# match) so a trailing "\n" (which Python's `$` anchor treats as matching
# just before a final newline, NOT as end-of-string) can no longer sneak a
# non-canonical byte string past the grammar.
_CANONICAL_RATIONAL_RE = re.compile(r'^(-?(?:0|[1-9][0-9]*))(?:/([1-9][0-9]*))?$', re.ASCII)


def _is_canonical_rational_string(s):
    if not isinstance(s, str):
        return False
    m = _CANONICAL_RATIONAL_RE.fullmatch(s)
    if not m:
        return False
    n_str, d_str = m.group(1), m.group(2)
    if n_str == "-0":
        return False  # F84-5.1: '-0' is not canonical -- same value as bare '0'
    if d_str is None:
        return True
    n, d = int(n_str), int(d_str)
    if n == 0:
        return False  # "0/d" is not canonical -- must be written as bare "0"
    if d == 1:
        return False  # "n/1" is not canonical -- must be written as bare "n"
    return math.gcd(abs(n), d) == 1

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


class RefDigestMismatch(MalformedWitness):
    """
    裁定139 item 3: a ref-triple ({artifact_id, digest, json_pointer|
    object_id}) that ALSO carries inline content whose recomputed digest
    disagrees with the ref's own declared digest. This is a MalformedWitness
    subtype (still caught the same way) but is tagged so callers can route
    the more specific, ALREADY-established `digest-mismatch [12]` reason
    code rather than the new (Sol-pending) generic `schema-invalid` one --
    'どちらかを黙って優先しない': both are surfaced, never silently resolved.
    """


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
# 裁定139 item 3: `_ref` triple = {artifact_id, digest, json_pointer |
# object_id}. Inline materialization ("inline" sibling key) is optional;
# WHEN present, its recomputed digest must equal the ref's declared
# `digest` exactly, or this is an integrity stop ([12] digest-mismatch),
# never a silently-preferred side. Dereferencing an ABSENT-inline,
# digest-only reference (i.e. actually walking `json_pointer` into a
# native artifact, or looking up `object_id`) is NOT implemented by this
# partial verifier -- flagged UNKNOWN (see callers), not silently assumed
# to PASS.
# --------------------------------------------------------------------------


def _parse_ref_triple(ref, what):
    _require_dict(ref, what)
    _require_keys(ref, ["artifact_id", "digest"], what)
    if "json_pointer" not in ref and "object_id" not in ref:
        raise MalformedWitness(f"{what} must carry one of json_pointer/object_id (裁定139 item 3)")
    return ref


def _check_ref_inline_consistency(ref, what):
    """Returns the inline value if present and digest-consistent; None if
    no inline content was supplied (digest-only reference). Raises
    RefDigestMismatch if inline content's digest disagrees."""
    if "inline" not in ref:
        return None
    recomputed = sha256_of(ref["inline"])
    declared = ref.get("digest")
    if recomputed != declared:
        raise RefDigestMismatch(f"{what}: inline content digest {recomputed} != declared digest {declared!r}")
    return ref["inline"]


def _resolve_json_pointer(root, pointer):
    """
    Sol 便86 P86-2 item 3 (B86-o3): RFC 6901 pointer resolution against
    `root`, ported independently from ninfty-verifier-a.mjs's own
    `resolveJsonPointer` (same algorithm -- '~1'->'/', '~0'->'~' escaping
    -- separate code, this file's own copy). Returns (found: bool, value).
    """
    if pointer == "":
        return True, root
    if not isinstance(pointer, str) or pointer[:1] != "/":
        return False, None
    node = root
    for step in pointer.split("/")[1:]:
        step = step.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or step not in node:
            return False, None
        node = node[step]
    return True, node


def _dereference_native_ref(ref, native_payload, what):
    """
    Sol 便86 P86-2 item 3 / B86-o3 fix: resolves a `_ref` triple's
    `artifact_id`+`json_pointer`/`object_id` against the RECEIVER-HELD
    PINNED native artifact (`native_payload`) -- not merely the ref's own
    self-carried `inline` copy. 裁定150 item 1 convention: `json_pointer`
    resolves WITHIN the artifact named by `artifact_id`, i.e. within
    `native_payload` itself (mirrors ninfty-verifier-a.mjs's `resolveRef`).

    Sol 便87 P87-1 item 1 (F87-1.2, closing the残り half of B86-o3): the
    prior version of this function fell back to `inline` whenever
    `json_pointer` was present but did NOT resolve inside `native_payload`
    -- an attacker could supply `json_pointer="/definitely_missing"` plus
    a self-consistent (`sha256(inline) == declared digest`) FORGED inline
    map that has no counterpart in the receiver-held native artifact at
    all, and this function would happily hand that forged value back as
    if it were authoritative (UNRESOLVED_POINTER_INLINE_ATTACK -- R1, R2,
    and overall all reached PASS on Sol's probe). `inline` is a CACHE for
    cross-checking an ALREADY-RESOLVED pointer value -- never an
    independent fallback authority for a pointer that failed to resolve.
    ★教材 1 (F87-1.2): cache は authority の複製であって、authority が
    見つからない時に authority へ昇格するものではない.

    Priority (the native artifact is AUTHORITATIVE; `inline` is a CACHE,
    consulted only when `json_pointer` was never supplied at all):
      1. `json_pointer` present and resolves inside `native_payload` ->
         that dereferenced value is the candidate; its recomputed digest
         MUST equal `ref['digest']` (RefDigestMismatch -- the existing
         [12] condition -- on disagreement). This is what actually BINDS
         the map to the pinned native artifact: a producer can no longer
         supply a self-consistent `inline` map that has no counterpart in
         `native_a`/`native_b` (closes B86-o3's "matching forged inline
         maps" and "swapped native refs" attacks).
      2. `json_pointer` present but UNRESOLVABLE inside `native_payload`
         -> MalformedWitness, unconditionally (裁定232 P87-1 item 1: no
         inline fallback here at all, regardless of whether `inline` is
         present or digest-consistent with itself -- an unresolved
         pointer is a contract violation, not mere evidence insufficiency,
         and is never a cache-eligible situation).
      3. `json_pointer` absent entirely, but `inline` present -> falls
         back to the pre-existing inline-digest-consistency check (裁定150
         items 2/3's legacy/offline fallback semantics, unchanged for the
         existing fixtures whose native payloads do not carry the pointed-
         to key at all and never claimed a `json_pointer` in the first
         place).
      4. neither `json_pointer` nor `inline` present -> (None, <reason>):
         UNKNOWN, never a silent PASS (`object_id`-only external artifact
         stores remain out of scope for this partial verifier).

    Returns (data_or_None, unknown_reason_or_None). Raises
    MalformedWitness (RefDigestMismatch on an actual digest disagreement;
    a plain MalformedWitness on an unresolved json_pointer).
    """
    json_pointer = ref.get("json_pointer") if isinstance(ref.get("json_pointer"), str) else None
    if json_pointer is not None:
        found, resolved = _resolve_json_pointer(native_payload, json_pointer)
        if not found:
            raise MalformedWitness(
                f"{what}: json_pointer {json_pointer!r} did not resolve within the pinned native "
                f"artifact (artifact_id={ref.get('artifact_id')!r}); inline is never consulted as a "
                "fallback authority for an unresolved pointer (Sol 便87 P87-1 item 1 fix, closing "
                "UNRESOLVED_POINTER_INLINE_ATTACK)"
            )
        recomputed = sha256_of(resolved)
        declared = ref.get("digest")
        if recomputed != declared:
            raise RefDigestMismatch(
                f"{what}: native artifact dereference at json_pointer={json_pointer!r} digest "
                f"{recomputed} != declared digest {declared!r} (Sol 便86 B86-o3 native-binding check)"
            )
        return resolved, None
    # json_pointer absent entirely -- legacy/offline inline-only path,
    # unchanged from before (existing fixtures rely on this; CACHE only,
    # never reached when a json_pointer was supplied at all).
    inline = _check_ref_inline_consistency(ref, what)
    if inline is not None:
        return inline, None
    reason = (f"{what}: no json_pointer and no inline content -- object_id-only external artifact "
              "stores are out of scope for this partial verifier (UNKNOWN, not a silent PASS)")
    return None, reason


# --------------------------------------------------------------------------
# 裁定139 (v3 item 5, F77-4.3): ABSENT and MALFORMED are DISTINCT statuses,
# not both folded into "FAIL":
#   - key entirely missing, OR present as an explicit []  -> ABSENT
#     (evidence insufficiency; still prevents overall PASS, but is not a
#     schema violation)
#   - key present as null, a non-array, OR an entry lacking/carrying an
#     unrecognized tag -> MALFORMED (a contract/schema violation; stops at
#     the parse/schema layer and is never silently folded into ABSENT or
#     an ordinary witness FAIL)
# MALFORMED anywhere escalates the overall verdict to INTEGRITY_STOP
# (schema-invalid gate stop) in run_verifier_b, taking priority over a
# plain per-witness FAIL -- see SCHEMA_INVALID_DETECTED / _record_malformed.
# --------------------------------------------------------------------------


def _read_container(cert, field_name):
    """
    Returns (kind, value):
      kind="missing"       value=[]      -- key not present at all
      kind="empty"         value=[]      -- key present, explicit []
      kind="malformed_null" value=None   -- key present, explicit null
      kind="malformed_type" value=<raw>  -- key present, not null, not a list
      kind="list"          value=<list>  -- key present, well-typed nonempty list
    """
    if field_name not in cert:
        return "missing", []
    v = cert[field_name]
    if v is None:
        return "malformed_null", None
    if isinstance(v, list):
        return ("empty", []) if len(v) == 0 else ("list", v)
    return "malformed_type", v


def _split_by_divisor_object(entries, tag_field="divisor_object", tag_values=None):
    """
    Groups entries by their tag (default 'divisor_object', values default
    to DIVISOR_OBJECT_TOKENS -- overridable for W-6's 'native_side' tag).
    Entries that are not dicts, lack the tag, or carry an unrecognized
    value are collected as 'unattributed' -- these make the field
    MALFORMED (裁定139 item 5), never silently dropped and never folded
    into an ordinary witness FAIL.
    """
    values = tag_values if tag_values is not None else DIVISOR_OBJECT_TOKENS
    groups = {v: [] for v in values}
    unattributed = []
    for i, e in enumerate(entries):
        tag = e.get(tag_field) if isinstance(e, dict) else None
        if tag in groups:
            groups[tag].append(e)
        else:
            unattributed.append((i, e))
    return groups, unattributed


def _absent_pair(reason):
    return {tok: ("ABSENT", {"reason": reason}) for tok in DIVISOR_OBJECT_TOKENS}


def _malformed_pair(reason):
    return {tok: ("MALFORMED", {"reason": reason}) for tok in DIVISOR_OBJECT_TOKENS}


def _container_gate(cert, field_name):
    """
    Shared first step for both plural and singular witness checkers:
    resolves the ABSENT-vs-MALFORMED-vs-well-typed-list question for the
    top-level container. Returns either a completed pair-map (for the
    ABSENT/MALFORMED terminal cases) or None (meaning: proceed with the
    well-typed, nonempty `raw` list returned alongside it).
    """
    kind, raw = _read_container(cert, field_name)
    if kind in ("missing", "empty"):
        return _absent_pair(f"{field_name} {'not supplied' if kind == 'missing' else 'is explicit []'} "
                             "(ABSENT, 裁定139 item 5)"), None
    if kind == "malformed_null":
        return _malformed_pair(f"{field_name} is explicit null (MALFORMED, 裁定139 item 5 -- "
                                "null is never a valid ABSENT/status marker)"), None
    if kind == "malformed_type":
        return _malformed_pair(f"{field_name} must be an array, got {type(raw).__name__} "
                                f"(MALFORMED, 裁定139 item 5)"), None
    return None, raw


def _check_plural_witness(cert, field_name, validate_entry):
    """
    For W-2/W-2'/W-3/W-4 style fields: any number of entries per object,
    ALL must PASS for that object's channel to PASS. Schema violations
    (missing/unrecognized divisor_object tag, or a MalformedWitness raised
    by validate_entry) yield MALFORMED for the affected object(s), kept
    distinct from an ordinary arithmetic FAIL.
    """
    terminal, raw = _container_gate(cert, field_name)
    if terminal is not None:
        return terminal

    groups, unattributed = _split_by_divisor_object(raw)
    unattributed_reason = None
    if unattributed:
        unattributed_reason = (
            f"{len(unattributed)} entr{'y' if len(unattributed) == 1 else 'ies'} in {field_name} "
            f"lack a recognized 'divisor_object' tag and cannot be attributed to either native "
            f"object -- MALFORMED (schema violation, 裁定139 item 5), not silently dropped"
        )

    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        entries = groups[tok]
        if not entries and not unattributed:
            out[tok] = ("ABSENT", {"reason": f"no {field_name} entries tagged divisor_object={tok!r}"})
            continue
        details = []
        any_malformed = False
        all_ok = True
        for i, e in enumerate(entries):
            try:
                status, detail = validate_entry(e)
            except MalformedWitness as ex:
                status, detail = "MALFORMED", {"reason": str(ex), "digest_mismatch": isinstance(ex, RefDigestMismatch)}
            details.append({"index": i, "status": status, "detail": detail})
            if status == "MALFORMED":
                any_malformed = True
            if status != "PASS":
                all_ok = False
        if unattributed:
            any_malformed = True
            details.append({"unattributed_entries": len(unattributed), "reason": unattributed_reason})
        if not entries and unattributed:
            out[tok] = ("MALFORMED", {"entries": details})
        elif any_malformed:
            out[tok] = ("MALFORMED", {"entries": details})
        else:
            out[tok] = ("PASS" if all_ok else "FAIL", {"entries": details})
    return out


def _check_singular_witness(cert, field_name, validate_entry):
    """
    For W-1/W-5 style fields (2-entry array, one per object). Exactly one
    entry per object is expected; 0 -> ABSENT, >1 or a MalformedWitness
    raised by validate_entry -> MALFORMED (schema violation), kept
    distinct from an ordinary arithmetic FAIL.
    """
    terminal, raw = _container_gate(cert, field_name)
    if terminal is not None:
        return terminal

    groups, unattributed = _split_by_divisor_object(raw)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        entries = groups[tok]
        if len(entries) == 0:
            out[tok] = ("ABSENT", {"reason": f"no {field_name} entry tagged divisor_object={tok!r}"})
        elif len(entries) > 1:
            out[tok] = ("MALFORMED", {"reason": f"{field_name} has {len(entries)} entries tagged "
                                       f"divisor_object={tok!r}, expected exactly 1 (singular witness)"})
        else:
            try:
                status, detail = validate_entry(entries[0])
            except MalformedWitness as ex:
                status, detail = "MALFORMED", {"reason": str(ex), "digest_mismatch": isinstance(ex, RefDigestMismatch)}
            out[tok] = (status, detail)
    if unattributed:
        reason = (f"{len(unattributed)} unattributed entries present in {field_name} "
                  "(missing/unrecognized divisor_object tag) -- MALFORMED, not silently dropped")
        for tok in DIVISOR_OBJECT_TOKENS:
            out[tok] = ("MALFORMED", {"reason": reason})
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
        except MalformedWitness as e:
            detail = {"reason": f"schema violation while checking this witness type: {e}",
                      "digest_mismatch": isinstance(e, RefDigestMismatch)}
            return {tok: ("MALFORMED", detail) for tok in DIVISOR_OBJECT_TOKENS}
        except Exception as e:  # noqa: BLE001 -- deliberate blanket catch, fail-closed by design
            detail = {
                "crashed": True,
                "exception_type": type(e).__name__,
                "exception": str(e),
                "reason": "unexpected exception while checking this witness type -- "
                          "treated as MALFORMED for both object channels (裁定139: an "
                          "unexpected processing failure is a schema/processing problem, "
                          "not a mathematical FAIL), never a crash or silent PASS (裁定127 fix (i))",
            }
            return {tok: ("MALFORMED", detail) for tok in DIVISOR_OBJECT_TOKENS}
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
        raise MalformedWitness(f"wrong kind for W-2 (must be ideal-equality, got {witness.get('kind')!r})")
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
        raise MalformedWitness(f"wrong kind for W-2' (must be disjointness, got {witness.get('kind')!r})")
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


def _validate_w4_inner_item(o, i, chart_ids, native_a, native_b):
    """
    v3 successor 条項7 (docs/notes/cert_shape_interpretation_v3_addendum_n_v3.md,
    Sol 便84 F84-5.2/P84-3, superseding 裁定192 F83-1.1's chart_pair name):
    validates ONE entries[] item against the UNIFIED, authority-bound item
    schema -- the SAME schema lane A's ninfty-verifier-a.mjs
    classifyChartOverlapEntry now requires:

        {side_pair: ["searcher","checker"],  # FIXED literal pair, in this
                                          # exact order -- NOT two chart ids.
                                          # Sol F84-5.2: the prior
                                          # 'chart_pair' name/shape (two
                                          # distinct chart_ids) implied a
                                          # real chart-transport claim this
                                          # payload cannot back up (no
                                          # registry binds a chart id to a
                                          # native side/digest/coordinate
                                          # ring, so a swapped chart-id pair
                                          # could never actually be
                                          # rejected). What IS actually
                                          # checked below is searcher-side
                                          # vs checker-side native equality
                                          # -- side_pair says exactly that.
                                          # Swapping it
                                          # (["checker","searcher"]) is
                                          # REJECTED as MALFORMED, not
                                          # silently accepted.
         locus_type: <str>,               # must resolve to a REAL native
                                          # component (searcher AND checker)
                                          # for this divisor_object
         component_in_chart_a: <str>,     # == locus_type (this payload has
         component_in_chart_b: <str>,     # only ONE native representation
                                          # per side, not a genuine per-chart
                                          # local-naming registry -- distinct
                                          # per-chart local ids are UNKNOWN/
                                          # out of scope pending a real chart
                                          # registry, condition 4)
         agree: <bool>,                   # producer claim, unscored
         generator_chart_a: [<canonical rational str>, ...],
         generator_chart_b: [<canonical rational str>, ...]}

    Raises MalformedWitness for ANY schema violation (missing/mistyped
    field, wrong/swapped side_pair, unresolvable locus_type, non-canonical
    coefficient string, raw JSON number coefficient -- F83-1.2 closed by
    construction: _is_canonical_rational_string never accepts a Python
    int/float at all, only an already-canonical string). Returns True/False
    (agrees / disagrees) when the item is well-formed and its generators are
    resolvable: 裁定192 condition 3 -- generator_chart_a/b are no longer
    compared to EACH OTHER (a producer self-consistency check); each is
    independently compared, by EXACT canonical-string-list equality, against
    the RECEIVER-DERIVED native ideal_generator for `locus_type` on the
    searcher side (for generator_chart_a) and the checker side (for
    generator_chart_b) respectively -- disagreement is a genuine
    native-binding FAILURE (this item disagrees), not a schema violation.
    This is a searcher/checker-SIDE-native-equality check (W-4's real name
    per Sol 便84 F84-5.2), NOT a chart-overlap / chart-transport proof --
    coordinate TRANSITION TRANSPORT across genuinely distinct charts
    remains UNKNOWN with the current payload (there is only one native
    representation per side, not a second chart's native data to transport
    into).
    """
    if not isinstance(o, dict):
        raise MalformedWitness(f"entries[{i}] is not an object")

    side_pair = o.get("side_pair")
    if not isinstance(side_pair, list) or side_pair != ["searcher", "checker"]:
        raise MalformedWitness(
            f"entries[{i}].side_pair must be EXACTLY ['searcher','checker'] in this fixed order (Sol 便84 "
            "F84-5.2/P84-3: this records searcher/checker-side native equality, not a swappable chart-id "
            f"pair -- chart transport across genuinely distinct charts is UNKNOWN with this payload), got {side_pair!r}"
        )

    locus_type = o.get("locus_type")
    if not isinstance(locus_type, str) or not locus_type:
        raise MalformedWitness(f"entries[{i}].locus_type must be a non-empty string")

    for field in ("component_in_chart_a", "component_in_chart_b"):
        v = o.get(field)
        if not isinstance(v, str) or not v:
            raise MalformedWitness(f"entries[{i}].{field} must be a non-empty string")
        if v != locus_type:
            raise MalformedWitness(
                f"entries[{i}].{field}={v!r} != locus_type={locus_type!r} -- this payload has only one "
                "native representation per side, so distinct per-chart local component naming is UNKNOWN "
                "(out of scope pending a real chart registry, 裁定192 F83-1.1 condition 4)"
            )

    if not isinstance(o.get("agree"), bool):
        raise MalformedWitness(f"entries[{i}].agree must be a boolean")

    for field in ("generator_chart_a", "generator_chart_b"):
        g = o.get(field)
        if not isinstance(g, list) or len(g) == 0 or not all(_is_canonical_rational_string(c) for c in g):
            raise MalformedWitness(
                f"entries[{i}].{field} must be a non-empty array of CANONICAL rational strings "
                "(integer or reduced 'n/d' with d>1, no leading zeros, no explicit '+', no raw JSON "
                f"numbers at all -- 裁定192 F83-1.1 condition 5 / F83-1.2), got {g!r}"
            )

    searcher_gen = _native_component_by_locus(native_a, o["divisor_object"], locus_type) if isinstance(o.get("divisor_object"), str) else None
    checker_gen = _native_component_by_locus(native_b, o["divisor_object"], locus_type) if isinstance(o.get("divisor_object"), str) else None
    if searcher_gen is None or checker_gen is None:
        raise MalformedWitness(
            f"entries[{i}].locus_type={locus_type!r} does not resolve to a real native component on "
            f"{'the searcher side' if searcher_gen is None else 'the checker side'} for this divisor_object "
            "-- unresolvable reference (裁定192 F83-1.1 condition 3)"
        )

    return o["generator_chart_a"] == searcher_gen and o["generator_chart_b"] == checker_gen


def _make_w4_entry_validator(chart_ids, native_a, native_b):
    """
    Factory producing the `validate_entry(e)` closure `_check_singular_witness`
    calls -- reads `e["divisor_object"]` itself (already present on every
    chart_overlap_witnesses entry) to select the correct native components
    per side, so a single closure serves BOTH divisor_object tokens without
    needing _check_singular_witness itself to change.
    """
    def validate_entry(e):
        """
        W-4 entry (裁定139 item 7 = v2 (l) maintained: EXACTLY 1 entry per
        divisor_object). 追補(n) v2 (裁定152 §3-1) ABSENT/PRESENT marker
        rules 1-7 are UNCHANGED (see docs/notes/
        cert_shape_interpretation_v3_addendum_n.md v2); this factory adds
        裁定192 F83-1.1's authority-bound inner-item schema on top, for the
        PRESENT/non-empty path only.
        """
        _require_dict(e, "W-4 entry")
        if "per_overlap_witnesses" in e:
            raise MalformedWitness(
                "W-4 entry carries the RETIRED 'per_overlap_witnesses' key alongside the "
                "canonical shape -- ambiguous regardless of whether it agrees with 'entries', "
                "never silently ignored (裁定177 F80-4.2 condition 5; run "
                "search/ninfty-legacy-normalizer.py first if this is genuinely legacy data)"
            )
            # (unreachable safety net -- kept identical to the pre-192 logic)
        _require_keys(e, ["status", "entries"], "W-4 entry")
        status = e["status"]
        if status not in ("ABSENT", "PRESENT"):
            raise MalformedWitness(
                f"W-4 entry.status must be exactly 'ABSENT' or 'PRESENT' (追補(n) v2 -- no bare "
                f"array default, no free-text producer-claim vocabulary), got {status!r}"
            )
        entries = _require_list(e["entries"], "W-4 entry.entries")
        if status == "ABSENT":
            if len(entries) != 0:
                raise MalformedWitness(
                    f"W-4 entry.status=ABSENT but entries is non-empty ({len(entries)} entries) -- "
                    "contradicts the ABSENT declaration (追補(n) v2 rule 3)"
                )
            return "ABSENT", {
                "reason": e.get(
                    "reason",
                    "structured ABSENT marker (追補(n) v2 rule 1): status=ABSENT, entries=[] -- "
                    "insufficient evidence, not FAIL",
                )
            }
        # status == "PRESENT"
        if len(entries) == 0:
            raise MalformedWitness(
                "W-4 entry.status=PRESENT but entries is empty -- declares presence while "
                "supplying no evidence, the mirror self-contradiction of rule 3 (追補(n) v2 rule 5, "
                "裁定149)"
            )
        # 裁定192: divisor_object must be present on the entry itself so the
        # inner-item validator can select the right native side (it always
        # is, per the generator's own tagging convention -- but this is
        # re-checked here defensively, not assumed).
        tag = e.get("divisor_object")
        if not isinstance(tag, str) or not tag:
            raise MalformedWitness("W-4 entry missing/invalid 'divisor_object' -- required to resolve native binding")
        # each entries[] item inherits the outer entry's own divisor_object
        # tag (not itself individually tagged) -- used only to select which
        # native side's components to resolve against.
        agrees = [
            _validate_w4_inner_item({**o, "divisor_object": tag} if isinstance(o, dict) else o, i, chart_ids, native_a, native_b)
            for i, o in enumerate(entries)
        ]
        bad = [{"index": i} for i, ok in enumerate(agrees) if not ok]
        overall_ok = len(bad) == 0
        return ("PASS" if overall_ok else "FAIL"), {"mismatches": bad, "checked": len(entries)}

    return validate_entry


@fail_closed_pairmap
def verify_W4(cert, native_a, native_b):
    """W-4: chart_overlap_witnesses (裁定139 item 7: exactly 1 entry per
    divisor_object -- layering lives inside entries[], 追補(n) v2 裁定152).
    裁定192 F83-1.1: now receives native_a/native_b so the inner entries[]
    schema can be bound to REAL native divisor data (chart_ids come from
    `cert` itself)."""
    chart_ids = cert.get("chart_ids") if isinstance(cert, dict) else None
    return _check_singular_witness(cert, "chart_overlap_witnesses", _make_w4_entry_validator(chart_ids, native_a, native_b))


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


def _native_component_ids(native_payload, tok):
    """
    Best-effort extraction of component ids from native_payload[tok]
    ['components']. 裁定139 追補 (m): the authoritative component_id is
    the FULLY QUALIFIED form "<divisor_object_ref>:<locus_type>" (matching
    the generator's own edge id convention in component_bijection) -- this
    is DERIVED here from (tok, locus_type), not read from any
    self-reported 'component_id' field the native artifact might also
    carry, so the receiving side's namespace is independent of what the
    producer happened to write.
    Returns None (not []) if the native payload is unreadable at this
    path, so callers can distinguish "no components" from "cannot check".
    """
    if not isinstance(native_payload, dict):
        return None
    obj = native_payload.get(tok)
    if not isinstance(obj, dict):
        return None
    comps = obj.get("components")
    if not isinstance(comps, list):
        return None
    return [f"{tok}:{c['locus_type']}" for c in comps if isinstance(c, dict) and "locus_type" in c]


def _native_component_by_locus(native_payload, tok, locus_type):
    """
    裁定192 (F83-1.1 condition 3): looks up the REAL native component
    matching `locus_type` for divisor_object `tok`, returning its
    `ideal_generator` (a list) -- or None if native_payload/tok/components
    is unreadable, or no component with that locus_type exists at all
    (native data does not attest this locus -- an unresolvable reference,
    distinct from "resolvable but the generator disagrees").
    """
    if not isinstance(native_payload, dict):
        return None
    obj = native_payload.get(tok)
    if not isinstance(obj, dict):
        return None
    comps = obj.get("components")
    if not isinstance(comps, list):
        return None
    for c in comps:
        if isinstance(c, dict) and c.get("locus_type") == locus_type:
            gen = c.get("ideal_generator")
            return gen if isinstance(gen, list) else None
    return None


def _validate_bijection_edges_for_token(entries, tok, native_a, native_b):
    """
    裁定139 item 6: component_bijection is an EDGE list -- entries =
    {divisor_object, searcher_native_digest, searcher_component_id,
    checker_native_digest, checker_component_id}. Self-reported domain/
    codomain lists are NOT the authority: both component sets are
    reconstructed here from the actual native_a/native_b payload (via
    _native_component_ids), and in/out-degree = 1 (injectivity + full
    coverage) is checked against THAT reconstruction, not against
    anything the certificate merely claims. searcher_native_digest /
    checker_native_digest are cross-checked against the ACTUAL recomputed
    digest of native_a/native_b (RefDigestMismatch, i.e. integrity-stop
    [12], on disagreement -- distinct from an ordinary schema MALFORMED).
    """
    if len(entries) == 0:
        return "ABSENT", {"reason": f"no component_bijection edges for divisor_object={tok!r}"}

    searcher_ids_actual = _native_component_ids(native_a, tok)
    checker_ids_actual = _native_component_ids(native_b, tok)

    # 裁定142 self-audit finding: when native reconstruction is entirely
    # unavailable for one or both sides (native_a/native_b is None or
    # unreadable -- e.g. self-contained resolution failed and the runner
    # supplied nothing either), the coverage check used to be SKIPPED
    # (treated as vacuously satisfied) rather than reported as
    # insufficient evidence -- reopening exactly the "self-reported list
    # is not authority" gap item 6 exists to close, in this one fallback
    # case. Fixed here: no independent native reconstruction on EITHER
    # side means this witness cannot legitimately PASS at all -- ABSENT
    # (insufficient evidence), not a silent pass-by-omission.
    if searcher_ids_actual is None or checker_ids_actual is None:
        return "ABSENT", {
            "reason": "native_a and/or native_b could not be independently reconstructed for this "
                      "divisor_object (neither runner-supplied nor self-resolvable from the "
                      "certificate's embedded refs) -- W-1 requires native reconstruction "
                      "(裁定139 item 6: self-reported lists are not authority), so this is "
                      "insufficient evidence, not a PASS",
            "searcher_ids_resolvable": searcher_ids_actual is not None,
            "checker_ids_resolvable": checker_ids_actual is not None,
        }

    searcher_digest_actual = sha256_of(native_a) if isinstance(native_a, dict) else None
    checker_digest_actual = sha256_of(native_b) if isinstance(native_b, dict) else None

    searcher_used, checker_used = [], []
    for i, e in enumerate(entries):
        _require_dict(e, f"component_bijection edge[{i}]")
        _require_keys(e, ["searcher_native_digest", "searcher_component_id",
                          "checker_native_digest", "checker_component_id"],
                       f"component_bijection edge[{i}]")
        if searcher_digest_actual is not None and e["searcher_native_digest"] != searcher_digest_actual:
            raise RefDigestMismatch(
                f"component_bijection edge[{i}].searcher_native_digest {e['searcher_native_digest']!r} "
                f"!= actual recomputed native_a digest {searcher_digest_actual!r}")
        if checker_digest_actual is not None and e["checker_native_digest"] != checker_digest_actual:
            raise RefDigestMismatch(
                f"component_bijection edge[{i}].checker_native_digest {e['checker_native_digest']!r} "
                f"!= actual recomputed native_b digest {checker_digest_actual!r}")
        searcher_used.append(e["searcher_component_id"])
        checker_used.append(e["checker_component_id"])

    injective_searcher = len(set(searcher_used)) == len(searcher_used)
    injective_checker = len(set(checker_used)) == len(checker_used)
    covers_searcher = set(searcher_used) == set(searcher_ids_actual)
    covers_checker = set(checker_used) == set(checker_ids_actual)
    ok = injective_searcher and injective_checker and covers_searcher and covers_checker
    detail = {
        "edge_count": len(entries),
        "injective_searcher_component_id": injective_searcher,
        "injective_checker_component_id": injective_checker,
        "covers_all_searcher_native_components": covers_searcher,
        "covers_all_checker_native_components": covers_checker,
        "searcher_component_ids_actual": searcher_ids_actual,
        "checker_component_ids_actual": checker_ids_actual,
    }
    return ("PASS" if ok else "FAIL"), detail


@fail_closed_pairmap
def verify_W1(cert, native_a, native_b):
    """
    W-1: component_bijection (裁定139 item 6: edge list, native-artifact
    reconstruction -- self-reported domain/codomain lists are NOT used).
    """
    kind, raw = _read_container(cert, "component_bijection")
    if kind in ("missing", "empty"):
        return _absent_pair(f"component_bijection {'not supplied' if kind == 'missing' else 'is explicit []'} "
                             "(ABSENT)")
    if kind == "malformed_null":
        return _malformed_pair("component_bijection is explicit null (MALFORMED)")
    if kind == "malformed_type":
        return _malformed_pair(f"component_bijection must be an array, got {type(raw).__name__} (MALFORMED)")

    groups, unattributed = _split_by_divisor_object(raw)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        try:
            status, detail = _validate_bijection_edges_for_token(groups[tok], tok, native_a, native_b)
        except MalformedWitness as ex:
            status, detail = "MALFORMED", {"reason": str(ex), "digest_mismatch": isinstance(ex, RefDigestMismatch)}
        if unattributed and status != "MALFORMED":
            status, detail = "MALFORMED", {"reason": f"{len(unattributed)} unattributed component_bijection "
                                            "edges present (missing/unrecognized divisor_object tag)"}
        out[tok] = (status, detail)
    return out


def _actual_bijection_entry_counts(cert):
    """{token: actual number of component_bijection EDGES for that token}
    (raw count, independent of whether verify_W1 itself PASSes) -- used
    only for W-5's matched_count cross-check. Never raises."""
    kind, raw = _read_container(cert, "component_bijection")
    if kind not in ("missing", "empty", "list"):
        return {tok: None for tok in DIVISOR_OBJECT_TOKENS}
    groups, _unattributed = _split_by_divisor_object(raw)
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


NATIVE_SIDE_VALUES = ("searcher", "checker")


def _extract_w6_map(entry, native_payload, label):
    """
    Reads ONE W-6 lane entry: {native_side, ramification_ref, branch_ref,
    map_ref, witness_ref} (裁定139 item 2). Each of the four ref fields
    must be a valid ref-triple (item 3); ramification_ref/branch_ref/
    witness_ref are still checked for inline/digest consistency ONLY (that
    scope is unchanged by 便86 -- Sol's B86-o3 finding was specifically
    about map_ref).

    Sol 便86 P86-2 item 3 (B86-o3 fix): map_ref is now DEREFERENCED
    against the RECEIVER-HELD pinned `native_payload` via
    `_dereference_native_ref` (json_pointer resolved into the actual
    native artifact, authoritative; `inline` is a cache fallback only) --
    NOT merely read from its self-carried `inline` copy. A map_ref that
    neither resolves via json_pointer/object_id into native_payload nor
    carries a digest-consistent inline cache yields (None, <unknown-
    reason>), same as before, rather than a silent PASS or a crash.
    """
    _require_dict(entry, f"W-6 {label} entry")
    _require_keys(entry, ["ramification_ref", "branch_ref", "map_ref", "witness_ref"], f"W-6 {label} entry")
    for key in ("ramification_ref", "branch_ref", "witness_ref"):
        ref = _parse_ref_triple(entry[key], f"W-6 {label} entry.{key}")
        _check_ref_inline_consistency(ref, f"W-6 {label} entry.{key}")  # raises RefDigestMismatch on conflict

    map_ref = _parse_ref_triple(entry["map_ref"], f"W-6 {label} entry.map_ref")
    map_data, unknown_reason = _dereference_native_ref(map_ref, native_payload, f"W-6 {label} entry.map_ref")
    if map_data is None:
        return None, unknown_reason
    if not isinstance(map_data, list):
        raise MalformedWitness(f"{label}.map_ref dereferenced value must be an array of "
                                f"{{branch_value, multiplicity}}, got {type(map_data).__name__}")
    m = {}
    for i, e in enumerate(map_data):
        if not isinstance(e, dict) or "branch_value" not in e or "multiplicity" not in e:
            raise MalformedWitness(f"{label}.map_ref[{i}] malformed (need branch_value, multiplicity)")
        mult = _require_int(e["multiplicity"], f"{label}.map_ref[{i}].multiplicity")
        m[e["branch_value"]] = m.get(e["branch_value"], 0) + mult
    return m, None


def verify_W6_single(cert, native_a, native_b):
    """
    W-6: pushforward_compatibility_witness (裁定139 item 2: NO
    divisor_object duplication -- native_side-tagged, exactly one entry
    each for 'searcher'/'checker', representing a SINGLE cross-lane
    pushforward comparison). Returns a single (status, detail) pair, NOT
    a per-divisor_object pair-map (unlike the other six witness types) --
    the caller duplicates this single result across both display columns
    (see run_verifier_b), since the field is no longer partitioned by
    divisor_object at all.
    """
    kind, raw = _read_container(cert, "pushforward_compatibility_witness")
    if kind in ("missing", "empty"):
        return "ABSENT", {"reason": "pushforward_compatibility_witness not supplied (ABSENT)"}
    if kind == "malformed_null":
        return "MALFORMED", {"reason": "pushforward_compatibility_witness is explicit null"}
    if kind == "malformed_type":
        return "MALFORMED", {"reason": f"must be an array, got {type(raw).__name__}"}

    groups, unattributed = _split_by_divisor_object(raw, tag_field="native_side", tag_values=NATIVE_SIDE_VALUES)
    if unattributed:
        return "MALFORMED", {"reason": f"{len(unattributed)} entries lack a recognized 'native_side' tag "
                              f"(expected one of {NATIVE_SIDE_VALUES})"}
    for side in NATIVE_SIDE_VALUES:
        if len(groups[side]) == 0:
            return "ABSENT", {"reason": f"no pushforward entry for native_side={side!r}"}
        if len(groups[side]) > 1:
            return "MALFORMED", {"reason": f"{len(groups[side])} entries for native_side={side!r}, "
                                  "expected exactly 1"}

    try:
        searcher_map, searcher_unknown = _extract_w6_map(groups["searcher"][0], native_a, "searcher")
        checker_map, checker_unknown = _extract_w6_map(groups["checker"][0], native_b, "checker")
    except MalformedWitness as ex:
        return "MALFORMED", {"reason": str(ex), "digest_mismatch": isinstance(ex, RefDigestMismatch)}

    if searcher_unknown or checker_unknown:
        return "ABSENT", {"reason": "one or both lanes have no dereferenceable map content",
                          "searcher_unknown": searcher_unknown, "checker_unknown": checker_unknown}
    ok = searcher_map == checker_map
    return ("PASS" if ok else "FAIL"), {"searcher_map": searcher_map, "checker_map": checker_map}


@fail_closed_pairmap
def verify_W6(cert, native_a, native_b):
    """Wraps verify_W6_single's single result into the (token -> (status,
    detail)) pair-map shape the rest of this file's plumbing expects,
    duplicating it identically across both object labels (裁定139 item 2:
    W-6 is no longer divisor_object-partitioned)."""
    status, detail = verify_W6_single(cert, native_a, native_b)
    return {tok: (status, detail) for tok in DIVISOR_OBJECT_TOKENS}


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


def _resolve_native_from_cert_embedded(cert, side):
    """
    裁定142 item 2: self-contained fallback. When the runner does not
    separately supply native_a/native_b, derive an equivalent
    {tok: {"components": [...]}, ...} payload from the certificate's OWN
    embedded searcher_native/checker_native ref-triples (item 3:
    {artifact_id, digest, json_pointer|object_id[, inline]}) -- so a
    certificate can be verified on its own, without depending on the
    runner wiring up native_a/native_b out-of-band.

    Never raises: any parse/digest failure along the way makes this
    return None (the caller's existing None-native code paths already
    handle "cannot determine native content" honestly, as ABSENT/UNKNOWN
    -- this fallback never fabricates a PASS from an unresolvable ref).
    Only inline-carrying refs can be resolved this way; a pure digest-only
    reference (no inline) is NOT dereferenced (walking json_pointer/
    object_id into a third-party artifact store is out of scope, per the
    module docstring's existing UNKNOWN note) -- also yields None here.
    """
    key = "searcher_native" if side == "searcher" else "checker_native"
    nat = cert.get(key)
    if not isinstance(nat, dict):
        return None
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        ref = nat.get(tok)
        if not isinstance(ref, dict):
            return None
        try:
            _parse_ref_triple(ref, f"{key}.{tok}")  # accepts json_pointer OR object_id (裁定142 item 1 re-confirmed)
            inline = _check_ref_inline_consistency(ref, f"{key}.{tok}")
        except MalformedWitness:
            return None
        if inline is None:
            return None
        out[tok] = inline
    return out


def run_verifier_b(payload):
    """
    payload = {
      "certificate": {...divisor_equality_certificate...},
      "native_a": {...searcher native raw content, optional...},
      "native_b": {...checker native raw content, optional...}
    }
    native_a/native_b are OPTIONAL (裁定142 item 2): if the runner does not
    supply them, this function falls back to resolving them from the
    certificate's OWN embedded searcher_native/checker_native ref-triples
    (_resolve_native_from_cert_embedded), so a certificate is verifiable
    self-contained, not only when an external runner separately wires up
    the native artifacts.
    **Never raises**: the outermost gate rejects a non-dict payload/
    certificate as a clean FAIL/INTEGRITY_STOP-style result before any
    witness processing; every per-witness-type function is additionally
    wrapped by @fail_closed_pairmap as defense in depth.
    """
    if not isinstance(payload, dict) or not isinstance(payload.get("certificate"), dict):
        return {
            "verifier_id": VERIFIER_ID,
            "overall_verdict_B": "INTEGRITY_STOP",
            "gate_stop_reason": "schema-invalid [pending Sol enum, 裁定139 item 5]",
            "reason": "payload is not an object, or payload['certificate'] is missing/not "
                      "an object -- fail-closed rejection before any witness processing",
            "witness_results": {label: {tok: "ABSENT" for tok in OBJECT_LABELS.values()}
                                 for label in WITNESS_LABELS},
            "unknown": ["entire certificate was structurally unusable; no further checks were attempted"],
        }

    cert = payload["certificate"]
    native_a = payload.get("native_a")
    native_b = payload.get("native_b")
    native_a_self_resolved = False
    native_b_self_resolved = False
    if native_a is None:
        native_a = _resolve_native_from_cert_embedded(cert, "searcher")
        native_a_self_resolved = native_a is not None
    if native_b is None:
        native_b = _resolve_native_from_cert_embedded(cert, "checker")
        native_b_self_resolved = native_b is not None

    p0_status, p0_detail = verify_P0(cert, EXPECTED_PINS)
    p3_status, p3_detail = verify_P3(cert, native_a, native_b, EXPECTED_PINS)

    per_witness_pairmaps = {
        "W-1": verify_W1(cert, native_a, native_b),
        "W-2": verify_W2(cert),
        "W-2prime": verify_W2prime(cert),
        "W-3": verify_W3(cert),
        "W-4": verify_W4(cert, native_a, native_b),
        "W-5": verify_W5(cert),
        "W-6": verify_W6(cert, native_a, native_b),
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

    # 裁定139 item 4/5: MALFORMED is a SCHEMA/PARSE-LAYER gate stop, kept
    # distinct from an ordinary witness FAIL. If ANY witness/object shows
    # MALFORMED, the overall verdict escalates to INTEGRITY_STOP rather
    # than being folded into a plain FAIL -- and the specific reason is
    # `digest-mismatch [12]` (an established code) if any of the
    # MALFORMED detections were a ref/inline or native-digest conflict
    # (RefDigestMismatch), else the new (Sol-pending) `schema-invalid`.
    malformed_found = False
    digest_mismatch_found = False
    for pairmap in per_witness_pairmaps.values():
        for status, detail in pairmap.values():
            if status == "MALFORMED":
                malformed_found = True
                if isinstance(detail, dict) and detail.get("digest_mismatch"):
                    digest_mismatch_found = True

    all_pass_ram = all(witness_results[label]["ramification_divisor_on_C"] == "PASS" for label in WITNESS_LABELS)
    all_pass_branch = all(witness_results[label]["branch_divisor_on_P1"] == "PASS" for label in WITNESS_LABELS)
    ambient_ok = p0_status == "PASS" and p3_status == "PASS"

    if malformed_found:
        verdict_B = "INTEGRITY_STOP"
        gate_reason = "digest-mismatch" if digest_mismatch_found else "schema-invalid [pending Sol enum, 裁定139 item 5]"
    else:
        verdict_B = "PASS" if (ambient_ok and all_pass_ram and all_pass_branch) else "FAIL"
        gate_reason = None

    result = {
        "verifier_id": VERIFIER_ID,
        "P-0": {"status": p0_status, "detail": p0_detail},
        "P-3": {"status": p3_status, "detail": p3_detail},
        "witness_results": witness_results,
        "witness_detail": witness_detail,
        "R_B": R_B,
        "overall_verdict_B": verdict_B,
        "native_a_self_resolved": native_a_self_resolved,
        "native_b_self_resolved": native_b_self_resolved,
    }
    if gate_reason is not None:
        result["gate_stop_reason"] = gate_reason
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
        "[裁定139, Sol confirmation pending] certificate shape follows "
        "docs/notes/cert_shape_interpretation_v3.md (current interface, "
        "supersedes v1/v2 -- NOT a spec revision). Two points remain open "
        "per v3's own 'Sol へ残す諮問': the `schema-invalid` reason code "
        "enum (item 5) and the chart registry minimal schema (item 1).",
        "P-0.6/P-1.4 field embedding: only presence is checked, not the "
        "embedding map itself (out of scope for this partial verifier)",
        "W-4 chart atlas: only internal consistency of declared overlaps "
        "is checked, not full re-derivation of the chart atlas",
        "CR-11 (contract sec.9.1): implemented_checks 3-layer equality is "
        "UNKNOWN -- no executable-inventory system exists yet",
        "R_A vs R_B concordance ([26]): NOT computed by this file (contract "
        "C-7: belongs to the receiving side that holds both R_A and R_B "
        "independently)",
        "W-6 map_ref dereferencing (裁定139 item 2; Sol 便86 P86-2 item 3 / "
        "B86-o3 FIX applied): map_ref's json_pointer/object_id IS now "
        "walked into the receiver-held pinned native artifact via "
        "_dereference_native_ref (native content authoritative, inline is "
        "a cache fallback only) -- a map_ref that resolves neither via "
        "the pointer nor a digest-consistent inline still yields ABSENT, "
        "not a silent PASS. This closes the prior 'inline-only' gap for "
        "map_ref specifically; the OTHER json_pointer/object_id gaps "
        "listed below (self-contained native resolution) are separate "
        "code paths and remain open.",
        "chart_ids registry resolution (裁定139 item 1): this verifier "
        "does not resolve chart_ids against any curve_model_digest-keyed "
        "chart registry; only non-empty-string presence is checked "
        "(P-0.7) -- registry resolution is UNKNOWN/out of scope.",
        "native_a/native_b self-contained resolution (裁定142 item 2): "
        "see native_a_self_resolved/native_b_self_resolved fields -- when "
        "the runner does not supply native_a/native_b directly, this "
        "verifier falls back to resolving them from the certificate's own "
        "embedded searcher_native/checker_native ref-triples, but ONLY "
        "when those refs carry inline content; a pure digest-only "
        "embedded ref (no inline) is NOT dereferenced (same "
        "json_pointer/object_id walking gap as W-6's map_ref).",
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
