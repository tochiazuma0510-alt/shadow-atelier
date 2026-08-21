#!/usr/bin/env python3
"""Independent checker for bounded target-6 full-D2 column generation v2."""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib.util
import json
import struct
import sys
import time
from array import array
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157en_b345_target6_dual_colgen_v2.md")
TASK_SHA = "0c650d358662d3d8e3eaf8fa67eac50ff8d64e35522348cfe634ead02f7c0ee8"
TASK_BYTES = 16_017
PRODUCER = Path("search/d972_b345_target6_dual_colgen_v2.py")
PRODUCER_SHA = "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"
PRODUCER_BYTES = 444_497
V1_CHECKER = Path("search/check_d972_b345_target6_dual_colgen_v1.py")
V1_CHECKER_SHA = "08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e"
V1_CHECKER_BYTES = 228_980
V1_CHECKER_MODULE = "_d972_157en_pinned_157em_checker"
V4_CHECKER = Path("search/check_d972_b345_lexfirst_block_target6_v4.py")
V4_CHECKER_SHA = "f15a2beeaf1925c1ea4894ef5fae02de6973c36047a91915b7efd12f6d424533"
V4_CHECKER_BYTES = 21_594
V4_MODULE = "_d972_157em_pinned_157el_checker_v4"
SCHEMA = "d972-b345-target6-dual-colgen/v2"
OUTPUT = Path("ci/out/d972_b345_target6_dual_colgen_v2.json")
WIDTH = 154

TERMINALS = {
    "B345_E4_D2_COLGEN_TARGET6_CONSISTENT",
    "B345_E4_D2_COLGEN_TARGET6_FULL_D2_OBSTRUCTION",
    "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_RESOURCE",
    "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT",
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

# Independent literal mirror of the only 24 reachable imported cap values.
# Envelope validation never derives authority from a producer receipt or a
# dynamically loaded producer module.
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


def cap_comparator(key: str, source: str) -> str:
    require(source in {"local", "upstream"}, "checker cap comparator source")
    if source == "local":
        return "ge" if key in {"common_math_soft_deadline_seconds",
                                "producer_soft_rss_bytes"} else "gt"
    return "ge" if key in UPSTREAM_GE_CAPS else "gt"


def validate_bounded_active_resource(detail: dict[str, Any], batches: int,
        generation: int, total_blocks: int) -> None:
    """Mirror the producer's total-block-before-batch terminal decision."""
    require(type(batches) is int and 0 <= batches <=
                CAPS["column_generation_batches"] and
            type(generation) is int and generation >= 1 and
            type(total_blocks) is int and
                0 <= total_blocks <= CAPS["total_new_translation_blocks"],
            "checker bounded ACTIVE inputs")
    if total_blocks == CAPS["total_new_translation_blocks"]:
        key, observed, why = ("total_new_translation_blocks",
            CAPS["total_new_translation_blocks"]+1,
            "total_translation_block_budget_exhausted")
    else:
        require(batches == CAPS["column_generation_batches"],
                "checker bounded ACTIVE cap contact")
        key, observed, why = ("column_generation_batches",
            CAPS["column_generation_batches"]+1,
            "column_generation_batch_limit")
    require(detail["cap_source"] == "local" and detail["cap_key"] == key and
            detail["cap_reason"] == key and detail["cap_limit"] == CAPS[key] and
            detail["observed_count"] == observed and
            detail["comparator"] == "gt" and
            detail["phase"] == "correlation_pass1" and
            detail["inner_phase"] is None and
            detail["detail"] == why and detail["current"] == {
                "generation": generation, "completed_batches": batches,
                "completed_blocks": total_blocks},
            "checker exact bounded ACTIVE resource")


MONITOR_REGISTRY: dict[str, frozenset[str]] = {
    "authenticated_input": frozenset({"authenticated_input"}),
    "source_preflight": frozenset({"affine_source_preflight"}),
    "fresh_B0": frozenset({"fresh_B0", "strong_wform_fresh_BFS",
        "strong_wform_directed_round", "packed_provenance_dag_growth",
        "packed_pivot_column_elimination", "packed_target_sparse_elimination",
        "proof_DAG_array_bytes", "proof_DAG_base64",
        "proof_DAG_base64_complete"}),
    "fixed_B1": frozenset({"fixed_B1", "raw_lambda_reverse_dp", "dual_correlation",
        "block_insertion", "affine_full_remainder",
        "packed_provenance_dag_growth", "packed_pivot_column_elimination",
        "proof_DAG_array_bytes", "proof_DAG_base64",
        "proof_DAG_base64_complete"}),
    "initial_target": frozenset({"initial_target", "target_reduction", "affine_full_remainder",
        "affine_remainder", "affine_transposed_row_absorption"}),
    "dual_lift": frozenset({"raw_lambda_reverse_dp"}),
    "correlation_pass1": frozenset({"correlation_pass1"}),
    "correlation_pass2": frozenset({"correlation_pass2"}),
    "batch_precompute": frozenset({"batch_precompute"}),
    "section_recovery": frozenset({"section_recovery",
        "proof_DAG_array_bytes", "proof_DAG_base64",
        "proof_DAG_base64_complete"}),
    "block_commit": frozenset({"block_commit",
        "packed_provenance_dag_growth", "packed_pivot_column_elimination"}),
    "incremental_reduction": frozenset({"incremental_reduction",
        "affine_full_remainder", "affine_remainder"}),
    "target_resolve": frozenset({"affine_transposed_row_absorption"}),
    "selected_proof": frozenset({"packed_target_sparse_elimination",
        "packed_provenance_dag_growth", "proof_DAG_pre_serialization_RSS",
        "proof_DAG_reachability", "proof_DAG_compact_serialization",
        "proof_DAG_array_bytes", "proof_DAG_base64",
        "proof_DAG_base64_complete"}),
    "receipt_serialization": frozenset({"receipt_serialization"}),
    "complete": frozenset(),
}
MONITOR_PUBLIC = {key: sorted(value) for key, value in MONITOR_REGISTRY.items()}
MONITOR_SHA = hashlib.sha256(json.dumps(MONITOR_PUBLIC, sort_keys=True,
    separators=(",", ":")).encode("utf-8")).hexdigest()
RECOVERY_ENCODING = (
    "key=component-u8|result-E4-blob154; direct-tie=00|source-u16be|"
    "source-offset-u32be where source<109 means signed-letter-offset and "
    "source=108+relator means canonical-base-term-ordinal; "
    "translated-tie=01|translation-blob154|relator-u8|term-u16be|"
    "parent-blob154; direct-parent precedes translated")

# These progress shapes and imported throw sites are reconstructed here,
# independently of the producer.  A cap name is not authority to move an
# imported exception to a different outer phase or public progress shape.
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


def _build_upstream_throw_sites() \
        -> dict[str, frozenset[tuple[str, str, str]]]:
    rows: dict[str, set[tuple[str, str, str]]] = {}

    def add(keys: Iterable[str], outer: str, shape: str,
            inner: str | None = None) -> None:
        for key in keys:
            rows.setdefault(key, set()).add(
                (outer, key if inner is None else inner, shape))

    add({"provenance_dag_nodes", "provenance_dag_edges",
         "total_sparse_group_ring_keys", "single_sparse_elimination_row",
         "target_elimination_support", "sparse_pivot_rows", "element_pool",
         "section_slp_nodes", "directed_section_expr_nodes",
         "directed_section_expr_edges"}, "fresh_B0", "empty")
    add({"raw_lambda_recursion_edges"}, "fixed_B1", "empty",
        "raw_lambda_reverse_dp")
    add({"pair_attempts", "distinct_correlation_candidates"},
        "fixed_B1", "fixed_correlation_pair", "dual_correlation")
    add({"packed_active_rows"}, "fixed_B1", "fixed_correlation_post",
        "dual_correlation")
    add({"single_word_or_section_length", "directed_section_expr_nodes",
         "directed_section_expr_edges"}, "fixed_B1", "empty")
    add({"single_word_or_section_length", "provenance_dag_nodes",
         "provenance_dag_edges", "total_sparse_group_ring_keys",
         "single_sparse_elimination_row", "target_elimination_support",
         "sparse_pivot_rows", "element_pool", "directed_unique_translations"},
        "fixed_B1", "fixed_block")
    add({"single_word_or_section_length", "target_elimination_support",
         "element_pool", "wordexpr_nodes_per_candidate",
         "wordexpr_edges_per_candidate", "wordexpr_flat_leaves_per_candidate",
         "wordexpr_expanded_letter_count_per_target",
         "candidate_live_gradient_entries_total", "affine_rows",
         "dual_provenance_entries"}, "initial_target", "initial_target")
    add({"target_live_remainders"}, "initial_target", "initial_target",
        "target_reduction")
    add({"directed_section_expr_nodes", "directed_section_expr_edges"},
        "section_recovery", "empty")
    add({"single_word_or_section_length"}, "section_recovery", "section_node")
    add({"provenance_dag_nodes", "provenance_dag_edges",
         "total_sparse_group_ring_keys", "single_sparse_elimination_row",
         "sparse_pivot_rows", "element_pool", "directed_section_expr_nodes",
         "directed_section_expr_edges", "directed_unique_translations"},
        "block_commit", "block")
    add({"element_pool", "target_elimination_support"},
        "incremental_reduction", "incremental")
    add({"affine_rows", "target_live_remainders", "dual_provenance_entries"},
        "target_resolve", "empty")
    add({"single_word_or_section_length", "provenance_dag_nodes",
         "provenance_dag_edges", "target_elimination_support", "element_pool",
         "wordexpr_nodes_per_candidate", "wordexpr_edges_per_candidate",
         "wordexpr_flat_leaves_per_candidate",
         "candidate_live_gradient_entries_total"},
        "selected_proof", "selected")
    return {key: frozenset(value) for key, value in sorted(rows.items())}


UPSTREAM_THROW_SITES = _build_upstream_throw_sites()
UPSTREAM_THROW_SITES_PUBLIC = {
    key: [{"outer": outer, "inner": inner, "current_shape": shape}
          for outer, inner, shape in sorted(value)]
    for key, value in UPSTREAM_THROW_SITES.items()}
UPSTREAM_THROW_SITES_SHA = hashlib.sha256(json.dumps(
    UPSTREAM_THROW_SITES_PUBLIC, sort_keys=True,
    separators=(",", ":")).encode("utf-8")).hexdigest()
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
ALGORITHM_PUBLIC = {"name": "bounded-full-D2-dual-column-generation",
    "version": 2, "max_batches": 12, "max_translations_per_batch": 1024,
    "max_total_new_translation_blocks": 4096,
    "relators_per_block": 11, "max_total_new_relator_columns": 45056,
    "target_ordinal": 6, "variable_count": 108,
    "candidate_order": "fixed registered seed order 1..108",
    "batch_order": "canonical translation blob then relator 1..11",
    "first_consistent_stops": True, "targets_7_33_scanned": False,
    "monitor_registry": MONITOR_PUBLIC,
    "monitor_registry_sha256": MONITOR_SHA,
    "registered_monitor_pair_count": sum(map(len, MONITOR_REGISTRY.values())),
    "upstream_throw_sites": UPSTREAM_THROW_SITES_PUBLIC,
    "upstream_throw_sites_sha256": UPSTREAM_THROW_SITES_SHA,
    "registered_upstream_throw_site_count": sum(
        map(len, UPSTREAM_THROW_SITES.values())),
    "recovery_encoding": RECOVERY_ENCODING}
TERMINAL_REASONS = {
    "B345_E4_D2_COLGEN_TARGET6_CONSISTENT":
        "registered_108_target6_consistent_mod_generated_D2",
    "B345_E4_D2_COLGEN_TARGET6_FULL_D2_OBSTRUCTION":
        "complete_full_D2_correlation_zero",
    "B345_E4_D2_COLGEN_TARGET6_UNKNOWN_INPUT":
        "authenticated_input_failure"}
GENERATION_KEYS = {"generation", "basis", "target", "raw_lambda",
    "correlation", "preflight", "commit", "incremental", "classification"}
BASIS_ACCOUNTING_KEYS = {"columns", "pivots", "dependent",
    "live_sparse_entries", "pool_size", "pool_order_sha256", "DAG_nodes",
    "DAG_edges", "section_bindings", "section_expression_nodes",
    "section_expression_edges", "recovery"}
TARGET_KEYS = {"generation", "variables", "equations", "rank", "nullity",
    "consistent", "row_space_sha256", "remainders_sha256",
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
    "selection_order", "first_active", "full_E4_enumerated",
    "pool_or_basis_mutated", "cumulative_pass1_pairs",
    "cumulative_pass2_pairs"}
PREFLIGHT_KEYS = {"generation", "translation_count", "column_count",
    "staged_sparse_entries", "all_selected_before_mutation",
    "all_eleven_before_mutation", "state_neutrality_before",
    "state_neutrality_after", "section_provenance", "row_binding_sha256"}
SECTION_PROVENANCE_KEYS = {"selected", "selected_count", "selected_sha256",
    "expression_DAG", "owned_inverse_materializer",
    "materialization_cadence", "all_values_exact"}
SECTION_SELECTED_KEYS = {"generation", "translation_ordinal",
    "translation_hex", "jstar", "correlation_scalar", "contributor",
    "g_recovery", "materialization_canary", "expression_root"}
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
    "active_row_count", "complete_76_occurrence_full_11_relator_correlation",
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
RESOURCE_KEYS = {"cap_reason", "cap_key", "cap_source", "cap_limit",
    "observed_count", "comparator", "phase", "detail", "inner_phase",
    "current"}
PARTIAL_KEYS = {"phase", "reason", "current",
    "completed_generation_count", "completed_batch_count",
    "completed_new_translation_block_count", "current_generation",
    "packed_block_ledger_prefix", "selected_proof", "full_D2_separator"}
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
EG_REACHABLE_RESOURCE_CAPS = frozenset({"pair_attempts",
    "distinct_correlation_candidates", "packed_active_rows"})
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
PROVENANCE = {"predecessor_failed_run": PREDECESSOR_FAILURE_EVIDENCE,
              "evidence_only_not_terminal_certificate": True}
BASE_OCCURRENCE_SHA = "3eacd6dc77d62c1799a55923d3c8d5313a37ceab8e78b58b07b45925a28f131d"
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
Q3_BYTES = 231_570
RECEIPT_PIN_SPECS: dict[str, tuple[Path, str, int]] = {
    "task": (TASK, TASK_SHA, TASK_BYTES),
    "157em_task": (Path("sol/luna_task_157em_b345_target6_dual_colgen.md"),
        "60df04261bfd9f30928ed51b26bd501518c05eae43b0bb8ca08507e3b6c4ca99", 43_511),
    "157em_producer": (Path("search/d972_b345_target6_dual_colgen_v1.py"),
        "8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc", 410_757),
    "157em_checker": (V1_CHECKER, V1_CHECKER_SHA, V1_CHECKER_BYTES),
    "157em_driver": (Path("search/d972_b345_target6_dual_colgen_gha_driver_v1.g"),
        "e67d6397fca2b7181710fe8baf5893f8273399dc43b6c4ec27caebe4f1a903dc", 14_634),
    "157em_reply": (Path("sol/luna_reply_157em_b345_target6_dual_colgen.md"),
        "70fc6a91a1e10316b5ef2c8ad497e4fc61479866de28b80e0402de92c1065b58", 39_427),
    "157el_producer": (Path("search/d972_b345_lexfirst_block_target6_v2.py"),
        "ad9a145f1d432afffc4dd3443dafb7d621708543730150636118d1332d83ce8a", 148_824),
    "157el_checker": (V4_CHECKER, V4_CHECKER_SHA, V4_CHECKER_BYTES),
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
CHECKER_STARTED: float | None = None
CHECKER_DEADLINE: float | None = None
CHECKER_CHECKS = 0
_V1_FIXTURE: Any | None = None


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
    """Independent canonical digest of 109 ordered semantic sparse rows."""
    require(isinstance(rows, (list, tuple)) and len(rows) == 109,
            "checker semantic remainder row count")
    canonical: list[list[tuple[tuple[int, str], int]]] = []
    for row in rows:
        require(type(row) is dict, "checker semantic remainder row type")
        entries: list[tuple[tuple[int, str], int]] = []
        for key, coefficient in row.items():
            require(type(key) is tuple and len(key) == 2 and
                    type(key[0]) is int and 1 <= key[0] <= 6 and
                    isinstance(key[1], str) and len(key[1]) == 2*WIDTH and
                    bytes.fromhex(key[1]).hex() == key[1] and
                    type(coefficient) is int and coefficient in (1, 2),
                    "checker semantic remainder coordinate")
            entries.append(((key[0], key[1]), coefficient))
        entries.sort(); canonical.append(entries)
    return sha_obj(canonical)


def validate_fresh_semantic_binding(initial: dict[str, Any],
        target: dict[str, Any], rows: Sequence[dict[tuple[int, str], int]],
        expected_ledger_digest: str) -> None:
    """Bind both public semantic claims to independently replayed rows."""
    fresh = semantic_remainders_sha256(rows)
    require(initial["semantic_remainders_sha256"] == fresh and
            target["remainders_sha256"] == fresh and
            initial["target6"]["fresh_remainder_sha256"] ==
                expected_ledger_digest and
            fresh != expected_ledger_digest,
            "checker fresh semantic/ledger binding")


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _sha256_text(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(
        character in "0123456789abcdef" for character in value)


_ZERO_VECTOR_SHA_CACHE: dict[int, str] = {}


def zero_vector_sha256(count: int) -> str:
    """Hash canonical JSON ``[0,...,0]`` without retaining a huge list."""
    require(type(count) is int and count >= 0,
            "checker zero-vector digest count")
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


def upstream_current_shape(current: dict[str, Any]) -> str:
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
    raise RuntimeError("checker unknown upstream resource current shape")


def tick(label: str, force: bool = False) -> None:
    global CHECKER_CHECKS
    CHECKER_CHECKS += 1
    if force or CHECKER_CHECKS & 1023 == 0:
        require(CHECKER_DEADLINE is not None and
                time.monotonic() < CHECKER_DEADLINE,
                "157em checker soft deadline: " + label)


def element_blob(value: Any) -> bytes:
    raw = bytes(value[0]) + bytes(value[1])
    require(len(raw) == WIDTH, "157em checker E4 blob width")
    return raw


def authenticate() -> None:
    rows = ((TASK, TASK_SHA, TASK_BYTES),
            (PRODUCER, PRODUCER_SHA, PRODUCER_BYTES),
            (V4_CHECKER, V4_CHECKER_SHA, V4_CHECKER_BYTES))
    for path, digest, size in rows:
        full = ROOT/path
        require(full.is_file() and full.stat().st_size == size and
                sha_file(full) == digest, "157em checker pin " + str(path))
    for label, (path, digest, size) in RECEIPT_PIN_SPECS.items():
        full = ROOT/path
        require(full.is_file() and full.stat().st_size == size and
                sha_file(full) == digest,
                "157em checker receipt pin " + label)


def expected_pin_rows(q3_path: Path) -> dict[str, Any]:
    rows = {label: {"path": path.as_posix(), "sha256": digest,
                    "bytes": size}
            for label, (path, digest, size) in sorted(
                RECEIPT_PIN_SPECS.items())}
    rows["q3_artifact"] = {"path": Q3_PATH.as_posix(), "sha256": Q3_SHA,
        "bytes": Q3_BYTES}
    rows["157el_crosschecked_run"] = {"run": "32401947156",
        "head": "2808c3fb61962d7180a192947fed375c754a25ce",
        "receipt_sha256":
            "746ca938a962f4d918c07ee270d4e03c3e4f75e40689f3a0507c8daff9d57053",
        "receipt_bytes": 1_314_365, "evidence_only_not_imported": True}
    return rows


def load_v4() -> Any:
    authenticate()
    existing = sys.modules.get(V4_MODULE)
    if existing is not None:
        require(Path(existing.__file__).resolve() == (ROOT/V4_CHECKER).resolve()
                and sha_file(Path(existing.__file__)) == V4_CHECKER_SHA,
                "157em checker loaded predecessor binding")
        return existing
    spec = importlib.util.spec_from_file_location(V4_MODULE, ROOT/V4_CHECKER)
    require(spec is not None and spec.loader is not None,
            "157em checker predecessor spec")
    module = importlib.util.module_from_spec(spec); sys.modules[V4_MODULE] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(V4_MODULE, None); raise
    require(module.SCHEMA == "d972-b345-lexfirst-block-target6/v2" and
            module.OUTPUT.as_posix().endswith(
                "d972_b345_lexfirst_block_target6_v2.json"),
            "157em checker predecessor API")
    module.authenticate_wrapper()
    return module


def load_v1_fixture() -> Any:
    """Load the frozen v1 checker only for inherited bounded self-tests."""
    global _V1_FIXTURE
    authenticate()
    if _V1_FIXTURE is not None:
        return _V1_FIXTURE
    spec = importlib.util.spec_from_file_location(
        V1_CHECKER_MODULE, ROOT/V1_CHECKER)
    require(spec is not None and spec.loader is not None,
            "checker v1 fixture spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[V1_CHECKER_MODULE] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(V1_CHECKER_MODULE, None)
        raise
    require(Path(module.__file__).resolve() == (ROOT/V1_CHECKER).resolve() and
            Path(module.__file__).stat().st_size == V1_CHECKER_BYTES and
            sha_file(Path(module.__file__)) == V1_CHECKER_SHA and
            module.SCHEMA == "d972-b345-target6-dual-colgen/v1" and
            callable(module.self_test) and
            callable(module.predecessor_modules),
            "checker v1 fixture binding")
    _V1_FIXTURE = module
    return module


_PREDECESSOR_RUNTIME: tuple[Any, Any, Any, Any, Any, Any] | None = None
_PREDECESSOR_FIXTURE_REUSE: bool | None = None


def predecessor_modules(*, fixture_reuse: bool = False) \
        -> tuple[Any, Any, Any, Any, Any, Any]:
    """Load production modules once, or reuse the exact inherited fixtures.

    Production enters with ``fixture_reuse=False`` in a fresh checker process.
    The bounded self-test first runs the inherited v4 chain, which intentionally
    leaves the two lower checker modules bound; it must therefore use the
    pinned v2 reuse gate instead of attempting a colliding fresh import.
    """
    global _PREDECESSOR_RUNTIME, _PREDECESSOR_FIXTURE_REUSE
    if _PREDECESSOR_RUNTIME is not None:
        require(_PREDECESSOR_FIXTURE_REUSE is fixture_reuse,
                "157em checker predecessor lifecycle mode")
        return _PREDECESSOR_RUNTIME
    v4 = load_v4(); v3 = v4.load_v3_checker(); v2 = v3.load_v2_checker()
    v4.install_accounting_repair(v2)
    eh = v2.load_eh_checker(); eg = eh.load_v1_checker()
    if fixture_reuse:
        ed, old = v2.loaded_fixture_checker_modules(eg)
    else:
        ed = eg.load_ed_checker(); old = ed.load_old()
    require(callable(ed.replay_prefix) and callable(v2._replay_block) and
            callable(old.checker_target6_formula) and
            callable(old.checker_probe_remainder),
            "157em checker predecessor API shape")
    _PREDECESSOR_RUNTIME = (v2, eh, eg, ed, old, v4)
    _PREDECESSOR_FIXTURE_REUSE = fixture_reuse
    return _PREDECESSOR_RUNTIME


def expected_upstream_caps(eg: Any, ed: Any, old: Any) -> dict[str, int]:
    rows = {key: int(old.CAPS[key]) for key in OLD_REACHABLE_RESOURCE_CAPS}
    for key in OLD_AFFINE_REACHABLE_RESOURCE_CAPS:
        value = int(old.AFFINE_CAPS[key])
        require(key not in rows or rows[key] == value,
                "checker old affine cap collision")
        rows[key] = value
    for key in ED_REACHABLE_RESOURCE_CAPS:
        require(hasattr(ed, "CAPS_157ED") and key in ed.CAPS_157ED,
                "checker 157ed cap registry API")
        rows[key] = int(ed.CAPS_157ED[key])
    for key in EG_REACHABLE_RESOURCE_CAPS:
        rows[key] = int(eg.CAPS[key])
    expected = (OLD_REACHABLE_RESOURCE_CAPS |
        OLD_AFFINE_REACHABLE_RESOURCE_CAPS | ED_REACHABLE_RESOURCE_CAPS |
        EG_REACHABLE_RESOURCE_CAPS)
    require(set(rows) == set(expected) == set(UPSTREAM_THROW_SITES) ==
            set(EXPECTED_UPSTREAM_CAPS) and rows == EXPECTED_UPSTREAM_CAPS and not {
        "transaction_trace_records", "blocker_table", "directed_columns",
        "candidate_element_pool_suffix",
        "missing_bounded_inverse_representative"} & set(rows),
        "checker exact reachable upstream registry")
    return dict(sorted(rows.items()))


def configure_deadlines(v2: Any, eg: Any, ed: Any, old: Any) -> None:
    require(CHECKER_STARTED is not None and CHECKER_DEADLINE is not None,
            "157em checker deadline initialized")
    v2.CHECKER_STARTED = CHECKER_STARTED; v2.CHECKER_DEADLINE = CHECKER_DEADLINE
    v2.CHECKER_CHECKS = 0
    eg.CHECKER_STARTED = CHECKER_STARTED; eg.CHECKER_DEADLINE = CHECKER_DEADLINE
    eg.CHECKER_CHECKS = 0; eg.configure_deadline_bridge(ed, old)


def theorem_boundary() -> dict[str, Any]:
    return {"pinned_E4_roof_only": True, "target6_only": True,
        "registered_108_family_only": True, "targets_7_through_33_checked": False,
        "full_D2_claim_only_after_zero_complete_correlation": True,
        "typed_lift_claimed": False, "full_H3_claimed": False,
        "B4_A_claimed": False, "B4_B_claimed": False,
        "global_nonexistence_claimed": False,
        "unknown_resource_is_not_obstruction": True}


def claim_row(token: str) -> dict[str, Any]:
    claim = ("target6_registered_108_membership_mod_current_D2"
             if token.endswith("CONSISTENT") else
             "target6_registered_108_no_solution_mod_full_D2"
             if token.endswith("FULL_D2_OBSTRUCTION") else "none")
    return {"claim": claim, **theorem_boundary()}


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
            row["semantic_entry_count"] == row["direct_parent_count"]+
                row["translated_parent_count"] and
            row["candidate_edge_count"] >= row["semantic_entry_count"] and
            row["translated_candidate_edge_count"] <=
                row["candidate_edge_count"] and
            _sha256_text(row["canonical_sha256"]) and
            row["one_selected_parent_per_semantic_key"] is True and
            row["all_candidate_dicts_or_roots_retained"] is False and
            row["pool_IDs_public"] is False,
            "checker exact recovery public ledger")


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
            "checker exact basis accounting")
    if recovery == "public":
        validate_recovery_public(row["recovery"])
    else:
        require(recovery == "none" and row["recovery"] is None,
                "checker basis accounting recovery boundary")


def validate_affine_dual(dual: Any, consistent: bool) -> None:
    if consistent:
        require(dual is None, "checker consistent target has no dual")
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
            "checker exact affine dual")
    prior: str | None = None
    for equation in dual["equations"]:
        require(isinstance(equation, dict) and
                set(equation) == DUAL_EQUATION_KEYS and
                equation["coefficient"] in (1, 2) and
                isinstance(equation["label"], list) and
                len(equation["label"]) == 4 and
                equation["label"][:2] == [6, "hexagon_1_coface_0"] and
                1 <= equation["label"][2] <= 6 and
                isinstance(equation["label"][3], str) and
                len(equation["label"][3]) == 2*WIDTH,
                "checker affine dual equation typing")
        label = json.dumps(equation["label"], sort_keys=True,
                           separators=(",", ":"))
        require(prior is None or prior < label,
                "checker affine dual equation order")
        prior = label


def validate_raw_lambda_public(row: Any, target: dict[str, Any],
                               basis: dict[str, Any],
                               completed_columns: int) -> None:
    require(isinstance(row, dict) and set(row) == RAW_LAMBDA_KEYS and
            row["algorithm"] == "general-reverse-canonical-pivot-DP/v1" and
            type(row["support_count"]) is int and
            1 <= row["support_count"] <= CAPS["raw_lambda_support_entries"] and
            isinstance(row["per_component"], list) and
            len(row["per_component"]) == 6 and
            all(type(value) is int and value >= 0
                for value in row["per_component"]) and
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
            all(isinstance(canary, list) and len(canary) == 3 and
                1 <= canary[0] <= 6 and isinstance(canary[1], str) and
                len(canary[1]) == 2*WIDTH and canary[2] in (1, 2)
                for canary in (row["first_canary"], row["last_canary"])),
            "checker exact raw-lambda public ledger")


def validate_correlation_public(row: Any, generation: int,
        prior_pass1: int, prior_pass2: int,
        lambda_per_component: Sequence[int]) -> tuple[int, int]:
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
            all(type(value) is int and value >= 0
                for value in row["scalar_distribution"].values()) and
            sum(row["scalar_distribution"].values()) == row["active_row_count"] and
            row["candidate_count_before_zero_deletion"] ==
                row["active_row_count"]+row["cancellation_to_zero_count"] and
            row["active_distinct_translation_count"] <= row["active_row_count"] and
            row["selected_translation_count"] <= min(
                row["active_distinct_translation_count"],
                CAPS["translations_per_batch"]) and
            row["active_packed_row_width"] == 156 and
            row["active_packed_bytes"] == 156*row["active_row_count"] and
            all(_sha256_text(row[key]) for key in
                ("active_packed_sha256", "selected_translation_sha256",
                 "selected_bindings_sha256")) and
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
            row["pass2_pair_attempts"] == (row["pass1_pair_attempts"] if
                row["selected_translation_count"] > 0 else 0) and
            row["pass1_pair_attempts"] == sum(value*count for value, count in
                zip(lambda_per_component, [10, 12, 18, 10, 12, 14])) and
            ((row["active_row_count"] == 0 and row["first_active"] is None and
              row["selected_translation_count"] == 0) or
             (row["active_row_count"] > 0 and
              isinstance(row["first_active"], dict) and
              set(row["first_active"]) ==
                  {"translation_hex", "relator_index", "scalar"} and
              len(row["first_active"]["translation_hex"]) == 2*WIDTH and
              1 <= row["first_active"]["relator_index"] <= 11 and
              row["first_active"]["scalar"] in (1, 2))),
            "checker exact correlation ledger")
    return row["cumulative_pass1_pairs"], row["cumulative_pass2_pairs"]


