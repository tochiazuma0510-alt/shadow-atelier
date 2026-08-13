#!/usr/bin/env python3
"""Independent preflight audit for the vN-BIT two-window main run.

The producer is not imported.  Matrix and permutation primitives come from
the task-132 main-run checker, whose augmentation-heart basis differs from the
producer's basis.  Cohomology relations are rebuilt from the 504-vertex
positive Cayley graph.
"""

from __future__ import annotations

import argparse
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

from check_vnbit_compact_mainrun_v3 import (
    FIELD,
    ROOT,
    S_PERM,
    T_PERM,
    after,
    alternate_heart,
    block_diagonal,
    block_transport,
    coordinate_change,
    file_digest,
    identity,
    inverse_matrix,
    inverse_permutation,
    kernel_columns,
    marked_elements,
    matrix,
    matrix_power,
    matrix_rank,
    module_action,
    object_digest,
    permutation_power,
    product,
    reduced_row_echelon,
    replace_json,
)


def extend_independent_columns(base: np.ndarray, candidates: np.ndarray) -> np.ndarray:
    answer = base.copy()
    current_rank = matrix_rank(answer) if answer.shape[1] else 0
    for column in range(candidates.shape[1]):
        trial = np.concatenate((answer, candidates[:, column : column + 1]), axis=1)
        trial_rank = matrix_rank(trial)
        if trial_rank > current_rank:
            answer = trial
            current_rank = trial_rank
    return answer


def coordinates_in_columns(base: np.ndarray, vector: np.ndarray) -> np.ndarray:
    augmented = np.concatenate((base, vector.reshape(-1, 1)), axis=1)
    reduced, pivots = reduced_row_echelon(augmented)
    width = base.shape[1]
    for row in range(reduced.shape[0]):
        if not np.any(reduced[row, :width]) and reduced[row, width]:
            raise RuntimeError("vector outside expected column space")
    answer = np.zeros(width, dtype=np.int64)
    for row, pivot in enumerate(pivots):
        if pivot < width:
            answer[pivot] = reduced[row, width]
    return answer


def cyclic_span_dimension(seed: np.ndarray, generators: tuple[np.ndarray, ...]) -> int:
    columns = np.zeros((len(seed), 0), dtype=np.int64)
    queue = [seed]
    while queue:
        vector = queue.pop()
        trial = np.concatenate((columns, vector.reshape(-1, 1)), axis=1)
        if matrix_rank(trial) == columns.shape[1]:
            continue
        columns = trial
        for generator in generators:
            queue.append((generator @ vector) % FIELD)
    return columns.shape[1]


def centralizer_dimension(generators: tuple[np.ndarray, ...]) -> tuple[int, str]:
    equations = []
    for generator in generators:
        for row in range(7):
            for column in range(7):
                equation = np.zeros(49, dtype=np.int64)
                for middle in range(7):
                    equation[7 * row + middle] += generator[middle, column]
                    equation[7 * middle + column] -= generator[row, middle]
                equations.append(equation % FIELD)
    relation_matrix = np.asarray(equations, dtype=np.int64) % FIELD
    reduced, _ = reduced_row_echelon(relation_matrix)
    canonical = reduced[np.any(reduced, axis=1)]
    return 49 - matrix_rank(relation_matrix), object_digest(canonical.tolist())


