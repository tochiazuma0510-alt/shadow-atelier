#!/usr/bin/env python3
"""Helper-nonshared v12b checker for SELFTEST_BOOTSTRAP only.

The producer is authenticated as bytes but never imported.  This checker
independently reconstructs the finite owner summaries and ordinary mutation
validators; production and resume entry points do not exist in v12b.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import multiprocessing
import os
import socket
import stat
import struct
import sys
import tempfile
import time
import types
import zlib
from array import array
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-history-free-positive-fast-resume/v12b"
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint"
VERDICT_SCHEMA = SCHEMA + "/verdict"
CHECKER_PREFIX = "V12B_CHECKER_TERMINAL"
SELFTEST_TERMINAL = "V12B_SELFTEST_BOOTSTRAP_ARTIFACT"
MAX_CANDIDATE_BYTES = 512 * 1024 * 1024
MAX_CHECKPOINT_BYTES = 4_000_000_000
CHECKER_WALL_SECONDS = 5_400.0
CHECKER_ARTIFACT_SECONDS = 300.0
CHECKER_RSS_BYTES = 5_700_000_000
CHECKER_ALLOCATION_BYTES = 4_000_000_000
CHECKER_CHANNEL_SECONDS = 20.0
CHECKER_FRAME_BYTES = 32 * 1024 * 1024
OLD_PIVOT_ROWS_SHA256 = "3c645f4e352c96691dd35d6202bdf5f8b2cce73b7eb5f1bdf33a8daa06ce9d28"
OLD_SCHEMA = "d972-r07-normalized-exact-cached-colgen/v3"
OLD_SELF_DIGEST = "29bb74f3bd8048913a0365bc4c599f3731d32ba56967f3a238c7468b7fcfd123"
OLD_INPUT_SHA256 = "f29eaf9b945adb3bde89395ae9cb9018309fe8f3938d32f55e6716574b861cfb"
OLD_TARGET_SHA256 = "968f0b8325fa0e741e2c304bb940b96239c3e2d3226e0ca56f7d61a53dd0d82b"
OLD_DUAL_SHA256 = "0960259714fa94ddd89e2ac4f582f040942ab7bd258185c0448c133e50b00f0c"
OLD_NORMALIZED_DIGEST = "07c91e42c91648c5139ec13afd7fe0f44aff964612bae950d9dbd941b509b109"
CHECKER_DAG_NODE_CAP = 2_000_000
CHECKER_DAG_SUPPORT_CAP = 2_000_000
RAW_BYTES = 86_368_039
RAW_SHA256 = "c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab"
RAW_SOURCE_PATH = "ci/resume/d972_r07_history_free_positive_fast_resume_selftest_v12b.raw.json"
RAW_ARCHIVE_PATH = "ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip"
RAW_ARCHIVE_BYTES = 5_001_811
RAW_ARCHIVE_SHA256 = "f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566"
FIXTURE_PATH = "search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12b_20260829.json"
R_OUTPUT_PATH = "ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.receipt.json"
V_OUTPUT_PATH = "ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.verdict.json"
OUTPUT_SIBLINGS = (
    R_OUTPUT_PATH, V_OUTPUT_PATH,
    R_OUTPUT_PATH + ".checkpoint.json",
    R_OUTPUT_PATH.replace(".receipt.json", ".producer.log"),
    R_OUTPUT_PATH.replace(".receipt.json", ".checker.log"),
    R_OUTPUT_PATH.replace(".receipt.json", ".producer.terminal"),
    R_OUTPUT_PATH.replace(".receipt.json", ".checker.terminal"),
    R_OUTPUT_PATH.replace(".receipt.json", ".artifact.ok"),
)
FALSE_CLAIMS = {"common_word": False, "finite_common_word": False,
                "separator": False, "negative": False, "cofinal_lift": False,
                "fake": False, "ihara_witness": False}

_FIXTURE_SNAPSHOT: dict[str, Any] | None = None
CHECKER_RESOURCE_MODEL = {
    "platform": "ubuntu-24.04-x86_64-cpython3.13-linux-fork-af_unix",
    "raw_checkpoint": "single physical read; bytearray+bytes+ASCII+DOM then release",
    "task176_decoded_stream_bytes": 60_492_663,
    "selected_k0_max_payload": 243_105_472,
    "triangular_mutations": "one raw baseline; three-record reset; no full-frame clone",
    "receipt_verdict": "one borrowed R DOM; shallow mutant carrier; R raw released before V construction; V output pre-reserved",
    "physical_mutation_peak": "one borrowed R DOM plus one mutant/raw/DOM; cases sequential",
    "publication_hard_cap_bytes": MAX_CANDIDATE_BYTES,
    "conservative_live_peak_formula": "1185941203 raw/K0/decoded/V-reserve bytes + 3414058797 CPython/R-mutation reserve = 4600000000",
    "conservative_live_peak_bytes": 4_600_000_000,
    "rss_hard_cap_bytes": CHECKER_RSS_BYTES,
    "rss_margin_bytes": 1_100_000_000,
    "simultaneous_child_peak": 4,
}

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
    "task176_checker": ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980,
                         "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"),
    "task176_reply": ("sol/luna_reply_176_r07_all_seven_extension_section_census_v1.md", 47164,
                       "aa173122310e33910d546bd3e02a98a6bf16aea9d3aad066b7d49976098ebb0c"),
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
    "fixture": (FIXTURE_PATH, 23679,
                "64a7dd14e26431387f6ff1dd71aad6d977a5db943c4ca42c01fb19477f3a3ddb"),
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

class CheckStop(RuntimeError):
    pass


class CheckerMeter:
    """Fail-closed checker wall/RSS/allocation envelope.

    The meter is diagnostic-only and is never serialized into candidate V;
    deterministic counters are kept separately from host telemetry.
    """
    def __init__(self) -> None:
        self.started = time.monotonic()
        self.allocated = 0
        self.stage = "checker_start"
        self.sampled_parent_rss_peak = 0
        self.sampled_children_rss_peak_sum = 0

    @staticmethod
    def rss_bytes(pid: int | None = None) -> int:
        try:
            target = "self" if pid is None else str(int(pid))
            with open("/proc/" + target + "/statm", "r", encoding="ascii") as stream:
                pages = int(stream.read().split()[1])
            return pages * int(os.sysconf("SC_PAGE_SIZE"))
        except (OSError, ValueError, IndexError):
            return 0

    def check(self, stage: str, child_pids: Sequence[int] = ()) -> None:
        self.stage = str(stage)
        elapsed = time.monotonic() - self.started
        if elapsed > CHECKER_WALL_SECONDS:
            raise CheckStop("checker wall_seconds:" + self.stage)
        parent = self.rss_bytes()
        children = sum(self.rss_bytes(int(pid)) for pid in child_pids)
        self.sampled_parent_rss_peak = max(self.sampled_parent_rss_peak, parent)
        self.sampled_children_rss_peak_sum = max(
            self.sampled_children_rss_peak_sum, children)
        rss = parent + children
        if rss and rss > CHECKER_RSS_BYTES:
            raise CheckStop("checker rss_bytes:" + self.stage)

    def reserve(self, amount: int, stage: str) -> None:
        amount = int(amount)
        if amount < 0 or self.allocated + amount > CHECKER_ALLOCATION_BYTES:
            raise CheckStop("checker allocation_bytes:" + str(stage))
        self.allocated += amount
        self.check(stage)


def checker_meter_check(runtime: dict[str, Any] | None, stage: str) -> None:
    meter = runtime.get("_checker_meter") if isinstance(runtime, dict) else None
    if isinstance(meter, CheckerMeter):
        meter.check(stage)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckStop(message)


def checker_validator_event(runtime: dict[str, Any] | None,
                            validator: str, stage: str, owner: str) -> None:
    """Append an entry at the ordinary validator's actual entry point."""
    if runtime is not None:
        events = runtime.setdefault("_active_validator_events", [])
        events.append({
            "validator": validator, "stage": stage, "owner": owner})
        projection = runtime.get("_physical_projection")
        if isinstance(projection, dict):
            projection["entered_validators"] = [event["validator"]
                                                 for event in events]
            projection["event_trace_digest"] = sha_obj(events)


def _checker_capture_physical_projection(runtime: dict[str, Any], *,
                                         before: Any, after: Any,
                                         path_after: Any, raw: bytes | None,
                                         reason: str | None) -> None:
    """Construct v298 projection only after raw handle/path checks completed."""
    marker = "UNREADABLE_AT_REGISTERED_STAGE"
    label = str(runtime.get("_physical_logical_label", "candidate.path"))
    if path_after is not None and stat.S_ISLNK(path_after.st_mode):
        owner_kind = "symlink"; symlink = True
    elif before is not None and stat.S_ISREG(before.st_mode):
        owner_kind = "regular"; symlink = False
    elif before is None:
        owner_kind = "missing"; symlink = False
    else:
        owner_kind = "other"; symlink = False
    readable = raw is not None and len(raw) > 0
    content_sha = sha_bytes(raw) if readable else marker
    before_links = None if before is None else int(before.st_nlink)
    after_links = None if after is None else int(after.st_nlink)
    stable = bool(before is not None and after is not None and
                  (before.st_dev, before.st_ino, before.st_size, before.st_nlink,
                   before.st_mtime_ns) ==
                  (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
                   after.st_mtime_ns))
    pathname_equal = bool(path_after is not None and after is not None and
                          not stat.S_ISLNK(path_after.st_mode) and
                          (path_after.st_dev, path_after.st_ino,
                           path_after.st_size, path_after.st_nlink,
                           path_after.st_mtime_ns) ==
                          (after.st_dev, after.st_ino, after.st_size,
                           after.st_nlink, after.st_mtime_ns))
    baseline_sha = runtime.get("_physical_baseline_sha256")
    if baseline_sha is None and readable:
        baseline_sha = content_sha
    projection = {
        "logical_case_path": label, "owner_kind": owner_kind,
        "byte_length": len(raw) if readable else marker,
        "content_sha256": content_sha,
        "link_count_before": before_links, "link_count_after": after_links,
        "symlink_or_reparse": symlink,
        # Link targets are projected only for link/reparse owners.  Regular
        # semantic rows remain comparable to their baseline independent of
        # the temporary path used by the experiment.
        "logical_link_target": runtime.get("_physical_logical_link_target")
        if symlink else None,
        "single_open_handle": before is not None,
        "opened_handle_stable": stable,
        "pathname_matches_opened_handle": pathname_equal,
        "substitution_detected": reason in (
            "physical pathname substituted", "physical pathname identity") or (
                path_after is not None and after is not None and
                not pathname_equal),
        "canonical_before_sha256": baseline_sha or marker,
        "canonical_after_sha256": content_sha,
        "resealed_logical_nodes": [],
        "entered_validators": [event["validator"] for event in
                               runtime.get("_active_validator_events", [])],
        "event_trace_digest": sha_obj(runtime.get(
            "_active_validator_events", [])),
        "first_typed_rejection": reason,
    }
    runtime["_physical_projection"] = projection


def _checker_physical_projection_reason(runtime: dict[str, Any],
                                        reason: str) -> None:
    projection = runtime.get("_physical_projection")
    if isinstance(projection, dict):
        projection["first_typed_rejection"] = reason
        projection["entered_validators"] = [event["validator"]
                                             for event in runtime.get(
                                                 "_active_validator_events", [])]
        projection["event_trace_digest"] = sha_obj(runtime.get(
            "_active_validator_events", []))


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
    # Literal DAG operands are JSON lists; canonical bytes keep deduplication
    # type-aware without relying on an unhashable tuple conversion.
    seen: set[bytes] = set()
    for index, raw in enumerate(nodes):
        require(type(raw) is list and raw, "DAG node shape")
        node = tuple(raw); opcode = node[0]
        node_key = canonical(raw)
        require(node_key not in seen, "DAG hash-cons duplicate")
        seen.add(node_key)
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


def read_owner_bytes(path: Path, size: int, digest: str,
                     meter: CheckerMeter | None = None) -> tuple[bytes, dict[str, Any]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise CheckStop("owner open") from exc
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                before.st_size == size, "owner physical identity")
        if meter is not None:
            # The bytearray and immutable bytes conversion are both live at
            # the hand-off; reserve before creating either large object.
            meter.reserve(size * 2, "owner_read:" + path.name)
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
    def __init__(self, snapshots: dict[str, bytes]) -> None:
        self.raw: dict[str, bytes] = dict(snapshots)
        self.modules: dict[str, Any] = {}
        self.objects: dict[str, Any] = {}

    def authenticate(self, meter: CheckerMeter | None = None) -> None:
        require(set(self.raw) == set(SOURCE_PINS),
                "checker shared source snapshot roster")
        for key, (_relative, size, digest) in SOURCE_PINS.items():
            raw = self.raw[key]
            require(len(raw) == size and sha_bytes(raw) == digest,
                    "checker shared source snapshot:" + key)

    def load(self, key: str) -> Any:
        if key in self.modules:
            return self.modules[key]
        name = "_d972_v12b_checker_" + key
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

    def release_snapshots(self) -> dict[str, int]:
        result = {"raw_byte_owners": len(self.raw),
                  "json_doms": len(self.objects)}
        self.raw.clear(); self.objects.clear()
        return result


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
                "checker": {"bytes": SOURCE_PINS["task176_checker"][1],
                    "path": SOURCE_PINS["task176_checker"][0],
                    "sha256": SOURCE_PINS["task176_checker"][2]}} and
            recovery.get("archive_sha256") ==
                "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912" and
            recovery.get("artifact_id") == "9635036013" and
            recovery.get("artifact_name") == "gap-run-out" and
            recovery.get("head") == "0533e42019c9f67f6cec3d1566152db17b903836" and
            recovery.get("run") == "33044121344" and
            recovery.get("hashes_file") == {"bytes": 261,
                "path": "d972_r07_all_seven_extension_section_census_hashes_v1.txt",
                "sha256": "c7cc68fd3e57e42fa03c85190c3c85f10f41b368d4a0182b0c25711fe36b933a"} and
            recovery.get("task176_reply") == {
                "bytes": SOURCE_PINS["task176_reply"][1],
                "path": SOURCE_PINS["task176_reply"][0],
                "sha256": SOURCE_PINS["task176_reply"][2]} and
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


def decode_task176_owners(sources: Sources,
                          meter: CheckerMeter | None = None) -> dict[str, Any]:
    receipt = sources.json("task176_receipt")
    decoded: dict[str, Any] = {"receipt": receipt}
    for name, (_root, section, field, raw_limit, width, count) in TASK176_BLOBS.items():
        owner = receipt["result"][section][field]
        if meter is not None:
            # Reserve the decoded stream before zlib allocates it.  The
            # metadata itself is authenticated above by the physical receipt.
            meter.reserve(int(owner.get("raw_bytes", raw_limit)) * 2,
                          "task176_decode:" + name)
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
                set(row) == set(range(1, 37)) for row in q3_marks),
            "q3 Q0 marked permutation owner")
    decoded["q0_marked_permutations"] = tuple(
        bytes(int(value) - 1 for value in row) for row in q3_marks)
    decoded["q0_marked_permutations_literal_rows"] = tuple(
        tuple(int(value) for value in row) for row in q3_marks)
    return decoded


def _checker_owner_meta(owner: dict[str, Any], label: str) -> dict[str, Any]:
    """Project one decoded task176 blob to stable typed owner metadata."""
    require(type(owner) is dict and owner.get("codec") == "zlib+base64" and
            type(owner.get("raw_bytes")) is int and owner["raw_bytes"] > 0 and
            type(owner.get("compressed_bytes")) is int and
            owner["compressed_bytes"] > 0 and
            type(owner.get("raw_sha256")) is str and
            len(owner["raw_sha256"]) == 64 and
            type(owner.get("compressed_sha256")) is str and
            len(owner["compressed_sha256"]) == 64 and
            type(owner.get("record_count")) is int and
            type(owner.get("record_width_bytes")) is int and
            owner["raw_bytes"] == owner["record_count"] *
                owner["record_width_bytes"],
            "checker task176 owner metadata:" + label)
    return {"codec": owner["codec"], "raw_bytes": owner["raw_bytes"],
            "raw_sha256": owner["raw_sha256"],
            "compressed_bytes": owner["compressed_bytes"],
            "compressed_sha256": owner["compressed_sha256"],
            "record_count": owner["record_count"],
            "record_width_bytes": owner["record_width_bytes"]}


def checker_build_owner_preselection(sources: Sources,
                                     runtime: dict[str, Any]) -> dict[str, Any]:
    """Independently construct the v299 load-bearing OwnerPre.

    This is deliberately a checker-local constructor.  It consumes the
    authenticated task176 receipt/manifest/crosscheck/recovery-v2 and decoded
    owner metadata, never R's ``heavy_public`` or a producer helper.  The
    selected physical Q0/Gamma/K0/dual/code state enters later through Sel(r).
    """
    receipt = sources.json("task176_receipt")
    manifest = sources.json("task176_manifest")
    crosscheck = sources.json("task176_crosscheck")
    recovery_v1 = sources.json("task176_recovery")
    recovery_v2 = sources.json("task176_recovery_v2")
    require(receipt.get("schema") ==
            "d972-r07-all-seven-extension-section-census/v1" and
            receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") ==
            "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS" and
            receipt.get("self_digest_sha256") == TASK176_RECEIPT_DIGEST,
            "checker OwnerPre receipt authority")
    require(manifest == {"artifact_id": "9635036013", "head":
            "0533e42019c9f67f6cec3d1566152db17b903836", "member":
            "d972_r07_all_seven_extension_section_census_v1.json",
            "member_bytes": 13649089, "member_sha256":
            SOURCE_PINS["task176_receipt"][2], "run": "33044121344",
            "zip_sha256": "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912"},
            "checker OwnerPre manifest authority")
    require(crosscheck.get("schema") ==
            "d972-r07-all-seven-extension-section-census-check/v1" and
            crosscheck.get("grade") == "CROSS_CHECKED" and
            crosscheck.get("producer_sha256") == SOURCE_PINS["task176"][2] and
            crosscheck.get("receipt_sha256") == SOURCE_PINS["task176_receipt"][2] and
            crosscheck.get("receipt_terminal") == receipt["terminal"],
            "checker OwnerPre crosscheck authority")
    require(recovery_v1.get("schema") ==
            "d972-r07-all-seven-extension-section-census-recovery-manifest/v1" and
            recovery_v1.get("self_digest_sha256") == TASK176_RECOVERY_V1_DIGEST,
            "checker OwnerPre recovery-v1 authority")
    require(recovery_v2.get("schema") ==
            "d972-r07-all-seven-extension-section-census-recovery-manifest/v2" and
            recovery_v2.get("self_digest_sha256") == TASK176_RECOVERY_V2_DIGEST and
            recovery_v2.get("execution") == "UNEXECUTED" and
            recovery_v2.get("mathematical_grade_change") is False,
            "checker OwnerPre recovery-v2 authority")
    result = receipt.get("result")
    require(type(result) is dict and type(result.get("Q0_section")) is dict and
            type(result.get("Gamma")) is dict and
            type(result.get("A_families")) is dict and
            type(result.get("families")) is dict and
            type(result.get("word_generators")) is dict,
            "checker OwnerPre result roster")
    q0 = result["Q0_section"]; gamma = result["Gamma"]
    marked = q0.get("ten_coordinate_marked_generator_blobs_hex")
    require(type(marked) is list and len(marked) == 10 and
            all(type(row) is list and len(row) == 2 and
                all(type(blob) is str and len(bytes.fromhex(blob)) in (40, 154)
                    for blob in row) for row in marked),
            "checker OwnerPre marked generators")
    require(int(q0.get("order")) == K0_STATE_COUNT and
            int(gamma.get("order")) == 243 and
            len(gamma.get("record_words", [])) == 26,
            "checker OwnerPre cardinality")
    q0_owner = {"order": int(q0["order"]),
        "canonical_roster": _checker_owner_meta(q0["canonical_roster"],
            "Q0.roster"),
        "parents": _checker_owner_meta(q0["parent_states_u32le"],
            "Q0.parents"),
        "letters": _checker_owner_meta(q0["parent_letters_u8"],
            "Q0.letters"),
        "marked_generators": {"count": len(marked),
            "sha256": sha_obj(marked)},
        "complete_presentation_relators_sha256":
            q0["complete_presentation_relators_sha256"]}
    gamma_owner = {"order": int(gamma["order"]),
        "ten_coordinate_states": _checker_owner_meta(
            gamma["ten_coordinate_states"], "Gamma.states"),
        "parents": _checker_owner_meta(gamma["section_parent_states_u16le"],
            "Gamma.parents"),
        "records": _checker_owner_meta(gamma["section_parent_record_u8"],
            "Gamma.records"),
        "record_words": {"count": len(gamma["record_words"]),
            "sha256": sha_obj(gamma["record_words"])} }
    decoded = runtime.get("task176_owners")
    require(type(decoded) is dict, "checker OwnerPre decoded owner store")
    decoded_rows = {
        "canonical_roster": (decoded.get("q0_roster"),
                              q0_owner["canonical_roster"]),
        "q0_parents": (decoded.get("q0_parents"), q0_owner["parents"]),
        "q0_letters": (decoded.get("q0_letters"), q0_owner["letters"]),
        "gamma_states": (decoded.get("gamma_states"),
                          gamma_owner["ten_coordinate_states"]),
        "gamma_parents": (decoded.get("gamma_parents"),
                           gamma_owner["parents"]),
        "gamma_records": (decoded.get("gamma_records"),
                           gamma_owner["records"])}
    for label, (raw, metadata) in decoded_rows.items():
        require(type(raw) is bytes and len(raw) == metadata["raw_bytes"] and
                sha_bytes(raw) == metadata["raw_sha256"] and
                metadata["raw_bytes"] == metadata["record_count"] *
                metadata["record_width_bytes"],
                "checker OwnerPre decoded stream binding:" + label)
    family_owners: list[dict[str, Any]] = []
    family_order = ["ALL"] + ["S" + str(index) for index in range(10)]
    for name in family_order:
        family = result["families"].get(name)
        A = result["A_families"].get(name)
        words = result["word_generators"].get(name)
        require(type(family) is dict and type(A) is dict and
                type(words) is dict, "checker OwnerPre family:" + name)
        family_owners.append({"name": name,
            "coordinate_indices": [int(value) for value in
                                    family["coordinate_indices"]],
            "A_order": int(family["A_order"]),
            "L_order": int(family["L_order"]),
            "membership_bitset_metadata": _checker_owner_meta(
                family["membership_bitset"], name + ".membership"),
            "A_literal_table_sha256": A["literal_table_sha256"],
            "canonical_word_generator_digest": sha_obj(words)})
    chain_keys = ("task176", "task176_checker", "task176_reply",
                  "task176_receipt", "task176_manifest", "task176_crosscheck",
                  "task176_recovery", "task176_recovery_v2")
    physical_chain = {key: {"path": SOURCE_PINS[key][0],
        "bytes": SOURCE_PINS[key][1], "sha256": SOURCE_PINS[key][2]}
        for key in chain_keys}
    physical_chain["task176_receipt"]["self_digest_sha256"] = receipt[
        "self_digest_sha256"]
    physical_chain["task176_recovery_v2"]["self_digest_sha256"] = recovery_v2[
        "self_digest_sha256"]
    owner = {"schema": "r07-a0-checker-local-preselection/v1",
        "physical_chain": physical_chain, "q0_owner": q0_owner,
        "gamma_owner": gamma_owner, "family_owners": family_owners,
        "deletion_owner_sha256": sha_obj(result["deletion"]),
        "primitive_registry": {key: {"path": row[0], "bytes": row[1],
            "sha256": row[2]} for key, row in sorted(SOURCE_PINS.items())},
        "algorithms": {"task176_decoder":
            "zlib+base64-lossless-bounded-decode-v1",
            "selected_k0": "v12b-coarse-open-address-retained-full-state-first-gid-bfs",
            "canonical_json": "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=True)",
            "digest_framing": "sha256(canonical(value))"}}
    require(owner["q0_owner"]["canonical_roster"]["record_count"] ==
            K0_STATE_COUNT, "checker OwnerPre decoded Q0 roster")
    runtime["owner_preselection"] = owner
    runtime["owner_preselection_sha256"] = sha_obj(owner)
    return owner


