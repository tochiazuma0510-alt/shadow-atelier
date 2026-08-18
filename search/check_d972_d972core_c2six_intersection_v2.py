#!/usr/bin/env python3
"""Independent checker for the 157cj fast D972 core intersection certificate.

The checker reconstructs the marked E/V/P arrays and the exact MakeGn(9)
permutation model itself.  It replays all six PB4 rows in E^4, P^4, and
G9^4, all coordinate-law solver witnesses, and every final lossless source
word.  It does not import the GAP producer or assume that the G9^4 projection
is onto.
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
MAP_CHECKER_PATH = ROOT / "search/check_d972_b4_marity_reduction_maps_v1.py"
MAP_CHECKER_SHA = "eb87e9d42ecde979b82a31beec8fdedea3e221a55d4881f8a71dbaffc2a7a032"
GN_SOURCE_PATH = ROOT / "search/week3-battery-common.g"
GN_SOURCE_SHA = "aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998"
DOVETAIL_SOURCE_PATH = ROOT / "search/d972_dovetail_core_v2.g"
DOVETAIL_SOURCE_SHA = "1c3348003805df874ab6d42503720259564eec25c1aebfb1c548a759e3d9f7ae"
PRODUCER_PATH = ROOT / "search/d972_d972core_c2six_intersection_v2.g"
PRODUCER_SHA = "57b340ad02d2864355ed5e2bd4c6ee4500a4509dafd5152e71c84b513b2738ad"
DEGREE_E = 72
DEGREE_P = 9
DEGREE_G9 = 27
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


def word_value(word: list[int], generators: tuple[Perm, ...]) -> Perm:
    result = one(len(generators[0]))
    for letter in word:
        generator = generators[letter - 1] if letter > 0 else inverse(generators[-letter - 1])
        result = compose(result, generator)
    return result


def embed_blocks(values: Iterable[Perm]) -> Perm:
    values = tuple(values)
    images: list[int] = []
    offset = 0
    for value in values:
        images.extend(offset + image for image in value)
        offset += len(value)
    return tuple(images)


def block_values(large: Perm, degree: int) -> tuple[Perm, ...]:
    return tuple(
        tuple(large[index] - offset for index in range(offset, offset + degree))
        for offset in range(0, len(large), degree)
    )


def paper_product(values: Iterable[Perm]) -> Perm:
    values = tuple(values)
    result = one(len(values[0]))
    for value in reversed(values):
        result = compose(result, value)
    return result


def hom_table(
    group_size: int, domain_gens: tuple[Perm, Perm], image_gens: tuple[Perm, Perm]
) -> tuple[bool, dict[Perm, Perm]]:
    domain_one = one(len(domain_gens[0]))
    image_one = one(len(image_gens[0]))
    mapping = {domain_one: image_one}
    steps = (
        (domain_gens[0], image_gens[0]),
        (inverse(domain_gens[0]), inverse(image_gens[0])),
        (domain_gens[1], image_gens[1]),
        (inverse(domain_gens[1]), inverse(image_gens[1])),
    )
    queue = deque([domain_one])
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


def quotient_data(group: set[Perm], kernel: set[Perm]):
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

def q_inverse(value: int, identity: int, operation, size: int) -> int:
    for candidate in range(size):
        if operation(value, candidate) == identity:
            return candidate
    raise AssertionError("quotient inverse missing")
def q_to_p(
    size: int,
    identity: int,
    qx: int,
    qy: int,
    operation,
    px: Perm,
    py: Perm,
) -> tuple[bool, dict[int, Perm]]:
    steps = (
        (qx, px),
        (q_inverse(qx, identity, operation, size), inverse(px)),
        (qy, py),
        (q_inverse(qy, identity, operation, size), inverse(py)),
    )
    mapping = {identity: one(DEGREE_P)}
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


def make_dn(n: int) -> tuple[Perm, Perm]:
    r = tuple(list(range(1, n)) + [0])
    s = tuple((n - j) % n for j in range(n))
    if power(r, n) != one(n) or power(s, 2) != one(n):
        raise AssertionError("D_n generator order drift")
    if compose(compose(s, r), inverse(s)) != inverse(r):
        raise AssertionError("D_n relation drift")
    return r, s
def make_gn(n: int) -> tuple[Perm, Perm, set[Perm]]:
    r, s = make_dn(n)

    def tr(p: Perm, block: int) -> Perm:
        values = list(range(3 * n))
        offset = block * n
        for index in range(n):
            values[offset + index] = offset + p[index]
        return tuple(values)

    sr = compose(s, r)
    x = compose(compose(tr(r, 0), tr(s, 1)), tr(s, 2))
    y = compose(compose(tr(sr, 0), tr(r, 1)), tr(sr, 2))
    return x, y, closure((x, y))
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
    if file_sha(MAP_CHECKER_PATH) != MAP_CHECKER_SHA:
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
    if file_sha(GN_SOURCE_PATH) != GN_SOURCE_SHA:
        raise AssertionError("MakeGn source SHA drift")
    if file_sha(DOVETAIL_SOURCE_PATH) != DOVETAIL_SOURCE_SHA:
        raise AssertionError("D972 core source SHA drift")
    return source, source_check, maps


def reconstruct_core(source: dict) -> dict:
    named = {
        name: tuple(source["candidate"]["original_generator_arrays"][name])
        for name in "abcuvwxyz"
    }
    x = tuple(source["candidate"]["selected_arrays"]["X"])
    y = tuple(source["candidate"]["selected_arrays"]["Y"])
    z = inverse(paper_product((x, y)))
    e = closure((x, y))
    v = closure(tuple(named[name] for name in "uvwxyz"))
    if len(e) != 32256 or len(v) != 64:
        raise AssertionError("E/V order drift")
    if not all(conjugate(g, a) in v for g in tuple(v) for a in (x, y, inverse(x), inverse(y))):
        raise AssertionError("V normality drift")
    theta_ok, theta = hom_table(len(e), (x, y), (y, x))
    tau_ok, tau = hom_table(len(e), (x, y), (y, z))
    if not theta_ok or not tau_ok:
        raise AssertionError("B3 normality automorphism drift")

    cosets, which, qop = quotient_data(e, v)
    if len(cosets) != 504:
        raise AssertionError("quotient order drift")
    qone = which[one(DEGREE_E)]
    qx, qy = which[x], which[y]
    _, _, px, py, p = canonical_group()
    iso_ok, iso = q_to_p(len(cosets), qone, qx, qy, qop, px, py)
    if not iso_ok:
        raise AssertionError("E/V marked quotient isomorphism drift")
    pz = inverse(paper_product((px, py)))
    comm_e = comm(x, y)
    normal_e = normal_generated(comm_e, (x, y))
    normal_p = normal_generated(comm(px, py), (px, py))
    if len(normal_e) != 32256 or len(normal_p) != 504:
        raise AssertionError("perfectness normal closure drift")
    gx, gy, g9 = make_gn(9)
    if len(g9) != 2916:
        raise AssertionError("G9 order drift")
    return {
        "named": named, "x": x, "y": y, "z": z, "e": e, "v": v,
        "which": which, "iso": iso, "p": p, "px": px, "py": py, "pz": pz,
        "theta": theta, "tau": tau, "comm_e": comm_e,
        "normal_e": normal_e, "normal_p": normal_p,
        "g9x": gx, "g9y": gy, "g9z": inverse(paper_product((gx, gy))), "g9": g9,
    }
def expected_tuple_values(core: dict, maps: dict, family: str) -> tuple[tuple[Perm, ...], ...]:
    if family == "E":
        target = (core["x"], core["z"], core["y"])
    elif family == "P":
        target = (core["px"], core["pz"], core["py"])
    elif family == "G9":
        target = (core["g9x"], core["g9z"], core["g9y"])
    else:
        raise ValueError(family)
    values = []
    for row in maps["maps"]:
        values.append(tuple(word_value(word, target) for word in row["generator_images"]))
    return tuple(
        tuple(values[map_index][generator_index] for map_index in range(4))
        for generator_index in range(6)
    )


def mask_for(value: Perm, module: tuple[Perm, ...]) -> int:
    for mask in range(64):
        product = one(DEGREE_E)
        for index, basis in enumerate(module):
            if mask & (1 << index):
                product = compose(product, basis)
        if product == value:
            return mask
    raise AssertionError("module basis mask missing")


def action_matrix(value: Perm, module: tuple[Perm, ...]) -> list[int]:
    return [
        mask_for(compose(compose(inverse(value), basis), value), module)
        for basis in module
    ]


def check_perm_array(value: object, degree: int, label: str) -> Perm:
    if not isinstance(value, list) or len(value) != degree:
        raise AssertionError(f"{label} degree drift")
    result = tuple(value)
    if sorted(result) != list(range(degree)):
        raise AssertionError(f"{label} is not a zero-based permutation")
    return result


def check_rows(reported: object, expected: tuple[tuple[Perm, ...], ...], degree: int, label: str) -> None:
    if not isinstance(reported, list) or len(reported) != 6:
        raise AssertionError(f"{label} row count drift")
    for row_index, (row, expected_row) in enumerate(zip(reported, expected), 1):
        if not isinstance(row, list) or len(row) != 4:
            raise AssertionError(f"{label} coordinate count drift")
        for coordinate, (array, expected_perm) in enumerate(zip(row, expected_row), 1):
            if check_perm_array(array, degree, f"{label}[{row_index},{coordinate}]") != expected_perm:
                raise AssertionError(f"{label} table mismatch at {row_index},{coordinate}")
def validate_fast_construction(
    report: dict,
    core: dict,
    expected_e: tuple[tuple[Perm, ...], ...],
    expected_p: tuple[tuple[Perm, ...], ...],
    expected_g9: tuple[tuple[Perm, ...], ...],
) -> None:
    """Replay the bounded coordinate-E law solvers independently."""
    construction = report.get("construction")
    if not isinstance(construction, dict):
        raise AssertionError("fast construction receipt missing")
    if construction.get("method") != (
        "metabelian commutator-of-commutators law plus coordinate E solver"
    ):
        raise AssertionError("fast construction method drift")
    if construction.get("law") != "[[a,b],[c,d]]":
        raise AssertionError("fast law drift")
    if (not isinstance(construction.get("h9_derived_series_length"), int) or
        construction["h9_derived_series_length"] > 3):
        raise AssertionError("metabelian H9 gate drift")
    if construction.get("h9_law_identity_replayed") is not True:
        raise AssertionError("H9 law replay flag drift")
    if (construction.get("coordinate_solver_order") != 32256 or
        construction.get("coordinate_solver_count") != 4 or
        construction.get("solver_generator_count") != 13 or
        construction.get("full_joint_preimage_calls") != 0):
        raise AssertionError("coordinate solver scalar gate drift")
    records = construction.get("fast_records")
    if not isinstance(records, list) or len(records) != 4:
        raise AssertionError("fast coordinate record count drift")
    tuple_e_gens = tuple(embed_blocks(row) for row in expected_e)
    tuple_p_gens = tuple(embed_blocks(row) for row in expected_p)
    tuple_g9_gens = tuple(embed_blocks(row) for row in expected_g9)
    identity_e = one(DEGREE_E)
    identity_p4 = one(4 * DEGREE_P)
    identity_g94 = one(4 * DEGREE_G9)
    for coordinate, record in enumerate(records, 1):
        if not isinstance(record, dict) or record.get("coordinate") != coordinate:
            raise AssertionError(f"fast coordinate record drift at {coordinate}")
        if (record.get("law") != "[[a,b],[c,d]]" or
            record.get("solver_group_order") != 32256 or
            record.get("solver_generator_count") != 13):
            raise AssertionError(f"fast coordinate scalar drift at {coordinate}")
        seed = record.get("seed_source_word")
        operands = record.get("seed_operand_source_words")
        solver_words = record.get("solver_source_words")
        solver_e = record.get("solver_target_E")
        solver_p = record.get("solver_target_P")
        solver_g9 = record.get("solver_target_G9")
        if (not isinstance(seed, list) or not isinstance(operands, list) or
            len(operands) != 4 or not isinstance(solver_words, list) or
            len(solver_words) != 13 or not isinstance(solver_e, list) or
            len(solver_e) != 13 or not isinstance(solver_p, list) or
            len(solver_p) != 13 or not isinstance(solver_g9, list) or
            len(solver_g9) != 13):
            raise AssertionError(f"fast word record shape drift at {coordinate}")
        if seed != solver_words[0]:
            raise AssertionError(f"fast seed/solver binding drift at {coordinate}")
        operand_values_e = [word_value(w, tuple_e_gens) for w in operands]
        operand_values_g9 = [word_value(w, tuple_g9_gens) for w in operands]
        seed_e = comm(comm(operand_values_e[0], operand_values_e[1]),
                      comm(operand_values_e[2], operand_values_e[3]))
        seed_g9 = comm(comm(operand_values_g9[0], operand_values_g9[1]),
                       comm(operand_values_g9[2], operand_values_g9[3]))
        if seed_g9 != identity_g94:
            raise AssertionError(f"fast seed G9 law drift at {coordinate}")
        if (word_value(seed, tuple_e_gens) != seed_e or
            word_value(seed, tuple_g9_gens) != seed_g9):
            raise AssertionError(f"fast seed source replay drift at {coordinate}")
        seed_blocks = block_values(seed_e, DEGREE_E)
        if (any(value != identity_e for index, value in enumerate(seed_blocks)
                if index != coordinate - 1) or
            seed_blocks[coordinate - 1] == identity_e):
            raise AssertionError(f"fast seed E support drift at {coordinate}")
        solver_values: list[Perm] = []
        for index, (word, e_array, p_array, g9_array) in enumerate(
            zip(solver_words, solver_e, solver_p, solver_g9), 1
        ):
            if (not isinstance(word, list) or not word or
                any(not isinstance(letter, int) or letter == 0 or abs(letter) > 6
                    for letter in word)):
                raise AssertionError(f"fast solver word alphabet drift at {coordinate},{index}")
            e_value = word_value(word, tuple_e_gens)
            p_value = word_value(word, tuple_p_gens)
            g9_value = word_value(word, tuple_g9_gens)
            if p_value != identity_p4 or g9_value != identity_g94:
                raise AssertionError(f"fast solver P/G9 drift at {coordinate},{index}")
            blocks = block_values(e_value, DEGREE_E)
            if check_perm_array(e_array, DEGREE_E, "fast solver E") != blocks[coordinate - 1]:
                raise AssertionError(f"fast solver E target drift at {coordinate},{index}")
            if check_perm_array(p_array, 4 * DEGREE_P, "fast solver P") != p_value:
                raise AssertionError(f"fast solver P target drift at {coordinate},{index}")
            if check_perm_array(g9_array, 4 * DEGREE_G9, "fast solver G9") != g9_value:
                raise AssertionError(f"fast solver G9 target drift at {coordinate},{index}")
            if any(value != identity_e for j, value in enumerate(blocks)
                   if j != coordinate - 1):
                raise AssertionError(f"fast solver support drift at {coordinate},{index}")
            solver_values.append(blocks[coordinate - 1])
        if len(closure(solver_values, DEGREE_E)) != 32256:
            raise AssertionError(f"coordinate E solver closure drift at {coordinate}")


def validate_report(report: dict, core: dict, maps: dict) -> None:
    if report.get("schema") != "d972-d972core-c2six-intersection/v2":
        raise AssertionError("schema drift")
    if report.get("final_marker") != "D972_CORE_INTERSECTION_V2_FINAL":
        raise AssertionError("final marker drift")
    if report.get("status") != "CORE_INTERSECTION_V2_COMPUTED":
        raise AssertionError("status drift")
    for key, value in (
        ("source_receipt_sha256", SOURCE_SHA),
        ("source_checker_receipt_sha256", SOURCE_CHECK_SHA),
        ("four_map_receipt_sha256", MAPS_SHA),
        ("four_map_checker_sha256", MAP_CHECKER_SHA),
    ):
        if report.get(key) != value:
            raise AssertionError(f"{key} binding drift")
    if file_sha(PRODUCER_PATH) != PRODUCER_SHA:
        raise AssertionError("producer SHA drift")
    if report.get("generator_labels") != list(LABELS):
        raise AssertionError("generator labels drift")
    if report.get("tuple_labels") != [list(row) for row in EXPECTED_LABEL_ROWS]:
        raise AssertionError("tuple labels drift")
    if report.get("four_map_replay") != {
        "generator_count": 6,
        "map_count": 4,
        "target_order": ["X", "Z", "Y"],
        "all_six_rows_replayed": True,
    }:
        raise AssertionError("four-map replay receipt drift")

    g9c = report.get("g9_constructor")
    if not isinstance(g9c, dict):
        raise AssertionError("G9 constructor receipt missing")
    gx, gy, g9 = core["g9x"], core["g9y"], core["g9"]
    gz = core["g9z"]
    if g9c.get("source_path") != GN_SOURCE_PATH.relative_to(ROOT).as_posix():
        raise AssertionError("G9 source path drift")
    if g9c.get("source_sha256") != GN_SOURCE_SHA or g9c.get("dovetail_core_sha256") != DOVETAIL_SOURCE_SHA:
        raise AssertionError("G9 source binding drift")
    if g9c.get("degree") != DEGREE_G9 or g9c.get("order") != 2916:
        raise AssertionError("G9 degree/order drift")
    if g9c.get("x_array") != list(gx) or g9c.get("y_array") != list(gy) or g9c.get("z_array") != list(gz):
        raise AssertionError("G9 generator arrays drift")
    if g9c.get("solvable") is not True:
        raise AssertionError("G9 solvability receipt drift")
    if not isinstance(g9c.get("derived_series_orders"), list) or len(g9c["derived_series_orders"]) > 3:
        raise AssertionError("G9 derived-series receipt drift")

    expected_e = expected_tuple_values(core, maps, "E")
    expected_p = expected_tuple_values(core, maps, "P")
    expected_g9 = expected_tuple_values(core, maps, "G9")
    check_rows(report.get("tuple_images_E"), expected_e, DEGREE_E, "E tuple")
    check_rows(report.get("tuple_images_P"), expected_p, DEGREE_P, "P tuple")
    check_rows(report.get("tuple_images_G9"), expected_g9, DEGREE_G9, "G9 tuple")
    validate_fast_construction(report, core, expected_e, expected_p, expected_g9)

    projection = report.get("projection_certificate")
    if not isinstance(projection, dict):
        raise AssertionError("projection certificate missing")
    if projection.get("E_factor_orders") != [32256] * 4:
        raise AssertionError("E factor orders drift")
    if projection.get("P_factor_orders") != [504] * 4:
        raise AssertionError("P factor orders drift")
    if projection.get("G9_factor_orders") != [2916] * 4:
        raise AssertionError("G9 factor orders drift")
    if projection.get("E4_order") != 32256**4 or projection.get("P4_order") != 504**4:
        raise AssertionError("E4/P4 order drift")
    if projection.get("no_G9_fourfold_onto_assumption") is not True:
        raise AssertionError("G9 onto boundary drift")
    if projection.get("E4_is_direct_product") is not True or projection.get("P4_is_direct_product") is not True:
        raise AssertionError("direct-product flags drift")

    tuple_e_gens = tuple(embed_blocks(row) for row in expected_e)
    tuple_p_gens = tuple(embed_blocks(row) for row in expected_p)
    tuple_g9_gens = tuple(embed_blocks(row) for row in expected_g9)
    witnesses = projection.get("pure_coordinate_witness_pairs")
    if witnesses != [[4, 6], [2, 6], [1, 5], [1, 4]]:
        raise AssertionError("pure witness pair drift")
    pure_report = projection.get("pure_coordinate_witnesses_E")
    if not isinstance(pure_report, list) or len(pure_report) != 4:
        raise AssertionError("pure witness count drift")
    for coordinate, pair in enumerate(witnesses, 1):
        actual = comm(tuple_e_gens[pair[0] - 1], tuple_e_gens[pair[1] - 1])
        expected_pure = embed_blocks(
            tuple(core["comm_e"] if index == coordinate - 1 else one(DEGREE_E) for index in range(4))
        )
        if actual != expected_pure or pure_report[coordinate - 1] != list(expected_pure):
            raise AssertionError(f"pure witness replay drift at {coordinate}")
    if projection.get("normal_closure_commutator_E") != 32256:
        raise AssertionError("E perfectness drift")
    if projection.get("normal_closure_commutator_P") != 504:
        raise AssertionError("P commutator closure drift")

    joint = report.get("joint_image")
    if not isinstance(joint, dict):
        raise AssertionError("joint image receipt missing")
    if joint.get("ambient_degree") != 4 * DEGREE_E + 4 * DEGREE_G9:
        raise AssertionError("joint ambient degree drift")
    if joint.get("E4_projection_order") != 32256**4:
        raise AssertionError("joint E projection drift")
    if joint.get("G9_fourfold_image_constructed") is not True:
        raise AssertionError("joint G9 construction flag drift")
    if joint.get("joint_order_computed") is not False or joint.get("goursat_direct_product") is not True:
        raise AssertionError("joint Goursat boundary drift")

    intersection = report.get("intersection")
    if not isinstance(intersection, dict):
        raise AssertionError("intersection receipt missing")
    if intersection.get("image_in_V4") != "V^4" or intersection.get("f2_rank") != 24:
        raise AssertionError("W rank verdict drift")
    if intersection.get("order") != 2**24 or intersection.get("generator_count") != 24:
        raise AssertionError("W order/generator drift")
    if intersection.get("conditional_on_157bb_isolation") is not True:
        raise AssertionError("157bb conditional boundary drift")
    generators = intersection.get("generators")
    if not isinstance(generators, list) or len(generators) != 24:
        raise AssertionError("W generator count drift")

    identity_e = one(DEGREE_E)
    identity_p = one(DEGREE_P)
    identity_g9 = one(DEGREE_G9)
    module = tuple(core["named"][name] for name in "uvwxyz")
    for index, (record, coordinate, basis_index) in enumerate(
        zip(generators, (c for c in range(1, 5) for _ in range(6)), (b for _ in range(4) for b in range(1, 7))),
        1,
    ):
        if not isinstance(record, dict):
            raise AssertionError(f"W generator {index} is not an object")
        if record.get("coordinate") != coordinate or record.get("module_index") != basis_index:
            raise AssertionError(f"W basis ordering drift at {index}")
        word = record.get("source_word")
        if not isinstance(word, list) or not word or any(
            not isinstance(letter, int) or letter == 0 or abs(letter) > 6 for letter in word
        ):
            raise AssertionError(f"W source word alphabet drift at {index}")
        target_e_rows = record.get("target_E")
        target_p_rows = record.get("target_P")
        target_g9_rows = record.get("target_G9")
        if not isinstance(target_e_rows, list) or len(target_e_rows) != 4:
            raise AssertionError(f"W E target row drift at {index}")
        if not isinstance(target_p_rows, list) or len(target_p_rows) != 4:
            raise AssertionError(f"W P target row drift at {index}")
        if not isinstance(target_g9_rows, list) or len(target_g9_rows) != 4:
            raise AssertionError(f"W G9 target row drift at {index}")
        target_e = tuple(check_perm_array(a, DEGREE_E, f"W{index}.E") for a in target_e_rows)
        target_p = tuple(check_perm_array(a, DEGREE_P, f"W{index}.P") for a in target_p_rows)
        target_g9 = tuple(check_perm_array(a, DEGREE_G9, f"W{index}.G9") for a in target_g9_rows)
        expected_e_target = tuple(module[basis_index - 1] if c == coordinate else identity_e for c in range(1, 5))
        if target_e != expected_e_target:
            raise AssertionError(f"W E target basis drift at {index}")
        if target_p != (identity_p,) * 4 or target_g9 != (identity_g9,) * 4:
            raise AssertionError(f"W target does not vanish in P/G9 at {index}")
        if word_value(word, tuple_e_gens) != embed_blocks(target_e):
            raise AssertionError(f"W E word replay drift at {index}")
        if word_value(word, tuple_p_gens) != embed_blocks(target_p):
            raise AssertionError(f"W P word replay drift at {index}")
        if word_value(word, tuple_g9_gens) != embed_blocks(target_g9):
            raise AssertionError(f"W G9 word replay drift at {index}")

    action = report.get("b4_action")
    if not isinstance(action, dict):
        raise AssertionError("B4 action receipt missing")
    if action.get("S4_coordinate_transpositions") != [[2, 1, 3, 4], [1, 3, 2, 4], [1, 2, 4, 3]]:
        raise AssertionError("S4 action drift")
    factors = action.get("composition_factors")
    if factors != [{
        "description": "Induced four-coordinate V-module under P^4 semidirect S4",
        "dimension": 24,
        "irreducible": True,
        "multiplicity": 1,
    }]:
        raise AssertionError("composition-factor drift")
    matrices = action.get("pure_generator_block_matrices")
    if not isinstance(matrices, list) or len(matrices) != 6:
        raise AssertionError("pure action matrix count drift")
    for matrix_rows, tuple_row in zip(matrices, expected_e):
        if not isinstance(matrix_rows, list) or len(matrix_rows) != 4:
            raise AssertionError("pure action matrix coordinate drift")
        for matrix, element in zip(matrix_rows, tuple_row):
            if matrix != action_matrix(element, module):
                raise AssertionError("pure action matrix replay drift")
    if action.get("B3_stabilizer_theta_matrix") != [
        mask_for(core["theta"][basis], module) for basis in module
    ]:
        raise AssertionError("theta matrix drift")
    if action.get("B3_stabilizer_tau_matrix") != [
        mask_for(core["tau"][basis], module) for basis in module
    ]:
        raise AssertionError("tau matrix drift")
    boundary = report.get("input_boundary")
    if boundary.get("cofinal_B4_B_claimed") is not False or boundary.get("Ihara_claimed") is not False:
        raise AssertionError("scope boundary drift")
def static_selftest() -> None:
    source, _, maps = load_inputs()
    core = reconstruct_core(source)
    expected_e = expected_tuple_values(core, maps, "E")
    expected_p = expected_tuple_values(core, maps, "P")
    expected_g9 = expected_tuple_values(core, maps, "G9")
    assert all(len(row) == 4 for row in expected_e)
    assert all(len(row) == 4 for row in expected_p)
    assert all(len(row) == 4 for row in expected_g9)
    tuple_e_gens = tuple(embed_blocks(row) for row in expected_e)
    witnesses = ([4, 6], [2, 6], [1, 5], [1, 4])
    for coordinate, pair in enumerate(witnesses, 1):
        actual = comm(tuple_e_gens[pair[0] - 1], tuple_e_gens[pair[1] - 1])
        expected_pure = embed_blocks(
            tuple(core["comm_e"] if index == coordinate - 1 else one(DEGREE_E) for index in range(4))
        )
        assert actual == expected_pure
        mutated_pure = list(expected_pure)
        mutated_pure[0], mutated_pure[1] = mutated_pure[1], mutated_pure[0]
        assert tuple(mutated_pure) != actual, "pure witness mutation accepted"
    mutated = copy.deepcopy(maps)
    mutated["maps"][0]["generator_images"][0] = ""
    try:
        validate_maps(mutated)
    except AssertionError:
        pass
    else:
        raise AssertionError("map mutation accepted")
    print("D972_CORE_INTERSECTION_V2_CHECKER_SELFTEST_PASS")


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
    print("D972_CORE_INTERSECTION_V2_CHECK_PASS", args.receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
