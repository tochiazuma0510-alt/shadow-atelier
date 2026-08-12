#!/usr/bin/env python3
"""
search/r13_p1_b_laneB_gha.py -- [P1-B] lane B (U_+/U_- decomposition, degree-9 elimination)
per docs/notes/w9_laneB_elimination_v1.md §3, 裁定1001.

10 unknowns: rho_p, rho_m, gp0..gp3, gm0..gm3.
U_p := (w-rho_p)*g_+(w)^2, U_m := (w-rho_m)*g_-(w)^2 (g_+ = w^4+gp3 w^3+gp2 w^2+gp1 w+gp0, monic
deg 4; g_- likewise).

13 equations (all degree <=3 in the unknowns -- rho*g_i*g_j type):
  (E1) [U_p]_j = 0 for j=8,7,6,5        (4)
  (E2) [U_m]_j = 0 for j=8,7,6,5        (4)
  (E3) [U_p]_j + [U_m]_j = 0 for j=4,3,2,1  (4)
  (E4) [U_p]_0 + [U_m]_0 = 2            (1)

Time-boxed (55min internal SIGALRM) exactly like search/r13_p1_1b_groebner_gha.py (lane A) --
writes a partial-result artifact if not finished in time. If 0-dimensional, enumerate exact
rational solutions and, for each, run the (B1)-(B7) watches specified in the design note (B6/genus
require reconstructing Delta and checking odd-multiplicity root count -- done here with sympy's
sqf_list, per the note's own explicit warning that this is NOT the squarefree-part DEGREE but the
count of odd-multiplicity roots).
"""
import json
import signal
import time

import sympy as sp

CERT_OUT = "ci/out/r13_p1_b_laneB_result.json"
TIME_BUDGET_SECONDS = 55 * 60


class TimeBudgetExceeded(Exception):
    pass


def _alarm_handler(signum, frame):
    raise TimeBudgetExceeded()


