#!/usr/bin/env python3
"""Bounded canonical precision-two lift producer for the authenticated P1 DAG.

The actual mode is deliberately a small release boundary around the already
accepted semantic replay.  It streams one packed degree-two row at a time and
does not construct the legacy global presentation or any physical/module
builder.  Packet leaves use the complete filtered projector from v486.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.machinery
import json
import math
import mmap
import os
import shutil
import stat
import sys
import tempfile
import time
import traceback
import types
from pathlib import Path
from typing import Any, Callable

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
G1_PATH = ROOT / "search/d972_r07_a0_first_rung_grade1_v4.py"
P2_PATH = ROOT / "search/d972_r07_a0_first_rung_grade2_prebuild_v1.py"
SEM_PATH = ROOT / "search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py"
CHECKER_PATH = ROOT / "crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v5.py"
STRUCTURAL_PATH = ROOT / "search/d972_r07_grade2_specific_owner_prejoin_v1.py"
FLOOR_PATH = ROOT / "search/d972_r07_a0_c2fourier_joint_floor_v1.py"
WORDS_PATH = ROOT / "scratchpad/a0_paper_words_v1.json"

G1_SHA = "1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4"
P2_SHA = "acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8"
SEM_SHA = "dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf"
CHECKER_SHA = "bc60882b3ee22aa449c51cc280491b3d66df384a814a7033e418454f66900f97"
STRUCTURAL_SHA = "38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73"
FLOOR_SHA = "6201ae0b5c1d648529ac648a574c5096b8088fe341423724556860d9d3f23fba"
WORDS_SHA = "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"

SOURCE_RUN = "33677346616"
SOURCE_ATTEMPT = "1"
SOURCE_HEAD = "22c6dddb43d107c05e65f53ad898823ae8ebe276"
CHECKER_RESULT_SHA = "405e1b26f971f67cb73129071a77346b126d0228c84219c2c3b0d879c63c99d5"
CHECKER_WORKFLOW_RECEIPT_SHA = "323ca2603b9ff7c42449fc0e2421c190eedcd7cd62471b695dee991fb1b728eb"
CHECKER_WORKFLOW_RUN_ID = 33819301663
CHECKER_WORKFLOW_RUN_ATTEMPT = 1
CHECKER_WORKFLOW_COMMIT = "e8a4de593700a81fb2a026366e349b89b640a6e8"
CHECKER_SUCCESS_ARTIFACT = {
    "id": 9918207444,
    "name": "task757-p1-semantic-checker-only-v3-success-33819301663-1",
    "archive_bytes": 24694,
    "digest": "sha256:f99fd6ce1172cc349b249ead8dbb8e75c8c8bd8a1b8a0493dfd4596aee5fbf0c",
}
PRODUCER_RUN = "33814881435"
PRODUCER_ATTEMPT = "1"
PRODUCER_HEAD = "15778e83c52941040ef9d4289ab76d897ee30ebc"
PRODUCER_ARTIFACT = {
    "id": 9916479231,
    "name": "task729-p1-semantic-six-receipts-33814881435-1",
    "archive_bytes": 8412,
    "digest": "sha256:91281261a272e6ff48104a579a86e9cb300fc1543eaad1321b609e6d83564245",
}
PRODUCER_JOBS = (
    (100844698807, "preflight", "completed", "success"),
    (100844805339, "prepare", "completed", "success"),
    (100846454006, "block-0", "completed", "success"),
    (100846453918, "block-1", "completed", "success"),
    (100846453996, "block-2", "completed", "success"),
    (100846453927, "block-3", "completed", "success"),
    (100847550237, "join", "completed", "success"),
    (100847634660, "independent-check", "completed", "failure"),
)
ACCEPTED_RECEIPT_HASHES = {
    "prepare": "9caf8cbf04742b1400c5c63d765508308af72ef773050af5562221a082fd159a",
    "blocks": [
        "e9271d20739aee299620ef6e8d53dd940ea10ed1ab688bd61b69c7fb0ff4afc8",
        "7f34bb964665078727c7ed2b5e5165c50b1763003d573789d7406a6b06445eca",
        "6d8ebdf7b9495608c89779ecfd7ca8f3c1a84790fc8e2b6b6fc5dd292c530e6a",
        "a558c466862bf050bf8c850aaf47be633ae1f0bce9785f18b410cb0eff9f6d9d",
    ],
    "join": "a3479e7ebc010fbfde4d42c95eebd8cf81cc5eeab9ef37ab77ba2284fb8b27c8",
}
PREPARE_DIGEST = "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865"
PARENTS = (
    "9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74",
    "d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6",
    "a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac",
    "642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01",
)
BASIS = (
    "cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39",
    "0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461",
    "602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6",
    "4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9",
)
OLD_RANKS = (505, 503, 503, 503)
NEW_RANKS = (1509, 1512, 1512, 1512)
ORDER = [0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059]
OLD_ORIGIN_RANGES = ((0, 2064), (2064, 4120), (4120, 6176), (6176, 8232))
CHARACTERS = ((0, 0), (0, 1), (1, 0), (1, 1))
ACTORS = (1, -1, 2, -2)
MONOMIALS = ((2, 0, 0), (1, 1, 0), (1, 0, 1),
             (0, 2, 0), (0, 1, 1), (0, 0, 2))
SOURCE_BASE = 6048
SOURCE_BLOCK = 18144
SOURCE_TOTAL = 72576
D2_WIDTH = 145152
ROW_BYTES = 36288
ROWS = 8059
CACHE_BYTES = ROW_BYTES * ROWS
FALSE_CLAIMS = {key: False for key in
                 ("A0", "COMMON", "COFINAL", "FAKE", "IHARA", "verified")}

# v8 checkpoint ABI.  The mathematical stream below is intentionally still
# the v6 stream; these constants only describe durable transport state.
CHECKPOINT_SCHEMA = (
    "d972.r07.canonical-p1-dag-degree2-lift.checkpoint.v8")
CHECKPOINT_STATUS = "UNCHECKED_PREFIX_CHECKPOINT"
CHECKPOINT_INTERVAL = 128
CHECKPOINT_FILES = ("degree2.cache.bin", "instructions.jsonl")

RUNTIME_PHASE = "startup"


def runtime_phase(value: str) -> None:
    global RUNTIME_PHASE
    RUNTIME_PHASE = value
CHECKER_FLAGS = {key: False for key in
                 ("A0", "COMMON", "COMPATIBLE_LIFT", "FAKE", "FULL_Q0",
                  "IHARA", "ORDER_54432", "verified")}

# Exactly seven immutable semantic inputs are recorded in every final
# manifest.  The producer, semantic replay, and checker executables are
# additionally separated in the launch manifest.
SEMANTIC_FILES = {
    "grade1_v4": G1_SHA,
    "grade2_prebuild_v1": P2_SHA,
    "semantic_v5": SEM_SHA,
    "checker_v5": CHECKER_SHA,
    "structural_v1": STRUCTURAL_SHA,
    "floor_v1": FLOOR_SHA,
    "words": WORDS_SHA,
}
IMPORT_HASHES = {
    "grade1_v4": G1_SHA,
    "grade2_prebuild_v1": P2_SHA,
    "semantic_v5": SEM_SHA,
    "structural_v1": STRUCTURAL_SHA,
    "floor_v1": FLOOR_SHA,
}
FORBIDDEN = {
    "origin_full_lift", "build_b1_degree2_lifts", "full_lower_zero",
    "assemble_b1_relations", "build_module_core", "build_module_state",
    "build_physical_core", "build_physical_state",
}


class ResourceStop(RuntimeError):
    """A bounded resource stop which can never promote a candidate."""


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_reparse(info: os.stat_result) -> bool:
    return bool(getattr(info, "st_file_attributes", 0) & 0x400)


def stable_identity(info: os.stat_result) -> tuple[int, int, int, int, int]:
    return (int(info.st_dev), int(info.st_ino), int(info.st_size),
            int(info.st_mtime_ns), int(info.st_ctime_ns))


def regular(path: Path) -> os.stat_result:
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and not stat.S_ISLNK(info.st_mode)
            and not is_reparse(info), "unsafe_file:" + str(path))
    return info


def canonical_file(path: Path) -> tuple[Any, bytes]:
    regular(path)
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise RuntimeError("json:" + str(exc)) from exc
    require(raw == canonical(value), "noncanonical_json:" + path.name)
    return value, raw


def read_words() -> tuple[dict[str, Any], bytes]:
    regular(WORDS_PATH)
    raw = WORDS_PATH.read_bytes()
    require(sha(raw) == WORDS_SHA, "word_input_pin")
    try:
        words = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise RuntimeError("word_input_json") from exc
    require(isinstance(words, dict), "word_input_shape")
    relators = words.get("relators")
    require(isinstance(relators, list) and len(relators) == 44,
            "relator_count")
    for word in relators:
        require(isinstance(word, list) and all(
            plain_int(x) and x in (-2, -1, 1, 2) for x in word),
            "relator_word")
    return words, raw


def load_exact(path: Path, expected: str, name: str) -> types.ModuleType:
    """Compile exactly the bytes hashed, without a second path open.

    ``exec_module`` on a normal file loader would reopen a mutable path.  A
    small module object and ``exec(compile(raw))`` retain the authenticated
    source bytes while preserving ordinary imports for the accepted modules.
    """
    raw = path.read_bytes()
    require(sha(raw) == expected, "source_pin:" + path.name)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    module.__spec__ = importlib.machinery.ModuleSpec(
        name, loader=None, origin=str(path))
    marker = object()
    previous = sys.modules.get(name, marker)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(path), "exec"), module.__dict__)
    except BaseException:
        if previous is marker:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
        raise
    return module


def load_dependencies() -> dict[str, types.ModuleType]:
    # The floor and grade-one modules are installed under their ordinary names
    # before prebuild execution; P2's transitive import therefore cannot
    # reopen a different grade-one source file.
    floor = load_exact(FLOOR_PATH, FLOOR_SHA,
                       "d972_r07_a0_c2fourier_joint_floor_v1")
    g1 = load_exact(G1_PATH, G1_SHA,
                    "d972_r07_a0_first_rung_grade1_v4")
    p2 = load_exact(P2_PATH, P2_SHA,
                    "d972_r07_a0_first_rung_grade2_prebuild_v1")
    structural = load_exact(STRUCTURAL_PATH, STRUCTURAL_SHA,
                            "task746_structural")
    sem = load_exact(SEM_PATH, SEM_SHA, "task746_semantic_v5")
    checker = load_exact(CHECKER_PATH, CHECKER_SHA, "task767_checker_v5")
    require(getattr(p2, "grade1", None) is g1,
            "transitive_grade1_identity")
    require(getattr(g1, "floor", None) is floor,
            "transitive_floor_identity")
    # v5 has a path loader for its own independent replay.  The producer only
    # needs v5's receipt/join logic, so bind that loader to the already
    # authenticated ordinary grade-one module.
    sem.load_v4 = lambda: g1
    return {"floor": floor, "g1": g1, "p2": p2, "structural": structural,
            "sem": sem, "checker": checker}


def rss_linux() -> int:
    """Mandatory Linux RSS source for actual mode."""
    require(sys.platform.startswith("linux"),
            "UNKNOWN_RESOURCE:rss_unavailable_non_linux")
    try:
        text = Path("/proc/self/status").read_text(encoding="ascii")
        for line in text.splitlines():
            if line.startswith("VmRSS:"):
                fields = line.split()
                if len(fields) < 2:
                    raise ResourceStop("UNKNOWN_RESOURCE:rss_parse")
                try:
                    value = int(fields[1])
                except ValueError as exc:
                    raise ResourceStop("UNKNOWN_RESOURCE:rss_parse") from exc
                if value < 0:
                    raise ResourceStop("UNKNOWN_RESOURCE:rss_parse")
                return value * 1024
    except (OSError, UnicodeError, ValueError) as exc:
        raise ResourceStop("UNKNOWN_RESOURCE:rss_unavailable") from exc
    raise ResourceStop("UNKNOWN_RESOURCE:rss_unavailable")


def enforce(started: float, phase: str) -> int:
    try:
        seconds = float(os.environ.get("D972_LIFT_SECONDS", "43200"))
        cap = int(os.environ.get("D972_LIFT_MAX_RSS", str(8 * 1024**3)))
    except ValueError as exc:
        raise ResourceStop("UNKNOWN_RESOURCE:invalid_cap") from exc
    if not math.isfinite(seconds) or seconds < 0 or cap < 0:
        raise ResourceStop("UNKNOWN_RESOURCE:invalid_cap")
    if time.monotonic() - started > seconds:
        raise ResourceStop("UNKNOWN_RESOURCE:" + phase + ":time")
    rss = rss_linux()
    if rss > cap:
        raise ResourceStop("UNKNOWN_RESOURCE:" + phase + ":rss")
    return rss


class FileRegistry:
    """Compact path/size/digest/stable-identity registry for input bytes."""

    def __init__(self) -> None:
        self._entries: dict[str, dict[str, Any]] = {}

    def add(self, path: Path, digest: str, kind: str) -> None:
        original = path.absolute()
        regular(original)
        resolved = original.resolve(strict=True)
        info = regular(resolved)
        require(isinstance(digest, str) and len(digest) == 64,
                "registry_digest")
        entry = {
            "kind": kind,
            "path": str(resolved),
            "bytes": int(info.st_size),
            "sha256": digest,
            "identity": list(stable_identity(info)),
        }
        previous = self._entries.get(str(resolved))
        require(previous is None or previous == entry, "registry_duplicate")
        self._entries[str(resolved)] = entry

    def entries(self) -> list[dict[str, Any]]:
        return [self._entries[key] for key in sorted(self._entries)]

    def verify(self) -> None:
        for entry in self.entries():
            path = Path(entry["path"])
            before = regular(path)
            before_id = stable_identity(before)
            digest = file_sha(path)
            after = regular(path)
            require(stable_identity(after) == before_id,
                    "registry_changed:" + path.name)
            require(int(after.st_size) == entry["bytes"]
                    and digest == entry["sha256"],
                    "registry_digest_changed:" + path.name)


def register_blob(registry: FileRegistry, root: Path, receipt: dict[str, Any],
                  kind: str) -> None:
    require(isinstance(receipt, dict) and isinstance(receipt.get("file"), str),
            "registry_blob_receipt")
    registry.add(root / receipt["file"], receipt["sha256"], kind)


def nonnegative_size(value: Any, reason: str) -> int:
    require(plain_int(value) and value >= 0, reason)
    return int(value)


def artifact_entry(root: Path, role: str, stem: str, digest: str,
                   body_size: int) -> dict[str, Any]:
    body_size = nonnegative_size(body_size, "artifact_body_size")
    require(isinstance(digest, str) and len(digest) == 64
            and all(char in "0123456789abcdef" for char in digest),
            "artifact_body_digest")
    body_path = root / f"{stem}.{digest}.json"
    info = regular(body_path)
    require(int(info.st_size) == body_size,
            "artifact_body_identity")
    return {
        "role": role,
        "root": str(root.resolve(strict=True)),
        "body_file": body_path.name,
        "body_sha256": digest,
        "body_bytes": body_size,
        "identity": list(stable_identity(info)),
    }


def launch_expected_receipts(digests: list[str]) -> dict[str, Any]:
    require(len(digests) == 6, "receipt_digest_count")
    return {"prepare": digests[0], "blocks": digests[1:5],
            "join": digests[5]}


LAUNCH_KEYS = {
    "schema", "raw_artifacts", "receipt_hashes", "checker_result_sha256",
    "checker_workflow_receipt_sha256", "checker_success_artifact",
    "source_run", "source_attempt", "source_head", "executable_hashes",
    "import_hashes", "semantic_file_hashes",
}


CHECKER_WORKFLOW_RECEIPT_KEYS = {
    "schema", "workflow_run_id", "workflow_run_attempt",
    "workflow_commit_sha", "producer_run", "producer_attempt",
    "producer_head", "producer_run_status", "producer_run_conclusion",
    "producer_jobs", "producer_artifact", "producer_sha256",
    "checker_sha256", "independent_result_sha256",
    "producer_receipt_sha256", "checker_elapsed_seconds",
    "checker_peak_rss_bytes", "checker_process", "claim_flags",
    "independent_checker", "verified",
}


def validate_artifact_identity(value: Any, expected: dict[str, Any],
                               reason: str) -> None:
    require(isinstance(value, dict) and set(value) == {
        "id", "name", "archive_bytes", "digest"
    }, reason + ":keys")
    require(plain_int(value["id"]) and plain_int(value["archive_bytes"])
            and value["id"] >= 0 and value["archive_bytes"] >= 0
            and isinstance(value["name"], str) and value["name"]
            and isinstance(value["digest"], str)
            and value["digest"].startswith("sha256:")
            and value == expected, reason + ":identity")


def validate_elapsed_clock(value: Any) -> None:
    require(isinstance(value, str) and value, "checker_process_elapsed_type")
    fields = value.split(":")
    require(len(fields) in (1, 2, 3), "checker_process_elapsed_shape")
    try:
        leading = [int(field) for field in fields[:-1]]
        seconds = float(fields[-1])
    except ValueError as exc:
        raise RuntimeError("checker_process_elapsed_value") from exc
    require(all(entry >= 0 for entry in leading)
            and math.isfinite(seconds) and 0 <= seconds < 60,
            "checker_process_elapsed_range")
    if len(fields) == 3:
        require(leading[1] < 60, "checker_process_elapsed_minutes")


def validate_checker_workflow_receipt(value: Any, checker_result: dict[str, Any],
                                      checker_result_sha: str,
                                      receipt_digests: list[str]) -> None:
    require(isinstance(value, dict)
            and set(value) == CHECKER_WORKFLOW_RECEIPT_KEYS,
            "checker_workflow_receipt_keys")
    require(value["schema"] ==
            "d972.r07.p1.componentwise.checker-only.v3.workflow-receipt",
            "checker_workflow_receipt_schema")
    require(plain_int(value["workflow_run_id"])
            and value["workflow_run_id"] == CHECKER_WORKFLOW_RUN_ID
            and plain_int(value["workflow_run_attempt"])
            and value["workflow_run_attempt"] == CHECKER_WORKFLOW_RUN_ATTEMPT
            and isinstance(value["workflow_commit_sha"], str)
            and value["workflow_commit_sha"] == CHECKER_WORKFLOW_COMMIT,
            "checker_workflow_identity")
    require(isinstance(value["producer_run"], str)
            and value["producer_run"] == PRODUCER_RUN
            and isinstance(value["producer_attempt"], str)
            and value["producer_attempt"] == PRODUCER_ATTEMPT
            and isinstance(value["producer_head"], str)
            and value["producer_head"] == PRODUCER_HEAD
            and isinstance(value["producer_run_status"], str)
            and value["producer_run_status"] == "completed"
            and isinstance(value["producer_run_conclusion"], str)
            and value["producer_run_conclusion"] == "failure",
            "checker_workflow_producer_identity")
    jobs = value["producer_jobs"]
    require(isinstance(jobs, list) and len(jobs) == len(PRODUCER_JOBS),
            "checker_workflow_jobs_shape")
    for row, expected in zip(jobs, PRODUCER_JOBS):
        require(isinstance(row, dict) and set(row) == {
            "id", "name", "status", "conclusion"
        } and plain_int(row["id"])
                and all(isinstance(row[key], str)
                        for key in ("name", "status", "conclusion"))
                and (row["id"], row["name"], row["status"],
                     row["conclusion"]) == expected,
                "checker_workflow_job")
    validate_artifact_identity(value["producer_artifact"], PRODUCER_ARTIFACT,
                               "checker_workflow_producer_artifact")
    require(isinstance(value["producer_sha256"], str)
            and value["producer_sha256"] == SEM_SHA
            and isinstance(value["checker_sha256"], str)
            and value["checker_sha256"] == CHECKER_SHA,
            "checker_workflow_executables")
    require(checker_result_sha == CHECKER_RESULT_SHA
            and value["independent_result_sha256"] == checker_result_sha,
            "checker_workflow_result_link")
    expected_receipts = launch_expected_receipts(receipt_digests)
    require(expected_receipts == ACCEPTED_RECEIPT_HASHES
            and value["producer_receipt_sha256"] == expected_receipts,
            "checker_workflow_receipt_link")
    finite_telemetry(value["checker_elapsed_seconds"],
                     "checker_workflow_elapsed")
    require(value["checker_elapsed_seconds"] == checker_result["elapsed_seconds"],
            "checker_workflow_elapsed_link")
    require(plain_int(value["checker_peak_rss_bytes"])
            and value["checker_peak_rss_bytes"] >= 0
            and value["checker_peak_rss_bytes"] ==
                checker_result["peak_rss_bytes"],
            "checker_workflow_peak_link")
    process = value["checker_process"]
    require(isinstance(process, dict) and set(process) == {
        "elapsed_wall_clock", "peak_rss_kbytes"
    }, "checker_workflow_process_keys")
    validate_elapsed_clock(process["elapsed_wall_clock"])
    require(plain_int(process["peak_rss_kbytes"])
            and process["peak_rss_kbytes"] >= 0,
            "checker_workflow_process_peak")
    require(value["claim_flags"] == CHECKER_FLAGS
            and all(value["claim_flags"][key] is False for key in CHECKER_FLAGS),
            "checker_workflow_claim_flags")
    require(value["independent_checker"] is True
            and value["verified"] is False,
            "checker_workflow_independent_flags")


def validate_launch_manifest(value: Any, producer_sha: str,
                             receipt_digests: list[str],
                             checker_result_sha: str,
                             checker_workflow_receipt_sha: str,
                             raw_artifacts: list[dict[str, Any]]) -> None:
    require(isinstance(value, dict) and set(value) == LAUNCH_KEYS,
            "launch_keys")
    require(value["schema"] ==
            "d972.r07.canonical-p1-dag-degree2-lift.launch.v6",
            "launch_schema")
    require(value["source_run"] == SOURCE_RUN
            and isinstance(value["source_run"], str), "launch_source_run")
    require(value["source_attempt"] == SOURCE_ATTEMPT
            and isinstance(value["source_attempt"], str),
            "launch_source_attempt")
    require(value["source_head"] == SOURCE_HEAD
            and isinstance(value["source_head"], str), "launch_source_head")
    require(value["receipt_hashes"] == launch_expected_receipts(receipt_digests)
            and value["receipt_hashes"] == ACCEPTED_RECEIPT_HASHES,
            "launch_receipts")
    require(checker_result_sha == CHECKER_RESULT_SHA
            and value["checker_result_sha256"] == checker_result_sha,
            "launch_checker_result")
    require(checker_workflow_receipt_sha == CHECKER_WORKFLOW_RECEIPT_SHA
            and value["checker_workflow_receipt_sha256"] ==
                checker_workflow_receipt_sha,
            "launch_checker_workflow_receipt")
    validate_artifact_identity(value["checker_success_artifact"],
                               CHECKER_SUCCESS_ARTIFACT,
                               "launch_checker_success_artifact")
    require(value["raw_artifacts"] == raw_artifacts,
            "launch_raw_artifacts")
    require(value["executable_hashes"] == {
        "producer_v8": producer_sha, "semantic_v5": SEM_SHA,
        "checker_v5": CHECKER_SHA,
    }, "launch_executable_hashes")
    require(value["import_hashes"] == IMPORT_HASHES,
            "launch_import_hashes")
    require(value["semantic_file_hashes"] == SEMANTIC_FILES,
            "launch_semantic_files")


def validate_node(node: Any, pivot: int, rank: int, lead_width: int,
                  origin_kinds: set[str], origin_count: int | None = None) -> None:
    require(isinstance(node, dict) and set(node) == {
        "pivot", "lead", "scale", "origin", "reductions"
    }, "node_keys")
    require(plain_int(node["pivot"]) and node["pivot"] == pivot,
            "node_pivot")
    require(plain_int(node["lead"]) and 0 <= node["lead"] < lead_width,
            "node_lead")
    require(plain_int(node["scale"]) and node["scale"] in (1, 2),
            "node_scale")
    reductions = node["reductions"]
    require(isinstance(reductions, list), "node_reductions")
    seen: set[int] = set()
    for pair in reductions:
        require(isinstance(pair, list) and len(pair) == 2
                and plain_int(pair[0]) and plain_int(pair[1]),
                "node_reduction_type")
        index, coefficient = pair
        require(0 <= index < pivot and index not in seen
                and coefficient in (1, 2), "node_reduction_prior")
        seen.add(index)
    origin = node["origin"]
    require(isinstance(origin, dict) and origin.get("kind") in origin_kinds,
            "node_origin_kind")
    kind = origin["kind"]
    if kind == "projected_seed":
        require(set(origin) == {"kind", "seed"}
                and plain_int(origin["seed"]) and 1 <= origin["seed"] <= 44,
                "node_seed_origin")
    elif kind == "defect":
        require(set(origin) == {"kind", "origin"}
                and plain_int(origin["origin"]), "node_defect_origin")
        require(origin_count is not None and 0 <= origin["origin"] < origin_count,
                "node_defect_range")
    else:
        require(set(origin) == {"kind", "parent", "letter"}
                and plain_int(origin["parent"])
                and 0 <= origin["parent"] < pivot
                and plain_int(origin["letter"])
                and origin["letter"] in ACTORS, "node_actor_origin")


def validate_expression(expression: Any, rank: int, reason: str,
                        earlier_than: int | None = None) -> None:
    require(isinstance(expression, list), reason + ":shape")
    bound = rank if earlier_than is None else earlier_than
    for pair in expression:
        require(isinstance(pair, list) and len(pair) == 2
                and plain_int(pair[0]) and plain_int(pair[1])
                and 0 <= pair[0] < bound and pair[1] in (1, 2),
                reason + ":entry")


def validate_actor_order(value: Any, reason: str) -> None:
    require(isinstance(value, list) and len(value) == 4
            and all(plain_int(x) for x in value)
            and tuple(value) == ACTORS, reason)


def validate_defect_origins(prepare: dict[str, Any]) -> None:
    origins = prepare.get("defect_origins")
    require(isinstance(origins, list) and len(origins) == 8232,
            "defect_origins_shape")
    cursor = 0
    for character, old in enumerate(prepare["old_blocks"]):
        begin, end = OLD_ORIGIN_RANGES[character]
        require(old["defect_origin_range"] == [begin, end]
                and begin == cursor, "defect_origin_range")
        for seed in range(1, 45):
            origin = origins[cursor]
            require(isinstance(origin, dict) and set(origin) == {
                "id", "kind", "lower_character", "seed"
            } and plain_int(origin["id"]) and origin["id"] == cursor
                and origin["kind"] == "seed"
                and plain_int(origin["lower_character"])
                and origin["lower_character"] == character
                and plain_int(origin["seed"]) and origin["seed"] == seed,
                "defect_seed_origin")
            cursor += 1
        for pivot in range(OLD_RANKS[character]):
            for letter in ACTORS:
                origin = origins[cursor]
                require(isinstance(origin, dict) and set(origin) == {
                    "id", "kind", "lower_character", "pivot", "letter"
                } and plain_int(origin["id"]) and origin["id"] == cursor
                    and origin["kind"] == "transition"
                    and plain_int(origin["lower_character"])
                    and origin["lower_character"] == character
                    and plain_int(origin["pivot"]) and origin["pivot"] == pivot
                    and plain_int(origin["letter"]) and origin["letter"] == letter,
                    "defect_transition_origin")
                cursor += 1
    require(cursor == len(origins), "defect_origin_count")


def validate_authenticated_dag(prepare: dict[str, Any],
                               blocks: list[dict[str, Any]]) -> None:
    require([old["rank"] for old in prepare["old_blocks"]] == list(OLD_RANKS),
            "old_rank_constants")
    require([block["rank"] for block in blocks] == list(NEW_RANKS),
            "new_rank_constants")
    require(tuple(ORDER) == (0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059),
            "global_order_constants")
    validate_defect_origins(prepare)
    require(tuple(prepare["old_blocks"][0]["record"]["actor_order"]) == ACTORS,
            "old_actor_order")
    for character, old in enumerate(prepare["old_blocks"]):
        record = old["record"]
        validate_actor_order(record["actor_order"], "old_actor_order")
        require(len(record["dag_nodes"]) == OLD_RANKS[character]
                and len(record["actor_transitions"]) == OLD_RANKS[character],
                "old_dag_cardinality")
        for expression in record["seed_reductions"]:
            validate_expression(expression, old["rank"], "old_seed_expression")
        for row in record["actor_transitions"]:
            require(isinstance(row, list) and len(row) == 4,
                    "old_actor_row")
            for expression in row:
                validate_expression(expression, old["rank"],
                                     "old_actor_expression")
        for pivot, node in enumerate(record["dag_nodes"]):
            validate_node(node, pivot, old["rank"], 6056,
                          {"projected_seed", "actor"})
    for character, block in enumerate(blocks):
        validate_actor_order(block["actor_order"], "new_actor_order")
        require(len(block["dag_nodes"]) == NEW_RANKS[character]
                and len(block["actor_transitions"]) == NEW_RANKS[character],
                "new_dag_cardinality")
        for expression in block["origin_reductions"]:
            validate_expression(expression, block["rank"],
                                "new_origin_expression")
        for row in block["actor_transitions"]:
            require(isinstance(row, list) and len(row) == 4,
                    "new_actor_row")
            for expression in row:
                validate_expression(expression, block["rank"],
                                     "new_actor_expression")
        for pivot, node in enumerate(block["dag_nodes"]):
            validate_node(node, pivot, block["rank"], SOURCE_BLOCK,
                          {"defect", "actor"}, 8232)


def raw_component_digest(p2: Any, row: tuple[np.ndarray, ...]) -> tuple[str, dict[str, str]]:
    require(len(row) == 4, "raw_row_parts")
    names = ("p0", "p1", "p2", "aux")
    parts: dict[str, str] = {}
    for name, part in zip(names, row):
        packed = p2.grade1.pack_trits(np.asarray(part, dtype=np.uint8).reshape(-1))
        parts[name] = sha(packed.tobytes())
    return sha(canonical(parts)), parts


def full_row_digest(p2: Any, row: tuple[np.ndarray, ...]) -> str:
    return raw_component_digest(p2, row)[0]


def digest_string(value: Any, reason: str) -> None:
    require(isinstance(value, str) and len(value) == 64
            and all(char in "0123456789abcdef" for char in value), reason)


def finite_telemetry(value: Any, reason: str) -> None:
    require(isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(float(value)) and float(value) >= 0, reason)


def add_full(p2: Any, destination: tuple[np.ndarray, ...],
             source: tuple[np.ndarray, ...], scalar: int) -> None:
    for left, right in zip(destination, source):
        p2._add_mod3(left, right, scalar)


def scale_full(row: tuple[np.ndarray, ...], scale: int) -> tuple[np.ndarray, ...]:
    require(scale in (1, 2), "scale")
    return tuple(((scale * part.astype(np.uint16)) % 3).astype(np.uint8)
                 for part in row)


def flatten_p1(p2: Any, row: tuple[np.ndarray, ...]) -> np.ndarray:
    return p2.flatten_precision1(row[0], row[1], row[3])


def full_from(cache: "PackedCache", p2: Any, p1store: "LazyP1",
              index: int) -> tuple[np.ndarray, ...]:
    p0, p1, aux = p2.split_precision1(p1store.row(index))
    d2 = cache.row(p2, index).reshape(4, p2.SOURCE_DEGREE2_PER_CHARACTER)
    return p0, p1, d2, aux


class PackedCache:
    """Append-only packed rows with positioned reads of earlier rows only.

    Fresh construction truncates a newly-created path.  ``from_resume``
    opens an already authenticated prefix without reading it a second time;
    the caller supplies the digest and per-row receipts reconstructed by the
    single resume scan.
    """

    def __init__(self, path: Path, row_width: int = D2_WIDTH,
                 mode: str = "w+b"):
        require(plain_int(row_width) and row_width > 0 and row_width % 4 == 0,
                "cache_width")
        require(mode in ("w+b", "r+b"), "cache_mode")
        self.path = path
        self.row_width = row_width
        self.row_bytes = row_width // 4
        self.cursor = 0
        self.stream = path.open(mode)
        self.digest = hashlib.sha256()
        self.row_hashes: list[str] = []

    @classmethod
    def from_resume(cls, path: Path, row_width: int, cursor: int,
                    digest: hashlib._Hash, row_hashes: list[str]) -> "PackedCache":
        require(plain_int(cursor) and cursor >= 0, "cache_resume_cursor")
        require(len(row_hashes) == cursor, "cache_resume_hash_count")
        obj = cls.__new__(cls)
        obj.path = path
        obj.row_width = row_width
        obj.row_bytes = row_width // 4
        obj.cursor = cursor
        obj.stream = path.open("r+b")
        obj.stream.seek(0, os.SEEK_END)
        obj.digest = digest
        obj.row_hashes = list(row_hashes)
        return obj

    def append(self, p2: Any, dense: np.ndarray) -> tuple[int, str]:
        dense = np.asarray(dense, dtype=np.uint8).reshape(-1)
        require(dense.shape == (self.row_width,) and not np.any(dense > 2),
                "cache_append_shape")
        raw = p2.grade1.pack_trits(dense).tobytes()
        require(len(raw) == self.row_bytes and max(raw, default=0) <= 80,
                "cache_append_packing")
        offset = self.cursor * self.row_bytes
        self.stream.seek(offset)
        self.stream.write(raw)
        self.digest.update(raw)
        row_digest = sha(raw)
        self.row_hashes.append(row_digest)
        self.cursor += 1
        return offset, row_digest

    def row_sha(self, index: int) -> str:
        require(plain_int(index) and 0 <= index < self.cursor,
                "cache_row_sha_prior_only")
        return self.row_hashes[index]

    def row(self, p2: Any, index: int) -> np.ndarray:
        require(plain_int(index) and 0 <= index < self.cursor,
                "cache_row_prior_only")
        self.stream.seek(index * self.row_bytes)
        raw = self.stream.read(self.row_bytes)
        require(len(raw) == self.row_bytes, "cache_eof")
        return p2.grade1.unpack_trits(np.frombuffer(raw, dtype=np.uint8),
                                      self.row_width)

    def sync(self) -> int:
        self.stream.flush()
        os.fsync(self.stream.fileno())
        return int(self.path.stat().st_size)

    def close(self) -> None:
        if not self.stream.closed:
            self.stream.flush()
            os.fsync(self.stream.fileno())
            self.stream.close()


class InstructionSink:
    def __init__(self, path: Path, mode: str = "wb", rows: int = 0,
                 byte_count: int = 0,
                 digest: hashlib._Hash | None = None,
                 ancestry_head: str | None = None):
        require(mode in ("wb", "ab"), "instruction_mode")
        require(plain_int(rows) and rows >= 0 and plain_int(byte_count)
                and byte_count >= 0, "instruction_resume_counters")
        self.path = path
        self.stream = path.open(mode)
        self.rows = rows
        self.bytes = byte_count
        self.digest = digest if digest is not None else hashlib.sha256()
        self.ancestry_head = ancestry_head or (b"\0" * 32).hex()

    def write(self, value: dict[str, Any]) -> None:
        data = canonical(value)
        require(data.endswith(b"\n"), "instruction_lf")
        self.stream.write(data)
        self.digest.update(data)
        self.rows += 1
        self.bytes += len(data)
        head = value.get("ancestry_sha256")
        if isinstance(head, str):
            self.ancestry_head = head

    @classmethod
    def from_resume(cls, path: Path, rows: int, byte_count: int,
                    digest: hashlib._Hash,
                    ancestry_head: str) -> "InstructionSink":
        obj = cls.__new__(cls)
        obj.path = path
        obj.stream = path.open("ab")
        obj.rows = rows
        obj.bytes = byte_count
        obj.digest = digest
        obj.ancestry_head = ancestry_head
        return obj

    def sync(self) -> int:
        self.stream.flush()
        os.fsync(self.stream.fileno())
        return int(self.path.stat().st_size)

    def close(self) -> None:
        if not self.stream.closed:
            self.stream.flush()
            os.fsync(self.stream.fileno())
            self.stream.close()


def _fsync_directory(path: Path) -> None:
    """Best-effort directory durability for the atomic sidecar replace."""
    try:
        descriptor = os.open(str(path), getattr(os, "O_DIRECTORY", 0))
    except (AttributeError, OSError):
        return
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def checkpoint(cache: PackedCache, instructions: InstructionSink,
               phase: str, started: float,
               rss_reader: Callable[[], int] = rss_linux,
               checkpoint_path: Path | None = None,
               pins: dict[str, Any] | None = None,
               global_order: list[int] | tuple[int, ...] = ORDER,
               total_rows: int = ROWS) -> dict[str, Any] | None:
    """Durably publish one exact prefix boundary.

    The append-only streams are fsynced first.  Only then is the canonical
    sidecar written to a sibling temporary file and atomically replaced.  A
    caller which does not pass ``checkpoint_path`` retains the old v6
    telemetry-only behaviour used by the tiny algebra fixtures.
    """
    cache_bytes = cache.sync()
    instruction_bytes = instructions.sync()
    rss = rss_reader()
    payload: dict[str, Any] | None = None
    if checkpoint_path is not None:
        require(isinstance(pins, dict), "checkpoint_pins_missing")
        require(plain_int(total_rows) and total_rows >= 0
                and cache.cursor <= total_rows, "checkpoint_total_rows")
        order = [int(value) for value in global_order]
        require(order and order[0] == 0 and order[-1] == total_rows,
                "checkpoint_order")
        require(cache.cursor == instructions.rows
                and cache_bytes == cache.cursor * cache.row_bytes,
                "checkpoint_prefix_counters")
        head = instructions.ancestry_head
        digest_string(head, "checkpoint_ancestry_head")
        final_lf = cache.cursor == 0 or instruction_bytes > 0
        payload = {
            "schema": CHECKPOINT_SCHEMA,
            "status": CHECKPOINT_STATUS,
            "phase": phase,
            "cursor": cache.cursor,
            "total_rows": total_rows,
            "row_width": cache.row_width,
            "row_bytes": cache.row_bytes,
            "global_order": order,
            "producer_sha256": pins.get("producer_sha256"),
            "launch_manifest_sha256": pins.get("launch_manifest_sha256"),
            "launch_input_identity": pins.get("launch_input_identity"),
            "cache": {
                "path": cache.path.name, "rows": cache.cursor,
                "bytes": cache_bytes,
                "sha256": cache.digest.hexdigest(), "eof": True,
            },
            "instruction": {
                "path": instructions.path.name, "rows": instructions.rows,
                "bytes": instruction_bytes,
                "sha256": instructions.digest.hexdigest(),
                "final_lf": final_lf, "eof": True,
                "final_head": head,
            },
            "ancestry_sha256": head,
            "pins": pins,
            "claim_flags": dict(FALSE_CLAIMS),
            **FALSE_CLAIMS,
        }
        path = Path(checkpoint_path).absolute()
        require(path.name == "checkpoint.json", "checkpoint_filename")
        require(path.parent.exists() and path.parent.is_dir(),
                "checkpoint_parent")
        temporary = path.with_name(".checkpoint.json.tmp")
        raw = canonical(payload)
        with temporary.open("wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    print(json.dumps({
        "cursor": cache.cursor, "phase": phase,
        "elapsed_seconds": time.monotonic() - started,
        "durable_bytes": cache_bytes + instruction_bytes,
        "rss_bytes": rss,
        **({"status": CHECKPOINT_STATUS} if payload is not None else {}),
    }, sort_keys=True, separators=(",", ":")), flush=True)
    return payload


def instruction_receipt(path: Path, expected_rows: int,
                        expected_row_bytes: int = ROW_BYTES,
                        expected_row_hashes: list[str] | None = None,
                        expected_head: str | None = None,
                        expected_stream_digest: str | None = None) -> dict[str, Any]:
    require(plain_int(expected_rows) and expected_rows >= 0,
            "instruction_expected_rows")
    if expected_row_hashes is not None:
        require(len(expected_row_hashes) == expected_rows,
                "instruction_expected_hash_count")
    digest = hashlib.sha256()
    total_bytes = 0
    rows = 0
    predecessor = b"\0" * 32
    final_head = predecessor.hex()
    with path.open("rb") as stream:
        for line in stream:
            require(line.endswith(b"\n"), "instruction_final_lf")
            digest.update(line)
            total_bytes += len(line)
            require(rows < expected_rows, "instruction_row_overflow")
            try:
                value = json.loads(line[:-1].decode("ascii"))
            except (ValueError, UnicodeError) as exc:
                raise RuntimeError("instruction_json") from exc
            require(isinstance(value, dict)
                    and canonical(value) == line, "instruction_line_canonical")
            require(value.get("node") == rows, "instruction_node_sequence")
            require(value.get("offset") == rows * expected_row_bytes
                    and value.get("length") == expected_row_bytes,
                    "instruction_row_position")
            receipt = value.get("row_receipt")
            require(isinstance(receipt, dict) and set(receipt) == {
                "offset", "length", "sha256"
            } and receipt["offset"] == value["offset"]
                    and receipt["length"] == value["length"],
                    "instruction_row_receipt")
            digest_string(receipt["sha256"], "instruction_row_digest")
            if expected_row_hashes is not None:
                require(receipt["sha256"] == expected_row_hashes[rows],
                        "instruction_row_hash_link")
            predecessor_hex = value.get("predecessor")
            require(predecessor_hex == predecessor.hex(),
                    "instruction_predecessor")
            ancestry = value.get("ancestry_sha256")
            digest_string(ancestry, "instruction_ancestry_digest")
            unsigned = dict(value)
            del unsigned["ancestry_sha256"]
            expected_ancestry = sha(predecessor + canonical(unsigned))
            require(ancestry == expected_ancestry, "instruction_ancestry")
            predecessor = bytes.fromhex(ancestry)
            final_head = ancestry
            rows += 1
    require(rows == expected_rows
            and (expected_rows == 0 or total_bytes > 0) and final_head,
            "instruction_final_lf_or_rows")
    stream_digest = digest.hexdigest()
    if expected_head is not None:
        require(expected_head == final_head, "instruction_final_head")
    if expected_stream_digest is not None:
        require(expected_stream_digest == stream_digest,
                "instruction_stream_digest")
    return {"bytes": total_bytes, "rows": rows, "sha256": stream_digest,
            "final_lf": True, "eof": True, "final_head": final_head}


def _checkpoint_phase(total_rows: int, cursor: int,
                      global_order: list[int] | tuple[int, ...]) -> str:
    """Return the frozen stream phase for a cursor (used by production)."""
    require(plain_int(total_rows) and plain_int(cursor)
            and 0 <= cursor <= total_rows, "checkpoint_cursor")
    if total_rows == ROWS and tuple(global_order) == tuple(ORDER):
        if cursor == 0:
            return "startup"
        return "old" if cursor < ORDER[4] else "new"
    return "startup" if cursor == 0 else "prefix"


def _safe_prefix_roster(staging: Path, checkpoint_path: Path) -> None:
    """Authenticate the exact files allowed in a checkpoint staging root."""
    info = staging.lstat()
    require(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode)
            and not is_reparse(info), "unsafe_staging")
    expected = set(CHECKPOINT_FILES)
    try:
        same_root = checkpoint_path.resolve(strict=False).parent == \
            staging.resolve(strict=True)
    except OSError as exc:
        raise RuntimeError("checkpoint_staging_path") from exc
    if same_root:
        expected.add(checkpoint_path.name)
    entries = list(staging.iterdir())
    require({entry.name for entry in entries} == expected,
            "checkpoint_roster")
    for entry in entries:
        regular(entry)
    regular(checkpoint_path)


def _scan_cache_prefix(path: Path, cursor: int, row_bytes: int
                       ) -> tuple[hashlib._Hash, list[str]]:
    require(plain_int(cursor) and cursor >= 0 and plain_int(row_bytes)
            and row_bytes > 0, "resume_cache_shape")
    digest = hashlib.sha256()
    row_hashes: list[str] = []
    with path.open("rb") as stream:
        for _ in range(cursor):
            raw = stream.read(row_bytes)
            require(len(raw) == row_bytes, "resume_cache_truncated")
            digest.update(raw)
            row_hashes.append(sha(raw))
        require(stream.read(1) == b"", "resume_cache_extension")
    return digest, row_hashes


def _scan_instruction_prefix(path: Path, cursor: int, row_bytes: int,
                             row_hashes: list[str], expected_bytes: int,
                             expected_digest: str,
                             expected_head: str
                             ) -> tuple[hashlib._Hash, str]:
    require(plain_int(cursor) and cursor >= 0 and len(row_hashes) == cursor,
            "resume_instruction_shape")
    digest = hashlib.sha256()
    predecessor = b"\0" * 32
    rows = 0
    total_bytes = 0
    with path.open("rb") as stream:
        for line in stream:
            require(line.endswith(b"\n"), "resume_instruction_final_lf")
            digest.update(line)
            total_bytes += len(line)
            require(rows < cursor, "resume_instruction_extension")
            try:
                value = json.loads(line[:-1].decode("ascii"))
            except (ValueError, UnicodeError) as exc:
                raise RuntimeError("resume_instruction_json") from exc
            require(isinstance(value, dict) and canonical(value) == line,
                    "resume_instruction_canonical")
            require(value.get("node") == rows,
                    "resume_instruction_node_sequence")
            offset = rows * row_bytes
            require(value.get("offset") == offset
                    and value.get("length") == row_bytes,
                    "resume_instruction_position")
            receipt = value.get("row_receipt")
            require(isinstance(receipt, dict) and set(receipt) == {
                "offset", "length", "sha256"
            } and receipt["offset"] == offset
                    and receipt["length"] == row_bytes,
                    "resume_instruction_row_receipt")
            digest_string(receipt["sha256"],
                          "resume_instruction_row_digest")
            require(receipt["sha256"] == row_hashes[rows],
                    "resume_instruction_row_hash_link")
            predecessor_hex = value.get("predecessor")
            require(predecessor_hex == predecessor.hex(),
                    "resume_instruction_predecessor")
            ancestry = value.get("ancestry_sha256")
            digest_string(ancestry, "resume_instruction_ancestry_digest")
            unsigned = dict(value)
            del unsigned["ancestry_sha256"]
            expected_ancestry = sha(predecessor + canonical(unsigned))
            require(ancestry == expected_ancestry,
                    "resume_instruction_ancestry")
            predecessor = bytes.fromhex(ancestry)
            rows += 1
    require(rows == cursor and total_bytes == expected_bytes,
            "resume_instruction_count")
    actual_digest = digest.hexdigest()
    require(actual_digest == expected_digest, "resume_instruction_digest")
    actual_head = predecessor.hex()
    require(actual_head == expected_head, "resume_instruction_final_head")
    return digest, actual_head


def validate_prefix_checkpoint(value: Any, pins: dict[str, Any],
                               total_rows: int = ROWS,
                               row_width: int = D2_WIDTH,
                               row_bytes: int = ROW_BYTES,
                               global_order: list[int] | tuple[int, ...] = ORDER
                               ) -> None:
    """Validate the sidecar ABI before any resume append is opened."""
    expected_keys = {
        "schema", "status", "phase", "cursor", "total_rows", "row_width",
        "row_bytes", "global_order", "producer_sha256",
        "launch_manifest_sha256", "launch_input_identity", "cache", "instruction",
        "ancestry_sha256", "pins", "claim_flags", *FALSE_CLAIMS,
    }
    require(isinstance(value, dict) and set(value) == expected_keys,
            "checkpoint_keys")
    require(value["schema"] == CHECKPOINT_SCHEMA
            and value["status"] == CHECKPOINT_STATUS,
            "checkpoint_schema_status")
    require(value["total_rows"] == total_rows
            and value["row_width"] == row_width
            and value["row_bytes"] == row_bytes
            and value["global_order"] == list(global_order),
            "checkpoint_frozen_shape")
    cursor = value["cursor"]
    require(plain_int(cursor) and 0 <= cursor <= total_rows,
            "checkpoint_cursor_range")
    # Every row boundary is legal.  The four old and four new phase changes
    # remain frozen by the global order and are checked explicitly for the
    # production stream.
    require(cursor in range(total_rows + 1), "checkpoint_cursor_boundary")
    phase = value["phase"]
    require(phase == _checkpoint_phase(total_rows, cursor, global_order)
            or (total_rows != ROWS and isinstance(phase, str)
                and phase in {"startup", "prefix", "old", "new"}),
            "checkpoint_phase")
    require(value["pins"] == pins, "checkpoint_pins")
    require(value["producer_sha256"] == pins.get("producer_sha256")
            and value["launch_manifest_sha256"] ==
                pins.get("launch_manifest_sha256")
            and value["launch_input_identity"] ==
                pins.get("launch_input_identity"),
            "checkpoint_launch_identity")
    flags = value["claim_flags"]
    require(flags == FALSE_CLAIMS
            and all(value[key] is False for key in FALSE_CLAIMS),
            "checkpoint_claim_flags")
    cache_value = value["cache"]
    require(isinstance(cache_value, dict) and set(cache_value) == {
        "path", "rows", "bytes", "sha256", "eof"
    } and cache_value["path"] == CHECKPOINT_FILES[0]
            and cache_value["rows"] == cursor
            and cache_value["bytes"] == cursor * row_bytes
            and cache_value["eof"] is True,
            "checkpoint_cache_receipt")
    digest_string(cache_value["sha256"], "checkpoint_cache_digest")
    instruction_value = value["instruction"]
    require(isinstance(instruction_value, dict)
            and set(instruction_value) == {
                "path", "rows", "bytes", "sha256", "final_lf", "eof",
                "final_head"
            } and instruction_value["path"] == CHECKPOINT_FILES[1]
            and instruction_value["rows"] == cursor
            and plain_int(instruction_value["bytes"])
            and instruction_value["bytes"] >= 0
            and instruction_value["eof"] is True
            and instruction_value["final_lf"] is True,
            "checkpoint_instruction_receipt")
    digest_string(instruction_value["sha256"],
                  "checkpoint_instruction_digest")
    digest_string(instruction_value["final_head"],
                  "checkpoint_instruction_head")
    require(value["ancestry_sha256"] == instruction_value["final_head"],
            "checkpoint_ancestry_link")


def resume_prefix(staging: Path, checkpoint_path: Path, pins: dict[str, Any],
                  total_rows: int = ROWS, row_width: int = D2_WIDTH,
                  row_bytes: int = ROW_BYTES,
                  global_order: list[int] | tuple[int, ...] = ORDER
                  ) -> tuple[PackedCache, InstructionSink, int, str, dict[str, Any]]:
    """Authenticate and reopen a retained prefix without recomputing rows."""
    staging = Path(staging).absolute()
    checkpoint_path = Path(checkpoint_path).absolute()
    _safe_prefix_roster(staging, checkpoint_path)
    checkpoint_value, _ = canonical_file(checkpoint_path)
    validate_prefix_checkpoint(checkpoint_value, pins, total_rows, row_width,
                               row_bytes, global_order)
    cursor = checkpoint_value["cursor"]
    cache_value = checkpoint_value["cache"]
    instruction_value = checkpoint_value["instruction"]
    cache_path = staging / CHECKPOINT_FILES[0]
    instruction_path = staging / CHECKPOINT_FILES[1]
    cache_info = regular(cache_path)
    instruction_info = regular(instruction_path)
    cache_identity = stable_identity(cache_info)
    instruction_identity = stable_identity(instruction_info)
    require(cache_info.st_size == cache_value["bytes"]
            and instruction_info.st_size == instruction_value["bytes"],
            "resume_prefix_size")
    cache_digest, row_hashes = _scan_cache_prefix(cache_path, cursor, row_bytes)
    require(stable_identity(regular(cache_path)) == cache_identity,
            "resume_cache_changed_during_scan")
    require(cache_digest.hexdigest() == cache_value["sha256"],
            "resume_cache_digest")
    instruction_digest, head = _scan_instruction_prefix(
        instruction_path, cursor, row_bytes, row_hashes,
        instruction_value["bytes"], instruction_value["sha256"],
        instruction_value["final_head"])
    require(stable_identity(regular(instruction_path)) == instruction_identity,
            "resume_instruction_changed_during_scan")
    cache = PackedCache.from_resume(cache_path, row_width, cursor,
                                    cache_digest, row_hashes)
    instructions = InstructionSink.from_resume(
        instruction_path, cursor, instruction_value["bytes"],
        instruction_digest, head)
    return cache, instructions, cursor, head, checkpoint_value


def expected_p1(p2: Any, p1store: "LazyP1", work: tuple[np.ndarray, ...],
                index: int) -> None:
    actual = flatten_p1(p2, work)
    expected = p1store.row(index)
    require(actual.ndim == expected.ndim == 1
            and actual.size == expected.size
            and actual.tobytes() == expected.tobytes(),
            "complete_p1_truncation")


def recurse_node(p2: Any, cache: PackedCache, p1store: "LazyP1",
                 global_id: int, local_id: int, local_rank: int,
                 node: dict[str, Any], raw: tuple[np.ndarray, ...],
                 origin_kinds: set[str], origin_count: int | None = None
                 ) -> tuple[np.ndarray, ...]:
    validate_node(node, local_id, local_rank,
                  6056 if local_rank <= 505 else SOURCE_BLOCK,
                  origin_kinds, origin_count)
    work = tuple(np.asarray(part, dtype=np.uint8).copy() for part in raw)
    base = global_id - local_id
    for prior, coefficient in node["reductions"]:
        add_full(p2, work, full_from(cache, p2, p1store, base + prior),
                 -coefficient)
    work = scale_full(work, node["scale"])
    expected_p1(p2, p1store, work, global_id)
    return work


def projected_seed(p2: Any, context: Any, words: dict[str, Any],
                   seed: int, label: tuple[int, int]) -> tuple[np.ndarray, ...]:
    require(plain_int(seed) and 1 <= seed <= 44, "seed_index")
    literal = tuple(int(x) for x in words["relators"][seed - 1])
    base = p2.evaluate_seed_precision2(context, literal)
    return p2.project_full_by_words(context, base, label)


def compile_packet_v486(p2: Any, context: Any,
                        full_old_defect: tuple[np.ndarray, ...],
                        label: tuple[int, int],
                        expected_packet: np.ndarray) -> tuple[np.ndarray, ...]:
    """Apply full filtered P_lambda before the exact P1 packet gate."""
    require(len(full_old_defect) == 4, "packet_full_shape")
    require(not np.any(full_old_defect[0]) and not np.any(full_old_defect[3]),
            "packet_p0_aux")
    require(np.any(full_old_defect[1]), "packet_requires_nonzero_p1")
    work = p2.project_full_by_words(context, full_old_defect, label)
    selected = p2.CHARACTER_LABELS.index(label)
    require(not np.any(work[0]) and not np.any(work[3]),
            "packet_project_lower")
    require(all(not np.any(work[1][index])
                for index in range(4) if index != selected),
            "packet_character_leak")
    actual = p2.grade1.pack_trits(work[1][selected]).tobytes()
    expected = p2.grade1.pack_trits(np.asarray(expected_packet,
                                                dtype=np.uint8)).tobytes()
    require(actual == expected, "packet_exact_bytes")
    return work


def compile_old_defect(p2: Any, context: Any, words: dict[str, Any],
                       origin: dict[str, Any],
                       cache: PackedCache, p1store: "LazyP1",
                       prepare: dict[str, Any], old_offsets: list[int]
                       ) -> tuple[tuple[np.ndarray, ...], dict[str, Any]]:
    character = origin["lower_character"]
    old = prepare["old_blocks"][character]
    parent_digests: list[str] = []
    if origin["kind"] == "seed":
        work = projected_seed(p2, context, words, origin["seed"],
                              CHARACTERS[character])
        expression = old["record"]["seed_reductions"][origin["seed"] - 1]
        literal = {"kind": "seed", "seed": origin["seed"],
                   "word": words["relators"][origin["seed"] - 1],
                   "character": list(CHARACTERS[character])}
    elif origin["kind"] == "transition":
        parent_index = old_offsets[character] + origin["pivot"]
        parent = full_from(cache, p2, p1store, parent_index)
        parent_digests.append(cache.row_sha(parent_index))
        work = p2.act_source_word_precision2(
            context, parent, (origin["letter"],))
        expression = old["record"]["actor_transitions"][origin["pivot"]][
            ACTORS.index(origin["letter"])]
        literal = {"kind": "transition", "pivot": origin["pivot"],
                   "letter": origin["letter"],
                   "character": list(CHARACTERS[character])}
    else:
        raise RuntimeError("packet_old_origin_kind")
    for local, coefficient in expression:
        prior = full_from(cache, p2, p1store, old_offsets[character] + local)
        parent_digests.append(cache.row_sha(old_offsets[character] + local))
        add_full(p2, work, prior, -coefficient)
    require(not np.any(work[0]) and not np.any(work[3]),
            "old_defect_p0_aux")
    require(np.any(work[1]), "old_defect_requires_nonzero_p1")
    return work, {"literal_input_sha256": sha(canonical(literal)),
                   "parent_row_sha256": parent_digests}


def validate_checker_phase(value: Any, phase: str, index: int | None) -> None:
    prepare_keys = {
        "schema", "phase", "producer_sha256", "source_run", "source_attempt",
        "source_head", "prepare_body_sha256", "input_manifest_sha256", "counts",
        "equality_receipts", "equality_receipts_sha256", "projector_identity",
        "checker_digests", "downstream_claim_flags", "resident_global_matrix",
        "independent_checker", "precision2", "A0", "COMMON", "COMPATIBLE_LIFT",
        "FAKE", "IHARA", "verified", "elapsed_seconds", "peak_rss_bytes",
    }
    block_keys = {
        "schema", "phase", "producer_sha256", "source_run", "source_attempt",
        "source_head", "prepare_body_sha256", "block_index", "block_body_sha256",
        "basis_sha256", "counts", "rank", "attempts", "dag_sha256",
        "checker_digests", "downstream_claim_flags", "resident_global_matrix",
        "independent_checker", "precision2", "A0", "COMMON", "COMPATIBLE_LIFT",
        "FAKE", "IHARA", "verified", "elapsed_seconds", "peak_rss_bytes",
    }
    required_keys = prepare_keys if index is None else block_keys
    require(isinstance(value, dict) and set(value) == required_keys,
            "checker_nested_keys")
    require(value["schema"] ==
            f"d972.r07.p1.componentwise.{phase}.v1"
            and value["phase"] == phase
            and value["producer_sha256"] == SEM_SHA
            and value["source_run"] == SOURCE_RUN
            and value["source_attempt"] == SOURCE_ATTEMPT
            and value["source_head"] == SOURCE_HEAD
            and value["prepare_body_sha256"] == PREPARE_DIGEST,
            "checker_nested_ancestry")
    require(value["independent_checker"] is True,
            "checker_nested_marker")
    require(value["downstream_claim_flags"] == CHECKER_FLAGS,
            "checker_nested_flags")
    for key in ("resident_global_matrix", "precision2", "A0", "COMMON",
                "COMPATIBLE_LIFT", "FAKE", "IHARA", "verified"):
        require(value[key] is False, "checker_nested_flag:" + key)
    finite_telemetry(value["elapsed_seconds"], "checker_nested_elapsed")
    peak = value["peak_rss_bytes"]
    require(peak is None or (plain_int(peak) and peak >= 0),
            "checker_nested_peak")
    if index is None:
        require(value["counts"] == {
            "old_ranks": 2014, "old_dag_nodes": 2014,
            "old_seed_lower": 176, "old_actor_lower": 8056,
            "direct_packet_halves": 32928,
        }, "checker_prepare_counts")
        digest_string(value["input_manifest_sha256"],
                      "checker_prepare_manifest_digest")
        equality = value["equality_receipts"]
        require(isinstance(equality, list) and len(equality) == 4,
                "checker_prepare_equality_shape")
        for position, record in enumerate(equality):
            require(isinstance(record, dict) and set(record) == {
                "character_index", "record_sha256", "lower_sha256",
                "lifted_sha256"
            } and plain_int(record["character_index"])
                    and record["character_index"] == position,
                    "checker_prepare_equality_record")
            for field in ("record_sha256", "lower_sha256", "lifted_sha256"):
                digest_string(record[field], "checker_prepare_equality_digest")
        require(value["equality_receipts_sha256"] == sha(canonical(equality)),
                "checker_prepare_equality_link")
        projector = value["projector_identity"]
        require(isinstance(projector, dict) and set(projector) == {
            "sum_chi_P_chi_mod3", "seed_reconstruction_count", "cv_sum_table",
            "cv_sum_table_sha256", "pure_words_sha256"
        } and projector["sum_chi_P_chi_mod3"] == 1
                and projector["seed_reconstruction_count"] == 44
                and projector["cv_sum_table"] == [1, 0, 0, 0]
                and projector["cv_sum_table_sha256"] ==
                    sha(canonical(projector["cv_sum_table"])),
                "checker_prepare_projector")
        digest_string(projector["pure_words_sha256"],
                      "checker_prepare_words_digest")
        digest = value["checker_digests"]
        require(isinstance(digest, dict) and set(digest) == {
            "prepare_body_sha256", "equality_receipts_sha256",
            "packet_component_sha256", "projector_full_sha256"
        }, "checker_prepare_digest_keys")
        require(digest["prepare_body_sha256"] == PREPARE_DIGEST
                and digest["equality_receipts_sha256"] ==
                    value["equality_receipts_sha256"],
                "checker_prepare_digest_link")
        digest_string(digest["packet_component_sha256"],
                      "checker_prepare_packet_digest")
        digest_string(digest["projector_full_sha256"],
                      "checker_prepare_projector_digest")
    else:
        require(plain_int(value["block_index"]) and value["block_index"] == index
                and value["block_body_sha256"] == PARENTS[index]
                and value["basis_sha256"] == BASIS[index]
                and plain_int(value["rank"]) and value["rank"] == NEW_RANKS[index]
                and plain_int(value["attempts"])
                and value["attempts"] == 8232 + 4 * NEW_RANKS[index],
                "checker_block_metadata")
        require(value["counts"] == {
            "packet_basis_halves": 8232,
            "new_actor_identities": 4 * NEW_RANKS[index],
            "new_dag_identities": NEW_RANKS[index],
            "compound_obligations": 8232 + 4 * NEW_RANKS[index],
        }, "checker_block_counts")
        digest_string(value["dag_sha256"], "checker_block_dag_digest")
        digest = value["checker_digests"]
        require(isinstance(digest, dict) and set(digest) == {
            "block_body_sha256", "basis_sha256", "origin_reductions_sha256",
            "actor_transitions_sha256", "dag_sha256"
        }, "checker_block_digest_keys")
        require(digest["block_body_sha256"] == value["block_body_sha256"]
                and digest["basis_sha256"] == value["basis_sha256"]
                and digest["dag_sha256"] == value["dag_sha256"],
                "checker_block_digest_link")
        for field in ("origin_reductions_sha256", "actor_transitions_sha256"):
            digest_string(digest[field], "checker_block_digest")


CHECKER_RESULT_KEYS = {
    "schema", "terminal", "marker", "source_run", "source_attempt",
    "source_head", "prepare_body_sha256", "old_ranks", "new_ranks",
    "dag_nodes", "global_relations", "old_local_relations",
    "direct_packet_halves", "packet_basis_halves", "new_actor_identities",
    "compound_obligations", "prepare", "blocks", "producer_receipt_sha256",
    "producer_sha256", "checker_digests", "resident_global_matrix",
    "independent_checker", "precision2", "A0", "COMMON", "COMPATIBLE_LIFT",
    "FAKE", "IHARA", "verified", "elapsed_seconds", "peak_rss_bytes",
}


def validate_checker_result(result: Any, checker: Any,
                            receipt_digests: list[str],
                            expected_manifest: str) -> None:
    require(isinstance(result, dict) and set(result) == CHECKER_RESULT_KEYS,
            "checker_result_keys")
    require(result["schema"] == checker.CHECKER_SCHEMA
            and result["terminal"] ==
            "TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED_INDEPENDENTLY"
            and result["marker"] == checker.MARKER,
            "checker_marker_terminal")
    require(result["source_run"] == SOURCE_RUN
            and result["source_attempt"] == SOURCE_ATTEMPT
            and result["source_head"] == SOURCE_HEAD
            and result["prepare_body_sha256"] == PREPARE_DIGEST,
            "checker_source_ancestry")
    expected_counts = {
        "old_ranks": 2014, "new_ranks": 6045, "dag_nodes": 8059,
        "global_relations": 32280, "old_local_relations": 8232,
        "direct_packet_halves": 32928, "packet_basis_halves": 32928,
        "new_actor_identities": 24180, "compound_obligations": 65340,
    }
    for key, wanted in expected_counts.items():
        require(plain_int(result[key]) and result[key] == wanted,
                "checker_count:" + key)
    require(result["producer_sha256"] == SEM_SHA,
            "checker_producer_sha")
    expected_receipts = launch_expected_receipts(receipt_digests)
    require(result["producer_receipt_sha256"] == expected_receipts,
            "checker_receipt_digests")
    validate_checker_phase(result["prepare"], "prepare", None)
    require(result["prepare"]["input_manifest_sha256"] == expected_manifest,
            "checker_prepare_manifest_link")
    require(isinstance(result["blocks"], list) and len(result["blocks"]) == 4,
            "checker_blocks_shape")
    for index, block in enumerate(result["blocks"]):
        validate_checker_phase(block, "block", index)
    digests = result["checker_digests"]
    require(isinstance(digests, dict) and set(digests) == {
        "prepare", "blocks", "producer_receipts", "semantic_family_sha256"
    }, "checker_digest_keys")
    require(digests["producer_receipts"] == expected_receipts,
            "checker_nested_receipt_digests")
    require(digests["prepare"] == result["prepare"]["checker_digests"],
            "checker_prepare_digest_unlinked")
    require(isinstance(digests["blocks"], list) and len(digests["blocks"]) == 4
            and digests["blocks"] ==
                [value["checker_digests"] for value in result["blocks"]],
            "checker_digest_shape")
    semantic_family = sha(canonical({
        "prepare": result["prepare"]["counts"],
        "equality": result["prepare"]["equality_receipts"],
        "blocks": [value["counts"] for value in result["blocks"]],
        "projector": result["prepare"]["projector_identity"],
    }))
    require(digests["semantic_family_sha256"] == semantic_family,
            "checker_semantic_family")
    for key in ("resident_global_matrix", "precision2", "A0", "COMMON",
                "COMPATIBLE_LIFT", "FAKE", "IHARA", "verified"):
        require(result[key] is False, "checker_flag:" + key)
    require(result["independent_checker"] is True, "checker_independent")
    finite_telemetry(result["elapsed_seconds"], "checker_elapsed")
    require(plain_int(result["peak_rss_bytes"]) and result["peak_rss_bytes"] >= 0,
            "checker_peak")


def authenticate_inputs(args: argparse.Namespace) -> dict[str, Any]:
    deps = load_dependencies()
    g1, p2, sem = deps["g1"], deps["p2"], deps["sem"]
    checker, structural = deps["checker"], deps["structural"]
    require(tuple(g1.ACTORS) == ACTORS and tuple(p2.ACTORS) == ACTORS
            and tuple(sem.ACTORS) == ACTORS and tuple(checker.ACTORS) == ACTORS,
            "actor_order_module_pin")
    receipt_paths = [Path(value).absolute()
                     for value in args.semantic_receipts]
    receipt_values: list[dict[str, Any]] = []
    receipt_raws: list[bytes] = []
    for path in receipt_paths:
        value, raw = canonical_file(path)
        require(isinstance(value, dict), "receipt_object")
        receipt_values.append(value)
        receipt_raws.append(raw)
    receipt_digests = [sha(raw) for raw in receipt_raws]
    checker_path = Path(args.semantic_checker_result).absolute()
    checker_result, checker_raw = canonical_file(checker_path)
    checker_result_sha = sha(checker_raw)
    require(checker_result_sha == CHECKER_RESULT_SHA,
            "checker_result_actual_sha256")
    checker_workflow_path = Path(
        args.semantic_checker_workflow_receipt).absolute()
    checker_workflow_receipt, checker_workflow_raw = canonical_file(
        checker_workflow_path)
    checker_workflow_sha = sha(checker_workflow_raw)
    require(checker_workflow_sha == CHECKER_WORKFLOW_RECEIPT_SHA,
            "checker_workflow_actual_sha256")
    validate_checker_workflow_receipt(
        checker_workflow_receipt, checker_result, checker_result_sha,
        receipt_digests)
    launch_path = Path(args.launch_manifest).absolute()
    launch, launch_raw = canonical_file(launch_path)
    producer_sha = file_sha(Path(__file__).resolve())
    # v5's exact phase and terminal schema is the sole producer receipt gate.
    prepare_value, block_values = receipt_values[0], receipt_values[1:5]
    sem.validate_prepare_receipt(prepare_value, SEM_SHA)
    require(len(block_values) == 4, "semantic_block_receipt_count")
    for index, value in enumerate(block_values):
        sem.validate_block_receipt(value, index, SEM_SHA)
    sem.validate_join_receipts(prepare_value, block_values)

    # Authenticate the five raw roots before allocating the candidate cache.
    prepare, prepare_raw, input_manifest = sem.authenticated_prepare(
        g1, Path(args.prepare_root))
    prepare_size = nonnegative_size(len(prepare_raw), "prepare_body_size")
    del prepare_raw
    prep_safe = Path(args.prepare_root).resolve(strict=True)
    blocks: list[dict[str, Any]] = []
    block_roots: list[Path] = []
    block_sizes: list[int] = []
    for index, root_arg in enumerate(args.block_roots):
        safe, body, body_size = sem.block_envelope(
            Path(root_arg), index, prepare, g1, structural)
        body_size = nonnegative_size(body_size, "block_body_size")
        blocks.append(body)
        block_roots.append(safe)
        block_sizes.append(body_size)
    require(len(block_sizes) == 4, "block_body_size_count")
    validate_authenticated_dag(prepare, blocks)

    # v5's join logic is executed, and the sixth receipt is compared with its
    # exact canonical terminal object rather than with a filename or count.
    expected_join = sem.join(receipt_paths[:5])
    require(receipt_values[5] == expected_join
            and receipt_raws[5] == canonical(expected_join),
            "semantic_terminal_join")
    expected_manifest = sha(canonical(input_manifest))
    checker.validate_producer_chain(prepare_value, block_values,
                                    receipt_values[5], SEM_SHA,
                                    expected_manifest)
    validate_checker_result(checker_result, checker, receipt_digests,
                            expected_manifest)

    registry = FileRegistry()
    registry.add(WORDS_PATH, WORDS_SHA, "words")
    registry.add(prep_safe / "prepare.HEAD",
                 sha((prep_safe / "prepare.HEAD").read_bytes()), "sealed-head")
    registry.add(prep_safe / f"prepare.{PREPARE_DIGEST}.json",
                 PREPARE_DIGEST, "sealed-body")
    for old in prepare["old_blocks"]:
        for key in ("lower_basis_blob", "lifted_grade_blob"):
            register_blob(registry, prep_safe, old[key], "prepare-blob")
    for packet in prepare["packets"]:
        register_blob(registry, prep_safe, packet["blob"], "prepare-packet")
    register_blob(registry, prep_safe, prepare["residual_blob"], "prepare-residual")
    raw_artifacts = [artifact_entry(
        prep_safe, "prepare", "prepare", PREPARE_DIGEST, prepare_size)]
    for index, (root, body, body_size) in enumerate(
            zip(block_roots, blocks, block_sizes)):
        digest = PARENTS[index]
        registry.add(root / f"block-{index}.HEAD",
                     sha((root / f"block-{index}.HEAD").read_bytes()),
                     "sealed-head")
        registry.add(root / f"block-{index}.{digest}.json",
                     digest, "sealed-body")
        register_blob(registry, root, body["basis_blob"], "block-basis")
        raw_artifacts.append(artifact_entry(
            root, f"block-{index}", f"block-{index}", digest, body_size))
    for path, digest, kind in zip(receipt_paths, receipt_digests,
                                  ("semantic-receipt",) * 6):
        registry.add(path, digest, kind)
    registry.add(checker_path, checker_result_sha, "checker-result")
    registry.add(checker_workflow_path, checker_workflow_sha,
                 "checker-workflow-receipt")
    registry.add(launch_path, sha(launch_raw), "launch-manifest")
    validate_launch_manifest(launch, producer_sha, receipt_digests,
                             checker_result_sha, checker_workflow_sha,
                             raw_artifacts)
    return {
        "deps": deps, "g1": g1, "p2": p2, "sem": sem,
        "checker": checker, "prepare": prepare, "prepare_safe": prep_safe,
        "blocks": blocks, "block_roots": block_roots,
        "p1_auth": input_manifest, "receipt_digests": receipt_digests,
        "checker_result_sha256": checker_result_sha,
        "checker_result": checker_result, "launch": launch,
        "checker_workflow_receipt_sha256": checker_workflow_sha,
        "checker_workflow_receipt": checker_workflow_receipt,
        "launch_sha256": sha(launch_raw), "raw_artifacts": raw_artifacts,
        "registry": registry, "producer_sha256": producer_sha,
        "block_sizes": block_sizes,
    }


class LazyP1:
    """Memmapped P1 rows; only the requested row is decoded."""

    def __init__(self, p2: Any, prepare: dict[str, Any], blocks: list[dict[str, Any]],
                 prep_root: Path, block_roots: list[Path]):
        self.p2 = p2
        self.old: list[tuple[np.ndarray, np.ndarray]] = []
        self.new: list[np.ndarray] = []
        for old in prepare["old_blocks"]:
            self.old.append((
                p2.load_grade1_packed_matrix(
                    prep_root, old["lower_basis_blob"]),
                p2.load_grade1_packed_matrix(
                    prep_root, old["lifted_grade_blob"]),
            ))
        for block, root in zip(blocks, block_roots):
            self.new.append(p2.load_grade1_packed_matrix(
                root, block["basis_blob"]))

    def row(self, index: int) -> np.ndarray:
        require(plain_int(index) and 0 <= index < ROWS, "p1_row_index")
        if index < ORDER[4]:
            character = max(i for i in range(4) if ORDER[i] <= index)
            pivot = index - ORDER[character]
            lower = self.p2.grade1.unpack_trits(
                self.old[character][0][pivot],
                self.p2.grade1.LOWER_ECHELON_WIDTH)
            lift = self.p2.grade1.unpack_trits(
                self.old[character][1][pivot],
                self.p2.SOURCE_DEGREE1_WIDTH).reshape(
                    4, self.p2.SOURCE_DEGREE1_PER_CHARACTER)
            degree0 = np.zeros((4, self.p2.SOURCE_DEGREE0_PER_CHARACTER),
                               dtype=np.uint8)
            degree0[character] = lower[:self.p2.SOURCE_DEGREE0_PER_CHARACTER]
            return self.p2.flatten_precision1(
                degree0, lift, lower[-8:])
        character = max(i for i in range(4) if ORDER[4 + i] <= index)
        pivot = index - ORDER[4 + character]
        one = self.p2.grade1.unpack_trits(
            self.new[character][pivot], self.p2.SOURCE_DEGREE1_PER_CHARACTER)
        degree0 = np.zeros((4, self.p2.SOURCE_DEGREE0_PER_CHARACTER),
                           dtype=np.uint8)
        degree1 = np.zeros((4, self.p2.SOURCE_DEGREE1_PER_CHARACTER),
                           dtype=np.uint8)
        degree1[character] = one
        return self.p2.flatten_precision1(
            degree0, degree1, np.zeros(8, dtype=np.uint8))

    def close(self) -> None:
        for matrix in [item for pair in self.old for item in pair] + self.new:
            handle = getattr(matrix, "_mmap", None)
            if handle is not None:
                try:
                    handle.close()
                except (BufferError, ValueError):
                    pass


def reduction_digests(cache: PackedCache,
                      base: int, reductions: list[list[int]]) -> list[str]:
    return [cache.row_sha(base + index) for index, _ in reductions]


def make_instruction(p2: Any, cache: PackedCache, p1store: LazyP1,
                     global_id: int, base: int, node: dict[str, Any],
                     origin: dict[str, Any], raw_origin: tuple[np.ndarray, ...],
                     work: tuple[np.ndarray, ...],
                     raw_meta: dict[str, Any], offset: int, row_sha: str,
                     predecessor: bytes) -> tuple[dict[str, Any], bytes]:
    raw_sha, components = raw_component_digest(p2, raw_origin)
    record: dict[str, Any] = {
        "node": global_id,
        "origin": origin,
        "reductions": [list(pair) for pair in node["reductions"]],
        "scale": node["scale"],
        "raw_origin_sha256": raw_sha,
        "raw_origin_components_sha256": components,
        "literal_input_sha256": raw_meta.get("literal_input_sha256"),
        "old_defect_literal_input_sha256": raw_meta.get(
            "old_defect_literal_input_sha256"),
        "parent_row_sha256": raw_meta.get("parent_row_sha256", []),
        "packet_sha256": raw_meta.get("packet_sha256"),
        "packet_row_sha256": raw_meta.get("packet_row_sha256"),
        "reduction_parent_sha256": reduction_digests(
            cache, base, node["reductions"]),
        "p1_sha256": sha(p2.grade1.pack_trits(flatten_p1(p2, work)).tobytes()),
        "offset": offset,
        "length": cache.row_bytes,
        "row_receipt": {"offset": offset, "length": cache.row_bytes,
                         "sha256": row_sha},
        "predecessor": predecessor.hex(),
    }
    encoded = canonical(record)
    ancestry = sha(predecessor + encoded)
    record["ancestry_sha256"] = ancestry
    return record, encoded


def _checkpoint_pins(boundary: dict[str, Any]) -> dict[str, Any]:
    """Stable semantic/input pins copied into every resumable sidecar."""
    launch = boundary["launch"]
    raw_artifacts = [
        {"role": entry["role"], "body_file": entry["body_file"],
         "body_sha256": entry["body_sha256"],
         "body_bytes": entry["body_bytes"]}
        for entry in boundary["raw_artifacts"]
    ]
    # The launch-manifest is a runner-local wrapper: its bytes contain
    # absolute roots and filesystem identities and therefore must not become
    # a resume pin.  The semantic launch identity below still binds every
    # immutable input through these normalized, path-independent records.
    raw_file_pins = sorted((
        {"kind": entry["kind"], "file": Path(entry["path"]).name,
         "bytes": entry["bytes"], "sha256": entry["sha256"]}
        for entry in boundary["registry"].entries()
        if entry["kind"] != "launch-manifest"
    ), key=lambda entry: (entry["kind"], entry["file"], entry["bytes"],
                          entry["sha256"]))
    launch_input_identity = {
        "schema": launch["schema"],
        "raw_artifacts": raw_artifacts,
        "raw_file_pins": raw_file_pins,
        "p1_input_manifest_sha256": sha(canonical(boundary["p1_auth"])),
        "receipt_hashes": launch["receipt_hashes"],
        "checker_result_sha256": launch["checker_result_sha256"],
        "checker_workflow_receipt_sha256":
            launch["checker_workflow_receipt_sha256"],
        "checker_success_artifact": launch["checker_success_artifact"],
        "source_run": launch["source_run"],
        "source_attempt": launch["source_attempt"],
        "source_head": launch["source_head"],
        "executable_hashes": launch["executable_hashes"],
        "import_hashes": launch["import_hashes"],
        "semantic_file_hashes": launch["semantic_file_hashes"],
    }
    return {
        "producer_sha256": boundary["producer_sha256"],
        # The launch file itself contains runner-local roots/inodes.  Bind the
        # canonical, path-independent input identity so a downloaded prefix
        # can resume on a new runner while still rejecting any input change.
        "launch_manifest_sha256": sha(canonical(launch_input_identity)),
        "launch_schema": launch["schema"],
        "source_run": SOURCE_RUN,
        "source_attempt": SOURCE_ATTEMPT,
        "source_head": SOURCE_HEAD,
        "receipt_hashes": launch_expected_receipts(
            boundary["receipt_digests"]),
        "checker_result_sha256": boundary["checker_result_sha256"],
        "checker_workflow_receipt_sha256":
            boundary["checker_workflow_receipt_sha256"],
        "checker_success_artifact": dict(CHECKER_SUCCESS_ARTIFACT),
        "semantic_file_hashes": dict(SEMANTIC_FILES),
        "import_hashes": dict(IMPORT_HASHES),
        "raw_artifacts": raw_artifacts,
        "raw_file_pins": raw_file_pins,
        "p1_input_manifest_sha256": sha(canonical(boundary["p1_auth"])),
        "prepare_body_sha256": PREPARE_DIGEST,
        "parents": list(PARENTS),
        "global_order": list(ORDER),
        "old_ranks": list(OLD_RANKS),
        "new_ranks": list(NEW_RANKS),
        "launch_input_identity": launch_input_identity,
    }


def _checkpoint_state(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "cursor": value["cursor"],
        "cache_bytes": value["cache"]["bytes"],
        "instruction_bytes": value["instruction"]["bytes"],
    }


def _rollback_prefix(cache: PackedCache, instructions: InstructionSink,
                     state: dict[str, Any]) -> None:
    """Remove rows written after the last authenticated sidecar boundary."""
    require(cache.stream.fileno() >= 0 and instructions.stream.fileno() >= 0,
            "rollback_stream")
    cache.stream.flush()
    instructions.stream.flush()
    os.ftruncate(cache.stream.fileno(), state["cache_bytes"])
    os.ftruncate(instructions.stream.fileno(), state["instruction_bytes"])
    os.fsync(cache.stream.fileno())
    os.fsync(instructions.stream.fileno())
    cache.stream.seek(state["cache_bytes"])
    instructions.stream.seek(state["instruction_bytes"])
    cache.cursor = state["cursor"]
    del cache.row_hashes[state["cursor"]:]


def _promotion_boundary(staging: Path, out: Path, checkpoint_path: Path,
                        manifest: dict[str, Any] | None = None,
                        terminal: BaseException | None = None,
                        cache: PackedCache | None = None,
                        instructions: InstructionSink | None = None,
                        last_checkpoint: dict[str, Any] | None = None) -> None:
    """Propagate a resource terminal or atomically promote one candidate."""
    if terminal is not None:
        require(manifest is None, "terminal_manifest_forbidden")
        if cache is not None and instructions is not None \
                and last_checkpoint is not None:
            try:
                _rollback_prefix(cache, instructions, last_checkpoint)
            except BaseException:
                pass
        # This branch deliberately reaches no checkpoint unlink, manifest
        # write, or output replace operation.
        raise terminal
    require(isinstance(manifest, dict), "promotion_manifest_required")
    if checkpoint_path.parent.resolve(strict=False) == staging.resolve(strict=True):
        require(checkpoint_path.name == "checkpoint.json", "checkpoint_filename")
        checkpoint_path.unlink()
    (staging / "manifest.json").write_bytes(canonical(manifest))
    os.replace(staging, out)


def build(args: argparse.Namespace) -> None:
    runtime_phase("build.authenticate_inputs")
    requested_out = Path(args.out).absolute()
    require(not os.path.lexists(requested_out), "fresh_output_required")
    out = requested_out.resolve()
    require(not out.exists(), "fresh_output_required")
    require(out != ROOT.resolve() and ROOT.resolve() not in out.parents,
            "output_external")
    staging = Path(args.staging).absolute()
    resume_arg = getattr(args, "resume_checkpoint", None)
    checkpoint_arg = getattr(args, "checkpoint", None)
    resume_requested = bool(getattr(args, "resume", False)) or \
        resume_arg is not None
    require(not resume_requested or resume_arg is not None,
            "resume_checkpoint_required")
    fresh = not resume_requested
    if fresh:
        require(not os.path.lexists(staging), "fresh_staging_required")
        staging.mkdir(parents=True)
        checkpoint_path = Path(checkpoint_arg).absolute()
        require(not os.path.lexists(checkpoint_path),
                "fresh_checkpoint_required")
    else:
        checkpoint_path = Path(checkpoint_arg or resume_arg).absolute()
        if checkpoint_path.is_dir():
            checkpoint_path /= "checkpoint.json"
        source_checkpoint = Path(resume_arg).absolute()
        if source_checkpoint.is_dir():
            source_checkpoint /= "checkpoint.json"
        require(checkpoint_path.resolve(strict=False) ==
                source_checkpoint.resolve(strict=False),
                "resume_checkpoint_identity")
        require(staging.exists() and staging.is_dir(),
                "resume_staging_required")
    require(checkpoint_path.name == "checkpoint.json",
            "checkpoint_filename")
    require(checkpoint_path.parent.exists()
            and checkpoint_path.parent.is_dir(), "checkpoint_parent")

    boundary = authenticate_inputs(args)
    deps = boundary["deps"]
    g1, p2 = boundary["g1"], boundary["p2"]
    runtime_phase("build.read_words")
    words, _ = read_words()
    runtime_phase("build.context")
    context = g1.Context(words)
    prepare = boundary["prepare"]
    blocks = boundary["blocks"]
    prep_root = boundary["prepare_safe"]
    block_roots = boundary["block_roots"]
    registry: FileRegistry = boundary["registry"]
    pins = _checkpoint_pins(boundary)
    runtime_phase("build.lazy_p1")
    p1store = LazyP1(p2, prepare, blocks, prep_root, block_roots)
    cache: PackedCache | None = None
    instructions: InstructionSink | None = None
    started = time.monotonic()
    rolling = b"\0" * 32
    last_checkpoint: dict[str, Any] | None = None
    resume_cursor = 0

    def durable_checkpoint(phase: str) -> None:
        nonlocal last_checkpoint
        require(cache is not None and instructions is not None,
                "checkpoint_stream_missing")
        value = checkpoint(cache, instructions, phase, started,
                           checkpoint_path=checkpoint_path, pins=pins,
                           global_order=ORDER, total_rows=ROWS)
        require(value is not None, "checkpoint_missing_payload")
        last_checkpoint = _checkpoint_state(value)

    old_offsets = ORDER[:4]
    try:
        if fresh:
            cache = PackedCache(staging / CHECKPOINT_FILES[0], D2_WIDTH)
            instructions = InstructionSink(staging / CHECKPOINT_FILES[1])
            # A cursor-zero sidecar makes a stop before the first interval
            # resumable as well, while remaining explicitly unchecked.
            durable_checkpoint("startup")
            enforce(started, "startup")
        else:
            cache, instructions, resume_cursor, rolling_hex, _ = resume_prefix(
                staging, checkpoint_path, pins, ROWS, D2_WIDTH, ROW_BYTES, ORDER)
            rolling = bytes.fromhex(rolling_hex)
            last_checkpoint = {
                "cursor": resume_cursor,
                "cache_bytes": resume_cursor * ROW_BYTES,
                "instruction_bytes": instructions.bytes,
            }
        # Old and new rows are evaluated in their authenticated global order.
        for character, old in enumerate(prepare["old_blocks"]):
            for pivot, node in enumerate(old["record"]["dag_nodes"]):
                global_id = old_offsets[character] + pivot
                if global_id < resume_cursor:
                    continue
                require(cache is not None and instructions is not None
                        and global_id == cache.cursor
                        and instructions.rows == cache.cursor,
                        "resume_old_cursor")
                runtime_phase(f"build.old[{character}].row[{pivot}]")
                origin = node["origin"]
                if origin["kind"] == "projected_seed":
                    raw = projected_seed(p2, context, words, origin["seed"],
                                         CHARACTERS[character])
                    raw_meta = {
                        "literal_input_sha256": sha(canonical({
                            "kind": "projected_seed", "seed": origin["seed"],
                            "word": words["relators"][origin["seed"] - 1],
                            "character": list(CHARACTERS[character]),
                        }))
                    }
                else:
                    parent_index = old_offsets[character] + origin["parent"]
                    parent = full_from(cache, p2, p1store, parent_index)
                    raw = p2.act_source_word_precision2(
                        context, parent, (origin["letter"],))
                    raw_meta = {
                        "literal_input_sha256": sha(canonical({
                            "kind": "actor", "letter": origin["letter"],
                            "actor_order": list(ACTORS),
                        })),
                        "parent_row_sha256": [full_row_digest(p2, parent)],
                    }
                work = recurse_node(
                    p2, cache, p1store, global_id, pivot, old["rank"], node,
                    raw, {"projected_seed", "actor"})
                offset, row_sha = cache.append(p2, work[2].reshape(-1))
                record, _ = make_instruction(
                    p2, cache, p1store, global_id, old_offsets[character],
                    node, origin, raw, work, raw_meta, offset, row_sha, rolling)
                rolling = bytes.fromhex(record["ancestry_sha256"])
                instructions.write(record)
                if cache.cursor % CHECKPOINT_INTERVAL == 0:
                    durable_checkpoint("old")
                    enforce(started, "old")
        for character, (block, root) in enumerate(zip(blocks, block_roots)):
            runtime_phase(f"build.new[{character}].packet_open")
            packet_receipt = prepare["packets"][character]["blob"]
            packet_path = prep_root / packet_receipt["file"]
            packet = np.memmap(packet_path, dtype=np.uint8, mode="r",
                               shape=(8232, SOURCE_BLOCK // 4))
            try:
                for pivot, node in enumerate(block["dag_nodes"]):
                    global_id = ORDER[4 + character] + pivot
                    if global_id < resume_cursor:
                        continue
                    require(cache is not None and instructions is not None
                            and global_id == cache.cursor
                            and instructions.rows == cache.cursor,
                            "resume_new_cursor")
                    runtime_phase(f"build.new[{character}].row[{pivot}]")
                    origin = node["origin"]
                    if origin["kind"] == "defect":
                        old_origin = prepare["defect_origins"][origin["origin"]]
                        defect, defect_meta = compile_old_defect(
                            p2, context, words, old_origin,
                            cache, p1store,
                            prepare, old_offsets)
                        expected = p2.grade1.unpack_trits(
                            packet[origin["origin"]], SOURCE_BLOCK)
                        raw = compile_packet_v486(
                            p2, context, defect, CHARACTERS[character], expected)
                        raw_meta = dict(defect_meta)
                        raw_meta["old_defect_literal_input_sha256"] = \
                            defect_meta["literal_input_sha256"]
                        raw_meta["literal_input_sha256"] = sha(canonical({
                            "kind": "packet", "origin": origin["origin"],
                            "old_defect_sha256": full_row_digest(p2, defect),
                            "character": list(CHARACTERS[character]),
                        }))
                        raw_meta["packet_sha256"] = packet_receipt["sha256"]
                        raw_meta["packet_row_sha256"] = sha(
                            packet[origin["origin"]].tobytes(order="C"))
                    else:
                        parent_index = ORDER[4 + character] + origin["parent"]
                        parent = full_from(cache, p2, p1store, parent_index)
                        raw = p2.act_source_word_precision2(
                            context, parent, (origin["letter"],))
                        raw_meta = {
                            "literal_input_sha256": sha(canonical({
                                "kind": "actor", "letter": origin["letter"],
                                "actor_order": list(ACTORS),
                            })),
                            "parent_row_sha256": [full_row_digest(p2, parent)],
                        }
                    work = recurse_node(
                        p2, cache, p1store, global_id, pivot, block["rank"],
                        node, raw, {"defect", "actor"}, 8232)
                    offset, row_sha = cache.append(p2, work[2].reshape(-1))
                    record, _ = make_instruction(
                        p2, cache, p1store, global_id,
                        ORDER[4 + character], node, origin, raw, work,
                        raw_meta, offset, row_sha, rolling)
                    rolling = bytes.fromhex(record["ancestry_sha256"])
                    instructions.write(record)
                    if cache.cursor % CHECKPOINT_INTERVAL == 0:
                        durable_checkpoint("new")
                        enforce(started, "new")
            finally:
                handle = getattr(packet, "_mmap", None)
                if handle is not None:
                    try:
                        handle.close()
                    except (BufferError, ValueError):
                        pass
        runtime_phase("build.stream_terminal")
        require(cache is not None and instructions is not None
                and cache.cursor == ROWS and instructions.rows == ROWS,
                "terminal_cursor")
        durable_checkpoint("new")
        enforce(started, "terminal")
    except (ResourceStop, KeyboardInterrupt) as terminal:
        _promotion_boundary(
            staging, out, checkpoint_path, terminal=terminal, cache=cache,
            instructions=instructions, last_checkpoint=last_checkpoint)
    except BaseException:
        # A rejected run may leave diagnostics for the operator, but any
        # retained prefix is first rolled back to the authenticated sidecar so
        # it can never be uploaded as a misleading byte stream.
        if cache is not None and instructions is not None \
                and last_checkpoint is not None:
            try:
                _rollback_prefix(cache, instructions, last_checkpoint)
            except BaseException:
                pass
        raise
    finally:
        close_error: BaseException | None = None
        try:
            if instructions is not None:
                instructions.close()
        except BaseException as exc:
            close_error = exc
        try:
            if cache is not None:
                cache.close()
        except BaseException as exc:
            if close_error is None:
                close_error = exc
        try:
            p1store.close()
        except BaseException as exc:
            if close_error is None:
                close_error = exc
        if close_error is not None:
            raise close_error
    require(cache is not None and instructions is not None,
            "build_stream_missing")
    cache_file = staging / CHECKPOINT_FILES[0]
    instruction_file = staging / CHECKPOINT_FILES[1]
    runtime_phase("build.final_receipts")
    require(cache_file.stat().st_size == CACHE_BYTES, "cache_size")
    inst_receipt = instruction_receipt(
        instruction_file, ROWS, ROW_BYTES, cache.row_hashes,
        rolling.hex(), instructions.digest.hexdigest())
    cache_sha = file_sha(cache_file)
    require(cache_sha == cache.digest.hexdigest(), "cache_digest")
    registry.verify()
    require(file_sha(Path(__file__).resolve()) == boundary["producer_sha256"],
            "producer_changed_during_build")
    require(file_sha(SEM_PATH) == SEM_SHA
            and file_sha(CHECKER_PATH) == CHECKER_SHA
            and file_sha(G1_PATH) == G1_SHA and file_sha(P2_PATH) == P2_SHA
            and file_sha(STRUCTURAL_PATH) == STRUCTURAL_SHA
            and file_sha(FLOOR_PATH) == FLOOR_SHA
            and file_sha(WORDS_PATH) == WORDS_SHA,
            "semantic_source_changed_during_build")
    manifest = {
        "schema": "d972.r07.canonical-p1-dag-degree2-lift.v8",
        "status": "CANONICAL_P1_DAG_DEGREE2_LIFT_CANDIDATE",
        "producer_sha256": boundary["producer_sha256"],
        "semantic_file_hashes": SEMANTIC_FILES,
        "imports": IMPORT_HASHES,
        "launch_manifest_sha256": boundary["launch_sha256"],
        "checker_result_sha256": boundary["checker_result_sha256"],
        "checker_workflow_receipt_sha256":
            boundary["checker_workflow_receipt_sha256"],
        "checker_success_artifact": dict(CHECKER_SUCCESS_ARTIFACT),
        "semantic_receipt_sha256": launch_expected_receipts(
            boundary["receipt_digests"]),
        "executable_hashes": {
            "producer_v8": boundary["producer_sha256"],
            "semantic_v5": SEM_SHA, "checker_v5": CHECKER_SHA,
        },
        "raw_artifacts": boundary["raw_artifacts"],
        "raw_file_registry": registry.entries(),
        "source_ancestry": {
            "source_run": SOURCE_RUN, "source_attempt": SOURCE_ATTEMPT,
            "source_head": SOURCE_HEAD, "prepare_body_sha256": PREPARE_DIGEST,
            "parents": list(PARENTS),
            "producer_receipts": launch_expected_receipts(
                boundary["receipt_digests"]),
            "checker_result_sha256": boundary["checker_result_sha256"],
            "checker_workflow_receipt_sha256":
                boundary["checker_workflow_receipt_sha256"],
            "checker_success_artifact": dict(CHECKER_SUCCESS_ARTIFACT),
        },
        "character_order": [list(value) for value in CHARACTERS],
        "actor_order": list(ACTORS),
        "monomial_order": [list(value) for value in MONOMIALS],
        "global_order": ORDER,
        "rows": ROWS,
        "row_trits": D2_WIDTH,
        "row_bytes": ROW_BYTES,
        "instruction": {"path": instruction_file.name, **inst_receipt},
        "cache": {"path": cache_file.name, "rows": ROWS,
                  "bytes": CACHE_BYTES, "sha256": cache_sha,
                  "final_lf": False, "eof": True},
        "ancestry_sha256": rolling.hex(),
        "independent_checker": False,
        **FALSE_CLAIMS,
    }
    _promotion_boundary(staging, out, checkpoint_path, manifest=manifest)
    print(json.dumps({"status": manifest["status"], "rows": ROWS,
                      "cache_bytes": CACHE_BYTES,
                      "instruction_rows": ROWS}, sort_keys=True), flush=True)


def _expect_reject(call: Callable[[], Any]) -> int:
    try:
        call()
    except (RuntimeError, ValueError, OSError, AssertionError):
        return 1
    raise RuntimeError("fixture_accept")


def _tiny_instruction(cache: PackedCache, instructions: InstructionSink,
                      node: int, predecessor: bytes) -> bytes:
    """Emit one deterministic fixture row through the production ABI."""
    tiny = TinyP2()
    dense = np.asarray([(node + index) % 3 for index in range(4)],
                       dtype=np.uint8)
    offset, row_sha = cache.append(tiny, dense)
    unsigned = {
        "node": node,
        "origin": {"kind": "projected_seed", "seed": 1},
        "reductions": [], "scale": 1,
        "raw_origin_sha256": "a" * 64,
        "raw_origin_components_sha256": {
            "p0": "b" * 64, "p1": "c" * 64,
            "p2": "d" * 64, "aux": "e" * 64,
        },
        "literal_input_sha256": None,
        "old_defect_literal_input_sha256": None,
        "parent_row_sha256": [], "packet_sha256": None,
        "packet_row_sha256": None, "reduction_parent_sha256": [],
        "p1_sha256": "f" * 64,
        "offset": offset, "length": cache.row_bytes,
        "row_receipt": {"offset": offset, "length": cache.row_bytes,
                         "sha256": row_sha},
        "predecessor": predecessor.hex(),
    }
    record = dict(unsigned)
    record["ancestry_sha256"] = sha(predecessor + canonical(unsigned))
    instructions.write(record)
    return bytes.fromhex(record["ancestry_sha256"])


def _tiny_stage(stage: Path, checkpoint_path: Path, pins: dict[str, Any],
                stop_at: int | None = None,
                total_rows: int = 12,
                global_order: list[int] | None = None) -> None:
    order = global_order or [0, 3, 6, 9, total_rows]
    stage.mkdir(parents=True)
    cache = PackedCache(stage / CHECKPOINT_FILES[0], 4)
    instructions = InstructionSink(stage / CHECKPOINT_FILES[1])
    rolling = b"\0" * 32
    checkpoint(cache, instructions, "startup", time.monotonic(),
               rss_reader=lambda: 7, checkpoint_path=checkpoint_path,
               pins=pins, global_order=order,
               total_rows=total_rows)
    limit = total_rows if stop_at is None else stop_at
    for node in range(limit):
        rolling = _tiny_instruction(cache, instructions, node, rolling)
    checkpoint(cache, instructions, "prefix", time.monotonic(),
               rss_reader=lambda: 7, checkpoint_path=checkpoint_path,
               pins=pins, global_order=order,
               total_rows=total_rows)
    instructions.close()
    cache.close()


def fixture_authenticated_resume() -> tuple[int, int]:
    """Bounded cross-boundary resume, rollback, and mutation matrix."""
    accepted = rejected = 0
    total_rows = 12
    # Eight intervals model the four old/four new production boundaries.
    tiny_order = [0, 1, 2, 3, 4, 6, 8, 10, total_rows]
    pins = {
        "producer_sha256": "1" * 64,
        "launch_manifest_sha256": "2" * 64,
        "launch_schema": "fixture.launch.v1",
        "source_run": "fixture", "source_attempt": "1",
        "source_head": "3" * 40,
        "receipt_hashes": {"prepare": "4" * 64,
                           "blocks": ["5" * 64] * 4,
                           "join": "6" * 64},
        "checker_result_sha256": "7" * 64,
        "checker_workflow_receipt_sha256": "8" * 64,
        "checker_success_artifact": {
            "id": 0, "name": "fixture", "archive_bytes": 0,
            "digest": "sha256:" + "9" * 64,
        },
        "semantic_file_hashes": {"fixture": "a" * 64},
        "import_hashes": {"fixture": "b" * 64},
        "raw_artifacts": [{"role": "fixture", "body_file": "fixture",
                           "body_sha256": "c" * 64, "body_bytes": 0}],
        "prepare_body_sha256": "d" * 64,
        "parents": ["e" * 64] * 4,
        "global_order": tiny_order,
        "old_ranks": [3, 3, 3, 3],
        "new_ranks": [3, 3, 3, 3],
        "launch_input_identity": {"source_run": "fixture",
                                   "source_attempt": "1",
                                   "source_head": "3" * 40,
                                   "checker_result_sha256": "7" * 64,
                                   "checker_workflow_receipt_sha256": "8" * 64,
                                   "receipt_hashes": {
                                       "prepare": "4" * 64,
                                       "blocks": ["5" * 64] * 4,
                                       "join": "6" * 64}},
    }
    with tempfile.TemporaryDirectory(prefix="task827-resume-") as td:
        root = Path(td)
        uninterrupted = root / "uninterrupted"
        _tiny_stage(uninterrupted, uninterrupted / "checkpoint.json", pins,
                    total_rows=total_rows, global_order=tiny_order)
        uninterrupted_checkpoint = json.loads(
            (uninterrupted / "checkpoint.json").read_text("ascii"))

        def finish_resume(target: Path, orphan: bool = False) -> None:
            nonlocal accepted
            checkpoint_value = json.loads(
                (target / "checkpoint.json").read_text("ascii"))
            cache, instructions, cursor, rolling_hex, _ = resume_prefix(
                target, target / "checkpoint.json", pins, total_rows, 4, 1,
                tiny_order)
            require(cursor == checkpoint_value["cursor"]
                    and rolling_hex == instructions.ancestry_head,
                    "fixture_resume_cursor")
            state = _checkpoint_state(checkpoint_value)
            if orphan:
                require(cursor + 2 <= total_rows, "fixture_orphan_room")
                rolling = bytes.fromhex(rolling_hex)
                rolling = _tiny_instruction(cache, instructions, cursor, rolling)
                _tiny_instruction(cache, instructions, cursor + 1, rolling)
                _rollback_prefix(cache, instructions, state)
                require(cache.cursor == cursor,
                        "fixture_orphan_rollback")
                # Re-authenticate the durable rollback boundary before any
                # continuation; this is the same cross-process path used by
                # the next runner after UNKNOWN_RESOURCE.
                instructions.close(); cache.close()
                cache, instructions, cursor, rolling_hex, _ = resume_prefix(
                    target, target / "checkpoint.json", pins, total_rows,
                    4, 1, tiny_order)
            rolling = bytes.fromhex(rolling_hex)
            for node in range(cursor, total_rows):
                rolling = _tiny_instruction(cache, instructions, node, rolling)
            checkpoint(cache, instructions, "prefix", time.monotonic(),
                       rss_reader=lambda: 7,
                       checkpoint_path=target / "checkpoint.json", pins=pins,
                       global_order=tiny_order, total_rows=total_rows)
            instructions.close(); cache.close()
            for name in CHECKPOINT_FILES:
                require((target / name).read_bytes() ==
                        (uninterrupted / name).read_bytes(),
                        "fixture_resume_byte_identity:" + name)
            resumed_checkpoint = json.loads(
                (target / "checkpoint.json").read_text("ascii"))
            require(resumed_checkpoint == uninterrupted_checkpoint,
                    "fixture_resume_semantic_final_fields")
            require(not (target / "candidate").exists(),
                    "fixture_rejected_promote")
            accepted += 1

        # Cursor zero, all eight global boundaries, and one mid-new cursor.
        for cursor in [0, 1, 2, 3, 4, 6, 8, 10, 12, 7]:
            partial = root / ("partial-" + str(cursor))
            _tiny_stage(partial, partial / "checkpoint.json", pins,
                        stop_at=cursor, total_rows=total_rows,
                        global_order=tiny_order)
            if cursor == 4:
                # A genuine post-checkpoint orphan is written and rolled back
                # before continuation; it is never promoted as a candidate.
                finish_target = root / "resumed-orphan"
                shutil.copytree(partial, finish_target)
                finish_resume(finish_target, orphan=True)
            resumed = root / ("resumed-" + str(cursor))
            shutil.copytree(partial, resumed)
            finish_resume(resumed)
        # The resource terminal retains the exact durable prefix and no
        # candidate path, matching the production UNKNOWN_RESOURCE branch.
        resource_partial = root / "resource-partial"
        _tiny_stage(resource_partial, resource_partial / "checkpoint.json",
                    pins, stop_at=5, total_rows=total_rows,
                    global_order=tiny_order)
        try:
            raise ResourceStop("UNKNOWN_RESOURCE:fixture")
        except ResourceStop:
            require((resource_partial / "checkpoint.json").exists(),
                    "fixture_resource_checkpoint")
            require(not (resource_partial / "candidate").exists(),
                    "fixture_resource_nonpromotion")
            accepted += 1

        partial = root / "mutation-source"
        _tiny_stage(partial, partial / "checkpoint.json", pins, stop_at=4,
                    total_rows=total_rows, global_order=tiny_order)

        def mutate(label: str, action: Callable[[Path], None]) -> None:
            nonlocal rejected
            target = root / ("mutation-" + label)
            shutil.copytree(partial, target)
            action(target)
            rejected += _expect_reject(lambda: resume_prefix(
                target, target / "checkpoint.json", pins, total_rows, 4, 1,
                tiny_order))

        mutate("cache-truncated", lambda p: (p / "degree2.cache.bin").write_bytes(
            (p / "degree2.cache.bin").read_bytes()[:-1]))
        def extend_cache(path: Path) -> None:
            with (path / "degree2.cache.bin").open("ab") as stream:
                stream.write(b"\0")
        mutate("cache-extended", extend_cache)
        def flip_cache(path: Path) -> None:
            raw = bytearray((path / "degree2.cache.bin").read_bytes())
            raw[0] ^= 1
            (path / "degree2.cache.bin").write_bytes(raw)
        mutate("cache-mutated", flip_cache)
        mutate("instruction-truncated", lambda p: (p / "instructions.jsonl").write_bytes(
            (p / "instructions.jsonl").read_bytes()[:-1]))
        def mutate_instruction_receipt(path: Path) -> None:
            rows = (path / "instructions.jsonl").read_bytes().splitlines(True)
            value = json.loads(rows[0])
            value["row_receipt"]["sha256"] = "f" * 64
            rows[0] = canonical(value)
            (path / "instructions.jsonl").write_bytes(b"".join(rows))
        mutate("instruction-receipt", mutate_instruction_receipt)
        def mutate_predecessor(path: Path) -> None:
            rows = (path / "instructions.jsonl").read_bytes().splitlines(True)
            value = json.loads(rows[1])
            value["predecessor"] = "1" * 64
            rows[1] = canonical(value)
            (path / "instructions.jsonl").write_bytes(b"".join(rows))
        mutate("instruction-predecessor", mutate_predecessor)
        def mutate_ancestry(path: Path) -> None:
            rows = (path / "instructions.jsonl").read_bytes().splitlines(True)
            value = json.loads(rows[0])
            value["ancestry_sha256"] = "2" * 64
            rows[0] = canonical(value)
            (path / "instructions.jsonl").write_bytes(b"".join(rows))
        mutate("instruction-ancestry", mutate_ancestry)
        def mutate_checkpoint(path: Path, key: str, value: Any) -> None:
            cp_value = json.loads((path / "checkpoint.json").read_text())
            cp_value[key] = value
            (path / "checkpoint.json").write_bytes(canonical(cp_value))
        mutate("checkpoint-cursor", lambda p: mutate_checkpoint(p, "cursor", 3))
        mutate("checkpoint-cache-digest",
               lambda p: mutate_checkpoint(p, "cache", {
                   **json.loads((p / "checkpoint.json").read_text())["cache"],
                   "sha256": "3" * 64}))
        mutate("checkpoint-pin", lambda p: mutate_checkpoint(
            p, "pins", {**pins, "producer_sha256": "4" * 64}))
        mutate("checkpoint-claim", lambda p: mutate_checkpoint(
            p, "A0", True))
        def add_roster(path: Path) -> None:
            (path / "extra").write_bytes(b"x")
        mutate("roster-extra", add_roster)
        require(not (root / "candidate").exists(), "fixture_rejected_promote")
    return accepted, rejected


def fixture_cross_runner_pins() -> tuple[int, int]:
    """Check that only runner-local launch wrappers vary across runners."""
    accepted = rejected = 0
    receipts = [str(index) * 64 for index in range(1, 7)]
    with tempfile.TemporaryDirectory(prefix="task835-cross-runner-") as td:
        root = Path(td)
        actual = root / "immutable-input.bin"
        wrapper = root / "launch-manifest.json"
        actual.write_bytes(b"immutable-input-v1")

        def boundary(wrapper_bytes: bytes, input_bytes: bytes | None = None
                     ) -> dict[str, Any]:
            if input_bytes is not None:
                actual.write_bytes(input_bytes)
            wrapper.write_bytes(wrapper_bytes)
            registry = FileRegistry()
            registry.add(actual, sha(actual.read_bytes()), "fixture-input")
            registry.add(wrapper, sha(wrapper.read_bytes()), "launch-manifest")
            raw = [{"role": "fixture", "body_file": actual.name,
                    "body_sha256": sha(actual.read_bytes()),
                    "body_bytes": actual.stat().st_size}]
            launch = {
                "schema": "fixture.launch.v1", "receipt_hashes": {
                    "prepare": receipts[0], "blocks": receipts[1:5],
                    "join": receipts[5]},
                "checker_result_sha256": "a" * 64,
                "checker_workflow_receipt_sha256": "b" * 64,
                "checker_success_artifact": {"id": 1, "name": "fixture",
                                               "archive_bytes": 1,
                                               "digest": "sha256:" + "c" * 64},
                "source_run": "fixture", "source_attempt": "1",
                "source_head": "d" * 40,
                "executable_hashes": {"producer_v8": "e" * 64},
                "import_hashes": {"fixture": "f" * 64},
                "semantic_file_hashes": {"fixture": "0" * 64},
            }
            return {"launch": launch, "raw_artifacts": raw,
                    "p1_auth": {"fixture": "p1"}, "registry": registry,
                    "receipt_digests": receipts,
                    "producer_sha256": "1" * 64,
                    "checker_result_sha256": "a" * 64,
                    "checker_workflow_receipt_sha256": "b" * 64}

        old = _checkpoint_pins(boundary(b"runner-a", b"immutable-input-v1"))
        wrapper_only = _checkpoint_pins(boundary(b"runner-b"))
        require(old == wrapper_only, "fixture_runner_wrapper_variation")
        accepted += 1
        changed = _checkpoint_pins(boundary(b"runner-c", b"immutable-input-v2"))
        require(old != changed, "fixture_runner_input_variation")
        accepted += 1

        stage = root / "resume"
        _tiny_stage(stage, stage / "checkpoint.json", old, stop_at=1,
                    total_rows=2, global_order=[0, 1, 2])
        cache, instructions, _, _, _ = resume_prefix(
            stage, stage / "checkpoint.json", wrapper_only, 2, 4, 1,
            [0, 1, 2])
        instructions.close(); cache.close()
        accepted += 1
        rejected += _expect_reject(lambda: resume_prefix(
            stage, stage / "checkpoint.json", changed, 2, 4, 1,
            [0, 1, 2]))
    return accepted, rejected


def fixture_reached_promotion_boundary() -> tuple[int, int]:
    """Reach both terminals of the production promotion boundary."""
    accepted = rejected = 0
    tiny_order = [0, 1, 2, 3, 4, 6, 8, 10, 12]
    pins = {
        "producer_sha256": "1" * 64,
        "launch_manifest_sha256": "2" * 64,
        "launch_schema": "fixture.launch.v1",
        "source_run": "fixture", "source_attempt": "1",
        "source_head": "3" * 40,
        "receipt_hashes": {"prepare": "4" * 64,
                           "blocks": ["5" * 64] * 4,
                           "join": "6" * 64},
        "checker_result_sha256": "7" * 64,
        "checker_workflow_receipt_sha256": "8" * 64,
        "checker_success_artifact": {
            "id": 0, "name": "fixture", "archive_bytes": 0,
            "digest": "sha256:" + "9" * 64},
        "semantic_file_hashes": {"fixture": "a" * 64},
        "import_hashes": {"fixture": "b" * 64},
        "raw_artifacts": [{"role": "fixture", "body_file": "fixture",
                           "body_sha256": "c" * 64, "body_bytes": 0}],
        "prepare_body_sha256": "d" * 64,
        "parents": ["e" * 64] * 4,
        "global_order": tiny_order,
        "old_ranks": [3, 3, 3, 3], "new_ranks": [3, 3, 3, 3],
        "launch_input_identity": {"source_run": "fixture",
                                   "source_attempt": "1",
                                   "source_head": "3" * 40},
    }
    with tempfile.TemporaryDirectory(prefix="task842-promotion-") as td:
        root = Path(td)
        stage = root / "resource-stage"
        checkpoint_path = stage / "checkpoint.json"
        requested_out = root / "fresh-requested-output"
        require(not requested_out.exists(), "fixture_output_not_fresh")
        _tiny_stage(stage, checkpoint_path, pins, stop_at=4,
                    total_rows=12, global_order=tiny_order)
        checkpoint_value = json.loads(checkpoint_path.read_text("ascii"))
        cache, instructions, cursor, rolling_hex, _ = resume_prefix(
            stage, checkpoint_path, pins, 12, 4, 1, tiny_order)
        require(cursor == 4, "fixture_promotion_cursor")
        rolling = bytes.fromhex(rolling_hex)
        rolling = _tiny_instruction(cache, instructions, cursor, rolling)
        _tiny_instruction(cache, instructions, cursor + 1, rolling)
        terminal = ResourceStop("UNKNOWN_RESOURCE:fixture_promotion")
        reached = propagated = False
        try:
            reached = True
            _promotion_boundary(
                stage, requested_out, checkpoint_path, terminal=terminal,
                cache=cache, instructions=instructions,
                last_checkpoint=_checkpoint_state(checkpoint_value))
        except ResourceStop as caught:
            propagated = caught is terminal
        finally:
            instructions.close(); cache.close()
        require(reached and propagated, "fixture_resource_terminal_propagated")
        require(stage.exists() and checkpoint_path.exists()
                and not requested_out.exists(),
                "fixture_resource_nonpromotion_reached")
        cache, instructions, cursor, _, _ = resume_prefix(
            stage, checkpoint_path, pins, 12, 4, 1, tiny_order)
        require(cursor == checkpoint_value["cursor"],
                "fixture_resource_rollback_authenticated")
        instructions.close(); cache.close()
        accepted += 1

        success_stage = root / "success-stage"
        success_stage.mkdir()
        success_checkpoint = success_stage / "checkpoint.json"
        success_checkpoint.write_bytes(b"unchecked-sidecar")
        (success_stage / "payload.bin").write_bytes(b"payload")
        success_out = root / "success-output"
        success_manifest = {"fixture": "promotion-success",
                            "A0": False, "verified": False}
        _promotion_boundary(success_stage, success_out, success_checkpoint,
                            manifest=success_manifest)
        require(success_out.is_dir() and not success_stage.exists()
                and not (success_out / "checkpoint.json").exists()
                and (success_out / "payload.bin").read_bytes() == b"payload"
                and (success_out / "manifest.json").read_bytes() ==
                    canonical(success_manifest),
                "fixture_success_promotion_reached")
        accepted += 1
    return accepted, rejected


def fixture_body_size_artifact() -> tuple[int, int]:
    """Exercise the integer envelope-size and physical registry boundary."""
    with tempfile.TemporaryDirectory(prefix="task781-body-size-") as td:
        root = Path(td)
        payload = b"{}"
        digest = sha(payload)
        body_path = root / f"block-0.{digest}.json"
        body_path.write_bytes(payload)
        # This is the shape returned by the pinned block-envelope helper;
        # only its small integer size crosses this producer boundary.
        envelope = (root, {"fixture": True}, len(payload))
        safe, _, body_size = envelope
        body_size = nonnegative_size(body_size, "fixture_block_body_size")
        registry = FileRegistry()
        entry = artifact_entry(safe, "block-0", "block-0", digest, body_size)
        require(entry["body_bytes"] == body_size
                and entry["body_sha256"] == digest,
                "fixture_body_size_entry")
        registry.add(body_path, digest, "sealed-body")
        registry.verify()
        rejected = 0
        for bad in (payload, True, -1, body_size + 1):
            rejected += _expect_reject(lambda value=bad: artifact_entry(
                safe, "block-0", "block-0", digest, value))
        body_path.write_bytes(b"[]")
        rejected += _expect_reject(registry.verify)
        return 1, rejected


def _fixture_join(producer: str) -> dict[str, Any]:
    return {
        "schema": "d972.r07.p1.componentwise.v1",
        "terminal": "TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED",
        "global_relations": 32280, "old_ranks": 2014, "new_ranks": 6045,
        "dag_nodes": 8059, "old_local_relations": 8232,
        "direct_packet_halves": 32928, "packet_basis_halves": 32928,
        "new_actor_identities": 24180, "compound_obligations": 65340,
        "resident_global_matrix": False, "independent_checker": False,
        "precision2": False, "A0": False, "COMMON": False,
        "COMPATIBLE_LIFT": False, "FAKE": False, "IHARA": False,
        "verified": False, "producer_sha256": producer,
    }


class TinyGrade1:
    LOWER_ECHELON_WIDTH = 4

    @staticmethod
    def pack_trits(value: np.ndarray) -> np.ndarray:
        flat = np.asarray(value, dtype=np.uint8).reshape(-1)
        require(flat.size % 4 == 0 and not np.any(flat > 2), "tiny_pack")
        return (flat.reshape(-1, 4) @ np.asarray([1, 3, 9, 27],
                                                   dtype=np.uint16)).astype(np.uint8)

    @staticmethod
    def unpack_trits(value: np.ndarray, width: int) -> np.ndarray:
        packed = np.asarray(value, dtype=np.uint8).reshape(-1)
        require(packed.size * 4 == width and not np.any(packed > 80),
                "tiny_unpack")
        return np.asarray([[(int(x) // (3 ** index)) % 3
                             for index in range(4)] for x in packed],
                           dtype=np.uint8).reshape(-1)


class TinyP2:
    CHARACTER_LABELS = CHARACTERS
    SOURCE_DEGREE0_PER_CHARACTER = 1
    SOURCE_DEGREE1_PER_CHARACTER = 4
    SOURCE_DEGREE1_WIDTH = 16
    SOURCE_DEGREE2_PER_CHARACTER = 1
    SOURCE_DEGREE2_WIDTH = 4
    grade1 = TinyGrade1

    @staticmethod
    def _add_mod3(destination: np.ndarray, source: np.ndarray,
                  scalar: int = 1) -> None:
        destination[:] = (destination.astype(np.uint16)
                          + (scalar % 3) * source.astype(np.uint16)) % 3

    @staticmethod
    def flatten_precision1(p0: np.ndarray, p1: np.ndarray,
                           aux: np.ndarray) -> np.ndarray:
        return np.concatenate((p0.reshape(-1), p1.reshape(-1), aux.reshape(-1)))

    @staticmethod
    def evaluate_seed_precision2(context: Any,
                                 word: tuple[int, ...]
                                 ) -> tuple[np.ndarray, ...]:
        require(word, "tiny_seed_word")
        base0 = np.zeros((4, 1), dtype=np.uint8)
        base1 = np.ones((4, 4), dtype=np.uint8)
        base2 = np.zeros((4, 1), dtype=np.uint8)
        base_aux = np.zeros(8, dtype=np.uint8)
        return base0, base1, base2, base_aux

    @staticmethod
    def split_precision1(row: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        require(row.shape == (28,), "tiny_split")
        return row[:4].reshape(4, 1), row[4:20].reshape(4, 4), row[20:].copy()

    @staticmethod
    def project_full_by_words(context: Any, row: tuple[np.ndarray, ...],
                              label: tuple[int, int]) -> tuple[np.ndarray, ...]:
        selected = CHARACTERS.index(label)
        out = tuple(part.copy() for part in row)
        out[0][:] = 0
        out[1][:] = 0
        out[1][selected] = row[1][selected]
        out[2][selected, 0] = (int(row[2][selected, 0])
                               + int(row[1][selected, 0])) % 3
        out[3][:] = 0
        return out

    @staticmethod
    def act_source_word_precision2(context: Any, row: tuple[np.ndarray, ...],
                                   word: tuple[int, ...]) -> tuple[np.ndarray, ...]:
        require(len(word) == 1 and word[0] in ACTORS, "tiny_actor_letter")
        out = tuple(part.copy() for part in row)
        scalar = 1 if word[0] in (1, 2) else 2
        out[2][:, 0] = (out[2][:, 0].astype(np.uint16)
                        + scalar * out[1][:, 0].astype(np.uint16)) % 3
        return out


class TinyP1:
    def __init__(self, row: np.ndarray):
        self._row = row

    def row(self, index: int) -> np.ndarray:
        require(index == 0, "tiny_p1_index")
        return self._row.copy()


def fixture_receipt_validation(deps: dict[str, types.ModuleType]) -> tuple[int, int]:
    sem, checker = deps["sem"], deps["checker"]
    prepare, blocks = sem._fixture_receipts()
    sem.validate_prepare_receipt(prepare, SEM_SHA)
    for index, block in enumerate(blocks):
        sem.validate_block_receipt(block, index, SEM_SHA)
    sem.validate_join_receipts(prepare, blocks)
    join = _fixture_join(SEM_SHA)
    # The validator fixture uses the exact accepted six-receipt digest vector;
    # the receipt objects above separately exercise v5's semantic validators.
    digests = [ACCEPTED_RECEIPT_HASHES["prepare"],
               *ACCEPTED_RECEIPT_HASHES["blocks"],
               ACCEPTED_RECEIPT_HASHES["join"]]
    checker_prepare = dict(prepare)
    checker_prepare["independent_checker"] = True
    checker_prepare["checker_digests"] = {
        "prepare_body_sha256": PREPARE_DIGEST,
        "equality_receipts_sha256": checker_prepare["equality_receipts_sha256"],
        "packet_component_sha256": "a" * 64,
        "projector_full_sha256": "b" * 64,
    }
    checker_blocks = []
    for index, block in enumerate(blocks):
        value = dict(block)
        value["independent_checker"] = True
        value["checker_digests"] = {
            "block_body_sha256": value["block_body_sha256"],
            "basis_sha256": value["basis_sha256"],
            "origin_reductions_sha256": f"{index + 30:064x}",
            "actor_transitions_sha256": f"{index + 40:064x}",
            "dag_sha256": value["dag_sha256"],
        }
        checker_blocks.append(value)
    semantic_family = sha(canonical({
        "prepare": checker_prepare["counts"],
        "equality": checker_prepare["equality_receipts"],
        "blocks": [value["counts"] for value in checker_blocks],
        "projector": checker_prepare["projector_identity"],
    }))
    checker_result = {
        "schema": checker.CHECKER_SCHEMA,
        "terminal": "TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED_INDEPENDENTLY",
        "marker": checker.MARKER, "source_run": SOURCE_RUN,
        "source_attempt": SOURCE_ATTEMPT, "source_head": SOURCE_HEAD,
        "prepare_body_sha256": PREPARE_DIGEST, "old_ranks": 2014,
        "new_ranks": 6045, "dag_nodes": 8059, "global_relations": 32280,
        "old_local_relations": 8232, "direct_packet_halves": 32928,
        "packet_basis_halves": 32928, "new_actor_identities": 24180,
        "compound_obligations": 65340, "prepare": checker_prepare,
        "blocks": checker_blocks,
        "producer_receipt_sha256": launch_expected_receipts(digests),
        "producer_sha256": SEM_SHA,
        "checker_digests": {
            "prepare": checker_prepare["checker_digests"],
            "blocks": [value["checker_digests"] for value in checker_blocks],
            "producer_receipts": launch_expected_receipts(digests),
            "semantic_family_sha256": semantic_family,
        }, "resident_global_matrix": False, "independent_checker": True,
        "precision2": False, "A0": False, "COMMON": False,
        "COMPATIBLE_LIFT": False, "FAKE": False, "IHARA": False,
        "verified": False, "elapsed_seconds": 0.0, "peak_rss_bytes": 0,
    }
    expected_manifest = checker_prepare["input_manifest_sha256"]
    validate_checker_result(checker_result, checker, digests,
                            expected_manifest)
    checker_workflow_receipt = {
        "schema": "d972.r07.p1.componentwise.checker-only.v3.workflow-receipt",
        "workflow_run_id": CHECKER_WORKFLOW_RUN_ID,
        "workflow_run_attempt": CHECKER_WORKFLOW_RUN_ATTEMPT,
        "workflow_commit_sha": CHECKER_WORKFLOW_COMMIT,
        "producer_run": PRODUCER_RUN,
        "producer_attempt": PRODUCER_ATTEMPT,
        "producer_head": PRODUCER_HEAD,
        "producer_run_status": "completed",
        "producer_run_conclusion": "failure",
        "producer_jobs": [
            {"id": row[0], "name": row[1], "status": row[2],
             "conclusion": row[3]} for row in PRODUCER_JOBS
        ],
        "producer_artifact": dict(PRODUCER_ARTIFACT),
        "producer_sha256": SEM_SHA,
        "checker_sha256": CHECKER_SHA,
        "independent_result_sha256": CHECKER_RESULT_SHA,
        "producer_receipt_sha256": launch_expected_receipts(digests),
        "checker_elapsed_seconds": checker_result["elapsed_seconds"],
        "checker_peak_rss_bytes": checker_result["peak_rss_bytes"],
        "checker_process": {"elapsed_wall_clock": "03.76",
                            "peak_rss_kbytes": 0},
        "claim_flags": dict(CHECKER_FLAGS),
        "independent_checker": True,
        "verified": False,
    }
    validate_checker_workflow_receipt(
        checker_workflow_receipt, checker_result, CHECKER_RESULT_SHA, digests)
    # Preserve the accepted colon spellings while admitting the exact
    # historical one-field GNU-time extraction above.
    validate_elapsed_clock("0:00.01")
    validate_elapsed_clock("1:02:03.50")
    raw_artifacts = [{"role": "prepare", "root": "fixture/prepare",
                      "body_file": "prepare.fixture.json",
                      "body_sha256": "b" * 64, "body_bytes": 1,
                      "identity": [1, 2, 1, 1, 1]}]
    raw_artifacts += [{"role": f"block-{i}", "root": f"fixture/block-{i}",
                       "body_file": f"block-{i}.fixture.json",
                       "body_sha256": PARENTS[i], "body_bytes": 1,
                       "identity": [i + 2, 3, 1, 1, 1]} for i in range(4)]
    launch = {
        "schema": "d972.r07.canonical-p1-dag-degree2-lift.launch.v6",
        "raw_artifacts": raw_artifacts,
        "receipt_hashes": launch_expected_receipts(digests),
        "checker_result_sha256": CHECKER_RESULT_SHA,
        "checker_workflow_receipt_sha256": CHECKER_WORKFLOW_RECEIPT_SHA,
        "checker_success_artifact": dict(CHECKER_SUCCESS_ARTIFACT),
        "source_run": SOURCE_RUN, "source_attempt": SOURCE_ATTEMPT,
        "source_head": SOURCE_HEAD,
        "executable_hashes": {"producer_v8": "d" * 64,
                               "semantic_v5": SEM_SHA,
                               "checker_v5": CHECKER_SHA},
        "import_hashes": IMPORT_HASHES,
        "semantic_file_hashes": SEMANTIC_FILES,
    }
    validate_launch_manifest(
        launch, "d" * 64, digests, CHECKER_RESULT_SHA,
        CHECKER_WORKFLOW_RECEIPT_SHA, raw_artifacts)
    rejects = 0
    for bad_clock in ("", "not-a-number", "nan", "inf", "-0.01",
                      "60", "0:60", "0:00:60", "0:60:00",
                      "0::01", "0:00:00:01"):
        rejects += _expect_reject(
            lambda value=bad_clock: validate_elapsed_clock(value))
    altered = json.loads(json.dumps(join)); altered["terminal"] = "WRONG"
    rejects += _expect_reject(lambda: require(altered == join,
                                               "join_mutation"))
    altered_launch = json.loads(json.dumps(launch))
    altered_launch["receipt_hashes"]["join"] = "e" * 64
    rejects += _expect_reject(lambda: validate_launch_manifest(
        altered_launch, "d" * 64, digests, CHECKER_RESULT_SHA,
        CHECKER_WORKFLOW_RECEIPT_SHA, raw_artifacts))
    altered_checker = json.loads(json.dumps(checker_result))
    altered_checker["marker"] = "WRONG"
    rejects += _expect_reject(lambda: validate_checker_result(
        altered_checker, checker, digests, expected_manifest))

    # The accepted checker-v5 result, its checker-only workflow receipt, and
    # the success artifact form one provenance chain.  Each mutation below
    # enters the same production validators used before cache allocation.
    for field, bad in (
            ("checker_sha256", "0" * 64),
            ("independent_result_sha256", "1" * 64),
            ("workflow_run_id", CHECKER_WORKFLOW_RUN_ID + 1),
            ("workflow_commit_sha", "2" * 40)):
        altered_workflow = json.loads(json.dumps(checker_workflow_receipt))
        altered_workflow[field] = bad
        rejects += _expect_reject(lambda value=altered_workflow:
            validate_checker_workflow_receipt(
                value, checker_result, CHECKER_RESULT_SHA, digests))
    altered_workflow = json.loads(json.dumps(checker_workflow_receipt))
    altered_workflow["producer_receipt_sha256"]["blocks"][0] = "3" * 64
    rejects += _expect_reject(lambda: validate_checker_workflow_receipt(
        altered_workflow, checker_result, CHECKER_RESULT_SHA, digests))
    altered_workflow = json.loads(json.dumps(checker_workflow_receipt))
    altered_workflow["claim_flags"]["A0"] = True
    rejects += _expect_reject(lambda: validate_checker_workflow_receipt(
        altered_workflow, checker_result, CHECKER_RESULT_SHA, digests))
    altered_workflow = json.loads(json.dumps(checker_workflow_receipt))
    altered_workflow["independent_checker"] = False
    rejects += _expect_reject(lambda: validate_checker_workflow_receipt(
        altered_workflow, checker_result, CHECKER_RESULT_SHA, digests))

    altered_checker = json.loads(json.dumps(checker_result))
    altered_checker["prepare"]["input_manifest_sha256"] = "4" * 64
    rejects += _expect_reject(lambda: validate_checker_result(
        altered_checker, checker, digests, expected_manifest))

    for field, bad in (
            ("id", CHECKER_SUCCESS_ARTIFACT["id"] + 1),
            ("digest", "sha256:" + "5" * 64),
            ("archive_bytes", CHECKER_SUCCESS_ARTIFACT["archive_bytes"] + 1),
            ("name", CHECKER_SUCCESS_ARTIFACT["name"] + "-mutated")):
        altered_launch = json.loads(json.dumps(launch))
        altered_launch["checker_success_artifact"][field] = bad
        rejects += _expect_reject(lambda value=altered_launch:
            validate_launch_manifest(
                value, "d" * 64, digests, CHECKER_RESULT_SHA,
                CHECKER_WORKFLOW_RECEIPT_SHA, raw_artifacts))
    altered_launch = json.loads(json.dumps(launch))
    altered_launch["checker_workflow_receipt_sha256"] = "6" * 64
    rejects += _expect_reject(lambda: validate_launch_manifest(
        altered_launch, "d" * 64, digests, CHECKER_RESULT_SHA,
        CHECKER_WORKFLOW_RECEIPT_SHA, raw_artifacts))
    altered_launch = json.loads(json.dumps(launch))
    altered_launch["executable_hashes"]["checker_v5"] = "7" * 64
    rejects += _expect_reject(lambda: validate_launch_manifest(
        altered_launch, "d" * 64, digests, CHECKER_RESULT_SHA,
        CHECKER_WORKFLOW_RECEIPT_SHA, raw_artifacts))
    altered_checker = json.loads(json.dumps(checker_result))
    altered_checker["prepare"]["checker_digests"] = {}
    rejects += _expect_reject(lambda: validate_checker_result(
        altered_checker, checker, digests, expected_manifest))
    altered_checker = json.loads(json.dumps(checker_result))
    del altered_checker["blocks"][0]["checker_digests"]
    rejects += _expect_reject(lambda: validate_checker_result(
        altered_checker, checker, digests, expected_manifest))
    altered_checker = json.loads(json.dumps(checker_result))
    altered_checker["blocks"][1]["rank"] = 0
    rejects += _expect_reject(lambda: validate_checker_result(
        altered_checker, checker, digests, expected_manifest))
    altered_checker = json.loads(json.dumps(checker_result))
    altered_checker["prepare"]["counts"] = {}
    rejects += _expect_reject(lambda: validate_checker_result(
        altered_checker, checker, digests, expected_manifest))
    altered_checker = json.loads(json.dumps(checker_result))
    altered_checker["checker_digests"]["prepare"] = {
        **altered_checker["checker_digests"]["prepare"],
        "packet_component_sha256": "e" * 64,
    }
    rejects += _expect_reject(lambda: validate_checker_result(
        altered_checker, checker, digests, expected_manifest))
    return 3, rejects


def selftest() -> None:
    deps = load_dependencies()
    g1, p2 = deps["g1"], deps["p2"]
    accepted, rejected = fixture_receipt_validation(deps)
    resume_accepted, resume_rejected = fixture_authenticated_resume()
    accepted += resume_accepted
    rejected += resume_rejected
    runner_accepted, runner_rejected = fixture_cross_runner_pins()
    accepted += runner_accepted
    rejected += runner_rejected
    promotion_accepted, promotion_rejected = \
        fixture_reached_promotion_boundary()
    accepted += promotion_accepted
    rejected += promotion_rejected
    size_accepted, size_rejected = fixture_body_size_artifact()
    accepted += size_accepted
    rejected += size_rejected
    tiny = TinyP2()
    tiny_words = {"relators": [[1] for _ in range(44)]}
    seed_row = projected_seed(tiny, None, tiny_words, 1, CHARACTERS[2])
    require(np.any(seed_row[1][2])
            and all(not np.any(seed_row[1][index])
                    for index in range(4) if index != 2),
            "fixture_projected_seed")
    old_prepare = {"old_blocks": [{"record": {
        "seed_reductions": [[] for _ in range(44)]
    }}]}
    old_origin = {"kind": "seed", "lower_character": 0, "seed": 1}
    old_defect, old_meta = compile_old_defect(
        tiny, None, tiny_words, old_origin, None, None, old_prepare, [0])
    require(np.any(old_defect[1][0])
            and not np.any(old_defect[1][1:])
            and old_meta["literal_input_sha256"] == sha(canonical({
                "kind": "seed", "seed": 1, "word": [1],
                "character": list(CHARACTERS[0]),
            })), "fixture_old_character_seed_defect")
    accepted += 1
    zeros0 = np.zeros((4, 1), dtype=np.uint8)
    p1 = np.zeros((4, 4), dtype=np.uint8)
    p1[2, 0] = 1
    d2 = np.zeros((4, 1), dtype=np.uint8)
    aux = np.zeros(8, dtype=np.uint8)
    raw = (zeros0, p1, d2, aux)
    packet = compile_packet_v486(tiny, None, raw, CHARACTERS[2],
                                 np.asarray([1, 0, 0, 0], dtype=np.uint8))
    require(int(packet[2][2, 0]) == 1, "fixture_full_projector_triangular")
    accepted += 1
    rejected += _expect_reject(lambda: compile_packet_v486(
        tiny, None, raw, CHARACTERS[2],
        np.asarray([2, 0, 0, 0], dtype=np.uint8)))
    rejected += _expect_reject(lambda: compile_packet_v486(
        tiny, None, (zeros0, np.zeros_like(p1), d2, aux),
        CHARACTERS[2], np.asarray([0, 0, 0, 0], dtype=np.uint8)))
    # All four actor slots are live, and each retains a triangular P1 term.
    actor_results = []
    for letter in ACTORS:
        actor_results.append(tiny.act_source_word_precision2(
            None, raw, (letter,)))
    require(len(actor_results) == 4
            and {int(value[2][2, 0]) for value in actor_results} == {1, 2},
            "fixture_all_actor_slots")
    no_p1 = (zeros0.copy(), np.zeros_like(p1), d2.copy(), aux.copy())
    no_p1_actor = tiny.act_source_word_precision2(None, no_p1, (ACTORS[0],))
    require(int(actor_results[0][2][2, 0]) != int(no_p1_actor[2][2, 0]),
            "fixture_actor_triangular_change")
    accepted += 1
    # A scale-two ordered reduction changes P1 exactly; a truncation mutation
    # is rejected through the same recurse_node validator used by production.
    cache_path = Path(tempfile.mkdtemp(prefix="task755-selftest-")) / "c.bin"
    cache = PackedCache(cache_path, 4)
    prior_p1 = np.zeros(28, dtype=np.uint8)
    prior_p1[4 + 2 * 4] = 1
    prior_row = np.zeros(4, dtype=np.uint8)
    cache.append(tiny, prior_row)
    expected_p1 = np.zeros(28, dtype=np.uint8)
    expected_p1[4 + 2 * 4] = 1
    class TinyRows:
        def row(self, index: int) -> np.ndarray:
            require(index in (0, 1), "tiny_rows_index")
            return prior_p1.copy() if index == 0 else expected_p1.copy()
    p1store = TinyRows()
    node = {"pivot": 1, "lead": 0, "scale": 2,
            "origin": {"kind": "projected_seed", "seed": 1},
            "reductions": [[0, 1]]}
    zero_p1 = np.zeros_like(p1)
    scaled_raw = (zeros0.copy(), zero_p1, d2.copy(), aux.copy())
    work = recurse_node(tiny, cache, p1store, 1, 1, 2, node, scaled_raw,
                        {"projected_seed"})
    require(int(flatten_p1(tiny, work)[4 + 2 * 4]) == 1,
            "fixture_scale_two")
    rejected += _expect_reject(lambda: recurse_node(
        tiny, cache, TinyP1(np.zeros(28, dtype=np.uint8)), 1, 1, 2,
        node, scaled_raw, {"projected_seed"}))
    for bad in (
        {"pivot": True, "lead": 0, "scale": 1,
         "origin": {"kind": "projected_seed", "seed": 1}, "reductions": []},
        {"pivot": 0, "lead": 0, "scale": 1,
         "origin": {"kind": "projected_seed", "seed": True}, "reductions": []},
        {"pivot": 1, "lead": 0, "scale": 1,
         "origin": {"kind": "actor", "parent": 1, "letter": 1},
         "reductions": []},
        {"pivot": 1, "lead": 0, "scale": 1,
         "origin": {"kind": "projected_seed", "seed": 1},
         "reductions": [[1, 1]]},
        {"pivot": 1, "lead": 0, "scale": 1,
         "origin": {"kind": "projected_seed", "seed": 1},
         "reductions": [[0, 1], [0, 2]]},
    ):
        rejected += _expect_reject(lambda bad=bad: validate_node(
            bad, 1, 2, 4, {"projected_seed", "actor"}))
    rejected += _expect_reject(lambda: cache.append(
        tiny, np.zeros(3, dtype=np.uint8)))
    rejected += _expect_reject(lambda: cache.append(
        tiny, np.full(4, 3, dtype=np.uint8)))
    instructions = InstructionSink(cache_path.parent / "i.jsonl")
    instruction_unsigned = {
        "node": 0, "origin": {"kind": "projected_seed", "seed": 1},
        "reductions": [], "scale": 1, "raw_origin_sha256": "a" * 64,
        "raw_origin_components_sha256": {"p0": "b" * 64, "p1": "c" * 64,
                                          "p2": "d" * 64, "aux": "e" * 64},
        "literal_input_sha256": None,
        "old_defect_literal_input_sha256": None,
        "parent_row_sha256": [], "packet_sha256": None,
        "packet_row_sha256": None, "reduction_parent_sha256": [],
        "p1_sha256": "f" * 64, "offset": 0, "length": 1,
        "row_receipt": {"offset": 0, "length": 1,
                         "sha256": cache.row_sha(0)},
        "predecessor": (b"\0" * 32).hex(),
    }
    instruction_head = sha(b"\0" * 32 + canonical(instruction_unsigned))
    instruction_record = dict(instruction_unsigned)
    instruction_record["ancestry_sha256"] = instruction_head
    instructions.write(instruction_record)
    checkpoint(cache, instructions, "fixture", time.monotonic(),
               rss_reader=lambda: 7)
    instructions.close(); cache.close()
    receipt = instruction_receipt(
        instructions.path, 1, 1, cache.row_hashes, instruction_head,
        instructions.digest.hexdigest())
    require(receipt["final_lf"] and receipt["eof"], "fixture_instruction_eof")
    instruction_bytes = instructions.path.read_bytes()
    for label, mutated in (
        ("instruction_missing_lf", instruction_bytes[:-1]),
        ("instruction_wrong_count", instruction_bytes),
        ("instruction_bad_predecessor", instruction_bytes.replace(
            b'"predecessor":"0000000000000000000000000000000000000000000000000000000000000000"',
            b'"predecessor":"1111111111111111111111111111111111111111111111111111111111111111"')),
    ):
        altered_path = instructions.path.with_name(label + ".jsonl")
        altered_path.write_bytes(mutated)
        if label == "instruction_wrong_count":
            rejected += _expect_reject(lambda p=altered_path:
                                       instruction_receipt(p, 2, 1))
        else:
            rejected += _expect_reject(lambda p=altered_path:
                                       instruction_receipt(p, 1, 1))
    altered_value = dict(instruction_record)
    altered_value["ancestry_sha256"] = "1" * 64
    altered_path = instructions.path.with_name("instruction_bad_ancestry.jsonl")
    altered_path.write_bytes(canonical(altered_value))
    rejected += _expect_reject(lambda: instruction_receipt(altered_path, 1, 1))
    # Exact four-character P1/P0/aux flattening and cache EOF are exercised.
    rejected += _expect_reject(lambda: cache.row(tiny, 1))
    with tempfile.TemporaryDirectory(prefix="task746-source-pin-") as td:
        altered = Path(td) / "grade1.py"
        altered.write_bytes(G1_PATH.read_bytes() + b"\n")
        rejected += _expect_reject(lambda: load_exact(altered, G1_SHA,
                                                       "task746_bad_g1"))
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    calls = {call.func.attr if isinstance(call.func, ast.Attribute)
             else call.func.id for call in ast.walk(tree)
             if isinstance(call, ast.Call)
             and isinstance(call.func, (ast.Name, ast.Attribute))}
    require(not calls.intersection(FORBIDDEN), "forbidden_callable")
    rejected += _expect_reject(lambda: validate_actor_order(
        [1, 2, -1, -2], "fixture_actor_order"))
    print(json.dumps({
        "selftest": "PASS", "fixture_accept": accepted,
        "rejections": rejected, "full_projector_nonzero_p1": True,
        "all_four_actor_slots": True, "scale_two": True,
        "body_size_artifact_registry": True,
        "body_size_rejections": size_rejected,
        "authenticated_resume": True,
        "resume_fixture_accept": resume_accepted,
        "resume_fixture_rejections": resume_rejected,
        "cross_runner_fixture_accept": runner_accepted,
        "cross_runner_fixture_rejections": runner_rejected,
        "promotion_fixture_accept": promotion_accepted,
        "promotion_fixture_rejections": promotion_rejected,
        "semantic_checker_launch_validation": True,
        "forbidden_calls": sorted(calls.intersection(FORBIDDEN)),
        "actual_replay": "DEFERRED_TO_GHA", "verified": False,
    }, sort_keys=True, separators=(",", ":")), flush=True)


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true")
    modes.add_argument("--build", action="store_true")
    parser.add_argument("--prepare-root", type=Path)
    parser.add_argument("--block-roots", nargs=4, type=Path)
    parser.add_argument("--semantic-receipts", nargs=6, type=Path)
    parser.add_argument("--semantic-checker-result", type=Path)
    parser.add_argument("--semantic-checker-workflow-receipt", type=Path)
    parser.add_argument("--launch-manifest", type=Path)
    parser.add_argument("--staging", type=Path)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--resume-checkpoint", type=Path)
    parser.add_argument("--out", type=Path)
    return parser


def validate_cli(args: argparse.Namespace) -> None:
    if args.selftest:
        require(not any((args.prepare_root, args.block_roots,
                         args.semantic_receipts,
                         args.semantic_checker_result,
                         args.semantic_checker_workflow_receipt,
                         args.launch_manifest, args.staging, args.checkpoint,
                         args.resume, args.resume_checkpoint, args.out)),
                "selftest_arguments")
        return
    require(args.build and args.prepare_root is not None
            and args.block_roots is not None and len(args.block_roots) == 4
            and args.semantic_receipts is not None
            and len(args.semantic_receipts) == 6
            and args.semantic_checker_result is not None
            and args.semantic_checker_workflow_receipt is not None
            and args.launch_manifest is not None and args.staging is not None
            and (args.checkpoint is not None or
                 args.resume_checkpoint is not None)
            and args.out is not None,
            "build_arguments")


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        validate_cli(args)
        if args.selftest:
            selftest()
        else:
            build(args)
        return 0
    except ResourceStop as exc:
        print(json.dumps({"status": "UNKNOWN_RESOURCE", "error": str(exc),
                          "verified": False}, separators=(",", ":")),
              file=sys.stderr, flush=True)
        return 2
    except KeyboardInterrupt:
        print(json.dumps({"status": "UNKNOWN_RESOURCE",
                          "error": "UNKNOWN_RESOURCE:interrupt",
                          "verified": False}, separators=(",", ":")),
              file=sys.stderr, flush=True)
        return 2
    except Exception as exc:
        trace = traceback.format_exception(type(exc), exc, exc.__traceback__)
        bounded_trace = "".join(trace)[-8192:]
        print(json.dumps({"status": "REJECTED", "error": str(exc),
                          "phase": RUNTIME_PHASE,
                          "traceback_tail": bounded_trace,
                          "verified": False}, separators=(",", ":")),
              file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
