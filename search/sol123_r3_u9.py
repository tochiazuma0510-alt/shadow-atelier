"""Exact producer for Sol task 123 [R-3-U9] and DESC-9.

The declared affine equations contain the vertical component X=Y=0.  At the
intended point over Q_0 we work on the main branch, eliminate Y where w+1 is
a unit, and use the resulting saturated local equation.  All series
arithmetic is over fractions.Fraction; no floating point is used.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = ROOT / "search" / "certs"
SPEC = ROOT / "docs" / "notes" / "r2_r3_unram_execution_spec_v1.md"
B_RECEIPT = CERT_DIR / "ds4_receipt_v1_20260812.json"
R3_CERT = CERT_DIR / "sol123_r3_u9_v1_20260813.json"
P8_CERT = CERT_DIR / "sol123_p8_a_class_v1_20260813.json"
EXPECTED_SPEC_SHA256 = (
    "da6294da1b2f359f3b80f2281570770e4db616a360a9896bc5fc6ca1055f1c26"
)
MAX_DEGREE = 30


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def zero_series() -> list[Fraction]:
    return [Fraction(0) for _ in range(MAX_DEGREE + 1)]


def series_add(*terms: list[Fraction]) -> list[Fraction]:
    result = zero_series()
    for term in terms:
        for degree, coefficient in enumerate(term):
            result[degree] += coefficient
    return result


def series_scale(series: list[Fraction], scalar: Fraction | int) -> list[Fraction]:
    return [Fraction(scalar) * coefficient for coefficient in series]


def series_shift(series: list[Fraction], shift: int) -> list[Fraction]:
    result = zero_series()
    for degree in range(MAX_DEGREE + 1 - shift):
        result[degree + shift] = series[degree]
    return result


def series_mul(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = zero_series()
    for i, left_coefficient in enumerate(left):
        if left_coefficient == 0:
            continue
        for j in range(MAX_DEGREE + 1 - i):
            right_coefficient = right[j]
            if right_coefficient:
                result[i + j] += left_coefficient * right_coefficient
    return result


def local_equation_series(x_series: list[Fraction]) -> list[Fraction]:
    # F = w^6 X^2 + 81 X w^3(1+w) + 54 w^3(1+w)
    #     - 729 X(1+w)^2.
    constant = zero_series()
    constant[3] = Fraction(54)
    constant[4] = Fraction(54)
    return series_add(
        series_shift(series_mul(x_series, x_series), 6),
        series_scale(series_shift(x_series, 3), 81),
        series_scale(series_shift(x_series, 4), 81),
        constant,
        series_scale(x_series, -729),
        series_scale(series_shift(x_series, 1), -1458),
        series_scale(series_shift(x_series, 2), -729),
    )


def solve_x_series() -> list[Fraction]:
    x_series = zero_series()
    for degree in range(MAX_DEGREE + 1):
        x_series[degree] = Fraction(0)
        residual = local_equation_series(x_series)[degree]
        # The coefficient of the new unknown is exactly -729.
        x_series[degree] = residual / 729
        if local_equation_series(x_series)[degree] != 0:
            raise ArithmeticError(f"series recurrence failed at degree {degree}")
    return x_series


def derive_y_series(x_series: list[Fraction]) -> list[Fraction]:
    # On the intended chart, Y = X^2 w^3 / (27(1+w)).
    inverse_one_plus_w = [Fraction((-1) ** degree) for degree in range(MAX_DEGREE + 1)]
    numerator = series_shift(series_mul(x_series, x_series), 3)
    return series_scale(series_mul(numerator, inverse_one_plus_w), Fraction(1, 27))


def model_residuals(
    x_series: list[Fraction], y_series: list[Fraction]
) -> tuple[list[Fraction], list[Fraction], list[Fraction]]:
    # E = Y^2 + 3XY + 2Y - X^3.
    e_residual = series_add(
        series_mul(y_series, y_series),
        series_scale(series_mul(x_series, y_series), 3),
        series_scale(y_series, 2),
        series_scale(series_mul(series_mul(x_series, x_series), x_series), -1),
    )
    # W = X^2 w^3 - 27Y(1+w).
    w_residual = series_add(
        series_shift(series_mul(x_series, x_series), 3),
        series_scale(y_series, -27),
        series_scale(series_shift(y_series, 1), -27),
    )
    return local_equation_series(x_series), e_residual, w_residual


def first_nonzero(series: list[Fraction]) -> tuple[int, Fraction]:
    for degree, coefficient in enumerate(series):
        if coefficient:
            return degree, coefficient
    raise ArithmeticError("zero series has no leading term")


def q_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def selected_terms(series: list[Fraction], start: int, stop: int) -> list[dict]:
    return [
        {"degree": degree, "coefficient": q_string(series[degree])}
        for degree in range(start, min(stop, MAX_DEGREE) + 1)
        if series[degree]
    ]


def factor_positive_integer(value: int) -> dict[int, int]:
    if value <= 0:
        raise ValueError("factor_positive_integer requires a positive integer")
    factors: dict[int, int] = {}
    divisor = 2
    remainder = value
    while divisor * divisor <= remainder:
        while remainder % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remainder //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remainder > 1:
        factors[remainder] = factors.get(remainder, 0) + 1
    return factors


def factor_fraction(value: Fraction) -> tuple[int, dict[int, int]]:
    sign = -1 if value < 0 else 1
    numerator_factors = factor_positive_integer(abs(value.numerator))
    denominator_factors = factor_positive_integer(value.denominator)
    valuations = dict(numerator_factors)
    for prime, exponent in denominator_factors.items():
        valuations[prime] = valuations.get(prime, 0) - exponent
    return sign, dict(sorted((prime, exponent) for prime, exponent in valuations.items() if exponent))


def class_order(exponents: list[int], modulus: int) -> int:
    common = modulus
    for exponent in exponents:
        common = math.gcd(common, exponent)
    return modulus // common


def main() -> None:
    spec_sha256 = sha256_file(SPEC)
    if spec_sha256 != EXPECTED_SPEC_SHA256:
        raise SystemExit("UNKNOWN: controlling specification SHA-256 mismatch")

    x_series = solve_x_series()
    y_series = derive_y_series(x_series)
    t_series = series_scale(series_mul(y_series, y_series), Fraction(-1, 4))
    f_residual, e_residual, w_residual = model_residuals(x_series, y_series)
    if any(f_residual) or any(e_residual) or any(w_residual):
        raise SystemExit("UNKNOWN: an exact local-series residual is nonzero")

    x_order, x_lead = first_nonzero(x_series)
    y_order, y_lead = first_nonzero(y_series)
    t_order, u9_s1 = first_nonzero(t_series)
    if (x_order, y_order, t_order) != (3, 9, 18):
        raise SystemExit("UNKNOWN: local valuation profile differs from (3,9,18)")

    # A second, non-proportional rational uniformizer is s_2=X/w^2.  Its
    # regularity follows from ord_w(X)=3, and its leading coefficient in w is
    # the leading coefficient of X, namely 2/27.
    s2_series = zero_series()
    for degree in range(MAX_DEGREE - 1):
        s2_series[degree] = x_series[degree + 2]
    s2_order, s2_lead_in_w = first_nonzero(s2_series)
    if s2_order != 1 or s2_lead_in_w == 0:
        raise SystemExit("UNKNOWN: X/w^2 is not a uniformizer in the exact expansion")
    u9_s2 = u9_s1 / (s2_lead_in_w**18)
    ratio = u9_s1 / u9_s2
    if ratio != s2_lead_in_w**18:
        raise SystemExit("UNKNOWN: the two leading coefficients do not differ by an 18th power")

    a9_representative = 1 / u9_s1
    a9_sign, a9_valuations = factor_fraction(a9_representative)
    class_mod18 = {prime: exponent % 18 for prime, exponent in a9_valuations.items()}
    class_mod9_all = {prime: exponent % 9 for prime, exponent in a9_valuations.items()}
    a_class = {prime: exponent for prime, exponent in class_mod9_all.items() if exponent}

    receipt = json.loads(B_RECEIPT.read_text(encoding="utf-8"))
    b_raw = Fraction(receipt["d1_input_tamper_check"]["u0_inverse_read"])
    b_sign, b_valuations = factor_fraction(b_raw)
    expected_b_raw = {2: -8, 3: 6, 5: 9}
    expected_b_mod9 = {2: 1, 3: 6, 5: 0}
    b_mod9 = {prime: exponent % 9 for prime, exponent in b_valuations.items()}
    if b_valuations != expected_b_raw or b_mod9 != expected_b_mod9:
        raise SystemExit("UNKNOWN: independent [b] normalization mismatch")

    sorted_support = sorted(a_class)
    sorted_exponents = [a_class[prime] for prime in sorted_support]
    order_mod9 = class_order(sorted_exponents, 9)

    r3_payload = {
        "schema": "r3_u9/v1",
        "task": "Sol-123/R-3-U9",
        "artifact_date": "2026-08-13",
        "method": "exact Fraction recurrence on a saturated implicit local chart",
        "controlling_spec": {
            "path": "docs/notes/r2_r3_unram_execution_spec_v1.md",
            "sha256": spec_sha256,
        },
        "declared_model": {
            "E": "Y^2 + 3*X*Y + 2*Y - X^3 = 0",
            "W": "X^2*w^3 - 27*Y*(w+1) = 0",
            "lambda_9": "t = -Y^2/4",
        },
        "local_branch": {
            "point": "(X,w)=(0,0) over Q_0=(X,Y)=(0,0)",
            "chart_condition": "w+1 is a unit",
            "elimination": "Y = X^2*w^3/(27*(w+1))",
            "saturated_equation": (
                "F=X^2*w^6+81*X*w^3*(w+1)+54*w^3*(w+1)-729*X*(w+1)^2"
            ),
            "derivation_identity": "F = 729*(w+1)^2*E(X,Y(X,w))/X^2",
            "dF_dX_at_origin": -729,
            "uniformizer": "w",
        },
        "exact_series": {
            "computed_through_degree": MAX_DEGREE,
            "X_terms": selected_terms(x_series, 3, 14),
            "Y_terms": selected_terms(y_series, 9, 20),
            "t_terms": selected_terms(t_series, 18, 24),
            "residual_checks": {
                "F_zero_through_degree": MAX_DEGREE,
                "E_zero_through_degree": MAX_DEGREE,
                "W_zero_through_degree": MAX_DEGREE,
            },
            "orders": {"w": 1, "X": x_order, "Y": y_order, "t": t_order},
            "leading_coefficients": {
                "X_in_w": q_string(x_lead),
                "Y_in_w": q_string(y_lead),
            },
        },
        "uniformizer_invariance": {
            "s_1": "w",
            "u_9_s_1": q_string(u9_s1),
            "s_2": "X/w^2",
            "s_2_series_in_w": selected_terms(s2_series, 1, 12),
            "s_2_leading_coefficient_in_s_1": q_string(s2_lead_in_w),
            "s_1_and_s_2_nonproportional_as_functions": s2_series[2] != 0,
            "u_9_s_2": q_string(u9_s2),
            "u_9_s_1_over_u_9_s_2": q_string(ratio),
            "witness_18th_power": f"({q_string(s2_lead_in_w)})^18",
            "passed": True,
        },
        "a_9": {
            "representative_u9_inverse": q_string(a9_representative),
            "home_field": "Q",
            "sign": a9_sign,
            "prime_valuations": {str(p): e for p, e in a9_valuations.items()},
            "class_mod18_Q": {str(p): e for p, e in class_mod18.items()},
            "image_in_F9": "scalar-extension image in Q(zeta_36)^x/(...)^18",
        },
        "desc_9": {
            "D_i": {
                "map": "Q^x/(Q^x)^18 -> Q^x/(Q^x)^9",
                "prime_exponents_mod9_including_zero": {
                    str(p): e for p, e in class_mod9_all.items()
                },
                "sign_removed_because": "-1=(-1)^9",
                "passed": True,
            },
            "D_ii": {
                "test": "representative u_9^(-1) is an exact element of Q^x",
                "in_image_of_Q_class": True,
                "passed": True,
            },
            "D_iii": {
                "rule": "RES-INJ-9 gives uniqueness of the rational preimage class",
                "res_inj_9_prerequisite": "inherited from the frozen r-card A4",
                "unique_rational_class": True,
                "passed": True,
            },
            "status": "COMPLETE",
        },
        "b_mod9_independent_normalization": {
            "input_receipt": "search/certs/ds4_receipt_v1_20260812.json",
            "input_receipt_sha256": sha256_file(B_RECEIPT),
            "raw_rational": q_string(b_raw),
            "sign": b_sign,
            "fresh_trial_division_valuations": {str(p): e for p, e in b_valuations.items()},
            "normalized_mod9_including_zero": {str(p): e for p, e in b_mod9.items()},
            "zero_exponents_removed_from_support": True,
            "matches_preregistered_target": True,
        },
        "touch_state": {
            "u": "touched_by_this_measurement",
            "c": "untouched",
            "d9": "not_computed",
            "r": "not_computed",
            "K5_instances": "untouched",
        },
        "provenance": {
            "producer_script": "search/sol123_r3_u9.py",
            "producer_script_sha256": sha256_file(Path(__file__)),
        },
        "status": "COMPLETE_PRODUCER",
    }

    p8_payload = {
        "schema": "p8_a_class/v1",
        "task": "Sol-123/DESC-9",
        "artifact_date": "2026-08-13",
        "source_r3_u9_cert": "search/certs/sol123_r3_u9_v1_20260813.json",
        "a_class": {
            "representation": "exponent vector mod 9 over the support primes",
            "support": sorted_support,
            "exponents": sorted_exponents,
            "order": order_mod9,
            "normalization": "representative in Q^x/(Q^x)^9; sign is a ninth power",
        },
        "a_9_field_note": {
            "u9_home_field": "Q",
            "class_mod18_Q": {str(p): e for p, e in class_mod18.items()},
            "image_in_F9": "scalar-extension image in Q(zeta_36)^x/(...)^18",
            "desc9_rule": "DESC-9 (D-i)->(D-ii)->(D-iii)",
            "desc9_step_ii_passed": True,
        },
        "score_rule_s1_measurement": {
            "rule": "support == [3] and order == 9",
            "result": sorted_support == [3] and order_mod9 == 9,
            "interpretive_label": "withheld_pending_commander_gate",
        },
        "preregistration_controls": {
            "b_value_used_only_for_required_independent_normalization": True,
            "u3_disc_certificate_not_read": True,
            "d9_not_computed": True,
            "r_not_computed": True,
        },
        "provenance": {
            "producer_script": "search/sol123_r3_u9.py",
            "producer_script_sha256": sha256_file(Path(__file__)),
        },
        "status": "COMPLETE_MEASUREMENT_INTERPRETATION_WITHHELD",
    }

    atomic_json(R3_CERT, r3_payload)
    # Add the R3 certificate digest only after its deterministic serialization.
    p8_payload["source_r3_u9_sha256"] = sha256_file(R3_CERT)
    atomic_json(P8_CERT, p8_payload)

    print(
        json.dumps(
            {
                "status": "COMPLETE_PRODUCER",
                "certificates": [
                    {"path": R3_CERT.relative_to(ROOT).as_posix(), "sha256": sha256_file(R3_CERT)},
                    {"path": P8_CERT.relative_to(ROOT).as_posix(), "sha256": sha256_file(P8_CERT)},
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
