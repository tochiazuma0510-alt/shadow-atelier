#!/usr/bin/env python3
"""v12c SELFTEST_BOOTSTRAP producer with no production/resume surface.


The authenticated old checkpoint is used as a finite triangular owner.  Each
physical owner, selected K0 record, and transport mutation is replayed by the
ordinary validator before a deterministic candidate receipt is written.
"""
from __future__ import annotations

import argparse
import base64
import bisect
import hashlib
import json
import multiprocessing
import os
import resource
import selectors
import signal
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
P0_PATH = ROOT / "ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.manifest.v1.json"
SCHEMA = "d972-r07-history-free-positive-fast-resume/v12c"
P0_SCHEMA = "d972-r07-history-free-positive-fast-resume/selftest-bootstrap-manifest/v1"
FIXTURE_PATH = "search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12c_20260829.json"
R_OUTPUT_PATH = "ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.receipt.json"
V_OUTPUT_PATH = "ci/out/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.verdict.json"
RAW_SOURCE_PATH = "ci/resume/d972_r07_history_free_positive_fast_resume_selftest_v12c.raw.json"
OUTPUT_SIBLINGS = (
    R_OUTPUT_PATH, V_OUTPUT_PATH,
    R_OUTPUT_PATH + ".checkpoint.json",
    R_OUTPUT_PATH.replace(".receipt.json", ".producer.log"),
    R_OUTPUT_PATH.replace(".receipt.json", ".checker.log"),
    R_OUTPUT_PATH.replace(".receipt.json", ".producer.terminal"),
    R_OUTPUT_PATH.replace(".receipt.json", ".checker.terminal"),
    R_OUTPUT_PATH.replace(".receipt.json", ".artifact.ok"),
)
CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint"
SELFTEST_TERMINAL = "V12C_SELFTEST_BOOTSTRAP_ARTIFACT"
PRODUCER_PREFIX = "V12C_PRODUCER_TERMINAL"
RAW_BYTES = 86_368_039
RAW_SHA256 = "c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab"
RAW_MEMBER = "d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json"
RAW_ARCHIVE_PATH = "ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip"
RAW_ARCHIVE_BYTES = 5_001_811
RAW_ARCHIVE_SHA256 = "f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566"
OLD_SCHEMA = "d972-r07-normalized-exact-cached-colgen/v3"
OLD_SELF_DIGEST = "29bb74f3bd8048913a0365bc4c599f3731d32ba56967f3a238c7468b7fcfd123"
OLD_INPUT_SHA256 = "f29eaf9b945adb3bde89395ae9cb9018309fe8f3938d32f55e6716574b861cfb"
OLD_TARGET_SHA256 = "968f0b8325fa0e741e2c304bb940b96239c3e2d3226e0ca56f7d61a53dd0d82b"
OLD_PIVOT_ROWS_SHA256 = "3c645f4e352c96691dd35d6202bdf5f8b2cce73b7eb5f1bdf33a8daa06ce9d28"
OLD_DUAL_SHA256 = "0960259714fa94ddd89e2ac4f582f040942ab7bd258185c0448c133e50b00f0c"
NORMALIZED_DIGEST = "07c91e42c91648c5139ec13afd7fe0f44aff964612bae950d9dbd941b509b109"
WALL_SECONDS = 9_600.0
DELTA_ORDER = 357_128_352
KERNEL_ORDERS = (9, 9, 9, 9, 9, 1, 1, 1, 3, 3)
K0_CAPACITY = 1 << 22
K0_STATE_COUNT = 1_469_664
MAX_FORMAL_ENTRIES = 2_000_000
MAX_FORMAL_LIVE_ENTRIES = 2_000_000
MAX_FRAME_BYTES = 32 * 1024 * 1024
MAX_CHECKPOINT_BYTES = 4_000_000_000
MAX_CANDIDATE_BYTES = 512 * 1024 * 1024
ADDRESS_SPACE_HARD_CAP = 5_700_000_000
PRODUCER_EXPLICIT_PAYLOAD_PEAK = 4_312_038_019
PRODUCER_PAYLOAD_WITHOUT_OUTPUT = PRODUCER_EXPLICIT_PAYLOAD_PEAK - MAX_CANDIDATE_BYTES
P0_BYTES = 11_476
P0_SHA256 = "24fbc1f9d7a7be3c96e1a56d4eb97d0aa5ccca9233f1e552088e9848bc081d74"
P0_SELF_DIGEST = "39b483cf2df56aa6148bac3026c16c7f4e68950c8ff417543e84b5abaaf5f775"
FIXTURE_BYTES = 22_785
FIXTURE_SHA256 = "6fb7fe92c3cf93f54e44f9f26c3e920d131dbc626fc826d8b5bb4745bf67c8ec"
FIXTURE_SELF_DIGEST = "5569881a6e79c0ad45a794d501f2f0e3a7625aee7f2032f42694ba6d2441256d"
PC_CACHE_ENTRY_CAP = 131_072
PC_CACHE_INSERTION_CAP = 15_000_000
CHANNEL_START_SECONDS = 20.0
CHANNEL_CLOSE_SECONDS = 3.0
EXPECTED_TRIANGULAR = {
    "columns": 2896,
    "rank": 2896,
    "boundary_columns": 2896,
    "correction_columns": 0,
    "raw_support_total": 20354,
    "raw_support_max": 12,
    "ancestry_entries_total": 137926,
    "ancestry_entries_max": 258,
    "ancestry_weighted_contributions": 1011460,
    "pivot_support_total": 289774,
    "pivot_support_max": 522,
    "future_ancestry_indices": 0,
    "zero_or_missing_diagonal": 0,
    "duplicate_empty_wrong_pivots": 0,
}
EXPECTED_MANIFEST = {
    "schema": "d972-r07-normalized-exact-cached-colgen/resume-input/v1",
    "source_run_id": 33149728601,
    "source_head_sha": "7dd85c94c01e35e090917f9d11f9a7252a260523",
    "source_artifact_id": 9681838782,
    "source_artifact_digest": "sha256:66ed561b0c19c22dd56ce6aaa1626159d8267788fa282d3f2cb72f33c36e6917",
    "source_receipt": {
        "bytes": 8759,
        "sha256": "955a6bebb442f6bbe111ffcb4c1eda732f8bbbe26292c4e5da451c69dbaf5dcc",
        "terminal": "UNKNOWN_RESOURCE:phase=positive_boundary_correlation:cap=wall_seconds:value=10801.537010798002:limit=10800.0",
    },
    "zip": {
        "path": "ci/in/d972_r07_normalized_exact_common_word_cached_v3_run33149728601_checkpoint.zip",
        "bytes": 5_001_811,
        "sha256": "f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566",
        "member": RAW_MEMBER,
    },
    "raw_checkpoint": {"bytes": RAW_BYTES, "sha256": RAW_SHA256},
    "progress": {"phase": "positive_boundary_correlation", "boundary_pairs": 3_145_728,
                 "retained_columns": 2896, "candidate_words": 0},
    "claims": {"common_word": False, "separator": False,
               "finite_common_word": False, "cofinal_lift": False,
               "fake": False, "ihara_witness": False},
}

# Direct source authorities.  The producer itself is intentionally absent.
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
    "fixture": (FIXTURE_PATH, FIXTURE_BYTES, FIXTURE_SHA256),
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

FALSE_CLAIMS = {"common_word": False, "finite_common_word": False,
                "separator": False, "negative": False, "cofinal_lift": False,
                "fake": False, "ihara_witness": False}
RESOURCE_MODEL = {
    "platform": "ubuntu-24.04-x86_64-cpython3.13-linux-fork-af_unix",
    "q0_ten_store_payload": "1469664*(5*40+5*154)=1425574080",
    "q0_state_payload": "1469664*36=52907904 plus bounded CPython object/list overhead",
    "selected_k0_max_payload": "1469664*154+4194304*4=243105472",
    "gamma_projected_payload": "243*970=235710",
    "gamma_full_diagnostic": "one 4814-byte canary plus one selected owner only",
    "raw_parse_live_bound": "bytearray+bytes+ASCII+DOM <=4*86368039",
    "mutation_policy": "single immutable baseline; triangular changes only three small records",
    "physical_mutation_peak": "one borrowed owner plus one mutant/raw/DOM; cases sequential",
    "publication_reservation": MAX_CANDIDATE_BYTES,
    "explicit_live_peak_formula": "3564038019 fixed byte owners + 2000000*96 sparse-map entries + 2000000*128 ancestry entries + 300000000 bounded Q0 byte-record/index headers = 4312038019",
    "explicit_live_peak_bytes": PRODUCER_EXPLICIT_PAYLOAD_PEAK,
    "address_space_hard_cap_bytes": ADDRESS_SPACE_HARD_CAP,
    "address_space_margin_bytes": ADDRESS_SPACE_HARD_CAP - PRODUCER_EXPLICIT_PAYLOAD_PEAK,
    "rss_observation_is_not_allocation_proof": True,
    "simultaneous_child_peak": 4,
}
DEADLINE_MODEL = {"producer_internal": 9600, "producer_external": 9900,
    "checker_internal": 5400, "checker_external": 5700,
    "artifact_internal": 1200, "artifact_external": 1500,
    "external_sum": 17100, "outer": 18000, "outer_margin": 900,
    "workflow": 21600, "setup_cleanup_upload_margin": 3600}


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float,
                 limit: int | float, detail: str = "") -> None:
        super().__init__(detail or f"{phase}:{cap}:{value}>{limit}")
        self.phase, self.cap = str(phase), str(cap)
        self.value, self.limit = value, limit


class ProtocolStop(RuntimeError):
    pass


class SelftestReject(RuntimeError):
    pass


class AncestryDAG:
    """Hash-consed immutable ancestry nodes; expansion is an explicit boundary."""
    def __init__(self) -> None:
        self.nodes: list[tuple[Any, ...]] = [("zero",)]
        self.intern: dict[tuple[Any, ...], int] = {("zero",): 0}

    def literal(self, expression: dict[str, int]) -> int:
        key = ("literal", tuple(sorted((str(k), int(v) % 3)
                                        for k, v in expression.items() if int(v) % 3)))
        if key not in self.intern:
            self.intern[key] = len(self.nodes); self.nodes.append(key)
        return self.intern[key]

    def add(self, left: int, right: int, coefficient: int) -> int:
        coefficient %= 3
        if not coefficient or right == 0:
            return left
        key = ("add", int(left), int(right), coefficient)
        if key not in self.intern:
            self.intern[key] = len(self.nodes); self.nodes.append(key)
        return self.intern[key]

    def scale(self, node: int, coefficient: int) -> int:
        return self.add(0, node, coefficient)

    def expand(self, node: int, max_nodes: int = MAX_FORMAL_ENTRIES,
               max_entries: int = MAX_FORMAL_ENTRIES,
               max_live_entries: int = MAX_FORMAL_LIVE_ENTRIES) -> dict[str, int]:
        require(0 <= int(node) < len(self.nodes), "DAG expansion node")
        # Node ids are topological: every add node is allocated after both
        # children.  Propagate one F3 weight per reachable node in descending
        # id order, then fold literals into one sparse answer.  Thus expansion
        # never materializes a dictionary per DAG node.  The aggregate live
        # sparse-entry invariant is len(weights)+len(answer) <=
        # max_live_entries, and each new key is charged before insertion.
        weights: dict[int, int] = {int(node): 1}
        answer: dict[str, int] = {}
        self.last_expanded_node_count = 0
        reachable = 0
        for current in range(int(node), -1, -1):
            scalar = weights.pop(current, 0)
            if not scalar:
                continue
            require(reachable < int(max_nodes), "DAG expansion node cap")
            reachable += 1
            require(0 <= current < len(self.nodes), "DAG expansion reference")
            item = self.nodes[current]
            if item[0] == "literal":
                for key0, value0 in item[1]:
                    key = str(key0)
                    value = (answer.get(key, 0) + scalar * int(value0)) % 3
                    if value:
                        if key not in answer:
                            require(len(weights) + len(answer) + 1 <=
                                    int(max_live_entries),
                                    "DAG expansion aggregate live-entry cap")
                        answer[key] = value
                    else:
                        answer.pop(key, None)
            elif item[0] == "add":
                for child, factor in ((int(item[1]), scalar),
                                      (int(item[2]), scalar * int(item[3]))):
                    value = (weights.get(child, 0) + factor) % 3
                    if value:
                        if child not in weights:
                            require(len(weights) + len(answer) + 1 <=
                                    int(max_live_entries),
                                    "DAG expansion aggregate live-entry cap")
                        weights[child] = value
                    else:
                        weights.pop(child, None)
            require(len(answer) <= int(max_entries),
                    "DAG expansion entry cap")
        self.last_expanded_node_count = reachable
        return answer


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProtocolStop(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(canonical(value))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    answer = dict(value); answer.pop("self_digest", None)
    answer["self_digest"] = sha_obj(answer)
    return answer


def _bounded_owner_copy(value: Any, budget: list[int],
                        meter: Meter | None = None) -> Any:
    """Copy only a named mutation subowner, with a hard scalar/container cap."""
    budget[0] -= 1
    require(budget[0] >= 0, "bounded owner-local delta cap")
    if meter is not None and (budget[0] & 4095) == 0:
        meter.check("mutation_delta_copy")
    if type(value) is dict:
        return {key: _bounded_owner_copy(item, budget, meter)
                for key, item in value.items()}
    if type(value) is list:
        return [_bounded_owner_copy(item, budget, meter) for item in value]
    return value


class BoundedOwnerDelta(dict[str, Any]):
    """Authenticated immutable baseline plus copied named subowners only."""
    def __init__(self, baseline: dict[str, Any], group: str, case_id: str,
                 mutable_roots: Sequence[str], meter: Meter | None = None) -> None:
        require(type(baseline) is dict and
                type(baseline.get("self_digest")) is str,
                "authenticated bounded-delta baseline")
        super().__init__(baseline)
        self._baseline = baseline
        self._baseline_digest = str(baseline["self_digest"])
        self._group = str(group); self._case_id = str(case_id)
        self._mutable_roots = tuple(str(key) for key in mutable_roots)
        budget = [131_072]
        for key in self._mutable_roots:
            require(key in baseline, "bounded delta root:" + key)
            self[key] = _bounded_owner_copy(baseline[key], budget, meter)
        if meter is not None:
            meter.check("mutation_delta_construct")
        self._delta_payload: dict[str, Any] | None = None

    def freeze_delta(self) -> None:
        roots = {key: self[key] for key in self._mutable_roots}
        extras = {key: self[key] for key in self if key not in self._baseline}
        self._delta_payload = seal({"schema": SCHEMA + "/bounded-owner-delta/v1",
            "group": self._group, "id": self._case_id,
            "baseline_self_digest": self._baseline.get("self_digest"),
            "mutable_roots": list(self._mutable_roots), "owners": roots,
            "extra_owners": extras})

    def physical_delta(self) -> dict[str, Any]:
        require(type(self._delta_payload) is dict,
                "bounded delta must be frozen before validation")
        return self._delta_payload

    def validate_delta(self) -> None:
        payload = self.physical_delta()
        validate_seal(payload)
        require(payload.get("baseline_self_digest") ==
                self._baseline_digest == self._baseline.get("self_digest") and
                payload.get("owners") == {key: self[key]
                    for key in self._mutable_roots} and
                payload.get("extra_owners") == {key: self[key]
                    for key in self if key not in self._baseline},
                "bounded owner-local delta seal")


def validate_seal(value: dict[str, Any]) -> None:
    if hasattr(value, "validate_delta"):
        value.validate_delta()
        return
    claimed = value.get("self_digest")
    body = dict(value); body.pop("self_digest", None)
    require(type(claimed) is str and claimed == sha_obj(body), "self seal")


def validate_dag_nodes(nodes: Any) -> None:
    require(type(nodes) is list and nodes and nodes[0] == ["zero"], "DAG zero root")
    # JSON literal nodes contain lists and are not hashable as Python tuples;
    # canonical bytes are the typed, deterministic deduplication key.
    seen: set[bytes] = set()
    for index, raw in enumerate(nodes):
        require(type(raw) is list and raw, "DAG node shape")
        node = tuple(raw); opcode = node[0]
        node_key = canonical(raw)
        require(node_key not in seen, "DAG hash-cons duplicate"); seen.add(node_key)
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
            raise ProtocolStop("DAG unknown opcode")


class SourceRegistry:
    """One immutable byte snapshot per source, also used for module exec."""
    def __init__(self, snapshots: dict[str, bytes]) -> None:
        self.raw: dict[str, bytes] = dict(snapshots)
        self.modules: dict[str, Any] = {}
        self.objects: dict[str, Any] = {}

    def authenticate(self, meter: Meter | None = None) -> None:
        require(set(self.raw) == set(SOURCE_PINS),
                "producer shared source snapshot roster")
        for key, (_relative, expected_size, expected_sha) in SOURCE_PINS.items():
            raw = self.raw[key]
            require(len(raw) == expected_size and sha_bytes(raw) == expected_sha,
                    "producer shared source snapshot:" + key)

    def load(self, key: str) -> Any:
        if key in self.modules:
            return self.modules[key]
        relative = SOURCE_PINS[key][0]
        name = "_d972_v12c_" + key
        if name in sys.modules:
            raise InputStop("module_slot:" + key)
        module = types.ModuleType(name)
        module.__file__ = str((ROOT / relative).resolve())
        module.__package__ = ""
        sys.modules[name] = module
        try:
            code = compile(self.raw[key], module.__file__, "exec")
            exec(code, module.__dict__)
        except BaseException:
            sys.modules.pop(name, None)
            raise
        self.modules[key] = module
        return module

    def json(self, key: str) -> Any:
        if key not in self.objects:
            try:
                self.objects[key] = json.loads(self.raw[key].decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError) as exc:
                raise InputStop("json:" + key) from exc
        return self.objects[key]

    def public(self) -> dict[str, Any]:
        return {key: {"path": row[0], "bytes": row[1], "sha256": row[2]}
                for key, row in SOURCE_PINS.items()}

    def release_snapshots(self) -> dict[str, int]:
        released = {"raw_byte_owners": len(self.raw),
                    "json_doms": len(self.objects)}
        self.raw.clear(); self.objects.clear()
        return released


class ElapsedSignalDeadline:
    """One elapsed-adjusted SIGALRM owner installed before material work."""
    def __init__(self, seconds: float) -> None:
        self.seconds = float(seconds)
        self.started = 0.0
        self.previous_handler: Any = None
        self.previous_timer = (0.0, 0.0)

    def __enter__(self) -> "ElapsedSignalDeadline":
        require(hasattr(signal, "setitimer") and hasattr(signal, "ITIMER_REAL"),
                "typed platform preflight:elapsed signal deadline")
        self.started = time.monotonic()
        self.previous_handler = signal.getsignal(signal.SIGALRM)
        self.previous_timer = signal.getitimer(signal.ITIMER_REAL)
        def expired(_signum: int, _frame: Any) -> None:
            raise ResourceStop("internal_signal_deadline", "wall_seconds",
                               self.seconds, self.seconds)
        signal.signal(signal.SIGALRM, expired)
        signal.setitimer(signal.ITIMER_REAL, self.seconds, 0.0)
        return self

    def __exit__(self, _kind: Any, _value: Any, _trace: Any) -> None:
        elapsed = max(0.0, time.monotonic() - self.started)
        signal.setitimer(signal.ITIMER_REAL, 0.0, 0.0)
        signal.signal(signal.SIGALRM, self.previous_handler)
        previous_remaining, previous_interval = self.previous_timer
        if previous_remaining > 0.0:
            signal.setitimer(signal.ITIMER_REAL,
                             max(0.000001, previous_remaining - elapsed),
                             previous_interval)


def install_address_space_limit() -> dict[str, int]:
    """Install/read back the OS ceiling before any material authority owner."""
    try:
        _soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        infinity = resource.RLIM_INFINITY
        require(hard == infinity or hard >= ADDRESS_SPACE_HARD_CAP,
                "typed platform preflight:RLIMIT_AS hard ceiling")
        resource.setrlimit(resource.RLIMIT_AS,
                           (ADDRESS_SPACE_HARD_CAP, ADDRESS_SPACE_HARD_CAP))
        installed = resource.getrlimit(resource.RLIMIT_AS)
    except (OSError, ValueError) as exc:
        raise InputStop("typed platform preflight:RLIMIT_AS install") from exc
    require(installed == (ADDRESS_SPACE_HARD_CAP, ADDRESS_SPACE_HARD_CAP),
            "typed platform preflight:RLIMIT_AS readback")
    return {"soft_bytes": int(installed[0]), "hard_bytes": int(installed[1])}


class Meter:
    """Fresh SELFTEST invocation counters; host telemetry is never serialized."""
    def __init__(self, seconds: float) -> None:
        if float(seconds) != WALL_SECONDS:
            raise InputStop("wall_seconds_must_equal_9600")
        self.started = time.monotonic()
        self.limits = {"wall_seconds": WALL_SECONDS, "boundary_pairs": 80_000_000,
                       "fibre_scans": 80_000_000, "candidate_words": 2_000_000,
                       "retained_columns": 250_000, "checkpoint_bytes": MAX_CHECKPOINT_BYTES,
                       "rss_bytes": 5_700_000_000, "oracle_rounds": 1,
                       "global_roster": DELTA_ORDER,
                       "pivot_support_inspections": 289774,
                       "dag_node_allocations": 4_000_000,
                       "sparse_operations": 100_000_000,
                       "expansion_calls": 64,
                       "expansion_nodes": MAX_FORMAL_ENTRIES,
                       "expansion_support": MAX_FORMAL_ENTRIES,
                       "expansion_live_entries": MAX_FORMAL_LIVE_ENTRIES,
                       "serialized_dag_bytes": MAX_CHECKPOINT_BYTES,
                       "owner_preselection_stream_bytes": MAX_CHECKPOINT_BYTES,
                       "owner_preselection_stream_records": 8_000_000,
                       "pc_cache_insertions": PC_CACHE_INSERTION_CAP}
        self.counters = {key: 0 for key in self.limits if key not in
                         ("wall_seconds", "rss_bytes")}
        self.phase = "authentication"
        self.sampled_parent_rss_peak = 0
        self.sampled_children_rss_peak_sum = 0
        self.live_limits = {"payload_bytes": PRODUCER_PAYLOAD_WITHOUT_OUTPUT,
                            "output_bytes": MAX_CANDIDATE_BYTES,
                            "pc_cache_entries": PC_CACHE_ENTRY_CAP}
        self.live_reserved = {key: 0 for key in self.live_limits}

    @staticmethod
    def _rss(pid: int | None = None) -> int:
        target = "self" if pid is None else str(pid)
        try:
            with open(f"/proc/{target}/statm", "r", encoding="ascii") as stream:
                pages = int(stream.read().split()[1])
            return pages * int(os.sysconf("SC_PAGE_SIZE"))
        except (OSError, ValueError, IndexError):
            return 0

    def remaining(self) -> float:
        return self.limits["wall_seconds"] - (time.monotonic() - self.started)

    def deadline(self) -> float:
        return self.started + self.limits["wall_seconds"]

    def check(self, phase: str, child_pids: Sequence[int] = ()) -> None:
        self.phase = phase
        elapsed = time.monotonic() - self.started
        if elapsed > self.limits["wall_seconds"]:
            raise ResourceStop(phase, "wall_seconds", elapsed,
                               self.limits["wall_seconds"])
        parent = self._rss()
        children = sum(self._rss(pid) for pid in child_pids)
        self.sampled_parent_rss_peak = max(self.sampled_parent_rss_peak, parent)
        self.sampled_children_rss_peak_sum = max(
            self.sampled_children_rss_peak_sum, children)
        sampled = parent + children
        if sampled and sampled > self.limits["rss_bytes"]:
            raise ResourceStop(phase, "rss_bytes", sampled,
                               self.limits["rss_bytes"])

    def reserve(self, name: str, amount: int, phase: str) -> None:
        value = self.counters[name] + int(amount)
        if value > self.limits[name]:
            raise ResourceStop(phase, name, value, self.limits[name])
        self.check(phase)

    def commit(self, name: str, amount: int) -> None:
        self.counters[name] += int(amount)

    def bump(self, name: str, amount: int = 1, phase: str | None = None) -> None:
        self.reserve(name, amount, phase or self.phase)
        self.commit(name, amount)

    def reserve_live(self, name: str, amount: int, phase: str) -> None:
        require(name in self.live_limits and int(amount) >= 0,
                "registered live allocation token")
        value = self.live_reserved[name] + int(amount)
        if value > self.live_limits[name]:
            raise ResourceStop(phase, name, value, self.live_limits[name])
        self.check(phase)
        self.live_reserved[name] = value

    def release_live(self, name: str, amount: int, phase: str) -> None:
        require(name in self.live_reserved and 0 <= int(amount) <=
                self.live_reserved[name], "live allocation token release")
        self.live_reserved[name] -= int(amount)
        self.check(phase)

    def public(self) -> dict[str, Any]:
        return {"phase": self.phase,
                "elapsed_seconds": time.monotonic() - self.started,
                "limits": self.limits,
                "fresh_invocation_counters": self.counters,
                "resource_metric": "sampled parent RSS plus sampled child RSS sum",
                "sampled_parent_rss_peak_bytes": self.sampled_parent_rss_peak,
                "sampled_children_rss_peak_sum_bytes": self.sampled_children_rss_peak_sum,
                "os_address_space_ceiling_bytes": ADDRESS_SPACE_HARD_CAP,
                "explicit_payload_peak_bytes": PRODUCER_EXPLICIT_PAYLOAD_PEAK,
                "live_allocation_tokens": dict(self.live_reserved),
                "rss_observation_is_not_allocation_proof": True}


def serial_group_row(live: Any, p176: Any, group_row: dict[Any, int],
                     block: int) -> dict[bytes, int]:
    answer: dict[bytes, int] = {}
    for (component, value), coefficient0 in group_row.items():
        coefficient = int(coefficient0) % 3
        if coefficient:
            raw = p176.packed_joint_blob(value, "v7 group element")
            key = live.row_key(block, int(component), raw)
            answer[key] = (answer.get(key, 0) + coefficient) % 3
            if not answer[key]:
                del answer[key]
    return answer


def serial_public(live: Any, p176: Any, group_row: dict[Any, int]) -> list[list[Any]]:
    rows = []
    for (component, value), coefficient0 in group_row.items():
        coefficient = int(coefficient0) % 3
        if coefficient:
            rows.append([int(component), p176.packed_joint_blob(
                value, "v7 public element").hex(), coefficient])
    rows.sort(key=lambda row: (row[0], bytes.fromhex(row[1])))
    return rows


# The producer-side all-seven composite is intentionally written here rather
# than obtained from the frozen v1 search module.  The frozen modules supply
# group arithmetic, Fox gradients, and typed codecs; the target, occurrence,
# boundary, and direct-column composition below are this side's acceptance
# logic.  The checker has a separately written counterpart.
def producer_row_key(block: int, component: int, raw: bytes) -> bytes:
    require(block in (1, 2, 3) and 1 <= component <= 6 and
            type(raw) is bytes and len(raw) in (40, 154),
            "producer typed row key")
    return b"R" + bytes((block, component)) + len(raw).to_bytes(2, "big") + raw


def producer_exponent_key(index: int) -> bytes:
    require(index in (1, 2), "producer exponent key")
    return b"E" + bytes((index,))


def producer_decode_row_key(key: bytes) -> tuple[int, int, bytes]:
    require(type(key) is bytes and len(key) >= 5 and key[:1] == b"R",
            "producer decode typed row key")
    width = int.from_bytes(key[3:5], "big")
    require(key[1] in (1, 2, 3) and 1 <= key[2] <= 6 and
            len(key) == width + 5 and width in (40, 154),
            "producer typed key width")
    return key[1], key[2], key[5:]


def producer_public_sparse(row: dict[bytes, int]) -> list[list[Any]]:
    return [[key.hex(), int(row[key]) % 3] for key in sorted(row)
            if int(row[key]) % 3]


def producer_parse_sparse(rows: Any) -> dict[bytes, int]:
    require(type(rows) is list, "producer sparse rows list")
    answer: dict[bytes, int] = {}
    for item in rows:
        require(type(item) is list and len(item) == 2 and
                item[1] in (1, 2), "producer sparse item")
        key = bytes.fromhex(str(item[0]))
        require(key not in answer, "producer duplicate sparse key")
        answer[key] = int(item[1])
    require(producer_public_sparse(answer) == rows,
            "producer canonical sparse order")
    return answer


def producer_add_scaled(target: dict[bytes, int],
                        source: dict[bytes, int], scalar: int) -> None:
    scalar %= 3
    for key, coefficient in source.items():
        value = (target.get(key, 0) + scalar * int(coefficient)) % 3
        if value:
            target[key] = value
        else:
            target.pop(key, None)


def producer_pair(functional: dict[bytes, int],
                  row: dict[bytes, int]) -> int:
    return sum(int(value) * int(row.get(key, 0))
               for key, value in functional.items()) % 3


def producer_reduce_word(word: Iterable[int]) -> list[int]:
    answer: list[int] = []
    for raw in word:
        letter = int(raw)
        require(letter != 0 and abs(letter) in range(1, 7),
                "producer free word letter")
        if answer and answer[-1] == -letter:
            answer.pop()
        else:
            answer.append(letter)
    return answer


def producer_inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(letter) for letter in reversed(word)]


def producer_exponent_pair(word: Sequence[int]) -> tuple[int, int]:
    return (sum(1 if x == 1 else -1 if x == -1 else 0
                for x in word) % 3,
            sum(1 if x == 2 else -1 if x == -2 else 0
                for x in word) % 3)


def producer_paper_product(*displayed: Sequence[int]) -> list[int]:
    return producer_reduce_word(letter for factor in reversed(displayed)
                                for letter in factor)


def producer_group_for(runtime: dict[str, Any], block: int) -> Any:
    require(block in (1, 2, 3), "producer group block")
    return runtime["e3"] if block in (1, 2) else runtime["e4"]


def producer_unpack_element(runtime: dict[str, Any], raw: bytes,
                            block: int) -> Any:
    require(block in (1, 2, 3), "producer unpack block")
    return runtime["p176"].value_from_blob(
        raw, 0 if block in (1, 2) else 5)


def producer_element_blob(runtime: dict[str, Any], value: Any) -> bytes:
    return runtime["p176"].packed_joint_blob(value,
                                               "producer typed element")


def producer_serial_group_row(runtime: dict[str, Any], row: dict[Any, int],
                              block: int) -> dict[bytes, int]:
    answer: dict[bytes, int] = {}
    for (component, value), coefficient0 in row.items():
        coefficient = int(coefficient0) % 3
        if coefficient:
            key = producer_row_key(block, int(component),
                                   producer_element_blob(runtime, value))
            value0 = (answer.get(key, 0) + coefficient) % 3
            if value0:
                answer[key] = value0
            else:
                answer.pop(key, None)
    return answer


def producer_tagged_serial(rows: Sequence[Sequence[Any]], block: int,
                           scalar: int = 1) -> dict[bytes, int]:
    answer: dict[bytes, int] = {}
    for component0, raw_hex, coefficient0 in rows:
        key = producer_row_key(block, int(component0),
                               bytes.fromhex(str(raw_hex)))
        coefficient = scalar * int(coefficient0) % 3
        if coefficient:
            value = (answer.get(key, 0) + coefficient) % 3
            if value:
                answer[key] = value
            else:
                answer.pop(key, None)
    return answer


def producer_exact_target(runtime: dict[str, Any]) -> dict[bytes, int]:
    bridge = runtime["bridge"]
    require(bridge.get("base_target_source") != "stacked_target",
            "producer target/canary confusion")
    target: dict[bytes, int] = {}
    for label, block in (("H1", 1), ("H2", 2), ("P", 3)):
        row = bridge["raw_base_targets"][label]
        require(sha_obj(row["row"]) == row["sha256"],
                "producer raw base target digest")
        producer_add_scaled(target,
                            producer_tagged_serial(row["row"], block), -1)
    require(all(key[:1] == b"R" for key in target),
            "producer zero exponent target")
    return target


def producer_boundary_source(runtime: dict[str, Any], block: int,
                             index: int) -> list[list[Any]]:
    rows = runtime["bridge"]["pb3" if block in (1, 2) else "pb4"]["rows"]
    require(1 <= index <= len(rows), "producer boundary source index")
    return rows[index - 1]


def producer_translated_boundary(runtime: dict[str, Any], block: int,
                                 index: int,
                                 translation_blob: bytes) -> dict[bytes, int]:
    quotient = producer_group_for(runtime, block)
    translation = producer_unpack_element(runtime, translation_blob, block)
    answer: dict[bytes, int] = {}
    for component0, raw_hex, coefficient0 in producer_boundary_source(
            runtime, block, index):
        value = producer_unpack_element(runtime,
                                        bytes.fromhex(str(raw_hex)), block)
        translated = quotient.mul(translation, value)
        key = producer_row_key(block, int(component0),
                               producer_element_blob(runtime, translated))
        coefficient = int(coefficient0) % 3
        value0 = (answer.get(key, 0) + coefficient) % 3
        if value0:
            answer[key] = value0
        else:
            answer.pop(key, None)
    return answer


