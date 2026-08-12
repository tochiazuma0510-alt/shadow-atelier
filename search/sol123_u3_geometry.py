"""Exact producer for Sol task 123 [U3-2] and quarantined [U3-3].

The smoothness calculation uses the complete-intersection Jacobian criterion
for E=G=0.  This is stricter and appropriate here; differentiating G alone
would test the ambient hypersurface G=0, not the curve cut out on E.
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
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def integer_content(expression: sp.Expr, variables: tuple[sp.Symbol, ...]) -> int:
    polynomial = sp.Poly(sp.expand(expression), *variables, domain=sp.ZZ)
    content = 0
    for coefficient in polynomial.coeffs():
        content = math.gcd(content, abs(int(coefficient)))
    return content


def prime_support(value: int) -> list[int]:
    value = abs(value)
    support: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            support.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if value > 1:
        support.append(value)
    return support


def main() -> None:
    spec_sha256 = sha256_file(SPEC)
    if spec_sha256 != EXPECTED_SPEC_SHA256:
        raise SystemExit("UNKNOWN: controlling specification SHA-256 mismatch")

    X, Y, w = sp.symbols("X Y w")
    E = Y**2 + 3 * X * Y + 2 * Y - X**3
    G = X**2 * w**3 - 27 * Y * (w + 1)

    # The three sections [0:1], [1:1], [1:0] have pairwise determinant a unit.
    sections = {"0": (0, 1), "1": (1, 1), "infinity": (1, 0)}
    pairs = [("0", "1"), ("0", "infinity"), ("1", "infinity")]
    determinants = {
        f"{left},{right}": sections[left][0] * sections[right][1]
        - sections[left][1] * sections[right][0]
        for left, right in pairs
    }
    noncollision = all(abs(value) == 1 for value in determinants.values())

    # Correct Jacobian criterion for the complete intersection E=G=0.
    variables = (X, Y, w)
    jacobian = sp.Matrix(
        [
            [sp.diff(E, variable) for variable in variables],
            [sp.diff(G, variable) for variable in variables],
        ]
    )
    minors = [
        sp.expand(jacobian[:, [0, 1]].det()),
        sp.expand(jacobian[:, [0, 2]].det()),
        sp.expand(jacobian[:, [1, 2]].det()),
    ]
    singular_groebner = sp.groebner(
        [E, G, *minors], X, Y, w, order="grevlex", domain=sp.QQ
    )
    singular_basis = [sp.sstr(sp.factor(poly.as_expr())) for poly in singular_groebner.polys]

    vertical_substitution = {X: 0, Y: 0}
    vertical_equations_zero = all(
        sp.expand(poly.subs(vertical_substitution)) == 0 for poly in [E, G, *minors]
    )
    jacobian_on_vertical = [
        [sp.sstr(sp.expand(entry.subs(vertical_substitution))) for entry in row]
        for row in jacobian.tolist()
    ]
    if not vertical_equations_zero:
        raise ArithmeticError("vertical singular-locus witness was not reproduced")

    # A smooth Z[1/S]-model has a smooth generic fibre.  The entire line
    # X=Y=0 is in the rank-drop locus over Q, so no finite localization of Z
    # can make this declared affine complete intersection smooth.
    generic_obstruction = True

    # Record the local saturation checkpoint used by R3; it is not promoted to
    # a global normalized model here.
    local_F = (
        X**2 * w**6
        + 81 * X * w**3 * (w + 1)
        + 54 * w**3 * (w + 1)
        - 729 * X * (w + 1) ** 2
    )
    local_derivative = sp.diff(local_F, X).subs({X: 0, w: 0})

    smooth_payload = {
        "schema": "u3_smooth/v1",
        "task": "Sol-123/U3-2",
        "artifact_date": "2026-08-13",
        "controlling_spec": {
            "path": "docs/notes/r2_r3_unram_execution_spec_v1.md",
            "sha256": spec_sha256,
        },
        "declared_affine_model": {
            "E": sp.sstr(E),
            "G": sp.sstr(G),
            "base_for_t": "Z[1/2]",
            "t": "-Y^2/4",
        },
        "D_noncollision": {
            "D": ["0", "1", "infinity"],
            "projective_sections": {key: list(value) for key, value in sections.items()},
            "pairwise_determinants": determinants,
            "all_determinants_are_units_over_Z": noncollision,
            "status": "COMPLETE",
        },
        "smoothness": {
            "criterion": "rank two of the 2x3 Jacobian for the complete intersection E=G=0",
            "jacobian_rows": [[sp.sstr(entry) for entry in row] for row in jacobian.tolist()],
            "two_by_two_minors": [sp.sstr(sp.factor(minor)) for minor in minors],
            "singular_ideal_groebner_basis_over_Q": singular_basis,
            "generic_rank_drop_witness": {
                "locus": "X=Y=0 with w arbitrary",
                "E_and_G_and_all_minors_vanish": vertical_equations_zero,
                "jacobian_on_locus": jacobian_on_vertical,
                "rank": 1,
                "persists_over_Q": True,
            },
            "raw_model_smooth_over_any_Z_localization": False,
            "reason_code": "GENERIC_VERTICAL_COMPONENT_AND_JACOBIAN_RANK_DROP",
        },
        "etale_outside_D": {
            "status": "UNKNOWN",
            "reason_code": "NORMALIZED_FINITE_MODEL_REQUIRED",
            "note": (
                "The declared complete intersection is not the normalized finite source; "
                "a relative-differential support claim for that source cannot be certified from it."
            ),
        },
        "normalization_checkpoint": {
            "local_branch_condition": "w+1 is a unit near (X,w)=(0,0)",
            "local_saturated_equation": sp.sstr(local_F),
            "dF_dX_at_origin": int(local_derivative),
            "global_normalized_projective_model_supplied": False,
        },
        "result": {
            "noncollision": "COMPLETE",
            "smoothness": "UNKNOWN_STOP",
            "etale_outside_D": "UNKNOWN_STOP",
            "required_input": "a global normalized finite model of W over the declared base",
        },
        "provenance": {
            "producer_script": "search/sol123_u3_geometry.py",
            "producer_script_sha256": sha256_file(Path(__file__)),
        },
        "status": "UNKNOWN_STOP_MODEL_NORMALIZATION_REQUIRED",
    }
    atomic_json(SMOOTH_CERT, smooth_payload)

    # U3-3: exact layerwise polynomial discriminants.  These values are kept
    # only in the quarantined certificate and are not printed by this script.
    polynomial_E_over_Y = X**3 - 3 * Y * X - (Y**2 + 2 * Y)
    polynomial_W_over_E = X**2 * w**3 - 27 * Y * w - 27 * Y
    disc_E_over_Y = sp.factor(sp.discriminant(polynomial_E_over_Y, X))
    disc_W_over_E = sp.factor(sp.discriminant(polynomial_W_over_E, w))
    content_E = integer_content(disc_E_over_Y, (Y,))
    content_W = integer_content(disc_W_over_E, (X, Y))
    layer_support = {
        "E_to_P1_Y": prime_support(content_E),
        "W_to_E": prime_support(content_W),
        "P1_s_to_P1_t": [2],
    }
    candidate_support = sorted(
        set(layer_support["E_to_P1_Y"])
        | set(layer_support["W_to_E"])
        | set(layer_support["P1_s_to_P1_t"])
    )
    delta_E = -216
    delta_support = prime_support(delta_E)
    if not set(delta_support).issubset(candidate_support):
        raise ArithmeticError("declared Delta(E) lower-bound support is not contained")

    disc_payload = {
        "schema": "u3_disc/v1",
        "task": "Sol-123/U3-3",
        "artifact_date": "2026-08-13",
        "controlling_spec": {
            "path": "docs/notes/r2_r3_unram_execution_spec_v1.md",
            "sha256": spec_sha256,
        },
        "computation": "exact SymPy polynomial discriminants over ZZ, layer by layer",
        "layers": {
            "E_to_P1_Y": {
                "polynomial_in_X": sp.sstr(polynomial_E_over_Y),
                "discriminant": sp.sstr(disc_E_over_Y),
                "content_ideal_generator_abs": content_E,
                "content_prime_support": layer_support["E_to_P1_Y"],
            },
            "W_to_E": {
                "polynomial_in_w": sp.sstr(polynomial_W_over_E),
                "discriminant": sp.sstr(disc_W_over_E),
                "content_ideal_generator_abs": content_W,
                "content_prime_support": layer_support["W_to_E"],
                "leading_coefficient_artifact_warning": True,
            },
            "P1_s_to_P1_t": {
                "map": "t=s^2",
                "content_prime_support": layer_support["P1_s_to_P1_t"],
            },
        },
        "candidate_S": {
            "construction": "union of layer content-prime supports and the quadratic-layer prime",
            "support": candidate_support,
            "delta_E_lower_bound": {
                "Delta_E": delta_E,
                "support": delta_support,
                "contained": True,
            },
        },
        "geometric_dependency": {
            "u3_smooth_cert": "search/certs/sol123_u3_smooth_v1_20260813.json",
            "u3_smooth_sha256": sha256_file(SMOOTH_CERT),
            "raw_model_is_normalized_finite_source": False,
            "upper_bound_interpretation_established": False,
            "unramified_arithmetic_conclusion_established": False,
            "unram_gap_4": "OPEN",
        },
        "special_quarantine": {
            "mode": "prereg-beta / ruling-1118",
            "certificate_may_be_committed": True,
            "reply_must_omit_S_value_and_support": True,
            "readout_and_interpretation_authorized": False,
            "a_class_artifact_read_by_this_producer": False,
            "simultaneous_disclosure": "pending_commander_gate",
        },
        "provenance": {
            "producer_script": "search/sol123_u3_geometry.py",
            "producer_script_sha256": sha256_file(Path(__file__)),
        },
        "status": "COMPUTED_QUARANTINED_INTERPRETATION_NOT_ASSERTED",
    }
    atomic_json(DISC_CERT, disc_payload)

    # Deliberately omit discriminant values and all S/support fields here.
    print(
        json.dumps(
            {
                "status": "U3_ARTIFACTS_WRITTEN",
                "certificates": [
                    {
                        "path": SMOOTH_CERT.relative_to(ROOT).as_posix(),
                        "sha256": sha256_file(SMOOTH_CERT),
                    },
                    {
                        "path": DISC_CERT.relative_to(ROOT).as_posix(),
                        "sha256": sha256_file(DISC_CERT),
                        "readout": "QUARANTINED",
                    },
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
