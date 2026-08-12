#!/usr/bin/env python3
"""
search/r13_p1_tier2_gha.py -- [P1] Tier 2 (remaining 4 layers, disc-product route) per 裁定1002,
docs/notes/w9_laneB_elimination_v1.md §4.

Layer (0,9) was found EMPTY by lane B (Gröbner basis = {1}, run 31578468586, confirmed
independently by hand-derivation in this session: substituting the E1/E2 triangular solutions
reduces the coupling equations to gp3^k+gm3^k=0 for k=5,6,7,8 (forcing gp3=gm3=0 given the k=6,8
even-power constraints) contradicting the k=9 equation gp3^9+gm3^9=-2). This script handles the
remaining 4 layers: (2,7), (4,5), (6,3), (8,1) -- i.e. all (o1,o2) with o1+o2=9, o1 even, o2 odd,
o1 in {2,4,6,8} (o1=0 already done by lane B).

Method (§4): R1 := P-2w^9, R2 := P+2w^9 (P(w;a,b) reconstructed from the g0..g7(a,b) solution in
search/certs/r13_p1_1pp_k2_v1_20260812.json, i.e. c9=2 fixed and c0..c8 read off the same target
polynomial's low-degree coefficients). ALL layers require disc_w(R1)=0 OR disc_w(R2)=0 (some
double root in R1 or R2) -- so:
  branch I:  resultant_b( gamma(a,b), disc_w(R1)(a,b) ) = 0  (eliminate b, univariate in a)
             deg R1 <= 8 -- SMALLER Sylvester matrix, tried FIRST per the note's own recommendation.
  branch II: resultant_b( gamma(a,b), disc_w(R2)(a,b) ) = 0  (deg R2 = 9)
gamma(a,b) is the step1 curve equation (c9(a,b)-2=0, already in the r13_p1_1pp_k2_v1 cert as
"ninth_equation").

For each candidate root a0 (exact algebraic number, sympy CRootOf / minimal polynomial), the
corresponding b0 is recovered from gamma(a0,b)=0 (solving in b), then Delta=R1*R2 at (a0,b0) is
squarefree-factored and the ODD-multiplicity root count is checked against 9 (genus-4 sieve, (B5)
in the lane B note's own language -- NOT the squarefree-part degree).

Time-boxed (55min internal SIGALRM), writes partial results if not finished; branch I is attempted
first and its own partial completion is preserved even if branch II runs out of budget.
"""
import json
import signal
import time

import sympy as sp

CERT_IN = "search/certs/r13_p1_1pp_k2_v1_20260812.json"
CERT_OUT = "ci/out/r13_p1_tier2_result.json"
TIME_BUDGET_SECONDS = 55 * 60


class TimeBudgetExceeded(Exception):
    pass


def _alarm_handler(signum, frame):
    raise TimeBudgetExceeded()


def build_P_and_gamma():
    """Reconstruct P(w;a,b) (c9=2 fixed, c0..c8 from the target polynomial's own coefficients)
    and gamma(a,b) (the step1 curve, c9(a,b)-2=0) -- SAME derivation as r13_p1_1pp_k2_v1.py,
    recomputed here (not re-imported) so this script is self-contained for the GHA job."""
    w = sp.symbols("w")
    a, b = sp.symbols("a b")
    gsyms = sp.symbols("g0 g1 g2 g3 g4 g5 g6 g7")

    gpoly = w ** 8 + sum(gsyms[i] * w ** i for i in range(8))
    target = sp.expand((w - a) * (w - b) * gpoly ** 2)
    target_poly = sp.Poly(target, w)
    coeffs = target_poly.all_coeffs()

    order = [gsyms[7], gsyms[6], gsyms[5], gsyms[4], gsyms[3], gsyms[2], gsyms[1], gsyms[0]]
    subs = {}
    for i in range(8):
        idx = 18 - (17 - i)
        eq = coeffs[idx].subs(subs)
        var = order[i]
        sol = sp.solve(sp.Eq(eq, 0), var)
        subs[var] = sp.simplify(sol[0])

    target_sub = sp.expand(target_poly.as_expr().subs(subs))
    target_sub_poly = sp.Poly(target_sub, w)
    tcoeffs = target_sub_poly.all_coeffs()  # index 0 = w^18 ... index 18 = w^0

    c = {}
    for j in range(0, 10):  # c_0..c_9
        idx = 18 - j
        c[j] = sp.simplify(tcoeffs[idx])

    gamma = sp.expand(c[9] - 2)  # the step1 curve equation
    P = sum(c[j] * w ** j for j in range(0, 10))
    return w, a, b, P, gamma, c


