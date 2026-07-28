#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/fixtures/ninfty/build_v3_fixtures.py

Rebuilds cert_pos_01..03.json / cert_neg_01..03.json in the
docs/notes/cert_shape_interpretation_v3.md shape (裁定139), superseding
build_v2_fixtures.py (kept for history). Two fields change shape from v2:

  - component_bijection (item 6): EDGE list --
    {divisor_object, searcher_native_digest, searcher_component_id,
     checker_native_digest, checker_component_id}. searcher/checker
    _native_digest are the ACTUAL recomputed sha256 of native_a/native_b
    (so verify_W1's digest cross-check passes); *_component_id use
    locus_type as the id (this implementer's adopted convention, matching
    verify_W1's _native_component_ids reader).

  - pushforward_compatibility_witness (item 2): native_side-tagged,
    EXACTLY 2 entries total (not per divisor_object) --
    {native_side: "searcher"|"checker", ramification_ref, branch_ref,
     map_ref, witness_ref}, each a ref-triple {artifact_id, digest,
     json_pointer, inline}(inline optional in general, but supplied here
     so the fixtures exercise genuine re-verification rather than landing
     in the documented "digest-only, UNKNOWN" branch). map_ref.inline
     carries the actual [{branch_value, multiplicity}, ...] data compared
     between the two lanes.

All other fields (W-2/W-2'/W-3/W-4/W-5, scalar id/digest fields) are
unchanged from v2 (裁定133/134 kept per v3 items 4/7/8).

Uses search/ninfty-checker.py's own from-scratch Q[x] arithmetic purely as
fixture-generation TOOLING (see build_v2_fixtures.py docstring for the
independence rationale, unchanged here).
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


chk = _load_module("ninfty_checker_for_fixture_build_v3", "ninfty-checker.py")

TOKENS = ("ramification_divisor_on_C_ref", "branch_divisor_on_P1_ref")


def sha256_str(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def poly_str(coeffs):
    return [str(c) for c in coeffs]


def bezout(a, b):
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
    g = chk._trim(old_r)
    if chk.p_deg(g) == 0 and g:
        scale = F(1) / g[0]
        return chk.p_scale(old_s, scale), chk.p_scale(old_t, scale), [F(1)]
    return old_s, old_t, g


def linear(root):
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


def make_ref(artifact_id, json_pointer, inline_content):
    """裁定139 item 3 ref-triple, WITH inline content (so digest = sha256
    of that content and the fixtures exercise genuine re-verification)."""
    return {
        "artifact_id": artifact_id,
        "digest": sha256_of(inline_content),
        "json_pointer": json_pointer,
        "inline": inline_content,
    }


SCALAR_DIGEST_FIELDS_FROM_ID = {
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
      {"w6_break": True}        -> checker's map_ref multiplicity wrong
    """
    mismatches = mismatches or {}
    cert = build_base_certificate(candidate_ref, curve_label)

    native_points = [(lt, gen, cm) for (lt, gen, sm, cm) in points]
    native_side = build_native_side(native_points)
    native_a = {"ramification_divisor_on_C_ref": native_side, "branch_divisor_on_P1_ref": native_side}
    native_b = {"ramification_divisor_on_C_ref": native_side, "branch_divisor_on_P1_ref": native_side}
    native_a_digest = sha256_of(native_a)
    native_b_digest = sha256_of(native_b)

    # 裁定139 item 3: any field literally named `*_ref` is itself a
    # ref-triple {artifact_id, digest, json_pointer|object_id[, inline]} --
    # this applies to searcher_native/checker_native's
    # ramification_divisor_on_C_ref / branch_divisor_on_P1_ref too, not
    # just the witness-level refs. inline mirrors native_side so the
    # content is genuinely re-derivable, not just a bare digest.
    cert["searcher_native"] = {
        "ramification_divisor_on_C_ref": make_ref("native_a", "/ramification_divisor_on_C_ref", native_side),
        "branch_divisor_on_P1_ref": make_ref("native_a", "/branch_divisor_on_P1_ref", native_side),
        "native_schema_id": "mb/ninfty-laneb-toy/native-output/v1",
        "native_schema_digest": None,
        "native_artifact_digest": native_a_digest,
    }
    cert["checker_native"] = {
        "ramification_divisor_on_C_ref": make_ref("native_b", "/ramification_divisor_on_C_ref", native_side),
        "branch_divisor_on_P1_ref": make_ref("native_b", "/branch_divisor_on_P1_ref", native_side),
        "native_schema_id": "mb/ninfty-laneb-toy/native-output/v1",
        "native_schema_digest": None,
        "native_artifact_digest": native_b_digest,
    }

    n = len(points)

    # W-1 component_bijection (裁定139 item 6 + 追補 (m): EDGE list,
    # native-digest bound, component_id = fully-qualified
    # "<divisor_object_ref>:<locus_type>" matching verify_W1's
    # independently-derived native reconstruction).
    component_bijection = []
    for tok in TOKENS:
        for (lt, gen, sm, cm) in points:
            qualified_id = f"{tok}:{lt}"
            component_bijection.append({
                "divisor_object": tok,
                "searcher_native_digest": native_a_digest,
                "searcher_component_id": qualified_id,
                "checker_native_digest": native_b_digest,
                "checker_component_id": qualified_id,
            })
    cert["component_bijection"] = component_bijection

    # W-2 exact_point_equality_witnesses (裁定133 (h) -- unchanged in v3).
    w2 = []
    for tok in TOKENS:
        for (lt, gen, sm, cm) in points:
            fwd_dividend = gen
            if mismatches.get("w2_break_locus") == lt:
                fwd_dividend = chk.p_add(gen, [F(1)])
            fwd = reduction_witness(fwd_dividend, chk.p_monic(gen), "reduction-to-zero")
            bwd = reduction_witness(gen, chk.p_monic(gen), "reduction-to-zero")
            w2.append({
                "divisor_object": tok, "locus_type": lt,
                "witness": {"kind": "ideal-equality", "ok": mismatches.get("w2_break_locus") != lt,
                            "forward": fwd, "backward": bwd},
            })
    cert["exact_point_equality_witnesses"] = w2

    # W-2' distinctness_witnesses (unchanged in v3).
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

    # W-3 multiplicity_equalities (裁定134 (j) -- unchanged in v3).
    w3 = []
    for tok in TOKENS:
        for (lt, gen, sm, cm) in points:
            actual_cm = cm
            if mismatches.get("w3_break_locus") == lt:
                actual_cm = cm + 1
            w3.append({
                "divisor_object": tok, "locus_type": lt,
                "searcher_mult": sm, "checker_mult": actual_cm,
            })
    cert["multiplicity_equalities"] = w3

    # W-4 chart_overlap_witnesses (裁定133 (i)/裁定139 item 7 shape unchanged;
    # field renamed + status vocabulary made strict by 裁定152 §3-1 /
    # 追補(n) v2, sol/裁定_152_便78検収.md: {status: "ABSENT"|"PRESENT",
    # entries: [...]} is now the ONLY accepted shape -- the old free-text
    # "agree" status and "per_overlap_witnesses" key are retired).
    w4 = []
    for tok in TOKENS:
        overlaps = [
            {"chart_pair": ["chart-A", "chart-B"], "component_in_chart_a": lt, "component_in_chart_b": lt}
            for (lt, gen, sm, cm) in points
        ]
        w4.append({"divisor_object": tok, "status": "PRESENT", "entries": overlaps})
    cert["chart_overlap_witnesses"] = w4

    # W-5 total_coverage_and_no_extra_component_witness (unchanged in v3).
    w5 = []
    for tok in TOKENS:
        w5.append({
            "divisor_object": tok, "searcher_count": n, "checker_count": n,
            "matched_count": n, "no_extra": True, "extra_candidates": [],
        })
    cert["total_coverage_and_no_extra_component_witness"] = w5

    # W-6 pushforward_compatibility_witness (裁定139 item 2: native_side tag,
    # exactly 2 entries total -- cross-lane map comparison, no
    # divisor_object duplication).
    searcher_map_inline = [{"branch_value": lt, "multiplicity": sm} for (lt, gen, sm, cm) in points]
    checker_map_inline = []
    for (lt, gen, sm, cm) in points:
        mult = cm
        if mismatches.get("w6_break") and lt == points[0][0]:
            mult = cm + 1
        checker_map_inline.append({"branch_value": lt, "multiplicity": mult})
    cert["pushforward_compatibility_witness"] = [
        {
            "native_side": "searcher",
            "ramification_ref": make_ref("native_a", "/ramification_divisor_on_C_ref",
                                          {"note": "ramification evidence (searcher)"}),
            "branch_ref": make_ref("native_a", "/branch_divisor_on_P1_ref",
                                    {"note": "branch evidence (searcher)"}),
            "map_ref": make_ref("native_a", "/pushforward_map", searcher_map_inline),
            "witness_ref": make_ref("native_a", "/witness", {"note": "witness evidence (searcher)"}),
        },
        {
            "native_side": "checker",
            "ramification_ref": make_ref("native_b", "/ramification_divisor_on_C_ref",
                                          {"note": "ramification evidence (checker)"}),
            "branch_ref": make_ref("native_b", "/branch_divisor_on_P1_ref",
                                    {"note": "branch evidence (checker)"}),
            "map_ref": make_ref("native_b", "/pushforward_map", checker_map_inline),
            "witness_ref": make_ref("native_b", "/witness", {"note": "witness evidence (checker)"}),
        },
    ]

    cert["certificate_digest"] = sha256_of(cert)

    payload = {
        "_description": None,
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
    pts1 = [("pt-x1", linear(1), 1, 1), ("pt-x2", linear(2), 2, 2)]
    write_fixture(
        "cert_pos_01.json",
        "Self-made positive certificate fixture 1, rebuilt in "
        "cert_shape_interpretation_v3.md shape (裁定139): component_bijection "
        "is now an edge list bound to the actual recomputed native_a/native_b "
        "digests; pushforward_compatibility_witness is native_side-tagged "
        "(exactly 2 entries: searcher, checker) with ref-triple fields "
        "carrying inline content. All scalar id/digest fields required by "
        "search/ninfty-cert-validator.py are present (fixture-synthetic "
        "digests, documented as such). Two toy point loci at x=1 (mult 1) "
        "and x=2 (mult 2); expect verifier-b overall PASS.",
        assemble("cert-pos-01-v3", "pos01", pts1),
    )

    pts2 = [("pt-x5", linear(5), 3, 3), ("pt-x6", linear(6), 1, 1)]
    write_fixture(
        "cert_pos_02.json",
        "Self-made positive certificate fixture 2 (v3 shape), point loci "
        "at x=5 (mult 3) and x=6 (mult 1).",
        assemble("cert-pos-02-v3", "pos02", pts2),
    )

    pts3 = [("pt-x7", linear(7), 1, 1), ("pt-x8", linear(8), 1, 1), ("pt-x9", linear(9), 2, 2)]
    write_fixture(
        "cert_pos_03.json",
        "Self-made positive certificate fixture 3 (v3 shape), three point "
        "loci (x=7,8,9), exercising a 3-component bijection/coverage/"
        "pushforward all at once.",
        assemble("cert-pos-03-v3", "pos03", pts3),
    )

    write_fixture(
        "cert_neg_01.json",
        "Self-made negative certificate fixture 1 (v3 shape): W-2 forward "
        "reduction identity deliberately broken for locus 'pt-x1'. Expect "
        "W-2 = FAIL, other witnesses PASS.",
        assemble("cert-neg-01-v3", "neg01", pts1, mismatches={"w2_break_locus": "pt-x1"}),
    )
    write_fixture(
        "cert_neg_02.json",
        "Self-made negative certificate fixture 2 (v3 shape): W-3 "
        "multiplicity_equalities deliberately mismatched for locus 'pt-x1'. "
        "Expect W-3 = FAIL.",
        assemble("cert-neg-02-v3", "neg02", pts1, mismatches={"w3_break_locus": "pt-x1"}),
    )
    write_fixture(
        "cert_neg_03.json",
        "Self-made negative certificate fixture 3 (v3 shape): W-6 checker "
        "lane's map_ref.inline multiplicity deliberately mismatched for the "
        "first locus (searcher says 1, checker says 2) -- cross-lane map "
        "comparison must FAIL.",
        assemble("cert-neg-03-v3", "neg03", pts1, mismatches={"w6_break": True}),
    )


if __name__ == "__main__":
    main()
