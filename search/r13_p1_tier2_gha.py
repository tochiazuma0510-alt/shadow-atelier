#!/usr/bin/env python3
"""
search/r13_p1_tier2_gha.py -- [P1] Tier 2 (remaining 4 layers, disc-product route) per 裁定1002,
docs/notes/w9_laneB_elimination_v1.md §4.

★ v2 (裁定1010 補記, 3 repairs applied to the v1 attempt that crashed -- run 31579129830):
  1. JSON writer: every field passed through _jsonable() (recursively converts sympy Integer/
     Rational/Expr etc to native int/str) and _checkpoint()/_write() wrap the WHOLE dump in
     try/except per-field so a single bad field can never prevent a valid partial JSON from being
     written at timeout (v1's bug: sp.degree() returns a sympy Integer, not a native int, and
     json.dump crashed on it -- exactly at the SIGALRM boundary, so NO artifact was written at all
     even though the alarm itself fired correctly).
  2. c9=2 substituted into P BEFORE constructing R1 = P-2w^9, so the w^9 terms cancel structurally
     and deg_w(R1) <= 8 is asserted (v1 built R1 from the GENERIC c9(a,b) expression, not yet on
     the gamma=0 curve, giving deg_w(R1)=9 -- the same degree as R2, defeating the "smaller
     Sylvester matrix" advantage the design note assumes, and likely a large factor in v1's disc_w
     (R1) taking 1486s).
  3. Checkpoint writes: after disc_w(R1) completes and after the branch I resultant completes (and
     symmetrically for branch II), an intermediate state is written to CERT_OUT immediately (not
     just at the very end or at timeout) -- so even a mid-branch-II timeout preserves branch I's
     full results, and a timeout can be pinpointed to exactly which step was in flight.

Layer (0,9) was found EMPTY by lane B (Gröbner basis = {1}, run 31578468586, confirmed
independently by hand-derivation: substituting the E1/E2 triangular solutions reduces the coupling
equations to gp3^k+gm3^k=0 for k=5,6,7,8 (forcing gp3=gm3=0 given the k=6,8 even-power constraints)
contradicting the k=9 equation gp3^9+gm3^9=-2). This script handles the remaining 4 layers: (2,7),
(4,5), (6,3), (8,1).

Method (§4): with c9=2 imposed, R1 := P-2w^9 (deg<=8), R2 := P+2w^9 (deg 9). ALL layers require
disc_w(R1)=0 OR disc_w(R2)=0 -- so:
  branch I:  resultant_b( gamma(a,b), disc_w(R1)(a,b) ) = 0  (eliminate b, univariate in a)
  branch II: resultant_b( gamma(a,b), disc_w(R2)(a,b) ) = 0
gamma(a,b) is the step1 curve equation (c9(a,b)-2=0).

For each candidate root a0, b0 recovered from gamma(a0,b)=0, Delta=R1*R2 at (a0,b0) is
squarefree-factored and the ODD-multiplicity root count is checked against 9 (genus-4 sieve --
NOT the squarefree-part degree).

Time-boxed (55min internal SIGALRM). Checkpoints written incrementally; a valid JSON artifact is
guaranteed at exit regardless of which step was interrupted.
"""
import json
import os
import signal
import time

import sympy as sp

CERT_OUT = "ci/out/r13_p1_tier2_result.json"
TIME_BUDGET_SECONDS = 55 * 60


class TimeBudgetExceeded(Exception):
    pass


def _alarm_handler(signum, frame):
    raise TimeBudgetExceeded()


def _jsonable(obj):
    """Recursively convert sympy objects (Integer, Rational, Expr, ...) and other non-native types
    into JSON-safe native Python values. Never raises -- falls back to str() for anything unknown."""
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, sp.Integer):
        return int(obj)
    if isinstance(obj, sp.Rational):
        return str(obj)
    if isinstance(obj, sp.Basic):
        return str(obj)
    try:
        return str(obj)
    except Exception:
        return "<unrepresentable>"


