#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-checker-native.py

N_infty stage-2 -- lane B "checker_native": FROM-SCRATCH, point-level
construction of ramification_divisor_on_C / branch_divisor_on_P1
(governing spec = mb/ninfty-stage2-predicate/v18, sec.1 math core +
sec.4.1 certificate schema). This fills the gap search/ninfty-checker.py
had explicitly declared NOT IMPLEMENTED ("full checker_native divisor
construction ... requires locating actual points on the curve C_crv over
Qbar" -- see that file's module docstring, item 5 of the UNKNOWN list).

Independence discipline (commander's brief, 2026-08-01): this module was
written from the governing spec text ONLY. It has never read lane A's
implementation (the mjs `buildSearcherNative` function in
search/mb-ninfty-branch-search.mjs) or any of lane A's native-artifact
output (e.g. search/certs/ep_first_run/beta_searcher_native.json). Any
comparison against lane A's actual output belongs in a SEPARATE crosscheck
script (search/checker_native_crosscheck.py), not here.

runtime = python + sympy (exact algebra only: Rational, sqrt, gcd,
all_roots/CRootOf, series). No floating point anywhere in this file.

--------------------------------------------------------------------------
Mathematical derivation (spec sec.1, symbols as in the spec: C_crv:
y^2=f6(x), mu=a(x)+p(x)y, deg a=5, deg p=2, a5=p2!=0, (Pell) a^2-f6p^2=C
in Q^x, (Or) (mu)=5P_0-5P_infty).

(A) mu has NO finite zeros or poles on C_crv.
    mu * mu^iota = a^2 - f6 p^2 = C (the Pell constant), a NONZERO
    CONSTANT POLYNOMIAL -- i.e. its value at every finite x0 is the same
    nonzero number C. So mu(Q)*mu^iota(Q) = C != 0 for every finite point
    Q, hence mu(Q) != 0 for every finite Q. mu = a(x)+p(x)y is manifestly
    a polynomial in (x,y), so it has no finite poles either (the only
    possible poles of a regular function on the affine model are at
    infinity). Consequence: every zero/pole of mu is located at one of
    the two points at infinity of C_crv (f6 monic of even degree 6 => two
    such points, distinguished below).

(B) Finite ramification points (fibers over s, -s with s^2=-C):
    lemma N-inf-pair (spec sec.1.5): for s with s^2=-C,
        H_s = -2 s a(x),    part(mu^{-1}(s)) = part(mu^{-1}(-s)) = rootpart(a).
    Under T-1 (deg gcd(a,a')=2, squarefree; deg gcd(a,a',a'')=0),
    rootpart(a) = [2,2,1]: d := monic(gcd(a,a')) is the SQUAREFREE degree-2
    factor collecting exactly the two double roots of a. For each root x0
    of d (obtained via sympy Poly(d,x).all_roots() -- exact radicals for
    a quadratic, no floating point), the RAMIFICATION points (e=2, i.e.
    contributing multiplicity e-1=1 each to the ramification divisor) in
    fiber s / -s are
        Q(x0, +s) = (x0, s / p(x0))   over branch value  s
        Q(x0, -s) = (x0, -s / p(x0))  over branch value -s
    (from mu(Q) = a(x0) + p(x0) y(Q) = v and a(x0) = 0 at a double root of
    a, since H_v(x0)=0 <=> a(x0)=0 for v with v^2=-C per the lemma's own
    proof). These lie on the curve automatically: y(Q)^2 = f6(x0) follows
    from (Pell) at x0 (p(x0)^2 f6(x0) = a(x0)^2 - C = -C = s^2, so
    (s/p(x0))^2 = s^2/p(x0)^2 = f6(x0)) -- checked explicitly below as a
    self-consistency guard, not assumed.

(C) Infinity points (contributing 5P_0 - 5P_infty, spec (Or), the "4+4"
    of the Riemann-Hurwitz total deg R_mu=12, spec sec.1.8):
    Local parameter t=1/x at infinity. Since f6 is monic of degree 6,
        g(t) := t^6 f6(1/t)          (finite polynomial in t, g(0)=1)
    and Y(t) := y * t^3 satisfies Y(t)^2 = g(t), a FORMAL POWER SERIES
    with Y(0) = +-1 -- the two points at infinity, labelled here
    "plus" (Y(0)=+1) and "minus" (Y(0)=-1). Writing
        A(t) := t^5 a(1/t)   (reverse of a's coefficients, degree <=5)
        P(t) := t^2 p(1/t)   (reverse of p's coefficients, degree <=2)
    one computes directly
        mu * t^5 = A(t) + P(t) Y(t)  =:  M(t)   (a power series in t).
    If M(t) has a nonzero constant term, mu has a POLE of order exactly 5
    at that point; if M(t) vanishes to order j>5, mu has a ZERO of order
    j-5. Since a5=p2 (E-3), the "plus" branch gives M(0)=a5+p2*1=2 a5 != 0
    (order j=0, ALWAYS a pole of order exactly 5 -- no series computation
    needed, this branch is P_infty, no ambiguity). The "minus" branch
    gives M(0)=a5-p2*1=0 by E-3 and requires expanding the series to find
    the first nonzero coefficient; spec (Or) predicts this is exactly
    j=10 (a zero of mu of order exactly 5 -- this branch is P_0). This
    module COMPUTES the actual leading order from (a,p,f6) via
    sympy series to a bounded cap and reports what it finds -- it does
    NOT assume j=10 a priori. If the computed order differs from the
    spec-predicted value, that is recorded as an explicit anomaly, not
    silently forced (commander's brief item on honest reporting; this is
    an instance-level computation, not a general theorem claim -- the
    general theorem status of (Or) is out of scope for this file and is
    NOT re-litigated here).

    NOTE on E-5 (divisor orientation) in ninfty-checker.py: that existing
    checker treats divisor_orientation_attested as an externally supplied,
    unrecoverable boolean and gates REJECT on it. This module does NOT
    touch that gate. The infinity-point labelling derived here (P_0 =
    "minus" branch when its computed local order is exactly +5, P_infty =
    "plus" branch, order exactly -5) is exposed as ADDITIONAL, informational,
    DERIVED data (`orientation_derivation` in the returned artifact) for
    cross-checking against any caller-supplied attestation -- it is not
    wired into any REJECT/ACCEPT decision by this file.
--------------------------------------------------------------------------

Field schema of the returned artifact matches the `native_artifact` shape
already exercised by search/ninfty-checker.py's check_native_pushforward
(and search/fixtures/ninfty/checker_pos_03.json):
    ramification_divisor_on_C: [ {point, maps_to_branch_value, multiplicity,
                                   kind, x_srepr, y_srepr (finite points
                                   only)}, ... ]
    branch_divisor_on_P1: [ {branch_value, multiplicity}, ... ]
    finite_aggregate_partitions: { branch_value: [2,2,1], ... }
    orientation_derivation: { ... local-order findings at infinity ... }
    native_artifact_digest: sha256 of the canonical serialization.

Status: implemented 20260801 (commander's brief: EP last missing piece,
裁定305 gap closure).
"""

from __future__ import annotations
import hashlib
import json
import sys
import argparse
import sympy as sp

X = sp.symbols("x")
T = sp.symbols("t")

CHECKER_NATIVE_ID = "search/ninfty-checker-native.py"
CHECKER_NATIVE_ALGORITHM_TAG = "sympy-exact-algebra(gcd+all_roots+series)-no-float"


# --------------------------------------------------------------------------
# exact coefficient parsing (same JSON convention as ninfty-checker.py:
# coefficient lists, low-degree-first, "p/q" strings or plain numbers)
# --------------------------------------------------------------------------

def _rat(c):
    if isinstance(c, sp.Basic):
        return c
    if isinstance(c, str):
        if "/" in c:
            n, d = c.split("/")
            return sp.Rational(int(n), int(d))
        return sp.Rational(c)
    return sp.Rational(c)


def poly_from_coeffs(coeffs, var=X):
    """coeffs low-degree-first -> sympy expression (exact Rational coeffs)."""
    return sp.expand(sum(_rat(c) * var ** i for i, c in enumerate(coeffs)))


def _canon(expr):
    """Canonical, deterministic, exact string key for a sympy algebraic
    number/expression (used both as a human label and as the exact-match
    key that ties ramification points to branch-divisor entries)."""
    return sp.srepr(sp.nsimplify(sp.together(sp.radsimp(sp.expand(expr)))))


def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# (B) finite ramification points, spec sec.1.5 N-inf-pair
# --------------------------------------------------------------------------

def _finite_ramification_points(a, p, C):
    """
    Returns (status, detail) where on success detail = {
        'd_expr', 'd_degree', 'roots' (list of sympy exprs),
        's', 'ms' (=-s), 'points': [ {x, y, branch} ... ]
    }.
    status in {"ok", "gcd-degree-not-2", "gcd-not-squarefree",
               "pell-not-nonzero-constant", "curve-consistency-failure"}.
    Never raises for malformed/degenerate input -- degeneracies are
    reported, not thrown.
    """
    ap = sp.diff(a, X)
    d = sp.gcd(a, ap)
    d = sp.expand(d)
    d_poly = sp.Poly(d, X) if d != 0 else None
    d_deg = d_poly.degree() if d_poly is not None else -1

    if d_deg != 2:
        return "gcd-degree-not-2", {"d_expr": str(d), "d_degree": d_deg}

    d_monic = sp.Poly(d, X).monic()
    disc = sp.discriminant(d_monic.as_expr(), X)
    if sp.simplify(disc) == 0:
        return "gcd-not-squarefree", {"d_expr": str(d_monic.as_expr())}

    roots = d_monic.all_roots()
    if len(roots) != 2:
        return "gcd-not-squarefree", {"d_expr": str(d_monic.as_expr()), "roots_found": len(roots)}

    if C == 0:
        return "pell-not-nonzero-constant", {"C": str(C)}

    s = sp.sqrt(-C)
    ms = -s

    points = []
    for r in roots:
        pr = sp.simplify(p.subs(X, r))
        if pr == 0:
            return "curve-consistency-failure", {"reason": "p(root)=0", "root": _canon(r)}
        for branch_val, branch_label in ((s, "plus_s"), (ms, "minus_s")):
            y = sp.radsimp(sp.simplify(branch_val / pr))
            # self-consistency guard: (x,y) must lie on y^2=f6(x); checked
            # by the caller (construct_checker_native) using the supplied
            # f6, not assumed true here.
            points.append({"x": r, "y": y, "branch_value": branch_val, "branch_label": branch_label})

    return "ok", {"d_expr": str(d_monic.as_expr()), "d_degree": 2, "roots": roots,
                  "s": s, "ms": ms, "points": points}


# --------------------------------------------------------------------------
# (C) infinity ramification points, local Puiseux-type order computation
# --------------------------------------------------------------------------

def _infinity_local_orders(a_coeffs, p_coeffs, f6_coeffs, series_cap=40):
    """
    Returns dict with the two branches' computed local orders of mu at
    t=1/x=0 (local order = coefficient-of-t^5*mu's leading exponent minus
    5; positive => zero of that order, negative => pole of that order),
    plus the raw series data for audit.
    """
    f6_rev = [_rat(c) for c in reversed(f6_coeffs)]
    g = sp.expand(sum(c * T ** i for i, c in enumerate(f6_rev)))
    if sp.simplify(g.subs(T, 0)) != 1:
        return {"status": "f6-not-monic-cannot-expand-at-infinity", "g0": str(g.subs(T, 0))}

    a_rev = [_rat(c) for c in reversed(a_coeffs)]
    A = sp.expand(sum(c * T ** i for i, c in enumerate(a_rev)))
    p_rev = [_rat(c) for c in reversed(p_coeffs)]
    P = sp.expand(sum(c * T ** i for i, c in enumerate(p_rev)))

    Yplus_series = sp.series(sp.sqrt(g), T, 0, series_cap).removeO()
    Yplus_series = sp.expand(Yplus_series)

    def leading_order(expr):
        e = sp.Poly(sp.expand(expr), T)
        for k in range(series_cap):
            c = e.coeff_monomial(T ** k)
            if sp.simplify(c) != 0:
                return k, c
        return None, None

    M_plus = sp.expand(A + P * Yplus_series)
    M_minus = sp.expand(A - P * Yplus_series)

    j_plus, c_plus = leading_order(M_plus)
    j_minus, c_minus = leading_order(M_minus)

    def local_order(j):
        return None if j is None else (j - 5)

    return {
        "status": "ok",
        "series_cap": series_cap,
        "plus_branch": {"leading_series_order_j": j_plus, "leading_coeff": str(c_plus),
                         "local_order_of_mu": local_order(j_plus)},
        "minus_branch": {"leading_series_order_j": j_minus, "leading_coeff": str(c_minus),
                          "local_order_of_mu": local_order(j_minus)},
    }


# --------------------------------------------------------------------------
# top-level construction
# --------------------------------------------------------------------------

def construct_checker_native(a_coeffs, p_coeffs, f6_coeffs, series_cap=40):
    """
    candidate coefficient lists (low-degree-first, same JSON convention as
    search/ninfty-checker.py). Returns the checker_native artifact dict
    (schema in module docstring) plus a top-level 'status' ("ok" or a
    degeneracy code) and 'diagnostics'. Never raises on malformed/
    degenerate numeric input -- everything is reported.
    """
    a = poly_from_coeffs(a_coeffs)
    p = poly_from_coeffs(p_coeffs)
    f6 = poly_from_coeffs(f6_coeffs)

    diagnostics = {}

    # basic degree/monic guards (mirrors E-1/E-2/E-3 shape checks, but this
    # module does not own REJECT semantics -- it just refuses to construct
    # points it cannot honestly locate).
    deg_a = sp.degree(a, X) if a != 0 else -1
    deg_p = sp.degree(p, X) if p != 0 else -1
    deg_f6 = sp.degree(f6, X) if f6 != 0 else -1
    if (deg_a, deg_p, deg_f6) != (5, 2, 6):
        return {"status": "degree-mismatch",
                "diagnostics": {"deg_a": deg_a, "deg_p": deg_p, "deg_f6": deg_f6}}

    C = sp.nsimplify(sp.expand(a ** 2 - f6 * p ** 2))
    if not C.is_constant() or sp.simplify(C) == 0:
        return {"status": "pell-not-nonzero-constant", "diagnostics": {"C_expr": str(C)}}

    fin_status, fin_detail = _finite_ramification_points(a, p, C)
    diagnostics["finite_construction_status"] = fin_status
    if fin_status != "ok":
        return {"status": fin_status, "diagnostics": {**diagnostics, "finite_detail": fin_detail}}

    # self-consistency guard: every constructed finite point really lies on
    # y^2 = f6(x) and mu(x,y) really equals the intended branch value.
    for pt in fin_detail["points"]:
        curve_residual = sp.simplify(pt["y"] ** 2 - f6.subs(X, pt["x"]))
        mu_residual = sp.simplify(a.subs(X, pt["x"]) + p.subs(X, pt["x"]) * pt["y"] - pt["branch_value"])
        if curve_residual != 0 or mu_residual != 0:
            return {"status": "curve-consistency-failure",
                    "diagnostics": {**diagnostics,
                                     "curve_residual": str(curve_residual),
                                     "mu_residual": str(mu_residual)}}

    inf = _infinity_local_orders(a_coeffs, p_coeffs, f6_coeffs, series_cap=series_cap)
    diagnostics["infinity_construction_status"] = inf.get("status")
    if inf.get("status") != "ok":
        return {"status": "infinity-construction-failed", "diagnostics": {**diagnostics, "infinity_detail": inf}}

    plus_order = inf["plus_branch"]["local_order_of_mu"]
    minus_order = inf["minus_branch"]["local_order_of_mu"]

    orientation_derivation = {
        "plus_branch_local_order": plus_order,
        "minus_branch_local_order": minus_order,
        "matches_Or_hypothesis": (plus_order == -5 and minus_order == 5),
        "note": ("(Or) predicts one branch order -5 (pole, P_infty) and the other "
                 "+5 (zero, P_0); this is a per-candidate computed finding, not a "
                 "general theorem re-derivation, and is NOT wired into any "
                 "REJECT/ACCEPT gate by this module."),
    }

    ram = []
    branch_mult = {}

    s_key = _canon(fin_detail["s"])
    ms_key = _canon(fin_detail["ms"])

    for pt in fin_detail["points"]:
        bkey = s_key if pt["branch_label"] == "plus_s" else ms_key
        ram.append({
            "point": f"finite:{_canon(pt['x'])}:{pt['branch_label']}",
            "kind": "finite",
            "x_srepr": _canon(pt["x"]),
            "y_srepr": _canon(pt["y"]),
            "maps_to_branch_value": bkey,
            "multiplicity": 1,
        })
        branch_mult[bkey] = branch_mult.get(bkey, 0) + 1

    if orientation_derivation["matches_Or_hypothesis"]:
        zero_key, pole_key = "0", "infinity"
    else:
        # anomaly: do not force a labelling that isn't backed by the
        # computed local orders. Use neutral labels and leave branch
        # mapping unresolved (reported honestly).
        zero_key, pole_key = "infinity-branch-UNRESOLVED-order-anomaly", "infinity-branch-UNRESOLVED-order-anomaly-2"

    ram.append({
        "point": "infinity:minus_branch",
        "kind": "infinity",
        "computed_local_order_of_mu": minus_order,
        "maps_to_branch_value": zero_key,
        "multiplicity": 4,
    })
    branch_mult[zero_key] = branch_mult.get(zero_key, 0) + 4

    ram.append({
        "point": "infinity:plus_branch",
        "kind": "infinity",
        "computed_local_order_of_mu": plus_order,
        "maps_to_branch_value": pole_key,
        "multiplicity": 4,
    })
    branch_mult[pole_key] = branch_mult.get(pole_key, 0) + 4

    branch_divisor = [{"branch_value": k, "multiplicity": v} for k, v in sorted(branch_mult.items())]

    # rootpart(a) restricted to the two double-root's multiplicities plus
    # the remaining simple root -- exactly [2,2,1] under T-1 (verified via
    # sympy factor_list here, independent of ninfty-checker.py's own
    # from-scratch Yun implementation).
    factor_mults = sorted((m for (_f, m) in sp.factor_list(a)[1]), reverse=True)
    # factor_list groups by IRREDUCIBLE factor, not by root; expand to a
    # root-multiset using each irreducible factor's degree.
    rootpart = []
    for (f, m) in sp.factor_list(a)[1]:
        rootpart += [m] * sp.degree(f, X)
    rootpart = sorted(rootpart, reverse=True)

    finite_aggregate_partitions = {s_key: rootpart, ms_key: rootpart}

    artifact_core = {
        "ramification_divisor_on_C": sorted(ram, key=lambda e: e["point"]),
        "branch_divisor_on_P1": branch_divisor,
        "finite_aggregate_partitions": finite_aggregate_partitions,
    }
    digest = sha256_of(artifact_core)

    return {
        "status": "ok",
        "checker_native_id": CHECKER_NATIVE_ID,
        "algorithm": CHECKER_NATIVE_ALGORITHM_TAG,
        "ramification_divisor_on_C": artifact_core["ramification_divisor_on_C"],
        "branch_divisor_on_P1": artifact_core["branch_divisor_on_P1"],
        "finite_aggregate_partitions": artifact_core["finite_aggregate_partitions"],
        "orientation_derivation": orientation_derivation,
        "infinity_series_detail": inf,
        "native_artifact_digest": digest,
        "diagnostics": diagnostics,
    }


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("candidate_json", help="path to candidate JSON (a,p,f6 coeff lists), or '-' for stdin")
    ap.add_argument("--series-cap", type=int, default=40)
    args = ap.parse_args(argv)

    if args.candidate_json == "-":
        candidate = json.load(sys.stdin)
    else:
        with open(args.candidate_json, "r", encoding="utf-8") as f:
            candidate = json.load(f)

    result = construct_checker_native(candidate["a"], candidate["p"], candidate["f6"],
                                       series_cap=args.series_cap)
    print(canonical_serialize(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