def validate_preflight_public(row: Any, generation: int,
                              correlation: dict[str, Any]) -> None:
    require(isinstance(row, dict) and set(row) == PREFLIGHT_KEYS and
            row["generation"] == generation and
            1 <= row["translation_count"] <= CAPS["translations_per_batch"] and
            row["column_count"] == 11*row["translation_count"] and
            0 <= row["staged_sparse_entries"] <=
                CAPS["batch_staged_sparse_entries"] and
            row["all_selected_before_mutation"] is True and
            row["all_eleven_before_mutation"] is True and
            row["state_neutrality_before"] == row["state_neutrality_after"] and
            _sha256_text(row["row_binding_sha256"]),
            "checker exact preflight ledger")
    validate_basis_accounting(row["state_neutrality_before"],
                              pool_digest=True, recovery="none")
    section = row["section_provenance"]
    require(isinstance(section, dict) and
            set(section) == SECTION_PROVENANCE_KEYS and
            section["selected_count"] == len(section["selected"]) ==
                row["translation_count"] and
            section["selected_sha256"] == sha_obj(section["selected"]) and
            section["owned_inverse_materializer"] is True and
            section["materialization_cadence"] ==
                "first,last,and-every-64th" and
            section["all_values_exact"] is True,
            "checker exact section-provenance wrapper")
    bindings = [[item["translation_hex"], item["jstar"],
                 item["correlation_scalar"]] for item in section["selected"]]
    require(row["translation_count"] ==
                correlation["selected_translation_count"] and
            sha_bytes(b"".join(bytes.fromhex(item["translation_hex"])
                               for item in section["selected"])) ==
                correlation["selected_translation_sha256"] and
            sha_obj(bindings) == correlation["selected_bindings_sha256"],
            "checker correlation/preflight binding")


def validate_commit_public(row: Any, generation: int,
                           preflight: dict[str, Any]) -> None:
    require(isinstance(row, dict) and set(row) == COMMIT_KEYS and
            row["generation"] == generation and row["complete"] is True and
            row["translation_count"] == preflight["translation_count"] and
            row["column_count"] == 11*row["translation_count"] and
            row["rank_gain"]+row["dependent_gain"] == row["column_count"] and
            row["all_blocks_complete"] is True and
            row["all_staged_before_first_mutation"] is True and
            _sha256_text(row["outcome_semantic_sha256"]),
            "checker exact commit ledger")
    validate_basis_accounting(row["pre_accounting"], pool_digest=True,
                              recovery="public")
    validate_basis_accounting(row["post_accounting"], pool_digest=True,
                              recovery="public")
    pre, post = row["pre_accounting"], row["post_accounting"]
    first = preflight["section_provenance"]["selected"][0]
    pivot = row["first_translation_jstar_pivot"]
    require(set(pivot) == {"translation_ordinal", "relator", "scalar", "pivot"}
            and pivot["translation_ordinal"] == 1 and
            pivot["relator"] == first["jstar"] and
            pivot["scalar"] == first["correlation_scalar"] and
            isinstance(pivot["pivot"], list) and len(pivot["pivot"]) == 2 and
            post["columns"]-pre["columns"] == row["column_count"] and
            post["pivots"]-pre["pivots"] == row["rank_gain"] and
            post["dependent"]-pre["dependent"] == row["dependent_gain"] and
            post["recovery"]["translated_candidate_edge_count"]-
                pre["recovery"]["translated_candidate_edge_count"] ==
                76*row["translation_count"],
            "checker commit accounting/jstar binding")


def validate_incremental_public(row: Any, generation: int,
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
                 "last_fully_updated_row_sha256",
                 "current_new_pivot_prefix_sha256", "reduction_order_sha256",
                 "old_pivot_set_sha256", "completed_quotient_prefix_sha256",
                 "post_update_remainder_sha256")) and
            row["quotient_rows_discarded_on_failure"] is False and
            row["batch_anchor_committed"] is True and
            row["rolled_back_on_failure"] is False and
            0 <= row["live_entry_count"] <= CAPS["target_live_remainders"] and
            [item.get("ordinal") for item in row["fresh_direct_cadence"]] ==
                [0, 1, 54, 108] and
            all(set(item) == {"ordinal", "sha256", "equal"} and
                _sha256_text(item["sha256"]) and item["equal"] is True
                for item in row["fresh_direct_cadence"]),
            "checker exact incremental ledger")


