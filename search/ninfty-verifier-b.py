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
    """terms: list of {"coeff": "n/d"|num, "mono": [e1,e2,...]}."""
    _require_list(terms, "polynomial term list")
    out = {}
    for i, t in enumerate(terms):
        _require_dict(t, f"term[{i}]")
        _require_keys(t, ["coeff", "mono"], f"term[{i}]")
        m = _canon_mono(t["mono"])
        c = _F(t["coeff"])
        out[m] = out.get(m, Fraction(0)) + c
    return {m: c for m, c in out.items() if c != 0}


def mv_add(a, b):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, Fraction(0)) + c
    return {m: c for m, c in out.items() if c != 0}


def mv_neg(a):
    return {m: -c for m, c in a.items()}


def mv_sub(a, b):
    return mv_add(a, mv_neg(b))


def mv_mono_mul(m1, m2):
    n = max(len(m1), len(m2))
    m1 = m1 + (0,) * (n - len(m1))
    m2 = m2 + (0,) * (n - len(m2))
    return _canon_mono(list(x + y for x, y in zip(m1, m2)))


def mv_mul(a, b):
    out = {}
    for m1, c1 in a.items():
        if c1 == 0:
            continue
        for m2, c2 in b.items():
            m = mv_mono_mul(m1, m2)
            out[m] = out.get(m, Fraction(0)) + c1 * c2
    return {m: c for m, c in out.items() if c != 0}


def mv_eq(a, b):
    ac = {m: c for m, c in a.items() if c != 0}
    bc = {m: c for m, c in b.items() if c != 0}
    return ac == bc


def mv_is_zero(a):
    return all(c == 0 for c in a.values())


CONST_ONE = {(): Fraction(1)}


def mv_is_one(a):
    return mv_eq(a, CONST_ONE)


def _terms_out(poly):
    return sorted(
        ({"mono": list(m), "coeff": str(c)} for m, c in poly.items()),
        key=lambda t: t["mono"],
    )


# --------------------------------------------------------------------------
# W-2 / W-2' per-entry validators (unchanged math content from 裁定127
# repair; now called per-entry from the divisor_object-aware drivers below
# instead of iterating the whole field directly).
# --------------------------------------------------------------------------


def _validate_representation_entry(witness):
    _require_dict(witness, "representation witness")
    _require_keys(witness, ["tag", "g", "u", "h"], "representation witness")
    if witness["tag"] not in ("reduction-to-zero", "reduction-to-one"):
        raise MalformedWitness(f"invalid/missing tag (P-1.5): {witness.get('tag')!r}")
    g = mv_from_json(witness["g"])
    us_raw = _require_list(witness["u"], "representation witness 'u'")
    hs_raw = _require_list(witness["h"], "representation witness 'h'")
    if len(us_raw) != len(hs_raw):
        return "FAIL", {"reason": "u/h length mismatch", "len_u": len(us_raw), "len_h": len(hs_raw)}
    us = [mv_from_json(u) for u in us_raw]
    hs = [mv_from_json(h) for h in hs_raw]
    acc = {}
    for u, h in zip(us, hs):
        acc = mv_add(acc, mv_mul(u, h))
    ok = mv_eq(acc, g)
    return ("PASS" if ok else "FAIL"), {"recomputed": _terms_out(acc), "claimed": _terms_out(g)}


def _validate_reduction_entry(witness):
    _require_dict(witness, "reduction witness")
    _require_keys(witness, ["tag", "g"], "reduction witness")
    if witness["tag"] not in ("reduction-to-zero", "reduction-to-one"):
        raise MalformedWitness(f"invalid/missing tag (P-1.5): {witness.get('tag')!r}")
    r = mv_from_json(witness["g"])
    steps = witness.get("steps", [])
    _require_list(steps, "reduction witness 'steps'")
    for i, step in enumerate(steps):
        _require_dict(step, f"reduction step[{i}]")
        _require_keys(step, ["coeff", "mono", "generator"], f"reduction step[{i}]")
        coeff = _F(step["coeff"])
        mono = _canon_mono(step["mono"])
        gen = mv_from_json(step["generator"])
        term_poly = {mono: coeff}
        r = mv_sub(r, mv_mul(term_poly, gen))
    if witness["tag"] == "reduction-to-zero":
        ok = mv_is_zero(r)
    else:
        ok = mv_is_one(r)
    return ("PASS" if ok else "FAIL"), {"final_remainder": _terms_out(r)}


