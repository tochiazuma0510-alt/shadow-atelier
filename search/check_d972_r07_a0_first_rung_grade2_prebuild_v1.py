#!/usr/bin/env python3
"""Independent checker for Task565's grade-two module prebuild.

This file does not import the producer.  It implements its own canonical
state reader, base-3 packing, degree-two polynomial arithmetic, affine actor
and legal-projector replay.  The public checker accepts only the target-
independent MODULE_READY terminal; it never decides membership.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

import numpy as np

import d972_r07_a0_c2fourier_joint_floor_v1 as floor


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972.r07.a0.first-rung-grade2-prebuild.v1"
STATE_SCHEMA = SCHEMA + ".state"
GRADE1_STATE_SCHEMA = "d972.r07.a0.first-rung-grade1.v3.state"
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
ACTORS = (1, -1, 2, -2)
PURE_WORDS = {
    (0, 0): (),
    (0, 1): (-2, -2, -2, -2, -2, -2, -2, -2, -2),
    (1, 0): (-2, -2, 1, 1, 2, 1, 2, 1, 1),
    (1, 1): (-2, -2, -2, -1, -2, -1, -1, -1, -2, -1),
}
MONOMIALS = (
    (0, 0, 0),
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (2, 0, 0), (1, 1, 0), (1, 0, 1),
    (0, 2, 0), (0, 1, 1), (0, 0, 2),
)
DEGREE2_MONOMIALS = MONOMIALS[4:]
MONOMIAL_INDEX = {value: index for index, value in enumerate(MONOMIALS)}
ETA = ((0, 1), (1, 0), (1, 1))
SOURCE0C = 6048
SOURCE1C = 18144
SOURCE2C = 36288
SOURCE0 = 24192
SOURCE1 = 72576
SOURCE2 = 145152
SOURCE_P1 = 96776
PHYSICAL0 = 8064
PHYSICAL1 = 24192
PHYSICAL2 = 48384
PHYSICAL_LOWER = 32260
PACK_ENCODING = "base3-four-trits-per-byte"

PREBUILD_PINS = {
    "sol/proof_r07_grade1_to_grade2_split_presentation_handoff_v450.md": "48acc55a73aba140aa73098791d73f936f1b46fc5316d6f56e668be242fdc630",
    "sol/luna_task_565_r07_a0_first_rung_grade2_prebuild_v1.md": "0c0c32831a5fbd055ba158b8f6b1c429aa51a4cdfe1d781e912a2eba016ebef3",
    "sol/proof_r07_first_rung_six_grade_character_schedule_v448.md": "168e3fc5ab38520faf8ed5d107013f1f8b53f22d2907032519b86b6e0f01182d",
    "sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md": "3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4",
    "sol/sol_reply_566_audit_r07_grade1_to_grade2_handoff_v1.md": "b8c04819a27906cfaa88534627c147307e1fb7b9429e1f1246fc518b72f2297a",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def add(destination: np.ndarray, source: np.ndarray, scalar: int = 1) -> None:
    scalar %= 3
    if scalar:
        destination[:] = (destination.astype(np.uint16) + scalar * source.astype(np.uint16)) % 3


def claim_flags() -> dict[str, bool]:
    return {
        "ORDER_54432": False, "FULL_Q0": False, "A0": False,
        "COMMON": False, "COFINAL_LIFT": False, "FAKE": False,
        "IHARA": False, "verified": False,
    }


def dimensions() -> dict[str, Any]:
    return {
        "characters": 4,
        "character_labels": [list(value) for value in CHARACTERS],
        "degree2_monomials": [list(value) for value in DEGREE2_MONOMIALS],
        "monomials_coupled": True,
        "source_degree0": SOURCE0,
        "source_degree1": SOURCE1,
        "source_degree2_per_character": SOURCE2C,
        "source_degree2_total": SOURCE2,
        "source_precision1_with_auxiliary": SOURCE_P1,
        "physical_degree0": PHYSICAL0,
        "physical_degree1": PHYSICAL1,
        "physical_lower_with_auxiliary": PHYSICAL_LOWER,
        "physical_degree2": PHYSICAL2,
        "packed_degree2_residual_bytes": 12096,
    }


def read_state(
    state_dir: Path, stem: str, parent: str | None, schema: str = STATE_SCHEMA
) -> tuple[dict[str, Any], str]:
    head_bytes = (state_dir / f"{stem}.HEAD").read_bytes()
    head = json.loads(head_bytes)
    if (
        canonical(head) != head_bytes
        or set(head) != {"schema", "stem", "body_sha256", "parent_sha256"}
        or head.get("schema") != schema + ".head"
        or head.get("stem") != stem
        or head.get("parent_sha256") != parent
        or re.fullmatch(r"[0-9a-f]{64}", head.get("body_sha256", "")) is None
    ):
        raise RuntimeError(f"head:{stem}")
    digest = head["body_sha256"]
    data = (state_dir / f"{stem}.{digest}.json").read_bytes()
    if sha(data) != digest:
        raise RuntimeError(f"body_hash:{stem}")
    body = json.loads(data)
    if canonical(body) != data or body.get("schema") != schema:
        raise RuntimeError(f"body_canonical:{stem}")
    return body, digest


def read_blob(state_dir: Path, receipt: Any, rows: int, width: int) -> Path:
    if not plain_int(rows) or not plain_int(width) or rows < 0 or width <= 0 or width % 4:
        raise RuntimeError("blob_expected_shape")
    expected = rows * (width // 4)
    if not isinstance(receipt, dict) or set(receipt) != {"file", "bytes", "sha256", "rows", "width", "encoding"}:
        raise RuntimeError("blob_receipt")
    name = receipt.get("file")
    digest = receipt.get("sha256")
    if (
        not isinstance(name, str) or Path(name).name != name
        or re.fullmatch(r"[0-9a-f]{64}", digest or "") is None
        or not name.endswith(f".{digest}.bin")
        or receipt.get("bytes") != expected
        or receipt.get("rows") != rows
        or receipt.get("width") != width
        or receipt.get("encoding") != PACK_ENCODING
    ):
        raise RuntimeError("blob_semantics")
    path = state_dir / name
    before = path.stat()
    if before.st_size != expected:
        raise RuntimeError("blob_size")
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    after = path.stat()
    if (
        hasher.hexdigest() != digest
        or before.st_size != after.st_size or before.st_mtime_ns != after.st_mtime_ns
    ):
        raise RuntimeError("blob_authentication")
    return path


TRIT_DECODE = np.asarray(
    [[(value // (3 ** position)) % 3 for position in range(4)] for value in range(81)],
    dtype=np.uint8,
)
TRIT_WEIGHTS = np.asarray((1, 3, 9, 27), dtype=np.uint16)


def unpack(data: np.ndarray, width: int) -> np.ndarray:
    packed = np.asarray(data, dtype=np.uint8).reshape(-1)
    if packed.size * 4 != width or np.any(packed > 80):
        raise RuntimeError("packed_row")
    return TRIT_DECODE[packed].reshape(-1).copy()


def pack(row: np.ndarray) -> bytes:
    flat = np.asarray(row, dtype=np.uint8).reshape(-1)
    if flat.size % 4 or np.any(flat > 2):
        raise RuntimeError("dense_row")
    return np.sum(flat.reshape(-1, 4).astype(np.uint16) * TRIT_WEIGHTS, axis=1).astype(np.uint8).tobytes()


def matrix(data: bytes, rows: int, width: int) -> list[np.ndarray]:
    packed = np.frombuffer(data, dtype=np.uint8).reshape(rows, width // 4)
    return [unpack(packed[index], width) for index in range(rows)]


def cv(label: tuple[int, int], parity: tuple[int, int]) -> int:
    return 1 if ((label[0] * parity[0] + label[1] * parity[1]) & 1) == 0 else 2


def sign_kernel(parity: tuple[int, int], value: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((cv(ETA[index], parity) * value[index]) % 3 for index in range(3))  # type: ignore[return-value]


Affine = tuple[tuple[int, ...], int, int, tuple[int, int, int]]


def affine_mul(left: Affine, right: Affine) -> Affine:
    acted = sign_kernel((right[1], right[2]), left[3])
    return (
        floor.M(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2],
        tuple((acted[index] + right[3][index]) % 3 for index in range(3)),
    )  # type: ignore[return-value]


def affine_inv(value: Affine) -> Affine:
    acted = sign_kernel((value[1], value[2]), value[3])
    return floor.inv(value[0]), value[1], value[2], tuple((-entry) % 3 for entry in acted)  # type: ignore[return-value]


def affine_eval(word: Iterable[int], images: tuple[Affine, Affine]) -> Affine:
    result: Affine = (floor.ID9, 0, 0, (0, 0, 0))
    inverses = affine_inv(images[0]), affine_inv(images[1])
    for letter in word:
        result = affine_mul(result, images[abs(letter) - 1] if letter > 0 else inverses[abs(letter) - 1])
    return result


def affine_fox(word: Iterable[int], images: tuple[Affine, Affine]) -> tuple[dict[tuple[int, Affine], int], Affine]:
    output: dict[tuple[int, Affine], int] = {}
    prefix: Affine = (floor.ID9, 0, 0, (0, 0, 0))
    inverses = affine_inv(images[0]), affine_inv(images[1])
    for letter in word:
        generator = abs(letter) - 1
        if letter > 0:
            key = generator, prefix
            output[key] = (output.get(key, 0) + 1) % 3
            prefix = affine_mul(prefix, images[generator])
        else:
            prefix = affine_mul(prefix, inverses[generator])
            key = generator, prefix
            output[key] = (output.get(key, 0) - 1) % 3
        if output.get(key) == 0:
            output.pop(key, None)
    return output, prefix


def matrix2_mul(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (left[0][0] * right[0][0] ^ left[0][1] * right[1][0], left[0][0] * right[0][1] ^ left[0][1] * right[1][1]),
        (left[1][0] * right[0][0] ^ left[1][1] * right[1][0], left[1][0] * right[0][1] ^ left[1][1] * right[1][1]),
    )


class Context:
    def __init__(self, words: dict[str, Any]):
        text = (ROOT / "scratchpad/fuda1_a0_rmax_data.g").read_text(encoding="utf-8")
        match = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;", text, re.S)
        if match is None:
            raise RuntimeError("marking")
        q36 = tuple(tuple(value - 1 for value in ast.literal_eval(match.group(index))) for index in (1, 2))
        self.a, self.c = q36[0][:9], q36[1][:9]
        self.psels, self.psidx = floor.group((self.a, self.c))
        if len(self.psels) != 504:
            raise RuntimeError("psl_order")
        floor.psels, floor.psidx = self.psels, self.psidx
        self.q1_images = ((self.a, 1, 0), (self.c, 0, 1))
        floor.qb = floor.qinv(floor.qmul(self.q1_images[1], self.q1_images[0]))
        self.images: tuple[Affine, Affine] = (
            (self.a, 1, 0, (1, 0, 0)),
            (self.c, 0, 1, (1, 1, 1)),
        )
        self.pb3_b = affine_inv(affine_mul(self.images[1], self.images[0]))
        self.transport: list[dict[tuple[int, int], tuple[int, int]]] = []
        for left_word, right_word in floor.OO:
            left = floor.qev(left_word, self.q1_images)
            right = floor.qev(right_word, self.q1_images)
            action = ((left[1], right[1]), (left[2], right[2]))
            inverse = None
            for aa in range(2):
                for ab in range(2):
                    for ba in range(2):
                        for bb in range(2):
                            candidate = ((aa, ab), (ba, bb))
                            if matrix2_mul(action, candidate) == ((1, 0), (0, 1)) and matrix2_mul(candidate, action) == ((1, 0), (0, 1)):
                                inverse = candidate
            if inverse is None:
                raise RuntimeError("transport")
            self.transport.append({
                label: (
                    label[0] * inverse[0][0] ^ label[1] * inverse[1][0],
                    label[0] * inverse[0][1] ^ label[1] * inverse[1][1],
                ) for label in CHARACTERS
            })
        self.actor_tags = {
            letter: tuple(affine_eval(floor.sub((letter,), *pair), self.images) for pair in floor.OO)
            for letter in ACTORS
        }
        self.pure_tags = {
            parity: tuple(affine_eval(floor.sub(PURE_WORDS[parity], *pair), self.images) for pair in floor.OO)
            for parity in CHARACTERS
        }
        g760 = tuple(int(value) for value in words["g760"])
        tags = tuple(affine_eval(floor.sub(g760, *pair), self.images) for pair in floor.OO)
        self.shifts = (
            (floor.ID9, 0, 0, (0, 0, 0)), tags[2], tags[2],
            affine_mul(tags[5], affine_inv(tags[4])), tags[5], tags[5],
        )
        self.aggregate_table = ((0, 0, 1), (1, 0, 2), (2, 0, 1), (3, 1, 2), (4, 1, 2), (5, 1, 1))
        self.maps: dict[tuple[int, ...], np.ndarray] = {}

    def pmap(self, permutation: tuple[int, ...]) -> np.ndarray:
        if permutation not in self.maps:
            self.maps[permutation] = np.asarray([self.psidx[floor.M(permutation, value)] for value in self.psels], dtype=np.int32)
        return self.maps[permutation]

    def word_tags(self, word: tuple[int, ...]) -> tuple[Affine, ...]:
        return tuple(affine_eval(floor.sub(word, *pair), self.images) for pair in floor.OO)


def multiply_monomial(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int] | None:
    value = tuple(left[index] + right[index] for index in range(3))
    if any(entry > 2 for entry in value) or sum(value) > 2:
        return None
    return value  # type: ignore[return-value]


PRODUCT = [[-1] * 10 for _ in range(10)]
for _i, _left in enumerate(MONOMIALS):
    for _j, _right in enumerate(MONOMIALS):
        _value = multiply_monomial(_left, _right)
        if _value is not None:
            PRODUCT[_i][_j] = MONOMIAL_INDEX[_value]


def poly_mul(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    output = np.zeros(10, dtype=np.uint8)
    for i in np.flatnonzero(left):
        for j in np.flatnonzero(right):
            target = PRODUCT[int(i)][int(j)]
            if target >= 0:
                output[target] = (int(output[target]) + int(left[i]) * int(right[j])) % 3
    return output


def e_poly(vector: tuple[int, int, int]) -> np.ndarray:
    output = np.zeros(10, dtype=np.uint8)
    output[0] = 1
    for variable, exponent0 in enumerate(vector):
        exponent = exponent0 % 3
        factor = np.zeros(10, dtype=np.uint8)
        factor[0] = 1
        if exponent:
            mono = [0, 0, 0]
            mono[variable] = 1
            factor[MONOMIAL_INDEX[tuple(mono)]] = exponent
        if exponent == 2:
            mono = [0, 0, 0]
            mono[variable] = 2
            factor[MONOMIAL_INDEX[tuple(mono)]] = 1
        output = poly_mul(output, factor)
    return output


def poly_rows_mul(factor: np.ndarray, rows: np.ndarray) -> np.ndarray:
    output = np.zeros_like(rows)
    for left in np.flatnonzero(factor):
        for right in range(10):
            target = PRODUCT[int(left)][right]
            if target >= 0:
                add(output[:, target], rows[:, right], int(factor[left]))
    return output


def lower_coord(tag: int, component: int, psl: int) -> int:
    return (tag * 2 + component) * 504 + psl


def grade1_coord(tag: int, component: int, monomial: int, psl: int) -> int:
    return ((tag * 2 + component) * 3 + monomial) * 504 + psl


def source_view(d0: np.ndarray, d1: np.ndarray, d2: np.ndarray, character: int, tag: int) -> np.ndarray:
    output = np.zeros((2, 10, 504), dtype=np.uint8)
    for component in (0, 1):
        begin = lower_coord(tag, component, 0)
        output[component, 0] = d0[character, begin:begin + 504]
        for monomial in range(3):
            begin = grade1_coord(tag, component, monomial, 0)
            output[component, 1 + monomial] = d1[character, begin:begin + 504]
        for monomial in range(6):
            begin = ((tag * 2 + component) * 6 + monomial) * 504
            output[component, 4 + monomial] = d2[character, begin:begin + 504]
    return output


def install_view(d0: np.ndarray, d1: np.ndarray, d2: np.ndarray, character: int, tag: int, value: np.ndarray) -> None:
    for component in (0, 1):
        begin = lower_coord(tag, component, 0)
        d0[character, begin:begin + 504] = value[component, 0]
        for monomial in range(3):
            begin = grade1_coord(tag, component, monomial, 0)
            d1[character, begin:begin + 504] = value[component, 1 + monomial]
        for monomial in range(6):
            begin = ((tag * 2 + component) * 6 + monomial) * 504
            d2[character, begin:begin + 504] = value[component, 4 + monomial]


def act(context: Context, row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], tag_actors: tuple[Affine, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d0, d1, d2, auxiliary = row
    output = (np.zeros_like(d0), np.zeros_like(d1), np.zeros_like(d2), auxiliary.copy())
    for tag, actor in enumerate(tag_actors):
        raw = np.zeros((4, 2, 10, 504), dtype=np.uint8)
        for parity_index, parity in enumerate(CHARACTERS):
            for source_index, source_label in enumerate(CHARACTERS):
                add(raw[parity_index], source_view(d0, d1, d2, source_index, tag), cv(context.transport[tag][source_label], parity))
        acted = np.zeros_like(raw)
        pmap = context.pmap(actor[0])
        for parity_index, parity in enumerate(CHARACTERS):
            target = (parity[0] ^ actor[1], parity[1] ^ actor[2])
            product = poly_rows_mul(e_poly(sign_kernel(parity, actor[3])), raw[parity_index])
            translated = np.zeros_like(product)
            translated[:, :, pmap] = product
            add(acted[CHARACTERS.index(target)], translated)
        for source_index, source_label in enumerate(CHARACTERS):
            value = np.zeros((2, 10, 504), dtype=np.uint8)
            tag_label = context.transport[tag][source_label]
            for parity_index, parity in enumerate(CHARACTERS):
                add(value, acted[parity_index], cv(tag_label, parity))
            install_view(output[0], output[1], output[2], source_index, tag, value)
    return output


def word_action(context: Context, row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], word: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return act(context, row, context.word_tags(word))


def associated_actor(context: Context, row: np.ndarray, character: int, letter: int) -> np.ndarray:
    output = np.zeros_like(row)
    label = CHARACTERS[character]
    source_q1 = floor.qev((letter,), context.q1_images)
    scalar = cv(label, (source_q1[1], source_q1[2]))
    for tag, actor in enumerate(context.actor_tags[letter]):
        pmap = context.pmap(actor[0])
        for component in (0, 1):
            for monomial in range(6):
                begin = ((tag * 2 + component) * 6 + monomial) * 504
                output[begin:begin + 504][pmap] = scalar * row[begin:begin + 504] % 3
    return output


def pure_project(context: Context, d2: np.ndarray, label: tuple[int, int]) -> np.ndarray:
    output = np.zeros_like(d2)
    zero0 = np.zeros((4, SOURCE0C), dtype=np.uint8)
    zero1 = np.zeros((4, SOURCE1C), dtype=np.uint8)
    zero_aux = np.zeros(8, dtype=np.uint8)
    row = (zero0, zero1, d2, zero_aux)
    for parity in CHARACTERS:
        acted = act(context, row, context.pure_tags[parity])
        add(output, acted[2], cv(label, parity))
    return output


def qnorm(word: tuple[int, ...], context: Context) -> tuple[list[tuple[int, Affine, int]], int]:
    gradient, endpoint = affine_fox(word, context.images)
    identity: Affine = (floor.ID9, 0, 0, (0, 0, 0))
    if endpoint != identity:
        raise RuntimeError("seed_endpoint")
    output: dict[tuple[int, Affine], int] = {}
    augmentation = 0
    for (generator, prefix), coefficient in gradient.items():
        if generator == 0:
            augmentation = (augmentation + coefficient) % 3
            first = affine_mul(prefix, context.images[0])
            second = affine_mul(first, context.pb3_b)
            for component, value in ((0, first), (1, second)):
                key = component, value
                output[key] = (output.get(key, 0) - coefficient) % 3
        else:
            key = 1, prefix
            output[key] = (output.get(key, 0) + coefficient) % 3
    return [(component, value, coefficient) for (component, value), coefficient in output.items() if coefficient], augmentation


def evaluate_seed(context: Context, word: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d0 = np.zeros((4, SOURCE0C), dtype=np.uint8)
    d1 = np.zeros((4, SOURCE1C), dtype=np.uint8)
    d2 = np.zeros((4, SOURCE2C), dtype=np.uint8)
    auxiliary = np.zeros(8, dtype=np.uint8)
    for tag, pair in enumerate(floor.OO):
        normal, augmentation = qnorm(tuple(floor.sub(word, *pair)), context)
        auxiliary[tag] = augmentation
        for component, value, coefficient in normal:
            polynomial = e_poly(value[3])
            psl = context.psidx[value[0]]
            for character, label in enumerate(CHARACTERS):
                weight = coefficient * cv(context.transport[tag][label], (value[1], value[2]))
                d0[character, lower_coord(tag, component, psl)] = (int(d0[character, lower_coord(tag, component, psl)]) + weight * int(polynomial[0])) % 3
                for monomial in range(3):
                    coordinate = grade1_coord(tag, component, monomial, psl)
                    d1[character, coordinate] = (int(d1[character, coordinate]) + weight * int(polynomial[1 + monomial])) % 3
                for monomial in range(6):
                    coordinate = ((tag * 2 + component) * 6 + monomial) * 504 + psl
                    d2[character, coordinate] = (int(d2[character, coordinate]) + weight * int(polynomial[4 + monomial])) % 3
    exponent = floor.exps(word)
    if exponent[0] % 18 or exponent[1] % 18:
        raise RuntimeError("integral_exponent")
    auxiliary[6:] = (exponent[0] // 18 % 3, exponent[1] // 18 % 3)
    return d0, d1, d2, auxiliary


def split_p1(row: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return row[:SOURCE0].reshape(4, SOURCE0C), row[SOURCE0:SOURCE0 + SOURCE1].reshape(4, SOURCE1C), row[-8:]


def flat_p1(row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]) -> np.ndarray:
    return np.concatenate((row[0].reshape(-1), row[1].reshape(-1), row[3]))


def combine(rows: list[np.ndarray], expression: list[list[int]], width: int) -> np.ndarray:
    output = np.zeros(width, dtype=np.uint8)
    for index, coefficient in expression:
        add(output, rows[index], coefficient)
    return output


def normalize_expression(entries: Iterable[Iterable[int]]) -> list[list[int]]:
    values: dict[int, int] = {}
    for index, coefficient in entries:
        values[int(index)] = (values.get(int(index), 0) + int(coefficient)) % 3
    return [[index, values[index]] for index in sorted(values) if values[index]]


def aggregate(context: Context, row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d0, d1, d2, auxiliary = row
    output = np.zeros((4, 2, 2, 10, 504), dtype=np.uint8)
    for tag, block, sign in context.aggregate_table:
        raw = np.zeros((4, 2, 10, 504), dtype=np.uint8)
        for parity_index, parity in enumerate(CHARACTERS):
            for source_index, source_label in enumerate(CHARACTERS):
                add(raw[parity_index], source_view(d0, d1, d2, source_index, tag), cv(context.transport[tag][source_label], parity))
        shift = context.shifts[tag]
        acted = np.zeros_like(raw)
        pmap = context.pmap(shift[0])
        for parity_index, parity in enumerate(CHARACTERS):
            target = (parity[0] ^ shift[1], parity[1] ^ shift[2])
            value = poly_rows_mul(e_poly(sign_kernel(parity, shift[3])), raw[parity_index])
            translated = np.zeros_like(value)
            translated[:, :, pmap] = value
            add(acted[CHARACTERS.index(target)], translated)
        for character, label in enumerate(CHARACTERS):
            value = np.zeros((2, 10, 504), dtype=np.uint8)
            for parity_index, parity in enumerate(CHARACTERS):
                add(value, acted[parity_index], sign * cv(label, parity))
            add(output[character, block], value)
    physical0 = np.zeros(PHYSICAL0, dtype=np.uint8)
    physical1 = np.zeros(PHYSICAL1, dtype=np.uint8)
    physical2 = np.zeros(PHYSICAL2, dtype=np.uint8)
    for character in range(4):
        for block in range(2):
            for component in (0, 1):
                begin0 = ((character * 2 + block) * 2 + component) * 504
                physical0[begin0:begin0 + 504] = output[character, block, component, 0]
                for monomial in range(3):
                    begin1 = (((character * 2 + block) * 2 + component) * 3 + monomial) * 504
                    physical1[begin1:begin1 + 504] = output[character, block, component, 1 + monomial]
                for monomial in range(6):
                    begin2 = (((character * 2 + block) * 2 + component) * 6 + monomial) * 504
                    physical2[begin2:begin2 + 504] = output[character, block, component, 4 + monomial]
    physical_aux = np.zeros(4, dtype=np.uint8)
    for tag, block, sign in context.aggregate_table:
        physical_aux[block] = (int(physical_aux[block]) + sign * int(auxiliary[tag])) % 3
    physical_aux[2:] = auxiliary[6:]
    return physical0, physical1, physical2, physical_aux


def full_project(context: Context, row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], label: tuple[int, int]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    output = tuple(np.zeros_like(part) for part in row)
    for parity in CHARACTERS:
        acted = act(context, row, context.pure_tags[parity])
        for destination, source in zip(output, acted):
            add(destination, source, cv(label, parity))
    return output  # type: ignore[return-value]


def add_full(destination: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], source: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], scalar: int) -> None:
    for left, right in zip(destination, source):
        add(left, right, scalar)


def scaled_full(row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], scalar: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return tuple(((scalar * part.astype(np.uint16)) % 3).astype(np.uint8) for part in row)  # type: ignore[return-value]


def full_from_rows(p1_rows: list[np.ndarray], d2_rows: list[np.ndarray], index: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d0, d1, auxiliary = split_p1(p1_rows[index])
    return d0, d1, d2_rows[index].reshape(4, SOURCE2C), auxiliary


def combine_full(p1_rows: list[np.ndarray], d2_rows: list[np.ndarray], expression: list[list[int]]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    p1 = combine(p1_rows, expression, SOURCE_P1)
    d0, d1, auxiliary = split_p1(p1)
    d2 = combine(d2_rows, expression, SOURCE2).reshape(4, SOURCE2C)
    return d0, d1, d2, auxiliary


GRADE1_MANIFEST_PATHS = {
    "sol/proof_r07_a0_relative_fibre_echelon_lift_v441.md",
    "sol/sol_reply_544_audit_r07_a0_relative_fibre_echelon_v1.md",
    "sol/proof_r07_a0_explicit_g9_two_rung_twisting_v442.md",
    "sol/sol_reply_548_audit_r07_a0_explicit_g9_two_rung_twisting_v1.md",
    "sol/proof_r07_a0_affine_truncated_two_rung_engine_v443.md",
    "sol/proof_r07_filtered_transition_defect_closure_v444.md",
    "sol/sol_reply_550_audit_r07_a0_affine_engine_transition_defects_v1.md",
    "sol/proof_r07_first_rung_character_blocks_coupled_monomials_v446.md",
    "sol/sol_reply_553_audit_r07_a0_character_blocks_coupled_monomials_v1.md",
    "sol/sol_reply_549_audit_r07_a0_order2016_literal_member_v1.md",
    "sol/sol_reply_547_audit_r07_a0_psl504_canonical_payload_v1.md",
    "search/certs/d972_r07_a0_c2fourier_joint_floor_v1.json",
    "search/d972_r07_a0_c2fourier_joint_floor_v1.py",
    "scratchpad/a0_paper_words_v1.json",
    "scratchpad/fuda1_a0_rmax_data.g",
    "sol/proof_r07_first_rung_character_projector_word_repair_v447.md",
    "sol/proof_r07_first_rung_six_grade_index_repair_v449.md",
    "sol/sol_reply_555_audit_r07_a0_six_grade_schedule_v1.md",
}


def authenticate_manifest(manifest: Any) -> None:
    if not isinstance(manifest, dict) or set(manifest) != GRADE1_MANIFEST_PATHS:
        raise RuntimeError("grade1_manifest_roster")
    for relative in sorted(manifest):
        receipt = manifest[relative]
        data = (ROOT / relative).read_bytes()
        if receipt != {"bytes": len(data), "sha256": sha(data)}:
            raise RuntimeError(f"grade1_manifest_entry:{relative}")


def authenticate_grade1(grade1_dir: Path) -> tuple[dict[str, Any], str, list[tuple[dict[str, Any], str]]]:
    prepare, prepare_digest = read_state(grade1_dir, "prepare", None, GRADE1_STATE_SCHEMA)
    manifest = prepare.get("input_manifest")
    authenticate_manifest(manifest)
    if prepare.get("input_manifest_sha256") != sha(canonical(manifest)):
        raise RuntimeError("grade1_manifest_digest")
    if (
        prepare.get("phase") != "prepare" or prepare.get("fixture") is not False
        or prepare.get("paired_lower_presentation_complete") is not True
        or prepare.get("dimensions", {}).get("character_labels") != [list(value) for value in CHARACTERS]
        or prepare.get("dimensions", {}).get("monomials") != [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    ):
        raise RuntimeError("grade1_prepare_semantics")
    blocks = [read_state(grade1_dir, f"block-{index}", prepare_digest, GRADE1_STATE_SCHEMA) for index in range(4)]
    origins = []
    cursor = 0
    for character, old in enumerate(prepare.get("old_blocks", [])):
        rank = old.get("rank")
        if not plain_int(rank) or rank < 0 or old.get("character_index") != character or old.get("character") != list(CHARACTERS[character]):
            raise RuntimeError("grade1_old")
        record = old.get("record")
        if (
            record.get("rank") != rank or record.get("attempts") != 44 + 4 * rank
            or record.get("actor_order") != list(ACTORS) or record.get("queue_exhausted") is not True
            or len(record.get("seed_reductions", [])) != 44
            or len(record.get("actor_transitions", [])) != rank
            or len(record.get("dag_nodes", [])) != rank
        ):
            raise RuntimeError("grade1_old_record")
        begin = cursor
        for seed in range(1, 45):
            origins.append({"id": len(origins), "kind": "seed", "lower_character": character, "seed": seed})
        for pivot in range(rank):
            for letter in ACTORS:
                origins.append({"id": len(origins), "kind": "transition", "lower_character": character, "pivot": pivot, "letter": letter})
        cursor = len(origins)
        if old.get("defect_origin_range") != [begin, cursor]:
            raise RuntimeError("grade1_origin_range")
    if len(prepare.get("old_blocks", [])) != 4 or prepare.get("defect_origins") != origins or prepare.get("defect_origin_sha256") != sha(canonical(origins)):
        raise RuntimeError("grade1_origin_roster")
    for character, ((block, _), packet) in enumerate(zip(blocks, prepare["packets"])):
        rank = block.get("rank")
        if (
            block.get("phase") != "block" or block.get("parent_sha256") != prepare_digest
            or block.get("character_index") != character or block.get("character") != list(CHARACTERS[character])
            or block.get("packet_sha256") != packet["blob"]["sha256"]
            or block.get("origin_count") != len(origins)
            or not plain_int(rank) or rank < 0
            or block.get("attempts") != len(origins) + 4 * rank
            or block.get("queue_exhausted") is not True or block.get("actor_order") != list(ACTORS)
            or len(block.get("origin_reductions", [])) != len(origins)
            or len(block.get("actor_transitions", [])) != rank
            or len(block.get("dag_nodes", [])) != rank
        ):
            raise RuntimeError("grade1_block")
    return prepare, prepare_digest, blocks


def expected_relations(prepare: dict[str, Any], blocks: list[tuple[dict[str, Any], str]]) -> tuple[list[list[list[int]]], list[list[list[list[int]]]], list[int], list[int]]:
    old_offsets = []
    cursor = 0
    for old in prepare["old_blocks"]:
        old_offsets.append(cursor)
        cursor += old["rank"]
    new_offsets = []
    for block, _ in blocks:
        new_offsets.append(cursor)
        cursor += block["rank"]
    seeds = []
    for seed in range(44):
        entries = []
        for character, old in enumerate(prepare["old_blocks"]):
            for pivot, coefficient in old["record"]["seed_reductions"][seed]:
                entries.append([old_offsets[character] + pivot, coefficient])
            origin = old["defect_origin_range"][0] + seed
            for target, (block, _) in enumerate(blocks):
                for pivot, coefficient in block["origin_reductions"][origin]:
                    entries.append([new_offsets[target] + pivot, coefficient])
        seeds.append(normalize_expression(entries))
    transitions = []
    for character, old in enumerate(prepare["old_blocks"]):
        for pivot in range(old["rank"]):
            row = []
            for actor_index in range(4):
                entries = []
                for target, coefficient in old["record"]["actor_transitions"][pivot][actor_index]:
                    entries.append([old_offsets[character] + target, coefficient])
                origin = old["defect_origin_range"][0] + 44 + 4 * pivot + actor_index
                for block_character, (block, _) in enumerate(blocks):
                    for target, coefficient in block["origin_reductions"][origin]:
                        entries.append([new_offsets[block_character] + target, coefficient])
                row.append(normalize_expression(entries))
            transitions.append(row)
    for character, (block, _) in enumerate(blocks):
        for pivot in range(block["rank"]):
            transitions.append([
                normalize_expression([[new_offsets[character] + target, coefficient] for target, coefficient in expression])
                for expression in block["actor_transitions"][pivot]
            ])
    return seeds, transitions, old_offsets, new_offsets


class PackedMatrix:
    """Authenticated file-backed packed rows; dense rows are decoded on demand."""

    def __init__(self, path: Path, rows: int, width: int):
        self.rows = rows
        self.width = width
        packed_width = width // 4
        self.values = (
            np.memmap(path, dtype=np.uint8, mode="r", shape=(rows, packed_width))
            if rows
            else np.empty((0, packed_width), dtype=np.uint8)
        )

    def row(self, index: int) -> np.ndarray:
        if not 0 <= index < self.rows:
            raise RuntimeError("matrix_index")
        return unpack(self.values[index], self.width)


def combine_store(store: PackedMatrix, expression: list[list[int]]) -> np.ndarray:
    output = np.zeros(store.width, dtype=np.uint8)
    for index, coefficient in expression:
        add(output, store.row(index), coefficient)
    return output


def full_store(p1: PackedMatrix, d2: PackedMatrix, index: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    p1row = p1.row(index)
    d0, d1, auxiliary = split_p1(p1row)
    return d0, d1, d2.row(index).reshape(4, SOURCE2C), auxiliary


def combine_full_store(p1: PackedMatrix, d2: PackedMatrix, expression: list[list[int]]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    p1row = combine_store(p1, expression)
    d0, d1, auxiliary = split_p1(p1row)
    return d0, d1, combine_store(d2, expression).reshape(4, SOURCE2C), auxiliary


def subtract_full(left: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], right: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    output = tuple(part.copy() for part in left)
    add_full(output, right, -1)
    return output  # type: ignore[return-value]


def iter_expected_p1(
    grade1_dir: Path, prepare1: dict[str, Any], blocks1: list[tuple[dict[str, Any], str]]
) -> Iterable[np.ndarray]:
    for character, old in enumerate(prepare1["old_blocks"]):
        lower = PackedMatrix(read_blob(grade1_dir, old["lower_basis_blob"], old["rank"], 6056), old["rank"], 6056)
        lifted = PackedMatrix(read_blob(grade1_dir, old["lifted_grade_blob"], old["rank"], SOURCE1), old["rank"], SOURCE1)
        for pivot in range(old["rank"]):
            lower_row = lower.row(pivot)
            d0 = np.zeros((4, SOURCE0C), dtype=np.uint8)
            d0[character] = lower_row[:SOURCE0C]
            yield np.concatenate((d0.reshape(-1), lifted.row(pivot), lower_row[-8:]))
    for character, (block, _) in enumerate(blocks1):
        basis = PackedMatrix(read_blob(grade1_dir, block["basis_blob"], block["rank"], SOURCE1C), block["rank"], SOURCE1C)
        for pivot in range(block["rank"]):
            d0 = np.zeros(SOURCE0, dtype=np.uint8)
            d1 = np.zeros((4, SOURCE1C), dtype=np.uint8)
            d1[character] = basis.row(pivot)
            yield np.concatenate((d0, d1.reshape(-1), np.zeros(8, dtype=np.uint8)))


def verify_b1_and_packets(
    grade1_dir: Path,
    context: Context,
    words: dict[str, Any],
    prepare: dict[str, Any],
    prepare1: dict[str, Any],
    blocks1: list[tuple[dict[str, Any], str]],
    p1: PackedMatrix,
    d2: PackedMatrix,
    grade2_packets: list[PackedMatrix],
) -> None:
    presentation = prepare["b1_presentation"]
    rank = presentation["rank"]
    expected_seed_relations, expected_transitions, old_offsets, new_offsets = expected_relations(prepare1, blocks1)
    if presentation["seed_reductions"] != expected_seed_relations or presentation["actor_transitions"] != expected_transitions:
        raise RuntimeError("b1_global_relations")
    expected_count = 0
    for pivot, expected in enumerate(iter_expected_p1(grade1_dir, prepare1, blocks1)):
        if pivot >= rank:
            raise RuntimeError("b1_order")
        if not np.array_equal(expected, p1.row(pivot)):
            raise RuntimeError(f"b1_precision1_blob:{pivot}")
        expected_count += 1
    if expected_count != rank:
        raise RuntimeError("b1_order")
    seeds = [evaluate_seed(context, tuple(int(value) for value in relator)) for relator in words["relators"]]
    for seed, expression in enumerate(expected_seed_relations):
        if not np.array_equal(flat_p1(seeds[seed]), combine_store(p1, expression)):
            raise RuntimeError(f"b1_seed_identity:{seed + 1}")
    for pivot, actor_row in enumerate(expected_transitions):
        parent = full_store(p1, d2, pivot)
        zeroed = (parent[0], parent[1], np.zeros_like(parent[2]), parent[3])
        for actor_index, letter in enumerate(ACTORS):
            actual = act(context, zeroed, context.actor_tags[letter])
            if not np.array_equal(flat_p1(actual), combine_store(p1, actor_row[actor_index])):
                raise RuntimeError(f"b1_actor_identity:{pivot}:{letter}")
    projected_seeds = [[full_project(context, seed, label) for seed in seeds] for label in CHARACTERS]
    for seed in range(44):
        recovered = tuple(np.zeros_like(part) for part in seeds[seed])
        for character in range(4):
            add_full(recovered, projected_seeds[character][seed], 1)
        if any(not np.array_equal(recovered[index], seeds[seed][index]) for index in range(4)):
            raise RuntimeError(f"full_word_sum:{seed + 1}")
    # Replay every old and H1 DAG lift, including v451 (2.7).
    for character, old in enumerate(prepare1["old_blocks"]):
        for pivot, node in enumerate(old["record"]["dag_nodes"]):
            origin = node["origin"]
            if origin["kind"] == "projected_seed":
                work = tuple(part.copy() for part in projected_seeds[character][origin["seed"] - 1])
            else:
                work = act(context, full_store(p1, d2, old_offsets[character] + origin["parent"]), context.actor_tags[origin["letter"]])
            for earlier, coefficient in node["reductions"]:
                add_full(work, full_store(p1, d2, old_offsets[character] + earlier), -coefficient)
            if node["scale"] == 2:
                work = scaled_full(work, 2)
            global_pivot = old_offsets[character] + pivot
            if not np.array_equal(flat_p1(work), p1.row(global_pivot)) or not np.array_equal(work[2].reshape(-1), d2.row(global_pivot)):
                raise RuntimeError(f"old_lift_dag:{character}:{pivot}")

    def lifted_origin(origin: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        character = origin["lower_character"]
        old = prepare1["old_blocks"][character]
        if origin["kind"] == "seed":
            work = tuple(part.copy() for part in projected_seeds[character][origin["seed"] - 1])
            expression = old["record"]["seed_reductions"][origin["seed"] - 1]
        else:
            work = act(context, full_store(p1, d2, old_offsets[character] + origin["pivot"]), context.actor_tags[origin["letter"]])
            expression = old["record"]["actor_transitions"][origin["pivot"]][ACTORS.index(origin["letter"])]
        for pivot, coefficient in expression:
            add_full(work, full_store(p1, d2, old_offsets[character] + pivot), -coefficient)
        return work  # type: ignore[return-value]

    for character, (block, _) in enumerate(blocks1):
        grade1_packet = PackedMatrix(
            read_blob(
                grade1_dir, prepare1["packets"][character]["blob"],
                len(prepare1["defect_origins"]), SOURCE1C,
            ),
            len(prepare1["defect_origins"]), SOURCE1C,
        )
        for pivot, node in enumerate(block["dag_nodes"]):
            origin = node["origin"]
            if origin["kind"] == "defect":
                work = full_project(context, lifted_origin(prepare1["defect_origins"][origin["origin"]]), CHARACTERS[character])
                if not np.array_equal(work[1][character], grade1_packet.row(origin["origin"])):
                    raise RuntimeError(f"grade1_packet_binding:{character}:{origin['origin']}")
            else:
                work = act(context, full_store(p1, d2, new_offsets[character] + origin["parent"]), context.actor_tags[origin["letter"]])
            for earlier, coefficient in node["reductions"]:
                add_full(work, full_store(p1, d2, new_offsets[character] + earlier), -coefficient)
            if node["scale"] == 2:
                work = scaled_full(work, 2)
            global_pivot = new_offsets[character] + pivot
            if not np.array_equal(flat_p1(work), p1.row(global_pivot)) or not np.array_equal(work[2].reshape(-1), d2.row(global_pivot)):
                raise RuntimeError(f"h1_lift_dag:{character}:{pivot}")
    origin_index = 0

    def check_defect(defect: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]) -> None:
        nonlocal origin_index
        if np.any(defect[0]) or np.any(defect[1]) or np.any(defect[3]):
            raise RuntimeError(f"grade2_defect_lower:{origin_index}")
        recovered = np.zeros_like(defect[2])
        for character, label in enumerate(CHARACTERS):
            projected = pure_project(context, defect[2], label)
            if not np.array_equal(projected[character], grade2_packets[character].row(origin_index)) or any(np.any(projected[index]) for index in range(4) if index != character):
                raise RuntimeError(f"grade2_packet:{origin_index}:{character}")
            add(recovered, projected)
        if not np.array_equal(recovered, defect[2]):
            raise RuntimeError(f"grade2_packet_resolution:{origin_index}")
        origin_index += 1

    for seed, expression in enumerate(expected_seed_relations):
        check_defect(subtract_full(seeds[seed], combine_full_store(p1, d2, expression)))
    for pivot, actor_row in enumerate(expected_transitions):
        parent = full_store(p1, d2, pivot)
        for actor_index, letter in enumerate(ACTORS):
            check_defect(subtract_full(act(context, parent, context.actor_tags[letter]), combine_full_store(p1, d2, actor_row[actor_index])))
    if origin_index != 44 + 4 * rank:
        raise RuntimeError("grade2_origin_count")


def validate_prepare_structure(state_dir: Path, prepare: dict[str, Any]) -> tuple[PackedMatrix, PackedMatrix, list[PackedMatrix]]:
    for relative, expected in PREBUILD_PINS.items():
        data = (ROOT / relative).read_bytes()
        if sha(data) != expected:
            raise RuntimeError(f"prebuild_pin:{relative}")
    expected_manifest = {
        relative: {"bytes": len((ROOT / relative).read_bytes()), "sha256": expected}
        for relative, expected in PREBUILD_PINS.items()
    }
    expected_ceilings = {
        "production_old_rank": 2014,
        "production_h1_rank": 6045,
        "production_b1_rank": 8059,
        "grade2_defect_origins": 32280,
        "one_character_rank": 36288,
        "one_character_queue_attempts": 177432,
        "joint_physical_input_rows": 153211,
        "one_block_packed_basis_bytes": 329204736,
        "joint_packed_physical_input_ceiling_bytes": 1853240256,
    }
    if (
        prepare.get("phase") != "prepare" or prepare.get("fixture") is not False
        or prepare.get("terminal") is not None or prepare.get("dimensions") != dimensions()
        or prepare.get("resource_ceilings_not_estimates") != expected_ceilings
        or prepare.get("prebuild_manifest") != expected_manifest
        or prepare.get("prebuild_manifest_sha256") != sha(canonical(expected_manifest))
        or prepare.get("queue_exhausted") is not True
        or prepare.get("downstream_claim_flags") != claim_flags()
    ):
        raise RuntimeError("prepare_structure")
    ancestry = prepare.get("state_ancestry")
    compact = prepare.get("compact_ancestry")
    if (
        not isinstance(ancestry, dict) or ancestry.get("grade1_schema") != GRADE1_STATE_SCHEMA
        or ancestry.get("grade1_input_manifest_sha256") != sha(canonical(ancestry.get("grade1_input_manifest")))
        or prepare.get("state_ancestry_sha256") != sha(canonical(ancestry))
        or not isinstance(compact, dict) or set(compact) != {"old", "h1", "grade1_defect_origins"}
        or prepare.get("compact_ancestry_sha256") != sha(canonical(compact))
    ):
        raise RuntimeError("prepare_ancestry")
    presentation = prepare.get("b1_presentation")
    unsigned = dict(presentation)
    presentation_digest = unsigned.pop("sha256", None)
    rank = presentation.get("rank")
    if (
        presentation_digest != sha(canonical(unsigned)) or presentation.get("grade") != 1
        or not plain_int(rank) or rank < 0 or rank > 8059
        or presentation.get("global_order") != "all_lifted_old_by_character_pivot_then_all_h1_by_character_pivot"
        or presentation.get("seed_count") != 44 or presentation.get("actor_order") != list(ACTORS)
        or presentation.get("complete") is not True
        or len(presentation.get("seed_reductions", [])) != 44
        or len(presentation.get("actor_transitions", [])) != rank
        or presentation.get("seed_reductions_sha256") != sha(canonical(presentation["seed_reductions"]))
        or presentation.get("actor_transitions_sha256") != sha(canonical(presentation["actor_transitions"]))
        or presentation.get("basis_roster_sha256") != sha(canonical(presentation.get("basis_roster")))
        or len(presentation.get("basis_roster", [])) != rank
    ):
        raise RuntimeError("presentation_structure")
    for expression in presentation["seed_reductions"]:
        if expression != normalize_expression(expression) or any(not 0 <= index < rank or coefficient not in (1, 2) for index, coefficient in expression):
            raise RuntimeError("seed_expression")
    for row in presentation["actor_transitions"]:
        if len(row) != 4:
            raise RuntimeError("actor_expression_shape")
        for expression in row:
            if expression != normalize_expression(expression) or any(not 0 <= index < rank or coefficient not in (1, 2) for index, coefficient in expression):
                raise RuntimeError("actor_expression")
    expected_origins = [{"id": seed, "kind": "seed", "seed": seed + 1} for seed in range(44)]
    for pivot in range(rank):
        for letter in ACTORS:
            expected_origins.append({"id": len(expected_origins), "kind": "transition", "pivot": pivot, "letter": letter})
    if (
        prepare.get("defect_roster") != expected_origins
        or prepare.get("defect_roster_sha256") != sha(canonical(expected_origins))
        or prepare.get("defect_roster_formula") != f"44+4*{rank}"
        or prepare.get("pure_q1_words") != [{"parity": list(parity), "word": list(PURE_WORDS[parity])} for parity in CHARACTERS]
    ):
        raise RuntimeError("defect_roster")
    preflight = prepare.get("affine_boundary_preflight")
    if (
        not isinstance(preflight, dict) or preflight.get("replayed") is not True
        or preflight.get("occurrence_affine_checks") != 12
        or preflight.get("crossed_law_checks") != 96
        or preflight.get("pb3_translated_boundaries") != 6
        or preflight.get("pb4_blocks") != 2
        or preflight.get("integral_exponent_relators") != 44
        or preflight.get("filtration_occurrence_aggregation_checks") != 5
    ):
        raise RuntimeError("affine_preflight_receipt")
    p1 = PackedMatrix(read_blob(state_dir, prepare["precision1_basis_blob"], rank, SOURCE_P1), rank, SOURCE_P1)
    d2 = PackedMatrix(read_blob(state_dir, prepare["degree2_lift_blob"], rank, SOURCE2), rank, SOURCE2)
    packets = []
    for character, packet in enumerate(prepare.get("packets", [])):
        if (
            packet.get("character_index") != character or packet.get("character") != list(CHARACTERS[character])
            or packet.get("origin_count") != len(expected_origins)
            or packet.get("origin_sha256") != prepare["defect_roster_sha256"]
        ):
            raise RuntimeError("packet_structure")
        packets.append(PackedMatrix(read_blob(state_dir, packet["blob"], len(expected_origins), SOURCE2C), len(expected_origins), SOURCE2C))
    if len(packets) != 4:
        raise RuntimeError("packet_count")
    return p1, d2, packets


def verify_blocks(
    state_dir: Path,
    context: Context,
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
    packets: list[PackedMatrix],
) -> list[Path]:
    paths: list[Path] = []
    origin_count = len(prepare["defect_roster"])
    for character, (block, _) in enumerate(blocks):
        rank = block.get("rank")
        if (
            block.get("phase") != "block" or block.get("fixture") is not False or block.get("terminal") is not None
            or block.get("parent_sha256") != prepare_digest or block.get("character_index") != character
            or block.get("character") != list(CHARACTERS[character])
            or block.get("dimensions") != {"width": SOURCE2C, "monomials": [list(value) for value in DEGREE2_MONOMIALS], "monomials_coupled": True}
            or block.get("packet_sha256") != prepare["packets"][character]["blob"]["sha256"]
            or block.get("origin_sha256") != prepare["defect_roster_sha256"]
            or block.get("origin_count") != origin_count or not plain_int(rank) or not 0 <= rank <= SOURCE2C
            or block.get("attempts") != origin_count + 4 * rank or block.get("attempts") > 177432
            or block.get("queue_exhausted") is not True or block.get("actor_order") != list(ACTORS)
            or len(block.get("origin_reductions", [])) != origin_count
            or len(block.get("actor_transitions", [])) != rank
            or len(block.get("dag_nodes", [])) != rank
            or len(block.get("pivot_leads", [])) != rank
            or block.get("dag_sha256") != sha(canonical(block.get("dag_nodes")))
            or block.get("downstream_claim_flags") != claim_flags()
        ):
            raise RuntimeError(f"block_structure:{character}")
        basis_path = read_blob(state_dir, block["basis_blob"], rank, SOURCE2C)
        basis = PackedMatrix(basis_path, rank, SOURCE2C)
        for origin, expression in enumerate(block["origin_reductions"]):
            if not np.array_equal(packets[character].row(origin), combine_store(basis, expression)):
                raise RuntimeError(f"block_origin_replay:{character}:{origin}")
        for pivot, row in enumerate(block["actor_transitions"]):
            if len(row) != 4:
                raise RuntimeError("block_actor_count")
            for actor_index, letter in enumerate(ACTORS):
                if not np.array_equal(associated_actor(context, basis.row(pivot), character, letter), combine_store(basis, row[actor_index])):
                    raise RuntimeError(f"block_actor_replay:{character}:{pivot}:{letter}")
        for pivot, node in enumerate(block["dag_nodes"]):
            origin = node["origin"]
            candidate = packets[character].row(origin["origin"]) if origin["kind"] == "defect" else associated_actor(context, basis.row(origin["parent"]), character, origin["letter"])
            for earlier, coefficient in node["reductions"]:
                add(candidate, basis.row(earlier), -coefficient)
            candidate = (node["scale"] * candidate.astype(np.uint16) % 3).astype(np.uint8)
            if not np.array_equal(candidate, basis.row(pivot)):
                raise RuntimeError(f"block_dag_replay:{character}:{pivot}")
        paths.append(basis_path)
    return paths


class FinalReducer:
    """Validate one sealed echelon once, then reduce by its lead index."""

    def __init__(self, rows: PackedMatrix, declared_leads: Any):
        if not isinstance(declared_leads, list) or len(declared_leads) != rows.rows:
            raise RuntimeError("basis_lead_roster")
        self.rows = rows
        self.lead_to_pivot: dict[int, int] = {}
        for pivot, declared in enumerate(declared_leads):
            if not plain_int(declared) or not 0 <= declared < rows.width:
                raise RuntimeError("basis_lead_value")
            dense = rows.row(pivot)
            mask = dense != 0
            if not bool(mask.any()):
                raise RuntimeError("basis_zero_row")
            lead = int(mask.argmax())
            if lead != declared or int(dense[lead]) != 1 or lead in self.lead_to_pivot:
                raise RuntimeError("basis_echelon")
            self.lead_to_pivot[lead] = pivot

    def reduce(self, row: np.ndarray) -> tuple[np.ndarray, list[list[int]]]:
        work = row.copy()
        reductions: list[list[int]] = []
        cursor = 0
        while cursor < work.size:
            mask = work[cursor:] != 0
            if not bool(mask.any()):
                break
            lead = cursor + int(mask.argmax())
            pivot = self.lead_to_pivot.get(lead)
            if pivot is None:
                break
            coefficient = int(work[lead])
            add(work, self.rows.row(pivot), -coefficient)
            reductions.append([pivot, coefficient])
            cursor = lead
        return work, reductions


def verify_module(
    state_dir: Path,
    context: Context,
    prepare: dict[str, Any],
    prepare_digest: str,
    blocks: list[tuple[dict[str, Any], str]],
    block_paths: list[Path],
    p1: PackedMatrix,
    d2: PackedMatrix,
) -> tuple[dict[str, Any], str]:
    module, module_digest = read_state(state_dir, "grade2-module", prepare_digest)
    lower_rank = module.get("physical_lower_rank")
    grade_rank = module.get("physical_grade_rank")
    block_ranks = [block["rank"] for block, _ in blocks]
    roster_count = p1.rows + sum(block_ranks)
    expected_ceilings = prepare["resource_ceilings_not_estimates"]
    if (
        module.get("phase") != "module" or module.get("fixture") is not False
        or module.get("parent_sha256") != prepare_digest
        or module.get("block_sha256") != [digest for _, digest in blocks]
        or module.get("dimensions") != dimensions()
        or module.get("resource_ceilings_not_estimates") != expected_ceilings
        or module.get("source_blocks_exhausted") != 4 or module.get("b1_rank") != p1.rows
        or module.get("h2_ranks") != block_ranks
        or module.get("target_independent") is not True or module.get("membership_tested") is not False
        or module.get("terminal") != "FIRST_RUNG_GRADE2_MODULE_READY"
        or module.get("downstream_claim_flags") != claim_flags()
        or not plain_int(lower_rank) or lower_rank < 0 or not plain_int(grade_rank) or grade_rank < 0
        or len(module.get("physical_roster", [])) != roster_count or roster_count > 153211
        or module.get("physical_roster_sha256") != sha(canonical(module.get("physical_roster")))
        or len(module.get("physical_lower_dag", [])) != lower_rank
        or len(module.get("physical_grade_dag", [])) != grade_rank
        or len(module.get("physical_lower_pivot_leads", [])) != lower_rank
        or len(module.get("physical_grade_pivot_leads", [])) != grade_rank
    ):
        raise RuntimeError("module_structure")
    lower_basis = PackedMatrix(read_blob(state_dir, module["physical_lower_basis_blob"], lower_rank, PHYSICAL_LOWER), lower_rank, PHYSICAL_LOWER)
    companion = PackedMatrix(read_blob(state_dir, module["physical_lower_grade_companion_blob"], lower_rank, PHYSICAL2), lower_rank, PHYSICAL2)
    grade_basis = PackedMatrix(read_blob(state_dir, module["physical_grade_basis_blob"], grade_rank, PHYSICAL2), grade_rank, PHYSICAL2)
    lower_reducer = FinalReducer(lower_basis, module["physical_lower_pivot_leads"])
    grade_reducer = FinalReducer(grade_basis, module["physical_grade_pivot_leads"])
    def aggregate_b1(pivot: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return aggregate(context, full_store(p1, d2, pivot))

    current_character = -1
    current_basis: PackedMatrix | None = None

    def aggregate_h2(character: int, pivot: int) -> np.ndarray:
        nonlocal current_character, current_basis
        if character != current_character:
            current_basis = PackedMatrix(
                block_paths[character], block_ranks[character], SOURCE2C
            )
            current_character = character
        if current_basis is None:
            raise RuntimeError("module_h2_store")
        row = np.zeros((4, SOURCE2C), dtype=np.uint8)
        row[character] = current_basis.row(pivot)
        return aggregate(
            context,
            (
                np.zeros((4, SOURCE0C), dtype=np.uint8),
                np.zeros((4, SOURCE1C), dtype=np.uint8),
                row,
                np.zeros(8, dtype=np.uint8),
            ),
        )[2]
    for pivot, node in enumerate(module["physical_lower_dag"]):
        origin = node["origin"]
        physical = aggregate_b1(origin["pivot"])
        lower = np.concatenate((physical[0], physical[1], physical[3]))
        grade = physical[2].copy()
        for earlier, coefficient in node["reductions"]:
            add(lower, lower_basis.row(earlier), -coefficient)
            add(grade, companion.row(earlier), -coefficient)
        lower = (node["scale"] * lower.astype(np.uint16) % 3).astype(np.uint8)
        grade = (node["scale"] * grade.astype(np.uint16) % 3).astype(np.uint8)
        if not np.array_equal(lower, lower_basis.row(pivot)) or not np.array_equal(grade, companion.row(pivot)):
            raise RuntimeError(f"module_lower_dag:{pivot}")
    for pivot, node in enumerate(module["physical_grade_dag"]):
        origin = node["origin"]
        if origin["kind"] == "lifted_b1_connection":
            physical = aggregate_b1(origin["pivot"])
            lower = np.concatenate((physical[0], physical[1], physical[3]))
            grade = physical[2].copy()
            for earlier, coefficient in origin["lower_reductions"]:
                add(lower, lower_basis.row(earlier), -coefficient)
                add(grade, companion.row(earlier), -coefficient)
            if np.any(lower):
                raise RuntimeError("module_connection_lower")
        else:
            grade = aggregate_h2(origin["character"], origin["pivot"])
        for earlier, coefficient in node["reductions"]:
            add(grade, grade_basis.row(earlier), -coefficient)
        grade = (node["scale"] * grade.astype(np.uint16) % 3).astype(np.uint8)
        if not np.array_equal(grade, grade_basis.row(pivot)):
            raise RuntimeError(f"module_grade_dag:{pivot}")
    # Complete containment, including candidates rejected during discovery.
    for b1_pivot in range(p1.rows):
        physical = aggregate_b1(b1_pivot)
        lower = np.concatenate((physical[0], physical[1], physical[3]))
        grade = physical[2].copy()
        lower_remainder, reductions = lower_reducer.reduce(lower)
        for pivot, coefficient in reductions:
            add(grade, companion.row(pivot), -coefficient)
        if np.any(lower_remainder) or np.any(grade_reducer.reduce(grade)[0]):
            raise RuntimeError("module_b1_containment")
    for character, rank in enumerate(block_ranks):
        for h2_pivot in range(rank):
            grade = aggregate_h2(character, h2_pivot)
            if np.any(grade_reducer.reduce(grade)[0]):
                raise RuntimeError("module_h2_containment")
    transition = module.get("transition_state")
    if (
        transition.get("b1_presentation_sha256") != prepare["b1_presentation"]["sha256"]
        or transition.get("grade2_origin_reductions_sha256") != [sha(canonical(block["origin_reductions"])) for block, _ in blocks]
        or transition.get("grade2_actor_transitions_sha256") != [sha(canonical(block["actor_transitions"])) for block, _ in blocks]
        or transition.get("grade2_dag_sha256") != [block["dag_sha256"] for block, _ in blocks]
        or transition.get("complete_for_future_t2") is not True
    ):
        raise RuntimeError("module_transition_state")
    if any(key in module for key in ("target", "residual", "member_coefficients", "dual")):
        raise RuntimeError("module_target_contamination")
    return module, module_digest


OCC_M = (
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    ((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
)
OCC_C = (
    ((0, 0, 0), (0, 0, 0)),
    ((0, 0, 0), (1, 0, 0)),
    ((1, 0, 1), (1, -2, 0)),
    ((0, 1, 0), (0, 1, 1)),
    ((0, 0, 0), (0, 0, 0)),
    ((0, 1, 0), (0, 0, 2)),
)


def mat3(matrix0: tuple[tuple[int, int, int], ...], vector: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(sum(matrix0[row][column] * vector[column] for column in range(3)) % 3 for row in range(3))  # type: ignore[return-value]


def parity_action(matrix0: tuple[tuple[int, int], tuple[int, int]], value: tuple[int, int]) -> tuple[int, int]:
    return ((matrix0[0][0] * value[0] + matrix0[0][1] * value[1]) & 1, (matrix0[1][0] * value[0] + matrix0[1][1] * value[1]) & 1)


def crossed(tag: int, parity: tuple[int, int], action: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, int, int]:
    first, second = OCC_C[tag]
    if parity == (0, 0):
        return (0, 0, 0)
    if parity == (1, 0):
        return tuple(value % 3 for value in first)  # type: ignore[return-value]
    if parity == (0, 1):
        return tuple(value % 3 for value in second)  # type: ignore[return-value]
    acted = sign_kernel(parity_action(action, (0, 1)), tuple(value % 3 for value in first))
    return tuple((acted[index] + second[index]) % 3 for index in range(3))  # type: ignore[return-value]


def verify_affine_boundary(context: Context, words: dict[str, Any]) -> dict[str, Any]:
    identity: Affine = (floor.ID9, 0, 0, (0, 0, 0))
    affine_checks = 0
    crossed_checks = 0
    for tag, pair in enumerate(floor.OO):
        xq = floor.qev(pair[0], context.q1_images)
        yq = floor.qev(pair[1], context.q1_images)
        action = ((xq[1], yq[1]), (xq[2], yq[2]))
        for generator, source in enumerate(context.images):
            expected_parity = parity_action(action, (source[1], source[2]))
            base = mat3(OCC_M[tag], source[3])
            extra = crossed(tag, (source[1], source[2]), action)
            expected_kernel = tuple((base[index] + extra[index]) % 3 for index in range(3))
            actual = context.actor_tags[(1, 2)[generator]][tag]
            if actual[1:3] != expected_parity or actual[3] != expected_kernel:
                raise RuntimeError("occurrence_affine")
            affine_checks += 1
        for left in CHARACTERS:
            for right in CHARACTERS:
                lhs = crossed(tag, (left[0] ^ right[0], left[1] ^ right[1]), action)
                first = sign_kernel(parity_action(action, right), crossed(tag, left, action))
                second = crossed(tag, right, action)
                rhs = tuple((first[index] + second[index]) % 3 for index in range(3))
                if lhs != rhs:
                    raise RuntimeError("crossed_law")
                crossed_checks += 1
        x = affine_eval(floor.sub((1,), *pair), context.images)
        b = affine_eval(floor.sub((-1, -2), *pair), context.images)
        y = affine_eval(floor.sub((2,), *pair), context.images)
        if affine_mul(affine_mul(x, b), y) != identity:
            raise RuntimeError("translated_pb3")
    if int(e_poly((2, 0, 0))[1]) != 2 or int(e_poly((2, 0, 0))[4]) != 1:
        raise RuntimeError("negative_column")
    for parity in CHARACTERS:
        source = affine_eval(PURE_WORDS[parity], context.images)
        if source[0] != floor.ID9 or source[1:3] != parity:
            raise RuntimeError("pure_word")
    g760 = tuple(int(value) for value in words["g760"])
    h1 = tuple(floor.wm(floor.sub(g760, *floor.OO[2]), floor.wi(floor.sub(g760, *floor.OO[1])), floor.sub(g760, *floor.OO[0])))
    h2 = tuple(
        floor.wm(
            floor.sub(g760, *floor.OO[5]),
            floor.wi(floor.sub(g760, *floor.OO[4])),
            floor.wi(floor.sub(g760, *floor.OO[3])),
        )
    )
    if affine_eval(h1, context.images) != identity or affine_eval(h2, context.images) != identity or floor.exps(h1) != (0, 0) or floor.exps(h2) != (0, 0):
        raise RuntimeError("pb4_boundary")
    for relator in words["relators"]:
        exponent = floor.exps(tuple(int(value) for value in relator))
        if exponent[0] % 18 or exponent[1] % 18:
            raise RuntimeError("exponent_gate")
    canary0 = np.zeros((4, SOURCE0C), dtype=np.uint8)
    canary1 = np.zeros((4, SOURCE1C), dtype=np.uint8)
    canary2 = np.zeros((4, SOURCE2C), dtype=np.uint8)
    canary_aux = np.asarray((1, 2, 0, 1, 0, 2, 1, 2), dtype=np.uint8)
    for character in range(4):
        canary0[character, lower_coord(character % 6, character % 2, character)] = character % 3
        canary1[character, grade1_coord((character + 1) % 6, character % 2, character % 3, character + 7)] = (character + 1) % 3
        canary2[character, (((character + 2) % 6 * 2 + character % 2) * 6 + (character + 1) % 6) * 504 + character + 11] = (character + 2) % 3
    filtration_checks = 0
    zero2 = np.zeros_like(canary2)
    for letter in ACTORS:
        full = act(context, (canary0, canary1, canary2, canary_aux), context.actor_tags[letter])
        truncated = act(context, (canary0, canary1, zero2, canary_aux), context.actor_tags[letter])
        if (
            not np.array_equal(full[0], truncated[0])
            or not np.array_equal(full[1], truncated[1])
            or not np.array_equal(full[3], truncated[3])
        ):
            raise RuntimeError("filtration_actor")
        filtration_checks += 1
    full_physical = aggregate(context, (canary0, canary1, canary2, canary_aux))
    truncated_physical = aggregate(context, (canary0, canary1, zero2, canary_aux))
    if (
        not np.array_equal(full_physical[0], truncated_physical[0])
        or not np.array_equal(full_physical[1], truncated_physical[1])
        or not np.array_equal(full_physical[3], truncated_physical[3])
    ):
        raise RuntimeError("filtration_aggregation")
    filtration_checks += 1
    return {
        "extension": "Q2=P_times_(C3^3_semidirect_C2^2)_over_Q1",
        "normal_form": "section-left-kernel-right",
        "multiplication_cocycle": "zero",
        "kernel_action": "v442-sign-action",
        "occurrence_kernel_matrices": [[list(row) for row in matrix] for matrix in OCC_M],
        "occurrence_crossed_generators": [[list(value) for value in pair] for pair in OCC_C],
        "occurrence_affine_checks": affine_checks,
        "crossed_law_checks": crossed_checks,
        "negative_column_degree2": "u->2u+u^2",
        "pb3_translated_boundaries": 6,
        "pb4_blocks": 2,
        "pb4_words_sha256": [
            sha(json.dumps(list(h1), separators=(",", ":")).encode("ascii")),
            sha(json.dumps(list(h2), separators=(",", ":")).encode("ascii")),
        ],
        "integral_exponent_relators": 44,
        "filtration_occurrence_aggregation_checks": filtration_checks,
        "normalized_exponent_actor_action": "trivial",
        "replayed": True,
    }


def check_state(state_dir: Path, grade1_dir: Path) -> dict[str, Any]:
    started = time.monotonic()
    prepare, prepare_digest = read_state(state_dir, "grade2-prepare", None)
    p1, d2, packets = validate_prepare_structure(state_dir, prepare)
    prepare1, prepare1_digest, blocks1 = authenticate_grade1(grade1_dir)
    ancestry = prepare["state_ancestry"]
    expected_ancestry = {
        "grade1_schema": GRADE1_STATE_SCHEMA,
        "grade1_input_manifest": prepare1["input_manifest"],
        "grade1_input_manifest_sha256": prepare1["input_manifest_sha256"],
        "grade1_prepare_sha256": prepare1_digest,
        "grade1_block_sha256": [digest for _, digest in blocks1],
        "grade1_prepare_blob_sha256": {
            "old_lower": [old["lower_basis_blob"]["sha256"] for old in prepare1["old_blocks"]],
            "old_lift": [old["lifted_grade_blob"]["sha256"] for old in prepare1["old_blocks"]],
            "packets": [packet["blob"]["sha256"] for packet in prepare1["packets"]],
        },
        "grade1_block_basis_sha256": [block["basis_blob"]["sha256"] for block, _ in blocks1],
    }
    expected_compact = {
        "old": [
            {
                "character_index": old["character_index"],
                "dag_nodes": old["record"]["dag_nodes"],
                "lower_basis_sha256": old["lower_basis_blob"]["sha256"],
                "lifted_grade_sha256": old["lifted_grade_blob"]["sha256"],
            }
            for old in prepare1["old_blocks"]
        ],
        "h1": [
            {
                "character_index": character,
                "dag_nodes": block["dag_nodes"],
                "dag_sha256": block["dag_sha256"],
                "basis_sha256": block["basis_blob"]["sha256"],
            }
            for character, (block, _) in enumerate(blocks1)
        ],
        "grade1_defect_origins": prepare1["defect_origins"],
    }
    if ancestry != expected_ancestry or prepare["compact_ancestry"] != expected_compact:
        raise RuntimeError("grade1_parent_binding")
    words = json.loads((ROOT / "scratchpad/a0_paper_words_v1.json").read_text(encoding="utf-8"))
    context = Context(words)
    preflight = verify_affine_boundary(context, words)
    if prepare["affine_boundary_preflight"] != preflight:
        raise RuntimeError("affine_preflight_disagreement")
    verify_b1_and_packets(
        grade1_dir, context, words, prepare, prepare1, blocks1, p1, d2, packets
    )
    blocks = [read_state(state_dir, f"grade2-block-{index}", prepare_digest) for index in range(4)]
    block_paths = verify_blocks(state_dir, context, prepare, prepare_digest, blocks, packets)
    module, module_digest = verify_module(
        state_dir, context, prepare, prepare_digest, blocks, block_paths, p1, d2
    )
    return {
        "checker": "PASS",
        "terminal": module["terminal"],
        "prepare_sha256": prepare_digest,
        "block_sha256": [digest for _, digest in blocks],
        "module_sha256": module_digest,
        "b1_rank": p1.rows,
        "defect_origins": len(prepare["defect_roster"]),
        "h2_ranks": [block["rank"] for block, _ in blocks],
        "physical_lower_rank": module["physical_lower_rank"],
        "physical_grade_rank": module["physical_grade_rank"],
        "affine_boundary_replay": preflight,
        "membership_tested": False,
        "verified": False,
        "elapsed_seconds": time.monotonic() - started,
    }


def fixture_contract(value: dict[str, Any]) -> None:
    if value.get("origin") != [[0, 1]]:
        raise RuntimeError("fixture_origin")
    if value.get("transition") != [[0, 2]]:
        raise RuntimeError("fixture_transition")
    if value.get("blob_sha256") != "a" * 64:
        raise RuntimeError("fixture_blob")
    if value.get("parent_sha256") != "b" * 64:
        raise RuntimeError("fixture_parent")
    if value.get("monomials") != [list(value) for value in DEGREE2_MONOMIALS]:
        raise RuntimeError("fixture_monomials")
    if value.get("queue_exhausted") is not True:
        raise RuntimeError("fixture_queue")


class TinyEchelon:
    def __init__(self, width: int):
        self.width = width
        self.rows: list[np.ndarray] = []
        self.leads: list[int] = []

    def reduce(self, row: np.ndarray) -> np.ndarray:
        work = row.copy()
        while True:
            nonzero = np.flatnonzero(work)
            if not len(nonzero):
                return work
            lead = int(nonzero[0])
            try:
                pivot = self.leads.index(lead)
            except ValueError:
                return work
            add(work, self.rows[pivot], -int(work[lead]))

    def insert(self, row: np.ndarray) -> bool:
        work = self.reduce(row)
        nonzero = np.flatnonzero(work)
        if not len(nonzero):
            return False
        lead = int(nonzero[0])
        if int(work[lead]) == 2:
            work = (2 * work.astype(np.uint16) % 3).astype(np.uint8)
        self.rows.append(work)
        self.leads.append(lead)
        return True


def fixture() -> dict[str, Any]:
    started = time.monotonic()
    words = json.loads((ROOT / "scratchpad/a0_paper_words_v1.json").read_text(encoding="utf-8"))
    context = Context(words)
    preflight = verify_affine_boundary(context, words)
    negative = e_poly((2, 0, 0))
    if int(negative[1]) != 2 or int(negative[4]) != 1:
        raise RuntimeError("fixture_negative")
    d2 = np.zeros((4, SOURCE2C), dtype=np.uint8)
    for monomial in range(6):
        d2[2, monomial * 504 + monomial] = (monomial % 2) + 1
    recovered = np.zeros_like(d2)
    for label in CHARACTERS:
        add(recovered, pure_project(context, d2, label))
    if not np.array_equal(recovered, d2) or np.count_nonzero(d2[2]) != 6:
        raise RuntimeError("fixture_projector_or_coupling")
    associated = d2[2]
    actor_rows = [associated_actor(context, associated, 2, letter) for letter in ACTORS]
    if len(actor_rows) != 4 or any(row.shape != (SOURCE2C,) for row in actor_rows):
        raise RuntimeError("fixture_actor_roster")
    if not np.array_equal(
        associated_actor(context, associated_actor(context, associated, 2, 1), 2, -1),
        associated,
    ) or not np.array_equal(
        associated_actor(context, associated_actor(context, associated, 2, 2), 2, -2),
        associated,
    ):
        raise RuntimeError("fixture_actor_inverse")
    # An old lower row has a genuine induced positive-grade actor defect.
    old = (
        np.zeros((4, SOURCE0C), dtype=np.uint8),
        np.zeros((4, SOURCE1C), dtype=np.uint8),
        np.zeros((4, SOURCE2C), dtype=np.uint8),
        np.zeros(8, dtype=np.uint8),
    )
    old[0][0, lower_coord(0, 0, 0)] = 1
    acted = act(context, old, context.actor_tags[1])
    recorded = (acted[0].copy(), np.zeros_like(acted[1]), np.zeros_like(acted[2]), acted[3].copy())
    defect = subtract_full(acted, recorded)
    if not np.any(defect[1]) and not np.any(defect[2]):
        raise RuntimeError("fixture_old_transition_defect")
    # Four projected seed records recover the unprojected relation.
    seed = evaluate_seed(context, tuple(int(value) for value in words["relators"][0]))
    seed_recovered = tuple(np.zeros_like(part) for part in seed)
    for label in CHARACTERS:
        add_full(seed_recovered, full_project(context, seed, label), 1)
    if any(not np.array_equal(seed[index], seed_recovered[index]) for index in range(4)):
        raise RuntimeError("fixture_seed_recovery")
    lower = TinyEchelon(4)
    if not lower.insert(np.asarray((1, 0, 0, 0), dtype=np.uint8)):
        raise RuntimeError("fixture_lower_insert")
    if np.any(lower.reduce(np.asarray((1, 0, 0, 0), dtype=np.uint8))):
        raise RuntimeError("fixture_lower_dependence")
    connection = np.asarray((0, 1, 0, 0), dtype=np.uint8)
    if not np.any(connection):
        raise RuntimeError("fixture_connection")
    contract = {
        "origin": [[0, 1]], "transition": [[0, 2]],
        "blob_sha256": "a" * 64, "parent_sha256": "b" * 64,
        "monomials": [list(value) for value in DEGREE2_MONOMIALS],
        "queue_exhausted": True,
    }
    fixture_contract(contract)
    mutations = 0
    for key, value in (
        ("origin", [[0, 2]]), ("transition", [[0, 1]]),
        ("blob_sha256", "c" * 64), ("parent_sha256", "d" * 64),
        ("monomials", [list(DEGREE2_MONOMIALS[0])]),
        ("queue_exhausted", False),
    ):
        changed = dict(contract)
        changed[key] = value
        try:
            fixture_contract(changed)
        except RuntimeError:
            mutations += 1
    target_lower = np.asarray((2, 0, 1, 2), dtype=np.uint8)
    replay_lower = target_lower.copy()
    target_grade = np.asarray((0, 2, 1, 2, 0, 1), dtype=np.uint8)
    replay_grade = np.asarray((0, 1, 1, 0, 0, 2), dtype=np.uint8)
    if np.any((target_lower.astype(np.int16) - replay_lower.astype(np.int16)) % 3):
        raise RuntimeError("fixture_join_lower")
    residual = ((target_grade.astype(np.int16) - replay_grade.astype(np.int16)) % 3).astype(np.uint8)
    stored = residual.copy()
    if not np.array_equal(stored, residual):
        raise RuntimeError("fixture_join")
    stored[1] = (int(stored[1]) + 1) % 3
    if np.array_equal(stored, residual):
        raise RuntimeError("fixture_join_mutation")
    mutations += 1
    resume = []
    parent = None
    for phase in ("prepare", "block0", "block1", "block2", "block3", "module", "join"):
        body = {"schema": STATE_SCHEMA, "phase": phase, "parent": parent}
        first = sha(canonical(body))
        second = sha(canonical(json.loads(canonical(body))))
        if first != second:
            raise RuntimeError("fixture_resume")
        resume.append(first)
        parent = first
    if mutations != 7:
        raise RuntimeError("fixture_mutation_count")
    return {
        "fixture": "PASS",
        "split_b1_nonzero_old_transition_defect": True,
        "original_seed_from_four_records": True,
        "old_new_four_actor_transitions": True,
        "negative_column": "u->2u+u^2",
        "coupled_monomials": 6,
        "dependent_lifted_old_connection": True,
        "mutations_rejected": mutations,
        "member_join_residual_recomputed": True,
        "phase_resume_idempotence": len(resume),
        "affine_boundary_replay": preflight,
        "membership_tested": False,
        "verified": False,
        "elapsed_seconds": time.monotonic() - started,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    modes = value.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", metavar="STATE_DIR", type=Path)
    modes.add_argument("--fixture", action="store_true")
    value.add_argument("--grade1-state-dir", type=Path)
    return value


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    if arguments.fixture:
        if arguments.grade1_state_dir is not None:
            parser().error("--fixture accepts no state directory")
        result = fixture()
    else:
        if arguments.grade1_state_dir is None:
            parser().error("--check requires --grade1-state-dir")
        result = check_state(arguments.check.resolve(), arguments.grade1_state_dir.resolve())
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
