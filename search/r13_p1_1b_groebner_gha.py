#!/usr/bin/env python3
"""
search/r13_p1_1b_groebner_gha.py -- [P1-1'' step1b] Groebner-basis dimension measurement,
GHA lane A ("force lane") per 裁定1000.

Reads the exact equation strings from search/certs/r13_p1_1pp_k2_v1_20260812.json's
step1b_stratum_R1_eq_S_squared.equations (7 unknowns a,b,s0..s4; 10 equations), computes a
Groebner basis (grevlex), reports the measured dimension, and if 0-dimensional, attempts to
enumerate exact rational solutions.

Time-boxed: writes a partial-result artifact (with whatever has been computed so far) if the
Groebner computation has not finished by TIME_BUDGET_SECONDS, rather than being killed with no
output. A partial result is a first-class outcome (not a failure), per project discipline.

No judgement/verdict language. u_touched=false, c untouched (this script only manipulates the
already-derived symbolic equations, never evaluates any actual field value).
"""
import json
import signal
import sys
import time

import sympy as sp

CERT_IN = "search/certs/r13_p1_1pp_k2_v1_20260812.json"
CERT_OUT = "ci/out/r13_p1_1b_groebner_result.json"
TIME_BUDGET_SECONDS = 55 * 60  # leave margin inside a 1h job cap


class TimeBudgetExceeded(Exception):
    pass


def _alarm_handler(signum, frame):
    raise TimeBudgetExceeded()


def main():
    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    with open(CERT_IN, encoding="utf-8") as fh:
        src = json.load(fh)
    eq_strs = src["step1b_stratum_R1_eq_S_squared"]["equations"]
    unknowns = src["step1b_stratum_R1_eq_S_squared"]["unknowns"]
    record(f"loaded {len(eq_strs)} equations, {len(unknowns)} unknowns: {unknowns}")

    syms = sp.symbols(" ".join(unknowns))
    if len(unknowns) == 1:
        syms = (syms,)
    sym_map = dict(zip(unknowns, syms))

    eqs = [sp.sympify(e, locals=sym_map) for e in eq_strs]
    record("parsed equations into sympy expressions")

    out = {
        "schema": "r13-p1-1b-groebner/v1",
        "generated_by": {"tool": "python/sympy", "script": "search/r13_p1_1b_groebner_gha.py",
                          "order": "裁定1000 [P1-1'' step1b] lane A (force/Groebner)"},
        "input_cert": CERT_IN,
        "num_equations": len(eqs),
        "num_unknowns": len(unknowns),
        "unknowns": unknowns,
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "u_touched": False,
        "c_touched": False,
        "d_no_interpretation": "machine values only; verdict は司令塔",
    }

    # ---- time-boxed Groebner basis computation ----
    use_alarm = hasattr(signal, "SIGALRM")
    if use_alarm:
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.alarm(TIME_BUDGET_SECONDS)
    gb = None
    gb_error = None
    try:
        record("starting Groebner basis computation (grevlex)...")
        gb = sp.groebner(eqs, *syms, order="grevlex")
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
        print("R13_P1_1B_GROEBNER_INCOMPLETE", flush=True)
        return

    gb_polys_str = [str(p) for p in gb.polys]
    out["groebner_basis"] = gb_polys_str
    out["groebner_basis_size"] = len(gb.polys)

    # 0-dimensionality check: the ideal is 0-dimensional (over an algebraically closed field) iff
    # for EVERY variable, some pure power of that variable's leading monomial appears among the
    # Groebner basis's leading terms (grevlex) -- i.e. each variable is "bounded" by the basis.
    zero_dimensional = True
    per_var_bounded = {}
    for i, s in enumerate(syms):
        bounded = False
        for p in gb.polys:
            pol = sp.Poly(p, *syms, domain='QQ')
            monom = pol.monoms(order="grevlex")[0]  # leading monomial's exponent vector
            only_this_var = all(monom[j] == 0 for j in range(len(syms)) if j != i)
            if only_this_var and monom[i] > 0:
                bounded = True
                break
        per_var_bounded[str(s)] = bounded
        if not bounded:
            zero_dimensional = False

    out["zero_dimensional_check"] = {
        "per_variable_bounded_by_pure_power": per_var_bounded,
        "zero_dimensional": zero_dimensional,
        "method": "each variable has a pure-power leading monomial among the grevlex Groebner "
                  "basis elements (standard 0-dimensionality criterion)",
    }
    record(f"zero_dimensional = {zero_dimensional}")

    if zero_dimensional:
        record("attempting exact rational solve...")
        try:
            sols = sp.solve(eqs, list(syms), dict=True)
            out["solutions"] = [{str(k): str(v) for k, v in sol.items()} for sol in sols]
            out["solution_count"] = len(sols)
            record(f"found {len(sols)} solution(s)")
        except Exception as e:
            out["solve_error"] = f"{type(e).__name__}: {e}"
            record(f"solve raised: {out['solve_error']}")

    out["status"] = "COMPLETE"
    out["elapsed_seconds"] = time.time() - t_start
    _write(out)
    record(f"wrote final result, elapsed={out['elapsed_seconds']:.2f}s")
    print("R13_P1_1B_GROEBNER_DONE", flush=True)


def _write(out):
    import os
    os.makedirs("ci/out", exist_ok=True)
    with open(CERT_OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
