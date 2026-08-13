#!/usr/bin/env python3
"""Task 133 producer for the ESCAPE-28 compact campaign.

The 28-dimensional module is the direct sum of the 21-dimensional orbit
bundle from task 132 and the 7-dimensional trivial-character constituent.
Preflight and outcome measurement are deliberately separate.  The full
1,099,008-row universe is evaluated through the certified direct-sum
factorisation of the affine equations; component outcomes are then expanded
over every pair of surjective component classes and every one of 324 rows.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import threading
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

import vnbit_compact_mainrun_v3 as old


ROOT = Path(__file__).resolve().parents[1]
F = 3
BLOCK = 7
ORBIT_DIM = 21
TRIVIAL_DIM = 7
FULL_DIM = 28


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def object_sha(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def counter_json(value: Counter) -> dict[str, int]:
    return {str(key): int(count) for key, count in sorted(value.items())}


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


def permutation_matrix(destinations: tuple[int, ...]) -> np.ndarray:
    answer = np.zeros((len(destinations), len(destinations)), dtype=np.uint8)
    for source, target in enumerate(destinations):
        answer[target, source] = 1
    return answer


def twist_classifier() -> dict[str, Any]:
    """Compute H^1(S3,F2^4) from the full Cayley collision system."""
    s = permutation_matrix((1, 0, 2, 3))
    t = permutation_matrix((2, 0, 1, 3))
    identity = np.eye(4, dtype=np.uint8)
    zero = np.zeros((4, 8), dtype=np.uint8)
    generator_expressions = []
    for which in range(2):
        expression = zero.copy()
        expression[:, 4 * which : 4 * which + 4] = identity
        generator_expressions.append(expression)
    key = lambda matrix: tuple(int(x) for x in matrix.flatten())
    elements = [identity]
    data = {key(identity): (identity, zero)}
    constraints = []
    for group_element in elements:
        action, expression = data[key(group_element)]
        for generator, generator_expression in (
            (s, generator_expressions[0]),
            (t, generator_expressions[1]),
        ):
            new_action = (action @ generator) % 2
            new_expression = (expression + action @ generator_expression) % 2
            new_key = key(new_action)
            if new_key in data:
                constraints.append((new_expression - data[new_key][1]) % 2)
            else:
                data[new_key] = (new_action, new_expression)
                elements.append(new_action)
    relation = np.concatenate(constraints, axis=0)
    z_dimension = 8 - gf2_rank(relation)
    coboundary = np.concatenate((identity - s, identity - t), axis=0) % 2
    b_dimension = gf2_rank(coboundary)
    return {
        "coefficient_module": "F_2^4 (three-point orbit plus one fixed point)",
        "S3_order": len(elements),
        "Z1_dimension": z_dimension,
        "B1_dimension": b_dimension,
        "H1_dimension": z_dimension - b_dimension,
        "H1_order": 2 ** (z_dimension - b_dimension),
        "collision_relation_rank": gf2_rank(relation),
        "relation_sha256": object_sha(relation.tolist()),
    }


def jordan_block(size: int) -> np.ndarray:
    answer = old.eye(size)
    for index in range(size - 1):
        answer[index, index + 1] = 1
    return answer % F


def jordan_partition(value: np.ndarray) -> list[int]:
    nilpotent = (value - old.eye(value.shape[0])) % F
    rank_one = old.rank(nilpotent)
    rank_two = old.rank(old.mm(nilpotent, nilpotent))
    count_three = rank_two
    count_two = rank_one - 2 * count_three
    count_one = value.shape[0] - 3 * count_three - 2 * count_two
    return sorted([3] * count_three + [2] * count_two + [1] * count_one, reverse=True)


def h2_audit(value: np.ndarray) -> dict[str, Any]:
    identity = old.eye(value.shape[0])
    norm = (identity + value + old.mm(value, value)) % F
    fixed_dimension = value.shape[0] - old.rank((value - identity) % F)
    norm_rank = old.rank(norm)
    if np.any(((value - identity) @ norm) % F):
        raise RuntimeError("C3 norm image is not fixed")
    return {
        "dimension": value.shape[0],
        "jordan_partition": jordan_partition(value),
        "fixed_dimension": fixed_dimension,
        "norm_rank": norm_rank,
        "norm_kernel_dimension": value.shape[0] - norm_rank,
        "H2_dimension": fixed_dimension - norm_rank,
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
    answer = []
    for partition in partitions:
        matrix = old.block_diag([jordan_block(size) for size in partition])
        entry = h2_audit(matrix)
        entry["partition"] = list(partition)
        answer.append(entry)
    return answer


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
                equations.append(equation % F)
    return BLOCK * BLOCK - old.rank(np.asarray(equations, dtype=np.int64))


class SymAff:
    def __init__(
        self,
        f_coefficient: np.ndarray,
        z_coefficient: np.ndarray,
        constant: np.ndarray,
        action: np.ndarray,
    ):
        self.f_coefficient = f_coefficient % F
        self.z_coefficient = z_coefficient % F
        self.constant = constant % F
        self.action = action % F


def sym_known(dimension: int, action: np.ndarray) -> SymAff:
    return SymAff(
        np.zeros((dimension, dimension), dtype=np.int64),
        np.zeros((dimension, 2 * dimension), dtype=np.int64),
        np.zeros(dimension, dtype=np.int64),
        action,
    )


def sym_z(dimension: int, half: int, action: np.ndarray) -> SymAff:
    z_coefficient = np.zeros((dimension, 2 * dimension), dtype=np.int64)
    z_coefficient[:, half * dimension : (half + 1) * dimension] = old.eye(dimension)
    return SymAff(
        np.zeros((dimension, dimension), dtype=np.int64),
        z_coefficient,
        np.zeros(dimension, dtype=np.int64),
        action,
    )


def sym_f(action: np.ndarray) -> SymAff:
    dimension = action.shape[0]
    return SymAff(
        old.eye(dimension),
        np.zeros((dimension, 2 * dimension), dtype=np.int64),
        np.zeros(dimension, dtype=np.int64),
        action,
    )


def sym_mul(left: SymAff, right: SymAff) -> SymAff:
    return SymAff(
        left.f_coefficient + old.mm(left.action, right.f_coefficient),
        left.z_coefficient + old.mm(left.action, right.z_coefficient),
        left.constant + left.action @ right.constant,
        old.mm(left.action, right.action),
    )


def sym_inv(value: SymAff) -> SymAff:
    inverse = old.minv(value.action)
    return SymAff(
        -old.mm(inverse, value.f_coefficient),
        -old.mm(inverse, value.z_coefficient),
        -(inverse @ value.constant),
        inverse,
    )


def sym_pow(value: SymAff, exponent: int) -> SymAff:
    if exponent < 0:
        return sym_pow(sym_inv(value), -exponent)
    answer = sym_known(value.action.shape[0], old.eye(value.action.shape[0]))
    factor = value
    while exponent:
        if exponent & 1:
            answer = sym_mul(answer, factor)
        factor = sym_mul(factor, factor)
        exponent >>= 1
    return answer


def marked_symbols(theta: np.ndarray, tau: np.ndarray) -> dict[str, SymAff]:
    dimension = theta.shape[0]
    delta = sym_z(dimension, 0, theta)
    small_delta = sym_z(dimension, 1, tau)
    sigma_1 = sym_mul(sym_inv(small_delta), delta)
    sigma_2 = sym_mul(sym_inv(delta), sym_pow(small_delta, 2))
    return {
        "Delta": delta,
        "delta": small_delta,
        "sigma_1": sigma_1,
        "sigma_2": sigma_2,
        "x": sym_pow(sigma_1, 2),
        "y": sym_pow(sigma_2, 2),
    }


def relation_symbols(
    elements: dict[str, SymAff], action: np.ndarray, m_value: int
) -> tuple[SymAff, SymAff, SymAff, SymAff]:
    f = sym_f(action)
    exponent = 2 * m_value + 1
    sigma_1 = elements["sigma_1"]
    sigma_2 = elements["sigma_2"]
    x = elements["x"]
    y = elements["y"]
    c = sym_pow(elements["Delta"], 2)

    left_1 = sym_mul(
        sym_mul(sym_mul(sym_pow(sigma_1, exponent), sym_inv(f)), sym_pow(sigma_2, exponent)),
        f,
    )
    right_1 = sym_mul(
        sym_mul(sym_mul(sym_inv(f), sigma_1), sigma_2),
        sym_mul(sym_pow(x, -m_value), sym_pow(c, m_value)),
    )
    relation_1 = sym_mul(left_1, sym_inv(right_1))

    left_2 = sym_mul(
        sym_mul(sym_mul(sym_inv(f), sym_pow(sigma_2, exponent)), f),
        sym_pow(sigma_1, exponent),
    )
    right_2 = sym_mul(
        sym_mul(sym_mul(sigma_2, sigma_1), sym_pow(y, -m_value)),
        sym_mul(sym_pow(c, m_value), f),
    )
    relation_2 = sym_mul(left_2, sym_inv(right_2))
    generator_a = sym_pow(x, exponent)
    generator_b = sym_mul(sym_mul(sym_inv(f), sym_pow(y, exponent)), f)
    return relation_1, relation_2, generator_a, generator_b


def sl_audit(
    x_perm: tuple[int, ...],
    y_perm: tuple[int, ...],
    s_perm: tuple[int, ...],
    t_perm: tuple[int, ...],
    p_x: np.ndarray,
    p_y: np.ndarray,
    theta: np.ndarray,
    tau: np.ndarray,
) -> tuple[dict[str, Any], dict[str, Any]]:
    graph = old.cocycle_graph(x_perm, y_perm, p_x, p_y)
    dimension = theta.shape[0]
    z_basis = old.nullspace(graph["constraints"])
    coboundaries = np.concatenate((old.eye(dimension) - p_x, old.eye(dimension) - p_y), axis=0) % F
    b_basis = coboundaries[:, old.rref(coboundaries)[1]]
    full_basis = old.extend_columns(b_basis, z_basis)
    h_basis = full_basis[:, b_basis.shape[1] :]
    theta_action = old.q_action_on_p_h1(
        graph, x_perm, y_perm, s_perm, theta, full_basis, h_basis, b_basis.shape[1]
    )
    tau_action = old.q_action_on_p_h1(
        graph, x_perm, y_perm, t_perm, tau, full_basis, h_basis, b_basis.shape[1]
    )
    conditions = np.concatenate(
        (theta_action - old.eye(h_basis.shape[1]), tau_action - old.eye(h_basis.shape[1])),
        axis=0,
    ) % F
    invariant_dimension = h_basis.shape[1] - old.rank(conditions)
    audit = {
        "P_order": len(graph["elements"]),
        "P_positive_edges": graph["positive_edges"],
        "P_collision_edges": graph["collision_edges"],
        "P_relation_rank": graph["relation_rank"],
        "P_relation_rref_sha256": graph["relation_rref_sha256"],
        "Z1_P_dimension": z_basis.shape[1],
        "B1_P_dimension": b_basis.shape[1],
        "H1_P_dimension": h_basis.shape[1],
        "H1_P_theta_action": theta_action.tolist(),
        "H1_P_tau_action": tau_action.tolist(),
        "H1_barW_dimension": invariant_dimension,
        "H1_barW_order": F**invariant_dimension,
    }
    return audit, graph


def component_cohomology(
    theta: np.ndarray,
    tau: np.ndarray,
    x_perm: tuple[int, ...],
    y_perm: tuple[int, ...],
    s_perm: tuple[int, ...],
    t_perm: tuple[int, ...],
    p_x: np.ndarray,
    p_y: np.ndarray,
) -> dict[str, Any]:
    dimension = theta.shape[0]
    condition = np.zeros((2 * dimension, 2 * dimension), dtype=np.int64)
    condition[:dimension, :dimension] = (old.eye(dimension) + theta) % F
    condition[dimension:, dimension:] = (
        old.eye(dimension) + tau + old.mm(tau, tau)
    ) % F
    z_basis = old.nullspace(condition)
    coboundaries = np.concatenate((old.eye(dimension) - theta, old.eye(dimension) - tau), axis=0) % F
    b_basis = coboundaries[:, old.rref(coboundaries)[1]]
    full_basis = old.extend_columns(b_basis, z_basis)
    h_basis = full_basis[:, b_basis.shape[1] :]
    sl, graph = sl_audit(x_perm, y_perm, s_perm, t_perm, p_x, p_y, theta, tau)
    symbols = marked_symbols(theta, tau)
    representatives = []
    for coordinates in itertools.product(range(F), repeat=h_basis.shape[1]):
        vector = (h_basis @ np.asarray(coordinates, dtype=np.int64)) % F
        representatives.append((tuple(int(x) for x in vector), tuple(coordinates)))
    representatives.sort()
    classes = []
    for index, (vector_tuple, coordinates) in enumerate(representatives):
        vector = np.asarray(vector_tuple, dtype=np.int64)
        x_value = (symbols["x"].z_coefficient @ vector + symbols["x"].constant) % F
        y_value = (symbols["y"].z_coefficient @ vector + symbols["y"].constant) % F
        descends = not np.any((graph["constraints"] @ np.concatenate((x_value, y_value))) % F)
        classes.append(
            {
                "class_index": index,
                "quotient_coordinates": list(coordinates),
                "representative": list(vector_tuple),
                "descends_to_barW": bool(descends),
                "surjective_component": not bool(descends),
            }
        )
    descending_count = sum(entry["descends_to_barW"] for entry in classes)
    if descending_count != sl["H1_barW_order"]:
        raise RuntimeError("SURJ-LIN descent count differs from H1(barW)")
    return {
        "dim_ker_I_plus_theta": dimension - old.rank((old.eye(dimension) + theta) % F),
        "dim_ker_I_plus_tau_plus_tau2": dimension
        - old.rank((old.eye(dimension) + tau + old.mm(tau, tau)) % F),
        "condition_rank": old.rank(condition),
        "Z1_dimension": z_basis.shape[1],
        "B1_dimension": b_basis.shape[1],
        "H1_dimension": h_basis.shape[1],
        "H1_order": F**h_basis.shape[1],
        "class_basis_sha256": object_sha(h_basis.tolist()),
        "SL_RE": sl,
        "descending_class_count": descending_count,
        "surjective_component_class_count": len(classes) - descending_count,
        "classes": classes,
    }


def component_templates(
    theta: np.ndarray,
    tau: np.ndarray,
    roof_rows: list[dict[str, Any]],
    action_key: str,
    block_count: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    dimension = theta.shape[0]
    elements = marked_symbols(theta, tau)
    templates = []
    digest_rows = []
    for row in roof_rows:
        first, second, generator_a, generator_b = relation_symbols(
            elements, row[action_key], int(row["m"])
        )
        if not np.array_equal(first.action, old.eye(dimension)) or not np.array_equal(
            second.action, old.eye(dimension)
        ):
            raise RuntimeError("roof action does not satisfy the full hexagons")
        rank_a1 = old.rank(first.f_coefficient)
        rank_a2 = old.rank(second.f_coefficient)
        if rank_a1 != rank_a2:
            raise RuntimeError("rank(A1) differs from rank(A2)")
        matrix = np.concatenate((first.f_coefficient, second.f_coefficient), axis=0)
        class_coefficient = np.concatenate((first.z_coefficient, second.z_coefficient), axis=0)
        constant = np.concatenate((first.constant, second.constant)) % F
        hex_template = old.system_template(matrix)
        subsets = {}
        invariant_dimensions = []
        for block in range(block_count):
            section = slice(BLOCK * block, BLOCK * block + BLOCK)
            invariant_matrix = np.concatenate(
                (
                    old.eye(BLOCK) - generator_a.action[section, section],
                    old.eye(BLOCK) - generator_b.action[section, section],
                ),
                axis=0,
            ) % F
            invariant_dimensions.append(BLOCK - old.rank(invariant_matrix))
        if invariant_dimensions != [0] * block_count:
            raise RuntimeError("target pair has a constituent invariant")
        for mask in range(1, 1 << block_count):
            selected = [block for block in range(block_count) if (mask >> block) & 1]
            variable_count = dimension + BLOCK * len(selected)
            pieces = []
            base_matrix = np.zeros((2 * dimension, variable_count), dtype=np.int64)
            base_matrix[:, :dimension] = matrix
            pieces.append(base_matrix)
            for position, block in enumerate(selected):
                section = slice(BLOCK * block, BLOCK * block + BLOCK)
                auxiliary = slice(
                    dimension + BLOCK * position,
                    dimension + BLOCK * position + BLOCK,
                )
                first_bad = np.zeros((BLOCK, variable_count), dtype=np.int64)
                first_bad[:, auxiliary] = (
                    old.eye(BLOCK) - generator_a.action[section, section]
                ) % F
                second_bad = np.zeros((BLOCK, variable_count), dtype=np.int64)
                second_bad[:, :dimension] = generator_b.f_coefficient[section, :]
                second_bad[:, auxiliary] = -(
                    old.eye(BLOCK) - generator_b.action[section, section]
                ) % F
                pieces.extend((first_bad, second_bad))
            subsets[str(mask)] = {
                "selected": selected,
                "template": old.system_template(np.concatenate(pieces, axis=0)),
            }
        template = {
            "rank_A1": rank_a1,
            "rank_A2": rank_a2,
            "matrix": matrix,
            "class_coefficient": class_coefficient,
            "constant": constant,
            "hex": hex_template,
            "subsets": subsets,
            "generator_a_z": generator_a.z_coefficient,
            "generator_a_constant": generator_a.constant,
            "generator_b_z": generator_b.z_coefficient,
            "generator_b_constant": generator_b.constant,
        }
        templates.append(template)
        digest_rows.append(
            {
                "rank_A1": rank_a1,
                "rank_A2": rank_a2,
                "rank_A": hex_template["rank"],
                "A_sha256": object_sha(matrix.tolist()),
                "C_sha256": object_sha(class_coefficient.tolist()),
                "left_null_sha256": hex_template["left_null_sha256"],
                "subset_ranks": {
                    mask: entry["template"]["rank"] for mask, entry in subsets.items()
                },
            }
        )
    rank_pairs = Counter((entry["rank_A1"], entry["rank_A2"]) for entry in templates)
    ranks = Counter(entry["hex"]["rank"] for entry in templates)
    summary = {
        "rows": len(templates),
        "A_shape": [2 * dimension, dimension],
        "rank_A1_A2_distribution": {
            f"{a},{b}": count for (a, b), count in sorted(rank_pairs.items())
        },
        "rank_A_distribution": counter_json(ranks),
        "dim_ker_A_distribution": counter_json(
            Counter(dimension - entry["hex"]["rank"] for entry in templates)
        ),
        "rank_A1_equals_rank_A2_all_rows": all(a == b for a, b in rank_pairs),
        "template_sha256": object_sha(digest_rows),
    }
    return templates, summary


def build_roof(r_x: np.ndarray, r_y: np.ndarray) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    old_rows, old_summary = old.roof_rows(r_x, r_y)
    rows = []
    public = []
    for row in old_rows:
        trivial_action = old.word_action(row["s4_f_word"], r_x, r_y)
        full_action = old.block_diag([row["fbar_action"], trivial_action])
        entry = {
            **row,
            "orbit_action": row["fbar_action"],
            "trivial_action": trivial_action,
            "full_action": full_action,
        }
        rows.append(entry)
        public.append(
            {
                key: value
                for key, value in {
                    **row,
                    "orbit_action_sha256": object_sha(row["fbar_action"].tolist()),
                    "trivial_action_sha256": object_sha(trivial_action.tolist()),
                    "full_action_sha256": object_sha(full_action.tolist()),
                }.items()
                if key not in ("fbar_action",)
            }
        )
    summary = {
        **old_summary,
        "full_dimension": FULL_DIM,
        "full_target_table_sha256": object_sha(public),
    }
    return rows, {"summary": summary, "targets": public}


def gauge_census(
    theta_base: np.ndarray,
    tau_base: np.ndarray,
    rho_x: np.ndarray,
    rho_y: np.ndarray,
) -> dict[str, Any]:
    candidates = []
    for theta_signs in itertools.product((1, 2), repeat=4):
        theta = old.mm(theta_base, old.block_diag([sign * old.eye(BLOCK) for sign in theta_signs]))
        for tau_signs in itertools.product((1, 2), repeat=4):
            tau = old.mm(tau_base, old.block_diag([sign * old.eye(BLOCK) for sign in tau_signs]))
            if not np.array_equal(old.mm(theta, theta), old.eye(FULL_DIM)):
                continue
            if not np.array_equal(old.mpow(tau, 3), old.eye(FULL_DIM)):
                continue
            sigma_1 = old.mm(old.mpow(tau, 2), theta)
            sigma_2 = old.mm(theta, old.mpow(tau, 2))
            if np.array_equal(old.mm(sigma_1, sigma_1), rho_x) and np.array_equal(
                old.mm(sigma_2, sigma_2), rho_y
            ):
                candidates.append((theta_signs, tau_signs, theta, tau))
    keys = {
        (tuple(theta.flatten()), tuple(tau.flatten())): index
        for index, (_, _, theta, tau) in enumerate(candidates)
    }
    orbit_sets = set()
    stabilizers = []
    for _, _, theta, tau in candidates:
        orbit = set()
        stabilizer = 0
        for signs in itertools.product((1, 2), repeat=4):
            diagonal = old.block_diag([sign * old.eye(BLOCK) for sign in signs])
            transformed_theta = old.mm(old.mm(diagonal, theta), diagonal)
            transformed_tau = old.mm(old.mm(diagonal, tau), diagonal)
            orbit.add(keys[(tuple(transformed_theta.flatten()), tuple(transformed_tau.flatten()))])
            stabilizer += int(
                np.array_equal(transformed_theta, theta) and np.array_equal(transformed_tau, tau)
            )
        orbit_sets.add(tuple(sorted(orbit)))
        stabilizers.append(stabilizer)
    classifier = twist_classifier()
    return {
        "End_W_V": "F_3^4",
        "End_W_V_dimension": 4,
        "gauge_group_order": 16,
        "conjugation_kernel_order": 4,
        "effective_gauge_order": 4,
        "anchor_solutions": len(candidates),
        "orbit_count": len(orbit_sets),
        "orbit_sizes": sorted(len(orbit) for orbit in orbit_sets),
        "full_gauge_stabilizer_sizes": sorted(set(stabilizers)),
        "twist_classifier": classifier,
        "candidate_signs": [
            {
                "theta_source_signs": [1 if value == 1 else -1 for value in theta_signs],
                "tau_source_signs": [1 if value == 1 else -1 for value in tau_signs],
            }
            for theta_signs, tau_signs, _, _ in candidates
        ],
        "orbits": [list(orbit) for orbit in sorted(orbit_sets)],
    }


def model_data() -> tuple[dict[str, Any], dict[str, Any]]:
    prior_path = ROOT / "search/certs/vnbit_affine_gate_raw_v1_20260813.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    s_perm = old.mobius((1, 0, 1, 1))
    t_perm = old.mobius((4, 3, 1, 5))
    sigma_1_perm = old.compose(old.inv_perm(t_perm), s_perm)
    sigma_2_perm = old.compose(s_perm, old.pow_perm(t_perm, 2))
    x_perm = old.pow_perm(sigma_1_perm, 2)
    y_perm = old.pow_perm(sigma_2_perm, 2)
    r_s = old.heart_matrix(s_perm)
    r_t = old.heart_matrix(t_perm)
    r_x = old.heart_matrix(x_perm)
    r_y = old.heart_matrix(y_perm)
    theta_base_orbit = old.mat(prior["C2"]["theta_operator"])
    tau_base_orbit = old.mat(prior["C2"]["tau_operator"])
    rho_x_orbit = old.mat(prior["C2"]["rho_X"])
    rho_y_orbit = old.mat(prior["C2"]["rho_Y"])
    theta_base_full = old.block_diag([theta_base_orbit, r_s])
    tau_base_full = old.block_diag([tau_base_orbit, r_t])
    rho_x_full = old.block_diag([rho_x_orbit, r_x])
    rho_y_full = old.block_diag([rho_y_orbit, r_y])

    signatures_x = (-1, 1, -1, 1)
    signatures_y = (1, -1, -1, 1)
    constituent_actions = [
        ((signatures_x[index] * r_x) % F, (signatures_y[index] * r_y) % F)
        for index in range(4)
    ]
    hom_dimensions = [
        [hom_dimension(constituent_actions[left], constituent_actions[right]) for right in range(4)]
        for left in range(4)
    ]
    cyclic_counts = Counter()
    for coordinates in itertools.product(range(F), repeat=BLOCK):
        if any(coordinates):
            cyclic_counts[old.cyclic_dimension(np.asarray(coordinates), (r_x, r_y))] += 1
    centralizer_dimension, centralizer_digest = old.centralizer_dimension((r_x, r_y))
    c9 = {
        "P_order": len(old.perm_group((x_perm, y_perm))),
        "V7_dimension": BLOCK,
        "nonzero_cyclic_submodule_dimension_distribution": counter_json(cyclic_counts),
        "V7_irreducible_over_F3": cyclic_counts == Counter({7: 2186}),
        "End_P_V7_dimension": centralizer_dimension,
        "End_P_relation_rref_sha256": centralizer_digest,
        "V7_absolutely_irreducible": cyclic_counts == Counter({7: 2186})
        and centralizer_dimension == 1,
        "W_constituent_character_signatures_XY": [
            [signatures_x[index], signatures_y[index]] for index in range(4)
        ],
        "Hom_W_dimension_matrix": hom_dimensions,
        "pairwise_nonisomorphic": hom_dimensions
        == [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        "End_W_V_dimension": sum(hom_dimensions[index][index] for index in range(4)),
        "End_W_V_unit_group_order": 2**4,
    }
    if not c9["V7_absolutely_irreducible"] or not c9["pairwise_nonisomorphic"]:
        raise RuntimeError("C-9 family gate changed")

    gauge = gauge_census(theta_base_full, tau_base_full, rho_x_full, rho_y_full)
    if gauge["anchor_solutions"] != 16 or gauge["orbit_sizes"] != [4, 4, 4, 4]:
        raise RuntimeError("28D gauge census changed")

    p9 = np.zeros((9, 9), dtype=np.int64)
    for source, target in enumerate(t_perm):
        p9[target, source] = 1
    h2 = {
        "all_eight_V7_Jordan_types": all_jordan_types(),
        "actual_V7_trivial_character_block": h2_audit(r_t),
        "orbit_bundle_V21": h2_audit(tau_base_orbit),
        "ESCAPE_V28": h2_audit(tau_base_full),
        "contrast_V9_permutation_block_system": h2_audit(p9),
    }
    if h2["ESCAPE_V28"]["H2_dimension"] < 1:
        raise RuntimeError("ESCAPE-28 entrance condition disappeared")

    orbit_components = {}
    orbit_templates = {}
    orbit_signs = {"+": (2, 2, 1), "-": (1, 1, 2)}
    roof_rows, roof_public = build_roof(r_x, r_y)
    for eps, signs in orbit_signs.items():
        theta = old.mm(theta_base_orbit, old.block_diag([sign * old.eye(BLOCK) for sign in signs]))
        tau = tau_base_orbit.copy()
        cohomology = component_cohomology(
            theta,
            tau,
            x_perm,
            y_perm,
            s_perm,
            t_perm,
            old.block_diag([r_x, r_x, r_x]),
            old.block_diag([r_y, r_y, r_y]),
        )
        templates, template_summary = component_templates(
            theta, tau, roof_rows, "orbit_action", 3
        )
        orbit_components[eps] = {
            "dimension": ORBIT_DIM,
            "theta_matrix": theta.tolist(),
            "tau_matrix": tau.tolist(),
            "theta_source_signs_F3": list(signs),
            "cohomology": cohomology,
            "template_gate": template_summary,
        }
        orbit_templates[eps] = templates

    trivial_components = {}
    trivial_templates = {}
    for eta, sign in (("+", 1), ("-", 2)):
        theta = (sign * r_s) % F
        tau = r_t.copy()
        cohomology = component_cohomology(
            theta, tau, x_perm, y_perm, s_perm, t_perm, r_x, r_y
        )
        templates, template_summary = component_templates(
            theta, tau, roof_rows, "trivial_action", 1
        )
        trivial_components[eta] = {
            "dimension": TRIVIAL_DIM,
            "theta_matrix": theta.tolist(),
            "tau_matrix": tau.tolist(),
            "theta_source_sign_F3": sign,
            "cohomology": cohomology,
            "template_gate": template_summary,
        }
        trivial_templates[eta] = templates

    windows = []
    for eps in ("+", "-"):
        for eta in ("+", "-"):
            orbit = orbit_components[eps]
            trivial = trivial_components[eta]
            theta = old.block_diag([old.mat(orbit["theta_matrix"]), old.mat(trivial["theta_matrix"])])
            tau = old.block_diag([old.mat(orbit["tau_matrix"]), old.mat(trivial["tau_matrix"])])
            symbols = marked_symbols(theta, tau)
            anchor_x = symbols["x"].action
            anchor_y = symbols["y"].action
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
            full_h1_order = orbit["cohomology"]["H1_order"] * trivial["cohomology"]["H1_order"]
            surjective_count = (
                orbit["cohomology"]["surjective_component_class_count"]
                * trivial["cohomology"]["surjective_component_class_count"]
            )
            window_id = f"eps={eps},eta={eta}"
            windows.append(
                {
                    "window_id": window_id,
                    "eps": eps,
                    "eta": eta,
                    "marking_version": "escape28-monomial/v1",
                    "theta_source_signs_F3": orbit["theta_source_signs_F3"]
                    + [trivial["theta_source_sign_F3"]],
                    "theta_source_signs_integer": [
                        1 if value == 1 else -1
                        for value in orbit["theta_source_signs_F3"]
                        + [trivial["theta_source_sign_F3"]]
                    ],
                    "tau_source_signs": [1, 1, 1, 1],
                    "theta_matrix": theta.tolist(),
                    "tau_matrix": tau.tolist(),
                    "pure_anchor": {
                        "A1_holds": bool(np.array_equal(anchor_x, rho_x_full)),
                        "A2_holds": bool(np.array_equal(anchor_y, rho_y_full)),
                        "residual_rank_A1": old.rank((anchor_x - rho_x_full) % F),
                        "residual_rank_A2": old.rank((anchor_y - rho_y_full) % F),
                        "rho_X_block_signs": [-1, 1, -1, 1],
                        "rho_Y_block_signs": [1, -1, -1, 1],
                        "trivial_character_block_signs_XY": [1, 1],
                    },
                    "B_matrix_sha256": object_sha(theta[14:21, 14:21].tolist()),
                    "trivial_theta_matrix_sha256": object_sha(theta[21:28, 21:28].tolist()),
                    "dim_ker_I_plus_theta": orbit["cohomology"]["dim_ker_I_plus_theta"]
                    + trivial["cohomology"]["dim_ker_I_plus_theta"],
                    "dim_ker_I_plus_tau_plus_tau2": orbit["cohomology"][
                        "dim_ker_I_plus_tau_plus_tau2"
                    ]
                    + trivial["cohomology"]["dim_ker_I_plus_tau_plus_tau2"],
                    "H1_order": full_h1_order,
                    "surjective_class_count": surjective_count,
                    "SURJ_LIN_factorisation": {
                        "barW_irreducible_components": [ORBIT_DIM, TRIVIAL_DIM],
                        "orbit_H1_order": orbit["cohomology"]["H1_order"],
                        "orbit_H1_barW_order": orbit["cohomology"]["SL_RE"]["H1_barW_order"],
                        "orbit_surjective_count": orbit["cohomology"][
                            "surjective_component_class_count"
                        ],
                        "trivial_H1_order": trivial["cohomology"]["H1_order"],
                        "trivial_H1_barW_order": trivial["cohomology"]["SL_RE"]["H1_barW_order"],
                        "trivial_surjective_count": trivial["cohomology"][
                            "surjective_component_class_count"
                        ],
                        "formula": "(H1_A-infl H1_barW_A)*(H1_B-infl H1_barW_B)",
                    },
                    "template_gate": {
                        "A_shape": [56, 28],
                        "rank_A1_A2_distribution": counter_json(Counter(zip(rank_a1, rank_a2))),
                        "rank_A_distribution": counter_json(Counter(rank_a)),
                        "dim_ker_A_distribution": counter_json(
                            Counter(FULL_DIM - value for value in rank_a)
                        ),
                        "rank_A1_equals_rank_A2_all_rows": rank_a1 == rank_a2,
                        "factorisation": "orbit 21D direct sum trivial-character 7D",
                        "component_template_sha256": [
                            orbit["template_gate"]["template_sha256"],
                            trivial["template_gate"]["template_sha256"],
                        ],
                    },
                }
            )
    if not all(
        entry["pure_anchor"]["A1_holds"] and entry["pure_anchor"]["A2_holds"]
        for entry in windows
    ):
        raise RuntimeError("28D pure anchor gate changed")

    sources = (
        "ops/inbox_codex/sol_task_133_escape28.txt",
        "docs/notes/entangled972_reading_v1.md",
        "docs/notes/vnbit_compact_route_v3.md",
        "docs/notes/bu_s35_embedding_v1.md",
        "docs/week1-定義ノート.md",
        "search/vnbit_compact_mainrun_v3.py",
        "search/certs/vnbit_affine_gate_raw_v1_20260813.json",
        "certificates/S4.v2.json",
        "certificates/K3.v1.json",
        "certificates/K9.v1.json",
    )
    preflight = {
        "schema": "escape28_preflight/v1",
        "generated_by": {
            "script": "search/escape28_mainrun_v1.py",
            "script_sha256": file_sha(Path(__file__)),
            "reused_engine": "search/vnbit_compact_mainrun_v3.py",
            "reused_engine_sha256": file_sha(ROOT / "search/vnbit_compact_mainrun_v3.py"),
            "runtime": f"Python {os.sys.version.split()[0]} + NumPy {np.__version__}",
        },
        "source_sha256": {name: file_sha(ROOT / name) for name in sources},
        "entry_H2": h2,
        "C9": c9,
        "gauge": gauge,
        "components": {
            "orbit_bundle": orbit_components,
            "trivial_character": trivial_components,
        },
        "windows": windows,
        "roof": roof_public,
        "universe": {
            "window_count": 4,
            "surjective_class_counts": {
                entry["window_id"]: entry["surjective_class_count"] for entry in windows
            },
            "roof_rows_per_class": 324,
            "total_surjective_classes": sum(entry["surjective_class_count"] for entry in windows),
            "total_full_rows": sum(entry["surjective_class_count"] * 324 for entry in windows),
        },
        "stage_boundary": {
            "stage": "template_gate_before_preregistration",
            "measurement_outcomes_opened": 0,
            "lift_rows_opened": 0,
        },
        "noncontact": {
            "u": False,
            "c": False,
            "sealed_three_quantities": False,
            "sealed_K5": False,
            "blind_measurement_outcomes": False,
        },
    }
    runtime = {
        "roof_rows": roof_rows,
        "orbit_templates": orbit_templates,
        "trivial_templates": trivial_templates,
    }
    return preflight, runtime


def measure_component(
    label: str,
    component: dict[str, Any],
    templates: list[dict[str, Any]],
    roof_rows: list[dict[str, Any]],
    checkpoint_update,
) -> tuple[dict[str, Any], list[list[tuple[tuple[int, ...], int, int, bool]]]]:
    classes = [
        entry for entry in component["cohomology"]["classes"] if entry["surjective_component"]
    ]
    outcomes_by_class = []
    summaries = []
    obstruction_distribution = Counter()
    solution_distribution = Counter()
    generation_distribution = Counter()
    joint_distribution = Counter()
    sparse_nonzero = []
    digest = hashlib.sha256()
    for class_position, entry in enumerate(classes):
        representative = np.asarray(entry["representative"], dtype=np.int64)
        outcomes = []
        class_nonzero = 0
        class_generation_absent = 0
        class_lifts = 0
        class_generation = Counter()
        for row, template in zip(roof_rows, templates):
            rhs = -(
                template["class_coefficient"] @ representative + template["constant"]
            ) % F
            obstruction = tuple(
                int(value) for value in (template["hex"]["left_null"] @ rhs) % F
            )
            obstruction_zero = not any(obstruction)
            total = old.system_count(template["hex"], rhs)
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
                            % F
                        )
                        rhs_parts.append(
                            -(
                                template["generator_b_z"][section, :] @ representative
                                + template["generator_b_constant"][section]
                            )
                            % F
                        )
                    bad_counts[mask] = old.system_count(
                        subset["template"], np.concatenate(rhs_parts)
                    )
                union = sum(
                    count if int(mask).bit_count() % 2 else -count
                    for mask, count in bad_counts.items()
                )
                generating_count = total - union
            else:
                generating_count = 0
            if generating_count < 0 or generating_count > total:
                raise RuntimeError("generation inclusion-exclusion escaped solution set")
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
    result = {
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
    }
    return result, outcomes_by_class


def combine_window(
    window: dict[str, Any],
    orbit_component: dict[str, Any],
    trivial_component: dict[str, Any],
    orbit_outcomes: list[list[tuple[tuple[int, ...], int, int, bool]]],
    trivial_outcomes: list[list[tuple[tuple[int, ...], int, int, bool]]],
    roof_rows: list[dict[str, Any]],
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
            obstruction_nonzero_count = 0
            generation_absent_count = 0
            theta_masks = [0] * 54
            class_generation = Counter()
            for row, orbit_value, trivial_value in zip(
                roof_rows,
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
                obstruction_nonzero_count += int(not obstruction_zero)
                generation_absent_count += int(generating_count == 0)
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
                    roof_rows,
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
                    "obstruction_nonzero_rows": obstruction_nonzero_count,
                    "generation_absent_rows": generation_absent_count,
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
    if class_position != window["surjective_class_count"]:
        raise RuntimeError("full SURJ-LIN Cartesian class count changed")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("preflight", "measure"), required=True)
    parser.add_argument(
        "--preflight-output",
        default="search/certs/escape28_preflight_v1_20260813.json",
    )
    parser.add_argument(
        "--prereg",
        default="search/certs/escape28_prereg_v1_20260813.json",
    )
    parser.add_argument(
        "--output",
        default="search/certs/escape28_mainrun_raw_v1_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/escape28_mainrun_v1_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=1800)
    args = parser.parse_args()
    preflight_path = ROOT / args.preflight_output
    prereg_path = ROOT / args.prereg
    output_path = ROOT / args.output
    checkpoint_path = ROOT / args.checkpoint
    began = time.monotonic()
    state: dict[str, Any] = {
        "schema": "escape28_mainrun_checkpoint/v1",
        "mode": args.mode,
        "stage": "start",
        "complete": False,
    }
    atomic_json(checkpoint_path, state)

    def update(stage: str, **fields: object) -> None:
        state.update(
            stage=stage,
            elapsed_ms=int(1000 * (time.monotonic() - began)),
            **fields,
        )
        atomic_json(checkpoint_path, state)

    def timeout() -> None:
        if not state.get("complete"):
            update("hard_timeout")
            os._exit(124)

    alarm = threading.Timer(args.hard_timeout_seconds, timeout)
    alarm.daemon = True
    alarm.start()
    try:
        preflight_rebuilt, runtime = model_data()
        if args.mode == "preflight":
            preflight_rebuilt["run_id"] = "escape28-preflight-" + datetime.now(
                timezone.utc
            ).strftime("%Y%m%dT%H%M%SZ")
            atomic_json(preflight_path, preflight_rebuilt)
            update(
                "preflight_complete",
                complete=True,
                output_sha256=file_sha(preflight_path),
                windows=4,
                lift_outcomes_opened=0,
            )
            return 0

        preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
        prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
        if prereg["preflight_sha256"] != file_sha(preflight_path):
            raise RuntimeError("preregistration is not bound to the preflight")
        if prereg["producer_sha256"] != file_sha(Path(__file__)):
            raise RuntimeError("preregistration is not bound to this producer")
        if prereg.get("blind_before_measurement") is not True:
            raise RuntimeError("blind preregistration declaration missing")
        if prereg.get("lift_outcomes_opened_before_freeze") != 0:
            raise RuntimeError("preregistration boundary was not blind")
        rebuilt_without_run = preflight_rebuilt
        loaded_without_run = {key: value for key, value in preflight.items() if key != "run_id"}
        # JSON turns numeric object keys into strings.  Normalize both sides
        # before hashing so a read-back does not change sort order (for
        # example, the m mod 18 distribution has keys 0,...,17).
        rebuilt_canonical = json.loads(json.dumps(rebuilt_without_run))
        loaded_canonical = json.loads(json.dumps(loaded_without_run))
        if object_sha(rebuilt_canonical) != object_sha(loaded_canonical):
            raise RuntimeError("preflight reconstruction changed before measurement")
        if prereg["universe"] != preflight["universe"]:
            raise RuntimeError("preregistered universe differs from preflight")
        expected_gates = {
            entry["window_id"]: entry["template_gate"] for entry in preflight["windows"]
        }
        if prereg["template_gates"] != expected_gates:
            raise RuntimeError("preregistered template gate differs from preflight")
        update("preregistration_bound", prereg_sha256=file_sha(prereg_path))

        component_results = {"orbit_bundle": {}, "trivial_character": {}}
        component_runtime: dict[str, dict[str, Any]] = {
            "orbit_bundle": {},
            "trivial_character": {},
        }
        for eps in ("+", "-"):
            result, outcomes = measure_component(
                f"orbit:{eps}",
                preflight["components"]["orbit_bundle"][eps],
                runtime["orbit_templates"][eps],
                runtime["roof_rows"],
                update,
            )
            component_results["orbit_bundle"][eps] = result
            component_runtime["orbit_bundle"][eps] = outcomes
        for eta in ("+", "-"):
            result, outcomes = measure_component(
                f"trivial:{eta}",
                preflight["components"]["trivial_character"][eta],
                runtime["trivial_templates"][eta],
                runtime["roof_rows"],
                update,
            )
            component_results["trivial_character"][eta] = result
            component_runtime["trivial_character"][eta] = outcomes

        per_window = []
        for window in preflight["windows"]:
            eps = window["eps"]
            eta = window["eta"]
            per_window.append(
                combine_window(
                    window,
                    preflight["components"]["orbit_bundle"][eps],
                    preflight["components"]["trivial_character"][eta],
                    component_runtime["orbit_bundle"][eps],
                    component_runtime["trivial_character"][eta],
                    runtime["roof_rows"],
                    update,
                )
            )
        total_rows = sum(entry["evaluated_full_rows"] for entry in per_window)
        nonzero_count = sum(
            len(entry["nonzero_obstruction_rows"]) for entry in per_window
        )
        generation_absent_count = sum(
            len(entry["generation_absent_rows"]) for entry in per_window
        )
        all_obstruction_zero = nonzero_count == 0
        result = {
            "schema": "escape28_mainrun/v1",
            "run_id": "escape28-mainrun-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "generated_by": preflight["generated_by"],
            "inputs": {
                "preflight": args.preflight_output,
                "preflight_sha256": file_sha(preflight_path),
                "preregistration": args.prereg,
                "preregistration_sha256": file_sha(prereg_path),
            },
            "entry_H2": preflight["entry_H2"],
            "C9": preflight["C9"],
            "gauge": preflight["gauge"],
            "roof": preflight["roof"],
            "component_factorisation": {
                "mathematical_statement": (
                    "The full LIFT-AFF equations and GEN-AFF constituent tests split "
                    "as the direct sum of the 21D orbit bundle and the 7D trivial-"
                    "character constituent. Full obstruction vanishing is the "
                    "conjunction, and solution/generating counts are products."
                ),
                "component_results": component_results,
            },
            "per_window": per_window,
            "full_campaign": {
                "windows": 4,
                "surjective_classes": sum(entry["surjective_class_count"] for entry in per_window),
                "evaluated_full_rows": total_rows,
                "expected_full_rows": preflight["universe"]["total_full_rows"],
                "nonzero_obstruction_row_count": nonzero_count,
                "generation_absent_row_count": generation_absent_count,
                "all_obstruction_classes_zero": all_obstruction_zero,
                "all_rows_have_generating_solution": generation_absent_count == 0,
                "stop_rule_triggered": (
                    "H²≠0 下の全消滅" if all_obstruction_zero else "nonzero obstruction observed"
                ),
                "next_step_boundary": (
                    "stop and report; a new vanishing theorem is needed"
                    if all_obstruction_zero
                    else "record nonzero rows before any interpretation"
                ),
            },
            "A_shape": {
                "rows": 56,
                "cols": 28,
                "rank_A1_equals_rank_A2_all_rows": all(
                    entry["template_gate"]["rank_A1_equals_rank_A2_all_rows"]
                    for entry in preflight["windows"]
                ),
            },
            "isolated": {
                "N_E_isolated": "UNKNOWN",
                "gate_policy": (
                    "C-4-prime permits measurement; no image-size value is interpreted "
                    "as an isolated-window type statement without an isolatedness proof"
                ),
                "escape28_gap": "open",
            },
            "endgame_scope": (
                "gentle side only. Elevation of a B-branch countercandidate requires "
                "the B4 layer PENT_W-PASS and then FAKE-KILL^{B4}/U-10. No finite-"
                "depth B-type identification is made."
            ),
            "noncontact": preflight["noncontact"],
            "stage_boundary": {
                "stage": "escape28_full_campaign_complete",
                "windows": 4,
                "surjective_classes": sum(entry["surjective_class_count"] for entry in per_window),
                "full_rows": total_rows,
            },
            "status_note": "raw machine values and distributions; no type adjudication",
        }
        if total_rows != preflight["universe"]["total_full_rows"]:
            raise RuntimeError("full row universe was not exhausted")
        atomic_json(output_path, result)
        update(
            "complete",
            complete=True,
            output_sha256=file_sha(output_path),
            full_rows=total_rows,
            nonzero_obstruction_rows=nonzero_count,
        )
        return 0
    except BaseException as error:
        update("exception", error_type=type(error).__name__, error_message=str(error))
        raise
    finally:
        alarm.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
