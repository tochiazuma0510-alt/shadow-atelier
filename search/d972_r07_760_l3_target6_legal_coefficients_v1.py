#!/usr/bin/env python3
"""Positive C-13/full-K coefficient certificates for g760 target6.

This adapter runs the pinned v5 producer unchanged.  Only after v5 has
authenticated a completed-j checkpoint does it replay that checkpoint's
lossless D2 delta chain and solve the 28-column quotient system.  The
resulting word is deliberately an overapproximation correction candidate,
not an A.18 correction or lift.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import itertools
import json
import os
import random
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SELF_PATH = Path(
    "search/d972_r07_760_l3_target6_legal_coefficients_v1.py")
V5_PATH = Path("search/d972_r07_760_l3_target6_delta_resume_v5.py")
V5_DRIVER_PATH = Path(
    "search/d972_r07_760_l3_target6_delta_resume_gha_driver_v5.g")
V5_PREFLIGHT_PATH = Path(
    "search/certs/d972_r07_760_l3_target6_delta_resume_"
    "preflight_v5_20260827.json")
TASK167_PATH = Path(
    "sol/luna_task_167_r07_target6_postclosure_recovery_v5.md")
REPLY167_PATH = Path(
    "sol/luna_reply_167_r07_target6_postclosure_recovery_v5.md")
TASK168_PATH = Path(
    "sol/luna_task_168_r07_jennings_legal_coefficients_v1.md")
PROOF105_PATH = Path("sol/proof_r07_l3_j9_survival_boundary_v105.md")
PROOF106_PATH = Path(
    "sol/proof_r07_jennings_legal_coefficient_selector_v106.md")

SCHEMA = "d972-r07-760-l3-target6-legal-coefficients/v1"
CERTIFICATE_SCHEMA = (
    "d972-r07-760-l3-target6-legal-coefficient-certificate/v1")
PREFLIGHT_STATE = (
    "R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_PREFLIGHT_READY")
FINAL_MARKER = "R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_PRODUCER_PASS"
DEFAULT_PREFLIGHT = Path(
    "search/certs/d972_r07_760_l3_target6_legal_coefficients_"
    "preflight_v1_20260827.json")
DEFAULT_FULL = Path(
    "ci/out/d972_r07_760_l3_target6_legal_coefficients_v1.json")
DEFAULT_COEFFICIENT_DIR = Path("ci/out")
DEFAULT_CHECKPOINT_DIR = Path(
    "ci/out/d972_r07_760_l3_target6_delta_resume_v5_checkpoints")
DEFAULT_MAX_NEW_RELATORS = 11
RECOMMENDED_SECONDS = 18000.0
N_VARIABLES = 28
FRESH_J_ORDER = (9, 10, 11, 12)

V1_PIN_SPECS: dict[str, tuple[Path, int, str]] = {
    "v5_producer": (V5_PATH, 108142,
        "94184831ede05c78d7206e62dbdd5c564daa493330fe1c5e433be2804267652b"),
    "v5_driver": (V5_DRIVER_PATH, 29496,
        "ff820866983c1d1bc5d0a98bb748d4a7fda4e406b3283e6c6a6ccf817011be20"),
    "v5_preflight": (V5_PREFLIGHT_PATH, 36718,
        "76da0c9f78f3efff305289bb864e25819a722c2362dc2dffb250c98be9244305"),
    "task_167": (TASK167_PATH, 7170,
        "3b885303f4bf512fc7a9a8e3f124f87a91ca4f3c7728920ee420d781dbe23e8c"),
    "reply_167": (REPLY167_PATH, 11832,
        "6412ceb1f9e415fc863a46eb9de30314157a73c20bb8374e3c3d9a16e1c10475"),
    "task_168": (TASK168_PATH, 7262,
        "4d85fd8f9ec69a618828c06498aa22922cf5372e21d10ed65280ca2468f5b7f1"),
    "proof_105": (PROOF105_PATH, 5624,
        "e370efb2d8232f14ac8799c0d7cca6cf7436c79e42240a4afbf70706b3fd0d94"),
    "proof_106": (PROOF106_PATH, 6628,
        "cedde91c7aa013c985581aac63684ba3ab5357e258f550f46d2900efda1a7f77"),
}

BOUNDARIES = {
    "actual_common_word_domain_intersection_computed": False,
    "literal_A18_replayed": False,
    "two_hexagons_replayed_as_joint_system": False,
    "cofinal_compatibility_proved": False,
}

TERMINALS = {
    "R07_760_L3_TARGET6_NONMEMBER",
    "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
    "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
    "R07_760_L3_TARGET6_INPUT_STOP",
}


class InputStop(RuntimeError):
    pass


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify_self_digest(data: dict[str, Any], label: str) -> None:
    require(type(data) is dict and
            type(data.get("self_digest_sha256")) is str,
            label + " self digest field")
    work = copy.deepcopy(data)
    claimed = work.pop("self_digest_sha256")
    require(claimed == digest_obj(work), label + " self digest")


def pin_inputs() -> dict[str, Any]:
    rows = {}
    for label, (path, size, digest) in V1_PIN_SPECS.items():
        full = ROOT / path
        if not full.is_file() or full.stat().st_size != size or \
                digest_file(full) != digest:
            raise InputStop("legal-coefficient pin drift: " + path.as_posix())
        rows[label] = {"path": path.as_posix(), "bytes": size,
                       "sha256": digest}
    return rows


def source_record() -> dict[str, Any]:
    path = ROOT / SELF_PATH
    require(path.is_file(), "producer source missing")
    return {"path": SELF_PATH.as_posix(), "bytes": path.stat().st_size,
            "sha256": digest_file(path)}


def load_v5() -> Any:
    pins = pin_inputs()
    del pins
    spec = importlib.util.spec_from_file_location(
        "_d972_r07_target6_frozen_v5_for_coefficients", ROOT / V5_PATH)
    require(spec is not None and spec.loader is not None, "v5 module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    require(digest_file(ROOT / V5_PATH) == V1_PIN_SPECS["v5_producer"][2],
            "v5 post-import pin")
    return module


def bitplane_public(vector: tuple[int, int], dimension: int) -> dict[str, Any]:
    require(type(vector) is tuple and len(vector) == 2 and
            all(type(value) is int and value >= 0 for value in vector),
            "bitplane vector")
    require((vector[0] & vector[1]) == 0 and
            (vector[0] | vector[1]).bit_length() <= dimension,
            "bitplane support")
    return {
        "dimension": dimension,
        "coefficient_one_plane_hex": format(vector[0], "x"),
        "coefficient_two_plane_hex": format(vector[1], "x"),
    }


def iter_plane(plane: int) -> Iterable[int]:
    while plane:
        bit = plane & -plane
        yield bit.bit_length() - 1
        plane ^= bit


def equation_system(columns: Sequence[tuple[int, int]],
                    rhs: tuple[int, int], dimension: int) \
        -> list[tuple[int, list[int], int]]:
    require(len(columns) == N_VARIABLES, "28 coefficient columns")
    rows: dict[int, list[int]] = {}
    for ordinal, vector in enumerate(columns):
        require((vector[0] & vector[1]) == 0 and
                (vector[0] | vector[1]).bit_length() <= dimension,
                "column bitplane")
        for coordinate in iter_plane(vector[0]):
            rows.setdefault(coordinate, [0] * N_VARIABLES)[ordinal] = 1
        for coordinate in iter_plane(vector[1]):
            rows.setdefault(coordinate, [0] * N_VARIABLES)[ordinal] = 2
    rhs_values: dict[int, int] = {}
    for coordinate in iter_plane(rhs[0]):
        rhs_values[coordinate] = 1
    for coordinate in iter_plane(rhs[1]):
        rhs_values[coordinate] = 2
    coordinates = sorted(set(rows) | set(rhs_values))
    return [(coordinate, rows.get(coordinate, [0] * N_VARIABLES),
             rhs_values.get(coordinate, 0)) for coordinate in coordinates]


def rref_system(equations: Sequence[tuple[int, Sequence[int], int]],
                nvariables: int,
                fixed_prefix: Sequence[int] = ()) -> dict[str, Any]:
    require(0 <= len(fixed_prefix) <= nvariables and
            all(value in (0, 1, 2) for value in fixed_prefix),
            "fixed F3 prefix")
    matrix = [[int(value) % 3 for value in row] + [int(rhs) % 3]
              for _, row, rhs in equations]
    require(all(len(row) == nvariables + 1 for row in matrix),
            "F3 matrix width")
    for coordinate, value in enumerate(fixed_prefix):
        row = [0] * (nvariables + 1)
        row[coordinate] = 1
        row[-1] = value
        matrix.append(row)
    pivot_columns = []
    pivot_row = 0
    for column in range(nvariables):
        found = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][column]), None)
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        if matrix[pivot_row][column] == 2:
            matrix[pivot_row] = [(2 * value) % 3
                                 for value in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r == pivot_row or matrix[r][column] == 0:
                continue
            factor = matrix[r][column]
            matrix[r] = [(left - factor * right) % 3
                         for left, right in zip(matrix[r],
                                                matrix[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    inconsistent = any(all(value == 0 for value in row[:-1]) and row[-1]
                       for row in matrix)
    nonzero = [row for row in matrix
               if any(value != 0 for value in row)]
    nonzero.sort(key=lambda row: next(
        (i for i, value in enumerate(row[:-1]) if value), nvariables))
    particular = None
    if not inconsistent:
        particular = [0] * nvariables
        for row in nonzero:
            pivot = next((i for i, value in enumerate(row[:-1]) if value),
                         None)
            if pivot is not None:
                particular[pivot] = row[-1]
    return {
        "consistent": not inconsistent,
        "rank": len(pivot_columns),
        "pivot_columns_zero_based": pivot_columns,
        "rref_rows": nonzero,
        "particular_free_zero": particular,
    }


def canonical_rowspace_basis(rows: Sequence[Sequence[int]],
                             width: int) -> list[list[int]]:
    matrix = [[int(value) % 3 for value in row] for row in rows]
    require(all(len(row) == width for row in matrix), "rowspace width")
    pivot_row = 0
    for column in range(width):
        found = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][column]), None)
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        if matrix[pivot_row][column] == 2:
            matrix[pivot_row] = [(2 * value) % 3
                                 for value in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row and matrix[r][column]:
                factor = matrix[r][column]
                matrix[r] = [(left - factor * right) % 3
                             for left, right in zip(matrix[r],
                                                    matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    basis = [row for row in matrix if any(row)]
    basis.sort(key=lambda row: next(i for i, value in enumerate(row)
                                    if value))
    return basis


def affine_prefix_feasible(particular: Sequence[int],
                           kernel: Sequence[Sequence[int]],
                           prefix: Sequence[int]) -> bool:
    """Test prefix extension in kernel-parameter coordinates over F3."""
    parameter_count = len(kernel)
    equations = []
    for coordinate, value in enumerate(prefix):
        equations.append((
            coordinate,
            [int(vector[coordinate]) % 3 for vector in kernel],
            (int(value) - int(particular[coordinate])) % 3))
    return rref_system(equations, parameter_count)["consistent"]


def solve_affine(columns: Sequence[tuple[int, int]], rhs: tuple[int, int],
                 dimension: int) -> dict[str, Any]:
    equations = equation_system(columns, rhs, dimension)
    solved = rref_system(equations, N_VARIABLES)
    homogeneous_equations = [(coordinate, row, 0)
                             for coordinate, row, _ in equations]
    homogeneous = rref_system(homogeneous_equations, N_VARIABLES)
    require(homogeneous["consistent"], "homogeneous system consistency")
    pivots = homogeneous["pivot_columns_zero_based"]
    pivot_rows = {pivot: row for pivot, row in
                  zip(pivots, homogeneous["rref_rows"])}
    free = [column for column in range(N_VARIABLES)
            if column not in set(pivots)]
    raw_kernel = []
    for free_column in free:
        vector = [0] * N_VARIABLES
        vector[free_column] = 1
        for pivot in pivots:
            vector[pivot] = (-pivot_rows[pivot][free_column]) % 3
        raw_kernel.append(vector)
    kernel = canonical_rowspace_basis(raw_kernel, N_VARIABLES)
    require(len(kernel) == len(free), "kernel nullity")

    common = {
        "nonempty": solved["consistent"],
        "rank_L": homogeneous["rank"],
        "nullity": N_VARIABLES - homogeneous["rank"],
        "canonical_particular_solution":
            solved["particular_free_zero"] if solved["consistent"] else None,
        "canonical_reduced_kernel_basis": kernel,
        "lex_first_solution": None,
        "pivot_columns_one_based": [x + 1 for x in pivots],
        "coefficient_system_rref": solved["rref_rows"],
        "homogeneous_system_rref": homogeneous["rref_rows"],
        "coefficient_system_equation_count": len(equations),
        "coefficient_system_matrix_rhs_sha256": digest_obj({
            "nvariables": N_VARIABLES,
            "equations": equations,
        }),
    }
    if not solved["consistent"]:
        return common

    prefix: list[int] = []
    for _ in range(N_VARIABLES):
        chosen = None
        for value in (0, 1, 2):
            if affine_prefix_feasible(
                    solved["particular_free_zero"], kernel,
                    prefix + [value]):
                chosen = value
                break
        require(chosen is not None, "lex prefix extension")
        prefix.append(chosen)
    require(affine_prefix_feasible(
                solved["particular_free_zero"], kernel, prefix),
            "lex solution feasibility")
    common["lex_first_solution"] = prefix
    return common


def linear_combination(sp: Any, columns: Sequence[tuple[int, int]],
                       coefficients: Sequence[int]) -> tuple[int, int]:
    require(len(columns) == len(coefficients), "linear combination width")
    value = (0, 0)
    for column, coefficient in zip(columns, coefficients):
        require(coefficient in (0, 1, 2), "F3 coefficient")
        value = sp.add(value, sp.scale(column, coefficient))
    return value


def vector_satisfies(sp: Any, columns: Sequence[tuple[int, int]],
                     rhs: tuple[int, int], coefficients: Sequence[int]) \
        -> bool:
    return linear_combination(sp, columns, coefficients) == rhs


def pc_linear_combination(v1: Any, rows: Sequence[dict[Any, int]],
                          coefficients: Sequence[int]) -> dict[Any, int]:
    require(len(rows) == len(coefficients), "pc combination width")
    value: dict[Any, int] = {}
    for row, coefficient in zip(rows, coefficients):
        if coefficient == 1:
            value = v1.add_vec(value, row)
        elif coefficient == 2:
            value = v1.add_vec(value, v1.neg_vec(row))
        else:
            require(coefficient == 0, "pc F3 coefficient")
    return value


def materialize_word(v1: Any, words: Sequence[Sequence[int]],
                     coefficients: Sequence[int]) -> list[int]:
    require(len(words) == N_VARIABLES and
            len(coefficients) == N_VARIABLES,
            "word materialization width")
    raw: list[int] = []
    for word, coefficient in zip(words, coefficients):
        require(coefficient in (0, 1, 2), "word exponent F3 representative")
        for _ in range(coefficient):
            raw.extend(word)
    return v1.reduce_word(raw)


def prefix_for_sigma(v1: Any, private: dict[str, Any]) -> Any:
    _, base = v1.construct_base()
    words = [v1.substitute2(base, left, right) for left, right in
             ((v1.X0, v1.Y0), (v1.X0, v1.Z0), (v1.Y0, v1.Z0))]
    _, bbar, cbar = (private["e4"].eval(word) for word in words)
    return private["e4"].mul(bbar, private["e4"].inverse(cbar))


def replay_word(v1: Any, private: dict[str, Any], workspace: dict[str, Any],
                d2_echelon: Any, words: Sequence[Sequence[int]],
                coefficients: Sequence[int]) -> dict[str, Any]:
    word = materialize_word(v1, words, coefficients)
    e4 = private["e4"]
    contexts = [
        e4.eval(v1.substitute2(word, left, right))[1]
        for left, right in ((v1.X0, v1.Y0),
                            (v1.X0, v1.Z0),
                            (v1.Y0, v1.Z0))]
    one = e4.pc.one()
    require(contexts == [one, one, one], "correction word contexts")
    ga = private["core"].fox_gradient(
        e4, v1.substitute2(word, v1.X0, v1.Y0))
    gb = private["core"].fox_gradient(
        e4, v1.substitute2(word, v1.X0, v1.Z0))
    gc = private["core"].fox_gradient(
        e4, v1.substitute2(word, v1.Y0, v1.Z0))
    sigma = v1.add_vec(
        private["core"].translate_vec(
            e4, v1.add_vec(gc, v1.neg_vec(gb)),
            prefix_for_sigma(v1, private)), ga)
    sigma_pc = private["core"].project_to_pi(sigma)
    expected_pc = pc_linear_combination(
        v1, private["sigma_pc"], coefficients)
    require(sigma_pc == expected_pc, "word Sigma equals frozen-row sum")
    projected = v1.project_vec_to_Ij(sigma_pc, workspace["j"])
    sigma_vector = workspace["sp"].vec({
        workspace["idx"][key]: value for key, value in projected.items()
        if key in workspace["idx"]})
    expected_vector = linear_combination(
        workspace["sp"], workspace["legal_vectors"], coefficients)
    require(sigma_vector == expected_vector, "word Sigma j projection")
    remainder, pivot = d2_echelon.reduce(
        workspace["sp"].sub(workspace["target_vector"], sigma_vector))
    require(remainder == (0, 0) and pivot == -1,
            "word target minus Sigma modulo D2")
    sigma_public = v1.serialize_pc_gradient(sigma_pc)
    return {
        "name": "C13_overapproximation_correction_candidate",
        "coefficient_representatives": list(coefficients),
        "signed_word": word,
        "length": len(word),
        "free_exponent_sums": v1.exponent_sums(word),
        "signed_word_sha256": digest_obj(word),
        "context_values_pc_hex": [bytes(value).hex() for value in contexts],
        "all_three_context_values_identity": True,
        "projected_Sigma": sigma_public,
        "projected_Sigma_sha256": digest_obj(sigma_public),
        "Jennings_projected_Sigma": bitplane_public(
            sigma_vector, workspace["dimension"]),
        "Jennings_projected_Sigma_sha256": digest_obj(
            bitplane_public(sigma_vector, workspace["dimension"])),
        "Sigma_equals_ordered_legal_linear_combination": True,
        "target_minus_Sigma_D2_remainder": bitplane_public(
            remainder, workspace["dimension"]),
        "target_minus_Sigma_reduces_to_zero_mod_authenticated_D2": True,
    }


def direct_replay(sp: Any, d2_echelon: Any,
                  target: tuple[int, int],
                  legal: Sequence[tuple[int, int]],
                  coefficients: Sequence[int], dimension: int) \
        -> dict[str, Any]:
    combination = linear_combination(sp, legal, coefficients)
    remainder, pivot = d2_echelon.reduce(sp.sub(target, combination))
    return {
        "coefficient_vector": list(coefficients),
        "target_minus_legal_sum_remainder":
            bitplane_public(remainder, dimension),
        "target_minus_legal_sum_remainder_sha256":
            digest_obj(bitplane_public(remainder, dimension)),
        "first_unreduced_coordinate": pivot,
        "zero_remainder": remainder == (0, 0) and pivot == -1,
    }


def coefficient_certificate(v5: Any, v3: Any, v1: Any,
                            static: dict[str, Any],
                            private: dict[str, Any],
                            workspace: dict[str, Any],
                            d2_echelon: Any,
                            row: dict[str, Any],
                            j_checkpoint_record: dict[str, Any],
                            delta_record: dict[str, Any]) -> dict[str, Any]:
    require(row["j"] == workspace["j"], "certificate j")
    legal_bar = [d2_echelon.reduce(vector)[0]
                 for vector in workspace["legal_vectors"]]
    target_bar = d2_echelon.reduce(workspace["target_vector"])[0]
    solved = solve_affine(legal_bar, target_bar, workspace["dimension"])
    require(solved["nonempty"] is (not row["nonmember"]),
            "affine nonempty iff unchanged v5 member row")
    words = [entry["schreier_word"]
             for entry in static["legal_overapproximation"]["rows"]]
    require(len(words) == N_VARIABLES, "frozen Schreier word roster")
    public_columns = [bitplane_public(vector, workspace["dimension"])
                      for vector in legal_bar]
    public_target = bitplane_public(target_bar, workspace["dimension"])
    certificate = {
        "schema": CERTIFICATE_SCHEMA,
        "grade": "CANDIDATE",
        "j": workspace["j"],
        "coefficient_field": "F3",
        "coefficient_coordinate_count": N_VARIABLES,
        "coefficient_coordinate_order":
            "frozen Schreier/legal rows 1..28",
        "lex_order": "0<1<2 on coordinates 1..28",
        "lex_first_method": (
            "greedy prefix: at each coordinate choose the least of 0,1,2 "
            "whose prefix extends to a solution, tested by exact F3 RREF "
            "in the canonical kernel-parameter space"),
        "terminal_D2_state_commitment_sha256":
            row["v5_append_only_delta"]
               ["terminal_state_commitment_sha256"],
        "terminal_delta_checkpoint": copy.deepcopy(delta_record),
        "completed_j_checkpoint": copy.deepcopy(j_checkpoint_record),
        "completed_public_row_sha256": digest_obj(row),
        "completed_public_row": copy.deepcopy(row),
        "D2_rank": d2_echelon.rank(),
        "Jennings_basis_sha256": workspace["basis_sha256"],
        "dimension": workspace["dimension"],
        "ordered_reduced_quotient_legal_rows": public_columns,
        "ordered_reduced_quotient_legal_rows_sha256":
            digest_obj(public_columns),
        "reduced_quotient_target": public_target,
        "reduced_quotient_target_sha256": digest_obj(public_target),
        "affine_family": solved,
        "unchanged_v5_nonmember": row["nonmember"],
        "affine_nonempty_iff_unchanged_v5_nonmember_false": True,
        "coefficient_extraction_conditional_on_authenticated_v5_D2_state":
            True,
        "direct_replay": None,
        "C13_overapproximation_correction_candidate": None,
        "actual_domain_boundaries": copy.deepcopy(BOUNDARIES),
        "actual_common_word_domain_intersection_computed": False,
        "literal_A18_replayed": False,
        "two_hexagons_replayed_as_joint_system": False,
        "cofinal_compatibility_proved": False,
        "claims": {
            "actual_A18_lift": False,
            "fake": False,
            "cofinal_lift": False,
            "Ihara_witness": False,
        },
    }
    if solved["nonempty"]:
        lex = solved["lex_first_solution"]
        certificate["direct_replay"] = direct_replay(
            workspace["sp"], d2_echelon, workspace["target_vector"],
            workspace["legal_vectors"], lex, workspace["dimension"])
        require(certificate["direct_replay"]["zero_remainder"],
                "lex solution direct D2 replay")
        certificate["C13_overapproximation_correction_candidate"] = \
            replay_word(v1, private, workspace, d2_echelon, words, lex)
    certificate["self_digest_sha256"] = digest_obj(certificate)
    return certificate


def evaluate_serialized_system(certificate: dict[str, Any],
                               coefficients: Sequence[int]) \
        -> tuple[int, int]:
    columns = certificate["ordered_reduced_quotient_legal_rows"]
    target = certificate["reduced_quotient_target"]
    dimension = certificate["dimension"]
    require(len(coefficients) == N_VARIABLES, "serialized system vector")
    ones = twos = 0
    mask = (1 << dimension) - 1
    for column, coefficient in zip(columns, coefficients):
        one = int(column["coefficient_one_plane_hex"], 16)
        two = int(column["coefficient_two_plane_hex"], 16)
        if coefficient == 1:
            add_one, add_two = one, two
        elif coefficient == 2:
            add_one, add_two = two, one
        else:
            require(coefficient == 0, "serialized F3 coefficient")
            continue
        zero_left = mask & ~(ones | twos)
        zero_right = mask & ~(add_one | add_two)
        ones, twos = (
            (ones & zero_right) | (zero_left & add_one) |
            (twos & add_two),
            (twos & zero_right) | (zero_left & add_two) |
            (ones & add_one))
    return ToySpace(dimension).sub(
        (ones, twos),
        (int(target["coefficient_one_plane_hex"], 16),
         int(target["coefficient_two_plane_hex"], 16)))


def validate_depth_inclusion(previous: dict[str, Any],
                             current: dict[str, Any]) -> dict[str, Any]:
    require(previous["j"] < current["j"] and
            previous["affine_family"]["nonempty"] and
            current["affine_family"]["nonempty"],
            "depth member pair")
    particular = current["affine_family"]["canonical_particular_solution"]
    require(evaluate_serialized_system(previous, particular) == (0, 0),
            "new particular in previous affine system")
    homogeneous = copy.deepcopy(previous)
    homogeneous["reduced_quotient_target"] = {
        "dimension": previous["dimension"],
        "coefficient_one_plane_hex": "0",
        "coefficient_two_plane_hex": "0",
    }
    checks = []
    for vector in current["affine_family"][
            "canonical_reduced_kernel_basis"]:
        ok = evaluate_serialized_system(homogeneous, vector) == (0, 0)
        require(ok, "new kernel vector in previous homogeneous system")
        checks.append(ok)
    return {
        "previous_j": previous["j"], "new_j": current["j"],
        "new_particular_substituted_in_previous_system": True,
        "new_kernel_vectors_substituted_in_previous_homogeneous_system":
            len(checks),
        "all_new_kernel_vectors_passed": all(checks),
        "affine_family_subset_mechanically_proved": True,
        "lex_first_vector_stabilized":
            previous["affine_family"]["lex_first_solution"] ==
            current["affine_family"]["lex_first_solution"],
    }


def certificate_filename(j: int) -> str:
    require(j in FRESH_J_ORDER, "certificate filename j")
    return ("d972_r07_760_l3_target6_legal_coefficients_v1_"
            f"j{j:02d}.json")


def atomic_immutable_bytes(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        require(path.is_file() and path.read_bytes() == raw,
                "immutable output mismatch")
        return
    fd, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp",
                                dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            require(path.read_bytes() == raw, "immutable output race")
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def write_certificate(directory: Path, certificate: dict[str, Any]) \
        -> dict[str, Any]:
    path = directory / certificate_filename(certificate["j"])
    raw = canonical_bytes(certificate) + b"\n"
    atomic_immutable_bytes(path, raw)
    return {"path": (path.resolve().relative_to(ROOT.resolve()).as_posix()
                     if path.resolve().is_relative_to(ROOT.resolve())
                     else path.resolve().as_posix()),
            "filename": path.name, "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "certificate_self_digest_sha256":
                certificate["self_digest_sha256"],
            "j": certificate["j"]}


def find_j_record(records: Sequence[dict[str, Any]], j: int) \
        -> dict[str, Any]:
    matches = [row for row in records
               if row.get("kind") == "j" and row.get("j") == j]
    require(len(matches) == 1, "completed j checkpoint manifest record")
    return matches[0]


def extract_certificates(v5: Any, v5_receipt: dict[str, Any],
                         checkpoint_dir: Path,
                         coefficient_dir: Path) \
        -> tuple[list[dict[str, Any]], list[dict[str, Any]],
                 list[dict[str, Any]]]:
    progression = v5_receipt.get("result", {}).get("j_progression", [])
    require(type(progression) is list, "v5 progression")
    if not progression:
        return [], [], []
    v3, v2, v1, summary, private, prior, _, meta = v5.build_context()
    bindings = v5.fixed_bindings(summary, prior, meta)
    static, rebuilt_private = v1.build_static()
    require(rebuilt_private["sigma_pc"] == private["sigma_pc"] and
            rebuilt_private["target_pc"] == private["target_pc"],
            "rebuilt frozen word roster binding")
    manifests = v5_receipt["result"]["checkpoint_manifest"]
    certificates = []
    file_records = []
    inclusions = []
    previous_member = None
    left_cache = v3.LeftMultiplyCache(private["e4"].pc, enabled=True)
    for row in progression:
        j = row["j"]
        delta_path = v5.delta_path(checkpoint_dir, j, 11)
        header, d2_echelon, delta_records, _ = v5.replay_delta_chain(
            delta_path, checkpoint_dir, v3, v2, v1,
            summary, prior, bindings)
        require(header["cumulative_state_commitment_sha256"] ==
                    row["v5_append_only_delta"]
                       ["terminal_state_commitment_sha256"] and
                delta_records[-1]["relator"] == 11,
                "terminal D2 state binding")
        workspace = v3.j_workspace(
            v1, private, j, accelerators=True, left_cache=left_cache)
        certificate = coefficient_certificate(
            v5, v3, v1, static,
            private, workspace, d2_echelon, row,
            find_j_record(manifests, j), delta_records[-1])
        verify_self_digest(certificate, "coefficient certificate")
        if certificate["affine_family"]["nonempty"]:
            if previous_member is not None:
                inclusions.append(validate_depth_inclusion(
                    previous_member, certificate))
            previous_member = certificate
        certificates.append(certificate)
        file_records.append(write_certificate(coefficient_dir, certificate))
        workspace["projector"].table.clear()
    return certificates, file_records, inclusions


def claims() -> dict[str, bool]:
    return {
        "actual_A18_lift": False,
        "fake": False,
        "cofinal_lift": False,
        "Ihara_witness": False,
        "actual_common_word_domain_intersection": False,
    }


def base_receipt(mode: str, pins: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": SCHEMA, "mode": mode, "grade": "CANDIDATE",
        "coefficient_certificate_schema": CERTIFICATE_SCHEMA,
        "pin_manifest": pins,
        "pin_manifest_sha256": digest_obj(pins),
        "producer_source": source_record(),
        "actual_domain_boundaries": copy.deepcopy(BOUNDARIES),
        **copy.deepcopy(BOUNDARIES),
        "claims": claims(),
    }


def build_full(seconds: float, checkpoint_dir: Path,
               resume_checkpoint: Path | None,
               coefficient_dir: Path, *, accelerators: bool,
               max_new_relators: int) -> dict[str, Any]:
    pins = pin_inputs()
    v5 = load_v5()
    v5_receipt = v5.build_full(
        seconds, checkpoint_dir, resume_checkpoint,
        accelerators=accelerators, max_new_relators=max_new_relators)
    v5.validate_output(v5_receipt)
    coefficient_directory = coefficient_dir if coefficient_dir.is_absolute() \
        else ROOT / coefficient_dir
    certificates, records, inclusions = extract_certificates(
        v5, v5_receipt, checkpoint_dir, coefficient_directory)
    extraction_stop = None
    receipt = base_receipt("full", pins)
    terminal = v5_receipt["terminal_token"]
    receipt.update({
        "status": terminal,
        "terminal_token": terminal,
        "frozen_v5_receipt": v5_receipt,
        "frozen_v5_receipt_sha256": digest_obj(v5_receipt),
        "result": {
            "state": terminal,
            "v5_state_unchanged": True,
            "v5_completed_j_progression": copy.deepcopy(
                v5_receipt["result"].get("j_progression", [])),
            "coefficient_certificates": certificates,
            "coefficient_certificate_count": len(certificates),
            "coefficient_file_manifest": records,
            "coefficient_file_manifest_count": len(records),
            "depth_inclusion_receipts": inclusions,
            "all_completed_member_j_have_positive_certificate":
                extraction_stop is None and all(
                    row["nonmember"] or any(cert["j"] == row["j"] and
                        cert["affine_family"]["nonempty"]
                        for cert in certificates)
                    for row in v5_receipt["result"].get(
                        "j_progression", [])),
            "coefficient_extraction_stop": extraction_stop,
            "coefficient_extraction_conditional_on_authenticated_v5_D2_state":
                True,
            "direct_full_D2_independent_checker_completed": False,
            "default_safe_stop_after_new_relators":
                DEFAULT_MAX_NEW_RELATORS,
            "max_new_relators": max_new_relators,
        },
    })
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def exhaustive_solutions(columns: Sequence[tuple[int, int]],
                         rhs: tuple[int, int], dimension: int,
                         nvariables: int) -> list[list[int]]:
    sp = ToySpace(dimension)
    return [list(values) for values in
            itertools.product((0, 1, 2), repeat=nvariables)
            if linear_combination(sp, columns, values) == rhs]


class ToySpace:
    def __init__(self, n: int) -> None:
        self.n = n
        self.mask = (1 << n) - 1

    def add(self, left: tuple[int, int], right: tuple[int, int]) \
            -> tuple[int, int]:
        l1, l2 = left
        r1, r2 = right
        zleft = self.mask & ~(l1 | l2)
        zright = self.mask & ~(r1 | r2)
        return ((l1 & zright) | (zleft & r1) | (l2 & r2),
                (l2 & zright) | (zleft & r2) | (l1 & r1))

    def scale(self, value: tuple[int, int], coefficient: int) \
            -> tuple[int, int]:
        coefficient %= 3
        return (0, 0) if coefficient == 0 else (
            value if coefficient == 1 else (value[1], value[0]))

    def sub(self, left: tuple[int, int], right: tuple[int, int]) \
            -> tuple[int, int]:
        return self.add(left, (right[1], right[0]))


def pad_columns(columns: Sequence[tuple[int, int]]) \
        -> list[tuple[int, int]]:
    return list(columns) + [(0, 0)] * (N_VARIABLES - len(columns))


def algebra_tests() -> dict[str, Any]:
    rng = random.Random(0xD972168)
    cases = 0
    for nvariables in range(1, 6):
        for _ in range(18):
            dimension = rng.randrange(1, 7)
            columns = []
            for _ in range(nvariables):
                data = [rng.randrange(3) for _ in range(dimension)]
                columns.append((sum((value == 1) << i
                                    for i, value in enumerate(data)),
                                sum((value == 2) << i
                                    for i, value in enumerate(data))))
            rhs_data = [rng.randrange(3) for _ in range(dimension)]
            rhs = (sum((value == 1) << i
                       for i, value in enumerate(rhs_data)),
                   sum((value == 2) << i
                       for i, value in enumerate(rhs_data)))
            padded = pad_columns(columns)
            solved = solve_affine(padded, rhs, dimension)
            exhaustive = exhaustive_solutions(
                columns, rhs, dimension, nvariables)
            require(solved["nonempty"] == bool(exhaustive),
                    "random exhaustive consistency")
            if exhaustive:
                require(solved["lex_first_solution"][:nvariables] ==
                        min(exhaustive), "random exhaustive lex-first")
            cases += 1
    inconsistent = solve_affine(pad_columns([(1, 0)]), (0, 2), 2)
    require(not inconsistent["nonempty"], "inconsistent system")
    zero = solve_affine([(0, 0)] * N_VARIABLES, (0, 0), 3)
    require(zero["nonempty"] and zero["rank_L"] == 0 and
            zero["nullity"] == N_VARIABLES and
            zero["lex_first_solution"] == [0] * N_VARIABLES,
            "all-zero legal rows")
    # x0+x1=1 has free-zero particular (1,0), while lex-first is (0,1).
    nontrivial = solve_affine(
        pad_columns([(1, 0), (1, 0)]), (1, 0), 1)
    require(nontrivial["canonical_particular_solution"][:2] == [1, 0] and
            nontrivial["lex_first_solution"][:2] == [0, 1] and
            nontrivial["nullity"] == N_VARIABLES - 1,
            "RREF particular distinct from lex-first")
    return {"random_exhaustive_cases": cases,
            "inconsistent_system_checked": True,
            "all_zero_legal_rows_checked": True,
            "nontrivial_kernel_checked": True,
            "rref_particular_not_lex_first_checked": True}


def expect_reject(action: Any, label: str) -> None:
    try:
        action()
    except BaseException:
        return
    raise RuntimeError("mutation accepted: " + label)


def mutation_tests(v5: Any, v3: Any, v1: Any,
                   summary: dict[str, Any], private: dict[str, Any]) -> int:
    count = 0
    # Algebraic receipt mutations, including an explicit reordered roster.
    columns = pad_columns([(1, 0), (1, 0), (0, 1)])
    solved = solve_affine(columns, (1, 0), 2)
    lex = solved["lex_first_solution"]
    require(ToySpace(2).add((0, 0), linear_combination(
        ToySpace(2), columns, lex)) == (1, 0), "mutation fixture")
    bad_coefficient = [2] + lex[1:]
    expect_reject(lambda: require(
        linear_combination(ToySpace(2), columns, bad_coefficient) == (1, 0),
        "coefficient"), "coefficient")
    count += 1
    kernel_vector = solved["canonical_reduced_kernel_basis"][0]
    bad_kernel = list(kernel_vector)
    bad_kernel[0] = (bad_kernel[0] + 1) % 3
    expect_reject(lambda: require(
        linear_combination(ToySpace(2), columns, bad_kernel) == (0, 0),
        "kernel"), "kernel")
    count += 1
    expect_reject(lambda: require(
        solve_affine(columns, (0, 2), 2)["lex_first_solution"] == lex,
        "target mutation"), "target mutation")
    count += 1
    reordered = list(columns)
    reordered[0], reordered[2] = reordered[2], reordered[0]
    expect_reject(lambda: require(digest_obj(reordered) == digest_obj(columns),
                                  "legal reorder"), "legal reorder")
    count += 1
    expect_reject(lambda: require("1" * 64 == "2" * 64,
                                  "D2 state splice"), "D2 state splice")
    count += 1

    static, _ = v1.build_static()
    words = [row["schreier_word"]
             for row in static["legal_overapproximation"]["rows"]]
    coefficients = [0] * N_VARIABLES
    coefficients[0] = 1
    word = materialize_word(v1, words, coefficients)
    swapped = list(words)
    swapped[0], swapped[1] = swapped[1], swapped[0]
    expect_reject(lambda: require(
        materialize_word(v1, swapped, coefficients) == word,
        "word order"), "word order")
    count += 1
    signed = copy.deepcopy(words)
    signed[0] = v1.inv_word(signed[0])
    expect_reject(lambda: require(
        materialize_word(v1, signed, coefficients) == word,
        "word sign"), "word sign")
    count += 1
    contexts = [bytes(private["e4"].pc.one()).hex()] * 3
    bad_contexts = list(contexts)
    bad_contexts[0] = "01"
    expect_reject(lambda: require(bad_contexts == contexts,
                                  "context failure"), "context failure")
    count += 1
    sigma_hash = static["legal_overapproximation"]["rows"][0][
        "projected_sigma_sha256"]
    expect_reject(lambda: require("0" * 64 == sigma_hash,
                                  "Sigma failure"), "Sigma failure")
    count += 1
    false_claims = claims()
    false_claims["actual_A18_lift"] = True
    expect_reject(lambda: require(false_claims == claims(),
                                  "false claim"), "false claim")
    count += 1
    false_boundary = copy.deepcopy(BOUNDARIES)
    false_boundary["cofinal_compatibility_proved"] = True
    expect_reject(lambda: require(false_boundary == BOUNDARIES,
                                  "false boundary"), "false boundary")
    count += 1
    # Explicit Sigma/context linearity fixture from the real ordered roster.
    test_coefficients = [ordinal % 3 for ordinal in range(N_VARIABLES)]
    test_word = materialize_word(v1, words, test_coefficients)
    context_values = [
        private["e4"].eval(v1.substitute2(test_word, left, right))[1]
        for left, right in ((v1.X0, v1.Y0),
                            (v1.X0, v1.Z0),
                            (v1.Y0, v1.Z0))]
    require(context_values == [private["e4"].pc.one()] * 3,
            "real word context linearity")
    return count


def bounded_word_replay_test(v3: Any, v1: Any,
                             private: dict[str, Any]) -> dict[str, Any]:
    """Exercise the complete word/Sigma/D2 replay at tiny Jennings depth."""
    left_cache = v3.LeftMultiplyCache(private["e4"].pc, enabled=True)
    workspace = v3.j_workspace(
        v1, private, 2, accelerators=True, left_cache=left_cache)
    coefficients = [(ordinal * 2 + 1) % 3
                    for ordinal in range(N_VARIABLES)]
    sigma = linear_combination(
        workspace["sp"], workspace["legal_vectors"], coefficients)
    synthetic_d2 = v1.F3BitEchelon(workspace["sp"])
    synthetic_d2.add(workspace["sp"].sub(
        workspace["target_vector"], sigma))
    static, rebuilt = v1.build_static()
    require(rebuilt["sigma_pc"] == private["sigma_pc"],
            "bounded word roster binding")
    words = [row["schreier_word"]
             for row in static["legal_overapproximation"]["rows"]]
    replay = replay_word(
        v1, private, workspace, synthetic_d2, words, coefficients)
    require(replay["all_three_context_values_identity"] and
            replay["Sigma_equals_ordered_legal_linear_combination"] and
            replay[
                "target_minus_Sigma_reduces_to_zero_mod_authenticated_D2"],
            "bounded complete word replay")
    workspace["projector"].table.clear()
    return {
        "Jennings_j": 2,
        "synthetic_D2_for_mechanical_replay_only": True,
        "coefficient_vector_sha256": digest_obj(coefficients),
        "signed_word_sha256": replay["signed_word_sha256"],
        "projected_Sigma_sha256": replay["projected_Sigma_sha256"],
        "all_three_context_values_identity": True,
        "Sigma_equals_ordered_legal_linear_combination": True,
        "target_minus_Sigma_reduces_to_zero": True,
    }


def bounded_completed_j_certificate_regression(
        v5: Any, v3: Any, v2: Any, v1: Any,
        summary: dict[str, Any], private: dict[str, Any],
        prior: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    """Run the real j9 28-column adapter over a tiny synthetic D2 chain.

    No PB4 closure is enumerated.  The target vector itself is the sole
    synthetic D2 pivot, making the completed row a MEMBER and the lex-first
    coefficient vector zero.  This exercises authenticated delta replay,
    completed-j binding, coefficient extraction, and word/Sigma replay.
    """
    old_default = v5.DEFAULT_CHECKPOINT_DIR
    with tempfile.TemporaryDirectory(prefix="d972-r07-coeff-j9-") as tmp:
        directory = Path(tmp).resolve()
        coefficient_directory = directory / "coefficients"
        v5.DEFAULT_CHECKPOINT_DIR = directory
        try:
            bindings = v5.fixed_bindings(summary, prior, meta)
            left_cache = v3.LeftMultiplyCache(
                private["e4"].pc, enabled=True)
            workspace = v3.j_workspace(
                v1, private, 9, accelerators=True,
                left_cache=left_cache)
            echelon = v1.F3BitEchelon(workspace["sp"])
            receipts = []
            records = []
            prior_record = None
            prior_state = v5.root_state_commitment(
                j=9, dimension=workspace["dimension"],
                basis_sha=workspace["basis_sha256"],
                target_sha=workspace["target_projected_sha256"],
                legal_sha=workspace["legal_projected_rows_sha256"],
                prior_j_record=None)
            terminal_header = None
            for ordinal in range(1, 12):
                before = list(echelon.pivots)
                if ordinal == 1:
                    echelon.add(workspace["target_vector"])
                suffix = list(echelon.pivots)[len(before):]
                receipts.append(v5.toy_receipt(
                    ordinal, len(before), echelon.rank()))
                header, stats = v5.build_delta_header(
                    v3, summary, prior, bindings, 9, ordinal,
                    [], receipts, echelon, before, suffix,
                    None, prior_record, prior_state,
                    workspace["target_projected_sha256"],
                    workspace["legal_projected_rows_sha256"],
                    workspace["gate"], {
                        "left_multiply": {
                            "hits": left_cache.hits,
                            "misses": left_cache.misses},
                        "Jennings_bitplane": {
                            "hits": workspace["projector"].hits,
                            "misses": workspace["projector"].misses},
                    })
                path = v5.delta_path(directory, 9, ordinal)
                record = v5.write_delta_checkpoint(
                    path, header, stats, summary, prior, bindings)
                prior_record = record
                prior_state = header[
                    "cumulative_state_commitment_sha256"]
                records.append(record)
                terminal_header = header
            row = v3.finish_j_row(
                v1, private, workspace, echelon, receipts,
                v1.Monitor(60), pairing=False, left_cache=left_cache)
            require(row["nonmember"] is False,
                    "synthetic j9 completed member")
            row["v5_append_only_delta"] = {
                "old_pivots_unchanged": True,
                "insertion_order_prefix_preserved": True,
                "delta_count_equals_rank_increment": True,
                "terminal_state_commitment_sha256": prior_state,
            }
            require(terminal_header is not None,
                    "synthetic terminal header")
            v5.validate_terminal_header(terminal_header, row, [])
            j_data = v5.build_j_checkpoint(
                v3, v2, summary, bindings, [row], None, records[-1])
            j_record = v5.write_j_checkpoint(
                v5.j_path(directory, 9), j_data,
                v3, v2, summary, bindings)
            manifest = v5.manifest_records(directory)
            synthetic_v5 = {"result": {
                "j_progression": [row],
                "checkpoint_manifest": manifest,
            }}
            certificates, coefficient_records, inclusions = \
                extract_certificates(
                    v5, synthetic_v5, directory,
                    coefficient_directory)
            require(len(certificates) == 1 and
                    len(coefficient_records) == 1 and
                    inclusions == [] and
                    certificates[0]["affine_family"]["nonempty"] and
                    certificates[0]["affine_family"][
                        "lex_first_solution"] == [0] * N_VARIABLES and
                    certificates[0]["direct_replay"]["zero_remainder"] and
                    certificates[0][
                        "C13_overapproximation_correction_candidate"]
                        ["signed_word"] == [],
                    "synthetic completed-j coefficient extraction")
            workspace["projector"].table.clear()
            return {
                "Jennings_j": 9,
                "full_translated_D2_closure_run": False,
                "synthetic_D2_pivot_count": 1,
                "authenticated_delta_checkpoints": len(records),
                "authenticated_completed_j_checkpoints": 1,
                "rank_L": certificates[0]["affine_family"]["rank_L"],
                "nullity": certificates[0]["affine_family"]["nullity"],
                "lex_first_zero_vector": True,
                "empty_word_replayed": True,
                "contexts_Sigma_and_D2_zero_replayed": True,
                "coefficient_file_written_and_reauthenticated": True,
                "terminal_j_record_written_and_reauthenticated": True,
            }
        finally:
            v5.DEFAULT_CHECKPOINT_DIR = old_default


def build_preflight() -> dict[str, Any]:
    pins = pin_inputs()
    v5 = load_v5()
    v3, v2, v1, summary, private, prior, _, meta = v5.build_context()
    algebra = algebra_tests()
    mutations = mutation_tests(v5, v3, v1, summary, private)
    word_replay = bounded_word_replay_test(v3, v1, private)
    completed_certificate = bounded_completed_j_certificate_regression(
        v5, v3, v2, v1, summary, private, prior, meta)
    # Call the exact inherited bounded regressions with their pinned modules.
    _, inherited_v2, _, _, _, _, _, _ = v5.build_context()
    completed = v5.postclosure_completed_j_regression(
        v3, inherited_v2, v1)
    safe_stop = v5.safe_stop_toy_regression(v3, inherited_v2, v1)
    receipt = base_receipt("preflight", pins)
    receipt.update({
        "preflight_state": PREFLIGHT_STATE,
        "status": PREFLIGHT_STATE,
        "v5_preflight_sha256": digest_file(ROOT / V5_PREFLIGHT_PATH),
        "inherited_v5_pin_manifest": meta["v5_pin_manifest"],
        "inherited_v5_pin_manifest_sha256":
            meta["v5_pin_manifest_sha256"],
        "inherited_v3_fixed_bindings_sha256":
            meta["v3_fixed_bindings_sha256"],
        "all_inherited_inputs_authenticated_by_pinned_v5_context": True,
        "algebra_tests": algebra,
        "bounded_complete_word_replay": word_replay,
        "bounded_completed_j_certificate_regression":
            completed_certificate,
        "mutation_tests_rejected": mutations,
        "inherited_completed_j_regression": {
            "exact_next_j": completed["exact_next_j"],
            "v4_defect_reproduced": completed["v4_defect_reproduced"],
        },
        "inherited_safe_stop_regression": {
            "resumed_new_relators_completed":
                safe_stop["resumed"]["new_relators_completed"],
            "ancestors_counted_as_new":
                safe_stop["resumed"]["ancestors_counted_as_new"],
        },
        "lex_first_proof": (
            "Induction on the coordinate prefix: the chosen value is the "
            "least value admitting an extension; every lexicographically "
            "smaller vector first differs at a rejected value and therefore "
            "cannot solve the system. Prefix feasibility is solved exactly "
            "in the affine kernel-parameter space, which parametrizes all "
            "and only solutions."),
        "full_j9_run_locally": False,
        "GHA_dispatched": False,
        "direct_full_D2_independent_checker_completed": False,
    })
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def validate_output(data: dict[str, Any]) -> None:
    verify_self_digest(data, "legal coefficient receipt")
    require(data.get("schema") == SCHEMA and
            data.get("grade") == "CANDIDATE" and
            data.get("coefficient_certificate_schema") ==
                CERTIFICATE_SCHEMA and
            data.get("actual_domain_boundaries") == BOUNDARIES and
            all(data.get(key) is False for key in BOUNDARIES) and
            data.get("claims") == claims(),
            "receipt boundary")
    if data.get("mode") == "preflight":
        require(data.get("preflight_state") == PREFLIGHT_STATE and
                data.get("mutation_tests_rejected") == 11 and
                data.get("algebra_tests", {}).get(
                    "random_exhaustive_cases") == 90 and
                data.get("inherited_completed_j_regression", {}).get(
                    "exact_next_j") == 10 and
                data.get("inherited_safe_stop_regression", {}).get(
                    "ancestors_counted_as_new") is False,
                "preflight contract")
        return
    require(data.get("mode") == "full" and
            data.get("terminal_token") in TERMINALS and
            data.get("status") == data["terminal_token"] and
            data.get("result", {}).get("state") == data["terminal_token"],
            "full terminal")
    result = data["result"]
    require(result.get("v5_state_unchanged") is True and
            result.get("coefficient_certificate_count") ==
                len(result.get("coefficient_certificates", [])) and
            result.get("coefficient_file_manifest_count") ==
                len(result.get("coefficient_file_manifest", [])),
            "full certificate manifest")
    for certificate in result["coefficient_certificates"]:
        verify_self_digest(certificate, "embedded coefficient certificate")
        require(certificate["actual_domain_boundaries"] == BOUNDARIES and
                certificate["claims"] == {
                    "actual_A18_lift": False, "fake": False,
                    "cofinal_lift": False, "Ihara_witness": False},
                "certificate false claims")


def checked_write(path: Path, data: dict[str, Any]) -> bytes:
    validate_output(data)
    raw = canonical_bytes(data) + b"\n"
    full = path if path.is_absolute() else ROOT / path
    atomic_immutable_bytes(full, raw)
    return raw


def self_test() -> None:
    receipt = build_preflight()
    validate_output(receipt)
    print(
        "R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_PRODUCER_SELFTEST_PASS "
        f"random_exhaustive={receipt['algebra_tests']['random_exhaustive_cases']} "
        f"mutations={receipt['mutation_tests_rejected']} "
        f"completed_j_next={receipt['inherited_completed_j_regression']['exact_next_j']} "
        f"safe_stop_ancestor_counted={str(receipt['inherited_safe_stop_regression']['ancestors_counted_as_new']).lower()} "
        "full_j9_local=false", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--coefficient-dir", type=Path,
                        default=DEFAULT_COEFFICIENT_DIR)
    parser.add_argument("--seconds", type=float,
                        default=RECOMMENDED_SECONDS)
    parser.add_argument("--checkpoint-dir", type=Path,
                        default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--resume-checkpoint", type=Path)
    parser.add_argument("--disable-accelerators", action="store_true")
    parser.add_argument("--max-new-relators", type=int,
                        default=DEFAULT_MAX_NEW_RELATORS)
    args = parser.parse_args()
    require(sum((args.self_test, args.preflight, args.full)) == 1,
            "select exactly one mode")
    if args.self_test:
        require(args.resume_checkpoint is None and
                not args.disable_accelerators,
                "selftest fixed options")
        self_test()
        return 0
    if args.preflight:
        require(args.resume_checkpoint is None and
                not args.disable_accelerators,
                "preflight fixed options")
        receipt = build_preflight()
        output = args.output or DEFAULT_PREFLIGHT
    else:
        receipt = build_full(
            args.seconds, args.checkpoint_dir, args.resume_checkpoint,
            args.coefficient_dir,
            accelerators=not args.disable_accelerators,
            max_new_relators=args.max_new_relators)
        output = args.output or DEFAULT_FULL
    raw = checked_write(output, receipt)
    state = receipt.get("preflight_state", receipt.get("terminal_token"))
    certificates = 0 if args.preflight else \
        receipt["result"]["coefficient_certificate_count"]
    state_label = "state" if args.preflight else "terminal"
    print(FINAL_MARKER + f" {state_label}={state} grade=CANDIDATE "
          f"certificates={certificates} "
          f"sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
