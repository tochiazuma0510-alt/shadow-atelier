"""Independent checker for Sol task 123 U3-2 and quarantined U3-3.

No producer code is imported.  The generic smoothness obstruction is checked
by direct substitution in the complete-intersection Jacobian.  Cubic
discriminants are evaluated with the coefficient formula rather than SymPy's
discriminant routine.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = ROOT / "search" / "certs"
SPEC = ROOT / "docs" / "notes" / "r2_r3_unram_execution_spec_v1.md"
SMOOTH_CERT = CERT_DIR / "sol123_u3_smooth_v1_20260813.json"
DISC_CERT = CERT_DIR / "sol123_u3_disc_v1_20260813.json"
CHECK_CERT = CERT_DIR / "sol123_u3_geometry_check_v1_20260813.json"
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


def cubic_discriminant(a: sp.Expr, b: sp.Expr, c: sp.Expr, d: sp.Expr) -> sp.Expr:
    return sp.expand(
        b**2 * c**2
        - 4 * a * c**3
        - 4 * b**3 * d
        - 27 * a**2 * d**2
        + 18 * a * b * c * d
    )


def coefficient_content(expression: sp.Expr, variables: tuple[sp.Symbol, ...]) -> int:
    coefficients = sp.Poly(sp.expand(expression), *variables, domain=sp.ZZ).coeffs()
    result = 0
    for coefficient in coefficients:
        result = math.gcd(result, abs(int(coefficient)))
    return result


def factor_support(value: int) -> list[int]:
    value = abs(value)
    result: list[int] = []
    candidate = 2
    while candidate * candidate <= value:
        if value % candidate == 0:
            result.append(candidate)
            while value % candidate == 0:
                value //= candidate
        candidate = 3 if candidate == 2 else candidate + 2
    if value > 1:
        result.append(value)
    return result


def main() -> None:
    if sha256_file(SPEC) != EXPECTED_SPEC_SHA256:
        raise SystemExit("UNKNOWN: controlling specification SHA-256 mismatch")

    smooth = json.loads(SMOOTH_CERT.read_text(encoding="utf-8"))
    disc = json.loads(DISC_CERT.read_text(encoding="utf-8"))

    X, Y, w = sp.symbols("X Y w")
    E = Y**2 + 3 * X * Y + 2 * Y - X**3
    G = X**2 * w**3 - 27 * Y * (w + 1)
    variables = (X, Y, w)
    rows = [[sp.diff(poly, variable) for variable in variables] for poly in (E, G)]
    minors = [
        sp.expand(rows[0][i] * rows[1][j] - rows[0][j] * rows[1][i])
        for i, j in ((0, 1), (0, 2), (1, 2))
    ]
    vertical = {X: 0, Y: 0}
    if E.subs(vertical) != 0 or G.subs(vertical) != 0:
        raise SystemExit("UNKNOWN: vertical component substitution failed")
    if any(minor.subs(vertical) != 0 for minor in minors):
        raise SystemExit("UNKNOWN: vertical Jacobian-rank witness failed")
    evaluated_rows = [[sp.expand(entry.subs(vertical)) for entry in row] for row in rows]
    if evaluated_rows != [[0, 2, 0], [0, -27 * w - 27, 0]]:
        raise SystemExit("UNKNOWN: Jacobian rows on the vertical component differ")

    # Pairwise determinants of [0:1], [1:1], [1:0].
    sections = [(0, 1), (1, 1), (1, 0)]
    determinants = [
        sections[i][0] * sections[j][1] - sections[i][1] * sections[j][0]
        for i, j in ((0, 1), (0, 2), (1, 2))
    ]
    if not all(abs(determinant) == 1 for determinant in determinants):
        raise SystemExit("UNKNOWN: D noncollision determinant check failed")

    # Independent coefficient-formula calculations for the two cubics.
    disc_E = sp.factor(cubic_discriminant(1, 0, -3 * Y, -(Y**2 + 2 * Y)))
    disc_W = sp.factor(cubic_discriminant(X**2, 0, -27 * Y, -27 * Y))
    content_E = coefficient_content(disc_E, (Y,))
    content_W = coefficient_content(disc_W, (X, Y))
    layer_support = {
        "E_to_P1_Y": factor_support(content_E),
        "W_to_E": factor_support(content_W),
        "P1_s_to_P1_t": [2],
    }
    candidate_support = sorted(
        set(layer_support["E_to_P1_Y"])
        | set(layer_support["W_to_E"])
        | set(layer_support["P1_s_to_P1_t"])
    )

    if smooth["status"] != "UNKNOWN_STOP_MODEL_NORMALIZATION_REQUIRED":
        raise SystemExit("UNKNOWN: producer did not fail closed on the generic obstruction")
    if not smooth["D_noncollision"]["all_determinants_are_units_over_Z"]:
        raise SystemExit("UNKNOWN: producer/checker D noncollision mismatch")
    if smooth["smoothness"]["raw_model_smooth_over_any_Z_localization"]:
        raise SystemExit("UNKNOWN: producer/checker raw smoothness mismatch")

    producer_layers = disc["layers"]
    if sp.expand(sp.sympify(producer_layers["E_to_P1_Y"]["discriminant"]) - disc_E) != 0:
        raise SystemExit("UNKNOWN: first layer discriminant mismatch")
    if sp.expand(sp.sympify(producer_layers["W_to_E"]["discriminant"]) - disc_W) != 0:
        raise SystemExit("UNKNOWN: second layer discriminant mismatch")
    if producer_layers["E_to_P1_Y"]["content_ideal_generator_abs"] != content_E:
        raise SystemExit("UNKNOWN: first content mismatch")
    if producer_layers["W_to_E"]["content_ideal_generator_abs"] != content_W:
        raise SystemExit("UNKNOWN: second content mismatch")
    if disc["candidate_S"]["support"] != candidate_support:
        raise SystemExit("UNKNOWN: candidate support mismatch")
    if disc["geometric_dependency"]["upper_bound_interpretation_established"]:
        raise SystemExit("UNKNOWN: upper-bound interpretation must remain unset")
    if disc["special_quarantine"]["readout_and_interpretation_authorized"]:
        raise SystemExit("UNKNOWN: quarantine authorization flag is open")

    payload = {
        "schema": "u3-geometry-check/v1",
        "task": "Sol-123/U3-2 and U3-3 independent checker",
        "artifact_date": "2026-08-13",
        "method_independence": {
            "producer_imported": False,
            "smoothness_obstruction": "direct complete-intersection Jacobian substitution",
            "discriminants": "generic cubic coefficient formula",
            "contents_and_supports": "local gcd and trial division",
        },
        "checks": {
            "D_noncollision": True,
            "generic_vertical_component": True,
            "generic_jacobian_rank_drop": True,
            "raw_model_localization_cannot_be_smooth": True,
            "layer_discriminants": True,
            "content_ideals": True,
            "candidate_support_internal_match": True,
            "special_quarantine_closed": True,
            "upper_bound_interpretation_not_asserted": True,
        },
        "inputs": {
            "u3_smooth_cert": {
                "path": "search/certs/sol123_u3_smooth_v1_20260813.json",
                "sha256": sha256_file(SMOOTH_CERT),
            },
            "u3_disc_cert": {
                "path": "search/certs/sol123_u3_disc_v1_20260813.json",
                "sha256": sha256_file(DISC_CERT),
                "readout": "QUARANTINED",
            },
        },
        "provenance": {
            "checker_script": "crosscheck/check_sol123_u3_geometry.py",
            "checker_script_sha256": sha256_file(Path(__file__)),
        },
        "status": "CROSS_CHECKED_WITH_U3_2_UNKNOWN_STOP",
    }
    atomic_json(CHECK_CERT, payload)
    # Deliberately omit all U3-3 values/supports from stdout.
    print(
        json.dumps(
            {
                "status": "CROSS_CHECKED_WITH_U3_2_UNKNOWN_STOP",
                "certificate": CHECK_CERT.relative_to(ROOT).as_posix(),
                "sha256": sha256_file(CHECK_CERT),
                "u3_disc_readout": "QUARANTINED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
