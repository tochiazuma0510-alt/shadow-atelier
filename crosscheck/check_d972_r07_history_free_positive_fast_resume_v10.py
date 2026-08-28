#!/usr/bin/env python3
"""Helper-nonshared checker for the R07 v9 positive resume.

The producer is authenticated as bytes but never imported.  UNKNOWN is a
bounded physical transport check.  COMMON independently rebuilds the light
E3/E4 owners and replays only the selected formal support.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import stat
import struct
import sys
import tempfile
import types
import zlib
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-history-free-positive-fast-resume/v10"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint"
VERDICT_SCHEMA = SCHEMA + "/verdict"
COMMON = "R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD"
CHECKER_PREFIX = "R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_CHECKER_TERMINAL"
SELFTEST_TERMINAL = "R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_SELFTEST_PASS"
MAX_CANDIDATE_BYTES = 512 * 1024 * 1024
MAX_CHECKPOINT_BYTES = 4_000_000_000
OLD_PIVOT_ROWS_SHA256 = "3c645f4e352c96691dd35d6202bdf5f8b2cce73b7eb5f1bdf33a8daa06ce9d28"
RAW_BYTES = 86_368_039
RAW_SHA256 = "c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab"
FIXTURE_PATH = "search/certs/d972_r07_history_free_positive_fast_resume_selftest_v10_20260829.json"
FALSE_CLAIMS = {"common_word": False, "finite_common_word": False,
                "separator": False, "negative": False, "cofinal_lift": False,
                "fake": False, "ihara_witness": False}
POSITIVE_CLAIMS = {**FALSE_CLAIMS, "common_word": True,
                   "finite_common_word": True}

# Must match the producer's public source snapshot ledger exactly.
SOURCE_PINS: dict[str, tuple[str, int, str]] = {
    "commission": ("sol/luna_task_342_r07_a0_v7_fast_positive_resume.md", 15393,
                   "9fca7eb266b433436f44a25f0b984d6941c5a1696e960a80e062c5abefcc028d"),
    "audit337": ("sol/sol_reply_337_r07_task325_v6_code_performance_audit_v1.md", 42611,
                 "035f3d987746f9662fb66da512889da7ad4f7ad899a3cc768e626093ce050f4a"),
    "proof265": ("sol/proof_r07_history_free_positive_common_word_verifier_v265.md", 10122,
                 "fd30ccb2458691ec7844d304f220a4be7d704259318c452f928f8088552ecb0a"),
    "proof275": ("sol/proof_r07_two_way_basis_checkpoint_resume_v275.md", 7662,
                 "51febdaadcdf9130af4dd0586969f28f533ff3e9d06d883841aa115410dd40ea"),
    "proof276": ("sol/proof_r07_triangular_checkpoint_basis_resume_v276.md", 5571,
                 "5765aec25e08e687841451d3707ba16e0f3e2c6c4d9de6c120e92bdafe071abb"),
    "proof277": ("sol/proof_r07_boundary_first_lazy_runtime_resume_v277.md", 9070,
                 "2539fa530195b7c5fe7035d2261301ed85c471af2df313fd33fb01e96df9a56d"),
    "proof278": ("sol/proof_r07_selected_support_positive_replay_v278.md", 7055,
                 "f9dcb97c86e401bd96a92805b6c31428483d624874388bcc0439d1f7dc2f390b"),
    "audit279": ("sol/audit_r07_task298_six_hour_cancel_no_artifact_v279.md", 3844,
                 "f669705e93a5ad3c84fb94a5b7f8ec4cf3cedd103df1e0b1d78460e9c8b1f5c9"),
    "live": ("search/d972_r07_positive_common_word_colgen_v1.py", 123870,
             "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    "task175": ("search/d972_r07_all_seven_raw_bridge_preflight_v1.py", 60306,
                "1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"),
    "task176": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109,
                "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "q3": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
           "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "joint_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036,
                      "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "old": ("search/d972_b345_seedspan_triple4_v1.py", 535219,
            "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    "old_bridge": ("search/d972_b345_triple_cube_raw_lambda_census_v1.py", 126942,
                   "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"),
    "joint": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945,
              "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "v172": ("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", 21918,
             "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"),
    "g760": ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409,
             "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"),
    "pb4": ("search/d972_b345_target6_dual_colgen_v2.py", 444497,
            "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"),
    "manifest": ("ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.manifest.json", 1328,
                 "6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302"),
    "fixture": (FIXTURE_PATH, 3785,
                "de6273d681238b1aa560353c70a245cc28823326908e31be464fa2c399917203"),
    "task176_receipt": ("ci/in/d972_r07_all_seven_extension_section_census_v1.json", 13649089,
                        "715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41"),
    "task176_manifest": ("ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json", 349,
                         "de62e5e55a2e348a3cce297764f7ff4bfedc10ebe2545f22cbc1551f15e1adc1"),
    "task176_crosscheck": ("ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.json", 757,
                           "e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5"),
    "task176_recovery": ("ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.json", 2035,
                         "41d2cb72614ce7e2d5b2d7a9000e861414da1c749876b3d51f1ccf2ca63390a8"),
    "task176_recovery_v2": ("ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.v2.json", 2690,
                            "67dd555f6e0f943d0161ef2f2c8124b4cc31c9167846b45b43fd2001f5fbba3f"),
}

# Filled from the frozen producer after its last edit.
PRODUCER_PIN = ("search/d972_r07_history_free_positive_fast_resume_v10.py",
                147892,
                "235a798e097a7388603a72462a4fef28d9a7e044c47e4339eb4e30714bd9e472")


class CheckStop(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckStop(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(canonical(value))


def validate_dag_nodes(nodes: Any) -> None:
    require(type(nodes) is list and nodes and nodes[0] == ["zero"],
            "DAG zero root")
    seen: set[tuple[Any, ...]] = set()
    for index, raw in enumerate(nodes):
        require(type(raw) is list and raw, "DAG node shape")
        node = tuple(raw); opcode = node[0]
        require(node not in seen, "DAG hash-cons duplicate")
        seen.add(node)
        if opcode == "zero":
            require(index == 0 and len(node) == 1, "DAG zero opcode")
        elif opcode == "literal":
            require(len(node) == 2 and type(node[1]) is list and
                    all(type(item) is list and len(item) == 2 and
                        type(item[0]) is str and item[1] in (1, 2)
                        for item in node[1]), "DAG literal opcode")
        elif opcode == "add":
            require(len(node) == 4 and type(node[1]) is int and
                    type(node[2]) is int and type(node[3]) is int and
                    0 <= node[1] < index and 0 <= node[2] < index and
                    node[3] in (1, 2), "DAG add opcode")
        else:
            require(False, "DAG unknown opcode")


def seal(value: dict[str, Any]) -> dict[str, Any]:
    answer = dict(value); answer.pop("self_digest", None)
    answer["self_digest"] = sha_obj(answer)
    return answer


def validate_seal(value: dict[str, Any]) -> None:
    claimed = value.get("self_digest")
    body = dict(value); body.pop("self_digest", None)
    require(type(claimed) is str and claimed == sha_obj(body), "outer seal")


def read_owner_bytes(path: Path, size: int, digest: str) -> tuple[bytes, dict[str, Any]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise CheckStop("owner open") from exc
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                before.st_size == size, "owner physical identity")
        raw = bytearray(size); offset = 0
        while offset < size:
            chunk = os.read(fd, min(1 << 20, size - offset))
            require(chunk, "owner short read")
            raw[offset:offset + len(chunk)] = chunk; offset += len(chunk)
        require(not os.read(fd, 1), "owner long read")
        after = os.fstat(fd)
        opened_before = (before.st_dev, before.st_ino, before.st_size,
                         before.st_mtime_ns, before.st_nlink)
        opened_after = (after.st_dev, after.st_ino, after.st_size,
                        after.st_mtime_ns, after.st_nlink)
        require(opened_before == opened_after, "owner fd TOCTOU")
        path_after = os.lstat(path)
        pathname = (path_after.st_dev, path_after.st_ino, path_after.st_size,
                    path_after.st_mtime_ns, path_after.st_nlink)
        require(not stat.S_ISLNK(path_after.st_mode) and pathname == opened_before,
                "owner pathname TOCTOU")
        raw_bytes = bytes(raw)
        require(sha_bytes(raw_bytes) == digest, "owner digest")
        return raw_bytes, {"device": before.st_dev, "inode": before.st_ino,
                           "bytes": size, "links": before.st_nlink,
                           "mtime_ns": before.st_mtime_ns, "sha256": digest}
    finally:
        os.close(fd)


class Sources:
    def __init__(self) -> None:
        self.raw: dict[str, bytes] = {}
        self.modules: dict[str, Any] = {}
        self.objects: dict[str, Any] = {}

    def authenticate(self) -> None:
        pins = dict(SOURCE_PINS)
        pins["producer"] = PRODUCER_PIN
        for key, (relative, size, digest) in pins.items():
            path = ROOT / relative
            raw, _identity = read_owner_bytes(path, size, digest)
            self.raw[key] = raw

    def load(self, key: str) -> Any:
        if key in self.modules:
            return self.modules[key]
        name = "_d972_v9_checker_" + key
        require(name not in sys.modules, "checker module slot")
        module = types.ModuleType(name)
        module.__file__ = str((ROOT / SOURCE_PINS[key][0]).resolve())
        module.__package__ = ""
        sys.modules[name] = module
        try:
            exec(compile(self.raw[key], module.__file__, "exec"), module.__dict__)
        except BaseException:
            sys.modules.pop(name, None); raise
        self.modules[key] = module
        return module

    def json(self, key: str) -> Any:
        if key not in self.objects:
            self.objects[key] = json.loads(self.raw[key].decode("utf-8"))
        return self.objects[key]

    @staticmethod
    def public() -> dict[str, Any]:
        return {key: {"path": row[0], "bytes": row[1], "sha256": row[2]}
                for key, row in SOURCE_PINS.items()}


TASK176_RECEIPT_DIGEST = "f8f0ce249ff547d3e1235bd4b9760daa2b34b23771bf7da47b48dbd5cbbfae1d"
TASK176_RECOVERY_V1_DIGEST = "f8c6c0faf2588cd58d8a2aec75a2a1f9950ea67769dd913fbd796d018098f581"
TASK176_RECOVERY_V2_DIGEST = "e95b4e7781a14cffd07d445141f20c942861168d201f2ce62879a0ddf3a45026"


def validate_task176_authority(sources: Sources) -> dict[str, Any]:
    receipt = sources.json("task176_receipt")
    manifest = sources.json("task176_manifest")
    verdict = sources.json("task176_crosscheck")
    recovery_v1 = sources.json("task176_recovery")
    recovery = sources.json("task176_recovery_v2")
    require(receipt.get("schema") ==
            "d972-r07-all-seven-extension-section-census/v1" and
            receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS" and
            receipt.get("self_digest_sha256") == TASK176_RECEIPT_DIGEST,
            "task176 receipt authority")
    require(manifest == {"artifact_id": "9635036013", "head":
            "0533e42019c9f67f6cec3d1566152db17b903836", "member":
            "d972_r07_all_seven_extension_section_census_v1.json",
            "member_bytes": 13649089, "member_sha256":
            "715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41",
            "run": "33044121344", "zip_sha256":
            "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912"},
            "task176 original manifest binding")
    require(verdict.get("schema") ==
            "d972-r07-all-seven-extension-section-census-check/v1" and
            verdict.get("grade") == "CROSS_CHECKED" and
            verdict.get("producer_sha256") == SOURCE_PINS["task176"][2] and
            verdict.get("receipt_bytes") == 13649089 and
            verdict.get("receipt_sha256") == SOURCE_PINS["task176_receipt"][2] and
            verdict.get("receipt_terminal") == receipt["terminal"],
            "task176 accepted checker binding")
    require(recovery_v1.get("schema") ==
            "d972-r07-all-seven-extension-section-census-recovery-manifest/v1" and
            recovery_v1.get("self_digest_sha256") == TASK176_RECOVERY_V1_DIGEST,
            "task176 superseded recovery-v1 identity")
    require(recovery.get("schema") ==
            "d972-r07-all-seven-extension-section-census-recovery-manifest/v2" and
            recovery.get("self_digest_sha256") == TASK176_RECOVERY_V2_DIGEST and
            recovery.get("execution") == "UNEXECUTED" and
            recovery.get("mathematical_grade_change") is False and
            recovery.get("supersedes") == {"bytes": 2035,
                "path": SOURCE_PINS["task176_recovery"][0],
                "self_digest_sha256": TASK176_RECOVERY_V1_DIGEST,
                "sha256": SOURCE_PINS["task176_recovery"][2]} and
            recovery.get("correction") == {
                "json_pointer": "/accepted_receipt/self_digest_sha256",
                "old_value": "f8f0ce249ff547d3e1235bd4b9760daa2b34f23771bf7da47b48dbd5cbbfae1d",
                "new_value": TASK176_RECEIPT_DIGEST,
                "reason": "transcription mismatch against physical accepted receipt and reply348"} and
            recovery.get("accepted_receipt") == {"bytes": 13649089,
                "path": "ci/in/d972_r07_all_seven_extension_section_census_v1.json",
                "self_digest_sha256": TASK176_RECEIPT_DIGEST,
                "sha256": SOURCE_PINS["task176_receipt"][2]} and
            recovery.get("receipt_manifest") == {"bytes": 349,
                "path": "ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json",
                "sha256": SOURCE_PINS["task176_manifest"][2]} and
            recovery.get("recovered_verdict") == {"bytes": 757,
                "path": "ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.json",
                "self_digest_sha256": verdict.get("self_digest_sha256"),
                "sha256": SOURCE_PINS["task176_crosscheck"][2]} and
            recovery.get("physical_sources") == {
                "producer": {"bytes": SOURCE_PINS["task176"][1],
                    "path": SOURCE_PINS["task176"][0],
                    "sha256": SOURCE_PINS["task176"][2]},
                "checker": {"bytes": 84980,
                    "path": "crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py",
                    "sha256": "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"}} and
            recovery.get("source_temp_member_names") == [
                "d972_r07_all_seven_extension_section_census_crosscheck_v1.json",
                "d972_r07_all_seven_extension_section_census_hashes_v1.txt",
                "d972_r07_all_seven_extension_section_census_v1.json"],
            "task176 recovery-v2 binding")
    return receipt


TASK176_BLOBS = {
    "q0_roster": ("result", "Q0_section", "canonical_roster", 52907904, 36, 1469664),
    "q0_parents": ("result", "Q0_section", "parent_states_u32le", 5878656, 4, 1469664),
    "q0_letters": ("result", "Q0_section", "parent_letters_u8", 1469664, 1, 1469664),
    "gamma_states": ("result", "Gamma", "ten_coordinate_states", 235710, 970, 243),
    "gamma_parents": ("result", "Gamma", "section_parent_states_u16le", 486, 2, 243),
    "gamma_records": ("result", "Gamma", "section_parent_record_u8", 243, 1, 243),
}


def decode_task176_blob(owner: dict[str, Any], raw_limit: int) -> bytes:
    require(owner.get("codec") == "zlib+base64" and
            owner.get("raw_bytes") == raw_limit and
            type(owner.get("data")) is str and
            type(owner.get("compressed_bytes")) is int and
            owner["compressed_bytes"] > 0, "task176 owner envelope")
    encoded = owner["data"].encode("ascii")
    try:
        compressed = base64.b64decode(encoded, validate=True)
    except (ValueError, UnicodeError) as exc:
        raise CheckStop("task176 strict base64") from exc
    require(len(compressed) == owner["compressed_bytes"],
            "task176 compressed size")
    require(base64.b64encode(compressed).decode("ascii") == owner["data"] and
            sha_bytes(compressed) == owner.get("compressed_sha256"),
            "task176 canonical compressed owner")
    inflater = zlib.decompressobj()
    try:
        decoded = inflater.decompress(compressed, raw_limit + 1)
    except zlib.error as exc:
        raise CheckStop("task176 zlib") from exc
    require(len(decoded) == raw_limit and inflater.eof and
            not inflater.unused_data and not inflater.unconsumed_tail and
            sha_bytes(decoded) == owner.get("raw_sha256"),
            "task176 lossless bounded decode")
    return decoded


def decode_task176_owners(sources: Sources) -> dict[str, Any]:
    receipt = sources.json("task176_receipt")
    decoded: dict[str, Any] = {"receipt": receipt}
    for name, (_root, section, field, raw_limit, width, count) in TASK176_BLOBS.items():
        owner = receipt["result"][section][field]
        raw = decode_task176_blob(owner, raw_limit)
        require(len(raw) == width * count, "task176 owner cardinality")
        decoded[name] = raw
    q0 = receipt["result"]["Q0_section"]
    gamma = receipt["result"]["Gamma"]
    marks = q0.get("ten_coordinate_marked_generator_blobs_hex")
    require(type(marks) is list and len(marks) == 10 and
            all(type(item) is list and len(item) == 2 and
                all(type(blob) is str and len(bytes.fromhex(blob)) ==
                    (40 if index < 5 else 154)
                    for blob in item)
                for index, item in enumerate(marks)),
            "task176 marked generator owner")
    decoded["marked_generators"] = tuple(
        (bytes.fromhex(item[0]), bytes.fromhex(item[1])) for item in marks)
    words = gamma.get("record_words")
    require(type(words) is list and len(words) == 26 and
            all(type(word) is list for word in words), "task176 gamma words")
    decoded["gamma_words"] = words
    validate_task176_q0_parent_owner(decoded["q0_parents"],
                                     decoded["q0_letters"], 1469664)
    validate_task176_gamma_parent_owner(decoded["gamma_parents"],
                                        decoded["gamma_records"], 243, 26)
    q3 = sources.json("q3")
    q3_marks = q3.get("coarse_models", {}).get("Q0", {}).get(
        "marked_permutations")
    require(type(q3_marks) is list and len(q3_marks) == 2 and
            all(type(row) is list and len(row) == 36 and
                set(row) == set(range(36)) for row in q3_marks),
            "q3 Q0 marked permutation owner")
    decoded["q0_marked_permutations"] = tuple(bytes(row) for row in q3_marks)
    return decoded


def task176_parent_walk(parents: bytes, letters: bytes, identifier: int,
                        count: int) -> list[int]:
    require(1 <= identifier <= count, "task176 selected identifier")
    current = identifier; seen: set[int] = set(); reversed_word: list[int] = []
    while current:
        require(current not in seen and len(seen) <= count, "task176 parent cycle")
        seen.add(current)
        parent = struct.unpack_from("<I", parents, (current - 1) * 4)[0]
        letter = letters[current - 1]
        require(0 <= parent < current and
                ((parent == 0 and letter == 0) or
                 (parent != 0 and letter in (1, 2))),
                "task176 chronological parent")
        if parent != 0: reversed_word.append(int(letter))
        current = parent
    return list(reversed(reversed_word))


def validate_task176_q0_parent_owner(parents: bytes, letters: bytes,
                                     count: int) -> None:
    require(len(parents) == 4 * count and len(letters) == count,
            "task176 Q0 parent owner dimensions")
    roots = 0
    for current in range(1, count + 1):
        parent = struct.unpack_from("<I", parents, (current - 1) * 4)[0]
        letter = letters[current - 1]
        require(0 <= parent < current and
                ((parent == 0 and letter == 0) or
                 (parent != 0 and letter in (1, 2))),
                "task176 Q0 parent grammar")
        if parent == 0: roots += 1
    require(roots == 1, "task176 Q0 unique root")


def task176_gamma_walk(parents: bytes, records: bytes, words: list[list[int]],
                        identifier: int) -> list[int]:
    current = identifier; seen: set[int] = set(); chunks: list[list[int]] = []
    while current:
        require(current not in seen and 1 <= current <= 243 and len(seen) <= 243,
                "task176 Gamma parent cycle")
        seen.add(current)
        parent = struct.unpack_from("<H", parents, (current - 1) * 2)[0]
        record = records[current - 1]
        require(parent < current and
                ((parent == 0 and record == 0) or
                 (parent != 0 and 1 <= record <= len(words))),
                "task176 Gamma chronological parent")
        if parent != 0:
            chunks.append([int(letter) for letter in words[record - 1]])
        current = parent
    answer: list[int] = []
    for chunk in reversed(chunks): answer.extend(chunk)
    return answer


def validate_task176_gamma_parent_owner(parents: bytes, records: bytes,
                                        count: int, word_count: int) -> None:
    require(len(parents) == 2 * count and len(records) == count and
            word_count == 26, "task176 Gamma parent owner dimensions")
    roots = 0
    for current in range(1, count + 1):
        parent = struct.unpack_from("<H", parents, (current - 1) * 2)[0]
        record = records[current - 1]
        require(0 <= parent < current and
                ((parent == 0 and record == 0) or
                 (parent != 0 and 1 <= record <= word_count)),
                "task176 Gamma parent grammar")
        if parent == 0: roots += 1
    require(roots == 1, "task176 Gamma unique root")


def q0_perm_mul(left: bytes, right: bytes) -> bytes:
    require(type(left) is bytes and type(right) is bytes and
            len(left) == len(right) == 36 and
            set(left) == set(range(36)) and set(right) == set(range(36)),
            "Q0 marked permutation representation")
    return bytes(left[index] for index in right)


def replay_q0_marked_permutations(qword: Sequence[int], marks: tuple[bytes, bytes]) -> bytes:
    require(len(marks) == 2 and all(type(row) is bytes and len(row) == 36
                                     for row in marks),
            "Q0 marked-generator roster")
    # Q0 has two independent 36-point marked generators.  Replay the
    # one-based parent word locally; no task176 composite helper is imported.
    value = bytes(range(36))
    for letter in qword:
        require(letter in (1, 2), "Q0 word alphabet")
        value = q0_perm_mul(value, marks[0 if letter == 1 else 1])
    return value


def replay_typed_ten_state(runtime: dict[str, Any], word: Sequence[int]) -> bytes:
    values = runtime["model"].coordinates(word)
    require(type(values) is list and len(values) == 10,
            "typed ten-coordinate replay cardinality")
    widths = [40] * 5 + [154] * 5
    require(all(type(value) is bytes and len(value) == width
                for value, width in zip(values, widths)),
            "typed ten-coordinate replay widths")
    return b"".join(values)


def reconstruct_task176_selected(runtime: dict[str, Any], section: dict[str, Any]) -> None:
    owners = runtime.get("task176_owners")
    require(type(owners) is dict, "task176 owners absent")
    qid, gid = int(section.get("q0_state_id")), int(section.get("gamma_state_id"))
    qword = task176_parent_walk(owners["q0_parents"], owners["q0_letters"], qid, 1469664)
    qrecord = owners["q0_roster"][(qid - 1) * 36:qid * 36]
    grecord = owners["gamma_states"][(gid - 1) * 970:gid * 970]
    gparents = owners["gamma_parents"][(gid - 1) * 2:gid * 2]
    grecord_parent = owners["gamma_records"][gid - 1]
    gword = task176_gamma_walk(owners["gamma_parents"], owners["gamma_records"],
                               owners["gamma_words"], gid)
    require(1 <= gid <= 243 and len(qrecord) == 36 and len(grecord) == 970 and
            len(gparents) == 2 and
            ((gparents == b"\x00\x00" and grecord_parent == 0) or
             grecord_parent in range(1, 27)) and
            (grecord_parent == 0 or
             type(owners["gamma_words"][grecord_parent - 1]) is list),
            "task176 selected record bounds")
    q0_replayed = replay_q0_marked_permutations(
        qword, owners["q0_marked_permutations"])
    q0_marks = (runtime["model"].coordinates([1]),
                runtime["model"].coordinates([2]))
    for coordinate, row in enumerate(owners["marked_generators"]):
        require(row[0] == q0_marks[0][coordinate] and row[1] == q0_marks[1][coordinate],
                "task176 selected typed marked-generator replay")
    require(section.get("q0_state_hex") == qrecord.hex() and
            q0_replayed == qrecord and
            type(section.get("q0_ten_coordinate_blobs_hex")) is list and
            section.get("q0_ten_coordinate_blobs_hex") == [
                value.hex() for value in runtime["model"].coordinates(qword)] and
            type(section.get("gamma_projected_ten_state_hex")) is str and
            section.get("gamma_projected_ten_state_hex") == grecord.hex() and
            replay_typed_ten_state(runtime, gword) == grecord,
            "task176 selected independent Q0/Gamma replay")
    require(type(section.get("selected_q0_word", qword)) is list and
            section.get("selected_q0_word", qword) == qword and
            type(section.get("selected_gamma_word", gword)) is list and
            section.get("selected_gamma_word", gword) == gword,
            "task176 selected parent-word binding")


def open_physical(path: Path, maximum: int, expected: dict[str, Any] | None = None,
                  mutation_hook: Any | None = None) -> tuple[dict[str, Any], bytes,
                                                             dict[str, Any]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise CheckStop("physical open") from exc
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                0 < before.st_size <= maximum, "physical regular unique owner")
        if expected is not None:
            require(before.st_size == expected["bytes"], "physical expected size")
        if mutation_hook is not None:
            mutation_hook(path)
        raw = bytearray()
        while len(raw) < before.st_size:
            chunk = os.read(fd, min(1 << 20, before.st_size - len(raw)))
            require(bool(chunk), "physical short read")
            raw.extend(chunk)
        require(not os.read(fd, 1), "physical long read")
        after = os.fstat(fd)
        require((before.st_dev, before.st_ino, before.st_size, before.st_nlink,
                 before.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
                 after.st_mtime_ns), "physical fd TOCTOU")
        try:
            path_after = os.lstat(path)
        except OSError as exc:
            raise CheckStop("physical pathname substituted") from exc
        require(not stat.S_ISLNK(path_after.st_mode) and
                (path_after.st_dev, path_after.st_ino, path_after.st_size,
                 path_after.st_nlink, path_after.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size,
                 after.st_nlink, after.st_mtime_ns),
                "physical pathname identity")
        raw_bytes = bytes(raw); digest = sha_bytes(raw_bytes)
        if expected is not None:
            require(digest == expected["sha256"], "physical expected digest")
        try:
            value = json.loads(raw_bytes.decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise CheckStop("physical JSON") from exc
        require(type(value) is dict, "physical JSON object")
        return value, raw_bytes, {"device": before.st_dev, "inode": before.st_ino,
            "bytes": before.st_size, "links": before.st_nlink,
            "mtime_ns": before.st_mtime_ns, "sha256": digest,
            "single_fd": True, "no_follow": True}
    finally:
        os.close(fd)


Sparse = dict[bytes, int]


def reduce_word(word: Iterable[int]) -> list[int]:
    answer: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter != 0 and abs(letter) in (1, 2, 3, 4, 5, 6),
                "free word letter")
        if answer and answer[-1] == -letter:
            answer.pop()
        else:
            answer.append(letter)
    return answer


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(letter) for letter in reversed(word)]


def exponent_pair(word: Sequence[int]) -> tuple[int, int]:
    return (sum(1 if x == 1 else -1 if x == -1 else 0 for x in word) % 3,
            sum(1 if x == 2 else -1 if x == -2 else 0 for x in word) % 3)


def paper_product(*displayed: Sequence[int]) -> list[int]:
    return reduce_word(letter for factor in reversed(displayed) for letter in factor)


def row_key(block: int, component: int, raw: bytes) -> bytes:
    require(block in (1, 2, 3) and 1 <= component <= 6, "row key type")
    return b"R" + bytes((block, component)) + len(raw).to_bytes(2, "big") + raw


def exponent_key(index: int) -> bytes:
    require(index in (1, 2), "exponent key")
    return b"E" + bytes((index,))


def decode_row_key(key: bytes) -> tuple[int, int, bytes]:
    require(len(key) >= 5 and key[:1] == b"R", "decode row key")
    width = int.from_bytes(key[3:5], "big")
    require(len(key) == width + 5 and key[1] in (1, 2, 3) and
            1 <= key[2] <= 6, "decode row width/type")
    return key[1], key[2], key[5:]


def add_scaled(target: Sparse, source: Sparse, scalar: int) -> None:
    scalar %= 3
    for key, coefficient in source.items():
        value = (target.get(key, 0) + scalar * int(coefficient)) % 3
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def scaled(source: Sparse, scalar: int) -> Sparse:
    return {key: int(value) * scalar % 3 for key, value in source.items()
            if int(value) * scalar % 3}


def pair(functional: Sparse, row: Sparse) -> int:
    return sum(int(value) * int(row.get(key, 0))
               for key, value in functional.items()) % 3


def public_sparse(row: Sparse) -> list[list[Any]]:
    return [[key.hex(), int(row[key]) % 3] for key in sorted(row)
            if int(row[key]) % 3]


def parse_sparse(rows: Sequence[Sequence[Any]]) -> Sparse:
    require(type(rows) is list, "sparse rows list")
    answer: Sparse = {}
    for item in rows:
        require(type(item) is list and len(item) == 2 and item[1] in (1, 2),
                "sparse item")
        key = bytes.fromhex(str(item[0]))
        require(key not in answer, "duplicate sparse key")
        answer[key] = int(item[1])
    require(public_sparse(answer) == list(rows), "canonical sparse order")
    return answer


def checker_packed_joint_blob(value: Any, label: str) -> bytes:
    require(type(value) is tuple and len(value) == 2,
            label + " tuple representation")
    permutation, pc = value
    require(type(permutation) in (bytes, tuple) and type(pc) is bytes,
            label + " component representation")
    degree = len(permutation)
    pc_width = {36: 4, 144: 10}.get(degree)
    require(pc_width is not None and len(pc) == pc_width and
            set(permutation) == set(range(degree)), label + " shape")
    return bytes(permutation) + pc


def checker_value_from_blob(raw: bytes, block: int) -> tuple[bytes, bytes]:
    degree = 36 if block in (1, 2) else 144
    width = degree + (4 if degree == 36 else 10)
    require(type(raw) is bytes and len(raw) == width and
            set(raw[:degree]) == set(range(degree)),
            "checker typed blob")
    return raw[:degree], raw[degree:]


def _serial_group(_unused: Any, row: dict[Any, int], block: int) -> Sparse:
    answer: Sparse = {}
    for (component, value), coefficient0 in row.items():
        coefficient = int(coefficient0) % 3
        if coefficient:
            raw = checker_packed_joint_blob(value, "checker group element")
            key = row_key(block, int(component), raw)
            answer[key] = (answer.get(key, 0) + coefficient) % 3
            if not answer[key]:
                del answer[key]
    return answer


def _serial_public(_unused: Any, row: dict[Any, int]) -> list[list[Any]]:
    result = []
    for (component, value), coefficient0 in row.items():
        coefficient = int(coefficient0) % 3
        if coefficient:
            result.append([int(component), checker_packed_joint_blob(
                value, "checker public element").hex(), coefficient])
    result.sort(key=lambda item: (item[0], bytes.fromhex(item[1])))
    return result


def build_checker_light(sources: Sources) -> dict[str, Any]:
    """Independent light reconstruction; no producer or old checker import."""
    old = sources.load("old")
    jointmod = sources.load("joint"); v172 = sources.load("v172")
    gmod = sources.load("g760"); pb4mod = sources.load("pb4")
    q3 = sources.json("q3")
    e3, e4, _ = old.reconstruct_quotients(q3)
    contexts, aliases, context_public = old.cheap_context_registry(e4)
    require(len(contexts) == 31 and len(context_public["named_uses"]) == 46,
            "checker context owner")
    words = [list(row["word"]) for row in q3["correction_fibre"]["records"]
             if row.get("word")]
    group, roster = v172.build_roster(jointmod, old, e3, e4, contexts, words)
    require(len(roster) == 6441 and
            all(group.eval(row["word"]) == group.identity for row in roster),
            "checker joint roster")
    _, _, g760 = gmod.construct_base()
    require(len(g760) == 760 and sha_obj(g760) ==
            "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d",
            "checker g760")
    h1, h2 = old.hexagon_words(g760)
    h1 = list(old.embed_f2_pb3(h1)); h2 = list(old.embed_f2_pb3(h2))
    pcontexts = [([1], [4]), ([4], [6]),
                 (paper_product([2], [4]), [6]),
                 (paper_product([1], [2]), paper_product([5], [6])),
                 ([1], paper_product([4], [5]))]
    factors = [old.f2_substitute(g760, left, right) for left, right in pcontexts]
    pword = paper_product(factors[1], factors[3], factors[0],
                          old.inv_word(factors[2]), old.inv_word(factors[4]))
    target: Sparse = {}
    base_public = {}
    for label, block, quotient, word in (("H1", 1, e3, h1),
                                         ("H2", 2, e3, h2),
                                         ("P", 3, e4, pword)):
        gradient, value = old.fox_gradient_without_sections(word, quotient)
        require(value == quotient.identity, "checker base identity")
        row = _serial_group(None, gradient, block)
        add_scaled(target, row, -1); base_public[label] = public_sparse(row)
    pb3_group = [old.fox_gradient_without_sections(row, e3)[0]
                 for row in old.pure_relations(3)]
    pb4_group = pb4mod.base_raw_columns(old, e4)
    require(len(pb3_group) == 2 and len(pb4_group) == 11 and
            all(old.d1(row, e3) == {} for row in pb3_group) and
            all(old.d1(row, e4) == {} for row in pb4_group),
            "checker boundary owners")
    runtime = {"old": old, "e3": e3, "e4": e4,
               "contexts": contexts, "aliases": aliases,
               "context_public": context_public, "joint_group": group,
               "roster": roster, "g760": list(g760), "target": target,
               "base_public": base_public,
               "boundary_group": {1: pb3_group, 2: pb3_group, 3: pb4_group},
               "pcontexts": pcontexts}
    runtime["model"] = IndependentAllSeven(runtime)
    light_public = {
        "source_snapshots_sha256": sha_obj(Sources.public()),
        "target_sha256": sha_obj(public_sparse(target)),
        "pb3_rows_sha256": sha_obj([_serial_public(None, row)
                                     for row in pb3_group]),
        "pb4_rows_sha256": sha_obj([_serial_public(None, row)
                                     for row in pb4_group]),
        "roster_sha256": sha_obj([[row["layer"], row["ordinal"], row["word"]]
                                    for row in roster]),
        "context_public_sha256": sha_obj(context_public),
        "e3_identity_hex": blob(runtime, e3.identity).hex(),
        "e4_identity_hex": blob(runtime, e4.identity).hex(),
        "no_q0_objects": True,
    }
    runtime["light_public"] = light_public
    runtime["light_input_sha256"] = sha_obj(light_public)
    return runtime


def group_for(runtime: dict[str, Any], block: int) -> Any:
    return runtime["e3"] if block in (1, 2) else runtime["e4"]


def unpack(runtime: dict[str, Any], raw: bytes, block: int) -> Any:
    return checker_value_from_blob(raw, block)


def blob(runtime: dict[str, Any], value: Any) -> bytes:
    return checker_packed_joint_blob(value, "checker typed element")


def boundary_row(runtime: dict[str, Any], block: int, relator: int,
                 translation_hex: str) -> Sparse:
    rows = runtime["boundary_group"][block]
    require(1 <= relator <= len(rows), "checker boundary relator")
    quotient = group_for(runtime, block)
    translation = unpack(runtime, bytes.fromhex(translation_hex), block)
    answer: Sparse = {}
    for (component, value), coefficient0 in rows[relator - 1].items():
        translated = quotient.mul(translation, value)
        key = row_key(block, int(component), blob(runtime, translated))
        coefficient = int(coefficient0) % 3
        answer[key] = (answer.get(key, 0) + coefficient) % 3
        if not answer[key]:
            del answer[key]
    return answer


class IndependentAllSeven:
    def __init__(self, runtime: dict[str, Any]) -> None:
        self.rt = runtime; self.old = runtime["old"]
        self.e3, self.e4 = runtime["e3"], runtime["e4"]
        self.g = runtime["g760"]
        x, y = [1], [2]
        z = self.old.inv_word(self.old.pp_words([x, y]))
        u = self.old.inv_word(self.old.pp_words([y, x]))
        raw_specs = [(1, self.e3, x, y, 1, True, "H1_fxy"),
            (1, self.e3, x, z, -1, True, "H1_fxz"),
            (1, self.e3, y, z, 1, True, "H1_fyz"),
            (2, self.e3, u, x, -1, True, "H2_fux"),
            (2, self.e3, x, y, -1, True, "H2_fxy"),
            (2, self.e3, u, y, 1, True, "H2_fuy")]
        for natural, label in ((1, "P_b1"), (3, "P_b2"), (0, "P_b3"),
                               (2, "P_b5_inverse"), (4, "P_b4_inverse")):
            left, right = runtime["pcontexts"][natural]
            raw_specs.append((3, self.e4, left, right,
                              -1 if natural in (2, 4) else 1, False, label))
        self.specs = []
        for block, quotient, left, right, sign, lift, label in raw_specs:
            base = self._substitute(self.g, left, right, lift)
            factor = base if sign > 0 else self.old.inv_word(base)
            self.specs.append({"block": block, "quotient": quotient,
                "left": left, "right": right, "sign": sign, "lift": lift,
                "label": label, "base_factor": factor})
        for block in (1, 2, 3):
            prefix = group_for(runtime, block).identity
            indices = [index for index, spec in enumerate(self.specs)
                       if spec["block"] == block]
            for index in reversed(indices):
                self.specs[index]["prefix"] = prefix
                prefix = group_for(runtime, block).mul(prefix,
                    group_for(runtime, block).eval(self.specs[index]["base_factor"]))
            require(prefix == group_for(runtime, block).identity,
                    "checker base prefix identity")
        for spec in self.specs:
            spec["occurrence_prefix"] = spec["prefix"]
            if spec["sign"] > 0:
                spec["occurrence_prefix"] = spec["quotient"].mul(
                    spec["prefix"], spec["quotient"].eval(spec["base_factor"]))

    def _substitute(self, word: Sequence[int], left: Sequence[int],
                    right: Sequence[int], lift: bool) -> list[int]:
        result = self.old.f2_substitute(list(word), list(left), list(right))
        return list(self.old.embed_f2_pb3(result)) if lift else list(result)

    def occurrence_column(self, delta: Sequence[int], relator: Sequence[int]) -> Sparse:
        answer: Sparse = {}
        for spec in self.specs:
            quotient = spec["quotient"]
            relation = self._substitute(relator, spec["left"], spec["right"],
                                        spec["lift"])
            if spec["sign"] < 0:
                relation = list(self.old.inv_word(relation))
            gradient, value = self.old.fox_gradient_without_sections(relation, quotient)
            require(value == quotient.identity, "checker occurrence relation")
            qword = self._substitute(delta, spec["left"], spec["right"], spec["lift"])
            translated = self.old.translate_vector(
                self.old.translate_vector(gradient, quotient.eval(qword), quotient),
                spec["occurrence_prefix"], quotient)
            add_scaled(answer, _serial_group(None, translated,
                                             spec["block"]), 1)
        e1, e2 = exponent_pair(relator)
        if e1: answer[exponent_key(1)] = e1
        if e2: answer[exponent_key(2)] = e2
        return answer

    def coordinates(self, word: Sequence[int]) -> list[bytes]:
        """Ten independent E3/E4 coordinate blobs for a literal F2 word."""
        values = []
        for spec, coordinate in zip(self.specs,
                                    (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)):
            qword = self._substitute(word, spec["left"], spec["right"], spec["lift"])
            value = spec["quotient"].eval(qword)
            while len(values) <= coordinate:
                values.append(None)
            if values[coordinate] is None:
                values[coordinate] = blob(self.rt, value)
            else:
                require(values[coordinate] == blob(self.rt, value),
                        "checker repeated coordinate")
        require(len(values) == 10 and all(type(value) is bytes for value in values),
                "checker complete coordinates")
        return values

    def occurrence_data(self, relator: Sequence[int], dual: Sparse) -> dict[str, Any]:
        merged: dict[tuple[int, bytes], int] = {}
        occurrence_rows = []
        coordinate_order = (0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9)
        for ordinal, (spec, coordinate) in enumerate(zip(self.specs,
                                                          coordinate_order), 1):
            quotient = spec["quotient"]
            relation = self._substitute(relator, spec["left"], spec["right"],
                                        spec["lift"])
            if spec["sign"] < 0:
                relation = list(self.old.inv_word(relation))
            gradient, value = self.old.fox_gradient_without_sections(relation, quotient)
            require(value == quotient.identity, "checker formula relation")
            prefix_inverse = quotient.inverse(spec["occurrence_prefix"])
            count = 0
            for (component, base_value), base_coefficient in gradient.items():
                base_inverse = quotient.inverse(base_value)
                for key, lambda_coefficient in dual.items():
                    if key[:1] != b"R":
                        continue
                    block, dual_component, target_raw = decode_row_key(key)
                    if block != spec["block"] or dual_component != int(component):
                        continue
                    target = unpack(self.rt, target_raw, block)
                    required = quotient.mul(quotient.mul(prefix_inverse, target),
                                            base_inverse)
                    merged_key = (coordinate, blob(self.rt, required))
                    coefficient = int(base_coefficient) * int(lambda_coefficient) % 3
                    if coefficient:
                        value0 = (merged.get(merged_key, 0) + coefficient) % 3
                        if value0:
                            merged[merged_key] = value0
                        else:
                            merged.pop(merged_key, None)
                        count += 1
            occurrence_rows.append({"ordinal": ordinal, "label": spec["label"],
                "coordinate": coordinate, "factor_sign": spec["sign"],
                "raw_dual_pair_terms": count})
        e1, e2 = exponent_pair(relator)
        constant = (dual.get(exponent_key(1), 0) * e1 +
                    dual.get(exponent_key(2), 0) * e2) % 3
        ordered = sorted(merged.items(), key=lambda item: (item[0][0], item[0][1]))
        public = {"K": constant,
            "terms": [[coordinate, raw.hex(), coefficient]
                      for (coordinate, raw), coefficient in ordered],
            "same_target_merged_mod3": True, "zero_sums_deleted": True,
            "eleven_occurrences": occurrence_rows}
        return {"constant": constant, "merged": merged, "public": public}

    def _pentagon(self, word: Sequence[int]) -> list[int]:
        factors = [self.old.f2_substitute(list(word), left, right)
                   for left, right in self.rt["pcontexts"]]
        return paper_product(factors[1], factors[3], factors[0],
                             self.old.inv_word(factors[2]),
                             self.old.inv_word(factors[4]))

    def direct_column(self, delta: Sequence[int], relator: Sequence[int]) -> tuple[Sparse,
                                                                                   dict[str, Any]]:
        conjugate = reduce_word(list(delta) + list(relator) + inverse_word(delta))
        require(self.rt["joint_group"].eval(conjugate) ==
                self.rt["joint_group"].identity, "checker conjugate joint kernel")
        corrected = reduce_word(self.g + conjugate)
        base_hex = self.old.hexagon_words(self.g)
        corrected_hex = self.old.hexagon_words(corrected)
        words = [(1, self.e3, list(self.old.embed_f2_pb3(base_hex[0])),
                  list(self.old.embed_f2_pb3(corrected_hex[0]))),
                 (2, self.e3, list(self.old.embed_f2_pb3(base_hex[1])),
                  list(self.old.embed_f2_pb3(corrected_hex[1]))),
                 (3, self.e4, self._pentagon(self.g), self._pentagon(corrected))]
        answer: Sparse = {}; quotient_values = []
        for block, quotient, base_word, corrected_word in words:
            base_gradient, base_value = self.old.fox_gradient_without_sections(
                base_word, quotient)
            corrected_gradient, corrected_value = self.old.fox_gradient_without_sections(
                corrected_word, quotient)
            require(base_value == quotient.identity and corrected_value == quotient.identity,
                    "checker direct all-seven identity")
            difference = dict(corrected_gradient)
            for key, coefficient in base_gradient.items():
                value = (difference.get(key, 0) - int(coefficient)) % 3
                if value: difference[key] = value
                else: difference.pop(key, None)
            add_scaled(answer, _serial_group(None, difference, block), 1)
            quotient_values.append(blob(self.rt, corrected_value).hex())
        e1, e2 = exponent_pair(conjugate)
        if e1: answer[exponent_key(1)] = e1
        if e2: answer[exponent_key(2)] = e2
        occurrence = self.occurrence_column(delta, relator)
        require(answer == occurrence, "checker all eleven/direct equality")
        return answer, {"delta_word": list(delta), "relator_word": list(relator),
            "conjugate_word": conjugate, "corrected_word": corrected,
            "quotient_value_blobs": quotient_values,
            "eleven_occurrence_replay": True, "direct_all_seven_replay": True}


EXPECTED_TRIANGULAR = {
    "columns": 2896, "rank": 2896, "boundary_columns": 2896,
    "correction_columns": 0, "raw_support_total": 20354,
    "raw_support_max": 12, "ancestry_entries_total": 137926,
    "ancestry_entries_max": 258,
    "ancestry_weighted_contributions": 1011460,
    "pivot_support_total": 289774, "pivot_support_max": 522,
    "future_ancestry_indices": 0, "zero_or_missing_diagonal": 0,
    "duplicate_empty_wrong_pivots": 0,
}
OLD_DUAL_SHA256 = "0960259714fa94ddd89e2ac4f582f040942ab7bd258185c0448c133e50b00f0c"
OLD_TARGET_SHA256 = "968f0b8325fa0e741e2c304bb940b96239c3e2d3226e0ca56f7d61a53dd0d82b"
KERNEL_ORDERS = [9, 9, 9, 9, 9, 1, 1, 1, 3, 3]
K0_INVERSE_MAX_BYTES = 256 * 1024 * 1024
DELTA_ORDER = 357_128_352


def checker_descriptors(runtime: dict[str, Any]) -> tuple[list[dict[str, Any]],
                                                           dict[tuple[int, int], list[int]]]:
    rows = []
    for block, count in ((1, 2), (2, 2), (3, 11)):
        quotient = group_for(runtime, block)
        for relator in range(1, count + 1):
            for (component, h), coefficient0 in runtime["boundary_group"][block][
                    relator - 1].items():
                coefficient = int(coefficient0) % 3
                if not coefficient:
                    continue
                h_raw = blob(runtime, h); h_inverse = quotient.inverse(h)
                rows.append({"block": block, "relator": relator,
                    "component": int(component), "h": h, "h_blob": h_raw,
                    "h_inverse": h_inverse,
                    "h_inverse_blob": blob(runtime, h_inverse),
                    "base_coefficient": coefficient})
    rows.sort(key=lambda row: (row["block"], row["relator"], row["component"],
                               row["h_blob"], row["base_coefficient"]))
    require(len(rows) == 104, "checker complete descriptor owner")
    lookup: dict[tuple[int, int], list[int]] = {}
    for index, row in enumerate(rows):
        lookup.setdefault((row["block"], row["component"]), []).append(index)
    return rows, lookup


def descriptor_public(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"block": row["block"], "relator": row["relator"],
             "component": row["component"], "h_hex": row["h_blob"].hex(),
             "h_inverse_hex": row["h_inverse_blob"].hex(),
             "base_coefficient": row["base_coefficient"]} for row in rows]


def dual_support(runtime: dict[str, Any], dual: Sparse) -> dict[str, Any]:
    private: dict[tuple[int, int], list[tuple[bytes, int, Any]]] = {}
    entries = []
    for key in sorted(dual):
        coefficient = int(dual[key]) % 3
        if key[:1] != b"R" or not coefficient:
            continue
        block, component, raw = decode_row_key(key)
        private.setdefault((block, component), []).append(
            (raw, coefficient, unpack(runtime, raw, block)))
        entries.append([block, component, raw.hex(), coefficient])
    return {"private": private, "entries": entries,
            "types": [[block, component] for block, component in sorted(private)],
            "entry_count": len(entries), "sha256": sha_obj(entries)}


def independent_boundary_outcome(runtime: dict[str, Any], dual: Sparse,
                                 workers: int, epoch: int) -> dict[str, Any]:
    require(workers in (2, 4), "checker worker count")
    descriptors, lookup = checker_descriptors(runtime)
    support = dual_support(runtime, dual)
    descriptor_ids = sorted(index for key in support["private"]
                            for index in lookup.get(key, ()))
    pairs = []
    for descriptor_id in descriptor_ids:
        descriptor = descriptors[descriptor_id]
        for g_raw, lambda_coefficient, g in support["private"].get(
                (descriptor["block"], descriptor["component"]), ()):
            quotient = group_for(runtime, descriptor["block"])
            translation = quotient.mul(g, descriptor["h_inverse"])
            require(quotient.mul(translation, descriptor["h"]) == g,
                    "checker boundary t*h=g")
            pairs.append((descriptor, blob(runtime, translation), lambda_coefficient))
    pair_stream = []
    for descriptor_id in descriptor_ids:
        descriptor = descriptors[descriptor_id]
        key = (descriptor["block"], descriptor["component"])
        entries = [[descriptor["block"], descriptor["component"],
                    g_raw.hex(), lambda_coefficient]
                   for g_raw, lambda_coefficient, _g in support["private"].get(key, ())]
        pair_stream.append((descriptor_id, entries))
    pair_offsets = [0]
    for _descriptor_id, entries in pair_stream:
        pair_offsets.append(pair_offsets[-1] + len(entries))
    require(pair_offsets[-1] == len(pairs), "checker pair stream cardinality")
    intervals = [[len(pairs) * index // workers,
                  len(pairs) * (index + 1) // workers]
                 for index in range(workers)]
    total: dict[tuple[int, bytes, int], int] = {}
    result_digests = []; worker_results = []; slice_digests = []
    for worker_id, (start, stop) in enumerate(intervals):
        slice_items = []
        for pair_index, (descriptor_id, entries) in enumerate(pair_stream):
            left = max(start, pair_offsets[pair_index])
            right = min(stop, pair_offsets[pair_index + 1])
            if left < right:
                base = pair_offsets[pair_index]
                slice_items.append([descriptor_id, entries[left - base:right - base]])
        require(sum(len(item[1]) for item in slice_items) == stop - start,
                "checker disjoint pair slice")
        slice_digest = sha_obj(slice_items)
        slice_digests.append(slice_digest)
        local: dict[tuple[int, bytes, int], int] = {}
        for descriptor, translation_raw, lambda_coefficient in pairs[start:stop]:
            key = (descriptor["block"], translation_raw, descriptor["relator"])
            value = (local.get(key, 0) + descriptor["base_coefficient"] *
                     lambda_coefficient) % 3
            if value:
                local[key] = value
            else:
                local.pop(key, None)
        for key, coefficient in local.items():
            value = (total.get(key, 0) + coefficient) % 3
            if value:
                total[key] = value
            else:
                total.pop(key, None)
        accumulator = [[block, raw.hex(), relator, local[(block, raw, relator)]]
                       for block, raw, relator in sorted(local)]
        result = {"kind": "RESULT", "epoch": epoch, "worker_id": worker_id,
                  "interval": [start, stop], "local_interval": [0, stop - start],
                  "slice_sha256": slice_digest, "attempted": stop - start,
                  "accumulator": accumulator, "complete": True}
        result["result_sha256"] = sha_obj(result)
        result_digests.append(result["result_sha256"])
        worker_results.append(result)
    selected = min(total) if total else None
    answer = {"epoch": epoch,
        "dual_sha256": sha_obj(public_sparse(dual)),
        "support_entry_count": support["entry_count"],
        "support_sha256": support["sha256"], "support_types": support["types"],
        "matching_descriptor_ids": descriptor_ids,
        "matching_descriptor_count": len(descriptor_ids),
        "expanded_pair_count": len(pairs), "intervals": intervals,
        "slice_digests": slice_digests,
        "slice_coverage": {"global_ordinal": [0, len(pairs)],
                            "disjoint": True, "overlap": False},
        "selected": None if selected is None else
            [selected[0], selected[1].hex(), selected[2]],
        "selected_scalar": None if selected is None else total[selected],
        "zero_complete": selected is None, "result_digests": result_digests,
        "worker_results": worker_results}
    if epoch == 1 and len(dual) == 1188:
        require(support["entry_count"] == 1188 and support["types"] == [[1, 1]] and
                len(descriptor_ids) == 4 and len(pairs) == 4752,
                "checker pinned first epoch")
        answer["pinned_first_epoch"] = True
    return answer


def validate_boundary_provenance(runtime: dict[str, Any], record: dict[str, Any],
                                 workers: int) -> Sparse:
    provenance = record.get("provenance")
    require(type(provenance) is dict and provenance.get("family") == "boundary" and
            provenance.get("left_translation_gate") == "t*h=g",
            "selected boundary provenance")
    block = int(provenance["block"]); relator = int(provenance["base_relator_index"])
    require(block in (1, 2, 3) and
            1 <= relator <= {1: 2, 2: 2, 3: 11}[block],
            "selected boundary indices")
    row = boundary_row(runtime, block, relator, provenance["translation_hex"])
    require(public_sparse(row) == record.get("sparse_row") and
            record.get("sparse_row_sha256") == sha_obj(record.get("sparse_row")),
            "selected boundary stored row")
    active_public = record.get("active_dual")
    if active_public is None:
        translation = unpack(runtime, bytes.fromhex(provenance["translation_hex"]), block)
        require(provenance.get("seed") == "identity_translation" and
                translation == group_for(runtime, block).identity and
                record.get("active_dual_sha256") is None and
                record.get("dual_pairing") is None,
                "selected seed boundary")
        return row
    dual = parse_sparse(active_public)
    require(record.get("active_dual_sha256") == sha_obj(active_public) and
            record.get("dual_pairing") == pair(dual, row) in (1, 2) and
            provenance.get("scalar") == record.get("dual_pairing") and
            provenance.get("complete_support_occurrence_accumulation") is True,
            "selected ACTIVE boundary")
    descriptors, _ = checker_descriptors(runtime)
    support = dual_support(runtime, dual)["private"]
    translation_raw = bytes.fromhex(provenance["translation_hex"])
    expected = []
    for descriptor in descriptors:
        if descriptor["block"] != block or descriptor["relator"] != relator:
            continue
        quotient = group_for(runtime, block)
        for g_raw, lambda_coefficient, g in support.get(
                (block, descriptor["component"]), ()):
            translation = quotient.mul(g, descriptor["h_inverse"])
            require(quotient.mul(translation, descriptor["h"]) == g,
                    "selected contributor orientation")
            if blob(runtime, translation) == translation_raw:
                expected.append({"component": descriptor["component"],
                    "g_hex": g_raw.hex(), "h_hex": descriptor["h_blob"].hex(),
                    "lambda_coefficient": lambda_coefficient,
                    "base_coefficient": descriptor["base_coefficient"]})
    order = lambda item: (item["component"], item["g_hex"], item["h_hex"],
                          item["lambda_coefficient"], item["base_coefficient"])
    claimed = provenance.get("contributing_pairs")
    require(type(claimed) is list and sorted(claimed, key=order) ==
            sorted(expected, key=order) and
            sum(item["lambda_coefficient"] * item["base_coefficient"]
                for item in expected) % 3 == record["dual_pairing"],
            "selected complete boundary contributors")
    epoch = provenance.get("boundary_epoch")
    if epoch is not None:
        expected_epoch = independent_boundary_outcome(runtime, dual, workers,
                                                       int(epoch["epoch"]))
        require(epoch == expected_epoch, "selected boundary epoch replay")
    return row


def weighted_support(formula: dict[str, Any]) -> dict[str, Any]:
    targets = sorted(formula["merged"], key=lambda item: (item[0], item[1]))
    rows = [{"coordinate": coordinate, "target_hex": target.hex(),
             "kernel_order": KERNEL_ORDERS[coordinate]}
            for coordinate, target in targets]
    return {"K": int(formula["constant"]),
            "W": sum(item["kernel_order"] for item in rows),
            "delta_order": DELTA_ORDER, "kernel_orders": KERNEL_ORDERS,
            "distinct_targets": rows}


def reconstruct_k0_selected_fibre(runtime: dict[str, Any], section: dict[str, Any],
                                  target: bytes, qword: list[int],
                                  gword: list[int]) -> None:
    """Independent single-coordinate fibre replay for one selected K=0 target."""
    coordinate = int(section.get("coordinate"))
    require(0 <= coordinate < 10 and type(target) is bytes and
            len(target) == (40 if coordinate < 5 else 154),
            "K0 selected typed target")
    count = 1469664
    width = 40 if coordinate < 5 else 154
    degree = 36 if coordinate < 5 else 144
    require(count * width <= K0_INVERSE_MAX_BYTES,
            "K0 inverse preallocation cap")
    owners = runtime["task176_owners"]
    marks = owners["marked_generators"][coordinate]
    require(len(marks) == 2 and all(len(mark) == width for mark in marks),
            "K0 selected coordinate marks")
    group = runtime["e3"] if coordinate < 5 else runtime["e4"]
    identity = replay_typed_ten_state(runtime, [])
    offset = 40 * min(coordinate, 5) + 154 * max(0, coordinate - 5)
    states = bytearray(count * width)
    states[:width] = identity[offset:offset + width]
    inverse: dict[bytes, int] = {}
    for qid in range(1, count + 1):
        parent = struct.unpack_from("<I", owners["q0_parents"], (qid - 1) * 4)[0]
        letter = owners["q0_letters"][qid - 1]
        require((parent == 0 and letter == 0) or
                (parent != 0 and letter in (1, 2)),
                "K0 Q0 chronological edge")
        if parent == 0:
            state = identity[offset:offset + width]
        else:
            parent_state = bytes(states[(parent - 1) * width:parent * width])
            state = checker_packed_joint_blob(
                group.mul(checker_value_from_blob(parent_state,
                    1 if coordinate < 5 else 3),
                    checker_value_from_blob(marks[letter - 1],
                        1 if coordinate < 5 else 3)),
                "K0 one-coordinate recurrence")
        states[(qid - 1) * width:qid * width] = state
        key = state[:degree]
        require(key not in inverse, "K0 duplicate coarse key")
        inverse[key] = qid
    require(len(inverse) == count, "K0 singleton Q0 coarse inverse")
    coarse_digest = hashlib.sha256()
    for qid, key in sorted(((qid, key) for key, qid in inverse.items())):
        coarse_digest.update(canonical([key.hex(), qid]))
    require(section.get("coarse_inverse_pairs_sha256") == coarse_digest.hexdigest(),
            "K0 coarse inverse digest")
    first_gamma: dict[bytes, int] = {}
    for gid in range(1, 244):
        word = task176_gamma_walk(owners["gamma_parents"], owners["gamma_records"],
                                  owners["gamma_words"], gid)
        value = replay_typed_ten_state(runtime, word)
        width = 40 if coordinate < 5 else 154
        offset = 0 if coordinate == 0 else (40 * min(coordinate, 5) +
            154 * max(0, coordinate - 5))
        first_gamma.setdefault(value[offset:offset + width], gid)
    require(first_gamma, "K0 Gamma value map")
    family = runtime["task176_receipt"]["result"]["A_families"][f"S{coordinate}"]
    literal = family.get("literal_elements")
    require(type(literal) is list and all(type(item) is dict for item in literal),
            "K0 authenticated A-family literal owner")
    literal_keys = {bytes.fromhex(str(item["coordinate_blobs_hex"][0]))
                    for item in literal}
    require(literal_keys == set(first_gamma), "K0 Gamma/A-family literal equality")
    target_value = checker_value_from_blob(target, 1 if coordinate < 5 else 3)
    candidates: list[tuple[int, int]] = []
    for gamma_key, gid in sorted(first_gamma.items()):
        gamma_value = checker_value_from_blob(gamma_key, 1 if coordinate < 5 else 3)
        source = checker_packed_joint_blob(
            group.mul(group.inverse(gamma_value), target_value),
            "K0 inverse source")
        qid = inverse.get(source[:degree])
        require(qid is not None, "K0 full typed blob inverse")
        require(checker_packed_joint_blob(group.mul(gamma_value,
            checker_value_from_blob(source, 1 if coordinate < 5 else 3)),
            "K0 target product") == target, "K0 target product equality")
        candidates.append((qid, gid))
    least = min(candidates)
    require((int(section.get("q0_state_id")), int(section.get("gamma_state_id"))) == least,
            "K0 lexicographically least base")
    require(section.get("coarse_inverse_entries") == count and
            section.get("gamma_distinct_values") == len(first_gamma) and
            section.get("gamma_distinct_values_sha256") ==
                sha_obj(sorted(key.hex() for key in first_gamma)),
            "K0 inverse provenance metadata")
    auth_generators = runtime["task176_receipt"]["result"]["word_generators"][f"S{coordinate}"]
    require(type(auth_generators) is dict, "K0 authenticated word-generator owner")
    generators: list[list[int]] = []
    for family_name in ("Gamma_S0_generators", "adjusted_L_generators"):
        for item in auth_generators.get(family_name, []):
            raw_word = item.get("source_word")
            require(type(raw_word) in (str, list), "K0 word-generator encoding")
            word = ([int(value) for value in raw_word.split()] if type(raw_word) is str
                    else [int(value) for value in raw_word])
            generators.extend((word, inverse_word(word)))
    require(generators and section.get("kernel_generators") == generators and
            section.get("kernel_generators_sha256") == sha_obj(generators),
            "K0 authenticated kernel generator binding")
    identity = replay_typed_ten_state(runtime, [])
    states: list[tuple[list[int], bytes]] = [([], identity)]
    seen_states = {identity}
    head = 0
    while head < len(states):
        prior_word, _prior_blobs = states[head]; head += 1
        for generator in generators:
            word = reduce_word(prior_word + generator)
            blobs = replay_typed_ten_state(runtime, word)
            require(blobs[sum([40] * min(coordinate, 5)) +
                sum([154] * max(0, coordinate - 5)):][:
                40 if coordinate < 5 else 154] ==
                identity[sum([40] * min(coordinate, 5)) +
                sum([154] * max(0, coordinate - 5)):][:
                40 if coordinate < 5 else 154], "K0 kernel singleton identity")
            if blobs in seen_states: continue
            seen_states.add(blobs); states.append((word, blobs))
    require(section.get("kernel_order") == KERNEL_ORDERS[coordinate] and
            len(states) == int(section["kernel_order"]) and
            section.get("kernel_cursor") in range(len(states)),
            "K0 exact kernel BFS order")
    cursor = int(section["kernel_cursor"])
    require(section.get("kernel_state_word") == states[cursor][0] and
            section.get("kernel_word") == states[cursor][0],
            "K0 exact kernel cursor state")


def validate_correction_provenance(runtime: dict[str, Any],
                                   record: dict[str, Any]) -> Sparse:
    provenance = record.get("provenance")
    require(type(provenance) is dict and provenance.get("family") == "correction",
            "selected correction provenance")
    roster_index = int(provenance["roster_index"])
    require(1 <= roster_index <= len(runtime["roster"]), "correction roster index")
    roster = runtime["roster"][roster_index - 1]
    require(provenance.get("relator_word") == roster["word"] and
            provenance.get("layer") == roster["layer"] and
            int(provenance.get("ordinal")) == int(roster["ordinal"]),
            "correction literal roster")
    row, replay = runtime["model"].direct_column(provenance["delta_word"],
                                                  provenance["relator_word"])
    for key in ("delta_word", "relator_word", "conjugate_word", "corrected_word",
                "quotient_value_blobs", "eleven_occurrence_replay",
                "direct_all_seven_replay"):
        require(provenance.get(key) == replay.get(key),
                "correction replay field:" + key)
    require(public_sparse(row) == record.get("sparse_row") and
            record.get("sparse_row_sha256") == sha_obj(record.get("sparse_row")),
            "selected correction stored row")
    dual_public = record.get("active_dual")
    require(type(dual_public) is list and
            record.get("active_dual_sha256") == sha_obj(dual_public),
            "correction ACTIVE dual")
    dual = parse_sparse(dual_public)
    require(record.get("dual_pairing") == pair(dual, row) in (1, 2),
            "correction ACTIVE scalar")
    formula = runtime["model"].occurrence_data(provenance["relator_word"], dual)
    require(provenance.get("weighted_formula") == formula["public"] and
            provenance.get("support_hitting") == weighted_support(formula),
            "correction independent weighted formula")
    coordinates = runtime["model"].coordinates(provenance["delta_word"])
    require(provenance.get("delta_coordinate_blobs_hex") ==
            [raw.hex() for raw in coordinates], "correction ten coordinates")
    scalar = int(formula["constant"])
    for (coordinate, target), coefficient in formula["merged"].items():
        if coordinates[coordinate] == target:
            scalar += coefficient
    require(scalar % 3 == record["dual_pairing"], "correction formula scalar")
    support = weighted_support(formula); schedule = provenance.get("schedule")
    section = provenance.get("section_provenance")
    require(type(section) is dict, "correction section provenance")
    require(section.get("membership_bound") is True and
            section.get("schedule_relation") == "qid/gid/current-dual/fibre-bound" and
            type(section.get("q0_state_hex")) is str and
            type(section.get("gamma_full_state_hex")) is str and
            section.get("q0_state_sha256") == sha_bytes(
                bytes.fromhex(section["q0_state_hex"])) and
            section.get("gamma_full_state_sha256") == sha_bytes(
                bytes.fromhex(section["gamma_full_state_hex"])),
            "correction reconstructed Q0/Gamma identity")
    reconstruct_task176_selected(runtime, section)
    owners = runtime["task176_owners"]
    qword = task176_parent_walk(owners["q0_parents"], owners["q0_letters"],
                                int(section["q0_state_id"]), 1469664)
    gword = task176_gamma_walk(owners["gamma_parents"], owners["gamma_records"],
                               owners["gamma_words"], int(section["gamma_state_id"]))
    base_word = reduce_word(gword + qword)
    require(section.get("selected_q0_word") == qword and
            section.get("selected_gamma_word") == gword and
            section.get("selected_base_word") == base_word,
            "selected Q0/Gamma/base word binding")
    if support["K"] == 0:
        kernel_word = section.get("kernel_word")
        require(type(kernel_word) is list and
                provenance.get("delta_word") ==
                reduce_word(kernel_word + gword + qword),
                "K0 kernel+Gamma+Q0 product order")
        target_hex = section.get("target_hex")
        require(type(target_hex) is str, "K0 target owner")
        reconstruct_k0_selected_fibre(runtime, section, bytes.fromhex(target_hex),
                                      qword, gword)
        require(schedule == "weighted_support_fibre_complete" and
                any(item["coordinate"] == int(section.get("coordinate")) and
                    item["target_hex"] == section.get("target_hex")
                    for item in support["distinct_targets"]) and
                coordinates[int(section["coordinate"])].hex() == section["target_hex"] and
                0 <= int(section.get("kernel_cursor")) <
                    KERNEL_ORDERS[int(section["coordinate"])] and
                0 <= int(section.get("support_fibre_cursor")) <
                    len(support["distinct_targets"]) and
                support["distinct_targets"][int(section["support_fibre_cursor"])] == {
                    "coordinate": int(section["coordinate"]),
                    "target_hex": section["target_hex"],
                    "kernel_order": KERNEL_ORDERS[int(section["coordinate"])]} and
                1 <= int(section.get("q0_state_id")) <= 1_469_664 and
                1 <= int(section.get("gamma_state_id")) <= 243,
                "correction K0 support fibre")
    else:
        require(provenance.get("delta_word") == base_word,
                "K-nonzero Gamma+Q0 product order")
        bound = support["W"] + 1 if support["W"] < DELTA_ORDER else DELTA_ORDER
        cursor = int(section.get("global_cursor"))
        require(0 <= cursor < bound and
                ((schedule == "weighted_global_prefix_W_plus_1" and
                  support["W"] < DELTA_ORDER) or
                 (schedule == "weighted_global_fair_fallback" and
                  support["W"] >= DELTA_ORDER)) and
                int(section.get("q0_state_id")) == cursor // 243 + 1 and
                int(section.get("gamma_state_id")) == cursor % 243 + 1,
                "correction global W+1 gate")
    return row


def validate_triangular_certificate(value: Any) -> None:
    require(type(value) is dict and
            {key: value.get(key) for key in EXPECTED_TRIANGULAR} ==
            EXPECTED_TRIANGULAR and
            value.get("P_rows_sha256") == OLD_PIVOT_ROWS_SHA256 and
            value.get("P_equations_independent") is True and
            value.get("historical_Echelon_add_called") is False and
            value.get("heuristic_discovery_only") is True and
            value.get("exact_cached_resume") is False and
            value.get("formal_entries") == 137926 and
            value.get("fresh_dual_support") == 1188 and
            value.get("fresh_dual_sha256") == OLD_DUAL_SHA256 and
            type(value.get("target_remainder_support")) is int and
            value["target_remainder_support"] > 0,
            "triangular discovery certificate")


def validate_boundary_owner(runtime: dict[str, Any], value: Any) -> int:
    require(type(value) is dict and value.get("workers") in (2, 4) and
            value.get("persistent") is True and
            value.get("transport") ==
                "nonblocking AF_UNIX socketpair, absolute deadline frames",
            "boundary owner envelope")
    workers = int(value["workers"]); accounting = value.get("accounting")
    cleanup = value.get("cleanup")
    descriptors, _ = checker_descriptors(runtime)
    require(type(accounting) is dict and
            accounting.get("descriptor_count") == 104 and
            accounting.get("descriptor_sha256") == sha_obj(descriptor_public(descriptors)) and
            accounting.get("metric") ==
                "sampled RSS sum; not exact physical peak" and
            all(type(accounting.get(key)) is int and accounting[key] >= 0
                for key in ("epochs_committed", "epochs_discarded",
                    "literal_pairs_committed", "support_bytes",
                    "frames_sent_bytes", "frames_received_bytes",
                    "accumulator_entries", "max_accumulator_entries",
                    "formal_ancestry_entries",
                    "winner_reconstructions", "process_restarts")),
            "boundary accounting")
    require(accounting["formal_ancestry_entries"] >= 137926,
            "boundary formal ancestry accounting")
    require(type(cleanup) is dict and cleanup.get("complete") is True and
            cleanup.get("live_pids_after_join") == [] and
            cleanup.get("process_close_count") == workers and
            len(cleanup.get("started_pids", [])) == workers and
            len(cleanup.get("worker_exitcodes", [])) == workers and
            "closed" in cleanup.get("transitions", []),
            "boundary bounded cleanup")
    return workers


def load_fixture_bounded() -> dict[str, Any]:
    raw, _physical = read_owner_bytes(ROOT / SOURCE_PINS["fixture"][0],
                                      SOURCE_PINS["fixture"][1],
                                      SOURCE_PINS["fixture"][2])
    return json.loads(raw.decode("ascii"))


def validate_selftest(runtime: dict[str, Any], receipt: dict[str, Any]) -> None:
    fixture = load_fixture_bounded()
    value = receipt.get("selftest")
    require(type(value) is dict and
            value.get("fixture_sha256") == SOURCE_PINS["fixture"][2] and
            value.get("real_owner_not_shaped_transcript") is True and
            value.get("boundary_mutations_committed_to_checker") ==
                fixture["boundary_mutations"] and
            value.get("positive_mutations_committed_to_checker") ==
                fixture["positive_mutations"] and
            value.get("physical_mutations_committed_to_checker") ==
                fixture["physical_mutations"], "selftest fixture binding")
    triangular = value.get("triangular_mutations")
    require([row.get("id") for row in triangular] == fixture["triangular_mutations"] and
            all(row.get("physical_before_validator") is True and
                row.get("narrow_rejection") is True for row in triangular),
            "triangular physical mutation ledger")
    processes = value.get("process_owner")
    require(type(processes) is dict and processes.get("actual_E3_E4_codec") is True and
            processes.get("actual_process_owner") is True and
            processes.get("W2_W4") is True and
            processes.get("blocked_send", {}).get("deadline_rejected") is True and
            processes["blocked_send"].get("cleanup_complete") is True and
            processes["blocked_send"].get("process_close") is True,
            "process owner selftest")
    dual = parse_sparse(processes.get("first_dual"))
    require(len(dual) == 1188 and processes.get("first_dual_sha256") ==
            sha_obj(public_sparse(dual)) == OLD_DUAL_SHA256,
            "selftest actual first dual")
    row_keys = [key for key in sorted(dual) if key[:1] == b"R"]
    require(len(row_keys) == 1188, "selftest typed row support")
    normal_workers = set(); faults: dict[int, set[str]] = {2: set(), 4: set()}
    for run in processes.get("runs", []):
        workers = int(run.get("workers"))
        require(workers in (2, 4), "selftest run workers")
        if "fault" in run:
            require(run.get("fault") in ("timeout", "death", "partial") and
                    run.get("atomic_discard") is True and
                    run.get("cleanup", {}).get("complete") is True and
                    run["cleanup"].get("live_pids_after_join") == [] and
                    run["cleanup"].get("process_close_count") == workers,
                    "selftest fault atomic cleanup")
            faults[workers].add(run["fault"]); continue
        require(workers not in normal_workers, "duplicate normal process run")
        normal_workers.add(workers)
        descriptors, _lookup = checker_descriptors(runtime)
        first_descriptor = descriptors[0]
        second_descriptor = next(row for row in descriptors[1:]
            if row["block"] == first_descriptor["block"] and
               row["relator"] == first_descriptor["relator"] and
               (row["component"], row["h_blob"]) !=
               (first_descriptor["component"], first_descriptor["h_blob"]))
        cancellation_second = (-first_descriptor["base_coefficient"] *
            (1 if second_descriptor["base_coefficient"] == 1 else 2)) % 3
        cancellation_probe = {
            row_key(first_descriptor["block"], first_descriptor["component"],
                    first_descriptor["h_blob"]): 1,
            row_key(second_descriptor["block"], second_descriptor["component"],
                    second_descriptor["h_blob"]): cancellation_second}
        probes = [({}, "empty_support"),
                  ({row_keys[0]: dual[row_keys[0]]}, "one_support"),
                  ({key: dual[key] for key in row_keys[:4]}, "short_support"),
                  ({**{key: dual[key] for key in row_keys[:2]},
                    exponent_key(1): 1}, "typed_present_shape_filter"),
                  (cancellation_probe, "f3_cancellation")]
        claimed = run.get("probes")
        require(type(claimed) is list and len(claimed) == len(probes),
                "selftest probe roster")
        for ordinal, ((probe, label), row) in enumerate(zip(probes, claimed), 1):
            expected = independent_boundary_outcome(runtime, probe, workers, ordinal)
            require(row.get("case") == label and row.get("outcome") == expected and
                    row.get("support") == expected["support_entry_count"] and
                    row.get("pairs") == expected["expanded_pair_count"] and
                    row.get("active") is (expected["selected"] is not None) and
                    row.get("zero") is (expected["selected"] is None),
                    "selftest actual process probe")
        serial = [dual, scaled(dual, 2),
                  {key: dual[key] for key in row_keys[:2]}]
        outcomes = run.get("three_serial_outcomes")
        require(type(outcomes) is list and len(outcomes) == 3,
                "selftest serial outcome roster")
        expected_outcomes = [independent_boundary_outcome(runtime, probe, workers,
                                                           index + 6)
                             for index, probe in enumerate(serial)]
        require(outcomes == expected_outcomes and
                run.get("three_serial_duals") ==
                    [row["dual_sha256"] for row in expected_outcomes] and
                run.get("cleanup", {}).get("complete") is True and
                run["cleanup"].get("live_pids_after_join") == [] and
                run["cleanup"].get("process_close_count") == workers,
                "selftest three serial epochs")
    require(normal_workers == {2, 4} and
            faults == {2: {"timeout", "death", "partial"},
                       4: {"timeout", "death", "partial"}},
            "selftest complete W2/W4 process matrix")
    phases = value.get("phase_mutations")
    require([row.get("id") for row in phases] == fixture["phase_mutations"] and
            all(row.get("owner_gate") is True or
                (row.get("owner_mutated_before_validator") is True and
                 row.get("narrow_rejection") is True) for row in phases),
            "selftest phase gates")


def validate_common(runtime: dict[str, Any], receipt: dict[str, Any],
                    *, include_selftest: bool = True,
                    source_raw: bytes | None = None) -> dict[str, Any]:
    validate_seal(receipt)
    require(receipt.get("schema") == SCHEMA and
            receipt.get("status") == "COMMON_WORD" and
            receipt.get("terminal") == COMMON and
            receipt.get("claims") == POSITIVE_CLAIMS and
            "checkpoint" not in receipt and receipt.get("common_word") is None and
            receipt.get("claim_boundary") ==
                "finite A0 candidate; checker required; no lift/fake/Ihara",
            "COMMON envelope")
    require(receipt.get("source_snapshots") == Sources.public() and
            receipt.get("light_input_sha256") == runtime["light_input_sha256"] and
            receipt.get("basis_authority") == {
                "heuristic_discovery_only": True, "exact_cached_resume": False},
            "COMMON source/light authority")
    validate_triangular_certificate(receipt.get("triangular_certificate"))
    target = runtime["target"]
    require(parse_sparse(receipt.get("target")) == target and
            sha_obj(receipt["target"]) == OLD_TARGET_SHA256 and
            receipt.get("g760") == runtime["g760"], "COMMON target/g760")
    workers = validate_boundary_owner(runtime, receipt.get("boundary_owner"))
    solution_rows = receipt.get("formal_solution")
    require(type(solution_rows) is list and solution_rows and
            all(type(row) is list and len(row) == 2 and type(row[0]) is str and
                row[1] in (1, 2) for row in solution_rows) and
            solution_rows == sorted(solution_rows) and
            len({row[0] for row in solution_rows}) == len(solution_rows),
            "COMMON canonical formal solution")
    solution = {str(symbol): int(coefficient)
                for symbol, coefficient in solution_rows}
    selected = list(receipt.get("selected_old", [])) + list(
        receipt.get("selected_new", []))
    require(len(selected) == len(solution) and
            {row.get("symbol") for row in selected} == set(solution),
            "COMMON selected support complete")
    old_source_value = None
    if receipt.get("selected_old"):
        require(source_raw is not None, "COMMON raw source binding")
        old_source_value = json.loads(source_raw.decode("utf-8"))
        require(type(old_source_value) is dict and
                len(old_source_value.get("columns", [])) == 2896,
                "COMMON authenticated old source roster")
    combined: Sparse = {}; correction_sum: Sparse = {}; boundary_sum: Sparse = {}
    boundary_expected = []; correction_expected = []; correction_word: list[int] = []
    for selected_row in sorted(selected, key=lambda row: row["symbol"]):
        symbol = selected_row.get("symbol"); coefficient = selected_row.get("coefficient")
        record = selected_row.get("record")
        require(coefficient == solution[symbol] and type(record) is dict,
                "COMMON selected coefficient")
        if symbol.startswith("o:"):
            require(selected_row in receipt["selected_old"] and
                    record.get("column_id") == int(symbol[2:]) and
                    record.get("family") == "boundary",
                    "COMMON old symbol binding")
            source_record = old_source_value["columns"][int(symbol[2:]) - 1]
            require(record == source_record and
                    record.get("sparse_row_sha256") == sha_obj(record.get("sparse_row")),
                    "COMMON old symbol literal source binding")
        else:
            require(symbol.startswith("n:") and selected_row in receipt["selected_new"] and
                    record.get("symbol") == symbol and
                    record.get("actual_direct_replay") is True and
                    record.get("rank_after") == record.get("rank_before") + 1,
                    "COMMON new symbol binding")
        if record.get("family") == "boundary":
            row = validate_boundary_provenance(runtime, record, workers)
            add_scaled(boundary_sum, row, coefficient)
            boundary_expected.append({"symbol": symbol, "coefficient": coefficient,
                                      "provenance": record["provenance"]})
        elif record.get("family") == "correction":
            require(symbol.startswith("n:"), "old correction forbidden")
            row = validate_correction_provenance(runtime, record)
            add_scaled(correction_sum, row, coefficient)
            conjugate = list(record["provenance"]["conjugate_word"])
            factor = conjugate if coefficient == 1 else inverse_word(conjugate)
            inverse_replayed = False
            if coefficient == 2:
                inverse_row, inverse_public = runtime["model"].direct_column(
                    record["provenance"]["delta_word"],
                    inverse_word(record["provenance"]["relator_word"]))
                require(inverse_row == scaled(row, -1) and
                        inverse_public["conjugate_word"] == factor,
                        "COMMON coefficient two inverse replay")
                inverse_replayed = True
            require(runtime["joint_group"].eval(factor) ==
                    runtime["joint_group"].identity,
                    "COMMON selected joint-kernel factor")
            correction_word = reduce_word(correction_word + factor)
            correction_expected.append({"symbol": symbol, "coefficient": coefficient,
                "factor_word": factor,
                "coefficient_two_inverse_replayed": inverse_replayed,
                "provenance": record["provenance"]})
        else:
            raise CheckStop("COMMON selected family")
        add_scaled(combined, row, coefficient)
    require(combined == target, "COMMON complete selected sparse target")
    require(receipt.get("boundary_preimage") == boundary_expected and
            receipt.get("selected_corrections") == correction_expected,
            "COMMON typed preimage/support")
    require(receipt.get("correction_word") == correction_word and
            exponent_pair(correction_word) == (0, 0),
            "COMMON literal correction product")
    direct, replay = runtime["model"].direct_column([], correction_word)
    require(direct == correction_sum and
            receipt.get("producer_all_seven_replay") == replay and
            receipt.get("corrected_word") == replay["corrected_word"] ==
                reduce_word(runtime["g760"] + correction_word),
            "COMMON correction all-seven additivity")
    residual = scaled(target, -1); add_scaled(residual, correction_sum, 1)
    add_scaled(residual, boundary_sum, 1)
    require(not residual and receipt.get("producer_sparse_equality") is True and
            receipt.get("producer_joint_kernel") is True,
            "COMMON independently derived PB3/PB4 residual")
    if correction_expected:
        require(type(receipt.get("heavy_input_sha256")) is str and
                len(receipt["heavy_input_sha256"]) == 64,
                "COMMON correction requires heavy owner")
    else:
        require(receipt.get("heavy_input_sha256") is None or
                (type(receipt["heavy_input_sha256"]) is str and
                 len(receipt["heavy_input_sha256"]) == 64),
                "COMMON heavy digest shape")
    if include_selftest:
        validate_selftest(runtime, receipt)
    return {"terminal": COMMON, "selected_rows": len(selected),
            "selected_old": len(receipt["selected_old"]),
            "selected_new": len(receipt["selected_new"]),
            "selected_corrections": len(correction_expected),
            "boundary_preimage_terms": len(boundary_expected),
            "helper_nonshared": True, "target_sha256": sha_obj(public_sparse(target)),
            "all_eleven_and_direct_all_seven": True}


def hash_physical(path: Path, expected_size: int, expected_sha256: str,
                  expected_identity: dict[str, Any] | None = None) -> dict[str, Any]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise CheckStop("source physical open") from exc
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                before.st_size == expected_size, "source physical unique regular")
        digest = hashlib.sha256(); remaining = expected_size
        while remaining:
            raw = os.read(fd, min(1 << 20, remaining))
            require(bool(raw), "source physical short read")
            digest.update(raw); remaining -= len(raw)
        require(not os.read(fd, 1), "source physical long read")
        after = os.fstat(fd)
        require((before.st_dev, before.st_ino, before.st_size, before.st_nlink,
                 before.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
                 after.st_mtime_ns) and digest.hexdigest() == expected_sha256,
                "source physical immutable digest")
        path_after = os.lstat(path)
        require(not stat.S_ISLNK(path_after.st_mode) and
                (path_after.st_dev, path_after.st_ino, path_after.st_size,
                 path_after.st_nlink, path_after.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size,
                 after.st_nlink, after.st_mtime_ns),
                "source physical pathname identity")
        if expected_identity is not None:
            require(expected_identity == {"device": before.st_dev,
                "inode": before.st_ino, "size": before.st_size,
                "links": before.st_nlink, "mtime_ns": before.st_mtime_ns,
                "sha256": expected_sha256}, "source physical receipt binding")
        return {"device": before.st_dev, "inode": before.st_ino,
                "bytes": before.st_size, "sha256": expected_sha256}
    finally:
        os.close(fd)


def validate_source_transport(receipt: dict[str, Any], *, hash_source: bool = True) -> dict[str, Any] | None:
    source = receipt.get("source")
    if source is None:
        return None
    require(type(source) is dict and source.get("member") ==
            "d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json" and
            source.get("bytes") == RAW_BYTES and source.get("sha256") == RAW_SHA256 and
            source.get("parsed_once") is True and type(source.get("path")) is str,
            "source receipt transport")
    path = Path(source["path"])
    if not path.is_absolute():
        path = ROOT / path
    try:
        path.resolve().relative_to(ROOT.resolve())
    except (OSError, ValueError) as exc:
        raise CheckStop("source outside workspace") from exc
    if hash_source:
        hash_physical(path, RAW_BYTES, RAW_SHA256, source.get("physical"))
    else:
        require(path.is_file() and not path.is_symlink(), "source path envelope")
    return source


def read_bound_source(receipt: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    """Open the producer's raw owner once and retain that immutable byte object."""
    source = receipt["source"]
    path = Path(source["path"])
    if not path.is_absolute(): path = ROOT / path
    value, raw, identity = open_physical(path, RAW_BYTES,
        {"bytes": RAW_BYTES, "sha256": RAW_SHA256})
    require(source.get("physical") is None or
            (source["physical"].get("device") == identity["device"] and
             source["physical"].get("inode") == identity["inode"] and
             source["physical"].get("mtime_ns") == identity["mtime_ns"]),
            "source owner identity")
    return value, raw