def _validate_w2_entry(w):
    _require_dict(w, "W-2 witness entry")
    kind = w.get("kind")
    if kind != "ideal-equality":
        return "FAIL", {"reason": f"wrong kind for W-2 (must be ideal-equality, got {kind!r})"}
    form = w.get("form")
    if form == "representation":
        return _validate_representation_entry(w)
    if form == "reduction-to-zero":
        return _validate_reduction_entry(w)
    return "FAIL", {"reason": f"unrecognized form: {form!r}"}


def _validate_w2prime_entry(w):
    _require_dict(w, "W-2' witness entry")
    kind = w.get("kind")
    if kind != "disjointness":
        return "FAIL", {"reason": f"wrong kind for W-2' (must be disjointness, got {kind!r})"}
    _require_keys(w, ["u", "g"], "W-2' witness entry")
    u_raw = _require_list(w["u"], "W-2' witness entry 'u'")
    g_raw = _require_list(w["g"], "W-2' witness entry 'g'")
    if len(u_raw) != len(g_raw):
        return "FAIL", {"reason": "u/g length mismatch"}
    u = [mv_from_json(x) for x in u_raw]
    g = [mv_from_json(x) for x in g_raw]
    acc = {}
    for ui, gi in zip(u, g):
        acc = mv_add(acc, mv_mul(ui, gi))
    ok = mv_is_one(acc)
    return ("PASS" if ok else "FAIL"), {"recomputed": _terms_out(acc)}


def _validate_w3_entry(e):
    _require_dict(e, "W-3 entry")
    _require_keys(e, ["mult_A", "mult_B"], "W-3 entry")
    ma = _require_int(e["mult_A"], "W-3 entry.mult_A")
    mb = _require_int(e["mult_B"], "W-3 entry.mult_B")
    ok = ma == mb
    return ("PASS" if ok else "FAIL"), {"mult_A": ma, "mult_B": mb}


def _validate_w4_entry(e):
    _require_dict(e, "W-4 entry")
    _require_keys(e, ["component_in_chart_a", "component_in_chart_b"], "W-4 entry")
    ok = e["component_in_chart_a"] == e["component_in_chart_b"]
    return ("PASS" if ok else "FAIL"), {
        "component_in_chart_a": e["component_in_chart_a"],
        "component_in_chart_b": e["component_in_chart_b"],
    }


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
# W-1 / W-5 / W-6: "singular" witnesses (裁定128 rule 4 -- 2-entry array,
# one per divisor_object). W-1 and W-6 additionally cross-check against
# W-5's per-object declared_total_components to close the exact
# empty-vs-empty vacuous-PASS hole 裁定127 identified, now applied
# per-object rather than once globally.
# --------------------------------------------------------------------------