class ProducerAllSeven:
    """Producer-local eleven-occurrence and direct-column composite."""

    def __init__(self, runtime: dict[str, Any]) -> None:
        self.rt = runtime; self.old = runtime["old"]
        self.e3, self.e4 = runtime["e3"], runtime["e4"]
        self.g = list(runtime["bridge"]["g760"]["word"])
        x, y = [1], [2]
        z = self.old.inv_word(self.old.pp_words([x, y]))
        u = self.old.inv_word(self.old.pp_words([y, x]))
        self.pcontexts = [([1], [4]), ([4], [6]),
                          (producer_paper_product([2], [4]), [6]),
                          (producer_paper_product([1], [2]),
                           producer_paper_product([5], [6])),
                          ([1], producer_paper_product([4], [5]))]
        raw_specs = [(1, 0, self.e3, x, y, 1, True, "H1_fxy"),
                     (1, 1, self.e3, x, z, -1, True, "H1_fxz"),
                     (1, 2, self.e3, y, z, 1, True, "H1_fyz"),
                     (2, 3, self.e3, u, x, -1, True, "H2_fux"),
                     (2, 0, self.e3, x, y, -1, True, "H2_fxy"),
                     (2, 4, self.e3, u, y, 1, True, "H2_fuy")]
        for natural_index, coordinate, label in (
                (1, 5, "P_b1"), (3, 6, "P_b2"), (0, 7, "P_b3"),
                (2, 8, "P_b5_inverse"), (4, 9, "P_b4_inverse")):
            left, right = self.pcontexts[natural_index]
            raw_specs.append((3, coordinate, self.e4, left, right,
                              -1 if natural_index in (2, 4) else 1,
                              False, label))
        self.specs: list[dict[str, Any]] = []
        for block, coordinate, quotient, left, right, sign, lift, label in raw_specs:
            relation = self._substitute(self.g, left, right, lift)
            factor = relation if sign > 0 else self.old.inv_word(relation)
            self.specs.append({"block": block, "coordinate": coordinate,
                "quotient": quotient, "left": left, "right": right,
                "sign": sign, "lift": lift, "label": label,
                "base_factor": factor})
        for block in (1, 2, 3):
            indices = [i for i, row in enumerate(self.specs)
                       if row["block"] == block]
            prefix = producer_group_for(runtime, block).identity
            for index in reversed(indices):
                self.specs[index]["prefix"] = prefix
                value = producer_group_for(runtime, block).eval(
                    self.specs[index]["base_factor"])
                prefix = producer_group_for(runtime, block).mul(prefix, value)
            require(prefix == producer_group_for(runtime, block).identity,
                    "producer g760 base relation quotient identity")
        for spec in self.specs:
            spec["occurrence_prefix"] = spec["prefix"]
            if spec["sign"] > 0:
                spec["occurrence_prefix"] = spec["quotient"].mul(
                    spec["prefix"], spec["quotient"].eval(
                        spec["base_factor"]))

    def _substitute(self, word: Sequence[int], left: Sequence[int],
                    right: Sequence[int], lift: bool) -> list[int]:
        answer = self.old.f2_substitute(list(word), list(left), list(right))
        return list(self.old.embed_f2_pb3(answer)) if lift else list(answer)

    def occurrence_data(self, relator_word: Sequence[int],
                        dual: dict[bytes, int]) -> dict[str, Any]:
        merged: dict[tuple[int, bytes], int] = {}
        occurrences = []
        for ordinal, spec in enumerate(self.specs, 1):
            quotient = spec["quotient"]
            relation = self._substitute(relator_word, spec["left"],
                                        spec["right"], spec["lift"])
            if spec["sign"] < 0:
                relation = list(self.old.inv_word(relation))
            gradient, value = self.old.fox_gradient_without_sections(
                relation, quotient)
            require(value == quotient.identity,
                    "producer roster relation occurrence identity")
            prefix_inverse = quotient.inverse(spec["occurrence_prefix"])
            terms = 0
            for (component, base_value), base_coefficient in gradient.items():
                base_inverse = quotient.inverse(base_value)
                for key, lambda_coefficient in dual.items():
                    if key[:1] != b"R":
                        continue
                    block, dual_component, target_raw = producer_decode_row_key(key)
                    if block != spec["block"] or dual_component != int(component):
                        continue
                    target = producer_unpack_element(self.rt, target_raw, block)
                    required = quotient.mul(quotient.mul(
                        prefix_inverse, target), base_inverse)
                    required_blob = producer_element_blob(self.rt, required)
                    coefficient = int(base_coefficient) * int(lambda_coefficient) % 3
                    if coefficient:
                        merged_key = (int(spec["coordinate"]), required_blob)
                        value0 = (merged.get(merged_key, 0) + coefficient) % 3
                        if value0:
                            merged[merged_key] = value0
                        else:
                            merged.pop(merged_key, None)
                        terms += 1
            occurrences.append({"ordinal": ordinal, "label": spec["label"],
                "coordinate": spec["coordinate"], "factor_sign": spec["sign"],
                "raw_dual_pair_terms": terms})
        e1, e2 = producer_exponent_pair(relator_word)
        constant = (dual.get(producer_exponent_key(1), 0) * e1 +
                    dual.get(producer_exponent_key(2), 0) * e2) % 3
        ordered = sorted(merged.items(), key=lambda item: (item[0][0], item[0][1]))
        return {"constant": constant, "merged": merged,
                "public": {"K": constant,
                           "terms": [[coordinate, raw.hex(), coefficient]
                                     for (coordinate, raw), coefficient in ordered],
                           "same_target_merged_mod3": True,
                           "zero_sums_deleted": True,
                           "eleven_occurrences": occurrences}}

    @staticmethod
    def formula_scalar(formula: dict[str, Any],
                       coordinate_blobs: Sequence[bytes]) -> int:
        answer = int(formula["constant"])
        for (coordinate, target), coefficient in formula["merged"].items():
            if coordinate_blobs[coordinate] == target:
                answer += int(coefficient)
        return answer % 3

    def coordinates(self, word: Sequence[int]) -> tuple[bytes, ...]:
        values = self.rt["p176"].eval_word_coordinates(
            self.old, self.e3, self.e4, self.rt["contexts"],
            self.rt["delete"], list(word))
        return tuple(producer_element_blob(self.rt, value) for value in values)

    def occurrence_column(self, delta_word: Sequence[int],
                          relator_word: Sequence[int]) -> dict[bytes, int]:
        answer: dict[bytes, int] = {}
        for spec in self.specs:
            quotient = spec["quotient"]
            relation = self._substitute(relator_word, spec["left"],
                                        spec["right"], spec["lift"])
            if spec["sign"] < 0:
                relation = list(self.old.inv_word(relation))
            gradient, value = self.old.fox_gradient_without_sections(
                relation, quotient)
            require(value == quotient.identity,
                    "producer occurrence relation value")
            qword = self._substitute(delta_word, spec["left"],
                                     spec["right"], spec["lift"])
            translated = self.old.translate_vector(
                self.old.translate_vector(gradient, quotient.eval(qword), quotient),
                spec["occurrence_prefix"], quotient)
            producer_add_scaled(answer, producer_serial_group_row(
                self.rt, translated, spec["block"]), 1)
        e1, e2 = producer_exponent_pair(relator_word)
        if e1:
            answer[producer_exponent_key(1)] = e1
        if e2:
            answer[producer_exponent_key(2)] = e2
        return answer

    def _pentagon_word(self, word: Sequence[int]) -> list[int]:
        factors = [self.old.f2_substitute(list(word), left, right)
                   for left, right in self.pcontexts]
        return producer_paper_product(factors[1], factors[3], factors[0],
                                      self.old.inv_word(factors[2]),
                                      self.old.inv_word(factors[4]))

    def direct_column(self, delta_word: Sequence[int],
                      relator_word: Sequence[int]) -> tuple[dict[bytes, int],
                                                            dict[str, Any]]:
        conjugate = producer_reduce_word(list(delta_word) + list(relator_word) +
                                         producer_inverse_word(delta_word))
        require(self.rt["joint_group"].eval(conjugate) ==
                self.rt["joint_group"].identity,
                "producer literal conjugate joint kernel")
        corrected = producer_reduce_word(self.g + conjugate)
        base_hex = self.old.hexagon_words(self.g)
        corrected_hex = self.old.hexagon_words(corrected)
        words = [(1, self.e3, list(self.old.embed_f2_pb3(base_hex[0])),
                  list(self.old.embed_f2_pb3(corrected_hex[0]))),
                 (2, self.e3, list(self.old.embed_f2_pb3(base_hex[1])),
                  list(self.old.embed_f2_pb3(corrected_hex[1]))),
                 (3, self.e4, self._pentagon_word(self.g),
                  self._pentagon_word(corrected))]
        answer: dict[bytes, int] = {}; quotient_values = []
        for block, quotient, base_word, corrected_word in words:
            base_gradient, base_value = self.old.fox_gradient_without_sections(
                base_word, quotient)
            corrected_gradient, corrected_value = \
                self.old.fox_gradient_without_sections(corrected_word, quotient)
            require(base_value == quotient.identity and
                    corrected_value == quotient.identity,
                    "producer direct all-seven quotient identity")
            difference = dict(corrected_gradient)
            for key, coefficient in base_gradient.items():
                value = (difference.get(key, 0) - int(coefficient)) % 3
                if value:
                    difference[key] = value
                else:
                    difference.pop(key, None)
            producer_add_scaled(answer, producer_serial_group_row(
                self.rt, difference, block), 1)
            quotient_values.append(producer_element_blob(
                self.rt, corrected_value).hex())
        e1, e2 = producer_exponent_pair(conjugate)
        if e1:
            answer[producer_exponent_key(1)] = e1
        if e2:
            answer[producer_exponent_key(2)] = e2
        occurrence = self.occurrence_column(delta_word, relator_word)
        require(answer == occurrence,
                "producer full eleven occurrence/direct Fox equality")
        return answer, {"delta_word": list(delta_word),
                        "relator_word": list(relator_word),
                        "conjugate_word": conjugate,
                        "corrected_word": corrected,
                        "quotient_value_blobs": quotient_values,
                        "eleven_occurrence_replay": True,
                        "direct_all_seven_replay": True}


def validate_q3_literal_owner(q3: dict[str, Any]) -> dict[str, Any]:
    """Validate the two physical Q3 marked rows with the registered convention."""
    coarse = q3.get("coarse_models")
    require(type(coarse) is dict and type(coarse.get("Q0")) is dict,
            "q3 literal owner")
    marked = coarse["Q0"].get("marked_permutations")
    require(type(marked) is list and len(marked) == 2,
            "q3 literal row count")
    literal_rows: list[list[int]] = []
    converted_rows: list[tuple[int, ...]] = []
    for item in marked:
        if type(item) is dict:
            values = item.get("value")
        else:
            values = item
        require(type(values) is list, "q3 literal row shape")
        row = [int(value) for value in values]
        require(len(row) == 36 and sorted(row) == list(range(1, 37)),
                "q3 literal row domain")
        converted = tuple(value - 1 for value in row)
        require(set(converted) == set(range(36)), "q3 x-minus-one domain")
        literal_rows.append(row)
        converted_rows.append(converted)
    left, right = converted_rows
    product = tuple(right[left[index]] for index in range(36))
    require(len(product) == 36 and set(product) == set(range(36)),
            "q3 right-left product")
    return {"literal_rows": literal_rows, "converted_rows":
            [list(row) for row in converted_rows],
            "multiplication": "right[left[i]]", "product": list(product),
            "literal_rows_sha256": sha_obj(literal_rows)}


def build_light(registry: SourceRegistry, meter: Meter) -> dict[str, Any]:
    """Literal v277 light runtime; no Q0/fine-deletion/membership objects."""
    # The authenticated fixed-size light/P prefix is completed atomically
    # before the first wall/RSS gate so a cap can always carry a P-bound
    # pre-pool checkpoint rather than an unusable partial object.
    meter.phase = "light_runtime_atomic_prefix"
    meter.check("light_runtime_start")
    live = registry.load("live")
    p176 = registry.load("task176")
    old = registry.load("old")
    jointmod = registry.load("joint")
    v172 = registry.load("v172")
    gmod = registry.load("g760")
    pb4mod = registry.load("pb4")
    q3 = registry.json("q3")
    q3_owner = validate_q3_literal_owner(q3)
    joint_receipt = registry.json("joint_receipt")
    e3, e4, _ = old.reconstruct_quotients(q3)
    contexts, aliases, context_public = old.cheap_context_registry(e4)
    require(len(contexts) == 31 and len(context_public["named_uses"]) == 46,
            "light ten-context registry")
    words = [list(row["word"]) for row in q3["correction_fibre"]["records"]
             if row.get("word")]
    require(len(words) == 26, "light correction record roster")
    group, roster = v172.build_roster(jointmod, old, e3, e4, contexts, words)
    require(len(roster) == 6441 and
            all(group.eval(row["word"]) == group.identity for row in roster),
            "light complete joint-kernel roster")
    _, _, g760 = gmod.construct_base()
    require(len(g760) == 760 and sha_obj(g760) ==
            "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d",
            "light g760")
    x, y = [1], [2]
    z = old.inv_word(old.pp_words([x, y]))
    u = old.inv_word(old.pp_words([y, x]))
    h1, h2 = old.hexagon_words(g760)
    h1 = list(old.embed_f2_pb3(h1)); h2 = list(old.embed_f2_pb3(h2))
    pcontexts = [([1], [4]), ([4], [6]),
                 (producer_paper_product([2], [4]), [6]),
                 (producer_paper_product([1], [2]),
                  producer_paper_product([5], [6])),
                 ([1], producer_paper_product([4], [5]))]
    factors = [old.f2_substitute(g760, left, right)
               for left, right in pcontexts]
    pword = producer_paper_product(factors[1], factors[3], factors[0],
                                   old.inv_word(factors[2]),
                                   old.inv_word(factors[4]))
    base_rows: dict[str, list[list[Any]]] = {}
    for label, quotient, word in (("H1", e3, h1), ("H2", e3, h2),
                                  ("P", e4, pword)):
        meter.check("light_base_rows")
        gradient, value = old.fox_gradient_without_sections(word, quotient)
        require(value == quotient.identity, "light base relation " + label)
        base_rows[label] = serial_public(live, p176, gradient)
    pb3_relators = old.pure_relations(3)
    pb3_group_rows = [old.fox_gradient_without_sections(row, e3)[0]
                      for row in pb3_relators]
    pb4_group_rows = pb4mod.base_raw_columns(old, e4)
    require(len(pb3_group_rows) == 2 and len(pb4_group_rows) == 11 and
            all(e3.eval(row) == e3.identity for row in pb3_relators) and
            all(e4.eval(row) == e4.identity for row in old.pure_relations(4)) and
            all(old.d1(row, e3) == {} for row in pb3_group_rows) and
            all(old.d1(row, e4) == {} for row in pb4_group_rows),
            "light PB3/PB4 boundary owners")
    bridge = {
        "g760": {"word": list(g760), "sha256": sha_obj(g760)},
        "raw_base_targets": {label: {"row": rows, "sha256": sha_obj(rows)}
                             for label, rows in base_rows.items()},
        "pb3": {"rows": [serial_public(live, p176, row)
                           for row in pb3_group_rows]},
        "pb4": {"rows": [serial_public(live, p176, row)
                           for row in pb4_group_rows]},
        "relation_roster": {"count": 6441,
            "roster_sha256": sha_obj([[row["layer"], row["ordinal"], row["word"]]
                                      for row in roster])},
        "base_target_source": "g760_raw_fox",
    }
    runtime = {"live": live, "p176": p176, "old": old, "e3": e3, "e4": e4,
               "contexts": contexts, "aliases": aliases,
               "context_public": context_public, "bridge": bridge,
               "roster": roster, "joint_group": group, "q3": q3,
               "meter": meter,
               "q3_literal_owner": q3_owner, "joint_receipt": joint_receipt}
    forbidden = {"qstates", "qids", "parents", "letters", "stores",
                 "memberships", "emitted", "A_maps", "adjusted_L"}
    require(forbidden.isdisjoint(runtime), "Q0 object constructed in light phase")
    # The producer's composite target/model is separate from the frozen v1
    # module.  Only the frozen group/codec/Fox primitives are shared.
    runtime["target"] = producer_exact_target(runtime)
    runtime["model"] = ProducerAllSeven(runtime)
    light_public = {
        "source_snapshots_sha256": sha_obj(registry.public()),
        "target_sha256": sha_obj(live.public_sparse(runtime["target"])),
        "pb3_rows_sha256": sha_obj(bridge["pb3"]["rows"]),
        "pb4_rows_sha256": sha_obj(bridge["pb4"]["rows"]),
        "roster_sha256": bridge["relation_roster"]["roster_sha256"],
        "context_public_sha256": sha_obj(context_public),
        "e3_identity_hex": p176.packed_joint_blob(e3.identity, "light E3 identity").hex(),
        "e4_identity_hex": p176.packed_joint_blob(e4.identity, "light E4 identity").hex(),
        "no_q0_objects": True,
    }
    runtime["light_public"] = light_public
    runtime["light_input_sha256"] = sha_obj(light_public)
    meter.check("light_runtime_complete")
    return runtime


def read_physical_once(path: Path, expected_size: int, expected_sha: str,
                       meter: Meter | None = None) -> tuple[bytes, dict[str, Any]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise InputStop("source_open") from exc
    try:
        before = os.fstat(fd)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                before.st_size != expected_size):
            raise InputStop("source_physical_identity")
        if meter is not None:
            # Reserve the contiguous read buffer before allocation; this is a
            # deterministic cap counter, not host telemetry.
            meter.bump("checkpoint_bytes", expected_size, "raw_read_reserve")
        raw_buffer = bytearray(expected_size)
        offset = 0
        remaining = expected_size
        digest = hashlib.sha256()
        while remaining:
            if meter is not None: meter.check("raw_read", ())
            chunk = os.read(fd, min(1 << 20, remaining))
            if not chunk:
                raise InputStop("source_short_read")
            raw_buffer[offset:offset + len(chunk)] = chunk
            offset += len(chunk); digest.update(chunk); remaining -= len(chunk)
        if os.read(fd, 1):
            raise InputStop("source_long_read")
        after = os.fstat(fd)
        before_identity = (before.st_dev, before.st_ino, before.st_size,
                           before.st_mtime_ns, before.st_nlink)
        after_identity = (after.st_dev, after.st_ino, after.st_size,
                          after.st_mtime_ns, after.st_nlink)
        if before_identity != after_identity:
            raise InputStop("source_TOCTOU")
        raw = bytes(raw_buffer)
        if digest.hexdigest() != expected_sha:
            raise InputStop("source_sha256")
        os.close(fd); fd = -1
        path_after = os.stat(path, follow_symlinks=False)
        path_identity = (path_after.st_dev, path_after.st_ino, path_after.st_size,
                         path_after.st_mtime_ns, path_after.st_nlink)
        if before_identity != path_identity:
            raise InputStop("source_path_TOCTOU")
        return raw, {"device": before.st_dev, "inode": before.st_ino,
                     "size": before.st_size, "links": before.st_nlink,
                     "mtime_ns": before.st_mtime_ns, "sha256": expected_sha}
    finally:
        if fd >= 0: os.close(fd)


def validate_old_envelope(value: dict[str, Any], live: Any) -> None:
    live.validate_seal(value)
    require(value.get("schema") == OLD_SCHEMA and
            value.get("self_digest") == OLD_SELF_DIGEST and
            value.get("input_sha256") == OLD_INPUT_SHA256 and
            value.get("target_sha256") == OLD_TARGET_SHA256 and
            value.get("pivot_rows_sha256") == OLD_PIVOT_ROWS_SHA256 and
            value.get("current_dual_sha256") == OLD_DUAL_SHA256 and
            value.get("normalized_semantics_digest") == NORMALIZED_DIGEST,
            "old checkpoint envelope")
    require(value.get("input_sha256") == live.sha_obj(value.get("input_components")) and
            value.get("target_sha256") == live.sha_obj(value.get("target")),
            "old checkpoint component seals")
    require(value.get("rank") == 2896 and len(value.get("columns", [])) == 2896 and
            len(value.get("pivot_order", [])) == 2896,
            "old checkpoint fixed rank")
    require(value.get("progress", {}).get("boundary") == {
        "complete": False, "dual_sha256": OLD_DUAL_SHA256,
        "pair_attempts": 3_145_088, "restart_pair_cursor": 0},
        "old boundary provenance")
    require(value.get("progress", {}).get("correction") == {
        "canonical_row_cursor": 0, "dual_sha256": OLD_DUAL_SHA256,
        "global_cursors": {}, "kernel_prefix": 0, "live_fibre_count": 0,
        "live_fibres": [], "weighted_rows": {}}, "old correction provenance")


def validate_provenance(record: dict[str, Any], expected_id: int) -> None:
    expected_record_keys = {"active_dual", "active_dual_sha256", "column_id",
        "dual_pairing", "family", "pivot_ancestry", "pivot_hex", "provenance",
        "rank_after", "rank_before", "sparse_row", "sparse_row_sha256"}
    require(set(record) == expected_record_keys and
            record["column_id"] == expected_id and record["family"] == "boundary" and
            record["rank_before"] == expected_id - 1 and
            record["rank_after"] == expected_id, "old column typed shape")
    provenance = record["provenance"]
    seed_keys = {"base_relator_index", "block", "family",
                 "left_translation_gate", "seed", "translation_hex"}
    active_keys = {"base_relator_index", "block",
        "complete_support_occurrence_accumulation", "contributing_pairs",
        "family", "left_translation_gate", "scalar", "translation_hex"}
    require(set(provenance) in (seed_keys, active_keys) and
            provenance["family"] == "boundary" and
            provenance["left_translation_gate"] == "t*h=g" and
            type(provenance["block"]) is int and provenance["block"] in (1, 2, 3) and
            type(provenance["base_relator_index"]) is int and
            1 <= provenance["base_relator_index"] <= {1: 2, 2: 2, 3: 11}[provenance["block"]],
            "old boundary provenance")
    translation = bytes.fromhex(provenance["translation_hex"])
    require(len(translation) in (40, 154), "old translation codec")
    if set(provenance) == seed_keys:
        require(provenance["seed"] == "identity_translation" and
                record["active_dual"] is None and
                record["active_dual_sha256"] is None and
                record["dual_pairing"] is None, "old seed provenance")
    else:
        require(provenance["complete_support_occurrence_accumulation"] is True and
                provenance["scalar"] in (1, 2) and
                type(provenance["contributing_pairs"]) is list and
                record["dual_pairing"] == provenance["scalar"],
                "old ACTIVE provenance")
        for row in provenance["contributing_pairs"]:
            require(set(row) == {"base_coefficient", "component", "g_hex", "h_hex",
                                 "lambda_coefficient"} and
                    row["base_coefficient"] in (1, 2) and
                    row["lambda_coefficient"] in (1, 2) and
                    1 <= row["component"] <= 6,
                    "old contributing pair shape")
            bytes.fromhex(row["g_hex"]); bytes.fromhex(row["h_hex"])
        dual = record["active_dual"]
        require(type(dual) is list and record["active_dual_sha256"] == sha_obj(dual),
                "old ACTIVE dual provenance")


class FormalReducer:
    """Pivot rows with a load-bearing sparse expression in formal symbols."""
    def __init__(self, live: Any, meter: Meter | None = None) -> None:
        self.live = live
        self.meter = meter
        self.rows: dict[bytes, dict[bytes, int]] = {}
        self.ancestry = AncestryDAG()
        self.expr_ids: dict[bytes, int] = {}
        self.order: list[bytes] = []
        self.formal_entries = 0
        self.dag_support_allocations = 0

    def _account_nodes(self, before: int) -> None:
        allocated = len(self.ancestry.nodes) - before
        if allocated and self.meter is not None:
            self.meter.bump("dag_node_allocations", allocated, "formal_dag")

    @staticmethod
    def _expr_add(target: dict[str, int], source: dict[str, int], scalar: int) -> None:
        for key, value in source.items():
            answer = (target.get(key, 0) + scalar * int(value)) % 3
            if answer:
                target[key] = answer
            else:
                target.pop(key, None)

    def inject(self, pivot: bytes, row: dict[bytes, int],
               expression: dict[str, int], expression_node: int | None = None) -> None:
        require(row and min(row) == pivot and row[pivot] == 1 and
                pivot not in self.rows,
                "direct P injection gate")
        require(expression and all(value in (1, 2) for value in expression.values()),
                "formal expression gate")
        if self.formal_entries + len(expression) > MAX_FORMAL_ENTRIES:
            raise ResourceStop("formal_ancestry", "formal_entries",
                               self.formal_entries + len(expression),
                               MAX_FORMAL_ENTRIES)
        self.rows[pivot] = dict(row)
        if self.meter is not None:
            self.meter.bump("sparse_operations", len(row), "formal_inject")
        before_nodes = len(self.ancestry.nodes)
        self.expr_ids[pivot] = (self.ancestry.literal(expression)
                                if expression_node is None else expression_node)
        self._account_nodes(before_nodes)
        self.order.append(pivot)
        self.dag_support_allocations += len(expression)
        self.formal_entries = self.dag_support_allocations

    def reduce(self, source: dict[bytes, int]) -> tuple[dict[bytes, int], int]:
        row = dict(source); node = 0
        for pivot in self.order:
            value = row.get(pivot, 0)
            if value:
                if self.meter is not None:
                    self.meter.bump("sparse_operations", len(self.rows[pivot]),
                                    "formal_reduce")
                self.live.add_scaled(row, self.rows[pivot], -value)
                before_nodes = len(self.ancestry.nodes)
                node = self.ancestry.add(node, self.expr_ids[pivot], value)
                self._account_nodes(before_nodes)
        return row, node

    def expand(self, node: int) -> dict[str, int]:
        require(0 <= node < len(self.ancestry.nodes), "DAG expansion node")
        if self.meter is not None:
            self.meter.bump("expansion_calls", 1, "formal_expansion")
        expanded = self.ancestry.expand(
            node, max_nodes=(self.meter.limits.get("expansion_nodes", MAX_FORMAL_ENTRIES)
                             if self.meter is not None else MAX_FORMAL_ENTRIES),
            max_entries=(self.meter.limits.get("expansion_support", MAX_FORMAL_ENTRIES)
                         if self.meter is not None else MAX_FORMAL_ENTRIES),
            max_live_entries=(self.meter.limits.get(
                "expansion_live_entries", MAX_FORMAL_LIVE_ENTRIES)
                if self.meter is not None else MAX_FORMAL_LIVE_ENTRIES))
        if self.meter is not None:
            self.meter.bump("expansion_nodes", self.ancestry.last_expanded_node_count,
                            "formal_expansion")
            self.meter.bump("expansion_support", len(expanded), "formal_expansion")
        return expanded

    def add_actual(self, source: dict[bytes, int], symbol: str) -> tuple[bytes, int]:
        row = dict(source); before_nodes = len(self.ancestry.nodes)
        node = self.ancestry.literal({symbol: 1})
        self._account_nodes(before_nodes)
        for pivot in self.order:
            value = row.get(pivot, 0)
            if value:
                if self.meter is not None:
                    self.meter.bump("sparse_operations", len(self.rows[pivot]),
                                    "formal_actual_reduce")
                self.live.add_scaled(row, self.rows[pivot], -value)
                before_nodes = len(self.ancestry.nodes)
                node = self.ancestry.add(node, self.expr_ids[pivot], -value)
                self._account_nodes(before_nodes)
        require(row, "ACTIVE actual row reduced to zero")
        pivot = min(row); inverse = 1 if row[pivot] == 1 else 2
        row = self.live.scaled(row, inverse)
        before_nodes = len(self.ancestry.nodes)
        node = self.ancestry.scale(node, inverse)
        self._account_nodes(before_nodes)
        # The composed node is the only actual-row formal representation.
        # No flat ancestry expansion is performed at rank increase.
        self.inject(pivot, row, {symbol: 1}, expression_node=node)
        return pivot, node

    def exact_dual(self, target: dict[bytes, int]) -> tuple[dict[bytes, int],
                                                            dict[bytes, int],
                                                            dict[str, int]]:
        remainder, solution_node = self.reduce(target)
        require(remainder, "dual after membership")
        functional: dict[bytes, int] = {min(remainder): 1}
        if self.meter is not None:
            self.meter.bump("sparse_operations",
                sum(max(0, len(self.rows[pivot]) - 1) for pivot in self.order),
                "formal_dual_backsolve")
        for pivot in reversed(self.order):
            value = -sum(coefficient * functional.get(key, 0)
                         for key, coefficient in self.rows[pivot].items()
                         if key != pivot) % 3
            if value:
                functional[pivot] = value
            else:
                functional.pop(pivot, None)
        require(all(self.live.pair(functional, self.rows[pivot]) == 0
                    for pivot in self.order) and
                self.live.pair(functional, target) != 0,
                "fresh heuristic dual")
        if self.meter is not None:
            self.meter.bump("sparse_operations",
                len(self.order) * len(functional) + len(functional),
                "formal_dual_annihilation")
        return functional, remainder, solution_node


def build_triangular(value: dict[str, Any], runtime: dict[str, Any],
                     meter: Meter) -> tuple[FormalReducer, list[dict[bytes, int]],
                                             dict[str, Any]]:
    """Streaming independent P=A*C products; never historical Echelon.add(C)."""
    live = runtime["live"]
    columns = value["columns"]
    raw_rows: list[dict[bytes, int]] = []
    ancestry_rows: list[list[tuple[int, int]]] = []
    pivots: list[bytes] = []
    pivot_set: set[bytes] = set()
    seen_pivots: set[bytes] = set()
    stats = {key: 0 for key in EXPECTED_TRIANGULAR}
    stats["columns"] = len(columns); stats["rank"] = value["rank"]
    for expected_id, record in enumerate(columns, 1):
        meter.phase = "triangular_parse_atomic_prefix"
        meter.check("triangular_parse")
        validate_provenance(record, expected_id)
        row = live.parse_sparse(record["sparse_row"])
        require(record["sparse_row_sha256"] == live.sha_obj(record["sparse_row"]),
                "old raw sparse digest")
        raw_rows.append(row)
        stats["raw_support_total"] += len(row)
        stats["raw_support_max"] = max(stats["raw_support_max"], len(row))
        stats["boundary_columns"] += 1
        ancestry: list[tuple[int, int]] = []
        prior_index = 0
        diagonal = 0
        for item in record["pivot_ancestry"]:
            require(type(item) is list and len(item) == 2 and
                    type(item[0]) is int and item[0] > prior_index and
                    item[1] in (1, 2), "canonical F3 ancestry")
            index, coefficient = int(item[0]), int(item[1])
            prior_index = index
            if index > expected_id:
                stats["future_ancestry_indices"] += 1
            if index == expected_id:
                diagonal = coefficient
            require(1 <= index <= len(columns), "ancestry source index")
            ancestry.append((index, coefficient))
            if index <= len(raw_rows):
                stats["ancestry_weighted_contributions"] += len(raw_rows[index - 1])
        if diagonal == 0:
            stats["zero_or_missing_diagonal"] += 1
        ancestry_rows.append(ancestry)
        stats["ancestry_entries_total"] += len(ancestry)
        stats["ancestry_entries_max"] = max(stats["ancestry_entries_max"], len(ancestry))
        pivot = bytes.fromhex(record["pivot_hex"])
        if not pivot or pivot in pivot_set or value["pivot_order"][expected_id - 1] != pivot.hex():
            stats["duplicate_empty_wrong_pivots"] += 1
        pivots.append(pivot)
        pivot_set.add(pivot)
    require(stats["future_ancestry_indices"] == 0 and
            stats["zero_or_missing_diagonal"] == 0 and
            stats["duplicate_empty_wrong_pivots"] == 0,
            "v276 structural gate")
    p_rows: list[dict[bytes, int]] = []
    reducer = FormalReducer(live, meter)
    for ordinal, (ancestry, pivot) in enumerate(zip(ancestry_rows, pivots), 1):
        meter.phase = "triangular_product_atomic_prefix"
        product: dict[bytes, int] = {}
        expression: dict[str, int] = {}
        row_sparse_operations = 0
        for index, coefficient in ancestry:
            live.add_scaled(product, raw_rows[index - 1], coefficient)
            row_sparse_operations += len(raw_rows[index - 1])
            expression[f"o:{index:04d}"] = coefficient
        meter.bump("sparse_operations", row_sparse_operations,
                   "triangular_product")
        earlier_pivot_hit = False
        for key in product:
            meter.bump("pivot_support_inspections", 1, "triangular_pivot_support")
            if key in seen_pivots:
                earlier_pivot_hit = True
        if (not product or product.get(pivot) != 1 or min(product) != pivot or
                earlier_pivot_hit):
            raise InputStop("triangular_P_gate")
        stats["pivot_support_total"] += len(product)
        stats["pivot_support_max"] = max(stats["pivot_support_max"], len(product))
        reducer.inject(pivot, product, expression)
        p_rows.append(product)
        seen_pivots.add(pivot)
        meter.check("triangular_row_complete")
    require(stats == EXPECTED_TRIANGULAR and
            live.sha_obj([live.public_sparse(row) for row in p_rows]) ==
            OLD_PIVOT_ROWS_SHA256, "exact pinned triangular arithmetic")
    target = runtime["target"]
    require(live.public_sparse(target) == value["target"] and
            live.sha_obj(value["target"]) == OLD_TARGET_SHA256,
            "fresh light target equals checkpoint target")
    dual, remainder, solution_node = reducer.exact_dual(target)
    dual_public = live.public_sparse(dual)
    require(len(dual_public) == 1188 and live.sha_obj(dual_public) == OLD_DUAL_SHA256,
            "fresh first heuristic dual")
    runtime["initial_dual_private"] = dict(dual)
    runtime["current_dual_private"] = dict(dual)
    runtime["target_remainder_private"] = dict(remainder)
    runtime["target_solution_node"] = int(solution_node)
    certificate = {**stats,
        "P_rows_sha256": OLD_PIVOT_ROWS_SHA256,
        "P_equations_independent": True,
        "historical_Echelon_add_called": False,
        "heuristic_discovery_only": True,
        "exact_cached_resume": False,
        "formal_entries": reducer.formal_entries,
        "target_remainder_support": len(remainder),
        "initial_remainder": live.public_sparse(remainder),
        "initial_solution": [[key, value] for key, value in sorted(
            reducer.expand(solution_node).items())],
        "initial_dual": live.public_sparse(dual),
        "fresh_dual_support": len(dual_public),
        "fresh_dual_sha256": live.sha_obj(dual_public)}
    return reducer, p_rows, certificate


def boundary_descriptors(runtime: dict[str, Any]) -> tuple[tuple[dict[str, Any], ...],
                                                           dict[tuple[int, int], tuple[int, ...]]]:
    descriptors: list[dict[str, Any]] = []
    for block, count in ((1, 2), (2, 2), (3, 11)):
        quotient = producer_group_for(runtime, block)
        for relator in range(1, count + 1):
            for component0, h_hex, coefficient0 in producer_boundary_source(
                    runtime, block, relator):
                h_blob = bytes.fromhex(str(h_hex))
                h = producer_unpack_element(runtime, h_blob, block)
                h_inverse = quotient.inverse(h)
                descriptors.append({"block": block, "relator": relator,
                    "component": int(component0), "h_blob": h_blob, "h": h,
                    "h_inverse": h_inverse,
                    "h_inverse_blob": producer_element_blob(runtime, h_inverse),
                    "base_coefficient": int(coefficient0) % 3})
    descriptors.sort(key=lambda row: (row["block"], row["relator"],
                                      row["component"], row["h_blob"],
                                      row["base_coefficient"]))
    require(len(descriptors) == 104, "complete 104 boundary descriptors")
    lookup: dict[tuple[int, int], list[int]] = {}
    for index, row in enumerate(descriptors):
        lookup.setdefault((row["block"], row["component"]), []).append(index)
    return tuple(descriptors), {key: tuple(value) for key, value in lookup.items()}


def descriptor_public(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"block": row["block"], "relator": row["relator"],
             "component": row["component"], "h_hex": row["h_blob"].hex(),
             "h_inverse_hex": row["h_inverse_blob"].hex(),
             "base_coefficient": row["base_coefficient"]} for row in rows]


def support_from_dual(runtime: dict[str, Any], dual: dict[bytes, int]) -> dict[str, Any]:
    private: dict[tuple[int, int], list[tuple[bytes, int, Any]]] = {}
    entries = []
    for key in sorted(dual):
        coefficient = int(dual[key]) % 3
        if key[:1] != b"R" or not coefficient:
            continue
        block, component, raw = producer_decode_row_key(key)
        value = producer_unpack_element(runtime, raw, block)
        private.setdefault((block, component), []).append((raw, coefficient, value))
        entries.append([block, component, raw.hex(), coefficient])
    return {"private": private, "entries": entries,
            "types": [[block, component] for block, component in sorted(private)],
            "entry_count": len(entries), "sha256": sha_obj(entries)}


