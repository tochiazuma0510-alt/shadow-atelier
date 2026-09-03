#!/usr/bin/env python3
"""Independent Task712 checker for canonical grade-two sparse maps.

The checker owns a separate implementation of the marked quotient, the
character transport, prefix reconstruction, sparse table compiler, parser,
transpose derivation, and map identities.  It imports no producer, Task565
module, Task565 checker, or executable arithmetic helper.  A checker PASS is
printed only after every table record and structural identity has matched.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import re
import tempfile
import time
from collections import deque
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972.r07.grade2.forward-adjoint-maps.v3"
TABLE_SCHEMA = SCHEMA + ".sparse-jsonl"
PASS_MARKER = "R07_GRADE2_FORWARD_ADJOINT_MAPS_V3_CHECKER_PASS"
PRODUCER_MARKER = "R07_GRADE2_FORWARD_ADJOINT_MAPS_V3_CANDIDATE"
PRODUCER_PATH = ROOT / "search/d972_r07_grade2_forward_adjoint_maps_v3.py"
PRODUCER_SHA256 = "7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84"

CHARACTERS: tuple[tuple[int, int], ...] = ((0, 0), (0, 1), (1, 0), (1, 1))
ACTORS: tuple[int, ...] = (1, -1, 2, -2)
MONOMIALS: tuple[tuple[int, int, int], ...] = (
    (2, 0, 0), (1, 1, 0), (1, 0, 1),
    (0, 2, 0), (0, 1, 1), (0, 0, 2),
)
OCCURRENCES: tuple[tuple[int, int, int], ...] = (
    (0, 0, 1), (1, 0, 2), (2, 0, 1),
    (3, 1, 2), (4, 1, 2), (5, 1, 1),
)
PURE_WORDS: dict[tuple[int, int], tuple[int, ...]] = {
    (0, 0): (), (0, 1): (-2,) * 9,
    (1, 0): (-2, -2, 1, 1, 2, 1, 2, 1, 1),
    (1, 1): (-2, -2, -2, -1, -2, -1, -1, -1, -2, -1),
}
SOURCE_WIDTH = 36288
PHYSICAL_WIDTH = 48384
PSL_ORDER = 504
PACKING = "jsonl-triples-utf8-lf"

SOURCE_PINS: dict[str, tuple[int, str]] = {
    "search/d972_r07_a0_first_rung_grade2_prebuild_v1.py":
        (145917, "acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8"),
    "search/check_d972_r07_a0_first_rung_grade2_prebuild_v1.py":
        (80693, "fc6f9976b4e3164d4dff31c05256750ddb4758856f39ac5b1fceb43249fbdecf"),
    "search/d972_r07_a0_first_rung_grade1_v4.py":
        (144552, "1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4"),
    "scratchpad/a0_paper_words_v1.json":
        (115928, "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"),
}
MARKING_PATH = "scratchpad/fuda1_a0_rmax_data.g"
MARKING_SHA = "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"
RELATOR_SHA = "7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canon(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def strict_fixed(value: Any, expected: Any, label: str) -> None:
    if isinstance(expected, bool):
        if value is not expected:
            raise RuntimeError(label)
    elif isinstance(expected, int):
        if not is_int(value) or value != expected:
            raise RuntimeError(label)
    elif isinstance(expected, list):
        if not isinstance(value, list) or len(value) != len(expected):
            raise RuntimeError(label)
        for index, (actual_item, expected_item) in enumerate(zip(value, expected)):
            strict_fixed(actual_item, expected_item, f"{label}:{index}")
    elif isinstance(expected, dict):
        if not isinstance(value, dict) or set(value) != set(expected):
            raise RuntimeError(label)
        for key in expected:
            strict_fixed(value[key], expected[key], f"{label}:{key}")
    elif type(value) is not type(expected) or value != expected:
        raise RuntimeError(label)


def validate_producer_source(path: Path, expected: str) -> str:
    if not path.is_file():
        raise RuntimeError("producer_source_missing")
    actual = digest(path.read_bytes())
    if actual != expected:
        raise RuntimeError("producer_source_digest")
    return actual


def flags() -> dict[str, bool]:
    return {
        "independent_checker": False, "precision2": False,
        "A0": False, "COMMON": False, "COMPATIBLE_LIFT": False,
        "FAKE": False, "IHARA": False, "verified": False,
    }


def expected_dimensions() -> dict[str, Any]:
    return {
        "characters_count": 4,
        "source_degree2_per_character": SOURCE_WIDTH,
        "source_degree2_total": 4 * SOURCE_WIDTH,
        "physical_degree2": PHYSICAL_WIDTH,
        "source_slice": SOURCE_WIDTH, "physical": PHYSICAL_WIDTH,
        "source_tags": 6, "source_components": 2,
        "source_degree2_monomials": [list(x) for x in MONOMIALS],
        "psl_index_count": PSL_ORDER,
        "characters": [list(x) for x in CHARACTERS],
        "actors": list(ACTORS), "monomials_coupled": True,
    }


def expected_coordinate_order() -> dict[str, Any]:
    return {
        "characters": [list(x) for x in CHARACTERS], "actors": list(ACTORS),
        "source": ["tag", "component", "monomial", "psl_index"],
        "physical": ["character", "physical_block", "component", "monomial", "psl_index"],
        "degree2_monomials": [list(x) for x in MONOMIALS],
    }


def validate_manifest_fixed_fields(value: dict[str, Any]) -> None:
    strict_fixed(value.get("dimensions"), expected_dimensions(), "manifest_dimensions")
    strict_fixed(value.get("coordinate_order"), expected_coordinate_order(),
                 "manifest_coordinate_order")
    strict_fixed(value.get("occurrence_triples"), [list(x) for x in OCCURRENCES],
                 "manifest_occurrences")


def source_index(tag: int, component: int, monomial: int, psl: int) -> int:
    return (((tag * 2 + component) * 6 + monomial) * PSL_ORDER) + psl


def physical_index(character: int, block: int, component: int, monomial: int, psl: int) -> int:
    return ((((character * 2 + block) * 2 + component) * 6 + monomial) * PSL_ORDER) + psl


def source_tuple(index: int) -> tuple[int, int, int, int]:
    psl = index % PSL_ORDER
    value = index // PSL_ORDER
    mono = value % 6
    value //= 6
    component = value % 2
    return value // 2, component, mono, psl


def physical_tuple(index: int) -> tuple[int, int, int, int, int]:
    psl = index % PSL_ORDER
    value = index // PSL_ORDER
    mono = value % 6
    value //= 6
    component = value % 2
    value //= 2
    block = value % 2
    return value // 2, block, component, mono, psl


# Independent local quotient implementation.  Names and traversal differ
# from the producer so accidental import/shared-helper coupling is visible.
ID9 = tuple(range(9))
Affine = tuple[tuple[int, ...], int, int, tuple[int, int, int]]
OCCURRENCE_WORDS: tuple[tuple[list[int], list[int]], ...] = (
    ([1], [2]), ([1], [-1, -2]), ([2], [-1, -2]),
    ([-2, -1], [1]), ([1], [2]), ([-2, -1], [2]),
)
ETA = ((0, 1), (1, 0), (1, 1))


def pmul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    output = [0] * len(left)
    for index, value in enumerate(left):
        output[index] = right[value]
    return tuple(output)


def pinv(value: tuple[int, ...]) -> tuple[int, ...]:
    output = [0] * len(value)
    for index, image in enumerate(value):
        output[image] = index
    return tuple(output)


def winv(word: Iterable[int]) -> tuple[int, ...]:
    values = tuple(int(x) for x in word)
    return tuple(-x for x in values[::-1])


def wproduct(*parts: Iterable[int]) -> tuple[int, ...]:
    result: list[int] = []
    for part in parts:
        for value in part:
            value = int(value)
            if value not in (-2, -1, 1, 2):
                raise RuntimeError("word_letter")
            if result and result[-1] == -value:
                result.pop()
            else:
                result.append(value)
    return tuple(result)


def substitute(word: Iterable[int], x: Iterable[int], y: Iterable[int]) -> tuple[int, ...]:
    x = tuple(x); y = tuple(y)
    parts = []
    for value in word:
        parts.append(x if value == 1 else y if value == 2 else winv(x) if value == -1 else winv(y))
    return wproduct(*parts)


def qproduct(left: tuple[tuple[int, ...], int, int], right: tuple[tuple[int, ...], int, int]) -> tuple[tuple[int, ...], int, int]:
    return pmul(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2]


def qinverse(value: tuple[tuple[int, ...], int, int]) -> tuple[tuple[int, ...], int, int]:
    return pinv(value[0]), value[1], value[2]


def qword(word: Iterable[int], images: tuple[tuple[tuple[int, ...], int, int], tuple[tuple[int, ...], int, int]]) -> tuple[tuple[int, ...], int, int]:
    result = (ID9, 0, 0)
    for value in word:
        value = int(value)
        result = qproduct(result, images[abs(value) - 1] if value > 0 else qinverse(images[abs(value) - 1]))
    return result


def character_sign(label: tuple[int, int], parity: tuple[int, int]) -> int:
    return 1 if ((label[0] * parity[0] + label[1] * parity[1]) & 1) == 0 else 2


def kernel_action(parity: tuple[int, int], value: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((character_sign(ETA[index], parity) * value[index]) % 3 for index in range(3))  # type: ignore[return-value]


def amul(left: Affine, right: Affine) -> Affine:
    acted = kernel_action((right[1], right[2]), left[3])
    return pmul(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2], tuple((acted[i] + right[3][i]) % 3 for i in range(3))  # type: ignore[return-value]


def ainverse(value: Affine) -> Affine:
    acted = kernel_action((value[1], value[2]), value[3])
    return pinv(value[0]), value[1], value[2], tuple((-v) % 3 for v in acted)  # type: ignore[return-value]


def aword(word: Iterable[int], images: tuple[Affine, Affine]) -> Affine:
    result: Affine = (ID9, 0, 0, (0, 0, 0))
    inverse = ainverse(images[0]), ainverse(images[1])
    for value in word:
        value = int(value)
        result = amul(result, images[abs(value) - 1] if value > 0 else inverse[abs(value) - 1])
    return result


def m2product(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (left[0][0] * right[0][0] ^ left[0][1] * right[1][0], left[0][0] * right[0][1] ^ left[0][1] * right[1][1]),
        (left[1][0] * right[0][0] ^ left[1][1] * right[1][0], left[1][0] * right[0][1] ^ left[1][1] * right[1][1]),
    )


def marking_generators() -> tuple[tuple[int, ...], tuple[int, ...]]:
    data = (ROOT / MARKING_PATH).read_bytes()
    if digest(data) != MARKING_SHA:
        raise RuntimeError("marking_pin")
    match = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;", data.decode("utf-8"), re.S)
    if match is None:
        raise RuntimeError("marking_syntax")
    values = [tuple(int(x) - 1 for x in ast.literal_eval(match.group(i))) for i in (1, 2)]
    if any(len(x) != 36 for x in values):
        raise RuntimeError("marking_width")
    return values[0][:9], values[1][:9]


def enumerate_psl(generators: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[tuple[tuple[int, ...], ...], dict[tuple[int, ...], int]]:
    steps = (generators[0], generators[1], pinv(generators[0]), pinv(generators[1]))
    seen: dict[tuple[int, ...], int] = {ID9: 0}
    values: list[tuple[int, ...]] = [ID9]
    todo: deque[tuple[int, ...]] = deque([ID9])
    while todo:
        current = todo.popleft()
        for step in steps:
            candidate = pmul(current, step)
            if candidate not in seen:
                seen[candidate] = len(values)
                values.append(candidate)
                todo.append(candidate)
    if len(values) != PSL_ORDER:
        raise RuntimeError("psl_cardinality")
    return tuple(values), seen


def json_affine(value: Affine) -> dict[str, Any]:
    return {"psl": list(value[0]), "parity": [value[1], value[2]], "kernel": list(value[3])}


class IndependentContext:
    def __init__(self, words: dict[str, Any]):
        first, second = marking_generators()
        self.qimages = ((first, 1, 0), (second, 0, 1))
        self.aimages: tuple[Affine, Affine] = (
            (first, 1, 0, (1, 0, 0)), (second, 0, 1, (1, 1, 1)),
        )
        self.psl, self.psl_index = enumerate_psl((first, second))
        self.transports: list[dict[tuple[int, int], tuple[int, int]]] = []
        self.matrices: list[list[list[int]]] = []
        for left_word, right_word in OCCURRENCE_WORDS:
            left = qword(left_word, self.qimages)
            right = qword(right_word, self.qimages)
            matrix = ((left[1], right[1]), (left[2], right[2]))
            inverse = None
            for a in range(2):
                for b in range(2):
                    for c in range(2):
                        for d in range(2):
                            candidate = ((a, b), (c, d))
                            if m2product(matrix, candidate) == ((1, 0), (0, 1)) and m2product(candidate, matrix) == ((1, 0), (0, 1)):
                                inverse = candidate
            if inverse is None:
                raise RuntimeError("transport_inverse")
            self.matrices.append([list(matrix[0]), list(matrix[1])])
            self.transports.append({
                label: ((label[0] * inverse[0][0]) ^ (label[1] * inverse[1][0]), (label[0] * inverse[0][1]) ^ (label[1] * inverse[1][1]))
                for label in CHARACTERS
            })
        self.source_actor: dict[int, tuple[tuple[int, ...], int, int]] = {letter: qword((letter,), self.qimages) for letter in ACTORS}
        self.actor_tags: dict[int, tuple[Affine, ...]] = {
            letter: tuple(aword(substitute((letter,), *pair), self.aimages) for pair in OCCURRENCE_WORDS)
            for letter in ACTORS
        }
        g = tuple(int(value) for value in words.get("g760", ()))
        if len(g) != 760:
            raise RuntimeError("g760_cardinality")
        self.g_tags = tuple(aword(substitute(g, *pair), self.aimages) for pair in OCCURRENCE_WORDS)
        identity: Affine = (ID9, 0, 0, (0, 0, 0))
        self.shifts: tuple[Affine, ...] = (
            identity, self.g_tags[2], self.g_tags[2],
            amul(self.g_tags[5], ainverse(self.g_tags[4])),
            self.g_tags[5], self.g_tags[5],
        )
        self.shift_words = (
            "identity", "tags(g760)[2]", "tags(g760)[2]",
            "tags(g760)[5] * tags(g760)[4]^-1", "tags(g760)[5]", "tags(g760)[5]",
        )
        self.maps: dict[tuple[int, ...], tuple[int, ...]] = {}

    def left_map(self, permutation: tuple[int, ...]) -> tuple[int, ...]:
        if permutation not in self.maps:
            self.maps[permutation] = tuple(self.psl_index[pmul(permutation, value)] for value in self.psl)
        return self.maps[permutation]

    def prefix_record(self) -> dict[str, Any]:
        values = [json_affine(value) for value in self.shifts]
        return {
            "derivation_order": list(self.shift_words), "values": values,
            "sha256": digest(canon(values)),
            "nonidentity_count": sum(value != (ID9, 0, 0, (0, 0, 0)) for value in self.shifts),
        }


def authenticate_inputs() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for relative, (size, expected) in SOURCE_PINS.items():
        data = (ROOT / relative).read_bytes()
        actual = digest(data)
        if len(data) != size or actual != expected:
            raise RuntimeError(f"source_pin:{relative}")
        result[relative] = {"bytes": len(data), "sha256": actual}
    marking = ROOT / MARKING_PATH
    data = marking.read_bytes()
    if digest(data) != MARKING_SHA:
        raise RuntimeError("marking_source_pin")
    result[MARKING_PATH] = {"bytes": len(data), "sha256": MARKING_SHA}
    return result


def words_input() -> tuple[dict[str, Any], dict[str, Any]]:
    path = ROOT / "scratchpad/a0_paper_words_v1.json"
    data = path.read_bytes()
    if digest(data) != SOURCE_PINS["scratchpad/a0_paper_words_v1.json"][1]:
        raise RuntimeError("word_pin")
    value = json.loads(data)
    if not isinstance(value, dict) or len(value.get("relators", [])) != 44:
        raise RuntimeError("relator_roster")
    relator_digest = digest(json.dumps(value["relators"], sort_keys=True, separators=(",", ":")).encode("ascii"))
    if relator_digest != RELATOR_SHA or value.get("relators_sha256") != RELATOR_SHA:
        raise RuntimeError("relator_digest")
    if not isinstance(value.get("g760"), list) or len(value["g760"]) != 760:
        raise RuntimeError("g760_roster")
    return value, {"bytes": len(data), "sha256": digest(data), "relators_sha256": relator_digest, "g760_length": 760}


def reduce_sparse(records: Iterable[Sequence[int]], source_width: int, destination_width: int) -> tuple[list[tuple[int, int, int]], int]:
    sums: dict[tuple[int, int], int] = {}
    seen = 0
    for record in records:
        seen += 1
        if len(record) != 3 or any(not is_int(x) for x in record):
            raise RuntimeError("raw_sparse_shape")
        source, destination, coefficient = int(record[0]), int(record[1]), int(record[2]) % 3
        if not (0 <= source < source_width and 0 <= destination < destination_width):
            raise RuntimeError("raw_sparse_range")
        key = source, destination
        sums[key] = (sums.get(key, 0) + coefficient) % 3
    return [(s, d, c) for (s, d), c in sorted(sums.items()) if c], seen


def transpose(records: Iterable[Sequence[int]], source_width: int, destination_width: int) -> list[tuple[int, int, int]]:
    return reduce_sparse(((int(d), int(s), int(c)) for s, d, c in records), destination_width, source_width)[0]


def actor_records(ctx: IndependentContext, character: int, actor_number: int) -> Iterator[tuple[int, int, int]]:
    letter = ACTORS[actor_number]
    scalar = character_sign(CHARACTERS[character], (ctx.source_actor[letter][1], ctx.source_actor[letter][2]))
    for tag in range(6):
        pmap = ctx.left_map(ctx.actor_tags[letter][tag][0])
        for component in range(2):
            for monomial in range(6):
                base = source_index(tag, component, monomial, 0)
                for psl, destination_psl in enumerate(pmap):
                    yield base + psl, base + destination_psl, scalar


def aggregation_records(ctx: IndependentContext, character: int) -> Iterator[tuple[int, int, int]]:
    label = CHARACTERS[character]
    for tag, block, occurrence_coefficient in OCCURRENCES:
        target = ctx.transports[tag][label]
        target_character = CHARACTERS.index(target)
        shift = ctx.shifts[tag]
        scalar = occurrence_coefficient * character_sign(target, (shift[1], shift[2]))
        pmap = ctx.left_map(shift[0])
        for component in range(2):
            for monomial in range(6):
                base = source_index(tag, component, monomial, 0)
                for psl, destination_psl in enumerate(pmap):
                    yield base + psl, physical_index(target_character, block, component, monomial, destination_psl), scalar


def sparse_apply(records: Iterable[Sequence[int]], vector: Sequence[int], source_width: int, destination_width: int, *, dual: bool = False) -> list[int]:
    required = destination_width if dual else source_width
    if len(vector) != required:
        raise RuntimeError("apply_width")
    result = [0] * (source_width if dual else destination_width)
    for source, destination, coefficient in records:
        if dual:
            result[int(source)] = (result[int(source)] + int(coefficient) * int(vector[int(destination)])) % 3
        else:
            result[int(destination)] = (result[int(destination)] + int(coefficient) * int(vector[int(source)])) % 3
    return result


def record_line(record: Sequence[int]) -> bytes:
    return (json.dumps([int(record[0]), int(record[1]), int(record[2])], separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def parse_exact(path: Path, receipt: dict[str, Any], source_width: int, destination_width: int, expected: Sequence[Sequence[int]]) -> list[tuple[int, int, int]]:
    if not isinstance(receipt, dict):
        raise RuntimeError("table_receipt_type")
    required = {"file", "schema", "source_width", "destination_width", "entry_count", "body_bytes", "body_sha256", "bytes", "sha256", "eof", "encoding", "map_kind", "map_direction", "character"}
    if path.name.startswith("T_"):
        required.add("actor")
    if set(receipt) != required:
        raise RuntimeError("table_receipt_keys")
    if receipt.get("file") != path.name or receipt.get("schema") != TABLE_SCHEMA or receipt.get("source_width") != source_width or receipt.get("destination_width") != destination_width or receipt.get("encoding") != PACKING or receipt.get("eof") is not True:
        raise RuntimeError("table_receipt_metadata")
    for key in ("source_width", "destination_width", "entry_count", "body_bytes", "bytes", "character"):
        if not is_int(receipt.get(key)):
            raise RuntimeError("table_bool_as_int")
    if path.name.startswith("T_") and not is_int(receipt.get("actor")):
        raise RuntimeError("table_actor_bool_as_int")
    raw = path.read_bytes()
    stream = io.BytesIO(raw)
    records: list[tuple[int, int, int]] = []
    body_hash = hashlib.sha256()
    body_size = 0
    previous: tuple[int, int] | None = None
    eof: dict[str, Any] | None = None
    while True:
        line = stream.readline()
        if not line:
            break
        if not line.endswith(b"\n") or line == b"\n":
            raise RuntimeError("table_lf_or_blank")
        try:
            item = json.loads(line)
        except Exception as error:
            raise RuntimeError("table_json") from error
        if isinstance(item, dict):
            if eof is not None or set(item) != {"body_bytes", "body_sha256", "count", "eof"} or item.get("eof") is not True or canon(item) != line:
                raise RuntimeError("table_eof")
            eof = item
            if stream.read(1):
                raise RuntimeError("table_after_eof")
            break
        if not isinstance(item, list) or len(item) != 3 or any(not is_int(x) for x in item):
            raise RuntimeError("table_record")
        record = tuple(int(x) for x in item)
        if not (0 <= record[0] < source_width and 0 <= record[1] < destination_width and record[2] in (1, 2)):
            raise RuntimeError("table_record_range")
        if previous is not None and record[:2] <= previous:
            raise RuntimeError("table_noncanonical_order")
        if record_line(record) != line:
            raise RuntimeError("table_record_encoding")
        if len(records) >= len(expected) or record != tuple(int(x) for x in expected[len(records)]):
            raise RuntimeError("table_entry_mismatch")
        previous = record[:2]
        records.append(record)
        body_hash.update(line)
        body_size += len(line)
    if eof is None or records != [tuple(int(x) for x in value) for value in expected]:
        raise RuntimeError("table_truncated_or_extra")
    if not is_int(eof.get("count")) or not is_int(eof.get("body_bytes")) or eof.get("count") != len(records) or eof.get("body_bytes") != body_size or eof.get("body_sha256") != body_hash.hexdigest():
        raise RuntimeError("table_body_digest")
    if receipt.get("entry_count") != len(records) or receipt.get("body_bytes") != body_size or receipt.get("body_sha256") != body_hash.hexdigest() or receipt.get("bytes") != len(raw) or receipt.get("sha256") != digest(raw):
        raise RuntimeError("table_receipt_digest")
    return records


def map_specs() -> list[tuple[str, str, int, int, int | None]]:
    specs: list[tuple[str, str, int, int, int | None]] = []
    for character in range(4):
        for actor_number in range(4):
            specs.append((f"T_fwd_a{character}_t{actor_number}.jsonl", "forward", character, character, actor_number))
            specs.append((f"T_adj_a{character}_t{actor_number}.jsonl", "adjoint", character, character, actor_number))
        specs.append((f"B_fwd_a{character}.jsonl", "forward", character, character, None))
        specs.append((f"B_adj_a{character}.jsonl", "adjoint", character, character, None))
    return specs


def expected_roster() -> list[str]:
    return ["manifest.json", "producer.marker"] + [item[0] for item in map_specs()]


def verify_coverage(records: Sequence[Sequence[int]], source_width: int, destination_width: int, physical: bool) -> dict[str, Any]:
    sources = {int(value[0]) for value in records}
    if sources != set(range(source_width)):
        raise RuntimeError("coverage_source")
    source_values = {source_tuple(value) for value in sources}
    destination_values = {(physical_tuple(value) if physical else source_tuple(value)) for value in {int(item[1]) for item in records}}
    result = {
        "source_coordinates": len(source_values),
        "source_tags": sorted({value[0] for value in source_values}),
        "source_components": sorted({value[1] for value in source_values}),
        "source_monomials": sorted({value[2] for value in source_values}),
        "source_psl_indices": len({value[3] for value in source_values}),
        "destination_coordinates": len(destination_values),
        "destination_components": sorted({value[2 if physical else 1] for value in destination_values}),
        "destination_monomials": sorted({value[3 if physical else 2] for value in destination_values}),
        "destination_psl_indices": len({value[4 if physical else 3] for value in destination_values}),
    }
    if result["source_tags"] != list(range(6)) or result["source_components"] != [0, 1] or result["source_monomials"] != list(range(6)) or result["source_psl_indices"] != PSL_ORDER or result["destination_components"] != [0, 1] or result["destination_monomials"] != list(range(6)) or result["destination_psl_indices"] != PSL_ORDER:
        raise RuntimeError("coverage_cases")
    if physical:
        result["destination_characters"] = sorted({value[0] for value in destination_values})
        result["destination_blocks"] = sorted({value[1] for value in destination_values})
        if result["destination_blocks"] != [0, 1]:
            raise RuntimeError("coverage_physical_cases")
    return result


def check_inverse(first: Sequence[Sequence[int]], second: Sequence[Sequence[int]], width: int) -> int:
    one: dict[int, tuple[int, int]] = {}
    two: dict[int, tuple[int, int]] = {}
    for source, destination, coefficient in first:
        if int(source) in one:
            raise RuntimeError("inverse_branch")
        one[int(source)] = int(destination), int(coefficient)
    for source, destination, coefficient in second:
        if int(source) in two:
            raise RuntimeError("inverse_branch_reverse")
        two[int(source)] = int(destination), int(coefficient)
    if set(one) != set(range(width)) or set(two) != set(range(width)):
        raise RuntimeError("inverse_coverage")
    for source in range(width):
        target, coefficient = one[source]
        back, reverse_coefficient = two[target]
        if back != source or coefficient * reverse_coefficient % 3 != 1:
            raise RuntimeError("inverse_identity")
    return width


def check_artifact(directory: Path) -> dict[str, Any]:
    started = time.monotonic()
    producer_digest = validate_producer_source(PRODUCER_PATH, PRODUCER_SHA256)
    directory = directory.resolve()
    if not directory.is_dir():
        raise RuntimeError("artifact_directory")
    manifest_path = directory / "manifest.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if canon(manifest) != manifest_bytes:
        raise RuntimeError("manifest_canonicality")
    required_manifest = {
        "schema", "marker", "fixture", "dimensions", "coordinate_order",
        "occurrence_triples", "prefix_shifts", "source_pins", "word_input",
        "marking_input", "producer_sha256", "tables", "table_roster",
        "output_roster", "structural_identities", "rows_emitted", "map_count", "table_count",
        "elapsed_seconds", "peak_rss_bytes", "claim_flags", "terminal",
        "ACTUAL_MAP_BUILD", "GRADE2_DECISION", "verified",
    }
    if set(manifest) != required_manifest:
        raise RuntimeError("manifest_keys")
    if manifest.get("schema") != SCHEMA or manifest.get("marker") != PRODUCER_MARKER or manifest.get("fixture") is not False or manifest.get("claim_flags") != flags() or manifest.get("terminal") != PRODUCER_MARKER or manifest.get("ACTUAL_MAP_BUILD") != "DEFERRED_TO_GHA" or manifest.get("GRADE2_DECISION") != "NOT_RUN" or manifest.get("verified") is not False or manifest.get("producer_sha256") != producer_digest:
        raise RuntimeError("manifest_semantics")
    validate_manifest_fixed_fields(manifest)
    if not is_int(manifest.get("rows_emitted")) or not is_int(manifest.get("map_count")) or not is_int(manifest.get("table_count")) or not is_int(manifest.get("peak_rss_bytes")):
        raise RuntimeError("manifest_bool_as_int")
    if isinstance(manifest.get("elapsed_seconds"), bool) or not isinstance(manifest.get("elapsed_seconds"), (int, float)) or manifest.get("elapsed_seconds") < 0:
        raise RuntimeError("manifest_elapsed")
    source_receipt = authenticate_inputs()
    strict_fixed(manifest.get("source_pins"), source_receipt, "manifest_source_binding")
    strict_fixed(manifest.get("marking_input"), source_receipt[MARKING_PATH],
                 "manifest_marking_binding")
    words, word_receipt = words_input()
    strict_fixed(manifest.get("word_input"), word_receipt, "manifest_word_binding")
    context = IndependentContext(words)
    strict_fixed(manifest.get("prefix_shifts"), context.prefix_record(),
                 "manifest_prefix_binding")
    marker_bytes = (directory / "producer.marker").read_bytes()
    if marker_bytes != (PRODUCER_MARKER + "\n").encode("ascii"):
        raise RuntimeError("producer_marker")
    roster = manifest.get("output_roster")
    if roster != expected_roster() or manifest.get("table_roster") != expected_roster()[2:]:
        raise RuntimeError("manifest_roster")
    actual_files = sorted(path.name for path in directory.iterdir() if path.is_file())
    permitted_files = sorted(expected_roster())
    # The producer artifact itself has an exact roster.  Checker receipts are
    # written outside that artifact (or to --output after this check).
    extras = set(actual_files) - set(permitted_files)
    missing = set(permitted_files) - set(actual_files)
    if extras or missing:
        raise RuntimeError(f"artifact_roster:{sorted(extras)}:{sorted(missing)}")
    table_records: dict[str, list[tuple[int, int, int]]] = {}
    receipts = manifest.get("tables")
    if not isinstance(receipts, list) or manifest.get("table_count") != len(map_specs()) or len(receipts) != len(map_specs()) or manifest.get("table_roster") != [receipt.get("file") for receipt in receipts]:
        raise RuntimeError("manifest_table_roster")
    for receipt, spec in zip(receipts, map_specs()):
        filename, direction, character, _, actor_number = spec
        if receipt.get("file") != filename or receipt.get("map_direction") != direction or receipt.get("character") != character or receipt.get("map_kind") != ("T" if filename.startswith("T_") else "B") or (actor_number is not None and receipt.get("actor") != ACTORS[actor_number]):
            raise RuntimeError("table_descriptor")
        if filename.startswith("T_"):
            expected, _ = reduce_sparse(actor_records(context, character, int(actor_number)), SOURCE_WIDTH, SOURCE_WIDTH)
            source_width = destination_width = SOURCE_WIDTH
        else:
            expected, _ = reduce_sparse(aggregation_records(context, character), SOURCE_WIDTH, PHYSICAL_WIDTH)
            source_width, destination_width = (SOURCE_WIDTH, PHYSICAL_WIDTH) if direction == "forward" else (PHYSICAL_WIDTH, SOURCE_WIDTH)
        if direction == "adjoint":
            if filename.startswith("T_"):
                expected = transpose(expected, SOURCE_WIDTH, SOURCE_WIDTH)
            else:
                expected = transpose(expected, SOURCE_WIDTH, PHYSICAL_WIDTH)
        parsed = parse_exact(directory / filename, receipt, source_width, destination_width, expected)
        table_records[filename] = parsed
    if manifest.get("rows_emitted") != sum(len(value) for value in table_records.values()) or manifest.get("map_count") != 20:
        raise RuntimeError("manifest_count")
    for character in range(4):
        for first, second in ((0, 1), (2, 3)):
            check_inverse(table_records[f"T_fwd_a{character}_t{first}.jsonl"], table_records[f"T_fwd_a{character}_t{second}.jsonl"], SOURCE_WIDTH)
    for character in range(4):
        forward = table_records[f"B_fwd_a{character}.jsonl"]
        adjoint = table_records[f"B_adj_a{character}.jsonl"]
        if adjoint != transpose(forward, SOURCE_WIDTH, PHYSICAL_WIDTH):
            raise RuntimeError("B_transpose")
    all_b_characters = sorted({physical_tuple(int(item[1]))[0] for name, values in table_records.items() if name.startswith("B_fwd_") for item in values})
    if all_b_characters != list(range(4)):
        raise RuntimeError("B_character_coverage")
    if any(table_records[f"T_adj_a{character}_t{actor}.jsonl"] != transpose(table_records[f"T_fwd_a{character}_t{actor}.jsonl"], SOURCE_WIDTH, SOURCE_WIDTH) for character in range(4) for actor in range(4)):
        raise RuntimeError("T_transpose")
    tcoverage = verify_coverage(table_records["T_fwd_a0_t0.jsonl"], SOURCE_WIDTH, SOURCE_WIDTH, False)
    bcoverage = verify_coverage(table_records["B_fwd_a0.jsonl"], SOURCE_WIDTH, PHYSICAL_WIDTH, True)
    coefficient_values = {int(item[2]) for values in table_records.values() for item in values}
    structural = manifest.get("structural_identities")
    expected_transpose_count = sum(len(value) for name, value in table_records.items() if "_adj_" in name)
    expected_structural = {
        "canonical_entry_legal": True, "transpose_entrywise": True,
        "transpose_entries_checked": expected_transpose_count,
        "actor_inverse_entrywise": True,
        "inverse_source_coordinates_checked": 8 * SOURCE_WIDTH,
        "all_sign_cases_visited": True, "coefficient_values": [1, 2],
        "all_prefix_cases_visited": True, "all_component_cases_visited": True,
        "all_monomial_cases_visited": True, "all_psl_index_cases_visited": True,
        "T_forward_table_count": 16, "B_forward_table_count": 4,
        "T_coverage": tcoverage, "B_coverage": bcoverage,
        "B_all_character_cases_visited": True, "B_occurrence_first": True,
        "B_occurrence_records_before_aggregation": 36288,
        "physical_row_action": False, "monomials_split": False,
        "sampled_dot_products_are_canaries_only": True,
    }
    if coefficient_values != {1, 2}:
        raise RuntimeError("structural_coefficients")
    strict_fixed(structural, expected_structural, "structural_receipt")
    result = {
        "schema": SCHEMA + ".checker",
        "marker": PASS_MARKER,
        "producer_manifest_sha256": digest(manifest_bytes),
        "producer_sha256": manifest["producer_sha256"],
        "checker_sha256": digest(Path(__file__).resolve().read_bytes()),
        "tables_checked": len(table_records),
        "entries_checked": sum(len(value) for value in table_records.values()),
        "source_dimensions": {"V_a": SOURCE_WIDTH, "P": PHYSICAL_WIDTH},
        "occurrence_triples": [list(x) for x in OCCURRENCES],
        "prefix_sha256": context.prefix_record()["sha256"],
        "structural_identities": {
            "canonical_entry_legal": True, "inverse_source_coordinates": 8 * SOURCE_WIDTH,
            "transpose_entries": sum(len(value) for name, value in table_records.items() if "_adj_" in name),
            "all_cases_visited": True, "B_occurrence_first": True,
        },
        "claim_flags": flags(),
        "terminal": PASS_MARKER,
        "ACTUAL_MAP_BUILD": "DEFERRED_TO_GHA",
        "GRADE2_DECISION": "NOT_RUN",
        "verified": False,
        "elapsed_seconds": time.monotonic() - started,
    }
    return result


def safe_output_path(artifact: Path, path: Path) -> Path:
    artifact = artifact.resolve()
    candidate = path.absolute()
    if candidate.exists():
        raise RuntimeError("output_exists")
    cursor = candidate.parent
    while True:
        if cursor.exists():
            if cursor.is_symlink() or (hasattr(cursor, "is_junction") and cursor.is_junction()):
                raise RuntimeError("output_reparse")
        if cursor == cursor.parent:
            break
        cursor = cursor.parent
    resolved = candidate.resolve()
    if resolved == artifact or artifact in resolved.parents:
        raise RuntimeError("output_inside_artifact")
    if resolved == ROOT or ROOT in resolved.parents:
        raise RuntimeError("output_inside_repository")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    if resolved.parent.resolve() != resolved.parent:
        raise RuntimeError("output_parent_reparse")
    return resolved


def atomic_output(path: Path, value: dict[str, Any], artifact: Path) -> None:
    path = safe_output_path(artifact, path)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(canon(value)); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
        if path.read_bytes() != canon(value):
            raise RuntimeError("output_readback")
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def selftest() -> dict[str, Any]:
    started = time.monotonic()
    producer_digest = validate_producer_source(PRODUCER_PATH, PRODUCER_SHA256)
    authenticate_inputs()
    words, _ = words_input()
    context = IndependentContext(words)
    prefix = context.prefix_record()
    if prefix["nonidentity_count"] <= 0:
        raise RuntimeError("fixture_prefix")
    actual_actor = {
        actor_number: reduce_sparse(
            actor_records(context, 0, actor_number), SOURCE_WIDTH, SOURCE_WIDTH)[0]
        for actor_number in range(4)
    }
    actor_coverage = verify_coverage(actual_actor[0], SOURCE_WIDTH, SOURCE_WIDTH,
                                     False)
    if actor_coverage != {
        "source_coordinates": SOURCE_WIDTH, "source_tags": list(range(6)),
        "source_components": [0, 1], "source_monomials": list(range(6)),
        "source_psl_indices": PSL_ORDER,
        "destination_coordinates": SOURCE_WIDTH,
        "destination_components": [0, 1],
        "destination_monomials": list(range(6)),
        "destination_psl_indices": PSL_ORDER,
    }:
        raise RuntimeError("fixture_actual_actor_coverage")
    check_inverse(actual_actor[0], actual_actor[1], SOURCE_WIDTH)
    check_inverse(actual_actor[2], actual_actor[3], SOURCE_WIDTH)
    actor_probe = [index % 3 for index in range(SOURCE_WIDTH)]
    if sparse_apply(actual_actor[1], sparse_apply(actual_actor[0], actor_probe,
                    SOURCE_WIDTH, SOURCE_WIDTH), SOURCE_WIDTH, SOURCE_WIDTH) != actor_probe:
        raise RuntimeError("fixture_actual_x_inverse_application")
    if sparse_apply(actual_actor[3], sparse_apply(actual_actor[2], actor_probe,
                    SOURCE_WIDTH, SOURCE_WIDTH), SOURCE_WIDTH, SOURCE_WIDTH) != actor_probe:
        raise RuntimeError("fixture_actual_y_inverse_application")
    actual_b, _ = reduce_sparse(
        aggregation_records(context, 0), SOURCE_WIDTH, PHYSICAL_WIDTH)
    nonidentity_tag = next(index for index, value in enumerate(context.shifts)
                           if value != (ID9, 0, 0, (0, 0, 0)))
    prefix_probe = [0] * SOURCE_WIDTH
    prefix_probe[source_index(nonidentity_tag, 0, 0, 0)] = 1
    if not any(sparse_apply(actual_b, prefix_probe, SOURCE_WIDTH, PHYSICAL_WIDTH)):
        raise RuntimeError("fixture_actual_prefix_application")
    cancelled, count = reduce_sparse(((0, 1, 1), (0, 1, 2)), 12, 12)
    if count != 2 or cancelled:
        raise RuntimeError("fixture_duplicate")
    raw = [
        (0, 1, 2), (1, 2, 2), (2, 0, 1),
        (3, 4, 1), (4, 5, 2), (5, 3, 1),
        (6, 7, 1), (7, 8, 2), (8, 6, 1),
        (9, 10, 2), (10, 11, 1), (11, 9, 2),
    ]
    forward, _ = reduce_sparse(raw, 12, 12)
    adjoint = transpose(forward, 12, 12)
    forward2, _ = reduce_sparse(tuple((index, (index + 2) % 12, 1 if index % 2 else 2) for index in range(12)), 12, 12)
    adjoint2 = transpose(forward2, 12, 12)
    rejections = 0
    live = {"reduce_sparse", "transpose", "parse_exact", "sparse_apply",
            "check_inverse", "actor_records", "aggregation_records",
            "verify_coverage",
            "validate_manifest_fixed_fields", "safe_output_path"}
    with tempfile.TemporaryDirectory(prefix="task712-checker-fixture-") as name:
        directory = Path(name)
        def write(name0: str, values: Sequence[Sequence[int]]) -> dict[str, Any]:
            body = b"".join(record_line(item) for item in values)
            eof = canon({"body_bytes": len(body), "body_sha256": digest(body), "count": len(values), "eof": True})
            data = body + eof
            (directory / name0).write_bytes(data)
            return {"file": name0, "schema": TABLE_SCHEMA, "source_width": 12, "destination_width": 12, "entry_count": len(values), "body_bytes": len(body), "body_sha256": digest(body), "bytes": len(data), "sha256": digest(data), "eof": True, "encoding": PACKING, "map_kind": "T", "map_direction": "forward", "character": 0}
        fwd_receipt = write("tiny-fwd.jsonl", forward)
        adj_receipt = write("tiny-adj.jsonl", adjoint)
        fwd_receipt2 = write("tiny-fwd-pair2.jsonl", forward2)
        adj_receipt2 = write("tiny-adj-pair2.jsonl", adjoint2)
        actual_body = b"".join(record_line(item) for item in actual_b)
        actual_eof = canon({"body_bytes": len(actual_body),
                            "body_sha256": digest(actual_body),
                            "count": len(actual_b), "eof": True})
        actual_data = actual_body + actual_eof
        actual_path = directory / "B_fwd_a0.jsonl"
        actual_path.write_bytes(actual_data)
        actual_receipt = {
            "file": actual_path.name, "schema": TABLE_SCHEMA,
            "source_width": SOURCE_WIDTH, "destination_width": PHYSICAL_WIDTH,
            "entry_count": len(actual_b), "body_bytes": len(actual_body),
            "body_sha256": digest(actual_body), "bytes": len(actual_data),
            "sha256": digest(actual_data), "eof": True, "encoding": PACKING,
            "map_kind": "B", "map_direction": "forward", "character": 0,
        }
        parse_exact(actual_path, actual_receipt, SOURCE_WIDTH, PHYSICAL_WIDTH, actual_b)
        parsed_fwd = parse_exact(directory / "tiny-fwd.jsonl", fwd_receipt, 12, 12, forward)
        parsed_adj = parse_exact(directory / "tiny-adj.jsonl", adj_receipt, 12, 12, adjoint)
        parsed_fwd2 = parse_exact(directory / "tiny-fwd-pair2.jsonl", fwd_receipt2, 12, 12, forward2)
        parsed_adj2 = parse_exact(directory / "tiny-adj-pair2.jsonl", adj_receipt2, 12, 12, adjoint2)
        if parsed_adj != transpose(parsed_fwd, 12, 12):
            raise RuntimeError("fixture_transpose")
        check_inverse(parsed_fwd, parsed_adj, 12)
        if parsed_adj2 != transpose(parsed_fwd2, 12, 12):
            raise RuntimeError("fixture_transpose_pair2")
        check_inverse(parsed_fwd2, parsed_adj2, 12)
        for basis in range(12):
            vector = [0] * 12; vector[basis] = 1
            if sparse_apply(parsed_adj, sparse_apply(parsed_fwd, vector, 12, 12), 12, 12) != vector:
                raise RuntimeError("fixture_apply_inverse")
        if forward[0][0] % 6 == forward[0][1] % 6:
            raise RuntimeError("fixture_monomial_mix")
        original = (directory / "tiny-fwd.jsonl").read_bytes()
        (directory / "tiny-fwd.jsonl").write_bytes(original[:-1])
        try:
            parse_exact(directory / "tiny-fwd.jsonl", fwd_receipt, 12, 12, forward)
        except Exception:
            rejections += 1
        else:
            raise RuntimeError("fixture_truncation")
        (directory / "tiny-fwd.jsonl").write_bytes(original + b"\n")
        try:
            parse_exact(directory / "tiny-fwd.jsonl", fwd_receipt, 12, 12, forward)
        except Exception:
            rejections += 1
        else:
            raise RuntimeError("fixture_trailing")
        (directory / "tiny-fwd.jsonl").write_bytes(original)

        typed_path = directory / "T_fixture.jsonl"
        typed_path.write_bytes(original)
        typed_receipt = {**fwd_receipt, "file": typed_path.name, "actor": 1}
        parse_exact(typed_path, typed_receipt, 12, 12, forward)
        for field, bad in (("actor", True), ("character", False)):
            mutated = dict(typed_receipt)
            mutated[field] = bad
            try:
                parse_exact(typed_path, mutated, 12, 12, forward)
            except Exception:
                rejections += 1
            else:
                raise RuntimeError("fixture_nested_bool:" + field)

        fixed = {"dimensions": expected_dimensions(),
                 "coordinate_order": expected_coordinate_order(),
                 "occurrence_triples": [list(x) for x in OCCURRENCES]}
        validate_manifest_fixed_fields(fixed)
        for label, mutate in (
            ("occurrence", lambda value: value["occurrence_triples"][0].__setitem__(0, False)),
            ("dimension", lambda value: value["dimensions"].__setitem__("characters_count", True)),
            ("order", lambda value: value["coordinate_order"]["actors"].__setitem__(0, True)),
        ):
            altered = json.loads(json.dumps(fixed))
            mutate(altered)
            try:
                validate_manifest_fixed_fields(altered)
            except Exception:
                rejections += 1
            else:
                raise RuntimeError("fixture_manifest_bool:" + label)

        changed = directory / "changed_producer.py"
        changed.write_bytes(PRODUCER_PATH.read_bytes() + b"\n")
        for path, wanted in ((changed, PRODUCER_SHA256), (PRODUCER_PATH, "0" * 64)):
            try:
                validate_producer_source(path, wanted)
            except Exception:
                rejections += 1
            else:
                raise RuntimeError("fixture_producer_pin")

        artifact = directory / "artifact"
        artifact.mkdir()
        existing = directory / "existing.json"
        existing.write_bytes(b"keep")
        for output in (existing, artifact / "inside.json", ROOT / "inside.json"):
            try:
                safe_output_path(artifact, output)
            except Exception:
                rejections += 1
            else:
                raise RuntimeError("fixture_safe_output")
        if existing.read_bytes() != b"keep":
            raise RuntimeError("fixture_existing_overwritten")
        malformed_coverage = []
        for source, destination, coefficient in actual_actor[0]:
            tag, component, monomial, psl = source_tuple(destination)
            changed = (source_index(tag, component, 0, psl)
                       if monomial == 5 else destination)
            malformed_coverage.append((source, changed, coefficient))
        try:
            verify_coverage(malformed_coverage, SOURCE_WIDTH, SOURCE_WIDTH, False)
        except Exception:
            rejections += 1
        else:
            raise RuntimeError("fixture_missing_destination_case")
    if rejections != 13:
        raise RuntimeError(f"fixture_rejections:{rejections}")
    result = {
        "schema": SCHEMA + ".checker", "fixture": "PASS",
        "coefficient_2": True, "duplicate_cancellation": True,
        "nontrivial_prefix": True, "both_inverse_pairs": True,
        "monomial_mixing": True, "transpose_orientation": True,
        "truncation_rejected": True, "trailing_bytes_rejected": True,
        "producer_sha256": producer_digest,
        "fixture_rejection_count": rejections, "live_kernels_reached": sorted(live),
        "claim_flags": flags(), "ACTUAL_MAP_BUILD": "DEFERRED_TO_GHA",
        "GRADE2_DECISION": "NOT_RUN", "verified": False,
        "elapsed_seconds": time.monotonic() - started,
    }
    print(json.dumps(result, sort_keys=True), flush=True)
    return result


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true")
    modes.add_argument("--check", type=Path, metavar="DIR")
    parser.add_argument("--output", type=Path, metavar="FILE")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = cli().parse_args(argv)
    if args.selftest:
        if args.output is not None:
            cli().error("--selftest accepts no --output")
        selftest(); return 0
    try:
        result = check_artifact(args.check)
    except Exception as error:
        print(json.dumps({"schema": SCHEMA + ".checker", "terminal": "UNKNOWN_SEMANTIC", "error": str(error), "claim_flags": flags(), "verified": False}, sort_keys=True), flush=True)
        return 1
    encoded = canon(result)
    if args.output is not None:
        atomic_output(args.output, result, args.check)
    print(encoded.decode("ascii"), end="", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