def validate_monitor(value: Any) -> None:
    require(type(value) is dict and value.get("limits", {}).get("wall_seconds") == 10800.0,
            "monitor wall boundary")
    limits = value["limits"]; counters = value.get("fresh_v10_counters")
    required = ("wall_seconds", "boundary_pairs", "fibre_scans",
                "candidate_words", "retained_columns", "checkpoint_bytes",
                "rss_bytes", "oracle_rounds", "global_roster",
                "pivot_support_inspections", "dag_node_allocations",
                "sparse_operations", "expansion_calls", "expansion_support",
                "serialized_dag_bytes")
    require(all(key in limits for key in required) and type(counters) is dict and
            all(type(item) in (int, float) and item >= 0 for item in counters.values()) and
            set(counters) == set(required) - {"wall_seconds", "rss_bytes"} and
            type(value.get("phase")) is str and
            type(value.get("elapsed_seconds")) in (int, float) and
            value["elapsed_seconds"] >= 0 and
            value.get("resource_metric") ==
                "sampled parent RSS plus sampled child RSS sum" and
            type(value.get("sampled_parent_rss_peak_bytes")) is int and
            type(value.get("sampled_children_rss_peak_sum_bytes")) is int,
            "monitor counters/authority")


def validate_checkpoint_transport(receipt: dict[str, Any], receipt_path: Path) -> dict[str, Any]:
    reference = receipt.get("checkpoint")
    require(type(reference) is dict and reference.get("terminal_checkpoint") is True and
            type(reference.get("path")) is str and
            Path(reference["path"]).name == reference["path"] and
            reference["path"] == receipt_path.name + ".checkpoint.json" and
            0 < int(reference.get("bytes")) <= MAX_CHECKPOINT_BYTES and
            type(reference.get("sha256")) is str,
            "resource checkpoint reference")
    checkpoint_path = receipt_path.parent / reference["path"]
    checkpoint, _raw, physical = open_physical(checkpoint_path, MAX_CHECKPOINT_BYTES,
        {"bytes": int(reference["bytes"]), "sha256": reference["sha256"]})
    validate_seal(checkpoint)
    require(checkpoint.get("schema") == CHECKPOINT_SCHEMA and
            checkpoint.get("phase") == "resource_stop" and
            checkpoint.get("source") == receipt.get("source") and
            checkpoint.get("source_snapshots") == Sources.public() and
            checkpoint.get("light_input_sha256") == receipt.get("light_input_sha256") and
            checkpoint.get("claims") == FALSE_CLAIMS and
            checkpoint.get("heuristic_discovery_only") is True and
            checkpoint.get("exact_cached_resume") is False,
            "resource checkpoint envelope")
    validate_triangular_certificate(checkpoint.get("triangular_certificate"))
    p_rows = checkpoint.get("P_rows")
    require(type(p_rows) is list and len(p_rows) == 2896 and
            all(type(row) is list and public_sparse(parse_sparse(row)) == row
                for row in p_rows) and
            checkpoint.get("P_rows_sha256") == sha_obj(p_rows) ==
                OLD_PIVOT_ROWS_SHA256,
            "resource canonical P owner")
    formal = checkpoint.get("formal_ancestry")
    new_records = checkpoint.get("new_records")
    require(type(formal) is dict and
            formal.get("owner") ==
                "hash-consed structural DAG over old/new formal symbols" and
            formal.get("dag_owner") == "hash-consed immutable structural DAG node ids" and
            type(formal.get("dag_nodes")) is list and type(formal.get("pivot_expr_ids")) is list and
            formal.get("old_symbol_count") == 2896 and
            type(new_records) is list and
            type(formal.get("entry_count")) is int and
            137926 <= formal["entry_count"] <= formal.get("max_entries") == 2_000_000 and
            checkpoint.get("formal_ancestry_sha256") == sha_obj(formal),
            "resource formal ancestry owner")
    validate_dag_nodes(formal["dag_nodes"])
    for index, record in enumerate(new_records, 1):
        require(record.get("symbol") == f"n:{index:04d}" and
                record.get("family") in ("boundary", "correction") and
                public_sparse(parse_sparse(record.get("sparse_row"))) ==
                    record.get("sparse_row") and
                record.get("sparse_row_sha256") == sha_obj(record["sparse_row"]) and
                type(record.get("active_dual")) is list and
                public_sparse(parse_sparse(record["active_dual"])) ==
                    record["active_dual"] and
                record.get("active_dual_sha256") == sha_obj(
                    record.get("active_dual")) and
                type(record.get("pivot_node_id")) is int and
                record.get("pivot_node_id") >= 1,
                "resource live new record transport")
    target = parse_sparse(checkpoint.get("target")); remainder = parse_sparse(
        checkpoint.get("remainder"))
    require(sha_obj(public_sparse(target)) == OLD_TARGET_SHA256 and
            type(remainder) is dict and
            type(checkpoint.get("solution_node_id")) is int and
            checkpoint.get("solution_node_id") >= 0 and
            checkpoint.get("target_node_id") == checkpoint.get("solution_node_id") and
            checkpoint.get("coefficient_solution_node_ids") ==
                [checkpoint.get("solution_node_id")] and
            checkpoint.get("current_dual_sha256") ==
                (None if checkpoint.get("current_dual") is None else
                 sha_obj(checkpoint["current_dual"])),
            "resource target/remainder/dual")
    if checkpoint.get("current_dual") is not None:
        parse_sparse(checkpoint["current_dual"])
    progress = checkpoint.get("correction_progress")
    require(type(progress) is dict and
            set(progress) == {"dual_sha256", "canonical_row_cursor", "weighted_rows"} and
            type(progress["canonical_row_cursor"]) is int and
            progress["canonical_row_cursor"] >= 0 and
            type(progress["weighted_rows"]) is dict and
            type(checkpoint.get("next_clean_boundary_epoch")) is int and
            checkpoint["next_clean_boundary_epoch"] >= 1,
            "resource correction/epoch state")
    heavy_complete = checkpoint.get("heavy_complete")
    require(type(heavy_complete) is bool and
            ((not heavy_complete and checkpoint.get("heavy_reconstructible") is bool) or
             (heavy_complete and type(checkpoint.get("heavy_input_sha256")) is str and
              len(checkpoint["heavy_input_sha256"]) == 64)),
            "resource Q0-LATE phase boundary")
    validate_monitor(checkpoint.get("monitor"))
    boundary = checkpoint.get("boundary_owner")
    accounting = boundary.get("accounting", {}) if type(boundary) is dict else {}
    require(type(boundary) is dict and boundary.get("workers") in (2, 4) and
            boundary.get("persistent") is True and
            accounting.get("descriptor_count") == 104 and
            type(accounting.get("descriptor_sha256")) is str and
            len(accounting["descriptor_sha256"]) == 64 and
            all(type(accounting.get(key)) is int and accounting[key] >= 0
                for key in ("epochs_committed", "epochs_discarded",
                    "literal_pairs_committed", "frames_sent_bytes",
                    "frames_received_bytes", "accumulator_entries",
                    "formal_ancestry_entries", "winner_reconstructions",
                    "process_restarts")) and
            boundary.get("cleanup", {}).get("complete") is True and
            boundary["cleanup"].get("live_pids_after_join") == [] and
            ((boundary["cleanup"].get("started_pids") == [] and
              boundary["cleanup"].get("worker_exitcodes") == [] and
              boundary["cleanup"].get("process_close_count") == 0) or
             (len(boundary["cleanup"].get("started_pids", [])) ==
                  boundary["workers"] and
              len(boundary["cleanup"].get("worker_exitcodes", [])) ==
                  boundary["workers"] and
              boundary["cleanup"].get("process_close_count") ==
                  boundary["workers"])),
            "resource worker cleanup")
    require(accounting["formal_ancestry_entries"] == formal["entry_count"],
            "resource ancestry accounting binding")
    receipt_monitor = receipt.get("monitor")
    validate_monitor(receipt_monitor)
    prior_counters = checkpoint["monitor"]["fresh_v10_counters"]
    final_counters = receipt_monitor["fresh_v10_counters"]
    require(all(final_counters[key] >= prior_counters[key]
                for key in prior_counters) and
            final_counters["checkpoint_bytes"] == reference["bytes"],
            "resource monotone counters/no reset")
    require(checkpoint.get("selftest") == receipt.get("selftest") and
            type(checkpoint.get("last_safe_phase")) is str,
            "resource selftest/phase binding")
    return {"path": reference["path"], "bytes": physical["bytes"],
            "sha256": physical["sha256"], "phase": checkpoint.get("phase"),
            "P_rows": 2896, "new_records": len(new_records),
            "heavy_complete": heavy_complete}


