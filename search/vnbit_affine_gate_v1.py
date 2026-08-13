#!/usr/bin/env python3
"""Task 130 producer: C-0/C-1, the natural 21-dimensional module, and C-3 preflight.

This program deliberately stops before forming any task-130 preregistration or
lift table.  The compact-route source does not specify the marked epimorphism
PB3 -> V semidirect W whose kernel is denoted N_E.  The output records the
linear data available before that missing choice and quantifies the associated
marked-lift ambiguity.
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
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULUS = 3
DIM_P = 7
CHARACTERS = ((1, 0), (0, 1), (1, 1))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def object_digest(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def identity_permutation(degree: int) -> tuple[int, ...]:
    return tuple(range(degree))


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Function composition left after right."""
    return tuple(left[right[i]] for i in range(len(left)))


def inverse_permutation(value: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(value)
    for source, target in enumerate(value):
        result[target] = source
    return tuple(result)


def permutation_power(value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    if exponent < 0:
        return permutation_power(inverse_permutation(value), -exponent)
    result = identity_permutation(len(value))
    power = value
    while exponent:
        if exponent & 1:
            result = compose(power, result)
        power = compose(power, power)
        exponent >>= 1
    return result


def permutation_order(value: tuple[int, ...]) -> int:
    current = identity_permutation(len(value))
    for exponent in range(1, 10_000):
        current = compose(value, current)
        if current == identity_permutation(len(value)):
            return exponent
    raise RuntimeError("permutation order bound exceeded")


def permutation_group(
    generators: tuple[tuple[int, ...], ...]
) -> set[tuple[int, ...]]:
    all_generators = generators + tuple(inverse_permutation(g) for g in generators)
    identity = identity_permutation(len(generators[0]))
    found = {identity}
    queue = [identity]
    while queue:
        current = queue.pop()
        for generator in all_generators:
            candidate = compose(generator, current)
            if candidate not in found:
                found.add(candidate)
                queue.append(candidate)
    return found


def gf8_multiply(left: int, right: int) -> int:
    raw = 0
    for bit in range(3):
        if (right >> bit) & 1:
            raw ^= left << bit
    # x^3 + x + 1, encoded as 0b1011.
    for bit in (4, 3):
        if (raw >> bit) & 1:
            raw ^= 0b1011 << (bit - 3)
    return raw


def gf8_inverse(value: int) -> int:
    if value == 0:
        raise ZeroDivisionError("zero in GF(8)")
    return next(candidate for candidate in range(1, 8) if gf8_multiply(value, candidate) == 1)


def mobius_permutation(matrix: tuple[int, int, int, int]) -> tuple[int, ...]:
    a, b, c, d = matrix
    result = [0 if c == 0 else 1 + gf8_multiply(a, gf8_inverse(c))]
    for value in range(8):
        numerator = gf8_multiply(a, value) ^ b
        denominator = gf8_multiply(c, value) ^ d
        result.append(
            0
            if denominator == 0
            else 1 + gf8_multiply(numerator, gf8_inverse(denominator))
        )
    return tuple(result)


def zero_matrix(rows: int, columns: int) -> list[list[int]]:
    return [[0] * columns for _ in range(rows)]


def identity_matrix(dimension: int) -> list[list[int]]:
    return [[int(row == column) for column in range(dimension)] for row in range(dimension)]


def matrix_product(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(left[row][middle] * right[middle][column] for middle in range(len(right)))
            % MODULUS
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def matrix_sum(*matrices: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(matrix[row][column] for matrix in matrices) % MODULUS
            for column in range(len(matrices[0][0]))
        ]
        for row in range(len(matrices[0]))
    ]


def matrix_difference(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [
            (left[row][column] - right[row][column]) % MODULUS
            for column in range(len(left[0]))
        ]
        for row in range(len(left))
    ]


def scalar_matrix_product(scalar: int, matrix: list[list[int]]) -> list[list[int]]:
    return [[scalar * entry % MODULUS for entry in row] for row in matrix]


def block_diagonal(blocks: list[list[list[int]]]) -> list[list[int]]:
    dimension = sum(len(block) for block in blocks)
    result = zero_matrix(dimension, dimension)
    offset = 0
    for block in blocks:
        for row in range(len(block)):
            for column in range(len(block)):
                result[offset + row][offset + column] = block[row][column]
        offset += len(block)
    return result


def matrix_rank(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    rank = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column] % MODULUS),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, MODULUS)
        work[rank] = [entry * inverse % MODULUS for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column] % MODULUS:
                factor = work[row][column] % MODULUS
                work[row] = [
                    (work[row][index] - factor * work[rank][index]) % MODULUS
                    for index in range(columns)
                ]
        rank += 1
    return rank