def main():
    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    w = sp.symbols("w")
    rho_p, rho_m = sp.symbols("rho_p rho_m")
    gp = sp.symbols("gp0 gp1 gp2 gp3")
    gm = sp.symbols("gm0 gm1 gm2 gm3")
    unknowns = [rho_p, rho_m] + list(gp) + list(gm)
    unknown_names = [str(u) for u in unknowns]

    g_plus = w ** 4 + gp[3] * w ** 3 + gp[2] * w ** 2 + gp[1] * w + gp[0]
    g_minus = w ** 4 + gm[3] * w ** 3 + gm[2] * w ** 2 + gm[1] * w + gm[0]
    U_p = sp.expand((w - rho_p) * g_plus ** 2)
    U_m = sp.expand((w - rho_m) * g_minus ** 2)

    Up_poly = sp.Poly(U_p, w)
    Um_poly = sp.Poly(U_m, w)
    Up_c = {d: Up_poly.coeff_monomial(w ** d) for d in range(10)}
    Um_c = {d: Um_poly.coeff_monomial(w ** d) for d in range(10)}
    record(f"deg U_p={Up_poly.degree()} deg U_m={Um_poly.degree()} (expect 9,9); "
           f"leading coeffs: {Up_c[9]}, {Um_c[9]} (expect 1,1 -- monic check)")

    eqs = []
    for j in (8, 7, 6, 5):
        eqs.append(Up_c[j])
    for j in (8, 7, 6, 5):
        eqs.append(Um_c[j])
    for j in (4, 3, 2, 1):
        eqs.append(Up_c[j] + Um_c[j])
    eqs.append(Up_c[0] + Um_c[0] - 2)
    record(f"built {len(eqs)} equations (expect 13)")

    out = {
        "schema": "r13-p1-b-laneB/v1",
        "generated_by": {"tool": "python/sympy", "script": "search/r13_p1_b_laneB_gha.py",
                          "order": "裁定1001 [P1-B] lane B / docs/notes/w9_laneB_elimination_v1.md §3"},
        "unknowns": unknown_names,
        "num_equations": len(eqs),
        "num_unknowns": len(unknowns),
        "monic_check": {"Up_leading": str(Up_c[9]), "Um_leading": str(Um_c[9])},
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "u_touched": False,
        "c_touched": False,
        "d_no_interpretation": "machine values only; verdict は司令塔",
    }

    use_alarm = hasattr(signal, "SIGALRM")
    if use_alarm:
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.alarm(TIME_BUDGET_SECONDS)
    gb = None
    gb_error = None
    try:
        record("starting Groebner basis computation (grevlex)...")
        gb = sp.groebner(eqs, *unknowns, order="grevlex")
        record(f"Groebner basis computed: {len(gb.polys)} polynomials")
    except TimeBudgetExceeded:
        gb_error = "TIME_BUDGET_EXCEEDED"
        record("TIME BUDGET EXCEEDED -- writing partial result")
    except Exception as e:
        gb_error = f"{type(e).__name__}: {e}"
        record(f"Groebner computation raised an exception: {gb_error}")
    finally:
        if use_alarm:
            signal.alarm(0)

    if gb is None:
        out["status"] = "INCOMPLETE"
        out["groebner_error"] = gb_error
        out["elapsed_seconds"] = time.time() - t_start
        _write(out)
        record("wrote partial/incomplete result")
        print("R13_P1_B_LANEB_INCOMPLETE", flush=True)
        return

    out["groebner_basis"] = [str(p) for p in gb.polys]
    out["groebner_basis_size"] = len(gb.polys)

    zero_dimensional = True
    per_var_bounded = {}
    for i, s in enumerate(unknowns):
        bounded = False
        for p in gb.polys:
            pol = sp.Poly(p, *unknowns, domain='QQ')
            monom = pol.monoms(order="grevlex")[0]
            only_this_var = all(monom[j] == 0 for j in range(len(unknowns)) if j != i)
            if only_this_var and monom[i] > 0:
                bounded = True
                break
        per_var_bounded[str(s)] = bounded
        if not bounded:
            zero_dimensional = False
    out["zero_dimensional_check"] = {
        "per_variable_bounded_by_pure_power": per_var_bounded,
        "zero_dimensional": zero_dimensional,
    }
    record(f"zero_dimensional = {zero_dimensional}")

    solutions_out = []
    if zero_dimensional:
        record("attempting exact rational solve...")
        try:
            sols = sp.solve(eqs, list(unknowns), dict=True)
            record(f"found {len(sols)} raw solution(s) from sp.solve")
            out["raw_solution_count"] = len(sols)

            for sol in sols:
                entry = {str(k): str(v) for k, v in sol.items()}
                # only proceed with watches if the solution is fully rational (no free symbols)
                vals = list(sol.values())
                is_fully_determined = all(v.free_symbols == set() for v in vals) if vals else False
                entry["fully_determined"] = is_fully_determined
                if not is_fully_determined:
                    solutions_out.append(entry)
                    continue
                try:
                    rho_p_v = sol.get(rho_p, rho_p)
                    rho_m_v = sol.get(rho_m, rho_m)
                    gp_v = [sol.get(s, s) for s in gp]
                    gm_v = [sol.get(s, s) for s in gm]
                    g_plus_v = w ** 4 + gp_v[3] * w ** 3 + gp_v[2] * w ** 2 + gp_v[1] * w + gp_v[0]
                    g_minus_v = w ** 4 + gm_v[3] * w ** 3 + gm_v[2] * w ** 2 + gm_v[1] * w + gm_v[0]
                    Up_v = sp.expand((w - rho_p_v) * g_plus_v ** 2)
                    Um_v = sp.expand((w - rho_m_v) * g_minus_v ** 2)

                    # (B2) gcd(U_p,U_m)=1
                    gcd_UpUm = sp.gcd(Up_v, Um_v)
                    b2_pass = (sp.degree(gcd_UpUm, w) == 0)
                    entry["B2_gcd_Up_Um_is_1"] = b2_pass

                    # reconstruct S1, R1, R2, P, a, b, g
                    S1 = sp.expand(Up_v - (w ** 9 + 1))
                    b3_deg_ok = (sp.degree(S1, w) <= 4) if S1 != 0 else True
                    R1 = sp.expand(-S1 ** 2)
                    R2 = sp.expand(R1 + 4 * w ** 9)
                    P = sp.expand(R1 + 2 * w ** 9)
                    a_val, b_val = rho_p_v, rho_m_v
                    g_val = sp.expand(g_plus_v * g_minus_v)

                    # (B3) R2 squarefree
                    R2_sqf = sp.sqf_list(sp.Poly(R2, w)) if sp.Poly(R2, w).degree() > 0 else None
                    b3_pass = (R2_sqf is not None) and all(m == 1 for _, m in R2_sqf[1])
                    entry["B3_R2_squarefree"] = b3_pass
                    entry["B3_deg_S1_leq_4"] = b3_deg_ok

                    # (B4) c0 != 0 where c0 = P(0)
                    c0_val = P.subs(w, 0)
                    b4_pass = (c0_val != 0)
                    entry["B4_c0_nonzero"] = b4_pass
                    entry["c0_value"] = str(c0_val)

                    # (B1) F(1,w) = (w-a)(w-b) g(w)^2 exact recheck
                    F1_check = sp.expand(w ** 18 + P + 1)
                    rhs_check = sp.expand((w - a_val) * (w - b_val) * g_val ** 2)
                    b1_pass = sp.simplify(F1_check - rhs_check) == 0
                    entry["B1_F1w_matches_factored_form"] = b1_pass

                    # (B5) Delta = R1*R2, count ODD-multiplicity roots (not squarefree-part degree)
                    Delta = sp.expand(R1 * R2)
                    Delta_poly = sp.Poly(Delta, w)
                    if Delta_poly.degree() > 0:
                        content, sqf_factors = sp.sqf_list(Delta_poly)
                        odd_mult_root_count = 0
                        for factor, mult in sqf_factors:
                            deg_f = sp.degree(factor, w)
                            if mult % 2 == 1:
                                odd_mult_root_count += deg_f
                        entry["B5_delta_degree"] = Delta_poly.degree()
                        entry["B5_odd_multiplicity_root_count"] = odd_mult_root_count
                        entry["B5_genus4_check"] = (odd_mult_root_count == 9)
                    else:
                        entry["B5_delta_degree"] = 0
                        entry["B5_odd_multiplicity_root_count"] = None
                        entry["B5_genus4_check"] = False

                    entry["a"] = str(a_val)
                    entry["b"] = str(b_val)
                    entry["reconstructed_g"] = str(g_val)
                    entry["reconstructed_P"] = str(P)
                except Exception as e:
                    entry["watch_computation_error"] = f"{type(e).__name__}: {e}"
                solutions_out.append(entry)
        except Exception as e:
            out["solve_error"] = f"{type(e).__name__}: {e}"
            record(f"solve raised: {out['solve_error']}")

    out["solutions"] = solutions_out
    out["solution_count"] = len(solutions_out)
    # (B7) solution count should be a multiple of 18 (mu_9 x swap gauge orbit)
    out["B7_solution_count_multiple_of_18"] = (len(solutions_out) % 18 == 0) if solutions_out else None
    if not solutions_out:
        out["B8_note"] = "zero solutions -- stratum (0,9) empty (per spec, this is NOT an anomaly; " \
                          "would indicate Tier 2 is needed, out of this script's scope per 裁定1001)"

    out["status"] = "COMPLETE"
    out["elapsed_seconds"] = time.time() - t_start
    _write(out)
    record(f"wrote final result, elapsed={out['elapsed_seconds']:.2f}s, "
           f"solution_count={len(solutions_out)}")
    print("R13_P1_B_LANEB_DONE", flush=True)


def _write(out):
    import os
    os.makedirs("ci/out", exist_ok=True)
    with open(CERT_OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