def _write(out):
    """Write the FULL out dict as JSON, guaranteed not to raise: any field that fails to serialize
    (even after _jsonable) is replaced with an error marker rather than aborting the whole write."""
    os.makedirs(os.path.dirname(CERT_OUT) or ".", exist_ok=True)
    safe = {}
    for k, v in out.items():
        try:
            safe[k] = _jsonable(v)
            json.dumps(safe[k])  # verify this specific field is actually serializable
        except Exception as e:
            safe[k] = f"<FIELD_SERIALIZE_ERROR: {type(e).__name__}: {e}>"
    try:
        with open(CERT_OUT, "w", encoding="utf-8") as fh:
            json.dump(safe, fh, ensure_ascii=False, indent=1)
    except Exception as e:
        # last-resort: write SOMETHING valid, even if it's just an error report
        with open(CERT_OUT, "w", encoding="utf-8") as fh:
            json.dump({"schema": "r13-p1-tier2/v2", "status": "WRITE_ERROR",
                       "error": f"{type(e).__name__}: {e}"}, fh)


def _checkpoint(out, tag):
    out["last_checkpoint"] = tag
    out["last_checkpoint_elapsed_seconds"] = out.get("_elapsed_fn", lambda: None)()
    _write(out)


def build_P_and_gamma():
    """Reconstruct P(w;a,b) and gamma(a,b) (the step1 curve, c9(a,b)-2=0) -- SAME derivation as
    r13_p1_1pp_k2_v1.py, recomputed here so this script is self-contained for the GHA job."""
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

    gamma = sp.expand(c[9] - 2)  # the step1 curve equation (c9(a,b) - 2 = 0)
    P_generic = sum(c[j] * w ** j for j in range(0, 10))
    return w, a, b, P_generic, gamma, c


def genus4_layer_check(R1, R2, a, b, a0, b0, w):
    Delta0 = sp.expand((R1.subs({a: a0, b: b0})) * (R2.subs({a: a0, b: b0})))
    Delta0_poly = sp.Poly(Delta0, w)
    if Delta0_poly.degree() <= 0:
        return None
    _, sqf = sp.sqf_list(Delta0_poly)
    odd_root_count = sum(sp.degree(f, w) for f, m in sqf if m % 2 == 1)
    return {"delta_degree": Delta0_poly.degree(),
            "odd_multiplicity_root_count": odd_root_count,
            "genus4_check": (odd_root_count == 9)}


def run_branch(label, discR, gamma, R1, R2, a, b, w, out, t_start, record):
    branch = out[label]
    record(f"computing resultant_b(gamma, disc{label}) elimination...")
    res = sp.factor(sp.resultant(gamma, discR, b))
    branch["resultant_in_a"] = str(res)
    branch["resultant_completed"] = True
    _checkpoint(out, f"{label}_resultant_done")
    record(f"resultant ({label}) computed -- checkpoint written")

    record(f"solving {label} resultant for candidate a values (exact)...")
    a_candidates = sp.solve(sp.Eq(res, 0), a)
    branch["a_candidate_count"] = len(a_candidates)
    branch["a_candidates"] = [str(x) for x in a_candidates]
    _checkpoint(out, f"{label}_a_candidates_done")
    record(f"{label}: {len(a_candidates)} candidate a-values found -- checkpoint written")

    results = []
    for idx, a0 in enumerate(a_candidates):
        entry = {"a": str(a0)}
        try:
            b_sols = sp.solve(sp.Eq(gamma.subs(a, a0), 0), b)
            entry["b_candidates"] = [str(x) for x in b_sols]
            hits = []
            for b0 in b_sols:
                r = genus4_layer_check(R1, R2, a, b, a0, b0, w)
                if r is not None:
                    r["b"] = str(b0)
                    hits.append(r)
            entry["delta_checks"] = hits
        except Exception as e:
            entry["error"] = f"{type(e).__name__}: {e}"
        results.append(entry)
        if idx % 3 == 0:
            branch["results"] = results
            _checkpoint(out, f"{label}_candidate_{idx}_of_{len(a_candidates)}")

    branch["results"] = results
    branch["completed"] = True
    _checkpoint(out, f"{label}_done")
    record(f"{label} complete -- checkpoint written")


