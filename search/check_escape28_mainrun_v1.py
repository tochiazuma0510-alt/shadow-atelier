#!/usr/bin/env python3
"""Independent checker for the task-133 ESCAPE-28 campaign.

The task producer is never imported.  This lane reuses only the older task-132
checker primitives, works in the alternate heart basis e_i-e_0, rebuilds the
roof from the three frozen certificate files, transports obstruction
coordinates back to the producer basis, and re-evaluates every component and
every full Cartesian row.
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

import check_vnbit_compact_mainrun_v3 as alt


ROOT = Path(__file__).resolve().parents[1]
FIELD = 3
BLOCK = 7


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def object_digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def replace_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".new")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def counter_json(value: Counter) -> dict[str, int]:
    return {str(key): int(count) for key, count in sorted(value.items())}


def compare(
    mismatches: list[dict[str, Any]],
    location: str,
    field: str,
    producer: object,
    checker: object,
) -> None:
    if producer != checker and len(mismatches) < 50:
        mismatches.append(
            {
                "location": location,
                "field": field,
                "producer": producer,
                "checker": checker,
            }
        )


def gf2_rank(value: np.ndarray) -> int:
    work = np.asarray(value, dtype=np.uint8).copy() % 2
    row = 0
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        choice = row + int(choices[0])
        work[[row, choice]] = work[[choice, row]]
        for other in range(work.shape[0]):
            if other != row and work[other, column]:
                work[other] ^= work[row]
        row += 1
        if row == work.shape[0]:
            break
    return row


def small_permutation_matrix(destinations: tuple[int, ...]) -> np.ndarray:
    answer = np.zeros((len(destinations), len(destinations)), dtype=np.uint8)
    for source, target in enumerate(destinations):
        answer[target, source] = 1
    return answer


def twist_classifier() -> dict[str, Any]:
    s = small_permutation_matrix((1, 0, 2, 3))
    t = small_permutation_matrix((2, 0, 1, 3))
    identity = np.eye(4, dtype=np.uint8)
    zero = np.zeros((4, 8), dtype=np.uint8)
    variables = []
    for which in range(2):
        expression = zero.copy()
        expression[:, 4 * which : 4 * which + 4] = identity
        variables.append(expression)
    key = lambda matrix: tuple(int(value) for value in matrix.flatten())
    group = [identity]
    data = {key(identity): (identity, zero)}
    constraints = []
    for element in group:
        action, expression = data[key(element)]
        for generator, variable in ((s, variables[0]), (t, variables[1])):
            new_action = (action @ generator) % 2
            new_expression = (expression + action @ variable) % 2
            new_key = key(new_action)
            if new_key in data:
                constraints.append((new_expression - data[new_key][1]) % 2)
            else:
                data[new_key] = (new_action, new_expression)
                group.append(new_action)
    relation = np.concatenate(constraints, axis=0)
    z_dimension = 8 - gf2_rank(relation)
    coboundary = np.concatenate((identity - s, identity - t), axis=0) % 2
    b_dimension = gf2_rank(coboundary)
    return {
        "coefficient_module": "F_2^4 (three-point orbit plus one fixed point)",
        "S3_order": len(group),
        "Z1_dimension": z_dimension,
        "B1_dimension": b_dimension,
        "H1_dimension": z_dimension - b_dimension,
        "H1_order": 2 ** (z_dimension - b_dimension),
        "collision_relation_rank": gf2_rank(relation),
        "relation_sha256": object_digest(relation.tolist()),
    }


def cyclic_span_dimension(seed: np.ndarray, generators: tuple[np.ndarray, ...]) -> int:
    columns = np.zeros((len(seed), 0), dtype=np.int64)
    queue = [seed]
    while queue:
        vector = queue.pop()
        trial = np.concatenate((columns, vector.reshape(-1, 1)), axis=1)
        if alt.matrix_rank(trial) == columns.shape[1]:
            continue
        columns = trial
        for generator in generators:
            queue.append((generator @ vector) % FIELD)
    return columns.shape[1]


def hom_dimension(
    left_actions: tuple[np.ndarray, np.ndarray],
    right_actions: tuple[np.ndarray, np.ndarray],
) -> int:
    equations = []
    for left, right in zip(left_actions, right_actions):
        for row in range(BLOCK):
            for column in range(BLOCK):
                equation = np.zeros(BLOCK * BLOCK, dtype=np.int64)
                for middle in range(BLOCK):
                    equation[BLOCK * row + middle] += right[middle, column]
                    equation[BLOCK * middle + column] -= left[row, middle]
                equations.append(equation % FIELD)
    return BLOCK * BLOCK - alt.matrix_rank(np.asarray(equations, dtype=np.int64))


def centralizer_dimension(generators: tuple[np.ndarray, ...]) -> int:
    equations = []
    for generator in generators:
        for row in range(BLOCK):
            for column in range(BLOCK):
                equation = np.zeros(BLOCK * BLOCK, dtype=np.int64)
                for middle in range(BLOCK):
                    equation[BLOCK * row + middle] += generator[middle, column]
                    equation[BLOCK * middle + column] -= generator[row, middle]
                equations.append(equation % FIELD)
    return BLOCK * BLOCK - alt.matrix_rank(np.asarray(equations, dtype=np.int64))


def jordan_block(size: int) -> np.ndarray:
    answer = alt.identity(size)
    for index in range(size - 1):
        answer[index, index + 1] = 1
    return answer % FIELD


def jordan_partition(value: np.ndarray) -> list[int]:
    nilpotent = (value - alt.identity(value.shape[0])) % FIELD
    rank_one = alt.matrix_rank(nilpotent)
    rank_two = alt.matrix_rank(alt.product(nilpotent, nilpotent))
    threes = rank_two
    twos = rank_one - 2 * threes
    ones = value.shape[0] - 3 * threes - 2 * twos
    return sorted([3] * threes + [2] * twos + [1] * ones, reverse=True)


def h2_audit(value: np.ndarray) -> dict[str, Any]:
    identity = alt.identity(value.shape[0])
    norm = (identity + value + alt.product(value, value)) % FIELD
    fixed = value.shape[0] - alt.matrix_rank((value - identity) % FIELD)
    norm_rank = alt.matrix_rank(norm)
    if np.any(((value - identity) @ norm) % FIELD):
        raise RuntimeError("checker C3 norm image is not fixed")
    return {
        "dimension": value.shape[0],
        "jordan_partition": jordan_partition(value),
        "fixed_dimension": fixed,
        "norm_rank": norm_rank,
        "norm_kernel_dimension": value.shape[0] - norm_rank,
        "H2_dimension": fixed - norm_rank,
    }


def all_jordan_types() -> list[dict[str, Any]]:
    partitions = (
        (3, 3, 1),
        (3, 2, 2),
        (3, 2, 1, 1),
        (3, 1, 1, 1, 1),
        (2, 2, 2, 1),
        (2, 2, 1, 1, 1),
        (2, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1),
    )
    result = []
    for partition in partitions:
        value = alt.block_diagonal([jordan_block(size) for size in partition])
        entry = h2_audit(value)
        entry["partition"] = list(partition)
        result.append(entry)
    return result


def extend_columns(base: np.ndarray, candidates: np.ndarray) -> np.ndarray:
    answer = base.copy()
    current = alt.matrix_rank(answer) if answer.shape[1] else 0
    for column in range(candidates.shape[1]):
        trial = np.concatenate((answer, candidates[:, column : column + 1]), axis=1)
        new_rank = alt.matrix_rank(trial)
        if new_rank > current:
            answer = trial
            current = new_rank
    return answer


def solve_columns(base: np.ndarray, vector: np.ndarray) -> np.ndarray:
    augmented = np.concatenate((base, vector.reshape(-1, 1)), axis=1)
    reduced, pivots = alt.reduced_row_echelon(augmented)
    width = base.shape[1]
    for row in range(reduced.shape[0]):
        if not np.any(reduced[row, :width]) and reduced[row, width]:
            raise RuntimeError("class representative is outside cocycle span")
    answer = np.zeros(width, dtype=np.int64)
    for row, pivot in enumerate(pivots):
        if pivot < width:
            answer[pivot] = reduced[row, width]
    return answer


def cayley_cocycle_graph(
    x_perm: tuple[int, ...],
    y_perm: tuple[int, ...],
    rho_x: np.ndarray,
    rho_y: np.ndarray,
) -> dict[str, Any]:
    dimension = rho_x.shape[0]
    identity_perm = tuple(range(len(x_perm)))
    zero = np.zeros((dimension, 2 * dimension), dtype=np.int64)
    generator_expressions = []
    for which in range(2):
        expression = zero.copy()
        expression[:, which * dimension : (which + 1) * dimension] = alt.identity(dimension)
        generator_expressions.append(expression)
    elements = [identity_perm]
    data: dict[tuple[int, ...], tuple[np.ndarray, np.ndarray]] = {
        identity_perm: (alt.identity(dimension), zero)
    }
    constraints = []
    collisions = 0
    for old_element in elements:
        old_action, old_expression = data[old_element]
        for generator, action, expression in (
            (x_perm, rho_x, generator_expressions[0]),
            (y_perm, rho_y, generator_expressions[1]),
        ):
            new_element = alt.after(old_element, generator)
            new_action = alt.product(old_action, action)
            new_expression = (old_expression + old_action @ expression) % FIELD
            if new_element in data:
                constraints.append((new_expression - data[new_element][1]) % FIELD)
                collisions += 1
            else:
                data[new_element] = (new_action, new_expression)
                elements.append(new_element)
    relation = np.concatenate(constraints, axis=0)
    reduced, _ = alt.reduced_row_echelon(relation)
    canonical = reduced[np.any(reduced, axis=1)]
    return {
        "elements": elements,
        "data": data,
        "constraints": relation,
        "relation_rank": alt.matrix_rank(relation),
        "relation_rref_sha256": object_digest(canonical.tolist()),
        "positive_edges": 2 * len(elements),
        "collision_edges": collisions,
    }


def quotient_action(
    graph: dict[str, Any],
    x_perm: tuple[int, ...],
    y_perm: tuple[int, ...],
    q_perm: tuple[int, ...],
    q_matrix: np.ndarray,
    full_basis: np.ndarray,
    h_basis: np.ndarray,
    b_dimension: int,
) -> np.ndarray:
    inverse_q = alt.inverse_permutation(q_perm)
    x_conjugate = alt.after(inverse_q, alt.after(x_perm, q_perm))
    y_conjugate = alt.after(inverse_q, alt.after(y_perm, q_perm))
    action = np.concatenate(
        (
            q_matrix @ graph["data"][x_conjugate][1],
            q_matrix @ graph["data"][y_conjugate][1],
        ),
        axis=0,
    ) % FIELD
    columns = []
    for column in range(h_basis.shape[1]):
        transformed = (action @ h_basis[:, column]) % FIELD
        coordinates = solve_columns(full_basis, transformed)
        columns.append(coordinates[b_dimension:])
    return np.asarray(columns, dtype=np.int64).T % FIELD


class SymAff:
    def __init__(
        self,
        f_coefficient: np.ndarray,
        z_coefficient: np.ndarray,
        constant: np.ndarray,
        action: np.ndarray,
    ):
        self.f_coefficient = f_coefficient % FIELD
        self.z_coefficient = z_coefficient % FIELD
        self.constant = constant % FIELD
        self.action = action % FIELD


def known_symbol(dimension: int, action: np.ndarray) -> SymAff:
    return SymAff(
        np.zeros((dimension, dimension), dtype=np.int64),
        np.zeros((dimension, 2 * dimension), dtype=np.int64),
        np.zeros(dimension, dtype=np.int64),
        action,
    )


def cocycle_symbol(dimension: int, half: int, action: np.ndarray) -> SymAff:
    coefficient = np.zeros((dimension, 2 * dimension), dtype=np.int64)
    coefficient[:, half * dimension : (half + 1) * dimension] = alt.identity(dimension)
    return SymAff(
        np.zeros((dimension, dimension), dtype=np.int64),
        coefficient,
        np.zeros(dimension, dtype=np.int64),
        action,
    )


def unknown_symbol(action: np.ndarray) -> SymAff:
    dimension = action.shape[0]
    return SymAff(
        alt.identity(dimension),
        np.zeros((dimension, 2 * dimension), dtype=np.int64),
        np.zeros(dimension, dtype=np.int64),
        action,
    )


def symbol_product(left: SymAff, right: SymAff) -> SymAff:
    return SymAff(
        left.f_coefficient + left.action @ right.f_coefficient,
        left.z_coefficient + left.action @ right.z_coefficient,
        left.constant + left.action @ right.constant,
        alt.product(left.action, right.action),
    )


def symbol_inverse(value: SymAff) -> SymAff:
    inverse = alt.inverse_matrix(value.action)
    return SymAff(
        -inverse @ value.f_coefficient,
        -inverse @ value.z_coefficient,
        -inverse @ value.constant,
        inverse,
    )


def symbol_power(value: SymAff, exponent: int) -> SymAff:
    if exponent < 0:
        return symbol_power(symbol_inverse(value), -exponent)
    answer = known_symbol(value.action.shape[0], alt.identity(value.action.shape[0]))
    factor = value
    while exponent:
        if exponent & 1:
            answer = symbol_product(answer, factor)
        factor = symbol_product(factor, factor)
        exponent >>= 1
    return answer


def marked_symbols(theta: np.ndarray, tau: np.ndarray) -> dict[str, SymAff]:
    dimension = theta.shape[0]
    delta = cocycle_symbol(dimension, 0, theta)
    small_delta = cocycle_symbol(dimension, 1, tau)
    sigma_1 = symbol_product(symbol_inverse(small_delta), delta)
    sigma_2 = symbol_product(symbol_inverse(delta), symbol_power(small_delta, 2))
    return {
        "Delta": delta,
        "sigma_1": sigma_1,
        "sigma_2": sigma_2,
        "x": symbol_power(sigma_1, 2),
        "y": symbol_power(sigma_2, 2),
    }


def full_relations(
    elements: dict[str, SymAff], action: np.ndarray, m_value: int
) -> tuple[SymAff, SymAff, SymAff, SymAff]:
    f = unknown_symbol(action)
    exponent = 2 * m_value + 1
    sigma_1 = elements["sigma_1"]
    sigma_2 = elements["sigma_2"]
    x = elements["x"]
    y = elements["y"]
    c = symbol_power(elements["Delta"], 2)
    left_1 = symbol_product(
        symbol_product(
            symbol_product(symbol_power(sigma_1, exponent), symbol_inverse(f)),
            symbol_power(sigma_2, exponent),
        ),
        f,
    )
    right_1 = symbol_product(
        symbol_product(symbol_product(symbol_inverse(f), sigma_1), sigma_2),
        symbol_product(symbol_power(x, -m_value), symbol_power(c, m_value)),
    )
    relation_1 = symbol_product(left_1, symbol_inverse(right_1))
    left_2 = symbol_product(
        symbol_product(
            symbol_product(symbol_inverse(f), symbol_power(sigma_2, exponent)), f
        ),
        symbol_power(sigma_1, exponent),
    )
    right_2 = symbol_product(
        symbol_product(
            symbol_product(sigma_2, sigma_1), symbol_power(y, -m_value)
        ),
        symbol_product(symbol_power(c, m_value), f),
    )
    relation_2 = symbol_product(left_2, symbol_inverse(right_2))
    generator_a = symbol_power(x, exponent)
    generator_b = symbol_product(
        symbol_product(symbol_inverse(f), symbol_power(y, exponent)), f
    )
    return relation_1, relation_2, generator_a, generator_b


def system_template(matrix: np.ndarray) -> dict[str, Any]:
    left_null = alt.kernel_columns(matrix.T).T % FIELD
    return {
        "matrix": matrix % FIELD,
        "rank": alt.matrix_rank(matrix),
        "left_null": left_null,
        "left_null_sha256": object_digest(left_null.tolist()),
        "variable_count": matrix.shape[1],
    }


def system_count(template: dict[str, Any], rhs: np.ndarray) -> int:
    if np.any((template["left_null"] @ rhs) % FIELD):
        return 0
    return FIELD ** (int(template["variable_count"]) - int(template["rank"]))


def build_roof(
    x_alt: np.ndarray,
    y_alt: np.ndarray,
    change_orbit: np.ndarray,
    change_orbit_inverse: np.ndarray,
    change_trivial: np.ndarray,
    change_trivial_inverse: np.ndarray,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    s4 = json.loads((ROOT / "certificates/S4.v2.json").read_text(encoding="utf-8"))
    k3 = json.loads((ROOT / "certificates/K3.v1.json").read_text(encoding="utf-8"))
    k9 = json.loads((ROOT / "certificates/K9.v1.json").read_text(encoding="utf-8"))
    s4_rows = [entry for entry in s4["generation_detail"] if entry.get("pass")]
    k3_rows = k3["shadows"]
    reduction = k9["reduction"][0]["image"]
    rows = []
    public = []
    for t2_index, first in enumerate(s4_rows):
        p_action = alt.evaluate_word(first["f_word"], x_alt, y_alt)
        for k3_index, second in enumerate(k3_rows):
            if int(first["m"]) % 3 != int(second["m"]) % 3:
                continue
            choices = [
                value
                for value in range(18)
                if value % 9 == int(first["m"]) and value % 6 == int(second["m"])
            ]
            if len(choices) != 1:
                raise RuntimeError("checker CRT row is not unique")
            m_value = choices[0]
            parity = alt.word_abelian_parity(second["f_word"])
            orbit_action = alt.module_action(p_action, parity)
            trivial_action = p_action
            full_action = alt.block_diagonal([orbit_action, trivial_action])
            orbit_producer = change_orbit_inverse @ orbit_action @ change_orbit % FIELD
            trivial_producer = (
                change_trivial_inverse @ trivial_action @ change_trivial % FIELD
            )
            full_change = alt.block_diagonal([change_orbit, change_trivial])
            full_change_inverse = alt.block_diagonal(
                [change_orbit_inverse, change_trivial_inverse]
            )
            full_producer = full_change_inverse @ full_action @ full_change % FIELD
            preimages = sum(
                1
                for index, target in enumerate(reduction)
                if int(target) == k3_index
                and int(k9["shadows"][index]["m"]) == m_value
            )
            entry = {
                "t_index": len(rows),
                "m": m_value,
                "t2_index": t2_index,
                "t2_m_mod9": int(first["m"]),
                "k3_index": k3_index,
                "k3_m_mod6": int(second["m"]),
                "k_mod3": int(second["kernel_cert"]["k"]) % 3,
                "K9_preimage_count": preimages,
                "s4_f_word": first["f_word"],
                "k3_f_word": second["f_word"],
                "k3_word_parity": list(parity),
                "orbit_action": orbit_action,
                "trivial_action": trivial_action,
                "full_action": full_action,
            }
            rows.append(entry)
            public.append(
                {
                    "t_index": entry["t_index"],
                    "m": m_value,
                    "t2_index": t2_index,
                    "t2_m_mod9": int(first["m"]),
                    "k3_index": k3_index,
                    "k3_m_mod6": int(second["m"]),
                    "k_mod3": entry["k_mod3"],
                    "K9_preimage_count": preimages,
                    "fbar_action_sha256": object_digest(orbit_producer.tolist()),
                    "s4_f_word": first["f_word"],
                    "k3_f_word": second["f_word"],
                    "k3_word_parity": list(parity),
                    "orbit_action_sha256": object_digest(orbit_producer.tolist()),
                    "trivial_action_sha256": object_digest(trivial_producer.tolist()),
                    "full_action_sha256": object_digest(full_producer.tolist()),
                }
            )
    if len(rows) != 324 or Counter(row["K9_preimage_count"] for row in rows) != Counter({3: 324}):
        raise RuntimeError("checker roof universe changed")
    return rows, public


def gauge_census(
    theta_base: np.ndarray,
    tau_base: np.ndarray,
    rho_x: np.ndarray,
    rho_y: np.ndarray,
) -> dict[str, Any]:
    candidates = []
    for theta_signs in itertools.product((1, 2), repeat=4):
        theta = alt.product(
            theta_base,
            alt.block_diagonal([sign * alt.identity(BLOCK) for sign in theta_signs]),
        )
        for tau_signs in itertools.product((1, 2), repeat=4):
            tau = alt.product(
                tau_base,
                alt.block_diagonal([sign * alt.identity(BLOCK) for sign in tau_signs]),
            )
            if not np.array_equal(alt.product(theta, theta), alt.identity(28)):
                continue
            if not np.array_equal(alt.matrix_power(tau, 3), alt.identity(28)):
                continue
            sigma_1 = alt.product(alt.matrix_power(tau, 2), theta)
            sigma_2 = alt.product(theta, alt.matrix_power(tau, 2))
            if np.array_equal(alt.product(sigma_1, sigma_1), rho_x) and np.array_equal(
                alt.product(sigma_2, sigma_2), rho_y
            ):
                candidates.append((theta_signs, tau_signs, theta, tau))
    keys = {
        (tuple(theta.flatten()), tuple(tau.flatten())): index
        for index, (_, _, theta, tau) in enumerate(candidates)
    }
    orbits = set()
    stabilizers = []
    for _, _, theta, tau in candidates:
        orbit = set()
        stabilizer = 0
        for signs in itertools.product((1, 2), repeat=4):
            diagonal = alt.block_diagonal(
                [sign * alt.identity(BLOCK) for sign in signs]
            )
            transformed_theta = alt.product(alt.product(diagonal, theta), diagonal)
            transformed_tau = alt.product(alt.product(diagonal, tau), diagonal)
            orbit.add(
                keys[
                    (
                        tuple(transformed_theta.flatten()),
                        tuple(transformed_tau.flatten()),
                    )
                ]
            )
            stabilizer += int(
                np.array_equal(transformed_theta, theta)
                and np.array_equal(transformed_tau, tau)
            )
        orbits.add(tuple(sorted(orbit)))
        stabilizers.append(stabilizer)
    return {
        "End_W_V": "F_3^4",
        "End_W_V_dimension": 4,
        "gauge_group_order": 16,
        "conjugation_kernel_order": 4,
        "effective_gauge_order": 4,
        "anchor_solutions": len(candidates),
        "orbit_count": len(orbits),
        "orbit_sizes": sorted(len(orbit) for orbit in orbits),
        "full_gauge_stabilizer_sizes": sorted(set(stabilizers)),
        "twist_classifier": twist_classifier(),
        "candidate_signs": [
            {
                "theta_source_signs": [1 if value == 1 else -1 for value in theta_signs],
                "tau_source_signs": [1 if value == 1 else -1 for value in tau_signs],
            }
            for theta_signs, tau_signs, _, _ in candidates
        ],
        "orbits": [list(orbit) for orbit in sorted(orbits)],
    }


def verify_component_cohomology(
    producer: dict[str, Any],
    theta: np.ndarray,
    tau: np.ndarray,
    x_perm: tuple[int, ...],
    y_perm: tuple[int, ...],
    p_x: np.ndarray,
    p_y: np.ndarray,
    change: np.ndarray,
    mismatches: list[dict[str, Any]],
    location: str,
) -> dict[str, Any]:
    dimension = theta.shape[0]
    condition = np.zeros((2 * dimension, 2 * dimension), dtype=np.int64)
    condition[:dimension, :dimension] = (alt.identity(dimension) + theta) % FIELD
    condition[dimension:, dimension:] = (
        alt.identity(dimension) + tau + alt.product(tau, tau)
    ) % FIELD
    z_basis = alt.kernel_columns(condition)
    coboundaries = np.concatenate(
        (alt.identity(dimension) - theta, alt.identity(dimension) - tau), axis=0
    ) % FIELD
    b_basis = coboundaries[:, alt.reduced_row_echelon(coboundaries)[1]]
    full_basis = extend_columns(b_basis, z_basis)
    h_basis = full_basis[:, b_basis.shape[1] :]
    graph = cayley_cocycle_graph(x_perm, y_perm, p_x, p_y)
    s_symbols = marked_symbols(theta, tau)
    change_twice = alt.block_diagonal([change, change])
    quotient_signatures = set()
    descends_count = 0
    for entry in producer["classes"]:
        producer_vector = alt.matrix(entry["representative"]).reshape(-1)
        vector = change_twice @ producer_vector % FIELD
        compare(
            mismatches,
            location + f".class[{entry['class_index']}]",
            "cocycle_condition",
            True,
            not np.any(condition @ vector % FIELD),
        )
        coordinates = solve_columns(full_basis, vector)
        quotient_signatures.add(tuple(int(value) for value in coordinates[b_basis.shape[1] :]))
        x_value = s_symbols["x"].z_coefficient @ vector % FIELD
        y_value = s_symbols["y"].z_coefficient @ vector % FIELD
        descends = not np.any(graph["constraints"] @ np.concatenate((x_value, y_value)) % FIELD)
        compare(
            mismatches,
            location + f".class[{entry['class_index']}]",
            "descends_to_barW",
            entry["descends_to_barW"],
            bool(descends),
        )
        compare(
            mismatches,
            location + f".class[{entry['class_index']}]",
            "surjective_component",
            entry["surjective_component"],
            not bool(descends),
        )
        descends_count += int(descends)

    theta_action = quotient_action(
        graph,
        x_perm,
        y_perm,
        alt.S_PERM,
        theta,
        full_basis=extend_columns(
            np.concatenate((alt.identity(dimension) - p_x, alt.identity(dimension) - p_y), axis=0)[:,
                           alt.reduced_row_echelon(np.concatenate((alt.identity(dimension) - p_x, alt.identity(dimension) - p_y), axis=0))[1]],
            alt.kernel_columns(graph["constraints"]),
        ),
        h_basis=np.zeros((2 * dimension, 0), dtype=np.int64),
        b_dimension=0,
    ) if False else None
    # Rebuild the LHS H1(P,V) quotient separately; the disabled expression
    # above documents that the Gamma quotient basis is not used here.
    p_z = alt.kernel_columns(graph["constraints"])
    p_coboundaries = np.concatenate(
        (alt.identity(dimension) - p_x, alt.identity(dimension) - p_y), axis=0
    ) % FIELD
    p_b = p_coboundaries[:, alt.reduced_row_echelon(p_coboundaries)[1]]
    p_full = extend_columns(p_b, p_z)
    p_h = p_full[:, p_b.shape[1] :]
    action_theta = quotient_action(
        graph, x_perm, y_perm, alt.S_PERM, theta, p_full, p_h, p_b.shape[1]
    )
    action_tau = quotient_action(
        graph, x_perm, y_perm, alt.T_PERM, tau, p_full, p_h, p_b.shape[1]
    )
    invariant_conditions = np.concatenate(
        (
            action_theta - alt.identity(p_h.shape[1]),
            action_tau - alt.identity(p_h.shape[1]),
        ),
        axis=0,
    ) % FIELD
    invariant_dimension = p_h.shape[1] - alt.matrix_rank(invariant_conditions)
    observed = {
        "dim_ker_I_plus_theta": dimension
        - alt.matrix_rank((alt.identity(dimension) + theta) % FIELD),
        "dim_ker_I_plus_tau_plus_tau2": dimension
        - alt.matrix_rank((alt.identity(dimension) + tau + alt.product(tau, tau)) % FIELD),
        "condition_rank": alt.matrix_rank(condition),
        "Z1_dimension": z_basis.shape[1],
        "B1_dimension": b_basis.shape[1],
        "H1_dimension": h_basis.shape[1],
        "H1_order": FIELD**h_basis.shape[1],
        "descending_class_count": descends_count,
        "surjective_component_class_count": len(producer["classes"]) - descends_count,
        "unique_quotient_signatures": len(quotient_signatures),
        "H1_barW_dimension": invariant_dimension,
        "H1_barW_order": FIELD**invariant_dimension,
        "P_relation_rank": graph["relation_rank"],
        "Z1_P_dimension": p_z.shape[1],
        "B1_P_dimension": p_b.shape[1],
        "H1_P_dimension": p_h.shape[1],
    }
    fields = (
        "dim_ker_I_plus_theta",
        "dim_ker_I_plus_tau_plus_tau2",
        "condition_rank",
        "Z1_dimension",
        "B1_dimension",
        "H1_dimension",
        "H1_order",
        "descending_class_count",
        "surjective_component_class_count",
    )
    for field in fields:
        compare(mismatches, location, field, producer[field], observed[field])
    compare(
        mismatches,
        location,
        "class_count_equals_H1_order",
        producer["H1_order"],
        observed["unique_quotient_signatures"],
    )
    for field in (
        "H1_barW_dimension",
        "H1_barW_order",
        "P_relation_rank",
        "Z1_P_dimension",
        "B1_P_dimension",
        "H1_P_dimension",
    ):
        compare(mismatches, location + ".SL_RE", field, producer["SL_RE"][field], observed[field])
    return observed


def component_templates(
    theta: np.ndarray,
    tau: np.ndarray,
    rows: list[dict[str, Any]],
    action_key: str,
    block_count: int,
    change: np.ndarray,
    change_inverse: np.ndarray,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    dimension = theta.shape[0]
    output_change_inverse = alt.block_diagonal([change_inverse, change_inverse])
    cocycle_change = alt.block_diagonal([change, change])
    elements = marked_symbols(theta, tau)
    templates = []
    digest_rows = []
    for row in rows:
        first, second, generator_a, generator_b = full_relations(
            elements, row[action_key], int(row["m"])
        )
        if not np.array_equal(first.action, alt.identity(dimension)) or not np.array_equal(
            second.action, alt.identity(dimension)
        ):
            raise RuntimeError("checker roof action misses full hexagon")
        rank_a1 = alt.matrix_rank(first.f_coefficient)
        rank_a2 = alt.matrix_rank(second.f_coefficient)
        if rank_a1 != rank_a2:
            raise RuntimeError("checker rank(A1) differs from rank(A2)")
        matrix = np.concatenate((first.f_coefficient, second.f_coefficient), axis=0)
        class_coefficient = np.concatenate((first.z_coefficient, second.z_coefficient), axis=0)
        constant = np.concatenate((first.constant, second.constant)) % FIELD
        hex_template = system_template(matrix)
        producer_matrix = output_change_inverse @ matrix @ change % FIELD
        producer_class_coefficient = (
            output_change_inverse @ class_coefficient @ cocycle_change % FIELD
        )
        producer_left_null = alt.kernel_columns(producer_matrix.T).T % FIELD
        subsets = {}
        invariant_dimensions = []
        for block in range(block_count):
            section = slice(BLOCK * block, BLOCK * block + BLOCK)
            invariant_matrix = np.concatenate(
                (
                    alt.identity(BLOCK) - generator_a.action[section, section],
                    alt.identity(BLOCK) - generator_b.action[section, section],
                ),
                axis=0,
            ) % FIELD
            invariant_dimensions.append(BLOCK - alt.matrix_rank(invariant_matrix))
        if invariant_dimensions != [0] * block_count:
            raise RuntimeError("checker target has constituent invariant")
        for mask in range(1, 1 << block_count):
            selected = [block for block in range(block_count) if (mask >> block) & 1]
            variable_count = dimension + BLOCK * len(selected)
            base = np.zeros((2 * dimension, variable_count), dtype=np.int64)
            base[:, :dimension] = matrix
            pieces = [base]
            for position, block in enumerate(selected):
                section = slice(BLOCK * block, BLOCK * block + BLOCK)
                auxiliary = slice(
                    dimension + BLOCK * position,
                    dimension + BLOCK * position + BLOCK,
                )
                first_bad = np.zeros((BLOCK, variable_count), dtype=np.int64)
                first_bad[:, auxiliary] = (
                    alt.identity(BLOCK) - generator_a.action[section, section]
                ) % FIELD
                second_bad = np.zeros((BLOCK, variable_count), dtype=np.int64)
                second_bad[:, :dimension] = generator_b.f_coefficient[section, :]
                second_bad[:, auxiliary] = -(
                    alt.identity(BLOCK) - generator_b.action[section, section]
                ) % FIELD
                pieces.extend((first_bad, second_bad))
            subsets[str(mask)] = {
                "selected": selected,
                "template": system_template(np.concatenate(pieces, axis=0)),
            }
        templates.append(
            {
                "rank_A1": rank_a1,
                "rank_A2": rank_a2,
                "matrix": matrix,
                "class_coefficient": class_coefficient,
                "constant": constant,
                "hex": hex_template,
                "producer_left_null": producer_left_null,
                "output_change_inverse": output_change_inverse,
                "subsets": subsets,
                "generator_a_z": generator_a.z_coefficient,
                "generator_a_constant": generator_a.constant,
                "generator_b_z": generator_b.z_coefficient,
                "generator_b_constant": generator_b.constant,
            }
        )
        digest_rows.append(
            {
                "rank_A1": rank_a1,
                "rank_A2": rank_a2,
                "rank_A": hex_template["rank"],
                "A_sha256": object_digest(producer_matrix.tolist()),
                "C_sha256": object_digest(producer_class_coefficient.tolist()),
                "left_null_sha256": object_digest(producer_left_null.tolist()),
                "subset_ranks": {
                    mask: entry["template"]["rank"] for mask, entry in subsets.items()
                },
            }
        )
    rank_pairs = Counter((entry["rank_A1"], entry["rank_A2"]) for entry in templates)
    ranks = Counter(entry["hex"]["rank"] for entry in templates)
    return templates, {
        "rows": len(templates),
        "A_shape": [2 * dimension, dimension],
        "rank_A1_A2_distribution": {
            f"{left},{right}": count for (left, right), count in sorted(rank_pairs.items())
        },
        "rank_A_distribution": counter_json(ranks),
        "dim_ker_A_distribution": counter_json(
            Counter(dimension - entry["hex"]["rank"] for entry in templates)
        ),
        "rank_A1_equals_rank_A2_all_rows": all(left == right for left, right in rank_pairs),
        "template_sha256": object_digest(digest_rows),
    }


def measure_component(
    label: str,
    producer_component: dict[str, Any],
    templates: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    change: np.ndarray,
    checkpoint_update,
) -> tuple[dict[str, Any], list[list[tuple[tuple[int, ...], int, int, bool]]]]:
    classes = [
        entry
        for entry in producer_component["cohomology"]["classes"]
        if entry["surjective_component"]
    ]
    change_twice = alt.block_diagonal([change, change])
    outcomes_by_class = []
    summaries = []
    obstruction_distribution = Counter()
    solution_distribution = Counter()
    generation_distribution = Counter()
    joint_distribution = Counter()
    sparse_nonzero = []
    digest = hashlib.sha256()
    for class_position, entry in enumerate(classes):
        producer_representative = alt.matrix(entry["representative"]).reshape(-1)
        representative = change_twice @ producer_representative % FIELD
        outcomes = []
        class_nonzero = 0
        class_generation_absent = 0
        class_lifts = 0
        class_generation = Counter()
        for row, template in zip(rows, templates):
            rhs = -(
                template["class_coefficient"] @ representative + template["constant"]
            ) % FIELD
            producer_rhs = template["output_change_inverse"] @ rhs % FIELD
            obstruction = tuple(
                int(value) for value in template["producer_left_null"] @ producer_rhs % FIELD
            )
            obstruction_zero = not any(obstruction)
            total = system_count(template["hex"], rhs)
            bad_counts = {}
            if total:
                for mask, subset in template["subsets"].items():
                    rhs_parts = [rhs]
                    for block in subset["selected"]:
                        section = slice(BLOCK * block, BLOCK * block + BLOCK)
                        rhs_parts.append(
                            (
                                template["generator_a_z"][section, :] @ representative
                                + template["generator_a_constant"][section]
                            )
                            % FIELD
                        )
                        rhs_parts.append(
                            -(
                                template["generator_b_z"][section, :] @ representative
                                + template["generator_b_constant"][section]
                            )
                            % FIELD
                        )
                    bad_counts[mask] = system_count(
                        subset["template"], np.concatenate(rhs_parts)
                    )
                union = sum(
                    count if int(mask).bit_count() % 2 else -count
                    for mask, count in bad_counts.items()
                )
                generating_count = total - union
            else:
                generating_count = 0
            lift = bool(obstruction_zero and generating_count > 0)
            outcomes.append((obstruction, int(total), int(generating_count), lift))
            obstruction_distribution[obstruction_zero] += 1
            solution_distribution[int(total)] += 1
            generation_distribution[int(generating_count)] += 1
            joint_distribution[(obstruction_zero, generating_count > 0)] += 1
            class_nonzero += int(not obstruction_zero)
            class_generation_absent += int(generating_count == 0)
            class_lifts += int(lift)
            class_generation[int(generating_count)] += 1
            record = [
                label,
                int(entry["class_index"]),
                int(row["t_index"]),
                list(obstruction),
                int(total),
                int(generating_count),
                int(lift),
            ]
            digest.update(json.dumps(record, separators=(",", ":")).encode() + b"\n")
            if not obstruction_zero:
                sparse_nonzero.append(
                    {
                        "class_index": int(entry["class_index"]),
                        "quotient_coordinates": entry["quotient_coordinates"],
                        "t_index": int(row["t_index"]),
                        "t2_index": int(row["t2_index"]),
                        "k3_index": int(row["k3_index"]),
                        "k_mod3": int(row["k_mod3"]),
                        "obstruction_coordinates": list(obstruction),
                    }
                )
        outcomes_by_class.append(outcomes)
        summaries.append(
            {
                "class_position": class_position,
                "class_index": int(entry["class_index"]),
                "quotient_coordinates": entry["quotient_coordinates"],
                "obstruction_nonzero_rows": class_nonzero,
                "generation_absent_rows": class_generation_absent,
                "lift_rows": class_lifts,
                "generating_solution_count_distribution": counter_json(class_generation),
            }
        )
        if (class_position + 1) % 10 == 0 or class_position + 1 == len(classes):
            checkpoint_update(
                f"component_{label}",
                component=label,
                classes_complete=class_position + 1,
                classes_total=len(classes),
            )
    return (
        {
            "label": label,
            "surjective_component_class_count": len(classes),
            "evaluated_rows": len(classes) * 324,
            "class_summaries": summaries,
            "obstruction_zero_distribution": counter_json(obstruction_distribution),
            "solution_count_distribution": counter_json(solution_distribution),
            "generating_solution_count_distribution": counter_json(generation_distribution),
            "obstruction_generation_joint_distribution": {
                f"obstruction_zero={str(left).lower()},generation_exists={str(right).lower()}": count
                for (left, right), count in sorted(joint_distribution.items())
            },
            "nonzero_obstruction_rows": sparse_nonzero,
            "component_outcome_sha256": digest.hexdigest(),
        },
        outcomes_by_class,
    )


def combine_window(
    window: dict[str, Any],
    orbit_component: dict[str, Any],
    trivial_component: dict[str, Any],
    orbit_outcomes: list[list[tuple[tuple[int, ...], int, int, bool]]],
    trivial_outcomes: list[list[tuple[tuple[int, ...], int, int, bool]]],
    rows: list[dict[str, Any]],
    checkpoint_update,
) -> dict[str, Any]:
    orbit_classes = [
        entry
        for entry in orbit_component["cohomology"]["classes"]
        if entry["surjective_component"]
    ]
    trivial_classes = [
        entry
        for entry in trivial_component["cohomology"]["classes"]
        if entry["surjective_component"]
    ]
    per_class = []
    obstruction_distribution = Counter()
    solution_distribution = Counter()
    generation_distribution = Counter()
    joint_distribution = Counter()
    image_nw_distribution = Counter()
    image_km_distribution = Counter()
    theta2_distribution = Counter()
    sparse_nonzero = []
    sparse_generation_absent = []
    digest = hashlib.sha256()
    class_position = 0
    for orbit_position, orbit_class in enumerate(orbit_classes):
        for trivial_position, trivial_class in enumerate(trivial_classes):
            lift_count = 0
            nonzero_count = 0
            generation_absent = 0
            theta_masks = [0] * 54
            class_generation = Counter()
            for row, orbit_value, trivial_value in zip(
                rows,
                orbit_outcomes[orbit_position],
                trivial_outcomes[trivial_position],
            ):
                orbit_obstruction, orbit_total, orbit_generation, orbit_lift = orbit_value
                trivial_obstruction, trivial_total, trivial_generation, trivial_lift = trivial_value
                obstruction_zero = not any(orbit_obstruction) and not any(trivial_obstruction)
                total = orbit_total * trivial_total
                generating_count = orbit_generation * trivial_generation
                lift = bool(orbit_lift and trivial_lift)
                obstruction_distribution[obstruction_zero] += 1
                solution_distribution[total] += 1
                generation_distribution[generating_count] += 1
                joint_distribution[(obstruction_zero, generating_count > 0)] += 1
                class_generation[generating_count] += 1
                nonzero_count += int(not obstruction_zero)
                generation_absent += int(generating_count == 0)
                lift_count += int(lift)
                if lift:
                    theta_masks[int(row["t2_index"])] |= 1 << int(row["k_mod3"])
                record = [
                    window["window_id"],
                    int(orbit_class["class_index"]),
                    int(trivial_class["class_index"]),
                    int(row["t_index"]),
                    list(orbit_obstruction),
                    list(trivial_obstruction),
                    int(total),
                    int(generating_count),
                    int(lift),
                ]
                digest.update(json.dumps(record, separators=(",", ":")).encode() + b"\n")
                if not obstruction_zero:
                    sparse_nonzero.append(
                        {
                            "class_position": class_position,
                            "orbit_class_index": int(orbit_class["class_index"]),
                            "trivial_class_index": int(trivial_class["class_index"]),
                            "orbit_quotient_coordinates": orbit_class["quotient_coordinates"],
                            "trivial_quotient_coordinates": trivial_class["quotient_coordinates"],
                            "t_index": int(row["t_index"]),
                            "t2_index": int(row["t2_index"]),
                            "k3_index": int(row["k3_index"]),
                            "k_mod3": int(row["k_mod3"]),
                            "obstruction_coordinates": {
                                "orbit_bundle": list(orbit_obstruction),
                                "trivial_character": list(trivial_obstruction),
                            },
                        }
                    )
                if generating_count == 0:
                    sparse_generation_absent.append(
                        {
                            "class_position": class_position,
                            "t_index": int(row["t_index"]),
                            "t2_index": int(row["t2_index"]),
                        }
                    )
            theta_counts = [int(mask).bit_count() for mask in theta_masks]
            theta2_distribution.update(theta_counts)
            image_nw = lift_count
            image_km = sum(
                int(row["K9_preimage_count"])
                for row, orbit_value, trivial_value in zip(
                    rows,
                    orbit_outcomes[orbit_position],
                    trivial_outcomes[trivial_position],
                )
                if orbit_value[3] and trivial_value[3]
            )
            image_nw_distribution[image_nw] += 1
            image_km_distribution[image_km] += 1
            per_class.append(
                {
                    "class_position": class_position,
                    "orbit_class_index": int(orbit_class["class_index"]),
                    "trivial_class_index": int(trivial_class["class_index"]),
                    "orbit_quotient_coordinates": orbit_class["quotient_coordinates"],
                    "trivial_quotient_coordinates": trivial_class["quotient_coordinates"],
                    "obstruction_nonzero_rows": nonzero_count,
                    "generation_absent_rows": generation_absent,
                    "lift_rows": lift_count,
                    "generating_solution_count_distribution": counter_json(class_generation),
                    "theta2_k_masks": theta_masks,
                    "theta2_counts": theta_counts,
                    "theta2_rigid": all(count == 1 for count in theta_counts),
                    "Im_R_N_E_N_W_size": image_nw,
                    "Im_R_K_M_size": image_km,
                }
            )
            class_position += 1
        if (orbit_position + 1) % 10 == 0 or orbit_position + 1 == len(orbit_classes):
            checkpoint_update(
                f"combine_{window['window_id']}",
                window_id=window["window_id"],
                orbit_classes_complete=orbit_position + 1,
                orbit_classes_total=len(orbit_classes),
                full_classes_complete=class_position,
            )
    rank_gate = window["template_gate"]
    return {
        "window_id": window["window_id"],
        "eps": window["eps"],
        "eta": window["eta"],
        "surjective_class_count": class_position,
        "evaluated_full_rows": class_position * 324,
        "per_class": per_class,
        "obstruction_zero_distribution": counter_json(obstruction_distribution),
        "solution_count_distribution": counter_json(solution_distribution),
        "generating_solution_count_distribution": counter_json(generation_distribution),
        "obstruction_generation_joint_distribution": {
            f"obstruction_zero={str(left).lower()},generation_exists={str(right).lower()}": count
            for (left, right), count in sorted(joint_distribution.items())
        },
        "nonzero_obstruction_rows": sparse_nonzero,
        "generation_absent_rows": sparse_generation_absent,
        "Im_R_N_E_N_W_distribution": counter_json(image_nw_distribution),
        "Im_R_K_M_distribution": counter_json(image_km_distribution),
        "theta2_count_distribution_across_classes_and_t2": counter_json(theta2_distribution),
        "theta2_rigid_class_count": sum(entry["theta2_rigid"] for entry in per_class),
        "rank_A1_A2_distribution": rank_gate["rank_A1_A2_distribution"],
        "rank_A_distribution": rank_gate["rank_A_distribution"],
        "dim_ker_A_distribution": rank_gate["dim_ker_A_distribution"],
        "full_outcome_sha256": digest.hexdigest(),
    }


def audit_preflight(
    preflight: dict[str, Any], mismatches: list[dict[str, Any]]
) -> dict[str, Any]:
    change7 = alt.coordinate_change()
    change7_inverse = alt.inverse_matrix(change7)
    change_orbit = alt.block_diagonal([change7, change7, change7])
    change_orbit_inverse = alt.block_diagonal(
        [change7_inverse, change7_inverse, change7_inverse]
    )
    change_full = alt.block_diagonal([change_orbit, change7])
    change_full_inverse = alt.block_diagonal([change_orbit_inverse, change7_inverse])
    s_heart = alt.alternate_heart(alt.S_PERM)
    t_heart = alt.alternate_heart(alt.T_PERM)
    sigma_1_perm = alt.after(alt.inverse_permutation(alt.T_PERM), alt.S_PERM)
    sigma_2_perm = alt.after(alt.S_PERM, alt.permutation_power(alt.T_PERM, 2))
    x_perm = alt.permutation_power(sigma_1_perm, 2)
    y_perm = alt.permutation_power(sigma_2_perm, 2)
    x_heart = alt.alternate_heart(x_perm)
    y_heart = alt.alternate_heart(y_perm)
    rho_x_orbit = alt.module_action(x_heart, (1, 0))
    rho_y_orbit = alt.module_action(y_heart, (0, 1))
    rho_x_full = alt.block_diagonal([rho_x_orbit, x_heart])
    rho_y_full = alt.block_diagonal([rho_y_orbit, y_heart])
    theta_base_orbit = alt.block_transport(s_heart, (1, 0, 2))
    tau_base_orbit = alt.block_transport(t_heart, (2, 0, 1))
    theta_base_full = alt.block_diagonal([theta_base_orbit, s_heart])
    tau_base_full = alt.block_diagonal([tau_base_orbit, t_heart])

    rows, public_rows = build_roof(
        x_heart,
        y_heart,
        change_orbit,
        change_orbit_inverse,
        change7,
        change7_inverse,
    )
    compare(mismatches, "roof", "targets", preflight["roof"]["targets"], public_rows)

    gauge = gauge_census(theta_base_full, tau_base_full, rho_x_full, rho_y_full)
    compare(mismatches, "gauge", "full_census", preflight["gauge"], gauge)

    signatures_x = (-1, 1, -1, 1)
    signatures_y = (1, -1, -1, 1)
    constituent_actions = [
        (
            (signatures_x[index] * x_heart) % FIELD,
            (signatures_y[index] * y_heart) % FIELD,
        )
        for index in range(4)
    ]
    hom_dimensions = [
        [hom_dimension(constituent_actions[left], constituent_actions[right]) for right in range(4)]
        for left in range(4)
    ]
    cyclic_counts = Counter()
    for coordinates in itertools.product(range(FIELD), repeat=BLOCK):
        if any(coordinates):
            cyclic_counts[cyclic_span_dimension(np.asarray(coordinates), (x_heart, y_heart))] += 1
    c9_numeric = {
        "P_order": 504,
        "V7_dimension": 7,
        "nonzero_cyclic_submodule_dimension_distribution": counter_json(cyclic_counts),
        "V7_irreducible_over_F3": cyclic_counts == Counter({7: 2186}),
        "End_P_V7_dimension": centralizer_dimension((x_heart, y_heart)),
        "V7_absolutely_irreducible": cyclic_counts == Counter({7: 2186})
        and centralizer_dimension((x_heart, y_heart)) == 1,
        "W_constituent_character_signatures_XY": [
            [signatures_x[index], signatures_y[index]] for index in range(4)
        ],
        "Hom_W_dimension_matrix": hom_dimensions,
        "pairwise_nonisomorphic": hom_dimensions
        == [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        "End_W_V_dimension": 4,
        "End_W_V_unit_group_order": 16,
    }
    for field, value in c9_numeric.items():
        compare(mismatches, "C9", field, preflight["C9"][field], value)

    p9 = np.zeros((9, 9), dtype=np.int64)
    for source, target in enumerate(alt.T_PERM):
        p9[target, source] = 1
    h2 = {
        "all_eight_V7_Jordan_types": all_jordan_types(),
        "actual_V7_trivial_character_block": h2_audit(t_heart),
        "orbit_bundle_V21": h2_audit(tau_base_orbit),
        "ESCAPE_V28": h2_audit(tau_base_full),
        "contrast_V9_permutation_block_system": h2_audit(p9),
    }
    compare(mismatches, "entry_H2", "all", preflight["entry_H2"], h2)

    orbit_templates = {}
    trivial_templates = {}
    orbit_signs = {"+": (2, 2, 1), "-": (1, 1, 2)}
    for eps, signs in orbit_signs.items():
        component = preflight["components"]["orbit_bundle"][eps]
        theta = alt.product(
            theta_base_orbit,
            alt.block_diagonal([sign * alt.identity(BLOCK) for sign in signs]),
        )
        tau = tau_base_orbit.copy()
        producer_theta = alt.matrix(component["theta_matrix"])
        producer_tau = alt.matrix(component["tau_matrix"])
        compare(
            mismatches,
            f"orbit[{eps}]",
            "theta_transport",
            theta.tolist(),
            (change_orbit @ producer_theta @ change_orbit_inverse % FIELD).tolist(),
        )
        compare(
            mismatches,
            f"orbit[{eps}]",
            "tau_transport",
            tau.tolist(),
            (change_orbit @ producer_tau @ change_orbit_inverse % FIELD).tolist(),
        )
        verify_component_cohomology(
            component["cohomology"],
            theta,
            tau,
            x_perm,
            y_perm,
            alt.block_diagonal([x_heart, x_heart, x_heart]),
            alt.block_diagonal([y_heart, y_heart, y_heart]),
            change_orbit,
            mismatches,
            f"orbit[{eps}].cohomology",
        )
        templates, summary = component_templates(
            theta,
            tau,
            rows,
            "orbit_action",
            3,
            change_orbit,
            change_orbit_inverse,
        )
        compare(
            mismatches,
            f"orbit[{eps}]",
            "template_gate",
            component["template_gate"],
            summary,
        )
        orbit_templates[eps] = templates

    for eta, sign in (("+", 1), ("-", 2)):
        component = preflight["components"]["trivial_character"][eta]
        theta = sign * s_heart % FIELD
        tau = t_heart.copy()
        producer_theta = alt.matrix(component["theta_matrix"])
        producer_tau = alt.matrix(component["tau_matrix"])
        compare(
            mismatches,
            f"trivial[{eta}]",
            "theta_transport",
            theta.tolist(),
            (change7 @ producer_theta @ change7_inverse % FIELD).tolist(),
        )
        compare(
            mismatches,
            f"trivial[{eta}]",
            "tau_transport",
            tau.tolist(),
            (change7 @ producer_tau @ change7_inverse % FIELD).tolist(),
        )
        verify_component_cohomology(
            component["cohomology"],
            theta,
            tau,
            x_perm,
            y_perm,
            x_heart,
            y_heart,
            change7,
            mismatches,
            f"trivial[{eta}].cohomology",
        )
        templates, summary = component_templates(
            theta,
            tau,
            rows,
            "trivial_action",
            1,
            change7,
            change7_inverse,
        )
        compare(
            mismatches,
            f"trivial[{eta}]",
            "template_gate",
            component["template_gate"],
            summary,
        )
        trivial_templates[eta] = templates

    checked_windows = []
    for window in preflight["windows"]:
        eps = window["eps"]
        eta = window["eta"]
        orbit_component = preflight["components"]["orbit_bundle"][eps]
        trivial_component = preflight["components"]["trivial_character"][eta]
        rank_a1 = [
            orbit_templates[eps][index]["rank_A1"] + trivial_templates[eta][index]["rank_A1"]
            for index in range(324)
        ]
        rank_a2 = [
            orbit_templates[eps][index]["rank_A2"] + trivial_templates[eta][index]["rank_A2"]
            for index in range(324)
        ]
        rank_a = [
            orbit_templates[eps][index]["hex"]["rank"] + trivial_templates[eta][index]["hex"]["rank"]
            for index in range(324)
        ]
        gate = {
            "A_shape": [56, 28],
            "rank_A1_A2_distribution": counter_json(Counter(zip(rank_a1, rank_a2))),
            "rank_A_distribution": counter_json(Counter(rank_a)),
            "dim_ker_A_distribution": counter_json(
                Counter(28 - value for value in rank_a)
            ),
            "rank_A1_equals_rank_A2_all_rows": rank_a1 == rank_a2,
            "factorisation": "orbit 21D direct sum trivial-character 7D",
            "component_template_sha256": [
                orbit_component["template_gate"]["template_sha256"],
                trivial_component["template_gate"]["template_sha256"],
            ],
        }
        compare(
            mismatches,
            f"window[{window['window_id']}]",
            "template_gate",
            window["template_gate"],
            gate,
        )
        checked_windows.append(
            {
                "window_id": window["window_id"],
                "surjective_class_count": window["surjective_class_count"],
                "template_gate": gate,
            }
        )
    return {
        "change7": change7,
        "change7_inverse": change7_inverse,
        "change_orbit": change_orbit,
        "change_orbit_inverse": change_orbit_inverse,
        "rows": rows,
        "orbit_templates": orbit_templates,
        "trivial_templates": trivial_templates,
        "checked_windows": checked_windows,
        "h2": h2,
        "gauge": gauge,
        "C9_numeric": c9_numeric,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("preflight", "measure"), required=True)
    parser.add_argument(
        "--preflight",
        default="search/certs/escape28_preflight_v1_20260813.json",
    )
    parser.add_argument(
        "--input",
        default="search/certs/escape28_mainrun_raw_v1_20260813.json",
    )
    parser.add_argument(
        "--output",
        default="search/certs/escape28_mainrun_check_v1_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/escape28_mainrun_check_v1_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=1800)
    args = parser.parse_args()
    preflight_path = ROOT / args.preflight
    input_path = ROOT / args.input
    output_path = ROOT / args.output
    checkpoint_path = ROOT / args.checkpoint
    began = time.monotonic()
    state: dict[str, Any] = {
        "schema": "escape28_mainrun_check_checkpoint/v1",
        "mode": args.mode,
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
        preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
        mismatches: list[dict[str, Any]] = []
        runtime = audit_preflight(preflight, mismatches)
        update("preflight_audited", mismatch_count=len(mismatches))
        if args.mode == "preflight":
            result = {
                "schema": "escape28_preflight_check/v1",
                "run_id": "escape28-preflight-check-"
                + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
                "checker": {
                    "script": "search/check_escape28_mainrun_v1.py",
                    "script_sha256": file_digest(Path(__file__)),
                    "reused_checker_engine": "search/check_vnbit_compact_mainrun_v3.py",
                    "reused_checker_engine_sha256": file_digest(
                        ROOT / "search/check_vnbit_compact_mainrun_v3.py"
                    ),
                    "imports_task_producer": False,
                    "basis": "e_i-e_0 (1<=i<=7), eliminate e_8-e_0",
                },
                "input": {args.preflight: file_digest(preflight_path)},
                "window_count": len(runtime["checked_windows"]),
                "roof_rows": len(runtime["rows"]),
                "mismatch_count": len(mismatches),
                "mismatch_examples": mismatches,
                "noncontact": {
                    "u": False,
                    "c": False,
                    "sealed_three_quantities": False,
                    "sealed_K5": False,
                },
                "status_note": "independent preflight comparison; no type adjudication",
            }
            replace_json(output_path, result)
            update(
                "complete",
                complete=True,
                mismatch_count=len(mismatches),
                output_sha256=file_digest(output_path),
            )
            return 0 if not mismatches else 1

        raw = json.loads(input_path.read_text(encoding="utf-8"))
        component_checked = {"orbit_bundle": {}, "trivial_character": {}}
        component_outcomes: dict[str, dict[str, Any]] = {
            "orbit_bundle": {},
            "trivial_character": {},
        }
        for eps in ("+", "-"):
            observed, outcomes = measure_component(
                f"orbit:{eps}",
                preflight["components"]["orbit_bundle"][eps],
                runtime["orbit_templates"][eps],
                runtime["rows"],
                runtime["change_orbit"],
                update,
            )
            producer = raw["component_factorisation"]["component_results"][
                "orbit_bundle"
            ][eps]
            compare(mismatches, f"component.orbit[{eps}]", "all", producer, observed)
            component_checked["orbit_bundle"][eps] = observed
            component_outcomes["orbit_bundle"][eps] = outcomes
        for eta in ("+", "-"):
            observed, outcomes = measure_component(
                f"trivial:{eta}",
                preflight["components"]["trivial_character"][eta],
                runtime["trivial_templates"][eta],
                runtime["rows"],
                runtime["change7"],
                update,
            )
            producer = raw["component_factorisation"]["component_results"][
                "trivial_character"
            ][eta]
            compare(mismatches, f"component.trivial[{eta}]", "all", producer, observed)
            component_checked["trivial_character"][eta] = observed
            component_outcomes["trivial_character"][eta] = outcomes

        checked_windows = []
        raw_by_window = {entry["window_id"]: entry for entry in raw["per_window"]}
        for window in preflight["windows"]:
            eps = window["eps"]
            eta = window["eta"]
            observed = combine_window(
                window,
                preflight["components"]["orbit_bundle"][eps],
                preflight["components"]["trivial_character"][eta],
                component_outcomes["orbit_bundle"][eps],
                component_outcomes["trivial_character"][eta],
                runtime["rows"],
                update,
            )
            compare(
                mismatches,
                f"window[{window['window_id']}]",
                "all",
                raw_by_window[window["window_id"]],
                observed,
            )
            checked_windows.append(
                {
                    "window_id": window["window_id"],
                    "surjective_classes": observed["surjective_class_count"],
                    "checked_full_rows": observed["evaluated_full_rows"],
                    "nonzero_obstruction_rows": len(observed["nonzero_obstruction_rows"]),
                    "generation_absent_rows": len(observed["generation_absent_rows"]),
                    "full_outcome_sha256": observed["full_outcome_sha256"],
                    "Im_R_N_E_N_W_distribution": observed[
                        "Im_R_N_E_N_W_distribution"
                    ],
                    "Im_R_K_M_distribution": observed["Im_R_K_M_distribution"],
                }
            )
        checked_rows = sum(entry["checked_full_rows"] for entry in checked_windows)
        compare(
            mismatches,
            "full_campaign",
            "evaluated_full_rows",
            raw["full_campaign"]["evaluated_full_rows"],
            checked_rows,
        )
        result = {
            "schema": "escape28_mainrun_check/v1",
            "run_id": "escape28-mainrun-check-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "checker": {
                "script": "search/check_escape28_mainrun_v1.py",
                "script_sha256": file_digest(Path(__file__)),
                "reused_checker_engine": "search/check_vnbit_compact_mainrun_v3.py",
                "reused_checker_engine_sha256": file_digest(
                    ROOT / "search/check_vnbit_compact_mainrun_v3.py"
                ),
                "imports_task_producer": False,
                "method": (
                    "alternate heart basis; independent roof rebuild; full hexagons; "
                    "component inclusion-exclusion; exhaustive Cartesian expansion"
                ),
            },
            "inputs": {
                args.preflight: file_digest(preflight_path),
                args.input: file_digest(input_path),
                "certificates/S4.v2.json": file_digest(ROOT / "certificates/S4.v2.json"),
                "certificates/K3.v1.json": file_digest(ROOT / "certificates/K3.v1.json"),
                "certificates/K9.v1.json": file_digest(ROOT / "certificates/K9.v1.json"),
            },
            "basis": {
                "checker": "e_i-e_0 (1<=i<=7), eliminate e_8-e_0",
                "producer_to_checker_sha256": object_digest(runtime["change7"].tolist()),
            },
            "roof_rows": len(runtime["rows"]),
            "checked_full_rows": checked_rows,
            "component_summaries": {
                family: {
                    key: {
                        "evaluated_rows": value["evaluated_rows"],
                        "component_outcome_sha256": value["component_outcome_sha256"],
                        "nonzero_obstruction_rows": len(value["nonzero_obstruction_rows"]),
                    }
                    for key, value in entries.items()
                }
                for family, entries in component_checked.items()
            },
            "window_summaries": checked_windows,
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
            checked_full_rows=checked_rows,
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