class DeadlineChannel:
    """Length-framed nonblocking socket with one absolute deadline."""
    def __init__(self, channel: socket.socket) -> None:
        self.channel = channel
        self.channel.setblocking(False)

    def _wait(self, event: int, deadline: float) -> None:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("channel deadline")
        with selectors.DefaultSelector() as selector:
            selector.register(self.channel, event)
            if not selector.select(remaining):
                raise TimeoutError("channel deadline")

    def _write(self, raw: bytes, deadline: float) -> None:
        view = memoryview(raw)
        while view:
            self._wait(selectors.EVENT_WRITE, deadline)
            try:
                sent = self.channel.send(view)
            except BlockingIOError:
                continue
            if sent <= 0:
                raise EOFError("channel closed on write")
            view = view[sent:]

    def _read(self, count: int, deadline: float) -> bytes:
        chunks = bytearray()
        while len(chunks) < count:
            self._wait(selectors.EVENT_READ, deadline)
            try:
                raw = self.channel.recv(count - len(chunks))
            except BlockingIOError:
                continue
            if not raw:
                raise EOFError("channel closed on read")
            chunks.extend(raw)
        return bytes(chunks)

    def send(self, value: dict[str, Any], deadline: float) -> int:
        raw = canonical(value)
        if len(raw) > MAX_FRAME_BYTES:
            raise ProtocolStop("frame cap")
        self._write(struct.pack(">I", len(raw)) + raw, deadline)
        return len(raw) + 4

    def recv(self, deadline: float) -> tuple[dict[str, Any], int]:
        header = self._read(4, deadline)
        size = struct.unpack(">I", header)[0]
        if size <= 0 or size > MAX_FRAME_BYTES:
            raise ProtocolStop("frame size")
        raw = self._read(size, deadline)
        try:
            value = json.loads(raw.decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise ProtocolStop("frame JSON") from exc
        require(type(value) is dict, "frame object")
        return value, size + 4

    def close(self) -> None:
        try:
            self.channel.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.channel.close()


_FORK_RUNTIME: dict[str, Any] | None = None
_FORK_DESCRIPTORS: tuple[dict[str, Any], ...] = ()
_FORK_SOCKETS: list[socket.socket] = []
_FORK_DEADLINE = 0.0
_FORK_CONTRIBUTORS: dict[int, dict[tuple[int, bytes, int],
                                   list[dict[str, Any]]]] = {}


def _worker_accumulate(frame: dict[str, Any], worker_id: int) -> dict[str, Any]:
    global _FORK_CONTRIBUTORS
    runtime = _FORK_RUNTIME
    require(runtime is not None, "fork runtime missing")
    live = runtime["live"]
    epoch = int(frame["epoch"])
    global_start, global_stop = map(int, frame["interval"])
    start, stop = map(int, frame["local_interval"])
    deadline = float(frame["deadline"])
    slice_items = frame["slice_items"]
    require(sha_obj(slice_items) == frame.get("slice_sha256"),
            "worker slice digest")
    descriptor_ids = []
    support_by_descriptor: list[list[tuple[bytes, int, Any]]] = []
    for descriptor_id0, entries0 in slice_items:
        descriptor_id = int(descriptor_id0)
        descriptor_ids.append(descriptor_id)
        rows: list[tuple[bytes, int, Any]] = []
        for block0, component0, raw_hex, coefficient0 in entries0:
            block, component = int(block0), int(component0)
            raw = bytes.fromhex(str(raw_hex)); coefficient = int(coefficient0)
            require(coefficient in (1, 2), "worker support coefficient")
            require((block, component) ==
                    (_FORK_DESCRIPTORS[descriptor_id]["block"],
                     _FORK_DESCRIPTORS[descriptor_id]["component"]),
                    "worker slice descriptor type")
            rows.append((raw, coefficient,
                         live.unpack_element(runtime, raw, block)))
        support_by_descriptor.append(rows)
    offsets = [0]
    for rows in support_by_descriptor:
        offsets.append(offsets[-1] + len(rows))
    require(0 <= start <= stop <= offsets[-1], "worker interval")
    accumulated: dict[tuple[int, bytes, int], int] = {}
    contributors: dict[tuple[int, bytes, int], list[dict[str, Any]]] = {}
    attempted = 0
    for ordinal in range(start, stop):
        if (attempted & 4095) == 0 and time.monotonic() >= deadline:
            raise TimeoutError("worker arithmetic deadline")
        local_descriptor = bisect.bisect_right(offsets, ordinal) - 1
        descriptor = _FORK_DESCRIPTORS[descriptor_ids[local_descriptor]]
        support_row = support_by_descriptor[local_descriptor][
            ordinal - offsets[local_descriptor]]
        g_blob, lambda_coefficient, g = support_row
        quotient = live.group_for_block(runtime, descriptor["block"])
        translation = quotient.mul(g, descriptor["h_inverse"])
        require(quotient.mul(translation, descriptor["h"]) == g,
                "worker t*h=g")
        t_blob = live.element_blob(runtime, translation)
        key = (descriptor["block"], t_blob, descriptor["relator"])
        coefficient = descriptor["base_coefficient"] * lambda_coefficient % 3
        contributors.setdefault(key, []).append({
            "component": descriptor["component"], "g_hex": g_blob.hex(),
            "h_hex": descriptor["h_blob"].hex(),
            "lambda_coefficient": lambda_coefficient,
            "base_coefficient": descriptor["base_coefficient"]})
        value = (accumulated.get(key, 0) + coefficient) % 3
        if value:
            accumulated[key] = value
        else:
            accumulated.pop(key, None)
        attempted += 1
    rows = [[block, raw.hex(), relator, accumulated[(block, raw, relator)]]
            for block, raw, relator in sorted(accumulated)]
    # Retain only the current bounded slice's literal contributor roster.
    # The parent asks for the selected key after the accumulator merge; no
    # descriptor/support arithmetic is replayed in either process.
    _FORK_CONTRIBUTORS = {epoch: contributors}
    public = {"kind": "RESULT", "epoch": epoch, "worker_id": worker_id,
              "interval": [global_start, global_stop],
              "local_interval": [start, stop],
              "slice_sha256": frame["slice_sha256"],
              "attempted": attempted,
              "accumulator": rows, "complete": True}
    public["result_sha256"] = sha_obj(public)
    return public


def _boundary_worker(worker_id: int, own_socket: socket.socket) -> None:
    own_fd = own_socket.fileno()
    for candidate in _FORK_SOCKETS:
        if candidate.fileno() != own_fd:
            candidate.close()
    channel = DeadlineChannel(own_socket)
    try:
        channel.send({"kind": "READY", "worker_id": worker_id,
                      "pid": os.getpid()}, time.monotonic() + CHANNEL_START_SECONDS)
        while True:
            frame, _ = channel.recv(_FORK_DEADLINE)
            kind = frame.get("kind")
            if kind == "STOP":
                channel.send({"kind": "STOPPED", "worker_id": worker_id,
                              "epoch": frame.get("epoch")}, float(frame["deadline"]))
                return
            if kind == "WINNER":
                epoch = int(frame.get("epoch")); selected = frame.get("selected")
                cache = _FORK_CONTRIBUTORS.pop(epoch, None)
                require(type(cache) is dict, "worker contributor epoch")
                if selected is None:
                    rows = []
                else:
                    require(type(selected) is list and len(selected) == 3,
                            "worker contributor key")
                    key = (int(selected[0]), bytes.fromhex(str(selected[1])),
                           int(selected[2]))
                    rows = cache.get(key, [])
                answer = {"kind": "CONTRIBUTORS", "epoch": epoch,
                          "worker_id": worker_id, "selected": selected,
                          "rows": rows}
                answer["result_sha256"] = sha_obj(answer)
                channel.send(answer, float(frame["deadline"]))
                continue
            require(kind == "EPOCH" and frame.get("worker_id") == worker_id,
                    "worker frame owner")
            fault = frame.get("fault")
            if fault == "death":
                os._exit(73)
            if fault == "timeout":
                # Hold the worker in one kernel wait.  A deadline fault must
                # exercise the blocked transport without a polling spin.
                waiter = selectors.DefaultSelector()
                try:
                    waiter.register(own_socket, selectors.EVENT_READ)
                    remaining = max(0.0, float(frame["deadline"]) -
                                    time.monotonic())
                    waiter.select(remaining)
                finally:
                    waiter.close()
            if fault == "partial":
                partial = b'{"kind":"RESULT"'
                channel._write(struct.pack(">I", len(partial) + 100) + partial,
                               float(frame["deadline"])); os._exit(74)
            result = _worker_accumulate(frame, worker_id)
            channel.send(result, float(frame["deadline"]))
    finally:
        channel.close()


class PersistentBoundaryOwner:
    """Persistent fork roster; every epoch is atomically collected or discarded."""
    def __init__(self, runtime: dict[str, Any], meter: Meter, workers: int) -> None:
        if workers not in (2, 4):
            raise InputStop("workers_must_be_2_or_4")
        methods = multiprocessing.get_all_start_methods()
        if sys.platform != "linux" or "fork" not in methods:
            raise InputStop("linux_fork_required")
        self.runtime, self.meter, self.workers = runtime, meter, workers
        self.descriptors, self.type_lookup = boundary_descriptors(runtime)
        self.descriptor_public = descriptor_public(self.descriptors)
        self.descriptor_sha256 = sha_obj(self.descriptor_public)
        self.context = multiprocessing.get_context("fork")
        self.channels: list[DeadlineChannel] = []
        self.processes: list[multiprocessing.Process] = []
        self.epoch = 0
        self._materialize_epoch = 0
        self.started = False
        self.closed = False
        self.accounting = {"epochs_committed": 0, "epochs_discarded": 0,
            "literal_pairs_committed": 0, "support_bytes": 0,
            "frames_sent_bytes": 0, "frames_received_bytes": 0,
            "frames_sent": 0, "frames_received": 0,
            "stop_frames_sent": 0, "stop_frames_received": 0,
            "accumulator_entries": 0, "max_accumulator_entries": 0,
            "formal_ancestry_entries": 0,
            "descriptor_count": len(self.descriptors),
            "descriptor_sha256": self.descriptor_sha256,
            "winner_reconstructions": 0, "process_restarts": 0,
            "metric": "sampled RSS sum; not exact physical peak"}
        self.cleanup = {"transitions": ["not_started"], "started_pids": [],
                        "worker_exitcodes": [], "live_pids_after_join": [],
                        "process_close_count": 0, "complete": False}

    def pids(self) -> list[int]:
        return [int(process.pid) for process in self.processes if process.pid]

    def start(self) -> None:
        global _FORK_RUNTIME, _FORK_DESCRIPTORS, _FORK_SOCKETS, _FORK_DEADLINE
        require(not self.started and not self.closed, "roster start state")
        _FORK_RUNTIME = self.runtime
        _FORK_DESCRIPTORS = self.descriptors
        _FORK_DEADLINE = self.meter.deadline()
        pairs = [socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
                 for _ in range(self.workers)]
        _FORK_SOCKETS = [sock for pair in pairs for sock in pair]
        deadline = min(self.meter.deadline(), time.monotonic() + CHANNEL_START_SECONDS)
        try:
            for worker_id, (_parent, child) in enumerate(pairs):
                process = self.context.Process(target=_boundary_worker,
                                               args=(worker_id, child),
                                               name=f"r07-v7-boundary-{worker_id}")
                process.start(); self.processes.append(process)
            for parent, child in pairs:
                child.close(); self.channels.append(DeadlineChannel(parent))
            for worker_id, channel in enumerate(self.channels):
                frame, size = channel.recv(deadline)
                require(frame.get("kind") == "READY" and
                        frame.get("worker_id") == worker_id and
                        frame.get("pid") == self.processes[worker_id].pid,
                        "worker READY")
                self.accounting["frames_received_bytes"] += size
            self.started = True
            self.meter.check("boundary_workers_started", self.pids())
            self.cleanup["transitions"].append("started")
            self.cleanup["started_pids"] = self.pids()
        except (TimeoutError, EOFError, OSError, ProtocolStop, RuntimeError, ValueError):
            self.abort("startup")
            for pair in pairs:
                for endpoint in pair:
                    try:
                        endpoint.close()
                    except OSError:
                        pass
            raise ResourceStop("boundary_roster_start", "wall_seconds",
                               time.monotonic() - self.meter.started,
                               self.meter.limits["wall_seconds"])

    @staticmethod
    def intervals(total: int, workers: int) -> list[list[int]]:
        require(total >= 0 and workers > 0, "interval domain")
        return [[total * index // workers, total * (index + 1) // workers]
                for index in range(workers)]

    def _matching(self, support: dict[str, Any]) -> tuple[list[int], int]:
        descriptor_ids = sorted(index for key in support["private"]
                                for index in self.type_lookup.get(key, ()))
        total = sum(len(support["private"].get(
            (self.descriptors[index]["block"], self.descriptors[index]["component"]), ()))
                    for index in descriptor_ids)
        return descriptor_ids, total

    def run_epoch(self, dual: dict[bytes, int], *, fault: str | None = None,
                  short_deadline: float | None = None) -> dict[str, Any]:
        require(self.started and not self.closed, "roster epoch state")
        support = support_from_dual(self.runtime, dual)
        descriptor_ids, total = self._matching(support)
        intervals = self.intervals(total, self.workers)
        require(intervals[0][0] == 0 and intervals[-1][1] == total and
                all(intervals[i][1] == intervals[i + 1][0]
                    for i in range(len(intervals) - 1)), "complete interval cover")
        self.meter.reserve("boundary_pairs", total, "positive_boundary_correlation")
        self.epoch += 1
        self._materialize_epoch = self.epoch
        deadline = self.meter.deadline()
        if short_deadline is not None:
            deadline = min(deadline, time.monotonic() + float(short_deadline))
        dual_digest = sha_obj(self.runtime["live"].public_sparse(dual))
        # Keep a reference-only layout, then construct/send one bounded worker
        # slice at a time.  No second parent copy of the complete pair stream
        # and no full post-selection contributor scan is made.
        pair_layout: list[tuple[int, Sequence[tuple[bytes, int, Any]]]] = []
        for descriptor_id in descriptor_ids:
            descriptor = self.descriptors[descriptor_id]
            key = (descriptor["block"], descriptor["component"])
            pair_layout.append((descriptor_id, support["private"].get(key, ())))
        pair_offsets = [0]
        for _descriptor_id, entries in pair_layout:
            pair_offsets.append(pair_offsets[-1] + len(entries))
        require(pair_offsets[-1] == total, "pair stream cardinality")
        frame_metadata = []
        results = []
        try:
            for worker_id, (channel, interval) in enumerate(
                    zip(self.channels, intervals)):
                self.meter.check("boundary_send", self.pids())
                global_start, global_stop = interval
                slice_items = []
                for pair_index, (descriptor_id, entries) in enumerate(pair_layout):
                    left = max(global_start, pair_offsets[pair_index])
                    right = min(global_stop, pair_offsets[pair_index + 1])
                    if left < right:
                        lo = left - pair_offsets[pair_index]
                        hi = right - pair_offsets[pair_index]
                        descriptor = self.descriptors[descriptor_id]
                        rows = [[descriptor["block"], descriptor["component"],
                                 raw.hex(), coefficient]
                                for raw, coefficient, _value in entries[lo:hi]]
                        slice_items.append([descriptor_id, rows])
                local_count = global_stop - global_start
                require(sum(len(entries) for _descriptor_id, entries in slice_items) ==
                        local_count, "disjoint pair slice")
                slice_digest = sha_obj(slice_items)
                frame = {"kind": "EPOCH", "epoch": self.epoch,
                    "worker_id": worker_id, "deadline": deadline,
                    "dual_sha256": dual_digest, "interval": interval,
                    "local_interval": [0, local_count],
                    "slice_items": slice_items, "slice_sha256": slice_digest,
                    "fault": fault if worker_id == 0 else None}
                self.accounting["frames_sent_bytes"] += channel.send(frame, deadline)
                self.accounting["frames_sent"] += 1
                frame_metadata.append({"slice_sha256": slice_digest,
                                       "local_count": local_count})
            for worker_id, channel in enumerate(self.channels):
                self.meter.check("boundary_receive", self.pids())
                result, size = channel.recv(deadline)
                self.accounting["frames_received_bytes"] += size
                self.accounting["frames_received"] += 1
                claimed = result.pop("result_sha256", None)
                require(claimed == sha_obj(result), "worker result digest")
                result["result_sha256"] = claimed
                require(result.get("kind") == "RESULT" and
                        result.get("epoch") == self.epoch and
                        result.get("worker_id") == worker_id and
                        result.get("interval") == intervals[worker_id] and
                        result.get("local_interval") ==
                        [0, intervals[worker_id][1] - intervals[worker_id][0]] and
                        result.get("slice_sha256") ==
                        frame_metadata[worker_id]["slice_sha256"] and
                        result.get("attempted") == intervals[worker_id][1] - intervals[worker_id][0] and
                        result.get("complete") is True,
                        "complete worker result")
                results.append(result)
        except (TimeoutError, EOFError, OSError, ProtocolStop, ValueError) as exc:
            self.accounting["epochs_discarded"] += 1
            self.abort("atomic_epoch_discard")
            raise ResourceStop("positive_boundary_correlation", "transport",
                               1, 0, "typed_atomic_discard") from exc
        accumulated: dict[tuple[int, bytes, int], int] = {}
        for result in results:
            rows = result["accumulator"]
            self.accounting["accumulator_entries"] += len(rows)
            self.accounting["max_accumulator_entries"] = max(
                self.accounting["max_accumulator_entries"], len(rows))
            for block0, raw_hex, relator0, coefficient0 in rows:
                key = (int(block0), bytes.fromhex(str(raw_hex)), int(relator0))
                coefficient = int(coefficient0)
                require(coefficient in (1, 2), "worker accumulator F3")
                value = (accumulated.get(key, 0) + coefficient) % 3
                if value:
                    accumulated[key] = value
                else:
                    accumulated.pop(key, None)
        selected = min(accumulated) if accumulated else None
        selected_public = None if selected is None else [
            selected[0], selected[1].hex(), selected[2]]
        contributors: list[dict[str, Any]] = []
        contributor_result_digests: list[str] = []
        try:
            for channel in self.channels:
                self.meter.check("boundary_winner_send", self.pids())
                size = channel.send({"kind": "WINNER", "epoch": self.epoch,
                    "selected": selected_public, "deadline": deadline}, deadline)
                self.accounting["frames_sent_bytes"] += size
                self.accounting["frames_sent"] += 1
            for worker_id, channel in enumerate(self.channels):
                self.meter.check("boundary_winner_receive", self.pids())
                reply, size = channel.recv(deadline)
                self.accounting["frames_received_bytes"] += size
                self.accounting["frames_received"] += 1
                claimed = reply.pop("result_sha256", None)
                require(claimed == sha_obj(reply), "worker contributor digest")
                reply["result_sha256"] = claimed
                require(reply.get("kind") == "CONTRIBUTORS" and
                        reply.get("epoch") == self.epoch and
                        reply.get("worker_id") == worker_id and
                        reply.get("selected") == selected_public and
                        type(reply.get("rows")) is list,
                        "worker retained winner contributors")
                contributors.extend(reply["rows"])
                contributor_result_digests.append(claimed)
        except (TimeoutError, EOFError, OSError, ProtocolStop, ValueError) as exc:
            self.accounting["epochs_discarded"] += 1
            self.abort("atomic_contributor_discard")
            raise ResourceStop("positive_boundary_correlation", "transport",
                               1, 0, "typed_atomic_discard") from exc
        if selected is None:
            require(not contributors, "zero outcome contributor roster")
        else:
            require(sum(item["lambda_coefficient"] * item["base_coefficient"]
                        for item in contributors) % 3 == accumulated[selected],
                    "retained winner contributor scalar")
        self.meter.commit("boundary_pairs", total)
        self.accounting["epochs_committed"] += 1
        self.accounting["literal_pairs_committed"] += total
        self.accounting["support_bytes"] += len(canonical(support["entries"]))
        outcome = {"epoch": self.epoch, "dual_sha256": dual_digest,
            "support_entry_count": support["entry_count"],
            "support_sha256": support["sha256"],
            "support_types": support["types"],
            "matching_descriptor_ids": descriptor_ids,
            "matching_descriptor_count": len(descriptor_ids),
            "expanded_pair_count": total, "intervals": intervals,
            "slice_digests": [frame["slice_sha256"] for frame in frame_metadata],
            "slice_coverage": {"global_ordinal": [0, total],
                                "disjoint": True, "overlap": False},
            "selected": selected_public,
            "selected_scalar": None if selected is None else accumulated[selected],
            "selected_contributors": contributors,
            "contributor_result_digests": contributor_result_digests,
            "zero_complete": selected is None,
            "result_digests": [row["result_sha256"] for row in results],
            "worker_results": results}
        if self.epoch == 1 and len(dual) == 1188:
            require(support["entry_count"] == 1188 and
                    support["types"] == [[1, 1]] and
                    len(descriptor_ids) == 4 and total == 4752,
                    "exact pinned first boundary epoch")
            outcome["pinned_first_epoch"] = True
        return outcome

    def materialize(self, dual: dict[bytes, int], outcome: dict[str, Any]) -> dict[str, Any] | None:
        require(outcome["epoch"] == self._materialize_epoch,
                "parent contributor/epoch binding")
        if outcome["selected"] is None:
            return None
        block, translation_hex, relator = outcome["selected"]
        translation_blob = bytes.fromhex(translation_hex)
        row = producer_translated_boundary(self.runtime, int(block),
                                           int(relator), translation_blob)
        scalar = producer_pair(dual, row)
        require(scalar == outcome["selected_scalar"] and scalar in (1, 2),
                "parent translated-row scalar")
        contributors = outcome.get("selected_contributors")
        require(type(contributors) is list, "parent retained contributors")
        require(sum(item["lambda_coefficient"] * item["base_coefficient"]
                    for item in contributors) % 3 == scalar, "parent full contributors")
        self.accounting["winner_reconstructions"] += 1
        return {"row": row, "provenance": {"family": "boundary",
            "block": block, "base_relator_index": relator,
            "translation_hex": translation_hex, "scalar": scalar,
            "complete_support_occurrence_accumulation": True,
            "left_translation_gate": "t*h=g", "contributing_pairs": contributors,
            "boundary_epoch": outcome}}

    def abort(self, reason: str) -> None:
        if self.closed:
            return
        self.cleanup["transitions"].append(reason)
        for channel in self.channels:
            channel.close()
        for process in self.processes:
            if process.is_alive():
                process.terminate()
        deadline = time.monotonic() + CHANNEL_CLOSE_SECONDS
        for process in self.processes:
            process.join(max(0.0, deadline - time.monotonic()))
        for process in self.processes:
            if process.is_alive():
                process.kill(); process.join(CHANNEL_CLOSE_SECONDS)
        self.cleanup["worker_exitcodes"] = [process.exitcode for process in self.processes]
        self.cleanup["live_pids_after_join"] = [process.pid for process in self.processes
                                                if process.is_alive()]
        for process in self.processes:
            process.close(); self.cleanup["process_close_count"] += 1
        self.cleanup["complete"] = not self.cleanup["live_pids_after_join"] and \
            self.cleanup["process_close_count"] == len(self.processes)
        self.closed = True

    def close(self) -> None:
        if self.closed:
            return
        deadline = min(self.meter.deadline(), time.monotonic() + CHANNEL_CLOSE_SECONDS)
        try:
            for channel in self.channels:
                size = channel.send({"kind": "STOP", "epoch": self.epoch,
                                    "deadline": deadline}, deadline)
                self.accounting["frames_sent_bytes"] += size
                self.accounting["frames_sent"] += 1
                self.accounting["stop_frames_sent"] += 1
            for worker_id, channel in enumerate(self.channels):
                value, size = channel.recv(deadline)
                self.accounting["frames_received_bytes"] += size
                self.accounting["frames_received"] += 1
                self.accounting["stop_frames_received"] += 1
                require(value.get("kind") == "STOPPED" and
                        value.get("worker_id") == worker_id,
                        "worker STOPPED")
        except (TimeoutError, EOFError, OSError, ProtocolStop):
            self.abort("cleanup_failure")
            return
        self.cleanup["transitions"].append("stop_acknowledged")
        for channel in self.channels:
            channel.close()
        for process in self.processes:
            process.join(CHANNEL_CLOSE_SECONDS)
        for process in self.processes:
            if process.is_alive():
                process.terminate(); process.join(CHANNEL_CLOSE_SECONDS)
        for process in self.processes:
            if process.is_alive():
                process.kill(); process.join(CHANNEL_CLOSE_SECONDS)
        self.cleanup["worker_exitcodes"] = [process.exitcode for process in self.processes]
        self.cleanup["live_pids_after_join"] = [process.pid for process in self.processes
                                                if process.is_alive()]
        for process in self.processes:
            process.close(); self.cleanup["process_close_count"] += 1
        self.cleanup["complete"] = not self.cleanup["live_pids_after_join"] and \
            self.cleanup["process_close_count"] == len(self.processes)
        self.cleanup["transitions"].append("closed")
        self.closed = True

    def public(self) -> dict[str, Any]:
        return {"workers": self.workers, "persistent": True,
                "transport": "nonblocking AF_UNIX socketpair, absolute deadline frames",
                "accounting": dict(self.accounting),
                "cleanup": dict(self.cleanup)}


def _stream_state_digest(states: Sequence[bytes], ids: dict[bytes, int],
                         meter: Meter) -> str:
    digest = hashlib.sha256()
    for expected, state in enumerate(states):
        if (expected & 4095) == 0:
            meter.check("q0_state_identity_digest")
        require(ids.get(state) == expected, "Q0 state/id binding")
        digest.update(struct.pack("<I", expected)); digest.update(state)
    return digest.hexdigest()


def _stream_store_digest(store: bytes | bytearray, meter: Meter) -> str:
    digest = hashlib.sha256()
    for offset in range(0, len(store), 1 << 20):
        meter.check("q0_store_stream_digest")
        digest.update(store[offset:offset + (1 << 20)])
    return digest.hexdigest()


def _stream_canonical_int_list_digest(values: Sequence[int],
                                      meter: Meter) -> str:
    """Hash compact canonical JSON without materializing its ASCII owner."""
    digest = hashlib.sha256(); digest.update(b"[")
    for index, value in enumerate(values):
        if (index & 4095) == 0:
            meter.check("q0_parent_canonical_digest")
        if index:
            digest.update(b",")
        digest.update(str(int(value)).encode("ascii"))
    digest.update(b"]")
    return digest.hexdigest()


def _stable_k0_hash(coarse: bytes) -> int:
    """Stable hash of the authenticated coarse key, never Python hash()."""
    return int.from_bytes(hashlib.sha256(
        b"v12c-k0-coarse-key\0" + coarse).digest()[:8], "little")


class StableProducerK0Index:
    """Coarse-key index retaining the complete typed state for equality."""
    def __init__(self, coordinate: int, store: bytearray,
                 width: int, degree: int, meter: Meter) -> None:
        require(0 <= coordinate < 10 and type(store) is bytearray and
                width in (40, 154) and
                degree in (36, 144) and degree <= width,
                "producer K0 index dimensions")
        self.coordinate = coordinate
        self.meter = meter
        self.store = store; self.width = width; self.degree = degree
        self.state_count = len(store) // width
        require(self.state_count == K0_STATE_COUNT and
                len(store) == self.state_count * width,
                "producer K0 state count")
        payload = self.state_count * width + K0_CAPACITY * 4
        require(payload == (243105472 if width == 154 else
                            K0_STATE_COUNT * 40 + K0_CAPACITY * 4) and
                payload <= 256 * 1024 * 1024,
                "producer K0 payload accounting")
        self.slots = array("I", [0]) * K0_CAPACITY
        require(self.slots.itemsize == 4, "producer K0 uint32 slots")
        self.build_count = 0
        # These are immutable build products.  A correction mutation must not
        # rescan the 226 MiB state slab (or the 16 MiB slot table) merely to
        # restate an already authenticated owner digest.
        self._state_digest: str | None = None
        self._slot_digest: str | None = None
        self._public_digest: str | None = None
        self._coarse_multiplicity_digest: str | None = None

    def _state(self, qid: int) -> bytes:
        start = qid * self.width
        return bytes(self.store[start:start + self.width])

    def build(self) -> None:
        if self.build_count:
            return
        state_digest = hashlib.sha256(b"v12c-k0-state-stream/v1\0")
        coarse_digest = hashlib.sha256()
        for qid in range(self.state_count):
            if (qid & 4095) == 0:
                self.meter.check("K0_state_build")
            state = self._state(qid)
            coarse = state[:self.degree]
            state_digest.update(struct.pack("<Q", len(state)))
            state_digest.update(state)
            coarse_digest.update(struct.pack("<H", len(coarse)))
            coarse_digest.update(coarse)
            coarse_digest.update(struct.pack("<I", 1))
            slot = _stable_k0_hash(coarse) & (K0_CAPACITY - 1)
            for probe in range(K0_CAPACITY):
                if (probe & 4095) == 0:
                    self.meter.check("K0_probe_build")
                prior = int(self.slots[slot])
                if prior == 0:
                    self.slots[slot] = qid + 1
                    break
                if self._state(prior - 1)[:self.degree] == coarse:
                    raise ProtocolStop("producer K0 duplicate coarse key")
                slot = (slot + 1) & (K0_CAPACITY - 1)
            else:
                raise ProtocolStop("producer K0 table full")
        self.build_count = 1
        slot_digest = hashlib.sha256(b"v12c-k0-slot-stream/v1\0")
        for index, qid in enumerate(self.slots):
            if (index & 4095) == 0:
                self.meter.check("K0_slot_digest")
            raw = struct.pack("<I", int(qid))
            slot_digest.update(struct.pack("<Q", len(raw)))
            slot_digest.update(raw)
        self._state_digest = state_digest.hexdigest()
        self._slot_digest = slot_digest.hexdigest()
        self._coarse_multiplicity_digest = coarse_digest.hexdigest()
        self._public_digest = sha_obj({
            "schema": "v12c-k0-public-cache/v1",
            "state_digest": self._state_digest,
            "slot_digest": self._slot_digest,
            "coarse_bucket_statistics": self.bucket_public(),
            "state_count": self.state_count, "width": self.width,
            "degree": self.degree, "table_length": K0_CAPACITY,
            "build_count": self.build_count})

    def lookup_full(self, expected: bytes) -> int | None:
        require(type(expected) is bytes and len(expected) == self.width,
                "producer K0 full lookup width")
        self.build()
        coarse = expected[:self.degree]
        slot = _stable_k0_hash(coarse) & (K0_CAPACITY - 1)
        for probe in range(K0_CAPACITY):
            if (probe & 4095) == 0:
                self.meter.check("K0_probe_lookup")
            prior = int(self.slots[slot])
            if prior == 0:
                return None
            retained = self._state(prior - 1)
            if retained[:self.degree] == coarse:
                return prior - 1 if retained == expected else None
            slot = (slot + 1) & (K0_CAPACITY - 1)
        return None

    def bucket_public(self) -> dict[str, Any]:
        self.build()
        require(self._coarse_multiplicity_digest is not None,
                "producer K0 coarse digest cache")
        histogram = [{"bucket_size": 1,
                      "coarse_key_count": self.state_count}]
        return {"label": f"S{self.coordinate}",
            "type": "E3" if self.coordinate < 5 else "E4",
            "coarse_key_width_bytes": self.degree,
            "q0_state_count": self.state_count,
            "distinct_coarse_keys": self.state_count,
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

    def state_digest(self) -> str:
        self.build()
        require(self._state_digest is not None, "producer K0 state digest cache")
        return self._state_digest

    def slot_digest(self) -> str:
        self.build()
        require(self._slot_digest is not None, "producer K0 slot digest cache")
        return self._slot_digest

    def public_digest(self) -> str:
        self.build()
        require(self._public_digest is not None, "producer K0 public digest cache")
        return self._public_digest

    def public(self) -> dict[str, Any]:
        return {"state_count": self.state_count, "width": self.width,
                "coordinate": self.coordinate,
                "degree": self.degree, "table_length": K0_CAPACITY,
                "payload_bytes": self.state_count * self.width + K0_CAPACITY * 4,
                "uint32_itemsize": self.slots.itemsize,
                "hash": "sha256(v12c-k0-coarse-key\\0)[:8]:little",
                "coarse_key_lookup": True, "full_state_equality": True,
                "coarse_mismatch_result": "NONE",
                "coarse_bucket_statistics": None if not self.build_count else
                    self.bucket_public(), "build_count": self.build_count,
                "built": self.build_count == 1,
                "cached_state_digest": self._state_digest,
                "cached_slot_digest": self._slot_digest,
                "cached_public_digest": self._public_digest}


def producer_replay_typed_ten_state(runtime: dict[str, Any],
                                    word: Sequence[int]) -> tuple[bytes, ...]:
    """Checker-independent direct replay used to bind every BFS edge word."""
    p176 = runtime["p176"]
    values = p176.eval_word_coordinates(runtime["old"], runtime["e3"],
                                        runtime["e4"], runtime["contexts"],
                                        runtime["delete"], list(word))
    return tuple(p176.packed_joint_blob(value,
                                        "producer direct typed ten-state replay")
                 for value in values)


def producer_full_gamma_diagnostic(runtime: dict[str, Any], state: Any) -> bytes:
    """Encode the full JointGroup state, not its ten-coordinate projection."""
    require(type(state) is tuple and len(state) == 2 and
            type(state[1]) is tuple and len(state[1]) == 31,
            "producer full Gamma JointGroup shape")
    p176 = runtime["p176"]
    pieces = [p176.packed_joint_blob(state[0],
        "producer full Gamma E3 factor")]
    pieces.extend(p176.packed_joint_blob(value,
        "producer full Gamma E4 factor") for value in state[1])
    widths = [len(value) for value in pieces]
    require(widths == [40] + [154] * 31 and sum(widths) == 4814,
            "producer full Gamma JointGroup codec")
    return b"".join(pieces)


def producer_parent_letter_stream_digest(parents: Sequence[int], letters: bytes,
                                         meter: Meter) -> str:
    """Hash compact u32le/u8 owners without million-element Python int lists."""
    require(len(parents) == len(letters) == K0_STATE_COUNT,
            "producer parent-letter compact owner dimensions")
    digest = hashlib.sha256(b"v12c-q0-parent-letter-compact/v1\0")
    block = bytearray()
    for index, parent in enumerate(parents):
        if (index & 4095) == 0:
            meter.check("q0_parent_stream_digest")
        block.extend(struct.pack("<I", int(parent)))
        if len(block) >= 1 << 20:
            digest.update(block); block.clear()
    if block:
        digest.update(block)
    for offset in range(0, len(letters), 1 << 20):
        meter.check("q0_letter_stream_digest")
        digest.update(letters[offset:offset + (1 << 20)])
    return digest.hexdigest()


class StableProducerFibreOracle:
    """Live FibreOracle surface with a stable full-state K0 owner."""
    def __init__(self, runtime: dict[str, Any], monitor: Any) -> None:
        live = runtime["live"]
        self.rt = runtime; self.monitor = monitor
        self.cache: dict[tuple[int, bytes], dict[str, Any] | None] = {}
        self.kernel_states: dict[int, list[dict[str, Any]]] = {}
        self.kernel_seen: dict[int, set[tuple[bytes, ...]]] = {}
        self.kernel_heads: dict[int, int] = {}
        self.coarse_indices: dict[int, StableProducerK0Index] = {}
        self.released_indices: dict[int, dict[str, Any]] = {}

    def _coarse_index(self, coordinate: int) -> StableProducerK0Index:
        require(0 <= coordinate < 10, "producer K0 coordinate")
        require(coordinate not in self.released_indices,
                "producer K0 coordinate released")
        index = self.coarse_indices.get(coordinate)
        if index is None:
            width = 40 if coordinate < 5 else 154
            degree = 36 if coordinate < 5 else 144
            index = StableProducerK0Index(coordinate,
                self.rt["stores"][coordinate], width, degree, self.monitor)
            self.coarse_indices[coordinate] = index
        return index

    def index_public(self) -> dict[str, Any]:
        e3_payload = K0_STATE_COUNT * 40 + K0_CAPACITY * 4
        e4_payload = K0_STATE_COUNT * 154 + K0_CAPACITY * 4
        return {"state_count": K0_STATE_COUNT, "coordinate_count": 10,
                "table_length": K0_CAPACITY,
                "payload_bytes_per_coordinate": [e3_payload] * 5 +
                    [e4_payload] * 5,
                "payload_bytes_total": 5 * e3_payload + 5 * e4_payload,
                "uint32_itemsize": 4,
                "hash": "sha256(v12c-k0-coarse-key\\0)[:8]:little",
                "full_state_equality": True,
                "coarse_mismatch_result": "NONE",
                "injectivity": "hard_stop_on_duplicate_coarse_key",
                "built_coordinate_count": len(self.coarse_indices),
                "built_coordinates": sorted(self.coarse_indices),
                "tables": {str(i): self.coarse_indices[i].public()
                           for i in sorted(self.coarse_indices)},
                "released_coordinates": sorted(self.released_indices),
                "released_tables": {str(i): self.released_indices[i]
                                     for i in sorted(self.released_indices)}}

    def release_coordinate(self, coordinate: int) -> None:
        index = self.coarse_indices.pop(coordinate, None)
        if index is None:
            return
        require(index.build_count == 1, "producer K0 release before build")
        self.released_indices[coordinate] = {
            "build_count": index.build_count,
            "state_digest": index.state_digest(),
            "slot_digest": index.slot_digest(),
            "public_digest": index.public_digest(),
            "payload_bytes": index.state_count * index.width + K0_CAPACITY * 4}

    def canonical(self, coordinate: int, target: bytes) -> dict[str, Any] | None:
        require(0 <= coordinate < 10 and type(target) is bytes and
                len(target) == (40 if coordinate < 5 else 154),
                "producer K0 canonical target")
        key = (coordinate, target)
        if key in self.cache:
            return self.cache[key]
        live = self.rt["live"]; p176 = self.rt["p176"]
        amap = self.rt["A_maps"][f"S{coordinate}"]
        index = self._coarse_index(coordinate)
        candidates: list[tuple[int, int, dict[str, Any]]] = []
        for (a,), gid in amap.items():
            section_target = p176.multiply_blob(
                p176.inverse_blob(a, coordinate, self.rt["e3"], self.rt["e4"]),
                target, coordinate, self.rt["e3"], self.rt["e4"])
            qid = index.lookup_full(section_target)
            if qid is None:
                continue
            section = p176.section_row(self.rt["stores"], qid)
            require(section[coordinate] == section_target,
                    "producer K0 retained full state")
            require(p176.multiply_blob(a, section[coordinate], coordinate,
                                       self.rt["e3"], self.rt["e4"]) == target,
                    "producer K0 target product")
            gamma_row = tuple(live.element_blob(self.rt, value)
                              for value in self.rt["projected"][gid])
            blobs = live.multiply_coordinate_rows(self.rt, gamma_row, section)
            gamma_word = list(self.rt["gamma"].section_word(gid))
            q0_word = p176.q0_section_word(qid, self.rt["parents"],
                                           self.rt["letters"])
            word = live.reduce_word(gamma_word + q0_word)
            require(blobs[coordinate] == target and
                    live.coordinate_blobs(self.rt, word) == blobs,
                    "producer literal singleton section witness")
            candidates.append((qid, gid, {"coordinate": coordinate,
                "target_hex": target.hex(), "q0_state_id": qid + 1,
                "gamma_state_id": gid + 1, "source_word": word,
                "gamma_source_word": gamma_word, "q0_source_word": q0_word,
                "coordinate_blobs": blobs,
                "section_blob_hex": [x.hex() for x in section],
                "gamma_coordinate_blob_hex": gamma_row[coordinate].hex(),
                "selection": "least_qid_then_gid_full_state_hash"}))
        answer = min(candidates, key=lambda item: (item[0], item[1]))[2] \
            if candidates else None
        self.cache[key] = answer
        return answer

    def _kernel_generators(self, coordinate: int) -> list[list[int]]:
        row = self.rt["emitted"][f"S{coordinate}"]
        positive = ([list(word) for word in row["Gamma_S0_generators"]] +
                    [list(word) for word in row["adjusted_L_generators"]])
        generators: list[list[int]] = []
        for word in positive:
            generators.extend((word, self.rt["live"].inverse_word(word)))
        return generators
    def verify_kernel_orders(self) -> tuple[int, ...]:
        """Authenticate the word-bearing kernel BFS without live CoarseInverse."""
        live = self.rt["live"]
        identity_blobs = producer_replay_typed_ten_state(self.rt, [])
        for coordinate, expected in enumerate(KERNEL_ORDERS):
            states = [{"source_word": [], "coordinate_blobs": identity_blobs}]
            seen = {identity_blobs}; head = 0
            generators = self._kernel_generators(coordinate)
            if expected != 1:
                require(generators, "producer nontrivial kernel roster")
            identity = identity_blobs[coordinate]
            generator_blobs = [producer_replay_typed_ten_state(self.rt, generator)
                               for generator in generators]
            while head < len(states):
                base = states[head]; head += 1
                for generator, generator_state in zip(generators, generator_blobs):
                    word = live.reduce_word(base["source_word"] + generator)
                    blobs = live.multiply_coordinate_rows(
                        self.rt, base["coordinate_blobs"], generator_state)
                    replayed = producer_replay_typed_ten_state(self.rt, word)
                    require(blobs == replayed,
                            "producer kernel direct typed-ten-state replay")
                    require(blobs[coordinate] == identity,
                            "producer kernel singleton fibre")
                    if blobs in seen:
                        continue
                    seen.add(blobs)
                    states.append({"source_word": word,
                                   "coordinate_blobs": blobs})
            require(len(states) == expected and len(seen) == expected,
                    "producer kernel order")
            self.kernel_states[coordinate] = states
            self.kernel_seen[coordinate] = seen
            self.kernel_heads[coordinate] = head
        return KERNEL_ORDERS

    def weighted_support(self, formula: dict[str, Any]) -> dict[str, Any]:
        targets = sorted(formula["merged"], key=lambda item: (item[0], item[1]))
        rows = [{"coordinate": coordinate, "target_hex": target.hex(),
                 "kernel_order": KERNEL_ORDERS[coordinate]}
                for coordinate, target in targets]
        return {"K": int(formula["constant"]),
                "W": sum(row["kernel_order"] for row in rows),
                "delta_order": DELTA_ORDER,
                "kernel_orders": list(KERNEL_ORDERS),
                "distinct_targets": rows}


def enumerate_q0_sections_fast(old: Any, q0_marked: Sequence[tuple[int, ...]],
                               coordinate_marks: Sequence[Sequence[Any]],
                               e3: Any, e4: Any, p176: Any,
                               meter: Meter) -> tuple[
                                   list[bytes], dict[bytes, int], list[int],
                                   bytes, list[bytearray],
                                   list[tuple[int, int, int]], dict[str, int]]:
    """Discover Q0 with duplicate-first edge handling.

    The frozen task176 routine computes all ten coordinate products before it
    knows whether the coarse successor was already seen.  This local owner
    makes the duplicate decision immediately after the permutation successor
    lookup; only a newly accepted state receives the ten-coordinate product
    work and store append.  The counters are part of the heavy identity.
    """
    identity = bytes(range(36))
    generators = [bytes(row) for row in q0_marked]
    qtables = []
    for generator in generators:
        table = bytearray(range(256))
        for index, value in enumerate(generator):
            table[index] = int(value)
        qtables.append(bytes(table))
    states = [identity]
    ids = {identity: 0}
    parents = [0]
    letters = bytearray([0])
    widths = [40] * 5 + [154] * 5
    coordinate_values = [bytearray(
        p176.packed_joint_blob(e3.identity if coordinate < 5 else e4.identity,
                               "v12c Q0 identity"))
        for coordinate in range(10)]
    right_tables: list[list[bytes]] = []
    for coordinate in range(10):
        rows = []
        for letter in range(2):
            table = bytearray(range(256))
            raw = bytes(coordinate_marks[coordinate][letter][0])
            for index, value in enumerate(raw):
                table[index] = int(value)
            rows.append(bytes(table))
        right_tables.append(rows)
    pc_cache: dict[tuple[int, int, bytes], bytes] = {}
    duplicate_edges: list[tuple[int, int, int]] = []
    duplicate_edge_count = 0
    accepted_edge_count = 0
    coordinate_product_count = 0
    for sid, state in enumerate(states):
        if (sid & 4095) == 0:
            meter.check("Q0_discovery")
        for letter in range(2):
            nxt = state.translate(qtables[letter])
            prior = ids.get(nxt)
            if prior is not None:
                duplicate_edge_count += 1
                if len(duplicate_edges) < 256 and prior != sid:
                    duplicate_edges.append((sid, letter + 1, prior))
                # The known duplicate must not perform any coordinate work.
                continue
            new_blobs: list[bytes] = []
            for coordinate, width in enumerate(widths):
                degree = 36 if coordinate < 5 else 144
                left = bytes(coordinate_values[coordinate][sid * width:
                                                           (sid + 1) * width])
                left_perm, left_pc = p176.split_blob(left, degree)
                right = coordinate_marks[coordinate][letter]
                perm_raw = bytes(left_perm).translate(right_tables[coordinate][letter])
                cache_key = (coordinate, letter, bytes(left_pc))
                pc_raw = pc_cache.get(cache_key)
                if pc_raw is None:
                    if len(pc_cache) >= PC_CACHE_ENTRY_CAP:
                        released = len(pc_cache)
                        pc_cache.clear()
                        meter.release_live("pc_cache_entries", released,
                                           "Q0_pc_cache_clear")
                    meter.reserve("pc_cache_insertions", 1, "Q0_pc_cache")
                    meter.reserve_live("pc_cache_entries", 1, "Q0_pc_cache")
                    pc = e3.pc if coordinate < 5 else e4.pc
                    try:
                        pc_raw = bytes(pc.mul(left_pc, right[1]))
                        require(cache_key not in pc_cache,
                                "Q0 pc_cache duplicate after precharge")
                        pc_cache[cache_key] = pc_raw
                        meter.commit("pc_cache_insertions", 1)
                    except BaseException:
                        meter.release_live("pc_cache_entries", 1,
                                           "Q0_pc_cache_rollback")
                        raise
                new_blobs.append(perm_raw + pc_raw)
                coordinate_product_count += 1
            new_id = len(states)
            ids[nxt] = new_id
            states.append(nxt)
            parents.append(sid)
            letters.append(letter + 1)
            accepted_edge_count += 1
            for store, value in zip(coordinate_values, new_blobs):
                store.extend(value)
    final_cache_entries = len(pc_cache)
    pc_cache.clear()
    meter.release_live("pc_cache_entries", final_cache_entries,
                       "Q0_pc_cache_final_release")
    require(len(states) == 1_469_664 and len(ids) == 1_469_664,
            "Q0 exact local discovery order")
    require(all(len(store) == 1_469_664 * width
                for store, width in zip(coordinate_values, widths)),
            "local Q0 section store dimensions")
    require(duplicate_edge_count + accepted_edge_count == 2 * len(states),
            "local Q0 edge accounting")
    return states, ids, parents, bytes(letters), coordinate_values, \
        duplicate_edges, {"duplicate_edges": duplicate_edge_count,
                           "accepted_edges": accepted_edge_count,
                           "coordinate_products": coordinate_product_count,
                           "duplicate_coordinate_products": 0,
                           "pc_cache_entry_cap": PC_CACHE_ENTRY_CAP,
                           "pc_cache_insertions": meter.counters[
                               "pc_cache_insertions"]}


def _producer_bit_set(bits: bytearray, index: int) -> None:
    bits[index >> 3] |= 1 << (index & 7)


def _producer_bit_get(bits: bytearray | bytes, index: int) -> bool:
    return bool(bits[index >> 3] & (1 << (index & 7)))


def shared_l_memberships(stores: Sequence[bytearray],
                         A_maps: dict[str, dict[tuple[bytes, ...], int]],
                         families: Sequence[tuple[str, Sequence[int]]],
                         meter: Meter) -> tuple[dict[str, bytearray], dict[str, int],
                                                dict[str, Any]]:
    """Build every L bitset in one indexed Q0 pass and freeze its digest.

    The rows are sliced once and all registered family keys are tested before
    advancing.  Later family proofs consume these immutable bitsets and the
    common digest; they do not rescan the ten coordinate stores.
    """
    size = (1_469_664 + 7) // 8
    bits = {name: bytearray(size) for name, _ in families}
    counts = {name: 0 for name, _ in families}
    for state in range(1_469_664):
        if (state & 4095) == 0:
            meter.check("A_L_membership_scan")
        row = tuple(bytes(store[state * width:(state + 1) * width])
                    for store, width in zip(stores, [40] * 5 + [154] * 5))
        for name, indices in families:
            if tuple(row[index] for index in indices) in A_maps[name]:
                _producer_bit_set(bits[name], state)
                counts[name] += 1
    require(all(count > 0 and 1_469_664 % count == 0
                for count in counts.values()), "shared L Lagrange")
    public_rows = [{"name": name, "count": counts[name],
                    "bitset_sha256": sha_bytes(bytes(bits[name]))}
                   for name, _ in families]
    groups: dict[str, list[str]] = {}
    for row in public_rows:
        groups.setdefault(row["bitset_sha256"], []).append(row["name"])
    identity_bits = bytes(bytearray([1]) + bytearray(size - 1))
    public = {"schema": SCHEMA + "/shared-l-bitset/v1",
              "state_count": 1_469_664, "families": public_rows,
              "combined_sha256": sha_obj(public_rows),
              "single_store_pass": True,
              "bitset_groups": [{"bitset_sha256": digest,
                                  "families": sorted(names)}
                                 for digest, names in sorted(groups.items())],
              "identity_bitset_sha256": sha_bytes(identity_bits)}
    return bits, counts, public


def _producer_q0_closure(old: Any, generators: Sequence[int],
                         qstates: Sequence[bytes], qids: dict[bytes, int],
                         budget: Meter) -> set[int]:
    selected = list(dict.fromkeys(int(value) for value in generators))
    tables = []
    for state_id in selected:
        table = bytearray(range(256))
        for index, value in enumerate(qstates[state_id]):
            table[index] = value
        tables.append(bytes(table))
    seen = {0}; queue = [0]
    for cursor, state_id in enumerate(queue):
        if (cursor & 4095) == 0:
            budget.check("L_subgroup_closure")
        state = qstates[state_id]
        for table in tables:
            target = qids[state.translate(table)]
            if target not in seen:
                seen.add(target); queue.append(target)
    return seen


def prove_l_shared(old: Any, name: str, membership: bytearray, count: int,
                   qstates: Sequence[bytes], qids: dict[bytes, int],
                   q0_marked: Sequence[tuple[int, ...]], meter: Meter,
                   shared_public: dict[str, Any],
                   proof_cache: dict[tuple[str, int], tuple[list[int], dict[str, Any]]] | None = None
                   ) -> tuple[list[int], dict[str, Any]]:
    """Prove one family against the frozen, one-pass L bitset owner."""
    key = (sha_bytes(bytes(membership)), int(count))
    if proof_cache is not None and key in proof_cache:
        cached_selected, cached_proof = proof_cache[key]
        proof = dict(cached_proof)
        proof["family"] = name
        proof["shared_l_bitset_sha256"] = shared_public["combined_sha256"]
        proof["shared_proof_key"] = key[0]
        return list(cached_selected), proof
    if count == 1:
        require(key[0] == shared_public["identity_bitset_sha256"],
                name + " identity-only bitset")
        selected: list[int] = []
        proof = {"identity": True,
            "closure_by_exact_generated_subgroup": True,
            "inverse_generators_in_subgroup": True,
            "normal_under_q0_x_y": True, "generated_order": 1,
            "greedy_generator_state_ids": [], "normality_witness_rows": [],
            "proof_method": "shared_identity_only_bitset_and_closure",
            "shared_l_bitset_sha256": shared_public["combined_sha256"],
            "shared_proof_key": key[0], "family": name}
        if proof_cache is not None:
            proof_cache[key] = (list(selected), dict(proof))
        return selected, proof
    require(_producer_bit_get(membership, 0), name + " L identity")
    selected: list[int] = []
    subgroup = {0}
    for state_id in range(1_469_664):
        if (state_id & 4095) == 0:
            meter.check("L_generator_roster_scan")
        if _producer_bit_get(membership, state_id) and state_id not in subgroup:
            selected.append(state_id)
            subgroup = _producer_q0_closure(old, selected, qstates, qids, meter)
            for ordinal, value in enumerate(subgroup):
                if (ordinal & 4095) == 0:
                    meter.check("L_closure_subset")
                require(_producer_bit_get(membership, value),
                        name + " closure subset")
            if len(subgroup) == count:
                break
    generated_bitset = len(subgroup) == count
    for state_id in range(1_469_664):
        if (state_id & 4095) == 0:
            meter.check("L_generated_bitset_compare")
        if (state_id in subgroup) != _producer_bit_get(membership, state_id):
            generated_bitset = False
            break
    require(generated_bitset, name + " generated bitset")
    require(1_469_664 % count == 0, name + " L divisibility")
    selected_inverse_ok = True
    normal_rows = []
    # Q0 inverse/conjugation are validated by the same literal permutation
    # arithmetic used by the frozen owner, while membership bytes stay shared.
    marked_bytes = [bytes(value) for value in q0_marked]
    require(all(value in qids for value in marked_bytes), name + " marked roster")
    marked_ids = [qids[value] for value in marked_bytes]
    for generator in selected:
        inverse = bytes(old.perm_inv(tuple(qstates[generator])))
        selected_inverse_ok &= qids[inverse] in subgroup
        for outer_id in marked_ids:
            outer = qstates[outer_id]
            conjugate = bytes(old.perm_mul(tuple(old.perm_mul(
                tuple(old.perm_inv(tuple(outer))), tuple(qstates[generator]))),
                tuple(outer))))
            conjugate_id = qids[conjugate]
            normal_rows.append([generator + 1, outer_id, conjugate_id + 1])
            require(conjugate_id in subgroup, name + " normality")
    require(selected_inverse_ok, name + " inverses")
    proof = {"identity": True,
        "closure_by_exact_generated_subgroup": True,
        "inverse_generators_in_subgroup": True, "normal_under_q0_x_y": True,
        "generated_order": len(subgroup),
        "greedy_generator_state_ids": [value + 1 for value in selected],
        "normality_witness_rows": normal_rows,
        "proof_method": "greedy_generator_closure_against_shared_exact_bitset",
        "shared_l_bitset_sha256": shared_public["combined_sha256"],
        "shared_proof_key": key[0], "family": name}
    if proof_cache is not None:
        proof_cache[key] = (list(selected), dict(proof))
    return selected, proof


def build_heavy(runtime: dict[str, Any], registry: SourceRegistry,
                meter: Meter) -> dict[str, Any]:
    """One Q0-LATE construction.  The digest is published only at the end."""
    require("heavy_input_sha256" not in runtime and "qstates" not in runtime,
            "heavy runtime constructed twice")
    meter.check("heavy_Q0_late_start")
    p176, old = runtime["p176"], runtime["old"]
    runtime["task176_receipt"] = registry.json("task176_receipt")
    e3, e4 = runtime["e3"], runtime["e4"]
    q3, contexts = runtime["q3"], runtime["contexts"]
    jointmod = registry.load("joint")

    class PackedJointGroup(jointmod.JointGroup):
        def blob(self, value: Any) -> bytes:
            return p176.packed_joint_blob(value, "v7 Gamma state")

    words = [list(row["word"]) for row in q3["correction_fibre"]["records"]
             if row.get("word")]
    gamma = PackedJointGroup(old, e3, e4, contexts, words)
    require(len(gamma.states) == 243 and
            gamma.public()["state_rows_sha256"] ==
            runtime["joint_receipt"]["gamma"]["state_rows_sha256"],
            "heavy Gamma identity")
    fine, fine_public = p176.build_fine_deletion(e3, e4, meter)
    q0_marked = [p176.canonical_packed_permutation(
        old.perm_from_row(row, 36), 36, "v7 Q0 mark")
        for row in q3["coarse_models"]["Q0"]["marked_permutations"]]
    delete, deletion_public = p176.make_deleter(old, e3, e4, fine, q0_marked)
    deletion_public["fine"] = fine_public
    projected = [p176.projection(state, delete) for state in gamma.states]
    require(len(projected) == 243 and all(len(row) == 10 for row in projected),
            "heavy projected Gamma")
    projected_packed = [b"".join(p176.packed_joint_blob(
        value, "v12c projected Gamma state") for value in row)
        for row in projected]
    require(all(len(row) == 970 for row in projected_packed),
            "heavy projected Gamma 970-byte owner")
    projected_widths = [40] * 5 + [154] * 5
    full_diagnostic_widths = [40] + [154] * 31
    full_diagnostic_canary = producer_full_gamma_diagnostic(runtime,
                                                             gamma.states[0])
    runtime["full_gamma_canary"] = full_diagnostic_canary
    require(sum(projected_widths) == 970 and
            sum(full_diagnostic_widths) == 4814 and
            len(full_diagnostic_canary) == 4814 and
            runtime["joint_receipt"].get("gamma", {}).get("order") == 243,
            "heavy full Gamma diagnostic typing")
    coordinate_marks = []
    for item in p176.COORDINATES:
        context = contexts[item["context_id"] - 1]
        row = [e4.eval([letter], context) for letter in (1, 2)]
        if item["type"] == "E3":
            row = [delete(value) for value in row]
        coordinate_marks.append(row)
    A_maps: dict[str, dict[tuple[bytes, ...], int]] = {}
    A_public: dict[str, Any] = {}
    for name, indices in p176.FAMILIES:
        A_maps[name], A_public[name] = p176.family_public_A(
            old, name, indices, projected, e3, e4, coordinate_marks)
    qstates, qids, parents, letters, stores, duplicate_edges, q0_work = \
        enumerate_q0_sections_fast(old, q0_marked, coordinate_marks, e3, e4,
                                   p176, meter)
    require(len(qstates) == len(qids) == len(parents) == len(letters) == 1_469_664 and
            len(stores) == 10, "heavy Q0 complete owner")
    memberships, L_counts, l_bitset_public = shared_l_memberships(
        stores, A_maps, p176.FAMILIES, meter)
    emitted: dict[str, Any] = {}
    membership_public: dict[str, Any] = {}
    l_proof_cache: dict[tuple[str, int], tuple[list[int], dict[str, Any]]] = {}
    for name, indices in p176.FAMILIES:
        selected, proof = prove_l_shared(
            old, name, memberships[name], L_counts[name], qstates, qids,
            q0_marked, meter, l_bitset_public, l_proof_cache)
        gamma_selected, gamma_kernel = p176.gamma_kernel_generators(
            gamma, projected, indices, e3, e4, old)
        gamma_words = [list(gamma.section_word(sid)) for sid in gamma_selected]
        adjusted: list[list[int]] = []
        for qid in selected:
            section = p176.section_row(stores, qid)
            key = p176.family_key(section, indices)
            need = p176.family_inverse_key(key, indices, e3, e4)
            require(need in A_maps[name], "heavy adjusted-L owner")
            gid = A_maps[name][need]
            word = runtime["live"].reduce_word(
                list(gamma.section_word(gid)) +
                p176.q0_section_word(qid, parents, letters))
            replay = p176.eval_word_coordinates(old, e3, e4, contexts, delete, word)
            identity = p176.tuple_key(old, p176.family_identity(indices, e3, e4))
            require(p176.tuple_key(old, tuple(replay[i] for i in indices)) == identity,
                    "heavy adjusted-L literal replay")
            adjusted.append(word)
        emitted[name] = {"Gamma_S0_generators": gamma_words,
                         "adjusted_L_generators": adjusted,
                         "Gamma_S0_order": len(gamma_kernel),
                         "L_order": L_counts[name], "L_proof": proof}
        membership_public[name] = {"count": L_counts[name],
                                   "sha256": _stream_store_digest(
                                       memberships[name], meter),
                                   "adjusted_L_sha256": sha_obj(adjusted)}
    runtime.update({"delete": delete, "deletion_public": deletion_public,
                    "gamma": gamma, "projected": projected,
                    "coordinate_marks": coordinate_marks, "A_maps": A_maps,
                    "A_public": A_public, "qstates": qstates, "qids": qids,
                    "parents": parents, "letters": letters, "stores": stores,
                    "q0_duplicate_edges": duplicate_edges,
                    "q0_work": q0_work, "l_bitset_public": l_bitset_public,
                    "l_proof_cache_keys": sorted(
                        [[key[0], key[1]] for key in l_proof_cache]),
                    "memberships": memberships, "emitted": emitted})
    fibres = StableProducerFibreOracle(runtime, meter)
    # Coarse inverse indices are materialized only by a correction query for
    # the requested coordinate and remain immutable thereafter.
    kernel_orders = fibres.verify_kernel_orders()
    require(tuple(kernel_orders) == KERNEL_ORDERS and
            fibres.index_public()["built_coordinates"] == [],
            "heavy coarse-index/kernel owners")
    runtime["fibres"] = fibres
    heavy_public = {
        "q0_order": len(qstates),
        "gamma_order": len(gamma.states),
        "q0_state_count": len(qstates),
        "q0_state_id_sha256": _stream_state_digest(qstates, qids, meter),
        "parents_sha256": _stream_canonical_int_list_digest(parents, meter),
        "letters_sha256": sha_bytes(letters),
        "store_sha256": [_stream_store_digest(store, meter) for store in stores],
        "memberships": membership_public,
        "A_public_sha256": sha_obj(A_public),
        "gamma_state_sha256": gamma.public()["state_rows_sha256"],
        "projected_sha256": sha_obj([[p176.packed_joint_blob(value,
            "v7 projected digest").hex() for value in row] for row in projected]),
        "projected_record_bytes": 970,
        "projected_widths": projected_widths,
        "full_diagnostic_codec": "jointgroup-E3-plus-31-E4/v1",
        "full_diagnostic_record_bytes": 4814,
        "full_diagnostic_factor_widths": full_diagnostic_widths,
        "full_diagnostic_canary_state_id": 1,
        "full_diagnostic_canary_sha256": sha_bytes(full_diagnostic_canary),
        "full_diagnostic_evaluated_state_count": 1,
        "full_diagnostic_non_load_bearing": True,
        "coarse_indices": fibres.index_public(),
        "q0_duplicate_edges": duplicate_edges,
        "q0_work": q0_work,
        "shared_l_bitset": l_bitset_public,
        "shared_l_proof_cache": {
            "keys": sorted([[key[0], key[1]] for key in l_proof_cache]),
            "build_count": len(l_proof_cache),
            "family_replays": len(p176.FAMILIES),
        },
        "kernel_orders": list(kernel_orders),
        "deletion_sha256": sha_obj(deletion_public),
        "light_input_sha256": runtime["light_input_sha256"],
    }
    runtime["heavy_public"] = heavy_public
    runtime["heavy_input_sha256"] = sha_obj(heavy_public)
    return runtime


def estimated_json_size(value: Any) -> int:
    if isinstance(value, dict):
        return 2 + sum(len(str(key)) + estimated_json_size(item) + 8
                       for key, item in value.items())
    if isinstance(value, (list, tuple)):
        return 2 + sum(estimated_json_size(item) + 1 for item in value)
    if isinstance(value, (bytes, bytearray)):
        return len(value) * 2 + 2
    return len(str(value)) + 4


def atomic_json(path: Path, value: dict[str, Any], *, allow_replace: bool = False,
                maximum: int = MAX_CHECKPOINT_BYTES,
                meter: Meter | None = None,
                trace_runtime: dict[str, Any] | None = None) -> tuple[int, str]:
    """Durable no-replace publication with retained-temp rollback evidence."""
    if trace_runtime is not None:
        _producer_validator_event(trace_runtime, "exclusive_json", "stale",
                                  "candidate.path")
    if allow_replace:
        raise ProtocolStop("replace publication is not an owned transport")
    require(type(maximum) is int and 0 < maximum <= MAX_CHECKPOINT_BYTES,
            "serialization cap registry")
    if os.path.lexists(str(path)):
        raise ProtocolStop("stale output")
    if meter is not None and maximum == MAX_CANDIDATE_BYTES:
        require(meter.live_reserved["output_bytes"] == MAX_CANDIDATE_BYTES,
                "full output cap must precede R construction")
    estimated = estimated_json_size(value) + 1
    if estimated > maximum:
        raise ResourceStop("checkpoint_serialization", "checkpoint_bytes",
                           estimated, maximum)
    raw = canonical(value) + b"\n"
    if len(raw) > maximum:
        raise ResourceStop("checkpoint_serialization", "checkpoint_bytes",
                           len(raw), maximum)
    expected_sha = sha_bytes(raw)
    parent_flags = (os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                    getattr(os, "O_DIRECTORY", 0) |
                    getattr(os, "O_NOFOLLOW", 0))
    try:
        directory_fd = os.open(path.parent, parent_flags)
    except OSError as exc:
        raise ProtocolStop("publication parent unavailable") from exc
    temporary_name = path.name + f".tmp.{os.getpid()}"
    final_name = path.name
    temporary_visible = False
    final_visible = False
    success = False
    try:
        parent_before = os.fstat(directory_fd)
        named_parent = os.lstat(path.parent)
        require(stat.S_ISDIR(parent_before.st_mode) and
                not stat.S_ISLNK(named_parent.st_mode) and
                (parent_before.st_dev, parent_before.st_ino,
                 parent_before.st_mode) ==
                (named_parent.st_dev, named_parent.st_ino,
                 named_parent.st_mode),
                "publication parent identity")
        try:
            os.stat(final_name, dir_fd=directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise ProtocolStop("stale output")
        flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
        fd = os.open(temporary_name, flags, 0o600, dir_fd=directory_fd)
        temporary_visible = True
        try:
            view = memoryview(raw)
            while view:
                if meter is not None:
                    meter.check("publication_write")
                written = os.write(fd, view[:1 << 20])
                if written <= 0:
                    raise OSError("atomic short write")
                view = view[written:]
            os.fsync(fd)
            temporary_stat = os.fstat(fd)
        finally:
            os.close(fd)
        try:
            os.link(temporary_name, final_name, src_dir_fd=directory_fd,
                    dst_dir_fd=directory_fd, follow_symlinks=False)
        except FileExistsError as exc:
            raise ProtocolStop("stale output") from exc
        except OSError as exc:
            raise ProtocolStop("exclusive publication") from exc
        final_visible = True
        verify_fd = os.open(final_name, os.O_RDONLY |
                            getattr(os, "O_CLOEXEC", 0) |
                            getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd)
        try:
            final_stat = os.fstat(verify_fd)
            require((temporary_stat.st_dev, temporary_stat.st_ino,
                     temporary_stat.st_size) ==
                    (final_stat.st_dev, final_stat.st_ino, final_stat.st_size) and
                    final_stat.st_size == len(raw),
                    "publication final physical identity")
            verify_hash = hashlib.sha256()
            while True:
                if meter is not None:
                    meter.check("publication_identity_hash")
                block = os.read(verify_fd, 1 << 20)
                if not block:
                    break
                verify_hash.update(block)
            require(verify_hash.hexdigest() == expected_sha,
                    "publication final physical digest")
            os.fsync(verify_fd)
        finally:
            os.close(verify_fd)
        parent_after = os.fstat(directory_fd)
        require((parent_before.st_dev, parent_before.st_ino,
                 parent_before.st_mode) ==
                (parent_after.st_dev, parent_after.st_ino,
                 parent_after.st_mode),
                "publication parent identity changed")
        os.fsync(directory_fd)
        os.unlink(temporary_name, dir_fd=directory_fd)
        temporary_visible = False
        os.fsync(directory_fd)
        success = True
    except BaseException as original:
        rollback_errors: list[str] = []
        if final_visible:
            try:
                if meter is not None:
                    meter.check("publication_rollback_final")
                os.unlink(final_name, dir_fd=directory_fd)
                final_visible = False
                os.fsync(directory_fd)
            except BaseException as rollback:
                rollback_errors.append("final:" + type(rollback).__name__)
        if temporary_visible:
            try:
                if meter is not None:
                    meter.check("publication_rollback_temp")
                os.unlink(temporary_name, dir_fd=directory_fd)
                temporary_visible = False
                os.fsync(directory_fd)
            except BaseException as rollback:
                rollback_errors.append("temp:" + type(rollback).__name__)
        if rollback_errors:
            raise ProtocolStop("publication rollback failure:" +
                               ",".join(rollback_errors)) from original
        raise
    finally:
        try:
            if not success and final_visible:
                os.unlink(final_name, dir_fd=directory_fd)
                os.fsync(directory_fd)
        except BaseException:
            pass
        try:
            if temporary_visible:
                os.unlink(temporary_name, dir_fd=directory_fd)
                os.fsync(directory_fd)
        except BaseException:
            pass
        os.close(directory_fd)
        if meter is not None and maximum == MAX_CANDIDATE_BYTES and \
                meter.live_reserved["output_bytes"] == MAX_CANDIDATE_BYTES:
            meter.release_live("output_bytes", MAX_CANDIDATE_BYTES,
                               "publication_or_rollback_complete")
        if trace_runtime is not None:
            trace_runtime["_last_owner_disposed"] = not temporary_visible
    return len(raw), expected_sha

def read_bounded_json(path: Path, maximum: int,
                      meter: Meter | None = None,
                      mutation_hook: Any | None = None,
                      trace_runtime: dict[str, Any] | None = None
                      ) -> tuple[dict[str, Any], dict[str, Any]]:
    before = None
    after = None
    path_after = None
    raw = bytearray()
    if trace_runtime is not None:
        owner = str(trace_runtime.get("_physical_logical_label", "candidate.path"))
        _producer_validator_event(trace_runtime, "physical_owner_open",
                                  "physical_open", owner)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        if trace_runtime is not None:
            try:
                failed_path = os.lstat(path)
            except OSError:
                failed_path = None
            _producer_capture_physical_projection(
                trace_runtime, path, before=None, after=None, path_after=failed_path,
                raw=None, reason="physical open")
            trace_runtime["_last_owner_disposed"] = True
        raise InputStop("physical open") from exc
    try:
        try:
            before = os.fstat(fd)
            if trace_runtime is not None:
                _producer_validator_event(trace_runtime, "physical_owner_open",
                                          "unique_link", owner)
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                    0 < before.st_size <= maximum, "physical regular unique owner")
            if mutation_hook is not None:
                mutation_hook(path)
            while len(raw) < before.st_size:
                if meter is not None:
                    meter.check("streaming_physical_read")
                chunk = os.read(fd, min(1 << 20, before.st_size - len(raw)))
                if not chunk:
                    raise InputStop("bounded_short_read")
                raw.extend(chunk)
            after = os.fstat(fd)
            if trace_runtime is not None:
                _producer_validator_event(trace_runtime, "physical_owner_open",
                                          "fd_TOCTOU", owner)
            require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
                     before.st_nlink) ==
                    (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                     after.st_nlink), "physical fd TOCTOU")
            try:
                path_after = os.lstat(path)
            except OSError as exc:
                raise InputStop("physical pathname substituted") from exc
            if trace_runtime is not None:
                _producer_validator_event(trace_runtime, "physical_owner_open",
                                          "pathname_identity", owner)
            require(not stat.S_ISLNK(path_after.st_mode) and
                (path_after.st_dev, path_after.st_ino, path_after.st_size,
                     path_after.st_mtime_ns, path_after.st_nlink) ==
                    (after.st_dev, after.st_ino, after.st_size,
                     after.st_mtime_ns, after.st_nlink),
                    "physical pathname identity")
            try:
                if meter is not None: meter.check("raw_decode_parse", ())
                immutable_raw = bytes(raw)
                value = json.loads(immutable_raw.decode("ascii"))
            except (UnicodeError, json.JSONDecodeError) as exc:
                raise InputStop("bounded_json") from exc
            require(type(value) is dict, "bounded JSON object")
            require(immutable_raw == canonical(value) + b"\n",
                    "canonical physical JSON")
            if trace_runtime is not None:
                _producer_capture_physical_projection(
                    trace_runtime, path, before=before, after=after,
                    path_after=path_after, raw=immutable_raw, reason=None)
            return value, {"bytes": len(raw), "sha256": sha_bytes(immutable_raw),
                           "device": before.st_dev, "inode": before.st_ino,
                           "links": before.st_nlink, "mtime_ns": before.st_mtime_ns}
        except (ProtocolStop, InputStop) as exc:
            if trace_runtime is not None:
                _producer_capture_physical_projection(
                    trace_runtime, path, before=before, after=after,
                    path_after=path_after, raw=bytes(raw) or None,
                    reason=str(exc))
            raise
    finally:
        os.close(fd)
        if trace_runtime is not None:
            trace_runtime["_last_owner_disposed"] = True


