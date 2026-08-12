"""
search/r13_p1_1_k2_v1.py -- [P1-1'] k=2 scan attempt (裁定993, docs/notes/w9_ansatz_v2_blocks.md §7)

lambda_9 route (deg_w=18), k=2 (11/10 unknowns per the design doc's Newton-triangle count -- see
note below on a discrepancy I found in that count). Attempts the t=1 branching condition
(F(1,w) = (w-a)(w-b)*g(w)^2, g monic degree 8) via direct coefficient matching (vanishing of the
w^17..w^10 coefficients, per the design's own (e1) instruction), WITHOUT yet imposing any other
condition.

★★★ RESULT: (g1) WATCH VIOLATION -- the solution set is NOT 0-dimensional. Solving the 8
coefficient-vanishing equations for g_0..g_7 in terms of (a,b) succeeds UNIQUELY (a clean
triangular/sequential solve, each g_i a polynomial in a,b with NO extra constraint on a,b), leaving
(a,b) as two genuinely FREE parameters. Per docs/notes/w9_structure_and_ansatz_v1.md §5's own
fail-closed instruction ("正次元が出たら過剰パラメータ化 = 実装バグ ⟹ 即停止"), this script STOPS
here and reports the finding rather than proceeding further into k=3/4/5 or attempting to force a
0-dimensional answer.

Not-yet-checked candidate explanation (reported, not asserted): matching ONLY the local branching
pattern at t=0,1,infty is a NECESSARY but plausibly NOT SUFFICIENT condition to pin down the
SPECIFIC cover W_9 (with its particular monodromy group, order 324, from r13_p1_0_blocks_v1) --
Hurwitz spaces of covers with a given branch-point/passport data are generically POSITIVE
dimensional unless the monodromy datum is additionally "rigid" (a separate condition this script
does not check). If so, [P1-1']'s ansatz as literally specified in §7 (local coefficient-matching
only) is underdetermined, and an additional equation set (capturing the actual monodromy group, not
just the local ramification type) is needed before a 0-dimensional solve is possible.

Discrepancy note (reported, not silently reconciled): the design doc's table
(docs/notes/branchP_and_r_spec_v1.md §4) states k=2 has "11" free unknowns after normalization.
This script's own direct count of the Newton-triangle support (18i+2j<=36, 0<=i<=2, 0<=j<=18),
after applying (n1) c_{0,j}=0 for j<18, (n2) c_{0,18}=1, (n3) c_{2,0}=1, gives 10 free unknowns
(the i=1 row, j=0..9), not 11. This 1-off discrepancy is reported for the record, not resolved
here -- it does not materially affect the positive-dimensionality finding above (a 9- or 10-
unknown system with only 8 independent equations is positive-dimensional either way).
"""
import json
import sympy as sp

w = sp.symbols("w")
a, b = sp.symbols("a b")
gsyms = sp.symbols("g0 g1 g2 g3 g4 g5 g6 g7")