def cayley_cocycle_graph(
    x_perm: tuple[int, ...],
    y_perm: tuple[int, ...],
    rho_x: np.ndarray,
    rho_y: np.ndarray,
) -> dict[str, Any]:
    dimension = rho_x.shape[0]
    zero = np.zeros((dimension, 2 * dimension), dtype=np.int64)
    expressions = []
    for generator_index in range(2):
        expression = zero.copy()
        expression[
            :, generator_index * dimension : (generator_index + 1) * dimension
        ] = identity(dimension)
        expressions.append(expression)
    identity_perm = tuple(range(9))
    elements = [identity_perm]
    data: dict[tuple[int, ...], tuple[np.ndarray, np.ndarray]] = {
        identity_perm: (identity(dimension), zero)
    }
    constraints = []
    collisions = 0
    for old in elements:
        old_action, old_expression = data[old]
        for permutation, action, expression in (
            (x_perm, rho_x, expressions[0]),
            (y_perm, rho_y, expressions[1]),
        ):
            new = after(old, permutation)
            new_action = product(old_action, action)
            new_expression = (
                old_expression + product(old_action, expression)
            ) % FIELD
            if new in data:
                if not np.array_equal(data[new][0], new_action):
                    raise RuntimeError("Cayley action inconsistency")
                constraints.append((new_expression - data[new][1]) % FIELD)
                collisions += 1
            else:
                data[new] = (new_action, new_expression)
                elements.append(new)
    relation_matrix = np.concatenate(constraints, axis=0)
    reduced, _ = reduced_row_echelon(relation_matrix)
    canonical = reduced[np.any(reduced, axis=1)]
    return {
        "elements": elements,
        "data": data,
        "constraints": relation_matrix,
        "relation_rank": matrix_rank(relation_matrix),
        "relation_rref_sha256_alt_basis": object_digest(canonical.tolist()),
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
    coboundary_dimension: int,
) -> np.ndarray:
    q_inverse = inverse_permutation(q_perm)
    x_conjugate = after(q_inverse, after(x_perm, q_perm))
    y_conjugate = after(q_inverse, after(y_perm, q_perm))
    x_expression = graph["data"][x_conjugate][1]
    y_expression = graph["data"][y_conjugate][1]
    action = np.concatenate(
        (product(q_matrix, x_expression), product(q_matrix, y_expression)), axis=0
    )
    columns = []
    for column in range(h_basis.shape[1]):
        transformed = (action @ h_basis[:, column]) % FIELD
        coordinates = coordinates_in_columns(full_basis, transformed)
        columns.append(coordinates[coboundary_dimension:])
    return np.asarray(columns, dtype=np.int64).T % FIELD


def sl_recompute(
    x_perm: tuple[int, ...],
    y_perm: tuple[int, ...],
    x_heart: np.ndarray,
    y_heart: np.ndarray,
    theta: np.ndarray,
    tau: np.ndarray,
) -> dict[str, Any]:
    pure_x = block_diagonal([x_heart, x_heart, x_heart])
    pure_y = block_diagonal([y_heart, y_heart, y_heart])
    graph = cayley_cocycle_graph(x_perm, y_perm, pure_x, pure_y)
    z_basis = kernel_columns(graph["constraints"])
    coboundaries = np.concatenate(
        (identity(21) - pure_x, identity(21) - pure_y), axis=0
    ) % FIELD
    _, pivot_columns = reduced_row_echelon(coboundaries)
    b_basis = coboundaries[:, pivot_columns]
    full_basis = extend_independent_columns(b_basis, z_basis)
    h_basis = full_basis[:, b_basis.shape[1] :]
    theta_action = quotient_action(
        graph,
        x_perm,
        y_perm,
        S_PERM,
        theta,
        full_basis,
        h_basis,
        b_basis.shape[1],
    )
    tau_action = quotient_action(
        graph,
        x_perm,
        y_perm,
        T_PERM,
        tau,
        full_basis,
        h_basis,
        b_basis.shape[1],
    )
    invariant_relations = np.concatenate(
        (theta_action - identity(h_basis.shape[1]), tau_action - identity(h_basis.shape[1])),
        axis=0,
    ) % FIELD
    invariant_dimension = h_basis.shape[1] - matrix_rank(invariant_relations)
    return {
        "P_order": len(graph["elements"]),
        "P_positive_edges": graph["positive_edges"],
        "P_collision_edges": graph["collision_edges"],
        "P_relation_rank": graph["relation_rank"],
        "P_relation_rref_sha256_alt_basis": graph[
            "relation_rref_sha256_alt_basis"
        ],
        "Z1_P_V_dimension": z_basis.shape[1],
        "B1_P_V_dimension": b_basis.shape[1],
        "H1_P_V_dimension": h_basis.shape[1],
        "H1_P_V_theta_action": theta_action.tolist(),
        "H1_P_V_tau_action": tau_action.tolist(),
        "H1_P_V_Q3_invariant_dimension": invariant_dimension,
        "H1_barW_dimension": invariant_dimension,
        "H1_barW_order": FIELD**invariant_dimension,
    }