def canonical_reader_mutation_selftest(p0: dict[str, Any], fixture: dict[str, Any],
                                       meter: Meter) -> list[dict[str, Any]]:
    """Route four noncanonical byte encodings through the ordinary reader."""
    contract = fixture.get("canonical_reader_mutations")
    require(type(contract) is list and len(contract) == 4,
            "canonical reader mutation contract")
    baselines = (("P0", p0), ("fixture", fixture))
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="r07-v12c-canonical-") as directory:
        root = Path(directory)
        for owner_name, owner in baselines:
            base = canonical(owner) + b"\n"
            reversed_owner = {key: owner[key] for key in reversed(list(owner))}
            variants = {
                "whitespace_prefix": b" " + base,
                "top_level_key_order": json.dumps(
                    reversed_owner, sort_keys=False, separators=(",", ":"),
                    ensure_ascii=True).encode("ascii") + b"\n",
                "extra_newline": base + b"\n",
                "noncanonical_ascii_escape": base.replace(b"/", b"\\/", 1),
            }
            require(set(variants) == {row["id"] for row in contract},
                    "canonical reader mutation ids")
            for ordinal, expected in enumerate(contract):
                meter.check("canonical_reader_mutation")
                raw = variants[expected["id"]]
                path = root / f"{owner_name}-{ordinal:02d}.json"
                try:
                    with path.open("xb") as stream:
                        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
                    try:
                        read_bounded_json(path, len(raw), meter)
                    except ProtocolStop as exc:
                        reason = str(exc)
                    else:
                        raise ProtocolStop("MUTATION_ACCEPTED:canonical:" +
                                           expected["id"])
                finally:
                    try: path.unlink()
                    except FileNotFoundError: pass
                require(reason == expected["first_reason"],
                        "canonical reader first reason:" + expected["id"])
                rows.append({"owner": owner_name, "id": expected["id"],
                    "before_sha256": sha_bytes(base),
                    "after_sha256": sha_bytes(raw), "first_reason": reason,
                    "owner_disposed": not path.exists()})
    return rows


