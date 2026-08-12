#!/usr/bin/env python3
"""Import-free checker for the exact t3 m=4 certificate.

This file deliberately does not import the producer.  In particular it does
not trust or rerun the producer's Groebner basis.  It derives the four quartic
coefficient equations independently and eliminates them by hand to the
nonzero remainder 645911 modulo h^2-h+1.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def integrity_ok(payload: dict[str, Any]) -> bool:
    stored = payload.get("integrity", {}).get("canonical_payload_sha256")
    candidate = copy.deepcopy(payload)
    candidate.pop("integrity", None)
    return stored == sha256_bytes(canonical_bytes(candidate))


def independent_coefficient_and_obstruction_check() -> dict[str, Any]:
    u, h, alpha, gamma, delta = sp.symbols("u h alpha gamma delta")
    phi = h**2 - h + 1
    square_cubic = u**3 - sp.Rational(9, 4) * h * u**2 + 3 * (h - 1) * u + 1
    identity = sp.Poly(
        sp.expand(
            -4 * u * (alpha + u) ** 3
            - 27 * (gamma + delta * u) ** 2
            + 4 * (u - h / 2) * square_cubic
        ),
        u,
    )

    def red(expr: sp.Expr) -> sp.Expr:
        num, den = sp.together(expr).as_numer_denom()
        num = sp.rem(sp.Poly(num, h), sp.Poly(phi, h)).as_expr()
        den = sp.rem(sp.Poly(den, h), sp.Poly(phi, h)).as_expr()
        return sp.cancel(num / den)

    raw = [red(identity.nth(j)) for j in range(5)]
    normalized_expected = [
        27 * gamma**2 + 2 * h,
        2 * alpha**3 + 27 * gamma * delta - 5,
        8 * alpha**2 + 18 * delta**2 - 11 * h + 11,
        12 * alpha + 11 * h,
    ]
    # Each raw coefficient need only be a nonzero rational unit multiple of
    # its normalized equation.
    coefficient_matches = []
    for got, expected in zip(raw[:4], normalized_expected):
        quotient = sp.cancel(got / expected)
        coefficient_matches.append(bool(quotient.free_symbols.isdisjoint({alpha, gamma, delta, h}) and quotient != 0))

    # e3 gives alpha=-11h/12; e0 gives gamma^2=-2h/27; squaring e1 then
    # substituting into e2 produces the following necessary equality.
    aval = -sp.Rational(11, 12) * h
    necessary = 8 * aval**2 - (5 - 2 * aval**3) ** 2 / (3 * h) - 11 * h + 11
    numerator = sp.together(necessary).as_numer_denom()[0]
    remainder = sp.rem(sp.Poly(numerator, h), sp.Poly(phi, h)).as_expr()
    norm = sp.resultant(remainder, phi, h)
    return {
        "raw_coefficients": [str(x) for x in raw],
        "normalized_coefficients_match_up_to_units": all(coefficient_matches),
        "necessary_numerator_remainder_mod_phi6": str(remainder),
        "remainder_norm": str(norm),
        "contradiction_is_nonzero": bool(remainder != 0 and norm != 0),
    }


def independent_positive_control() -> dict[str, Any]:
    u = sp.symbols("u")
    lhs = -4 * u * (-4 + u) ** 3 - 27 * (1 + u) ** 2
    square_cubic = (4 * u**3 - 44 * u**2 + 175 * u - 27) / 4
    residual = sp.expand(lhs + 4 * (u - 1) * square_cubic)
    return {
        "planted_identity_residual": str(residual),
        "pass": residual == 0,
    }


def independent_two_torsion_reduction() -> dict[str, Any]:
    """Give an independent good-reduction irreducibility witness over F_73."""
    u = sp.symbols("u")
    prime = 73
    zeta36 = 25
    order = sp.n_order(zeta36, prime)
    h = pow(zeta36, 6, prime)
    inv4 = pow(4, -1, prime)
    reduced = sp.Poly(
        u**3 + ((-9 * h * inv4) % prime) * u**2 + ((3 * (h - 1)) % prime) * u + 1,
        u,
        modulus=prime,
    )
    factors = sp.factor_list(reduced, modulus=prime)[1]
    degrees = [factor.degree() for factor, exponent in factors for _ in range(exponent)]
    return {
        "prime": prime,
        "zeta36": zeta36,
        "zeta36_order": int(order),
        "h": h,
        "reduced_cubic": str(reduced.as_expr()),
        "factor_degrees": degrees,
        "irreducible": degrees == [3],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cert", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    cert = json.loads(args.cert.read_text(encoding="utf-8"))
    elimination = independent_coefficient_and_obstruction_check()
    control = independent_positive_control()
    two_torsion = independent_two_torsion_reduction()
    quarantine = cert.get("quarantine", {})
    checks = {
        "producer_integrity_valid": integrity_ok(cert),
        "schema_correct": cert.get("schema") == "r13-p1d/v1",
        "producer_reports_unit_ideal": cert.get("D_2_m4_ansatz", {}).get("elimination", {}).get("unit_ideal") is True,
        "producer_reports_m4_no_solution": cert.get("m4_solution_exists_over_F9") is False,
        "independent_elimination": elimination,
        "independent_positive_control": control,
        "independent_F9_two_torsion_gate": two_torsion,
        "quarantine_exact": {
            "name_collide_note_present": quarantine.get("name_collide_note")
            == "K^(9) window instance, separate from the sealed K^(5) quantity, ruling 1007",
            "n5_value_computed_false": quarantine.get("n5_value_computed") is False,
            "derivation_bridge_found_false": quarantine.get("derivation_bridge_found") is False,
            "b34_handled_as_divisor_true": quarantine.get("b34_handled_as_divisor") is True,
            "square_class_is_function_field": quarantine.get("discriminant_square_class_field")
            == "F9(E)^x/(F9(E)^x)^2 (function field square class)",
        },
    }
    all_true = bool(
        checks["producer_integrity_valid"]
        and checks["schema_correct"]
        and checks["producer_reports_unit_ideal"]
        and checks["producer_reports_m4_no_solution"]
        and elimination["normalized_coefficients_match_up_to_units"]
        and elimination["contradiction_is_nonzero"]
        and control["pass"]
        and two_torsion["irreducible"]
        and two_torsion["zeta36_order"] == 36
        and all(checks["quarantine_exact"].values())
    )
    result = {
        "schema": "r13-p1d-check/v1",
        "cert_path": str(args.cert),
        "checks": checks,
        "all_checks_true": all_true,
        "classification": "cross-check of exact candidate computation; not Lean verification",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"T3_M4_CHECK_{'PASS' if all_true else 'FAIL'}", flush=True)
    return 0 if all_true else 1


if __name__ == "__main__":
    raise SystemExit(main())
