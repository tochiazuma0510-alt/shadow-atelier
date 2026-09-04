#!/usr/bin/env python3
"""R07 grade-two scalar owner.

This version owns the scalar boundary: authenticated separator/current-S
input, a topological raw dual chain, one chronological P1 pass, and the
complete scalar receipt.  Physical providers deliberately remain NOT_READY.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_SCHEMA = "d972.r07.targeted-grade2-owner-generated-join.v7"
LIVE_SCHEMA = "d972.r07.targeted-grade2.scalar-live.v15"
TASK712_MANIFEST_SHA = "48c5d1f455e775cbcb3d887248de72d6bbda9df25deb5bafb8f02c8d121bdd47"
TASK712_ARCHIVE_SHA = "sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858"
TASK712_WORKFLOW_SCHEMA = "d972.r07.grade2.forward-adjoint-maps.v4.workflow-receipt"
TASK712_CHECKER_SCHEMA = "d972.r07.grade2.forward-adjoint-maps.v3.checker"
TASK712_CHECKER_MARKER = "R07_GRADE2_FORWARD_ADJOINT_MAPS_V4_CHECKER_PASS"
TASK712_COMMIT = "5ff2c5a30b604536df12acba8801828a5a7e5fe0"
TASK712_PRODUCER_SHA = "7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84"
TASK712_CHECKER_SHA = "7ba94ee884db49bbe42d11a84228a6bdf7c88a3918407928af90c71b65fe4a29"
TASK712_WORKFLOW_RECEIPT_BYTES = 1034
TASK712_WORKFLOW_RECEIPT_SHA = "3fc967d6851b03bcb5c6d9c662c05a5c32d80028b698c925b313fa9ae9cc68c8"
TASK712_CHECKER_RECEIPT_BYTES = 1133
TASK712_CHECKER_RECEIPT_SHA = "3d9dc1a40c37a91d00b114f166128a08281badd1a4cb0735008cbd1b3e7b3160"
WORD_FILE = "scratchpad/a0_paper_words_v1.json"
WORD_SHA = "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"
WORD_RELATOR_SHA = "7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"
ACTORS = (1, -1, 2, -2)
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
P1_ROWS = 8059
P1_ROW_TRITS = 145152
P1_ROW_BYTES = 36288
SOURCE_WIDTH = 36288
SOURCE0C = 6048
SOURCE1C = 18144
SOURCE2C = 36288
PHYSICAL_WIDTH = 48384
PHYSICAL_PACKED_BYTES = 12096
SCALAR_ORIGINS = 32280
PRODUCTION_SEGMENTS = (0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059)
SEED_OO = (((1,), (2,)), ((1,), (-1, -2)), ((2,), (-1, -2)),
          ((-2, -1), (1,)), ((1,), (2,)), ((-2, -1), (2,)))
SEED_PURE_WORDS = {
    (0, 0): (),
    (0, 1): (-2, -2, -2, -2, -2, -2, -2, -2, -2),
    (1, 0): (-2, -2, 1, 1, 2, 1, 2, 1, 1),
    (1, 1): (-2, -2, -2, -1, -2, -1, -1, -1, -2, -1),
}
SEED_MONOMIALS = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                  (2, 0, 0), (1, 1, 0), (1, 0, 1), (0, 2, 0),
                  (0, 1, 1), (0, 0, 2))
SEED_MONOMIAL_INDEX = {value: index for index, value in enumerate(SEED_MONOMIALS)}
SEED_DEGREE2_PRODUCT = [[-1] * 10 for _ in range(10)]
for _left_index, _left_monomial in enumerate(SEED_MONOMIALS):
    for _right_index, _right_monomial in enumerate(SEED_MONOMIALS):
        _sum = tuple(_left_monomial[index] + _right_monomial[index]
                     for index in range(3))
        if sum(_sum) <= 2 and all(index <= 2 for index in _sum):
            SEED_DEGREE2_PRODUCT[_left_index][_right_index] = SEED_MONOMIAL_INDEX[_sum]
SEED_REGISTERED_ROW_SHA = (
    "9e123f653d0584aae0a048d94121e6a526702901d82b5d28b5f18f51a8ea4f1d",
    "de0cbf27c3adc01874f3b7af25ff70fa0c56f13e01ec4939f91b5830ee3821b8",
    "0a1c5f4aa0b49a66e2dbf0c1e659416f518a858030d47d6582b65ed2c9a30e7a",
    "ba3c0d6c6483be36d4b2a47fed1188ad35460fa9db5ff25a7312d275db706fec",
)


class NotReady(RuntimeError):
    pass


class UnknownResource(RuntimeError):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def digest_string(value: Any, reason: str) -> None:
    require(isinstance(value, str) and len(value) == 64 and
            all(x in "0123456789abcdef" for x in value), reason)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def regular(path: Path) -> os.stat_result:
    info = path.lstat()
    require(not path.is_symlink() and path.is_file(),
            "unsafe_file:" + str(path))
    return info


def read_canonical(path: Path, cap: int, reason: str) -> tuple[Any, bytes]:
    info = regular(path)
    if info.st_size > cap:
        raise UnknownResource("UNKNOWN_RESOURCE:" + reason + ":bytes")
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeError, ValueError) as exc:
        raise RuntimeError(reason + ":json") from exc
    require(canonical(value) == raw, reason + ":canonical")
    return value, raw


def read_receipt(root: Path, record: Any, cap: int, reason: str) -> bytes:
    require(isinstance(record, dict) and set(record) ==
            {"file", "bytes", "sha256"}, reason + ":receipt")
    name = record["file"]
    require(isinstance(name, str) and name and Path(name).name == name,
            reason + ":filename")
    require(plain_int(record["bytes"]) and record["bytes"] >= 0,
            reason + ":bytes")
    digest_string(record["sha256"], reason + ":digest_shape")
    if record["bytes"] > cap:
        raise UnknownResource("UNKNOWN_RESOURCE:" + reason + ":bytes")
    path = root / name
    require(regular(path).st_size == record["bytes"], reason + ":size")
    data = path.read_bytes()
    require(sha(data) == record["sha256"], reason + ":digest")
    return data


def pack_trits(row: np.ndarray) -> bytes:
    value = np.asarray(row, dtype=np.uint8).reshape(-1)
    require(value.size % 4 == 0 and not np.any(value > 2), "dense_row")
    weights = np.asarray((1, 3, 9, 27), dtype=np.uint16)
    return np.sum(value.reshape(-1, 4).astype(np.uint16) * weights,
                  axis=1).astype(np.uint8).tobytes()


def unpack_trits(raw: bytes, width: int) -> np.ndarray:
    require(type(raw) is bytes and len(raw) * 4 == width, "packed_width")
    packed = np.frombuffer(raw, dtype=np.uint8)
    require(not np.any(packed > 80), "packed_digit")
    result = np.empty(width, dtype=np.uint8)
    for index, item in enumerate(packed):
        number = int(item)
        result[4 * index:4 * index + 4] = (
            number % 3, (number // 3) % 3, (number // 9) % 3,
            (number // 27) % 3)
    return result


def dot_mod3(left: np.ndarray, right: np.ndarray) -> int:
    a = np.asarray(left, dtype=np.uint8).reshape(-1)
    b = np.asarray(right, dtype=np.uint8).reshape(-1)
    require(a.size == b.size and not np.any(a > 2) and not np.any(b > 2),
            "dot_shape")
    return int(np.sum(a.astype(np.uint16) * b.astype(np.uint16)) % 3)


def normal_terms(entries: Iterable[Iterable[int]], bound: int) -> list[list[int]]:
    values: dict[int, int] = {}
    for item in entries:
        pair = list(item)
        require(len(pair) == 2 and plain_int(pair[0]) and
                plain_int(pair[1]) and 0 <= pair[0] < bound and
                pair[1] in (1, 2), "relation_term")
        values[pair[0]] = (values.get(pair[0], 0) + pair[1]) % 3
    return [[index, values[index]] for index in sorted(values) if values[index]]


def sparse_adjoint(entries: Iterable[Iterable[int]], source_width: int,
                   destination_width: int, vector: np.ndarray) -> np.ndarray:
    value = np.asarray(vector, dtype=np.uint8).reshape(-1)
    require(value.size == destination_width and not np.any(value > 2),
            "map_adjoint_width")
    output = np.zeros(source_width, dtype=np.uint8)
    for source, destination, coefficient in entries:
        require(plain_int(source) and plain_int(destination) and
                coefficient in (1, 2), "map_entry")
        output[source] = (int(output[source]) + coefficient *
                          int(value[destination])) % 3
    return output


def _table_line(value: Iterable[int]) -> bytes:
    row = list(value)
    require(len(row) == 3 and all(plain_int(x) for x in row),
            "task712_table_entry")
    return (json.dumps(row, separators=(",", ":"), ensure_ascii=True) +
            "\n").encode("ascii")


def _read_table(path: Path, receipt: dict[str, Any]) -> list[tuple[int, int, int]]:
    data = path.read_bytes()
    require(len(data) == receipt["bytes"] and sha(data) == receipt["sha256"],
            "task712_table_digest")
    lines = data.splitlines(keepends=True)
    require(lines and all(line.endswith(b"\n") for line in lines),
            "task712_jsonl_eof")
    body = bytearray(); entries: list[tuple[int, int, int]] = []
    marker: Any = None; previous: tuple[int, int] | None = None
    for line in lines:
        value = json.loads(line.decode("ascii"))
        if isinstance(value, dict):
            require(marker is None and set(value) ==
                    {"body_bytes", "body_sha256", "count", "eof"} and
                    value["eof"] is True and canonical(value) == line,
                    "task712_table_eof")
            marker = value
            break
        require(isinstance(value, list) and len(value) == 3 and
                all(plain_int(x) for x in value), "task712_table_record")
        row = tuple(int(x) for x in value)
        require(row[2] in (1, 2) and 0 <= row[0] < receipt["source_width"] and
                0 <= row[1] < receipt["destination_width"],
                "task712_table_semantics")
        require(previous is None or row[:2] > previous, "task712_table_order")
        require(_table_line(row) == line, "task712_table_canonical")
        entries.append(row); body.extend(line); previous = row[:2]
    require(marker is not None and marker["body_bytes"] == len(body) and
            marker["count"] == len(entries) and
            marker["body_sha256"] == sha(bytes(body)), "task712_table_body")
    require(receipt["entry_count"] == len(entries) and
            receipt["body_bytes"] == len(body) and
            receipt["body_sha256"] == sha(bytes(body)) and
            receipt["eof"] is True and data == bytes(body) + canonical(marker),
            "task712_table_receipt")
    return entries


def _task712_root(value: Any) -> tuple[Path, Path]:
    require(isinstance(value, dict) and set(value) ==
            {"root", "run_id", "run_attempt", "artifact_id", "artifact_digest"},
            "task712_envelope_keys")
    require(value["run_id"] == 33814194630 and value["run_attempt"] == 1 and
            value["artifact_id"] == 9915928157 and
            value["artifact_digest"] == TASK712_ARCHIVE_SHA,
            "task712_acquisition")
    root = Path(value["root"]).absolute(); data = root / "r07-grade2-maps-v4"
    if root.name == "r07-grade2-maps-v4" and (root / "manifest.json").is_file():
        data = root; root = root.parent
    require(data.is_dir(), "task712_root")
    return root, data


def table_identity(name: str, receipt: dict[str, Any]) -> str:
    return name + ":" + receipt["sha256"]


def read_task712_envelope(value: Any, character: int) -> dict[str, Any]:
    """Authenticate the accepted workflow/checker/manifest and 10 used maps."""
    require(plain_int(character) and 0 <= character < 4, "task712_character")
    root, data = _task712_root(value)
    manifest_path = data / "manifest.json"; manifest_raw = manifest_path.read_bytes()
    require(len(manifest_raw) == 24277 and sha(manifest_raw) == TASK712_MANIFEST_SHA,
            "task712_manifest_pin")
    manifest = json.loads(manifest_raw.decode("ascii"))
    require(canonical(manifest) == manifest_raw and
            manifest.get("schema") == "d972.r07.grade2.forward-adjoint-maps.v3" and
            manifest.get("marker") == "R07_GRADE2_FORWARD_ADJOINT_MAPS_V3_CANDIDATE",
            "task712_manifest")
    workflow, workflow_raw = read_canonical(root / "r07-grade2-maps-v4-receipt.json", 1 << 20,
                                            "task712_workflow")
    checker, checker_raw = read_canonical(root / "r07-grade2-maps-v4-checker.json", 1 << 20,
                                          "task712_checker")
    require(len(workflow_raw) == TASK712_WORKFLOW_RECEIPT_BYTES and
            sha(workflow_raw) == TASK712_WORKFLOW_RECEIPT_SHA and
            len(checker_raw) == TASK712_CHECKER_RECEIPT_BYTES and
            sha(checker_raw) == TASK712_CHECKER_RECEIPT_SHA,
            "task712_receipt_file_pin")
    require(set(workflow) == {"GRADE2_DECISION", "checker", "checker_process",
            "checker_reported_elapsed_seconds", "checker_result_sha256", "claim_flags",
            "commit_sha", "entry_count", "manifest_sha256", "map_count", "producer",
            "producer_process", "producer_reported_elapsed_seconds", "run_attempt",
            "run_id", "schema", "table_count", "verified"} and
            set(workflow["producer"]) == {"bytes", "sha256"} and
            set(workflow["checker"]) == {"bytes", "sha256"} and
            set(workflow["producer_process"]) == {"elapsed", "peak_rss_kbytes"} and
            set(workflow["checker_process"]) == {"elapsed", "peak_rss_kbytes"} and
            set(workflow["claim_flags"]) == {"A0", "COMMON", "COMPATIBLE_LIFT",
                                               "FAKE", "IHARA", "independent_checker",
                                               "precision2", "verified"},
            "task712_workflow_keys")
    require(set(checker) == {"ACTUAL_MAP_BUILD", "checker_sha256", "claim_flags",
            "elapsed_seconds", "entries_checked", "GRADE2_DECISION", "marker",
            "occurrence_triples", "prefix_sha256", "producer_manifest_sha256",
            "producer_sha256", "schema", "source_dimensions", "structural_identities",
            "tables_checked", "terminal", "verified"} and
            set(checker["claim_flags"]) == {"A0", "COMMON", "COMPATIBLE_LIFT",
                                              "FAKE", "IHARA", "independent_checker",
                                              "precision2", "verified"},
            "task712_checker_keys")
    workflow_flags = {"A0": False, "COMMON": False, "COMPATIBLE_LIFT": False,
                      "FAKE": False, "IHARA": False, "independent_checker": False,
                      "precision2": False, "verified": False}
    require(workflow.get("schema") == TASK712_WORKFLOW_SCHEMA and
            workflow.get("run_id") == 33814194630 and workflow.get("run_attempt") == 1 and
            workflow.get("commit_sha") == TASK712_COMMIT and
            workflow.get("manifest_sha256") == TASK712_MANIFEST_SHA and
            workflow.get("producer") == {"bytes": 46179, "sha256": TASK712_PRODUCER_SHA} and
            workflow.get("checker") == {"bytes": 49643, "sha256": TASK712_CHECKER_SHA} and
            workflow.get("checker_result_sha256") == sha(checker_raw) and
            workflow.get("GRADE2_DECISION") == "NOT_RUN" and
            workflow.get("entry_count") == 1451520 and workflow.get("table_count") == 40 and
            workflow.get("map_count") == 20 and workflow.get("producer_process") ==
            {"elapsed": "09.57", "peak_rss_kbytes": 139692} and
            workflow.get("checker_process") ==
            {"elapsed": "19.53", "peak_rss_kbytes": 243244} and
            workflow.get("producer_reported_elapsed_seconds") == 9.29909895999998 and
            workflow.get("checker_reported_elapsed_seconds") == 19.272781078999998 and
            workflow.get("claim_flags") == workflow_flags and
            workflow.get("verified") is False,
            "task712_workflow")
    checker_flags = dict(workflow_flags)
    require(checker.get("schema") == TASK712_CHECKER_SCHEMA and
            checker.get("terminal") == TASK712_CHECKER_MARKER and
            checker.get("producer_manifest_sha256") == TASK712_MANIFEST_SHA and
            checker.get("checker_sha256") == TASK712_CHECKER_SHA,
            "task712_checker")
    require(checker.get("ACTUAL_MAP_BUILD") == "DEFERRED_TO_GHA" and
            checker.get("GRADE2_DECISION") == "NOT_RUN" and
            checker.get("entries_checked") == 1451520 and
            checker.get("tables_checked") == 40 and
            checker.get("elapsed_seconds") == 19.272781078999998 and
            checker.get("prefix_sha256") ==
            "03803203943dd9179608e5cbe1c5a6e0adf41a7722eb66bdbe81fb263a14f30c" and
            checker.get("producer_sha256") == TASK712_PRODUCER_SHA and
            checker.get("occurrence_triples") ==
            [[0, 0, 1], [1, 0, 2], [2, 0, 1], [3, 1, 2], [4, 1, 2], [5, 1, 1]] and
            checker.get("source_dimensions") == {"P": 48384, "V_a": 36288} and
            checker.get("structural_identities") ==
            {"B_occurrence_first": True, "all_cases_visited": True,
             "canonical_entry_legal": True, "inverse_source_coordinates": 290304,
             "transpose_entries": 725760} and checker.get("claim_flags") == checker_flags and
            checker.get("verified") is False,
            "task712_checker_semantics")
    expected_roster = ["manifest.json", "producer.marker"]
    for roster_character in range(4):
        for roster_slot in range(4):
            expected_roster.extend([
                f"T_fwd_a{roster_character}_t{roster_slot}.jsonl",
                f"T_adj_a{roster_character}_t{roster_slot}.jsonl"])
        expected_roster.extend([f"B_fwd_a{roster_character}.jsonl",
                                f"B_adj_a{roster_character}.jsonl"])
    roster = manifest.get("output_roster")
    require(roster == expected_roster and
            set(roster) == {p.name for p in data.iterdir()},
            "task712_roster")
    require(isinstance(manifest.get("tables"), list) and
            [item.get("file") for item in manifest["tables"]] == expected_roster[2:],
            "task712_table_order")
    by_name = {x.get("file"): x for x in manifest.get("tables", [])
               if isinstance(x, dict)}
    require(len(by_name) == 40, "task712_table_roster")
    wanted = ([f"B_fwd_a{character}.jsonl"] +
              [f"T_fwd_a{character}_t{slot}.jsonl" for slot in range(4)] +
              [f"B_adj_a{character}.jsonl"] +
              [f"T_adj_a{character}_t{slot}.jsonl" for slot in range(4)])
    output: dict[str, Any] = {"root": root, "data": data,
        "manifest_raw": manifest_raw, "manifest_sha256": sha(manifest_raw),
        "forward": {}, "adjoint": {}, "identity": {}, "receipts": {}}
    for name in wanted:
        record = by_name.get(name); require(isinstance(record, dict),
                                            "task712_used_receipt")
        is_b = name.startswith("B_")
        keys = {"file", "schema", "source_width", "destination_width", "entry_count",
                "body_bytes", "body_sha256", "bytes", "sha256", "eof", "encoding",
                "map_kind", "map_direction", "character"}
        if not is_b: keys.add("actor")
        require(set(record) == keys and record["file"] == name and
                record["schema"] == "d972.r07.grade2.forward-adjoint-maps.v3.sparse-jsonl" and
                record["encoding"] == "jsonl-triples-utf8-lf" and
                record["map_kind"] == ("B" if is_b else "T") and
                record["map_direction"] == ("forward" if "_fwd_" in name else "adjoint") and
                record["character"] == character, "task712_receipt_semantics")
        if is_b:
            require(record["source_width"] == (SOURCE_WIDTH if "_fwd_" in name
                                                else PHYSICAL_WIDTH) and
                    record["destination_width"] == (PHYSICAL_WIDTH if "_fwd_" in name
                                                      else SOURCE_WIDTH),
                    "task712_B_dimensions")
            key: Any = "B"
        else:
            actor = record["actor"]
            require(plain_int(actor) and actor in ACTORS and
                    name.endswith(f"_t{ACTORS.index(actor)}.jsonl") and
                    record["source_width"] == SOURCE_WIDTH and
                    record["destination_width"] == SOURCE_WIDTH,
                    "task712_T_dimensions")
            key = actor
        entries = _read_table(data / name, record)
        direction = "forward" if "_fwd_" in name else "adjoint"
        output[direction][key] = entries; output["receipts"][name] = record
        output["identity"][direction + ":" + str(key)] = table_identity(name, record)
        SCALAR_CALLS["task712_tables"] += 1
    require(set(output["forward"]) == {"B", *ACTORS} and
            set(output["adjoint"]) == {"B", *ACTORS}, "task712_used_roster")
    for key in output["forward"]:
        expected = sorted((d, s, c) for s, d, c in output["forward"][key])
        require(output["adjoint"][key] == expected, "task712_adjoint_transpose")
    output["envelope"] = dict(value); return output


def _load_words() -> dict[str, Any]:
    raw = (PROJECT_ROOT / WORD_FILE).read_bytes()
    require(len(raw) == 115928 and sha(raw) == WORD_SHA, "word_input_pin")
    words = json.loads(raw.decode("ascii"))
    require(isinstance(words, dict) and isinstance(words.get("relators"), list) and
            len(words["relators"]) == 44 and isinstance(words.get("g760"), list) and
            len(words["g760"]) == 760, "word_input_shape")
    relator_raw = json.dumps(words["relators"], sort_keys=True,
                             separators=(",", ":")).encode("ascii")
    require(words.get("relators_sha256") == WORD_RELATOR_SHA and
            sha(relator_raw) == WORD_RELATOR_SHA, "word_relator_pin")
    return words


SEED_ID9 = tuple(range(9))
SEED_AFFINE_IDENTITY = (SEED_ID9, 0, 0, (0, 0, 0))


def _seed_perm_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(right[left[index]] for index in range(len(left)))


def _seed_perm_inv(value: tuple[int, ...]) -> tuple[int, ...]:
    output = [0] * len(value)
    for index, image in enumerate(value):
        output[image] = index
    return tuple(output)


def _seed_word_inverse(word: Iterable[int]) -> tuple[int, ...]:
    return tuple(-int(value) for value in reversed(tuple(word)))


def _seed_word_multiply(*words: Iterable[int]) -> tuple[int, ...]:
    output: list[int] = []
    for word in words:
        for value in word:
            value = int(value)
            if output and output[-1] == -value:
                output.pop()
            else:
                output.append(value)
    return tuple(output)


def _seed_substitute(word: Iterable[int], x: Iterable[int],
                     y: Iterable[int]) -> tuple[int, ...]:
    xx, yy = tuple(x), tuple(y)
    return _seed_word_multiply(*(
        xx if value == 1 else yy if value == 2 else
        _seed_word_inverse(xx) if value == -1 else _seed_word_inverse(yy)
        for value in word))


def _seed_qmul(left: tuple[tuple[int, ...], int, int],
               right: tuple[tuple[int, ...], int, int]) -> tuple[tuple[int, ...], int, int]:
    return (_seed_perm_mul(left[0], right[0]), left[1] ^ right[1],
            left[2] ^ right[2])


def _seed_qinv(value: tuple[tuple[int, ...], int, int]) -> tuple[tuple[int, ...], int, int]:
    return (_seed_perm_inv(value[0]), value[1], value[2])


def _seed_qeval(word: Iterable[int], images: tuple[tuple[tuple[int, ...], int, int],
                                                     tuple[tuple[int, ...], int, int]]) -> tuple[tuple[int, ...], int, int]:
    result = (SEED_ID9, 0, 0)
    for value in word:
        image = images[abs(int(value)) - 1]
        result = _seed_qmul(result, image if value > 0 else _seed_qinv(image))
    return result


SeedAffine = tuple[tuple[int, ...], int, int, tuple[int, int, int]]


def _seed_cv(label: tuple[int, int], parity: tuple[int, int]) -> int:
    return 1 if ((label[0] * parity[0] + label[1] * parity[1]) & 1) == 0 else 2


def _seed_sign_kernel(parity: tuple[int, int], value: tuple[int, int, int]) -> tuple[int, int, int]:
    eta = ((0, 1), (1, 0), (1, 1))
    return tuple((_seed_cv(eta[index], parity) * value[index]) % 3
                 for index in range(3))


def _seed_affine_mul(left: SeedAffine, right: SeedAffine) -> SeedAffine:
    acted = _seed_sign_kernel((right[1], right[2]), left[3])
    return (_seed_perm_mul(left[0], right[0]), left[1] ^ right[1],
            left[2] ^ right[2], tuple((acted[index] + right[3][index]) % 3
                                       for index in range(3)))


def _seed_affine_inv(value: SeedAffine) -> SeedAffine:
    acted = _seed_sign_kernel((value[1], value[2]), value[3])
    return (_seed_perm_inv(value[0]), value[1], value[2],
            tuple((-entry) % 3 for entry in acted))


def _seed_affine_eval(word: Iterable[int], images: tuple[SeedAffine, SeedAffine]) -> SeedAffine:
    result = SEED_AFFINE_IDENTITY
    inverses = _seed_affine_inv(images[0]), _seed_affine_inv(images[1])
    for value in word:
        result = _seed_affine_mul(
            result, images[abs(int(value)) - 1] if value > 0 else
            inverses[abs(int(value)) - 1])
    return result


def _seed_affine_fox(word: Iterable[int], images: tuple[SeedAffine, SeedAffine]) -> tuple[dict[tuple[int, SeedAffine], int], SeedAffine]:
    output: dict[tuple[int, SeedAffine], int] = {}
    prefix = SEED_AFFINE_IDENTITY
    inverses = _seed_affine_inv(images[0]), _seed_affine_inv(images[1])
    for value in word:
        generator = abs(int(value)) - 1
        if value > 0:
            key = generator, prefix
            output[key] = (output.get(key, 0) + 1) % 3
            prefix = _seed_affine_mul(prefix, images[generator])
        else:
            prefix = _seed_affine_mul(prefix, inverses[generator])
            key = generator, prefix
            output[key] = (output.get(key, 0) - 1) % 3
        if output.get(key) == 0:
            output.pop(key, None)
    return output, prefix


def _seed_group(generators: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[tuple[tuple[int, ...], ...], dict[tuple[int, ...], int]]:
    elements: list[tuple[int, ...]] = [SEED_ID9]
    positions = {SEED_ID9: 0}
    steps = (generators[0], generators[1], _seed_perm_inv(generators[0]),
             _seed_perm_inv(generators[1]))
    cursor = 0
    while cursor < len(elements):
        parent = elements[cursor]; cursor += 1
        for generator in steps:
            value = _seed_perm_mul(parent, generator)
            if value not in positions:
                positions[value] = len(elements); elements.append(value)
    return tuple(elements), positions


def _seed_matrix2_mul(left: tuple[tuple[int, int], tuple[int, int]],
                      right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (left[0][0] * right[0][0] ^ left[0][1] * right[1][0],
         left[0][0] * right[0][1] ^ left[0][1] * right[1][1]),
        (left[1][0] * right[0][0] ^ left[1][1] * right[1][0],
         left[1][0] * right[0][1] ^ left[1][1] * right[1][1]),
    )


class _SeedContext:
    def __init__(self, words: dict[str, Any]):
        text = (PROJECT_ROOT / "scratchpad/fuda1_a0_rmax_data.g").read_text(
            encoding="utf-8")
        match = re.search(r"FUDA1_Q0PERMS\s*:=\s*\[\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\]\s*;;",
                          text, re.S)
        require(match is not None, "seed_marking")
        q36 = tuple(tuple(value - 1 for value in ast.literal_eval(match.group(index)))
                     for index in (1, 2))
        self.a, self.c = q36[0][:9], q36[1][:9]
        self.psels, self.psidx = _seed_group((self.a, self.c))
        require(len(self.psels) == 504, "seed_psl_order")
        self.q1_images = ((self.a, 1, 0), (self.c, 0, 1))
        self.images: tuple[SeedAffine, SeedAffine] = (
            (self.a, 1, 0, (1, 0, 0)),
            (self.c, 0, 1, (1, 1, 1)),
        )
        self.pb3_b = _seed_affine_inv(
            _seed_affine_mul(self.images[1], self.images[0]))
        self.transport: list[dict[tuple[int, int], tuple[int, int]]] = []
        for left_word, right_word in SEED_OO:
            left = _seed_qeval(left_word, self.q1_images)
            right = _seed_qeval(right_word, self.q1_images)
            action = ((left[1], right[1]), (left[2], right[2]))
            inverse = None
            for aa in range(2):
                for ab in range(2):
                    for ba in range(2):
                        for bb in range(2):
                            candidate = ((aa, ab), (ba, bb))
                            identity = ((1, 0), (0, 1))
                            if (_seed_matrix2_mul(action, candidate) == identity and
                                    _seed_matrix2_mul(candidate, action) == identity):
                                inverse = candidate
            require(inverse is not None, "seed_transport")
            self.transport.append({
                label: (label[0] * inverse[0][0] ^ label[1] * inverse[1][0],
                        label[0] * inverse[0][1] ^ label[1] * inverse[1][1])
                for label in CHARACTERS
            })
        self.pure_tags = {
            parity: tuple(_seed_affine_eval(
                _seed_substitute(SEED_PURE_WORDS[parity], *pair), self.images)
                for pair in SEED_OO)
            for parity in CHARACTERS
        }
        self.maps: dict[tuple[int, ...], np.ndarray] = {}

    def pmap(self, permutation: tuple[int, ...]) -> np.ndarray:
        if permutation not in self.maps:
            self.maps[permutation] = np.asarray(
                [self.psidx[_seed_perm_mul(permutation, value)]
                 for value in self.psels], dtype=np.int32)
        return self.maps[permutation]


def _seed_poly_mul(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    output = np.zeros(10, dtype=np.uint8)
    for i in np.flatnonzero(left):
        for j in np.flatnonzero(right):
            target = SEED_DEGREE2_PRODUCT[int(i)][int(j)]
            if target >= 0:
                output[target] = (int(output[target]) + int(left[i]) * int(right[j])) % 3
    return output


def _seed_e_poly(vector: tuple[int, int, int]) -> np.ndarray:
    output = np.zeros(10, dtype=np.uint8); output[0] = 1
    for variable, exponent0 in enumerate(vector):
        exponent = exponent0 % 3
        factor = np.zeros(10, dtype=np.uint8); factor[0] = 1
        if exponent:
            mono = [0, 0, 0]; mono[variable] = 1
            factor[SEED_MONOMIAL_INDEX[tuple(mono)]] = exponent
        if exponent == 2:
            mono = [0, 0, 0]; mono[variable] = 2
            factor[SEED_MONOMIAL_INDEX[tuple(mono)]] = 1
        output = _seed_poly_mul(output, factor)
    return output


def _seed_poly_rows_mul(factor: np.ndarray, rows: np.ndarray) -> np.ndarray:
    output = np.zeros_like(rows)
    for left in np.flatnonzero(factor):
        for right in range(10):
            target = SEED_DEGREE2_PRODUCT[int(left)][right]
            if target >= 0:
                output[:, target] = (output[:, target].astype(np.uint16) +
                                     int(factor[left]) * rows[:, right].astype(np.uint16)) % 3
    return output.astype(np.uint8)


def _seed_lower_coord(tag: int, component: int, psl: int) -> int:
    return (tag * 2 + component) * 504 + psl


def _seed_grade1_coord(tag: int, component: int, monomial: int, psl: int) -> int:
    return ((tag * 2 + component) * 3 + monomial) * 504 + psl


def _seed_source_view(d0: np.ndarray, d1: np.ndarray, d2: np.ndarray,
                      character: int, tag: int) -> np.ndarray:
    output = np.zeros((2, 10, 504), dtype=np.uint8)
    for component in (0, 1):
        output[component, 0] = d0[character,
                                  _seed_lower_coord(tag, component, 0):
                                  _seed_lower_coord(tag, component, 0) + 504]
        for monomial in range(3):
            begin = _seed_grade1_coord(tag, component, monomial, 0)
            output[component, 1 + monomial] = d1[character, begin:begin + 504]
        for monomial in range(6):
            begin = ((tag * 2 + component) * 6 + monomial) * 504
            output[component, 4 + monomial] = d2[character, begin:begin + 504]
    return output


def _seed_install_view(d0: np.ndarray, d1: np.ndarray, d2: np.ndarray,
                       character: int, tag: int, value: np.ndarray) -> None:
    for component in (0, 1):
        begin = _seed_lower_coord(tag, component, 0)
        d0[character, begin:begin + 504] = value[component, 0]
        for monomial in range(3):
            begin = _seed_grade1_coord(tag, component, monomial, 0)
            d1[character, begin:begin + 504] = value[component, 1 + monomial]
        for monomial in range(6):
            begin = ((tag * 2 + component) * 6 + monomial) * 504
            d2[character, begin:begin + 504] = value[component, 4 + monomial]


def _seed_act(context: _SeedContext,
              row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
              tag_actors: tuple[SeedAffine, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d0, d1, d2, auxiliary = row
    output = (np.zeros_like(d0), np.zeros_like(d1), np.zeros_like(d2),
              auxiliary.copy())
    for tag, actor in enumerate(tag_actors):
        raw = np.zeros((4, 2, 10, 504), dtype=np.uint8)
        for parity_index, parity in enumerate(CHARACTERS):
            for source_index, source_label in enumerate(CHARACTERS):
                raw[parity_index] = (raw[parity_index].astype(np.uint16) +
                    _seed_cv(context.transport[tag][source_label], parity) *
                    _seed_source_view(d0, d1, d2, source_index, tag).astype(np.uint16)) % 3
        acted = np.zeros_like(raw)
        pmap = context.pmap(actor[0])
        for parity_index, parity in enumerate(CHARACTERS):
            target = (parity[0] ^ actor[1], parity[1] ^ actor[2])
            product = _seed_poly_rows_mul(
                _seed_e_poly(_seed_sign_kernel(parity, actor[3])), raw[parity_index])
            translated = np.zeros_like(product)
            translated[:, :, pmap] = product
            acted[CHARACTERS.index(target)] = (
                acted[CHARACTERS.index(target)].astype(np.uint16) +
                translated.astype(np.uint16)) % 3
        for source_index, source_label in enumerate(CHARACTERS):
            value = np.zeros((2, 10, 504), dtype=np.uint8)
            tag_label = context.transport[tag][source_label]
            for parity_index, parity in enumerate(CHARACTERS):
                value = (value.astype(np.uint16) +
                         _seed_cv(tag_label, parity) *
                         acted[parity_index].astype(np.uint16)) % 3
            _seed_install_view(output[0], output[1], output[2], source_index,
                               tag, value.astype(np.uint8))
    return output


def _seed_qnorm(word: tuple[int, ...], context: _SeedContext) -> tuple[list[tuple[int, SeedAffine, int]], int]:
    gradient, endpoint = _seed_affine_fox(word, context.images)
    require(endpoint == SEED_AFFINE_IDENTITY, "seed_endpoint")
    output: dict[tuple[int, SeedAffine], int] = {}
    augmentation = 0
    for (generator, prefix), coefficient in gradient.items():
        if generator == 0:
            augmentation = (augmentation + coefficient) % 3
            first = _seed_affine_mul(prefix, context.images[0])
            second = _seed_affine_mul(first, context.pb3_b)
            for component, value in ((0, first), (1, second)):
                key = component, value
                output[key] = (output.get(key, 0) - coefficient) % 3
        else:
            key = 1, prefix
            output[key] = (output.get(key, 0) + coefficient) % 3
    return [(component, value, coefficient) for (component, value), coefficient in output.items()
            if coefficient], augmentation


def _seed_evaluate_seed(context: _SeedContext, word: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d0 = np.zeros((4, SOURCE0C), dtype=np.uint8)
    d1 = np.zeros((4, SOURCE1C), dtype=np.uint8)
    d2 = np.zeros((4, SOURCE2C), dtype=np.uint8)
    auxiliary = np.zeros(8, dtype=np.uint8)
    for tag, pair in enumerate(SEED_OO):
        normal, augmentation = _seed_qnorm(
            _seed_substitute(word, *pair), context)
        auxiliary[tag] = augmentation
        for component, value, coefficient in normal:
            polynomial = _seed_e_poly(value[3]); psl = context.psidx[value[0]]
            for character, label in enumerate(CHARACTERS):
                weight = coefficient * _seed_cv(
                    context.transport[tag][label], (value[1], value[2]))
                begin = _seed_lower_coord(tag, component, psl)
                d0[character, begin] = (int(d0[character, begin]) +
                    weight * int(polynomial[0])) % 3
                for monomial in range(3):
                    coordinate = _seed_grade1_coord(tag, component, monomial, psl)
                    d1[character, coordinate] = (int(d1[character, coordinate]) +
                        weight * int(polynomial[1 + monomial])) % 3
                for monomial in range(6):
                    coordinate = ((tag * 2 + component) * 6 + monomial) * 504 + psl
                    d2[character, coordinate] = (int(d2[character, coordinate]) +
                        weight * int(polynomial[4 + monomial])) % 3
    exponent = (sum(1 if value == 1 else -1 if value == -1 else 0 for value in word),
                sum(1 if value == 2 else -1 if value == -2 else 0 for value in word))
    require(exponent[0] % 18 == 0 and exponent[1] % 18 == 0, "seed_integral_exponent")
    auxiliary[6:] = (exponent[0] // 18 % 3, exponent[1] // 18 % 3)
    return d0, d1, d2, auxiliary


def _seed_full_project(context: _SeedContext,
                       row: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
                       label: tuple[int, int]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    output = tuple(np.zeros_like(part) for part in row)
    for parity in CHARACTERS:
        acted = _seed_act(context, row, context.pure_tags[parity])
        for destination, source in zip(output, acted):
            destination[:] = (destination.astype(np.uint16) +
                              _seed_cv(label, parity) * source.astype(np.uint16)) % 3
    return output  # type: ignore[return-value]


def direct_seed_rows(q: np.ndarray, character: int) -> list[np.ndarray]:
    """Generate the registered affine-Fox/projected degree-two seed rows."""
    words = _load_words(); value = np.asarray(q, dtype=np.uint8).reshape(-1)
    require(value.size == SOURCE_WIDTH and 0 <= character < 4, "seed_q_width")
    context = _SeedContext(words); rows: list[np.ndarray] = []
    for relator in words["relators"]:
        seed = _seed_evaluate_seed(context, tuple(int(x) for x in relator))
        projected = _seed_full_project(context, seed, CHARACTERS[character])
        rows.append(projected[2][character].copy())
    require(len(rows) == 44 and sha(b"".join(row.tobytes() for row in rows)) ==
            SEED_REGISTERED_ROW_SHA[character], "seed_registered_semantics")
    return rows


def direct_seed_evaluations(q: np.ndarray, character: int) -> list[int]:
    rows = direct_seed_rows(q, character)
    value = np.asarray(q, dtype=np.uint8).reshape(-1)
    return [dot_mod3(value, row) for row in rows]


def _fixture_universe(value: Any) -> dict[str, Any]:
    keys = {"schema", "fixture", "rows", "p1_row_trits", "p1_row_bytes",
            "segment_order", "old_ranks", "new_ranks", "scalar_origins"}
    require(isinstance(value, dict) and set(value) == keys and
            value["schema"] == LIVE_SCHEMA + ".reader-boundary.v1" and
            value["fixture"] is True, "reader_boundary_keys")
    require(value["rows"] == 16 and value["p1_row_trits"] == P1_ROW_TRITS and
            value["p1_row_bytes"] == P1_ROW_BYTES and
            value["segment_order"] == [0, 2, 4, 6, 8, 10, 12, 14, 16] and
            value["old_ranks"] == [2, 2, 2, 2] and value["new_ranks"] == [2, 2, 2, 2] and
            value["scalar_origins"] == 108, "reader_boundary_shape")
    return {"fixture": True, "rows": 16, "row_trits": P1_ROW_TRITS,
            "row_bytes": P1_ROW_BYTES, "segments": (0, 2, 4, 6, 8, 10, 12, 14, 16),
            "old_ranks": (2, 2, 2, 2), "new_ranks": (2, 2, 2, 2), "scalar_origins": 108}


def _production_universe() -> dict[str, Any]:
    return {"fixture": False, "rows": P1_ROWS, "row_trits": P1_ROW_TRITS,
            "row_bytes": P1_ROW_BYTES, "segments": PRODUCTION_SEGMENTS,
            "old_ranks": (505, 503, 503, 503), "new_ranks": (1509, 1512, 1512, 1512),
            "scalar_origins": SCALAR_ORIGINS}


def _validate_caps(value: Any) -> dict[str, int]:
    required = {"manifest_bytes", "rho2_durable_bytes", "p1_durable_bytes",
                "task554_durable_bytes", "instruction_bytes", "resident_bytes"}
    require(isinstance(value, dict) and set(value) == required, "caps_keys")
    result: dict[str, int] = {}
    for key in required:
        require(plain_int(value[key]) and value[key] >= 0, "cap:" + key)
        result[key] = int(value[key])
    return result


def _fixture_json_receipt(root: Path, name: str,
                          data: bytes) -> dict[str, Any]:
    path = root / name
    path.write_bytes(data)
    return {"file": name, "bytes": len(data), "sha256": sha(data)}


def _validate_fixture_rho2(parent: Any) -> dict[str, Any]:
    require(isinstance(parent, dict) and set(parent) ==
            {"schema", "root", "manifest", "files"} and
            parent["schema"] == LIVE_SCHEMA + ".rho2.fixture.v1",
            "rho2_fixture_parent")
    root = Path(parent["root"]).absolute()
    manifest, raw = read_canonical(root / parent["manifest"]["file"],
                                   1 << 20, "rho2_fixture_manifest")
    require(set(manifest) == {"schema", "width", "packed_bytes", "rho2",
                              "files"} and manifest["schema"] ==
            LIVE_SCHEMA + ".rho2-manifest.v1" and manifest["width"] ==
            PHYSICAL_WIDTH and manifest["packed_bytes"] == PHYSICAL_PACKED_BYTES,
            "rho2_fixture_manifest_shape")
    require(parent["manifest"] == {"file": parent["manifest"]["file"],
            "bytes": len(raw), "sha256": sha(raw)},
            "rho2_fixture_manifest_receipt")
    require(isinstance(parent["files"], list) and len(parent["files"]) == 1 and
            parent["files"][0] == manifest["files"][0], "rho2_fixture_files")
    packed = read_receipt(root, parent["files"][0], PHYSICAL_PACKED_BYTES,
                          "rho2_fixture_payload")
    dense = unpack_trits(packed, PHYSICAL_WIDTH)
    require(manifest["rho2"] == {"sha256": sha(packed), "pairing_target": 1},
            "rho2_fixture_digest")
    return {"root": root, "manifest": manifest, "manifest_sha256": sha(raw),
            "dense": dense, "packed": packed}


def _validate_fixture_p1(parent: Any, universe: dict[str, Any],
                         caps: dict[str, int]) -> dict[str, Any]:
    require(isinstance(parent, dict) and set(parent) ==
            {"schema", "root", "manifest", "files"} and
            parent["schema"] == LIVE_SCHEMA + ".p1.fixture.v1",
            "p1_fixture_parent")
    root = Path(parent["root"]).absolute()
    manifest, raw = read_canonical(root / parent["manifest"]["file"],
                                   caps["manifest_bytes"], "p1_fixture_manifest")
    require(set(manifest) == {"schema", "rows", "row_trits", "row_bytes",
                              "cache", "instruction", "ancestry_sha256"} and
            manifest["schema"] == LIVE_SCHEMA + ".p1-manifest.v1" and
            manifest["rows"] == universe["rows"] and
            manifest["row_trits"] == P1_ROW_TRITS and
            manifest["row_bytes"] == P1_ROW_BYTES,
            "p1_fixture_manifest_shape")
    require(parent["manifest"] == {"file": parent["manifest"]["file"],
            "bytes": len(raw), "sha256": sha(raw)},
            "p1_fixture_manifest_receipt")
    cache = manifest["cache"]; instruction = manifest["instruction"]
    require(set(cache) == {"path", "rows", "bytes", "sha256", "final_lf", "eof"} and
            set(instruction) == {"path", "rows", "bytes", "sha256", "final_lf",
                                 "eof", "final_head"} and
            cache["path"] == "degree2.cache.bin" and
            instruction["path"] == "instructions.jsonl" and
            cache["rows"] == universe["rows"] and
            instruction["rows"] == universe["rows"] and cache["eof"] is True and
            instruction["eof"] is True and instruction["final_lf"] is True,
            "p1_fixture_headers")
    expected_files = [{"file": cache["path"], "bytes": cache["bytes"],
                       "sha256": cache["sha256"]},
                      {"file": instruction["path"], "bytes": instruction["bytes"],
                       "sha256": instruction["sha256"]}]
    require(sorted(parent["files"], key=lambda x: x["file"]) ==
            sorted(expected_files, key=lambda x: x["file"]),
            "p1_fixture_file_roster")
    require(regular(root / cache["path"]).st_size == cache["bytes"] and
            regular(root / instruction["path"]).st_size == instruction["bytes"],
            "p1_fixture_file_size")
    return {"root": root, "manifest": manifest, "manifest_raw": raw,
            "manifest_sha256": sha(raw), "universe": universe}


def _validate_fixture_state(state: Any, root_hint: Path, index: int,
                            universe: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(state, dict) and set(state) ==
            {"root", "head", "body", "files"}, "task554_fixture_state")
    root = Path(state["root"]).absolute()
    require(root == root_hint and isinstance(state["files"], list) and
            len(state["files"]) == 2, "task554_fixture_root")
    body_raw = read_receipt(root, state["body"], 1 << 28,
                            "task554_fixture_body")
    head_raw = read_receipt(root, state["head"], 1 << 20,
                            "task554_fixture_head")
    require(state["body"] in state["files"] and state["head"] in state["files"],
            "task554_fixture_roster")
    body = json.loads(body_raw.decode("ascii")); head = json.loads(head_raw.decode("ascii"))
    require(canonical(body) == body_raw and canonical(head) == head_raw and
            head == {"schema": LIVE_SCHEMA + ".task554-head.v1", "index": index,
                     "body_sha256": sha(body_raw)}, "task554_fixture_head_binding")
    origin_count = sum(44 + 4 * rank for rank in universe["old_ranks"])
    if index == -1:
        require(set(body) == {"schema", "phase", "old_blocks", "defect_origins",
                              "packets"} and body["phase"] == "prepare" and
                len(body["old_blocks"]) == 4 and len(body["defect_origins"]) ==
                origin_count, "task554_fixture_prepare")
    else:
        require(set(body) == {"schema", "phase", "character_index", "character",
                              "rank", "origin_count", "origin_reductions",
                              "actor_transitions"} and body["phase"] == "block" and
                body["character_index"] == index and body["rank"] ==
                universe["new_ranks"][index] and body["origin_count"] ==
                origin_count, "task554_fixture_block")
    return {"root": root, "head": head, "body": body,
            "body_sha256": sha(body_raw), "files": state["files"], "index": index}


def _validate_fixture_task554(parent: Any, universe: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(parent, dict) and set(parent) ==
            {"schema", "source_run", "source_attempt", "source_head",
             "prepare", "blocks"} and parent["schema"] ==
            LIVE_SCHEMA + ".task554-parent.v1" and isinstance(parent["blocks"], list) and
            len(parent["blocks"]) == 4, "task554_fixture_parent")
    root = Path(parent["prepare"]["root"]).absolute()
    prepare = _validate_fixture_state(parent["prepare"], root, -1, universe)
    blocks = [_validate_fixture_state(state, root, index, universe)
              for index, state in enumerate(parent["blocks"])]
    return {"root": root, "prepare": prepare, "blocks": blocks,
            "source_run": parent["source_run"],
            "source_attempt": parent["source_attempt"],
            "source_head": parent["source_head"], "universe": universe}


def validate_base_launch(path: Path) -> dict[str, Any]:
    launch, raw = read_canonical(path, 1 << 24, "base_launch")
    fixture = "reader_boundary" in launch
    expected = {"schema", "rho2_parent", "p1_parent", "task554_parent", "caps"}
    if fixture:
        expected.add("reader_boundary")
    require(launch.get("schema") == BASE_SCHEMA and set(launch) == expected,
            "base_launch_schema")
    caps = _validate_caps(launch["caps"])
    universe = (_fixture_universe(launch["reader_boundary"])
                if fixture else _production_universe())
    if not fixture:
        raise NotReady("NOT_READY:parent.p1")
    rho2 = _validate_fixture_rho2(launch["rho2_parent"])
    p1 = _validate_fixture_p1(launch["p1_parent"], universe, caps)
    task554 = _validate_fixture_task554(launch["task554_parent"], universe)
    return {"launch": launch, "launch_raw": raw, "launch_sha256": sha(raw),
            "caps": caps, "universe": universe, "rho2": rho2, "p1": p1,
            "task554": task554}


def validate_separator_parent(parent: Any, base: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(parent, dict) and set(parent) ==
            {"schema", "root", "manifest", "files"} and
            parent["schema"] == LIVE_SCHEMA + ".separator-parent.v1",
            "separator_parent_keys")
    root = Path(parent["root"]).absolute()
    manifest, raw = read_canonical(root / parent["manifest"]["file"],
                                   base["caps"]["manifest_bytes"], "separator_manifest")
    keys = {"schema", "base_launch_sha256", "generation", "row_count", "row_width",
            "row_bytes", "order", "current_s", "lambda", "rolling_s_head", "eof"}
    require(set(manifest) == keys and manifest["schema"] ==
            LIVE_SCHEMA + ".separator-manifest.v1" and
            manifest["base_launch_sha256"] == base["launch_sha256"] and
            plain_int(manifest["generation"]) and manifest["generation"] >= 0 and
            plain_int(manifest["row_count"]) and manifest["row_count"] >= 1 and
            manifest["row_width"] == PHYSICAL_WIDTH and
            manifest["row_bytes"] == PHYSICAL_PACKED_BYTES and
            manifest["order"] == "packed-row-major" and manifest["eof"] is True,
            "separator_manifest_shape")
    require(parent["manifest"] == {"file": parent["manifest"]["file"],
            "bytes": len(raw), "sha256": sha(raw)}, "separator_manifest_receipt")
    current = manifest["current_s"]; lam_rec = manifest["lambda"]
    require(set(current) == {"file", "bytes", "sha256", "rows", "row_width", "row_bytes", "eof"} and
            current["rows"] == manifest["row_count"] and current["row_width"] == PHYSICAL_WIDTH and
            current["row_bytes"] == PHYSICAL_PACKED_BYTES and current["eof"] is True and
            set(lam_rec) == {"file", "bytes", "sha256"} and
            lam_rec["bytes"] == PHYSICAL_PACKED_BYTES, "separator_stream_receipts")
    expected_files = [{"file": current["file"], "bytes": current["bytes"],
                       "sha256": current["sha256"]}, lam_rec]
    require(sorted(parent["files"], key=lambda x: x["file"]) ==
            sorted(expected_files, key=lambda x: x["file"]), "separator_file_roster")
    lam_raw = read_receipt(root, lam_rec, base["caps"]["rho2_durable_bytes"],
                           "separator_lambda")
    lam = unpack_trits(lam_raw, PHYSICAL_WIDTH)
    require(current["bytes"] == current["rows"] * PHYSICAL_PACKED_BYTES,
            "separator_current_s_size")
    if current["bytes"] > base["caps"]["rho2_durable_bytes"]:
        raise UnknownResource("UNKNOWN_RESOURCE:separator_current_s:bytes")
    current_path = root / current["file"]; info = regular(current_path)
    require(info.st_size == current["bytes"], "separator_current_s_size")
    rolling = b"\0" * 32; current_hash = hashlib.sha256()
    with current_path.open("rb") as stream:
        for _index in range(current["rows"]):
            packed = stream.read(PHYSICAL_PACKED_BYTES)
            require(len(packed) == PHYSICAL_PACKED_BYTES,
                    "separator_current_s_eof")
            row = unpack_trits(packed, PHYSICAL_WIDTH)
            require(dot_mod3(lam, row) == 0, "separator_lambda_current_s")
            rolling = hashlib.sha256(rolling + packed).digest()
            current_hash.update(packed); SCALAR_CALLS["separator_rows"] += 1
        require(stream.read(1) == b"", "separator_current_s_trailing")
    require(current_hash.hexdigest() == current["sha256"],
            "separator_current_s_digest")
    require(rolling.hex() == manifest["rolling_s_head"], "separator_rolling_head")
    require(dot_mod3(lam, base["rho2"]["dense"]) == 1,
            "separator_lambda_rho2")
    return {"root": root, "manifest": manifest, "manifest_sha256": sha(raw),
            "generation": manifest["generation"], "rolling_s_head": manifest["rolling_s_head"],
            "lambda": lam, "lambda_sha256": sha(lam_raw), "rows": current["rows"],
            "rho2_pairing": 1}


def _raw_dual_keys() -> set[str]:
    return {"schema", "separator_generation", "separator_s_head_sha256", "lambda_sha256",
            "character", "B_adj_table_identity", "word_node",
            "actor_table_identities_along_w", "raw_q_packed_sha256",
            "raw_q_packed_offset", "raw_q_packed_length", "raw_predecessor_sha256", "sha256"}


def validate_raw_dual(value: Any) -> None:
    require(isinstance(value, dict) and set(value) == _raw_dual_keys() and
            value["schema"] == LIVE_SCHEMA + ".RawDual", "raw_dual_keys")
    body = dict(value); seal = body.pop("sha256")
    require(seal == sha(canonical(body)), "raw_dual_seal")
    for key in ("separator_s_head_sha256", "lambda_sha256", "raw_q_packed_sha256"):
        digest_string(value[key], "raw_dual_digest:" + key)
    require(plain_int(value["separator_generation"]) and plain_int(value["character"]) and
            0 <= value["character"] < 4 and plain_int(value["raw_q_packed_offset"]) and
            value["raw_q_packed_offset"] == 0 and value["raw_q_packed_length"] ==
            SOURCE_WIDTH // 4 and isinstance(value["word_node"], dict) and
            isinstance(value["actor_table_identities_along_w"], list), "raw_dual_shape")


def _read_q(root: Path, receipt: dict[str, Any]) -> np.ndarray:
    require(set(receipt) == {"raw_dual_sha256", "file", "offset", "length", "sha256"},
            "raw_q_receipt_keys")
    require(plain_int(receipt["offset"]) and receipt["offset"] == 0 and
            plain_int(receipt["length"]) and receipt["length"] == SOURCE_WIDTH // 4,
            "raw_q_location")
    raw = read_receipt(root, {"file": receipt["file"], "bytes": receipt["length"],
                              "sha256": receipt["sha256"]}, 1 << 28, "raw_q")
    return unpack_trits(raw, SOURCE_WIDTH)


def _prior_state_keys() -> set[str]:
    return {"schema", "root", "manifest", "files", "sha256"}


def _prior_manifest_keys() -> set[str]:
    return {"schema", "separator_generation", "separator_s_head_sha256",
            "lambda_sha256", "character", "width", "row_bytes", "rank_before",
            "normalized_rows", "pivot_records", "rolling_head", "eof"}


def _prior_row_record_keys() -> set[str]:
    return {"schema", "pivot_id", "lead", "normalized_row", "raw_dual_sha256",
            "origin_identity", "rolling_head"}


def _prior_receipt_keys() -> set[str]:
    return {"file", "bytes", "sha256"}


def _read_prior_state_row(stream: Any, offset: int, row_bytes: int,
                          buffer: bytearray, reason: str) -> bytes:
    require(offset >= 0 and offset % row_bytes == 0, reason + ":offset")
    stream.seek(offset)
    view = memoryview(buffer)
    count = stream.readinto(view)
    require(count == row_bytes, reason + ":eof")
    return bytes(view)


def validate_prior_dual_state(value: Any, separator: dict[str, Any],
                              character: int) -> dict[str, Any]:
    """Authenticate and stream the prior normalized dual basis.

    Only record metadata is retained.  Dense rows are read through one
    positioned, reusable packed-row buffer when the reduction is replayed.
    """
    require(isinstance(value, dict) and set(value) == _prior_state_keys() and
            value["schema"] == LIVE_SCHEMA + ".prior-dual-state.v1",
            "prior_state_keys")
    unsigned = dict(value); seal = unsigned.pop("sha256")
    require(seal == sha(canonical(unsigned)), "prior_state_seal")
    root = Path(value["root"]).absolute()
    manifest_record = value["manifest"]
    require(isinstance(manifest_record, dict) and set(manifest_record) ==
            _prior_receipt_keys() and Path(manifest_record["file"]).name ==
            manifest_record["file"], "prior_state_manifest_receipt")
    manifest, manifest_raw = read_canonical(root / manifest_record["file"],
                                           1 << 24, "prior_state_manifest")
    require(manifest_record == {"file": manifest_record["file"],
            "bytes": len(manifest_raw), "sha256": sha(manifest_raw)},
            "prior_state_manifest_pin")
    require(set(manifest) == _prior_manifest_keys() and
            manifest["schema"] == LIVE_SCHEMA + ".prior-dual-manifest.v1" and
            manifest["separator_generation"] == separator["generation"] and
            manifest["separator_s_head_sha256"] == separator["rolling_s_head"] and
            manifest["lambda_sha256"] == separator["lambda_sha256"] and
            manifest["character"] == character and manifest["width"] == SOURCE_WIDTH and
            manifest["row_bytes"] == SOURCE_WIDTH // 4 and plain_int(manifest["rank_before"]) and
            0 <= manifest["rank_before"] <= SOURCE_WIDTH and manifest["eof"] is True,
            "prior_state_manifest_shape")
    for key in ("separator_s_head_sha256", "lambda_sha256", "rolling_head"):
        digest_string(manifest[key], "prior_state_manifest_" + key)
    rank = manifest["rank_before"]; row_bytes = SOURCE_WIDTH // 4
    normalized = manifest["normalized_rows"]
    records = manifest["pivot_records"]
    require(isinstance(normalized, dict) and set(normalized) ==
            {"file", "bytes", "sha256", "rows", "row_width", "row_bytes", "eof"} and
            normalized["rows"] == rank and normalized["row_width"] == SOURCE_WIDTH and
            normalized["row_bytes"] == row_bytes and normalized["eof"] is True and
            normalized["bytes"] == rank * row_bytes,
            "prior_state_normalized_receipt")
    require(isinstance(records, dict) and set(records) ==
            {"file", "bytes", "sha256", "rows", "eof"} and records["rows"] == rank and
            records["eof"] is True, "prior_state_records_receipt")
    for receipt in (normalized, records):
        require(Path(receipt["file"]).name == receipt["file"],
                "prior_state_filename")
        require(plain_int(receipt["bytes"]) and receipt["bytes"] >= 0,
                "prior_state_file_bytes")
        digest_string(receipt["sha256"], "prior_state_file_digest")
    require(isinstance(value["files"], list) and
            sorted(value["files"], key=lambda item: item["file"]) ==
            sorted([{"file": normalized["file"], "bytes": normalized["bytes"],
                    "sha256": normalized["sha256"]},
                   {"file": records["file"], "bytes": records["bytes"],
                    "sha256": records["sha256"]}], key=lambda item: item["file"]),
            "prior_state_file_roster")
    norm_path = root / normalized["file"]
    norm_info = regular(norm_path)
    require(norm_info.st_size == normalized["bytes"], "prior_state_normalized_size")
    if norm_info.st_size > 1 << 30:
        raise UnknownResource("UNKNOWN_RESOURCE:prior_state_normalized:bytes")
    records_path = root / records["file"]; record_info = regular(records_path)
    require(record_info.st_size == records["bytes"], "prior_state_records_size")
    if record_info.st_size > 1 << 30:
        raise UnknownResource("UNKNOWN_RESOURCE:prior_state_records:bytes")
    expected_names = {manifest_record["file"], normalized["file"], records["file"]}
    require({item.name for item in root.iterdir()} == expected_names,
            "prior_state_directory_roster")
    buffer = bytearray(row_bytes)
    norm_hash = hashlib.sha256(); record_hash = hashlib.sha256()
    body_hash = hashlib.sha256(); body_bytes = 0; rolling = b"\0" * 32
    metadata: list[dict[str, Any]] = []; seen_leads: set[int] = set()
    seen_raw_duals: set[str] = set(); seen_origins: set[tuple[str, int]] = set()
    with norm_path.open("rb") as norm_stream, records_path.open("rb") as record_stream:
        for pivot_id in range(rank):
            line = record_stream.readline()
            require(line and line.endswith(b"\n"), "prior_state_record_eof")
            record_hash.update(line); body_hash.update(line); body_bytes += len(line)
            try:
                record = json.loads(line[:-1].decode("ascii"))
            except (UnicodeError, ValueError) as exc:
                raise RuntimeError("prior_state_record_json") from exc
            require(canonical(record) == line and isinstance(record, dict) and
                    set(record) == _prior_row_record_keys() and
                    record["schema"] == LIVE_SCHEMA + ".PriorPivotRecord" and
                    record["pivot_id"] == pivot_id and plain_int(record["lead"]) and
                    0 <= record["lead"] < SOURCE_WIDTH and
                    record["lead"] not in seen_leads,
                    "prior_state_record_shape")
            if metadata and record["lead"] <= metadata[-1]["lead"]:
                raise RuntimeError("prior_state_lead_order")
            seen_leads.add(record["lead"])
            digest_string(record["raw_dual_sha256"], "prior_state_raw_dual")
            require(record["raw_dual_sha256"] not in seen_raw_duals,
                    "prior_state_raw_dual_unique")
            seen_raw_duals.add(record["raw_dual_sha256"])
            origin_identity = record["origin_identity"]
            require(isinstance(origin_identity, dict) and
                    set(origin_identity) == {"kind", "id"} and
                    isinstance(origin_identity["kind"], str) and origin_identity["kind"] and
                    plain_int(origin_identity["id"]) and origin_identity["id"] >= 0,
                    "prior_state_origin")
            origin_key = (origin_identity["kind"], origin_identity["id"])
            require(origin_key not in seen_origins, "prior_state_origin_unique")
            seen_origins.add(origin_key)
            row_loc = record["normalized_row"]
            require(isinstance(row_loc, dict) and set(row_loc) ==
                    {"offset", "length", "sha256"} and
                    row_loc["offset"] == pivot_id * row_bytes and
                    row_loc["length"] == row_bytes, "prior_state_row_location")
            digest_string(row_loc["sha256"], "prior_state_row_digest")
            packed = _read_prior_state_row(norm_stream, row_loc["offset"],
                                            row_bytes, buffer, "prior_state_row")
            require(sha(packed) == row_loc["sha256"], "prior_state_row_file_digest")
            norm_hash.update(packed)
            row = unpack_trits(packed, SOURCE_WIDTH)
            nonzero = np.flatnonzero(row)
            require(len(nonzero) > 0 and int(nonzero[0]) == record["lead"] and
                    int(row[record["lead"]]) == 1,
                    "prior_state_row_lead")
            prior_head = rolling
            unsigned_record = dict(record); record_head = unsigned_record.pop("rolling_head")
            digest_string(record_head, "prior_state_record_head")
            expected_head = sha(prior_head + canonical(unsigned_record))
            require(record_head == expected_head, "prior_state_record_head_replay")
            rolling = bytes.fromhex(record_head)
            metadata.append({"pivot_id": pivot_id, "lead": record["lead"],
                             "offset": row_loc["offset"], "length": row_bytes,
                             "sha256": row_loc["sha256"],
                             "raw_dual_sha256": record["raw_dual_sha256"],
                             "origin_identity": origin_identity,
                             "rolling_head": record_head})
        eof_line = record_stream.readline()
        require(eof_line and eof_line.endswith(b"\n"), "prior_state_records_eof")
        record_hash.update(eof_line)
        try:
            marker = json.loads(eof_line[:-1].decode("ascii"))
        except (UnicodeError, ValueError) as exc:
            raise RuntimeError("prior_state_records_marker_json") from exc
        require(canonical(marker) == eof_line and set(marker) ==
                {"schema", "rows", "body_bytes", "body_sha256", "rolling_head", "eof"} and
                marker["schema"] == LIVE_SCHEMA + ".PriorPivotRecordEOF" and
                marker["rows"] == rank and marker["body_bytes"] == body_bytes and
                marker["body_sha256"] == body_hash.hexdigest() and
                marker["rolling_head"] == rolling.hex() and marker["eof"] is True,
                "prior_state_records_marker")
        require(record_stream.read(1) == b"" and norm_stream.seek(0, 2) == normalized["bytes"],
                "prior_state_records_trailing")
    require(norm_hash.hexdigest() == normalized["sha256"] and
            record_hash.hexdigest() == records["sha256"] and
            rolling.hex() == manifest["rolling_head"], "prior_state_stream_pin")
    return {"root": root, "manifest": manifest, "manifest_sha256": sha(manifest_raw),
            "files": value["files"], "records": metadata, "rank_before": rank,
            "rolling_head": rolling.hex(), "normalized_path": norm_path,
            "normalized_rows_sha256": normalized["sha256"], "records_sha256": records["sha256"],
            "sha256": seal, "row_bytes": row_bytes}


def _dual_next_state_head(prior_head: str, pivot_id: int, lead: int,
                          normalized_sha256: str, raw_dual_sha256: str,
                          remainder_sha256: str, rank_after: int) -> str:
    payload = {"pivot_id": pivot_id, "lead": lead,
               "normalized_pivot_sha256": normalized_sha256,
               "raw_dual_sha256": raw_dual_sha256,
               "remainder_sha256": remainder_sha256, "rank_after": rank_after}
    return sha(bytes.fromhex(prior_head) + canonical(payload))


def _validate_dual_pivot(value: Any, final_raw: dict[str, Any], root: Path,
                         files: list[dict[str, Any]], raw_q: np.ndarray,
                         prior_state: dict[str, Any]) -> dict[str, Any]:
    keys = {"schema", "raw_dual_sha256", "prior_state_head_sha256",
            "prior_pivot_coefficients", "remainder_sha256", "raw_lead",
            "raw_lead_scalar", "lead", "scale", "normalized_pivot_sha256",
            "normalized_pivot", "rank_before", "insertion_id", "dual_rank_after",
            "next_state_head_sha256", "sha256"}
    require(isinstance(value, dict) and set(value) == keys and value["schema"] ==
            LIVE_SCHEMA + ".DualPivot", "dual_pivot_keys")
    body = dict(value); seal = body.pop("sha256")
    require(seal == sha(canonical(body)) and value["raw_dual_sha256"] == final_raw["sha256"],
            "dual_pivot_seal_join")
    require(isinstance(raw_q, np.ndarray) and raw_q.size == SOURCE_WIDTH and
            not np.any(raw_q > 2), "dual_pivot_raw_q")
    require(value["prior_state_head_sha256"] == prior_state["rolling_head"],
            "dual_pivot_prior_state_head")
    digest_string(value["prior_state_head_sha256"], "dual_pivot_prior_state_head_shape")
    digest_string(value["remainder_sha256"], "dual_pivot_remainder")
    digest_string(value["normalized_pivot_sha256"], "dual_pivot_normalized")
    digest_string(value["next_state_head_sha256"], "dual_pivot_next_state_head")
    raw_positions = np.flatnonzero(raw_q)
    require(len(raw_positions) > 0 and plain_int(value["raw_lead"]) and
            value["raw_lead"] == int(raw_positions[0]) and 0 <= value["raw_lead"] < SOURCE_WIDTH and
            plain_int(value["raw_lead_scalar"]) and
            value["raw_lead_scalar"] == int(raw_q[value["raw_lead"]]) and
            value["raw_lead_scalar"] in (1, 2), "dual_pivot_raw_shape")
    coefficients = value["prior_pivot_coefficients"]
    require(isinstance(coefficients, list), "dual_pivot_prior_coefficients")
    remainder = raw_q.copy(); previous_id = -1; reduction_steps = 0
    buffer = bytearray(prior_state["row_bytes"])
    normalized_path = prior_state["normalized_path"]
    with normalized_path.open("rb") as stream:
        for item in coefficients:
            require(isinstance(item, dict) and set(item) ==
                    {"pivot_id", "lead", "coefficient"} and
                    plain_int(item["pivot_id"]) and item["pivot_id"] > previous_id and
                    0 <= item["pivot_id"] < prior_state["rank_before"] and
                    plain_int(item["lead"]) and plain_int(item["coefficient"]) and
                    item["coefficient"] in (1, 2), "dual_pivot_coefficient_shape")
            pivot_id = item["pivot_id"]; previous_id = pivot_id
            record = prior_state["records"][pivot_id]
            require(item["lead"] == record["lead"] and
                    remainder[item["lead"]] != 0,
                    "dual_pivot_prior_applicability")
            derived = int(remainder[item["lead"]])
            require(item["coefficient"] == derived, "dual_pivot_coefficient_replay")
            packed = _read_prior_state_row(stream, record["offset"], record["length"],
                                            buffer, "dual_pivot_prior_row")
            require(sha(packed) == record["sha256"], "dual_pivot_prior_row_digest")
            row = unpack_trits(packed, SOURCE_WIDTH)
            require(int(row[record["lead"]]) == 1, "dual_pivot_prior_lead")
            remainder[:] = (remainder.astype(np.int16) -
                            derived * row.astype(np.int16)) % 3
            remainder = remainder.astype(np.uint8)
            reduction_steps += 1
    for record in prior_state["records"]:
        require(int(remainder[record["lead"]]) == 0,
                "dual_pivot_prior_remaining_lead")
    nonzero = np.flatnonzero(remainder)
    require(len(nonzero) > 0, "dual_pivot_dependent_zero")
    new_lead = int(nonzero[0]); new_scalar = int(remainder[new_lead])
    require(value["lead"] == new_lead and 0 <= value["lead"] < SOURCE_WIDTH and
            value["remainder_sha256"] == sha(pack_trits(remainder)),
            "dual_pivot_remainder_replay")
    require(plain_int(value["scale"]) and value["scale"] in (1, 2) and
            value["scale"] == (1 if new_scalar == 1 else 2), "dual_pivot_scale")
    require(plain_int(value["rank_before"]) and
            value["rank_before"] == prior_state["rank_before"] and
            plain_int(value["insertion_id"]) and
            value["insertion_id"] == prior_state["rank_before"] and
            plain_int(value["dual_rank_after"]) and
            value["dual_rank_after"] == prior_state["rank_before"] + 1,
            "dual_pivot_rank_shape")
    loc = value["normalized_pivot"]
    require(isinstance(loc, dict) and set(loc) == {"file", "offset", "length", "sha256"} and
            plain_int(loc["offset"]) and loc["offset"] == 0 and
            loc["length"] == SOURCE_WIDTH // 4,
            "dual_pivot_location")
    require(any(item == {"file": loc["file"], "bytes": loc["length"],
                        "sha256": loc["sha256"]} for item in files), "dual_pivot_file_join")
    data = read_receipt(root, {"file": loc["file"], "bytes": loc["length"],
                               "sha256": loc["sha256"]}, 1 << 28,
                        "dual_pivot_normalized")
    normalized = (value["scale"] * remainder.astype(np.uint16) % 3).astype(np.uint8)
    require(sha(data) == value["normalized_pivot_sha256"] and
            data == pack_trits(normalized), "dual_pivot_normalized_shape")
    expected_next = _dual_next_state_head(prior_state["rolling_head"],
        value["insertion_id"], new_lead, value["normalized_pivot_sha256"],
        value["raw_dual_sha256"], value["remainder_sha256"], value["dual_rank_after"])
    require(value["next_state_head_sha256"] == expected_next,
            "dual_pivot_next_state_head_replay")
    SCALAR_CALLS["dual_reduction_steps"] += reduction_steps
    SCALAR_CALLS["dual_prior_records"] = prior_state["rank_before"]
    return {"remainder": remainder, "new_lead": new_lead,
            "new_scalar": new_scalar, "reduction_steps": reduction_steps,
            "next_state_head": expected_next}


def validate_raw_chain(chain: Any, tables: dict[str, Any],
                       separator: dict[str, Any]) -> tuple[dict[str, Any], list[np.ndarray]]:
    keys = {"schema", "separator_generation", "separator_s_head_sha256", "lambda_sha256",
            "character", "root", "root_node", "root_q_receipt", "edges", "children", "files",
            "final_raw_dual_sha256", "sha256"}
    require(isinstance(chain, dict) and set(chain) == keys and chain["schema"] ==
            LIVE_SCHEMA + ".RawDualChain", "raw_chain_keys")
    body = dict(chain); seal = body.pop("sha256")
    require(seal == sha(canonical(body)), "raw_chain_seal")
    require(chain["separator_generation"] == separator["generation"] and
            chain["separator_s_head_sha256"] == separator["rolling_s_head"] and
            chain["lambda_sha256"] == separator["lambda_sha256"] and
            plain_int(chain["character"]) and 0 <= chain["character"] < 4,
            "raw_chain_separator_join")
    require(isinstance(chain["files"], list) and
            all(isinstance(item, dict) and set(item) ==
                {"file", "bytes", "sha256"} for item in chain["files"]),
            "raw_chain_file_roster")
    root = Path(chain["root"]).absolute()
    require(len({item["file"] for item in chain["files"]}) == len(chain["files"]),
            "raw_chain_file_duplicates")
    for item in chain["files"]:
        read_receipt(root, item, 1 << 28, "raw_chain_file")
    node = chain["root_node"]
    validate_raw_dual(node)
    require(node["word_node"] == {"kind": "root", "actors": []} and
            node["raw_predecessor_sha256"] is None and
            node["character"] == chain["character"] and
            node["separator_generation"] == chain["separator_generation"] and
            node["separator_s_head_sha256"] == chain["separator_s_head_sha256"] and
            node["lambda_sha256"] == chain["lambda_sha256"] and
            node["B_adj_table_identity"] == tables["identity"]["adjoint:B"] and
            chain["root_q_receipt"]["raw_dual_sha256"] == node["sha256"] and
            chain["root_q_receipt"]["sha256"] == node["raw_q_packed_sha256"],
            "raw_chain_root_metadata")
    current_q = _read_q(root, chain["root_q_receipt"])
    expected_q = sparse_adjoint(tables["forward"]["B"], SOURCE_WIDTH, PHYSICAL_WIDTH,
                                separator["lambda"])
    require(current_q.tobytes() == expected_q.tobytes(), "raw_chain_root_recompute")
    previous = node
    for edge in chain["edges"]:
        require(set(edge) == {"schema", "parent_raw_dual_sha256", "appended_actor",
                              "T_adj_table_identity", "q_receipt", "predecessor", "raw_dual"} and
                edge["schema"] == LIVE_SCHEMA + ".RawDualEdge", "raw_chain_edge_keys")
        child = edge["raw_dual"]; validate_raw_dual(child); actor = edge["appended_actor"]
        require(plain_int(actor) and actor in ACTORS and
                edge["parent_raw_dual_sha256"] == previous["sha256"] and
                edge["predecessor"] == previous["sha256"] and
                edge["T_adj_table_identity"] == tables["identity"]["adjoint:" + str(actor)] and
                child["raw_predecessor_sha256"] == previous["sha256"] and
                child["character"] == chain["character"] and
                child["separator_generation"] == chain["separator_generation"] and
                child["separator_s_head_sha256"] == chain["separator_s_head_sha256"] and
                child["lambda_sha256"] == chain["lambda_sha256"] and
                child["B_adj_table_identity"] == tables["identity"]["adjoint:B"] and
                child["actor_table_identities_along_w"] ==
                previous["actor_table_identities_along_w"] +
                [edge["T_adj_table_identity"]] and
                child["word_node"] == {"kind": "edge", "parent_raw_dual_sha256": previous["sha256"],
                                        "appended_actor": actor}, "raw_chain_edge_join")
        expected_q = sparse_adjoint(tables["forward"][actor], SOURCE_WIDTH, SOURCE_WIDTH,
                                    current_q)
        receipt = edge["q_receipt"]
        require(receipt["raw_dual_sha256"] == child["sha256"] and
                receipt["sha256"] == child["raw_q_packed_sha256"], "raw_chain_edge_q_join")
        current_q = _read_q(root, receipt)
        require(current_q.tobytes() == expected_q.tobytes(), "raw_chain_edge_recompute")
        previous = child; SCALAR_CALLS["raw_edges"] += 1
    final = previous
    require(final["sha256"] == chain["final_raw_dual_sha256"] and
            isinstance(chain["children"], list) and len(chain["children"]) == 4,
            "raw_chain_final")
    children: list[np.ndarray] = []
    for index, edge in enumerate(chain["children"]):
        require(set(edge) == {"schema", "parent_raw_dual_sha256", "appended_actor",
                              "T_adj_table_identity", "q_receipt", "predecessor", "raw_dual"},
                "raw_child_edge_keys")
        child = edge["raw_dual"]; validate_raw_dual(child); actor = ACTORS[index]
        require(edge["parent_raw_dual_sha256"] == final["sha256"] and
                edge["predecessor"] == final["sha256"] and edge["appended_actor"] == actor and
                edge["T_adj_table_identity"] == tables["identity"]["adjoint:" + str(actor)] and
                child["raw_predecessor_sha256"] == final["sha256"] and
                child["character"] == chain["character"] and
                child["separator_generation"] == chain["separator_generation"] and
                child["separator_s_head_sha256"] == chain["separator_s_head_sha256"] and
                child["lambda_sha256"] == chain["lambda_sha256"] and
                child["B_adj_table_identity"] == tables["identity"]["adjoint:B"] and
                child["actor_table_identities_along_w"] ==
                final["actor_table_identities_along_w"] +
                [edge["T_adj_table_identity"]] and
                child["word_node"] == {"kind": "edge",
                    "parent_raw_dual_sha256": final["sha256"],
                    "appended_actor": actor}, "raw_child_parent")
        expected = sparse_adjoint(tables["forward"][actor], SOURCE_WIDTH, SOURCE_WIDTH,
                                  current_q)
        receipt = edge["q_receipt"]
        require(receipt["raw_dual_sha256"] == child["sha256"] and
                receipt["sha256"] == child["raw_q_packed_sha256"],
                "raw_child_receipt_join")
        actual = _read_q(root, receipt)
        require(actual.tobytes() == expected.tobytes(),
                "raw_child_recompute")
        children.append(actual)
    return final, [current_q] + children


def _validate_instruction(record: Any, node: int, raw_row: bytes,
                          predecessor: bytes) -> str:
    keys = {"node", "offset", "length", "row_sha256", "predecessor",
            "origin", "reductions", "scale", "ancestry_sha256"}
    require(isinstance(record, dict) and set(record) == keys and
            record["node"] == node and record["offset"] == node * P1_ROW_BYTES and
            record["length"] == P1_ROW_BYTES and record["row_sha256"] == sha(raw_row) and
            record["predecessor"] == predecessor.hex() and plain_int(record["scale"]) and
            record["scale"] in (1, 2) and isinstance(record["origin"], dict) and
            isinstance(record["reductions"], list), "scalar_instruction")
    previous = -1
    for pair in record["reductions"]:
        require(isinstance(pair, list) and len(pair) == 2 and plain_int(pair[0]) and
                plain_int(pair[1]) and pair[0] > previous and pair[1] in (1, 2),
                "scalar_instruction_reductions")
        previous = pair[0]
    unsigned = dict(record); ancestry = unsigned.pop("ancestry_sha256")
    digest_string(ancestry, "scalar_instruction_ancestry_shape")
    require(ancestry == sha(predecessor + canonical(unsigned)),
            "scalar_instruction_ancestry")
    return ancestry


SCALAR_CALLS = {"task712_tables": 0, "separator_rows": 0, "raw_edges": 0,
                "p1_cache_passes": 0, "p1_rows": 0, "scalar_records": 0,
                "seed_evaluations": 0, "extra_cache_opens": 0,
                "dual_prior_records": 0, "dual_reduction_steps": 0}


def read_scalar_p1(base: dict[str, Any], character: int,
                   covectors: list[np.ndarray]) -> tuple[list[np.ndarray], dict[str, Any]]:
    """Accumulate five vectors during one sequential authenticated P1 pass."""
    p1 = base["p1"]; manifest = p1["manifest"]; universe = base["universe"]
    require(len(covectors) == 5 and all(np.asarray(q).size == SOURCE_WIDTH
                                        for q in covectors), "scalar_covectors")
    rows = universe["rows"]; cache_rec = manifest["cache"]; inst_rec = manifest["instruction"]
    cache_path = Path(p1["root"]) / cache_rec["path"]
    inst_path = Path(p1["root"]) / inst_rec["path"]
    values = [np.empty(rows, dtype=np.uint8) for _ in range(5)]
    SCALAR_CALLS["p1_cache_passes"] += 1
    cache_hash = hashlib.sha256(); instruction_hash = hashlib.sha256()
    predecessor = b"\0" * 32; started = time.monotonic()
    completed_claim = (cache_rec["rows"] == rows and inst_rec["rows"] == rows and
                       cache_rec["eof"] is True and inst_rec["eof"] is True)
    with cache_path.open("rb") as cache_file, inst_path.open("rb") as instruction_file:
        for node in range(rows):
            line = instruction_file.readline()
            if not line:
                if completed_claim:
                    raise RuntimeError("p1_instruction_completed_truncated")
                raise UnknownResource("UNKNOWN_RESOURCE:p1_instruction_stream")
            require(line.endswith(b"\n"), "p1_instruction_line")
            raw_row = cache_file.read(P1_ROW_BYTES)
            if len(raw_row) != P1_ROW_BYTES:
                if completed_claim:
                    raise RuntimeError("p1_cache_completed_truncated")
                raise UnknownResource("UNKNOWN_RESOURCE:p1_cache_stream")
            try:
                record = json.loads(line[:-1].decode("ascii"))
            except (UnicodeError, ValueError) as exc:
                raise RuntimeError("p1_instruction_json") from exc
            require(canonical(record) == line, "p1_instruction_canonical")
            predecessor = bytes.fromhex(_validate_instruction(record, node, raw_row,
                                                               predecessor))
            selected = unpack_trits(raw_row, P1_ROW_TRITS).reshape(4, SOURCE_WIDTH)[character]
            for index, covector in enumerate(covectors):
                values[index][node] = dot_mod3(covector, selected)
            cache_hash.update(raw_row); instruction_hash.update(line)
            SCALAR_CALLS["p1_rows"] += 1
        require(cache_file.read(1) == b"" and instruction_file.read(1) == b"",
                "p1_stream_trailing")
    require(cache_file if False else True, "p1_scope")
    require(instruction_file if False else True, "p1_scope")
    require(cache_path.stat().st_size == rows * P1_ROW_BYTES and
            inst_path.stat().st_size == inst_rec["bytes"] and
            cache_hash.hexdigest() == cache_rec["sha256"] and
            instruction_hash.hexdigest() == inst_rec["sha256"] and
            predecessor.hex() == manifest["ancestry_sha256"], "p1_stream_eof")
    elapsed = max(time.monotonic() - started, 1e-9)
    return {"manifest_sha256": p1["manifest_sha256"], "cache_eof": True,
            "instruction_eof": True, "rows": rows, "value_sha256":
            [sha(v.tobytes()) for v in values], "cache_sha256": cache_rec["sha256"],
            "instruction_sha256": inst_rec["sha256"],
            "rolling_p1_sha256": sha(cache_hash.digest() + instruction_hash.digest()),
            "extra_open_count": 0, "throughput_rows_per_second": rows / elapsed,
            "_values": values}


def _global_relations(task554: dict[str, Any], universe: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct v531 SeedRed/ActRed with every old/new block."""
    prepare = task554["prepare"]["body"]; blocks = [x["body"] for x in task554["blocks"]]
    old_offsets: list[int] = []; cursor = 0
    for index, old in enumerate(prepare["old_blocks"]):
        require(old["rank"] == universe["old_ranks"][index], "relation_old_rank")
        old_offsets.append(cursor); cursor += old["rank"]
    new_offsets: list[int] = []
    for index, block in enumerate(blocks):
        require(block["rank"] == universe["new_ranks"][index], "relation_new_rank")
        new_offsets.append(cursor); cursor += block["rank"]
    require(cursor == universe["rows"], "relation_row_count")
    seeds: list[list[list[int]]] = []; new_terms = 0
    for seed in range(44):
        terms: list[list[int]] = []
        for character, old in enumerate(prepare["old_blocks"]):
            terms.extend([[old_offsets[character] + p, c] for p, c in
                          normal_terms(old["record"]["seed_reductions"][seed], old["rank"])])
            origin = old["defect_origin_range"][0] + seed
            for target, block in enumerate(blocks):
                terms.extend([[new_offsets[target] + p, c] for p, c in
                              normal_terms(block["origin_reductions"][origin], block["rank"])])
                new_terms += 1
        seeds.append(normal_terms(terms, universe["rows"]))
    actors: list[list[list[list[int]]]] = []
    for character, old in enumerate(prepare["old_blocks"]):
        for pivot in range(old["rank"]):
            row: list[list[list[int]]] = []
            for slot in range(4):
                terms = [[old_offsets[character] + p, c] for p, c in
                         normal_terms(old["record"]["actor_transitions"][pivot][slot], old["rank"])]
                origin = old["defect_origin_range"][0] + 44 + 4 * pivot + slot
                for target, block in enumerate(blocks):
                    terms.extend([[new_offsets[target] + p, c] for p, c in
                                  normal_terms(block["origin_reductions"][origin], block["rank"])])
                    new_terms += 1
                row.append(normal_terms(terms, universe["rows"]))
            actors.append(row)
    for character, block in enumerate(blocks):
        for source_row in block["actor_transitions"]:
            actors.append([normal_terms([[new_offsets[character] + p, c] for p, c in
                                          normal_terms(expr, block["rank"])], universe["rows"])
                           for expr in source_row])
    require(len(actors) == universe["rows"] and new_terms > 0, "relation_actor_eof")
    result = {"row_count": universe["rows"], "actor_order": list(ACTORS),
              "seeds": seeds, "actors": actors, "old_offsets": old_offsets,
              "new_offsets": new_offsets, "new_contributions": new_terms, "eof": True}
    result["sha256"] = sha(canonical(result)); return result