class BoundedDeltaColumns(list[Any]):
    """List-compatible sparse overlay without copying the 2,896-row roster."""
    def __init__(self, baseline: list[Any], replacements: dict[int, Any]) -> None:
        super().__init__()
        self.baseline = baseline; self.replacements = replacements

    def __len__(self) -> int:
        return len(self.baseline)

    def __getitem__(self, index: Any) -> Any:
        if isinstance(index, slice):
            return [self[position] for position in range(*index.indices(len(self)))]
        position = int(index)
        if position < 0: position += len(self)
        return self.replacements.get(position, self.baseline[position])

    def __iter__(self) -> Any:
        for index in range(len(self.baseline)):
            yield self.replacements.get(index, self.baseline[index])


class TriangularDeltaFrame(dict[str, Any]):
    def __init__(self, baseline: dict[str, Any], case_id: str,
                 replacement_indices: Sequence[int], meter: Meter) -> None:
        require(type(baseline) is dict and
                type(baseline.get("self_digest")) is str and
                type(baseline.get("columns")) is list,
                "authenticated triangular baseline")
        super().__init__(baseline)
        self._baseline = baseline; self._case_id = str(case_id)
        self._baseline_digest = str(baseline["self_digest"])
        replacements: dict[int, Any] = {}
        for index in replacement_indices:
            record = dict(baseline["columns"][index])
            record["sparse_row"] = [list(item) for item in record["sparse_row"]]
            record["pivot_ancestry"] = [list(item) for item in
                                         record["pivot_ancestry"]]
            replacements[int(index)] = record
        self["columns"] = BoundedDeltaColumns(baseline["columns"], replacements)
        self._replacements = replacements
        self._delta_payload: dict[str, Any] | None = None
        meter.check("triangular_delta_construct")

    def freeze_delta(self) -> None:
        self._delta_payload = seal({"schema": SCHEMA + "/bounded-owner-delta/v1",
            "group": "triangular", "id": self._case_id,
            "baseline_self_digest": self._baseline["self_digest"],
            "mutable_roots": ["columns"],
            "owners": {str(index): self._replacements[index]
                       for index in sorted(self._replacements)}})

    def physical_delta(self) -> dict[str, Any]:
        require(type(self._delta_payload) is dict,
                "triangular delta must be frozen")
        return self._delta_payload

    def validate_delta(self) -> None:
        validate_seal(self.physical_delta())
        require(self._baseline.get("self_digest") == self._baseline_digest and
                self.physical_delta().get("baseline_self_digest") ==
                    self._baseline_digest and
                self.physical_delta().get("owners") == {
            str(index): self._replacements[index]
            for index in sorted(self._replacements)},
            "triangular bounded delta binding")


def _triangular_subset_frame(old_value: dict[str, Any], live: Any) -> dict[str, Any]:
    # Borrow the once-parsed authenticated roster.  The ordinary validator
    # replays every row; no second 2,896-column DOM is constructed or retained.
    records = old_value["columns"]
    return seal({"schema": SCHEMA + "/triangular-physical-frame",
            "columns": records, "P_rows_sha256": OLD_PIVOT_ROWS_SHA256})


def _validate_triangular_subset(frame: dict[str, Any], live: Any,
                                trace_runtime: dict[str, Any] | None = None) -> None:
    _producer_validator_event(trace_runtime, "_validate_triangular_subset",
                              "triangular", "old.columns")
    require(set(frame) == {"schema", "columns", "P_rows_sha256", "self_digest"} and
            frame.get("schema") == SCHEMA + "/triangular-physical-frame" and
            isinstance(frame.get("columns"), list) and len(frame["columns"]) > 0,
            "triangular selftest frame")
    validate_seal(frame)
    _producer_validator_event(trace_runtime, "_validate_triangular_subset",
                              "full_P_equation", "old.columns")
    raw_rows = []
    pivots = []
    pivot_set = set()
    for expected, record in enumerate(frame["columns"], 1):
        if (expected & 63) == 1 and trace_runtime is not None and \
                trace_runtime.get("meter") is not None:
            trace_runtime["meter"].check("triangular_row_validation")
        _producer_validator_event(trace_runtime, "_validate_triangular_subset",
                                  "full_P_equation", "old.columns.ancestry")
        validate_provenance(record, expected)
        row = live.parse_sparse(record["sparse_row"])
        require(record["sparse_row_sha256"] == live.sha_obj(record["sparse_row"]),
                "triangular selftest raw digest")
        raw_rows.append(row)
        ancestry = record["pivot_ancestry"]
        require(all(type(item) is list and len(item) == 2 and item[1] in (1, 2)
                    for item in ancestry) and
                [item[0] for item in ancestry] == sorted(set(item[0] for item in ancestry)) and
                all(1 <= item[0] <= expected for item in ancestry) and
                any(item[0] == expected and item[1] in (1, 2) for item in ancestry),
                "triangular selftest ancestry")
        pivot = bytes.fromhex(record["pivot_hex"])
        _producer_validator_event(trace_runtime, "_validate_triangular_subset",
                                  "pivot_identity", "old.columns.pivot")
        require(pivot and pivot not in pivot_set, "triangular selftest pivot identity")
        pivots.append(pivot)
        pivot_set.add(pivot)
    products = []
    seen_pivots: set[bytes] = set()
    for expected, (record, pivot) in enumerate(zip(frame["columns"], pivots), 1):
        if (expected & 63) == 1 and trace_runtime is not None and \
                trace_runtime.get("meter") is not None:
            trace_runtime["meter"].check("triangular_product_validation")
        product: dict[bytes, int] = {}
        for index, coefficient in record["pivot_ancestry"]:
            live.add_scaled(product, raw_rows[index - 1], coefficient)
        _producer_validator_event(trace_runtime, "_validate_triangular_subset",
                                  "full_P_equation", "old.columns.product")
        require(product and min(product) == pivot and product[pivot] == 1 and
                all(key not in seen_pivots for key in product),
                "triangular selftest P equation")
        products.append(live.public_sparse(product))
        seen_pivots.add(pivot)
    require(frame.get("P_rows_sha256") == live.sha_obj(products),
            "triangular selftest full P digest")


def triangular_mutation_selftest(old_value: dict[str, Any], live: Any,
                                 names: Sequence[str],
                                 contract: Sequence[dict[str, Any]] | None = None,
                                 owner_frame: dict[str, Any] | None = None,
                                 meter: Meter | None = None
                                 ) -> list[dict[str, Any]]:
    baseline = owner_frame if owner_frame is not None else \
        _triangular_subset_frame(old_value, live)
    require(meter is not None, "triangular mutation meter")
    trace_runtime: dict[str, Any] = {"meter": meter}
    _validate_triangular_subset(baseline, live, trace_runtime)
    results: list[dict[str, Any]] = []
    before_digest = str(baseline["self_digest"])
    replacement_index = {
        "future_ancestry_index": 1, "zero_diagonal": 1,
        "changed_raw_sparse_entry": 0, "changed_ancestry_coefficient": 1,
        "duplicate_pivot": 1, "wrong_pivot": 2,
        "hidden_smaller_pivot": 2, "skipped_P_equation": 2}
    with tempfile.TemporaryDirectory(prefix="r07-v12c-triangular-") as directory:
        root = Path(directory)
        for ordinal, name in enumerate(names):
            meter.check("triangular_mutation_delta")
            require(name in replacement_index, "unknown triangular mutation")
            value = TriangularDeltaFrame(
                baseline, name, (replacement_index[name],), meter)
            columns = value["columns"]
            if name == "future_ancestry_index":
                columns[1]["pivot_ancestry"].append([7, 1])
            elif name == "zero_diagonal":
                columns[1]["pivot_ancestry"] = [row for row in
                    columns[1]["pivot_ancestry"] if row[0] != 2]
            elif name == "changed_raw_sparse_entry":
                columns[0]["sparse_row"][0][1] = 3 - columns[0]["sparse_row"][0][1]
                columns[0]["sparse_row_sha256"] = live.sha_obj(
                    columns[0]["sparse_row"])
            elif name == "changed_ancestry_coefficient":
                columns[1]["pivot_ancestry"][0][1] = 3 - \
                    columns[1]["pivot_ancestry"][0][1]
            elif name == "duplicate_pivot":
                columns[1]["pivot_hex"] = baseline["columns"][0]["pivot_hex"]
            elif name == "wrong_pivot":
                columns[2]["pivot_hex"] = "00"
            elif name == "hidden_smaller_pivot":
                columns[2]["pivot_hex"] = columns[2]["sparse_row"][-1][0]
            elif name == "skipped_P_equation":
                index = next(index for index, row in enumerate(
                    columns[2]["pivot_ancestry"]) if row[0] != 3)
                columns[2]["pivot_ancestry"].pop(index)
            expected = (contract[ordinal] if contract is not None else
                        {"owner_path": "old.columns",
                         "validator": "_validate_triangular_subset",
                         "stage": "full_P_equation", "reseal": True,
                         "first_reason": "triangular selftest ancestry"})
            trace_runtime["_active_validator_events"] = []
            before, after, reason = _producer_mutation_trace(
                root / f"{ordinal:02d}.json", value,
                lambda candidate: _validate_triangular_subset(
                    candidate, live, trace_runtime),
                trace_runtime=trace_runtime)
            require(reason == expected["first_reason"],
                    "triangular first reason:" + name + ":" + reason)
            require(before != after, "triangular mutation identity unchanged:" + name)
            events = trace_runtime.get("_active_validator_events", [])
            require(events and all(type(event) is dict for event in events),
                    "triangular validator event trace")
            rejection_event = events[-1]
            terminal_count = int(trace_runtime.get("_terminal_count", 0))
            owner_disposed = bool(trace_runtime.get("_last_owner_disposed"))
            require(terminal_count == 1 and owner_disposed,
                    "triangular measured terminal/owner:" + name)
            results.append({"id": name, "group": "triangular",
                "owner_path": expected["owner_path"],
                "identity_kind": "bounded_owner_delta",
                "before_identity": {"kind": "immutable_baseline",
                                    "sha256": before_digest},
                "after_identity": {"kind": "physical_delta", "sha256": after},
                "physical_digest": after, "event_trace": list(events),
                "event_trace_digest": sha_obj(events),
                "entered_validators": [event["validator"] for event in events],
                "first_rejection": {"validator": rejection_event["validator"],
                    "stage": rejection_event["stage"], "narrow_reason": reason},
                "baseline_revalidated": True, "terminal_count": terminal_count,
                "owner_disposed": owner_disposed,
                "validator": rejection_event["validator"],
                "stage": rejection_event["stage"],
                "reseal": expected["reseal"], "before_sha256": before,
                "after_sha256": after,
                "reached_validator": rejection_event["validator"],
                "first_reason": reason})
    require(str(baseline["self_digest"]) == before_digest and
            baseline["columns"] is old_value["columns"],
            "triangular immutable baseline restoration")
    return results
def producer_bind_section_identity(runtime: dict[str, Any],
                                   section: dict[str, Any],
                                   candidate: dict[str, Any]) -> dict[str, Any]:
    """SELFTEST-only section binder over the already built literal owners.

    This is intentionally a plain SELFTEST helper over authenticated owners;
    no production search or resume object is exposed.
    """
    qid, gid = int(candidate["q0_state_id"]), int(candidate["gamma_state_id"])
    require(1 <= qid <= len(runtime["qstates"]) and
            1 <= gid <= len(runtime["gamma"].states),
            "section state id")
    qstate = runtime["qstates"][qid - 1]
    gamma_state = runtime["gamma"].states[gid - 1]
    p176 = runtime["p176"]
    qword = list(p176.q0_section_word(qid - 1, runtime["parents"],
                                      runtime["letters"]))
    gword = list(runtime["gamma"].section_word(gid - 1))
    base_word = runtime["live"].reduce_word(gword + qword)
    q0_row = p176.section_row(runtime["stores"], qid - 1)
    coordinate = int(candidate.get("coordinate", 0))
    require(0 <= coordinate < 10, "section coordinate")
    q3_rows = runtime["q3_literal_owner"]["literal_rows"]
    coordinate_mark = runtime["coordinate_marks"][coordinate]
    selected_coordinate_mark = [p176.packed_joint_blob(
        value, "v12c selected coordinate mark") for value in coordinate_mark]
    gamma_parent = runtime["gamma"].parent[gid - 1]
    gamma_generator = runtime["gamma"].parent_generator[gid - 1]
    gamma_parent_record = [0 if gamma_parent is None else gamma_parent + 1,
                           0 if gamma_generator is None else gamma_generator + 1]
    gamma_projected = b"".join(p176.packed_joint_blob(
        value, "v10 projected Gamma coordinate")
        for value in runtime["projected"][gid - 1])
    fibres = runtime["fibres"]
    coarse = fibres.coarse_indices.get(coordinate)
    kernel_states = fibres.kernel_states.get(coordinate, [])
    require(type(candidate.get("kernel_word")) is list and
            type(candidate.get("kernel_cursor")) is int,
            "explicit selected kernel owner")
    selected_kernel_word = list(candidate["kernel_word"])
    matched_kernel_cursor = next((index for index, state in enumerate(kernel_states)
        if state.get("source_word") == selected_kernel_word), None)
    require(matched_kernel_cursor is not None and
            matched_kernel_cursor == candidate["kernel_cursor"],
            "explicit selected kernel cursor")
    kernel_cursor = int(matched_kernel_cursor)
    kernel_generators = fibres._kernel_generators(coordinate)
    kernel_state_words = [list(state.get("source_word", []))
                          for state in kernel_states]
    kernel_state_blobs = [b"".join(bytes(blob) for blob in state[
        "coordinate_blobs"]).hex() for state in kernel_states]
    kernel_state_parents: list[int | None] = []
    kernel_state_generators: list[int | None] = []
    for state_index, state_word in enumerate(kernel_state_words):
        if state_index == 0:
            kernel_state_parents.append(None)
            kernel_state_generators.append(None)
            continue
        found: tuple[int, int] | None = None
        for parent_index, parent_word in enumerate(kernel_state_words[:state_index]):
            for generator_index, generator in enumerate(kernel_generators):
                if runtime["live"].reduce_word(parent_word + generator) == state_word:
                    found = (parent_index, generator_index)
                    break
            if found is not None:
                break
        require(found is not None, "kernel BFS parent/generator owner")
        kernel_state_parents.append(found[0])
        kernel_state_generators.append(found[1])
    gamma_first: dict[bytes, int] = {}
    gamma_offset = 40 * min(coordinate, 5) + 154 * max(0, coordinate - 5)
    gamma_width = 40 if coordinate < 5 else 154
    for gamma_id, projected_row in enumerate(runtime["projected"], 1):
        packed = b"".join(p176.packed_joint_blob(
            value, "v12c Gamma projected coordinate") for value in projected_row)
        gamma_first.setdefault(packed[gamma_offset:gamma_offset + gamma_width],
                               gamma_id)
    gamma_values = sorted(key.hex() for key in gamma_first)
    gamma_first_pairs_sha256 = sha_obj(sorted(
        (key.hex(), value) for key, value in gamma_first.items()))
    gamma_literal = [{"coordinate_blobs_hex": [key.hex()],
                      "gamma_state_id": value}
                     for key, value in sorted(gamma_first.items())]
    accepted_A = runtime["A_public"][f"S{coordinate}"]
    require(accepted_A.get("order") == len(gamma_first) and
            accepted_A.get("literal_elements") == gamma_literal and
            accepted_A.get("literal_table_sha256") == sha_obj(gamma_literal),
            "producer exact Gamma/A first-gid table")
    accepted_buckets = runtime["task176_receipt"]["result"][
        "typed_singleton_images"]["raw_section_coarse_key_bucket_statistics"][
            coordinate]
    require(coarse is not None and coarse.build_count == 1 and
            coarse.bucket_public() == accepted_buckets,
            "producer accepted singleton coarse buckets")
    gamma_full = producer_full_gamma_diagnostic(runtime, gamma_state)
    require("selected_full_gamma" not in runtime,
            "producer selected full Gamma constructed twice")
    runtime["selected_full_gamma"] = gamma_full
    runtime["selected_full_gamma_state_id"] = gid
    parent_letter_digest = producer_parent_letter_stream_digest(
        runtime["parents"], runtime["letters"], runtime["meter"])
    require("q0_parent_letter_digest" not in runtime,
            "producer parent-letter digest constructed twice")
    runtime["q0_parent_letter_digest"] = parent_letter_digest
    result = dict(section)
    result.update({"q0_state_hex": bytes(qstate).hex(),
        "q0_state_sha256": sha_bytes(bytes(qstate)),
        "q0_parent_state_id": int(runtime["parents"][qid - 1]),
        "q0_parent_letter": int(runtime["letters"][qid - 1]),
        "selected_marked_generator_row": list(q3_rows[0]),
        "least_q0_state_id": qid,
        "selected_q0_word": qword, "selected_gamma_word": gword,
        "selected_base_word": base_word,
        "coarse_inverse_entries": coarse.state_count,
        "coarse_inverse_digest": sha_obj(coarse.public()),
        "coarse_inverse_pairs_sha256": coarse.public_digest(),
        "coarse_bucket_statistics": coarse.bucket_public(),
        "k0_build_count": coarse.build_count,
        "k0_state_digest": coarse.state_digest(),
        "k0_slot_digest": coarse.slot_digest(),
        "gamma_distinct_values": len(gamma_values),
        "gamma_distinct_values_sha256": sha_obj(gamma_values),
        "gamma_first_gid_pairs_sha256": gamma_first_pairs_sha256,
        "gamma_A_order": len(gamma_first),
        "gamma_A_literal_table_sha256": sha_obj(gamma_literal),
        "kernel_generators": kernel_generators,
        "kernel_generators_sha256": sha_obj(kernel_generators),
        "kernel_order": len(kernel_states), "kernel_cursor": kernel_cursor,
        "kernel_state_word": selected_kernel_word,
        "kernel_state_words": kernel_state_words,
        "kernel_state_blobs": kernel_state_blobs,
        "kernel_state_parents": kernel_state_parents,
        "kernel_state_generators": kernel_state_generators,
        "kernel_state_blob_digest": sha_obj(kernel_state_blobs),
        "kernel_state_word_digest": sha_obj(kernel_state_words),
        "kernel_state_roster_digest": sha_obj(list(zip(
            kernel_state_parents, kernel_state_generators,
            kernel_state_words, kernel_state_blobs))),
        "kernel_state_blob": kernel_state_blobs[kernel_cursor],
        "q0_ten_coordinate_blobs_hex": [bytes(value).hex() for value in q0_row],
        "q0_parent_letter_digest": parent_letter_digest,
        "q3_marked_permutation_rows": q3_rows,
        "selected_coordinate_mark_hex": [value.hex()
                                          for value in selected_coordinate_mark],
        "gamma_parent_record": gamma_parent_record,
        "gamma_parent_state_id": gamma_parent_record[0],
        "gamma_parent_record_id": gamma_parent_record[1],
        "gamma_projected_ten_state_hex": gamma_projected.hex(),
        "gamma_projected_ten_state_sha256": sha_bytes(gamma_projected),
        "gamma_full_state_codec": "jointgroup-E3-plus-31-E4/v1",
        "gamma_full_state_factor_widths": [40] + [154] * 31,
        "gamma_full_state_hex": gamma_full.hex(),
        "gamma_full_state_sha256": sha_bytes(gamma_full),
        "membership_bound": True,
        "schedule_relation": "qid/gid/current-dual/fibre-bound"})
    return result


def _producer_recovery_public(registry: SourceRegistry) -> dict[str, Any]:
    recovery_v1 = registry.json("task176_recovery")
    recovery_v2 = registry.json("task176_recovery_v2")
    return {"v1": {"path": SOURCE_PINS["task176_recovery"][0],
                    "bytes": SOURCE_PINS["task176_recovery"][1],
                    "sha256": SOURCE_PINS["task176_recovery"][2],
                    "self_digest_sha256": recovery_v1.get("self_digest_sha256")},
            "v2": {"path": SOURCE_PINS["task176_recovery_v2"][0],
                    "bytes": SOURCE_PINS["task176_recovery_v2"][1],
                    "sha256": SOURCE_PINS["task176_recovery_v2"][2],
                    "self_digest_sha256": recovery_v2.get("self_digest_sha256"),
                    "correction": recovery_v2.get("correction")}}


def producer_validate_correction(runtime: dict[str, Any], record: dict[str, Any],
                                 recovery: dict[str, Any]) -> None:
    """Producer's ordinary selected-correction validator, independently written."""
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "correction", "selected.record.provenance")
    model = runtime["model"]; provenance = record.get("provenance")
    require(type(provenance) is dict and provenance.get("family") == "correction",
            "selected correction provenance")
    roster_index = int(provenance.get("roster_index"))
    require(1 <= roster_index <= len(runtime["roster"]),
            "correction roster index")
    roster = runtime["roster"][roster_index - 1]
    require(provenance.get("relator_word") == roster["word"] and
            provenance.get("layer") == roster["layer"] and
            int(provenance.get("ordinal")) == int(roster["ordinal"]),
            "correction literal roster")
    row, replay = model.direct_column(provenance["delta_word"],
                                      provenance["relator_word"])
    for key in ("delta_word", "relator_word", "conjugate_word", "corrected_word",
                "quotient_value_blobs", "eleven_occurrence_replay",
                "direct_all_seven_replay"):
        if key == "conjugate_word":
            _producer_validator_event(runtime, "validate_correction_provenance",
                                      "coefficient_two_inverse",
                                      "selected.provenance.conjugate_word")
        require(provenance.get(key) == replay.get(key),
                "correction replay field:" + key)
    public_row = producer_public_sparse(row)
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "row_replay", "selected.record.sparse_row")
    require(public_row == record.get("sparse_row") and
            record.get("sparse_row_sha256") == sha_obj(public_row),
            "selected correction stored row")
    dual = producer_parse_sparse(record.get("active_dual"))
    scalar = producer_pair(dual, row)
    require(record.get("active_dual_sha256") == sha_obj(record["active_dual"]) and
            record.get("dual_pairing") == scalar in (1, 2),
            "correction ACTIVE scalar")
    formula = model.occurrence_data(provenance["relator_word"], dual)
    support = runtime["fibres"].weighted_support(formula)
    require(provenance.get("weighted_formula") == formula["public"] and
            provenance.get("support_hitting") == support,
            "correction independent weighted formula")
    coordinates = model.coordinates(provenance["delta_word"])
    require(provenance.get("delta_coordinate_blobs_hex") ==
            [raw.hex() for raw in coordinates], "correction ten coordinates")
    section = provenance.get("section_provenance")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Q0_replay", "selected.section.q0_state")
    require(type(section) is dict and section.get("membership_bound") is True and
            section.get("schedule_relation") == "qid/gid/current-dual/fibre-bound" and
            section.get("q0_state_sha256") == sha_bytes(
                bytes.fromhex(section["q0_state_hex"])) and
            type(section.get("gamma_full_state_hex")) is str and
            type(section.get("gamma_full_state_sha256")) is str,
            "correction reconstructed Q0/Gamma identity")
    qid = int(section.get("q0_state_id")); gid = int(section.get("gamma_state_id"))
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "K0_owner", "selected.section.state_ids")
    require(1 <= qid <= len(runtime["qstates"]) and
            1 <= gid <= len(runtime["gamma"].states) and
            section.get("q0_state_hex") == bytes(runtime["qstates"][qid - 1]).hex(),
            "producer correction state bounds")
    p176 = runtime["p176"]
    replay_cache = runtime.setdefault("_selected_replay_cache", {})
    cache_key = (qid, gid)
    require(cache_key in replay_cache or len(replay_cache) < 8,
            "producer selected replay cache cap")
    if cache_key not in replay_cache:
        replay_cache[cache_key] = (
            list(p176.q0_section_word(qid - 1, runtime["parents"],
                                      runtime["letters"])),
            list(runtime["gamma"].section_word(gid - 1)),
            p176.section_row(runtime["stores"], qid - 1),
            b"".join(p176.packed_joint_blob(
                value, "producer projected Gamma owner")
                for value in runtime["projected"][gid - 1]))
    qword, gword, q0_row, gamma_projected = replay_cache[cache_key]
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Q0_parent", "selected.section.q0_parent")
    require(section.get("q0_ten_coordinate_blobs_hex") ==
            [bytes(value).hex() for value in q0_row] and
            section.get("q0_parent_state_id") == int(runtime["parents"][qid - 1]) and
            section.get("q0_parent_letter") == int(runtime["letters"][qid - 1]),
            "correction Q0 parent-record owner")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Gamma_replay", "selected.section.gamma_projected")
    require(type(section.get("gamma_projected_ten_state_hex")) is str and
            section.get("gamma_projected_ten_state_sha256") == sha_bytes(
                bytes.fromhex(section["gamma_projected_ten_state_hex"])),
            "task176 selected independent Q0/Gamma replay")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "K0_owner", "selected.section.gamma_state_id")
    require(section.get("gamma_projected_ten_state_hex") == gamma_projected.hex(),
            "task176 selected independent Q0/Gamma replay")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Gamma_970", "selected.section.gamma_projected_digest")
    require(section.get("gamma_projected_ten_state_sha256") ==
            sha_bytes(gamma_projected), "task176 selected independent Q0/Gamma replay")
    require(runtime.get("selected_full_gamma_state_id") == gid and
            type(runtime.get("selected_full_gamma")) is bytes,
            "producer selected full Gamma immutable owner")
    gamma_full = runtime["selected_full_gamma"]
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Gamma_full_diagnostic", "selected.section.gamma_full")
    require(section.get("gamma_full_state_codec") ==
                "jointgroup-E3-plus-31-E4/v1" and
            section.get("gamma_full_state_factor_widths") ==
                [40] + [154] * 31 and len(gamma_full) == 4814 and
            section.get("gamma_full_state_hex") == gamma_full.hex() and
            section.get("gamma_full_state_sha256") == sha_bytes(gamma_full),
            "correction reconstructed Q0/Gamma identity")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Q0_word", "selected.section.q0_word")
    require(section.get("selected_q0_word") == qword,
            "task176 selected parent-word binding")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Gamma_word", "selected.section.gamma_word")
    require(section.get("selected_gamma_word") == gword,
            "task176 selected parent-word binding")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "base_word", "selected.section.base_word")
    require(section.get("selected_base_word") == producer_reduce_word(gword + qword),
            "selected Q0/Gamma/base word binding")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Q3_mark", "selected.section.marked_generator")
    require(section.get("selected_marked_generator_row") ==
            runtime["q3_literal_owner"]["literal_rows"][0],
            "task176 selected typed marked-generator replay")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Q3_owner", "selected.section.marked_permutations")
    require(section.get("q3_marked_permutation_rows") ==
            runtime["q3_literal_owner"]["literal_rows"],
            "correction Q3 marked-permutation owner")
    coordinate = int(section.get("coordinate"))
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "coordinate_mark", "selected.section.coordinate_mark")
    require(0 <= coordinate < 10 and
            section.get("selected_coordinate_mark_hex") == [
                p176.packed_joint_blob(value, "producer coordinate mark").hex()
                for value in runtime["coordinate_marks"][coordinate]],
            "correction coordinate mark owner")
    gamma_parent = runtime["gamma"].parent[gid - 1]
    gamma_generator = runtime["gamma"].parent_generator[gid - 1]
    expected_gamma_parent = 0 if gamma_parent is None else gamma_parent + 1
    expected_gamma_record = 0 if gamma_generator is None else gamma_generator + 1
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Gamma_parent", "selected.section.gamma_parent")
    require(section.get("gamma_parent_state_id") == expected_gamma_parent,
            "correction Gamma parent-record owner")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Gamma_parent_record", "selected.section.gamma_record")
    require(section.get("gamma_parent_record_id") == expected_gamma_record and
            section.get("gamma_parent_record") == [expected_gamma_parent,
                                                     expected_gamma_record],
            "correction Gamma parent-record owner")
    _producer_validator_event(runtime, "validate_correction_provenance",
                              "Q0_parent_roster", "selected.section.q0_parent_roster")
    require(section.get("q0_parent_letter_digest") ==
            runtime.get("q0_parent_letter_digest"),
        "correction Q0 parent-letter owner")
    require(provenance.get("recovery_v1") == recovery["v1"] and
            provenance.get("recovery_v2") == recovery["v2"],
            "correction recovery-v2 identity")
    if support["K"] == 0:
        target = bytes.fromhex(str(section.get("target_hex")))
        require(coordinates[coordinate] == target and
                provenance.get("schedule") == "weighted_support_fibre_complete",
                "correction K0 support fibre")
        store = runtime["fibres"]._coarse_index(coordinate)
        _producer_validator_event(runtime, "validate_correction_provenance",
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
        first_gid: dict[bytes, int] = {}
        offset = 40 * min(coordinate, 5) + 154 * max(0, coordinate - 5)
        width = 40 if coordinate < 5 else 154
        for gamma_id, projected_row in enumerate(runtime["projected"], 1):
            packed = b"".join(p176.packed_joint_blob(
                value, "producer Gamma coordinate owner") for value in projected_row)
            first_gid.setdefault(packed[offset:offset + width], gamma_id)
        amap = runtime["A_maps"][f"S{coordinate}"]
        require(set(first_gid) == {key[0] for key in amap},
                    "K0 Gamma/A-family literal equality")
        literal = [{"coordinate_blobs_hex": [key.hex()],
                    "gamma_state_id": gamma_id}
                   for key, gamma_id in sorted(first_gid.items())]
        accepted_A = runtime["A_public"][f"S{coordinate}"]
        require(accepted_A.get("order") == len(first_gid) and
                accepted_A.get("literal_elements") == literal and
                accepted_A.get("literal_table_sha256") == sha_obj(literal) and
                section.get("gamma_A_order") == len(first_gid) and
                section.get("gamma_A_literal_table_sha256") == sha_obj(literal),
                "K0 exact Gamma/A first-gid table")
        require(section.get("gamma_first_gid_pairs_sha256") == sha_obj(sorted(
            (key.hex(), gid0) for key, gid0 in first_gid.items())),
            "K0 Gamma first-gid owner")
        candidates: list[tuple[int, int]] = []
        target_value = target
        quotient = runtime["e3"] if coordinate < 5 else runtime["e4"]
        for (a,), gid0 in amap.items():
            needed = p176.multiply_blob(p176.inverse_blob(
                a, coordinate, runtime["e3"], runtime["e4"]), target_value,
                coordinate, runtime["e3"], runtime["e4"])
            qid0 = store.lookup_full(needed)
            if qid0 is None:
                continue
            retained = p176.section_row(runtime["stores"], qid0)
            require(store._state(qid0) == needed and
                    retained[coordinate] == needed,
                    "producer K0 retained full state")
            require(p176.multiply_blob(a, retained[coordinate], coordinate,
                                       runtime["e3"], runtime["e4"]) == target_value,
                    "producer K0 target product")
            candidates.append((qid0 + 1, gid0 + 1))
        require(candidates, "producer K0 candidate owner")
        least = min(candidates)
        _producer_validator_event(runtime, "validate_correction_provenance",
                                  "least_base", "selected.section.least_q0_state_id")
        require(candidates and section.get("least_q0_state_id") == least[0] and
                (qid, gid) == least,
                "K0 lexicographically least base")
        states = runtime["fibres"].kernel_states[coordinate]
        kernel_generators = runtime["fibres"]._kernel_generators(coordinate)
        expected_blobs = [b"".join(bytes(blob) for blob in state[
            "coordinate_blobs"]).hex() for state in states]
        expected_words = [list(state["source_word"]) for state in states]
        expected_parents: list[int | None] = []
        expected_generators: list[int | None] = []
        for state_index, state_word in enumerate(expected_words):
            if state_index == 0:
                expected_parents.append(None); expected_generators.append(None)
                continue
            found: tuple[int, int] | None = None
            for parent_index, parent_word in enumerate(expected_words[:state_index]):
                for generator_index, generator in enumerate(kernel_generators):
                    if producer_reduce_word(parent_word + generator) == state_word:
                        found = (parent_index, generator_index); break
                if found is not None: break
            require(found is not None, "producer kernel BFS parent/generator owner")
            expected_parents.append(found[0]); expected_generators.append(found[1])
        _producer_validator_event(runtime, "validate_correction_provenance",
                                  "kernel_roster", "selected.section.kernel_generators")
        require(section.get("kernel_generators") == kernel_generators and
                section.get("kernel_generators_sha256") == sha_obj(kernel_generators),
                "K0 authenticated kernel generator binding")
        cursor = int(section.get("kernel_cursor"))
        _producer_validator_event(runtime, "validate_correction_provenance",
                                  "kernel_BFS", "selected.section.kernel_state_roster")
        require(0 <= cursor < len(states) and
                section.get("kernel_order") == KERNEL_ORDERS[coordinate] and
                section.get("kernel_state_blobs") == expected_blobs and
                section.get("kernel_state_words") == expected_words and
                section.get("kernel_state_parents") == expected_parents and
                section.get("kernel_state_generators") == expected_generators and
                section.get("kernel_state_blob_digest") == sha_obj(expected_blobs) and
                section.get("kernel_state_word_digest") == sha_obj(expected_words) and
                section.get("kernel_state_roster_digest") == sha_obj(list(zip(
                    expected_parents, expected_generators, expected_words,
                    expected_blobs))) and
                section.get("kernel_state_blob") == expected_blobs[cursor] and
                section.get("kernel_state_word") == expected_words[cursor],
                "producer kernel BFS owner")
        _producer_validator_event(runtime, "validate_correction_provenance",
                                  "product_order", "selected.section.product")
        require(provenance.get("delta_word") == producer_reduce_word(
            list(section["kernel_word"]) + gword + qword),
            "K0 kernel+Gamma+Q0 product order")
    else:
        require(provenance.get("delta_word") == producer_reduce_word(gword + qword),
                "producer nonzero Gamma+Q0 product order")


def _producer_correction_selftest_frame(runtime: dict[str, Any],
                                        reducer: FormalReducer,
                                        registry: SourceRegistry) -> dict[str, Any]:
    """Select the first physical correction hit by the actual current dual."""
    live = runtime["live"]; p176 = runtime["p176"]
    recovery = _producer_recovery_public(registry)
    dual = dict(runtime["current_dual_private"])
    remainder = dict(runtime["target_remainder_private"])
    target = dict(runtime["target"])
    rank_before = len(reducer.order)
    require(rank_before == EXPECTED_TRIANGULAR["rank"] and
            all(live.pair(dual, reducer.rows[pivot]) == 0
                for pivot in reducer.order),
            "actual current dual annihilates chronological basis")
    target_pairing = live.pair(dual, target)
    remainder_pairing = live.pair(dual, remainder)
    require(target_pairing in (1, 2) and
            target_pairing == remainder_pairing,
            "actual current dual target/remainder pairing")
    formal_solution = [[key, value] for key, value in sorted(
        reducer.expand(runtime["target_solution_node"]).items())]
    current_epoch = {
        "rank_before": rank_before,
        "chronological_pivot_order_sha256": sha_obj(
            [pivot.hex() for pivot in reducer.order]),
        "chronological_basis_sha256": sha_obj(
            [live.public_sparse(reducer.rows[pivot]) for pivot in reducer.order]),
        "current_dual": live.public_sparse(dual),
        "current_dual_sha256": live.sha_obj(live.public_sparse(dual)),
        "basis_annihilation": True,
        "target": live.public_sparse(target),
        "target_pairing": target_pairing,
        "remainder": live.public_sparse(remainder),
        "remainder_pairing": remainder_pairing,
        "formal_solution": formal_solution,
        "formal_solution_sha256": sha_obj(formal_solution),
    }
    for coordinate in range(10):
        runtime["meter"].check("selected_coordinate_roster")
        width = 40 if coordinate < 5 else 154
        for gamma_id in range(1, 244):
            if (gamma_id & 31) == 1:
                runtime["meter"].check("selected_gamma_roster")
            target = p176.packed_joint_blob(
                runtime["projected"][gamma_id - 1][coordinate],
                "producer correction target")
            candidate = runtime["fibres"].canonical(coordinate, target)
            if candidate is None:
                continue
            kernel_states = runtime["fibres"].kernel_states.get(coordinate)
            require(type(kernel_states) is list and kernel_states and
                    type(kernel_states[0].get("source_word")) is list,
                    "producer explicit authenticated kernel identity")
            candidate = dict(candidate)
            candidate["kernel_cursor"] = 0
            candidate["kernel_word"] = list(kernel_states[0]["source_word"])
            for roster_index, roster_row in enumerate(runtime["roster"], 1):
                if (roster_index & 63) == 1:
                    runtime["meter"].check("selected_literal_roster")
                row, replay = runtime["model"].direct_column(
                    candidate["source_word"], roster_row["word"])
                if live.pair(dual, row) not in (1, 2):
                    continue
                formula = runtime["model"].occurrence_data(roster_row["word"], dual)
                support = runtime["fibres"].weighted_support(formula)
                # The selected-correction mutation suite is specifically the
                # finite K=0 owner route.  Do not manufacture a K>0 frame
                # whose section lacks the coarse table, fibre cursor, and
                # kernel witness fields exercised below.
                if support["K"] != 0:
                    continue
                scalar = runtime["model"].formula_scalar(
                    formula, candidate["coordinate_blobs"])
                if scalar not in (1, 2):
                    continue
                section = producer_bind_section_identity(
                    runtime,
                    {key0: value for key0, value in candidate.items()
                     if key0 not in ("source_word", "coordinate_blobs")}, candidate)
                targets = sorted(formula["merged"], key=lambda item: (item[0], item[1]))
                support_index = next((index for index, item in enumerate(targets)
                    if item == (coordinate, target)), None)
                require(support_index is not None, "producer correction support target")
                section.update({"support_fibre_cursor": support_index,
                                "target_hex": target.hex(),
                                "kernel_cursor": int(section["kernel_cursor"])})
                provenance = {"family": "correction", "roster_index": roster_index,
                    "layer": roster_row["layer"], "ordinal": roster_row["ordinal"],
                    "schedule": "weighted_support_fibre_complete",
                    "weighted_formula": formula["public"],
                    "support_hitting": support,
                    "delta_word": list(candidate["source_word"]),
                    "delta_coordinate_blobs_hex": [raw.hex() for raw in
                                                    candidate["coordinate_blobs"]],
                    "section_provenance": section,
                    "recovery_v1": recovery["v1"], "recovery_v2": recovery["v2"],
                    **replay}
                pivot, selected_solution_node = reducer.add_actual(
                    row, "n:selftest")
                rank_after = len(reducer.order)
                require(rank_after == rank_before + 1 and
                        reducer.order[-1] == pivot,
                        "selected actual rank epoch")
                selected_formal_solution = [[key0, value0] for key0, value0 in
                    sorted(reducer.expand(selected_solution_node).items())]
                record = {"symbol": "n:selftest", "family": "correction",
                    "provenance": provenance, "sparse_row": live.public_sparse(row),
                    "sparse_row_sha256": live.sha_obj(live.public_sparse(row)),
                    "active_dual": live.public_sparse(dual),
                    "active_dual_sha256": live.sha_obj(live.public_sparse(dual)),
                    "dual_pairing": live.pair(dual, row),
                    "pivot_hex": pivot.hex(), "rank_before": rank_before,
                    "rank_after": rank_after,
                    "current_epoch": current_epoch,
                    "selected_formal_solution": selected_formal_solution,
                    "selected_formal_solution_sha256": sha_obj(
                        selected_formal_solution),
                    "selected_coordinate": coordinate,
                    "actual_direct_replay": True, "coefficient": 1}
                producer_validate_correction(runtime, record, recovery)
                frame = {"schema": SCHEMA + "/selected-correction-selftest-frame",
                    "record": record, "recovery": recovery,
                    "heavy_input_sha256": runtime["heavy_input_sha256"],
                    "heavy_public": runtime["heavy_public"],
                    "target": record["sparse_row"],
                    "producer_sparse_equality": True,
                    "boundary_preimage": [],
                    "validator": "producer_validate_correction"}
                # Require every owner field before the first mutation is
                # written.  This turns an absent physical owner into an
                # honest stop at the baseline rather than a later KeyError.
                section_owner_fields = {
                    "q0_state_hex", "q0_state_sha256", "q0_state_id",
                    "q0_parent_state_id", "q0_parent_letter",
                    "selected_marked_generator_row", "least_q0_state_id",
                    "q0_ten_coordinate_blobs_hex", "selected_q0_word",
                    "selected_gamma_word", "selected_base_word",
                    "q3_marked_permutation_rows", "selected_coordinate_mark_hex",
                    "selected_marked_generator_row", "gamma_parent_record",
                    "gamma_parent_state_id", "gamma_parent_record_id",
                    "gamma_projected_ten_state_hex",
                    "gamma_projected_ten_state_sha256", "gamma_full_state_hex",
                    "gamma_full_state_sha256", "gamma_full_state_codec",
                    "gamma_full_state_factor_widths",
                    "gamma_first_gid_pairs_sha256", "gamma_A_order",
                    "gamma_A_literal_table_sha256",
                    "gamma_state_id", "coordinate", "target_hex",
                    "support_fibre_cursor", "kernel_cursor", "kernel_word",
                    "kernel_order", "kernel_generators", "kernel_generators_sha256",
                    "kernel_state_words", "kernel_state_blobs", "kernel_state_blob",
                    "coarse_inverse_entries", "coarse_inverse_digest",
                    "coarse_inverse_pairs_sha256", "coarse_bucket_statistics",
                    "k0_build_count",
                    "k0_state_digest", "k0_slot_digest"}
                require(section_owner_fields <=
                        set(provenance["section_provenance"]),
                        "producer selected K0 owner field roster")
                require(frame["record"]["provenance"]["support_hitting"]["K"] == 0,
                        "producer selected K0 baseline")
                return seal(frame)
        runtime["fibres"].release_coordinate(coordinate)
    require(False, "producer selected correction owner unavailable")
    return {}


def producer_selected_statement(record: dict[str, Any]) -> dict[str, Any]:
    """Construct the v296 canonical selected statement from typed owner data."""
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
            "table_capacity": K0_CAPACITY, "width":
                40 if int(section["coordinate"]) < 5 else 154,
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
            "s": record["dual_pairing"], "weighted_formula":
                provenance["weighted_formula"], "support_hitting": support,
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


def producer_final_heavy_identity(runtime: dict[str, Any],
                                  selected_frame: dict[str, Any],
                                  registry: SourceRegistry) -> dict[str, Any]:
    """Build v296/v299 H only after an actual selected K=0 owner exists.

    ``RunPre`` (the large diagnostic ``heavy_public`` object) is deliberately
    not the preselection authority.  The small OwnerPre below is rebuilt from
    the separately authenticated task176 physical chain and is the only
    preselection object admitted to H.
    """
    require(type(runtime.get("p0_identity")) is dict and
            type(runtime.get("p0_sources")) is dict and
            type(runtime.get("p0_frozen_authorities")) is dict,
            "producer final carrier P0 identity")
    owner_pre = runtime.get("owner_preselection")
    require(type(owner_pre) is dict and type(runtime.get(
        "owner_preselection_sha256")) is str,
            "producer OwnerPre authority")
    statement = producer_selected_statement(selected_frame["record"])
    public = {"schema": "r07-a0-final-heavy-carrier/v2",
        "p0": runtime["p0_identity"], "p0_self_digest_sha256":
            runtime["p0_identity"]["self_digest_sha256"],
        "sources": runtime["p0_sources"],
        "frozen_authorities": runtime["p0_frozen_authorities"],
        "algorithms": {"selected_k0":
            "v12c-coarse-open-address-retained-full-state-first-gid-bfs",
            "correction_validator": SCHEMA +
                "/selected-correction-selftest-frame",
            "canonical_json": "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=True)",
            "digest_framing": "sha256(canonical(H))"},
        "preselection_owner": {"public": owner_pre,
                                "sha256": runtime[
                                    "owner_preselection_sha256"]},
        "selected_statement": statement}
    return {"public": public, "sha256": sha_obj(public)}


def _producer_decode_task176_blob(owner: dict[str, Any], raw_limit: int,
                                  label: str, meter: Meter | None = None) -> bytes:
    """Bounded producer-local decoder for each task176 physical blob."""
    require(type(owner) is dict and owner.get("codec") == "zlib+base64" and
            owner.get("raw_bytes") == raw_limit and
            type(owner.get("data")) is str and
            type(owner.get("compressed_bytes")) is int and
            owner["compressed_bytes"] > 0 and
            type(owner.get("compressed_sha256")) is str and
            len(owner["compressed_sha256"]) == 64,
            "producer task176 blob envelope:" + label)
    try:
        compressed = base64.b64decode(owner["data"].encode("ascii"),
                                      validate=True)
    except (ValueError, UnicodeError) as exc:
        raise InputStop("producer task176 base64:" + label) from exc
    require(len(compressed) == owner["compressed_bytes"] and
            base64.b64encode(compressed).decode("ascii") == owner["data"] and
            sha_bytes(compressed) == owner["compressed_sha256"],
            "producer task176 compressed owner:" + label)
    if meter is not None:
        meter.bump("owner_preselection_stream_bytes", raw_limit,
                   "owner_preselection_decode:" + label)
    inflater = zlib.decompressobj()
    try:
        decoded = inflater.decompress(compressed, raw_limit + 1)
    except zlib.error as exc:
        raise InputStop("producer task176 zlib:" + label) from exc
    require(len(decoded) == raw_limit and inflater.eof and
            not inflater.unused_data and not inflater.unconsumed_tail and
            sha_bytes(decoded) == owner.get("raw_sha256"),
            "producer task176 decoded owner:" + label)
    return decoded


def _producer_owner_meta(owner: dict[str, Any], label: str) -> dict[str, Any]:
    """Project a decoded task176 blob to its deterministic owner metadata."""
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
            "producer task176 owner metadata:" + label)
    return {"codec": owner["codec"], "raw_bytes": owner["raw_bytes"],
            "raw_sha256": owner["raw_sha256"],
            "compressed_bytes": owner["compressed_bytes"],
            "compressed_sha256": owner["compressed_sha256"],
            "record_count": owner["record_count"],
            "record_width_bytes": owner["record_width_bytes"]}


