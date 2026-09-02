#!/usr/bin/env python3
"""Independent checker for the Task559 v3 first-grade state/certificate chain."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import tempfile
from collections import deque
from pathlib import Path
from typing import Any, Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972.r07.a0.first-rung-grade1.v3"
STATE_SCHEMA = SCHEMA + ".state"
CHARS = ((0, 0), (0, 1), (1, 0), (1, 1))
MONS1 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ETA = ((0, 1), (1, 0), (1, 1))
OCC = (([1], [2]), ([1], [-1, -2]), ([2], [-1, -2]), ([-2, -1], [1]), ([1], [2]), ([-2, -1], [2]))
ACTORS = (1, -1, 2, -2)
PURE = {
    (0, 0): (),
    (0, 1): (-2, -2, -2, -2, -2, -2, -2, -2, -2),
    (1, 0): (-2, -2, 1, 1, 2, 1, 2, 1, 1),
    (1, 1): (-2, -2, -2, -1, -2, -1, -1, -1, -2, -1),
}
SOURCE_WIDTH = 18144
PHYSICAL_WIDTH = 24192
INPUT_PINS = {
    "sol/proof_r07_a0_relative_fibre_echelon_lift_v441.md": "5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb",
    "sol/sol_reply_544_audit_r07_a0_relative_fibre_echelon_v1.md": "7875fa2641355c8d6d09248b23c9fa9c766f48db751d34b90826ab609b457eb3",
    "sol/proof_r07_a0_explicit_g9_two_rung_twisting_v442.md": "afa91b6137f8321522cf97fa11502213bde45c7c4c325b3b2ad28e8f6e844de4",
    "sol/sol_reply_548_audit_r07_a0_explicit_g9_two_rung_twisting_v1.md": "bd1b0239e0410f2ab63abd30e7ff9a422528d141138cfeafc8ca3960da1cd834",
    "sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md": "80970217b415d7b764e399b5ce5892075b1f82f7f87f0c6199e9f6b0e404f24c",
    "sol/proof_r07_filtered_transition_defect_closure_v444.md": "705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645",
    "sol/sol_reply_550_audit_r07_a0_affine_engine_transition_defects_v1.md": "329aa9b8c8b87e5672938cb70ab99dbf365b59a0e63468a3df58420ee26e4616",
    "sol/proof_r07_first_rung_character_blocks_coupled_monomials_v446.md": "389ceee1250b892ec4845753af23f4455e619e2d72782931645d8b8176764756",
    "sol/sol_reply_553_audit_r07_a0_character_blocks_coupled_monomials_v1.md": "9e06ae4022e6267846561b13fed2f64a73909ba0d3b68436173763cf6bdba1df",
    "sol/sol_reply_549_audit_r07_a0_order2016_literal_member_v1.md": "a088d27203e2064ac8240b813fd15e905ec82633b93b829e89b4a073f111256c",
    "sol/sol_reply_547_audit_r07_a0_psl504_canonical_payload_v1.md": "84029c2f64ac8a20f83d9680e2b105f6994db140c4062d8e5c8f99228f7ab32f",
    "search/certs/d972_r07_a0_c2fourier_joint_floor_v1.json": "e55b7dfa5a0876054b05259f115266c0b2651431f1f2670efe85e9b34c94222b",
    "search/d972_r07_a0_c2fourier_joint_floor_v1.py": "6201ae0b5c1d648529ac648a574c5096b8088fe341423724556860d9d3f23fba",
    "scratchpad/a0_paper_words_v1.json": "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893",
    "scratchpad/fuda1_a0_rmax_data.g": "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba",
    "sol/proof_r07_first_rung_character_projector_word_repair_v447.md": "3e4bb3e498beb2c44cf3e1f0786ad83c7691312674967877b766e3e61bb496c2",
    "sol/proof_r07_first_rung_six_grade_index_repair_v449.md": "0237572f8ee949cdac8129cb9a9dae8c833b00baee2647c0deed194449577ff9",
    "sol/sol_reply_555_audit_r07_a0_six_grade_schedule_v1.md": "8dcdfbb4825c65bff9698311b735e830c27d39f98405bcfb01af3411d97a2e45",
}
PRODUCER_SHA256 = "bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canon(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def insist(condition: bool, gate: str) -> None:
    if not condition:
        raise RuntimeError(gate)


def pins() -> dict[str, dict[str, Any]]:
    answer = {}
    for name, expected in INPUT_PINS.items():
        data = (ROOT / name).read_bytes()
        insist(digest(data) == expected, "input_pin:" + name)
        answer[name] = {"bytes": len(data), "sha256": expected}
    insist("FIRST_RUNG_CHARACTER_BLOCKS_PASS_AFTER_REPAIR" in (ROOT / "sol/sol_reply_553_audit_r07_a0_character_blocks_coupled_monomials_v1.md").read_text(encoding="utf-8"), "task553_gate")
    producer = ROOT / "search/d972_r07_a0_first_rung_grade1_v3.py"
    insist(PRODUCER_SHA256 != "TO_BE_PINNED" and digest(producer.read_bytes()) == PRODUCER_SHA256, "producer_pin")
    return answer


def reduce_free(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for raw in word:
        letter = int(raw)
        insist(letter in (-2, -1, 1, 2), "literal_letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def canonical_terms(terms: Any) -> list[list[Any]]:
    insist(isinstance(terms, list), "literal_list")
    values: dict[tuple[int, tuple[int, ...]], int] = {}
    for term in terms:
        insist(isinstance(term, list) and len(term) == 3, "literal_shape")
        seed, word, coefficient = int(term[0]), term[1], int(term[2])
        insist(1 <= seed <= 44 and isinstance(word, list) and coefficient in (1, 2), "literal_type")
        key = seed, reduce_free(word)
        values[key] = (values.get(key, 0) + coefficient) % 3
    return [[seed, list(word), coefficient] for (seed, word), coefficient in sorted(values.items()) if coefficient]


DECODE = np.asarray([[(value // (3**position)) % 3 for position in range(4)] for value in range(81)], dtype=np.uint8)
WEIGHTS = np.asarray((1, 3, 9, 27), dtype=np.uint16)


def unpack(data: bytes, width: int, rows: int) -> np.ndarray:
    raw = np.frombuffer(data, dtype=np.uint8)
    insist(width % 4 == 0 and raw.size == rows * (width // 4) and not np.any(raw > 80), "packed_shape")
    return DECODE[raw].reshape(rows, width).copy()


_CHECKED_BLOBS: set[tuple[str, int, str, int, int]] = set()


def checked_blob_path(directory: Path, receipt: dict[str, Any], width: int, rows: int) -> Path:
    """Validate a blob without retaining it; large packet rows stay mmap-backed."""
    insist(
        isinstance(receipt, dict)
        and set(receipt) == {"file", "bytes", "sha256", "rows", "width", "encoding"}
        and plain_int(width)
        and width > 0
        and width % 4 == 0
        and plain_int(rows)
        and rows >= 0,
        "blob_receipt_shape",
    )
    name = receipt.get("file")
    expected_bytes = rows * (width // 4)
    insist(
        isinstance(name, str)
        and Path(name).name == name
        and re.fullmatch(r"[A-Za-z0-9_.-]+\.[0-9a-f]{64}\.bin", name) is not None
        and isinstance(receipt.get("sha256"), str)
        and re.fullmatch(r"[0-9a-f]{64}", receipt["sha256"]) is not None
        and name.endswith(f".{receipt['sha256']}.bin")
        and receipt.get("rows") == rows
        and receipt.get("width") == width
        and receipt.get("encoding") == "base3-four-trits-per-byte"
        and receipt.get("bytes") == expected_bytes,
        "blob_receipt_semantics",
    )
    path = directory / name
    stat_before = path.stat()
    insist(stat_before.st_size == expected_bytes, "blob_size")
    key = (str(path.resolve()), expected_bytes, receipt["sha256"], stat_before.st_mtime_ns, stat_before.st_ino)
    if key in _CHECKED_BLOBS:
        return path
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
            insist(not chunk or int(np.frombuffer(chunk, dtype=np.uint8).max()) <= 80, "packed_byte")
    insist(hasher.hexdigest() == receipt.get("sha256"), "blob_digest")
    stat_after = path.stat()
    insist(
        stat_after.st_size == stat_before.st_size
        and stat_after.st_mtime_ns == stat_before.st_mtime_ns
        and stat_after.st_ino == stat_before.st_ino,
        "blob_changed_during_check",
    )
    _CHECKED_BLOBS.add(key)
    return path


def read_blob(directory: Path, receipt: dict[str, Any]) -> bytes:
    width, rows = receipt.get("width"), receipt.get("rows")
    insist(plain_int(width) and plain_int(rows), "blob_dimensions")
    path = checked_blob_path(directory, receipt, width, rows)
    data = path.read_bytes()
    insist(len(data) == receipt["bytes"], "blob_size_after_check")
    return data


def packed_map(directory: Path, receipt: dict[str, Any], width: int, rows: int) -> np.ndarray:
    insist(
        receipt.get("width") == width
        and receipt.get("rows") == rows
        and receipt.get("encoding") == "base3-four-trits-per-byte"
        and width % 4 == 0
        and receipt.get("bytes") == rows * (width // 4),
        "packed_receipt",
    )
    path = checked_blob_path(directory, receipt, width, rows)
    if rows == 0:
        return np.empty((0, width // 4), dtype=np.uint8)
    answer = np.memmap(path, mode="r", dtype=np.uint8, shape=(rows, width // 4))
    return answer


def pack(row: np.ndarray) -> np.ndarray:
    flat = np.asarray(row, dtype=np.uint8).reshape(-1)
    insist(flat.size % 4 == 0 and not np.any(flat > 2), "pack_shape")
    return np.sum(flat.reshape(-1, 4).astype(np.uint16) * WEIGHTS, axis=1).astype(np.uint8)


def read_state(directory: Path, stem: str, parent: str | None = None) -> tuple[dict[str, Any], str]:
    head_data = (directory / (stem + ".HEAD")).read_bytes()
    head = json.loads(head_data)
    insist(set(head) == {"schema", "stem", "body_sha256", "parent_sha256"}, "head_shape")
    insist(
        canon(head) == head_data
        and head["schema"] == STATE_SCHEMA + ".head"
        and head["stem"] == stem
        and isinstance(head["body_sha256"], str)
        and re.fullmatch(r"[0-9a-f]{64}", head["body_sha256"]) is not None,
        "head_semantics",
    )
    insist(head["parent_sha256"] == parent, "head_parent")
    body_data = (directory / f"{stem}.{head['body_sha256']}.json").read_bytes()
    insist(digest(body_data) == head["body_sha256"], "body_digest")
    body = json.loads(body_data)
    insist(body.get("schema") == STATE_SCHEMA and canon(body) == body_data, "body_canonical")
    return body, head["body_sha256"]


def mul_perm(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(right[left[i]] for i in range(len(left)))


def inv_perm(value: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(value)
    for i, j in enumerate(value):
        out[j] = i
    return tuple(out)


def inverse_word(word: Iterable[int]) -> list[int]:
    return [-x for x in reversed(list(word))]


def reduced_product(*parts: Iterable[int]) -> list[int]:
    out: list[int] = []
    for part in parts:
        for x in part:
            if out and out[-1] == -x:
                out.pop()
            else:
                out.append(int(x))
    return out


def substitute(word: Iterable[int], xword: list[int], yword: list[int]) -> list[int]:
    choices = {1: xword, 2: yword, -1: inverse_word(xword), -2: inverse_word(yword)}
    return reduced_product(*(choices[int(x)] for x in word))


Aff = tuple[tuple[int, ...], int, int, tuple[int, int, int]]
ID9 = tuple(range(9))


def character(label: tuple[int, int], a: int, b: int) -> int:
    return 1 if ((label[0] * a + label[1] * b) & 1) == 0 else 2


def signed(parity: tuple[int, int], vector: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(character(ETA[i], parity[0], parity[1]) * vector[i] % 3 for i in range(3))  # type: ignore[return-value]


def product(left: Aff, right: Aff) -> Aff:
    first = signed((right[1], right[2]), left[3])
    return mul_perm(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2], tuple((first[i] + right[3][i]) % 3 for i in range(3))  # type: ignore[return-value]


def inverse(value: Aff) -> Aff:
    vector = signed((value[1], value[2]), value[3])
    return inv_perm(value[0]), value[1], value[2], tuple(-x % 3 for x in vector)  # type: ignore[return-value]


def value_of(word: Iterable[int], images: tuple[Aff, Aff]) -> Aff:
    out: Aff = (ID9, 0, 0, (0, 0, 0))
    inverses = inverse(images[0]), inverse(images[1])
    for x in word:
        out = product(out, images[abs(int(x)) - 1] if x > 0 else inverses[abs(int(x)) - 1])
    return out


def enumerate_psl(a: tuple[int, ...], c: tuple[int, ...]) -> tuple[list[tuple[int, ...]], dict[tuple[int, ...], int]]:
    steps = (a, c, inv_perm(a), inv_perm(c))
    elements = [ID9]
    index = {ID9: 0}
    queue = deque([ID9])
    while queue:
        current = queue.popleft()
        for step in steps:
            nxt = mul_perm(current, step)
            if nxt not in index:
                index[nxt] = len(elements)
                elements.append(nxt)
                queue.append(nxt)
    insist(len(elements) == 504, "psl_order")
    return elements, index


class IndependentContext:
    def __init__(self):
        text = (ROOT / "scratchpad/fuda1_a0_rmax_data.g").read_text(encoding="utf-8")
        match = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;", text, re.S)
        insist(match is not None, "marking_parse")
        q36 = [tuple(x - 1 for x in ast.literal_eval(match.group(i))) for i in (1, 2)]
        self.a, self.c = q36[0][:9], q36[1][:9]
        self.elements, self.index = enumerate_psl(self.a, self.c)
        self.images: tuple[Aff, Aff] = ((self.a, 1, 0, (1, 0, 0)), (self.c, 0, 1, (1, 1, 1)))
        self.pb = inverse(product(self.images[1], self.images[0]))
        self.words = json.loads((ROOT / "scratchpad/a0_paper_words_v1.json").read_text(encoding="utf-8"))
        gvalues = tuple(value_of(substitute(self.words["g760"], *pair), self.images) for pair in OCC)
        self.shifts = ((ID9, 0, 0, (0, 0, 0)), gvalues[2], gvalues[2], product(gvalues[5], inverse(gvalues[4])), gvalues[5], gvalues[5])
        self.aggregation = ((0, 0, 1), (1, 0, 2), (2, 0, 1), (3, 1, 2), (4, 1, 2), (5, 1, 1))
        self.actor_tags = {letter: tuple(value_of(substitute((letter,), *pair), self.images) for pair in OCC) for letter in ACTORS}
        self.actor_source = {letter: value_of((letter,), self.images) for letter in ACTORS}
        self.pure_source: dict[tuple[int, int], Aff] = {}
        self.pure_tags: dict[tuple[int, int], tuple[Aff, ...]] = {}
        for parity, word in PURE.items():
            endpoint = value_of(word, self.images)
            insist(endpoint[0] == ID9 and endpoint[1:3] == parity, "pure_word")
            self.pure_source[parity] = endpoint
            self.pure_tags[parity] = tuple(value_of(substitute(word, *pair), self.images) for pair in OCC)
        self.transports: list[dict[tuple[int, int], tuple[int, int]]] = []
        self.inverse_transports: list[dict[tuple[int, int], tuple[int, int]]] = []
        for pair in OCC:
            left, right = value_of(pair[0], self.images), value_of(pair[1], self.images)
            matrix = ((left[1], right[1]), (left[2], right[2]))
            candidates = [
                ((aa, ab), (ba, bb))
                for aa in range(2)
                for ab in range(2)
                for ba in range(2)
                for bb in range(2)
            ]

            def mm(x: Any, y: Any) -> Any:
                return (
                    (
                        x[0][0] * y[0][0] ^ x[0][1] * y[1][0],
                        x[0][0] * y[0][1] ^ x[0][1] * y[1][1],
                    ),
                    (
                        x[1][0] * y[0][0] ^ x[1][1] * y[1][0],
                        x[1][0] * y[0][1] ^ x[1][1] * y[1][1],
                    ),
                )

            inverse_matrix = next(
                candidate
                for candidate in candidates
                if mm(matrix, candidate) == ((1, 0), (0, 1))
                and mm(candidate, matrix) == ((1, 0), (0, 1))
            )
            transport = {
                label: (
                    label[0] * inverse_matrix[0][0] ^ label[1] * inverse_matrix[1][0],
                    label[0] * inverse_matrix[0][1] ^ label[1] * inverse_matrix[1][1],
                )
                for label in CHARS
            }
            self.transports.append(transport)
            self.inverse_transports.append({target: source for source, target in transport.items()})
        self.left_maps: dict[tuple[int, ...], np.ndarray] = {}

    def left_map(self, permutation: tuple[int, ...]) -> np.ndarray:
        if permutation not in self.left_maps:
            self.left_maps[permutation] = np.asarray(
                [self.index[mul_perm(permutation, value)] for value in self.elements], dtype=np.int32
            )
        return self.left_maps[permutation]


def fox(word: Iterable[int], images: tuple[Aff, Aff]) -> tuple[dict[tuple[int, Aff], int], Aff]:
    row: dict[tuple[int, Aff], int] = {}
    point: Aff = (ID9, 0, 0, (0, 0, 0))
    inverses = inverse(images[0]), inverse(images[1])
    for letter in word:
        generator = abs(int(letter)) - 1
        if letter > 0:
            key = generator, point
            row[key] = (row.get(key, 0) + 1) % 3
            point = product(point, images[generator])
        else:
            point = product(point, inverses[generator])
            key = generator, point
            row[key] = (row.get(key, 0) - 1) % 3
        if row.get(key) == 0:
            row.pop(key, None)
    return row, point


def normal(word: Iterable[int], context: IndependentContext) -> tuple[list[tuple[int, Aff, int]], int]:
    gradient, endpoint = fox(word, context.images)
    insist(endpoint == (ID9, 0, 0, (0, 0, 0)), "identity_endpoint")
    row: dict[tuple[int, Aff], int] = {}
    augmentation = 0
    for (generator, prefix), coefficient in gradient.items():
        if generator == 0:
            augmentation = (augmentation + coefficient) % 3
            one = product(prefix, context.images[0])
            two = product(one, context.pb)
            for component, value in ((0, one), (1, two)):
                row[component, value] = (row.get((component, value), 0) - coefficient) % 3
        else:
            row[1, prefix] = (row.get((1, prefix), 0) + coefficient) % 3
    return [(component, value, coefficient) for (component, value), coefficient in row.items() if coefficient], augmentation


def sparse_add(row: dict[int, int], coordinate: int, value: int) -> None:
    coefficient = (row.get(coordinate, 0) + value) % 3
    if coefficient:
        row[coordinate] = coefficient
    else:
        row.pop(coordinate, None)


def pcoord(character_index: int, block: int, component: int, monomial: int, psl: int) -> int:
    return (((character_index * 2 + block) * 2 + component) * 4 + monomial) * 504 + psl


def raw_seed(word: list[int], context: IndependentContext) -> tuple[list[list[tuple[int, Aff, int]]], list[int], tuple[int, int]]:
    rows, augmentations = [], []
    for pair in OCC:
        value, aug = normal(substitute(word, *pair), context)
        rows.append(value)
        augmentations.append(aug)
    ex = (sum(x == 1 for x in word) - sum(x == -1 for x in word), sum(x == 2 for x in word) - sum(x == -2 for x in word))
    insist(ex[0] % 18 == 0 and ex[1] % 18 == 0, "normalized_integrality")
    return rows, augmentations, (ex[0] // 18 % 3, ex[1] // 18 % 3)


def add_mod3(destination: np.ndarray, source: np.ndarray, coefficient: int = 1) -> None:
    scalar = int(coefficient) % 3
    if scalar:
        destination[:] = (
            destination.astype(np.uint16) + scalar * source.astype(np.uint16)
        ) % 3


def translated(source: np.ndarray, mapping: np.ndarray, coefficient: int) -> np.ndarray:
    answer = np.zeros(504, dtype=np.uint8)
    answer[mapping] = (int(coefficient) % 3) * source.astype(np.uint16) % 3
    return answer


def source_lower_coord(tag: int, component: int, psl: int = 0) -> int:
    return (tag * 2 + component) * 504 + psl


def source_grade_coord(tag: int, component: int, monomial: int, psl: int = 0) -> int:
    return ((tag * 2 + component) * 3 + monomial) * 504 + psl


def source_seed_pair(
    seed: tuple[list[list[tuple[int, Aff, int]]], list[int], tuple[int, int]],
    context: IndependentContext,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Independent source-character degree-zero/one Fourier evaluation."""
    lower = np.zeros((4, 6048), dtype=np.uint8)
    grade = np.zeros((4, SOURCE_WIDTH), dtype=np.uint8)
    auxiliary = np.zeros(8, dtype=np.uint8)
    for tag, normal_row in enumerate(seed[0]):
        auxiliary[tag] = seed[1][tag]
        for component, value, coefficient in normal_row:
            psl = context.index[value[0]]
            for source_index, source_label in enumerate(CHARS):
                target_label = context.transports[tag][source_label]
                weight = int(coefficient) * character(target_label, value[1], value[2])
                li = source_lower_coord(tag, component, psl)
                lower[source_index, li] = (int(lower[source_index, li]) + weight) % 3
                for monomial, kernel_coefficient in enumerate(value[3]):
                    if kernel_coefficient:
                        gi = source_grade_coord(tag, component, monomial, psl)
                        grade[source_index, gi] = (
                            int(grade[source_index, gi]) + weight * kernel_coefficient
                        ) % 3
    auxiliary[6:] = seed[2]
    return lower, grade, auxiliary