def safe_terminal(terminal: str) -> bool:
    return bool(terminal) and len(terminal) <= 512 and all(
        character.isalnum() or character in "_:.=,+-" for character in terminal)


def validate_unknown(receipt: dict[str, Any], receipt_path: Path) -> dict[str, Any]:
    validate_seal(receipt)
    terminal = receipt.get("terminal")
    require(receipt.get("schema") == SCHEMA and receipt.get("status") == "UNKNOWN" and
            type(terminal) is str and safe_terminal(terminal) and
            (terminal.startswith("UNKNOWN_INPUT:") or
             terminal.startswith("UNKNOWN_RESOURCE:phase=")) and
            receipt.get("claims") == FALSE_CLAIMS and
            receipt.get("correction_word") is None and
            receipt.get("common_word") is None and
            receipt.get("claim_boundary") == "typed unknown; no negative content" and
            receipt.get("source_snapshots") in (None, Sources.public()),
            "typed UNKNOWN envelope")
    if receipt.get("monitor") is not None:
        validate_monitor(receipt["monitor"])
    validate_source_transport(receipt, hash_source=False)
    sidecar = receipt_path.with_suffix(receipt_path.suffix + ".checkpoint.json")
    if terminal.startswith("UNKNOWN_RESOURCE:"):
        require(receipt.get("checkpoint_required") is (sidecar.is_file()),
                "resource checkpoint requirement binding")
        checkpoint_public = (validate_checkpoint_transport(receipt, receipt_path)
                             if sidecar.is_file() else None)
    else:
        require("checkpoint" not in receipt and not sidecar.exists(),
                "input terminal forbids checkpoint")
        checkpoint_public = None
    boundary = receipt.get("boundary_owner")
    if boundary is not None:
        require(boundary.get("cleanup", {}).get("complete") is True and
                boundary["cleanup"].get("live_pids_after_join") == [],
                "UNKNOWN process cleanup")
    return {"terminal": terminal, "transport_only": True,
            "checkpoint": checkpoint_public, "mathematical_flags": FALSE_CLAIMS}


