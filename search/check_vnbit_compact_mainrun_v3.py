#!/usr/bin/env python3
"""Helper-disjoint checker for the two-window vN-BIT main run.

The producer is never imported.  This checker uses a different basis of the
9-point augmentation heart, independently rebuilds the 324 roof rows, expands
the two full B3/N hexagons, and enumerates every affine solution (at most 81)
for every marked class and roof row.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import threading
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIELD = 3
ID9 = tuple(range(9))
S_PERM = (2, 1, 0, 8, 5, 4, 7, 6, 3)
T_PERM = (5, 7, 4, 1, 8, 6, 0, 3, 2)
CHARACTERS = ((1, 0), (0, 1), (1, 1))


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def object_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def replace_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".new")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def matrix(value: object) -> np.ndarray:
    return np.asarray(value, dtype=np.int64) % FIELD


def identity(size: int) -> np.ndarray:
    return np.eye(size, dtype=np.int64)


def product(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return (left @ right) % FIELD


def reduced_row_echelon(value: np.ndarray) -> tuple[np.ndarray, list[int]]:
    work = value.copy() % FIELD
    row = 0
    pivots: list[int] = []
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        choice = row + int(choices[0])
        work[[row, choice]] = work[[choice, row]]
        if work[row, column] == 2:
            work[row] = (2 * work[row]) % FIELD
        for other in range(work.shape[0]):
            coefficient = int(work[other, column])
            if other != row and coefficient:
                work[other] = (work[other] - coefficient * work[row]) % FIELD
        pivots.append(column)
        row += 1
        if row == work.shape[0]:
            break
    return work, pivots


def matrix_rank(value: np.ndarray) -> int:
    return len(reduced_row_echelon(value)[1])


def kernel_columns(value: np.ndarray) -> np.ndarray:
    reduced, pivots = reduced_row_echelon(value)
    free = [column for column in range(value.shape[1]) if column not in pivots]
    answer = np.zeros((value.shape[1], len(free)), dtype=np.int64)
    for output, free_column in enumerate(free):
        answer[free_column, output] = 1
        for row, pivot in enumerate(pivots):
            answer[pivot, output] = (-reduced[row, free_column]) % FIELD
    return answer


def inverse_matrix(value: np.ndarray) -> np.ndarray:
    size = value.shape[0]
    reduced, pivots = reduced_row_echelon(
        np.concatenate((value % FIELD, identity(size)), axis=1)
    )
    if pivots[:size] != list(range(size)):
        raise RuntimeError("singular action matrix")
    return reduced[:, size:] % FIELD


def matrix_power(value: np.ndarray, exponent: int) -> np.ndarray:
    if exponent < 0:
        return matrix_power(inverse_matrix(value), -exponent)
    answer = identity(value.shape[0])
    factor = value.copy()
    while exponent:
        if exponent & 1:
            answer = product(answer, factor)
        factor = product(factor, factor)
        exponent >>= 1
    return answer


def block_diagonal(blocks: list[np.ndarray]) -> np.ndarray:
    size = sum(block.shape[0] for block in blocks)
    answer = np.zeros((size, size), dtype=np.int64)
    offset = 0
    for block in blocks:
        width = block.shape[0]
        answer[offset : offset + width, offset : offset + width] = block
        offset += width
    return answer % FIELD


def after(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def inverse_permutation(value: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * len(value)
    for source, target in enumerate(value):
        answer[target] = source
    return tuple(answer)


def permutation_power(value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    if exponent < 0:
        return permutation_power(inverse_permutation(value), -exponent)
    answer = tuple(range(len(value)))
    factor = value
    while exponent:
        if exponent & 1:
            answer = after(answer, factor)
        factor = after(factor, factor)
        exponent >>= 1
    return answer


def alternate_heart(permutation: tuple[int, ...]) -> np.ndarray:
    """Basis e_i-e_0 (1 <= i <= 7), eliminating e_8-e_0."""
    answer = np.zeros((7, 7), dtype=np.int64)
    for column, point in enumerate(range(1, 8)):
        vector = np.zeros(9, dtype=np.int64)
        vector[permutation[point]] += 1
        vector[permutation[0]] -= 1
        coefficient_eight = int(vector[8])
        for row, coordinate in enumerate(range(1, 8)):
            answer[row, column] = (vector[coordinate] - coefficient_eight) % FIELD
    return answer


def coordinate_change() -> np.ndarray:
    """Producer heart coordinates -> alternate checker coordinates."""
    answer = np.zeros((7, 7), dtype=np.int64)
    for column in range(7):
        vector = np.zeros(9, dtype=np.int64)
        vector[column] += 1
        vector[8] -= 1
        coefficient_eight = int(vector[8])
        for row, coordinate in enumerate(range(1, 8)):
            answer[row, column] = (vector[coordinate] - coefficient_eight) % FIELD
    return answer


def block_transport(
    base: np.ndarray,
    destinations: tuple[int, int, int],
    scalars: tuple[int, int, int] = (1, 1, 1),
) -> np.ndarray:
    answer = np.zeros((21, 21), dtype=np.int64)
    for source, target in enumerate(destinations):
        answer[7 * target : 7 * target + 7, 7 * source : 7 * source + 7] = (
            scalars[source] * base
        ) % FIELD
    return answer


def module_action(base: np.ndarray, abelian: tuple[int, int]) -> np.ndarray:
    blocks = []
    for character in CHARACTERS:
        scalar = 2 if sum(x * y for x, y in zip(character, abelian)) % 2 else 1
        blocks.append((scalar * base) % FIELD)
    return block_diagonal(blocks)


def evaluate_word(word: list[list[Any]], x: np.ndarray, y: np.ndarray) -> np.ndarray:
    answer = identity(x.shape[0])
    for letter, exponent in word:
        generator = x if letter == "x" else y
        answer = product(answer, matrix_power(generator, int(exponent)))
    return answer


def word_abelian_parity(word: list[list[Any]]) -> tuple[int, int]:
    totals = [0, 0]
    for letter, exponent in word:
        totals[0 if letter == "x" else 1] += int(exponent)
    return totals[0] % 2, totals[1] % 2


class AffineElement:
    def __init__(self, coefficient: np.ndarray, constant: np.ndarray, action: np.ndarray):
        self.coefficient = coefficient % FIELD
        self.constant = constant % FIELD
        self.action = action % FIELD


def known_element(vector: np.ndarray, action: np.ndarray) -> AffineElement:
    return AffineElement(np.zeros((21, 21), dtype=np.int64), vector, action)


def unknown_element(action: np.ndarray) -> AffineElement:
    return AffineElement(identity(21), np.zeros(21, dtype=np.int64), action)


def affine_product(left: AffineElement, right: AffineElement) -> AffineElement:
    return AffineElement(
        left.coefficient + left.action @ right.coefficient,
        left.constant + left.action @ right.constant,
        product(left.action, right.action),
    )


def affine_inverse(value: AffineElement) -> AffineElement:
    action_inverse = inverse_matrix(value.action)
    return AffineElement(
        -action_inverse @ value.coefficient,
        -action_inverse @ value.constant,
        action_inverse,
    )


def affine_power(value: AffineElement, exponent: int) -> AffineElement:
    if exponent < 0:
        return affine_power(affine_inverse(value), -exponent)
    answer = known_element(np.zeros(21, dtype=np.int64), identity(21))
    factor = value
    while exponent:
        if exponent & 1:
            answer = affine_product(answer, factor)
        factor = affine_product(factor, factor)
        exponent >>= 1
    return answer


def marked_elements(
    representative: list[int], theta: np.ndarray, tau: np.ndarray
) -> dict[str, AffineElement]:
    vector = matrix(representative).reshape(-1)
    delta = known_element(vector[:21], theta)
    small_delta = known_element(vector[21:], tau)
    sigma_1 = affine_product(affine_inverse(small_delta), delta)
    sigma_2 = affine_product(affine_inverse(delta), affine_power(small_delta, 2))
    return {
        "Delta": delta,
        "delta": small_delta,
        "sigma_1": sigma_1,
        "sigma_2": sigma_2,
        "x": affine_power(sigma_1, 2),
        "y": affine_power(sigma_2, 2),
    }


def full_relations(
    elements: dict[str, AffineElement], roof_row: dict[str, Any]
) -> tuple[AffineElement, AffineElement, AffineElement, AffineElement]:
    f = unknown_element(roof_row["action_alt"])
    m = int(roof_row["m"])
    exponent = 2 * m + 1
    sigma_1 = elements["sigma_1"]
    sigma_2 = elements["sigma_2"]
    x = elements["x"]
    y = elements["y"]
    c = affine_power(elements["Delta"], 2)

    left_1 = affine_product(
        affine_product(
            affine_product(affine_power(sigma_1, exponent), affine_inverse(f)),
            affine_power(sigma_2, exponent),
        ),
        f,
    )
    right_1 = affine_product(
        affine_product(affine_product(affine_inverse(f), sigma_1), sigma_2),
        affine_product(affine_power(x, -m), affine_power(c, m)),
    )
    relation_1 = affine_product(left_1, affine_inverse(right_1))

    left_2 = affine_product(
        affine_product(
            affine_product(affine_inverse(f), affine_power(sigma_2, exponent)),
            f,
        ),
        affine_power(sigma_1, exponent),
    )
    right_2 = affine_product(
        affine_product(affine_product(sigma_2, sigma_1), affine_power(y, -m)),
        affine_product(affine_power(c, m), f),
    )
    relation_2 = affine_product(left_2, affine_inverse(right_2))

    generator_a = affine_power(x, exponent)
    generator_b = affine_product(
        affine_product(affine_inverse(f), affine_power(y, exponent)), f
    )
    return relation_1, relation_2, generator_a, generator_b


def solver_template(coefficients: np.ndarray) -> dict[str, Any]:
    work = coefficients.copy() % FIELD
    transform = identity(work.shape[0])
    row = 0
    pivots: list[int] = []
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        choice = row + int(choices[0])
        work[[row, choice]] = work[[choice, row]]
        transform[[row, choice]] = transform[[choice, row]]
        if work[row, column] == 2:
            work[row] = (2 * work[row]) % FIELD
            transform[row] = (2 * transform[row]) % FIELD
        for other in range(work.shape[0]):
            coefficient = int(work[other, column])
            if other != row and coefficient:
                work[other] = (work[other] - coefficient * work[row]) % FIELD
                transform[other] = (
                    transform[other] - coefficient * transform[row]
                ) % FIELD
        pivots.append(column)
        row += 1
        if row == work.shape[0]:
            break
    free = [column for column in range(work.shape[1]) if column not in pivots]
    null_basis = np.zeros((work.shape[1], len(free)), dtype=np.int64)
    for output, free_column in enumerate(free):
        null_basis[free_column, output] = 1
        for pivot_row, pivot in enumerate(pivots):
            null_basis[pivot, output] = (-work[pivot_row, free_column]) % FIELD
    return {
        "rref": work,
        "transform": transform,
        "pivots": pivots,
        "free": free,
        "null_basis": null_basis,
        "rank": len(pivots),
    }


def enumerate_solutions(template: dict[str, Any], rhs: np.ndarray) -> np.ndarray:
    transformed = (template["transform"] @ rhs) % FIELD
    rank = int(template["rank"])
    if np.any(transformed[rank:]):
        return np.zeros((0, len(template["pivots"]) + len(template["free"])), dtype=np.int64)
    particular = np.zeros(template["rref"].shape[1], dtype=np.int64)
    for row, pivot in enumerate(template["pivots"]):
        particular[pivot] = transformed[row]
    coordinates = np.asarray(
        list(itertools.product(range(FIELD), repeat=len(template["free"]))),
        dtype=np.int64,
    )
    if not len(template["free"]):
        coordinates = np.zeros((1, 0), dtype=np.int64)
    return (
        particular.reshape(1, -1) + coordinates @ template["null_basis"].T
    ) % FIELD


def build_roof_rows(
    x_alt: np.ndarray,
    y_alt: np.ndarray,
    change_21: np.ndarray,
    change_21_inverse: np.ndarray,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    s4 = json.loads((ROOT / "certificates/S4.v2.json").read_text(encoding="utf-8"))
    k3 = json.loads((ROOT / "certificates/K3.v1.json").read_text(encoding="utf-8"))
    k9 = json.loads((ROOT / "certificates/K9.v1.json").read_text(encoding="utf-8"))
    s4_rows = [entry for entry in s4["generation_detail"] if entry.get("pass")]
    k3_rows = k3["shadows"]
    reduction = k9["reduction"][0]["image"]
    rows: list[dict[str, Any]] = []
    public_rows: list[dict[str, Any]] = []
    for t2_index, first in enumerate(s4_rows):
        p_action_alt = evaluate_word(first["f_word"], x_alt, y_alt)
        for k3_index, second in enumerate(k3_rows):
            if int(first["m"]) % 3 != int(second["m"]) % 3:
                continue
            choices = [
                value
                for value in range(18)
                if value % 9 == int(first["m"]) and value % 6 == int(second["m"])
            ]
            if len(choices) != 1:
                raise RuntimeError("CRT row count changed")
            m = choices[0]
            parity = word_abelian_parity(second["f_word"])
            action_alt = module_action(p_action_alt, parity)
            action_producer = product(
                product(change_21_inverse, action_alt), change_21
            )
            preimages = sum(
                1
                for index, target in enumerate(reduction)
                if int(target) == k3_index and int(k9["shadows"][index]["m"]) == m
            )
            public = {
                "t_index": len(rows),
                "m": m,
                "t2_index": t2_index,
                "t2_m_mod9": int(first["m"]),
                "k3_index": k3_index,
                "k3_m_mod6": int(second["m"]),
                "k_mod3": int(second["kernel_cert"]["k"]) % 3,
                "K9_preimage_count": preimages,
                "fbar_action_sha256": object_digest(action_producer.tolist()),
                "s4_f_word": first["f_word"],
                "k3_f_word": second["f_word"],
                "k3_word_parity": list(parity),
            }
            rows.append({**public, "action_alt": action_alt})
            public_rows.append(public)
    if len(s4_rows) != 54 or len(k3_rows) != 12 or len(rows) != 324:
        raise RuntimeError("roof universe changed")
    if Counter(row["K9_preimage_count"] for row in rows) != Counter({3: 324}):
        raise RuntimeError("K9 fibre count changed")
    return rows, public_rows


def build_templates(
    theta: np.ndarray,
    tau: np.ndarray,
    rows: list[dict[str, Any]],
    change_21: np.ndarray,
    change_21_inverse: np.ndarray,
) -> tuple[list[dict[str, Any]], str]:
    elements = marked_elements([0] * 42, theta, tau)
    change_out_inverse = block_diagonal([change_21_inverse, change_21_inverse])
    templates = []
    producer_digest_rows = []
    for row in rows:
        first, second, generator_a, generator_b = full_relations(elements, row)
        if not np.array_equal(first.action, identity(21)) or not np.array_equal(
            second.action, identity(21)
        ):
            raise RuntimeError("roof relation action changed")
        rank_1 = matrix_rank(first.coefficient)
        rank_2 = matrix_rank(second.coefficient)
        if rank_1 != rank_2:
            raise RuntimeError("full-hexagon coefficient rank pair changed")
        combined = np.concatenate((first.coefficient, second.coefficient), axis=0)
        solver = solver_template(combined)
        producer_combined = product(
            product(change_out_inverse, combined), change_21
        )
        producer_left_null = kernel_columns(producer_combined.T).T % FIELD
        block_tests = []
        invariant_dimensions = []
        for block in range(3):
            section = slice(7 * block, 7 * block + 7)
            coboundary = np.concatenate(
                (
                    identity(7) - generator_a.action[section, section],
                    identity(7) - generator_b.action[section, section],
                ),
                axis=0,
            ) % FIELD
            invariant_dimensions.append(7 - matrix_rank(coboundary))
            block_tests.append(kernel_columns(coboundary.T).T % FIELD)
        if invariant_dimensions != [0, 0, 0]:
            raise RuntimeError("target pair block invariant changed")
        templates.append(
            {
                "A1": first.coefficient,
                "A2": second.coefficient,
                "combined": combined,
                "solver": solver,
                "producer_left_null": producer_left_null,
                "block_tests": block_tests,
                "generator_a_action": generator_a.action,
                "generator_b_action": generator_b.action,
                "generator_b_coefficient": generator_b.coefficient,
                "rank_A1": rank_1,
                "rank_A2": rank_2,
            }
        )
        producer_digest_rows.append(
            {
                "rank_A1": rank_1,
                "rank_A2": rank_2,
                "rank_A": int(solver["rank"]),
                "A_sha256": object_digest(producer_combined.tolist()),
                "left_null_sha256": object_digest(producer_left_null.tolist()),
            }
        )
    return templates, object_digest(producer_digest_rows)


def compare_field(
    mismatches: list[dict[str, Any]],
    location: str,
    field: str,
    observed: object,
    expected: object,
) -> None:
    if observed != expected and len(mismatches) < 40:
        mismatches.append(
            {
                "location": location,
                "field": field,
                "producer": observed,
                "checker": expected,
            }
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="search/certs/vnbit_compact_mainrun_raw_v3_20260813.json",
    )
    parser.add_argument(
        "--preflight",
        default="search/certs/vnbit_compact_preflight_v3_20260813.json",
    )
    parser.add_argument(
        "--output",
        default="search/certs/vnbit_compact_mainrun_check_v3_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/vnbit_compact_mainrun_check_v3_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()

    input_path = ROOT / args.input
    preflight_path = ROOT / args.preflight
    output_path = ROOT / args.output
    checkpoint_path = ROOT / args.checkpoint
    began = time.monotonic()
    state: dict[str, Any] = {
        "schema": "vnbit_compact_mainrun_check_checkpoint/v3",
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
        preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
        mismatches: list[dict[str, Any]] = []

        change = coordinate_change()
        change_inverse = inverse_matrix(change)
        change_21 = block_diagonal([change, change, change])
        change_21_inverse = block_diagonal(
            [change_inverse, change_inverse, change_inverse]
        )
        s_heart = alternate_heart(S_PERM)
        t_heart = alternate_heart(T_PERM)
        sigma_1_perm = after(inverse_permutation(T_PERM), S_PERM)
        sigma_2_perm = after(S_PERM, permutation_power(T_PERM, 2))
        x_alt = alternate_heart(permutation_power(sigma_1_perm, 2))
        y_alt = alternate_heart(permutation_power(sigma_2_perm, 2))
        rho_x_alt = module_action(x_alt, (1, 0))
        rho_y_alt = module_action(y_alt, (0, 1))

        rows, public_rows = build_roof_rows(
            x_alt, y_alt, change_21, change_21_inverse
        )
        compare_field(
            mismatches,
            "roof",
            "public_rows",
            raw["roof_targets"],
            public_rows,
        )
        update("roof_rebuilt", rows=len(rows), mismatch_count=len(mismatches))

        theta_base = block_transport(s_heart, (1, 0, 2))
        tau_base = block_transport(t_heart, (2, 0, 1))
        sign_by_eps = {"+": (2, 2, 1), "-": (1, 1, 2)}
        checked_rows = 0
        window_summaries = []

        for raw_window in raw["per_eps"]:
            eps = raw_window["eps"]
            pre_window = next(item for item in preflight["windows"] if item["eps"] == eps)
            signs = sign_by_eps[eps]
            theta = product(
                theta_base,
                block_diagonal([sign * identity(7) for sign in signs]),
            )
            tau = tau_base.copy()
            transformed_theta = product(
                product(change_21, matrix(pre_window["theta_matrix"])),
                change_21_inverse,
            )
            transformed_tau = product(
                product(change_21, matrix(pre_window["tau_matrix"])),
                change_21_inverse,
            )
            compare_field(
                mismatches,
                f"window[{eps}]",
                "theta_basis_transport",
                transformed_theta.tolist(),
                theta.tolist(),
            )
            compare_field(
                mismatches,
                f"window[{eps}]",
                "tau_basis_transport",
                transformed_tau.tolist(),
                tau.tolist(),
            )
            pure = marked_elements([0] * 42, theta, tau)
            compare_field(
                mismatches,
                f"window[{eps}]",
                "pure_x_action",
                pure["x"].action.tolist(),
                rho_x_alt.tolist(),
            )
            compare_field(
                mismatches,
                f"window[{eps}]",
                "pure_y_action",
                pure["y"].action.tolist(),
                rho_y_alt.tolist(),
            )

            templates, template_digest = build_templates(
                theta, tau, rows, change_21, change_21_inverse
            )
            compare_field(
                mismatches,
                f"window[{eps}]",
                "template_sha256",
                raw_window["template_sha256"],
                template_digest,
            )
            update(
                f"templates_{eps}",
                eps=eps,
                rows=len(templates),
                mismatch_count=len(mismatches),
            )

            image_km = Counter()
            image_nw = Counter()
            theta2_counts = Counter()
            theta2_rigid = 0
            rank_pairs = Counter(
                (item["rank_A1"], item["rank_A2"]) for item in templates
            )
            rank_combined = Counter(int(item["solver"]["rank"]) for item in templates)
            producer_classes = {
                int(entry["class_index"]): entry
                for entry in pre_window["gamma_cohomology"]["classes"]
                if entry["surjective"]
            }
            for class_position, raw_class in enumerate(raw_window["per_class"]):
                class_index = int(raw_class["class_index"])
                source_class = producer_classes[class_index]
                compare_field(
                    mismatches,
                    f"window[{eps}].class[{class_index}]",
                    "representative",
                    raw_class["representative"],
                    source_class["representative"],
                )
                producer_vector = matrix(source_class["representative"]).reshape(-1)
                alternate_vector = np.concatenate(
                    (
                        change_21 @ producer_vector[:21],
                        change_21 @ producer_vector[21:],
                    )
                ) % FIELD
                elements = marked_elements(alternate_vector.tolist(), theta, tau)
                lifted_rows: list[dict[str, Any]] = []
                for roof_row, template, raw_row in zip(
                    rows, templates, raw_class["lift_table"]
                ):
                    first, second, generator_a, generator_b = full_relations(
                        elements, roof_row
                    )
                    if not np.array_equal(first.coefficient, template["A1"]) or not np.array_equal(
                        second.coefficient, template["A2"]
                    ):
                        raise RuntimeError("class-dependent coefficient matrix")
                    if not np.array_equal(generator_b.coefficient, template["generator_b_coefficient"]):
                        raise RuntimeError("class-dependent generator coefficient")
                    rhs = (-np.concatenate((first.constant, second.constant))) % FIELD
                    solutions = enumerate_solutions(template["solver"], rhs)
                    solution_count = int(solutions.shape[0])

                    rhs_producer = product(
                        block_diagonal([change_21_inverse, change_21_inverse]),
                        rhs.reshape(-1, 1),
                    ).reshape(-1)
                    obstruction = (
                        template["producer_left_null"] @ rhs_producer
                    ) % FIELD
                    obstruction_zero = not np.any(obstruction)

                    bad_masks = np.zeros(solution_count, dtype=np.int64)
                    for block in range(3):
                        section = slice(7 * block, 7 * block + 7)
                        first_rhs = np.repeat(
                            generator_a.constant[section].reshape(1, 7),
                            solution_count,
                            axis=0,
                        )
                        second_rhs = (
                            solutions @ generator_b.coefficient[section, :].T
                            + generator_b.constant[section].reshape(1, 7)
                        ) % FIELD
                        test_rhs = np.concatenate((first_rhs, second_rhs), axis=1)
                        residual = (
                            test_rhs @ template["block_tests"][block].T
                        ) % FIELD
                        is_bad = ~np.any(residual, axis=1)
                        bad_masks[is_bad] |= 1 << block
                    bad_counts = {
                        str(mask): int(np.sum((bad_masks & mask) == mask))
                        for mask in range(1, 8)
                    }
                    generating_count = int(np.sum(bad_masks == 0))
                    lifts = bool(obstruction_zero and generating_count > 0)
                    expected_fields = {
                        "t_index": int(roof_row["t_index"]),
                        "rank_A1": int(template["rank_A1"]),
                        "rank_A2": int(template["rank_A2"]),
                        "rank_A1_equals_rank_A2": template["rank_A1"]
                        == template["rank_A2"],
                        "rank_A": int(template["solver"]["rank"]),
                        "dim_ker_A": 21 - int(template["solver"]["rank"]),
                        "obstruction_coordinates": [int(x) for x in obstruction],
                        "obstruction_zero": obstruction_zero,
                        "solution_count": solution_count,
                        "bad_solution_counts_by_block_subset": bad_counts,
                        "generating_solution_count": generating_count,
                        "generating_solution_exists": generating_count > 0,
                        "lifts": lifts,
                    }
                    for field, expected in expected_fields.items():
                        compare_field(
                            mismatches,
                            f"window[{eps}].class[{class_index}].row[{roof_row['t_index']}]",
                            field,
                            raw_row[field],
                            expected,
                        )
                    if lifts:
                        lifted_rows.append(roof_row)
                    checked_rows += 1

                per_t2 = []
                for t2_index in range(54):
                    values = sorted(
                        {
                            int(row["k_mod3"])
                            for row in lifted_rows
                            if int(row["t2_index"]) == t2_index
                        }
                    )
                    per_t2.append(
                        {
                            "t2_index": t2_index,
                            "k_values_realized": values,
                            "count": len(values),
                            "lifted_NW_rows": sum(
                                1
                                for row in lifted_rows
                                if int(row["t2_index"]) == t2_index
                            ),
                        }
                    )
                expected_theta2 = {
                    "per_t2": per_t2,
                    "count_distribution": {
                        str(key): value
                        for key, value in Counter(
                            item["count"] for item in per_t2
                        ).items()
                    },
                    "rigid": all(item["count"] == 1 for item in per_t2),
                }
                compare_field(
                    mismatches,
                    f"window[{eps}].class[{class_index}]",
                    "theta2",
                    raw_class["theta2"],
                    expected_theta2,
                )
                expected_nw = len(lifted_rows)
                expected_km = sum(int(row["K9_preimage_count"]) for row in lifted_rows)
                compare_field(
                    mismatches,
                    f"window[{eps}].class[{class_index}]",
                    "Im_R_N_E_N_W_size",
                    raw_class["Im_R_N_E_N_W_size"],
                    expected_nw,
                )
                compare_field(
                    mismatches,
                    f"window[{eps}].class[{class_index}]",
                    "Im_R_K_M_size",
                    raw_class["Im_R_K_M_size"],
                    expected_km,
                )
                image_nw[expected_nw] += 1
                image_km[expected_km] += 1
                theta2_counts.update(item["count"] for item in per_t2)
                theta2_rigid += int(expected_theta2["rigid"])
                if (class_position + 1) % 5 == 0 or class_position + 1 == len(
                    raw_window["per_class"]
                ):
                    update(
                        f"check_{eps}",
                        eps=eps,
                        classes_complete=class_position + 1,
                        classes_total=len(raw_window["per_class"]),
                        checked_rows=checked_rows,
                        mismatch_count=len(mismatches),
                    )

            expected_window_summary = {
                "Im_R_K_M_distribution": {
                    str(key): value for key, value in sorted(image_km.items())
                },
                "Im_R_N_E_N_W_distribution": {
                    str(key): value for key, value in sorted(image_nw.items())
                },
                "theta2_rigid_class_count": theta2_rigid,
                "theta2_count_distribution_across_classes_and_t2": {
                    str(key): value for key, value in sorted(theta2_counts.items())
                },
                "rank_A1_A2_distribution": {
                    f"{left},{right}": count
                    for (left, right), count in sorted(rank_pairs.items())
                },
                "rank_A_distribution": {
                    str(key): value for key, value in sorted(rank_combined.items())
                },
            }
            for field, expected in expected_window_summary.items():
                compare_field(
                    mismatches,
                    f"window[{eps}]",
                    field,
                    raw_window[field],
                    expected,
                )
            window_summaries.append(
                {
                    "eps": eps,
                    "classes": len(raw_window["per_class"]),
                    "rows": len(raw_window["per_class"]) * 324,
                    **expected_window_summary,
                    "template_sha256": template_digest,
                }
            )

        result = {
            "schema": "vnbit_compact_mainrun_check/v3",
            "run_id": "vnbit-compact-mainrun-check-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "checker": {
                "script": "search/check_vnbit_compact_mainrun_v3.py",
                "script_sha256": file_digest(Path(__file__)),
                "method": (
                    "alternate augmentation-heart basis; independent roof rebuild; "
                    "full (3.3)/(3.4) expansion; exhaustive affine-kernel enumeration"
                ),
                "imports_producer": False,
            },
            "inputs": {
                args.input: file_digest(input_path),
                args.preflight: file_digest(preflight_path),
                "certificates/S4.v2.json": file_digest(ROOT / "certificates/S4.v2.json"),
                "certificates/K3.v1.json": file_digest(ROOT / "certificates/K3.v1.json"),
                "certificates/K9.v1.json": file_digest(ROOT / "certificates/K9.v1.json"),
            },
            "basis": {
                "checker": "e_i-e_0 (1<=i<=7), eliminate e_8-e_0",
                "producer_to_checker_sha256": object_digest(change.tolist()),
                "dimension": 7,
            },
            "roof_rows": len(rows),
            "checked_lift_rows": checked_rows,
            "window_summaries": window_summaries,
            "mismatch_count": len(mismatches),
            "mismatch_examples": mismatches,
            "noncontact": {
                "u": False,
                "c": False,
                "sealed_three_quantities": False,
                "sealed_K5": False,
            },
            "status_note": "independent machine comparison; no type adjudication",
        }
        replace_json(output_path, result)
        update(
            "complete",
            complete=True,
            checked_rows=checked_rows,
            mismatch_count=len(mismatches),
            output_sha256=file_digest(output_path),
        )
        return 0 if not mismatches else 1
    except BaseException as error:
        update("exception", error_type=type(error).__name__, error_message=str(error))
        raise
    finally:
        alarm.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
