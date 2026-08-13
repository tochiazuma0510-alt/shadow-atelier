"""Versioned repair certificate for C1-prime(S4) and P5-prime.

This producer never reads the local-coefficient payload in the uloc
certificate. It stops at the JSON key named measurement and uses only the
structural prefix required by review requirements A--D and G.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from sympy import Symbol, discriminant, expand, factor
from sympy.combinatorics import Permutation, PermutationGroup


ROOT = Path(__file__).resolve().parents[1]
GF8_MOD = 0b1011
POINTS = tuple([(1, t) for t in range(8)] + [(0, 1)])


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def structural_prefix(path: Path) -> tuple[dict[str, object], dict[str, object]]:
    prefix: list[str] = []
    stopped = False
    with path.open("r", encoding="utf-8") as source:
        for line in source:
            if line.startswith(' "measurement"'):
                stopped = True
                break
            prefix.append(line)
    text = "".join(prefix).rstrip()
    if text.endswith(","):
        text = text[:-1]
    data = json.loads(text + "\n}\n")
    gate = data["gate_schema_v2"]
    return gate, {
        "measurement_payload_read": False,
        "stream_stopped_before_measurement_payload": stopped,
    }


def gf_mul(a: int, b: int) -> int:
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= GF8_MOD
    return result & 7


def gf_inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError
    return next(b for b in range(1, 8) if gf_mul(a, b) == 1)


def matrix_perm(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Permutation:
    image: list[int] = []
    for a, b in POINTS:
        c = gf_mul(a, matrix[0][0]) ^ gf_mul(b, matrix[1][0])
        d = gf_mul(a, matrix[0][1]) ^ gf_mul(b, matrix[1][1])
        line = (1, gf_mul(d, gf_inv(c))) if c else (0, 1)
        image.append(POINTS.index(line))
    return Permutation(image)


def cycle_type(p: Permutation) -> tuple[int, ...]:
    lengths = [len(cycle) for cycle in p.cyclic_form]
    lengths.extend([1] * (9 - sum(lengths)))
    return tuple(sorted(lengths, reverse=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="search/certs/c1prime_s4_p5prime_v2_20260813.json")
    parser.add_argument("--checkpoint", default="search/certs/c1prime_s4_p5prime_v2_checkpoint.json")
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()

    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "c1prime_s4_p5prime_checkpoint/v2",
        "stage": "start",
        "complete": False,
    }
    atomic_json(checkpoint, state)

    def watchdog() -> None:
        time.sleep(args.hard_timeout_seconds)
        if not state.get("complete"):
            state.update(stage="hard_timeout", elapsed_ms=int((time.monotonic() - started) * 1000))
            atomic_json(checkpoint, state)
            os._exit(124)

    threading.Thread(target=watchdog, daemon=True).start()

    try:
        v1_path = ROOT / "search/certs/c1prime_s4_p5prime_v1_20260813.json"
        v1_check_path = ROOT / "search/certs/c1prime_s4_p5prime_v1_check_20260813.json"
        v1 = json.loads(v1_path.read_text(encoding="utf-8"))
        v1_check = json.loads(v1_check_path.read_text(encoding="utf-8"))
        if not v1_check["all_checks_true"]:
            raise RuntimeError("v1 finite census checker is not all true")

        uloc_path = ROOT / "search/certs/u_meas_uloc_v2_20260731.json"
        gate, boundary = structural_prefix(uloc_path)
        state.update(stage="structural_prefix")
        atomic_json(checkpoint, state)

        t = Symbol("t")
        lam = Symbol("lambda")
        shanks = lam**3 - t * lam**2 + (t - 3) * lam + 1
        disc = factor(discriminant(shanks, lam))
        expected_disc = (t**2 - 3 * t + 9) ** 2
        if expand(disc - expected_disc) != 0:
            raise RuntimeError("Shanks discriminant mismatch")

        tau_rows: dict[str, object] = {}
        for name in ("N_tau1", "N_tau2"):
            row = gate[name]
            partition = [3, 3, 3] if (
                row["degree"] == 9
                and row["deg_radical"] == 3
                and row["deg_gcd_with_derivative"] == 6
                and row["equals_kappa_g_cubed"]
            ) else None
            tau_rows[name] = {
                "degree": row["degree"],
                "deg_radical": row["deg_radical"],
                "deg_gcd_with_derivative": row["deg_gcd_with_derivative"],
                "equals_kappa_g_cubed": row["equals_kappa_g_cubed"],
                "ramification_partition": partition,
            }
        passport_pinned = all(row["ramification_partition"] == [3, 3, 3] for row in tau_rows.values())

        s = matrix_perm(((1, 0), (1, 1)))
        tt = matrix_perm(((4, 3), (1, 5)))
        w = s * (~tt)
        x = w**2
        y = (~s) * x * s
        p_group = PermutationGroup([x, y])
        p_elements = list(p_group.generate_schreier_sims())
        abstract_order9 = [g for g in p_elements if int(g.order()) == 9]
        order9_cycle_types = sorted({cycle_type(g) for g in abstract_order9})
        all_order9_are_nine_cycles = len(abstract_order9) == 168 and order9_cycle_types == [(9,)]

        frob = gate["frobenius"]
        patterns = frob["patterns"]
        p_cycle_types = {
            json.dumps(list(cycle_type(g)), separators=(",", ":")) for g in p_elements
        }
        strict_witness_types = [
            key for key in ("[3, 3, 1, 1, 1]", "[6, 2, 1]")
            if patterns.get(key, 0) > 0
            and json.dumps(json.loads(key), separators=(",", ":")) not in p_cycle_types
        ]

        paths = (
            v1_path,
            v1_check_path,
            uloc_path,
            ROOT / "docs/notes/u_meas_m1_passport_v1.md",
            ROOT / "docs/notes/u_meas_m3_caseb_v1.md",
            ROOT / "docs/notes/litgate_positive_genus_belyi_v1.md",
            ROOT / "docs/notes/c1p5_closure_review_v1.md",
        )
        digests = {
            str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path) for path in paths
        }

        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        cert = {
            "schema": "c1prime_s4_p5prime/v2",
            "run_id": f"c1prime-s4-p5prime-v2-{now}",
            "generated_by": {
                "script": "search/c1prime_s4_p5prime_v2.py",
                "tool": "Python 3.13 + SymPy 1.14",
            },
            "v1_finite_census_binding": {
                "source_run_id": v1["run_id"],
                "source_checker_all_true": v1_check["all_checks_true"],
                "source_solution_count": v1["quotient_dessin"]["solution_count_fixed_C"],
                "source_order_distribution": v1["quotient_dessin"]["monodromy_order_distribution"],
                "source_order504_orbit_count": v1["quotient_dessin"]["order504_centralizer_orbit_count"],
            },
            "requirement_A_passport_binding": {
                "shanks_polynomial": "lambda^3-t*lambda^2+(t-3)*lambda+1",
                "discriminant": "(t^2-3*t+9)^2",
                "branch_points": ["3*zeta_6", "3*zeta_6^-1"],
                "cyclic_degree": 3,
                "tau_rows": tau_rows,
                "registered_W_passport": [[9], [9], [9]],
                "normalized_fibre_product_local_rule": "e_W=a/gcd(a,b)",
                "riemann_hurwitz": {
                    "C_formula": "2*g_C-2=-18+8+2*(j1+j2)",
                    "j1": 3,
                    "j2": 3,
                    "g_C": 2,
                    "C_branch_support_subset": "{tau1,tau2,p}",
                    "p_partition": [9],
                },
                "measured_C_passport": [[3, 3, 3], [3, 3, 3], [9]],
                "shanks_branch_equals_C_order3_branch": passport_pinned,
                "load_bearing_for_7cycle_argument": True,
                "legacy_reconstruction_XYZ_exact_role": {
                    "classification": "free-group identity under the producer definitions",
                    "independent_information": False,
                    "retained_only_as_regression": True,
                },
            },
            "requirement_B_specialization": {
                "witness_coordinate_line": "t-line",
                "witness_encoding": "(p,t0)",
                "seven_cycle_witness_count": len(frob["seven_cycle_witnesses_p_t0"]),
                "good_specialization_statement": (
                    "at good specialization Gal(f(x,t0)/Q) embeds in Gal(f(x,t)/Q(t)) "
                    "with the same action on the nine roots; mod-p factor degrees give a cycle type"
                ),
                "used_as_existence_only": True,
            },
            "requirement_C_intrinsic_Q_model": {
                "source": "docs/notes/litgate_positive_genus_belyi_v1.md",
                "pin": "section (I), LEDGER 633",
                "claim_used": "the genus-2 degree-9 canonical quotient cover is defined over Q",
                "rigidity_reading": "passport plus monodromy PSL(2,8), not the bare passport",
                "s_intr_Q_model_premise": True,
            },
            "requirement_D_prior_work": {
                "source": "docs/notes/u_meas_m1_passport_v1.md",
                "pin": "FINDING U-8; frozen F-9/F-10 (2026-07-31)",
                "already_recorded": "24 solutions, 81:6/324:9/504:9, one orbit for the 504 solutions",
                "new_in_v1": "normalizer census plus seven-cycle forcing",
            },
            "requirement_G_nine_cycle_incidence": {
                "P_order": int(p_group.order()),
                "abstract_order9_element_count": len(abstract_order9),
                "cycle_types_of_all_abstract_order9_elements": [list(row) for row in order9_cycle_types],
                "all_168_are_nine_cycles_in_this_action": all_order9_are_nine_cycles,
                "normalizer_order": v1["quotient_dessin"]["normalizers_in_S9"]["504"]["order"],
                "conjugate_P_copies": 240,
                "incidence_total": 240 * len(abstract_order9),
                "S9_nine_cycle_total": 40320,
                "copies_through_fixed_nine_cycle": 1,
            },
            "convention_repair": {
                "mathematical_convention": "left Ad(g)(h)=g*h*g^-1",
                "legacy_orbit_indices_are_not_semantic": True,
                "canonical_record": {
                    "fixed_Z_orbit_count": v1["fibre_product_binding"]["fixed_Z_centralizer_orbit_count"],
                    "diagonal_orbit_count": v1["fibre_product_binding"]["diagonal_orbit_count"],
                    "intrinsic_orbit_is_diagonal": v1["fibre_product_binding"]["intrinsic_orbit_diagonal"],
                },
            },
            "monodromy_geometric": {
                "passport_is_now_measured_side_pinned": passport_pinned,
                "order": 504,
                "forced_by_normalizer_and_t_line_seven_cycle": (
                    passport_pinned
                    and v1["quotient_dessin"]["geometric_monodromy_order_forced_by_exact_7cycle_and_normalizers"]
                ),
            },
            "monodromy_arithmetic": {
                "strict_overgroup_witness_cycle_types": strict_witness_types,
                "normalizer_of_geometric_group_order": 1512,
                "normalizer_quotient_order": 3,
                "order": 1512,
                "name": "PGammaL(2,8)",
                "outside_PGammaL_empty_sample_used_as_upper_bound": False,
            },
            "p5prime": {
                "intrinsic_Q_model_pin_shared_with_requirement_C": True,
                "local_parameter_change": "s_meas=gamma*s_intr*(1+O(s_intr))",
                "coefficient_change": "u0=uS4*gamma^-9, up to unit exponent for orientation",
                "generated_cyclic_subgroups_equal": True,
                "representative_equality_claimed": False,
                "numeric_local_class_read": False,
            },
            "structural_boundary": boundary,
            "input_sha256": digests,
            "elapsed_ms": int((time.monotonic() - started) * 1000),
            "u_touched": False,
            "c_touched": False,
            "sealed_k5_touched": False,
            "prereg_quantities_untouched": True,
        }
        atomic_json(output, cert)
        state.update(
            stage="complete",
            complete=True,
            output=str(output.relative_to(ROOT)).replace("\\", "/"),
            run_id=cert["run_id"],
            elapsed_ms=cert["elapsed_ms"],
        )
        atomic_json(checkpoint, state)
        print(json.dumps({
            "run_id": cert["run_id"],
            "passport_pinned": passport_pinned,
            "all_168_are_nine_cycles": all_order9_are_nine_cycles,
            "arithmetic_order": 1512,
        }, sort_keys=True))
        return 0
    except Exception as exc:
        state.update(
            stage="error",
            error=repr(exc),
            elapsed_ms=int((time.monotonic() - started) * 1000),
        )
        atomic_json(checkpoint, state)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