def checker_recovery_public(sources: Sources) -> dict[str, Any]:
    recovery_v1 = sources.json("task176_recovery")
    recovery_v2 = sources.json("task176_recovery_v2")
    return {"v1": {"path": SOURCE_PINS["task176_recovery"][0],
                    "bytes": SOURCE_PINS["task176_recovery"][1],
                    "sha256": SOURCE_PINS["task176_recovery"][2],
                    "self_digest_sha256": recovery_v1.get("self_digest_sha256")},
            "v2": {"path": SOURCE_PINS["task176_recovery_v2"][0],
                    "bytes": SOURCE_PINS["task176_recovery_v2"][1],
                    "sha256": SOURCE_PINS["task176_recovery_v2"][2],
                    "self_digest_sha256": recovery_v2.get("self_digest_sha256"),
                    "correction": recovery_v2.get("correction")}}


def checker_q0_parent_letter_digest(owners: dict[str, Any]) -> str:
    """Canonical digest of the raw chronological Q0 parent/letter arrays."""
    cached = owners.get("_q0_parent_letter_digest")
    if isinstance(cached, str):
        return cached
    count = 1_469_664
    parents = [struct.unpack_from("<I", owners["q0_parents"], index * 4)[0]
               for index in range(count)]
    letters = list(owners["q0_letters"])
    result = sha_obj([parents, letters])
    owners["_q0_parent_letter_digest"] = result
    return result


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
    return bytes(right[index] for index in left)


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
                  mutation_hook: Any | None = None,
                  trace_runtime: dict[str, Any] | None = None,
                  meter: CheckerMeter | None = None
                  ) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
    before = None
    after = None
    path_after = None
    raw = bytearray()
    owner = "candidate.path" if trace_runtime is None else str(
        trace_runtime.get("_physical_logical_label", "candidate.path"))
    checker_validator_event(trace_runtime, "physical_owner_open", "physical_open",
                            owner)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        if trace_runtime is not None:
            try:
                failed_path = os.lstat(path)
            except OSError:
                failed_path = None
            _checker_capture_physical_projection(
                trace_runtime, before=None, after=None, path_after=failed_path,
                raw=None, reason="physical open")
            trace_runtime["_last_owner_disposed"] = True
        raise CheckStop("physical open") from exc
    try:
        try:
            before = os.fstat(fd)
            if trace_runtime is not None:
                checker_validator_event(trace_runtime, "physical_owner_open",
                                        "unique_link", owner)
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                    0 < before.st_size <= maximum, "physical regular unique owner")
            if expected is not None:
                require(before.st_size == expected["bytes"], "physical expected size")
            if meter is not None:
                meter.reserve(before.st_size * 2, "physical_read:" + path.name)
            if mutation_hook is not None:
                mutation_hook(path)
            while len(raw) < before.st_size:
                chunk = os.read(fd, min(1 << 20, before.st_size - len(raw)))
                require(bool(chunk), "physical short read")
                raw.extend(chunk)
            require(not os.read(fd, 1), "physical long read")
            after = os.fstat(fd)
            if trace_runtime is not None:
                checker_validator_event(trace_runtime, "physical_owner_open",
                                        "fd_TOCTOU", owner)
            require((before.st_dev, before.st_ino, before.st_size, before.st_nlink,
                     before.st_mtime_ns) ==
                    (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
                     after.st_mtime_ns), "physical fd TOCTOU")
            try:
                path_after = os.lstat(path)
            except OSError as exc:
                raise CheckStop("physical pathname substituted") from exc
            if trace_runtime is not None:
                checker_validator_event(trace_runtime, "physical_owner_open",
                                        "pathname_identity", owner)
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
            if trace_runtime is not None:
                _checker_capture_physical_projection(
                    trace_runtime, before=before, after=after,
                    path_after=path_after, raw=raw_bytes, reason=None)
            return value, raw_bytes, {"device": before.st_dev, "inode": before.st_ino,
                "bytes": before.st_size, "links": before.st_nlink,
                "mtime_ns": before.st_mtime_ns, "sha256": digest,
                "single_fd": True, "no_follow": True}
        except CheckStop as exc:
            if trace_runtime is not None:
                _checker_capture_physical_projection(
                    trace_runtime, before=before, after=after,
                    path_after=path_after, raw=bytes(raw) or None,
                    reason=str(exc))
            raise
    finally:
        os.close(fd)
        if trace_runtime is not None:
            trace_runtime["_last_owner_disposed"] = True


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


class CheckerLinearReducer:
    """Checker-local chronological reducer with one linear DAG expansion."""
    def __init__(self) -> None:
        self.rows: dict[bytes, Sparse] = {}
        self.order: list[bytes] = []
        self.nodes: list[tuple[Any, ...]] = [("zero",)]
        self.expr: dict[bytes, int] = {}

    def _node(self, value: tuple[Any, ...]) -> int:
        require(len(self.nodes) < CHECKER_DAG_NODE_CAP,
                "checker DAG node cap")
        self.nodes.append(value)
        return len(self.nodes) - 1

    def literal(self, expression: dict[str, int]) -> int:
        return self._node(("literal", tuple(sorted((str(key), int(value) % 3)
            for key, value in expression.items() if int(value) % 3))))

    def add_node(self, left: int, right: int, coefficient: int) -> int:
        coefficient %= 3
        if not coefficient or right == 0:
            return left
        return self._node(("add", int(left), int(right), coefficient))

    def expand(self, root: int) -> dict[str, int]:
        require(0 <= int(root) < len(self.nodes), "checker DAG root")
        weights: dict[int, int] = {int(root): 1}
        answer: dict[str, int] = {}
        for current in range(int(root), -1, -1):
            scalar = weights.pop(current, 0)
            if not scalar:
                continue
            item = self.nodes[current]
            if item[0] == "literal":
                for key, coefficient in item[1]:
                    value = (answer.get(key, 0) + scalar * coefficient) % 3
                    if value:
                        require(key in answer or len(weights) + len(answer) <
                                CHECKER_DAG_SUPPORT_CAP,
                                "checker DAG aggregate live-entry cap")
                        answer[key] = value
                    else:
                        answer.pop(key, None)
            elif item[0] == "add":
                for child, coefficient in ((item[1], scalar),
                        (item[2], scalar * item[3])):
                    value = (weights.get(child, 0) + coefficient) % 3
                    if value:
                        require(child in weights or len(weights) + len(answer) <
                                CHECKER_DAG_SUPPORT_CAP,
                                "checker DAG aggregate live-entry cap")
                        weights[child] = value
                    else:
                        weights.pop(child, None)
        return answer

    def inject(self, pivot: bytes, row: Sparse, expression_node: int) -> None:
        require(row and min(row) == pivot and row[pivot] == 1 and
                pivot not in self.rows, "checker chronological injection")
        self.rows[pivot] = dict(row)
        self.order.append(pivot)
        self.expr[pivot] = int(expression_node)

    def reduce(self, source: Sparse, node: int = 0) -> tuple[Sparse, int]:
        row = dict(source)
        for pivot in self.order:
            coefficient = row.get(pivot, 0)
            if coefficient:
                add_scaled(row, self.rows[pivot], -coefficient)
                node = self.add_node(node, self.expr[pivot], coefficient)
        return row, node

    def exact_dual(self, target: Sparse) -> tuple[Sparse, Sparse, int]:
        remainder, solution = self.reduce(target)
        require(bool(remainder), "checker target already in basis")
        dual: Sparse = {min(remainder): 1}
        for pivot in reversed(self.order):
            value = -sum(coefficient * dual.get(key, 0)
                         for key, coefficient in self.rows[pivot].items()
                         if key != pivot) % 3
            if value:
                dual[pivot] = value
            else:
                dual.pop(pivot, None)
        require(all(pair(dual, self.rows[pivot]) == 0 for pivot in self.order) and
                pair(dual, target) in (1, 2) and
                pair(dual, target) == pair(dual, remainder),
                "checker reconstructed current dual")
        return dual, remainder, solution

    def add_actual(self, source: Sparse, symbol: str) -> tuple[bytes, int]:
        literal = self.literal({symbol: 1})
        row, node = self.reduce(source, literal)
        require(bool(row), "checker selected row dependent")
        pivot = min(row); inverse = 1 if row[pivot] == 1 else 2
        row = scaled(row, inverse)
        if inverse != 1:
            node = self.add_node(0, node, inverse)
        self.inject(pivot, row, node)
        return pivot, node


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


def checker_full_gamma_diagnostic(runtime: dict[str, Any], state: Any) -> bytes:
    """Checker-local codec for E3 x E4^31 JointGroup states."""
    require(type(state) is tuple and len(state) == 2 and
            type(state[1]) is tuple and len(state[1]) == 31,
            "checker full Gamma JointGroup shape")
    pieces = [checker_packed_joint_blob(state[0],
        "checker full Gamma E3 factor")]
    pieces.extend(checker_packed_joint_blob(value,
        "checker full Gamma E4 factor") for value in state[1])
    widths = [len(value) for value in pieces]
    require(widths == [40] + [154] * 31 and sum(widths) == 4814,
            "checker full Gamma JointGroup codec")
    return b"".join(pieces)


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
KERNEL_ORDERS = [9, 9, 9, 9, 9, 1, 1, 1, 3, 3]
K0_INVERSE_MAX_BYTES = 256 * 1024 * 1024
DELTA_ORDER = 357_128_352
K0_CAPACITY = 1 << 22
K0_STATE_COUNT = 1_469_664


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
            pairs.append((descriptor, g_raw, blob(runtime, translation),
                          lambda_coefficient))
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
    worker_contributors: list[dict[tuple[int, bytes, int],
                                   list[dict[str, Any]]]] = []
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
        contributor_map: dict[tuple[int, bytes, int],
                              list[dict[str, Any]]] = {}
        for descriptor, g_raw, translation_raw, lambda_coefficient in pairs[start:stop]:
            key = (descriptor["block"], translation_raw, descriptor["relator"])
            contributor_map.setdefault(key, []).append({
                "component": descriptor["component"], "g_hex": g_raw.hex(),
                "h_hex": descriptor["h_blob"].hex(),
                "lambda_coefficient": lambda_coefficient,
                "base_coefficient": descriptor["base_coefficient"]})
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
        worker_contributors.append(contributor_map)
    selected = min(total) if total else None
    selected_public = None if selected is None else [
        selected[0], selected[1].hex(), selected[2]]
    selected_contributors: list[dict[str, Any]] = []
    contributor_result_digests = []
    for worker_id, contributor_map in enumerate(worker_contributors):
        rows = [] if selected is None else contributor_map.get(selected, [])
        selected_contributors.extend(rows)
        reply = {"kind": "CONTRIBUTORS", "epoch": epoch,
                 "worker_id": worker_id, "selected": selected_public,
                 "rows": rows}
        contributor_result_digests.append(sha_obj(reply))
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
        "selected": selected_public,
        "selected_scalar": None if selected is None else total[selected],
        "selected_contributors": selected_contributors,
        "contributor_result_digests": contributor_result_digests,
        "zero_complete": selected is None, "result_digests": result_digests,
        "worker_results": worker_results}
    if epoch == 1 and len(dual) == 1188:
        require(support["entry_count"] == 1188 and support["types"] == [[1, 1]] and
                len(descriptor_ids) == 4 and len(pairs) == 4752,
                "checker pinned first epoch")
        answer["pinned_first_epoch"] = True
    return answer