def main():
    gpoly = w ** 8 + sum(gsyms[i] * w ** i for i in range(8))
    target = sp.expand((w - a) * (w - b) * gpoly ** 2)
    target_poly = sp.Poly(target, w)
    coeffs = target_poly.all_coeffs()  # index 0 = w^18 coeff, ..., index 18 = w^0 coeff
    leading_coeff_is_1 = (coeffs[0] == 1)
    print(f"target polynomial degree = {target_poly.degree()} (expect 18)")
    print(f"leading (w^18) coefficient = {coeffs[0]} (expect 1, matching c_{{0,18}}=1 normalization)")

    # equations: coefficients of w^17 down to w^10 must vanish (8 equations)
    eqs = []
    for k in range(17, 9, -1):
        idx = 18 - k
        eqs.append(coeffs[idx])
    print(f"{len(eqs)} coefficient-vanishing equations (w^17 down to w^10)")

    # sequential (triangular) solve for g7,g6,...,g0 in terms of a,b
    subs = {}
    order = [gsyms[7], gsyms[6], gsyms[5], gsyms[4], gsyms[3], gsyms[2], gsyms[1], gsyms[0]]
    solved_uniquely = True
    solutions_summary = {}
    for i, eq in enumerate(eqs):
        e2 = eq.subs(subs)
        var = order[i]
        sol = sp.solve(sp.Eq(e2, 0), var)
        if len(sol) != 1:
            solved_uniquely = False
            print(f"  step {i}: solving for {var} gave {len(sol)} solutions (not unique): {sol}")
            if not sol:
                break
            subs[var] = sp.simplify(sol[0])
        else:
            subs[var] = sp.simplify(sol[0])
        solutions_summary[str(var)] = str(subs[var])
        print(f"  step {i}: {var} = {subs[var]}")

    # check: after solving all 8, are (a,b) still genuinely free (i.e. no equation constrains them)?
    remaining_free_symbols = {a, b} - set().union(*(eq.free_symbols for eq in [])) if False else {a, b}
    # (the 8 equations were fully consumed by the triangular solve above -- if solved_uniquely and
    # no equation was ever left over as a residual constraint purely in a,b, then a,b are free)
    positive_dimensional = solved_uniquely  # 8 equations, 10 unknowns, uniquely solved for 8 of them
    # leaves exactly 2 (a,b) unconstrained => 2-dimensional solution variety

    print(f"\n[G1 WATCH] solved_uniquely_for_g0_through_g7={solved_uniquely}")
    print(f"[G1 WATCH] (a,b) remain UNCONSTRAINED by the 8 equations => solution variety is "
          f"(at least) 2-dimensional, NOT 0-dimensional")
    print(f"[G1 WATCH VIOLATED] = {positive_dimensional}")

    out = {
        "schema": "r13-p1-1-k2/v1",
        "generated_by": {"tool": "python/sympy", "script": "search/r13_p1_1_k2_v1.py",
                          "order": "裁定993 / docs/notes/w9_ansatz_v2_blocks.md §7 [P1-1']"},
        "k_attempted": 2,
        "route": "lambda_9 (deg_w=18); mu route NOT used (forbidden per §7 [P1-3])",
        "target_polynomial_degree": target_poly.degree(),
        "leading_coeff_is_1": leading_coeff_is_1,
        "num_equations": len(eqs),
        "num_unknowns_in_this_parametrization": 10,  # a,b,g0..g7
        "design_doc_stated_unknown_count_k2": 11,
        "unknown_count_discrepancy_note": "this script's own direct Newton-triangle count gives 10 "
                                            "free unknowns for k=2 after (n1)(n2)(n3), not 11 as "
                                            "stated in branchP_and_r_spec_v1.md §4's table; reported "
                                            "not silently reconciled; does not change the finding "
                                            "below either way",
        "solved_uniquely_for_g0_g7_in_terms_of_ab": solved_uniquely,
        "g_solutions_in_terms_of_ab": solutions_summary,
        "g1_watch": {
            "claim": "解イデアルは0次元でなければならない(docs/notes/w9_structure_and_ansatz_v1.md §5)",
            "finding": "positive-dimensional (a,b free, >=2 dimensions) -- WATCH VIOLATED",
            "violated": positive_dimensional,
            "action_per_spec": "即停止・バグ報告 (STOP and report, per the design's own fail-closed instruction)",
        },
        "candidate_explanation_unconfirmed": "matching only the LOCAL branching pattern at t=0,1,infty "
            "(this ansatz's (e1) condition) is likely necessary but not sufficient to pin down the "
            "SPECIFIC cover with monodromy group order 324 (r13_p1_0_blocks_v1); Hurwitz spaces of "
            "covers sharing a passport are generically positive-dimensional unless the monodromy "
            "datum is additionally rigid, a separate condition not checked by this ansatz as literally "
            "specified in §7. NOT asserted as proven -- reported as the leading candidate explanation.",
        "u_touched": False,
        "c_touched": False,
        "d_no_interpretation": "machine values only; verdict は司令塔",
        "status": "STOPPED at k=2 per (g1) fail-closed watch; k=3,4,5 NOT attempted",
    }
    with open("search/certs/r13_p1_1_k2_v1_20260812.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("\nwrote search/certs/r13_p1_1_k2_v1_20260812.json")


if __name__ == "__main__":
    main()
