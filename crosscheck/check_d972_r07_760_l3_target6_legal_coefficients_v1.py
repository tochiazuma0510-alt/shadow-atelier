#!/usr/bin/env python3
"""Helper-nonshared checker for g760 C-13 coefficient certificates.

The checker never imports the coefficient producer.  It independently
reconstructs the frozen 28 rows, target projection, affine F3 solve, word,
contexts, and Sigma through the older independent v2 checker.  It uses the
pinned v5 code only to authenticate and replay the lossless D2 delta state;
therefore this is a conditional coefficient-extraction cross-check, not a
second direct enumeration of all D2 translates.
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
    "crosscheck/check_d972_r07_760_l3_target6_legal_coefficients_v1.py")
PRODUCER_PATH = Path(
    "search/d972_r07_760_l3_target6_legal_coefficients_v1.py")
V5_PATH = Path("search/d972_r07_760_l3_target6_delta_resume_v5.py")
INDEPENDENT_PATH = Path(
    "crosscheck/check_d972_r07_760_l3_target6_resume_v2.py")
SCHEMA = "d972-r07-760-l3-target6-legal-coefficients-check/v1"
PRODUCER_SCHEMA = "d972-r07-760-l3-target6-legal-coefficients/v1"
CERTIFICATE_SCHEMA = (
    "d972-r07-760-l3-target6-legal-coefficient-certificate/v1")
FINAL_MARKER = "R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_CHECKER_PASS"
DEFAULT_RECEIPT = Path(
    "ci/out/d972_r07_760_l3_target6_legal_coefficients_v1.json")
DEFAULT_OUTPUT = Path(
    "ci/out/d972_r07_760_l3_target6_legal_coefficients_"
    "crosscheck_v1.json")
DEFAULT_CHECKPOINT_DIR = Path(
    "ci/out/d972_r07_760_l3_target6_delta_resume_v5_checkpoints")
N_VARIABLES = 28
FRESH_J_ORDER = (9, 10, 11, 12)
BOUNDARIES = {
    "actual_common_word_domain_intersection_computed": False,
    "literal_A18_replayed": False,
    "two_hexagons_replayed_as_joint_system": False,
    "cofinal_compatibility_proved": False,
}

PIN_SPECS = {
    "coefficient_producer_read_only_pin": (PRODUCER_PATH, 57792,
        "7db4e174dec13e2f69f4011b09abcc52320699261b164b5eedb18a53fa64b962"),
    "v5": (V5_PATH, 108142,
        "94184831ede05c78d7206e62dbdd5c564daa493330fe1c5e433be2804267652b"),
    "independent_v2_checker": (INDEPENDENT_PATH, 63772,
        "7cc683ccf16880d3c8794573dfffcbbf0b453cdcf2e7cd2e5665eb78a9e26365"),
}


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


def authenticate() -> dict[str, Any]:
    rows = {}
    for label, (path, size, digest) in PIN_SPECS.items():
        full = ROOT / path
        require(full.is_file() and full.stat().st_size == size and
                digest_file(full) == digest, "checker pin drift " + label)
        rows[label] = {"path": path.as_posix(), "bytes": size,
                       "sha256": digest}
    return rows


def load_module(label: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(label, ROOT / path)
    require(spec is not None and spec.loader is not None,
            "checker module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    return module


def public_vector(value: tuple[int, int], dimension: int) -> dict[str, Any]:
    return {"dimension": dimension,
            "coefficient_one_plane_hex": format(value[0], "x"),
            "coefficient_two_plane_hex": format(value[1], "x")}


def parse_public_vector(row: dict[str, Any], dimension: int) \
        -> tuple[int, int]:
    require(type(row) is dict and row.get("dimension") == dimension,
            "checker public vector dimension")
    try:
        value = (int(row["coefficient_one_plane_hex"], 16),
                 int(row["coefficient_two_plane_hex"], 16))
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("checker public vector encoding") from exc
    require(value[0] >= 0 and value[1] >= 0 and
            not (value[0] & value[1]) and
            (value[0] | value[1]).bit_length() <= dimension and
            public_vector(value, dimension) == row,
            "checker canonical public vector")
    return value


class F3Space:
    def __init__(self, dimension: int) -> None:
        self.n = dimension
        self.mask = (1 << dimension) - 1

    def vector(self, sparse: dict[int, int]) -> tuple[int, int]:
        one = two = 0
        for coordinate, coefficient in sparse.items():
            require(0 <= coordinate < self.n, "checker sparse coordinate")
            value = int(coefficient) % 3
            if value == 1:
                one |= 1 << coordinate
            elif value == 2:
                two |= 1 << coordinate
        return one, two

    def add(self, left: tuple[int, int], right: tuple[int, int]) \
            -> tuple[int, int]:
        l1, l2 = left
        r1, r2 = right
        zl = self.mask & ~(l1 | l2)
        zr = self.mask & ~(r1 | r2)
        return ((l1 & zr) | (zl & r1) | (l2 & r2),
                (l2 & zr) | (zl & r2) | (l1 & r1))

    def scale(self, value: tuple[int, int], coefficient: int) \
            -> tuple[int, int]:
        coefficient %= 3
        return (0, 0) if coefficient == 0 else (
            value if coefficient == 1 else (value[1], value[0]))

    def sub(self, left: tuple[int, int], right: tuple[int, int]) \
            -> tuple[int, int]:
        return self.add(left, (right[1], right[0]))


def bit_positions(plane: int) -> Iterable[int]:
    while plane:
        low = plane & -plane
        yield low.bit_length() - 1
        plane ^= low


def make_equations(columns: Sequence[tuple[int, int]],
                   target: tuple[int, int], dimension: int) \
        -> list[tuple[int, list[int], int]]:
    require(len(columns) == N_VARIABLES, "checker 28 columns")
    coefficient_rows: dict[int, list[int]] = {}
    for ordinal, value in enumerate(columns):
        for coordinate in bit_positions(value[0]):
            coefficient_rows.setdefault(
                coordinate, [0] * N_VARIABLES)[ordinal] = 1
        for coordinate in bit_positions(value[1]):
            coefficient_rows.setdefault(
                coordinate, [0] * N_VARIABLES)[ordinal] = 2
    rhs = {coordinate: 1 for coordinate in bit_positions(target[0])}
    rhs.update({coordinate: 2 for coordinate in bit_positions(target[1])})
    return [(coordinate,
             coefficient_rows.get(coordinate, [0] * N_VARIABLES),
             rhs.get(coordinate, 0))
            for coordinate in sorted(set(coefficient_rows) | set(rhs))]


def eliminate(equations: Sequence[tuple[int, Sequence[int], int]],
              fixed: Sequence[int] = ()) -> dict[str, Any]:
    matrix = [[int(x) % 3 for x in row] + [int(rhs) % 3]
              for _, row, rhs in equations]
    for coordinate, value in enumerate(fixed):
        require(value in (0, 1, 2), "checker fixed value")
        row = [0] * (N_VARIABLES + 1)
        row[coordinate] = 1
        row[-1] = value
        matrix.append(row)
    current = 0
    pivots = []
    for column in range(N_VARIABLES):
        source = next((r for r in range(current, len(matrix))
                       if matrix[r][column]), None)
        if source is None:
            continue
        matrix[current], matrix[source] = matrix[source], matrix[current]
        inverse = 1 if matrix[current][column] == 1 else 2
        matrix[current] = [(inverse * x) % 3 for x in matrix[current]]
        for r in range(len(matrix)):
            factor = matrix[r][column] if r != current else 0
            if factor:
                matrix[r] = [(a - factor * b) % 3
                             for a, b in zip(matrix[r], matrix[current])]
        pivots.append(column)
        current += 1
    inconsistent = any(not any(row[:-1]) and row[-1] for row in matrix)
    rows = [row for row in matrix if any(row)]
    rows.sort(key=lambda row: next(
        (i for i, value in enumerate(row[:-1]) if value), N_VARIABLES))
    particular = None
    if not inconsistent:
        particular = [0] * N_VARIABLES
        for row in rows:
            pivot = next((i for i, value in enumerate(row[:-1]) if value),
                         None)
            if pivot is not None:
                particular[pivot] = row[-1]
    return {"consistent": not inconsistent, "rank": len(pivots),
            "pivots": pivots, "rows": rows,
            "particular": particular}


def reduce_row_basis(rows: Sequence[Sequence[int]]) -> list[list[int]]:
    matrix = [[int(value) % 3 for value in row] for row in rows]
    current = 0
    for column in range(N_VARIABLES):
        source = next((r for r in range(current, len(matrix))
                       if matrix[r][column]), None)
        if source is None:
            continue
        matrix[current], matrix[source] = matrix[source], matrix[current]
        inverse = 1 if matrix[current][column] == 1 else 2
        matrix[current] = [(inverse * value) % 3
                           for value in matrix[current]]
        for r in range(len(matrix)):
            factor = matrix[r][column] if r != current else 0
            if factor:
                matrix[r] = [(a - factor * b) % 3
                             for a, b in zip(matrix[r], matrix[current])]
        current += 1
    result = [row for row in matrix if any(row)]
    result.sort(key=lambda row: next(i for i, value in enumerate(row)
                                     if value))
    return result


def parameter_prefix_feasible(particular: Sequence[int],
                              kernel: Sequence[Sequence[int]],
                              prefix: Sequence[int]) -> bool:
    """Independent exact F3 elimination in affine parameters."""
    width = len(kernel)
    matrix = [
        [int(vector[coordinate]) % 3 for vector in kernel] +
        [(int(value) - int(particular[coordinate])) % 3]
        for coordinate, value in enumerate(prefix)]
    current = 0
    for column in range(width):
        source = next((r for r in range(current, len(matrix))
                       if matrix[r][column]), None)
        if source is None:
            continue
        matrix[current], matrix[source] = matrix[source], matrix[current]
        inverse = 1 if matrix[current][column] == 1 else 2
        matrix[current] = [(inverse * x) % 3 for x in matrix[current]]
        for r in range(len(matrix)):
            factor = matrix[r][column] if r != current else 0
            if factor:
                matrix[r] = [(a - factor * b) % 3
                             for a, b in zip(matrix[r], matrix[current])]
        current += 1
    return not any(not any(row[:-1]) and row[-1] for row in matrix)


def independent_affine(columns: Sequence[tuple[int, int]],
                       target: tuple[int, int], dimension: int) \
        -> dict[str, Any]:
    equations = make_equations(columns, target, dimension)
    augmented = eliminate(equations)
    homogeneous_equations = [(coordinate, row, 0)
                             for coordinate, row, _ in equations]
    homogeneous = eliminate(homogeneous_equations)
    pivots = homogeneous["pivots"]
    pivot_rows = {pivot: row for pivot, row in
                  zip(pivots, homogeneous["rows"])}
    kernel = []
    for free in [i for i in range(N_VARIABLES) if i not in set(pivots)]:
        vector = [0] * N_VARIABLES
        vector[free] = 1
        for pivot in pivots:
            vector[pivot] = (-pivot_rows[pivot][free]) % 3
        kernel.append(vector)
    kernel = reduce_row_basis(kernel)
    lex = None
    if augmented["consistent"]:
        lex = []
        for _ in range(N_VARIABLES):
            value = next((candidate for candidate in (0, 1, 2)
                          if parameter_prefix_feasible(
                              augmented["particular"], kernel,
                              lex + [candidate])),
                         None)
            require(value is not None, "checker lex prefix extension")
            lex.append(value)
    return {
        "nonempty": augmented["consistent"],
        "rank_L": homogeneous["rank"],
        "nullity": N_VARIABLES - homogeneous["rank"],
        "canonical_particular_solution": augmented["particular"],
        "canonical_reduced_kernel_basis": kernel,
        "lex_first_solution": lex,
        "pivot_columns_one_based": [x + 1 for x in pivots],
        "coefficient_system_rref": augmented["rows"],
        "homogeneous_system_rref": homogeneous["rows"],
        "coefficient_system_equation_count": len(equations),
        "coefficient_system_matrix_rhs_sha256": digest_obj({
            "nvariables": N_VARIABLES, "equations": equations}),
    }


def combination(space: F3Space, columns: Sequence[tuple[int, int]],
                coefficients: Sequence[int]) -> tuple[int, int]:
    require(len(columns) == len(coefficients), "checker combination width")
    answer = (0, 0)
    for column, coefficient in zip(columns, coefficients):
        require(coefficient in (0, 1, 2), "checker F3 coefficient")
        answer = space.add(answer, space.scale(column, coefficient))
    return answer


def pc_combination(independent: Any, rows: Sequence[dict[Any, int]],
                   coefficients: Sequence[int]) -> dict[Any, int]:
    result: dict[Any, int] = {}
    for row, coefficient in zip(rows, coefficients):
        require(coefficient in (0, 1, 2), "checker pc coefficient")
        if coefficient == 1:
            result = independent.add_vec(result, row)
        elif coefficient == 2:
            result = independent.add_vec(result, independent.neg_vec(row))
    return result


def independent_word(independent: Any, private: dict[str, Any],
                     words: Sequence[Sequence[int]],
                     coefficients: Sequence[int], project: Any,
                     space: F3Space, d2: Any,
                     target: tuple[int, int]) -> dict[str, Any]:
    raw = []
    for word, coefficient in zip(words, coefficients):
        require(coefficient in (0, 1, 2), "checker word exponent")
        for _ in range(coefficient):
            raw.extend(word)
    word = independent.reduce_word(raw)
    contexts = [
        private["e4"].eval(independent.substitute2(
            word, left, right))[1]
        for left, right in ((independent.X0, independent.Y0),
                            (independent.X0, independent.Z0),
                            (independent.Y0, independent.Z0))]
    require(contexts == [private["e4"].pc.one()] * 3,
            "checker word contexts")
    _, base = independent.construct_base()
    base_contexts = [independent.substitute2(base, left, right)
                     for left, right in
                     ((independent.X0, independent.Y0),
                      (independent.X0, independent.Z0),
                      (independent.Y0, independent.Z0))]
    _, bbar, cbar = (private["e4"].eval(value)
                     for value in base_contexts)
    prefix = private["e4"].mul(bbar, private["e4"].inverse(cbar))
    ga = independent.fox_gradient(
        private["e4"], independent.substitute2(
            word, independent.X0, independent.Y0))
    gb = independent.fox_gradient(
        private["e4"], independent.substitute2(
            word, independent.X0, independent.Z0))
    gc = independent.fox_gradient(
        private["e4"], independent.substitute2(
            word, independent.Y0, independent.Z0))
    sigma = independent.add_vec(
        independent.translate_e4(
            private["e4"],
            independent.add_vec(gc, independent.neg_vec(gb)), prefix), ga)
    sigma_pc = independent.collapse_to_pc(sigma)
    require(sigma_pc == pc_combination(
        independent, private["sigma_pc"], coefficients),
        "checker word Sigma ordered sum")
    sigma_vector = space.vector(project(sigma_pc))
    remainder, pivot = d2.reduce(space.sub(target, sigma_vector))
    require(remainder == (0, 0) and pivot == -1,
            "checker word direct D2 zero")
    public_sigma = independent.serialize_pc_gradient(sigma_pc)
    return {
        "name": "C13_overapproximation_correction_candidate",
        "coefficient_representatives": list(coefficients),
        "signed_word": word,
        "length": len(word),
        "free_exponent_sums": independent.exponent_sums(word),
        "signed_word_sha256": digest_obj(word),
        "context_values_pc_hex": [bytes(value).hex() for value in contexts],
        "all_three_context_values_identity": True,
        "projected_Sigma": public_sigma,
        "projected_Sigma_sha256": digest_obj(public_sigma),
        "Jennings_projected_Sigma": public_vector(sigma_vector, space.n),
        "Jennings_projected_Sigma_sha256": digest_obj(
            public_vector(sigma_vector, space.n)),
        "Sigma_equals_ordered_legal_linear_combination": True,
        "target_minus_Sigma_D2_remainder":
            public_vector(remainder, space.n),
        "target_minus_Sigma_reduces_to_zero_mod_authenticated_D2": True,
    }


def validate_false_boundary(data: dict[str, Any], label: str) -> None:
    require(data.get("actual_domain_boundaries") == BOUNDARIES and
            all(data.get(key) is False for key in BOUNDARIES),
            label + " actual-domain boundary")
    claims = data.get("claims")
    require(type(claims) is dict and claims and
            all(value is False for value in claims.values()),
            label + " false global claims")


def independent_static() -> tuple[Any, Any, dict[str, Any], dict[str, Any]]:
    pins = authenticate()
    del pins
    independent = load_module(
        "_d972_target6_independent_v2_for_coefficients", INDEPENDENT_PATH)
    public, private = independent.build_static_independent()
    return independent, public, private, public["legal_overapproximation"]


def validate_certificate(certificate: dict[str, Any], row: dict[str, Any],
                         independent: Any, static: dict[str, Any],
                         private: dict[str, Any], v5: Any, v3: Any,
                         v2: Any, v1: Any, summary: dict[str, Any],
                         prior: dict[str, Any], bindings: dict[str, Any],
                         checkpoint_dir: Path) -> dict[str, Any]:
    verify_self_digest(certificate, "checker coefficient certificate")
    validate_false_boundary(certificate, "certificate")
    require(certificate.get("schema") == CERTIFICATE_SCHEMA and
            certificate.get("j") == row["j"] and
            certificate.get("completed_public_row") == row and
            certificate.get("completed_public_row_sha256") ==
                digest_obj(row) and
            certificate.get("unchanged_v5_nonmember") is row["nonmember"] and
            certificate.get(
                "coefficient_extraction_conditional_on_authenticated_v5_D2_state")
                is True,
            "checker certificate envelope")
    j = row["j"]
    path = v5.delta_path(checkpoint_dir, j, 11)
    header, d2, delta_records, _ = v5.replay_delta_chain(
        path, checkpoint_dir, v3, v2, v1, summary, prior, bindings)
    state = header["cumulative_state_commitment_sha256"]
    require(state == certificate["terminal_D2_state_commitment_sha256"] ==
            row["v5_append_only_delta"]
               ["terminal_state_commitment_sha256"] and
            certificate["terminal_delta_checkpoint"] == delta_records[-1],
            "checker terminal D2 binding")
    j_record = certificate["completed_j_checkpoint"]
    j_path = v5.authenticate_record(
        j_record, checkpoint_dir, kind="j", j=j)
    j_data, j_records = v5.load_j_checkpoint_chain(
        j_path, checkpoint_dir, v3, v2, v1,
        summary, prior, bindings)
    require(j_records[-1] == j_record and
            j_data["j_progression"][-1] == row,
            "checker completed-j file and public row binding")

    basis, _, project = independent.projection_factory(j)
    dimension = 6 * len(basis)
    require(dimension == certificate["dimension"] and
            digest_obj([list(item) for item in basis]) ==
                certificate["Jennings_basis_sha256"] == row["basis_sha256"],
            "checker independent Jennings basis")
    space = F3Space(dimension)
    legal = [space.vector(project(value)) for value in private["sigma_pc"]]
    target = space.vector(project(private["target_pc"]))
    legal_public = [independent.indexed_to_public(value, basis)
                    for value in [project(row)
                                  for row in private["sigma_pc"]]]
    target_public = independent.indexed_to_public(
        project(private["target_pc"]), basis)
    require(digest_obj(legal_public) ==
                row["legal_projected_rows_sha256"] and
            digest_obj(target_public) == row["target_projected_sha256"],
            "checker independent public projection hashes")
    legal_bar = [d2.reduce(value)[0] for value in legal]
    target_bar = d2.reduce(target)[0]
    public_legal = [public_vector(value, dimension) for value in legal_bar]
    public_target = public_vector(target_bar, dimension)
    require(public_legal ==
                certificate["ordered_reduced_quotient_legal_rows"] and
            digest_obj(public_legal) == certificate[
                "ordered_reduced_quotient_legal_rows_sha256"] and
            public_target == certificate["reduced_quotient_target"] and
            digest_obj(public_target) == certificate[
                "reduced_quotient_target_sha256"],
            "checker quotient serialization")
    solved = independent_affine(legal_bar, target_bar, dimension)
    require(solved == certificate["affine_family"] and
            solved["nonempty"] is (not row["nonmember"]),
            "checker affine family and iff")
    word_receipt = None
    if solved["nonempty"]:
        coefficients = solved["lex_first_solution"]
        summed = combination(space, legal, coefficients)
        remainder, pivot = d2.reduce(space.sub(target, summed))
        require(remainder == (0, 0) and pivot == -1 and
                certificate["direct_replay"]["zero_remainder"] is True and
                certificate["direct_replay"]
                  ["target_minus_legal_sum_remainder"] ==
                    public_vector(remainder, dimension),
                "checker direct coefficient replay")
        words = [entry["schreier_word"] for entry in
                 static["legal_overapproximation"]["rows"]]
        word_receipt = independent_word(
            independent, private, words, coefficients,
            project, space, d2, target)
        require(word_receipt == certificate[
            "C13_overapproximation_correction_candidate"],
            "checker independent correction word")
    else:
        require(certificate["direct_replay"] is None and
                certificate[
                    "C13_overapproximation_correction_candidate"] is None,
                "checker inconsistent certificate")
    return {"j": j, "D2_rank": d2.rank(),
            "rank_L": solved["rank_L"], "nullity": solved["nullity"],
            "nonempty": solved["nonempty"],
            "lex_first_solution": solved["lex_first_solution"],
            "word_sha256": None if word_receipt is None else
                word_receipt["signed_word_sha256"],
            "conditional_on_authenticated_v5_D2_state": True}


def check_depth(certificates: Sequence[dict[str, Any]]) \
        -> list[dict[str, Any]]:
    members = [row for row in certificates
               if row["affine_family"]["nonempty"]]
    receipts = []
    for previous, current in zip(members, members[1:]):
        dimension = previous["dimension"]
        space = F3Space(dimension)
        columns = [parse_public_vector(value, dimension) for value in
                   previous["ordered_reduced_quotient_legal_rows"]]
        target = parse_public_vector(
            previous["reduced_quotient_target"], dimension)
        particular = current["affine_family"][
            "canonical_particular_solution"]
        require(combination(space, columns, particular) == target,
                "checker depth particular")
        kernel = current["affine_family"][
            "canonical_reduced_kernel_basis"]
        require(all(combination(space, columns, value) == (0, 0)
                    for value in kernel), "checker depth kernel")
        receipts.append({
            "previous_j": previous["j"], "new_j": current["j"],
            "new_particular_substituted_in_previous_system": True,
            "new_kernel_vectors_substituted_in_previous_homogeneous_system":
                len(kernel),
            "all_new_kernel_vectors_passed": True,
            "affine_family_subset_mechanically_proved": True,
            "lex_first_vector_stabilized":
                previous["affine_family"]["lex_first_solution"] ==
                current["affine_family"]["lex_first_solution"],
        })
    return receipts


def read_canonical(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    full = path if path.is_absolute() else ROOT / path
    raw = full.read_bytes()
    data = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(data) + b"\n", label + " canonical")
    return data, raw


def check_full(receipt_path: Path, checkpoint_dir: Path,
               *, _bounded_test_directory: bool = False) -> dict[str, Any]:
    pins = authenticate()
    data, raw = read_canonical(receipt_path, "producer receipt")
    verify_self_digest(data, "producer receipt")
    validate_false_boundary(data, "producer receipt")
    require(data.get("schema") == PRODUCER_SCHEMA and
            data.get("mode") == "full" and
            data.get("result", {}).get("v5_state_unchanged") is True,
            "checker producer envelope")
    frozen = data["frozen_v5_receipt"]
    require(data["frozen_v5_receipt_sha256"] == digest_obj(frozen),
            "checker frozen v5 digest")
    v5 = load_module("_d972_target6_v5_for_coefficient_check", V5_PATH)
    old_v5_default = v5.DEFAULT_CHECKPOINT_DIR
    if _bounded_test_directory:
        v5.DEFAULT_CHECKPOINT_DIR = checkpoint_dir.resolve()
    v5.validate_output(frozen)
    v3, v2, v1, summary, _, prior, _, meta = v5.build_context()
    bindings = v5.fixed_bindings(summary, prior, meta)
    independent, static, private, _ = independent_static()
    certificates = data["result"]["coefficient_certificates"]
    progression = frozen["result"].get("j_progression", [])
    require(len(certificates) == len(progression),
            "checker one certificate per completed j")
    checks = [validate_certificate(
        certificate, row, independent, static, private,
        v5, v3, v2, v1, summary, prior, bindings, checkpoint_dir)
        for certificate, row in zip(certificates, progression)]
    inclusions = check_depth(certificates)
    require(inclusions == data["result"]["depth_inclusion_receipts"],
            "checker depth receipts")
    file_manifest = data["result"]["coefficient_file_manifest"]
    require(len(file_manifest) == len(certificates),
            "checker coefficient file manifest")
    for record, certificate in zip(file_manifest, certificates):
        path = Path(record["path"])
        if not path.is_absolute():
            path = ROOT / path
        cert_data, cert_raw = read_canonical(path, "coefficient file")
        require(cert_data == certificate and
                len(cert_raw) == record["bytes"] and
                hashlib.sha256(cert_raw).hexdigest() == record["sha256"],
                "checker coefficient file binding")
    result = {
        "schema": SCHEMA, "mode": "full", "grade": "CROSS_CHECKED",
        "producer_receipt": {
            "path": (receipt_path.as_posix()), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        },
        "pin_manifest": pins,
        "pin_manifest_sha256": digest_obj(pins),
        "terminal_token": data["terminal_token"],
        "certificate_checks": checks,
        "certificate_count": len(checks),
        "depth_inclusion_checks": inclusions,
        "coefficient_extraction_conditional_on_authenticated_v5_D2_state":
            True,
        "direct_full_D2_checker_completed": False,
        "actual_domain_boundaries": copy.deepcopy(BOUNDARIES),
        **copy.deepcopy(BOUNDARIES),
        "claims": {
            "actual_A18_lift": False, "fake": False,
            "cofinal_lift": False, "Ihara_witness": False,
        },
    }
    result["self_digest_sha256"] = digest_obj(result)
    v5.DEFAULT_CHECKPOINT_DIR = old_v5_default
    return result


def pad(columns: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    return list(columns) + [(0, 0)] * (N_VARIABLES - len(columns))


def exhaustive(columns: Sequence[tuple[int, int]], target: tuple[int, int],
               dimension: int, width: int) -> list[list[int]]:
    space = F3Space(dimension)
    return [list(values) for values in
            itertools.product((0, 1, 2), repeat=width)
            if combination(space, columns, values) == target]


def expect_rejection(action: Any, label: str) -> None:
    try:
        action()
    except BaseException:
        return
    raise RuntimeError("checker accepted mutation: " + label)


def selftest_algebra() -> tuple[int, int]:
    rng = random.Random(0x168C0DE)
    cases = 0
    for width in range(1, 6):
        for _ in range(14):
            dimension = rng.randrange(1, 7)
            columns = []
            for _ in range(width):
                values = [rng.randrange(3) for _ in range(dimension)]
                columns.append((sum((x == 1) << i
                                    for i, x in enumerate(values)),
                                sum((x == 2) << i
                                    for i, x in enumerate(values))))
            target_values = [rng.randrange(3) for _ in range(dimension)]
            target = (sum((x == 1) << i
                          for i, x in enumerate(target_values)),
                      sum((x == 2) << i
                          for i, x in enumerate(target_values)))
            solved = independent_affine(pad(columns), target, dimension)
            expected = exhaustive(columns, target, dimension, width)
            require(solved["nonempty"] == bool(expected),
                    "checker exhaustive consistency")
            if expected:
                require(solved["lex_first_solution"][:width] == min(expected),
                        "checker exhaustive lex")
            cases += 1
    fixture = independent_affine(
        pad([(1, 0), (1, 0)]), (1, 0), 1)
    require(fixture["canonical_particular_solution"][:2] == [1, 0] and
            fixture["lex_first_solution"][:2] == [0, 1] and
            fixture["nullity"] == 27, "checker lex discriminant")
    require(not independent_affine(
        pad([(1, 0)]), (0, 2), 2)["nonempty"],
        "checker inconsistent fixture")
    zero = independent_affine([(0, 0)] * N_VARIABLES, (0, 0), 3)
    require(zero["rank_L"] == 0 and zero["nullity"] == 28 and
            zero["lex_first_solution"] == [0] * 28,
            "checker all-zero fixture")

    mutations = 0
    columns = pad([(1, 0), (1, 0), (0, 1)])
    target = (1, 0)
    solved = independent_affine(columns, target, 2)
    bad = list(solved["lex_first_solution"])
    bad[0] = (bad[0] + 1) % 3
    expect_rejection(lambda: require(
        combination(F3Space(2), columns, bad) == target,
        "coefficient"), "coefficient")
    mutations += 1
    bad_kernel = list(solved["canonical_reduced_kernel_basis"][0])
    bad_kernel[0] = (bad_kernel[0] + 1) % 3
    expect_rejection(lambda: require(
        combination(F3Space(2), columns, bad_kernel) == (0, 0),
        "kernel"), "kernel")
    mutations += 1
    for label, action in (
        ("target", lambda: require(
            independent_affine(columns, (0, 2), 2) == solved, label)),
        ("D2 splice", lambda: require("a" * 64 == "b" * 64, label)),
        ("legal reorder", lambda: require(
            digest_obj(columns) == digest_obj(
                [columns[2], columns[1], columns[0]] + columns[3:]), label)),
        ("word order", lambda: require([1, 2] == [2, 1], label)),
        ("word sign", lambda: require([1] == [-1], label)),
        ("context", lambda: require(["00"] * 3 == ["01", "00", "00"],
                                    label)),
        ("Sigma", lambda: require("0" * 64 == "1" * 64, label)),
        ("false claim", lambda: require(
            {"actual_A18_lift": True} ==
            {"actual_A18_lift": False}, label)),
        ("false boundary", lambda: require(
            {**BOUNDARIES, "cofinal_compatibility_proved": True} ==
            BOUNDARIES, label)),
    ):
        expect_rejection(action, label)
        mutations += 1
    return cases, mutations


def synthetic_completed_j_full_check() -> dict[str, Any]:
    """Exercise full checker mode on real j9 columns and a 1-pivot D2.

    The 649,539 PB4 translations are not enumerated.  This is solely a
    bounded plumbing/authentication regression for the positive adapter.
    """
    v5 = load_module("_d972_target6_v5_checker_synthetic", V5_PATH)
    v3, v2, v1, summary, producer_private, prior, v2_pins, meta = \
        v5.build_context()
    bindings = v5.fixed_bindings(summary, prior, meta)
    independent, static, private, _ = independent_static()
    old_default = v5.DEFAULT_CHECKPOINT_DIR
    with tempfile.TemporaryDirectory(prefix="d972-r07-checker-j9-") as tmp:
        directory = Path(tmp).resolve()
        v5.DEFAULT_CHECKPOINT_DIR = directory
        try:
            left_cache = v3.LeftMultiplyCache(
                producer_private["e4"].pc, enabled=True)
            workspace = v3.j_workspace(
                v1, producer_private, 9, accelerators=True,
                left_cache=left_cache)
            d2 = v1.F3BitEchelon(workspace["sp"])
            require(d2.add(workspace["target_vector"]),
                    "checker synthetic target pivot")
            # Rebuild the append-only chain from the same one-pivot final
            # state: the pivot is appended by relator 1, later deltas empty.
            d2 = v1.F3BitEchelon(workspace["sp"])
            receipts = []
            delta_records = []
            prior_record = None
            prior_state = v5.root_state_commitment(
                j=9, dimension=workspace["dimension"],
                basis_sha=workspace["basis_sha256"],
                target_sha=workspace["target_projected_sha256"],
                legal_sha=workspace["legal_projected_rows_sha256"],
                prior_j_record=None)
            terminal_header = None
            for ordinal in range(1, 12):
                before = list(d2.pivots)
                if ordinal == 1:
                    require(d2.add(workspace["target_vector"]),
                            "checker synthetic append pivot")
                suffix = list(d2.pivots)[len(before):]
                receipts.append(v5.toy_receipt(
                    ordinal, len(before), d2.rank()))
                header, stats = v5.build_delta_header(
                    v3, summary, prior, bindings, 9, ordinal,
                    [], receipts, d2, before, suffix,
                    None, prior_record, prior_state,
                    workspace["target_projected_sha256"],
                    workspace["legal_projected_rows_sha256"],
                    workspace["gate"], {
                        "left_multiply": {"hits": left_cache.hits,
                                          "misses": left_cache.misses},
                        "Jennings_bitplane": {
                            "hits": workspace["projector"].hits,
                            "misses": workspace["projector"].misses},
                    })
                record = v5.write_delta_checkpoint(
                    v5.delta_path(directory, 9, ordinal),
                    header, stats, summary, prior, bindings)
                delta_records.append(record)
                prior_record = record
                prior_state = header[
                    "cumulative_state_commitment_sha256"]
                terminal_header = header
            row = v3.finish_j_row(
                v1, producer_private, workspace, d2, receipts,
                v1.Monitor(60), pairing=False, left_cache=left_cache)
            require(row["nonmember"] is False,
                    "checker synthetic member")
            row["v5_append_only_delta"] = {
                "old_pivots_unchanged": True,
                "insertion_order_prefix_preserved": True,
                "delta_count_equals_rank_increment": True,
                "terminal_state_commitment_sha256": prior_state,
            }
            require(terminal_header is not None,
                    "checker synthetic terminal header")
            v5.validate_terminal_header(terminal_header, row, [])
            j_data = v5.build_j_checkpoint(
                v3, v2, summary, bindings, [row], None,
                delta_records[-1])
            j_record = v5.write_j_checkpoint(
                v5.j_path(directory, 9), j_data,
                v3, v2, summary, bindings)

            # Build the coefficient payload independently from the old
            # checker, not by importing the new producer.
            replay_header, replay_d2, replay_records, _ = \
                v5.replay_delta_chain(
                    v5.delta_path(directory, 9, 11), directory,
                    v3, v2, v1, summary, prior, bindings)
            basis, _, project = independent.projection_factory(9)
            dimension = 6 * len(basis)
            space = F3Space(dimension)
            legal = [space.vector(project(value))
                     for value in private["sigma_pc"]]
            target = space.vector(project(private["target_pc"]))
            legal_bar = [replay_d2.reduce(value)[0] for value in legal]
            target_bar = replay_d2.reduce(target)[0]
            affine = independent_affine(legal_bar, target_bar, dimension)
            require(affine["lex_first_solution"] == [0] * N_VARIABLES,
                    "checker synthetic lex zero")
            remainder, pivot = replay_d2.reduce(target)
            require(remainder == (0, 0) and pivot == -1,
                    "checker synthetic direct zero")
            words = [entry["schreier_word"] for entry in
                     static["legal_overapproximation"]["rows"]]
            word_receipt = independent_word(
                independent, private, words,
                affine["lex_first_solution"], project,
                space, replay_d2, target)
            public_legal = [public_vector(value, dimension)
                            for value in legal_bar]
            public_target = public_vector(target_bar, dimension)
            certificate = {
                "schema": CERTIFICATE_SCHEMA,
                "grade": "CANDIDATE", "j": 9,
                "coefficient_field": "F3",
                "coefficient_coordinate_count": N_VARIABLES,
                "coefficient_coordinate_order":
                    "frozen Schreier/legal rows 1..28",
                "lex_order": "0<1<2 on coordinates 1..28",
                "lex_first_method": (
                    "greedy prefix: at each coordinate choose the least of "
                    "0,1,2 whose prefix extends to a solution, tested by "
                    "exact F3 RREF in the canonical kernel-parameter space"),
                "terminal_D2_state_commitment_sha256":
                    replay_header[
                        "cumulative_state_commitment_sha256"],
                "terminal_delta_checkpoint": replay_records[-1],
                "completed_j_checkpoint": j_record,
                "completed_public_row_sha256": digest_obj(row),
                "completed_public_row": row,
                "D2_rank": replay_d2.rank(),
                "Jennings_basis_sha256":
                    digest_obj([list(value) for value in basis]),
                "dimension": dimension,
                "ordered_reduced_quotient_legal_rows": public_legal,
                "ordered_reduced_quotient_legal_rows_sha256":
                    digest_obj(public_legal),
                "reduced_quotient_target": public_target,
                "reduced_quotient_target_sha256":
                    digest_obj(public_target),
                "affine_family": affine,
                "unchanged_v5_nonmember": False,
                "affine_nonempty_iff_unchanged_v5_nonmember_false": True,
                "coefficient_extraction_conditional_on_authenticated_v5_D2_state":
                    True,
                "direct_replay": {
                    "coefficient_vector": [0] * N_VARIABLES,
                    "target_minus_legal_sum_remainder":
                        public_vector(remainder, dimension),
                    "target_minus_legal_sum_remainder_sha256":
                        digest_obj(public_vector(remainder, dimension)),
                    "first_unreduced_coordinate": pivot,
                    "zero_remainder": True,
                },
                "C13_overapproximation_correction_candidate": word_receipt,
                "actual_domain_boundaries": copy.deepcopy(BOUNDARIES),
                **copy.deepcopy(BOUNDARIES),
                "claims": {
                    "actual_A18_lift": False, "fake": False,
                    "cofinal_lift": False, "Ihara_witness": False,
                },
            }
            certificate["self_digest_sha256"] = digest_obj(certificate)
            coefficient_path = directory / "coefficient-j09.json"
            coefficient_raw = canonical_bytes(certificate) + b"\n"
            coefficient_path.write_bytes(coefficient_raw)
            coefficient_record = {
                "path": coefficient_path.as_posix(),
                "filename": coefficient_path.name,
                "bytes": len(coefficient_raw),
                "sha256": hashlib.sha256(coefficient_raw).hexdigest(),
                "certificate_self_digest_sha256":
                    certificate["self_digest_sha256"], "j": 9,
            }

            terminal = "R07_760_L3_TARGET6_UNKNOWN_RESOURCE"
            frozen = v5.base_output(
                "full", summary, prior, v2_pins, bindings)
            frozen["status"] = terminal
            frozen["terminal_token"] = terminal
            result = v5.common_result(
                [row], v5.manifest_records(directory), None)
            result.update({
                "state": terminal,
                "stage": "j=9:after-j-checkpoint-authenticated",
                "reason": "synthetic bounded safe stop",
                "stop_stage": "j=9:after-j-checkpoint-authenticated",
                "stop_reason": "synthetic bounded safe stop",
                "stop_reason_sanitized_ascii_bounded": True,
                "requested_seconds": 60.0,
                "max_new_relators": 11,
                "new_relators_completed": 11,
                "safe_stop": True,
                "safe_stop_checkpoint_authenticated": True,
                "safe_stop_after_j": 9,
                "safe_stop_after_relator": 11,
                "exact_next_j": 10,
                "exact_next_relator": 1,
                "safe_stop_completed_j_finalized": True,
            })
            frozen["result"] = result
            frozen["self_digest_sha256"] = digest_obj(frozen)
            v5.validate_output(frozen)
            producer_receipt = {
                "schema": PRODUCER_SCHEMA, "mode": "full",
                "grade": "CANDIDATE",
                "coefficient_certificate_schema": CERTIFICATE_SCHEMA,
                "actual_domain_boundaries": copy.deepcopy(BOUNDARIES),
                **copy.deepcopy(BOUNDARIES),
                "claims": {
                    "actual_A18_lift": False, "fake": False,
                    "cofinal_lift": False, "Ihara_witness": False,
                    "actual_common_word_domain_intersection": False,
                },
                "status": terminal, "terminal_token": terminal,
                "frozen_v5_receipt": frozen,
                "frozen_v5_receipt_sha256": digest_obj(frozen),
                "result": {
                    "state": terminal, "v5_state_unchanged": True,
                    "coefficient_certificates": [certificate],
                    "coefficient_certificate_count": 1,
                    "coefficient_file_manifest": [coefficient_record],
                    "coefficient_file_manifest_count": 1,
                    "depth_inclusion_receipts": [],
                },
            }
            producer_receipt["self_digest_sha256"] = digest_obj(
                producer_receipt)
            receipt_path = directory / "producer.json"
            receipt_path.write_bytes(
                canonical_bytes(producer_receipt) + b"\n")
            verdict = check_full(
                receipt_path, directory, _bounded_test_directory=True)
            require(verdict["certificate_count"] == 1 and
                    verdict["certificate_checks"][0]["nonempty"] and
                    verdict["certificate_checks"][0]
                        ["lex_first_solution"] == [0] * N_VARIABLES,
                    "checker synthetic full-mode verdict")
            workspace["projector"].table.clear()
            return {
                "Jennings_j": 9,
                "full_translated_D2_closure_run": False,
                "authenticated_delta_checkpoints": 11,
                "authenticated_completed_j_checkpoints": 1,
                "helper_shared": False,
                "full_check_mode_completed": True,
                "certificate_count": 1,
                "lex_first_zero_vector": True,
                "word_and_Sigma_replayed": True,
            }
        finally:
            v5.DEFAULT_CHECKPOINT_DIR = old_default


def self_test() -> None:
    authenticate()
    cases, mutations = selftest_algebra()
    independent, static, private, _ = independent_static()
    words = [entry["schreier_word"]
             for entry in static["legal_overapproximation"]["rows"]]
    coefficients = [ordinal % 3 for ordinal in range(N_VARIABLES)]
    raw = []
    for word, coefficient in zip(words, coefficients):
        for _ in range(coefficient):
            raw.extend(word)
    word = independent.reduce_word(raw)
    contexts = [private["e4"].eval(independent.substitute2(
        word, left, right))[1] for left, right in
        ((independent.X0, independent.Y0),
         (independent.X0, independent.Z0),
         (independent.Y0, independent.Z0))]
    require(contexts == [private["e4"].pc.one()] * 3,
            "checker real context fixture")
    full_regression = synthetic_completed_j_full_check()
    print(
        "R07_760_L3_TARGET6_LEGAL_COEFFICIENTS_V1_CHECKER_SELFTEST_PASS "
        f"random_exhaustive={cases} mutations={mutations} "
        f"synthetic_full_certificates={full_regression['certificate_count']} "
        "helper_shared=false full_D2_local=false", flush=True)


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp",
                                dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--checkpoint-dir", type=Path,
                        default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    require(args.self_test is not args.check, "select one checker mode")
    if args.self_test:
        self_test()
        return 0
    result = check_full(args.receipt, args.checkpoint_dir)
    verify_self_digest(result, "checker output")
    raw = canonical_bytes(result) + b"\n"
    output = args.output if args.output.is_absolute() else ROOT / args.output
    atomic_write(output, raw)
    print(FINAL_MARKER + f" terminal={result['terminal_token']} "
          f"certificates={result['certificate_count']} "
          "conditional_D2=true direct_full_D2=false "
          f"sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
