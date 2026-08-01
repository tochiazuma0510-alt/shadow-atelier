#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-w6-key-gate-r2p.py

RECEIVER ROUTE R2' -- the SECOND, INDEPENDENT pointwise W-6 branch-key /
point-map gate outside the byte-frozen R1/R2 core (Sol 便97 P97-3.2 item 6:
"the two receiver routes must not share a key/image implementation").

DRAFT, NOT ADOPTED -- same standing as R1': W-6 stays OPEN, `W6_CLOSED` is
False, and `overall` cannot be PASS in v1.

INDEPENDENCE FROM R1' IS ALGORITHMIC, NOT COSMETIC. This route decides the
two hard predicates by different mathematics:

  * root rank: STURM SEQUENCES over Q plus exact rational-interval
    counting (R1' uses discriminant sign analysis).
  * irreducibility over Q: the RATIONAL ROOT THEOREM, by enumerating the
    divisors of the constant and leading coefficients (R1' uses a
    perfect-square test on the discriminant).
  * token parsing: a hand-rolled character scan (R1' uses regular
    expressions).

This module does not import R1', shares no helper module with it, and
reads only the mathematical schema document -- which is exactly what Sol
permits to be common ("the only thing in common is the mathematical
schema").

ERA (governing spec sec.5.3.4 / dependency manifest Y-3c): this file belongs
to the plane `w6_key_route`, era ERA_W6KEY. The plane was declared first and
adopted by the commander freeze receipt for the v20/v15/v15 trio (Sol 便99
F99-5.2). Adoption changes nothing about W-6: it is still OPEN.
  [ep-era-declaration] plane=w6_key_route predicate_spec_id=mb/ninfty-stage2-predicate/v20 verifier_contract_id=mb/ninfty-verifier-contract/v15 dependency_manifest_schema_id=mb/dependency-manifest/v15

Status algebra is the same fail-closed one: schema/provenance defect ->
MALFORMED, undecidable -> UNKNOWN, well-formed divisor disagreement ->
FAIL, and never a float fallback or an orbit-level key.
"""
from __future__ import annotations

import hashlib
import os
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)

BRANCH_KEY_SCHEMA_ID = "mb/ninfty-w6-branch-key/v1"
POINT_MAP_SCHEMA_ID = "mb/ninfty-w6-point-map/v1"
IMAGE_WITNESS_SCHEMA_ID = "mb/ninfty-w6-image-witness/v1"
TARGET_COORDINATE_ID = "aqp1"
TARGET_MAP_ID = "mu"
DEFINITION_DOC = "docs/mb_ninfty_w6_branch_key_v1.md"
ROUTE_ID = "R2'"

W6_CLOSED = False

_DIGITS = "0123456789"
_HEXDIGITS = "0123456789abcdef"


# ---------------------------------------------------------------------------
# character-scan integer parsing (G-1: ASCII decimal, no '+', no leading
# zero, no '-0', no whitespace). Deliberately not a regular expression.
# ---------------------------------------------------------------------------

def _scan_int(text, allow_negative=True):
    if not isinstance(text, str) or text == "":
        return None
    body, negative = text, False
    if body[0] == "-":
        if not allow_negative:
            return None
        negative, body = True, body[1:]
    if body == "" or any(ch not in _DIGITS for ch in body):
        return None
    if len(body) > 1 and body[0] == "0":
        return None
    value = 0
    for ch in body:
        value = value * 10 + (ord(ch) - 48)
    if negative and value == 0:
        return None
    return -value if negative else value


def _is_hex64(text):
    return (isinstance(text, str) and len(text) == 64
            and all(ch in _HEXDIGITS for ch in text.lower()) and text == text.lower())


def _definition_digest():
    try:
        with open(os.path.join(_REPO, *DEFINITION_DOC.split("/")), "rb") as handle:
            return hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        return None


# ---------------------------------------------------------------------------
# exact polynomial arithmetic over Q, low-to-high coefficient lists
# ---------------------------------------------------------------------------

def _trim(poly):
    out = list(poly)
    while out and out[-1] == 0:
        out.pop()
    return out


def _deriv(poly):
    return _trim([poly[i] * i for i in range(1, len(poly))])


def _divmod_poly(num, den):
    num, den = _trim(num), _trim(den)
    quo = [Fraction(0)] * max(0, len(num) - len(den) + 1)
    rem = list(num)
    while _trim(rem) and len(_trim(rem)) >= len(den):
        rem = _trim(rem)
        shift = len(rem) - len(den)
        factor = Fraction(rem[-1], 1) / den[-1]
        quo[shift] = factor
        for i, coefficient in enumerate(den):
            rem[shift + i] -= factor * coefficient
        rem = _trim(rem)
    return quo, _trim(rem)


def _neg(poly):
    return [-c for c in poly]


def _sturm_chain(poly):
    """p0 = p, p1 = p', p_{i+1} = -rem(p_{i-1}, p_i)."""
    chain = [_trim(poly), _deriv(poly)]
    while len(chain[-1]) > 1:
        _, rem = _divmod_poly(chain[-2], chain[-1])
        if not rem:
            break
        chain.append(_neg(rem))
    return [p for p in chain if p]


def _eval(poly, x):
    total = Fraction(0)
    for coefficient in reversed(poly):
        total = total * x + coefficient
    return total


def _sign_variations_at(chain, x):
    signs = []
    for poly in chain:
        value = _eval(poly, x)
        if value != 0:
            signs.append(1 if value > 0 else -1)
    return sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])