def _producer_bind_owner_stream(owner: dict[str, Any],
                                chunks: Iterable[bytes], label: str,
                                meter: Meter | None = None) -> None:
    """Bind a locally materialized owner without making a second blob.

    The task176 decoder has already authenticated the compressed and decoded
    byte stream against ``owner``.  The local stream below is therefore
    compared by its exact fixed-record count, length, and SHA while retaining
    only the current record.  This avoids a contiguous 52--226 MB copy while
    both the decoded authority and the heavy stores are live.
    """
    width = int(owner["record_width_bytes"])
    expected_count = int(owner["record_count"])
    digest = hashlib.sha256()
    total = 0
    count = 0
    for chunk in chunks:
        value = bytes(chunk)
        require(len(value) == width, "producer OwnerPre stream width:" + label)
        digest.update(value)
        total += len(value)
        count += 1
    require(count == expected_count and total == int(owner["raw_bytes"]) and
            total == count * width and digest.hexdigest() == owner["raw_sha256"],
            "producer OwnerPre stream binding:" + label)
    if meter is not None:
        meter.bump("owner_preselection_stream_bytes", total,
                   "owner_preselection:" + label)
        meter.bump("owner_preselection_stream_records", count,
                   "owner_preselection:" + label)


def producer_build_owner_preselection(runtime: dict[str, Any],
                                      registry: SourceRegistry) -> dict[str, Any]:
    """Build the v299 OwnerPre from independently opened task176 owners.

    This constructor intentionally does not consume ``runtime["heavy_public"]``
    or any producer final-carrier field.  It checks the physical chain and
    retains only typed owner metadata, family ownership, and algorithm pins;
    selected K0/Gamma/Q0 state is supplied later by Sel(r).
    """
    receipt = registry.json("task176_receipt")
    manifest = registry.json("task176_manifest")
    crosscheck = registry.json("task176_crosscheck")
    recovery_v1 = registry.json("task176_recovery")
    recovery_v2 = registry.json("task176_recovery_v2")
    require(receipt.get("schema") ==
            "d972-r07-all-seven-extension-section-census/v1" and
            receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") ==
            "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS" and
            receipt.get("self_digest_sha256") ==
            "f8f0ce249ff547d3e1235bd4b9760daa2b34b23771bf7da47b48dbd5cbbfae1d",
            "producer task176 receipt authority")
    require(manifest == {"artifact_id": "9635036013", "head":
            "0533e42019c9f67f6cec3d1566152db17b903836", "member":
            "d972_r07_all_seven_extension_section_census_v1.json",
            "member_bytes": 13649089, "member_sha256":
            SOURCE_PINS["task176_receipt"][2], "run": "33044121344",
            "zip_sha256": "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912"},
            "producer task176 manifest authority")
    require(crosscheck.get("schema") ==
            "d972-r07-all-seven-extension-section-census-check/v1" and
            crosscheck.get("grade") == "CROSS_CHECKED" and
            crosscheck.get("producer_sha256") == SOURCE_PINS["task176"][2] and
            crosscheck.get("receipt_sha256") == SOURCE_PINS["task176_receipt"][2] and
            crosscheck.get("receipt_terminal") == receipt["terminal"],
            "producer task176 crosscheck authority")
    require(recovery_v1.get("schema") ==
            "d972-r07-all-seven-extension-section-census-recovery-manifest/v1" and
            recovery_v1.get("self_digest_sha256") ==
            "f8c6c0faf2588cd58d8a2aec75a2a1f9950ea67769dd913fbd796d018098f581",
            "producer recovery-v1 authority")
    require(recovery_v2.get("schema") ==
            "d972-r07-all-seven-extension-section-census-recovery-manifest/v2" and
            recovery_v2.get("self_digest_sha256") ==
            "e95b4e7781a14cffd07d445141f20c942861168d201f2ce62879a0ddf3a45026" and
            recovery_v2.get("execution") == "UNEXECUTED" and
            recovery_v2.get("mathematical_grade_change") is False and
            recovery_v2.get("archive_sha256") ==
                "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912" and
            recovery_v2.get("artifact_id") == "9635036013" and
            recovery_v2.get("artifact_name") == "gap-run-out" and
            recovery_v2.get("head") == "0533e42019c9f67f6cec3d1566152db17b903836" and
            recovery_v2.get("run") == "33044121344" and
            recovery_v2.get("hashes_file") == {"bytes": 261,
                "path": "d972_r07_all_seven_extension_section_census_hashes_v1.txt",
                "sha256": "c7cc68fd3e57e42fa03c85190c3c85f10f41b368d4a0182b0c25711fe36b933a"} and
            recovery_v2.get("physical_sources") == {
                "producer": {"bytes": SOURCE_PINS["task176"][1],
                    "path": SOURCE_PINS["task176"][0],
                    "sha256": SOURCE_PINS["task176"][2]},
                "checker": {"bytes": SOURCE_PINS["task176_checker"][1],
                    "path": SOURCE_PINS["task176_checker"][0],
                    "sha256": SOURCE_PINS["task176_checker"][2]}} and
            recovery_v2.get("task176_reply") == {
                "bytes": SOURCE_PINS["task176_reply"][1],
                "path": SOURCE_PINS["task176_reply"][0],
                "sha256": SOURCE_PINS["task176_reply"][2]},
            "producer recovery-v2 authority")
    result = receipt.get("result")
    require(type(result) is dict and type(result.get("Q0_section")) is dict and
            type(result.get("Gamma")) is dict and
            type(result.get("A_families")) is dict and
            type(result.get("families")) is dict and
            type(result.get("word_generators")) is dict,
            "producer task176 owner result")
    q0 = result["Q0_section"]; gamma = result["Gamma"]
    q0_roster = _producer_owner_meta(q0["canonical_roster"], "Q0.roster")
    q0_parents = _producer_owner_meta(q0["parent_states_u32le"], "Q0.parents")
    q0_letters = _producer_owner_meta(q0["parent_letters_u8"], "Q0.letters")
    marked = q0.get("ten_coordinate_marked_generator_blobs_hex")
    require(type(marked) is list and len(marked) == 10 and
            all(type(row) is list and len(row) == 2 and
                all(type(blob) is str and len(bytes.fromhex(blob)) in (40, 154)
                    for blob in row) for row in marked),
            "producer task176 marked generators")
    gamma_states = _producer_owner_meta(gamma["ten_coordinate_states"],
                                        "Gamma.states")
    gamma_parents = _producer_owner_meta(gamma["section_parent_states_u16le"],
                                         "Gamma.parents")
    gamma_records = _producer_owner_meta(gamma["section_parent_record_u8"],
                                         "Gamma.records")
    # Decode each physical blob only long enough to authenticate its bounded
    # compressed payload and raw digest; the returned bytes are released before
    # the next blob and are never retained beside the heavy runtime.
    decoded = _producer_decode_task176_blob(
        q0["canonical_roster"], q0_roster["raw_bytes"], "Q0.roster",
        runtime.get("meter"))
    del decoded
    decoded = _producer_decode_task176_blob(
        q0["parent_states_u32le"], q0_parents["raw_bytes"], "Q0.parents",
        runtime.get("meter"))
    del decoded
    decoded = _producer_decode_task176_blob(
        q0["parent_letters_u8"], q0_letters["raw_bytes"], "Q0.letters",
        runtime.get("meter"))
    del decoded
    decoded = _producer_decode_task176_blob(
        gamma["ten_coordinate_states"], gamma_states["raw_bytes"],
        "Gamma.states", runtime.get("meter"))
    del decoded
    decoded = _producer_decode_task176_blob(
        gamma["section_parent_states_u16le"], gamma_parents["raw_bytes"],
        "Gamma.parents", runtime.get("meter"))
    del decoded
    decoded = _producer_decode_task176_blob(
        gamma["section_parent_record_u8"], gamma_records["raw_bytes"],
        "Gamma.records", runtime.get("meter"))
    del decoded
    require(int(q0.get("order")) == K0_STATE_COUNT and
            int(gamma.get("order")) == 243 and
            len(gamma.get("record_words", [])) == 26,
            "producer task176 owner cardinality")
    # Bind every decoded physical stream to the corresponding locally
    # materialized owner.  Metadata alone is not accepted as a carrier, and
    # no locally generated stream is joined into a second global blob.
    stream_meter = runtime.get("meter")
    _producer_bind_owner_stream(
        q0_roster, (bytes(state) for state in runtime["qstates"]),
        "Q0.roster", stream_meter)
    _producer_bind_owner_stream(
        q0_parents,
        (struct.pack("<I", int(parent)) for parent in runtime["parents"]),
        "Q0.parents", stream_meter)
    _producer_bind_owner_stream(
        q0_letters,
        (bytes((int(letter),)) for letter in runtime["letters"]),
        "Q0.letters", stream_meter)
    _producer_bind_owner_stream(
        gamma_states,
        (b"".join(runtime["p176"].packed_joint_blob(
            value, "producer OwnerPre Gamma state") for value in row)
         for row in runtime["projected"]),
        "Gamma.states", stream_meter)
    _producer_bind_owner_stream(
        gamma_parents,
        (struct.pack("<H", 0 if parent is None else int(parent))
         for parent in runtime["gamma"].parent),
        "Gamma.parents", stream_meter)
    _producer_bind_owner_stream(
        gamma_records,
        (bytes((0 if record is None else int(record),))
         for record in runtime["gamma"].parent_generator),
        "Gamma.records", stream_meter)
    family_order = ["ALL"] + ["S" + str(index) for index in range(10)]
    family_owners: list[dict[str, Any]] = []
    for name in family_order:
        family = result["families"].get(name)
        A = result["A_families"].get(name)
        words = result["word_generators"].get(name)
        require(type(family) is dict and type(A) is dict and
                type(words) is dict, "producer family owner:" + name)
        membership = _producer_owner_meta(family["membership_bitset"],
                                          name + ".membership")
        family_owners.append({"name": name,
            "coordinate_indices": [int(value) for value in
                                    family["coordinate_indices"]],
            "A_order": int(family["A_order"]),
            "L_order": int(family["L_order"]),
            "membership_bitset_metadata": membership,
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
        "physical_chain": physical_chain,
        "q0_owner": {"order": int(q0["order"]),
            "canonical_roster": q0_roster, "parents": q0_parents,
            "letters": q0_letters,
            "marked_generators": {"count": len(marked),
                "sha256": sha_obj(marked)},
            "complete_presentation_relators_sha256":
                q0["complete_presentation_relators_sha256"]},
        "gamma_owner": {"order": int(gamma["order"]),
            "ten_coordinate_states": gamma_states,
            "parents": gamma_parents, "records": gamma_records,
            "record_words": {"count": len(gamma["record_words"]),
                "sha256": sha_obj(gamma["record_words"])}},
        "family_owners": family_owners,
        "deletion_owner_sha256": sha_obj(result["deletion"]),
        "primitive_registry": {key: {"path": row[0], "bytes": row[1],
            "sha256": row[2]} for key, row in sorted(SOURCE_PINS.items())},
        "algorithms": {"task176_decoder":
            "zlib+base64-lossless-bounded-decode-v1",
            "selected_k0": "v12c-coarse-open-address-retained-full-state-first-gid-bfs",
            "canonical_json": "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=True)",
            "digest_framing": "sha256(canonical(value))"}}
    require(owner["q0_owner"]["canonical_roster"]["record_count"] ==
            K0_STATE_COUNT and owner["gamma_owner"]["order"] == 243,
            "producer OwnerPre decoded cardinality")
    runtime["owner_preselection"] = owner
    runtime["owner_preselection_sha256"] = sha_obj(owner)
    return owner


def _producer_selected_validator(runtime: dict[str, Any], frame: dict[str, Any],
                                 recovery: dict[str, Any]) -> None:
    _producer_validator_event(runtime, "validate_selected_frame",
                              "frame", "selected-correction-frame")
    validate_seal(frame)
    _producer_validator_event(runtime, "validate_selected_frame",
                              "heavy_identity", "selected.frame.heavy_public")
    require(set(frame) == {"schema", "record", "recovery", "heavy_input_sha256",
            "heavy_public", "target", "producer_sparse_equality",
            "boundary_preimage", "validator", "source_snapshots",
            "final_heavy_carrier", "h_final", "final_heavy_identity_public",
            "final_heavy_identity_sha256", "self_digest"} and
            frame.get("schema") == SCHEMA + "/selected-correction-selftest-frame" and
            frame.get("heavy_input_sha256") == runtime["heavy_input_sha256"] and
            frame.get("heavy_public") == runtime["heavy_public"] and
            frame.get("heavy_input_sha256") == sha_obj(frame.get("heavy_public")) and
            frame.get("source_snapshots") == runtime.get("source_snapshots",
                                                            frame.get("source_snapshots")) and
            frame.get("record", {}).get("coefficient") == 1 and
            frame.get("target") == frame.get("record", {}).get("sparse_row") and
            frame.get("producer_sparse_equality") is True and
            frame.get("boundary_preimage") == [],
            "selected-correction frame")
    owner_pre = runtime.get("owner_preselection")
    owner_pre_sha = runtime.get("owner_preselection_sha256")
    require(type(owner_pre) is dict and type(owner_pre_sha) is str,
            "producer selected OwnerPre")
    identity = {"schema": "r07-a0-final-heavy-carrier/v2",
        "p0": runtime["p0_identity"],
        "p0_self_digest_sha256": runtime["p0_identity"][
            "self_digest_sha256"],
        "sources": runtime["p0_sources"],
        "frozen_authorities": runtime["p0_frozen_authorities"],
        "algorithms": {"selected_k0":
            "v12c-coarse-open-address-retained-full-state-first-gid-bfs",
            "correction_validator": SCHEMA +
                "/selected-correction-selftest-frame",
            "canonical_json": "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=True)",
            "digest_framing": "sha256(canonical(H))"},
        "preselection_owner": {"public": owner_pre,
                                "sha256": owner_pre_sha},
        "selected_statement": producer_selected_statement(frame["record"])}
    require(frame.get("final_heavy_carrier") == identity and
            frame.get("h_final") == sha_obj(identity) and
            frame.get("final_heavy_identity_public") == identity and
            frame.get("final_heavy_identity_sha256") == sha_obj(identity),
            "final heavy identity")
    producer_validate_correction(runtime, frame["record"], recovery)


def _flip_hex(text: str) -> str:
    raw = bytearray.fromhex(text)
    require(raw, "producer mutation nonempty hex")
    raw[0] ^= 1
    return raw.hex()


def _producer_selected_mutators() -> dict[str, Any]:
    """Declarative owner mutations; validation is never selected by a name branch."""
    def record(frame: dict[str, Any]) -> dict[str, Any]:
        return frame["record"]
    def provenance(frame: dict[str, Any]) -> dict[str, Any]:
        return record(frame)["provenance"]
    def section(frame: dict[str, Any]) -> dict[str, Any]:
        return provenance(frame)["section_provenance"]
    return {
        "selected_q0_roster_state": lambda frame: section(frame).__setitem__(
            "q0_state_hex", _flip_hex(section(frame)["q0_state_hex"])),
        "selected_q0_parent": lambda frame: section(frame).__setitem__(
            "q0_parent_state_id", int(section(frame)["q0_parent_state_id"]) + 1),
        "selected_q0_letter": lambda frame: section(frame)["selected_q0_word"].append(1),
        "selected_marked_generator": lambda frame: section(frame)[
            "selected_marked_generator_row"].__setitem__(0, 2),
        "selected_gamma_state": lambda frame: section(frame).__setitem__(
            "gamma_projected_ten_state_hex",
            _flip_hex(section(frame)["gamma_projected_ten_state_hex"])),
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
            "heavy_input_sha256", _flip_hex(frame["heavy_input_sha256"])),
        "selected_section_word": lambda frame: section(frame)["selected_base_word"].append(1),
        "selected_coefficient_two_inverse_word": lambda frame: provenance(
            frame)["conjugate_word"].append(1),
        "recovery_v1_substitution": lambda frame: provenance(frame)[
            "recovery_v1"].__setitem__("bytes", int(provenance(frame)[
                "recovery_v1"]["bytes"]) + 1),
        "recovery_v2_corrected_field": lambda frame: provenance(frame)[
            "recovery_v2"]["correction"].__setitem__("new_value", "0" * 64),
        "recovery_v2_self_seal": lambda frame: provenance(frame)[
            "recovery_v2"].__setitem__("self_digest_sha256", _flip_hex(
                provenance(frame)["recovery_v2"]["self_digest_sha256"])),
        "q0_parent_letter_roster": lambda frame: section(frame).__setitem__(
            "q0_parent_letter_digest", _flip_hex(
                section(frame)["q0_parent_letter_digest"])),
        "q3_marked_permutation": lambda frame: section(frame)[
            "q3_marked_permutation_rows"][1].__setitem__(0, 3),
        "one_coordinate_mark": lambda frame: section(frame)[
            "selected_coordinate_mark_hex"].__setitem__(0, _flip_hex(
                section(frame)["selected_coordinate_mark_hex"][0])),
        "gamma_parent_record_word": lambda frame: section(frame).__setitem__(
            "gamma_parent_record_id", int(section(frame)["gamma_parent_record_id"]) + 1),
        "gamma_projected_970_byte_state": lambda frame: section(frame).__setitem__(
            "gamma_projected_ten_state_sha256", _flip_hex(
                section(frame)["gamma_projected_ten_state_sha256"])),
        "gamma_full_vs_projected_substitution": lambda frame: section(frame).__setitem__(
            "gamma_full_state_hex", _flip_hex(section(frame)["gamma_full_state_hex"])),
        "k0_coarse_key_full_blob_least_base": lambda frame: section(frame).__setitem__(
            "k0_state_digest", _flip_hex(section(frame)["k0_state_digest"])),
        "kernel_generator_order_cursor_word": lambda frame: section(frame)[
            "kernel_generators"].append([1]),
        # A reduced identity pair is still a real owner-byte mutation: the
        # direct-column replay remains unchanged, while the typed product
        # witness must reject the unreduced provenance word at product_order.
        "product_order": lambda frame: provenance(frame)["delta_word"].extend([1, -1]),
        "heavy_identity_final_row": lambda frame: frame["heavy_public"].__setitem__(
            "light_input_sha256", _flip_hex(frame["heavy_public"][
                "light_input_sha256"])),
    }


def _producer_path_identity(path: Path, logical_label: str = "candidate",
                            content_sha256: str | None = None
                            ) -> dict[str, Any]:
    try:
        item = os.lstat(path)
    except FileNotFoundError:
        marker = "UNREADABLE_AT_REGISTERED_STAGE"
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
        marker = "UNREADABLE_AT_REGISTERED_STAGE"
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
    digest = content_sha256 if content_sha256 is not None else \
        "UNREADABLE_AT_REGISTERED_STAGE"
    return {"logical_case_path": logical_label,
            "owner_kind": "regular" if stat.S_ISREG(item.st_mode) else "other",
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


def _producer_capture_physical_projection(runtime: dict[str, Any], path: Path,
                                          *, before: Any, after: Any,
                                          path_after: Any, raw: bytes | None,
                                          reason: str | None) -> None:
    """Project the already-observed V297 witness without host identifiers."""
    label = str(runtime.get("_physical_logical_label", "candidate.path"))
    marker = "UNREADABLE_AT_REGISTERED_STAGE"
    if path_after is not None and stat.S_ISLNK(path_after.st_mode):
        owner_kind = "symlink"
        symlink = True
    elif before is not None and stat.S_ISREG(before.st_mode):
        owner_kind = "regular"
        symlink = False
    elif before is None:
        owner_kind = "missing"
        symlink = False
    else:
        owner_kind = "other"
        symlink = False
    readable = raw is not None and len(raw) > 0
    content_sha = sha_bytes(raw) if readable else marker
    byte_length: int | str = len(raw) if readable else marker
    before_links = None if before is None else int(before.st_nlink)
    after_links = None if after is None else int(after.st_nlink)
    stable = bool(before is not None and after is not None and
                  (before.st_dev, before.st_ino, before.st_size,
                   before.st_mtime_ns, before.st_nlink) ==
                  (after.st_dev, after.st_ino, after.st_size,
                   after.st_mtime_ns, after.st_nlink))
    pathname_equal = bool(path_after is not None and after is not None and
                          not stat.S_ISLNK(path_after.st_mode) and
                          (path_after.st_dev, path_after.st_ino,
                           path_after.st_size, path_after.st_mtime_ns,
                           path_after.st_nlink) ==
                          (after.st_dev, after.st_ino, after.st_size,
                           after.st_mtime_ns, after.st_nlink))
    substituted = reason in ("physical pathname substituted",
                             "physical pathname identity") or (
        path_after is not None and after is not None and not pathname_equal)
    projection = {
        "logical_case_path": label,
        "owner_kind": owner_kind,
        "byte_length": byte_length,
        "content_sha256": content_sha,
        "link_count_before": before_links,
        "link_count_after": after_links,
        "symlink_or_reparse": symlink,
        # A regular semantic owner has no link target.  The target is only
        # meaningful for a link/reparse mutation; keeping it null here makes
        # the baseline and mutant projections comparable without letting a
        # logical label/path choice create the reported identity delta.
        "logical_link_target": runtime.get("_physical_logical_link_target")
        if symlink else None,
        "single_open_handle": before is not None,
        "opened_handle_stable": stable,
        "pathname_matches_opened_handle": pathname_equal,
        "substitution_detected": substituted,
        "canonical_before_sha256": runtime.get("_physical_baseline_sha256",
                                               marker),
        "canonical_after_sha256": content_sha,
        "resealed_logical_nodes": [],
        "entered_validators": [event["validator"] for event in
                               runtime.get("_active_validator_events", [])],
        "event_trace_digest": sha_obj(runtime.get(
            "_active_validator_events", [])),
        "first_typed_rejection": reason,
    }
    runtime["_physical_projection"] = projection


def _producer_validator_event(runtime: dict[str, Any], validator: str,
                              stage: str, owner: str) -> None:
    events = runtime.setdefault("_active_validator_events", [])
    events.append({"validator": validator, "stage": stage, "owner": owner})
    projection = runtime.get("_physical_projection")
    if isinstance(projection, dict):
        projection["entered_validators"] = [event["validator"]
                                             for event in events]
        projection["event_trace_digest"] = sha_obj(events)


def _producer_physical_projection_reason(runtime: dict[str, Any],
                                         reason: str) -> None:
    projection = runtime.get("_physical_projection")
    if isinstance(projection, dict):
        projection["first_typed_rejection"] = reason
        projection["entered_validators"] = [event["validator"]
                                             for event in runtime.get(
                                                 "_active_validator_events", [])]
        projection["event_trace_digest"] = sha_obj(runtime.get(
            "_active_validator_events", []))


def _producer_identity_changed(before: dict[str, Any],
                               after: dict[str, Any]) -> bool:
    """Compare physical projection, deliberately excluding logical labels."""
    return {key: value for key, value in before.items()
            if key != "logical_case_path"} != {
        key: value for key, value in after.items()
                if key != "logical_case_path"}


def _producer_mutation_trace(path: Path, value: Any,
                             validator: Any,
                             trace_runtime: dict[str, Any] | None = None
                             ) -> tuple[str, str, str]:
    """Persist only the typed delta; the ordinary validator consumes its view."""
    require(hasattr(value, "freeze_delta") and hasattr(value, "physical_delta"),
            "mutation route requires bounded owner delta")
    value.freeze_delta()
    delta = value.physical_delta()
    before = str(delta["baseline_self_digest"])
    if trace_runtime is not None:
        trace_runtime["_active_validator_events"] = []
        trace_runtime["_terminal_count"] = 0
        trace_runtime["_last_owner_disposed"] = False
    raw = canonical(delta) + b"\n"
    try:
        with path.open("xb") as stream:
            view = memoryview(raw)
            while view:
                if trace_runtime is not None and trace_runtime.get("meter") is not None:
                    trace_runtime["meter"].check("mutation_delta_write")
                written = stream.write(view[:1 << 20])
                require(written > 0, "mutation delta short write")
                view = view[written:]
            stream.flush(); os.fsync(stream.fileno())
        parsed, physical = read_bounded_json(path, len(raw),
                                             trace_runtime.get("meter")
                                             if trace_runtime else None)
        validate_seal(parsed)
        require(parsed == delta, "bounded mutation physical delta binding")
        try:
            validator(value)
        except ProtocolStop as exc:
            if trace_runtime is not None:
                trace_runtime["_terminal_count"] = int(
                    trace_runtime.get("_terminal_count", 0)) + 1
                _producer_physical_projection_reason(trace_runtime, str(exc))
            return before, physical["sha256"], str(exc)
        raise ProtocolStop("MUTATION_ACCEPTED:" + path.name)
    finally:
        try: path.unlink()
        except FileNotFoundError: pass
        if trace_runtime is not None:
            trace_runtime["_last_owner_disposed"] = not path.exists()
def producer_selected_correction_mutations(runtime: dict[str, Any],
                                            frame: dict[str, Any],
                                            fixture: dict[str, Any],
                                            registry: SourceRegistry) -> list[dict[str, Any]]:
    recovery = _producer_recovery_public(registry)
    baseline = seal({**frame, "target": frame["record"]["sparse_row"],
        "producer_sparse_equality": True, "boundary_preimage": []})
    baseline_revalidated = False
    _producer_selected_validator(runtime, baseline, recovery)
    baseline_revalidated = True
    contract = {row["id"]: row for row in fixture["mutation_contract"][
        "selected_correction"]}
    mutators = _producer_selected_mutators()
    require(list(contract) == fixture["selected_correction_mutations"] and
            set(mutators) == set(contract), "producer selected mutation contract")
    before = str(baseline["self_digest"])
    ledger: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="r07-v12c-producer-selected-") as directory:
        root = Path(directory)
        for ordinal, name in enumerate(fixture["selected_correction_mutations"]):
            runtime["meter"].check("selected_mutation_delta")
            value = BoundedOwnerDelta(baseline, "selected_correction", name,
                ("record", "recovery", "heavy_input_sha256", "heavy_public"),
                runtime["meter"])
            mutators[name](value)
            _before, after, reason = _producer_mutation_trace(
                root / f"selected-{ordinal:02d}.json", value,
                lambda candidate: _producer_selected_validator(
                    runtime, candidate, recovery), trace_runtime=runtime)
            expected = contract[name]
            require(reason == expected["first_reason"],
                    "producer first reason:" + name + ":" + reason)
            require(before != after, "producer mutation identity unchanged:" + name)
            events = runtime.get("_active_validator_events", [])
            require(events and all(type(event) is dict for event in events),
                    "producer selected validator event trace")
            entered = [event["validator"] for event in events]
            rejection_event = events[-1]
            rejection_validator = rejection_event["validator"]
            terminal_count = int(runtime.get("_terminal_count", 0))
            owner_disposed = bool(runtime.get("_last_owner_disposed"))
            require(terminal_count == 1 and owner_disposed,
                    "producer selected measured terminal/owner:" + name)
            ledger.append({"id": name, "owner_path": expected["owner_path"],
                "identity_kind": "bounded_owner_delta",
                "before_identity": {"kind": "immutable_baseline", "sha256": before},
                "after_identity": {"kind": "physical_delta", "sha256": after},
                "physical_digest": after, "event_trace": list(events),
                "event_trace_digest": sha_obj(events),
                "entered_validators": entered,
                "first_rejection": {"validator": rejection_validator,
                    "stage": rejection_event["stage"], "narrow_reason": reason},
                "baseline_revalidated": baseline_revalidated,
                "terminal_count": terminal_count,
                "owner_disposed": owner_disposed,
                "validator": rejection_event["validator"],
                "stage": rejection_event["stage"],
                "reseal": expected["reseal"], "before_sha256": before,
                "after_sha256": after, "reached_validator": rejection_validator,
                "first_reason": reason})
    return ledger