class CheckerRecovery:
    """Checker-owned semantic recovery table; no producer IDs are consumed."""
    DIRECT = 0
    TRANSLATED = 1

    def __init__(self) -> None:
        self.rows: dict[tuple[int, bytes], tuple[bytes, dict[str, Any]]] = {}
        self.candidates = 0; self.direct_candidates = 0
        self.translated_candidates = 0; self.replacements = 0
        self.direct_keys: set[tuple[int, bytes]] = set()

    @staticmethod
    def direct_tie(source: int, offset: int) -> bytes:
        require(0 <= source <= 65535 and 1 <= offset <= 0xffffffff,
                "checker direct recovery range")
        return b"\x00"+struct.pack(">HI", source, offset)

    @staticmethod
    def translated_tie(translation: bytes, relator: int, term: int,
                       parent: bytes) -> bytes:
        require(len(translation) == len(parent) == WIDTH and
                1 <= relator <= 11 and 1 <= term <= 65535,
                "checker translated recovery range")
        return b"\x01"+translation+bytes([relator])+struct.pack(">H", term)+parent

    def _store(self, key: tuple[int, bytes], tie: bytes,
               descriptor: dict[str, Any]) -> None:
        prior = self.rows.get(key)
        if prior is None:
            require(len(self.rows)+1 <= CAPS["raw_coordinate_recovery_nodes"],
                    "checker recovery node cap")
            self.rows[key] = (tie, descriptor); return
        if tie < prior[0]:
            self.rows[key] = (tie, descriptor); self.replacements += 1

    def direct(self, component: int, blob: bytes,
               source: int, offset: int) -> None:
        require(1 <= component <= 6 and len(blob) == WIDTH,
                "checker recovery direct key")
        key = (component, blob)
        attempted = len(self.direct_keys)+(key not in self.direct_keys)
        require(attempted <= CAPS["raw_coordinate_parent_entries"],
                "checker raw parent cap")
        self.direct_keys.add(key); self.candidates += 1
        self.direct_candidates += 1; tie = self.direct_tie(source, offset)
        if source < 109:
            descriptor = {"kind": "direct_target_source_prefix",
                "component": component, "element_hex": blob.hex(),
                "source_word_ordinal": source,
                "signed_letter_offset": offset}
        else:
            require(109 <= source <= 119,
                    "checker direct base source encoding")
            descriptor = {"kind": "direct_base_support_prefix",
                "component": component, "element_hex": blob.hex(),
                "relator_index": source-108, "term_ordinal": offset}
        self._store(key, tie, descriptor)

    def translated(self, component: int, blob: bytes, translation: bytes,
                   relator: int, term: int, parent: bytes) -> None:
        self.candidates += 1; self.translated_candidates += 1
        require(self.translated_candidates <=
                CAPS["raw_coordinate_recovery_edges"],
                "checker recovery edge cap")
        tie = self.translated_tie(translation, relator, term, parent)
        descriptor = {"kind": "registered_translation_times_base_prefix",
            "component": component, "element_hex": blob.hex(),
            "translation_hex": translation.hex(), "relator_index": relator,
            "term_ordinal": term, "parent_hex": parent.hex()}
        self._store((component, blob), tie, descriptor)

    def descriptor(self, component: int, blob: bytes) -> dict[str, Any]:
        row = self.rows.get((component, blob))
        require(row is not None, "checker recovery parent exists")
        return dict(row[1])

    def public(self) -> dict[str, Any]:
        digest = hashlib.sha256(); kinds = [0, 0]
        for key in sorted(self.rows):
            tie, descriptor = self.rows[key]
            kinds[0 if descriptor["kind"].startswith("direct_") else 1] += 1
            digest.update(bytes([key[0]])+key[1]); digest.update(
                struct.pack(">H", len(tie))); digest.update(tie)
        return {"encoding": RECOVERY_ENCODING,
            "semantic_entry_count": len(self.rows),
            "direct_parent_count": kinds[0],
            "raw_coordinate_parent_entry_count": len(self.direct_keys),
            "translated_parent_count": kinds[1],
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


def numbered_occurrences(eg: Any, old: Any, e4: Any) \
        -> tuple[list[dict[str, Any]], dict[str, Any]]:
    bundle = eg.checker_base_bundle(old, e4)
    rows: list[dict[str, Any]] = []
    for ordinal, source in enumerate(bundle["private_occurrences"], 1):
        relator = int(source["relator_index"])
        prior = sum(int(row["relator_index"]) == relator for row in rows)
        rows.append({**source, "occurrence_ordinal": ordinal,
                     "term_ordinal": prior+1})
    projection = [{key: row[key] for key in
        ("relator_index", "component", "coefficient", "element_hex",
         "section_word")} for row in rows]
    require(len(rows) == 76 and [row["occurrence_ordinal"] for row in rows] ==
            list(range(1, 77)) and projection ==
            bundle["public"]["occurrences"] and
            sha_obj(projection) == BASE_OCCURRENCE_SHA,
            "checker numbered base occurrences")
    return rows, bundle["public"]


def independent_base_columns(old: Any, e4: Any,
        occurrences: Sequence[dict[str, Any]]) \
        -> list[tuple[dict[tuple[int, Any], int], Any]]:
    """Rebuild the eleven typed base columns independently of the producer."""
    relations = old.pure_relations(4)
    require(len(relations) == 11, "checker exact eleven base relations")
    answer: list[tuple[dict[tuple[int, Any], int], Any]] = []
    for relator, word in enumerate(relations, 1):
        from_occurrences: dict[tuple[int, Any], int] = {}
        for occurrence in occurrences:
            if int(occurrence["relator_index"]) == relator:
                old.add(from_occurrences,
                    (int(occurrence["component"]), occurrence["_value"]),
                    int(occurrence["coefficient"]))
        typed, quotient_value = old.fox(word, e4)
        require(typed == from_occurrences and quotient_value == e4.identity and
                old.boundary1(typed, e4) == {},
                "checker independent typed base column/D1")
        answer.append((typed, quotient_value))
    require(len(answer) == 11, "checker typed base column count")
    return answer


def record_complete_relator(masks: dict[bytes, int], blob: bytes,
                            relator: int) -> None:
    require(len(blob) == WIDTH and 1 <= relator <= 11,
            "checker complete block semantic row")
    bit = 1 << (relator-1); prior = masks.get(blob, 0)
    require(prior & bit == 0, "checker duplicate complete-block relator")
    masks[blob] = prior | bit


def complete_registry(masks: dict[bytes, int], count: int) -> dict[str, Any]:
    require(len(masks) == count and all(value == 0x7ff
            for value in masks.values()), "checker complete block registry")
    rows = sorted(masks)
    return {"translation_count": count, "relators_per_translation": 11,
        "all_masks_equal_0x7ff": True,
        "canonical_translation_sha256": sha_bytes(b"".join(rows)),
        "semantic_blob_order": "exact E4 blob lexicographic",
        "pool_IDs_public": False}


def recovery_basis_class(old: Any, recovery: CheckerRecovery,
                         occurrences: Sequence[dict[str, Any]],
                         complete_masks: dict[bytes, int]) -> type:
    parent = old.ReplayBasis
    by_relator = {j: [row for row in occurrences
                      if int(row["relator_index"]) == j]
                   for j in range(1, 12)}

    class Instrumented(parent):  # type: ignore[misc,valid-type]
        def add_column(self, relator: int, translation: int) -> bool:
            # The frozen EI fixed-B1 block deliberately dispatches directly
            # to the base reducer and reconstructs its 76 semantic recovery
            # edges afterwards.  Preserve that schedule explicitly instead
            # of accidentally instrumenting B1 merely because this checker
            # keeps the B0 subclass instance alive.
            if getattr(self, "_em_disable_instrumentation", False):
                return super().add_column(relator, translation)
            t_blob = self.pool.values[translation]; t = self.pool.value(translation)
            pending = []
            for row in by_relator[relator]:
                value = self.pool.q.mul(t, row["_value"])
                pending.append((int(row["component"]), element_blob(value),
                    t_blob, relator, int(row["term_ordinal"]),
                    bytes.fromhex(row["element_hex"])))
            require(recovery.translated_candidates+len(pending) <=
                    CAPS["raw_coordinate_recovery_edges"] and
                    len(recovery.rows)+len({(row[0], row[1]) for row in pending
                        if (row[0], row[1]) not in recovery.rows}) <=
                    CAPS["raw_coordinate_recovery_nodes"],
                    "checker recovery precommit reservation")
            result = super().add_column(relator, translation)
            for edge in pending:
                recovery.translated(*edge)
            record_complete_relator(complete_masks, t_blob, relator)
            return result

    return Instrumented


def replay_B0(ed: Any, old: Any, data: dict[str, Any], e4: Any,
              normalized: dict[str, Any], base_key: Sequence[Any],
              recovery: CheckerRecovery,
              occurrences: Sequence[dict[str, Any]],
              complete_masks: dict[bytes, int]) \
        -> tuple[Any, Any, list[dict[str, Any]]]:
    public_names = ("counts", "accounting", "basis_gate",
        "prefix_pool_checkpoint", "dependent_events", "dependent_event_count",
        "dependent_event_sha256", "fresh_not_imported", "source_sha256")
    projected = {"directed_base_support": data["directed_base_support"],
        "directed_surgery": data["directed_surgery"],
        "prefix": {name: data["prefix_B0"][name] for name in public_names}}
    original = old.ReplayBasis
    old.ReplayBasis = recovery_basis_class(
        old, recovery, occurrences, complete_masks)
    try:
        pool, basis, events = ed.replay_prefix(
            old, projected, e4, normalized, base_key)
    finally:
        old.ReplayBasis = original
    require(_sha256_text(data["prefix_B0"]["pool_order_sha256"]) and
            data["prefix_B0"]["counts"] == {
                "columns": 362725, "pivots": 362709,
                "dependent_columns": 16, "live_sparse_entries": 3090367,
                "row_tail_visits": 2727658, "BFS_translations": 32768,
                "directed_translations": 207},
            data["prefix_B0"]["complete_block_registry"] ==
                complete_registry(complete_masks, 32975),
            "checker B0 pool/count/complete-block anchor")
    return pool, basis, events


def replay_fixed_B1_prefix(v2: Any, old: Any, e4: Any, pool: Any,
                           basis: Any, oracle: Any,
                           claimed: dict[str, Any] | None, *,
                           completed: int = 11, raw_count: int = 11,
                           shadow_count: int = 11) \
        -> tuple[dict[str, Any], int, list[dict[str, Any]]]:
    """Replay the frozen direct-base-dispatch B1 schedule exactly once."""
    sentinel = object()
    prior = getattr(basis, "_em_disable_instrumentation", sentinel)
    require(prior is sentinel,
            "checker fixed-B1 instrumentation adapter initially detached")
    basis._em_disable_instrumentation = True
    try:
        return v2._replay_block(old, e4, pool, basis, oracle, claimed,
            completed=completed, raw_count=raw_count,
            shadow_count=shadow_count)
    finally:
        require(getattr(basis, "_em_disable_instrumentation", None) is True,
                "checker fixed-B1 instrumentation adapter identity")
        delattr(basis, "_em_disable_instrumentation")


def accounting_semantic(row: dict[str, Any]) -> dict[str, int]:
    keys = ("columns", "pivots", "dependent", "live_sparse_entries")
    require(isinstance(row, dict) and all(type(row.get(key)) is int
            for key in keys), "checker semantic accounting projection")
    return {key: int(row[key]) for key in keys}


def validate_fixed_B1_resource_prefix(v2: Any, old: Any, e4: Any,
                                      pool: Any, basis: Any, oracle: Any,
                                      current: dict[str, Any]) -> None:
    """Independently replay exactly the committed fixed-block prefix."""
    _validate_fixed_B1_progress(current)
    replayed, _, ledger = replay_fixed_B1_prefix(
        v2, old, e4, pool, basis, oracle, None,
        completed=int(current["completed_relators"]),
        raw_count=int(current["raw_completed_relators"]),
        shadow_count=int(current["shadow_completed_relators"]))
    require(current["raw_prefix"] == replayed["raw_rows"] and
            current["shadow_prefix"] == replayed["shadow_rows"] and
            current["scalar_prefix"] == replayed["old_qstar_scalars"] and
            current["block_prefix"] == ledger and
            current["rank_gain_so_far"] == replayed["rank_gain"] and
            accounting_semantic(current["block_pre_accounting"]) ==
                accounting_semantic(replayed["pre_accounting"]) and
            accounting_semantic(current["block_post_accounting"]) ==
                accounting_semantic(replayed["post_accounting"]),
            "checker fixed-B1 RESOURCE exact semantic prefix")


def semantic_key(old: Any, pool: Any, packed: int) -> tuple[int, bytes]:
    component, identifier = old.replay_unpack_key(packed)
    return component, pool.values[identifier]


def semantic_row(old: Any, pool: Any,
                 packed: dict[int, int]) -> dict[tuple[int, bytes], int]:
    return {semantic_key(old, pool, key): int(value) % 3
            for key, value in packed.items() if int(value) % 3}


def semantic_public(row: dict[tuple[int, bytes], int]) -> list[list[Any]]:
    return [[component, blob.hex(), coefficient]
            for (component, blob), coefficient in sorted(row.items())]


def semantic_bytes(row: dict[tuple[int, bytes], int]) -> bytes:
    raw = bytearray()
    for (component, blob), coefficient in sorted(row.items()):
        require(1 <= component <= 6 and len(blob) == WIDTH and
                coefficient in (1, 2), "checker semantic row")
        raw.extend(bytes([component])); raw.extend(blob); raw.append(coefficient)
    return bytes(raw)


def dot(functional: dict[tuple[int, bytes], int],
        row: dict[tuple[int, bytes], int]) -> int:
    return sum(coefficient*functional.get(key, 0)
               for key, coefficient in row.items()) % 3


def target_words(old: Any, seeds: Sequence[Sequence[int]]) -> list[list[int]]:
    mapping = old.cofaces(3)[0]
    lift = lambda word: old.substitute(old.embed_f2(word), mapping)
    r0 = lift(old.hexagon_words(old.FIXED_WORD)[0])
    rows = [r0]
    for seed in seeds:
        rs = lift(old.hexagon_words(old.reduce_word(
            old.FIXED_WORD+list(seed)))[0])
        rows.append(old.reduce_word(rs+old.inv_word(r0)))
    require(len(rows) == 109, "checker target word manifest")
    return rows


def direct_parents(e4: Any, pool: Any, recovery: CheckerRecovery,
                   words: Sequence[Sequence[int]],
                   gradients: Sequence[dict[Any, int]]) -> dict[str, Any]:
    require(len(words) == len(gradients) == 109,
            "checker parent manifest size")
    rows = []
    for source, (word, gradient) in enumerate(zip(words, gradients)):
        prefix = e4.identity; seen: set[tuple[int, bytes]] = set()
        for offset, letter in enumerate(word, 1):
            component = abs(int(letter))
            if letter > 0:
                value = prefix; prefix = e4.mul(
                    prefix, e4.generators[component-1])
            else:
                prefix = e4.mul(prefix, e4.inverse_generators[component-1])
                value = prefix
            blob = element_blob(value)
            if (component, value) in gradient:
                recovery.direct(component, blob, source, offset)
                seen.add((component, blob))
        expected = {(component, element_blob(value))
                    for component, value in gradient}
        require(seen == expected, "checker exact raw Fox parents")
        public = [[c, element_blob(v).hex(), a]
            for (c, v), a in sorted(gradient.items(),
                key=lambda item: (item[0][0], element_blob(item[0][1])))]
        rows.append({"source_word_ordinal": source, "word_length": len(word),
            "word_sha256": sha_obj(word), "gradient_entry_count": len(gradient),
            "gradient_sha256": sha_obj(public),
            "all_nonzero_terms_parented": True})
    return {"source_count": 109, "rows": rows, "rows_sha256": sha_obj(rows),
        "source_word_order": "base target6 then registered seeds 1..108",
        "signed_offset_convention":
            "positive uses prefix before letter; negative uses prefix after inverse"}


def fresh_target(v2: Any, old: Any, e4: Any, seeds: dict[str, Any],
                 source: dict[str, Any], inverse_words: Sequence[Any],
                 pool: Any, basis: Any, *, evaluated_seeds: int = 108,
                 solve_complete: bool = True) -> dict[str, Any]:
    require(source["supported"] is True and len(seeds["seed_words"]) == 108,
            "checker target source handoff")
    require(type(evaluated_seeds) is int and
            0 <= evaluated_seeds <= 108 and
            (not solve_complete or evaluated_seeds == 108),
            "checker target prefix range")
    mapping = old.cofaces(3)[0]
    r0 = old.substitute(old.embed_f2(
        old.hexagon_words(old.FIXED_WORD)[0]), mapping)
    base_raw, base_value = old.fox(r0, e4)
    base_binding = old.check_gradient_binding(
        "hexagon_1_coface_0", "hexagon", base_raw, base_value)
    require(base_value == e4.identity, "checker base target identity")
    empty = old.checker_target6_public([], e4)
    empty_detail = old.checker_target6_formula([], e4, include_gradient=True)
    require(empty_detail["direct_gradient"] == {} and
            empty_detail["direct_value"] == e4.identity,
            "checker empty target delta")
    base_rem = old.checker_probe_remainder(base_raw, pool, basis)
    delta_rows: dict[tuple[int, str], dict[int, int]] = {}
    split = []; remainder_rows = [{"ordinal": 0, "kind": "base",
        "remainder": [[c, h, a] for (c, h), a in sorted(base_rem.items(),
            key=lambda row: (row[0][0], bytes.fromhex(row[0][1])))],
        "sha256": sha_obj(sorted(base_rem.items()))}]
    formula_rows = [empty]; direct_bindings = [base_binding]
    gradients = [dict(base_raw)]; remainders = [dict(base_rem)]
    live = len(base_rem)
    for index, seed in enumerate(
            seeds["seed_words"][:evaluated_seeds], 1):
        tick("checker initial target", index % 4 == 0)
        detail = old.checker_target6_formula(seed, e4, include_gradient=True)
        delta = detail["direct_gradient"]
        require(detail["direct_value"] == e4.identity,
                "checker target delta identity")
        formula_rows.append(old.checker_target6_public_from_detail(seed, detail))
        one = [0]*108; one[index-1] = 1
        typed = old.checker_make_typed_positive(one, seeds["seed_words"])
        targets = old.checker_build_typed_target6(typed)
        root = old.checker_select_typed_target_root(targets, 6)
        evaluator = old.CheckWordExprEvaluator(targets["dag"], e4)
        evaluator.evaluate_values([root]); typed_raw = evaluator.gradients([root])[root]
        value = evaluator.values[root-1]
        predicted = dict(base_raw); old.add_scaled(predicted, delta, 1)
        require(value == e4.identity and typed_raw == predicted,
                "checker typed/direct target equality")
        binding = old.check_gradient_binding(
            "hexagon_1_coface_0", "hexagon", typed_raw, value)
        split.append({"seed_index": index, "gradient_sha256": sha_obj(binding),
            "value_identity": True, "direct_replay": True,
            "typed_replay": True})
        direct_bindings.append(binding); gradients.append(dict(delta))
        remainder = old.checker_probe_remainder(delta, pool, basis)
        remainders.append(dict(remainder)); live += len(remainder)
        require(live <= CAPS["target_live_remainders"],
                "checker target remainder cap")
        for coordinate, coefficient in remainder.items():
            delta_rows.setdefault(coordinate, {})[index-1] = coefficient
        remainder_rows.append({"ordinal": index, "kind": "delta",
            "entry_count": len(remainder),
            "sha256": sha_obj(sorted(remainder.items()))})
    prefix_public = {"typed_split": split,
        "fresh_remainders": remainder_rows,
        "direct_gradient_bindings_sha256": sha_obj(direct_bindings),
        "raw_gradients": gradients, "remainders": remainders,
        "base_raw": base_raw, "base_remainder": base_rem,
        "delta_rows": delta_rows, "live_remainder_entries": live}
    if not solve_complete:
        return prefix_public
    system = old.CheckerAffineSystem(108, (e4.degree, e4.collector.n))
    target_row, affine = v2._solve_transposed_target_core(
        old, system, base_rem, delta_rows, live,
        expected_coordinate_count=len(set(base_rem).union(delta_rows)))
    expected_target = {"ordinal": 6, "name": "hexagon_1_coface_0",
        "kind": "hexagon", "base_is_direct_not_empty_formula": True,
        "affine_rhs_is_negative_base_remainder": True,
        "empty_formula_is_zero_delta_canary": True,
        "base_gradient": base_binding,
        "base_gradient_sha256": sha_obj(base_binding),
        "formula_checks": formula_rows,
        "formula_checks_sha256": sha_obj(formula_rows),
        "typed_split": split, "typed_split_sha256": sha_obj(split),
        "direct_gradient_bindings_sha256": sha_obj(direct_bindings),
        "direct_vs_typed_count": 108, "fresh_remainders": remainder_rows,
        "fresh_remainder_count": 109,
        "fresh_remainder_sha256": sha_obj(remainder_rows),
        "old_B0_remainder_or_dual_imported": False,
        "post_block_anchor_used_for_all_109": True, "target_row": target_row,
        "old_157ec_comparison": {"receipt_sha256":
            "d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d",
            "old104_rank": 50, "full108_rank": 54,
            "old104_comparison_sha256":
                "383ac66dd41e95f0d66cf6f18e3563f4f0e21bec9d1992d7ec0cb39fab21477a",
            "evidence_only_not_imported": True}}
    require(expected_target["fresh_remainder_sha256"] ==
            B1["fresh_remainders_sha256"] and
            expected_target["typed_split_sha256"] == B1["typed_split_sha256"] and
            expected_target["direct_gradient_bindings_sha256"] ==
                B1["direct_bindings_sha256"] and
            affine["row_space_sha256"] == B1["target_row_space_sha256"] and
            affine["rank"] == 54 and affine["nullity"] == 54 and
            affine["consistent"] is False,
            "checker frozen B1 target anchors")
    public = {"target6": expected_target, "affine_system": affine,
        "fresh_B1_stable_digests_all_equal": True,
        "semantic_remainders_sha256":
            semantic_remainders_sha256(remainders),
        "raw_gradient_count": 109,
        "raw_gradients_sha256": sha_obj([semantic_public({
            (component, element_blob(value)): coefficient
            for (component, value), coefficient in gradient.items()})
            for gradient in gradients])}
    return {"public": public, "system": system, "base_raw": base_raw,
            "gradients": gradients, "remainders": remainders,
            "words": target_words(old, seeds["seed_words"])}


def validate_initial_target_resource_prefix(
        v2: Any, old: Any, e4: Any, seeds: dict[str, Any],
        source: dict[str, Any], inverse_words: Sequence[Any], pool: Any,
        basis: Any, current: dict[str, Any]) -> None:
    """Replay exactly the committed target-row prefix, never a suffix."""
    _validate_initial_target_progress(current)
    stage = current["substage"]
    if stage in {"typed_formula_setup", "base_remainder"}:
        require(current == {"substage": stage, "evaluated_seeds": 0,
            "completed_equations": 0, "current_seed": None,
            "typed_split_prefix": [], "remainder_prefix": [],
            "completed_target_system": None},
            "checker atomic initial target setup/base prefix")
        return
    count = int(current["evaluated_seeds"])
    if stage == "seed_remainder":
        require(current["current_seed"] == count+1 and count < 108 and
                current["completed_equations"] == 0 and
                current["completed_target_system"] is None,
                "checker initial target seed-prefix counters")
    else:
        require(stage == "affine_absorption" and count == 108 and
                current["current_seed"] is None,
                "checker initial target affine-prefix counters")
    replayed = fresh_target(v2, old, e4, seeds, source, inverse_words,
        pool, basis, evaluated_seeds=count, solve_complete=False)
    require(current["typed_split_prefix"] == replayed["typed_split"] and
            current["remainder_prefix"] == replayed["fresh_remainders"],
            "checker initial target exact typed/remainder prefix")
    completed = current["completed_target_system"]
    if completed is None:
        require(current["completed_equations"] == 0,
                "checker initial target uncommitted affine state")
        return
    full = fresh_target(v2, old, e4, seeds, source, inverse_words,
                        pool, basis)
    system = full["system"]; dual = system.dual_public()
    projection = {"coordinate_count": system.equations,
        "rank": system.rank(), "nullity": system.nullity(),
        "consistent": False, "equations": system.equations,
        "row_space_sha256": system.digest(),
        "attempted_dual_support_count": dual["support_count"],
        "attempted_dual_sha256": sha_obj(dual)}
    require(current["completed_equations"] == system.equations and
            completed == projection and not system.consistent and
            dual["support_count"] > CAPS["dual_public_provenance_entries"],
            "checker initial target completed dual-cap projection")


def reverse_lift(old: Any, pool: Any, basis: Any, system: Any,
                 remainders: Sequence[dict[tuple[int, str], int]],
                 dependent_raw: Sequence[dict[tuple[int, bytes], int]],
                 prior_raw: Sequence[dict[tuple[int, bytes], int]]) \
        -> tuple[dict[tuple[int, bytes], int], dict[str, Any]]:
    dual = system.dual_public()
    require(not system.consistent and isinstance(dual, dict) and
            dual["normalized_rhs"] == 1 and dual["yTz_mod3"] == 2 and
            dual["support_count"] <= 109 <
                CAPS["dual_public_provenance_entries"],
            "checker normalized current dual")
    values: dict[tuple[int, bytes], int] = {}
    for equation in dual["equations"]:
        label = equation["label"]
        require(isinstance(label, list) and len(label) == 4 and
                label[0] == 6 and label[1] == "hexagon_1_coface_0",
                "checker dual coordinate label")
        key = (int(label[2]), bytes.fromhex(label[3]))
        require(key not in values and len(key[1]) == WIDTH,
                "checker unique dual support")
        coefficient = int(equation["coefficient"]) % 3
        if coefficient: values[key] = coefficient
    pivots = sorted(basis.rows, key=pool.pivot_order); edges = 0
    for ordinal, pivot in enumerate(reversed(pivots), 1):
        row = basis.rows[pivot]
        if isinstance(row, tuple): row = row[0]
        semantic = semantic_row(old, pool, row); pkey = semantic_key(old, pool, pivot)
        require(semantic.get(pkey) == 1 and pkey == min(semantic),
                "checker normalized semantic pivot")
        total = 0
        for key, coefficient in semantic.items():
            if key == pkey: continue
            require(key > pkey, "checker strict pivot tail")
            edges += 1; require(edges <= CAPS["raw_lambda_reverse_edge_visits"],
                                 "checker reverse edge cap")
            total = (total-coefficient*values.get(key, 0)) % 3
            if edges & 4095 == 0: tick("checker reverse lift")
        if total:
            values[pkey] = total
            require(len(values) <= CAPS["raw_lambda_support_entries"],
                    "checker lambda support cap")
    pivot_values = [dot(values, semantic_row(old, pool,
        basis.rows[pivot][0] if isinstance(basis.rows[pivot], tuple)
        else basis.rows[pivot])) for pivot in pivots]
    dep_values = [dot(values, row) for row in dependent_raw]
    prior_values = [dot(values, row) for row in prior_raw]
    semantic_remainders = [{(c, bytes.fromhex(h)): a for (c, h), a in row.items()}
                           for row in remainders]
    delta_values = [dot(values, row) for row in semantic_remainders[1:]]
    base_value = dot(values, semantic_remainders[0])
    require(pivot_values == [0]*len(pivots) and
            dep_values == [0]*len(dep_values) and
            prior_values == [0]*len(prior_values) and
            delta_values == [0]*108 and base_value == 2,
            "checker raw lambda annihilation/sign")
    support = semantic_public(values); packed = semantic_bytes(values)
    public = {"algorithm": "general-reverse-canonical-pivot-DP/v1",
        "support_count": len(values),
        "per_component": [sum(key[0] == component for key in values)
                          for component in range(1, 7)],
        "packed_support_sha256": sha_bytes(packed),
        "packed_support_bytes": len(packed), "pivot_count": len(pivots),
        "reverse_edge_visits": edges,
        "pivot_annihilation_sha256": sha_obj(pivot_values),
        "dependent_event_count": len(dep_values),
        "dependent_annihilation_sha256": sha_obj(dep_values),
        "completed_block_column_count": len(prior_values),
        "completed_block_annihilation_sha256": sha_obj(prior_values),
        "delta_annihilation_sha256": sha_obj(delta_values),
        "base_z_scalar": base_value, "negative_base_scalar": 1,
        "normalized_dual_whole_sha256": sha_obj(dual),
        "support_rows_not_serialized": True,
        "pool_IDs_or_old_qstar_used": False,
        "first_canary": support[0] if support else None,
        "last_canary": support[-1] if support else None}
    return values, public


def contributor_bytes(component: int, g_blob: bytes, coefficient: int,
                      occurrence: dict[str, Any]) -> bytes:
    raw = bytes([component])+g_blob+bytes([coefficient])+bytes([
        int(occurrence["relator_index"])])+struct.pack(">H", int(
            occurrence["occurrence_ordinal"]))+bytes.fromhex(
                occurrence["element_hex"])+bytes([
                    int(occurrence["coefficient"])])
    require(len(raw) == 314, "checker contributor width")
    return raw


def independent_correlation(e4: Any, pool: Any,
        support: Sequence[Sequence[Any]], occurrences: Sequence[dict[str, Any]],
        generation: int, cumulative: dict[str, int], remaining: int) \
        -> dict[str, Any]:
    """Base-major complete enumeration, independent of producer loop order."""
    by_component: dict[int, list[tuple[Any, bytes, int]]] = defaultdict(list)
    for component0, blob_hex, coefficient0 in support:
        component = int(component0); blob = bytes.fromhex(str(blob_hex))
        require(len(blob) == WIDTH and int(coefficient0) in (1, 2),
                "checker support row")
        by_component[component].append((pool.unpack(blob), blob,
                                        int(coefficient0)))
    for rows in by_component.values():
        rows.sort(key=lambda row: row[1])
    scalars: dict[tuple[bytes, int], int] = {}; pairs = 0
    for occurrence in occurrences:
        component = int(occurrence["component"]); h = occurrence["_value"]
        hinv = e4.inverse(h); h_blob = bytes.fromhex(occurrence["element_hex"])
        for g, g_blob, coefficient in by_component[component]:
            pairs += 1
            require(pairs <= CAPS["correlation_pass1_pairs_per_generation"] and
                    cumulative["pass1"]+pairs <=
                        CAPS["correlation_pass1_pairs_total"],
                    "checker pass1 cap")
            t = e4.mul(g, hinv); require(e4.mul(t, h) == g,
                                         "checker left action orientation")
            t_blob = element_blob(t); key = (t_blob, int(
                occurrence["relator_index"]))
            require(key in scalars or len(scalars) <
                    CAPS["distinct_correlation_candidates"],
                    "checker correlation candidate cap")
            scalars[key] = (scalars.get(key, 0)+coefficient*int(
                occurrence["coefficient"])) % 3
            if pairs & 4095 == 0: tick("checker correlation pass1")
    expected = sum(len(by_component[component]) * sum(
        int(row["component"]) == component for row in occurrences)
        for component in range(1, 7))
    require(pairs == expected, "checker complete correlation pairs")
    cumulative["pass1"] += pairs
    active = sorted((t, j, coefficient) for (t, j), coefficient in
                    scalars.items() if coefficient)
    require(len(active) <= CAPS["packed_active_rows"],
            "checker packed active cap")
    distinct = sorted({row[0] for row in active})
    selected = distinct[:min(len(distinct), CAPS["translations_per_batch"],
                             remaining)]
    jstar = {t: min(j for tt, j, coefficient in active if tt == t)
             for t in selected}
    scalar_map = {(t, j): coefficient for t, j, coefficient in active}
    contributors: dict[bytes, tuple[bytes, dict[str, Any]]] = {}
    selected_set = set(selected); pass2 = selected_filter = 0
    if selected:
        for occurrence in occurrences:
            component = int(occurrence["component"]); h = occurrence["_value"]
            hinv = e4.inverse(h); relator = int(occurrence["relator_index"])
            for g, g_blob, coefficient in by_component[component]:
                pass2 += 1
                require(pass2 <= CAPS["correlation_pass2_pairs_per_generation"]
                        and cumulative["pass2"]+pass2 <=
                            CAPS["correlation_pass2_pairs_total"],
                        "checker pass2 cap")
                t = e4.mul(g, hinv); t_blob = element_blob(t)
                if t_blob not in selected_set or relator != jstar[t_blob]:
                    continue
                selected_filter += 1
                raw = contributor_bytes(component, g_blob, coefficient,
                                        occurrence)
                public = {"component": component, "g_hex": g_blob.hex(),
                    "lambda_coefficient": coefficient,
                    "relator_index": relator,
                    "occurrence_ordinal": int(
                        occurrence["occurrence_ordinal"]),
                    "h_hex": occurrence["element_hex"],
                    "base_coefficient": int(occurrence["coefficient"]),
                    "translation_hex": t_blob.hex(),
                    "record_hex": raw.hex(), "record_sha256": sha_bytes(raw)}
                prior = contributors.get(t_blob)
                if prior is None or raw < prior[0]:
                    contributors[t_blob] = (raw, public)
                if pass2 & 4095 == 0: tick("checker correlation pass2")
        cumulative["pass2"] += pass2
        require(set(contributors) == selected_set,
                "checker selected contributor coverage")
    active_raw = b"".join(t+bytes([j, coefficient])
                          for t, j, coefficient in active)
    public = {"complete": True, "generation": generation,
        "pass1_pair_attempts": pairs, "pass2_pair_attempts": pass2,
        "pass2_selected_filter_count": selected_filter,
        "candidate_count_before_zero_deletion": len(scalars),
        "cancellation_to_zero_count": sum(value == 0
                                            for value in scalars.values()),
        "active_row_count": len(active),
        "active_distinct_translation_count": len(distinct),
        "scalar_distribution": {"1": sum(row[2] == 1 for row in active),
                                "2": sum(row[2] == 2 for row in active)},
        "active_packed_row_width": 156,
        "active_packed_bytes": len(active_raw),
        "active_packed_sha256": sha_bytes(active_raw),
        "selected_translation_count": len(selected),
        "selected_truncated": len(selected) < len(distinct),
        "selected_translation_sha256": sha_bytes(b"".join(selected)),
        "selected_bindings_sha256": sha_obj([[t.hex(), jstar[t],
            scalar_map[(t, jstar[t])]] for t in selected]),
        "selection_order": "exact 154-byte translation blob lexicographic",
        "first_active": None if not active else {"translation_hex":
            active[0][0].hex(), "relator_index": active[0][1],
            "scalar": active[0][2]},
        "full_E4_enumerated": False, "pool_or_basis_mutated": False,
        "cumulative_pass1_pairs": cumulative["pass1"],
        "cumulative_pass2_pairs": cumulative["pass2"]}
    return {"public": public, "active": active, "selected": selected,
        "jstar": jstar, "scalar_map": scalar_map,
        "contributors": {key: value[1] for key, value in contributors.items()}}


PACKED_LEDGER_KEYS = {"format", "translation_encoding", "translation_count",
    "translation_decoded_bytes", "translation_sha256",
    "translation_base64_length", "translation_base64_sha256",
    "translation_base64", "record_encoding", "record_endianness",
    "record_bytes", "record_count", "decoded_bytes", "decoded_sha256",
    "base64_length", "base64_sha256", "base64",
    "flags_unused_high_nibble_zero", "JSON_column_objects_used"}


def decode_packed_ledger(public: dict[str, Any]) \
        -> tuple[list[bytes], list[dict[str, Any]], bytes]:
    require(set(public) == PACKED_LEDGER_KEYS and
            public["format"] == "complete-D2-block-ledger/v1" and
            public["translation_encoding"] ==
                "exact-E4-blob154-no-padding" and
            public["record_encoding"] ==
                "generation-u8|translation-ordinal-u16le|relator-u8|flags-u8|lambda-u8|pivot-component-u8|pivot-blob154|raw-sha256|typed-sha256" and
            public["record_endianness"] == "little" and
            public["record_bytes"] == 225 and
            public["flags_unused_high_nibble_zero"] is True and
            public["JSON_column_objects_used"] is False,
            "checker packed ledger header")
    try:
        translations_raw = base64.b64decode(
            public["translation_base64"], validate=True)
        records_raw = base64.b64decode(public["base64"], validate=True)
    except Exception as exc:
        raise RuntimeError("checker packed ledger base64") from exc
    require(base64.b64encode(translations_raw).decode("ascii") ==
                public["translation_base64"] and
            base64.b64encode(records_raw).decode("ascii") == public["base64"] and
            len(translations_raw) == public["translation_decoded_bytes"] ==
                public["translation_count"]*WIDTH and
            sha_bytes(translations_raw) == public["translation_sha256"] and
            len(public["translation_base64"]) ==
                public["translation_base64_length"] and
            sha_bytes(public["translation_base64"].encode("ascii")) ==
                public["translation_base64_sha256"] and
            len(records_raw) == public["decoded_bytes"] ==
                public["record_count"]*225 and
            sha_bytes(records_raw) == public["decoded_sha256"] and
            len(public["base64"]) == public["base64_length"] and
            sha_bytes(public["base64"].encode("ascii")) ==
                public["base64_sha256"] and
            len(translations_raw) <= CAPS["packed_translation_table_bytes"] and
            len(records_raw) <= CAPS["packed_block_ledger_decoded_bytes"],
            "checker packed ledger length/digest/cap")
    translations = [translations_raw[index:index+WIDTH]
                    for index in range(0, len(translations_raw), WIDTH)]
    rows = []
    for offset in range(0, len(records_raw), 225):
        raw = records_raw[offset:offset+225]
        generation = raw[0]; ordinal = struct.unpack("<H", raw[1:3])[0]
        relator, flags, scalar, component = raw[3:7]
        pivot_blob = raw[7:161]
        require(1 <= generation <= CAPS["column_generation_batches"] and
                1 <= ordinal <= 1024 and
                1 <= relator <= 11 and flags & 0xf0 == 0 and
                flags & 0x0e == 0x0e and scalar in (0, 1, 2) and
                ((flags & 1 and 1 <= component <= 6) or
                 (not flags & 1 and component == 0 and
                  pivot_blob == bytes(WIDTH))),
                "checker packed ledger record")
        rows.append({"generation": generation,
            "translation_ordinal": ordinal, "relator": relator,
            "flags": flags, "lambda_scalar": scalar,
            "pivot_component": component, "pivot_blob": pivot_blob,
            "raw_sha256": raw[161:193].hex(),
            "typed_sha256": raw[193:225].hex()})
    require(len(rows) == 11*len(translations),
            "checker complete block ledger cardinality")
    return translations, rows, records_raw


def checker_basis_public(basis: Any, pool: Any,
                         recovery: CheckerRecovery) -> dict[str, Any]:
    """ID-free checker projection of the live reducer boundary."""
    return {"columns": basis.columns_seen, "pivots": len(basis.rows),
        "dependent": basis.dependent, "live_sparse_entries": basis.live_entries,
        "pool_size": len(pool.values), "recovery": recovery.public()}


def require_basis_public(claimed: dict[str, Any], basis: Any, pool: Any,
                         recovery: CheckerRecovery,
                         prior: dict[str, Any] | None = None) -> None:
    require(set(claimed) == BASIS_ACCOUNTING_KEYS and
            claimed["pool_order_sha256"] is None and
            claimed["columns"] == basis.columns_seen and
            claimed["pivots"] == len(basis.rows) and
            claimed["dependent"] == basis.dependent and
            claimed["live_sparse_entries"] == basis.live_entries and
            claimed["pool_size"] == len(pool.values) and
            claimed["recovery"] == recovery.public() and
            claimed["dependent"] == claimed["columns"]-claimed["pivots"] and
            all(type(claimed[key]) is int and claimed[key] >= 0 for key in
                ("DAG_nodes", "DAG_edges", "section_bindings",
                 "section_expression_nodes", "section_expression_edges")),
            "checker live generation accounting")
    if prior is not None:
        require(all(claimed[key] >= prior[key] for key in
            ("columns", "pivots", "dependent", "live_sparse_entries",
             "pool_size", "DAG_nodes", "DAG_edges", "section_bindings",
             "section_expression_nodes", "section_expression_edges")),
            "checker monotone generation accounting")


def validate_selected_sections(eg: Any, old: Any, e4: Any,
        recovery: CheckerRecovery, occurrences: Sequence[dict[str, Any]],
        correlation: dict[str, Any], preflight: dict[str, Any],
        generation: int) -> None:
    section = preflight["section_provenance"]
    require(set(section) == SECTION_PROVENANCE_KEYS and
            section["selected_count"] == len(section["selected"]) ==
                len(correlation["selected"]) and
            section["selected_sha256"] == sha_obj(section["selected"]) and
            section["owned_inverse_materializer"] is True and
            section["materialization_cadence"] ==
                "first,last,and-every-64th" and
            section["all_values_exact"] is True,
            "checker selected section envelope")
    values, words, kinds, left, right = eg.decode_expression_details(
        old, section["expression_DAG"], e4)
    require(section["expression_DAG"]["roots"] ==
            [row["expression_root"] for row in section["selected"]],
            "checker selected expression root order")
    for ordinal, (t_blob, public) in enumerate(zip(
            correlation["selected"], section["selected"]), 1):
        jstar = correlation["jstar"][t_blob]
        pair = correlation["contributors"][t_blob]
        require(set(public) == SECTION_SELECTED_KEYS and
                public["generation"] == generation and
                public["translation_ordinal"] == ordinal and
                public["translation_hex"] == t_blob.hex() and
                public["jstar"] == jstar and
                public["correlation_scalar"] ==
                    correlation["scalar_map"][(t_blob, jstar)] and
                public["contributor"] == pair,
                "checker selected correlation/contributor binding")
        root = int(public["expression_root"])
        require(0 <= root < len(values) and kinds[root] == 2,
                "checker selected PRODUCT root")
        g_node, inverse_node = int(left[root]), int(right[root])
        require(kinds[inverse_node] == 3,
                "checker selected INVERSE child")
        h_node = int(left[inverse_node])
        g_blob = bytes.fromhex(pair["g_hex"])
        h_blob = bytes.fromhex(pair["h_hex"])
        require(element_blob(values[g_node]) == g_blob and
                element_blob(values[h_node]) == h_blob and
                element_blob(values[root]) == t_blob and
                e4.mul(values[g_node], e4.inverse(values[h_node])) ==
                    values[root] and e4.mul(values[root], values[h_node]) ==
                    values[g_node], "checker selected t=g*h^-1 replay")
        matches = [row for row in occurrences
            if int(row["component"]) == int(pair["component"]) and
               int(row["relator_index"]) == int(pair["relator_index"]) and
               int(row["occurrence_ordinal"]) ==
                    int(pair["occurrence_ordinal"]) and
               row["element_hex"] == pair["h_hex"]]
        require(len(matches) == 1 and
                words[h_node] == list(matches[0]["section_word"]),
                "checker selected contributing h section")
        descriptor = recovery.descriptor(int(pair["component"]), g_blob)
        method = {"direct_target_source_prefix":
                    "target_word_signed_prefix",
                  "direct_base_support_prefix":
                    "base_D2_canonical_support_prefix",
                  "registered_translation_times_base_prefix":
                    "registered_u_times_base_prefix"}[descriptor["kind"]]
        expected_recovery = {**descriptor, "method": method,
            "word_length": len(words[g_node]),
            "word_sha256": sha_obj(words[g_node])}
        require(public["g_recovery"] == expected_recovery,
                "checker selected canonical g recovery")
        expected_canary = ordinal == 1 or ordinal == len(
            correlation["selected"]) or ordinal % 64 == 0
        canary = public["materialization_canary"]
        require((isinstance(canary, dict)) == expected_canary and
                (not expected_canary or canary == {
                    "word_length": len(words[root]),
                    "word_sha256": sha_obj(words[root]),
                    "value_hex": t_blob.hex()}),
                "checker selected materialization cadence")


def typed_semantic_projection(
        typed: dict[tuple[int, Any], int]) -> dict[tuple[int, bytes], int]:
    answer: dict[tuple[int, bytes], int] = {}
    for (component, value), coefficient in typed.items():
        require(1 <= int(component) <= 6 and int(coefficient) in (1, 2),
                "checker typed column coefficient")
        key = (int(component), element_blob(value))
        require(key not in answer, "checker typed semantic blob collision")
        answer[key] = int(coefficient)
    return answer


def independent_staged_column(old: Any, e4: Any,
        base_column: dict[tuple[int, Any], int], translation: Any,
        direct_semantic: dict[tuple[int, bytes], int],
        quotient_value: Any) -> tuple[str, str]:
    """Validate one row through the checker-only typed translation/D1 core."""
    typed = old.translate(base_column, translation, e4)
    typed_semantic = typed_semantic_projection(typed)
    boundary = old.boundary1(typed, e4)
    require(quotient_value == e4.identity,
            "checker staged relator quotient identity")
    require(boundary == {}, "checker staged translated D1 zero")
    require(typed_semantic == direct_semantic,
            "checker direct/typed translated column equality")
    return (sha_bytes(semantic_bytes(direct_semantic)),
            sha_bytes(semantic_bytes(typed_semantic)))


def stage_generation_rows(old: Any, e4: Any, pool: Any,
        occurrences: Sequence[dict[str, Any]],
        base_columns: Sequence[tuple[dict[tuple[int, Any], int], Any]],
        functional: dict[tuple[int, bytes], int],
        correlation: dict[str, Any], preflight: dict[str, Any],
        generation: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []; sparse = 0
    require(len(base_columns) == 11,
            "checker staged exact base-column universe")
    before = len(pool.values)
    for ordinal, t_blob in enumerate(correlation["selected"], 1):
        t = pool.unpack(t_blob)
        require(element_blob(t) == t_blob, "checker staged translation blob")
        for relator in range(1, 12):
            semantic: dict[tuple[int, bytes], int] = {}
            for occurrence in occurrences:
                if int(occurrence["relator_index"]) != relator:
                    continue
                key = (int(occurrence["component"]), element_blob(
                    e4.mul(t, occurrence["_value"])))
                value = (semantic.get(key, 0)+int(
                    occurrence["coefficient"])) % 3
                if value: semantic[key] = value
                else: semantic.pop(key, None)
            scalar = dot(functional, semantic)
            require(scalar == correlation["scalar_map"].get(
                (t_blob, relator), 0), "checker staged scalar equality")
            raw_sha, typed_sha = independent_staged_column(
                old, e4, base_columns[relator-1][0], t, semantic,
                base_columns[relator-1][1])
            sparse += len(semantic)
            require(sparse <= CAPS["batch_staged_sparse_entries"],
                    "checker staged sparse cap")
            rows.append({"generation": generation,
                "translation_ordinal": ordinal, "translation_blob": t_blob,
                "relator": relator, "lambda_scalar": scalar,
                "raw": semantic, "raw_sha256": raw_sha,
                "typed_sha256": typed_sha})
    require(len(pool.values) == before and
            preflight["generation"] == generation and
            preflight["translation_count"] == len(correlation["selected"]) and
            preflight["column_count"] == len(rows) and
            preflight["staged_sparse_entries"] == sparse and
            preflight["all_selected_before_mutation"] is True and
            preflight["all_eleven_before_mutation"] is True and
            preflight["state_neutrality_before"] ==
                preflight["state_neutrality_after"] and
            preflight["row_binding_sha256"] == sha_obj([[
                row["translation_blob"].hex(), row["relator"],
                row["lambda_scalar"], row["raw_sha256"], row["typed_sha256"]]
                for row in rows]), "checker all-selected/all-eleven preflight")
    return rows


def semantic_pivot_set_sha(old: Any, pool: Any,
                           keys: Sequence[int]) -> str:
    ordered = sorted(keys, key=pool.pivot_order)
    digest = hashlib.sha256(b"d972-157em-semantic-pivot-set-v1\x00"+
                            struct.pack(">I", len(ordered)))
    prior: tuple[int, bytes] | None = None
    for packed in ordered:
        key = semantic_key(old, pool, packed)
        require(prior is None or prior < key,
                "checker canonical old-pivot set")
        digest.update(bytes([key[0]])); digest.update(key[1]); prior = key
    return digest.hexdigest()


def checker_incremental(old: Any, pool: Any, basis: Any,
        prior_remainders: Sequence[dict[tuple[int, str], int]],
        old_rows: dict[int, dict[int, int]], new_keys: Sequence[int],
        raw_gradients: Sequence[dict[Any, int]], generation: int, *,
        resource_current: dict[str, Any] | None = None) \
        -> tuple[list[dict[tuple[int, str], int]], dict[str, Any]]:
    require(len(prior_remainders) == len(raw_gradients) == 109 and
            len(new_keys) == len(set(new_keys)),
            "checker incremental universe")
    old_set = set(old_rows); new_set = set(new_keys)
    quotient_unsorted: list[dict[tuple[int, bytes], int]] = []
    for packed_pivot in new_keys:
        pending = dict(basis.rows[packed_pivot]); free: dict[int, int] = {}
        while pending:
            key = min(pending, key=pool.pivot_order)
            coefficient = pending[key]
            prior = old_rows.get(key)
            if prior is None:
                free[key] = pending.pop(key); continue
            for tail, value in prior.items():
                answer = (pending.get(tail, 0)-coefficient*value) % 3
                if answer: pending[tail] = answer
                else: pending.pop(tail, None)
        require(packed_pivot in free and free[packed_pivot] == 1 and
                not old_set.intersection(free),
                "checker incremental quotient row")
        row = semantic_row(old, pool, free); pivot = semantic_key(
            old, pool, packed_pivot)
        require(min(row) == pivot and all(key == pivot or key > pivot
                                          for key in row),
                "checker incremental semantic pivot/tail")
        quotient_unsorted.append(row)
    ordered = sorted(quotient_unsorted, key=lambda row: min(row))
    require(len({min(row) for row in ordered}) == len(ordered),
            "checker unique incremental pivots")
    before = [dict(row) for row in prior_remainders]
    old_set_sha = semantic_pivot_set_sha(old, pool, list(old_rows))
    quotient_prefixes = [sha_obj([semantic_public(row)
        for row in quotient_unsorted[:count]])
        for count in range(len(quotient_unsorted)+1)]
    if resource_current is not None:
        current = resource_current
        q_done = int(current["completed_quotient_pivot_ordinal"])
        require(current["generation"] == generation and
                current["new_pivot_count"] == len(ordered) and
                current["old_pivot_count"] == len(old_rows) and
                current["old_pivot_set_sha256"] == old_set_sha and
                current["old_pivot_set_encoding"] ==
                    "domain:d972-157em-semantic-pivot-set-v1\\0|count:u32be|"
                    "repeated(component:u8,blob:154)" and
                0 <= q_done <= len(quotient_unsorted) and
                current["completed_quotient_prefix_sha256"] ==
                    quotient_prefixes[q_done] and
                current["quotient_rows_discarded_on_failure"] ==
                    (q_done < len(quotient_unsorted)) and
                current["reduction_order_sha256"] == (sha_obj([
                    semantic_public(row) for row in ordered]) if
                    q_done == len(quotient_unsorted) else None),
                "checker incremental RESOURCE quotient prefix")
    work = [dict(row) for row in before]
    for row in ordered:
        pivot = min(row); pivot_hex = (pivot[0], pivot[1].hex())
        for remainder in work:
            coefficient = remainder.get(pivot_hex, 0)
            if not coefficient: continue
            for (component, blob), value in row.items():
                key = (component, blob.hex())
                answer = (remainder.get(key, 0)-coefficient*value) % 3
                if answer: remainder[key] = answer
                else: remainder.pop(key, None)
    if resource_current is not None:
        current = resource_current
        completed = int(current["completed_new_pivot_ordinal"])
        rows_in = int(current["completed_rows_in_current_pivot"])
        require(0 <= completed <= len(ordered) and
                0 <= rows_in <= (109 if completed < len(ordered) else 0),
                "checker incremental RESOURCE row prefix range")
        partial_work = [dict(row) for row in before]
        for pivot_ordinal, row in enumerate(ordered):
            limit = 109 if pivot_ordinal < completed else (
                rows_in if pivot_ordinal == completed else 0)
            if limit == 0:
                break
            pivot = min(row); pivot_hex = (pivot[0], pivot[1].hex())
            for ordinal in range(limit):
                coefficient = partial_work[ordinal].get(pivot_hex, 0)
                if coefficient:
                    for (component, blob), value in row.items():
                        key = (component, blob.hex())
                        answer = (partial_work[ordinal].get(key, 0)-
                                  coefficient*value) % 3
                        if answer: partial_work[ordinal][key] = answer
                        else: partial_work[ordinal].pop(key, None)
        expected_last = (None if completed == 0 and rows_in == 0 else
            sha_obj(sorted(partial_work[(rows_in-1) if rows_in else 108].items())))
        committed_work = [dict(row) for row in before]
        for row in ordered[:completed]:
            pivot = min(row); pivot_hex = (pivot[0], pivot[1].hex())
            for remainder in committed_work:
                coefficient = remainder.get(pivot_hex, 0)
                if coefficient:
                    for (component, blob), value in row.items():
                        key = (component, blob.hex())
                        answer = (remainder.get(key, 0)-coefficient*value) % 3
                        if answer: remainder[key] = answer
                        else: remainder.pop(key, None)
        require(current["pre_update_remainder_sha256"] == sha_obj([
                    sorted(row.items()) for row in before]) and
                current["current_new_pivot_prefix_sha256"] == sha_obj([
                    semantic_public(row) for row in ordered[:completed]]) and
                current["last_fully_updated_row_sha256"] == expected_last and
                current["live_entry_count"] == sum(map(len, committed_work)) and
                current["batch_anchor_committed"] is True and
                current["rolled_back_on_failure"] is True and
                current["remaining_rows"] == [None]*109,
                "checker incremental RESOURCE exact attempted prefix")
    # The producer publishes four bounded cadence canaries, but the independent
    # checker must not trust those samples as a proof of the transposed update.
    # Freshly reduce every one of the 109 raw gradients through the committed
    # current basis, then retain only the frozen four ordinals in the public
    # cadence projection.
    fresh_rows: list[dict[tuple[int, str], int]] = []
    cadence_ordinals = {0, 1, 54, 108}
    cadence = []
    for ordinal, gradient in enumerate(raw_gradients):
        tick("checker incremental fresh 109", ordinal % 4 == 0)
        direct = old.checker_probe_remainder(
            gradient, pool, basis)
        require(direct == work[ordinal],
                "checker incremental/all-109 fresh direct equality")
        fresh_rows.append(dict(direct))
        if ordinal in cadence_ordinals:
            cadence.append({"ordinal": ordinal,
                "sha256": sha_obj(sorted(direct.items())), "equal": True})
    require(fresh_rows == work and
            [row["ordinal"] for row in cadence] == [0, 1, 54, 108],
            "checker all-109 fresh equality/cadence projection")
    public = {"generation": generation,
        "completed_new_pivot_ordinal": len(ordered),
        "completed_rows_in_current_pivot": 0,
        "pre_update_remainder_sha256": sha_obj([
            sorted(row.items()) for row in before]),
        "last_fully_updated_row_sha256": sha_obj(sorted(work[-1].items())),
        "current_new_pivot_prefix_sha256": sha_obj([
            semantic_public(row) for row in ordered]),
        "new_pivot_count": len(ordered),
        "reduction_order_sha256": sha_obj([
            semantic_public(row) for row in ordered]),
        "old_pivot_count": len(old_rows),
        "old_pivot_set_encoding":
            "domain:d972-157em-semantic-pivot-set-v1\\0|count:u32be|"
            "repeated(component:u8,blob:154)",
        "old_pivot_set_sha256": old_set_sha,
        "completed_quotient_pivot_ordinal": len(quotient_unsorted),
        "completed_quotient_prefix_sha256": sha_obj([
            semantic_public(row) for row in quotient_unsorted]),
        "quotient_rows_discarded_on_failure": False,
        "live_entry_count": sum(map(len, work)),
        "batch_anchor_committed": True,
        "rolled_back_on_failure": False, "complete": True,
        "post_update_remainder_sha256": sha_obj([
            sorted(row.items()) for row in work]),
        "fresh_direct_cadence": cadence}
    return work, public


def solve_remainders(v2: Any, old: Any, e4: Any,
        remainders: Sequence[dict[tuple[int, str], int]], generation: int) \
        -> tuple[Any, dict[str, Any]]:
    base = dict(remainders[0]); delta: dict[tuple[int, str], dict[int, int]] = {}
    for index, row in enumerate(remainders[1:]):
        for coordinate, coefficient in row.items():
            delta.setdefault(coordinate, {})[index] = coefficient
    system = old.CheckerAffineSystem(108, (e4.degree, e4.collector.n))
    target_row, affine = v2._solve_transposed_target_core(
        old, system, base, delta, sum(map(len, remainders)),
        expected_coordinate_count=len(set(base).union(delta)))
    target = {"generation": generation, "variables": 108,
        "equations": system.equations, "rank": system.rank(),
        "nullity": system.nullity(), "consistent": system.consistent,
        "row_space_sha256": system.digest(),
        "remainders_sha256": semantic_remainders_sha256(remainders),
        "live_remainder_entries": sum(map(len, remainders)),
        "complete_all_coordinates": True,
        "stopped_at_first_contradiction": False,
        "dual": system.dual_public()}
    require(target["equations"] == len(set().union(
        *(set(row) for row in remainders))) and
        target_row["row_space_sha256"] == target["row_space_sha256"] and
        affine["consistent"] is target["consistent"],
        "checker complete target rebuild")
    return system, target


def pool_order_sha(pool: Any) -> str:
    return sha_bytes(b"".join(pool.values))


def encode_checker_record(generation: int, ordinal: int, relator: int,
        independent: bool, scalar: int,
        pivot: list[Any] | None, raw_sha: str, typed_sha: str) -> bytes:
    flags = (1 if independent else 0) | 0x0e
    component = 0 if pivot is None else int(pivot[0])
    blob = bytes(WIDTH) if pivot is None else bytes.fromhex(str(pivot[1]))
    raw = (bytes([generation])+struct.pack("<H", ordinal)+
        bytes([relator, flags, scalar, component])+blob+
        bytes.fromhex(raw_sha)+bytes.fromhex(typed_sha))
    require(len(raw) == 225, "checker packed record encoder width")
    return raw


def replay_generation_batch(old: Any, e4: Any, pool: Any, basis: Any,
        recovery: CheckerRecovery, complete_masks: dict[bytes, int],
        correlation: dict[str, Any], staged: Sequence[dict[str, Any]],
        generation_row: dict[str, Any], packed_translations: Sequence[bytes],
        packed_rows: Sequence[dict[str, Any]] | None) \
        -> tuple[list[int], list[dict[tuple[int, bytes], int]],
                 list[dict[str, Any]], bytes]:
    generation = int(generation_row["generation"])
    commit = generation_row["commit"]
    require(set(commit) == COMMIT_KEYS and commit["generation"] == generation and
            commit["complete"] is True and
            list(packed_translations) == list(correlation["selected"]) and
            len(staged) == 11*len(correlation["selected"]) and
            (packed_rows is None or len(packed_rows) == len(staged)),
            "checker committed batch dimensions")
    pre_claim = commit["pre_accounting"]
    require(pre_claim["columns"] == basis.columns_seen and
            pre_claim["pivots"] == len(basis.rows) and
            pre_claim["dependent"] == basis.dependent and
            pre_claim["live_sparse_entries"] == basis.live_entries and
            pre_claim["pool_size"] == len(pool.values) and
            pre_claim["recovery"] == recovery.public(),
            "checker committed pre-accounting")
    new_keys: list[int] = []; new_rows: list[dict[tuple[int, bytes], int]] = []
    raw_rows: list[dict[str, Any]] = []; outcomes = []
    first: dict[str, Any] | None = None
    encoded = bytearray()
    packed_cursor = 0
    for ordinal, t_blob in enumerate(correlation["selected"], 1):
        require(complete_masks.get(t_blob, 0) == 0,
                "checker selected translation not complete")
        t_id = pool.intern(pool.unpack(t_blob))
        for relator in range(1, 12):
            row = staged[packed_cursor]
            packed = None if packed_rows is None else packed_rows[packed_cursor]
            packed_cursor += 1
            require(row["translation_ordinal"] == ordinal and
                    row["relator"] == relator and
                    (packed is None or packed["generation"] == generation and
                    packed["translation_ordinal"] == ordinal and
                    packed["relator"] == relator and
                    packed["lambda_scalar"] == row["lambda_scalar"] and
                    packed["raw_sha256"] == row["raw_sha256"] and
                    packed["typed_sha256"] == row["typed_sha256"]),
                    "checker packed staged row binding")
            before_keys = set(basis.rows)
            independent = basis.add_column(relator, t_id)
            added = sorted(set(basis.rows)-before_keys, key=pool.pivot_order)
            require(independent == (len(added) == 1),
                    "checker packed reducer independence")
            pivot: list[Any] | None = None
            if independent:
                key = added[0]; new_keys.append(key)
                semantic = semantic_row(old, pool, basis.rows[key])
                semantic_key0 = semantic_key(old, pool, key)
                require(semantic.get(semantic_key0) == 1 and
                        min(semantic) == semantic_key0,
                        "checker new normalized pivot")
                new_rows.append(semantic)
                pivot = [semantic_key0[0], semantic_key0[1].hex()]
            flags = (1 if independent else 0) | 0x0e
            require(packed is None or packed["flags"] == flags and
                    ((pivot is None and packed["pivot_component"] == 0 and
                      packed["pivot_blob"] == bytes(WIDTH)) or
                     (pivot is not None and
                      packed["pivot_component"] == pivot[0] and
                      packed["pivot_blob"].hex() == pivot[1])),
                    "checker packed pivot/flags")
            outcome = {"translation_ordinal": ordinal,
                "relator": relator, "independent": independent,
                "lambda_scalar": row["lambda_scalar"], "pivot": pivot}
            outcomes.append(outcome); raw_rows.append(dict(row["raw"]))
            encoded.extend(encode_checker_record(generation, ordinal,
                relator, independent, int(row["lambda_scalar"]), pivot,
                str(row["raw_sha256"]), str(row["typed_sha256"])))
            if ordinal == 1 and relator == correlation["jstar"][t_blob]:
                require(independent and row["lambda_scalar"] in (1, 2),
                        "checker first jstar pivot theorem")
                first = {"translation_ordinal": 1, "relator": relator,
                    "scalar": row["lambda_scalar"], "pivot": pivot}
        require(complete_masks.get(t_blob) == 0x7ff,
                "checker complete adaptive 11-relator mask")
    post = commit["post_accounting"]
    require((packed_rows is None or packed_cursor == len(packed_rows)) and
            first is not None and
            commit["translation_count"] == len(correlation["selected"]) and
            commit["column_count"] == len(outcomes) and
            commit["rank_gain"] == len(new_keys) and
            commit["dependent_gain"] == len(outcomes)-len(new_keys) and
            commit["first_translation_jstar_pivot"] == first and
            commit["outcome_semantic_sha256"] == sha_obj(outcomes) and
            commit["all_blocks_complete"] is True and
            commit["all_staged_before_first_mutation"] is True and
            post["columns"] == basis.columns_seen and
            post["pivots"] == len(basis.rows) and
            post["dependent"] == basis.dependent and
            post["live_sparse_entries"] == basis.live_entries and
            post["pool_size"] == len(pool.values) and
            post["recovery"] == recovery.public(),
            "checker committed batch public replay")
    return new_keys, new_rows, raw_rows, bytes(encoded)


def replay_partial_batch(old: Any, pool: Any, basis: Any,
        recovery: CheckerRecovery, complete_masks: dict[bytes, int],
        correlation: dict[str, Any], staged: Sequence[dict[str, Any]],
        current: dict[str, Any], prior_record_count: int) -> tuple[bytes, bytes]:
    """Replay exactly the committed translation prefix after rollback."""
    completed = int(current["completed_translations"])
    require(current["completed_translation_prefix"] == [blob.hex() for blob in
            correlation["selected"][:completed]] and
            current["completed_record_count"] ==
                prior_record_count+11*completed,
            "checker partial block translation/record prefix")
    pre = current["pre_accounting"]
    require(pre["columns"] == basis.columns_seen and
            pre["pivots"] == len(basis.rows) and
            pre["dependent"] == basis.dependent and
            pre["live_sparse_entries"] == basis.live_entries and
            pre["pool_size"] == len(pool.values) and
            pre["recovery"] == recovery.public(),
            "checker partial block pre-state")
    translations = bytearray(); records = bytearray(); cursor = 0
    for ordinal, t_blob in enumerate(correlation["selected"], 1):
        rows = staged[cursor:cursor+11]; cursor += 11
        if ordinal > completed:
            continue
        require(complete_masks.get(t_blob, 0) == 0 and
                [row["relator"] for row in rows] == list(range(1, 12)),
                "checker partial block complete selected rows")
        translations.extend(t_blob); t_id = pool.intern(pool.unpack(t_blob))
        for row in rows:
            before_keys = set(basis.rows)
            independent = basis.add_column(int(row["relator"]), t_id)
            added = sorted(set(basis.rows)-before_keys, key=pool.pivot_order)
            require(independent == (len(added) == 1),
                    "checker partial block reducer delta")
            pivot = None
            if independent:
                key = added[0]; semantic = semantic_key(old, pool, key)
                pivot = [semantic[0], semantic[1].hex()]
            records.extend(encode_checker_record(int(current["generation"]),
                ordinal, int(row["relator"]), independent,
                int(row["lambda_scalar"]), pivot,
                str(row["raw_sha256"]), str(row["typed_sha256"])))
        require(complete_masks.get(t_blob) == 0x7ff,
                "checker partial block completed mask")
    post = current["post_failure_accounting"]
    require(post["columns"] == basis.columns_seen and
            post["pivots"] == len(basis.rows) and
            post["dependent"] == basis.dependent and
            post["live_sparse_entries"] == basis.live_entries and
            post["pool_size"] == len(pool.values) and
            post["recovery"] == recovery.public(),
            "checker partial block post-rollback state")
    return bytes(translations), bytes(records)


def validate_generation_shape(rows: Any, token: str,
                              partial: dict[str, Any] | None = None) -> None:
    require(isinstance(rows, list), "checker generation ledger list")
    allowed = {None, "ACTIVE_BATCH_COMMITTED", "CONSISTENT",
               "FULL_D2_OBSTRUCTION"}
    cumulative_pass1 = cumulative_pass2 = 0
    completed_columns = 11
    prior_post: dict[str, Any] | None = None
    for index, row in enumerate(rows, 1):
        require(isinstance(row, dict) and set(row) == GENERATION_KEYS and
                row["generation"] == index and row["classification"] in allowed,
                "checker generation row exact key/order")
        basis, target = row["basis"], row["target"]
        validate_basis_accounting(basis, pool_digest=False,
                                  recovery="public")
        if prior_post is not None:
            require(all(basis[key] == prior_post[key] for key in
                BASIS_ACCOUNTING_KEYS-{"pool_order_sha256"}),
                "checker generation basis/prior commit chain")
        require(set(target) == TARGET_KEYS and target["generation"] == index and
                target["variables"] == 108 and
                type(target["equations"]) is int and target["equations"] >= 0 and
                target["rank"]+target["nullity"] == 108 and
                type(target["consistent"]) is bool and
                _sha256_text(target["row_space_sha256"]) and
                _sha256_text(target["remainders_sha256"]) and
                0 <= target["live_remainder_entries"] <=
                    CAPS["target_live_remainders"] and
                target["complete_all_coordinates"] is True and
                target["stopped_at_first_contradiction"] is False,
                "checker generation target shape")
        validate_affine_dual(target["dual"], target["consistent"])
        classification = row["classification"]
        if classification == "ACTIVE_BATCH_COMMITTED":
            require(target["consistent"] is False and all(row[key] for key in
                ("raw_lambda", "correlation",
                "preflight", "commit", "incremental")),
                "checker active generation payload")
            validate_raw_lambda_public(row["raw_lambda"], target, basis,
                                       completed_columns)
            cumulative_pass1, cumulative_pass2 = validate_correlation_public(
                row["correlation"], index, cumulative_pass1,
                cumulative_pass2, row["raw_lambda"]["per_component"])
            require(row["correlation"]["active_row_count"] > 0 and
                    row["correlation"]["selected_translation_count"] > 0,
                    "checker active correlation selection")
            validate_preflight_public(row["preflight"], index,
                                      row["correlation"])
            validate_commit_public(row["commit"], index, row["preflight"])
            validate_incremental_public(row["incremental"], index,
                                        row["commit"])
            prior_post = row["commit"]["post_accounting"]
            completed_columns += row["commit"]["column_count"]
        elif classification == "CONSISTENT":
            require(target["consistent"] is True and all(row[key] == {} for key in
                ("raw_lambda", "correlation", "preflight", "commit",
                 "incremental")), "checker consistent generation payload")
        elif classification == "FULL_D2_OBSTRUCTION":
            require(target["consistent"] is False and row["raw_lambda"] and
                    row["correlation"] and all(row[key] == {} for key in
                ("preflight", "commit", "incremental")),
                    "checker obstruction generation payload")
            validate_raw_lambda_public(row["raw_lambda"], target, basis,
                                       completed_columns)
            cumulative_pass1, cumulative_pass2 = validate_correlation_public(
                row["correlation"], index, cumulative_pass1,
                cumulative_pass2, row["raw_lambda"]["per_component"])
            require(row["correlation"]["active_row_count"] == 0,
                    "checker obstruction zero complete correlation")
        else:
            require(index == len(rows), "checker only last generation partial")
            present = [bool(row[key]) for key in ("raw_lambda", "correlation",
                "preflight", "commit", "incremental")]
            require(target["consistent"] and present == [False]*5 or
                    not target["consistent"] and
                    present == sorted(present, reverse=True),
                    "checker partial generation fill-prefix")
            if row["raw_lambda"]:
                validate_raw_lambda_public(row["raw_lambda"], target, basis,
                                           completed_columns)
            if row["correlation"]:
                cumulative_pass1, cumulative_pass2 = \
                    validate_correlation_public(row["correlation"], index,
                        cumulative_pass1, cumulative_pass2,
                        row["raw_lambda"]["per_component"])
            if row["preflight"]:
                validate_preflight_public(row["preflight"], index,
                                          row["correlation"])
            if row["commit"]:
                validate_commit_public(row["commit"], index,
                                       row["preflight"])
            if row["incremental"]:
                validate_incremental_public(row["incremental"], index,
                                            row["commit"])
    if rows:
        require(all(row["classification"] == "ACTIVE_BATCH_COMMITTED"
                    for row in rows[:-1]), "checker generation prefix classes")
        if token.endswith("CONSISTENT"):
            require(rows[-1]["classification"] == "CONSISTENT",
                    "checker terminal consistent class")
        elif token.endswith("FULL_D2_OBSTRUCTION"):
            require(rows[-1]["classification"] == "FULL_D2_OBSTRUCTION",
                    "checker terminal obstruction class")
        elif partial is not None:
            require(rows[-1]["classification"] in {
                None, "ACTIVE_BATCH_COMMITTED"},
                "checker resource final generation class")
            require(partial["completed_generation_count"] == sum(
                row["classification"] == "ACTIVE_BATCH_COMMITTED" for row in rows),
                "checker resource completed-generation count")


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
    current = receipt.get("partial", {}).get("current", {}) if isinstance(
        receipt.get("partial"), dict) else {}
    completed = current.get("completed_terminal_before_serialization") if \
        isinstance(current, dict) else None
    if completed == "B345_E4_D2_COLGEN_TARGET6_CONSISTENT" and \
            receipt["generation_ledger"]:
        expected.add("selected_proof_g"+str(
            receipt["generation_ledger"][-1]["generation"]))
    if receipt["phase"] == "complete":
        expected.add("receipt_serialization")
    elif receipt["phase"] == "receipt_serialization" and \
            current.get("serialization_phase_completed") is True:
        expected.add("receipt_serialization")
    if receipt["terminal_token"].endswith("UNKNOWN_RESOURCE") and \
            receipt["phase"] == "authenticated_input":
        expected.discard("authenticated_input")
    return expected


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
            "checker source RESOURCE prefix")


def _validate_fixed_B1_progress(current: dict[str, Any]) -> None:
    require(set(current) == FIXED_B1_PROGRESS_KEYS,
            "checker fixed-B1 RESOURCE keys")
    attempted, completed = (current["attempted_relators"],
                            current["completed_relators"])
    raw, shadow = (current["raw_completed_relators"],
                   current["shadow_completed_relators"])
    rank, relator = current["rank_gain_so_far"], current["current_relator"]
    require(all(type(value) is int for value in
                (attempted, completed, raw, shadow, rank)) and
            0 <= shadow <= raw <= 11 and 0 <= completed <= attempted <= 11 and
            0 <= rank <= completed and
            len(current["raw_prefix"]) == raw and
            len(current["shadow_prefix"]) == shadow and
            len(current["scalar_prefix"]) == shadow and
            len(current["block_prefix"]) == completed and
            isinstance(current["block_pre_accounting"], dict) and
            isinstance(current["block_post_accounting"], dict),
            "checker fixed-B1 RESOURCE counts")
    stage = current["substage"]
    if stage == "translation_section":
        require((attempted, completed, raw, shadow, rank) == (0, 0, 0, 0, 0)
                and relator is None, "checker fixed-B1 translation prefix")
    elif stage == "shadow_remainders":
        require(completed == rank == 0 and relator == attempted and
                1 <= attempted <= 11 and attempted in {raw, raw+1} and
                raw-shadow in {0, 1}, "checker fixed-B1 shadow prefix")
    else:
        require(stage == "persistent_columns" and raw == shadow == 11 and
                relator == attempted and
                completed <= attempted <= completed+1 and
                1 <= attempted <= 11,
                "checker fixed-B1 persistent prefix")


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
            len(current["typed_split_prefix"]) == current["evaluated_seeds"] and
            isinstance(current["remainder_prefix"], list) and
            len(current["remainder_prefix"]) in {
                0, current["evaluated_seeds"]+1} and
            (current["completed_target_system"] is None or
             isinstance(current["completed_target_system"], dict)),
            "checker initial-target RESOURCE prefix")
    stage = current["substage"]
    if stage in {"typed_formula_setup", "base_remainder"}:
        require(current["evaluated_seeds"] == 0 and
                current["completed_equations"] == 0 and
                current["current_seed"] is None and
                current["typed_split_prefix"] == [] and
                current["remainder_prefix"] == [] and
                current["completed_target_system"] is None,
                "checker initial target setup/base atomicity")
    elif stage == "seed_remainder":
        require(current["current_seed"] ==
                    current["evaluated_seeds"]+1 and
                len(current["remainder_prefix"]) ==
                    current["evaluated_seeds"]+1 and
                current["completed_equations"] == 0 and
                current["completed_target_system"] is None,
                "checker initial target seed atomicity")
    else:
        completed = current["completed_target_system"]
        require(current["evaluated_seeds"] == 108 and
                current["current_seed"] is None and
                len(current["typed_split_prefix"]) == 108 and
                len(current["remainder_prefix"]) == 109 and
                current["completed_equations"] in {
                    0, (completed or {}).get("equations", -1)},
                "checker initial target affine atomicity")
        if completed is not None:
            require(set(completed) == {"coordinate_count", "rank",
                "nullity", "consistent", "equations", "row_space_sha256",
                "attempted_dual_support_count", "attempted_dual_sha256"} and
                completed["consistent"] is False and
                completed["rank"]+completed["nullity"] == 108 and
                completed["coordinate_count"] == completed["equations"] and
                completed["attempted_dual_support_count"] >
                    CAPS["dual_public_provenance_entries"] and
                _sha256_text(completed["row_space_sha256"]) and
                _sha256_text(completed["attempted_dual_sha256"]),
                "checker initial target dual-cap projection")


