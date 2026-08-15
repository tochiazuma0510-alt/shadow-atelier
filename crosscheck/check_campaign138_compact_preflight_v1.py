#!/usr/bin/env python3
"""Independent checker for campaign138_compact_preflight/v1.

This file imports no producer or search helper.  It rebuilds finite-field
linear algebra, marked affine words, gauge orbits, and the G3 Cayley collision
system directly from frozen JSON matrices and roof words.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import os
import sys
import threading
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PRIME = 2


def set_prime(value: int) -> None:
    global PRIME
    PRIME = value


def eye(n: int) -> np.ndarray:
    return np.eye(n, dtype=np.int64)


def mm(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return (left @ right) % PRIME


def rref(value: np.ndarray) -> tuple[np.ndarray, list[int]]:
    work = np.asarray(value, dtype=np.int64).copy() % PRIME
    row = 0
    pivots = []
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        pivot = row + int(choices[0])
        work[[row, pivot]] = work[[pivot, row]]
        inverse = pow(int(work[row, column]), -1, PRIME)
        work[row] = (inverse * work[row]) % PRIME
        for other in range(work.shape[0]):
            if other != row and work[other, column]:
                work[other] = (work[other] - work[other, column] * work[row]) % PRIME
        pivots.append(column)
        row += 1
        if row == work.shape[0]:
            break
    return work, pivots


def rank(value: np.ndarray) -> int:
    return len(rref(value)[1])


def inverse(value: np.ndarray) -> np.ndarray:
    n = value.shape[0]
    work, pivots = rref(np.concatenate((value, eye(n)), axis=1))
    if pivots[:n] != list(range(n)):
        raise RuntimeError("singular matrix")
    return work[:, n:] % PRIME


def mpow(value: np.ndarray, exponent: int) -> np.ndarray:
    if exponent < 0:
        return mpow(inverse(value), -exponent)
    answer = eye(value.shape[0])
    factor = value.copy() % PRIME
    while exponent:
        if exponent & 1:
            answer = mm(answer, factor)
        factor = mm(factor, factor)
        exponent >>= 1
    return answer


def nullspace(value: np.ndarray) -> np.ndarray:
    reduced, pivots = rref(value)
    free = [column for column in range(value.shape[1]) if column not in pivots]
    answer = np.zeros((value.shape[1], len(free)), dtype=np.int64)
    for index, column in enumerate(free):
        answer[column, index] = 1
        for row, pivot in enumerate(pivots):
            answer[pivot, index] = -reduced[row, column] % PRIME
    return answer


def extend_columns(initial: np.ndarray, candidates: np.ndarray) -> np.ndarray:
    answer = initial.copy() % PRIME
    current_rank = rank(answer)
    for column in range(candidates.shape[1]):
        trial = np.concatenate((answer, candidates[:, column : column + 1]), axis=1)
        new_rank = rank(trial)
        if new_rank > current_rank:
            answer = trial
            current_rank = new_rank
    return answer


def block_diag(values: list[np.ndarray]) -> np.ndarray:
    total = sum(value.shape[0] for value in values)
    answer = np.zeros((total, total), dtype=np.int64)
    offset = 0
    for value in values:
        size = value.shape[0]
        answer[offset : offset + size, offset : offset + size] = value
        offset += size
    return answer % PRIME


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha_obj(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def counter_json(value: collections.Counter) -> dict[str, int]:
    return {str(key): int(count) for key, count in sorted(value.items())}


class Symbol:
    def __init__(self, f: np.ndarray, z: np.ndarray, action: np.ndarray):
        self.f = f % PRIME
        self.z = z % PRIME
        self.action = action % PRIME


def sym_identity(n: int) -> Symbol:
    return Symbol(np.zeros((n, n), dtype=np.int64), np.zeros((n, 2 * n), dtype=np.int64), eye(n))


def sym_known(action: np.ndarray) -> Symbol:
    n = action.shape[0]
    return Symbol(np.zeros((n, n), dtype=np.int64), np.zeros((n, 2 * n), dtype=np.int64), action)


def sym_generator(action: np.ndarray, half: int) -> Symbol:
    n = action.shape[0]
    z = np.zeros((n, 2 * n), dtype=np.int64)
    z[:, half * n : (half + 1) * n] = eye(n)
    return Symbol(np.zeros((n, n), dtype=np.int64), z, action)


def sym_variable(action: np.ndarray) -> Symbol:
    n = action.shape[0]
    return Symbol(eye(n), np.zeros((n, 2 * n), dtype=np.int64), action)


def sym_mul(left: Symbol, right: Symbol) -> Symbol:
    return Symbol(
        left.f + mm(left.action, right.f),
        left.z + mm(left.action, right.z),
        mm(left.action, right.action),
    )


def sym_inv(value: Symbol) -> Symbol:
    action_inverse = inverse(value.action)
    return Symbol(-mm(action_inverse, value.f), -mm(action_inverse, value.z), action_inverse)


def sym_pow(value: Symbol, exponent: int) -> Symbol:
    if exponent < 0:
        return sym_pow(sym_inv(value), -exponent)
    answer = sym_identity(value.action.shape[0])
    factor = value
    while exponent:
        if exponent & 1:
            answer = sym_mul(answer, factor)
        factor = sym_mul(factor, factor)
        exponent >>= 1
    return answer


def marked(theta: np.ndarray, tau: np.ndarray) -> dict[str, Symbol]:
    delta_big = sym_generator(theta, 0)
    delta_small = sym_generator(tau, 1)
    sigma_1 = sym_mul(sym_inv(delta_small), delta_big)
    sigma_2 = sym_mul(sym_inv(delta_big), sym_pow(delta_small, 2))
    return {
        "Delta": delta_big,
        "delta": delta_small,
        "sigma_1": sigma_1,
        "sigma_2": sigma_2,
        "x": sym_pow(sigma_1, 2),
        "y": sym_pow(sigma_2, 2),
    }


def relation_pair(symbols: dict[str, Symbol], action: np.ndarray, m_value: int) -> tuple[Symbol, Symbol]:
    f = sym_variable(action)
    exponent = 2 * m_value + 1
    s1, s2 = symbols["sigma_1"], symbols["sigma_2"]
    x, y = symbols["x"], symbols["y"]
    central = sym_pow(symbols["Delta"], 2)
    left_1 = sym_mul(sym_mul(sym_mul(sym_pow(s1, exponent), sym_inv(f)), sym_pow(s2, exponent)), f)
    right_1 = sym_mul(
        sym_mul(sym_mul(sym_inv(f), s1), s2),
        sym_mul(sym_pow(x, -m_value), sym_pow(central, m_value)),
    )
    left_2 = sym_mul(sym_mul(sym_mul(sym_inv(f), sym_pow(s2, exponent)), f), sym_pow(s1, exponent))
    right_2 = sym_mul(
        sym_mul(sym_mul(s2, s1), sym_pow(y, -m_value)),
        sym_mul(sym_pow(central, m_value), f),
    )
    return sym_mul(left_1, sym_inv(right_1)), sym_mul(left_2, sym_inv(right_2))


def word_action(word: list, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    answer = eye(x.shape[0])
    for letter, exponent in word:
        answer = mm(answer, mpow(x if letter == "x" else y, int(exponent)))
    return answer


def roof_rows(targets: list[dict], x: np.ndarray, y: np.ndarray, word_key: str) -> list[dict]:
    return [
        {
            "t_index": int(row["t_index"]),
            "m": int(row["m"]),
            "f_action": word_action(row[word_key], x, y),
        }
        for row in sorted(targets, key=lambda item: int(item["t_index"]))
    ]


def rank_gate(theta: np.ndarray, tau: np.ndarray, rows: list[dict]) -> dict:
    n = theta.shape[0]
    condition = np.zeros((2 * n, 2 * n), dtype=np.int64)
    condition[:n, :n] = eye(n) + theta
    condition[n:, n:] = eye(n) + tau + mm(tau, tau)
    condition %= PRIME
    z_basis = nullspace(condition)
    coboundaries = np.concatenate((eye(n) - theta, eye(n) - tau), axis=0) % PRIME
    symbols = marked(theta, tau)
    rank_a = collections.Counter()
    rank_cz = collections.Counter()
    rank_observation = collections.Counter()
    digest = hashlib.sha256()
    first_positive = None
    for row in rows:
        first, second = relation_pair(symbols, row["f_action"], row["m"])
        matrix_a = np.concatenate((first.f, second.f), axis=0) % PRIME
        matrix_c = np.concatenate((first.z, second.z), axis=0) % PRIME
        cz = mm(matrix_c, z_basis)
        a_rank = rank(matrix_a)
        c_rank = rank(cz)
        observation = rank(np.concatenate((matrix_a, cz), axis=1)) - a_rank
        record = {
            "t_index": row["t_index"],
            "rank_A": a_rank,
            "rank_CZ": c_rank,
            "rank_observation": observation,
        }
        digest.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode() + b"\n")
        rank_a[a_rank] += 1
        rank_cz[c_rank] += 1
        rank_observation[observation] += 1
        if observation and first_positive is None:
            first_positive = record
    b_dimension = rank(coboundaries)
    return {
        "Z1_dimension": z_basis.shape[1],
        "B1_dimension": b_dimension,
        "H1_dimension": z_basis.shape[1] - b_dimension,
        "rows": len(rows),
        "rank_A_distribution": counter_json(rank_a),
        "rank_CZ_distribution": counter_json(rank_cz),
        "rank_observation_distribution": counter_json(rank_observation),
        "first_positive_rank_row": first_positive,
        "rank_row_digest": digest.hexdigest(),
    }


def cyclic_h2(theta: np.ndarray, tau: np.ndarray) -> dict:
    operator = theta if PRIME == 2 else tau
    unit = eye(operator.shape[0])
    norm = unit + operator
    if PRIME == 3:
        norm += mm(operator, operator)
    norm %= PRIME
    fixed = operator.shape[0] - rank(operator - unit)
    return {
        "cyclic_order": PRIME,
        "fixed_dimension": fixed,
        "norm_rank": rank(norm),
        "H2_dimension": fixed - rank(norm),
    }


def all_gl2(prime: int) -> list[np.ndarray]:
    set_prime(prime)
    return [
        np.asarray(values, dtype=np.int64).reshape(2, 2)
        for values in itertools.product(range(prime), repeat=4)
        if rank(np.asarray(values, dtype=np.int64).reshape(2, 2)) == 2
    ]


def duplicate_blocks(matrix: np.ndarray, block_size: int, count: int) -> np.ndarray:
    answer = np.zeros((2 * matrix.shape[0], 2 * matrix.shape[1]), dtype=np.int64)
    for target_block in range(count):
        for source_block in range(count):
            piece = matrix[
                block_size * target_block : block_size * (target_block + 1),
                block_size * source_block : block_size * (source_block + 1),
            ]
            for multiplicity in range(2):
                row = 2 * block_size * target_block + block_size * multiplicity
                column = 2 * block_size * source_block + block_size * multiplicity
                answer[row : row + block_size, column : column + block_size] = piece
    return answer % PRIME


def c1_centralizer(triple: tuple[np.ndarray, ...]) -> np.ndarray:
    answer = np.zeros((24, 24), dtype=np.int64)
    for block, matrix in enumerate(triple):
        for target in range(2):
            for source in range(2):
                if matrix[target, source]:
                    answer[
                        8 * block + 4 * target : 8 * block + 4 * target + 4,
                        8 * block + 4 * source : 8 * block + 4 * source + 4,
                    ] = eye(4)
    return answer % 2


def c2_centralizer(matrix: np.ndarray) -> np.ndarray:
    unit = eye(7)
    return np.block(
        [[matrix[0, 0] * unit, matrix[0, 1] * unit], [matrix[1, 0] * unit, matrix[1, 1] * unit]]
    ) % 3


def anchor_orbits(theta_base: np.ndarray, tau_base: np.ndarray, centralizers: list[np.ndarray]) -> list[dict]:
    s1 = mm(mpow(tau_base, -1), theta_base)
    s2 = mm(mpow(theta_base, -1), mpow(tau_base, 2))
    rho_x, rho_y = mpow(s1, 2), mpow(s2, 2)
    valid = {}
    for i, a in enumerate(centralizers):
        theta = mm(theta_base, a)
        if not np.array_equal(mpow(theta, 2), eye(theta.shape[0])):
            continue
        for j, b in enumerate(centralizers):
            tau = mm(tau_base, b)
            if not np.array_equal(mpow(tau, 3), eye(tau.shape[0])):
                continue
            new_s1 = mm(mpow(tau, -1), theta)
            new_s2 = mm(mpow(theta, -1), mpow(tau, 2))
            if np.array_equal(mpow(new_s1, 2), rho_x) and np.array_equal(mpow(new_s2, 2), rho_y):
                valid[(i, j)] = (theta, tau)
    lookup = {matrix.tobytes(): index for index, matrix in enumerate(centralizers)}
    unseen = set(valid)
    answer = []
    while unseen:
        seed = min(unseen)
        theta, tau = valid[seed]
        orbit = set()
        for gauge in centralizers:
            gauge_inverse = inverse(gauge)
            theta_g = mm(mm(gauge_inverse, theta), gauge)
            tau_g = mm(mm(gauge_inverse, tau), gauge)
            a = mm(mpow(theta_base, -1), theta_g)
            b = mm(mpow(tau_base, -1), tau_g)
            key = (lookup[a.tobytes()], lookup[b.tobytes()])
            if key in valid:
                orbit.add(key)
        representative = min(orbit)
        answer.append(
            {
                "representative": representative,
                "orbit": sorted(orbit),
                "theta": valid[representative][0],
                "tau": valid[representative][1],
            }
        )
        unseen -= orbit
    answer.sort(key=lambda item: item["representative"])
    return answer


def group_order(generators: tuple[np.ndarray, ...]) -> int:
    unit = eye(generators[0].shape[0])
    seen = {unit.tobytes()}
    queue = [unit]
    for item in queue:
        for generator in generators:
            new = mm(item, generator)
            if new.tobytes() not in seen:
                seen.add(new.tobytes())
                queue.append(new)
    return len(queue)


def orbit_summary(orbits: list[dict], rows: list[dict], identity_index: int) -> list[dict]:
    answer = []
    for index, orbit in enumerate(orbits):
        answer.append(
            {
                "orbit_index": index,
                "representative_twist_indices": list(orbit["representative"]),
                "orbit_size": len(orbit["orbit"]),
                "contains_block_duplicate": (identity_index, identity_index) in orbit["orbit"],
                "marked_group_order": group_order((orbit["theta"], orbit["tau"])),
                "cyclic_H2": cyclic_h2(orbit["theta"], orbit["tau"]),
                "rank_gate": rank_gate(orbit["theta"], orbit["tau"], rows),
            }
        )
    return answer


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def perm_inverse(value: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * len(value)
    for source, target in enumerate(value):
        answer[target] = source
    return tuple(answer)


def g3_permutations() -> tuple[tuple[int, ...], tuple[int, ...]]:
    rotation = (1, 2, 0)
    reflection = (0, 2, 1)
    product = compose(rotation, reflection)
    def blocks(parts: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
        answer = []
        for block, permutation in enumerate(parts):
            answer.extend(3 * block + permutation[index] for index in range(3))
        return tuple(answer)
    return blocks((rotation, reflection, reflection)), blocks((product, rotation, product))


def cocycle_graph(gx: tuple[int, ...], gy: tuple[int, ...], ax: np.ndarray, ay: np.ndarray) -> dict:
    dimension = ax.shape[0]
    identity_perm = tuple(range(len(gx)))
    unit = eye(dimension)
    zero = np.zeros((dimension, 2 * dimension), dtype=np.int64)
    gen_expr = []
    for which in range(2):
        value = zero.copy()
        value[:, which * dimension : (which + 1) * dimension] = unit
        gen_expr.append(value)
    data = {identity_perm: (unit, zero)}
    queue = [identity_perm]
    constraints = []
    for element in queue:
        action, expression = data[element]
        for generator_perm, generator_action, generator_expression in (
            (gx, ax, gen_expr[0]),
            (gy, ay, gen_expr[1]),
        ):
            new_perm = compose(element, generator_perm)
            new_action = mm(action, generator_action)
            new_expression = (expression + mm(action, generator_expression)) % PRIME
            if new_perm in data:
                constraints.append((new_expression - data[new_perm][1]) % PRIME)
            else:
                data[new_perm] = (new_action, new_expression)
                queue.append(new_perm)
    relation = np.concatenate(constraints, axis=0)
    return {"order": len(queue), "constraints": relation, "relation_rank": rank(relation)}


R = np.asarray([[0, 1], [1, 1]], dtype=np.int64)
J = np.asarray([[0, 1], [1, 0]], dtype=np.int64)
THETA3 = np.asarray([[0, 1, 0], [1, 0, 0], [0, 0, 2]], dtype=np.int64)
TAU3 = np.asarray([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=np.int64)
SUPPORT2 = [(1, 1, 0), (1, 2, 0), (0, 1, 1), (0, 1, 2), (1, 0, 1), (1, 0, 2)]


def q_operator(representatives: list[tuple[int, int, int]], q: np.ndarray) -> np.ndarray:
    answer = np.zeros((2 * len(representatives), 2 * len(representatives)), dtype=np.int64)
    for source, weight in enumerate(representatives):
        image = tuple(int(x) for x in (q @ np.asarray(weight, dtype=np.int64)) % 3)
        for target, representative in enumerate(representatives):
            if image == representative:
                piece = eye(2)
                break
            if image == tuple((-x) % 3 for x in representative):
                piece = J
                break
        else:
            raise RuntimeError("unstable weight orbit")
        answer[2 * target : 2 * target + 2, 2 * source : 2 * source + 2] = piece
    return answer % 2


def a_operator(representatives: list[tuple[int, int, int]], vector: tuple[int, int, int]) -> np.ndarray:
    pieces = []
    for weight in representatives:
        exponent = sum(a * b for a, b in zip(weight, vector)) % 3
        pieces.append(mpow(R, exponent))
    return block_diag(pieces)


def support_module(representatives: list[tuple[int, int, int]]) -> tuple[np.ndarray, np.ndarray]:
    theta = q_operator(representatives, THETA3)
    tau = mm(a_operator(representatives, (1, 2, 0)), q_operator(representatives, TAU3))
    return theta, tau


def simple_modules() -> list[dict]:
    modules = [
        ("one", eye(1), eye(1)),
        ("D", J.copy(), R.copy()),
        ("orbit1", *support_module([(1, 0, 0), (0, 1, 0), (0, 0, 1)])),
        ("orbit2", *support_module(SUPPORT2)),
        ("orbit3", *support_module([(1, b, c) for b in (1, 2) for c in (1, 2)])),
    ]
    answer = []
    for name, theta, tau in modules:
        s1 = mm(mpow(tau, -1), theta)
        s2 = mm(mpow(theta, -1), mpow(tau, 2))
        answer.append({"name": name, "theta": theta, "tau": tau, "rho_x": mpow(s1, 2), "rho_y": mpow(s2, 2)})
    return answer


def hom_action(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    right_inverse = inverse(right)
    left_dim, right_dim = left.shape[0], right.shape[0]
    answer = np.zeros((left_dim * right_dim, left_dim * right_dim), dtype=np.int64)
    for row in range(left_dim):
        for column in range(right_dim):
            answer[:, right_dim * row + column] = np.outer(
                left[:, row], right_inverse[column, :]
            ).reshape(-1) % 2
    return answer


def extension_spaces(submodule: dict, quotient: dict) -> dict:
    theta_hom = hom_action(submodule["theta"], quotient["theta"])
    tau_hom = hom_action(submodule["tau"], quotient["tau"])
    x_hom = hom_action(submodule["rho_x"], quotient["rho_x"])
    y_hom = hom_action(submodule["rho_y"], quotient["rho_y"])
    dimension = theta_hom.shape[0]
    gx, gy = g3_permutations()
    graph = cocycle_graph(gx, gy, x_hom, y_hom)
    pure_b = np.concatenate((eye(dimension) - x_hom, eye(dimension) - y_hom), axis=0) % 2
    pure_h1 = 2 * dimension - graph["relation_rank"] - rank(pure_b)
    condition = np.zeros((2 * dimension, 2 * dimension), dtype=np.int64)
    condition[:dimension, :dimension] = eye(dimension) + theta_hom
    condition[dimension:, dimension:] = eye(dimension) + tau_hom + mm(tau_hom, tau_hom)
    condition %= 2
    symbols = marked(theta_hom, tau_hom)
    restriction = np.concatenate((symbols["x"].z, symbols["y"].z), axis=0) % 2
    z_basis = nullspace(np.concatenate((condition, mm(graph["constraints"], restriction)), axis=0))
    marked_b = np.concatenate((eye(dimension) - theta_hom, eye(dimension) - tau_hom), axis=0) % 2
    marked_b_basis = marked_b[:, rref(marked_b)[1]]
    full = extend_columns(marked_b_basis, z_basis)
    marked_h = full[:, marked_b_basis.shape[1] :]
    pure_image = rank(np.concatenate((pure_b, mm(restriction, marked_h)), axis=1)) - rank(pure_b)
    return {
        "pure_H1_dimension": pure_h1,
        "marked_H1_dimension": marked_h.shape[1],
        "pure_image_dimension": pure_image,
        "marked_H_basis": marked_h,
        "restriction": restriction,
        "pure_B": pure_b,
    }


def build_extension(submodule: dict, quotient: dict, vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    a = submodule["theta"].shape[0]
    b = quotient["theta"].shape[0]
    hom_dim = a * b
    z_theta = vector[:hom_dim].reshape(a, b)
    z_tau = vector[hom_dim:].reshape(a, b)
    zero = np.zeros((b, a), dtype=np.int64)
    theta = np.block(
        [[submodule["theta"], mm(z_theta, quotient["theta"])], [zero, quotient["theta"]]]
    ) % 2
    tau = np.block(
        [[submodule["tau"], mm(z_tau, quotient["tau"])], [zero, quotient["tau"]]]
    ) % 2
    return theta, tau


def normalized_gate(value: dict) -> dict:
    keys = (
        "Z1_dimension",
        "B1_dimension",
        "H1_dimension",
        "rows",
        "rank_A_distribution",
        "rank_CZ_distribution",
        "rank_observation_distribution",
        "first_positive_rank_row",
        "rank_row_digest",
    )
    return {key: value[key] for key in keys}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--hard-timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    began = time.monotonic()
    source_path = Path(args.source)
    output_path = Path(args.output)
    checkpoint_path = Path(args.checkpoint)
    state = {"schema": "campaign138_check_checkpoint/v1", "stage": "start", "complete": False}
    atomic_json(checkpoint_path, state)

    def update(stage: str, **extra: object) -> None:
        state.update(stage=stage, elapsed_ms=int(1000 * (time.monotonic() - began)), **extra)
        atomic_json(checkpoint_path, state)

    def timeout() -> None:
        if not state["complete"]:
            update("hard_timeout")
            os._exit(124)

    alarm = threading.Timer(args.hard_timeout_seconds, timeout)
    alarm.daemon = True
    alarm.start()
    try:
        source = json.loads(source_path.read_text(encoding="utf-8"))
        p2_input = json.loads((ROOT / "search/certs/escape2_preflight_v1_20260815.json").read_text(encoding="utf-8"))
        p3_input = json.loads((ROOT / "search/certs/escape28_preflight_v1r2_20260813.json").read_text(encoding="utf-8"))
        targets = p3_input["roof"]["targets"]

        update("C1")
        set_prime(2)
        theta12 = np.asarray(p2_input["module"]["theta_matrix"], dtype=np.int64)
        tau12 = np.asarray(p2_input["module"]["tau_matrix"], dtype=np.int64)
        theta24 = duplicate_blocks(theta12, 4, 3)
        tau24 = duplicate_blocks(tau12, 4, 3)
        gl2 = all_gl2(2)
        centralizers1 = [c1_centralizer(triple) for triple in itertools.product(gl2, repeat=3)]
        orbits1 = anchor_orbits(theta24, tau24, centralizers1)
        s1 = mm(mpow(tau24, -1), theta24)
        s2 = mm(mpow(theta24, -1), mpow(tau24, 2))
        rows1 = roof_rows(targets, mpow(s1, 2), mpow(s2, 2), "k3_f_word")
        identity1 = next(i for i, value in enumerate(centralizers1) if np.array_equal(value, eye(24)))
        summary1 = orbit_summary(orbits1, rows1, identity1)

        update("C2")
        set_prime(3)
        base = p3_input["components"]["trivial_character"]["+"]
        theta7 = np.asarray(base["theta_matrix"], dtype=np.int64)
        tau7 = np.asarray(base["tau_matrix"], dtype=np.int64)
        theta14, tau14 = block_diag([theta7, theta7]), block_diag([tau7, tau7])
        gl3 = all_gl2(3)
        centralizers2 = [c2_centralizer(matrix) for matrix in gl3]
        orbits2 = anchor_orbits(theta14, tau14, centralizers2)
        base_symbols = marked(theta7, tau7)
        rows7 = roof_rows(targets, base_symbols["x"].action, base_symbols["y"].action, "s4_f_word")
        rows2 = [
            {"t_index": row["t_index"], "m": row["m"], "f_action": block_diag([row["f_action"], row["f_action"]])}
            for row in rows7
        ]
        identity2 = next(i for i, value in enumerate(centralizers2) if np.array_equal(value, eye(14)))
        summary2 = orbit_summary(orbits2, rows2, identity2)

        update("C3")
        set_prime(2)
        modules = simple_modules()
        ext_table = []
        marked_table = []
        candidates = []
        for submodule in modules:
            ext_row = []
            marked_row = []
            for quotient in modules:
                spaces = extension_spaces(submodule, quotient)
                ext_row.append(spaces["pure_H1_dimension"])
                marked_row.append(
                    {
                        "marked_H1_dimension": spaces["marked_H1_dimension"],
                        "pure_image_dimension": spaces["pure_image_dimension"],
                    }
                )
                if spaces["pure_image_dimension"]:
                    pure_b_rank = rank(spaces["pure_B"])
                    good = []
                    for column in range(spaces["marked_H_basis"].shape[1]):
                        vector = spaces["marked_H_basis"][:, column]
                        restricted = mm(spaces["restriction"], vector.reshape(-1, 1))
                        if rank(np.concatenate((spaces["pure_B"], restricted), axis=1)) > pure_b_rank:
                            good.append(vector)
                    if len(good) != 1:
                        raise RuntimeError("checker extension basis is not unique")
                    theta, tau = build_extension(submodule, quotient, good[0])
                    symbols = marked(theta, tau)
                    rows = roof_rows(targets, symbols["x"].action, symbols["y"].action, "k3_f_word")
                    candidates.append(
                        {
                            "extension_id": f"{submodule['name']}<-{quotient['name']}",
                            "dimension": theta.shape[0],
                            "cyclic_H2": cyclic_h2(theta, tau),
                            "rank_gate": rank_gate(theta, tau, rows),
                        }
                    )
            ext_table.append(ext_row)
            marked_table.append(marked_row)

        checks = {
            "source_schema": source["schema"] == "campaign138_compact_preflight/v1",
            "C1_counts": source["C1"]["anchor_solutions"] == sum(len(item["orbit"]) for item in orbits1)
            and source["C1"]["gauge_orbits"] == len(orbits1),
            "C1_orbits": all(
                all(
                    actual[key] == expected[key]
                    for key in (
                        "orbit_index",
                        "representative_twist_indices",
                        "orbit_size",
                        "contains_block_duplicate",
                        "marked_group_order",
                        "cyclic_H2",
                    )
                )
                and normalized_gate(actual["rank_gate"]) == normalized_gate(expected["rank_gate"])
                for actual, expected in zip(source["C1"]["orbits"], summary1)
            ),
            "C2_counts": source["C2"]["anchor_solutions"] == sum(len(item["orbit"]) for item in orbits2)
            and source["C2"]["gauge_orbits"] == len(orbits2),
            "C2_orbits": all(
                all(
                    actual[key] == expected[key]
                    for key in (
                        "orbit_index",
                        "representative_twist_indices",
                        "orbit_size",
                        "contains_block_duplicate",
                        "marked_group_order",
                        "cyclic_H2",
                    )
                )
                and normalized_gate(actual["rank_gate"]) == normalized_gate(expected["rank_gate"])
                for actual, expected in zip(source["C2"]["orbits"], summary2)
            ),
            "C3_Ext_table": source["C3"]["pure_Ext1_dimension_table"] == ext_table,
            "C3_marked_table": source["C3"]["marked_extension_table"] == marked_table,
            "C3_candidates": len(source["C3"]["nonsplit_marked_candidates"]) == len(candidates)
            and all(
                actual["extension_id"] == expected["extension_id"]
                and actual["dimension"] == expected["dimension"]
                and actual["cyclic_H2"] == expected["cyclic_H2"]
                and normalized_gate(actual["rank_gate"]) == normalized_gate(expected["rank_gate"])
                for actual, expected in zip(source["C3"]["nonsplit_marked_candidates"], candidates)
            ),
            "rank_templates": source["aggregate"]["rank_templates"] == 3240,
            "no_positive_rank": source["aggregate"]["positive_rank_entries"] == []
            and all(entry["rank_gate"]["first_positive_rank_row"] is None for entry in summary1 + summary2 + candidates),
            "no_formal_outcomes": source["aggregate"]["formal_class_outcomes_opened"] == 0
            and source["aggregate"]["element_survival_outcomes_opened"] == 0,
            "positive_control": source["positive_control"]["passed"]
            and source["positive_control"]["escape2_Im_R_K_M_distribution"] == {"972": 7}
            and source["positive_control"]["minimum_required"] == 324,
        }
        result = {
            "schema": "campaign138_compact_preflight_check/v1",
            "source": str(source_path).replace("\\", "/"),
            "source_sha256": sha_file(source_path),
            "checker_sha256": sha_file(Path(__file__)),
            "checks": checks,
            "all_checks_true": all(checks.values()),
            "reconstructed": {
                "C1_anchor_solutions": sum(len(item["orbit"]) for item in orbits1),
                "C1_gauge_orbits": len(orbits1),
                "C2_anchor_solutions": sum(len(item["orbit"]) for item in orbits2),
                "C2_gauge_orbits": len(orbits2),
                "C3_nonsplit_marked_candidates": len(candidates),
                "rank_templates": 324 * (len(summary1) + len(summary2) + len(candidates)),
            },
            "formal_class_outcomes_opened": 0,
            "noncontact": source["noncontact"],
            "generated_by": {"python": sys.version.split()[0], "numpy": np.__version__},
        }
        atomic_json(output_path, result)
        update("complete", complete=True, output_sha256=sha_file(output_path), all_checks_true=result["all_checks_true"])
        if not result["all_checks_true"]:
            raise SystemExit(2)
    finally:
        alarm.cancel()


if __name__ == "__main__":
    main()
