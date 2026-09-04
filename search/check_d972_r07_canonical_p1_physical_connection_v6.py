#!/usr/bin/env python3
"""Independent checker for the v6 actual-P1 physical connection stream.

The checker is intentionally a separate implementation.  It authenticates
the immutable inputs as bytes, reconstructs one precision-one row directly
from the Task554 state files, performs the occurrence-first degree-two
aggregation and then replays the packed v492 recurrence.  No producer or
upstream executable is imported or executed here.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import mmap
import os
import re
import shutil
import sys
import tempfile
import time
from collections import deque
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ROWS = 8059
P1_WIDTH = 96776
P1_BYTES = P1_WIDTH // 4
D2_WIDTH = 145152
D2_BYTES = D2_WIDTH // 4
ELL_WIDTH = 32260
TOP_WIDTH = 48384
COEFF_BYTES = (ROWS + 3) // 4
ELL_BYTES = ELL_WIDTH // 4
TOP_BYTES = TOP_WIDTH // 4
SCHEMA = "d972.r07.canonical-p1-physical-connection.v5"
STATUS = "CANONICAL_P1_PHYSICAL_CONNECTION_CANDIDATE"
P1_SCHEMA = "d972.r07.canonical-p1-dag-degree2-lift.v8"
P1_STATUS = "CANONICAL_P1_DAG_DEGREE2_LIFT_CANDIDATE"
LAUNCH_SCHEMA = "d972.r07.canonical-p1-physical-connection.launch.v5"
ZERO_HEAD = "00" * 32
REPOSITORY = "tochiazuma0510-alt/shadow-atelier"
SOURCE_RUN = "33677346616"
SOURCE_ATTEMPT = "1"
SOURCE_HEAD = "22c6dddb43d107c05e65f53ad898823ae8ebe276"
P1_V10_SHA = "af99dbb399a0f98ab70e240498fb7b934ce8e0af93e4930cd1dbd549177f750f"
PREPARE_DIGEST = "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865"
PARENTS = (
    "9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74",
    "d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6",
    "a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac",
    "642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01",
)
ORDER = (0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059)
OLD_RANKS = (505, 503, 503, 503)
NEW_RANKS = (1509, 1512, 1512, 1512)
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
ACTORS = (1, -1, 2, -2)
MONOMIALS = ((2, 0, 0), (1, 1, 0), (1, 0, 1),
             (0, 2, 0), (0, 1, 1), (0, 0, 2))
FALSE_FLAGS = {"A0": False, "COMMON": False, "COFINAL_LIFT": False,
               "FAKE": False, "IHARA": False, "verified": False}
SOURCE_HASHES = {
    "p1_v10": P1_V10_SHA,
    "grade1_v4": "1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4",
    "prebuild_v1": "acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8",
    "semantic_v5": "dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf",
    "structural_v1": "38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73",
    "floor_v1": "6201ae0b5c1d648529ac648a574c5096b8088fe341423724556860d9d3f23fba",
    "words": "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893",
    "task712_v3": "7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84",
}
TASK554 = (
    {"role": "prepare", "run": SOURCE_RUN, "attempt": SOURCE_ATTEMPT,
     "head": SOURCE_HEAD, "id": 9865061266,
     "name": "task554-grade1-v3-prepare-33677346616-1",
     "archive_bytes": 204360988,
     "digest": "sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4",
     "expires_at": "2026-12-01T20:06:55Z"},
    {"role": "block-0", "run": SOURCE_RUN, "attempt": SOURCE_ATTEMPT,
     "head": SOURCE_HEAD, "id": 9865238399,
     "name": "task554-grade1-v3-state-block-0-33677346616-1",
     "archive_bytes": 81729645,
     "digest": "sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838",
     "expires_at": "2026-12-01T20:06:55Z"},
    {"role": "block-1", "run": SOURCE_RUN, "attempt": SOURCE_ATTEMPT,
     "head": SOURCE_HEAD, "id": 9865242284,
     "name": "task554-grade1-v3-state-block-1-33677346616-1",
     "archive_bytes": 82259824,
     "digest": "sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb",
     "expires_at": "2026-12-01T20:06:55Z"},
    {"role": "block-2", "run": SOURCE_RUN, "attempt": SOURCE_ATTEMPT,
     "head": SOURCE_HEAD, "id": 9865193269,
     "name": "task554-grade1-v3-state-block-2-33677346616-1",
     "archive_bytes": 82200189,
     "digest": "sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d",
     "expires_at": "2026-12-01T20:06:55Z"},
    {"role": "block-3", "run": SOURCE_RUN, "attempt": SOURCE_ATTEMPT,
     "head": SOURCE_HEAD, "id": 9865239848,
     "name": "task554-grade1-v3-state-block-3-33677346616-1",
     "archive_bytes": 82266526,
     "digest": "sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92",
     "expires_at": "2026-12-01T20:06:55Z"},
)
SEMANTIC = {"role": "semantic-checker", "run": "33819301663", "attempt": "1",
            "head": "e8a4de593700a81fb2a026366e349b89b640a6e8",
            "id": 9918207444,
            "name": "task757-p1-semantic-checker-only-v3-success-33819301663-1",
            "archive_bytes": 24694,
            "digest": "sha256:f99fd6ce1172cc349b249ead8dbb8e75c8c8bd8a1b8a0493dfd4596aee5fbf0c",
            "expires_at": "2026-12-02T23:50:18Z"}
TASK712_ARTIFACT = {"role": "task712", "run": "33814194630", "attempt": "1",
                   "head": "5ff2c5a30b604536df12acba8801828a5a7e5fe0",
                   "id": 9915928157,
                   "name": "d972-r07-grade2-maps-v4-33814194630-1",
                   "archive_bytes": 22404961,
                   "digest": "sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858",
                   "expires_at": "2026-10-03T22:41:38Z"}
MARKING_PATH = ROOT / "scratchpad/fuda1_a0_rmax_data.g"
MARKING_SHA = "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"
RELATOR_SHA = "7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"
OCCURRENCES = ((0, 0, 1), (1, 0, 2), (2, 0, 1),
               (3, 1, 2), (4, 1, 2), (5, 1, 1))
OCCURRENCE_WORDS = (
    ((1,), (2,)), ((1,), (-1, -2)), ((2,), (-1, -2)),
    ((-2, -1), (1,)), ((1,), (2,)), ((-2, -1), (2,)),
)
ETA = ((0, 1), (1, 0), (1, 1))


def canon(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def need(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def file_receipt(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw,
         "file_bom_or_cr")
    return {"path": str(path), "bytes": len(raw), "sha256": sha(raw),
            "lf": raw.count(b"\n"), "bom": False, "cr": False}


def digits(value: int) -> tuple[int, int, int, int]:
    need(0 <= value <= 80, "packed_byte")
    return value % 3, (value // 3) % 3, (value // 9) % 3, (value // 27) % 3


DIGITS = np.asarray([digits(i) for i in range(81)], dtype=np.uint8)
AXPY = np.empty((2, 81, 81), dtype=np.uint8)
for _scalar in (1, 2):
    for _left in range(81):
        for _right in range(81):
            AXPY[_scalar - 1, _left, _right] = sum(
                ((int(DIGITS[_left, j]) - _scalar * int(DIGITS[_right, j])) % 3)
                * 3 ** j for j in range(4))
SCALE2 = np.asarray([
    sum((2 * int(DIGITS[i, j]) % 3) * 3 ** j for j in range(4))
    for i in range(81)], dtype=np.uint8)
FIRST_TRIT = np.full(81, -1, dtype=np.int8)
FIRST_VALUE = np.zeros(81, dtype=np.uint8)
for _value in range(1, 81):
    for _position, _digit in enumerate(DIGITS[_value]):
        if _digit:
            FIRST_TRIT[_value] = _position
            FIRST_VALUE[_value] = _digit
            break


def validate_packed(raw: bytes | bytearray | memoryview | np.ndarray,
                    width: int) -> None:
    view = raw.reshape(-1) if isinstance(raw, np.ndarray) else np.frombuffer(raw, dtype=np.uint8)
    need(view.size == (width + 3) // 4 and not np.any(view > 80),
         "packed_shape")
    if width % 4:
        need(int(DIGITS[int(view[-1]), width % 4]) == 0, "packed_padding")


def pack(values: Sequence[int] | np.ndarray, width: int) -> bytes:
    a = np.asarray(values, dtype=np.uint8).reshape(-1)
    need(a.size == width and not np.any(a > 2), "pack_shape")
    result = np.zeros((width + 3) // 4, dtype=np.uint8)
    for position in range(4):
        result[:(width + 3 - position) // 4] += (
            a[position::4] * 3 ** position).astype(np.uint8)
    validate_packed(result, width)
    return result.tobytes()


def unpack(raw: bytes | bytearray | memoryview, width: int) -> np.ndarray:
    validate_packed(raw, width)
    packed = np.frombuffer(raw, dtype=np.uint8)
    result = np.empty(width, dtype=np.uint8)
    for position in range(4):
        result[position::4] = DIGITS[packed, position][:result[position::4].size]
    return result


def axpy(destination: bytearray, source: bytes | bytearray | memoryview,
          scalar: int, width: int) -> None:
    need(scalar in (1, 2) and len(destination) == len(source) == (width + 3) // 4,
         "axpy_shape")
    left = np.frombuffer(destination, dtype=np.uint8)
    right = np.frombuffer(source, dtype=np.uint8)
    # Candidate stores and source rows are authenticated before replay; the
    # packed lookup is total on the authenticated byte alphabet.
    left[:] = AXPY[scalar - 1, left, right]


def unit(index: int) -> bytearray:
    need(0 <= index < ROWS, "unit_index")
    result = bytearray(COEFF_BYTES)
    result[index // 4] = 3 ** (index % 4)
    return result


def first(raw: bytes | bytearray | memoryview, width: int) -> tuple[int, int] | None:
    validate_packed(raw, width)
    packed = np.frombuffer(raw, dtype=np.uint8)
    nonzero = np.flatnonzero(packed)
    if not nonzero.size:
        return None
    byte_index = int(nonzero[0])
    coordinate = 4 * byte_index + int(FIRST_TRIT[int(packed[byte_index])])
    return None if coordinate >= width else (coordinate, int(FIRST_VALUE[int(packed[byte_index])]))


def validate_artifact(value: Any, expected: dict[str, Any], label: str) -> None:
    need(isinstance(value, dict), label + ":type")
    required = {"role", "run", "attempt", "head", "id", "name",
                "archive_bytes", "digest", "expires_at", "repository",
                "run_status", "run_conclusion"}
    need(set(value) == required and value == expected, label + ":identity")


def validate_launch(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("ascii"))
    need(raw == canon(value) and set(value) == {
        "schema", "repository", "p1_artifact", "task554_artifacts",
        "semantic_checker_artifact", "task712_artifact", "source_files",
        "executable_files", "query_receipts"} and value["schema"] == LAUNCH_SCHEMA,
         "launch_shape")
    need(value["repository"] == REPOSITORY and isinstance(value["task554_artifacts"], list)
         and len(value["task554_artifacts"]) == 5, "launch_repository")
    for actual, expected in zip(value["task554_artifacts"], TASK554):
        validate_artifact(actual, {**expected, "repository": REPOSITORY,
                                   "run_status": "completed",
                                   "run_conclusion": "success"}, "launch_task554")
    validate_artifact(value["semantic_checker_artifact"],
                      {**SEMANTIC, "repository": REPOSITORY,
                       "run_status": "completed", "run_conclusion": "success"},
                      "launch_semantic")
    validate_artifact(value["task712_artifact"],
                      {**TASK712_ARTIFACT, "repository": REPOSITORY,
                       "run_status": "completed", "run_conclusion": "success"},
                      "launch_task712")
    p1 = value["p1_artifact"]
    p1_keys = {"role", "repository", "run", "attempt", "head", "id", "name",
               "archive_bytes", "digest", "expires_at", "run_status",
               "run_conclusion", "workflow_run_id", "workflow_run_attempt",
               "workflow_head_sha", "api_verified"}
    need(isinstance(p1, dict) and set(p1) == p1_keys and p1["role"] == "p1-candidate"
         and p1["repository"] == REPOSITORY and p1["run"] == str(p1["workflow_run_id"])
         and p1["attempt"] == str(p1["workflow_run_attempt"])
         and p1["head"] == p1["workflow_head_sha"]
         and p1["run_status"] == "completed" and p1["run_conclusion"] == "success"
         and p1["api_verified"] is True and plain_int(p1["id"]) and p1["id"] > 0
         and isinstance(p1["name"], str) and p1["name"]
         and isinstance(p1["digest"], str) and p1["digest"].startswith("sha256:")
         and isinstance(p1["expires_at"], str) and p1["expires_at"], "launch_p1")
    for item in value["source_files"] + value["executable_files"]:
        need(isinstance(item, dict) and set(item) == {
            "path", "sha256", "bytes", "lf", "bom", "cr"}
             and isinstance(item["path"], str) and item["bom"] is False
             and item["cr"] is False and plain_int(item["bytes"])
             and plain_int(item["lf"]), "launch_file_receipt")
    need(len(value["executable_files"]) == 2 and
         set(value["query_receipts"]) == {
             "p1_run", "p1_artifact", "task554", "semantic_checker", "task712"},
         "launch_receipts")
    return value


def verify_launch_files(launch: dict[str, Any]) -> dict[str, Any]:
    paths = {
        "search/d972_r07_canonical_p1_dag_degree2_lift_v10.py": ROOT / "search/d972_r07_canonical_p1_dag_degree2_lift_v10.py",
        "search/d972_r07_a0_first_rung_grade1_v4.py": ROOT / "search/d972_r07_a0_first_rung_grade1_v4.py",
        "search/d972_r07_a0_first_rung_grade2_prebuild_v1.py": ROOT / "search/d972_r07_a0_first_rung_grade2_prebuild_v1.py",
        "search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py": ROOT / "search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py",
        "search/d972_r07_grade2_specific_owner_prejoin_v1.py": ROOT / "search/d972_r07_grade2_specific_owner_prejoin_v1.py",
        "search/d972_r07_a0_c2fourier_joint_floor_v1.py": ROOT / "search/d972_r07_a0_c2fourier_joint_floor_v1.py",
        "scratchpad/a0_paper_words_v1.json": ROOT / "scratchpad/a0_paper_words_v1.json",
        "search/d972_r07_grade2_forward_adjoint_maps_v3.py": ROOT / "search/d972_r07_grade2_forward_adjoint_maps_v3.py",
        "search/d972_r07_canonical_p1_physical_connection_v5.py": ROOT / "search/d972_r07_canonical_p1_physical_connection_v5.py",
        "search/check_d972_r07_canonical_p1_physical_connection_v5.py": ROOT / "search/check_d972_r07_canonical_p1_physical_connection_v5.py",
        "search/check_d972_r07_canonical_p1_physical_connection_v6.py": ROOT / "search/check_d972_r07_canonical_p1_physical_connection_v6.py",
    }
    all_items = {str(item["path"]): item for item in
                 launch["source_files"] + launch["executable_files"]}
    result = {}
    for relative, path in paths.items():
        item = all_items.get(relative)
        need(item is not None and path.is_file(), "launch_file_missing:" + relative)
        actual = file_receipt(path)
        need(actual["sha256"] == item["sha256"] and actual["bytes"] == item["bytes"]
             and actual["lf"] == item["lf"], "launch_file_mismatch:" + relative)
        result[relative] = actual
    need(set(all_items) == set(paths), "launch_file_roster")
    return result


# ---------------------------------------------------------------------------
# The following quotient and truncated-polynomial code is a local copy of
# the mathematics, with no executable dependency on the producer/upstream.

ID9 = tuple(range(9))
Affine = tuple[tuple[int, ...], int, int, tuple[int, int, int]]


def pmul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(right[index] for index in left)


def pinv(value: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(value)
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)


def winv(word: Iterable[int]) -> tuple[int, ...]:
    return tuple(-int(value) for value in tuple(word)[::-1])


def wproduct(*parts: Iterable[int]) -> tuple[int, ...]:
    result: list[int] = []
    for part in parts:
        for value in part:
            value = int(value)
            need(value in (-2, -1, 1, 2), "word_letter")
            if result and result[-1] == -value:
                result.pop()
            else:
                result.append(value)
    return tuple(result)


def substitute(word: Iterable[int], x: Iterable[int], y: Iterable[int]) -> tuple[int, ...]:
    parts = []
    for value in word:
        parts.append(tuple(x) if value == 1 else tuple(y) if value == 2
                     else winv(x) if value == -1 else winv(y))
    return wproduct(*parts)


def qproduct(left: tuple[tuple[int, ...], int, int], right: tuple[tuple[int, ...], int, int]) -> tuple[tuple[int, ...], int, int]:
    return pmul(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2]


def qinverse(value: tuple[tuple[int, ...], int, int]) -> tuple[tuple[int, ...], int, int]:
    return pinv(value[0]), value[1], value[2]


def qword(word: Iterable[int], images: tuple[tuple[tuple[int, ...], int, int], tuple[tuple[int, ...], int, int]]) -> tuple[tuple[int, ...], int, int]:
    result = (ID9, 0, 0)
    for value in word:
        result = qproduct(result, images[abs(int(value)) - 1] if value > 0
                          else qinverse(images[abs(int(value)) - 1]))
    return result


def character_sign(label: tuple[int, int], parity: tuple[int, int]) -> int:
    return 1 if ((label[0] * parity[0] + label[1] * parity[1]) & 1) == 0 else 2


def kernel_action(parity: tuple[int, int], value: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(character_sign(ETA[index], parity) * value[index] % 3
                 for index in range(3))  # type: ignore[return-value]


def amul(left: Affine, right: Affine) -> Affine:
    acted = kernel_action((right[1], right[2]), left[3])
    return (pmul(left[0], right[0]), left[1] ^ right[1], left[2] ^ right[2],
            tuple((acted[i] + right[3][i]) % 3 for i in range(3)))  # type: ignore[return-value]


def ainverse(value: Affine) -> Affine:
    acted = kernel_action((value[1], value[2]), value[3])
    return (pinv(value[0]), value[1], value[2],
            tuple((-x) % 3 for x in acted))  # type: ignore[return-value]


def aword(word: Iterable[int], images: tuple[Affine, Affine]) -> Affine:
    result: Affine = (ID9, 0, 0, (0, 0, 0))
    inverse = ainverse(images[0]), ainverse(images[1])
    for value in word:
        result = amul(result, images[abs(int(value)) - 1] if value > 0
                      else inverse[abs(int(value)) - 1])
    return result


def m2product(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return ((left[0][0] * right[0][0] ^ left[0][1] * right[1][0],
             left[0][0] * right[0][1] ^ left[0][1] * right[1][1]),
            (left[1][0] * right[0][0] ^ left[1][1] * right[1][0],
             left[1][0] * right[0][1] ^ left[1][1] * right[1][1]))


def marking_generators() -> tuple[tuple[int, ...], tuple[int, ...]]:
    raw = MARKING_PATH.read_bytes()
    need(sha(raw) == MARKING_SHA, "marking_pin")
    match = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;",
                      raw.decode("utf-8"), re.S)
    need(match is not None, "marking_syntax")
    values = [tuple(int(x) - 1 for x in ast.literal_eval(match.group(i)))
              for i in (1, 2)]
    need(all(len(value) == 36 for value in values), "marking_width")
    return values[0][:9], values[1][:9]


def enumerate_psl(generators: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[tuple[tuple[int, ...], ...], dict[tuple[int, ...], int]]:
    steps = (generators[0], generators[1], pinv(generators[0]), pinv(generators[1]))
    seen = {ID9: 0}
    values = [ID9]
    todo: deque[tuple[int, ...]] = deque([ID9])
    while todo:
        current = todo.popleft()
        for step in steps:
            candidate = pmul(current, step)
            if candidate not in seen:
                seen[candidate] = len(values)
                values.append(candidate)
                todo.append(candidate)
    need(len(values) == 504, "psl_cardinality")
    return tuple(values), seen


class IndependentContext:
    def __init__(self, words: dict[str, Any]):
        first, second = marking_generators()
        qimages = ((first, 1, 0), (second, 0, 1))
        aimages: tuple[Affine, Affine] = (
            (first, 1, 0, (1, 0, 0)), (second, 0, 1, (1, 1, 1)))
        self.psl, self.psl_index = enumerate_psl((first, second))
        self.transport: list[dict[tuple[int, int], tuple[int, int]]] = []
        for left_word, right_word in OCCURRENCE_WORDS:
            left, right = qword(left_word, qimages), qword(right_word, qimages)
            matrix = ((left[1], right[1]), (left[2], right[2]))
            inverse = None
            for a in range(2):
                for b in range(2):
                    for c in range(2):
                        for d in range(2):
                            candidate = ((a, b), (c, d))
                            if (m2product(matrix, candidate) == ((1, 0), (0, 1))
                                    and m2product(candidate, matrix) == ((1, 0), (0, 1))):
                                inverse = candidate
            need(inverse is not None, "transport_inverse")
            self.transport.append({
                label: ((label[0] * inverse[0][0]) ^ (label[1] * inverse[1][0]),
                        (label[0] * inverse[0][1]) ^ (label[1] * inverse[1][1]))
                for label in CHARACTERS})
        self.source_actor = {letter: qword((letter,), qimages) for letter in ACTORS}
        self.actor_tags = {
            letter: tuple(aword(substitute((letter,), *pair), aimages)
                          for pair in OCCURRENCE_WORDS) for letter in ACTORS}
        g = tuple(int(value) for value in words.get("g760", ()))
        need(len(g) == 760, "g760_cardinality")
        gtags = tuple(aword(substitute(g, *pair), aimages)
                      for pair in OCCURRENCE_WORDS)
        identity: Affine = (ID9, 0, 0, (0, 0, 0))
        self.shifts = (identity, gtags[2], gtags[2],
                       amul(gtags[5], ainverse(gtags[4])), gtags[5], gtags[5])
        self.maps: dict[tuple[int, ...], tuple[int, ...]] = {}

    def left_map(self, permutation: tuple[int, ...]) -> tuple[int, ...]:
        if permutation not in self.maps:
            self.maps[permutation] = tuple(
                self.psl_index[pmul(permutation, value)] for value in self.psl)
        return self.maps[permutation]


MONOMIALS_LE2 = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)) + MONOMIALS
MONOMIAL_INDEX = {value: index for index, value in enumerate(MONOMIALS_LE2)}
PRODUCT_INDEX = [[-1] * 10 for _ in range(10)]
for _left, _left_value in enumerate(MONOMIALS_LE2):
    for _right, _right_value in enumerate(MONOMIALS_LE2):
        product = tuple(_left_value[i] + _right_value[i] for i in range(3))
        if sum(product) <= 2 and max(product) <= 2:
            PRODUCT_INDEX[_left][_right] = MONOMIAL_INDEX[product]


def add_mod3(destination: np.ndarray, source: np.ndarray, scalar: int = 1) -> None:
    destination[:] = (destination.astype(np.uint16) + (scalar % 3) * source.astype(np.uint16)) % 3


def multiply_polynomial(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    result = np.zeros(10, dtype=np.uint8)
    for i in np.flatnonzero(left):
        for j in np.flatnonzero(right):
            target = PRODUCT_INDEX[int(i)][int(j)]
            if target >= 0:
                result[target] = (int(result[target]) + int(left[i]) * int(right[j])) % 3
    return result


def multiply_rows(factor: np.ndarray, rows: np.ndarray) -> np.ndarray:
    result = np.zeros_like(rows)
    for left in np.flatnonzero(factor):
        for right in range(10):
            target = PRODUCT_INDEX[int(left)][right]
            if target >= 0:
                add_mod3(result[:, target, :], rows[:, right, :], int(factor[left]))
    return result


def e_polynomial(vector: tuple[int, int, int]) -> np.ndarray:
    result = np.zeros(10, dtype=np.uint8)
    result[0] = 1
    for variable, raw in enumerate(vector):
        exponent = int(raw) % 3
        factor = np.zeros(10, dtype=np.uint8)
        factor[0] = 1
        if exponent:
            linear = [0, 0, 0]
            linear[variable] = 1
            factor[MONOMIAL_INDEX[tuple(linear)]] = exponent
        if exponent == 2:
            quadratic = [0, 0, 0]
            quadratic[variable] = 2
            factor[MONOMIAL_INDEX[tuple(quadratic)]] = 1
        result = multiply_polynomial(result, factor)
    return result


def source_index(tag: int, component: int, monomial: int, psl: int) -> int:
    return (((tag * 2 + component) * 6 + monomial) * 504) + psl


def physical_index(character: int, block: int, component: int,
                   monomial: int, psl: int) -> int:
    """Map one physical coordinate to its canonical pure-grade index."""
    need(0 <= character < 4 and 0 <= block < 2 and 0 <= component < 2
         and 0 <= monomial < 6 and 0 <= psl < 504, "physical_coordinate")
    return ((((character * 2 + block) * 2 + component) * 6 + monomial)
            * 504) + psl


def source_view(d0: np.ndarray, d1: np.ndarray, d2: np.ndarray,
                character: int, tag: int) -> np.ndarray:
    result = np.zeros((2, 10, 504), dtype=np.uint8)
    for component in (0, 1):
        base = (tag * 2 + component) * 504
        result[component, 0] = d0[character, base:base + 504]
        for monomial in range(3):
            start = ((tag * 2 + component) * 3 + monomial) * 504
            result[component, 1 + monomial] = d1[character, start:start + 504]
        for monomial in range(6):
            start = source_index(tag, component, monomial, 0)
            result[component, 4 + monomial] = d2[character, start:start + 504]
    return result


def aggregate(ctx: IndependentContext, d0: np.ndarray, d1: np.ndarray,
              d2: np.ndarray, auxiliary: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    output = np.zeros((4, 2, 2, 10, 504), dtype=np.uint8)
    for tag, block, sign in OCCURRENCES:
        shift = ctx.shifts[tag]
        raw = np.zeros((4, 2, 10, 504), dtype=np.uint8)
        for parity_index, parity in enumerate(CHARACTERS):
            for source_character, source_label in enumerate(CHARACTERS):
                add_mod3(raw[parity_index], source_view(d0, d1, d2,
                        source_character, tag), character_sign(
                            ctx.transport[tag][source_label], parity))
        acted = np.zeros_like(raw)
        pmap = ctx.left_map(shift[0])
        for parity_index, parity in enumerate(CHARACTERS):
            target = (parity[0] ^ shift[1], parity[1] ^ shift[2])
            kernel = tuple(character_sign(ETA[i], parity) * shift[3][i] % 3
                           for i in range(3))
            product = multiply_rows(e_polynomial(kernel), raw[parity_index])
            translated = np.zeros_like(product)
            translated[:, :, pmap] = product
            add_mod3(acted[CHARACTERS.index(target)], translated)
        for character, label in enumerate(CHARACTERS):
            transformed = np.zeros((2, 10, 504), dtype=np.uint8)
            for parity_index, parity in enumerate(CHARACTERS):
                add_mod3(transformed, acted[parity_index], sign *
                         character_sign(label, parity))
            add_mod3(output[character, block], transformed)
    physical0 = np.zeros(8064, dtype=np.uint8)
    physical1 = np.zeros(24192, dtype=np.uint8)
    physical2 = np.zeros(TOP_WIDTH, dtype=np.uint8)
    for character in range(4):
        for block in range(2):
            for component in (0, 1):
                start0 = ((character * 2 + block) * 2 + component) * 504
                physical0[start0:start0 + 504] = output[character, block, component, 0]
                for monomial in range(3):
                    start1 = (((character * 2 + block) * 2 + component) * 3 + monomial) * 504
                    physical1[start1:start1 + 504] = output[character, block, component, 1 + monomial]
                for monomial in range(6):
                    start2 = ((((character * 2 + block) * 2 + component) * 6 + monomial) * 504)
                    physical2[start2:start2 + 504] = output[character, block, component, 4 + monomial]
    physical_aux = np.zeros(4, dtype=np.uint8)
    for tag, block, sign in OCCURRENCES:
        physical_aux[block] = (int(physical_aux[block]) + sign * int(auxiliary[tag])) % 3
    physical_aux[2:] = auxiliary[6:]
    return physical0, physical1, physical2, physical_aux


def occurrence_records(ctx: IndependentContext, character: int) -> list[tuple[int, int, int]]:
    """Reconstruct the complete pure-grade occurrence-side map independently."""
    label = CHARACTERS[character]
    raw: list[tuple[int, int, int]] = []
    for tag, block, occurrence_coefficient in OCCURRENCES:
        target = ctx.transport[tag][label]
        target_character = CHARACTERS.index(target)
        shift = ctx.shifts[tag]
        scalar = occurrence_coefficient * character_sign(target, (shift[1], shift[2]))
        pmap = ctx.left_map(shift[0])
        for component in range(2):
            for monomial in range(6):
                base = source_index(tag, component, monomial, 0)
                for psl, destination_psl in enumerate(pmap):
                    raw.append((base + psl,
                                physical_index(target_character, block, component,
                                               monomial, destination_psl), scalar))
    sums: dict[tuple[int, int], int] = {}
    for source, destination, coefficient in raw:
        key = (source, destination)
        sums[key] = (sums.get(key, 0) + coefficient) % 3
    return [(source, destination, coefficient)
            for (source, destination), coefficient in sorted(sums.items())
            if coefficient]


def fixture_expected_occurrence_records(
        ctx: IndependentContext, character: int) -> list[tuple[int, int, int]]:
    """Independent fixed-layout oracle for the bounded production fixture."""
    label = CHARACTERS[character]
    raw: list[tuple[int, int, int]] = []
    for tag, block, occurrence_coefficient in OCCURRENCES:
        target = ctx.transport[tag][label]
        target_character = CHARACTERS.index(target)
        shift = ctx.shifts[tag]
        scalar = occurrence_coefficient * character_sign(
            target, (shift[1], shift[2]))
        pmap = ctx.left_map(shift[0])
        for component in range(2):
            for monomial in range(6):
                base = source_index(tag, component, monomial, 0)
                for psl, destination_psl in enumerate(pmap):
                    # This literal layout is the immutable bounded-fixture
                    # oracle; occurrence_records must use its own function.
                    destination = (((((target_character * 2 + block) * 2
                                       + component) * 6 + monomial) * 504)
                                   + destination_psl)
                    raw.append((base + psl, destination, scalar))
    sums: dict[tuple[int, int], int] = {}
    for source, destination, coefficient in raw:
        key = (source, destination)
        sums[key] = (sums.get(key, 0) + coefficient) % 3
    return [(source, destination, coefficient)
            for (source, destination), coefficient in sorted(sums.items())
            if coefficient]


def compare_complete_restriction(actual: Sequence[Sequence[int]],
                                 expected: Sequence[Sequence[int]],
                                 source_width: int = 36288,
                                 destination_width: int = TOP_WIDTH,
                                 label: str = "task712_complete_map") -> dict[str, int]:
    """Compare every entry and explicitly traverse every source column."""
    actual_rows = [tuple(int(value) for value in row) for row in actual]
    expected_rows = [tuple(int(value) for value in row) for row in expected]
    need(actual_rows == expected_rows, label + ":entry")
    actual_columns = [[] for _ in range(source_width)]
    expected_columns = [[] for _ in range(source_width)]
    for source, destination, coefficient in actual_rows:
        need(0 <= source < source_width and 0 <= destination < destination_width
             and coefficient in (1, 2), label + ":range")
        actual_columns[source].append((destination, coefficient))
    for source, destination, coefficient in expected_rows:
        need(0 <= source < source_width and 0 <= destination < destination_width
             and coefficient in (1, 2), label + ":expected_range")
        expected_columns[source].append((destination, coefficient))
    for source in range(source_width):
        need(actual_columns[source] == expected_columns[source],
             label + ":column:" + str(source))
    return {"source_columns": source_width, "entries": len(actual_rows)}


# ---------------------------------------------------------------------------
# Task712 and Task554 data readers.  These read sealed files as data only.


class Task712Tables:
    @staticmethod
    def _spec(name: str) -> tuple[str, int, int | None, int, int, str]:
        need(name in Task712Tables.names(), "task712_unknown_table")
        match = re.fullmatch(
            r"(?P<kind>T|B)_(?P<direction>fwd|adj)_a(?P<character>[0-3])"
            r"(?:_t(?P<actor>[0-3]))?\.jsonl", name)
        need(match is not None, "task712_name_syntax")
        kind = match.group("kind")
        direction = "adjoint" if match.group("direction") == "adj" else "forward"
        character = int(match.group("character"))
        actor = int(match.group("actor")) if match.group("actor") is not None else None
        need((kind == "T") == (actor is not None), "task712_actor_shape")
        source_width, destination_width = ((36288, 36288) if kind == "T" else
                                           ((36288, TOP_WIDTH) if direction == "forward" else
                                            (TOP_WIDTH, 36288)))
        return kind, character, actor, source_width, destination_width, direction

    def __init__(self, root: Path):
        self.root = root.resolve()
        files = [path for path in self.root.rglob("*")
                 if path.is_file() and not path.is_symlink()]
        manifests = []
        for path in files:
            if path.name != "manifest.json":
                continue
            try:
                value = json.loads(path.read_bytes().decode("ascii"))
            except Exception:
                continue
            if isinstance(value, dict) and value.get("table_count") == 40:
                manifests.append((path, value))
        need(len(manifests) == 1, "task712_manifest")
        self.manifest_path, self.manifest = manifests[0]
        raw = self.manifest_path.read_bytes()
        need(raw == canon(self.manifest)
             and self.manifest.get("schema") == "d972.r07.grade2.forward-adjoint-maps.v3"
             and self.manifest.get("marker") == "R07_GRADE2_FORWARD_ADJOINT_MAPS_V3_CANDIDATE"
             and self.manifest.get("map_count") == 20, "task712_manifest_identity")
        expected_names = self.names()
        need(self.manifest.get("table_roster") == expected_names, "task712_roster")
        descriptors = {str(item.get("file")): item for item in self.manifest.get("tables", [])
                       if isinstance(item, dict)}
        need(set(descriptors) == set(expected_names), "task712_descriptor_roster")
        self.tables: dict[int, list[tuple[int, int, int]]] = {}
        self.table_records: dict[str, list[tuple[int, int, int]]] = {}
        self.table_hashes: dict[str, str] = {}
        for name in expected_names:
            matches = [path for path in files if path.name == name]
            need(len(matches) == 1 and name in descriptors, "task712_table_missing:" + name)
            kind, character, actor_number, source_width, destination_width, direction = self._spec(name)
            records = self._read_table(matches[0], descriptors[name], source_width,
                                       destination_width, kind, direction,
                                       character, actor_number)
            self.table_records[name] = records
            self.table_hashes[name] = sha(matches[0].read_bytes())
            if name.startswith("B_fwd_a"):
                self.tables[character] = records
        checker = []
        for path in files:
            if "checker" in path.name and path.suffix == ".json":
                try:
                    value = json.loads(path.read_bytes().decode("ascii"))
                except Exception:
                    continue
                if isinstance(value, dict) and value.get("tables_checked") == 40:
                    checker.append((path, value))
        need(len(checker) == 1 and checker[0][1].get("marker") ==
             "R07_GRADE2_FORWARD_ADJOINT_MAPS_V4_CHECKER_PASS", "task712_checker")
        receipts = []
        for path in files:
            if "receipt" not in path.name or path.suffix != ".json":
                continue
            try:
                value = json.loads(path.read_bytes().decode("ascii"))
            except Exception:
                continue
            if isinstance(value, dict) and value.get("schema") == "d972.r07.grade2.forward-adjoint-maps.v4.workflow-receipt":
                receipts.append((path, value))
        need(len(receipts) == 1 and receipts[0][1].get("table_count") == 40
             and receipts[0][1].get("map_count") == 20, "task712_workflow_receipt")
        self.receipt = {"manifest_sha256": sha(raw),
                        "checker_sha256": sha(checker[0][0].read_bytes()),
                        "workflow_sha256": sha(receipts[0][0].read_bytes()),
                        "table_files": dict(self.table_hashes)}

    @staticmethod
    def names() -> list[str]:
        result = []
        for character in range(4):
            for actor in range(4):
                result.extend((f"T_fwd_a{character}_t{actor}.jsonl",
                               f"T_adj_a{character}_t{actor}.jsonl"))
            result.extend((f"B_fwd_a{character}.jsonl",
                           f"B_adj_a{character}.jsonl"))
        return result

    @staticmethod
    def _read_table(path: Path, receipt: dict[str, Any], source_width: int,
                     destination_width: int, kind: str, direction: str,
                     character: int, actor_number: int | None) -> list[tuple[int, int, int]]:
        required = {"file", "schema", "source_width", "destination_width",
                    "entry_count", "body_bytes", "body_sha256", "bytes",
                    "sha256", "eof", "encoding", "map_kind", "map_direction",
                    "character"}
        if path.name.startswith("T_"):
            required.add("actor")
        need(set(receipt) == required and receipt["file"] == path.name
             and receipt["source_width"] == source_width
             and receipt["destination_width"] == destination_width
             and receipt["schema"] == "d972.r07.grade2.forward-adjoint-maps.v3.sparse-jsonl"
             and receipt["encoding"] == "jsonl-triples-utf8-lf"
             and receipt["map_kind"] == kind
             and receipt["map_direction"] == direction
             and receipt["character"] == character
             and (kind != "T" or receipt["actor"] == ACTORS[actor_number])
             and receipt["eof"] is True, "task712_table_receipt")
        for key in ("source_width", "destination_width", "entry_count", "body_bytes",
                    "bytes", "character") + (("actor",) if kind == "T" else ()):
            need(plain_int(receipt[key]), "task712_table_type")
        raw = path.read_bytes()
        body = hashlib.sha256(); body_bytes = 0; previous = None; rows = []
        eof = None
        for line in raw.splitlines(keepends=True):
            need(line.endswith(b"\n") and line != b"\n" and b"\r" not in line,
                 "task712_table_lf")
            value = json.loads(line.decode("ascii"))
            if isinstance(value, dict):
                need(eof is None and set(value) == {"body_bytes", "body_sha256",
                     "count", "eof"} and value["eof"] is True
                     and line == canon(value), "task712_table_eof")
                eof = value
                continue
            need(eof is None and isinstance(value, list) and len(value) == 3
                  and all(plain_int(x) for x in value), "task712_table_row")
            row = tuple(int(x) for x in value)
            need(0 <= row[0] < source_width and 0 <= row[1] < destination_width
                 and row[2] in (1, 2) and (previous is None or row[:2] > previous)
                 and line == (json.dumps(list(row), separators=(",", ":")) + "\n").encode("ascii"),
                 "task712_table_order")
            previous = row[:2]; rows.append(row); body.update(line); body_bytes += len(line)
        need(eof is not None and plain_int(eof["count"]) and plain_int(eof["body_bytes"])
             and eof["count"] == len(rows)
             and eof["body_bytes"] == body_bytes and eof["body_sha256"] == body.hexdigest()
             and receipt["entry_count"] == len(rows) and receipt["body_bytes"] == body_bytes
             and receipt["body_sha256"] == body.hexdigest() and receipt["bytes"] == len(raw)
             and receipt["sha256"] == sha(raw), "task712_table_digest")
        return rows

    def pure(self, character: int, source: np.ndarray) -> np.ndarray:
        need(source.shape == (36288,), "task712_pure_source")
        output = np.zeros(TOP_WIDTH, dtype=np.uint8)
        for source_index, destination, coefficient in self.tables[character]:
            output[destination] = (int(output[destination]) + coefficient *
                                   int(source[source_index])) % 3
        return output

    def restriction(self, d2: np.ndarray) -> np.ndarray:
        need(d2.shape == (4, 36288), "task712_restriction_shape")
        output = np.zeros(TOP_WIDTH, dtype=np.uint8)
        for character in range(4):
            output = (output + self.pure(character, d2[character])) % 3
        return output


def validate_complete_task712_maps(task712: Task712Tables,
                                   context: IndependentContext) -> dict[str, int]:
    totals = {"source_columns": 0, "entries": 0}
    for character in range(4):
        expected = occurrence_records(context, character)
        receipt = compare_complete_restriction(
            task712.table_records[f"B_fwd_a{character}.jsonl"], expected,
            label=f"task712_complete_map_a{character}")
        totals["source_columns"] += receipt["source_columns"]
        totals["entries"] += receipt["entries"]
    return totals


def read_state(root: Path, stem: str, expected: str,
               parent: str | None) -> dict[str, Any]:
    root = root.resolve(); head_path = root / f"{stem}.HEAD"
    body_path = root / f"{stem}.{expected}.json"
    head_raw = head_path.read_bytes(); body_raw = body_path.read_bytes()
    head = json.loads(head_raw.decode("ascii")); body = json.loads(body_raw.decode("ascii"))
    need(head_raw == canon(head) and body_raw == canon(body)
         and sha(body_raw) == expected and head == {
             "body_sha256": expected, "parent_sha256": parent,
             "schema": "d972.r07.a0.first-rung-grade1.v3.state.head",
             "stem": stem}, "task554_state_head")
    need(body.get("schema") == "d972.r07.a0.first-rung-grade1.v3.state"
         and body.get("phase") == ("prepare" if stem == "prepare" else "block"),
         "task554_state_body")
    return {"root": root, "body": body}


class MappedBlob:
    def __init__(self, path: Path, expected_bytes: int, expected_sha: str):
        self.stream = path.open("rb")
        need(path.stat().st_size == expected_bytes and file_digest(path) == expected_sha,
             "task554_blob_digest")
        self.map = mmap.mmap(self.stream.fileno(), 0, access=mmap.ACCESS_READ)

    def close(self) -> None:
        self.map.close(); self.stream.close()


def blob_row(state: dict[str, Any], local: int, receipt: dict[str, Any],
             width: int, rows: int) -> np.ndarray:
    required = {"file", "bytes", "sha256", "rows", "width", "encoding"}
    need(isinstance(receipt, dict) and set(receipt) == required
         and isinstance(receipt["file"], str) and Path(receipt["file"]).name == receipt["file"]
         and receipt["rows"] == rows and receipt["width"] == width
         and receipt["bytes"] == rows * (width // 4)
         and receipt["encoding"] == "base3-four-trits-per-byte"
         and plain_int(local) and 0 <= local < rows, "task554_blob_receipt")
    blobs = state.setdefault("blob_maps", {})
    if receipt["file"] not in blobs:
        blobs[receipt["file"]] = MappedBlob(state["root"] / receipt["file"],
                                             receipt["bytes"], receipt["sha256"])
    raw = blobs[receipt["file"]].map
    start = local * (width // 4)
    return unpack(raw[start:start + width // 4], width)


class Task554Rows:
    """Independent Task554 state reader and precision-one row selector."""
    def __init__(self, prepare_root: Path, block_roots: Sequence[Path]):
        self.prepare = read_state(prepare_root, "prepare", PREPARE_DIGEST, None)
        self.blocks = [read_state(path, f"block-{index}", PARENTS[index], PREPARE_DIGEST)
                       for index, path in enumerate(block_roots)]
        body = self.prepare["body"]
        old = body.get("old_blocks")
        need(isinstance(old, list) and len(old) == 4, "task554_old_roster")
        need([item.get("rank") for item in old] == list(OLD_RANKS), "task554_old_ranks")
        need([item["body"].get("rank") for item in self.blocks] == list(NEW_RANKS),
             "task554_new_ranks")

    def close(self) -> None:
        for state in [self.prepare, *self.blocks]:
            for blob in state.get("blob_maps", {}).values():
                blob.close()

    def row(self, index: int) -> np.ndarray:
        need(0 <= index < ROWS, "task554_row_index")
        if index < ORDER[4]:
            character = max(i for i in range(4) if ORDER[i] <= index)
            local = index - ORDER[character]
            old = self.prepare["body"]["old_blocks"][character]
            lower = blob_row(self.prepare, local, old["lower_basis_blob"], 6056,
                             OLD_RANKS[character])
            grade = blob_row(self.prepare, local, old["lifted_grade_blob"], 72576,
                             OLD_RANKS[character])
            degree0 = np.zeros(24192, dtype=np.uint8)
            degree0[character * 6048:(character + 1) * 6048] = lower[:6048]
            return np.concatenate((degree0, grade, lower[-8:]))
        character = max(i for i in range(4) if ORDER[4 + i] <= index)
        local = index - ORDER[4 + character]
        basis = blob_row(self.blocks[character], local,
                         self.blocks[character]["body"]["basis_blob"], 18144,
                         NEW_RANKS[character])
        degree1 = np.zeros(72576, dtype=np.uint8)
        degree1[character * 18144:(character + 1) * 18144] = basis
        return np.concatenate((np.zeros(24192, dtype=np.uint8), degree1,
                               np.zeros(8, dtype=np.uint8)))


P1_INSTRUCTION_KEYS = {"node", "origin", "reductions", "scale",
                       "raw_origin_sha256", "raw_origin_components_sha256",
                       "literal_input_sha256", "old_defect_literal_input_sha256",
                       "parent_row_sha256", "packet_sha256", "packet_row_sha256",
                       "reduction_parent_sha256", "p1_sha256", "offset", "length",
                       "row_receipt", "predecessor", "ancestry_sha256"}
P1_MANIFEST_KEYS = {"schema", "status", "producer_sha256", "semantic_file_hashes",
                    "imports", "launch_manifest_sha256", "checker_result_sha256",
                    "checker_workflow_receipt_sha256", "checker_success_artifact",
                    "semantic_receipt_sha256", "executable_hashes", "raw_artifacts",
                    "raw_file_registry", "source_ancestry", "character_order",
                    "actor_order", "monomial_order", "global_order", "rows",
                    "row_trits", "row_bytes", "instruction", "cache",
                    "ancestry_sha256", "independent_checker", "A0", "COMMON",
                     "COFINAL", "FAKE", "IHARA", "verified"}


class BoundedTask712:
    """Tiny complete-map stand-in used only by the bounded public adapter."""
    def __init__(self) -> None:
        self.tables = {character: [] for character in range(4)}
        self.receipt = {"fixture": "complete-task712-structural-map",
                        "table_count": 40, "map_count": 20,
                        "table_roster": Task712Tables.names()}

    def pure(self, character: int, source: np.ndarray) -> np.ndarray:
        need(source.shape == (36288,), "bounded_task712_source")
        return np.zeros(TOP_WIDTH, dtype=np.uint8)

    def restriction(self, d2: np.ndarray) -> np.ndarray:
        need(d2.shape == (4, 36288), "bounded_task712_restriction")
        result = np.zeros(TOP_WIDTH, dtype=np.uint8)
        for character in range(4):
            result = (result + self.pure(character, d2[character])) % 3
        return result


class BoundedProductionTask712(BoundedTask712):
    """Complete-map stand-in injected only into the ordinary adapter init."""
    def __init__(self, records: dict[int, list[tuple[int, int, int]]]) -> None:
        super().__init__()
        self.table_records = {name: [] for name in Task712Tables.names()}
        for character in range(4):
            values = list(records[character])
            self.table_records[f"B_fwd_a{character}.jsonl"] = values
            self.tables[character] = values
        self.receipt = {"fixture": "production-shaped-complete-task712",
                        "table_count": 40, "map_count": 20,
                        "table_roster": Task712Tables.names()}


class PhysicalSourceAdapter:
    """Actual P1-v10 row path; all counters are incremented in ``pair``."""
    def __init__(self, p1_root: Path, prepare_root: Path,
                 block_roots: Sequence[Path], words_path: Path,
                 task712_root: Path, launch: dict[str, Any] | None = None,
                 *, fixture_context: IndependentContext | None = None,
                 fixture_task712: BoundedProductionTask712 | None = None):
        self.p1_root = p1_root.resolve()
        fixture = fixture_context is not None or fixture_task712 is not None
        need(fixture_context is None or fixture_task712 is not None,
             "bounded_fixture_dependencies")
        if fixture:
            self.task554 = None
            self.context = fixture_context
            self.task712 = fixture_task712
        else:
            self.task554 = Task554Rows(prepare_root, block_roots)
            self.context = IndependentContext(
                json.loads(words_path.read_text("ascii")))
            self.task712 = Task712Tables(task712_root)
        self.complete_map_receipt = validate_complete_task712_maps(self.task712,
                                                                    self.context)
        self.task712.receipt["complete_map"] = self.complete_map_receipt
        if fixture:
            self.p1_identity = {"fixture": "production-shaped-p1"}
            self.task712_identity = {
                "fixture": "production-shaped-complete-task712",
                "complete_map": self.complete_map_receipt}
            self.pair_calls = 0
            self.node_hits: dict[int, int] = {}
            self.restriction_checked = False
            return
        self.cache_file = (self.p1_root / "degree2.cache.bin").open("rb")
        need((self.p1_root / "degree2.cache.bin").stat().st_size == ROWS * D2_BYTES,
             "p1_cache_size")
        self.cache = mmap.mmap(self.cache_file.fileno(), 0, access=mmap.ACCESS_READ)
        self.instructions = self._read_instructions()
        self.p1_identity = {
            "artifact": launch["p1_artifact"] if launch is not None else {},
            "manifest_sha256": sha((self.p1_root / "manifest.json").read_bytes()),
            "cache_sha256": file_digest(self.p1_root / "degree2.cache.bin"),
            "instruction": {key: value for key, value in self.p1_manifest["instruction"].items() if key != "path"},
            "ancestry_sha256": self.p1_manifest["ancestry_sha256"],
        }
        self.task712_identity = {**TASK712_ARTIFACT, "tables": self.task712.receipt}
        self.pair_calls = 0
        self.node_hits: dict[int, int] = {}
        self.restriction_checked = False

    @classmethod
    def bounded_fixture(cls, rows: Sequence[tuple[bytes, bytes, dict[str, Any]]]) -> "PhysicalSourceAdapter":
        obj = cls.__new__(cls)
        obj._fixture_rows = list(rows)
        obj.pair_calls = 0
        obj.node_hits = {}
        obj.restriction_checked = False
        obj.p1_identity = {"fixture": "production-shaped-p1"}
        obj.task712_identity = {"fixture": "complete-task712-structural-map"}
        obj.task712 = BoundedTask712()
        return obj

    def _read_instructions(self) -> list[dict[str, Any]]:
        path = self.p1_root / "instructions.jsonl"
        need(path.is_file(), "p1_instruction_missing")
        result = []
        previous = ZERO_HEAD
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for node in range(ROWS):
                line = stream.readline()
                need(line and line.endswith(b"\n") and b"\r" not in line,
                     "p1_instruction_lf")
                value = json.loads(line.decode("ascii"))
                need(line == canon(value) and set(value) == P1_INSTRUCTION_KEYS
                     and plain_int(value["node"]) and value["node"] == node, "p1_instruction_shape")
                row = self.cache[node * D2_BYTES:(node + 1) * D2_BYTES]
                receipt = value["row_receipt"]
                need(isinstance(receipt, dict) and set(receipt) == {
                    "offset", "length", "sha256"} and receipt["offset"] == node * D2_BYTES
                     and receipt["length"] == D2_BYTES and sha(row) == receipt["sha256"],
                     "p1_cache_row_receipt")
                unsigned = dict(value); unsigned.pop("ancestry_sha256")
                head = sha(bytes.fromhex(previous) + canon(unsigned))
                need(value["predecessor"] == previous and value["ancestry_sha256"] == head,
                     "p1_instruction_ancestry")
                digest.update(line); result.append(value); previous = head
            need(stream.read(1) == b"", "p1_instruction_eof")
        manifest_path = self.p1_root / "manifest.json"
        manifest_raw = manifest_path.read_bytes(); manifest = json.loads(manifest_raw.decode("ascii"))
        expected_imports = {"grade1_v4": SOURCE_HASHES["grade1_v4"], "grade2_prebuild_v1": SOURCE_HASHES["prebuild_v1"], "semantic_v5": SOURCE_HASHES["semantic_v5"], "structural_v1": SOURCE_HASHES["structural_v1"], "floor_v1": SOURCE_HASHES["floor_v1"]}
        expected_semantic = {"grade1_v4": SOURCE_HASHES["grade1_v4"], "grade2_prebuild_v1": SOURCE_HASHES["prebuild_v1"], "semantic_v5": SOURCE_HASHES["semantic_v5"], "checker_v5": "bc60882b3ee22aa449c51cc280491b3d66df384a814a7033e418454f66900f97", "structural_v1": SOURCE_HASHES["structural_v1"], "floor_v1": SOURCE_HASHES["floor_v1"], "words": SOURCE_HASHES["words"]}
        need(manifest_raw == canon(manifest) and set(manifest) == P1_MANIFEST_KEYS
             and manifest.get("schema") == P1_SCHEMA
             and manifest.get("status") == P1_STATUS and manifest.get("rows") == ROWS
             and manifest.get("row_trits") == D2_WIDTH and manifest.get("row_bytes") == D2_BYTES
             and manifest.get("producer_sha256") == P1_V10_SHA
             and manifest.get("imports") == expected_imports
             and manifest.get("semantic_file_hashes") == expected_semantic
             and manifest.get("executable_hashes") == {"producer_v8": P1_V10_SHA, "semantic_v5": SOURCE_HASHES["semantic_v5"], "checker_v5": expected_semantic["checker_v5"]}
             and manifest.get("source_ancestry") == source_ancestry()
             and all(manifest.get(key) is False for key in ("A0", "COMMON", "COFINAL", "FAKE", "IHARA", "verified"))
             and manifest.get("instruction", {}).get("sha256") == digest.hexdigest()
             and manifest.get("instruction", {}).get("rows") == ROWS
             and manifest.get("instruction", {}).get("final_head") == previous
             and manifest.get("instruction", {}).get("final_lf") is True
             and manifest.get("instruction", {}).get("eof") is True
             and manifest.get("cache", {}).get("path") == "degree2.cache.bin"
             and manifest.get("cache", {}).get("rows") == ROWS
             and manifest.get("cache", {}).get("bytes") == ROWS * D2_BYTES
             and manifest.get("cache", {}).get("sha256") == file_digest(self.p1_root / "degree2.cache.bin")
             and manifest.get("cache", {}).get("final_lf") is False
             and manifest.get("cache", {}).get("eof") is True
             and manifest.get("ancestry_sha256") == previous, "p1_manifest_receipt")
        self.p1_manifest = manifest
        return result

    def pair(self, index: int) -> tuple[bytes, bytes, dict[str, Any]]:
        self.pair_calls += 1
        self.node_hits[index] = self.node_hits.get(index, 0) + 1
        if hasattr(self, "_fixture_rows"):
            ell, top, source = self._fixture_rows[index]
            need(set(source) == {"node", "instruction_sha256", "p1_sha256", "cache_row_sha256", "predecessor", "ancestry_sha256"} and plain_int(source["node"]) and source["node"] == index, "fixture_source_shape")
            validate_packed(ell, ELL_WIDTH); validate_packed(top, TOP_WIDTH); d2=np.zeros((4,36288),dtype=np.uint8); need(np.array_equal(self.task712.restriction(d2),np.zeros(TOP_WIDTH,dtype=np.uint8)),"task712_full_restriction_fixture")
            return ell, top, dict(source)
        p1_row = self.task554.row(index)
        meta = self.instructions[index]
        packed_p1 = pack(p1_row, P1_WIDTH)
        need(sha(packed_p1) == meta["p1_sha256"], "pair_p1_source_receipt")
        cache_row = self.cache[index * D2_BYTES:(index + 1) * D2_BYTES]
        d2 = unpack(cache_row, D2_WIDTH).reshape(4, 36288)
        d0 = p1_row[:24192].reshape(4, 6048)
        d1 = p1_row[24192:96768].reshape(4, 18144)
        auxiliary = p1_row[96768:].copy()
        p0, p1, p2, paux = aggregate(self.context, d0, d1, d2, auxiliary)
        character = (max(i for i in range(4) if ORDER[i] <= index)
                     if index < ORDER[4] else
                     max(i for i in range(4) if ORDER[4 + i] <= index))
        if not self.restriction_checked:
            zeros0 = np.zeros_like(d0); zeros1 = np.zeros_like(d1)
            pure = aggregate(self.context, zeros0, zeros1, d2,
                             np.zeros(8, dtype=np.uint8))[2]
            need(np.array_equal(pure, self.task712.restriction(d2)),
                 "task712_full_restriction")
            self.restriction_checked = True
        ell_dense = np.concatenate((p0.reshape(-1), p1.reshape(-1), paux))
        return pack(ell_dense, ELL_WIDTH), pack(p2, TOP_WIDTH), {
            "node": index,
            "instruction_sha256": sha(canon(meta)),
            "p1_sha256": meta["p1_sha256"],
            "cache_row_sha256": meta["row_receipt"]["sha256"],
            "predecessor": meta["predecessor"],
            "ancestry_sha256": meta["ancestry_sha256"],
        }

    def close(self) -> None:
        if hasattr(self, "cache"):
            self.cache.close(); self.cache_file.close(); self.task554.close()


# ---------------------------------------------------------------------------
# Candidate replay and mutation-resistant bounded fixture.


RECORD_KEYS = {"offer", "kind", "source", "ell_sha256", "g_sha256",
               "reductions", "lead", "sigma", "lower_zero", "coefficient",
               "lower", "top", "rank", "dependent", "rolling_sha256"}
SOURCE_KEYS = {"instruction_sha256", "p1_sha256", "cache_row_sha256",
               "predecessor", "ancestry_sha256", "node"}


def record_shape(value: Any, offer: int, expected_offers: int) -> None:
    need(isinstance(value, dict) and set(value) == RECORD_KEYS
         and plain_int(value["offer"]) and value["offer"] == offer
         and value["kind"] in ("pivot", "connection")
         and isinstance(value["source"], dict) and set(value["source"]) == SOURCE_KEYS
         and plain_int(value["source"]["node"]) and value["source"]["node"] == offer
         and isinstance(value["reductions"], list), "record_shape")
    for item in value["reductions"]:
        need(isinstance(item, list) and len(item) == 2 and plain_int(item[0])
             and 0 <= item[0] < offer and plain_int(item[1]) and item[1] in (1, 2), "record_reduction")
    for key in ("instruction_sha256", "p1_sha256", "cache_row_sha256",
                "predecessor", "ancestry_sha256"):
        need(isinstance(value["source"][key], str)
             and len(value["source"][key]) == 64
             and all(char in "0123456789abcdef" for char in value["source"][key]),
             "record_source_digest")
    for key in ("ell_sha256", "g_sha256", "rolling_sha256"):
        need(isinstance(value[key], str) and len(value[key]) == 64
             and all(char in "0123456789abcdef" for char in value[key]), "record_digest")
    for key in ("coefficient", "lower", "top"):
        need(isinstance(value[key], dict) and set(value[key]) == {
             "offset", "length", "sha256"}, "record_store_receipt")
        if value[key]["sha256"] is not None:
            need(isinstance(value[key]["sha256"], str)
                 and len(value[key]["sha256"]) == 64
                 and all(char in "0123456789abcdef" for char in value[key]["sha256"]),
                 "record_store_digest")
    need(plain_int(value["coefficient"]["offset"])
         and plain_int(value["coefficient"]["length"])
         and plain_int(value["top"]["offset"])
         and plain_int(value["top"]["length"])
         and value["coefficient"]["offset"] == offer * COEFF_BYTES
         and value["coefficient"]["length"] == COEFF_BYTES
         and value["top"]["offset"] == offer * TOP_BYTES
         and value["top"]["length"] == TOP_BYTES, "record_offset")
    if value["kind"] == "connection":
        need(value["lower"] == {"offset": None, "length": ELL_BYTES,
                                 "sha256": None} and value["lower_zero"] is True,
             "record_connection_lower")
    else:
        need(plain_int(value["lower"]["offset"])
             and plain_int(value["lower"]["length"])
             and value["lower"]["length"] == ELL_BYTES, "record_pivot_lower")
    need(isinstance(value["lower_zero"], bool)
         and (value["lead"] is None or plain_int(value["lead"]))
         and (value["sigma"] is None or (plain_int(value["sigma"]) and value["sigma"] in (1, 2)))
         and plain_int(value["rank"]) and plain_int(value["dependent"]),
         "record_counts")


class MappedStore:
    def __init__(self, path: Path):
        self.stream = path.open("rb")
        self.map = mmap.mmap(self.stream.fileno(), 0, access=mmap.ACCESS_READ)

    def __getitem__(self, key: Any) -> Any:
        return self.map[key]

    def close(self) -> None:
        self.map.close(); self.stream.close()


def check_store(path: Path, rows: int, row_bytes: int,
                expected: dict[str, Any], width: int) -> MappedStore:
    need(isinstance(expected, dict) and set(expected) == {"path", "rows", "bytes", "sha256", "eof"}
         and expected["path"] == path.name and plain_int(expected["rows"])
         and expected["rows"] == rows and plain_int(expected["bytes"])
         and expected["bytes"] == rows * row_bytes
         and isinstance(expected["sha256"], str) and len(expected["sha256"]) == 64
         and expected["eof"] is True, "store_receipt_shape")
    need(path.is_file() and path.stat().st_size == rows * row_bytes
         and file_digest(path) == expected["sha256"], "store_receipt_digest")
    mapped = MappedStore(path)
    for index in range(rows):
        validate_packed(mapped[index * row_bytes:(index + 1) * row_bytes], width)
    return mapped


def source_ancestry() -> dict[str, Any]:
    return {"source_run": SOURCE_RUN, "source_attempt": SOURCE_ATTEMPT,
            "source_head": SOURCE_HEAD, "prepare_body_sha256": PREPARE_DIGEST,
            "parents": list(PARENTS),
            "producer_receipts": {"prepare": "9caf8cbf04742b1400c5c63d765508308af72ef773050af5562221a082fd159a", "blocks": ["e9271d20739aee299620ef6e8d53dd940ea10ed1ab688bd61b69c7fb0ff4afc8", "7f34bb964665078727c7ed2b5e5165c50b1763003d573789d7406a6b06445eca", "6d8ebdf7b9495608c89779ecfd7ca8f3c1a84790fc8e2b6b6fc5dd292c530e6a", "a558c466862bf050bf8c850aaf47be633ae1f0bce9785f18b410cb0eff9f6d9d"], "join": "a3479e7ebc010fbfde4d42c95eebd8cf81cc5eeab9ef37ab77ba2284fb8b27c8"},
            "checker_result_sha256": "405e1b26f971f67cb73129071a77346b126d0228c84219c2c3b0d879c63c99d5",
            "checker_workflow_receipt_sha256": "323ca2603b9ff7c42449fc0e2421c190eedcd7cd62471b695dee991fb1b728eb",
            "checker_success_artifact": {"id": 9918207444, "name": "task757-p1-semantic-checker-only-v3-success-33819301663-1", "archive_bytes": 24694, "digest": "sha256:f99fd6ce1172cc349b249ead8dbb8e75c8c8bd8a1b8a0493dfd4596aee5fbf0c"}}


def check_candidate(root: Path, pair: Any | None = None,
                    expected_offers: int = ROWS,
                    expected_p1_identity: dict[str, Any] | None = None,
                    expected_task712: dict[str, Any] | None = None) -> dict[str, Any]:
    root = root.resolve(); manifest_path = root / "manifest.json"
    raw = manifest_path.read_bytes(); manifest = json.loads(raw.decode("ascii"))
    expected_keys = {"schema", "status", "offers", "rank", "dependent",
                     "reduction_count", "source_ancestry", "p1_identity", "task712",
                     "coefficient", "lower", "top", "instruction",
                     "final_rolling_head", "candidate_roster", *FALSE_FLAGS}
    owner = getattr(pair, "__self__", None)
    if expected_p1_identity is None and owner is not None:
        expected_p1_identity = getattr(owner, "p1_identity", None)
    if expected_task712 is None and owner is not None:
        expected_task712 = getattr(owner, "task712_identity", None)
    need(pair is not None and callable(pair), "independent_pair_required")
    need(expected_p1_identity is not None and expected_task712 is not None,
         "candidate_identity_context")
    need(raw == canon(manifest) and set(manifest) == expected_keys
         and manifest["schema"] == SCHEMA and manifest["status"] == STATUS
         and plain_int(manifest["offers"]) and manifest["offers"] == expected_offers
         and plain_int(manifest["rank"]) and plain_int(manifest["dependent"])
         and plain_int(manifest["reduction_count"])
         and manifest["rank"] + manifest["dependent"] == expected_offers
         and manifest["source_ancestry"] == source_ancestry()
         and manifest["p1_identity"] == expected_p1_identity
         and manifest["task712"] == expected_task712
         and all(manifest[key] is False for key in FALSE_FLAGS), "candidate_manifest")
    names = ["coefficient.bin", "lower.bin", "top.bin", "instructions.jsonl", "manifest.json"]
    need(manifest["candidate_roster"] == names, "candidate_roster")
    actual_files = sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())
    need(actual_files == sorted(names), "candidate_exact_roster")
    for name in names:
        need((root / name).is_file(), "candidate_missing:" + name)
    coeff_path, lower_path, top_path = (root / "coefficient.bin", root / "lower.bin", root / "top.bin")
    coeff = check_store(coeff_path, expected_offers, COEFF_BYTES,
                        manifest["coefficient"], ROWS)
    lower = check_store(lower_path, manifest["rank"], ELL_BYTES,
                        manifest["lower"], ELL_WIDTH)
    top = check_store(top_path, expected_offers, TOP_BYTES, manifest["top"], TOP_WIDTH)
    instruction_path = root / "instructions.jsonl"
    need(instruction_path.stat().st_size == manifest["instruction"]["bytes"]
         and file_digest(instruction_path) == manifest["instruction"]["sha256"]
         and manifest["instruction"] == {
             "path": "instructions.jsonl", "rows": expected_offers,
             "bytes": manifest["instruction"]["bytes"],
             "sha256": manifest["instruction"]["sha256"], "final_lf": True,
             "eof": True, "final_head": manifest["final_rolling_head"]},
         "candidate_instruction_receipt")
    pivots: dict[int, tuple[int, int, int, int]] = {}
    leads: dict[int, int] = {}
    rank = dependent = 0; previous = ZERO_HEAD; reductions_total = 0
    calls = 0; node_hits: dict[int, int] = {}
    try:
        with instruction_path.open("rb") as stream:
            for offer in range(expected_offers):
                line = stream.readline()
                need(line and line.endswith(b"\n") and b"\r" not in line,
                     "candidate_instruction_lf")
                record = json.loads(line.decode("ascii"))
                record_shape(record, offer, expected_offers)
                need(line == canon(record), "candidate_instruction_canonical")
                rolling_unsigned = {key: value for key, value in record.items()
                                    if key != "rolling_sha256"}
                need(record["rolling_sha256"] == sha(bytes.fromhex(previous)
                     + canon(rolling_unsigned)), "candidate_rolling")
                previous = record["rolling_sha256"]
                expected = pair(offer); calls += 1
                node_hits[offer] = node_hits.get(offer, 0) + 1
                need(isinstance(expected, tuple) and len(expected) == 3
                     and isinstance(expected[0], (bytes, bytearray))
                     and isinstance(expected[1], (bytes, bytearray)), "candidate_pair_shape")
                need(record["ell_sha256"] == sha(expected[0])
                     and record["g_sha256"] == sha(expected[1])
                     and record["source"] == expected[2], "candidate_source")
                ell = bytearray(expected[0]); top_work = bytearray(expected[1])
                coefficient = bytearray(unit(offer))
                for pivot_id, scalar in record["reductions"]:
                    current = first(ell, ELL_WIDTH)
                    need(current is not None and current[0] in leads
                         and leads[current[0]] == pivot_id
                         and pivot_id in pivots and pivot_id < rank
                         and current[1] == scalar, "candidate_lower_first_parent")
                    lead, co_offset, lo_offset, top_offset = pivots[pivot_id]
                    need(lead == current[0], "candidate_pivot_lead")
                    pivot_coeff = coeff[co_offset:co_offset + COEFF_BYTES]
                    pivot_lower = lower[lo_offset:lo_offset + ELL_BYTES]
                    pivot_top = top[top_offset:top_offset + TOP_BYTES]
                    axpy(coefficient, pivot_coeff, scalar, ROWS)
                    axpy(ell, pivot_lower, scalar, ELL_WIDTH)
                    axpy(top_work, pivot_top, scalar, TOP_WIDTH)
                    reductions_total += 1
                remainder = first(ell, ELL_WIDTH)
                need(remainder is None or remainder[0] not in leads,
                     "candidate_unreduced_or_duplicate_lead")
                kind = "pivot" if remainder is not None else "connection"
                sigma = (2 if remainder and remainder[1] == 2 else
                         1 if remainder else None)
                need(record["kind"] == kind and record["lead"] == (remainder[0] if remainder else None)
                     and record["sigma"] == sigma
                     and record["lower_zero"] is (remainder is None),
                     "candidate_normalization")
                if sigma == 2:
                    coefficient[:] = bytes(SCALE2[np.frombuffer(coefficient, dtype=np.uint8)])
                    ell[:] = bytes(SCALE2[np.frombuffer(ell, dtype=np.uint8)])
                    top_work[:] = bytes(SCALE2[np.frombuffer(top_work, dtype=np.uint8)])
                cbytes = bytes(coeff[offer * COEFF_BYTES:(offer + 1) * COEFF_BYTES])
                tbytes = bytes(top[offer * TOP_BYTES:(offer + 1) * TOP_BYTES])
                need(bytes(coefficient) == cbytes and bytes(top_work) == tbytes
                     and sha(cbytes) == record["coefficient"]["sha256"]
                     and sha(tbytes) == record["top"]["sha256"], "candidate_store_replay")
                if remainder is None:
                    dependent += 1
                else:
                    loff = rank * ELL_BYTES
                    lbytes = bytes(lower[loff:loff + ELL_BYTES])
                    need(bytes(ell) == lbytes and sha(lbytes) == record["lower"]["sha256"]
                         and record["lower"]["offset"] == loff
                         and first(lbytes, ELL_WIDTH) is not None
                         and first(lbytes, ELL_WIDTH)[0] == remainder[0]
                         and first(lbytes, ELL_WIDTH)[1] == 1
                         and remainder[0] not in leads, "candidate_lower_replay")
                    pivots[rank] = (remainder[0], offer * COEFF_BYTES,
                                    loff, offer * TOP_BYTES)
                    leads[remainder[0]] = rank; rank += 1
                need(record["rank"] == rank and record["dependent"] == dependent,
                     "candidate_counts")
            need(stream.read(1) == b"", "candidate_instruction_eof")
        need(rank == manifest["rank"] and dependent == manifest["dependent"]
             and reductions_total == manifest["reduction_count"]
             and previous == manifest["final_rolling_head"], "candidate_terminal")
        return {"status": "PASS", "offers": expected_offers, "rank": rank,
                "dependent": dependent, "reductions": reductions_total,
                "rolling": previous, "checker_pair_calls": calls,
                "checker_node0": node_hits.get(0, 0),
                "checker_node3523": node_hits.get(3523, 0), "verified": False}
    finally:
        for mapped in (coeff, lower, top):
            mapped.close()


def fixture_pairs(count: int) -> list[tuple[bytes, bytes, dict[str, Any]]]:
    rows = []
    for index in range(count):
        ell = np.zeros(ELL_WIDTH, dtype=np.uint8)
        if index != 3:
            ell[:index + 1] = 1
            ell[index] = 2 if index == 1 else 1
        top = np.zeros(TOP_WIDTH, dtype=np.uint8)
        if index != 4:
            top[(13 * index) % TOP_WIDTH] = index % 3 or 1
        ell_bytes = pack(ell, ELL_WIDTH); top_bytes = pack(top, TOP_WIDTH)
        source = sha(f"fixture-source-{index}".encode("ascii"))
        rows.append((ell_bytes, top_bytes, {
            "node": index, "instruction_sha256": source,
            "p1_sha256": source, "cache_row_sha256": sha(top_bytes),
            "predecessor": ZERO_HEAD, "ancestry_sha256": source}))
    return rows


def duplicate_fixture_pairs() -> list[tuple[bytes, bytes, dict[str, Any]]]:
    """Two identical lower offers; the second is truly rank-dependent."""
    rows = fixture_pairs(2)
    ell, top, _ = rows[0]
    source = sha(b"fixture-duplicate-second")
    rows[1] = (ell, top, {
        "node": 1, "instruction_sha256": source,
        "p1_sha256": source, "cache_row_sha256": sha(top),
        "predecessor": ZERO_HEAD, "ancestry_sha256": source})
    return rows


def make_fixture(root: Path, source: PhysicalSourceAdapter) -> None:
    root.mkdir(); coeff_rows = []; lower_rows = []; top_rows = []
    pivots: dict[int, tuple[int, bytes, bytes]] = {}; rank = dependent = 0
    previous = ZERO_HEAD; instruction_lines = []; reduction_count = 0
    count = len(source._fixture_rows)
    for offer in range(count):
        ell, top_value, metadata = source.pair(offer)
        coefficient = unit(offer); work = bytearray(ell); top_work = bytearray(top_value); reductions = []
        while True:
            lead = first(work, ELL_WIDTH)
            if lead is None or lead[0] not in pivots:
                break
            pivot_id, pcoeff, plower, ptop = pivots[lead[0]]
            scalar = lead[1]
            axpy(coefficient, pcoeff, scalar, ROWS); axpy(work, plower, scalar, ELL_WIDTH); axpy(top_work, ptop, scalar, TOP_WIDTH)
            reductions.append([pivot_id, scalar]); reduction_count += 1
        remainder = first(work, ELL_WIDTH); sigma = 2 if remainder and remainder[1] == 2 else (1 if remainder else None)
        if sigma == 2:
            coefficient[:] = bytes(SCALE2[np.frombuffer(coefficient, dtype=np.uint8)])
            work[:] = bytes(SCALE2[np.frombuffer(work, dtype=np.uint8)])
            top_work[:] = bytes(SCALE2[np.frombuffer(top_work, dtype=np.uint8)])
        cbytes, lbytes, tbytes = bytes(coefficient), bytes(work), bytes(top_work)
        coeff_rows.append(cbytes); top_rows.append(tbytes)
        if remainder:
            lower_rows.append(lbytes); pivots[remainder[0]] = (rank, cbytes, lbytes, tbytes); rank += 1
            kind = "pivot"; lower_receipt = {"offset": (rank - 1) * ELL_BYTES, "length": ELL_BYTES, "sha256": sha(lbytes)}
        else:
            dependent += 1; kind = "connection"; lower_receipt = {"offset": None, "length": ELL_BYTES, "sha256": None}
        record = {"offer": offer, "kind": kind, "source": metadata,
                  "ell_sha256": sha(ell), "g_sha256": sha(top_value),
                  "reductions": reductions, "lead": remainder[0] if remainder else None,
                  "sigma": sigma, "lower_zero": remainder is None,
                  "coefficient": {"offset": offer * COEFF_BYTES, "length": COEFF_BYTES, "sha256": sha(cbytes)},
                  "lower": lower_receipt,
                  "top": {"offset": offer * TOP_BYTES, "length": TOP_BYTES, "sha256": sha(tbytes)},
                  "rank": rank, "dependent": dependent}
        record["rolling_sha256"] = sha(bytes.fromhex(previous) + canon(record)); previous = record["rolling_sha256"]
        instruction_lines.append(canon(record))
    (root / "coefficient.bin").write_bytes(b"".join(coeff_rows)); (root / "lower.bin").write_bytes(b"".join(lower_rows)); (root / "top.bin").write_bytes(b"".join(top_rows)); (root / "instructions.jsonl").write_bytes(b"".join(instruction_lines))
    manifest = {"schema": SCHEMA, "status": STATUS, "offers": count,
                "rank": rank, "dependent": dependent, "reduction_count": reduction_count,
                "source_ancestry": source_ancestry(), "p1_identity": source.p1_identity, "task712": source.task712_identity,
                "coefficient": {"path": "coefficient.bin", "rows": count, "bytes": count * COEFF_BYTES, "sha256": sha((root / "coefficient.bin").read_bytes()), "eof": True},
                "lower": {"path": "lower.bin", "rows": rank, "bytes": rank * ELL_BYTES, "sha256": sha((root / "lower.bin").read_bytes()), "eof": True},
                "top": {"path": "top.bin", "rows": count, "bytes": count * TOP_BYTES, "sha256": sha((root / "top.bin").read_bytes()), "eof": True},
                "instruction": {"path": "instructions.jsonl", "rows": count, "bytes": (root / "instructions.jsonl").stat().st_size, "sha256": sha((root / "instructions.jsonl").read_bytes()), "final_lf": True, "eof": True, "final_head": previous},
                "final_rolling_head": previous, "candidate_roster": ["coefficient.bin", "lower.bin", "top.bin", "instructions.jsonl", "manifest.json"], **FALSE_FLAGS}
    (root / "manifest.json").write_bytes(canon(manifest))


def expect_reject(action: Any, label: str) -> str:
    try:
        action()
    except Exception as error:
        return str(error)
    raise AssertionError("mutation_accepted:" + label)


def mutate_instruction(root: Path, index: int, mutate: Any) -> None:
    path = root / "instructions.jsonl"; lines = path.read_bytes().splitlines(keepends=True); value = json.loads(lines[index].decode("ascii")); mutate(value); lines[index] = canon(value); path.write_bytes(b"".join(lines))


def reseal_candidate(root: Path) -> None:
    """Recompute only fixture receipts after an intentional mutation."""
    path = root / "instructions.jsonl"; lines = path.read_bytes().splitlines(keepends=True)
    previous = ZERO_HEAD; resealed = []
    for line in lines:
        value = json.loads(line.decode("ascii")); value["rolling_sha256"] = sha(bytes.fromhex(previous) + canon({key: value[key] for key in value if key != "rolling_sha256"})); previous = value["rolling_sha256"]; resealed.append(canon(value))
    path.write_bytes(b"".join(resealed))
    manifest_path = root / "manifest.json"; manifest = json.loads(manifest_path.read_text("ascii")); raw = path.read_bytes(); manifest["instruction"].update({"bytes": len(raw), "sha256": sha(raw), "final_head": previous}); manifest["final_rolling_head"] = previous; manifest_path.write_bytes(canon(manifest))


def make_duplicate_lead_candidate(base: Path, target: Path) -> None:
    shutil.copytree(base, target)
    lines = (target / "instructions.jsonl").read_bytes().splitlines(keepends=True)
    first_record = json.loads(lines[0].decode("ascii")); second = json.loads(lines[1].decode("ascii"))
    lower_row = (target / "lower.bin").read_bytes()[:ELL_BYTES]
    with (target / "lower.bin").open("ab") as stream:
        stream.write(lower_row)
    coefficient = bytearray((target / "coefficient.bin").read_bytes()); coefficient[COEFF_BYTES:2 * COEFF_BYTES] = unit(1); (target / "coefficient.bin").write_bytes(coefficient)
    expected_top = np.zeros(TOP_WIDTH, dtype=np.uint8); expected_top[13] = 1; expected_top_bytes = pack(expected_top, TOP_WIDTH)
    top = bytearray((target / "top.bin").read_bytes()); top[TOP_BYTES:2 * TOP_BYTES] = expected_top_bytes; (target / "top.bin").write_bytes(top)
    second.update({"kind": "pivot", "reductions": [], "lead": 0, "sigma": 1, "lower_zero": False,
                   "coefficient": {"offset": COEFF_BYTES, "length": COEFF_BYTES,
                                   "sha256": sha(bytes(coefficient[COEFF_BYTES:2 * COEFF_BYTES]))},
                   "lower": {"offset": ELL_BYTES, "length": ELL_BYTES,
                              "sha256": sha(lower_row)},
                   "top": {"offset": TOP_BYTES, "length": TOP_BYTES,
                           "sha256": sha(expected_top_bytes)}, "rank": 2,
                   "dependent": 0})
    lines[1] = canon(second); (target / "instructions.jsonl").write_bytes(b"".join(lines)); reseal_candidate(target)
    manifest_path = target / "manifest.json"; manifest = json.loads(manifest_path.read_text("ascii")); lower_raw = (target / "lower.bin").read_bytes(); coeff_raw = (target / "coefficient.bin").read_bytes(); top_raw = (target / "top.bin").read_bytes(); manifest.update({"rank": 2, "dependent": 0}); manifest["lower"].update({"rows": 2, "bytes": len(lower_raw), "sha256": sha(lower_raw)}); manifest["coefficient"]["sha256"] = sha(coeff_raw); manifest["top"]["sha256"] = sha(top_raw); manifest_path.write_bytes(canon(manifest))


def benchmark() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="d972-v5-checker-bench-") as td:
        source = PhysicalSourceAdapter.bounded_fixture(fixture_pairs(128)); candidate = Path(td) / "candidate"; make_fixture(candidate, source); source.pair_calls = 0; source.node_hits = {}
        started = time.perf_counter(); result = check_candidate(candidate, source.pair, 128); elapsed = max(1e-9, time.perf_counter() - started)
    rate = result["reductions"] / elapsed
    return {"offers": 128, "reductions": result["reductions"], "seconds": elapsed,
            "reductions_per_second": rate,
            "full_rank_upper_envelope_reductions": 32469711,
            "full_rank_upper_envelope_seconds": 32469711 / rate}


def selftest() -> None:
    need(unpack(pack(np.asarray([0, 1, 2, 0], dtype=np.uint8), 4), 4).tolist() == [0, 1, 2, 0], "codec")
    need(first(bytes([0]), 4) is None, "first")
    need(physical_index(0, 0, 0, 0, 0) == 0
         and physical_index(3, 1, 1, 5, 503) == 48383,
         "physical_index_formula")
    need(Task712Tables._spec("B_adj_a0.jsonl") == ("B", 0, None, TOP_WIDTH, 36288, "adjoint"), "task712_adj_direction")
    need(Task712Tables._spec("B_fwd_a0.jsonl") == ("B", 0, None, 36288, TOP_WIDTH, "forward"), "task712_fwd_direction")
    context = IndependentContext(json.loads((ROOT / "scratchpad/a0_paper_words_v1.json").read_text("ascii")))
    d0 = np.ones((4, 6048), dtype=np.uint8); d1 = np.ones((4, 18144), dtype=np.uint8); d2 = np.ones((4, 36288), dtype=np.uint8)
    aggregated = aggregate(context, d0, d1, d2, np.zeros(8, dtype=np.uint8))
    need(np.any(aggregated[1]) and np.any(aggregated[2]), "prefix_degree_mixing")
    negative_kernel = e_polynomial((0, 0, 2))
    need(int(negative_kernel[0]) == 1 and int(negative_kernel[3]) == 2
         and int(negative_kernel[9]) == 1, "negative_exponent_polynomial")
    with tempfile.TemporaryDirectory(prefix="d972-v5-checker-") as td:
        production_records = {
            character: fixture_expected_occurrence_records(context, character)
            for character in range(4)}

        def production_adapter() -> "PhysicalSourceAdapter":
            return PhysicalSourceAdapter(
                Path(td) / "unused-p1", Path(td) / "unused-prepare", [],
                Path(td) / "unused-words", Path(td) / "unused-task712",
                fixture_context=context,
                fixture_task712=BoundedProductionTask712(production_records))

        production = production_adapter()
        need(production.complete_map_receipt["source_columns"] == 4 * 36288
             and production.task712.receipt["complete_map"] ==
             production.complete_map_receipt,
             "production_call_chain_complete_map")
        production.close()
        saved_physical_index = physical_index
        globals()["physical_index"] = lambda character, block, component, monomial, psl: saved_physical_index(
            character, block, component, monomial, psl) + 1
        try:
            drift_error = expect_reject(production_adapter,
                                        "physical-index-drift")
        finally:
            globals()["physical_index"] = saved_physical_index
        need(drift_error == "task712_complete_map_a0:entry",
             "physical_index_regression")
        base = Path(td) / "positive"; source = PhysicalSourceAdapter.bounded_fixture(fixture_pairs(8)); make_fixture(base, source); source.pair_calls = 0; source.node_hits = {}
        result = check_candidate(base, source.pair, 8)
        need(result["status"] == "PASS" and source.pair_calls == 8
             and source.node_hits.get(0) == 1 and source.node_hits.get(7) == 1,
             "positive_public_adapter_fixture")
        tiny_expected = [(0, 1, 1), (1, 2, 2), (2, 3, 1)]
        tiny_path = Path(td) / "B_fwd_a0.jsonl"
        tiny_body = b"".join((json.dumps(list(row), separators=(",", ":")) + "\n").encode("ascii")
                             for row in tiny_expected)
        tiny_eof = canon({"body_bytes": len(tiny_body),
                          "body_sha256": sha(tiny_body),
                          "count": len(tiny_expected), "eof": True})
        tiny_path.write_bytes(tiny_body + tiny_eof)
        tiny_receipt = {"file": tiny_path.name,
                        "schema": "d972.r07.grade2.forward-adjoint-maps.v3.sparse-jsonl",
                        "source_width": 3, "destination_width": 4,
                        "entry_count": len(tiny_expected),
                        "body_bytes": len(tiny_body),
                        "body_sha256": sha(tiny_body),
                        "bytes": tiny_path.stat().st_size,
                        "sha256": sha(tiny_path.read_bytes()), "eof": True,
                        "encoding": "jsonl-triples-utf8-lf", "map_kind": "B",
                        "map_direction": "forward", "character": 0}
        parsed_tiny = Task712Tables._read_table(tiny_path, tiny_receipt, 3, 4,
                                                "B", "forward", 0, None)
        compare_complete_restriction(parsed_tiny, tiny_expected, 3, 4,
                                     "task712_tiny_complete_map")
        mutated_tiny = [(0, 1, 1), (1, 2, 1), (2, 3, 1)]
        mutated_body = b"".join((json.dumps(list(row), separators=(",", ":")) + "\n").encode("ascii")
                                for row in mutated_tiny)
        tiny_path.write_bytes(mutated_body + canon({
            "body_bytes": len(mutated_body), "body_sha256": sha(mutated_body),
            "count": len(mutated_tiny), "eof": True}))
        mutated_receipt = {**tiny_receipt, "body_bytes": len(mutated_body),
                           "body_sha256": sha(mutated_body),
                           "bytes": tiny_path.stat().st_size,
                           "sha256": sha(tiny_path.read_bytes())}
        parsed_mutated = Task712Tables._read_table(
            tiny_path, mutated_receipt, 3, 4, "B", "forward", 0, None)
        task712_mutation_error = expect_reject(lambda: compare_complete_restriction(
            parsed_mutated, tiny_expected, 3, 4,
            "task712_rows_preserving_resealed_mutation"),
            "task712-rows-preserving-resealed")
        need(task712_mutation_error == "task712_rows_preserving_resealed_mutation:entry",
             "task712_mutation_label")
        mutations = {
            "record-key": lambda value: value.__setitem__("extra", True),
            "offset": lambda value: value["coefficient"].__setitem__("offset", 1),
            "lower-zero": lambda value: value.__setitem__("lower_zero", not value["lower_zero"]),
            "rolling": lambda value: value.__setitem__("rolling_sha256", "0" * 64),
            "boolean-offer": lambda value: value.__setitem__("offer", True),
        }
        for label, action in mutations.items():
            target = Path(td) / label; shutil.copytree(base, target)
            mutate_instruction(target, 0, action)
            expect_reject(lambda target=target: check_candidate(target, PhysicalSourceAdapter.bounded_fixture(fixture_pairs(8)).pair, 8), label)
        cancel = Path(td) / "canceling-reduction"; shutil.copytree(base, cancel); mutate_instruction(cancel, 1, lambda value: value["reductions"].append([0, 2])); reseal_candidate(cancel); expect_reject(lambda: check_candidate(cancel, PhysicalSourceAdapter.bounded_fixture(fixture_pairs(8)).pair, 8), "canceling-reduction")
        forged = Path(td) / "forged-identity"; shutil.copytree(base, forged); forged_manifest = json.loads((forged / "manifest.json").read_text("ascii")); forged_manifest["p1_identity"] = {"forged": True}; (forged / "manifest.json").write_bytes(canon(forged_manifest)); expect_reject(lambda: check_candidate(forged, PhysicalSourceAdapter.bounded_fixture(fixture_pairs(8)).pair, 8), "forged-p1-identity")
        forged712 = Path(td) / "forged-task712-identity"; shutil.copytree(base, forged712); forged_manifest = json.loads((forged712 / "manifest.json").read_text("ascii")); forged_manifest["task712"] = {"forged": True}; (forged712 / "manifest.json").write_bytes(canon(forged_manifest)); forged712_error = expect_reject(lambda: check_candidate(forged712, PhysicalSourceAdapter.bounded_fixture(fixture_pairs(8)).pair, 8), "forged-task712-identity")
        need(forged712_error == "candidate_manifest", "forged_task712_label")
        extra = Path(td) / "extra-roster"; shutil.copytree(base, extra); (extra / "sixth.bin").write_bytes(b"extra"); expect_reject(lambda: check_candidate(extra, PhysicalSourceAdapter.bounded_fixture(fixture_pairs(8)).pair, 8), "extra-candidate-file")
        duplicate_base = Path(td) / "duplicate-base"; duplicate_source = PhysicalSourceAdapter.bounded_fixture(duplicate_fixture_pairs()); make_fixture(duplicate_base, duplicate_source); duplicate = Path(td) / "duplicate-lead"; make_duplicate_lead_candidate(duplicate_base, duplicate); duplicate_error = expect_reject(lambda: check_candidate(duplicate, PhysicalSourceAdapter.bounded_fixture(duplicate_fixture_pairs()).pair, 2), "duplicate-lead-true-rank-one-unreduced")
        need(duplicate_error == "candidate_unreduced_or_duplicate_lead", "duplicate_lead_label")
        bad_descriptor = {"file": "B_fwd_a0.jsonl", "schema": "d972.r07.grade2.forward-adjoint-maps.v3.sparse-jsonl", "source_width": 36288, "destination_width": TOP_WIDTH, "entry_count": 0, "body_bytes": 0, "body_sha256": "" * 0, "bytes": 0, "sha256": "0" * 64, "eof": True, "encoding": "jsonl-triples-utf8-lf", "map_kind": "T", "map_direction": "forward", "character": 0}
        expect_reject(lambda: Task712Tables._read_table(Path("B_fwd_a0.jsonl"), bad_descriptor, 36288, TOP_WIDTH, "B", 0, None), "task712-full-structural-descriptor")
        padding = lambda: validate_packed(bytes([81]), 4)
        expect_reject(padding, "padding")
        target = Path(td) / "eof"; shutil.copytree(base, target); (target / "instructions.jsonl").open("ab").write(b"\n")
        expect_reject(lambda: check_candidate(target, PhysicalSourceAdapter.bounded_fixture(fixture_pairs(8)).pair, 8), "eof")
        target = Path(td) / "store-receipt"; shutil.copytree(base, target); m = json.loads((target / "manifest.json").read_text("ascii")); m["coefficient"]["sha256"] = "0" * 64; (target / "manifest.json").write_bytes(canon(m)); expect_reject(lambda: check_candidate(target, PhysicalSourceAdapter.bounded_fixture(fixture_pairs(8)).pair, 8), "store-receipt")
        target = Path(td) / "synchronized-row"; shutil.copytree(base, target); data = bytearray((target / "coefficient.bin").read_bytes()); data[0] ^= 1; (target / "coefficient.bin").write_bytes(data); m = json.loads((target / "manifest.json").read_text("ascii")); m["coefficient"]["sha256"] = sha(bytes(data)); (target / "manifest.json").write_bytes(canon(m)); expect_reject(lambda: check_candidate(target, PhysicalSourceAdapter.bounded_fixture(fixture_pairs(8)).pair, 8), "synchronized-row")
    print(json.dumps({"selftest": "PASS", "positive_fixture": "production_shaped_public_adapter_and_full_task712_restriction", "production_call_chain": "PASS", "physical_index_regression": "PASS", "pair_calls": source.pair_calls, "pair_node0": source.node_hits.get(0, 0), "pair_node7": source.node_hits.get(7, 0), "mutation_classes": 15, "independent_source_replay": "READY", "complete_map_columns": 4 * 36288, "mutation_rejection_labels": {"task712_rows_preserving_resealed": task712_mutation_error, "forged_task712_identity": forged712_error, "duplicate_lead_true_rank_one": duplicate_error}, "verified": False, "benchmark": benchmark()}, separators=(",", ":")))


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true")
    modes.add_argument("--benchmark", action="store_true")
    modes.add_argument("--check", action="store_true")
    for name in ("candidate", "launch-manifest", "p1-root", "prepare-root", "p1-v10", "grade1", "prebuild", "semantic", "structural", "floor", "words", "task712-root"):
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-roots", nargs=4, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.selftest:
            selftest(); return 0
        if args.benchmark:
            print(json.dumps(benchmark(), separators=(",", ":"))); return 0
        required = ("candidate", "launch_manifest", "p1_root", "prepare_root", "block_roots", "p1_v10", "grade1", "prebuild", "semantic", "structural", "floor", "words", "task712_root")
        need(all(getattr(args, key) is not None for key in required), "check_arguments")
        launch = validate_launch(args.launch_manifest.resolve()); verify_launch_files(launch)
        source_expected = {"p1-v10": (args.p1_v10, P1_V10_SHA), "grade1": (args.grade1, SOURCE_HASHES["grade1_v4"]), "prebuild": (args.prebuild, SOURCE_HASHES["prebuild_v1"]), "semantic": (args.semantic, SOURCE_HASHES["semantic_v5"]), "structural": (args.structural, SOURCE_HASHES["structural_v1"]), "floor": (args.floor, SOURCE_HASHES["floor_v1"]), "words": (args.words, SOURCE_HASHES["words"]), "task712-v3": (ROOT / "search/d972_r07_grade2_forward_adjoint_maps_v3.py", SOURCE_HASHES["task712_v3"])}
        for label, (path, expected) in source_expected.items():
            need(file_digest(path.resolve()) == expected, "source_pin:" + label)
        source = PhysicalSourceAdapter(args.p1_root, args.prepare_root, args.block_roots, args.words, args.task712_root, launch)
        try:
            result = check_candidate(args.candidate, source.pair,
                                     expected_p1_identity=source.p1_identity,
                                     expected_task712=source.task712_identity)
            result["source_pair_calls"] = source.pair_calls; result["source_node0"] = source.node_hits.get(0, 0); result["source_node3523"] = source.node_hits.get(3523, 0); print(json.dumps(result, separators=(",", ":")))
        finally:
            source.close()
        return 0
    except RuntimeError as exc:
        print(json.dumps({"status": "UNKNOWN_RESOURCE", "error": str(exc), "verified": False}, separators=(",", ":")), file=sys.stderr); return 2
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc), "verified": False}, separators=(",", ":")), file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