def matrix_nullity(matrix: list[list[int]]) -> int:
    return len(matrix[0]) - matrix_rank(matrix)


def matrix_vector(matrix: list[list[int]], vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(len(vector)))
        % MODULUS
        for row in range(len(matrix))
    )


def heart_matrix(permutation: tuple[int, ...]) -> list[list[int]]:
    """The 9-point augmentation heart, basis u_0,...,u_6 modulo sum u_i."""
    result = zero_matrix(DIM_P, DIM_P)
    for column in range(DIM_P):
        vector = [0] * 9
        vector[permutation[column]] = (vector[permutation[column]] + 1) % MODULUS
        vector[permutation[8]] = (vector[permutation[8]] - 1) % MODULUS
        coefficients = vector[:8]
        for row in range(DIM_P):
            result[row][column] = (coefficients[row] - coefficients[7]) % MODULUS
    return result


def cyclic_submodule_dimension(
    seed: tuple[int, ...], generators: tuple[list[list[int]], ...]
) -> int:
    vectors: list[tuple[int, ...]] = []
    queue = [seed]
    while queue:
        vector = queue.pop()
        if matrix_rank([list(item) for item in vectors + [vector]]) == len(vectors):
            continue
        vectors.append(vector)
        for generator in generators:
            queue.append(matrix_vector(generator, vector))
    return len(vectors)


