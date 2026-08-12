#!/usr/bin/env python3
"""Independent exact/modular checker for r13-p1-tier2/v2 certificates.

This file intentionally does not import the producer.  It rebuilds the
normalized system and discriminant factorizations from the source certificate,
then checks every profile at two independently selected good finite-field
specializations.  In the producer these good reductions are exact upper-bound
witnesses, paired with exact discriminant divisibility for the lower bound.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import time
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "search" / "certs" / "r13_p1_1pp_k2_v1_20260812.json"
DEFAULT_CERT = ROOT / "ci" / "out" / "r13_p1_tier2_result.json"
DEFAULT_OUTPUT = ROOT / "ci" / "out" / "r13_p1_tier2_check.json"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def attach_integrity(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("integrity", None)
    result["integrity"] = {
        "canonical_payload_sha256": sha256_bytes(canonical_bytes(result)),
        "definition": "sha256 of canonical UTF-8 JSON after removing the integrity member",
    }
    return result


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(
        json.dumps(attach_integrity(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def verify_integrity(cert: dict[str, Any]) -> bool:
    stored = cert.get("integrity", {}).get("canonical_payload_sha256")
    payload = copy.deepcopy(cert)
    payload.pop("integrity", None)
    return stored == sha256_bytes(canonical_bytes(payload))


def primitive_coefficients(poly: sp.Poly) -> list[int]:
    p = sp.Poly(poly, *poly.gens, domain=sp.QQ)
    denominator = 1
    for q in p.all_coeffs():
        denominator = math.lcm(denominator, int(q.q))
    values = [int(q * denominator) for q in p.all_coeffs()]
    content = 0
    for value in values:
        content = math.gcd(content, abs(value))
    if content:
        values = [value // content for value in values]
    if values and values[0] < 0:
        values = [-value for value in values]
    return values


def polynomial_sha(poly: sp.Poly) -> str:
    return sha256_bytes(canonical_bytes(primitive_coefficients(poly)))


def rebuild(source: dict[str, Any]):
    z, a, b, r = sp.symbols("z a b r")
    local = {"a": a, "b": b}
    g = z**8
    for index in range(8):
        expression = sp.sympify(source["g_solutions_in_terms_of_ab"][f"g{index}"], locals=local)
        g += expression.subs({a: 1, b: r}) * z**index
    q = sp.Poly((z - 1) * (z - r) * g**2, z)
    h = q.nth(9)
    gamma = sp.Poly(
        sp.sympify(source["step1"]["ninth_equation"], locals=local).subs({a: 1, b: r}),
        r,
        domain=sp.QQ,
    )
    assert gamma == sp.Poly(h - 2, r, domain=sp.QQ)
    constant = q.nth(0) - h**2 / 4
    coeff1 = [constant] + [q.nth(i) for i in range(1, 9)]
    coeff2 = [constant] + [q.nth(i) for i in range(1, 9)] + [2 * h]
    s1 = sp.Poly.from_list(list(reversed(coeff1)), gens=z)
    s2 = sp.Poly.from_list(list(reversed(coeff2)), gens=z)
    return z, r, h, constant, coeff1, coeff2, s1, s2


def factor_map(poly: sp.Poly, z: sp.Symbol, r: sp.Symbol, branch: str):
    disc = sp.Poly(sp.discriminant(poly, z), r, domain=sp.QQ)
    content, factors = sp.factor_list(disc.as_expr(), r)
    reconstructed = sp.Poly(content, r, domain=sp.QQ)
    result = {}
    for factor, exponent in factors:
        p = sp.Poly(factor, r, domain=sp.QQ)
        reconstructed *= p**exponent
        result[polynomial_sha(p)] = {
            "poly": p,
            "branch": branch,
            "exponent": int(exponent),
        }
    assert reconstructed == disc
    return disc, result


def rational_mod(value: sp.Rational, prime: int) -> int:
    numerator = int(value.p) % prime
    denominator = int(value.q) % prime
    if denominator == 0:
        raise ZeroDivisionError
    return numerator * pow(denominator, -1, prime) % prime


def evaluate_expression_mod(expression: sp.Expr, r: sp.Symbol, value: int, prime: int) -> int:
    poly = sp.Poly(expression, r, domain=sp.QQ)
    result = 0
    for coefficient in poly.all_coeffs():
        result = (result * value + rational_mod(coefficient, prime)) % prime
    return result


def modular_poly(
    coefficients: list[sp.Expr], r: sp.Symbol, value: int, prime: int, z: sp.Symbol
) -> sp.Poly:
    expression = sum(
        evaluate_expression_mod(coefficient, r, value, prime) * z**degree
        for degree, coefficient in enumerate(coefficients)
    )
    return sp.Poly(expression, z, modulus=prime)


def profile_mod(poly: sp.Poly) -> tuple[list[dict[str, int]], int]:
    _, factors = sp.sqf_list(poly)
    profile = [
        {"multiplicity": int(multiplicity), "distinct_root_degree": factor.degree()}
        for factor, multiplicity in factors
    ]
    odd = sum(
        row["distinct_root_degree"]
        for row in profile
        if row["multiplicity"] % 2 == 1
    )
    return profile, odd


def modular_checks_for_factor(
    factor: sp.Poly,
    expected: tuple[int, int],
    coeff1: list[sp.Expr],
    coeff2: list[sp.Expr],
    r: sp.Symbol,
    z: sp.Symbol,
) -> dict[str, Any]:
    accepted = []
    rejected = []
    derivative = factor.diff()
    for prime in list(sp.primerange(5, 2000)):
        roots = []
        for value in range(prime):
            if int(factor.eval(value)) % prime == 0 and int(derivative.eval(value)) % prime != 0:
                roots.append(value)
        for value in roots:
            p1 = modular_poly(coeff1, r, value, prime, z)
            p2 = modular_poly(coeff2, r, value, prime, z)
            if p1.degree() != 8 or p2.degree() != 9 or sp.gcd(p1, p2).degree() != 0:
                rejected.append({"prime": prime, "r": value, "reason": "degree_or_coprimality"})
                continue
            profile1, odd1 = profile_mod(p1)
            profile2, odd2 = profile_mod(p2)
            row = {
                "prime": prime,
                "r": value,
                "observed": [odd1, odd2],
                "S1_profile": profile1,
                "S2_profile": profile2,
            }
            if (odd1, odd2) == expected:
                accepted.append(row)
                break
            row["reason"] = "extra_collision_or_profile_mismatch"
            rejected.append(row)
        if len(accepted) >= 2:
            break
    if len(accepted) < 2:
        raise RuntimeError(f"could not find two good modular checks for factor {polynomial_sha(factor)}")
    return {
        "expected": list(expected),
        "good_specializations": accepted,
        "rejected_specialization_count": len(rejected),
        "two_good_specializations_found": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--cert", type=Path, default=DEFAULT_CERT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    source = json.loads(args.input.read_text(encoding="utf-8"))
    cert = json.loads(args.cert.read_text(encoding="utf-8"))
    if cert.get("status") != "COMPLETE":
        raise RuntimeError("producer certificate is not COMPLETE")

    z, r, h, constant, coeff1, coeff2, s1, s2 = rebuild(source)
    disc1, factors1 = factor_map(s1, z, r, "I")
    disc2, factors2 = factor_map(s2, z, r, "II")
    all_factors = dict(factors1)
    for factor_sha, row in factors2.items():
        if factor_sha in all_factors:
            all_factors[factor_sha] = {
                "poly": row["poly"],
                "branch": "I+II",
                "exponent": [all_factors[factor_sha]["exponent"], row["exponent"]],
            }
        else:
            all_factors[factor_sha] = row

    producer_rows = cert["candidate_factor_classifications"]
    modular = []
    excluded_sha = {
        sha
        for sha, item in all_factors.items()
        if primitive_coefficients(item["poly"]) == [1, -1]
    }
    expected_classified_sha = set(all_factors) - excluded_sha
    producer_sha = {row["polynomial_sha256"] for row in producer_rows}
    factor_rows_match = producer_sha == expected_classified_sha
    for row in producer_rows:
        factor_sha = row["polynomial_sha256"]
        if factor_sha not in all_factors:
            factor_rows_match = False
            continue
        factor = all_factors[factor_sha]["poly"]
        factor_rows_match &= (
            primitive_coefficients(factor)
            == row["primitive_integer_coefficients_high_to_low"]
        )
        modular.append(
            {
                "factor_id": row["factor_id"],
                **modular_checks_for_factor(
                    factor,
                    tuple(row["odd_root_profile"]),
                    coeff1,
                    coeff2,
                    r,
                    z,
                ),
            }
        )

    excluded_r1 = any(
        item["primitive_integer_coefficients_high_to_low"] == [1, -1]
        for item in cert["excluded_factors"]
    )
    producer_branch_factorizations_match = True
    for branch_name, rebuilt in (("branch_I", factors1), ("branch_II", factors2)):
        expected = {
            factor_sha: row["exponent"] for factor_sha, row in rebuilt.items()
        }
        observed = {
            row["polynomial_sha256"]: row["exponent"]
            for row in cert[branch_name]["factors"]
        }
        producer_branch_factorizations_match &= expected == observed

    requested_layers = {(2, 7), (4, 5), (6, 3), (8, 1)}
    recomputed_layer_counts = {f"({a},{b})": 0 for a, b in sorted(requested_layers)}
    for row in producer_rows:
        layer = tuple(row["odd_root_profile"])
        if row["admissible_candidate_factor"] and layer in requested_layers:
            recomputed_layer_counts[f"({layer[0]},{layer[1]})"] += row[
                "point_enumeration"
            ]["ordered_points_over_Qbar"]
    raw = cert["raw_result"]
    producer_raw_counts_match = (
        raw["candidate_factor_count_after_open_conditions"]
        == sum(bool(row["admissible_candidate_factor"]) for row in producer_rows)
        and raw["candidate_ordered_point_count_before_genus_sieve"]
        == sum(
            row["point_enumeration"]["ordered_points_over_Qbar"]
            for row in producer_rows
            if row["admissible_candidate_factor"]
        )
        and raw["requested_layer_ordered_point_counts"] == recomputed_layer_counts
        and raw["surviving_factor_count"]
        == sum(bool(row["requested_layer"]) for row in producer_rows)
        and raw["surviving_ordered_point_count"]
        == sum(
            row["point_enumeration"]["ordered_points_over_Qbar"]
            for row in producer_rows
            if row["requested_layer"]
        )
    )
    result = {
        "schema": "r13-p1-tier2-check/v1",
        "status": "COMPLETE",
        "generated_by": {
            "script": str(Path(__file__).resolve().relative_to(ROOT)),
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "github_sha": os.environ.get("GITHUB_SHA"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        },
        "inputs": {
            "source_sha256": sha256_file(args.input),
            "producer_cert_sha256": sha256_file(args.cert),
        },
        "checks": {
            "producer_payload_integrity": verify_integrity(cert),
            "producer_source_hash_matches": cert["input"]["sha256"] == sha256_file(args.input),
            "disc_I_degree": disc1.degree(),
            "disc_II_degree": disc2.degree(),
            "producer_disc_degrees_match": (
                cert["branch_I"]["degree"] == disc1.degree()
                and cert["branch_II"]["degree"] == disc2.degree()
            ),
            "factor_rows_match": bool(factor_rows_match),
            "producer_factor_set_complete": producer_sha == expected_classified_sha,
            "producer_branch_factorizations_match": bool(
                producer_branch_factorizations_match
            ),
            "producer_raw_counts_match": bool(producer_raw_counts_match),
            "r_equals_1_exclusion_present": excluded_r1,
            "modular_profiles": modular,
            "all_modular_profiles_have_two_good_specializations": all(
                row["two_good_specializations_found"] for row in modular
            ),
        },
        "u_touched": False,
        "c_touched": False,
        "floating_point_used_for_decisions": False,
        "elapsed_seconds": time.monotonic() - started,
    }
    booleans = [
        result["checks"]["producer_payload_integrity"],
        result["checks"]["producer_source_hash_matches"],
        result["checks"]["producer_disc_degrees_match"],
        result["checks"]["factor_rows_match"],
        result["checks"]["producer_factor_set_complete"],
        result["checks"]["producer_branch_factorizations_match"],
        result["checks"]["producer_raw_counts_match"],
        result["checks"]["r_equals_1_exclusion_present"],
        result["checks"]["all_modular_profiles_have_two_good_specializations"],
    ]
    result["all_checks_true"] = all(booleans)
    if not result["all_checks_true"]:
        raise RuntimeError("one or more independent checks are false")
    atomic_json(args.output, result)
    print("R13_P1_TIER2_CHECK_DONE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
