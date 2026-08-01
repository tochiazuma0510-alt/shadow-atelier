#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/checker_native_crosscheck.py

Field-by-field crosscheck of search/ninfty-checker-native.py's from-scratch
checker_native construction against lane A's ALREADY-PRODUCED native
artifact output (a data file, not lane A's code). This script is
deliberately SEPARATE from both search/ninfty-checker.py and
search/ninfty-checker-native.py -- it is the crosscheck/照合器, not the
探索器/generator. It does not import any lane A source module; it only
reads lane A's JSON output artifact(s) already committed to the repo.

Per the commander's brief (2026-08-01), this is a lightweight, honest
diff -- NOT the full D-2 divisor_equality_certificate/witness pipeline
(search/ninfty-verifier-b.py already owns that, at a much larger scope,
and is out of this task).

Inputs used (both already exist in the repo, machine-produced, not typed
by hand):
  * candidate:        search/certs/ep_first_run/beta_candidate.json
  * lane A's native:  search/certs/ep_first_run/beta_searcher_native.json
  * this checker_native's own construction, run fresh here on the same
    candidate coefficients.

Finding (recorded, not silently smoothed over): the ONLY genuine (i.e.
actually produced by lane A's real EP export pipeline, not a hand-built
"explicitly-labeled stand-in" toy fixture -- see search/fixtures/ninfty/
gen_native_fixtures.py's own docstring) lane-A native artifact available
in this repo is for the beta candidate, which is REJECTED at
a-partition-mismatch (search/certs/ep_first_run/beta_lanea_decision.json)
-- i.e. rootpart(a) != [2,2,1], T-1 does NOT hold for this candidate. This
checker_native's own from-scratch finite-point construction ALSO reports
this candidate as a degeneracy (gcd(a,a') has degree 1, not 2 -- see
search/ninfty-checker-native.py's own run below), so the two lanes AGREE
on the qualitative fact "this candidate has no genuine [2,2,1] structure".

Beyond that qualitative agreement, however, the two artifacts are NOT
directly comparable field-by-field: lane A's searcher_native represents
ramification_divisor_on_C as THREE named ideal-loci ("a-pair-locus" =
gcd(a,a'), "p-locus" = p(x) itself, "weierstrass-locus" = f6(x) itself),
with NO explicit points, NO infinity points, and no dependence on T-1
actually holding -- it looks like a general-purpose locus catalog usable
regardless of accept/reject status, not literally "the support of R_mu"
in the sense of spec sec.1.8. This checker_native instead constructs
explicit Qbar points (roots of gcd(a,a'), plus the two points at infinity
via a Puiseux-order computation) that ARE meant to be R_mu's actual point
support for a genuine [2,2,1] candidate. Reconciling these two
representations (are lane A's three loci meant to jointly cover R_mu's
support in some other encoding? do they also carry the infinity
contribution somewhere this script did not find?) requires either reading
lane A's implementation (explicitly out of scope for the checker_native
side of this task) or a mathematician/commander-level judgment call. This
script reports the structural mismatch explicitly rather than attempting
a guessed semantic translation.

No other genuine (non-toy) lane-A native artifact for a PASSING [2,2,1]
candidate exists in this repo as of 20260801, so a same-shape crosscheck
on a genuine ACCEPT case could not be run here.

Run: python search/checker_native_crosscheck.py
Prints a JSON report to stdout; exit code is always 0 (this is a report,
not a pass/fail gate -- a structural mismatch is itself the recorded
finding, per the commander's brief: "不一致 = そのまま記録して停止=発見").
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EP_DIR = os.path.join(HERE, "certs", "ep_first_run")


def _load_native_module():
    path = os.path.join(HERE, "ninfty-checker-native.py")
    spec = importlib.util.spec_from_file_location("ninfty_checker_native_x", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_of_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    candidate_path = os.path.join(EP_DIR, "beta_candidate.json")
    lanea_native_path = os.path.join(EP_DIR, "beta_searcher_native.json")
    lanea_decision_path = os.path.join(EP_DIR, "beta_lanea_decision.json")

    with open(candidate_path, "r", encoding="utf-8") as f:
        candidate = json.load(f)
    with open(lanea_native_path, "r", encoding="utf-8") as f:
        lanea_native = json.load(f)
    with open(lanea_decision_path, "r", encoding="utf-8") as f:
        lanea_decision = json.load(f)

    mod = _load_native_module()
    mine = mod.construct_checker_native(candidate["a"], candidate["p"], candidate["f6"])

    lanea_loci = [c["locus_type"] for c in lanea_native["ramification_divisor_on_C_ref"]["components"]]
    lanea_a_pair_generator = None
    for c in lanea_native["ramification_divisor_on_C_ref"]["components"]:
        if c["locus_type"] == "a-pair-locus":
            lanea_a_pair_generator = c["ideal_generator"]

    my_finite_status = mine.get("diagnostics", {}).get("finite_construction_status")
    my_gcd_expr = None
    if mine["status"] != "ok" and "finite_detail" in mine.get("diagnostics", {}):
        my_gcd_expr = mine["diagnostics"]["finite_detail"].get("d_expr")

    # symbolic (not string-literal) comparison: parse lane A's ideal_generator
    # (low-degree-first coefficient list, same convention as candidate a/p/f6)
    # as a polynomial and compare against my computed gcd(a,a') up to a
    # nonzero scalar (both are meant to generate the same ideal).
    import sympy as sp
    x = sp.symbols("x")
    a_pair_matches_my_gcd = False
    if lanea_a_pair_generator is not None and my_gcd_expr is not None:
        lanea_poly = sum(sp.Rational(c) * x ** i for i, c in enumerate(lanea_a_pair_generator))
        mine_poly = sp.sympify(my_gcd_expr)
        # same ideal <=> proportional (both nonzero, low degree here)
        ratio_ok = False
        try:
            q, r = sp.div(lanea_poly, mine_poly, x)
            ratio_ok = (sp.expand(r) == 0) and sp.degree(sp.Poly(q, x), x) == 0
        except Exception:
            ratio_ok = False
        a_pair_matches_my_gcd = ratio_ok

    report = {
        "role": "checker_native_crosscheck (independent照合器, reads artifacts only, no lane A code import)",
        "candidate_ref": "search/certs/ep_first_run/beta_candidate.json",
        "candidate_sha256": sha256_of_file(candidate_path),
        "lanea_native_ref": "search/certs/ep_first_run/beta_searcher_native.json",
        "lanea_native_sha256": sha256_of_file(lanea_native_path),
        "lanea_native_artifact_digest_declared": lanea_native.get("native_artifact_digest"),
        "lanea_decision": lanea_decision,
        "qualitative_agreement": {
            "lanea_decision_is_reject_a_partition_mismatch": lanea_decision.get("primary_reason_code") == "a-partition-mismatch",
            "mine_reports_gcd_degree_not_2": my_finite_status == "gcd-degree-not-2",
            "agree_no_genuine_2_2_1_structure": (
                lanea_decision.get("primary_reason_code") == "a-partition-mismatch"
                and my_finite_status == "gcd-degree-not-2"
            ),
        },
        "structural_field_comparison": {
            "lanea_ramification_divisor_on_C_ref_locus_types": lanea_loci,
            "lanea_a_pair_locus_ideal_generator_low_deg_first": lanea_a_pair_generator,
            "mine_gcd_a_ap_expr": my_gcd_expr,
            "mine_construction_status": mine["status"],
            "a_pair_locus_field_agrees_with_my_gcd(as-ideal, symbolic-div-check)": a_pair_matches_my_gcd,
            "note": ("lane A represents ramification_divisor_on_C as 3 named ideal-loci "
                     "(a-pair-locus/p-locus/weierstrass-locus), independent of whether T-1 "
                     "holds, and with NO infinity points; this checker_native represents it "
                     "as explicit Qbar points (finite +-s branch points + 2 infinity points) "
                     "and only produces output when T-1's gcd(a,a') has degree exactly 2. "
                     "The two schemas are NOT directly field-comparable beyond the qualitative "
                     "a-pair-locus-degree fact checked above. See this module's docstring for "
                     "the full finding -- reported as an open reconciliation question, not "
                     "silently resolved."),
        },
        "verdict": "STRUCTURAL_MISMATCH_RECORDED_NOT_RESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
