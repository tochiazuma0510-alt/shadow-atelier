#!/usr/bin/env python3
"""Helper-disjoint checker for the task-131 marked-action stop.

This checker does not import the producer.  It uses audited 9-point
permutations, an alternate augmentation-heart basis, and pure-Python
elimination over F3.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P = 3
ONE = tuple(range(9))
S_PERM = (2, 1, 0, 8, 5, 4, 7, 6, 3)
T_PERM = (5, 7, 4, 1, 8, 6, 0, 3, 2)
CHARS = ((1, 0), (0, 1), (1, 1))


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        while True:
            block = source.read(65536)
            if not block:
                return h.hexdigest()
            h.update(block)


def replace_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".new")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def after(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def inverse(value: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * len(value)
    for source, target in enumerate(value):
        answer[target] = source
    return tuple(answer)


def ppow(value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    answer = ONE
    factor = value
    while exponent:
        if exponent & 1:
            answer = after(answer, factor)
        factor = after(factor, factor)
        exponent >>= 1
    return answer


def zeros(rows: int, columns: int) -> list[list[int]]:
    return [[0] * columns for _ in range(rows)]


def eye(size: int) -> list[list[int]]:
    answer = zeros(size, size)
    for index in range(size):
        answer[index][index] = 1
    return answer


def multiply(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    answer = zeros(len(left), len(right[0]))
    for row in range(len(left)):
        for middle in range(len(right)):
            coefficient = left[row][middle] % P
            if coefficient:
                for column in range(len(right[0])):
                    answer[row][column] = (
                        answer[row][column]
                        + coefficient * right[middle][column]
                    ) % P
    return answer


def subtract(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [(a - b) % P for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def equal(left: list[list[int]], right: list[list[int]]) -> bool:
    return all(a % P == b % P for x, y in zip(left, right) for a, b in zip(x, y))


def rank_mod3(value: list[list[int]]) -> int:
    work = [[entry % P for entry in row] for row in value]
    pivot = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        choice = next(
            (row for row in range(pivot, len(work)) if work[row][column]),
            None,
        )
        if choice is None:
            continue
        work[pivot], work[choice] = work[choice], work[pivot]
        if work[pivot][column] == 2:
            work[pivot] = [(2 * entry) % P for entry in work[pivot]]
        for row in range(pivot + 1, len(work)):
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    (entry - coefficient * base) % P
                    for entry, base in zip(work[row], work[pivot])
                ]
        pivot += 1
        if pivot == len(work):
            break
    return pivot


def alternate_heart(permutation: tuple[int, ...]) -> list[list[int]]:
    """Basis e_i-e_0, i=1,...,7, eliminating e_8-e_0."""
    answer = zeros(7, 7)
    for column, point in enumerate(range(1, 8)):
        vector = [0] * 9
        vector[permutation[point]] = (vector[permutation[point]] + 1) % P
        vector[permutation[0]] = (vector[permutation[0]] - 1) % P
        coefficient_eight = vector[8]
        for row, coordinate in enumerate(range(1, 8)):
            answer[row][column] = (
                vector[coordinate] - coefficient_eight
            ) % P
    return answer


def signed_blocks(base: list[list[int]], abelian: tuple[int, int]) -> list[list[int]]:
    answer = zeros(21, 21)
    for block, character in enumerate(CHARS):
        sign = 2 if sum(a * b for a, b in zip(character, abelian)) % 2 else 1
        for row in range(7):
            for column in range(7):
                answer[7 * block + row][7 * block + column] = (
                    sign * base[row][column]
                ) % P
    return answer


def block_transport(
    base: list[list[int]],
    destinations: tuple[int, int, int],
    scalars: tuple[int, int, int] = (1, 1, 1),
) -> list[list[int]]:
    answer = zeros(21, 21)
    for source, target in enumerate(destinations):
        for row in range(7):
            for column in range(7):
                answer[7 * target + row][7 * source + column] = (
                    scalars[source] * base[row][column]
                ) % P
    return answer


def small_monomial(
    destinations: tuple[int, int, int], scalars: tuple[int, int, int]
) -> list[list[int]]:
    answer = zeros(3, 3)
    for source, target in enumerate(destinations):
        answer[target][source] = scalars[source]
    return answer


def enumerate_scalar_factors() -> list[dict[str, list[int]]]:
    theta_dest = (1, 0, 2)
    tau_dest = (2, 0, 1)
    target_x = [[2, 0, 0], [0, 1, 0], [0, 0, 2]]
    target_y = [[1, 0, 0], [0, 2, 0], [0, 0, 2]]
    unit = eye(3)
    answer = []
    for theta_scalars in itertools.product((1, 2), repeat=3):
        theta = small_monomial(theta_dest, theta_scalars)
        for tau_scalars in itertools.product((1, 2), repeat=3):
            tau = small_monomial(tau_dest, tau_scalars)
            tau2 = multiply(tau, tau)
            first = multiply(tau2, theta)
            second = multiply(theta, tau2)
            if not equal(multiply(theta, theta), unit):
                continue
            if not equal(multiply(tau2, tau), unit):
                continue
            if not equal(multiply(first, first), target_x):
                continue
            if not equal(multiply(second, second), target_y):
                continue
            answer.append(
                {
                    "theta_source_scalars": list(theta_scalars),
                    "tau_source_scalars": list(tau_scalars),
                }
            )
    return answer


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="search/certs/vnbit_compact_measurement_raw_v2_20260813.json",
    )
    parser.add_argument(
        "--output",
        default="search/certs/vnbit_compact_measurement_check_v2_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/vnbit_compact_measurement_check_v2_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    input_path = ROOT / args.input
    output_path = ROOT / args.output
    checkpoint_path = ROOT / args.checkpoint
    began = time.monotonic()
    state: dict[str, object] = {
        "schema": "vnbit_compact_measurement_check_checkpoint/v2",
        "stage": "start",
        "complete": False,
    }
    replace_json(checkpoint_path, state)

    def update(stage: str, **fields: object) -> None:
        state.update(
            stage=stage,
            elapsed_ms=int(1000 * (time.monotonic() - began)),
            **fields,
        )
        replace_json(checkpoint_path, state)

    def timeout() -> None:
        if not state.get("complete"):
            update("hard_timeout")
            os._exit(124)

    alarm = threading.Timer(args.hard_timeout_seconds, timeout)
    alarm.daemon = True
    alarm.start()
    try:
        raw = json.loads(input_path.read_text(encoding="utf-8"))
        update("input_loaded")

        w = after(inverse(T_PERM), S_PERM)
        x = ppow(w, 2)
        sigma_2_perm = after(S_PERM, ppow(T_PERM, 2))
        y = ppow(sigma_2_perm, 2)
        heart_x = alternate_heart(x)
        heart_y = alternate_heart(y)
        rho_x = signed_blocks(heart_x, (1, 0))
        rho_y = signed_blocks(heart_y, (0, 1))
        theta = block_transport(
            alternate_heart(S_PERM), (1, 0, 2)
        )
        tau = block_transport(
            alternate_heart(T_PERM), (2, 0, 1)
        )
        tau2 = multiply(tau, tau)
        sigma_1 = multiply(tau2, theta)
        sigma_2 = multiply(theta, tau2)
        marked_x = multiply(sigma_1, sigma_1)
        marked_y = multiply(sigma_2, sigma_2)
        own = {
            "theta_order_two": equal(multiply(theta, theta), eye(21)),
            "tau_order_three": equal(multiply(tau2, tau), eye(21)),
            "Delta_reconstructed": equal(
                multiply(multiply(sigma_1, sigma_2), sigma_1), theta
            ),
            "delta_reconstructed": equal(multiply(sigma_1, sigma_2), tau),
            "braid_relation": equal(
                multiply(multiply(sigma_1, sigma_2), sigma_1),
                multiply(multiply(sigma_2, sigma_1), sigma_2),
            ),
            "sigma_1_squared_matches_frozen_rho_X": equal(marked_x, rho_x),
            "sigma_2_squared_matches_frozen_rho_Y": equal(marked_y, rho_y),
            "marked_projection_matches_frozen_C2_W_action": equal(
                marked_x, rho_x
            )
            and equal(marked_y, rho_y),
            "rank_difference_x": rank_mod3(subtract(marked_x, rho_x)),
            "rank_difference_y": rank_mod3(subtract(marked_y, rho_y)),
        }
        update("alternate_basis_reconstruction")

        repairs = enumerate_scalar_factors()
        corrected_theta = block_transport(
            alternate_heart(S_PERM), (1, 0, 2), (1, 1, 1)
        )
        corrected_tau = block_transport(
            alternate_heart(T_PERM), (2, 0, 1), (1, 2, 2)
        )
        corrected_tau2 = multiply(corrected_tau, corrected_tau)
        corrected_sigma_1 = multiply(corrected_tau2, corrected_theta)
        corrected_sigma_2 = multiply(corrected_theta, corrected_tau2)
        repair_diagnostic = {
            "candidate_count": len(repairs),
            "candidate_list": repairs,
            "lexicographically_first_recovers_x": equal(
                multiply(corrected_sigma_1, corrected_sigma_1), rho_x
            ),
            "lexicographically_first_recovers_y": equal(
                multiply(corrected_sigma_2, corrected_sigma_2), rho_y
            ),
            "repair_used_for_measurement": False,
        }

        comparisons = {
            "producer_input_sha256_current": raw["generated_by"]["script_sha256"]
            == file_sha(ROOT / raw["generated_by"]["script"]),
            "theta_order_two_equal": raw["marking"]["theta_order_two"]
            == own["theta_order_two"],
            "tau_order_three_equal": raw["marking"]["tau_order_three"]
            == own["tau_order_three"],
            "Delta_reconstruction_equal": raw["marking"]["Delta_reconstructed"]
            == own["Delta_reconstructed"],
            "delta_reconstruction_equal": raw["marking"]["delta_reconstructed"]
            == own["delta_reconstructed"],
            "braid_relation_equal": raw["marking"]["braid_relation"]
            == own["braid_relation"],
            "x_anchor_boolean_equal": raw["marking"][
                "sigma_1_squared_matches_frozen_rho_X"
            ]
            == own["sigma_1_squared_matches_frozen_rho_X"],
            "y_anchor_boolean_equal": raw["marking"][
                "sigma_2_squared_matches_frozen_rho_Y"
            ]
            == own["sigma_2_squared_matches_frozen_rho_Y"],
            "x_difference_rank_equal": raw["marking"]["rank_difference_x"]
            == own["rank_difference_x"],
            "y_difference_rank_equal": raw["marking"]["rank_difference_y"]
            == own["rank_difference_y"],
            "scalar_candidate_count_equal": raw[
                "diagnostic_unfrozen_scalar_factor"
            ]["repair_candidate_count"]
            == len(repairs),
            "scalar_candidate_list_equal": raw[
                "diagnostic_unfrozen_scalar_factor"
            ]["repair_candidates"]
            == repairs,
            "stage_stopped_before_classification": raw["stage_boundary"]["stage"]
            == "stopped_before_SURJ_LIN",
            "no_rows_opened": raw["stage_boundary"]["target_rows_formed"] == 0
            and raw["stage_boundary"]["lift_table_rows"] == 0,
            "no_preregistration_created": not raw["stage_boundary"][
                "preregistration_created"
            ],
            "noncontact_all_false": not any(raw["noncontact"].values()),
        }
        if not all(comparisons.values()):
            raise RuntimeError("producer/checker equality changed")

        result = {
            "schema": "vnbit_compact_measurement_check/v2",
            "run_id": "vnbit-compact-measurement-check-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "generated_by": {
                "script": "search/check_vnbit_compact_measurement_v2.py",
                "script_sha256": file_sha(Path(__file__)),
                "runtime": f"Python {os.sys.version.split()[0]}; standard library only",
            },
            "input": {
                "path": args.input,
                "sha256": file_sha(input_path),
                "schema": raw["schema"],
            },
            "helper_disjointness": {
                "producer_imported": False,
                "P_model": "hard-coded audited permutations on 9 points",
                "heart_basis": "e_i-e_0 for i=1..7, eliminating e_8-e_0",
                "field_elimination": "independent pure-Python forward elimination",
                "scalar_enumeration": "independent 64-pair loop",
            },
            "independent_marking": own,
            "independent_repair_diagnostic": repair_diagnostic,
            "comparisons": comparisons,
            "all_equalities_true": all(comparisons.values()),
            "stage_boundary": raw["stage_boundary"],
            "scope": raw["endgame_scope"],
            "noncontact": raw["noncontact"],
        }
        replace_json(output_path, result)
        update(
            "complete",
            complete=True,
            output_sha256=file_sha(output_path),
        )
        return 0
    finally:
        alarm.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