def validate_selftest_envelope(receipt: dict[str, Any]) -> dict[str, Any]:
    fixture_raw, _fixture_identity = read_owner_bytes(
        ROOT / FIXTURE_PATH, 2784,
        "a96d7e400b5f71a03975b9d223b98fe6cc6c22ef8e17fe59f0eac07f4bc7e641")
    require(receipt.get("schema") == SCHEMA + "/selftest" and
            receipt.get("terminal") == SELFTEST_TERMINAL and
            receipt.get("fixture_sha256") == sha_bytes(fixture_raw) and
            receipt.get("claims") == FALSE_CLAIMS and
            type(receipt.get("selftest")) is dict,
            "SELFTEST identity envelope")
    return {"selftest": True, "production_invocations": 0,
            "mathematical_terminal": False}


def exclusive_json(path: Path, value: dict[str, Any]) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise CheckStop("stale output")
    raw = canonical(value) + b"\n"
    temporary = path.with_name(path.name + ".tmp." + str(os.getpid()))
    try:
        with temporary.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
        try:
            directory_fd = os.open(path.parent, os.O_RDONLY)
            try: os.fsync(directory_fd)
            finally: os.close(directory_fd)
        except OSError:
            pass
    finally:
        try: temporary.unlink()
        except FileNotFoundError: pass
    return len(raw), sha_bytes(raw)


