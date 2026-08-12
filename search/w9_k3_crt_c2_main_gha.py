#!/usr/bin/env python3
"""Bounded exact main computation for the k=3 CRT-C2 lane, steps C2-2--C2-4.

The ordering is deliberately fail-closed:

1. attest the already-completed C2-0/C2-1 gates;
2. impose the degree-five mu_3 CRT colour stratum;
3. only then impose D=c*E(w)^2 (deg E=17);
4. inspect genus/order watches only if a characteristic-zero candidate exists.

The production ideals are reduced modulo a good prime and handed to Singular.
If Singular returns the unit ideal, that special-fibre obstruction is also an
exact characteristic-zero obstruction.  NONUNIT or timeout is reported as
UNKNOWN; it is never promoted to a solution or nonexistence claim.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import time
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_RESULT = ROOT / "ci" / "k3_crtC2_artifacts_31592557898" / "w9_k3_crt_C2_stage1_result.json"
UPSTREAM_CHECK = ROOT / "ci" / "k3_crtC2_artifacts_31592557898" / "w9_k3_crt_C2_stage1_check.json"
DEFAULT_OUTPUT = ROOT / "ci" / "out" / "w9_k3_crt_c2_main_result.json"
DEFAULT_CHECKPOINT = ROOT / "ci" / "out" / "w9_k3_crt_c2_main_checkpoint.json"
DEFAULT_WORK = ROOT / "ci" / "out" / "w9_k3_crt_c2_work"


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


def singular_expr(expr: sp.Expr) -> str:
    return sp.sstr(expr).replace("**", "^")


def coefficient_equations(poly: sp.Poly, low: int, high: int) -> list[sp.Expr]:
    return [poly.nth(j) for j in range(low, high + 1)]


def square_equations(discriminant: sp.Poly, root: sp.Poly, scalar: sp.Symbol, max_degree: int) -> list[sp.Expr]:
    """The exact D-cE^2 path shared by production and the planted control."""
    residual = discriminant - scalar * root * root
    return coefficient_equations(residual, 0, max_degree)


def mu3_distributions() -> list[tuple[int, int, int]]:
    rows = []
    for f_one in range(5, -1, -1):
        for f_omega in range(5 - f_one, -1, -1):
            f_omega2 = 5 - f_one - f_omega
            if f_omega >= f_omega2:
                rows.append((f_one, f_omega, f_omega2))
    return rows


def build_common_system() -> dict[str, Any]:
    """Eliminate the six high g coefficients and build D=cE^2 exactly over Q."""
    w = sp.symbols("w")
    ss, pp = sp.symbols("ss pp")
    g0, g1 = sp.symbols("g0 g1")
    g_symbols = list(sp.symbols("g0:8"))
    p_symbols = list(sp.symbols("p0:6"))
    e_symbols = list(sp.symbols("e0:17"))
    scalar = sp.symbols("sqc")

    g_raw = sp.Poly(w**8 + sum(g_symbols[i] * w**i for i in range(8)), w)
    target_raw = sp.Poly(w**2 - ss * w + pp, w) * g_raw * g_raw
    boundary = sp.Poly((w**6 + 1) ** 3, w)
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    solve_rows = []
    for degree, variable in zip(range(17, 11, -1), reversed(g_symbols[2:8])):
        equation = sp.expand(target_raw.nth(degree).subs(substitutions) - boundary.nth(degree))
        solutions = sp.solve(equation, variable)
        if len(solutions) != 1:
            raise RuntimeError(f"C2-2 high-coefficient elimination failed at w^{degree}")
        substitutions[variable] = sp.factor(solutions[0])
        solve_rows.append({"degree": degree, "variable": str(variable), "formula": str(substitutions[variable])})

    g = sp.Poly(g_raw.as_expr().subs(substitutions), w)
    target = sp.Poly(w**2 - ss * w + pp, w) * g * g
    p2 = sp.Poly(sum(p_symbols[i] * w**i for i in range(6)), w)
    p1 = target - boundary - p2
    if p1.degree() > 11:
        raise RuntimeError(f"C2-2 internal error: P1 degree {p1.degree()} > 11")

    cubic_b = sp.Poly(3 * w**6, w) + p2
    cubic_c = sp.Poly(3 * w**12, w) + p1
    cubic_d = sp.Poly(w**18, w)
    discriminant = (
        cubic_b * cubic_b * cubic_c * cubic_c
        - 4 * cubic_c * cubic_c * cubic_c
        - 4 * cubic_b * cubic_b * cubic_b * cubic_d
        - 27 * cubic_d * cubic_d
        + 18 * cubic_b * cubic_c * cubic_d
    )
    if discriminant.degree() != 34:
        raise RuntimeError(f"C2-2 internal error: symbolic D degree {discriminant.degree()} != 34")
    root = sp.Poly(w**17 + sum(e_symbols[i] * w**i for i in range(17)), w)
    square_eqs = square_equations(discriminant, root, scalar, 34)

    return {
        "w": w,
        "ss": ss,
        "pp": pp,
        "g0": g0,
        "g1": g1,
        "p_symbols": p_symbols,
        "e_symbols": e_symbols,
        "scalar": scalar,
        "g": g,
        "target": target,
        "boundary": boundary,
        "p1": p1,
        "p2": p2,
        "discriminant": discriminant,
        "square_eqs": square_eqs,
        "square_eq_strings": [singular_expr(eq) for eq in square_eqs],
        "solve_rows": solve_rows,
    }


def colour_factors(
    distribution: tuple[int, int, int], w: sp.Symbol, m_symbols: list[sp.Symbol]
) -> list[sp.Poly]:
    factors: list[sp.Poly] = []
    offset = 0
    for degree in distribution:
        if degree == 0:
            factors.append(sp.Poly(1, w))
            continue
        coeffs = m_symbols[offset : offset + degree]
        offset += degree
        factors.append(sp.Poly(w**degree + sum(coeffs[j] * w**j for j in range(degree)), w))
    if offset != 5:
        raise RuntimeError("colour-factor coefficient allocation did not use five variables")
    return factors


def crt_equations(common: dict[str, Any], distribution: tuple[int, int, int], omega_mod_p: int) -> dict[str, Any]:
    w: sp.Symbol = common["w"]
    m_symbols = list(sp.symbols("m0:5"))
    factors = colour_factors(distribution, w, m_symbols)
    zetas = [1, omega_mod_p, (omega_mod_p * omega_mod_p)]
    equations: list[sp.Expr] = []
    rows = []
    for colour, (degree, zeta, factor) in enumerate(zip(distribution, zetas, factors)):
        if degree == 0:
            rows.append({"colour": colour, "degree": 0, "equation_count": 0})
            continue
        residue_p2 = sp.Poly(-3 * (1 - zeta) * w**6, w)
        residue_p1 = sp.Poly(-3 * (1 - zeta * zeta) * w**12, w)
        rem_p2 = (common["p2"] - residue_p2).rem(factor)
        rem_p1 = (common["p1"] - residue_p1).rem(factor)
        local = coefficient_equations(rem_p2, 0, degree - 1) + coefficient_equations(rem_p1, 0, degree - 1)
        equations.extend(local)
        rows.append({"colour": colour, "degree": degree, "equation_count": len(local)})
    if len(equations) != 10:
        raise RuntimeError(f"CRT equation count {len(equations)} != 10")
    return {"equations": equations, "factors": factors, "rows": rows, "m_symbols": m_symbols}


def make_singular_script(
    *,
    prime: int,
    variables: list[sp.Symbol],
    equations: list[sp.Expr] | list[str],
    label: str,
) -> str:
    variable_text = ",".join(str(v) for v in variables)
    equation_text = []
    for equation in equations:
        text = equation if isinstance(equation, str) else singular_expr(equation)
        if text != "0":
            equation_text.append(text)
    if not equation_text:
        equation_text = ["0"]
    return "\n".join(
        [
            f"// {label}",
            f"ring r={prime},({variable_text}),dp;",
            "option(redSB);",
            "ideal I=" + ",\n".join(equation_text) + ";",
            "ideal G=std(I);",
            "poly nf=reduce(1,G);",
            'if (nf==0) { print("CODEX_UNIT_IDEAL"); } else { print("CODEX_NONUNIT_IDEAL"); }',
            'print("CODEX_GB_SIZE");',
            "print(size(G));",
            "quit;",
            "",
        ]
    )


def terminate_process(proc: subprocess.Popen[str]) -> None:
    if proc.poll() is not None:
        return
    if os.name == "nt":
        proc.kill()
        return
    try:
        os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(timeout=3)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        if proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass


def run_singular(singular: str, script_path: Path, timeout_seconds: float) -> dict[str, Any]:
    started = time.monotonic()
    kwargs: dict[str, Any] = {}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    proc = subprocess.Popen(
        [singular, "-q", str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        **kwargs,
    )
    try:
        stdout, _ = proc.communicate(timeout=max(1.0, timeout_seconds))
        timed_out = False
    except subprocess.TimeoutExpired:
        terminate_process(proc)
        stdout, _ = proc.communicate()
        timed_out = True
    elapsed = time.monotonic() - started
    if timed_out:
        status = "TIMEOUT"
    elif "CODEX_UNIT_IDEAL" in stdout and proc.returncode == 0:
        status = "UNIT"
    elif "CODEX_NONUNIT_IDEAL" in stdout and proc.returncode == 0:
        status = "NONUNIT"
    else:
        status = "ERROR"
    return {
        "status": status,
        "returncode": proc.returncode,
        "timed_out": timed_out,
        "elapsed_seconds": elapsed,
        "stdout_tail": stdout[-4000:],
        "script_sha256": sha256_file(script_path),
        "script_bytes": script_path.stat().st_size,
    }


def positive_control_script(prime: int) -> tuple[str, dict[str, Any]]:
    w = sp.symbols("w")
    e_symbols = list(sp.symbols("ce0:5"))
    scalar = sp.symbols("csqc")
    h = sp.Poly(w**5 + w + 1, w)
    discriminant = -27 * h * h
    root = sp.Poly(w**5 + sum(e_symbols[i] * w**i for i in range(5)), w)
    equations = square_equations(discriminant, root, scalar, 10)
    planted = {scalar: -27, e_symbols[0]: 1, e_symbols[1]: 1}
    planted.update({e_symbols[i]: 0 for i in range(2, 5)})
    anchors = [symbol - value for symbol, value in planted.items()]
    script = make_singular_script(
        prime=prime,
        variables=e_symbols + [scalar],
        equations=equations + anchors,
        label="same square_equations path: planted y^3=(w^5+w+1)",
    )
    gcd = sp.gcd(h, h.diff())
    return script, {
        "name": "cyclic_trigonal_genus4_y3_equals_w5_plus_w_plus_1",
        "same_square_equations_function": True,
        "h_squarefree_over_Q": gcd.degree() == 0,
        "finite_ramification_contribution": 10,
        "infinity_ramification_contribution": 2,
        "riemann_hurwitz_genus": 4,
        "expected_singular_status": "NONUNIT",
    }


def upstream_gate() -> dict[str, Any]:
    result = json.loads(UPSTREAM_RESULT.read_text(encoding="utf-8"))
    check = json.loads(UPSTREAM_CHECK.read_text(encoding="utf-8"))
    passed = bool(
        result.get("C2_0_regression_gate", {}).get("all_pass")
        and result.get("C2_1_D_construction", {}).get("coeff_w36_is_zero")
        and check.get("all_checks_true")
    )
    return {
        "pass": passed,
        "C2_0_all_pass": result.get("C2_0_regression_gate", {}).get("all_pass"),
        "C2_1_w36_zero": result.get("C2_1_D_construction", {}).get("coeff_w36_is_zero"),
        "independent_stage1_checker_pass": check.get("all_checks_true"),
        "result_sha256": sha256_file(UPSTREAM_RESULT),
        "check_sha256": sha256_file(UPSTREAM_CHECK),
        "upstream_run_id": "31592557898",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--work-dir", type=Path, default=DEFAULT_WORK)
    parser.add_argument("--budget-seconds", type=float, default=1400.0)
    parser.add_argument("--per-system-seconds", type=float, default=90.0)
    parser.add_argument("--prime", type=int, default=7)
    parser.add_argument("--omega", type=int, default=2)
    parser.add_argument("--singular", default="Singular")
    parser.add_argument("--build-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    out: dict[str, Any] = {
        "schema": "r13-r1p/v3-k3-crt-c2-main/v1",
        "status": "RUNNING",
        "generated_by": {
            "script": "search/w9_k3_crt_c2_main_gha.py",
            "script_sha256": sha256_file(Path(__file__)),
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "github_sha": os.environ.get("GITHUB_SHA"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "started_at_utc": utc_now(),
        },
        "universe": {
            "window": "K^(9)",
            "lane": "crt-C2",
            "layer": "(s,f)=(0,5)",
            "colour_degree_distributions": [list(row) for row in mu3_distributions()],
            "galois_half_rule": "f_omega >= f_omega2",
            "coefficient_field": "F9=Q(zeta36); equations use Q(zeta3) and exact good-prime reductions",
            "prime": args.prime,
            "omega_mod_prime": args.omega,
            "budget_seconds": args.budget_seconds,
            "per_system_seconds": args.per_system_seconds,
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
        "d_no_interpretation": "bounded exact computation; UNKNOWN is retained",
        "C2_0_C2_1_upstream_gate": upstream_gate(),
    }
    atomic_write_json(args.checkpoint, out)
    if not out["C2_0_C2_1_upstream_gate"]["pass"]:
        out["status"] = "STOPPED_FAIL_CLOSED_UPSTREAM"
        atomic_write_json(args.output, out)
        atomic_write_json(args.checkpoint, out)
        return 1
    if pow(args.omega, 3, args.prime) != 1 or args.omega % args.prime == 1:
        out["status"] = "STOPPED_BAD_MU3_REDUCTION"
        atomic_write_json(args.output, out)
        atomic_write_json(args.checkpoint, out)
        return 1

    build_started = time.monotonic()
    common = build_common_system()
    out["C2_2_system_design"] = {
        "ordering": ["mu3_CRT", "D_equals_cE2", "genus", "order9"],
        "step_C1_high_elimination": common["solve_rows"],
        "free_variables_before_CRT": 10,
        "CRT_equations_at_f5": 10,
        "dimension_after_CRT_expected_but_not_assumed": 5,
        "D_degree": common["discriminant"].degree(),
        "E_degree": 17,
        "square_coefficient_equations": len(common["square_eqs"]),
        "build_elapsed_seconds": time.monotonic() - build_started,
        "common_square_equations_sha256": sha256_bytes("\n".join(common["square_eq_strings"]).encode("utf-8")),
        "mod_p_unit_ideal_logic": "UNIT after good reduction implies the characteristic-zero ideal is UNIT; NONUNIT does not imply existence",
        "open_handling": "closure first; then easy-open Rabinowitsch superset. Pairwise/collision opens are not needed for a UNIT proof and NONUNIT remains UNKNOWN",
    }
    atomic_write_json(args.checkpoint, out)

    if args.build_only:
        manifests = []
        for distribution in mu3_distributions():
            crt = crt_equations(common, distribution, args.omega)
            manifests.append(
                {
                    "distribution": list(distribution),
                    "equation_count": len(crt["equations"]),
                    "rows": crt["rows"],
                    "sha256": sha256_bytes("\n".join(singular_expr(e) for e in crt["equations"]).encode("utf-8")),
                }
            )
        out["build_only_manifests"] = manifests
        out["status"] = "BUILD_ONLY_COMPLETE"
        out["elapsed_seconds"] = time.monotonic() - started
        atomic_write_json(args.output, out)
        atomic_write_json(args.checkpoint, out)
        print("CRT_C2_BUILD_ONLY_COMPLETE", flush=True)
        return 0

    singular_path = shutil.which(args.singular)
    if singular_path is None:
        out["status"] = "UNKNOWN_SINGULAR_NOT_FOUND"
        out["elapsed_seconds"] = time.monotonic() - started
        atomic_write_json(args.output, out)
        atomic_write_json(args.checkpoint, out)
        return 2

    control_text, control_meta = positive_control_script(args.prime)
    control_path = args.work_dir / "positive_control.sing"
    control_path.write_text(control_text, encoding="utf-8")
    control_run = run_singular(singular_path, control_path, min(args.per_system_seconds, args.budget_seconds))
    control_meta["run"] = control_run
    control_meta["pass"] = bool(
        control_meta["h_squarefree_over_Q"]
        and control_meta["riemann_hurwitz_genus"] == 4
        and control_run["status"] == "NONUNIT"
    )
    out["positive_control"] = control_meta
    atomic_write_json(args.checkpoint, out)
    if not control_meta["pass"]:
        out["status"] = "STOPPED_FAIL_CLOSED_POSITIVE_CONTROL"
        out["elapsed_seconds"] = time.monotonic() - started
        atomic_write_json(args.output, out)
        atomic_write_json(args.checkpoint, out)
        return 1

    base_variables = (
        list(common["e_symbols"])
        + [common["scalar"]]
        + list(common["p_symbols"])
        + [common["g0"], common["g1"], common["ss"], common["pp"]]
        + list(sp.symbols("m0:5"))
    )
    easy_inverse_variables = list(sp.symbols("iv0:5"))
    results = []
    for index, distribution in enumerate(mu3_distributions()):
        elapsed = time.monotonic() - started
        remaining = args.budget_seconds - elapsed
        if remaining <= 5:
            results.append({"distribution": list(distribution), "status": "NOT_RUN_BUDGET_EXHAUSTED"})
            continue
        crt = crt_equations(common, distribution, args.omega)
        closure_equations: list[sp.Expr] | list[str] = list(common["square_eq_strings"]) + crt["equations"]
        label = "f" + "_".join(str(x) for x in distribution) + "_closure"
        script_path = args.work_dir / f"{index:02d}_{label}.sing"
        script_text = make_singular_script(
            prime=args.prime,
            variables=base_variables,
            equations=closure_equations,
            label=label,
        )
        script_path.write_text(script_text, encoding="utf-8")
        out["current_system"] = {"index": index, "distribution": list(distribution), "phase": "closure"}
        atomic_write_json(args.checkpoint, out)
        closure_run = run_singular(
            singular_path,
            script_path,
            min(args.per_system_seconds, max(1.0, remaining - 2)),
        )
        row: dict[str, Any] = {
            "distribution": list(distribution),
            "crt_rows": crt["rows"],
            "closure": closure_run,
            "status": None,
        }
        if closure_run["status"] == "UNIT":
            row["status"] = "EMPTY_BY_CLOSURE_MOD_P_UNIT"
            results.append(row)
            out["C2_2_distribution_results"] = results
            atomic_write_json(args.checkpoint, out)
            continue
        if closure_run["status"] != "NONUNIT":
            row["status"] = "UNKNOWN_CLOSURE_" + closure_run["status"]
            results.append(row)
            out["C2_2_distribution_results"] = results
            atomic_write_json(args.checkpoint, out)
            continue

        # Easy open conditions define a superset of the actual open stratum.
        # UNIT for this superset is already a valid emptiness obstruction.
        p1_const = common["p1"].nth(0)
        e5_open = common["p2"].nth(5) - common["p1"].nth(11)
        ab_open = common["ss"] ** 2 - 4 * common["pp"]
        colour_constant = sp.Integer(1)
        for factor, degree in zip(crt["factors"], distribution):
            if degree:
                colour_constant *= factor.nth(0)
        open_values = [common["scalar"], p1_const, e5_open, ab_open, colour_constant]
        open_equations = [easy_inverse_variables[i] * value - 1 for i, value in enumerate(open_values)]
        remaining = args.budget_seconds - (time.monotonic() - started)
        if remaining <= 5:
            row["status"] = "UNKNOWN_CORE_OPEN_NOT_RUN_BUDGET"
            results.append(row)
            out["C2_2_distribution_results"] = results
            atomic_write_json(args.checkpoint, out)
            continue
        core_label = "f" + "_".join(str(x) for x in distribution) + "_core_open"
        core_path = args.work_dir / f"{index:02d}_{core_label}.sing"
        core_text = make_singular_script(
            prime=args.prime,
            variables=base_variables + easy_inverse_variables,
            equations=closure_equations + open_equations,
            label=core_label,
        )
        core_path.write_text(core_text, encoding="utf-8")
        out["current_system"] = {"index": index, "distribution": list(distribution), "phase": "core_open"}
        atomic_write_json(args.checkpoint, out)
        core_run = run_singular(
            singular_path,
            core_path,
            min(args.per_system_seconds, max(1.0, remaining - 2)),
        )
        row["core_open"] = core_run
        row["status"] = (
            "EMPTY_BY_CORE_OPEN_SUPERSET_MOD_P_UNIT"
            if core_run["status"] == "UNIT"
            else "UNKNOWN_CORE_OPEN_" + core_run["status"]
        )
        results.append(row)
        out["C2_2_distribution_results"] = results
        atomic_write_json(args.checkpoint, out)

    empty_statuses = {
        "EMPTY_BY_CLOSURE_MOD_P_UNIT",
        "EMPTY_BY_CORE_OPEN_SUPERSET_MOD_P_UNIT",
    }
    all_distributions_empty = len(results) == 12 and all(row.get("status") in empty_statuses for row in results)
    out["C2_2_summary"] = {
        "distribution_count_expected": 12,
        "distribution_count_recorded": len(results),
        "all_distributions_empty_by_mod_p_unit": all_distributions_empty,
        "unknown_distribution_count": sum(row.get("status") not in empty_statuses for row in results),
    }
    if all_distributions_empty:
        out["status"] = "COMPLETE_F5_LAYER_EMPTY_BY_GOOD_REDUCTION"
        out["layer_0_5_solution_exists_over_F9"] = False
        out["C2_3_genus"] = "NOT_REACHED_NO_CANDIDATE"
        out["C2_4_order_P0_minus_Pinf"] = "NOT_REACHED_NO_CANDIDATE"
        return_code = 0
    else:
        out["status"] = "UNKNOWN_BOUNDED_C2_2"
        out["layer_0_5_solution_exists_over_F9"] = None
        out["C2_3_genus"] = "NOT_REACHED_C2_2_UNKNOWN"
        out["C2_4_order_P0_minus_Pinf"] = "NOT_REACHED_C2_2_UNKNOWN"
        return_code = 2
    out.pop("current_system", None)
    out["elapsed_seconds"] = time.monotonic() - started
    atomic_write_json(args.output, out)
    atomic_write_json(args.checkpoint, out)
    print(f"W9_K3_CRT_C2_{out['status']} elapsed={out['elapsed_seconds']:.1f}s", flush=True)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
