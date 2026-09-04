#!/usr/bin/env python3
"""R07 actual four-character root-scalar batch.

The executable is deliberately a small bridge.  The large P1 object is read
once, row by row, and only the twenty sparse packed projections are retained.
The arithmetic for seeds and relations is imported from the audited producer
v15 module; no checker code is imported here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

import numpy as np

try:
    import d972_r07_targeted_grade2_owner_generated_join_v15 as ARITH
except ModuleNotFoundError:  # pragma: no cover - permits an absolute launch
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import d972_r07_targeted_grade2_owner_generated_join_v15 as ARITH


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972.r07.actual-grade2.root-scalar-batch.v1"
ARITH_PATH = PROJECT_ROOT / "search" / "d972_r07_targeted_grade2_owner_generated_join_v15.py"
ARITH_SHA256 = "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632"
CHECKER_ARITH_PATH = PROJECT_ROOT / "search" / "check_d972_r07_targeted_grade2_owner_generated_join_v15.py"
CHECKER_ARITH_SHA256 = "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662"
P1_RUN = 33851744070
P1_ATTEMPT = 1
P1_HEAD = "6673eb2ea15ca6022acc2ddc5a8a204a0380172f"
P1_ARTIFACT = 9931437113
P1_ARTIFACT_NAME = "task809-canonical-p1-degree2-lift-v9-33851744070-1"
P1_ARCHIVE_BYTES = 641518300
P1_ARCHIVE_SHA256 = "sha256:6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c"
P1_MANIFEST_BYTES = 17472
P1_MANIFEST_SHA256 = "86e8b14cb0a60c86468ffb54a7bf14980366406a1e5bea17018fc6961f331feb"
P1_CACHE_BYTES = 292444992
P1_CACHE_SHA256 = "b88edb9b12753cdb7a3629403f8ac14206595e03525fa2a201b6b00b985c1abf"
P1_INSTRUCTION_BYTES = 349055442
P1_INSTRUCTION_SHA256 = "8b549337786b1f3b970a7250f1c326724ef957369c213c55af5a3d52a96f38ae"
P1_ROWS = 8059
P1_ROW_TRITS = 145152
P1_ROW_BYTES = 36288
SOURCE_WIDTH = 36288
SLICE_BYTES = SOURCE_WIDTH // 4
PHYSICAL_WIDTH = 48384
PHYSICAL_PACKED_BYTES = 12096
ACTORS = (1, -1, 2, -2)
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
OLD_RANKS = (505, 503, 503, 503)
NEW_RANKS = (1509, 1512, 1512, 1512)
ORIGIN_RANGES = ((0, 2064), (2064, 4120), (4120, 6176), (6176, 8232))
SCALAR_ORIGINS = 32280
TASK554_ORIGINS = 8232
POW3 = (1, 3, 9, 27)

SEPARATOR_RUN = 33891714539
SEPARATOR_ATTEMPT = 1
SEPARATOR_HEAD = "7b7b9de20faaa3b8f26e331bb738b374f6f5708c"
SEPARATOR_ARTIFACT = 9944214057
SEPARATOR_ARTIFACT_NAME = "d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1"
SEPARATOR_ARCHIVE_BYTES = 107195261
SEPARATOR_ARCHIVE_SHA256 = "sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017"
SEPARATOR_MANIFEST_SHA256 = "d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b"
SEPARATOR_PHYSICAL_BYTES = 16377984
SEPARATOR_PHYSICAL_SHA256 = "1246ae0c23c7dcbfc2a1c2f73075f38968a4ab7b2e5c8fc006f0f8aafae2d57e"
SEPARATOR_LAMBDA_BYTES = 12096
SEPARATOR_LAMBDA_SHA256 = "7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed"
SEPARATOR_TERMINAL_SHA256 = "098d5961cddc187d01c08e22f9f40ce55a7a02e8a1b1d088eca8c804957098cf"
SEPARATOR_RESULT_SHA256 = "d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968"
SEPARATOR_CHECKER_SHA256 = "2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433"
SEPARATOR_GENERATION = 8059
SEPARATOR_RANK = 1354
SEPARATOR_STATE_HEAD = "69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88"

TASK554_RUN = 33677346616
TASK554_ATTEMPT = 1
TASK554_HEAD = "22c6dddb43d107c05e65f53ad898823ae8ebe276"
TASK554_BODY_DIGESTS = (
    "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865",
    "9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74",
    "d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6",
    "a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac",
    "642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01",
)
TASK554_ARTIFACTS = (
    (9865061266, "task554-grade1-v3-prepare-33677346616-1", 204360988,
     "sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4"),
    (9865238399, "task554-grade1-v3-state-block-0-33677346616-1", 81729645,
     "sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838"),
    (9865242284, "task554-grade1-v3-state-block-1-33677346616-1", 82259824,
     "sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb"),
    (9865193269, "task554-grade1-v3-state-block-2-33677346616-1", 82200189,
     "sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d"),
    (9865239848, "task554-grade1-v3-state-block-3-33677346616-1", 82266526,
     "sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92"),
)

TASK712_PARENT = {
    "run_id": 33814194630, "run_attempt": 1, "artifact_id": 9915928157,
    "artifact_digest": "sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858",
}

# The actual preflight fixed these packed outputs.  Keeping the pins here
# makes a wrong map/character join a rejection, rather than a new candidate.
EXPECTED_ROOT = {
    0: (2742, 3, 2, "af62027aa99fbd1a4b7b53c6b380b4e7fa7403915ea91f9d51d7cb2198c7e053"),
    1: (0, None, None, "8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838"),
    2: (0, None, None, "8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838"),
    3: (0, None, None, "8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838"),
}
EXPECTED_CHILD = {
    0: (
        "aa54bbed30791f3f771c5fb8d74e38329564101cbcd805db20e1e232595e7033",
        "1b98282910ed00d253cad00cbc389b9c85c6b84be9b8da0418ece4f8b0218cd8",
        "f98650b321a16e846539698d98710a544fd1953656afcaecbee995523f0def2b",
        "2245611c3efcef71758e281950ca4b23ba96d0991880cdb92ecafa0fac7aa8b4",
    ),
    1: ("8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838",) * 4,
    2: ("8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838",) * 4,
    3: ("8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838",) * 4,
}


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def digest(value: Any, reason: str) -> None:
    require(isinstance(value, str) and len(value) == 64 and
            all(c in "0123456789abcdef" for c in value), reason)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def sealed_object(value: Any) -> bool:
    """Check an embedded canonical seal, distinct from an outer file hash."""
    if not isinstance(value, dict) or not isinstance(value.get("sha256"), str):
        return False
    body = dict(value); seal = body.pop("sha256")
    return seal == sha(canonical(body))


def safe_path(root: Path, name: str) -> Path:
    require(isinstance(name, str) and name and not Path(name).is_absolute(),
            "relative_path")
    path = (root / name).resolve()
    require(path == root.resolve() or root.resolve() in path.parents,
            "path_escape")
    require(not path.is_symlink() and path.is_file(), "unsafe_file:" + name)
    return path


def file_hash(path: Path, expected_bytes: int | None = None,
              cap: int = 1 << 30) -> tuple[int, str]:
    size = path.stat().st_size
    require(size <= cap, "file_cap")
    if expected_bytes is not None:
        require(size == expected_bytes, "file_size")
    h = hashlib.sha256(); total = 0
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1 << 20)
            if not chunk:
                break
            h.update(chunk); total += len(chunk)
    require(total == size, "file_read_size")
    return total, h.hexdigest()


def read_json(path: Path, expected_bytes: int | None = None,
              expected_sha: str | None = None, cap: int = 1 << 28) -> tuple[Any, bytes]:
    size, actual = file_hash(path, expected_bytes, cap)
    raw = path.read_bytes()
    require(len(raw) == size and (expected_sha is None or actual == expected_sha),
            "json_digest")
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeError, ValueError) as exc:
        raise RuntimeError("json_decode") from exc
    require(canonical(value) == raw, "json_canonical")
    return value, raw


def read_json_stream(path: Path, expected_bytes: int, expected_sha: str,
                     cap: int = 1 << 28) -> Any:
    """Authenticate a large canonical body without retaining raw bytes too."""
    size, actual = file_hash(path, expected_bytes, cap)
    require(size == expected_bytes and actual == expected_sha, "json_stream_digest")
    try:
        with path.open("rb") as stream:
            value = json.load(stream)
    except (OSError, UnicodeError, ValueError) as exc:
        raise RuntimeError("json_stream_decode") from exc
    require(isinstance(value, dict), "json_stream_object")
    return value


def receipt(root: Path, value: Any, cap: int = 1 << 30) -> bytes:
    require(isinstance(value, dict) and set(value) == {"file", "bytes", "sha256"},
            "receipt_shape")
    digest(value["sha256"], "receipt_digest_shape")
    path = safe_path(root, value["file"])
    size, actual = file_hash(path, value["bytes"], cap)
    require(actual == value["sha256"], "receipt_digest")
    return path.read_bytes()


def verify_source_pin() -> None:
    size, actual = file_hash(ARITH_PATH)
    require(actual == ARITH_SHA256 and size > 1000, "arithmetic_source_pin")


def sparse_entries(vector: np.ndarray) -> list[tuple[int, int]]:
    value = np.asarray(vector, dtype=np.uint8).reshape(-1)
    require(value.size == SOURCE_WIDTH and not np.any(value > 2), "covector_width")
    return [(int(i), int(value[i])) for i in np.flatnonzero(value)]


def sparse_projection(packed_row: bytes, byte_offset: int,
                      entries: Iterable[tuple[int, int]]) -> int:
    require(type(packed_row) is bytes and len(packed_row) == P1_ROW_BYTES,
            "packed_row_shape")
    total = 0
    for index, coefficient in entries:
        require(0 <= index < SOURCE_WIDTH and coefficient in (1, 2),
                "sparse_entry")
        digit = (packed_row[byte_offset + index // 4] // POW3[index % 4]) % 3
        total += coefficient * digit
    return total % 3


def check_table_transpose(forward: Iterable[Iterable[int]],
                          adjoint: Iterable[Iterable[int]]) -> None:
    """Check the table-level transpose relation used by the live parent."""
    expected = sorted((int(destination), int(source), int(coefficient))
                      for source, destination, coefficient in forward)
    require(list(adjoint) == expected, "task712_transpose")


def dense_projection(packed_row: bytes, byte_offset: int,
                     vector: np.ndarray) -> int:
    dense = ARITH.unpack_trits(packed_row[byte_offset:byte_offset + SLICE_BYTES],
                               SOURCE_WIDTH)
    return ARITH.dot_mod3(dense, vector)


def vectorized_projection_chunk(packed_rows: np.ndarray, byte_offset: int,
                                projections: list[tuple[np.ndarray, np.ndarray, np.ndarray]]) -> np.ndarray:
    """Project one bounded row chunk with the exact sparse packed kernel."""
    rows = np.asarray(packed_rows, dtype=np.uint8)
    require(rows.ndim == 2 and rows.shape[1] == P1_ROW_BYTES and
            0 <= byte_offset <= P1_ROW_BYTES - SLICE_BYTES, "projection_chunk_shape")
    result = np.zeros((rows.shape[0], len(projections)), dtype=np.uint8)
    for slot, (byte_index, digit_slot, coefficient) in enumerate(projections):
        if not len(byte_index):
            continue
        selected = rows[:, byte_offset + byte_index]
        powers = np.asarray([POW3[i] for i in digit_slot], dtype=np.uint8)
        digits = (selected // powers) % 3
        result[:, slot] = (np.sum(digits.astype(np.uint32) * coefficient,
                                  axis=1, dtype=np.uint32) % 3).astype(np.uint8)
    return result


def relation_source_sha256() -> str:
    """Digest the fixed coefficient source without reserializing its terms."""
    old_offsets = [0]
    for rank in OLD_RANKS[:-1]:
        old_offsets.append(old_offsets[-1] + rank)
    new_offsets = [sum(OLD_RANKS)]
    for rank in NEW_RANKS[:-1]:
        new_offsets.append(new_offsets[-1] + rank)
    return sha(canonical({
        "schema": SCHEMA + ".relation-stream", "body_sha256": list(TASK554_BODY_DIGESTS),
        "old_ranks": list(OLD_RANKS), "new_ranks": list(NEW_RANKS),
        "old_offsets": old_offsets, "new_offsets": new_offsets,
        "actor_order": list(ACTORS), "seed_count": 44,
        "origin_count": TASK554_ORIGINS, "relation_count": SCALAR_ORIGINS,
        "evaluator_version": "direct-blockwise-scalar-v1",
        "source_pin": "task554-v3-body-pins"}))


def _expression(value: Any, bound: int, reason: str) -> None:
    require(isinstance(value, list), reason + ":list")
    seen: set[int] = set()
    for item in value:
        require(isinstance(item, list) and len(item) == 2 and
                plain_int(item[0]) and plain_int(item[1]) and
                0 <= item[0] < bound and item[1] in (1, 2), reason + ":entry")
        require(item[0] not in seen, reason + ":duplicate")
        seen.add(item[0])


def _validate_task554_body(body: Any, index: int) -> None:
    require(isinstance(body, dict), "task554_body")
    if index == -1:
        olds = body.get("old_blocks"); origins = body.get("defect_origins")
        packets = body.get("packets")
        require(isinstance(olds, list) and len(olds) == 4 and
                isinstance(origins, list) and len(origins) == TASK554_ORIGINS and
                isinstance(packets, list) and len(packets) == 4, "task554_prepare_shape")
        cursor = 0
        for character, old in enumerate(olds):
            rank = OLD_RANKS[character]
            require(old.get("character_index") == character and
                    old.get("character") == list(CHARACTERS[character]) and
                    old.get("rank") == rank, "task554_old_rank")
            record = old.get("record")
            require(isinstance(record, dict) and record.get("rank") == rank and
                    record.get("character") == list(CHARACTERS[character]) and
                    record.get("attempts") == 44 + 4 * rank and
                    record.get("actor_order") == list(ACTORS) and
                    record.get("queue_exhausted") is True and
                    len(record.get("seed_reductions", [])) == 44 and
                    len(record.get("dag_nodes", [])) == rank and
                    len(record.get("actor_transitions", [])) == rank, "task554_old_record")
            for expression in record["seed_reductions"]:
                _expression(expression, rank, "task554_seed")
            for row in record["actor_transitions"]:
                require(isinstance(row, list) and len(row) == 4, "task554_old_actor")
                for expression in row:
                    _expression(expression, rank, "task554_actor")
            for pivot, node in enumerate(record["dag_nodes"]):
                require(node.get("pivot") == pivot and node.get("scale") in (1, 2),
                        "task554_old_node")
                _expression(node.get("reductions"), rank, "task554_old_reduction")
            require(old.get("defect_origin_range") == list(ORIGIN_RANGES[character]) and
                    ORIGIN_RANGES[character][0] == cursor, "task554_origin_range")
            cursor += 44 + 4 * rank
        require(cursor == len(origins), "task554_origin_eof")
    else:
        rank = NEW_RANKS[index]
        require(body.get("phase") == "block" and body.get("character_index") == index and
                body.get("character") == list(CHARACTERS[index]) and
                body.get("rank") == rank and body.get("origin_count") == TASK554_ORIGINS and
                body.get("attempts") == TASK554_ORIGINS + 4 * rank and
                body.get("actor_order") == list(ACTORS) and
                body.get("queue_exhausted") is True, "task554_new_metadata")
        reductions = body.get("origin_reductions"); transitions = body.get("actor_transitions")
        nodes = body.get("dag_nodes"); leads = body.get("pivot_leads")
        require(isinstance(reductions, list) and len(reductions) == TASK554_ORIGINS and
                isinstance(transitions, list) and len(transitions) == rank and
                isinstance(nodes, list) and len(nodes) == rank and
                isinstance(leads, list) and len(leads) == rank and
                len(set(leads)) == rank, "task554_new_lists")
        for expression in reductions:
            _expression(expression, rank, "task554_new_origin")
        for row in transitions:
            require(isinstance(row, list) and len(row) == 4, "task554_new_actor")
            for expression in row:
                _expression(expression, rank, "task554_new_transition")
        for pivot, node in enumerate(nodes):
            require(node.get("pivot") == pivot and node.get("lead") == leads[pivot] and
                    node.get("scale") in (1, 2), "task554_new_node")
            _expression(node.get("reductions"), rank, "task554_new_reduction")
        require(body.get("dag_sha256") == sha(canonical(nodes)), "task554_dag_digest")


def _state_descriptor(parent: dict[str, Any], index: int) -> dict[str, Any]:
    require(isinstance(parent, dict) and set(parent) == {"root", "head", "body", "files"},
            "task554_state_descriptor")
    root = Path(parent["root"]).absolute(); require(root.is_dir(), "task554_root")
    stem = "prepare" if index == -1 else "block-" + str(index)
    expected = TASK554_BODY_DIGESTS[0 if index == -1 else index + 1]
    head = parent["head"]; body = parent["body"]
    require(head == {"file": stem + ".HEAD", "bytes": head["bytes"], "sha256": head["sha256"]},
            "task554_head_name")
    require(body.get("file") == stem + "." + expected + ".json" and
            body.get("sha256") == expected, "task554_body_name")
    require(isinstance(parent["files"], list) and
            sorted(parent["files"], key=lambda x: x["file"]) ==
            sorted([head, body], key=lambda x: x["file"]), "task554_body_only_roster")
    head_value, head_raw = read_json(safe_path(root, head["file"]), head["bytes"],
                                     head["sha256"], 1 << 20)
    body_path = safe_path(root, body["file"])
    body_value = read_json_stream(body_path, body["bytes"], body["sha256"], 1 << 28)
    require(head_value == {"body_sha256": expected,
                           "parent_sha256": None if index == -1 else TASK554_BODY_DIGESTS[0],
                           "schema": "d972.r07.a0.first-rung-grade1.v3.state.head",
                           "stem": stem}, "task554_head_join")
    require(body_value.get("schema") == "d972.r07.a0.first-rung-grade1.v3.state" and
            body_value.get("phase") == ("prepare" if index == -1 else "block") and
            body_value.get("parent_sha256") == (None if index == -1 else TASK554_BODY_DIGESTS[0]),
            "task554_body_join")
    _validate_task554_body(body_value, index)
    return {"root": root, "head": head_value, "body": body_value,
            "body_sha256": expected, "index": index}


def validate_task554(parent: Any) -> dict[str, Any]:
    require(isinstance(parent, dict) and set(parent) ==
            {"schema", "source_run", "source_attempt", "source_head", "artifacts",
             "prepare", "blocks"} and
            parent["schema"] == SCHEMA + ".task554-parent.v1" and
            parent["source_run"] == TASK554_RUN and parent["source_attempt"] == TASK554_ATTEMPT and
            parent["source_head"] == TASK554_HEAD and len(parent["blocks"]) == 4,
            "task554_parent")
    require(parent["artifacts"] == [
        {"id": item[0], "name": item[1], "bytes": item[2], "sha256": item[3]}
        for item in TASK554_ARTIFACTS], "task554_artifact_pins")
    # Do not open the five state bodies at launch validation time.  The
    # relation builder below opens prepare once and one block at a time.
    for state in [parent["prepare"], *parent["blocks"]]:
        require(isinstance(state, dict) and set(state) ==
                {"root", "head", "body", "files"}, "task554_state_descriptor")
    return {"parent": parent, "source_run": TASK554_RUN,
            "source_attempt": TASK554_ATTEMPT, "source_head": TASK554_HEAD}


def _shifted_terms(expression: Any, bound: int, offset: int) -> list[list[int]]:
    _expression(expression, bound, "relation_expression")
    return [[offset + int(index), int(coefficient)] for index, coefficient in expression]


def _subtract_expression(accumulator: Any, expression: Any, values: np.ndarray,
                         bound: int, offset: int, relation_hash: Any,
                         label: dict[str, Any]) -> int:
    """Apply a relation directly; no global relation list is materialized."""
    # The body validator has already authenticated unique, in-range local
    # terms with coefficients in {1,2}; preserve source order in the hot loop.
    terms = expression
    result = int(accumulator)
    for index, coefficient in terms:
        result = (result - int(coefficient) * int(values[offset + index])) % 3
    return result


def accumulate_scalars(parent: dict[str, Any], character: int, direct: list[int],
                       children: list[np.ndarray], values: list[np.ndarray]) -> dict[str, Any]:
    """Fubini/blockwise evaluator for 44+4*8059 scalar accumulators.

    Only prepare and one new block are live at a time.  The accumulator is
    32280 uint8 values; it is not the nested v15 relation tree.
    """
    require(len(direct) == 44 and len(children) == 4 and len(values) == 5,
            "scalar_accumulator_inputs")
    prepare = _state_descriptor(parent["prepare"], -1); old = prepare["body"]["old_blocks"]
    old_offsets: list[int] = []; cursor = 0
    for rank in OLD_RANKS:
        old_offsets.append(cursor); cursor += rank
    new_offsets: list[int] = []; cursor = sum(OLD_RANKS)
    for rank in NEW_RANKS:
        new_offsets.append(cursor); cursor += rank
    require(cursor == P1_ROWS, "scalar_accumulator_offsets")
    seeds = np.asarray(direct, dtype=np.uint8).copy()
    actor_values = np.column_stack([np.asarray(item, dtype=np.uint8) for item in values[1:]])
    require(actor_values.shape == (P1_ROWS, 4), "scalar_accumulator_shape")
    # This is a receipt of the fixed Task554 coefficient family, not of a
    # particular q/character evaluation.  Keep q-dependent values out of it
    # so every character can join the same authenticated relation source.
    relation_hash = relation_source_sha256()
    for seed in range(44):
        for source, old_block in enumerate(old):
            seeds[seed] = _subtract_expression(
                seeds[seed], old_block["record"]["seed_reductions"][seed], values[0],
                OLD_RANKS[source], old_offsets[source], relation_hash,
                {"kind": "seed-old", "source": source, "seed": seed})
    old_actor_cursor = 0
    for source, old_block in enumerate(old):
        for pivot in range(OLD_RANKS[source]):
            global_row = old_offsets[source] + pivot
            for slot in range(4):
                actor_values[global_row, slot] = _subtract_expression(
                    actor_values[global_row, slot], old_block["record"]["actor_transitions"][pivot][slot],
                    values[0], OLD_RANKS[source], old_offsets[source], relation_hash,
                    {"kind": "actor-old", "basis_i": global_row, "slot": slot})
            old_actor_cursor += 1
    # Fold each new block's origin reductions into the same scalar accumulators,
    # append its own actor transitions, and release that body immediately.
    for target in range(4):
        block = _state_descriptor(parent["blocks"][target], target)
        body = block["body"]; rank = NEW_RANKS[target]; offset = new_offsets[target]
        reductions = body["origin_reductions"]
        for seed in range(44):
            for source in range(4):
                seeds[seed] = _subtract_expression(
                    seeds[seed], reductions[ORIGIN_RANGES[source][0] + seed], values[0], rank,
                    new_offsets[target], relation_hash, {"kind": "seed-new", "target": target,
                                     "source": source, "seed": seed})
        for source in range(4):
            for pivot in range(OLD_RANKS[source]):
                global_row = old_offsets[source] + pivot
                for slot in range(4):
                    origin = ORIGIN_RANGES[source][0] + 44 + 4 * pivot + slot
                    actor_values[global_row, slot] = _subtract_expression(
                        actor_values[global_row, slot], reductions[origin], values[0], rank,
                        new_offsets[target], relation_hash, {"kind": "actor-new-old", "target": target,
                                         "basis_i": global_row, "slot": slot})
        transitions = body["actor_transitions"]
        for local, row in enumerate(transitions):
            global_row = offset + local
            for slot in range(4):
                actor_values[global_row, slot] = _subtract_expression(
                    actor_values[global_row, slot], row[slot], values[0], rank,
                    new_offsets[target], relation_hash, {"kind": "actor-new", "target": target,
                     "basis_i": global_row, "slot": slot})
        del transitions, reductions, body, block
    del prepare, old
    return {"seed_values": seeds, "actor_values": actor_values,
            "relation_sha256": relation_hash,
            "origins": SCALAR_ORIGINS, "accumulator_count": SCALAR_ORIGINS}


def validate_p1(parent: Any) -> dict[str, Any]:
    require(isinstance(parent, dict) and set(parent) ==
            {"root", "manifest", "files", "run", "attempt", "head", "artifact",
             "artifact_name", "archive_bytes", "archive_sha256"}, "p1_parent")
    require(parent["run"] == P1_RUN and parent["attempt"] == P1_ATTEMPT and
            parent["head"] == P1_HEAD and parent["artifact"] == P1_ARTIFACT and
            parent["artifact_name"] == P1_ARTIFACT_NAME and
            parent["archive_bytes"] == P1_ARCHIVE_BYTES and
            parent["archive_sha256"] == P1_ARCHIVE_SHA256, "p1_identity")
    root = Path(parent["root"]).absolute(); require(root.is_dir(), "p1_root")
    manifest, raw = read_json(safe_path(root, parent["manifest"]["file"]),
                              P1_MANIFEST_BYTES, P1_MANIFEST_SHA256, 1 << 20)
    require(parent["manifest"] == {"file": "manifest.json", "bytes": P1_MANIFEST_BYTES,
                                    "sha256": P1_MANIFEST_SHA256}, "p1_manifest_receipt")
    require(manifest.get("schema") == "d972.r07.canonical-p1-dag-degree2-lift.v8" and
            manifest.get("status") == "CANONICAL_P1_DAG_DEGREE2_LIFT_CANDIDATE" and
            manifest.get("rows") == P1_ROWS and manifest.get("row_trits") == P1_ROW_TRITS and
            manifest.get("row_bytes") == P1_ROW_BYTES and
            manifest.get("global_order") == [0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059] and
            manifest.get("actor_order") == list(ACTORS) and
            manifest.get("character_order") == [list(x) for x in CHARACTERS] and
            manifest.get("independent_checker") is False and
            all(manifest.get(k) is False for k in ("A0", "COMMON", "COFINAL", "FAKE", "IHARA", "verified")),
            "p1_manifest_shape")
    cache = manifest.get("cache"); instruction = manifest.get("instruction")
    require(cache == {"path": "degree2.cache.bin", "rows": P1_ROWS,
                      "bytes": P1_CACHE_BYTES, "sha256": P1_CACHE_SHA256,
                      "final_lf": False, "eof": True}, "p1_cache_receipt")
    require(instruction == {"path": "instructions.jsonl", "rows": P1_ROWS,
                            "bytes": P1_INSTRUCTION_BYTES, "sha256": P1_INSTRUCTION_SHA256,
                            "final_lf": True, "eof": True,
                            "final_head": manifest.get("ancestry_sha256")}, "p1_instruction_receipt")
    expected_files = [{"file": "degree2.cache.bin", "bytes": P1_CACHE_BYTES,
                       "sha256": P1_CACHE_SHA256},
                      {"file": "instructions.jsonl", "bytes": P1_INSTRUCTION_BYTES,
                       "sha256": P1_INSTRUCTION_SHA256}]
    require(parent["files"] == expected_files and
            {p.name for p in root.iterdir()} == {"manifest.json", "degree2.cache.bin", "instructions.jsonl"},
            "p1_file_roster")
    require(manifest.get("ancestry_sha256") == instruction["final_head"], "p1_ancestry")
    return {"root": root, "manifest": manifest, "manifest_sha256": sha(raw),
            "cache": cache, "instruction": instruction}


def validate_separator(parent: Any) -> dict[str, Any]:
    require(isinstance(parent, dict) and set(parent) ==
            {"schema", "root", "artifact", "manifest", "physical", "lambda", "internal"} and
            parent["schema"] == SCHEMA + ".separator-parent.v1" and
            parent["artifact"] == {"run": SEPARATOR_RUN, "attempt": SEPARATOR_ATTEMPT,
                                    "head": SEPARATOR_HEAD, "id": SEPARATOR_ARTIFACT,
                                    "name": SEPARATOR_ARTIFACT_NAME, "bytes": SEPARATOR_ARCHIVE_BYTES,
                                    "sha256": SEPARATOR_ARCHIVE_SHA256}, "separator_identity")
    root = Path(parent["root"]).absolute(); require(root.is_dir(), "separator_root")
    manifest_path = safe_path(root, parent["manifest"]["file"])
    manifest_value, manifest_raw = read_json(manifest_path, None, SEPARATOR_MANIFEST_SHA256, 1 << 20)
    require(parent["manifest"]["sha256"] == SEPARATOR_MANIFEST_SHA256 and
            manifest_value.get("generation") == SEPARATOR_GENERATION and
            manifest_value.get("rank") == SEPARATOR_RANK and
            manifest_value.get("instructions", {}).get("final_head") == SEPARATOR_STATE_HEAD and
            manifest_value.get("candidate_roster") ==
            ["physical.bin", "physical-p1-coeff.bin", "instructions.jsonl",
             "manifest.json", "HEAD"], "separator_manifest_shape")
    lam_raw = receipt(root, parent["lambda"], PHYSICAL_PACKED_BYTES)
    require(len(lam_raw) == SEPARATOR_LAMBDA_BYTES and sha(lam_raw) == SEPARATOR_LAMBDA_SHA256,
            "separator_lambda_pin")
    lam = ARITH.unpack_trits(lam_raw, PHYSICAL_WIDTH)
    physical = parent["physical"]
    require(physical == {"file": "state/physical.bin", "bytes": SEPARATOR_PHYSICAL_BYTES,
                         "sha256": SEPARATOR_PHYSICAL_SHA256, "rows": SEPARATOR_RANK},
            "separator_physical_receipt")
    path = safe_path(root, physical["file"]); h = hashlib.sha256(); rolling = b"\0" * 32
    with path.open("rb") as stream:
        for _ in range(SEPARATOR_RANK):
            packed = stream.read(PHYSICAL_PACKED_BYTES)
            require(len(packed) == PHYSICAL_PACKED_BYTES, "separator_physical_eof")
            row = ARITH.unpack_trits(packed, PHYSICAL_WIDTH)
            require(ARITH.dot_mod3(lam, row) == 0, "separator_lambda_row")
            h.update(packed); rolling = hashlib.sha256(rolling + packed).digest()
        require(stream.read(1) == b"", "separator_physical_trailing")
    require(h.hexdigest() == SEPARATOR_PHYSICAL_SHA256, "separator_physical_digest")
    for item, expected in ((parent["internal"]["terminal"], SEPARATOR_TERMINAL_SHA256),
                           (parent["internal"]["result"], SEPARATOR_RESULT_SHA256),
                           (parent["internal"]["checker"], SEPARATOR_CHECKER_SHA256)):
        data = receipt(root, item, 1 << 24); require(sha(data) == expected, "separator_internal_pin")
    return {"root": root, "manifest": manifest_value, "manifest_sha256": sha(manifest_raw),
            "lambda": lam, "lambda_sha256": sha(lam_raw), "generation": SEPARATOR_GENERATION,
            "physical_rows": SEPARATOR_RANK, "rolling_head": rolling.hex()}


def validate_launch(path: Path) -> dict[str, Any]:
    launch, raw = read_json(path, cap=1 << 24)
    require(isinstance(launch, dict) and set(launch) ==
            {"schema", "fixture_only", "mode", "characters", "actors", "p1_parent",
             "task554_parent", "task712_parents", "separator_parent", "out", "claims",
             "source_pin"} and launch["schema"] == SCHEMA + ".launch.v1" and
            launch["fixture_only"] is False and launch["mode"] == "actual" and
            launch["characters"] == [list(x) for x in CHARACTERS] and
            launch["actors"] == list(ACTORS) and launch["claims"] == {
                "ROOT_SCALAR_BATCH_CANDIDATE": True, "COMPLETE_DUAL_ORBITS": False,
                "GRADE2_MEMBER": "NOT_DECIDED", "GRADE2_NONMEMBER": "NOT_DECIDED",
                "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED", "COFINAL_LIFT": "NOT_DECLARED",
                "FAKE": "NOT_DECLARED", "IHARA": "NOT_DECLARED", "verified": False},
            "launch_shape")
    verify_source_pin()
    require(launch["source_pin"] == {
        "producer": {"path": str(ARITH_PATH.as_posix()), "sha256": ARITH_SHA256},
        "checker": {"path": str(CHECKER_ARITH_PATH.as_posix()), "sha256": CHECKER_ARITH_SHA256}},
        "launch_source_pin")
    separator = validate_separator(launch["separator_parent"])
    p1 = validate_p1(launch["p1_parent"])
    task554 = validate_task554(launch["task554_parent"])
    task712 = launch["task712_parents"]
    require(isinstance(task712, list) and len(task712) == 4, "task712_parent_list")
    for item in task712:
        require(set(item) == set(TASK712_PARENT) | {"root"} and
                {k: item[k] for k in TASK712_PARENT} == TASK712_PARENT, "task712_parent_pin")
    return {"launch": launch, "launch_raw": raw, "launch_sha256": sha(raw),
            "separator": separator, "p1": p1, "task554": task554,
            "task712": task712}


def make_covectors(separator: dict[str, Any], task712: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[list[np.ndarray]]]:
    tables: list[dict[str, Any]] = []
    vectors: list[list[np.ndarray]] = []
    for character in range(4):
        table = ARITH.read_task712_envelope(task712[character], character)
        for key in ("B", *ACTORS):
            check_table_transpose(table["forward"][key], table["adjoint"][key])
        tables.append(table)
        root = ARITH.sparse_adjoint(table["forward"]["B"], SOURCE_WIDTH,
                                    PHYSICAL_WIDTH, separator["lambda"])
        children = [ARITH.sparse_adjoint(table["forward"][actor], SOURCE_WIDTH,
                                         SOURCE_WIDTH, root) for actor in ACTORS]
        vectors.append([root] + children)
        packed = ARITH.pack_trits(root)
        support = int(np.count_nonzero(root)); nz = np.flatnonzero(root)
        expected = EXPECTED_ROOT[character]
        require((support, int(nz[0]) if len(nz) else None,
                 int(root[nz[0]]) if len(nz) else None, sha(packed)) == expected,
                "actual_root_pin")
        for slot, child in enumerate(children):
            require(sha(ARITH.pack_trits(child)) == EXPECTED_CHILD[character][slot],
                    "actual_child_pin")
    return tables, vectors


def p1_batch(p1: dict[str, Any], vectors: list[list[np.ndarray]]) -> dict[str, Any]:
    covectors = [[sparse_entries(vector) for vector in group] for group in vectors]
    values = [[np.zeros(P1_ROWS, dtype=np.uint8) for _ in range(5)] for _ in range(4)]
    inst_path = safe_path(p1["root"], p1["instruction"]["path"])
    inst_size, inst_sha = file_hash(inst_path, P1_INSTRUCTION_BYTES, 1 << 30)
    require(inst_size == P1_INSTRUCTION_BYTES and inst_sha == P1_INSTRUCTION_SHA256,
            "p1_instruction_stream_pin")
    cache_path = safe_path(p1["root"], p1["cache"]["path"])
    cache_hash = hashlib.sha256(); started = time.monotonic()
    active = [bool(np.count_nonzero(group[0])) for group in vectors]
    require(active == [True, False, False, False], "actual_active_root_pin")
    # The union of each active covector's packed coordinates is gathered per
    # bounded row chunk.  This is sparse projection, not a dense row matrix.
    projections = []
    for character in range(4):
        group = []
        for entries in covectors[character]:
            if entries:
                byte_index = np.asarray([i // 4 for i, _ in entries], dtype=np.int64)
                digit_slot = np.asarray([i % 4 for i, _ in entries], dtype=np.int64)
                coefficient = np.asarray([c for _, c in entries], dtype=np.uint32)
            else:
                byte_index = digit_slot = np.asarray([], dtype=np.int64)
                coefficient = np.asarray([], dtype=np.uint32)
            group.append((byte_index, digit_slot, coefficient))
        projections.append(group)
    buffer = bytearray(P1_ROW_BYTES * 256)
    with cache_path.open("rb") as stream:
        cursor = 0
        while cursor < P1_ROWS:
            count_rows = min(256, P1_ROWS - cursor)
            byte_count = count_rows * P1_ROW_BYTES
            count = stream.readinto(memoryview(buffer)[:byte_count])
            require(count == byte_count, "p1_cache_row_eof")
            raw_chunk = memoryview(buffer)[:byte_count]
            cache_hash.update(raw_chunk)
            packed_rows = np.frombuffer(raw_chunk, dtype=np.uint8).reshape(count_rows, P1_ROW_BYTES)
            # Actual preflight shows only character zero is nonzero.  Zero
            # characters remain authenticated arrays without wasted pairings.
            for character in range(4):
                if not active[character]:
                    continue
                projected = vectorized_projection_chunk(
                    packed_rows, character * SLICE_BYTES, projections[character])
                for slot in range(5):
                    values[character][slot][cursor:cursor + count_rows] = projected[:, slot]
            cursor += count_rows
        require(stream.read(1) == b"", "p1_cache_trailing")
    require(cache_hash.hexdigest() == P1_CACHE_SHA256, "p1_cache_stream_pin")
    flat = [item for group in values for item in group]
    return {"rows": P1_ROWS, "values": values,
            "value_sha256": [sha(item.tobytes()) for item in flat],
            "cache_sha256": cache_hash.hexdigest(), "instruction_sha256": inst_sha,
            "manifest_sha256": p1["manifest_sha256"], "cache_passes": 1,
            "instruction_passes": 1, "elapsed_seconds": time.monotonic() - started,
            "extra_open_count": 0, "active_characters": [0],
            "active_pairings": 5, "sparse_chunk_rows": 256}


def raw_dual(character: int, tables: dict[str, Any], separator: dict[str, Any],
             vector: np.ndarray) -> dict[str, Any]:
    packed = ARITH.pack_trits(vector)
    body = {"schema": ARITH.LIVE_SCHEMA + ".RawDual",
            "separator_generation": separator["generation"],
            "separator_s_head_sha256": separator["manifest"].get("state_head", SEPARATOR_STATE_HEAD),
            "lambda_sha256": separator["lambda_sha256"], "character": character,
            "B_adj_table_identity": tables["identity"]["adjoint:B"],
            "word_node": {"kind": "root", "character": character, "actors": []},
            "actor_table_identities_along_w": [],
            "raw_q_packed_sha256": sha(packed), "raw_q_packed_offset": 0,
            "raw_q_packed_length": len(packed), "raw_predecessor_sha256": None}
    return {**body, "sha256": sha(canonical(body))}


def _scan_accumulated(raw: dict[str, Any], accum: dict[str, Any],
                      p1: dict[str, Any]) -> dict[str, Any]:
    """Scan fixed seed/actor order after the blockwise fold."""
    ARITH.validate_raw_dual(raw)
    seeds = accum["seed_values"]; actors = accum["actor_values"]
    require(len(seeds) == 44 and actors.shape == (P1_ROWS, 4), "scalar_accumulator_scan_shape")
    chain = b"\0" * 32; origin = 0
    def emit(kind: str, descriptor: dict[str, Any], scalar: int) -> dict[str, Any] | None:
        nonlocal chain, origin
        record = {"origin_id": origin, "origin_kind": kind, **descriptor,
                  "scalar": int(scalar)}
        chain = hashlib.sha256(chain + canonical(record)).digest(); origin += 1
        if scalar:
            return ARITH._sealed("Violation", {
                "raw_dual_sha256": raw["sha256"], "character": raw["character"],
                "word_node_sha256": sha(canonical(raw["word_node"])), **record,
                "scalar_prefix_digest": chain.hex(), "p1_manifest_sha256": p1["manifest_sha256"],
                "global_relation_stream_sha256": accum["relation_sha256"]})
        return None
    for seed in range(44):
        hit = emit("seed", {"seed": seed}, int(seeds[seed]))
        if hit is not None:
            return hit
    for basis_i in range(P1_ROWS):
        for slot, actor in enumerate(ACTORS):
            hit = emit("actor", {"basis_i": basis_i, "actor": actor},
                       int(actors[basis_i, slot]))
            if hit is not None:
                return hit
    require(origin == SCALAR_ORIGINS, "scalar_accumulator_origin_eof")
    return ARITH._sealed("ScalarEOF", {
        "raw_dual_sha256": raw["sha256"], "p1_manifest_sha256": p1["manifest_sha256"],
        "global_relation_stream_sha256": accum["relation_sha256"], "origins": SCALAR_ORIGINS,
        "seed_pairings": 44, "actor_pairings": 4 * P1_ROWS, "next_origin": SCALAR_ORIGINS,
        "coefficient_stream_eof": True, "p1_cache_pass_eof": True,
        "value_vector_sha256": [sha(value.tobytes()) for value in p1["values"]],
        "rolling_scalar_head": chain.hex()})


def _scalar_result(character: int, tables: dict[str, Any], vectors: list[np.ndarray],
                   parent: dict[str, Any], p1: dict[str, Any], separator: dict[str, Any],
                   p1_values: list[np.ndarray]) -> dict[str, Any]:
    root = vectors[0]; packed = ARITH.pack_trits(root)
    positions = np.flatnonzero(root)
    child_receipts = [{"actor": actor, "support": int(np.count_nonzero(v)),
                       "packed_sha256": sha(ARITH.pack_trits(v))}
                      for actor, v in zip(ACTORS, vectors[1:])]
    base = {"character": character, "character_label": list(CHARACTERS[character]),
            "root_support": int(np.count_nonzero(root)),
            "root_packed_sha256": sha(packed),
            "children": child_receipts,
            "task712_table_identities": tables["identity"],
            "raw_dual": raw_dual(character, tables, separator, root),
            "root_packed_bytes": len(packed)}
    ARITH.validate_raw_dual(base["raw_dual"])
    if not len(positions):
        zero = {"schema": SCHEMA + ".RootZero", **base, "root_scalar": "zero"}
        zero["sha256"] = sha(canonical(zero))
        require(sealed_object(zero), "character_embedded_seal")
        return zero
    direct = ARITH.direct_seed_evaluations(root, character)
    accumulator = accumulate_scalars(parent, character, direct, vectors[1:], p1_values)
    base["relation_stream_sha256"] = accumulator["relation_sha256"]
    scalar = _scan_accumulated(base["raw_dual"], accumulator,
                                {"manifest_sha256": p1["manifest_sha256"], "values": p1_values})
    base["scalar"] = scalar
    base["scalar_schema"] = scalar["schema"]
    if scalar["schema"].endswith("Violation"):
        kind = "Violation"
    else:
        kind = "ScalarEOF"
    if kind == "ScalarEOF":
        nz = int(positions[0]); scale = 1 if int(root[nz]) == 1 else 2
        normalized_packed = ARITH.pack_trits((scale * root.astype(np.uint16) % 3).astype(np.uint8))
        normalized_sha = sha(normalized_packed)
        remainder_sha = sha(packed)  # no prior pivots at the root
        next_head = ARITH._dual_next_state_head(
            "0" * 64, 0, nz, normalized_sha, base["raw_dual"]["sha256"],
            remainder_sha, 1)
        base["normalized_root_state"] = {"lead": nz, "scale": scale,
            "raw_lead": nz, "raw_lead_scalar": int(root[nz]),
            "raw_packed_sha256": sha(packed), "raw_q_file": f"q-a{character}-root.bin",
            "raw_q_file_bytes": len(packed), "raw_q_file_sha256": sha(packed),
            "raw_dual_sha256": base["raw_dual"]["sha256"],
            "remainder_sha256": remainder_sha,
            "normalized_packed_sha256": normalized_sha,
            "packed_sha256": normalized_sha, "normalized_pivot_sha256": normalized_sha,
            "normalized_packed_bytes": len(normalized_packed),
            "prior_state_head_sha256": "0" * 64, "prior_pivot_coefficients": [],
            "rank_before": 0, "insertion_id": 0, "dual_rank_after": 1,
            "next_state_head_sha256": next_head, "rolling_head": next_head,
            "normalized_from_raw_q": True,
            "future_orbit_bound": 504,
            "remaining_independent_after_root": 503}
    wrapper = {"schema": SCHEMA + ".Root" + kind, **base}
    wrapper["sha256"] = sha(canonical(wrapper))
    require(sealed_object(wrapper), "character_embedded_seal")
    return wrapper


def _write_json(root: Path, name: str, value: Any) -> dict[str, Any]:
    raw = canonical(value); path = root / name; path.write_bytes(raw)
    return {"file": name, "bytes": len(raw), "sha256": sha(raw)}


def _write_bytes(root: Path, name: str, raw: bytes) -> dict[str, Any]:
    (root / name).write_bytes(raw)
    return {"file": name, "bytes": len(raw), "sha256": sha(raw)}


def terminal_kind(records: list[dict[str, Any]]) -> str:
    require(isinstance(records, list) and len(records) == 4,
            "terminal_record_count")
    return ("RootViolationBatch" if any(
        item.get("scalar_schema", "").endswith("Violation") for item in records)
            else "AllFourRootEOF")


def run_actual(launch_path: Path) -> dict[str, Any]:
    base = validate_launch(launch_path); launch = base["launch"]
    out = Path(launch["out"]).absolute(); require(not out.exists(), "output_must_be_fresh")
    out.mkdir(parents=True)
    separator = base["separator"]; tables, vectors = make_covectors(separator, base["task712"])
    cache = p1_batch(base["p1"], vectors)
    records: list[dict[str, Any]] = []; files: list[dict[str, Any]] = []
    for character in range(4):
        for slot, actor in enumerate(ACTORS):
            files.append(_write_bytes(out, f"q-a{character}-t{slot}.bin",
                                      ARITH.pack_trits(vectors[character][slot + 1])))
        files.append(_write_bytes(out, f"q-a{character}-root.bin", ARITH.pack_trits(vectors[character][0])))
        record = _scalar_result(character, tables[character], vectors[character], launch["task554_parent"],
                                base["p1"], separator, cache["values"][character])
        records.append(record)
        files.append(_write_json(out, f"character-a{character}.json", record))
        if record["schema"].endswith("RootScalarEOF"):
            files.append(_write_json(out, f"root-state-a{character}.json",
                                     record["normalized_root_state"]))
    terminal_value = terminal_kind(records)
    terminal_body = {"schema": SCHEMA + ".terminal", "terminal": terminal_value,
                     "character_order": [list(x) for x in CHARACTERS],
                     "actor_order": list(ACTORS), "characters": [
                         {"character": i, "schema": records[i]["schema"],
                          "sha256": records[i]["sha256"]} for i in range(4)],
                     "p1_cache_passes": cache["cache_passes"], "p1_rows": P1_ROWS,
                     "global_relation_count": SCALAR_ORIGINS,
                     "future_active_orbit_bound": 504,
                     "ROOT_SCALAR_BATCH_CANDIDATE": True, "COMPLETE_DUAL_ORBITS": False,
                     "GRADE2_MEMBER": "NOT_DECIDED", "GRADE2_NONMEMBER": "NOT_DECIDED",
                     "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED",
                     "COFINAL_LIFT": "NOT_DECLARED", "FAKE": "NOT_DECLARED",
                     "IHARA": "NOT_DECLARED", "verified": False}
    terminal = {**terminal_body, "sha256": sha(canonical(terminal_body))}
    require(sealed_object(terminal), "terminal_embedded_seal")
    files.append(_write_json(out, "terminal.json", terminal))
    result_body = {"schema": SCHEMA + ".result", "launch_sha256": base["launch_sha256"],
                   "separator_manifest_sha256": separator["manifest_sha256"],
                   "p1_manifest_sha256": base["p1"]["manifest_sha256"],
                   "task712_manifest_sha256": [x["manifest_sha256"] for x in tables],
                   # Character zero is always the active root in the actual
                   # pinned preflight; this is the fixed coefficient receipt.
                   "global_relation_stream_sha256": records[0].get("relation_stream_sha256"),
                   "cache_passes": cache["cache_passes"], "instruction_passes": cache["instruction_passes"],
                   "rows": P1_ROWS, "characters": [x["sha256"] for x in records],
                   "terminal_sha256": terminal["sha256"], "files": list(files),
                   "claims": launch["claims"]}
    result = {**result_body, "sha256": sha(canonical(result_body))}
    require(sealed_object(result), "result_embedded_seal")
    files.append(_write_json(out, "result.json", result))
    roster = sorted([item["file"] for item in files] + ["manifest.json"])
    manifest_body = {"schema": SCHEMA + ".output-manifest", "terminal": terminal["terminal"],
                     "file_roster": roster, "files": sorted(files, key=lambda x: x["file"]),
                     "result": {"file": "result.json", "bytes": len(canonical(result)),
                                "sha256": sha(canonical(result))},
                     "candidate": True, "verified": False}
    manifest = {**manifest_body, "sha256": sha(canonical(manifest_body))}
    require(sealed_object(manifest), "manifest_embedded_seal")
    _write_json(out, "manifest.json", manifest)
    return {"status": "PASS", "terminal": terminal_value, "output": str(out),
            "rows": P1_ROWS, "p1_cache_passes": 1, "relation_origins": SCALAR_ORIGINS,
            "claims": launch["claims"], "verified": False}


def _expect_reject(action: Any, reason: str) -> None:
    try:
        action()
    except Exception:
        return
    raise RuntimeError(reason)


def selftest() -> dict[str, Any]:
    rng = np.random.default_rng(908)
    row = rng.integers(0, 3, size=P1_ROW_TRITS, dtype=np.uint8)
    packed = ARITH.pack_trits(row)
    vectors = [rng.integers(0, 3, size=SOURCE_WIDTH, dtype=np.uint8) for _ in range(20)]
    vectors = [v * (v != 0) for v in vectors]
    sparse_ok = []
    for offset in range(4):
        for vector in vectors[offset:offset + 4]:
            sparse_ok.append(sparse_projection(packed, offset * SLICE_BYTES,
                                               sparse_entries(vector)) ==
                             dense_projection(packed, offset * SLICE_BYTES, vector))
    require(all(sparse_ok), "selftest_sparse_dense")

    # The batch path is the vectorized five-value call; the reference path is
    # five independent scalar projections, so the two computations are not
    # the same expression evaluated twice.
    one_row = np.frombuffer(packed, dtype=np.uint8).reshape(1, P1_ROW_BYTES)
    chunk_projections = []
    for character in range(4):
        group = []
        for slot in range(5):
            indices = np.flatnonzero(vectors[5 * character + slot])
            group.append((np.asarray([i // 4 for i in indices], dtype=np.int64),
                          np.asarray([i % 4 for i in indices], dtype=np.int64),
                          np.asarray([int(vectors[5 * character + slot][i])
                                      for i in indices], dtype=np.int64)))
        chunk_projections.append(group)
    simultaneous = [vectorized_projection_chunk(one_row, character * SLICE_BYTES,
                                                 chunk_projections[character])[0].tolist()
                    for character in range(4)]
    separate = [[sparse_projection(packed, character * SLICE_BYTES,
                                   sparse_entries(vectors[5 * character + slot]))
                 for slot in range(5)] for character in range(4)]
    require(simultaneous == separate, "selftest_simultaneous")

    # Exercise the exact chunk kernel, including a short final chunk, against
    # independently dense-unpacked rows at all four character offsets.
    tiny_dense = rng.integers(0, 3, size=(3, P1_ROW_TRITS), dtype=np.uint8)
    tiny_rows = np.vstack([np.frombuffer(ARITH.pack_trits(item), dtype=np.uint8)
                           for item in tiny_dense])
    for character in range(4):
        got = vectorized_projection_chunk(tiny_rows, character * SLICE_BYTES,
                                           chunk_projections[character])
        expected = np.asarray([[dense_projection(bytes(tiny_rows[row]), character * SLICE_BYTES,
                                                  vectors[5 * character + slot])
                                for slot in range(5)] for row in range(3)], dtype=np.uint8)
        require(np.array_equal(got, expected), "selftest_vectorized_chunk_dense")

    # A real table parser plus the production transpose check rejects a
    # canonically resealed but non-transpose table.
    table_control = False
    with tempfile.TemporaryDirectory(prefix="d972-r07-task913-table-") as temp:
        table_root = Path(temp)
        forward_entries = [(0, 0, 1), (1, 0, 2), (3, 2, 1)]
        adjoint_entries = sorted((d, s, c) for s, d, c in forward_entries)

        def table_file(name: str, entries: list[tuple[int, int, int]]) -> tuple[Path, dict[str, Any]]:
            body = b"".join(ARITH._table_line(item) for item in entries)
            marker = {"body_bytes": len(body), "body_sha256": sha(body),
                      "count": len(entries), "eof": True}
            raw = body + canonical(marker); path = table_root / name
            path.write_bytes(raw)
            return path, {"bytes": len(raw), "sha256": sha(raw),
                          "source_width": SOURCE_WIDTH, "destination_width": SOURCE_WIDTH,
                          "entry_count": len(entries), "body_bytes": len(body),
                          "body_sha256": sha(body), "eof": True}

        _, forward_receipt = table_file("forward.jsonl", forward_entries)
        _, adjoint_receipt = table_file("adjoint.jsonl", adjoint_entries)
        forward = ARITH._read_table(table_root / "forward.jsonl", forward_receipt)
        adjoint = ARITH._read_table(table_root / "adjoint.jsonl", adjoint_receipt)
        check_table_transpose(forward, adjoint); table_control = True
        bad_entries = list(adjoint_entries); bad_entries[-1] = (2, 3, 2)
        _, bad_receipt = table_file("bad-adjoint.jsonl", bad_entries)
        bad_adjoint = ARITH._read_table(table_root / "bad-adjoint.jsonl", bad_receipt)
        _expect_reject(lambda: check_table_transpose(forward, bad_adjoint),
                       "selftest_task712_transpose_control")

    # Exercise the actual separator validator on a one-row temporary parent,
    # then mutate an internal sealed receipt.  All frozen constants are
    # restored before the real-path portion of this selftest continues.
    separator_control = False
    separator_names = ("SEPARATOR_RUN", "SEPARATOR_ATTEMPT", "SEPARATOR_HEAD",
                       "SEPARATOR_ARTIFACT", "SEPARATOR_ARTIFACT_NAME",
                       "SEPARATOR_ARCHIVE_BYTES", "SEPARATOR_ARCHIVE_SHA256",
                       "SEPARATOR_MANIFEST_SHA256", "SEPARATOR_PHYSICAL_BYTES",
                       "SEPARATOR_PHYSICAL_SHA256", "SEPARATOR_LAMBDA_BYTES",
                       "SEPARATOR_LAMBDA_SHA256", "SEPARATOR_TERMINAL_SHA256",
                       "SEPARATOR_RESULT_SHA256", "SEPARATOR_CHECKER_SHA256",
                       "SEPARATOR_GENERATION", "SEPARATOR_RANK", "SEPARATOR_STATE_HEAD")
    saved_separator = {name: globals()[name] for name in separator_names}
    try:
        zero_physical = bytes(PHYSICAL_PACKED_BYTES)
        state_head = "b" * 64
        manifest_body = {"generation": 1, "rank": 1,
                         "instructions": {"final_head": state_head},
                         "candidate_roster": ["physical.bin", "physical-p1-coeff.bin",
                                              "instructions.jsonl", "manifest.json", "HEAD"]}
        manifest_raw = canonical(manifest_body)
        internal_raw = {"terminal": b"terminal", "result": b"result", "checker": b"checker"}
        globals().update({
            "SEPARATOR_RUN": 1, "SEPARATOR_ATTEMPT": 1, "SEPARATOR_HEAD": "h" * 40,
            "SEPARATOR_ARTIFACT": 2, "SEPARATOR_ARTIFACT_NAME": "tiny-separator",
            "SEPARATOR_ARCHIVE_BYTES": 3, "SEPARATOR_ARCHIVE_SHA256": "sha256:" + "a" * 64,
            "SEPARATOR_MANIFEST_SHA256": sha(manifest_raw),
            "SEPARATOR_PHYSICAL_BYTES": len(zero_physical),
            "SEPARATOR_PHYSICAL_SHA256": sha(zero_physical),
            "SEPARATOR_LAMBDA_BYTES": len(zero_physical),
            "SEPARATOR_LAMBDA_SHA256": sha(zero_physical),
            "SEPARATOR_TERMINAL_SHA256": sha(internal_raw["terminal"]),
            "SEPARATOR_RESULT_SHA256": sha(internal_raw["result"]),
            "SEPARATOR_CHECKER_SHA256": sha(internal_raw["checker"]),
            "SEPARATOR_GENERATION": 1, "SEPARATOR_RANK": 1,
            "SEPARATOR_STATE_HEAD": state_head})
        with tempfile.TemporaryDirectory(prefix="d972-r07-task913-separator-") as temp:
            root = Path(temp); (root / "state").mkdir(); (root / "output").mkdir()
            (root / "manifest.json").write_bytes(manifest_raw)
            (root / "state" / "physical.bin").write_bytes(zero_physical)
            (root / "output" / "lambda.bin").write_bytes(zero_physical)
            for name, raw in internal_raw.items(): (root / "output" / (name + ".bin")).write_bytes(raw)
            parent = {"schema": SCHEMA + ".separator-parent.v1", "root": str(root),
                      "artifact": {"run": 1, "attempt": 1, "head": "h" * 40, "id": 2,
                                   "name": "tiny-separator", "bytes": 3,
                                   "sha256": "sha256:" + "a" * 64},
                      "manifest": {"file": "manifest.json", "bytes": len(manifest_raw),
                                   "sha256": sha(manifest_raw)},
                      "physical": {"file": "state/physical.bin", "bytes": len(zero_physical),
                                   "sha256": sha(zero_physical), "rows": 1},
                      "lambda": {"file": "output/lambda.bin", "bytes": len(zero_physical),
                                 "sha256": sha(zero_physical)},
                      "internal": {key: {"file": "output/" + key + ".bin", "bytes": len(raw),
                                          "sha256": sha(raw)} for key, raw in internal_raw.items()}}
            validate_separator(parent); separator_control = True
            bad = json.loads(json.dumps(parent)); bad["internal"]["terminal"]["sha256"] = "0" * 64
            _expect_reject(lambda: validate_separator(bad), "selftest_separator_mutation_control")
    finally:
        globals().update(saved_separator)

    # P1's manifest and cache readers are exercised with one real packed row;
    # both a descriptor digest mutation and a truncated cache are rejected.
    p1_control = False
    p1_names = ("P1_RUN", "P1_ATTEMPT", "P1_HEAD", "P1_ARTIFACT", "P1_ARTIFACT_NAME",
                "P1_ARCHIVE_BYTES", "P1_ARCHIVE_SHA256", "P1_MANIFEST_BYTES",
                "P1_MANIFEST_SHA256", "P1_CACHE_BYTES", "P1_CACHE_SHA256",
                "P1_INSTRUCTION_BYTES", "P1_INSTRUCTION_SHA256", "P1_ROWS")
    saved_p1 = {name: globals()[name] for name in p1_names}
    try:
        cache_raw = bytes(P1_ROW_BYTES); instruction_raw = b"x"
        ancestry = "c" * 64
        globals().update({"P1_RUN": 1, "P1_ATTEMPT": 1, "P1_HEAD": "p" * 40,
                          "P1_ARTIFACT": 2, "P1_ARTIFACT_NAME": "tiny-p1",
                          "P1_ARCHIVE_BYTES": 3, "P1_ARCHIVE_SHA256": "sha256:" + "d" * 64,
                          "P1_CACHE_BYTES": len(cache_raw), "P1_CACHE_SHA256": sha(cache_raw),
                          "P1_INSTRUCTION_BYTES": len(instruction_raw),
                          "P1_INSTRUCTION_SHA256": sha(instruction_raw), "P1_ROWS": 1})
        manifest = {"schema": "d972.r07.canonical-p1-dag-degree2-lift.v8",
                    "status": "CANONICAL_P1_DAG_DEGREE2_LIFT_CANDIDATE", "rows": 1,
                    "row_trits": P1_ROW_TRITS, "row_bytes": P1_ROW_BYTES,
                    "global_order": [0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059],
                    "actor_order": list(ACTORS), "character_order": [list(x) for x in CHARACTERS],
                    "independent_checker": False,
                    "A0": False, "COMMON": False, "COFINAL": False, "FAKE": False,
                    "IHARA": False, "verified": False, "ancestry_sha256": ancestry,
                    "cache": {"path": "degree2.cache.bin", "rows": 1,
                              "bytes": len(cache_raw), "sha256": sha(cache_raw),
                              "final_lf": False, "eof": True},
                    "instruction": {"path": "instructions.jsonl", "rows": 1,
                                    "bytes": len(instruction_raw), "sha256": sha(instruction_raw),
                                    "final_lf": True, "eof": True, "final_head": ancestry}}
        manifest_raw = canonical(manifest)
        globals()["P1_MANIFEST_BYTES"] = len(manifest_raw)
        globals()["P1_MANIFEST_SHA256"] = sha(manifest_raw)
        with tempfile.TemporaryDirectory(prefix="d972-r07-task913-p1-") as temp:
            root = Path(temp); (root / "manifest.json").write_bytes(manifest_raw)
            (root / "degree2.cache.bin").write_bytes(cache_raw)
            (root / "instructions.jsonl").write_bytes(instruction_raw)
            parent = {"root": str(root), "manifest": {"file": "manifest.json",
                       "bytes": len(manifest_raw), "sha256": sha(manifest_raw)},
                      "files": [{"file": "degree2.cache.bin", "bytes": len(cache_raw),
                                 "sha256": sha(cache_raw)},
                                {"file": "instructions.jsonl", "bytes": len(instruction_raw),
                                 "sha256": sha(instruction_raw)}],
                      "run": 1, "attempt": 1, "head": "p" * 40, "artifact": 2,
                      "artifact_name": "tiny-p1", "archive_bytes": 3,
                      "archive_sha256": "sha256:" + "d" * 64}
            checked = validate_p1(parent)
            tiny_vectors = [np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)]
            tiny_vectors[0][0] = 1
            p1_batch(checked, [tiny_vectors, [np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)],
                               [np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)],
                               [np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)]])
            bad_manifest = json.loads(json.dumps(parent)); bad_manifest["manifest"]["sha256"] = "0" * 64
            _expect_reject(lambda: validate_p1(bad_manifest), "selftest_p1_manifest_control")
            (root / "degree2.cache.bin").write_bytes(cache_raw[:-1])
            _expect_reject(lambda: p1_batch(checked, [tiny_vectors,
                                                       [np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)],
                                                       [np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)],
                                                       [np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)]]),
                           "selftest_p1_truncation_control")
        p1_control = True
    finally:
        globals().update(saved_p1)

    # Build a tiny but genuine prepare + two-block parent.  The production
    # blockwise evaluator is compared with an independently flattened fold,
    # including four distinguishable actor slots and local/global offsets.
    tiny_accumulator_control = False
    accumulator_names = ("P1_ROWS", "OLD_RANKS", "NEW_RANKS", "ORIGIN_RANGES",
                         "TASK554_ORIGINS", "SCALAR_ORIGINS", "TASK554_BODY_DIGESTS")
    saved_accumulator = {name: globals()[name] for name in accumulator_names}
    try:
        globals().update({"P1_ROWS": 3, "OLD_RANKS": (1, 0, 0, 0),
                          "NEW_RANKS": (0, 1, 1, 0),
                          "ORIGIN_RANGES": ((0, 48), (48, 92), (92, 136), (136, 180)),
                          "TASK554_ORIGINS": 180, "SCALAR_ORIGINS": 56})

        def tiny_old(character: int, rank: int, start: int) -> dict[str, Any]:
            seed_terms = [[[0, 1]] for _ in range(44)] if rank else [[] for _ in range(44)]
            actor_terms = [[[[0, 1 if slot % 2 == 0 else 2]] for slot in range(4)]] if rank else []
            nodes = [{"pivot": 0, "scale": 1, "reductions": [[0, 1]]}] if rank else []
            record = {"rank": rank, "character": list(CHARACTERS[character]),
                      "attempts": 44 + 4 * rank, "actor_order": list(ACTORS),
                      "queue_exhausted": True, "seed_reductions": seed_terms,
                      "dag_nodes": nodes, "actor_transitions": actor_terms}
            return {"character_index": character, "character": list(CHARACTERS[character]),
                    "rank": rank, "record": record, "defect_origin_range": [start, start + 44 + 4 * rank]}

        old_blocks = []; cursor = 0
        for character, rank in enumerate(OLD_RANKS):
            old_blocks.append(tiny_old(character, rank, cursor)); cursor += 44 + 4 * rank
        prepare = {"schema": "d972.r07.a0.first-rung-grade1.v3.state", "phase": "prepare",
                   "parent_sha256": None, "old_blocks": old_blocks,
                   "defect_origins": [0] * TASK554_ORIGINS, "packets": [[], [], [], []]}
        prepare_raw = canonical(prepare); prepare_hash = sha(prepare_raw)
        block_bodies = []
        for character, rank in enumerate(NEW_RANKS):
            if rank:
                reductions = [[[0, 1 if index % 2 == 0 else 2]] for index in range(TASK554_ORIGINS)]
                transitions = [[[[0, 1]], [[0, 2]], [[0, 1]], [[0, 2]]]]
                nodes = [{"pivot": 0, "lead": 0, "scale": 1, "reductions": [[0, 1]]}]
                leads = [0]
            else:
                reductions = [[] for _ in range(TASK554_ORIGINS)]; transitions = []
                nodes = []; leads = []
            block_bodies.append({"schema": "d972.r07.a0.first-rung-grade1.v3.state", "phase": "block",
                                 "parent_sha256": prepare_hash, "character_index": character,
                                 "character": list(CHARACTERS[character]), "rank": rank,
                                 "origin_count": TASK554_ORIGINS, "attempts": TASK554_ORIGINS + 4 * rank,
                                 "actor_order": list(ACTORS), "queue_exhausted": True,
                                 "origin_reductions": reductions, "actor_transitions": transitions,
                                 "dag_nodes": nodes, "pivot_leads": leads,
                                 "dag_sha256": sha(canonical(nodes))})
        body_values = [prepare] + block_bodies
        body_raws = [canonical(value) for value in body_values]
        body_hashes = tuple(sha(raw) for raw in body_raws)
        globals()["TASK554_BODY_DIGESTS"] = body_hashes

        def write_state(root: Path, index: int, body_raw: bytes, body_hash: str) -> dict[str, Any]:
            stem = "prepare" if index == -1 else "block-" + str(index)
            head_value = {"body_sha256": body_hash,
                          "parent_sha256": None if index == -1 else body_hashes[0],
                          "schema": "d972.r07.a0.first-rung-grade1.v3.state.head", "stem": stem}
            head_raw = canonical(head_value); (root / (stem + ".HEAD")).write_bytes(head_raw)
            body_name = stem + "." + body_hash + ".json"; (root / body_name).write_bytes(body_raw)
            head_desc = {"file": stem + ".HEAD", "bytes": len(head_raw), "sha256": sha(head_raw)}
            body_desc = {"file": body_name, "bytes": len(body_raw), "sha256": body_hash}
            return {"root": str(root), "head": head_desc, "body": body_desc,
                    "files": sorted([head_desc, body_desc], key=lambda item: item["file"])}

        with tempfile.TemporaryDirectory(prefix="d972-r07-task913-accumulator-") as temp:
            root = Path(temp)
            descriptors = [write_state(root, -1, body_raws[0], body_hashes[0])]
            descriptors.extend(write_state(root, index, body_raws[index + 1], body_hashes[index + 1])
                               for index in range(4))
            values = [np.asarray(item, dtype=np.uint8) for item in (
                [1, 2, 0], [0, 1, 2], [2, 0, 1], [1, 1, 0], [2, 2, 1])]
            direct = [index % 3 for index in range(44)]
            got = accumulate_scalars({"prepare": descriptors[0], "blocks": descriptors[1:]},
                                     0, direct, values[1:], values)
            expected_seeds = np.asarray(direct, dtype=np.uint8)
            expected_actors = np.column_stack(values[1:]).astype(np.uint8, copy=True)

            def direct_sub(accumulator: int, expression: list[list[int]], bound: int,
                           offset: int) -> int:
                _expression(expression, bound, "selftest_direct_relation")
                return (int(accumulator) - sum(int(coef) * int(values[0][offset + int(index)])
                                               for index, coef in expression)) % 3

            old_offsets = [0, 1, 1, 1]; new_offsets = [1, 1, 2, 3]
            for seed in range(44):
                for source, old in enumerate(old_blocks):
                    expected_seeds[seed] = direct_sub(expected_seeds[seed],
                        old["record"]["seed_reductions"][seed], OLD_RANKS[source], old_offsets[source])
            for source, old in enumerate(old_blocks):
                for pivot in range(OLD_RANKS[source]):
                    global_row = old_offsets[source] + pivot
                    for slot in range(4):
                        expected_actors[global_row, slot] = direct_sub(
                            expected_actors[global_row, slot], old["record"]["actor_transitions"][pivot][slot],
                            OLD_RANKS[source], old_offsets[source])
            for target, body in enumerate(block_bodies):
                rank = NEW_RANKS[target]; offset = new_offsets[target]
                for seed in range(44):
                    for source in range(4):
                        expected_seeds[seed] = direct_sub(
                            expected_seeds[seed], body["origin_reductions"][ORIGIN_RANGES[source][0] + seed],
                            rank, offset)
                for source, old in enumerate(old_blocks):
                    global_row_base = old_offsets[source]
                    for pivot in range(OLD_RANKS[source]):
                        for slot in range(4):
                            origin = ORIGIN_RANGES[source][0] + 44 + 4 * pivot + slot
                            expected_actors[global_row_base + pivot, slot] = direct_sub(
                                expected_actors[global_row_base + pivot, slot], body["origin_reductions"][origin],
                                rank, offset)
                for local, row_value in enumerate(body["actor_transitions"]):
                    for slot in range(4):
                        expected_actors[offset + local, slot] = direct_sub(
                            expected_actors[offset + local, slot], row_value[slot], rank, offset)
            require(np.array_equal(got["seed_values"], expected_seeds) and
                    np.array_equal(got["actor_values"], expected_actors) and
                    got["accumulator_count"] == 56, "selftest_two_block_accumulator")
            tiny_accumulator_control = True
    finally:
        globals().update(saved_accumulator)

    # The real scalar scan is bounded by the 32,280 records even though its
    # values are tiny.  Three runs prove seed-first, actor-first and EOF paths.
    fake = {"schema": ARITH.LIVE_SCHEMA + ".RawDual", "separator_generation": 0,
            "separator_s_head_sha256": "0" * 64, "lambda_sha256": "0" * 64,
            "character": 0, "B_adj_table_identity": "B:x", "word_node": {"kind": "root"},
            "actor_table_identities_along_w": [], "raw_q_packed_sha256": "0" * 64,
            "raw_q_packed_offset": 0, "raw_q_packed_length": SOURCE_WIDTH // 4,
            "raw_predecessor_sha256": None}
    fake["sha256"] = sha(canonical({k: v for k, v in fake.items() if k != "sha256"}))
    scan_values = [np.zeros(P1_ROWS, dtype=np.uint8) for _ in range(5)]
    scan_cache = {"manifest_sha256": "2" * 64, "values": scan_values}
    eof_accumulator = {"seed_values": np.zeros(44, dtype=np.uint8),
                       "actor_values": np.zeros((P1_ROWS, 4), dtype=np.uint8),
                       "relation_sha256": "3" * 64}
    eof_record = _scan_accumulated(fake, eof_accumulator, {"manifest_sha256": "2" * 64,
                                                            "values": scan_values})
    require(eof_record["schema"].endswith("ScalarEOF") and
            eof_record["origins"] == SCALAR_ORIGINS and sealed_object(eof_record),
            "selftest_full_scalar_eof")
    seed_accumulator = {"seed_values": np.zeros(44, dtype=np.uint8),
                        "actor_values": np.zeros((P1_ROWS, 4), dtype=np.uint8),
                        "relation_sha256": "3" * 64}
    seed_accumulator["seed_values"][0] = 1
    seed_record = _scan_accumulated(fake, seed_accumulator, scan_cache)
    require(seed_record["schema"].endswith("Violation") and seed_record["origin_id"] == 0 and
            seed_record["origin_kind"] == "seed" and seed_record["seed"] == 0,
            "selftest_seed_first")
    actor_accumulator = {"seed_values": np.zeros(44, dtype=np.uint8),
                         "actor_values": np.zeros((P1_ROWS, 4), dtype=np.uint8),
                         "relation_sha256": "3" * 64}
    actor_accumulator["actor_values"][0, 0] = 1
    actor_record = _scan_accumulated(fake, actor_accumulator, scan_cache)
    require(actor_record["schema"].endswith("Violation") and actor_record["origin_id"] == 44 and
            actor_record["origin_kind"] == "actor" and actor_record["basis_i"] == 0 and
            actor_record["actor"] == ACTORS[0], "selftest_actor_first")

    # Root-zero records go through the actual character constructor and the
    # shared terminal classifier, rather than a telemetry boolean.
    zero_table = {"identity": {"adjoint:B": "B:tiny"}}
    zero_separator = {"generation": 0, "manifest": {"state_head": "0" * 64},
                      "lambda_sha256": "0" * 64}
    zero_vectors = [[np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)] for _ in range(4)]
    zero_records = [_scalar_result(character, zero_table, zero_vectors[character], {}, {},
                                   zero_separator, []) for character in range(4)]
    require(all(item["schema"].endswith("RootZero") for item in zero_records),
            "selftest_zero_root")
    require(terminal_kind(zero_records) == "AllFourRootEOF", "selftest_all_four_root_eof")

    # Task554 preserves insertion order.  Syntax validation therefore accepts
    # unsorted, unique terms and rejects only malformed/duplicate entries.
    _expression([[2, 2], [0, 1]], 3, "selftest_relation_unsorted")
    for bad_expression, label in (
            ([[2, 2], [2, 1]], "selftest_relation_duplicate"),
            ([[3, 1]], "selftest_relation_out_of_range"),
            ([[0, 0]], "selftest_relation_coefficient")):
        _expect_reject(lambda bad=bad_expression: _expression(
            bad, 3, "selftest_relation_invalid"), label)

    # The exact Task554 body receipt still authenticates term order.  A
    # semantically equivalent reordering is rejected at that boundary, rather
    # than by the expression syntax validator above.
    relation_order_control = False
    with tempfile.TemporaryDirectory(prefix="d972-r07-task917-body-") as temp:
        body_path = Path(temp) / "task554-body.json"
        body = {"schema": "task554-order-fixture", "origin_reductions": [[2, 2], [0, 1]]}
        body_raw = canonical(body); body_sha = sha(body_raw)
        body_path.write_bytes(body_raw)
        read_json_stream(body_path, len(body_raw), body_sha)
        reordered_raw = canonical({"schema": body["schema"],
                                   "origin_reductions": [[0, 1], [2, 2]]})
        require(len(reordered_raw) == len(body_raw), "selftest_relation_order_fixture_size")
        body_path.write_bytes(reordered_raw)
        _expect_reject(lambda: read_json_stream(body_path, len(body_raw), body_sha),
                       "selftest_task554_body_order_digest_control")
        relation_order_control = True

    # A coherently resealed child/prefix object is still rejected by the
    # exact expected-object comparison used by the producer's own seals.
    sealed_expected = {"schema": SCHEMA + ".fixture", "q_child_sha256": sha(b"q"),
                       "scalar_prefix_digest": sha(b"prefix")}
    sealed_expected["sha256"] = sha(canonical(sealed_expected))
    require(sealed_object(sealed_expected), "selftest_fixture_seal")
    resealed = dict(sealed_expected); resealed["q_child_sha256"] = sha(b"changed")
    resealed["sha256"] = sha(canonical({k: v for k, v in resealed.items() if k != "sha256"}))
    _expect_reject(lambda: require(sealed_object(resealed) and resealed == sealed_expected,
                                   "selftest_resealed_expected"),
                   "selftest_resealed_control")

    return {"schema": SCHEMA + ".selftest", "status": "PASS",
            "sparse_offsets": 4, "simultaneous_values": 20,
            "vectorized_chunk_dense_crosscheck": True,
            "offset_four_slot_control": tiny_accumulator_control,
            "two_block_accumulator": tiny_accumulator_control,
            "full_scalar_eof_32280": True, "seed_first_violation": 0,
            "actor_first_violation": "basis_i/actor", "all_four_root_eof": True,
            "zero_root": True, "separator_mutation_rejected": separator_control,
            "task712_transpose_mutation_rejected": table_control,
            "p1_truncation_digest_mutation_rejected": p1_control,
            "task554_relation_order_mutation_rejected": relation_order_control,
            "result_q_child_scalar_prefix_resealing_rejected": True,
            "dense_all_row_matrix": False, "p1_cache_passes": 1, "verified": False}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    group = result.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true")
    group.add_argument("--run-launch", type=Path)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.selftest:
            print(json.dumps(selftest(), sort_keys=True)); return 0
        print(json.dumps(run_actual(args.run_launch), sort_keys=True)); return 0
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc), "verified": False},
                         sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