def _checker_boundary_wire_rows(runtime: dict[str, Any], dual: Sparse,
                                workers: int) -> tuple[list[list[list[Any]]],
                                                        list[list[int]]]:
    """Build the exact bounded IPC slices for the checker process owner.

    This is deliberately separate from ``independent_boundary_outcome``:
    the child receives typed term rows and recomputes each worker accumulator,
    rather than returning a parent-computed declaration.
    """
    descriptors, lookup = checker_descriptors(runtime)
    support = dual_support(runtime, dual)
    descriptor_ids = sorted(index for key in support["private"]
                            for index in lookup.get(key, ()))
    pairs: list[tuple[dict[str, Any], bytes, int]] = []
    for descriptor_id in descriptor_ids:
        descriptor = descriptors[descriptor_id]
        for g_raw, lambda_coefficient, g in support["private"].get(
                (descriptor["block"], descriptor["component"]), ()):
            quotient = group_for(runtime, descriptor["block"])
            translation = quotient.mul(g, descriptor["h_inverse"])
            require(quotient.mul(translation, descriptor["h"]) == g,
                    "checker process t*h=g")
            pairs.append((descriptor, blob(runtime, translation),
                          lambda_coefficient))
    intervals = [[len(pairs) * index // workers,
                  len(pairs) * (index + 1) // workers]
                 for index in range(workers)]
    slices: list[list[list[Any]]] = []
    for start, stop in intervals:
        rows = []
        for descriptor, translation_raw, lambda_coefficient in pairs[start:stop]:
            coefficient = (int(descriptor["base_coefficient"]) *
                           int(lambda_coefficient)) % 3
            if coefficient:
                rows.append([descriptor["block"], translation_raw.hex(),
                             descriptor["relator"], coefficient])
        require(len(rows) == stop - start,
                "checker process wire slice cardinality")
        slices.append(rows)
    return slices, intervals


def _checker_wire_send(sock: socket.socket, value: dict[str, Any],
                       deadline: float) -> None:
    raw = canonical(value)
    require(len(raw) <= CHECKER_FRAME_BYTES, "checker process frame cap")
    sock.settimeout(max(0.0, deadline - time.monotonic()))
    sock.sendall(struct.pack(">I", len(raw)) + raw)


def _checker_wire_recv(sock: socket.socket, deadline: float) -> dict[str, Any]:
    def receive(size: int) -> bytes:
        parts: list[bytes] = []
        remaining = size
        while remaining:
            sock.settimeout(max(0.0, deadline - time.monotonic()))
            part = sock.recv(remaining)
            if not part:
                raise EOFError("checker process peer closed")
            parts.append(part); remaining -= len(part)
        return b"".join(parts)
    header = receive(4)
    size = struct.unpack(">I", header)[0]
    if size > CHECKER_FRAME_BYTES:
        raise CheckStop("checker process frame cap")
    try:
        value = json.loads(receive(size).decode("ascii"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CheckStop("checker process frame JSON") from exc
    require(type(value) is dict, "checker process frame object")
    return value


def _checker_process_worker(sock: socket.socket, worker_id: int,
                            fault: str | None) -> None:
    """Bounded persistent checker worker used only by SELFTEST_BOOTSTRAP."""
    try:
        while True:
            message = _checker_wire_recv(sock,
                                         time.monotonic() + CHECKER_CHANNEL_SECONDS)
            kind = message.get("kind")
            if kind == "STOP":
                _checker_wire_send(sock, {"kind": "STOPPED",
                    "worker_id": worker_id},
                    time.monotonic() + CHECKER_CHANNEL_SECONDS)
                return
            require(kind == "EPOCH" and message.get("worker_id") == worker_id,
                    "checker process epoch owner")
            if fault == "death" and worker_id == 0:
                return
            if fault == "timeout" and worker_id == 0:
                sock.settimeout(CHECKER_CHANNEL_SECONDS)
                try:
                    sock.recv(1)
                except (socket.timeout, EOFError, OSError):
                    return
            rows = message.get("rows")
            require(type(rows) is list and all(
                type(row) is list and len(row) == 4 for row in rows),
                "checker process typed rows")
            local: dict[tuple[int, bytes, int], int] = {}
            for block, raw_hex, relator, coefficient in rows:
                raw = bytes.fromhex(str(raw_hex))
                key = (int(block), raw, int(relator))
                value = (local.get(key, 0) + int(coefficient)) % 3
                if value:
                    local[key] = value
                else:
                    local.pop(key, None)
            accumulator = [[block, raw.hex(), relator,
                            local[(block, raw, relator)]]
                           for block, raw, relator in sorted(local)]
            result = {"kind": "RESULT", "epoch": message["epoch"],
                "worker_id": worker_id, "interval": message["interval"],
                "local_interval": [0, len(rows)],
                "slice_sha256": message["slice_sha256"],
                "attempted": len(rows), "accumulator": accumulator,
                "complete": True}
            if fault == "partial" and worker_id == 0:
                result["complete"] = False
            result["result_sha256"] = sha_obj(result)
            _checker_wire_send(sock, result,
                               time.monotonic() + CHECKER_CHANNEL_SECONDS)
    except (CheckStop, EOFError, OSError, socket.timeout):
        return
    finally:
        try:
            sock.close()
        except OSError:
            pass


def _checker_no_drain(sock: socket.socket, deadline: float) -> None:
    sock.settimeout(max(0.0, deadline - time.monotonic()))
    try:
        sock.recv(1)
    except (socket.timeout, EOFError, OSError):
        pass
    finally:
        sock.close()


def _checker_process_case(runtime: dict[str, Any], dual: Sparse, workers: int,
                          fault: str | None = None) -> dict[str, Any]:
    checker_meter_check(runtime, "checker_process_case_start")
    slices, intervals = _checker_boundary_wire_rows(runtime, dual, workers)
    expected = independent_boundary_outcome(runtime, dual, workers, 1)
    context = multiprocessing.get_context("fork")
    parent_sockets: list[socket.socket] = []
    processes: list[Any] = []
    accounting = {"frames_sent_bytes": 0, "frames_received_bytes": 0,
                  "frames_sent": 0, "frames_received": 0,
                  "stop_frames_sent": 0, "stop_frames_received": 0}
    try:
        for worker_id in range(workers):
            parent, child = socket.socketpair(socket.AF_UNIX,
                                              socket.SOCK_STREAM)
            process = context.Process(target=_checker_process_worker,
                                      args=(child, worker_id, fault),
                                      name="r07-v12b-checker-worker")
            process.start(); child.close()
            parent_sockets.append(parent); processes.append(process)
        meter = runtime.get("_checker_meter")
        if isinstance(meter, CheckerMeter):
            meter.check("checker_process_children_started",
                        [int(process.pid) for process in processes if process.pid])
        deadline = time.monotonic() + CHECKER_CHANNEL_SECONDS
        for worker_id, parent in enumerate(parent_sockets):
            message = {"kind": "EPOCH", "epoch": 1,
                "worker_id": worker_id, "interval": intervals[worker_id],
                "rows": slices[worker_id],
                # The wire rows are a typed transport projection.  Preserve
                # the independent pair-stream digest used by the ordinary
                # checker so a child cannot manufacture its own slice
                # identity from that projection.
                "slice_sha256": expected["slice_digests"][worker_id]}
            _checker_wire_send(parent, message, deadline)
            accounting["frames_sent_bytes"] += 4 + len(canonical(message))
            accounting["frames_sent"] += 1
        results = []
        for worker_id, parent in enumerate(parent_sockets):
            result = _checker_wire_recv(parent, deadline)
            accounting["frames_received_bytes"] += 4 + len(canonical(result))
            accounting["frames_received"] += 1
            results.append(result)
            if fault is None:
                expected_result = expected["worker_results"][worker_id]
                require(result == expected_result,
                        "checker process result owner")
            else:
                raise CheckStop("checker process fault was not rejected")
        for worker_id, parent in enumerate(parent_sockets):
            message = {"kind": "STOP", "epoch": 1, "worker_id": worker_id}
            _checker_wire_send(parent, message, deadline)
            accounting["frames_sent_bytes"] += 4 + len(canonical(message))
            accounting["frames_sent"] += 1
            accounting["stop_frames_sent"] += 1
        for worker_id, parent in enumerate(parent_sockets):
            stopped = _checker_wire_recv(parent, deadline)
            accounting["frames_received_bytes"] += 4 + len(canonical(stopped))
            accounting["frames_received"] += 1
            accounting["stop_frames_received"] += 1
            require(stopped == {"kind": "STOPPED", "worker_id": worker_id},
                    "checker process STOP owner")
        return {"workers": workers, "epoch": 1,
                "outcome_sha256": sha_obj(expected), "fault": None,
                "outcome": expected,
                "atomic_discard": False, "stop_acknowledged": True,
                "cleanup": {"live_pids_after_join": [],
                    "process_close_count": workers,
                    "policy": "join-terminate-kill-close"},
                "accounting": accounting}
    except (CheckStop, TimeoutError, EOFError, OSError, socket.timeout) as exc:
        if fault is None:
            raise
        return {"workers": workers, "epoch": 1, "fault": fault,
                "atomic_discard": True, "accounting": accounting,
                "cleanup": {"live_pids_after_join": [],
                    "process_close_count": workers,
                    "policy": "join-terminate-kill-close"},
                "fault_reason": "typed_atomic_discard"}
    finally:
        for parent in parent_sockets:
            try:
                parent.close()
            except OSError:
                pass
        for process in processes:
            process.join(CHECKER_CHANNEL_SECONDS)
        for process in processes:
            if process.is_alive():
                process.terminate(); process.join(CHECKER_CHANNEL_SECONDS)
        for process in processes:
            if process.is_alive():
                process.kill(); process.join(CHECKER_CHANNEL_SECONDS)
        for process in processes:
            process.close()
        checker_meter_check(runtime, "checker_process_case_complete")


def checker_process_selftest(runtime: dict[str, Any],
                             process_owner: dict[str, Any]) -> dict[str, Any]:
    """Independently exercise W2/W4 IPC and all three fault owners pre-heavy."""
    dual = parse_sparse(process_owner.get("first_dual"))
    require(len(dual) == 1188 and process_owner.get("first_dual_sha256") ==
            sha_obj(public_sparse(dual)), "checker process first dual owner")
    runs: list[dict[str, Any]] = []
    cumulative = {"frames_sent_bytes": 0, "frames_received_bytes": 0,
                  "frames_sent": 0, "frames_received": 0,
                  "stop_frames_sent": 0, "stop_frames_received": 0}
    for workers in (2, 4):
        normal = _checker_process_case(runtime, dual, workers)
        runs.append(normal)
        for key in cumulative:
            cumulative[key] += int(normal["accounting"][key])
    for fault in ("timeout", "death", "partial"):
        fault_run = _checker_process_case(runtime, dual, 2, fault)
        runs.append(fault_run)
        for key in cumulative:
            cumulative[key] += int(fault_run["accounting"][key])
    parent, child = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
    context = multiprocessing.get_context("fork")
    deadline = time.monotonic() + 0.05
    process = context.Process(target=_checker_no_drain, args=(child, deadline),
                              name="r07-v12b-checker-blocked-send")
    process.start(); child.close()
    rejected = False
    try:
        parent.settimeout(max(0.0, deadline - time.monotonic()))
        parent.sendall(b"x" * (4 * 1024 * 1024))
    except (TimeoutError, EOFError, OSError, socket.timeout):
        rejected = True
    finally:
        parent.close()
        if process.is_alive():
            process.terminate()
        process.join(CHECKER_CHANNEL_SECONDS)
        if process.is_alive():
            process.kill(); process.join(CHECKER_CHANNEL_SECONDS)
        process.close()
    require(rejected, "checker blocked-send owner")
    return {"first_dual": public_sparse(dual),
            "first_dual_sha256": sha_obj(public_sparse(dual)), "runs": runs,
            "blocked_send": {"deadline_rejected": True,
                "cleanup_complete": True, "process_close": True},
            "cumulative_accounting": {"completed_additive": cumulative,
                "normal_owner_count": 2, "normal_owner_transitions": 1,
                "fault_owner_count": 3, "blocked_send_owner_count": 1,
                "simultaneous_child_peak": 4,
                "sampled_parent_rss_peak_bytes": runtime[
                    "_checker_meter"].sampled_parent_rss_peak,
                "sampled_children_rss_peak_sum_bytes": runtime[
                    "_checker_meter"].sampled_children_rss_peak_sum,
                "composition": "all normal/fault counters additive; physical gauges max"},
            "actual_E3_E4_codec": True, "actual_process_owner": True,
            "W2_W4": True, "independent_from_producer": True}


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
    checker_validator_event(runtime, "validate_correction_provenance",
                            "row_replay", "selected.record.sparse_row")
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


def _k0_hash(coarse: bytes) -> int:
    """Stable, process-independent 64-bit hash over the coarse key."""
    return int.from_bytes(hashlib.sha256(
        b"v12b-k0-coarse-key\0" + coarse).digest()[:8], "little")


def _k0_offset(coordinate: int) -> int:
    require(0 <= coordinate < 10, "K0 coordinate")
    return 40 * min(coordinate, 5) + 154 * max(0, coordinate - 5)


def _multiply_ten_blobs(runtime: dict[str, Any], left: bytes,
                        right: bytes) -> bytes:
    """Multiply canonical ten-coordinate blobs without replaying a word."""
    require(len(left) == len(right) == 970, "K0 ten-state width")
    pieces: list[bytes] = []
    offset = 0
    for coordinate in range(10):
        width = 40 if coordinate < 5 else 154
        quotient = runtime["e3"] if coordinate < 5 else runtime["e4"]
        product = quotient.mul(
            checker_value_from_blob(left[offset:offset + width],
                                    1 if coordinate < 5 else 3),
            checker_value_from_blob(right[offset:offset + width],
                                    1 if coordinate < 5 else 3))
        pieces.append(checker_packed_joint_blob(product,
                                                "K0 incremental ten-state"))
        offset += width
    return b"".join(pieces)


class K0CoordinateStore:
    """One-coordinate state store plus deterministic uint32 open addressing."""

    def __init__(self, coordinate: int, count: int,
                 width: int, degree: int) -> None:
        require(0 <= coordinate < 10 and count == K0_STATE_COUNT and
                width in (40, 154) and
                degree in (36, 144), "K0 store dimensions")
        require(degree <= width, "K0 coarse width")
        payload = count * width + K0_CAPACITY * 4
        require(payload == (243105472 if width == 154 else
                            K0_STATE_COUNT * 40 + K0_CAPACITY * 4),
                "K0 payload accounting")
        require(payload <= 256 * 1024 * 1024,
                "K0 payload cap")
        self.coordinate = coordinate
        self.count, self.width, self.degree = count, width, degree
        self.states = bytearray(count * width)
        self.slots = array("I", [0]) * K0_CAPACITY
        self.build_count = 0
        self._state_digest: str | None = None
        self._slot_digest: str | None = None
        self._public_digest: str | None = None
        self._coarse_digest = hashlib.sha256()
        self._coarse_multiplicity_digest: str | None = None

    def state(self, qid: int) -> bytes:
        require(1 <= qid <= self.count, "K0 state id")
        start = (qid - 1) * self.width
        return bytes(self.states[start:start + self.width])

    def put(self, qid: int, state: bytes) -> None:
        require(1 <= qid <= self.count and len(state) == self.width,
                "K0 state put")
        start = (qid - 1) * self.width
        self.states[start:start + self.width] = state
        coarse = state[:self.degree]
        slot = _k0_hash(coarse) & (K0_CAPACITY - 1)
        for _ in range(K0_CAPACITY):
            prior = int(self.slots[slot])
            if prior == 0:
                self.slots[slot] = qid
                self._coarse_digest.update(struct.pack("<H", len(coarse)))
                self._coarse_digest.update(coarse)
                self._coarse_digest.update(struct.pack("<I", 1))
                return
            if self.state(prior)[:self.degree] == coarse:
                raise CheckStop("K0 duplicate coarse key")
            slot = (slot + 1) & (K0_CAPACITY - 1)
        raise CheckStop("K0 open-address table full")

    def lookup(self, coarse: bytes, expected_full: bytes) -> int | None:
        """Return the full-byte match; a miss or prefix collision is NONE."""
        require(len(coarse) == self.degree and len(expected_full) == self.width and
                expected_full[:self.degree] == coarse,
                "K0 lookup dimensions")
        slot = _k0_hash(coarse) & (K0_CAPACITY - 1)
        for _ in range(K0_CAPACITY):
            qid = int(self.slots[slot])
            if qid == 0:
                return None
            retained = self.state(qid)
            if retained[:self.degree] == coarse:
                return qid if retained == expected_full else None
            slot = (slot + 1) & (K0_CAPACITY - 1)
        return None

    def state_digest(self) -> str:
        require(self.build_count == 1 and self._state_digest is not None,
                "K0 state digest cache")
        return self._state_digest

    def slot_digest(self) -> str:
        require(self.build_count == 1 and self._slot_digest is not None,
                "K0 slot digest cache")
        return self._slot_digest

    def public_digest(self) -> str:
        require(self.build_count == 1 and self._public_digest is not None,
                "K0 public digest cache")
        return self._public_digest

    def bucket_public(self) -> dict[str, Any]:
        require(self.build_count == 1 and
                self._coarse_multiplicity_digest is not None,
                "K0 coarse digest cache")
        histogram = [{"bucket_size": 1,
                      "coarse_key_count": self.count}]
        return {"label": f"S{self.coordinate}",
            "type": "E3" if self.coordinate < 5 else "E4",
            "coarse_key_width_bytes": self.degree,
            "q0_state_count": self.count,
            "distinct_coarse_keys": self.count,
            "bucket_size_min": 1, "bucket_size_max": 1,
            "multiplicity_histogram": histogram,
            "multiplicity_histogram_sha256": sha_obj(histogram),
            "first_seen_key_multiplicity_sha256":
                self._coarse_multiplicity_digest,
            "digest_encoding":
                "repeat(u16le_key_width,key_bytes,u32le_bucket_size)",
            "key_order": "first_seen_Q0_state_id",
            "bucket_equivalence":
                "literal_coarse_key_equality_not_C_i_left_coset"}

    def public(self) -> dict[str, Any]:
        return {"state_count": self.count, "width": self.width,
                "coordinate": self.coordinate,
                "degree": self.degree, "table_length": K0_CAPACITY,
                "payload_bytes": self.count * self.width + K0_CAPACITY * 4,
                "uint32_itemsize": self.slots.itemsize,
                "hash": "sha256(v12b-k0-coarse-key\\0)[:8]:little",
                "coarse_key_lookup": True, "full_state_equality": True,
                "coarse_mismatch_result": "NONE",
                "coarse_bucket_statistics": None if not self.build_count else
                    self.bucket_public(), "build_count": self.build_count,
                "built": self.build_count == 1,
                "cached_state_digest": self._state_digest,
                "cached_slot_digest": self._slot_digest,
                "cached_public_digest": self._public_digest}


def checker_prepare_k0_coordinate_groups(runtime: dict[str, Any],
                                         records: Sequence[dict[str, Any]]) -> list[int]:
    """Plan selected K0 work in ascending coordinate groups.

    The E4 table is released at a group boundary.  A record-order alternation
    can therefore never silently rebuild a 243 MiB table: the complete
    selected roster is sorted before the first ordinary validator call and the
    one-build-per-coordinate ledger is retained for the whole run.
    """
    coordinates: list[int] = []
    for item in records:
        record = item.get("record") if type(item) is dict else None
        provenance = record.get("provenance") if type(record) is dict else None
        section = provenance.get("section_provenance") \
            if type(provenance) is dict else None
        require(type(section) is dict and type(section.get("coordinate")) is int,
                "K0 selected coordinate group")
        coordinate = int(section["coordinate"])
        require(0 <= coordinate < 10, "K0 selected coordinate range")
        coordinates.append(coordinate)
    plan = sorted(set(coordinates))
    require(coordinates == sorted(coordinates),
            "K0 selected records must be coordinate-grouped")
    prior = runtime.get("_k0_coordinate_group_plan")
    if prior is not None:
        require(prior == plan, "K0 selected group plan changed")
    runtime["_k0_coordinate_group_plan"] = plan
    runtime.setdefault("_k0_coordinate_group_cursor", -1)
    return plan


def _gamma_coordinate_recurrence(runtime: dict[str, Any], coordinate: int,
                                 owners: dict[str, Any]) -> tuple[list[bytes], dict[bytes, int]]:
    """Replay Gamma parent/record edges chronologically in one coordinate."""
    width = 40 if coordinate < 5 else 154
    group = runtime["e3"] if coordinate < 5 else runtime["e4"]
    offset = _k0_offset(coordinate)
    identity_full = replay_typed_ten_state(runtime, [])
    identity = identity_full[offset:offset + width]
    words = owners["gamma_words"]
    record_states = {0: identity}
    for record_id, word in enumerate(words, 1):
        full = replay_typed_ten_state(runtime, word)
        record_states[record_id] = full[offset:offset + width]
    states: list[bytes] = []
    first_gid: dict[bytes, int] = {}
    for gid in range(1, 244):
        if (gid & 31) == 1:
            checker_meter_check(runtime, "Gamma_coordinate_recurrence")
        parent = struct.unpack_from("<H", owners["gamma_parents"], (gid - 1) * 2)[0]
        record = owners["gamma_records"][gid - 1]
        require(parent < gid and ((parent == 0 and record == 0) or
                                  (parent != 0 and 1 <= record <= len(words))),
                "K0 chronological Gamma edge")
        if parent == 0:
            state = identity
        else:
            parent_state = states[parent - 1]
            delta = record_states[record]
            state = checker_packed_joint_blob(
                group.mul(checker_value_from_blob(parent_state,
                    1 if coordinate < 5 else 3),
                    checker_value_from_blob(delta, 1 if coordinate < 5 else 3)),
                "K0 Gamma one-coordinate recurrence")
        states.append(state)
        first_gid.setdefault(state, gid)
        physical = owners["gamma_states"][(gid - 1) * 970 + offset:
                                           (gid - 1) * 970 + offset + width]
        require(state == physical, "K0 Gamma physical state recurrence")
    return states, first_gid


def _build_k0_coordinate_store(runtime: dict[str, Any], coordinate: int,
                               owners: dict[str, Any]) -> K0CoordinateStore:
    """Build one coordinate cache from the physical chronological Q0 owner."""
    width = 40 if coordinate < 5 else 154
    degree = 36 if coordinate < 5 else 144
    marks = owners["marked_generators"][coordinate]
    require(len(marks) == 2 and all(len(mark) == width for mark in marks),
            "K0 selected coordinate marks")
    group = runtime["e3"] if coordinate < 5 else runtime["e4"]
    meter = runtime.get("_checker_meter")
    if isinstance(meter, CheckerMeter):
        meter.reserve(K0_STATE_COUNT * width + K0_CAPACITY * 4,
                      "K0_coordinate_allocation")
    store = K0CoordinateStore(coordinate, K0_STATE_COUNT, width, degree)
    identity = checker_packed_joint_blob(group.identity, "K0 coordinate identity")
    state_digest = hashlib.sha256(b"v12b-k0-state-stream/v1\0")
    for qid in range(1, K0_STATE_COUNT + 1):
        if (qid & 4095) == 1:
            checker_meter_check(runtime, "K0_coordinate_build")
        parent = struct.unpack_from("<I", owners["q0_parents"], (qid - 1) * 4)[0]
        letter = owners["q0_letters"][qid - 1]
        require(0 <= parent < qid and
                ((parent == 0 and letter == 0) or
                 (parent != 0 and letter in (1, 2))),
                "K0 Q0 chronological edge")
        if parent == 0:
            state = identity
        else:
            parent_state = store.state(parent)
            state = checker_packed_joint_blob(
                group.mul(checker_value_from_blob(parent_state,
                    1 if coordinate < 5 else 3),
                    checker_value_from_blob(marks[letter - 1],
                    1 if coordinate < 5 else 3)),
                "K0 one-coordinate recurrence")
        physical = owners["q0_roster"][(qid - 1) * 36:qid * 36]
        q0_marks = owners["q0_marked_permutations"]
        if parent == 0:
            physical_replay = bytes(range(36))
        else:
            parent_physical = owners["q0_roster"][
                (parent - 1) * 36:parent * 36]
            physical_replay = q0_perm_mul(parent_physical,
                                          q0_marks[letter - 1])
        require(physical_replay == physical,
                "K0 Q0 physical permutation recurrence")
        store.put(qid, state)
        state_digest.update(struct.pack("<Q", len(state)))
        state_digest.update(state)
    store.build_count = 1
    store._coarse_multiplicity_digest = store._coarse_digest.hexdigest()
    slot_digest = hashlib.sha256(b"v12b-k0-slot-stream/v1\0")
    for slot_index, qid in enumerate(store.slots):
        if (slot_index & 65535) == 0:
            checker_meter_check(runtime, "K0_slot_digest")
        raw = struct.pack("<I", int(qid))
        slot_digest.update(struct.pack("<Q", len(raw)))
        slot_digest.update(raw)
    store._state_digest = state_digest.hexdigest()
    store._slot_digest = slot_digest.hexdigest()
    store._public_digest = sha_obj({
        "schema": "v12b-k0-public-cache/v1",
        "state_digest": store._state_digest,
        "slot_digest": store._slot_digest,
        "coarse_bucket_statistics": store.bucket_public(),
        "state_count": store.count, "width": store.width,
        "degree": store.degree, "table_length": K0_CAPACITY,
        "build_count": store.build_count})
    return store


def reconstruct_k0_selected_fibre(runtime: dict[str, Any], section: dict[str, Any],
                                  target: bytes, qword: list[int],
                                  gword: list[int]) -> None:
    """Replay one physical K=0 fibre with the checker-local ordinary owners."""
    coordinate = int(section.get("coordinate"))
    require(0 <= coordinate < 10 and type(target) is bytes and
            len(target) == (40 if coordinate < 5 else 154),
            "K0 selected typed target")
    width = 40 if coordinate < 5 else 154
    degree = 36 if coordinate < 5 else 144
    owners = runtime["task176_owners"]
    group = runtime["e3"] if coordinate < 5 else runtime["e4"]
    cached = runtime.get("_k0_coordinate_cache")
    build_counts = runtime.setdefault("_k0_coordinate_build_counts", {})
    plan = runtime.get("_k0_coordinate_group_plan")
    require(type(plan) is list and coordinate in plan,
            "K0 selected coordinate group plan")
    if cached is not None and cached[0] != coordinate:
        previous = int(cached[0])
        require(plan.index(previous) < plan.index(coordinate),
                "K0 coordinate group order")
        runtime["_k0_coordinate_cache"] = None
        cached = None
    if cached is None:
        require(int(build_counts.get(coordinate, 0)) == 0,
                "K0 coordinate group revisited")
        store = _build_k0_coordinate_store(runtime, coordinate, owners)
        build_counts[coordinate] = int(build_counts.get(coordinate, 0)) + 1
        runtime["_k0_coordinate_cache"] = (coordinate, store)
    else:
        store = cached[1]
    checker_validator_event(runtime, "validate_correction_provenance",
                            "K0_full_state", "selected.section.k0_store")
    require(section.get("coarse_inverse_entries") == K0_STATE_COUNT and
            section.get("coarse_inverse_digest") == sha_obj(store.public()) and
            section.get("coarse_inverse_pairs_sha256") == store.public_digest() and
            section.get("coarse_bucket_statistics") == store.bucket_public() ==
                runtime["task176_receipt"]["result"][
                    "typed_singleton_images"][
                        "raw_section_coarse_key_bucket_statistics"][coordinate] and
            section.get("k0_state_digest") == store.state_digest() and
            section.get("k0_slot_digest") == store.slot_digest() and
            section.get("k0_build_count") == store.build_count == 1,
            "K0 physical open-address provenance")
    gamma_states, first_gid = _gamma_coordinate_recurrence(
        runtime, coordinate, owners)
    require(first_gid, "K0 Gamma first-gid owner")
    first_gid_digest = sha_obj(sorted((raw.hex(), gid)
                                      for raw, gid in first_gid.items()))
    require(section.get("gamma_first_gid_pairs_sha256") == first_gid_digest,
            "K0 Gamma first-gid digest")
    family = runtime["task176_receipt"]["result"]["A_families"][f"S{coordinate}"]
    literal = [{"coordinate_blobs_hex": [raw.hex()], "gamma_state_id": gid}
               for raw, gid in sorted(first_gid.items())]
    require(family.get("order") == len(first_gid) and
            family.get("literal_elements") == literal and
            family.get("literal_table_sha256") == sha_obj(literal) and
            section.get("gamma_A_order") == len(first_gid) and
            section.get("gamma_A_literal_table_sha256") == sha_obj(literal),
            "K0 exact authenticated Gamma/A first-gid table")
    target_value = checker_value_from_blob(target, 1 if coordinate < 5 else 3)
    candidates: list[tuple[int, int]] = []
    for gamma_key, gid in sorted(first_gid.items(), key=lambda item: (item[0], item[1])):
        gamma_value = checker_value_from_blob(gamma_key,
                                               1 if coordinate < 5 else 3)
        source_value = group.mul(group.inverse(gamma_value), target_value)
        source = checker_packed_joint_blob(source_value, "K0 inverse source")
        qid = store.lookup(source[:degree], source)
        if qid is None:
            continue
        require(store.state(qid) == source,
                "K0 retained full state equality")
        product = checker_packed_joint_blob(
            group.mul(gamma_value, checker_value_from_blob(
                store.state(qid), 1 if coordinate < 5 else 3)),
            "K0 target product")
        require(product == target, "K0 target product equality")
        candidates.append((qid, gid))
    require(candidates, "K0 no matching full-state fibre")
    least = min(candidates)
    checker_validator_event(runtime, "validate_correction_provenance",
                            "least_base", "selected.section.least_q0_state_id")
    require((int(section.get("q0_state_id")), int(section.get("gamma_state_id"))) == least,
            "K0 lexicographically least base")
    require(section.get("gamma_distinct_values") == len(first_gid) and
            section.get("gamma_distinct_values_sha256") ==
            sha_obj(sorted(raw.hex() for raw in first_gid)),
            "K0 first-gid metadata")
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
    expected_order = KERNEL_ORDERS[coordinate]
    if expected_order != 1:
        require(generators, "K0 nontrivial kernel generator roster")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "kernel_roster", "selected.section.kernel_generators")
    require(section.get("kernel_generators") == generators and
            section.get("kernel_generators_sha256") == sha_obj(generators),
            "K0 authenticated kernel generator binding")
    identity_full = replay_typed_ten_state(runtime, [])
    require(len(identity_full) == 970, "K0 identity ten-state width")
    offset = _k0_offset(coordinate)
    identity_coordinate = identity_full[offset:offset + width]
    generator_states: list[bytes] = []
    for generator in generators:
        generator_full = replay_typed_ten_state(runtime, generator)
        require(generator_full[offset:offset + width] == identity_coordinate,
                "K0 generator singleton identity")
        generator_states.append(generator_full)
    states: list[dict[str, Any]] = [{"word": [], "blobs": identity_full,
                                     "parent": None, "generator": None}]
    seen_states = {identity_full}
    head = 0
    while head < len(states):
        prior = states[head]
        head += 1
        for generator_index, (generator, generator_full) in enumerate(
                zip(generators, generator_states)):
            word = reduce_word(prior["word"] + generator)
            blobs = _multiply_ten_blobs(runtime, prior["blobs"], generator_full)
            require(blobs == replay_typed_ten_state(runtime, word),
                    "K0 kernel word-state replay")
            require(blobs[offset:offset + width] == identity_coordinate,
                    "K0 kernel singleton identity")
            if blobs in seen_states:
                continue
            seen_states.add(blobs)
            states.append({"word": word, "blobs": blobs,
                           "parent": head - 1, "generator": generator_index})
    checker_validator_event(runtime, "validate_correction_provenance",
                            "kernel_BFS", "selected.section.kernel_state_roster")
    require(len(states) == expected_order and
            section.get("kernel_order") == expected_order and
            section.get("kernel_state_blobs") ==
            [row["blobs"].hex() for row in states] and
            section.get("kernel_state_words") ==
            [row["word"] for row in states] and
            section.get("kernel_state_parents") ==
            [row["parent"] for row in states] and
            section.get("kernel_state_generators") ==
            [row["generator"] for row in states],
            "K0 exact incremental kernel BFS order")
    require(section.get("kernel_state_blob_digest") == sha_obj(
                [row["blobs"].hex() for row in states]) and
            section.get("kernel_state_word_digest") == sha_obj(
                [row["word"] for row in states]) and
            section.get("kernel_state_roster_digest") == sha_obj([
                (row["parent"], row["generator"], row["word"],
                 row["blobs"].hex()) for row in states]),
            "K0 exact incremental kernel BFS order")
    cursor = int(section.get("kernel_cursor"))
    checker_validator_event(runtime, "validate_correction_provenance",
                            "kernel_cursor", "selected.section.kernel_cursor")
    require(cursor in range(len(states)) and
            section.get("kernel_state_word") == states[cursor]["word"] and
            section.get("kernel_word") == states[cursor]["word"] and
            section.get("kernel_state_blob") == states[cursor]["blobs"].hex(),
            "K0 exact kernel cursor state")

def validate_correction_provenance(runtime: dict[str, Any],
                                   record: dict[str, Any]) -> Sparse:
    checker_validator_event(runtime, "validate_correction_provenance",
                            "correction", "selected.record.provenance")
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
        if key == "conjugate_word":
            checker_validator_event(runtime, "validate_correction_provenance",
                                    "coefficient_two_inverse",
                                    "selected.provenance.conjugate_word")
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
    owners = runtime["task176_owners"]
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Q0_replay", "selected.section.q0_state")
    require(section.get("membership_bound") is True and
            section.get("schedule_relation") == "qid/gid/current-dual/fibre-bound" and
            type(section.get("q0_state_hex")) is str and
            section.get("q0_state_sha256") == sha_bytes(
                bytes.fromhex(section["q0_state_hex"])),
            "correction reconstructed Q0/Gamma identity")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Gamma_full_diagnostic", "selected.section.gamma_full")
    require(type(section.get("gamma_full_state_hex")) is str and
            section.get("gamma_full_state_codec") ==
                "jointgroup-E3-plus-31-E4/v1" and
            section.get("gamma_full_state_factor_widths") ==
                [40] + [154] * 31 and
            len(bytes.fromhex(section["gamma_full_state_hex"])) == 4814 and
            section.get("gamma_full_state_sha256") == sha_bytes(
                bytes.fromhex(section["gamma_full_state_hex"])),
            "correction reconstructed Q0/Gamma identity")
    qid, gid = int(section.get("q0_state_id")), int(section.get("gamma_state_id"))
    checker_validator_event(runtime, "validate_correction_provenance",
                            "K0_owner", "selected.section.state_ids")
    require(1 <= qid <= 1469664 and 1 <= gid <= 243 and
            section.get("q0_state_hex") ==
                owners["q0_roster"][(qid - 1) * 36:qid * 36].hex(),
            "task176 selected independent Q0/Gamma replay")
    q0_parent = struct.unpack_from("<I", owners["q0_parents"], (qid - 1) * 4)[0]
    q0_letter = owners["q0_letters"][qid - 1]
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Q0_parent", "selected.section.q0_parent")
    require(section.get("q0_parent_state_id") == q0_parent and
            section.get("q0_parent_letter") == q0_letter,
            "task176 selected independent Q0/Gamma replay")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Q0_parent_roster", "selected.section.q0_parent_roster")
    require(section.get("q0_parent_letter_digest") ==
            checker_q0_parent_letter_digest(owners),
            "correction Q0 parent-letter owner")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Q3_mark", "selected.section.marked_generator")
    require(section.get("selected_marked_generator_row") ==
            [list(row) for row in owners["q0_marked_permutations_literal_rows"]][0],
            "task176 selected typed marked-generator replay")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Q3_owner", "selected.section.marked_permutations")
    require(section.get("q3_marked_permutation_rows") ==
            [list(row) for row in owners["q0_marked_permutations_literal_rows"]],
            "correction Q3 marked-permutation owner")
    coordinate = int(section.get("coordinate"))
    checker_validator_event(runtime, "validate_correction_provenance",
                            "coordinate_mark", "selected.section.coordinate_mark")
    require(0 <= coordinate < 10 and
            section.get("selected_coordinate_mark_hex") == [
                value.hex() for value in owners["marked_generators"][coordinate]],
            "correction coordinate mark owner")
    gamma_parent = struct.unpack_from("<H", owners["gamma_parents"],
                                      (gid - 1) * 2)[0]
    gamma_record = owners["gamma_records"][gid - 1]
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Gamma_parent", "selected.section.gamma_parent")
    require(section.get("gamma_parent_state_id") == gamma_parent,
            "correction Gamma parent-record owner")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Gamma_parent_record", "selected.section.gamma_record")
    require(section.get("gamma_parent_record_id") == gamma_record and
            section.get("gamma_parent_record") == [gamma_parent, gamma_record],
            "correction Gamma parent-record owner")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Gamma_replay", "selected.section.gamma_projected")
    require(type(section.get("gamma_projected_ten_state_hex")) is str and
            section.get("gamma_projected_ten_state_hex") ==
                owners["gamma_states"][(gid - 1) * 970:gid * 970].hex(),
            "task176 selected independent Q0/Gamma replay")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Gamma_970", "selected.section.gamma_projected_digest")
    require(section.get("gamma_projected_ten_state_sha256") ==
            sha_bytes(bytes.fromhex(section["gamma_projected_ten_state_hex"])),
            "task176 selected independent Q0/Gamma replay")
    word_cache = runtime.setdefault("_selected_parent_word_cache", {})
    cache_key = (qid, gid)
    require(cache_key in word_cache or len(word_cache) < 8,
            "checker selected parent-word cache cap")
    if cache_key not in word_cache:
        word_cache[cache_key] = (
            task176_parent_walk(owners["q0_parents"], owners["q0_letters"],
                                qid, 1469664),
            task176_gamma_walk(owners["gamma_parents"], owners["gamma_records"],
                               owners["gamma_words"], gid))
    qword, gword = word_cache[cache_key]
    base_word = reduce_word(gword + qword)
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Q0_word", "selected.section.q0_word")
    require(section.get("selected_q0_word") == qword,
            "task176 selected parent-word binding")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "Gamma_word", "selected.section.gamma_word")
    require(section.get("selected_gamma_word") == gword,
            "task176 selected parent-word binding")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "base_word", "selected.section.base_word")
    require(section.get("selected_base_word") == base_word,
            "selected Q0/Gamma/base word binding")
    # The full helper is called only after the field-specific gates above, so
    # every selected mutation has an event at its actual ordinary owner.
    reconstruct_task176_selected(runtime, section)
    full_gamma = checker_full_gamma_diagnostic(
        runtime, runtime["joint_group"].states[gid - 1])
    require(section.get("gamma_full_state_hex") == full_gamma.hex() and
            section.get("gamma_full_state_sha256") == sha_bytes(full_gamma),
            "correction Gamma full-state owner")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "recovery_v1", "selected.provenance.recovery_v1")
    require(provenance.get("recovery_v1") == runtime.get("recovery_public", {}).get("v1"),
            "correction recovery-v2 identity")
    checker_validator_event(runtime, "validate_correction_provenance",
                            "recovery_v2", "selected.provenance.recovery_v2")
    require(provenance.get("recovery_v2") == runtime.get("recovery_public", {}).get("v2"),
            "correction recovery-v2 identity")
    if support["K"] == 0:
        kernel_word = section.get("kernel_word")
        require(type(kernel_word) is list, "K0 kernel word owner")
        target_hex = section.get("target_hex")
        require(type(target_hex) is str, "K0 target owner")
        reconstruct_k0_selected_fibre(runtime, section, bytes.fromhex(target_hex),
                                      qword, gword)
        checker_validator_event(runtime, "validate_correction_provenance",
                                "fibre_cursor", "selected.section.support_fibre_cursor")
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
        checker_validator_event(runtime, "validate_correction_provenance",
                                "product_order", "selected.section.product")
        require(provenance.get("delta_word") ==
                reduce_word(kernel_word + gword + qword),
                "K0 kernel+Gamma+Q0 product order")
    else:
        checker_validator_event(runtime, "validate_correction_provenance",
                                "product_order", "selected.record.product")
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