def _validate_block_progress(current: dict[str, Any],
                             packed: dict[str, Any]) -> None:
    require(set(current) == BLOCK_PROGRESS_KEYS and
            type(current["generation"]) is int and
            1 <= current["generation"] <= CAPS["column_generation_batches"] and
            1 <= current["selected_translation_count"] <= 1024 and
            0 <= current["completed_translations"] <=
                current["selected_translation_count"] and
            current["completed_translations"] <=
                current["attempted_translation"] <= min(
                    current["selected_translation_count"],
                    current["completed_translations"]+1) and
            0 <= current["completed_relators"] <= 11 and
            0 <= current["attempted_relator"] <= 11 and
            current["batch_anchor_committed"] is False and
            type(current["unfinished_translation_rolled_back"]) is bool and
            len(current["completed_translation_prefix"]) ==
                current["completed_translations"] and
            all(isinstance(value, str) and len(value) == 2*WIDTH
                for value in current["completed_translation_prefix"]) and
            current["completed_record_count"] == packed["record_count"],
            "checker block RESOURCE prefix")
    validate_basis_accounting(current["pre_accounting"], pool_digest=True,
                              recovery="public")
    validate_basis_accounting(current["post_failure_accounting"],
                              pool_digest=True, recovery="public")
    if current["unfinished_translation_rolled_back"]:
        require(current["rollback_translation_ordinal"] ==
                    current["attempted_translation"] and
                current["completed_relators"] == 0,
                "checker block rollback prefix")
    else:
        require(current["rollback_translation_ordinal"] is None,
                "checker block nonrollback prefix")