def _sign_variations_at_infinity(chain, at_plus):
    signs = []
    for poly in chain:
        lead = poly[-1]
        degree = len(poly) - 1
        sign = 1 if lead > 0 else -1
        if not at_plus and degree % 2 == 1:
            sign = -sign
        signs.append(sign)
    return sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])


def _real_roots_total(poly):
    chain = _sturm_chain(poly)
    return _sign_variations_at_infinity(chain, False) - _sign_variations_at_infinity(chain, True)


def _real_roots_below(poly, bound):
    """Number of real roots strictly less than the rational `bound`."""
    chain = _sturm_chain(poly)
    below = _sign_variations_at_infinity(chain, False) - _sign_variations_at(chain, bound)
    return below


# ---------------------------------------------------------------------------
# irreducibility by the rational root theorem
# ---------------------------------------------------------------------------

def _divisors(n):
    n = abs(n)
    if n == 0:
        return []
    out, i = [], 1
    while i * i <= n:
        if n % i == 0:
            out.append(i)
            out.append(n // i)
        i += 1
    return sorted(set(out))


def _irreducible_over_Q(coeffs):
    """(verdict, reason); None = this route does not decide -> UNKNOWN."""
    degree = len(coeffs) - 1
    if degree == 1:
        return True, "degree 1"
    if degree in (2, 3):
        if coeffs[0] == 0:
            return False, "T divides the polynomial (constant term 0) -> reducible over Q"
        for p in _divisors(coeffs[0]):
            for q in _divisors(coeffs[-1]):
                for candidate in (Fraction(p, q), Fraction(-p, q)):
                    if _eval([Fraction(c) for c in coeffs], candidate) == 0:
                        return False, f"rational root {candidate} found -> reducible over Q"
        return True, ("no rational root among the divisor candidates; for degree 2 or 3 that is "
                      "equivalent to irreducibility over Q")
    return None, f"degree {degree}: irreducibility not decided by this route (v1 universe is degree <= 2)"


def _rank_admissible(coeffs, rank):
    """(verdict, reason) via Sturm-counted real roots."""
    degree = len(coeffs) - 1
    if not (0 <= rank < degree):
        return False, f"rank {rank} out of range for degree {degree} (G-2)"
    if degree == 1:
        return True, "degree 1: the unique root has rank 0"
    if degree == 2:
        rational = [Fraction(c) for c in coeffs]
        real_count = _real_roots_total(rational)
        if real_count == 0:
            return True, ("Sturm: 0 real roots -> a conjugate pair with equal real parts, ordered by "
                          "imaginary part (K-3)")
        if real_count == 2:
            return True, "Sturm: 2 distinct real roots, ordered by value (K-3)"
        return False, f"Sturm: {real_count} real root(s) -- a repeated root carries no well-defined rank"
    return None, f"degree {degree}: exact complex ordering not decided by this route"


# ---------------------------------------------------------------------------
# KEY
# ---------------------------------------------------------------------------

def parse_token(token):
    if not isinstance(token, str):
        return False, "branch_value is not a string (K-5)"
    for ch in token:
        if ord(ch) > 127:
            return False, "branch_value is not pure ASCII (K-5)"
        if ch in " \t\n\r\f\v":
            return False, "branch_value contains whitespace (G-1)"
        if ch == "+":
            return False, "branch_value contains '+' (G-1)"
    fields = token.split("|")
    if len(fields) < 3 or fields[0] != TARGET_COORDINATE_ID or fields[1] != TARGET_MAP_ID:
        return False, f"token prefix is not {TARGET_COORDINATE_ID}|{TARGET_MAP_ID} (G-4): {token!r}"
    if fields[2] == "I":
        if len(fields) != 3:
            return False, "infinity token must be exactly aqp1|mu|I (G-2)"
        return True, {"kind": "infinity", "token": token}
    if fields[2] != "F" or len(fields) != 5:
        return False, f"token is neither the infinity nor the finite shape (G-2): {token!r}"
    coeffs = []
    for chunk in fields[3].split(","):
        value = _scan_int(chunk)
        if value is None:
            return False, f"coefficient {chunk!r} violates G-1"
        coeffs.append(value)
    if len(coeffs) - 1 < 1:
        return False, "finite token requires degree >= 1 (G-2)"
    if coeffs[-1] <= 0:
        return False, f"leading coefficient {coeffs[-1]} is not > 0 (K-2)"
    content = 0
    for value in coeffs:
        a, b = content, abs(value)
        while b:
            a, b = b, a % b
        content = a
    if content != 1:
        return False, f"coefficient content is {content}, not 1 -- not primitive (K-2)"
    rank = _scan_int(fields[4], allow_negative=False)
    if rank is None:
        return False, f"rank field {fields[4]!r} violates G-1"
    return True, {"kind": "finite", "token": token, "coeffs": coeffs,
                  "degree": len(coeffs) - 1, "rank": rank}


def validate_token(token):
    ok, parsed = parse_token(token)
    if not ok:
        return "MALFORMED", {"token": token, "reason": parsed}
    if parsed["kind"] == "infinity":
        return "PASS", {"token": token, "kind": "infinity"}
    irreducible, irr_reason = _irreducible_over_Q(parsed["coeffs"])
    rank_ok, rank_reason = _rank_admissible(parsed["coeffs"], parsed["rank"])
    detail = {"token": token, "kind": "finite", "degree": parsed["degree"],
              "coefficients_low_to_high": parsed["coeffs"], "rank": parsed["rank"],
              "irreducible": irreducible, "irreducibility_reason": irr_reason,
              "rank_admissible": rank_ok, "rank_reason": rank_reason,
              "route": ROUTE_ID, "method": "Sturm sequence / rational root theorem"}
    if irreducible is False or rank_ok is False:
        return "MALFORMED", detail
    if irreducible is None or rank_ok is None:
        return "UNKNOWN", detail
    return "PASS", detail


# ---------------------------------------------------------------------------
# IMAGE-KEY: recompute the token from the exact image datum, by polynomial
# construction and Sturm-counted rank (never by the closed-form rules R1'
# uses).
# ---------------------------------------------------------------------------

def _exact_rational(value):
    if isinstance(value, int) and not isinstance(value, bool):
        return Fraction(value)
    if not isinstance(value, str) or value == "":
        return None
    numerator, _, denominator = value.partition("/")
    n = _scan_int(numerator)
    if n is None:
        return None
    if denominator == "":
        return Fraction(n)
    d = _scan_int(denominator, allow_negative=False)
    if d is None or d == 0:
        return None
    return Fraction(n, d)


def _primitive(rational_coeffs):
    denominator = 1
    for c in rational_coeffs:
        d = c.denominator
        a, b = denominator, d
        while b:
            a, b = b, a % b
        denominator = denominator * d // a
    ints = [int(c * denominator) for c in rational_coeffs]
    content = 0
    for value in ints:
        a, b = content, abs(value)
        while b:
            a, b = b, a % b
        content = a
    if content:
        ints = [v // content for v in ints]
    if ints and ints[-1] < 0:
        ints = [-v for v in ints]
    return ints


def token_from_image_witness(datum):
    if not isinstance(datum, dict):
        return "MALFORMED", None, {"reason": "image datum is not an object"}
    kind = datum.get("kind")
    if kind == "infinity":
        return "PASS", TARGET_COORDINATE_ID + "|" + TARGET_MAP_ID + "|I", {"kind": kind}
    if kind == "rational":
        value = _exact_rational(datum.get("value"))
        if value is None:
            return "MALFORMED", None, {"reason": "rational datum carries no exact value"}
        coeffs = _primitive([-value, Fraction(1)])
        token = "%s|%s|F|%s|0" % (TARGET_COORDINATE_ID, TARGET_MAP_ID,
                                  ",".join(str(c) for c in coeffs))
        return "PASS", token, {"kind": kind, "minimal_polynomial": coeffs, "rank": 0}
    if kind in ("quadratic_imaginary", "quadratic_real"):
        centre = _exact_rational(datum.get("real_part"))
        radicand = _exact_rational(datum.get("imag_sq") if kind == "quadratic_imaginary"
                                   else datum.get("radicand"))
        sign = datum.get("sign")
        if centre is None or radicand is None or sign not in (-1, 1) or radicand <= 0:
            return "MALFORMED", None, {"reason": "quadratic datum needs exact real_part, a positive "
                                                 "radicand and sign in {-1,+1}"}
        # (T - centre)^2 built by polynomial multiplication, then +/- radicand
        base = [centre * centre, -2 * centre, Fraction(1)]
        base[0] = base[0] + (radicand if kind == "quadratic_imaginary" else -radicand)
        coeffs = _primitive(base)
        irreducible, reason = _irreducible_over_Q(coeffs)
        if irreducible is False:
            return "MALFORMED", None, {"reason": "minimal polynomial is reducible: " + reason}
        if irreducible is None:
            return "UNKNOWN", None, {"reason": reason}
        rational = [Fraction(c) for c in coeffs]
        if kind == "quadratic_imaginary":
            if _real_roots_total(rational) != 0:
                return "MALFORMED", None, {"reason": "Sturm says the polynomial has real roots, so the "
                                                     "datum cannot be a non-real conjugate root"}
            rank = 0 if sign < 0 else 1
            how = "Sturm: no real roots -> conjugate pair; rank by the sign of the imaginary part (K-3)"
        else:
            below_centre = _real_roots_below(rational, centre)
            rank = below_centre - (1 if sign < 0 else 0)
            how = ("Sturm: %d real root(s) below the rational centre; rank = that count, minus one for "
                   "the minus branch (K-3)" % below_centre)
        if not 0 <= rank < len(coeffs) - 1:
            return "MALFORMED", None, {"reason": "the recomputed rank %r is out of range" % rank}
        token = "%s|%s|F|%s|%d" % (TARGET_COORDINATE_ID, TARGET_MAP_ID,
                                   ",".join(str(c) for c in coeffs), rank)
        return "PASS", token, {"kind": kind, "minimal_polynomial": coeffs, "rank": rank, "method": how}
    return "MALFORMED", None, {"reason": "unknown image-datum kind %r -- v1 accepts only exact rational "
                                         "or quadratic data (O-3 forbids a float form)" % (kind,)}


# ---------------------------------------------------------------------------
# gates
# ---------------------------------------------------------------------------

def key_gate(records, frame):
    errors, per_record, statuses = [], {}, []
    mine = _definition_digest()
    frame = frame or {}
    frame_ok = True
    if frame.get("branch_key_schema_id") != BRANCH_KEY_SCHEMA_ID:
        frame_ok = False
        errors.append("frame: branch_key_schema_id %r != %r (G-3)"
                      % (frame.get("branch_key_schema_id"), BRANCH_KEY_SCHEMA_ID))
    if frame.get("target_coordinate_id") != TARGET_COORDINATE_ID:
        frame_ok = False
        errors.append("frame: target_coordinate_id %r != %r, and it must equal the token prefix (G-3/G-4)"
                      % (frame.get("target_coordinate_id"), TARGET_COORDINATE_ID))
    claimed = frame.get("branch_key_definition_digest")
    if not (_is_hex64(claimed) and mine is not None and claimed == mine):
        frame_ok = False
        errors.append("frame: branch_key_definition_digest %r does not match the receiver's own "
                      "recomputation of %s (%r)" % (claimed, DEFINITION_DOC, mine))
    if not isinstance(records, list) or not records:
        return "MALFORMED", {"status": "MALFORMED", "errors": ["the point map is absent or empty"]}
    for record in records:
        record = record or {}
        status, detail = validate_token(record.get("branch_value"))
        per_record[str(record.get("ramification_point_id"))] = {"status": status, "detail": detail}
        statuses.append(status)
        if status != "PASS":
            errors.append("point %r: %s" % (record.get("ramification_point_id"),
                                            detail.get("reason") or detail.get("rank_reason")))
    status = "MALFORMED" if (not frame_ok or "MALFORMED" in statuses) else (
        "UNKNOWN" if "UNKNOWN" in statuses else "PASS")
    return status, {"status": status, "frame_ok": frame_ok, "errors": errors, "records": per_record,
                    "receiver_definition_digest": mine}


def coverage_gate(records, declared_support):
    if not isinstance(records, list) or not isinstance(declared_support, list):
        return "MALFORMED", {"status": "MALFORMED", "reason": "records or declared support is not a list"}
    counts = {}
    for record in records:
        point_id = (record or {}).get("ramification_point_id")
        if not isinstance(point_id, str) or point_id == "":
            return "MALFORMED", {"status": "MALFORMED", "reason": "a record carries no "
                                                                  "ramification_point_id"}
        counts[point_id] = counts.get(point_id, 0) + 1
    duplicated = sorted(k for k, v in counts.items() if v > 1)
    missing = sorted(p for p in set(declared_support) if p not in counts)
    unexpected = sorted(p for p in counts if p not in set(declared_support))
    ok = not duplicated and not missing and not unexpected
    return ("PASS" if ok else "MALFORMED"), {"status": "PASS" if ok else "MALFORMED",
                                             "duplicated": duplicated, "missing": missing,
                                             "not_in_declared_support": unexpected}


def image_gate(records):
    per_record, statuses, errors = {}, [], []
    for record in records if isinstance(records, list) else []:
        record = record or {}
        point_id = str(record.get("ramification_point_id"))
        entry = {"IMAGE-MU": "UNKNOWN"}
        multiplicity = record.get("multiplicity")
        if not isinstance(multiplicity, int) or isinstance(multiplicity, bool) or multiplicity < 1:
            entry["multiplicity_type"] = "MALFORMED"
            statuses.append("MALFORMED")
            errors.append("point %s: multiplicity %r is not a positive integer" % (point_id, multiplicity))
        else:
            entry["multiplicity_type"] = "PASS"
        witness = record.get("exact_image_witness") or {}
        if witness.get("schema_id") != IMAGE_WITNESS_SCHEMA_ID:
            entry["IMAGE-KEY"] = "MALFORMED"
            statuses.append("MALFORMED")
            errors.append("point %s: exact_image_witness.schema_id %r != %r"
                          % (point_id, witness.get("schema_id"), IMAGE_WITNESS_SCHEMA_ID))
        else:
            status, token, detail = token_from_image_witness(witness.get("datum"))
            if status != "PASS":
                entry["IMAGE-KEY"] = status
                statuses.append(status)
            elif token != record.get("branch_value"):
                entry["IMAGE-KEY"] = "FAIL"
                statuses.append("FAIL")
                errors.append("point %s: declared %r, the exact image datum encodes %r"
                              % (point_id, record.get("branch_value"), token))
            else:
                entry["IMAGE-KEY"] = "PASS"
            entry["recomputed_token"] = token
            entry["recomputation_detail"] = detail
        statuses.append("UNKNOWN")          # IMAGE-MU, always, in v1
        per_record[point_id] = entry
    status = ("MALFORMED" if "MALFORMED" in statuses else
              "FAIL" if "FAIL" in statuses else
              "UNKNOWN" if "UNKNOWN" in statuses else "PASS")
    return status, {"status": status, "records": per_record, "errors": errors,
                    "image_mu_note": "IMAGE-MU is not implemented in v1 (no curve model on the receiver "
                                     "side); it reports UNKNOWN, never PASS."}


def aggregate_pushforward(records):
    out = {}
    for record in records if isinstance(records, list) else []:
        record = record or {}
        token, multiplicity = record.get("branch_value"), record.get("multiplicity")
        if not isinstance(token, str) or not isinstance(multiplicity, int) or isinstance(multiplicity, bool):
            return None
        out[token] = out.get(token, 0) + multiplicity
    return out


def aggregate_gate(records, lane_b_branch_map):
    mine = aggregate_pushforward(records)
    if mine is None:
        return "MALFORMED", {"status": "MALFORMED", "reason": "a record has no usable token/multiplicity"}
    if not isinstance(lane_b_branch_map, dict) or not lane_b_branch_map:
        return "ABSENT", {"status": "ABSENT", "reason": "no independent lane-B branch divisor supplied"}
    for token in lane_b_branch_map:
        if validate_token(token)[0] == "MALFORMED":
            return "MALFORMED", {"status": "MALFORMED",
                                 "reason": "lane B branch key %r is not a valid v1 token" % (token,)}
    ok = mine == lane_b_branch_map
    return ("PASS" if ok else "FAIL"), {"status": "PASS" if ok else "FAIL",
                                        "receiver_recomputed_pushforward": mine,
                                        "lane_b_branch_divisor": lane_b_branch_map}


def independence_gate(source_texts):
    findings = []
    source_texts = source_texts or {}
    # 【chg 便99 F99-5.1】additive rows: the lane B per-point producer is an
    # independent producer, not a port of lane A's, so neither producer may
    # pull in the other's module, canonicaliser or token helpers.
    for label, forbidden in (("lane_a", "ninfty-nf-laneb"), ("lane_b", "ninfty-nf-lanea"),
                             ("lane_a", "ninfty-w6-pointmap-laneb"),
                             ("lane_b", "ninfty-w6-pointmap-lanea"),
                             ("lane_b", "ninfty-searcher-v2"),
                             ("lane_b", "ninfty-native-a-cli"),
                             ("receiver_r1p", "ninfty-w6-key-gate-r2p"),
                             ("receiver_r2p", "ninfty-w6-key-gate-r1p")):
        if forbidden in (source_texts.get(label) or ""):
            findings.append("%s reads %s -- forbidden shared implementation (P97-3.2 item 5)"
                            % (label, forbidden))
    if "srepr" in (source_texts.get("lane_a") or ""):
        findings.append("lane A mentions sympy srepr -- it must derive its own key, not mimic lane B (H-1)")
    return ("PASS" if not findings else "FAIL"), {"status": "PASS" if not findings else "FAIL",
                                                  "findings": findings}


def run_receiver_route(records, frame, declared_support, lane_b_branch_map, source_texts=None):
    gates = {}
    gates["KEY"], key_detail = key_gate(records, frame)
    gates["COVERAGE"], coverage_detail = coverage_gate(records, declared_support)
    gates["IMAGE"], image_detail = image_gate(records)
    gates["AGGREGATE"], aggregate_detail = aggregate_gate(records, lane_b_branch_map)
    gates["INDEPENDENCE"], independence_detail = independence_gate(source_texts)
    for candidate in ("MALFORMED", "FAIL", "ABSENT", "UNKNOWN"):
        if candidate in gates.values():
            overall = candidate
            break
    else:
        overall = "PASS"
    return {"schema_id": BRANCH_KEY_SCHEMA_ID, "point_map_schema_id": POINT_MAP_SCHEMA_ID,
            "route": ROUTE_ID, "gates": gates,
            "details": {"KEY": key_detail, "COVERAGE": coverage_detail, "IMAGE": image_detail,
                        "AGGREGATE": aggregate_detail, "INDEPENDENCE": independence_detail},
            "overall": overall, "w6_closed": W6_CLOSED,
            "final_comparison_reached": overall == "PASS",
            "note": "the frozen dictionary equality may serve as the final W-6 comparison only after "
                    "every gate is PASS (P97-3.2 item 6); unreachable in v1."}
