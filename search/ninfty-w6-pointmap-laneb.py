#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-w6-pointmap-laneb.py

LANE B per-point W-6 point-map PRODUCER.

AUTHORISATION: Sol 便99 §5 F99-5.1 (実装認可), commander 裁定412, effective
from the freeze receipt
`mb/ninfty-stage2-freeze-receipt/sol99/92025385-8f26416b-72623050`
(provenance/ninfty_freeze_receipt_sol99.md).

WHAT F99-5.1 AUTHORISES, VERBATIM: not an isomorphic port of the lane A
producer, but an INDEPENDENT lane B producer satisfying the same output
contract. Accordingly:

  * the exact witness of every rational root is constructed from LANE B's
    OWN curve/native data. Lane B's derivation is genuinely different from
    lane A's: lane A evaluates mu = a(x0) + p(x0)y and squares to get
    (b - a(x0))^2 = p(x0)^2 f6(x0); lane B locates the fibres of the
    branch values s, -s with s^2 = -C directly from lemma N-inf-pair
    (spec sec.1.5) through its own point-level construction, and reads the
    branch value off the point rather than reconstructing it from a square.
  * this module imports NO lane A producer, canonicaliser, branch-token
    helper or output token. Its only project dependencies are lane B's own
    two modules (the checker's decision chain and the checker's from-scratch
    point construction), both loaded by path below. What IS shared with lane
    A is the normative schema `mb/ninfty-w6-branch-key/v1` and its literals
    (token grammar, K-2 primitive form, K-3 rank order, the point-id
    grammar) -- Sol permits the schema and its literals, and forbids the
    producer code path and the derivation.
  * finite points keep BOTH the x-root and the y-root rank; the two points
    at infinity keep their own branch; the whole degree-12 accounting is
    RECONSTRUCTED from the per-point records (2g-2+2deg(mu), with g and
    deg(mu) themselves derived here from the curve, not typed in) and is a
    fail-closed assert: a map that does not add up is UNKNOWN, never a
    partial map presented as complete.

WHAT IT DOES NOT DO (便99 F99-5.1 last paragraph, verbatim): even a complete
lane B closes only the AGGREGATE plane. IMAGE-MU stays UNKNOWN, so W-6 is
OPEN and EP stays `uncalibrated / UNKNOWN`. `W6_CLOSED` is False here and
every output is stamped `artifact_class: "diagnostic_construction"` --
buildable pre-gate, and NOT a minted/published artifact (便95 F95-2.3).

NO SELF-DECLARED AGGREGATE (W6-C4): this producer ships per-point records
only. Summing them into a branch divisor is the RECEIVER's job on both
sides; a producer-declared divisor would reintroduce exactly the defect
W97-3.1 named.

ERA (spec v20 sec.5.3.4 / manifest v15 Y-3c): this file belongs to the plane
`w6_point_map_producer`, era ERA_W6KEY. Its payload carries
`point_map_schema_id` and must never be presented to the byte-frozen R1/R2
core as a frozen-era native payload (M-8).
  [ep-era-declaration] plane=w6_point_map_producer predicate_spec_id=mb/ninfty-stage2-predicate/v20 verifier_contract_id=mb/ninfty-verifier-contract/v15 dependency_manifest_schema_id=mb/dependency-manifest/v15

FAIL-CLOSED: anything undecidable inside the v1 universe (coefficient field
Q, fixed target P^1_mu) is UNKNOWN with the reason recorded and NO records
emitted. Exact algebra only (sympy Rational/radicals); there is no floating
point anywhere in this file and no approximate root comparison.

CLI:  python search/ninfty-w6-pointmap-laneb.py <candidate.json> [artifact_id]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

X = sp.symbols("x")
TVAR = sp.symbols("T")

BRANCH_KEY_SCHEMA_ID = "mb/ninfty-w6-branch-key/v1"
POINT_MAP_SCHEMA_ID = "mb/ninfty-w6-point-map/v1"
IMAGE_WITNESS_SCHEMA_ID = "mb/ninfty-w6-image-witness/v1"
TARGET_COORDINATE_ID = "aqp1"
TARGET_MAP_ID = "mu"
DEFINITION_DOC = "docs/mb_ninfty_w6_branch_key_v1.md"

# This producer does not close W-6 and may not be read as closing it.
W6_CLOSED = False

_checker = None
_checker_native = None