def blocked_send_selftest(context: Any, meter: Meter, workers: int = 4,
                          deadline_seconds: float = 0.05) -> dict[str, Any]:
    """Exercise one real W4 blocked-send owner; all four children are cleaned."""
    require(workers == 4, "blocked send requires W4")
    def no_drain(sock: socket.socket, deadline: float) -> None:
        sock.settimeout(max(0.0, deadline - time.monotonic()))
        try:
            sock.recv(1)
        except (socket.timeout, EOFError, OSError):
            pass
        finally:
            sock.close()
    deadline = time.monotonic() + deadline_seconds
    parents: list[socket.socket] = []
    processes: list[Any] = []
    rejected = 0
    try:
        for ordinal in range(workers):
            meter.check("W4_blocked_send_start",
                        [process.pid for process in processes if process.pid])
            parent, child = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
            process = context.Process(target=no_drain, args=(child, deadline),
                                      name=f"r07-v12c-W4-blocked-send-{ordinal}")
            process.start(); child.close()
            parents.append(parent); processes.append(process)
        for parent in parents:
            try:
                DeadlineChannel(parent).send(
                    {"padding": "x" * (4 * 1024 * 1024)}, deadline)
            except (TimeoutError, EOFError, OSError):
                rejected += 1
            meter.check("W4_blocked_send",
                        [process.pid for process in processes if process.pid])
    finally:
        for parent in parents:
            try: parent.close()
            except OSError: pass
        for process in processes:
            if process.is_alive():
                process.terminate()
        for process in processes:
            process.join(CHANNEL_CLOSE_SECONDS)
            if process.is_alive():
                process.kill(); process.join(CHANNEL_CLOSE_SECONDS)
        alive = [process.pid for process in processes if process.is_alive()]
        for process in processes:
            process.close()
    require(rejected >= 1 and not alive and len(processes) == workers,
            "blocked send W4 selftest")
    return {"route": "blocked_send", "workers": workers,
            "deadline_rejected": True, "cleanup_complete": True,
            "live_pids_after_join": [], "process_close_count": workers,
            "simultaneous_child_peak": workers}

def _deterministic_cleanup(cleanup: dict[str, Any], workers: int) -> dict[str, Any]:
    """Project process cleanup to stable proof fields; omit PID/exit telemetry."""
    require(cleanup.get("complete") is True and
            cleanup.get("live_pids_after_join") == [] and
            cleanup.get("process_close_count") == workers,
            "selftest cleanup owner")
    return {"complete": True, "live_pids_after_join": [],
            "process_close_count": workers, "process_close": True}


def _deterministic_boundary_accounting(accounting: dict[str, Any],
                                       workers: int,
                                       expect_stop: bool = True) -> dict[str, Any]:
    """Project additive IPC counters and max gauges without host telemetry."""
    additive = ("epochs_committed", "epochs_discarded",
        "literal_pairs_committed", "support_bytes", "frames_sent_bytes",
        "frames_received_bytes", "frames_sent", "frames_received",
        "stop_frames_sent", "stop_frames_received", "accumulator_entries",
        "formal_ancestry_entries", "winner_reconstructions",
        "process_restarts")
    require(all(type(accounting.get(key)) is int and accounting[key] >= 0
                for key in additive) and
            (not expect_stop or (accounting.get("stop_frames_sent") == workers and
             accounting.get("stop_frames_received") == workers)),
            "deterministic cumulative IPC/STOP accounting")
    return {"completed_additive": {key: int(accounting[key])
                                   for key in additive},
            "physical_max": {"max_accumulator_entries":
                             int(accounting["max_accumulator_entries"])},
            "descriptor_count": int(accounting["descriptor_count"]),
            "descriptor_sha256": accounting["descriptor_sha256"],
            "composition": "additive counters sum; physical gauges max"}


def process_selftest(runtime: dict[str, Any], reducer: FormalReducer,
                     fixture: dict[str, Any], meter: Meter) -> dict[str, Any]:
    live = runtime["live"]
    dual = dict(runtime.get("initial_dual_private", {}))
    require(dual and live.pair(dual, runtime["target"]) in (1, 2),
            "selftest cached initial dual owner")
    row_keys = [key for key in sorted(dual) if key[:1] == b"R"]
    require(len(row_keys) == 1188, "selftest actual first dual")
    runs = []
    cumulative_additive: dict[str, int] = {}
    cumulative_max = {"max_accumulator_entries": 0}
    for owner_ordinal, workers in enumerate(fixture["worker_counts"]):
        owner = PersistentBoundaryOwner(runtime, meter, workers)
        owner.accounting["formal_ancestry_entries"] = int(reducer.formal_entries)
        owner.accounting["process_restarts"] = 1 if owner_ordinal else 0
        owner.start()
        try:
            first_descriptor = owner.descriptors[0]
            second_descriptor = next(row for row in owner.descriptors[1:]
                if row["block"] == first_descriptor["block"] and
                   row["relator"] == first_descriptor["relator"] and
                   (row["component"], row["h_blob"]) !=
                   (first_descriptor["component"], first_descriptor["h_blob"]))
            cancellation_second = (-first_descriptor["base_coefficient"] *
                (1 if second_descriptor["base_coefficient"] == 1 else 2)) % 3
            cancellation_probe = {
                live.row_key(first_descriptor["block"], first_descriptor["component"],
                             first_descriptor["h_blob"]): 1,
                live.row_key(second_descriptor["block"], second_descriptor["component"],
                             second_descriptor["h_blob"]): cancellation_second}
            probes = [({}, "empty_support"),
                      ({row_keys[0]: dual[row_keys[0]]}, "one_support"),
                      ({key: dual[key] for key in row_keys[:4]}, "short_support"),
                      ({**{key: dual[key] for key in row_keys[:2]},
                        live.exponent_key(1): 1}, "typed_present_shape_filter"),
                      (cancellation_probe, "f3_cancellation")]
            probe_rows = []
            for probe, label in probes:
                outcome = owner.run_epoch(probe)
                active = owner.materialize(probe, outcome)
                probe_rows.append({"case": label,
                    "support": outcome["support_entry_count"],
                    "pairs": outcome["expanded_pair_count"],
                    "active": active is not None, "zero": active is None,
                    "outcome": outcome})
            serial_duals = []; serial_outcomes = []
            for probe in (dual, live.scaled(dual, 2),
                          {key: dual[key] for key in row_keys[:2]}):
                outcome = owner.run_epoch(probe)
                serial_duals.append(outcome["dual_sha256"])
                serial_outcomes.append(outcome)
            require(len(serial_duals) == 3 and probe_rows[0]["zero"] is True and
                    probe_rows[1]["active"] is True and
                    probe_rows[3]["support"] == 2 and
                    probe_rows[4]["support"] == 2,
                    "selftest serial/ACTIVE/zero/filter/cancellation")
        finally:
            owner.close()
        require(owner.cleanup["complete"], "normal selftest cleanup")
        stable_accounting = _deterministic_boundary_accounting(
            owner.accounting, workers)
        for key, value in stable_accounting["completed_additive"].items():
            cumulative_additive[key] = cumulative_additive.get(key, 0) + int(value)
        cumulative_max["max_accumulator_entries"] = max(
            cumulative_max["max_accumulator_entries"],
            int(stable_accounting["physical_max"]["max_accumulator_entries"]))
        runs.append({"workers": workers, "probes": probe_rows,
                     "three_serial_duals": serial_duals,
                     "three_serial_outcomes": serial_outcomes,
                     "accounting": stable_accounting,
                     "cleanup": _deterministic_cleanup(owner.cleanup, workers)})
    # Every fault is a real sequential W4 owner; no W2/one-child substitute.
    fault_workers = 4
    for fault in ("timeout", "death", "partial"):
        fault_owner = PersistentBoundaryOwner(runtime, meter, fault_workers)
        fault_owner.accounting["formal_ancestry_entries"] = int(
            reducer.formal_entries)
        fault_owner.start(); rejected = False
        try:
            fault_owner.run_epoch({row_keys[0]: dual[row_keys[0]]},
                                  fault=fault, short_deadline=0.05)
        except ResourceStop:
            rejected = True
        require(rejected and fault_owner.cleanup["complete"],
                "fault cleanup:" + fault)
        fault_accounting = _deterministic_boundary_accounting(
            fault_owner.accounting, fault_workers, expect_stop=False)
        for key, value in fault_accounting["completed_additive"].items():
            cumulative_additive[key] = cumulative_additive.get(key, 0) + int(value)
        cumulative_max["max_accumulator_entries"] = max(
            cumulative_max["max_accumulator_entries"], int(
                fault_accounting["physical_max"]["max_accumulator_entries"]))
        runs.append({"workers": fault_workers, "fault": fault,
                     "atomic_discard": True, "accounting": fault_accounting,
                     "cleanup": _deterministic_cleanup(
                          fault_owner.cleanup, fault_workers)})
    context = multiprocessing.get_context("fork")
    blocked = blocked_send_selftest(context, meter, workers=4)
    return {"first_dual": live.public_sparse(dual),
            "first_dual_sha256": live.sha_obj(live.public_sparse(dual)),
            "runs": runs, "blocked_send": blocked,
            "cumulative_accounting": {
                "completed_additive": cumulative_additive,
                "physical_max": cumulative_max,
                "normal_owner_count": len(fixture["worker_counts"]),
                "normal_owner_transitions":
                    max(0, len(fixture["worker_counts"]) - 1),
                "fault_owner_count": 3,
                "blocked_send_owner_count": 1,
                "simultaneous_child_peak": 4,
                "sampled_parent_rss_peak_bytes": meter.sampled_parent_rss_peak,
                "sampled_children_rss_peak_sum_bytes":
                    meter.sampled_children_rss_peak_sum,
                "composition": "all normal/fault counters additive; physical gauges max"},
            "actual_E3_E4_codec": True, "actual_process_owner": True,
            "W2_W4": True}


def producer_boundary_validate(runtime: dict[str, Any], frame: dict[str, Any]) -> None:
    """Validate one boundary envelope against the one sealed owner outcome.

    The persistent owner is exercised once to establish the immutable baseline.
    Mutation cases are ordinary envelope validations; restarting the owner (or
    replaying every epoch) here would make the ledger both non-independent and
    needlessly quadratic.
    """
    live = runtime.get("live")
    require(live is not None and callable(getattr(live, "parse_sparse", None)) and
            callable(getattr(live, "public_sparse", None)),
            "boundary live sparse interface")
    _producer_validator_event(runtime, "validate_boundary_frame",
                              "boundary", "boundary-selftest-frame")
    validate_seal(frame)
    require(set(frame) == {"schema", "workers", "dual", "outcome",
            "orientation", "transport", "counter_floor", "self_digest"},
            "boundary selftest schema")
    dual_public = frame.get("dual")
    _producer_validator_event(runtime, "validate_boundary_frame",
                              "typed_support", "boundary.dual")
    require(type(dual_public) is list and all(
        type(item) is list and len(item) == 2 and item[1] in (1, 2)
        for item in dual_public), "sparse item")
    try:
        dual = live.parse_sparse(dual_public)
    except (TypeError, ValueError, IndexError, KeyError):
        raise ProtocolStop("sparse item")
    require(live.public_sparse(dual) == frame.get("dual"), "sparse item")
    try:
        for key in dual:
            if key[:1] == b"R":
                producer_decode_row_key(key)
            else:
                require(key in (producer_exponent_key(1),
                                producer_exponent_key(2)), "sparse item")
    except ProtocolStop:
        raise ProtocolStop("sparse item")
    require(frame.get("schema") == SCHEMA + "/boundary-selftest-frame",
            "boundary selftest owner frame")
    _producer_validator_event(runtime, "validate_boundary_frame",
                              "orientation", "boundary.orientation")
    require(frame.get("orientation") == "t=g*h^-1;t*h=g",
            "boundary selftest owner frame")
    _producer_validator_event(runtime, "validate_boundary_frame",
                              "transport", "boundary.transport")
    require(frame.get("transport") == runtime.get(
                "_producer_boundary_transport_expected"),
            "boundary selftest owner frame")
    _producer_validator_event(runtime, "validate_boundary_frame",
                              "counter", "boundary.counter_floor")
    require(frame.get("counter_floor") == frame.get("outcome", {}).get(
                "expanded_pair_count"), "boundary selftest owner frame")
    expected = runtime.get("_producer_boundary_expected")
    require(type(expected) is dict, "boundary selftest immutable ordinary outcome")
    outcome = frame.get("outcome")
    if type(outcome) is not dict:
        _producer_validator_event(runtime, "independent_boundary_outcome",
                                  "result_digest", "boundary.outcome")
        raise ProtocolStop("boundary selftest immutable ordinary outcome")
    # Emit the reached ordinary sub-validator at the first differing field;
    # this is evidence from the validator, not a mutation-name projection.
    for field, stage in (("epoch", "epoch"), ("intervals", "interval_partition"),
                         ("worker_results", "result_digest"),
                         ("selected", "winner"),
                         ("selected_scalar", "scalar")):
        if outcome.get(field) != expected.get(field):
            _producer_validator_event(runtime, "independent_boundary_outcome",
                                      stage, "boundary.outcome")
            raise ProtocolStop("boundary selftest immutable ordinary outcome")
    if outcome != expected:
        _producer_validator_event(runtime, "independent_boundary_outcome",
                                  "result_digest", "boundary.outcome")
        raise ProtocolStop("boundary selftest immutable ordinary outcome")


def _producer_boundary_mutators(routes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "wrong_typed_support": lambda value: value["dual"][0].__setitem__(
            0, (bytearray.fromhex(value["dual"][0][0])[:1] + b"\x04" +
                bytearray.fromhex(value["dual"][0][0])[2:]).hex()),
        "missing_interval": lambda value: value["outcome"]["intervals"][0].__setitem__(
            1, value["outcome"]["intervals"][0][1] - 1),
        "overlapping_interval": lambda value: value["outcome"]["intervals"][1].__setitem__(
            0, value["outcome"]["intervals"][1][0] - 1),
        "wrong_t_orientation": lambda value: value.__setitem__(
            "orientation", "t=h^-1*g"),
        "changed_accumulator": lambda value: value["outcome"][
            "worker_results"][0]["accumulator"].__setitem__(
                0, [1, value["outcome"]["worker_results"][0]["accumulator"][0][1],
                    1, 1]) if value["outcome"]["worker_results"][0][
                        "accumulator"] else value["outcome"]["worker_results"][0][
                            "accumulator"].append([1, "00", 1, 1]),
        "changed_winner": lambda value: value["outcome"].__setitem__(
            "selected", None if value["outcome"].get("selected") is not None else
            [1, value["dual"][0][0], 1]),
        "changed_scalar": lambda value: value["outcome"].__setitem__(
            "selected_scalar", 1 if value["outcome"].get("selected_scalar") is None
            else 3 - int(value["outcome"]["selected_scalar"])),
        "cross_epoch_frame": lambda value: value["outcome"].__setitem__(
            "epoch", int(value["outcome"]["epoch"]) + 1),
        "blocked_send": lambda value: value.__setitem__(
            "transport", routes["blocked_send"]),
        "partial_worker": lambda value: value.__setitem__(
            "transport", routes["partial"]),
        "dead_worker": lambda value: value.__setitem__(
            "transport", routes["death"]),
        "surviving_process": lambda value: value["transport"][
            "cleanup"].__setitem__("live_pids_after_join", [1]),
        "counter_reset": lambda value: value.__setitem__("counter_floor", 0),
    }


def producer_boundary_mutations(runtime: dict[str, Any], processes: dict[str, Any],
                                fixture: dict[str, Any]) -> list[dict[str, Any]]:
    live = runtime["live"]; dual = live.parse_sparse(processes["first_dual"])
    workers = 4
    owner_run = next(row for row in processes["runs"]
                     if row.get("workers") == workers and row.get("fault") is None)
    outcome = owner_run["three_serial_outcomes"][0]
    # Reuse the extant pre-heavy ordinary W4 transition.  No post-heavy fork,
    # fresh meter or fabricated outcome is permitted here.
    runtime["_producer_boundary_expected"] = outcome
    normal_transport = {"route": "normal", "workers": workers,
        "outcome_sha256": sha_obj(outcome),
        "accounting": owner_run["accounting"],
        "cleanup": owner_run["cleanup"]}
    routes = {"blocked_send": {"route": "blocked_send",
        "owner": processes["blocked_send"]}}
    for fault in ("timeout", "death", "partial"):
        fault_run = next(row for row in processes["runs"]
                         if row.get("fault") == fault)
        routes[fault] = {"route": fault, "workers": fault_run["workers"],
            "atomic_discard": fault_run["atomic_discard"],
            "accounting": fault_run["accounting"],
            "cleanup": fault_run["cleanup"]}
    runtime["_producer_boundary_transport_expected"] = normal_transport
    baseline = seal({"schema": SCHEMA + "/boundary-selftest-frame",
        "workers": workers, "dual": live.public_sparse(dual), "outcome": outcome,
        "orientation": "t=g*h^-1;t*h=g",
        "transport": normal_transport,
        "counter_floor": outcome["expanded_pair_count"]})
    baseline_revalidated = False
    producer_boundary_validate(runtime, baseline)
    baseline_revalidated = True
    contract = {row["id"]: row for row in fixture["mutation_contract"]["boundary"]}
    mutators = _producer_boundary_mutators(routes)
    require(list(contract) == fixture["boundary_mutations"] and
            set(mutators) == set(contract), "producer boundary mutation contract")
    before = str(baseline["self_digest"]); ledger = []
    with tempfile.TemporaryDirectory(prefix="r07-v12c-producer-boundary-") as directory:
        root = Path(directory)
        for ordinal, name in enumerate(fixture["boundary_mutations"]):
            runtime["meter"].check("boundary_mutation_delta")
            value = BoundedOwnerDelta(baseline, "boundary", name,
                ("dual", "outcome", "orientation", "transport", "counter_floor"),
                runtime["meter"])
            mutators[name](value)
            _before, after, reason = _producer_mutation_trace(
                root / f"boundary-{ordinal:02d}.json", value,
                lambda candidate: producer_boundary_validate(runtime, candidate),
                trace_runtime=runtime)
            expected = contract[name]
            require(reason == expected["first_reason"],
                    "producer boundary first reason:" + name + ":" + reason)
            require(before != after, "producer boundary identity unchanged:" + name)
            events = runtime.get("_active_validator_events", [])
            require(events, "producer boundary validator event trace")
            entered = [event["validator"] for event in events]
            terminal_count = int(runtime.get("_terminal_count", 0))
            owner_disposed = bool(runtime.get("_last_owner_disposed"))
            require(terminal_count == 1 and owner_disposed,
                    "producer boundary measured terminal/owner:" + name)
            ledger.append({"id": name, "owner_path": expected["owner_path"],
                "identity_kind": "bounded_owner_delta",
                "before_identity": {"kind": "immutable_baseline", "sha256": before},
                "after_identity": {"kind": "physical_delta", "sha256": after},
                "physical_digest": after, "event_trace": list(events),
                "event_trace_digest": sha_obj(events),
                "entered_validators": entered,
                "first_rejection": {"validator": events[-1]["validator"],
                    "stage": events[-1]["stage"], "narrow_reason": reason},
                "baseline_revalidated": baseline_revalidated,
                "terminal_count": terminal_count,
                "owner_disposed": owner_disposed,
                "validator": events[-1]["validator"],
                "stage": events[-1]["stage"],
                "reseal": expected["reseal"], "before_sha256": before,
                "after_sha256": after, "reached_validator": events[-1]["validator"],
                "first_reason": reason})
    return ledger


def producer_validate_coefficient_two(runtime: dict[str, Any],
                                      value: dict[str, Any]) -> None:
    _producer_validator_event(runtime, "validate_coefficient_two_frame",
                              "coefficient_two", "coefficient-two-frame")
    live = runtime["live"]; model = runtime["model"]
    validate_seal(value)
    require(set(value) == {"schema", "coefficient", "delta_word",
            "relator_word", "stored_row", "target", "factor_word",
            "correction_word", "self_digest"} and
            value.get("schema") == SCHEMA + "/coefficient-two-selftest-frame" and
            value.get("coefficient") == 2, "coefficient-two frame")
    row, replay = model.direct_column(value["delta_word"], value["relator_word"])
    inverse_row, inverse_replay = model.direct_column(
        value["delta_word"], live.inverse_word(value["relator_word"]))
    factor = live.inverse_word(replay["conjugate_word"])
    require(live.public_sparse(row) == value.get("stored_row") and
            live.parse_sparse(value.get("target")) == live.scaled(row, 2) and
            inverse_row == live.scaled(row, 2) and
            inverse_replay["conjugate_word"] == factor and
            value.get("factor_word") == factor and
            value.get("correction_word") == factor and
            runtime["joint_group"].eval(factor) == runtime["joint_group"].identity,
            "literal coefficient-two inverse word")


def producer_validate_positive(runtime: dict[str, Any], value: dict[str, Any],
                               recovery: dict[str, Any]) -> None:
    physical_trace = "_physical_logical_label" in runtime
    _producer_validator_event(runtime, "selftest_envelope" if physical_trace else
                              "validate_positive_frame",
                              "identity_envelope" if physical_trace else
                              "positive", "positive-selftest-frame")
    validate_seal(value)
    require(set(value) == {"schema", "selected", "selected_record_sha256",
            "coefficient", "target",
            "boundary_preimage", "producer_sparse_equality",
            "heavy_input_sha256", "heavy_public", "claims", "self_digest"} and
            value.get("schema") == SCHEMA + "/positive-selftest-frame" and
            value.get("claims") == FALSE_CLAIMS and
            "checkpoint" not in value, "SELFTEST identity envelope")
    selected = value.get("selected")
    _producer_validator_event(runtime, "validate_positive_frame",
                              "selected_support", "positive.selected")
    require(type(selected) is list and len(selected) == 1,
            "SELFTEST selected support complete")
    if value.get("selected_record_sha256") != runtime.get(
            "_producer_positive_selected_sha256") or sha_obj(selected[0]) != \
            runtime.get("_producer_positive_selected_sha256"):
        _producer_validator_event(runtime, "validate_correction_provenance",
                                  "row_replay", "selected.record.sparse_row")
        raise ProtocolStop("selected correction stored row")
    _producer_validator_event(runtime, "validate_positive_frame",
                              "coefficient", "positive.coefficient")
    require(value.get("coefficient") == 1, "SELFTEST selected coefficient")
    _producer_validator_event(runtime, "validate_positive_frame",
                              "target", "positive.target")
    require(value.get("target") == selected[0].get("sparse_row"),
            "SELFTEST target/g760")
    _producer_validator_event(runtime, "validate_positive_frame",
                              "preimage", "positive.boundary_preimage")
    require(value.get("boundary_preimage") == [],
            "SELFTEST typed preimage/support")
    _producer_validator_event(runtime, "validate_positive_frame",
                              "residual", "positive.producer_sparse_equality")
    require(value.get("producer_sparse_equality") is True,
            "SELFTEST typed preimage/support")
    require(value.get("heavy_input_sha256") == runtime["heavy_input_sha256"] and
            value.get("heavy_public") == runtime["heavy_public"],
            "SELFTEST independently derived PB3/PB4 residual")
    # The selected record was authenticated once before this suite.  Positive
    # mutations bind its immutable digest and never rerun Gamma/K0 validation.


def producer_positive_mutations(runtime: dict[str, Any], selected_frame: dict[str, Any],
                                fixture: dict[str, Any], registry: SourceRegistry) -> list[dict[str, Any]]:
    recovery = _producer_recovery_public(registry)
    baseline = seal({"schema": SCHEMA + "/positive-selftest-frame",
        "selected": [selected_frame["record"]], "coefficient": 1,
        "selected_record_sha256": sha_obj(selected_frame["record"]),
        "target": selected_frame["record"]["sparse_row"],
        "boundary_preimage": [], "producer_sparse_equality": True,
        "heavy_input_sha256": runtime["heavy_input_sha256"],
        "heavy_public": runtime["heavy_public"], "claims": dict(FALSE_CLAIMS)})
    runtime["_producer_positive_selected_sha256"] = sha_obj(
        selected_frame["record"])
    baseline_revalidated = False
    producer_validate_positive(runtime, baseline, recovery)
    baseline_revalidated = True
    contract = {row["id"]: row for row in fixture["mutation_contract"]["positive"]}
    require(list(contract) == fixture["positive_mutations"],
            "producer positive mutation contract")
    before = str(baseline["self_digest"]); ledger = []
    with tempfile.TemporaryDirectory(prefix="r07-v12c-producer-positive-") as directory:
        root = Path(directory)
        for ordinal, name in enumerate(fixture["positive_mutations"]):
            if name == "wrong_coefficient_two_word":
                record = selected_frame["record"]; prov = record["provenance"]
                coefficient_baseline = seal({"schema": SCHEMA + "/coefficient-two-selftest-frame",
                    "coefficient": 2, "delta_word": prov["delta_word"],
                    "relator_word": prov["relator_word"],
                    "stored_row": record["sparse_row"], "target": runtime["live"].public_sparse(
                        runtime["live"].scaled(runtime["live"].parse_sparse(
                            record["sparse_row"]), 2)),
                    "factor_word": runtime["live"].inverse_word(prov["conjugate_word"]),
                    "correction_word": runtime["live"].inverse_word(prov["conjugate_word"])})
                producer_validate_coefficient_two(runtime, coefficient_baseline)
                value = BoundedOwnerDelta(coefficient_baseline, "positive", name,
                    ("correction_word",), runtime["meter"])
                value["correction_word"].append(1)
                validator = lambda candidate: producer_validate_coefficient_two(runtime, candidate)
                expected = contract[name]
            else:
                runtime["meter"].check("positive_mutation_delta")
                value = BoundedOwnerDelta(baseline, "positive", name,
                    ("selected", "coefficient", "target", "boundary_preimage",
                     "producer_sparse_equality"), runtime["meter"])
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
                    raise ProtocolStop("unknown producer positive mutation")
                validator = lambda candidate: producer_validate_positive(
                    runtime, candidate, recovery)
                expected = contract[name]
            _before, after, reason = _producer_mutation_trace(
                root / f"positive-{ordinal:02d}.json", value, validator,
                trace_runtime=runtime)
            require(reason == expected["first_reason"],
                    "producer positive first reason:" + name + ":" + reason)
            require(_before != after, "producer positive identity unchanged:" + name)
            events = runtime.get("_active_validator_events", [])
            require(events, "producer positive validator event trace")
            terminal_count = int(runtime.get("_terminal_count", 0))
            owner_disposed = bool(runtime.get("_last_owner_disposed"))
            require(terminal_count == 1 and owner_disposed,
                    "producer positive measured terminal/owner:" + name)
            ledger.append({"id": name, "owner_path": expected["owner_path"],
                "identity_kind": "bounded_owner_delta",
                "before_identity": {"kind": "immutable_baseline", "sha256": _before},
                "after_identity": {"kind": "physical_delta", "sha256": after},
                "physical_digest": after, "event_trace": list(events),
                "event_trace_digest": sha_obj(events),
                "entered_validators": [event["validator"] for event in events],
                "first_rejection": {"validator": events[-1]["validator"],
                    "stage": events[-1]["stage"], "narrow_reason": reason},
                "baseline_revalidated": baseline_revalidated,
                "terminal_count": terminal_count,
                "owner_disposed": owner_disposed,
                "validator": events[-1]["validator"],
                "stage": events[-1]["stage"],
                "reseal": expected["reseal"], "before_sha256": _before,
                "after_sha256": after, "reached_validator": events[-1]["validator"],
                "first_reason": reason})
    return ledger


def producer_validate_r_owner(runtime: dict[str, Any],
                              value: dict[str, Any]) -> None:
    """Ordinary SELFTEST R constructor/envelope validator."""
    _producer_validator_event(runtime, "selftest_envelope",
                              "identity_envelope", "actual-R")
    validate_seal(value)
    expected_fields = runtime.get("_producer_r_expected_fields")
    require(type(expected_fields) is set and set(value) == expected_fields and
            value.get("schema") == SCHEMA + "/selftest-bootstrap" and
            value.get("status") == "CANDIDATE_ONLY" and
            value.get("terminal") == SELFTEST_TERMINAL and
            value.get("mode") == "SELFTEST_BOOTSTRAP" and
            value.get("candidate_only") is True and
            value.get("production_authorized") is False and
            value.get("requires_v12c_physical_pin") is True and
            value.get("claims") == FALSE_CLAIMS and
            value.get("no_acceptance_or_negative_claim") is True and
            "checkpoint" not in value,
            "SELFTEST identity envelope")
    require(value.get("p0") == runtime.get("p0_identity") and
            value.get("source_snapshots") == runtime.get("source_snapshots") and
            value.get("selftest", {}).get(
                "actual_r_publication_binding") == {
                    "path": R_OUTPUT_PATH,
                    "maximum_bytes": MAX_CANDIDATE_BYTES,
                    "exclusive_no_replace": True,
                    "rollback_directory_fsync": True},
            "SELFTEST identity envelope")


