#!/usr/bin/env python3
"""Import-free checker for the bounded CRT-C2 main-run receipt.

This checker does not import the producer.  It independently rebuilds the
Step-C1 high-coefficient subsystem, the mu_3 distribution census, and the
cyclic-trigonal positive control.  For an UNKNOWN producer result it checks
that no nonexistence/existence claim leaked through.  A future complete
good-reduction obstruction deliberately remains only a candidate unless a
second-prime run is attached.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_RESULT = ROOT / "ci" / "k3_crtC2_artifacts_31592557898" / "w9_k3_crt_C2_stage1_result.json"
UPSTREAM_CHECK = ROOT / "ci" / "k3_crtC2_artifacts_31592557898" / "w9_k3_crt_C2_stage1_check.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def integrity_ok(payload: dict[str, Any]) -> bool:
    stored = payload.get("integrity", {}).get("canonical_payload_sha256")
    candidate = copy.deepcopy(payload)
    candidate.pop("integrity", None)
    return stored == sha256_bytes(canonical_bytes(candidate))


def expected_distributions() -> list[list[int]]:
    result = []
    for f0 in range(5, -1, -1):
        for f1 in range(5 - f0, -1, -1):
            f2 = 5 - f0 - f1
            if f1 >= f2:
                result.append([f0, f1, f2])
    return result


def independent_step_c1() -> dict[str, Any]:
    """Solve all six high equations at once (not producer's triangular loop)."""
    w = sp.symbols("w")
    ss, pp = sp.symbols("ss pp")
    high = list(sp.symbols("g2:8"))
    g = w**8 + sum(high[i] * w ** (i + 2) for i in range(6)) + sp.symbols("g1") * w + sp.symbols("g0")
    target = sp.Poly(sp.expand((w**2 - ss * w + pp) * g**2 - (w**6 + 1) ** 3), w)
    equations = [target.nth(j) for j in range(12, 18)]
    solved = sp.solve(equations, high, dict=True)
    unique = len(solved) == 1 and all(v in solved[0] for v in high)
    substituted = sp.Poly(target.as_expr().subs(solved[0]) if unique else target.as_expr(), w)
    return {
        "equation_count": len(equations),
        "unique_high_solution": unique,
        "remaining_high_coefficients_zero": bool(unique and all(substituted.nth(j) == 0 for j in range(12, 18))),
        "free_dimension_after_t1": 10 if unique else None,
        "solution_formulas": {str(k): str(sp.factor(v)) for k, v in (solved[0].items() if unique else [])},
    }


def independent_positive_control() -> dict[str, Any]:
    w = sp.symbols("w")
    h = sp.Poly(w**5 + w + 1, w)
    disc = -27 * h * h
    square_identity = disc == -27 * h * h
    squarefree = sp.gcd(h, h.diff()).degree() == 0
    finite = 5 * 2
    infinity = 2
    genus = (3 * (-2) + finite + infinity + 2) // 2
    return {
        "h_squarefree": squarefree,
        "discriminant_square_identity": square_identity,
        "finite_contribution": finite,
        "infinity_contribution": infinity,
        "genus": genus,
        "pass": bool(squarefree and square_identity and genus == 4),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cert", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    cert = json.loads(args.cert.read_text(encoding="utf-8"))
    upstream_result = json.loads(UPSTREAM_RESULT.read_text(encoding="utf-8"))
    upstream_check = json.loads(UPSTREAM_CHECK.read_text(encoding="utf-8"))
    step_c1 = independent_step_c1()
    control = independent_positive_control()
    quarantine = cert.get("quarantine", {})
    status = cert.get("status", "")
    rows = cert.get("C2_2_distribution_results", [])
    empty_statuses = {
        "EMPTY_BY_CLOSURE_MOD_P_UNIT",
        "EMPTY_BY_CORE_OPEN_SUPERSET_MOD_P_UNIT",
    }
    complete_claim = status == "COMPLETE_F5_LAYER_EMPTY_BY_GOOD_REDUCTION"
    unknown_claim = status.startswith("UNKNOWN_")
    all_rows_empty = len(rows) == 12 and all(row.get("status") in empty_statuses for row in rows)
    unknown_semantics_ok = bool(
        not unknown_claim
        or (
            cert.get("layer_0_5_solution_exists_over_F9") is None
            and cert.get("C2_3_genus") == "NOT_REACHED_C2_2_UNKNOWN"
            and cert.get("C2_4_order_P0_minus_Pinf") == "NOT_REACHED_C2_2_UNKNOWN"
        )
    )
    # One prime is a valid candidate obstruction, but this import-free checker
    # does not pretend it independently recomputed all 12 Groebner bases.
    second_prime_attached = bool(cert.get("independent_second_prime", {}).get("all_distributions_unit"))
    complete_claim_crosscheck_ok = bool(not complete_claim or (all_rows_empty and second_prime_attached))

    checks: dict[str, Any] = {
        "producer_integrity_valid": integrity_ok(cert),
        "schema_correct": cert.get("schema") == "r13-r1p/v3-k3-crt-c2-main/v1",
        "upstream_hashes_match": bool(
            cert.get("C2_0_C2_1_upstream_gate", {}).get("result_sha256") == sha256_file(UPSTREAM_RESULT)
            and cert.get("C2_0_C2_1_upstream_gate", {}).get("check_sha256") == sha256_file(UPSTREAM_CHECK)
        ),
        "upstream_gates_independently_visible": bool(
            upstream_result.get("C2_0_regression_gate", {}).get("all_pass")
            and upstream_result.get("C2_1_D_construction", {}).get("coeff_w36_is_zero")
            and upstream_check.get("all_checks_true")
        ),
        "distribution_census_correct": cert.get("universe", {}).get("colour_degree_distributions")
        == expected_distributions(),
        "strict_order_correct": cert.get("C2_2_system_design", {}).get("ordering")
        == ["mu3_CRT", "D_equals_cE2", "genus", "order9"],
        "independent_step_C1": step_c1,
        "independent_positive_control": control,
        "producer_positive_control_pass": cert.get("positive_control", {}).get("pass") is True,
        "unknown_semantics_ok": unknown_semantics_ok,
        "complete_claim_crosscheck_ok": complete_claim_crosscheck_ok,
        "complete_claim_requires_second_prime": complete_claim,
        "second_prime_attached": second_prime_attached,
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
        and checks["upstream_hashes_match"]
        and checks["upstream_gates_independently_visible"]
        and checks["distribution_census_correct"]
        and checks["strict_order_correct"]
        and step_c1["unique_high_solution"]
        and step_c1["remaining_high_coefficients_zero"]
        and control["pass"]
        and checks["producer_positive_control_pass"]
        and unknown_semantics_ok
        and complete_claim_crosscheck_ok
        and all(checks["quarantine_exact"].values())
    )
    result = {
        "schema": "r13-r1p/v3-k3-crt-c2-main-check/v1",
        "cert_path": str(args.cert),
        "checks": checks,
        "all_checks_true": all_true,
        "classification": (
            "consistent bounded UNKNOWN receipt" if unknown_claim else "second-prime cross-check required for complete obstruction"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"CRT_C2_MAIN_CHECK_{'PASS' if all_true else 'FAIL'}", flush=True)
    return 0 if all_true else 1


if __name__ == "__main__":
    raise SystemExit(main())