def _pair(direct: int, terms: list[list[int]], values: np.ndarray) -> int:
    total = direct % 3
    for index, coefficient in terms:
        require(plain_int(index) and plain_int(coefficient) and coefficient in (1, 2) and
                0 <= index < len(values), "scalar_relation_term")
        total = (total - coefficient * int(values[index])) % 3
    return total


def _sealed(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    result = {"schema": LIVE_SCHEMA + "." + kind, **body}
    result["sha256"] = sha(canonical(result)); return result


def scan_scalar(raw_dual: dict[str, Any], values: list[np.ndarray],
                relations: dict[str, Any], cache: dict[str, Any]) -> dict[str, Any]:
    validate_raw_dual(raw_dual)
    rows = len(values[0]); require(len(values) == 5 and all(len(v) == rows for v in values) and
                                   relations["row_count"] == rows and
                                   relations["actor_order"] == list(ACTORS) and
                                   len(relations["seeds"]) == 44 and
                                   len(relations["actors"]) == rows and relations["eof"] is True,
            "scalar_stream_shape")
    chain = b"\0" * 32; origin = 0
    def emit(kind: str, descriptor: dict[str, Any], scalar: int) -> dict[str, Any] | None:
        nonlocal chain, origin
        record = {"origin_id": origin, "origin_kind": kind, **descriptor,
                  "scalar": int(scalar)}
        chain = hashlib.sha256(chain + canonical(record)).digest(); origin += 1
        SCALAR_CALLS["scalar_records"] += 1
        if scalar:
            return _sealed("Violation", {"raw_dual_sha256": raw_dual["sha256"],
                "character": raw_dual["character"], "word_node_sha256":
                sha(canonical(raw_dual["word_node"])), **record,
                "scalar_prefix_digest": chain.hex(), "p1_manifest_sha256":
                cache["manifest_sha256"], "global_relation_stream_sha256": relations["sha256"]})
        return None
    for seed, item in enumerate(relations["seeds"]):
        hit = emit("seed", {"seed": seed}, _pair(item.get("direct", 0), item["terms"], values[0]))
        if hit is not None: return hit
    for index, row in enumerate(relations["actors"]):
        require(isinstance(row, list) and len(row) == 4, "scalar_actor_row")
        for slot, actor in enumerate(ACTORS):
            hit = emit("actor", {"basis_i": index, "actor": actor},
                       _pair(int(values[slot + 1][index]), row[slot], values[0]))
            if hit is not None: return hit
    expected = 44 + 4 * rows
    require(origin == expected and expected == cache["rows"] * 4 + 44,
            "scalar_origin_eof")
    return _sealed("ScalarEOF", {"raw_dual_sha256": raw_dual["sha256"],
        "p1_manifest_sha256": cache["manifest_sha256"],
        "global_relation_stream_sha256": relations["sha256"], "origins": expected,
        "seed_pairings": 44, "actor_pairings": 4 * rows, "next_origin": expected,
        "coefficient_stream_eof": True, "p1_cache_pass_eof": True,
        "value_vector_sha256": cache["value_sha256"],
        "rolling_scalar_head": chain.hex()})


def validate_raw_materialization(value: Any, violation: dict[str, Any]) -> None:
    """Validate the future physical materialization join before its provider runs."""
    require(isinstance(value, dict) and set(value) ==
            {"schema", "violation_sha256", "raw_dual_sha256", "character",
             "origin_id", "physical_width", "payload_sha256", "sha256"},
            "raw_materialization_keys")
    body = dict(value); seal = body.pop("sha256")
    require(value["schema"] == LIVE_SCHEMA + ".RawMaterialization" and
            seal == sha(canonical(body)) and
            value["violation_sha256"] == violation["sha256"] and
            value["raw_dual_sha256"] == violation["raw_dual_sha256"] and
            value["character"] == violation["character"] and
            value["origin_id"] == violation["origin_id"] and
            value["physical_width"] == PHYSICAL_WIDTH, "raw_materialization_join")
    digest_string(value["payload_sha256"], "raw_materialization_payload")


def validate_physical_pivot(value: Any, materialization: dict[str, Any]) -> None:
    """Validate the future current-S insertion join without owning that provider."""
    require(isinstance(value, dict) and set(value) ==
            {"schema", "materialization_sha256", "separator_generation",
             "separator_s_head_sha256", "insertion_id", "sha256"},
            "physical_pivot_keys")
    body = dict(value); seal = body.pop("sha256")
    require(value["schema"] == LIVE_SCHEMA + ".PhysicalPivot" and
            seal == sha(canonical(body)) and
            value["materialization_sha256"] == materialization["sha256"],
            "physical_pivot_join")
    require(plain_int(value["separator_generation"]) and
            value["separator_generation"] >= 0 and
            plain_int(value["insertion_id"]) and value["insertion_id"] >= 0,
            "physical_pivot_shape")
    digest_string(value["separator_s_head_sha256"], "physical_pivot_head")


def materialize_violation(violation: dict[str, Any], provider: Any = None) -> dict[str, Any]:
    require(isinstance(violation, dict) and
            violation.get("schema") == LIVE_SCHEMA + ".Violation" and
            plain_int(violation.get("origin_id")) and
            plain_int(violation.get("character")) and
            plain_int(violation.get("scalar")) and violation["scalar"] in (1, 2),
            "materialization_violation")
    for key in ("raw_dual_sha256", "p1_manifest_sha256",
                "global_relation_stream_sha256", "word_node_sha256",
                "scalar_prefix_digest"):
        digest_string(violation.get(key), "materialization_violation_" + key)
    if provider is None:
        raise NotReady("NOT_READY:authenticated_physical_provider")
    value = provider.materialize(violation)
    validate_raw_materialization(value, violation)
    return value


def insert_physical(materialization: dict[str, Any], provider: Any = None) -> dict[str, Any]:
    require(isinstance(materialization, dict) and
            materialization.get("schema") == LIVE_SCHEMA + ".RawMaterialization",
            "physical_insert_materialization")
    if provider is None:
        raise NotReady("NOT_READY:authenticated_current_S_provider")
    value = provider.insert(materialization)
    validate_physical_pivot(value, materialization)
    return value


def _fixture_write_json(root: Path, name: str, value: Any) -> dict[str, Any]:
    raw = canonical(value); path = root / name; path.write_bytes(raw)
    return {"file": name, "bytes": len(raw), "sha256": sha(raw)}


def _fixture_state(root: Path, index: int, body: dict[str, Any]) -> dict[str, Any]:
    stem = "prepare" if index == -1 else "block-" + str(index)
    body_rec = _fixture_write_json(root, "task554-" + stem + "-body.json", body)
    head = {"schema": LIVE_SCHEMA + ".task554-head.v1", "index": index,
            "body_sha256": body_rec["sha256"]}
    head_rec = _fixture_write_json(root, "task554-" + stem + "-head.json", head)
    return {"root": str(root), "head": head_rec, "body": body_rec,
            "files": [body_rec, head_rec]}


def _fixture_task554(root: Path, universe: dict[str, Any]) -> dict[str, Any]:
    origin_count = sum(44 + 4 * rank for rank in universe["old_ranks"])
    old_blocks: list[dict[str, Any]] = []; cursor = 0
    for index, rank in enumerate(universe["old_ranks"]):
        old_blocks.append({
            "character_index": index, "character": list(CHARACTERS[index]),
            "rank": rank, "defect_origin_range": [cursor, cursor + 44 + 4 * rank],
            "record": {
                "seed_reductions": [[[0, 1]] for _ in range(44)],
                "actor_transitions": [
                    [[[0, 1]] for _ in range(4)] for _ in range(rank)]
                }})
        cursor += 44 + 4 * rank
    require(cursor == origin_count, "fixture_task554_origin_cursor")
    prepare_body = {"schema": LIVE_SCHEMA + ".task554-state.v1", "phase": "prepare",
                    "old_blocks": old_blocks,
                    "defect_origins": [{"origin_id": i} for i in range(origin_count)],
                    "packets": [{"character_index": i, "origin_count": origin_count}
                                 for i in range(4)]}
    prepare = _fixture_state(root, -1, prepare_body)
    blocks: list[dict[str, Any]] = []
    for index, rank in enumerate(universe["new_ranks"]):
        body = {"schema": LIVE_SCHEMA + ".task554-state.v1", "phase": "block",
                "character_index": index, "character": list(CHARACTERS[index]),
                "rank": rank, "origin_count": origin_count,
                "origin_reductions": [[[0, 1]] for _ in range(origin_count)],
                "actor_transitions": [
                    [[[0, 1]] for _ in range(4)] for _ in range(rank)]}
        blocks.append(_fixture_state(root, index, body))
    return {"schema": LIVE_SCHEMA + ".task554-parent.v1", "source_run": 0,
            "source_attempt": 1, "source_head": "fixture-task554-head",
            "prepare": prepare, "blocks": blocks}


def _fixture_p1(root: Path, universe: dict[str, Any], character: int = 0) -> dict[str, Any]:
    rows = universe["rows"]; cache = bytearray(); instructions = bytearray()
    predecessor = b"\0" * 32
    for node in range(rows):
        dense = np.zeros(P1_ROW_TRITS, dtype=np.uint8)
        # A zero row keeps the fixture terminal while still exercising all five dots.
        # The row is full degree-two width; no precision-one reconstruction occurs.
        raw_row = pack_trits(dense); cache.extend(raw_row)
        unsigned = {"node": node, "offset": node * P1_ROW_BYTES,
                    "length": P1_ROW_BYTES, "row_sha256": sha(raw_row),
                    "predecessor": predecessor.hex(),
                    "origin": {"kind": "fixture", "node": node},
                    "reductions": [], "scale": 1}
        ancestry = sha(predecessor + canonical(unsigned))
        record = {**unsigned, "ancestry_sha256": ancestry}
        line = canonical(record); instructions.extend(line); predecessor = bytes.fromhex(ancestry)
    cache_rec = _fixture_write_bytes(root, "degree2.cache.bin", bytes(cache))
    inst_rec = _fixture_write_bytes(root, "instructions.jsonl", bytes(instructions))
    manifest = {"schema": LIVE_SCHEMA + ".p1-manifest.v1", "rows": rows,
                "row_trits": P1_ROW_TRITS, "row_bytes": P1_ROW_BYTES,
                "cache": {"path": cache_rec["file"], "rows": rows,
                          "bytes": cache_rec["bytes"], "sha256": cache_rec["sha256"],
                          "final_lf": True, "eof": True},
                "instruction": {"path": inst_rec["file"], "rows": rows,
                                 "bytes": inst_rec["bytes"], "sha256": inst_rec["sha256"],
                                 "final_lf": True, "eof": True,
                                 "final_head": predecessor.hex()},
                "ancestry_sha256": predecessor.hex()}
    manifest_rec = _fixture_write_json(root, "p1-manifest.json", manifest)
    return {"schema": LIVE_SCHEMA + ".p1.fixture.v1", "root": str(root),
            "manifest": manifest_rec, "files": [cache_rec, inst_rec]}


def _fixture_write_bytes(root: Path, name: str, data: bytes) -> dict[str, Any]:
    (root / name).write_bytes(data)
    return {"file": name, "bytes": len(data), "sha256": sha(data)}


def _fixture_universe_parents(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    universe = {"schema": LIVE_SCHEMA + ".reader-boundary.v1", "fixture": True,
                "rows": 16, "p1_row_trits": P1_ROW_TRITS, "p1_row_bytes": P1_ROW_BYTES,
                "segment_order": [0, 2, 4, 6, 8, 10, 12, 14, 16],
                "old_ranks": [2, 2, 2, 2], "new_ranks": [2, 2, 2, 2],
                "scalar_origins": 108}
    # The bounded public fixture deliberately exercises a raw leading scalar 2.
    # Pairing remains one because rho2 uses the same inverse coefficient.
    physical = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8); physical[45] = 2
    rho_raw = pack_trits(physical); rho_rec = _fixture_write_bytes(root, "rho2.bin", rho_raw)
    rho_manifest = {"schema": LIVE_SCHEMA + ".rho2-manifest.v1", "width": PHYSICAL_WIDTH,
                    "packed_bytes": PHYSICAL_PACKED_BYTES,
                    "rho2": {"sha256": rho_rec["sha256"], "pairing_target": 1},
                    "files": [rho_rec]}
    rho_manifest_rec = _fixture_write_json(root, "rho2-manifest.json", rho_manifest)
    rho_parent = {"schema": LIVE_SCHEMA + ".rho2.fixture.v1", "root": str(root),
                  "manifest": rho_manifest_rec, "files": [rho_rec]}
    p1_parent = _fixture_p1(root, _fixture_universe(universe), 0)
    return universe, rho_parent, p1_parent


def _fixture_base(root: Path) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    universe_descriptor, rho_parent, p1_parent = _fixture_universe_parents(root)
    universe = _fixture_universe(universe_descriptor)
    task554_parent = _fixture_task554(root, universe)
    caps = {"manifest_bytes": 1 << 20, "rho2_durable_bytes": 1 << 20,
            "p1_durable_bytes": 1 << 30, "task554_durable_bytes": 1 << 30,
            "instruction_bytes": 1 << 30, "resident_bytes": 1 << 30}
    launch = {"schema": BASE_SCHEMA, "rho2_parent": rho_parent,
              "p1_parent": p1_parent, "task554_parent": task554_parent,
              "caps": caps, "reader_boundary": universe_descriptor}
    path = root / "base-launch.json"; path.write_bytes(canonical(launch))
    return path, launch, universe


def _fixture_separator(root: Path, base_path: Path, base_launch: dict[str, Any]) -> dict[str, Any]:
    physical = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8); physical[45] = 2
    lambda_raw = pack_trits(physical); lambda_rec = _fixture_write_bytes(root, "lambda.bin", lambda_raw)
    rows: list[bytes] = []
    for coordinate in (1, 2):
        row = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8); row[coordinate] = 1
        rows.append(pack_trits(row))
    current_raw = b"".join(rows); current_rec = _fixture_write_bytes(root, "current-S.bin", current_raw)
    rolling = b"\0" * 32
    for row in rows: rolling = hashlib.sha256(rolling + row).digest()
    manifest = {"schema": LIVE_SCHEMA + ".separator-manifest.v1",
                "base_launch_sha256": sha(base_path.read_bytes()), "generation": 7,
                "row_count": len(rows), "row_width": PHYSICAL_WIDTH,
                "row_bytes": PHYSICAL_PACKED_BYTES, "order": "packed-row-major",
                "current_s": {"file": current_rec["file"], "bytes": current_rec["bytes"],
                              "sha256": current_rec["sha256"], "rows": len(rows),
                              "row_width": PHYSICAL_WIDTH, "row_bytes": PHYSICAL_PACKED_BYTES,
                              "eof": True},
                "lambda": lambda_rec, "rolling_s_head": rolling.hex(), "eof": True}
    manifest_rec = _fixture_write_json(root, "separator-manifest.json", manifest)
    return {"schema": LIVE_SCHEMA + ".separator-parent.v1", "root": str(root),
            "manifest": manifest_rec, "files": [current_rec, lambda_rec]}


