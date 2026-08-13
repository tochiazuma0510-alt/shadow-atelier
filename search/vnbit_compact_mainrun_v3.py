#!/usr/bin/env python3
"""Task 132 producer for the two-window compact v3 measurement.

Modes are deliberately separated.  ``preflight`` computes C-2', C-9,
P-vNC3-2, SL-RE, and the 324-element roof without opening any lift outcome.
``measure`` requires a separately frozen preregistration and then evaluates
both windows, every surjective marked class, and every roof row.
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


ROOT = Path(__file__).resolve().parents[1]
F = 3
DIM_H = 7
DIM_V = 21
CHARS = ((1, 0), (0, 1), (1, 1))


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def value_sha(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def ident_perm(degree: int) -> tuple[int, ...]:
    return tuple(range(degree))


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Paper product / function composition: left after right."""
    return tuple(left[right[index]] for index in range(len(left)))


def inv_perm(value: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * len(value)
    for old, new in enumerate(value):
        answer[new] = old
    return tuple(answer)


def pow_perm(value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    if exponent < 0:
        return pow_perm(inv_perm(value), -exponent)
    answer = ident_perm(len(value))
    factor = value
    while exponent:
        if exponent & 1:
            answer = compose(answer, factor)
        factor = compose(factor, factor)
        exponent >>= 1
    return answer


def perm_order(value: tuple[int, ...]) -> int:
    answer = ident_perm(len(value))
    for exponent in range(1, 10000):
        answer = compose(answer, value)
        if answer == ident_perm(len(value)):
            return exponent
    raise RuntimeError("permutation order bound")


def perm_group(generators: tuple[tuple[int, ...], ...]) -> list[tuple[int, ...]]:
    steps = generators + tuple(inv_perm(value) for value in generators)
    answer = [ident_perm(len(generators[0]))]
    known = {answer[0]}
    for old in answer:
        for step in steps:
            new = compose(old, step)
            if new not in known:
                known.add(new)
                answer.append(new)
    return answer


def gf8_mul(left: int, right: int) -> int:
    raw = 0
    for bit in range(3):
        if (right >> bit) & 1:
            raw ^= left << bit
    for bit in (4, 3):
        if (raw >> bit) & 1:
            raw ^= 0b1011 << (bit - 3)
    return raw


def gf8_inv(value: int) -> int:
    return next(test for test in range(1, 8) if gf8_mul(value, test) == 1)


def mobius(matrix: tuple[int, int, int, int]) -> tuple[int, ...]:
    a, b, c, d = matrix
    answer = [0 if c == 0 else 1 + gf8_mul(a, gf8_inv(c))]
    for value in range(8):
        top = gf8_mul(a, value) ^ b
        bottom = gf8_mul(c, value) ^ d
        answer.append(0 if bottom == 0 else 1 + gf8_mul(top, gf8_inv(bottom)))
    return tuple(answer)


def mat(value: object) -> np.ndarray:
    return np.asarray(value, dtype=np.int64) % F


def eye(size: int) -> np.ndarray:
    return np.eye(size, dtype=np.int64)


def mm(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return (left @ right) % F


def mpow(value: np.ndarray, exponent: int) -> np.ndarray:
    if exponent < 0:
        return mpow(minv(value), -exponent)
    answer = eye(value.shape[0])
    factor = value.copy()
    while exponent:
        if exponent & 1:
            answer = mm(answer, factor)
        factor = mm(factor, factor)
        exponent >>= 1
    return answer


def rref(value: np.ndarray) -> tuple[np.ndarray, list[int]]:
    work = value.copy() % F
    pivot_row = 0
    pivots: list[int] = []
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[pivot_row:, column])
        if not len(choices):
            continue
        choice = pivot_row + int(choices[0])
        work[[pivot_row, choice]] = work[[choice, pivot_row]]
        if work[pivot_row, column] == 2:
            work[pivot_row] = (2 * work[pivot_row]) % F
        for row in range(work.shape[0]):
            if row != pivot_row and work[row, column]:
                work[row] = (work[row] - work[row, column] * work[pivot_row]) % F
        pivots.append(column)
        pivot_row += 1
        if pivot_row == work.shape[0]:
            break
    return work, pivots


def rank(value: np.ndarray) -> int:
    return len(rref(value)[1])


def nullspace(value: np.ndarray) -> np.ndarray:
    reduced, pivots = rref(value)
    free = [column for column in range(value.shape[1]) if column not in pivots]
    answer = np.zeros((value.shape[1], len(free)), dtype=np.int64)
    for output, free_column in enumerate(free):
        answer[free_column, output] = 1
        for row, pivot in enumerate(pivots):
            answer[pivot, output] = (-reduced[row, free_column]) % F
    return answer


def minv(value: np.ndarray) -> np.ndarray:
    size = value.shape[0]
    augmented = np.concatenate((value.copy() % F, eye(size)), axis=1)
    reduced, pivots = rref(augmented)
    if pivots[:size] != list(range(size)):
        raise RuntimeError("singular matrix")
    return reduced[:, size:] % F


def extend_columns(base: np.ndarray, candidates: np.ndarray) -> np.ndarray:
    answer = base.copy()
    current = rank(answer) if answer.shape[1] else 0
    for column in range(candidates.shape[1]):
        trial = np.concatenate((answer, candidates[:, column : column + 1]), axis=1)
        trial_rank = rank(trial)
        if trial_rank > current:
            answer = trial
            current = trial_rank
    return answer


def solve_columns(base: np.ndarray, vector: np.ndarray) -> np.ndarray:
    augmented = np.concatenate((base, vector.reshape(-1, 1)), axis=1)
    reduced, pivots = rref(augmented)
    width = base.shape[1]
    for row in range(reduced.shape[0]):
        if not np.any(reduced[row, :width]) and reduced[row, width]:
            raise RuntimeError("vector outside column span")
    answer = np.zeros(width, dtype=np.int64)
    for row, pivot in enumerate(pivots):
        if pivot < width:
            answer[pivot] = reduced[row, width]
    return answer


def heart_matrix(permutation: tuple[int, ...]) -> np.ndarray:
    answer = np.zeros((7, 7), dtype=np.int64)
    for column in range(7):
        vector = np.zeros(9, dtype=np.int64)
        vector[permutation[column]] += 1
        vector[permutation[8]] -= 1
        coefficients = vector[:8] % F
        for row in range(7):
            answer[row, column] = (coefficients[row] - coefficients[7]) % F
    return answer


def block_diag(blocks: list[np.ndarray]) -> np.ndarray:
    size = sum(block.shape[0] for block in blocks)
    answer = np.zeros((size, size), dtype=np.int64)
    offset = 0
    for block in blocks:
        length = block.shape[0]
        answer[offset : offset + length, offset : offset + length] = block
        offset += length
    return answer % F


def cyclic_dimension(seed: np.ndarray, generators: tuple[np.ndarray, ...]) -> int:
    columns = np.zeros((len(seed), 0), dtype=np.int64)
    queue = [seed]
    while queue:
        vector = queue.pop()
        trial = np.concatenate((columns, vector.reshape(-1, 1)), axis=1)
        if rank(trial) == columns.shape[1]:
            continue
        columns = trial
        for generator in generators:
            queue.append((generator @ vector) % F)
    return columns.shape[1]


def extended_operator(
    base: np.ndarray,
    destinations: tuple[int, int, int],
    signs: tuple[int, int, int],
) -> np.ndarray:
    answer = np.zeros((21, 21), dtype=np.int64)
    for source, target in enumerate(destinations):
        answer[7 * target : 7 * target + 7, 7 * source : 7 * source + 7] = (
            signs[source] * base
        ) % F
    return answer


def module_pair_action(
    p_action: np.ndarray, g3_abelian: tuple[int, int]
) -> np.ndarray:
    blocks = []
    for character in CHARS:
        sign = 2 if sum(a * b for a, b in zip(character, g3_abelian)) % 2 else 1
        blocks.append((sign * p_action) % F)
    return block_diag(blocks)


def word_action(word: list[list[Any]], x: np.ndarray, y: np.ndarray) -> np.ndarray:
    answer = eye(x.shape[0])
    for letter, exponent in word:
        generator = x if letter == "x" else y
        answer = mm(answer, mpow(generator, int(exponent)))
    return answer


def word_parity(word: list[list[Any]]) -> tuple[int, int]:
    values = [0, 0]
    for letter, exponent in word:
        values[0 if letter == "x" else 1] += int(exponent)
    return values[0] % 2, values[1] % 2


def centralizer_dimension(generators: tuple[np.ndarray, ...]) -> tuple[int, str]:
    equations = []
    for generator in generators:
        for row in range(7):
            for column in range(7):
                equation = np.zeros(49, dtype=np.int64)
                for middle in range(7):
                    equation[7 * row + middle] += generator[middle, column]
                    equation[7 * middle + column] -= generator[row, middle]
                equations.append(equation % F)
    relation = np.asarray(equations, dtype=np.int64)
    reduced, _ = rref(relation)
    canonical = reduced[np.any(reduced, axis=1)]
    return 49 - rank(relation), value_sha(canonical.tolist())


def cocycle_graph(
    x_perm: tuple[int, ...],
    y_perm: tuple[int, ...],
    rho_x: np.ndarray,
    rho_y: np.ndarray,
) -> dict[str, Any]:
    dimension = rho_x.shape[0]
    identity = ident_perm(len(x_perm))
    zero = np.zeros((dimension, 2 * dimension), dtype=np.int64)
    generator_expressions = []
    for which in range(2):
        expression = zero.copy()
        expression[:, which * dimension : (which + 1) * dimension] = eye(dimension)
        generator_expressions.append(expression)
    elements = [identity]
    data: dict[tuple[int, ...], tuple[np.ndarray, np.ndarray]] = {
        identity: (eye(dimension), zero)
    }
    constraint_chunks = []
    collision_count = 0
    for old in elements:
        old_rho, old_expression = data[old]
        for generator, generator_rho, generator_expression in (
            (x_perm, rho_x, generator_expressions[0]),
            (y_perm, rho_y, generator_expressions[1]),
        ):
            new = compose(old, generator)
            new_rho = mm(old_rho, generator_rho)
            new_expression = (old_expression + mm(old_rho, generator_expression)) % F
            if new in data:
                if not np.array_equal(data[new][0], new_rho):
                    raise RuntimeError("Cayley representation mismatch")
                constraint_chunks.append((new_expression - data[new][1]) % F)
                collision_count += 1
            else:
                data[new] = (new_rho, new_expression)
                elements.append(new)
    constraints = np.concatenate(constraint_chunks, axis=0)
    reduced, _ = rref(constraints)
    canonical = reduced[np.any(reduced, axis=1)]
    return {
        "elements": elements,
        "data": data,
        "constraints": constraints,
        "relation_rank": rank(constraints),
        "relation_rref_sha256": value_sha(canonical.tolist()),
        "positive_edges": 2 * len(elements),
        "collision_edges": collision_count,
    }


def q_action_on_p_h1(
    graph: dict[str, Any],
    x_perm: tuple[int, ...],
    y_perm: tuple[int, ...],
    q_perm: tuple[int, ...],
    q_matrix: np.ndarray,
    full_basis: np.ndarray,
    h_basis: np.ndarray,
    b_dimension: int,
) -> np.ndarray:
    q_inverse = inv_perm(q_perm)
    x_conjugate = compose(q_inverse, compose(x_perm, q_perm))
    y_conjugate = compose(q_inverse, compose(y_perm, q_perm))
    x_expression = graph["data"][x_conjugate][1]
    y_expression = graph["data"][y_conjugate][1]
    action = np.concatenate(
        (mm(q_matrix, x_expression), mm(q_matrix, y_expression)), axis=0
    )
    columns = []
    for column in range(h_basis.shape[1]):
        transformed = (action @ h_basis[:, column]) % F
        coordinates = solve_columns(full_basis, transformed)
        columns.append(coordinates[b_dimension:])
    return np.asarray(columns, dtype=np.int64).T % F


def sl_re(
    x_perm: tuple[int, ...],
    y_perm: tuple[int, ...],
    s_perm: tuple[int, ...],
    t_perm: tuple[int, ...],
    p_x: np.ndarray,
    p_y: np.ndarray,
    theta: np.ndarray,
    tau: np.ndarray,
) -> dict[str, Any]:
    pure_x = block_diag([p_x, p_x, p_x])
    pure_y = block_diag([p_y, p_y, p_y])
    graph = cocycle_graph(x_perm, y_perm, pure_x, pure_y)
    z_basis = nullspace(graph["constraints"])
    coboundaries = np.concatenate((eye(21) - pure_x, eye(21) - pure_y), axis=0) % F
    b_basis = coboundaries[:, rref(coboundaries)[1]]
    full = extend_columns(b_basis, z_basis)
    h_basis = full[:, b_basis.shape[1] :]
    action_theta = q_action_on_p_h1(
        graph, x_perm, y_perm, s_perm, theta, full, h_basis, b_basis.shape[1]
    )
    action_tau = q_action_on_p_h1(
        graph, x_perm, y_perm, t_perm, tau, full, h_basis, b_basis.shape[1]
    )
    invariant_conditions = np.concatenate(
        (action_theta - eye(h_basis.shape[1]), action_tau - eye(h_basis.shape[1])),
        axis=0,
    ) % F
    invariant_dimension = h_basis.shape[1] - rank(invariant_conditions)
    return {
        "method": (
            "Lyndon-Hochschild-Serre with normal P; P relations are generated "
            "from all positive Cayley-graph edge collisions, not hand fixed"
        ),
        "P_order": len(graph["elements"]),
        "P_positive_edges": graph["positive_edges"],
        "P_collision_edges": graph["collision_edges"],
        "P_relation_rank": graph["relation_rank"],
        "P_relation_rref_sha256": graph["relation_rref_sha256"],
        "Z1_P_V_dimension": z_basis.shape[1],
        "B1_P_V_dimension": b_basis.shape[1],
        "H1_P_V_dimension": h_basis.shape[1],
        "H1_P_V_theta_action": action_theta.tolist(),
        "H1_P_V_tau_action": action_tau.tolist(),
        "H1_P_V_Q3_invariant_dimension": invariant_dimension,
        "V_P_invariant_dimension": 0,
        "H1_barW_dimension": invariant_dimension,
        "H1_barW_order": F**invariant_dimension,
        "inflated_Z1_barW_dimension": 21 + invariant_dimension,
        "inflated_Z1_barW_sha256": value_sha(coboundaries.tolist()),
    }


def gamma_classes(theta: np.ndarray, tau: np.ndarray) -> dict[str, Any]:
    condition = np.zeros((42, 42), dtype=np.int64)
    condition[:21, :21] = (eye(21) + theta) % F
    condition[21:, 21:] = (eye(21) + tau + mm(tau, tau)) % F
    z_basis = nullspace(condition)
    coboundaries = np.concatenate((eye(21) - theta, eye(21) - tau), axis=0) % F
    b_basis = coboundaries[:, rref(coboundaries)[1]]
    full = extend_columns(b_basis, z_basis)
    h_basis = full[:, b_basis.shape[1] :]
    representatives = []
    for coordinates in itertools.product(range(F), repeat=h_basis.shape[1]):
        vector = (h_basis @ np.asarray(coordinates, dtype=np.int64)) % F
        representatives.append((tuple(int(x) for x in vector), tuple(coordinates)))
    representatives.sort()
    classes = []
    for index, (vector, coordinates) in enumerate(representatives):
        classes.append(
            {
                "class_index": index,
                "quotient_coordinates": list(coordinates),
                "representative": list(vector),
                "surjective": any(vector),
            }
        )
    return {
        "condition_rank": rank(condition),
        "condition_rref_sha256": value_sha(rref(condition)[0].tolist()),
        "Z1_dimension": z_basis.shape[1],
        "B1_dimension": b_basis.shape[1],
        "H1_dimension": h_basis.shape[1],
        "H1_order": F**h_basis.shape[1],
        "class_basis_sha256": value_sha(h_basis.tolist()),
        "classes": classes,
    }


def sign_pattern(value: np.ndarray, base: np.ndarray) -> list[int]:
    answer = []
    for block in range(3):
        piece = value[7 * block : 7 * block + 7, 7 * block : 7 * block + 7]
        if np.array_equal(piece, base):
            answer.append(1)
        elif np.array_equal(piece, (-base) % F):
            answer.append(-1)
        else:
            raise RuntimeError("non-scalar block pattern")
    return answer


def gauge_data(
    theta_base: np.ndarray, tau_base: np.ndarray, rho_x: np.ndarray, rho_y: np.ndarray
) -> dict[str, Any]:
    candidates = []
    for theta_signs in itertools.product((1, 2), repeat=3):
        theta = mm(theta_base, block_diag([sign * eye(7) for sign in theta_signs]))
        for tau_signs in itertools.product((1, 2), repeat=3):
            tau = mm(tau_base, block_diag([sign * eye(7) for sign in tau_signs]))
            if not np.array_equal(mm(theta, theta), eye(21)):
                continue
            if not np.array_equal(mpow(tau, 3), eye(21)):
                continue
            sigma_1 = mm(mpow(tau, 2), theta)
            sigma_2 = mm(theta, mpow(tau, 2))
            if np.array_equal(mm(sigma_1, sigma_1), rho_x) and np.array_equal(
                mm(sigma_2, sigma_2), rho_y
            ):
                candidates.append((theta_signs, tau_signs, theta, tau))
    keys = {
        (tuple(theta.flatten()), tuple(tau.flatten())): index
        for index, (_, _, theta, tau) in enumerate(candidates)
    }
    orbit_sets = set()
    stabilizer_sizes = []
    for _, _, theta, tau in candidates:
        orbit = set()
        stabilizer = 0
        for signs in itertools.product((1, 2), repeat=3):
            diagonal = block_diag([sign * eye(7) for sign in signs])
            transformed_theta = mm(mm(diagonal, theta), diagonal)
            transformed_tau = mm(mm(diagonal, tau), diagonal)
            key = (tuple(transformed_theta.flatten()), tuple(transformed_tau.flatten()))
            orbit.add(keys[key])
            if np.array_equal(transformed_theta, theta) and np.array_equal(
                transformed_tau, tau
            ):
                stabilizer += 1
        orbit_sets.add(tuple(sorted(orbit)))
        stabilizer_sizes.append(stabilizer)
    return {
        "End_W_V": "F_3^3",
        "gauge_group_order": 8,
        "effective_gauge_order": 4,
        "anchor_solutions": len(candidates),
        "orbit_count": len(orbit_sets),
        "orbit_sizes": sorted(len(orbit) for orbit in orbit_sets),
        "full_gauge_stabilizer_sizes": sorted(set(stabilizer_sizes)),
        "H1_S3_F2_3_order": 2,
        "candidate_signs": [
            {
                "theta_source_signs": [1 if x == 1 else -1 for x in theta_signs],
                "tau_source_signs": [1 if x == 1 else -1 for x in tau_signs],
            }
            for theta_signs, tau_signs, _, _ in candidates
        ],
        "orbits": [list(orbit) for orbit in sorted(orbit_sets)],
    }


def roof_rows(r_x: np.ndarray, r_y: np.ndarray) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    s4_cert = json.loads((ROOT / "certificates/S4.v2.json").read_text(encoding="utf-8"))
    k3_cert = json.loads((ROOT / "certificates/K3.v1.json").read_text(encoding="utf-8"))
    k9_cert = json.loads((ROOT / "certificates/K9.v1.json").read_text(encoding="utf-8"))
    s4 = [entry for entry in s4_cert["generation_detail"] if entry.get("pass")]
    k3 = k3_cert["shadows"]
    reduction = k9_cert["reduction"][0]["image"]
    rows = []
    for t2_index, first in enumerate(s4):
        p_action = word_action(first["f_word"], r_x, r_y)
        for k3_index, second in enumerate(k3):
            if int(first["m"]) % 3 != int(second["m"]) % 3:
                continue
            choices = [
                m
                for m in range(18)
                if m % 9 == int(first["m"]) and m % 6 == int(second["m"])
            ]
            if len(choices) != 1:
                raise RuntimeError("CRT row did not have one m")
            m = choices[0]
            g3_parity = word_parity(second["f_word"])
            action = module_pair_action(p_action, g3_parity)
            preimages = sum(
                1
                for k9_index, target in enumerate(reduction)
                if int(target) == k3_index
                and int(k9_cert["shadows"][k9_index]["m"]) == m
            )
            rows.append(
                {
                    "t_index": len(rows),
                    "m": m,
                    "t2_index": t2_index,
                    "t2_m_mod9": int(first["m"]),
                    "k3_index": k3_index,
                    "k3_m_mod6": int(second["m"]),
                    "k_mod3": int(second["kernel_cert"]["k"]) % 3,
                    "K9_preimage_count": preimages,
                    "fbar_action": action,
                    "fbar_action_sha256": value_sha(action.tolist()),
                    "s4_f_word": first["f_word"],
                    "k3_f_word": second["f_word"],
                    "k3_word_parity": list(g3_parity),
                }
            )
    if len(s4) != 54 or len(k3) != 12 or len(rows) != 324:
        raise RuntimeError("roof count mismatch")
    if Counter(row["K9_preimage_count"] for row in rows) != Counter({3: 324}):
        raise RuntimeError("K9 fibre mismatch")
    return rows, {
        "GT_N_S4_order": len(s4),
        "GT_K3_order": len(k3),
        "GT_N_W_order": len(rows),
        "glue": "m mod 3; unique CRT lift modulo 18",
        "m_mod18_distribution": dict(sorted(Counter(row["m"] for row in rows).items())),
        "K9_preimage_count_distribution": {"3": 324},
        "GT_M_order_from_fibres": sum(row["K9_preimage_count"] for row in rows),
        "target_table_sha256": value_sha(
            [
                {
                    key: value
                    for key, value in row.items()
                    if key != "fbar_action"
                }
                for row in rows
            ]
        ),
    }


class Aff:
    def __init__(self, coefficient: np.ndarray, constant: np.ndarray, action: np.ndarray):
        self.coefficient = coefficient % F
        self.constant = constant % F
        self.action = action % F


def aff_const(vector: np.ndarray, action: np.ndarray) -> Aff:
    return Aff(np.zeros((21, 21), dtype=np.int64), vector, action)


def aff_unknown(action: np.ndarray) -> Aff:
    return Aff(eye(21), np.zeros(21, dtype=np.int64), action)


def aff_mul(left: Aff, right: Aff) -> Aff:
    return Aff(
        left.coefficient + mm(left.action, right.coefficient),
        left.constant + left.action @ right.constant,
        mm(left.action, right.action),
    )


def aff_inv(value: Aff) -> Aff:
    action_inverse = minv(value.action)
    return Aff(
        -mm(action_inverse, value.coefficient),
        -(action_inverse @ value.constant),
        action_inverse,
    )


def aff_pow(value: Aff, exponent: int) -> Aff:
    if exponent < 0:
        return aff_pow(aff_inv(value), -exponent)
    answer = aff_const(np.zeros(21, dtype=np.int64), eye(21))
    factor = value
    while exponent:
        if exponent & 1:
            answer = aff_mul(answer, factor)
        factor = aff_mul(factor, factor)
        exponent >>= 1
    return answer


def aff_conj(conjugator: Aff, value: Aff) -> Aff:
    return aff_mul(aff_mul(conjugator, value), aff_inv(conjugator))


def marked_elements(representative: list[int], theta: np.ndarray, tau: np.ndarray) -> dict[str, Aff]:
    vector = np.asarray(representative, dtype=np.int64)
    u = aff_const(vector[:21], theta)
    s = aff_const(vector[21:], tau)
    sigma_1 = aff_mul(aff_inv(s), u)
    sigma_2 = aff_mul(aff_inv(u), aff_pow(s, 2))
    x = aff_pow(sigma_1, 2)
    y = aff_pow(sigma_2, 2)
    return {"U": u, "S": s, "sigma_1": sigma_1, "sigma_2": sigma_2, "x": x, "y": y}


def relation_values(elements: dict[str, Aff], row: dict[str, Any]) -> tuple[Aff, Aff, Aff, Aff]:
    f = aff_unknown(row["fbar_action"])
    m = int(row["m"])
    exponent = 2 * m + 1
    sigma_1 = elements["sigma_1"]
    sigma_2 = elements["sigma_2"]
    x = elements["x"]
    y = elements["y"]
    c = aff_pow(elements["U"], 2)

    # Full B_3/N hexagons (3.3) and (3.4), in paper product order.
    # The reduced F_2 equations are equivalent at the element level here,
    # but their two coefficient ranks need not agree; A-42 explicitly binds
    # A1 and A2 to these two full equations.
    first_left = aff_mul(
        aff_mul(aff_mul(aff_pow(sigma_1, exponent), aff_inv(f)), aff_pow(sigma_2, exponent)),
        f,
    )
    first_right = aff_mul(
        aff_mul(aff_mul(aff_inv(f), sigma_1), sigma_2),
        aff_mul(aff_pow(x, -m), aff_pow(c, m)),
    )
    first = aff_mul(first_left, aff_inv(first_right))

    second_left = aff_mul(
        aff_mul(aff_mul(aff_inv(f), aff_pow(sigma_2, exponent)), f),
        aff_pow(sigma_1, exponent),
    )
    second_right = aff_mul(
        aff_mul(aff_mul(sigma_2, sigma_1), aff_pow(y, -m)),
        aff_mul(aff_pow(c, m), f),
    )
    second = aff_mul(second_left, aff_inv(second_right))

    generator_a = aff_pow(elements["x"], exponent)
    generator_b = aff_mul(
        aff_mul(aff_inv(f), aff_pow(elements["y"], exponent)), f
    )
    return first, second, generator_a, generator_b


def system_template(matrix: np.ndarray) -> dict[str, Any]:
    left_null = nullspace(matrix.T).T % F
    return {
        "matrix": matrix % F,
        "rank": rank(matrix),
        "left_null": left_null,
        "left_null_sha256": value_sha(left_null.tolist()),
        "variable_count": matrix.shape[1],
    }


def system_consistent(template: dict[str, Any], rhs: np.ndarray) -> bool:
    return not np.any((template["left_null"] @ rhs) % F)


def system_count(template: dict[str, Any], rhs: np.ndarray) -> int:
    if not system_consistent(template, rhs):
        return 0
    return F ** (int(template["variable_count"]) - int(template["rank"]))


def build_row_templates(
    theta: np.ndarray, tau: np.ndarray, rows: list[dict[str, Any]], rho_x: np.ndarray, rho_y: np.ndarray
) -> list[dict[str, Any]]:
    zero_class = [0] * 42
    elements = marked_elements(zero_class, theta, tau)
    if not np.array_equal(elements["x"].action, rho_x) or not np.array_equal(
        elements["y"].action, rho_y
    ):
        raise RuntimeError("pure anchor changed while building templates")
    answer = []
    for row in rows:
        first, second, generator_a, generator_b = relation_values(elements, row)
        if not np.array_equal(first.action, eye(21)) or not np.array_equal(
            second.action, eye(21)
        ):
            raise RuntimeError("roof shadow W relation mismatch")
        a1 = first.coefficient
        a2 = second.coefficient
        rank_a1 = rank(a1)
        rank_a2 = rank(a2)
        if rank_a1 != rank_a2:
            raise RuntimeError("rank_A1 differs from rank_A2")
        combined = np.concatenate((a1, a2), axis=0)
        hex_template = system_template(combined)
        subset_templates = {}
        invariant_dims = []
        for block in range(3):
            sl = slice(7 * block, 7 * block + 7)
            invariant_matrix = np.concatenate(
                (
                    eye(7) - generator_a.action[sl, sl],
                    eye(7) - generator_b.action[sl, sl],
                ),
                axis=0,
            ) % F
            invariant_dims.append(7 - rank(invariant_matrix))
        if invariant_dims != [0, 0, 0]:
            raise RuntimeError("target pair has a block invariant")
        for mask in range(1, 8):
            selected = [block for block in range(3) if (mask >> block) & 1]
            variable_count = 21 + 7 * len(selected)
            pieces = []
            base = np.zeros((42, variable_count), dtype=np.int64)
            base[:, :21] = combined
            pieces.append(base)
            for position, block in enumerate(selected):
                sl = slice(7 * block, 7 * block + 7)
                column_slice = slice(21 + 7 * position, 21 + 7 * position + 7)
                first_bad = np.zeros((7, variable_count), dtype=np.int64)
                first_bad[:, column_slice] = (
                    eye(7) - generator_a.action[sl, sl]
                ) % F
                second_bad = np.zeros((7, variable_count), dtype=np.int64)
                second_bad[:, :21] = generator_b.coefficient[sl, :]
                second_bad[:, column_slice] = -(
                    eye(7) - generator_b.action[sl, sl]
                ) % F
                pieces.extend((first_bad, second_bad))
            subset_templates[str(mask)] = system_template(np.concatenate(pieces, axis=0))
        answer.append(
            {
                "A1": a1,
                "A2": a2,
                "combined": combined,
                "rank_A1": rank_a1,
                "rank_A2": rank_a2,
                "hex": hex_template,
                "subsets": subset_templates,
                "block_invariant_dimensions": invariant_dims,
            }
        )
    return answer


def measure_window(
    eps: str,
    theta: np.ndarray,
    tau: np.ndarray,
    classes: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    rho_x: np.ndarray,
    rho_y: np.ndarray,
    checkpoint_update,
) -> dict[str, Any]:
    templates = build_row_templates(theta, tau, rows, rho_x, rho_y)
    checkpoint_update(
        f"templates_{eps}",
        eps=eps,
        rows=len(templates),
        rank_pair_distribution={
            f"{a},{b}": count
            for (a, b), count in sorted(
                Counter(
                    (item["rank_A1"], item["rank_A2"]) for item in templates
                ).items()
            )
        },
    )
    per_class = []
    surjective_classes = [entry for entry in classes if entry["surjective"]]
    for class_position, class_entry in enumerate(surjective_classes):
        elements = marked_elements(class_entry["representative"], theta, tau)
        lift_table = []
        for row, template in zip(rows, templates):
            first, second, generator_a, generator_b = relation_values(elements, row)
            if not np.array_equal(first.coefficient, template["A1"]) or not np.array_equal(
                second.coefficient, template["A2"]
            ):
                raise RuntimeError("class changed an affine coefficient")
            rhs = (-np.concatenate((first.constant, second.constant))) % F
            obstruction = (template["hex"]["left_null"] @ rhs) % F
            obstruction_zero = not np.any(obstruction)
            total = system_count(template["hex"], rhs)
            bad_counts: dict[str, int] = {}
            if total:
                for mask in range(1, 8):
                    selected = [block for block in range(3) if (mask >> block) & 1]
                    rhs_parts = [rhs]
                    for block in selected:
                        sl = slice(7 * block, 7 * block + 7)
                        rhs_parts.append(generator_a.constant[sl] % F)
                        rhs_parts.append((-generator_b.constant[sl]) % F)
                    extended_rhs = np.concatenate(rhs_parts)
                    bad_counts[str(mask)] = system_count(
                        template["subsets"][str(mask)], extended_rhs
                    )
                union = sum(
                    count if int(mask).bit_count() % 2 else -count
                    for mask, count in bad_counts.items()
                )
                generating_count = total - union
                if generating_count < 0 or generating_count > total:
                    raise RuntimeError("generation union count outside solution count")
            else:
                bad_counts = {str(mask): 0 for mask in range(1, 8)}
                generating_count = 0
            generating_exists = generating_count > 0
            lift_table.append(
                {
                    "t_index": int(row["t_index"]),
                    "rank_A1": int(template["rank_A1"]),
                    "rank_A2": int(template["rank_A2"]),
                    "rank_A1_equals_rank_A2": True,
                    "rank_A": int(template["hex"]["rank"]),
                    "dim_ker_A": 21 - int(template["hex"]["rank"]),
                    "obstruction_coordinates": [int(x) for x in obstruction],
                    "obstruction_zero": obstruction_zero,
                    "solution_count": int(total),
                    "bad_solution_counts_by_block_subset": bad_counts,
                    "generating_solution_count": int(generating_count),
                    "generating_solution_exists": generating_exists,
                    "lifts": bool(obstruction_zero and generating_exists),
                }
            )
        lifted = [row for row, result in zip(rows, lift_table) if result["lifts"]]
        per_t2 = []
        for t2_index in range(54):
            values = sorted(
                {
                    int(row["k_mod3"])
                    for row in lifted
                    if int(row["t2_index"]) == t2_index
                }
            )
            per_t2.append(
                {
                    "t2_index": t2_index,
                    "k_values_realized": values,
                    "count": len(values),
                    "lifted_NW_rows": sum(
                        1 for row in lifted if int(row["t2_index"]) == t2_index
                    ),
                }
            )
        image_nw = len(lifted)
        image_km = sum(int(row["K9_preimage_count"]) for row in lifted)
        per_class.append(
            {
                "class_index": int(class_entry["class_index"]),
                "quotient_coordinates": class_entry["quotient_coordinates"],
                "representative": class_entry["representative"],
                "lift_table": lift_table,
                "theta2": {
                    "per_t2": per_t2,
                    "count_distribution": dict(Counter(item["count"] for item in per_t2)),
                    "rigid": all(item["count"] == 1 for item in per_t2),
                },
                "Im_R_N_E_N_W_size": image_nw,
                "Im_R_K_M_size": image_km,
            }
        )
        if (class_position + 1) % 5 == 0 or class_position + 1 == len(surjective_classes):
            checkpoint_update(
                f"measure_{eps}",
                eps=eps,
                classes_complete=class_position + 1,
                classes_total=len(surjective_classes),
            )
    image_distribution = Counter(item["Im_R_K_M_size"] for item in per_class)
    nw_distribution = Counter(item["Im_R_N_E_N_W_size"] for item in per_class)
    return {
        "eps": eps,
        "surjective_class_count": len(surjective_classes),
        "per_class": per_class,
        "Im_R_K_M_distribution": dict(sorted(image_distribution.items())),
        "Im_R_N_E_N_W_distribution": dict(sorted(nw_distribution.items())),
        "theta2_rigid_class_count": sum(item["theta2"]["rigid"] for item in per_class),
        "theta2_count_distribution_across_classes_and_t2": dict(
            Counter(
                t2["count"]
                for item in per_class
                for t2 in item["theta2"]["per_t2"]
            )
        ),
        "rank_A1_A2_distribution": {
            f"{a},{b}": count
            for (a, b), count in sorted(
                Counter((item["rank_A1"], item["rank_A2"]) for item in templates).items()
            )
        },
        "rank_A_distribution": dict(
            sorted(Counter(item["hex"]["rank"] for item in templates).items())
        ),
        "template_sha256": value_sha(
            [
                {
                    "rank_A1": item["rank_A1"],
                    "rank_A2": item["rank_A2"],
                    "rank_A": item["hex"]["rank"],
                    "A_sha256": value_sha(item["combined"].tolist()),
                    "left_null_sha256": item["hex"]["left_null_sha256"],
                }
                for item in templates
            ]
        ),
    }


def build_preflight() -> dict[str, Any]:
    prior = json.loads(
        (ROOT / "search/certs/vnbit_affine_gate_raw_v1_20260813.json").read_text(
            encoding="utf-8"
        )
    )
    s_perm = mobius((1, 0, 1, 1))
    t_perm = mobius((4, 3, 1, 5))
    sigma_1_perm = compose(inv_perm(t_perm), s_perm)
    sigma_2_perm = compose(s_perm, pow_perm(t_perm, 2))
    x_perm = pow_perm(sigma_1_perm, 2)
    y_perm = pow_perm(sigma_2_perm, 2)
    p_group = perm_group((x_perm, y_perm))
    r_s = heart_matrix(s_perm)
    r_t = heart_matrix(t_perm)
    r_x = heart_matrix(x_perm)
    r_y = heart_matrix(y_perm)
    rho_x = mat(prior["C2"]["rho_X"])
    rho_y = mat(prior["C2"]["rho_Y"])
    theta_base = mat(prior["C2"]["theta_operator"])
    tau_base = mat(prior["C2"]["tau_operator"])
    if not np.array_equal(rho_x, module_pair_action(r_x, (1, 0))) or not np.array_equal(
        rho_y, module_pair_action(r_y, (0, 1))
    ):
        raise RuntimeError("task-130 matrix anchor changed")
    cyclic_counts = Counter()
    for coordinates in itertools.product(range(3), repeat=7):
        if not any(coordinates):
            continue
        cyclic_counts[cyclic_dimension(np.asarray(coordinates), (r_x, r_y))] += 1
    centralizer_dim, centralizer_digest = centralizer_dimension((r_x, r_y))
    c9 = {
        "P_order": len(p_group),
        "heart_dimension": 7,
        "nonzero_cyclic_submodule_dimension_distribution": dict(cyclic_counts),
        "irreducible_over_F3": cyclic_counts == Counter({7: 2186}),
        "endomorphism_ring_F3_dimension": centralizer_dim,
        "endomorphism_relation_rref_sha256": centralizer_digest,
        "V7_absolutely_irreducible": cyclic_counts == Counter({7: 2186})
        and centralizer_dim == 1,
        "criterion": "irreducible plus End_P(H)=F3 over a finite field",
    }
    gauge = gauge_data(theta_base, tau_base, rho_x, rho_y)
    if not c9["V7_absolutely_irreducible"]:
        raise RuntimeError("C-9 changed")
    if gauge["anchor_solutions"] != 8 or gauge["orbit_sizes"] != [4, 4]:
        raise RuntimeError("gauge census changed")

    windows = []
    # The fixed block is array block 2 (third displayed character block).
    normal_forms = {
        "+": ((2, 2, 1), "fixed block B=+R_S"),
        "-": ((1, 1, 2), "fixed block B=-R_S"),
    }
    for eps, (theta_signs, convention) in normal_forms.items():
        theta = mm(theta_base, block_diag([sign * eye(7) for sign in theta_signs]))
        tau = tau_base.copy()
        sigma_1 = mm(mpow(tau, 2), theta)
        sigma_2 = mm(theta, mpow(tau, 2))
        marked_x = mm(sigma_1, sigma_1)
        marked_y = mm(sigma_2, sigma_2)
        anchor = {
            "A1_holds": bool(np.array_equal(marked_x, rho_x)),
            "A2_holds": bool(np.array_equal(marked_y, rho_y)),
            "rho_X_block_signs": sign_pattern(rho_x, r_x),
            "rho_Y_block_signs": sign_pattern(rho_y, r_y),
            "residual_rank_A1": rank((marked_x - rho_x) % F),
            "residual_rank_A2": rank((marked_y - rho_y) % F),
        }
        pattern_x = anchor["rho_X_block_signs"]
        pattern_y = anchor["rho_Y_block_signs"]
        sign_check = {
            "X_plus_count": pattern_x.count(1),
            "Y_plus_count": pattern_y.count(1),
            "Y_is_cyclic_shift_of_X": any(
                pattern_y == pattern_x[offset:] + pattern_x[:offset] for offset in (1, 2)
            ),
            "Xbar_nontrivial_in_G3ab": pattern_x != [1, 1, 1],
        }
        if not all((anchor["A1_holds"], anchor["A2_holds"])) or sign_check != {
            "X_plus_count": 1,
            "Y_plus_count": 1,
            "Y_is_cyclic_shift_of_X": True,
            "Xbar_nontrivial_in_G3ab": True,
        }:
            raise RuntimeError("C-2 prime changed")
        ker_theta = 21 - rank((eye(21) + theta) % F)
        ker_tau = 21 - rank((eye(21) + tau + mm(tau, tau)) % F)
        gamma = gamma_classes(theta, tau)
        sl = sl_re(x_perm, y_perm, s_perm, t_perm, r_x, r_y, theta, tau)
        if sl["H1_barW_order"] != 1:
            for entry in gamma["classes"]:
                entry["surjective"] = None
            raise RuntimeError("nonzero H1_barW requires explicit inflation membership")
        surjective_count = sum(entry["surjective"] for entry in gamma["classes"])
        windows.append(
            {
                "eps": eps,
                "marking_version": "vnbit-monomial/v3",
                "theta_source_signs_F3": list(theta_signs),
                "theta_source_signs_integer": [1 if x == 1 else -1 for x in theta_signs],
                "tau_signs": [1, 1, 1],
                "fixed_block_array_index": 2,
                "eps_convention": convention,
                "B_matrix_sha256": value_sha(theta[14:21, 14:21].tolist()),
                "theta_matrix": theta.tolist(),
                "tau_matrix": tau.tolist(),
                "pure_anchor": anchor,
                "sign_pattern_check": sign_check,
                "C9": c9,
                "dim_ker_I_plus_theta": ker_theta,
                "dim_ker_I_plus_tau_plus_tau2": ker_tau,
                "gamma_cohomology": gamma,
                "SL_RE": sl,
                "H1_barW_order": sl["H1_barW_order"],
                "surjective_class_count": surjective_count,
            }
        )
    if sorted(window["dim_ker_I_plus_theta"] for window in windows) != [10, 11]:
        raise RuntimeError("P-vNC3-2 pair changed")
    if sum(window["dim_ker_I_plus_theta"] for window in windows) != 21:
        raise RuntimeError("P-vNC3-2 sum changed")
    if [window["gamma_cohomology"]["H1_order"] for window in windows] != [81, 27]:
        raise RuntimeError("P-vNC3-2 H1 orders changed")
    if any(window["dim_ker_I_plus_tau_plus_tau2"] != 14 for window in windows):
        raise RuntimeError("P-vNC3-3 changed")
    rows, roof = roof_rows(r_x, r_y)
    return {
        "schema": "vnbit_compact_preflight/v3",
        "generated_by": {
            "script": "search/vnbit_compact_mainrun_v3.py",
            "script_sha256": file_sha(Path(__file__)),
            "runtime": f"Python {os.sys.version.split()[0]} + NumPy {np.__version__}",
        },
        "source_sha256": {
            name: file_sha(ROOT / name)
            for name in (
                "ops/inbox_codex/sol_task_132_mainrun.txt",
                "docs/notes/vnbit_compact_route_v3.md",
                "docs/notes/bu_s35_embedding_v1.md",
                "docs/week1-定義ノート.md",
                "search/certs/vnbit_affine_gate_raw_v1_20260813.json",
                "certificates/S4.v2.json",
                "certificates/K3.v1.json",
                "certificates/K9.v1.json",
            )
        },
        "C9": c9,
        "gauge": gauge,
        "windows": windows,
        "cross_eps": {
            "dim_ker_values": [window["dim_ker_I_plus_theta"] for window in windows],
            "dim_ker_sum": sum(window["dim_ker_I_plus_theta"] for window in windows),
            "dim_ker_sum_is_21": True,
            "H1_orders": [window["gamma_cohomology"]["H1_order"] for window in windows],
            "tau_kernel_dimensions": [
                window["dim_ker_I_plus_tau_plus_tau2"] for window in windows
            ],
        },
        "roof": roof,
        "roof_targets": [
            {key: value for key, value in row.items() if key != "fbar_action"}
            for row in rows
        ],
        "stage_boundary": {
            "stage": "classified_before_preregistration",
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("preflight", "measure"), required=True)
    parser.add_argument(
        "--preflight-output",
        default="search/certs/vnbit_compact_preflight_v3_20260813.json",
    )
    parser.add_argument(
        "--prereg",
        default="search/certs/vnbit_compact_v3_prereg_20260813.json",
    )
    parser.add_argument(
        "--output",
        default="search/certs/vnbit_compact_mainrun_raw_v3_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/vnbit_compact_mainrun_v3_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    preflight_path = ROOT / args.preflight_output
    prereg_path = ROOT / args.prereg
    output_path = ROOT / args.output
    checkpoint_path = ROOT / args.checkpoint
    began = time.monotonic()
    state: dict[str, Any] = {
        "schema": "vnbit_compact_mainrun_checkpoint/v3",
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
        if args.mode == "preflight":
            preflight = build_preflight()
            preflight["run_id"] = "vnbit-compact-preflight-" + datetime.now(
                timezone.utc
            ).strftime("%Y%m%dT%H%M%SZ")
            atomic_json(preflight_path, preflight)
            update(
                "preflight_complete",
                complete=True,
                output_sha256=file_sha(preflight_path),
            )
            return 0

        preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
        prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
        if prereg["preflight_sha256"] != file_sha(preflight_path):
            raise RuntimeError("preregistration is not bound to current preflight")
        if prereg["producer_sha256"] != file_sha(Path(__file__)):
            raise RuntimeError("preregistration is not bound to current producer")
        if prereg["blind_before_measurement"] is not True:
            raise RuntimeError("blind preregistration declaration missing")
        update("preregistration_bound", prereg_sha256=file_sha(prereg_path))

        prior = json.loads(
            (ROOT / "search/certs/vnbit_affine_gate_raw_v1_20260813.json").read_text(
                encoding="utf-8"
            )
        )
        rho_x = mat(prior["C2"]["rho_X"])
        rho_y = mat(prior["C2"]["rho_Y"])
        s_perm = mobius((1, 0, 1, 1))
        t_perm = mobius((4, 3, 1, 5))
        sigma_1_perm = compose(inv_perm(t_perm), s_perm)
        sigma_2_perm = compose(s_perm, pow_perm(t_perm, 2))
        r_x = heart_matrix(pow_perm(sigma_1_perm, 2))
        r_y = heart_matrix(pow_perm(sigma_2_perm, 2))
        rows, roof = roof_rows(r_x, r_y)
        per_eps = []
        for window in preflight["windows"]:
            eps = window["eps"]
            measured = measure_window(
                eps,
                mat(window["theta_matrix"]),
                mat(window["tau_matrix"]),
                window["gamma_cohomology"]["classes"],
                rows,
                rho_x,
                rho_y,
                update,
            )
            measured.update(
                {
                    "marking_version": window["marking_version"],
                    "B_matrix_sha256": window["B_matrix_sha256"],
                    "dim_ker_I_plus_theta": window["dim_ker_I_plus_theta"],
                    "dim_ker_I_plus_tau_plus_tau2": window[
                        "dim_ker_I_plus_tau_plus_tau2"
                    ],
                    "H1_order": window["gamma_cohomology"]["H1_order"],
                    "H1_barW_order": window["H1_barW_order"],
                }
            )
            per_eps.append(measured)
        plus_sizes = set(per_eps[0]["Im_R_K_M_distribution"])
        minus_sizes = set(per_eps[1]["Im_R_K_M_distribution"])
        result = {
            "schema": "vnbit_compact/v3",
            "run_id": "vnbit-compact-mainrun-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "generated_by": preflight["generated_by"],
            "inputs": {
                "preflight": args.preflight_output,
                "preflight_sha256": file_sha(preflight_path),
                "preregistration": args.prereg,
                "preregistration_sha256": file_sha(prereg_path),
            },
            "pure_anchor": [window["pure_anchor"] for window in preflight["windows"]],
            "sign_pattern_check": [
                window["sign_pattern_check"] for window in preflight["windows"]
            ],
            "gauge": preflight["gauge"],
            "C9": preflight["C9"],
            "roof": roof,
            "roof_targets": preflight["roof_targets"],
            "per_eps": per_eps,
            "cross_eps": {
                **preflight["cross_eps"],
                "Im_R_size_sets": [sorted(map(int, plus_sizes)), sorted(map(int, minus_sizes))],
                "Im_R_agrees": plus_sizes == minus_sizes,
            },
            "A_shape": {
                "rows": 42,
                "cols": 21,
                "rank_A1_equals_rank_A2_all_rows": all(
                    a == b
                    for eps_data in per_eps
                    for key, count in eps_data["rank_A1_A2_distribution"].items()
                    for a, b in [map(int, key.split(","))]
                ),
            },
            "isolated": {
                "N_E_isolated": "UNKNOWN",
                "gate_policy": (
                    "measurement is allowed by C-4-prime; an image size corresponding "
                    "to 324 requires an isolatedness proof before interpretation"
                ),
                "vNB_GAP_1": "open",
            },
            "endgame_scope": (
                "gentle side only. Elevation of a B-branch countercandidate requires "
                "the B4 layer PENT_W-PASS and then FAKE-KILL^{B4}/U-10. No finite-"
                "depth B-type identification is made."
            ),
            "noncontact": preflight["noncontact"],
            "stage_boundary": {
                "stage": "two_window_measurement_complete",
                "windows": 2,
                "surjective_classes": sum(
                    item["surjective_class_count"] for item in per_eps
                ),
                "lift_rows": sum(
                    item["surjective_class_count"] * 324 for item in per_eps
                ),
            },
            "status_note": "raw machine values and distributions; no type adjudication",
        }
        atomic_json(output_path, result)
        update("complete", complete=True, output_sha256=file_sha(output_path))
        return 0
    finally:
        alarm.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
