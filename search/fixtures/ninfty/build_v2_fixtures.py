#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/fixtures/ninfty/build_v2_fixtures.py

Rebuilds cert_pos_01..03.json / cert_neg_01..03.json from scratch in the
docs/notes/cert_shape_interpretation_v2.md shape (裁定133), additionally
satisfying search/ninfty-cert-validator.py's concrete checks (裁定134):
  - every required scalar id/digest field present, ids non-empty strings,
    digests EXACT 64-hex (computed here as sha256 of a documented label
    string / of the certificate's own canonicalized content for
    certificate_digest -- these are fixture-synthetic digests, NOT digests
    of any real external document; that is stated in each fixture's
    _description, not hidden).
  - field_embedding_witness_schema_id/digest present.
  - native *_ref fields are inline {"components":[...]} objects (not free
    strings).
  - multiplicity_equalities entries use searcher_mult/checker_mult (裁定134
    (j) -- mult_A/mult_B retired).

Uses search/ninfty-checker.py's own from-scratch Q[x] arithmetic (poly
add/mul/gcd/divmod) purely as fixture-generation TOOLING to compute exact
Bezout coefficients and reduction identities for the toy point sets below
-- this script is not part of either lane's shipped verifier code, so
importing it here does not create a cross-lane or cross-verifier
dependency (search/certs/laneB_manifest.json's independence claim is
about verify_W*/verifier-b.py's own runtime closure, unaffected by this
build-time-only script).
"""
import hashlib
import importlib.util
import json
import os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
SEARCH_DIR = os.path.dirname(os.path.dirname(HERE))


def _load_module(name, relpath):
    path = os.path.join(SEARCH_DIR, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


chk = _load_module("ninfty_checker_for_fixture_build", "ninfty-checker.py")

TOKENS = ("ramification_divisor_on_C_ref", "branch_divisor_on_P1_ref")


def sha256_str(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def poly_str(coeffs):
    """coeffs: list[Fraction] low-to-high -> list[str] for JSON."""
    return [str(c) for c in coeffs]


def bezout(a, b):
    """
    Extended Euclid over Q[x] (self-contained, via chk.p_gcd's building
    blocks): returns (u, v, g) with u*a + v*b = g (g = monic gcd(a,b) up
    to the same scalar as computed here -- we normalize so g = [1] when
    a,b are coprime, which is all this fixture builder needs).
    """
    old_r, r = list(a), list(b)
    old_s, s = [F(1)], []
    old_t, t = [], [F(1)]
    while chk.p_deg(r) >= 0 or r:
        if not r:
            break
        q, rem = chk.p_divmod(old_r, r)
        old_r, r = r, rem
        old_s, s = s, chk.p_sub(old_s, chk.p_mul(q, s))
        old_t, t = t, chk.p_sub(old_t, chk.p_mul(q, t))
    # old_r is (a scalar multiple of) gcd(a,b); normalize to monic 1 (coprime case)
    g = chk._trim(old_r)
    if chk.p_deg(g) == 0 and g:
        scale = F(1) / g[0]
        return chk.p_scale(old_s, scale), chk.p_scale(old_t, scale), [F(1)]
    return old_s, old_t, g


def linear(root):
    """monic (x - root) as list[Fraction]."""
    return [F(-root), F(1)]


def reduction_witness(dividend, divisor_monic, tag="reduction-to-zero"):
    q, r = chk.p_divmod(dividend, divisor_monic)
    return {
        "tag": tag,
        "dividend": poly_str(dividend),
        "divisor_monic": poly_str(divisor_monic),
        "quotient": poly_str(q),
        "remainder": poly_str(r),
    }


SCALAR_ID_FIELDS = [
    "predicate_spec_id", "schema_id", "candidate_ref",
    "ambient_coordinate_ring_schema_id", "coefficient_field_presentation_id",
    "field_embedding_witness_schema_id", "monomial_order_id", "groebner_reduction_contract_id",
]
SCALAR_DIGEST_FIELDS_FROM_ID = {
    # digest = sha256(corresponding id string) -- fixture-synthetic, documented.
    "ambient_coordinate_ring_schema_digest": "ambient_coordinate_ring_schema_id",
    "coefficient_field_presentation_digest": "coefficient_field_presentation_id",
    "field_embedding_witness_schema_digest": "field_embedding_witness_schema_id",
    "monomial_order_digest": "monomial_order_id",
    "groebner_reduction_contract_digest": "groebner_reduction_contract_id",
}


def build_base_certificate(candidate_ref, curve_label):
    cert = {
        "predicate_spec_id": "mb/ninfty-stage2-predicate/v18",
        "predicate_spec_digest": "e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56",
        "schema_id": "mb/ninfty-stage2-predicate/v18#cert-schema",
        "schema_digest": "e2c9c701477968b9d08b60ffc22f828b917074361f6cc3b71e8eff7ee37c0f56",
        "candidate_ref": candidate_ref,
        "curve_model_digest": sha256_str(f"toy-curve-model/{curve_label}"),
        "chart_ids": ["chart-A", "chart-B"],
        "ambient_coordinate_ring_schema_id": "mb/ninfty-laneb-toy/ambient-ring/v1",
        "ambient_quotient_relations": "none (Q[x], no quotient) -- toy single-variable fixture",
        "coefficient_field_presentation_id": "Q/standard",
        "field_embedding_witness_schema_id": "mb/ninfty-laneb-toy/no-embedding-needed/v1",
        "monomial_order_id": "lex-single-variable",
        "groebner_reduction_contract_id": "mb/ninfty-laneb-toy/monic-poly-division/v1",
    }
    for digest_field, id_field in SCALAR_DIGEST_FIELDS_FROM_ID.items():
        cert[digest_field] = sha256_str(cert[id_field])
    return cert


def build_native_side(points):
    """points: list of (locus_type, generator_poly[Fraction], multiplicity)."""
    components = [
        {"locus_type": lt, "ideal_generator": poly_str(gen), "multiplicity": mult}
        for (lt, gen, mult) in points
    ]
    return {"components": components}


def assemble(candidate_ref, curve_label, points, mismatches=None):
    """
    points: list of (locus_type, generator_poly[Fraction], searcher_mult, checker_mult)
    mismatches: dict of deliberate defects to inject, e.g.
      {"w2_break_locus": "pt1"}  -> forward reduction for that locus is wrong
      {"w3_break_locus": "pt1"}  -> searcher_mult != checker_mult for that locus
      {"w6_break": True}        -> branch_points multiplicity wrong
    """
    mismatches = mismatches or {}
    cert = build_base_certificate(candidate_ref, curve_label)

    native_points = [(lt, gen, cm) for (lt, gen, sm, cm) in points]  # native components use checker_mult by convention
    native_side = build_native_side(native_points)
    cert["searcher_native"] = {
        "ramification_divisor_on_C_ref": native_side,
        "branch_divisor_on_P1_ref": native_side,
        "native_schema_id": "mb/ninfty-laneb-toy/native-output/v1",
        "native_schema_digest": None,  # documented ABSENT-null exception (validator allows this one)
    }
    cert["checker_native"] = {
        "ramification_divisor_on_C_ref": native_side,
        "branch_divisor_on_P1_ref": native_side,
        "native_schema_id": "mb/ninfty-laneb-toy/native-output/v1",
        "native_schema_digest": None,
    }
    native_a = {"ramification_divisor_on_C_ref": native_side, "branch_divisor_on_P1_ref": native_side}
    native_b = {"ramification_divisor_on_C_ref": native_side, "branch_divisor_on_P1_ref": native_side}
    cert["searcher_native"]["native_artifact_digest"] = sha256_of(native_a)
    cert["checker_native"]["native_artifact_digest"] = sha256_of(native_b)

    n = len(points)

    # W-1 component_bijection (裁定133 (g)): one entry per (token, locus).
    component_bijection = []
    for tok in TOKENS:
        for i, (lt, gen, sm, cm) in enumerate(points):
            component_bijection.append({
                "divisor_object": tok, "searcher_index": i, "checker_index": i, "locus_type": lt,
            })
    cert["component_bijection"] = component_bijection

    # W-2 exact_point_equality_witnesses (裁定133 (h), nested witness).
    w2 = []
    for tok in TOKENS:
        for (lt, gen, sm, cm) in points:
            fwd_dividend = gen
            if mismatches.get("w2_break_locus") == lt:
                # deliberately wrong dividend (add 1 to the constant term) so the
                # reduction identity dividend == quotient*divisor + remainder fails.
                fwd_dividend = chk.p_add(gen, [F(1)])
            fwd = reduction_witness(fwd_dividend, chk.p_monic(gen), "reduction-to-zero")
            bwd = reduction_witness(gen, chk.p_monic(gen), "reduction-to-zero")
            w2.append({
                "divisor_object": tok, "locus_type": lt,
                "witness": {"kind": "ideal-equality", "ok": mismatches.get("w2_break_locus") != lt,
                            "forward": fwd, "backward": bwd},
            })
    cert["exact_point_equality_witnesses"] = w2

    # W-2' distinctness_witnesses (裁定133 (h) family, disjointness kind).
    w2p = []
    for tok in TOKENS:
        for i in range(n):
            for j in range(i + 1, n):
                gi = points[i][1]
                gj = points[j][1]
                u, v, g = bezout(gi, gj)
                w2p.append({
                    "divisor_object": tok, "pair": [i, j],
                    "witness": {
                        "kind": "disjointness", "ok": True,
                        "generator_P": poly_str(gi), "generator_Q": poly_str(gj),
                        "bezout_u": poly_str(u), "bezout_v": poly_str(v),
                        "reduction_tag": "reduction-to-one",
                    },
                })
    cert["distinctness_witnesses"] = w2p

    # W-3 multiplicity_equalities (裁定134 (j): searcher_mult/checker_mult).
    w3 = []
    for tok in TOKENS:
        for (lt, gen, sm, cm) in points:
            actual_cm = cm
            if mismatches.get("w3_break_locus") == lt:
                actual_cm = cm + 1  # deliberate mismatch
            w3.append({
                "divisor_object": tok, "locus_type": lt,
                "searcher_mult": sm, "checker_mult": actual_cm,
            })
    cert["multiplicity_equalities"] = w3

    # W-4 chart_overlap_witnesses (裁定133 (i): {divisor_object, status,
    # per_overlap_witnesses:[...]} -- plural, divisor_object-tagged).
    w4 = []
    for tok in TOKENS:
        overlaps = [
            {"chart_pair": ["chart-A", "chart-B"], "component_in_chart_a": lt, "component_in_chart_b": lt}
            for (lt, gen, sm, cm) in points
        ]
        w4.append({"divisor_object": tok, "status": "agree", "per_overlap_witnesses": overlaps})
    cert["chart_overlap_witnesses"] = w4

    # W-5 total_coverage_and_no_extra_component_witness (2-entry array;
    # this implementer's adopted field names, 裁定133/134 do not literally
    # specify W-5's own shape -- see verifier-b.py module docstring).
    w5 = []
    for tok in TOKENS:
        w5.append({
            "divisor_object": tok, "searcher_count": n, "checker_count": n,
            "matched_count": n, "no_extra": True, "extra_candidates": [],
        })
    cert["total_coverage_and_no_extra_component_witness"] = w5

    # W-6 pushforward_compatibility_witness (裁定133 (i): {divisor_object,
    # status, points:[...]} -- 2-entry array, one status+points list per
    # object; each point tagged role="ramification"|"branch").
    w6 = []
    for tok in TOKENS:
        points_list = [
            {"role": "ramification", "maps_to_branch_value": lt, "multiplicity": sm}
            for (lt, gen, sm, cm) in points
        ]
        for (lt, gen, sm, cm) in points:
            mult = sm
            if mismatches.get("w6_break") and lt == points[0][0]:
                mult = sm + 1  # deliberate mismatch on the first locus
            points_list.append({"role": "branch", "branch_value": lt, "multiplicity": mult})
        status = "FAIL" if mismatches.get("w6_break") else "PASS"
        w6.append({"divisor_object": tok, "status": status, "points": points_list})
    cert["pushforward_compatibility_witness"] = w6

    cert["certificate_digest"] = sha256_of(cert)

    payload = {
        "_description": None,  # filled by caller
        "certificate": cert,
        "native_a": native_a,
        "native_b": native_b,
    }
    return payload


def write_fixture(fname, description, payload):
    payload["_description"] = description
    path = os.path.join(HERE, fname)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, indent=2, ensure_ascii=True)
        f.write("\n")
    print(f"wrote {fname}")


def main():
    # --- positive fixtures ---
    pts1 = [("pt-x1", linear(1), 1, 1), ("pt-x2", linear(2), 2, 2)]
    write_fixture(
        "cert_pos_01.json",
        "Self-made positive certificate fixture 1, rebuilt in "
        "cert_shape_interpretation_v2.md shape (裁定133/134). All scalar "
        "id/digest fields required by search/ninfty-cert-validator.py are "
        "present; digests are sha256 of a documented label string (or, for "
        "certificate_digest, sha256 of the certificate's own canonical "
        "content) -- fixture-synthetic, NOT real external document digests. "
        "Two toy point loci at x=1 (mult 1) and x=2 (mult 2), all 7 witness "
        "fields fully populated and internally consistent (expect verifier-b "
        "overall PASS).",
        assemble("cert-pos-01-v2", "pos01", pts1),
    )

    pts2 = [("pt-x5", linear(5), 3, 3), ("pt-x6", linear(6), 1, 1)]
    write_fixture(
        "cert_pos_02.json",
        "Self-made positive certificate fixture 2 (v2 shape), point loci "
        "at x=5 (mult 3) and x=6 (mult 1).",
        assemble("cert-pos-02-v2", "pos02", pts2),
    )

    pts3 = [("pt-x7", linear(7), 1, 1), ("pt-x8", linear(8), 1, 1), ("pt-x9", linear(9), 2, 2)]
    write_fixture(
        "cert_pos_03.json",
        "Self-made positive certificate fixture 3 (v2 shape), three point "
        "loci (x=7,8,9), exercising a 3-component bijection/coverage/"
        "pushforward all at once.",
        assemble("cert-pos-03-v2", "pos03", pts3),
    )

    # --- negative fixtures (each isolates exactly one witness failure) ---
    write_fixture(
        "cert_neg_01.json",
        "Self-made negative certificate fixture 1 (v2 shape): W-2 forward "
        "reduction identity deliberately broken for locus 'pt-x1' (dividend "
        "shifted by +1, so dividend != quotient*divisor_monic+remainder). "
        "Expect W-2 = FAIL, other witnesses PASS.",
        assemble("cert-neg-01-v2", "neg01", pts1, mismatches={"w2_break_locus": "pt-x1"}),
    )
    write_fixture(
        "cert_neg_02.json",
        "Self-made negative certificate fixture 2 (v2 shape): W-3 "
        "multiplicity_equalities deliberately mismatched for locus 'pt-x1' "
        "(checker_mult off by one from searcher_mult). Expect W-3 = FAIL.",
        assemble("cert-neg-02-v2", "neg02", pts1, mismatches={"w3_break_locus": "pt-x1"}),
    )
    write_fixture(
        "cert_neg_03.json",
        "Self-made negative certificate fixture 3 (v2 shape): W-6 "
        "pushforward_compatibility_witness deliberately mismatched (declared "
        "branch multiplicity for the first locus is off by one from the sum "
        "of ramification multiplicities). Expect W-6 = FAIL.",
        assemble("cert-neg-03-v2", "neg03", pts1, mismatches={"w6_break": True}),
    )


if __name__ == "__main__":
    main()