def clone(value: Any) -> Any:
    return json.loads(canonical(value).decode("ascii"))


def reseal(value: dict[str, Any]) -> dict[str, Any]:
    value.pop("self_digest", None)
    return seal(value)


def write_frame(path: Path, value: dict[str, Any]) -> None:
    raw = canonical(value) + b"\n"
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def expect_physical_rejection(path: Path, value: dict[str, Any],
                              validator: Any) -> None:
    write_frame(path, value)
    candidate, _raw, _identity = open_physical(path, MAX_CANDIDATE_BYTES)
    rejected = False
    try:
        validator(candidate)
    except CheckStop:
        rejected = True
    require(rejected, "physical mutation accepted:" + path.name)


def validate_boundary_frame(runtime: dict[str, Any], frame: dict[str, Any]) -> None:
    validate_seal(frame)
    require(frame.get("schema") == SCHEMA + "/boundary-selftest-frame" and
            frame.get("orientation") == "t=g*h^-1;t*h=g" and
            frame.get("transport") == {"fault": None, "partial": False,
                "dead": False, "blocked": False, "cleanup_complete": True,
                "survivors": []} and
            frame.get("counter_floor") == frame.get("outcome", {}).get(
                "expanded_pair_count"), "boundary selftest owner frame")
    dual = parse_sparse(frame.get("dual")); workers = int(frame.get("workers"))
    epoch = int(frame.get("outcome", {}).get("epoch"))
    require(frame.get("outcome") == independent_boundary_outcome(runtime, dual,
                                                                  workers, epoch),
            "boundary selftest independent outcome")


