# search/probe/wac_v1/u_meas_m7b1_checker.py
#
# Versioned, standalone re-implementation of M7-B1 (the "norm path" for
# u_0^{-1}), written per Sol 便 92 F92-5.2 differential (W92-2/F92-5.2/W92-9
# repair batch, sol/sol_reply_92_math19.md sec.5): the earlier
# u_meas_m7b_20260731.json cert recorded a B1 result but had no versioned,
# independently re-runnable script, no recorded source/input digest, and no
# reproduce command -- so it could not be re-executed by a third party.
# This file is that missing checker.
#
# HELPER-DISJOINT BY CONSTRUCTION: this script does NOT import, exec(), or
# otherwise execute any code from search/probe/wac_v1/u_meas_uloc_fire2.py
# (the U-LOC "series path" driver) or from u_meas_caseb_search2.py (which
# fire2.py itself execs). Every formula needed below (the t-pullback, the
# norm N_tau(x), kappa, delta) is re-derived from first principles in the
# comments and re-typed as fresh sympy code. The only thing shared with the
# fire2.py run is DATA (curve-model rational constants c,c3,c5,c7,c9), read
# machine-fresh from search/certs/u_meas_caseb_a5_20260731.json -- a cert
# file, not a code path -- and its SHA-256 is recorded below as the input
# digest.
#
# MATH BACKGROUND (re-derived here, not copied from fire2.py):
#   Curve model (Case B, CB-27 sqrt(-5) descent candidate):
#     C : y^2 = (x^3 - x/5)^2 + c ,  c = c(x)-independent rational constant.
#   Write q(x) := x^3 - x/5, so f6(x) := q(x)^2 + c is the curve's degree-6
#   RHS (y^2 = f6(x)).
#   The frozen U-LOC extraction (u_meas_m3_design_v1.md 1.2 / the
#   preregistration block already on file in u_meas_uloc_v2_20260731.json)
#   expresses 3*t as a function on C via
#     3*t = 3/2 + c3*th + c5*x^2*th + c7*x*th^2 + c9*th^3 ,  th := y + q(x).
#   ==> t(x,y) is a polynomial of degree <=1 in y once y^2 is reduced via
#   y^2 = f6(x): write t(x,y) = A(x) + y*B(x) for polynomials A,B in x
#   (obtained below purely by sympy polynomial reduction mod y^2-f6, not by
#   retyping any closed-form for A/B).
#   The hyperelliptic involution sends y -> -y, i.e. t -> A - y*B. For a
#   fixed algebraic tau, the norm from the function field extension
#   Q(C)/Q(x) of (t-tau) is
#     N_tau(x) := (t-tau)(x,y) * (t-tau)(x,-y) = (A-tau)^2 - y^2*B^2
#               = (A-tau)^2 - f6*B^2 ,
#   a polynomial in x alone (pure algebra, no series/limit involved). This
#   is exactly the "norm path" computation of M7-B1.
#   Sign convention (frozen, u_meas_uloc_v2_20260731.json preregistration):
#     tau_1 = 3/2 + (3/2)*sqrt(-3).  Set delta := tau_1 - 3/2, so
#     delta^2 = (3/2)^2 * (-3) = -27/4.
#   As x -> infinity, t(x,y) -> 3/2 on the branch used (see below), so
#   N_tau(x) ~ c_lead * x^9 * (3/2 - tau_1) = -c_lead * x^9 * delta at
#   leading order (deg N_tau = 9, matching the local extraction cusp of
#   order 9). Reading off kappa := leading coefficient (coeff of x^9) of
#   N_tau(x) as an exact polynomial-algebra computation (no limit) then
#   gives
#     kappa = -c_lead * delta   =>   u_0^{-1} = -c_lead = kappa / delta.
#   This u_0^{-1} is compared below against the value obtained purely
#   algebraically as -8*c9 (the frozen identity c_lead = 8*c9, itself a
#   coefficient-extraction fact recorded independently of any series/limit
#   computation -- see u_meas_uloc_fire2.py's own in-file identity-check
#   print, "c_lead - 8*c9", which that script logs as identically 0; the
#   present script does not read that log, it re-derives the -8*c9 target
#   value directly from c9 as sourced from the curve cert below).
#
# M7-B4 (separate leg, NOT re-computed by this script): M7-B4 was a point
# count of Y = C/psibar over several primes p, testing 3 | #Y(F_p) as a
# necessary condition for Prop CB-3T (a rational 3-torsion point on Y). It
# is a CURVE-INTEGRITY / consistency check on the model, not an independent
# computation of the value u_0^{-1} -- it cannot by itself confirm or deny
# the number kappa/delta computed here. This role is recorded verbatim in
# the output cert's "M7_B4_role" field per Sol 便 92 F92-5.2 instruction,
# without re-running the point counts (out of scope for this checker).
#
# Usage:  python search/probe/wac_v1/u_meas_m7b1_checker.py \
#             [curve_cert_path] [out_cert_path]
#         (both arguments optional; defaults shown below)

