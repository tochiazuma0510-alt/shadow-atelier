#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-nf-crosscheck.py

THIRD script (照合器 / crosscheck, not 探索器): judges the N-1..N-5 equalities
from docs/notes/lanea_native_semantics_v1.md §4.1 between lane A's NF
(search/ninfty-searcher-v2.mjs computeNormalFormLaneA, invoked via the
node CLI wrapper search/ninfty-nf-lanea-cli.mjs) and lane B's NF
(search/ninfty-nf-laneb.py compute_normal_form_lane_b).

INDEPENDENCE DISCIPLINE: this script imports NEITHER lane's implementation.
It only invokes each lane's CLI entry point as a SEPARATE OS process and
parses the JSON each one prints to stdout. It has no shared helper with
either lane's NF construction code -- the only thing shared is the NF
SCHEMA (a data contract, spec §4.1), which is exactly what "cross-checked"
is licensed to compare (per CLAUDE.md's 探索器/照合器 separation discipline
and the note's own §4 framing: "NF は形式契約であって共有実装ではない").

"cross-checked", not "verified": both sides are machine computations, not
Lean-formalized proofs (per project convention, verified is reserved for Lean).

Verdict logic:
  * If either lane reports status != "PRESENT" (ABSENT / INTEGRITY_STOP), no
    NF exists to compare on that side. The two statuses are compared for
    DECISION-LANE CONCORDANCE (do both lanes agree the candidate is not
    mintable, and for the same class of reason -- ABSENT vs ABSENT,
    INTEGRITY_STOP vs INTEGRITY_STOP) -- N-1..N-5 are reported ABSENT
    (not run), never silently treated as PASS.
  * If both report PRESENT, N-1..N-5 are checked structurally, exactly as
    specified (monic-normalized exact rational coefficient comparison,
    Q-exact throughout -- no floating point, no resultants).

Run: python search/ninfty-nf-crosscheck.py <candidate.json>
Prints a JSON report to stdout. Exit code 0 always (this is a report, per
the same convention as checker_native_crosscheck.py); the report's own
"all_pass" / "concordant" fields carry the verdict.
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def _rat(s):
    s = str(s)
    if "/" in s:
        n, d = s.split("/")
        return Fraction(int(n), int(d))
    return Fraction(int(s))


def run_lane_a(candidate_path):
    cli = os.path.join(HERE, "ninfty-nf-lanea-cli.mjs")
    out = subprocess.run(["node", cli, candidate_path], capture_output=True, encoding="utf-8", check=True)
    return json.loads(out.stdout)


def run_lane_b(candidate_path):
    script = os.path.join(HERE, "ninfty-nf-laneb.py")
    out = subprocess.run([sys.executable, script, candidate_path], capture_output=True, encoding="utf-8", check=True)
    return json.loads(out.stdout)


def _poly_eq(coeffs_a, coeffs_b):
    """low-degree-first coefficient lists, exact Fraction comparison, both
    already required to be monic by NF §4.1 (no independent renormalization
    performed here -- a non-monic generator from either lane is itself a
    reportable mismatch, not silently fixed)."""
    fa = [_rat(c) for c in coeffs_a]
    fb = [_rat(c) for c in coeffs_b]
    return fa == fb


def check_n1_n5(nf_a, nf_b):
    """Returns dict of the five equality checks, spec §4.1 N-1..N-5."""
    out = {}

    # N-1: ram_finite.ideal_generator monic-coefficient exact match.
    rf_a, rf_b = nf_a["ram_finite"], nf_b["ram_finite"]
    n1 = _poly_eq(rf_a["ideal_generator"], rf_b["ideal_generator"])
    out["N-1"] = {"pass": n1, "lane_a_generator": rf_a["ideal_generator"], "lane_b_generator": rf_b["ideal_generator"]}

    # N-2: ram_finite.coefficient equal, and 2*deg(gen)*coefficient == 4.
    deg_a = len(rf_a["ideal_generator"]) - 1
    deg_b = len(rf_b["ideal_generator"]) - 1
    coef_eq = rf_a["coefficient"] == rf_b["coefficient"]
    degree_identity_a = 2 * deg_a * rf_a["coefficient"] == 4
    degree_identity_b = 2 * deg_b * rf_b["coefficient"] == 4
    n2 = coef_eq and degree_identity_a and degree_identity_b
    out["N-2"] = {"pass": n2, "coefficient_equal": coef_eq,
                  "degree_identity_lane_a": degree_identity_a, "degree_identity_lane_b": degree_identity_b}

    # N-3: ram_infinite == {(inf_+,4),(inf_-,4)} on both lanes.
    def _inf_set(ram_inf):
        return {(e["point"].replace("_plus", "_+").replace("_minus", "_-"), e["e"], e["coefficient"]) for e in ram_inf}
    expect = {("inf_+", 5, 4), ("inf_-", 5, 4)}
    ia, ib = _inf_set(nf_a["ram_infinite"]), _inf_set(nf_b["ram_infinite"])
    n3 = (ia == expect) and (ib == expect)
    out["N-3"] = {"pass": n3, "lane_a": sorted(str(x) for x in ia), "lane_b": sorted(str(x) for x in ib)}

    # N-4: branch components (ideal_generator, coefficient) exact match per
    # component (matched by shape: linear v / quadratic v^2+C / at_infinity),
    # plus sum(deg(gen)*coefficient) + at_infinity.coefficient == 12.
    def _classify(components):
        lin = [c for c in components if not c.get("at_infinity") and len(c["ideal_generator"]) == 2]
        quad = [c for c in components if not c.get("at_infinity") and len(c["ideal_generator"]) == 3]
        inf = [c for c in components if c.get("at_infinity")]
        return lin, quad, inf

    lin_a, quad_a, inf_a = _classify(nf_a["branch"]["components"])
    lin_b, quad_b, inf_b = _classify(nf_b["branch"]["components"])
    shape_ok = len(lin_a) == 1 and len(quad_a) == 1 and len(inf_a) == 1 and \
               len(lin_b) == 1 and len(quad_b) == 1 and len(inf_b) == 1
    n4 = shape_ok
    if shape_ok:
        lin_match = _poly_eq(lin_a[0]["ideal_generator"], lin_b[0]["ideal_generator"]) and lin_a[0]["coefficient"] == lin_b[0]["coefficient"]
        quad_match = _poly_eq(quad_a[0]["ideal_generator"], quad_b[0]["ideal_generator"]) and quad_a[0]["coefficient"] == quad_b[0]["coefficient"]
        inf_match = inf_a[0]["coefficient"] == inf_b[0]["coefficient"]
        n4 = lin_match and quad_match and inf_match
        deg_sum_a = 1 * lin_a[0]["coefficient"] + 2 * quad_a[0]["coefficient"] + inf_a[0]["coefficient"]
        deg_sum_b = 1 * lin_b[0]["coefficient"] + 2 * quad_b[0]["coefficient"] + inf_b[0]["coefficient"]
        n4 = n4 and (deg_sum_a == 12) and (deg_sum_b == 12)
        out["N-4"] = {"pass": n4, "shape_ok": shape_ok, "lin_match": lin_match, "quad_match": quad_match,
                      "inf_match": inf_match, "degree_sum_lane_a": deg_sum_a, "degree_sum_lane_b": deg_sum_b}
    else:
        out["N-4"] = {"pass": False, "shape_ok": shape_ok, "reason": "branch component shape (1 linear + 1 quadratic + 1 at_infinity) not found on both lanes -- possible -C-square split-vs-undecomposed convention mismatch (Sol 便94 F94-4.2)"}

    # N-5: non_ramification_certificates' two generators match as ideals
    # (monic exact match, same convention as N-1).
    nrc_a, nrc_b = nf_a["non_ramification_certificates"], nf_b["non_ramification_certificates"]
    p_match = _poly_eq(nrc_a["p_locus"]["generator"], nrc_b["p_locus"]["generator"])
    w_match = _poly_eq(nrc_a["w_locus"]["generator"], nrc_b["w_locus"]["generator"])
    n5 = p_match and w_match
    out["N-5"] = {"pass": n5, "p_locus_match": p_match, "w_locus_match": w_match}

    return out


def main(argv):
    if len(argv) != 2:
        print("usage: python ninfty-nf-crosscheck.py <candidate.json>", file=sys.stderr)
        return 2
    candidate_path = argv[1]

    nf_a_report = run_lane_a(candidate_path)
    nf_b_report = run_lane_b(candidate_path)

    report = {
        "role": "ninfty-nf-crosscheck (third script, 照合器 -- imports neither lane's implementation)",
        "candidate_ref": candidate_path,
        "lane_a_status": nf_a_report["status"],
        "lane_b_status": nf_b_report["status"],
    }

    if nf_a_report["status"] != "PRESENT" or nf_b_report["status"] != "PRESENT":
        report["decision_lane_concordance"] = (nf_a_report["status"] == nf_b_report["status"])
        report["n1_n5"] = "ABSENT (not run -- at least one lane did not mint an NF)"
        report["all_pass"] = None
        report["lane_a_full"] = nf_a_report
        report["lane_b_full"] = nf_b_report
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True))
        return 0

    n1_n5 = check_n1_n5(nf_a_report["nf"], nf_b_report["nf"])
    all_pass = all(v["pass"] for v in n1_n5.values())
    report["digest_match"] = (nf_a_report["nf_digest"] == nf_b_report["nf_digest"])
    report["n1_n5"] = n1_n5
    report["all_pass"] = all_pass
    report["cross_checked_not_verified"] = True
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