def _validate_bijection_entry_factory(declared_total):
    def _validate(bij):
        _require_dict(bij, "component_bijection entry")
        _require_keys(bij, ["domain_components", "codomain_components", "mapping"], "component_bijection entry")
        domain = _require_list(bij["domain_components"], "component_bijection entry.domain_components")
        codomain = _require_list(bij["codomain_components"], "component_bijection entry.codomain_components")
        mapping = _require_list(bij["mapping"], "component_bijection entry.mapping")
        for i, m in enumerate(mapping):
            if not isinstance(m, list) or len(m) != 2:
                raise MalformedWitness(f"component_bijection entry.mapping[{i}] must be a 2-element "
                                        f"[domain_id, codomain_id] array, got {m!r}")

        if not domain and not codomain and not mapping:
            if declared_total not in (0, None):
                return "FAIL", {
                    "reason": "component_bijection entry is entirely empty, but the matching "
                              "total_coverage_and_no_extra_component_witness entry declares "
                              f"declared_total_components={declared_total!r} (!= 0) -- refusing a "
                              "vacuous empty-vs-empty PASS"
                }

        mapped_dom = [m[0] for m in mapping]
        mapped_cod = [m[1] for m in mapping]
        dom_set = set(domain)
        cod_set = set(codomain)
        total = set(mapped_dom) == dom_set and len(mapped_dom) == len(dom_set)
        injective = len(set(mapped_cod)) == len(mapped_cod)
        onto_declared_cod = set(mapped_cod) == cod_set
        ok = total and injective and onto_declared_cod
        detail = {
            "total": total, "injective": injective, "onto_declared_codomain": onto_declared_cod,
            "domain_size": len(dom_set), "codomain_size": len(cod_set), "mapping_size": len(mapping),
        }
        return ("PASS" if ok else "FAIL"), detail
    return _validate


def _validate_coverage_entry_factory(matched_count):
    """
    matched_count: the SAME-token component_bijection entry's mapping
    length (or None if W-1's bijection entry for this token could not be
    read) -- cross-referenced here so W-5's PASS genuinely requires (a)
    declared_total_components to agree with W-1's actual matched count for
    the SAME divisor_object, and (b) every extra candidate to carry a
    distinctness_witness_ref. Fixing a regression caught during this
    file's own 裁定128 reshape self-test: an earlier draft of this
    function always returned PASS regardless of (a)/(b), silently
    dropping the fail-open guard the pre-128 verify_W5 had.
    """
    def _validate(w):
        _require_dict(w, "total_coverage entry")
        _require_keys(w, ["declared_total_components"], "total_coverage entry")
        declared_total = _require_int(w["declared_total_components"],
                                       "total_coverage entry.declared_total_components")
        extras = w.get("extra_candidates", [])
        if not isinstance(extras, list):
            return "FAIL", {"reason": f"extra_candidates must be an array, got {type(extras).__name__}"}
        extras_have_distinctness = True
        for e in extras:
            ref = e.get("distinctness_witness_ref") if isinstance(e, dict) else None
            if not ref:
                extras_have_distinctness = False
        no_extra = len(extras) == 0
        matched_ok = matched_count is None or declared_total == matched_count
        ok = matched_ok and (no_extra or extras_have_distinctness)
        detail = {
            "declared_total": declared_total,
            "matched_count_from_W1": matched_count,
            "matched_ok": matched_ok,
            "extras": len(extras),
            "extras_have_distinctness_ref": extras_have_distinctness,
        }
        return ("PASS" if ok else "FAIL"), detail
    return _validate


def _validate_pushforward_entry_factory(declared_total):
    def _validate(w):
        _require_dict(w, "pushforward entry")
        _require_keys(w, ["ramification_points", "branch_points"], "pushforward entry")
        ram = _require_list(w["ramification_points"], "pushforward entry.ramification_points")
        branch = _require_list(w["branch_points"], "pushforward entry.branch_points")

        if len(ram) == 0 and len(branch) == 0:
            if declared_total not in (0, None):
                return "FAIL", {
                    "reason": "both ramification_points and branch_points are empty in this "
                              "pushforward entry, but the matching total_coverage entry declares "
                              f"declared_total_components={declared_total!r} (!= 0) -- refusing a "
                              "vacuous empty-vs-empty PASS"
                }

        push = {}
        for i, r in enumerate(ram):
            if not isinstance(r, dict) or "maps_to_branch_value" not in r or "multiplicity" not in r:
                raise MalformedWitness(f"ramification_points[{i}] malformed (need "
                                        f"maps_to_branch_value, multiplicity): {r!r}")
            bv = r["maps_to_branch_value"]
            mult = _require_int(r["multiplicity"], f"ramification_points[{i}].multiplicity")
            push[bv] = push.get(bv, 0) + mult

        declared = {}
        for i, b in enumerate(branch):
            if not isinstance(b, dict) or "branch_value" not in b or "multiplicity" not in b:
                raise MalformedWitness(f"branch_points[{i}] malformed (need "
                                        f"branch_value, multiplicity): {b!r}")
            bv = b["branch_value"]
            mult = _require_int(b["multiplicity"], f"branch_points[{i}].multiplicity")
            declared[bv] = mult

        ok = set(push.keys()) == set(declared.keys()) and all(push[k] == declared[k] for k in push)
        return ("PASS" if ok else "FAIL"), {"recomputed": push, "declared": declared}
    return _validate