def producer_physical_mutations_v297(runtime: dict[str, Any],
                                     receipt_owner: dict[str, Any],
                                     fixture: dict[str, Any]) -> list[dict[str, Any]]:
    """Mutate the actual constructed R owner and its publication binding."""
    baseline = receipt_owner
    producer_validate_r_owner(runtime, baseline)
    contract = {row["id"]: row for row in fixture["mutation_contract"]["physical"]}
    require(list(contract) == fixture["physical_mutations"],
            "producer physical mutation contract")
    base_raw = canonical(baseline) + b"\n"
    base_sha = sha_bytes(base_raw)
    ledger: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="r07-v12c-actual-R-") as directory:
        root = Path(directory)
        base = root / "actual-R.json"
        with base.open("xb") as stream:
            stream.write(base_raw); stream.flush(); os.fsync(stream.fileno())
        baseline_identity = _producer_path_identity(
            base, "actual-R", base_sha)
        for ordinal, name in enumerate(fixture["physical_mutations"]):
            runtime["meter"].check("actual_R_physical_mutation")
            expected = contract[name]
            path = root / f"physical-{ordinal:02d}.json"
            runtime["_active_validator_events"] = []
            runtime["_last_owner_disposed"] = False
            runtime["_terminal_count"] = 0
            runtime["_physical_logical_label"] = name
            runtime["_physical_logical_link_target"] = "actual-R"
            runtime["_physical_baseline_sha256"] = base_sha
            runtime.pop("_physical_projection", None)
            first_identity = baseline_identity
            after_identity: dict[str, Any]
            before_sha = base_sha
            after_sha: str | None = None
            if name in ("symlink_candidate", "hardlink_candidate"):
                try:
                    if name == "symlink_candidate":
                        os.symlink(base, path)
                    else:
                        os.link(base, path)
                except OSError as exc:
                    raise ProtocolStop("physical mutation construction:" + name) from exc
                try:
                    read_bounded_json(path, len(base_raw), runtime["meter"],
                                      trace_runtime=runtime)
                except (InputStop, ProtocolStop) as exc:
                    runtime["_terminal_count"] += 1; reason = str(exc)
                else:
                    raise ProtocolStop("MUTATION_ACCEPTED:" + name)
                after_sha = base_sha
                after_identity = runtime.get("_physical_projection",
                    _producer_path_identity(path, name))
            elif name == "toctou_substitution":
                with path.open("xb") as stream:
                    stream.write(base_raw); stream.flush(); os.fsync(stream.fileno())
                substitute = root / "toctou-new.json"
                with substitute.open("xb") as stream:
                    stream.write(base_raw); stream.flush(); os.fsync(stream.fileno())
                first_identity = _producer_path_identity(path, name, base_sha)
                try:
                    read_bounded_json(path, len(base_raw), runtime["meter"],
                                      lambda target: os.replace(substitute, target),
                                      runtime)
                except (InputStop, ProtocolStop) as exc:
                    runtime["_terminal_count"] += 1; reason = str(exc)
                else:
                    raise ProtocolStop("MUTATION_ACCEPTED:" + name)
                after_sha = base_sha
                after_identity = runtime.get("_physical_projection", {})
            elif name == "stale_output":
                first_identity = _producer_path_identity(path, name)
                atomic_json(path, baseline, maximum=MAX_CANDIDATE_BYTES,
                            trace_runtime=runtime)
                after_identity = _producer_path_identity(path, name, base_sha)
                try:
                    atomic_json(path, baseline, maximum=MAX_CANDIDATE_BYTES,
                                trace_runtime=runtime)
                except ProtocolStop as exc:
                    runtime["_terminal_count"] += 1; reason = str(exc)
                else:
                    raise ProtocolStop("MUTATION_ACCEPTED:" + name)
                after_sha = base_sha
            else:
                value = BoundedOwnerDelta(
                    baseline, "physical", name, ("claims", "terminal"),
                    runtime["meter"])
                if name == "unbound_checkpoint":
                    value["checkpoint"] = {"path": "alien.json"}
                elif name == "positive_claim_on_resource_exit":
                    value["claims"]["common_word"] = True
                elif name in ("separator_flip", "cofinal_flip",
                              "fake_flip", "ihara_flip"):
                    claim = {"separator_flip": "separator",
                             "cofinal_flip": "cofinal_lift",
                             "fake_flip": "fake",
                             "ihara_flip": "ihara_witness"}[name]
                    value["claims"][claim] = True
                elif name == "terminal_reseal":
                    value["terminal"] = "V12C_RESEALED"
                else:
                    raise ProtocolStop("unknown producer physical mutation")
                before_sha, after_sha, reason = _producer_mutation_trace(
                    path, value,
                    lambda candidate: producer_validate_r_owner(runtime, candidate),
                    trace_runtime=runtime)
                after_identity = {"logical_case_path": name,
                    "owner_kind": "bounded_actual_R_delta",
                    "byte_length": None, "content_sha256": after_sha,
                    "canonical_before_sha256": base_sha,
                    "canonical_after_sha256": after_sha,
                    "entered_validators": [event["validator"] for event in
                                           runtime.get("_active_validator_events", [])],
                    "event_trace_digest": sha_obj(runtime.get(
                        "_active_validator_events", [])),
                    "first_typed_rejection": reason}
            try: path.unlink()
            except FileNotFoundError: pass
            runtime["_last_owner_disposed"] = not path.exists()
            events = list(runtime.get("_active_validator_events", []))
            require(events and reason == expected["first_reason"],
                    "producer physical first reason:" + name + ":" + reason)
            terminal_count = int(runtime.get("_terminal_count", 0))
            require(terminal_count == 1 and runtime["_last_owner_disposed"],
                    "producer physical measured terminal/owner:" + name)
            producer_validate_r_owner(dict(runtime,
                _active_validator_events=[]), baseline)
            rejection = events[-1]
            ledger.append({"id": name, "group": "physical",
                "owner_path": expected["owner_path"],
                "identity_kind": after_identity.get("owner_kind", "path"),
                "before_identity": first_identity,
                "after_identity": after_identity,
                "physical_digest": after_sha,
                "event_trace": list(events),
                "event_trace_digest": sha_obj(events),
                "entered_validators": [event["validator"] for event in events],
                "first_rejection": {"validator": rejection["validator"],
                    "stage": rejection["stage"], "narrow_reason": reason},
                "baseline_revalidated": True,
                "terminal_count": terminal_count, "owner_disposed": True,
                "validator": rejection["validator"], "stage": rejection["stage"],
                "reseal": expected["reseal"], "before_sha256": before_sha,
                "after_sha256": after_sha,
                "reached_validator": rejection["validator"],
                "first_reason": reason})
        base.unlink()
        require(not base.exists(), "actual R baseline disposal")
    return ledger
def producer_validate_phase_transition(runtime: dict[str, Any],
                                       value: dict[str, Any]) -> None:
    """Validate an ordinary runtime transition against its actual owner."""
    _producer_validator_event(runtime, "validate_phase_transition",
                              "transition", "runtime.phase_transition")
    validate_seal(value)
    expected_by_phase = runtime.get("_producer_phase_expected_by_phase")
    require(type(expected_by_phase) is dict, "phase gate")
    phase = value.get("phase")
    expected = expected_by_phase.get(phase)
    if type(expected) is not dict:
        _producer_validator_event(runtime, "validate_phase_transition",
                                  "phase", "runtime.phase_transition.phase")
        raise ProtocolStop("phase gate")
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
            _producer_validator_event(runtime, "validate_phase_transition",
                                      stage, "runtime.phase_transition." + field)
            raise ProtocolStop("phase gate")


def phase_gate_selftest(runtime: dict[str, Any], fixture: dict[str, Any],
                        selected_frame: dict[str, Any]
                        ) -> dict[str, list[dict[str, Any]]]:
    """Mutate extant runtime transitions through one ordinary validator."""
    light_hash = runtime["light_input_sha256"]
    heavy_hash = runtime["heavy_input_sha256"]
    owner_pre_sha = runtime.get("owner_preselection_sha256")
    require(type(owner_pre_sha) is str and len(owner_pre_sha) == 64,
            "phase OwnerPre must be loaded")
    heavy_owner = {"owner_preselection_sha256": owner_pre_sha,
                   "q0_order": int(runtime["heavy_public"]["q0_order"]),
                   "gamma_order": int(runtime["heavy_public"]["gamma_order"]),
                   "selected_k0_algorithm":
                       "v12c-coarse-open-address-retained-full-state-first-gid-bfs"}
    heavy_owner_sha = sha_obj(heavy_owner)
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
    runtime["_producer_phase_expected_by_phase"] = {
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
            "producer phase mutation contract")
    baseline_revalidated = False
    producer_validate_phase_transition(runtime, baseline)
    baseline_revalidated = True
    rows = []
    with tempfile.TemporaryDirectory(prefix="r07-v12c-producer-phase-") as directory:
        root = Path(directory)
        for ordinal, name in enumerate(fixture["phase_mutations"]):
            runtime["meter"].check("phase_mutation_delta")
            value = BoundedOwnerDelta(baseline, "phase", name,
                ("heavy_input_sha256", "heavy_complete", "correction_progress",
                 "zero_is_negative"), runtime["meter"])
            actions[name](value); expected = contract[name]
            before, after, reason = _producer_mutation_trace(
                root / f"phase-{ordinal:02d}.json", value,
                lambda candidate: producer_validate_phase_transition(
                    runtime, candidate), trace_runtime=runtime)
            require(reason == expected["first_reason"],
                    "producer phase first reason:" + name + ":" + reason)
            require(before != after, "producer phase identity unchanged:" + name)
            events = runtime.get("_active_validator_events", [])
            require(events, "producer phase validator event trace")
            terminal_count = int(runtime.get("_terminal_count", 0))
            owner_disposed = bool(runtime.get("_last_owner_disposed"))
            require(terminal_count == 1 and owner_disposed,
                    "producer phase measured terminal/owner:" + name)
            rows.append({"id": name, "owner_path": expected["owner_path"],
                "identity_kind": "bounded_owner_delta",
                "before_identity": {"kind": "immutable_baseline", "sha256": before},
                "after_identity": {"kind": "physical_delta", "sha256": after},
                "physical_digest": after,
                "event_trace": list(events),
                "event_trace_digest": sha_obj(events),
                "entered_validators": [event["validator"] for event in events],
                "first_rejection": {"validator": events[-1]["validator"],
                    "stage": events[-1]["stage"], "narrow_reason": reason},
                "baseline_revalidated": baseline_revalidated,
                "terminal_count": terminal_count,
                "owner_disposed": owner_disposed,
                "validator": events[-1]["validator"],
                "stage": events[-1]["stage"],
                "reseal": expected["reseal"], "before_sha256": before,
                "after_sha256": after, "reached_validator": events[-1]["validator"],
                "first_reason": reason})
        gates = {"light_resource_checkpoint": light_gate,
                 "heavy_transition": heavy_gate}
        gate_contract = {row["id"]: row for row in fixture[
            "mutation_contract"]["phase_positive_gates"]}
        require(list(gate_contract) == fixture["phase_positive_gates"],
                "producer phase positive-gate contract")
        positive_gates = []
        for ordinal, name in enumerate(fixture["phase_positive_gates"]):
            runtime["meter"].check("phase_positive_validation")
            expected = gate_contract[name]; value = gates[name]
            runtime["_active_validator_events"] = []
            runtime["_last_owner_disposed"] = False
            ordinary_pass = False
            path = root / f"phase-positive-{ordinal:02d}.json"
            raw = canonical(value) + b"\n"
            try:
                with path.open("xb") as stream:
                    stream.write(raw); stream.flush(); os.fsync(stream.fileno())
                candidate, physical = read_bounded_json(
                    path, len(raw), None, trace_runtime=runtime)
                producer_validate_phase_transition(runtime, candidate)
                ordinary_pass = True
                digest = physical["sha256"]
            finally:
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass
            events = runtime.get("_active_validator_events", [])
            require(events and candidate == gates[name] and not path.exists(),
                    "producer phase positive-gate trace")
            gate_event = events[-1]
            positive_gates.append({"id": name, "owner_path": expected["owner_path"],
                "validator": gate_event["validator"],
                "stage": gate_event["stage"],
                "reseal": expected["reseal"], "positive_gate": True,
                "ordinary_pass": ordinary_pass,
                "before_identity": {"sha256": digest},
                "after_identity": {"sha256": digest},
                "physical_digest": digest,
                "event_trace": list(events),
                "event_trace_digest": sha_obj(events),
                "entered_validators": [event["validator"] for event in events],
                "baseline_revalidated": baseline_revalidated,
                "terminal_count": 0, "owner_disposed": not path.exists(),
                "first_rejection": None, "first_reason": None,
                "positive_gate_evidence": "ordinary pass; no terminal counter"})
    return {"mutations": rows, "positive_gates": positive_gates}


MUTATION_GROUP_ORDER = ("triangular", "boundary", "selected_correction",
                        "positive", "physical", "phase", "phase_positive")
MUTATION_GROUP_COUNTS = {"triangular": 8, "boundary": 13,
    "selected_correction": 30, "positive": 7, "physical": 11,
    "phase": 4, "phase_positive": 2}


def finalize_complete_mutation_ledger(fixture: dict[str, Any],
                                      groups: dict[str, list[dict[str, Any]]]
                                      ) -> tuple[list[dict[str, Any]], str]:
    require(tuple(groups) == MUTATION_GROUP_ORDER and
            all(len(groups[group]) == MUTATION_GROUP_COUNTS[group]
                for group in MUTATION_GROUP_ORDER),
            "complete mutation ledger group counts")
    complete: list[dict[str, Any]] = []
    for group in MUTATION_GROUP_ORDER:
        contract_key = "phase_positive_gates" if group == "phase_positive" else group
        contract = fixture["mutation_contract"][contract_key]
        for row, expected in zip(groups[group], contract):
            require(row.get("id") == expected.get("id") and
                    row.get("owner_path") == expected.get("owner_path") and
                    row.get("validator") == expected.get("validator") and
                    row.get("stage") == expected.get("stage") and
                    row.get("reseal") is expected.get("reseal") and
                    row.get("first_reason") == expected.get("first_reason"),
                    "complete mutation measured contract:" + group)
            measured = dict(row); measured["group"] = group
            measured.setdefault("physical_digest", row.get("after_sha256") or
                                row.get("after_identity", {}).get("sha256"))
            measured.setdefault("terminal_count", 0 if group ==
                                "phase_positive" else 1)
            measured.setdefault("owner_disposed", True)
            require(type(measured.get("before_identity")) is dict and
                    type(measured.get("after_identity")) is dict and
                    type(measured.get("event_trace_digest")) is str and
                    len(measured["event_trace_digest"]) == 64 and
                    type(measured.get("event_trace")) is list and
                    sha_obj(measured["event_trace"]) ==
                        measured["event_trace_digest"] and
                    type(measured.get("entered_validators")) is list and
                    type(measured.get("physical_digest")) is str and
                    len(measured["physical_digest"]) == 64 and
                    measured.get("terminal_count") == (0 if group ==
                        "phase_positive" else 1) and
                    measured.get("owner_disposed") is True,
                    "complete mutation measured identities:" + group)
            complete.append(measured)
    require(len(complete) == 75, "complete mutation ledger 75")
    return complete, sha_obj(complete)


def run_real_owner_selftest(runtime: dict[str, Any], old_value: dict[str, Any],
                            reducer: FormalReducer, registry: SourceRegistry,
                            processes: dict[str, Any]) -> dict[str, Any]:
    fixture = registry.json("fixture")
    fixture_body = dict(fixture)
    fixture_claim = fixture_body.pop("self_digest_sha256", None)
    require(fixture.get("schema") ==
            "d972-r07-history-free-positive-fast-resume/selftest-input/v12c" and
            fixture.get("worker_counts") == [2, 4] and
            fixture.get("claims") == FALSE_CLAIMS and
            fixture.get("expected_first_checkpoint") == {
                "columns": 2896, "rank": 2896, "boundary_columns": 2896,
                "correction_columns": 0, "raw_support_total": 20354,
                "raw_support_max": 12, "ancestry_entries_total": 137926,
                "ancestry_entries_max": 258,
                "ancestry_weighted_contributions": 1011460,
                "pivot_support_total": 289774, "pivot_support_max": 522,
                "first_dual_support": 1188,
                "first_dual_matching_descriptors": 4,
                "first_dual_pairs": 4752} and
            type(fixture_claim) is str and fixture_claim == sha_obj(fixture_body) and
            fixture.get("p5_p6_chronological_witness", {}).get(
                "validator_semantics") == "chronological-seen-pivots-only" and
            fixture.get("resource_deadline_platform_contract", {}).get(
                "external_sum_seconds") == 17100,
            "selftest fixture envelope")
    require(type(fixture.get("mutation_contract")) is dict and
            all(type(fixture["mutation_contract"].get(group)) is list
                for group in ("triangular", "boundary", "selected_correction",
                              "positive", "physical", "phase",
                              "phase_positive_gates")),
            "selftest mutation contract envelope")
    require(fixture.get("mutation_contract_complete_case_count") == 75 and
            fixture.get("complete_ledger_groups") == {
                "triangular": 8, "boundary": 13,
                "selected_correction": 30, "positive": 7,
                "physical": 11, "phase": 4,
                "phase_positive_gates": 2} and
            fixture.get("complete_ledger_required_fields") == [
                "id", "group", "owner_path", "before_identity",
                "after_identity", "event_trace_digest", "physical_digest",
                "first_rejection", "terminal_count", "owner_disposed"] and
            fixture.get("owner_requirements", {}).get(
                "bounded_owner_local_delta_views") is True and
            fixture.get("owner_requirements", {}).get(
                "exactly_two_full_gamma_values_per_process") is True and
            fixture.get("owner_requirements", {}).get(
                "real_w4_all_fault_routes") is True and
            fixture.get("owner_requirements", {}).get("k0_capacity") ==
                K0_CAPACITY,
            "selftest complete measured owner contract")
    triangular_owner_frame = _triangular_subset_frame(old_value, runtime["live"])
    triangular = triangular_mutation_selftest(
        old_value, runtime["live"], fixture["triangular_mutations"],
        fixture["mutation_contract"]["triangular"], triangular_owner_frame,
        runtime["meter"])
    require(type(processes) is dict and processes.get("actual_process_owner") is True,
            "pre-heavy process owner selftest required")
    selected_frame = _producer_correction_selftest_frame(runtime, reducer, registry)
    selected_frame["source_snapshots"] = registry.public()
    runtime["source_snapshots"] = registry.public()
    # Freeze the one selected coordinate's immutable table metadata before
    # constructing H; later mutation cases read this snapshot and never
    # trigger a payload rescan.
    runtime["heavy_public"]["coarse_indices"] = runtime[
        "fibres"].index_public()
    # ``coarse_indices`` is part of the diagnostic RunPre carrier that is
    # sealed into every ordinary positive frame.  The selected-owner search
    # above necessarily builds this one table after the initial light/heavy
    # summary was assembled, so refresh the carrier hash and frame together;
    # otherwise the ordinary seal validator would compare a post-build object
    # with a pre-build digest.
    runtime["heavy_input_sha256"] = sha_obj(runtime["heavy_public"])
    selected_frame["heavy_public"] = runtime["heavy_public"]
    selected_frame["heavy_input_sha256"] = runtime["heavy_input_sha256"]
    selected_frame = seal(selected_frame)
    # Build the load-bearing preselection owner from task176 bytes before H;
    # this is intentionally separate from the diagnostic RunPre object.
    producer_build_owner_preselection(runtime, registry)
    final_heavy = producer_final_heavy_identity(runtime, selected_frame, registry)
    selected_frame["final_heavy_carrier"] = final_heavy["public"]
    selected_frame["h_final"] = final_heavy["sha256"]
    selected_frame["final_heavy_identity_public"] = final_heavy["public"]
    selected_frame["final_heavy_identity_sha256"] = final_heavy["sha256"]
    selected_frame = seal(selected_frame)
    selected_ledger = producer_selected_correction_mutations(
        runtime, selected_frame, fixture, registry)
    positive_ledger = producer_positive_mutations(
        runtime, selected_frame, fixture, registry)
    physical_ledger: list[dict[str, Any]] = []
    boundary_ledger = producer_boundary_mutations(runtime, processes, fixture)
    phase_result = phase_gate_selftest(runtime, fixture, selected_frame)
    phases = phase_result["mutations"]
    phase_positive_gates = phase_result["positive_gates"]
    selected_coordinate = int(selected_frame["record"]["provenance"][
        "section_provenance"]["coordinate"])
    selected_index = runtime["fibres"].coarse_indices.get(selected_coordinate)
    require(selected_index is not None and selected_index.build_count == 1,
            "producer K0 lifecycle selected build")
    release_public = {"coordinate": selected_coordinate,
        "build_count": selected_index.build_count,
        "state_digest": selected_index.state_digest(),
        "slot_digest": selected_index.slot_digest(),
        "public_digest": selected_index.public_digest(),
        "payload_bytes": selected_index.state_count * selected_index.width +
            K0_CAPACITY * 4}
    runtime["fibres"].release_coordinate(selected_coordinate)
    require(selected_coordinate in runtime["fibres"].released_indices,
            "producer K0 lifecycle release")
    measured_groups_without_physical = {
        "triangular": triangular, "boundary": boundary_ledger,
        "selected_correction": selected_ledger, "positive": positive_ledger,
        "phase": phases, "phase_positive": phase_positive_gates}
    released_store_bytes = sum(len(store) for store in runtime["stores"])
    released_membership_bytes = sum(len(bits) for bits in
                                    runtime["memberships"].values())
    released_qstate_count = len(runtime["qstates"])
    for store in runtime["stores"]:
        store.clear()
    runtime["stores"].clear(); runtime["qstates"].clear(); runtime["qids"].clear()
    runtime["parents"].clear(); runtime["memberships"].clear()
    runtime["A_maps"].clear(); runtime["projected"].clear()
    runtime.get("_selected_replay_cache", {}).clear()
    runtime["letters"] = b""
    release_large = {"q0_store_bytes": released_store_bytes,
        "membership_bytes": released_membership_bytes,
        "q0_state_count": released_qstate_count,
        "ten_coordinate_stores_released": True,
        "q0_roster_and_parent_walk_released": True,
        "membership_and_projection_released": True}
    return {"fixture_sha256": SOURCE_PINS["fixture"][2],
            "triangular_mutations": triangular,
            "process_owner": processes, "phase_mutations": phases,
            "phase_positive_gates": phase_positive_gates,
            "selected_correction_seed": selected_frame,
            "triangular_owner_baseline_sha256": triangular[0]["before_sha256"],
            "triangular_mutation_ledger": triangular,
            "boundary_mutation_ledger": boundary_ledger,
            "selected_correction_mutation_ledger": selected_ledger,
            "positive_mutation_ledger": positive_ledger,
            "physical_mutation_ledger": [],
            "complete_mutation_ledger": [],
            "complete_mutation_ledger_sha256": None,
            "mutation_groups_without_physical": measured_groups_without_physical,
            "phase_mutation_ledger": phases,
            "phase_positive_gate_ledger": phase_positive_gates,
            "k0_lifecycle": {"built": runtime["heavy_public"][
                "coarse_indices"], "released": release_public,
                "build_bound": 1, "release_after_mutations": True},
            "phase_release": release_large,
            "resource_model": dict(RESOURCE_MODEL),
            "deadline_model": dict(DEADLINE_MODEL),
            "mutation_contract_sha256": sha_obj(fixture["mutation_contract"]),
            "real_owner_not_shaped_transcript": True}


def exclusive_json(path: Path, value: dict[str, Any],
                   meter: Meter | None = None) -> tuple[int, str]:
    return atomic_json(path, value, maximum=MAX_CANDIDATE_BYTES, meter=meter)


def validate_p0_manifest(value: dict[str, Any]) -> None:
    """Validate the semantic P0 contract before loading any heavy owner."""
    require(value.get("schema") == P0_SCHEMA, "v12c P0 schema")
    require(value.get("mode") == "SELFTEST_BOOTSTRAP" and
            value.get("status") == "COMPLETE" and
            value.get("execution") == "UNEXECUTED" and
            value.get("candidate_only") is True and
            value.get("production_authorized") is False and
            value.get("resume_authorized") is False and
            value.get("acceptance_preregistration") is False and
            value.get("requires_v12c_physical_pin") is True,
            "v12c P0 bootstrap envelope")
    require(value.get("manifest_path") ==
            "ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.manifest.v1.json",
            "v12c P0 path")
    require(value.get("platform_contract", {}).get("gha_runner") ==
                "ubuntu-24.04" and
            value.get("platform_contract", {}).get(
                "typed_preflight_before_heavy_load") is True and
            value.get("deadline_contract") == DEADLINE_MODEL and
            value.get("resource_contract", {}).get(
                "producer_explicit_payload_peak_bytes") ==
                PRODUCER_EXPLICIT_PAYLOAD_PEAK and
            value.get("resource_contract", {}).get(
                "candidate_output_hard_cap_bytes") == MAX_CANDIDATE_BYTES,
            "v12c P0 platform/resource/deadline contract")
    prospective = value.get("prospective_outputs")
    require(type(prospective) is dict and
            prospective.get("R", {}).get("sha256") ==
            "TO_BE_GENERATED_BY_AUDITED_V12C_SELFTEST" and
            prospective.get("V", {}).get("sha256") ==
            "TO_BE_GENERATED_BY_AUDITED_V12C_SELFTEST",
            "v12c prospective identity gate")
    sources = value.get("sources")
    require(type(sources) is dict and sources == {},
            "v12c P0 must not pin final producer/checker owners")
    frozen = value.get("frozen_authorities")
    expected_frozen: dict[str, tuple[str, int, str]] = dict(SOURCE_PINS)
    expected_frozen.update({
        "raw_checkpoint": (RAW_SOURCE_PATH, RAW_BYTES, RAW_SHA256),
        "checkpoint_archive": (RAW_ARCHIVE_PATH, RAW_ARCHIVE_BYTES,
                                RAW_ARCHIVE_SHA256)})
    require(type(frozen) is dict and set(frozen) == set(expected_frozen),
            "v12c P0 frozen authority roster")
    physical_paths = [str(row.get("path")) for row in frozen.values()]
    require(len(physical_paths) == len(set(physical_paths)),
            "v12c duplicate physical authority path")
    for key, (path, size, digest) in expected_frozen.items():
        row = frozen[key]
        require(type(row) is dict and row.get("path") == path and
                row.get("bytes") == size and row.get("sha256") == digest,
                "v12c P0 frozen authority row:" + key)
    claimed = value.get("self_digest_sha256")
    body = dict(value)
    body.pop("self_digest_sha256", None)
    require(type(claimed) is str and claimed == sha_obj(body),
            "v12c P0 self seal")


def validate_p0_source_graph(value: dict[str, Any], meter: Meter
                             ) -> dict[str, Any]:
    """Bind every P0 source row to the final regular file before heavy load."""
    authenticated: dict[str, tuple[bytes, dict[str, Any]]] = {}
    def snapshot(row: dict[str, Any]) -> tuple[bytes, dict[str, Any]]:
        relative = str(row["path"])
        if relative not in authenticated:
            authenticated[relative] = read_physical_once(
                ROOT / relative, int(row["bytes"]), str(row["sha256"]), meter)
        raw0, physical0 = authenticated[relative]
        require(len(raw0) == row["bytes"] and
                physical0["sha256"] == row["sha256"],
                "v12c shared physical snapshot:" + relative)
        return raw0, physical0
    for key, row in value["sources"].items():
        raw, physical = snapshot(row)
        require(physical["sha256"] == row["sha256"] and
                len(raw) == row["bytes"], "v12c P0 physical source:" + key)
    for key, row in value["frozen_authorities"].items():
        raw, physical = snapshot(row)
        require(physical["sha256"] == row["sha256"] and
                len(raw) == row["bytes"],
                "v12c P0 physical frozen authority:" + key)
    return {"source_raws": {key: authenticated[row[0]][0]
                            for key, row in SOURCE_PINS.items()},
            "raw_checkpoint": authenticated[RAW_SOURCE_PATH][0]}


def validate_owned_paths(output: Path, source: Path) -> None:
    """Accept only the preregistered repository transport identities."""
    expected_output = (ROOT / R_OUTPUT_PATH).resolve()
    expected_source = (ROOT / RAW_SOURCE_PATH).resolve()
    # Resolve equality alone accepts a symlink/reparse at the caller's path.
    # The owned transport is a lexical repository path whose final component
    # is a regular, singly-linked file; no alternate path may be substituted.
    require(output.absolute() == expected_output,
            "v12c receipt path is not preregistered")
    require(source.absolute() == expected_source,
            "v12c raw source path is not preregistered")
    output_dir = ROOT / "ci/out"
    require(output_dir.is_dir() and not output_dir.is_symlink(),
            "v12c output directory identity")
    try:
        source_stat = os.lstat(source)
    except OSError as exc:
        raise InputStop("v12c raw source path unavailable") from exc
    require(stat.S_ISREG(source_stat.st_mode) and source_stat.st_nlink == 1,
            "v12c raw source must be a unique regular owner")
    if os.path.lexists(str(output)):
        output_stat = os.lstat(output)
        require(stat.S_ISREG(output_stat.st_mode) and
                output_stat.st_nlink == 1,
                "v12c receipt output identity")
    for relative in OUTPUT_SIBLINGS:
        target = ROOT / relative
        require(not os.path.lexists(str(target)), "stale v12c transport:" + relative)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="v12c SELFTEST_BOOTSTRAP producer")
    value.add_argument("--mode", choices=("SELFTEST_BOOTSTRAP",), required=True)
    value.add_argument("--source", type=Path, required=True)
    value.add_argument("--manifest", type=Path, required=True)
    value.add_argument("--output", type=Path, required=True)
    value.add_argument("--seconds", type=float, required=True)
    value.add_argument("--workers", type=int, choices=(2, 4), default=4)
    return value


def platform_preflight() -> None:
    require(sys.platform == "linux" and os.name == "posix" and
            "fork" in multiprocessing.get_all_start_methods() and
            hasattr(socket, "AF_UNIX") and hasattr(os, "O_NOFOLLOW") and
            Path("/proc/self/statm").is_file(),
            "typed platform preflight:ubuntu-linux-fork-af_unix-nofollow-proc")


def _bounded_main(args: argparse.Namespace,
                  address_limit: dict[str, int]) -> int:
    require(args.mode == "SELFTEST_BOOTSTRAP",
            "production/resume entry point is forbidden")
    output = args.output if args.output.is_absolute() else ROOT / args.output
    source_path = args.source if args.source.is_absolute() else ROOT / args.source
    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    require(manifest_path.resolve() == P0_PATH.resolve(),
            "v12c P0 manifest required")
    validate_owned_paths(output, source_path)
    meter = Meter(args.seconds)
    meter.reserve_live("payload_bytes", PRODUCER_PAYLOAD_WITHOUT_OUTPUT,
                       "pre_material_payload_reservation")
    p0, p0_physical = read_bounded_json(P0_PATH, P0_BYTES, meter)
    require(p0_physical["bytes"] == P0_BYTES and
            p0_physical["sha256"] == P0_SHA256 and
            p0.get("self_digest_sha256") == P0_SELF_DIGEST,
            "v12c exact canonical P0 physical pin")
    validate_p0_manifest(p0)
    snapshots = validate_p0_source_graph(p0, meter)
    p0_relative = str(P0_PATH.relative_to(ROOT)).replace("\\", "/")
    p0_identity = {"path": p0_relative, "bytes": p0_physical["bytes"],
                   "sha256": p0_physical["sha256"],
                   "self_digest_sha256": p0["self_digest_sha256"]}
    registry = SourceRegistry(snapshots["source_raws"])
    snapshots["source_raws"].clear()
    registry.authenticate(meter)
    fixture, fixture_physical = read_bounded_json(
        ROOT / FIXTURE_PATH, FIXTURE_BYTES, meter)
    require(fixture == registry.json("fixture") and
            fixture_physical["sha256"] == FIXTURE_SHA256 and
            fixture.get("self_digest_sha256") == FIXTURE_SELF_DIGEST,
            "v12c exact canonical fixture physical pin")
    canonical_mutations = canonical_reader_mutation_selftest(p0, fixture, meter)
    require(registry.json("manifest") == EXPECTED_MANIFEST,
            "frozen physical checkpoint manifest")
    raw = snapshots["raw_checkpoint"]
    try:
        old_value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise InputStop("source_json") from exc
    source_public = {
        "path": str(source_path.relative_to(ROOT)).replace("\\", "/")
        if source_path.is_relative_to(ROOT) else str(source_path),
        "member": RAW_MEMBER, "bytes": RAW_BYTES, "sha256": RAW_SHA256,
        "parsed_once": True}
    del raw
    snapshots["raw_checkpoint"] = None
    runtime = build_light(registry, meter)
    runtime["p0_identity"] = p0_identity
    runtime["p0_sources"] = p0["sources"]
    runtime["p0_frozen_authorities"] = p0["frozen_authorities"]
    runtime["address_space_limit"] = address_limit
    try:
        validate_old_envelope(old_value, runtime["live"])
        reducer, p_rows, triangular = build_triangular(old_value, runtime, meter)
        p_rows.clear(); del p_rows
    except ResourceStop:
        raise
    except (ProtocolStop, RuntimeError, ValueError, TypeError,
            IndexError, KeyError) as exc:
        raise InputStop("v12c_triangular_gate") from exc
    meter.check("v12c_light_basis_complete")
    processes = process_selftest(runtime, reducer, fixture, meter)
    build_heavy(runtime, registry, meter)
    selftest = run_real_owner_selftest(runtime, old_value, reducer, registry,
                                       processes)
    old_value.clear()
    selftest["canonical_reader_mutations"] = canonical_mutations
    selftest["source_snapshot_release"] = registry.release_snapshots()
    selftest["actual_r_publication_binding"] = {
        "path": R_OUTPUT_PATH, "maximum_bytes": MAX_CANDIDATE_BYTES,
        "exclusive_no_replace": True, "rollback_directory_fsync": True}
    selftest["address_space_limit"] = address_limit
    meter.reserve_live("output_bytes", MAX_CANDIDATE_BYTES,
                       "full_R_output_cap_before_construction")
    receipt_body = {
        "schema": SCHEMA + "/selftest-bootstrap",
        "status": "CANDIDATE_ONLY", "terminal": SELFTEST_TERMINAL,
        "mode": "SELFTEST_BOOTSTRAP", "candidate_only": True,
        "production_authorized": False,
        "requires_v12c_physical_pin": True,
        "execution": "SELFTEST_BOOTSTRAP_COMPLETE_CANDIDATE",
        "p0": p0_identity, "source": source_public,
        "source_snapshots": registry.public(), "p0_sources": p0["sources"],
        "frozen_authorities": p0["frozen_authorities"],
        "triangular_certificate": triangular,
        "light_input_sha256": runtime["light_input_sha256"],
        "heavy_input_sha256": runtime["heavy_input_sha256"],
        "heavy_public": runtime["heavy_public"],
        "final_heavy_carrier": selftest["selected_correction_seed"][
            "final_heavy_carrier"],
        "h_final": selftest["selected_correction_seed"]["h_final"],
        "final_heavy_identity_public": selftest["selected_correction_seed"][
            "final_heavy_carrier"],
        "final_heavy_identity_sha256": selftest["selected_correction_seed"][
            "h_final"],
        "selftest": selftest, "claims": dict(FALSE_CLAIMS),
        "production_and_resume": "FORBIDDEN_PENDING_INDEPENDENT_AUDIT",
        "no_acceptance_or_negative_claim": True}
    runtime["_producer_r_expected_fields"] = set(
        p0["constructors"]["R"]["deterministic_field_set"]) | {
            "semantic_digest", "self_digest"}
    provisional_body = dict(receipt_body)
    provisional_body["semantic_digest"] = sha_obj(provisional_body)
    provisional_r = seal(provisional_body)
    physical_ledger = producer_physical_mutations_v297(
        runtime, provisional_r, fixture)
    selftest["physical_mutation_ledger"] = physical_ledger
    partial = selftest.pop("mutation_groups_without_physical")
    complete_groups = {
        "triangular": partial["triangular"],
        "boundary": partial["boundary"],
        "selected_correction": partial["selected_correction"],
        "positive": partial["positive"],
        "physical": physical_ledger,
        "phase": partial["phase"],
        "phase_positive": partial["phase_positive"]}
    complete, complete_sha = finalize_complete_mutation_ledger(
        fixture, complete_groups)
    selftest["complete_mutation_ledger"] = complete
    selftest["complete_mutation_ledger_sha256"] = complete_sha
    receipt_body["semantic_digest"] = sha_obj(receipt_body)
    final_r = seal(receipt_body)
    producer_validate_r_owner(runtime, final_r)
    exclusive_json(output, final_r, meter=meter)
    print(PRODUCER_PREFIX + " " + SELFTEST_TERMINAL, flush=True)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    require(args.mode == "SELFTEST_BOOTSTRAP" and args.seconds == WALL_SECONDS,
            "v12c producer SELFTEST_BOOTSTRAP/9600 envelope")
    platform_preflight()
    address_limit = install_address_space_limit()
    with ElapsedSignalDeadline(WALL_SECONDS):
        return _bounded_main(args, address_limit)


def rollback_owned_output(path: Path) -> None:
    """Best-effort nonaccepting rollback with a directory fsync per removal."""
    directory_fd = os.open(path.parent, os.O_RDONLY |
        getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
    failures: list[str] = []
    try:
        for name in (path.name, path.name + f".tmp.{os.getpid()}"):
            try:
                os.unlink(name, dir_fd=directory_fd); os.fsync(directory_fd)
            except FileNotFoundError:
                pass
            except BaseException as exc:
                failures.append(type(exc).__name__)
    finally:
        os.close(directory_fd)
    if failures:
        raise ProtocolStop("rollback owned output failure:" + ",".join(failures))

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (InputStop, ResourceStop) as exc:
        candidate = ROOT / R_OUTPUT_PATH
        try: rollback_owned_output(candidate)
        except BaseException: pass
        terminal = ("UNKNOWN_PLATFORM" if str(exc).startswith(
                    "typed platform preflight") else
                    "UNKNOWN_INPUT" if isinstance(exc, InputStop) else
                    "UNKNOWN_RESOURCE:" + exc.phase + ":" + exc.cap)
        print("V12C_PRODUCER_UNKNOWN " + terminal,
              file=sys.stderr, flush=True)
        raise SystemExit(3)
    except (ProtocolStop, SelftestReject, KeyError, TypeError, ValueError,
            AssertionError) as exc:
        try: rollback_owned_output(ROOT / R_OUTPUT_PATH)
        except BaseException: pass
        print("V12C_PRODUCER_STOP REJECTED",
              file=sys.stderr, flush=True)
        raise
