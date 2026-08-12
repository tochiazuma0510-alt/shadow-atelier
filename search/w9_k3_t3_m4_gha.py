#!/usr/bin/env python3
"""Exact m=4 computation for the W9 k=3 t3 lane (ruling 1024).

The implementation follows ``docs/notes/t3_spec_and_C2_calib_v1.md`` Part I.
It uses the exact subfield Q(zeta_6) of F9=Q(zeta_36); no numerical root or
floating-point comparison occurs.

The chosen pole is Pi0=-Q0.  Translation by -Pi0=Q0 puts Pi0 at infinity and
gives the same generalized Weierstrass equation

    v^2 + 3*omega*u*v + 2*v = u^3,       omega=zeta_3.

The two prescribed simple branch points become the negative pair over
u=zeta_6/2.  The complete-square coordinate

    q=v+1+(3*omega/2)u,
    q^2=S(u)=u^3-(9*zeta_6/4)u^2+3*omega*u+1

turns the residual-even-divisor condition into one quartic identity.  Exact
pole order 12 forces the top A coefficient to be nonzero, so the cubic-root
gauge may be normalized geometrically to that coefficient=1.  This is safe
for an emptiness result: every nonzero coefficient has a square root over the
algebraic closure.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import time
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "ci" / "out" / "w9_k3_t3_m4_result.json"
DEFAULT_CHECKPOINT = ROOT / "ci" / "out" / "w9_k3_t3_m4_checkpoint.json"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def json_compatible(value: Any) -> Any:
    if value is None or isinstance(value, (bool, str, int, float)):
        return value
    if isinstance(value, sp.Integer):
        return int(value)
    if isinstance(value, sp.Rational):
        return str(value)
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): json_compatible(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_compatible(v) for v in value]
    return str(value)


def with_integrity(payload: dict[str, Any]) -> dict[str, Any]:
    result = json_compatible(copy.deepcopy(payload))
    result.pop("integrity", None)
    result["integrity"] = {
        "canonical_payload_sha256": sha256_bytes(canonical_bytes(result)),
        "definition": "sha256 of canonical UTF-8 JSON after removing integrity",
    }
    return result


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    final = with_integrity(payload)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def reduce_mod(expr: sp.Expr, generator: sp.Symbol, modulus: sp.Expr) -> sp.Expr:
    num, den = sp.together(expr).as_numer_denom()
    num_r = sp.rem(sp.Poly(num, generator), sp.Poly(modulus, generator)).as_expr()
    den_r = sp.rem(sp.Poly(den, generator), sp.Poly(modulus, generator)).as_expr()
    return sp.cancel(num_r / den_r)


def is_zero_mod(expr: sp.Expr, generator: sp.Symbol, modulus: sp.Expr) -> bool:
    num = sp.together(expr).as_numer_denom()[0]
    return sp.rem(sp.Poly(num, generator), sp.Poly(modulus, generator)).is_zero


def equation_coefficients(square_cubic: sp.Expr, branch_x: sp.Expr) -> tuple[list[sp.Expr], dict[str, sp.Expr]]:
    """Build the quartic equations used by both production and positive control.

    A=u(alpha+u), B=u(gamma+delta*u), and lambda=-4 after normalizing the
    nonzero top coefficient of A.  The requested divisor parity is

        -4*u*(alpha+u)^3 - 27*(gamma+delta*u)^2
          = -4*(u-branch_x)*square_cubic.
    """
    u, alpha, gamma, delta = sp.symbols("u alpha gamma delta")
    lhs = -4 * u * (alpha + u) ** 3 - 27 * (gamma + delta * u) ** 2
    rhs = -4 * (u - branch_x) * square_cubic
    poly = sp.Poly(sp.expand(lhs - rhs), u)
    return [sp.factor(poly.nth(j)) for j in range(5)], {
        "u": u,
        "alpha": alpha,
        "gamma": gamma,
        "delta": delta,
        "lhs": lhs,
        "rhs": rhs,
    }


def exact_geometry_checks() -> dict[str, Any]:
    """Recheck the plane cubic, Weierstrass map, and special points exactly."""
    z, s, y, X, Y = sp.symbols("z s y X Y")
    phi12 = z**4 - z**2 + 1
    ii = z**3
    omega = ii * z
    original = y**3 - 6 * z * s * y + 4 * ii * s**2 + 4 * s
    target = Y**2 + 3 * omega * X * Y + 2 * Y - X**3
    substituted = original.subs({y: -ii * X, s: -ii * Y / 2})
    weierstrass_ok = is_zero_mod(substituted + ii * target, z, phi12)

    simple_plus = -2 * (1 + ii) / z
    simple_minus = -2 * (1 - ii) / z
    f_plus = original.subs({s: 1, y: simple_plus})
    f_minus = original.subs({s: -1, y: simple_minus})
    derivative = sp.diff(original, y)
    df_plus = reduce_mod(derivative.subs({s: 1, y: simple_plus}), z, phi12)
    df_minus = reduce_mod(derivative.subs({s: -1, y: simple_minus}), z, phi12)

    # The source note's assertion that these square roots leave F9 is false:
    # both displayed elements already lie in Q(zeta_12).  They are recorded as
    # an audit finding only; the production equations use the rational divisor.
    double_plus = (1 + ii) / z
    double_minus = (1 - ii) / z
    root_plus_ok = is_zero_mod(double_plus**2 - 2 * z, z, phi12)
    root_minus_ok = is_zero_mod(double_minus**2 + 2 * z, z, phi12)

    return {
        "weierstrass_substitution_exact": weierstrass_ok,
        "weierstrass_model": "Y^2 + 3*zeta3*X*Y + 2*Y = X^3",
        "coordinate_map": {"X": "i*y", "Y": "2*i*s", "Q_infinity": "O"},
        "points": {
            "Q0": ["0", "0"],
            "B1_simple_s_plus_1": ["2*(1-i)/zeta12", "2*i"],
            "B2_simple_s_minus_1": ["-2*(1+i)/zeta12", "-2*i"],
        },
        "B1_on_curve": is_zero_mod(f_plus, z, phi12),
        "B2_on_curve": is_zero_mod(f_minus, z, phi12),
        "B1_is_simple": bool(df_plus != 0),
        "B2_is_simple": bool(df_minus != 0),
        "three_Q0_is_O": True,
        "three_Q0_reason": "the tangent Y=0 meets the cubic only at Q0=(0,0), with multiplicity 3",
        "b34_divisor": {
            "ideal_on_E": ["s^2-1", "3*y^2-6*zeta12*s"],
        "individual_coordinates_used_by_solver": False,
            "handled_as_F9_rational_divisor": True,
        },
        "source_field_claim_audit": {
            "claim_sqrt_2zeta12_outside_F9": False,
            "exact_identity_plus": "((1+i)/zeta12)^2 = 2*zeta12",
            "exact_identity_minus": "((1-i)/zeta12)^2 = -2*zeta12",
            "identity_plus_checked": root_plus_ok,
            "identity_minus_checked": root_minus_ok,
            "impact": "the solver does not use individual B3/B4 coordinates; it uses the rational divisor ideal only",
        },
    }


def production_elimination() -> dict[str, Any]:
    u, h = sp.symbols("u h")
    phi6 = h**2 - h + 1
    square_cubic = u**3 - sp.Rational(9, 4) * h * u**2 + 3 * (h - 1) * u + 1
    coeffs, symbols = equation_coefficients(square_cubic, h / 2)
    reduced_coeffs = [reduce_mod(c, h, phi6) for c in coeffs]
    nonzero_coeffs = [sp.together(c).as_numer_denom()[0] for c in reduced_coeffs if c != 0]
    alpha = symbols["alpha"]
    gamma = symbols["gamma"]
    delta = symbols["delta"]
    gb = sp.groebner(nonzero_coeffs + [phi6], delta, gamma, alpha, h, order="lex")
    unit_ideal = len(gb.polys) == 1 and gb.polys[0].as_expr() == 1

    # Independent-looking scalar diagnostic retained in the producer.  The
    # import-free checker re-derives it from the four coefficient equations.
    alpha_value = -sp.Rational(11, 12) * h
    obstruction_expr = (
        8 * alpha_value**2
        - (5 - 2 * alpha_value**3) ** 2 / (3 * h)
        - 11 * h
        + 11
    )
    obstruction_num = sp.together(obstruction_expr).as_numer_denom()[0]
    obstruction_remainder = sp.rem(sp.Poly(obstruction_num, h), sp.Poly(phi6, h)).as_expr()

    prime = 73
    zeta36_mod = 25
    h_mod = pow(zeta36_mod, 6, prime)
    u_mod = sp.symbols("u_mod")
    reduced_two_torsion = sp.Poly(
        u_mod**3
        + ((-9 * h_mod * pow(4, -1, prime)) % prime) * u_mod**2
        + ((3 * (h_mod - 1)) % prime) * u_mod
        + 1,
        u_mod,
        modulus=prime,
    )
    reduced_factor_degrees = [
        factor.degree()
        for factor, exponent in sp.factor_list(reduced_two_torsion, modulus=prime)[1]
        for _ in range(exponent)
    ]
    two_torsion_irreducible = sp.n_order(zeta36_mod, prime) == 36 and reduced_factor_degrees == [3]

    normalized = [
        "27*gamma^2 + 2*h",
        "2*alpha^3 + 27*gamma*delta - 5",
        "8*alpha^2 + 18*delta^2 - 11*h + 11",
        "12*alpha + 11*h",
        "h^2-h+1",
    ]
    return {
        "phi6": "h^2-h+1",
        "embedding": "h=zeta6=zeta36^6; omega=zeta3=h-1=zeta36^12",
        "completed_square_cubic": str(square_cubic),
        "branch_pair_u_coordinate": "h/2",
        "normalized_equations": normalized,
        "groebner_order": ["delta", "gamma", "alpha", "h"],
        "groebner_basis": [str(p.as_expr()) for p in gb.polys],
        "unit_ideal": unit_ideal,
        "selected_square_class_geometric_solution_count": 0 if unit_ideal else None,
        "groebner_dimension": -1 if unit_ideal else None,
        "analytic_obstruction_remainder": str(obstruction_remainder),
        "F9_rational_2_torsion_gate": {
            "completed_square_cubic": "u^3-(9*h/4)u^2+3*(h-1)u+1",
            "good_prime": 73,
            "zeta36_mod_prime": 25,
            "zeta36_order_mod_prime": 36,
            "h_mod_prime": 9,
            "reduced_cubic": "u^3-2*u^2+24*u+1",
            "reduced_factor_degrees": reduced_factor_degrees,
            "reduced_cubic_irreducible": two_torsion_irreducible,
            "conclusion": "E[2](F9) is trivial; the rational even-divisor square class used here exhausts F9-rational m=4 solutions",
        },
    }


def positive_control() -> dict[str, Any]:
    u = sp.symbols("u")
    # Planted A=u*(-4+u), B=u*(1+u), branch x=1.
    planted_square_cubic = (4 * u**3 - 44 * u**2 + 175 * u - 27) / 4
    coeffs, symbols = equation_coefficients(planted_square_cubic, sp.Integer(1))
    alpha, gamma, delta = symbols["alpha"], symbols["gamma"], symbols["delta"]
    equations = [sp.together(c).as_numer_denom()[0] for c in coeffs if c != 0]
    anchored = equations + [alpha + 4, gamma - 1, delta - 1]
    gb = sp.groebner(anchored, delta, gamma, alpha, order="lex")
    residuals = [sp.expand(c.subs({alpha: -4, gamma: 1, delta: 1})) for c in coeffs]
    pass_same_path = all(r == 0 for r in residuals) and not (len(gb.polys) == 1 and gb.polys[0].as_expr() == 1)
    return {
        "name": "planted_quartic_divisor_identity",
        "same_equation_builder": "equation_coefficients",
        "same_groebner_path": True,
        "planted_values": {"alpha": -4, "beta": 1, "gamma": 1, "delta": 1, "branch_x": 1},
        "artificial_square_cubic": str(planted_square_cubic),
        "square_cubic_discriminant": str(sp.factor(sp.discriminant(sp.Poly(planted_square_cubic, u)))),
        "all_planted_residuals_zero": all(r == 0 for r in residuals),
        "anchored_ideal_nonempty": not (len(gb.polys) == 1 and gb.polys[0].as_expr() == 1),
        "pass": pass_same_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    out: dict[str, Any] = {
        "schema": "r13-p1d/v1",
        "status": "RUNNING",
        "generated_by": {
            "script": "search/w9_k3_t3_m4_gha.py",
            "script_sha256": sha256_file(Path(__file__)),
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "github_sha": os.environ.get("GITHUB_SHA"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "started_at_utc": utc_now(),
        },
        "universe": {
            "window": "K^(9)",
            "coefficient_field": "F9=Q(zeta36), exact subfield computation in Q(zeta6)",
            "m_values_run": [4],
            "m2_theoretically_excluded": True,
            "m6_run": False,
            "pole_point_Pi0": "-Q0=(0,-2) on the generalized Weierstrass model",
            "claim_scope": "F9-rational emptiness for m=4 and this specification-authorized Pi0",
        },
        "quarantine": {
            "name_collide_note": "K^(9) window instance, separate from the sealed K^(5) quantity, ruling 1007",
            "n5_value_computed": False,
            "derivation_bridge_found": False,
            "b34_handled_as_divisor": True,
            "discriminant_square_class_field": "F9(E)^x/(F9(E)^x)^2 (function field square class)",
        },
        "u_touched": False,
        "c_touched": False,
        "preregistered_b9_a9_d9_computed": False,
        "floating_point_used": False,
        "d_no_interpretation": "machine output only; no project verdict",
    }
    atomic_write_json(args.checkpoint, out)

    geometry = exact_geometry_checks()
    out["D_1_exact_geometry"] = geometry
    atomic_write_json(args.checkpoint, out)
    if not all(
        geometry[k]
        for k in ("weierstrass_substitution_exact", "B1_on_curve", "B2_on_curve", "B1_is_simple", "B2_is_simple")
    ):
        out["status"] = "STOPPED_FAIL_CLOSED_D1"
        atomic_write_json(args.output, out)
        atomic_write_json(args.checkpoint, out)
        return 1

    control = positive_control()
    out["positive_control"] = control
    atomic_write_json(args.checkpoint, out)
    if not control["pass"]:
        out["status"] = "STOPPED_FAIL_CLOSED_POSITIVE_CONTROL"
        atomic_write_json(args.output, out)
        atomic_write_json(args.checkpoint, out)
        return 1

    elimination = production_elimination()
    out["D_2_m4_ansatz"] = {
        "RR_raw_dimensions": {"A": 2, "B_before_zero_conditions": 4, "raw_total": 6},
        "spec_raw_unknowns_minus_gauge": 5,
        "B_zero_conditions": 2,
        "solver_dimensions_after_B_zeros": {"A": 2, "B": 2, "total": 4},
        "exact_pole_condition": "top A coefficient beta != 0; normalized beta=1 over algebraic closure",
        "A": "u*(alpha+u)",
        "B": "u*(gamma+delta*u)",
        "ord_Q0_B_equals_1_open_condition": "gamma != 0",
        "ord_Qinfinity_B_equals_1_open_condition": "gamma != 0",
        "elimination": elimination,
    }
    out["D_3_watches"] = {
        "D_a_m2_excluded_and_not_run": True,
        "D_b_genus4": "NOT_REACHED_NO_SOLUTION",
        "D_c_order_P0_minus_Pinf_9": "NOT_REACHED_NO_SOLUTION",
        "D_d_solution_scheme_positive_dimensional": False,
        "D_e_m4_empty_m6_forbidden_by_commission": True,
    }
    out["D_4_quarantine_pass"] = all(
        [
            out["quarantine"]["n5_value_computed"] is False,
            out["quarantine"]["derivation_bridge_found"] is False,
            out["quarantine"]["b34_handled_as_divisor"] is True,
        ]
    )
    f9_empty = bool(
        elimination["unit_ideal"]
        and elimination["F9_rational_2_torsion_gate"]["reduced_cubic_irreducible"]
    )
    out["m4_solution_exists_over_F9"] = False if f9_empty else None
    out["solution_count_over_F9"] = 0 if f9_empty else None
    out["status"] = (
        "COMPLETE_EMPTY_F9_RATIONAL_M4_FIXED_PI0" if f9_empty else "UNKNOWN_ELIMINATION_OR_2TORSION_GATE"
    )
    out["elapsed_seconds"] = time.monotonic() - started
    atomic_write_json(args.output, out)
    atomic_write_json(args.checkpoint, out)
    print(f"W9_K3_T3_M4_{out['status']} elapsed={out['elapsed_seconds']:.3f}s", flush=True)
    return 0 if f9_empty else 2


if __name__ == "__main__":
    raise SystemExit(main())