def _fixture_prior_state(root: Path, separator: dict[str, Any], raw_q: np.ndarray,
                         character: int = 0) -> tuple[dict[str, Any], list[int], list[np.ndarray], str]:
    """Build a small file-backed two-pivot prior state for public replay."""
    prior_root = root / "prior-dual-state"; prior_root.mkdir(parents=True, exist_ok=True)
    positions = np.flatnonzero(raw_q)
    require(len(positions) >= 2, "fixture_prior_support")
    leads = [int(positions[0]), int(positions[1])]
    preferred_tail = int(positions[2]) if len(positions) > 2 else SOURCE_WIDTH - 2
    tails = [preferred_tail, SOURCE_WIDTH - 1]
    while tails[0] in leads or (tails[0] in positions and tails[0] != preferred_tail):
        tails[0] -= 1
    while tails[1] in leads or tails[1] in positions or tails[1] == tails[0]:
        tails[1] -= 1
    prior_rows: list[np.ndarray] = []
    for pivot_id, (lead, tail) in enumerate(zip(leads, tails)):
        row = np.zeros(SOURCE_WIDTH, dtype=np.uint8); row[lead] = 1
        row[tail] = 2 if pivot_id == 0 and tail == preferred_tail and len(positions) > 2 else 1
        prior_rows.append(row)
    packed_rows = b"".join(pack_trits(row) for row in prior_rows)
    normalized_rec = _fixture_write_bytes(prior_root, "normalized-rows.bin", packed_rows)
    row_bytes = SOURCE_WIDTH // 4; records_body = bytearray(); rolling = b"\0" * 32
    record_values: list[dict[str, Any]] = []
    for pivot_id, (lead, row) in enumerate(zip(leads, prior_rows)):
        normalized_digest = sha(pack_trits(row))
        raw_identity = sha(canonical({"kind": "fixture-prior-raw-dual", "pivot_id": pivot_id,
                                      "separator_generation": separator["generation"],
                                      "character": character}))
        unsigned = {"schema": LIVE_SCHEMA + ".PriorPivotRecord", "pivot_id": pivot_id,
                    "lead": lead,
                    "normalized_row": {"offset": pivot_id * row_bytes, "length": row_bytes,
                                        "sha256": normalized_digest},
                    "raw_dual_sha256": raw_identity,
                    "origin_identity": {"kind": "fixture-prior", "id": pivot_id}}
        head = sha(rolling + canonical(unsigned)); record = {**unsigned, "rolling_head": head}
        records_body.extend(canonical(record)); rolling = bytes.fromhex(head)
        record_values.append(record)
    eof = {"schema": LIVE_SCHEMA + ".PriorPivotRecordEOF", "rows": len(prior_rows),
           "body_bytes": len(records_body), "body_sha256": sha(bytes(records_body)),
           "rolling_head": rolling.hex(), "eof": True}
    records_raw = bytes(records_body) + canonical(eof)
    records_rec = _fixture_write_bytes(prior_root, "pivot-records.jsonl", records_raw)
    manifest = {"schema": LIVE_SCHEMA + ".prior-dual-manifest.v1",
                "separator_generation": separator["generation"],
                "separator_s_head_sha256": separator["rolling_s_head"],
                "lambda_sha256": separator["lambda_sha256"], "character": character,
                "width": SOURCE_WIDTH, "row_bytes": row_bytes, "rank_before": len(prior_rows),
                "normalized_rows": {"file": normalized_rec["file"], "bytes": normalized_rec["bytes"],
                                    "sha256": normalized_rec["sha256"], "rows": len(prior_rows),
                                    "row_width": SOURCE_WIDTH, "row_bytes": row_bytes, "eof": True},
                "pivot_records": {"file": records_rec["file"], "bytes": records_rec["bytes"],
                                   "sha256": records_rec["sha256"], "rows": len(prior_rows), "eof": True},
                "rolling_head": rolling.hex(), "eof": True}
    manifest_rec = _fixture_write_json(prior_root, "prior-dual-manifest.json", manifest)
    state_body = {"schema": LIVE_SCHEMA + ".prior-dual-state.v1", "root": str(prior_root),
                  "manifest": manifest_rec,
                  "files": [normalized_rec, records_rec]}
    state = {**state_body, "sha256": sha(canonical(state_body))}
    return state, leads, prior_rows, rolling.hex()


