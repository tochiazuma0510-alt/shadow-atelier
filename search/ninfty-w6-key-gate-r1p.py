#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-w6-key-gate-r1p.py

RECEIVER ROUTE R1' -- the pointwise W-6 branch-key / point-map gate that
sits OUTSIDE the byte-frozen R1/R2 core (Sol 便97 W97-3.1, P97-3.2).

DRAFT, NOT ADOPTED. Sol P97-3.4 authorised "the versioned draft of the
schema and outer gates, independent prototypes of the two lane producers,
and the negative-example suite" and explicitly did NOT authorise declaring
W-6 closed on token agreement, substituting a weak W-6, or re-activating
EP. Nothing in this module may be read as W-6 closure: `W6_CLOSED` is
False and `overall` can never be PASS in v1 (the IMAGE-MU sub-gate --
"mu(r) = b recomputed exactly" -- is structurally UNKNOWN here, because it
needs the curve model, which is the producer's side).

WHY THIS MODULE EXISTS (W97-3.1, verbatim defect): `verify_W6_single` and
R2 dereference `map_ref` and add up `{branch_value, multiplicity}`, then
compare two dictionaries. They never use `ramification_ref` / `branch_ref`
/ `witness_ref` to compute the image r |-> mu(r), and never check that a
branch token was built from the key schema at all. So a producer can
self-declare arbitrary tokens and, if the two maps happen to agree, the
frozen core PASSes. The repair Sol prescribes is validation OUTSIDE the
comparison core -- this file, plus an INDEPENDENT second receiver route.

INDEPENDENCE (P97-3.2 item 6, "the two receiver routes must not share a
key/image implementation"): this module and search/ninfty-w6-key-gate-r2p.py
do not import each other and share no helper module. Their algorithms
differ on purpose:

    this module (R1')          | R2'
    ---------------------------+--------------------------------------
    root rank via DISCRIMINANT | root rank via STURM sequence + exact
    sign analysis              | rational-interval bisection
    irreducibility via         | irreducibility via the RATIONAL ROOT
    perfect-square test on D   | theorem (divisor enumeration)

The only thing they share is the mathematical schema in
docs/mb_ninfty_w6_branch_key_v1.md, which is what Sol permits ("the only
thing in common is the mathematical schema above").

FAIL-CLOSED STATUS ALGEBRA (P97-3.2, O-2/O-3 of the schema doc):
  schema / provenance defect              -> MALFORMED
  exact rank or image undecidable here    -> UNKNOWN   (never PASS)
  well-formed divisor disagreement        -> FAIL
No float fallback and no orbit-level key is ever accepted.
"""
from __future__ import annotations

import hashlib
import math
import os
import re
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

BRANCH_KEY_SCHEMA_ID = "mb/ninfty-w6-branch-key/v1"
POINT_MAP_SCHEMA_ID = "mb/ninfty-w6-point-map/v1"
IMAGE_WITNESS_SCHEMA_ID = "mb/ninfty-w6-image-witness/v1"
TARGET_COORDINATE_ID = "aqp1"
TARGET_MAP_ID = "mu"
DEFINITION_DOC = "docs/mb_ninfty_w6_branch_key_v1.md"
ROUTE_ID = "R1'"

# W-6 is OPEN. This constant exists so that any consumer, and the suite,
# can assert the claim mechanically rather than trusting prose.
W6_CLOSED = False

# G-1: ASCII decimal integers only -- no whitespace, no '+', no leading
# zeros, no '-0'. Written as explicit alternations rather than \d so that
# unicode digits cannot slip in.
_INT_RE = re.compile(r"^(0|-?[1-9][0-9]*)$")
_NAT_RE = re.compile(r"^(0|[1-9][0-9]*)$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


def _definition_digest():
    """The receiver recomputes the schema document's digest from its OWN
    copy (never trusts a digest supplied alongside the artifact)."""
    try:
        with open(os.path.join(REPO, *DEFINITION_DOC.split("/")), "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


# ---------------------------------------------------------------------------
# KEY -- token grammar, primitivity, irreducibility, rank range, rank
#        decidability. Every one of these is RECOMPUTED; nothing is taken
#        on the producer's word.
# ---------------------------------------------------------------------------

def _perfect_square(n):
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def _irreducible_over_Q(coeffs):
    """(verdict, reason). verdict True/False/None; None means 'this module
    cannot decide' -> UNKNOWN, never an assumed PASS.

    R1' method: degree 1 is trivially irreducible; degree 2 is irreducible
    over Q iff its discriminant is not a perfect square. Degree >= 3 is not
    decided here."""
    d = len(coeffs) - 1
    if d == 1:
        return True, "degree 1"
    if d == 2:
        a0, a1, a2 = coeffs
        disc = a1 * a1 - 4 * a0 * a2
        if _perfect_square(disc):
            return False, f"discriminant {disc} is a perfect square -> the quadratic splits over Q"
        return True, f"discriminant {disc} is not a perfect square"
    return None, f"degree {d}: irreducibility not decided by this route (v1 universe is degree <= 2)"


def _rank_of_root(coeffs, k):
    """(verdict, reason) for 'is k a rank this polynomial actually has, under
    the exact lexicographic order Re < Re, then Im < Im'.

    R1' method: discriminant sign analysis.
      D < 0 : conjugate pair, equal real parts -> rank 0 is the NEGATIVE
              imaginary part, rank 1 the positive one.
      D > 0 : two distinct reals -> rank 0 is the smaller one.
      D = 0 : a repeated root; excluded earlier by irreducibility.
    Degree >= 3 is UNKNOWN (no float fallback -- P97-3.2 O-3)."""
    d = len(coeffs) - 1
    if not (0 <= k < d):
        return False, f"rank {k} out of range for degree {d} (G-2 requires 0 <= k < d)"
    if d == 1:
        return True, "degree 1: the unique root has rank 0"
    if d == 2:
        a0, a1, a2 = coeffs
        disc = a1 * a1 - 4 * a0 * a2
        if disc < 0:
            return True, ("complex conjugate pair with equal real parts: rank 0 = negative imaginary "
                          "part, rank 1 = positive imaginary part")
        if disc > 0:
            return True, "two distinct real roots: rank 0 = the smaller one"
        return False, "discriminant 0: a repeated root cannot carry a well-defined rank"
    return None, f"degree {d}: exact root ordering not decided by this route"


def parse_token(token):
    """(ok, parsed_or_reason). Pure grammar + normalisation checks."""
    if not isinstance(token, str):
        return False, f"branch_value must be a string, got {type(token).__name__} (K-5)"
    if not token.isascii():
        return False, "branch_value is not pure ASCII (K-5)"
    if any(ch.isspace() for ch in token):
        return False, "branch_value contains whitespace (G-1)"
    if "+" in token:
        return False, "branch_value contains '+' (G-1)"
    parts = token.split("|")
    if len(parts) < 3:
        return False, f"branch_value has {len(parts)} '|'-separated fields, expected 3 or 5"
    if parts[0] != TARGET_COORDINATE_ID:
        return False, f"token prefix {parts[0]!r} != target_coordinate_id {TARGET_COORDINATE_ID!r} (G-4)"
    if parts[1] != TARGET_MAP_ID:
        return False, f"token map field {parts[1]!r} != {TARGET_MAP_ID!r} (G-4)"
    if parts[2] == "I":
        if len(parts) != 3:
            return False, "infinity token must be exactly 'aqp1|mu|I' (G-2)"
        return True, {"kind": "infinity", "token": token}
    if parts[2] != "F":
        return False, f"token kind {parts[2]!r} is neither 'I' nor 'F'"
    if len(parts) != 5:
        return False, f"finite token has {len(parts)} fields, expected 5 (G-2)"
    raw_coeffs = parts[3].split(",")
    if any(not _INT_RE.match(c) for c in raw_coeffs):
        return False, ("coefficient list violates G-1 (ASCII decimal, no '+', no leading zero, no '-0'): "
                       f"{parts[3]!r}")
    coeffs = [int(c) for c in raw_coeffs]
    d = len(coeffs) - 1
    if d < 1:
        return False, "finite token requires degree >= 1 (G-2)"
    if coeffs[-1] <= 0:
        return False, f"leading coefficient {coeffs[-1]} is not > 0 (K-2)"
    g = 0
    for c in coeffs:
        g = math.gcd(g, abs(c))
    if g != 1:
        return False, f"coefficient gcd is {g}, not 1 -- the token is not primitive (K-2)"
    if not _NAT_RE.match(parts[4]):
        return False, f"rank field {parts[4]!r} violates G-1"
    return True, {"kind": "finite", "token": token, "coeffs": coeffs,
                  "degree": d, "rank": int(parts[4])}


def validate_token(token):
    """(status, detail) with status in PASS / MALFORMED / UNKNOWN."""
    ok, parsed = parse_token(token)
    if not ok:
        return "MALFORMED", {"token": token, "reason": parsed}
    if parsed["kind"] == "infinity":
        return "PASS", {"token": token, "kind": "infinity"}
    irr, irr_reason = _irreducible_over_Q(parsed["coeffs"])
    rank_ok, rank_reason = _rank_of_root(parsed["coeffs"], parsed["rank"])
    detail = {"token": token, "kind": "finite", "degree": parsed["degree"],
              "coefficients_low_to_high": parsed["coeffs"], "rank": parsed["rank"],
              "irreducible": irr, "irreducibility_reason": irr_reason,
              "rank_admissible": rank_ok, "rank_reason": rank_reason,
              "route": ROUTE_ID, "method": "discriminant sign analysis / perfect-square test"}
    if irr is False or rank_ok is False:
        return "MALFORMED", detail
    if irr is None or rank_ok is None:
        return "UNKNOWN", detail
    return "PASS", detail


# ---------------------------------------------------------------------------
# IMAGE-KEY -- recompute the token from an EXACT image datum.
#
# The datum is an exact algebraic number in the v1-decidable class; there is
# no float form and none is accepted. This checks "the token really encodes
# THIS exact value". It does NOT check mu(r) = b -- that is IMAGE-MU, which
# needs the curve model and is UNKNOWN in v1.
# ---------------------------------------------------------------------------

def _frac(x):
    if isinstance(x, str) and re.match(r"^-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?$", x):
        return Fraction(x)
    if isinstance(x, int) and not isinstance(x, bool):
        return Fraction(x)
    return None


def _primitive_integer_form(rational_coeffs):
    """Clear denominators, divide by the content, force a positive leading
    coefficient. Returns the low-to-high integer coefficient list."""
    den = 1
    for c in rational_coeffs:
        den = den * c.denominator // math.gcd(den, c.denominator)
    ints = [int(c * den) for c in rational_coeffs]
    g = 0
    for c in ints:
        g = math.gcd(g, abs(c))
    if g:
        ints = [c // g for c in ints]
    if ints and ints[-1] < 0:
        ints = [-c for c in ints]
    return ints


def token_from_image_witness(datum):
    """(status, token_or_None, detail). status PASS / MALFORMED / UNKNOWN."""
    if not isinstance(datum, dict):
        return "MALFORMED", None, {"reason": "image datum is not an object"}
    kind = datum.get("kind")
    if kind == "infinity":
        return "PASS", f"{TARGET_COORDINATE_ID}|{TARGET_MAP_ID}|I", {"kind": kind}
    if kind == "rational":
        v = _frac(datum.get("value"))
        if v is None:
            return "MALFORMED", None, {"reason": f"rational datum has no exact value: {datum.get('value')!r}"}
        coeffs = _primitive_integer_form([-v, Fraction(1)])
        tok = "{0}|{1}|F|{2}|0".format(TARGET_COORDINATE_ID, TARGET_MAP_ID, ",".join(str(c) for c in coeffs))
        return "PASS", tok, {"kind": kind, "minimal_polynomial": coeffs, "rank": 0}
    if kind in ("quadratic_imaginary", "quadratic_real"):
        re_part = _frac(datum.get("real_part"))
        sq = _frac(datum.get("imag_sq") if kind == "quadratic_imaginary" else datum.get("radicand"))
        sign = datum.get("sign")
        if re_part is None or sq is None or sign not in (-1, 1):
            return "MALFORMED", None, {"reason": "quadratic datum needs exact real_part, a positive "
                                                 "imag_sq/radicand and sign in {-1,+1}"}
        if sq <= 0:
            return "MALFORMED", None, {"reason": "the radicand must be > 0"}
        if kind == "quadratic_imaginary":
            # z = re + sign*sqrt(sq)*i  ->  (T-re)^2 + sq
            const = re_part * re_part + sq
        else:
            # z = re + sign*sqrt(sq)    ->  (T-re)^2 - sq
            const = re_part * re_part - sq
        coeffs = _primitive_integer_form([const, -2 * re_part, Fraction(1)])
        irr, irr_reason = _irreducible_over_Q(coeffs)
        if irr is False:
            return "MALFORMED", None, {"reason": f"the datum's minimal polynomial is reducible: {irr_reason}"}
        if irr is None:
            return "UNKNOWN", None, {"reason": irr_reason}
        # K-3: imaginary case -> equal real parts, negative imaginary part
        # ranks 0. Real case -> the smaller real root ranks 0, and the
        # smaller root is the one with the MINUS sign.
        rank = 0 if sign < 0 else 1
        tok = "{0}|{1}|F|{2}|{3}".format(TARGET_COORDINATE_ID, TARGET_MAP_ID,
                                         ",".join(str(c) for c in coeffs), rank)
        return "PASS", tok, {"kind": kind, "minimal_polynomial": coeffs, "rank": rank}
    return "MALFORMED", None, {"reason": f"unknown image-datum kind {kind!r} -- v1 accepts only exact "
                                         "rational / quadratic data (no float form exists, O-3)"}


# ---------------------------------------------------------------------------
# The five gates.
# ---------------------------------------------------------------------------

def key_gate(records, frame):
    """KEY: token grammar/primitivity/irreducibility/rank plus the outer
    frame's schema ids and the definition digest (G-3)."""
    errors, per_record, statuses = [], {}, []
    mine = _definition_digest()
    claimed = (frame or {}).get("branch_key_definition_digest")
    frame_ok = True
    if (frame or {}).get("branch_key_schema_id") != BRANCH_KEY_SCHEMA_ID:
        frame_ok = False
        errors.append("frame: branch_key_schema_id is {0!r}, required {1!r} (G-3)".format(
            (frame or {}).get("branch_key_schema_id"), BRANCH_KEY_SCHEMA_ID))
    if (frame or {}).get("target_coordinate_id") != TARGET_COORDINATE_ID:
        frame_ok = False
        errors.append("frame: target_coordinate_id is {0!r}, required {1!r} -- and it must equal the "
                      "token prefix (G-3/G-4)".format((frame or {}).get("target_coordinate_id"),
                                                      TARGET_COORDINATE_ID))
    if not (_HEX64_RE.match(claimed or "") and mine is not None and claimed == mine):
        frame_ok = False
        errors.append("frame: branch_key_definition_digest {0!r} does not match the receiver's own "
                      "recomputation of {1} ({2!r}) -- a wrong/absent coordinate-definition digest is "
                      "MALFORMED, never 'probably the same schema'".format(claimed, DEFINITION_DOC, mine))
    for rec in records if isinstance(records, list) else []:
        rid = (rec or {}).get("ramification_point_id")
        st, detail = validate_token((rec or {}).get("branch_value"))
        per_record[str(rid)] = {"status": st, "detail": detail}
        statuses.append(st)
        if st != "PASS":
            errors.append(f"point {rid!r}: {detail.get('reason') or detail.get('rank_reason')}")
    if not isinstance(records, list) or not records:
        return "MALFORMED", {"status": "MALFORMED", "errors": ["the point map is absent or empty"],
                             "records": per_record}
    status = "MALFORMED" if (not frame_ok or "MALFORMED" in statuses) else (
        "UNKNOWN" if "UNKNOWN" in statuses else "PASS")
    return status, {"status": status, "frame_ok": frame_ok, "errors": errors, "records": per_record,
                    "receiver_definition_digest": mine}


def coverage_gate(records, declared_support):
    """COVERAGE: every ramification point of the declared support is covered
    exactly once -- no duplicate, no omission (P97-3.2 item 2)."""
    if not isinstance(records, list) or not isinstance(declared_support, list):
        return "MALFORMED", {"status": "MALFORMED", "reason": "records or declared support is not a list"}
    seen, dupes = {}, []
    for rec in records:
        rid = (rec or {}).get("ramification_point_id")
        if not isinstance(rid, str) or not rid:
            return "MALFORMED", {"status": "MALFORMED",
                                 "reason": "a record carries no ramification_point_id (P97-3.2 schema)"}
        seen[rid] = seen.get(rid, 0) + 1
        if seen[rid] == 2:
            dupes.append(rid)
    missing = sorted(set(declared_support) - set(seen))
    extra = sorted(set(seen) - set(declared_support))
    ok = not dupes and not missing and not extra
    return ("PASS" if ok else "MALFORMED"), {
        "status": "PASS" if ok else "MALFORMED",
        "covered_once": sorted(k for k, v in seen.items() if v == 1),
        "duplicated": sorted(dupes), "missing": missing, "not_in_declared_support": extra,
        "note": ("a duplicated or omitted ramification point is a provenance defect, not a mathematical "
                 "FAIL (O-2)"),
    }


def image_gate(records):
    """IMAGE. Two sub-gates:
      IMAGE-KEY: the token is recomputed from the record's own exact image
                 datum and must agree byte-for-byte.
      IMAGE-MU : mu(r) = b recomputed exactly from the curve model.
                 STRUCTURALLY UNKNOWN in v1 -- this route has no curve
                 model, so it reports UNKNOWN and never PASS. This is the
                 remaining hole in W-6 and is reported as such.
    Also type-checks multiplicity (P97-3.2 item 3)."""
    per_record, statuses, errors = {}, [], []
    for rec in records if isinstance(records, list) else []:
        rid = str((rec or {}).get("ramification_point_id"))
        witness = (rec or {}).get("exact_image_witness") or {}
        entry = {"IMAGE-MU": "UNKNOWN"}
        mult = (rec or {}).get("multiplicity")
        if not isinstance(mult, int) or isinstance(mult, bool) or mult < 1:
            entry["multiplicity_type"] = "MALFORMED"
            errors.append(f"point {rid}: multiplicity {mult!r} is not a positive integer")
            statuses.append("MALFORMED")
        else:
            entry["multiplicity_type"] = "PASS"
        if witness.get("schema_id") != IMAGE_WITNESS_SCHEMA_ID:
            entry["IMAGE-KEY"] = "MALFORMED"
            errors.append(f"point {rid}: exact_image_witness.schema_id is {witness.get('schema_id')!r}, "
                          f"required {IMAGE_WITNESS_SCHEMA_ID!r}")
            statuses.append("MALFORMED")
        else:
            st, tok, detail = token_from_image_witness(witness.get("datum"))
            entry["IMAGE-KEY"] = st if st != "PASS" else (
                "PASS" if tok == (rec or {}).get("branch_value") else "FAIL")
            entry["recomputed_token"] = tok
            entry["recomputation_detail"] = detail
            if entry["IMAGE-KEY"] == "FAIL":
                errors.append(f"point {rid}: the declared branch_value {(rec or {}).get('branch_value')!r} "
                              f"is not what the point's own exact image datum encodes ({tok!r})")
            if entry["IMAGE-KEY"] != "PASS":
                statuses.append("MALFORMED" if entry["IMAGE-KEY"] == "MALFORMED" else entry["IMAGE-KEY"])
        per_record[rid] = entry
        statuses.append("UNKNOWN")          # IMAGE-MU, always
    status = ("MALFORMED" if "MALFORMED" in statuses else
              "FAIL" if "FAIL" in statuses else
              "UNKNOWN" if "UNKNOWN" in statuses else "PASS")
    return status, {"status": status, "records": per_record, "errors": errors,
                    "image_mu_note": ("IMAGE-MU (mu(r) = b recomputed exactly from the curve model) is "
                                      "NOT implemented in v1: this receiver route holds no curve model, "
                                      "so it reports UNKNOWN rather than passing the point through. This "
                                      "is the remaining W-6 hole -- see docs/mb_ninfty_w6_branch_key_v1.md "
                                      "section 5.")}


def aggregate_pushforward(records):
    """AGGREGATE: the RECEIVER re-sums the per-point multiplicities into a
    branch divisor. The producer's own aggregate is never used (W6-C4)."""
    out = {}
    for rec in records if isinstance(records, list) else []:
        tok = (rec or {}).get("branch_value")
        mult = (rec or {}).get("multiplicity")
        if not isinstance(tok, str) or not isinstance(mult, int) or isinstance(mult, bool):
            return None
        out[tok] = out.get(tok, 0) + mult
    return out


def aggregate_gate(records, lane_b_branch_map):
    """Compare the receiver-recomputed pushforward with lane B's independent
    branch divisor map. ONLY a well-formed disagreement is a W-6 FAIL."""
    mine = aggregate_pushforward(records)
    if mine is None:
        return "MALFORMED", {"status": "MALFORMED", "reason": "a record has no usable token/multiplicity"}
    if not isinstance(lane_b_branch_map, dict) or not lane_b_branch_map:
        return "ABSENT", {"status": "ABSENT", "reason": "no independent lane-B branch divisor was supplied "
                                                        "-- absence is never agreement"}
    for tok in lane_b_branch_map:
        st, _ = validate_token(tok)
        if st == "MALFORMED":
            return "MALFORMED", {"status": "MALFORMED",
                                 "reason": f"lane B branch key {tok!r} is not a valid v1 token"}
    ok = mine == lane_b_branch_map
    return ("PASS" if ok else "FAIL"), {
        "status": "PASS" if ok else "FAIL",
        "receiver_recomputed_pushforward": mine,
        "lane_b_branch_divisor": lane_b_branch_map,
        "note": ("a well-formed divisor disagreement is the ONLY thing reported as a W-6 FAIL (O-2); "
                 "schema defects are MALFORMED and undecidable data is UNKNOWN"),
    }


def independence_gate(source_texts):
    """INDEPENDENCE (P97-3.2 item 5): the two producers and the two receiver
    routes must not read one another's outputs or share a canonicaliser.
    `source_texts` maps a label to that component's source text; the check is
    over the shipped source, not over a declaration."""
    findings = []
    lane_a = source_texts.get("lane_a", "")
    lane_b = source_texts.get("lane_b", "")
    r1p = source_texts.get("receiver_r1p", "")
    r2p = source_texts.get("receiver_r2p", "")
    if "srepr" in lane_a:
        findings.append("lane A source mentions sympy srepr -- lane A must derive its key from its own "
                        "curve/ideal data, never by mimicking lane B's representation (H-1/H-3)")
    for label, text, forbidden in (("lane_a", lane_a, "ninfty-nf-laneb"),
                                   ("lane_b", lane_b, "ninfty-nf-lanea"),
                                   ("receiver_r1p", r1p, "ninfty-w6-key-gate-r2p"),
                                   ("receiver_r2p", r2p, "ninfty-w6-key-gate-r1p")):
        if forbidden in text:
            findings.append(f"{label} loads {forbidden} -- the two sides must not share an implementation "
                            "(P97-3.2 item 5 / H-4')")
    return ("PASS" if not findings else "FAIL"), {"status": "PASS" if not findings else "FAIL",
                                                  "findings": findings}


def run_receiver_route(records, frame, declared_support, lane_b_branch_map, source_texts=None):
    """The whole outer gate, fail-closed. `overall` is PASS only if every
    sub-gate is PASS -- which cannot happen in v1, because IMAGE-MU is
    structurally UNKNOWN. That is the honest report, not a defect to be
    papered over."""
    gates = {}
    gates["KEY"], key_detail = key_gate(records, frame)
    gates["COVERAGE"], cov_detail = coverage_gate(records, declared_support)
    gates["IMAGE"], img_detail = image_gate(records)
    gates["AGGREGATE"], agg_detail = aggregate_gate(records, lane_b_branch_map)
    gates["INDEPENDENCE"], ind_detail = independence_gate(source_texts or {})
    order = ("MALFORMED", "FAIL", "ABSENT", "UNKNOWN")
    overall = next((s for s in order if s in gates.values()), "PASS")
    return {
        "schema_id": BRANCH_KEY_SCHEMA_ID,
        "point_map_schema_id": POINT_MAP_SCHEMA_ID,
        "route": ROUTE_ID,
        "gates": gates,
        "details": {"KEY": key_detail, "COVERAGE": cov_detail, "IMAGE": img_detail,
                    "AGGREGATE": agg_detail, "INDEPENDENCE": ind_detail},
        "overall": overall,
        "w6_closed": W6_CLOSED,
        "final_comparison_reached": overall == "PASS",
        "note": ("the frozen R1/R2 dictionary equality may be used as the FINAL W-6 comparison only "
                 "AFTER every gate above is PASS (P97-3.2 item 6). In v1 that is unreachable, so this "
                 "report is never W-6 closure and never EP activation (P97-3.4)."),
    }