def boundary_physical_mutations(runtime: dict[str, Any], receipt: dict[str, Any],
                                root: Path) -> list[dict[str, Any]]:
    fixture = load_fixture_bounded()
    processes = receipt["selftest"]["process_owner"]
    dual_public = processes["first_dual"]; dual = parse_sparse(dual_public)
    workers = 4; epoch = 1
    outcome = independent_boundary_outcome(runtime, dual, workers, epoch)
    baseline = seal({"schema": SCHEMA + "/boundary-selftest-frame",
        "workers": workers, "dual": dual_public, "outcome": outcome,
        "orientation": "t=g*h^-1;t*h=g",
        "transport": {"fault": None, "partial": False, "dead": False,
                      "blocked": False, "cleanup_complete": True,
                      "survivors": []},
        "counter_floor": outcome["expanded_pair_count"]})
    validate_boundary_frame(runtime, baseline)
    ledger = []
    for ordinal, name in enumerate(fixture["boundary_mutations"]):
        value = clone(baseline)
        if name == "wrong_typed_support":
            wrong = bytearray.fromhex(value["dual"][0][0]); wrong[1] = 4
            value["dual"][0][0] = bytes(wrong).hex()
            value["dual"].sort()
        elif name == "missing_interval":
            value["outcome"]["intervals"][0][1] -= 1
        elif name == "overlapping_interval":
            value["outcome"]["intervals"][1][0] -= 1
        elif name == "wrong_t_orientation":
            value["orientation"] = "t=h^-1*g"
        elif name == "changed_accumulator":
            accumulator = value["outcome"]["worker_results"][0]["accumulator"]
            if accumulator:
                accumulator[0][3] = 3 - int(accumulator[0][3])
            else:
                accumulator.append([1, blob(runtime, runtime["e3"].identity).hex(),
                                    1, 1])
        elif name == "changed_winner":
            if value["outcome"]["selected"] is None:
                value["outcome"]["selected"] = [1, blob(
                    runtime, runtime["e3"].identity).hex(), 1]
            else:
                value["outcome"]["selected"] = None
        elif name == "changed_scalar":
            scalar = value["outcome"]["selected_scalar"]
            value["outcome"]["selected_scalar"] = 1 if scalar is None else 3 - int(scalar)
        elif name == "cross_epoch_frame":
            value["outcome"]["epoch"] += 1
        elif name == "blocked_send":
            value["transport"]["blocked"] = True
        elif name == "partial_worker":
            value["transport"]["partial"] = True
        elif name == "dead_worker":
            value["transport"]["dead"] = True
        elif name == "surviving_process":
            value["transport"]["survivors"] = [999999]
        elif name == "counter_reset":
            value["counter_floor"] = 0
        else:
            raise CheckStop("unknown boundary mutation")
        expect_physical_rejection(root / f"boundary-{ordinal:02d}.json",
                                  reseal(value),
                                  lambda candidate: validate_boundary_frame(
                                      runtime, candidate))
        ledger.append({"id": name, "physical_before_actual_validator": True,
                       "narrow_CheckStop": True})
    return ledger


