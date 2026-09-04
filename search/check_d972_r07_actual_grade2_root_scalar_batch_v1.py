#!/usr/bin/env python3
"""Independent checker for the R07 actual root-scalar batch.

This file intentionally has no import of the producer.  It owns its cache
projection, parent checks, relation walk, scalar replay, and output-roster
comparison; only the already audited checker-v15 arithmetic is reused.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable

import numpy as np

try:
    import check_d972_r07_targeted_grade2_owner_generated_join_v15 as ARITH
except ModuleNotFoundError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import check_d972_r07_targeted_grade2_owner_generated_join_v15 as ARITH


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972.r07.actual-grade2.root-scalar-batch.v1"
ARITH_PATH = PROJECT_ROOT / "search" / "check_d972_r07_targeted_grade2_owner_generated_join_v15.py"
ARITH_SHA256 = "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662"
PRODUCER_ARITH_PATH = PROJECT_ROOT / "search" / "d972_r07_targeted_grade2_owner_generated_join_v15.py"
PRODUCER_ARITH_SHA256 = "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632"
P1_RUN = 33851744070; P1_ATTEMPT = 1
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
P1_ROWS = 8059; P1_ROW_TRITS = 145152; P1_ROW_BYTES = 36288
SOURCE_WIDTH = 36288; SLICE_BYTES = 9072
PHYSICAL_WIDTH = 48384; PHYSICAL_PACKED_BYTES = 12096
ACTORS = (1, -1, 2, -2); CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
OLD_RANKS = (505, 503, 503, 503); NEW_RANKS = (1509, 1512, 1512, 1512)
ORIGIN_RANGES = ((0, 2064), (2064, 4120), (4120, 6176), (6176, 8232))
SCALAR_ORIGINS = 32280; TASK554_ORIGINS = 8232; POW3 = (1, 3, 9, 27)

SEPARATOR_RUN = 33891714539; SEPARATOR_ATTEMPT = 1
SEPARATOR_HEAD = "7b7b9de20faaa3b8f26e331bb738b374f6f5708c"
SEPARATOR_ARTIFACT = 9944214057
SEPARATOR_ARTIFACT_NAME = "d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1"
SEPARATOR_ARCHIVE_BYTES = 107195261
SEPARATOR_ARCHIVE_SHA256 = "sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017"
SEPARATOR_MANIFEST_SHA256 = "d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b"
SEPARATOR_PHYSICAL_BYTES = 16377984
SEPARATOR_PHYSICAL_SHA256 = "1246ae0c23c7dcbfc2a1c2f73075f38968a4ab7b2e5c8fc006f0f8aafae2d57e"
SEPARATOR_LAMBDA_SHA256 = "7522ee1f00f386b229ea46bc0f2b9fdf2854cf03c262f40a2f60dd9ced0102ed"
SEPARATOR_TERMINAL_SHA256 = "098d5961cddc187d01c08e22f9f40ce55a7a02e8a1b1d088eca8c804957098cf"
SEPARATOR_RESULT_SHA256 = "d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968"
SEPARATOR_CHECKER_SHA256 = "2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433"
SEPARATOR_GENERATION = 8059; SEPARATOR_RANK = 1354
SEPARATOR_STATE_HEAD = "69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88"

TASK554_RUN = 33677346616; TASK554_ATTEMPT = 1
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
TASK712_PARENT = {"run_id": 33814194630, "run_attempt": 1, "artifact_id": 9915928157,
                  "artifact_digest": "sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858"}
EXPECTED_ROOT = {
    0: (2742, 3, 2, "af62027aa99fbd1a4b7b53c6b380b4e7fa7403915ea91f9d51d7cb2198c7e053"),
    1: (0, None, None, "8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838"),
    2: (0, None, None, "8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838"),
    3: (0, None, None, "8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838"),
}
EXPECTED_CHILD = {
    0: ("aa54bbed30791f3f771c5fb8d74e38329564101cbcd805db20e1e232595e7033",
        "1b98282910ed00d253cad00cbc389b9c85c6b84be9b8da0418ece4f8b0218cd8",
        "f98650b321a16e846539698d98710a544fd1953656afcaecbee995523f0def2b",
        "2245611c3efcef71758e281950ca4b23ba96d0991880cdb92ecafa0fac7aa8b4"),
    1: ("8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838",) * 4,
    2: ("8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838",) * 4,
    3: ("8f23754a0b5b965d1b0e2e5a9b043586911a3f8283a36412c739dad14c500838",) * 4,
}


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sealed_object(value: Any) -> bool:
    if not isinstance(value, dict) or not isinstance(value.get("sha256"), str):
        return False
    body = dict(value); seal = body.pop("sha256")
    return seal == sha(canonical(body))


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def safe_path(root: Path, name: str) -> Path:
    require(isinstance(name, str) and name and not Path(name).is_absolute(), "relative_path")
    path = (root / name).resolve(); require(root.resolve() in path.parents, "path_escape")
    require(not path.is_symlink() and path.is_file(), "unsafe_file")
    return path


def file_hash(path: Path, expected: int | None = None, cap: int = 1 << 30) -> tuple[int, str]:
    size = path.stat().st_size; require(size <= cap, "file_cap")
    if expected is not None: require(size == expected, "file_size")
    h = hashlib.sha256(); total = 0
    with path.open("rb") as stream:
        while True:
            block = stream.read(1 << 20)
            if not block: break
            h.update(block); total += len(block)
    require(total == size, "file_read_size"); return size, h.hexdigest()


def read_json(path: Path, expected_size: int | None = None,
              expected_hash: str | None = None, cap: int = 1 << 28) -> tuple[Any, bytes]:
    size, actual = file_hash(path, expected_size, cap); raw = path.read_bytes()
    require(len(raw) == size and (expected_hash is None or actual == expected_hash), "json_digest")
    value = json.loads(raw.decode("ascii")); require(canonical(value) == raw, "json_canonical")
    return value, raw


def read_json_stream(path: Path, expected_size: int, expected_hash: str,
                     cap: int = 1 << 28) -> Any:
    """Authenticate a large fixed body without a duplicate raw-byte copy."""
    size, actual = file_hash(path, expected_size, cap)
    require(size == expected_size and actual == expected_hash, "checker_json_stream_digest")
    try:
        with path.open("rb") as stream:
            value = json.load(stream)
    except (OSError, UnicodeError, ValueError) as exc:
        raise RuntimeError("checker_json_stream_decode") from exc
    require(isinstance(value, dict), "checker_json_stream_object")
    return value


def receipt(root: Path, item: dict[str, Any], cap: int = 1 << 30) -> bytes:
    require(isinstance(item, dict) and set(item) == {"file", "bytes", "sha256"}, "receipt_shape")
    path = safe_path(root, item["file"]); size, actual = file_hash(path, item["bytes"], cap)
    require(actual == item["sha256"], "receipt_digest"); return path.read_bytes()


def verify_source() -> None:
    _, actual = file_hash(ARITH_PATH); require(actual == ARITH_SHA256, "checker_source_pin")


def sparse_projection(packed: bytes, offset: int, entries: Iterable[tuple[int, int]]) -> int:
    total = 0
    for index, coefficient in entries:
        require(0 <= index < SOURCE_WIDTH and coefficient in (1, 2), "sparse_entry")
        total += coefficient * ((packed[offset + index // 4] // POW3[index % 4]) % 3)
    return total % 3


def check_table_transpose(forward: Iterable[Iterable[int]],
                          adjoint: Iterable[Iterable[int]]) -> None:
    """Independent table-level transpose check used after envelope parsing."""
    expected = sorted((int(destination), int(source), int(coefficient))
                      for source, destination, coefficient in forward)
    require(list(adjoint) == expected, "checker_task712_transpose")


def vectorized_projection_chunk(packed_rows: np.ndarray, byte_offset: int,
                                projections: list[tuple[np.ndarray, np.ndarray, np.ndarray]]) -> np.ndarray:
    """Independent bounded implementation of the sparse packed projection."""
    rows = np.asarray(packed_rows, dtype=np.uint8)
    require(rows.ndim == 2 and rows.shape[1] == P1_ROW_BYTES and
            0 <= byte_offset <= P1_ROW_BYTES - SLICE_BYTES, "checker_projection_chunk_shape")
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
    """Digest the fixed coefficient source without serializing every term."""
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


def _expr(value: Any, bound: int, reason: str) -> None:
    require(isinstance(value, list), reason + ":list"); previous = -1
    for pair in value:
        require(isinstance(pair, list) and len(pair) == 2 and plain_int(pair[0]) and
                plain_int(pair[1]) and previous < pair[0] < bound and pair[1] in (1, 2), reason)
        previous = pair[0]


def _body(value: Any, index: int) -> None:
    require(isinstance(value, dict), "checker_task554_body")
    if index == -1:
        olds = value.get("old_blocks"); origins = value.get("defect_origins")
        require(isinstance(olds, list) and len(olds) == 4 and isinstance(origins, list) and
                len(origins) == TASK554_ORIGINS and isinstance(value.get("packets"), list) and
                len(value["packets"]) == 4, "checker_prepare_shape")
        cursor = 0
        for character, old in enumerate(olds):
            rank = OLD_RANKS[character]; record = old.get("record")
            require(old.get("character_index") == character and
                    old.get("character") == list(CHARACTERS[character]) and old.get("rank") == rank and
                    isinstance(record, dict) and record.get("character") == list(CHARACTERS[character]) and
                    record.get("rank") == rank and record.get("attempts") == 44 + 4 * rank and
                    record.get("actor_order") == list(ACTORS) and record.get("queue_exhausted") is True and
                    len(record.get("seed_reductions", [])) == 44 and len(record.get("dag_nodes", [])) == rank and
                    len(record.get("actor_transitions", [])) == rank, "checker_old_shape")
            for expression in record["seed_reductions"]: _expr(expression, rank, "checker_seed")
            for row in record["actor_transitions"]:
                require(isinstance(row, list) and len(row) == 4, "checker_old_actor")
                for expression in row: _expr(expression, rank, "checker_actor")
            for pivot, node in enumerate(record["dag_nodes"]):
                require(node.get("pivot") == pivot and node.get("scale") in (1, 2), "checker_old_node")
                _expr(node.get("reductions"), rank, "checker_old_reduction")
            require(old.get("defect_origin_range") == list(ORIGIN_RANGES[character]) and
                    ORIGIN_RANGES[character][0] == cursor, "checker_origin_range")
            cursor += 44 + 4 * rank
        require(cursor == len(origins), "checker_origin_count")
    else:
        rank = NEW_RANKS[index]
        require(value.get("phase") == "block" and value.get("character_index") == index and
                value.get("character") == list(CHARACTERS[index]) and value.get("rank") == rank and
                value.get("origin_count") == TASK554_ORIGINS and value.get("attempts") == TASK554_ORIGINS + 4 * rank and
                value.get("actor_order") == list(ACTORS) and value.get("queue_exhausted") is True,
                "checker_new_metadata")
        reductions = value.get("origin_reductions"); transitions = value.get("actor_transitions")
        nodes = value.get("dag_nodes"); leads = value.get("pivot_leads")
        require(isinstance(reductions, list) and len(reductions) == TASK554_ORIGINS and
                isinstance(transitions, list) and len(transitions) == rank and
                isinstance(nodes, list) and len(nodes) == rank and isinstance(leads, list) and
                len(leads) == rank and len(set(leads)) == rank, "checker_new_lists")
        for expression in reductions: _expr(expression, rank, "checker_origin_reduction")
        for row in transitions:
            require(isinstance(row, list) and len(row) == 4, "checker_new_actor")
            for expression in row: _expr(expression, rank, "checker_transition")
        for pivot, node in enumerate(nodes):
            require(node.get("pivot") == pivot and node.get("lead") == leads[pivot] and
                    node.get("scale") in (1, 2), "checker_new_node")
            _expr(node.get("reductions"), rank, "checker_new_reduction")
        require(value.get("dag_sha256") == sha(canonical(nodes)), "checker_dag_digest")


def state_descriptor(value: Any, index: int) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) == {"root", "head", "body", "files"},
            "checker_state_descriptor")
    root = Path(value["root"]).absolute(); require(root.is_dir(), "checker_state_root")
    stem = "prepare" if index == -1 else "block-" + str(index)
    body_hash = TASK554_BODY_DIGESTS[0 if index == -1 else index + 1]
    head = value["head"]; body = value["body"]
    require(body["file"] == stem + "." + body_hash + ".json" and body["sha256"] == body_hash and
            isinstance(value["files"], list) and sorted(value["files"], key=lambda x: x["file"]) ==
            sorted([head, body], key=lambda x: x["file"]), "checker_body_roster")
    hvalue, _ = read_json(safe_path(root, head["file"]), head["bytes"], head["sha256"], 1 << 20)
    bpath = safe_path(root, body["file"])
    bvalue = read_json_stream(bpath, body["bytes"], body["sha256"], 1 << 28)
    require(hvalue == {
        "body_sha256": body_hash, "parent_sha256": None if index == -1 else TASK554_BODY_DIGESTS[0],
        "schema": "d972.r07.a0.first-rung-grade1.v3.state.head", "stem": stem},
        "checker_head_join")
    require(bvalue.get("schema") == "d972.r07.a0.first-rung-grade1.v3.state" and
            bvalue.get("phase") == ("prepare" if index == -1 else "block") and
            bvalue.get("parent_sha256") == (None if index == -1 else TASK554_BODY_DIGESTS[0]),
            "checker_body_join")
    _body(bvalue, index)
    return {"root": root, "body": bvalue, "body_sha256": body_hash}


def validate_task554(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) ==
            {"schema", "source_run", "source_attempt", "source_head", "artifacts", "prepare", "blocks"} and
            value["schema"] == SCHEMA + ".task554-parent.v1" and value["source_run"] == TASK554_RUN and
            value["source_attempt"] == TASK554_ATTEMPT and value["source_head"] == TASK554_HEAD and
            value["artifacts"] == [{"id": x[0], "name": x[1], "bytes": x[2], "sha256": x[3]}
                                    for x in TASK554_ARTIFACTS] and len(value["blocks"]) == 4,
            "checker_task554_parent")
    for item in [value["prepare"], *value["blocks"]]:
        require(isinstance(item, dict) and set(item) == {"root", "head", "body", "files"},
                "checker_task554_descriptor")
    return value


def validate_p1(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) ==
            {"root", "manifest", "files", "run", "attempt", "head", "artifact", "artifact_name",
             "archive_bytes", "archive_sha256"} and value["run"] == P1_RUN and
            value["attempt"] == P1_ATTEMPT and value["head"] == P1_HEAD and
            value["artifact"] == P1_ARTIFACT and value["artifact_name"] == P1_ARTIFACT_NAME and
            value["archive_bytes"] == P1_ARCHIVE_BYTES and value["archive_sha256"] == P1_ARCHIVE_SHA256,
            "checker_p1_parent")
    root = Path(value["root"]).absolute(); require(root.is_dir(), "checker_p1_root")
    manifest, raw = read_json(safe_path(root, value["manifest"]["file"]), P1_MANIFEST_BYTES,
                              P1_MANIFEST_SHA256, 1 << 20)
    require(value["manifest"] == {"file": "manifest.json", "bytes": P1_MANIFEST_BYTES,
                                   "sha256": P1_MANIFEST_SHA256} and
            manifest.get("schema") == "d972.r07.canonical-p1-dag-degree2-lift.v8" and
            manifest.get("status") == "CANONICAL_P1_DAG_DEGREE2_LIFT_CANDIDATE" and
            manifest.get("rows") == P1_ROWS and manifest.get("row_trits") == P1_ROW_TRITS and
            manifest.get("row_bytes") == P1_ROW_BYTES and
            manifest.get("global_order") == [0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059] and
            manifest.get("actor_order") == list(ACTORS) and
            manifest.get("character_order") == [list(x) for x in CHARACTERS] and
            manifest.get("independent_checker") is False and
            all(manifest.get(k) is False for k in ("A0", "COMMON", "COFINAL", "FAKE", "IHARA", "verified")),
            "checker_p1_manifest")
    cache = manifest.get("cache"); instruction = manifest.get("instruction")
    require(cache == {"path": "degree2.cache.bin", "rows": P1_ROWS, "bytes": P1_CACHE_BYTES,
                      "sha256": P1_CACHE_SHA256, "final_lf": False, "eof": True} and
            instruction == {"path": "instructions.jsonl", "rows": P1_ROWS, "bytes": P1_INSTRUCTION_BYTES,
                            "sha256": P1_INSTRUCTION_SHA256, "final_lf": True, "eof": True,
                            "final_head": manifest.get("ancestry_sha256")} and
            value["files"] == [{"file": "degree2.cache.bin", "bytes": P1_CACHE_BYTES,
                                 "sha256": P1_CACHE_SHA256},
                                {"file": "instructions.jsonl", "bytes": P1_INSTRUCTION_BYTES,
                                 "sha256": P1_INSTRUCTION_SHA256}],
            "checker_p1_receipts")
    require({p.name for p in root.iterdir()} == {"manifest.json", "degree2.cache.bin", "instructions.jsonl"},
            "checker_p1_roster")
    return {"root": root, "manifest": manifest, "manifest_sha256": sha(raw),
            "cache": cache, "instruction": instruction}


def validate_separator(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) ==
            {"schema", "root", "artifact", "manifest", "physical", "lambda", "internal"} and
            value["schema"] == SCHEMA + ".separator-parent.v1" and value["artifact"] == {
                "run": SEPARATOR_RUN, "attempt": SEPARATOR_ATTEMPT, "head": SEPARATOR_HEAD,
                "id": SEPARATOR_ARTIFACT, "name": SEPARATOR_ARTIFACT_NAME,
                "bytes": SEPARATOR_ARCHIVE_BYTES, "sha256": SEPARATOR_ARCHIVE_SHA256},
            "checker_separator_identity")
    root = Path(value["root"]).absolute(); require(root.is_dir(), "checker_separator_root")
    manifest, raw = read_json(safe_path(root, value["manifest"]["file"]), None,
                              SEPARATOR_MANIFEST_SHA256, 1 << 20)
    require(value["manifest"]["sha256"] == SEPARATOR_MANIFEST_SHA256 and
            manifest.get("generation") == SEPARATOR_GENERATION and manifest.get("rank") == SEPARATOR_RANK and
            manifest.get("instructions", {}).get("final_head") == SEPARATOR_STATE_HEAD and
            manifest.get("candidate_roster") == ["physical.bin", "physical-p1-coeff.bin",
                                                   "instructions.jsonl", "manifest.json", "HEAD"],
            "checker_separator_manifest")
    lam_raw = receipt(root, value["lambda"], PHYSICAL_PACKED_BYTES)
    require(sha(lam_raw) == SEPARATOR_LAMBDA_SHA256, "checker_separator_lambda")
    lam = ARITH.unpack_trits(lam_raw, PHYSICAL_WIDTH); physical = value["physical"]
    require(physical == {"file": "state/physical.bin", "bytes": SEPARATOR_PHYSICAL_BYTES,
                         "sha256": SEPARATOR_PHYSICAL_SHA256, "rows": SEPARATOR_RANK},
            "checker_physical_receipt")
    path = safe_path(root, physical["file"]); h = hashlib.sha256()
    with path.open("rb") as stream:
        for _ in range(SEPARATOR_RANK):
            packed = stream.read(PHYSICAL_PACKED_BYTES)
            require(len(packed) == PHYSICAL_PACKED_BYTES, "checker_physical_eof")
            row = ARITH.unpack_trits(packed, PHYSICAL_WIDTH)
            require(ARITH.dot_mod3(lam, row) == 0, "checker_separator_dot"); h.update(packed)
        require(stream.read(1) == b"", "checker_physical_trailing")
    require(h.hexdigest() == SEPARATOR_PHYSICAL_SHA256, "checker_physical_digest")
    for item, wanted in ((value["internal"]["terminal"], SEPARATOR_TERMINAL_SHA256),
                         (value["internal"]["result"], SEPARATOR_RESULT_SHA256),
                         (value["internal"]["checker"], SEPARATOR_CHECKER_SHA256)):
        require(sha(receipt(root, item, 1 << 24)) == wanted, "checker_internal_receipt")
    return {"root": root, "manifest": manifest, "manifest_sha256": sha(raw),
            "lambda": lam, "lambda_sha256": sha(lam_raw), "generation": SEPARATOR_GENERATION}


def validate_launch(path: Path) -> tuple[dict[str, Any], bytes]:
    launch, raw = read_json(path, cap=1 << 24)
    claims = launch_claims()
    require(isinstance(launch, dict) and set(launch) ==
            {"schema", "fixture_only", "mode", "characters", "actors", "p1_parent", "task554_parent",
             "task712_parents", "separator_parent", "out", "claims", "source_pin"} and
            launch["schema"] == SCHEMA + ".launch.v1" and launch["fixture_only"] is False and
            launch["mode"] == "actual" and launch["characters"] == [list(x) for x in CHARACTERS] and
            launch["actors"] == list(ACTORS) and launch["claims"] == claims,
            "checker_launch_shape")
    verify_source(); require(launch["source_pin"] == {
        "producer": {"path": PRODUCER_ARITH_PATH.as_posix(), "sha256": PRODUCER_ARITH_SHA256},
        "checker": {"path": ARITH_PATH.as_posix(), "sha256": ARITH_SHA256}},
                             "checker_launch_source")
    separator = validate_separator(launch["separator_parent"]); p1 = validate_p1(launch["p1_parent"])
    task554 = validate_task554(launch["task554_parent"])
    parents = launch["task712_parents"]
    require(isinstance(parents, list) and len(parents) == 4, "checker_task712_parent_list")
    for item in parents:
        require(set(item) == set(TASK712_PARENT) | {"root"} and
                {key: item[key] for key in TASK712_PARENT} == TASK712_PARENT, "checker_task712_pin")
    return ({"launch": launch, "launch_raw": raw, "launch_sha256": sha(raw),
             "separator": separator, "p1": p1, "task554": task554, "task712": parents}, raw)


def covectors(separator: dict[str, Any], parents: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[list[np.ndarray]]]:
    tables: list[dict[str, Any]] = []; vectors: list[list[np.ndarray]] = []
    for character in range(4):
        table = ARITH.read_task712_envelope(parents[character], character); tables.append(table)
        for key in ("B", *ACTORS):
            check_table_transpose(table["forward"][key], table["adjoint"][key])
        root = ARITH.sparse_adjoint(table["forward"]["B"], SOURCE_WIDTH, PHYSICAL_WIDTH,
                                    separator["lambda"])
        children = [ARITH.sparse_adjoint(table["forward"][actor], SOURCE_WIDTH, SOURCE_WIDTH, root)
                    for actor in ACTORS]
        vectors.append([root] + children)
        nz = np.flatnonzero(root); packed = ARITH.pack_trits(root)
        wanted = EXPECTED_ROOT[character]
        require((int(len(nz)), int(nz[0]) if len(nz) else None,
                 int(root[nz[0]]) if len(nz) else None, sha(packed)) == wanted, "checker_root_pin")
        for slot, child in enumerate(children):
            require(sha(ARITH.pack_trits(child)) == EXPECTED_CHILD[character][slot], "checker_child_pin")
    return tables, vectors


def _shift(expression: Any, bound: int, offset: int) -> list[list[int]]:
    _expr(expression, bound, "checker_relation_expression")
    return [[offset + int(i), int(c)] for i, c in expression]


def _subtract(accumulator: Any, expression: Any, values: np.ndarray, bound: int,
              offset: int, relation_hash: Any, label: dict[str, Any]) -> int:
    # state_descriptor already checked strict local ordering and coefficients;
    # reuse the canonical list instead of allocating a normalized copy.
    terms = expression; result = int(accumulator)
    for index, coefficient in terms:
        result = (result - int(coefficient) * int(values[offset + index])) % 3
    return result


def accumulate_scalars(parent: dict[str, Any], character: int, direct: list[int],
                       values: list[np.ndarray]) -> dict[str, Any]:
    """Checker-owned direct accumulator; no nested relation tree is retained."""
    prepare = state_descriptor(parent["prepare"], -1); olds = prepare["body"]["old_blocks"]
    old_offsets: list[int] = []; cursor = 0
    for rank in OLD_RANKS: old_offsets.append(cursor); cursor += rank
    new_offsets: list[int] = []; cursor = sum(OLD_RANKS)
    for rank in NEW_RANKS: new_offsets.append(cursor); cursor += rank
    require(cursor == P1_ROWS and len(direct) == 44, "checker_accumulator_offsets")
    seeds = np.asarray(direct, dtype=np.uint8).copy()
    actor_values = np.column_stack([np.asarray(item, dtype=np.uint8) for item in values[1:]])
    require(actor_values.shape == (P1_ROWS, 4), "checker_accumulator_shape")
    # Bind only the fixed Task554 coefficient family here.  q/character
    # values belong to the scalar result, not this common relation receipt.
    relation_hash = relation_source_sha256()
    for seed in range(44):
        for source, old in enumerate(olds):
            seeds[seed] = _subtract(seeds[seed], old["record"]["seed_reductions"][seed],
                                    values[0], OLD_RANKS[source], old_offsets[source], relation_hash,
                                    {"kind": "seed-old", "source": source, "seed": seed})
    for source, old in enumerate(olds):
        for pivot in range(OLD_RANKS[source]):
            global_row = old_offsets[source] + pivot
            for slot in range(4):
                actor_values[global_row, slot] = _subtract(
                    actor_values[global_row, slot], old["record"]["actor_transitions"][pivot][slot],
                    values[0], OLD_RANKS[source], old_offsets[source], relation_hash,
                    {"kind": "actor-old", "basis_i": global_row, "slot": slot})
    for target in range(4):
        checked = state_descriptor(parent["blocks"][target], target); body = checked["body"]
        rank = NEW_RANKS[target]; offset = new_offsets[target]; reductions = body["origin_reductions"]
        for seed in range(44):
            for source in range(4):
                seeds[seed] = _subtract(
                    seeds[seed], reductions[ORIGIN_RANGES[source][0] + seed], values[0], rank,
                    new_offsets[target], relation_hash, {"kind": "seed-new", "target": target,
                                     "source": source, "seed": seed})
        for source in range(4):
            for pivot in range(OLD_RANKS[source]):
                global_row = old_offsets[source] + pivot
                for slot in range(4):
                    origin = ORIGIN_RANGES[source][0] + 44 + 4 * pivot + slot
                    actor_values[global_row, slot] = _subtract(
                        actor_values[global_row, slot], reductions[origin], values[0], rank,
                        new_offsets[target], relation_hash, {"kind": "actor-new-old", "target": target,
                                         "basis_i": global_row, "slot": slot})
        for local, row in enumerate(body["actor_transitions"]):
            global_row = offset + local
            for slot in range(4):
                actor_values[global_row, slot] = _subtract(
                    actor_values[global_row, slot], row[slot], values[0], rank,
                    new_offsets[target], relation_hash,
                    {"kind": "actor-new", "target": target, "basis_i": global_row, "slot": slot})
        del reductions, body, checked
    del prepare, olds
    return {"seed_values": seeds, "actor_values": actor_values,
            "relation_sha256": relation_hash, "origins": SCALAR_ORIGINS,
            "accumulator_count": SCALAR_ORIGINS}


def make_raw(character: int, table: dict[str, Any], separator: dict[str, Any],
             vector: np.ndarray) -> dict[str, Any]:
    packed = ARITH.pack_trits(vector)
    body = {"schema": ARITH.LIVE_SCHEMA + ".RawDual", "separator_generation": separator["generation"],
            "separator_s_head_sha256": SEPARATOR_STATE_HEAD, "lambda_sha256": separator["lambda_sha256"],
            "character": character, "B_adj_table_identity": table["identity"]["adjoint:B"],
            "word_node": {"kind": "root", "character": character, "actors": []},
            # This is the root node; actor identities belong to future edges.
            "actor_table_identities_along_w": [],
            "raw_q_packed_sha256": sha(packed), "raw_q_packed_offset": 0,
            "raw_q_packed_length": len(packed), "raw_predecessor_sha256": None}
    return {**body, "sha256": sha(canonical(body))}


def p1_values(p1: dict[str, Any], vectors: list[list[np.ndarray]]) -> dict[str, Any]:
    values = [[np.zeros(P1_ROWS, dtype=np.uint8) for _ in range(5)] for _ in range(4)]
    instruction_path = safe_path(p1["root"], p1["instruction"]["path"])
    _, instruction_sha = file_hash(instruction_path, P1_INSTRUCTION_BYTES, 1 << 30)
    require(instruction_sha == P1_INSTRUCTION_SHA256, "checker_instruction_hash")
    active = [bool(np.count_nonzero(group[0])) for group in vectors]
    require(active == [True, False, False, False], "checker_active_root_pin")
    projections: list[list[tuple[np.ndarray, np.ndarray, np.ndarray]]] = []
    for character in range(4):
        group: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []
        for vector in vectors[character]:
            pairs = [(int(i), int(vector[i])) for i in np.flatnonzero(vector)]
            if pairs:
                byte_index = np.asarray([i // 4 for i, _ in pairs], dtype=np.int64)
                digit_slot = np.asarray([i % 4 for i, _ in pairs], dtype=np.int64)
                coefficient = np.asarray([c for _, c in pairs], dtype=np.uint32)
            else:
                byte_index = np.asarray([], dtype=np.int64)
                digit_slot = np.asarray([], dtype=np.int64)
                coefficient = np.asarray([], dtype=np.uint32)
            group.append((byte_index, digit_slot, coefficient))
        projections.append(group)
    cache_path = safe_path(p1["root"], p1["cache"]["path"]); cache_hash = hashlib.sha256()
    buffer = bytearray(P1_ROW_BYTES * 256)
    cursor = 0
    with cache_path.open("rb") as stream:
        while cursor < P1_ROWS:
            count_rows = min(256, P1_ROWS - cursor)
            byte_count = count_rows * P1_ROW_BYTES
            require(stream.readinto(memoryview(buffer)[:byte_count]) == byte_count,
                    "checker_cache_eof")
            raw_chunk = memoryview(buffer)[:byte_count]; cache_hash.update(raw_chunk)
            packed_rows = np.frombuffer(raw_chunk, dtype=np.uint8).reshape(count_rows, P1_ROW_BYTES)
            for character in range(4):
                if not active[character]:
                    continue
                projected = vectorized_projection_chunk(
                    packed_rows, character * SLICE_BYTES, projections[character])
                for slot in range(5):
                    values[character][slot][cursor:cursor + count_rows] = projected[:, slot]
            cursor += count_rows
        require(stream.read(1) == b"", "checker_cache_trailing")
    require(cache_hash.hexdigest() == P1_CACHE_SHA256, "checker_cache_hash")
    return {"values": values, "manifest_sha256": p1["manifest_sha256"],
            "cache_sha256": cache_hash.hexdigest(), "instruction_sha256": instruction_sha,
            "value_sha256": [sha(v.tobytes()) for group in values for v in group],
            "rows": P1_ROWS, "cache_passes": 1, "instruction_passes": 1,
            "active_characters": [0], "active_pairings": 5}


def _scan_accumulated(raw: dict[str, Any], accum: dict[str, Any],
                      p1: dict[str, Any]) -> dict[str, Any]:
    """Independent scalar-order replay over the direct accumulator."""
    ARITH.validate_raw_dual(raw)
    seeds = accum["seed_values"]; actors = accum["actor_values"]
    require(len(seeds) == 44 and actors.shape == (P1_ROWS, 4),
            "checker_accumulator_scan_shape")
    chain = b"\0" * 32; origin = 0

    def emit(kind: str, descriptor: dict[str, Any], scalar: int) -> dict[str, Any] | None:
        nonlocal chain, origin
        record = {"origin_id": origin, "origin_kind": kind, **descriptor,
                  "scalar": int(scalar)}
        chain = hashlib.sha256(chain + canonical(record)).digest(); origin += 1
        if scalar:
            return _sealed("Violation", {
                "raw_dual_sha256": raw["sha256"], "character": raw["character"],
                "word_node_sha256": sha(canonical(raw["word_node"])), **record,
                "scalar_prefix_digest": chain.hex(),
                "p1_manifest_sha256": p1["manifest_sha256"],
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
    require(origin == SCALAR_ORIGINS, "checker_accumulator_origin_eof")
    return _sealed("ScalarEOF", {
        "raw_dual_sha256": raw["sha256"], "p1_manifest_sha256": p1["manifest_sha256"],
        "global_relation_stream_sha256": accum["relation_sha256"],
        "origins": SCALAR_ORIGINS, "seed_pairings": 44,
        "actor_pairings": 4 * P1_ROWS, "next_origin": SCALAR_ORIGINS,
        "coefficient_stream_eof": True, "p1_cache_pass_eof": True,
        "value_vector_sha256": [sha(value.tobytes()) for value in p1["values"]],
        "rolling_scalar_head": chain.hex()})


def _sealed(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    result = {"schema": ARITH.LIVE_SCHEMA + "." + kind, **body}
    result["sha256"] = sha(canonical(result)); return result


def _expected_character(character: int, table: dict[str, Any], vectors: list[np.ndarray],
                        separator: dict[str, Any], p1: dict[str, Any], task554: dict[str, Any],
                        values: list[np.ndarray]) -> dict[str, Any]:
    root = vectors[0]; packed = ARITH.pack_trits(root); nz = np.flatnonzero(root)
    children = [{"actor": actor, "support": int(np.count_nonzero(vector)),
                 "packed_sha256": sha(ARITH.pack_trits(vector))}
                for actor, vector in zip(ACTORS, vectors[1:])]
    base = {"character": character, "character_label": list(CHARACTERS[character]),
            "root_support": int(np.count_nonzero(root)), "root_packed_sha256": sha(packed),
            "children": children, "task712_table_identities": table["identity"],
            "raw_dual": make_raw(character, table, separator, root), "root_packed_bytes": len(packed)}
    ARITH.validate_raw_dual(base["raw_dual"])
    if not len(nz):
        unsigned = {"schema": SCHEMA + ".RootZero", **base, "root_scalar": "zero"}
        unsigned["sha256"] = sha(canonical(unsigned)); return unsigned
    direct = ARITH.checker_direct_seed_evaluations(root, character)
    accumulator = accumulate_scalars(task554, character, direct,
                                     [values[slot] for slot in range(5)])
    base["relation_stream_sha256"] = accumulator["relation_sha256"]
    scalar = _scan_accumulated(base["raw_dual"], accumulator,
                                {"manifest_sha256": p1["manifest_sha256"], "values": values})
    base["scalar"] = scalar; base["scalar_schema"] = scalar["schema"]
    if scalar["schema"].endswith("ScalarEOF"):
        lead = int(nz[0]); scale = 1 if int(root[lead]) == 1 else 2
        normalized = ((scale * root.astype(np.uint16)) % 3).astype(np.uint8)
        normalized_packed = ARITH.pack_trits(normalized); normalized_sha = sha(normalized_packed)
        remainder_sha = sha(packed)
        next_head = ARITH._dual_next_state_head(
            "0" * 64, 0, lead, normalized_sha, base["raw_dual"]["sha256"],
            remainder_sha, 1)
        base["normalized_root_state"] = {
            "lead": lead, "scale": scale, "raw_lead": lead,
            "raw_lead_scalar": int(root[lead]), "raw_packed_sha256": sha(packed),
            "raw_q_file": f"q-a{character}-root.bin", "raw_q_file_bytes": len(packed),
            "raw_q_file_sha256": sha(packed), "raw_dual_sha256": base["raw_dual"]["sha256"],
            "remainder_sha256": remainder_sha, "normalized_packed_sha256": normalized_sha,
            "packed_sha256": normalized_sha, "normalized_pivot_sha256": normalized_sha,
            "normalized_packed_bytes": len(normalized_packed),
            "prior_state_head_sha256": "0" * 64, "prior_pivot_coefficients": [],
            "rank_before": 0, "insertion_id": 0, "dual_rank_after": 1,
            "next_state_head_sha256": next_head, "rolling_head": next_head,
            "normalized_from_raw_q": True,
            "future_orbit_bound": 504, "remaining_independent_after_root": 503}
    result = {"schema": SCHEMA + (".RootViolation" if scalar["schema"].endswith("Violation") else ".RootScalarEOF"),
              **base}; result["sha256"] = sha(canonical(result)); return result


def launch_claims() -> dict[str, Any]:
    return {"ROOT_SCALAR_BATCH_CANDIDATE": True, "COMPLETE_DUAL_ORBITS": False,
            "GRADE2_MEMBER": "NOT_DECIDED", "GRADE2_NONMEMBER": "NOT_DECIDED",
            "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED", "COFINAL_LIFT": "NOT_DECLARED",
            "FAKE": "NOT_DECLARED", "IHARA": "NOT_DECLARED", "verified": False}


def terminal_claims() -> dict[str, Any]:
    return {"ROOT_SCALAR_BATCH_CANDIDATE": True, "COMPLETE_DUAL_ORBITS": False,
            "GRADE2_MEMBER": "NOT_DECIDED", "GRADE2_NONMEMBER": "NOT_DECIDED",
            "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED", "COFINAL_LIFT": "NOT_DECLARED",
            "FAKE": "NOT_DECLARED", "IHARA": "NOT_DECLARED", "verified": False}


def terminal_kind(records: list[dict[str, Any]]) -> str:
    require(isinstance(records, list) and len(records) == 4,
            "checker_terminal_record_count")
    return ("RootViolationBatch" if any(
        item.get("schema", "").endswith("RootViolation") for item in records)
            else "AllFourRootEOF")


def validate_scalar_record(actual: Any, expected: Any) -> None:
    require(actual == expected and sealed_object(actual),
            "checker_scalar_record_exact")


def validate_character_record(actual: Any, expected: Any) -> None:
    require(isinstance(actual, dict) and isinstance(expected, dict),
            "checker_character_record_shape")
    if "scalar" in expected:
        validate_scalar_record(actual.get("scalar"), expected["scalar"])
    require(actual == expected and sealed_object(actual),
            "checker_character_record_exact")


def validate_output_objects(terminal: Any, result: Any, manifest: Any,
                            expected_terminal: Any, expected_result: Any,
                            expected_manifest: Any) -> None:
    """Exact sealed-object join used by production output checking."""
    require(terminal == expected_terminal and sealed_object(terminal),
            "checker_terminal_exact")
    require(result == expected_result and sealed_object(result),
            "checker_result_exact")
    require(manifest == expected_manifest and sealed_object(manifest),
            "checker_manifest_exact")


def check_output(base: dict[str, Any], tables: list[dict[str, Any]], vectors: list[list[np.ndarray]],
                 values: dict[str, Any]) -> dict[str, Any]:
    out = Path(base["launch"]["out"]).absolute(); require(out.is_dir(), "checker_output_root")
    manifest, manifest_raw = read_json(out / "manifest.json", cap=1 << 24)
    files = manifest.get("files"); require(isinstance(files, list), "checker_output_manifest_files")
    actual = sorted(p.name for p in out.iterdir() if p.is_file())
    require(manifest.get("file_roster") == actual and len(actual) == len(set(actual)) and
            "manifest.json" in actual and "result.json" in actual and "terminal.json" in actual,
            "checker_output_roster")
    by_name = {item.get("file"): item for item in files if isinstance(item, dict)}
    require(len(by_name) == len(files), "checker_output_receipt_unique")
    for item in files: receipt(out, item, 1 << 28)
    terminal, terminal_raw = read_json(out / "terminal.json", cap=1 << 24)
    result, result_raw = read_json(out / "result.json", cap=1 << 24)
    expected_chars: list[dict[str, Any]] = []
    expected_records: list[dict[str, Any]] = []
    expected_result_files: list[dict[str, Any]] = []
    for character in range(4):
        child_receipts = []
        for slot, wanted in enumerate(EXPECTED_CHILD[character]):
            item = {"file": f"q-a{character}-t{slot}", "bytes": SLICE_BYTES,
                    "sha256": wanted}
            # The producer's file name includes the .bin suffix; retain the
            # exact receipt in the sealed result order below.
            item["file"] += ".bin"
            child_receipts.append(item)
            child_raw = receipt(out, item, 1 << 20)
            require(child_raw == ARITH.pack_trits(vectors[character][slot + 1]),
                    "checker_child_file")
        root_item = {"file": f"q-a{character}-root.bin", "bytes": SLICE_BYTES,
                     "sha256": EXPECTED_ROOT[character][3]}
        root_raw = receipt(out, root_item, 1 << 20)
        require(root_raw == ARITH.pack_trits(vectors[character][0]), "checker_root_file")
        expected = _expected_character(character, tables[character], vectors[character], base["separator"],
                                       base["p1"], base["task554"], values["values"][character])
        actual_path = out / f"character-a{character}.json"; got, got_raw = read_json(actual_path, cap=1 << 24)
        validate_character_record(got, expected)
        expected_chars.append({"character": character, "schema": expected["schema"], "sha256": expected["sha256"]})
        expected_records.append(expected)
        expected_result_files.extend(child_receipts + [root_item,
            {"file": f"character-a{character}.json", "bytes": len(got_raw),
             "sha256": sha(got_raw)}])
        if expected["schema"].endswith("RootScalarEOF"):
            state_name = f"root-state-a{character}.json"
            state_value, state_raw = read_json(out / state_name, cap=1 << 20)
            require(state_value == expected["normalized_root_state"], "checker_root_state_replay")
            require(sha(state_raw) == sha(canonical(state_value)), "checker_root_state_canonical")
            expected_result_files.append({"file": state_name, "bytes": len(state_raw),
                                          "sha256": sha(state_raw)})
    terminal_value = terminal_kind(expected_records)
    expected_terminal_body = {
        "schema": SCHEMA + ".terminal", "terminal": terminal_value,
        "character_order": [list(x) for x in CHARACTERS], "actor_order": list(ACTORS),
        "characters": expected_chars, "p1_cache_passes": 1, "p1_rows": P1_ROWS,
        "global_relation_count": SCALAR_ORIGINS, "future_active_orbit_bound": 504,
        **terminal_claims()}
    expected_terminal = {**expected_terminal_body,
                        "sha256": sha(canonical(expected_terminal_body))}
    expected_terminal_receipt = {"file": "terminal.json", "bytes": len(terminal_raw),
                                 "sha256": sha(terminal_raw)}
    expected_result_files.append(expected_terminal_receipt)
    expected_result_body = {
        "schema": SCHEMA + ".result", "launch_sha256": base["launch_sha256"],
        "separator_manifest_sha256": base["separator"]["manifest_sha256"],
        "p1_manifest_sha256": base["p1"]["manifest_sha256"],
        "task712_manifest_sha256": [item["manifest_sha256"] for item in tables],
        "global_relation_stream_sha256": expected_records[0].get("relation_stream_sha256"),
        "cache_passes": 1, "instruction_passes": 1, "rows": P1_ROWS,
        "characters": [item["sha256"] for item in expected_chars],
        "terminal_sha256": expected_terminal["sha256"], "files": expected_result_files,
        "claims": base["launch"]["claims"]}
    expected_result = {**expected_result_body,
                       "sha256": sha(canonical(expected_result_body))}
    expected_result_raw = canonical(expected_result)
    expected_result_receipt = {"file": "result.json", "bytes": len(expected_result_raw),
                               "sha256": sha(expected_result_raw)}
    expected_manifest_files = sorted(expected_result_files + [expected_result_receipt],
                                     key=lambda item: item["file"])
    expected_manifest_body = {
        "schema": SCHEMA + ".output-manifest", "terminal": terminal_value,
        "file_roster": sorted([item["file"] for item in expected_manifest_files] +
                               ["manifest.json"]),
        "files": expected_manifest_files, "result": expected_result_receipt,
        "candidate": True, "verified": False}
    expected_manifest = {**expected_manifest_body,
                         "sha256": sha(canonical(expected_manifest_body))}
    expected_names = {item["file"] for item in expected_result_files} | {"result.json", "manifest.json"}
    require(set(actual) == expected_names, "checker_output_exact_roster")
    validate_output_objects(terminal, result, manifest, expected_terminal,
                            expected_result, expected_manifest)
    return {"status": "PASS", "terminal": terminal["terminal"], "rows": P1_ROWS,
            "root_characters": 4, "cache_passes": 1, "relation_origins": SCALAR_ORIGINS,
            "complete_dual_orbits": False, "verified": False}


def _expect_reject(action: Any, reason: str) -> None:
    try:
        action()
    except Exception:
        return
    raise RuntimeError(reason)


def selftest() -> dict[str, Any]:
    rng = np.random.default_rng(9081)
    dense = rng.integers(0, 3, P1_ROW_TRITS, dtype=np.uint8)
    packed = ARITH.pack_trits(dense)
    vectors = [rng.integers(0, 3, SOURCE_WIDTH, dtype=np.uint8) for _ in range(20)]
    sparse_ok = []
    for offset in range(4):
        for vector in vectors[offset:offset + 4]:
            entries = [(int(i), int(vector[i])) for i in np.flatnonzero(vector)]
            sparse_ok.append(sparse_projection(packed, offset * SLICE_BYTES, entries) ==
                             ARITH.dot_mod3(ARITH.unpack_trits(
                                 packed[offset * SLICE_BYTES:(offset + 1) * SLICE_BYTES], SOURCE_WIDTH), vector))
    require(all(sparse_ok), "selftest_sparse")

    # Compare the checker vectorized five-value call with five independent
    # scalar projections; this is not the same expression twice.
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
                                   [(int(i), int(vectors[5 * character + slot][i]))
                                    for i in np.flatnonzero(vectors[5 * character + slot])])
                 for slot in range(5)] for character in range(4)]
    require(simultaneous == separate, "selftest_batch_equivalence")

    # Exercise the exact vectorized chunk path, including a short final chunk,
    # against independently unpacked dense rows at all four offsets.
    tiny_dense = rng.integers(0, 3, size=(3, P1_ROW_TRITS), dtype=np.uint8)
    tiny_rows = np.vstack([np.frombuffer(ARITH.pack_trits(item), dtype=np.uint8)
                           for item in tiny_dense])
    for character in range(4):
        got = vectorized_projection_chunk(tiny_rows, character * SLICE_BYTES,
                                           chunk_projections[character])
        expected = np.asarray([[ARITH.dot_mod3(
            ARITH.unpack_trits(bytes(tiny_rows[row])[character * SLICE_BYTES:
                                                    (character + 1) * SLICE_BYTES], SOURCE_WIDTH),
            vectors[5 * character + slot]) for slot in range(5)] for row in range(3)], dtype=np.uint8)
        require(np.array_equal(got, expected), "checker_vectorized_chunk_dense")

    table_control = False
    with tempfile.TemporaryDirectory(prefix="d972-r07-task913-checker-table-") as temp:
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
                       "checker_task712_transpose_control")

    separator_control = False
    separator_names = ("SEPARATOR_RUN", "SEPARATOR_ATTEMPT", "SEPARATOR_HEAD",
                       "SEPARATOR_ARTIFACT", "SEPARATOR_ARTIFACT_NAME",
                       "SEPARATOR_ARCHIVE_BYTES", "SEPARATOR_ARCHIVE_SHA256",
                       "SEPARATOR_MANIFEST_SHA256", "SEPARATOR_PHYSICAL_BYTES",
                       "SEPARATOR_PHYSICAL_SHA256", "SEPARATOR_LAMBDA_SHA256",
                       "SEPARATOR_TERMINAL_SHA256", "SEPARATOR_RESULT_SHA256",
                       "SEPARATOR_CHECKER_SHA256", "SEPARATOR_GENERATION",
                       "SEPARATOR_RANK", "SEPARATOR_STATE_HEAD")
    saved_separator = {name: globals()[name] for name in separator_names}
    try:
        zero_physical = bytes(PHYSICAL_PACKED_BYTES); state_head = "b" * 64
        manifest_body = {"generation": 1, "rank": 1,
                         "instructions": {"final_head": state_head},
                         "candidate_roster": ["physical.bin", "physical-p1-coeff.bin",
                                              "instructions.jsonl", "manifest.json", "HEAD"]}
        manifest_raw = canonical(manifest_body)
        internal_raw = {"terminal": b"terminal", "result": b"result", "checker": b"checker"}
        globals().update({"SEPARATOR_RUN": 1, "SEPARATOR_ATTEMPT": 1,
                          "SEPARATOR_HEAD": "h" * 40, "SEPARATOR_ARTIFACT": 2,
                          "SEPARATOR_ARTIFACT_NAME": "tiny-separator", "SEPARATOR_ARCHIVE_BYTES": 3,
                          "SEPARATOR_ARCHIVE_SHA256": "sha256:" + "a" * 64,
                          "SEPARATOR_MANIFEST_SHA256": sha(manifest_raw),
                          "SEPARATOR_PHYSICAL_BYTES": len(zero_physical),
                          "SEPARATOR_PHYSICAL_SHA256": sha(zero_physical),
                          "SEPARATOR_LAMBDA_SHA256": sha(zero_physical),
                          "SEPARATOR_TERMINAL_SHA256": sha(internal_raw["terminal"]),
                          "SEPARATOR_RESULT_SHA256": sha(internal_raw["result"]),
                          "SEPARATOR_CHECKER_SHA256": sha(internal_raw["checker"]),
                          "SEPARATOR_GENERATION": 1, "SEPARATOR_RANK": 1,
                          "SEPARATOR_STATE_HEAD": state_head})
        with tempfile.TemporaryDirectory(prefix="d972-r07-task913-checker-separator-") as temp:
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

    p1_control = False
    p1_names = ("P1_RUN", "P1_ATTEMPT", "P1_HEAD", "P1_ARTIFACT", "P1_ARTIFACT_NAME",
                "P1_ARCHIVE_BYTES", "P1_ARCHIVE_SHA256", "P1_MANIFEST_BYTES",
                "P1_MANIFEST_SHA256", "P1_CACHE_BYTES", "P1_CACHE_SHA256",
                "P1_INSTRUCTION_BYTES", "P1_INSTRUCTION_SHA256", "P1_ROWS")
    saved_p1 = {name: globals()[name] for name in p1_names}
    try:
        cache_raw = bytes(P1_ROW_BYTES); instruction_raw = b"x"; ancestry = "c" * 64
        globals().update({"P1_RUN": 1, "P1_ATTEMPT": 1, "P1_HEAD": "p" * 40,
                          "P1_ARTIFACT": 2, "P1_ARTIFACT_NAME": "tiny-p1", "P1_ARCHIVE_BYTES": 3,
                          "P1_ARCHIVE_SHA256": "sha256:" + "d" * 64, "P1_CACHE_BYTES": len(cache_raw),
                          "P1_CACHE_SHA256": sha(cache_raw), "P1_INSTRUCTION_BYTES": len(instruction_raw),
                          "P1_INSTRUCTION_SHA256": sha(instruction_raw), "P1_ROWS": 1})
        manifest = {"schema": "d972.r07.canonical-p1-dag-degree2-lift.v8",
                    "status": "CANONICAL_P1_DAG_DEGREE2_LIFT_CANDIDATE", "rows": 1,
                    "row_trits": P1_ROW_TRITS, "row_bytes": P1_ROW_BYTES,
                    "global_order": [0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059],
                    "actor_order": list(ACTORS), "character_order": [list(x) for x in CHARACTERS],
                    "independent_checker": False, "A0": False, "COMMON": False,
                    "COFINAL": False, "FAKE": False, "IHARA": False, "verified": False,
                    "ancestry_sha256": ancestry,
                    "cache": {"path": "degree2.cache.bin", "rows": 1, "bytes": len(cache_raw),
                              "sha256": sha(cache_raw), "final_lf": False, "eof": True},
                    "instruction": {"path": "instructions.jsonl", "rows": 1,
                                    "bytes": len(instruction_raw), "sha256": sha(instruction_raw),
                                    "final_lf": True, "eof": True, "final_head": ancestry}}
        manifest_raw = canonical(manifest)
        globals()["P1_MANIFEST_BYTES"] = len(manifest_raw); globals()["P1_MANIFEST_SHA256"] = sha(manifest_raw)
        with tempfile.TemporaryDirectory(prefix="d972-r07-task913-checker-p1-") as temp:
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
            tiny_vectors = [[np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)] for _ in range(4)]
            tiny_vectors[0][0][0] = 1
            p1_values(checked, tiny_vectors)
            bad_manifest = json.loads(json.dumps(parent)); bad_manifest["manifest"]["sha256"] = "0" * 64
            _expect_reject(lambda: validate_p1(bad_manifest), "selftest_p1_manifest_control")
            (root / "degree2.cache.bin").write_bytes(cache_raw[:-1])
            _expect_reject(lambda: p1_values(checked, tiny_vectors), "selftest_p1_truncation_control")
        p1_control = True
    finally:
        globals().update(saved_p1)

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
        prepare_raw = canonical(prepare); prepare_hash = sha(prepare_raw); block_bodies = []
        for character, rank in enumerate(NEW_RANKS):
            if rank:
                reductions = [[[0, 1 if index % 2 == 0 else 2]] for index in range(TASK554_ORIGINS)]
                transitions = [[[[0, 1]], [[0, 2]], [[0, 1]], [[0, 2]]]]
                nodes = [{"pivot": 0, "lead": 0, "scale": 1, "reductions": [[0, 1]]}]
                leads = [0]
            else:
                reductions = [[] for _ in range(TASK554_ORIGINS)]; transitions = []; nodes = []; leads = []
            block_bodies.append({"schema": "d972.r07.a0.first-rung-grade1.v3.state", "phase": "block",
                                 "parent_sha256": prepare_hash, "character_index": character,
                                 "character": list(CHARACTERS[character]), "rank": rank,
                                 "origin_count": TASK554_ORIGINS, "attempts": TASK554_ORIGINS + 4 * rank,
                                 "actor_order": list(ACTORS), "queue_exhausted": True,
                                 "origin_reductions": reductions, "actor_transitions": transitions,
                                 "dag_nodes": nodes, "pivot_leads": leads,
                                 "dag_sha256": sha(canonical(nodes))})
        body_values = [prepare] + block_bodies; body_raws = [canonical(value) for value in body_values]
        body_hashes = tuple(sha(raw) for raw in body_raws); globals()["TASK554_BODY_DIGESTS"] = body_hashes

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

        with tempfile.TemporaryDirectory(prefix="d972-r07-task913-checker-accumulator-") as temp:
            root = Path(temp); descriptors = [write_state(root, -1, body_raws[0], body_hashes[0])]
            descriptors.extend(write_state(root, index, body_raws[index + 1], body_hashes[index + 1])
                               for index in range(4))
            values = [np.asarray(item, dtype=np.uint8) for item in (
                [1, 2, 0], [0, 1, 2], [2, 0, 1], [1, 1, 0], [2, 2, 1])]
            direct = [index % 3 for index in range(44)]
            got = accumulate_scalars({"prepare": descriptors[0], "blocks": descriptors[1:]},
                                     0, direct, values)
            expected_seeds = np.asarray(direct, dtype=np.uint8)
            expected_actors = np.column_stack(values[1:]).astype(np.uint8, copy=True)

            def direct_sub(accumulator: int, expression: list[list[int]], bound: int,
                           offset: int) -> int:
                _expr(expression, bound, "checker_selftest_direct_relation")
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
                    for pivot in range(OLD_RANKS[source]):
                        for slot in range(4):
                            origin = ORIGIN_RANGES[source][0] + 44 + 4 * pivot + slot
                            expected_actors[old_offsets[source] + pivot, slot] = direct_sub(
                                expected_actors[old_offsets[source] + pivot, slot],
                                body["origin_reductions"][origin], rank, offset)
                for local, row_value in enumerate(body["actor_transitions"]):
                    for slot in range(4):
                        expected_actors[offset + local, slot] = direct_sub(
                            expected_actors[offset + local, slot], row_value[slot], rank, offset)
            require(np.array_equal(got["seed_values"], expected_seeds) and
                    np.array_equal(got["actor_values"], expected_actors) and
                    got["accumulator_count"] == 56, "checker_two_block_accumulator")
            tiny_accumulator_control = True
    finally:
        globals().update(saved_accumulator)

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
    eof_record = _scan_accumulated(fake, eof_accumulator, scan_cache)
    require(eof_record["schema"].endswith("ScalarEOF") and eof_record["origins"] == SCALAR_ORIGINS and
            sealed_object(eof_record), "checker_full_scalar_eof")
    seed_accumulator = {"seed_values": np.zeros(44, dtype=np.uint8),
                        "actor_values": np.zeros((P1_ROWS, 4), dtype=np.uint8),
                        "relation_sha256": "3" * 64}
    seed_accumulator["seed_values"][0] = 1
    seed_record = _scan_accumulated(fake, seed_accumulator, scan_cache)
    require(seed_record["schema"].endswith("Violation") and seed_record["origin_id"] == 0 and
            seed_record["origin_kind"] == "seed" and seed_record["seed"] == 0,
            "checker_seed_first")
    actor_accumulator = {"seed_values": np.zeros(44, dtype=np.uint8),
                         "actor_values": np.zeros((P1_ROWS, 4), dtype=np.uint8),
                         "relation_sha256": "3" * 64}
    actor_accumulator["actor_values"][0, 0] = 1
    actor_record = _scan_accumulated(fake, actor_accumulator, scan_cache)
    require(actor_record["schema"].endswith("Violation") and actor_record["origin_id"] == 44 and
            actor_record["origin_kind"] == "actor" and actor_record["basis_i"] == 0 and
            actor_record["actor"] == ACTORS[0], "checker_actor_first")

    zero_table = {"identity": {"adjoint:B": "B:tiny"}}
    zero_separator = {"generation": 0, "lambda_sha256": "0" * 64}
    zero_vectors = [[np.zeros(SOURCE_WIDTH, dtype=np.uint8) for _ in range(5)] for _ in range(4)]
    zero_records = [_expected_character(character, zero_table, zero_vectors[character], zero_separator,
                                        {}, {}, zero_vectors[character]) for character in range(4)]
    require(all(item["schema"].endswith("RootZero") for item in zero_records), "checker_zero_root")
    require(terminal_kind(zero_records) == "AllFourRootEOF", "checker_all_four_root_eof")

    # Relation syntax/order is the validator used for every Task554 body.
    _expect_reject(lambda: _expr([[1, 1], [0, 2]], 2, "checker_relation_order"),
                   "checker_task554_relation_order_control")

    # The same exact-record validator used by check_output must reject
    # coherently resealed relation, child and scalar-prefix changes.
    character_expected = {"schema": SCHEMA + ".RootScalarEOF", "character": 0,
                          "children": [{"actor": ACTORS[0], "packed_sha256": "a" * 64}],
                          "relation_stream_sha256": "b" * 64, "scalar": eof_record}
    character_expected["sha256"] = sha(canonical(character_expected))
    validate_character_record(character_expected, character_expected)
    bad_relation = json.loads(json.dumps(character_expected)); bad_relation["relation_stream_sha256"] = "c" * 64
    bad_relation["sha256"] = sha(canonical({k: v for k, v in bad_relation.items() if k != "sha256"}))
    _expect_reject(lambda: validate_character_record(bad_relation, character_expected),
                   "checker_relation_reseal_control")
    bad_child = json.loads(json.dumps(character_expected)); bad_child["children"][0]["packed_sha256"] = "d" * 64
    bad_child["sha256"] = sha(canonical({k: v for k, v in bad_child.items() if k != "sha256"}))
    _expect_reject(lambda: validate_character_record(bad_child, character_expected),
                   "checker_child_reseal_control")
    bad_prefix = json.loads(json.dumps(character_expected)); bad_prefix["scalar"]["rolling_scalar_head"] = "e" * 64
    bad_prefix["scalar"]["sha256"] = sha(canonical({k: v for k, v in bad_prefix["scalar"].items() if k != "sha256"}))
    bad_prefix["sha256"] = sha(canonical({k: v for k, v in bad_prefix.items() if k != "sha256"}))
    _expect_reject(lambda: validate_character_record(bad_prefix, character_expected),
                   "checker_prefix_reseal_control")

    # Exercise the exact terminal/result/manifest join helper with a
    # coherently resealed upper claim and each authenticated parent join.
    terminal_body = {"schema": SCHEMA + ".terminal", "terminal": "AllFourRootEOF",
                     "claim": "candidate", "verified": False}
    expected_terminal = {**terminal_body, "sha256": sha(canonical(terminal_body))}
    result_body = {"schema": SCHEMA + ".result", "launch_sha256": "1" * 64,
                   "separator_manifest_sha256": "2" * 64, "p1_manifest_sha256": "3" * 64,
                   "task712_manifest_sha256": ["4" * 64] * 4}
    expected_result = {**result_body, "sha256": sha(canonical(result_body))}
    manifest_body = {"schema": SCHEMA + ".output-manifest", "terminal": "AllFourRootEOF",
                     "candidate": True, "verified": False}
    expected_manifest = {**manifest_body, "sha256": sha(canonical(manifest_body))}
    validate_output_objects(expected_terminal, expected_result, expected_manifest,
                            expected_terminal, expected_result, expected_manifest)
    bad_terminal = dict(expected_terminal); bad_terminal["claim"] = "GRADE2_MEMBER";
    bad_terminal["sha256"] = sha(canonical({k: v for k, v in bad_terminal.items() if k != "sha256"}))
    _expect_reject(lambda: validate_output_objects(bad_terminal, expected_result, expected_manifest,
                                                   expected_terminal, expected_result, expected_manifest),
                   "checker_terminal_claim_control")
    for field, altered in (("launch_sha256", "9" * 64),
                           ("separator_manifest_sha256", "8" * 64),
                           ("p1_manifest_sha256", "7" * 64),
                           ("task712_manifest_sha256", ["6" * 64] * 4)):
        bad_result = dict(expected_result); bad_result[field] = altered
        bad_result["sha256"] = sha(canonical({k: v for k, v in bad_result.items() if k != "sha256"}))
        _expect_reject(lambda bad_result=bad_result: validate_output_objects(
            expected_terminal, bad_result, expected_manifest,
            expected_terminal, expected_result, expected_manifest),
            "checker_result_join_control")
    bad_manifest = dict(expected_manifest); bad_manifest["terminal"] = "RootViolationBatch"
    bad_manifest["sha256"] = sha(canonical({k: v for k, v in bad_manifest.items() if k != "sha256"}))
    _expect_reject(lambda: validate_output_objects(expected_terminal, expected_result, bad_manifest,
                                                   expected_terminal, expected_result, expected_manifest),
                   "checker_manifest_join_control")

    # Exercise the actual canonical launch handoff.  The parent validators are
    # replaced only inside this bounded test so no real parent is opened; the
    # launch file itself still goes through validate_launch and its exact
    # source/claim/shape checks.
    launch_handoff_control = False
    saved_validators = (validate_separator, validate_p1, validate_task554)
    try:
        globals()["validate_separator"] = lambda value: {}
        globals()["validate_p1"] = lambda value: {}
        globals()["validate_task554"] = lambda value: {}
        with tempfile.TemporaryDirectory(prefix="d972-r07-task915-launch-") as temp:
            root = Path(temp)
            task712 = [dict(TASK712_PARENT, root=str(root / ("task712-" + str(index))))
                       for index in range(4)]
            launch = {"schema": SCHEMA + ".launch.v1", "fixture_only": False, "mode": "actual",
                      "characters": [list(item) for item in CHARACTERS], "actors": list(ACTORS),
                      "p1_parent": {}, "task554_parent": {}, "task712_parents": task712,
                      "separator_parent": {}, "out": str(root / "out"), "claims": launch_claims(),
                      "source_pin": {"producer": {"path": PRODUCER_ARITH_PATH.as_posix(),
                                                    "sha256": PRODUCER_ARITH_SHA256},
                                     "checker": {"path": ARITH_PATH.as_posix(),
                                                 "sha256": ARITH_SHA256}}}
            launch_path = root / "launch.json"; launch_raw = canonical(launch)
            launch_path.write_bytes(launch_raw)
            checked, authenticated_raw = validate_launch(launch_path)
            require(authenticated_raw == launch_raw and
                    checked["launch_sha256"] == sha(authenticated_raw),
                    "selftest_launch_sha_handoff")
            launch_handoff_control = True
    finally:
        globals().update({"validate_separator": saved_validators[0],
                          "validate_p1": saved_validators[1],
                          "validate_task554": saved_validators[2]})

    return {"schema": SCHEMA + ".checker-selftest", "status": "PASS", "sparse_offsets": 4,
            "simultaneous_values": 20, "vectorized_chunk_dense_crosscheck": True,
            "offset_four_slot_control": tiny_accumulator_control,
            "two_block_accumulator": tiny_accumulator_control,
            "full_scalar_eof_32280": True, "seed_first_violation": 0,
            "actor_first_violation": "basis_i/actor", "all_four_root_eof": True,
            "zero_root": True, "separator_mutation_rejected": separator_control,
            "task712_transpose_mutation_rejected": table_control,
            "p1_truncation_digest_mutation_rejected": p1_control,
            "task554_relation_order_mutation_rejected": True,
            "result_q_child_scalar_prefix_resealing_rejected": True,
            "terminal_claim_and_parent_join_rejected": True,
            "launch_sha256_handoff": launch_handoff_control,
            "dense_all_row_matrix": False, "verified": False}


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__); group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true"); group.add_argument("--check-launch", type=Path)
    return parser


def check_actual(path: Path) -> dict[str, Any]:
    base, _ = validate_launch(path); tables, vectors = covectors(base["separator"], base["task712"])
    values = p1_values(base["p1"], vectors)
    return check_output(base, tables, vectors, values)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.selftest:
            print(json.dumps(selftest(), sort_keys=True)); return 0
        print(json.dumps(check_actual(args.check_launch), sort_keys=True)); return 0
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc), "verified": False}, sort_keys=True),
              file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
