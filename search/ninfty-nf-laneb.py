#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-nf-laneb.py

Lane B (python / checker runtime) independent normal-form (NF) calculator.
Governing design: docs/notes/lanea_native_semantics_v1.md §4.1 (Theorem A/B,
NF schema, N-1..N-5), adopted by Sol 便94 §4 (F94-4.2), frozen by 裁定311.

INDEPENDENCE DISCIPLINE: this module builds ONLY on lane B's own files
(search/ninfty-checker.py's run_checker for the mint-gate verdict chain,
search/ninfty-checker-native.py's point-level from-scratch construction for
the divisor data) -- it never reads or imports lane A's
search/ninfty-searcher-v2.mjs. NF is a FORMAL CONTRACT (spec §4.1), not a
shared implementation: lane A computes the same NF shape independently in
search/ninfty-searcher-v2.mjs's computeNormalFormLaneA, from its own 3-loci
data, with no code shared between the two files. Comparison of the two NF
outputs belongs to the THIRD script, search/ninfty-nf-crosscheck.py, which
this module also does not import.

MINT GATE (P94-4.1 / 裁定311 是正 R-2): NF is minted (status="PRESENT") only
when lane B's own decision chain (run_checker's precondition E-1..E-4 checks,
E-5 derivation, T-1, T-2/(60.5)) reaches stage=None ("fully passed", lane B's
equivalent of lane A's verdict=ACCEPT). A REJECT-class stage yields
status="ABSENT" (no divisor-shaped data exists for a REJECTed candidate,
裁定309's beta finding). An INTEGRITY_STOP-class stage yields
status="INTEGRITY_STOP" (a theorem-forced identity broke after prerequisites
held -- input-inconsistent, not merely rejected).

CONVENTION (Sol 便94 F94-4.2, -C-square ambiguity): effective divisors are
kept as (monic polynomial generator, multiplicity) pairs WITHOUT further
irreducible factorization over Q -- v^2+C is always ONE degree-2 component
(coefficient 2), even when -C happens to be a rational square. This module
never decomposes further, matching lane A's stated convention.

runtime = python + sympy (exact algebra only, same discipline as
ninfty-checker-native.py: no floating point).
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
import sys
import argparse
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
X = sp.symbols("x")

NF_SCHEMA_ID = "mb/ninfty-nf/v1"


def _load_module(filename, alias):
    path = os.path.join(HERE, filename)
    spec = importlib.util.spec_from_file_location(alias, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_checker = None
_checker_native = None


def _lane_b_modules():
    global _checker, _checker_native
    if _checker is None:
        _checker = _load_module("ninfty-checker.py", "ninfty_checker_x_nf")
    if _checker_native is None:
        _checker_native = _load_module("ninfty-checker-native.py", "ninfty_checker_native_x_nf")
    return _checker, _checker_native


def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def _rat_str(x):
    return str(sp.nsimplify(x))


def compute_normal_form_lane_b(candidate):
    """
    candidate = {"a": [...], "p": [...], "f6": [...],
                 "divisor_orientation_attested": bool|None, ...}
    Returns the lane-B NF report dict: {lane, nf_schema_id, status,
    decision_stage, primary_reason_code, nf, nf_digest}.
    """
    checker, checker_native = _lane_b_modules()

    # mint-gate verdict chain: reuse lane B's OWN decision machinery
    # (run_checker), same discipline as lane A's evaluateDecisionLane call
    # inside computeNormalFormLaneA -- both sides gate NF on their own
    # lane's full prerequisite/theorem-identity chain, never on a shared
    # third implementation.
    decision_candidate = dict(candidate)
    decision_candidate["skip_native_construction"] = True
    decision = checker.run_checker(decision_candidate)
    stage = decision.get("stage")

    if stage == "REJECT":
        return {
            "lane": "B",
            "nf_schema_id": NF_SCHEMA_ID,
            "status": "ABSENT",
            "decision_stage": stage,
            "primary_reason_code": decision.get("primary_reason_code"),
            "reason": "prerequisite chain (degree/E-1..E-4/T-1) not satisfied -- no divisor-shaped data exists to mint (裁定309 beta finding).",
            "nf": None,
            "nf_digest": None,
        }
    if stage == "INTEGRITY_STOP":
        return {
            "lane": "B",
            "nf_schema_id": NF_SCHEMA_ID,
            "status": "INTEGRITY_STOP",
            "decision_stage": stage,
            "primary_reason_code": decision.get("primary_reason_code"),
            "reason": "prerequisites passed but a theorem-forced identity ((60.5)/E-6/E-5-orientation) broke -- input is internally inconsistent, not merely rejected.",
            "nf": None,
            "nf_digest": None,
        }

    # stage is None: full prerequisite chain passed. Build the divisor data
    # from scratch via checker_native's point-level construction (independent
    # sympy gcd/roots/series code, distinct from checker.py's own Euclid/Yun
    # implementation and from lane A's mjs implementation).
    a = checker_native.poly_from_coeffs(candidate["a"])
    p = checker_native.poly_from_coeffs(candidate["p"])
    f6 = checker_native.poly_from_coeffs(candidate["f6"])

    C = sp.nsimplify(sp.expand(a ** 2 - f6 * p ** 2))
    if not C.is_constant() or sp.simplify(C) == 0:
        # theorem guarantees this cannot happen once stage is None; report
        # honestly as an anomaly rather than silently minting bad data.
        return {
            "lane": "B",
            "nf_schema_id": NF_SCHEMA_ID,
            "status": "INTEGRITY_STOP",
            "decision_stage": stage,
            "primary_reason_code": "nf-lane-b-pell-anomaly-after-stage-none",
            "reason": "run_checker reported stage=None but a^2-f6*p^2 is not a nonzero constant -- internal inconsistency.",
            "nf": None,
            "nf_digest": None,
        }

    fin_status, fin_detail = checker_native._finite_ramification_points(a, p, C)
    if fin_status != "ok":
        return {
            "lane": "B",
            "nf_schema_id": NF_SCHEMA_ID,
            "status": "INTEGRITY_STOP",
            "decision_stage": stage,
            "primary_reason_code": "nf-lane-b-finite-construction-anomaly-after-stage-none",
            "reason": f"run_checker reported stage=None but finite ramification construction failed: {fin_status}",
            "nf": None,
            "nf_digest": None,
        }
    d_monic_expr = sp.sympify(fin_detail["d_expr"])

    inf = checker_native._infinity_local_orders(candidate["a"], candidate["p"], candidate["f6"])
    matches_or = (
        inf.get("status") == "ok"
        and inf["plus_branch"]["local_order_of_mu"] == -5
        and inf["minus_branch"]["local_order_of_mu"] == 5
    )
    if not matches_or:
        return {
            "lane": "B",
            "nf_schema_id": NF_SCHEMA_ID,
            "status": "INTEGRITY_STOP",
            "decision_stage": stage,
            "primary_reason_code": "nf-lane-b-orientation-anomaly-after-stage-none",
            "reason": "run_checker reported stage=None but the computed infinity local orders do not match (Or) (Prop E5-D) -- internal inconsistency.",
            "nf": None,
            "nf_digest": None,
        }

    p_sqfree = bool(sp.discriminant(sp.Poly(p, X).as_expr(), X) != 0) if sp.degree(p, X) >= 1 else True
    f6_sqfree = bool(sp.discriminant(sp.Poly(f6, X).as_expr(), X) != 0)
    gcd_p_f6 = sp.gcd(p, f6)
    gcd_p_f6_degree = int(sp.degree(sp.Poly(gcd_p_f6, X), X)) if gcd_p_f6 != 0 else 0
    p_f6_coprime = (gcd_p_f6_degree == 0)

    d_monic_poly = sp.Poly(d_monic_expr, X)
    d_coeffs_low_first = [_rat_str(c) for c in reversed(d_monic_poly.all_coeffs())]
    p_monic_expr = sp.expand(p / sp.Poly(p, X).LC())
    p_monic_coeffs = [_rat_str(c) for c in reversed(sp.Poly(p_monic_expr, X).all_coeffs())]
    f6_monic_expr = sp.expand(f6 / sp.Poly(f6, X).LC())
    f6_monic_coeffs = [_rat_str(c) for c in reversed(sp.Poly(f6_monic_expr, X).all_coeffs())]

    nf = {
        "ram_finite": {
            "variable": "x",
            "ideal_generator": d_coeffs_low_first,
            "pullback": "pi^*",
            "reduced": True,
            "coefficient": 1,
        },
        "ram_infinite": [
            {"point": "inf_plus", "e": 5, "coefficient": 4},
            {"point": "inf_minus", "e": 5, "coefficient": 4},
        ],
        "branch": {
            "variable": "v",
            "components": [
                {"ideal_generator": ["0", "1"], "coefficient": 4},
                {"ideal_generator": [_rat_str(C), "0", "1"], "coefficient": 2},
                {"at_infinity": True, "coefficient": 4},
            ],
        },
        "non_ramification_certificates": {
            "p_locus": {
                "generator": p_monic_coeffs,
                "squarefree": bool(p_sqfree),
                "coprime_to_f6": {
                    "witness_gcd_degree": gcd_p_f6_degree,
                    "coprime": bool(p_f6_coprime),
                },
            },
            "w_locus": {
                "generator": f6_monic_coeffs,
                "squarefree": bool(f6_sqfree),
                "coprime_to_p": {
                    "witness_gcd_degree": gcd_p_f6_degree,
                    "coprime": bool(p_f6_coprime),
                },
            },
            "claim": "contributes 0 to R_mu (Theorem B cancellation)",
        },
    }
    nf_digest = sha256_of(nf)

    return {
        "lane": "B",
        "nf_schema_id": NF_SCHEMA_ID,
        "status": "PRESENT",
        "decision_stage": stage,
        "nf": nf,
        "nf_digest": nf_digest,
    }


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("candidate_json", help="path to candidate JSON, or '-' for stdin")
    args = ap.parse_args(argv)
    if args.candidate_json == "-":
        candidate = json.load(sys.stdin)
    else:
        with open(args.candidate_json, "r", encoding="utf-8") as f:
            candidate = json.load(f)
    result = compute_normal_form_lane_b(candidate)
    print(canonical_serialize(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