def invert_matrix_mod2(matrix: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    for entries in product(range(2), repeat=4):
        candidate = (entries[:2], entries[2:])
        if all(
            sum(matrix[row][middle] * candidate[middle][column] for middle in range(2))
            % 2
            == int(row == column)
            for row in range(2)
            for column in range(2)
        ):
            return candidate
    raise RuntimeError("singular matrix over F2")


def dual_destination(
    character: tuple[int, int], automorphism: tuple[tuple[int, int], tuple[int, int]]
) -> tuple[int, int]:
    inverse = invert_matrix_mod2(automorphism)
    return tuple(
        sum(inverse[column][row] * character[column] for column in range(2)) % 2
        for row in range(2)
    )


def extended_operator(
    p_operator: list[list[int]],
    abelian_automorphism: tuple[tuple[int, int], tuple[int, int]],
) -> list[list[int]]:
    result = zero_matrix(21, 21)
    indices = {character: index for index, character in enumerate(CHARACTERS)}
    for source, character in enumerate(CHARACTERS):
        target = indices[dual_destination(character, abelian_automorphism)]
        for row in range(DIM_P):
            for column in range(DIM_P):
                result[7 * target + row][7 * source + column] = p_operator[row][column]
    return result


def character_sign(character: tuple[int, int], value: tuple[int, int]) -> int:
    pairing = sum(character[index] * value[index] for index in range(2)) % 2
    return 2 if pairing else 1


def module_generator(
    p_matrix: list[list[int]], abelian_value: tuple[int, int]
) -> list[list[int]]:
    return block_diagonal(
        [
            scalar_matrix_product(character_sign(character, abelian_value), p_matrix)
            for character in CHARACTERS
        ]
    )


def ct_data() -> dict[str, object]:
    gap_root = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / (
        "GAP-4.16.0/runtime/opt/gap-4.16.0"
    )
    modular_path = gap_root / "pkg/ctbllib/data/ctbline1.tbl"
    ordinary_path = gap_root / "pkg/ctbllib/data/ctoline1.tbl"
    modular = modular_path.read_text(encoding="utf-8")
    ordinary = ordinary_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'MBT\("L2\(8\)",3,\s*TEXT1,\s*'
        r'\[1,1,2,3,4\],\s*\[2,0,0,0\],\s*\[\],\s*'
        r'\[\[\[1,6\],\[2,3,4,5,6\]\]\],\s*\[\],\s*0,\s*'
        r'\[\(3,4,5\)\],\s*0\);',
        re.DOTALL,
    )
    if pattern.search(modular) is None:
        raise RuntimeError("L2(8) characteristic-3 modular table record changed")
    ordinary_match = re.search(
        r'MOT\("L2\(8\)",(.*?)ARC\("L2\(8\)"', ordinary, re.DOTALL
    )
    if ordinary_match is None:
        raise RuntimeError("L2(8) ordinary table record changed")
    ordinary_record = re.sub(r"\s+", "", ordinary_match.group(1))
    degree_structure = (
        "[1,1,1,1,1,1,1,1,1]" in ordinary_record
        and "[7,-1,-2,0,0,0,1,1,1]" in ordinary_record
        and "[7,-1,1,0,0,0," in ordinary_record
        and "[GALOIS,[3,4]],[GALOIS,[3,2]],[8,0,-1,1,1,1,-1,-1,-1]"
        in ordinary_record
        and "[9,1,0," in ordinary_record
        and "[GALOIS,[7,3]],[GALOIS,[7,2]]]" in ordinary_record
    )
    class_centralizers = [504, 8, 9, 7, 7, 7, 9, 9, 9]
    if (
        str(class_centralizers).replace(" ", "") not in ordinary_record
        or not degree_structure
    ):
        raise RuntimeError("L2(8) ordinary character rows changed")

    # The principal block has ordinary degrees 1,7,7,7,7,8.  Its stored
    # Brauer tree has columns [1,6] and [2,3,4,5,6], hence decomposition
    # rows (1,0), four copies of (0,1), and (1,1).  The remaining three
    # degree-nine ordinary characters are defect-zero blocks.
    principal_ordinary_degrees = [1, 7, 7, 7, 7, 8]
    ordinary_character_degrees = principal_ordinary_degrees + [9, 9, 9]
    brauer_degrees = [1, 7, 9, 9, 9]
    if principal_ordinary_degrees[-1] != sum(brauer_degrees[:2]):
        raise RuntimeError("Brauer tree degree reconstruction mismatch")
    return {
        "modular_table_path": str(modular_path),
        "modular_table_sha256": digest(modular_path),
        "ordinary_table_path": str(ordinary_path),
        "ordinary_table_sha256": digest(ordinary_path),
        "ordinary_class_centralizer_orders": class_centralizers,
        "ordinary_character_degrees": ordinary_character_degrees,
        "stored_modular_block_assignment": [1, 1, 2, 3, 4],
        "stored_block_defects": [2, 0, 0, 0],
        "stored_principal_brauer_tree": [[1, 6], [2, 3, 4, 5, 6]],
        "stored_table_automorphism": [3, 4, 5],
        "brauer_degrees_characteristic_3": brauer_degrees,
        "seven_dimensional_irreducible_count": 1,
        "out_C3_orbits_on_brauer_positions": [[1], [2], [3, 4, 5]],
        "seven_dimensional_position": 2,
        "seven_dimensional_out_orbit_size": 1,
    }