def coefficient_two_frame(runtime: dict[str, Any]) -> dict[str, Any]:
    relator = list(runtime["roster"][0]["word"]); delta: list[int] = []
    row, replay = runtime["model"].direct_column(delta, relator)
    factor = inverse_word(replay["conjugate_word"])
    return seal({"schema": SCHEMA + "/coefficient-two-selftest-frame",
        "coefficient": 2, "delta_word": delta, "relator_word": relator,
        "stored_row": public_sparse(row), "target": public_sparse(scaled(row, 2)),
        "factor_word": factor, "correction_word": factor})


def validate_coefficient_two_frame(runtime: dict[str, Any], value: dict[str, Any]) -> None:
    validate_seal(value)
    require(value.get("schema") == SCHEMA + "/coefficient-two-selftest-frame" and
            value.get("coefficient") == 2, "coefficient-two frame")
    row, replay = runtime["model"].direct_column(value["delta_word"],
                                                  value["relator_word"])
    inverse_row, inverse_replay = runtime["model"].direct_column(
        value["delta_word"], inverse_word(value["relator_word"]))
    factor = inverse_word(replay["conjugate_word"])
    require(public_sparse(row) == value.get("stored_row") and
            parse_sparse(value.get("target")) == scaled(row, 2) and
            inverse_row == scaled(row, 2) and
            inverse_replay["conjugate_word"] == factor and
            value.get("factor_word") == factor and
            value.get("correction_word") == factor and
            runtime["joint_group"].eval(factor) == runtime["joint_group"].identity,
            "coefficient-two literal inverse word")


