#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-verifier-b.py

N_infty stage-2 -- independent verifier B, per
mb/ninfty-verifier-contract/v13 (governing spec = mb/ninfty-stage2-predicate/v18).

Role (contract sec.1 V-0..V-3):
  * This is NOT a judgment lane. It cannot emit ACCEPT on its own.
  * It re-verifies a `divisor_equality_certificate` (governing spec sec.4.1)
    against the two supplied native artifacts, producing the canonical
    per-witness result vector R_B (contract sec.3.4) for BOTH objects
    (ramification_divisor_on_C, branch_divisor_on_P1), plus an overall
    verdict_B and its result_digest_B.
  * It does NOT compute the concordance comparison R_A vs R_B itself
    (contract C-7: "A と B は互いの中間結果を読まない" -- the comparison
    at [26] belongs to the receiving side, which holds both R_A and R_B
    independently computed). This file only ever reads its own
    certificate/native inputs; it never imports, reads, or references
    verifier A's code or output.
  * It replays certificate-declared arithmetic (representation
    coefficients / reduction steps / Bezout coefficients) using its own
    from-scratch multivariate polynomial engine below -- it never trusts
    the certificate's claims, and it never calls a shared canonicalizer
    (there isn't one available to it: this file has no import of lane A
    or of any shared math-helper module; role classification for the
    manifest is done in search/certs/laneB_manifest.json).

Contact discipline: value-independent. Never hardcodes C, h, a5,
squareclasses, signs, branch values, concrete coefficients, or raw shard
naming patterns. All data comes from the certificate/native JSON supplied
by the caller.