def _load_module(filename, alias):
    path = os.path.join(HERE, filename)
    spec = importlib.util.spec_from_file_location(alias, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _lane_b_modules():
    """Lane B's OWN modules -- its decision chain and its from-scratch
    point-level construction. Nothing from the other lane is loadable from
    here: these are the only two project files this module ever opens."""
    global _checker, _checker_native
    if _checker is None:
        _checker = _load_module("ninfty-checker.py", "ninfty_checker_x_w6pm")
    if _checker_native is None:
        _checker_native = _load_module("ninfty-checker-native.py", "ninfty_checker_native_x_w6pm")
    return _checker, _checker_native


def _schema_definition_digest():
    try:
        with open(os.path.join(REPO, *DEFINITION_DOC.split("/")), "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def _sha256_json(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()


# ---------------------------------------------------------------------------
# K-2 / K-3, coded here from the schema's words. This is lane B's own
# implementation: no canonicaliser is imported and none is shared.
# ---------------------------------------------------------------------------

def _primitive_integer_form(rational_coeffs):
    """Low-to-high integer coefficient list: denominators cleared, content
    divided out, leading coefficient forced positive (K-2)."""
    den = 1
    for c in rational_coeffs:
        den = sp.ilcm(den, sp.Rational(c).q)
    ints = [int(sp.Rational(c) * den) for c in rational_coeffs]
    g = 0
    for c in ints:
        g = sp.igcd(g, abs(c))
    if g:
        ints = [c // g for c in ints]
    while len(ints) > 1 and ints[-1] == 0:
        ints = ints[:-1]
    if ints and ints[-1] < 0:
        ints = [-c for c in ints]
    return ints


def _exact_sign(expr):
    """+1 / -1 / 0, or None when this module cannot decide it EXACTLY.
    No numeric evaluation: the decision goes through sympy's exact
    assumptions on a simplified rational/radical expression (K-4 forbids
    comparing numerical approximations)."""
    e = sp.simplify(sp.nsimplify(expr))
    if e.is_zero:
        return 0
    if e.is_extended_negative:
        return -1
    if e.is_extended_positive:
        return 1
    return None


def _lex_less(z1, z2):
    """K-3's exact lexicographic order: Re first, then Im. Returns True /
    False / None (undecidable -> the caller reports UNKNOWN)."""
    dre = _exact_sign(sp.re(sp.expand(z1 - z2)))
    if dre is None:
        return None
    if dre != 0:
        return dre < 0
    dim = _exact_sign(sp.im(sp.expand(z1 - z2)))
    if dim is None:
        return None
    return dim < 0


def _minimal_polynomial_coeffs(value):
    """(coeffs_low_to_high, error). Lane B's own route: sympy's algebraic
    minimal polynomial of its own exact algebraic number, then K-2
    normalisation by the function above."""
    try:
        poly = sp.Poly(sp.minimal_polynomial(sp.nsimplify(value), TVAR), TVAR)
    except Exception as exc:                                    # noqa: BLE001
        return None, f"minimal polynomial of the exact image is not computable here: {exc}"
    coeffs = [sp.Rational(c) for c in reversed(poly.all_coeffs())]
    return _primitive_integer_form(coeffs), None


def _roots_of_quadratic(coeffs):
    """Exact roots of a0 + a1 T + a2 T^2 with a2 != 0, by lane B's own
    radical formula (never a numeric solver)."""
    a0, a1, a2 = (sp.Rational(c) for c in coeffs)
    disc = sp.simplify(a1 ** 2 - 4 * a0 * a2)
    root = sp.sqrt(disc)
    return [sp.simplify((-a1 - root) / (2 * a2)), sp.simplify((-a1 + root) / (2 * a2))]


def _rank_of(value, coeffs):
    """(rank, error). The 0-based rank of `value` among the roots of its own
    minimal polynomial under K-3's exact order. Degree 1 is rank 0; degree 2
    is decided exactly; degree >= 3 is UNKNOWN in the v1 universe (no float
    fallback -- schema O-3)."""
    degree = len(coeffs) - 1
    if degree == 1:
        return 0, None
    if degree != 2:
        return None, (f"the image's minimal polynomial has degree {degree}: the v1 universe decides exact "
                      "root ranks only up to degree 2, and an undecided rank is not a satisfied one")
    roots = _roots_of_quadratic(coeffs)
    less = _lex_less(roots[0], roots[1])
    if less is None:
        return None, "the two roots could not be ordered exactly under K-3"
    ordered = roots if less else [roots[1], roots[0]]
    for k, r in enumerate(ordered):
        if sp.simplify(sp.expand(r - value)) == 0:
            return k, None
    return None, "the value is not a root of its own minimal polynomial (internal inconsistency)"


def _image_datum(value, coeffs):
    """The exact image datum, in the schema's exact-datum vocabulary, derived
    from lane B's own algebraic number. (rational / quadratic_real /
    quadratic_imaginary; `infinity` is handled by the caller.)"""
    degree = len(coeffs) - 1
    if degree == 1:
        a0, a1 = coeffs
        return {"kind": "rational", "value": str(sp.Rational(-a0, a1))}, None
    if degree != 2:
        return None, f"degree {degree} image data are outside the v1 universe"
    a0, a1, a2 = (sp.Rational(c) for c in coeffs)
    re_part = sp.Rational(-a1, 2 * a2)
    disc = sp.Rational(a1 ** 2 - 4 * a0 * a2)
    quarter = sp.Rational(disc, 4 * a2 ** 2)          # (value - re_part)^2
    if quarter == 0:
        return None, "a repeated root cannot carry a well-defined rank"
    if quarter < 0:
        sign = _exact_sign(sp.im(sp.expand(value)))
        if sign in (None, 0):
            return None, "the imaginary part's sign could not be decided exactly"
        return {"kind": "quadratic_imaginary", "real_part": str(re_part),
                "imag_sq": str(-quarter), "sign": int(sign)}, None
    sign = _exact_sign(sp.expand(value - re_part))
    if sign in (None, 0):
        return None, "the offset from the rational real part could not be signed exactly"
    return {"kind": "quadratic_real", "real_part": str(re_part),
            "radicand": str(quarter), "sign": int(sign)}, None


def _token(coeffs, rank):
    return "{0}|{1}|F|{2}|{3}".format(TARGET_COORDINATE_ID, TARGET_MAP_ID,
                                      ",".join(str(c) for c in coeffs), rank)


TOKEN_INFINITY = "{0}|{1}|I".format(TARGET_COORDINATE_ID, TARGET_MAP_ID)


def _root_multiplicity(poly_expr, x0):
    """Exact multiplicity of x0 as a root of `poly_expr`, by repeated
    differentiation (lane B's own derivation of the ramification index:
    lemma N-inf-pair gives part(mu^{-1}(s)) = rootpart(a), so the index at a
    point over x0 is x0's multiplicity in a)."""
    k, cur = 0, sp.expand(poly_expr)
    while k <= 8:
        if sp.simplify(cur.subs(X, x0)) != 0:
            return k
        cur = sp.diff(cur, X)
        k += 1
    return None


# ---------------------------------------------------------------------------
# the producer
# ---------------------------------------------------------------------------

def build_w6_point_map_lane_b(candidate, source_artifact_id=None):
    checker, checker_native = _lane_b_modules()
    frame = {
        "branch_key_schema_id": BRANCH_KEY_SCHEMA_ID,
        "point_map_schema_id": POINT_MAP_SCHEMA_ID,
        "target_coordinate_id": TARGET_COORDINATE_ID,
        "branch_key_definition_digest": _schema_definition_digest(),
    }
    base = {
        "producer": "lane_b",
        "producer_module": "search/ninfty-w6-pointmap-laneb.py",
        "point_map_schema_id": POINT_MAP_SCHEMA_ID,
        "artifact_class": "diagnostic_construction",
        "registry_pinned": False,
        "w6_closed": W6_CLOSED,
        "frame": frame,
        "declared_support": [],
        "records": [],
        "unresolved": [],
        "note": ("diagnostic construction, not a published artifact; W-6 is OPEN (IMAGE-MU is UNKNOWN on "
                 "both receiver routes) and EP stays uncalibrated/UNKNOWN."),
    }

    # (1) lane B's OWN decision chain gates the map, exactly as lane B's own
    #     normal form is gated: a REJECTed candidate has no divisor-shaped
    #     data, so no ramification point may be named.
    decision_candidate = dict(candidate)
    decision_candidate["skip_native_construction"] = True
    decision = checker.run_checker(decision_candidate)
    stage = decision.get("stage")
    if stage == "REJECT":
        return dict(base, status="ABSENT", decision_stage=stage,
                    primary_reason_code=decision.get("primary_reason_code"),
                    reason=("lane B's own prerequisite chain (degree / E-1..E-4 / T-1) rejected this "
                            "candidate -- no divisor-shaped data exists, so no ramification point may "
                            "be named."))
    if stage == "INTEGRITY_STOP":
        return dict(base, status="INTEGRITY_STOP", decision_stage=stage,
                    primary_reason_code=decision.get("primary_reason_code"),
                    reason=("a theorem-forced identity broke after the prerequisites held; the input is "
                            "internally inconsistent."))

    a = checker_native.poly_from_coeffs(candidate["a"])
    p = checker_native.poly_from_coeffs(candidate["p"])
    f6 = checker_native.poly_from_coeffs(candidate["f6"])
    C = sp.nsimplify(sp.expand(a ** 2 - f6 * p ** 2))
    if (not C.is_constant()) or sp.simplify(C) == 0:
        return dict(base, status="UNKNOWN",
                    reason="a^2 - f6 p^2 is not a nonzero constant: the Pell datum this map rests on is absent.")

    # (2) lane B's own point-level construction of the finite ramification
    #     points: the fibres of the branch values s, -s with s^2 = -C.
    fin_status, fin = checker_native._finite_ramification_points(a, p, C)
    if fin_status != "ok":
        return dict(base, status="UNKNOWN",
                    reason=f"lane B's own finite ramification construction did not resolve: {fin_status}")

    # (3) the two points at infinity, from lane B's own local expansion. The
    #     branch that carries a ZERO of mu maps to 0; the branch that carries
    #     a POLE maps to infinity. Which is which is COMPUTED here, never
    #     assumed from the orientation attestation.
    inf = checker_native._infinity_local_orders(candidate["a"], candidate["p"], candidate["f6"])
    if inf.get("status") != "ok":
        return dict(base, status="UNKNOWN",
                    reason=f"the local expansion at infinity did not resolve: {inf.get('status')}")
    order_minus = inf["minus_branch"]["local_order_of_mu"]
    order_plus = inf["plus_branch"]["local_order_of_mu"]
    if order_minus is None or order_plus is None or order_minus <= 0 or order_plus >= 0:
        return dict(base, status="UNKNOWN",
                    reason=("the two branches at infinity did not come out as one zero and one pole of "
                            f"mu (minus branch order {order_minus}, plus branch order {order_plus}); "
                            "the points at infinity cannot be named. Fail-closed."))
    if order_minus != -order_plus:
        return dict(base, status="UNKNOWN",
                    reason=("the zero and pole orders of mu at infinity disagree "
                            f"({order_minus} vs {order_plus}), so deg(mu) is not well defined here."))
    deg_mu = int(order_minus)

    deg_f6 = int(sp.degree(f6, X))
    if deg_f6 % 2 != 0 or deg_f6 < 4:
        return dict(base, status="UNKNOWN", reason=f"deg f6 = {deg_f6}: the genus is not derivable here.")
    genus = (deg_f6 - 2) // 2
    required_degree = 2 * genus - 2 + 2 * deg_mu

    locus_digest = _sha256_json({"locus_type": "a-double-root-locus", "d_expr": fin["d_expr"],
                                 "lane": "B"})
    ref_status = "registry_pinned_claimed" if source_artifact_id else "LEGACY_UNVERIFIED_REF"

    records, support, unresolved = [], [], []

    for point in fin["points"]:
        x0 = sp.nsimplify(point["x"])
        if not x0.is_rational:
            unresolved.append({"x": str(x0),
                               "reason": ("the finite ramification support does not split into Q-rational "
                                          "points; separating it needs an x-side extension the v1 universe "
                                          "does not cover. Nothing is guessed.")})
            continue
        branch_value = sp.nsimplify(point["branch_value"])
        y_value = sp.nsimplify(point["y"])

        e_index = _root_multiplicity(a, x0)
        if not e_index or e_index < 2:
            unresolved.append({"x": str(x0),
                               "reason": f"x0 has multiplicity {e_index} in a: it is not a ramification point."})
            continue

        y_coeffs, err = _minimal_polynomial_coeffs(y_value)
        if err:
            unresolved.append({"x": str(x0), "reason": f"y: {err}"})
            continue
        y_rank, err = _rank_of(y_value, y_coeffs)
        if err:
            unresolved.append({"x": str(x0), "reason": f"y-root rank: {err}"})
            continue

        b_coeffs, err = _minimal_polynomial_coeffs(branch_value)
        if err:
            unresolved.append({"x": str(x0), "y_root_rank": y_rank, "reason": f"image: {err}"})
            continue
        b_rank, err = _rank_of(branch_value, b_coeffs)
        if err:
            unresolved.append({"x": str(x0), "y_root_rank": y_rank, "reason": f"image rank: {err}"})
            continue
        datum, err = _image_datum(branch_value, b_coeffs)
        if err:
            unresolved.append({"x": str(x0), "y_root_rank": y_rank, "reason": f"image datum: {err}"})
            continue

        point_id = f"aff|x={x0}|yrank={y_rank}"
        support.append(point_id)
        records.append({
            "ramification_point_id": point_id,
            "branch_value": _token(b_coeffs, b_rank),
            "multiplicity": int(e_index) - 1,
            "ramification_index": int(e_index),
            "source_locus_ref": {
                "artifact_id": source_artifact_id or "lane-b-diagnostic-locus",
                "json_pointer": "/ramification_divisor_on_C/finite",
                "digest": locus_digest,
                "ref_status": ref_status,
            },
            "exact_image_witness": {
                "schema_id": IMAGE_WITNESS_SCHEMA_ID,
                "datum": datum,
                "exact_reduction": {
                    "fibre_relation": {"variable": "y",
                                       "minimal_polynomial_low_to_high": [str(c) for c in y_coeffs],
                                       "root_rank": y_rank},
                    "point_construction": {
                        "form": "the fibre of the branch value v over x0, located from s^2 = -C: "
                                "y = v / p(x0), which lies on y^2 = f6(x0) by (Pell) at x0",
                        "x": str(x0), "y": str(y_value), "p_at_x": str(sp.nsimplify(p.subs(X, x0))),
                        "pell_constant": str(C),
                    },
                    "image_relation": {"variable": "mu",
                                       "minimal_polynomial_low_to_high": [str(c) for c in b_coeffs],
                                       "root_rank": b_rank},
                    "branch_value_relation": {"statement": "v^2 = -C (lemma N-inf-pair)",
                                              "value": str(branch_value)},
                },
            },
        })

    for point_id, order, image in (("inf_minus", order_minus, "zero"), ("inf_plus", order_plus, "pole")):
        multiplicity = abs(int(order)) - 1
        if image == "zero":
            coeffs, err = _minimal_polynomial_coeffs(sp.Integer(0))
            if err:
                unresolved.append({"point": point_id, "reason": err})
                continue
            token = _token(coeffs, 0)
            datum = {"kind": "rational", "value": "0"}
            image_relation = {"variable": "mu", "minimal_polynomial_low_to_high": [str(c) for c in coeffs],
                              "root_rank": 0}
        else:
            token = TOKEN_INFINITY
            datum = {"kind": "infinity"}
            image_relation = {"variable": "mu", "at_infinity": True}
        support.append(point_id)
        records.append({
            "ramification_point_id": point_id,
            "branch_value": token,
            "multiplicity": multiplicity,
            "ramification_index": abs(int(order)),
            "source_locus_ref": {
                "artifact_id": source_artifact_id or "lane-b-diagnostic-locus",
                "json_pointer": "/ramification_divisor_on_C/infinity",
                "digest": _sha256_json({"locus_type": "infinity", "point": point_id, "lane": "B"}),
                "ref_status": ref_status,
            },
            "exact_image_witness": {
                "schema_id": IMAGE_WITNESS_SCHEMA_ID,
                "datum": datum,
                "exact_reduction": {
                    "local_expansion": {
                        "form": "t = 1/x, Y(t) = y t^3 with Y(t)^2 = t^6 f6(1/t), mu t^5 = A(t) + P(t)Y(t)",
                        "branch": point_id,
                        "computed_local_order_of_mu": int(order),
                        "image": image,
                    },
                    "image_relation": image_relation,
                },
            },
        })

    total = sum(r["multiplicity"] for r in records)
    status = "UNKNOWN" if (unresolved or total != required_degree) else "PRESENT"
    out = dict(
        base,
        status=status,
        decision_stage=stage,
        declared_support=support,
        records=records,
        unresolved=unresolved,
        ramification_degree_check={
            "total_multiplicity": total,
            "required": required_degree,
            "derivation": f"2g-2+2deg(mu) with g = {genus} (from deg f6 = {deg_f6}) and "
                          f"deg(mu) = {deg_mu} (from the computed pole order at infinity)",
            "ok": total == required_degree,
        },
        pell_constant=str(C),
        finite_ramification_locus=fin["d_expr"],
    )
    if status == "UNKNOWN":
        out["reason"] = ("at least one ramification point could not be resolved exactly in the v1 universe "
                         "(see unresolved[])" if unresolved else
                         f"the per-point multiplicities sum to {total}, not the required "
                         f"deg R_mu = {required_degree}.")
    return out


def main(argv):
    ap = argparse.ArgumentParser(description="lane B per-point W-6 point-map producer")
    ap.add_argument("candidate_json", help="path to candidate JSON, or '-' for stdin")
    ap.add_argument("source_artifact_id", nargs="?", default=None)
    args = ap.parse_args(argv)
    if args.candidate_json == "-":
        candidate = json.load(sys.stdin)
    else:
        with open(args.candidate_json, encoding="utf-8") as f:
            candidate = json.load(f)
    out = build_w6_point_map_lane_b(candidate, source_artifact_id=args.source_artifact_id)
    print(json.dumps(out, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