def positive_physical_mutations(runtime: dict[str, Any], receipt: dict[str, Any],
                                root: Path) -> list[dict[str, Any]]:
    fixture = load_fixture_bounded()
    ledger = []
    selected_paths = (("selected_old", 0), ("selected_new", 0))
    first_group, first_index = next((group, index) for group, index in selected_paths
                                    if receipt.get(group))
    for ordinal, name in enumerate(fixture["positive_mutations"]):
        if name == "wrong_coefficient_two_word":
            value = coefficient_two_frame(runtime)
            validate_coefficient_two_frame(runtime, value)
            value = clone(value)
            value["correction_word"] = reduce_word(value["correction_word"] + [1])
            expect_physical_rejection(root / f"positive-{ordinal:02d}.json",
                                      reseal(value),
                                      lambda candidate: validate_coefficient_two_frame(
                                          runtime, candidate))
            ledger.append({"id": name, "physical_before_actual_validator": True,
                           "literal_coefficient": 2, "narrow_CheckStop": True})
            continue
        value = clone(receipt)
        if name == "omitted_selected_row":
            value[first_group].pop(first_index)
        elif name == "changed_selected_row":
            record = value[first_group][first_index]["record"]
            require(bool(record["sparse_row"]), "mutation selected sparse row")
            record["sparse_row"][0][1] = 3 - record["sparse_row"][0][1]
            record["sparse_row_sha256"] = sha_obj(record["sparse_row"])
        elif name == "changed_selected_coefficient":
            row = value[first_group][first_index]
            row["coefficient"] = 3 - int(row["coefficient"])
        elif name == "copied_sparse_equality_boolean":
            value["producer_sparse_equality"] = False
        elif name == "changed_target":
            require(bool(value["target"]), "mutation target support")
            value["target"][0][1] = 3 - value["target"][0][1]
        elif name == "changed_boundary_preimage":
            if value["boundary_preimage"]:
                value["boundary_preimage"].pop()
            else:
                value["boundary_preimage"].append({"symbol": "o:0000",
                    "coefficient": 1, "provenance": {}})
        else:
            raise CheckStop("unknown positive mutation")
        expect_physical_rejection(root / f"positive-{ordinal:02d}.json",
                                  reseal(value),
                                  lambda candidate: validate_common(
                                      runtime, candidate, include_selftest=False))
        ledger.append({"id": name, "physical_before_actual_validator": True,
                       "narrow_CheckStop": True})
    return ledger


def transport_physical_mutations(runtime: dict[str, Any], receipt: dict[str, Any],
                                 receipt_path: Path, root: Path) -> list[dict[str, Any]]:
    fixture = load_fixture_bounded()
    ledger = []
    raw = canonical(receipt) + b"\n"
    base = root / "physical-base.json"; write_frame(base, receipt)
    for ordinal, name in enumerate(fixture["physical_mutations"]):
        path = root / f"physical-{ordinal:02d}.json"
        rejected = False
        if name == "symlink_candidate":
            os.symlink(base, path)
            try:
                open_physical(path, MAX_CANDIDATE_BYTES)
            except CheckStop:
                rejected = True
        elif name == "hardlink_candidate":
            hard_source = root / "hard-source.json"; write_frame(hard_source, receipt)
            os.link(hard_source, path)
            try:
                open_physical(path, MAX_CANDIDATE_BYTES)
            except CheckStop:
                rejected = True
        elif name == "toctou_substitution":
            write_frame(path, receipt)
            substitute = root / "toctou-new.json"; write_frame(substitute, receipt)
            try:
                open_physical(path, MAX_CANDIDATE_BYTES,
                              mutation_hook=lambda target: os.replace(substitute, target))
            except CheckStop:
                rejected = True
        elif name == "stale_output":
            exclusive_json(path, {"first": True})
            try:
                exclusive_json(path, {"second": True})
            except CheckStop:
                rejected = True
        else:
            value = clone(receipt)
            validator = lambda candidate: validate_common(runtime, candidate,
                                                            include_selftest=False)
            if name == "unbound_checkpoint":
                value["checkpoint"] = {"path": "alien.json", "bytes": 1,
                                       "sha256": "0" * 64,
                                       "terminal_checkpoint": True}
            elif name == "positive_claim_on_resource_exit":
                value.update({"status": "UNKNOWN",
                    "terminal": "UNKNOWN_RESOURCE:phase=selftest:cap=wall_seconds:value=1:limit=1",
                    "claims": POSITIVE_CLAIMS, "correction_word": None,
                    "common_word": None,
                    "claim_boundary": "typed unknown; no negative content",
                    "checkpoint": {"path": "missing.json", "bytes": 1,
                                   "sha256": "0" * 64,
                                   "terminal_checkpoint": True}})
                validator = lambda candidate: validate_unknown(candidate, path)
            elif name == "separator_flip":
                value["claims"]["separator"] = True
            elif name == "cofinal_flip":
                value["claims"]["cofinal_lift"] = True
            elif name == "fake_flip":
                value["claims"]["fake"] = True
            elif name == "ihara_flip":
                value["claims"]["ihara_witness"] = True
            elif name == "terminal_reseal":
                value["terminal"] = "UNKNOWN_INPUT:resealed"
            else:
                raise CheckStop("unknown physical mutation")
            value = reseal(value); write_frame(path, value)
            candidate, _candidate_raw, _identity = open_physical(
                path, MAX_CANDIDATE_BYTES)
            try:
                validator(candidate)
            except CheckStop:
                rejected = True
        require(rejected, "transport mutation accepted:" + name)
        ledger.append({"id": name, "physical_before_actual_validator": True,
                       "narrow_CheckStop": True})
    require(len(raw) <= MAX_CANDIDATE_BYTES and receipt_path.is_file(),
            "physical mutation baseline binding")
    return ledger


def run_common_mutations(runtime: dict[str, Any], receipt: dict[str, Any],
                         receipt_path: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="r07-v7-checker-mutations-") as directory:
        root = Path(directory)
        return {"boundary": boundary_physical_mutations(runtime, receipt, root),
                "positive": positive_physical_mutations(runtime, receipt, root),
                "physical": transport_physical_mutations(runtime, receipt,
                                                            receipt_path, root),
                "actual_physical_validators": True,
                "broad_exception_catch": False}


def run_unknown_transport_mutations(receipt: dict[str, Any],
                                    receipt_path: Path) -> dict[str, Any]:
    fixture = load_fixture_bounded()
    ledger = []
    with tempfile.TemporaryDirectory(prefix="r07-v7-unknown-mutations-") as directory:
        root = Path(directory); base = root / "base.json"; write_frame(base, receipt)
        if str(receipt.get("terminal", "")).startswith("UNKNOWN_RESOURCE:"):
            reference = receipt["checkpoint"]
            original = receipt_path.parent / reference["path"]
            checkpoint, _raw, _identity = open_physical(
                original, MAX_CHECKPOINT_BYTES,
                {"bytes": reference["bytes"], "sha256": reference["sha256"]})
            write_frame(root / reference["path"], checkpoint)
        for ordinal, name in enumerate(fixture["physical_mutations"]):
            path = root / f"unknown-{ordinal:02d}.json"; rejected = False
            if name == "symlink_candidate":
                os.symlink(base, path)
                try:
                    open_physical(path, MAX_CANDIDATE_BYTES)
                except CheckStop:
                    rejected = True
            elif name == "hardlink_candidate":
                source = root / "unknown-hard-source.json"; write_frame(source, receipt)
                os.link(source, path)
                try:
                    open_physical(path, MAX_CANDIDATE_BYTES)
                except CheckStop:
                    rejected = True
            elif name == "toctou_substitution":
                write_frame(path, receipt)
                substitute = root / "unknown-toctou-new.json"
                write_frame(substitute, receipt)
                try:
                    open_physical(path, MAX_CANDIDATE_BYTES,
                        mutation_hook=lambda target: os.replace(substitute, target))
                except CheckStop:
                    rejected = True
            elif name == "stale_output":
                exclusive_json(path, {"first": True})
                try:
                    exclusive_json(path, {"second": True})
                except CheckStop:
                    rejected = True
            else:
                value = clone(receipt)
                if name == "unbound_checkpoint":
                    value["checkpoint"] = {"path": "unbound.json", "bytes": 1,
                        "sha256": "0" * 64, "terminal_checkpoint": True}
                    value["terminal"] = (
                        "UNKNOWN_RESOURCE:phase=selftest:cap=wall_seconds:value=1:limit=1")
                elif name == "positive_claim_on_resource_exit":
                    value["terminal"] = (
                        "UNKNOWN_RESOURCE:phase=selftest:cap=wall_seconds:value=1:limit=1")
                    value["claims"]["common_word"] = True
                elif name == "separator_flip":
                    value["claims"]["separator"] = True
                elif name == "cofinal_flip":
                    value["claims"]["cofinal_lift"] = True
                elif name == "fake_flip":
                    value["claims"]["fake"] = True
                elif name == "ihara_flip":
                    value["claims"]["ihara_witness"] = True
                elif name == "terminal_reseal":
                    value["terminal"] = COMMON
                else:
                    raise CheckStop("unknown UNKNOWN mutation")
                expect_physical_rejection(path, reseal(value),
                    lambda candidate, candidate_path=path: validate_unknown(
                        candidate, candidate_path))
                rejected = True
            require(rejected, "UNKNOWN transport mutation accepted:" + name)
            ledger.append({"id": name, "physical_before_actual_validator": True,
                           "narrow_CheckStop": True})
    return {"physical": ledger, "transport_only": True,
            "positive_mathematics_built": False,
            "broad_exception_catch": False}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--receipt", type=Path, required=True)
    value.add_argument("--verdict", type=Path, required=True)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    receipt_path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    verdict_path = args.verdict if args.verdict.is_absolute() else ROOT / args.verdict
    require(not verdict_path.exists(), "stale verdict")
    receipt, _raw, identity = open_physical(receipt_path, MAX_CANDIDATE_BYTES)
    terminal = str(receipt.get("terminal", ""))
    if terminal == SELFTEST_TERMINAL:
        sources = Sources(); sources.authenticate()
        runtime = build_checker_light(sources)
        validate_selftest(runtime, receipt)
        derived = validate_selftest_envelope(receipt)
        mutations = {"executed": False, "authority": "SELFTEST envelope only"}
        verdict = seal({"schema": VERDICT_SCHEMA, "status": "PASS",
            "terminal": terminal, "receipt_physical": identity,
            "derived": derived, "mutation_ledger": mutations,
            "source_snapshots": Sources.public(),
            "claims": dict(FALSE_CLAIMS), "authority": "SELFTEST route"})
    elif terminal == COMMON:
        sources = Sources(); sources.authenticate()
        task176_receipt = validate_task176_authority(sources)
        task176_owners = decode_task176_owners(sources)
        require(not receipt_path.with_suffix(
            receipt_path.suffix + ".checkpoint.json").exists(),
            "COMMON forbids checkpoint sidecar")
        validate_source_transport(receipt, hash_source=False)
        _source_value, source_raw = read_bound_source(receipt)
        runtime = build_checker_light(sources)
        runtime["task176_receipt"] = task176_receipt
        runtime["task176_owners"] = task176_owners
        derived = validate_common(runtime, receipt, source_raw=source_raw)
        mutations = {"executed": False, "authority": "SELFTEST artifact only"}
        verdict = seal({"schema": VERDICT_SCHEMA, "status": "PASS",
            "terminal": COMMON, "receipt_physical": identity,
            "derived": derived, "mutation_ledger": mutations,
            "source_snapshots": Sources.public(),
            "producer_pin": {"path": PRODUCER_PIN[0], "bytes": PRODUCER_PIN[1],
                             "sha256": PRODUCER_PIN[2]},
            "claims": {"finite_A0_candidate": True, "common_word": True,
                "separator": False, "negative": False, "cofinal_lift": False,
                "fake": False, "ihara_witness": False},
            "authority": "helper-nonshared selected-support replay"})
    else:
        derived = validate_unknown(receipt, receipt_path)
        unknown_mutations = {"executed": False, "authority": "SELFTEST artifact only"}
        verdict = seal({"schema": VERDICT_SCHEMA, "status": "PASS",
            "terminal": terminal, "receipt_physical": identity,
            "derived": derived, "mutation_ledger": unknown_mutations,
            "source_snapshots": Sources.public(),
            "producer_pin": {"path": PRODUCER_PIN[0], "bytes": PRODUCER_PIN[1],
                             "sha256": PRODUCER_PIN[2]},
            "claims": {"finite_A0_candidate": False, **FALSE_CLAIMS},
            "authority": "bounded physical transport only; no mathematics"})
    exclusive_json(verdict_path, verdict)
    print(CHECKER_PREFIX + " " + terminal, flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckStop as exc:
        print(CHECKER_PREFIX + " STOP:" + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(2)