def gauge_census(
    theta_base: np.ndarray,
    tau_base: np.ndarray,
    rho_x: np.ndarray,
    rho_y: np.ndarray,
) -> dict[str, Any]:
    candidates = []
    for theta_signs in itertools.product((1, 2), repeat=3):
        theta = product(
            theta_base,
            block_diagonal([sign * identity(7) for sign in theta_signs]),
        )
        for tau_signs in itertools.product((1, 2), repeat=3):
            tau = product(
                tau_base,
                block_diagonal([sign * identity(7) for sign in tau_signs]),
            )
            sigma_1 = product(matrix_power(tau, 2), theta)
            sigma_2 = product(theta, matrix_power(tau, 2))
            if not np.array_equal(product(theta, theta), identity(21)):
                continue
            if not np.array_equal(matrix_power(tau, 3), identity(21)):
                continue
            if np.array_equal(product(sigma_1, sigma_1), rho_x) and np.array_equal(
                product(sigma_2, sigma_2), rho_y
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
        for signs in itertools.product((1, 2), repeat=3):
            diagonal = block_diagonal([sign * identity(7) for sign in signs])
            transformed_theta = product(product(diagonal, theta), diagonal)
            transformed_tau = product(product(diagonal, tau), diagonal)
            orbit.add(
                keys[(tuple(transformed_theta.flatten()), tuple(transformed_tau.flatten()))]
            )
            stabilizer += int(
                np.array_equal(transformed_theta, theta)
                and np.array_equal(transformed_tau, tau)
            )
        orbit_sets.add(tuple(sorted(orbit)))
        stabilizers.append(stabilizer)
    return {
        "anchor_solutions": len(candidates),
        "orbit_count": len(orbit_sets),
        "orbit_sizes": sorted(len(orbit) for orbit in orbit_sets),
        "full_gauge_stabilizer_sizes": sorted(set(stabilizers)),
        "effective_gauge_order": 4,
    }


def gamma_audit(
    theta: np.ndarray,
    tau: np.ndarray,
    source_classes: list[dict[str, Any]],
    change_21: np.ndarray,
) -> dict[str, Any]:
    condition = np.zeros((42, 42), dtype=np.int64)
    condition[:21, :21] = (identity(21) + theta) % FIELD
    condition[21:, 21:] = (
        identity(21) + tau + product(tau, tau)
    ) % FIELD
    z_basis = kernel_columns(condition)
    coboundaries = np.concatenate(
        (identity(21) - theta, identity(21) - tau), axis=0
    ) % FIELD
    _, pivot_columns = reduced_row_echelon(coboundaries)
    b_basis = coboundaries[:, pivot_columns]
    full_basis = extend_independent_columns(b_basis, z_basis)
    h_basis = full_basis[:, b_basis.shape[1] :]
    coordinates = set()
    cocycle_residual_ranks = Counter()
    for source in source_classes:
        producer_vector = matrix(source["representative"]).reshape(-1)
        vector = np.concatenate(
            (
                change_21 @ producer_vector[:21],
                change_21 @ producer_vector[21:],
            )
        ) % FIELD
        cocycle_residual_ranks[matrix_rank((condition @ vector).reshape(-1, 1))] += 1
        coordinate = coordinates_in_columns(full_basis, vector)[b_basis.shape[1] :]
        coordinates.add(tuple(int(value) for value in coordinate))
    return {
        "condition_rank": matrix_rank(condition),
        "Z1_dimension": z_basis.shape[1],
        "B1_dimension": b_basis.shape[1],
        "H1_dimension": h_basis.shape[1],
        "H1_order": FIELD**h_basis.shape[1],
        "source_class_count": len(source_classes),
        "distinct_quotient_coordinates": len(coordinates),
        "zero_quotient_coordinate_count": sum(
            not any(coordinate) for coordinate in coordinates
        ),
        "cocycle_residual_rank_distribution": dict(cocycle_residual_ranks),
    }


def compare(
    mismatches: list[dict[str, Any]],
    location: str,
    field: str,
    producer: object,
    checker: object,
) -> None:
    if producer != checker and len(mismatches) < 40:
        mismatches.append(
            {
                "location": location,
                "field": field,
                "producer": producer,
                "checker": checker,
            }
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="search/certs/vnbit_compact_preflight_v3_20260813.json",
    )
    parser.add_argument(
        "--output",
        default="search/certs/vnbit_compact_preflight_check_v3_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/vnbit_compact_preflight_check_v3_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=180)
    args = parser.parse_args()
    input_path = ROOT / args.input
    output_path = ROOT / args.output
    checkpoint_path = ROOT / args.checkpoint
    began = time.monotonic()
    state: dict[str, Any] = {
        "schema": "vnbit_compact_preflight_check_checkpoint/v3",
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
        source = json.loads(input_path.read_text(encoding="utf-8"))
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
        x_perm = permutation_power(sigma_1_perm, 2)
        y_perm = permutation_power(sigma_2_perm, 2)
        x_heart = alternate_heart(x_perm)
        y_heart = alternate_heart(y_perm)
        rho_x = module_action(x_heart, (1, 0))
        rho_y = module_action(y_heart, (0, 1))
        theta_base = block_transport(s_heart, (1, 0, 2))
        tau_base = block_transport(t_heart, (2, 0, 1))

        cyclic = Counter()
        for coordinates in itertools.product(range(FIELD), repeat=7):
            if any(coordinates):
                cyclic[
                    cyclic_span_dimension(
                        np.asarray(coordinates, dtype=np.int64), (x_heart, y_heart)
                    )
                ] += 1
        centralizer_dim, centralizer_digest = centralizer_dimension(
            (x_heart, y_heart)
        )
        c9 = {
            "nonzero_cyclic_submodule_dimension_distribution": dict(cyclic),
            "endomorphism_ring_F3_dimension": centralizer_dim,
            "V7_absolutely_irreducible": cyclic == Counter({7: 2186})
            and centralizer_dim == 1,
            "endomorphism_relation_rref_sha256_alt_basis": centralizer_digest,
        }
        compare(
            mismatches,
            "C9",
            "cyclic_distribution",
            source["C9"]["nonzero_cyclic_submodule_dimension_distribution"],
            {str(key): value for key, value in cyclic.items()},
        )
        compare(
            mismatches,
            "C9",
            "endomorphism_dimension",
            source["C9"]["endomorphism_ring_F3_dimension"],
            centralizer_dim,
        )
        compare(
            mismatches,
            "C9",
            "absolute_irreducibility",
            source["C9"]["V7_absolutely_irreducible"],
            c9["V7_absolutely_irreducible"],
        )
        gauge = gauge_census(theta_base, tau_base, rho_x, rho_y)
        for field in (
            "anchor_solutions",
            "orbit_count",
            "orbit_sizes",
            "full_gauge_stabilizer_sizes",
            "effective_gauge_order",
        ):
            compare(mismatches, "gauge", field, source["gauge"][field], gauge[field])
        update("C9_and_gauge", mismatch_count=len(mismatches))

        window_results = []
        signs_by_eps = {"+": (2, 2, 1), "-": (1, 1, 2)}
        for source_window in source["windows"]:
            eps = source_window["eps"]
            theta = product(
                theta_base,
                block_diagonal(
                    [sign * identity(7) for sign in signs_by_eps[eps]]
                ),
            )
            tau = tau_base.copy()
            source_theta_alt = product(
                product(change_21, matrix(source_window["theta_matrix"])),
                change_21_inverse,
            )
            source_tau_alt = product(
                product(change_21, matrix(source_window["tau_matrix"])),
                change_21_inverse,
            )
            compare(
                mismatches,
                f"window[{eps}]",
                "theta_normal_form",
                source_theta_alt.tolist(),
                theta.tolist(),
            )
            compare(
                mismatches,
                f"window[{eps}]",
                "tau_normal_form",
                source_tau_alt.tolist(),
                tau.tolist(),
            )
            pure = marked_elements([0] * 42, theta, tau)
            compare(
                mismatches,
                f"window[{eps}]",
                "pure_x",
                pure["x"].action.tolist(),
                rho_x.tolist(),
            )
            compare(
                mismatches,
                f"window[{eps}]",
                "pure_y",
                pure["y"].action.tolist(),
                rho_y.tolist(),
            )
            ker_theta = 21 - matrix_rank((identity(21) + theta) % FIELD)
            ker_tau = 21 - matrix_rank(
                (identity(21) + tau + product(tau, tau)) % FIELD
            )
            gamma = gamma_audit(
                theta,
                tau,
                source_window["gamma_cohomology"]["classes"],
                change_21,
            )
            sl = sl_recompute(x_perm, y_perm, x_heart, y_heart, theta, tau)
            numeric_pairs = {
                "dim_ker_I_plus_theta": ker_theta,
                "dim_ker_I_plus_tau_plus_tau2": ker_tau,
                "gamma_Z1_dimension": gamma["Z1_dimension"],
                "gamma_B1_dimension": gamma["B1_dimension"],
                "gamma_H1_dimension": gamma["H1_dimension"],
                "gamma_H1_order": gamma["H1_order"],
                "H1_barW_order": sl["H1_barW_order"],
                "surjective_class_count": gamma["H1_order"]
                - sl["H1_barW_order"],
            }
            source_pairs = {
                "dim_ker_I_plus_theta": source_window[
                    "dim_ker_I_plus_theta"
                ],
                "dim_ker_I_plus_tau_plus_tau2": source_window[
                    "dim_ker_I_plus_tau_plus_tau2"
                ],
                "gamma_Z1_dimension": source_window["gamma_cohomology"][
                    "Z1_dimension"
                ],
                "gamma_B1_dimension": source_window["gamma_cohomology"][
                    "B1_dimension"
                ],
                "gamma_H1_dimension": source_window["gamma_cohomology"][
                    "H1_dimension"
                ],
                "gamma_H1_order": source_window["gamma_cohomology"]["H1_order"],
                "H1_barW_order": source_window["H1_barW_order"],
                "surjective_class_count": source_window["surjective_class_count"],
            }
            for field, checker_value in numeric_pairs.items():
                compare(
                    mismatches,
                    f"window[{eps}]",
                    field,
                    source_pairs[field],
                    checker_value,
                )
            for field in (
                "P_order",
                "P_positive_edges",
                "P_collision_edges",
                "P_relation_rank",
                "Z1_P_V_dimension",
                "B1_P_V_dimension",
                "H1_P_V_dimension",
                "H1_P_V_Q3_invariant_dimension",
                "H1_barW_dimension",
                "H1_barW_order",
            ):
                compare(
                    mismatches,
                    f"window[{eps}].SL_RE",
                    field,
                    source_window["SL_RE"][field],
                    sl[field],
                )
            marked_surjective = sum(
                entry["surjective"] is True
                for entry in source_window["gamma_cohomology"]["classes"]
            )
            compare(
                mismatches,
                f"window[{eps}]",
                "marked_surjective_classes",
                marked_surjective,
                numeric_pairs["surjective_class_count"],
            )
            window_results.append(
                {
                    "eps": eps,
                    **numeric_pairs,
                    "gamma_class_audit": gamma,
                    "SL_RE": sl,
                }
            )
            update(
                f"window_{eps}",
                eps=eps,
                mismatch_count=len(mismatches),
            )

        result = {
            "schema": "vnbit_compact_preflight_check/v3",
            "run_id": "vnbit-compact-preflight-check-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "checker": {
                "script": "search/check_vnbit_compact_preflight_v3.py",
                "script_sha256": file_digest(Path(__file__)),
                "shared_checker_primitives": "search/check_vnbit_compact_mainrun_v3.py",
                "shared_checker_primitives_sha256": file_digest(
                    ROOT / "search/check_vnbit_compact_mainrun_v3.py"
                ),
                "imports_producer": False,
                "basis": "e_i-e_0 (1<=i<=7), eliminate e_8-e_0",
            },
            "input": {args.input: file_digest(input_path)},
            "C9": c9,
            "gauge": gauge,
            "windows": window_results,
            "cross_eps": {
                "dim_ker_sum": sum(
                    item["dim_ker_I_plus_theta"] for item in window_results
                ),
                "H1_orders": [item["gamma_H1_order"] for item in window_results],
            },
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
    except BaseException as error:
        update("exception", error_type=type(error).__name__, error_message=str(error))
        raise
    finally:
        alarm.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
