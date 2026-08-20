"""One lexicographically-first full D2 block, then the target-6 affine test.

This lane rebuilds every private object.  Frozen predecessors supply typed
arithmetic implementations, never a basis, pool, remainder, dual, or verdict.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Sequence

try:
    import resource
except ImportError:  # pragma: no cover - Windows fixture path
    resource = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157ei_b345_lexfirst_block_target6.md")
TASK_SHA = "cfe0c50046a750e4169c473872c5770ce76c105267353e82c9ed19de01c043f4"
TASK_BYTES = 24179
SCHEMA = "d972-b345-lexfirst-block-target6/v1"
OUTPUT = Path("ci/out/d972_b345_lexfirst_block_target6_v1.json")
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"

EH_PRODUCER = Path("search/d972_b345_full_d2_dual_correlation_v2.py")
EH_PRODUCER_SHA = "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f"
EH_PRODUCER_BYTES = 42449
EH_CHECKER = Path("search/check_d972_b345_full_d2_dual_correlation_v2.py")
EH_CHECKER_SHA = "881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060"
EH_CHECKER_BYTES = 21933
EH_DRIVER = Path("search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g")
EH_DRIVER_SHA = "5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde"
EH_DRIVER_BYTES = 13253
EH_TASK = Path("sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md")
EH_TASK_SHA = "5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e"
EH_TASK_BYTES = 15015

EC_PRODUCER = Path("search/d972_b345_seedspan_triple4_v1.py")
EC_PRODUCER_SHA = "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"
EC_PRODUCER_BYTES = 535219
EC_CHECKER = Path("search/check_d972_b345_seedspan_triple4_v1.py")
EC_CHECKER_SHA = "ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981"
EC_CHECKER_BYTES = 574347
EC_DRIVER = Path("search/d972_b345_seedspan_triple4_gha_driver_v1.g")
EC_DRIVER_SHA = "a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4"
EC_DRIVER_BYTES = 9041
EC_TASK = Path("sol/luna_task_157ec_b345_seedspan_triple4.md")
EC_TASK_SHA = "1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2"
EC_TASK_BYTES = 14751

Q3_PRODUCER = Path("search/d972_b345_q3_chief_v1.g")
Q3_PRODUCER_SHA = "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755"
Q3_CHECKER = Path("search/check_d972_b345_q3_chief_v1.py")
Q3_CHECKER_SHA = "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73"
Q3_DRIVER = Path("search/d972_b345_q3_gha_driver_v1.g")
Q3_DRIVER_SHA = "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831"

PIN_SPECS = {
    "157ei_task": (TASK, TASK_SHA, TASK_BYTES),
    "157eh_producer": (EH_PRODUCER, EH_PRODUCER_SHA, EH_PRODUCER_BYTES),
    "157eh_checker": (EH_CHECKER, EH_CHECKER_SHA, EH_CHECKER_BYTES),
    "157eh_driver": (EH_DRIVER, EH_DRIVER_SHA, EH_DRIVER_BYTES),
    "157eh_task": (EH_TASK, EH_TASK_SHA, EH_TASK_BYTES),
    "157ec_producer": (EC_PRODUCER, EC_PRODUCER_SHA, EC_PRODUCER_BYTES),
    "157ec_checker": (EC_CHECKER, EC_CHECKER_SHA, EC_CHECKER_BYTES),
    "157ec_driver": (EC_DRIVER, EC_DRIVER_SHA, EC_DRIVER_BYTES),
    "157ec_task": (EC_TASK, EC_TASK_SHA, EC_TASK_BYTES),
    "q3_producer": (Q3_PRODUCER, Q3_PRODUCER_SHA, None),
    "q3_checker": (Q3_CHECKER, Q3_CHECKER_SHA, None),
    "q3_driver": (Q3_DRIVER, Q3_DRIVER_SHA, None),
}

TERMINALS = frozenset({
    "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT",
    "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT",
    "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE",
    "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT",
})
CAPS = {
    "translation_blocks": 1,
    "relator_columns": 11,
    "affine_variables": 108,
    "affine_rows": 1_000_000,
    "target_live_remainders": 2_000_000,
    "dual_provenance_entries": 128,
    "common_math_soft_deadline_seconds": 18_000,
    "producer_soft_rss_bytes": 4_831_838_208,
    "packed_receipt_bytes": 268_435_456,
}

PREFIX_COUNTS = {"columns": 362725, "pivots": 362709,
    "dependent_columns": 16, "live_sparse_entries": 3090367,
    "row_tail_visits": 2727658, "BFS_translations": 32768,
    "directed_translations": 207}
PREFIX_POOL_CHECKPOINT = 976408
PREFIX_STABLE_SHA = "75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d"
PREFIX_TRANSLATIONS_SHA = "a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f"
PREFIX_COLUMNS_SHA = "cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343"
PREFIX_BLOCKERS_SHA = "b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53"
BASE_OCCURRENCE_SHA = "3eacd6dc77d62c1799a55923d3c8d5313a37ceab8e78b58b07b45925a28f131d"
FIRST_T_HEX = (
    "0001030608070402050d0a0b0e1011090c0f16131417191a1215181b1c1d1e1f"
    "2021222328272625242c2b2a293534333231302f2e2d3c3d3e363738393a3b4140"
    "3f4746454443424d4c4b4a4948504f4e5951525354555657585b5c5d5e5f606162"
    "5a6867666564636b6a696c74737271706f6e6d75767778797a7b7c7d7e7f808182"
    "838485868788898a8b8c8d8e8f00000200000000000000")
FIRST_T_WORD_SHA = "04813137f271cba21b5fdab6b733f0a0ac8ca9daa6b23323e5de55d2b7edba36"
FIRST_G_WORD_SHA = "5e1880d33973be6d67c31110827daf4db55cddf533c4e88354e0c26fbb74a448"
SECTION_MANIFEST_SHA = "aae5341e2f0586069548360b7441d7ebd4fc9550dd752171a8f59ffa3804b073"
CORRELATION_SHA = "8f69ef922a646c0306f2c9ebcf0c8f03531c84b057e29ad4e580a508911c6551"
SEED_MANIFEST_SHA = "17655b21cf526800e751fc5ce5876934de634f3e32d7ba258119138a9828ed80"
OLD_TYPED_SPLIT_SHA = "96e906aaee06d8748dd5c48c9fb3e9d009a185abdee91d8b66f14d545541f545"
OLD_BASE_GRADIENT_SHA = "788fd8712f76a3ca254bb2179b5498fed3ca00e649ba0321ef297d2d985cc71e"
OLD_TARGET6_ROW_SHA = "e99602b0981251e4bb81ab0d2113791563bc9ec9df2a45828aea2880ec6d2f9e"


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True,
        separators=(",", ":")).encode("utf-8"))


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


class InputFailure(RuntimeError):
    pass


def authenticate_static() -> None:
    for label, (path, digest, size) in PIN_SPECS.items():
        full = ROOT/path
        if not full.is_file() or (size is not None and full.stat().st_size != size) \
                or sha_file(full) != digest:
            raise InputFailure(f"authenticated pin drift: {label}")


def pin_rows(q3_path: Path) -> dict[str, Any]:
    rows = {label: {"path": path.as_posix(), "sha256": digest,
                    "bytes": ((ROOT/path).stat().st_size
                              if (ROOT/path).is_file() else None)}
            for label, (path, digest, _) in PIN_SPECS.items()}
    rows["q3_artifact"] = {"path": Q3_PATH.as_posix(), "sha256": Q3_SHA,
        "bytes": q3_path.stat().st_size if q3_path.is_file() else None}
    rows["157ec_run_evidence"] = {"run": "32326652060",
        "receipt_sha256":
            "d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d",
        "evidence_only_not_imported": True}
    rows["157eh_run_evidence"] = {"run": "32374248796",
        "commit": "9e1da3ca55133ae17fe6349bf64e7695fdda14f6",
        "receipt_sha256":
            "7c9de4d4aa5dc0facf94cec9c4b2b71d81c1b8cc590e84aa574cace18c1cb7d5",
        "evidence_only_not_imported": True}
    return rows


_EH_RUNTIME: Any | None = None


def load_eh() -> Any:
    global _EH_RUNTIME
    authenticate_static()
    if _EH_RUNTIME is not None:
        return _EH_RUNTIME
    spec = importlib.util.spec_from_file_location(
        "_d972_157ei_frozen_157eh_producer", ROOT/EH_PRODUCER)
    require(spec is not None and spec.loader is not None,
            "157ei 157eh producer import spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    require(module.SCHEMA == "d972-b345-full-d2-dual-correlation/v2",
            "157ei frozen 157eh schema")
    _EH_RUNTIME = module
    return module


def current_rss() -> int:
    try:
        with open("/proc/self/status", "r", encoding="ascii") as stream:
            for line in stream:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1])*1024
    except (OSError, ValueError, IndexError):
        pass
    if resource is None:
        return 0
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value*1024


_REGISTRY_SOURCE = {
    "authenticated_input": {"authenticated_input"},
    "source_preflight": {"source_preflight", "affine_source_preflight"},
    "fresh_immutable_prefix": {
        "fresh_immutable_prefix", "strong_wform_fresh_BFS",
        "strong_wform_directed_round", "packed_provenance_dag_growth",
        "packed_pivot_column_elimination", "packed_target_sparse_elimination",
        "proof_DAG_array_bytes", "proof_DAG_base64",
        "proof_DAG_base64_complete"},
    "raw_lambda_oracle": {"raw_lambda_oracle", "raw_lambda_reverse_dp"},
    "base_columns": {"base_columns"},
    "dual_correlation": {"dual_correlation"},
    "section_witness": {"section_witness", "proof_DAG_array_bytes",
        "proof_DAG_base64", "proof_DAG_base64_complete"},
    "block_insertion": {"block_insertion", "packed_provenance_dag_growth",
        "packed_pivot_column_elimination", "affine_full_remainder",
        "affine_remainder"},
    "target_reduction": {"target_reduction", "affine_full_remainder",
        "affine_remainder", "affine_transposed_row_absorption"},
    "selected_proof": {"selected_proof", "packed_provenance_dag_growth",
        "packed_target_sparse_elimination", "proof_DAG_pre_serialization_RSS",
        "proof_DAG_reachability", "proof_DAG_compact_serialization",
        "proof_DAG_array_bytes", "proof_DAG_base64",
        "proof_DAG_base64_complete"},
}
MONITOR_REGISTRY = {outer: sorted(inner) for outer, inner in
                    sorted(_REGISTRY_SOURCE.items())}
MONITOR_FROZEN = {outer: frozenset(inner) for outer, inner in
                  _REGISTRY_SOURCE.items()}
MONITOR_SHA = sha_obj(MONITOR_REGISTRY)


class LaneResource(RuntimeError):
    def __init__(self, key: str, limit: int, observed: int, relation: str,
                 phase: str, current: dict[str, Any], *,
                 cap_source: str = "local", inner: str | None = None,
                 callback_api: str | None = None) -> None:
        super().__init__(key)
        require(relation in {"gt", "ge"} and phase in set(MONITOR_FROZEN) |
                {"receipt_serialization"}, "157ei resource phase/comparator")
        if cap_source == "local":
            require(key in CAPS and CAPS[key] == int(limit),
                    "157ei local resource registry")
        else:
            require(cap_source == "upstream", "157ei resource source")
        if inner is not None:
            require(phase in MONITOR_FROZEN and inner in MONITOR_FROZEN[phase]
                    and callback_api in {"check", "reserve"},
                    "157ei callback pair")
        self.key = key; self.limit = int(limit); self.observed = int(observed)
        self.relation = relation; self.phase = phase; self.current = current
        self.cap_source = cap_source; self.inner = inner
        self.callback_api = callback_api

    def public(self) -> dict[str, Any]:
        return {"cap_reason": self.key, "cap_key": self.key,
            "cap_source": self.cap_source, "cap_limit": self.limit,
            "observed_count": self.observed, "comparator": self.relation,
            "phase": self.phase, "current": self.current}

    def diagnostic(self) -> dict[str, str] | None:
        if self.inner is None:
            return None
        return {"outer": self.phase, "inner": self.inner,
                "api": str(self.callback_api)}


class Monitor:
    def __init__(self, seconds: float = 18_000.0) -> None:
        require(0.0 < seconds <= CAPS["common_math_soft_deadline_seconds"],
                "157ei producer deadline")
        self.started = time.monotonic(); self.deadline = self.started+seconds
        self.initial_seconds = float(seconds); self.checks = 0
        self.peak_rss_bytes = 0; self.hit_reason: str | None = None
        self.callback_counts: dict[tuple[str, str, str], int] = defaultdict(int)

    def bind(self, outer: str) -> "BoundMonitor":
        return BoundMonitor(self, outer)

    def _event(self, outer: str, inner: str, api: str,
               force: bool = False, reserve_bytes: int = 0) -> None:
        require(outer in MONITOR_FROZEN and inner in MONITOR_FROZEN[outer] and
                api in {"check", "reserve"}, "157ei exact callback pair")
        self.callback_counts[(outer, inner, api)] += 1; self.checks += 1
        if not force and not reserve_bytes and self.checks & 63:
            return
        rss = current_rss(); self.peak_rss_bytes = max(self.peak_rss_bytes, rss)
        observed = rss+reserve_bytes
        if observed >= CAPS["producer_soft_rss_bytes"]:
            self.hit_reason = "producer_soft_rss_bytes"
            raise LaneResource(self.hit_reason, CAPS[self.hit_reason], observed,
                "ge", outer, {}, inner=inner, callback_api=api)
        if time.monotonic() >= self.deadline:
            self.hit_reason = "common_math_soft_deadline_seconds"
            elapsed = max(CAPS[self.hit_reason],
                          int(time.monotonic()-self.started))
            raise LaneResource(self.hit_reason, CAPS[self.hit_reason], elapsed,
                "ge", outer, {}, inner=inner, callback_api=api)

    def public(self) -> dict[str, Any]:
        return {"initial_remaining_seconds": self.initial_seconds,
            "elapsed_seconds": time.monotonic()-self.started,
            "remaining_seconds": max(0.0, self.deadline-time.monotonic()),
            "checks": self.checks, "peak_rss_bytes": self.peak_rss_bytes,
            "hit_reason": self.hit_reason}


class BoundMonitor:
    __slots__ = ("_base", "_outer", "_sealed")

    def __init__(self, base: Monitor, outer: str) -> None:
        require(type(base) is Monitor and outer in MONITOR_FROZEN,
                "157ei bound monitor")
        object.__setattr__(self, "_base", base)
        object.__setattr__(self, "_outer", outer)
        object.__setattr__(self, "_sealed", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_sealed", False):
            raise AttributeError("157ei bound monitor immutable")
        object.__setattr__(self, name, value)

    @property
    def started(self) -> float:
        return self._base.started

    @property
    def deadline(self) -> float:
        return self._base.deadline

    @property
    def outer(self) -> str:
        return self._outer

    def check(self, inner: str, force: bool = False, **_: Any) -> None:
        self._base._event(self._outer, inner, "check", force)

    def reserve(self, inner: str, additional_bytes: int) -> None:
        require(isinstance(additional_bytes, int) and additional_bytes >= 0,
                "157ei RSS reservation")
        self._base._event(self._outer, inner, "reserve", True,
                          additional_bytes)


def convert_upstream(exc: Any, caps: dict[str, int], phase: str,
                     current: dict[str, Any]) -> LaneResource:
    key = str(getattr(exc, "cap_key", ""))
    reason = str(getattr(exc, "reason", ""))
    limit = int(getattr(exc, "cap_limit", -1))
    observed = int(getattr(exc, "observed_count", -1))
    relation = str(getattr(exc, "trigger_relation", "gt"))
    require(key in caps and caps[key] == limit and reason == key,
            "157ei closed inherited resource")
    return LaneResource(key, limit, observed, relation, phase, current,
                        cap_source="upstream")


def monitor_scope(detached: bool,
                  diagnostic: dict[str, str] | None = None) -> dict[str, Any]:
    return {"contract": "one-clock-exact-outer-inner/v1",
        "registry": MONITOR_REGISTRY, "registry_sha256": MONITOR_SHA,
        "registered_pair_count": sum(map(len, MONITOR_REGISTRY.values())),
        "fresh_adapter_detached_after_prefix": detached,
        "post_stage_adapters_detached": True,
        "resource_callback": diagnostic,
        "wildcards_or_inference_used": False,
        "deadline_or_RSS_epoch_reset": False,
        "receipt_serialization_is_outside_monitor": True}


def theorem_boundary() -> dict[str, Any]:
    return {"pinned_E4_roof_only": True,
        "single_lexfirst_translation_block_only": True,
        "all_old_active_rows_added": False,
        "full_D2_claimed": False, "full_H3_claimed": False,
        "targets_7_through_33_checked": False,
        "typed_lift_claimed": False, "negative_claimed": False,
        "B4_A_claimed": False, "B4_B_claimed": False,
        "inconsistent_is_not_full_D2_obstruction": True,
        "consistent_is_target6_membership_only": True}


def claim_row(token: str, block_complete: bool) -> dict[str, Any]:
    consistent = token == "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT"
    return {"single_lexfirst_translation_block_only": True,
        "complete_11_relator_block": bool(block_complete),
        "all_old_active_rows_added": False, "full_D2_claimed": False,
        "full_H3_claimed": False, "targets_7_through_33_checked": False,
        "typed_lift_claimed": False, "negative_claimed": False,
        "B4_A_claimed": False, "B4_B_claimed": False,
        "target6_membership_in_full_D2_for_selected_correction": consistent,
        "mathematical_claim": ("one_registered_108_seed_correction_has_"
            "target6_boundary_in_B1_subset_full_D2" if consistent else
            "none" if token.endswith(("UNKNOWN_RESOURCE", "UNKNOWN_INPUT"))
            else "no_registered_108_seed_coefficient_solves_target6_mod_B1")}


COMMON_KEYS = {"schema", "task_sha256", "terminal_token", "status",
    "reason", "phase", "pins", "caps", "upstream_caps", "claims",
    "theorem_boundary", "monitor_scope", "resource_guards", "partial",
    "input_errors", "performance"}
AUTH_FIELDS = {"base_q3_replay", "normalized_inverse_fibre", "seed_manifest"}
SOURCE_FIELDS = {"source_preflight"}
PREFIX_FIELDS = {"directed_base_support", "directed_surgery", "prefix"}
LAMBDA_FIELDS = {"lambda_oracle", "lambda_support"}
BASE_FIELDS = {"base_columns"}
CORRELATION_FIELDS = {"correlation", "direct_canaries",
    "state_no_mutation"}
SECTION_FIELDS = {"section_witness"}
BLOCK_FIELDS = {"translation_block", "post_block_anchor"}
TARGET_FIELDS = {"target6"}
AFFINE_FIELDS = {"affine_system"}
PHASE_SEQUENCE = ["authenticated_input", "source_preflight",
    "fresh_immutable_prefix", "raw_lambda_oracle", "base_columns",
    "dual_correlation", "section_witness", "block_insertion",
    "target_reduction", "selected_proof"]


def normal_guard() -> dict[str, Any]:
    return {"resource_hit": False, "resource": None,
            "atomic_partial": True}


def stage_fields_before(phase: str) -> set[str]:
    groups = [AUTH_FIELDS, SOURCE_FIELDS, PREFIX_FIELDS, LAMBDA_FIELDS,
              BASE_FIELDS, CORRELATION_FIELDS, SECTION_FIELDS, BLOCK_FIELDS,
              TARGET_FIELDS, AFFINE_FIELDS]
    boundaries = {"authenticated_input": 0, "source_preflight": 1,
        "fresh_immutable_prefix": 2, "raw_lambda_oracle": 3,
        "base_columns": 4, "dual_correlation": 5,
        "section_witness": 6, "block_insertion": 7,
        "target_reduction": 8, "selected_proof": 10,
        "receipt_serialization": 8}
    require(phase in boundaries, "157ei resource phase registry")
    answer: set[str] = set()
    for group in groups[:boundaries[phase]]:
        answer |= group
    return answer


def expected_keys(receipt: dict[str, Any]) -> set[str]:
    token = receipt.get("terminal_token")
    if token == "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT":
        return set(COMMON_KEYS)
    if token == "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE":
        return set(COMMON_KEYS) | stage_fields_before(str(receipt.get("phase")))
    normal = (set(COMMON_KEYS) | AUTH_FIELDS | SOURCE_FIELDS | PREFIX_FIELDS |
              LAMBDA_FIELDS | BASE_FIELDS | CORRELATION_FIELDS |
              SECTION_FIELDS | BLOCK_FIELDS | TARGET_FIELDS | AFFINE_FIELDS)
    if token == "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT":
        return normal | {"normalized_dual"}
    if token == "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT":
        return normal | {"selected_proof"}
    raise RuntimeError("157ei terminal registry")


def performance_record(monitor: Monitor, phases: dict[str, float],
                       receipt_bytes: int = 0) -> dict[str, Any]:
    return {**monitor.public(), "receipt_bytes": int(receipt_bytes),
        "phase_seconds": dict(phases), "pair_loop_cadence": 4096,
        "block_relator_columns": 11,
        "target6_remainder_probes": 109,
        "full_E4_enumerations": 0,
        "old_receipt_objects_imported": 0,
        "cross_process_pool_ID_equality_used": False}


def expected_phase_sets(receipt: dict[str, Any]) -> set[frozenset[str]]:
    token, phase = receipt["terminal_token"], receipt["phase"]
    if token.endswith("UNKNOWN_INPUT"):
        return {frozenset()}
    if token.endswith("UNKNOWN_RESOURCE"):
        if phase == "receipt_serialization":
            base = frozenset(PHASE_SEQUENCE[:-1])
            return {base, frozenset(PHASE_SEQUENCE)}
        require(phase in PHASE_SEQUENCE, "157ei timing resource phase")
        return {frozenset(PHASE_SEQUENCE[:PHASE_SEQUENCE.index(phase)])}
    require(phase == "complete", "157ei timing normal phase")
    return ({frozenset(PHASE_SEQUENCE)} if token ==
            "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT" else
            {frozenset(PHASE_SEQUENCE[:-1])})


def base_receipt(q3_path: Path, monitor: Monitor,
                 upstream: dict[str, int]) -> dict[str, Any]:
    token = "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT"
    return {"schema": SCHEMA, "task_sha256": TASK_SHA,
        "terminal_token": token, "status": token,
        "reason": "authenticated_input_failure", "phase": "authenticated_input",
        "pins": pin_rows(q3_path), "caps": CAPS,
        "upstream_caps": {"registry": dict(sorted(upstream.items())),
            "sha256": sha_obj(dict(sorted(upstream.items())))},
        "claims": claim_row(token, False),
        "theorem_boundary": theorem_boundary(),
        "monitor_scope": monitor_scope(False),
        "resource_guards": normal_guard(), "partial": {},
        "input_errors": [], "performance": performance_record(monitor, {})}


def validate_performance(row: dict[str, Any], receipt: dict[str, Any]) -> None:
    require(set(row) == {"initial_remaining_seconds", "elapsed_seconds",
        "remaining_seconds", "checks", "peak_rss_bytes", "hit_reason",
        "receipt_bytes", "phase_seconds", "pair_loop_cadence",
        "block_relator_columns", "target6_remainder_probes",
        "full_E4_enumerations", "old_receipt_objects_imported",
        "cross_process_pool_ID_equality_used"},
        "157ei performance keys")
    initial = row["initial_remaining_seconds"]
    elapsed = row["elapsed_seconds"]; remaining = row["remaining_seconds"]
    require(isinstance(initial, (int, float)) and not isinstance(initial, bool)
            and 0 < initial <= 18_000 and
            isinstance(elapsed, (int, float)) and elapsed >= 0 and
            isinstance(remaining, (int, float)) and 0 <= remaining <= initial
            and abs(initial-elapsed-remaining) <= 2.0 and
            isinstance(row["checks"], int) and row["checks"] >= 0 and
            isinstance(row["peak_rss_bytes"], int) and
            row["peak_rss_bytes"] >= 0 and
            isinstance(row["receipt_bytes"], int) and row["receipt_bytes"] >= 0
            and row["pair_loop_cadence"] == 4096 and
            row["block_relator_columns"] == 11 and
            row["target6_remainder_probes"] == 109 and
            row["full_E4_enumerations"] == 0 and
            row["old_receipt_objects_imported"] == 0 and
            row["cross_process_pool_ID_equality_used"] is False,
            "157ei performance numeric contract")
    timings = row["phase_seconds"]
    require(isinstance(timings, dict) and
            frozenset(timings) in expected_phase_sets(receipt) and
            all(isinstance(value, (int, float)) and value >= 0
                for value in timings.values()) and
            sum(timings.values()) <= elapsed+2.0,
            "157ei phase timings")
    hit = receipt["terminal_token"].endswith("UNKNOWN_RESOURCE")
    require((row["hit_reason"] is not None) == hit,
            "157ei performance hit binding")


def _validate_block_progress_shape(current: dict[str, Any]) -> None:
    """Validate the exact committed prefix represented by a block stop.

    The three substages have different atomicity boundaries.  In particular,
    raw and shadow rows are transient until all eleven have been constructed;
    only ``persistent_columns`` may report committed basis columns.
    """
    attempted = current["attempted_relators"]
    completed = current["completed_relators"]
    raw = current["raw_completed_relators"]
    shadow = current["shadow_completed_relators"]
    rank = current["rank_gain_so_far"]
    relator = current["current_relator"]
    require(all(isinstance(value, int) and not isinstance(value, bool)
                for value in (attempted, completed, raw, shadow, rank)) and
            0 <= attempted <= 11 and 0 <= completed <= 11 and
            0 <= shadow <= raw <= 11 and 0 <= rank <= completed and
            len(current["raw_prefix"]) == raw and
            len(current["shadow_prefix"]) == shadow and
            len(current["scalar_prefix"]) == shadow and
            len(current["block_prefix"]) == completed,
            "157ei block progress counts")
    substage = current["substage"]
    if substage == "translation_section":
        require((attempted, completed, raw, shadow, rank) == (0, 0, 0, 0, 0)
                and relator is None and current["block_prefix"] == [],
                "157ei translation-section atomic prefix")
    elif substage == "shadow_remainders":
        require(completed == rank == 0 and relator == attempted and
                1 <= attempted <= 11 and attempted in {raw, raw+1} and
                raw-shadow in {0, 1} and current["block_prefix"] == [],
                "157ei shadow-remainder atomic prefix")
    elif substage == "persistent_columns":
        require(raw == shadow == 11 and relator == attempted and
                completed <= attempted <= completed+1 and
                1 <= attempted <= 11,
                "157ei persistent-column atomic prefix")
    else:
        require(False, "157ei registered block substage")


def _validate_completed_block_anchor(block: dict[str, Any],
                                     anchor: dict[str, Any]) -> None:
    accounting_keys = {"columns", "pivots", "dependent",
        "live_sparse_entries", "pool_size", "pool_order_sha256",
        "DAG_nodes", "DAG_edges", "section_bindings",
        "section_expression_nodes", "section_expression_edges"}
    pre, post = block["pre_accounting"], block["post_accounting"]
    require(set(pre) == accounting_keys and set(post) == accounting_keys and
            all(isinstance(row[key], int) and row[key] >= 0
                for row in (pre, post) for key in accounting_keys
                if key != "pool_order_sha256") and
            all(isinstance(row["pool_order_sha256"], str) and
                len(row["pool_order_sha256"]) == 64 for row in (pre, post)) and
            post["section_bindings"] == pre["section_bindings"]+1 and
            post["columns"] == pre["columns"]+11 and
            post["pivots"] == pre["pivots"]+block["rank_gain"] and
            post["dependent"] == pre["dependent"]+11-block["rank_gain"] and
            all(post[key] >= pre[key] for key in ("pool_size", "DAG_nodes",
                "DAG_edges", "section_expression_nodes",
                "section_expression_edges")),
            "157ei complete block accounting relation")
    counts = {key: post[key] for key in
              ("columns", "pivots", "dependent", "live_sparse_entries")}
    require(anchor["basis_columns"] == post["columns"] and
            anchor["basis_pivots"] == post["pivots"] and
            anchor["basis_dependent"] == post["dependent"] and
            anchor["basis_live_sparse_entries"] == post["live_sparse_entries"]
            and anchor["pool_size"] == post["pool_size"] and
            anchor["DAG_nodes"] == post["DAG_nodes"] and
            anchor["DAG_edges"] == post["DAG_edges"] and
            anchor["section_bindings"] == post["section_bindings"] and
            anchor["anchor_semantic_sha256"] == sha_obj({
                "basis_counts": counts, "translation_hex": FIRST_T_HEX,
                "columns_sha256": block["raw_columns_sha256"]}),
            "157ei post-block anchor/accounting binding")


def _validate_completed_public_shape(receipt: dict[str, Any], *,
                                     fixture: bool) -> None:
    """Closed, ID-free shape/digest checks shared by normal production/toys."""
    block = receipt["translation_block"]
    block_keys = {"complete", "translation_ordinal", "translation_hex",
        "section_newly_registered", "section_word_length",
        "section_word_sha256", "columns", "column_count", "column_order",
        "old_qstar_scalars", "raw_columns_sha256",
        "reducer_ledger_sha256", "pre_accounting", "post_accounting",
        "rank_gain", "shadow_rank_mod_B0", "two_rank_computations_equal",
        "relator9_independent", "pivot_count_before_relator9",
        "pivot_count_after_relator9", "lexfirst_active_provenance",
        "all_11_rows_are_D2_columns"}
    require(set(block) == block_keys and block["complete"] is True and
            block["translation_ordinal"] == 32976 and
            block["translation_hex"] == FIRST_T_HEX and
            block["section_newly_registered"] is True and
            block["section_word_length"] == 24 and
            block["section_word_sha256"] == FIRST_T_WORD_SHA and
            block["column_count"] == 11 and
            block["column_order"] == "relator indices 1 through 11" and
            block["two_rank_computations_equal"] is True and
            block["all_11_rows_are_D2_columns"] is True and
            block["raw_columns_sha256"] == sha_obj(
                [row["raw_column"] for row in block["columns"]]) and
            block["reducer_ledger_sha256"] == sha_obj(block["columns"]),
            "157ei exact completed block shape/digests")
    column_keys = {"relator_index", "translation_ordinal",
        "translation_hex", "termwise_equals_direct_left_translation",
        "quotient_identity", "D1_D2_zero", "old_qstar_scalar",
        "independent", "pivot", "raw_column"}
    raw_keys = {"entries", "entry_count", "byte_length", "sha256",
                "encoding", "order"}
    for index, column in enumerate(block["columns"], 1):
        require(set(column) == column_keys and
                column["relator_index"] == index and
                column["translation_ordinal"] == 32976 and
                column["translation_hex"] == FIRST_T_HEX and
                column["termwise_equals_direct_left_translation"] is True and
                column["quotient_identity"] is True and
                column["D1_D2_zero"] is True and
                isinstance(column["independent"], bool),
                "157ei exact completed block column")
        raw = column["raw_column"]
        require(set(raw) == raw_keys and
                raw["entry_count"] == len(raw["entries"]) and
                raw["entries"] == sorted(raw["entries"],
                    key=lambda row: (row[0], bytes.fromhex(row[1]))) and
                raw["encoding"] ==
                    "component-u8|E4-blob-154|coefficient-u8" and
                raw["order"] == "component then exact canonical E4 bytes" and
                raw["byte_length"] == len(_raw_bytes(raw["entries"], 154)) and
                raw["sha256"] == sha_bytes(_raw_bytes(raw["entries"], 154)),
                "157ei exact completed raw column")
        pivot = column["pivot"]
        require((not column["independent"] and pivot is None) or
                (column["independent"] and isinstance(pivot, dict) and
                 set(pivot) == {"component", "element_hex", "reduced_row"}
                 and 1 <= pivot["component"] <= 6 and
                 len(bytes.fromhex(pivot["element_hex"])) == 154 and
                 set(pivot["reduced_row"]) == raw_keys),
                "157ei exact completed pivot shape")
    _validate_block_reducer_contract(block["columns"],
        block["old_qstar_scalars"], block["pre_accounting"],
        block["post_accounting"], block["shadow_rank_mod_B0"],
        block["pivot_count_before_relator9"],
        block["pivot_count_after_relator9"], frozen_counts=not fixture)
    _validate_completed_block_anchor(block, receipt["post_block_anchor"])

    affine = receipt["affine_system"]
    affine_keys = {"variables", "rank", "nullity", "consistent",
        "equations", "row_space_sha256", "dual_witness",
        "dual_support_cap_noncontact", "complete_all_coordinates",
        "stopped_at_first_contradiction", "coordinate_encoding"}
    require(set(affine) == affine_keys and affine["variables"] == 108 and
            affine["rank"]+affine["nullity"] == 108 and
            isinstance(affine["equations"], int) and affine["equations"] > 0
            and affine["complete_all_coordinates"] is True and
            affine["stopped_at_first_contradiction"] is False and
            affine["coordinate_encoding"] ==
                "one-based component plus exact 154-byte blob",
            "157ei exact affine public shape")
    target = receipt["target6"]
    common_target_keys = {"ordinal", "name",
        "base_is_direct_not_empty_formula",
        "affine_rhs_is_negative_base_remainder",
        "old_B0_remainder_or_dual_imported",
        "post_block_anchor_used_for_all_109", "target_row"}
    require(target["ordinal"] == 6 and
            target["name"] == "hexagon_1_coface_0" and
            target["base_is_direct_not_empty_formula"] is True and
            target["affine_rhs_is_negative_base_remainder"] is True and
            target["old_B0_remainder_or_dual_imported"] is False and
            target["post_block_anchor_used_for_all_109"] is True and
            target["target_row"]["consistent"] is affine["consistent"] and
            target["target_row"]["constraint_rank"] == affine["rank"] and
            target["target_row"]["nullity"] == affine["nullity"] and
            target["target_row"]["row_space_sha256"] ==
                affine["row_space_sha256"] and
            target["target_row"]["affine_equations"] == affine["equations"],
            "157ei exact target6/affine binding")
    if fixture:
        expected = common_target_keys | {"base_remainder_sha256",
            "delta_rows_sha256", "noncommutative_formula_canary",
            "first_contradiction_canary"}
        canary = target["noncommutative_formula_canary"]
        contradiction = target["first_contradiction_canary"]
        require(set(target) == expected and
                set(canary) == {"operation", "g", "h", "ordered_value",
                    "reversed_value", "ordered_not_reversed"} and
                canary["operation"] ==
                    "PRODUCT(g,INVERSE(INVERSE(h)))" and
                canary["ordered_value"] != canary["reversed_value"] and
                canary["ordered_not_reversed"] is True and
                set(contradiction) == {"coordinate_ordinal",
                    "rows_after_coordinate", "full_equation_count",
                    "consistent_fixture"} and
                contradiction["coordinate_ordinal"] == 2 and
                contradiction["rows_after_coordinate"] == 107 and
                contradiction["full_equation_count"] ==
                    affine["equations"] == 109,
                "157ei exact fixture target6 ledger")
    else:
        expected = common_target_keys | {"kind",
            "empty_formula_is_zero_delta_canary", "base_gradient",
            "base_gradient_sha256", "formula_checks",
            "formula_checks_sha256", "typed_split", "typed_split_sha256",
            "direct_gradient_bindings_sha256", "direct_vs_typed_count",
            "fresh_remainders", "fresh_remainder_count",
            "fresh_remainder_sha256", "old_157ec_comparison"}
        require(set(target) == expected and target["kind"] == "hexagon" and
                target["empty_formula_is_zero_delta_canary"] is True and
                target["base_gradient_sha256"] ==
                    sha_obj(target["base_gradient"]) and
                target["formula_checks_sha256"] ==
                    sha_obj(target["formula_checks"]) and
                target["typed_split_sha256"] ==
                    sha_obj(target["typed_split"]) and
                target["direct_vs_typed_count"] == 108 and
                len(target["typed_split"]) == 108 and
                target["fresh_remainder_count"] == 109 ==
                    len(target["fresh_remainders"]) and
                target["fresh_remainder_sha256"] ==
                    sha_obj(target["fresh_remainders"]) and
                target["old_157ec_comparison"] == {
                    "receipt_sha256":
                        "d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d",
                    "old104_rank": 50, "full108_rank": 54,
                    "old104_comparison_sha256": OLD_TARGET6_ROW_SHA,
                    "evidence_only_not_imported": True},
                "157ei exact production target6 ledger")


def validate_receipt_schema(receipt: dict[str, Any], *,
                            fixture: bool = False) -> None:
    require(set(receipt) == expected_keys(receipt) and
            receipt.get("schema") == SCHEMA and
            receipt.get("task_sha256") == TASK_SHA and
            receipt.get("terminal_token") == receipt.get("status") in TERMINALS,
            "157ei exact receipt envelope")
    require(receipt["caps"] == CAPS and
            receipt["theorem_boundary"] == theorem_boundary() and
            set(receipt["upstream_caps"]) == {"registry", "sha256"} and
            receipt["upstream_caps"]["sha256"] ==
                sha_obj(receipt["upstream_caps"]["registry"]),
            "157ei fixed contracts")
    if not fixture:
        q3 = ROOT/Q3_PATH
        require(receipt["pins"] == pin_rows(q3), "157ei receipt pins")
    scope = receipt["monitor_scope"]
    require(set(scope) == {"contract", "registry", "registry_sha256",
        "registered_pair_count", "fresh_adapter_detached_after_prefix",
        "post_stage_adapters_detached", "resource_callback",
        "wildcards_or_inference_used", "deadline_or_RSS_epoch_reset",
        "receipt_serialization_is_outside_monitor"} and
        scope["contract"] == "one-clock-exact-outer-inner/v1" and
        scope["registry"] == MONITOR_REGISTRY and
        scope["registry_sha256"] == MONITOR_SHA and
        scope["registered_pair_count"] == sum(map(len, MONITOR_REGISTRY.values()))
        and scope["post_stage_adapters_detached"] is True and
        scope["fresh_adapter_detached_after_prefix"] is
            ("prefix" in receipt) and
        scope["wildcards_or_inference_used"] is False and
        scope["deadline_or_RSS_epoch_reset"] is False and
        scope["receipt_serialization_is_outside_monitor"] is True,
        "157ei monitor scope")
    validate_performance(receipt["performance"], receipt)
    token = receipt["terminal_token"]
    block_complete = bool(receipt.get("translation_block", {}).get("complete"))
    require(receipt["claims"] == claim_row(token, block_complete),
            "157ei claim boundary")
    guard = receipt["resource_guards"]
    require(set(guard) == {"resource_hit", "resource", "atomic_partial"} and
            guard["atomic_partial"] is True,
            "157ei resource guard keys")
    if token.endswith("UNKNOWN_INPUT"):
        require(receipt["reason"] == "authenticated_input_failure" and
                receipt["phase"] == "authenticated_input" and
                bool(receipt["input_errors"]) and receipt["partial"] == {} and
                guard == normal_guard(), "157ei input terminal")
        return
    if token.endswith("UNKNOWN_RESOURCE"):
        row = guard["resource"]
        require(guard["resource_hit"] is True and isinstance(row, dict) and
                set(row) == {"cap_reason", "cap_key", "cap_source",
                    "cap_limit", "observed_count", "comparator", "phase",
                    "current"} and
                receipt["reason"] == row["cap_reason"] == row["cap_key"] and
                receipt["phase"] == row["phase"] and
                row["cap_source"] in {"local", "upstream"} and
                row["comparator"] in {"gt", "ge"} and
                (row["observed_count"] > row["cap_limit"] if
                 row["comparator"] == "gt" else
                 row["observed_count"] >= row["cap_limit"]),
                "157ei resource row")
        registry = CAPS if row["cap_source"] == "local" else \
            receipt["upstream_caps"]["registry"]
        require(row["cap_key"] in registry and
                registry[row["cap_key"]] == row["cap_limit"],
                "157ei resource closed registry")
        partial = receipt["partial"]
        require(set(partial) == {"phase", "reason", "attempted_relators",
            "completed_relators", "raw_completed_relators",
            "shadow_completed_relators", "raw_column_prefix_sha256",
            "shadow_remainder_prefix_sha256", "old_qstar_prefix_sha256",
            "rank_gain_so_far", "source_evaluated_seeds",
            "source_records_prefix_sha256", "evaluated_seeds",
            "completed_equations",
            "current_seed", "block_digest_prefix", "block_pre_accounting",
            "block_post_accounting", "target_ledger_prefix_sha256",
            "completed_target_system", "rollback_anchor_after_block",
            "mathematical_claim"} and
            partial["phase"] == receipt["phase"] and
            partial["reason"] == receipt["reason"] and
            partial["mathematical_claim"] == "none",
            "157ei resource partial")
        current = row["current"]
        if receipt["phase"] == "source_preflight":
            require(set(current) == {"current_seed", "evaluated_seeds",
                "records_prefix_sha256"} and
                0 <= current["evaluated_seeds"] <= 108 and
                partial["source_evaluated_seeds"] ==
                    current["evaluated_seeds"] and
                partial["source_records_prefix_sha256"] ==
                    current["records_prefix_sha256"],
                "157ei source resource current")
        elif receipt["phase"] == "block_insertion":
            require(set(current) == {"attempted_relators",
                "completed_relators", "rank_gain_so_far", "block_prefix",
                "block_pre_accounting", "block_post_accounting",
                "current_relator", "substage", "raw_prefix",
                "shadow_prefix", "scalar_prefix", "raw_completed_relators",
                "shadow_completed_relators"},
                "157ei block resource current keys")
            _validate_block_progress_shape(current)
            require(
                partial["attempted_relators"] == current["attempted_relators"]
                and partial["completed_relators"] ==
                    current["completed_relators"] and
                partial["raw_completed_relators"] ==
                    current["raw_completed_relators"] and
                partial["shadow_completed_relators"] ==
                    current["shadow_completed_relators"] and
                partial["raw_column_prefix_sha256"] ==
                    sha_obj(current["raw_prefix"]) and
                partial["shadow_remainder_prefix_sha256"] ==
                    sha_obj(current["shadow_prefix"]) and
                partial["old_qstar_prefix_sha256"] ==
                    sha_obj(current["scalar_prefix"]) and
                partial["rank_gain_so_far"] == current["rank_gain_so_far"] and
                partial["block_digest_prefix"] ==
                    (None if not current["block_prefix"] else
                     sha_obj(current["block_prefix"])) and
                partial["block_pre_accounting"] ==
                    current["block_pre_accounting"] and
                partial["block_post_accounting"] ==
                    current["block_post_accounting"],
                "157ei block resource current")
        elif receipt["phase"] == "target_reduction":
            require(set(current) == {"substage", "evaluated_seeds",
                "completed_equations", "current_seed", "typed_split_prefix",
                "remainder_prefix", "completed_target_system"} and
                current["substage"] in {
                    "typed_formula_setup", "base_remainder",
                    "seed_remainder", "affine_absorption"} and
                partial["evaluated_seeds"] == current["evaluated_seeds"] and
                partial["completed_equations"] ==
                    current["completed_equations"] and
                partial["current_seed"] == current["current_seed"] and
                partial["target_ledger_prefix_sha256"] ==
                    sha_obj(current["typed_split_prefix"]) and
                partial["completed_target_system"] ==
                    current["completed_target_system"] and
                ((current["completed_target_system"] is None and
                  current["completed_equations"] == 0) or
                 (isinstance(current["completed_target_system"], dict) and
                  current["completed_equations"] ==
                    current["completed_target_system"]["equations"])),
                "157ei target resource current")
            substage = current["substage"]
            if substage in {"typed_formula_setup", "base_remainder"}:
                require(current["evaluated_seeds"] == 0 and
                        current["completed_equations"] == 0 and
                        current["current_seed"] is None and
                        current["typed_split_prefix"] == [] and
                        current["remainder_prefix"] == [] and
                        current["completed_target_system"] is None,
                        "157ei target setup/base atomic prefix")
            elif substage == "seed_remainder":
                require(1 <= current["current_seed"] <= 108 and
                        current["evaluated_seeds"]+1 ==
                            current["current_seed"] and
                        len(current["typed_split_prefix"]) ==
                            current["evaluated_seeds"] and
                        len(current["remainder_prefix"]) ==
                            current["evaluated_seeds"]+1 and
                        current["completed_equations"] == 0 and
                        current["completed_target_system"] is None,
                        "157ei target seed atomic prefix")
            else:
                require(current["evaluated_seeds"] == 108 and
                        current["current_seed"] is None and
                        len(current["typed_split_prefix"]) == 108 and
                        len(current["remainder_prefix"]) == 109 and
                        current["completed_equations"] in {0,
                            (current["completed_target_system"] or {}).get(
                                "equations", -1)},
                        "157ei affine absorption atomic prefix")
            completed_system = current["completed_target_system"]
            if completed_system is not None:
                require(row["cap_key"] == "dual_provenance_entries" and
                    set(completed_system) == {"coordinate_count", "rank",
                        "nullity", "consistent", "equations",
                        "row_space_sha256", "attempted_dual_support_count",
                        "attempted_dual_sha256"} and
                    completed_system["consistent"] is False and
                    completed_system["rank"]+completed_system["nullity"] ==
                        108 and
                    completed_system["coordinate_count"] ==
                        completed_system["equations"] and
                    completed_system["attempted_dual_support_count"] >
                        CAPS["dual_provenance_entries"],
                    "157ei completed target dual-cap projection")
        elif receipt["phase"] == "selected_proof":
            require(current == {} or set(current) == {"evaluated_seeds",
                "completed_equations", "current_seed"},
                "157ei selected resource current")
            require(partial["evaluated_seeds"] == 108 and
                    partial["completed_equations"] ==
                        receipt["affine_system"]["equations"] and
                    partial["current_seed"] is None and
                    partial["completed_target_system"] is None,
                    "157ei selected-proof committed target")
        else:
            require(current == {} and partial["evaluated_seeds"] == 0 and
                    partial["completed_equations"] == 0 and
                    partial["current_seed"] is None and
                    partial["target_ledger_prefix_sha256"] is None and
                    partial["completed_target_system"] is None,
                    "157ei pretarget/serialization resource current")
        if receipt["phase"] in {"target_reduction", "selected_proof",
                                "receipt_serialization"}:
            completed_block = receipt["translation_block"]
            require(partial["attempted_relators"] == 11 and
                    partial["completed_relators"] == 11 and
                    partial["raw_completed_relators"] == 11 and
                    partial["shadow_completed_relators"] == 11 and
                    partial["raw_column_prefix_sha256"] ==
                        completed_block["raw_columns_sha256"] and
                    partial["old_qstar_prefix_sha256"] ==
                        sha_obj(completed_block["old_qstar_scalars"]) and
                    partial["rank_gain_so_far"] ==
                        completed_block["rank_gain"] and
                    partial["block_digest_prefix"] ==
                        sha_obj(completed_block["columns"]) and
                    partial["block_pre_accounting"] ==
                        completed_block["pre_accounting"] and
                    partial["block_post_accounting"] ==
                        completed_block["post_accounting"] and
                    partial["rollback_anchor_after_block"] is True,
                    "157ei completed block resource binding")
            _validate_completed_block_anchor(
                completed_block, receipt["post_block_anchor"])
        diagnostic = scope["resource_callback"]
        if row["cap_source"] == "local" and row["cap_key"] in {
                "common_math_soft_deadline_seconds", "producer_soft_rss_bytes"}:
            require(isinstance(diagnostic, dict) and set(diagnostic) ==
                    {"outer", "inner", "api"} and
                    diagnostic["outer"] == receipt["phase"] and
                    diagnostic["inner"] in MONITOR_FROZEN[diagnostic["outer"]]
                    and diagnostic["api"] in {"check", "reserve"},
                    "157ei monitor resource diagnostic")
        else:
            require(diagnostic is None, "157ei nonmonitor resource diagnostic")
        return
    require(receipt["phase"] == "complete" and receipt["reason"] in {
        "complete_target6_affine_system_consistent_with_selected_proof",
        "complete_target6_affine_system_inconsistent_with_normalized_dual"}
        and guard == normal_guard() and receipt["partial"] == {} and
        receipt["input_errors"] == [] and
        receipt["monitor_scope"]["fresh_adapter_detached_after_prefix"] is True,
        "157ei normal terminal")
    expected_reason = {
        "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT":
            "complete_target6_affine_system_consistent_with_selected_proof",
        "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT":
            "complete_target6_affine_system_inconsistent_with_normalized_dual",
    }[token]
    require(receipt["reason"] == expected_reason,
            "157ei exact terminal reason")
    block = receipt["translation_block"]
    require(block["complete"] is True and
            block["section_newly_registered"] is True and
            block["rank_gain"] in range(1, 12)
            and block["relator9_independent"] is True and
            block["pivot_count_after_relator9"] ==
                block["pivot_count_before_relator9"]+1 and
            block["old_qstar_scalars"][:8] == [0]*8 and
            block["old_qstar_scalars"][8] == 1 and
            block["lexfirst_active_provenance"] == {"component": 4,
                "relator_index": 9, "scalar": 1,
                "translation_hex": FIRST_T_HEX,
                "section_word_sha256": FIRST_T_WORD_SHA},
            "157ei load-bearing block theorem")
    anchor = receipt["post_block_anchor"]
    require(set(anchor) == {"after_complete_block", "basis_columns",
        "basis_pivots", "basis_dependent", "basis_live_sparse_entries",
        "pool_size", "DAG_nodes", "DAG_edges", "section_bindings",
        "translation_retained", "anchor_semantic_sha256",
        "private_anchor_ids_not_exported"} and
        anchor["after_complete_block"] is True and
        anchor["private_anchor_ids_not_exported"] is True and
        not any(key.startswith("_") for key in anchor),
        "157ei public post-block anchor")
    _validate_completed_public_shape(receipt, fixture=fixture)
    system = receipt["affine_system"]
    require(system["variables"] == 108 and system["rank"]+system["nullity"] == 108
            and system["consistent"] is
                (token == "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT"),
            "157ei affine terminal")
    if token.endswith("INCONSISTENT"):
        require(receipt["normalized_dual"] == system["dual_witness"] and
                receipt["normalized_dual"]["normalized_rhs"] == 1 and
                receipt["normalized_dual"]["yTz_mod3"] == 2,
                "157ei normalized dual")
    else:
        _validate_selected_public_contract(receipt["selected_proof"])


def _pool_order_sha(pool: Any) -> str:
    digest = hashlib.sha256()
    for identifier, value in enumerate(pool.values):
        require(pool.ids.get(value) == identifier,
                "157ei pool bijection/order")
        digest.update(value)
    require(len(pool.ids) == len(pool.values), "157ei pool cardinality")
    return digest.hexdigest()


def _raw_public(old: Any, vector: dict[int, int], pool: Any) \
        -> list[list[Any]]:
    rows: list[list[Any]] = []
    for key, coefficient in vector.items():
        coefficient = int(coefficient) % 3
        if not coefficient:
            continue
        component, identifier = old.unpack_vector_key(int(key))
        blob = bytes(pool.blob(identifier))
        require(1 <= component <= 6 and len(blob) == pool.width,
                "157ei packed vector key")
        rows.append([int(component), blob.hex(), coefficient])
    rows.sort(key=lambda row: (row[0], bytes.fromhex(row[1])))
    return rows


def _raw_bytes(rows: Sequence[Sequence[Any]], width: int) -> bytes:
    out = bytearray()
    for component, value_hex, coefficient in rows:
        value = bytes.fromhex(str(value_hex))
        require(1 <= int(component) <= 6 and len(value) == width and
                int(coefficient) in (1, 2), "157ei raw encoding")
        out.append(int(component)); out.extend(value); out.append(int(coefficient))
    return bytes(out)


def _raw_row(old: Any, vector: dict[int, int], pool: Any) -> dict[str, Any]:
    rows = _raw_public(old, vector, pool)
    raw = _raw_bytes(rows, pool.width)
    return {"entries": rows, "entry_count": len(rows),
        "byte_length": len(raw), "sha256": sha_bytes(raw),
        "encoding": "component-u8|E4-blob-154|coefficient-u8",
        "order": "component then exact canonical E4 bytes"}


def _semantic_rank(rows: Sequence[Sequence[Sequence[Any]]]) -> int:
    """Rank of public sparse rows; canonical labels, never pool IDs."""
    pivots: dict[tuple[int, str], dict[tuple[int, str], int]] = {}
    for public in rows:
        row = {(int(c), str(h)): int(a) % 3 for c, h, a in public
               if int(a) % 3}
        while row:
            pivot = min(row, key=lambda key: (key[0], bytes.fromhex(key[1])))
            old = pivots.get(pivot)
            if old is None:
                factor = 1 if row[pivot] == 1 else 2
                pivots[pivot] = {key: factor*value % 3
                                 for key, value in row.items()
                                 if factor*value % 3}
                break
            coefficient = row[pivot]
            for key, value in old.items():
                result = (row.get(key, 0)-coefficient*value) % 3
                if result:
                    row[key] = result
                else:
                    row.pop(key, None)
    return len(pivots)


def _validate_block_reducer_contract(ledger: Sequence[dict[str, Any]],
                                     scalar_rows: Sequence[int],
                                     pre: dict[str, Any],
                                     post: dict[str, Any],
                                     shadow_rank: int,
                                     pivots_before_9: int,
                                     pivots_after_9: int, *,
                                     frozen_counts: bool) -> int:
    require(len(ledger) == len(scalar_rows) == 11 and
            [row["relator_index"] for row in ledger] == list(range(1, 12)) and
            list(scalar_rows[:8]) == [0]*8 and scalar_rows[8] == 1 and
            all(row["old_qstar_scalar"] == scalar_rows[index]
                for index, row in enumerate(ledger)) and
            ledger[8]["independent"] is True and
            pivots_after_9 == pivots_before_9+1,
            "157ei shared relator9 block theorem")
    gain = int(post["pivots"])-int(pre["pivots"])
    require(int(post["columns"]) == int(pre["columns"])+11 and
            int(post["dependent"]) == int(pre["dependent"])+(11-gain) and
            gain == shadow_rank and 1 <= gain <= 11,
            "157ei shared block rank/accounting")
    if frozen_counts:
        require(pre["columns"] == 362725 and pre["pivots"] == 362709 and
                pre["dependent"] == 16 and post["columns"] == 362736 and
                post["pivots"] == 362709+gain and
                post["dependent"] == 16+(11-gain),
                "157ei frozen B0/B1 accounting")
    return gain


def _prefix_public(old: Any, prefix: dict[str, Any], dependent: list[Any],
                   ed: Any) -> dict[str, Any]:
    pool, basis = prefix["pool"], prefix["basis"]
    directed = prefix["directed_surgery"]
    require(directed["stable_rounds_projection_sha256"] == PREFIX_STABLE_SHA and
            directed["translations_sha256"] == PREFIX_TRANSLATIONS_SHA and
            directed["columns_sha256"] == PREFIX_COLUMNS_SHA and
            directed["blocker_history_sha256"] == PREFIX_BLOCKERS_SHA,
            "157ei fresh directed schedule")
    accounting = prefix["accounting"]
    require(accounting["columns"] == PREFIX_COUNTS["columns"] and
            accounting["pivots"] == PREFIX_COUNTS["pivots"] and
            accounting["dependent_columns"] == 16 and
            accounting["BFS_translations"] == 32768 and
            accounting["directed_translations"] == 207 and
            accounting["live_sparse_entries"] == 3090367 and
            len(pool.values) == PREFIX_POOL_CHECKPOINT and len(dependent) == 16,
            "157ei fresh prefix accounting")
    return {"counts": dict(PREFIX_COUNTS), "accounting": accounting,
        "basis_gate": old.affine_basis_gate(basis, pool),
        "prefix_pool_checkpoint": len(pool.values),
        "pool_order_sha256": _pool_order_sha(pool),
        "dependent_events": dependent,
        "dependent_event_count": len(dependent),
        "dependent_event_sha256": sha_obj(dependent),
        "fresh_not_imported": True, "source_sha256": ed.STRONG_SHA,
        "stable_rounds_projection_sha256": PREFIX_STABLE_SHA,
        "translations_sha256": PREFIX_TRANSLATIONS_SHA,
        "columns_sha256": PREFIX_COLUMNS_SHA,
        "blocker_history_sha256": PREFIX_BLOCKERS_SHA}


def _require_correlation(corr: dict[str, Any], witness: dict[str, Any]) -> None:
    public = corr["public"]
    require(public == {**public} and public["complete"] is True and
            public["pair_attempts"] == 886 and
            public["candidate_count_before_zero_deletion"] == 724 and
            public["cancellation_to_zero_count"] == 156 and
            public["active_count"] == 568 and
            public["scalar_distribution"] == {"1": 284, "2": 284} and
            public["packed_rows_sha256"] == CORRELATION_SHA and
            public["first_active"] == {
                "translation_hex": FIRST_T_HEX,
                "relator_index": 9, "scalar": 1},
            "157ei complete old correlation")
    pair = corr["first_contributing_pair"]
    require(pair == witness["contributing_pair"] and
            pair["translation_hex"] == FIRST_T_HEX and
            pair["component"] == 4 and
            pair["relator_index"] == 9 and
            pair["formula"] == "t=g*h^-1" and
            witness["direct_replay"] == {
                **witness["direct_replay"], "g_word_length": 22,
                "g_word_sha256": FIRST_G_WORD_SHA,
                "t_word_length": 24, "t_word_sha256": FIRST_T_WORD_SHA,
                "t_value_hex": FIRST_T_HEX, "both_exact": True} and
            witness["section_expressions"]["manifest_sha256"] ==
                SECTION_MANIFEST_SHA,
            "157ei first active typed section")


def _manual_translate(old: Any, base: dict[int, int], translation_id: int,
                      pool: Any) -> dict[int, int]:
    result: dict[int, int] = {}
    for key, coefficient in base.items():
        component, identifier = old.unpack_vector_key(key)
        shifted = pool.mul_id(translation_id, identifier)
        old.add_packed_term(result,
            old.pack_vector_key(component, shifted), coefficient)
    return result


def _recover_translation_root(old: Any, eg: Any, prefix: dict[str, Any]) \
        -> tuple[Any, int, list[int]]:
    expressions = prefix["sections"].expressions
    roots = [node for node, roles in expressions.roles.items()
             if "full_D2_translation_t" in roles]
    require(len(roots) == 1, "157ei unique translation expression root")
    root = roots[0]
    t_blob = bytes.fromhex(FIRST_T_HEX)
    require(expressions.value_blob(root) == t_blob,
            "157ei translation expression value")
    word = eg.materialize_section_node(old, prefix["pool"].quotient,
                                       expressions, root)
    require(len(word) == 24 and sha_obj(word) == FIRST_T_WORD_SHA,
            "157ei exact translation word")
    return prefix["pool"].unpack(t_blob), root, word


def _block_accounting(prefix: dict[str, Any], *, pool_digest: bool) \
        -> dict[str, Any]:
    pool, basis, dag, sections = (prefix[k] for k in
                                  ("pool", "basis", "dag", "sections"))
    return {"columns": basis.columns_seen, "pivots": len(basis.rows),
        "dependent": basis.dependent_columns,
        "live_sparse_entries": basis.live_vector_entries,
        "pool_size": len(pool.values),
        "pool_order_sha256": _pool_order_sha(pool) if pool_digest else None,
        "DAG_nodes": dag.node_count, "DAG_edges": dag.edge_count,
        "section_bindings": len(sections.by_blob),
        "section_expression_nodes": len(sections.expressions.kind),
        "section_expression_edges": sections.expressions.edge_count}


def _absorb_ordered_block_core(
        raw_rows: Sequence[dict[str, Any]], scalar_rows: Sequence[int],
        shadow_rows: Sequence[Sequence[Sequence[Any]]], pre: dict[str, Any],
        add_column: Callable[[int], tuple[bool, dict[str, Any] | None]],
        accounting: Callable[[bool], dict[str, Any]],
        progress: dict[str, Any], *, frozen_counts: bool,
        before_each: Callable[[], None] | None = None,
        trace: dict[str, int] | None = None) \
        -> tuple[list[dict[str, Any]], int, int, int, int, dict[str, Any]]:
    """Shared persistent 11-column reducer used by production and fixtures."""
    if trace is not None:
        trace["block_core"] = trace.get("block_core", 0)+1
    require(len(raw_rows) == len(scalar_rows) == len(shadow_rows) == 11 and
            list(scalar_rows[:8]) == [0]*8 and scalar_rows[8] == 1,
            "157ei shared block inputs")
    for row in raw_rows:
        require(set(row) == {"entries", "entry_count", "byte_length",
            "sha256", "encoding", "order"} and
            row["entry_count"] == len(row["entries"]) and
            row["encoding"] ==
                "component-u8|E4-blob-154|coefficient-u8" and
            row["order"] == "component then exact canonical E4 bytes" and
            row["entries"] == sorted(row["entries"],
                key=lambda item: (item[0], bytes.fromhex(item[1]))) and
            row["byte_length"] == len(_raw_bytes(row["entries"], 154)) and
            row["sha256"] == sha_bytes(_raw_bytes(row["entries"], 154)),
            "157ei shared canonical raw row")
    shadow_rank = _semantic_rank(shadow_rows)
    require(1 <= shadow_rank <= 11, "157ei shared block shadow rank")
    ledger: list[dict[str, Any]] = progress["block_prefix"]
    require(ledger == [] and progress["completed_relators"] == 0,
            "157ei shared block fresh ledger")
    before9: int | None = None
    after9: int | None = None
    progress["substage"] = "persistent_columns"
    for relator, raw_row in enumerate(raw_rows, 1):
        progress["attempted_relators"] = relator
        progress["current_relator"] = relator
        if before_each is not None:
            before_each()
        before = accounting(False)
        if relator == 9:
            before9 = int(before["pivots"])
        independent, pivot_row = add_column(relator)
        after = accounting(False)
        require(after["columns"] == before["columns"]+1 and
                after["pivots"]-before["pivots"] in (0, 1) and
                after["dependent"]-before["dependent"] in (0, 1) and
                independent == (after["pivots"] == before["pivots"]+1) and
                independent == (after["dependent"] == before["dependent"]),
                "157ei shared block reducer outcome")
        ledger.append({"relator_index": relator,
            "translation_ordinal": 32976,
            "translation_hex": FIRST_T_HEX,
            "termwise_equals_direct_left_translation": True,
            "quotient_identity": True, "D1_D2_zero": True,
            "old_qstar_scalar": int(scalar_rows[relator-1]),
            "independent": independent, "pivot": pivot_row,
            "raw_column": raw_row})
        progress["completed_relators"] = relator
        progress["rank_gain_so_far"] = \
            int(after["pivots"])-int(pre["pivots"])
        progress["block_post_accounting"] = after
        if relator == 9:
            after9 = int(after["pivots"])
            require(after9 == int(before9)+1 and independent,
                    "157ei shared relator9 immediate pivot increment")
    require(before9 is not None and after9 is not None and
            ledger[8]["independent"] is True,
            "157ei shared relator9 theorem")
    post = accounting(True)
    gain = _validate_block_reducer_contract(
        ledger, scalar_rows, pre, post, shadow_rank, before9, after9,
        frozen_counts=frozen_counts)
    return ledger, gain, shadow_rank, before9, after9, post


def _commit_block(old: Any, eg: Any, prefix: dict[str, Any], oracle: Any,
                  monitor: Monitor) -> tuple[dict[str, Any], dict[str, Any]]:
    pool, basis, dag, sections = (prefix[k] for k in
                                  ("pool", "basis", "dag", "sections"))
    require(basis.deadline is None and dag.deadline is None,
            "157ei detached prefix before block")
    raw_columns: list[dict[int, int]] = []
    shadow_rows: list[list[list[Any]]] = []
    scalar_rows: list[int] = []
    block_monitor = monitor.bind("block_insertion")
    basis.deadline = block_monitor; dag.deadline = block_monitor
    pre = _block_accounting(prefix, pool_digest=True)
    require(pre["columns"] == 362725 and pre["pivots"] == 362709 and
            pre["dependent"] == 16, "157ei B0 pre-block counts")
    ledger: list[dict[str, Any]] = []
    progress: dict[str, Any] = {"attempted_relators": 0,
        "completed_relators": 0, "rank_gain_so_far": 0,
        "block_prefix": ledger, "block_pre_accounting": pre,
        "block_post_accounting": dict(pre), "current_relator": None,
        "substage": "translation_section", "raw_prefix": [],
        "shadow_prefix": [], "scalar_prefix": [],
        "raw_completed_relators": 0, "shadow_completed_relators": 0}
    pivots_before_9: int | None = None
    pivots_after_9_actual: int | None = None
    shadow_rank = 0
    gain = 0
    post: dict[str, Any] = {}
    t_word: list[int] = []
    newly_registered = False
    translation_id: int | None = None
    try:
        block_monitor.check("block_insertion", force=True)
        t, t_root, t_word = _recover_translation_root(old, eg, prefix)
        t_blob = bytes.fromhex(FIRST_T_HEX)
        require(t_blob not in sections.by_blob and
                t_blob not in sections.directed_blobs and
                t_blob not in sections.directed_roots,
                "157ei translation pool containment is not section registration")
        tagged, newly_registered = sections.register_directed(t, t_root)
        translation_id = pool.ids.get(t_blob)
        require(newly_registered is True and translation_id is not None and
                sections.directed_roots.get(t_blob) == t_root and
                t_blob in sections.directed_blobs and
                sections.node_for(translation_id) == tagged and
                (tagged < sections.EXPR_TAG or
                 eg.materialize_section_node(old, pool.quotient,
                    sections.expressions, tagged-sections.EXPR_TAG) == t_word),
                "157ei persistent exact translation section")
        anchor_ids = list(prefix["base_source_key"])+[translation_id]
        progress["substage"] = "shadow_remainders"
        for relator in range(1, 12):
            progress["attempted_relators"] = relator
            progress["current_relator"] = relator
            block_monitor.check("block_insertion", force=True)
            base = basis.relator_columns[relator-1]
            direct = old.translate_vector_packed(base, translation_id, pool)
            manual = _manual_translate(old, base, translation_id, pool)
            require(direct == manual and old.d1_packed(direct, pool) == {},
                    f"157ei translated D2 column {relator}")
            raw_columns.append(direct)
            progress["raw_prefix"].append(_raw_row(old, direct, pool))
            progress["raw_completed_relators"] = relator
            snapshot = old.candidate_transaction_snapshot(
                pool, dag, basis, sections, anchor_ids)
            try:
                remainder = old.affine_full_remainder(
                    direct, basis, pool, block_monitor)
            finally:
                old.rollback_candidate_transaction(
                    snapshot, pool, dag, basis, sections)
            shadow_public = _raw_public(old, remainder, pool)
            shadow_rows.append(shadow_public)
            scalar = int(oracle.packed(direct))
            scalar_rows.append(scalar)
            progress["shadow_prefix"].append(shadow_public)
            progress["scalar_prefix"].append(scalar)
            progress["shadow_completed_relators"] = relator
        raw_rows = [_raw_row(old, raw, pool) for raw in raw_columns]

        def add_column(relator: int) -> tuple[bool, dict[str, Any] | None]:
            before_pivots = set(basis.rows)
            # Explicitly invoke the frozen base implementation, bypassing the
            # predecessor's instrumentation subclass: this block owns its
            # public, semantic ledger and does not alter the old 16 events.
            old.SparseBoundaryBasis.add_column(
                basis, relator, translation_id, tagged,
                translation_ordinal=32976)
            added = sorted(set(basis.rows)-before_pivots,
                key=pool.pivot_order)
            independent = len(added) == 1
            require(len(added) in (0, 1), "157ei block reducer outcome")
            pivot_row = None
            if independent:
                pivot = added[0]
                component, identifier = old.unpack_vector_key(pivot)
                reduced = basis.rows[pivot][0]
                pivot_row = {"component": component,
                    "element_hex": pool.blob(identifier).hex(),
                    "reduced_row": _raw_row(old, reduced, pool)}
            return independent, pivot_row

        ledger, gain, shadow_rank, pivots_before_9, \
            pivots_after_9_actual, post = _absorb_ordered_block_core(
                raw_rows, scalar_rows, shadow_rows, pre, add_column,
                lambda digest: _block_accounting(prefix, pool_digest=digest),
                progress, frozen_counts=True,
                before_each=lambda: block_monitor.check(
                    "block_insertion", force=True))
    except Exception as exc:
        progress["block_post_accounting"] = _block_accounting(
            prefix, pool_digest=True)
        progress["rank_gain_so_far"] = len(basis.rows)-int(pre["pivots"])
        if isinstance(exc, LaneResource):
            exc.current = copy.deepcopy(progress)
        else:
            setattr(exc, "ei_block_current", copy.deepcopy(progress))
        raise
    finally:
        require(basis.deadline is block_monitor and dag.deadline is block_monitor,
                "157ei block adapter identity")
        basis.deadline = None; dag.deadline = None

    require(pivots_before_9 is not None and
            pivots_after_9_actual is not None,
            "157ei complete shared block result")
    public = {"complete": True, "translation_ordinal": 32976,
        "translation_hex": FIRST_T_HEX,
        "section_newly_registered": newly_registered,
        "section_word_length": len(t_word),
        "section_word_sha256": sha_obj(t_word),
        "columns": ledger, "column_count": len(ledger),
        "column_order": "relator indices 1 through 11",
        "old_qstar_scalars": scalar_rows,
        "raw_columns_sha256": sha_obj([row["raw_column"] for row in ledger]),
        "reducer_ledger_sha256": sha_obj(ledger),
        "pre_accounting": pre, "post_accounting": post,
        "rank_gain": gain, "shadow_rank_mod_B0": shadow_rank,
        "two_rank_computations_equal": True,
        "relator9_independent": True,
        "pivot_count_before_relator9": pivots_before_9,
        "pivot_count_after_relator9": pivots_after_9_actual,
        "lexfirst_active_provenance": {"component": 4,
            "relator_index": 9, "scalar": 1,
            "translation_hex": FIRST_T_HEX,
            "section_word_sha256": FIRST_T_WORD_SHA},
        "all_11_rows_are_D2_columns": True}
    require(translation_id is not None, "157ei retained translation ID")
    canonical_basis_counts = {key: post[key] for key in
        ("columns", "pivots", "dependent", "live_sparse_entries")}
    anchor = {"after_complete_block": True,
        "basis_columns": basis.columns_seen, "basis_pivots": len(basis.rows),
        "basis_dependent": basis.dependent_columns,
        "basis_live_sparse_entries": basis.live_vector_entries,
        "pool_size": len(pool.values), "DAG_nodes": dag.node_count,
        "DAG_edges": dag.edge_count,
        "section_bindings": len(sections.by_blob),
        "translation_retained": pool.ids.get(t_blob) == translation_id and
            sections.node_for(translation_id) == tagged,
        "anchor_semantic_sha256": sha_obj({"basis_counts": canonical_basis_counts,
            "translation_hex": FIRST_T_HEX,
            "columns_sha256": public["raw_columns_sha256"]}),
        "private_anchor_ids_not_exported": True,
        "_pool_checkpoint": pool.checkpoint(),
        "_dag_checkpoint": list(dag.checkpoint()), "_ids": anchor_ids}
    return public, anchor


def _binding(old: Any, name: str, kind: str, gradient: Any,
             value: Any) -> dict[str, Any]:
    return old.raw_gradient_binding(name, kind, gradient, value)


def _gradient_add(old: Any, left: dict[Any, int], right: dict[Any, int],
                  scalar: int = 1) -> dict[Any, int]:
    out = dict(left); old.add_scaled(out, right, scalar); return out


def _classify_affine_system(system: Any, variables: int = 108) \
        -> dict[str, Any]:
    dual = system.dual_public()
    require(system.rank()+system.nullity() == variables and
            system.equations >= 1, "157ei complete affine rank/nullity")
    if not system.consistent:
        require(isinstance(dual, dict) and dual["normalized_rhs"] == 1 and
                dual["yTz_mod3"] == 2 and
                dual["all_108_annihilation_dimension"] == variables and
                dual["support_count"] <= 109 and
                dual["support_count"] <= CAPS["dual_provenance_entries"],
                "157ei normalized B1 dual")
    return {"variables": variables, "rank": system.rank(),
        "nullity": system.nullity(), "consistent": system.consistent,
        "equations": system.equations,
        "row_space_sha256": system.digest(), "dual_witness": dual,
        "dual_support_cap_noncontact": dual is None or
            dual["support_count"] <= 109 < CAPS["dual_provenance_entries"],
        "complete_all_coordinates": True,
        "stopped_at_first_contradiction": False,
        "coordinate_encoding":
            "one-based component plus exact 154-byte blob"}


def _validate_selected_literal_core(coefficients: Sequence[int],
                                    predicted: dict[Any, int],
                                    actual: dict[Any, int], value: Any,
                                    identity: Any) -> None:
    require(len(coefficients) == 108 and all(x in (0, 1, 2)
            for x in coefficients) and value == identity and
            actual == predicted,
            "157ei selected literal affine replay")


def _validate_selected_public_contract(selected: dict[str, Any]) -> None:
    require(set(selected) == {"coefficient_vector",
        "coefficient_vector_sha256", "support", "factor_count",
        "typed_candidate", "target_expression", "direct_gradient",
        "direct_replay", "affine_prediction_equal", "D2_proof",
        "element_registry", "proof_root_node_id",
        "proof_expands_to_selected_gradient", "post_block_anchor_used",
        "targets_7_through_33_not_checked"} and
        len(selected["coefficient_vector"]) == 108 and
        selected["coefficient_vector_sha256"] ==
            sha_obj(selected["coefficient_vector"]) and
        selected["support"] == [index+1 for index, coefficient in
            enumerate(selected["coefficient_vector"]) if coefficient] and
        selected["factor_count"] == sum(selected["coefficient_vector"]) and
        selected["direct_replay"] is True and
        selected["affine_prediction_equal"] is True and
        selected["proof_expands_to_selected_gradient"] is True and
        selected["post_block_anchor_used"] is True and
        selected["targets_7_through_33_not_checked"] is True and
        isinstance(selected["proof_root_node_id"], int) and
        selected["proof_root_node_id"] >= 0,
        "157ei selected public proof contract")


def _solve_transposed_target_core(old: Any, system: Any,
                                  base_remainder: dict[Any, int],
                                  delta_rows: dict[Any, dict[int, int]],
                                  live_remainder_entries: int,
                                  target_monitor: Any, *,
                                  expected_coordinate_count: int | None = None,
                                  trace: dict[str, int] | None = None,
                                  progress: dict[str, Any] | None = None) \
        -> tuple[dict[str, Any], dict[str, Any]]:
    """Shared target-major absorption/classification production core."""
    if trace is not None:
        trace["target_reducer"] = trace.get("target_reducer", 0)+1
    require(all(value in (1, 2) for value in base_remainder.values()) and
            all(row and all(0 <= index < 108 and value in (1, 2)
                for index, value in row.items())
                for row in delta_rows.values()),
            "157ei canonical sparse target rows")
    coordinate_count = len(set(base_remainder).union(delta_rows))
    if expected_coordinate_count is not None:
        require(coordinate_count == expected_coordinate_count,
                "157ei expected target6 coordinate count")
    row = old._affine_target_row_transposed(
        system, base_remainder, delta_rows, 6, live_remainder_entries,
        target_monitor, "hexagon_1_coface_0")
    require(system.equations == coordinate_count and
            row["affine_equations"] == coordinate_count and
            row["ordinal"] == 6 and
            row["coordinate_count"] == coordinate_count,
            "157ei shared target6 complete coordinate absorption")
    dual = system.dual_public()
    if progress is not None:
        progress["completed_equations"] = system.equations
    if not system.consistent and isinstance(dual, dict) and \
            dual["support_count"] > CAPS["dual_provenance_entries"]:
        if progress is not None:
            progress["completed_target_system"] = \
                _completed_target_system_projection(system, coordinate_count)
        raise LaneResource("dual_provenance_entries",
            CAPS["dual_provenance_entries"], dual["support_count"], "gt",
            "target_reduction", {})
    affine = _classify_affine_system(system)
    require(row["consistent"] is affine["consistent"] and
            row["constraint_rank"] == affine["rank"] and
            row["nullity"] == affine["nullity"] and
            row["row_space_sha256"] == affine["row_space_sha256"],
            "157ei shared target6 classification")
    return row, affine


def _selected_replay_and_proof_core(
        coefficients: Sequence[int],
        direct_replay: Callable[[], dict[str, Any]],
        proof_builder: Callable[[dict[str, Any]], dict[str, Any]], *,
        trace: dict[str, int] | None = None) -> dict[str, Any]:
    """Shared selected-literal direct replay and proof callback boundary."""
    if trace is not None:
        trace["selected_core"] = trace.get("selected_core", 0)+1
    require(len(coefficients) == 108 and all(value in (0, 1, 2)
            for value in coefficients), "157ei selected coefficient universe")
    replay = direct_replay()
    require(set(replay) == {"predicted", "actual", "value", "identity",
                            "context"},
            "157ei selected replay callback shape")
    _validate_selected_literal_core(coefficients, replay["predicted"],
        replay["actual"], replay["value"], replay["identity"])
    public = proof_builder(replay)
    _validate_selected_public_contract(public)
    return public


def _completed_target_system_projection(system: Any,
                                        coordinate_count: int) \
        -> dict[str, Any]:
    dual = system.dual_public()
    require(isinstance(dual, dict),
            "157ei completed inconsistent target projection")
    return {"coordinate_count": coordinate_count,
        "rank": system.rank(), "nullity": system.nullity(),
        "consistent": False, "equations": system.equations,
        "row_space_sha256": system.digest(),
        "attempted_dual_support_count": dual["support_count"],
        "attempted_dual_sha256": sha_obj(dual)}


def _target6_system_core(old: Any, seed_info: dict[str, Any], e4: Any,
                         source: dict[str, Any], inverse_words: Sequence[Any],
                         prefix: dict[str, Any], anchor: dict[str, Any],
                         monitor: Monitor, progress: dict[str, Any]) \
        -> tuple[dict[str, Any], Any, dict[Any, int], Any]:
    seeds = seed_info["seed_words"]
    require(len(seeds) == 108 and len(seed_info["new_seed_words"]) == 4 and
            sha_obj(seeds) == SEED_MANIFEST_SHA,
            "157ei exact 108-seed manifest")
    require(source["supported"] is True and source["seed_count"] == 108 and
            source["all_source_tuples_equal"] is True and
            source["all_correction_occurrences_identity"] is True,
            "157ei complete source/context preflight")

    static = old.build_memo_static_quotient_binding(e4)
    base_compiled = old.build_wordexpr_candidate(0, [], inverse_words)
    root = base_compiled["acceptance"][5][2]
    base_eval = old._affine_candidate_values(base_compiled, e4, 0, static,
        pin_sources=True, value_roots=[root])
    base_raw, base_value = old._affine_direct_gradient(
        base_compiled, base_eval, root, e4)
    base_binding = _binding(old, "hexagon_1_coface_0", "hexagon",
                            base_raw, base_value)
    require(base_value == e4.identity and sha_obj(base_binding) ==
            OLD_BASE_GRADIENT_SHA, "157ei target6 actual base gradient")
    empty = old.affine_target6_formula([], e4, include_gradient=True)
    require(empty.pop("_direct_gradient") == {} and
            empty.pop("_direct_value") == e4.identity,
            "157ei empty formula is delta only")
    base_eval.discard_candidate_memo()

    target_monitor = prefix["basis"].deadline
    require(target_monitor is not None and
            target_monitor is prefix["dag"].deadline,
            "157ei target adapter identity")
    anchors = list(anchor["_ids"])
    progress["substage"] = "base_remainder"
    base_rem = old._affine_probe_remainder(base_raw, prefix, anchors,
                                           target_monitor)
    delta_rows: dict[tuple[int, str], dict[int, int]] = {}
    split: list[dict[str, Any]] = []
    remainder_rows: list[dict[str, Any]] = [{"ordinal": 0,
        "kind": "base", "remainder": [[c, h, a] for (c, h), a in
            sorted(base_rem.items(), key=lambda row:(row[0][0],
                bytes.fromhex(row[0][1])))],
        "sha256": sha_obj(sorted(base_rem.items()))}]
    formula_rows: list[dict[str, Any]] = [empty]
    live = len(base_rem)
    direct_bindings: list[dict[str, Any]] = [base_binding]
    progress["remainder_prefix"] = copy.deepcopy(remainder_rows)
    progress["typed_split_prefix"] = []
    for seed_index, seed in enumerate(seeds, 1):
        progress["substage"] = "seed_remainder"
        progress["current_seed"] = seed_index
        target_monitor.check("target_reduction", force=(seed_index % 4 == 0))
        formula = old.affine_target6_formula(seed, e4, include_gradient=True)
        delta = formula.pop("_direct_gradient")
        require(formula.pop("_direct_value") == e4.identity,
                "157ei target6 formula value")
        one = [0]*108; one[seed_index-1] = 1
        typed = old._affine_make_typed_positive(one, seeds, inverse_words)
        typed_target = old._affine_build_typed_target6(typed)
        typed_root = old._affine_select_typed_target_root(typed_target, 6)
        typed_eval = old._affine_candidate_values(typed_target, e4,
            seed_index, static, pin_sources=False, value_roots=[typed_root])
        typed_raw, typed_value = old._affine_direct_gradient(
            typed_target, typed_eval, typed_root, e4)
        predicted = _gradient_add(old, base_raw, delta)
        require(typed_value == e4.identity and typed_raw == predicted,
                "157ei target6 raw affine formula/direct equality")
        binding = _binding(old, "hexagon_1_coface_0", "hexagon",
                           typed_raw, typed_value)
        split.append({"seed_index": seed_index,
            "gradient_sha256": sha_obj(binding), "value_identity": True,
            "direct_replay": True, "typed_replay": True})
        direct_bindings.append(binding); formula_rows.append(formula)
        rem = old._affine_probe_remainder(delta, prefix, anchors,
                                          target_monitor)
        live += len(rem)
        if live > CAPS["target_live_remainders"]:
            raise LaneResource("target_live_remainders",
                CAPS["target_live_remainders"], live, "gt",
                "target_reduction", {"seed_index": seed_index})
        for coordinate, coefficient in rem.items():
            delta_rows.setdefault(coordinate, {})[seed_index-1] = coefficient
        remainder_rows.append({"ordinal": seed_index, "kind": "delta",
            "entry_count": len(rem), "sha256": sha_obj(sorted(rem.items()))})
        progress["evaluated_seeds"] = seed_index
        progress["typed_split_prefix"] = copy.deepcopy(split)
        progress["remainder_prefix"] = copy.deepcopy(remainder_rows)
        typed_eval.discard_candidate_memo()
    require(len(split) == 108 and sha_obj(split) == OLD_TYPED_SPLIT_SHA,
            "157ei exact old target6 direct/typed ledger")

    system = old.AffineSystem(108, coordinate_widths=(e4.degree, e4.pc.n))
    progress["substage"] = "affine_absorption"
    progress["current_seed"] = None
    row, affine = _solve_transposed_target_core(
        old, system, base_rem, delta_rows, live, target_monitor,
        progress=progress)
    target = {"ordinal": 6, "name": "hexagon_1_coface_0",
        "kind": "hexagon", "base_is_direct_not_empty_formula": True,
        "affine_rhs_is_negative_base_remainder": True,
        "empty_formula_is_zero_delta_canary": True,
        "base_gradient": base_binding,
        "base_gradient_sha256": sha_obj(base_binding),
        "formula_checks": formula_rows,
        "formula_checks_sha256": sha_obj(formula_rows),
        "typed_split": split, "typed_split_sha256": sha_obj(split),
        "direct_gradient_bindings_sha256": sha_obj(direct_bindings),
        "direct_vs_typed_count": 108,
        "fresh_remainders": remainder_rows,
        "fresh_remainder_count": len(remainder_rows),
        "fresh_remainder_sha256": sha_obj(remainder_rows),
        "old_B0_remainder_or_dual_imported": False,
        "post_block_anchor_used_for_all_109": True,
        "target_row": row,
        "old_157ec_comparison": {"receipt_sha256":
            "d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d",
            "old104_rank": 50, "full108_rank": 54,
            "old104_comparison_sha256": OLD_TARGET6_ROW_SHA,
            "evidence_only_not_imported": True}}
    return {"seed_manifest": seed_info, "source_preflight": source,
            "target6": target, "affine_system": affine}, system, base_raw, static


def _target6_system(old: Any, seed_info: dict[str, Any], e4: Any,
                    source: dict[str, Any], inverse_words: Sequence[Any],
                    prefix: dict[str, Any], anchor: dict[str, Any],
                    monitor: Monitor) -> tuple[dict[str, Any], Any,
                                               dict[Any, int], Any]:
    progress: dict[str, Any] = {"substage": "typed_formula_setup",
        "evaluated_seeds": 0, "completed_equations": 0,
        "current_seed": None, "typed_split_prefix": [],
        "remainder_prefix": [], "completed_target_system": None}
    basis, dag = prefix["basis"], prefix["dag"]
    require(basis.deadline is None and dag.deadline is None,
            "157ei detached block anchor before target")
    target_monitor = monitor.bind("target_reduction")
    basis.deadline = target_monitor; dag.deadline = target_monitor
    try:
        return _target6_system_core(old, seed_info, e4, source,
            inverse_words, prefix, anchor, monitor, progress)
    except Exception as exc:
        if isinstance(exc, LaneResource):
            exc.current = copy.deepcopy(progress)
        else:
            setattr(exc, "ei_target_current", copy.deepcopy(progress))
        raise
    finally:
        require(basis.deadline is target_monitor and
                dag.deadline is target_monitor,
                "157ei target adapter retained")
        basis.deadline = None; dag.deadline = None


def _selected_proof(old: Any, e4: Any, inverse_words: Sequence[Any],
                    seeds: Sequence[Any], base_raw: dict[Any, int],
                    prefix: dict[str, Any], anchor: dict[str, Any],
                    system: Any, static: Any, monitor: Monitor) -> dict[str, Any]:
    coefficients = system.canonical_solution()
    evaluator_box: dict[str, Any] = {}

    def direct_replay() -> dict[str, Any]:
        typed = old._affine_make_typed_positive(
            coefficients, seeds, inverse_words)
        targets = old._affine_build_typed_target6(typed)
        root = old._affine_select_typed_target_root(targets, 6)
        evaluator = old._affine_candidate_values(targets, e4, 0, static,
            pin_sources=False, value_roots=[root])
        gradient, value = old._affine_direct_gradient(
            targets, evaluator, root, e4)
        predicted = dict(base_raw)
        for index, coefficient in enumerate(coefficients):
            if coefficient:
                detail = old.affine_target6_formula(
                    seeds[index], e4, include_gradient=True)
                old.add_scaled(predicted, detail.pop("_direct_gradient"),
                               coefficient)
                require(detail.pop("_direct_value") == e4.identity,
                        "157ei selected affine delta")
        evaluator_box["evaluator"] = evaluator
        return {"predicted": predicted, "actual": gradient, "value": value,
            "identity": e4.identity, "context": {
                "typed": typed, "targets": targets, "root": root,
                "evaluator": evaluator}}

    def proof_builder(replay: dict[str, Any]) -> dict[str, Any]:
        context = replay["context"]
        typed, targets, root = (context[key]
                                for key in ("typed", "targets", "root"))
        gradient, value = replay["actual"], replay["value"]
        pool, dag, basis, sections = (prefix[k] for k in
                                      ("pool", "dag", "basis", "sections"))
        proof_monitor = monitor.bind("selected_proof")
        snapshot = old.candidate_transaction_snapshot(
            pool, dag, basis, sections, anchor["_ids"])
        basis.deadline = proof_monitor; dag.deadline = proof_monitor
        try:
            packed = old.intern_raw_vector(gradient, pool)
            proof_root = basis.solve(packed)
            require(proof_root is not None,
                    "157ei selected target6 membership")
            registry = old.ElementRegistry({4: e4})
            proof, renumber = old.serialize_proof_dag(
                dag, {"hexagon_1_coface_0": proof_root}, basis, registry)
            require(proof_root in renumber and proof["roots"] == [{
                "name": "hexagon_1_coface_0",
                "node_id": renumber[proof_root]}],
                "157ei selected proof root")
            return {"coefficient_vector": list(coefficients),
                "coefficient_vector_sha256": sha_obj(coefficients),
                "support": [index+1 for index, coefficient in
                            enumerate(coefficients) if coefficient],
                "factor_count": sum(coefficients),
                "typed_candidate": old._affine_typed_candidate_public(typed),
                "target_expression": targets["dag"].serialize_reachable(
                    [("hexagon_1_coface_0", root)]),
                "direct_gradient": _binding(old, "hexagon_1_coface_0",
                    "hexagon", gradient, value),
                "direct_replay": True, "affine_prediction_equal": True,
                "D2_proof": proof, "element_registry": registry.rows,
                "proof_root_node_id": renumber[proof_root],
                "proof_expands_to_selected_gradient": True,
                "post_block_anchor_used": True,
                "targets_7_through_33_not_checked": True}
        finally:
            require(basis.deadline is proof_monitor and
                    dag.deadline is proof_monitor,
                    "157ei selected adapter identity")
            basis.deadline = None; dag.deadline = None
            old.rollback_candidate_transaction(
                snapshot, pool, dag, basis, sections)

    try:
        return _selected_replay_and_proof_core(
            coefficients, direct_replay, proof_builder)
    finally:
        evaluator = evaluator_box.get("evaluator")
        if evaluator is not None:
            evaluator.discard_candidate_memo()


def _partial(phase: str, reason: str, receipt: dict[str, Any],
             current: dict[str, Any]) -> dict[str, Any]:
    block = receipt.get("translation_block", {})
    target = receipt.get("target6", {})
    completed_relators = int(current.get("completed_relators",
        len(block.get("columns", []))))
    evaluated = (int(current.get("evaluated_seeds",
        len(target.get("typed_split", [])))) if phase in
        {"target_reduction", "selected_proof"} else 0)
    typed_prefix = (current.get("typed_split_prefix") if phase in
                    {"target_reduction", "selected_proof"} else None)
    if typed_prefix is None and target and phase in {
            "target_reduction", "selected_proof"}:
        typed_prefix = target.get("typed_split", [])
    return {"phase": phase, "reason": reason,
        "attempted_relators": int(current.get("attempted_relators",
            completed_relators)),
        "completed_relators": completed_relators,
        "raw_completed_relators": int(current.get("raw_completed_relators",
            11 if block else 0)),
        "shadow_completed_relators": int(current.get(
            "shadow_completed_relators", 11 if block else 0)),
        "raw_column_prefix_sha256": (sha_obj(current["raw_prefix"])
            if "raw_prefix" in current else
            block.get("raw_columns_sha256") if block else None),
        "shadow_remainder_prefix_sha256": (sha_obj(current["shadow_prefix"])
            if "shadow_prefix" in current else None),
        "old_qstar_prefix_sha256": (sha_obj(current["scalar_prefix"])
            if "scalar_prefix" in current else
            sha_obj(block.get("old_qstar_scalars", [])) if block else None),
        "rank_gain_so_far": int(current.get("rank_gain_so_far",
            block.get("rank_gain", 0))),
        "source_evaluated_seeds": int(current.get("evaluated_seeds", 0))
            if phase == "source_preflight" else 0,
        "source_records_prefix_sha256": current.get(
            "records_prefix_sha256") if phase == "source_preflight" else None,
        "evaluated_seeds": evaluated,
        "completed_equations": (int(current.get("completed_equations",
            receipt.get("affine_system", {}).get("equations", 0))) if phase in
            {"target_reduction", "selected_proof"} else 0),
        "current_seed": current.get("current_seed",
            current.get("seed_index")),
        "block_digest_prefix": (
            None if "block_prefix" in current and
                not current["block_prefix"] else
            sha_obj(current["block_prefix"])
                if "block_prefix" in current else
            sha_obj(block["columns"]) if block.get("columns") else None),
        "block_pre_accounting": current.get("block_pre_accounting",
            block.get("pre_accounting")),
        "block_post_accounting": current.get("block_post_accounting",
            block.get("post_accounting")),
        "target_ledger_prefix_sha256": (None if typed_prefix is None else
            sha_obj(typed_prefix)),
        "completed_target_system": current.get("completed_target_system"),
        "rollback_anchor_after_block": bool(
            receipt.get("post_block_anchor", {}).get("after_complete_block")),
        "mathematical_claim": "none"}


def _strip_to_stage(receipt: dict[str, Any], phase: str) -> None:
    allowed = stage_fields_before(phase)
    for field in AUTH_FIELDS | SOURCE_FIELDS | PREFIX_FIELDS | LAMBDA_FIELDS | \
            BASE_FIELDS | CORRELATION_FIELDS | SECTION_FIELDS | BLOCK_FIELDS | \
            TARGET_FIELDS | AFFINE_FIELDS | {"normalized_dual", "selected_proof"}:
        if field not in allowed:
            receipt.pop(field, None)


def _source_prefix_rows(old: Any, e4: Any, count: int) \
        -> list[dict[str, Any]]:
    require(0 <= count <= 108, "157ei source prefix count")
    contexts, _, context_public = old.cheap_context_registry(e4)
    ids = list(range(1, len(contexts)+1))
    require(len(contexts) == 31 and
            context_public["named_use_count"] == 46,
            "157ei source prefix registry")
    return [{"seed_index": index, "source_tuple_equal": True,
        "correction_context_count": len(contexts),
        "correction_contexts_sha256": sha_obj(ids),
        "named_use_count": context_public["named_use_count"],
        "context_registry_unique_count": len(contexts),
        "context_registry_sha256": sha_obj(context_public)}
        for index in range(1, count+1)]


def _finalize_normal_terminal(receipt: dict[str, Any], system: Any,
                              selected: dict[str, Any] | None, *,
                              trace: dict[str, int] | None = None) -> str:
    """Shared normal terminal finalizer; no fixture-only schema branch."""
    if trace is not None:
        trace["normal_finalizer"] = trace.get("normal_finalizer", 0)+1
    require(receipt.get("translation_block", {}).get("complete") is True and
            "target6" in receipt and "affine_system" in receipt and
            receipt["affine_system"]["consistent"] is system.consistent,
            "157ei normal finalizer completed inputs")
    receipt.pop("selected_proof", None); receipt.pop("normalized_dual", None)
    if system.consistent:
        require(selected is not None, "157ei consistent selected proof")
        _validate_selected_public_contract(selected)
        receipt["selected_proof"] = selected
        token = "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT"
        reason = \
            "complete_target6_affine_system_consistent_with_selected_proof"
    else:
        require(selected is None and system.dual_public() is not None and
                receipt["affine_system"]["dual_witness"] ==
                    system.dual_public(),
                "157ei inconsistent normalized dual")
        receipt["normalized_dual"] = system.dual_public()
        token = "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT"
        reason = \
            "complete_target6_affine_system_inconsistent_with_normalized_dual"
    receipt["terminal_token"] = receipt["status"] = token
    receipt["reason"] = reason; receipt["phase"] = "complete"
    receipt["claims"] = claim_row(token, True)
    return token


def run(q3_path: Path, *, seconds: float = 18_000.0) -> dict[str, Any]:
    monitor = Monitor(seconds); phases: dict[str, float] = {}
    phase_started = time.monotonic(); phase = "authenticated_input"
    upstream: dict[str, int] = {}; receipt = base_receipt(q3_path, monitor, upstream)
    eh = eg = ed = old = None; prefix = None

    def close(label: str) -> None:
        nonlocal phase_started
        now = time.monotonic(); phases[label] = now-phase_started; phase_started = now
        print("D972_B345_LEXBLOCK_TARGET6_PHASE " + label +
              f" elapsed_s={phases[label]:.6f}", flush=True)

    try:
        authenticate_static()
        if q3_path.resolve() != (ROOT/Q3_PATH).resolve() or \
                not q3_path.is_file() or sha_file(q3_path) != Q3_SHA:
            raise InputFailure("q3 artifact path/SHA drift")
        eh = load_eh(); eg = eh.load_v1(); ed = eg.load_ed()
        upstream = eg.upstream_caps(ed)
        receipt = base_receipt(q3_path, monitor, upstream)
        try:
            q3, old = ed.authenticated_input(q3_path)
        except ed.AffineInput as exc:
            raise InputFailure(str(exc)) from exc
        e3, e4, _ = old.reconstruct_quotients(q3)
        require(e4.degree == 144 and e4.pc.n == 10,
                "157ei E4 canonical width")
        receipt["base_q3_replay"] = old.replay_base_q3(q3, e3, e4)
        normalized, raw_source_key, inverse_words = \
            old.normalized_inverse_fibre(q3, e4)
        receipt["normalized_inverse_fibre"] = normalized
        seed_info = old.affine_seed_words(q3, e3)
        require(len(seed_info["seed_words"]) == 108 and
                sha_obj(seed_info["seed_words"]) == SEED_MANIFEST_SHA,
                "157ei seed manifest authentication")
        receipt["seed_manifest"] = seed_info
        close(phase)

        phase = "source_preflight"
        source_monitor = monitor.bind(phase)
        source_progress: dict[str, Any] = {"current_seed": None,
            "evaluated_seeds": 0,
            "records_prefix_sha256": sha_obj([])}

        class SourceProgressMonitor:
            @property
            def started(self) -> float:
                return source_monitor.started

            @property
            def deadline(self) -> float:
                return source_monitor.deadline

            def progress(self, index: int) -> None:
                source_progress["current_seed"] = index
                source_progress["evaluated_seeds"] = index-1

            def check(self, inner: str, force: bool = False, **kw: Any) -> None:
                current = int(source_progress["current_seed"] or 0)
                source_progress["evaluated_seeds"] = current
                source_monitor.check(inner, force=force, **kw)

            def reserve(self, inner: str, additional_bytes: int) -> None:
                source_monitor.reserve(inner, additional_bytes)

        tracked_source_monitor = SourceProgressMonitor()
        try:
            source = old._affine_source_preflight(seed_info["seed_words"], e4,
                tuple(raw_source_key), inverse_words, tracked_source_monitor,
                progress=tracked_source_monitor.progress)
        except old.ResourceStop as exc:
            source_progress["records_prefix_sha256"] = sha_obj(
                _source_prefix_rows(old, e4,
                    int(source_progress["evaluated_seeds"])))
            raise convert_upstream(exc, upstream, phase,
                                   source_progress) from exc
        except LaneResource as exc:
            source_progress["records_prefix_sha256"] = sha_obj(
                _source_prefix_rows(old, e4,
                    int(source_progress["evaluated_seeds"])))
            exc.current = copy.deepcopy(source_progress)
            raise
        require(source["supported"] is True, "157ei source preflight")
        receipt["source_preflight"] = source; close(phase)

        phase = "fresh_immutable_prefix"
        fresh = monitor.bind(phase); fresh.check(phase, force=True)
        try:
            prefix, dependent = ed.build_instrumented_prefix(
                old, e4, fresh, raw_source_key)
        except (old.ResourceStop, ed.ResourceStop) as exc:
            raise convert_upstream(exc, upstream, phase, {}) from exc
        require(prefix["dag"].deadline is fresh and
                prefix["basis"].deadline is fresh,
                "157ei fresh adapter retained")
        prefix["dag"].deadline = None; prefix["basis"].deadline = None
        pool = prefix["pool"]
        require(tuple(prefix["raw_source_tuple"]) == tuple(raw_source_key) and
                tuple(pool.value(i) for i in prefix["base_source_key"]) ==
                    tuple(raw_source_key), "157ei prefix source anchors")
        receipt["directed_base_support"] = prefix["directed_base_support"]
        receipt["directed_surgery"] = prefix["directed_surgery"]
        receipt["prefix"] = _prefix_public(old, prefix, dependent, ed)
        receipt["monitor_scope"] = monitor_scope(True)
        close(phase)

        phase = "raw_lambda_oracle"
        raw_monitor = monitor.bind(phase); raw_monitor.check(phase, force=True)
        try:
            qstar = ed.validate_qstar_label(ed.QSTAR_LABEL, 154)
            oracle = ed.RawLambdaOracle(old, prefix, qstar, raw_monitor)
        except (old.ResourceStop, ed.ResourceStop) as exc:
            raise convert_upstream(exc, upstream, phase, {}) from exc
        pivot_zero = [oracle.packed(prefix["basis"].rows[pivot][0])
            for pivot in sorted(prefix["basis"].rows, key=pool.pivot_order)]
        require(pivot_zero == [0]*362709, "157ei qstar kills B0 pivots")
        receipt["lambda_oracle"] = {**oracle.public,
            "pivot_annihilation_count": len(pivot_zero),
            "pivot_annihilation_sha256": sha_obj(pivot_zero)}
        support = eg.lambda_support(oracle, 154)
        require(support["count"] == 78 and
                support["per_component"] == [43, 9, 11, 15, 0, 0],
                "157ei qstar support")
        receipt["lambda_support"] = support; close(phase)

        phase = "base_columns"; monitor.bind(phase).check(phase, force=True)
        bundle = eg.rebuild_base_bundle(old, prefix, e4)
        require(bundle["public"]["ordered_sha256"] == BASE_OCCURRENCE_SHA,
                "157ei base occurrence digest")
        receipt["base_columns"] = bundle["public"]; close(phase)

        phase = "dual_correlation"; dual_monitor = monitor.bind(phase)
        dual_monitor.check(phase, force=True)
        before = eg.state_snapshot(prefix)
        mul, inverse = eg.uncached_ops(old, e4)
        corr = eg.exact_correlation(support["rows"],
            bundle["private_occurrences"], width=154, unpack=pool.unpack,
            mul=mul, inverse=inverse, pack=pool.pack,
            monitor=dual_monitor)
        canaries = eg.correlation_canaries(corr, support["rows"],
            bundle["private_occurrences"], width=154, identity=e4.identity,
            unpack=pool.unpack, mul=mul, pack=pool.pack)
        after = eg.state_snapshot(prefix)
        require(before == after, "157ei correlation state neutrality")
        receipt["correlation"] = corr["public"]
        receipt["direct_canaries"] = canaries
        receipt["state_no_mutation"] = {"before": eg.public_snapshot(before),
            "after": eg.public_snapshot(after), "exact_equal": True,
            "pool_ID_or_basis_mutation": False}
        close(phase)

        phase = "section_witness"; section_monitor = monitor.bind(phase)
        section_monitor.check(phase, force=True)
        try:
            witness = eg.make_section_witness(old, e4, prefix,
                bundle["private_occurrences"], corr, section_monitor)
        except (old.ResourceStop, ed.ResourceStop) as exc:
            raise convert_upstream(exc, upstream, phase, {}) from exc
        _require_correlation(corr, witness)
        receipt["section_witness"] = witness; close(phase)

        phase = "block_insertion"
        try:
            block, anchor = _commit_block(old, eg, prefix, oracle, monitor)
        except (old.ResourceStop, ed.ResourceStop) as exc:
            current = getattr(exc, "ei_block_current", None)
            require(isinstance(current, dict),
                    "157ei block resource progress binding")
            raise convert_upstream(exc, upstream, phase, current) from exc
        receipt["translation_block"] = block
        public_anchor = {k: v for k, v in anchor.items()
                         if not k.startswith("_")}
        receipt["post_block_anchor"] = public_anchor; close(phase)

        phase = "target_reduction"
        try:
            target_data, system, base_raw, static = _target6_system(
                old, seed_info, e4, source, inverse_words,
                prefix, anchor, monitor)
        except old.ResourceStop as exc:
            current = getattr(exc, "ei_target_current", None)
            require(isinstance(current, dict),
                    "157ei target resource progress binding")
            raise convert_upstream(exc, upstream, phase, current) from exc
        require(target_data["source_preflight"] == receipt["source_preflight"]
                and target_data["seed_manifest"] == receipt["seed_manifest"],
                "157ei single preflight handoff equality")
        receipt["target6"] = target_data["target6"]
        receipt["affine_system"] = target_data["affine_system"]
        close(phase)
        if system.consistent:
            phase = "selected_proof"
            try:
                selected = _selected_proof(old, e4, inverse_words,
                    seed_info["seed_words"], base_raw, prefix, anchor,
                    system, static, monitor)
            except old.ResourceStop as exc:
                raise convert_upstream(exc, upstream, phase,
                    {"evaluated_seeds": 108,
                     "completed_equations": system.equations,
                     "current_seed": None}) from exc
            close(phase)
        else:
            require(system.dual_public() is not None,
                    "157ei inconsistent dual existence")
            selected = None
        _finalize_normal_terminal(receipt, system, selected)
    except InputFailure as exc:
        receipt = base_receipt(q3_path, monitor, upstream)
        receipt["input_errors"] = [str(exc)]
    except LaneResource as exc:
        monitor.hit_reason = exc.key
        token = "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE"
        receipt["terminal_token"] = receipt["status"] = token
        receipt["reason"] = exc.key; receipt["phase"] = exc.phase
        receipt["claims"] = claim_row(token,
            bool(receipt.get("translation_block", {}).get("complete")))
        receipt["resource_guards"] = {"resource_hit": True,
            "resource": exc.public(), "atomic_partial": True}
        receipt["partial"] = _partial(exc.phase, exc.key, receipt, exc.current)
        receipt["monitor_scope"] = monitor_scope(
            "prefix" in receipt, exc.diagnostic())
        _strip_to_stage(receipt, exc.phase)
    receipt["performance"] = performance_record(monitor, phases)
    validate_receipt_schema(receipt)
    return receipt


def _canonical_bytes(receipt: dict[str, Any]) -> bytes:
    for _ in range(12):
        raw = (json.dumps(receipt, sort_keys=True,
            separators=(",", ":"))+"\n").encode("utf-8")
        if receipt["performance"]["receipt_bytes"] == len(raw):
            return raw
        receipt["performance"]["receipt_bytes"] = len(raw)
    raise RuntimeError("157ei receipt-byte fixed point")


def write_checked(path: Path, receipt: dict[str, Any]) -> None:
    raw = _canonical_bytes(receipt)
    if len(raw) > CAPS["packed_receipt_bytes"]:
        raise LaneResource("packed_receipt_bytes", CAPS["packed_receipt_bytes"],
            len(raw), "gt", "receipt_serialization", {})
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+".tmp")
    temporary.write_bytes(raw)
    require(temporary.read_bytes() == raw, "157ei temporary readback")
    os.replace(temporary, path)
    require(path.read_bytes() == raw, "157ei final readback")


def finalize_serialization_resource(receipt: dict[str, Any],
                                    exc: LaneResource, *,
                                    fixture: bool = False) -> None:
    require(exc.key == "packed_receipt_bytes" and
            exc.phase == "receipt_serialization", "157ei serialization stop")
    token = "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE"
    receipt["terminal_token"] = receipt["status"] = token
    receipt["reason"] = exc.key; receipt["phase"] = exc.phase
    receipt["claims"] = claim_row(token,
        bool(receipt.get("translation_block", {}).get("complete")))
    receipt["resource_guards"] = {"resource_hit": True,
        "resource": exc.public(), "atomic_partial": True}
    receipt["partial"] = _partial(exc.phase, exc.key, receipt, {})
    receipt["performance"]["hit_reason"] = exc.key
    _strip_to_stage(receipt, exc.phase)
    validate_receipt_schema(receipt, fixture=fixture)


def write_with_fallback(path: Path, receipt: dict[str, Any], *,
                        fixture: bool = False) -> bool:
    try:
        write_checked(path, receipt); return False
    except LaneResource as exc:
        finalize_serialization_resource(receipt, exc, fixture=fixture)
        write_checked(path, receipt); return True


def _expect_failure(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (RuntimeError, ValueError, TypeError, AttributeError):
        return
    raise RuntimeError("157ei selftest mutation accepted: "+label)


def _fixture_old_producer() -> Any:
    name = "_d972_157ei_fixture_157ec_producer"
    module = sys.modules.get(name)
    if module is not None:
        return module
    spec = importlib.util.spec_from_file_location(name, ROOT/EC_PRODUCER)
    require(spec is not None and spec.loader is not None,
            "157ei fixture producer import")
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None); raise
    require(module.AFFINE_SCHEMA == "d972-b345-seedspan-triple4/v1",
            "157ei fixture pinned affine module")
    return module


def _fixture_accounting(columns: int, pivots: int, dependent: int,
                        live: int) -> dict[str, Any]:
    registered = 0 if columns == 0 else 1
    return {"columns": columns, "pivots": pivots, "dependent": dependent,
        "live_sparse_entries": live, "pool_size": 16+pivots,
        "pool_order_sha256": sha_obj([columns, pivots, dependent, live]),
        "DAG_nodes": 1+pivots, "DAG_edges": pivots,
        "section_bindings": registered, "section_expression_nodes": 1,
        "section_expression_edges": 0}


def _fixture_block(trace: dict[str, int]) \
        -> tuple[dict[str, Any], dict[str, Any]]:
    vectors = [{index: 1} for index in range(1, 12)]
    scalar_rows = [0]*8+[1, 0, 0]
    pivots: dict[int, dict[int, int]] = {}
    dependent = 0
    columns = 0
    blobs = [(bytes([index])+bytes(153)).hex()
             for index in range(1, 12)]
    raw_rows = [{"entries": [[1, blobs[index-1], 1]],
        "entry_count": 1, "byte_length": 156,
        "sha256": sha_bytes(bytes([1])+bytes.fromhex(blobs[index-1])+
                            bytes([1])),
        "encoding": "component-u8|E4-blob-154|coefficient-u8",
        "order": "component then exact canonical E4 bytes"}
        for index in range(1, 12)]
    shadow = [[[1, blobs[index-1], 1]] for index in range(1, 12)]
    pre = _fixture_accounting(0, 0, 0, 0)
    progress = {"attempted_relators": 0, "completed_relators": 0,
        "rank_gain_so_far": 0, "block_prefix": [],
        "block_pre_accounting": pre, "block_post_accounting": dict(pre),
        "current_relator": None, "substage": "persistent_columns",
        "raw_prefix": list(raw_rows), "shadow_prefix": list(shadow),
        "scalar_prefix": list(scalar_rows), "raw_completed_relators": 11,
        "shadow_completed_relators": 11}

    def accounting(pool_digest: bool) -> dict[str, Any]:
        del pool_digest
        return _fixture_accounting(columns, len(pivots), dependent,
                                   len(pivots))

    def add_column(relator: int) -> tuple[bool, dict[str, Any] | None]:
        nonlocal columns, dependent
        source = vectors[relator-1]
        row = dict(source)
        while row:
            pivot = min(row); prior = pivots.get(pivot)
            if prior is None:
                pivots[pivot] = row; break
            coefficient = row[pivot]
            for key, value in prior.items():
                updated = (row.get(key, 0)-coefficient*value) % 3
                if updated: row[key] = updated
                else: row.pop(key, None)
        independent = bool(row)
        columns += 1
        if not independent:
            dependent += 1
        pivot = None if not independent else {"component": 1,
            "element_hex": blobs[relator-1],
            "reduced_row": raw_rows[relator-1]}
        return independent, pivot

    ledger, gain, rank, before9, after9, post = \
        _absorb_ordered_block_core(raw_rows, scalar_rows, shadow, pre,
            add_column, accounting, progress, frozen_counts=False, trace=trace)
    block = {"complete": True, "translation_ordinal": 32976,
        "translation_hex": FIRST_T_HEX, "section_newly_registered": True,
        "section_word_length": 24, "section_word_sha256": FIRST_T_WORD_SHA,
        "columns": ledger, "column_count": 11,
        "column_order": "relator indices 1 through 11",
        "old_qstar_scalars": scalar_rows,
        "raw_columns_sha256": sha_obj([row["raw_column"] for row in ledger]),
        "reducer_ledger_sha256": sha_obj(ledger),
        "pre_accounting": pre, "post_accounting": post,
        "rank_gain": gain, "shadow_rank_mod_B0": rank,
        "two_rank_computations_equal": True,
        "relator9_independent": True,
        "pivot_count_before_relator9": before9,
        "pivot_count_after_relator9": after9,
        "lexfirst_active_provenance": {"component": 4,
            "relator_index": 9, "scalar": 1,
            "translation_hex": FIRST_T_HEX,
            "section_word_sha256": FIRST_T_WORD_SHA},
        "all_11_rows_are_D2_columns": True}
    counts = {"columns": 11, "pivots": len(pivots),
        "dependent": 11-len(pivots), "live_sparse_entries": len(pivots)}
    anchor = {"after_complete_block": True, "basis_columns": 11,
        "basis_pivots": len(pivots), "basis_dependent": 11-len(pivots),
        "basis_live_sparse_entries": len(pivots), "pool_size": 16+len(pivots),
        "DAG_nodes": 1+len(pivots), "DAG_edges": len(pivots),
        "section_bindings": 1, "translation_retained": True,
        "anchor_semantic_sha256": sha_obj({"basis_counts": counts,
            "translation_hex": FIRST_T_HEX,
            "columns_sha256": block["raw_columns_sha256"]}),
        "private_anchor_ids_not_exported": True}
    return block, anchor


def _fixture_affine(old: Any, consistent: bool, trace: dict[str, int]) \
        -> tuple[Any, dict[str, Any], dict[str, Any]]:
    system = old.AffineSystem(108, (1, 0))
    base: dict[tuple[int, str], int] = {}
    deltas: dict[tuple[int, str], dict[int, int]] = {}
    base[(1, "00")] = 2
    base[(1, "01")] = 2 if consistent else 1
    deltas[(1, "00")] = {0: 1}
    deltas[(1, "01")] = {0: 1}
    for index in range(1, 108):
        deltas[(1, f"{index+1:02x}")] = {index: 1}
    row, public = _solve_transposed_target_core(
        old, system, base, deltas,
        sum(len(item) for item in deltas.values())+len(base), None,
        expected_coordinate_count=109, trace=trace)
    require(public["consistent"] is consistent and
            public["equations"] == 109 and row["coordinate_count"] == 109,
            "157ei fixture complete 108-variable system")
    def mul(left: tuple[int, ...], right: tuple[int, ...]) \
            -> tuple[int, ...]:
        return tuple(left[right[index]-1] for index in range(3))
    g = (2, 3, 1); h = (2, 1, 3); ordered = mul(g, h)
    require(ordered != mul(h, g), "157ei fixture target noncommutativity")
    target = {"ordinal": 6, "name": "hexagon_1_coface_0",
        "base_is_direct_not_empty_formula": True,
        "affine_rhs_is_negative_base_remainder": True,
        "base_remainder_sha256": sha_obj(sorted(base.items())),
        "delta_rows_sha256": sha_obj(sorted(deltas.items())),
        "target_row": row, "noncommutative_formula_canary": {
            "operation": "PRODUCT(g,INVERSE(INVERSE(h)))",
            "g": list(g), "h": list(h), "ordered_value": list(ordered),
            "reversed_value": list(mul(h, g)), "ordered_not_reversed": True},
        "first_contradiction_canary": {"coordinate_ordinal": 2,
            "rows_after_coordinate": 107,
            "full_equation_count": system.equations,
            "consistent_fixture": consistent},
        "old_B0_remainder_or_dual_imported": False,
        "post_block_anchor_used_for_all_109": True}
    return system, public, target


def _fixture_selected(system: Any, trace: dict[str, int]) -> dict[str, Any]:
    coefficients = system.canonical_solution()

    def mul(left: tuple[int, ...], right: tuple[int, ...]) \
            -> tuple[int, ...]:
        return tuple(left[right[index]-1] for index in range(3))

    identity = (1, 2, 3); g = (2, 3, 1); h = (2, 1, 3)
    require(mul(g, h) != mul(h, g),
            "157ei fixture noncommutative selected replay")

    def direct_replay() -> dict[str, Any]:
        literal = mul(g, h)
        gradient = {("toy", literal): 1}
        return {"predicted": dict(gradient), "actual": gradient,
            "value": identity, "identity": identity,
            "context": {"literal": literal}}

    def proof_builder(replay: dict[str, Any]) -> dict[str, Any]:
        require(replay["context"]["literal"] == mul(g, h),
                "157ei fixture ordered noncommutative literal")
        return {"coefficient_vector": list(coefficients),
            "coefficient_vector_sha256": sha_obj(coefficients),
            "support": [index+1 for index, value in enumerate(coefficients)
                        if value], "factor_count": sum(coefficients),
            "typed_candidate": {"fixture": "ordered-noncommutative-literal",
                "value": list(replay["context"]["literal"])},
            "target_expression": {"fixture": "typed-target6-product"},
            "direct_gradient": {"fixture": "nonzero-base-direct"},
            "direct_replay": True, "affine_prediction_equal": True,
            "D2_proof": {"roots": [{"name": "hexagon_1_coface_0",
                                      "node_id": 0}]},
            "element_registry": [], "proof_root_node_id": 0,
            "proof_expands_to_selected_gradient": True,
            "post_block_anchor_used": True,
            "targets_7_through_33_not_checked": True}

    return _selected_replay_and_proof_core(
        coefficients, direct_replay, proof_builder, trace=trace)


def _fixture_receipt(token: str, block: dict[str, Any],
                     anchor: dict[str, Any], system: Any,
                     affine: dict[str, Any],
                     target: dict[str, Any],
                     selected: dict[str, Any] | None,
                     trace: dict[str, int]) -> dict[str, Any]:
    monitor = Monitor(30.0); upstream = {"toy_upstream": 7}
    row = base_receipt(ROOT/Q3_PATH, monitor, upstream)
    row["pins"] = {}; row["monitor_scope"] = monitor_scope(True)
    row.update({"base_q3_replay": {}, "normalized_inverse_fibre": {},
        "seed_manifest": {}, "source_preflight": {},
        "directed_base_support": {}, "directed_surgery": {}, "prefix": {},
        "lambda_oracle": {}, "lambda_support": {}, "base_columns": {},
        "correlation": {}, "direct_canaries": {},
        "state_no_mutation": {}, "section_witness": {},
        "translation_block": block, "post_block_anchor": anchor,
        "target6": target,
        "affine_system": affine})
    row["input_errors"] = []
    actual = _finalize_normal_terminal(
        row, system, selected, trace=trace)
    require(actual == token, "157ei fixture finalizer token")
    completed = PHASE_SEQUENCE if token == \
        "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT" else PHASE_SEQUENCE[:-1]
    row["performance"] = performance_record(
        monitor, {name: 0.0 for name in completed})
    validate_receipt_schema(row, fixture=True)
    return row


def self_test() -> None:
    """Bounded shared-production-core fixture; no q3, GAP, or large prefix."""
    authenticate_static()
    inherited = load_eh()
    inherited.self_test()
    old = _fixture_old_producer()
    trace: dict[str, int] = {}
    block, anchor = _fixture_block(trace)
    consistent_system, consistent_public, consistent_target = \
        _fixture_affine(old, True, trace)
    inconsistent_system, inconsistent_public, inconsistent_target = \
        _fixture_affine(
        old, False, trace)
    selected = _fixture_selected(consistent_system, trace)
    consistent = _fixture_receipt(
        "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT", block, anchor,
        consistent_system, consistent_public, consistent_target,
        selected, trace)
    inconsistent = _fixture_receipt(
        "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT", block, anchor,
        inconsistent_system, inconsistent_public, inconsistent_target,
        None, trace)
    completed_fixture_entries = 0

    def validate_completed_fixture(row: dict[str, Any]) -> None:
        """Production schema plus freshly derived sealed target binding."""
        nonlocal completed_fixture_entries
        validate_receipt_schema(row, fixture=True)
        token = row["terminal_token"]
        if token == "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT":
            expected_target, expected_affine = (consistent_target,
                                                 consistent_public)
        elif token == "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT":
            expected_target, expected_affine = (inconsistent_target,
                                                 inconsistent_public)
        else:
            return
        require(row["target6"] == expected_target and
                row["affine_system"] == expected_affine,
                "157ei completed fixture fresh target/affine binding")
        completed_fixture_entries += 1

    validate_completed_fixture(consistent)
    validate_completed_fixture(inconsistent)
    require(trace == {"block_core": 1, "target_reducer": 2,
                      "selected_core": 1, "normal_finalizer": 2},
            "157ei fixture shared production-core entries")

    input_monitor = Monitor(30.0); input_row = base_receipt(
        ROOT/Q3_PATH, input_monitor, {"toy_upstream": 7})
    input_row["pins"] = {}; input_row["input_errors"] = ["toy missing pin"]
    validate_receipt_schema(input_row, fixture=True)
    resource_monitor = Monitor(30.0)
    pre_accounting = block["pre_accounting"]
    current = {"attempted_relators": 3, "completed_relators": 0,
        "rank_gain_so_far": 0, "block_prefix": [],
        "block_pre_accounting": pre_accounting,
        "block_post_accounting": pre_accounting,
        "current_relator": 3, "substage": "shadow_remainders",
        "raw_prefix": [row["raw_column"] for row in block["columns"][:3]],
        "shadow_prefix": [row["raw_column"]["entries"]
                          for row in block["columns"][:2]],
        "scalar_prefix": [0, 0], "raw_completed_relators": 3,
        "shadow_completed_relators": 2}
    resource_stop = LaneResource("common_math_soft_deadline_seconds",
        CAPS["common_math_soft_deadline_seconds"],
        CAPS["common_math_soft_deadline_seconds"], "ge",
        "block_insertion", current, inner="block_insertion",
        callback_api="check")
    resource_monitor.hit_reason = resource_stop.key
    resource_row = copy.deepcopy(consistent)
    resource_row["pins"] = {}
    resource_row["terminal_token"] = resource_row["status"] = \
        "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE"
    resource_row["reason"] = resource_stop.key
    resource_row["phase"] = resource_stop.phase
    resource_row["claims"] = claim_row(resource_row["terminal_token"], False)
    resource_row["resource_guards"] = {"resource_hit": True,
        "resource": resource_stop.public(), "atomic_partial": True}
    resource_row["partial"] = _partial(resource_stop.phase,
        resource_stop.key, resource_row, current)
    require(resource_row["partial"]["block_digest_prefix"] is None,
            "157ei explicit empty block prefix is absent digest")
    prefix_current = copy.deepcopy(current)
    prefix_current["block_prefix"] = copy.deepcopy(block["columns"][:1])
    prefix_partial = _partial(resource_stop.phase, resource_stop.key,
                              resource_row, prefix_current)
    require(prefix_partial["block_digest_prefix"] ==
                sha_obj(prefix_current["block_prefix"]),
            "157ei explicit nonempty block prefix digest")
    fallback_current = copy.deepcopy(current)
    fallback_current.pop("block_prefix")
    fallback_partial = _partial(resource_stop.phase, resource_stop.key,
                                resource_row, fallback_current)
    require(fallback_partial["block_digest_prefix"] ==
                sha_obj(block["columns"]),
            "157ei absent block prefix uses completed block")
    resource_row["monitor_scope"] = monitor_scope(
        True, resource_stop.diagnostic())
    resource_row["performance"] = performance_record(resource_monitor,
        {name: 0.0 for name in
         PHASE_SEQUENCE[:PHASE_SEQUENCE.index("block_insertion")]})
    _strip_to_stage(resource_row, resource_stop.phase)
    validate_receipt_schema(resource_row, fixture=True)

    mutation_count = 0
    def reject_receipt_mutation(row: dict[str, Any], label: str) -> None:
        nonlocal mutation_count
        _expect_failure(lambda: validate_completed_fixture(row),
                        label)
        mutation_count += 1

    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"] = \
        bad["translation_block"]["columns"][:-1]
    reject_receipt_mutation(bad, "complete block omitted column")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"] = [copy.deepcopy(
        bad["translation_block"]["columns"][8])]
    reject_receipt_mutation(bad, "relator9-only incomplete block")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"][1] = copy.deepcopy(
        bad["translation_block"]["columns"][0])
    reject_receipt_mutation(bad, "complete block duplicate column")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"][0], \
        bad["translation_block"]["columns"][1] = \
        bad["translation_block"]["columns"][1], \
        bad["translation_block"]["columns"][0]
    reject_receipt_mutation(bad, "complete block reordered columns")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"][3]["relator_index"] = 5
    reject_receipt_mutation(bad, "complete block relator index")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"][0]["translation_hex"] = "00"*154
    reject_receipt_mutation(bad, "complete block translation blob")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"][0]["raw_column"]["sha256"] = \
        "00"*32
    reject_receipt_mutation(bad, "complete block raw digest")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["old_qstar_scalars"][0] = 1
    reject_receipt_mutation(bad, "relator1 old-qstar nonzero")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["old_qstar_scalars"][8] = 2
    reject_receipt_mutation(bad, "relator9 old-qstar not one")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["section_newly_registered"] = False
    reject_receipt_mutation(bad, "section registration not pool")
    bad = copy.deepcopy(consistent)
    bad["post_block_anchor"]["after_complete_block"] = False
    reject_receipt_mutation(bad, "pre-block rollback anchor")
    bad = copy.deepcopy(consistent)
    bad["target6"]["base_is_direct_not_empty_formula"] = False
    reject_receipt_mutation(bad, "formula empty used as base")
    bad = copy.deepcopy(consistent)
    bad["target6"]["affine_rhs_is_negative_base_remainder"] = False
    reject_receipt_mutation(bad, "affine rhs sign reversal")
    bad = copy.deepcopy(consistent)
    bad["target6"]["old_B0_remainder_or_dual_imported"] = True
    reject_receipt_mutation(bad, "old B0 remainder import")
    bad = copy.deepcopy(consistent)
    canary = bad["target6"]["noncommutative_formula_canary"]
    canary["ordered_value"] = list(canary["reversed_value"])
    reject_receipt_mutation(bad, "target noncommutative order")
    bad = copy.deepcopy(inconsistent)
    bad["target6"]["first_contradiction_canary"][
        "rows_after_coordinate"] = 0
    reject_receipt_mutation(bad, "stopped at first contradiction")
    bad = copy.deepcopy(inconsistent)
    bad["target6"]["first_contradiction_canary"][
        "full_equation_count"] = 2
    reject_receipt_mutation(bad, "incomplete contradiction system")
    bad = copy.deepcopy(inconsistent)
    bad["target6"]["delta_rows_sha256"] = "00"*32
    reject_receipt_mutation(bad, "target delta-row digest")
    bad = copy.deepcopy(inconsistent)
    bad["target6"]["target_row"]["row_space_sha256"] = "00"*32
    reject_receipt_mutation(bad, "target row-space digest")
    bad = copy.deepcopy(consistent)
    bad["selected_proof"]["coefficient_vector"][0] = \
        (bad["selected_proof"]["coefficient_vector"][0]+1) % 3
    reject_receipt_mutation(bad, "selected coefficient value")
    bad = copy.deepcopy(consistent)
    bad["selected_proof"]["support"] = []
    reject_receipt_mutation(bad, "selected support")
    bad = copy.deepcopy(consistent)
    bad["selected_proof"]["proof_root_node_id"] = -1
    reject_receipt_mutation(bad, "selected proof root")
    bad = copy.deepcopy(resource_row); bad["selected_proof"] = selected
    reject_receipt_mutation(bad, "stale positive field in resource")
    bad = copy.deepcopy(input_row); bad["translation_block"] = block
    reject_receipt_mutation(bad, "stale mathematical field in input")

    bad = copy.deepcopy(block); bad["old_qstar_scalars"][0] = 1
    _expect_failure(lambda: _validate_block_reducer_contract(
        bad["columns"], bad["old_qstar_scalars"], bad["pre_accounting"],
        bad["post_accounting"], bad["shadow_rank_mod_B0"],
        bad["pivot_count_before_relator9"],
        bad["pivot_count_after_relator9"], frozen_counts=False),
        "nonzero relator1-8")
    bad = copy.deepcopy(block); bad["columns"][8]["independent"] = False
    _expect_failure(lambda: _validate_block_reducer_contract(
        bad["columns"], bad["old_qstar_scalars"], bad["pre_accounting"],
        bad["post_accounting"], bad["shadow_rank_mod_B0"],
        bad["pivot_count_before_relator9"],
        bad["pivot_count_after_relator9"], frozen_counts=False),
        "dependent relator9")
    bad = copy.deepcopy(consistent); bad["selected_proof"][
        "coefficient_vector"] = list(reversed(
            bad["selected_proof"]["coefficient_vector"]))
    _expect_failure(lambda: validate_receipt_schema(bad, fixture=True),
                    "coefficient order/hash drift")
    bad = copy.deepcopy(inconsistent); bad["selected_proof"] = selected
    _expect_failure(lambda: validate_receipt_schema(bad, fixture=True),
                    "stale selected field")
    bad = copy.deepcopy(resource_row)
    bad["resource_guards"]["resource"]["current"][
        "attempted_relators"] = 5
    _expect_failure(lambda: validate_receipt_schema(bad, fixture=True),
                    "mid-block attempted/current drift")

    callback_monitor = Monitor(30.0)
    for outer, inners in MONITOR_REGISTRY.items():
        bound = callback_monitor.bind(outer)
        for inner in inners:
            bound.check(inner)
    _expect_failure(lambda: callback_monitor.bind("block_insertion").check(
        "raw_lambda_reverse_dp"), "monitor cross-scope callback")

    with tempfile.TemporaryDirectory(prefix="d972-157ei-") as folder:
        target = Path(folder)/"receipt.json"
        overflow = copy.deepcopy(consistent)
        normal_bytes = len(_canonical_bytes(overflow))
        old_cap = CAPS["packed_receipt_bytes"]
        try:
            CAPS["packed_receipt_bytes"] = normal_bytes
            overflow["caps"] = dict(CAPS)
            adjusted = len(_canonical_bytes(overflow))
            CAPS["packed_receipt_bytes"] = adjusted-1
            overflow["caps"] = dict(CAPS)
            require(len(_canonical_bytes(overflow)) >
                    CAPS["packed_receipt_bytes"],
                    "157ei fixture actual serialization overflow")
            require(write_with_fallback(target, overflow, fixture=True) is True
                    and json.loads(target.read_text(encoding="utf-8"))[
                        "terminal_token"].endswith("UNKNOWN_RESOURCE"),
                    "157ei checked-write overflow fallback")
        finally:
            CAPS["packed_receipt_bytes"] = old_cap
    require(mutation_count == 24,
            "157ei exact EI-specific mutation coverage")
    require(completed_fixture_entries == 2,
            "157ei completed fixture validator baseline entries")
    print("D972_B345_LEXBLOCK_TARGET6_PRODUCER_SELFTEST_PASS "
          f"block_core={trace['block_core']} relator9_independent=1 "
          f"target_reducer={trace['target_reducer']} "
          "consistent_proof=1 inconsistent_dual=1 schemas=4 "
          f"selected_core={trace['selected_core']} "
          f"normal_finalizer={trace['normal_finalizer']} "
          f"ei_mutations={mutation_count} "
          f"completed_fixture_validator={completed_fixture_entries} "
          "partial_presence=3 monitor_callbacks=1 checked_write=1 "
          "inherited_eh=1", flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--q3", type=Path, default=ROOT/Q3_PATH)
    parser.add_argument("--output", type=Path, default=ROOT/OUTPUT)
    parser.add_argument("--seconds", type=float, default=18_000.0)
    args = parser.parse_args(argv)
    if args.self_test:
        self_test(); return 0
    receipt = run(args.q3, seconds=args.seconds)
    write_with_fallback(args.output, receipt)
    print("D972_B345_LEXBLOCK_TARGET6_PRODUCER_PASS "
          f"terminal={receipt['terminal_token']} output={args.output}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
