#!/usr/bin/env python3
"""Helper-independent checker for task 129 inventory and size cert.

The modular dimension is reconstructed without importing the producer and
without using AtlasRep's stored minimum: an explicit 9-point L2(8) action is
closed, its 2^3:7 stabilizer gives the dimension lower bound, and every one of
the 2186 nonzero vectors in the 7-dimensional F3 permutation heart is checked.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
import threading
import time
from collections import Counter, deque
from itertools import product
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
Perm = tuple[int, ...]
Vector = tuple[int, ...]
Matrix = tuple[tuple[int, ...], ...]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def cycle_permutation(degree: int, cycles: Iterable[tuple[int, ...]]) -> Perm:
    result = list(range(degree))
    for cycle in cycles:
        for left, right in zip(cycle, cycle[1:] + cycle[:1]):
            result[left] = right
    return tuple(result)


def multiply(left: Perm, right: Perm) -> Perm:
    return tuple(right[left[index]] for index in range(len(left)))


def inverse(value: Perm) -> Perm:
    result = [0] * len(value)
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)


def closure(generators: tuple[Perm, ...]) -> set[Perm]:
    identity = tuple(range(len(generators[0])))
    result = {identity}
    queue = deque([identity])
    steps = generators + tuple(inverse(value) for value in generators)
    while queue:
        current = queue.popleft()
        for step in steps:
            nxt = multiply(current, step)
            if nxt not in result:
                result.add(nxt)
                queue.append(nxt)
    return result


def element_order(value: Perm) -> int:
    identity = tuple(range(len(value)))
    current = identity
    for exponent in range(1, 100):
        current = multiply(current, value)
        if current == identity:
            return exponent
    raise RuntimeError("element order bound")


def conjugate(value: Perm, actor: Perm) -> Perm:
    return multiply(multiply(inverse(actor), value), actor)


def heart_matrix(permutation: Perm) -> Matrix:
    # A=ker(sum:F3^9->F3), basis a_i=e_i-e_8 (i=0..7).
    # In A/<all-ones>, a_7=-sum_{i=0}^6 a_i.
    def quotient_a(index: int) -> list[int]:
        if index == 8:
            return [0] * 7
        if index == 7:
            return [2] * 7
        result = [0] * 7
        result[index] = 1
        return result

    columns = []
    for index in range(7):
        left = quotient_a(permutation[index])
        right = quotient_a(permutation[8])
        columns.append([(x - y) % 3 for x, y in zip(left, right)])
    return tuple(
        tuple(columns[column][row] for column in range(7)) for row in range(7)
    )


def matrix_vector(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(7)) % 3
        for row in range(7)
    )


def add_to_basis(basis: list[list[int]], value: Vector) -> bool:
    row = [entry % 3 for entry in value]
    for pivot, current in enumerate(basis):
        pivot_column = next(index for index, entry in enumerate(current) if entry)
        if row[pivot_column]:
            scalar = row[pivot_column]
            row = [(x - scalar * y) % 3 for x, y in zip(row, current)]
    if not any(row):
        return False
    pivot_column = next(index for index, entry in enumerate(row) if entry)
    inverse_pivot = pow(row[pivot_column], -1, 3)
    row = [(entry * inverse_pivot) % 3 for entry in row]
    for index, current in enumerate(basis):
        if current[pivot_column]:
            scalar = current[pivot_column]
            basis[index] = [
                (x - scalar * y) % 3 for x, y in zip(current, row)
            ]
    basis.append(row)
    basis.sort(key=lambda current: next(i for i, entry in enumerate(current) if entry))
    return True


def cyclic_dimension(vector: Vector, matrices: tuple[Matrix, ...]) -> int:
    basis: list[list[int]] = []
    queue: deque[Vector] = deque()
    if add_to_basis(basis, vector):
        queue.append(vector)
    while queue:
        current = queue.popleft()
        for matrix in matrices:
            nxt = matrix_vector(matrix, current)
            if add_to_basis(basis, nxt):
                queue.append(nxt)
    return len(basis)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", default="search/certs/g3bridge_inventory_v1_20260813.json"
    )
    parser.add_argument(
        "--output",
        default="search/certs/g3bridge_inventory_v1_check_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/g3bridge_inventory_v1_check_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    source_path = ROOT / args.input
    output_path = ROOT / args.output
    checkpoint_path = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "g3bridge_inventory_check_checkpoint/v1",
        "stage": "start",
        "complete": False,
    }
    atomic_json(checkpoint_path, state)

    def update(stage: str, **fields: object) -> None:
        state.update(
            stage=stage,
            elapsed_ms=int(1000 * (time.monotonic() - started)),
            **fields,
        )
        atomic_json(checkpoint_path, state)

    def hard_timeout() -> None:
        if not state.get("complete"):
            update("hard_timeout")
            os._exit(124)

    timer = threading.Timer(args.hard_timeout_seconds, hard_timeout)
    timer.daemon = True
    timer.start()
    try:
        source = json.loads(source_path.read_text(encoding="utf-8"))
        checks: dict[str, bool] = {}
        checks["schema"] = source["schema"] == "g3bridge_inventory/v1"
        checks["producer_sha256_inputs"] = all(
            digest(ROOT / name) == value
            for name, value in source["input_sha256"].items()
        )

        phase2 = json.loads(
            (ROOT / "search/certs/d972_phase2_coord_v1_20260813.json").read_text(
                encoding="utf-8"
            )
        )["group_order_receipts"]
        expected_rows = {}
        for level in (9, 27, 36, 108):
            g_order = int(phase2["canonical_gn_orders"][str(level)])
            e_order = int(phase2["roof_orders"][str(level)])
            expected_rows[f"K{level}_cap_NS4"] = {
                "E_order": e_order,
                "V_order": g_order // 108,
                "G_vN_0": True,
                "G_vN_1": level != 9,
                "G_vN_2": g_order // 108 != 1,
                "G_vN_3": False,
                "tensor_type_raw_boolean": False,
            }
        actual_rows = {
            row["inventory_id"]: row
            for row in source["inventory_scan"]["task125_rows"]
        }
        checks["task125_rows"] = set(actual_rows) == set(expected_rows) and all(
            all(actual_rows[key][field] == value for field, value in row.items())
            for key, row in expected_rows.items()
        )

        target83 = json.loads(
            (ROOT / "search/certs/wincnotn_v1_20260812.json").read_text(
                encoding="utf-8"
            )
        )["win_cnotn_target_members"]
        target83_orders = [int(row["index"]) for row in target83]
        target_summary = source["inventory_scan"]["target83"]
        checks["target83_order_obstruction"] = (
            len(target83) == 83
            and max(target83_orders) <= 2000
            and target_summary["G_vN_0_false_count"] == 83
            and target_summary["tensor_type_hit_count"] == 0
        )

        atlas_path = ROOT / "search/probe/atlas_stats/atlas_features_v1.csv"
        with atlas_path.open(encoding="utf-8", newline="") as handle:
            atlas_rows = list(csv.DictReader(handle))
        typed = [row for row in atlas_rows if "isolated=TRUE" in row.get("note", "")]
        checks["atlas_typed_inventory"] = (
            len(typed) == 1
            and typed[0]["window_id"].startswith("W-5")
            and int(typed[0]["G_order"]) == 1000
            and source["inventory_scan"]["atlas"]["csv_record_count"]
            == len(atlas_rows)
        )
        checks["finite_inventory_zero_hits"] = (
            source["inventory_scan"]["finite_inventory_tensor_type_hit_count"] == 0
            and not source["inventory_scan"]["universe_pin"]["global_absence_claimed"]
            and not source["inventory_scan"]["universe_pin"][
                "task125_effective_dovetail_exhausted"
            ]
        )
        update("inventory_recomputed")

        # Explicit Atlas standard generators on nine points, converted to 0-base.
        generator_a = cycle_permutation(
            9, ((0, 1), (2, 3), (5, 6), (7, 8))
        )
        generator_b = cycle_permutation(
            9, ((0, 2, 1), (3, 4, 5), (6, 7, 8))
        )
        group = closure((generator_a, generator_b))
        stabilizer = {value for value in group if value[8] == 8}
        order_distribution = Counter(element_order(value) for value in stabilizer)
        elementary = {
            value for value in stabilizer if element_order(value) in (1, 2)
        }
        actor7 = next(value for value in stabilizer if element_order(value) == 7)
        nonidentity = next(value for value in elementary if element_order(value) == 2)
        orbit = []
        current = nonidentity
        for _ in range(7):
            orbit.append(current)
            current = conjugate(current, actor7)
        checks["L2_8_order"] = len(group) == 504
        checks["point_stabilizer_2cubed_by_7"] = (
            len(stabilizer) == 56
            and order_distribution == Counter({1: 1, 2: 7, 7: 48})
            and len(elementary) == 8
            and len(closure(tuple(elementary))) == 8
            and set(orbit) == elementary - {tuple(range(9))}
        )

        matrices = (heart_matrix(generator_a), heart_matrix(generator_b))
        cyclic_dimensions = Counter()
        for vector in product(range(3), repeat=7):
            if any(vector):
                cyclic_dimensions[cyclic_dimension(vector, matrices)] += 1
        checks["heart_irreducible_all_nonzero_vectors"] = cyclic_dimensions == Counter(
            {7: 2186}
        )
        reconstructed_dim_p = 7 if all(
            checks[name]
            for name in (
                "L2_8_order",
                "point_stabilizer_2cubed_by_7",
                "heart_irreducible_all_nonzero_vectors",
            )
        ) else None
        checks["dim_V_P"] = (
            reconstructed_dim_p
            == source["dimension_gate"]["P"][
                "minimum_nontrivial_module_dimension"
            ]
            == 7
        )
        update("module_dimension_reconstructed", dim_V_P=reconstructed_dim_p)

        g3_ab = json.loads(
            (ROOT / "search/certs/d972_entangled_hand2_v1_20260813.json").read_text(
                encoding="utf-8"
            )
        )["surjective_kernel_orbit"]["intersection_quotient_abelianization_order"]
        checks["dim_V_G3"] = (
            g3_ab == 4
            and source["dimension_gate"]["G3"][
                "minimum_nontrivial_module_dimension"
            ]
            == 1
        )

        expected_sizes = []
        for dim_g3 in (1, 2):
            dim_v = 7 * dim_g3
            e_order = 54432 * 3**dim_v
            permutation_degree_floor = 1
            while math.factorial(permutation_degree_floor) < e_order:
                permutation_degree_floor += 1
            tuple_bytes = sys.getsizeof(tuple(range(permutation_degree_floor)))
            expected_sizes.append(
                (
                    dim_v,
                    e_order,
                    e_order,
                    27 * e_order,
                    None,
                    permutation_degree_floor,
                    tuple_bytes,
                    tuple_bytes * e_order,
                    tuple_bytes * e_order <= 8 * 2**30,
                )
            )
        actual_sizes = [
            (
                row["dim_V"],
                row["E_order"],
                row["PB3_over_K9_cap_NE_order_lower_bound"],
                row["PB3_over_K9_cap_NE_order_upper_bound"],
                row["PB3_over_K9_cap_NE_order_exact"],
                row["faithful_permutation_degree_lower_bound"],
                row["python_tuple_bytes_at_degree_lower_bound"],
                row["one_tuple_per_E_element_bytes"],
                row["within_8GiB_existing_tuple_floor"],
            )
            for row in source["scale_gate"]["rows"]
        ]
        checks["size_rows"] = actual_sizes == expected_sizes
        checks["memory_stop"] = (
            expected_sizes[0][7] == 16189818624
            and not expected_sizes[0][8]
            and not source["scale_gate"][
                "minimum_case_within_existing_enumerator_memory_gate"
            ]
        )
        boundary = source["stage_boundary"]
        checks["stage_boundary"] = (
            boundary["stage_reached"] == 2
            and not boundary["E_constructed"]
            and not boundary["P_vN_1_instantiated"]
            and not boundary["rigidity_measurement_performed"]
            and boundary["raw_image_size"] is None
            and boundary["status"] == "UNKNOWN"
        )
        checks["noncontact"] = not any(
            source["scope"][name]
            for name in (
                "u_touched",
                "c_touched",
                "sealed_quantities_touched",
                "sealed_k5_touched",
                "preregistered_quantities_read",
                "finite_depth_B_type_recognition",
            )
        )

        result = {
            "schema": "g3bridge_inventory_check/v1",
            "checked_input": str(source_path.relative_to(ROOT)),
            "checked_input_sha256": digest(source_path),
            "checks": checks,
            "all_equalities_true": all(checks.values()),
            "independent_module_reconstruction": {
                "group_order": len(group),
                "point_stabilizer_order": len(stabilizer),
                "point_stabilizer_element_order_distribution": dict(
                    sorted(order_distribution.items())
                ),
                "normal_elementary_2_subgroup_order": len(elementary),
                "C7_orbit_on_nontrivial_weights_size": len(set(orbit)),
                "lower_bound_argument": (
                    "a nontrivial P-module is faithful; restriction to 2^3 has a "
                    "nontrivial F3 weight, and C7 permutes all seven nontrivial "
                    "weights transitively, so dimension is at least seven"
                ),
                "heart_dimension": 7,
                "nonzero_vectors_checked": 2186,
                "cyclic_dimension_distribution": dict(
                    sorted(cyclic_dimensions.items())
                ),
                "reconstructed_minimum": reconstructed_dim_p,
            },
            "elapsed_ms": int(1000 * (time.monotonic() - started)),
        }
        atomic_json(output_path, result)
        state["complete"] = True
        update("complete", output=str(output_path.relative_to(ROOT)))
        return 0 if result["all_equalities_true"] else 1
    finally:
        timer.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
