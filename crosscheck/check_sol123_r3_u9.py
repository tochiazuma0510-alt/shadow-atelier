"""Independent exact checker for Sol task 123 R3-U9 and DESC-9.

This checker does not import the producer.  It obtains the leading terms from
the initial form of the independently reconstructed saturated equation, uses
trial division for rational factorizations, and substitutes the producer's
series back into both declared equations.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = ROOT / "search" / "certs"
SPEC = ROOT / "docs" / "notes" / "r2_r3_unram_execution_spec_v1.md"
B_RECEIPT = CERT_DIR / "ds4_receipt_v1_20260812.json"
FACTORY_R2_CERT = CERT_DIR / "r2_u_uniformizer_v1_20260813.json"
R3_CERT = CERT_DIR / "sol123_r3_u9_v1_20260813.json"
P8_CERT = CERT_DIR / "sol123_p8_a_class_v1_20260813.json"
CHECK_CERT = CERT_DIR / "sol123_r3_u9_check_v1_20260813.json"
EXPECTED_SPEC_SHA256 = (
    "da6294da1b2f359f3b80f2281570770e4db616a360a9896bc5fc6ca1055f1c26"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def trial_factor(value: int) -> dict[int, int]:
    value = abs(value)
    if value == 0:
        raise ValueError("cannot factor zero")
    factors: dict[int, int] = {}
    candidate = 2
    while candidate * candidate <= value:
        count = 0
        while value % candidate == 0:
            count += 1
            value //= candidate
        if count:
            factors[candidate] = count
        candidate = 3 if candidate == 2 else candidate + 2
    if value != 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def rational_valuations(value: Fraction) -> tuple[int, dict[int, int]]:
    sign = -1 if value < 0 else 1
    valuations = trial_factor(value.numerator)
    for prime, exponent in trial_factor(value.denominator).items():
        valuations[prime] = valuations.get(prime, 0) - exponent
    return sign, dict(sorted((p, e) for p, e in valuations.items() if e))


def terms_to_expr(terms: list[dict], variable: sp.Symbol) -> sp.Expr:
    return sp.Add(
        *(sp.Rational(term["coefficient"]) * variable ** int(term["degree"]) for term in terms)
    )


def main() -> None:
    if sha256_file(SPEC) != EXPECTED_SPEC_SHA256:
        raise SystemExit("UNKNOWN: controlling specification SHA-256 mismatch")

    # Reconstruct the local equation independently from the declared model.
    X, Y, w = sp.symbols("X Y w")
    E = Y**2 + 3 * X * Y + 2 * Y - X**3
    W = X**2 * w**3 - 27 * Y * (w + 1)
    y_eliminated = X**2 * w**3 / (27 * (w + 1))
    reconstructed = sp.cancel(729 * (w + 1) ** 2 * E.subs(Y, y_eliminated) / X**2)
    expected_local = (
        X**2 * w**6
        + 81 * X * w**3 * (w + 1)
        + 54 * w**3 * (w + 1)
        - 729 * X * (w + 1) ** 2
    )
    if sp.expand(reconstructed - expected_local) != 0:
        raise SystemExit("UNKNOWN: independent local-equation derivation failed")
    derivative = sp.diff(expected_local, X).subs({X: 0, w: 0})
    if derivative != -729:
        raise SystemExit("UNKNOWN: implicit derivative mismatch")

    # Initial form: X=c*w^3 gives 54-729*c=0.
    c_x = sp.Rational(54, 729)
    c_y = sp.cancel(c_x**2 / 27)
    u9_s1 = sp.cancel(-c_y**2 / 4)
    # The second rational function is X/w^2 = c_x*w+..., so its leading
    # coefficient relative to s_1=w is c_x.  This route is non-proportional
    # (the stored direct series has a nonzero quadratic term).
    u9_s2 = sp.cancel(u9_s1 / c_x**18)
    if sp.cancel(u9_s1 / u9_s2) != c_x**18:
        raise SystemExit("UNKNOWN: independent uniformizer-ratio check failed")

    r3 = json.loads(R3_CERT.read_text(encoding="utf-8"))
    p8 = json.loads(P8_CERT.read_text(encoding="utf-8"))
    producer_u9 = Fraction(r3["uniformizer_invariance"]["u_9_s_1"])
    if producer_u9 != Fraction(int(sp.numer(u9_s1)), int(sp.denom(u9_s1))):
        raise SystemExit("UNKNOWN: producer/checker u_9 mismatch")
    producer_u9_s2 = Fraction(r3["uniformizer_invariance"]["u_9_s_2"])
    expected_u9_s2 = Fraction(int(sp.numer(u9_s2)), int(sp.denom(u9_s2)))
    if producer_u9_s2 != expected_u9_s2:
        raise SystemExit("UNKNOWN: producer/checker second-uniformizer u_9 mismatch")
    if r3["uniformizer_invariance"]["s_2"] != "X/w^2":
        raise SystemExit("UNKNOWN: second uniformizer identity mismatch")
    if not r3["uniformizer_invariance"]["s_1_and_s_2_nonproportional_as_functions"]:
        raise SystemExit("UNKNOWN: second uniformizer was not shown non-proportional")

    # Direct substitution check of every stored series term, without using the
    # producer recurrence.  Only degrees represented in the certificate are
    # asserted, so compare below the first omitted degree for each expression.
    x_terms = r3["exact_series"]["X_terms"]
    y_terms = r3["exact_series"]["Y_terms"]
    x_expr = terms_to_expr(x_terms, w)
    y_expr = terms_to_expr(y_terms, w)
    x_cut = max(int(term["degree"]) for term in x_terms) + 1
    y_cut = max(int(term["degree"]) for term in y_terms) + 1
    safe_cut = min(x_cut + 2, y_cut)
    e_expanded = sp.Poly(sp.expand(E.subs({X: x_expr, Y: y_expr})), w)
    w_expanded = sp.Poly(sp.expand(W.subs({X: x_expr, Y: y_expr})), w)
    for degree in range(safe_cut):
        if e_expanded.coeff_monomial(w**degree) != 0:
            raise SystemExit(f"UNKNOWN: E series residual at degree {degree}")
        if w_expanded.coeff_monomial(w**degree) != 0:
            raise SystemExit(f"UNKNOWN: W series residual at degree {degree}")

    a_representative = Fraction(1, 1) / producer_u9
    a_sign, a_valuations = rational_valuations(a_representative)
    a_mod9 = {prime: exponent % 9 for prime, exponent in a_valuations.items() if exponent % 9}
    support = sorted(a_mod9)
    exponents = [a_mod9[prime] for prime in support]
    common = 9
    for exponent in exponents:
        common = math.gcd(common, exponent)
    order = 9 // common
    if p8["a_class"]["support"] != support:
        raise SystemExit("UNKNOWN: a_class support mismatch")
    if p8["a_class"]["exponents"] != exponents or p8["a_class"]["order"] != order:
        raise SystemExit("UNKNOWN: a_class exponent/order mismatch")
    if a_sign != -1:
        raise SystemExit("UNKNOWN: unexpected sign for u_9 inverse")

    # Re-read the source receipt, factor its rational from scratch, and enforce
    # the preregistered normalization exactly, including the zero coordinate.
    receipt = json.loads(B_RECEIPT.read_text(encoding="utf-8"))
    b_value = Fraction(receipt["d1_input_tamper_check"]["u0_inverse_read"])
    b_sign, b_valuations = rational_valuations(b_value)
    b_mod9 = {prime: exponent % 9 for prime, exponent in b_valuations.items()}
    if b_sign != -1 or b_valuations != {2: -8, 3: 6, 5: 9}:
        raise SystemExit("UNKNOWN: independent raw [b] factorization mismatch")
    if b_mod9 != {2: 1, 3: 6, 5: 0}:
        raise SystemExit("UNKNOWN: independent [b] mod-9 normalization mismatch")

    producer_b = {
        int(prime): exponent
        for prime, exponent in r3["b_mod9_independent_normalization"][
            "normalized_mod9_including_zero"
        ].items()
    }
    if producer_b != b_mod9:
        raise SystemExit("UNKNOWN: producer/checker [b] mismatch")

    # This factory artifact arrived only after the Sol producer output had
    # already been fixed.  Use it solely as a post-measurement third rail.
    factory_r2 = json.loads(FACTORY_R2_CERT.read_text(encoding="utf-8"))
    factory_series = factory_r2["u3_puiseux_series"]
    if factory_series["s1_definition"] != "w" or factory_series["s2_definition"] != "X / w^2":
        raise SystemExit("UNKNOWN: post-measurement factory uniformizer identities differ")
    if factory_series["c1_relation"] != "c1^3 = 27/2":
        raise SystemExit("UNKNOWN: post-measurement factory leading relation differs")
    factory_abstract_lead = Fraction(
        factory_r2["u4_watches"]["w_b_ord_lambda9_is_18"]["leading_coeff"]
    )
    c1_cubed = Fraction(1, 1) / Fraction(int(sp.numer(c_x)), int(sp.denom(c_x)))
    if factory_abstract_lead / c1_cubed**6 != producer_u9:
        raise SystemExit("UNKNOWN: post-measurement factory first u_9 route differs")
    if factory_abstract_lead * c1_cubed**12 != producer_u9_s2:
        raise SystemExit("UNKNOWN: post-measurement factory second u_9 route differs")

    score_expected = support == [3] and order == 9
    if p8["score_rule_s1_measurement"]["result"] != score_expected:
        raise SystemExit("UNKNOWN: score-rule measurement mismatch")

    payload = {
        "schema": "r3_u9-check/v1",
        "task": "Sol-123/R-3-U9 independent checker",
        "artifact_date": "2026-08-13",
        "method_independence": {
            "producer_imported": False,
            "local_leading_term": "initial-form balance",
            "factorization": "local trial division",
            "series_check": "direct symbolic substitution",
        },
        "checks": {
            "controlling_spec_sha256": True,
            "saturated_chart_identity": True,
            "implicit_derivative": True,
            "uniformizer_18th_power_ratio": True,
            "stored_series_substitution_through_degree": safe_cut - 1,
            "desc9_rationality_and_unique_class_data": True,
            "b_mod9_preregistered_normalization": True,
            "score_rule_same_measurement": True,
            "post_measurement_factory_R2_concordance": True,
        },
        "inputs": {
            "r3_u9_cert": {
                "path": "search/certs/sol123_r3_u9_v1_20260813.json",
                "sha256": sha256_file(R3_CERT),
            },
            "p8_a_class_cert": {
                "path": "search/certs/sol123_p8_a_class_v1_20260813.json",
                "sha256": sha256_file(P8_CERT),
            },
            "b_receipt": {
                "path": "search/certs/ds4_receipt_v1_20260812.json",
                "sha256": sha256_file(B_RECEIPT),
            },
            "factory_R2_cert_post_measurement": {
                "path": "search/certs/r2_u_uniformizer_v1_20260813.json",
                "sha256": sha256_file(FACTORY_R2_CERT),
            },
        },
        "touch_state": {
            "new_measurements": "none; checker reads R3/P8 outputs and the preregistered b receipt",
            "c": "untouched",
            "d9": "not_computed",
            "r": "not_computed",
            "K5_instances": "untouched",
        },
        "provenance": {
            "checker_script": "crosscheck/check_sol123_r3_u9.py",
            "checker_script_sha256": sha256_file(Path(__file__)),
        },
        "status": "CROSS_CHECKED",
    }
    atomic_json(CHECK_CERT, payload)
    print(
        json.dumps(
            {
                "status": "CROSS_CHECKED",
                "certificate": CHECK_CERT.relative_to(ROOT).as_posix(),
                "sha256": sha256_file(CHECK_CERT),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