def main():
    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    use_alarm = hasattr(signal, "SIGALRM")
    if use_alarm:
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.alarm(TIME_BUDGET_SECONDS)

    out = {
        "schema": "r13-p1-tier2/v2",
        "generated_by": {"tool": "python/sympy", "script": "search/r13_p1_tier2_gha.py",
                          "order": "裁定1010補記 [P1] Tier2 v2 (3 repairs) / "
                                   "docs/notes/w9_laneB_elimination_v1.md §4"},
        "supersedes_note": "v1 = run 31579129830, crashed writing the partial-result JSON due to "
                            "an un-jsonable sympy Integer field (fixed: repair 1); also built R1 "
                            "from the pre-gamma=0 generic c9(a,b) expression giving deg_w(R1)=9 "
                            "instead of the expected <=8 (fixed: repair 2, c9=2 substituted first)",
        "layer_0_9_status": "EMPTY (lane B, run 31578468586, Groebner basis = {1}, cross-checked "
                             "by hand-derivation -- see script docstring)",
        "layers_this_script_covers": ["(2,7)", "(4,5)", "(6,3)", "(8,1)"],
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "u_touched": False,
        "c_touched": False,
        "d_no_interpretation": "machine values only; verdict は司令塔",
        "branch_I": {"attempted": False}, "branch_II": {"attempted": False},
        "status": "INCOMPLETE",
        "_elapsed_fn": lambda: round(time.time() - t_start, 2),
    }
    _checkpoint(out, "start")

    try:
        record("reconstructing P(w;a,b) and gamma(a,b)...")
        w, a, b, P_generic, gamma, c = build_P_and_gamma()
        record(f"gamma(a,b) built (repair 2: substituting c9=2 BEFORE forming R1)")
        _checkpoint(out, "gamma_built")

        # repair 2: c[9] is a big expression (c9(a,b)), not a bare symbol -- a direct .subs() of
        # it to 2 is unreliable via sympy's generic subs. Instead rebuild P directly using c[0..8]
        # (still generic functions of a,b) plus the LITERAL constant 2 for the w^9 coefficient --
        # this is exactly "impose gamma=0 (c9=2) before forming R1", giving w^9 cancellation
        # structurally rather than as an equation to solve later.
        P_on_curve = sum(c[j] * w ** j for j in range(0, 9)) + 2 * w ** 9
        R1 = sp.expand(P_on_curve - 2 * w ** 9)
        R2 = sp.expand(P_on_curve + 2 * w ** 9)
        out["R1_degree_w"] = sp.degree(R1, w) if R1 != 0 else 0
        out["R2_degree_w"] = sp.degree(R2, w)
        record(f"deg_w R1={out['R1_degree_w']} (assert <=8) deg_w R2={out['R2_degree_w']} (expect 9)")
        assert out["R1_degree_w"] <= 8, f"repair 2 failed: deg_w(R1)={out['R1_degree_w']} > 8"
        out["repair2_assert_deg_R1_leq_8"] = True
        _checkpoint(out, "R1_R2_built_deg_asserted")

        record("computing disc_w(R1) (branch I, deg<=8 Sylvester matrix)...")
        discR1 = sp.expand(sp.discriminant(sp.Poly(R1, w)))
        out["branch_I"]["attempted"] = True
        out["branch_I"]["discR1_num_terms"] = len(sp.Add.make_args(discR1))
        _checkpoint(out, "discR1_done")
        record("disc_w(R1) computed -- checkpoint written")

        run_branch("branch_I", discR1, gamma, R1, R2, a, b, w, out, t_start, record)

        record("computing disc_w(R2) (branch II, deg=9)...")
        discR2 = sp.expand(sp.discriminant(sp.Poly(R2, w)))
        out["branch_II"]["attempted"] = True
        _checkpoint(out, "discR2_done")
        record("disc_w(R2) computed -- checkpoint written")

        run_branch("branch_II", discR2, gamma, R1, R2, a, b, w, out, t_start, record)

        out["status"] = "COMPLETE"
    except TimeBudgetExceeded:
        out["status"] = "INCOMPLETE"
        out["stop_reason"] = "TIME_BUDGET_EXCEEDED"
        record("TIME BUDGET EXCEEDED -- writing partial result (from last checkpoint state)")
    except Exception as e:
        out["status"] = "INCOMPLETE"
        out["stop_reason"] = f"{type(e).__name__}: {e}"
        record(f"exception: {out['stop_reason']}")
    finally:
        if use_alarm:
            signal.alarm(0)

    out["elapsed_seconds"] = time.time() - t_start
    del out["_elapsed_fn"]
    _write(out)
    record(f"wrote FINAL result, status={out['status']}, elapsed={out['elapsed_seconds']:.2f}s")
    if out["status"] == "COMPLETE":
        print("R13_P1_TIER2_DONE", flush=True)
    else:
        print("R13_P1_TIER2_INCOMPLETE", flush=True)


if __name__ == "__main__":
    main()