def _validate_incremental_progress(current: dict[str, Any]) -> None:
    require(set(current) == INCREMENTAL_PROGRESS_KEYS and
            1 <= current["generation"] <= CAPS["column_generation_batches"] and
            type(current["new_pivot_count"]) is int and
            current["new_pivot_count"] >= 1 and
            0 <= current["completed_quotient_pivot_ordinal"] <=
                current["new_pivot_count"] and
            0 <= current["completed_new_pivot_ordinal"] <=
                current["new_pivot_count"] and
            0 <= current["completed_rows_in_current_pivot"] <= 109 and
            current["batch_anchor_committed"] is True and
            current["rolled_back_on_failure"] is True and
            current["remaining_rows"] == [None]*109 and
            0 <= current["live_entry_count"] <=
                CAPS["target_live_remainders"] and
            all(current[key] is None or _sha256_text(current[key]) for key in
                ("last_fully_updated_row_sha256", "reduction_order_sha256",
                 "old_pivot_set_sha256")) and
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
            "checker incremental RESOURCE rollback")


def validate_resource_detail(detail: Any, receipt: dict[str, Any],
                             upstream: dict[str, int]) -> None:
    require(isinstance(detail, dict) and set(detail) == RESOURCE_KEYS and
            detail["cap_reason"] == detail["cap_key"] == receipt["reason"] and
            detail["phase"] == receipt["phase"] in MONITOR_REGISTRY and
            detail["cap_source"] in {"local", "upstream"} and
            detail["comparator"] in {"gt", "ge"} and
            type(detail["cap_limit"]) is int and
            type(detail["observed_count"]) is int and
            isinstance(detail["current"], dict) and
            (detail["detail"] is None or isinstance(detail["detail"], str)) and
            (detail["inner_phase"] is None or
             isinstance(detail["inner_phase"], str)),
            "checker exact resource row")
    registry = CAPS if detail["cap_source"] == "local" else upstream
    require(detail["cap_key"] in registry and
            detail["cap_limit"] == registry[detail["cap_key"]] and
            detail["comparator"] == cap_comparator(
                detail["cap_key"], detail["cap_source"]) and
            ((detail["comparator"] == "gt" and
              detail["observed_count"] > detail["cap_limit"]) or
             (detail["comparator"] == "ge" and
              detail["observed_count"] >= detail["cap_limit"])),
            "checker resource cap/comparator")
    if detail["cap_source"] == "local":
        if detail["cap_key"] in {"common_math_soft_deadline_seconds",
                                  "producer_soft_rss_bytes"}:
            require(detail["inner_phase"] in
                    MONITOR_REGISTRY[detail["phase"]],
                    "checker local monitor pair")
        else:
            require(detail["inner_phase"] is None,
                    "checker local count cap inner phase")
    else:
        shape = upstream_current_shape(detail["current"])
        require(detail["cap_key"] in UPSTREAM_THROW_SITES and
                (detail["phase"], detail["inner_phase"], shape) in
                    UPSTREAM_THROW_SITES[detail["cap_key"]],
                "checker upstream throw-site binding")
    expected_detail = {
        "total_new_translation_blocks":
            "total_translation_block_budget_exhausted",
        "column_generation_batches": "column_generation_batch_limit",
    }.get(detail["cap_key"])
    require(detail["detail"] == expected_detail,
            "checker resource detail registry")


def validate_partial_public(partial: Any, detail: dict[str, Any]) -> None:
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
            "checker exact resource partial")
    packed = partial["packed_block_ledger_prefix"]
    require(set(packed) == PACKED_PARTIAL_KEYS and
            packed["format"] == "complete-D2-block-ledger/v1-partial" and
            packed["record_bytes"] == 225 and
            packed["base64_omitted_for_resource_partial"] is True and
            packed["translation_count"] ==
                partial["completed_new_translation_block_count"] and
            packed["record_count"] == 11*packed["translation_count"] and
            packed["translation_decoded_bytes"] ==
                WIDTH*packed["translation_count"] and
            packed["decoded_bytes"] == 225*packed["record_count"] and
            _sha256_text(packed["translation_sha256"]) and
            _sha256_text(packed["decoded_sha256"]) and
            partial["completed_batch_count"] in {
                partial["completed_generation_count"],
                partial["completed_generation_count"]+1} and
            (partial["current_generation"] is None or
             partial["current_generation"] in {
                partial["completed_generation_count"],
                 partial["completed_generation_count"]+1}),
            "checker packed resource partial")
    if packed["translation_count"] == 0:
        require(packed["record_count"] == 0 and
                packed["translation_sha256"] == sha_bytes(b"") and
                packed["decoded_sha256"] == sha_bytes(b""),
                "checker empty resource packed-prefix digest")


def validate_resource_current(detail: dict[str, Any],
                              receipt: dict[str, Any]) -> None:
    phase, key, current = detail["phase"], detail["cap_key"], detail["current"]
    packed = receipt["partial"]["packed_block_ledger_prefix"]
    local_monitor_empty = (detail["cap_source"] == "local" and
        key in {"common_math_soft_deadline_seconds", "producer_soft_rss_bytes"}
        and detail["inner_phase"] in MONITOR_REGISTRY[phase] and current == {})
    if phase == "authenticated_input":
        require(current == {}, "checker authenticated resource current")
    elif phase == "source_preflight":
        _validate_source_progress(current)
    elif phase == "fresh_B0":
        if current == {}:
            require(detail["cap_source"] == "upstream" or local_monitor_empty,
                    "checker B0 empty resource current")
        elif set(current) == {"candidate_edges"}:
            require(detail["cap_source"] == "local" and
                    key == "raw_coordinate_recovery_nodes" and
                    current["candidate_edges"] >= 0,
                    "checker B0 recovery node current")
        else:
            require(set(current) == {"completed_candidate_edges"} and
                    detail["cap_source"] == "local" and
                    key in {"raw_coordinate_recovery_edges",
                            "raw_coordinate_recovery_nodes"} and
                    current["completed_candidate_edges"] >= 0,
                    "checker B0 recovery edge current")
    elif phase == "fixed_B1":
        if set(current) == FIXED_B1_PROGRESS_KEYS:
            _validate_fixed_B1_progress(current)
        elif set(current) == {"lambda_ordinal", "base_component_ordinal"}:
            require(all(type(value) is int and value >= 1
                        for value in current.values()),
                    "checker fixed correlation pair current")
        elif set(current) == {"post_accumulation"}:
            require(current["post_accumulation"] is True,
                    "checker fixed correlation post current")
        else:
            require(current == {} or set(current) in (
                {"completed_candidate_edges"}, {"candidate_edges"}) and
                all(type(value) is int and value >= 0
                    for value in current.values()),
                "checker fixed-B1 resource current")
    elif phase == "initial_target":
        if set(current) == INITIAL_TARGET_PROGRESS_KEYS:
            _validate_initial_target_progress(current)
        elif current == {}:
            require(local_monitor_empty,
                    "checker initial target empty monitor current")
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
                    "checker initial recovery current")
    elif phase == "dual_lift":
        require(current == {} or set(current) ==
                {"completed_reverse_pivots"} and
                current["completed_reverse_pivots"] >= 0,
                "checker dual-lift current")
    elif phase in {"correlation_pass1", "correlation_pass2"}:
        if current == {}:
            require(local_monitor_empty,
                    "checker correlation empty monitor current")
        else:
            require(set(current) in ({"generation"},
                    {"generation", "completed_batches", "completed_blocks"}) and
                    detail["cap_source"] == "local" and
                    type(current["generation"]) is int and
                    current["generation"] >= 1,
                    "checker correlation current")
    elif phase == "section_recovery":
        require(current == {} or set(current) == {"node"} and
                type(current["node"]) is int and current["node"] >= 0,
                "checker section resource current")
    elif phase == "batch_precompute":
        require(current == {} or set(current) ==
                {"generation", "translation_ordinal", "relator"} and
                all(type(value) is int and value >= 1
                    for value in current.values()),
                "checker batch-precompute current")
    elif phase == "block_commit":
        _validate_block_progress(current, packed)
    elif phase == "incremental_reduction":
        _validate_incremental_progress(current)
    elif phase == "target_resolve":
        require(current == {}, "checker target-resolve current")
    elif phase == "selected_proof":
        require(current == {} or set(current) ==
                {"generation", "completed_target"} and
                type(current["generation"]) is int and
                current["generation"] >= 1 and
                current["completed_target"] is True,
                "checker selected-proof current")
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
                "checker serialization resource current")
    else:
        require(False, "checker unknown resource outer phase")
    if key in {"column_generation_batches", "total_new_translation_blocks"}:
        require(phase == "correlation_pass1" and set(current) ==
                {"generation", "completed_batches", "completed_blocks"} and
                (key != "column_generation_batches" or
                 current["completed_batches"] ==
                    CAPS["column_generation_batches"]) and
                (key != "total_new_translation_blocks" or
                 current["completed_blocks"] ==
                    CAPS["total_new_translation_blocks"]),
                "checker exhausted-budget resource current")


def validate_stable_public_schema(data: dict[str, Any], *,
                                  bounded_fixture: bool = False) -> None:
    """Closed public schemas; semantic values are rebuilt later, independently."""
    fill = [bool(data[key]) for key in ("base_q3_replay",
        "normalized_inverse_fibre", "seed_manifest", "source_preflight")]
    require(fill == sorted(fill, reverse=True),
            "checker authenticated frontend fill-prefix")
    base = data["base_q3_replay"]
    if base:
        require(set(base) == BASE_Q3_REPLAY_KEYS and
                base["roof_exponent"] == 2 and base["roof_order"] == 9 and
                base["arithmetic_outside_by_index_three"] is True and
                base["marking_m"] == 0 and base["lambda"] == 1 and
                base["replayed_not_copied"] is True and
                len(base["settled_source_words"]) == 6,
                "checker base-q3 public schema")
    normalized = data["normalized_inverse_fibre"]
    if normalized:
        require(set(normalized) == NORMALIZED_INVERSE_KEYS and
                normalized["normalized_exponent"] == 7 and
                normalized["normalized_roof_order"] == 9 and
                normalized["correction_fibre_size"] == 27 and
                normalized["tested_indices"] == list(range(1, 28)) and
                normalized["passing_indices"] and
                normalized["selected_correction_index"] ==
                    normalized["passing_indices"][0] and
                len(normalized["selected_inverse_words"]) == 6 and
                normalized["max_inverse_word_length"] == max(
                    map(len, normalized["selected_inverse_words"])),
                "checker normalized inverse public schema")
    seeds = data["seed_manifest"]
    if seeds:
        require(set(seeds) == SEED_MANIFEST_KEYS and
                seeds["cube_count"] == len(seeds["cube_words"]) == 26 and
                seeds["old_seed_count"] == len(seeds["old_seed_words"]) == 104 and
                seeds["new_seed_count"] == len(seeds["new_seed_words"]) == 4 and
                seeds["seed_count"] == len(seeds["seed_words"]) == 108 and
                seeds["seed_words"] ==
                    seeds["old_seed_words"]+seeds["new_seed_words"] and
                seeds["cube_digest_sha256"] == sha_obj(seeds["cube_words"]) and
                seeds["old_seed_digest_sha256"] ==
                    sha_obj(seeds["old_seed_words"]) and
                seeds["new_seed_digest_sha256"] ==
                    sha_obj(seeds["new_seed_words"]) and
                seeds["digest_obj_sha256"] == sha_obj(seeds["seed_words"]) and
                len(seeds["provenance"]) == 108,
                "checker seed public schema")
    source = data["source_preflight"]
    if source:
        require(set(source) == SOURCE_PREFLIGHT_KEYS and source["supported"] is True and
                source["seed_count"] == len(source["records"]) == 108 and
                source["contexts_per_seed"] ==
                    source["unique_context_count"] == 31 and
                source["named_use_count"] == 46 and
                source["all_source_tuples_equal"] is True and
                source["all_correction_occurrences_identity"] is True and
                set(source["context_registry"]) ==
                    SOURCE_CONTEXT_REGISTRY_KEYS,
                "checker source-preflight public schema")
        registry = source["context_registry"]
        require(registry["context_count"] == len(registry["contexts"]) == 31 and
                registry["named_use_count"] == len(registry["named_uses"]) == 46 and
                registry["context_rows_sha256"] == sha_obj(registry["contexts"]) and
                registry["named_use_mapping_sha256"] ==
                    sha_obj(registry["named_uses"]) and
                all(set(row) == SOURCE_CONTEXT_ROW_KEYS
                    for row in registry["contexts"]) and
                all(set(row) == SOURCE_NAMED_USE_KEYS
                    for row in registry["named_uses"]) and
                all(set(row) == SOURCE_PREFLIGHT_RECORD_KEYS
                    for row in source["records"]),
                "checker source registry schema")
    base_columns = data["base_columns"]
    if base_columns:
        require(set(base_columns) == BASE_COLUMN_KEYS and
                base_columns["occurrence_count"] ==
                    len(base_columns["occurrences"]) and
                base_columns["occurrence_count"] > 0 and
                base_columns["ordered_sha256"] ==
                    sha_obj(base_columns["occurrences"]) and
                sum(base_columns["per_relator_counts"]) ==
                    base_columns["occurrence_count"] and
                sum(base_columns["per_component_counts"]) ==
                    base_columns["occurrence_count"] and
                all(set(row) == BASE_OCCURRENCE_KEYS
                    for row in base_columns["occurrences"]),
                "checker base columns schema")
        if not bounded_fixture:
            require(base_columns["occurrence_count"] == 76 and
                    base_columns["ordered_sha256"] == BASE_OCCURRENCE_SHA and
                    base_columns["per_relator_counts"] ==
                        [8, 6, 8, 6, 4, 8, 12, 6, 4, 8, 6] and
                    base_columns["per_component_counts"] ==
                        [10, 12, 18, 10, 12, 14],
                    "checker frozen base columns schema")
    support = data["directed_base_support"]
    if support:
        require(set(support) == DIRECTED_SUPPORT_KEYS and
                support["occurrence_count"] == len(support["occurrences"]) and
                support["occurrence_count"] > 0 and
                support["ordered_sha256"] == sha_obj(support["occurrences"]) and
                (not base_columns or support["occurrences"] ==
                    base_columns["occurrences"]),
                "checker directed base schema")
        if not bounded_fixture:
            require(support["occurrence_count"] == 76 and
                    support["ordered_sha256"] == BASE_OCCURRENCE_SHA,
                    "checker frozen directed base schema")
    prefix = data["prefix_B0"]
    if prefix:
        require(set(prefix) == PREFIX_B0_KEYS and
                set(prefix["counts"]) == PREFIX_COUNT_KEYS and
                set(prefix["accounting"]) == PREFIX_ACCOUNTING_KEYS and
                prefix["dependent_event_count"] ==
                    len(prefix["dependent_events"]) and
                prefix["dependent_event_sha256"] ==
                    sha_obj(prefix["dependent_events"]) and
                set(prefix["complete_block_registry"]) == COMPLETE_REGISTRY_KEYS and
                all(set(row) == PREFIX_DEPENDENT_KEYS
                    for row in prefix["dependent_events"]),
                "checker B0 public schema")
        if not bounded_fixture:
            require(prefix["dependent_event_count"] == 16 and
                    prefix["complete_block_registry"][
                        "translation_count"] == 32975,
                    "checker frozen B0 public schema")
    surgery = data["directed_surgery"]
    if surgery:
        require(prefix and set(surgery) == DIRECTED_SURGERY_KEYS and
                surgery["round_count"] == len(surgery["rounds"]) and
                surgery["translation_count"] ==
                    len(surgery["translations"]) and
                surgery["rounds_sha256"] == sha_obj(surgery["rounds"]) and
                surgery["translations_sha256"] ==
                    sha_obj(surgery["translations"]) and
                surgery["stable_rounds_projection_sha256"] ==
                    prefix["stable_rounds_projection_sha256"],
                "checker surgery public schema")
        if not bounded_fixture:
            require(surgery["round_count"] == 32 and
                    surgery["translation_count"] == 207,
                    "checker frozen surgery public schema")
    block, anchor = data["fixed_B1_block"], data["fixed_B1_anchor"]
    require(bool(block) == bool(anchor), "checker fixed block/anchor presence")
    if block:
        require(set(block) == BLOCK_KEYS and set(anchor) == BLOCK_ANCHOR_KEYS and
                block["complete"] is True and block["column_count"] ==
                    len(block["columns"]) == 11 and
                [row["relator_index"] for row in block["columns"]] ==
                    list(range(1, 12)) and
                all(set(row) == BLOCK_COLUMN_KEYS and
                    set(row["raw_column"]) == BLOCK_RAW_KEYS
                    for row in block["columns"]) and
                block["relator9_independent"] is True and
                block["pivot_count_after_relator9"] ==
                    block["pivot_count_before_relator9"]+1 and
                anchor["after_complete_block"] is True and
                anchor["private_anchor_ids_not_exported"] is True,
                "checker fixed B1 public schema")
    if data["old_qstar_boundary"]:
        qstar = data["old_qstar_boundary"]
        require(set(qstar) == OLD_QSTAR_KEYS and
                qstar["used_only_to_freshly_reconstruct_fixed_B1"] is True and
                qstar["used_after_fixed_B1"] is False and
                type(qstar["support_count"]) is int and
                qstar["support_count"] > 0,
                "checker old-qstar boundary schema")
        if not bounded_fixture:
            require(qstar["support_count"] == 78,
                    "checker frozen old-qstar support")
    parents = data["raw_parent_manifest"]
    if parents:
        require(set(parents) == RAW_PARENT_KEYS and
                parents["source_count"] == len(parents["rows"]) == 109 and
                parents["rows_sha256"] == sha_obj(parents["rows"]) and
                all(set(row) == RAW_PARENT_ROW_KEYS
                    for row in parents["rows"]),
                "checker raw-parent schema")
    if data["recovery_map"]:
        validate_recovery_public(data["recovery_map"])
    if data["initial_target"]:
        initial = data["initial_target"]
        require(set(initial) == INITIAL_TARGET_KEYS and
                initial["fresh_B1_stable_digests_all_equal"] is True and
                initial["raw_gradient_count"] == 109 and
                _sha256_text(initial["raw_gradients_sha256"]) and
                _sha256_text(initial["semantic_remainders_sha256"]) and
                initial["semantic_remainders_sha256"] !=
                    initial["target6"]["fresh_remainder_sha256"],
                "checker initial target wrapper")


def validate_resource_stage_shape(data: dict[str, Any],
                                  detail: dict[str, Any]) -> None:
    phase = detail["phase"]
    early = ("base_q3_replay", "normalized_inverse_fibre", "seed_manifest")
    prefix = ("directed_base_support", "directed_surgery", "prefix_B0")
    fixed = ("base_columns", "fixed_B1_block", "fixed_B1_anchor",
             "old_qstar_boundary")
    initial = ("raw_parent_manifest", "recovery_map", "initial_target")
    if phase == "authenticated_input":
        present = [bool(data[key]) for key in early]
        require(present == sorted(present, reverse=True) and
                not data["source_preflight"] and
                all(not data[key] for key in (*prefix, *fixed, *initial,
                    "generation_ledger")),
                "checker authenticated resource projection")
    elif phase == "source_preflight":
        require(all(data[key] for key in early) and
                not data["source_preflight"] and
                all(not data[key] for key in (*prefix, *fixed, *initial,
                    "generation_ledger")),
                "checker source resource projection")
    elif phase == "fresh_B0":
        require(all(data[key] for key in (*early, "source_preflight")) and
                all(not data[key] for key in (*prefix, *fixed, *initial,
                    "generation_ledger")),
                "checker B0 resource projection")
    elif phase == "fixed_B1":
        require(all(data[key] for key in (*early, "source_preflight", *prefix))
                and all(not data[key] for key in (*fixed, *initial,
                    "generation_ledger")),
                "checker B1 resource projection")
    elif phase == "initial_target":
        require(all(data[key] for key in
                    (*early, "source_preflight", *prefix, *fixed)) and
                all(not data[key] for key in (*initial, "generation_ledger")),
                "checker initial target resource projection")
    else:
        require(all(data[key] for key in
                    (*early, "source_preflight", *prefix, *fixed, *initial)) and
                data["generation_ledger"],
                "checker adaptive resource prefix")
        last = data["generation_ledger"][-1]
        if phase == "dual_lift":
            require(last["classification"] is None and all(not last[key]
                for key in ("raw_lambda", "correlation", "preflight",
                            "commit", "incremental")),
                "checker dual resource projection")
        elif phase in {"correlation_pass1", "correlation_pass2"}:
            require(last["classification"] is None and last["raw_lambda"] and
                    not last["preflight"] and not last["commit"] and
                    not last["incremental"],
                    "checker correlation resource projection")
        elif phase in {"section_recovery", "batch_precompute"}:
            require(last["classification"] is None and last["raw_lambda"] and
                    last["correlation"] and not last["preflight"] and
                    not last["commit"] and not last["incremental"],
                    "checker precommit resource projection")
        elif phase == "block_commit":
            require(last["classification"] is None and last["preflight"] and
                    not last["commit"] and not last["incremental"],
                    "checker block resource projection")
        elif phase == "incremental_reduction":
            require(last["classification"] is None and last["commit"] and
                    not last["incremental"],
                    "checker incremental resource projection")
        elif phase == "target_resolve":
            require(last["classification"] == "ACTIVE_BATCH_COMMITTED" and
                    last["incremental"],
                    "checker target resolve projection")
        elif phase == "selected_proof":
            require(last["classification"] is None and
                    last["target"]["consistent"] is True and
                    all(not last[key] for key in ("raw_lambda", "correlation",
                        "preflight", "commit", "incremental")),
                    "checker selected resource projection")
        elif phase == "receipt_serialization":
            require(last["classification"] is None and
                    (last["target"]["consistent"] is True or
                     last["raw_lambda"] and last["correlation"] and
                     not last["preflight"]),
                    "checker serialization resource projection")
        else:
            require(False, "checker adaptive resource phase")
    active = [row for row in data["generation_ledger"] if
              row.get("classification") == "ACTIVE_BATCH_COMMITTED"]
    batches = len(active); blocks = sum(row["commit"]["translation_count"]
                                       for row in active)
    if phase == "block_commit":
        blocks += detail["current"]["completed_translations"]
    elif phase == "incremental_reduction":
        batches += 1
        blocks += data["generation_ledger"][-1]["commit"]["translation_count"]
    partial = data["partial"]
    if detail["cap_key"] in {
            "column_generation_batches", "total_new_translation_blocks"}:
        require(detail["current"]["completed_batches"] == batches and
                detail["current"]["completed_blocks"] == blocks,
                "checker exhausted-budget current/ledger binding")
    require(partial["completed_generation_count"] == len(active) and
            partial["completed_batch_count"] == batches and
            partial["completed_new_translation_block_count"] == blocks,
            "checker resource committed count projection")