def act_source_pair(
    context: IndependentContext,
    lower: np.ndarray,
    grade: np.ndarray,
    auxiliary: np.ndarray,
    source_actor: Aff,
    tag_actors: tuple[Aff, ...],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    insist(lower.shape == (4, 6048) and grade.shape == (4, SOURCE_WIDTH), "source_pair_shape")
    out_lower = np.zeros_like(lower)
    out_grade = np.zeros_like(grade)
    for source_index, source_label in enumerate(CHARS):
        direct_scalar = character(source_label, source_actor[1], source_actor[2])
        for tag, actor in enumerate(tag_actors):
            mapping = context.left_map(actor[0])
            target_label = context.transports[tag][source_label]
            for component in (0, 1):
                lstart = source_lower_coord(tag, component)
                lower_image = translated(lower[source_index, lstart : lstart + 504], mapping, direct_scalar)
                out_lower[source_index, lstart : lstart + 504] = lower_image
                for monomial in range(3):
                    gstart = source_grade_coord(tag, component, monomial)
                    add_mod3(
                        out_grade[source_index, gstart : gstart + 504],
                        translated(
                            grade[source_index, gstart : gstart + 504], mapping, direct_scalar
                        ),
                    )
                    kernel_coefficient = actor[3][monomial]
                    if kernel_coefficient:
                        output_target = (
                            target_label[0] ^ ETA[monomial][0],
                            target_label[1] ^ ETA[monomial][1],
                        )
                        output_source = context.inverse_transports[tag][output_target]
                        output_index = CHARS.index(output_source)
                        induced_scalar = kernel_coefficient * character(
                            output_target, actor[1], actor[2]
                        )
                        add_mod3(
                            out_grade[output_index, gstart : gstart + 504],
                            translated(
                                lower[source_index, lstart : lstart + 504],
                                mapping,
                                induced_scalar,
                            ),
                        )
    return out_lower, out_grade, auxiliary.copy()


def project_source_pair(
    context: IndependentContext,
    base: tuple[np.ndarray, np.ndarray, np.ndarray],
    label: tuple[int, int],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    lower = np.zeros_like(base[0])
    grade = np.zeros_like(base[1])
    auxiliary = np.zeros_like(base[2])
    for parity in CHARS:
        acted = act_source_pair(
            context,
            base[0],
            base[1],
            base[2],
            context.pure_source[parity],
            context.pure_tags[parity],
        )
        coefficient = character(label, parity[0], parity[1])
        add_mod3(lower, acted[0], coefficient)
        add_mod3(grade, acted[1], coefficient)
        add_mod3(auxiliary, acted[2], coefficient)
    selected = CHARS.index(label)
    insist(
        all(not np.any(lower[index]) for index in range(4) if index != selected),
        "projected_lower_leak",
    )
    if label != (0, 0):
        insist(not np.any(auxiliary), "projected_auxiliary_leak")
    return lower, grade, auxiliary


def lower_actor(
    context: IndependentContext,
    row: np.ndarray,
    label: tuple[int, int],
    letter: int,
) -> np.ndarray:
    insist(row.shape == (6056,), "lower_actor_shape")
    answer = np.zeros_like(row)
    scalar = character(label, context.actor_source[letter][1], context.actor_source[letter][2])
    for tag, actor in enumerate(context.actor_tags[letter]):
        mapping = context.left_map(actor[0])
        for component in (0, 1):
            start = source_lower_coord(tag, component)
            answer[start : start + 504] = translated(row[start : start + 504], mapping, scalar)
    answer[6048:] = row[6048:]
    return answer


def lifted_grade_actor(
    context: IndependentContext,
    lower_row: np.ndarray,
    grade_flat: np.ndarray,
    label: tuple[int, int],
    letter: int,
) -> np.ndarray:
    lower = np.zeros((4, 6048), dtype=np.uint8)
    lower[CHARS.index(label)] = lower_row[:6048]
    acted = act_source_pair(
        context,
        lower,
        grade_flat.reshape(4, SOURCE_WIDTH),
        lower_row[6048:],
        context.actor_source[letter],
        context.actor_tags[letter],
    )
    return acted[1].reshape(4 * SOURCE_WIDTH)


def column(
    seed: tuple[list[list[tuple[int, Aff, int]]], list[int], tuple[int, int]],
    conjugator: tuple[int, ...],
    context: IndependentContext,
) -> dict[int, int]:
    output: dict[int, int] = {}
    actors = tuple(value_of(substitute(conjugator, *pair), context.images) for pair in OCC)
    agg = {tag: (block, sign) for tag, block, sign in context.aggregation}
    for tag in range(6):
        combined = product(context.shifts[tag], actors[tag])
        block, sign = agg[tag]
        for component, value, coefficient in seed[0][tag]:
            final = product(combined, value)
            psl = context.index[final[0]]
            for ci, label in enumerate(CHARS):
                weight = sign * coefficient * character(label, final[1], final[2])
                sparse_add(output, pcoord(ci, block, component, 0, psl), weight)
                for monomial, v in enumerate(final[3]):
                    if v:
                        sparse_add(output, pcoord(ci, block, component, monomial + 1, psl), weight * v)
        sparse_add(output, 4 * 2 * 2 * 4 * 504 + block, sign * seed[1][tag])
    sparse_add(output, 4 * 2 * 2 * 4 * 504 + 2, seed[2][0])
    sparse_add(output, 4 * 2 * 2 * 4 * 504 + 3, seed[2][1])
    return output


def target(context: IndependentContext) -> dict[int, int]:
    g = context.words["g760"]
    h1 = reduced_product(substitute(g, *OCC[2]), inverse_word(substitute(g, *OCC[1])), substitute(g, *OCC[0]))
    h2 = reduced_product(substitute(g, *OCC[5]), inverse_word(substitute(g, *OCC[4])), inverse_word(substitute(g, *OCC[3])))
    output: dict[int, int] = {}
    for block, word in enumerate((h1, h2)):
        row, augmentation = normal(word, context)
        sparse_add(output, 4 * 2 * 2 * 4 * 504 + block, -augmentation)
        for component, value, coefficient in row:
            psl = context.index[value[0]]
            for ci, label in enumerate(CHARS):
                weight = -coefficient * character(label, value[1], value[2])
                sparse_add(output, pcoord(ci, block, component, 0, psl), weight)
                for monomial, v in enumerate(value[3]):
                    if v:
                        sparse_add(output, pcoord(ci, block, component, monomial + 1, psl), weight * v)
    return output


def replay_member(terms: list[list[Any]], context: IndependentContext) -> None:
    seeds = [raw_seed(word, context) for word in context.words["relators"]]
    actual: dict[int, int] = {}
    for seed, word, coefficient in terms:
        for coordinate, value in column(seeds[int(seed) - 1], tuple(int(x) for x in word), context).items():
            sparse_add(actual, coordinate, int(coefficient) * value)
    insist(actual == target(context), "direct_precision1_replay")


def rebuild_prepare_residual(
    terms: list[list[Any]],
    context: IndependentContext,
    seeds: list[tuple[list[list[tuple[int, Aff, int]]], list[int], tuple[int, int]]] | None = None,
) -> tuple[np.ndarray, list[tuple[list[list[tuple[int, Aff, int]]], list[int], tuple[int, int]]]]:
    """Rebuild target minus the frozen ORDER-2016 lift through degree one."""
    if seeds is None:
        seeds = [raw_seed(word, context) for word in context.words["relators"]]
    difference = target(context).copy()
    for seed, word, coefficient in terms:
        for coordinate, value in column(
            seeds[int(seed) - 1], tuple(int(x) for x in word), context
        ).items():
            sparse_add(difference, coordinate, -int(coefficient) * value)
    residual = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    lower = np.zeros(8068, dtype=np.uint8)
    for character_index in range(4):
        for block in range(2):
            for component in range(2):
                for psl in range(504):
                    lower_coordinate = ((character_index * 2 + block) * 2 + component) * 504 + psl
                    lower[lower_coordinate] = difference.get(
                        pcoord(character_index, block, component, 0, psl), 0
                    )
                    for monomial in range(3):
                        residual_coordinate = (
                            ((character_index * 2 + block) * 2 + component) * 3 + monomial
                        ) * 504 + psl
                        residual[residual_coordinate] = difference.get(
                            pcoord(character_index, block, component, monomial + 1, psl), 0
                        )
    lower[8064:] = [difference.get(4 * 2 * 2 * 4 * 504 + index, 0) for index in range(4)]
    insist(not np.any(lower), "prepare_residual_nonzero_lower")
    allowed = set()
    for character_index in range(4):
        for block in range(2):
            for component in range(2):
                for monomial in range(4):
                    start = pcoord(character_index, block, component, monomial, 0)
                    allowed.update(range(start, start + 504))
    allowed.update(range(4 * 2 * 2 * 4 * 504, 4 * 2 * 2 * 4 * 504 + 4))
    insist(all(coordinate in allowed for coordinate in difference), "prepare_residual_coordinate")
    return residual, seeds


def fixed_dimensions() -> dict[str, Any]:
    return {"characters": 4, "character_labels": [list(x) for x in CHARS], "monomials": [list(x) for x in MONS1], "monomials_coupled": True, "source_base": 6048, "source_per_character": 18144, "source_total": 72576, "physical_grade": 24192, "physical_lower_regular": 8064, "physical_lower_with_auxiliary": 8068}


class DenseOwner:
    """Independent dense echelon replay; pivot ids remain insertion ordered."""

    def __init__(self, width: int):
        self.width = width
        self.rows: list[np.ndarray] = []
        self.leads: list[int] = []
        self.lead_to_pivot: dict[int, int] = {}

    def reduce(self, row: np.ndarray) -> tuple[np.ndarray, list[list[int]]]:
        insist(row.shape == (self.width,) and not np.any(row > 2), "dense_reduce_shape")
        work = row.copy()
        reductions: list[list[int]] = []
        while True:
            support = np.flatnonzero(work)
            if not len(support):
                break
            lead = int(support[0])
            pivot = self.lead_to_pivot.get(lead)
            if pivot is None:
                break
            coefficient = int(work[lead])
            work = (
                work.astype(np.int16) - coefficient * self.rows[pivot].astype(np.int16)
            ) % 3
            work = work.astype(np.uint8)
            reductions.append([pivot, coefficient])
        return work, reductions

    def insert(self, row: np.ndarray) -> dict[str, Any]:
        remainder, reductions = self.reduce(row)
        support = np.flatnonzero(remainder)
        if not len(support):
            return {"accepted": False, "reductions": reductions}
        lead = int(support[0])
        leading = int(remainder[lead])
        scale = 1 if leading == 1 else 2
        normalized = (scale * remainder.astype(np.uint16) % 3).astype(np.uint8)
        pivot = len(self.rows)
        self.rows.append(normalized)
        self.leads.append(lead)
        self.lead_to_pivot[lead] = pivot
        return {
            "accepted": True,
            "pivot": pivot,
            "lead": lead,
            "leading_coefficient": leading,
            "scale": scale,
            "reductions": reductions,
        }


def insertion_expression(record: dict[str, Any]) -> list[list[int]]:
    answer = [list(pair) for pair in record["reductions"]]
    if record["accepted"]:
        answer.append([int(record["pivot"]), int(record["leading_coefficient"])])
    return answer


def compare_packet_row(
    packet_maps: list[np.ndarray],
    origin: int,
    grade_flat: np.ndarray,
    zero_counts: list[int],
) -> None:
    insist(grade_flat.shape == (4 * SOURCE_WIDTH,), "defect_shape")
    rows = grade_flat.reshape(4, SOURCE_WIDTH)
    for packet in range(4):
        row = rows[packet]
        if not np.any(row):
            zero_counts[packet] += 1
        insist(np.array_equal(pack(row), packet_maps[packet][origin]), "prepare_packet_row")


def verify_paired_prepare(
    state_dir: Path,
    prepare: dict[str, Any],
    context: IndependentContext,
    raw_seeds: list[tuple[list[list[tuple[int, Aff, int]]], list[int], tuple[int, int]]],
) -> None:
    """Rebuild all old paired closures and every packet origin independently."""
    insist(len(raw_seeds) == 44 and len(prepare.get("old_blocks", [])) == 4, "old_block_count")
    origins = prepare.get("defect_origins")
    insist(isinstance(origins, list) and len(origins) > 0, "defect_origins")
    origin_digest = digest(canon(origins))
    insist(prepare.get("defect_origin_sha256") == origin_digest, "defect_origin_digest")
    insist(len(prepare.get("packets", [])) == 4, "packet_count")
    packet_maps: list[np.ndarray] = []
    for packet, receipt in enumerate(prepare["packets"]):
        insist(
            receipt.get("character") == list(CHARS[packet])
            and receipt.get("origin_count") == len(origins)
            and receipt.get("origin_sha256") == origin_digest,
            "packet_metadata",
        )
        packet_maps.append(packed_map(state_dir, receipt["blob"], SOURCE_WIDTH, len(origins)))

    source_pairs = [source_seed_pair(seed, context) for seed in raw_seeds]
    zero_counts = [0, 0, 0, 0]
    origin_cursor = 0
    for character_index, label in enumerate(CHARS):
        old = prepare["old_blocks"][character_index]
        insist(
            old.get("character_index") == character_index
            and old.get("character") == list(label)
            and isinstance(old.get("rank"), int),
            "old_block_metadata",
        )
        rank = int(old["rank"])
        record = old.get("record")
        insist(
            isinstance(record, dict)
            and record.get("character") == list(label)
            and record.get("rank") == rank
            and record.get("actor_order") == list(ACTORS)
            and record.get("queue_exhausted") is True
            and record.get("attempts") == 44 + 4 * rank
            and len(record.get("seed_reductions", [])) == 44
            and len(record.get("actor_transitions", [])) == rank
            and len(record.get("dag_nodes", [])) == rank,
            "old_record_shape",
        )
        stored_lower = packed_map(state_dir, old["lower_basis_blob"], 6056, rank)
        stored_lifts = packed_map(state_dir, old["lifted_grade_blob"], 4 * SOURCE_WIDTH, rank)
        projected = [project_source_pair(context, pair, label) for pair in source_pairs]
        owner = DenseOwner(6056)
        queue: deque[int] = deque()

        def check_new_node(inserted: dict[str, Any], origin: dict[str, Any]) -> None:
            if not inserted["accepted"]:
                return
            pivot = int(inserted["pivot"])
            insist(pivot < rank, "old_rank_overflow")
            expected = {
                "pivot": pivot,
                "lead": int(inserted["lead"]),
                "scale": int(inserted["scale"]),
                "origin": origin,
                "reductions": inserted["reductions"],
            }
            insist(record["dag_nodes"][pivot] == expected, "old_dag_node")
            insist(np.array_equal(pack(owner.rows[pivot]), stored_lower[pivot]), "old_lower_basis")
            queue.append(pivot)

        for seed_index, pair in enumerate(projected):
            lower_row = np.empty(6056, dtype=np.uint8)
            lower_row[:6048] = pair[0][character_index]
            lower_row[6048:] = pair[2]
            inserted = owner.insert(lower_row)
            insist(
                record["seed_reductions"][seed_index] == insertion_expression(inserted),
                "old_seed_reduction",
            )
            check_new_node(
                inserted, {"kind": "projected_seed", "seed": seed_index + 1}
            )
        while queue:
            pivot = queue.popleft()
            insist(
                isinstance(record["actor_transitions"][pivot], list)
                and len(record["actor_transitions"][pivot]) == 4,
                "old_transition_shape",
            )
            for actor_index, letter in enumerate(ACTORS):
                inserted = owner.insert(lower_actor(context, owner.rows[pivot], label, letter))
                insist(
                    record["actor_transitions"][pivot][actor_index]
                    == insertion_expression(inserted),
                    "old_actor_transition",
                )
                check_new_node(
                    inserted, {"kind": "actor", "parent": pivot, "letter": letter}
                )
        insist(len(owner.rows) == rank, "old_rank")

        lifts = np.empty((rank, 4 * SOURCE_WIDTH), dtype=np.uint8)
        for pivot, node in enumerate(record["dag_nodes"]):
            source = node["origin"]
            if source["kind"] == "projected_seed":
                work = projected[int(source["seed"]) - 1][1].reshape(4 * SOURCE_WIDTH).copy()
            else:
                parent = int(source["parent"])
                insist(parent < pivot, "old_lift_cycle")
                work = lifted_grade_actor(
                    context, owner.rows[parent], lifts[parent], label, int(source["letter"])
                )
            for earlier, coefficient in node["reductions"]:
                insist(int(earlier) < pivot and int(coefficient) in (1, 2), "old_lift_reduction")
                add_mod3(work, lifts[int(earlier)], -int(coefficient))
            work = (int(node["scale"]) * work.astype(np.uint16) % 3).astype(np.uint8)
            lifts[pivot] = work
            insist(np.array_equal(pack(work), stored_lifts[pivot]), "old_lift_basis")

        range_begin = origin_cursor
        for seed_index, pair in enumerate(projected):
            expression = record["seed_reductions"][seed_index]
            work = pair[1].reshape(4 * SOURCE_WIDTH).copy()
            for pivot, coefficient in expression:
                add_mod3(work, lifts[int(pivot)], -int(coefficient))
            expected_origin = {
                "id": origin_cursor,
                "kind": "seed",
                "lower_character": character_index,
                "seed": seed_index + 1,
            }
            insist(origins[origin_cursor] == expected_origin, "seed_defect_origin")
            compare_packet_row(packet_maps, origin_cursor, work, zero_counts)
            origin_cursor += 1
        for pivot in range(rank):
            for actor_index, letter in enumerate(ACTORS):
                work = lifted_grade_actor(context, owner.rows[pivot], lifts[pivot], label, letter)
                for earlier, coefficient in record["actor_transitions"][pivot][actor_index]:
                    add_mod3(work, lifts[int(earlier)], -int(coefficient))
                expected_origin = {
                    "id": origin_cursor,
                    "kind": "transition",
                    "lower_character": character_index,
                    "pivot": pivot,
                    "letter": letter,
                }
                insist(origins[origin_cursor] == expected_origin, "transition_defect_origin")
                compare_packet_row(packet_maps, origin_cursor, work, zero_counts)
                origin_cursor += 1
        insist(old.get("defect_origin_range") == [range_begin, origin_cursor], "defect_origin_range")
        del stored_lower, stored_lifts, projected, lifts, owner
    insist(origin_cursor == len(origins), "defect_origin_complete")
    for packet in range(4):
        insist(prepare["packets"][packet].get("zero_rows") == zero_counts[packet], "packet_zero_rows")
    del packet_maps


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_expression(value: Any, rank: int, gate: str, upper: int | None = None) -> None:
    insist(isinstance(value, list), gate + "_shape")
    bound = rank if upper is None else upper
    for pair in value:
        insist(
            isinstance(pair, list)
            and len(pair) == 2
            and plain_int(pair[0])
            and 0 <= pair[0] < bound
            and plain_int(pair[1])
            and pair[1] in (1, 2),
            gate + "_entry",
        )


def validate_nonmember_block_roster(prepare: dict[str, Any], body: dict[str, Any]) -> None:
    """R1: establish complete typed source coverage before any row algebra."""
    rank = body.get("rank")
    origin_count = body.get("origin_count")
    insist(plain_int(rank) and rank >= 0, "block_rank")
    insist(
        plain_int(origin_count)
        and origin_count == len(prepare.get("defect_origins", [])),
        "block_origin_count",
    )
    origins = body.get("origin_reductions")
    transitions = body.get("actor_transitions")
    nodes = body.get("dag_nodes")
    insist(isinstance(origins, list) and len(origins) == origin_count, "origin_reduction_count")
    insist(
        isinstance(transitions, list)
        and len(transitions) == rank
        and all(isinstance(row, list) and len(row) == 4 for row in transitions),
        "block_transition_count",
    )
    insist(isinstance(nodes, list) and len(nodes) == rank, "block_dag_count")
    for origin, expression in enumerate(origins):
        validate_expression(expression, rank, f"origin_reduction_{origin}")
    for pivot, row in enumerate(transitions):
        for actor_index, expression in enumerate(row):
            validate_expression(expression, rank, f"actor_transition_{pivot}_{actor_index}")
    for pivot, node in enumerate(nodes):
        insist(
            isinstance(node, dict)
            and node.get("pivot") == pivot
            and plain_int(node.get("lead"))
            and 0 <= node["lead"] < SOURCE_WIDTH
            and node.get("scale") in (1, 2),
            "block_dag_node",
        )
        validate_expression(node.get("reductions"), rank, f"block_dag_reduction_{pivot}", pivot)
        origin = node.get("origin")
        insist(isinstance(origin, dict), "block_dag_origin")
        if origin.get("kind") == "defect":
            insist(
                plain_int(origin.get("origin")) and 0 <= origin["origin"] < origin_count,
                "block_dag_defect_origin",
            )
        elif origin.get("kind") == "actor":
            insist(
                plain_int(origin.get("parent"))
                and 0 <= origin["parent"] < pivot
                and origin.get("letter") in ACTORS,
                "block_dag_actor_origin",
            )
        else:
            raise RuntimeError("block_dag_origin_kind")


def claim_flags() -> dict[str, bool]:
    return {
        "ORDER_54432": False,
        "FULL_Q0": False,
        "A0": False,
        "COMMON": False,
        "COMPATIBLE_LIFT": False,
        "FAKE": False,
        "IHARA": False,
        "verified": False,
    }


def validate_prepare_state_files(
    state_dir: Path, prepare: dict[str, Any], receipt: dict[str, dict[str, Any]]
) -> None:
    insist(
        prepare.get("phase") == "prepare"
        and prepare.get("fixture") is False
        and prepare.get("input_manifest") == receipt
        and prepare.get("input_manifest_sha256") == digest(canon(receipt))
        and prepare.get("dimensions") == fixed_dimensions()
        and prepare.get("paired_lower_presentation_complete") is True
        and prepare.get("downstream_claim_flags") == claim_flags(),
        "prepare_state_semantics",
    )
    origins = prepare.get("defect_origins")
    old_blocks = prepare.get("old_blocks")
    packets = prepare.get("packets")
    insist(
        isinstance(origins, list)
        and isinstance(old_blocks, list)
        and len(old_blocks) == 4
        and isinstance(packets, list)
        and len(packets) == 4
        and prepare.get("defect_origin_sha256") == digest(canon(origins)),
        "prepare_state_rosters",
    )
    checked_blob_path(state_dir, prepare["residual_blob"], PHYSICAL_WIDTH, 1)
    cursor = 0
    for character_index, old in enumerate(old_blocks):
        rank = old.get("rank")
        record = old.get("record")
        insist(
            old.get("character_index") == character_index
            and old.get("character") == list(CHARS[character_index])
            and plain_int(rank)
            and rank >= 0
            and isinstance(record, dict)
            and record.get("rank") == rank
            and record.get("character") == list(CHARS[character_index])
            and record.get("attempts") == 44 + 4 * rank
            and record.get("actor_order") == list(ACTORS)
            and record.get("queue_exhausted") is True
            and isinstance(record.get("seed_reductions"), list)
            and len(record["seed_reductions"]) == 44
            and isinstance(record.get("actor_transitions"), list)
            and len(record["actor_transitions"]) == rank
            and all(isinstance(row, list) and len(row) == 4 for row in record["actor_transitions"])
            and isinstance(record.get("dag_nodes"), list)
            and len(record["dag_nodes"]) == rank,
            "prepare_old_block",
        )
        checked_blob_path(state_dir, old["lower_basis_blob"], 6056, rank)
        checked_blob_path(state_dir, old["lifted_grade_blob"], 4 * SOURCE_WIDTH, rank)
        end = cursor + 44 + 4 * rank
        insist(old.get("defect_origin_range") == [cursor, end], "prepare_origin_range")
        cursor = end
    insist(cursor == len(origins), "prepare_origin_count")
    for index, origin in enumerate(origins):
        insist(isinstance(origin, dict) and origin.get("id") == index, "prepare_origin_id")
    for packet_index, packet in enumerate(packets):
        insist(
            packet.get("character") == list(CHARS[packet_index])
            and packet.get("origin_count") == len(origins)
            and packet.get("origin_sha256") == prepare["defect_origin_sha256"],
            "prepare_packet_metadata",
        )
        checked_blob_path(state_dir, packet["blob"], SOURCE_WIDTH, len(origins))


def validate_block_state_file(
    state_dir: Path,
    prepare: dict[str, Any],
    prepare_digest: str,
    block: int,
    body: dict[str, Any],
) -> None:
    validate_nonmember_block_roster(prepare, body)
    insist(
        body.get("phase") == "block"
        and body.get("fixture") is False
        and body.get("parent_sha256") == prepare_digest
        and body.get("character_index") == block
        and body.get("character") == list(CHARS[block])
        and body.get("dimensions") == {"width": SOURCE_WIDTH, "monomials_coupled": 3}
        and body.get("packet_sha256") == prepare["packets"][block]["blob"]["sha256"]
        and body.get("attempts") == body["origin_count"] + 4 * body["rank"]
        and body.get("queue_exhausted") is True
        and body.get("actor_order") == list(ACTORS)
        and body.get("downstream_claim_flags") == claim_flags(),
        "block_state_semantics",
    )
    leads = body.get("pivot_leads")
    insist(
        isinstance(leads, list)
        and len(leads) == body["rank"]
        and all(plain_int(lead) and 0 <= lead < SOURCE_WIDTH for lead in leads)
        and len(set(leads)) == len(leads)
        and leads == [node["lead"] for node in body["dag_nodes"]]
        and body.get("dag_sha256") == digest(canon(body["dag_nodes"])),
        "block_pivot_roster",
    )
    checked_blob_path(state_dir, body["basis_blob"], SOURCE_WIDTH, body["rank"])


def validate_merge_state_file(
    state_dir: Path,
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
    merge: dict[str, Any],
) -> None:
    lower_rank = merge.get("physical_lower_rank")
    grade_rank = merge.get("physical_grade_rank")
    roster = merge.get("physical_roster")
    insist(
        merge.get("phase") == "merge"
        and merge.get("fixture") is False
        and merge.get("parent_sha256") == prepare_digest
        and merge.get("block_sha256") == [state_digest for _, state_digest in blocks]
        and merge.get("dimensions") == fixed_dimensions()
        and merge.get("source_blocks_exhausted") == 4
        and merge.get("terminal")
        in ("FIRST_RUNG_GRADE1_MEMBER", "FIRST_RUNG_GRADE1_NONMEMBER")
        and plain_int(lower_rank)
        and lower_rank >= 0
        and plain_int(grade_rank)
        and grade_rank >= 0
        and isinstance(roster, list)
        and len(roster)
        == sum(old["rank"] for old in prepare["old_blocks"])
        + sum(body["rank"] for body, _ in blocks)
        and merge.get("physical_roster_sha256") == digest(canon(roster))
        and isinstance(merge.get("physical_lower_dag"), list)
        and len(merge["physical_lower_dag"]) == lower_rank
        and isinstance(merge.get("physical_grade_dag"), list)
        and len(merge["physical_grade_dag"]) == grade_rank
        and isinstance(merge.get("physical_grade_pivot_leads"), list)
        and len(merge["physical_grade_pivot_leads"]) == grade_rank
        and merge.get("downstream_claim_flags") == claim_flags()
        and isinstance(merge.get("provisional_merge_sha256"), str)
        and re.fullmatch(r"[0-9a-f]{64}", merge["provisional_merge_sha256"]) is not None,
        "merge_state_semantics",
    )
    checked_blob_path(
        state_dir, merge["physical_grade_basis_blob"], PHYSICAL_WIDTH, grade_rank
    )
    presentation = merge.get("transition_presentation")
    insist(isinstance(presentation, dict) and presentation.get("complete") is True, "transition_presentation")
    presentation_body = dict(presentation)
    presentation_digest = presentation_body.pop("sha256", None)
    insist(digest(canon(presentation_body)) == presentation_digest, "transition_presentation_digest")
    if merge["terminal"] == "FIRST_RUNG_GRADE1_MEMBER":
        next_residual = merge.get("next_degree2_residual")
        width = 4 * 2 * 2 * 6 * 504
        insist(
            isinstance(next_residual, dict)
            and next_residual.get("grade") == 2
            and next_residual.get("width") == width,
            "next_residual",
        )
        checked_blob_path(state_dir, next_residual["blob"], width, 1)
    else:
        insist(merge.get("next_degree2_residual") is None, "nonmember_next_residual")


def expected_certificate(
    receipt: dict[str, dict[str, Any]],
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
    merge: dict[str, Any],
    merge_digest: str,
) -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".certificate",
        "producer_sha256": PRODUCER_SHA256,
        "input_manifest": receipt,
        "input_manifest_sha256": prepare["input_manifest_sha256"],
        "state_chain": {
            "prepare_sha256": prepare_digest,
            "block_sha256": [state_digest for _, state_digest in blocks],
            "merge_sha256": merge_digest,
        },
        "dimensions": fixed_dimensions(),
        "canonical_solution": prepare["canonical_solution"],
        "pure_q1_projectors": prepare["pure_q1_projectors"],
        "source_closures": [
            {
                "character_index": index,
                "rank": body["rank"],
                "attempts": body["attempts"],
                "queue_exhausted": body["queue_exhausted"],
                "basis_sha256": body["basis_blob"]["sha256"],
                "dag_sha256": body["dag_sha256"],
            }
            for index, (body, _) in enumerate(blocks)
        ],
        "physical": {
            "roster_sha256": merge["physical_roster_sha256"],
            "roster": merge["physical_roster"],
            "lower_rank": merge["physical_lower_rank"],
            "grade_rank": merge["physical_grade_rank"],
            "basis_sha256": merge["physical_grade_basis_blob"]["sha256"],
            "residual_sha256": prepare["residual_sha256"],
            "remainder_sha256": merge["remainder_sha256"],
            "remainder_support": merge["remainder_support"],
            "dual": merge["dual"],
            "dual_pair": merge["dual_pair"],
        },
        "transition_presentation": merge["transition_presentation"],
        "source_ancestry": merge["source_ancestry"],
        "next_degree2_residual": merge["next_degree2_residual"],
        "terminal": merge["terminal"],
        "downstream_claim_flags": claim_flags(),
        "verified": False,
        "runtime_seconds": merge["elapsed_seconds"],
    }


def verify_certificate(state_dir: Path) -> dict[str, Any]:
    receipt = pins()
    prepare, prepare_digest = read_state(state_dir, "prepare")
    validate_prepare_state_files(state_dir, prepare, receipt)
    frozen = json.loads((ROOT / "search/certs/d972_r07_a0_c2fourier_joint_floor_v1.json").read_text(encoding="utf-8"))["source_ancestry"]["full_literal_terms"]
    canonical = canonical_terms(frozen)
    insist(len(frozen) == 3936 and len(canonical) == 2622 and prepare["canonical_solution"]["terms"] == canonical, "canonical_solution")
    blocks = [read_state(state_dir, f"block-{i}", prepare_digest) for i in range(4)]
    for i, (body, _) in enumerate(blocks):
        validate_block_state_file(state_dir, prepare, prepare_digest, i, body)
    merge, merge_digest = read_state(state_dir, "merge", prepare_digest)
    validate_merge_state_file(state_dir, prepare, prepare_digest, blocks, merge)
    certificate_path = ROOT / "search/certs/d972_r07_a0_first_rung_grade1_v3.json"
    certificate_data = certificate_path.read_bytes()
    certificate = json.loads(certificate_data)
    insist(canon(certificate) == certificate_data, "certificate_canonical")
    insist(
        certificate
        == expected_certificate(
            receipt, prepare, prepare_digest, blocks, merge, merge_digest
        ),
        "certificate_complete_content",
    )
    if merge["terminal"] == "FIRST_RUNG_GRADE1_MEMBER":
        terms = certificate["source_ancestry"]["accumulated_terms"]
        insist(terms == canonical_terms(terms), "member_terms_canonical")
        replay_member(terms, IndependentContext())
        insist(certificate["source_ancestry"]["direct_precision1_target_replay"] is True and certificate["source_ancestry"]["zero_lower_change"] is True, "member_replay_receipt")
        insist(certificate.get("next_degree2_residual") is not None, "next_residual")
        read_blob(state_dir, certificate["next_degree2_residual"]["blob"])
    elif merge["terminal"] == "FIRST_RUNG_GRADE1_NONMEMBER":
        verify_nonmember(state_dir, prepare, blocks, merge)
    else:
        raise RuntimeError("terminal")
    return {"terminal": merge["terminal"], "prepare_sha256": prepare_digest, "merge_sha256": merge_digest}


def verify_nonmember(
    state_dir: Path,
    prepare: dict[str, Any],
    blocks: list[tuple[dict[str, Any], str]],
    merge: dict[str, Any],
) -> None:
    # Full dual rows are rebound below; discovery pivot identities remain
    # telemetry, but packet containment and all four actor reductions are
    # checked directly in the complete 18,144-coordinate blocks.
    for body, _ in blocks:
        validate_nonmember_block_roster(prepare, body)
    context = IndependentContext()
    frozen = json.loads(
        (ROOT / "search/certs/d972_r07_a0_c2fourier_joint_floor_v1.json").read_text(
            encoding="utf-8"
        )
    )["source_ancestry"]["full_literal_terms"]
    canonical = canonical_terms(frozen)
    rebuilt_residual, raw_seeds = rebuild_prepare_residual(canonical, context)
    residual = unpack(read_blob(state_dir, prepare["residual_blob"]), PHYSICAL_WIDTH, 1)[0]
    insist(np.array_equal(rebuilt_residual, residual), "prepare_residual_blob")
    insist(prepare.get("residual_support") == int(np.count_nonzero(residual)), "residual_support")
    residual_sparse = [
        [int(coordinate), int(residual[coordinate])] for coordinate in np.flatnonzero(residual)
    ]
    insist(
        prepare.get("residual_sha256")
        == digest(json.dumps(residual_sparse, separators=(",", ":")).encode("ascii")),
        "residual_sparse_digest",
    )
    verify_paired_prepare(state_dir, prepare, context, raw_seeds)
    dual = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    for coordinate, coefficient in merge["dual"]:
        dual[int(coordinate)] = int(coefficient)
    insist(np.any(dual) and merge["dual_pair"] in (1, 2), "dual_shape")
    insist(int(np.dot(residual.astype(np.int64), dual.astype(np.int64)) % 3) == merge["dual_pair"], "dual_pair")
    for character_index, (body, _) in enumerate(blocks):
        basis = unpack(read_blob(state_dir, body["basis_blob"]), SOURCE_WIDTH, body["rank"])
        packet = packed_map(
            state_dir,
            prepare["packets"][character_index]["blob"],
            SOURCE_WIDTH,
            body["origin_count"],
        )
        for origin, expression in enumerate(body["origin_reductions"]):
            rebuilt = np.zeros(SOURCE_WIDTH, dtype=np.uint8)
            for pivot, coefficient in expression:
                rebuilt = (rebuilt.astype(np.uint16) + int(coefficient) * basis[int(pivot)].astype(np.uint16)) % 3
            insist(np.array_equal(pack(rebuilt.astype(np.uint8)), packet[origin]), "packet_reduction")
        for pivot in range(body["rank"]):
            for actor_index, letter in enumerate(ACTORS):
                child = independent_grade_actor(context, basis[pivot], CHARS[character_index], letter)
                rebuilt = np.zeros(SOURCE_WIDTH, dtype=np.uint8)
                for target_pivot, coefficient in body["actor_transitions"][pivot][actor_index]:
                    rebuilt = (rebuilt.astype(np.uint16) + int(coefficient) * basis[int(target_pivot)].astype(np.uint16)) % 3
                insist(np.array_equal(child, rebuilt.astype(np.uint8)), "actor_transition")
            physical = independent_aggregate_grade(context, character_index, basis[pivot])
            insist(int(np.dot(physical.astype(np.int64), dual.astype(np.int64)) % 3) == 0, "dual_defect_annihilation")
        del basis, packet
    # Old-lift zero-lower connections are checked against the sealed physical
    # grade basis DAG/body by reconstructing their complete aggregates.
    verify_old_connections(state_dir, prepare, dual, context)


def independent_grade_actor(context: IndependentContext, row: np.ndarray, label: tuple[int, int], letter: int) -> np.ndarray:
    output = np.zeros_like(row)
    scalar = character(label, context.actor_source[letter][1], context.actor_source[letter][2])
    for tag, actor in enumerate(context.actor_tags[letter]):
        mapping = context.left_map(actor[0])
        for component in (0, 1):
            for monomial in range(3):
                start = ((tag * 2 + component) * 3 + monomial) * 504
                output[start + mapping] = scalar * row[start : start + 504] % 3
    return output


def transport_labels(context: IndependentContext) -> list[dict[tuple[int, int], tuple[int, int]]]:
    return context.transports


def independent_aggregate_grade(context: IndependentContext, character_index: int, row: np.ndarray) -> np.ndarray:
    output = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    transports = transport_labels(context)
    label = CHARS[character_index]
    for tag, block, sign in context.aggregation:
        shift = context.shifts[tag]
        target_label = transports[tag][label]
        target_index = CHARS.index(target_label)
        scalar = sign * character(target_label, shift[1], shift[2])
        mapping = context.left_map(shift[0])
        for component in (0,1):
            for monomial in range(3):
                source = ((tag*2+component)*3+monomial)*504
                destination = (((target_index*2+block)*2+component)*3+monomial)*504
                output[destination + mapping] = (output[destination + mapping] + scalar * row[source:source+504]) % 3
    return output


def verify_old_connections(state_dir: Path, prepare: dict[str, Any], dual: np.ndarray, context: IndependentContext) -> None:
    # Rebuild the same lower-first kernel with an independent dense lead map.
    lower_basis: dict[int, tuple[np.ndarray, np.ndarray]] = {}
    for old in prepare["old_blocks"]:
        rank = old["rank"]
        lower_rows = unpack(read_blob(state_dir, old["lower_basis_blob"]), 6056, rank)
        lift_rows = unpack(read_blob(state_dir, old["lifted_grade_blob"]), 72576, rank)
        ci = old["character_index"]
        for index in range(rank):
            physical_lower, physical_grade = independent_aggregate_old(context, ci, lower_rows[index], lift_rows[index])
            work_lower, work_grade = physical_lower.copy(), physical_grade.copy()
            while np.any(work_lower):
                lead = int(np.flatnonzero(work_lower)[0])
                if lead not in lower_basis:
                    inv = 1 if work_lower[lead] == 1 else 2
                    lower_basis[lead] = ((inv * work_lower) % 3, (inv * work_grade) % 3)
                    break
                coefficient = int(work_lower[lead])
                work_lower = (work_lower.astype(np.int16) - coefficient * lower_basis[lead][0].astype(np.int16)) % 3
                work_grade = (work_grade.astype(np.int16) - coefficient * lower_basis[lead][1].astype(np.int16)) % 3
            if not np.any(work_lower):
                insist(int(np.dot(work_grade.astype(np.int64), dual.astype(np.int64)) % 3) == 0, "dual_old_connection")


def independent_aggregate_old(context: IndependentContext, character_index: int, lower_row: np.ndarray, grade_flat: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # The checker reconstructs the exact prefix action from raw Fourier
    # coordinates.  This is deliberately separate from producer helpers.
    transports = transport_labels(context)
    lower = np.zeros(8068, dtype=np.uint8)
    grade = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    source_label = CHARS[character_index]
    grade_blocks = grade_flat.reshape(4, SOURCE_WIDTH)
    for source_ci, label in enumerate(CHARS):
        for tag, block, sign in context.aggregation:
            shift = context.shifts[tag]
            mapping = context.left_map(shift[0])
            target_label = transports[tag][label]
            target_ci = CHARS.index(target_label)
            scalar = sign * character(target_label, shift[1], shift[2])
            for component in (0,1):
                if source_ci == character_index:
                    source0 = (tag*2+component)*504
                    destination0 = ((target_ci*2+block)*2+component)*504
                    lower[destination0+mapping] = (lower[destination0+mapping] + scalar*lower_row[source0:source0+504])%3
                for monomial in range(3):
                    source1=((tag*2+component)*3+monomial)*504
                    destination1=(((target_ci*2+block)*2+component)*3+monomial)*504
                    grade[destination1+mapping]=(grade[destination1+mapping]+scalar*grade_blocks[source_ci,source1:source1+504])%3
                    if source_ci == character_index and shift[3][monomial]:
                        output_label=(target_label[0]^ETA[monomial][0],target_label[1]^ETA[monomial][1]); output_ci=CHARS.index(output_label)
                        destination2=(((output_ci*2+block)*2+component)*3+monomial)*504
                        scale=sign*shift[3][monomial]*character(output_label,shift[1],shift[2])
                        grade[destination2+mapping]=(grade[destination2+mapping]+scale*lower_row[source0:source0+504])%3
    for tag, block, sign in context.aggregation:
        lower[8064+block]=(int(lower[8064+block])+sign*int(lower_row[6048+tag]))%3
    lower[8066:]=lower_row[6054:6056]
    return lower, grade


def fixture() -> dict[str, Any]:
    # No producer import: frozen literal shape, projector algebra, packed
    # encoding, and a single acceptance predicate are exercised here.
    receipts = pins()
    old = json.loads((ROOT / "search/certs/d972_r07_a0_c2fourier_joint_floor_v1.json").read_text(encoding="utf-8"))["source_ancestry"]["full_literal_terms"]
    canonical = canonical_terms(old)
    insist(len(old) == 3936 and len(canonical) == 2622, "fixture_canonical")
    for left in CHARS:
        for right in CHARS:
            total = sum(character(left, a, b) * character(right, a, b) for a, b in CHARS) % 3
            insist(total == (1 if left == right else 0), "fixture_projector")
    context = IndependentContext()
    action_lower = np.zeros((4, 6048), dtype=np.uint8)
    action_grade = np.zeros((4, SOURCE_WIDTH), dtype=np.uint8)
    for source_index, source_label in enumerate(CHARS):
        coefficient = character(source_label, 1, 0)
        action_lower[source_index, source_lower_coord(0, 0, 1)] = coefficient
        action_grade[source_index, source_grade_coord(0, 0, 0, 1)] = coefficient
    actor = context.actor_tags[-2][0]
    direct_value = product(actor, (context.elements[1], 1, 0, (1, 0, 0)))
    acted_grade = act_source_pair(
        context,
        action_lower,
        action_grade,
        np.zeros(8, dtype=np.uint8),
        context.actor_source[-2],
        context.actor_tags[-2],
    )[1]
    isolated_rows: list[list[tuple[int, Aff, int]]] = [[] for _ in range(6)]
    isolated_rows[0] = [(0, (context.elements[1], 1, 0, (1, 0, 0)), 1)]
    direct_column = column((isolated_rows, [0] * 6, (0, 0)), (-2,), context)
    direct_coordinate = pcoord(1, 0, 0, 1, 14)
    insist(
        context.index[direct_value[0]] == 14
        and direct_value[1:] == (1, 1, (2, 1, 2))
        and int(acted_grade[1, source_grade_coord(0, 0, 0, 14)]) == 1
        and direct_column.get(direct_coordinate) == 1,
        "fixture_v443_actor_accumulation",
    )
    row = np.asarray([0,1,2,0,2,0,1,0], dtype=np.uint8)
    packed = np.sum(row.reshape(-1,4).astype(np.uint16)*WEIGHTS,axis=1).astype(np.uint8).tobytes()
    insist(np.array_equal(unpack(packed,8,1)[0],row), "fixture_pack")
    mutations = 0
    for mutation in ([[0, [], 1]], [[1, [3], 1]], [[1, [], 0]]):
        try:
            canonical_terms(mutation)
        except RuntimeError:
            mutations += 1
    insist(mutations == 3, "fixture_mutations")
    truncated_rejected = False
    try:
        validate_nonmember_block_roster(
            {"defect_origins": [{"id": 0}]},
            {
                "rank": 0,
                "origin_count": 1,
                "origin_reductions": [],
                "actor_transitions": [],
                "dag_nodes": [],
            },
        )
    except RuntimeError as error:
        truncated_rejected = str(error) == "origin_reduction_count"
    insist(truncated_rejected, "fixture_truncated_origin_reduction")
    return {"fixture":"PASS","raw_terms":3936,"canonical_terms":2622,"projectors":16,"mutations_rejected":3,"v443_actor_accumulation":"PASS","pinned_inputs":len(receipts),"truncated_origin_reduction":"REJECTED"}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument("--fixture", action="store_true")
    modes.add_argument("--state-dir", type=Path)
    return p


def main() -> int:
    args = parser().parse_args()
    result = fixture() if args.fixture else verify_certificate(args.state_dir.resolve())
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