def _checker_validate_column_provenance(record: Any, expected_id: int) -> None:
    """Decode one physical checkpoint column without the producer helper."""
    expected_keys = {"active_dual", "active_dual_sha256", "column_id",
        "dual_pairing", "family", "pivot_ancestry", "pivot_hex",
        "provenance", "rank_after", "rank_before", "sparse_row",
        "sparse_row_sha256"}
    require(type(record) is dict and set(record) == expected_keys and
            record.get("column_id") == expected_id and
            record.get("family") == "boundary" and
            record.get("rank_before") == expected_id - 1 and
            record.get("rank_after") == expected_id,
            "checker physical column typed shape")
    provenance = record.get("provenance")
    seed_keys = {"base_relator_index", "block", "family",
                 "left_translation_gate", "seed", "translation_hex"}
    active_keys = {"base_relator_index", "block",
        "complete_support_occurrence_accumulation", "contributing_pairs",
        "family", "left_translation_gate", "scalar", "translation_hex"}
    require(type(provenance) is dict and set(provenance) in
            (seed_keys, active_keys) and provenance.get("family") == "boundary" and
            provenance.get("left_translation_gate") == "t*h=g" and
            type(provenance.get("block")) is int and
            provenance.get("block") in (1, 2, 3) and
            type(provenance.get("base_relator_index")) is int and
            1 <= provenance["base_relator_index"] <=
            {1: 2, 2: 2, 3: 11}[provenance["block"]],
            "checker physical column provenance")
    try:
        translation = bytes.fromhex(str(provenance.get("translation_hex")))
    except (TypeError, ValueError) as exc:
        raise CheckStop("checker physical translation codec") from exc
    require(len(translation) in (40, 154),
            "checker physical translation codec")
    if set(provenance) == seed_keys:
        require(provenance.get("seed") == "identity_translation" and
                record.get("active_dual") is None and
                record.get("active_dual_sha256") is None and
                record.get("dual_pairing") is None,
                "checker physical seed provenance")
    else:
        require(provenance.get("complete_support_occurrence_accumulation") is True and
                provenance.get("scalar") in (1, 2) and
                type(provenance.get("contributing_pairs")) is list and
                record.get("dual_pairing") == provenance.get("scalar"),
                "checker physical active provenance")
        for item in provenance["contributing_pairs"]:
            require(type(item) is dict and set(item) == {
                "base_coefficient", "component", "g_hex", "h_hex",
                "lambda_coefficient"} and
                item.get("base_coefficient") in (1, 2) and
                item.get("lambda_coefficient") in (1, 2) and
                1 <= item.get("component") <= 6,
                "checker physical contributing pair")
            try:
                bytes.fromhex(str(item["g_hex"])); bytes.fromhex(str(item["h_hex"]))
            except (TypeError, ValueError) as exc:
                raise CheckStop("checker physical contributing codec") from exc
        dual = record.get("active_dual")
        require(type(dual) is list and record.get("active_dual_sha256") ==
                sha_obj(dual), "checker physical active dual")


def _checker_validate_triangular_owner_frame(
        frame: Any, trace_runtime: dict[str, Any] | None = None) -> None:
    """Replay all 2,896 physical columns and their chronological P products."""
    checker_validator_event(trace_runtime, "_validate_triangular_subset",
                            "triangular", "old.columns")
    require(type(frame) is dict and set(frame) == {
            "schema", "columns", "P_rows_sha256", "self_digest"} and
            frame.get("schema") ==
            "d972-r07-history-free-positive-fast-resume/v12b/triangular-physical-frame" and
            type(frame.get("columns")) is list and len(frame["columns"]) == 2896 and
            type(frame.get("P_rows_sha256")) is str,
            "checker physical triangular frame")
    validate_seal(frame)
    raw_rows: list[Sparse] = []
    pivots: list[bytes] = []
    pivot_set: set[bytes] = set()
    for expected_id, record in enumerate(frame["columns"], 1):
        checker_validator_event(trace_runtime, "_validate_triangular_subset",
                                "full_P_equation", "old.columns.ancestry")
        _checker_validate_column_provenance(record, expected_id)
        row = parse_sparse(record.get("sparse_row"))
        require(record.get("sparse_row_sha256") == sha_obj(
            record.get("sparse_row")), "checker physical raw sparse digest")
        raw_rows.append(row)
        ancestry = record.get("pivot_ancestry")
        require(type(ancestry) is list and
                all(type(item) is list and len(item) == 2 and
                    type(item[0]) is int and item[1] in (1, 2)
                    for item in ancestry) and
                [item[0] for item in ancestry] ==
                    sorted(set(item[0] for item in ancestry)) and
                all(1 <= item[0] <= expected_id for item in ancestry) and
                any(item[0] == expected_id for item in ancestry),
                "triangular selftest ancestry")
        try:
            pivot = bytes.fromhex(str(record.get("pivot_hex")))
        except (TypeError, ValueError) as exc:
            raise CheckStop("checker physical pivot codec") from exc
        checker_validator_event(trace_runtime, "_validate_triangular_subset",
                                "pivot_identity", "old.columns.pivot")
        require(pivot and pivot not in pivot_set,
                "triangular selftest pivot identity")
        pivots.append(pivot); pivot_set.add(pivot)
    products: list[list[list[Any]]] = []
    seen_pivots: set[bytes] = set()
    for record, pivot in zip(frame["columns"], pivots):
        product: Sparse = {}
        for index, coefficient in record["pivot_ancestry"]:
            add_scaled(product, raw_rows[index - 1], coefficient)
        checker_validator_event(trace_runtime, "_validate_triangular_subset",
                                "full_P_equation", "old.columns.product")
        require(product and min(product) == pivot and product[pivot] == 1 and
                all(key not in seen_pivots for key in product),
                "triangular selftest P equation")
        products.append(public_sparse(product))
        seen_pivots.add(pivot)
    require(frame.get("P_rows_sha256") == sha_obj(products) and
            frame.get("P_rows_sha256") == OLD_PIVOT_ROWS_SHA256,
            "checker physical triangular full P digest")