def validate_envelope(data: dict[str, Any], raw_bytes: int,
                      upstream: dict[str, int], *,
                      sealed_bounded_fixture: bool = False) -> None:
    require(upstream == EXPECTED_UPSTREAM_CAPS,
            "checker literal upstream cap authority")
    require(set(data) == TOP_KEYS and data["schema"] == SCHEMA and
            data["task_sha256"] == TASK_SHA and
            data["pins"] == expected_pin_rows(ROOT/Q3_PATH) and
            data["caps"] == CAPS and data["caps_sha256"] == sha_obj(CAPS) and
            data["algorithm"] == ALGORITHM_PUBLIC and
            data["provenance"] == PROVENANCE and
            data["theorem_boundary"] == theorem_boundary() and
            data["upstream_caps_sha256"] == sha_obj(data["upstream_caps"]) and
            data["algorithm"]["max_total_new_relator_columns"] ==
                11*data["algorithm"]["max_total_new_translation_blocks"] and
            data["algorithm"]["monitor_registry_sha256"] == MONITOR_SHA and
            data["algorithm"]["upstream_throw_sites_sha256"] ==
                UPSTREAM_THROW_SITES_SHA,
            "checker exact envelope")
    token = data["terminal_token"]
    require(token in TERMINALS and data["status"] == token and
            data["claims"] == claim_row(token), "checker terminal/claim")
    guards = data["resource_guards"]
    require(set(guards) == {"resource_hit", "resource",
        "local_and_upstream_separate", "reason_equals_cap_key"} and
        guards["local_and_upstream_separate"] is True and
        guards["reason_equals_cap_key"] is True,
        "checker resource guard schema")
    validate_stable_public_schema(data,
                                  bounded_fixture=sealed_bounded_fixture)
    if data["initial_target"] and data["generation_ledger"]:
        first = data["generation_ledger"][0]
        require(first["target"]["remainders_sha256"] ==
                    data["initial_target"]["semantic_remainders_sha256"] and
                data["initial_target"]["semantic_remainders_sha256"] !=
                    data["initial_target"]["target6"][
                        "fresh_remainder_sha256"],
                "checker generation-one semantic/ledger separation")
        if data["fixed_B1_block"]:
            post = data["fixed_B1_block"]["post_accounting"]
            anchor = data["fixed_B1_anchor"]
            structural = ("columns", "pivots", "dependent",
                "live_sparse_entries", "pool_size", "DAG_nodes",
                "DAG_edges", "section_bindings")
            require(all(first["basis"][key] == post[key]
                        for key in structural) and
                    first["basis"]["columns"] == anchor["basis_columns"] and
                    first["basis"]["pivots"] == anchor["basis_pivots"] and
                    first["basis"]["dependent"] ==
                        anchor["basis_dependent"] and
                    first["basis"]["live_sparse_entries"] ==
                        anchor["basis_live_sparse_entries"] and
                    first["basis"]["pool_size"] == anchor["pool_size"] and
                    first["basis"]["DAG_nodes"] == anchor["DAG_nodes"] and
                    first["basis"]["DAG_edges"] == anchor["DAG_edges"] and
                    first["basis"]["section_bindings"] ==
                        anchor["section_bindings"],
                    "checker generation-one fixed-block anchor binding")
    if token.endswith("UNKNOWN_INPUT"):
        require(data["reason"] == TERMINAL_REASONS[token] and
                data["phase"] == "authenticated_input" and
                data["upstream_caps"] in ({}, upstream) and
                guards["resource_hit"] is False and
                guards["resource"] is None and data["partial"] == {} and
                len(data["input_errors"]) == 1 and
                isinstance(data["input_errors"][0], str) and
                bool(data["input_errors"][0]) and
                data["selected_proof"] == {} and data["full_D2_separator"] == {},
                "checker INPUT boundary")
        require(all(not data[key] for key in ("base_q3_replay",
            "normalized_inverse_fibre", "seed_manifest", "source_preflight",
            "directed_base_support", "directed_surgery", "prefix_B0",
            "base_columns", "fixed_B1_block", "fixed_B1_anchor",
            "old_qstar_boundary", "raw_parent_manifest", "recovery_map",
            "initial_target", "generation_ledger", "packed_block_ledger")),
            "checker INPUT no math payload")
    elif token.endswith("UNKNOWN_RESOURCE"):
        detail = guards["resource"]
        require(data["upstream_caps"] == upstream and
                guards["resource_hit"] is True and
                data["packed_block_ledger"] == {} and
                data["selected_proof"] == {} and
                data["full_D2_separator"] == {} and data["input_errors"] == [],
                "checker RESOURCE exact row")
        validate_resource_detail(detail, data, upstream)
        validate_partial_public(data["partial"], detail)
        validate_resource_current(detail, data)
        validate_resource_stage_shape(data, detail)
        partial = data["partial"]
        validate_generation_shape(data["generation_ledger"], token, partial)
    else:
        require(data["upstream_caps"] == upstream and data["phase"] == "complete" and
                data["reason"] == TERMINAL_REASONS[token] and
                guards == {"resource_hit": False, "resource": None,
                    "local_and_upstream_separate": True,
                    "reason_equals_cap_key": True} and data["partial"] == {} and
                data["input_errors"] == [] and
                ((token.endswith("CONSISTENT") and data["selected_proof"] and
                  data["full_D2_separator"] == {}) or
                 (token.endswith("FULL_D2_OBSTRUCTION") and
                  data["full_D2_separator"] and data["selected_proof"] == {})),
                "checker exact normal boundary")
        require(all(data[key] for key in ("base_q3_replay",
            "normalized_inverse_fibre", "seed_manifest", "source_preflight",
            "directed_base_support", "directed_surgery", "prefix_B0",
            "base_columns", "fixed_B1_block", "fixed_B1_anchor",
            "old_qstar_boundary", "raw_parent_manifest", "recovery_map",
            "initial_target", "generation_ledger", "packed_block_ledger")),
            "checker completed production stage payload")
        validate_generation_shape(data["generation_ledger"], token)
        require(bool(data["generation_ledger"]),
                "checker normal generation exists")
        if token.endswith("CONSISTENT"):
            require(set(data["selected_proof"]) == SELECTED_PROOF_KEYS,
                    "checker selected-proof exact top keyset")
        else:
            final = data["generation_ledger"][-1]
            separator = data["full_D2_separator"]
            require(set(separator) == SEPARATOR_KEYS and
                    separator["generation"] == final["generation"] and
                    separator["raw_lambda"] == final["raw_lambda"] and
                    separator["correlation"] == final["correlation"] and
                    separator["active_row_count"] == 0 and
                    separator["complete_76_occurrence_full_11_relator_correlation"]
                        is True and separator["annihilates_full_D2"] is True and
                    separator["lambda_delta_all_zero"] is True and
                    separator["lambda_base_z"] == 2 and
                    separator["registered_108_family_only"] is True and
                    separator["pinned_E4_roof_only"] is True,
                    "checker exact full-D2 separator")
    perf = data["performance"]
    require(set(perf) == {"initial_remaining_seconds", "elapsed_seconds",
        "remaining_seconds", "checks", "peak_rss_bytes", "hit_reason",
        "callback_count", "receipt_bytes", "phase_seconds",
        "correlation_pool_intern_calls",
        "correlation_full_sparse_vectors_materialized", "full_E4_enumerations",
        "hard_outer_allowance_seconds"} and perf["receipt_bytes"] == raw_bytes and
        0 < perf["initial_remaining_seconds"] <= 18000 and
        0 <= perf["remaining_seconds"] <= perf["initial_remaining_seconds"] and
        perf["elapsed_seconds"] >= 0 and type(perf["checks"]) is int and
        perf["checks"] >= 0 and type(perf["callback_count"]) is int and
        perf["callback_count"] == perf["checks"] and
        type(perf["peak_rss_bytes"]) is int and perf["peak_rss_bytes"] >= 0 and
        perf["correlation_pool_intern_calls"] == 0 and
        perf["correlation_full_sparse_vectors_materialized"] == 0 and
        perf["full_E4_enumerations"] == 0 and
        isinstance(perf["phase_seconds"], dict) and
        set(perf["phase_seconds"]) == expected_phase_seconds_keys(data) and
        all(isinstance(key, str) and isinstance(value, (int, float)) and
            not isinstance(value, bool) and value >= 0
            for key, value in perf["phase_seconds"].items()) and
        sum(perf["phase_seconds"].values()) <= perf["elapsed_seconds"]+2.0 and
        perf["hard_outer_allowance_seconds"] == 18000 and
        perf["hit_reason"] == (data["reason"] if
            token.endswith("UNKNOWN_RESOURCE") else None),
        "checker performance/receipt-byte binding")


def _resource_here(data: dict[str, Any], phases: set[str]) -> bool:
    if not data["terminal_token"].endswith("UNKNOWN_RESOURCE"):
        return False
    require(data["phase"] in phases and data["partial"]["phase"] ==
            data["phase"], "checker exact resource stopping stage")
    return True


