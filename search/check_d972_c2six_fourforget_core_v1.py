#!/usr/bin/env python3
"""Independent checker for the 157ax four-forget core certificate.

The checker does not import the GAP producer and never enumerates E^4 or P^4.
It reconstructs E, V, and P from the pinned Phase-2b arrays, replays the
four canonical PB4 -> PB3 maps, and validates the pure-coordinate
commutator/normal-closure certificate.  Those witnesses prove the two
subdirect products are direct products, so the reported orders and the
kernel rank follow without trusting a reported large order.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import deque
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "search/certs/d972_phase2b_nonsplit_v1_20260813.json"
SOURCE_SHA = "648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9"
SOURCE_CHECK_PATH = ROOT / "search/certs/d972_phase2b_nonsplit_v1_check_20260813.json"
SOURCE_CHECK_SHA = "90db0fc500eb44bd905059d7a00dfaf4920c8c9890ed151d773141456fd059bb"
MAPS_PATH = ROOT / "search/certs/d972_b4_marity_reduction_maps_v1.json"
MAPS_SHA = "6bab29852ec35210abe7bfc46e68c5457abc76653af3778921a71be8256dbfc2"
MAP_CHECKER_SHA = "eb87e9d42ecde979b82a31beec8fdedea3e221a55d4881f8a71dbaffc2a7a032"
PRODUCER_SHA = "f08142861b5e3d85593f10666275753b82283d214c5711c1d508e8e9d322218c"
DEGREE = 72
LABELS = ("x12", "x13", "x14", "x23", "x24", "x34")
EXPECTED_LABEL_ROWS = (
    ("1", "1", "X", "X"),
    ("1", "X", "1", "Z"),
    ("1", "Z", "Z", "1"),
    ("X", "1", "1", "Y"),
    ("Z", "1", "Y", "1"),
    ("Y", "Y", "1", "1"),
)
EXPECTED_MAPS = [
    {"index": 1, "deleted_strand": 1, "generator_images": [[], [], [], [1], [2], [3]]},
    {"index": 2, "deleted_strand": 2, "generator_images": [[], [1], [2], [], [], [3]]},
    {"index": 3, "deleted_strand": 3, "generator_images": [[1], [], [2], [], [3], []]},
    {"index": 4, "deleted_strand": 4, "generator_images": [[1], [2], [], [3], [], []]},
]
EXPECTED_IDENTITIES = [
    "p4 o c_(sigma3^-1) = p3",
    "p3 o c_(sigma2^-1) = p2",
    "p2 o c_(sigma1^-1) = p1",
]
Perm = tuple[int, ...]


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def object_sha(value: object) -> str:
    return hashlib.sha256(compact(value)).hexdigest()


def one(degree: int) -> Perm:
    return tuple(range(degree))


def compose(left: Perm, right: Perm) -> Perm:
    """GAP-compatible product: apply left, then right."""
    return tuple(right[left[i]] for i in range(len(left)))


def inverse(value: Perm) -> Perm:
    result = [0] * len(value)
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)


def power(value: Perm, exponent: int) -> Perm:
    if exponent < 0:
        return power(inverse(value), -exponent)
    result = one(len(value))
    while exponent:
        if exponent & 1:
            result = compose(result, value)
        value = compose(value, value)
        exponent >>= 1
    return result


def closure(generators: Iterable[Perm], degree: int | None = None) -> set[Perm]:
    gens = tuple(generators)
    if degree is None:
        if not gens:
            raise ValueError("degree required for empty generator list")
        degree = len(gens[0])
    identity = one(degree)
    result = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for generator in gens:
            nxt = compose(current, generator)
            if nxt not in result:
                result.add(nxt)
                queue.append(nxt)
    return result


def comm(left: Perm, right: Perm) -> Perm:
    return compose(compose(compose(inverse(left), inverse(right)), left), right)


def conjugate(value: Perm, by: Perm) -> Perm:
    return compose(compose(inverse(by), value), by)


def normal_generated(seed: Perm, actors: tuple[Perm, ...]) -> set[Perm]:
    basis = [seed]
    while True:
        subgroup = closure(basis)
        extra = None
        for generator in tuple(basis):
            for actor in actors:
                for by in (actor, inverse(actor)):
                    candidate = conjugate(generator, by)
                    if candidate not in subgroup:
                        extra = candidate
                        break
                if extra is not None:
                    break
            if extra is not None:
                break
        if extra is None:
            return subgroup
        basis.append(extra)


def hom_table(
    group_size: int, domain_gens: tuple[Perm, Perm], image_gens: tuple[Perm, Perm]
) -> tuple[bool, dict[Perm, Perm]]:
    domain_one = one(len(domain_gens[0]))
    image_one = one(len(image_gens[0]))
    mapping = {domain_one: image_one}
    queue = deque([domain_one])
    steps = (
        (domain_gens[0], image_gens[0]),
        (inverse(domain_gens[0]), inverse(image_gens[0])),
        (domain_gens[1], image_gens[1]),
        (inverse(domain_gens[1]), inverse(image_gens[1])),
    )
    while queue:
        current = queue.popleft()
        for domain_step, image_step in steps:
            nxt = compose(current, domain_step)
            image = compose(mapping[current], image_step)
            if nxt in mapping:
                if mapping[nxt] != image:
                    return False, mapping
            else:
                mapping[nxt] = image
                queue.append(nxt)
    return len(mapping) == group_size, mapping


def paper_product(values: Iterable[Perm]) -> Perm:
    values = tuple(values)
    result = one(len(values[0]))
    for value in reversed(values):
        result = compose(result, value)
    return result


def word_value(word: list[int], generators: tuple[Perm, ...]) -> Perm:
    result = one(len(generators[0]))
    for letter in word:
        generator = generators[letter - 1] if letter > 0 else inverse(generators[-letter - 1])
        result = compose(result, generator)
    return result


def evaluate_signed_target(word: list[int], target: tuple[Perm, ...]) -> Perm:
    return word_value(word, target)


def embed_blocks(values: Iterable[Perm]) -> Perm:
    values = tuple(values)
    images: list[int] = []
    offset = 0
    for value in values:
        images.extend(offset + image for image in value)
        offset += len(value)
    return tuple(images)


def block_values(large: Perm, degree: int = DEGREE) -> tuple[Perm, ...]:
    return tuple(
        tuple(large[index] - offset for index in range(offset, offset + degree))
        for offset in range(0, len(large), degree)
    )


def quotient_data(
    group: set[Perm], kernel: set[Perm]
) -> tuple[list[tuple[Perm, ...]], dict[Perm, int], callable]:
    pending = set(group)
    cosets: list[tuple[Perm, ...]] = []
    while pending:
        representative = min(pending)
        coset = tuple(sorted(compose(value, representative) for value in kernel))
        cosets.append(coset)
        pending.difference_update(coset)
    cosets.sort()
    which = {value: index for index, coset in enumerate(cosets) for value in coset}
    representatives = [coset[0] for coset in cosets]

    def operation(left: int, right: int) -> int:
        return which[compose(representatives[left], representatives[right])]

    return cosets, which, operation


def q_inverse(value: int, identity: int, operation: callable, size: int) -> int:
    for candidate in range(size):
        if operation(value, candidate) == identity:
            return candidate
    raise AssertionError("quotient inverse missing")


def q_to_p(
    size: int,
    identity: int,
    qx: int,
    qy: int,
    operation: callable,
    px: Perm,
    py: Perm,
) -> tuple[bool, dict[int, Perm]]:
    steps = (
        (qx, px),
        (q_inverse(qx, identity, operation, size), inverse(px)),
        (qy, py),
        (q_inverse(qy, identity, operation, size), inverse(py)),
    )
    mapping = {identity: one(9)}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for qstep, pstep in steps:
            nxt = operation(current, qstep)
            image = compose(mapping[current], pstep)
            if nxt in mapping:
                if mapping[nxt] != image:
                    return False, mapping
            else:
                mapping[nxt] = image
                queue.append(nxt)
    return len(mapping) == size and len(set(mapping.values())) == size, mapping


GF8_MOD = 0b1011
P1_GF8 = tuple([(1, value) for value in range(8)] + [(0, 1)])


def gf8_mul(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left & 8:
            left ^= GF8_MOD
    return result & 7


def gf8_inv(value: int) -> int:
    return next(candidate for candidate in range(1, 8) if gf8_mul(value, candidate) == 1)


def matrix_action(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Perm:
    result = []
    for left, right in P1_GF8:
        a = gf8_mul(left, matrix[0][0]) ^ gf8_mul(right, matrix[1][0])
        b = gf8_mul(left, matrix[0][1]) ^ gf8_mul(right, matrix[1][1])
        line = (1, gf8_mul(b, gf8_inv(a))) if a else (0, 1)
        result.append(P1_GF8.index(line))
    return tuple(result)


def canonical_group() -> tuple[Perm, Perm, Perm, Perm, set[Perm]]:
    s = matrix_action(((1, 0), (1, 1)))
    t = matrix_action(((4, 3), (1, 5)))
    w = compose(s, inverse(t))
    x = power(w, 2)
    y = compose(compose(inverse(s), x), s)
    return s, t, x, y, closure((x, y))


def load_json(path: Path, expected_sha: str) -> dict:
    if file_sha(path) != expected_sha:
        raise AssertionError(f"SHA drift: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"not an object: {path}")
    return value


def validate_maps(maps: dict) -> None:
    if maps.get("schema") != "d972-b4-marity-reduction-maps/v1":
        raise AssertionError("map schema drift")
    if maps.get("status") != "PROVED_BY_CANONICAL_STRAND_FORGETTING":
        raise AssertionError("map status drift")
    if maps.get("maps") != EXPECTED_MAPS:
        raise AssertionError("map rows drift")
    if maps.get("conjugation_identities") != EXPECTED_IDENTITIES:
        raise AssertionError("map identities drift")
    if maps.get("maps_sha256") != object_sha(EXPECTED_MAPS):
        raise AssertionError("map digest drift")
    if file_sha(ROOT / "search/check_d972_b4_marity_reduction_maps_v1.py") != MAP_CHECKER_SHA:
        raise AssertionError("map checker SHA drift")


def load_inputs() -> tuple[dict, dict, dict]:
    source = load_json(SOURCE_PATH, SOURCE_SHA)
    source_check = load_json(SOURCE_CHECK_PATH, SOURCE_CHECK_SHA)
    maps = load_json(MAPS_PATH, MAPS_SHA)
    if source.get("schema") != "d972_phase2b_nonsplit/v1":
        raise AssertionError("source schema drift")
    if source_check.get("schema") != "d972_phase2b_nonsplit_check/v1":
        raise AssertionError("source checker schema drift")
    if source_check.get("all_checks_true") is not True:
        raise AssertionError("pinned source checker is not all true")
    validate_maps(maps)
    return source, source_check, maps


def reconstruct_core(source: dict) -> dict:
    named_arrays = {
        name: tuple(source["candidate"]["original_generator_arrays"][name])
        for name in "abcuvwxyz"
    }
    x = tuple(source["candidate"]["selected_arrays"]["X"])
    y = tuple(source["candidate"]["selected_arrays"]["Y"])
    z = inverse(paper_product((x, y)))
    e = closure((x, y))
    v = closure(tuple(named_arrays[name] for name in "uvwxyz"))
    if len(e) != 32256 or len(v) != 64:
        raise AssertionError("E/V order drift")
    if not all(conjugate(g, a) in v for g in tuple(v) for a in (x, y, inverse(x), inverse(y))):
        raise AssertionError("V is not normal under marked E")
    theta_ok, theta = hom_table(len(e), (x, y), (y, x))
    tau_ok, tau = hom_table(len(e), (x, y), (y, z))
    if not theta_ok or not tau_ok:
        raise AssertionError("B3 normality automorphism did not replay")
    cosets, which, qop = quotient_data(e, v)
    if len(cosets) != 504:
        raise AssertionError("quotient order drift")
    qone = which[one(DEGREE)]
    qx, qy = which[x], which[y]
    ps, pt, px, py, p = canonical_group()
    iso_ok, iso = q_to_p(len(cosets), qone, qx, qy, qop, px, py)
    if not iso_ok:
        raise AssertionError("E/V marked quotient isomorphism did not replay")
    pz = inverse(paper_product((px, py)))
    ptheta_ok, _ = hom_table(len(p), (px, py), (py, px))
    ptau_ok, _ = hom_table(len(p), (px, py), (py, pz))
    if not ptheta_ok or not ptau_ok:
        raise AssertionError("P B3 normality automorphism did not replay")
    comm_e = comm(x, y)
    normal_e = normal_generated(comm_e, (x, y))
    normal_p = normal_generated(comm(px, py), (px, py))
    if len(normal_e) != 32256 or len(normal_p) != 504:
        raise AssertionError("commutator normal-closure certificate drift")
    return {
        "named": named_arrays,
        "x": x,
        "y": y,
        "z": z,
        "e": e,
        "v": v,
        "which": which,
        "qop": qop,
        "qone": qone,
        "iso": iso,
        "p": p,
        "px": px,
        "py": py,
        "pz": pz,
        "theta": theta,
        "tau": tau,
        "comm_e": comm_e,
        "normal_e": normal_e,
        "normal_p": normal_p,
    }


def expected_tuple_values(core: dict, maps: dict) -> tuple[tuple[Perm, ...], ...]:
    target = (core["x"], core["z"], core["y"])
    values: list[tuple[Perm, ...]] = []
    for row in maps["maps"]:
        values.append(
            tuple(
                word_value(word, target)
                for word in row["generator_images"]
            )
        )
    by_generator = tuple(
        tuple(values[map_index][generator_index] for map_index in range(4))
        for generator_index in range(6)
    )
    return by_generator


def mask_for(value: Perm, module: tuple[Perm, ...], e: set[Perm]) -> int:
    for mask in range(64):
        product = one(DEGREE)
        for index, basis in enumerate(module):
            if mask & (1 << index):
                product = compose(product, basis)
        if product == value:
            return mask
    raise AssertionError("module basis mask missing")


def action_matrix(value: Perm, module: tuple[Perm, ...], e: set[Perm]) -> list[int]:
    return [
        mask_for(compose(compose(inverse(value), basis), value), module, e)
        for basis in module
    ]


def validate_report(report: dict, core: dict, maps: dict) -> None:
    if report.get("schema") != "d972-c2six-fourforget-core/v1":
        raise AssertionError("157ax schema drift")
    if report.get("final_marker") != "D972_C2SIX_FOURFORGET_CORE_FINAL":
        raise AssertionError("157ax final marker drift")
    if report.get("status") != "FOURFORGET_CORE_COMPUTED":
        raise AssertionError("157ax status drift")
    if report.get("source_receipt_sha256") != SOURCE_SHA:
        raise AssertionError("source receipt binding drift")
    if report.get("source_checker_receipt_sha256") != SOURCE_CHECK_SHA:
        raise AssertionError("source checker binding drift")
    if report.get("four_map_receipt_sha256") != MAPS_SHA:
        raise AssertionError("map receipt binding drift")
    if report.get("four_map_checker_sha256") != MAP_CHECKER_SHA:
        raise AssertionError("map checker binding drift")
    if file_sha(ROOT / "search/d972_c2six_fourforget_core_v1.g") != PRODUCER_SHA:
        raise AssertionError("producer SHA drift")
    if report.get("generator_labels") != list(LABELS):
        raise AssertionError("generator labels drift")
    if report.get("tuple_labels") != [list(row) for row in EXPECTED_LABEL_ROWS]:
        raise AssertionError("tuple label table drift")
    if report.get("tuple_target_labels") != ["1", "X", "Y", "Z"]:
        raise AssertionError("tuple target labels drift")

    expected = expected_tuple_values(core, maps)
    reported_rows = report.get("tuple_images_E")
    if not isinstance(reported_rows, list) or len(reported_rows) != 6:
        raise AssertionError("tuple image row count drift")
    for row_index, (reported, expected_row) in enumerate(zip(reported_rows, expected), 1):
        if not isinstance(reported, list) or len(reported) != 4:
            raise AssertionError(f"tuple image coordinate count drift {row_index}")
        for coordinate, (array, expected_perm) in enumerate(zip(reported, expected_row), 1):
            if not isinstance(array, list) or len(array) != DEGREE:
                raise AssertionError("tuple image degree drift")
            perm = tuple(array)
            if sorted(perm) != list(range(DEGREE)):
                raise AssertionError("tuple image is not a permutation")
            if perm != expected_perm:
                raise AssertionError(f"tuple table mismatch generator={row_index} coordinate={coordinate}")

    tuple_gens = tuple(embed_blocks(row) for row in expected)
    for coordinate in range(4):
        if closure((row[coordinate] for row in expected), DEGREE) != core["e"]:
            raise AssertionError(f"factor projection is not onto at {coordinate + 1}")
    direct = report.get("direct_product_certificate")
    if not isinstance(direct, dict):
        raise AssertionError("direct-product certificate missing")
    witness_pairs = direct.get("pure_coordinate_witness_pairs")
    if witness_pairs != [[4, 6], [2, 6], [1, 5], [1, 4]]:
        raise AssertionError("pure witness pair table drift")
    pure_report = direct.get("pure_coordinate_witnesses_E")
    if not isinstance(pure_report, list) or len(pure_report) != 4:
        raise AssertionError("pure witness array count drift")
    for coordinate, pair in enumerate(witness_pairs, 1):
        actual = comm(tuple_gens[pair[0] - 1], tuple_gens[pair[1] - 1])
        expected_pure = embed_blocks(
            tuple(core["comm_e"] if index == coordinate - 1 else one(DEGREE) for index in range(4))
        )
        if actual != expected_pure:
            raise AssertionError(f"pure coordinate witness failed at {coordinate}")
        if pure_report[coordinate - 1] != list(expected_pure):
            raise AssertionError(f"pure witness array drift at {coordinate}")
    if direct.get("normal_closure_of_commutator_E") != len(core["normal_e"]):
        raise AssertionError("E normal closure report drift")
    if direct.get("normal_closure_of_commutator_P") != len(core["normal_p"]):
        raise AssertionError("P normal closure report drift")
    if direct.get("normal_closure_of_commutator_E") != 32256:
        raise AssertionError("E normal closure is not E")
    if direct.get("normal_closure_of_commutator_P") != 504:
        raise AssertionError("P normal closure is not P")
    if direct.get("E_order") != 32256**4 or direct.get("P_order") != 504**4:
        raise AssertionError("direct product order drift")
    if direct.get("E_direct_product") is not True or direct.get("P_direct_product") is not True:
        raise AssertionError("direct product flags drift")
    if direct.get("no_large_subgroup_enumeration") is not True:
        raise AssertionError("large enumeration boundary drift")

    pairs = report.get("pair_projection_certificate", {})
    if pairs.get("factor_orders") != [32256] * 4 or pairs.get("factor_orders_P") != [504] * 4:
        raise AssertionError("factor projection order certificate drift")
    for field, order in (("E", 32256**2), ("P", 504**2)):
        rows = pairs.get(field)
        if not isinstance(rows, list) or len(rows) != 6:
            raise AssertionError(f"{field} pair rows drift")
        if any(row.get("order") != order for row in rows):
            raise AssertionError(f"{field} pair order drift")
        if any("no pair enumeration" not in row.get("method", "") for row in rows):
            raise AssertionError(f"{field} pair method drift")

    quotient = report.get("quotient_kernel", {})
    if quotient.get("GE_order") != 32256**4 or quotient.get("GP_order") != 504**4:
        raise AssertionError("quotient order drift")
    if quotient.get("kernel_order") != 64**4 or quotient.get("F2_rank") != 24:
        raise AssertionError("kernel order/rank drift")
    if quotient.get("elementary_abelian") is not True or quotient.get("coordinates") != 4:
        raise AssertionError("kernel structure drift")

    normality = report.get("b3_normality", {})
    if any(normality.get(name) is not True for name in (
        "N_E_B3_normal", "N_P_B3_normal", "theta_E_bijective",
        "tau_E_bijective", "theta_P_bijective", "tau_P_bijective",
    )):
        raise AssertionError("B3 normality receipt drift")
    orbit = report.get("core_orbit", {})
    if orbit.get("B4_mod_PB4") != "S4" or orbit.get("representative_count") != 24:
        raise AssertionError("B4 orbit receipt drift")
    if orbit.get("reduced_to_four_forget_kernels") is not True:
        raise AssertionError("four-forget reduction not certified")

    witness = report.get("kernel_witness", {})
    word = witness.get("source_word")
    if not isinstance(word, list) or not word:
        raise AssertionError("kernel witness word missing")
    if any(not isinstance(letter, int) or letter == 0 or abs(letter) > 6 for letter in word):
        raise AssertionError("kernel witness word alphabet drift")
    target_coordinates = witness.get("target_coordinates")
    if not isinstance(target_coordinates, list) or len(target_coordinates) != 4:
        raise AssertionError("kernel witness coordinate count drift")
    target = embed_blocks(tuple(tuple(row) for row in target_coordinates))
    if target != word_value(word, tuple_gens):
        raise AssertionError("kernel witness word does not replay")
    module_u = core["named"]["u"]
    expected_target = embed_blocks((module_u, one(DEGREE), one(DEGREE), one(DEGREE)))
    if target != expected_target or target == embed_blocks((one(DEGREE),) * 4):
        raise AssertionError("kernel witness target is not the pinned nonzero V element")
    for component in block_values(target):
        if component not in core["v"]:
            raise AssertionError("kernel witness component is not in V")
    p_identity = one(9)
    for component in block_values(target):
        if core["iso"][core["which"][component]] != p_identity:
            raise AssertionError("kernel witness does not vanish in P^4")

    action = report.get("b4_action", {})
    if action.get("S4_coordinate_transpositions") != [[2, 1, 3, 4], [1, 3, 2, 4], [1, 2, 4, 3]]:
        raise AssertionError("S4 coordinate action drift")
    if action.get("action_image_order") != 504**4 * 24:
        raise AssertionError("B4 action image order drift")
    factors = action.get("composition_factors")
    if factors != [{
        "description": "Induced four-coordinate V-module under P^4 semidirect S4",
        "dimension": 24,
        "irreducible": True,
        "multiplicity": 1,
    }]:
        raise AssertionError("composition-factor receipt drift")
    matrices = action.get("pure_generator_block_matrices")
    if not isinstance(matrices, list) or len(matrices) != 6:
        raise AssertionError("pure action matrix generator count drift")
    for generator_index, (matrix_rows, tuple_row) in enumerate(zip(matrices, expected), 1):
        if len(matrix_rows) != 4:
            raise AssertionError("pure action matrix coordinate count drift")
        for matrix, element in zip(matrix_rows, tuple_row):
            module = tuple(core["named"][name] for name in "uvwxyz")
            if matrix != action_matrix(element, module, core["e"]):
                raise AssertionError(f"pure action matrix drift at generator {generator_index}")
    module = tuple(core["named"][name] for name in "uvwxyz")
    if action.get("B3_stabilizer_theta_matrix") != [
        mask_for(core["theta"][basis], module, core["e"]) for basis in module
    ]:
        raise AssertionError("theta action matrix drift")
    if action.get("B3_stabilizer_tau_matrix") != [
        mask_for(core["tau"][basis], module, core["e"]) for basis in module
    ]:
        raise AssertionError("tau action matrix drift")
    boundary = report.get("input_boundary", {})
    if boundary.get("old_raw_158_used") is not False or boundary.get("typed_four_forget_maps") is not True:
        raise AssertionError("scope boundary drift")


def static_selftest() -> None:
    source, _, maps = load_inputs()
    core = reconstruct_core(source)
    expected = expected_tuple_values(core, maps)
    assert tuple(tuple(row) for row in EXPECTED_LABEL_ROWS) == EXPECTED_LABEL_ROWS
    assert all(len(row) == 4 for row in expected)
    tuple_gens = tuple(embed_blocks(row) for row in expected)
    witness_pairs = ([4, 6], [2, 6], [1, 5], [1, 4])
    for coordinate, pair in enumerate(witness_pairs, 1):
        actual = comm(tuple_gens[pair[0] - 1], tuple_gens[pair[1] - 1])
        expected_pure = embed_blocks(
            tuple(core["comm_e"] if index == coordinate - 1 else one(DEGREE) for index in range(4))
        )
        assert actual == expected_pure
        mutated = list(expected_pure)
        mutated[0], mutated[1] = mutated[1], mutated[0]
        assert tuple(mutated) != actual, "pure witness mutation accepted"
    mutated = copy.deepcopy(maps)
    mutated["maps"][0]["generator_images"][0] = ""
    try:
        validate_maps(mutated)
    except AssertionError:
        pass
    else:
        raise AssertionError("map serializer mutation accepted")
    print("D972_C2SIX_FOURFORGET_CORE_CHECKER_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    if args.self_test:
        static_selftest()
        return 0
    if args.receipt is None:
        raise SystemExit("--receipt is required unless --self-test")
    source, _, maps = load_inputs()
    core = reconstruct_core(source)
    report = json.loads(args.receipt.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise AssertionError("report must be an object")
    validate_report(report, core, maps)
    print("D972_C2SIX_FOURFORGET_CORE_CHECK_PASS", args.receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