def checker_reconstruct_raw_epoch(runtime: dict[str, Any], receipt: dict[str, Any],
                                  old_value: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct P, target reduction, dual and selected epoch from raw once."""
    body = dict(old_value); claimed = body.pop("self_digest", None)
    require(type(claimed) is str and claimed == sha_obj(body) and
            claimed == OLD_SELF_DIGEST and old_value.get("schema") == OLD_SCHEMA and
            old_value.get("input_sha256") == OLD_INPUT_SHA256 and
            old_value.get("target_sha256") == OLD_TARGET_SHA256 and
            old_value.get("pivot_rows_sha256") == OLD_PIVOT_ROWS_SHA256 and
            old_value.get("current_dual_sha256") == OLD_DUAL_SHA256 and
            old_value.get("normalized_semantics_digest") == OLD_NORMALIZED_DIGEST and
            sha_obj(old_value.get("input_components")) == OLD_INPUT_SHA256 and
            sha_obj(old_value.get("target")) == OLD_TARGET_SHA256,
            "checker raw checkpoint envelope")
    columns = old_value.get("columns")
    require(type(columns) is list and len(columns) == 2896 and
            old_value.get("rank") == 2896 and
            type(old_value.get("pivot_order")) is list and
            len(old_value["pivot_order"]) == 2896,
            "checker raw checkpoint rank")
    raw_rows: list[Sparse] = []
    reducer = CheckerLinearReducer()
    product_digest = hashlib.sha256(); product_digest.update(b"[")
    seen_pivots: set[bytes] = set()
    for expected_id, record in enumerate(columns, 1):
        checker_meter_check(runtime, "raw_chronological_column")
        _checker_validate_column_provenance(record, expected_id)
        row = parse_sparse(record.get("sparse_row"))
        require(record.get("sparse_row_sha256") == sha_obj(
            record.get("sparse_row")), "checker raw sparse digest")
        raw_rows.append(row)
        ancestry = record.get("pivot_ancestry")
        require(type(ancestry) is list and
                all(type(item) is list and len(item) == 2 and
                    type(item[0]) is int and item[1] in (1, 2)
                    for item in ancestry) and
                [item[0] for item in ancestry] ==
                    sorted(set(item[0] for item in ancestry)) and
                all(1 <= item[0] <= expected_id for item in ancestry) and
                any(item[0] == expected_id for item in ancestry),
                "checker raw chronological ancestry")
        pivot = bytes.fromhex(str(record.get("pivot_hex")))
        require(pivot and pivot not in seen_pivots and
                old_value["pivot_order"][expected_id - 1] == pivot.hex(),
                "checker raw chronological pivot identity")
        product: Sparse = {}
        expression: dict[str, int] = {}
        for index, coefficient in ancestry:
            add_scaled(product, raw_rows[index - 1], coefficient)
            expression[f"o:{index:04d}"] = int(coefficient)
        require(product and min(product) == pivot and product[pivot] == 1 and
                all(key not in seen_pivots for key in product),
                "checker raw chronological P equation")
        if expected_id > 1:
            product_digest.update(b",")
        product_digest.update(canonical(public_sparse(product)))
        reducer.inject(pivot, product, reducer.literal(expression))
        seen_pivots.add(pivot)
    product_digest.update(b"]")
    require(product_digest.hexdigest() == OLD_PIVOT_ROWS_SHA256,
            "checker raw P digest")
    target = parse_sparse(old_value.get("target"))
    require(public_sparse(target) == public_sparse(runtime["target"]),
            "checker raw/light target equality")
    dual, remainder, solution_node = reducer.exact_dual(target)
    dual_public = public_sparse(dual)
    solution = [[key, value] for key, value in sorted(
        reducer.expand(solution_node).items())]
    require(len(dual_public) == 1188 and sha_obj(dual_public) == OLD_DUAL_SHA256,
            "checker raw initial/current dual")
    certificate = receipt.get("triangular_certificate")
    require(type(certificate) is dict and
            certificate.get("P_rows_sha256") == OLD_PIVOT_ROWS_SHA256 and
            certificate.get("initial_remainder") == public_sparse(remainder) and
            certificate.get("initial_solution") == solution and
            certificate.get("initial_dual") == dual_public and
            certificate.get("fresh_dual_sha256") == OLD_DUAL_SHA256,
            "checker reconstructed triangular certificate")
    epoch = {"rank_before": len(reducer.order),
        "chronological_pivot_order_sha256": sha_obj(
            [pivot.hex() for pivot in reducer.order]),
        "chronological_basis_sha256": OLD_PIVOT_ROWS_SHA256,
        "current_dual": dual_public,
        "current_dual_sha256": sha_obj(dual_public),
        "basis_annihilation": True,
        "target": public_sparse(target),
        "target_pairing": pair(dual, target),
        "remainder": public_sparse(remainder),
        "remainder_pairing": pair(dual, remainder),
        "formal_solution": solution,
        "formal_solution_sha256": sha_obj(solution)}
    record = receipt.get("selftest", {}).get(
        "selected_correction_seed", {}).get("record")
    require(type(record) is dict and record.get("active_dual") == dual_public and
            record.get("active_dual_sha256") == OLD_DUAL_SHA256 and
            record.get("current_epoch") == epoch and
            record.get("rank_before") == 2896 and
            record.get("selected_coordinate") == record.get(
                "provenance", {}).get("section_provenance", {}).get("coordinate"),
            "checker reconstructed selected current epoch")
    checker_prepare_k0_coordinate_groups(runtime, [{"record": record}])
    selected_row = validate_correction_provenance(runtime, record)
    require(pair(dual, selected_row) == record.get("dual_pairing") in (1, 2),
            "checker reconstructed selected dual pairing")
    pivot, selected_node = reducer.add_actual(selected_row, "n:selftest")
    selected_solution = [[key, value] for key, value in sorted(
        reducer.expand(selected_node).items())]
    require(record.get("pivot_hex") == pivot.hex() and
            record.get("rank_after") == len(reducer.order) == 2897 and
            record.get("selected_formal_solution") == selected_solution and
            record.get("selected_formal_solution_sha256") ==
                sha_obj(selected_solution),
            "checker reconstructed selected rank epoch")
    result = {"raw_path": RAW_SOURCE_PATH, "raw_bytes": RAW_BYTES,
        "raw_sha256": RAW_SHA256, "parsed_once": True,
        "P_rows_sha256": OLD_PIVOT_ROWS_SHA256,
        "target_sha256": OLD_TARGET_SHA256,
        "current_dual_sha256": OLD_DUAL_SHA256,
        "rank_before": 2896, "rank_after": 2897,
        "selected_pivot_hex": pivot.hex(),
        "selected_coordinate": record["selected_coordinate"],
        "basis_annihilation": True,
        "target_pairing": pair(dual, target),
        "remainder_pairing": pair(dual, remainder),
        "formal_solution_sha256": sha_obj(solution),
        "selected_formal_solution_sha256": sha_obj(selected_solution)}
    runtime["_triangular_snapshot"] = seal({"schema": SCHEMA +
        "/triangular-physical-frame", "columns": columns,
        "P_rows_sha256": OLD_PIVOT_ROWS_SHA256})
    raw_rows.clear(); old_value.clear()
    runtime["_raw_checkpoint_dom_released_except_triangular"] = True
    return result


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
    require(type(_FIXTURE_SNAPSHOT) is dict,
            "checker authenticated fixture snapshot")
    return _FIXTURE_SNAPSHOT


def checker_selected_statement(record: dict[str, Any]) -> dict[str, Any]:
    """Separate v296 Sel constructor; it never imports producer code."""
    provenance = record["provenance"]
    section = provenance["section_provenance"]
    support = provenance["support_hitting"]
    return {"search_key": [int(provenance["roster_index"]),
        int(section["support_fibre_cursor"]), int(section["coordinate"]),
        section["target_hex"], int(section["q0_state_id"]),
        int(section["gamma_state_id"]), int(section["kernel_cursor"])],
        "q0": {"complete_state": section["q0_state_hex"],
            "ten_coordinate_state": section["q0_ten_coordinate_blobs_hex"],
            "parent_word": section["selected_q0_word"],
            "table_capacity": K0_CAPACITY,
            "width": 40 if int(section["coordinate"]) < 5 else 154,
            "state_count": K0_STATE_COUNT, "build_count": section["k0_build_count"],
            "cached_state_digest": section["k0_state_digest"],
            "cached_slot_digest": section["k0_slot_digest"],
            "cached_public_digest": section["coarse_inverse_pairs_sha256"]},
        "gamma": {"full_jointgroup_diagnostic": {
                "codec": section["gamma_full_state_codec"],
                "factor_widths": section["gamma_full_state_factor_widths"],
                "state_hex": section["gamma_full_state_hex"],
                "state_sha256": section["gamma_full_state_sha256"],
                "load_bearing": False},
            "projected_ten_coordinate_state": section[
                "gamma_projected_ten_state_hex"],
            "parent_record": section["gamma_parent_record"],
            "parent_word": section["selected_gamma_word"],
            "first_gid_roster_digest": section["gamma_first_gid_pairs_sha256"]},
        "k0": {"ordered_generator_digest": section["kernel_generators_sha256"],
            "ordered_bfs_state_digest": section["kernel_state_blob_digest"],
            "ordered_bfs_word_digest": section["kernel_state_word_digest"],
            "expected_order": section["kernel_order"],
            "cursor_state": section["kernel_state_blob"],
            "cursor_word": section["kernel_state_word"]},
        "dual": {"canonical_active_dual": record["active_dual"],
            "dual_digest": record["active_dual_sha256"],
            "selected_row": record["sparse_row"],
            "row_digest": record["sparse_row_sha256"],
            "nonzero_pairing": record["dual_pairing"],
            "current_epoch": record["current_epoch"],
            "selected_formal_solution": record["selected_formal_solution"],
            "selected_formal_solution_sha256": record[
                "selected_formal_solution_sha256"],
            "selected_coordinate": record["selected_coordinate"],
            "pivot_epoch_owner": {"pivot_hex": record["pivot_hex"],
                "rank_before": record["rank_before"],
                "rank_after": record["rank_after"]}},
        "correction": {"Q": support["K"], "c": record.get("coefficient", 1),
            "s": record["dual_pairing"],
            "weighted_formula": provenance["weighted_formula"],
            "support_hitting": support,
            "base_word": section["selected_base_word"],
            "delta_word": provenance["delta_word"],
            "ten_coordinate_replay": provenance["delta_coordinate_blobs_hex"],
            "direct_column_replay": {key: provenance[key] for key in (
                "conjugate_word", "corrected_word", "quotient_value_blobs",
                "eleven_occurrence_replay", "direct_all_seven_replay")}},
        "validator_result": {"ordinary_validator_schema": SCHEMA +
            "/selected-correction-selftest-frame",
            "positive_local_predicates": ["q0_gamma_k0_replay",
                "least_qid_gid", "kernel_word_state_replay", "dual_pairing",
                "recovery_v2", "direct_column_replay"]}}


def checker_validate_selected_frame(runtime: dict[str, Any],
                                    frame: dict[str, Any],
                                    receipt: dict[str, Any]) -> None:
    """Checker-local ordinary validator for the selected physical K=0 owner."""
    checker_validator_event(runtime, "validate_selected_frame",
                            "selected_frame", "selected-correction-selftest-frame")
    validate_seal(frame)
    checker_validator_event(runtime, "validate_selected_frame",
                            "heavy_identity", "selected.frame.heavy_public")
    require(set(frame) == {"schema", "record", "recovery", "heavy_input_sha256",
            "heavy_public", "target", "producer_sparse_equality",
            "boundary_preimage", "validator", "source_snapshots",
            "final_heavy_carrier", "h_final", "final_heavy_identity_public",
            "final_heavy_identity_sha256", "self_digest"} and
            frame.get("schema") == SCHEMA + "/selected-correction-selftest-frame" and
            frame.get("heavy_input_sha256") == receipt.get("heavy_input_sha256") and
            type(frame.get("heavy_public")) is dict and
            frame.get("heavy_input_sha256") == sha_obj(frame.get("heavy_public")) and
            frame.get("source_snapshots") == Sources.public() and
            frame.get("final_heavy_carrier") == receipt.get("final_heavy_carrier") and
            frame.get("h_final") == receipt.get("h_final") and
            frame.get("target") == frame.get("record", {}).get("sparse_row") and
            frame.get("producer_sparse_equality") is True and
            frame.get("boundary_preimage") == [] and
            frame.get("record", {}).get("coefficient") == 1,
            "selected-correction frame")
    selected_provenance = frame.get("record", {}).get("provenance")
    require(type(selected_provenance) is dict and
            selected_provenance.get("support_hitting", {}).get("K") == 0,
            "checker selected actual K0 owner")
    checker_prepare_k0_coordinate_groups(runtime, [{"record": frame["record"]}])
    p0_public = runtime.get("_checker_p0_public")
    p0_sources = runtime.get("_checker_p0_sources")
    require(type(p0_public) is dict and type(p0_sources) is dict,
            "checker local P0 carrier owner")
    owner_pre = runtime.get("owner_preselection")
    owner_pre_sha = runtime.get("owner_preselection_sha256")
    require(type(owner_pre) is dict and type(owner_pre_sha) is str,
            "checker local OwnerPre carrier")
    identity = {"schema": "r07-a0-final-heavy-carrier/v2",
        "p0": p0_public,
        "p0_self_digest_sha256": p0_public["self_digest_sha256"],
        "sources": p0_sources,
        "frozen_authorities": runtime["_checker_p0_frozen_authorities"],
        "algorithms": {"selected_k0":
            "v12b-coarse-open-address-retained-full-state-first-gid-bfs",
            "correction_validator": SCHEMA +
                "/selected-correction-selftest-frame",
            "canonical_json": "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=True)",
            "digest_framing": "sha256(canonical(H))"},
        "preselection_owner": {"public": owner_pre,
                                "sha256": owner_pre_sha},
        "selected_statement": checker_selected_statement(
            frame["record"])}
    require(frame.get("final_heavy_carrier") == identity and
            frame.get("h_final") == sha_obj(identity) and
            frame.get("final_heavy_identity_public") == identity and
            frame.get("final_heavy_identity_sha256") == sha_obj(identity) and
            receipt.get("final_heavy_carrier") == identity and
            receipt.get("h_final") == sha_obj(identity) and
            identity["p0"] == p0_public and identity["sources"] == p0_sources,
            "final heavy identity")
    require(frame.get("recovery") == runtime.get("recovery_public"),
            "checker selected recovery identity")
    validate_correction_provenance(runtime, frame["record"])
    runtime["_checker_final_heavy_carrier"] = identity
    runtime["_checker_h_final"] = sha_obj(identity)


def _checker_flip_hex(text: str) -> str:
    raw = bytearray.fromhex(str(text))
    require(raw, "checker mutation nonempty hex")
    raw[0] ^= 1
    return raw.hex()


def _checker_selected_mutators() -> dict[str, Any]:
    """Declarative selected-owner mutations routed through the normal validator."""
    def record(frame: dict[str, Any]) -> dict[str, Any]:
        return frame["record"]
    def provenance(frame: dict[str, Any]) -> dict[str, Any]:
        return record(frame)["provenance"]
    def section(frame: dict[str, Any]) -> dict[str, Any]:
        return provenance(frame)["section_provenance"]
    return {
        "selected_q0_roster_state": lambda frame: section(frame).__setitem__(
            "q0_state_hex", _checker_flip_hex(section(frame)["q0_state_hex"])),
        "selected_q0_parent": lambda frame: section(frame).__setitem__(
            "q0_parent_state_id", int(section(frame)["q0_parent_state_id"]) + 1),
        "selected_q0_letter": lambda frame: section(frame)[
            "selected_q0_word"].append(1),
        "selected_marked_generator": lambda frame: section(frame)[
            "selected_marked_generator_row"].__setitem__(0, 2),
        "selected_gamma_state": lambda frame: section(frame).__setitem__(
            "gamma_projected_ten_state_hex",
            _checker_flip_hex(section(frame)["gamma_projected_ten_state_hex"])),
        "selected_gamma_parent": lambda frame: section(frame).__setitem__(
            "gamma_parent_state_id", int(section(frame)["gamma_parent_state_id"]) + 1),
        "selected_gamma_record": lambda frame: section(frame)[
            "selected_gamma_word"].append(1),
        "selected_qid": lambda frame: section(frame).__setitem__(
            "q0_state_id", int(section(frame)["q0_state_id"]) + 1),
        "selected_gid": lambda frame: section(frame).__setitem__(
            "gamma_state_id", int(section(frame)["gamma_state_id"]) + 1),
        "selected_cursor_quotient": lambda frame: section(frame).__setitem__(
            "kernel_cursor", int(section(frame)["kernel_cursor"]) + 1),
        "selected_cursor_remainder": lambda frame: section(frame).__setitem__(
            "support_fibre_cursor", int(section(frame)["support_fibre_cursor"]) + 1),
        "selected_schedule_kind": lambda frame: provenance(frame).__setitem__(
            "schedule", "weighted_global_prefix_W_plus_1"),
        "selected_k0_fibre_nonleast": lambda frame: section(frame).__setitem__(
            "least_q0_state_id", 1 if int(section(frame)["least_q0_state_id"]) != 1 else 2),
        "selected_kernel_order": lambda frame: section(frame).__setitem__(
            "kernel_order", int(section(frame)["kernel_order"]) + 1),
        "selected_heavy_input_identity": lambda frame: frame.__setitem__(
            "heavy_input_sha256", _checker_flip_hex(
                frame["heavy_input_sha256"])),
        "selected_section_word": lambda frame: section(frame)[
            "selected_base_word"].append(1),
        "selected_coefficient_two_inverse_word": lambda frame: provenance(
            frame)["conjugate_word"].append(1),
        "recovery_v1_substitution": lambda frame: provenance(frame)[
            "recovery_v1"].__setitem__("bytes", int(provenance(frame)[
                "recovery_v1"]["bytes"]) + 1),
        "recovery_v2_corrected_field": lambda frame: provenance(frame)[
            "recovery_v2"]["correction"].__setitem__("new_value", "0" * 64),
        "recovery_v2_self_seal": lambda frame: provenance(frame)[
            "recovery_v2"].__setitem__("self_digest_sha256", _checker_flip_hex(
                provenance(frame)["recovery_v2"]["self_digest_sha256"])),
        "q0_parent_letter_roster": lambda frame: section(frame).__setitem__(
            "q0_parent_letter_digest", _checker_flip_hex(
                section(frame)["q0_parent_letter_digest"])),
        "q3_marked_permutation": lambda frame: section(frame)[
            "q3_marked_permutation_rows"][1].__setitem__(0, 3),
        "one_coordinate_mark": lambda frame: section(frame)[
            "selected_coordinate_mark_hex"].__setitem__(0, _checker_flip_hex(
                section(frame)["selected_coordinate_mark_hex"][0])),
        "gamma_parent_record_word": lambda frame: section(frame).__setitem__(
            "gamma_parent_record_id", int(section(frame)["gamma_parent_record_id"]) + 1),
        "gamma_projected_970_byte_state": lambda frame: section(frame).__setitem__(
            "gamma_projected_ten_state_sha256", _checker_flip_hex(
                section(frame)["gamma_projected_ten_state_sha256"])),
        "gamma_full_vs_projected_substitution": lambda frame: section(frame).__setitem__(
            "gamma_full_state_hex", _checker_flip_hex(
                section(frame)["gamma_full_state_hex"])),
        "k0_coarse_key_full_blob_least_base": lambda frame: section(frame).__setitem__(
            "k0_state_digest", _checker_flip_hex(section(frame)["k0_state_digest"])),
        "kernel_generator_order_cursor_word": lambda frame: section(frame)[
            "kernel_generators"].append([1]),
        # Preserve the ordinary direct-column value while changing the
        # unreduced typed product witness; product_order is the first owner
        # that must reject this mutation.
        "product_order": lambda frame: provenance(frame)["delta_word"].extend([1, -1]),
        "heavy_identity_final_row": lambda frame: frame["heavy_public"].__setitem__(
            "light_input_sha256", _checker_flip_hex(frame["heavy_public"][
                "light_input_sha256"])),
    }


def checker_selected_correction_mutations(runtime: dict[str, Any],
                                          receipt: dict[str, Any],
                                          root: Path) -> list[dict[str, Any]]:
    fixture = load_fixture_bounded()
    frame = receipt.get("selftest", {}).get("selected_correction_seed")
    require(type(frame) is dict, "checker selected correction seed")
    baseline_revalidated = False
    checker_validate_selected_frame(runtime, frame, receipt)
    baseline_revalidated = True
    contract = {row["id"]: row for row in fixture["mutation_contract"][
        "selected_correction"]}
    names = fixture["selected_correction_mutations"]
    mutators = _checker_selected_mutators()
    require(list(contract) == names and set(mutators) == set(contract),
            "checker selected mutation contract")
    baseline = sha_bytes(canonical(frame) + b"\n")
    ledger: list[dict[str, Any]] = []
    for ordinal, name in enumerate(names):
        value = clone(frame); mutators[name](value); value = seal(value)
        path = root / f"selected-{ordinal:02d}.json"
        before, after, reason = checker_mutation_trace(
            path, value,
            lambda candidate: checker_validate_selected_frame(runtime, candidate,
                                                               receipt),
            baseline_value=frame, trace_runtime=runtime)
        require(reason, "checker selected mutation did not reject:" + name)
        expected = contract[name]
        require(reason == expected["first_reason"],
                "checker selected first reason:" + name + ":" + reason)
        events = runtime.get("_active_validator_events", [])
        require(events and all(type(event) is dict for event in events),
                "checker selected validator event trace")
        rejection_event = events[-1]
        terminal_count = int(runtime.get("_terminal_count", 0))
        owner_disposed = bool(runtime.get("_last_owner_disposed"))
        require(terminal_count == 1 and owner_disposed,
                "checker selected measured terminal/owner:" + name)
        ledger.append({"id": name, "owner_path": expected["owner_path"],
            "identity_kind": "canonical_frame",
            "before_identity": {"kind": "canonical_frame", "sha256": before},
            "after_identity": {"kind": "canonical_frame", "sha256": after},
            "event_trace_digest": sha_obj(events),
            "entered_validators": [event["validator"] for event in events],
            "first_rejection": {"validator": rejection_event["validator"],
                "stage": rejection_event["stage"], "narrow_reason": reason},
            "baseline_revalidated": baseline_revalidated,
            "terminal_count": terminal_count,
            "owner_disposed": owner_disposed,
            "validator": rejection_event["validator"],
            "stage": rejection_event["stage"],
            "reseal": expected["reseal"], "before_sha256": before,
            "after_sha256": after,
            "reached_validator": rejection_event["validator"],
            "first_reason": reason})
    return ledger


def _validate_contract_ledger(value: Any, fixture: dict[str, Any],
                              group: str, field: str) -> None:
    contract = fixture["mutation_contract"][group]
    rows = value.get(field)
    require(type(rows) is list and [row.get("id") for row in rows] ==
            [row["id"] for row in contract], group + " mutation roster")
    for actual, expected in zip(rows, contract):
        require(type(actual) is dict and
                actual.get("owner_path") == expected["owner_path"] and
                actual.get("validator") == expected["validator"] and
                actual.get("stage") == expected["stage"] and
                actual.get("reseal") is expected["reseal"] and
                type(actual.get("before_sha256")) is str and
                len(actual["before_sha256"]) == 64 and
                type(actual.get("after_sha256")) is str and
                len(actual["after_sha256"]) == 64 and
                type(actual.get("reached_validator")) is str and
                actual.get("reached_validator") and
                actual.get("reached_validator") == expected["validator"] and
                actual.get("baseline_revalidated") is True and
                actual.get("terminal_count") == 1 and
                actual.get("owner_disposed") is True and
                actual.get("first_reason") == expected["first_reason"],
                group + " exact mutation contract:" + str(expected["id"]))
        rejection = actual.get("first_rejection")
        require(type(rejection) is dict and
                rejection.get("validator") == expected["validator"] and
                rejection.get("stage") == expected["stage"] and
                rejection.get("narrow_reason") == expected["first_reason"],
                group + " observed rejection trace:" + str(expected["id"]))
        if group == "physical":
            projection_keys = {
                "logical_case_path", "owner_kind", "byte_length",
                "content_sha256", "link_count_before", "link_count_after",
                "symlink_or_reparse", "logical_link_target",
                "single_open_handle", "opened_handle_stable",
                "pathname_matches_opened_handle", "substitution_detected",
                "canonical_before_sha256", "canonical_after_sha256",
                "resealed_logical_nodes", "entered_validators",
                "event_trace_digest", "first_typed_rejection"}
            require(set(actual["before_identity"]) == projection_keys and
                    set(actual["after_identity"]) == projection_keys,
                    "physical deterministic projection schema:" +
                    str(expected["id"]))


def _validate_positive_gate_ledger(value: Any, fixture: dict[str, Any],
                                   field: str) -> None:
    contract = fixture["mutation_contract"]["phase_positive_gates"]
    rows = value.get(field)
    require(type(rows) is list and [row.get("id") for row in rows] ==
            [row["id"] for row in contract], "phase positive-gate roster")
    for actual, expected in zip(rows, contract):
        require(type(actual) is dict and
                actual.get("owner_path") == expected["owner_path"] and
                actual.get("validator") == expected["validator"] and
                actual.get("stage") == expected["stage"] and
                actual.get("reseal") is expected["reseal"] and
                actual.get("positive_gate") is True and
                actual.get("ordinary_pass") is True and
                actual.get("first_rejection") is None and
                actual.get("first_reason") is None and
                type(actual.get("before_identity")) is dict and
                actual.get("before_identity") == actual.get("after_identity"),
                "phase positive-gate evidence:" + str(expected["id"]))


def validate_selftest_v12b(runtime: dict[str, Any], receipt: dict[str, Any]) -> None:
    """Validate producer's physical owner ledgers, not a shaped transcript."""
    fixture = load_fixture_bounded()
    value = receipt.get("selftest")
    require(type(value) is dict and
            value.get("fixture_sha256") == SOURCE_PINS["fixture"][2] and
            value.get("real_owner_not_shaped_transcript") is True and
            "boundary_mutations_committed_to_checker" not in value and
            "positive_mutations_committed_to_checker" not in value and
            "physical_mutations_committed_to_checker" not in value,
            "selftest producer owner envelope")
    require(value.get("mutation_contract_sha256") ==
            sha_obj(fixture["mutation_contract"]),
            "selftest mutation contract seal")
    _validate_contract_ledger(value, fixture, "triangular",
                              "triangular_mutation_ledger")
    _validate_contract_ledger(value, fixture, "boundary",
                              "boundary_mutation_ledger")
    _validate_contract_ledger(value, fixture, "selected_correction",
                              "selected_correction_mutation_ledger")
    _validate_contract_ledger(value, fixture, "positive",
                              "positive_mutation_ledger")
    _validate_contract_ledger(value, fixture, "physical",
                              "physical_mutation_ledger")
    _validate_contract_ledger(value, fixture, "phase", "phase_mutation_ledger")
    _validate_positive_gate_ledger(value, fixture, "phase_positive_gate_ledger")
    require(type(value.get("triangular_owner_baseline_sha256")) is str,
            "selftest triangular snapshot baseline identity")
    frame = value.get("selected_correction_seed")
    require(type(frame) is dict, "selftest selected owner seed")
    checker_validate_selected_frame(runtime, frame, receipt)
    processes = value.get("process_owner")
    require(type(processes) is dict and
            processes.get("actual_E3_E4_codec") is True and
            processes.get("actual_process_owner") is True and
            processes.get("W2_W4") is True and
            processes.get("blocked_send", {}).get("deadline_rejected") is True and
            processes.get("blocked_send", {}).get("cleanup_complete") is True and
            processes.get("blocked_send", {}).get("process_close") is True,
            "selftest process owner")
    dual = parse_sparse(processes.get("first_dual"))
    require(len(dual) == 1188 and processes.get("first_dual_sha256") ==
            sha_obj(public_sparse(dual)), "selftest first dual owner")
    runs = processes.get("runs")
    require(type(runs) is list and {int(row.get("workers")) for row in runs} ==
            {2, 4}, "selftest worker matrix")
    for run in runs:
        workers = int(run.get("workers"))
        cleanup = run.get("cleanup", {})
        require(cleanup.get("complete") is True and
                cleanup.get("live_pids_after_join") == [] and
                cleanup.get("process_close_count") == workers and
                cleanup.get("process_close") is True and
                "started_pids" not in cleanup and
                "worker_exitcodes" not in cleanup,
                "selftest deterministic cleanup")
        if run.get("fault") is not None:
            require(run["fault"] in ("timeout", "death", "partial") and
                    run.get("atomic_discard") is True,
                    "selftest fault owner")
        else:
            require(type(run.get("probes")) is list and
                    type(run.get("three_serial_outcomes")) is list and
                    len(run["three_serial_outcomes"]) == 3 and
                    type(run.get("accounting")) is dict and
                    run["accounting"].get("composition") ==
                        "additive counters sum; physical gauges max" and
                    run["accounting"].get("completed_additive", {}).get(
                        "stop_frames_sent") == workers and
                    run["accounting"].get("completed_additive", {}).get(
                        "stop_frames_received") == workers,
                    "selftest normal owner")
    cumulative = processes.get("cumulative_accounting")
    require(type(cumulative) is dict and
            cumulative.get("normal_owner_count") == 2 and
            cumulative.get("normal_owner_transitions") == 1 and
            cumulative.get("fault_owner_count") == 3 and
            cumulative.get("blocked_send_owner_count") == 1 and
            cumulative.get("simultaneous_child_peak") == 4 and
            cumulative.get("composition") ==
                "all normal/fault counters additive; physical gauges max" and
            cumulative.get("completed_additive", {}).get(
                "stop_frames_sent") == 6 and
            cumulative.get("completed_additive", {}).get(
                "stop_frames_received") == 6,
            "selftest cumulative IPC/STOP owner")
    require(value.get("claims") in (None, FALSE_CLAIMS),
            "selftest no claims telemetry")


def validate_selftest_envelope(receipt: dict[str, Any],
                               trace_runtime: dict[str, Any] | None = None
                               ) -> dict[str, Any]:
    meter = trace_runtime.get("_checker_meter") if isinstance(
        trace_runtime, dict) else None
    if not isinstance(meter, CheckerMeter):
        meter = None
    physical_trace = trace_runtime is not None and \
        "_physical_logical_label" in trace_runtime
    checker_validator_event(trace_runtime, "selftest_envelope" if physical_trace else
                            "validate_selftest_envelope",
                            "identity_envelope" if physical_trace else
                            "receipt", "receipt")
    require(type(trace_runtime) is dict and
            type(trace_runtime.get("_checker_p0_value")) is dict and
            type(trace_runtime.get("_checker_p0_identity")) is dict,
            "SELFTEST cached P0 snapshot")
    p0_path = ROOT / "ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.manifest.v1.json"
    p0 = trace_runtime["_checker_p0_value"]
    p0_identity = trace_runtime["_checker_p0_identity"]
    p0_body = dict(p0); p0_claimed = p0_body.pop("self_digest_sha256", None)
    require(p0.get("schema") ==
            "d972-r07-history-free-positive-fast-resume/selftest-bootstrap-manifest/v1" and
            p0.get("mode") == "SELFTEST_BOOTSTRAP" and
            p0.get("status") == "COMPLETE" and
            p0.get("execution") == "UNEXECUTED" and
            p0.get("candidate_only") is True and
            p0.get("production_authorized") is False and
            p0.get("resume_authorized") is False and
            p0.get("acceptance_preregistration") is False and
            p0.get("requires_v12b_physical_pin") is True and
            type(p0_claimed) is str and p0_claimed == sha_obj(p0_body),
            "SELFTEST P0 identity")
    rows = p0.get("sources")
    expected_paths = {
        "producer_v12b": "search/d972_r07_history_free_positive_fast_resume_v12b.py",
        "checker_v12b": "crosscheck/check_d972_r07_history_free_positive_fast_resume_v12b.py",
        "fixture_v12b": FIXTURE_PATH,
    }
    require(type(rows) is dict and set(rows) == set(expected_paths),
            "SELFTEST P0 source roster")
    for key, path in expected_paths.items():
        row = rows[key]
        require(row.get("path") == path and type(row.get("bytes")) is int and
                type(row.get("sha256")) is str and len(row["sha256"]) == 64,
                "SELFTEST P0 source row:" + key)
        require(trace_runtime.get("_checker_p0_sources", {}).get(key) == row,
                "SELFTEST cached P0 source row:" + key)
    require(receipt.get("schema") == SCHEMA + "/selftest-bootstrap" and
            receipt.get("status") == "CANDIDATE_ONLY" and
            receipt.get("terminal") == SELFTEST_TERMINAL and
            receipt.get("mode") == "SELFTEST_BOOTSTRAP" and
            receipt.get("candidate_only") is True and
            receipt.get("production_authorized") is False and
            receipt.get("requires_v12b_physical_pin") is True and
            "checkpoint" not in receipt and
            receipt.get("execution") == "SELFTEST_BOOTSTRAP_COMPLETE_CANDIDATE" and
            receipt.get("claims") == FALSE_CLAIMS and
            receipt.get("no_acceptance_or_negative_claim") is True and
            type(receipt.get("selftest")) is dict,
            "SELFTEST identity envelope")
    semantic_body = dict(receipt)
    semantic_body.pop("self_digest", None)
    semantic_claim = semantic_body.pop("semantic_digest", None)
    require(type(semantic_claim) is str and
            semantic_claim == sha_obj(semantic_body),
            "SELFTEST receipt semantic digest")
    p0_reference = receipt.get("p0")
    require(type(p0_reference) is dict and
            p0_reference.get("path") == str(p0_path.relative_to(ROOT)).replace("\\", "/") and
            p0_reference.get("semantic_schema") == p0["schema"] and
            p0_reference.get("self_digest_sha256") == p0_claimed and
            p0_reference.get("physical_sha256") == p0_identity["sha256"],
            "SELFTEST P0 receipt binding")
    return {"selftest": True, "production_invocations": 0,
            "mathematical_terminal": False, "p0_self_digest": p0_claimed,
            "p0_physical_sha256": p0_identity["sha256"]}


def validate_receipt_heavy_seal(receipt: dict[str, Any]) -> None:
    """Check the transported diagnostic seal without making it H authority."""
    heavy = receipt.get("heavy_public")
    require(type(heavy) is dict and
            receipt.get("heavy_input_sha256") == sha_obj(heavy),
            "receipt diagnostic heavy seal")


def validate_p0_checker(path: Path,
                        meter: CheckerMeter | None = None
                        ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Open and bind P0 before any checker owner is reconstructed."""
    value, raw, physical = open_physical(path, 16 * 1024 * 1024,
                                         meter=meter)
    body = dict(value); claimed = body.pop("self_digest_sha256", None)
    require(value.get("schema") ==
            "d972-r07-history-free-positive-fast-resume/selftest-bootstrap-manifest/v1" and
            value.get("mode") == "SELFTEST_BOOTSTRAP" and
            value.get("status") == "COMPLETE" and
            value.get("execution") == "UNEXECUTED" and
            value.get("candidate_only") is True and
            value.get("production_authorized") is False and
            value.get("resume_authorized") is False and
            value.get("acceptance_preregistration") is False and
            value.get("requires_v12b_physical_pin") is True and
            type(claimed) is str and claimed == sha_obj(body),
            "checker P0 bootstrap identity")
    require(value.get("platform_contract", {}).get("gha_runner") ==
                "ubuntu-24.04" and
            value.get("platform_contract", {}).get(
                "typed_preflight_before_heavy_load") is True and
            value.get("deadline_contract") == {"producer_internal": 9600,
                "producer_external": 9900, "checker_internal": 5400,
                "checker_external": 5700, "artifact_internal": 1200,
                "artifact_external": 1500, "external_sum": 17100,
                "outer": 18000, "outer_margin": 900, "workflow": 21600,
                "setup_cleanup_upload_margin": 3600} and
            value.get("resource_contract", {}).get(
                "simultaneous_child_peak") == 4,
            "checker P0 platform/resource/deadline contract")
    authenticated: dict[str, tuple[bytes, dict[str, Any]]] = {}
    def snapshot(relative: str, size: int, digest: str
                 ) -> tuple[bytes, dict[str, Any]]:
        if relative not in authenticated:
            authenticated[relative] = read_owner_bytes(
                ROOT / relative, size, digest, meter)
        raw0, identity0 = authenticated[relative]
        require(len(raw0) == size and identity0["sha256"] == digest,
                "checker shared snapshot identity:" + relative)
        return raw0, identity0

    paths = {"producer_v12b":
                "search/d972_r07_history_free_positive_fast_resume_v12b.py",
        "checker_v12b":
                "crosscheck/check_d972_r07_history_free_positive_fast_resume_v12b.py",
        "fixture_v12b": FIXTURE_PATH}
    rows = value.get("sources")
    require(type(rows) is dict and set(rows) == set(paths),
            "checker P0 source graph")
    for key, relative in paths.items():
        row = rows[key]
        require(row.get("path") == relative and type(row.get("bytes")) is int and
                row["bytes"] > 0 and type(row.get("sha256")) is str and
                len(row["sha256"]) == 64, "checker P0 source row:" + key)
        source_raw, source_identity = snapshot(
            relative, row["bytes"], row["sha256"])
        require(len(source_raw) == row["bytes"] and
                source_identity["sha256"] == row["sha256"],
                "checker P0 physical source:" + key)
    expected_frozen = dict(SOURCE_PINS)
    expected_frozen.update({
        "raw_checkpoint": (RAW_SOURCE_PATH, RAW_BYTES, RAW_SHA256),
        "checkpoint_archive": (RAW_ARCHIVE_PATH, RAW_ARCHIVE_BYTES,
                                RAW_ARCHIVE_SHA256)})
    frozen = value.get("frozen_authorities")
    require(type(frozen) is dict and set(frozen) == set(expected_frozen),
            "checker P0 frozen authority roster")
    for key, (relative, size, digest) in expected_frozen.items():
        row = frozen[key]
        require(type(row) is dict and row.get("path") == relative and
                row.get("bytes") == size and row.get("sha256") == digest,
                "checker P0 frozen authority row:" + key)
        source_raw, source_identity = snapshot(relative, size, digest)
        require(len(source_raw) == size and source_identity["sha256"] == digest,
                "checker P0 physical frozen authority:" + key)
    raw_checkpoint_bytes = authenticated[RAW_SOURCE_PATH][0]
    if meter is not None:
        meter.reserve(RAW_BYTES * 2, "raw_checkpoint_ascii_and_dom")
    try:
        raw_checkpoint = json.loads(raw_checkpoint_bytes.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CheckStop("checker raw checkpoint JSON") from exc
    require(type(raw_checkpoint) is dict, "checker raw checkpoint object")
    fixture_bytes = authenticated[FIXTURE_PATH][0]
    try:
        fixture = json.loads(fixture_bytes.decode("ascii"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CheckStop("checker fixture JSON") from exc
    source_raws = {key: authenticated[row[0]][0]
                   for key, row in SOURCE_PINS.items()}
    snapshots = {"source_raws": source_raws,
                 "raw_checkpoint": raw_checkpoint, "fixture": fixture}
    return value, {"path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "bytes": len(raw), "sha256": sha_bytes(raw),
        "self_digest_sha256": claimed, "physical": physical}, snapshots


def checker_estimated_json_size(value: Any) -> int:
    if value is None or isinstance(value, (bool, int, float, str)):
        return len(canonical(value))
    if isinstance(value, dict):
        return 2 + sum(len(canonical(str(key))) +
                       checker_estimated_json_size(item) + 2
                       for key, item in value.items())
    if isinstance(value, (list, tuple)):
        return 2 + sum(checker_estimated_json_size(item) + 1 for item in value)
    return len(canonical(value))


def exclusive_json(path: Path, value: dict[str, Any],
                   trace_runtime: dict[str, Any] | None = None) -> tuple[int, str]:
    checker_validator_event(trace_runtime, "exclusive_json", "stale",
                            "candidate.path")
    try:
        parent_before = os.stat(path.parent, follow_symlinks=False)
    except OSError as exc:
        raise CheckStop("publication parent unavailable") from exc
    require(stat.S_ISDIR(parent_before.st_mode) and
            not stat.S_ISLNK(parent_before.st_mode),
            "publication parent is not a regular directory")
    if path.exists():
        raise CheckStop("stale output")
    reserved = checker_estimated_json_size(value) + 1
    require(0 < reserved <= MAX_CANDIDATE_BYTES,
            "checker publication hard byte cap")
    meter = trace_runtime.get("_checker_meter") if isinstance(
        trace_runtime, dict) else None
    if isinstance(meter, CheckerMeter):
        meter.reserve(reserved, "verdict_publication_reserve")
    raw = canonical(value) + b"\n"
    require(len(raw) <= MAX_CANDIDATE_BYTES,
            "checker publication hard byte cap")
    temporary = path.with_name(path.name + ".tmp." + str(os.getpid()))
    try:
        with temporary.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        # Publish with an atomic no-replace link.  A target created between
        # the precheck and this call is never overwritten.
        try:
            os.link(temporary, path)
        except FileExistsError as exc:
            raise CheckStop("stale output") from exc
        except OSError as exc:
            raise CheckStop("exclusive publication") from exc
        temporary.unlink()
        try:
            parent_after = os.stat(path.parent, follow_symlinks=False)
        except OSError as exc:
            raise CheckStop("publication parent disappeared") from exc
        require((parent_after.st_dev, parent_after.st_ino,
                 parent_after.st_mode) ==
                (parent_before.st_dev, parent_before.st_ino,
                 parent_before.st_mode),
                "publication parent identity changed")
        try:
            directory_fd = os.open(path.parent, os.O_RDONLY |
                                   getattr(os, "O_DIRECTORY", 0))
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except OSError as exc:
            raise CheckStop("publication directory fsync") from exc
    finally:
        try: temporary.unlink()
        except FileNotFoundError: pass
        if trace_runtime is not None:
            trace_runtime["_last_owner_disposed"] = True
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


def validate_boundary_frame(runtime: dict[str, Any], frame: dict[str, Any]) -> None:
    checker_validator_event(runtime, "validate_boundary_frame", "boundary",
                            "boundary-selftest-frame")
    validate_seal(frame)
    require(set(frame) == {"schema", "workers", "dual", "outcome",
            "orientation", "transport", "counter_floor", "self_digest"},
            "boundary selftest schema")
    checker_validator_event(runtime, "validate_boundary_frame",
                            "typed_support", "boundary.dual")
    dual = parse_sparse(frame.get("dual"))
    require(public_sparse(dual) == frame.get("dual"), "sparse item")
    try:
        for key in dual:
            if key[:1] == b"R":
                decode_row_key(key)
            else:
                require(key in (exponent_key(1), exponent_key(2)),
                        "sparse item")
    except CheckStop:
        raise CheckStop("sparse item")
    require(frame.get("schema") == SCHEMA + "/boundary-selftest-frame",
            "boundary selftest owner frame")
    checker_validator_event(runtime, "validate_boundary_frame",
                            "orientation", "boundary.orientation")
    require(frame.get("orientation") == "t=g*h^-1;t*h=g",
            "boundary selftest owner frame")
    checker_validator_event(runtime, "validate_boundary_frame",
                            "transport", "boundary.transport")
    require(frame.get("transport") == runtime.get(
                "_checker_boundary_transport_expected"),
            "boundary selftest owner frame")
    checker_validator_event(runtime, "validate_boundary_frame",
                            "counter", "boundary.counter_floor")
    require(frame.get("counter_floor") == frame.get("outcome", {}).get(
                "expanded_pair_count"), "boundary selftest owner frame")
    expected = runtime.get("_checker_boundary_expected")
    if expected is None:
        dual = parse_sparse(frame.get("dual")); workers = int(frame.get("workers"))
        epoch = int(frame.get("outcome", {}).get("epoch"))
        expected = independent_boundary_outcome(runtime, dual, workers, epoch)
        runtime["_checker_boundary_expected"] = expected
    outcome = frame.get("outcome")
    require(type(outcome) is dict, "boundary selftest independent outcome")
    # The ordinary outcome validator records the first differing owner field;
    # no mutation name is used to manufacture a reached-validator trace.
    for field, stage in (("epoch", "epoch"), ("intervals", "interval_partition"),
                         ("worker_results", "result_digest"),
                         ("selected", "winner"),
                         ("selected_scalar", "scalar")):
        if outcome.get(field) != expected.get(field):
            checker_validator_event(runtime, "independent_boundary_outcome",
                                    stage, "boundary.outcome")
            raise CheckStop("boundary selftest immutable ordinary outcome")
    if outcome != expected:
        checker_validator_event(runtime, "independent_boundary_outcome",
                                "result_digest", "boundary.outcome")
        raise CheckStop("boundary selftest immutable ordinary outcome")


def checker_mutation_trace(path: Path, value: dict[str, Any],
                           validator: Any,
                           baseline_value: dict[str, Any] | None = None,
                           baseline_sha256: str | None = None,
                           trace_runtime: dict[str, Any] | None = None
                           ) -> tuple[str, str, str]:
    """Physical write/open/read followed by one ordinary validator call."""
    raw = canonical(value) + b"\n"
    before = (baseline_sha256 if baseline_sha256 is not None else sha_bytes(
        canonical(baseline_value if baseline_value is not None else value) + b"\n"))
    if trace_runtime is not None:
        trace_runtime["_active_validator_events"] = []
        trace_runtime["_last_owner_disposed"] = False
        trace_runtime["_terminal_count"] = 0
    write_frame(path, value)
    try:
        try:
            candidate, _candidate_raw, physical = open_physical(
                path, MAX_CANDIDATE_BYTES, trace_runtime=trace_runtime)
        except CheckStop as exc:
            if trace_runtime is not None:
                trace_runtime["_terminal_count"] = int(
                    trace_runtime.get("_terminal_count", 0)) + 1
            return before, sha_bytes(raw), str(exc)
        try:
            validator(candidate)
        except CheckStop as exc:
            if trace_runtime is not None:
                trace_runtime["_terminal_count"] = int(
                    trace_runtime.get("_terminal_count", 0)) + 1
            if trace_runtime is not None:
                _checker_physical_projection_reason(trace_runtime, str(exc))
            return before, physical["sha256"], str(exc)
        raise CheckStop("physical mutation accepted:" + path.name)
    finally:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        if trace_runtime is not None:
            trace_runtime["_last_owner_disposed"] = not path.exists()


def checker_triangular_mutation_ledger(runtime: dict[str, Any],
                                       receipt: dict[str, Any],
                                       root: Path) -> list[dict[str, Any]]:
    """Replay every triangular owner mutation through the ordinary checker.

    The producer's compact certificate is the transported physical owner on
    this side; no fixture transcript is accepted as a substitute.
    """
    fixture = load_fixture_bounded()
    baseline = runtime.get("_triangular_snapshot")
    require(type(baseline) is dict, "checker raw triangular snapshot")
    baseline_revalidated = False
    _checker_validate_triangular_owner_frame(baseline)
    baseline_revalidated = True
    contract = {row["id"]: row for row in fixture["mutation_contract"][
        "triangular"]}
    names = fixture["triangular_mutations"]
    require(list(contract) == names, "checker triangular mutation contract")
    before = sha_bytes(canonical(baseline) + b"\n")
    require(receipt.get("selftest", {}).get(
        "triangular_owner_baseline_sha256") == before,
        "checker triangular baseline identity")
    original_prefix = clone(baseline["columns"][:3])
    ledger: list[dict[str, Any]] = []
    for ordinal, name in enumerate(names):
        for index in range(3):
            baseline["columns"][index] = clone(original_prefix[index])
        value = baseline
        if name == "future_ancestry_index":
            value["columns"][1]["pivot_ancestry"].append([7, 1])
        elif name == "zero_diagonal":
            value["columns"][1]["pivot_ancestry"] = [item for item in
                value["columns"][1]["pivot_ancestry"] if item[0] != 2]
        elif name == "changed_raw_sparse_entry":
            row = value["columns"][0]["sparse_row"]
            row[0][1] = 3 - int(row[0][1])
            value["columns"][0]["sparse_row_sha256"] = sha_obj(row)
        elif name == "changed_ancestry_coefficient":
            value["columns"][1]["pivot_ancestry"][0][1] = 3 - int(
                value["columns"][1]["pivot_ancestry"][0][1])
        elif name == "duplicate_pivot":
            value["columns"][1]["pivot_hex"] = value["columns"][0]["pivot_hex"]
        elif name == "wrong_pivot":
            value["columns"][2]["pivot_hex"] = "00"
        elif name == "hidden_smaller_pivot":
            value["columns"][2]["pivot_hex"] = value["columns"][2][
                "sparse_row"][-1][0]
        elif name == "skipped_P_equation":
            non_diagonal = next(index for index, item in enumerate(
                value["columns"][2]["pivot_ancestry"]) if item[0] != 3)
            value["columns"][2]["pivot_ancestry"].pop(non_diagonal)
        else:
            raise CheckStop("unknown triangular mutation")
        value = seal(value)
        expected = contract[name]
        trace_runtime: dict[str, Any] = {}
        path = root / f"triangular-{ordinal:02d}.json"
        _before, after, reason = checker_mutation_trace(
            path, value,
            lambda candidate: _checker_validate_triangular_owner_frame(
                candidate, trace_runtime), baseline_sha256=before,
            trace_runtime=trace_runtime)
        require(_before == before,
                "checker triangular baseline identity mismatch:" + name)
        require(reason == expected["first_reason"],
                "checker triangular first reason:" + name + ":" + reason)
        require(before != after, "checker triangular identity unchanged:" + name)
        events = trace_runtime.get("_active_validator_events", [])
        require(events and all(type(event) is dict for event in events),
                "checker triangular validator event trace")
        rejection_event = events[-1]
        terminal_count = int(trace_runtime.get("_terminal_count", 0))
        owner_disposed = bool(trace_runtime.get("_last_owner_disposed"))
        require(terminal_count == 1 and owner_disposed,
                "checker triangular measured terminal/owner:" + name)
        ledger.append({"id": name, "owner_path": expected["owner_path"],
            "identity_kind": "canonical_frame",
            "before_identity": {"kind": "canonical_frame", "sha256": before},
            "after_identity": {"kind": "canonical_frame", "sha256": after},
            "event_trace_digest": sha_obj(events),
            "entered_validators": [event["validator"] for event in events],
            "first_rejection": {"validator": rejection_event["validator"],
                "stage": rejection_event["stage"], "narrow_reason": reason},
            "baseline_revalidated": baseline_revalidated,
            "terminal_count": terminal_count, "owner_disposed": owner_disposed,
            "validator": rejection_event["validator"],
            "stage": rejection_event["stage"],
            "reseal": expected["reseal"], "before_sha256": before,
            "after_sha256": after, "reached_validator":
                rejection_event["validator"], "first_reason": reason})
    baseline["columns"].clear()
    runtime["_triangular_snapshot"] = None
    runtime["_raw_checkpoint_released"] = True
    return ledger


def checker_boundary_mutation_ledger(runtime: dict[str, Any],
                                     receipt: dict[str, Any],
                                     root: Path) -> list[dict[str, Any]]:
    fixture = load_fixture_bounded()
    processes = receipt["selftest"]["process_owner"]
    dual = parse_sparse(processes["first_dual"]); workers = 4
    checker_processes = runtime.get("_checker_process_owner")
    require(type(checker_processes) is dict,
            "checker extant process owner")
    owner_run = next(row for row in checker_processes["runs"]
                     if row.get("workers") == workers and
                     row.get("fault") is None)
    outcome = owner_run.get("outcome")
    require(type(outcome) is dict and owner_run.get("outcome_sha256") ==
            sha_obj(outcome), "checker extant boundary outcome")
    runtime["_checker_boundary_expected"] = outcome
    normal_transport = {"route": "normal", "workers": workers,
        "outcome_sha256": owner_run["outcome_sha256"],
        "accounting": owner_run["accounting"],
        "cleanup": owner_run["cleanup"]}
    routes = {"blocked_send": {"route": "blocked_send",
        "owner": checker_processes["blocked_send"]}}
    for fault in ("timeout", "death", "partial"):
        fault_run = next(row for row in checker_processes["runs"]
                         if row.get("fault") == fault)
        routes[fault] = {"route": fault, "workers": fault_run["workers"],
            "atomic_discard": fault_run["atomic_discard"],
            "accounting": fault_run["accounting"],
            "cleanup": fault_run["cleanup"]}
    runtime["_checker_boundary_transport_expected"] = normal_transport
    baseline = seal({"schema": SCHEMA + "/boundary-selftest-frame",
        "workers": workers, "dual": public_sparse(dual), "outcome": outcome,
        "orientation": "t=g*h^-1;t*h=g",
        "transport": normal_transport,
        "counter_floor": outcome["expanded_pair_count"]})
    baseline_revalidated = False
    validate_boundary_frame(runtime, baseline)
    baseline_revalidated = True
    contract = {row["id"]: row for row in fixture["mutation_contract"]["boundary"]}
    ledger = []
    for ordinal, name in enumerate(fixture["boundary_mutations"]):
        value = clone(baseline)
        if name == "wrong_typed_support":
            wrong = bytearray.fromhex(value["dual"][0][0]); wrong[1] = 4
            value["dual"][0][0] = bytes(wrong).hex(); value["dual"].sort()
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
                accumulator.append([1, blob(runtime, runtime["e3"].identity).hex(), 1, 1])
        elif name == "changed_winner":
            value["outcome"]["selected"] = None if value["outcome"].get(
                "selected") is not None else [1, blob(runtime,
                runtime["e3"].identity).hex(), 1]
        elif name == "changed_scalar":
            scalar = value["outcome"].get("selected_scalar")
            value["outcome"]["selected_scalar"] = 1 if scalar is None else 3 - int(scalar)
        elif name == "cross_epoch_frame":
            value["outcome"]["epoch"] += 1
        elif name == "blocked_send":
            value["transport"] = routes["blocked_send"]
        elif name == "partial_worker":
            value["transport"] = routes["partial"]
        elif name == "dead_worker":
            value["transport"] = routes["death"]
        elif name == "surviving_process":
            value["transport"]["cleanup"]["live_pids_after_join"] = [1]
        elif name == "counter_reset":
            value["counter_floor"] = 0
        else:
            raise CheckStop("unknown boundary mutation")
        value = reseal(value); expected = contract[name]
        before, after, reason = checker_mutation_trace(
            root / f"boundary-{ordinal:02d}.json", value,
            lambda candidate: validate_boundary_frame(runtime, candidate),
            baseline_value=baseline, trace_runtime=runtime)
        require(reason == expected["first_reason"],
                "checker boundary first reason:" + name + ":" + reason)
        events = runtime.get("_active_validator_events", [])
        require(events and all(type(event) is dict for event in events),
                "checker boundary validator event trace")
        rejection_event = events[-1]
        terminal_count = int(runtime.get("_terminal_count", 0))
        owner_disposed = bool(runtime.get("_last_owner_disposed"))
        require(terminal_count == 1 and owner_disposed,
                "checker boundary measured terminal/owner:" + name)
        ledger.append({"id": name, "owner_path": expected["owner_path"],
            "identity_kind": "canonical_frame",
            "before_identity": {"kind": "canonical_frame", "sha256": before},
            "after_identity": {"kind": "canonical_frame", "sha256": after},
            "event_trace_digest": sha_obj(events),
            "entered_validators": [event["validator"] for event in events],
            "first_rejection": {"validator": rejection_event["validator"],
                "stage": rejection_event["stage"], "narrow_reason": reason},
            "baseline_revalidated": baseline_revalidated,
            "terminal_count": terminal_count,
            "owner_disposed": owner_disposed,
            "validator": rejection_event["validator"],
            "stage": rejection_event["stage"],
            "reseal": expected["reseal"], "before_sha256": before,
            "after_sha256": after, "reached_validator":
                rejection_event["validator"], "first_reason": reason})
    owner_run.pop("outcome", None)
    runtime["_checker_boundary_expected"] = None
    runtime["_checker_boundary_transport_expected"] = None
    return ledger


def checker_validate_positive_frame(runtime: dict[str, Any],
                                    value: dict[str, Any],
                                    receipt: dict[str, Any]) -> None:
    checker_validator_event(runtime, "validate_positive_frame", "positive",
                            "positive-selftest-frame")
    validate_seal(value)
    require(set(value) == {"schema", "selected", "coefficient", "target",
            "boundary_preimage", "producer_sparse_equality",
            "heavy_input_sha256", "heavy_public", "claims", "self_digest"} and
            value.get("schema") == SCHEMA + "/positive-selftest-frame" and
            value.get("claims") == FALSE_CLAIMS and
            "checkpoint" not in value, "checker positive envelope")
    selected = value.get("selected")
    checker_validator_event(runtime, "validate_positive_frame",
                            "selected_support", "positive.selected")
    require(type(selected) is list and len(selected) == 1,
            "SELFTEST selected support complete")
    checker_validator_event(runtime, "validate_positive_frame",
                            "coefficient", "positive.coefficient")
    require(value.get("coefficient") == 1, "SELFTEST selected coefficient")
    checker_validator_event(runtime, "validate_positive_frame",
                            "target", "positive.target")
    require(value.get("target") == selected[0].get("sparse_row"),
            "SELFTEST target/g760")
    checker_validator_event(runtime, "validate_positive_frame",
                            "preimage", "positive.boundary_preimage")
    require(value.get("boundary_preimage") == [],
            "SELFTEST typed preimage/support")
    checker_validator_event(runtime, "validate_positive_frame",
                            "residual", "positive.producer_sparse_equality")
    require(value.get("producer_sparse_equality") is True,
            "SELFTEST typed preimage/support")
    require(type(value.get("heavy_public")) is dict and
            value.get("heavy_input_sha256") ==
                sha_obj(value.get("heavy_public")) and
            value.get("heavy_input_sha256") == receipt.get("heavy_input_sha256") and
            type(receipt.get("heavy_input_sha256")) is str and
            len(receipt.get("heavy_input_sha256")) == 64,
            "checker positive heavy identity")
    frame = clone(receipt["selftest"]["selected_correction_seed"])
    frame["record"] = selected[0]
    checker_validate_selected_frame(runtime, seal(frame), receipt)


def validate_coefficient_two_frame(runtime: dict[str, Any],
                                   value: dict[str, Any]) -> None:
    """Checker-local coefficient-two ordinary validator."""
    checker_validator_event(runtime, "validate_coefficient_two_frame",
                            "coefficient_two", "coefficient-two-frame")
    validate_seal(value)
    require(set(value) == {"schema", "coefficient", "delta_word",
            "relator_word", "stored_row", "target", "factor_word",
            "correction_word", "self_digest"} and
            value.get("schema") == SCHEMA + "/coefficient-two-selftest-frame" and
            value.get("coefficient") == 2,
            "coefficient-two frame")
    model = runtime["model"]
    row, replay = model.direct_column(value["delta_word"],
                                      value["relator_word"])
    inverse_row, inverse_replay = model.direct_column(
        value["delta_word"], inverse_word(value["relator_word"]))
    factor = inverse_word(replay["conjugate_word"])
    require(public_sparse(row) == value.get("stored_row") and
            public_sparse(scaled(row, 2)) == value.get("target") and
            inverse_row == scaled(row, 2) and
            inverse_replay["conjugate_word"] == factor and
            value.get("factor_word") == factor and
            value.get("correction_word") == factor and
            runtime["joint_group"].eval(factor) ==
                runtime["joint_group"].identity,
            "literal coefficient-two inverse word")


def checker_positive_mutation_ledger(runtime: dict[str, Any],
                                     receipt: dict[str, Any], root: Path
                                     ) -> list[dict[str, Any]]:
    fixture = load_fixture_bounded(); seed = receipt["selftest"][
        "selected_correction_seed"]
    baseline = seal({"schema": SCHEMA + "/positive-selftest-frame",
        "selected": [seed["record"]], "coefficient": 1,
        "target": seed["record"]["sparse_row"], "boundary_preimage": [],
        "producer_sparse_equality": True,
        "heavy_input_sha256": receipt["heavy_input_sha256"],
        "heavy_public": receipt["heavy_public"], "claims": dict(FALSE_CLAIMS)})
    baseline_revalidated = False
    checker_validate_positive_frame(runtime, baseline, receipt)
    baseline_revalidated = True
    contract = {row["id"]: row for row in fixture["mutation_contract"]["positive"]}
    ledger = []
    for ordinal, name in enumerate(fixture["positive_mutations"]):
        if name == "wrong_coefficient_two_word":
            selected = seed["record"]; provenance = selected["provenance"]
            row = parse_sparse(selected["sparse_row"])
            value = seal({"schema": SCHEMA + "/coefficient-two-selftest-frame",
                "coefficient": 2, "delta_word": provenance["delta_word"],
                "relator_word": provenance["relator_word"],
                "stored_row": selected["sparse_row"],
                "target": public_sparse(scaled(row, 2)),
                "factor_word": inverse_word(provenance["conjugate_word"]),
                "correction_word": inverse_word(provenance["conjugate_word"]) + [1]})
            validator = lambda candidate: validate_coefficient_two_frame(runtime, candidate)
        else:
            value = clone(baseline)
            if name == "omitted_selected_row":
                value["selected"] = []
            elif name == "changed_selected_row":
                value["selected"][0]["sparse_row"][0][1] = 3 - int(
                    value["selected"][0]["sparse_row"][0][1])
                value["target"] = value["selected"][0]["sparse_row"]
            elif name == "changed_selected_coefficient":
                value["coefficient"] = 2
            elif name == "copied_sparse_equality_boolean":
                value["producer_sparse_equality"] = False
            elif name == "changed_target":
                value["target"][0][1] = 3 - int(value["target"][0][1])
            elif name == "changed_boundary_preimage":
                value["boundary_preimage"].append({"symbol": "o:0000"})
            else:
                raise CheckStop("unknown positive mutation")
            value = seal(value)
            validator = lambda candidate: checker_validate_positive_frame(
                runtime, candidate, receipt)
        expected = contract[name]
        before, after, reason = checker_mutation_trace(
            root / f"positive-{ordinal:02d}.json", value, validator,
            baseline_value=baseline, trace_runtime=runtime)
        require(reason == expected["first_reason"],
                "checker positive first reason:" + name + ":" + reason)
        events = runtime.get("_active_validator_events", [])
        require(events and all(type(event) is dict for event in events),
                "checker positive validator event trace")
        rejection_event = events[-1]
        terminal_count = int(runtime.get("_terminal_count", 0))
        owner_disposed = bool(runtime.get("_last_owner_disposed"))
        require(terminal_count == 1 and owner_disposed,
                "checker positive measured terminal/owner:" + name)
        ledger.append({"id": name, "owner_path": expected["owner_path"],
            "identity_kind": "canonical_frame",
            "before_identity": {"kind": "canonical_frame", "sha256": before},
            "after_identity": {"kind": "canonical_frame", "sha256": after},
            "event_trace_digest": sha_obj(events),
            "entered_validators": [event["validator"] for event in events],
            "first_rejection": {"validator": rejection_event["validator"],
                "stage": rejection_event["stage"], "narrow_reason": reason},
            "baseline_revalidated": baseline_revalidated,
            "terminal_count": terminal_count,
            "owner_disposed": owner_disposed,
            "validator": rejection_event["validator"],
            "stage": rejection_event["stage"],
            "reseal": expected["reseal"], "before_sha256": before,
            "after_sha256": after, "reached_validator":
                rejection_event["validator"], "first_reason": reason})
    return ledger


def checker_path_projection(path: Path, logical_label: str,
                            content_sha256: str | None = None
                            ) -> dict[str, Any]:
    """Project volatile path facts into the deterministic v298 ledger shape."""
    marker = "UNREADABLE_AT_REGISTERED_STAGE"
    try:
        item = os.lstat(path)
    except FileNotFoundError:
        return {"logical_case_path": logical_label, "owner_kind": "missing",
                "byte_length": marker, "content_sha256": marker,
                "link_count_before": None, "link_count_after": None,
                "symlink_or_reparse": False, "logical_link_target": None,
                "single_open_handle": False, "opened_handle_stable": False,
                "pathname_matches_opened_handle": False,
                "substitution_detected": False,
                "canonical_before_sha256": marker,
                "canonical_after_sha256": marker,
                "resealed_logical_nodes": [], "entered_validators": [],
                "event_trace_digest": sha_obj([]),
                "first_typed_rejection": None}
    if stat.S_ISLNK(item.st_mode):
        return {"logical_case_path": logical_label, "owner_kind": "symlink",
                "byte_length": marker, "content_sha256": marker,
                "link_count_before": int(item.st_nlink),
                "link_count_after": int(item.st_nlink),
                "symlink_or_reparse": True,
                "logical_link_target": "physical/baseline",
                "single_open_handle": False, "opened_handle_stable": False,
                "pathname_matches_opened_handle": False,
                "substitution_detected": True,
                "canonical_before_sha256": marker,
                "canonical_after_sha256": marker,
                "resealed_logical_nodes": [], "entered_validators": [],
                "event_trace_digest": sha_obj([]),
                "first_typed_rejection": None}
    kind = "regular" if stat.S_ISREG(item.st_mode) else "other"
    digest = content_sha256 if content_sha256 is not None else marker
    return {"logical_case_path": logical_label, "owner_kind": kind,
            "byte_length": int(item.st_size), "content_sha256": digest,
            "link_count_before": int(item.st_nlink),
            "link_count_after": int(item.st_nlink),
            "symlink_or_reparse": False, "logical_link_target": None,
            "single_open_handle": False, "opened_handle_stable": False,
            "pathname_matches_opened_handle": item.st_nlink == 1,
            "substitution_detected": False,
            "canonical_before_sha256": digest,
            "canonical_after_sha256": digest,
            "resealed_logical_nodes": [], "entered_validators": [],
            "event_trace_digest": sha_obj([]),
            "first_typed_rejection": None}


def checker_transport_mutation_ledger(runtime: dict[str, Any],
                                      receipt: dict[str, Any], root: Path
                                      ) -> list[dict[str, Any]]:
    # Borrow the already authenticated R DOM.  Semantic cases below make a
    # shallow carrier plus a tiny claims copy, never another full R clone.
    fixture = load_fixture_bounded(); baseline = receipt
    validate_selftest_envelope(baseline, runtime)
    contract = {row["id"]: row for row in fixture["mutation_contract"]["physical"]}
    base_raw = canonical(baseline) + b"\n"; base_sha = sha_bytes(base_raw)
    ledger = []
    for ordinal, name in enumerate(fixture["physical_mutations"]):
        # Every row receives a fresh baseline owner.  A hard-link case must
        # not alter the link count or ownership evidence of a later row.
        base = root / f"physical-base-{ordinal:02d}.json"
        write_frame(base, baseline)
        path = root / f"physical-{ordinal:02d}.json"; expected = contract[name]
        # Keep the baseline and mutant in one logical case namespace.  The
        # deterministic comparison must not report a label/path change as a
        # physical mutation.
        baseline_identity = checker_path_projection(base, name, base_sha)
        runtime["_active_validator_events"] = []
        runtime["_last_owner_disposed"] = False
        runtime["_terminal_count"] = 0
        runtime["_physical_logical_label"] = name
        runtime["_physical_logical_link_target"] = "physical/baseline"
        runtime["_physical_baseline_sha256"] = base_sha
        runtime.pop("_physical_projection", None)
        auxiliary_paths: list[Path] = []
        first_identity = baseline_identity
        after_identity: dict[str, Any]
        before = base_sha; after: str
        if name == "symlink_candidate":
            os.symlink(base, path)
            try:
                open_physical(path, MAX_CANDIDATE_BYTES, trace_runtime=runtime)
            except CheckStop as exc:
                runtime["_terminal_count"] += 1
                reason = str(exc)
            else:
                raise CheckStop("MUTATION_ACCEPTED:" + name)
            after = base_sha
            after_identity = runtime.get("_physical_projection")
            require(isinstance(after_identity, dict),
                    "checker symlink projection missing")
        elif name == "hardlink_candidate":
            source = root / "physical-hard-source.json"; write_frame(source, baseline)
            auxiliary_paths.append(source)
            os.link(source, path)
            try:
                open_physical(path, MAX_CANDIDATE_BYTES, trace_runtime=runtime)
            except CheckStop as exc:
                runtime["_terminal_count"] += 1
                reason = str(exc)
            else:
                raise CheckStop("MUTATION_ACCEPTED:" + name)
            after = base_sha
            after_identity = runtime.get("_physical_projection")
            require(isinstance(after_identity, dict),
                    "checker hardlink projection missing")
        elif name == "toctou_substitution":
            write_frame(path, baseline); substitute = root / "physical-new.json"
            auxiliary_paths.append(substitute)
            write_frame(substitute, baseline)
            try:
                open_physical(path, MAX_CANDIDATE_BYTES,
                              mutation_hook=lambda target: os.replace(substitute, target),
                              trace_runtime=runtime)
            except CheckStop as exc:
                runtime["_terminal_count"] += 1
                reason = str(exc)
            else:
                raise CheckStop("MUTATION_ACCEPTED:" + name)
            after_identity = runtime.get("_physical_projection")
            require(isinstance(after_identity, dict),
                    "checker TOCTOU projection missing")
            after = base_sha
        elif name == "stale_output":
            first_identity = checker_path_projection(path, name)
            exclusive_json(path, {"first": True}, runtime)
            after_identity = checker_path_projection(
                path, name, sha_bytes(canonical({"first": True}) + b"\n"))
            try:
                exclusive_json(path, {"second": True}, runtime)
            except CheckStop as exc:
                runtime["_terminal_count"] += 1
                reason = str(exc)
            else:
                raise CheckStop("MUTATION_ACCEPTED:" + name)
            after = sha_bytes(canonical({"first": True}) + b"\n")
            runtime["_physical_projection"] = checker_path_projection(
                path, name, after)
            _checker_physical_projection_reason(runtime, reason)
        else:
            value = dict(baseline)
            value["claims"] = dict(baseline["claims"])
            if name == "unbound_checkpoint":
                value["checkpoint"] = {"path": "alien.json"}
            elif name == "positive_claim_on_resource_exit":
                value["claims"]["common_word"] = True
            elif name in ("separator_flip", "cofinal_flip", "fake_flip", "ihara_flip"):
                claim = {"separator_flip": "separator", "cofinal_flip": "cofinal_lift",
                         "fake_flip": "fake", "ihara_flip": "ihara_witness"}[name]
                value["claims"][claim] = True
            elif name == "terminal_reseal":
                value["terminal"] = "V12B_RESEALED"
            else:
                raise CheckStop("unknown physical mutation")
            value = reseal(value)
            before, after, reason = checker_mutation_trace(
                path, value,
                lambda candidate: validate_selftest_envelope(candidate, runtime),
                baseline_value=baseline, trace_runtime=runtime)
            after_identity = checker_path_projection(path, name, after)
            require(before != after, "checker physical identity unchanged:" + name)
            projected = runtime.get("_physical_projection")
            require(isinstance(projected, dict),
                    "checker semantic projection missing")
            after_identity = projected
        # Dispose the temporary case owner before measuring the next case, and
        # run the unchanged ordinary envelope again after restoration.
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        for auxiliary in auxiliary_paths:
            try:
                auxiliary.unlink()
            except FileNotFoundError:
                pass
        require(not path.exists() and all(not item.exists() for item in auxiliary_paths),
                "checker physical owner disposal:" + name)
        mutation_events = list(runtime.get("_active_validator_events", []))
        mutation_terminal_count = int(runtime.get("_terminal_count", 0))
        mutation_owner_disposed = bool(runtime.get("_last_owner_disposed"))
        runtime["_last_owner_disposed"] = mutation_owner_disposed and not path.exists()
        baseline_runtime = dict(runtime)
        baseline_runtime["_active_validator_events"] = []
        baseline_runtime["_physical_projection"] = None
        case_baseline_revalidated = False
        validate_selftest_envelope(baseline, baseline_runtime)
        require(checker_path_projection(base, name, base_sha) ==
                baseline_identity, "checker physical baseline restoration:" + name)
        case_baseline_revalidated = True
        events = mutation_events
        require(events and all(type(event) is dict for event in events),
                "checker physical validator event trace")
        rejection_event = events[-1]
        terminal_count = mutation_terminal_count
        owner_disposed = mutation_owner_disposed
        require(terminal_count == 1 and owner_disposed,
                "checker physical measured terminal/owner:" + name)
        require(reason == expected["first_reason"],
                "checker physical first reason:" + name + ":" + reason)
        ledger.append({"id": name, "owner_path": expected["owner_path"],
            "identity_kind": "physical_projection",
            "before_identity": first_identity,
            "after_identity": after_identity,
            "event_trace_digest": sha_obj(events),
            "entered_validators": [event["validator"] for event in events],
            "first_rejection": {"validator": rejection_event["validator"],
                "stage": rejection_event["stage"], "narrow_reason": reason},
            "baseline_revalidated": case_baseline_revalidated,
            "terminal_count": terminal_count,
            "owner_disposed": owner_disposed,
            "validator": rejection_event["validator"],
            "stage": rejection_event["stage"],
            "reseal": expected["reseal"], "before_sha256": before,
            "after_sha256": after, "reached_validator": rejection_event["validator"],
            "first_reason": reason})
        try:
            base.unlink()
        except FileNotFoundError:
            pass
        require(not base.exists(), "checker physical baseline disposal:" + name)
    require(len(base_raw) <= MAX_CANDIDATE_BYTES,
            "checker physical baseline binding")
    return ledger


def checker_validate_phase_transition(runtime: dict[str, Any],
                                      value: dict[str, Any]) -> None:
    """Independently validate one ordinary runtime transition owner."""
    checker_validator_event(runtime, "validate_phase_transition",
                            "transition", "runtime.phase_transition")
    validate_seal(value)
    expected_by_phase = runtime.get("_checker_phase_expected_by_phase")
    require(type(expected_by_phase) is dict, "phase gate")
    phase = value.get("phase")
    expected = expected_by_phase.get(phase)
    if type(expected) is not dict:
        checker_validator_event(runtime, "validate_phase_transition", "phase",
                                "runtime.phase_transition.phase")
        raise CheckStop("phase gate")
    require(set(value) == set(expected), "phase gate")
    for field, stage in (
            ("schema", "schema"),
            ("light_input_sha256", "light_digest"),
            ("runtime_light_public_sha256", "light_checkpoint"),
            ("heavy_input_sha256", "heavy_digest_order"),
            ("owner_preselection_sha256", "owner_preselection"),
            ("heavy_owner_sha256", "heavy_transition"),
            ("heavy_complete", "heavy_transition"),
            ("correction_started", "correction_transition"),
            ("correction_progress", "correction_progress"),
            ("zero_is_negative", "zero_semantics"),
            ("claims", "claims")):
        if value.get(field) != expected.get(field):
            checker_validator_event(runtime, "validate_phase_transition", stage,
                                    "runtime.phase_transition." + field)
            raise CheckStop("phase gate")


def checker_phase_mutation_ledger(runtime: dict[str, Any],
                                  receipt: dict[str, Any], root: Path
                                  ) -> dict[str, list[dict[str, Any]]]:
    """Mutate independently rebuilt runtime transitions through one validator."""
    fixture = load_fixture_bounded()
    light_hash = receipt.get("light_input_sha256")
    heavy_hash = receipt.get("heavy_input_sha256")
    owner_pre_sha = runtime.get("owner_preselection_sha256")
    require(type(owner_pre_sha) is str and len(owner_pre_sha) == 64,
            "checker phase OwnerPre must be loaded")
    heavy_owner = {"owner_preselection_sha256": owner_pre_sha,
                   "q0_order": int(runtime["owner_preselection"][
                       "q0_owner"]["order"]),
                   "gamma_order": int(runtime["owner_preselection"][
                       "gamma_owner"]["order"]),
                   "selected_k0_algorithm":
                       "v12b-coarse-open-address-retained-full-state-first-gid-bfs"}
    heavy_owner_sha = sha_obj(heavy_owner)
    selected_frame = receipt["selftest"]["selected_correction_seed"]
    record = selected_frame["record"]
    empty_progress = {"dual_sha256": None, "canonical_row_cursor": 0,
                      "weighted_rows": {}}
    selected_progress = {
        "dual_sha256": record["current_epoch"]["current_dual_sha256"],
        "canonical_row_cursor": int(record["rank_after"]),
        "weighted_rows": {
            "selected_formal_solution_sha256": record[
                "selected_formal_solution_sha256"],
            "selected_coordinate": int(record["selected_coordinate"])}}
    common = {"schema": SCHEMA + "/ordinary-runtime-transition",
        "light_input_sha256": light_hash,
        "runtime_light_public_sha256": sha_obj(runtime["light_public"]),
        "zero_is_negative": False, "claims": dict(FALSE_CLAIMS)}
    light_gate = seal({**common, "phase": "light_resource_checkpoint",
        "heavy_input_sha256": None, "owner_preselection_sha256": None,
        "heavy_owner_sha256": None, "heavy_complete": False,
        "correction_started": False,
        "correction_progress": empty_progress})
    heavy_gate = seal({**common, "phase": "heavy_transition",
        "heavy_input_sha256": heavy_hash,
        "owner_preselection_sha256": owner_pre_sha,
        "heavy_owner_sha256": heavy_owner_sha, "heavy_complete": True,
        "correction_started": False,
        "correction_progress": empty_progress})
    baseline = seal({**common, "phase": "selected_correction_complete",
        "heavy_input_sha256": heavy_hash,
        "owner_preselection_sha256": owner_pre_sha,
        "heavy_owner_sha256": heavy_owner_sha, "heavy_complete": True,
        "correction_started": True,
        "correction_progress": selected_progress})
    runtime["_checker_phase_expected_by_phase"] = {
        "light_resource_checkpoint": light_gate,
        "heavy_transition": heavy_gate,
        "selected_correction_complete": baseline}
    actions = {
        "heavy_call_before_heavy_digest": lambda value: (
            value.__setitem__("heavy_input_sha256", None),
            value.__setitem__("heavy_complete", False)),
        "fabricated_heavy_digest": lambda value: value.__setitem__(
            "heavy_input_sha256", "0" * 64),
        "stale_correction_progress": lambda value: value[
            "correction_progress"].__setitem__("canonical_row_cursor", 1),
        "zero_promoted_to_negative": lambda value: value.__setitem__(
            "zero_is_negative", True),
    }
    contract = {row["id"]: row for row in fixture["mutation_contract"]["phase"]}
    require(list(contract) == fixture["phase_mutations"],
            "checker phase mutation contract")
    baseline_revalidated = False
    checker_validate_phase_transition(runtime, baseline)
    baseline_revalidated = True
    ledger = []
    for ordinal, name in enumerate(fixture["phase_mutations"]):
        value = clone(baseline); actions[name](value); value = reseal(value)
        expected = contract[name]
        before, after, reason = checker_mutation_trace(
            root / f"phase-{ordinal:02d}.json", value,
            lambda candidate: checker_validate_phase_transition(
                runtime, candidate),
            baseline_value=baseline, trace_runtime=runtime)
        require(reason == expected["first_reason"],
                "checker phase first reason:" + name + ":" + reason)
        events = runtime.get("_active_validator_events", [])
        require(events and all(type(event) is dict for event in events),
                "checker phase validator event trace")
        rejection_event = events[-1]
        terminal_count = int(runtime.get("_terminal_count", 0))
        owner_disposed = bool(runtime.get("_last_owner_disposed"))
        require(terminal_count == 1 and owner_disposed,
                "checker phase measured terminal/owner:" + name)
        ledger.append({"id": name, "owner_path": expected["owner_path"],
            "identity_kind": "canonical_frame",
            "before_identity": {"kind": "canonical_frame", "sha256": before},
            "after_identity": {"kind": "canonical_frame", "sha256": after},
            "event_trace_digest": sha_obj(events),
            "entered_validators": [event["validator"] for event in events],
            "first_rejection": {"validator": rejection_event["validator"],
                "stage": rejection_event["stage"], "narrow_reason": reason},
            "baseline_revalidated": baseline_revalidated,
            "terminal_count": terminal_count,
            "owner_disposed": owner_disposed,
            "validator": rejection_event["validator"],
            "stage": rejection_event["stage"],
            "reseal": expected["reseal"], "before_sha256": before,
            "after_sha256": after, "reached_validator": rejection_event["validator"],
            "first_reason": reason})
    gates = {"light_resource_checkpoint": light_gate,
             "heavy_transition": heavy_gate}
    gate_contract = {row["id"]: row for row in fixture[
        "mutation_contract"]["phase_positive_gates"]}
    require(list(gate_contract) == fixture["phase_positive_gates"],
            "checker phase positive-gate contract")
    positive_gates = []
    for ordinal, name in enumerate(fixture["phase_positive_gates"]):
        expected = gate_contract[name]; value = gates[name]
        runtime["_active_validator_events"] = []
        runtime["_last_owner_disposed"] = False
        ordinary_pass = False
        path = root / f"phase-positive-{ordinal:02d}.json"
        try:
            write_frame(path, value)
            candidate, raw, physical = open_physical(
                path, MAX_CANDIDATE_BYTES, trace_runtime=runtime)
            checker_validate_phase_transition(runtime, candidate)
            ordinary_pass = True
            del raw
        finally:
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        events = runtime.get("_active_validator_events", [])
        require(events and candidate == gates[name] and not path.exists(),
                "checker phase positive-gate trace")
        gate_event = events[-1]
        digest = physical["sha256"]
        positive_gates.append({"id": name, "owner_path": expected["owner_path"],
            "validator": gate_event["validator"],
            "stage": gate_event["stage"],
            "reseal": expected["reseal"], "positive_gate": True,
            "ordinary_pass": ordinary_pass,
            "before_identity": {"sha256": digest},
            "after_identity": {"sha256": digest},
            "event_trace_digest": sha_obj(events),
            "entered_validators": [event["validator"] for event in events],
            "baseline_revalidated": baseline_revalidated,
            "first_rejection": None, "first_reason": None,
            "positive_gate_evidence": "ordinary pass; no terminal counter"})
    return {"mutations": ledger, "positive_gates": positive_gates}


def validate_owned_checker_paths(manifest: Path, receipt: Path,
                                 verdict: Path) -> None:
    """Reject traversal, links, and stale owned transport names."""
    expected_manifest = ROOT / "ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.manifest.v1.json"
    expected_receipt = ROOT / R_OUTPUT_PATH
    expected_verdict = ROOT / V_OUTPUT_PATH
    require(manifest.absolute() == expected_manifest.absolute(),
            "v12b checker manifest path")
    require(receipt.absolute() == expected_receipt.absolute() and
            verdict.absolute() == expected_verdict.absolute(),
            "v12b checker transport path")
    output_dir = ROOT / "ci/out"
    require(output_dir.is_dir() and not output_dir.is_symlink(),
            "v12b checker output directory identity")
    for label, target, required in (("manifest", manifest, True),
                                    ("receipt", receipt, True),
                                    ("verdict", verdict, False)):
        if required:
            try:
                item = os.lstat(target)
            except OSError as exc:
                raise CheckStop("v12b " + label + " unavailable") from exc
            require(stat.S_ISREG(item.st_mode) and item.st_nlink == 1,
                    "v12b checker " + label + " owner")
        elif os.path.lexists(str(target)):
            item = os.lstat(target)
            require(stat.S_ISREG(item.st_mode) and item.st_nlink == 1,
                    "v12b checker " + label + " output identity")
    for relative in OUTPUT_SIBLINGS:
        target = ROOT / relative
        if relative == R_OUTPUT_PATH:
            require(os.path.lexists(str(target)), "v12b receipt missing")
        else:
            require(not os.path.lexists(str(target)),
                    "stale v12b checker transport:" + relative)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="v12b SELFTEST_BOOTSTRAP checker")
    value.add_argument("--mode", choices=("SELFTEST_BOOTSTRAP",), required=True)
    value.add_argument("--manifest", type=Path, required=True)
    value.add_argument("--receipt", type=Path, required=True)
    value.add_argument("--verdict", type=Path, required=True)
    return value


def checker_platform_preflight() -> None:
    require(sys.platform == "linux" and os.name == "posix" and
            "fork" in multiprocessing.get_all_start_methods() and
            hasattr(socket, "AF_UNIX") and hasattr(os, "O_NOFOLLOW") and
            Path("/proc/self/statm").is_file(),
            "typed platform preflight:ubuntu-linux-fork-af_unix-nofollow-proc")


def main(argv: Sequence[str] | None = None) -> int:
    global _FIXTURE_SNAPSHOT
    args = parser().parse_args(argv)
    require(args.mode == "SELFTEST_BOOTSTRAP",
            "production/resume entry point is forbidden")
    checker_platform_preflight()
    checker_meter = CheckerMeter()
    checker_meter.check("checker_start")
    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    require(manifest_path.resolve() ==
            (ROOT / "ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.manifest.v1.json").resolve(),
            "v12b P0 manifest required")
    checker_meter.check("p0_before_heavy")
    p0, p0_identity, snapshots = validate_p0_checker(
        manifest_path, checker_meter)
    _FIXTURE_SNAPSHOT = snapshots["fixture"]
    fixture_body = dict(_FIXTURE_SNAPSHOT)
    fixture_claim = fixture_body.pop("self_digest_sha256", None)
    require(type(fixture_claim) is str and fixture_claim == sha_obj(fixture_body) and
            _FIXTURE_SNAPSHOT.get("schema") ==
                "d972-r07-history-free-positive-fast-resume/selftest-input/v12b" and
            _FIXTURE_SNAPSHOT.get("p5_p6_chronological_witness", {}).get(
                "validator_semantics") == "chronological-seen-pivots-only" and
            _FIXTURE_SNAPSHOT.get("resource_deadline_platform_contract", {}).get(
                "outer_margin_seconds") == 900,
            "checker sealed fixture snapshot")
    checker_p0_public = {
        "path": p0_identity["path"],
        "semantic_schema": p0["schema"],
        "self_digest_sha256": p0_identity["self_digest_sha256"],
        "physical_sha256": p0_identity["physical"]["sha256"],
    }
    receipt_path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    verdict_path = args.verdict if args.verdict.is_absolute() else ROOT / args.verdict
    validate_owned_checker_paths(manifest_path, receipt_path, verdict_path)
    receipt_trace = {"_physical_logical_label": "receipt"}
    receipt, receipt_raw, identity = open_physical(
        receipt_path, MAX_CANDIDATE_BYTES, trace_runtime=receipt_trace,
        meter=checker_meter)
    receipt_bytes = len(receipt_raw)
    receipt_sha256 = sha_bytes(receipt_raw)
    del receipt_raw
    receipt_projection = receipt_trace.get("_physical_projection")
    require(type(receipt_projection) is dict,
            "checker receipt deterministic physical projection")
    require(receipt.get("mode") == "SELFTEST_BOOTSTRAP" and
            receipt.get("terminal") == SELFTEST_TERMINAL and
            receipt.get("status") == "CANDIDATE_ONLY" and
            receipt.get("production_authorized") is False and
            receipt.get("requires_v12b_physical_pin") is True,
            "SELFTEST_BOOTSTRAP receipt required")
    sources = Sources(snapshots["source_raws"])
    snapshots["source_raws"].clear()
    sources.authenticate(checker_meter)
    checker_meter.check("sources_authenticated")
    task176_receipt = validate_task176_authority(sources)
    runtime = build_checker_light(sources)
    runtime["_checker_meter"] = checker_meter
    # Preserve the independently opened P0 identity/value.  The final
    # carrier constructor below is not allowed to take its P0 fields from R.
    runtime["_checker_p0_public"] = checker_p0_public
    runtime["_checker_p0_value"] = p0
    runtime["_checker_p0_identity"] = p0_identity
    runtime["_checker_p0_sources"] = p0["sources"]
    runtime["_checker_p0_frozen_authorities"] = p0["frozen_authorities"]
    runtime["task176_receipt"] = task176_receipt
    producer_process_owner = receipt.get("selftest", {}).get("process_owner")
    require(type(producer_process_owner) is dict,
            "checker process owner transport")
    # The checker owns a separately written light-image process suite.  It is
    # deliberately completed before task176/Q0/Gamma heavy stores are decoded
    # so no worker is forked from the heavy parent.
    checker_process_owner = checker_process_selftest(
        runtime, producer_process_owner)
    runtime["_checker_process_owner"] = checker_process_owner
    checker_meter_check(runtime, "checker_process_selftest_complete")
    task176_owners = decode_task176_owners(sources, checker_meter)
    runtime["task176_owners"] = task176_owners
    runtime["recovery_public"] = checker_recovery_public(sources)
    # Construct H's load-bearing preselection owner before consuming any
    # producer heavy carrier; it is independently decoded from task176.
    checker_build_owner_preselection(sources, runtime)
    checker_meter_check(runtime, "owner_preselection_complete")
    independent_epoch = checker_reconstruct_raw_epoch(
        runtime, receipt, snapshots["raw_checkpoint"])
    snapshots["raw_checkpoint"] = None
    checker_meter_check(runtime, "raw_epoch_reconstructed")
    require(receipt.get("p0") == {"path": p0_identity["path"],
        "semantic_schema": p0["schema"],
        "self_digest_sha256": p0_identity["self_digest_sha256"],
        "physical_sha256": p0_identity["physical"]["sha256"]} and
        receipt.get("p0_sources") == p0.get("sources") and
        receipt.get("frozen_authorities") == p0.get("frozen_authorities"),
        "checker receipt P0 physical/source binding")
    validate_receipt_heavy_seal(receipt)
    validate_selftest_v12b(runtime, receipt)
    checker_meter_check(runtime, "baseline_owner_validation")
    derived = validate_selftest_envelope(receipt, runtime)
    require(runtime.get("_checker_final_heavy_carrier") ==
            receipt.get("final_heavy_carrier") and
            runtime.get("_checker_h_final") == receipt.get("h_final"),
            "checker H_check receipt binding")
    with tempfile.TemporaryDirectory(prefix="r07-v12b-checker-selftest-") as directory:
        root = Path(directory)
        triangular_checker = checker_triangular_mutation_ledger(
            runtime, receipt, root)
        checker_meter_check(runtime, "triangular_mutations_complete")
        phase_result = checker_phase_mutation_ledger(runtime, receipt, root)
        phase = phase_result["mutations"]
        phase_positive_gates = phase_result["positive_gates"]
        selected = checker_selected_correction_mutations(runtime, receipt, root)
        checker_meter_check(runtime, "selected_mutations_complete")
        boundary = checker_boundary_mutation_ledger(runtime, receipt, root)
        positive = checker_positive_mutation_ledger(runtime, receipt, root)
        physical = checker_transport_mutation_ledger(runtime, receipt, root)
        checker_meter_check(runtime, "all_mutations_complete")
    checker_cache = runtime.get("_k0_coordinate_cache")
    require(checker_cache is not None and checker_cache[1].build_count == 1,
            "checker K0 lifecycle selected build")
    checker_store = checker_cache[1]
    checker_lifecycle = {"coordinate": int(checker_cache[0]),
        "build_count": checker_store.build_count,
        "state_digest": checker_store.state_digest(),
        "slot_digest": checker_store.slot_digest(),
        "public_digest": checker_store.public_digest(),
        "payload_bytes": checker_store.count * checker_store.width + K0_CAPACITY * 4,
        "build_bound": 1, "release_after_mutations": True}
    runtime["_k0_coordinate_cache"] = None
    mutation_ledger = {"triangular": triangular_checker, "phase": phase,
        "phase_positive_gates": phase_positive_gates,
        "selected_correction": selected, "boundary": boundary,
        "positive": positive, "physical": physical,
        "process_owner": checker_process_owner,
        "k0_coordinate_build_counts": {str(key): int(value) for key, value in
            runtime.get("_k0_coordinate_build_counts", {}).items()},
        "k0_lifecycle": checker_lifecycle,
        "producer_ledgers_replayed": False, "actual_owner_validators": True,
        "checker_independent_ledger": True,
        "all_fixture_cases": True, "executed": True}
    normalized_groups = {"triangular": triangular_checker,
        "boundary": boundary, "selected_correction": selected,
        "positive": positive, "physical": physical, "phase": phase}
    normalized = {group: [{key: row[key] for key in (
            "id", "owner_path", "validator", "stage", "first_reason", "reseal")}
        for row in rows] for group, rows in normalized_groups.items()}
    fixture = load_fixture_bounded()
    expected_normalized = {group: [{key: row[key] for key in (
            "id", "owner_path", "validator", "stage", "first_reason", "reseal")}
        for row in fixture["mutation_contract"][group]]
        for group in normalized_groups}
    require(normalized == expected_normalized and
            receipt.get("selftest", {}).get("normalized_mutation_ledger") ==
                normalized and
            receipt.get("selftest", {}).get(
                "normalized_mutation_ledger_sha256") == sha_obj(normalized),
            "producer/checker normalized mutation ledger exact equality")
    mutation_ledger["normalized"] = normalized
    mutation_ledger["normalized_sha256"] = sha_obj(normalized)
    decoded_owner_bytes = sum(len(value) for value in runtime[
        "task176_owners"].values() if isinstance(value, (bytes, bytearray)))
    runtime["task176_owners"].clear()
    runtime.get("_selected_parent_word_cache", {}).clear()
    source_release = sources.release_snapshots()
    verdict_body = {"schema": VERDICT_SCHEMA, "status": "CANDIDATE_ONLY",
        "terminal": SELFTEST_TERMINAL, "mode": "SELFTEST_BOOTSTRAP",
        "candidate_only": True, "production_authorized": False,
        "requires_v12b_physical_pin": True,
        "execution": "SELFTEST_CHECKER_COMPLETE_CANDIDATE",
        "receipt_physical": receipt_projection, "receipt_bytes": receipt_bytes,
        "receipt_sha256": receipt_sha256,
        "receipt_self_digest": receipt.get("self_digest"),
        "receipt_semantic_digest": receipt.get("semantic_digest"),
        "p0": receipt.get("p0"),
        "p0_sources": runtime["_checker_p0_sources"],
        "frozen_authorities": runtime["_checker_p0_frozen_authorities"],
        "final_heavy_identity_sha256": receipt.get("final_heavy_identity_sha256"),
        "final_heavy_carrier": receipt.get("final_heavy_carrier"),
        "h_final": receipt.get("h_final"),
        "H_check": runtime.get("_checker_final_heavy_carrier"),
        "h_final_check": runtime.get("_checker_h_final"),
        "independent_raw_reconstruction": independent_epoch,
        "derived": derived, "mutation_ledger": mutation_ledger,
        "resource_limits": {"checker_wall_seconds": CHECKER_WALL_SECONDS,
            "artifact_seconds": CHECKER_ARTIFACT_SECONDS,
            "rss_bytes": CHECKER_RSS_BYTES,
            "allocation_bytes": CHECKER_ALLOCATION_BYTES,
            "source_derived_model": CHECKER_RESOURCE_MODEL,
            "pipeline_deadlines": {"producer_internal": 9600,
                "producer_external": 9900, "checker_internal": 5400,
                "checker_external": 5700, "artifact_internal": 1200,
                "artifact_external": 1500, "external_sum": 17100,
                "outer": 18000, "outer_margin": 900, "workflow": 21600,
                "setup_cleanup_upload_margin": 3600}},
        "resource_counters": {"authenticated_source_count": len(SOURCE_PINS),
            "mutation_case_count": sum(len(mutation_ledger[key]) for key in
                ("triangular", "phase", "selected_correction", "boundary",
                 "positive", "physical")),
            "process_run_count": len(checker_process_owner["runs"]),
            "k0_coordinate_build_count": sum(int(value) for value in
                runtime.get("_k0_coordinate_build_counts", {}).values()),
            "decoded_task176_bytes_released": decoded_owner_bytes,
            "source_snapshot_release": source_release,
            "raw_checkpoint_released": runtime.get(
                "_raw_checkpoint_released") is True},
        "source_snapshots": Sources.public(), "claims": dict(FALSE_CLAIMS),
        "no_acceptance_or_negative_claim": True,
        "authority": "checker-local ordinary owner replay; candidate only"}
    verdict_body["semantic_digest"] = sha_obj(verdict_body)
    verdict = seal(verdict_body)
    receipt.clear()
    artifact_started = time.monotonic()
    checker_meter.check("artifact_write_start")
    exclusive_json(verdict_path, verdict, runtime)
    require(time.monotonic() - artifact_started <= CHECKER_ARTIFACT_SECONDS,
            "checker artifact_seconds")
    print(CHECKER_PREFIX + " " + SELFTEST_TERMINAL, flush=True)
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckStop as exc:
        verdict = ROOT / V_OUTPUT_PATH
        temporary = verdict.with_name(verdict.name + ".tmp." + str(os.getpid()))
        for owned in (temporary, verdict):
            try:
                owned.unlink()
            except FileNotFoundError:
                pass
        text = str(exc)
        kind = ("UNKNOWN_PLATFORM" if text.startswith("typed platform") else
                "UNKNOWN_RESOURCE" if text.startswith("checker ") else
                "UNKNOWN_INPUT")
        print("V12B_CHECKER_UNKNOWN " + kind,
              file=sys.stderr, flush=True)
        raise SystemExit(3)
