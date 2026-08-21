#!/usr/bin/env python3
"""Bounded target-6 full-D2 dual column generation (157en/v2).

This is a versioned successor of the frozen 157el producer.  The predecessor
is used only for authenticated constructors and the already cross-checked B0
to B1 bridge.  All general-dual, correlation, batching, incremental normal
form, terminal, and receipt code below is owned by this lane.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib.util
import json
import os
import struct
import sys
import tempfile
import time
import types
from array import array
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

try:
    import resource
except ImportError:  # pragma: no cover - Windows self-test host
    resource = None


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157en_b345_target6_dual_colgen_v2.md")
TASK_SHA = "0c650d358662d3d8e3eaf8fa67eac50ff8d64e35522348cfe634ead02f7c0ee8"
TASK_BYTES = 16_017
SCHEMA = "d972-b345-target6-dual-colgen/v2"
OUTPUT = Path("ci/out/d972_b345_target6_dual_colgen_v2.json")
EI_PRODUCER = Path("search/d972_b345_lexfirst_block_target6_v2.py")
EI_PRODUCER_SHA = "ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a"
EI_PRODUCER_BYTES = 148_824
V1_PRODUCER = Path("search/d972_b345_target6_dual_colgen_v1.py")
V1_PRODUCER_SHA = "8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc"
V1_PRODUCER_BYTES = 410_757
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
Q3_BYTES = 231_570

PIN_SPECS: dict[str, tuple[Path, str, int]] = {
    "task": (TASK, TASK_SHA, TASK_BYTES),
    "157em_task": (Path("sol/luna_task_157em_b345_target6_dual_colgen.md"),
        "60df04261bfd9f30928ed51b26bd501518c05eae43b0bb8ca08507e3b6c4ca99", 43_511),
    "157em_producer": (Path("search/d972_b345_target6_dual_colgen_v1.py"),
        "8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc", 410_757),
    "157em_checker": (Path("search/check_d972_b345_target6_dual_colgen_v1.py"),
        "08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e", 228_980),
    "157em_driver": (Path("search/d972_b345_target6_dual_colgen_gha_driver_v1.g"),
        "e67d6397fca2b7181710fe8baf5893f8273399dc43b6c4ec27caebe4f1a903dc", 14_634),
    "157em_reply": (Path("sol/luna_reply_157em_b345_target6_dual_colgen.md"),
        "70fc6a91a1e10316b5ef2c8ad497e4fc61479866de28b80e0402de92c1065b58", 39_427),
    "157el_producer": (EI_PRODUCER, EI_PRODUCER_SHA, EI_PRODUCER_BYTES),
    "157el_checker": (Path("search/check_d972_b345_lexfirst_block_target6_v4.py"),
        "f15a2beeaf1925c1ea4894ef5fae02de6973c36047a91915b7efd12f6d424533", 21_594),
    "157el_driver": (Path("search/d972_b345_lexfirst_block_target6_gha_driver_v4.g"),
        "fa288727c77dcbdd8061b066d4863babeaf160dbac8ca4f87ba602a6c7a58836", 14_899),
    "157el_task": (Path("sol/luna_task_157el_b345_lexfirst_block_checker_accounting_v4.md"),
        "755861e724fbd66f88b59b9ad9808703f26e2c8016394cb49c0c9cb09ce1f88a", 16_945),
    "157el_reply": (Path("sol/luna_reply_157el_b345_lexfirst_block_checker_accounting_v4.md"),
        "af8b33dccc44881fae7533d633922899774738b7dd1c310afbfaeda967417cb6", 16_035),
    "157eh_producer": (Path("search/d972_b345_full_d2_dual_correlation_v2.py"),
        "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f", 42_449),
    "157eh_checker": (Path("search/check_d972_b345_full_d2_dual_correlation_v2.py"),
        "881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060", 21_933),
    "157eh_driver": (Path("search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g"),
        "5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde", 13_253),
    "157eh_task": (Path("sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md"),
        "5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e", 15_015),
    "157eh_reply": (Path("sol/luna_reply_157eh_b345_full_d2_monitor_scope_repair.md"),
        "0b595d82e7fa84ce4ee59256e03ca813b55f36a5c0f90d012ad141554fc23bfa", 10_817),
    "157ec_producer": (Path("search/d972_b345_seedspan_triple4_v1.py"),
        "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29", 535_219),
    "157ec_checker": (Path("search/check_d972_b345_seedspan_triple4_v1.py"),
        "ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981", 574_347),
    "157ec_driver": (Path("search/d972_b345_seedspan_triple4_gha_driver_v1.g"),
        "a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4", 9_041),
    "157ec_task": (Path("sol/luna_task_157ec_b345_seedspan_triple4.md"),
        "1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2", 14_751),
    "q3_producer": (Path("search/d972_b345_q3_chief_v1.g"),
        "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755", 76_867),
    "q3_checker": (Path("search/check_d972_b345_q3_chief_v1.py"),
        "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73", 89_082),
    "q3_driver": (Path("search/d972_b345_q3_gha_driver_v1.g"),
        "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831", 5_488),
}

CAPS = {
    "column_generation_batches": 12,
    "translations_per_batch": 1024,
    "total_new_translation_blocks": 4096,
    "total_new_relator_columns": 45056,
    "affine_variables": 108,
    "affine_rows": 1_000_000,
    "target_live_remainders": 2_000_000,
    "dual_public_provenance_entries": 128,
    "raw_lambda_support_entries": 2_000_000,
    "raw_lambda_reverse_edge_visits": 8_388_608,
    "raw_coordinate_parent_entries": 2_000_000,
    "raw_coordinate_recovery_nodes": 2_000_000,
    "raw_coordinate_recovery_edges": 4_194_304,
    "inverse_materialized_letters": 4_194_304,
    "correlation_pass1_pairs_per_generation": 8_388_608,
    "correlation_pass2_pairs_per_generation": 8_388_608,
    "correlation_pass1_pairs_total": 75_497_472,
    "correlation_pass2_pairs_total": 67_108_864,
    "distinct_correlation_candidates": 2_000_000,
    "packed_active_rows": 2_000_000,
    "batch_staged_sparse_entries": 262_144,
    "packed_translation_table_bytes": 1_048_576,
    "packed_translation_table_base64_bytes": 1_398_104,
    "packed_block_ledger_decoded_bytes": 16_777_216,
    "packed_block_ledger_base64_bytes": 22_369_624,
    "common_math_soft_deadline_seconds": 18_000,
    "producer_soft_rss_bytes": 4_831_838_208,
    "packed_receipt_bytes": 268_435_456,
}


UPSTREAM_GE_CAPS = frozenset({"element_pool", "section_slp_nodes",
    "directed_section_expr_nodes", "directed_unique_translations",
    "wordexpr_nodes_per_candidate"})


def cap_comparator(key: str, source: str) -> str:
    require(source in {"local", "upstream"}, "157em cap comparator source")
    if source == "local":
        return "ge" if key in {"common_math_soft_deadline_seconds",
                                "producer_soft_rss_bytes"} else "gt"
    return "ge" if key in UPSTREAM_GE_CAPS else "gt"

TERMINALS = {
    "B345_E4_D2_COLGEN_TARGET6_CONSISTENT",
    "B345_E4_D2_COLGEN_TARGET6_FULL_D2_OBSTRUCTION",
    "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_RESOURCE",
    "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT",
}

B1 = {
    "columns": 362736, "pivots": 362720, "dependent": 16,
    "live_sparse_entries": 3090463, "variables": 108,
    "equations": 33687, "rank": 54, "nullity": 54,
    "raw_columns_sha256": "01ee4f1c1d833b82cedc4728b2b642237e503bac72faab8b28133f29e1075d0f",
    "reducer_ledger_sha256": "171e40b114dc23b4a4656e8cdfd904beef766f3349c0decc317dca924bbc166e",
    "anchor_semantic_sha256": "8ef207454deb76ae49daabe3241b4ca5c70e873fdb5be59010fb35e63f04c74a",
    "target_row_space_sha256": "5dd0bd3411afae0a9adafca4254b6fda739774a8b970b59e661d67e686f549be",
    "fresh_remainders_sha256": "9cfd9adc23c9b4dff3d9415f06ce0d0df5fe53b0bf5394aaa8ef667f1b55d407",
    "typed_split_sha256": "96e906aaee06d8748dd5c48c9fb3e9d009a185abdee91d8b66f14d545541f545",
    "direct_bindings_sha256": "32d0b157b4ddbc212ac595543c38f3de5467800cb50bef8361f2c0fbf62ff214",
    "dual_support_sha256": "f8b1cb6325b158f0984ca945dac2c0e915e0386e1f13ddb911acf0e4e2d9dcad",
    "dual_whole_sha256": "005d0ad3f9e9c3aa8182108ab13ceed9108594aedec68d3913c5b752646bcc93",
    "dual_annihilation_sha256": "400f67f74b1250e538c395aa8bf647f6f7432ec07fe2582aaff06e5a47fe7ed5",
}

PREDECESSOR_FAILURE_EVIDENCE = {
    "run_id": 32439034163,
    "head_sha": "2234d5968d3658ab3721aef6f5bf8eab204e9136",
    "job_id": 96645874482,
    "main_start_utc": "2026-08-21T02:13:28Z",
    "main_end_utc": "2026-08-21T04:53:04Z",
    "main_wall_seconds": 9_576,
    "artifact": None,
    "completed_batches": 8,
    "last_completed_phase": "correlation_g9",
    "next_phase_not_printed": "preflight_g9",
    "resource_candidate": {
        "cap_key": "column_generation_batches", "cap_limit": 8,
        "observed_count": 9, "comparator": "gt",
        "phase": "correlation_pass1",
        "detail": "column_generation_batch_limit"},
    "scope": "runtime-and-debugging-evidence-only",
    "valid_receipt": False,
    "independent_checker_ran": False,
    "cross_checked": False,
    "mathematical_terminal_claim": None,
}

PROVENANCE = {
    "predecessor_failed_run": PREDECESSOR_FAILURE_EVIDENCE,
    "evidence_only_not_terminal_certificate": True,
}

BASE_OCCURRENCE_SHA = "3eacd6dc77d62c1799a55923d3c8d5313a37ceab8e78b58b07b45925a28f131d"
WIDTH = 154
RECOVERY_ENCODING = (
    "key=component-u8|result-E4-blob154; direct-tie=00|source-u16be|"
    "source-offset-u32be where source<109 means signed-letter-offset and "
    "source=108+relator means canonical-base-term-ordinal; "
    "translated-tie=01|translation-blob154|"
    "relator-u8|term-u16be|parent-blob154; direct-parent precedes translated"
)

# Only exceptions reachable from the imported functions used by this lane.
# In particular, predecessor whole-search counters such as blocker_table and
# transaction_trace_records are intentionally absent.
OLD_REACHABLE_RESOURCE_CAPS = frozenset({
    "single_word_or_section_length", "provenance_dag_nodes",
    "provenance_dag_edges", "total_sparse_group_ring_keys",
    "single_sparse_elimination_row", "target_elimination_support",
    "sparse_pivot_rows", "element_pool", "section_slp_nodes",
    "directed_section_expr_nodes", "directed_section_expr_edges",
    "directed_unique_translations", "wordexpr_nodes_per_candidate",
    "wordexpr_edges_per_candidate", "wordexpr_flat_leaves_per_candidate",
    "wordexpr_expanded_letter_count_per_target",
    "candidate_live_gradient_entries_total"})
OLD_AFFINE_REACHABLE_RESOURCE_CAPS = frozenset({
    "affine_rows", "target_live_remainders", "dual_provenance_entries"})
ED_REACHABLE_RESOURCE_CAPS = frozenset({"raw_lambda_recursion_edges"})
EG_REACHABLE_RESOURCE_CAPS = frozenset({
    "pair_attempts", "distinct_correlation_candidates",
    "packed_active_rows"})

# Literal, closed values independently mirrored by the checker. Receipt
# validation never imports a predecessor module: pre-authentication INPUT may
# publish {}, while every authenticated or mathematical stage publishes this
# exact table.
EXPECTED_UPSTREAM_CAPS = {
    "affine_rows": 1_000_000,
    "candidate_live_gradient_entries_total": 1_000_000,
    "directed_section_expr_edges": 262_144,
    "directed_section_expr_nodes": 131_072,
    "directed_unique_translations": 32_768,
    "distinct_correlation_candidates": 2_000_000,
    "dual_provenance_entries": 128,
    "element_pool": 2_000_000,
    "packed_active_rows": 2_000_000,
    "pair_attempts": 8_388_608,
    "provenance_dag_edges": 4_000_000,
    "provenance_dag_nodes": 2_000_000,
    "raw_lambda_recursion_edges": 8_388_608,
    "section_slp_nodes": 65_536,
    "single_sparse_elimination_row": 4_194_304,
    "single_word_or_section_length": 100_000,
    "sparse_pivot_rows": 1_000_000,
    "target_elimination_support": 4_194_304,
    "target_live_remainders": 2_000_000,
    "total_sparse_group_ring_keys": 4_194_304,
    "wordexpr_edges_per_candidate": 1_048_576,
    "wordexpr_expanded_letter_count_per_target": 4_194_304,
    "wordexpr_flat_leaves_per_candidate": 16_384,
    "wordexpr_nodes_per_candidate": 262_144,
}


def require(ok: Any, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True,
        separators=(",", ":")).encode("utf-8"))


def semantic_remainders_sha256(rows: Sequence[dict[tuple[int, str], int]]) \
        -> str:
    """Canonical digest of the complete ordered 109 semantic sparse rows."""
    require(isinstance(rows, (list, tuple)) and len(rows) == 109,
            "157en semantic remainder row count")
    canonical: list[list[tuple[tuple[int, str], int]]] = []
    for row in rows:
        require(type(row) is dict, "157en semantic remainder row type")
        entries: list[tuple[tuple[int, str], int]] = []
        for key, coefficient in row.items():
            require(type(key) is tuple and len(key) == 2 and
                    type(key[0]) is int and 1 <= key[0] <= 6 and
                    isinstance(key[1], str) and len(key[1]) == 2*WIDTH and
                    bytes.fromhex(key[1]).hex() == key[1] and
                    type(coefficient) is int and coefficient in (1, 2),
                    "157en semantic remainder coordinate")
            entries.append(((key[0], key[1]), coefficient))
        entries.sort()
        canonical.append(entries)
    return sha_obj(canonical)


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def element_blob(value: Any) -> bytes:
    raw = bytes(value[0]) + bytes(value[1])
    require(len(raw) == WIDTH, "157em canonical E4 blob width")
    return raw


def current_rss() -> int:
    try:
        with open("/proc/self/status", "r", encoding="ascii") as stream:
            for line in stream:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    if resource is None:
        return 0
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024


class InputFailure(RuntimeError):
    pass


class LaneResource(RuntimeError):
    def __init__(self, key: str, limit: int, observed: int, comparator: str,
                 phase: str, current: dict[str, Any] | None = None, *,
                 detail: str | None = None, source: str = "local",
                 inner: str | None = None) -> None:
        super().__init__(key)
        require(comparator in {"gt", "ge"} and source in {"local", "upstream"},
                "157em resource shape")
        if source == "local":
            require(key in CAPS and CAPS[key] == int(limit),
                    "157em local cap binding")
        require(comparator == cap_comparator(key, source),
                "157em resource comparator binding")
        normalized_current = copy.deepcopy(current or {})
        if source == "upstream":
            require(isinstance(inner, str) and key in UPSTREAM_THROW_SITES and
                    (phase, inner, upstream_current_shape(normalized_current))
                        in UPSTREAM_THROW_SITES[key],
                    "157em upstream resource exact throw site")
        self.key = key; self.limit = int(limit); self.observed = int(observed)
        self.comparator = comparator; self.phase = phase
        self.current = normalized_current; self.detail = detail
        self.source = source; self.inner = inner

    def public(self) -> dict[str, Any]:
        return {"cap_reason": self.key, "cap_key": self.key,
            "cap_source": self.source, "cap_limit": self.limit,
            "observed_count": self.observed, "comparator": self.comparator,
            "phase": self.phase, "detail": self.detail,
            "inner_phase": self.inner, "current": self.current}


# Exact callsite pairs.  This is deliberately not a broad collection of
# strings accepted by every adapter: each row below is the complete static
# callback set of the function(s) that receive that particular outer-scoped
# adapter.  The same inherited callback spelling may occur in two rows only
# when two distinct authenticated callsites genuinely invoke it.
MONITOR_REGISTRY: dict[str, frozenset[str]] = {
    "authenticated_input": frozenset({"authenticated_input"}),
    "source_preflight": frozenset({"affine_source_preflight"}),
    "fresh_B0": frozenset({
        "fresh_B0",
        "strong_wform_fresh_BFS", "strong_wform_directed_round",
        "packed_provenance_dag_growth", "packed_pivot_column_elimination",
        "packed_target_sparse_elimination", "proof_DAG_array_bytes",
        "proof_DAG_base64", "proof_DAG_base64_complete"}),
    "fixed_B1": frozenset({
        "fixed_B1",
        "raw_lambda_reverse_dp", "dual_correlation", "block_insertion",
        "affine_full_remainder", "packed_provenance_dag_growth",
        "packed_pivot_column_elimination", "proof_DAG_array_bytes",
        "proof_DAG_base64", "proof_DAG_base64_complete"}),
    "initial_target": frozenset({
        "initial_target",
        "target_reduction", "affine_full_remainder", "affine_remainder",
        "affine_transposed_row_absorption"}),
    "dual_lift": frozenset({"raw_lambda_reverse_dp"}),
    "correlation_pass1": frozenset({"correlation_pass1"}),
    "correlation_pass2": frozenset({"correlation_pass2"}),
    "batch_precompute": frozenset({"batch_precompute"}),
    "section_recovery": frozenset({
        "section_recovery", "proof_DAG_array_bytes", "proof_DAG_base64",
        "proof_DAG_base64_complete"}),
    "block_commit": frozenset({
        "block_commit", "packed_provenance_dag_growth",
        "packed_pivot_column_elimination"}),
    "incremental_reduction": frozenset({
        "incremental_reduction", "affine_full_remainder",
        "affine_remainder"}),
    "target_resolve": frozenset({"affine_transposed_row_absorption"}),
    "selected_proof": frozenset({
        "packed_target_sparse_elimination", "packed_provenance_dag_growth",
        "proof_DAG_pre_serialization_RSS", "proof_DAG_reachability",
        "proof_DAG_compact_serialization", "proof_DAG_array_bytes",
        "proof_DAG_base64", "proof_DAG_base64_complete"}),
    "receipt_serialization": frozenset({"receipt_serialization"}),
    "complete": frozenset(),
}
MONITOR_PUBLIC = {key: sorted(value) for key, value in MONITOR_REGISTRY.items()}
MONITOR_SHA = sha_obj(MONITOR_PUBLIC)
OUTER_ALIAS = {"block_insertion": "fixed_B1",
               "target_reduction": "initial_target"}


def _build_upstream_throw_sites() \
        -> dict[str, frozenset[tuple[str, str, str]]]:
    """Freeze imported ResourceStop callsites, including public progress shape.

    This registry is intentionally separate from ``MONITOR_REGISTRY``.
    Structural imported exceptions usually have no helper phase and therefore
    use their cap key as the exact inner spelling.  Frozen 157ed/157eg/157ei
    wrappers retain the three explicit inner spellings listed below.  Merely
    preserving a cap key while moving it to another outer phase is forbidden.
    """
    keys = (OLD_REACHABLE_RESOURCE_CAPS |
            OLD_AFFINE_REACHABLE_RESOURCE_CAPS |
            ED_REACHABLE_RESOURCE_CAPS | EG_REACHABLE_RESOURCE_CAPS)
    rows: dict[str, set[tuple[str, str, str]]] = {key: set() for key in keys}

    def add(selected: Iterable[str], outer: str, shape: str, *,
            inner: str | None = None) -> None:
        for key in selected:
            require(key in rows, "157em upstream throw-site cap")
            rows[key].add((outer, key if inner is None else inner, shape))

    # Frozen strong-prefix construction: pool/section/DAG/basis construction,
    # target probes, and directed registration.  WordExpr and affine-system
    # constructors are not called by this prefix path.
    fresh = {
        "provenance_dag_nodes",
        "provenance_dag_edges", "total_sparse_group_ring_keys",
        "single_sparse_elimination_row", "target_elimination_support",
        "sparse_pivot_rows", "element_pool", "section_slp_nodes",
        "directed_section_expr_nodes", "directed_section_expr_edges"}
    add(fresh, "fresh_B0", "empty")

    # Fixed B1 first builds the old raw oracle/correlation/witness without a
    # persistent block-progress object, then enters the frozen 11-column
    # helper, whose exact progress ledger is attached to every structural stop.
    add({"raw_lambda_recursion_edges"}, "fixed_B1", "empty",
        inner="raw_lambda_reverse_dp")
    add({"pair_attempts", "distinct_correlation_candidates"},
        "fixed_B1", "fixed_correlation_pair", inner="dual_correlation")
    add({"packed_active_rows"}, "fixed_B1", "fixed_correlation_post",
        inner="dual_correlation")
    add({"single_word_or_section_length", "directed_section_expr_nodes",
         "directed_section_expr_edges"}, "fixed_B1", "empty")
    fixed_block = {
        "single_word_or_section_length", "provenance_dag_nodes",
        "provenance_dag_edges", "total_sparse_group_ring_keys",
        "single_sparse_elimination_row", "target_elimination_support",
        "sparse_pivot_rows", "element_pool", "directed_unique_translations"}
    add(fixed_block, "fixed_B1", "fixed_block")

    # The frozen 109-row B1 target wrapper attaches its exact target progress
    # to old structural/WordExpr/affine stops.  Its per-seed live-remainder
    # guard is the sole reachable imported stop whose inner spelling is the
    # frozen wrapper phase rather than the cap key.
    initial = {
        "single_word_or_section_length", "target_elimination_support",
        "element_pool", "wordexpr_nodes_per_candidate",
        "wordexpr_edges_per_candidate", "wordexpr_flat_leaves_per_candidate",
        "wordexpr_expanded_letter_count_per_target",
        "candidate_live_gradient_entries_total", "affine_rows",
        "dual_provenance_entries"}
    add(initial, "initial_target", "initial_target")
    add({"target_live_remainders"},
        "initial_target", "initial_target", inner="target_reduction")

    # Adaptive section preflight owns a transient expression DAG.  A length
    # stop is raised by this lane with the exact node ledger; constructor caps
    # occur before a materialization node is selected.
    add({"directed_section_expr_nodes", "directed_section_expr_edges"},
        "section_recovery", "empty")
    add({"single_word_or_section_length"}, "section_recovery", "section_node")

    # Every persistent adaptive translation is transaction-wrapped; imported
    # structural stops carry the exact rolled-back block progress ledger.
    adaptive_block = {
        "provenance_dag_nodes", "provenance_dag_edges",
        "total_sparse_group_ring_keys", "single_sparse_elimination_row",
        "sparse_pivot_rows", "element_pool",
        "directed_section_expr_nodes", "directed_section_expr_edges",
        "directed_unique_translations"}
    add(adaptive_block, "block_commit", "block")

    # Only the four fresh cadence probes in the incremental path can enter an
    # imported pool/remainder helper.  The local quotient update has its own
    # caps and does not appear here.
    add({"element_pool", "target_elimination_support"},
        "incremental_reduction", "incremental")

    # The fresh post-batch solve enters the old transposed affine helper
    # directly, so each reachable inner spelling is its cap key.
    add({"affine_rows", "target_live_remainders",
         "dual_provenance_entries"},
        "target_resolve", "empty")

    # A consistent terminal regenerates the typed target and a fresh D2 proof.
    selected = {
        "single_word_or_section_length", "provenance_dag_nodes",
        "provenance_dag_edges", "target_elimination_support", "element_pool",
        "wordexpr_nodes_per_candidate", "wordexpr_edges_per_candidate",
        "wordexpr_flat_leaves_per_candidate",
        "candidate_live_gradient_entries_total"}
    add(selected, "selected_proof", "selected")

    require(set(rows) == set(keys) and all(rows.values()),
            "157em complete upstream throw-site registry")
    return {key: frozenset(value) for key, value in sorted(rows.items())}


UPSTREAM_THROW_SITES = _build_upstream_throw_sites()
UPSTREAM_THROW_SITES_PUBLIC = {
    key: [{"outer": outer, "inner": inner, "current_shape": shape}
          for outer, inner, shape in sorted(value)]
    for key, value in UPSTREAM_THROW_SITES.items()}
UPSTREAM_THROW_SITES_SHA = sha_obj(UPSTREAM_THROW_SITES_PUBLIC)


class Monitor:
    def __init__(self, seconds: float = 18_000.0) -> None:
        require(0 < seconds <= CAPS["common_math_soft_deadline_seconds"],
                "157em deadline")
        self.started = time.monotonic(); self.deadline = self.started + seconds
        self.initial_seconds = float(seconds); self.checks = 0
        self.peak_rss_bytes = 0; self.hit_reason: str | None = None
        self.callbacks: dict[tuple[str, str, str], int] = defaultdict(int)

    def bind(self, outer: str) -> "BoundMonitor":
        return BoundMonitor(self, OUTER_ALIAS.get(outer, outer))

    def event(self, outer: str, inner: str, api: str, force: bool,
              reserve: int = 0) -> None:
        require(outer in MONITOR_REGISTRY and inner in MONITOR_REGISTRY[outer]
                and api in {"check", "reserve"},
                f"157em unknown monitor pair {outer}/{inner}/{api}")
        self.callbacks[(outer, inner, api)] += 1; self.checks += 1
        if not force and reserve == 0 and self.checks & 63:
            return
        rss = current_rss(); self.peak_rss_bytes = max(self.peak_rss_bytes, rss)
        observed = rss + reserve
        if observed >= CAPS["producer_soft_rss_bytes"]:
            self.hit_reason = "producer_soft_rss_bytes"
            raise LaneResource(self.hit_reason, CAPS[self.hit_reason], observed,
                "ge", outer, inner=inner)
        if time.monotonic() >= self.deadline:
            self.hit_reason = "common_math_soft_deadline_seconds"
            elapsed = max(CAPS[self.hit_reason], int(time.monotonic()-self.started))
            raise LaneResource(self.hit_reason, CAPS[self.hit_reason], elapsed,
                "ge", outer, inner=inner)

    def public(self) -> dict[str, Any]:
        return {"initial_remaining_seconds": self.initial_seconds,
            "elapsed_seconds": time.monotonic()-self.started,
            "remaining_seconds": max(0.0, self.deadline-time.monotonic()),
            "checks": self.checks, "peak_rss_bytes": self.peak_rss_bytes,
            "hit_reason": self.hit_reason,
            "callback_count": sum(self.callbacks.values())}


class BoundMonitor:
    __slots__ = ("base", "outer")

    def __init__(self, base: Monitor, outer: str) -> None:
        require(outer in MONITOR_REGISTRY, "157em monitor outer")
        self.base = base; self.outer = outer

    @property
    def started(self) -> float:
        return self.base.started

    @property
    def deadline(self) -> float:
        return self.base.deadline

    def check(self, inner: str, force: bool = False, **_: Any) -> None:
        self.base.event(self.outer, inner, "check", force)

    def reserve(self, inner: str, additional_bytes: int) -> None:
        require(type(additional_bytes) is int and additional_bytes >= 0,
                "157em reserve")
        self.base.event(self.outer, inner, "reserve", True, additional_bytes)


_EI: Any | None = None
_V1_FIXTURE: Any | None = None


def authenticate_static() -> None:
    for label, (path, digest, size) in PIN_SPECS.items():
        full = ROOT/path
        if not full.is_file() or full.stat().st_size != size or sha_file(full) != digest:
            raise InputFailure(f"authenticated pin drift: {label}")


def load_ei() -> Any:
    global _EI
    authenticate_static()
    if _EI is not None:
        return _EI
    spec = importlib.util.spec_from_file_location(
        "_d972_157em_pinned_157el_producer", ROOT/EI_PRODUCER)
    require(spec is not None and spec.loader is not None, "157em predecessor spec")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None); raise
    require(module.SCHEMA == "d972-b345-lexfirst-block-target6/v2" and
            callable(module._commit_block) and callable(module._target6_system),
            "157em predecessor API")
    _EI = module
    return module


def load_v1_fixture() -> Any:
    """Load the frozen 157em source only for inherited bounded self-tests."""
    global _V1_FIXTURE
    authenticate_static()
    if _V1_FIXTURE is not None:
        return _V1_FIXTURE
    name = "_d972_157en_pinned_157em_producer"
    spec = importlib.util.spec_from_file_location(name, ROOT/V1_PRODUCER)
    require(spec is not None and spec.loader is not None,
            "157en v1 producer fixture spec")
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None); raise
    require(Path(module.__file__).resolve() == (ROOT/V1_PRODUCER).resolve() and
            Path(module.__file__).stat().st_size == V1_PRODUCER_BYTES and
            sha_file(Path(module.__file__)) == V1_PRODUCER_SHA and
            module.SCHEMA == "d972-b345-target6-dual-colgen/v1" and
            callable(module.self_test),
            "157en v1 producer fixture binding")
    _V1_FIXTURE = module
    return module


SELFTEST_OLD_MODULE = "_d972_157en_selftest_old_producer"
SELFTEST_OLD_REQUIRED_API = (
    "ElementRegistry", "ProvenanceDAG", "SectionExpressionDAG",
    "WordExprDAG", "_affine_make_typed_positive",
    "_affine_typed_candidate_public", "inv_word", "reduce_word",
    "serialize_proof_dag")


def loaded_old_fixture_module(ed: Any) -> Any:
    """Load once or reuse the exact 157ec producer under a v2-only name."""
    name = SELFTEST_OLD_MODULE
    pinned_path, pinned_sha, pinned_bytes = PIN_SPECS["157ec_producer"]
    expected = (ROOT/pinned_path).resolve()
    require((ROOT/ed.OLD_PRODUCER).resolve() == expected and
            ed.OLD_PRODUCER_SHA == pinned_sha,
            "157en old fixture predecessor pin binding")
    module = sys.modules.get(name)
    if module is None:
        module = ed.load_pinned_module(ed.OLD_PRODUCER,
            ed.OLD_PRODUCER_SHA, name)
    module_file = getattr(module, "__file__", None)
    module_spec = getattr(module, "__spec__", None)
    require(isinstance(module, types.ModuleType) and
            sys.modules.get(name) is module and
            getattr(module, "__name__", None) == name and
            getattr(module_spec, "name", None) == name and
            type(module_file) is str and
            Path(module_file).resolve() == expected and
            expected.is_file() and expected.stat().st_size == pinned_bytes and
            sha_file(expected) == pinned_sha and
            getattr(module, "SCHEMA", None) ==
                "d972-b345-relative-frattini3-wordexpr-memo/v9" and
            type(getattr(module, "CAPS", None)) is dict and
            type(getattr(module, "FIXED_WORD", None)) in (list, tuple) and
            all(callable(getattr(module, api, None))
                for api in SELFTEST_OLD_REQUIRED_API),
            "157en exact old fixture module lifecycle/API")
    return module


def pin_rows(q3_path: Path) -> dict[str, Any]:
    rows = {label: {"path": path.as_posix(), "sha256": digest, "bytes": size}
            for label, (path, digest, size) in sorted(PIN_SPECS.items())}
    rows["q3_artifact"] = {"path": Q3_PATH.as_posix(),
        "sha256": Q3_SHA,
        "bytes": Q3_BYTES}
    rows["157el_crosschecked_run"] = {"run": "32401947156",
        "head": "2808c3fb61962d7180a192947fed375c754a25ce",
        "receipt_sha256":
            "746ca938a962f4d918c07ee270d4e03c3e4f75e40689f3a0507c8daff9d57053",
        "receipt_bytes": 1_314_365, "evidence_only_not_imported": True}
    return rows


def theorem_boundary() -> dict[str, Any]:
    return {"pinned_E4_roof_only": True, "target6_only": True,
        "registered_108_family_only": True, "targets_7_through_33_checked": False,
        "full_D2_claim_only_after_zero_complete_correlation": True,
        "typed_lift_claimed": False, "full_H3_claimed": False,
        "B4_A_claimed": False, "B4_B_claimed": False,
        "global_nonexistence_claimed": False,
        "unknown_resource_is_not_obstruction": True}


def claim_row(token: str) -> dict[str, Any]:
    return {"claim": ("target6_registered_108_membership_mod_current_D2"
            if token.endswith("CONSISTENT") else
            "target6_registered_108_no_solution_mod_full_D2"
            if token.endswith("FULL_D2_OBSTRUCTION") else "none"),
        **theorem_boundary()}


class RecoveryMap:
    """One canonical parent per semantic coordinate; candidate edges are not retained."""

    DIRECT = 0
    TRANSLATED = 1

    def __init__(self, monitor: Monitor) -> None:
        self.monitor = monitor
        self.ids: dict[bytes, int] = {}
        self.kind = array("B"); self.component = array("B")
        self.source = array("H"); self.offset = array("I")
        self.relator = array("B"); self.term = array("H")
        self.result = bytearray(); self.translation = bytearray(); self.parent = bytearray()
        self.candidates = 0; self.replacements = 0
        self.direct_candidates = 0; self.translated_candidates = 0
        self.direct_semantic_keys: set[bytes] = set()

    @staticmethod
    def key(component: int, blob: bytes) -> bytes:
        require(1 <= component <= 6 and len(blob) == WIDTH,
                "157em recovery semantic key")
        return bytes([component]) + blob

    @staticmethod
    def direct_tie(source: int, offset: int) -> bytes:
        require(0 <= source <= 65535 and 1 <= offset <= 0xffffffff,
                "157em direct parent range")
        return b"\x00" + struct.pack(">HI", source, offset)

    @staticmethod
    def translated_tie(translation: bytes, relator: int, term: int,
                       parent: bytes) -> bytes:
        require(len(translation) == len(parent) == WIDTH and
                1 <= relator <= 11 and 1 <= term <= 65535,
                "157em translated parent range")
        return b"\x01" + translation + bytes([relator]) + \
            struct.pack(">H", term) + parent

    def _tie(self, index: int) -> bytes:
        if self.kind[index] == self.DIRECT:
            return self.direct_tie(self.source[index], self.offset[index])
        start = index * WIDTH
        return self.translated_tie(bytes(self.translation[start:start+WIDTH]),
            self.relator[index], self.term[index],
            bytes(self.parent[start:start+WIDTH]))

    def _append(self, component: int, blob: bytes, kind: int, source: int,
                offset: int, relator: int, term: int, translation: bytes,
                parent: bytes, phase: str) -> int:
        attempted = len(self.kind) + 1
        if attempted > CAPS["raw_coordinate_recovery_nodes"]:
            raise LaneResource("raw_coordinate_recovery_nodes",
                CAPS["raw_coordinate_recovery_nodes"], attempted, "gt",
                phase, {"candidate_edges": self.candidates})
        index = len(self.kind); self.kind.append(kind); self.component.append(component)
        self.source.append(source); self.offset.append(offset)
        self.relator.append(relator); self.term.append(term)
        self.result.extend(blob); self.translation.extend(translation)
        self.parent.extend(parent); self.ids[self.key(component, blob)] = index
        return index

    def _replace(self, index: int, kind: int, source: int, offset: int,
                 relator: int, term: int, translation: bytes,
                 parent: bytes) -> None:
        self.kind[index] = kind; self.source[index] = source
        self.offset[index] = offset; self.relator[index] = relator
        self.term[index] = term; start = index * WIDTH
        self.translation[start:start+WIDTH] = translation
        self.parent[start:start+WIDTH] = parent; self.replacements += 1

    def consider_direct(self, component: int, blob: bytes,
                        source: int, offset: int) -> int:
        key = self.key(component, blob)
        attempted = len(self.direct_semantic_keys) + (key not in
                                                       self.direct_semantic_keys)
        if attempted > CAPS["raw_coordinate_parent_entries"]:
            raise LaneResource("raw_coordinate_parent_entries",
                CAPS["raw_coordinate_parent_entries"], attempted, "gt",
                "initial_target", {"completed_parent_entries":
                    len(self.direct_semantic_keys)})
        next_candidates = self.candidates + 1
        if next_candidates & 4095 == 0:
            self.monitor.bind("initial_target").check("initial_target")
        self.candidates = next_candidates; self.direct_candidates += 1
        self.direct_semantic_keys.add(key)
        tie = self.direct_tie(source, offset)
        index = self.ids.get(key)
        if index is None:
            return self._append(component, blob, self.DIRECT, source, offset,
                0, 0, bytes(WIDTH), bytes(WIDTH), "initial_target")
        if tie < self._tie(index):
            self._replace(index, self.DIRECT, source, offset, 0, 0,
                          bytes(WIDTH), bytes(WIDTH))
        return index

    def consider_translated(self, component: int, blob: bytes,
                            translation: bytes, relator: int, term: int,
                            parent: bytes, *, phase: str) -> int:
        row = (component, blob, translation, relator, term, parent)
        self.preflight_translated([row], phase=phase)
        return self.apply_translated_prechecked(*row)

    def preflight_translated(self,
            rows: Sequence[tuple[int, bytes, bytes, int, int, bytes]], *,
            phase: str) -> None:
        """Reserve a whole column's recovery suffix before reducer mutation."""
        attempted_edges = self.translated_candidates + len(rows)
        if attempted_edges > CAPS["raw_coordinate_recovery_edges"]:
            raise LaneResource("raw_coordinate_recovery_edges",
                CAPS["raw_coordinate_recovery_edges"], attempted_edges, "gt",
                phase, {"completed_candidate_edges": self.candidates})
        new_keys = {self.key(component, blob)
                    for component, blob, _, _, _, _ in rows
                    if self.key(component, blob) not in self.ids}
        attempted_nodes = len(self.kind) + len(new_keys)
        if attempted_nodes > CAPS["raw_coordinate_recovery_nodes"]:
            raise LaneResource("raw_coordinate_recovery_nodes",
                CAPS["raw_coordinate_recovery_nodes"], attempted_nodes, "gt",
                phase, {"completed_candidate_edges": self.candidates})
        before, after = self.candidates, self.candidates+len(rows)
        if before//4096 != after//4096:
            self.monitor.bind(phase).check(phase)

    def apply_translated_prechecked(self, component: int, blob: bytes,
                                    translation: bytes, relator: int,
                                    term: int, parent: bytes) -> int:
        """Apply only data that passed ``preflight_translated``."""
        self.candidates += 1; self.translated_candidates += 1
        key = self.key(component, blob)
        tie = self.translated_tie(translation, relator, term, parent)
        index = self.ids.get(key)
        if index is None:
            # The batch reservation proves this append cannot cross the cap.
            require(len(self.kind) < CAPS["raw_coordinate_recovery_nodes"],
                    "157em prechecked recovery node reservation")
            return self._append(component, blob, self.TRANSLATED, 0, 0,
                relator, term, translation, parent, "complete")
        if tie < self._tie(index):
            self._replace(index, self.TRANSLATED, 0, 0, relator, term,
                          translation, parent)
        return index

    def contains(self, component: int, blob: bytes) -> bool:
        return self.key(component, blob) in self.ids

    def descriptor(self, component: int, blob: bytes) -> dict[str, Any]:
        index = self.ids.get(self.key(component, blob))
        require(index is not None, "157em missing authenticated recovery parent")
        if self.kind[index] == self.DIRECT:
            source = int(self.source[index]); offset = int(self.offset[index])
            common = {"root": index, "component": component,
                      "element_hex": blob.hex()}
            if source < 109:
                return {**common, "kind": "direct_target_source_prefix",
                    "source_word_ordinal": source,
                    "signed_letter_offset": offset}
            require(109 <= source <= 119,
                    "157em direct base source encoding")
            return {**common, "kind": "direct_base_support_prefix",
                "relator_index": source - 108,
                "term_ordinal": offset}
        start = index * WIDTH
        return {"kind": "registered_translation_times_base_prefix",
            "root": index, "component": component, "element_hex": blob.hex(),
            "translation_hex": bytes(self.translation[start:start+WIDTH]).hex(),
            "relator_index": self.relator[index], "term_ordinal": self.term[index],
            "parent_hex": bytes(self.parent[start:start+WIDTH]).hex()}

    def checkpoint(self, rows: Sequence[tuple[int, bytes, bytes,
                                              int, int, bytes]]) \
            -> dict[str, Any]:
        """Small rollback record for one precomputed translation block."""
        saved: dict[int, tuple[int, int, int, int, int, bytes, bytes]] = {}
        base_length = len(self.kind)
        for component, blob, translation, relator, term, parent in rows:
            index = self.ids.get(self.key(component, blob))
            if index is None or index >= base_length or index in saved:
                continue
            tie = self.translated_tie(translation, relator, term, parent)
            if tie < self._tie(index):
                start = index*WIDTH
                saved[index] = (int(self.kind[index]), int(self.source[index]),
                    int(self.offset[index]), int(self.relator[index]),
                    int(self.term[index]),
                    bytes(self.translation[start:start+WIDTH]),
                    bytes(self.parent[start:start+WIDTH]))
        return {"length": base_length, "candidates": self.candidates,
            "translated_candidates": self.translated_candidates,
            "replacements": self.replacements, "saved": saved}

    def rollback(self, checkpoint: dict[str, Any]) -> None:
        length = int(checkpoint["length"])
        require(0 <= length <= len(self.kind),
                "157em recovery rollback length")
        for index in range(len(self.kind)-1, length-1, -1):
            start = index*WIDTH
            key = self.key(int(self.component[index]),
                           bytes(self.result[start:start+WIDTH]))
            require(self.ids.get(key) == index,
                    "157em recovery rollback suffix binding")
            del self.ids[key]
        del self.kind[length:]; del self.component[length:]
        del self.source[length:]; del self.offset[length:]
        del self.relator[length:]; del self.term[length:]
        del self.result[length*WIDTH:]; del self.translation[length*WIDTH:]
        del self.parent[length*WIDTH:]
        for index, row in checkpoint["saved"].items():
            kind, source, offset, relator, term, translation, parent = row
            self.kind[index] = kind; self.source[index] = source
            self.offset[index] = offset; self.relator[index] = relator
            self.term[index] = term; start = index*WIDTH
            self.translation[start:start+WIDTH] = translation
            self.parent[start:start+WIDTH] = parent
        self.candidates = int(checkpoint["candidates"])
        self.translated_candidates = int(checkpoint["translated_candidates"])
        self.replacements = int(checkpoint["replacements"])
        require(len(self.ids) == len(self.kind),
                "157em recovery rollback integrity")

    def public(self) -> dict[str, Any]:
        digest = hashlib.sha256()
        kind_counts = [0, 0]
        for key in sorted(self.ids):
            index = self.ids[key]; kind_counts[self.kind[index]] += 1
            tie = self._tie(index)
            digest.update(key); digest.update(struct.pack(">H", len(tie)))
            digest.update(tie)
        return {"encoding": RECOVERY_ENCODING, "semantic_entry_count": len(self.ids),
            "direct_parent_count": kind_counts[0],
            "raw_coordinate_parent_entry_count": len(self.direct_semantic_keys),
            "translated_parent_count": kind_counts[1],
            "candidate_edge_count": self.candidates,
            "translated_candidate_edge_count": self.translated_candidates,
            "canonical_replacement_count": self.replacements,
            "canonical_sha256": digest.hexdigest(),
            "typed_arrays": {"kind": "u8", "component": "u8",
                "source": "u16-native-private", "offset": "u32-native-private",
                "relator": "u8", "term": "u16-native-private",
                "blob_width": WIDTH},
            "one_selected_parent_per_semantic_key": True,
            "all_candidate_dicts_or_roots_retained": False,
            "pool_IDs_public": False}


def base_occurrences_exact(old: Any, e4: Any, sections: Any,
                           pool: Any) -> list[dict[str, Any]]:
    before = dict(sections.base_prefix_roots); rows: list[dict[str, Any]] = []
    model = old.fox_model(4, e4); global_ordinal = 0
    for relator, (gradient, support_sections) in enumerate(
            zip(model["columns"], model["sections"]), 1):
        ordered = sorted(gradient.items(),
            key=lambda item: (item[0][0], pool.pack(item[0][1])))
        for term_ordinal, ((component, value), coefficient) in \
                enumerate(ordered, 1):
            global_ordinal += 1; blob = pool.pack(value)
            root = sections.base_prefix_roots.get((component, blob))
            require(root is not None and value in support_sections and
                    sections.expressions.value_blob(root) == blob,
                    "157em base occurrence root")
            rows.append({"relator_index": relator,
                "occurrence_ordinal": global_ordinal,
                "term_ordinal": term_ordinal, "component": component,
                "coefficient": int(coefficient), "element_hex": blob.hex(),
                "section_word": list(support_sections[value]),
                "section_expression_root": root, "_value": value})
    require(len(rows) == 76 and sections.base_prefix_roots == before,
            "157em exact 76 base occurrence roots/state neutrality")
    return rows


def record_complete_block_relator(masks: dict[bytes, int], blob: bytes,
                                  relator: int) -> None:
    require(len(blob) == WIDTH and 1 <= relator <= 11,
            "157em complete-block semantic row")
    prior = masks.get(blob, 0); bit = 1 << (relator-1)
    require(prior & bit == 0,
            "157em duplicate relator in complete-block registry")
    masks[blob] = prior | bit


def complete_block_registry_public(masks: dict[bytes, int],
                                   expected_count: int) -> dict[str, Any]:
    full_mask = (1 << 11)-1
    require(len(masks) == expected_count and
            all(mask == full_mask for mask in masks.values()),
            "157em exact complete 11-relator block registry")
    ordered = sorted(masks)
    return {"translation_count": len(ordered),
        "relators_per_translation": 11, "all_masks_equal_0x7ff": True,
        "canonical_translation_sha256": sha_bytes(b"".join(ordered)),
        "semantic_blob_order": "exact E4 blob lexicographic",
        "pool_IDs_public": False}


def require_active_not_completed(active_rows: Sequence[tuple[bytes, int, int]],
                                 completed: set[bytes]) -> None:
    require(not {row[0] for row in active_rows}.intersection(completed),
            "157em correlation cannot reactivate complete D2 block")


def instrument_basis_class(old: Any, recovery: RecoveryMap,
                           phase: str,
                           complete_block_masks: dict[bytes, int]) -> type:
    parent = old.SparseBoundaryBasis

    class Instrumented(parent):  # type: ignore[misc,valid-type]
        def add_column(self, relator_index: int, translation_id: int,
                       section_node: int, translation_ordinal: int = 0) -> None:
            u_blob = self.pool.blob(translation_id)
            base_rows = getattr(self, "_em_base_rows", None)
            if base_rows is None:
                rows = base_occurrences_exact(
                    old, self.pool.quotient, self.sections, self.pool)
                base_rows = {j: [row for row in rows
                                 if row["relator_index"] == j]
                             for j in range(1, 12)}
                setattr(self, "_em_base_rows", base_rows)
            pending = []
            for row in base_rows[relator_index]:
                g = self.pool.quotient.mul(self.pool.value(translation_id),
                                           row["_value"])
                g_blob = self.pool.pack(g)
                pending.append((int(row["component"]), g_blob, u_blob,
                    relator_index, int(row["term_ordinal"]),
                    bytes.fromhex(row["element_hex"])))
            current_phase = getattr(self, "_em_recovery_phase", phase)
            recovery.preflight_translated(pending, phase=current_phase)
            result = super().add_column(relator_index, translation_id,
                section_node, translation_ordinal=translation_ordinal)
            for edge in pending:
                recovery.apply_translated_prechecked(*edge)
            record_complete_block_relator(
                complete_block_masks, u_blob, relator_index)
            return result

    return Instrumented


def build_prefix_with_recovery(old: Any, ed: Any, e4: Any,
                               raw_source_key: Sequence[Any], monitor: Monitor,
                               recovery: RecoveryMap) -> tuple[dict[str, Any], list[Any]]:
    original = old.SparseBoundaryBasis
    complete_block_masks: dict[bytes, int] = {}
    old.SparseBoundaryBasis = instrument_basis_class(
        old, recovery, "fresh_B0", complete_block_masks)
    adapter = monitor.bind("fresh_B0")
    try:
        prefix, dependent = ed.build_instrumented_prefix(
            old, e4, adapter, raw_source_key)
    finally:
        old.SparseBoundaryBasis = original
    require(prefix["basis"].deadline is adapter and prefix["dag"].deadline is adapter,
            "157em fresh adapter retained")
    prefix["basis"].deadline = None; prefix["dag"].deadline = None
    ordered = sorted(complete_block_masks)
    # The instrumented basis method closes over this exact semantic mask map.
    # Keep it private so an unfinished adaptive translation can restore the
    # one entry that add_column may have advanced before a resource stop.
    prefix["_em_complete_block_masks"] = complete_block_masks
    prefix["_em_complete_blocks"] = set(ordered)
    prefix["_em_complete_block_public"] = complete_block_registry_public(
        complete_block_masks, 32975)
    return prefix, dependent


def target6_words(old: Any, seeds: Sequence[Sequence[int]]) -> list[list[int]]:
    mapping = old.cofaces(3)[0]
    lift = lambda word: old.word_substitute(old.embed_f2_pb3(word), mapping)
    r0 = lift(old.hexagon_words(old.FIXED_WORD)[0])
    words = [r0]
    for seed in seeds:
        rs = lift(old.hexagon_words(old.reduce_word(old.FIXED_WORD+list(seed)))[0])
        words.append(old.reduce_word(rs + old.inv_word(r0)))
    require(len(words) == 109, "157em target word manifest")
    return words


def add_direct_parents(old: Any, e4: Any, pool: Any, recovery: RecoveryMap,
                       words: Sequence[Sequence[int]],
                       gradients: Sequence[dict[Any, int]]) -> dict[str, Any]:
    require(len(words) == len(gradients) == 109,
            "157em raw parent manifest dimensions")
    rows = []
    for source, (word, gradient) in enumerate(zip(words, gradients)):
        prefix = e4.identity; seen: set[tuple[int, bytes]] = set()
        for offset, letter in enumerate(word, 1):
            component = abs(letter)
            if letter > 0:
                value = prefix
                prefix = e4.mul(prefix, e4.generators[component-1])
            else:
                prefix = e4.mul(prefix, e4.inverse_generators[component-1])
                value = prefix
            blob = pool.pack(value); key = (component, blob)
            if (component, value) in gradient:
                recovery.consider_direct(component, blob, source, offset)
                seen.add(key)
        expected = {(component, pool.pack(value)) for component, value in gradient}
        require(seen == expected, "157em each nonzero raw term has Fox parent")
        rows.append({"source_word_ordinal": source, "word_length": len(word),
            "word_sha256": sha_obj(word), "gradient_entry_count": len(gradient),
            "gradient_sha256": sha_obj([[c, pool.pack(v).hex(), a]
                for (c, v), a in sorted(gradient.items(),
                    key=lambda item: (item[0][0], pool.pack(item[0][1])))]),
            "all_nonzero_terms_parented": True})
    return {"source_count": 109, "rows": rows, "rows_sha256": sha_obj(rows),
        "source_word_order": "base target6 then registered seeds 1..108",
        "signed_offset_convention":
            "positive uses prefix before letter; negative uses prefix after inverse"}


def semantic_key(old: Any, pool: Any, packed_key: int) -> tuple[int, bytes]:
    component, identifier = old.unpack_vector_key(packed_key)
    return component, pool.blob(identifier)


def semantic_row(old: Any, pool: Any, packed: dict[int, int]) \
        -> dict[tuple[int, bytes], int]:
    return {semantic_key(old, pool, key): int(value) % 3
            for key, value in packed.items() if int(value) % 3}


def semantic_public(row: dict[tuple[int, bytes], int]) -> list[list[Any]]:
    return [[component, blob.hex(), coefficient]
            for (component, blob), coefficient in sorted(row.items())]


def semantic_bytes(row: dict[tuple[int, bytes], int]) -> bytes:
    out = bytearray()
    for (component, blob), coefficient in sorted(row.items()):
        require(1 <= component <= 6 and len(blob) == WIDTH and
                coefficient in (1, 2), "157em semantic sparse row")
        out.extend(bytes([component])); out.extend(blob); out.extend(bytes([coefficient]))
    return bytes(out)


def dot_semantic(functional: dict[tuple[int, bytes], int],
                 row: dict[tuple[int, bytes], int]) -> int:
    return sum(coefficient * functional.get(key, 0)
               for key, coefficient in row.items()) % 3


class RawLambda:
    """General reverse-pivot lift of an affine inconsistency dual."""

    def __init__(self, old: Any, prefix: dict[str, Any], system: Any,
                 remainders: Sequence[dict[tuple[int, str], int]],
                 dependent_raw: Sequence[dict[tuple[int, bytes], int]],
                 prior_block_raw: Sequence[dict[tuple[int, bytes], int]],
                 monitor: Monitor) -> None:
        pool, basis = prefix["pool"], prefix["basis"]
        dual = system.dual_public()
        require(not system.consistent and isinstance(dual, dict) and
                dual["normalized_rhs"] == 1 and dual["yTz_mod3"] == 2,
                "157em normalized affine dual")
        require(dual["support_count"] <= 109 <
                CAPS["dual_public_provenance_entries"],
                "157em dual support cap theorem")
        initial: dict[tuple[int, bytes], int] = {}
        for equation in dual["equations"]:
            label = equation["label"]
            require(isinstance(label, list) and len(label) == 4 and
                    label[0] == 6 and label[1] == "hexagon_1_coface_0",
                    "157em dual equation label")
            key = (int(label[2]), bytes.fromhex(label[3]))
            require(len(key[1]) == WIDTH and key not in initial,
                    "157em dual support semantic key")
            initial[key] = int(equation["coefficient"]) % 3
        pivots = sorted(basis.rows, key=pool.pivot_order)
        semantic_pivots = []
        for pivot in pivots:
            row_data = basis.rows[pivot]
            packed = row_data[0] if isinstance(row_data, tuple) else row_data
            semantic_pivots.append((semantic_key(old, pool, pivot),
                                    semantic_row(old, pool, packed)))
        values, edges, pivot_values = reverse_lift_core(
            semantic_pivots, initial, monitor=monitor)
        self.values = values; self.edges = edges; self.dual = dual
        require(pivot_values == [0] * len(pivots),
                "157em raw lambda annihilates all pivot rows")
        dep_values = [dot_semantic(values, row) for row in dependent_raw]
        prior_values = [dot_semantic(values, row) for row in prior_block_raw]
        delta_values = [dot_semantic(values, {(c, bytes.fromhex(h)): a
            for (c, h), a in row.items()}) for row in remainders[1:]]
        base_value = dot_semantic(values, {(c, bytes.fromhex(h)): a
            for (c, h), a in remainders[0].items()})
        require(dep_values == [0] * len(dep_values) and
                prior_values == [0] * len(prior_values) and
                delta_values == [0] * 108 and base_value == 2,
                "157em raw lambda required annihilation/sign gates")
        support_rows = semantic_public(values)
        encoded = semantic_bytes(values)
        per_component = [sum(key[0] == component for key in values)
                         for component in range(1, 7)]
        self.support_rows = support_rows
        self.public = {"algorithm": "general-reverse-canonical-pivot-DP/v1",
            "support_count": len(values), "per_component": per_component,
            "packed_support_sha256": sha_bytes(encoded),
            "packed_support_bytes": len(encoded), "pivot_count": len(pivots),
            "reverse_edge_visits": edges,
            "pivot_annihilation_sha256": sha_obj(pivot_values),
            "dependent_event_count": len(dep_values),
            "dependent_annihilation_sha256": sha_obj(dep_values),
            "completed_block_column_count": len(prior_values),
            "completed_block_annihilation_sha256": sha_obj(prior_values),
            "delta_annihilation_sha256": sha_obj(delta_values),
            "base_z_scalar": base_value, "negative_base_scalar": (-base_value) % 3,
            "normalized_dual_whole_sha256": sha_obj(dual),
            "support_rows_not_serialized": True,
            "pool_IDs_or_old_qstar_used": False,
            "first_canary": support_rows[0] if support_rows else None,
            "last_canary": support_rows[-1] if support_rows else None}


def reverse_lift_core(
        pivots: Sequence[tuple[tuple[int, bytes],
                               dict[tuple[int, bytes], int]]],
        initial: dict[tuple[int, bytes], int], *,
        monitor: Monitor | None = None,
        support_cap: int | None = None,
        edge_cap: int | None = None,
        source_kind: str = "affine_normalized_dual",
        trace: dict[str, int] | None = None) \
        -> tuple[dict[tuple[int, bytes], int], int, list[int]]:
    """Pool-free shared reverse-pivot lift used by production and fixtures."""
    if trace is not None:
        trace["reverse_lift_core"] = trace.get("reverse_lift_core", 0)+1
    support_limit = CAPS["raw_lambda_support_entries"] if support_cap is None \
        else support_cap
    edge_limit = CAPS["raw_lambda_reverse_edge_visits"] if edge_cap is None \
        else edge_cap
    require(source_kind == "affine_normalized_dual" and
            type(support_limit) is int and support_limit >= 0 and
            type(edge_limit) is int and edge_limit >= 0,
            "157em reverse lift caps")
    labels = [pivot for pivot, _ in pivots]
    require(labels == sorted(labels) and len(labels) == len(set(labels)) and
            not set(initial).intersection(labels) and
            all(1 <= key[0] <= 6 and len(key[1]) == WIDTH
                for key in initial), "157em reverse lift labels/support")
    values = {key: int(value) % 3 for key, value in initial.items()
              if int(value) % 3}
    edges = 0; adapter = None if monitor is None else monitor.bind("dual_lift")
    for ordinal, (pivot, row) in enumerate(reversed(pivots), 1):
        require(row.get(pivot) == 1 and pivot == min(row),
                "157em normalized semantic pivot")
        total = 0
        for key, coefficient in row.items():
            require(int(coefficient) % 3 in (1, 2),
                    "157em normalized row coefficient")
            if key == pivot:
                continue
            require(key > pivot, "157em strict semantic pivot tail")
            edges += 1
            if edges > edge_limit:
                if edge_cap is not None:
                    raise RuntimeError("157em fixture reverse-edge cap")
                raise LaneResource("raw_lambda_reverse_edge_visits",
                    CAPS["raw_lambda_reverse_edge_visits"], edges, "gt",
                    "dual_lift", {"completed_reverse_pivots": ordinal-1})
            total = (total-int(coefficient)*values.get(key, 0)) % 3
            if adapter is not None and edges & 4095 == 0:
                adapter.check("raw_lambda_reverse_dp")
        if total:
            values[pivot] = total
            if len(values) > support_limit:
                if support_cap is not None:
                    raise RuntimeError("157em fixture support cap")
                raise LaneResource("raw_lambda_support_entries",
                    CAPS["raw_lambda_support_entries"], len(values), "gt",
                    "dual_lift", {"completed_reverse_pivots": ordinal})
    annihilation = [dot_semantic(values, row) for _, row in pivots]
    require(annihilation == [0]*len(pivots),
            "157em reverse lift direct dot annihilation")
    return values, edges, annihilation


def translation_from_pair(e4: Any, g: Any, h: Any) -> Any:
    value = e4.mul(g, e4.inverse(h))
    require(e4.mul(value, h) == g, "157em exact left translation orientation")
    return value


def contributor_record(component: int, g_blob: bytes, lam: int,
                       occurrence: dict[str, Any]) -> bytes:
    out = bytes([component]) + g_blob + bytes([lam]) + \
        bytes([int(occurrence["relator_index"])]) + \
        struct.pack(">H", int(occurrence["occurrence_ordinal"])) + \
        bytes.fromhex(occurrence["element_hex"]) + \
        bytes([int(occurrence["coefficient"])])
    require(len(out) == 314, "157em contributor record width")
    return out


def complete_correlation(e4: Any, pool: Any, support_rows: Sequence[Sequence[Any]],
                         occurrences: Sequence[dict[str, Any]], monitor: Monitor,
                         generation: int, cumulative: dict[str, int],
                         remaining_blocks: int) -> dict[str, Any]:
    by_component: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in occurrences:
        by_component[int(row["component"])].append(row)
    for rows in by_component.values():
        rows.sort(key=lambda row: (int(row["relator_index"]),
            int(row["occurrence_ordinal"]), bytes.fromhex(row["element_hex"])))
    inverse_h = {bytes.fromhex(row["element_hex"]): e4.inverse(row["_value"])
                 for row in occurrences}
    scalars: dict[tuple[bytes, int], int] = {}
    pairs = 0; adapter = monitor.bind("correlation_pass1")
    for component0, g_hex0, lam0 in support_rows:
        component = int(component0); g_blob = bytes.fromhex(str(g_hex0))
        require(len(g_blob) == WIDTH, "157em correlation support width")
        g = pool.unpack(g_blob); lam = int(lam0)
        for row in by_component[component]:
            pairs += 1
            if pairs > CAPS["correlation_pass1_pairs_per_generation"]:
                raise LaneResource("correlation_pass1_pairs_per_generation",
                    CAPS["correlation_pass1_pairs_per_generation"], pairs, "gt",
                    "correlation_pass1", {"generation": generation})
            if cumulative["pass1"] + pairs > CAPS["correlation_pass1_pairs_total"]:
                raise LaneResource("correlation_pass1_pairs_total",
                    CAPS["correlation_pass1_pairs_total"],
                    cumulative["pass1"] + pairs, "gt", "correlation_pass1",
                    {"generation": generation})
            t = e4.mul(g, inverse_h[bytes.fromhex(row["element_hex"])])
            require(e4.mul(t, row["_value"]) == g,
                    "157em correlation g*h inverse orientation")
            t_blob = pool.pack(t); key = (t_blob, int(row["relator_index"]))
            if key not in scalars and len(scalars) + 1 > \
                    CAPS["distinct_correlation_candidates"]:
                raise LaneResource("distinct_correlation_candidates",
                    CAPS["distinct_correlation_candidates"], len(scalars)+1,
                    "gt", "correlation_pass1", {"generation": generation})
            scalars[key] = (scalars.get(key, 0) +
                            lam * int(row["coefficient"])) % 3
            if pairs & 4095 == 0:
                adapter.check("correlation_pass1")
    expected = sum(sum(int(row[0]) == component for row in support_rows) *
                   len(by_component[component]) for component in range(1, 7))
    require(pairs == expected, "157em complete matching-pair count")
    cumulative["pass1"] += pairs
    active = [(key[0], key[1], value) for key, value in scalars.items() if value]
    active.sort(key=lambda row: (row[0], row[1]))
    if len(active) > CAPS["packed_active_rows"]:
        raise LaneResource("packed_active_rows", CAPS["packed_active_rows"],
            len(active), "gt", "correlation_pass1", {"generation": generation})
    zero_count = sum(value == 0 for value in scalars.values())
    active_bytes = b"".join(t + bytes([j, a]) for t, j, a in active)
    distinct = sorted({row[0] for row in active})
    selected = distinct[:min(len(distinct), CAPS["translations_per_batch"],
                             remaining_blocks)]
    selected_set = set(selected)
    jstar = {t: min(j for tt, j, value in active if tt == t and value)
             for t in selected}
    scalar_map = {(t, j): value for t, j, value in active}
    contributors: dict[bytes, tuple[bytes, dict[str, Any]]] = {}
    pass2 = 0; selected_filter = 0
    if selected:
        adapter2 = monitor.bind("correlation_pass2")
        for component0, g_hex0, lam0 in support_rows:
            component = int(component0); g_blob = bytes.fromhex(str(g_hex0))
            g = pool.unpack(g_blob); lam = int(lam0)
            for row in by_component[component]:
                pass2 += 1
                if pass2 > CAPS["correlation_pass2_pairs_per_generation"]:
                    raise LaneResource("correlation_pass2_pairs_per_generation",
                        CAPS["correlation_pass2_pairs_per_generation"], pass2,
                        "gt", "correlation_pass2", {"generation": generation})
                if cumulative["pass2"] + pass2 > \
                        CAPS["correlation_pass2_pairs_total"]:
                    raise LaneResource("correlation_pass2_pairs_total",
                        CAPS["correlation_pass2_pairs_total"],
                        cumulative["pass2"] + pass2, "gt",
                        "correlation_pass2", {"generation": generation})
                if pass2 & 4095 == 0:
                    adapter2.check("correlation_pass2")
                t = e4.mul(g, inverse_h[bytes.fromhex(row["element_hex"])])
                t_blob = pool.pack(t)
                if t_blob not in selected_set or \
                        int(row["relator_index"]) != jstar[t_blob]:
                    continue
                selected_filter += 1
                record = contributor_record(component, g_blob, lam, row)
                prior = contributors.get(t_blob)
                public = {"component": component, "g_hex": g_blob.hex(),
                    "lambda_coefficient": lam,
                    "relator_index": int(row["relator_index"]),
                    "occurrence_ordinal": int(row["occurrence_ordinal"]),
                    "h_hex": row["element_hex"],
                    "base_coefficient": int(row["coefficient"]),
                    "translation_hex": t_blob.hex(),
                    "record_hex": record.hex(), "record_sha256": sha_bytes(record)}
                if prior is None or record < prior[0]:
                    contributors[t_blob] = (record, public)
        cumulative["pass2"] += pass2
        require(set(contributors) == selected_set,
                "157em contributor for every selected translation")
    public = {"complete": True, "generation": generation,
        "pass1_pair_attempts": pairs, "pass2_pair_attempts": pass2,
        "pass2_selected_filter_count": selected_filter,
        "candidate_count_before_zero_deletion": len(scalars),
        "cancellation_to_zero_count": zero_count,
        "active_row_count": len(active),
        "active_distinct_translation_count": len(distinct),
        "scalar_distribution": {"1": sum(row[2] == 1 for row in active),
                                "2": sum(row[2] == 2 for row in active)},
        "active_packed_row_width": 156, "active_packed_bytes": len(active_bytes),
        "active_packed_sha256": sha_bytes(active_bytes),
        "selected_translation_count": len(selected),
        "selected_truncated": len(selected) < len(distinct),
        "selected_translation_sha256": sha_bytes(b"".join(selected)),
        "selected_bindings_sha256": sha_obj([[blob.hex(), jstar[blob],
            scalar_map[(blob, jstar[blob])]] for blob in selected]),
        "selection_order": "exact 154-byte translation blob lexicographic",
        "first_active": None if not active else {"translation_hex": active[0][0].hex(),
            "relator_index": active[0][1], "scalar": active[0][2]},
        "full_E4_enumerated": False, "pool_or_basis_mutated": False,
        "cumulative_pass1_pairs": cumulative["pass1"],
        "cumulative_pass2_pairs": cumulative["pass2"]}
    return {"public": public, "active": active, "selected": selected,
        "jstar": jstar, "scalar_map": scalar_map,
        "contributors": {blob: row[1] for blob, row in contributors.items()}}


def enforce_generation_capacity(remaining: int, batches: int,
                                generation: int, total_blocks: int) -> None:
    """Apply the total-block-before-batch precedence used by production."""
    require(type(remaining) is int and remaining >= 0 and
            type(batches) is int and 0 <= batches <=
                CAPS["column_generation_batches"] and
            type(generation) is int and generation >= 1 and
            type(total_blocks) is int and 0 <= total_blocks <=
                CAPS["total_new_translation_blocks"],
            "157en generation capacity inputs")
    current = {"generation": generation, "completed_batches": batches,
               "completed_blocks": total_blocks}
    if remaining == 0:
        raise LaneResource("total_new_translation_blocks",
            CAPS["total_new_translation_blocks"],
            CAPS["total_new_translation_blocks"]+1, "gt",
            "correlation_pass1", current,
            detail="total_translation_block_budget_exhausted")
    if batches == CAPS["column_generation_batches"]:
        raise LaneResource("column_generation_batches",
            CAPS["column_generation_batches"],
            CAPS["column_generation_batches"]+1, "gt",
            "correlation_pass1", current,
            detail="column_generation_batch_limit")


def upstream_caps(ed: Any, eg: Any) -> dict[str, int]:
    """Freshly derive and gate the literal reachable imported-cap table."""
    require(hasattr(ed, "UPSTREAM_RESOURCE_CAPS") and
            hasattr(ed, "CAPS") and hasattr(eg, "CAPS") and
            callable(getattr(eg, "upstream_caps", None)),
            "157em frozen upstream cap registry APIs")
    inherited = eg.upstream_caps(ed)
    rows = {key: int(inherited[key])
            for key in OLD_REACHABLE_RESOURCE_CAPS}
    for key in OLD_AFFINE_REACHABLE_RESOURCE_CAPS:
        value = int(inherited[key])
        require(key not in rows or rows[key] == value,
                "157em old affine cap collision")
        rows[key] = value
    for key in ED_REACHABLE_RESOURCE_CAPS:
        value = int(ed.CAPS[key])
        require(key not in rows or rows[key] == value,
                "157em 157ed cap collision")
        rows[key] = value
    for key in EG_REACHABLE_RESOURCE_CAPS:
        value = int(eg.CAPS[key])
        require(key not in rows or rows[key] == value,
                "157em 157eg cap collision")
        rows[key] = value
    expected = (OLD_REACHABLE_RESOURCE_CAPS |
        OLD_AFFINE_REACHABLE_RESOURCE_CAPS |
        ED_REACHABLE_RESOURCE_CAPS | EG_REACHABLE_RESOURCE_CAPS)
    require(set(rows) == set(expected) == set(EXPECTED_UPSTREAM_CAPS) and
            rows == EXPECTED_UPSTREAM_CAPS and
            not {"transaction_trace_records", "blocker_table",
                 "candidate_element_pool_suffix", "directed_columns",
                 "missing_bounded_inverse_representative"} & set(rows),
            "157em exact reachable upstream resource registry")
    return dict(sorted(rows.items()))


def structural_stop(old: Any, key: str, observed: int, comparison: str,
                    phase: str, current: dict[str, Any] | None = None) \
        -> LaneResource:
    caps = getattr(old, "CAPS", {})
    require(key in caps and type(caps[key]) is int,
            "157em structural resource key")
    return LaneResource(key, int(caps[key]), observed, comparison, phase,
                        current, source="upstream", inner=key)


def seed_base_recovery(recovery: RecoveryMap,
                       occurrences: Sequence[dict[str, Any]]) -> None:
    for row in occurrences:
        recovery.consider_direct(int(row["component"]),
            bytes.fromhex(row["element_hex"]),
            108 + int(row["relator_index"]),
            int(row["term_ordinal"]))


def translated_recovery_edges(e4: Any, pool: Any, t_blob: bytes,
                              occurrences: Sequence[dict[str, Any]]) \
        -> list[tuple[int, bytes, bytes, int, int, bytes]]:
    t = pool.unpack(t_blob); rows = []
    for row in occurrences:
        value = e4.mul(t, row["_value"])
        rows.append((int(row["component"]), pool.pack(value), t_blob,
            int(row["relator_index"]), int(row["term_ordinal"]),
            bytes.fromhex(row["element_hex"])))
    require(len(rows) == len(occurrences),
            "157em complete translated recovery edge set")
    return rows


def apply_manual_recovery_once(recovery: RecoveryMap, t_blob: bytes,
                               edges: Sequence[tuple[int, bytes, bytes,
                                                     int, int, bytes]],
                               applied: set[bytes]) -> None:
    require(t_blob not in applied and all(row[2] == t_blob for row in edges),
            "157em manual recovery exactly once")
    for edge in edges:
        recovery.apply_translated_prechecked(*edge)
    applied.add(t_blob)


def prefix_word_at(old: Any, word: Sequence[int], signed_offset: int) \
        -> list[int]:
    require(1 <= signed_offset <= len(word), "157em source offset range")
    prefix: list[int] = []
    for ordinal, letter in enumerate(word, 1):
        if letter < 0:
            prefix = old.reduce_word(prefix + [int(letter)])
        if ordinal == signed_offset:
            return list(prefix)
        if letter > 0:
            prefix = old.reduce_word(prefix + [int(letter)])
    raise RuntimeError("157em unreachable source offset")


def _save_existing_expression_role(expressions: Any,
                                   key: tuple[Any, ...],
                                   saved: dict[int, frozenset[str]]) -> None:
    node = expressions.keys.get(key)
    if node is not None and node not in saved:
        saved[int(node)] = frozenset(expressions.roles.get(int(node), set()))


def _expression_flat(expressions: Any, old: Any, word: Sequence[int],
                     blob: bytes, role: str,
                     saved: dict[int, frozenset[str]] | None) -> int:
    if saved is not None:
        reduced = tuple(old.reduce_word(word))
        _save_existing_expression_role(
            expressions, ("flat", reduced, blob), saved)
    return expressions.flat(word, blob, role)


def _expression_inverse(expressions: Any, parent: int, role: str,
                        saved: dict[int, frozenset[str]] | None) -> int:
    if saved is not None:
        _save_existing_expression_role(expressions, ("inverse", parent), saved)
    return expressions.inverse(parent, role)


def _expression_product(expressions: Any, left: int, right: int, role: str,
                        saved: dict[int, frozenset[str]] | None) -> int:
    if saved is not None:
        _save_existing_expression_role(
            expressions, ("product", left, right), saved)
    return expressions.product(left, right, role)


def _section_expression_root(sections: Any, role: str, tagged: int,
                             old: Any,
                             saved: dict[int, frozenset[str]] | None) -> int:
    expressions = sections.expressions
    if tagged >= sections.EXPR_TAG:
        root = tagged-sections.EXPR_TAG
        if saved is not None and root not in saved:
            saved[root] = frozenset(expressions.roles.get(root, set()))
        return sections.expression_root(tagged, role)
    word = sections.bfs.materialize(tagged)
    value = sections.pool.eval_id(word)
    return _expression_flat(expressions, old, word,
                            sections.pool.blob(value), role, saved)


def recovery_expression_root(old: Any, prefix: dict[str, Any],
                             recovery: RecoveryMap,
                             words: Sequence[Sequence[int]],
                             occurrences: Sequence[dict[str, Any]],
                             component: int, blob: bytes, role: str,
                             role_snapshot: dict[int, frozenset[str]] | None =
                                None) \
        -> tuple[int, dict[str, Any]]:
    """Promote only one selected semantic parent to a section DAG root."""
    descriptor = recovery.descriptor(component, blob)
    sections, pool = prefix["sections"], prefix["pool"]
    expressions = sections.expressions
    if descriptor["kind"] == "direct_target_source_prefix":
        source = int(descriptor["source_word_ordinal"])
        offset = int(descriptor["signed_letter_offset"])
        require(source < len(words), "157em target source ordinal")
        word = prefix_word_at(old, words[source], offset)
        root = _expression_flat(expressions, old, word, blob,
                                role + "_direct_target", role_snapshot)
        method = "target_word_signed_prefix"
        require(expressions.value_blob(root) == blob,
                "157em direct recovery root binding")
        return root, {**descriptor, "method": method,
                      "expression_value_sha256": sha_bytes(blob)}
    if descriptor["kind"] == "direct_base_support_prefix":
        relator = int(descriptor["relator_index"])
        offset = int(descriptor["term_ordinal"])
        matches = [row for row in occurrences
                   if int(row["relator_index"]) == relator and
                      int(row["term_ordinal"]) == offset and
                      int(row["component"]) == component and
                      bytes.fromhex(row["element_hex"]) == blob]
        require(len(matches) == 1, "157em base direct recovery")
        root = int(matches[0]["section_expression_root"])
        method = "base_D2_canonical_support_prefix"
        require(expressions.value_blob(root) == blob,
                "157em direct recovery root binding")
        return root, {**descriptor, "method": method,
                      "expression_value_sha256": sha_bytes(blob)}
    require(descriptor["kind"] ==
            "registered_translation_times_base_prefix",
            "157em recovery descriptor kind")
    u_blob = bytes.fromhex(descriptor["translation_hex"])
    parent_blob = bytes.fromhex(descriptor["parent_hex"])
    tagged = sections.by_blob.get(u_blob)
    require(tagged is not None, "157em registered recovery translation")
    u_root = _section_expression_root(
        sections, role + "_registered_u", tagged, old, role_snapshot)
    matches = [row for row in occurrences
               if int(row["relator_index"]) == descriptor["relator_index"] and
                  int(row["term_ordinal"]) == descriptor["term_ordinal"] and
                  int(row["component"]) == component and
                  bytes.fromhex(row["element_hex"]) == parent_blob]
    require(len(matches) == 1, "157em translated base parent")
    h_root = int(matches[0]["section_expression_root"])
    root = _expression_product(expressions, u_root, h_root,
                               role + "_translated_parent", role_snapshot)
    require(expressions.value_blob(root) == blob,
            "157em translated recovery value")
    return root, {**descriptor, "method": "registered_u_times_base_prefix",
                  "registered_u_root_private": u_root,
                  "base_h_root_private": h_root,
                  "expression_value_sha256": sha_bytes(blob)}


def owned_materialize(old: Any, e4: Any, expressions: Any, node: int,
                      monitor: Monitor, phase: str,
                      *, trace: dict[str, int] | None = None) -> list[int]:
    require(0 <= node < len(expressions.kind), "157em materialize root")
    adapter = monitor.bind(phase); memo: dict[int, list[int]] = {}

    def visit(current: int) -> list[int]:
        if current in memo:
            return memo[current]
        require(0 <= current < len(expressions.kind),
                "157em materialize child")
        kind = int(expressions.kind[current])
        if kind == expressions.IDENTITY:
            word: list[int] = []
        elif kind == expressions.SIGNED_GENERATOR:
            word = [int(expressions.signed_generator[current])]
        elif kind == expressions.FLAT:
            flat = expressions.flat_words[current]
            require(flat is not None, "157em materialize flat")
            word = list(flat)
        elif kind == expressions.INVERSE:
            child = visit(int(expressions.left[current]))
            attempted = len(child)
            if attempted > CAPS["inverse_materialized_letters"]:
                raise LaneResource("inverse_materialized_letters",
                    CAPS["inverse_materialized_letters"], attempted, "gt",
                    phase, {"node": current})
            adapter.reserve("section_recovery", attempted * 8)
            word = old.inv_word(child)
            if trace is not None:
                trace["owned_inverse"] = trace.get("owned_inverse", 0) + 1
        else:
            require(kind == expressions.PRODUCT,
                    "157em materialize opcode")
            left = visit(int(expressions.left[current]))
            right = visit(int(expressions.right[current]))
            adapter.reserve("section_recovery", (len(left)+len(right))*8)
            word = old.reduce_word(left + right)
        cap = int(old.CAPS["single_word_or_section_length"])
        if len(word) > cap:
            raise structural_stop(old, "single_word_or_section_length",
                                  len(word), "gt", phase, {"node": current})
        require(element_blob(e4.eval(word)) ==
                bytes(expressions.value_blobs[current]),
                "157em owned materializer value")
        memo[current] = word
        return word
    return visit(node)


def recovery_section_word(old: Any, e4: Any, prefix: dict[str, Any],
                          recovery: RecoveryMap,
                          words: Sequence[Sequence[int]],
                          occurrences: Sequence[dict[str, Any]],
                          component: int, blob: bytes, monitor: Monitor) \
        -> tuple[list[int], dict[str, Any]]:
    """Read a selected recovery descriptor without mutating persistent state."""
    descriptor = recovery.descriptor(component, blob)
    sections = prefix["sections"]
    if descriptor["kind"] == "direct_target_source_prefix":
        source = int(descriptor["source_word_ordinal"])
        offset = int(descriptor["signed_letter_offset"])
        word = prefix_word_at(old, words[source], offset)
        method = "target_word_signed_prefix"
        require(element_blob(e4.eval(word)) == blob,
                "157em direct recovery word value")
        return word, {**descriptor, "method": method,
                      "word_length": len(word), "word_sha256": sha_obj(word)}
    if descriptor["kind"] == "direct_base_support_prefix":
        relator = int(descriptor["relator_index"])
        offset = int(descriptor["term_ordinal"])
        matches = [row for row in occurrences
            if int(row["relator_index"]) == relator and
               int(row["term_ordinal"]) == offset and
               int(row["component"]) == component and
               bytes.fromhex(row["element_hex"]) == blob]
        require(len(matches) == 1, "157em base recovery word")
        word = list(matches[0]["section_word"])
        method = "base_D2_canonical_support_prefix"
        require(element_blob(e4.eval(word)) == blob,
                "157em direct base recovery word value")
        return word, {**descriptor, "method": method,
                      "word_length": len(word), "word_sha256": sha_obj(word)}
    require(descriptor["kind"] ==
            "registered_translation_times_base_prefix",
            "157em recovery word descriptor kind")
    u_blob = bytes.fromhex(descriptor["translation_hex"])
    parent_blob = bytes.fromhex(descriptor["parent_hex"])
    tagged = sections.by_blob.get(u_blob)
    require(tagged is not None, "157em recovery registered u")
    if tagged < sections.EXPR_TAG:
        u_word = sections.bfs.materialize(tagged)
    else:
        u_word = owned_materialize(old, e4, sections.expressions,
            tagged-sections.EXPR_TAG, monitor, "section_recovery")
    matches = [row for row in occurrences
        if int(row["relator_index"]) == descriptor["relator_index"] and
           int(row["term_ordinal"]) == descriptor["term_ordinal"] and
           int(row["component"]) == component and
           bytes.fromhex(row["element_hex"]) == parent_blob]
    require(len(matches) == 1, "157em recovery base parent word")
    word = old.reduce_word(u_word + list(matches[0]["section_word"]))
    require(element_blob(e4.eval(word)) == blob,
            "157em translated recovery word value")
    return word, {**descriptor, "method": "registered_u_times_base_prefix",
                  "word_length": len(word), "word_sha256": sha_obj(word)}


def recover_selected_sections(old: Any, e4: Any, prefix: dict[str, Any],
                              recovery: RecoveryMap,
                              words: Sequence[Sequence[int]],
                              occurrences: Sequence[dict[str, Any]],
                              correlation: dict[str, Any], monitor: Monitor,
                              generation: int) -> dict[str, Any]:
    roots: list[int] = []; public: list[dict[str, Any]] = []
    # Deliberately separate from the persistent prefix.  No section, pool,
    # basis, proof-DAG, or persistent expression mutation occurs in preflight.
    expressions = old.SectionExpressionDAG(prefix["pool"])
    selected = correlation["selected"]
    for ordinal, t_blob in enumerate(selected, 1):
        pair = correlation["contributors"][t_blob]
        require(bytes.fromhex(pair["translation_hex"]) == t_blob and
                pair["relator_index"] == correlation["jstar"][t_blob],
                "157em selected contributor binding")
        component = int(pair["component"])
        g_blob = bytes.fromhex(pair["g_hex"])
        h_blob = bytes.fromhex(pair["h_hex"])
        g_word, g_recovery = recovery_section_word(old, e4, prefix, recovery,
            words, occurrences, component, g_blob, monitor)
        g_root = expressions.flat(g_word, g_blob,
            f"generation_{generation}_translation_{ordinal}_g")
        h_matches = [row for row in occurrences
            if int(row["component"]) == component and
               int(row["relator_index"]) == int(pair["relator_index"]) and
               int(row["occurrence_ordinal"]) ==
                    int(pair["occurrence_ordinal"]) and
               bytes.fromhex(row["element_hex"]) == h_blob]
        require(len(h_matches) == 1, "157em contributor h root")
        h_root = expressions.flat(h_matches[0]["section_word"], h_blob,
            f"generation_{generation}_translation_{ordinal}_h")
        inverse_root = expressions.inverse(h_root,
            f"generation_{generation}_translation_{ordinal}_inverse_h")
        t_root = expressions.product(g_root, inverse_root,
            f"generation_{generation}_translation_{ordinal}_t")
        require(expressions.value_blob(t_root) == t_blob,
                "157em section t=g*h^-1")
        roots.append(t_root)
        canary = ordinal == 1 or ordinal == len(selected) or ordinal % 64 == 0
        direct: dict[str, Any] | None = None
        if canary:
            word = owned_materialize(old, e4, expressions, t_root,
                                     monitor, "section_recovery")
            require(element_blob(e4.eval(word)) == t_blob,
                    "157em materialized selected translation")
            direct = {"word_length": len(word),
                "word_sha256": sha_obj(word), "value_hex": t_blob.hex()}
        public.append({"generation": generation,
            "translation_ordinal": ordinal, "translation_hex": t_blob.hex(),
            "jstar": correlation["jstar"][t_blob],
            "correlation_scalar": correlation["scalar_map"][
                (t_blob, correlation["jstar"][t_blob])],
            "contributor": pair,
            "g_recovery": {k: v for k, v in g_recovery.items()
                if not k.endswith("_private") and k != "root"},
            "expression_root_private": t_root,
            "g_word_private": g_word,
            "h_word_private": list(h_matches[0]["section_word"]),
            "materialization_canary": direct})
    payload, renumber = expressions.serialize_reachable(
        roots, monitor.bind("section_recovery")) if roots else (
        {"format": "typed-section-expression-arrays/v1", "node_count": 0,
         "edge_count": 0, "roots": [], "arrays": {},
         "canonical_value_width": WIDTH,
         "node_order": "zero_based_topological",
         "ordinary_word_composition": True,
         "manifest_sha256": sha_obj({"arrays": {}, "roots": []})}, {})
    for row in public:
        row["expression_root"] = renumber.pop(
            row.pop("expression_root_private"))
        # These bounded words remain private staging inputs for the commit;
        # hashes and typed DAG nodes are the public certificate.
    stable = [{k: v for k, v in row.items() if not k.endswith("_private")}
              for row in public]
    return {"selected": stable, "selected_count": len(stable),
        "selected_sha256": sha_obj(stable), "expression_DAG": payload,
        "owned_inverse_materializer": True,
        "materialization_cadence": "first,last,and-every-64th",
        "all_values_exact": True,
        "_private": {bytes.fromhex(row["translation_hex"]): {
            "g_word": row.pop("g_word_private"),
            "h_word": row.pop("h_word_private"),
            "component": row["contributor"]["component"],
            "g_hex": row["contributor"]["g_hex"],
            "h_hex": row["contributor"]["h_hex"]}
            for row in public}}


def capture_initial_target(ei: Any, old: Any, seed_info: dict[str, Any],
                           e4: Any, source: dict[str, Any],
                           inverse_words: Sequence[Any],
                           prefix: dict[str, Any], anchor: dict[str, Any],
                           monitor: Monitor) -> dict[str, Any]:
    """Execute the frozen 109-row path once while retaining semantic rows."""
    captured_remainders: list[dict[tuple[int, str], int]] = []
    captured_deltas: list[dict[Any, int]] = []
    original_probe = old._affine_probe_remainder
    original_formula = old.affine_target6_formula

    def probe(raw: Any, *args: Any, **kwargs: Any) -> Any:
        result = original_probe(raw, *args, **kwargs)
        captured_remainders.append(dict(result)); return result

    def formula(seed: Sequence[int], *args: Any, **kwargs: Any) -> Any:
        result = original_formula(seed, *args, **kwargs)
        if kwargs.get("include_gradient") and seed:
            captured_deltas.append(dict(result["_direct_gradient"]))
        return result

    old._affine_probe_remainder = probe
    old.affine_target6_formula = formula
    try:
        target, system, base_raw, static = ei._target6_system(
            old, seed_info, e4, source, inverse_words, prefix, anchor, monitor)
    finally:
        old._affine_probe_remainder = original_probe
        old.affine_target6_formula = original_formula
    require(len(captured_remainders) == 109 and len(captured_deltas) == 108,
            "157em captured exact 109 target rows")
    require(target["target6"]["fresh_remainder_sha256"] ==
            B1["fresh_remainders_sha256"] and
            target["target6"]["typed_split_sha256"] ==
            B1["typed_split_sha256"] and
            target["target6"]["direct_gradient_bindings_sha256"] ==
            B1["direct_bindings_sha256"] and
            target["affine_system"]["row_space_sha256"] ==
            B1["target_row_space_sha256"] and
            target["affine_system"]["rank"] == B1["rank"] and
            target["affine_system"]["nullity"] == B1["nullity"] and
            target["affine_system"]["equations"] == B1["equations"] and
            target["affine_system"]["consistent"] is False,
            "157em fresh B1 target anchors")
    raw_gradients = [dict(base_raw), *captured_deltas]
    require(len(raw_gradients) == 109,
            "157em retained target raw gradient count")
    return {"public": target, "system": system, "static": static,
        "base_raw": base_raw, "raw_gradients": raw_gradients,
        "remainders": captured_remainders}


def base_raw_columns(old: Any, e4: Any) -> list[dict[Any, int]]:
    rows: list[dict[Any, int]] = []
    for relator in old.pure_relations(4):
        gradient, value = old.fox_gradient_without_sections(relator, e4)
        require(value == e4.identity and old.d1(gradient, e4) == {},
                "157em base D2 column gates")
        rows.append(gradient)
    require(len(rows) == 11, "157em eleven base columns")
    return rows


def direct_translated_semantic(e4: Any, t: Any,
                               occurrences: Sequence[dict[str, Any]],
                               relator: int) \
        -> dict[tuple[int, bytes], int]:
    row: dict[tuple[int, bytes], int] = {}
    for occurrence in occurrences:
        if int(occurrence["relator_index"]) != relator:
            continue
        key = (int(occurrence["component"]),
               element_blob(e4.mul(t, occurrence["_value"])))
        value = (row.get(key, 0) + int(occurrence["coefficient"])) % 3
        if value:
            row[key] = value
        else:
            row.pop(key, None)
    return row


def stage_batch(old: Any, e4: Any, prefix: dict[str, Any],
                occurrences: Sequence[dict[str, Any]],
                base_columns: Sequence[dict[Any, int]],
                raw_lambda: RawLambda, correlation: dict[str, Any],
                sections_stage: dict[str, Any], monitor: Monitor,
                generation: int) -> dict[str, Any]:
    """Precompute the entire batch without touching persistent prefix state."""
    before = state_accounting(prefix, pool_digest=True)
    adapter = monitor.bind("batch_precompute")
    private_sections = sections_stage["_private"]
    rows: list[dict[str, Any]] = []; sparse_entries = 0
    for ordinal, t_blob in enumerate(correlation["selected"], 1):
        adapter.check("batch_precompute", force=(ordinal == 1 or ordinal % 16 == 0))
        t = prefix["pool"].unpack(t_blob)
        require(element_blob(t) == t_blob and t_blob in private_sections,
                "157em staged translation binding")
        for relator in range(1, 12):
            direct = direct_translated_semantic(e4, t, occurrences, relator)
            typed_raw = old.translate_vector(base_columns[relator-1], t, e4)
            typed = {(component, element_blob(value)): int(coefficient) % 3
                     for (component, value), coefficient in typed_raw.items()
                     if int(coefficient) % 3}
            require(direct == typed and e4.eval(old.pure_relations(4)[relator-1]) ==
                    e4.identity and old.d1(typed_raw, e4) == {},
                    "157em staged direct/typed/D1D2 gates")
            scalar = dot_semantic(raw_lambda.values, direct)
            expected = int(correlation["scalar_map"].get((t_blob, relator), 0))
            require(scalar == expected,
                    "157em staged lambda/correlation scalar")
            sparse_entries += len(direct)
            if sparse_entries > CAPS["batch_staged_sparse_entries"]:
                raise LaneResource("batch_staged_sparse_entries",
                    CAPS["batch_staged_sparse_entries"], sparse_entries,
                    "gt", "batch_precompute", {"generation": generation,
                    "translation_ordinal": ordinal, "relator": relator})
            raw = semantic_bytes(direct)
            rows.append({"generation": generation,
                "translation_ordinal": ordinal, "translation_blob": t_blob,
                "relator": relator, "lambda_scalar": scalar,
                "raw": direct, "raw_sha256": sha_bytes(raw),
                "typed_sha256": sha_bytes(semantic_bytes(typed)),
                "direct_equals_typed": True, "quotient_identity": True,
                "D1_D2_zero": True})
    after = state_accounting(prefix, pool_digest=True)
    require(before == after and len(rows) == len(correlation["selected"])*11,
            "157em all-selected all-eleven state-neutral preflight")
    if correlation["selected"]:
        first = correlation["selected"][0]
        jstar = correlation["jstar"][first]
        vector = [int(correlation["scalar_map"].get((first, j), 0))
                  for j in range(1, 12)]
        require(vector[:jstar-1] == [0]*(jstar-1) and
                vector[jstar-1] in (1, 2),
                "157em first translation earliest active relator")
    public = {k: v for k, v in sections_stage.items() if k != "_private"}
    return {"public": {"generation": generation,
        "translation_count": len(correlation["selected"]),
        "column_count": len(rows), "staged_sparse_entries": sparse_entries,
        "all_selected_before_mutation": True,
        "all_eleven_before_mutation": True,
        "state_neutrality_before": before,
        "state_neutrality_after": after,
        "section_provenance": public,
        "row_binding_sha256": sha_obj([[row["translation_blob"].hex(),
            row["relator"], row["lambda_scalar"], row["raw_sha256"],
            row["typed_sha256"]] for row in rows])},
        "rows": rows, "sections": private_sections}


def state_accounting(prefix: dict[str, Any], *, pool_digest: bool) \
        -> dict[str, Any]:
    pool, basis, dag, sections = (prefix[key] for key in
                                  ("pool", "basis", "dag", "sections"))
    pool_sha: str | None = None
    if pool_digest:
        h = hashlib.sha256()
        for identifier, blob in enumerate(pool.values):
            require(pool.ids.get(blob) == identifier,
                    "157em pool schedule integrity")
            h.update(blob)
        pool_sha = h.hexdigest()
    return {"columns": basis.columns_seen, "pivots": len(basis.rows),
        "dependent": basis.dependent_columns,
        "live_sparse_entries": basis.live_vector_entries,
        "pool_size": len(pool.values), "pool_order_sha256": pool_sha,
        "DAG_nodes": dag.node_count, "DAG_edges": dag.edge_count,
        "section_bindings": len(sections.by_blob),
        "section_expression_nodes": len(sections.expressions.kind),
        "section_expression_edges": sections.expressions.edge_count,
        "recovery": None}


class PackedBlockLedger:
    RECORD_BYTES = 225

    def __init__(self) -> None:
        self.translations = bytearray(); self.records = bytearray()
        self.translation_count = 0; self.record_count = 0

    def checkpoint(self) -> tuple[int, int, int, int]:
        return (len(self.translations), len(self.records),
                self.translation_count, self.record_count)

    def rollback(self, checkpoint: tuple[int, int, int, int]) -> None:
        t_bytes, r_bytes, t_count, r_count = checkpoint
        require(0 <= t_bytes <= len(self.translations) and
                0 <= r_bytes <= len(self.records) and
                t_bytes == t_count*WIDTH and
                r_bytes == r_count*self.RECORD_BYTES,
                "157em packed ledger rollback checkpoint")
        del self.translations[t_bytes:]; del self.records[r_bytes:]
        self.translation_count = t_count; self.record_count = r_count

    def preflight_batch(self, translation_count: int) -> None:
        require(type(translation_count) is int and
                0 <= translation_count <= CAPS["translations_per_batch"],
                "157em packed batch preflight count")
        t_bytes = len(self.translations)+translation_count*WIDTH
        r_bytes = len(self.records)+translation_count*11*self.RECORD_BYTES
        t64 = 4*((t_bytes+2)//3); r64 = 4*((r_bytes+2)//3)
        if t_bytes > CAPS["packed_translation_table_bytes"]:
            raise LaneResource("packed_translation_table_bytes",
                CAPS["packed_translation_table_bytes"], t_bytes, "gt",
                "block_commit", {"completed_record_count": self.record_count})
        if t64 > CAPS["packed_translation_table_base64_bytes"]:
            raise LaneResource("packed_translation_table_base64_bytes",
                CAPS["packed_translation_table_base64_bytes"], t64, "gt",
                "block_commit", {"completed_record_count": self.record_count})
        if r_bytes > CAPS["packed_block_ledger_decoded_bytes"]:
            raise LaneResource("packed_block_ledger_decoded_bytes",
                CAPS["packed_block_ledger_decoded_bytes"], r_bytes, "gt",
                "block_commit", {"completed_record_count": self.record_count})
        if r64 > CAPS["packed_block_ledger_base64_bytes"]:
            raise LaneResource("packed_block_ledger_base64_bytes",
                CAPS["packed_block_ledger_base64_bytes"], r64, "gt",
                "block_commit", {"completed_record_count": self.record_count})

    def add_translation(self, blob: bytes) -> None:
        require(len(blob) == WIDTH, "157em translation table width")
        attempted = len(self.translations) + WIDTH
        if attempted > CAPS["packed_translation_table_bytes"]:
            raise LaneResource("packed_translation_table_bytes",
                CAPS["packed_translation_table_bytes"], attempted, "gt",
                "block_commit", {"translation_count": self.translation_count})
        self.translations.extend(blob); self.translation_count += 1

    def add_record(self, generation: int, ordinal: int, relator: int,
                   scalar: int, independent: bool,
                   pivot: tuple[int, bytes] | None,
                   raw_sha: str, typed_sha: str) -> None:
        require(1 <= generation <= CAPS["column_generation_batches"] and
                1 <= ordinal <= 1024 and
                1 <= relator <= 11 and scalar in (0, 1, 2),
                "157em packed record fields")
        if pivot is None:
            pivot_component, pivot_blob = 0, bytes(WIDTH)
        else:
            pivot_component, pivot_blob = pivot
            require(1 <= pivot_component <= 6 and len(pivot_blob) == WIDTH,
                    "157em packed semantic pivot")
        flags = (1 if independent else 0) | 2 | 4 | 8
        record = bytes([generation]) + struct.pack("<H", ordinal) + \
            bytes([relator, flags, scalar, pivot_component]) + pivot_blob + \
            bytes.fromhex(raw_sha) + bytes.fromhex(typed_sha)
        require(len(record) == self.RECORD_BYTES,
                "157em exact 225-byte record")
        attempted = len(self.records)+len(record)
        if attempted > CAPS["packed_block_ledger_decoded_bytes"]:
            raise LaneResource("packed_block_ledger_decoded_bytes",
                CAPS["packed_block_ledger_decoded_bytes"], attempted, "gt",
                "block_commit", {"record_count": self.record_count})
        self.records.extend(record); self.record_count += 1

    def public(self, monitor: Monitor) -> dict[str, Any]:
        adapter = monitor.bind("receipt_serialization")
        adapter.reserve("receipt_serialization",
            len(self.translations)+len(self.records)+
            4*((len(self.translations)+2)//3+(len(self.records)+2)//3))
        t64 = base64.b64encode(self.translations).decode("ascii")
        r64 = base64.b64encode(self.records).decode("ascii")
        require(len(t64) <= CAPS["packed_translation_table_base64_bytes"] and
                len(r64) <= CAPS["packed_block_ledger_base64_bytes"],
                "157em packed ledger base64 caps")
        return {"format": "complete-D2-block-ledger/v1",
            "translation_encoding": "exact-E4-blob154-no-padding",
            "translation_count": self.translation_count,
            "translation_decoded_bytes": len(self.translations),
            "translation_sha256": sha_bytes(bytes(self.translations)),
            "translation_base64_length": len(t64),
            "translation_base64_sha256": sha_bytes(t64.encode("ascii")),
            "translation_base64": t64,
            "record_encoding": "generation-u8|translation-ordinal-u16le|relator-u8|flags-u8|lambda-u8|pivot-component-u8|pivot-blob154|raw-sha256|typed-sha256",
            "record_endianness": "little", "record_bytes": self.RECORD_BYTES,
            "record_count": self.record_count,
            "decoded_bytes": len(self.records),
            "decoded_sha256": sha_bytes(bytes(self.records)),
            "base64_length": len(r64),
            "base64_sha256": sha_bytes(r64.encode("ascii")),
            "base64": r64, "flags_unused_high_nibble_zero": True,
            "JSON_column_objects_used": False}

    def partial_public(self) -> dict[str, Any]:
        return {"format": "complete-D2-block-ledger/v1-partial",
            "translation_count": self.translation_count,
            "translation_decoded_bytes": len(self.translations),
            "translation_sha256": sha_bytes(bytes(self.translations)),
            "record_bytes": self.RECORD_BYTES,
            "record_count": self.record_count,
            "decoded_bytes": len(self.records),
            "decoded_sha256": sha_bytes(bytes(self.records)),
            "base64_omitted_for_resource_partial": True}


def decode_packed_ledger(public: dict[str, Any]) \
        -> tuple[list[bytes], list[dict[str, Any]]]:
    require(set(public) == PACKED_LEDGER_KEYS and
            public["format"] == "complete-D2-block-ledger/v1" and
            public["record_bytes"] == 225 and
            public["record_endianness"] == "little" and
            public["flags_unused_high_nibble_zero"] is True and
            public["JSON_column_objects_used"] is False,
            "157em packed ledger header")
    translation_raw = base64.b64decode(public["translation_base64"],
                                       validate=True)
    record_raw = base64.b64decode(public["base64"], validate=True)
    require(len(translation_raw) == public["translation_decoded_bytes"] ==
                public["translation_count"]*WIDTH and
            sha_bytes(translation_raw) == public["translation_sha256"] and
            len(public["translation_base64"]) ==
                public["translation_base64_length"] and
            sha_bytes(public["translation_base64"].encode("ascii")) ==
                public["translation_base64_sha256"] and
            len(record_raw) == public["decoded_bytes"] ==
                public["record_count"]*225 and
            sha_bytes(record_raw) == public["decoded_sha256"] and
            len(public["base64"]) == public["base64_length"] and
            sha_bytes(public["base64"].encode("ascii")) ==
                public["base64_sha256"],
            "157em packed ledger hashes/lengths")
    translations = [translation_raw[index:index+WIDTH]
                    for index in range(0, len(translation_raw), WIDTH)]
    rows: list[dict[str, Any]] = []
    for offset in range(0, len(record_raw), 225):
        record = record_raw[offset:offset+225]
        generation = record[0]; ordinal = struct.unpack("<H", record[1:3])[0]
        relator, flags, scalar, component = record[3:7]
        pivot_blob = record[7:161]
        require(1 <= generation <= CAPS["column_generation_batches"] and
                1 <= ordinal <= 1024 and
                1 <= relator <= 11 and flags & 0xf0 == 0 and
                flags & 0x0e == 0x0e and scalar in (0, 1, 2) and
                ((flags & 1 and 1 <= component <= 6) or
                 (not flags & 1 and component == 0 and pivot_blob == bytes(WIDTH))),
                "157em packed record field gates")
        rows.append({"generation": generation,
            "translation_ordinal": ordinal, "relator": relator,
            "flags": flags, "lambda_scalar": scalar,
            "pivot_component": component, "pivot_blob": pivot_blob,
            "raw_sha256": record[161:193].hex(),
            "typed_sha256": record[193:225].hex()})
    return translations, rows


def validate_packed_generation_bindings(generation_row: dict[str, Any],
                                        translations: Sequence[bytes],
                                        rows: Sequence[dict[str, Any]]) -> None:
    """Cross-bind one completed generation to its packed public records."""
    generation = generation_row["generation"]
    preflight, commit = (generation_row["preflight"],
                         generation_row["commit"])
    selected = preflight["section_provenance"]["selected"]
    expected_translations = [bytes.fromhex(item["translation_hex"])
                             for item in selected]
    require(list(translations) == expected_translations and
            len(rows) == 11*len(expected_translations) ==
                commit["column_count"],
            "157em packed generation translation/count binding")
    preflight_binding: list[list[Any]] = []
    outcomes: list[dict[str, Any]] = []
    cursor = 0
    for translation_ordinal, translation in enumerate(translations, 1):
        for relator in range(1, 12):
            packed = rows[cursor]; cursor += 1
            independent = bool(packed["flags"] & 1)
            pivot = (None if not independent else
                [packed["pivot_component"], packed["pivot_blob"].hex()])
            require(packed["generation"] == generation and
                    packed["translation_ordinal"] == translation_ordinal and
                    packed["relator"] == relator,
                    "157em packed generation/translation/relator order")
            preflight_binding.append([translation.hex(), relator,
                packed["lambda_scalar"], packed["raw_sha256"],
                packed["typed_sha256"]])
            outcomes.append({"translation_ordinal": translation_ordinal,
                "relator": relator, "independent": independent,
                "lambda_scalar": packed["lambda_scalar"], "pivot": pivot})
    require(cursor == len(rows) and
            sha_obj(preflight_binding) == preflight["row_binding_sha256"] and
            sha_obj(outcomes) == commit["outcome_semantic_sha256"],
            "157em packed rows/preflight/commit semantic digest binding")


def translation_transaction_snapshot(prefix: dict[str, Any],
                                     recovery: RecoveryMap,
                                     recovery_edges: Sequence[tuple[int, bytes,
                                         bytes, int, int, bytes]],
                                     ledger: PackedBlockLedger,
                                     t_blob: bytes) -> dict[str, Any]:
    """O(1)+76-edge checkpoint before one persistent translation block."""
    pool, basis, dag, sections = (prefix[key] for key in
                                  ("pool", "basis", "dag", "sections"))
    expressions = sections.expressions
    complete_masks = prefix.get("_em_complete_block_masks")
    require(isinstance(complete_masks, dict),
            "157em transaction complete-block mask registry")
    return {"pool": pool.checkpoint(), "basis_rows": len(basis.rows),
        "basis_columns": basis.columns_seen,
        "basis_dependent": basis.dependent_columns,
        "basis_live": basis.live_vector_entries,
        "basis_max_vector": basis.max_vector_support,
        "basis_max_transient": basis.max_transient_vector_support,
        "basis_eliminations": basis.elimination_operations,
        "basis_pivot_introductions": len(basis.pivot_introductions),
        "dag": dag.checkpoint(), "dag_max_nodes": dag.max_nodes,
        "dag_max_edges": dag.max_edges,
        "section_BFS_nodes": len(sections.parent),
        "section_BFS_bindings": len(sections.by_element),
        "section_base_prefix_bindings": len(sections.base_prefix_roots),
        "section_by_blob_present": t_blob in sections.by_blob,
        "section_by_blob_value": sections.by_blob.get(t_blob),
        "section_directed_present": t_blob in sections.directed_blobs,
        "section_directed_root": sections.directed_roots.get(t_blob),
        "expression_nodes": len(expressions.kind),
        "expression_edges": expressions.edge_count,
        "expression_keys": len(expressions.keys),
        "expression_peak_nodes": expressions.peak_nodes,
        "expression_peak_edges": expressions.peak_edges,
        "expression_roles": {},
        "complete_mask_present": t_blob in complete_masks,
        "complete_mask_value": complete_masks.get(t_blob),
        "recovery": recovery.checkpoint(recovery_edges),
        "ledger": ledger.checkpoint()}


def rollback_translation_transaction(prefix: dict[str, Any],
                                     recovery: RecoveryMap,
                                     ledger: PackedBlockLedger,
                                     t_blob: bytes,
                                     snapshot: dict[str, Any]) -> None:
    pool, basis, dag, sections = (prefix[key] for key in
                                  ("pool", "basis", "dag", "sections"))
    expressions = sections.expressions
    complete_masks = prefix.get("_em_complete_block_masks")
    require(isinstance(complete_masks, dict),
            "157em rollback complete-block mask registry")
    while len(basis.rows) > int(snapshot["basis_rows"]):
        basis.rows.popitem()
    require(len(basis.rows) == int(snapshot["basis_rows"]),
            "157em basis rollback suffix")
    basis.columns_seen = int(snapshot["basis_columns"])
    basis.dependent_columns = int(snapshot["basis_dependent"])
    basis.live_vector_entries = int(snapshot["basis_live"])
    basis.max_vector_support = int(snapshot["basis_max_vector"])
    basis.max_transient_vector_support = int(snapshot["basis_max_transient"])
    basis.elimination_operations = int(snapshot["basis_eliminations"])
    del basis.pivot_introductions[int(snapshot["basis_pivot_introductions"]):]
    dag.rollback(tuple(snapshot["dag"]))
    dag.max_nodes = int(snapshot["dag_max_nodes"])
    dag.max_edges = int(snapshot["dag_max_edges"])

    if snapshot["section_by_blob_present"]:
        sections.by_blob[t_blob] = snapshot["section_by_blob_value"]
    else:
        sections.by_blob.pop(t_blob, None)
    if snapshot["section_directed_present"]:
        sections.directed_blobs.add(t_blob)
        sections.directed_roots[t_blob] = snapshot["section_directed_root"]
    else:
        sections.directed_blobs.discard(t_blob)
        sections.directed_roots.pop(t_blob, None)
    node_count = int(snapshot["expression_nodes"])
    key_count = int(snapshot["expression_keys"])
    while len(expressions.keys) > key_count:
        key, node = expressions.keys.popitem()
        require(int(node) >= node_count,
                "157em expression rollback key suffix")
    del expressions.kind[node_count:]
    del expressions.signed_generator[node_count:]
    del expressions.left[node_count:]; del expressions.right[node_count:]
    del expressions.flat_words[node_count:]
    del expressions.value_blobs[node_count:]
    for node in list(expressions.roles):
        if node >= node_count:
            del expressions.roles[node]
    for node, roles in snapshot["expression_roles"].items():
        expressions.roles[int(node)] = set(roles)
    expressions.edge_count = int(snapshot["expression_edges"])
    expressions.peak_nodes = int(snapshot["expression_peak_nodes"])
    expressions.peak_edges = int(snapshot["expression_peak_edges"])
    if snapshot["complete_mask_present"]:
        complete_masks[t_blob] = int(snapshot["complete_mask_value"])
    else:
        complete_masks.pop(t_blob, None)
    recovery.rollback(snapshot["recovery"])
    ledger.rollback(tuple(snapshot["ledger"]))
    pool.rollback(int(snapshot["pool"]))
    require(len(sections.parent) == snapshot["section_BFS_nodes"] and
            len(sections.by_element) == snapshot["section_BFS_bindings"] and
            len(sections.base_prefix_roots) ==
                snapshot["section_base_prefix_bindings"] and
            len(expressions.kind) == node_count and
            expressions.edge_count == snapshot["expression_edges"],
            "157em exact translation transaction rollback")


def commit_batch(old: Any, e4: Any, prefix: dict[str, Any],
                 recovery: RecoveryMap,
                 words: Sequence[Sequence[int]],
                 occurrences: Sequence[dict[str, Any]],
                 correlation: dict[str, Any], staged: dict[str, Any],
                 ledger: PackedBlockLedger, monitor: Monitor,
                 generation: int, completed_blocks: set[bytes]) \
        -> dict[str, Any]:
    pool, basis, dag, sections = (prefix[key] for key in
                                  ("pool", "basis", "dag", "sections"))
    require(basis.deadline is None and dag.deadline is None,
            "157em detached before block commit")
    adapter = monitor.bind("block_commit")
    basis.deadline = adapter; dag.deadline = adapter
    prior_recovery_phase = getattr(basis, "_em_recovery_phase", None)
    setattr(basis, "_em_recovery_phase", "block_commit")
    pre = state_accounting(prefix, pool_digest=True)
    pre["recovery"] = recovery.public()
    progress: dict[str, Any] = {"generation": generation,
        "selected_translation_count": len(correlation["selected"]),
        "completed_translations": 0, "attempted_translation": 0,
        "completed_relators": 0, "attempted_relator": 0,
        "batch_anchor_committed": False,
        "unfinished_translation_rolled_back": False,
        "rollback_translation_ordinal": None,
        "completed_record_count": ledger.record_count,
        "pre_accounting": pre, "completed_translation_prefix": []}
    rows_by_translation: dict[bytes, list[dict[str, Any]]] = defaultdict(list)
    for row in staged["rows"]:
        rows_by_translation[row["translation_blob"]].append(row)
    new_pivots: list[dict[tuple[int, bytes], int]] = []
    new_pivot_keys: list[int] = []
    outcomes: list[dict[str, Any]] = []
    first_pivot_event: dict[str, Any] | None = None
    try:
        ledger.preflight_batch(len(correlation["selected"]))
        for ordinal, t_blob in enumerate(correlation["selected"], 1):
            require(t_blob not in completed_blocks and
                    [row["relator"] for row in rows_by_translation[t_blob]] ==
                    list(range(1, 12)),
                    "157em no prior complete block/all eleven staged")
            progress["attempted_translation"] = ordinal
            recovery_edges = translated_recovery_edges(
                e4, pool, t_blob, occurrences)
            recovery.preflight_translated(recovery_edges, phase="block_commit")
            transaction = translation_transaction_snapshot(
                prefix, recovery, recovery_edges, ledger, t_blob)
            pivot_prefix = len(new_pivots); outcome_prefix = len(outcomes)
            packed_pivot_prefix = len(new_pivot_keys)
            try:
                roles = transaction["expression_roles"]
                g_root, _ = recovery_expression_root(old, prefix, recovery,
                    words, occurrences,
                    int(staged["sections"][t_blob]["component"]),
                    bytes.fromhex(staged["sections"][t_blob]["g_hex"]),
                    f"generation_{generation}_translation_{ordinal}_g_commit",
                    roles)
                h_blob = bytes.fromhex(staged["sections"][t_blob]["h_hex"])
                h_word = staged["sections"][t_blob]["h_word"]
                h_root = _expression_flat(sections.expressions, old,
                    h_word, h_blob,
                    f"generation_{generation}_translation_{ordinal}_h_commit",
                    roles)
                inv_root = _expression_inverse(sections.expressions, h_root,
                    f"generation_{generation}_translation_{ordinal}_inverse_h_commit",
                    roles)
                t_root = _expression_product(sections.expressions,
                    g_root, inv_root,
                    f"generation_{generation}_translation_{ordinal}_t_commit",
                    roles)
                require(sections.expressions.value_blob(t_root) == t_blob,
                        "157em committed section expression value")
                t = pool.unpack(t_blob)
                tagged, newly = sections.register_directed(t, t_root)
                if not newly:
                    require(tagged >= sections.EXPR_TAG and
                            tagged-sections.EXPR_TAG == t_root,
                            "157em registered section exact provenance reuse")
                translation_id = pool.ids.get(t_blob)
                require(translation_id is not None and
                        sections.node_for(translation_id) == tagged,
                        "157em committed section/pool binding")
                ledger.add_translation(t_blob)
                for row in rows_by_translation[t_blob]:
                    relator = int(row["relator"])
                    progress["attempted_relator"] = relator
                    adapter.check("block_commit", force=(relator == 1))
                    before = len(basis.rows)
                    basis.add_column(relator, translation_id, tagged,
                                     translation_ordinal=
                                        32976+ledger.translation_count)
                    after = len(basis.rows); independent = after == before+1
                    require(after-before in (0, 1),
                            "157em reducer pivot delta")
                    pivot: tuple[int, bytes] | None = None
                    if independent:
                        packed_pivot = next(reversed(basis.rows))
                        pivot = semantic_key(old, pool, packed_pivot)
                        reduced = semantic_row(
                            old, pool, basis.rows[packed_pivot][0])
                        require(reduced.get(pivot) == 1 and
                                 all(key >= pivot for key in reduced),
                                 "157em normalized strict new pivot")
                        new_pivots.append(reduced)
                        new_pivot_keys.append(packed_pivot)
                    if ordinal == 1 and relator == \
                            correlation["jstar"][t_blob]:
                        require(independent and row["lambda_scalar"] in (1, 2),
                                "157em first jstar immediate pivot theorem")
                        first_pivot_event = {"translation_ordinal": ordinal,
                            "relator": relator,
                            "scalar": row["lambda_scalar"],
                            "pivot": None if pivot is None else
                                [pivot[0], pivot[1].hex()]}
                    ledger.add_record(generation, ordinal, relator,
                        int(row["lambda_scalar"]), independent, pivot,
                        row["raw_sha256"], row["typed_sha256"])
                    outcomes.append({"translation_ordinal": ordinal,
                        "relator": relator, "independent": independent,
                        "lambda_scalar": row["lambda_scalar"],
                        "pivot": None if pivot is None else
                            [pivot[0], pivot[1].hex()]})
                    progress["completed_relators"] = relator
                    progress["completed_record_count"] = ledger.record_count
            except BaseException:
                rollback_translation_transaction(
                    prefix, recovery, ledger, t_blob, transaction)
                del new_pivots[pivot_prefix:]; del outcomes[outcome_prefix:]
                del new_pivot_keys[packed_pivot_prefix:]
                progress["unfinished_translation_rolled_back"] = True
                progress["rollback_translation_ordinal"] = ordinal
                progress["completed_relators"] = 0
                progress["completed_record_count"] = ledger.record_count
                raise
            complete_masks = prefix.get("_em_complete_block_masks")
            require(isinstance(complete_masks, dict) and
                    complete_masks.get(t_blob) == (1 << 11)-1,
                    "157em successful adaptive complete-block mask")
            completed_blocks.add(t_blob)
            progress["completed_translations"] = ordinal
            progress["completed_relators"] = 0
            progress["completed_translation_prefix"].append(t_blob.hex())
        progress["batch_anchor_committed"] = True
        require(first_pivot_event is not None,
                "157em first selected translation pivot event")
        post = state_accounting(prefix, pool_digest=True)
        post["recovery"] = recovery.public()
        require(post["columns"]-pre["columns"] ==
                11*len(correlation["selected"]),
                "157em complete block column count")
        return {"public": {"generation": generation,
            "complete": True, "translation_count": len(correlation["selected"]),
            "column_count": len(outcomes),
            "rank_gain": post["pivots"]-pre["pivots"],
            "dependent_gain": post["dependent"]-pre["dependent"],
            "pre_accounting": pre, "post_accounting": post,
            "first_translation_jstar_pivot": first_pivot_event,
            "outcome_semantic_sha256": sha_obj(outcomes),
            "all_blocks_complete": True,
            "all_staged_before_first_mutation": True},
            "new_pivots": new_pivots, "new_pivot_keys": new_pivot_keys,
            "progress": progress}
    except BaseException as exc:
        progress["post_failure_accounting"] = state_accounting(
            prefix, pool_digest=True)
        progress["post_failure_accounting"]["recovery"] = recovery.public()
        if isinstance(exc, LaneResource):
            exc.current = copy.deepcopy(progress)
        else:
            setattr(exc, "em_block_current", copy.deepcopy(progress))
        raise
    finally:
        require(basis.deadline is adapter and dag.deadline is adapter,
                "157em commit adapter retained")
        basis.deadline = None; dag.deadline = None
        if prior_recovery_phase is None:
            if hasattr(basis, "_em_recovery_phase"):
                delattr(basis, "_em_recovery_phase")
        else:
            setattr(basis, "_em_recovery_phase", prior_recovery_phase)


def semantic_pivot_set_sha256(old: Any, pool: Any,
                              packed_keys: Sequence[int]) -> str:
    """Canonical streaming digest; never binds private pool identifiers."""
    ordered = sorted(packed_keys, key=pool.pivot_order)
    digest = hashlib.sha256(b"d972-157em-semantic-pivot-set-v1\x00" +
                            struct.pack(">I", len(ordered)))
    prior: tuple[int, bytes] | None = None
    for packed in ordered:
        component, identifier = old.unpack_vector_key(packed)
        row = (component, pool.blob(identifier))
        require(prior is None or prior < row,
                "157em unique sorted semantic old pivots")
        digest.update(bytes([component])); digest.update(row[1]); prior = row
    return digest.hexdigest()


def canonical_incremental_pivot_order(
        old: Any, prefix: dict[str, Any],
        new_pivots: Sequence[dict[tuple[int, bytes], int]],
        new_pivot_keys: Sequence[int], expected_old_pivot_count: int,
        adapter: Any, progress: dict[str, Any],
        expected_order_sha256: str | None = None,
        expected_pivots: Sequence[tuple[int, bytes]] | None = None) \
        -> tuple[list[dict[tuple[int, bytes], int]], str]:
    """Project actual new stored rows through Bk, then freeze pivot order.

    SparseBoundaryBasis stops as soon as it finds a new minimum pivot, so its
    stored tail may still contain later pivots of Bk.  Those old coordinates
    are removed here without mutating the pool or basis.  Only the resulting
    quotient rows may act on the 109 already-Bk-normal remainders.
    """
    pool, basis = prefix["pool"], prefix["basis"]
    require(len(new_pivots) == len(new_pivot_keys) and
            all(isinstance(row, dict) and row for row in new_pivots) and
            len(set(new_pivot_keys)) == len(new_pivot_keys),
            "157em actual independent pivot row/key universe")
    new_key_set = set(new_pivot_keys)
    require(all(key in basis.rows for key in new_key_set) and
            len(basis.rows)-len(new_key_set) == expected_old_pivot_count,
            "157em fixed precommit old-pivot view")
    old_keys = [key for key in basis.rows if key not in new_key_set]
    old_digest = semantic_pivot_set_sha256(old, pool, old_keys)
    progress.update({"old_pivot_count": len(old_keys),
        "old_pivot_set_encoding":
            "domain:d972-157em-semantic-pivot-set-v1\\0|count:u32be|"
            "repeated(component:u8,blob:154)",
        "old_pivot_set_sha256": old_digest,
        "completed_quotient_pivot_ordinal": 0,
        "completed_quotient_prefix_sha256": sha_obj([]),
        "quotient_rows_discarded_on_failure": False})
    pool_size = len(pool.values); basis_size = len(basis.rows)
    quotient_rows: list[dict[tuple[int, bytes], int]] = []
    eliminations = 0
    try:
        for ordinal, (published, packed_pivot) in enumerate(
                zip(new_pivots, new_pivot_keys), 1):
            actual_packed = dict(basis.rows[packed_pivot][0])
            actual_semantic = semantic_row(old, pool, actual_packed)
            require(actual_semantic == dict(published) and
                    min(actual_packed, key=pool.pivot_order) == packed_pivot,
                    "157em actual persistent independent row/pivot binding")
            pending = dict(actual_packed)
            free: dict[int, int] = {}
            while pending:
                key = min(pending, key=pool.pivot_order)
                coefficient = pending[key]
                if key in basis.rows and key not in new_key_set:
                    old_row = basis.rows[key][0]
                    require(old_row.get(key) == 1 and
                            all(pool.pivot_order(tail) >= pool.pivot_order(key)
                                for tail in old_row),
                            "157em normalized old-basis quotient row")
                    for tail, value in old_row.items():
                        result = (pending.get(tail, 0)-coefficient*value) % 3
                        if result:
                            pending[tail] = result
                        else:
                            pending.pop(tail, None)
                    eliminations += 1
                    if eliminations & 1023 == 0:
                        adapter.check("affine_full_remainder")
                else:
                    free[key] = pending.pop(key)
                observed = len(pending)+len(free)
                if observed > CAPS["target_live_remainders"]:
                    raise LaneResource("target_live_remainders",
                        CAPS["target_live_remainders"], observed, "gt",
                        "incremental_reduction", progress)
            require(packed_pivot in free and free[packed_pivot] == 1 and
                    all(key not in basis.rows or key in new_key_set
                        for key in free),
                    "157em quotient row old-pivot zero/leading one")
            quotient = semantic_row(old, pool, free)
            actual_pivot = semantic_key(old, pool, packed_pivot)
            require(min(quotient) == actual_pivot and
                    all(key == actual_pivot or key > actual_pivot
                        for key in quotient),
                    "157em quotient row actual pivot/strict tail")
            quotient_rows.append(quotient)
            progress["completed_quotient_pivot_ordinal"] = ordinal
        ordered = sorted(quotient_rows, key=lambda row: min(row))
        pivots = [min(row) for row in ordered]
        require(len(set(pivots)) == len(pivots),
                "157em unique quotient incremental pivots")
        if expected_pivots is not None:
            require(list(expected_pivots) == pivots,
                    "157em incremental claimed pivot/tail order")
        projection = [semantic_public(row) for row in ordered]
        order_digest = sha_obj(projection)
        if expected_order_sha256 is not None:
            require(expected_order_sha256 == order_digest,
                    "157em incremental reduction-order binding")
        progress["completed_quotient_prefix_sha256"] = sha_obj([
            semantic_public(row) for row in quotient_rows])
        require(len(pool.values) == pool_size and len(basis.rows) == basis_size,
                "157em quotient projection state neutrality")
        return ordered, order_digest
    except BaseException:
        progress["completed_quotient_prefix_sha256"] = sha_obj([
            semantic_public(row) for row in quotient_rows])
        progress["quotient_rows_discarded_on_failure"] = True
        require(len(pool.values) == pool_size and len(basis.rows) == basis_size,
                "157em failed quotient projection state neutrality")
        raise


def incremental_remainders(old: Any, prefix: dict[str, Any],
                           remainders: Sequence[dict[tuple[int, str], int]],
                           new_pivots: Sequence[dict[tuple[int, bytes], int]],
                           new_pivot_keys: Sequence[int],
                           expected_old_pivot_count: int,
                           raw_gradients: Sequence[dict[Any, int]],
                           anchor_ids: Sequence[int], monitor: Monitor,
                           generation: int) -> tuple[list[dict[tuple[int, str], int]],
                                                     dict[str, Any]]:
    require(len(remainders) == len(raw_gradients) == 109,
            "157em incremental row universe")
    before = [dict(row) for row in remainders]
    before_sha = sha_obj([sorted(row.items()) for row in before])
    work = [dict(row) for row in before]
    adapter = monitor.bind("incremental_reduction")
    progress = {"generation": generation, "completed_new_pivot_ordinal": 0,
        "completed_rows_in_current_pivot": 0,
        "pre_update_remainder_sha256": before_sha,
        "last_fully_updated_row_sha256": None,
        "current_new_pivot_prefix_sha256": sha_obj([]),
        "new_pivot_count": len(new_pivots),
        "reduction_order_sha256": None,
        "old_pivot_count": None, "old_pivot_set_encoding": None,
        "old_pivot_set_sha256": None,
        "completed_quotient_pivot_ordinal": 0,
        "completed_quotient_prefix_sha256": sha_obj([]),
        "quotient_rows_discarded_on_failure": False,
        "live_entry_count": sum(map(len, before)),
        "batch_anchor_committed": True, "rolled_back_on_failure": False}
    try:
        ordered_pivots, reduction_order_sha = \
            canonical_incremental_pivot_order(old, prefix, new_pivots,
                new_pivot_keys, expected_old_pivot_count, adapter, progress)
        progress["reduction_order_sha256"] = reduction_order_sha
        for pivot_ordinal, row in enumerate(ordered_pivots, 1):
            pivot = min(row)
            progress["completed_rows_in_current_pivot"] = 0
            for ordinal, remainder in enumerate(work):
                coefficient = remainder.get((pivot[0], pivot[1].hex()), 0)
                if coefficient:
                    for (component, blob), value in row.items():
                        key = (component, blob.hex())
                        result = (remainder.get(key, 0)-coefficient*value) % 3
                        if result:
                            remainder[key] = result
                        else:
                            remainder.pop(key, None)
                progress["completed_rows_in_current_pivot"] = ordinal+1
                progress["last_fully_updated_row_sha256"] = \
                    sha_obj(sorted(remainder.items()))
                if ordinal % 16 == 0:
                    adapter.check("incremental_reduction")
            progress["completed_new_pivot_ordinal"] = pivot_ordinal
            progress["completed_rows_in_current_pivot"] = 0
            progress["current_new_pivot_prefix_sha256"] = sha_obj([
                semantic_public(value) for value in
                ordered_pivots[:pivot_ordinal]])
            live = sum(map(len, work)); progress["live_entry_count"] = live
            if live > CAPS["target_live_remainders"]:
                raise LaneResource("target_live_remainders",
                    CAPS["target_live_remainders"], live, "gt",
                    "incremental_reduction", progress)
        cadence: list[dict[str, Any]] = []
        for ordinal in (0, 1, 54, 108):
            direct = old._affine_probe_remainder(raw_gradients[ordinal],
                prefix, anchor_ids, adapter)
            require(direct == work[ordinal],
                    "157em incremental/fresh direct cadence")
            cadence.append({"ordinal": ordinal,
                "sha256": sha_obj(sorted(direct.items())), "equal": True})
        return work, {**progress, "complete": True,
            "post_update_remainder_sha256":
                sha_obj([sorted(row.items()) for row in work]),
            "fresh_direct_cadence": cadence}
    except BaseException as exc:
        progress["rolled_back_on_failure"] = True
        progress["remaining_rows"] = [None]*109
        if isinstance(exc, LaneResource):
            exc.current = copy.deepcopy(progress)
        else:
            setattr(exc, "em_incremental_current", copy.deepcopy(progress))
        raise


def solve_from_remainders(ei: Any, old: Any, e4: Any,
                          remainders: Sequence[dict[tuple[int, str], int]],
                          monitor: Monitor, generation: int) \
        -> tuple[Any, dict[str, Any]]:
    require(len(remainders) == 109, "157em solve row count")
    base = dict(remainders[0]); delta: dict[tuple[int, str], dict[int, int]] = {}
    for seed_index, row in enumerate(remainders[1:]):
        for coordinate, coefficient in row.items():
            delta.setdefault(coordinate, {})[seed_index] = coefficient
    live = sum(map(len, remainders))
    system = old.AffineSystem(108, coordinate_widths=(e4.degree, e4.pc.n))
    adapter = monitor.bind("target_resolve")
    target_row, affine = ei._solve_transposed_target_core(
        old, system, base, delta, live, adapter,
        expected_coordinate_count=len(set(base).union(delta)))
    return system, {"generation": generation, "target_row": target_row,
        "affine_system": affine, "variables": 108,
        "remainder_count": 109, "live_remainder_entries": live,
        "remainders_sha256": semantic_remainders_sha256(remainders),
        "old_remainder_or_dual_imported": False,
        "complete_all_coordinates": True}


def public_semantic_from_rows(rows: Sequence[Sequence[Any]]) \
        -> dict[tuple[int, bytes], int]:
    result: dict[tuple[int, bytes], int] = {}
    for component, value_hex, coefficient in rows:
        key = (int(component), bytes.fromhex(str(value_hex)))
        require(len(key[1]) == WIDTH and int(coefficient) in (1, 2),
                "157em imported public semantic row")
        require(key not in result, "157em duplicate public semantic key")
        result[key] = int(coefficient)
    return result


EG_PREFIX_KEYS = frozenset({"pool", "sections", "dag", "basis", "model4",
    "raw_source_tuple", "base_source_key", "directed_base_support",
    "directed_surgery", "accounting", "157ed_dependent_events",
    "157ed_prefix_bindings"})
EM_PREFIX_PRIVATE_KEYS = frozenset({"_em_complete_block_masks",
    "_em_complete_blocks", "_em_complete_block_public"})


def exact_eg_prefix_projection(prefix: dict[str, Any]) -> dict[str, Any]:
    """Expose exactly the authenticated 157eg prefix shape, by identity."""
    require(set(prefix) == EG_PREFIX_KEYS | EM_PREFIX_PRIVATE_KEYS,
            "157em full/private prefix exact shape")
    projected = {key: prefix[key] for key in EG_PREFIX_KEYS}
    require(set(projected) == EG_PREFIX_KEYS and
            all(projected[key] is prefix[key] for key in EG_PREFIX_KEYS),
            "157em 157eg prefix projection identity")
    return projected


def construct_fixed_B1(ei: Any, old: Any, ed: Any, eg: Any, e4: Any,
                       prefix: dict[str, Any], dependent: list[Any],
                       recovery: RecoveryMap, monitor: Monitor) \
        -> dict[str, Any]:
    pool = prefix["pool"]
    eg_prefix = exact_eg_prefix_projection(prefix)
    bundle = eg.rebuild_base_bundle(old, eg_prefix, e4)
    require(bundle["public"]["ordered_sha256"] == BASE_OCCURRENCE_SHA and
            bundle["public"]["occurrence_count"] == 76,
            "157em exact base occurrence bundle")
    occurrences = base_occurrences_exact(old, e4, prefix["sections"], pool)
    numbered_projection = [{key: row[key] for key in (
        "relator_index", "component", "coefficient", "element_hex",
        "section_word")} for row in occurrences]
    require(numbered_projection == bundle["public"]["occurrences"] and
            sha_obj(numbered_projection) == BASE_OCCURRENCE_SHA and
            [row["occurrence_ordinal"] for row in occurrences] ==
                list(range(1, 77)),
            "157em numbered 76-occurrence projection")
    bundle = {**bundle, "private_occurrences": occurrences}
    seed_base_recovery(recovery, occurrences)
    raw_adapter = monitor.bind("fixed_B1")
    qstar = ed.validate_qstar_label(ed.QSTAR_LABEL, WIDTH)
    oracle = ed.RawLambdaOracle(old, prefix, qstar, raw_adapter)
    pivot_zero = [oracle.packed(prefix["basis"].rows[pivot][0])
        for pivot in sorted(prefix["basis"].rows, key=pool.pivot_order)]
    require(pivot_zero == [0]*362709,
            "157em frozen old qstar B0-only annihilation")
    support = eg.lambda_support(oracle, WIDTH)
    mul, inverse = eg.uncached_ops(old, e4)
    old_corr = eg.exact_correlation(support["rows"], occurrences,
        width=WIDTH, unpack=pool.unpack, mul=mul, inverse=inverse,
        pack=pool.pack, monitor=raw_adapter)
    witness = eg.make_section_witness(old, e4, prefix, occurrences,
                                      old_corr, raw_adapter)
    ei._require_correlation(old_corr, witness)
    first = old_corr["public"]["first_active"]
    require(isinstance(first, dict), "157em fixed B1 active translation")
    expected_t = bytes.fromhex(first["translation_hex"])
    pending_edges = translated_recovery_edges(e4, pool, expected_t,
                                                occurrences)
    recovery.preflight_translated(pending_edges, phase="fixed_B1")
    basis = prefix["basis"]; prior_phase = getattr(
        basis, "_em_recovery_phase", None)
    setattr(basis, "_em_recovery_phase", "fixed_B1")
    try:
        block, anchor = ei._commit_block(old, eg, prefix, oracle, monitor)
    finally:
        if prior_phase is None:
            if hasattr(basis, "_em_recovery_phase"):
                delattr(basis, "_em_recovery_phase")
        else:
            setattr(basis, "_em_recovery_phase", prior_phase)
        # The support-one object has no reference in the adaptive state.
        oracle = None; qstar = None
    require(block["complete"] is True and block["column_count"] == 11 and
            block["translation_ordinal"] == 32976 and
            block["raw_columns_sha256"] == B1["raw_columns_sha256"] and
            block["reducer_ledger_sha256"] == B1["reducer_ledger_sha256"] and
            block["rank_gain"] == 11 and
            block["old_qstar_scalars"] == [0]*8+[1, 0, 0] and
            anchor["anchor_semantic_sha256"] == B1["anchor_semantic_sha256"],
            "157em fresh fixed B1 block anchors")
    accounting = state_accounting(prefix, pool_digest=False)
    require(accounting["columns"] == B1["columns"] and
            accounting["pivots"] == B1["pivots"] and
            accounting["dependent"] == B1["dependent"] and
            accounting["live_sparse_entries"] == B1["live_sparse_entries"],
            "157em B1 accounting")
    t_blob = bytes.fromhex(block["translation_hex"])
    require(t_blob == expected_t, "157em fixed B1 translation binding")
    before_manual = recovery.translated_candidates
    manual_applied: set[bytes] = set()
    apply_manual_recovery_once(recovery, t_blob, pending_edges, manual_applied)
    require(recovery.translated_candidates-before_manual == 76 and
            manual_applied == {t_blob},
            "157em fixed B1 base-dispatch recovery count")
    dependent_raw = [public_semantic_from_rows(event["raw_column"])
                     for event in dependent]
    block_raw = [public_semantic_from_rows(row["raw_column"]["entries"])
                 for row in block["columns"]]
    require(len(dependent_raw) == 16 and len(block_raw) == 11,
            "157em dependent/B1 raw ledgers")
    return {"block": block, "anchor": anchor, "bundle": bundle,
        "old_qstar_provenance": {
            "used_only_to_freshly_reconstruct_fixed_B1": True,
            "used_after_fixed_B1": False,
            "support_count": support["count"],
            "support_sha256": support["ordered_sha256"],
            "complete_correlation_sha256":
                old_corr["public"]["packed_rows_sha256"]},
        "dependent_raw": dependent_raw, "block_raw": block_raw,
        "completed_translation": t_blob,
        "state": accounting}


def source_preflight(old: Any, seed_words: Sequence[Any], e4: Any,
                     raw_source_key: Sequence[Any],
                     inverse_words: Sequence[Any], monitor: Monitor) \
        -> dict[str, Any]:
    adapter = monitor.bind("source_preflight")
    progress = {"current_seed": None, "evaluated_seeds": 0,
                "records_prefix_sha256": sha_obj([])}

    class Progress:
        @property
        def started(self) -> float:
            return adapter.started

        @property
        def deadline(self) -> float:
            return adapter.deadline

        def mark(self, index: int) -> None:
            progress["current_seed"] = index
            progress["evaluated_seeds"] = index-1

        def check(self, inner: str, force: bool = False, **kw: Any) -> None:
            current = int(progress["current_seed"] or 0)
            progress["evaluated_seeds"] = current
            adapter.check(inner, force=force, **kw)

        def reserve(self, inner: str, additional_bytes: int) -> None:
            adapter.reserve(inner, additional_bytes)

    tracked = Progress()
    try:
        result = old._affine_source_preflight(seed_words, e4,
            tuple(raw_source_key), inverse_words, tracked,
            progress=tracked.mark)
    except BaseException as exc:
        if hasattr(old, "_source_prefix_rows"):
            progress["records_prefix_sha256"] = sha_obj(
                old._source_prefix_rows(e4, int(progress["evaluated_seeds"])))
        setattr(exc, "em_source_current", copy.deepcopy(progress)); raise
    require(result["supported"] is True and result["seed_count"] == 108 and
            result["all_source_tuples_equal"] is True and
            result["all_correction_occurrences_identity"] is True,
            "157em source preflight complete")
    return result


def phase_close(phases: dict[str, float], label: str,
                started: float) -> float:
    now = time.monotonic(); phases[label] = now-started
    print("D972_B345_DUAL_COLGEN_PHASE " + label +
          f" elapsed_s={phases[label]:.6f}", flush=True)
    return now


def validate_prefix_provider(row: dict[str, Any], *, sealed: bool,
                             trace: dict[str, int] | None = None) -> None:
    """Shared anchor validator; sealed fixtures cannot impersonate B0/B1."""
    if trace is not None:
        trace["prefix_provider"] = trace.get("prefix_provider", 0)+1
    if sealed:
        require(row.get("sealed_bounded_fixture") is True and
                row.get("fresh_immutable_prefix") is False and
                0 < int(row.get("columns", 0)) < 362725 and
                0 < int(row.get("pivots", 0)) < 362709 and
                row.get("production_stable_digest_imported") is False and
                row.get("mathematical_claim") == "none",
                "157em sealed bounded provider boundary")
    else:
        require("sealed_bounded_fixture" not in row and
                row["counts"]["columns"] == 362725 and
                row["counts"]["pivots"] == 362709 and
                row["counts"]["dependent_columns"] == 16 and
                row["counts"]["live_sparse_entries"] == 3090367 and
                row["fresh_not_imported"] is True,
                "157em production B0 provider")


def target_public(system: Any,
                  remainders: Sequence[dict[tuple[int, str], int]],
                  generation: int) -> dict[str, Any]:
    dual = system.dual_public()
    public = {"generation": generation, "variables": 108,
        "equations": system.equations, "rank": system.rank(),
        "nullity": system.nullity(), "consistent": system.consistent,
        "row_space_sha256": system.digest(),
        "remainders_sha256": semantic_remainders_sha256(remainders),
        "live_remainder_entries": sum(map(len, remainders)),
        "complete_all_coordinates": True,
        "stopped_at_first_contradiction": False,
        "dual": dual}
    require(public["rank"]+public["nullity"] == 108 and
            public["equations"] == len(set(remainders[0]).union(
                *(set(row) for row in remainders[1:]))),
            "157em complete target public")
    return public


TOP_KEYS = {"schema", "task_sha256", "terminal_token", "status",
    "reason", "phase", "pins", "caps", "caps_sha256", "upstream_caps",
    "upstream_caps_sha256", "algorithm", "base_q3_replay",
    "normalized_inverse_fibre", "seed_manifest", "source_preflight",
    "directed_base_support", "directed_surgery", "prefix_B0",
    "base_columns", "fixed_B1_block", "fixed_B1_anchor",
    "old_qstar_boundary", "raw_parent_manifest", "recovery_map",
    "initial_target", "generation_ledger", "packed_block_ledger",
    "selected_proof", "full_D2_separator", "claims", "theorem_boundary",
    "provenance",
    "resource_guards", "partial", "input_errors", "performance"}

ALGORITHM_PUBLIC = {
    "name": "bounded-full-D2-dual-column-generation",
    "version": 2,
    "max_batches": 12,
    "max_translations_per_batch": 1024,
    "max_total_new_translation_blocks": 4096,
    "relators_per_block": 11,
    "max_total_new_relator_columns": 45056,
    "target_ordinal": 6,
    "variable_count": 108,
    "candidate_order": "fixed registered seed order 1..108",
    "batch_order": "canonical translation blob then relator 1..11",
    "first_consistent_stops": True,
    "targets_7_33_scanned": False,
    "monitor_registry": MONITOR_PUBLIC,
    "monitor_registry_sha256": MONITOR_SHA,
    "registered_monitor_pair_count": sum(map(len, MONITOR_REGISTRY.values())),
    "upstream_throw_sites": UPSTREAM_THROW_SITES_PUBLIC,
    "upstream_throw_sites_sha256": UPSTREAM_THROW_SITES_SHA,
    "registered_upstream_throw_site_count": sum(
        map(len, UPSTREAM_THROW_SITES.values())),
    "recovery_encoding": RECOVERY_ENCODING,
}

TERMINAL_REASONS = {
    "B345_E4_D2_COLGEN_TARGET6_CONSISTENT":
        "registered_108_target6_consistent_mod_generated_D2",
    "B345_E4_D2_COLGEN_TARGET6_FULL_D2_OBSTRUCTION":
        "complete_full_D2_correlation_zero",
    "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT":
        "authenticated_input_failure",
}

GENERATION_KEYS = {"generation", "basis", "target", "raw_lambda",
    "correlation", "preflight", "commit", "incremental", "classification"}
BASIS_ACCOUNTING_KEYS = {"columns", "pivots", "dependent",
    "live_sparse_entries", "pool_size", "pool_order_sha256", "DAG_nodes",
    "DAG_edges", "section_bindings", "section_expression_nodes",
    "section_expression_edges", "recovery"}
TARGET_PUBLIC_KEYS = {"generation", "variables", "equations", "rank",
    "nullity", "consistent", "row_space_sha256", "remainders_sha256",
    "live_remainder_entries", "complete_all_coordinates",
    "stopped_at_first_contradiction", "dual"}
DUAL_KEYS = {"normalization", "equations", "support_count",
    "support_sha256", "normalized_rhs", "yTz_mod3",
    "all_108_annihilation_sha256", "all_108_annihilation_dimension",
    "live_provenance_entries", "witness_provenance_entries",
    "peak_live_provenance_entries", "target_boundary",
    "target6_fixed_prefix_functional", "coordinate_encoding",
    "seed_manifest_sha256", "variables"}
DUAL_EQUATION_KEYS = {"label", "coefficient"}
DUAL_BOUNDARY_KEYS = {"first_target_ordinal", "last_target_ordinal",
    "target_ordinals"}
DUAL_ENCODING_KEYS = {"label", "component_numbering", "E4_blob",
    "permutation_width_bytes", "pc_width_bytes", "blob_width",
    "blob_hex_length", "endianness", "pivot_order"}
RECOVERY_PUBLIC_KEYS = {"encoding", "semantic_entry_count",
    "direct_parent_count", "raw_coordinate_parent_entry_count",
    "translated_parent_count", "candidate_edge_count",
    "translated_candidate_edge_count", "canonical_replacement_count",
    "canonical_sha256", "typed_arrays",
    "one_selected_parent_per_semantic_key",
    "all_candidate_dicts_or_roots_retained", "pool_IDs_public"}
RECOVERY_ARRAY_KEYS = {"kind", "component", "source", "offset",
    "relator", "term", "blob_width"}
RAW_LAMBDA_KEYS = {"algorithm", "support_count", "per_component",
    "packed_support_sha256", "packed_support_bytes", "pivot_count",
    "reverse_edge_visits", "pivot_annihilation_sha256",
    "dependent_event_count", "dependent_annihilation_sha256",
    "completed_block_column_count", "completed_block_annihilation_sha256",
    "delta_annihilation_sha256", "base_z_scalar", "negative_base_scalar",
    "normalized_dual_whole_sha256", "support_rows_not_serialized",
    "pool_IDs_or_old_qstar_used", "first_canary", "last_canary"}
CORRELATION_KEYS = {"complete", "generation", "pass1_pair_attempts",
    "pass2_pair_attempts", "pass2_selected_filter_count",
    "candidate_count_before_zero_deletion", "cancellation_to_zero_count",
    "active_row_count", "active_distinct_translation_count",
    "scalar_distribution", "active_packed_row_width",
    "active_packed_bytes", "active_packed_sha256",
    "selected_translation_count", "selected_truncated",
    "selected_translation_sha256", "selected_bindings_sha256",
    "selection_order", "first_active",
    "full_E4_enumerated", "pool_or_basis_mutated",
    "cumulative_pass1_pairs", "cumulative_pass2_pairs"}
PREFLIGHT_KEYS = {"generation", "translation_count", "column_count",
    "staged_sparse_entries", "all_selected_before_mutation",
    "all_eleven_before_mutation", "state_neutrality_before",
    "state_neutrality_after", "section_provenance", "row_binding_sha256"}
SECTION_PROVENANCE_KEYS = {"selected", "selected_count", "selected_sha256",
    "expression_DAG", "owned_inverse_materializer",
    "materialization_cadence", "all_values_exact"}
SECTION_SELECTED_KEYS = {"generation", "translation_ordinal",
    "translation_hex", "jstar", "correlation_scalar", "contributor", "g_recovery",
    "materialization_canary", "expression_root"}
CONTRIBUTOR_KEYS = {"component", "g_hex", "lambda_coefficient",
    "relator_index", "occurrence_ordinal", "h_hex", "base_coefficient",
    "translation_hex", "record_hex", "record_sha256"}
COMMIT_KEYS = {"generation", "complete", "translation_count",
    "column_count", "rank_gain", "dependent_gain", "pre_accounting",
    "post_accounting", "first_translation_jstar_pivot",
    "outcome_semantic_sha256", "all_blocks_complete",
    "all_staged_before_first_mutation"}
INCREMENTAL_KEYS = {"generation", "completed_new_pivot_ordinal",
    "completed_rows_in_current_pivot", "pre_update_remainder_sha256",
    "last_fully_updated_row_sha256", "current_new_pivot_prefix_sha256",
    "new_pivot_count", "reduction_order_sha256", "old_pivot_count",
    "old_pivot_set_encoding", "old_pivot_set_sha256",
    "completed_quotient_pivot_ordinal",
    "completed_quotient_prefix_sha256",
    "quotient_rows_discarded_on_failure", "live_entry_count",
    "batch_anchor_committed", "rolled_back_on_failure", "complete",
    "post_update_remainder_sha256", "fresh_direct_cadence"}
SELECTED_PROOF_KEYS = {"coefficient_vector", "coefficient_vector_sha256",
    "support", "factor_count", "typed_candidate", "target_expression",
    "direct_gradient", "direct_replay", "affine_prediction_equal",
    "D2_proof", "element_registry", "proof_root_node_id",
    "proof_expands_to_selected_gradient", "post_block_anchor_used",
    "targets_7_through_33_not_checked"}
SEPARATOR_KEYS = {"generation", "raw_lambda", "correlation",
    "active_row_count",
    "complete_76_occurrence_full_11_relator_correlation",
    "annihilates_full_D2", "lambda_delta_all_zero", "lambda_base_z",
    "registered_108_family_only", "pinned_E4_roof_only"}
PACKED_LEDGER_KEYS = {"format", "translation_encoding", "translation_count",
    "translation_decoded_bytes", "translation_sha256",
    "translation_base64_length", "translation_base64_sha256",
    "translation_base64", "record_encoding", "record_endianness",
    "record_bytes", "record_count", "decoded_bytes", "decoded_sha256",
    "base64_length", "base64_sha256", "base64",
    "flags_unused_high_nibble_zero", "JSON_column_objects_used"}
PACKED_PARTIAL_KEYS = {"format", "translation_count",
    "translation_decoded_bytes", "translation_sha256", "record_bytes",
    "record_count", "decoded_bytes", "decoded_sha256",
    "base64_omitted_for_resource_partial"}
PARTIAL_KEYS = {"phase", "reason", "current",
    "completed_generation_count", "completed_batch_count",
    "completed_new_translation_block_count", "current_generation",
    "packed_block_ledger_prefix", "selected_proof", "full_D2_separator"}
RESOURCE_KEYS = {"cap_reason", "cap_key", "cap_source", "cap_limit",
    "observed_count", "comparator", "phase", "detail", "inner_phase",
    "current"}
OUTER_PHASES = frozenset(MONITOR_REGISTRY)
SOURCE_PROGRESS_KEYS = {"current_seed", "evaluated_seeds",
    "records_prefix_sha256"}
FIXED_B1_PROGRESS_KEYS = {"attempted_relators", "completed_relators",
    "rank_gain_so_far", "block_prefix", "block_pre_accounting",
    "block_post_accounting", "current_relator", "substage", "raw_prefix",
    "shadow_prefix", "scalar_prefix", "raw_completed_relators",
    "shadow_completed_relators"}
INITIAL_TARGET_PROGRESS_KEYS = {"substage", "evaluated_seeds",
    "completed_equations", "current_seed", "typed_split_prefix",
    "remainder_prefix", "completed_target_system"}
BLOCK_PROGRESS_KEYS = {"generation", "selected_translation_count",
    "completed_translations", "attempted_translation",
    "completed_relators", "attempted_relator", "batch_anchor_committed",
    "unfinished_translation_rolled_back", "rollback_translation_ordinal",
    "completed_record_count", "pre_accounting",
    "completed_translation_prefix", "post_failure_accounting"}
INCREMENTAL_PROGRESS_KEYS = {"generation",
    "completed_new_pivot_ordinal", "completed_rows_in_current_pivot",
    "pre_update_remainder_sha256", "last_fully_updated_row_sha256",
    "current_new_pivot_prefix_sha256", "new_pivot_count",
    "reduction_order_sha256", "old_pivot_count",
    "old_pivot_set_encoding", "old_pivot_set_sha256",
    "completed_quotient_pivot_ordinal",
    "completed_quotient_prefix_sha256",
    "quotient_rows_discarded_on_failure", "live_entry_count",
    "batch_anchor_committed", "rolled_back_on_failure", "remaining_rows"}


def upstream_current_shape(current: dict[str, Any]) -> str:
    """Return the closed public progress-shape label for an upstream stop."""
    keys = set(current)
    if not keys:
        return "empty"
    if keys == SOURCE_PROGRESS_KEYS:
        return "source"
    if keys == FIXED_B1_PROGRESS_KEYS:
        return "fixed_block"
    if keys == {"lambda_ordinal", "base_component_ordinal"}:
        return "fixed_correlation_pair"
    if keys == {"post_accumulation"}:
        return "fixed_correlation_post"
    if keys == INITIAL_TARGET_PROGRESS_KEYS:
        return "initial_target"
    if keys == {"node"}:
        return "section_node"
    if keys == BLOCK_PROGRESS_KEYS:
        return "block"
    if keys == INCREMENTAL_PROGRESS_KEYS:
        return "incremental"
    if keys == {"generation", "completed_target"}:
        return "selected"
    raise RuntimeError("157em unknown upstream resource current shape")


def _sha256_text(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(
        character in "0123456789abcdef" for character in value)


_ZERO_VECTOR_SHA_CACHE: dict[int, str] = {}


def zero_vector_sha256(count: int) -> str:
    """Hash canonical JSON [0,...,0] without retaining a multi-million list."""
    require(type(count) is int and count >= 0,
            "157em zero-vector digest count")
    prior = _ZERO_VECTOR_SHA_CACHE.get(count)
    if prior is not None:
        return prior
    digest = hashlib.sha256()
    if count == 0:
        digest.update(b"[]")
    else:
        digest.update(b"[0")
        block = b",0"*8192
        full, remainder = divmod(count-1, 8192)
        for _ in range(full):
            digest.update(block)
        digest.update(b",0"*remainder); digest.update(b"]")
    answer = digest.hexdigest(); _ZERO_VECTOR_SHA_CACHE[count] = answer
    return answer


def validate_recovery_public(row: Any) -> None:
    require(isinstance(row, dict) and set(row) == RECOVERY_PUBLIC_KEYS and
            row["encoding"] == RECOVERY_ENCODING and
            isinstance(row["typed_arrays"], dict) and
            set(row["typed_arrays"]) == RECOVERY_ARRAY_KEYS and
            row["typed_arrays"]["blob_width"] == WIDTH and
            all(type(row[key]) is int and row[key] >= 0 for key in
                ("semantic_entry_count", "direct_parent_count",
                 "raw_coordinate_parent_entry_count", "translated_parent_count",
                 "candidate_edge_count", "translated_candidate_edge_count",
                 "canonical_replacement_count")) and
            row["semantic_entry_count"] == row["direct_parent_count"] +
                row["translated_parent_count"] and
            row["candidate_edge_count"] >= row["semantic_entry_count"] and
            row["translated_candidate_edge_count"] <= row["candidate_edge_count"] and
            _sha256_text(row["canonical_sha256"]) and
            row["one_selected_parent_per_semantic_key"] is True and
            row["all_candidate_dicts_or_roots_retained"] is False and
            row["pool_IDs_public"] is False,
            "157em exact recovery public ledger")


def validate_basis_accounting(row: Any, *, pool_digest: bool,
                              recovery: str) -> None:
    require(isinstance(row, dict) and set(row) == BASIS_ACCOUNTING_KEYS and
            all(type(row[key]) is int and row[key] >= 0 for key in
                ("columns", "pivots", "dependent", "live_sparse_entries",
                 "pool_size", "DAG_nodes", "DAG_edges", "section_bindings",
                 "section_expression_nodes", "section_expression_edges")) and
            row["pivots"] <= row["columns"] and
            row["dependent"] == row["columns"]-row["pivots"] and
            ((_sha256_text(row["pool_order_sha256"]) if pool_digest else
              row["pool_order_sha256"] is None)),
            "157em exact basis accounting")
    if recovery == "public":
        validate_recovery_public(row["recovery"])
    else:
        require(recovery == "none" and row["recovery"] is None,
                "157em basis accounting recovery boundary")


def validate_affine_dual(dual: Any, consistent: bool) -> None:
    if consistent:
        require(dual is None, "157em consistent target has no dual")
        return
    require(isinstance(dual, dict) and set(dual) == DUAL_KEYS and
            dual["normalization"] ==
                "first contradiction multiplied by inverse RHS" and
            dual["variables"] == 108 and dual["normalized_rhs"] == 1 and
            dual["yTz_mod3"] == 2 and
            dual["all_108_annihilation_dimension"] == 108 and
            dual["all_108_annihilation_sha256"] == zero_vector_sha256(108) and
            dual["target6_fixed_prefix_functional"] is True and
            isinstance(dual["target_boundary"], dict) and
            set(dual["target_boundary"]) == DUAL_BOUNDARY_KEYS and
            dual["target_boundary"] == {"first_target_ordinal": 6,
                "last_target_ordinal": 6, "target_ordinals": [6]} and
            isinstance(dual["coordinate_encoding"], dict) and
            set(dual["coordinate_encoding"]) == DUAL_ENCODING_KEYS and
            dual["coordinate_encoding"]["permutation_width_bytes"] == 144 and
            dual["coordinate_encoding"]["pc_width_bytes"] == 10 and
            dual["coordinate_encoding"]["blob_width"] == WIDTH and
            dual["coordinate_encoding"]["blob_hex_length"] == 2*WIDTH and
            dual["coordinate_encoding"]["pivot_order"] ==
                "component then exact E4 bytes" and
            dual["support_count"] == len(dual["equations"]) ==
                dual["witness_provenance_entries"] and
            dual["support_count"] <= 109 and
            dual["support_sha256"] == sha_obj(dual["equations"]) and
            _sha256_text(dual["seed_manifest_sha256"]),
            "157em exact inherited affine dual")
    prior_label: str | None = None
    for equation in dual["equations"]:
        require(isinstance(equation, dict) and set(equation) ==
                DUAL_EQUATION_KEYS and equation["coefficient"] in (1, 2) and
                isinstance(equation["label"], list) and
                len(equation["label"]) == 4 and
                equation["label"][0:2] == [6, "hexagon_1_coface_0"] and
                1 <= equation["label"][2] <= 6 and
                isinstance(equation["label"][3], str) and
                len(equation["label"][3]) == 2*WIDTH,
                "157em affine dual equation typing")
        label = json.dumps(equation["label"], sort_keys=True,
                           separators=(",", ":"))
        require(prior_label is None or prior_label < label,
                "157em affine dual canonical equation order")
        prior_label = label


def validate_raw_lambda(row: Any, target: dict[str, Any],
                        basis: dict[str, Any], completed_columns: int) -> None:
    require(isinstance(row, dict) and set(row) == RAW_LAMBDA_KEYS and
            row["algorithm"] == "general-reverse-canonical-pivot-DP/v1" and
            type(row["support_count"]) is int and
            1 <= row["support_count"] <= CAPS["raw_lambda_support_entries"] and
            isinstance(row["per_component"], list) and
            len(row["per_component"]) == 6 and
            all(type(value) is int and value >= 0 for value in
                row["per_component"]) and
            sum(row["per_component"]) == row["support_count"] and
            row["packed_support_bytes"] == row["support_count"]*156 and
            _sha256_text(row["packed_support_sha256"]) and
            row["pivot_count"] == basis["pivots"] and
            0 <= row["reverse_edge_visits"] <=
                CAPS["raw_lambda_reverse_edge_visits"] and
            row["pivot_annihilation_sha256"] ==
                zero_vector_sha256(row["pivot_count"]) and
            row["dependent_event_count"] == 16 and
            row["dependent_annihilation_sha256"] == zero_vector_sha256(16) and
            row["completed_block_column_count"] == completed_columns and
            row["completed_block_annihilation_sha256"] ==
                zero_vector_sha256(completed_columns) and
            row["delta_annihilation_sha256"] == zero_vector_sha256(108) and
            row["base_z_scalar"] == 2 and row["negative_base_scalar"] == 1 and
            row["normalized_dual_whole_sha256"] == sha_obj(target["dual"]) and
            row["support_rows_not_serialized"] is True and
            row["pool_IDs_or_old_qstar_used"] is False and
            ((row["support_count"] == 0 and row["first_canary"] is None and
              row["last_canary"] is None) or
             (row["support_count"] > 0 and
              all(isinstance(canary, list) and len(canary) == 3 and
                  1 <= canary[0] <= 6 and isinstance(canary[1], str) and
                  len(canary[1]) == 2*WIDTH and canary[2] in (1, 2)
                  for canary in (row["first_canary"], row["last_canary"])))),
            "157em exact raw-lambda public ledger")


def validate_correlation_public(row: Any, generation: int,
                                prior_pass1: int, prior_pass2: int,
                                lambda_per_component: Sequence[int]) \
        -> tuple[int, int]:
    require(isinstance(row, dict) and set(row) == CORRELATION_KEYS and
            row["complete"] is True and row["generation"] == generation and
            all(type(row[key]) is int and row[key] >= 0 for key in
                ("pass1_pair_attempts", "pass2_pair_attempts",
                 "pass2_selected_filter_count",
                 "candidate_count_before_zero_deletion",
                 "cancellation_to_zero_count", "active_row_count",
                 "active_distinct_translation_count", "active_packed_bytes",
                 "selected_translation_count", "cumulative_pass1_pairs",
                 "cumulative_pass2_pairs")) and
            isinstance(row["scalar_distribution"], dict) and
            set(row["scalar_distribution"]) == {"1", "2"} and
            all(type(value) is int and value >= 0 for value in
                row["scalar_distribution"].values()) and
            sum(row["scalar_distribution"].values()) == row["active_row_count"] and
            row["candidate_count_before_zero_deletion"] ==
                row["active_row_count"]+row["cancellation_to_zero_count"] and
            row["active_distinct_translation_count"] <= row["active_row_count"] and
            row["selected_translation_count"] <= min(
                row["active_distinct_translation_count"],
                CAPS["translations_per_batch"]) and
            row["active_packed_row_width"] == 156 and
            row["active_packed_bytes"] == 156*row["active_row_count"] and
            _sha256_text(row["active_packed_sha256"]) and
            _sha256_text(row["selected_translation_sha256"]) and
            _sha256_text(row["selected_bindings_sha256"]) and
            row["selected_truncated"] == (row["selected_translation_count"] <
                row["active_distinct_translation_count"]) and
            row["selection_order"] ==
                "exact 154-byte translation blob lexicographic" and
            row["full_E4_enumerated"] is False and
            row["pool_or_basis_mutated"] is False and
            row["cumulative_pass1_pairs"] ==
                prior_pass1+row["pass1_pair_attempts"] and
            row["cumulative_pass2_pairs"] ==
                prior_pass2+row["pass2_pair_attempts"] and
            row["pass2_selected_filter_count"] <= row["pass2_pair_attempts"] and
            list(lambda_per_component) and len(lambda_per_component) == 6 and
            row["pass1_pair_attempts"] == sum(value*count for value, count in
                zip(lambda_per_component, [10, 12, 18, 10, 12, 14])) and
            row["pass2_pair_attempts"] == (row["pass1_pair_attempts"] if
                row["selected_translation_count"] > 0 else 0) and
            ((row["active_row_count"] == 0 and row["first_active"] is None and
              row["selected_translation_count"] == 0 and
              row["pass2_pair_attempts"] == 0) or
             (row["active_row_count"] > 0 and
              isinstance(row["first_active"], dict) and
              set(row["first_active"]) ==
                  {"translation_hex", "relator_index", "scalar"} and
              len(row["first_active"]["translation_hex"]) == 2*WIDTH and
              1 <= row["first_active"]["relator_index"] <= 11 and
              row["first_active"]["scalar"] in (1, 2))),
            "157em exact correlation public ledger")
    return row["cumulative_pass1_pairs"], row["cumulative_pass2_pairs"]


def validate_section_provenance(row: Any, generation: int,
                                translations: int) -> None:
    require(isinstance(row, dict) and set(row) == SECTION_PROVENANCE_KEYS and
            row["selected_count"] == len(row["selected"]) == translations and
            row["selected_sha256"] == sha_obj(row["selected"]) and
            isinstance(row["expression_DAG"], dict) and
            row["owned_inverse_materializer"] is True and
            row["materialization_cadence"] ==
                "first,last,and-every-64th" and row["all_values_exact"] is True,
            "157em exact selected section provenance")
    expression_nodes = validate_section_expression_payload(
        row["expression_DAG"])
    prior_blob: bytes | None = None
    for ordinal, selected in enumerate(row["selected"], 1):
        require(isinstance(selected, dict) and
                set(selected) == SECTION_SELECTED_KEYS and
                selected["generation"] == generation and
                selected["translation_ordinal"] == ordinal and
                isinstance(selected["translation_hex"], str) and
                len(selected["translation_hex"]) == 2*WIDTH and
                1 <= selected["jstar"] <= 11 and
                selected["correlation_scalar"] in (1, 2) and
                isinstance(selected["expression_root"], int) and
                0 <= selected["expression_root"] < expression_nodes and
                isinstance(selected["g_recovery"], dict) and
                isinstance(selected["contributor"], dict) and
                set(selected["contributor"]) == CONTRIBUTOR_KEYS and
                selected["contributor"]["translation_hex"] ==
                    selected["translation_hex"] and
                selected["contributor"]["relator_index"] == selected["jstar"],
                "157em selected section row binding")
        contributor = selected["contributor"]
        g_blob = bytes.fromhex(contributor["g_hex"])
        h_blob = bytes.fromhex(contributor["h_hex"])
        record = bytes([contributor["component"]]) + g_blob + \
            bytes([contributor["lambda_coefficient"],
                   contributor["relator_index"]]) + \
            struct.pack(">H", contributor["occurrence_ordinal"]) + h_blob + \
            bytes([contributor["base_coefficient"]])
        require(1 <= contributor["component"] <= 6 and
                len(g_blob) == len(h_blob) == WIDTH and
                contributor["lambda_coefficient"] in (1, 2) and
                contributor["base_coefficient"] in (1, 2) and
                contributor["lambda_coefficient"]*
                    contributor["base_coefficient"] % 3 in (1, 2) and
                1 <= contributor["occurrence_ordinal"] <= 76 and
                contributor["record_hex"] == record.hex() and
                contributor["record_sha256"] == sha_bytes(record),
                "157em canonical contributor record")
        recovery = selected["g_recovery"]
        common_recovery = {"kind", "component", "element_hex", "method",
                           "word_length", "word_sha256"}
        recovery_keys = {
            "direct_target_source_prefix": common_recovery |
                {"source_word_ordinal", "signed_letter_offset"},
            "direct_base_support_prefix": common_recovery |
                {"relator_index", "term_ordinal"},
            "registered_translation_times_base_prefix": common_recovery |
                {"translation_hex", "relator_index", "term_ordinal",
                 "parent_hex"},
        }
        require(recovery.get("kind") in recovery_keys and
                set(recovery) == recovery_keys[recovery["kind"]] and
                recovery["component"] == contributor["component"] and
                recovery["element_hex"] == contributor["g_hex"] and
                type(recovery["word_length"]) is int and
                0 <= recovery["word_length"] <= SELECTED_SECTION_WORD_CAP and
                _sha256_text(recovery["word_sha256"]),
                "157em exact selected recovery descriptor")
        if recovery["kind"] == "direct_target_source_prefix":
            require(0 <= recovery["source_word_ordinal"] < 109 and
                    type(recovery["signed_letter_offset"]) is int and
                    recovery["signed_letter_offset"] >= 1 and
                    recovery["method"] == "target_word_signed_prefix",
                    "157em direct target recovery descriptor")
        elif recovery["kind"] == "direct_base_support_prefix":
            require(1 <= recovery["relator_index"] <= 11 and
                    1 <= recovery["term_ordinal"] <= 76 and
                    recovery["method"] ==
                        "base_D2_canonical_support_prefix",
                    "157em direct base recovery descriptor")
        else:
            require(len(recovery["translation_hex"]) == 2*WIDTH and
                    len(recovery["parent_hex"]) == 2*WIDTH and
                    1 <= recovery["relator_index"] <= 11 and
                    1 <= recovery["term_ordinal"] <= 76 and
                    recovery["method"] ==
                        "registered_u_times_base_prefix",
                    "157em translated recovery descriptor")
        blob = bytes.fromhex(selected["translation_hex"])
        require(prior_blob is None or prior_blob < blob,
                "157em selected section canonical translation order")
        prior_blob = blob
        canary_expected = ordinal == 1 or ordinal == translations or \
            ordinal % 64 == 0
        canary = selected["materialization_canary"]
        require((isinstance(canary, dict)) == canary_expected and
                (not canary_expected or
                 set(canary) == {"word_length", "word_sha256", "value_hex"}
                 and type(canary["word_length"]) is int and
                 0 <= canary["word_length"] <= SELECTED_SECTION_WORD_CAP and
                 _sha256_text(canary["word_sha256"]) and
                 canary["value_hex"] == selected["translation_hex"]),
                "157em selected materialization cadence")
    require(row["expression_DAG"]["roots"] ==
                [selected["expression_root"] for selected in row["selected"]],
            "157em section-expression selected root order")


def validate_preflight(row: Any, generation: int,
                       correlation: dict[str, Any]) -> None:
    require(isinstance(row, dict) and set(row) == PREFLIGHT_KEYS and
            row["generation"] == generation and
            type(row["translation_count"]) is int and
            1 <= row["translation_count"] <= CAPS["translations_per_batch"] and
            row["column_count"] == 11*row["translation_count"] and
            0 <= row["staged_sparse_entries"] <=
                CAPS["batch_staged_sparse_entries"] and
            row["all_selected_before_mutation"] is True and
            row["all_eleven_before_mutation"] is True and
            row["state_neutrality_before"] == row["state_neutrality_after"] and
            _sha256_text(row["row_binding_sha256"]),
            "157em exact batch preflight ledger")
    validate_basis_accounting(row["state_neutrality_before"],
                              pool_digest=True, recovery="none")
    validate_section_provenance(row["section_provenance"], generation,
                                row["translation_count"])
    selected = row["section_provenance"]["selected"]
    bindings = [[item["translation_hex"], item["jstar"],
                 item["correlation_scalar"]] for item in selected]
    require(row["translation_count"] ==
                correlation["selected_translation_count"] and
            sha_bytes(b"".join(bytes.fromhex(item["translation_hex"])
                               for item in selected)) ==
                correlation["selected_translation_sha256"] and
            sha_obj(bindings) == correlation["selected_bindings_sha256"] and
            (not selected or
             selected[0]["translation_hex"] ==
                correlation["first_active"]["translation_hex"] and
             selected[0]["jstar"] ==
                correlation["first_active"]["relator_index"] and
             selected[0]["correlation_scalar"] ==
                correlation["first_active"]["scalar"]),
            "157em correlation/preflight selected bundle binding")


def validate_commit(row: Any, generation: int,
                    preflight: dict[str, Any], *,
                    expected_recovery_edges_per_translation: int = 76) -> None:
    require(type(expected_recovery_edges_per_translation) is int and
            expected_recovery_edges_per_translation > 0,
            "157em commit recovery-edge fixture binding")
    require(isinstance(row, dict) and set(row) == COMMIT_KEYS and
            row["generation"] == generation and row["complete"] is True and
            row["translation_count"] == preflight["translation_count"] and
            row["column_count"] == 11*row["translation_count"] and
            row["rank_gain"]+row["dependent_gain"] == row["column_count"] and
            row["all_blocks_complete"] is True and
            row["all_staged_before_first_mutation"] is True and
            _sha256_text(row["outcome_semantic_sha256"]),
            "157em exact committed batch ledger")
    validate_basis_accounting(row["pre_accounting"], pool_digest=True,
                              recovery="public")
    validate_basis_accounting(row["post_accounting"], pool_digest=True,
                              recovery="public")
    pre, post = row["pre_accounting"], row["post_accounting"]
    first = preflight["section_provenance"]["selected"][0]
    pivot = row["first_translation_jstar_pivot"]["pivot"]
    require(post["columns"]-pre["columns"] == row["column_count"] and
            post["pivots"]-pre["pivots"] == row["rank_gain"] and
            post["dependent"]-pre["dependent"] == row["dependent_gain"] and
            post["recovery"]["translated_candidate_edge_count"]-
                pre["recovery"]["translated_candidate_edge_count"] ==
                expected_recovery_edges_per_translation*
                    row["translation_count"] and
            isinstance(row["first_translation_jstar_pivot"], dict) and
            set(row["first_translation_jstar_pivot"]) ==
                {"translation_ordinal", "relator", "scalar", "pivot"} and
            row["first_translation_jstar_pivot"]["translation_ordinal"] == 1 and
            row["first_translation_jstar_pivot"]["scalar"] ==
                first["correlation_scalar"] and
            row["first_translation_jstar_pivot"]["relator"] ==
                first["jstar"] and
            isinstance(pivot, list) and len(pivot) == 2 and
            type(pivot[0]) is int and 1 <= pivot[0] <= 6 and
            isinstance(pivot[1], str) and len(pivot[1]) == 2*WIDTH and
            all(post[key] >= pre[key] for key in
                ("pool_size", "DAG_nodes", "DAG_edges", "section_bindings",
                 "section_expression_nodes", "section_expression_edges")),
            "157em commit accounting/recovery/jstar binding")


def validate_incremental(row: Any, generation: int,
                         commit: dict[str, Any]) -> None:
    require(isinstance(row, dict) and set(row) == INCREMENTAL_KEYS and
            row["generation"] == generation and row["complete"] is True and
            row["new_pivot_count"] == row["completed_new_pivot_ordinal"] ==
                row["completed_quotient_pivot_ordinal"] == commit["rank_gain"] and
            row["completed_rows_in_current_pivot"] == 0 and
            row["old_pivot_count"] == commit["pre_accounting"]["pivots"] and
            row["old_pivot_set_encoding"] ==
                "domain:d972-157em-semantic-pivot-set-v1\\0|count:u32be|"
                "repeated(component:u8,blob:154)" and
            all(_sha256_text(row[key]) for key in
                ("pre_update_remainder_sha256",
                 "current_new_pivot_prefix_sha256", "reduction_order_sha256",
                 "old_pivot_set_sha256", "completed_quotient_prefix_sha256",
                 "post_update_remainder_sha256")) and
            row["quotient_rows_discarded_on_failure"] is False and
            row["batch_anchor_committed"] is True and
            row["rolled_back_on_failure"] is False and
            0 <= row["live_entry_count"] <= CAPS["target_live_remainders"] and
            _sha256_text(row["last_fully_updated_row_sha256"]) and
            isinstance(row["fresh_direct_cadence"], list) and
            [item.get("ordinal") for item in row["fresh_direct_cadence"]] ==
                [0, 1, 54, 108] and
            all(set(item) == {"ordinal", "sha256", "equal"} and
                _sha256_text(item["sha256"]) and item["equal"] is True
                for item in row["fresh_direct_cadence"]),
            "157em exact incremental quotient/remainder ledger")


PACKED_ARRAY_KEYS = {"type", "array_typecode", "endianness", "length",
    "itemsize", "byte_length", "cap", "sha256", "base64"}
SELECTED_WORDEXPR_NODE_CAP = 262_144
SELECTED_WORDEXPR_EDGE_CAP = 1_048_576
SELECTED_WORDEXPR_FLAT_CAP = 16_384
SELECTED_WORDEXPR_EXPANDED_CAP = 4_194_304
SELECTED_SECTION_NODE_CAP = 131_072
SELECTED_SECTION_EDGE_CAP = 262_144
SELECTED_SECTION_WORD_CAP = 100_000
SELECTED_PROOF_NODE_CAP = 2_000_000
SELECTED_PROOF_EDGE_CAP = 4_000_000


def decode_packed_array_block(block: Any, expected_type: str,
                              typecode: str, cap: int) -> Sequence[int]:
    require(isinstance(block, dict) and set(block) == PACKED_ARRAY_KEYS and
            block["type"] == expected_type and
            block["array_typecode"] == typecode and
            block["endianness"] == "little" and block["cap"] == cap and
            type(block["length"]) is int and 0 <= block["length"] <= cap and
            type(block["itemsize"]) is int and
            type(block["byte_length"]) is int and
            isinstance(block["base64"], str) and
            _sha256_text(block["sha256"]),
            "157em packed selected-proof array schema")
    raw = base64.b64decode(block["base64"], validate=True)
    require(base64.b64encode(raw).decode("ascii") == block["base64"] and
            sha_bytes(raw) == block["sha256"] and
            block["byte_length"] == len(raw),
            "157em packed selected-proof array bytes")
    if typecode == "B":
        require(block["itemsize"] == 1 and len(raw) == block["length"],
                "157em packed uint8 length")
        return raw
    values = array(typecode)
    require(block["itemsize"] == values.itemsize and
            len(raw) == block["length"]*values.itemsize,
            "157em packed integer length")
    values.frombytes(raw)
    if sys.byteorder != "little":
        values.byteswap()
    return values


def validate_wordexpr_payload(block: Any, expected_roots: Sequence[str]) \
        -> None:
    keys = {"format", "node_order", "nodes", "roots", "node_count",
        "edge_count", "ordinary_product", "free_reduction_semantic_bridge",
        "manifest_sha256"}
    require(isinstance(block, dict) and set(block) == keys and
            block["format"] == "typed-wordexpr-dag/v1" and
            block["node_order"] == "one_based_topological" and
            block["ordinary_product"] is True and
            isinstance(block["nodes"], list) and
            isinstance(block["roots"], list) and
            block["node_count"] == len(block["nodes"]) and
            1 <= block["node_count"] <= SELECTED_WORDEXPR_NODE_CAP and
            block["edge_count"] == sum(len(node.get("children", []))
                                       for node in block["nodes"]) and
            0 <= block["edge_count"] <= SELECTED_WORDEXPR_EDGE_CAP and
            block["free_reduction_semantic_bridge"] ==
                "recursive expansion then free reduction equals the literal "
                "word; D(xx^-1)=0" and
            block["manifest_sha256"] == sha_obj({"nodes": block["nodes"],
                                                  "roots": block["roots"]}),
            "157em typed WordExpr payload header")
    allowed = {"IDENTITY", "FLAT_WORD", "PRODUCT", "INVERSE",
               "SUBSTITUTE_WORD"}
    expanded: list[int] = []
    ranks: list[int] = []
    for node_id, node in enumerate(block["nodes"], 1):
        require(isinstance(node, dict) and set(node) == {"node_id", "opcode",
                "rank", "flat_word", "children", "expanded_letter_count"} and
                node["node_id"] == node_id and node["opcode"] in allowed and
                type(node["rank"]) is int and node["rank"] > 0 and
                isinstance(node["flat_word"], list) and
                isinstance(node["children"], list) and
                all(type(child) is int and 1 <= child < node_id
                    for child in node["children"]) and
                type(node["expanded_letter_count"]) is int and
                node["expanded_letter_count"] >= 0,
                "157em typed WordExpr node")
        opcode, word, children = (node[key] for key in
                                  ("opcode", "flat_word", "children"))
        rank = node["rank"]
        require(
            (opcode == "IDENTITY" and not word and not children and
             node["expanded_letter_count"] == 0) or
            (opcode == "FLAT_WORD" and not children and
             len(word) <= SELECTED_SECTION_WORD_CAP and
             all(type(letter) is int and 1 <= abs(letter) <= rank
                 for letter in word) and
             node["expanded_letter_count"] == len(word)) or
            (opcode == "PRODUCT" and not word and len(children) == 2 and
             all(ranks[child-1] == rank for child in children) and
             node["expanded_letter_count"] ==
                sum(expanded[child-1] for child in children)) or
            (opcode == "INVERSE" and not word and len(children) == 1 and
             ranks[children[0]-1] == rank and
             node["expanded_letter_count"] == expanded[children[0]-1]) or
            (opcode == "SUBSTITUTE_WORD" and children and
             all(ranks[child-1] == rank for child in children) and
             all(type(letter) is int and
                 1 <= abs(letter) <= len(children) for letter in word) and
             node["expanded_letter_count"] == sum(
                 expanded[children[abs(letter)-1]-1] for letter in word)),
            "157em typed WordExpr opcode/rank/count")
        ranks.append(rank); expanded.append(node["expanded_letter_count"])
    require([root.get("name") for root in block["roots"]] ==
                list(expected_roots) and
            all(isinstance(root, dict) and set(root) == {"name", "node_id"} and
                type(root["node_id"]) is int and
                1 <= root["node_id"] <= block["node_count"]
                for root in block["roots"]),
            "157em typed WordExpr roots")
    require(sum(node["opcode"] == "FLAT_WORD" for node in block["nodes"])
                <= SELECTED_WORDEXPR_FLAT_CAP and
            all(expanded[root["node_id"]-1] <=
                SELECTED_WORDEXPR_EXPANDED_CAP for root in block["roots"]),
            "157em typed WordExpr frozen caps")
    reached: set[int] = set(); pending = [root["node_id"]
                                         for root in block["roots"]]
    while pending:
        node = pending.pop()
        if node in reached:
            continue
        reached.add(node); pending.extend(block["nodes"][node-1]["children"])
    require(len(reached) == block["node_count"],
            "157em typed WordExpr unreachable node")


def validate_section_expression_payload(block: Any) -> int:
    keys = {"format", "node_order", "ordinary_word_composition",
        "canonical_value_width", "node_count", "edge_count", "roots",
        "arrays", "manifest_sha256"}
    require(isinstance(block, dict) and set(block) == keys and
            block["format"] == "typed-section-expression-arrays/v1" and
            block["node_order"] == "zero_based_topological" and
            block["ordinary_word_composition"] is True and
            block["canonical_value_width"] == WIDTH and
            type(block["node_count"]) is int and
            0 <= block["node_count"] <= SELECTED_SECTION_NODE_CAP and
            type(block["edge_count"]) is int and
            0 <= block["edge_count"] <= SELECTED_SECTION_EDGE_CAP and
            isinstance(block["roots"], list),
            "157em section-expression payload header")
    n = block["node_count"]
    if n == 0:
        require(block["arrays"] == {} and block["roots"] == [] and
                block["edge_count"] == 0 and block["manifest_sha256"] ==
                    sha_obj({"arrays": {}, "roots": []}),
                "157em empty section-expression payload")
        return 0
    arrays = block["arrays"]
    require(set(arrays) == {"kind", "signed_generator", "left", "right",
            "flat_offsets", "flat_letters", "canonical_values"},
            "157em section-expression arrays")
    kinds = decode_packed_array_block(arrays["kind"], "uint8", "B",
                                      SELECTED_SECTION_NODE_CAP)
    signed = decode_packed_array_block(
        arrays["signed_generator"], "int8", "b", SELECTED_SECTION_NODE_CAP)
    left = decode_packed_array_block(
        arrays["left"], "uint32", "I", SELECTED_SECTION_NODE_CAP)
    right = decode_packed_array_block(
        arrays["right"], "uint32", "I", SELECTED_SECTION_NODE_CAP)
    offsets = decode_packed_array_block(
        arrays["flat_offsets"], "uint32", "I", SELECTED_SECTION_NODE_CAP+1)
    letters = decode_packed_array_block(
        arrays["flat_letters"], "int16", "h",
        SELECTED_SECTION_NODE_CAP*SELECTED_SECTION_WORD_CAP)
    values = decode_packed_array_block(
        arrays["canonical_values"], "uint8", "B",
        SELECTED_SECTION_NODE_CAP*WIDTH)
    require(len(kinds) == len(signed) == len(left) == len(right) == n and
            len(offsets) == n+1 and offsets[0] == 0 and
            offsets[-1] == len(letters) and len(values) == n*WIDTH and
            all(offsets[index] <= offsets[index+1]
                for index in range(n)) and
            sum(1 if kind == 3 else 2 if kind == 2 else 0
                for kind in kinds) == block["edge_count"] and
            all(
                (kind == 0 and signed[index] == 0 and
                 left[index] == right[index] == 0 and
                 offsets[index] == offsets[index+1]) or
                (kind == 1 and 1 <= abs(int(signed[index])) <= 6 and
                 left[index] == right[index] == 0 and
                 offsets[index] == offsets[index+1]) or
                (kind == 4 and signed[index] == 0 and
                 left[index] == right[index] == 0 and
                 offsets[index+1]-offsets[index] <=
                    SELECTED_SECTION_WORD_CAP and
                 all(1 <= abs(int(letter)) <= 6 for letter in
                     letters[offsets[index]:offsets[index+1]])) or
                (kind == 3 and signed[index] == 0 and
                 left[index] < index and right[index] == 0 and
                 offsets[index] == offsets[index+1]) or
                (kind == 2 and signed[index] == 0 and
                 left[index] < index and right[index] < index and
                 offsets[index] == offsets[index+1])
                for index, kind in enumerate(kinds)),
            "157em section-expression topology")
    manifest = {name: {key: value for key, value in item.items()
                       if key != "base64"} for name, item in arrays.items()}
    require(block["manifest_sha256"] == sha_obj(
                {"arrays": manifest, "roots": block["roots"]}) and
            len(set(block["roots"])) == len(block["roots"]) and
            all(type(root) is int and 0 <= root < n for root in block["roots"]),
            "157em section-expression manifest/roots")
    reached: set[int] = set(); pending = list(block["roots"])
    while pending:
        node = pending.pop()
        if node in reached:
            continue
        reached.add(node)
        if kinds[node] == 3:
            pending.append(int(left[node]))
        elif kinds[node] == 2:
            pending.extend((int(left[node]), int(right[node])))
    require(len(reached) == n,
            "157em section-expression unreachable node")
    return n


def validate_selected_registry(rows: Any, expression_nodes: int) \
        -> tuple[set[int], set[int]]:
    require(isinstance(rows, list), "157em selected element registry list")
    ids: set[int] = set(); semantic: set[tuple[Any, ...]] = set()
    expression_roots: set[int] = set()
    for expected, row in enumerate(rows, 1):
        flat = isinstance(row, dict) and "section_word" in row
        keys = ({"id", "rank", "section_word", "coarse_permutation",
                 "fine_pc_coords"} if flat else
                {"id", "rank", "section_expression_root",
                 "coarse_permutation", "fine_pc_coords"})
        require(isinstance(row, dict) and set(row) == keys and
                row["id"] == expected and row["rank"] == 4 and
                isinstance(row["coarse_permutation"], list) and
                sorted(row["coarse_permutation"]) == list(range(1, 145)) and
                isinstance(row["fine_pc_coords"], list) and
                len(row["fine_pc_coords"]) == 10 and
                all(type(value) is int and 0 <= value < 3
                    for value in row["fine_pc_coords"]) and
                ((flat and isinstance(row["section_word"], list) and
                  len(row["section_word"]) <= SELECTED_SECTION_WORD_CAP and
                  all(type(letter) is int and 1 <= abs(letter) <= 6
                      for letter in row["section_word"])) or
                 (not flat and type(row["section_expression_root"]) is int and
                  0 <= row["section_expression_root"] < expression_nodes)),
                "157em selected element registry row")
        key = (tuple(row["coarse_permutation"]),
               tuple(row["fine_pc_coords"]))
        require(key not in semantic, "157em selected registry duplicate value")
        semantic.add(key); ids.add(expected)
        if not flat:
            expression_roots.add(row["section_expression_root"])
    return ids, expression_roots


def validate_selected_d2_proof(proof: Any, registry: Any,
                               claimed_root: int) -> None:
    keys = {"format", "field", "node_order", "translation_action",
        "section_expressions", "arrays", "roots", "node_count", "edge_count",
        "leaf_count", "combination_node_count",
        "all_serialized_nodes_reachable_from_roots",
        "unreachable_search_nodes_pruned",
        "expanded_boundary_ledgers_serialized", "packed_manifest_sha256"}
    require(isinstance(proof, dict) and set(proof) == keys and
            proof["format"] == "packed-parallel-arrays/v1" and
            proof["field"] == 3 and
            proof["node_order"] == "one_based_topological" and
            proof["translation_action"] == "left" and
            type(proof["node_count"]) is int and
            1 <= proof["node_count"] <= SELECTED_PROOF_NODE_CAP and
            type(proof["edge_count"]) is int and
            0 <= proof["edge_count"] <= SELECTED_PROOF_EDGE_CAP and
            proof["all_serialized_nodes_reachable_from_roots"] is True and
            proof["expanded_boundary_ledgers_serialized"] is False and
            type(proof["unreachable_search_nodes_pruned"]) is int and
            proof["unreachable_search_nodes_pruned"] >= 0,
            "157em selected D2 proof header")
    expression_nodes = validate_section_expression_payload(
        proof["section_expressions"])
    registry_ids, registry_expression_roots = validate_selected_registry(
        registry, expression_nodes)
    require(set(proof["section_expressions"]["roots"]) ==
                registry_expression_roots,
            "157em selected registry/section-expression roots")
    arrays = proof["arrays"]
    require(set(arrays) == {"node_kind", "leaf_relator_index",
        "leaf_translation_element_id", "edge_offsets", "edge_parent_node_id",
        "edge_coefficient"}, "157em selected D2 proof arrays")
    kinds = decode_packed_array_block(
        arrays["node_kind"], "uint8", "B", SELECTED_PROOF_NODE_CAP)
    relators = decode_packed_array_block(
        arrays["leaf_relator_index"], "uint16", "H", SELECTED_PROOF_NODE_CAP)
    translations = decode_packed_array_block(
        arrays["leaf_translation_element_id"], "uint32", "I",
        SELECTED_PROOF_NODE_CAP)
    offsets = decode_packed_array_block(
        arrays["edge_offsets"], "uint32", "I", SELECTED_PROOF_NODE_CAP+1)
    parents = decode_packed_array_block(
        arrays["edge_parent_node_id"], "uint32", "I",
        SELECTED_PROOF_EDGE_CAP)
    coefficients = decode_packed_array_block(
        arrays["edge_coefficient"], "uint8", "B",
        SELECTED_PROOF_EDGE_CAP)
    n, e = proof["node_count"], proof["edge_count"]
    require(len(kinds) == len(relators) == len(translations) == n and
            len(offsets) == n+1 and offsets[0] == 0 and offsets[-1] == e and
            len(parents) == len(coefficients) == e and
            all(offsets[index] <= offsets[index+1]
                for index in range(n)), "157em selected D2 proof dimensions")
    leaf_count = 0
    used_registry_ids: set[int] = set()
    for index, kind in enumerate(kinds):
        start, stop = int(offsets[index]), int(offsets[index+1])
        if kind == 1:
            require(start == stop and 1 <= relators[index] <= 11 and
                    translations[index] in registry_ids,
                    "157em selected D2 leaf")
            leaf_count += 1
            used_registry_ids.add(int(translations[index]))
        else:
            require(kind == 2 and relators[index] == translations[index] == 0 and
                    (stop > start or index == 0) and
                    len(set(int(parents[position]) for position in
                            range(start, stop))) == stop-start and
                    all(int(parents[position]) < int(parents[position+1])
                        for position in range(start, stop-1)) and
                    all(1 <= parents[position] < index+1 and
                        coefficients[position] in (1, 2)
                        for position in range(start, stop)),
                    "157em selected D2 linear node")
    roots = proof["roots"]
    require(roots == [{"name": "hexagon_1_coface_0",
                       "node_id": claimed_root}] and
            1 <= claimed_root <= n and proof["leaf_count"] == leaf_count and
            proof["combination_node_count"] == n-leaf_count and
            used_registry_ids == registry_ids,
            "157em selected D2 root/accounting")
    reached: set[int] = set(); pending = [claimed_root]
    while pending:
        node = pending.pop()
        if node in reached:
            continue
        reached.add(node)
        pending.extend(int(parents[position]) for position in
            range(int(offsets[node-1]), int(offsets[node])))
    manifest = {name: {key: value for key, value in item.items()
                       if key != "base64"} for name, item in arrays.items()}
    require(len(reached) == n and proof["packed_manifest_sha256"] ==
            sha_obj({"arrays": manifest, "roots": roots}),
            "157em selected D2 reachable manifest")


def validate_selected_proof(row: Any) -> None:
    require(isinstance(row, dict) and set(row) == SELECTED_PROOF_KEYS and
            isinstance(row["coefficient_vector"], list) and
            len(row["coefficient_vector"]) == 108 and
            all(value in (0, 1, 2) for value in row["coefficient_vector"]) and
            row["coefficient_vector_sha256"] ==
                sha_obj(row["coefficient_vector"]) and
            row["support"] == [index+1 for index, coefficient in
                enumerate(row["coefficient_vector"]) if coefficient] and
            row["factor_count"] == sum(row["coefficient_vector"]) and
            all(isinstance(row[key], dict) and row[key] for key in
                ("typed_candidate", "target_expression", "direct_gradient",
                 "D2_proof")) and isinstance(row["element_registry"], list) and
            type(row["proof_root_node_id"]) is int and
            row["proof_root_node_id"] >= 0 and
            all(row[key] is True for key in ("direct_replay",
                "affine_prediction_equal", "proof_expands_to_selected_gradient",
                "post_block_anchor_used", "targets_7_through_33_not_checked")),
            "157em exact selected-proof public ledger")
    typed = row["typed_candidate"]
    typed_keys = {"f0_root", "correction_root", "candidate_root",
        "coefficient_vector", "nonzero_support", "expanded_count",
        "correction_word", "correction_word_flattened",
        "correction_expanded_count", "typed_product_order",
        "exponent_two_is_two_copies", "correction_word_sha256",
        "coefficient_vector_sha256", "expression", "expression_root_names"}
    require(set(typed) == typed_keys and
            typed["coefficient_vector"] == row["coefficient_vector"] and
            typed["coefficient_vector_sha256"] ==
                row["coefficient_vector_sha256"] and
            typed["nonzero_support"] == row["support"] and
            type(typed["f0_root"]) is int and typed["f0_root"] >= 1 and
            type(typed["correction_root"]) is int and
                typed["correction_root"] >= 1 and
            type(typed["candidate_root"]) is int and
                typed["candidate_root"] >= 1 and
            type(typed["expanded_count"]) is int and
                typed["expanded_count"] >= 0 and
            type(typed["correction_expanded_count"]) is int and
                typed["correction_expanded_count"] >= 0 and
            isinstance(typed["correction_word_flattened"], bool) and
            ((typed["correction_word_flattened"] is True and
              isinstance(typed["correction_word"], list) and
              len(typed["correction_word"]) <= SELECTED_SECTION_WORD_CAP and
              all(type(letter) is int and 1 <= abs(letter) <= 2
                  for letter in typed["correction_word"])) or
             (typed["correction_word_flattened"] is False and
              typed["correction_word"] is None)) and
            typed["correction_word_sha256"] == sha_obj(
                typed["correction_word"] if typed["correction_word"] is not None
                else {"typed_product_order": typed["typed_product_order"],
                      "coefficient_vector": typed["coefficient_vector"]}) and
            typed["typed_product_order"] ==
                "seed_1^a1 * ... * seed_108^a108" and
            typed["exponent_two_is_two_copies"] is True and
            typed["expression_root_names"] ==
                ["f0_root", "correction_root", "candidate_root"],
            "157em selected typed-candidate exact contract")
    validate_wordexpr_payload(typed["expression"],
        ["f0_root", "correction_root", "candidate_root"])
    require({root["name"]: root["node_id"] for root in
             typed["expression"]["roots"]} == {
                "f0_root": typed["f0_root"],
                "correction_root": typed["correction_root"],
                "candidate_root": typed["candidate_root"]},
            "157em selected typed-candidate root binding")
    validate_wordexpr_payload(row["target_expression"],
                              ["hexagon_1_coface_0"])
    direct = row["direct_gradient"]
    require(set(direct) == {"name", "kind", "entry_count",
            "quotient_value_hex", "canonical_gradient_sha256",
            "canonical_order", "digest_is_binding_only_not_element_equality"} and
            direct["name"] == "hexagon_1_coface_0" and
            direct["kind"] == "hexagon" and
            type(direct["entry_count"]) is int and
            0 <= direct["entry_count"] <= 4_194_304 and
            isinstance(direct["quotient_value_hex"], str) and
            direct["quotient_value_hex"] ==
                (bytes(range(144))+bytes(10)).hex() and
            _sha256_text(direct["canonical_gradient_sha256"]) and
            direct["canonical_order"] ==
                "component then exact canonical E4 bytes" and
            direct["digest_is_binding_only_not_element_equality"] is True and
            (direct["entry_count"] != 0 or
             direct["canonical_gradient_sha256"] == sha_bytes(b"")),
            "157em selected direct-gradient exact contract")
    validate_selected_d2_proof(row["D2_proof"], row["element_registry"],
                               row["proof_root_node_id"])


def validate_separator(row: Any, final_generation: dict[str, Any]) -> None:
    require(isinstance(row, dict) and set(row) == SEPARATOR_KEYS and
            row["generation"] == final_generation["generation"] and
            row["raw_lambda"] == final_generation["raw_lambda"] and
            row["correlation"] == final_generation["correlation"] and
            row["active_row_count"] == 0 and
            row["correlation"]["active_row_count"] == 0 and
            row["complete_76_occurrence_full_11_relator_correlation"] is True and
            row["annihilates_full_D2"] is True and
            row["lambda_delta_all_zero"] is True and
            row["lambda_base_z"] == 2 and
            row["registered_108_family_only"] is True and
            row["pinned_E4_roof_only"] is True,
            "157em exact full-D2 separator")


def expected_phase_seconds_keys(receipt: dict[str, Any]) -> set[str]:
    expected: set[str] = set()
    for field, label in (("base_q3_replay", "authenticated_input"),
                         ("source_preflight", "source_preflight"),
                         ("prefix_B0", "fresh_B0"),
                         ("fixed_B1_block", "fixed_B1"),
                         ("initial_target", "initial_target")):
        if receipt[field]:
            expected.add(label)
    for index, generation in enumerate(receipt["generation_ledger"], 1):
        if index > 1:
            expected.add(f"target_g{index}")
        for field, label in (("raw_lambda", "dual_lift"),
                             ("correlation", "correlation"),
                             ("preflight", "preflight"),
                             ("commit", "commit"),
                             ("incremental", "incremental")):
            if generation[field]:
                expected.add(f"{label}_g{index}")
        if generation["classification"] == "CONSISTENT":
            expected.add(f"selected_proof_g{index}")
    serialization_current = (receipt.get("partial", {}).get("current", {})
        if isinstance(receipt.get("partial"), dict) else {})
    completed_token = (serialization_current.get(
        "completed_terminal_before_serialization")
        if isinstance(serialization_current, dict) else None)
    if completed_token == "B345_E4_D2_COLGEN_TARGET6_CONSISTENT" and \
            receipt["generation_ledger"]:
        expected.add("selected_proof_g" + str(
            receipt["generation_ledger"][-1]["generation"]))
    if receipt["phase"] == "complete":
        expected.add("receipt_serialization")
    elif receipt["phase"] == "receipt_serialization" and \
            serialization_current.get("serialization_phase_completed") is True:
        expected.add("receipt_serialization")
    if receipt["terminal_token"].endswith("UNKNOWN_RESOURCE") and \
            receipt["phase"] == "authenticated_input":
        expected.discard("authenticated_input")
    return expected


def base_receipt(q3_path: Path, monitor: Monitor,
                 inherited: dict[str, int] | None = None) -> dict[str, Any]:
    return {"schema": SCHEMA, "task_sha256": TASK_SHA,
        "terminal_token": None, "status": None, "reason": None,
        "phase": "authenticated_input", "pins": pin_rows(q3_path),
        "caps": dict(CAPS), "caps_sha256": sha_obj(CAPS),
        "upstream_caps": dict(inherited or {}),
        "upstream_caps_sha256": sha_obj(dict(inherited or {})),
        "algorithm": copy.deepcopy(ALGORITHM_PUBLIC),
        "base_q3_replay": {}, "normalized_inverse_fibre": {},
        "seed_manifest": {}, "source_preflight": {},
        "directed_base_support": {}, "directed_surgery": {},
        "prefix_B0": {}, "base_columns": {}, "fixed_B1_block": {},
        "fixed_B1_anchor": {}, "old_qstar_boundary": {},
        "raw_parent_manifest": {}, "recovery_map": {},
        "initial_target": {}, "generation_ledger": [],
        "packed_block_ledger": {}, "selected_proof": {},
        "full_D2_separator": {}, "claims": {},
        "theorem_boundary": theorem_boundary(),
        "provenance": copy.deepcopy(PROVENANCE),
        "resource_guards": {"resource_hit": False, "resource": None,
            "local_and_upstream_separate": True,
            "reason_equals_cap_key": True},
        "partial": {}, "input_errors": [], "performance": {}}


def resource_public(stop: LaneResource) -> dict[str, Any]:
    row = stop.public()
    require(row["cap_reason"] == row["cap_key"] == stop.key,
            "157em resource reason binding")
    return row


def performance_public(monitor: Monitor, phases: dict[str, float],
                       receipt_bytes: int = 0) -> dict[str, Any]:
    row = monitor.public()
    return {**row, "receipt_bytes": receipt_bytes,
        "phase_seconds": dict(phases),
        "correlation_pool_intern_calls": 0,
        "correlation_full_sparse_vectors_materialized": 0,
        "full_E4_enumerations": 0,
        "hard_outer_allowance_seconds": 18000}


_STRUCTURAL_ACCOUNTING_KEYS = (
    "columns", "pivots", "dependent", "live_sparse_entries", "pool_size",
    "DAG_nodes", "DAG_edges", "section_bindings",
    "section_expression_nodes", "section_expression_edges")


def _structural_accounting(row: dict[str, Any]) -> dict[str, int]:
    """ID-free state projection shared by the generation-chain gates."""
    return {key: int(row[key]) for key in _STRUCTURAL_ACCOUNTING_KEYS}


def validate_generation_cross_bind(rows: Sequence[dict[str, Any]], *,
                                   fixed_block: dict[str, Any] | None = None,
                                   fixed_anchor: dict[str, Any] | None = None,
                                   initial_target: dict[str, Any] | None = None,
                                   frozen: bool = True) \
        -> None:
    """Bind every public generation boundary to its actual predecessor.

    Pool-order hashes are intentionally diagnostic and allocation-schedule
    dependent.  All semantic counts and the canonical recovery projection are
    nevertheless exact across each committed boundary.
    """
    if not rows:
        return
    first = rows[0]
    if fixed_block is not None or fixed_anchor is not None:
        require(isinstance(fixed_block, dict) and fixed_block and
                isinstance(fixed_anchor, dict) and fixed_anchor,
                "157em generation-one fixed-B1 prerequisites")
        basis = first["basis"]
        post = fixed_block["post_accounting"]
        anchor_projection = {
            "columns": fixed_anchor["basis_columns"],
            "pivots": fixed_anchor["basis_pivots"],
            "dependent": fixed_anchor["basis_dependent"],
            "live_sparse_entries": fixed_anchor["basis_live_sparse_entries"],
            "pool_size": fixed_anchor["pool_size"],
            "DAG_nodes": fixed_anchor["DAG_nodes"],
            "DAG_edges": fixed_anchor["DAG_edges"],
            "section_bindings": fixed_anchor["section_bindings"],
        }
        require(_structural_accounting(basis) ==
                    _structural_accounting(post) and
                all(basis[key] == value for key, value in
                    anchor_projection.items()),
                "157em generation-one basis/fixed-B1 anchor binding")
    if initial_target is not None:
        require(isinstance(initial_target, dict) and initial_target,
                "157em generation-one initial target prerequisite")
        target = first["target"]; affine = initial_target["affine_system"]
        summary_key = ("fresh_remainder_sha256" if frozen else
                       "base_remainder_sha256")
        opposite_key = ("base_remainder_sha256" if frozen else
                        "fresh_remainder_sha256")
        require(type(frozen) is bool and
                summary_key in initial_target["target6"] and
                opposite_key not in initial_target["target6"],
                "157en exact sealed/fixture target summary key")
        require(target["generation"] == 1 and
                target["variables"] == affine["variables"] and
                target["equations"] == affine["equations"] and
                target["rank"] == affine["rank"] and
                target["nullity"] == affine["nullity"] and
                target["consistent"] is affine["consistent"] and
                target["row_space_sha256"] == affine["row_space_sha256"] and
                target["dual"] == affine["dual_witness"] and
                target["remainders_sha256"] ==
                    initial_target["semantic_remainders_sha256"] and
                target["remainders_sha256"] !=
                    initial_target["target6"][summary_key],
                "157em generation-one target/initial-target binding")
    for ordinal, row in enumerate(rows):
        if not row.get("preflight"):
            continue
        basis = row["basis"]
        preflight = row["preflight"]
        commit = row.get("commit", {})
        require(_structural_accounting(
                    preflight["state_neutrality_before"]) ==
                    _structural_accounting(basis),
                "157em preflight state/generation basis neutrality")
        if commit:
            require(_structural_accounting(commit["pre_accounting"]) ==
                        _structural_accounting(basis) and
                    commit["pre_accounting"]["recovery"] == basis["recovery"],
                    "157em commit pre-state/generation recovery binding")
        incremental = row.get("incremental", {})
        if incremental:
            require(incremental["pre_update_remainder_sha256"] ==
                        row["target"]["remainders_sha256"],
                    "157em incremental pre/generation remainder binding")
            if ordinal+1 < len(rows):
                next_row = rows[ordinal+1]
                require(next_row["target"]["remainders_sha256"] ==
                            incremental["post_update_remainder_sha256"] and
                        _structural_accounting(next_row["basis"]) ==
                            _structural_accounting(commit["post_accounting"]) and
                        next_row["basis"]["recovery"] ==
                            commit["post_accounting"]["recovery"],
                        "157em committed block/incremental next-generation chain")


def validate_generation_ledger(rows: Any, token: str,
                               partial: dict[str, Any] | None = None, *,
                               fixed_block: dict[str, Any] | None = None,
                               fixed_anchor: dict[str, Any] | None = None,
                               initial_target: dict[str, Any] | None = None,
                               frozen: bool = True) -> None:
    require(isinstance(rows, list), "157em generation ledger list")
    allowed = {None, "ACTIVE_BATCH_COMMITTED", "CONSISTENT",
               "FULL_D2_OBSTRUCTION"}
    cumulative_pass1 = 0; cumulative_pass2 = 0
    completed_columns = 11
    prior_post: dict[str, Any] | None = None
    for index, row in enumerate(rows, 1):
        require(isinstance(row, dict) and set(row) == GENERATION_KEYS and
                row["generation"] == index and
                row["classification"] in allowed,
                "157em generation row key/order/classification")
        basis, target = row["basis"], row["target"]
        validate_basis_accounting(basis, pool_digest=False, recovery="public")
        if prior_post is not None:
            require(all(basis[key] == prior_post[key] for key in
                BASIS_ACCOUNTING_KEYS-{"pool_order_sha256"}),
                "157em generation basis equals prior committed anchor")
        require(isinstance(target, dict) and set(target) == TARGET_PUBLIC_KEYS and
                target["generation"] == index and target["variables"] == 108 and
                type(target["equations"]) is int and target["equations"] >= 0 and
                type(target["rank"]) is int and type(target["nullity"]) is int and
                target["rank"]+target["nullity"] == 108 and
                type(target["consistent"]) is bool and
                target["complete_all_coordinates"] is True and
                target["stopped_at_first_contradiction"] is False and
                _sha256_text(target["row_space_sha256"]) and
                _sha256_text(target["remainders_sha256"]) and
                0 <= target["live_remainder_entries"] <=
                    CAPS["target_live_remainders"],
                "157em generation target accounting")
        validate_affine_dual(target["dual"], bool(target["consistent"]))
        classification = row["classification"]
        if classification == "ACTIVE_BATCH_COMMITTED":
            require(all(isinstance(row[key], dict) and row[key] for key in
                        ("raw_lambda", "correlation", "preflight", "commit",
                         "incremental")) and target["consistent"] is False,
                    "157em completed ACTIVE generation")
            validate_raw_lambda(row["raw_lambda"], target, basis,
                                completed_columns)
            cumulative_pass1, cumulative_pass2 = validate_correlation_public(
                row["correlation"], index, cumulative_pass1, cumulative_pass2,
                row["raw_lambda"]["per_component"])
            require(row["correlation"]["active_row_count"] > 0 and
                    row["correlation"]["selected_translation_count"] > 0,
                    "157em ACTIVE correlation/batch")
            validate_preflight(row["preflight"], index, row["correlation"])
            validate_commit(row["commit"], index, row["preflight"])
            validate_incremental(row["incremental"], index, row["commit"])
            prior_post = row["commit"]["post_accounting"]
            completed_columns += row["commit"]["column_count"]
        elif classification == "CONSISTENT":
            require(target["consistent"] is True and all(row[key] == {} for key in
                    ("raw_lambda", "correlation", "preflight", "commit",
                     "incremental")), "157em consistent generation boundary")
        elif classification == "FULL_D2_OBSTRUCTION":
            require(target["consistent"] is False and row["raw_lambda"] and
                    row["correlation"] and all(row[key] == {} for key in
                     ("preflight", "commit", "incremental")),
                     "157em full-D2 generation boundary")
            validate_raw_lambda(row["raw_lambda"], target, basis,
                                completed_columns)
            cumulative_pass1, cumulative_pass2 = validate_correlation_public(
                row["correlation"], index, cumulative_pass1, cumulative_pass2,
                row["raw_lambda"]["per_component"])
            require(row["correlation"]["active_row_count"] == 0,
                    "157em zero complete full-D2 correlation")
        else:
            require(index == len(rows), "157em only final generation is partial")
            if target["consistent"]:
                require(all(row[key] == {} for key in ("raw_lambda",
                    "correlation", "preflight", "commit", "incremental")),
                    "157em consistent proof-resource prefix")
            else:
                present = [bool(row[key]) for key in ("raw_lambda",
                    "correlation", "preflight", "commit", "incremental")]
                require(present == sorted(present, reverse=True),
                        "157em RESOURCE generation fill-prefix")
                if row["raw_lambda"]:
                    validate_raw_lambda(row["raw_lambda"], target, basis,
                                        completed_columns)
                if row["correlation"]:
                    cumulative_pass1, cumulative_pass2 = \
                        validate_correlation_public(row["correlation"], index,
                            cumulative_pass1, cumulative_pass2,
                            row["raw_lambda"]["per_component"])
                if row["preflight"]:
                    validate_preflight(row["preflight"], index,
                                       row["correlation"])
                if row["commit"]:
                    validate_commit(row["commit"], index, row["preflight"])
                if row["incremental"]:
                    validate_incremental(row["incremental"], index,
                                         row["commit"])
    validate_generation_cross_bind(rows, fixed_block=fixed_block,
        fixed_anchor=fixed_anchor, initial_target=initial_target,
        frozen=frozen)
    if not rows:
        return
    for row in rows[:-1]:
        require(row["classification"] == "ACTIVE_BATCH_COMMITTED",
                "157em generation prefix classification")
    final = rows[-1]["classification"]
    if token.endswith("CONSISTENT"):
        require(final == "CONSISTENT", "157em terminal/generation consistent")
    elif token.endswith("FULL_D2_OBSTRUCTION"):
        require(final == "FULL_D2_OBSTRUCTION",
                "157em terminal/generation obstruction")
    elif partial is not None:
        require(final in {None, "ACTIVE_BATCH_COMMITTED"},
                "157em resource generation prefix")
        require(partial["completed_generation_count"] == sum(
            row["classification"] == "ACTIVE_BATCH_COMMITTED" for row in rows),
            "157em partial completed-generation binding")


def _validate_source_progress(current: dict[str, Any]) -> None:
    require(set(current) == SOURCE_PROGRESS_KEYS and
            (current["current_seed"] is None or
             type(current["current_seed"]) is int and
             1 <= current["current_seed"] <= 108) and
            type(current["evaluated_seeds"]) is int and
            0 <= current["evaluated_seeds"] <= 108 and
            (current["current_seed"] is None and
             current["evaluated_seeds"] == 0 or
             current["current_seed"] is not None and
             current["evaluated_seeds"] in {
                current["current_seed"]-1, current["current_seed"]}) and
            _sha256_text(current["records_prefix_sha256"]),
            "157em exact source RESOURCE prefix")


def _validate_fixed_B1_progress(current: dict[str, Any]) -> None:
    require(set(current) == FIXED_B1_PROGRESS_KEYS,
            "157em exact fixed-B1 RESOURCE keys")
    attempted = current["attempted_relators"]
    completed = current["completed_relators"]
    raw = current["raw_completed_relators"]
    shadow = current["shadow_completed_relators"]
    rank = current["rank_gain_so_far"]
    relator = current["current_relator"]
    require(all(type(value) is int for value in
                (attempted, completed, raw, shadow, rank)) and
            0 <= attempted <= 11 and 0 <= completed <= 11 and
            0 <= shadow <= raw <= 11 and 0 <= rank <= completed and
            len(current["raw_prefix"]) == raw and
            len(current["shadow_prefix"]) == shadow and
            len(current["scalar_prefix"]) == shadow and
            len(current["block_prefix"]) == completed and
            isinstance(current["block_pre_accounting"], dict) and
            isinstance(current["block_post_accounting"], dict),
            "157em fixed-B1 RESOURCE counts")
    stage = current["substage"]
    if stage == "translation_section":
        require((attempted, completed, raw, shadow, rank) == (0, 0, 0, 0, 0)
                and relator is None,
                "157em fixed-B1 translation-section prefix")
    elif stage == "shadow_remainders":
        require(completed == rank == 0 and relator == attempted and
                1 <= attempted <= 11 and attempted in {raw, raw+1} and
                raw-shadow in {0, 1},
                "157em fixed-B1 shadow prefix")
    else:
        require(stage == "persistent_columns" and raw == shadow == 11 and
                relator == attempted and
                completed <= attempted <= completed+1 and
                1 <= attempted <= 11,
                "157em fixed-B1 persistent prefix")


def _validate_initial_target_progress(current: dict[str, Any]) -> None:
    require(set(current) == INITIAL_TARGET_PROGRESS_KEYS and
            current["substage"] in {"typed_formula_setup", "base_remainder",
                "seed_remainder", "affine_absorption"} and
            type(current["evaluated_seeds"]) is int and
            0 <= current["evaluated_seeds"] <= 108 and
            type(current["completed_equations"]) is int and
            current["completed_equations"] >= 0 and
            (current["current_seed"] is None or
             type(current["current_seed"]) is int and
             1 <= current["current_seed"] <= 108) and
            isinstance(current["typed_split_prefix"], list) and
            len(current["typed_split_prefix"]) ==
                current["evaluated_seeds"] and
            isinstance(current["remainder_prefix"], list) and
            len(current["remainder_prefix"]) in {
                0, current["evaluated_seeds"]+1} and
            (current["completed_target_system"] is None or
             isinstance(current["completed_target_system"], dict)),
            "157em exact initial-target RESOURCE prefix")


def _validate_block_progress(current: dict[str, Any],
                             packed: dict[str, Any]) -> None:
    require(set(current) == BLOCK_PROGRESS_KEYS and
            type(current["generation"]) is int and
            1 <= current["generation"] <= CAPS["column_generation_batches"] and
            type(current["selected_translation_count"]) is int and
            1 <= current["selected_translation_count"] <= 1024 and
            type(current["completed_translations"]) is int and
            0 <= current["completed_translations"] <=
                current["selected_translation_count"] and
            type(current["attempted_translation"]) is int and
            current["completed_translations"] <=
                current["attempted_translation"] <=
                min(current["selected_translation_count"],
                    current["completed_translations"]+1) and
            type(current["completed_relators"]) is int and
            0 <= current["completed_relators"] <= 11 and
            type(current["attempted_relator"]) is int and
            0 <= current["attempted_relator"] <= 11 and
            current["batch_anchor_committed"] is False and
            type(current["unfinished_translation_rolled_back"]) is bool and
            len(current["completed_translation_prefix"]) ==
                current["completed_translations"] and
            all(isinstance(value, str) and len(value) == 2*WIDTH
                for value in current["completed_translation_prefix"]) and
            type(current["completed_record_count"]) is int and
            current["completed_record_count"] == packed["record_count"] and
            isinstance(current["pre_accounting"], dict) and
            isinstance(current["post_failure_accounting"], dict),
            "157em exact block RESOURCE prefix")
    validate_basis_accounting(current["pre_accounting"], pool_digest=True,
                              recovery="public")
    validate_basis_accounting(current["post_failure_accounting"],
                              pool_digest=True, recovery="public")
    if current["unfinished_translation_rolled_back"]:
        require(current["rollback_translation_ordinal"] ==
                    current["attempted_translation"] and
                current["completed_relators"] == 0,
                "157em rolled-back translation prefix")
    else:
        require(current["rollback_translation_ordinal"] is None,
                "157em nonrollback translation prefix")


def _validate_incremental_progress(current: dict[str, Any]) -> None:
    require(set(current) == INCREMENTAL_PROGRESS_KEYS and
            type(current["generation"]) is int and
            1 <= current["generation"] <= CAPS["column_generation_batches"] and
            type(current["new_pivot_count"]) is int and
            current["new_pivot_count"] >= 1 and
            type(current["completed_quotient_pivot_ordinal"]) is int and
            0 <= current["completed_quotient_pivot_ordinal"] <=
                current["new_pivot_count"] and
            type(current["completed_new_pivot_ordinal"]) is int and
            0 <= current["completed_new_pivot_ordinal"] <=
                current["new_pivot_count"] and
            type(current["completed_rows_in_current_pivot"]) is int and
            0 <= current["completed_rows_in_current_pivot"] <= 109 and
            current["batch_anchor_committed"] is True and
            current["rolled_back_on_failure"] is True and
            current["remaining_rows"] == [None]*109 and
            type(current["live_entry_count"]) is int and
            0 <= current["live_entry_count"] <=
                CAPS["target_live_remainders"] and
            all(current[key] is None or _sha256_text(current[key]) for key in
                ("last_fully_updated_row_sha256",
                 "reduction_order_sha256", "old_pivot_set_sha256")) and
            all(_sha256_text(current[key]) for key in
                ("pre_update_remainder_sha256",
                 "current_new_pivot_prefix_sha256",
                 "completed_quotient_prefix_sha256")) and
            (current["old_pivot_count"] is None or
             type(current["old_pivot_count"]) is int and
             current["old_pivot_count"] >= 0) and
            (current["old_pivot_set_encoding"] is None or
             isinstance(current["old_pivot_set_encoding"], str)) and
            type(current["quotient_rows_discarded_on_failure"]) is bool,
            "157em exact incremental RESOURCE rollback")


def validate_resource_current(detail: dict[str, Any],
                              receipt: dict[str, Any],
                              partial: dict[str, Any]) -> None:
    """Close every public attempted-stage shape without promoting it."""
    phase, key, current = detail["phase"], detail["cap_key"], detail["current"]
    packed = partial["packed_block_ledger_prefix"]
    local_monitor_empty = (detail["cap_source"] == "local" and
        key in {"common_math_soft_deadline_seconds",
                "producer_soft_rss_bytes"} and
        detail["inner_phase"] in MONITOR_REGISTRY[phase] and current == {})
    if phase == "authenticated_input":
        require(current == {}, "157em authenticated RESOURCE current")
    elif phase == "source_preflight":
        _validate_source_progress(current)
    elif phase == "fresh_B0":
        if current == {}:
            require(detail["cap_source"] == "upstream" or
                    local_monitor_empty,
                    "157em fresh-B0 empty RESOURCE current source")
        elif set(current) == {"candidate_edges"}:
            require(detail["cap_source"] == "local" and
                    key == "raw_coordinate_recovery_nodes" and
                    type(current["candidate_edges"]) is int and
                    current["candidate_edges"] >= 0,
                    "157em fresh-B0 recovery-node current")
        elif set(current) == {"completed_candidate_edges"}:
            require(detail["cap_source"] == "local" and
                    key in {"raw_coordinate_recovery_edges",
                            "raw_coordinate_recovery_nodes"} and
                    type(current["completed_candidate_edges"]) is int and
                    current["completed_candidate_edges"] >= 0,
                    "157em fresh-B0 recovery preflight current")
        else:
            require(False, "157em fresh-B0 RESOURCE current")
    elif phase == "fixed_B1":
        if set(current) == FIXED_B1_PROGRESS_KEYS:
            _validate_fixed_B1_progress(current)
        elif set(current) == {"lambda_ordinal", "base_component_ordinal"}:
            require(all(type(value) is int and value >= 1
                        for value in current.values()),
                    "157em fixed-B1 correlation pair current")
        elif set(current) == {"post_accumulation"}:
            require(current["post_accumulation"] is True,
                    "157em fixed-B1 correlation post current")
        else:
            require(current == {} or set(current) in (
                {"completed_candidate_edges"}, {"candidate_edges"}) and
                all(type(value) is int and value >= 0
                    for value in current.values()),
                "157em fixed-B1 RESOURCE current")
    elif phase == "initial_target":
        if set(current) == INITIAL_TARGET_PROGRESS_KEYS:
            _validate_initial_target_progress(current)
        elif current == {}:
            require(local_monitor_empty,
                    "157em initial-target empty monitor current")
        else:
            require(set(current) in ({"completed_parent_entries"},
                    {"candidate_edges"}) and
                    detail["cap_source"] == "local" and
                    ((set(current) == {"completed_parent_entries"} and
                      key == "raw_coordinate_parent_entries") or
                     (set(current) == {"candidate_edges"} and
                      key == "raw_coordinate_recovery_nodes")) and
                    all(type(value) is int and value >= 0
                        for value in current.values()),
                    "157em initial-target recovery current")
    elif phase == "dual_lift":
        require(current == {} or set(current) ==
                {"completed_reverse_pivots"} and
                type(current["completed_reverse_pivots"]) is int and
                current["completed_reverse_pivots"] >= 0,
                "157em dual-lift RESOURCE current")
    elif phase in {"correlation_pass1", "correlation_pass2"}:
        if current == {}:
            require(local_monitor_empty,
                    "157em correlation empty monitor current")
        else:
            require(set(current) in ({"generation"},
                    {"generation", "completed_batches", "completed_blocks"}) and
                    detail["cap_source"] == "local" and
                    key in ({"correlation_pass1_pairs_per_generation",
                             "correlation_pass1_pairs_total",
                             "distinct_correlation_candidates",
                             "packed_active_rows",
                             "column_generation_batches",
                             "total_new_translation_blocks"} if
                            phase == "correlation_pass1" else
                            {"correlation_pass2_pairs_per_generation",
                             "correlation_pass2_pairs_total"}) and
                    type(current["generation"]) is int and
                    current["generation"] >= 1 and
                    all(type(value) is int and value >= 0
                        for value in current.values()),
                    "157em correlation RESOURCE current")
    elif phase == "section_recovery":
        require(current == {} or set(current) == {"node"} and
                type(current["node"]) is int and current["node"] >= 0,
                "157em section RESOURCE current")
    elif phase == "batch_precompute":
        require(current == {} or set(current) ==
                {"generation", "translation_ordinal", "relator"} and
                all(type(value) is int and value >= 1
                    for value in current.values()),
                "157em precompute RESOURCE current")
    elif phase == "block_commit":
        _validate_block_progress(current, packed)
    elif phase == "incremental_reduction":
        _validate_incremental_progress(current)
    elif phase == "target_resolve":
        require(current == {}, "157em target-resolve RESOURCE current")
    elif phase == "selected_proof":
        require(current == {} or set(current) ==
                {"generation", "completed_target"} and
                type(current["generation"]) is int and
                current["generation"] >= 1 and
                current["completed_target"] is True,
                "157em selected-proof RESOURCE current")
    elif phase == "receipt_serialization":
        require(current == {} or set(current) == {
                "completed_terminal_before_serialization",
                "packed_block_ledger_prefix",
                "serialization_phase_completed"} and
                current["completed_terminal_before_serialization"] in
                    TERMINALS-{"B345_E4_D2_COLGEN_TARGET6_UNKNOWN_RESOURCE",
                               "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT"} and
                current["packed_block_ledger_prefix"] == packed and
                type(current["serialization_phase_completed"]) is bool,
                "157em serialization RESOURCE current")
    else:
        require(False, "157em RESOURCE outer phase")
    if key in {"column_generation_batches", "total_new_translation_blocks"}:
        require(phase == "correlation_pass1" and
                set(current) ==
                    {"generation", "completed_batches", "completed_blocks"} and
                (key != "column_generation_batches" or
                 current["completed_batches"] ==
                    CAPS["column_generation_batches"]) and
                (key != "total_new_translation_blocks" or
                 current["completed_blocks"] ==
                    CAPS["total_new_translation_blocks"]),
                "157em exhausted-budget RESOURCE shape")


def validate_resource_stage_projection(receipt: dict[str, Any],
                                       detail: dict[str, Any], *,
                                       require_external_prefix: bool) -> None:
    phase = detail["phase"]
    fields = receipt
    early = ("base_q3_replay", "normalized_inverse_fibre", "seed_manifest")
    prefix = ("directed_base_support", "directed_surgery", "prefix_B0")
    fixed = ("base_columns", "fixed_B1_block", "fixed_B1_anchor",
             "old_qstar_boundary")
    initial = ("raw_parent_manifest", "recovery_map", "initial_target")
    # Isolated bounded current-shape canaries intentionally carry no imported
    # mathematical prefix.  Once any such payload is present, however, the
    # exact production stage table is mandatory even for a sealed fixture.
    external_payload_present = any(bool(fields[key]) for key in
        (*early, "source_preflight", *prefix, *fixed, *initial,
         "generation_ledger"))
    if not require_external_prefix and not external_payload_present:
        pass
    elif phase == "authenticated_input":
        early_present = [bool(fields[key]) for key in early]
        require(early_present == sorted(early_present, reverse=True) and
            not fields["source_preflight"] and
            all(not fields[key] for key in (*prefix, *fixed, *initial,
                "generation_ledger")),
            "157em authenticated RESOURCE stage")
    elif phase == "source_preflight":
        require(all(fields[key] for key in early) and
                not fields["source_preflight"] and
                all(not fields[key] for key in (*prefix, *fixed, *initial,
                    "generation_ledger")), "157em source RESOURCE stage")
    elif phase == "fresh_B0":
        require(all(fields[key] for key in (*early, "source_preflight")) and
                all(not fields[key] for key in (*prefix, *fixed, *initial,
                    "generation_ledger")), "157em B0 RESOURCE stage")
    elif phase == "fixed_B1":
        require(all(fields[key] for key in (*early, "source_preflight", *prefix))
                and all(not fields[key] for key in (*fixed, *initial,
                    "generation_ledger")), "157em B1 RESOURCE stage")
    elif phase == "initial_target":
        require(all(fields[key] for key in
                    (*early, "source_preflight", *prefix, *fixed)) and
                all(not fields[key] for key in (*initial, "generation_ledger")),
                "157em initial-target RESOURCE stage")
    else:
        require(all(fields[key] for key in
                    (*early, "source_preflight", *prefix, *fixed, *initial)),
                "157em adaptive RESOURCE authenticated prefix")
        rows = fields["generation_ledger"]
        require(isinstance(rows, list) and rows,
                "157em adaptive RESOURCE generation")
        last = rows[-1]
        if phase == "dual_lift":
            require(last["classification"] is None and
                    all(not last[key] for key in ("raw_lambda", "correlation",
                        "preflight", "commit", "incremental")),
                    "157em dual-lift stage prefix")
        elif phase in {"correlation_pass1", "correlation_pass2"}:
            require(last["classification"] is None and last["raw_lambda"] and
                    not last["preflight"] and not last["commit"] and
                    not last["incremental"],
                    "157em correlation stage prefix")
        elif phase in {"section_recovery", "batch_precompute"}:
            require(last["classification"] is None and last["raw_lambda"] and
                    last["correlation"] and not last["preflight"] and
                    not last["commit"] and not last["incremental"],
                    "157em precommit stage prefix")
        elif phase == "block_commit":
            require(last["classification"] is None and last["preflight"] and
                    not last["commit"] and not last["incremental"],
                    "157em block stage prefix")
        elif phase == "incremental_reduction":
            require(last["classification"] is None and last["commit"] and
                    not last["incremental"],
                    "157em incremental stage prefix")
        elif phase == "target_resolve":
            require(last["classification"] == "ACTIVE_BATCH_COMMITTED" and
                    last["incremental"], "157em target-resolve stage prefix")
        elif phase == "selected_proof":
            require(last["classification"] is None and
                    last["target"]["consistent"] is True and
                    all(not last[key] for key in ("raw_lambda", "correlation",
                        "preflight", "commit", "incremental")),
                    "157em selected-proof stage prefix")
        elif phase == "receipt_serialization":
            require(last["classification"] is None and
                    (last["target"]["consistent"] is True or
                     last["raw_lambda"] and last["correlation"] and
                     not last["preflight"]),
                    "157em serialization stage prefix")
            completed_token = detail["current"].get(
                "completed_terminal_before_serialization")
            if completed_token is not None:
                require((completed_token.endswith("CONSISTENT") and
                         last["target"]["consistent"] is True) or
                        (completed_token.endswith("FULL_D2_OBSTRUCTION") and
                         last["target"]["consistent"] is False and
                         last["correlation"]["active_row_count"] == 0),
                        "157em serialization prior-terminal binding")
        else:
            require(False, "157em adaptive RESOURCE phase")
    rows = receipt["generation_ledger"]
    active_rows = [row for row in rows if
                   row.get("classification") == "ACTIVE_BATCH_COMMITTED"]
    expected_batches = len(active_rows)
    expected_blocks = sum(row["commit"]["translation_count"]
                          for row in active_rows)
    if phase == "block_commit":
        expected_blocks += detail["current"]["completed_translations"]
    elif phase == "incremental_reduction":
        expected_batches += 1
        expected_blocks += rows[-1]["commit"]["translation_count"]
    partial = receipt["partial"]
    if detail["cap_key"] in {
            "column_generation_batches", "total_new_translation_blocks"}:
        require(detail["current"]["completed_batches"] == expected_batches and
                detail["current"]["completed_blocks"] == expected_blocks,
                "157em exhausted-budget current/ledger binding")
    require(partial["completed_generation_count"] == len(active_rows) and
            partial["completed_batch_count"] == expected_batches and
            partial["completed_new_translation_block_count"] ==
                expected_blocks,
            "157em RESOURCE committed generation/batch/block projection")


def validate_resource_detail(detail: Any, receipt: dict[str, Any]) -> None:
    require(isinstance(detail, dict) and set(detail) == RESOURCE_KEYS and
            detail["cap_reason"] == detail["cap_key"] == receipt["reason"] and
            detail["phase"] == receipt["phase"] in OUTER_PHASES and
            detail["cap_source"] in {"local", "upstream"} and
            detail["comparator"] in {"gt", "ge"} and
            type(detail["cap_limit"]) is int and
            type(detail["observed_count"]) is int and
            isinstance(detail["current"], dict) and
            (detail["detail"] is None or isinstance(detail["detail"], str)) and
            (detail["inner_phase"] is None or
             isinstance(detail["inner_phase"], str)),
            "157em exact resource row")
    registry = (CAPS if detail["cap_source"] == "local" else
                receipt["upstream_caps"])
    require(detail["cap_key"] in registry and
            detail["cap_limit"] == registry[detail["cap_key"]] and
            detail["comparator"] == cap_comparator(
                detail["cap_key"], detail["cap_source"]) and
            ((detail["comparator"] == "gt" and
              detail["observed_count"] > detail["cap_limit"]) or
             (detail["comparator"] == "ge" and
              detail["observed_count"] >= detail["cap_limit"])),
            "157em resource registry/limit/comparator")
    if detail["cap_source"] == "local":
        if detail["cap_key"] in {"common_math_soft_deadline_seconds",
                                  "producer_soft_rss_bytes"}:
            require(detail["inner_phase"] in
                    MONITOR_REGISTRY[detail["phase"]],
                    "157em local monitor resource pair")
        else:
            require(detail["inner_phase"] is None,
                    "157em local count cap has no inherited phase")
    else:
        shape = upstream_current_shape(detail["current"])
        require(isinstance(detail["inner_phase"], str) and
                detail["cap_key"] in UPSTREAM_THROW_SITES and
                (detail["phase"], detail["inner_phase"], shape) in
                    UPSTREAM_THROW_SITES[detail["cap_key"]],
                "157em exact upstream throw-site/outer/current binding")
    expected_detail = {
        "total_new_translation_blocks":
            "total_translation_block_budget_exhausted",
        "column_generation_batches": "column_generation_batch_limit",
    }.get(detail["cap_key"])
    require(detail["detail"] == expected_detail,
            "157em resource detail closed reason registry")


def validate_partial(partial: Any, detail: dict[str, Any]) -> None:
    require(isinstance(partial, dict) and set(partial) == PARTIAL_KEYS and
            partial["phase"] == detail["phase"] and
            partial["reason"] == detail["cap_key"] and
            partial["current"] == detail["current"] and
            partial["selected_proof"] is None and
            partial["full_D2_separator"] is None and
            all(type(partial[key]) is int and partial[key] >= 0 for key in
                ("completed_generation_count", "completed_batch_count",
                 "completed_new_translation_block_count")) and
            (partial["current_generation"] is None or
             type(partial["current_generation"]) is int and
             partial["current_generation"] >= 1) and
            isinstance(partial["packed_block_ledger_prefix"], dict),
            "157em exact resource partial")
    packed = partial["packed_block_ledger_prefix"]
    require(set(packed) == PACKED_PARTIAL_KEYS and
            packed["format"] == "complete-D2-block-ledger/v1-partial" and
            packed["record_bytes"] == 225 and
            packed["base64_omitted_for_resource_partial"] is True and
            type(packed.get("translation_count")) is int and
            type(packed.get("record_count")) is int and
            packed["translation_count"] ==
                partial["completed_new_translation_block_count"] and
            packed["record_count"] == 11*packed["translation_count"] and
            packed["translation_decoded_bytes"] == WIDTH*packed[
                "translation_count"] and
            packed["decoded_bytes"] == 225*packed["record_count"] and
            _sha256_text(packed["translation_sha256"]) and
            _sha256_text(packed["decoded_sha256"]),
            "157em partial packed ledger/count binding")
    require(partial["completed_batch_count"] in {
                partial["completed_generation_count"],
                partial["completed_generation_count"]+1} and
            (partial["current_generation"] is None or
             partial["current_generation"] in {
                partial["completed_generation_count"]+1,
                partial["completed_generation_count"]}) and
            partial["completed_new_translation_block_count"] ==
                packed["translation_count"],
            "157em partial committed generation/batch relations")


BASE_COLUMN_KEYS = {"D1_D2_zero_all", "occurrence_count", "occurrences",
    "order", "ordered_sha256", "per_component_counts",
    "per_relator_counts", "private_fields_published",
    "quotient_identity_all"}
BASE_OCCURRENCE_KEYS = {"relator_index", "component", "coefficient",
    "element_hex", "section_word"}
PREFIX_B0_KEYS = {"counts", "accounting", "basis_gate",
    "prefix_pool_checkpoint", "pool_order_sha256", "dependent_events",
    "dependent_event_count", "dependent_event_sha256",
    "fresh_not_imported", "source_sha256",
    "stable_rounds_projection_sha256", "translations_sha256",
    "columns_sha256", "blocker_history_sha256",
    "complete_block_registry"}
PREFIX_COUNT_KEYS = {"BFS_translations", "columns", "dependent_columns",
    "directed_translations", "live_sparse_entries", "pivots",
    "row_tail_visits"}
PREFIX_ACCOUNTING_KEYS = {"BFS_translations", "columns",
    "dependent_columns", "directed_translations", "element_pool",
    "live_sparse_entries", "pivots", "provenance_DAG",
    "single_shared_basis", "targeted_translations_for_six_questions",
    "total_translation_blocks"}
PREFIX_POOL_KEYS = {"canonical_order", "capacity", "digest_used_as_equality",
    "exact_equality", "hits", "inverse_cache", "max_rollback_suffix",
    "misses", "packed_payload_bytes", "packed_width_bytes", "peak",
    "product_cache", "rollback_lru_clears", "rollback_suffix_removed",
    "size", "transaction_commits", "transaction_rollbacks"}
PREFIX_CACHE_KEYS = {"capacity", "clears", "evictions", "hits", "misses",
    "peak", "size"}
PREFIX_DAG_KEYS = {"edge_payload_bytes", "live_edges", "live_nodes",
    "node_payload_bytes", "packed_arrays", "peak_edges", "peak_nodes"}
PREFIX_BASIS_GATE_KEYS = {"immutable_during_affine_probes",
    "least_pivot_coeff_one", "no_preceding_keys", "pivot_order", "pivots",
    "rows"}
PREFIX_DEPENDENT_KEYS = {"byte_length", "column_ordinal", "encoding",
    "raw_column", "relator_index", "schedule", "sha256", "support",
    "translation_blob", "translation_ordinal"}
COMPLETE_REGISTRY_KEYS = {"translation_count", "relators_per_translation",
    "all_masks_equal_0x7ff", "canonical_translation_sha256",
    "semantic_blob_order", "pool_IDs_public"}
DIRECTED_SUPPORT_KEYS = {"all_prefix_sections_directly_replayed",
    "occurrence_count", "occurrences", "order", "ordered_sha256"}
DIRECTED_SURGERY_KEYS = {"blocker_history", "blocker_history_sha256",
    "bounded_prefix_sha256", "column_count", "column_order",
    "columns_sha256", "round_count", "rounds", "rounds_sha256",
    "section_expressions", "section_oracle", "stable_projection_omits_exactly",
    "stable_rounds_projection", "stable_rounds_projection_sha256",
    "stop_reason", "theorem", "translation_count", "translations",
    "translations_sha256", "volatile_rounds_sha256_provenance_only"}
BLOCK_KEYS = {"complete", "translation_ordinal", "translation_hex",
    "section_newly_registered", "section_word_length", "section_word_sha256",
    "columns", "column_count", "column_order", "old_qstar_scalars",
    "raw_columns_sha256", "reducer_ledger_sha256", "pre_accounting",
    "post_accounting", "rank_gain", "shadow_rank_mod_B0",
    "two_rank_computations_equal", "relator9_independent",
    "pivot_count_before_relator9", "pivot_count_after_relator9",
    "lexfirst_active_provenance", "all_11_rows_are_D2_columns"}
BLOCK_COLUMN_KEYS = {"relator_index", "translation_ordinal",
    "translation_hex", "termwise_equals_direct_left_translation",
    "quotient_identity", "D1_D2_zero", "old_qstar_scalar", "independent",
    "pivot", "raw_column"}
BLOCK_RAW_KEYS = {"entries", "entry_count", "byte_length", "sha256",
    "encoding", "order"}
BLOCK_ANCHOR_KEYS = {"after_complete_block", "basis_columns", "basis_pivots",
    "basis_dependent", "basis_live_sparse_entries", "pool_size", "DAG_nodes",
    "DAG_edges", "section_bindings", "translation_retained",
    "anchor_semantic_sha256", "private_anchor_ids_not_exported"}
OLD_QSTAR_KEYS = {"used_only_to_freshly_reconstruct_fixed_B1",
    "used_after_fixed_B1", "support_count", "support_sha256",
    "complete_correlation_sha256"}
RAW_PARENT_KEYS = {"source_count", "rows", "rows_sha256",
    "source_word_order", "signed_offset_convention"}
RAW_PARENT_ROW_KEYS = {"source_word_ordinal", "word_length", "word_sha256",
    "gradient_entry_count", "gradient_sha256", "all_nonzero_terms_parented"}
INITIAL_TARGET_KEYS = {"target6", "affine_system",
    "fresh_B1_stable_digests_all_equal", "raw_gradient_count",
    "raw_gradients_sha256", "semantic_remainders_sha256"}

# Authenticated front-end projections.  These are deliberately closed here,
# rather than treated as merely truthy prerequisites for the large prefix.
BASE_Q3_REPLAY_KEYS = {"fixed_word", "roof_exponent", "roof_order",
    "arithmetic_outside_by_index_three", "marking_m", "lambda",
    "hexagon_residual_words_F2", "pentagon_residual_word_PB4",
    "derived_membership", "onto_small_factors", "settled_source_words",
    "replayed_not_copied"}
NORMALIZED_INVERSE_KEYS = {"source", "normalized_exponent",
    "normalized_roof_order", "normalized_power_row",
    "correction_fibre_size", "tested_indices", "passing_indices",
    "selection_policy", "selected_correction_index",
    "selected_correction_word", "selected_inverse_candidate_word",
    "selected_inverse_words", "max_inverse_word_length",
    "raw_endomorphism_powering_used",
    "componentwise_Q4_Pi4_inverse_words_combined"}
SEED_MANIFEST_KEYS = {"cube_words", "cube_count", "old_seed_words",
    "old_seed_count", "new_seed_words", "new_seed_count", "seed_words",
    "seed_count", "old_seed_digest_sha256", "new_seed_digest_sha256",
    "digest_obj_sha256", "cube_digest_sha256", "triple4_manifest",
    "provenance", "order", "commutator", "literal_threefold_cube",
    "four_preregistered_positive_triple_cube_words", "all_E3_identity",
    "all_exponent_sums_zero", "registered_BFS_not_constructed"}
SOURCE_PREFLIGHT_KEYS = {"supported", "seed_count", "contexts_per_seed",
    "unique_context_count", "context_registry_sha256", "named_use_count",
    "context_registry", "records", "source_contexts",
    "all_source_tuples_equal", "all_correction_occurrences_identity"}
SOURCE_CONTEXT_REGISTRY_KEYS = {"context_count", "contexts", "named_uses",
    "named_use_count", "named_use_mapping_sha256", "context_rows_sha256",
    "deduplication"}
SOURCE_CONTEXT_ROW_KEYS = {"context_id", "left_hex", "right_hex"}
SOURCE_NAMED_USE_KEYS = {"name", "context_id"}
SOURCE_PREFLIGHT_RECORD_KEYS = {"seed_index", "source_tuple_equal",
    "correction_context_count", "correction_contexts_sha256",
    "named_use_count", "context_registry_unique_count",
    "context_registry_sha256"}


def _semantic_raw_bytes(rows: Sequence[Sequence[Any]]) -> bytes:
    encoded = bytearray()
    for component, value_hex, coefficient in rows:
        value = bytes.fromhex(str(value_hex))
        require(1 <= int(component) <= 6 and len(value) == WIDTH and
                int(coefficient) in (1, 2), "157em public raw entry")
        encoded.append(int(component)); encoded.extend(value)
        encoded.append(int(coefficient))
    return bytes(encoded)


def validate_base_columns_public(row: Any, *, frozen: bool) -> None:
    require(isinstance(row, dict) and set(row) == BASE_COLUMN_KEYS and
            row["D1_D2_zero_all"] is True and
            row["quotient_identity_all"] is True and
            row["private_fields_published"] is False and
            row["order"] == "relator index, component, canonical E4 bytes" and
            type(row["occurrence_count"]) is int and
            row["occurrence_count"] == len(row["occurrences"]) and
            row["ordered_sha256"] == sha_obj(row["occurrences"]),
            "157em exact base-column public")
    per_rel = [0]*11; per_comp = [0]*6
    prior: tuple[int, int, bytes] | None = None
    for occurrence in row["occurrences"]:
        require(isinstance(occurrence, dict) and
                set(occurrence) == BASE_OCCURRENCE_KEYS and
                1 <= int(occurrence["relator_index"]) <= 11 and
                1 <= int(occurrence["component"]) <= 6 and
                int(occurrence["coefficient"]) in (1, 2) and
                len(bytes.fromhex(occurrence["element_hex"])) == WIDTH and
                isinstance(occurrence["section_word"], list) and
                all(type(letter) is int and letter != 0
                    for letter in occurrence["section_word"]),
                "157em base occurrence row")
        key = (int(occurrence["relator_index"]),
               int(occurrence["component"]),
               bytes.fromhex(occurrence["element_hex"]))
        require(prior is None or prior <= key, "157em base occurrence order")
        prior = key; per_rel[key[0]-1] += 1; per_comp[key[1]-1] += 1
    require(row["per_relator_counts"] == per_rel and
            row["per_component_counts"] == per_comp,
            "157em base occurrence distributions")
    if frozen:
        require(row["occurrence_count"] == 76 and
                row["ordered_sha256"] == BASE_OCCURRENCE_SHA and
                per_rel == [8, 6, 8, 6, 4, 8, 12, 6, 4, 8, 6] and
                per_comp == [10, 12, 18, 10, 12, 14],
                "157em frozen 76-occurrence bundle")


def validate_directed_base_support(row: Any, base: dict[str, Any] | None, *,
                                   frozen: bool) -> None:
    require(isinstance(row, dict) and set(row) == DIRECTED_SUPPORT_KEYS and
            row["all_prefix_sections_directly_replayed"] is True and
            row["occurrence_count"] == len(row["occurrences"]) and
            row["ordered_sha256"] == sha_obj(row["occurrences"]) and
            row["order"] == "relator index, component, canonical E4 bytes" and
            all(isinstance(item, dict) and set(item) == BASE_OCCURRENCE_KEYS
                for item in row["occurrences"]),
            "157em directed/base occurrence exact binding")
    if base is not None:
        require(row["order"] == base["order"] and
                row["occurrences"] == base["occurrences"] and
                row["occurrence_count"] == base["occurrence_count"] and
                row["ordered_sha256"] == base["ordered_sha256"],
                "157em directed/base fresh public equality")
    if frozen:
        require(row["occurrence_count"] == 76 and
                row["ordered_sha256"] == BASE_OCCURRENCE_SHA,
                "157em frozen directed base support")


def validate_prefix_B0(row: Any, ei: Any, *, frozen: bool) -> None:
    require(isinstance(row, dict) and set(row) == PREFIX_B0_KEYS and
            isinstance(row["counts"], dict) and
            set(row["counts"]) == PREFIX_COUNT_KEYS and
            isinstance(row["accounting"], dict) and
            set(row["accounting"]) == PREFIX_ACCOUNTING_KEYS and
            isinstance(row["basis_gate"], dict) and
            set(row["basis_gate"]) == PREFIX_BASIS_GATE_KEYS and
            row["fresh_not_imported"] is True and
            row["dependent_event_count"] == len(row["dependent_events"]) and
            row["dependent_event_sha256"] == sha_obj(row["dependent_events"]) and
            _sha256_text(row["pool_order_sha256"]),
            "157em exact B0 prefix shape")
    counts, accounting, pool_public, dag_public = (row["counts"],
        row["accounting"], row["accounting"]["element_pool"],
        row["accounting"]["provenance_DAG"])
    require(set(pool_public) == PREFIX_POOL_KEYS and
            set(pool_public["product_cache"]) == PREFIX_CACHE_KEYS and
            set(pool_public["inverse_cache"]) == PREFIX_CACHE_KEYS and
            set(dag_public) == PREFIX_DAG_KEYS and
            pool_public["packed_width_bytes"] == WIDTH and
            pool_public["size"] == row["prefix_pool_checkpoint"] and
            counts["columns"] == accounting["columns"] and
            counts["pivots"] == accounting["pivots"] and
            counts["dependent_columns"] == accounting["dependent_columns"] and
            counts["live_sparse_entries"] == accounting["live_sparse_entries"] and
            counts["BFS_translations"] == accounting["BFS_translations"] and
            counts["directed_translations"] == accounting["directed_translations"] and
            row["basis_gate"]["pivots"] == counts["pivots"] ==
                row["basis_gate"]["rows"] and
            row["basis_gate"]["least_pivot_coeff_one"] is True and
            row["basis_gate"]["no_preceding_keys"] is True and
            row["basis_gate"]["immutable_during_affine_probes"] is True,
            "157em B0 prefix nested accounting")
    for event in row["dependent_events"]:
        require(isinstance(event, dict) and set(event) == PREFIX_DEPENDENT_KEYS and
                event["support"] == len(event["raw_column"]) and
                event["byte_length"] == len(_semantic_raw_bytes(
                    event["raw_column"])) and
                event["sha256"] == sha_bytes(_semantic_raw_bytes(
                    event["raw_column"])),
                "157em B0 dependent event")
    registry = row["complete_block_registry"]
    require(isinstance(registry, dict) and
            set(registry) == COMPLETE_REGISTRY_KEYS and
            registry["relators_per_translation"] == 11 and
            registry["all_masks_equal_0x7ff"] is True and
            _sha256_text(registry["canonical_translation_sha256"]) and
            registry["semantic_blob_order"] == "exact E4 blob lexicographic" and
            registry["pool_IDs_public"] is False and
            registry["translation_count"] ==
                accounting["total_translation_blocks"],
            "157em complete B0 block registry")
    if frozen:
        require(counts == ei.PREFIX_COUNTS and
                row["prefix_pool_checkpoint"] == 976408 and
                row["dependent_event_count"] == 16 and
                row["dependent_event_sha256"] ==
                    "77ba0632b468c1cb543e1f3eded6c63d52c806686a48e8fa8248de334cebadee" and
                row["source_sha256"] ==
                    "d41123a8c4803f6ac67387ac9bbf1a32f797b90d6233605a5511713f215244be" and
                row["stable_rounds_projection_sha256"] ==
                    ei.PREFIX_STABLE_SHA and
                row["translations_sha256"] == ei.PREFIX_TRANSLATIONS_SHA and
                row["columns_sha256"] == ei.PREFIX_COLUMNS_SHA and
                row["blocker_history_sha256"] == ei.PREFIX_BLOCKERS_SHA and
                registry["translation_count"] == 32975,
                "157em frozen B0 public anchors")


def validate_directed_surgery(row: Any, prefix: dict[str, Any], ei: Any, *,
                              frozen: bool) -> None:
    require(isinstance(row, dict) and set(row) == DIRECTED_SURGERY_KEYS and
            row["round_count"] == len(row["rounds"]) and
            row["translation_count"] == len(row["translations"]) and
            row["rounds_sha256"] == sha_obj(row["rounds"]) and
            row["translations_sha256"] == sha_obj(row["translations"]) and
            row["blocker_history_sha256"] == sha_obj(row["blocker_history"]) and
            row["stable_rounds_projection"] == [
                {key: value for key, value in round_row.items()
                 if key not in {"elapsed_seconds", "RSS_bytes"}}
                for round_row in row["rounds"]] and
            row["stable_rounds_projection_sha256"] ==
                sha_obj(row["stable_rounds_projection"]) and
            row["stable_projection_omits_exactly"] ==
                ["elapsed_seconds", "RSS_bytes"] and
            row["column_order"] ==
                "translation first-seen order, relator 1..11" and
            row["stop_reason"] == "no_new_exact_directed_translation" and
            row["bounded_prefix_sha256"] == sha_obj({
                "translations": row["translations"],
                "columns_sha256": row["columns_sha256"],
                "blockers": row["blocker_history"],
                "rounds": row["rounds"]}) and
            isinstance(row["section_expressions"], dict) and
            isinstance(row["section_oracle"], dict) and
            isinstance(row["theorem"], dict),
            "157em directed surgery exact public")
    require(row["stable_rounds_projection_sha256"] ==
                prefix["stable_rounds_projection_sha256"] and
            row["translations_sha256"] == prefix["translations_sha256"] and
            row["columns_sha256"] == prefix["columns_sha256"] and
            row["blocker_history_sha256"] == prefix["blocker_history_sha256"],
            "157em directed surgery/B0 anchor binding")
    if frozen:
        require(row["round_count"] == 32 and row["translation_count"] == 207 and
                row["column_count"] == 2277 and
                row["stable_rounds_projection_sha256"] == ei.PREFIX_STABLE_SHA and
                row["translations_sha256"] == ei.PREFIX_TRANSLATIONS_SHA and
                row["columns_sha256"] == ei.PREFIX_COLUMNS_SHA and
                row["blocker_history_sha256"] == ei.PREFIX_BLOCKERS_SHA,
                "157em frozen directed surgery anchors")


def validate_fixed_B1_payload(ei: Any, block: Any, anchor: Any, *,
                              frozen: bool) -> None:
    require(isinstance(block, dict) and set(block) == BLOCK_KEYS and
            isinstance(anchor, dict) and set(anchor) == BLOCK_ANCHOR_KEYS and
            block["complete"] is True and block["column_count"] == 11 ==
                len(block["columns"]) and
            block["column_order"] == "relator indices 1 through 11" and
            block["raw_columns_sha256"] ==
                sha_obj([column["raw_column"] for column in block["columns"]]) and
            block["reducer_ledger_sha256"] == sha_obj(block["columns"]),
            "157em fixed B1 block/anchor exact shape")
    for relator, column in enumerate(block["columns"], 1):
        require(set(column) == BLOCK_COLUMN_KEYS and
                column["relator_index"] == relator and
                column["translation_ordinal"] == block["translation_ordinal"] and
                column["translation_hex"] == block["translation_hex"] and
                column["termwise_equals_direct_left_translation"] is True and
                column["quotient_identity"] is True and
                column["D1_D2_zero"] is True and
                isinstance(column["independent"], bool),
                "157em fixed B1 column shape")
        raw = column["raw_column"]
        require(set(raw) == BLOCK_RAW_KEYS and
                raw["entry_count"] == len(raw["entries"]) and
                raw["entries"] == sorted(raw["entries"],
                    key=lambda item: (item[0], bytes.fromhex(item[1]))) and
                raw["byte_length"] == len(_semantic_raw_bytes(raw["entries"])) and
                raw["sha256"] == sha_bytes(_semantic_raw_bytes(raw["entries"])),
                "157em fixed B1 raw column")
        pivot = column["pivot"]
        require((not column["independent"] and pivot is None) or
                (column["independent"] and isinstance(pivot, dict) and
                 set(pivot) == {"component", "element_hex", "reduced_row"} and
                 set(pivot["reduced_row"]) == BLOCK_RAW_KEYS),
                "157em fixed B1 pivot row")
    ei._validate_block_reducer_contract(block["columns"],
        block["old_qstar_scalars"], block["pre_accounting"],
        block["post_accounting"], block["shadow_rank_mod_B0"],
        block["pivot_count_before_relator9"],
        block["pivot_count_after_relator9"], frozen_counts=frozen)
    ei._validate_completed_block_anchor(block, anchor)
    provenance = block["lexfirst_active_provenance"]
    require(set(provenance) == {"component", "relator_index", "scalar",
            "translation_hex", "section_word_sha256"} and
            provenance["translation_hex"] == block["translation_hex"] and
            provenance["relator_index"] == 9 and provenance["scalar"] == 1,
            "157em fixed B1 lex-first provenance")
    if frozen:
        require(block["translation_ordinal"] == 32976 and
                block["translation_hex"] == ei.FIRST_T_HEX and
                block["section_word_sha256"] == ei.FIRST_T_WORD_SHA and
                block["old_qstar_scalars"] == [0]*8+[1, 0, 0] and
                block["rank_gain"] == 11 and
                block["raw_columns_sha256"] == B1["raw_columns_sha256"] and
                block["reducer_ledger_sha256"] == B1["reducer_ledger_sha256"] and
                anchor["anchor_semantic_sha256"] == B1["anchor_semantic_sha256"],
                "157em frozen fixed B1 anchors")


def validate_old_qstar_boundary(row: Any, ei: Any, *, frozen: bool) -> None:
    require(isinstance(row, dict) and set(row) == OLD_QSTAR_KEYS and
            row["used_only_to_freshly_reconstruct_fixed_B1"] is True and
            row["used_after_fixed_B1"] is False and
            type(row["support_count"]) is int and row["support_count"] > 0 and
            _sha256_text(row["support_sha256"]) and
            _sha256_text(row["complete_correlation_sha256"]),
            "157em old qstar exact boundary")
    if frozen:
        require(row["support_count"] == 78 and
                row["complete_correlation_sha256"] == ei.CORRELATION_SHA,
                "157em frozen old qstar reconstruction")


def validate_raw_parent_manifest(row: Any, *, frozen: bool) -> None:
    require(isinstance(row, dict) and set(row) == RAW_PARENT_KEYS and
            row["source_count"] == len(row["rows"]) and
            row["rows_sha256"] == sha_obj(row["rows"]) and
            row["source_word_order"] ==
                "base target6 then registered seeds 1..108" and
            row["signed_offset_convention"] ==
                "positive uses prefix before letter; negative uses prefix after inverse",
            "157em raw parent exact manifest")
    for source, item in enumerate(row["rows"]):
        require(isinstance(item, dict) and set(item) == RAW_PARENT_ROW_KEYS and
                item["source_word_ordinal"] == source and
                type(item["word_length"]) is int and item["word_length"] >= 0 and
                type(item["gradient_entry_count"]) is int and
                item["gradient_entry_count"] >= 0 and
                _sha256_text(item["word_sha256"]) and
                _sha256_text(item["gradient_sha256"]) and
                item["all_nonzero_terms_parented"] is True,
                "157em raw parent row")
    if frozen:
        require(row["source_count"] == 109,
                "157em frozen raw parent dimension")


def validate_initial_target_payload(ei: Any, block: dict[str, Any],
                                    anchor: dict[str, Any], row: Any, *,
                                    frozen: bool) -> None:
    # EI's sealed tiny affine fixture has its own exact target schema and calls
    # the summary commitment ``base_remainder_sha256``.  Production always
    # uses the canonical 109-row public summary field below.
    ledger_key = ("fresh_remainder_sha256" if frozen else
                  "base_remainder_sha256")
    require(isinstance(row, dict) and set(row) == INITIAL_TARGET_KEYS and
            row["fresh_B1_stable_digests_all_equal"] is True and
            row["raw_gradient_count"] == 109 and
            _sha256_text(row["raw_gradients_sha256"]) and
            _sha256_text(row["semantic_remainders_sha256"]) and
            row["semantic_remainders_sha256"] !=
                row["target6"][ledger_key],
            "157em initial target exact wrapper")
    ei._validate_completed_public_shape({"translation_block": block,
        "post_block_anchor": anchor, "target6": row["target6"],
        "affine_system": row["affine_system"]}, fixture=not frozen)
    if frozen:
        require(row["target6"]["fresh_remainder_sha256"] ==
                    B1["fresh_remainders_sha256"] and
                row["target6"]["typed_split_sha256"] == B1["typed_split_sha256"] and
                row["target6"]["direct_gradient_bindings_sha256"] ==
                    B1["direct_bindings_sha256"] and
                row["affine_system"]["row_space_sha256"] ==
                    B1["target_row_space_sha256"] and
                row["affine_system"]["rank"] == B1["rank"] and
                row["affine_system"]["nullity"] == B1["nullity"] and
                row["affine_system"]["equations"] == B1["equations"] and
                row["affine_system"]["consistent"] is False,
                "157em frozen initial target anchors")


def validate_authenticated_frontend(receipt: dict[str, Any], *,
                                    expected: dict[str, Any] | None = None,
                                    frozen: bool) -> None:
    """Close and cross-bind the four authenticated pre-prefix projections.

    ``expected`` is the same-job fresh-object projection supplied immediately
    after construction.  Final receipt validation repeats every closed-schema
    and digest relation without retaining private quotient objects.
    """
    names = ("base_q3_replay", "normalized_inverse_fibre",
             "seed_manifest", "source_preflight")
    present = [bool(receipt.get(name)) for name in names]
    require(present == sorted(present, reverse=True),
            "157em authenticated frontend fill-prefix")
    if expected is not None:
        require(set(expected) == set(names) and
                all(receipt.get(name, {}) == expected[name]
                    for name in names if expected[name]),
                "157em authenticated frontend same-job fresh equality")
    base = receipt.get("base_q3_replay", {})
    if base:
        require(isinstance(base, dict) and set(base) == BASE_Q3_REPLAY_KEYS and
                base["fixed_word"] == [-2, -2, -1, -1, 2, 2, 1, -2,
                    -1, -1, 2, 2, 2, -1, -2, -2, 1, 1, 1, 1] and
                base["roof_exponent"] == 2 and base["roof_order"] == 9 and
                base["arithmetic_outside_by_index_three"] is True and
                base["marking_m"] == 0 and base["lambda"] == 1 and
                isinstance(base["hexagon_residual_words_F2"], list) and
                len(base["hexagon_residual_words_F2"]) == 2 and
                isinstance(base["pentagon_residual_word_PB4"], list) and
                isinstance(base["derived_membership"], dict) and
                base["onto_small_factors"] == {"P_order_504": True,
                    "G9_order_2916": True, "B2_order_27": True} and
                isinstance(base["settled_source_words"], list) and
                len(base["settled_source_words"]) == 6 and
                base["replayed_not_copied"] is True,
                "157em exact authenticated base-q3 replay")
    normalized = receipt.get("normalized_inverse_fibre", {})
    if normalized:
        require(bool(base) and isinstance(normalized, dict) and
                set(normalized) == NORMALIZED_INVERSE_KEYS and
                normalized["normalized_exponent"] == 7 and
                normalized["normalized_roof_order"] == 9 and
                normalized["correction_fibre_size"] == 27 and
                normalized["tested_indices"] == list(range(1, 28)) and
                isinstance(normalized["passing_indices"], list) and
                normalized["passing_indices"] and
                normalized["selected_correction_index"] ==
                    normalized["passing_indices"][0] and
                1 <= normalized["selected_correction_index"] <= 27 and
                normalized["selection_policy"] in {"unique",
                    "deterministic first; full passing set retained"} and
                isinstance(normalized["selected_inverse_words"], list) and
                len(normalized["selected_inverse_words"]) == 6 and
                normalized["max_inverse_word_length"] == max(
                    map(len, normalized["selected_inverse_words"])) and
                normalized["raw_endomorphism_powering_used"] is False and
                normalized["componentwise_Q4_Pi4_inverse_words_combined"]
                    is False,
                "157em exact authenticated normalized inverse")
    seeds = receipt.get("seed_manifest", {})
    if seeds:
        require(bool(normalized) and isinstance(seeds, dict) and
                set(seeds) == SEED_MANIFEST_KEYS and
                seeds["cube_count"] == len(seeds["cube_words"]) == 26 and
                seeds["old_seed_count"] ==
                    len(seeds["old_seed_words"]) == 104 and
                seeds["new_seed_count"] ==
                    len(seeds["new_seed_words"]) == 4 and
                seeds["seed_count"] == len(seeds["seed_words"]) == 108 and
                seeds["seed_words"] ==
                    seeds["old_seed_words"]+seeds["new_seed_words"] and
                seeds["cube_digest_sha256"] == sha_obj(seeds["cube_words"]) and
                seeds["old_seed_digest_sha256"] ==
                    sha_obj(seeds["old_seed_words"]) and
                seeds["new_seed_digest_sha256"] ==
                    sha_obj(seeds["new_seed_words"]) and
                seeds["digest_obj_sha256"] == sha_obj(seeds["seed_words"]) and
                len(seeds["provenance"]) == 108 and
                [row.get("global_index") for row in seeds["provenance"]] ==
                    list(range(1, 109)) and
                seeds["order"] ==
                    "cube first occurrence; [k,x],[x,k],[k,y],[y,k]" and
                seeds["commutator"] == "[a,b]=a^-1*b^-1*a*b" and
                all(seeds[key] is True for key in
                    ("literal_threefold_cube",
                     "four_preregistered_positive_triple_cube_words",
                     "all_E3_identity", "all_exponent_sums_zero",
                     "registered_BFS_not_constructed")),
                "157em exact authenticated seed manifest")
        if frozen:
            ei = load_ei()
            require(seeds["digest_obj_sha256"] == ei.SEED_MANIFEST_SHA,
                    "157em frozen 108-seed manifest")
    source = receipt.get("source_preflight", {})
    if source:
        require(bool(seeds) and isinstance(source, dict) and
                set(source) == SOURCE_PREFLIGHT_KEYS and
                source["supported"] is True and
                source["seed_count"] == len(source["records"]) == 108 and
                source["seed_count"] == seeds["seed_count"] and
                source["contexts_per_seed"] ==
                    source["unique_context_count"] == 31 and
                source["named_use_count"] == 46 and
                source["source_contexts"] == ["source_1", "source_2",
                    "source_3", "source_4", "source_5", "source_6"] and
                source["all_source_tuples_equal"] is True and
                source["all_correction_occurrences_identity"] is True,
                "157em exact authenticated source preflight")
        registry = source["context_registry"]
        require(isinstance(registry, dict) and
                set(registry) == SOURCE_CONTEXT_REGISTRY_KEYS and
                registry["context_count"] ==
                    len(registry["contexts"]) == 31 and
                registry["named_use_count"] ==
                    len(registry["named_uses"]) == 46 and
                registry["context_rows_sha256"] ==
                    sha_obj(registry["contexts"]) and
                registry["named_use_mapping_sha256"] ==
                    sha_obj(registry["named_uses"]) and
                registry["deduplication"] == "exact E4 pair equality" and
                all(set(row) == SOURCE_CONTEXT_ROW_KEYS and
                    row["context_id"] == index and
                    len(bytes.fromhex(row["left_hex"])) == WIDTH and
                    len(bytes.fromhex(row["right_hex"])) == WIDTH
                    for index, row in enumerate(registry["contexts"], 1)) and
                all(set(row) == SOURCE_NAMED_USE_KEYS and
                    isinstance(row["name"], str) and
                    1 <= row["context_id"] <= 31
                    for row in registry["named_uses"]) and
                source["context_registry_sha256"] == sha_obj(registry) and
                source["context_registry_sha256"] ==
                    source["records"][0]["context_registry_sha256"],
                "157em exact source context registry")
        for index, record in enumerate(source["records"], 1):
            require(isinstance(record, dict) and
                    set(record) == SOURCE_PREFLIGHT_RECORD_KEYS and
                    record["seed_index"] == index and
                    record["source_tuple_equal"] is True and
                    record["correction_context_count"] == 31 and
                    record["correction_contexts_sha256"] ==
                        sha_obj(list(range(1, 32))) and
                    record["named_use_count"] == 46 and
                    record["context_registry_unique_count"] == 31 and
                    record["context_registry_sha256"] ==
                        source["context_registry_sha256"],
                    "157em exact source-preflight record")


def validate_stable_prefix_payloads(receipt: dict[str, Any], *,
                                    frozen: bool, ei: Any | None = None) -> None:
    validate_authenticated_frontend(receipt, frozen=frozen)
    fields = ("directed_base_support", "directed_surgery", "prefix_B0",
              "base_columns", "fixed_B1_block", "fixed_B1_anchor",
              "old_qstar_boundary", "raw_parent_manifest", "recovery_map",
              "initial_target")
    if not any(receipt.get(key) for key in fields):
        return
    if ei is None:
        ei = load_ei()
    base = receipt.get("base_columns", {})
    if base:
        validate_base_columns_public(base, frozen=frozen)
    support = receipt.get("directed_base_support", {})
    if support:
        validate_directed_base_support(support, base if base else None,
                                       frozen=frozen)
    prefix = receipt.get("prefix_B0", {})
    if prefix:
        validate_prefix_B0(prefix, ei, frozen=frozen)
    surgery = receipt.get("directed_surgery", {})
    if surgery:
        require(bool(prefix), "157em directed surgery requires B0 public")
        validate_directed_surgery(surgery, prefix, ei, frozen=frozen)
    block, anchor = (receipt.get("fixed_B1_block", {}),
                     receipt.get("fixed_B1_anchor", {}))
    require(bool(block) == bool(anchor), "157em fixed block/anchor co-presence")
    if block:
        validate_fixed_B1_payload(ei, block, anchor, frozen=frozen)
    old_qstar = receipt.get("old_qstar_boundary", {})
    if old_qstar:
        require(bool(block), "157em old qstar requires fixed B1")
        validate_old_qstar_boundary(old_qstar, ei, frozen=frozen)
    parents = receipt.get("raw_parent_manifest", {})
    if parents:
        validate_raw_parent_manifest(parents, frozen=frozen)
    recovery = receipt.get("recovery_map", {})
    if recovery:
        validate_recovery_public(recovery)
    initial = receipt.get("initial_target", {})
    if initial:
        require(bool(block) and bool(parents) and bool(recovery),
                "157em initial target prerequisites")
        validate_initial_target_payload(ei, block, anchor, initial,
                                        frozen=frozen)
    ledger = receipt.get("generation_ledger", [])
    if recovery and ledger and receipt.get("phase") == "complete":
        require(ledger[-1]["basis"]["recovery"] == recovery,
                "157em final recovery/last generation binding")


def validate_receipt(receipt: dict[str, Any], *, allow_unsealed: bool = False) \
        -> None:
    require(set(receipt) == TOP_KEYS and receipt["schema"] == SCHEMA and
            receipt["task_sha256"] == TASK_SHA and
            receipt["pins"] == pin_rows(ROOT/Q3_PATH) and
            receipt["caps"] == CAPS and receipt["caps_sha256"] == sha_obj(CAPS) and
            receipt["algorithm"] == ALGORITHM_PUBLIC and
            receipt["provenance"] == PROVENANCE and
            receipt["upstream_caps_sha256"] == sha_obj(receipt["upstream_caps"]) and
            receipt["theorem_boundary"] == theorem_boundary() and
            receipt["algorithm"]["max_total_new_relator_columns"] ==
                11*receipt["algorithm"]["max_total_new_translation_blocks"] and
            receipt["algorithm"]["monitor_registry_sha256"] == MONITOR_SHA and
            receipt["algorithm"]["upstream_throw_sites_sha256"] ==
                UPSTREAM_THROW_SITES_SHA and
            receipt["algorithm"]["registered_upstream_throw_site_count"] ==
                sum(map(len, UPSTREAM_THROW_SITES.values())),
            "157em exact receipt envelope")
    token = receipt["terminal_token"]
    require(token in TERMINALS and receipt["status"] == token and
            receipt["claims"] == claim_row(token),
            "157em exact terminal/claim")
    if token.endswith("UNKNOWN_INPUT"):
        require(receipt["upstream_caps"] in ({}, EXPECTED_UPSTREAM_CAPS),
                "157em authenticated-stage upstream registry state")
    else:
        require(receipt["upstream_caps"] == EXPECTED_UPSTREAM_CAPS,
                "157em literal reachable upstream registry binding")
    resource = receipt["resource_guards"]
    require(set(resource) == {"resource_hit", "resource",
        "local_and_upstream_separate", "reason_equals_cap_key"} and
        resource["local_and_upstream_separate"] is True and
        resource["reason_equals_cap_key"] is True,
        "157em resource guard schema")
    validate_stable_prefix_payloads(receipt, frozen=not allow_unsealed)
    if token.endswith("UNKNOWN_RESOURCE"):
        detail = resource["resource"]
        require(resource["resource_hit"] is True and isinstance(detail, dict) and
                receipt["reason"] == detail["cap_key"] ==
                    detail["cap_reason"] and
                receipt["selected_proof"] == {} and
                receipt["full_D2_separator"] == {} and
                receipt["packed_block_ledger"] == {} and
                receipt["input_errors"] == [] and
                receipt["partial"].get("phase") == receipt["phase"],
                "157em RESOURCE terminal")
        validate_resource_detail(detail, receipt)
        validate_partial(receipt["partial"], detail)
        validate_resource_current(detail, receipt, receipt["partial"])
        validate_resource_stage_projection(receipt, detail,
            require_external_prefix=not allow_unsealed)
        validate_generation_ledger(receipt["generation_ledger"], token,
            receipt["partial"],
            fixed_block=receipt["fixed_B1_block"] or None,
            fixed_anchor=receipt["fixed_B1_anchor"] or None,
            initial_target=receipt["initial_target"] or None,
            frozen=not allow_unsealed)
        if not allow_unsealed:
            ordered = [
                ("base_q3_replay", ("normalized_inverse_fibre", "seed_manifest",
                    "source_preflight", "directed_base_support",
                    "directed_surgery", "prefix_B0", "base_columns",
                    "fixed_B1_block", "fixed_B1_anchor", "old_qstar_boundary",
                    "raw_parent_manifest", "recovery_map", "initial_target",
                    "generation_ledger")),
                ("source_preflight", ("directed_base_support",
                    "directed_surgery", "prefix_B0", "base_columns",
                    "fixed_B1_block", "fixed_B1_anchor", "old_qstar_boundary",
                    "raw_parent_manifest", "recovery_map", "initial_target",
                    "generation_ledger")),
                ("prefix_B0", ("base_columns", "fixed_B1_block",
                    "fixed_B1_anchor", "old_qstar_boundary",
                    "raw_parent_manifest", "recovery_map", "initial_target",
                    "generation_ledger")),
                ("fixed_B1_block", ("raw_parent_manifest", "recovery_map",
                    "initial_target", "generation_ledger")),
                ("initial_target", ("generation_ledger",)),
            ]
            for prerequisite, later in ordered:
                if not receipt[prerequisite]:
                    require(all(not receipt[key] for key in later),
                            "157em RESOURCE completed-stage prefix")
    elif token.endswith("UNKNOWN_INPUT"):
        require(resource == {"resource_hit": False, "resource": None,
            "local_and_upstream_separate": True,
            "reason_equals_cap_key": True} and
            receipt["reason"] == "authenticated_input_failure" and
            len(receipt["input_errors"]) == 1 and
            isinstance(receipt["input_errors"][0], str) and
            bool(receipt["input_errors"][0]) and receipt["partial"] == {} and
            receipt["selected_proof"] == {} and
            receipt["full_D2_separator"] == {},
            "157em INPUT terminal")
        require(all(receipt[key] in ({}, []) for key in {
            "base_q3_replay", "normalized_inverse_fibre", "seed_manifest",
            "source_preflight", "directed_base_support", "directed_surgery",
            "prefix_B0", "base_columns", "fixed_B1_block",
            "fixed_B1_anchor", "old_qstar_boundary", "raw_parent_manifest",
            "recovery_map", "initial_target", "generation_ledger",
            "packed_block_ledger"}), "157em INPUT has no math payload")
    else:
        require(receipt["phase"] == "complete" and
            receipt["reason"] == TERMINAL_REASONS[token] and
            resource["resource_hit"] is False and resource["resource"] is None and
            receipt["partial"] == {} and receipt["input_errors"] == [],
            "157em normal terminal")
        require((token.endswith("CONSISTENT") and
                 bool(receipt["selected_proof"]) and
                 receipt["full_D2_separator"] == {}) or
                (token.endswith("FULL_D2_OBSTRUCTION") and
                 bool(receipt["full_D2_separator"]) and
                 receipt["selected_proof"] == {}),
                "157em competing terminal exclusion")
        require(all(receipt[key] for key in ("base_q3_replay",
            "normalized_inverse_fibre", "seed_manifest", "source_preflight",
            "directed_base_support", "directed_surgery", "prefix_B0",
            "base_columns", "fixed_B1_block", "fixed_B1_anchor",
            "old_qstar_boundary", "raw_parent_manifest", "recovery_map",
            "initial_target", "generation_ledger", "packed_block_ledger")),
            "157em completed receipt stage payload")
        validate_generation_ledger(receipt["generation_ledger"], token,
            fixed_block=receipt["fixed_B1_block"] or None,
            fixed_anchor=receipt["fixed_B1_anchor"] or None,
            initial_target=receipt["initial_target"] or None,
            frozen=not allow_unsealed)
        require(receipt["generation_ledger"],
                "157em normal terminal has completed generation")
        translations, packed_rows = decode_packed_ledger(
            receipt["packed_block_ledger"])
        active_generations = [row for row in receipt["generation_ledger"]
                              if row["classification"] ==
                                 "ACTIVE_BATCH_COMMITTED"]
        expected_translations = [bytes.fromhex(selected["translation_hex"])
            for generation_row in active_generations
            for selected in generation_row["preflight"][
                "section_provenance"]["selected"]]
        require(translations == expected_translations and
                len(packed_rows) == 11*len(translations),
                "157em packed ledger translation/public binding")
        translation_cursor = 0; record_cursor = 0
        for generation_row in active_generations:
            translation_count = generation_row["commit"]["translation_count"]
            record_count = 11*translation_count
            validate_packed_generation_bindings(generation_row,
                translations[translation_cursor:
                             translation_cursor+translation_count],
                packed_rows[record_cursor:record_cursor+record_count])
            translation_cursor += translation_count
            record_cursor += record_count
        require(translation_cursor == len(translations) and
                record_cursor == len(packed_rows),
                "157em packed ledger complete cursors")
        if token.endswith("CONSISTENT"):
            validate_selected_proof(receipt["selected_proof"])
        else:
            validate_separator(receipt["full_D2_separator"],
                               receipt["generation_ledger"][-1])
    if token.endswith("UNKNOWN_INPUT"):
        require(receipt["reason"] == TERMINAL_REASONS[token],
                "157em INPUT token/reason")
    perf = receipt["performance"]
    require(set(perf) == {"initial_remaining_seconds", "elapsed_seconds",
        "remaining_seconds", "checks", "peak_rss_bytes", "hit_reason",
        "callback_count", "receipt_bytes", "phase_seconds",
        "correlation_pool_intern_calls",
        "correlation_full_sparse_vectors_materialized",
        "full_E4_enumerations", "hard_outer_allowance_seconds"} and
        0 < perf["initial_remaining_seconds"] <= 18000 and
        perf["elapsed_seconds"] >= 0 and 0 <= perf["remaining_seconds"] <=
            perf["initial_remaining_seconds"] and
        type(perf["checks"]) is int and perf["checks"] >= 0 and
        type(perf["callback_count"]) is int and
        perf["callback_count"] == perf["checks"] and
        type(perf["peak_rss_bytes"]) is int and perf["peak_rss_bytes"] >= 0 and
        perf["correlation_pool_intern_calls"] == 0 and
        perf["correlation_full_sparse_vectors_materialized"] == 0 and
        perf["full_E4_enumerations"] == 0 and
        type(perf["receipt_bytes"]) is int and perf["receipt_bytes"] >= 0 and
        isinstance(perf["phase_seconds"], dict) and
        set(perf["phase_seconds"]) == expected_phase_seconds_keys(receipt) and
        all(isinstance(key, str) and isinstance(value, (int, float)) and
            not isinstance(value, bool) and value >= 0
            for key, value in perf["phase_seconds"].items()) and
        sum(perf["phase_seconds"].values()) <= perf["elapsed_seconds"]+2.0 and
        perf["hit_reason"] == (receipt["reason"] if
            token.endswith("UNKNOWN_RESOURCE") else None) and
        perf["hard_outer_allowance_seconds"] == 18000,
        "157em performance schema")
    if not allow_unsealed:
        require(not receipt["algorithm"].get("sealed_bounded_fixture", False),
                "157em production rejects sealed provider")


def convert_foreign_resource(exc: Any, inherited: dict[str, int],
                             phase: str, current: dict[str, Any]) \
        -> LaneResource:
    if isinstance(exc, LaneResource):
        if current and not exc.current:
            exc.current = copy.deepcopy(current)
        return exc
    key = str(getattr(exc, "cap_key", getattr(exc, "key", "")))
    reason = str(getattr(exc, "reason", key))
    limit = int(getattr(exc, "cap_limit", getattr(exc, "limit", -1)))
    observed = int(getattr(exc, "observed_count",
                           getattr(exc, "observed", -1)))
    comparison = str(getattr(exc, "trigger_relation",
                             getattr(exc, "comparator", "gt")))
    require(key in inherited and inherited[key] == limit and reason == key,
            "157em foreign resource closed registry")
    return LaneResource(key, limit, observed, comparison, phase, current,
                        source="upstream",
                        inner=str(getattr(exc, "phase", "")) or key)


def current_anchor_ids(prefix: dict[str, Any]) -> list[int]:
    pool, sections = prefix["pool"], prefix["sections"]
    ids = list(prefix["base_source_key"])
    ids.extend(pool.ids[blob] for blob in sorted(sections.directed_blobs))
    answer = list(dict.fromkeys(ids))
    require(all(0 <= value < len(pool.values) for value in answer),
            "157em current candidate anchors")
    return answer


def neutralize_terminal_generation(receipt: dict[str, Any]) -> None:
    rows = receipt.get("generation_ledger", [])
    if rows and rows[-1].get("classification") in {
            "CONSISTENT", "FULL_D2_OBSTRUCTION"}:
        rows[-1]["classification"] = None


def resource_progress(exc: Any, outer_phase: str) -> dict[str, Any]:
    """Recover the most informative committed-prefix ledger from wrappers."""
    preferred = {
        "source_preflight": ("em_source_current",),
        "fixed_B1": ("ei_block_current", "em_block_current"),
        "initial_target": ("ei_target_current",),
        "block_commit": ("em_block_current",),
        "incremental_reduction": ("em_incremental_current",),
    }.get(outer_phase, ())
    for name in preferred:
        value = getattr(exc, name, None)
        if isinstance(value, dict):
            return copy.deepcopy(value)
    value = getattr(exc, "current", None)
    return copy.deepcopy(value) if isinstance(value, dict) else {}


def run(q3_path: Path, *, seconds: float = 18_000.0) -> dict[str, Any]:
    monitor = Monitor(seconds); phases: dict[str, float] = {}
    phase = "authenticated_input"; started = time.monotonic()
    inherited: dict[str, int] = {}; receipt = base_receipt(q3_path, monitor)
    ledger = PackedBlockLedger(); prefix: dict[str, Any] | None = None
    recovery: RecoveryMap | None = None
    batches = 0; total_blocks = 0; generation = 0
    try:
        ei = load_ei(); eh = ei.load_eh()
        eg = eh.load_v1(); ed = eg.load_ed()
        inherited = upstream_caps(ed, eg)
        receipt = base_receipt(q3_path, monitor, inherited)
        monitor.bind("authenticated_input").check(
            "authenticated_input", force=True)
        require(ei.Q3_PATH == Q3_PATH and ei.Q3_SHA == Q3_SHA,
                "157em q3 predecessor/public pin equality")
        if q3_path.resolve() != (ROOT/Q3_PATH).resolve() or \
                not q3_path.is_file() or q3_path.stat().st_size != Q3_BYTES or \
                sha_file(q3_path) != Q3_SHA:
            raise InputFailure("q3 artifact path/SHA drift")
        try:
            q3, old = ed.authenticated_input(q3_path)
        except ed.AffineInput as exc:
            raise InputFailure(str(exc)) from exc
        e3, e4, _ = old.reconstruct_quotients(q3)
        require(e4.degree == 144 and e4.pc.n == 10 and WIDTH ==
                e4.degree+e4.pc.n, "157em E4 exact width")
        receipt["base_q3_replay"] = old.replay_base_q3(q3, e3, e4)
        normalized, raw_source_key, inverse_words = \
            old.normalized_inverse_fibre(q3, e4)
        receipt["normalized_inverse_fibre"] = normalized
        seed_info = old.affine_seed_words(q3, e3)
        require(len(seed_info["seed_words"]) == 108 and
                sha_obj(seed_info["seed_words"]) == ei.SEED_MANIFEST_SHA,
                "157em exact seed manifest")
        receipt["seed_manifest"] = seed_info
        started = phase_close(phases, phase, started)

        phase = "source_preflight"
        try:
            source = source_preflight(old, seed_info["seed_words"], e4,
                                      raw_source_key, inverse_words, monitor)
        except BaseException as exc:
            if isinstance(exc, (old.ResourceStop, ed.ResourceStop)):
                raise convert_foreign_resource(exc, inherited, phase,
                    resource_progress(exc, phase)) from exc
            raise
        receipt["source_preflight"] = source
        validate_authenticated_frontend(receipt, expected={
            name: copy.deepcopy(receipt[name]) for name in
            ("base_q3_replay", "normalized_inverse_fibre",
             "seed_manifest", "source_preflight")}, frozen=True)
        started = phase_close(phases, phase, started)

        phase = "fresh_B0"; recovery = RecoveryMap(monitor)
        try:
            prefix, dependent = build_prefix_with_recovery(
                old, ed, e4, raw_source_key, monitor, recovery)
        except BaseException as exc:
            if isinstance(exc, (old.ResourceStop, ed.ResourceStop)):
                raise convert_foreign_resource(exc, inherited, phase,
                                               {}) from exc
            raise
        pool = prefix["pool"]
        require(tuple(prefix["raw_source_tuple"]) == tuple(raw_source_key) and
                tuple(pool.value(index) for index in prefix["base_source_key"]) ==
                    tuple(raw_source_key), "157em prefix source anchor")
        prefix_public = ei._prefix_public(old, prefix, dependent, ed)
        require(prefix_public["counts"]["columns"] == 362725 and
                prefix_public["counts"]["pivots"] == 362709 and
                prefix_public["counts"]["dependent_columns"] == 16 and
                prefix_public["counts"]["live_sparse_entries"] == 3090367,
                "157em B0 stable counts")
        prefix_public["complete_block_registry"] = \
            prefix["_em_complete_block_public"]
        validate_prefix_provider(prefix_public, sealed=False)
        receipt["directed_base_support"] = prefix["directed_base_support"]
        receipt["directed_surgery"] = prefix["directed_surgery"]
        receipt["prefix_B0"] = prefix_public
        validate_directed_base_support(
            receipt["directed_base_support"], None, frozen=True)
        validate_prefix_B0(receipt["prefix_B0"], ei, frozen=True)
        validate_directed_surgery(receipt["directed_surgery"],
                                  receipt["prefix_B0"], ei, frozen=True)
        started = phase_close(phases, phase, started)

        phase = "fixed_B1"
        try:
            fixed = construct_fixed_B1(ei, old, ed, eg, e4, prefix,
                                       dependent, recovery, monitor)
        except BaseException as exc:
            foreign_types = tuple(value for value in
                (getattr(old, "ResourceStop", None),
                 getattr(ed, "ResourceStop", None)) if isinstance(value, type))
            if isinstance(exc, foreign_types):
                raise convert_foreign_resource(exc, inherited, phase,
                    resource_progress(exc, phase)) from exc
            raise
        receipt["base_columns"] = fixed["bundle"]["public"]
        receipt["fixed_B1_block"] = fixed["block"]
        receipt["fixed_B1_anchor"] = {k: v for k, v in fixed["anchor"].items()
                                      if not k.startswith("_")}
        receipt["old_qstar_boundary"] = fixed["old_qstar_provenance"]
        validate_base_columns_public(receipt["base_columns"], frozen=True)
        validate_directed_base_support(receipt["directed_base_support"],
                                       receipt["base_columns"], frozen=True)
        validate_fixed_B1_payload(ei, receipt["fixed_B1_block"],
                                  receipt["fixed_B1_anchor"], frozen=True)
        validate_old_qstar_boundary(receipt["old_qstar_boundary"], ei,
                                    frozen=True)
        started = phase_close(phases, phase, started)

        phase = "initial_target"
        try:
            captured = capture_initial_target(ei, old, seed_info, e4, source,
                inverse_words, prefix, fixed["anchor"], monitor)
        except BaseException as exc:
            foreign_types = tuple(value for value in
                (getattr(old, "ResourceStop", None),) if isinstance(value, type))
            if isinstance(exc, foreign_types) or (hasattr(exc, "key") and
                    not isinstance(exc, LaneResource)):
                raise convert_foreign_resource(exc, inherited, phase,
                    resource_progress(exc, phase)) from exc
            raise
        system = captured["system"]; remainders = captured["remainders"]
        raw_gradients = captured["raw_gradients"]
        dual = system.dual_public()
        require(sha_obj(dual) == B1["dual_whole_sha256"] and
                dual["support_sha256"] == B1["dual_support_sha256"] and
                dual["all_108_annihilation_sha256"] ==
                    B1["dual_annihilation_sha256"],
                "157em B1 normalized dual anchors")
        words = target6_words(old, seed_info["seed_words"])
        parent_manifest = add_direct_parents(old, e4, pool, recovery,
                                             words, raw_gradients)
        receipt["raw_parent_manifest"] = parent_manifest
        receipt["recovery_map"] = recovery.public()
        receipt["initial_target"] = {
            "target6": captured["public"]["target6"],
            "affine_system": captured["public"]["affine_system"],
            "semantic_remainders_sha256":
                semantic_remainders_sha256(remainders),
            "fresh_B1_stable_digests_all_equal": True,
            "raw_gradient_count": 109,
            "raw_gradients_sha256": sha_obj([
                semantic_public({(component, element_blob(value)): coefficient
                    for (component, value), coefficient in gradient.items()})
                for gradient in raw_gradients])}
        validate_raw_parent_manifest(receipt["raw_parent_manifest"],
                                     frozen=True)
        validate_recovery_public(receipt["recovery_map"])
        validate_initial_target_payload(ei, receipt["fixed_B1_block"],
            receipt["fixed_B1_anchor"], receipt["initial_target"],
            frozen=True)
        started = phase_close(phases, phase, started)

        prior_raw = list(fixed["block_raw"])
        dependent_raw = fixed["dependent_raw"]
        completed_blocks: set[bytes] = set(prefix["_em_complete_blocks"])
        require(fixed["completed_translation"] not in completed_blocks,
                "157em fixed B1 translation absent from B0 complete blocks")
        completed_blocks.add(fixed["completed_translation"])
        cumulative = {"pass1": 0, "pass2": 0}
        generation = 1
        current_target = target_public(system, remainders, generation)
        static = captured["static"]; base_raw = captured["base_raw"]
        fixed_base_columns = base_raw_columns(old, e4)
        while True:
            generation_row: dict[str, Any] = {"generation": generation,
                "basis": {**state_accounting(prefix, pool_digest=False),
                          "recovery": recovery.public()},
                "target": current_target, "raw_lambda": {},
                "correlation": {}, "preflight": {}, "commit": {},
                "incremental": {}, "classification": None}
            receipt["generation_ledger"].append(generation_row)
            if system.consistent:
                phase = "selected_proof"
                anchor = {"_ids": current_anchor_ids(prefix)}
                try:
                    selected = ei._selected_proof(old, e4, inverse_words,
                        seed_info["seed_words"], base_raw, prefix, anchor,
                        system, static, monitor)
                except BaseException as exc:
                    if isinstance(exc, getattr(old, "ResourceStop")):
                        raise convert_foreign_resource(exc, inherited, phase,
                            {"generation": generation,
                             "completed_target": True}) from exc
                    raise
                receipt["selected_proof"] = selected
                generation_row["classification"] = "CONSISTENT"
                started = phase_close(
                    phases, f"selected_proof_g{generation}", started)
                receipt["terminal_token"] = receipt["status"] = \
                    "B345_E4_D2_COLGEN_TARGET6_CONSISTENT"
                receipt["reason"] = \
                    "registered_108_target6_consistent_mod_generated_D2"
                break

            phase = "dual_lift"
            raw_lambda = RawLambda(old, prefix, system, remainders,
                dependent_raw, prior_raw, monitor)
            require(all(recovery.contains(int(row[0]), bytes.fromhex(row[1]))
                        for row in raw_lambda.support_rows),
                    "157em every raw-lambda support has recovery parent")
            generation_row["raw_lambda"] = raw_lambda.public
            started = phase_close(phases, f"dual_lift_g{generation}", started)

            phase = "correlation_pass1"
            remaining = CAPS["total_new_translation_blocks"]-total_blocks
            selection_budget = 0 if batches == \
                CAPS["column_generation_batches"] else remaining
            correlation = complete_correlation(e4, pool,
                raw_lambda.support_rows, fixed["bundle"]["private_occurrences"],
                monitor, generation, cumulative, selection_budget)
            require_active_not_completed(
                correlation["active"], completed_blocks)
            generation_row["correlation"] = correlation["public"]
            started = phase_close(phases, f"correlation_g{generation}", started)
            if not correlation["active"]:
                generation_row["classification"] = "FULL_D2_OBSTRUCTION"
                receipt["full_D2_separator"] = {
                    "generation": generation,
                    "raw_lambda": raw_lambda.public,
                    "correlation": correlation["public"],
                    "active_row_count": 0,
                    "complete_76_occurrence_full_11_relator_correlation": True,
                    "annihilates_full_D2": True,
                    "lambda_delta_all_zero": True,
                    "lambda_base_z": 2,
                    "registered_108_family_only": True,
                    "pinned_E4_roof_only": True}
                receipt["terminal_token"] = receipt["status"] = \
                    "B345_E4_D2_COLGEN_TARGET6_FULL_D2_OBSTRUCTION"
                receipt["reason"] = "complete_full_D2_correlation_zero"
                break
            enforce_generation_capacity(
                remaining, batches, generation, total_blocks)
            require(correlation["selected"],
                    "157em ACTIVE correlation selects nonempty batch")
            require(not set(correlation["selected"]).intersection(
                        completed_blocks),
                    "157em ACTIVE translation cannot have complete D2 block")

            phase = "section_recovery"
            section_stage = recover_selected_sections(old, e4, prefix,
                recovery, words, fixed["bundle"]["private_occurrences"],
                correlation, monitor, generation)
            phase = "batch_precompute"
            staged = stage_batch(old, e4, prefix,
                fixed["bundle"]["private_occurrences"],
                fixed_base_columns, raw_lambda, correlation,
                section_stage, monitor, generation)
            generation_row["preflight"] = staged["public"]
            started = phase_close(phases, f"preflight_g{generation}", started)

            phase = "block_commit"
            committed = commit_batch(old, e4, prefix, recovery, words,
                fixed["bundle"]["private_occurrences"], correlation, staged,
                ledger, monitor, generation, completed_blocks)
            generation_row["commit"] = committed["public"]
            count = len(correlation["selected"]); batches += 1
            total_blocks += count
            require(total_blocks <= 4096 and ledger.record_count ==
                    total_blocks*11 and ledger.translation_count == total_blocks,
                    "157em cumulative block/column caps")
            prior_raw.extend(row["raw"] for row in staged["rows"])
            started = phase_close(phases, f"commit_g{generation}", started)

            phase = "incremental_reduction"
            anchors = current_anchor_ids(prefix)
            remainders, incremental = incremental_remainders(old, prefix,
                remainders, committed["new_pivots"],
                committed["new_pivot_keys"],
                committed["public"]["pre_accounting"]["pivots"], raw_gradients,
                anchors, monitor, generation)
            generation_row["incremental"] = incremental
            started = phase_close(phases, f"incremental_g{generation}", started)
            generation_row["classification"] = "ACTIVE_BATCH_COMMITTED"
            generation += 1
            phase = "target_resolve"
            system, solve_public = solve_from_remainders(
                ei, old, e4, remainders, monitor, generation)
            current_target = target_public(system, remainders, generation)
            require(solve_public["affine_system"]["row_space_sha256"] ==
                    current_target["row_space_sha256"],
                    "157em target resolve public equality")
            started = phase_close(phases, f"target_g{generation}", started)

        phase = "receipt_serialization"
        receipt["packed_block_ledger"] = ledger.public(monitor)
        receipt["recovery_map"] = recovery.public()
        receipt["phase"] = "complete"
        receipt["claims"] = claim_row(receipt["terminal_token"])
        started = phase_close(phases, phase, started)
        phase = "complete"
    except InputFailure as exc:
        receipt = base_receipt(q3_path, monitor, inherited)
        receipt["terminal_token"] = receipt["status"] = \
            "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT"
        receipt["reason"] = "authenticated_input_failure"
        receipt["phase"] = "authenticated_input"
        receipt["claims"] = claim_row(receipt["terminal_token"])
        receipt["input_errors"] = [str(exc)]
    except LaneResource as exc:
        exc.current = resource_progress(exc, exc.phase)
        if exc.phase == "receipt_serialization" and not exc.current:
            exc.current = {
                "completed_terminal_before_serialization":
                    receipt["terminal_token"],
                "packed_block_ledger_prefix": ledger.partial_public(),
                "serialization_phase_completed": False}
        monitor.hit_reason = exc.key
        neutralize_terminal_generation(receipt)
        receipt["terminal_token"] = receipt["status"] = \
            "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_RESOURCE"
        receipt["reason"] = exc.key; receipt["phase"] = exc.phase
        receipt["claims"] = claim_row(receipt["terminal_token"])
        receipt["resource_guards"] = {"resource_hit": True,
            "resource": resource_public(exc),
            "local_and_upstream_separate": True,
            "reason_equals_cap_key": True}
        receipt["partial"] = {"phase": exc.phase, "reason": exc.key,
            "current": copy.deepcopy(exc.current),
            "completed_generation_count": sum(row.get("classification") ==
                "ACTIVE_BATCH_COMMITTED" for row in
                receipt["generation_ledger"]),
            "completed_batch_count": batches,
            "completed_new_translation_block_count": ledger.translation_count,
            "current_generation": generation or None,
            "packed_block_ledger_prefix": ledger.partial_public(),
            "selected_proof": None, "full_D2_separator": None}
        receipt["selected_proof"] = {}; receipt["full_D2_separator"] = {}
        receipt["packed_block_ledger"] = {}
    except BaseException as foreign:
        if not (hasattr(foreign, "cap_key") or hasattr(foreign, "key")):
            raise
        current = resource_progress(foreign, phase)
        exc = convert_foreign_resource(foreign, inherited, phase, current)
        monitor.hit_reason = exc.key
        neutralize_terminal_generation(receipt)
        receipt["terminal_token"] = receipt["status"] = \
            "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_RESOURCE"
        receipt["reason"] = exc.key; receipt["phase"] = exc.phase
        receipt["claims"] = claim_row(receipt["terminal_token"])
        receipt["resource_guards"] = {"resource_hit": True,
            "resource": resource_public(exc),
            "local_and_upstream_separate": True,
            "reason_equals_cap_key": True}
        receipt["partial"] = {"phase": exc.phase, "reason": exc.key,
            "current": copy.deepcopy(exc.current),
            "completed_generation_count": sum(row.get("classification") ==
                "ACTIVE_BATCH_COMMITTED" for row in
                receipt["generation_ledger"]),
            "completed_batch_count": batches,
            "completed_new_translation_block_count": ledger.translation_count,
            "current_generation": generation or None,
            "packed_block_ledger_prefix": ledger.partial_public(),
            "selected_proof": None, "full_D2_separator": None}
        receipt["selected_proof"] = {}; receipt["full_D2_separator"] = {}
        receipt["packed_block_ledger"] = {}
    receipt["performance"] = performance_public(monitor, phases)
    validate_receipt(receipt)
    return receipt


def canonical_bytes(receipt: dict[str, Any]) -> bytes:
    for _ in range(16):
        raw = (json.dumps(receipt, sort_keys=True,
            separators=(",", ":"))+"\n").encode("utf-8")
        if receipt["performance"]["receipt_bytes"] == len(raw):
            return raw
        receipt["performance"]["receipt_bytes"] = len(raw)
    raise RuntimeError("157em receipt byte fixed point")


def serialization_fallback(receipt: dict[str, Any], observed: int) \
        -> dict[str, Any]:
    answer = copy.deepcopy(receipt)
    old_token = answer["terminal_token"]
    neutralize_terminal_generation(answer)
    packed = answer.get("packed_block_ledger", {})
    require(isinstance(packed, dict) and set(packed) == PACKED_LEDGER_KEYS,
            "157em serialization fallback starts from full packed ledger")
    packed_prefix = {"format": "complete-D2-block-ledger/v1-partial",
        "translation_count": packed["translation_count"],
        "translation_decoded_bytes": packed["translation_decoded_bytes"],
        "translation_sha256": packed["translation_sha256"],
        "record_bytes": packed["record_bytes"],
        "record_count": packed["record_count"],
        "decoded_bytes": packed["decoded_bytes"],
        "decoded_sha256": packed["decoded_sha256"],
        "base64_omitted_for_resource_partial": True}
    answer["terminal_token"] = answer["status"] = \
        "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_RESOURCE"
    answer["reason"] = "packed_receipt_bytes"
    answer["phase"] = "receipt_serialization"
    answer["claims"] = claim_row(answer["terminal_token"])
    stop = LaneResource("packed_receipt_bytes", CAPS["packed_receipt_bytes"],
        observed, "gt", "receipt_serialization",
        {"completed_terminal_before_serialization": old_token,
         "packed_block_ledger_prefix": packed_prefix,
         "serialization_phase_completed": True})
    answer["resource_guards"] = {"resource_hit": True,
        "resource": resource_public(stop),
        "local_and_upstream_separate": True,
        "reason_equals_cap_key": True}
    answer["partial"] = {"phase": "receipt_serialization",
        "reason": "packed_receipt_bytes", "current": stop.current,
        "completed_generation_count": sum(row.get("classification") ==
            "ACTIVE_BATCH_COMMITTED" for row in
            answer["generation_ledger"]),
        "completed_batch_count": sum(row.get("classification") ==
            "ACTIVE_BATCH_COMMITTED" for row in
            answer["generation_ledger"]),
        "completed_new_translation_block_count":
            int(packed_prefix.get("translation_count", 0)),
        "current_generation": (answer["generation_ledger"][-1]["generation"]
            if answer["generation_ledger"] else None),
        "packed_block_ledger_prefix": packed_prefix,
        "selected_proof": None, "full_D2_separator": None}
    answer["packed_block_ledger"] = {}
    answer["selected_proof"] = {}; answer["full_D2_separator"] = {}
    answer["input_errors"] = []
    answer["performance"]["hit_reason"] = "packed_receipt_bytes"
    answer["performance"]["receipt_bytes"] = 0
    validate_receipt(answer)
    return answer


def write_checked(path: Path, receipt: dict[str, Any]) \
        -> tuple[dict[str, Any], bytes]:
    raw = canonical_bytes(receipt)
    if len(raw) > CAPS["packed_receipt_bytes"]:
        receipt = serialization_fallback(receipt, len(raw))
        raw = canonical_bytes(receipt)
    require(len(raw) <= CAPS["packed_receipt_bytes"],
            "157em fallback receipt fits cap")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+".tmp")
    temporary.write_bytes(raw); os.replace(temporary, path)
    require(path.read_bytes() == raw and sha_file(path) == sha_bytes(raw),
            "157em checked write/readback")
    validate_receipt(receipt)
    return receipt, raw


def self_test() -> None:
    """Bounded shared-core fixtures; no q3, GAP, or full prefix."""
    authenticate_static(); trace: dict[str, int] = {}
    mutation_count = 0

    def expect_failure(call: Callable[[], Any], label: str) -> None:
        nonlocal mutation_count
        try:
            call()
        except Exception:
            mutation_count += 1; return
        raise RuntimeError("157em mutation accepted: " + label)

    # The frozen v1 self-test supplies every inherited source marker exactly
    # once.  Reuse its already authenticated EI module instead of re-running
    # EI or colliding with the fixed module name.
    v1 = load_v1_fixture(); v1.self_test()
    ei = getattr(v1, "_EI", None)
    require(ei is not None and
            Path(ei.__file__).resolve() == (ROOT/EI_PRODUCER).resolve() and
            Path(ei.__file__).stat().st_size == EI_PRODUCER_BYTES and
            sha_file(Path(ei.__file__)) == EI_PRODUCER_SHA,
            "157en inherited v1 EI module reuse")
    global _EI
    _EI = ei
    eh = ei.load_eh(); eg = eh.load_v1()
    ed = eh.loaded_ed_fixture_module(eg)
    old = loaded_old_fixture_module(ed)
    old_again = loaded_old_fixture_module(ed)
    require(old_again is old,
            "157en repeated old fixture load preserves module identity")
    saved_old_binding = sys.modules[SELFTEST_OLD_MODULE]
    wrong_old_binding = types.ModuleType(SELFTEST_OLD_MODULE)
    wrong_old_binding.__file__ = old.__file__
    wrong_old_binding.__spec__ = old.__spec__
    wrong_old_binding.SCHEMA = old.SCHEMA
    sys.modules[SELFTEST_OLD_MODULE] = wrong_old_binding
    try:
        expect_failure(lambda: loaded_old_fixture_module(ed),
            "old fixture wrong-bound module")
        require(sys.modules.get(SELFTEST_OLD_MODULE) is wrong_old_binding,
                "157en wrong-bound rejection does not overwrite/delete")
    finally:
        sys.modules[SELFTEST_OLD_MODULE] = saved_old_binding
    require(sys.modules.get(SELFTEST_OLD_MODULE) is old,
            "157en exact old fixture binding restored")
    trace["old_module_lifecycle"] = 3
    require(not hasattr(ed, "load_old") and hasattr(ed, "CAPS") and
            hasattr(ed, "UPSTREAM_RESOURCE_CAPS") and
            callable(getattr(ed, "authenticated_input", None)) and
            callable(getattr(eg, "upstream_caps", None)) and
            Path(old.__file__).resolve() == (ROOT/ed.OLD_PRODUCER).resolve() and
            sha_file(Path(old.__file__)) == ed.OLD_PRODUCER_SHA,
            "157em producer/checker predecessor API separation")

    # Closed authenticated front-end fixture.  It exercises the same
    # production validator but contains no q3 object or production basis.
    context_rows = [{"context_id": index,
        "left_hex": bytes(WIDTH).hex(), "right_hex": bytes(WIDTH).hex()}
        for index in range(1, 32)]
    named_uses = [{"name": f"fixture_context_{index}",
        "context_id": (index-1) % 31+1} for index in range(1, 47)]
    context_registry = {"context_count": 31, "contexts": context_rows,
        "named_uses": named_uses, "named_use_count": 46,
        "named_use_mapping_sha256": sha_obj(named_uses),
        "context_rows_sha256": sha_obj(context_rows),
        "deduplication": "exact E4 pair equality"}
    seed_words_fixture = [[index+1] for index in range(108)]
    old_seed_fixture, new_seed_fixture = (seed_words_fixture[:104],
                                          seed_words_fixture[104:])
    early_fixture = {
        "base_q3_replay": {"fixed_word": list(old.FIXED_WORD),
            "roof_exponent": 2, "roof_order": 9,
            "arithmetic_outside_by_index_three": True, "marking_m": 0,
            "lambda": 1, "hexagon_residual_words_F2": [[], []],
            "pentagon_residual_word_PB4": [], "derived_membership": {},
            "onto_small_factors": {"P_order_504": True,
                "G9_order_2916": True, "B2_order_27": True},
            "settled_source_words": [[] for _ in range(6)],
            "replayed_not_copied": True},
        "normalized_inverse_fibre": {"source": "fixture",
            "normalized_exponent": 7, "normalized_roof_order": 9,
            "normalized_power_row": {}, "correction_fibre_size": 27,
            "tested_indices": list(range(1, 28)), "passing_indices": [1],
            "selection_policy": "unique", "selected_correction_index": 1,
            "selected_correction_word": [],
            "selected_inverse_candidate_word": [],
            "selected_inverse_words": [[] for _ in range(6)],
            "max_inverse_word_length": 0,
            "raw_endomorphism_powering_used": False,
            "componentwise_Q4_Pi4_inverse_words_combined": False},
        "seed_manifest": {"cube_words": [[index] for index in range(26)],
            "cube_count": 26, "old_seed_words": old_seed_fixture,
            "old_seed_count": 104, "new_seed_words": new_seed_fixture,
            "new_seed_count": 4, "seed_words": seed_words_fixture,
            "seed_count": 108,
            "old_seed_digest_sha256": sha_obj(old_seed_fixture),
            "new_seed_digest_sha256": sha_obj(new_seed_fixture),
            "digest_obj_sha256": sha_obj(seed_words_fixture),
            "cube_digest_sha256": sha_obj([[index] for index in range(26)]),
            "triple4_manifest": [], "provenance": [
                {"global_index": index} for index in range(1, 109)],
            "order": "cube first occurrence; [k,x],[x,k],[k,y],[y,k]",
            "commutator": "[a,b]=a^-1*b^-1*a*b",
            "literal_threefold_cube": True,
            "four_preregistered_positive_triple_cube_words": True,
            "all_E3_identity": True, "all_exponent_sums_zero": True,
            "registered_BFS_not_constructed": True},
        "source_preflight": {"supported": True, "seed_count": 108,
            "contexts_per_seed": 31, "unique_context_count": 31,
            "context_registry_sha256": sha_obj(context_registry),
            "named_use_count": 46, "context_registry": context_registry,
            "records": [{"seed_index": index,
                "source_tuple_equal": True,
                "correction_context_count": 31,
                "correction_contexts_sha256": sha_obj(list(range(1, 32))),
                "named_use_count": 46, "context_registry_unique_count": 31,
                "context_registry_sha256": sha_obj(context_registry)}
                for index in range(1, 109)],
            "source_contexts": [f"source_{index}" for index in range(1, 7)],
            "all_source_tuples_equal": True,
            "all_correction_occurrences_identity": True}}
    early_receipt = {name: copy.deepcopy(value)
                     for name, value in early_fixture.items()}
    validate_authenticated_frontend(early_receipt,
        expected=early_fixture, frozen=False)
    for name, mutation in (
            ("base_q3_replay", lambda row: row.__setitem__("extra", True)),
            ("normalized_inverse_fibre", lambda row: row.pop("source")),
            ("seed_manifest", lambda row: row.__setitem__("seed_count", 107)),
            ("source_preflight", lambda row: row.__setitem__(
                "named_use_count", 45))):
        bad = copy.deepcopy(early_receipt); mutation(bad[name])
        expect_failure(lambda bad=bad: validate_authenticated_frontend(
            bad, expected=early_fixture, frozen=False),
            "authenticated frontend " + name)
    trace["authenticated_frontend"] = 4

    prefix_projection_fixture = {key: object() for key in EG_PREFIX_KEYS}
    prefix_projection_fixture.update({key: object()
                                      for key in EM_PREFIX_PRIVATE_KEYS})
    expect_failure(lambda: require(
        set(prefix_projection_fixture) == EG_PREFIX_KEYS,
        "fixture direct full-prefix rejection"),
        "157eg direct full private-prefix shape")
    projected_fixture = exact_eg_prefix_projection(prefix_projection_fixture)
    require(set(projected_fixture) == EG_PREFIX_KEYS and all(
            projected_fixture[key] is prefix_projection_fixture[key]
            for key in EG_PREFIX_KEYS),
            "157em production prefix projection fixture")
    trace["exact_157eg_prefix_projection"] = 1

    inherited = upstream_caps(ed, eg)
    expected_upstream_keys = (OLD_REACHABLE_RESOURCE_CAPS |
        OLD_AFFINE_REACHABLE_RESOURCE_CAPS | ED_REACHABLE_RESOURCE_CAPS |
        EG_REACHABLE_RESOURCE_CAPS)
    require(set(inherited) == set(expected_upstream_keys) and
            inherited == EXPECTED_UPSTREAM_CAPS and
            "transaction_trace_records" not in inherited and
            "blocker_table" not in inherited and
            "missing_bounded_inverse_representative" not in inherited and
            set(UPSTREAM_THROW_SITES) == set(inherited),
            "157em selftest exact reachable upstream caps")

    # Independent literal call-tree fixture.  Keep this separate from the
    # production registry builder so an accidental broad union, dormant key,
    # wrong outer phase, or wrong progress shape cannot validate itself.
    expected_sites: set[tuple[str, str, str, str]] = set()

    def fixture_sites(keys: Iterable[str], outer: str, shape: str, *,
                      inner: str | None = None) -> None:
        for key in keys:
            expected_sites.add((key, outer,
                                key if inner is None else inner, shape))

    fixture_sites({"element_pool", "section_slp_nodes",
        "directed_section_expr_nodes", "directed_section_expr_edges",
        "provenance_dag_nodes", "provenance_dag_edges",
        "total_sparse_group_ring_keys", "single_sparse_elimination_row",
        "target_elimination_support", "sparse_pivot_rows"},
        "fresh_B0", "empty")
    fixture_sites({"raw_lambda_recursion_edges"}, "fixed_B1", "empty",
        inner="raw_lambda_reverse_dp")
    fixture_sites({"pair_attempts", "distinct_correlation_candidates"},
        "fixed_B1", "fixed_correlation_pair", inner="dual_correlation")
    fixture_sites({"packed_active_rows"}, "fixed_B1",
        "fixed_correlation_post", inner="dual_correlation")
    fixture_sites({"directed_section_expr_nodes",
        "directed_section_expr_edges", "single_word_or_section_length"},
        "fixed_B1", "empty")
    fixture_sites({"single_word_or_section_length",
        "directed_unique_translations", "element_pool",
        "target_elimination_support", "provenance_dag_nodes",
        "provenance_dag_edges", "total_sparse_group_ring_keys",
        "single_sparse_elimination_row", "sparse_pivot_rows"},
        "fixed_B1", "fixed_block")
    fixture_sites({"single_word_or_section_length",
        "wordexpr_nodes_per_candidate", "wordexpr_edges_per_candidate",
        "wordexpr_flat_leaves_per_candidate",
        "wordexpr_expanded_letter_count_per_target",
        "candidate_live_gradient_entries_total", "element_pool",
        "target_elimination_support", "affine_rows",
        "dual_provenance_entries"},
        "initial_target", "initial_target")
    fixture_sites({"target_live_remainders"}, "initial_target",
        "initial_target", inner="target_reduction")
    fixture_sites({"directed_section_expr_nodes",
        "directed_section_expr_edges"}, "section_recovery", "empty")
    fixture_sites({"single_word_or_section_length"}, "section_recovery",
        "section_node")
    fixture_sites({"directed_section_expr_nodes",
        "directed_section_expr_edges", "directed_unique_translations",
        "element_pool", "provenance_dag_nodes", "provenance_dag_edges",
        "total_sparse_group_ring_keys", "single_sparse_elimination_row",
        "sparse_pivot_rows"}, "block_commit", "block")
    fixture_sites({"element_pool", "target_elimination_support"},
        "incremental_reduction", "incremental")
    fixture_sites({"affine_rows", "target_live_remainders",
        "dual_provenance_entries"}, "target_resolve", "empty")
    fixture_sites({"single_word_or_section_length",
        "wordexpr_nodes_per_candidate", "wordexpr_edges_per_candidate",
        "wordexpr_flat_leaves_per_candidate",
        "candidate_live_gradient_entries_total", "element_pool",
        "target_elimination_support", "provenance_dag_nodes",
        "provenance_dag_edges"}, "selected_proof", "selected")
    actual_sites = {(key, outer, inner, shape)
                    for key, rows in UPSTREAM_THROW_SITES.items()
                    for outer, inner, shape in rows}
    require(actual_sites == expected_sites,
            "157em exact upstream symbol-level throw-site fixture")
    trace["upstream_throw_site_exact"] = 1

    class ForeignStop:
        cap_key = reason = "raw_lambda_recursion_edges"
        cap_limit = inherited[cap_key]; observed_count = cap_limit+1
        trigger_relation = "gt"; phase = "raw_lambda_reverse_dp"

    converted = convert_foreign_resource(
        ForeignStop(), inherited, "fixed_B1", {})
    require(converted.source == "upstream" and
            converted.key == ForeignStop.cap_key,
            "157em honest reachable upstream conversion")

    class ForeignGeStop:
        cap_key = reason = "element_pool"
        cap_limit = inherited[cap_key]; observed_count = cap_limit
        trigger_relation = "ge"; phase = "element_pool"

    converted_ge = convert_foreign_resource(
        ForeignGeStop(), inherited, "fresh_B0", {})
    require(converted_ge.source == "upstream" and
            converted_ge.comparator == "ge",
            "157em honest upstream ge comparator")
    wrong_outer = ForeignGeStop()
    expect_failure(lambda: convert_foreign_resource(
        wrong_outer, inherited, "selected_proof", {}),
        "cap-key-preserving upstream outer swap")
    wrong_inner = ForeignGeStop(); wrong_inner.phase = \
        "wordexpr_nodes_per_candidate"
    expect_failure(lambda: convert_foreign_resource(
        wrong_inner, inherited, "fresh_B0", {}),
        "cap-key-preserving upstream inner swap")
    wrong_current = ForeignGeStop()
    expect_failure(lambda: convert_foreign_resource(
        wrong_current, inherited, "fresh_B0", {"node": 0}),
        "cap-key-preserving upstream current-shape swap")
    dormant_fresh = ForeignGeStop()
    dormant_fresh.cap_key = dormant_fresh.reason = \
        "directed_unique_translations"
    dormant_fresh.cap_limit = inherited[dormant_fresh.cap_key]
    dormant_fresh.phase = dormant_fresh.cap_key
    expect_failure(lambda: convert_foreign_resource(
        dormant_fresh, inherited, "fresh_B0", {}),
        "fresh-B0 dormant directed-unique throw site")
    dormant_incremental = ForeignGeStop()
    dormant_incremental.cap_key = dormant_incremental.reason = \
        "provenance_dag_nodes"
    dormant_incremental.cap_limit = inherited[dormant_incremental.cap_key]
    dormant_incremental.observed_count = dormant_incremental.cap_limit+1
    dormant_incremental.trigger_relation = "gt"
    dormant_incremental.phase = dormant_incremental.cap_key
    expect_failure(lambda: convert_foreign_resource(
        dormant_incremental, inherited, "incremental_reduction", {}),
        "incremental dormant provenance-DAG throw site")
    wrong_relation = ForeignGeStop(); wrong_relation.trigger_relation = "gt"
    expect_failure(lambda: convert_foreign_resource(
        wrong_relation, inherited, "fresh_B0", {}),
        "upstream comparator relation")
    bad_foreign = ForeignStop(); bad_foreign.cap_key = bad_foreign.reason = \
        "transaction_trace_records"
    expect_failure(lambda: convert_foreign_resource(
        bad_foreign, inherited, "fresh_B0", {}),
        "unreachable upstream cap key")
    stale_foreign = ForeignStop(); stale_foreign.cap_limit -= 1
    expect_failure(lambda: convert_foreign_resource(
        stale_foreign, inherited, "fixed_B1", {}),
        "stale upstream cap limit")

    scope_monitor = Monitor(30.0)
    scope_monitor.bind("authenticated_input").check(
        "authenticated_input", force=True)
    expect_failure(lambda: scope_monitor.bind("receipt_serialization").check(
        "affine_remainder", force=True),
        "receipt serialization wrong affine callback")
    expect_failure(lambda: scope_monitor.bind("selected_proof").check(
        "affine_transposed_row_absorption", force=True),
        "selected proof wrong affine callback")
    expect_failure(lambda: scope_monitor.bind("batch_precompute").reserve(
        "proof_DAG_array_bytes", 0),
        "batch precompute wrong proof callback")
    require(MONITOR_PUBLIC["receipt_serialization"] ==
                ["receipt_serialization"] and
            "flat_left_fox" not in {inner for rows in MONITOR_PUBLIC.values()
                                      for inner in rows},
            "157em exact callsite monitor registry")
    cadence_blob = bytes(WIDTH)
    cadence_direct = RecoveryMap(scope_monitor)
    cadence_direct.candidates = 4095
    cadence_direct.consider_direct(1, cadence_blob, 0, 1)
    for cadence_phase in ("fresh_B0", "fixed_B1"):
        cadence_recovery = RecoveryMap(scope_monitor)
        cadence_recovery.candidates = 4095
        cadence_recovery.translated_candidates = 4095
        cadence_recovery.preflight_translated(
            [(1, cadence_blob, cadence_blob, 1, 1, cadence_blob)],
            phase=cadence_phase)
    expect_failure(lambda: scope_monitor.bind("fresh_B0").check(
        "initial_target", force=True), "recovery wrong outer callback")
    trace["recovery_4096_monitor_pairs"] = 1
    trace["resource_registry"] = 1; trace["monitor_pair_registry"] = 1

    sealed = {"sealed_bounded_fixture": True,
        "fresh_immutable_prefix": False, "columns": 23, "pivots": 19,
        "production_stable_digest_imported": False,
        "mathematical_claim": "none"}
    validate_prefix_provider(sealed, sealed=True, trace=trace)
    for key, value in (("fresh_immutable_prefix", True),
                       ("columns", 362725), ("pivots", 362709),
                       ("production_stable_digest_imported", True),
                       ("mathematical_claim", "B1")):
        bad = dict(sealed); bad[key] = value
        expect_failure(lambda row=bad: validate_prefix_provider(
            row, sealed=True), "sealed provider " + key)

    def label(value: int, component: int = 1) -> tuple[int, bytes]:
        return component, bytes([value])*WIDTH

    p1, p2, free = label(1), label(2), label(3)
    pivots = [(p1, {p1: 1, p2: 1, free: 2}),
              (p2, {p2: 1, free: 1})]
    lifted, edges, zero = reverse_lift_core(
        pivots, {free: 1}, trace=trace)
    require(edges == 3 and zero == [0, 0] and
            dot_semantic(lifted, pivots[0][1]) == 0 and
            dot_semantic(lifted, pivots[1][1]) == 0,
            "157em toy reverse lift/direct dot")
    expect_failure(lambda: reverse_lift_core(
        list(reversed(pivots)), {free: 1}), "reverse pivot order")
    expect_failure(lambda: reverse_lift_core(
        pivots, {p1: 1}), "pivot in public support")
    expect_failure(lambda: reverse_lift_core(
        [pivots[0], pivots[0]], {free: 1}), "duplicate pivot")
    expect_failure(lambda: reverse_lift_core(
        [(p2, {p2: 1, p1: 1})], {free: 1}), "nonstrict/cycle tail")
    expect_failure(lambda: reverse_lift_core(
        pivots, {free: 1}, edge_cap=1), "reverse edge cap")
    expect_failure(lambda: reverse_lift_core(
        pivots, {free: 1}, support_cap=1), "support cap")
    expect_failure(lambda: reverse_lift_core(
        pivots, {free: 1}, source_kind="old_support_one_qstar"),
        "old-qstar substitution")

    class ToyPC:
        n = 10

    class ToyE4:
        degree = 144
        pc = ToyPC()

        def __init__(self) -> None:
            identity = tuple(range(144)); self.identity = (identity, (0,)*10)
            cycle = list(identity); cycle[:13] = [*range(1, 13), 0]
            swap = list(identity); swap[:3] = [1, 0, 2]
            self.generators = [(tuple(cycle), (0,)*10),
                (tuple(swap), (0,)*10)] + [self.identity]*4
            self.inverse_generators = [self.inverse(value)
                                       for value in self.generators]

        def mul(self, left: Any, right: Any) -> Any:
            return (tuple(left[0][right[0][index]] for index in range(144)),
                    (0,)*10)

        def inverse(self, value: Any) -> Any:
            inverse = [0]*144
            for index, image in enumerate(value[0]): inverse[image] = index
            return tuple(inverse), (0,)*10

        def eval(self, word: Sequence[int]) -> Any:
            value = self.identity
            for letter in word:
                generator = (self.generators[letter-1] if letter > 0 else
                             self.inverse_generators[-letter-1])
                value = self.mul(value, generator)
            return value

    class ToyPool:
        def __init__(self, quotient: Any) -> None:
            self.quotient = quotient; self.width = WIDTH
            self.identity_id = 0; self.values = [element_blob(quotient.identity)]
            self.ids = {self.values[0]: 0}

        def pack(self, value: Any) -> bytes: return element_blob(value)
        def unpack(self, blob: bytes) -> Any:
            require(len(blob) == WIDTH, "157em toy pool width")
            return tuple(blob[:144]), tuple(blob[144:])
        def blob(self, identifier: int) -> bytes: return self.values[identifier]
        def value(self, identifier: int) -> Any:
            return self.unpack(self.values[identifier])
        def intern(self, value: Any) -> int:
            blob = self.pack(value); found = self.ids.get(blob)
            if found is not None: return found
            identifier = len(self.values); self.values.append(blob)
            self.ids[blob] = identifier; return identifier
        def pivot_order(self, packed: int) -> tuple[int, bytes]:
            component, identifier = ToyOld.unpack_vector_key(packed)
            return component, self.blob(identifier)
        def checkpoint(self) -> int: return len(self.values)
        def rollback(self, checkpoint: int) -> int:
            removed = len(self.values)-checkpoint
            for identifier in range(len(self.values)-1, checkpoint-1, -1):
                blob = self.values[identifier]
                require(self.ids.get(blob) == identifier,
                        "157em toy pool rollback binding")
                del self.ids[blob]
            del self.values[checkpoint:]
            return removed

    e4 = ToyE4(); toy_pool = ToyPool(e4); toy_monitor = Monitor(30.0)
    g, h = e4.generators[:2]
    correct = translation_from_pair(e4, g, h)
    wrong = [e4.mul(e4.inverse(h), g), e4.mul(e4.inverse(g), h),
             e4.mul(h, e4.inverse(g))]
    require(len({element_blob(correct), *(element_blob(value) for value in wrong)})
            == 4, "157em nonabelian orientation witnesses distinct")
    for value in wrong:
        expect_failure(lambda value=value: require(e4.mul(value, h) == g,
            "wrong left action"), "inverse/right orientation")

    expressions = old.SectionExpressionDAG(toy_pool)
    g_root = expressions.flat([1, 2], element_blob(e4.eval([1, 2])),
                              "fixture_g")
    h_root = expressions.flat([2], element_blob(h), "fixture_h")
    inverse_root = expressions.inverse(h_root, "fixture_inverse_h")
    t_root = expressions.product(g_root, inverse_root, "fixture_t")
    materialize_trace: dict[str, int] = {}
    word = owned_materialize(old, e4, expressions, t_root, toy_monitor,
                             "section_recovery", trace=materialize_trace)
    require(element_blob(e4.eval(word)) == expressions.value_blob(t_root) and
            materialize_trace == {"owned_inverse": 1},
            "157em owned inverse/materializer production path")
    saved = int(expressions.left[inverse_root])
    expressions.left[inverse_root] = g_root
    expect_failure(lambda: owned_materialize(old, e4, expressions, t_root,
        toy_monitor, "section_recovery"), "inverse child mutation")
    expressions.left[inverse_root] = saved

    occurrences = [
        {"relator_index": 1, "occurrence_ordinal": 1, "term_ordinal": 1,
         "component": 1, "coefficient": 1,
         "element_hex": element_blob(e4.identity).hex(), "_value": e4.identity},
        {"relator_index": 1, "occurrence_ordinal": 2, "term_ordinal": 2,
         "component": 1, "coefficient": 2,
         "element_hex": element_blob(h).hex(), "_value": h},
        {"relator_index": 2, "occurrence_ordinal": 3, "term_ordinal": 1,
         "component": 1, "coefficient": 1,
         "element_hex": element_blob(g).hex(), "_value": g},
        {"relator_index": 3, "occurrence_ordinal": 4, "term_ordinal": 1,
         "component": 2, "coefficient": 2,
         "element_hex": element_blob(h).hex(), "_value": h},
    ]
    support = [[1, element_blob(g).hex(), 1],
               [1, element_blob(h).hex(), 2],
               [2, element_blob(g).hex(), 1]]
    cumulative = {"pass1": 0, "pass2": 0}
    corr = complete_correlation(e4, toy_pool, support, occurrences,
                                toy_monitor, 1, cumulative, 2)
    brute: dict[tuple[bytes, int], int] = {}
    for component, g_hex, lam in support:
        gv = toy_pool.unpack(bytes.fromhex(g_hex))
        for occurrence in occurrences:
            if occurrence["component"] != component: continue
            tv = translation_from_pair(e4, gv, occurrence["_value"])
            key = (element_blob(tv), occurrence["relator_index"])
            brute[key] = (brute.get(key, 0)+lam*occurrence["coefficient"]) % 3
    brute_active = sorted((t, j, value) for (t, j), value in brute.items()
                          if value)
    require(corr["active"] == brute_active and
            corr["public"]["pass1_pair_attempts"] == 7 and
            corr["public"]["pass2_pair_attempts"] == 7 and
            corr["public"]["selected_translation_count"] <= 2 and
            set(corr["contributors"]) == set(corr["selected"]),
            "157em optimized/brute nonabelian correlation")
    corr_all = complete_correlation(e4, toy_pool, support, occurrences,
        toy_monitor, 2, {"pass1": 0, "pass2": 0}, 100)
    require(corr_all["public"]["selected_truncated"] is False,
            "157em all ACTIVE below cap")
    for mutation in ("active_packed_sha256", "pass1_pair_attempts",
                     "pass2_pair_attempts", "selected_translation_sha256"):
        bad = copy.deepcopy(corr["public"]); bad[mutation] = None
        expect_failure(lambda bad=bad: require(bad == corr["public"],
            "correlation fixture exact"), "correlation " + mutation)

    packed = PackedBlockLedger(); translation = corr["selected"][0]
    packed.add_translation(translation)
    packed.add_record(1, 1, 1, 1, True, (1, element_blob(g)),
                      "11"*32, "22"*32)
    packed.add_record(1, 1, 2, 0, False, None, "33"*32, "44"*32)
    packed_public = packed.public(toy_monitor)
    decoded_t, decoded_rows = decode_packed_ledger(packed_public)
    require(decoded_t == [translation] and len(decoded_rows) == 2 and
            decoded_rows[0]["pivot_component"] == 1 and
            decoded_rows[1]["pivot_component"] == 0,
            "157em packed 225-byte roundtrip")
    raw = bytearray(base64.b64decode(packed_public["base64"])); raw[4] |= 0x10
    bad = copy.deepcopy(packed_public)
    bad["base64"] = base64.b64encode(raw).decode("ascii")
    bad["base64_length"] = len(bad["base64"])
    bad["base64_sha256"] = sha_bytes(bad["base64"].encode("ascii"))
    bad["decoded_sha256"] = sha_bytes(bytes(raw))
    expect_failure(lambda: decode_packed_ledger(bad), "packed unused flags")
    bad = copy.deepcopy(packed_public); bad["record_bytes"] = 226
    expect_failure(lambda: decode_packed_ledger(bad), "packed padding/width")
    bad = copy.deepcopy(packed_public); bad["record_endianness"] = "big"
    expect_failure(lambda: decode_packed_ledger(bad), "packed endian")

    # The adaptive lane's own shared recovery/staging/commit/incremental path
    # is exercised on a sealed 109-row prefix.  Main has no provider switch;
    # these adapters exist only inside self_test.
    class ToyDag:
        def __init__(self) -> None:
            self.node_count = 0; self.edge_count = 0
            self.max_nodes = 0; self.max_edges = 0
            self.deadline: Any = None
        def checkpoint(self) -> tuple[int, int]:
            return self.node_count, self.edge_count
        def rollback(self, checkpoint: tuple[int, int]) -> None:
            self.node_count, self.edge_count = checkpoint

    class ToySections:
        EXPR_TAG = 1 << 31

        def __init__(self, pool: Any) -> None:
            self.pool = pool; self.expressions = old.SectionExpressionDAG(pool)
            self.by_blob: dict[bytes, int] = {}; self.directed_blobs: set[bytes] = set()
            self.directed_roots: dict[bytes, int] = {}
            self.base_prefix_roots: dict[Any, int] = {}
            self.parent: list[int] = []; self.by_element: dict[int, int] = {}

        def register_directed(self, value: Any, root: int) -> tuple[int, bool]:
            blob = self.pool.pack(value); expected = self.EXPR_TAG+root
            prior = self.by_blob.get(blob)
            if prior is not None:
                require(prior == expected, "157em fixture exact section reuse")
                return prior, False
            self.pool.intern(value); self.by_blob[blob] = expected
            self.directed_blobs.add(blob); self.directed_roots[blob] = root
            return expected, True

        def node_for(self, identifier: int) -> int:
            return self.by_blob[self.pool.blob(identifier)]

    class ToyOld:
        CAPS = old.CAPS
        SectionExpressionDAG = old.SectionExpressionDAG
        reduce_word = staticmethod(old.reduce_word)
        inv_word = staticmethod(old.inv_word)

        @staticmethod
        def pack_vector_key(component: int, identifier: int) -> int:
            return identifier*8+component-1

        @staticmethod
        def unpack_vector_key(key: int) -> tuple[int, int]:
            return key % 8+1, key//8

        @staticmethod
        def pure_relations(rank: int) -> list[list[int]]:
            require(rank == 4, "157em fixture rank")
            return [[] for _ in range(11)]

        @staticmethod
        def translate_vector(vector: dict[Any, int], translation: Any,
                             quotient: Any) -> dict[Any, int]:
            return {(component, quotient.mul(translation, value)): coefficient
                    for (component, value), coefficient in vector.items()}

        @staticmethod
        def d1(vector: dict[Any, int], quotient: Any) -> dict[Any, int]:
            return {}

        @staticmethod
        def _affine_probe_remainder(raw: dict[Any, int], prefix: dict[str, Any],
                                    anchors: Sequence[int], adapter: Any) \
                -> dict[tuple[int, str], int]:
            del anchors; pool0, basis0 = prefix["pool"], prefix["basis"]
            vector: dict[int, int] = {}
            for (component, value), coefficient in raw.items():
                blob = pool0.pack(value)
                require(blob in pool0.ids,
                        "157em fixture fresh probe cannot intern")
                vector[ToyOld.pack_vector_key(component,
                                               pool0.ids[blob])] = coefficient
            while vector:
                pivot = min(vector, key=pool0.pivot_order)
                prior = basis0.rows.get(pivot)
                if prior is None: break
                factor = vector[pivot]
                for key, coefficient in prior[0].items():
                    value = (vector.get(key, 0)-factor*coefficient) % 3
                    if value: vector[key] = value
                    else: vector.pop(key, None)
            return {(component, pool0.blob(identifier).hex()): coefficient
                    for key, coefficient in vector.items()
                    for component, identifier in [ToyOld.unpack_vector_key(key)]}

    toy_old = ToyOld()
    toy_sections = ToySections(toy_pool)
    toy_recovery = RecoveryMap(toy_monitor)
    toy_dag = ToyDag()

    def power_word(exponent: int) -> list[int]:
        return [1]*exponent

    exponents = [1, 2, 3, 4, 5, 6, 7, 8, 0, 9, 10]
    fixture_occurrences: list[dict[str, Any]] = []
    for relator, exponent in enumerate(exponents, 1):
        h_value = e4.eval(power_word(exponent)); h_blob = element_blob(h_value)
        h_root = toy_sections.expressions.flat(power_word(exponent), h_blob,
            f"fixture_base_{relator}")
        fixture_occurrences.append({"relator_index": relator,
            "occurrence_ordinal": relator, "term_ordinal": 1,
            "component": 1, "coefficient": 1,
            "element_hex": h_blob.hex(), "section_word": power_word(exponent),
            "section_expression_root": h_root, "_value": h_value})

    def decode_fixture_semantic_blob(value_blob: Any) -> Any:
        """Sealed adapter from staged semantic bytes to a ToyPool Element."""
        require(type(value_blob) is bytes and len(value_blob) == WIDTH,
                "157em fixture staged semantic blob shape")
        value = toy_pool.unpack(value_blob)
        require(toy_pool.pack(value) == value_blob,
                "157em fixture staged semantic blob roundtrip")
        return value

    decoder_mutations_before = mutation_count
    expect_failure(lambda: decode_fixture_semantic_blob(e4.generators[0]),
        "typed Element passed in staged blob position")
    require(mutation_count == decoder_mutations_before+1,
            "157em fixture blob-decoder mutation count")

    class ToyBasis:
        def __init__(self) -> None:
            self.pool = toy_pool; self.sections = toy_sections
            self.rows: dict[int, tuple[dict[int, int], int]] = {}
            self.columns_seen = 0; self.dependent_columns = 0
            self.live_vector_entries = 0
            self.max_vector_support = 0; self.max_transient_vector_support = 0
            self.elimination_operations = 0; self.pivot_introductions: list[Any] = []
            self.deadline: Any = None; self.pending: list[dict[Any, int]] = []
            self.fail_after_relator: int | None = None
            self.complete_masks: dict[bytes, int] = {}

        def add_column(self, relator: int, translation_id: int,
                       section_node: int, translation_ordinal: int = 0) -> None:
            del section_node, translation_ordinal
            require(self.pending, "157em fixture staged row queue")
            semantic = self.pending.pop(0); t_blob = self.pool.blob(translation_id)
            occurrence = fixture_occurrences[relator-1]
            g = e4.mul(self.pool.value(translation_id), occurrence["_value"])
            edge = (1, self.pool.pack(g), t_blob, relator, 1,
                    bytes.fromhex(occurrence["element_hex"]))
            phase0 = getattr(self, "_em_recovery_phase", "block_commit")
            toy_recovery.preflight_translated([edge], phase=phase0)
            vector: dict[int, int] = {}
            for (component, value_blob), coefficient in semantic.items():
                value = decode_fixture_semantic_blob(value_blob)
                identifier = self.pool.intern(value)
                vector[ToyOld.pack_vector_key(component, identifier)] = coefficient
            while vector:
                pivot = min(vector, key=self.pool.pivot_order)
                prior = self.rows.get(pivot)
                if prior is None: break
                factor = vector[pivot]
                for key, coefficient in prior[0].items():
                    value = (vector.get(key, 0)-factor*coefficient) % 3
                    if value: vector[key] = value
                    else: vector.pop(key, None)
            self.columns_seen += 1
            if vector:
                pivot = min(vector, key=self.pool.pivot_order)
                inverse = 1 if vector[pivot] == 1 else 2
                vector = {key: value*inverse % 3
                          for key, value in vector.items() if value*inverse % 3}
                self.rows[pivot] = (vector, 0)
                self.live_vector_entries += len(vector)
                self.max_vector_support = max(self.max_vector_support,
                                              len(vector))
            else:
                self.dependent_columns += 1
            toy_recovery.apply_translated_prechecked(*edge)
            record_complete_block_relator(
                self.complete_masks, t_blob, relator)
            if self.fail_after_relator == relator:
                raise LaneResource("batch_staged_sparse_entries",
                    CAPS["batch_staged_sparse_entries"],
                    CAPS["batch_staged_sparse_entries"]+1, "gt",
                    "block_commit", {"fixture_after_basis_mutation": True})

    toy_basis = ToyBasis()
    toy_prefix = {"pool": toy_pool, "basis": toy_basis,
        "dag": toy_dag, "sections": toy_sections,
        "_em_complete_block_masks": toy_basis.complete_masks}
    t_value = e4.generators[0]; t_blob = element_blob(t_value)
    words = [[1, 1]] + [[] for _ in range(108)]
    require(prefix_word_at(toy_old, words[0], 2) == [1] and
            e4.eval(prefix_word_at(toy_old, words[0], 2)) == t_value,
            "157em positive-letter prefix-before-offset fixture")
    offset_mutations_before = mutation_count
    wrong_offset_recovery = RecoveryMap(toy_monitor)
    wrong_offset_recovery.consider_direct(1, t_blob, 0, 1)
    expect_failure(lambda: recovery_expression_root(toy_old, toy_prefix,
        wrong_offset_recovery, words, fixture_occurrences, 1, t_blob,
        "fixture_wrong_positive_offset"),
        "positive-letter offset1 identity versus generator")
    require(mutation_count == offset_mutations_before+1,
            "157em positive-prefix mutation count")
    toy_recovery.consider_direct(1, t_blob, 0, 2)
    base_columns = [{(1, row["_value"]): 1}
                    for row in fixture_occurrences]

    class ToyLambda:
        values = {(1, t_blob): 1}

    scalar_map = {(t_blob, relator): (1 if relator == 9 else 0)
                  for relator in range(1, 12)}
    fixture_correlation = {"selected": [t_blob], "jstar": {t_blob: 9},
        "scalar_map": scalar_map,
        "public": {"selected_translation_count": 1,
            "selected_translation_sha256": sha_bytes(t_blob),
            "selected_bindings_sha256": sha_obj([[t_blob.hex(), 9, 1]]),
            "first_active": {"translation_hex": t_blob.hex(),
                "relator_index": 9, "scalar": 1}}}
    fixture_contributor_raw = contributor_record(
        1, t_blob, 1, fixture_occurrences[8])
    fixture_expression_payload, fixture_expression_renumber = \
        expressions.serialize_reachable(
            [t_root], toy_monitor.bind("section_recovery"))
    fixture_selected = [{"generation": 1, "translation_ordinal": 1,
        "translation_hex": t_blob.hex(), "jstar": 9,
        "correlation_scalar": 1,
        "contributor": {"component": 1, "g_hex": t_blob.hex(),
            "lambda_coefficient": 1, "relator_index": 9,
            "occurrence_ordinal": 9,
            "h_hex": element_blob(e4.identity).hex(), "base_coefficient": 1,
            "translation_hex": t_blob.hex(),
            "record_hex": fixture_contributor_raw.hex(),
            "record_sha256": sha_bytes(fixture_contributor_raw)},
        "g_recovery": {"kind": "direct_target_source_prefix",
            "component": 1, "element_hex": t_blob.hex(),
            "source_word_ordinal": 0, "signed_letter_offset": 2,
            "method": "target_word_signed_prefix", "word_length": 1,
            "word_sha256": sha_obj([1])},
        "materialization_canary": {"word_length": 1,
            "word_sha256": sha_obj([1]), "value_hex": t_blob.hex()},
        "expression_root": fixture_expression_renumber[t_root]}]
    fixture_section_stage = {"selected": fixture_selected, "selected_count": 1,
        "selected_sha256": sha_obj(fixture_selected),
        "expression_DAG": fixture_expression_payload,
        "owned_inverse_materializer": True,
        "materialization_cadence": "first,last,and-every-64th",
        "all_values_exact": True,
        "_private": {t_blob: {"g_word": [1], "h_word": [],
            "component": 1, "g_hex": t_blob.hex(),
            "h_hex": element_blob(e4.identity).hex()}}}
    staged = stage_batch(toy_old, e4, toy_prefix, fixture_occurrences,
        base_columns, ToyLambda(), fixture_correlation,
        fixture_section_stage, toy_monitor, 1)
    toy_basis.pending = [dict(row["raw"]) for row in staged["rows"]]
    fixture_ledger = PackedBlockLedger()
    committed = commit_batch(toy_old, e4, toy_prefix, toy_recovery, words,
        fixture_occurrences, fixture_correlation, staged, fixture_ledger,
        toy_monitor, 1, set())
    raw_gradients = [{(1, t_value): 1} for _ in range(109)]
    before_remainders = [{(1, t_blob.hex()): 1} for _ in range(109)]
    semantic_fixture_digest = semantic_remainders_sha256(before_remainders)
    updated, update_public = incremental_remainders(toy_old, toy_prefix,
        before_remainders, committed["new_pivots"],
        committed["new_pivot_keys"],
        committed["public"]["pre_accounting"]["pivots"], raw_gradients,
        [toy_pool.identity_id], toy_monitor, 1)
    recovery_public = toy_recovery.public()
    require(staged["public"]["column_count"] == 11 and
            committed["public"]["column_count"] == 11 and
            committed["public"]["first_translation_jstar_pivot"]["relator"] == 9 and
            fixture_ledger.translation_count == 1 and
            fixture_ledger.record_count == 11 and all(not row for row in updated) and
            len(update_public["fresh_direct_cadence"]) == 4 and
            recovery_public["raw_coordinate_parent_entry_count"] == 1 and
            recovery_public["translated_candidate_edge_count"] == 11 and
            recovery_public["candidate_edge_count"] == 12 and
            isinstance(update_public["reduction_order_sha256"], str) and
            update_public["completed_quotient_pivot_ordinal"] ==
                len(committed["new_pivots"]),
            "157em recovery/stage/commit/incremental shared pipeline")
    validate_preflight(staged["public"], 1, fixture_correlation["public"])
    # A Pass-2 contributor is one lexicographically selected summand, not the
    # combined Pass-1 scalar.  Two scalar-1 terms may therefore produce an
    # aggregate scalar 2 while the canonical contributor remains scalar 1.
    aggregate_preflight = copy.deepcopy(staged["public"])
    aggregate_selected = aggregate_preflight["section_provenance"]["selected"]
    aggregate_selected[0]["correlation_scalar"] = 2
    aggregate_preflight["section_provenance"]["selected_sha256"] = \
        sha_obj(aggregate_selected)
    aggregate_correlation = copy.deepcopy(fixture_correlation["public"])
    aggregate_correlation["selected_bindings_sha256"] = sha_obj(
        [[t_blob.hex(), 9, 2]])
    aggregate_correlation["first_active"]["scalar"] = 2
    validate_preflight(aggregate_preflight, 1, aggregate_correlation)
    wrong_aggregate = copy.deepcopy(aggregate_correlation)
    wrong_aggregate["selected_bindings_sha256"] = sha_obj(
        [[t_blob.hex(), 9, 1]])
    expect_failure(lambda: validate_preflight(
        aggregate_preflight, 1, wrong_aggregate),
        "Pass1 aggregate distinct from canonical contributor term")
    trace["contributor_aggregate_split"] = 1
    cross_count = copy.deepcopy(fixture_correlation["public"])
    cross_count["selected_translation_count"] += 1
    expect_failure(lambda: validate_preflight(
        staged["public"], 1, cross_count), "correlation/preflight count")
    cross_hash = copy.deepcopy(fixture_correlation["public"])
    cross_hash["selected_bindings_sha256"] = "0"*64
    expect_failure(lambda: validate_preflight(
        staged["public"], 1, cross_hash), "correlation/preflight hash")
    cross_jstar = copy.deepcopy(fixture_correlation["public"])
    cross_jstar["first_active"]["relator_index"] = 8
    expect_failure(lambda: validate_preflight(
        staged["public"], 1, cross_jstar), "correlation/preflight jstar")
    cross_translation = copy.deepcopy(staged["public"])
    cross_translation["section_provenance"]["selected"][0][
        "translation_hex"] = element_blob(e4.identity).hex()
    expect_failure(lambda: validate_preflight(
        cross_translation, 1, fixture_correlation["public"]),
        "correlation/preflight translation")
    validate_commit(committed["public"], 1, staged["public"],
                    expected_recovery_edges_per_translation=11)
    validate_incremental(update_public, 1, committed["public"])
    fixture_packed_public = fixture_ledger.public(toy_monitor)
    fixture_packed_translations, fixture_packed_rows = \
        decode_packed_ledger(fixture_packed_public)
    fixture_packed_generation = {"generation": 1,
        "preflight": staged["public"], "commit": committed["public"]}
    validate_packed_generation_bindings(fixture_packed_generation,
        fixture_packed_translations, fixture_packed_rows)
    bad_packed_rows = copy.deepcopy(fixture_packed_rows)
    bad_packed_rows[0]["raw_sha256"] = "0"*64
    expect_failure(lambda: validate_packed_generation_bindings(
        fixture_packed_generation, fixture_packed_translations,
        bad_packed_rows), "packed preflight row-binding mutation")

    basis1 = copy.deepcopy(committed["public"]["pre_accounting"])
    basis1["pool_order_sha256"] = None
    basis2 = copy.deepcopy(committed["public"]["post_accounting"])
    basis2["pool_order_sha256"] = None
    target1 = {"generation": 1, "variables": 108, "equations": 1,
        "rank": 1, "nullity": 107, "consistent": False,
        "row_space_sha256": "91"*32,
        "remainders_sha256": semantic_fixture_digest,
        "dual": {"fixture": "dual-one"}}
    target2 = {**target1, "generation": 2,
        "remainders_sha256": update_public["post_update_remainder_sha256"]}
    chain_rows = [{"generation": 1, "basis": basis1, "target": target1,
        "preflight": staged["public"], "commit": committed["public"],
        "incremental": update_public},
        {"generation": 2, "basis": basis2, "target": target2,
         "preflight": {}, "commit": {}, "incremental": {}}]
    chain_fixed = {"post_accounting": {
        **copy.deepcopy(committed["public"]["pre_accounting"]),
        "recovery": None}}
    chain_anchor = {"basis_columns": basis1["columns"],
        "basis_pivots": basis1["pivots"],
        "basis_dependent": basis1["dependent"],
        "basis_live_sparse_entries": basis1["live_sparse_entries"],
        "pool_size": basis1["pool_size"], "DAG_nodes": basis1["DAG_nodes"],
        "DAG_edges": basis1["DAG_edges"],
        "section_bindings": basis1["section_bindings"]}
    chain_initial = {"affine_system": {"variables": 108, "equations": 1,
        "rank": 1, "nullity": 107, "consistent": False,
        "row_space_sha256": "91"*32, "dual_witness": {"fixture": "dual-one"}},
        "target6": {"fresh_remainder_sha256":
            "a5"*32},
        "semantic_remainders_sha256": semantic_fixture_digest}
    require(semantic_fixture_digest ==
                update_public["pre_update_remainder_sha256"] and
            semantic_fixture_digest !=
                chain_initial["target6"]["fresh_remainder_sha256"],
            "157en semantic and public-summary commitments are distinct")
    validate_generation_cross_bind(chain_rows, fixed_block=chain_fixed,
        fixed_anchor=chain_anchor, initial_target=chain_initial)
    fixture_chain_initial = copy.deepcopy(chain_initial)
    fixture_chain_initial["target6"]["base_remainder_sha256"] = \
        fixture_chain_initial["target6"].pop("fresh_remainder_sha256")
    validate_generation_cross_bind(chain_rows, fixed_block=chain_fixed,
        fixed_anchor=chain_anchor, initial_target=fixture_chain_initial,
        frozen=False)
    expect_failure(lambda: validate_generation_cross_bind(chain_rows,
        fixed_block=chain_fixed, fixed_anchor=chain_anchor,
        initial_target=fixture_chain_initial), "sealed base-only summary key")
    expect_failure(lambda: validate_generation_cross_bind(chain_rows,
        fixed_block=chain_fixed, fixed_anchor=chain_anchor,
        initial_target=chain_initial, frozen=False),
        "fixture fresh-only summary key")
    both_summary_keys = copy.deepcopy(chain_initial)
    both_summary_keys["target6"]["base_remainder_sha256"] = "b5"*32
    expect_failure(lambda: validate_generation_cross_bind(chain_rows,
        fixed_block=chain_fixed, fixed_anchor=chain_anchor,
        initial_target=both_summary_keys), "both target summary keys")
    neither_summary_key = copy.deepcopy(chain_initial)
    neither_summary_key["target6"].pop("fresh_remainder_sha256")
    expect_failure(lambda: validate_generation_cross_bind(chain_rows,
        fixed_block=chain_fixed, fixed_anchor=chain_anchor,
        initial_target=neither_summary_key), "neither target summary key")
    trace["summary_key_modes"] = 2
    trace["summary_key_mutations"] = 4
    bad_initial = copy.deepcopy(chain_initial)
    bad_initial["semantic_remainders_sha256"] = \
        bad_initial["target6"]["fresh_remainder_sha256"]
    expect_failure(lambda: validate_generation_cross_bind(chain_rows,
        fixed_block=chain_fixed, fixed_anchor=chain_anchor,
        initial_target=bad_initial), "semantic digest replaced by ledger digest")
    bad_initial = copy.deepcopy(chain_initial)
    bad_initial["target6"]["fresh_remainder_sha256"] = \
        bad_initial["semantic_remainders_sha256"]
    expect_failure(lambda: validate_generation_cross_bind(chain_rows,
        fixed_block=chain_fixed, fixed_anchor=chain_anchor,
        initial_target=bad_initial), "ledger digest replaced by semantic digest")
    altered_remainders = copy.deepcopy(before_remainders)
    altered_remainders[0][(1, t_blob.hex())] = 2
    bad_initial = copy.deepcopy(chain_initial)
    bad_initial["semantic_remainders_sha256"] = \
        semantic_remainders_sha256(altered_remainders)
    expect_failure(lambda: validate_generation_cross_bind(chain_rows,
        fixed_block=chain_fixed, fixed_anchor=chain_anchor,
        initial_target=bad_initial), "semantic coordinate mutation")
    ordered_remainders = [{} for _ in range(109)]
    ordered_remainders[0] = {(1, t_blob.hex()): 1}
    ordered_remainders[1] = {(1, t_blob.hex()): 2}
    permuted_remainders = copy.deepcopy(ordered_remainders)
    permuted_remainders[0], permuted_remainders[1] = \
        permuted_remainders[1], permuted_remainders[0]
    require(semantic_remainders_sha256(ordered_remainders) !=
                semantic_remainders_sha256(permuted_remainders),
            "157en semantic row order commitment")
    bad_chain = copy.deepcopy(chain_rows)
    bad_chain[1]["target"]["remainders_sha256"] = "0"*64
    expect_failure(lambda: validate_generation_cross_bind(bad_chain,
        fixed_block=chain_fixed, fixed_anchor=chain_anchor,
        initial_target=chain_initial), "stale next-generation remainder")
    bad_chain = copy.deepcopy(chain_rows)
    bad_chain[0]["commit"]["pre_accounting"]["recovery"][
        "canonical_sha256"] = "0"*64
    expect_failure(lambda: validate_generation_cross_bind(bad_chain,
        fixed_block=chain_fixed, fixed_anchor=chain_anchor,
        initial_target=chain_initial), "commit pre recovery representation")
    trace["generation_cross_bind"] = 1
    trace["packed_generation_bindings"] = 1
    trace["semantic_remainder_binding_mutations"] = 4
    incremental_current = {key: copy.deepcopy(update_public[key])
                           for key in INCREMENTAL_PROGRESS_KEYS
                           if key != "remaining_rows"}
    incremental_current["rolled_back_on_failure"] = True
    incremental_current["remaining_rows"] = [None]*109

    class ForeignIncrementalStop:
        cap_key = reason = "element_pool"
        cap_limit = inherited[cap_key]; observed_count = cap_limit
        trigger_relation = "ge"; phase = "element_pool"

    foreign_incremental = ForeignIncrementalStop()
    setattr(foreign_incremental, "em_incremental_current",
            copy.deepcopy(incremental_current))
    recovered_incremental = resource_progress(
        foreign_incremental, "incremental_reduction")
    converted_incremental = convert_foreign_resource(
        foreign_incremental, inherited, "incremental_reduction",
        recovered_incremental)
    _validate_incremental_progress(converted_incremental.current)
    require(converted_incremental.inner == "element_pool" and
            converted_incremental.source == "upstream",
            "157em honest foreign incremental resource progress")
    trace["incremental_foreign_progress"] = 1
    for payload, validator, label in (
            (staged["public"], lambda value: validate_preflight(
                value, 1, fixture_correlation["public"]),
             "preflight nested key"),
            (committed["public"], lambda value: validate_commit(
                value, 1, staged["public"],
                expected_recovery_edges_per_translation=11),
             "commit nested key"),
            (update_public, lambda value: validate_incremental(
                value, 1, committed["public"]), "incremental nested key")):
        bad_payload = copy.deepcopy(payload); bad_payload["extra"] = True
        expect_failure(lambda bad_payload=bad_payload, validator=validator:
            validator(bad_payload), label)
    trace["nested_public_validators"] = 3

    # Closed stable-prefix payload validators use the same public entry in
    # production and bounded fixtures.  No real B0 digest/count is imported
    # into this sealed fixture.
    fixture_base_occurrences = [{"relator_index": index, "component": 1,
        "coefficient": 1, "element_hex": element_blob(e4.identity).hex(),
        "section_word": []} for index in range(1, 12)]
    fixture_base = {"D1_D2_zero_all": True,
        "occurrence_count": len(fixture_base_occurrences),
        "occurrences": fixture_base_occurrences,
        "order": "relator index, component, canonical E4 bytes",
        "ordered_sha256": sha_obj(fixture_base_occurrences),
        "per_component_counts": [11, 0, 0, 0, 0, 0],
        "per_relator_counts": [1]*11, "private_fields_published": False,
        "quotient_identity_all": True}
    fixture_support = {"all_prefix_sections_directly_replayed": True,
        "occurrence_count": len(fixture_base_occurrences),
        "occurrences": copy.deepcopy(fixture_base_occurrences),
        "order": fixture_base["order"],
        "ordered_sha256": fixture_base["ordered_sha256"]}
    fixture_cache = {"capacity": 8, "clears": 0, "evictions": 0,
        "hits": 0, "misses": 0, "peak": 0, "size": 0}
    fixture_pool_public = {"canonical_order": "fixture canonical bytes",
        "capacity": 64, "digest_used_as_equality": False,
        "exact_equality": "fixture canonical bytes", "hits": 0,
        "inverse_cache": copy.deepcopy(fixture_cache),
        "max_rollback_suffix": 0, "misses": 1,
        "packed_payload_bytes": WIDTH, "packed_width_bytes": WIDTH,
        "peak": 1, "product_cache": copy.deepcopy(fixture_cache),
        "rollback_lru_clears": 0, "rollback_suffix_removed": 0,
        "size": 1, "transaction_commits": 0, "transaction_rollbacks": 0}
    fixture_dag_public = {"edge_payload_bytes": 0, "live_edges": 0,
        "live_nodes": 1, "node_payload_bytes": 1, "packed_arrays": True,
        "peak_edges": 0, "peak_nodes": 1}
    fixture_counts = {"BFS_translations": 1, "columns": 11,
        "dependent_columns": 0, "directed_translations": 0,
        "live_sparse_entries": 11, "pivots": 11, "row_tail_visits": 0}
    fixture_accounting = {"BFS_translations": 1, "columns": 11,
        "dependent_columns": 0, "directed_translations": 0,
        "element_pool": fixture_pool_public, "live_sparse_entries": 11,
        "pivots": 11, "provenance_DAG": fixture_dag_public,
        "single_shared_basis": True,
        "targeted_translations_for_six_questions": 0,
        "total_translation_blocks": 1}
    empty_sha = sha_obj([])
    fixture_registry = {"translation_count": 1,
        "relators_per_translation": 11, "all_masks_equal_0x7ff": True,
        "canonical_translation_sha256": sha_bytes(t_blob),
        "semantic_blob_order": "exact E4 blob lexicographic",
        "pool_IDs_public": False}
    fixture_prefix = {"counts": fixture_counts,
        "accounting": fixture_accounting,
        "basis_gate": {"immutable_during_affine_probes": True,
            "least_pivot_coeff_one": True, "no_preceding_keys": True,
            "pivot_order": "component then exact E4 bytes", "pivots": 11,
            "rows": 11}, "prefix_pool_checkpoint": 1,
        "pool_order_sha256": sha_bytes(element_blob(e4.identity)),
        "dependent_events": [], "dependent_event_count": 0,
        "dependent_event_sha256": empty_sha, "fresh_not_imported": True,
        "source_sha256": "10"*32,
        "stable_rounds_projection_sha256": empty_sha,
        "translations_sha256": empty_sha, "columns_sha256": "20"*32,
        "blocker_history_sha256": empty_sha,
        "complete_block_registry": fixture_registry}
    fixture_surgery = {"blocker_history": [],
        "blocker_history_sha256": empty_sha, "bounded_prefix_sha256": "",
        "column_count": 0,
        "column_order": "translation first-seen order, relator 1..11",
        "columns_sha256": fixture_prefix["columns_sha256"],
        "round_count": 0, "rounds": [], "rounds_sha256": empty_sha,
        "section_expressions": {}, "section_oracle": {},
        "stable_projection_omits_exactly": ["elapsed_seconds", "RSS_bytes"],
        "stable_rounds_projection": [],
        "stable_rounds_projection_sha256": empty_sha,
        "stop_reason": "no_new_exact_directed_translation", "theorem": {},
        "translation_count": 0, "translations": [],
        "translations_sha256": empty_sha,
        "volatile_rounds_sha256_provenance_only": "30"*32}
    fixture_surgery["bounded_prefix_sha256"] = sha_obj({
        "translations": [], "columns_sha256": fixture_surgery["columns_sha256"],
        "blockers": [], "rounds": []})
    stable_trace: dict[str, int] = {}
    fixture_block, fixture_anchor = ei._fixture_block(stable_trace)
    fixture_old = ei._fixture_old_producer()
    _, fixture_affine, fixture_target6 = ei._fixture_affine(
        fixture_old, False, stable_trace)
    _, fixture_affine_consistent, fixture_target6_consistent = \
        ei._fixture_affine(fixture_old, True, stable_trace)
    fixture_initial = {"target6": fixture_target6,
        "affine_system": fixture_affine,
        "fresh_B1_stable_digests_all_equal": True,
        "raw_gradient_count": 109, "raw_gradients_sha256": "40"*32,
        "semantic_remainders_sha256":
            semantic_remainders_sha256([{} for _ in range(109)])}
    fixture_initial_consistent = {"target6": fixture_target6_consistent,
        "affine_system": fixture_affine_consistent,
        "fresh_B1_stable_digests_all_equal": True,
        "raw_gradient_count": 109, "raw_gradients_sha256": "41"*32,
        "semantic_remainders_sha256": semantic_remainders_sha256(
            [{(1, t_blob.hex()): 1}]+[{} for _ in range(108)])}
    fixture_parents_rows = [{"source_word_ordinal": index,
        "word_length": 0, "word_sha256": "50"*32,
        "gradient_entry_count": 0, "gradient_sha256": "60"*32,
        "all_nonzero_terms_parented": True} for index in range(109)]
    fixture_parents = {"source_count": 109, "rows": fixture_parents_rows,
        "rows_sha256": sha_obj(fixture_parents_rows),
        "source_word_order": "base target6 then registered seeds 1..108",
        "signed_offset_convention":
            "positive uses prefix before letter; negative uses prefix after inverse"}
    fixture_qstar = {"used_only_to_freshly_reconstruct_fixed_B1": True,
        "used_after_fixed_B1": False, "support_count": 1,
        "support_sha256": "70"*32, "complete_correlation_sha256": "80"*32}
    stable_payload = {"directed_base_support": fixture_support,
        "directed_surgery": fixture_surgery, "prefix_B0": fixture_prefix,
        "base_columns": fixture_base, "fixed_B1_block": fixture_block,
        "fixed_B1_anchor": fixture_anchor, "old_qstar_boundary": fixture_qstar,
        "raw_parent_manifest": fixture_parents,
        "recovery_map": toy_recovery.public(),
        "initial_target": fixture_initial, "generation_ledger": [],
        "phase": "fixture"}
    validate_stable_prefix_payloads(stable_payload, frozen=False, ei=ei)
    stable_mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("directed support", lambda value: value["directed_base_support"].update(
            {"occurrence_count": 10})),
        ("directed surgery", lambda value: value["directed_surgery"].update(
            {"extra": True})),
        ("prefix B0", lambda value: value["prefix_B0"].update(
            {"dependent_event_count": 1})),
        ("base columns", lambda value: value["base_columns"].update(
            {"extra": True})),
        ("fixed block", lambda value: value["fixed_B1_block"].update(
            {"extra": True})),
        ("fixed anchor", lambda value: value["fixed_B1_anchor"].update(
            {"extra": True})),
        ("old qstar", lambda value: value["old_qstar_boundary"].update(
            {"used_after_fixed_B1": True})),
        ("raw parents", lambda value: value["raw_parent_manifest"].update(
            {"rows_sha256": "0"*64})),
        ("recovery", lambda value: value["recovery_map"].update(
            {"pool_IDs_public": True})),
        ("initial target", lambda value: value["initial_target"].update(
            {"raw_gradient_count": 108})),
    ]
    for label0, mutate in stable_mutations:
        bad_stable = copy.deepcopy(stable_payload); mutate(bad_stable)
        expect_failure(lambda bad_stable=bad_stable:
            validate_stable_prefix_payloads(
                bad_stable, frozen=False, ei=ei), label0+" public payload")
    trace["stable_prefix_payloads"] = 1

    # The production quotient-row helper must remove later Bk pivots before
    # applying new rows.  Use two actual stored rows in reversed insertion
    # order so an insertion-order reducer, duplicate pivot, or claimed
    # tail/pivot reversal cannot pass this fixture.
    identity_blob = toy_pool.blob(toy_pool.identity_id)
    p1 = ToyOld.pack_vector_key(3, toy_pool.identity_id)
    p2 = ToyOld.pack_vector_key(4, toy_pool.identity_id)
    q = ToyOld.pack_vector_key(5, toy_pool.identity_id)
    r = ToyOld.pack_vector_key(6, toy_pool.identity_id)
    toy_basis.rows[q] = ({q: 1, r: 1}, 0)
    toy_basis.rows[p1] = ({p1: 1, q: 1}, 0)
    toy_basis.rows[p2] = ({p2: 1}, 0)
    order_input = [semantic_row(toy_old, toy_pool, toy_basis.rows[p2][0]),
                   semantic_row(toy_old, toy_pool, toy_basis.rows[p1][0])]
    order_keys = [p2, p1]
    order_progress: dict[str, Any] = {}
    ordered_fixture, order_sha = canonical_incremental_pivot_order(
        toy_old, toy_prefix, order_input, order_keys,
        len(toy_basis.rows)-2, toy_monitor.bind("incremental_reduction"),
        order_progress)
    require([min(row) for row in ordered_fixture] ==
                [(3, identity_blob), (4, identity_blob)] and
            ordered_fixture[0] == {(3, identity_blob): 1,
                                    (6, identity_blob): 2} and
            order_progress["completed_quotient_pivot_ordinal"] == 2,
            "157em old-basis quotient and semantic pivot order")
    insertion_sha = sha_obj([semantic_public(row) for row in
                             reversed(ordered_fixture)])
    require(insertion_sha != order_sha,
            "157em insertion reversal fixture distinct")
    expect_failure(lambda: canonical_incremental_pivot_order(
        toy_old, toy_prefix, order_input, order_keys,
        len(toy_basis.rows)-2, toy_monitor.bind("incremental_reduction"),
        {}, insertion_sha), "incremental insertion order digest")
    expect_failure(lambda: canonical_incremental_pivot_order(
        toy_old, toy_prefix, [order_input[0], order_input[0]], [p2, p2],
        len(toy_basis.rows)-2, toy_monitor.bind("incremental_reduction"),
        {}), "incremental duplicate pivot")
    expect_failure(lambda: canonical_incremental_pivot_order(
        toy_old, toy_prefix, order_input, order_keys,
        len(toy_basis.rows)-2, toy_monitor.bind("incremental_reduction"),
        {}, order_sha, [(4, identity_blob), (3, identity_blob)]),
        "incremental tail/pivot reversal")
    for fixture_key in (p1, p2, q):
        toy_basis.rows.pop(fixture_key)
    trace.update({"recovery_core": 1, "stage_batch_core": 1,
                  "commit_batch_core": 1, "incremental_109_core": 1,
                  "incremental_order_core": 1,
                  "single_recovery_edge_path": 1})
    # A resource after a reducer/recovery mutation must roll the unfinished
    # translation back to the last complete semantic block prefix.
    toy_basis.complete_masks = {}
    toy_prefix["_em_complete_block_masks"] = toy_basis.complete_masks
    rollback_before = state_accounting(toy_prefix, pool_digest=True)
    rollback_recovery = toy_recovery.public()
    rollback_ledger = PackedBlockLedger()
    toy_basis.pending = [dict(row["raw"]) for row in staged["rows"]]
    toy_basis.fail_after_relator = 5
    try:
        commit_batch(toy_old, e4, toy_prefix, toy_recovery, words,
            fixture_occurrences, fixture_correlation, staged,
            rollback_ledger, toy_monitor, 1, set())
    except LaneResource as exc:
        require(exc.phase == "block_commit" and
                exc.current["unfinished_translation_rolled_back"] is True and
                exc.current["rollback_translation_ordinal"] == 1 and
                exc.current["completed_translations"] == 0,
                "157em unfinished translation RESOURCE ledger")
    else:
        raise RuntimeError("157em incomplete transaction fixture accepted")
    finally:
        toy_basis.fail_after_relator = None
    require(state_accounting(toy_prefix, pool_digest=True) == rollback_before and
            toy_recovery.public() == rollback_recovery and
            rollback_ledger.translation_count == 0 and
            rollback_ledger.record_count == 0 and
            toy_basis.complete_masks == {},
            "157em pool/basis/DAG/section/recovery/ledger/mask rollback")
    trace["translation_transaction_rollback"] = 1

    fixture_masks: dict[bytes, int] = {}
    mask_blob = element_blob(e4.generators[0])
    for relator in range(1, 12):
        record_complete_block_relator(fixture_masks, mask_blob, relator)
    mask_public = complete_block_registry_public(fixture_masks, 1)
    require(mask_public["translation_count"] == 1,
            "157em complete-block shared fixture")
    incomplete_masks = dict(fixture_masks)
    incomplete_masks[mask_blob] &= ~(1 << 4)
    expect_failure(lambda: complete_block_registry_public(
        incomplete_masks, 1), "incomplete B0 block mask")
    expect_failure(lambda: record_complete_block_relator(
        fixture_masks, mask_blob, 9), "duplicate B0 block relator")
    expect_failure(lambda: require_active_not_completed(
        [(mask_blob, 9, 1)], {mask_blob}),
        "ACTIVE already-complete translation")
    trace["complete_block_registry"] = 1
    # Frozen EI deliberately dispatches its B1 insertion through the base
    # class.  Reproduce that bypass, then exercise the owned one-shot manual
    # recovery of all 76 support occurrences.
    manual_recovery = RecoveryMap(toy_monitor)
    manual_occurrences = []
    for ordinal in range(1, 77):
        relator = (ordinal-1) % 11+1; exponent = (ordinal-1) % 13
        value = e4.eval(power_word(exponent))
        manual_occurrences.append({"relator_index": relator,
            "term_ordinal": (ordinal-1)//11+1, "component": 1,
            "element_hex": element_blob(value).hex(), "_value": value})
    manual_edges = translated_recovery_edges(
        e4, toy_pool, t_blob, manual_occurrences)
    base_dispatch_column_count = 11
    require(base_dispatch_column_count == 11 and
            manual_recovery.translated_candidates == 0,
            "157em fixture base-class B1 dispatch bypass")
    saved_edge_cap0 = CAPS["raw_coordinate_recovery_edges"]
    try:
        CAPS["raw_coordinate_recovery_edges"] = 0
        try:
            manual_recovery.preflight_translated(
                manual_edges, phase="fixed_B1")
        except LaneResource as exc:
            require(exc.phase == "fixed_B1" and exc.observed == 76 and
                    manual_recovery.translated_candidates == 0,
                    "157em fixed B1 recovery cap phase/pre-mutation")
        else:
            raise RuntimeError("157em fixed B1 recovery cap accepted")
    finally:
        CAPS["raw_coordinate_recovery_edges"] = saved_edge_cap0
    manual_recovery.preflight_translated(manual_edges, phase="fixed_B1")
    manual_applied: set[bytes] = set()
    apply_manual_recovery_once(
        manual_recovery, t_blob, manual_edges, manual_applied)
    require(manual_recovery.translated_candidates == 76 and
            manual_recovery.candidates == 76,
            "157em fixed B1 exact 76 recovery candidates")
    expect_failure(lambda: apply_manual_recovery_once(
        manual_recovery, t_blob, manual_edges, manual_applied),
        "fixed B1 duplicate manual recovery")
    trace["fixed_B1_manual_recovery"] = 1
    try:
        enforce_generation_capacity(1, 12, 13, 8)
    except LaneResource as exc:
        require(exc.key == "column_generation_batches" and exc.limit == 12 and
                exc.observed == 13 and exc.comparator == "gt" and
                exc.phase == "correlation_pass1" and
                exc.detail == "column_generation_batch_limit" and
                exc.current == {"generation": 13, "completed_batches": 12,
                                "completed_blocks": 8},
                "157en generation-13 batch RESOURCE")
    else:
        raise RuntimeError("157en generation-13 batch cap accepted")
    try:
        enforce_generation_capacity(0, 12, 13, 4096)
    except LaneResource as exc:
        require(exc.key == "total_new_translation_blocks" and
                exc.limit == 4096 and exc.observed == 4097 and
                exc.detail == "total_translation_block_budget_exhausted",
                "157en total-block cap precedes batch cap")
    else:
        raise RuntimeError("157en total-block precedence accepted")
    trace["generation_13_resource"] = 1
    saved_parent_cap = CAPS["raw_coordinate_parent_entries"]
    try:
        CAPS["raw_coordinate_parent_entries"] = 0
        capped = RecoveryMap(toy_monitor)
        expect_failure(lambda: capped.consider_direct(1, t_blob, 0, 1),
                       "raw parent insertion cap")
        require(capped.public()["candidate_edge_count"] == 0,
                "157em raw parent cap is pre-mutation")
    finally:
        CAPS["raw_coordinate_parent_entries"] = saved_parent_cap
    saved_edge_cap = CAPS["raw_coordinate_recovery_edges"]
    try:
        CAPS["raw_coordinate_recovery_edges"] = \
            toy_recovery.translated_candidates
        before_atomic = toy_recovery.public(); before_columns = toy_basis.columns_seen
        extra = (1, element_blob(e4.eval([1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                         1, 1])).hex(), t_blob, 1, 1,
                 element_blob(e4.identity))
        expect_failure(lambda: toy_recovery.preflight_translated(
            [(extra[0], bytes.fromhex(extra[1]), *extra[2:])],
            phase="block_commit"), "recovery precommit cap")
        require(toy_recovery.public() == before_atomic and
                toy_basis.columns_seen == before_columns,
                "157em recovery cap leaves reducer/ledger unchanged")
    finally:
        CAPS["raw_coordinate_recovery_edges"] = saved_edge_cap

    def fixture_selected_proof() -> dict[str, Any]:
        """Build the bounded positive payload with pinned production serializers."""
        coefficients = [0]*108
        typed_private = old._affine_make_typed_positive(
            coefficients, [[] for _ in range(108)], ())
        typed_public = old._affine_typed_candidate_public(typed_private)
        target_dag = old.WordExprDAG()
        target_root = target_dag.identity(6)
        target_public = target_dag.serialize_reachable(
            [("hexagon_1_coface_0", target_root)])

        class FixtureProofPool:
            width = WIDTH

        class FixtureProofBasis:
            deadline = None
            pool = FixtureProofPool()
            sections: Any = None

        proof_dag = old.ProvenanceDAG()
        registry = old.ElementRegistry({4: e4})
        proof, renumber = old.serialize_proof_dag(
            proof_dag, {"hexagon_1_coface_0": 1},
            FixtureProofBasis(), registry)
        require(renumber == {1: 1} and registry.rows == [],
                "157em pinned zero-proof serializer fixture")
        selected = {"coefficient_vector": coefficients,
            "coefficient_vector_sha256": sha_obj(coefficients),
            "support": [], "factor_count": 0,
            "typed_candidate": typed_public,
            "target_expression": target_public,
            "direct_gradient": {"name": "hexagon_1_coface_0",
                "kind": "hexagon", "entry_count": 0,
                "quotient_value_hex": element_blob(e4.identity).hex(),
                "canonical_gradient_sha256": sha_bytes(b""),
                "canonical_order":
                    "component then exact canonical E4 bytes",
                "digest_is_binding_only_not_element_equality": True},
            "direct_replay": True, "affine_prediction_equal": True,
            "D2_proof": proof, "element_registry": registry.rows,
            "proof_root_node_id": renumber[1],
            "proof_expands_to_selected_gradient": True,
            "post_block_anchor_used": True,
            "targets_7_through_33_not_checked": True}
        validate_selected_proof(selected)
        return selected

    selected_fixture_public = fixture_selected_proof()
    trace["selected_payload_serializers"] = 1

    def fixture_receipt(token: str) -> dict[str, Any]:
        fixture_monitor = Monitor(30.0)
        fixture_phases: dict[str, float] = {}
        row = base_receipt(Path("fixture-q3.json"), fixture_monitor,
                           EXPECTED_UPSTREAM_CAPS)
        row["terminal_token"] = row["status"] = token
        row["phase"] = "complete"
        row["claims"] = claim_row(token)
        fixture_basis = copy.deepcopy(fixture_block["post_accounting"])
        fixture_basis["pool_order_sha256"] = None
        fixture_basis["recovery"] = toy_recovery.public()
        selected_fixture = copy.deepcopy(selected_fixture_public)
        equation = {"label": [6, "hexagon_1_coface_0", 1, t_blob.hex()],
                    "coefficient": 1}
        dual_fixture = {"normalization":
                "first contradiction multiplied by inverse RHS",
            "equations": [equation], "support_count": 1,
            "support_sha256": sha_obj([equation]), "normalized_rhs": 1,
            "yTz_mod3": 2, "all_108_annihilation_sha256": sha_obj([0]*108),
            "all_108_annihilation_dimension": 108,
            "live_provenance_entries": 1, "witness_provenance_entries": 1,
            "peak_live_provenance_entries": 1,
            "target_boundary": {"first_target_ordinal": 6,
                "last_target_ordinal": 6, "target_ordinals": [6]},
            "target6_fixed_prefix_functional": True,
            "coordinate_encoding": {"label":
                "[target_ordinal,target_name,component,E4_blob_hex]",
                "component_numbering": "one_based_1_through_6",
                "E4_blob": "canonical permutation bytes then PC bytes",
                "permutation_width_bytes": 144, "pc_width_bytes": 10,
                "blob_width": WIDTH, "blob_hex_length": 2*WIDTH,
                "endianness": "byte-string order; no integer reinterpretation",
                "pivot_order": "component then exact E4 bytes"},
            "seed_manifest_sha256": "11"*32, "variables": 108}

        def fixture_target(consistent: bool) -> dict[str, Any]:
            initial0 = (fixture_initial_consistent if consistent else
                        fixture_initial)
            affine0 = initial0["affine_system"]
            return {"generation": 1, "variables": 108,
                "equations": affine0["equations"], "rank": affine0["rank"],
                "nullity": affine0["nullity"], "consistent": consistent,
                "row_space_sha256": affine0["row_space_sha256"],
                "remainders_sha256":
                    initial0["semantic_remainders_sha256"],
                "live_remainder_entries": 1,
                "complete_all_coordinates": True,
                "stopped_at_first_contradiction": False,
                "dual": None if consistent else dual_fixture}

        raw_fixture = {"algorithm": "general-reverse-canonical-pivot-DP/v1",
            "support_count": 1, "per_component": [1, 0, 0, 0, 0, 0],
            "packed_support_sha256": "44"*32, "packed_support_bytes": 156,
            "pivot_count": fixture_basis["pivots"], "reverse_edge_visits": 0,
            "pivot_annihilation_sha256": sha_obj(
                [0]*fixture_basis["pivots"]), "dependent_event_count": 16,
            "dependent_annihilation_sha256": sha_obj([0]*16),
            "completed_block_column_count": 11,
            "completed_block_annihilation_sha256": sha_obj([0]*11),
            "delta_annihilation_sha256": sha_obj([0]*108),
            "base_z_scalar": 2, "negative_base_scalar": 1,
            "normalized_dual_whole_sha256": sha_obj(dual_fixture),
            "support_rows_not_serialized": True,
            "pool_IDs_or_old_qstar_used": False,
            "first_canary": [1, t_blob.hex(), 1],
            "last_canary": [1, t_blob.hex(), 1]}
        correlation_fixture = {"complete": True, "generation": 1,
            "pass1_pair_attempts": 10, "pass2_pair_attempts": 0,
            "pass2_selected_filter_count": 0,
            "candidate_count_before_zero_deletion": 1,
            "cancellation_to_zero_count": 1, "active_row_count": 0,
            "active_distinct_translation_count": 0,
            "scalar_distribution": {"1": 0, "2": 0},
            "active_packed_row_width": 156, "active_packed_bytes": 0,
            "active_packed_sha256": sha_bytes(b""),
            "selected_translation_count": 0, "selected_truncated": False,
            "selected_translation_sha256": sha_bytes(b""),
            "selected_bindings_sha256": sha_obj([]),
            "selection_order": "exact 154-byte translation blob lexicographic",
            "first_active": None, "full_E4_enumerated": False,
            "pool_or_basis_mutated": False, "cumulative_pass1_pairs": 10,
            "cumulative_pass2_pairs": 0}
        if token.endswith("CONSISTENT"):
            for name, value in early_fixture.items():
                row[name] = copy.deepcopy(value)
            for name in ("directed_base_support", "directed_surgery",
                    "prefix_B0", "base_columns", "fixed_B1_block",
                    "fixed_B1_anchor", "old_qstar_boundary",
                    "raw_parent_manifest", "recovery_map"):
                row[name] = copy.deepcopy(stable_payload[name])
            row["initial_target"] = copy.deepcopy(
                fixture_initial_consistent)
            row["reason"] = \
                "registered_108_target6_consistent_mod_generated_D2"
            row["generation_ledger"] = [{"generation": 1,
                "basis": fixture_basis, "target": fixture_target(True),
                "raw_lambda": {}, "correlation": {}, "preflight": {},
                "commit": {}, "incremental": {},
                "classification": "CONSISTENT"}]
            row["selected_proof"] = selected_fixture
            row["packed_block_ledger"] = PackedBlockLedger().public(
                fixture_monitor)
            fixture_phases = {"selected_proof_g1": 0.0,
                              "receipt_serialization": 0.0}
        elif token.endswith("FULL_D2_OBSTRUCTION"):
            for name, value in early_fixture.items():
                row[name] = copy.deepcopy(value)
            for name in ("directed_base_support", "directed_surgery",
                    "prefix_B0", "base_columns", "fixed_B1_block",
                    "fixed_B1_anchor", "old_qstar_boundary",
                    "raw_parent_manifest", "recovery_map"):
                row[name] = copy.deepcopy(stable_payload[name])
            row["initial_target"] = copy.deepcopy(fixture_initial)
            row["initial_target"]["affine_system"]["dual_witness"] = \
                copy.deepcopy(dual_fixture)
            row["reason"] = "complete_full_D2_correlation_zero"
            generation_fixture = {"generation": 1, "basis": fixture_basis,
                "target": fixture_target(False), "raw_lambda": raw_fixture,
                "correlation": correlation_fixture, "preflight": {},
                "commit": {}, "incremental": {},
                "classification": "FULL_D2_OBSTRUCTION"}
            row["generation_ledger"] = [generation_fixture]
            row["full_D2_separator"] = {"generation": 1,
                "raw_lambda": raw_fixture, "correlation": correlation_fixture,
                "active_row_count": 0,
                "complete_76_occurrence_full_11_relator_correlation": True,
                "annihilates_full_D2": True, "lambda_delta_all_zero": True,
                "lambda_base_z": 2, "registered_108_family_only": True,
                "pinned_E4_roof_only": True}
            row["packed_block_ledger"] = PackedBlockLedger().public(
                fixture_monitor)
            fixture_phases = {"dual_lift_g1": 0.0,
                "correlation_g1": 0.0, "receipt_serialization": 0.0}
        elif token.endswith("UNKNOWN_INPUT"):
            row["phase"] = "authenticated_input"
            row["reason"] = "authenticated_input_failure"
            row["input_errors"] = ["sealed pin drift"]
        else:
            stop = LaneResource("producer_soft_rss_bytes",
                CAPS["producer_soft_rss_bytes"],
                CAPS["producer_soft_rss_bytes"], "ge",
                "authenticated_input", {}, inner="authenticated_input")
            row["phase"] = stop.phase; row["reason"] = stop.key
            row["resource_guards"] = {"resource_hit": True,
                "resource": stop.public(),
                "local_and_upstream_separate": True,
                "reason_equals_cap_key": True}
            row["partial"] = {"phase": stop.phase, "reason": stop.key,
                "current": stop.current, "completed_generation_count": 0,
                "completed_batch_count": 0,
                "completed_new_translation_block_count": 0,
                "current_generation": None,
                "packed_block_ledger_prefix": PackedBlockLedger().partial_public(),
                "selected_proof": None, "full_D2_separator": None}
            fixture_monitor.hit_reason = stop.key
        row["performance"] = performance_public(fixture_monitor, fixture_phases)
        if token.endswith(("CONSISTENT", "FULL_D2_OBSTRUCTION")):
            row["performance"]["phase_seconds"] = {key: 0.0 for key in
                expected_phase_seconds_keys(row)}
        validate_receipt(row, allow_unsealed=True); return row

    four = [fixture_receipt(token) for token in sorted(TERMINALS)]
    fixed_q3_pin = {"path": Q3_PATH.as_posix(), "sha256": Q3_SHA,
                    "bytes": Q3_BYTES}
    require(len(four) == 4 and all(row["pins"]["q3_artifact"] ==
            fixed_q3_pin for row in four),
            "157em four terminal fixed q3 receipt pin")
    cap_bound = next(row for row in four if
                     row["terminal_token"].endswith("CONSISTENT"))
    bad = copy.deepcopy(cap_bound)
    bad["upstream_caps"]["element_pool"] -= 1
    bad["upstream_caps_sha256"] = sha_obj(bad["upstream_caps"])
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "literal upstream cap value")
    bad = copy.deepcopy(four[0]); bad["pins"]["q3_artifact"]["bytes"] -= 1
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "q3 fixed bytes mutation")
    bad = copy.deepcopy(four[0]); bad["pins"]["157el_producer"]["sha256"] = "0"*64
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "full predecessor pin mutation")
    bad = copy.deepcopy(four[0]); bad["algorithm"]["monitor_registry"][
        "receipt_serialization"] = []
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "monitor registry receipt mutation")
    for field in ("terminal_token", "status", "reason", "phase", "claims"):
        bad = copy.deepcopy(four[0]); bad[field] = None
        expect_failure(lambda bad=bad: validate_receipt(
            bad, allow_unsealed=True), "terminal " + field)
    bad = copy.deepcopy(four[0]); bad["extra"] = True
    expect_failure(lambda: validate_receipt(bad, allow_unsealed=True),
                   "extra top field")
    bad = copy.deepcopy(four[0])
    bad["provenance"]["predecessor_failed_run"]["cross_checked"] = True
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "failed-run provenance promotion")
    resource_row = next(row for row in four
                        if row["terminal_token"].endswith("UNKNOWN_RESOURCE"))

    def scoped_resource_fixture(stop: LaneResource) -> dict[str, Any]:
        """Route an honest scoped stop through the production receipt entry."""
        row = copy.deepcopy(resource_row)
        row["phase"] = stop.phase; row["reason"] = stop.key
        row["resource_guards"]["resource"] = resource_public(stop)
        row["partial"]["phase"] = stop.phase
        row["partial"]["reason"] = stop.key
        row["partial"]["current"] = copy.deepcopy(stop.current)
        row["performance"]["hit_reason"] = stop.key
        row["performance"]["phase_seconds"] = {}
        validate_receipt(row, allow_unsealed=True)
        return row

    fresh_edge_resource = scoped_resource_fixture(LaneResource(
        "raw_coordinate_recovery_edges",
        CAPS["raw_coordinate_recovery_edges"],
        CAPS["raw_coordinate_recovery_edges"]+1, "gt", "fresh_B0",
        {"completed_candidate_edges": 4095}))
    scoped_resource_fixture(LaneResource(
        "raw_coordinate_recovery_nodes",
        CAPS["raw_coordinate_recovery_nodes"],
        CAPS["raw_coordinate_recovery_nodes"]+1, "gt", "fresh_B0",
        {"candidate_edges": 4095}))
    scoped_resource_fixture(LaneResource(
        "common_math_soft_deadline_seconds",
        CAPS["common_math_soft_deadline_seconds"],
        CAPS["common_math_soft_deadline_seconds"], "ge", "initial_target",
        {}, inner="initial_target"))
    scoped_resource_fixture(LaneResource(
        "producer_soft_rss_bytes", CAPS["producer_soft_rss_bytes"],
        CAPS["producer_soft_rss_bytes"], "ge", "correlation_pass1", {},
        inner="correlation_pass1"))
    bad = copy.deepcopy(fresh_edge_resource)
    bad["resource_guards"]["resource"]["current"] = {}
    bad["partial"]["current"] = {}
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "fresh recovery singleton erased")
    trace["resource_current_scopes"] = 1

    bad = copy.deepcopy(resource_row); bad["reason"] = "detail"
    expect_failure(lambda: validate_receipt(bad, allow_unsealed=True),
                   "resource reason/detail swap")
    bad = copy.deepcopy(resource_row); bad["selected_proof"] = {"stale": True}
    expect_failure(lambda: validate_receipt(bad, allow_unsealed=True),
                   "resource stale positive")
    bad = copy.deepcopy(resource_row)
    bad["packed_block_ledger"] = {"stale": "full"}
    expect_failure(lambda: validate_receipt(bad, allow_unsealed=True),
                   "resource stale packed ledger")
    input_row = next(row for row in four
                     if row["terminal_token"].endswith("UNKNOWN_INPUT"))
    bad = copy.deepcopy(input_row); bad["input_errors"] = [""]
    expect_failure(lambda: validate_receipt(bad, allow_unsealed=True),
                   "input empty diagnostic")
    for field, value in (("cap_source", "upstream"), ("cap_limit", 7),
                         ("comparator", "gt"), ("phase", "fixed_B1")):
        bad = copy.deepcopy(resource_row)
        bad["resource_guards"]["resource"][field] = value
        expect_failure(lambda bad=bad: validate_receipt(
            bad, allow_unsealed=True), "resource " + field)
    bad = copy.deepcopy(resource_row)
    bad["resource_guards"]["resource"]["current"]["forged"] = True
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "resource current binding")
    consistent_fixture = next(row for row in four if
        row["terminal_token"].endswith("CONSISTENT"))
    obstruction_fixture = next(row for row in four if
        row["terminal_token"].endswith("FULL_D2_OBSTRUCTION"))
    bad = copy.deepcopy(consistent_fixture)
    bad["selected_proof"]["extra"] = True
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "selected proof nested schema")
    selected_mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("typed candidate", lambda value: value["typed_candidate"][
            "expression"].update({"manifest_sha256": "0"*64})),
        ("target expression", lambda value: value["target_expression"][
            "roots"][0].update({"node_id": 2})),
        ("direct gradient", lambda value: value["direct_gradient"].update(
            {"canonical_gradient_sha256": "1"*64})),
        ("D2 manifest", lambda value: value["D2_proof"].update(
            {"packed_manifest_sha256": "2"*64})),
        ("proof root", lambda value: value.update(
            {"proof_root_node_id": 2})),
        ("registry", lambda value: value["element_registry"].append(
            {"forged": True})),
    ]
    for label0, mutate in selected_mutations:
        bad = copy.deepcopy(consistent_fixture); mutate(bad["selected_proof"])
        expect_failure(lambda bad=bad: validate_receipt(
            bad, allow_unsealed=True), "selected " + label0)
    bad = copy.deepcopy(obstruction_fixture)
    del bad["generation_ledger"][0]["raw_lambda"]["first_canary"]
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "raw lambda nested schema")
    bad = copy.deepcopy(obstruction_fixture)
    bad["generation_ledger"][0]["correlation"]["extra"] = 0
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "correlation nested schema")
    bad = copy.deepcopy(obstruction_fixture)
    bad["full_D2_separator"]["active_row_count"] = 1
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "separator semantic binding")
    bad = copy.deepcopy(resource_row)
    bad["partial"]["completed_batch_count"] = 1
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "RESOURCE committed count")
    bad = copy.deepcopy(resource_row)
    bad["performance"]["phase_seconds"]["forged"] = 0.0
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "performance phase prefix")

    # Reproduce the run-32439034163 boundary, not merely an empty-stage
    # RESOURCE envelope: fixed B1 is committed, all 109 B1 target remainders
    # are complete, and generation one exists with no classification because
    # the raw-dual lift is the attempted (uncommitted) stage.  The semantic
    # remainder commitment is deliberately distinct from EI's summary-ledger
    # commitment and is bound to the generation target by the same production
    # validators used by ``run``.
    sealed_dual = copy.deepcopy(obstruction_fixture[
        "generation_ledger"][0]["target"]["dual"])
    sealed_initial = copy.deepcopy(fixture_initial)
    sealed_initial["semantic_remainders_sha256"] = \
        semantic_remainders_sha256(
            [{(1, t_blob.hex()): 1}]+[{} for _ in range(108)])
    sealed_initial["affine_system"]["dual_witness"] = sealed_dual
    sealed_affine = sealed_initial["affine_system"]
    sealed_basis = copy.deepcopy(fixture_block["post_accounting"])
    sealed_basis["pool_order_sha256"] = None
    sealed_basis["recovery"] = copy.deepcopy(toy_recovery.public())
    sealed_target = {"generation": 1, "variables": 108,
        "equations": sealed_affine["equations"],
        "rank": sealed_affine["rank"],
        "nullity": sealed_affine["nullity"],
        "consistent": sealed_affine["consistent"],
        "row_space_sha256": sealed_affine["row_space_sha256"],
        "remainders_sha256":
            sealed_initial["semantic_remainders_sha256"],
        "live_remainder_entries": 1,
        "complete_all_coordinates": True,
        "stopped_at_first_contradiction": False,
        "dual": sealed_dual}

    generation_resource = copy.deepcopy(resource_row)
    generation_resource.update(copy.deepcopy(early_fixture))
    for completed_field in ("directed_base_support", "directed_surgery",
            "prefix_B0", "base_columns", "fixed_B1_block",
            "fixed_B1_anchor", "old_qstar_boundary",
            "raw_parent_manifest", "recovery_map"):
        generation_resource[completed_field] = copy.deepcopy(
            stable_payload[completed_field])
    generation_resource["initial_target"] = sealed_initial
    generation_stop = LaneResource("raw_lambda_reverse_edge_visits",
        CAPS["raw_lambda_reverse_edge_visits"],
        CAPS["raw_lambda_reverse_edge_visits"]+1, "gt", "dual_lift",
        {"completed_reverse_pivots": 0})
    generation_resource["phase"] = generation_stop.phase
    generation_resource["reason"] = generation_stop.key
    generation_resource["resource_guards"]["resource"] = \
        generation_stop.public()
    generation_resource["partial"].update({"phase": generation_stop.phase,
        "reason": generation_stop.key, "current": generation_stop.current,
        "current_generation": 1})
    generation_resource["performance"]["hit_reason"] = generation_stop.key
    generation_resource["performance"]["phase_seconds"] = {
        "authenticated_input": 0.0, "source_preflight": 0.0,
        "fresh_B0": 0.0, "fixed_B1": 0.0, "initial_target": 0.0}
    generation_resource["generation_ledger"] = [{
        "generation": 1,
        "basis": sealed_basis, "target": sealed_target,
        "raw_lambda": {}, "correlation": {}, "preflight": {}, "commit": {},
        "incremental": {}, "classification": None}]
    validate_receipt(generation_resource, allow_unsealed=True)
    bad = copy.deepcopy(generation_resource)
    bad["generation_ledger"][0]["target"]["remainders_sha256"] = \
        sealed_initial["target6"]["base_remainder_sha256"]
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "RESOURCE old summary-ledger binding")
    bad = copy.deepcopy(generation_resource)
    bad["initial_target"]["semantic_remainders_sha256"] = "ab"*32
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "RESOURCE stale initial semantic binding")
    bad = copy.deepcopy(generation_resource); bad["generation_ledger"][0][
        "generation"] = 2
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "generation order")
    bad = copy.deepcopy(generation_resource); bad["generation_ledger"][0][
        "extra"] = True
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "generation row keyset")
    trace["completed_initial_resource_envelope"] = 1

    def cap12_recovery_after(row: dict[str, Any], generation: int) \
            -> dict[str, Any]:
        answer = copy.deepcopy(row)
        answer["candidate_edge_count"] += 76
        answer["translated_candidate_edge_count"] += 76
        answer["canonical_sha256"] = sha_obj(
            {"cap12_recovery_generation": generation,
             "prior": row["canonical_sha256"]})
        return answer

    def cap12_raw_lambda(generation: int, basis: dict[str, Any],
                         target: dict[str, Any], blob: bytes) \
            -> dict[str, Any]:
        canary = [1, blob.hex(), 1]
        completed_columns = 11*generation
        return {"algorithm": "general-reverse-canonical-pivot-DP/v1",
            "support_count": 1, "per_component": [1, 0, 0, 0, 0, 0],
            "packed_support_sha256": sha_obj(canary),
            "packed_support_bytes": 156,
            "pivot_count": basis["pivots"], "reverse_edge_visits": 0,
            "pivot_annihilation_sha256":
                zero_vector_sha256(basis["pivots"]),
            "dependent_event_count": 16,
            "dependent_annihilation_sha256": zero_vector_sha256(16),
            "completed_block_column_count": completed_columns,
            "completed_block_annihilation_sha256":
                zero_vector_sha256(completed_columns),
            "delta_annihilation_sha256": zero_vector_sha256(108),
            "base_z_scalar": 2, "negative_base_scalar": 1,
            "normalized_dual_whole_sha256": sha_obj(target["dual"]),
            "support_rows_not_serialized": True,
            "pool_IDs_or_old_qstar_used": False,
            "first_canary": canary, "last_canary": canary}

    def cap12_correlation(generation: int, blob: bytes, *,
                          selected: bool) -> dict[str, Any]:
        selected_rows = 1 if selected else 0
        return {"complete": True, "generation": generation,
            "pass1_pair_attempts": 10,
            "pass2_pair_attempts": 10 if selected else 0,
            "pass2_selected_filter_count": selected_rows,
            "candidate_count_before_zero_deletion": 1,
            "cancellation_to_zero_count": 0, "active_row_count": 1,
            "active_distinct_translation_count": 1,
            "scalar_distribution": {"1": 1, "2": 0},
            "active_packed_row_width": 156, "active_packed_bytes": 156,
            "active_packed_sha256": sha_bytes(
                bytes([1])+blob+bytes([9, 1])),
            "selected_translation_count": selected_rows,
            "selected_truncated": not selected,
            "selected_translation_sha256":
                sha_bytes(blob if selected else b""),
            "selected_bindings_sha256":
                sha_obj([[blob.hex(), 9, 1]] if selected else []),
            "selection_order":
                "exact 154-byte translation blob lexicographic",
            "first_active": {"translation_hex": blob.hex(),
                "relator_index": 9, "scalar": 1},
            "full_E4_enumerated": False, "pool_or_basis_mutated": False,
            "cumulative_pass1_pairs": 10*generation,
            "cumulative_pass2_pairs": 10*min(generation, 12)}

    def cap12_preflight(generation: int, basis: dict[str, Any], blob: bytes,
                        record_specs: Sequence[tuple[int, bool,
                            tuple[int, bytes] | None, str, str]]) \
            -> dict[str, Any]:
        row = copy.deepcopy(staged["public"])
        row["generation"] = generation
        state = copy.deepcopy(basis)
        state["pool_order_sha256"] = sha_obj(
            {"cap12_pre_state": generation})
        state["recovery"] = None
        row["state_neutrality_before"] = state
        row["state_neutrality_after"] = copy.deepcopy(state)
        selected = row["section_provenance"]["selected"]
        require(len(selected) == 1,
                "157en cap12 sealed single selected fixture")
        item = selected[0]; item["generation"] = generation
        item["translation_hex"] = blob.hex()
        item["contributor"]["g_hex"] = blob.hex()
        item["contributor"]["translation_hex"] = blob.hex()
        contributor = item["contributor"]
        contributor_raw = bytes([contributor["component"]]) + blob + \
            bytes([contributor["lambda_coefficient"],
                   contributor["relator_index"]]) + \
            struct.pack(">H", contributor["occurrence_ordinal"]) + \
            bytes.fromhex(contributor["h_hex"]) + \
            bytes([contributor["base_coefficient"]])
        contributor["record_hex"] = contributor_raw.hex()
        contributor["record_sha256"] = sha_bytes(contributor_raw)
        item["g_recovery"]["element_hex"] = blob.hex()
        item["materialization_canary"]["value_hex"] = blob.hex()
        section = row["section_provenance"]
        section["selected_sha256"] = sha_obj(selected)
        binding = [[blob.hex(), relator, 1 if relator == 9 else 0,
                    raw_sha, typed_sha]
            for relator, _, _, raw_sha, typed_sha in record_specs]
        row["row_binding_sha256"] = sha_obj(binding)
        return row

    cap12_ledger = PackedBlockLedger()
    cap12_rows: list[dict[str, Any]] = []
    cap12_basis = copy.deepcopy(sealed_basis)
    cap12_remainder_sha = sealed_initial["semantic_remainders_sha256"]
    for generation in range(1, 13):
        blob = bytes([generation])+bytes(WIDTH-1)
        target = copy.deepcopy(sealed_target)
        target["generation"] = generation
        target["remainders_sha256"] = cap12_remainder_sha
        record_specs: list[tuple[int, bool,
            tuple[int, bytes] | None, str, str]] = []
        cap12_ledger.add_translation(blob)
        for relator in range(1, 12):
            independent = relator == 9
            pivot = (1, blob) if independent else None
            raw_sha = sha_obj({"generation": generation,
                               "relator": relator, "kind": "raw"})
            typed_sha = sha_obj({"generation": generation,
                                 "relator": relator, "kind": "typed"})
            record_specs.append((relator, independent, pivot,
                                 raw_sha, typed_sha))
            cap12_ledger.add_record(generation, 1, relator,
                1 if relator == 9 else 0, independent, pivot,
                raw_sha, typed_sha)
        correlation = cap12_correlation(generation, blob, selected=True)
        preflight = cap12_preflight(generation, cap12_basis, blob,
                                    record_specs)
        pre_public = copy.deepcopy(cap12_basis)
        pre_public["pool_order_sha256"] = sha_obj(
            {"cap12_commit_pre": generation})
        post_public = copy.deepcopy(pre_public)
        post_public.update({"columns": pre_public["columns"]+11,
            "pivots": pre_public["pivots"]+1,
            "dependent": pre_public["dependent"]+10,
            "live_sparse_entries": pre_public["live_sparse_entries"]+1,
            "pool_size": pre_public["pool_size"]+1,
            "DAG_nodes": pre_public["DAG_nodes"]+1,
            "DAG_edges": pre_public["DAG_edges"]+1,
            "section_bindings": pre_public["section_bindings"]+1,
            "section_expression_nodes":
                pre_public["section_expression_nodes"]+1,
            "section_expression_edges":
                pre_public["section_expression_edges"]+1,
            "recovery": cap12_recovery_after(
                pre_public["recovery"], generation)})
        outcomes = [{"translation_ordinal": 1, "relator": relator,
            "independent": independent, "lambda_scalar":
                1 if relator == 9 else 0,
            "pivot": None if pivot is None else [1, blob.hex()]}
            for relator, independent, pivot, _, _ in record_specs]
        commit = {"generation": generation, "complete": True,
            "translation_count": 1, "column_count": 11, "rank_gain": 1,
            "dependent_gain": 10, "pre_accounting": pre_public,
            "post_accounting": post_public,
            "first_translation_jstar_pivot": {"translation_ordinal": 1,
                "relator": 9, "scalar": 1, "pivot": [1, blob.hex()]},
            "outcome_semantic_sha256": sha_obj(outcomes),
            "all_blocks_complete": True,
            "all_staged_before_first_mutation": True}
        next_remainder_sha = sha_obj(
            {"cap12_post_remainder_generation": generation})
        incremental = {"generation": generation,
            "completed_new_pivot_ordinal": 1,
            "completed_rows_in_current_pivot": 0,
            "pre_update_remainder_sha256": cap12_remainder_sha,
            "last_fully_updated_row_sha256": sha_obj(
                {"cap12_last_row": generation}),
            "current_new_pivot_prefix_sha256": sha_obj([blob.hex()]),
            "new_pivot_count": 1,
            "reduction_order_sha256": sha_obj([[1, blob.hex()]]),
            "old_pivot_count": pre_public["pivots"],
            "old_pivot_set_encoding":
                "domain:d972-157em-semantic-pivot-set-v1\\0|count:u32be|"
                "repeated(component:u8,blob:154)",
            "old_pivot_set_sha256": sha_obj(
                {"cap12_old_pivots": generation}),
            "completed_quotient_pivot_ordinal": 1,
            "completed_quotient_prefix_sha256": sha_obj([blob.hex()]),
            "quotient_rows_discarded_on_failure": False,
            "live_entry_count": 1, "batch_anchor_committed": True,
            "rolled_back_on_failure": False, "complete": True,
            "post_update_remainder_sha256": next_remainder_sha,
            "fresh_direct_cadence": [{"ordinal": ordinal,
                "sha256": sha_obj({"generation": generation,
                                    "ordinal": ordinal}), "equal": True}
                for ordinal in (0, 1, 54, 108)]}
        cap12_rows.append({"generation": generation,
            "basis": copy.deepcopy(cap12_basis), "target": target,
            "raw_lambda": cap12_raw_lambda(
                generation, cap12_basis, target, blob),
            "correlation": correlation, "preflight": preflight,
            "commit": commit, "incremental": incremental,
            "classification": "ACTIVE_BATCH_COMMITTED"})
        cap12_basis = copy.deepcopy(post_public)
        cap12_basis["pool_order_sha256"] = None
        cap12_remainder_sha = next_remainder_sha
    blob13 = bytes([13])+bytes(WIDTH-1)
    target13 = copy.deepcopy(sealed_target)
    target13["generation"] = 13
    target13["remainders_sha256"] = cap12_remainder_sha
    cap12_rows.append({"generation": 13,
        "basis": copy.deepcopy(cap12_basis), "target": target13,
        "raw_lambda": cap12_raw_lambda(13, cap12_basis, target13, blob13),
        "correlation": cap12_correlation(13, blob13, selected=False),
        "preflight": {}, "commit": {}, "incremental": {},
        "classification": None})
    cap12_resource = copy.deepcopy(generation_resource)
    cap12_current = {"generation": 13, "completed_batches": 12,
                     "completed_blocks": 12}
    cap12_stop = LaneResource("column_generation_batches", 12, 13, "gt",
        "correlation_pass1", cap12_current,
        detail="column_generation_batch_limit")
    cap12_resource["phase"] = cap12_stop.phase
    cap12_resource["reason"] = cap12_stop.key
    cap12_resource["resource_guards"]["resource"] = cap12_stop.public()
    cap12_resource["generation_ledger"] = cap12_rows
    cap12_resource["partial"].update({"phase": cap12_stop.phase,
        "reason": cap12_stop.key, "current": copy.deepcopy(cap12_current),
        "completed_generation_count": 12, "completed_batch_count": 12,
        "completed_new_translation_block_count": 12,
        "current_generation": 13,
        "packed_block_ledger_prefix": cap12_ledger.partial_public()})
    cap12_resource["performance"]["hit_reason"] = cap12_stop.key
    cap12_resource["performance"]["phase_seconds"] = {key: 0.0 for key in
        expected_phase_seconds_keys(cap12_resource)}
    validate_receipt(cap12_resource, allow_unsealed=True)
    bad = copy.deepcopy(cap12_resource)
    bad["generation_ledger"][0]["target"]["remainders_sha256"] = \
        bad["initial_target"]["target6"]["base_remainder_sha256"]
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "cap12 RESOURCE old summary binding")
    bad = copy.deepcopy(cap12_resource)
    bad["initial_target"]["semantic_remainders_sha256"] = "bc"*32
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "cap12 RESOURCE stale semantic")
    bad = copy.deepcopy(cap12_resource)
    bad["resource_guards"]["resource"]["inner_phase"] = "correlation_pass1"
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "cap12 RESOURCE forged inner")
    bad = copy.deepcopy(cap12_resource)
    bad["resource_guards"]["resource"]["current"][
        "completed_blocks"] = 11
    bad["partial"]["current"]["completed_blocks"] = 11
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "cap12 RESOURCE stale current")
    bad = copy.deepcopy(cap12_resource)
    bad["generation_ledger"][5]["generation"] = 7
    expect_failure(lambda bad=bad: validate_receipt(
        bad, allow_unsealed=True), "cap12 RESOURCE generation order")
    trace["cap12_resource_envelope"] = 1
    trace["receipt_validator"] = 1
    input_row = next(row for row in four
                     if row["terminal_token"].endswith("UNKNOWN_INPUT"))
    bad = copy.deepcopy(input_row); bad["fixed_B1_block"] = {"stale": True}
    expect_failure(lambda: validate_receipt(bad, allow_unsealed=True),
                   "input stale math")

    with tempfile.TemporaryDirectory(prefix="d972-157em-") as folder:
        target = Path(folder)/"receipt.json"
        checked_input = next(row for row in four
            if row["terminal_token"].endswith("UNKNOWN_INPUT"))
        require(checked_input["terminal_token"] ==
                "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT",
                "157em checked-write fixture exact INPUT token")
        written, raw = write_checked(target, copy.deepcopy(checked_input))
        require(target.read_bytes() == raw and written["performance"][
            "receipt_bytes"] == len(raw) and
            written["pins"]["q3_artifact"] == fixed_q3_pin and
            written["terminal_token"] ==
                "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT",
            "157em checked write exact readback/fixed q3 pin")

    require(trace == {"resource_registry": 1, "monitor_pair_registry": 1,
            "authenticated_frontend": 4,
            "old_module_lifecycle": 3,
            "upstream_throw_site_exact": 1,
            "exact_157eg_prefix_projection": 1,
            "recovery_4096_monitor_pairs": 1,
            "prefix_provider": 1, "reverse_lift_core": 1,
            "recovery_core": 1, "stage_batch_core": 1,
            "commit_batch_core": 1, "incremental_109_core": 1,
            "incremental_order_core": 1,
            "nested_public_validators": 3,
            "stable_prefix_payloads": 1,
            "contributor_aggregate_split": 1,
            "generation_cross_bind": 1,
            "packed_generation_bindings": 1,
            "summary_key_modes": 2,
            "summary_key_mutations": 4,
            "semantic_remainder_binding_mutations": 4,
            "generation_13_resource": 1,
            "resource_current_scopes": 1,
            "completed_initial_resource_envelope": 1,
            "cap12_resource_envelope": 1,
            "selected_payload_serializers": 1,
            "incremental_foreign_progress": 1,
            "single_recovery_edge_path": 1,
            "translation_transaction_rollback": 1,
            "complete_block_registry": 1,
            "fixed_B1_manual_recovery": 1,
            "receipt_validator": 1} and
            materialize_trace == {"owned_inverse": 1} and
            mutation_count >= 28,
            "157em shared-core fixture coverage counters")
    print("D972_B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_SELFTEST_PASS "
          f"prefix_provider={trace['prefix_provider']} "
          f"reverse_lift={trace['reverse_lift_core']} correlation=2 "
          f"section_inverse={materialize_trace['owned_inverse']} "
          "resource_registry=1 monitor_pair_registry=1 "
          "upstream_throw_site_exact=1 "
          "authenticated_frontend=4 "
          "old_module_lifecycle=3 "
          "exact_157eg_prefix_projection=1 "
          "recovery_4096_monitor_pairs=1 "
          "recovery=1 stage_batch=1 commit_batch=1 incremental109=1 "
          "incremental_order=1 "
          "nested_validators=3 stable_prefix_payloads=1 "
          "contributor_aggregate_split=1 "
          "generation_cross_bind=1 packed_generation_bindings=1 "
          "summary_key_modes=2 summary_key_mutations=4 "
          "semantic_remainders=1 semantic_mutations=4 "
          "generation_13_resource=1 cap12=1 "
          "resource_current_scopes=1 "
          "completed_initial_resource_envelope=1 "
          "cap12_resource_envelope=1 "
          "selected_payload_serializers=1 "
          "incremental_foreign_progress=1 "
          "single_recovery_edge_path=1 transaction_rollback=1 "
          "complete_block_registry=1 fixed_B1_manual_recovery=1 "
          "positive_prefix_offset=1 "
          "fixture_blob_decoder=1 "
          "receipt_validator=1 "
          "packed_225=1 terminals=4 checked_write=1 "
          f"mutations={mutation_count} inherited_157el=1", flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q3", default="ci/out/d972_b345_q3_chief_v1.json")
    parser.add_argument("--output", default=OUTPUT.as_posix())
    parser.add_argument("--seconds", type=float, default=18_000.0)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        self_test(); return 0
    receipt = run((ROOT/Path(args.q3)).resolve(), seconds=args.seconds)
    receipt, raw = write_checked((ROOT/Path(args.output)).resolve(), receipt)
    print("D972_B345_TARGET6_DUAL_COLGEN_V2_PRODUCER_PASS " +
          f"terminal={receipt['terminal_token']} sha256={sha_bytes(raw)} " +
          f"bytes={len(raw)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