def affine_fixture() -> dict[str, object]:
    # V=F3^2, W=C2 acts as diag(-1,1).  For f=(v,s), f^2 has
    # V-component (I+s)v.  The equation f^2=1 has exactly three solutions.
    action = [[2, 0], [0, 1]]
    affine_matrix = matrix_sum(identity_matrix(2), action)
    values = []
    solutions = []
    for vector in product(range(3), repeat=2):
        direct = tuple(
            (vector[index] + matrix_vector(action, vector)[index]) % 3
            for index in range(2)
        )
        predicted = matrix_vector(affine_matrix, vector)
        values.append(direct == predicted)
        if direct == (0, 0):
            solutions.append(list(vector))
    return {
        "fixture": "F3^2 semidirect C2, relation f^2=1",
        "action": action,
        "affine_matrix": affine_matrix,
        "constant_vector": [0, 0],
        "all_nine_values_affine": all(values),
        "solution_count": len(solutions),
        "solutions": solutions,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="search/certs/vnbit_affine_gate_raw_v1_20260813.json",
    )
    parser.add_argument(
        "--checkpoint",
        default="search/certs/vnbit_affine_gate_v1_checkpoint.json",
    )
    parser.add_argument("--hard-timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state: dict[str, object] = {
        "schema": "vnbit_affine_gate_checkpoint/v1",
        "stage": "start",
        "complete": False,
    }
    atomic_json(checkpoint, state)

    def update(stage: str, **fields: object) -> None:
        state.update(
            stage=stage,
            elapsed_ms=int(1000 * (time.monotonic() - started)),
            **fields,
        )
        atomic_json(checkpoint, state)

    def hard_timeout() -> None:
        if not state.get("complete"):
            update("hard_timeout")
            os._exit(124)

    timer = threading.Timer(args.hard_timeout_seconds, hard_timeout)
    timer.daemon = True
    timer.start()
    try:
        task_path = ROOT / "ops/inbox_codex/sol_task_130_affine.txt"
        route_path = ROOT / "docs/notes/vnbit_compact_route_v1.md"
        addendum_path = ROOT / "docs/notes/vnbit_compact_route_v1_addendum_novelty.md"
        p_source_path = ROOT / "search/week3-psl-S4.g"
        source_hashes = {
            str(path.relative_to(ROOT)): digest(path)
            for path in (task_path, route_path, addendum_path, p_source_path)
        }

        # Exact S4 marked matrices from search/week3-psl-S4.g.
        s_perm = mobius_permutation((1, 0, 1, 1))
        t_perm = mobius_permutation((4, 3, 1, 5))
        w_perm = compose(inverse_permutation(t_perm), s_perm)
        x_perm = permutation_power(w_perm, 2)
        y_perm = compose(t_perm, compose(x_perm, inverse_permutation(t_perm)))
        z_perm = inverse_permutation(compose(x_perm, y_perm))
        p_group = permutation_group((x_perm, y_perm))
        c0 = {
            "P_order": len(p_group),
            "S_order": permutation_order(s_perm),
            "T_order": permutation_order(t_perm),
            "X_order": permutation_order(x_perm),
            "Y_order": permutation_order(y_perm),
            "Z_order": permutation_order(z_perm),
            "S_in_P": s_perm in p_group,
            "T_in_P": t_perm in p_group,
            "theta_X_to_Y_by_S": compose(s_perm, compose(x_perm, s_perm)) == y_perm,
            "theta_Y_to_X_by_S": compose(s_perm, compose(y_perm, s_perm)) == x_perm,
            "tau_X_to_Y_by_T": (
                compose(t_perm, compose(x_perm, inverse_permutation(t_perm))) == y_perm
            ),
            "tau_Y_to_Z_by_T": (
                compose(t_perm, compose(y_perm, inverse_permutation(t_perm))) == z_perm
            ),
            "theta_on_P": "inner",
            "tau_on_P": "inner",
            "theta_conjugator": "S",
            "tau_conjugator": "T",
        }
        if not all(
            value
            for key, value in c0.items()
            if key.endswith("_in_P") or key.startswith("theta_") or key.startswith("tau_")
            if isinstance(value, bool)
        ) or len(p_group) != 504:
            raise RuntimeError("C-0 marked permutation reconstruction mismatch")
        update("C0_internal", P_order=len(p_group))

        c1 = ct_data()
        update("C1_brauer", seven_dimensional_count=1)

        r_s = heart_matrix(s_perm)
        r_t = heart_matrix(t_perm)
        r_x = heart_matrix(x_perm)
        r_y = heart_matrix(y_perm)
        r_z = heart_matrix(z_perm)
        cyclic_distribution: dict[str, int] = {}
        for vector in product(range(3), repeat=7):
            if not any(vector):
                continue
            dimension = cyclic_submodule_dimension(vector, (r_x, r_y))
            key = str(dimension)
            cyclic_distribution[key] = cyclic_distribution.get(key, 0) + 1
        if cyclic_distribution != {"7": 2186}:
            raise RuntimeError("heart irreducibility reconstruction mismatch")

        rho_x = module_generator(r_x, (1, 0))
        rho_y = module_generator(r_y, (0, 1))
        rho_z = module_generator(r_z, (1, 1))
        theta_ab = ((0, 1), (1, 0))
        tau_ab = ((0, 1), (1, 1))
        theta_operator = extended_operator(r_s, theta_ab)
        tau_operator = extended_operator(r_t, tau_ab)
        identity_21 = identity_matrix(21)
        tau_squared = matrix_product(tau_operator, tau_operator)
        module_checks = {
            "rho_XYZ_identity": matrix_rank(
                matrix_difference(
                    matrix_product(matrix_product(rho_x, rho_y), rho_z), identity_21
                )
            )
            == 0,
            "theta_squared_identity": matrix_rank(
                matrix_difference(matrix_product(theta_operator, theta_operator), identity_21)
            )
            == 0,
            "tau_cubed_identity": matrix_rank(
                matrix_difference(matrix_product(tau_squared, tau_operator), identity_21)
            )
            == 0,
            "theta_X_to_Y": matrix_rank(
                matrix_difference(
                    matrix_product(matrix_product(theta_operator, rho_x), theta_operator),
                    rho_y,
                )
            )
            == 0,
            "theta_Y_to_X": matrix_rank(
                matrix_difference(
                    matrix_product(matrix_product(theta_operator, rho_y), theta_operator),
                    rho_x,
                )
            )
            == 0,
            "tau_X_to_Y": matrix_rank(
                matrix_difference(
                    matrix_product(matrix_product(tau_operator, rho_x), tau_squared),
                    rho_y,
                )
            )
            == 0,
            "tau_Y_to_Z": matrix_rank(
                matrix_difference(
                    matrix_product(matrix_product(tau_operator, rho_y), tau_squared),
                    rho_z,
                )
            )
            == 0,
        }
        if not all(module_checks.values()):
            raise RuntimeError("21-dimensional module relation mismatch")
        module = {
            "field": "F3",
            "dim_V_P": 7,
            "dim_V_G3_orbit_bundle": 3,
            "dim_V": 21,
            "E_order_if_semidirect": 54_432 * 3**21,
            "P_heart_cyclic_dimension_distribution": cyclic_distribution,
            "G3_character_order": [list(character) for character in CHARACTERS],
            "rho_X": rho_x,
            "rho_Y": rho_y,
            "theta_operator": theta_operator,
            "tau_operator": tau_operator,
            "rho_generators_sha256": object_digest([rho_x, rho_y]),
            "outer_operators_sha256": object_digest([theta_operator, tau_operator]),
            "checks": module_checks,
        }
        update("C2_module", dim_V=21)

        norm_tau = matrix_sum(identity_21, tau_operator, tau_squared)
        coboundary = matrix_difference(theta_operator, identity_21) + matrix_difference(
            tau_operator, identity_21
        )
        h1_dimension = (
            matrix_nullity(matrix_sum(identity_21, theta_operator))
            + matrix_nullity(norm_tau)
            - matrix_rank(coboundary)
        )
        marked_lift_preflight = {
            "ambient_presentation": "B3/<c> = C2 * C3",
            "ker_I_plus_theta_dimension": matrix_nullity(
                matrix_sum(identity_21, theta_operator)
            ),
            "ker_I_plus_tau_plus_tau2_dimension": matrix_nullity(norm_tau),
            "coboundary_rank": matrix_rank(coboundary),
            "joint_invariant_dimension": matrix_nullity(coboundary),
            "H1_C2_free_C3_dimension": h1_dimension,
            "V_conjugacy_class_count_for_marked_lifts": 3**h1_dimension,
            "scope_note": (
                "This is the prequotient marked-lift class space. It is not a count "
                "of surjective PB3 kernels; generation, kernel equality, and a "
                "normalization still have to be supplied."
            ),
        }
        if marked_lift_preflight != {
            **marked_lift_preflight,
            "H1_C2_free_C3_dimension": 4,
            "V_conjugacy_class_count_for_marked_lifts": 81,
        }:
            raise RuntimeError("marked-lift cohomology dimension changed")

        fixture = affine_fixture()
        if not fixture["all_nine_values_affine"] or fixture["solution_count"] != 3:
            raise RuntimeError("affine fixture mismatch")

        target_definition_audit = {
            "E_group_type_constructed": True,
            "natural_theta_tau_module_intertwiners_constructed": True,
            "marked_epimorphism_PB3_to_E_specified_in_source": False,
            "V_component_of_marked_x_specified": False,
            "V_component_of_marked_y_specified": False,
            "marked_lift_normalization_specified": False,
            "surjective_marked_lift_class_selected": False,
            "kernel_equality_across_surjective_lifts_proved": False,
            "W_presentation_for_GEN_AFF_supplied": False,
            "natural_zero_section_image": "W only",
            "natural_zero_section_surjects_to_E": False,
            "consequence": (
                "The symbol N_E=ker(PB3->E) does not denote a unique target. "
                "The constants in x, y, x^u, y^u and hence b_t are unavailable."
            ),
            "matrix_shape_note": (
                "LIFT-AFF section 2 defines A by vertically stacking all vector "
                "relations. Two independent 21-component relations give a 42x21 "
                "system unless a reduction to 21x21 is separately proved; no such "
                "reduction is supplied."
            ),
        }

        result = {
            "schema": "vnbit_affine_gate_raw/v1",
            "run_id": "vnbit-affine-gate-"
            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "generated_by": {
                "script": "search/vnbit_affine_gate_v1.py",
                "script_sha256": digest(Path(__file__)),
            },
            "source_sha256": source_hashes,
            "C0": c0,
            "C1": c1,
            "C2": module,
            "marked_lift_preflight": marked_lift_preflight,
            "lift_affine_calibration": fixture,
            "target_definition_audit": target_definition_audit,
            "stage_boundary": {
                "stage_reached": "C2 plus natural-action preflight",
                "C0_internal": True,
                "C1_complete": True,
                "C2_rho_constructed": True,
                "C3_N_E_theta_tau_invariant": None,
                "C4_N_E_isolated": None,
                "C5_324_target_reformed": False,
                "C6_H1_W_V_measured": False,
                "task130_preregistration_created": False,
                "obstruction_classes_measured": 0,
                "lift_table_rows": 0,
                "theta2_rigidity_measured": False,
                "single_bit_image_size": None,
                "raw_image_size": None,
                "status": "UNKNOWN_STOP_MARKED_EPIMORPHISM_UNDEFINED",
            },
            "endgame_scope": (
                "A gentle-genuine branch requires the B4 layer: inspect PENT_W-PASS, "
                "then apply FAKE-KILL^{B4}/U-10; finite-depth data alone does not "
                "elevate a countercandidate. The other branch ends within gentle."
            ),
            "noncontact": {
                "u_touched": False,
                "c_touched": False,
                "sealed_quantities_touched": False,
                "sealed_k5_touched": False,
                "preregistered_values_972_324_modified": False,
                "finite_depth_B_type_recognition": False,
            },
            "gap_runtime": {
                "used_for_values": False,
                "note": (
                    "The requested wrapper was attempted separately in this session "
                    "and stopped before script loading with Win32 signal-pipe error 5."
                ),
            },
        }
        atomic_json(output, result)
        update("complete", complete=True, output_sha256=digest(output))
        return 0
    finally:
        timer.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