def main():
    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    use_alarm = hasattr(signal, "SIGALRM")
    if use_alarm:
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.alarm(TIME_BUDGET_SECONDS)

    out = {
        "schema": "r13-p1-tier2/v1",
        "generated_by": {"tool": "python/sympy", "script": "search/r13_p1_tier2_gha.py",
                          "order": "裁定1002 [P1] Tier2 / docs/notes/w9_laneB_elimination_v1.md §4"},
        "layer_0_9_status": "EMPTY (lane B, run 31578468586, Groebner basis = {1}, cross-checked "
                             "by hand-derivation this session -- see script docstring)",
        "layers_this_script_covers": ["(2,7)", "(4,5)", "(6,3)", "(8,1)"],
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "u_touched": False,
        "c_touched": False,
        "d_no_interpretation": "machine values only; verdict は司令塔",
        "branch_I": {"attempted": False}, "branch_II": {"attempted": False},
        "status": "INCOMPLETE",
    }

    try:
        record("reconstructing P(w;a,b) and gamma(a,b)...")
        w, a, b, P, gamma, c = build_P_and_gamma()
        record(f"gamma(a,b) degree check: {sp.total_degree(gamma)} (expect ~9)")
        R1 = sp.expand(P - 2 * w ** 9)
        R2 = sp.expand(P + 2 * w ** 9)
        out["R1_degree_w"] = sp.degree(R1, w)
        out["R2_degree_w"] = sp.degree(R2, w)
        record(f"deg_w R1={out['R1_degree_w']} (expect <=8) deg_w R2={out['R2_degree_w']} (expect 9)")

        record("computing disc_w(R1) (branch I, smaller Sylvester matrix)...")
        discR1 = sp.discriminant(sp.Poly(R1, w))
        discR1 = sp.expand(discR1)
        record("disc_w(R1) computed")
        out["branch_I"]["attempted"] = True
        out["branch_I"]["discR1_num_terms"] = len(sp.Add.make_args(discR1))

        record("computing resultant_b(gamma, discR1) (branch I elimination)...")
        res_I = sp.resultant(gamma, discR1, b)
        res_I = sp.factor(res_I)
        record("resultant (branch I) computed")
        out["branch_I"]["resultant_in_a"] = str(res_I)

        record("solving branch I resultant for candidate a values (exact)...")
        a_candidates_I = sp.solve(sp.Eq(res_I, 0), a)
        out["branch_I"]["a_candidate_count"] = len(a_candidates_I)
        out["branch_I"]["a_candidates"] = [str(x) for x in a_candidates_I]
        record(f"branch I: {len(a_candidates_I)} candidate a-values found")

        branch_I_results = []
        for a0 in a_candidates_I:
            entry = {"a": str(a0)}
            try:
                b_sols = sp.solve(sp.Eq(gamma.subs(a, a0), 0), b)
                entry["b_candidates"] = [str(x) for x in b_sols]
                layer_hits = []
                for b0 in b_sols:
                    Delta0 = sp.expand((R1.subs({a: a0, b: b0})) * (R2.subs({a: a0, b: b0})))
                    Delta0_poly = sp.Poly(Delta0, w)
                    if Delta0_poly.degree() <= 0:
                        continue
                    _, sqf = sp.sqf_list(Delta0_poly)
                    odd_root_count = sum(sp.degree(f, w) for f, m in sqf if m % 2 == 1)
                    layer_hits.append({"b": str(b0), "delta_degree": Delta0_poly.degree(),
                                        "odd_multiplicity_root_count": odd_root_count,
                                        "genus4_check": (odd_root_count == 9)})
                entry["delta_checks"] = layer_hits
            except Exception as e:
                entry["error"] = f"{type(e).__name__}: {e}"
            branch_I_results.append(entry)
        out["branch_I"]["results"] = branch_I_results
        out["branch_I"]["completed"] = True
        record("branch I complete")

        record("computing disc_w(R2) (branch II)...")
        discR2 = sp.expand(sp.discriminant(sp.Poly(R2, w)))
        out["branch_II"]["attempted"] = True
        record("disc_w(R2) computed")

        record("computing resultant_b(gamma, discR2) (branch II elimination)...")
        res_II = sp.factor(sp.resultant(gamma, discR2, b))
        out["branch_II"]["resultant_in_a"] = str(res_II)
        a_candidates_II = sp.solve(sp.Eq(res_II, 0), a)
        out["branch_II"]["a_candidate_count"] = len(a_candidates_II)
        out["branch_II"]["a_candidates"] = [str(x) for x in a_candidates_II]
        record(f"branch II: {len(a_candidates_II)} candidate a-values found")

        branch_II_results = []
        for a0 in a_candidates_II:
            entry = {"a": str(a0)}
            try:
                b_sols = sp.solve(sp.Eq(gamma.subs(a, a0), 0), b)
                entry["b_candidates"] = [str(x) for x in b_sols]
                layer_hits = []
                for b0 in b_sols:
                    Delta0 = sp.expand((R1.subs({a: a0, b: b0})) * (R2.subs({a: a0, b: b0})))
                    Delta0_poly = sp.Poly(Delta0, w)
                    if Delta0_poly.degree() <= 0:
                        continue
                    _, sqf = sp.sqf_list(Delta0_poly)
                    odd_root_count = sum(sp.degree(f, w) for f, m in sqf if m % 2 == 1)
                    layer_hits.append({"b": str(b0), "delta_degree": Delta0_poly.degree(),
                                        "odd_multiplicity_root_count": odd_root_count,
                                        "genus4_check": (odd_root_count == 9)})
                entry["delta_checks"] = layer_hits
            except Exception as e:
                entry["error"] = f"{type(e).__name__}: {e}"
            branch_II_results.append(entry)
        out["branch_II"]["results"] = branch_II_results
        out["branch_II"]["completed"] = True
        record("branch II complete")

        out["status"] = "COMPLETE"
    except TimeBudgetExceeded:
        out["status"] = "INCOMPLETE"
        out["stop_reason"] = "TIME_BUDGET_EXCEEDED"
        record("TIME BUDGET EXCEEDED -- writing partial result")
    except Exception as e:
        out["status"] = "INCOMPLETE"
        out["stop_reason"] = f"{type(e).__name__}: {e}"
        record(f"exception: {out['stop_reason']}")
    finally:
        if use_alarm:
            signal.alarm(0)

    out["elapsed_seconds"] = time.time() - t_start
    _write(out)
    record(f"wrote result, status={out['status']}, elapsed={out['elapsed_seconds']:.2f}s")
    if out["status"] == "COMPLETE":
        print("R13_P1_TIER2_DONE", flush=True)
    else:
        print("R13_P1_TIER2_INCOMPLETE", flush=True)


def _write(out):
    import os
    os.makedirs("ci/out", exist_ok=True)
    with open(CERT_OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
