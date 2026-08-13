#!/usr/bin/env python3
"""Independent checker for the task-130 affine gate artifact.

The checker does not import the producer.  It uses a different basis for the
9-point augmentation heart, hard-coded audited permutations instead of GF(8)
arithmetic, and a separately written finite-field elimination routine.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
P = 3
ONE = tuple(range(9))
S = (2, 1, 0, 8, 5, 4, 7, 6, 3)
T = (5, 7, 4, 1, 8, 6, 0, 3, 2)
CHARS = ((1, 0), (0, 1), (1, 1))


def file_sha(path: Path) -> str:
    accumulator = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            piece = handle.read(65536)
            if not piece:
                break
            accumulator.update(piece)
    return accumulator.hexdigest()


def value_sha(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def replace_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    work = path.with_suffix(path.suffix + ".new")
    work.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(work, path)


def after(first: tuple[int, ...], second: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(first[second[position]] for position in range(len(first)))


def pinv(item: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * len(item)
    for old, new in enumerate(item):
        answer[new] = old
    return tuple(answer)


def ppow(item: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    answer = ONE
    factor = item
    while exponent:
        if exponent % 2:
            answer = after(factor, answer)
        factor = after(factor, factor)
        exponent //= 2
    return answer


def closure(first: tuple[int, ...], second: tuple[int, ...]) -> int:
    steps = (first, second, pinv(first), pinv(second))
    known = {ONE}
    frontier = [ONE]
    while frontier:
        old = frontier.pop(0)
        for step in steps:
            new = after(old, step)
            if new not in known:
                known.add(new)
                frontier.append(new)
    return len(known)


def zeros(height: int, width: int) -> list[list[int]]:
    return [[0 for _ in range(width)] for _ in range(height)]


def eye(size: int) -> list[list[int]]:
    answer = zeros(size, size)
    for index in range(size):
        answer[index][index] = 1
    return answer


def mm(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
    height = len(first)
    width = len(second[0])
    middle = len(second)
    answer = zeros(height, width)
    for i in range(height):
        for k in range(middle):
            coefficient = first[i][k] % P
            if coefficient:
                for j in range(width):
                    answer[i][j] = (
                        answer[i][j] + coefficient * second[k][j]
                    ) % P
    return answer


def madd(*items: list[list[int]]) -> list[list[int]]:
    return [
        [sum(item[i][j] for item in items) % P for j in range(len(items[0][0]))]
        for i in range(len(items[0]))
    ]


def msub(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
    return [
        [(first[i][j] - second[i][j]) % P for j in range(len(first[0]))]
        for i in range(len(first))
    ]


def rank_mod3(item: list[list[int]]) -> int:
    rows = [list(map(lambda entry: entry % P, row)) for row in item]
    pivot_row = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        choice = None
        for row in range(pivot_row, len(rows)):
            if rows[row][column]:
                choice = row
                break
        if choice is None:
            continue
        rows[pivot_row], rows[choice] = rows[choice], rows[pivot_row]
        if rows[pivot_row][column] == 2:
            rows[pivot_row] = [(2 * entry) % P for entry in rows[pivot_row]]
        for row in range(pivot_row + 1, len(rows)):
            multiple = rows[row][column]
            if multiple:
                rows[row] = [
                    (rows[row][j] - multiple * rows[pivot_row][j]) % P
                    for j in range(width)
                ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def minv(item: list[list[int]]) -> list[list[int]]:
    size = len(item)
    rows = [item[i][:] + eye(size)[i] for i in range(size)]
    for column in range(size):
        choice = next(
            (row for row in range(column, size) if rows[row][column] % P), None
        )
        if choice is None:
            raise RuntimeError("singular matrix")
        rows[column], rows[choice] = rows[choice], rows[column]
        scale = 1 if rows[column][column] == 1 else 2
        rows[column] = [(scale * entry) % P for entry in rows[column]]
        for row in range(size):
            if row == column:
                continue
            scale = rows[row][column] % P
            if scale:
                rows[row] = [
                    (rows[row][j] - scale * rows[column][j]) % P
                    for j in range(2 * size)
                ]
    return [row[size:] for row in rows]


def equal(first: list[list[int]], second: list[list[int]]) -> bool:
    return rank_mod3(msub(first, second)) == 0


def alternate_heart(permutation: tuple[int, ...]) -> list[list[int]]:
    """Heart basis e_i-e_0 (i=1,...,7), eliminating e_8-e_0."""
    answer = zeros(7, 7)
    for column, point in enumerate(range(1, 8)):
        vector = [0] * 9
        vector[permutation[point]] = (vector[permutation[point]] + 1) % P
        vector[permutation[0]] = (vector[permutation[0]] - 1) % P
        coefficient_8 = vector[8]
        for row, coordinate in enumerate(range(1, 8)):
            answer[row][column] = (vector[coordinate] - coefficient_8) % P
    return answer


def signed_blocks(base: list[list[int]], abelian_value: tuple[int, int]) -> list[list[int]]:
    answer = zeros(21, 21)
    for block, character in enumerate(CHARS):
        dot = sum(character[i] * abelian_value[i] for i in range(2)) % 2
        sign = 2 if dot else 1
        for row in range(7):
            for column in range(7):
                answer[7 * block + row][7 * block + column] = sign * base[row][column] % P
    return answer


def block_transport(base: list[list[int]], destinations: tuple[int, int, int]) -> list[list[int]]:
    answer = zeros(21, 21)
    for source, target in enumerate(destinations):
        for row in range(7):
            for column in range(7):
                answer[7 * target + row][7 * source + column] = base[row][column]
    return answer


def relation_checks(
    rho_x: list[list[int]],
    rho_y: list[list[int]],
    theta: list[list[int]],
    tau: list[list[int]],
) -> dict[str, bool]:
    unit = eye(21)
    theta_inverse = minv(theta)
    tau_inverse = minv(tau)
    rho_z = minv(mm(rho_x, rho_y))
    return {
        "rho_XYZ_identity": equal(mm(mm(rho_x, rho_y), rho_z), unit),
        "theta_squared_identity": equal(mm(theta, theta), unit),
        "tau_cubed_identity": equal(mm(mm(tau, tau), tau), unit),
        "theta_X_to_Y": equal(mm(mm(theta, rho_x), theta_inverse), rho_y),
        "theta_Y_to_X": equal(mm(mm(theta, rho_y), theta_inverse), rho_x),
        "tau_X_to_Y": equal(mm(mm(tau, rho_x), tau_inverse), rho_y),
        "tau_Y_to_Z": equal(mm(mm(tau, rho_y), tau_inverse), rho_z),
    }


def h1_numbers(theta: list[list[int]], tau: list[list[int]]) -> dict[str, int]:
    unit = eye(21)
    tau2 = mm(tau, tau)
    condition_two = madd(unit, theta)
    condition_three = madd(unit, tau, tau2)
    principal = msub(theta, unit) + msub(tau, unit)
    dimension_two = 21 - rank_mod3(condition_two)
    dimension_three = 21 - rank_mod3(condition_three)
    principal_rank = rank_mod3(principal)
    return {
        "ker_I_plus_theta_dimension": dimension_two,
        "ker_I_plus_tau_plus_tau2_dimension": dimension_three,
        "coboundary_rank": principal_rank,
        "joint_invariant_dimension": 21 - principal_rank,
        "H1_C2_free_C3_dimension": dimension_two + dimension_three - principal_rank,
        "V_conjugacy_class_count_for_marked_lifts": P
        ** (dimension_two + dimension_three - principal_rank),
    }


def table_data() -> dict[str, object]:
    installation = Path(r"C:\Program Files\GAP-4.16.0\runtime\opt\gap-4.16.0")
    modular_path = installation / "pkg/ctbllib/data/ctbline1.tbl"
    ordinary_path = installation / "pkg/ctbllib/data/ctoline1.tbl"
    modular = modular_path.read_text(encoding="utf-8")
    ordinary = ordinary_path.read_text(encoding="utf-8")
    modular_match = re.search(
        r'MBT\("L2\(8\)",3,(.*?)\n0\);', modular, flags=re.DOTALL
    )
    ordinary_match = re.search(
        r'MOT\("L2\(8\)",(.*?)\nARC\("L2\(8\)"', ordinary, flags=re.DOTALL
    )
    if modular_match is None or ordinary_match is None:
        raise RuntimeError("local L2(8) table records not found")
    modular_record = re.sub(r"\s+", "", modular_match.group(1))
    ordinary_record = re.sub(r"\s+", "", ordinary_match.group(1))
    requirements = {
        "blocks": "[1,1,2,3,4]" in modular_record,
        "defects": "[2,0,0,0]" in modular_record,
        "tree": "[[[1,6],[2,3,4,5,6]]]" in modular_record,
        "automorphism": "[(3,4,5)]" in modular_record,
        "class_centralizers": "[504,8,9,7,7,7,9,9,9]" in ordinary_record,
        "degree_one_row": "[1,1,1,1,1,1,1,1,1]" in ordinary_record,
        "degree_seven_rows": (
            "[7,-1,-2,0,0,0,1,1,1]" in ordinary_record
            and "[7,-1,1,0,0,0," in ordinary_record
            and "[GALOIS,[3,4]],[GALOIS,[3,2]]" in ordinary_record
        ),
        "degree_eight_row": "[8,0,-1,1,1,1,-1,-1,-1]" in ordinary_record,
        "degree_nine_rows": (
            "[9,1,0," in ordinary_record
            and "[GALOIS,[7,3]],[GALOIS,[7,2]]]" in ordinary_record
        ),
    }
    if not all(requirements.values()):
        raise RuntimeError("local L2(8) table fields changed")
    # Tree vertices have degrees 1 and 7 because the last principal-block
    # ordinary degree is 8=1+7.  The three defect-zero blocks have degree 9.
    return {
        "source_fields_present": requirements,
        "ordinary_class_centralizer_orders": [504, 8, 9, 7, 7, 7, 9, 9, 9],
        "ordinary_character_degrees": [1, 7, 7, 7, 7, 8, 9, 9, 9],
        "brauer_degrees_characteristic_3": [1, 7, 9, 9, 9],
        "seven_dimensional_irreducible_count": 1,
        "seven_dimensional_out_orbit_size": 1,
        "nine_dimensional_out_orbit": [3, 4, 5],
        "modular_table_sha256": file_sha(modular_path),
        "ordinary_table_sha256": file_sha(ordinary_path),
    }


def fixture_check() -> dict[str, object]:
    values = []
    solutions = []
    for first in range(3):
        for second in range(3):
            direct = ((first + 2 * first) % 3, (second + second) % 3)
            affine = (0, 2 * second % 3)
            values.append(direct == affine)
            if direct == (0, 0):
                solutions.append([first, second])
    return {
        "all_nine_values_affine": all(values),
        "solution_count": len(solutions),
        "solutions": solutions,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="search/certs/vnbit_affine_gate_raw_v1_20260813.json",
    )
    parser.add_argument(
        "--output",
        default="search/certs/vnbit_affine_gate_check_v1_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/vnbit_affine_gate_check_v1_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    raw_path = BASE / args.input
    output_path = BASE / args.output
    checkpoint_path = BASE / args.checkpoint
    began = time.monotonic()
    checkpoint: dict[str, object] = {
        "schema": "vnbit_affine_gate_check_checkpoint/v1",
        "stage": "start",
        "complete": False,
    }
    replace_json(checkpoint_path, checkpoint)

    def record(stage: str, **extra: object) -> None:
        checkpoint.update(
            stage=stage,
            elapsed_ms=int(1000 * (time.monotonic() - began)),
            **extra,
        )
        replace_json(checkpoint_path, checkpoint)

    def timeout() -> None:
        if not checkpoint.get("complete"):
            record("hard_timeout")
            os._exit(124)

    alarm = threading.Timer(args.hard_timeout_seconds, timeout)
    alarm.daemon = True
    alarm.start()
    try:
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        record("input_loaded")

        w = after(pinv(T), S)
        x = ppow(w, 2)
        y = after(T, after(x, pinv(T)))
        z = pinv(after(x, y))
        c0_independent = {
            "P_order": closure(x, y),
            "S_in_P": None,
            "T_in_P": None,
            "X_order_ninth_power": ppow(x, 9) == ONE,
            "Y_order_ninth_power": ppow(y, 9) == ONE,
            "XYZ_identity": after(after(x, y), z) == ONE,
            "theta_X_to_Y": after(S, after(x, S)) == y,
            "theta_Y_to_X": after(S, after(y, S)) == x,
            "tau_X_to_Y": after(T, after(x, pinv(T))) == y,
            "tau_Y_to_Z": after(T, after(y, pinv(T))) == z,
        }
        # Membership is checked with a second closure that keeps its elements.
        generated = {ONE}
        frontier = [ONE]
        moves = (x, y, pinv(x), pinv(y))
        while frontier:
            old = frontier.pop()
            for move in moves:
                new = after(move, old)
                if new not in generated:
                    generated.add(new)
                    frontier.append(new)
        c0_independent["S_in_P"] = S in generated
        c0_independent["T_in_P"] = T in generated
        if c0_independent["P_order"] != 504 or not all(
            value for key, value in c0_independent.items() if key != "P_order"
        ):
            raise RuntimeError("independent C-0 reconstruction changed")
        record("C0_rebuilt")

        tables = table_data()
        record("C1_rebuilt")

        heart_x = alternate_heart(x)
        heart_y = alternate_heart(y)
        rho_x = signed_blocks(heart_x, (1, 0))
        rho_y = signed_blocks(heart_y, (0, 1))
        theta = block_transport(alternate_heart(S), (1, 0, 2))
        tau = block_transport(alternate_heart(T), (2, 0, 1))
        own_relations = relation_checks(rho_x, rho_y, theta, tau)
        own_h1 = h1_numbers(theta, tau)
        if not all(own_relations.values()) or own_h1 != {
            "ker_I_plus_theta_dimension": 11,
            "ker_I_plus_tau_plus_tau2_dimension": 14,
            "coboundary_rank": 21,
            "joint_invariant_dimension": 0,
            "H1_C2_free_C3_dimension": 4,
            "V_conjugacy_class_count_for_marked_lifts": 81,
        }:
            raise RuntimeError("independent module reconstruction changed")
        record("C2_rebuilt")

        raw_relations = relation_checks(
            raw["C2"]["rho_X"],
            raw["C2"]["rho_Y"],
            raw["C2"]["theta_operator"],
            raw["C2"]["tau_operator"],
        )
        raw_h1 = h1_numbers(
            raw["C2"]["theta_operator"], raw["C2"]["tau_operator"]
        )
        fixture = fixture_check()
        expected_source_hashes = {
            name: file_sha(BASE / name)
            for name in (
                "ops/inbox_codex/sol_task_130_affine.txt",
                "docs/notes/vnbit_compact_route_v1.md",
                "docs/notes/vnbit_compact_route_v1_addendum_novelty.md",
                "search/week3-psl-S4.g",
            )
        }
        normalized_raw_source_hashes = {
            name.replace("\\", "/"): value
            for name, value in raw["source_sha256"].items()
        }
        comparisons = {
            "source_hashes_equal_current_files": normalized_raw_source_hashes
            == expected_source_hashes,
            "raw_C0_order_equal": raw["C0"]["P_order"]
            == c0_independent["P_order"],
            "raw_C0_inner_equal": raw["C0"]["S_in_P"]
            and raw["C0"]["T_in_P"],
            "raw_C1_degrees_equal": raw["C1"]["brauer_degrees_characteristic_3"]
            == tables["brauer_degrees_characteristic_3"],
            "raw_C1_seven_count_equal": raw["C1"]["seven_dimensional_irreducible_count"]
            == tables["seven_dimensional_irreducible_count"],
            "raw_C1_orbit_size_equal": raw["C1"]["seven_dimensional_out_orbit_size"]
            == tables["seven_dimensional_out_orbit_size"],
            "raw_C2_dimension_equal": raw["C2"]["dim_V"] == 21,
            "raw_C2_relations_recomputed": all(raw_relations.values()),
            "raw_H1_equal_independent": all(
                raw["marked_lift_preflight"][key] == value
                for key, value in own_h1.items()
            ),
            "raw_fixture_equal_independent": (
                raw["lift_affine_calibration"]["all_nine_values_affine"]
                == fixture["all_nine_values_affine"]
                and raw["lift_affine_calibration"]["solution_count"]
                == fixture["solution_count"]
                and raw["lift_affine_calibration"]["solutions"]
                == fixture["solutions"]
            ),
            "raw_stage_boundary_equal": raw["stage_boundary"]["status"]
            == "UNKNOWN_STOP_MARKED_EPIMORPHISM_UNDEFINED",
            "raw_measurement_not_started": raw["stage_boundary"][
                "obstruction_classes_measured"
            ]
            == 0
            and raw["stage_boundary"]["lift_table_rows"] == 0,
            "raw_noncontact_all_false": not any(raw["noncontact"].values()),
        }
        record("producer_compared", comparisons=comparisons)
        if not all(comparisons.values()):
            raise RuntimeError("producer/checker comparison changed")

        result = {
            "schema": "vnbit_affine_gate_check/v1",
            "run_id": "vnbit-affine-check-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "generated_by": {
                "script": "search/check_vnbit_affine_gate_v1.py",
                "script_sha256": file_sha(Path(__file__)),
            },
            "input": {
                "path": args.input,
                "sha256": file_sha(raw_path),
                "schema": raw["schema"],
            },
            "helper_disjointness": {
                "producer_imported": False,
                "P_model": "hard-coded audited permutations on 9 points",
                "heart_basis": "e_i-e_0 for i=1..7, eliminating e_8-e_0",
                "field_elimination": "independent forward elimination",
            },
            "C0_independent": c0_independent,
            "C1_independent": tables,
            "C2_independent": {
                "dim_V": 21,
                "rho_generators_sha256_in_alternate_basis": value_sha(
                    [rho_x, rho_y]
                ),
                "outer_operators_sha256_in_alternate_basis": value_sha(
                    [theta, tau]
                ),
                "relations": own_relations,
            },
            "raw_relations_recomputed": raw_relations,
            "marked_lift_preflight_independent": own_h1,
            "affine_fixture_independent": fixture,
            "comparisons": comparisons,
            "all_equalities_true": all(comparisons.values()),
            "stage_boundary": raw["stage_boundary"],
            "scope": raw["endgame_scope"],
            "noncontact": raw["noncontact"],
        }
        replace_json(output_path, result)
        record("complete", complete=True, output_sha256=file_sha(output_path))
        return 0
    finally:
        alarm.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