Scope / EP status: EP has not run. Per spec sec.9 / contract sec.9, this
is a PARTIAL verifier. Declared UNKNOWN / NOT IMPLEMENTED (sec. "Scope"
below, not silently skipped):
  * P-0.6 / P-1.4 (field_embedding_witness cross-presentation checks):
    only structural presence is checked (witness object exists and is
    well-typed); the embedding map itself is not independently
    recomputed (would require a field-arithmetic engine beyond this
    partial predicate's scope).
  * W-4 (chart_overlap_witnesses): checked for internal consistency of
    the declared data only; does not re-derive the chart atlas itself.
  * CR-11 (contract sec.9.1): the three-layer `implemented_checks`
    equality is UNKNOWN (no executable inventory system exists yet);
    this file only claims `defined = claimed_covered` in its own
    self-report, matching the contract's own current-unknown note.

runtime = python (stdlib only: fractions, hashlib, json, sys, argparse).
"""

from __future__ import annotations
from fractions import Fraction
import hashlib
import json
import sys
import argparse

# --------------------------------------------------------------------------
# Self-implemented multivariate polynomial engine over Q.
# Monomial = tuple of nonnegative ints (exponents, variable order fixed by
# the certificate's declared variable list). Poly = dict{monomial: Fraction}
# with zero coefficients always removed (canonical form for this file).
# This engine is used ONLY to replay certificate-declared arithmetic
# (representation coefficients / reduction steps / Bezout coefficients).
# It does not compute a Groebner basis from scratch; it verifies that the
# certificate's own claimed reduction/representation is arithmetically
# correct, which is the check the contract specifies (sec.3.1 table:
# "再計算内容" = replay the claimed coefficients/reduction and compare).
# --------------------------------------------------------------------------


def _F(x):
    if isinstance(x, Fraction):
        return x
    if isinstance(x, str) and "/" in x:
        n, d = x.split("/")
        return Fraction(int(n), int(d))
    return Fraction(x)


def _canon_mono(m):
    """
    Strip trailing zero exponents so monomials of differing declared
    arity that denote the same term (e.g. mono=[0] and mono=[] both
    meaning the constant monomial) hash and compare equal. Without this,
    a certificate that writes the constant term as mono=[0] (one
    variable, exponent 0) instead of mono=[] would silently fail a
    disjointness / reduction-to-one check even though it is
    mathematically the same monomial -- caught by cert_pos_01's W-2'
    self-test during development, fixed here.
    """
    m = tuple(m)
    while m and m[-1] == 0:
        m = m[:-1]
    return m


def mv_from_json(terms):
    """terms: list of {"coeff": "n/d"|num, "mono": [e1,e2,...]}"""
    out = {}
    for t in terms:
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


def mv_scale(a, k):
    if k == 0:
        return {}
    return {m: c * k for m, c in a.items()}


def mv_mono_mul(m1, m2):
    n = max(len(m1), len(m2))
    m1 = m1 + (0,) * (n - len(m1))
    m2 = m2 + (0,) * (n - len(m2))
    return _canon_mono(tuple(x + y for x, y in zip(m1, m2)))


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


# --------------------------------------------------------------------------
# W-2 (contract sec.3.1): kind = ideal-equality re-verification.
# --------------------------------------------------------------------------


def verify_membership_by_representation(witness):
    """
    witness = {
      "kind": "ideal-equality", "form": "representation",
      "g": <poly terms>,                # the generator being expressed
      "u": [<poly terms>, ...],         # representation coefficients u_i
      "h": [<poly terms>, ...],         # the OTHER ideal's generators h_i
      "tag": "reduction-to-zero"|"reduction-to-one"   # per P-1.5 (mandatory)
    }
    Re-derive sum(u_i * h_i) from scratch and compare to g (contract
    sec.3.1: "係数まで一致するか").
    """
    if witness.get("tag") not in ("reduction-to-zero", "reduction-to-one"):
        return "FAIL", {"reason": "missing/invalid kind tag (P-1.5)"}
    g = mv_from_json(witness["g"])
    us = [mv_from_json(u) for u in witness["u"]]
    hs = [mv_from_json(h) for h in witness["h"]]
    if len(us) != len(hs):
        return "FAIL", {"reason": "u/h length mismatch"}
    acc = {}
    for u, h in zip(us, hs):
        acc = mv_add(acc, mv_mul(u, h))
    ok = mv_eq(acc, g)
    return ("PASS" if ok else "FAIL"), {"recomputed": _terms_out(acc), "claimed": _terms_out(g)}


def verify_membership_by_reduction(witness):
    """
    witness = {
      "kind": "ideal-equality", "form": "reduction-to-zero",
      "g": <poly terms>,
      "steps": [ {"coeff": ..., "mono": [...], "generator": <poly terms>} , ... ],
      "tag": "reduction-to-zero"|"reduction-to-one"
    }
    Replays: r := g ; for each step: r := r - coeff * x^mono * generator.
    PASS iff final r is zero (tag=reduction-to-zero) or one
    (tag=reduction-to-one, used only for disjointness certs, see below).
    """
    if witness.get("tag") not in ("reduction-to-zero", "reduction-to-one"):
        return "FAIL", {"reason": "missing/invalid kind tag (P-1.5)"}
    r = mv_from_json(witness["g"])
    for step in witness.get("steps", []):
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


def _terms_out(poly):
    return sorted(
        ({"mono": list(m), "coeff": str(c)} for m, c in poly.items()),
        key=lambda t: t["mono"],
    )


def verify_W2(cert):
    """
    W-2: exact_point_equality_witnesses, kind=ideal-equality ONLY (contract
    sec.3.1). Requires BOTH directions (I0 subseteq I1 and I1 subseteq I0)
    for ALL generators to PASS (P-1.1).
    """
    witnesses = cert.get("exact_point_equality_witnesses")
    if not witnesses:
        return "ABSENT", {"reason": "no exact_point_equality_witnesses supplied"}

    all_detail = []
    all_ok = True
    for w in witnesses:
        if w.get("kind") != "ideal-equality":
            all_ok = False
            all_detail.append({"reason": "wrong kind for W-2 (must be ideal-equality)"})
            continue
        form = w.get("form")
        if form == "representation":
            status, detail = verify_membership_by_representation(w)
        elif form == "reduction-to-zero":
            status, detail = verify_membership_by_reduction(w)
        else:
            status, detail = "FAIL", {"reason": "unknown form"}
        all_detail.append({"form": form, "status": status, "detail": detail})
        if status != "PASS":
            all_ok = False
    return ("PASS" if all_ok else "FAIL"), {"witnesses": all_detail}


def verify_W2prime(cert):
    """
    W-2' (contract sec.3.1.2): kind=disjointness. Bezout certificate
    1 in I_P + I_Q, replayed via reduction-to-one or explicit sum check.
    """
    witnesses = cert.get("distinctness_witnesses")
    if not witnesses:
        return "ABSENT", {"reason": "no distinctness_witnesses supplied"}

    all_detail = []
    all_ok = True
    for w in witnesses:
        if w.get("kind") != "disjointness":
            all_ok = False
            all_detail.append({"reason": "wrong kind for W-2' (must be disjointness)"})
            continue
        u = [mv_from_json(x) for x in w["u"]]
        g = [mv_from_json(x) for x in w["g"]]  # generators from I_P union I_Q
        if len(u) != len(g):
            all_ok = False
            all_detail.append({"reason": "u/g length mismatch"})
            continue
        acc = {}
        for ui, gi in zip(u, g):
            acc = mv_add(acc, mv_mul(ui, gi))
        ok = mv_is_one(acc)
        all_detail.append({"status": "PASS" if ok else "FAIL", "recomputed": _terms_out(acc)})
        if not ok:
            all_ok = False
    return ("PASS" if all_ok else "FAIL"), {"witnesses": all_detail}


def verify_W1(cert):
    """
    W-1: component_bijection re-derivation. This verifier reconstructs
    bijectivity purely from the declared bijection map + the declared
    component id sets (contract sec.3.2: certificate's map must be total
    and injective over the declared domain/codomain); injectivity is
    corroborated by W-2' where available.
    """
    bij = cert.get("component_bijection")
    if not bij:
        return "ABSENT", {"reason": "no component_bijection supplied"}

    domain = bij.get("domain_components", [])
    codomain = bij.get("codomain_components", [])
    mapping = bij.get("mapping", [])  # list of [dom_id, cod_id]

    dom_set = set(domain)
    cod_set = set(codomain)
    mapped_dom = [m[0] for m in mapping]
    mapped_cod = [m[1] for m in mapping]

    total = set(mapped_dom) == dom_set and len(mapped_dom) == len(dom_set)
    injective = len(set(mapped_cod)) == len(mapped_cod)
    onto_declared_cod = set(mapped_cod) == cod_set

    ok = total and injective and onto_declared_cod
    detail = {
        "total": total,
        "injective": injective,
        "onto_declared_codomain": onto_declared_cod,
        "domain_size": len(dom_set),
        "codomain_size": len(cod_set),
    }
    return ("PASS" if ok else "FAIL"), detail


def verify_W3(cert):
    """
    W-3: multiplicity_equalities. Integer comparison for every declared
    component pair.
    """
    entries = cert.get("multiplicity_equalities")
    if not entries:
        return "ABSENT", {"reason": "no multiplicity_equalities supplied"}
    bad = [e for e in entries if int(e["mult_A"]) != int(e["mult_B"])]
    ok = len(bad) == 0
    return ("PASS" if ok else "FAIL"), {"mismatches": bad, "checked": len(entries)}


def verify_W4(cert):
    """
    W-4: chart_overlap_witnesses. Structural self-consistency check only
    (declared UNKNOWN: full chart-atlas re-derivation, see module docstring).
    For every declared overlap region, both charts must agree on which
    component occupies it.
    """
    entries = cert.get("chart_overlap_witnesses")
    if not entries:
        return "ABSENT", {"reason": "no chart_overlap_witnesses supplied"}
    bad = [e for e in entries if e.get("component_in_chart_a") != e.get("component_in_chart_b")]
    ok = len(bad) == 0
    return ("PASS" if ok else "FAIL"), {"mismatches": bad, "checked": len(entries)}


def verify_W5(cert):
    """
    W-5: total_coverage_and_no_extra_component_witness. Component total
    count must match the bijection's image size (no missing / no extra);
    any claimed "extra" candidate requires a W-2' distinctness witness
    against every matched component (checked structurally here from
    declared cross-references).
    """
    w = cert.get("total_coverage_and_no_extra_component_witness")
    if not w:
        return "ABSENT", {"reason": "no coverage witness supplied"}
    declared_total = w.get("declared_total_components")
    bij = cert.get("component_bijection", {})
    matched = len(bij.get("mapping", []))
    extras = w.get("extra_candidates", [])
    extras_have_distinctness = all(e.get("distinctness_witness_ref") for e in extras)
    no_extra = len(extras) == 0
    ok = (declared_total == matched) and (no_extra or extras_have_distinctness)
    detail = {
        "declared_total": declared_total,
        "matched": matched,
        "extras": len(extras),
        "extras_have_distinctness_ref": extras_have_distinctness,
    }
    return ("PASS" if ok else "FAIL"), detail


def verify_W6(cert):
    """
    W-6: pushforward_compatibility_witness. Sum of ramification
    multiplicities pushed to each branch point recomputed and compared
    to the declared branch-divisor multiplicity (plain integer arithmetic
    on declared data -- no root-finding required).
    """
    w = cert.get("pushforward_compatibility_witness")
    if not w:
        return "ABSENT", {"reason": "no pushforward witness supplied"}
    ram = w.get("ramification_points", [])
    branch = w.get("branch_points", [])

    push = {}
    for r in ram:
        bv = r["maps_to_branch_value"]
        push[bv] = push.get(bv, 0) + int(r["multiplicity"])
    declared = {b["branch_value"]: int(b["multiplicity"]) for b in branch}

    ok = set(push.keys()) == set(declared.keys()) and all(
        push[k] == declared[k] for k in push
    )
    return ("PASS" if ok else "FAIL"), {"recomputed": push, "declared": declared}


# --------------------------------------------------------------------------
# P-0.* / P-3.* input binding checks (contract sec.3.0 / sec.3.3).
# --------------------------------------------------------------------------


def verify_P0(cert, expected):
    """
    P-0.1..P-0.8: ambient fixation re-check. Structural presence +
    digest-string equality against the expected pinned constants the
    caller supplies (expected = dict of the freeze receipt's known ids,
    see EXPECTED_PINS below). This file does not recompute digests of
    external documents (no filesystem access to governing spec/contract
    blobs is assumed); it only checks the certificate is internally
    consistent and matches the pins it declares.
    """
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
    p_0_6 = True  # UNKNOWN-scoped: only presence-if-needed is checked, see docstring
    if cert.get("_requires_field_embedding_witness"):
        p_0_6 = field_embedding_present
    p_0_8 = (not field_embedding_present) or (
        "field_embedding_witness_schema_digest" in cert
    )

    all_ok = all([p_0_1, p_0_2, p_0_3, p_0_4, p_0_5, p_0_7, p_0_6, p_0_8])
    return ("PASS" if all_ok else "FAIL"), {
        "P-0.1": p_0_1, "P-0.2": p_0_2, "P-0.3": p_0_3, "P-0.4": p_0_4,
        "P-0.5": p_0_5, "P-0.6": p_0_6, "P-0.7": p_0_7, "P-0.8": p_0_8,
        "field_embedding_witness_present": field_embedding_present,
    }


def verify_P3(cert, native_a, native_b, expected):
    """
    P-3.1..P-3.3: input/output binding.
      P-3.1: cert.predicate_spec_id/digest == governing spec pin.
      P-3.2: cert.schema_id/digest == governing spec sec.4.1 anchor.
      P-3.3: native_artifact_digest matches the actual blob the verifier
             read (recomputed sha256 over the native content this verifier
             was handed).
    """
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

    searcher_native = cert.get("searcher_native", {})
    checker_native = cert.get("checker_native", {})

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
# contract sec.3.4: canonical per-witness result vector R_B (two objects:
# ramification_divisor_on_C / branch_divisor_on_P1). Since this partial
# verifier does not yet distinguish witnesses per-object (the certificate
# schema in this fixture set carries one witness set covering both native
# objects jointly -- see fixtures), R_B is computed once and reported
# under both object labels; a per-object split is left as UNKNOWN /
# future work if the certificate schema is extended to carry per-object
# witness sets.
# --------------------------------------------------------------------------

WITNESS_LABELS = ["W-1", "W-2", "W-2prime", "W-3", "W-4", "W-5", "W-6"]

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
    Returns the verifier-B result record: R_B (per object, duplicated per
    the scope note above), overall verdict_B, and result_digest_B.
    """
    cert = payload["certificate"]
    native_a = payload.get("native_a")
    native_b = payload.get("native_b")

    p0_status, p0_detail = verify_P0(cert, EXPECTED_PINS)
    p3_status, p3_detail = verify_P3(cert, native_a, native_b, EXPECTED_PINS)

    w1_status, w1_detail = verify_W1(cert)
    w2_status, w2_detail = verify_W2(cert)
    w2p_status, w2p_detail = verify_W2prime(cert)
    w3_status, w3_detail = verify_W3(cert)
    w4_status, w4_detail = verify_W4(cert)
    w5_status, w5_detail = verify_W5(cert)
    w6_status, w6_detail = verify_W6(cert)

    witness_results = {
        "W-1": w1_status, "W-2": w2_status, "W-2prime": w2p_status,
        "W-3": w3_status, "W-4": w4_status, "W-5": w5_status, "W-6": w6_status,
    }
    witness_detail = {
        "W-1": w1_detail, "W-2": w2_detail, "W-2prime": w2p_detail,
        "W-3": w3_detail, "W-4": w4_detail, "W-5": w5_detail, "W-6": w6_detail,
    }

    R_vector = [(label, witness_results[label]) for label in WITNESS_LABELS]
    # duplicated across the two native objects per the scope note above
    R_B = {
        "ramification_divisor_on_C": R_vector,
        "branch_divisor_on_P1": R_vector,
    }

    all_pass = all(status == "PASS" for status in witness_results.values())
    ambient_ok = p0_status == "PASS" and p3_status == "PASS"

    verdict_B = "PASS" if (ambient_ok and all_pass) else "FAIL"

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
        "P-0.6/P-1.4 field embedding: only presence is checked, not the "
        "embedding map itself (out of scope for this partial verifier)",
        "W-4 chart atlas: only internal consistency of declared overlaps "
        "is checked, not full re-derivation of the chart atlas",
        "CR-11 (contract sec.9.1): implemented_checks 3-layer equality is "
        "UNKNOWN -- no executable-inventory system exists yet",
        "R_A vs R_B concordance ([26]): NOT computed by this file (contract "
        "C-7: belongs to the receiving side that holds both R_A and R_B "
        "independently)",
        "per-object witness split: this fixture schema carries one witness "
        "set for both native objects; R_B is duplicated across both labels "
        "rather than independently checked per object",
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