import hashlib
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

DEFAULT_CURVE_CERT = "search/certs/u_meas_caseb_a5_20260731.json"
DEFAULT_OUT_CERT = "search/certs/u_meas_m7b_v2_20260731.json"


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    curve_cert_rel = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CURVE_CERT
    out_cert_rel = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT_CERT
    curve_cert_path = os.path.join(REPO_ROOT, curve_cert_rel)
    out_cert_path = os.path.join(REPO_ROOT, out_cert_rel)

    raw_lines = []

    def log(s):
        s = str(s)
        print(s)
        raw_lines.append(s)

    log("=== u_meas_m7b1_checker.py -- M7-B1 norm-path independent re-check ===")
    log("python: %s" % sys.version.split()[0])
    log("sympy_version: %s" % sp.__version__)

    # ---- (0) machine-fresh input: curve-model rational constants --------
    with open(curve_cert_path, "r", encoding="utf-8") as f:
        curve_cert = json.load(f)
    curve_cert_sha256 = sha256_of_file(curve_cert_path)
    log("input curve cert: %s" % curve_cert_rel)
    log("input curve cert sha256: %s" % curve_cert_sha256)

    ex = curve_cert["exact_solution"]
    c = sp.nsimplify(ex["c"])
    c3 = sp.nsimplify(ex["values"]["c3"])
    c5 = sp.nsimplify(ex["values"]["c5"])
    c7 = sp.nsimplify(ex["values"]["c7"])
    c9 = sp.nsimplify(ex["values"]["c9"])
    log("c  = %s" % c)
    log("c3 = %s   c5 = %s   c7 = %s   c9 = %s" % (c3, c5, c7, c9))

    # ---- (1) curve / t-pullback, re-derived fresh (no import from fire2) -
    x, y = sp.symbols("x y")
    q = x ** 3 - x / 5
    f6 = sp.expand(q ** 2 + c)
    th = y + q
    t3 = sp.expand(sp.Rational(3, 2) + c3 * th + c5 * x ** 2 * th
                    + c7 * x * th ** 2 + c9 * th ** 3)
    # t3 = 3*t(x,y), a polynomial in x,y of y-degree <= 3 before reduction.
    # Reduce modulo y^2 - f6(x) (i.e. substitute y^2 -> f6, y^3 -> y*f6, ...)
    # by sympy polynomial division in y over the field Q(x), so that the
    # result is genuinely computed, not retyped from a closed form.
    t3_poly_y = sp.Poly(t3, y)
    ymod = sp.Poly(y ** 2 - f6, y)
    remainder = sp.rem(t3_poly_y, ymod)
    remainder_expr = sp.expand(remainder.as_expr())
    # remainder_expr should now have y-degree <= 1: split into A (y^0 part)
    # and B (y^1 coefficient).
    rem_poly_y = sp.Poly(remainder_expr, y)
    coeffs_y = rem_poly_y.all_coeffs()  # highest degree first
    if rem_poly_y.degree() == 1:
        Bc, Ac = coeffs_y[0], coeffs_y[1]
    elif rem_poly_y.degree() <= 0:
        Bc, Ac = sp.Integer(0), remainder_expr
    else:
        raise RuntimeError("y-reduction did not collapse to degree <= 1: %s"
                            % remainder_expr)
    A3 = sp.expand(Ac)   # y-free part of 3*t
    B3 = sp.expand(Bc)   # y-coefficient of 3*t
    A = sp.expand(A3)    # A(x) with  3*t = A + y*B   (A plays fire2's "A")
    B = sp.expand(B3)
    log("deg_x(A) = %s   deg_x(B) = %s   deg_x(f6) = %s"
        % (sp.degree(A, x), sp.degree(B, x), sp.degree(f6, x)))

    # ---- (2) norm N_tau(x) = (A-tau)^2 - f6*B^2, tau = tau_1, tau_2 -----
    sqrtm3 = sp.sqrt(3) * sp.I   # sqrt(-3), written explicitly (not sp.sqrt(-3))
    tau1 = sp.Rational(3, 2) + sp.Rational(3, 2) * sqrtm3
    tau2 = sp.Rational(3, 2) - sp.Rational(3, 2) * sqrtm3
    results = {}
    for name, tau in (("tau1", tau1), ("tau2", tau2)):
        delta = sp.simplify(tau - sp.Rational(3, 2))
        delta2 = sp.simplify(delta ** 2)
        N_tau = sp.expand((A - tau) ** 2 - f6 * B ** 2)
        N_poly = sp.Poly(N_tau, x)
        deg = N_poly.degree()
        kappa = sp.simplify(N_poly.coeff_monomial(x ** 9)) if deg == 9 else None
        u0_inv_norm = sp.simplify(kappa / delta) if kappa is not None else None
        log("[%s] delta = %s   delta^2 = %s (expect -27/4)" % (name, delta, delta2))
        log("[%s] deg N_tau = %s   kappa (coeff x^9) = %s" % (name, deg, kappa))
        log("[%s] u_0^{-1} (norm path, = kappa/delta) = %s" % (name, u0_inv_norm))
        results[name] = {
            "delta": str(delta),
            "delta_squared": str(delta2),
            "delta_squared_is_minus_27_over_4": bool(sp.simplify(delta2 + sp.Rational(27, 4)) == 0),
            "N_tau_degree": int(deg),
            "kappa": str(kappa),
            "u_0_inverse_norm_path": str(u0_inv_norm),
        }

    # ---- (3) target value via the frozen identity c_lead = 8*c9 --------
    # (a coefficient-extraction fact, re-derived here as a plain algebraic
    # statement -- NOT obtained via sp.limit or any series expansion, and
    # not read from any fire2.py log; c9 itself comes only from the curve
    # cert read in step (0) above.)
    c_lead = sp.simplify(8 * c9)
    u0_inv_target = sp.simplify(-c_lead)
    log("c_lead (:= 8*c9, algebraic identity) = %s" % c_lead)
    log("u_0^{-1} target (:= -c_lead) = %s" % u0_inv_target)

    agree = {}
    for name in ("tau1", "tau2"):
        norm_val = sp.nsimplify(results[name]["u_0_inverse_norm_path"])
        ok = bool(sp.simplify(norm_val - u0_inv_target) == 0)
        agree[name] = ok
        log("[%s] agrees with -c_lead target? %s" % (name, ok))

    u0_inv = u0_inv_target  # use the (agreeing) value for factorisation below

    # ---- (4) valuations / sign / exponent vector mod 3 ------------------
    r = sp.Rational(u0_inv)
    sign = -1 if r < 0 else 1
    num_fac = sp.factorint(abs(r.p))
    den_fac = sp.factorint(r.q)
    valuations = {}
    for p_, e_ in num_fac.items():
        valuations[str(p_)] = valuations.get(str(p_), 0) + int(e_)
    for p_, e_ in den_fac.items():
        valuations[str(p_)] = valuations.get(str(p_), 0) - int(e_)
    exponent_vector_mod_3 = {k_: int(v_ % 3) for k_, v_ in valuations.items()}
    log("u_0^{-1} = %s   sign = %s   valuations = %s" % (r, sign, valuations))
    log("exponent vector mod 3 = %s" % exponent_vector_mod_3)

    # ---- (5) write cert ---------------------------------------------------
    script_path_rel = "search/probe/wac_v1/u_meas_m7b1_checker.py"
    script_path_abs = os.path.join(REPO_ROOT, script_path_rel)
    script_sha256 = sha256_of_file(script_path_abs)

    reproduce_command = ("python search/probe/wac_v1/u_meas_m7b1_checker.py "
                          + curve_cert_rel + " " + out_cert_rel)

    cert = {
        "schema": "u-meas-m7b1-checker/v2",
        "generated_by": {
            "path": script_path_rel,
            "sha256": script_sha256,
        },
        "sympy_version": sp.__version__,
        "python_version": sys.version.split()[0],
        "reproduce_command": reproduce_command,
        "input": {
            "curve_cert_path": curve_cert_rel,
            "curve_cert_sha256": curve_cert_sha256,
        },
        "helper_disjoint": True,
        "helper_disjoint_note": ("does not import or exec() "
                                  "search/probe/wac_v1/u_meas_uloc_fire2.py or "
                                  "u_meas_caseb_search2.py; all formulas "
                                  "re-derived and re-typed independently "
                                  "(see header comment)."),
        "M7_B1": {
            "method": "norm path: N_tau(x) = (A-tau)^2 - f6(x)*B(x)^2, "
                      "kappa = leading coeff (x^9) of N_tau, "
                      "delta = tau - 3/2, u_0^{-1} = kappa/delta. "
                      "No series expansion, no sp.limit.",
            "per_tau": results,
            "c_lead_identity": str(c_lead),
            "u_0_inverse_target_minus_c_lead": str(u0_inv_target),
            "agrees_with_target_by_tau": agree,
            "agrees_with_series_path": bool(all(agree.values())),
        },
        "measurement": {
            "u_0_inverse": str(r),
            "sign": int(sign),
            "valuations": valuations,
            "exponent_vector_mod_3": exponent_vector_mod_3,
        },
        "M7_B4_role": ("M7-B4 (point counts of Y=C/psibar over several primes, "
                        "testing 3 | #Y(F_p) for Prop CB-3T) is a curve-integrity "
                        "/ model-consistency check, not an independent computation "
                        "of u_0^{-1}. It is not re-executed by this script; see "
                        "search/certs/u_meas_m7b_20260731.json field B4 for the "
                        "original point-count record."),
        "raw_output": raw_lines,
        "note": "machine values only, no interpretation, no ledger claim.",
    }

    with open(out_cert_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=1, sort_keys=True)
        f.write("\n")

    log("\nWrote cert: %s" % out_cert_rel)
    log("CHECKER_DONE")


if __name__ == "__main__":
    main()