def _fixture_raw_chain(root: Path, tables: dict[str, Any], separator: dict[str, Any],
                       character: int = 0) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    lam = separator["lambda"]
    files: list[dict[str, Any]] = []

    def put(name: str, data: bytes) -> dict[str, Any]:
        receipt = _fixture_write_bytes(root, name, data); files.append(receipt); return receipt

    def node(q: np.ndarray, word_node: dict[str, Any], previous: str | None,
             actors: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
        packed = pack_trits(q); unsigned = {"schema": LIVE_SCHEMA + ".RawDual",
            "separator_generation": separator["generation"],
            "separator_s_head_sha256": separator["rolling_s_head"],
            "lambda_sha256": separator["lambda_sha256"], "character": character,
            "B_adj_table_identity": tables["identity"]["adjoint:B"],
            "word_node": word_node, "actor_table_identities_along_w": actors,
            "raw_q_packed_sha256": sha(packed), "raw_q_packed_offset": 0,
            "raw_q_packed_length": len(packed), "raw_predecessor_sha256": previous}
        value = {**unsigned, "sha256": sha(canonical(unsigned))}
        rec = {"raw_dual_sha256": value["sha256"], **put(
            "raw-q-" + str(len(files)) + ".bin", packed)}
        return value, {"raw_dual_sha256": rec["raw_dual_sha256"], "file": rec["file"],
                       "offset": 0, "length": len(packed), "sha256": rec["sha256"]}

    current = sparse_adjoint(tables["forward"]["B"], SOURCE_WIDTH, PHYSICAL_WIDTH, lam)
    root_node, root_q = node(current, {"kind": "root", "actors": []}, None, [])
    edges: list[dict[str, Any]] = []; previous = root_node; previous_q = current; actor_ids: list[str] = []
    for actor in ACTORS:
        current = sparse_adjoint(tables["forward"][actor], SOURCE_WIDTH, SOURCE_WIDTH, previous_q)
        actor_id = tables["identity"]["adjoint:" + str(actor)]; actor_ids = actor_ids + [actor_id]
        child, receipt = node(current, {"kind": "edge", "parent_raw_dual_sha256": previous["sha256"],
                                        "appended_actor": actor}, previous["sha256"], actor_ids)
        edges.append({"schema": LIVE_SCHEMA + ".RawDualEdge",
                      "parent_raw_dual_sha256": previous["sha256"], "appended_actor": actor,
                      "T_adj_table_identity": actor_id, "q_receipt": receipt,
                      "predecessor": previous["sha256"], "raw_dual": child})
        previous, previous_q = child, current
    final = previous; children: list[dict[str, Any]] = []
    for actor in ACTORS:
        current = sparse_adjoint(tables["forward"][actor], SOURCE_WIDTH, SOURCE_WIDTH, previous_q)
        actor_id = tables["identity"]["adjoint:" + str(actor)]
        child, receipt = node(current, {"kind": "edge", "parent_raw_dual_sha256": final["sha256"],
                                        "appended_actor": actor}, final["sha256"], actor_ids + [actor_id])
        children.append({"schema": LIVE_SCHEMA + ".RawDualEdge",
                         "parent_raw_dual_sha256": final["sha256"], "appended_actor": actor,
                         "T_adj_table_identity": actor_id, "q_receipt": receipt,
                         "predecessor": final["sha256"], "raw_dual": child})
    raw_q = previous_q
    raw_nonzero = np.flatnonzero(raw_q)
    require(len(raw_nonzero) > 0, "fixture_dual_pivot_raw_nonzero")
    prior_state, prior_leads, prior_rows, prior_head = _fixture_prior_state(
        root, separator, raw_q, character)
    coefficients = [{"pivot_id": pivot_id, "lead": lead,
                     "coefficient": int(raw_q[lead])}
                    for pivot_id, lead in enumerate(prior_leads)]
    remainder = raw_q.copy()
    for coefficient, row in zip(coefficients, prior_rows):
        factor = int(remainder[coefficient["lead"]])
        require(factor == coefficient["coefficient"], "fixture_prior_factor")
        remainder[:] = (remainder.astype(np.int16) - factor * row.astype(np.int16)) % 3
        remainder = remainder.astype(np.uint8)
    new_nonzero = np.flatnonzero(remainder)
    require(len(new_nonzero) > 0, "fixture_dual_pivot_remainder")
    raw_lead = int(raw_nonzero[0]); raw_lead_scalar = int(raw_q[raw_lead])
    new_lead = int(new_nonzero[0]); new_scalar = int(remainder[new_lead])
    pivot_scale = 1 if new_scalar == 1 else 2
    normalized = put("normalized-pivot.bin", pack_trits(
        (pivot_scale * remainder.astype(np.uint16) % 3).astype(np.uint8)))
    chain_body = {"schema": LIVE_SCHEMA + ".RawDualChain",
                  "separator_generation": separator["generation"],
                  "separator_s_head_sha256": separator["rolling_s_head"],
                  "lambda_sha256": separator["lambda_sha256"], "character": character,
                  "root": str(root), "root_node": root_node, "root_q_receipt": root_q,
                  "edges": edges, "children": children, "files": files,
                  "final_raw_dual_sha256": final["sha256"]}
    chain = {**chain_body, "sha256": sha(canonical(chain_body))}
    next_head = _dual_next_state_head(prior_head, len(prior_leads),
                                      new_lead, normalized["sha256"], final["sha256"],
                                      sha(pack_trits(remainder)), len(prior_leads) + 1)
    pivot_body = {"schema": LIVE_SCHEMA + ".DualPivot", "raw_dual_sha256": final["sha256"],
                  "prior_state_head_sha256": prior_head,
                  "prior_pivot_coefficients": coefficients,
                  "remainder_sha256": sha(pack_trits(remainder)), "raw_lead": raw_lead,
                  "raw_lead_scalar": raw_lead_scalar, "lead": new_lead, "scale": pivot_scale,
                  "normalized_pivot_sha256": normalized["sha256"],
                  "normalized_pivot": {"file": normalized["file"], "offset": 0,
                                       "length": normalized["bytes"], "sha256": normalized["sha256"]},
                  "rank_before": len(prior_leads), "insertion_id": len(prior_leads),
                  "dual_rank_after": len(prior_leads) + 1,
                  "next_state_head_sha256": next_head}
    pivot = {**pivot_body, "sha256": sha(canonical(pivot_body))}
    return chain, pivot, prior_state


def _build_fixture() -> dict[str, Any]:
    root = Path(tempfile.mkdtemp(prefix="d972-r07-grade2-live-v15-"))
    base_path, base_launch, universe = _fixture_base(root)
    separator_parent = _fixture_separator(root, base_path, base_launch)
    base = validate_base_launch(base_path)
    separator = validate_separator_parent(separator_parent, base)
    task_parent = {"root": str(Path(tempfile.gettempdir()) / "shadow-atelier-task712-9915928157"),
                   "run_id": 33814194630, "run_attempt": 1, "artifact_id": 9915928157,
                   "artifact_digest": TASK712_ARCHIVE_SHA}
    if not (Path(task_parent["root"]) / "r07-grade2-maps-v4" / "manifest.json").is_file():
        raise UnknownResource("UNKNOWN_RESOURCE:task712_accepted_fixture")
    tables = read_task712_envelope(task_parent, 0)
    chain, pivot, prior_state = _fixture_raw_chain(root, tables, separator, 0)
    launch = {"schema": LIVE_SCHEMA, "base_launch": str(base_path),
              "task712_parent": task_parent, "separator_parent": separator_parent,
              "raw_dual_chain": chain, "prior_dual_state": prior_state,
              "dual_pivot": pivot, "character": 0,
              "out": str(root / "scalar-result.json")}
    launch_path = root / "scalar-launch.json"; launch_path.write_bytes(canonical(launch))
    return {"root": root, "base_path": base_path, "launch_path": launch_path,
            "launch": launch, "base": base, "separator": separator, "tables": tables,
            "chain": chain, "pivot": pivot, "prior_state": prior_state,
            "universe": universe}


def scalar_live_owner(launch_path: Path) -> dict[str, Any]:
    launch, launch_raw = read_canonical(launch_path, 1 << 24, "scalar_live_launch")
    require(isinstance(launch, dict) and set(launch) ==
            {"schema", "base_launch", "task712_parent", "separator_parent",
             "raw_dual_chain", "prior_dual_state", "dual_pivot", "character", "out"} and
            launch["schema"] == LIVE_SCHEMA and plain_int(launch["character"]) and
            0 <= launch["character"] < 4, "scalar_live_launch")
    SCALAR_CALLS.update({key: 0 for key in SCALAR_CALLS})
    base = validate_base_launch(Path(launch["base_launch"]))
    tables = read_task712_envelope(launch["task712_parent"], launch["character"])
    separator_parent = launch["separator_parent"]
    separator = validate_separator_parent(separator_parent, base)
    prior_state = validate_prior_dual_state(launch["prior_dual_state"], separator,
                                           launch["character"])
    chain = launch["raw_dual_chain"]
    require(isinstance(chain, dict) and chain.get("character") == launch["character"],
            "scalar_launch_chain_character")
    final_raw, covectors = validate_raw_chain(chain, tables, separator)
    dual_replay = _validate_dual_pivot(launch["dual_pivot"], final_raw,
                         Path(chain["root"]).absolute(), chain["files"],
                         covectors[0], prior_state)
    cache = read_scalar_p1(base, launch["character"], covectors)
    relations = _global_relations(base["task554"], base["universe"])
    direct = direct_seed_evaluations(covectors[0], launch["character"])
    SCALAR_CALLS["seed_evaluations"] += len(direct)
    scalar_relations = {"actor_order": relations["actor_order"],
                        "seeds": [{"direct": direct[index], "terms": terms}
                                  for index, terms in enumerate(relations["seeds"])],
                        "actors": relations["actors"], "sha256": relations["sha256"],
                        "row_count": relations["row_count"], "eof": True}
    result = scan_scalar(final_raw, [np.asarray(v) for v in _p1_values(cache)],
                         scalar_relations, cache)
    envelope = {"schema": LIVE_SCHEMA + ".result", "launch_sha256": sha(launch_raw),
                "task712_manifest_sha256": tables["manifest_sha256"],
                "separator_generation": separator["generation"],
                "separator_s_head_sha256": separator["rolling_s_head"],
                "raw_dual_chain_sha256": chain["sha256"], "raw_dual": final_raw,
                "prior_dual_state_sha256": prior_state["sha256"],
                "dual_pivot": launch["dual_pivot"],
                "p1_manifest_sha256": cache["manifest_sha256"],
                "global_relation_stream_sha256": relations["sha256"],
                "value_vector_sha256": cache["value_sha256"], "result": result,
                "physical_provider": "NOT_READY:authenticated_physical_provider",
                "current_s_provider": "NOT_READY:authenticated_current_S_provider",
                "extra_open_count": cache["extra_open_count"],
                "throughput_rows_per_second": cache["throughput_rows_per_second"],
                "counters": dict(SCALAR_CALLS),
                "dual_replay": {"rank_before": prior_state["rank_before"],
                                "reduction_steps": dual_replay["reduction_steps"],
                                "new_lead": dual_replay["new_lead"],
                                "raw_lead": launch["dual_pivot"]["raw_lead"],
                                "raw_lead_scalar": launch["dual_pivot"]["raw_lead_scalar"]},
                "ACTUAL_GRADE2_SCALAR_RUN": False, "cross_checked": False,
                "GRADE2_MEMBER": "NOT_DECIDED", "GRADE2_NONMEMBER": "NOT_DECIDED",
                "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED",
                "COFINAL_LIFT": "NOT_DECLARED", "FAKE": "NOT_DECLARED",
                "IHARA": "NOT_DECLARED", "verified": False}
    out = Path(launch["out"]); out.write_bytes(canonical(envelope)); return envelope


def _p1_values(cache: dict[str, Any]) -> list[np.ndarray]:
    """The vectors are retained only in the scalar call; this helper is replaced below."""
    value = cache.get("_values")
    require(isinstance(value, list), "p1_values_lifetime")
    return value


def _expect_reject(action: Any, reason: str) -> None:
    try:
        action()
    except (RuntimeError, UnknownResource, NotReady):
        return
    raise RuntimeError(reason)


def scalar_selftest() -> dict[str, Any]:
    fixture = _build_fixture()
    envelope = scalar_live_owner(fixture["launch_path"])
    require(envelope["result"]["schema"] == LIVE_SCHEMA + ".ScalarEOF" and
            envelope["result"]["origins"] == 108 and
            envelope["extra_open_count"] == 0 and
            envelope["counters"]["p1_cache_passes"] == 1 and
            envelope["counters"]["p1_rows"] == 16 and
            envelope["counters"]["seed_evaluations"] == 44 and
            envelope["result"]["coefficient_stream_eof"] is True and
            envelope["result"]["p1_cache_pass_eof"] is True,
            "scalar_fixture_terminal")
    # The separator and raw-chain validators are exercised on their real files.
    base = validate_base_launch(fixture["base_path"])
    separator = validate_separator_parent(fixture["launch"]["separator_parent"], base)
    tables = read_task712_envelope(fixture["launch"]["task712_parent"], 0)
    final, covectors = validate_raw_chain(fixture["chain"], tables, separator)
    prior_state = validate_prior_dual_state(fixture["prior_state"], separator, 0)
    replay = _validate_dual_pivot(fixture["pivot"], final, fixture["root"],
                                  fixture["chain"]["files"], covectors[0], prior_state)
    require(prior_state["rank_before"] == 2 and replay["reduction_steps"] == 2 and
            fixture["pivot"]["rank_before"] == 2 and
            fixture["pivot"]["insertion_id"] == 2 and
            fixture["pivot"]["raw_lead_scalar"] == 2,
            "general_dual_pivot_fixture")
    bad_separator = json.loads(json.dumps(fixture["launch"]["separator_parent"]))
    bad_separator["manifest"] = dict(bad_separator["manifest"])
    bad_separator["manifest"]["sha256"] = "0" * 64
    _expect_reject(lambda: validate_separator_parent(bad_separator, base),
                   "separator_mutation_accepted")
    bad_chain = json.loads(json.dumps(fixture["chain"]))
    bad_chain["final_raw_dual_sha256"] = bad_chain["root_node"]["sha256"]
    unsigned = dict(bad_chain); unsigned.pop("sha256")
    bad_chain["sha256"] = sha(canonical(unsigned))
    _expect_reject(lambda: validate_raw_chain(bad_chain, tables, separator),
                   "raw_chain_mutation_accepted")
    bad_pivot = json.loads(json.dumps(fixture["pivot"]))
    bad_pivot["raw_dual_sha256"] = bad_pivot["raw_dual_sha256"][::-1]
    unsigned = dict(bad_pivot); unsigned.pop("sha256")
    bad_pivot["sha256"] = sha(canonical(unsigned))
    _expect_reject(lambda: _validate_dual_pivot(bad_pivot, final, fixture["root"],
                                                 fixture["chain"]["files"], covectors[0],
                                                 prior_state),
                   "dual_pivot_mutation_accepted")
    values = _p1_values(read_scalar_p1(base, 0, covectors))
    relations = _global_relations(base["task554"], base["universe"])
    direct = direct_seed_evaluations(covectors[0], 0)
    scalar_relations = {"actor_order": list(ACTORS),
                        "seeds": [{"direct": direct[i], "terms": relations["seeds"][i]}
                                  for i in range(44)],
                        "actors": relations["actors"], "sha256": relations["sha256"],
                        "row_count": relations["row_count"], "eof": True}
    changed = json.loads(json.dumps(scalar_relations))
    changed["seeds"][0]["direct"] = 1
    violation = scan_scalar(final, values, changed,
                            {"manifest_sha256": envelope["p1_manifest_sha256"],
                             "value_sha256": envelope["value_vector_sha256"], "rows": 16})
    require(violation["schema"] == LIVE_SCHEMA + ".Violation" and
            violation["raw_dual_sha256"] == final["sha256"] and
            violation["word_node_sha256"] == sha(canonical(final["word_node"])) and
            violation["scalar_prefix_digest"], "scalar_violation_join")
    stopped = False
    try:
        materialize_violation(violation)
    except NotReady as exc:
        stopped = str(exc) == "NOT_READY:authenticated_physical_provider"
    require(stopped, "materialization_provider_boundary")
    return {"schema": LIVE_SCHEMA + ".selftest", "status": "PASS",
            "rows": 16, "origins": 108, "nonempty_separator_rows": 2,
            "raw_chain_edges": len(fixture["chain"]["edges"]),
            "p1_cache_passes": envelope["counters"]["p1_cache_passes"],
            "extra_open_count": envelope["extra_open_count"],
            "bounded_throughput_rows_per_second": envelope["throughput_rows_per_second"],
            "dense_defect_matrix": False, "physical_provider": "NOT_READY",
            "current_s_provider": "NOT_READY", "verified": False}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    group = result.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true")
    group.add_argument("--task712-smoke", type=Path, metavar="ROOT")
    group.add_argument("--scalar-run", type=Path, metavar="LAUNCH")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.selftest:
            print(json.dumps(scalar_selftest(), sort_keys=True))
            return 0
        if args.task712_smoke is not None:
            parent = {"root": str(args.task712_smoke), "run_id": 33814194630,
                      "run_attempt": 1, "artifact_id": 9915928157,
                      "artifact_digest": TASK712_ARCHIVE_SHA}
            tables = read_task712_envelope(parent, 0)
            print(json.dumps({"status": "PASS", "manifest_sha256": tables["manifest_sha256"],
                              "used_tables": len(tables["forward"]), "verified": False},
                             sort_keys=True))
            return 0
        require(args.scalar_run is not None, "scalar_run_arguments")
        print(json.dumps(scalar_live_owner(args.scalar_run), sort_keys=True))
        return 0
    except NotReady as exc:
        print(json.dumps({"status": "NOT_READY", "error": str(exc),
                          "verified": False}, sort_keys=True), file=sys.stderr)
        return 2
    except UnknownResource as exc:
        print(json.dumps({"status": "UNKNOWN_RESOURCE", "error": str(exc),
                          "verified": False}, sort_keys=True), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc),
                          "verified": False}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