def _matched_counts_by_object(cert):
    """
    Best-effort extraction of {token: len(mapping) or None} from the raw
    (uncoerced) component_bijection container, for cross-checking W-5
    against W-1's actual matched count. Never raises.
    """
    raw, _coerced = _coerce_to_list(cert, "component_bijection")
    groups, _unattributed = _split_by_divisor_object(raw)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        entries = groups[tok]
        val = None
        if len(entries) == 1 and isinstance(entries[0], dict):
            mapping = entries[0].get("mapping")
            if isinstance(mapping, list):
                val = len(mapping)
        out[tok] = val
    return out


@fail_closed_pairmap
def verify_W5(cert):
    """W-5: total_coverage_and_no_extra_component_witness (裁定128 singular -> 2-entry array),
    cross-checked against W-1's actual matched count for the same divisor_object."""
    matched = _matched_counts_by_object(cert)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        result_pair = _check_singular_witness(
            {"total_coverage_and_no_extra_component_witness":
                cert.get("total_coverage_and_no_extra_component_witness")},
            "total_coverage_and_no_extra_component_witness",
            _validate_coverage_entry_factory(matched[tok]),
        )
        out[tok] = result_pair[tok]
    return out


def _declared_totals_by_object(cert):
    """
    Best-effort extraction of {token: declared_total_components or None}
    from the raw (uncoerced) total_coverage container, for cross-checking
    W-1/W-6 against W-5. Never raises -- any malformation here just yields
    None for that token (the W-5 check itself independently reports the
    malformation via verify_W5).
    """
    raw, _coerced = _coerce_to_list(cert, "total_coverage_and_no_extra_component_witness")
    groups, _unattributed = _split_by_divisor_object(raw)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        entries = groups[tok]
        val = None
        if len(entries) == 1 and isinstance(entries[0], dict):
            v = entries[0].get("declared_total_components")
            if isinstance(v, int) and not isinstance(v, bool):
                val = v
        out[tok] = val
    return out


@fail_closed_pairmap
def verify_W1(cert):
    """W-1: component_bijection (裁定128 singular -> 2-entry array), cross-checked against W-5."""
    totals = _declared_totals_by_object(cert)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        result_pair = _check_singular_witness(
            {"component_bijection": cert.get("component_bijection")},
            "component_bijection",
            _validate_bijection_entry_factory(totals[tok]),
        )
        out[tok] = result_pair[tok]
    return out


@fail_closed_pairmap
def verify_W6(cert):
    """W-6: pushforward_compatibility_witness (裁定128 singular -> 2-entry array), cross-checked against W-5."""
    totals = _declared_totals_by_object(cert)
    out = {}
    for tok in DIVISOR_OBJECT_TOKENS:
        result_pair = _check_singular_witness(
            {"pushforward_compatibility_witness": cert.get("pushforward_compatibility_witness")},
            "pushforward_compatibility_witness",
            _validate_pushforward_entry_factory(totals[tok]),
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
