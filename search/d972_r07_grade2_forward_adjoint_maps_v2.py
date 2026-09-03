#!/usr/bin/env python3
"""Task712: streaming grade-two forward/adjoint map compiler.

This owner is deliberately result independent.  It compiles only the four
associated-grade actor maps and the six-occurrence physical aggregation map
for one source character at a time.  Sparse records are canonical JSONL
triples ``[source,destination,coefficient]``; adjoints are derived from the
same records, never implemented as a second arithmetic path.

The production ``--emit`` mode is intentionally inert with respect to the
Task565 phase runner and to every grade-two decision.  ``--selftest`` uses the
same sparse compiler, writer, parser, map application, and structural checks
on tiny live fixtures.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import tempfile
import time
from collections import deque
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972.r07.grade2.forward-adjoint-maps.v2"
TABLE_SCHEMA = SCHEMA + ".sparse-jsonl"
MARKER = "R07_GRADE2_FORWARD_ADJOINT_MAPS_V2_CANDIDATE"

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
    (0, 0): (),
    (0, 1): (-2,) * 9,
    (1, 0): (-2, -2, 1, 1, 2, 1, 2, 1, 1),
    (1, 1): (-2, -2, -2, -1, -2, -1, -1, -1, -2, -1),
}

SOURCE_WIDTH = 6 * 2 * 6 * 504
PHYSICAL_WIDTH = 4 * 2 * 2 * 6 * 504
PSL_ORDER = 504
PACKING = "jsonl-triples-utf8-lf"

# These are translation pins, not trusted executable owners.  The producer
# and checker each authenticate them locally.  The source pin for the words
# is also used to bind the exact g760 word and the relator roster.
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
MARKING_PIN = (
    "scratchpad/fuda1_a0_rmax_data.g",
    "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba",
)
WORDS_RELATOR_SHA = "7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def claim_flags() -> dict[str, bool]:
    return {
        "independent_checker": False,
        "precision2": False,
        "A0": False,
        "COMMON": False,
        "COMPATIBLE_LIFT": False,
        "FAKE": False,
        "IHARA": False,
        "verified": False,
    }


def dimensions() -> dict[str, Any]:
    return {
        "characters_count": 4,
        "source_degree2_per_character": SOURCE_WIDTH,
        "source_degree2_total": 4 * SOURCE_WIDTH,
        "physical_degree2": PHYSICAL_WIDTH,
        "source_slice": SOURCE_WIDTH,
        "physical": PHYSICAL_WIDTH,
        "source_tags": 6,
        "source_components": 2,
        "source_degree2_monomials": [list(x) for x in MONOMIALS],
        "psl_index_count": PSL_ORDER,
        "characters": [list(x) for x in CHARACTERS],
        "actors": list(ACTORS),
        "monomials_coupled": True,
    }


def source_coord(tag: int, component: int, monomial: int, psl: int) -> int:
    return (((tag * 2 + component) * 6 + monomial) * PSL_ORDER) + psl


def physical_coord(character: int, block: int, component: int, monomial: int, psl: int) -> int:
    return ((((character * 2 + block) * 2 + component) * 6 + monomial) * PSL_ORDER) + psl


def decode_source(index: int) -> tuple[int, int, int, int]:
    psl = index % PSL_ORDER
    value = index // PSL_ORDER
    monomial = value % 6
    value //= 6
    component = value % 2
    return value // 2, component, monomial, psl


def decode_physical(index: int) -> tuple[int, int, int, int, int]:
    psl = index % PSL_ORDER
    value = index // PSL_ORDER
    monomial = value % 6
    value //= 6
    component = value % 2
    value //= 2
    block = value % 2
    return value // 2, block, component, monomial, psl


# ---------------------------------------------------------------------------
# Local marked quotient arithmetic.  This is intentionally self-contained;
# no Task565 module or arithmetic helper is imported.

ID9 = tuple(range(9))
Affine = tuple[tuple[int, ...], int, int, tuple[int, int, int]]
OO: tuple[tuple[list[int], list[int]], ...] = (
    ([1], [2]), ([1], [-1, -2]), ([2], [-1, -2]),
    ([-2, -1], [1]), ([1], [2]), ([-2, -1], [2]),
)
ETA = ((0, 1), (1, 0), (1, 1))


def permutation_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(right[left[index]] for index in range(len(left)))


def permutation_inverse(value: tuple[int, ...]) -> tuple[int, ...]:
    output = [0] * len(value)
    for index, image in enumerate(value):
        output[image] = index
    return tuple(output)


def inverse_word(word: Iterable[int]) -> tuple[int, ...]:
    return tuple(-int(value) for value in reversed(tuple(word)))


def word_multiply(*parts: Iterable[int]) -> tuple[int, ...]:
    output: list[int] = []
    for part in parts:
        for raw in part:
            value = int(raw)
            if value not in (-2, -1, 1, 2):
                raise RuntimeError("word_letter")
            if output and output[-1] == -value:
                output.pop()
            else:
                output.append(value)
    return tuple(output)


def substituted_word(word: Iterable[int], x: Iterable[int], y: Iterable[int]) -> tuple[int, ...]:
    xx = tuple(x)
    yy = tuple(y)
    return word_multiply(*(
        xx if value == 1 else yy if value == 2
        else inverse_word(xx) if value == -1 else inverse_word(yy)
        for value in word
    ))


def qmul(left: tuple[tuple[int, ...], int, int], right: tuple[tuple[int, ...], int, int]) -> tuple[tuple[int, ...], int, int]:
    return (permutation_mul(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2])


def qinv(value: tuple[tuple[int, ...], int, int]) -> tuple[tuple[int, ...], int, int]:
    return (permutation_inverse(value[0]), value[1], value[2])


def qeval(word: Iterable[int], images: tuple[tuple[tuple[int, ...], int, int], tuple[tuple[int, ...], int, int]]) -> tuple[tuple[int, ...], int, int]:
    result = (ID9, 0, 0)
    for raw in word:
        letter = int(raw)
        result = qmul(result, images[abs(letter) - 1] if letter > 0 else qinv(images[abs(letter) - 1]))
    return result


def cv(label: tuple[int, int], parity: tuple[int, int]) -> int:
    return 1 if ((label[0] * parity[0] + label[1] * parity[1]) & 1) == 0 else 2


def sign_kernel(parity: tuple[int, int], vector: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((cv(ETA[index], parity) * vector[index]) % 3 for index in range(3))  # type: ignore[return-value]


def affine_mul(left: Affine, right: Affine) -> Affine:
    acted = sign_kernel((right[1], right[2]), left[3])
    return (
        permutation_mul(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2],
        tuple((acted[index] + right[3][index]) % 3 for index in range(3)),  # type: ignore[return-value]
    )


def affine_inverse(value: Affine) -> Affine:
    acted = sign_kernel((value[1], value[2]), value[3])
    return (
        permutation_inverse(value[0]), value[1], value[2],
        tuple((-entry) % 3 for entry in acted),  # type: ignore[return-value]
    )


def affine_eval(word: Iterable[int], images: tuple[Affine, Affine]) -> Affine:
    result: Affine = (ID9, 0, 0, (0, 0, 0))
    inverse = affine_inverse(images[0]), affine_inverse(images[1])
    for raw in word:
        letter = int(raw)
        result = affine_mul(result, images[abs(letter) - 1] if letter > 0 else inverse[abs(letter) - 1])
    return result


def matrix2_mul(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (left[0][0] * right[0][0] ^ left[0][1] * right[1][0], left[0][0] * right[0][1] ^ left[0][1] * right[1][1]),
        (left[1][0] * right[0][0] ^ left[1][1] * right[1][0], left[1][0] * right[0][1] ^ left[1][1] * right[1][1]),
    )


def parse_marking() -> tuple[tuple[int, ...], tuple[int, ...]]:
    path = ROOT / MARKING_PIN[0]
    data = path.read_bytes()
    if sha256_bytes(data) != MARKING_PIN[1]:
        raise RuntimeError("marking_source_pin")
    match = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;", data.decode("utf-8"), re.S)
    if match is None:
        raise RuntimeError("marking_parse")
    first = tuple(int(value) - 1 for value in ast.literal_eval(match.group(1)))
    second = tuple(int(value) - 1 for value in ast.literal_eval(match.group(2)))
    if len(first) != 36 or len(second) != 36:
        raise RuntimeError("marking_degree36")
    return first[:9], second[:9]


def build_psl(generators: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[tuple[tuple[int, ...], ...], dict[tuple[int, ...], int]]:
    steps = (generators[0], generators[1], permutation_inverse(generators[0]), permutation_inverse(generators[1]))
    elements: list[tuple[int, ...]] = [ID9]
    indices: dict[tuple[int, ...], int] = {ID9: 0}
    queue: deque[tuple[int, ...]] = deque([ID9])
    while queue:
        parent = queue.popleft()
        for step in steps:
            value = permutation_mul(parent, step)
            if value not in indices:
                indices[value] = len(elements)
                elements.append(value)
                queue.append(value)
    if len(elements) != PSL_ORDER:
        raise RuntimeError(f"psl_order:{len(elements)}")
    return tuple(elements), indices


def affine_json(value: Affine) -> dict[str, Any]:
    return {
        "psl": list(value[0]), "parity": [value[1], value[2]],
        "kernel": list(value[3]),
    }


class Context:
    """Frozen local action context reconstructed from g760 and Q0 marking."""

    def __init__(self, words: dict[str, Any]):
        first, second = parse_marking()
        self.q1_images = ((first, 1, 0), (second, 0, 1))
        self.affine_images: tuple[Affine, Affine] = (
            (first, 1, 0, (1, 0, 0)),
            (second, 0, 1, (1, 1, 1)),
        )
        self.psels, self.psl_index = build_psl((first, second))
        self.transport: list[dict[tuple[int, int], tuple[int, int]]] = []
        self.substitution_matrices: list[list[list[int]]] = []
        for left_word, right_word in OO:
            left = qeval(left_word, self.q1_images)
            right = qeval(right_word, self.q1_images)
            matrix = ((left[1], right[1]), (left[2], right[2]))
            inverse: tuple[tuple[int, int], tuple[int, int]] | None = None
            for aa in range(2):
                for ab in range(2):
                    for ba in range(2):
                        for bb in range(2):
                            candidate = ((aa, ab), (ba, bb))
                            if matrix2_mul(matrix, candidate) == ((1, 0), (0, 1)) and matrix2_mul(candidate, matrix) == ((1, 0), (0, 1)):
                                inverse = candidate
            if inverse is None:
                raise RuntimeError("occurrence_matrix")
            self.substitution_matrices.append([list(matrix[0]), list(matrix[1])])
            self.transport.append({
                label: (
                    (label[0] * inverse[0][0]) ^ (label[1] * inverse[1][0]),
                    (label[0] * inverse[0][1]) ^ (label[1] * inverse[1][1]),
                ) for label in CHARACTERS
            })
        self.actor_source_q1: dict[int, tuple[tuple[int, ...], int, int]] = {
            letter: qeval((letter,), self.q1_images) for letter in ACTORS
        }
        self.actor_tags: dict[int, tuple[Affine, ...]] = {
            letter: tuple(affine_eval(substituted_word((letter,), *pair), self.affine_images) for pair in OO)
            for letter in ACTORS
        }
        g760 = tuple(int(value) for value in words.get("g760", ()))
        if len(g760) != 760:
            raise RuntimeError("g760_length")
        self.g760 = g760
        self.g_tags = tuple(affine_eval(substituted_word(g760, *pair), self.affine_images) for pair in OO)
        identity: Affine = (ID9, 0, 0, (0, 0, 0))
        self.shifts: tuple[Affine, ...] = (
            identity,
            self.g_tags[2], self.g_tags[2],
            affine_mul(self.g_tags[5], affine_inverse(self.g_tags[4])),
            self.g_tags[5], self.g_tags[5],
        )
        self.prefix_derivation = (
            "identity", "tags(g760)[2]", "tags(g760)[2]",
            "tags(g760)[5] * tags(g760)[4]^-1", "tags(g760)[5]", "tags(g760)[5]",
        )
        self._psl_maps: dict[tuple[int, ...], tuple[int, ...]] = {}

    def psl_map(self, permutation: tuple[int, ...]) -> tuple[int, ...]:
        if permutation not in self._psl_maps:
            self._psl_maps[permutation] = tuple(
                self.psl_index[permutation_mul(permutation, value)] for value in self.psels
            )
        return self._psl_maps[permutation]

    def prefix_receipt(self) -> dict[str, Any]:
        values = [affine_json(value) for value in self.shifts]
        return {
            "derivation_order": list(self.prefix_derivation),
            "values": values,
            "sha256": sha256_bytes(canonical_json(values)),
            "nonidentity_count": sum(value != (ID9, 0, 0, (0, 0, 0)) for value in self.shifts),
        }


def authenticate_sources() -> dict[str, dict[str, Any]]:
    receipt: dict[str, dict[str, Any]] = {}
    for relative, (size, expected) in SOURCE_PINS.items():
        data = (ROOT / relative).read_bytes()
        actual = sha256_bytes(data)
        if len(data) != size or actual != expected:
            raise RuntimeError(f"source_pin:{relative}:{len(data)}:{actual}")
        receipt[relative] = {"bytes": len(data), "sha256": actual}
    marking = ROOT / MARKING_PIN[0]
    marking_data = marking.read_bytes()
    if sha256_bytes(marking_data) != MARKING_PIN[1]:
        raise RuntimeError("marking_pin")
    receipt[MARKING_PIN[0]] = {"bytes": len(marking_data), "sha256": MARKING_PIN[1]}
    return receipt


def load_words() -> tuple[dict[str, Any], dict[str, Any]]:
    path = ROOT / "scratchpad/a0_paper_words_v1.json"
    data = path.read_bytes()
    if sha256_bytes(data) != SOURCE_PINS["scratchpad/a0_paper_words_v1.json"][1]:
        raise RuntimeError("word_input_pin")
    words = json.loads(data)
    if not isinstance(words, dict) or not isinstance(words.get("relators"), list) or len(words["relators"]) != 44:
        raise RuntimeError("word_relator_roster")
    relator_digest = sha256_bytes(json.dumps(words["relators"], sort_keys=True, separators=(",", ":")).encode("ascii"))
    if words.get("relators_sha256") != WORDS_RELATOR_SHA or relator_digest != WORDS_RELATOR_SHA:
        raise RuntimeError("word_relator_digest")
    if not isinstance(words.get("g760"), list) or len(words["g760"]) != 760:
        raise RuntimeError("word_g760")
    return words, {"bytes": len(data), "sha256": sha256_bytes(data), "relators_sha256": relator_digest, "g760_length": len(words["g760"])}


# ---------------------------------------------------------------------------
# Canonical sparse table compiler and parser.


def canonical_entries(raw: Iterable[Sequence[int]], source_width: int, destination_width: int) -> tuple[list[tuple[int, int, int]], int]:
    accumulator: dict[tuple[int, int], int] = {}
    raw_count = 0
    for record in raw:
        raw_count += 1
        if len(record) != 3 or any(not plain_int(value) for value in record):
            raise RuntimeError("sparse_raw_record")
        source, destination, coefficient = (int(record[0]), int(record[1]), int(record[2]) % 3)
        if not 0 <= source < source_width or not 0 <= destination < destination_width:
            raise RuntimeError("sparse_raw_coordinate")
        key = source, destination
        accumulator[key] = (accumulator.get(key, 0) + coefficient) % 3
    entries = [(source, destination, coefficient) for (source, destination), coefficient in sorted(accumulator.items()) if coefficient]
    return entries, raw_count


def derive_adjoint(entries: Iterable[Sequence[int]], source_width: int, destination_width: int) -> list[tuple[int, int, int]]:
    return canonical_entries(((int(destination), int(source), int(coefficient)) for source, destination, coefficient in entries), destination_width, source_width)[0]


def iter_actor_raw(context: Context, character: int, actor_index: int) -> Iterator[tuple[int, int, int]]:
    label = CHARACTERS[character]
    letter = ACTORS[actor_index]
    scalar = cv(label, (context.actor_source_q1[letter][1], context.actor_source_q1[letter][2]))
    for tag, affine in enumerate(context.actor_tags[letter]):
        pmap = context.psl_map(affine[0])
        for component in range(2):
            for monomial in range(6):
                for psl in range(PSL_ORDER):
                    yield source_coord(tag, component, monomial, psl), source_coord(tag, component, monomial, pmap[psl]), scalar


def iter_aggregation_raw(context: Context, character: int) -> Iterator[tuple[int, int, int]]:
    label = CHARACTERS[character]
    # This is occurrence-first: each source coordinate is handled by its own
    # tagged occurrence before any physical row can be formed.
    for tag, block, occurrence_coefficient in OCCURRENCES:
        target_label = context.transport[tag][label]
        target_character = CHARACTERS.index(target_label)
        shift = context.shifts[tag]
        scalar = occurrence_coefficient * cv(target_label, (shift[1], shift[2]))
        pmap = context.psl_map(shift[0])
        for component in range(2):
            for monomial in range(6):
                for psl in range(PSL_ORDER):
                    yield source_coord(tag, component, monomial, psl), physical_coord(target_character, block, component, monomial, pmap[psl]), scalar


def apply_sparse(entries: Iterable[Sequence[int]], vector: Sequence[int], source_width: int, destination_width: int, *, adjoint: bool = False) -> list[int]:
    if len(vector) != (destination_width if adjoint else source_width):
        raise RuntimeError("map_apply_width")
    output = [0] * (source_width if adjoint else destination_width)
    for source, destination, coefficient in entries:
        source = int(source); destination = int(destination); coefficient = int(coefficient) % 3
        if adjoint:
            output[source] = (output[source] + coefficient * int(vector[destination])) % 3
        else:
            output[destination] = (output[destination] + coefficient * int(vector[source])) % 3
    return output


def table_line(record: Sequence[int]) -> bytes:
    return (json.dumps([int(record[0]), int(record[1]), int(record[2])], separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def atomic_bytes(path: Path, data: bytes) -> None:
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def write_table(directory: Path, filename: str, entries: Sequence[Sequence[int]], source_width: int, destination_width: int) -> dict[str, Any]:
    if list(entries) != sorted((tuple(map(int, value)) for value in entries)):
        raise RuntimeError("table_not_sorted")
    body_hash = hashlib.sha256()
    body_bytes = 0
    fd, temporary = tempfile.mkstemp(prefix=filename + ".", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "wb") as stream:
            for entry in entries:
                line = table_line(entry)
                stream.write(line)
                body_hash.update(line)
                body_bytes += len(line)
            marker = {
                "body_bytes": body_bytes, "body_sha256": body_hash.hexdigest(),
                "count": len(entries), "eof": True,
            }
            marker_bytes = canonical_json(marker)
            stream.write(marker_bytes)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, directory / filename)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    full_data = (directory / filename).read_bytes()
    return {
        "file": filename,
        "schema": TABLE_SCHEMA,
        "source_width": source_width,
        "destination_width": destination_width,
        "entry_count": len(entries),
        "body_bytes": body_bytes,
        "body_sha256": body_hash.hexdigest(),
        "bytes": len(full_data),
        "sha256": sha256_bytes(full_data),
        "eof": True,
        "encoding": PACKING,
    }


def parse_table(path: Path, receipt: dict[str, Any] | None, source_width: int, destination_width: int, expected: Sequence[Sequence[int]] | None = None) -> list[tuple[int, int, int]]:
    entries: list[tuple[int, int, int]] = []
    body_hash = hashlib.sha256()
    body_bytes = 0
    previous: tuple[int, int] | None = None
    marker: dict[str, Any] | None = None
    with path.open("rb") as stream:
        while True:
            line = stream.readline()
            if not line:
                break
            if not line.endswith(b"\n") or not line.strip():
                raise RuntimeError("table_line_termination")
            value = json.loads(line)
            if isinstance(value, dict):
                if marker is not None or set(value) != {"body_bytes", "body_sha256", "count", "eof"} or value.get("eof") is not True:
                    raise RuntimeError("table_eof_shape")
                if canonical_json(value) != line:
                    raise RuntimeError("table_eof_canonicality")
                marker = value
                break
            if not isinstance(value, list) or len(value) != 3 or any(not plain_int(item) for item in value):
                raise RuntimeError("table_record_shape")
            record = (int(value[0]), int(value[1]), int(value[2]))
            if not 0 <= record[0] < source_width or not 0 <= record[1] < destination_width or record[2] not in (1, 2):
                raise RuntimeError("table_record_semantics")
            key = record[:2]
            if previous is not None and key <= previous:
                raise RuntimeError("table_order_or_duplicate")
            previous = key
            encoded = table_line(record)
            if encoded != line:
                raise RuntimeError("table_record_canonicality")
            entries.append(record)
            body_hash.update(line)
            body_bytes += len(line)
        if marker is None or stream.read(1):
            raise RuntimeError("table_missing_or_trailing_eof")
    if not plain_int(marker.get("count")) or not plain_int(marker.get("body_bytes")) or marker.get("count") != len(entries) or marker.get("body_bytes") != body_bytes or marker.get("body_sha256") != body_hash.hexdigest():
        raise RuntimeError("table_eof_digest")
    if receipt is not None:
        required = {"file", "schema", "source_width", "destination_width", "entry_count", "body_bytes", "body_sha256", "bytes", "sha256", "eof", "encoding"}
        if set(receipt) != required or receipt.get("file") != path.name or receipt.get("schema") != TABLE_SCHEMA or receipt.get("source_width") != source_width or receipt.get("destination_width") != destination_width or receipt.get("entry_count") != len(entries) or receipt.get("body_bytes") != body_bytes or receipt.get("body_sha256") != body_hash.hexdigest() or receipt.get("bytes") != path.stat().st_size or receipt.get("sha256") != sha256_bytes(path.read_bytes()) or receipt.get("eof") is not True or receipt.get("encoding") != PACKING:
            raise RuntimeError("table_receipt")
    if expected is not None and entries != [tuple(map(int, item)) for item in expected]:
        raise RuntimeError("table_entry_mismatch")
    return entries


def verify_transpose(forward: Sequence[Sequence[int]], adjoint: Sequence[Sequence[int]]) -> int:
    expected = sorted((int(destination), int(source), int(coefficient)) for source, destination, coefficient in forward)
    actual = [tuple(map(int, item)) for item in adjoint]
    if actual != expected:
        raise RuntimeError("transpose_mismatch")
    return len(expected)


def verify_inverse(forward: Sequence[Sequence[int]], inverse: Sequence[Sequence[int]], width: int) -> int:
    left: dict[int, tuple[int, int]] = {}
    right: dict[int, tuple[int, int]] = {}
    for source, destination, coefficient in forward:
        if source in left:
            raise RuntimeError("inverse_forward_branch")
        left[int(source)] = (int(destination), int(coefficient))
    for source, destination, coefficient in inverse:
        if source in right:
            raise RuntimeError("inverse_reverse_branch")
        right[int(source)] = (int(destination), int(coefficient))
    if set(left) != set(range(width)) or set(right) != set(range(width)):
        raise RuntimeError("inverse_coordinate_coverage")
    for source in range(width):
        destination, coefficient = left[source]
        back, back_coefficient = right[destination]
        if back != source or coefficient * back_coefficient % 3 != 1:
            raise RuntimeError("inverse_identity")
    return width


def verify_coverage(entries: Sequence[Sequence[int]], source_width: int, destination_width: int, *, physical: bool) -> dict[str, Any]:
    sources = {int(value[0]) for value in entries}
    if sources != set(range(source_width)):
        raise RuntimeError("source_coordinate_coverage")
    source_cases = {decode_source(index) for index in sources}
    result: dict[str, Any] = {
        "source_coordinates": len(source_cases),
        "components": sorted({value[1] for value in source_cases}),
        "monomials": sorted({value[2] for value in source_cases}),
        "tags": sorted({value[0] for value in source_cases}),
        "psl_indices": len({value[3] for value in source_cases}),
    }
    destinations = {int(value[1]) for value in entries}
    decoded = {decode_physical(index) for index in destinations} if physical else {decode_source(index) for index in destinations}
    result["destination_coordinates"] = len(decoded)
    result["destination_components"] = sorted({value[2] for value in decoded})
    result["destination_monomials"] = sorted({value[3] for value in decoded})
    result["destination_psl_indices"] = len({value[-1] for value in decoded})
    if physical:
        result["destination_characters"] = sorted({value[0] for value in decoded})
        result["destination_blocks"] = sorted({value[1] for value in decoded})
    if result["components"] != [0, 1] or result["monomials"] != list(range(6)) or result["tags"] != list(range(6)) or result["psl_indices"] != PSL_ORDER or result["destination_components"] != [0, 1] or result["destination_monomials"] != list(range(6)) or result["destination_psl_indices"] != PSL_ORDER:
        raise RuntimeError("coordinate_case_coverage")
    if physical and result["destination_blocks"] != [0, 1]:
        raise RuntimeError("physical_case_coverage")
    return result


def rss_bytes() -> int:
    try:
        import psutil  # type: ignore[import-not-found]
        return int(psutil.Process(os.getpid()).memory_info().rss)
    except Exception:
        return 0


def progress(phase: str, **values: Any) -> None:
    record = {"progress": phase, **values}
    print(json.dumps(record, sort_keys=True), flush=True)


def compile_table_pair(context: Context, directory: Path, kind: str, character: int, actor_index: int | None = None) -> tuple[dict[str, Any], dict[str, Any], list[tuple[int, int, int]]]:
    if kind == "T":
        if actor_index is None:
            raise RuntimeError("actor_required")
        forward, raw_count = canonical_entries(iter_actor_raw(context, character, actor_index), SOURCE_WIDTH, SOURCE_WIDTH)
        stem = f"T_fwd_a{character}_t{actor_index}"
        adjoint = derive_adjoint(forward, SOURCE_WIDTH, SOURCE_WIDTH)
        adj_stem = f"T_adj_a{character}_t{actor_index}"
        source_width = destination_width = SOURCE_WIDTH
    elif kind == "B":
        forward, raw_count = canonical_entries(iter_aggregation_raw(context, character), SOURCE_WIDTH, PHYSICAL_WIDTH)
        stem = f"B_fwd_a{character}"
        adjoint = derive_adjoint(forward, SOURCE_WIDTH, PHYSICAL_WIDTH)
        adj_stem = f"B_adj_a{character}"
        source_width, destination_width = SOURCE_WIDTH, PHYSICAL_WIDTH
    else:
        raise RuntimeError("map_kind")
    forward_receipt = write_table(directory, stem + ".jsonl", forward, source_width, destination_width)
    adjoint_receipt = write_table(directory, adj_stem + ".jsonl", adjoint, destination_width, source_width)
    verify_transpose(forward, adjoint)
    progress("map", kind=kind, character=character, actor=(ACTORS[actor_index] if actor_index is not None else None), rows_emitted=len(forward) + len(adjoint), raw_entries=raw_count)
    return forward_receipt, adjoint_receipt, forward


def structural_identities(context: Context, tables: list[dict[str, Any]], forward_entries: dict[str, list[tuple[int, int, int]]]) -> dict[str, Any]:
    for character in range(4):
        for first, second in ((0, 1), (2, 3)):
            verify_inverse(forward_entries[f"T_fwd_a{character}_t{first}"], forward_entries[f"T_fwd_a{character}_t{second}"], SOURCE_WIDTH)
    # Every table's adjoint was compared entry by entry while it was written;
    # repeat the complete count here so the receipt cannot be canary-only.
    transpose_entries = sum(1 for table in tables if table["map_direction"] == "adjoint")
    t_forward = [table for table in tables if table["map_kind"] == "T" and table["map_direction"] == "forward"]
    b_forward = [table for table in tables if table["map_kind"] == "B" and table["map_direction"] == "forward"]
    coverage_t = verify_coverage(forward_entries["T_fwd_a0_t0"], SOURCE_WIDTH, SOURCE_WIDTH, physical=False)
    coverage_b = verify_coverage(forward_entries["B_fwd_a0"], SOURCE_WIDTH, PHYSICAL_WIDTH, physical=True)
    all_b_characters = sorted({decode_physical(int(item[1]))[0] for name, entries in forward_entries.items() if name.startswith("B_fwd_") for item in entries})
    if all_b_characters != list(range(4)):
        raise RuntimeError("physical_character_case_coverage")
    coefficient_values = {int(value[2]) for entries in forward_entries.values() for value in entries}
    return {
        "canonical_entry_legal": True,
        "transpose_entrywise": transpose_entries == 20,
        "transpose_entries_checked": sum(table["entry_count"] for table in tables if table["map_direction"] == "adjoint"),
        "actor_inverse_entrywise": True,
        "inverse_source_coordinates_checked": 8 * SOURCE_WIDTH,
        "all_sign_cases_visited": coefficient_values == {1, 2},
        "coefficient_values": sorted(coefficient_values),
        "all_prefix_cases_visited": context.prefix_receipt()["nonidentity_count"] > 0,
        "all_component_cases_visited": coverage_t["components"] == [0, 1] and coverage_b["components"] == [0, 1],
        "all_monomial_cases_visited": coverage_t["monomials"] == list(range(6)) and coverage_b["monomials"] == list(range(6)),
        "all_psl_index_cases_visited": coverage_t["psl_indices"] == PSL_ORDER and coverage_b["psl_indices"] == PSL_ORDER,
        "T_forward_table_count": len(t_forward),
        "B_forward_table_count": len(b_forward),
        "T_coverage": coverage_t,
        "B_coverage": coverage_b,
        "B_all_character_cases_visited": True,
        "B_occurrence_first": True,
        "B_occurrence_records_before_aggregation": 6 * 2 * 6 * PSL_ORDER,
        "physical_row_action": False,
        "monomials_split": False,
        "sampled_dot_products_are_canaries_only": True,
    }


def make_manifest(directory: Path, context: Context, source_receipt: dict[str, dict[str, Any]], word_receipt: dict[str, Any], tables: list[dict[str, Any]], structural: dict[str, Any], started: float, peak_rss: int) -> dict[str, Any]:
    prefix = context.prefix_receipt()
    table_roster = [table["file"] for table in tables]
    roster = ["manifest.json", "producer.marker"] + table_roster
    for table in tables:
        table.setdefault("map_kind", "T" if table["file"].startswith("T_") else "B")
        table.setdefault("map_direction", "adjoint" if "_adj_" in table["file"] else "forward")
    return {
        "schema": SCHEMA,
        "marker": MARKER,
        "fixture": False,
        "dimensions": dimensions(),
        "coordinate_order": {
            "characters": [list(x) for x in CHARACTERS],
            "actors": list(ACTORS),
            "source": ["tag", "component", "monomial", "psl_index"],
            "physical": ["character", "physical_block", "component", "monomial", "psl_index"],
            "degree2_monomials": [list(x) for x in MONOMIALS],
        },
        "occurrence_triples": [list(x) for x in OCCURRENCES],
        "prefix_shifts": prefix,
        "source_pins": source_receipt,
        "word_input": word_receipt,
        "marking_input": source_receipt[MARKING_PIN[0]],
        "producer_sha256": sha256_bytes(Path(__file__).resolve().read_bytes()),
        "tables": tables,
        "table_roster": table_roster,
        "output_roster": roster,
        "structural_identities": structural,
        "rows_emitted": sum(table["entry_count"] for table in tables),
        "map_count": 20,
        "table_count": len(tables),
        "elapsed_seconds": time.monotonic() - started,
        "peak_rss_bytes": peak_rss,
        "claim_flags": claim_flags(),
        "terminal": MARKER,
        "ACTUAL_MAP_BUILD": "DEFERRED_TO_GHA",
        "GRADE2_DECISION": "NOT_RUN",
        "verified": False,
    }


def emit(directory: Path) -> None:
    started = time.monotonic()
    source_receipt = authenticate_sources()
    words, word_receipt = load_words()
    context = Context(words)
    directory = directory.resolve()
    if directory == ROOT or ROOT in directory.parents:
        raise RuntimeError("emit_directory_must_be_external")
    if directory.exists():
        raise RuntimeError("emit_directory_must_not_exist")
    directory.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=directory.name + ".", dir=directory.parent))
    peak = rss_bytes()
    tables: list[dict[str, Any]] = []
    forward_entries: dict[str, list[tuple[int, int, int]]] = {}
    try:
        for character in range(4):
            progress("character", character=character, actors=list(ACTORS), rows_emitted=0)
            for actor_index in range(4):
                forward_receipt, adjoint_receipt, forward = compile_table_pair(context, temporary, "T", character, actor_index)
                forward_receipt.update({"map_kind": "T", "map_direction": "forward", "character": character, "actor": ACTORS[actor_index]})
                adjoint_receipt.update({"map_kind": "T", "map_direction": "adjoint", "character": character, "actor": ACTORS[actor_index]})
                tables.extend((forward_receipt, adjoint_receipt))
                forward_entries[f"T_fwd_a{character}_t{actor_index}"] = forward
                peak = max(peak, rss_bytes())
            forward_receipt, adjoint_receipt, forward = compile_table_pair(context, temporary, "B", character)
            forward_receipt.update({"map_kind": "B", "map_direction": "forward", "character": character})
            adjoint_receipt.update({"map_kind": "B", "map_direction": "adjoint", "character": character})
            tables.extend((forward_receipt, adjoint_receipt))
            forward_entries[f"B_fwd_a{character}"] = forward
            peak = max(peak, rss_bytes())
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    try:
        structural = structural_identities(context, tables, forward_entries)
        marker_path = temporary / "producer.marker"
        atomic_bytes(marker_path, (MARKER + "\n").encode("ascii"))
        manifest = make_manifest(temporary, context, source_receipt, word_receipt, tables, structural, started, peak)
        atomic_bytes(temporary / "manifest.json", canonical_json(manifest))
        os.replace(temporary, directory)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    print(json.dumps({"schema": SCHEMA, "terminal": MARKER, "directory": str(directory), "tables": len(tables), "rows_emitted": manifest["rows_emitted"], "elapsed_seconds": manifest["elapsed_seconds"], "peak_rss_bytes": peak}, sort_keys=True), flush=True)


# ---------------------------------------------------------------------------
# Bounded live fixtures.  The tiny maps deliberately include a coefficient-2
# edge and a monomial-changing edge; neither is substituted for the actual
# six-monomial owner.


def selftest() -> dict[str, Any]:
    started = time.monotonic()
    authenticate_sources()
    words, _ = load_words()
    context = Context(words)
    prefix = context.prefix_receipt()
    if prefix["nonidentity_count"] <= 0:
        raise RuntimeError("fixture_nontrivial_prefix")
    # Exercise the actual one-character actor compiler for both registered
    # inverse pairs, then apply each composition to a full-width vector.
    actual_actor = {
        actor_index: canonical_entries(
            iter_actor_raw(context, 0, actor_index), SOURCE_WIDTH, SOURCE_WIDTH)[0]
        for actor_index in range(4)
    }
    verify_inverse(actual_actor[0], actual_actor[1], SOURCE_WIDTH)
    verify_inverse(actual_actor[2], actual_actor[3], SOURCE_WIDTH)
    actor_probe = [index % 3 for index in range(SOURCE_WIDTH)]
    if apply_sparse(actual_actor[1], apply_sparse(actual_actor[0], actor_probe,
                    SOURCE_WIDTH, SOURCE_WIDTH), SOURCE_WIDTH, SOURCE_WIDTH) != actor_probe:
        raise RuntimeError("fixture_actual_x_inverse_application")
    if apply_sparse(actual_actor[3], apply_sparse(actual_actor[2], actor_probe,
                    SOURCE_WIDTH, SOURCE_WIDTH), SOURCE_WIDTH, SOURCE_WIDTH) != actor_probe:
        raise RuntimeError("fixture_actual_y_inverse_application")
    actual_b, _ = canonical_entries(
        iter_aggregation_raw(context, 0), SOURCE_WIDTH, PHYSICAL_WIDTH)
    nonidentity_tag = next(index for index, value in enumerate(context.shifts)
                           if value != (ID9, 0, 0, (0, 0, 0)))
    prefix_source = source_coord(nonidentity_tag, 0, 0, 0)
    prefix_probe = [0] * SOURCE_WIDTH
    prefix_probe[prefix_source] = 1
    if not any(apply_sparse(actual_b, prefix_probe, SOURCE_WIDTH, PHYSICAL_WIDTH)):
        raise RuntimeError("fixture_actual_prefix_application")
    cancelled, raw_count = canonical_entries(((0, 1, 1), (0, 1, 2)), 12, 12)
    if raw_count != 2 or cancelled:
        raise RuntimeError("fixture_duplicate_cancellation")
    tiny_forward_raw = [
        (0, 1, 2), (1, 2, 2), (2, 0, 1),
        (3, 4, 1), (4, 5, 2), (5, 3, 1),
        (6, 7, 1), (7, 8, 2), (8, 6, 1),
        (9, 10, 2), (10, 11, 1), (11, 9, 2),
    ]
    tiny_forward, _ = canonical_entries(tiny_forward_raw, 12, 12)
    tiny_adjoint = derive_adjoint(tiny_forward, 12, 12)
    tiny_forward2, _ = canonical_entries(
        tuple((index, (index + 2) % 12, 1 if index % 2 else 2) for index in range(12)),
        12, 12,
    )
    tiny_adjoint2 = derive_adjoint(tiny_forward2, 12, 12)
    rejections = 0
    reached = {
        "canonical_entries", "derive_adjoint", "write_table", "parse_table",
        "apply_sparse", "verify_inverse", "verify_transpose",
        "iter_actor_raw", "iter_aggregation_raw",
    }
    with tempfile.TemporaryDirectory(prefix="task712-producer-fixture-") as name:
        directory = Path(name)
        actual_b_receipt = write_table(directory, "actual_b_prefix.jsonl", actual_b,
                                       SOURCE_WIDTH, PHYSICAL_WIDTH)
        parse_table(directory / actual_b_receipt["file"], actual_b_receipt,
                    SOURCE_WIDTH, PHYSICAL_WIDTH, actual_b)
        fwd = write_table(directory, "tiny_fwd.jsonl", tiny_forward, 12, 12)
        adj = write_table(directory, "tiny_adj.jsonl", tiny_adjoint, 12, 12)
        fwd2 = write_table(directory, "tiny_fwd_pair2.jsonl", tiny_forward2, 12, 12)
        adj2 = write_table(directory, "tiny_adj_pair2.jsonl", tiny_adjoint2, 12, 12)
        parsed_fwd = parse_table(directory / fwd["file"], fwd, 12, 12, tiny_forward)
        parsed_adj = parse_table(directory / adj["file"], adj, 12, 12, tiny_adjoint)
        parsed_fwd2 = parse_table(directory / fwd2["file"], fwd2, 12, 12, tiny_forward2)
        parsed_adj2 = parse_table(directory / adj2["file"], adj2, 12, 12, tiny_adjoint2)
        verify_transpose(parsed_fwd, parsed_adj)
        verify_inverse(parsed_fwd, parsed_adj, 12)
        verify_transpose(parsed_fwd2, parsed_adj2)
        verify_inverse(parsed_fwd2, parsed_adj2, 12)
        for basis in range(12):
            vector = [0] * 12
            vector[basis] = 1
            after = apply_sparse(parsed_fwd, vector, 12, 12)
            back = apply_sparse(parsed_adj, after, 12, 12)
            if back != vector:
                raise RuntimeError("fixture_inverse_application")
        # Source index 0 -> destination 1 changes the tiny monomial slot.
        if tiny_forward[0][0] % 6 == tiny_forward[0][1] % 6:
            raise RuntimeError("fixture_monomial_mixing")
        original = (directory / fwd["file"]).read_bytes()
        (directory / fwd["file"]).write_bytes(original[:-1])
        try:
            parse_table(directory / fwd["file"], None, 12, 12)
        except Exception:
            rejections += 1
        else:
            raise RuntimeError("fixture_truncation_accepted")
        (directory / fwd["file"]).write_bytes(original + b"\n")
        try:
            parse_table(directory / fwd["file"], None, 12, 12)
        except Exception:
            rejections += 1
        else:
            raise RuntimeError("fixture_trailing_accepted")
    if rejections != 2:
        raise RuntimeError(f"fixture_rejection_count:{rejections}")
    result = {
        "schema": SCHEMA,
        "fixture": "PASS",
        "coefficient_2": True,
        "duplicate_cancellation": True,
        "nontrivial_prefix": True,
        "both_inverse_pairs": True,
        "monomial_mixing": True,
        "transpose_orientation": True,
        "truncation_rejected": True,
        "trailing_bytes_rejected": True,
        "fixture_rejection_count": rejections,
        "live_kernels_reached": sorted(reached),
        "claim_flags": claim_flags(),
        "ACTUAL_MAP_BUILD": "DEFERRED_TO_GHA",
        "GRADE2_DECISION": "NOT_RUN",
        "verified": False,
        "elapsed_seconds": time.monotonic() - started,
    }
    print(json.dumps(result, sort_keys=True), flush=True)
    return result


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    modes = result.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true")
    modes.add_argument("--emit", type=Path, metavar="DIR")
    return result


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    if arguments.selftest:
        selftest()
    elif arguments.emit is not None:
        emit(arguments.emit)
    else:
        raise RuntimeError("fail_closed_cli")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