def check_receipt(q3_path: Path, receipt_path: Path, *,
                  seconds: float = 18_000.0) -> dict[str, Any]:
    """Fresh semantic replay; no new-producer helper is imported."""
    global CHECKER_STARTED, CHECKER_DEADLINE, CHECKER_CHECKS
    require(0 < seconds <= 18_000, "157em checker deadline seconds")
    CHECKER_STARTED = time.monotonic(); CHECKER_DEADLINE = CHECKER_STARTED+seconds
    CHECKER_CHECKS = 0
    authenticate()
    v2, eh, eg, ed, old, v4 = predecessor_modules()
    del eh
    configure_deadlines(v2, eg, ed, old)
    raw = receipt_path.read_bytes(); data = json.loads(raw.decode("utf-8"))
    require(raw == (json.dumps(data, sort_keys=True,
            separators=(",", ":"))+"\n").encode("utf-8"),
            "checker canonical receipt bytes")
    upstream = expected_upstream_caps(eg, ed, old)
    validate_envelope(data, len(raw), upstream)
    q3_good = (q3_path.resolve() == (ROOT/Q3_PATH).resolve() and
        q3_path.is_file() and q3_path.stat().st_size == Q3_BYTES and
        sha_file(q3_path) == Q3_SHA)
    if data["terminal_token"].endswith("UNKNOWN_INPUT"):
        require(not q3_good, "checker false authenticated INPUT terminal")
        return data
    require(q3_good, "checker authenticated q3 artifact")
    if not data["base_q3_replay"]:
        require(_resource_here(data, {"authenticated_input"}),
                "checker pre-q3 resource boundary")
        return data
    q3 = ed.load_q3(q3_path); e3, e4 = old.reconstruct(q3)
    require(e4.degree == 144 and e4.collector.n == 10,
            "checker frozen E4 widths")
    tick("checker authenticated q3", True)
    old.validate_base_replay(data, q3, e3, e4)
    normalized, base_key, inverse_words = old.rebuild_normalized_inverse_fibre(
        q3, e4)
    require(data["normalized_inverse_fibre"] == normalized,
            "checker normalized inverse fresh equality")
    seeds = old.affine_checker_seed_words(q3, e3)
    require(data["seed_manifest"] == seeds and
            sha_obj(seeds["seed_words"]) == v2.SEED_MANIFEST_SHA,
            "checker exact registered 108 seeds")
    if not data["source_preflight"]:
        require(_resource_here(data, {"source_preflight"}),
                "checker source resource boundary")
        current = data["partial"]["current"]
        count = int(current["evaluated_seeds"])
        prefix = old.checker_rebuild_occurrence_preflight(
            seeds["seed_words"][:count], e4, tuple(base_key))
        require(prefix["supported"] is True and
                len(prefix["records"]) == count and
                sha_obj(prefix["records"]) ==
                    current["records_prefix_sha256"],
                "checker source RESOURCE exact prefix")
        return data
    source = old.checker_rebuild_occurrence_preflight(
        seeds["seed_words"], e4, tuple(base_key))
    require(data["source_preflight"] == source and source["supported"] is True,
            "checker source preflight fresh equality")
    occurrences, base_public = numbered_occurrences(eg, old, e4)
    base_columns = independent_base_columns(old, e4, occurrences)
    require(data["base_columns"] in ({}, base_public) and
            data["directed_base_support"] == base_public,
            "checker base/directed occurrence bundle")
    recovery = CheckerRecovery()
    for occurrence in occurrences:
        recovery.direct(int(occurrence["component"]),
            bytes.fromhex(occurrence["element_hex"]),
            108+int(occurrence["relator_index"]),
            int(occurrence["term_ordinal"]))
    complete_masks: dict[bytes, int] = {}
    if not data["prefix_B0"]:
        require(_resource_here(data, {"fresh_B0"}),
                "checker fresh-B0 resource boundary")
        return data
    pool, basis, events = replay_B0(ed, old, data, e4, normalized,
        base_key, recovery, occurrences, complete_masks)
    require(data["prefix_B0"]["prefix_pool_checkpoint"] == len(pool.values) ==
                976408 and _sha256_text(
                    data["prefix_B0"]["pool_order_sha256"]) and
            data["prefix_B0"]["stable_rounds_projection_sha256"] ==
                v2.PREFIX_STABLE_SHA and
            data["prefix_B0"]["translations_sha256"] ==
                v2.PREFIX_TRANSLATIONS_SHA and
            data["prefix_B0"]["columns_sha256"] == v2.PREFIX_COLUMNS_SHA and
            data["prefix_B0"]["blocker_history_sha256"] ==
                v2.PREFIX_BLOCKERS_SHA and
            data["prefix_B0"]["dependent_events"] == events,
            "checker full B0 public anchors")
    qstar = ed.validate_qstar_label(ed.QSTAR, WIDTH)
    oracle = ed.RawOracle(old, pool, basis, qstar)
    support = eg.checker_lambda_support(oracle, WIDTH)
    if not data["fixed_B1_block"]:
        require(_resource_here(data, {"fixed_B1"}),
                "checker fixed-B1 resource boundary")
        current = data["partial"]["current"]
        if set(current) == FIXED_B1_PROGRESS_KEYS:
            validate_fixed_B1_resource_prefix(
                v2, old, e4, pool, basis, oracle, current)
        return data
    require(data["base_columns"] == base_public,
            "checker frozen base columns public equality")
    old_corr = eg.independent_correlation(support["rows"], occurrences,
        width=WIDTH, unpack=pool.unpack, mul=e4.mul, inverse=e4.inverse,
        pack=element_blob)
    require(data["old_qstar_boundary"] == {
        "used_only_to_freshly_reconstruct_fixed_B1": True,
        "used_after_fixed_B1": False, "support_count": support["count"],
        "support_sha256": support["ordered_sha256"],
        "complete_correlation_sha256":
            old_corr["public"]["packed_rows_sha256"]},
        "checker old-qstar B0-only boundary")
    fixed, _, fixed_ledger = replay_fixed_B1_prefix(
        v2, old, e4, pool, basis, oracle, data["fixed_B1_block"])
    del oracle, qstar
    # The pinned fixed-block checker deliberately calls the base reducer
    # directly, bypassing our instrumented subclass.  Reconstruct the 76
    # semantic recovery edges and the complete 11-bit mask exactly once here.
    fixed_blob = bytes.fromhex(fixed["translation_hex"])
    fixed_value = pool.unpack(fixed_blob)
    recovery_before_fixed = recovery.translated_candidates
    require(complete_masks.get(fixed_blob, 0) == 0,
            "checker fixed B1 not previously complete")
    for occurrence in occurrences:
        relator = int(occurrence["relator_index"])
        parent = bytes.fromhex(occurrence["element_hex"])
        value = e4.mul(fixed_value, occurrence["_value"])
        recovery.translated(int(occurrence["component"]),
            element_blob(value), fixed_blob, relator,
            int(occurrence["term_ordinal"]), parent)
    for relator in range(1, 12):
        record_complete_relator(complete_masks, fixed_blob, relator)
    require(recovery.translated_candidates-recovery_before_fixed == 76 and
            complete_masks[fixed_blob] == 0x7ff,
            "checker fixed B1 manual recovery/mask")
    def validate_fixed_public(block: dict[str, Any],
                              anchor: dict[str, Any],
                              live_entries: int) -> bool:
        v2._validate_anchor_public(block, anchor, frozen=True,
                                   live_basis_entries=live_entries)
        return True
    v4.validate_completed_anchor_split(v2, fixed, data["fixed_B1_block"],
        data["fixed_B1_anchor"], basis.live_entries,
        validate_fixed_public)
    require(fixed["raw_columns_sha256"] == B1["raw_columns_sha256"] and
            fixed["reducer_ledger_sha256"] == B1["reducer_ledger_sha256"] and
            complete_registry(complete_masks, 32976)["translation_count"] ==
                32976,
            "checker fixed B1/complete registry")
    dependent_raw = [{(int(c), bytes.fromhex(h)): int(a)
                      for c, h, a in event["raw_column"]}
                     for event in events]
    prior_raw = [{(int(c), bytes.fromhex(h)): int(a)
                  for c, h, a in row["raw_column"]["entries"]}
                 for row in fixed_ledger]
    if not data["initial_target"]:
        require(_resource_here(data, {"initial_target"}),
                "checker initial-target resource boundary")
        current = data["partial"]["current"]
        if set(current) == INITIAL_TARGET_PROGRESS_KEYS:
            validate_initial_target_resource_prefix(v2, old, e4, seeds,
                source, inverse_words, pool, basis, current)
        return data
    target0 = fresh_target(v2, old, e4, seeds, source, inverse_words,
                           pool, basis)
    parent_public = direct_parents(e4, pool, recovery, target0["words"],
                                   target0["gradients"])
    require(data["raw_parent_manifest"] == parent_public and
            data["recovery_map"] == recovery.public() and
            data["initial_target"] == target0["public"],
            "checker fresh 109 target/recovery public equality")
    remainders = target0["remainders"]
    raw_gradients = target0["gradients"]
    base_raw = target0["base_raw"]
    system, current_target = solve_remainders(v2, old, e4, remainders, 1)
    validate_fresh_semantic_binding(data["initial_target"], current_target,
                                    remainders,
                                    B1["fresh_remainders_sha256"])
    require(current_target["row_space_sha256"] == B1["target_row_space_sha256"],
            "checker frozen B1 solve")
    normal = not data["terminal_token"].endswith("UNKNOWN_RESOURCE")
    if normal:
        packed_translations, packed_rows, packed_record_raw = decode_packed_ledger(
            data["packed_block_ledger"])
    else:
        packed_translations, packed_rows, packed_record_raw = [], [], b""
    generated_translations = bytearray(); generated_records = bytearray()
    translation_cursor = record_cursor = 0
    cumulative = {"pass1": 0, "pass2": 0}
    batches = total_blocks = 0
    prior_accounting: dict[str, Any] | None = None
    derived_terminal: str | None = None
    for index, claimed in enumerate(data["generation_ledger"], 1):
        require(claimed["generation"] == index,
                "checker generation order")
        require_basis_public(claimed["basis"], basis, pool, recovery,
                             prior_accounting)
        require(claimed["target"] == current_target,
                "checker generation target fresh equality")
        if system.consistent:
            require(claimed["classification"] in {"CONSISTENT", None} and
                    all(claimed[key] == {} for key in ("raw_lambda",
                        "correlation", "preflight", "commit", "incremental")),
                    "checker consistent generation boundary")
            if claimed["classification"] == "CONSISTENT":
                require(normal and index == len(data["generation_ledger"]),
                        "checker consistent terminal location")
                v2._validate_selected(old, e4, inverse_words,
                    seeds["seed_words"], pool, basis, system, base_raw,
                    data["selected_proof"])
                derived_terminal = \
                    "B345_E4_D2_COLGEN_TARGET6_CONSISTENT"
            else:
                serialization = data["partial"]["current"].get(
                    "completed_terminal_before_serialization") if \
                    data["terminal_token"].endswith("UNKNOWN_RESOURCE") else None
                require((_resource_here(data, {"selected_proof"}) or
                         _resource_here(data, {"receipt_serialization"}) and
                         serialization ==
                            "B345_E4_D2_COLGEN_TARGET6_CONSISTENT"),
                        "checker selected/serialization resource")
            break
        functional, raw_public = reverse_lift(old, pool, basis, system,
            remainders, dependent_raw, prior_raw)
        if not claimed["raw_lambda"]:
            require(_resource_here(data, {"dual_lift"}),
                    "checker dual-lift resource")
            break
        require(claimed["raw_lambda"] == raw_public,
                "checker general raw-lambda replay")
        remaining = CAPS["total_new_translation_blocks"]-total_blocks
        selection_budget = 0 if batches == CAPS[
            "column_generation_batches"] else remaining
        correlation = independent_correlation(e4, pool,
            semantic_public(functional), occurrences, index, cumulative,
            selection_budget)
        require(not {row[0] for row in correlation["active"]}.intersection(
            {blob for blob, mask in complete_masks.items() if mask == 0x7ff}),
            "checker ACTIVE translation not already complete")
        if not claimed["correlation"]:
            require(_resource_here(data, {"correlation_pass1",
                "correlation_pass2"}), "checker correlation resource")
            break
        require(claimed["correlation"] == correlation["public"],
                "checker complete two-pass correlation")
        if not correlation["active"]:
            expected_separator = {"generation": index,
                "raw_lambda": raw_public,
                "correlation": correlation["public"], "active_row_count": 0,
                "complete_76_occurrence_full_11_relator_correlation": True,
                "annihilates_full_D2": True,
                "lambda_delta_all_zero": True, "lambda_base_z": 2,
                "registered_108_family_only": True,
                "pinned_E4_roof_only": True}
            if normal:
                require(claimed["classification"] ==
                            "FULL_D2_OBSTRUCTION" and
                        data["full_D2_separator"] == expected_separator and
                        index == len(data["generation_ledger"]),
                        "checker full-D2 separator replay")
                derived_terminal = \
                    "B345_E4_D2_COLGEN_TARGET6_FULL_D2_OBSTRUCTION"
            else:
                serialization = data["partial"]["current"].get(
                    "completed_terminal_before_serialization")
                require(claimed["classification"] is None and
                        _resource_here(data, {"receipt_serialization"}) and
                        serialization ==
                            "B345_E4_D2_COLGEN_TARGET6_FULL_D2_OBSTRUCTION",
                        "checker obstruction serialization resource")
            break
        if not correlation["selected"]:
            require(_resource_here(data, {"correlation_pass1"}) and
                    (total_blocks == CAPS["total_new_translation_blocks"] or
                     batches == CAPS["column_generation_batches"]),
                    "checker bounded ACTIVE terminal")
            validate_bounded_active_resource(
                data["resource_guards"]["resource"], batches, index,
                total_blocks)
            break
        if not claimed["preflight"]:
            require(_resource_here(data, {"section_recovery",
                "batch_precompute"}), "checker preflight resource")
            break
        validate_selected_sections(eg, old, e4, recovery, occurrences,
                                   correlation, claimed["preflight"], index)
        staged = stage_generation_rows(old, e4, pool, occurrences,
            base_columns, functional, correlation, claimed["preflight"], index)
        old_rows = {key: dict(value) for key, value in basis.rows.items()}
        count = len(correlation["selected"]); record_count = 11*count
        if normal:
            batch_translations = packed_translations[
                translation_cursor:translation_cursor+count]
            batch_records = packed_rows[record_cursor:record_cursor+record_count]
        else:
            batch_translations = correlation["selected"]
            batch_records = None
        if not claimed["commit"]:
            require(_resource_here(data, {"block_commit"}),
                    "checker block-commit resource")
            partial_t, partial_r = replay_partial_batch(old, pool, basis,
                recovery, complete_masks, correlation, staged,
                data["partial"]["current"], len(generated_records)//225)
            generated_translations.extend(partial_t)
            generated_records.extend(partial_r)
            break
        new_keys, _, block_raw, encoded_records = replay_generation_batch(old, e4, pool,
            basis, recovery, complete_masks, correlation, staged, claimed,
            batch_translations, batch_records)
        generated_translations.extend(b"".join(correlation["selected"]))
        generated_records.extend(encoded_records)
        translation_cursor += count; record_cursor += record_count
        total_blocks += count; batches += 1; prior_raw.extend(block_raw)
        if not claimed["incremental"]:
            require(_resource_here(data, {"incremental_reduction"}),
                    "checker incremental resource")
            checker_incremental(old, pool, basis, remainders, old_rows,
                new_keys, raw_gradients, index,
                resource_current=data["partial"]["current"])
            break
        remainders, incremental = checker_incremental(old, pool, basis,
            remainders, old_rows, new_keys, raw_gradients, index)
        require(claimed["incremental"] == incremental and
                claimed["classification"] == "ACTIVE_BATCH_COMMITTED",
                "checker incremental/public generation commit")
        prior_accounting = claimed["commit"]["post_accounting"]
        if index == len(data["generation_ledger"]):
            require(_resource_here(data, {"target_resolve",
                "receipt_serialization"}),
                "checker committed-prefix resource boundary")
            break
        system, current_target = solve_remainders(v2, old, e4,
                                                  remainders, index+1)
    if normal:
        require(derived_terminal == data["terminal_token"] and
                translation_cursor == len(packed_translations) and
                record_cursor == len(packed_rows) and
                bytes(generated_translations) == b"".join(packed_translations) and
                bytes(generated_records) == packed_record_raw,
                "checker exact normal terminal/packed cursors")
    else:
        packed = data["partial"]["packed_block_ledger_prefix"]
        require(packed["translation_count"]*WIDTH ==
                    len(generated_translations) and
                packed["record_count"]*225 == len(generated_records) and
                packed["translation_sha256"] ==
                    sha_bytes(bytes(generated_translations)) and
                packed["decoded_sha256"] == sha_bytes(bytes(generated_records)),
                "checker exact RESOURCE packed committed prefix")
    if normal:
        require(data["recovery_map"] == recovery.public(),
                "checker final canonical recovery map")
    tick("checker complete", True)
    return data


def _empty_packed_ledger_fixture() -> dict[str, Any]:
    empty = b""; encoded = ""
    return {"format": "complete-D2-block-ledger/v1",
        "translation_encoding": "exact-E4-blob154-no-padding",
        "translation_count": 0, "translation_decoded_bytes": 0,
        "translation_sha256": sha_bytes(empty),
        "translation_base64_length": 0,
        "translation_base64_sha256": sha_bytes(encoded.encode("ascii")),
        "translation_base64": encoded,
        "record_encoding":
            "generation-u8|translation-ordinal-u16le|relator-u8|flags-u8|lambda-u8|pivot-component-u8|pivot-blob154|raw-sha256|typed-sha256",
        "record_endianness": "little", "record_bytes": 225,
        "record_count": 0, "decoded_bytes": 0,
        "decoded_sha256": sha_bytes(empty), "base64_length": 0,
        "base64_sha256": sha_bytes(encoded.encode("ascii")),
        "base64": encoded, "flags_unused_high_nibble_zero": True,
        "JSON_column_objects_used": False}


def _fixture_recovery_public() -> dict[str, Any]:
    return {"encoding": RECOVERY_ENCODING, "semantic_entry_count": 0,
        "direct_parent_count": 0, "raw_coordinate_parent_entry_count": 0,
        "translated_parent_count": 0, "candidate_edge_count": 0,
        "translated_candidate_edge_count": 0,
        "canonical_replacement_count": 0,
        "canonical_sha256": hashlib.sha256().hexdigest(),
        "typed_arrays": {"kind": "u8", "component": "u8",
            "source": "u16-native-private", "offset": "u32-native-private",
            "relator": "u8", "term": "u16-native-private",
            "blob_width": WIDTH},
        "one_selected_parent_per_semantic_key": True,
        "all_candidate_dicts_or_roots_retained": False,
        "pool_IDs_public": False}


def _fixture_receipt(token: str) -> dict[str, Any]:
    require(token in TERMINALS, "checker fixture terminal")
    recovery = _fixture_recovery_public()
    basis = {"columns": 0, "pivots": 0, "dependent": 0,
        "live_sparse_entries": 0, "pool_size": 1,
        "pool_order_sha256": None, "DAG_nodes": 0, "DAG_edges": 0,
        "section_bindings": 0, "section_expression_nodes": 0,
        "section_expression_edges": 0, "recovery": recovery}
    row = {"schema": SCHEMA, "task_sha256": TASK_SHA,
        "terminal_token": token, "status": token, "reason": None,
        "phase": "complete", "pins": expected_pin_rows(ROOT/Q3_PATH),
        "caps": dict(CAPS), "caps_sha256": sha_obj(CAPS),
        "upstream_caps": dict(EXPECTED_UPSTREAM_CAPS),
        "upstream_caps_sha256": sha_obj(EXPECTED_UPSTREAM_CAPS),
        "algorithm": copy.deepcopy(ALGORITHM_PUBLIC),
        "provenance": copy.deepcopy(PROVENANCE),
        "base_q3_replay": {}, "normalized_inverse_fibre": {},
        "seed_manifest": {}, "source_preflight": {},
        "directed_base_support": {}, "directed_surgery": {},
        "prefix_B0": {}, "base_columns": {}, "fixed_B1_block": {},
        "fixed_B1_anchor": {}, "old_qstar_boundary": {},
        "raw_parent_manifest": {}, "recovery_map": {},
        "initial_target": {}, "generation_ledger": [],
        "packed_block_ledger": {}, "selected_proof": {},
        "full_D2_separator": {}, "claims": claim_row(token),
        "theorem_boundary": theorem_boundary(),
        "resource_guards": {"resource_hit": False, "resource": None,
            "local_and_upstream_separate": True,
            "reason_equals_cap_key": True},
        "partial": {}, "input_errors": [], "performance": {}}
    phases: dict[str, float] = {}
    if token.endswith("CONSISTENT"):
        target = {"generation": 1, "variables": 108, "equations": 0,
            "rank": 0, "nullity": 108, "consistent": True,
            "row_space_sha256": "11"*32, "remainders_sha256": "22"*32,
            "live_remainder_entries": 0, "complete_all_coordinates": True,
            "stopped_at_first_contradiction": False, "dual": None}
        row["generation_ledger"] = [{"generation": 1, "basis": basis,
            "target": target, "raw_lambda": {}, "correlation": {},
            "preflight": {}, "commit": {}, "incremental": {},
            "classification": "CONSISTENT"}]
        row["selected_proof"] = {key: (False if key in {
            "direct_replay", "affine_prediction_equal",
            "proof_expands_to_selected_gradient", "post_block_anchor_used",
            "targets_7_through_33_not_checked"} else [] if key in {
            "coefficient_vector", "support", "element_registry"} else 0 if key in
            {"factor_count", "proof_root_node_id"} else {})
            for key in SELECTED_PROOF_KEYS}
        row["packed_block_ledger"] = _empty_packed_ledger_fixture()
        row["reason"] = TERMINAL_REASONS[token]
        phases = {"selected_proof_g1": 0.0,
                  "receipt_serialization": 0.0}
    elif token.endswith("FULL_D2_OBSTRUCTION"):
        equations = [{"label": [6, "hexagon_1_coface_0", 1,
                                  bytes(WIDTH).hex()], "coefficient": 1}]
        dual = {"normalization":
                "first contradiction multiplied by inverse RHS",
            "equations": equations, "support_count": 1,
            "support_sha256": sha_obj(equations), "normalized_rhs": 1,
            "yTz_mod3": 2,
            "all_108_annihilation_sha256": zero_vector_sha256(108),
            "all_108_annihilation_dimension": 108,
            "live_provenance_entries": 1, "witness_provenance_entries": 1,
            "peak_live_provenance_entries": 1,
            "target_boundary": {"first_target_ordinal": 6,
                "last_target_ordinal": 6, "target_ordinals": [6]},
            "target6_fixed_prefix_functional": True,
            "coordinate_encoding": {"label":
                "[target_ordinal,target_name,component,element_hex]",
                "component_numbering": "one_based_1_through_6",
                "E4_blob": "canonical permutation bytes then PC bytes",
                "permutation_width_bytes": 144, "pc_width_bytes": 10,
                "blob_width": WIDTH, "blob_hex_length": 2*WIDTH,
                "endianness": "byte-string order; no integer reinterpretation",
                "pivot_order": "component then exact E4 bytes"},
            "seed_manifest_sha256": "33"*32, "variables": 108}
        target = {"generation": 1, "variables": 108, "equations": 1,
            "rank": 0, "nullity": 108, "consistent": False,
            "row_space_sha256": "44"*32, "remainders_sha256": "55"*32,
            "live_remainder_entries": 1, "complete_all_coordinates": True,
            "stopped_at_first_contradiction": False, "dual": dual}
        canary = [1, bytes(WIDTH).hex(), 1]
        raw_lambda = {"algorithm":
                "general-reverse-canonical-pivot-DP/v1",
            "support_count": 1, "per_component": [1, 0, 0, 0, 0, 0],
            "packed_support_sha256": "66"*32,
            "packed_support_bytes": 156, "pivot_count": 0,
            "reverse_edge_visits": 0,
            "pivot_annihilation_sha256": zero_vector_sha256(0),
            "dependent_event_count": 16,
            "dependent_annihilation_sha256": zero_vector_sha256(16),
            "completed_block_column_count": 11,
            "completed_block_annihilation_sha256": zero_vector_sha256(11),
            "delta_annihilation_sha256": zero_vector_sha256(108),
            "base_z_scalar": 2, "negative_base_scalar": 1,
            "normalized_dual_whole_sha256": sha_obj(dual),
            "support_rows_not_serialized": True,
            "pool_IDs_or_old_qstar_used": False,
            "first_canary": canary, "last_canary": canary}
        correlation = {"complete": True, "generation": 1,
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
            "pool_or_basis_mutated": False,
            "cumulative_pass1_pairs": 10, "cumulative_pass2_pairs": 0}
        generation = {"generation": 1, "basis": basis, "target": target,
            "raw_lambda": raw_lambda, "correlation": correlation,
            "preflight": {}, "commit": {}, "incremental": {},
            "classification": "FULL_D2_OBSTRUCTION"}
        row["generation_ledger"] = [generation]
        row["full_D2_separator"] = {"generation": 1,
            "raw_lambda": raw_lambda, "correlation": correlation,
            "active_row_count": 0,
            "complete_76_occurrence_full_11_relator_correlation": True,
            "annihilates_full_D2": True, "lambda_delta_all_zero": True,
            "lambda_base_z": 2, "registered_108_family_only": True,
            "pinned_E4_roof_only": True}
        row["packed_block_ledger"] = _empty_packed_ledger_fixture()
        row["reason"] = TERMINAL_REASONS[token]
        phases = {"dual_lift_g1": 0.0, "correlation_g1": 0.0,
                  "receipt_serialization": 0.0}
    elif token.endswith("UNKNOWN_INPUT"):
        row["phase"] = "authenticated_input"
        row["reason"] = TERMINAL_REASONS[token]
        row["input_errors"] = ["sealed q3 drift"]
    else:
        detail = {"cap_reason": "producer_soft_rss_bytes",
            "cap_key": "producer_soft_rss_bytes", "cap_source": "local",
            "cap_limit": CAPS["producer_soft_rss_bytes"],
            "observed_count": CAPS["producer_soft_rss_bytes"],
            "comparator": "ge", "phase": "authenticated_input",
            "detail": None, "inner_phase": "authenticated_input",
            "current": {}}
        packed = {"format": "complete-D2-block-ledger/v1-partial",
            "translation_count": 0, "translation_decoded_bytes": 0,
            "translation_sha256": sha_bytes(b""), "record_bytes": 225,
            "record_count": 0, "decoded_bytes": 0,
            "decoded_sha256": sha_bytes(b""),
            "base64_omitted_for_resource_partial": True}
        row["phase"] = "authenticated_input"; row["reason"] = detail["cap_key"]
        row["resource_guards"] = {"resource_hit": True,
            "resource": detail, "local_and_upstream_separate": True,
            "reason_equals_cap_key": True}
        row["partial"] = {"phase": detail["phase"],
            "reason": detail["cap_key"], "current": {},
            "completed_generation_count": 0, "completed_batch_count": 0,
            "completed_new_translation_block_count": 0,
            "current_generation": None,
            "packed_block_ledger_prefix": packed,
            "selected_proof": None, "full_D2_separator": None}
    hit = row["reason"] if token.endswith("UNKNOWN_RESOURCE") else None
    row["performance"] = {"initial_remaining_seconds": 30.0,
        "elapsed_seconds": 1.0, "remaining_seconds": 29.0,
        "checks": 1, "peak_rss_bytes": 0, "hit_reason": hit,
        "callback_count": 1, "receipt_bytes": 0,
        "phase_seconds": phases, "correlation_pool_intern_calls": 0,
        "correlation_full_sparse_vectors_materialized": 0,
        "full_E4_enumerations": 0, "hard_outer_allowance_seconds": 18000}
    return row


def self_test() -> None:
    """Bounded independent production-core fixtures; never builds B0."""
    global CHECKER_STARTED, CHECKER_DEADLINE, CHECKER_CHECKS
    global _PREDECESSOR_RUNTIME, _PREDECESSOR_FIXTURE_REUSE
    authenticate(); mutations = 0; fixture_scope_repairs = 0
    completed_resource_envelopes = 0

    def expect_failure(call: Callable[[], Any], label: str) -> None:
        nonlocal mutations
        try:
            call()
        except Exception:
            mutations += 1; return
        raise RuntimeError("checker mutation accepted: "+label)

    # The frozen v1 source supplies every inherited checker marker exactly
    # once.  Reuse the exact predecessor tuple it leaves bound instead of
    # re-running v4 or colliding with its fixed module names.
    v1 = load_v1_fixture(); v1.self_test()
    inherited = v1.predecessor_modules(fixture_reuse=True)
    require(len(inherited) == 6 and
            all(module is not None for module in inherited),
            "checker inherited v1 predecessor tuple")
    _PREDECESSOR_RUNTIME = inherited
    _PREDECESSOR_FIXTURE_REUSE = True
    v4 = inherited[5]
    modules1 = predecessor_modules(fixture_reuse=True)
    modules2 = predecessor_modules(fixture_reuse=True)
    require(all(left is right for left, right in zip(modules1, modules2)) and
            Path(v4.__file__).resolve() == (ROOT/V4_CHECKER).resolve() and
            Path(v4.__file__).stat().st_size == V4_CHECKER_BYTES and
            sha_file(Path(v4.__file__)) == V4_CHECKER_SHA and
            callable(modules1[4].inv_word) and
            hasattr(modules1[3], "CAPS_157ED") and
            not hasattr(modules1[3], "CAPS"),
            "checker exact predecessor lifecycle reuse")
    v2_fixture, _, eg_fixture, ed_fixture, old_fixture, _ = modules1
    for name, expected in ((v2_fixture.FIXTURE_ED_MODULE_NAME, ed_fixture),
                           (v2_fixture.FIXTURE_OLD_MODULE_NAME, old_fixture)):
        require(sys.modules.get(name) is expected,
                "checker inherited fixture module identity")
        sys.modules[name] = object()
        try:
            expect_failure(lambda: v2_fixture.loaded_fixture_checker_modules(
                eg_fixture), "checker wrong-bound module " + name)
        finally:
            sys.modules[name] = expected
    require(v2_fixture.loaded_fixture_checker_modules(eg_fixture) ==
            (ed_fixture, old_fixture),
            "checker fixture modules restored after canaries")

    # Exercise the same checker-only typed translation/D1 gate used for every
    # production staged column.  The toy carries the real 144+10 byte Element
    # shape; neither mutation is a schema-only shortcut.
    typed_gate_before = mutations
    toy_identity = (tuple(range(144)), (0,)*10)
    toy_value = (tuple(reversed(range(144))), (1,)*10)
    toy_direct = {(1, element_blob(toy_value)): 1}
    toy_base = {(1, toy_value): 1}
    class TypedGateE4:
        identity = toy_identity
    class TypedGateOld:
        @staticmethod
        def translate(vector: dict[Any, int], value: Any,
                      quotient: Any) -> dict[Any, int]:
            del value, quotient
            return dict(vector)
        @staticmethod
        def boundary1(vector: dict[Any, int], quotient: Any) -> dict[Any, int]:
            del vector, quotient
            return {}
    raw_sha, typed_sha = independent_staged_column(TypedGateOld(),
        TypedGateE4(), toy_base, toy_identity, toy_direct, toy_identity)
    require(raw_sha == typed_sha == sha_bytes(semantic_bytes(toy_direct)),
            "checker typed-stage production-core fixture")
    class WrongTypedGateOld(TypedGateOld):
        @staticmethod
        def translate(vector: dict[Any, int], value: Any,
                      quotient: Any) -> dict[Any, int]:
            del value, quotient
            return {key: 2 for key in vector}
    class WrongBoundaryGateOld(TypedGateOld):
        @staticmethod
        def boundary1(vector: dict[Any, int], quotient: Any) -> dict[Any, int]:
            del vector, quotient
            return {toy_identity: 1}
    expect_failure(lambda: independent_staged_column(WrongTypedGateOld(),
        TypedGateE4(), toy_base, toy_identity, toy_direct, toy_identity),
        "checker wrong typed translation")
    expect_failure(lambda: independent_staged_column(WrongBoundaryGateOld(),
        TypedGateE4(), toy_base, toy_identity, toy_direct, toy_identity),
        "checker nonzero translated D1")
    require(mutations-typed_gate_before == 2,
            "checker typed-stage mutation count")

    # The real B0 checker basis remains an instrumented subclass.  Exercise
    # the same adapter used by production to mirror EI's intentional direct
    # base-reducer dispatch for fixed B1, then require clean detachment.
    class DispatchBasis:
        base_calls = 0; instrumented_calls = 0
        def add_column(self, relator: int, translation: int) -> bool:
            if getattr(self, "_em_disable_instrumentation", False):
                self.base_calls += 1
            else:
                self.instrumented_calls += 1
            return True
    class DispatchV2:
        @staticmethod
        def _replay_block(old: Any, e4: Any, pool: Any, basis: Any,
                          oracle: Any, claimed: Any, **kwargs: Any) -> Any:
            basis.add_column(1, 0)
            return ({"pre_accounting": {"columns": 0, "pivots": 0,
                "dependent": 0, "live_sparse_entries": 0},
                "post_accounting": {"columns": 1, "pivots": 1,
                "dependent": 0, "live_sparse_entries": 1},
                "rank_gain": 1, "raw_rows": [], "shadow_rows": [],
                "old_qstar_scalars": []}, 0, [])
    dispatch_basis = DispatchBasis()
    replay_fixed_B1_prefix(DispatchV2(), None, None, None,
                           dispatch_basis, None, None,
                           completed=0, raw_count=0, shadow_count=0)
    require(dispatch_basis.base_calls == 1 and
            dispatch_basis.instrumented_calls == 0 and
            not hasattr(dispatch_basis, "_em_disable_instrumentation"),
            "checker fixed-B1 base-dispatch fixture")

    upstream_fixture = expected_upstream_caps(
        modules1[2], modules1[3], modules1[4])
    require(upstream_fixture == EXPECTED_UPSTREAM_CAPS,
            "checker selftest literal upstream cap values")
    four = [_fixture_receipt(token) for token in sorted(TERMINALS)]
    semantic_rows = [{(1, bytes(WIDTH).hex()): 1}]+[{} for _ in range(108)]
    semantic_digest = semantic_remainders_sha256(semantic_rows)
    ledger_digest = sha_obj([{"ordinal": ordinal,
        "entry_count": int(ordinal == 0)} for ordinal in range(109)])
    require(semantic_digest != ledger_digest,
            "checker fixture semantic/summary digest separation")
    for receipt in four:
        if receipt["terminal_token"].endswith((
                "CONSISTENT", "FULL_D2_OBSTRUCTION")):
            receipt["initial_target"] = {
                "target6": {"fresh_remainder_sha256": ledger_digest},
                "affine_system": {},
                "fresh_B1_stable_digests_all_equal": True,
                "raw_gradient_count": 109,
                "raw_gradients_sha256": "99"*32,
                "semantic_remainders_sha256": semantic_digest}
            receipt["generation_ledger"][0]["target"][
                "remainders_sha256"] = semantic_digest
            receipt["performance"]["phase_seconds"]["initial_target"] = 0.0
    consistent = next(row for row in four if row["terminal_token"].endswith(
        "CONSISTENT"))
    obstruction = next(row for row in four if row["terminal_token"].endswith(
        "FULL_D2_OBSTRUCTION"))
    resource = next(row for row in four if row["terminal_token"].endswith(
        "UNKNOWN_RESOURCE"))
    for receipt in four:
        if receipt in (consistent, obstruction):
            continue
        validate_envelope(receipt, 0, upstream_fixture,
                          sealed_bounded_fixture=True)

    # Full-envelope RESOURCE fixture for the exact run-32439034163 boundary:
    # fixed B1 and its anchor are committed, all 109 initial target rows have
    # a semantic digest distinct from the public summary ledger, generation
    # one binds that semantic digest, and classification remains uncommitted
    # while dual lift is attempted.  Every object goes through the production
    # top/stage/generation validators; ``sealed_bounded_fixture`` changes only
    # frozen cardinalities, never keysets or cross-bindings.
    zero_hex = bytes(WIDTH).hex()
    context_rows = [{"context_id": index, "left_hex": zero_hex,
        "right_hex": zero_hex} for index in range(1, 32)]
    named_uses = [{"name": f"fixture_context_{index}",
        "context_id": (index-1) % 31+1} for index in range(1, 47)]
    context_registry = {"context_count": 31, "contexts": context_rows,
        "named_uses": named_uses, "named_use_count": 46,
        "named_use_mapping_sha256": sha_obj(named_uses),
        "context_rows_sha256": sha_obj(context_rows),
        "deduplication": "exact E4 pair equality"}
    seed_words = [[index+1] for index in range(108)]
    old_seeds, new_seeds = seed_words[:104], seed_words[104:]
    early = {
        "base_q3_replay": {"fixed_word": [], "roof_exponent": 2,
            "roof_order": 9, "arithmetic_outside_by_index_three": True,
            "marking_m": 0, "lambda": 1,
            "hexagon_residual_words_F2": [[], []],
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
            "cube_count": 26, "old_seed_words": old_seeds,
            "old_seed_count": 104, "new_seed_words": new_seeds,
            "new_seed_count": 4, "seed_words": seed_words,
            "seed_count": 108,
            "old_seed_digest_sha256": sha_obj(old_seeds),
            "new_seed_digest_sha256": sha_obj(new_seeds),
            "digest_obj_sha256": sha_obj(seed_words),
            "cube_digest_sha256": sha_obj(
                [[index] for index in range(26)]),
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
    occurrences = [{"relator_index": index, "component": 1,
        "coefficient": 1, "element_hex": zero_hex, "section_word": []}
        for index in range(1, 12)]
    base_columns = {"D1_D2_zero_all": True, "occurrence_count": 11,
        "occurrences": occurrences,
        "order": "relator,component,first occurrence",
        "ordered_sha256": sha_obj(occurrences),
        "per_component_counts": [11, 0, 0, 0, 0, 0],
        "per_relator_counts": [1]*11, "private_fields_published": False,
        "quotient_identity_all": True}
    directed_support = {"all_prefix_sections_directly_replayed": True,
        "occurrence_count": 11, "occurrences": copy.deepcopy(occurrences),
        "order": base_columns["order"],
        "ordered_sha256": base_columns["ordered_sha256"]}
    empty_sha = sha_obj([])
    prefix_counts = {"BFS_translations": 1, "columns": 11,
        "dependent_columns": 0, "directed_translations": 0,
        "live_sparse_entries": 11, "pivots": 11,
        "row_tail_visits": 0}
    prefix_accounting = {"BFS_translations": 1, "columns": 11,
        "dependent_columns": 0, "directed_translations": 0,
        "element_pool": {}, "live_sparse_entries": 11, "pivots": 11,
        "provenance_DAG": {}, "single_shared_basis": True,
        "targeted_translations_for_six_questions": 0,
        "total_translation_blocks": 1}
    prefix = {"counts": prefix_counts, "accounting": prefix_accounting,
        "basis_gate": {}, "prefix_pool_checkpoint": 1,
        "pool_order_sha256": "10"*32, "dependent_events": [],
        "dependent_event_count": 0, "dependent_event_sha256": empty_sha,
        "fresh_not_imported": True, "source_sha256": "11"*32,
        "stable_rounds_projection_sha256": empty_sha,
        "translations_sha256": empty_sha, "columns_sha256": "12"*32,
        "blocker_history_sha256": empty_sha,
        "complete_block_registry": {"translation_count": 1,
            "relators_per_translation": 11,
            "all_masks_equal_0x7ff": True,
            "canonical_translation_sha256": "13"*32,
            "semantic_blob_order": "exact E4 blob lexicographic",
            "pool_IDs_public": False}}
    surgery = {"blocker_history": [], "blocker_history_sha256": empty_sha,
        "bounded_prefix_sha256": "14"*32, "column_count": 0,
        "column_order": "translation first-seen order, relator 1..11",
        "columns_sha256": prefix["columns_sha256"], "round_count": 0,
        "rounds": [], "rounds_sha256": empty_sha,
        "section_expressions": {}, "section_oracle": {},
        "stable_projection_omits_exactly": ["elapsed_seconds", "RSS_bytes"],
        "stable_rounds_projection": [],
        "stable_rounds_projection_sha256":
            prefix["stable_rounds_projection_sha256"],
        "stop_reason": "no_new_exact_directed_translation", "theorem": {},
        "translation_count": 0, "translations": [],
        "translations_sha256": empty_sha,
        "volatile_rounds_sha256_provenance_only": "15"*32}
    raw_columns = [{"entries": [[1, zero_hex, 1]], "entry_count": 1,
        "byte_length": WIDTH+2, "sha256": "16"*32,
        "encoding": "component-u8|E4-blob-154|coefficient-u8",
        "order": "component then exact canonical E4 bytes"}
        for _ in range(11)]
    basis_post = {"columns": 11, "pivots": 11, "dependent": 0,
        "live_sparse_entries": 11, "pool_size": 12,
        "pool_order_sha256": "17"*32, "DAG_nodes": 12,
        "DAG_edges": 11, "section_bindings": 1,
        "section_expression_nodes": 1, "section_expression_edges": 0}
    block_columns = [{"relator_index": index,
        "translation_ordinal": 1, "translation_hex": zero_hex,
        "termwise_equals_direct_left_translation": True,
        "quotient_identity": True, "D1_D2_zero": True,
        "old_qstar_scalar": int(index == 9), "independent": True,
        "pivot": {"component": 1, "element_hex": zero_hex,
            "reduced_row": copy.deepcopy(raw_columns[index-1])},
        "raw_column": copy.deepcopy(raw_columns[index-1])}
        for index in range(1, 12)]
    fixed_block = {"complete": True, "translation_ordinal": 1,
        "translation_hex": zero_hex, "section_newly_registered": True,
        "section_word_length": 0, "section_word_sha256": empty_sha,
        "columns": block_columns, "column_count": 11,
        "column_order": "relator indices 1 through 11",
        "old_qstar_scalars": [0]*8+[1, 0, 0],
        "raw_columns_sha256": sha_obj(raw_columns),
        "reducer_ledger_sha256": sha_obj(block_columns),
        "pre_accounting": {**basis_post, "columns": 0, "pivots": 0,
            "live_sparse_entries": 0, "pool_size": 1, "DAG_nodes": 1,
            "DAG_edges": 0, "section_bindings": 0},
        "post_accounting": basis_post, "rank_gain": 11,
        "shadow_rank_mod_B0": 11, "two_rank_computations_equal": True,
        "relator9_independent": True, "pivot_count_before_relator9": 8,
        "pivot_count_after_relator9": 9,
        "lexfirst_active_provenance": {"component": 4,
            "relator_index": 9, "scalar": 1,
            "translation_hex": zero_hex, "section_word_sha256": empty_sha},
        "all_11_rows_are_D2_columns": True}
    fixed_anchor = {"after_complete_block": True, "basis_columns": 11,
        "basis_pivots": 11, "basis_dependent": 0,
        "basis_live_sparse_entries": 11, "pool_size": 12,
        "DAG_nodes": 12, "DAG_edges": 11, "section_bindings": 1,
        "translation_retained": True,
        "anchor_semantic_sha256": "18"*32,
        "private_anchor_ids_not_exported": True}
    parents = [{"source_word_ordinal": index, "word_length": 0,
        "word_sha256": "19"*32, "gradient_entry_count": 0,
        "gradient_sha256": "1a"*32,
        "all_nonzero_terms_parented": True} for index in range(109)]
    initial = {"target6": {"fresh_remainder_sha256": ledger_digest},
        "affine_system": {}, "fresh_B1_stable_digests_all_equal": True,
        "raw_gradient_count": 109, "raw_gradients_sha256": "1b"*32,
        "semantic_remainders_sha256": semantic_digest}
    sealed_resource = copy.deepcopy(resource)
    sealed_resource.update(copy.deepcopy(early))
    sealed_resource.update({"directed_base_support": directed_support,
        "directed_surgery": surgery, "prefix_B0": prefix,
        "base_columns": base_columns, "fixed_B1_block": fixed_block,
        "fixed_B1_anchor": fixed_anchor,
        "old_qstar_boundary": {
            "used_only_to_freshly_reconstruct_fixed_B1": True,
            "used_after_fixed_B1": False, "support_count": 1,
            "support_sha256": "1c"*32,
            "complete_correlation_sha256": "1d"*32},
        "raw_parent_manifest": {"source_count": 109, "rows": parents,
            "rows_sha256": sha_obj(parents),
            "source_word_order":
                "base target6 then registered seeds 1..108",
            "signed_offset_convention":
                "positive uses prefix before letter; negative uses prefix after inverse"},
        "recovery_map": _fixture_recovery_public(),
        "initial_target": initial})
    basis = {**basis_post, "pool_order_sha256": None,
             "recovery": _fixture_recovery_public()}
    completed_prefix_fields = ("base_q3_replay",
        "normalized_inverse_fibre", "seed_manifest", "source_preflight",
        "directed_base_support", "directed_surgery", "prefix_B0",
        "base_columns", "fixed_B1_block", "fixed_B1_anchor",
        "old_qstar_boundary", "raw_parent_manifest", "recovery_map")
    for normal in (consistent, obstruction):
        for field in completed_prefix_fields:
            normal[field] = copy.deepcopy(sealed_resource[field])
        normal_initial = copy.deepcopy(initial)
        normal_initial["semantic_remainders_sha256"] = \
            normal["generation_ledger"][0]["target"]["remainders_sha256"]
        normal["initial_target"] = normal_initial
        normal["generation_ledger"][0]["basis"] = copy.deepcopy(basis)
        if normal is obstruction:
            raw0 = normal["generation_ledger"][0]["raw_lambda"]
            raw0["pivot_count"] = basis["pivots"]
            raw0["pivot_annihilation_sha256"] = zero_vector_sha256(
                basis["pivots"])
            normal["full_D2_separator"]["raw_lambda"] = raw0
        normal["performance"]["phase_seconds"] = {key: 0.0 for key in
            expected_phase_seconds_keys(normal)}
        validate_envelope(normal, 0, upstream_fixture,
                          sealed_bounded_fixture=True)

    for label, mutate in (
            ("terminal reason", lambda row: row.__setitem__("reason", "bad")),
            ("generation key", lambda row: row["generation_ledger"][0].
                __setitem__("extra", True)),
            ("raw lambda", lambda row: row["generation_ledger"][0][
                "raw_lambda"].pop("base_z_scalar")),
            ("correlation", lambda row: row["generation_ledger"][0][
                "correlation"].__setitem__("pass1_pair_attempts", 9)),
            ("separator", lambda row: row["full_D2_separator"].
                __setitem__("active_row_count", 1))):
        bad = copy.deepcopy(obstruction); mutate(bad)
        expect_failure(lambda bad=bad: validate_envelope(
            bad, 0, upstream_fixture, sealed_bounded_fixture=True), label)
    bad = copy.deepcopy(consistent); bad["selected_proof"]["extra"] = True
    expect_failure(lambda: validate_envelope(
        bad, 0, upstream_fixture, sealed_bounded_fixture=True),
        "selected proof key")
    semantic_mutations = mutations
    bad = copy.deepcopy(consistent)
    bad["initial_target"]["semantic_remainders_sha256"] = ledger_digest
    expect_failure(lambda: validate_envelope(
        bad, 0, upstream_fixture, sealed_bounded_fixture=True),
        "semantic digest replaced by summary ledger")
    bad = copy.deepcopy(consistent)
    bad["initial_target"]["target6"][
        "fresh_remainder_sha256"] = semantic_digest
    expect_failure(lambda: validate_envelope(
        bad, 0, upstream_fixture, sealed_bounded_fixture=True),
        "summary ledger replaced by semantic digest")
    altered_rows = copy.deepcopy(semantic_rows)
    altered_rows[0][(1, bytes(WIDTH).hex())] = 2
    bad = copy.deepcopy(consistent)
    bad["initial_target"]["semantic_remainders_sha256"] = \
        semantic_remainders_sha256(altered_rows)
    expect_failure(lambda: validate_envelope(
        bad, 0, upstream_fixture, sealed_bounded_fixture=True),
        "altered semantic coefficient")
    ordered_rows = [{(1, bytes(WIDTH).hex()): 1},
                    {(2, (bytes([1])+bytes(WIDTH-1)).hex()): 2}]
    ordered_rows.extend({} for _ in range(107))
    permuted_rows = [ordered_rows[1], ordered_rows[0], *ordered_rows[2:]]
    require(semantic_remainders_sha256(ordered_rows) !=
                semantic_remainders_sha256(permuted_rows),
            "checker semantic row order mutation")
    fake_initial = copy.deepcopy(consistent["initial_target"])
    fake_target = copy.deepcopy(consistent["generation_ledger"][0]["target"])
    fake_initial["semantic_remainders_sha256"] = "ab"*32
    fake_target["remainders_sha256"] = "ab"*32
    expect_failure(lambda: validate_fresh_semantic_binding(
        fake_initial, fake_target, semantic_rows, ledger_digest),
        "matching fake semantic strings without fresh replay")
    require(mutations-semantic_mutations == 4,
            "checker semantic binding mutation count")

    target = copy.deepcopy(obstruction["generation_ledger"][0]["target"])
    target["remainders_sha256"] = semantic_digest
    sealed_resource["generation_ledger"] = [{"generation": 1,
        "basis": basis, "target": target, "raw_lambda": {},
        "correlation": {}, "preflight": {}, "commit": {},
        "incremental": {}, "classification": None}]
    detail = {"cap_reason": "raw_lambda_reverse_edge_visits",
        "cap_key": "raw_lambda_reverse_edge_visits", "cap_source": "local",
        "cap_limit": CAPS["raw_lambda_reverse_edge_visits"],
        "observed_count": CAPS["raw_lambda_reverse_edge_visits"]+1,
        "comparator": "gt", "phase": "dual_lift", "detail": None,
        "inner_phase": None, "current": {"completed_reverse_pivots": 0}}
    sealed_resource["phase"] = "dual_lift"
    sealed_resource["reason"] = detail["cap_key"]
    sealed_resource["resource_guards"]["resource"] = detail
    sealed_resource["partial"].update({"phase": "dual_lift",
        "reason": detail["cap_key"], "current": copy.deepcopy(detail["current"]),
        "current_generation": 1})
    sealed_resource["performance"]["hit_reason"] = detail["cap_key"]
    sealed_resource["performance"]["phase_seconds"] = {
        "authenticated_input": 0.0, "source_preflight": 0.0,
        "fresh_B0": 0.0, "fixed_B1": 0.0, "initial_target": 0.0}
    validate_envelope(sealed_resource, 0, upstream_fixture,
                      sealed_bounded_fixture=True)
    bad = copy.deepcopy(sealed_resource)
    bad["generation_ledger"][0]["target"]["remainders_sha256"] = ledger_digest
    expect_failure(lambda bad=bad: validate_envelope(
        bad, 0, upstream_fixture, sealed_bounded_fixture=True),
        "RESOURCE old summary-ledger generation binding")
    bad = copy.deepcopy(sealed_resource)
    bad["initial_target"]["semantic_remainders_sha256"] = "ab"*32
    expect_failure(lambda bad=bad: validate_envelope(
        bad, 0, upstream_fixture, sealed_bounded_fixture=True),
        "RESOURCE stale initial semantic binding")
    completed_resource_envelopes = 1

    section_node_cap = 131_072
    section_word_cap = 100_000

    def cap12_array(raw: bytes, kind: str, code: str, itemsize: int,
                    cap: int, length: int) -> dict[str, Any]:
        return {"type": kind, "array_typecode": code,
            "endianness": "little", "length": length,
            "itemsize": itemsize, "byte_length": len(raw), "cap": cap,
            "sha256": sha_bytes(raw),
            "base64": base64.b64encode(raw).decode("ascii")}

    section_arrays = {
        "kind": cap12_array(bytes([4]), "uint8", "B", 1,
                             section_node_cap, 1),
        "signed_generator": cap12_array(bytes([0]), "int8", "b", 1,
                             section_node_cap, 1),
        "left": cap12_array(bytes(4), "uint32", "I", 4,
                             section_node_cap, 1),
        "right": cap12_array(bytes(4), "uint32", "I", 4,
                              section_node_cap, 1),
        "flat_offsets": cap12_array(bytes(8), "uint32", "I", 4,
                              section_node_cap+1, 2),
        "flat_letters": cap12_array(b"", "int16", "h", 2,
                              section_node_cap*section_word_cap, 0),
        "canonical_values": cap12_array(bytes(WIDTH), "uint8", "B", 1,
                              section_node_cap*WIDTH, WIDTH)}
    section_manifest = {name: {key: value for key, value in item.items()
        if key != "base64"} for name, item in section_arrays.items()}
    section_expression = {"format": "typed-section-expression-arrays/v1",
        "node_order": "zero_based_topological",
        "ordinary_word_composition": True,
        "canonical_value_width": WIDTH, "node_count": 1,
        "edge_count": 0, "roots": [0], "arrays": section_arrays,
        "manifest_sha256": sha_obj(
            {"arrays": section_manifest, "roots": [0]})}

    def cap12_recovery_after(row: dict[str, Any], generation: int) \
            -> dict[str, Any]:
        answer = copy.deepcopy(row)
        answer["candidate_edge_count"] += 76
        answer["translated_candidate_edge_count"] += 76
        answer["canonical_sha256"] = sha_obj(
            {"cap12_recovery_generation": generation,
             "prior": row["canonical_sha256"]})
        return answer

    def cap12_raw_lambda(generation: int, basis0: dict[str, Any],
                         target0: dict[str, Any], blob: bytes) \
            -> dict[str, Any]:
        canary = [1, blob.hex(), 1]
        columns = 11*generation
        return {"algorithm": "general-reverse-canonical-pivot-DP/v1",
            "support_count": 1, "per_component": [1, 0, 0, 0, 0, 0],
            "packed_support_sha256": sha_obj(canary),
            "packed_support_bytes": 156,
            "pivot_count": basis0["pivots"], "reverse_edge_visits": 0,
            "pivot_annihilation_sha256":
                zero_vector_sha256(basis0["pivots"]),
            "dependent_event_count": 16,
            "dependent_annihilation_sha256": zero_vector_sha256(16),
            "completed_block_column_count": columns,
            "completed_block_annihilation_sha256":
                zero_vector_sha256(columns),
            "delta_annihilation_sha256": zero_vector_sha256(108),
            "base_z_scalar": 2, "negative_base_scalar": 1,
            "normalized_dual_whole_sha256": sha_obj(target0["dual"]),
            "support_rows_not_serialized": True,
            "pool_IDs_or_old_qstar_used": False,
            "first_canary": canary, "last_canary": canary}

    def cap12_correlation(generation: int, blob: bytes, *,
                          selected: bool) -> dict[str, Any]:
        selected_count = int(selected)
        return {"complete": True, "generation": generation,
            "pass1_pair_attempts": 10,
            "pass2_pair_attempts": 10 if selected else 0,
            "pass2_selected_filter_count": selected_count,
            "candidate_count_before_zero_deletion": 1,
            "cancellation_to_zero_count": 0, "active_row_count": 1,
            "active_distinct_translation_count": 1,
            "scalar_distribution": {"1": 1, "2": 0},
            "active_packed_row_width": 156, "active_packed_bytes": 156,
            "active_packed_sha256": sha_bytes(
                bytes([1])+blob+bytes([9, 1])),
            "selected_translation_count": selected_count,
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

    def cap12_preflight(generation: int, basis0: dict[str, Any], blob: bytes,
                        specs: Sequence[tuple[int, bool,
                            list[Any] | None, str, str]]) -> dict[str, Any]:
        contributor_raw = bytes([1])+blob+bytes([1, 9])+ \
            struct.pack(">H", 9)+bytes(WIDTH)+bytes([1])
        selected = [{"generation": generation,
            "translation_ordinal": 1, "translation_hex": blob.hex(),
            "jstar": 9, "correlation_scalar": 1,
            "contributor": {"component": 1, "g_hex": blob.hex(),
                "lambda_coefficient": 1, "relator_index": 9,
                "occurrence_ordinal": 9, "h_hex": zero_hex,
                "base_coefficient": 1, "translation_hex": blob.hex(),
                "record_hex": contributor_raw.hex(),
                "record_sha256": sha_bytes(contributor_raw)},
            "g_recovery": {"kind": "direct_target_source_prefix",
                "component": 1, "element_hex": blob.hex(),
                "source_word_ordinal": 0, "signed_letter_offset": 1,
                "method": "target_word_signed_prefix", "word_length": 0,
                "word_sha256": sha_obj([])},
            "materialization_canary": {"word_length": 0,
                "word_sha256": sha_obj([]), "value_hex": blob.hex()},
            "expression_root": 0}]
        state = copy.deepcopy(basis0)
        state["pool_order_sha256"] = sha_obj(
            {"cap12_pre_state": generation})
        state["recovery"] = None
        binding = [[blob.hex(), relator, 1 if relator == 9 else 0,
                    raw_sha, typed_sha]
            for relator, _, _, raw_sha, typed_sha in specs]
        return {"generation": generation, "translation_count": 1,
            "column_count": 11, "staged_sparse_entries": 11,
            "all_selected_before_mutation": True,
            "all_eleven_before_mutation": True,
            "state_neutrality_before": state,
            "state_neutrality_after": copy.deepcopy(state),
            "section_provenance": {"selected": selected,
                "selected_count": 1, "selected_sha256": sha_obj(selected),
                "expression_DAG": copy.deepcopy(section_expression),
                "owned_inverse_materializer": True,
                "materialization_cadence": "first,last,and-every-64th",
                "all_values_exact": True},
            "row_binding_sha256": sha_obj(binding)}

    cap12_rows: list[dict[str, Any]] = []
    cap12_basis = copy.deepcopy(basis)
    cap12_remainder = initial["semantic_remainders_sha256"]
    translation_bytes = bytearray(); record_bytes = bytearray()
    for generation in range(1, 13):
        blob = bytes([generation])+bytes(WIDTH-1)
        translation_bytes.extend(blob)
        target0 = copy.deepcopy(target)
        target0["generation"] = generation
        target0["remainders_sha256"] = cap12_remainder
        specs: list[tuple[int, bool, list[Any] | None, str, str]] = []
        for relator in range(1, 12):
            independent = relator == 9
            pivot = [1, blob.hex()] if independent else None
            raw_sha = sha_obj({"generation": generation,
                               "relator": relator, "kind": "raw"})
            typed_sha = sha_obj({"generation": generation,
                                 "relator": relator, "kind": "typed"})
            specs.append((relator, independent, pivot, raw_sha, typed_sha))
            record_bytes.extend(encode_checker_record(generation, 1,
                relator, independent, 1 if relator == 9 else 0,
                pivot, raw_sha, typed_sha))
        correlation0 = cap12_correlation(generation, blob, selected=True)
        preflight0 = cap12_preflight(generation, cap12_basis, blob, specs)
        pre = copy.deepcopy(cap12_basis)
        pre["pool_order_sha256"] = sha_obj(
            {"cap12_commit_pre": generation})
        post = copy.deepcopy(pre)
        post.update({"columns": pre["columns"]+11,
            "pivots": pre["pivots"]+1,
            "dependent": pre["dependent"]+10,
            "live_sparse_entries": pre["live_sparse_entries"]+1,
            "pool_size": pre["pool_size"]+1,
            "DAG_nodes": pre["DAG_nodes"]+1,
            "DAG_edges": pre["DAG_edges"]+1,
            "section_bindings": pre["section_bindings"]+1,
            "section_expression_nodes": pre["section_expression_nodes"]+1,
            "section_expression_edges": pre["section_expression_edges"]+1,
            "recovery": cap12_recovery_after(pre["recovery"], generation)})
        outcomes = [{"translation_ordinal": 1, "relator": relator,
            "independent": independent,
            "lambda_scalar": 1 if relator == 9 else 0,
            "pivot": pivot} for relator, independent, pivot, _, _ in specs]
        commit0 = {"generation": generation, "complete": True,
            "translation_count": 1, "column_count": 11, "rank_gain": 1,
            "dependent_gain": 10, "pre_accounting": pre,
            "post_accounting": post,
            "first_translation_jstar_pivot": {"translation_ordinal": 1,
                "relator": 9, "scalar": 1, "pivot": [1, blob.hex()]},
            "outcome_semantic_sha256": sha_obj(outcomes),
            "all_blocks_complete": True,
            "all_staged_before_first_mutation": True}
        next_remainder = sha_obj(
            {"cap12_post_remainder_generation": generation})
        incremental0 = {"generation": generation,
            "completed_new_pivot_ordinal": 1,
            "completed_rows_in_current_pivot": 0,
            "pre_update_remainder_sha256": cap12_remainder,
            "last_fully_updated_row_sha256": sha_obj(
                {"cap12_last_row": generation}),
            "current_new_pivot_prefix_sha256": sha_obj([blob.hex()]),
            "new_pivot_count": 1,
            "reduction_order_sha256": sha_obj([[1, blob.hex()]]),
            "old_pivot_count": pre["pivots"],
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
            "post_update_remainder_sha256": next_remainder,
            "fresh_direct_cadence": [{"ordinal": ordinal,
                "sha256": sha_obj({"generation": generation,
                                    "ordinal": ordinal}), "equal": True}
                for ordinal in (0, 1, 54, 108)]}
        cap12_rows.append({"generation": generation,
            "basis": copy.deepcopy(cap12_basis), "target": target0,
            "raw_lambda": cap12_raw_lambda(
                generation, cap12_basis, target0, blob),
            "correlation": correlation0, "preflight": preflight0,
            "commit": commit0, "incremental": incremental0,
            "classification": "ACTIVE_BATCH_COMMITTED"})
        cap12_basis = copy.deepcopy(post)
        cap12_basis["pool_order_sha256"] = None
        cap12_remainder = next_remainder
    blob13 = bytes([13])+bytes(WIDTH-1)
    target13 = copy.deepcopy(target)
    target13["generation"] = 13
    target13["remainders_sha256"] = cap12_remainder
    cap12_rows.append({"generation": 13,
        "basis": cap12_basis, "target": target13,
        "raw_lambda": cap12_raw_lambda(13, cap12_basis, target13, blob13),
        "correlation": cap12_correlation(13, blob13, selected=False),
        "preflight": {}, "commit": {}, "incremental": {},
        "classification": None})
    cap12_resource = copy.deepcopy(sealed_resource)
    cap12_resource["generation_ledger"] = cap12_rows
    cap12_detail = {"cap_reason": "column_generation_batches",
        "cap_key": "column_generation_batches", "cap_source": "local",
        "cap_limit": 12, "observed_count": 13, "comparator": "gt",
        "phase": "correlation_pass1",
        "detail": "column_generation_batch_limit", "inner_phase": None,
        "current": {"generation": 13, "completed_batches": 12,
                    "completed_blocks": 12}}
    packed_prefix = {"format": "complete-D2-block-ledger/v1-partial",
        "translation_count": 12,
        "translation_decoded_bytes": len(translation_bytes),
        "translation_sha256": sha_bytes(bytes(translation_bytes)),
        "record_bytes": 225, "record_count": 132,
        "decoded_bytes": len(record_bytes),
        "decoded_sha256": sha_bytes(bytes(record_bytes)),
        "base64_omitted_for_resource_partial": True}
    cap12_resource["phase"] = cap12_detail["phase"]
    cap12_resource["reason"] = cap12_detail["cap_key"]
    cap12_resource["resource_guards"]["resource"] = cap12_detail
    cap12_resource["partial"].update({"phase": cap12_detail["phase"],
        "reason": cap12_detail["cap_key"],
        "current": copy.deepcopy(cap12_detail["current"]),
        "completed_generation_count": 12, "completed_batch_count": 12,
        "completed_new_translation_block_count": 12,
        "current_generation": 13,
        "packed_block_ledger_prefix": packed_prefix})
    cap12_resource["performance"]["hit_reason"] = cap12_detail["cap_key"]
    cap12_resource["performance"]["phase_seconds"] = {key: 0.0 for key in
        expected_phase_seconds_keys(cap12_resource)}
    validate_envelope(cap12_resource, 0, upstream_fixture,
                      sealed_bounded_fixture=True)
    for label, mutate in (
            ("old summary", lambda row: row["generation_ledger"][0][
                "target"].__setitem__("remainders_sha256", ledger_digest)),
            ("stale semantic", lambda row: row["initial_target"].__setitem__(
                "semantic_remainders_sha256", "bc"*32)),
            ("inner", lambda row: row["resource_guards"]["resource"].
                __setitem__("inner_phase", "correlation_pass1")),
            ("current", lambda row: (row["resource_guards"]["resource"][
                "current"].__setitem__("completed_blocks", 11),
                row["partial"]["current"].__setitem__(
                    "completed_blocks", 11))),
            ("generation order", lambda row: row["generation_ledger"][5].
                __setitem__("generation", 7))):
        bad = copy.deepcopy(cap12_resource); mutate(bad)
        expect_failure(lambda bad=bad: validate_envelope(
            bad, 0, upstream_fixture, sealed_bounded_fixture=True),
            "cap12 RESOURCE " + label)
    completed_resource_envelopes += 1

    generation13 = {"cap_reason": "column_generation_batches",
        "cap_key": "column_generation_batches", "cap_source": "local",
        "cap_limit": 12, "observed_count": 13, "comparator": "gt",
        "phase": "correlation_pass1", "detail":
            "column_generation_batch_limit",
        "inner_phase": None, "current": {
            "generation": 13, "completed_batches": 12,
            "completed_blocks": 8}}
    validate_bounded_active_resource(generation13, 12, 13, 8)
    wrong_generation13 = copy.deepcopy(generation13)
    wrong_generation13["cap_limit"] = 8
    expect_failure(lambda: validate_bounded_active_resource(
        wrong_generation13, 12, 13, 8), "stale generation-9 batch cap")
    wrong_inner_generation13 = copy.deepcopy(generation13)
    wrong_inner_generation13["inner_phase"] = "correlation_pass1"
    expect_failure(lambda: validate_bounded_active_resource(
        wrong_inner_generation13, 12, 13, 8),
        "forged generation-13 inner phase")
    total_cap = copy.deepcopy(generation13)
    total_cap.update({"cap_reason": "total_new_translation_blocks",
        "cap_key": "total_new_translation_blocks", "cap_limit": 4096,
        "observed_count": 4097,
        "detail": "total_translation_block_budget_exhausted"})
    total_cap["current"] = {"generation": 13, "completed_batches": 12,
                            "completed_blocks": 4096}
    validate_bounded_active_resource(total_cap, 12, 13, 4096)
    for label, mutate in (
            ("resource source", lambda row: row["resource_guards"][
                "resource"].__setitem__("cap_source", "upstream")),
            ("resource inner", lambda row: row["resource_guards"][
                "resource"].__setitem__("inner_phase", "fresh_B0")),
            ("resource current", lambda row: row["resource_guards"][
                "resource"]["current"].__setitem__("forged", 1))):
        bad = copy.deepcopy(resource); mutate(bad)
        expect_failure(lambda bad=bad: validate_envelope(
            bad, 0, upstream_fixture, sealed_bounded_fixture=True), label)

    bad = copy.deepcopy(consistent)
    bad["upstream_caps"]["element_pool"] -= 1
    bad["upstream_caps_sha256"] = sha_obj(bad["upstream_caps"])
    expect_failure(lambda bad=bad: validate_envelope(
        bad, 0, upstream_fixture, sealed_bounded_fixture=True),
        "literal upstream cap value")

    # Independent general reverse-lift fixture.
    blob_p, blob_f = bytes([1])+bytes(WIDTH-1), bytes([2])+bytes(WIDTH-1)
    class ToyPool:
        values = [blob_p, blob_f]
        def pivot_order(self, packed: int) -> tuple[int, bytes]:
            return 1, self.values[packed]
        def value(self, packed: int) -> bytes:
            return self.values[packed]
    class ToyOld:
        @staticmethod
        def replay_unpack_key(packed: int) -> tuple[int, int]:
            return 1, packed
    class ToyBasis:
        rows = {0: {0: 1, 1: 1}}
    dual = {"normalized_rhs": 1, "yTz_mod3": 2, "support_count": 1,
        "equations": [{"label": [6, "hexagon_1_coface_0", 1,
                                    blob_f.hex()], "coefficient": 1}]}
    class ToySystem:
        consistent = False
        @staticmethod
        def dual_public() -> dict[str, Any]:
            return dual
    remainders = [{(1, blob_f.hex()): 2}]+[{} for _ in range(108)]
    lifted, _ = reverse_lift(ToyOld(), ToyPool(), ToyBasis(), ToySystem(),
                             remainders, [], [])
    require(lifted[(1, blob_p)] == 2 and lifted[(1, blob_f)] == 1,
            "checker reverse-lift fixture")
    fixture_scope_repairs += 1

    # Tiny nonabelian complete two-pass correlation through the production
    # checker core.  The 154-byte representation is retained exactly.
    class ToyE4:
        identity = (tuple(range(3)), (0,)*151)
        def mul(self, left: Any, right: Any) -> Any:
            return (tuple(left[0][right[0][index]] for index in range(3)),
                    (0,)*151)
        def inverse(self, value: Any) -> Any:
            inverse = [0]*3
            for index, image in enumerate(value[0]):
                inverse[image] = index
            return tuple(inverse), (0,)*151
    toy_e4 = ToyE4()
    g_cycle = ((1, 2, 0), (0,)*151)
    g_swap = ((1, 0, 2), (0,)*151)
    class CorrelationPool:
        @staticmethod
        def unpack(blob: bytes) -> Any:
            return tuple(blob[:3]), tuple(blob[3:])
    occurrences = [{"component": 1, "_value": toy_e4.identity,
        "element_hex": element_blob(toy_e4.identity).hex(),
        "relator_index": 1, "occurrence_ordinal": 1, "coefficient": 1},
        {"component": 1, "_value": g_swap,
        "element_hex": element_blob(g_swap).hex(),
        "relator_index": 2, "occurrence_ordinal": 2, "coefficient": 2}]
    support = [[1, element_blob(g_cycle).hex(), 1],
               [1, element_blob(g_swap).hex(), 2]]
    cumulative = {"pass1": 0, "pass2": 0}
    correlation = independent_correlation(toy_e4, CorrelationPool(), support,
        occurrences, 1, cumulative, 4)
    require(correlation["public"]["pass1_pair_attempts"] == 4 and
            correlation["public"]["pass2_pair_attempts"] == 4 and
            correlation["public"]["pool_or_basis_mutated"] is False,
            "checker nonabelian complete correlation fixture")
    omitted = independent_correlation(toy_e4, CorrelationPool(), support,
        occurrences[:1], 1, {"pass1": 0, "pass2": 0}, 4)
    expect_failure(lambda: require(omitted["public"]["active_packed_sha256"] ==
        correlation["public"]["active_packed_sha256"],
        "checker omitted occurrence digest"), "correlation omitted occurrence")
    wrong_orientation = toy_e4.mul(toy_e4.inverse(g_swap), g_cycle)
    expect_failure(lambda: require(toy_e4.mul(wrong_orientation, g_swap) ==
        g_cycle, "checker wrong h^-1*g orientation"),
        "correlation inverse orientation")

    # All 109 rows are freshly reduced, while only four are published.
    blob_new = bytes(WIDTH)
    require(blob_new < blob_p < blob_f,
            "checker incremental fixture semantic pivot order")
    fixture_scope_repairs += 1
    class IncrementalPool:
        values = [blob_new, blob_p, blob_f]
        def pivot_order(self, packed: int) -> tuple[int, bytes]:
            return 1, self.values[packed]
    class IncrementalOld:
        calls = 0
        @staticmethod
        def replay_unpack_key(packed: int) -> tuple[int, int]:
            return 1, packed
        @classmethod
        def checker_probe_remainder(cls, ordinal: int, pool: Any,
                                    basis: Any) -> dict[tuple[int, str], int]:
            cls.calls += 1
            return ({(1, blob_f.hex()): 1} if ordinal % 2 == 0 else {})
    class IncrementalBasis:
        rows = {1: {1: 1, 2: 1}, 0: {0: 1, 1: 1}}
    before = [({(1, blob_new.hex()): 1} if index % 2 == 0 else {})
              for index in range(109)]
    checker_clock_before = (CHECKER_STARTED, CHECKER_DEADLINE, CHECKER_CHECKS)
    fixture_now = time.monotonic(); fixture_checks = -1
    CHECKER_STARTED = fixture_now
    CHECKER_DEADLINE = fixture_now+30.0
    CHECKER_CHECKS = 0
    try:
        updated, incremental = checker_incremental(IncrementalOld(),
            IncrementalPool(), IncrementalBasis(), before,
            {1: {1: 1, 2: 1}}, [0], list(range(109)), 1)
        fixture_checks = CHECKER_CHECKS
    finally:
        CHECKER_STARTED, CHECKER_DEADLINE, CHECKER_CHECKS = checker_clock_before
    require(fixture_checks == 109 and
            (CHECKER_STARTED, CHECKER_DEADLINE, CHECKER_CHECKS) ==
                checker_clock_before,
            "checker incremental fixture exact deadline scope")
    fixture_scope_repairs += 1
    require(IncrementalOld.calls == 109 and
            incremental["fresh_direct_cadence"] == [{"ordinal": ordinal,
                "sha256": sha_obj(sorted(updated[ordinal].items())),
                "equal": True} for ordinal in (0, 1, 54, 108)],
            "checker all-109 independent cadence fixture")

    # Packed 225-byte decoder and a canonical-endian mutation.
    translation = bytes([7])*WIDTH; records = bytearray()
    for relator in range(1, 12):
        records.extend(bytes([1])+struct.pack("<H", 1)+
            bytes([relator, 0x0e, 0, 0])+bytes(WIDTH)+bytes(64))
    encoded_t = base64.b64encode(translation).decode("ascii")
    encoded_r = base64.b64encode(records).decode("ascii")
    packed = _empty_packed_ledger_fixture(); packed.update({
        "translation_count": 1, "translation_decoded_bytes": WIDTH,
        "translation_sha256": sha_bytes(translation),
        "translation_base64_length": len(encoded_t),
        "translation_base64_sha256": sha_bytes(encoded_t.encode("ascii")),
        "translation_base64": encoded_t, "record_count": 11,
        "decoded_bytes": len(records), "decoded_sha256": sha_bytes(records),
        "base64_length": len(encoded_r),
        "base64_sha256": sha_bytes(encoded_r.encode("ascii")),
        "base64": encoded_r})
    translations, rows, _ = decode_packed_ledger(packed)
    require(translations == [translation] and len(rows) == 11,
            "checker packed-225 fixture")
    bad_packed = copy.deepcopy(packed); bad_packed["record_endianness"] = "big"
    expect_failure(lambda: decode_packed_ledger(bad_packed), "packed endian")

    require(len(four) == 4 and mutations >= 10 and
            fixture_scope_repairs == 3 and
            completed_resource_envelopes == 2,
            "checker bounded fixture counters")
    print("D972_B345_TARGET6_DUAL_COLGEN_V2_CHECKER_SELFTEST_PASS "
          "independent_reverse_lift=1 independent_correlation=1 "
          "incremental_all109=1 packed_225=1 terminals=4 "
          "stable_schema=1 resource_schema=1 lifecycle_reuse=1 "
          "fixed_B1_dispatch=1 typed_stage_core=1 "
          "typed_stage_mutations=2 "
          "fixture_scope_repairs=3 "
          "completed_initial_resource_envelope=1 "
          "cap12_resource_envelope=1 "
          "semantic_remainders=1 semantic_mutations=4 "
          "generation_13_resource=1 inherited_157em_v1=1 "
          f"mutations={mutations} inherited_157el_v4=1", flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--q3", type=Path, default=ROOT/Q3_PATH)
    parser.add_argument("--receipt", type=Path, default=ROOT/OUTPUT)
    parser.add_argument("--seconds", type=float, default=18_000.0)
    args = parser.parse_args(argv)
    if args.self_test:
        self_test(); return 0
    data = check_receipt(args.q3, args.receipt, seconds=args.seconds)
    print("D972_B345_TARGET6_DUAL_COLGEN_V2_CHECKER_PASS "
          f"terminal={data['terminal_token']} receipt={args.receipt}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
