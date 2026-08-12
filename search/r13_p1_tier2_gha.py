#!/usr/bin/env python3
"""Exact Tier-2 elimination for the four remaining W9 k=2 strata.

The original v1 script formed a large bivariate resultant and used SIGALRM.
This replacement uses the residual scaling action before elimination.  Put

    r = b/a,  w = a*z,
    Q0(z,r) = (z-1)(z-r) g(z;1,r)^2,
    H(r) = [z^9] Q0.

The step-1 equation is a^9 H(r)=2.  Since P=Q-w^18-1 (the -1 is essential),
the two normalized discriminant factors are

    S1 = Q0 - (z^9 + H/2)^2,   deg_z S1 <= 8,
    S2 = Q0 - (z^9 - H/2)^2,   deg_z S2  = 9.

Thus candidate ratios are roots of the two univariate discriminants in r.
For each irreducible factor f, discriminant divisibility gives the exact lower
bound deg(gcd(S,S')) >= 1.  A degree-preserving good reduction at a simple
root of f with gcd degree one gives the exact upper bound <= 1 (specialization
can only increase gcd degree).  Together these prove the characteristic-zero
profile.  No floating-point decision is made.  Earlier number-field rows may
also be reused after a full integrity and coefficient-system check.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
from functools import reduce
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time
import traceback
from typing import Any, Iterable

import sympy as sp

try:
    import flint
    from flint import fmpq
    from flint.types._gr import gr_nf_ctx
except ImportError:  # A structured incomplete certificate is written below.
    flint = None
    fmpq = None
    gr_nf_ctx = None


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "search" / "certs" / "r13_p1_1pp_k2_v1_20260812.json"
DEFAULT_OUTPUT = ROOT / "ci" / "out" / "r13_p1_tier2_result.json"
DEFAULT_CHECKPOINT = ROOT / "ci" / "out" / "r13_p1_tier2_math_checkpoint.json"
TARGET_LAYERS = {(2, 7), (4, 5), (6, 3), (8, 1)}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def json_compatible(value: Any) -> Any:
    """Normalize exact-algebra objects before any checkpoint serialization."""
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
        return {str(key): json_compatible(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_compatible(item) for item in value]
    raise TypeError(f"unsupported JSON checkpoint value: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def with_integrity(payload: dict[str, Any]) -> dict[str, Any]:
    result = json_compatible(copy.deepcopy(payload))
    result.pop("integrity", None)
    result["integrity"] = {
        "canonical_payload_sha256": sha256_bytes(canonical_bytes(result)),
        "definition": "sha256 of canonical UTF-8 JSON after removing the integrity member",
    }
    return result


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    final_payload = with_integrity(payload)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(
        json.dumps(final_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def payload_integrity_is_valid(payload: dict[str, Any]) -> bool:
    stored = payload.get("integrity", {}).get("canonical_payload_sha256")
    candidate = copy.deepcopy(payload)
    candidate.pop("integrity", None)
    return stored == sha256_bytes(canonical_bytes(candidate))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument(
        "--resume-from",
        type=Path,
        help="integrity-checked earlier v2 checkpoint whose completed factor rows may be reused",
    )
    return parser.parse_args()


def rational_coefficients(poly: sp.Poly) -> list[str]:
    p = sp.Poly(poly, *poly.gens, domain=sp.QQ)
    return [str(q) for q in p.all_coeffs()]


def primitive_integer_coefficients(poly: sp.Poly) -> list[int]:
    p = sp.Poly(poly, *poly.gens, domain=sp.QQ)
    coeffs = p.all_coeffs()
    denominator = 1
    for q in coeffs:
        denominator = math.lcm(denominator, int(q.q))
    integers = [int(q * denominator) for q in coeffs]
    content = reduce(math.gcd, (abs(x) for x in integers if x), 0)
    if content:
        integers = [x // content for x in integers]
    if integers and integers[0] < 0:
        integers = [-x for x in integers]
    return integers


def polynomial_id(poly: sp.Poly) -> str:
    coeffs = primitive_integer_coefficients(poly)
    return sha256_bytes(canonical_bytes(coeffs))


def coefficient_system_digest(coefficients: list[sp.Expr], r: sp.Symbol) -> str:
    payload = []
    for z_degree, coefficient in enumerate(coefficients):
        p = sp.Poly(coefficient, r, domain=sp.QQ)
        payload.append(
            {
                "z_degree": z_degree,
                "r_degree": p.degree() if not p.is_zero else -1,
                "r_coefficients_high_to_low": rational_coefficients(p),
            }
        )
    return sha256_bytes(canonical_bytes(payload))


def build_normalized_system(source: dict[str, Any]) -> dict[str, Any]:
    z, a, b, r = sp.symbols("z a b r")
    local = {"a": a, "b": b}
    g_values: dict[str, sp.Expr] = {}
    homogeneity: dict[str, bool] = {}
    for name, text in source["g_solutions_in_terms_of_ab"].items():
        expr = sp.sympify(text, locals=local)
        index = int(name[1:])
        expected_degree = 8 - index
        homogeneity[name] = all(
            sum(monomial) == expected_degree
            for monomial, _ in sp.Poly(expr, a, b, domain=sp.QQ).terms()
        )
        g_values[name] = expr.subs({a: 1, b: r})

    g = z**8 + sum(g_values[f"g{i}"] * z**i for i in range(8))
    q0 = sp.Poly((z - 1) * (z - r) * g * g, z)
    h = q0.nth(9)

    input_gamma = sp.Poly(
        sp.sympify(source["step1"]["ninth_equation"], locals=local).subs({a: 1, b: r}),
        r,
        domain=sp.QQ,
    )
    derived_gamma = sp.Poly(h - 2, r, domain=sp.QQ)
    gamma_matches = input_gamma == derived_gamma

    # P=Q-w^18-1.  After w=a*z and a^9*H=2, one has a^-18=H^2/4.
    constant = q0.nth(0) - h * h / 4
    s1_coefficients = [constant] + [q0.nth(i) for i in range(1, 9)]
    s2_coefficients = [constant] + [q0.nth(i) for i in range(1, 9)] + [2 * h]
    s1 = sp.Poly.from_list(list(reversed(s1_coefficients)), gens=z)
    s2 = sp.Poly.from_list(list(reversed(s2_coefficients)), gens=z)

    assert gamma_matches
    assert all(homogeneity.values())
    assert s1.degree() == 8
    assert s2.degree() == 9
    assert sp.Poly(s2.as_expr() - s1.as_expr() - 2 * h * z**9, z).is_zero

    return {
        "z": z,
        "r": r,
        "q0": q0,
        "h": h,
        "gamma": input_gamma,
        "s1": s1,
        "s2": s2,
        "s1_coefficients": s1_coefficients,
        "s2_coefficients": s2_coefficients,
        "constant": constant,
        "metadata": {
            "g_coefficient_homogeneity": homogeneity,
            "input_gamma_equals_H_minus_2": gamma_matches,
            "gamma_degree_r": input_gamma.degree(),
            "H_degree_r": sp.degree(h, r),
            "S1_degree_z": s1.degree(),
            "S2_degree_z": s2.degree(),
            "S2_minus_S1_equals_2H_z9": True,
            "constant_term_correction": "P=Q-w^18-1; normalized constant is [z^0]Q0-H(r)^2/4",
            "S1_coefficient_system_sha256": coefficient_system_digest(s1_coefficients, r),
            "S2_coefficient_system_sha256": coefficient_system_digest(s2_coefficients, r),
        },
    }


def factor_discriminant(poly: sp.Poly, z: sp.Symbol, r: sp.Symbol) -> dict[str, Any]:
    started = time.monotonic()
    discriminant = sp.Poly(sp.discriminant(poly, z), r, domain=sp.QQ)
    content, factors = sp.factor_list(discriminant.as_expr(), r)
    factor_rows = []
    reconstructed = sp.Poly(content, r, domain=sp.QQ)
    for factor, exponent in factors:
        p = sp.Poly(factor, r, domain=sp.QQ)
        reconstructed *= p**exponent
        coefficients = primitive_integer_coefficients(p)
        factor_rows.append(
            {
                "poly": p,
                "degree": p.degree(),
                "exponent": int(exponent),
                "primitive_integer_coefficients_high_to_low": coefficients,
                "polynomial_sha256": sha256_bytes(canonical_bytes(coefficients)),
                "reciprocal": coefficients == list(reversed(coefficients)),
            }
        )
    assert reconstructed == discriminant
    return {
        "poly": discriminant,
        "degree": discriminant.degree(),
        "term_count": len(discriminant.terms()),
        "factorization_reconstructs_discriminant": True,
        "factors": factor_rows,
        "elapsed_seconds": time.monotonic() - started,
    }


class NumberFieldOps:
    def __init__(self, factor: sp.Poly, r: sp.Symbol):
        if gr_nf_ctx is None or fmpq is None:
            raise RuntimeError("python-flint is required for exact number-field classification")
        monic = sp.Poly(factor, r, domain=sp.QQ).monic()
        low_to_high = []
        for q in reversed(monic.all_coeffs()):
            low_to_high.append(fmpq(int(q.p), int(q.q)))
        self.context = gr_nf_ctx.new(low_to_high)
        self.alpha = self.context.gen()
        self.r = r

    def from_expr(self, value: sp.Expr):
        p = sp.Poly(value, self.r, domain=sp.QQ)
        result = self.context(0)
        for q in p.all_coeffs():
            result = result * self.alpha + self.context(fmpq(int(q.p), int(q.q)))
        return result

    def zero(self):
        return self.context(0)

    def one(self):
        return self.context(1)

    @staticmethod
    def is_zero(value) -> bool:
        result = value.is_zero()
        if result is None:
            raise RuntimeError("number-field zero test returned UNKNOWN")
        return bool(result)


def trim(poly: list[Any], field: NumberFieldOps) -> list[Any]:
    while poly and field.is_zero(poly[-1]):
        poly.pop()
    return poly


def monic(poly: list[Any], field: NumberFieldOps) -> list[Any]:
    result = trim(poly[:], field)
    if not result:
        return []
    inverse = field.one() / result[-1]
    return trim([coefficient * inverse for coefficient in result], field)


def polynomial_divmod(
    dividend: list[Any], divisor: list[Any], field: NumberFieldOps
) -> tuple[list[Any], list[Any]]:
    remainder = trim(dividend[:], field)
    divisor = trim(divisor[:], field)
    if not divisor:
        raise ZeroDivisionError("zero polynomial divisor")
    if len(remainder) < len(divisor):
        return [], remainder
    quotient = [field.zero() for _ in range(len(remainder) - len(divisor) + 1)]
    inverse_lead = field.one() / divisor[-1]
    while remainder and len(remainder) >= len(divisor):
        shift = len(remainder) - len(divisor)
        coefficient = remainder[-1] * inverse_lead
        quotient[shift] = coefficient
        for j, divisor_coefficient in enumerate(divisor):
            remainder[j + shift] = remainder[j + shift] - coefficient * divisor_coefficient
        trim(remainder, field)
    return trim(quotient, field), remainder


def polynomial_gcd(left: list[Any], right: list[Any], field: NumberFieldOps) -> list[Any]:
    left = trim(left[:], field)
    right = trim(right[:], field)
    while right:
        _, remainder = polynomial_divmod(left, right, field)
        left, right = right, remainder
    return monic(left, field)


def derivative(poly: list[Any], field: NumberFieldOps) -> list[Any]:
    return trim([field.context(i) * poly[i] for i in range(1, len(poly))], field)


def squarefree_profile(poly: list[Any], field: NumberFieldOps) -> list[dict[str, int]]:
    source = monic(poly, field)
    repeated = polynomial_gcd(source, derivative(source, field), field)
    squarefree, remainder = polynomial_divmod(source, repeated, field)
    assert not remainder
    profile: list[dict[str, int]] = []
    multiplicity = 1
    while len(squarefree) > 1:
        common = polynomial_gcd(squarefree, repeated, field)
        exact_factor, remainder = polynomial_divmod(squarefree, common, field)
        assert not remainder
        if len(exact_factor) > 1:
            profile.append(
                {"multiplicity": multiplicity, "distinct_root_degree": len(exact_factor) - 1}
            )
        squarefree = common
        repeated, remainder = polynomial_divmod(repeated, common, field)
        assert not remainder
        multiplicity += 1
        if multiplicity > 20:
            raise RuntimeError("squarefree decomposition exceeded degree bound")
    return profile


def odd_root_count(profile: list[dict[str, int]]) -> int:
    return sum(
        row["distinct_root_degree"]
        for row in profile
        if row["multiplicity"] % 2 == 1
    )


def rational_mod(value: sp.Rational, prime: int) -> int:
    numerator = int(value.p) % prime
    denominator = int(value.q) % prime
    if denominator == 0:
        raise ZeroDivisionError
    return numerator * pow(denominator, -1, prime) % prime


def evaluate_expression_mod(
    expression: sp.Expr, r: sp.Symbol, value: int, prime: int
) -> int:
    poly = sp.Poly(expression, r, domain=sp.QQ)
    result = 0
    for coefficient in poly.all_coeffs():
        result = (result * value + rational_mod(coefficient, prime)) % prime
    return result


def modular_polynomial(
    coefficients: list[sp.Expr],
    r: sp.Symbol,
    value: int,
    prime: int,
    z: sp.Symbol,
) -> sp.Poly:
    reduced = [
        evaluate_expression_mod(coefficient, r, value, prime)
        for coefficient in coefficients
    ]
    return sp.Poly.from_list(list(reversed(reduced)), gens=z, modulus=prime)


def quotient_remainder_nonzero(
    expression: sp.Expr, factor: sp.Poly, r: sp.Symbol
) -> bool:
    remainder = sp.rem(
        sp.Poly(expression, r, domain=sp.QQ),
        sp.Poly(factor, r, domain=sp.QQ),
    )
    return not remainder.is_zero


def good_reduction_gcd_one_witnesses(
    factor: sp.Poly,
    coefficients: list[sp.Expr],
    expected_degree: int,
    r: sp.Symbol,
    z: sp.Symbol,
    count: int = 2,
) -> list[dict[str, Any]]:
    integer_factor = sp.Poly.from_list(
        primitive_integer_coefficients(factor), gens=r, domain=sp.ZZ
    )
    derivative_factor = integer_factor.diff()
    witnesses = []
    for prime in sp.primerange(5, 2000):
        if int(integer_factor.LC()) % prime == 0:
            continue
        for value in range(prime):
            factor_value = int(integer_factor.eval(value)) % prime
            derivative_value = int(derivative_factor.eval(value)) % prime
            if factor_value != 0 or derivative_value == 0:
                continue
            try:
                polynomial = modular_polynomial(coefficients, r, value, prime, z)
            except ZeroDivisionError:
                continue
            if polynomial.degree() != expected_degree:
                continue
            gcd = sp.gcd(polynomial, polynomial.diff())
            if gcd.degree() != 1:
                continue
            witnesses.append(
                {
                    "prime": int(prime),
                    "ratio_root": int(value),
                    "factor_value_mod_prime": factor_value,
                    "factor_derivative_value_mod_prime": derivative_value,
                    "degree_preserved": True,
                    "gcd_with_derivative_degree": gcd.degree(),
                    "polynomial_coefficients_high_to_low_mod_prime": [
                        int(coefficient) % prime for coefficient in polynomial.all_coeffs()
                    ],
                    "gcd_coefficients_high_to_low_mod_prime": [
                        int(coefficient) % prime for coefficient in gcd.monic().all_coeffs()
                    ],
                }
            )
            break
        if len(witnesses) >= count:
            return witnesses
    raise RuntimeError(
        f"could not find {count} exact good-reduction witnesses for {polynomial_id(factor)}"
    )


def synthetic_polynomial(odd: int, degree: int, start: int, x: sp.Symbol) -> sp.Poly:
    expression: sp.Expr = sp.Integer(1)
    next_root = start
    for _ in range(odd):
        expression *= x - next_root
        next_root += 1
    for _ in range((degree - odd) // 2):
        expression *= (x - next_root) ** 2
        next_root += 1
    return sp.Poly(expression, x, domain=sp.QQ)


def sympy_squarefree_profile(poly: sp.Poly) -> list[dict[str, int]]:
    _, factors = sp.sqf_list(poly)
    return [
        {"multiplicity": int(multiplicity), "distinct_root_degree": factor.degree()}
        for factor, multiplicity in factors
    ]


def artificial_layer_controls() -> list[dict[str, Any]]:
    x = sp.symbols("x")
    rows = []
    for index, layer in enumerate([(0, 9), (2, 7), (4, 5), (6, 3), (8, 1)]):
        p1 = synthetic_polynomial(layer[0], 8, 100 * index + 1, x)
        p2 = synthetic_polynomial(layer[1], 9, 100 * index + 30, x)
        profile1 = sympy_squarefree_profile(p1)
        profile2 = sympy_squarefree_profile(p2)
        observed = (odd_root_count(profile1), odd_root_count(profile2))
        rows.append(
            {
                "expected_layer": list(layer),
                "observed_layer": list(observed),
                "matches_expected": observed == layer,
                "S1_profile": profile1,
                "S2_profile": profile2,
            }
        )
    assert all(row["matches_expected"] for row in rows)
    return rows


def reproduce_layer_0_9_empty() -> dict[str, Any]:
    started = time.monotonic()
    w = sp.symbols("w")
    rho_p, rho_m = sp.symbols("rho_p rho_m")
    gp = sp.symbols("gp0 gp1 gp2 gp3")
    gm = sp.symbols("gm0 gm1 gm2 gm3")
    unknowns = [rho_p, rho_m] + list(gp) + list(gm)
    g_plus = w**4 + gp[3] * w**3 + gp[2] * w**2 + gp[1] * w + gp[0]
    g_minus = w**4 + gm[3] * w**3 + gm[2] * w**2 + gm[1] * w + gm[0]
    up = sp.Poly((w - rho_p) * g_plus**2, w)
    um = sp.Poly((w - rho_m) * g_minus**2, w)
    equations = [up.nth(j) for j in (8, 7, 6, 5)]
    equations += [um.nth(j) for j in (8, 7, 6, 5)]
    equations += [up.nth(j) + um.nth(j) for j in (4, 3, 2, 1)]
    equations.append(up.nth(0) + um.nth(0) - 2)
    basis = sp.groebner(equations, *unknowns, order="grevlex")
    unit_basis = len(basis.polys) == 1 and basis.polys[0].as_expr() == 1
    assert unit_basis
    return {
        "source_run_id": 31578468586,
        "num_equations": len(equations),
        "num_unknowns": len(unknowns),
        "groebner_basis": [str(poly.as_expr()) for poly in basis.polys],
        "basis_is_unit": unit_basis,
        "elapsed_seconds": time.monotonic() - started,
    }


def classify_factor(
    factor: sp.Poly,
    memberships: list[dict[str, Any]],
    system: dict[str, Any],
) -> dict[str, Any]:
    r = system["r"]
    z = system["z"]
    started = time.monotonic()
    branches = {membership["branch"] for membership in memberships}
    h_nonzero = quotient_remainder_nonzero(system["h"], factor, r)
    c0_nonzero = quotient_remainder_nonzero(system["constant"], factor, r)
    s1_degree_8 = quotient_remainder_nonzero(
        system["s1_coefficients"][-1], factor, r
    )
    s2_degree_9 = quotient_remainder_nonzero(
        system["s2_coefficients"][-1], factor, r
    )

    profile_proofs: dict[str, Any] = {}
    if "I" in branches:
        witnesses = good_reduction_gcd_one_witnesses(
            factor, system["s1_coefficients"], 8, r, z
        )
        profile1 = [
            {"multiplicity": 1, "distinct_root_degree": 6},
            {"multiplicity": 2, "distinct_root_degree": 1},
        ]
        profile_proofs["S1"] = {
            "lower_bound": "f divides the exactly reconstructed discriminant, so gcd(S1,dS1) has degree at least 1",
            "upper_bound": "a degree-preserving simple-root reduction has gcd degree 1; specialization can only increase gcd degree",
            "characteristic_zero_gcd_degree": 1,
            "good_reduction_witnesses": witnesses,
        }
    else:
        profile1 = [{"multiplicity": 1, "distinct_root_degree": 8}]
        profile_proofs["S1"] = {
            "proof": "f is absent from the exact irreducible factorization of disc(S1)",
            "characteristic_zero_gcd_degree": 0,
        }

    if "II" in branches:
        witnesses = good_reduction_gcd_one_witnesses(
            factor, system["s2_coefficients"], 9, r, z
        )
        profile2 = [
            {"multiplicity": 1, "distinct_root_degree": 7},
            {"multiplicity": 2, "distinct_root_degree": 1},
        ]
        profile_proofs["S2"] = {
            "lower_bound": "f divides the exactly reconstructed discriminant, so gcd(S2,dS2) has degree at least 1",
            "upper_bound": "a degree-preserving simple-root reduction has gcd degree 1; specialization can only increase gcd degree",
            "characteristic_zero_gcd_degree": 1,
            "good_reduction_witnesses": witnesses,
        }
    else:
        profile2 = [{"multiplicity": 1, "distinct_root_degree": 9}]
        profile_proofs["S2"] = {
            "proof": "f is absent from the exact irreducible factorization of disc(S2)",
            "characteristic_zero_gcd_degree": 0,
        }

    observed = (odd_root_count(profile1), odd_root_count(profile2))
    coefficients = primitive_integer_coefficients(factor)
    factor_sha = sha256_bytes(canonical_bytes(coefficients))
    degree = factor.degree()
    admissible = (
        degree > 1
        and h_nonzero
        and c0_nonzero
        and s1_degree_8
        and s2_degree_9
    )
    return {
        "factor_id": factor_sha[:16],
        "polynomial_sha256": factor_sha,
        "primitive_integer_coefficients_high_to_low": coefficients,
        "factor_degree": degree,
        "branch_memberships": memberships,
        "reciprocal": coefficients == list(reversed(coefficients)),
        "point_enumeration": {
            "ratio_equation": f"factor_{factor_sha[:16]}(r)=0",
            "scale_equation": "a^9*H(r)-2=0",
            "second_coordinate_equation": "b-r*a=0",
            "ordered_points_over_Qbar": 9 * degree,
            "mu9_orbits": degree,
            "mu9_and_swap_orbits": degree // 2 if coefficients == list(reversed(coefficients)) else None,
        },
        "open_conditions": {
            "a_not_zero_from_scale_equation": h_nonzero,
            "a_not_equal_b": degree > 1,
            "H_nonzero": h_nonzero,
            "c0_nonzero": c0_nonzero,
            "S1_degree_8": s1_degree_8,
            "S2_degree_9": s2_degree_9,
            "gcd_S1_S2_degree": 0,
            "gcd_S1_S2_proof": "S2-S1=2*H*z^9; a common root would be z=0, contradicted by c0!=0",
        },
        "admissible_candidate_factor": admissible,
        "S1_squarefree_profile": profile1,
        "S2_squarefree_profile": profile2,
        "exact_profile_proofs": profile_proofs,
        "odd_root_profile": list(observed),
        "odd_root_total": sum(observed),
        "requested_layer": admissible and observed in TARGET_LAYERS,
        "elapsed_seconds": time.monotonic() - started,
    }


def validated_resume_rows(
    path: Path,
    source_path: Path,
    state: dict[str, Any],
    combined: dict[tuple[int, ...], dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not payload_integrity_is_valid(payload):
        raise RuntimeError("resume checkpoint payload integrity mismatch")
    if payload.get("schema") != "r13-p1-tier2/v2":
        raise RuntimeError("resume checkpoint schema mismatch")
    if payload.get("input", {}).get("sha256") != sha256_file(source_path):
        raise RuntimeError("resume checkpoint source hash mismatch")

    metadata_keys = (
        "S1_coefficient_system_sha256",
        "S2_coefficient_system_sha256",
        "constant_term_correction",
    )
    for key in metadata_keys:
        if payload.get("normalized_system", {}).get(key) != state.get(
            "normalized_system", {}
        ).get(key):
            raise RuntimeError(f"resume normalized-system mismatch: {key}")

    for branch in ("branch_I", "branch_II"):
        cached = payload.get(branch, {})
        current = state.get(branch, {})
        for key in ("degree", "term_count", "factorization_reconstructs_discriminant"):
            if cached.get(key) != current.get(key):
                raise RuntimeError(f"resume {branch} mismatch: {key}")
        if cached.get("factors") != current.get("factors"):
            raise RuntimeError(f"resume {branch} factor rows mismatch")

    current_by_sha: dict[str, dict[str, Any]] = {}
    for coefficients, record in combined.items():
        factor_sha = sha256_bytes(canonical_bytes(list(coefficients)))
        current_by_sha[factor_sha] = {
            "coefficients": list(coefficients),
            "factor": record["poly"],
            "memberships": record["memberships"],
        }

    rows: dict[str, dict[str, Any]] = {}
    for cached_row in payload.get("candidate_factor_classifications", []):
        factor_sha = cached_row.get("polynomial_sha256")
        if factor_sha not in current_by_sha:
            raise RuntimeError(f"resume classification has unknown factor: {factor_sha}")
        current = current_by_sha[factor_sha]
        if cached_row.get("primitive_integer_coefficients_high_to_low") != current[
            "coefficients"
        ]:
            raise RuntimeError(f"resume classification coefficient mismatch: {factor_sha}")
        if cached_row.get("factor_degree") != current["factor"].degree():
            raise RuntimeError(f"resume classification degree mismatch: {factor_sha}")
        if cached_row.get("branch_memberships") != current["memberships"]:
            raise RuntimeError(f"resume classification membership mismatch: {factor_sha}")
        observed = (
            odd_root_count(cached_row.get("S1_squarefree_profile", [])),
            odd_root_count(cached_row.get("S2_squarefree_profile", [])),
        )
        if cached_row.get("odd_root_profile") != list(observed):
            raise RuntimeError(f"resume classification profile mismatch: {factor_sha}")
        expected_requested = bool(cached_row.get("admissible_candidate_factor")) and (
            observed in TARGET_LAYERS
        )
        if cached_row.get("requested_layer") != expected_requested:
            raise RuntimeError(f"resume requested-layer mismatch: {factor_sha}")
        rows[factor_sha] = copy.deepcopy(cached_row)

    provenance = {
        "path": str(path.relative_to(ROOT)),
        "file_sha256": sha256_file(path),
        "payload_integrity_valid": True,
        "source_github_run_id": payload.get("generated_by", {}).get("github_run_id"),
        "source_github_sha": payload.get("generated_by", {}).get("github_sha"),
        "source_script_sha256": payload.get("generated_by", {}).get("script_sha256"),
        "imported_factor_ids": sorted(row["factor_id"] for row in rows.values()),
    }
    return rows, provenance


def main() -> int:
    args = parse_args()
    start = time.monotonic()
    source_path = args.input.resolve()
    output_path = args.output.resolve()
    checkpoint_path = args.checkpoint.resolve()
    source = json.loads(source_path.read_text(encoding="utf-8"))
    state: dict[str, Any] = {
        "schema": "r13-p1-tier2/v2",
        "generated_by": {
            "script": str(Path(__file__).resolve().relative_to(ROOT)),
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "python_flint": getattr(flint, "__version__", None),
            "platform": platform.platform(),
            "github_sha": os.environ.get("GITHUB_SHA"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        },
        "input": {
            "path": str(source_path.relative_to(ROOT)),
            "sha256": sha256_file(source_path),
            "schema": source.get("schema"),
        },
        "scope": {
            "window": "K^(9)",
            "k": 2,
            "previous_layer": [0, 9],
            "requested_layers": [list(layer) for layer in sorted(TARGET_LAYERS)],
            "decisions_are_exact": True,
            "floating_point_used_for_decisions": False,
            "u_touched": False,
            "c_touched": False,
            "preregistered_value_computation": False,
        },
        "status": "INCOMPLETE",
        "progress": {"stage": "INPUT_LOADED", "updated_at_utc": utc_now()},
        "started_at_utc": utc_now(),
    }

    def checkpoint(stage: str) -> None:
        state["progress"] = {
            "stage": stage,
            "updated_at_utc": utc_now(),
            "elapsed_seconds": time.monotonic() - start,
        }
        atomic_write_json(checkpoint_path, state)
        print(f"W9_TIER2_CHECKPOINT stage={stage}", flush=True)

    checkpoint("INPUT_LOADED")
    try:
        system = build_normalized_system(source)
        state["normalized_system"] = system["metadata"]
        state["normalized_system"]["chart"] = (
            "a!=0: r=b/a; a=0 is covered after swapping a,b by r=0; the equations are swap-symmetric"
        )
        checkpoint("NORMALIZED_SYSTEM_DERIVED")

        branch_i = factor_discriminant(system["s1"], system["z"], system["r"])
        state["branch_I"] = {
            key: value for key, value in branch_i.items() if key not in {"poly", "factors"}
        }
        state["branch_I"]["factors"] = [
            {key: value for key, value in row.items() if key != "poly"}
            for row in branch_i["factors"]
        ]
        checkpoint("BRANCH_I_FACTORED")

        branch_ii = factor_discriminant(system["s2"], system["z"], system["r"])
        state["branch_II"] = {
            key: value for key, value in branch_ii.items() if key not in {"poly", "factors"}
        }
        state["branch_II"]["factors"] = [
            {key: value for key, value in row.items() if key != "poly"}
            for row in branch_ii["factors"]
        ]
        checkpoint("BRANCH_II_FACTORED")

        combined: dict[tuple[int, ...], dict[str, Any]] = {}
        for branch_name, branch in (("I", branch_i), ("II", branch_ii)):
            for row in branch["factors"]:
                key = tuple(row["primitive_integer_coefficients_high_to_low"])
                record = combined.setdefault(
                    key,
                    {"poly": row["poly"], "memberships": []},
                )
                record["memberships"].append(
                    {"branch": branch_name, "discriminant_exponent": row["exponent"]}
                )

        resumed_rows: dict[str, dict[str, Any]] = {}
        resume_provenance = None
        if args.resume_from is not None:
            resume_path = args.resume_from.resolve()
            resumed_rows, resume_provenance = validated_resume_rows(
                resume_path, source_path, state, combined
            )
            state["resume"] = resume_provenance
            checkpoint("RESUME_VALIDATED")

        classifications = []
        excluded = []
        for key in sorted(combined, key=lambda item: (len(item), item)):
            record = combined[key]
            factor = record["poly"]
            if factor.degree() == 1 and factor.eval(1) == 0:
                excluded.append(
                    {
                        "reason": "r=1 gives a=b, contrary to the two distinct simple roots at t=1",
                        "primitive_integer_coefficients_high_to_low": list(key),
                        "branch_memberships": record["memberships"],
                    }
                )
                continue
            factor_sha = sha256_bytes(canonical_bytes(list(key)))
            if factor_sha in resumed_rows:
                row = copy.deepcopy(resumed_rows[factor_sha])
                row["classification_provenance"] = {
                    "mode": "integrity_checked_resume",
                    "checkpoint_file_sha256": resume_provenance["file_sha256"],
                    "source_github_run_id": resume_provenance["source_github_run_id"],
                    "source_github_sha": resume_provenance["source_github_sha"],
                }
                stage_prefix = "RESUMED"
            else:
                row = classify_factor(factor, record["memberships"], system)
                row["classification_provenance"] = {"mode": "computed_in_this_run"}
                stage_prefix = "CLASSIFIED"
            classifications.append(row)
            state["candidate_factor_classifications"] = classifications
            state["excluded_factors"] = excluded
            checkpoint(f"{stage_prefix}_{row['factor_id']}")

        layer_counts = {f"({a},{b})": 0 for a, b in sorted(TARGET_LAYERS)}
        survivor_factor_count = 0
        survivor_ordered_point_count = 0
        for row in classifications:
            layer = tuple(row["odd_root_profile"])
            if row["requested_layer"]:
                survivor_factor_count += 1
                survivor_ordered_point_count += row["point_enumeration"]["ordered_points_over_Qbar"]
                layer_counts[f"({layer[0]},{layer[1]})"] += row["point_enumeration"][
                    "ordered_points_over_Qbar"
                ]

        controls = {
            "artificial_solvable_layers": artificial_layer_controls(),
            "known_layer_0_9_reproduction": reproduce_layer_0_9_empty(),
        }
        controls["all_artificial_layers_match"] = all(
            row["matches_expected"] for row in controls["artificial_solvable_layers"]
        )
        controls["known_layer_0_9_basis_is_unit"] = controls[
            "known_layer_0_9_reproduction"
        ]["basis_is_unit"]
        state["calibration"] = controls
        state["raw_result"] = {
            "candidate_factor_count_after_open_conditions": sum(
                bool(row["admissible_candidate_factor"]) for row in classifications
            ),
            "candidate_ordered_point_count_before_genus_sieve": sum(
                row["point_enumeration"]["ordered_points_over_Qbar"]
                for row in classifications
                if row["admissible_candidate_factor"]
            ),
            "requested_layer_ordered_point_counts": layer_counts,
            "surviving_factor_count": survivor_factor_count,
            "surviving_ordered_point_count": survivor_ordered_point_count,
        }
        state["status"] = "COMPLETE"
        state["completed_at_utc"] = utc_now()
        state["elapsed_seconds"] = time.monotonic() - start
        checkpoint("COMPLETE")
        atomic_write_json(output_path, state)
        print("R13_P1_TIER2_DONE", flush=True)
        return 0
    except BaseException as exc:
        state["status"] = "INCOMPLETE"
        state["stop_reason"] = f"{type(exc).__name__}: {exc}"
        state["traceback"] = traceback.format_exc()
        state["elapsed_seconds"] = time.monotonic() - start
        state["completed_at_utc"] = utc_now()
        atomic_write_json(checkpoint_path, state)
        atomic_write_json(output_path, state)
        print(f"R13_P1_TIER2_INCOMPLETE reason={state['stop_reason']}", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
